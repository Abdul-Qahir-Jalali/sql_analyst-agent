"""
SQL Analyst Agent - Main Entry Point
Intelligent database query agent that minimizes token usage.
"""

import os
import yaml
from dotenv import load_dotenv

from src.llm.groq_client import GroqClient
from src.mcp.tools import DatabaseTools
from src.cache.schema_cache import SchemaCache
from src.agent.nodes import WorkflowNodes
from src.agent.graph import SQLAgent
from src.ui.cli import create_cli


def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Load API key from environment
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError(
            "Please set your GROQ_API_KEY in the .env file.\n"
            "Get your free API key at: https://console.groq.com/keys"
        )
    
    config['groq']['api_key'] = api_key
    
    return config


def main():
    """Main function to run the SQL Agent"""
    
    print("Initializing SQL Analyst Agent...")
    
    # Load configuration
    try:
        config = load_config()
    except FileNotFoundError:
        print("Error: config.yaml not found!")
        return
    except ValueError as e:
        print(f"Configuration error: {e}")
        return
    
    # Initialize components
    print(">> Loading Groq client...")
    groq_client = GroqClient(
        api_key=config['groq']['api_key'],
        model=config['groq']['model'],
        max_tokens=config['groq']['max_tokens'],
        temperature=config['groq']['temperature']
    )
    
    print(">> Connecting to MySQL database...")
    db_tools = DatabaseTools(config['database'])
    
    print(">> Initializing schema cache...")
    schema_cache = SchemaCache(
        ttl_minutes=config['cache']['ttl_minutes'],
        max_questions=config['cache']['max_questions']
    )
    
    print(">> Building agent workflow...")
    workflow_nodes = WorkflowNodes(groq_client, db_tools, schema_cache)
    agent = SQLAgent(workflow_nodes)
    
    print(">> Starting CLI...\n")
    
    # Create and run CLI
    cli = create_cli(agent)
    
    try:
        cli.run()
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Cleanup
        db_tools.close()
        print("\nThank you for using SQL Analyst Agent!")


if __name__ == "__main__":
    main()
