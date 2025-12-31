"""
LangGraph Workflow
Connects all the nodes together into a complete agent.
"""

from langgraph.graph import StateGraph, END
from typing import Dict, Any
from .state import AgentState
from .nodes import WorkflowNodes


def create_agent_graph(workflow_nodes: WorkflowNodes) -> StateGraph:
    """
    Create the agent workflow graph.
    
    The workflow:
    1. Analyze Question → Which tables needed?
    2. Fetch Schema → Get table structures
    3. Generate SQL → Write the query
    4. Execute Query → Run on database
    5. Generate Answer → Explain results
    
    With error handling: If SQL fails, retry with fix_sql node.
    """
    
    # Create graph
    graph = StateGraph(AgentState)
    
    # Add nodes
    graph.add_node("analyze_question", workflow_nodes.analyze_question)
    graph.add_node("fetch_schema", workflow_nodes.fetch_schema)
    graph.add_node("generate_sql", workflow_nodes.generate_sql)
    graph.add_node("execute_query", workflow_nodes.execute_query)
    graph.add_node("fix_sql", workflow_nodes.fix_sql)
    graph.add_node("generate_answer", workflow_nodes.generate_answer)
    
    # Set entry point
    graph.set_entry_point("analyze_question")
    
    # Define edges (workflow flow)
    graph.add_edge("analyze_question", "fetch_schema")
    graph.add_edge("fetch_schema", "generate_sql")
    graph.add_edge("generate_sql", "execute_query")
    
    # Conditional edge after execute_query
    def should_retry_sql(state: Dict[str, Any]) -> str:
        """Decide if we should retry failed SQL"""
        if state.get("should_retry", False):
            return "fix_sql"
        elif state.get("execution_error"):
            return END  # Give up after max retries
        else:
            return "generate_answer"
    
    graph.add_conditional_edges(
        "execute_query",
        should_retry_sql,
        {
            "fix_sql": "fix_sql",
            "generate_answer": "generate_answer",
            END: END
        }
    )
    
    # After fixing SQL, try executing again
    graph.add_edge("fix_sql", "execute_query")
    
    # After generating answer, we're done
    graph.add_edge("generate_answer", END)
    
    return graph.compile()


class SQLAgent:
    """The complete SQL Analyst Agent"""
    
    def __init__(self, workflow_nodes: WorkflowNodes):
        """
        Initialize agent.
        
        Args:
            workflow_nodes: Workflow nodes instance
        """
        self.workflow_nodes = workflow_nodes
        self.graph = create_agent_graph(workflow_nodes)
    
    def ask(self, question: str) -> Dict[str, Any]:
        """
        Ask the agent a question.
        
        Args:
            question: User's question in natural language
            
        Returns:
            Dictionary with answer and metadata
        """
        # Initial state
        initial_state = {
            "user_question": question,
            "messages": [],
            "identified_tables": [],
            "table_schemas": {},
            "generated_sql": None,
            "sql_attempts": 0,
            "query_results": None,
            "execution_error": None,
            "final_answer": None,
            "tokens_used": 0,
            "tokens_breakdown": {},
            "workflow_step": "start",
            "should_retry": False,
            "needs_schema_fetch": False
        }
        
        # Run workflow
        print(f"\n{'='*80}")
        print(f"Question: {question}")
        print(f"{'='*80}")
        
        final_state = self.graph.invoke(initial_state)
        
        # Return results
        return {
            "question": question,
            "answer": final_state.get("final_answer", "Sorry, I couldn't answer that."),
            "sql": final_state.get("generated_sql"),
            "results": final_state.get("query_results"),
            "tokens_used": final_state.get("tokens_used", 0),
            "tokens_breakdown": final_state.get("tokens_breakdown", {}),
            "error": final_state.get("execution_error")
        }
