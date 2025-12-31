"""
Agent Workflow Nodes
Each node is a step in the agent's thinking process.
"""

from typing import Dict, Any
from ..llm.groq_client import GroqClient
from ..llm.prompts import (
    analyze_question_prompt,
    generate_sql_prompt,
    fix_sql_prompt,
    generate_answer_prompt
)
from ..mcp.tools import DatabaseTools
from ..cache.schema_cache import SchemaCache


class WorkflowNodes:
    """Individual steps in the agent workflow"""
    
    def __init__(self, groq_client: GroqClient, db_tools: DatabaseTools, 
                 schema_cache: SchemaCache):
        """
        Initialize workflow nodes.
        
        Args:
            groq_client: Groq API client
            db_tools: Database tools
            schema_cache: Schema cache
        """
        self.groq = groq_client
        self.db = db_tools
        self.cache = schema_cache
    
    def analyze_question(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 1: Identify which tables are needed.
        Token cost: ~100-150 tokens
        """
        print("\n[1/5] Analyzing question...")
        
        # Get available tables
        available_tables = self.db.list_tables()
        
        # Create prompt
        prompt = analyze_question_prompt(state["user_question"], available_tables)
        
        # Ask Groq
        response = self.groq.chat([
            {"role": "user", "content": prompt}
        ], max_tokens=50)
        
        if not response["success"]:
            return {
                **state,
                "execution_error": f"Failed to analyze question: {response['error']}",
                "tokens_used": state["tokens_used"] + response["tokens_used"]
            }
        
        # Parse table names
        table_names = [t.strip() for t in response["content"].split(",")]
        table_names = [t for t in table_names if t in available_tables]
        
        print(f"   >> Needs tables: {', '.join(table_names)}")
        print(f"   >> Tokens used: {response['tokens_used']}")
        
        return {
            **state,
            "identified_tables": table_names,
            "tokens_used": state["tokens_used"] + response["tokens_used"],
            "tokens_breakdown": {
                **state.get("tokens_breakdown", {}),
                "analyze": response["tokens_used"]
            },
            "needs_schema_fetch": True,
            "workflow_step": "fetch_schema"
        }
    
    def fetch_schema(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: Get table schemas (from cache or database).
        Token cost: 0 if cached, ~100 per table if not
        """
        print("\n[2/5] Fetching table schemas...")
        
        schemas = {}
        cache_hits = 0
        cache_misses = 0
        
        for table_name in state["identified_tables"]:
            # Try cache first
            cached_schema = self.cache.get(table_name)
            
            if cached_schema:
                schemas[table_name] = cached_schema
                cache_hits += 1
            else:
                # Fetch from database
                schema = self.db.get_table_schema(table_name)
                schemas[table_name] = schema
                self.cache.set(table_name, schema)
                cache_misses += 1
        
        print(f"   >> Cache hits: {cache_hits}, misses: {cache_misses}")
        print(f"   >> Token savings: ~{cache_hits * 100} tokens")
        
        return {
            **state,
            "table_schemas": schemas,
            "needs_schema_fetch": False,
            "workflow_step": "generate_sql"
        }
    
    def generate_sql(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: Generate SQL query.
        Token cost: ~200-400 tokens
        """
        print("\n[3/5] Generating SQL query...")
        
        # Create prompt with schemas
        prompt = generate_sql_prompt(state["user_question"], state["table_schemas"])
        
        # Ask Groq to write SQL
        response = self.groq.chat([
            {"role": "user", "content": prompt}
        ], max_tokens=200)
        
        if not response["success"]:
            return {
                **state,
                "execution_error": f"Failed to generate SQL: {response['error']}",
                "tokens_used": state["tokens_used"] + response["tokens_used"]
            }
        
        sql_query = response["content"].strip()
        
        # Clean up SQL (remove markdown code blocks if present)
        if sql_query.startswith("```"):
            lines = sql_query.split("\n")
            sql_query = "\n".join(lines[1:-1]) if len(lines) > 2 else sql_query
        
        print(f"   >> SQL: {sql_query[:100]}...")
        print(f"   >> Tokens used: {response['tokens_used']}")
        
        return {
            **state,
            "generated_sql": sql_query,
            "tokens_used": state["tokens_used"] + response["tokens_used"],
            "tokens_breakdown": {
                **state.get("tokens_breakdown", {}),
                "generate_sql": response["tokens_used"]
            },
            "workflow_step": "execute_query"
        }
    
    def execute_query(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 4: Execute SQL query on database.
        Token cost: 0 (runs locally)
        """
        print("\n[4/5] Executing query...")
        
        # Execute SQL
        result = self.db.execute_query(state["generated_sql"])
        
        if not result["success"]:
            print(f"   >> SQL Error: {result['error']}")
            
            # Decide if we should retry
            attempts = state.get("sql_attempts", 0) + 1
            
            if attempts < 3:  # Max 2 retries
                print(f"   >> Retrying (attempt {attempts}/2)...")
                return {
                    **state,
                    "sql_attempts": attempts,
                    "execution_error": result["error"],
                    "should_retry": True,
                    "workflow_step": "fix_sql"
                }
            else:
                return {
                    **state,
                    "execution_error": result["error"],
                    "should_retry": False,
                    "workflow_step": "error"
                }
        
        print(f"   >> Retrieved {result['row_count']} rows")
        
        return {
            **state,
            "query_results": result,
            "execution_error": None,
            "should_retry": False,
            "workflow_step": "generate_answer"
        }
    
    def fix_sql(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step: Fix failed SQL query.
        Token cost: ~200-300 tokens
        """
        print("\n[Retry] Fixing SQL query...")
        
        # Create fix prompt
        prompt = fix_sql_prompt(
            state["generated_sql"],
            state["execution_error"],
            state["user_question"]
        )
        
        # Ask Groq to fix it
        response = self.groq.chat([
            {"role": "user", "content": prompt}
        ], max_tokens=200)
        
        if not response["success"]:
            return {
                **state,
                "should_retry": False,
                "workflow_step": "error"
            }
        
        fixed_sql = response["content"].strip()
        
        # Clean up
        if fixed_sql.startswith("```"):
            lines = fixed_sql.split("\n")
            fixed_sql = "\n".join(lines[1:-1]) if len(lines) > 2 else fixed_sql
        
        print(f"   >> Fixed SQL: {fixed_sql[:100]}...")
        print(f"   >> Tokens used: {response['tokens_used']}")
        
        return {
            **state,
            "generated_sql": fixed_sql,
            "tokens_used": state["tokens_used"] + response["tokens_used"],
            "tokens_breakdown": {
                **state.get("tokens_breakdown", {}),
                "fix_sql": response["tokens_used"]
            },
            "workflow_step": "execute_query"
        }
    
    def generate_answer(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 5: Generate human-friendly answer.
        Token cost: ~100-200 tokens
        """
        print("\n[5/5] Generating answer...")
        
        # Create answer prompt
        prompt = generate_answer_prompt(
            state["user_question"],
            state["query_results"]["data"]
        )
        
        # Ask Groq to explain
        response = self.groq.chat([
            {"role": "user", "content": prompt}
        ], max_tokens=150)
        
        if not response["success"]:
            # Fallback: just show the raw data
            return {
                **state,
                "final_answer": f"Query returned {state['query_results']['row_count']} rows: {state['query_results']['data']}",
                "tokens_used": state["tokens_used"] + response["tokens_used"],
                "workflow_step": "complete"
            }
        
        print(f"   >> Tokens used: {response['tokens_used']}")
        
        # Increment cache question count
        self.cache.increment_question_count()
        
        return {
            **state,
            "final_answer": response["content"],
            "tokens_used": state["tokens_used"] + response["tokens_used"],
            "tokens_breakdown": {
                **state.get("tokens_breakdown", {}),
                "generate_answer": response["tokens_used"]
            },
            "workflow_step": "complete"
        }
