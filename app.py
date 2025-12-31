"""
FastAPI Web Server for SQL Agent
Provides REST API and serves the web interface.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
import os

# Import agent components
from src.llm.groq_client import GroqClient
from src.mcp.tools import DatabaseTools
from src.cache.schema_cache import SchemaCache
from src.agent.nodes import WorkflowNodes
from src.agent.graph import SQLAgent
import yaml
from dotenv import load_dotenv


# Load configuration
def load_config():
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    load_dotenv()
    
    # Groq API
    config['groq']['api_key'] = os.getenv("GROQ_API_KEY")
    
    # Database - use environment variables if available (for production with MySQL)
    # Only update MySQL fields if database type is MySQL
    if config['database'].get('type') == 'mysql':
        config['database']['host'] = os.getenv("DB_HOST", config['database'].get('host', 'localhost'))
        config['database']['user'] = os.getenv("DB_USER", config['database'].get('user', 'root'))
        config['database']['password'] = os.getenv("DB_PASSWORD", config['database'].get('password', ''))
        config['database']['database'] = os.getenv("DB_NAME", config['database'].get('database', 'retail_analytics'))
        config['database']['port'] = int(os.getenv("DB_PORT", config['database'].get('port', 3306)))
    
    return config


# Initialize agent
config = load_config()
groq_client = GroqClient(
    api_key=config['groq']['api_key'],
    model=config['groq']['model'],
    max_tokens=config['groq']['max_tokens'],
    temperature=config['groq']['temperature']
)
db_tools = DatabaseTools(config['database'])
schema_cache = SchemaCache(
    ttl_minutes=config['cache']['ttl_minutes'],
    max_questions=config['cache']['max_questions']
)
workflow_nodes = WorkflowNodes(groq_client, db_tools, schema_cache)
agent = SQLAgent(workflow_nodes)

# Create FastAPI app
app = FastAPI(title="SQL Analyst Agent", version="1.0.0")


# Request/Response models
class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    sql: Optional[str]
    tokens_used: int
    tokens_breakdown: dict
    error: Optional[str]


class StatsResponse(BaseModel):
    session_total: int
    questions_asked: int
    average_per_question: int
    cached_tables: list
    cache_age_minutes: int


# API Routes
@app.post("/api/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question to the SQL Agent.
    """
    try:
        result = agent.ask(request.question)
        return QuestionResponse(
            answer=result["answer"],
            sql=result.get("sql"),
            tokens_used=result["tokens_used"],
            tokens_breakdown=result.get("tokens_breakdown", {}),
            error=result.get("error")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get token usage statistics.
    """
    groq_stats = groq_client.get_token_stats()
    cache_stats = schema_cache.get_stats()
    
    return StatsResponse(
        session_total=groq_stats['session_total'],
        questions_asked=groq_stats['questions_asked'],
        average_per_question=groq_stats['average_per_question'],
        cached_tables=cache_stats['cached_tables'],
        cache_age_minutes=cache_stats['cache_age_minutes']
    )


@app.get("/api/reset")
async def reset_session():
    """
    Reset the session (clear cache and token counters).
    """
    groq_client.reset_session()
    schema_cache.clear()
    return {"message": "Session reset successfully"}


# Database Viewer API Routes
@app.get("/api/database/tables")
async def get_tables():
    """
    Get list of all tables in the database with row counts.
    """
    try:
        tables_info = db_tools.get_all_tables()
        return {"tables": tables_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/database/table/{table_name}")
async def get_table_schema(table_name: str):
    """
    Get schema information for a specific table.
    """
    try:
        schema = db_tools.get_table_schema(table_name)
        return {"table_name": table_name, "schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/database/data/{table_name}")
async def get_table_data(
    table_name: str,
    page: int = 1,
    page_size: int = 50,
    search: Optional[str] = None
):
    """
    Get paginated data from a specific table.
    """
    try:
        data = db_tools.get_table_data(table_name, page, page_size, search)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve static files and index
@app.get("/", response_class=HTMLResponse)
async def serve_home():
    """
    Serve the main web interface.
    """
    try:
        with open("web/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Web interface not found. Make sure web/index.html exists.</h1>"


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*80)
    print(" " * 25 + "SQL ANALYST WEB SERVER")
    print("="*80)
    print("\n>> Starting server at: http://localhost:8000")
    print(">> Open your browser and visit: http://localhost:8000\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
