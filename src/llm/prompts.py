"""
Prompt Templates
Short, efficient prompts to minimize token usage.
Each prompt is designed to get the job done with minimum tokens.
"""

from typing import Dict, Any, List


def analyze_question_prompt(user_question: str, available_tables: list) -> str:
    """
    Prompt to identify which tables are needed.
    Very short to save tokens.
    """
    tables_str = ", ".join(available_tables)
    
    return f"""Available tables: {tables_str}

Question: {user_question}

Which tables do you need to answer this? Reply with ONLY the table names, comma-separated. Nothing else."""


def generate_sql_prompt(user_question: str, schemas: Dict[str, Any]) -> str:
    """
    Prompt to generate SQL query.
    Provides only necessary schema information.
    """
    schema_text = ""
    for table_name, schema in schemas.items():
        cols = [f"{c['name']} ({c['type']})" for c in schema['columns']]
        schema_text += f"\n{table_name}: {', '.join(cols)}"
    
    return f"""Tables and columns:{schema_text}

Question: {user_question}

Write a MySQL query to answer this. Return ONLY the SQL query, no explanation or formatting."""


def fix_sql_prompt(original_sql: str, error_message: str, user_question: str) -> str:
    """
    Prompt to fix a failed SQL query.
    Used when query has syntax errors.
    """
    return f"""This SQL query failed:
{original_sql}

Error: {error_message}

Question was: {user_question}

Fix the query. Return ONLY the corrected SQL, no explanation."""


def generate_answer_prompt(user_question: str, query_results: List[Dict]) -> str:
    """
    Prompt to generate human-friendly answer from query results.
    Keeps it short.
    """
    # Limit results shown to save tokens (max 10 rows)
    results_preview = query_results[:10]
    
    return f"""Question: {user_question}

Query results: {results_preview}

Explain the answer in 1-2 clear sentences."""


def direct_sql_patterns() -> Dict[str, str]:
    """
    Patterns for direct SQL generation (no LLM needed).
    Ultra-fast, 0 tokens.
    """
    return {
        r"how many (\w+)": "SELECT COUNT(*) FROM {table}",
        r"count (\w+)": "SELECT COUNT(*) FROM {table}",
        r"show me (\w+)": "SELECT * FROM {table} LIMIT 10",
        r"list (\w+)": "SELECT * FROM {table} LIMIT 10"
    }
