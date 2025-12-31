"""
Command Line Interface
Simple chat interface for the SQL Agent.
"""

import sys
from typing import Dict, Any


class CLI:
    """Command line interface for SQL Agent"""
    
    def __init__(self, agent):
        """
        Initialize CLI.
        
        Args:
            agent: SQLAgent instance
        """
        self.agent = agent
        self.session_tokens = 0
    
    def print_header(self):
        """Print welcome message"""
        print("\n" + "="*80)
        print(" " * 25 + "SQL ANALYST AGENT")
        print("="*80)
        print("\nAsk me anything about your retail_analytics database!")
        print("Type 'exit' or 'quit' to end the session.")
        print("Type 'stats' to see token usage statistics.\n")
    
    def print_response(self, result: Dict[str, Any]):
        """
        Print agent's response.
        
        Args:
            result: Response dictionary from agent
        """
        print("\n" + "-"*80)
        
        if result.get("error"):
            print(f"Error: {result['error']}")
        else:
            print(f"Answer: {result['answer']}")
        
        if result.get("sql"):
            print(f"\nSQL Query:")
            print(f"  {result['sql']}")
        
        # Token usage
        tokens = result.get("tokens_used", 0)
        self.session_tokens += tokens
        print(f"\nTokens used: {tokens} (Session total: {self.session_tokens})")
        
        # Token breakdown
        breakdown = result.get("tokens_breakdown", {})
        if breakdown:
            print(f"Breakdown: {breakdown}")
        
        print("-"*80)
    
    def print_stats(self):
        """Print session statistics"""
        groq_stats = self.agent.workflow_nodes.groq.get_token_stats()
        cache_stats = self.agent.workflow_nodes.cache.get_stats()
        
        print("\n" + "="*80)
        print("SESSION STATISTICS")
        print("="*80)
        print(f"\nToken Usage:")
        print(f"  Total Tokens: {groq_stats['session_total']}")
        print(f"  Questions Asked: {groq_stats['questions_asked']}")
        print(f"  Average per Question: {groq_stats['average_per_question']}")
        
        print(f"\nSchema Cache:")
        print(f"  Cached Tables: {', '.join(cache_stats['cached_tables']) if cache_stats['cached_tables'] else 'None'}")
        print(f"  Cache Age: {cache_stats['cache_age_minutes']} minutes")
        print(f"  Questions Counted: {cache_stats['questions_asked']}")
        
        print("="*80 + "\n")
    
    def run(self):
        """Run the CLI"""
        self.print_header()
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("\nGoodbye! Total tokens used:", self.session_tokens)
                    break
                
                if user_input.lower() == "stats":
                    self.print_stats()
                    continue
                
                # Ask agent
                result = self.agent.ask(user_input)
                
                # Print response
                self.print_response(result)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
                continue


def create_cli(agent) -> CLI:
    """
    Create CLI instance.
    
    Args:
        agent: SQLAgent instance
        
    Returns:
        CLI instance
    """
    return CLI(agent)
