"""
Agent State
Defines what the agent remembers during a conversation.
"""

from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State that persists throughout the agent's workflow"""
    
    # User input
    user_question: str
    
    # Conversation history
    messages: List[Dict[str, str]]
    
    # Analysis phase
    identified_tables: List[str]
    table_schemas: Dict[str, Any]
    
    # SQL generation phase
    generated_sql: Optional[str]
    sql_attempts: int  # Track retries
    
    # Execution phase
    query_results: Optional[Dict[str, Any]]
    execution_error: Optional[str]
    
    # Response phase
    final_answer: Optional[str]
    
    # Token tracking
    tokens_used: int
    tokens_breakdown: Dict[str, int]  # Track where tokens were spent
    
    # Metadata
    workflow_step: str  # Current step name
    should_retry: bool  # Whether to retry failed SQL
    needs_schema_fetch: bool  # Whether schemas need to be fetched
