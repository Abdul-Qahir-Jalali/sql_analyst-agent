"""
MCP Database Tools - Updated for SQLite support
Provides functions to interact with both MySQL and SQLite databases.
"""

import mysql.connector
from mysql.connector import Error
import sqlite3
from typing import List, Dict, Any, Optional
import json
import os


class DatabaseTools:
    """Tools for database operations - supports both MySQL and SQLite"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize database connection"""
        self.config = config
        self.connection = None
        self.db_type = config.get('type', 'mysql')
        self._connect()
    
    def _connect(self):
        """Establish database connection (MySQL or SQLite)"""
        try:
            if self.db_type == 'sqlite':
                # SQLite connection
                db_file = self.config.get('database', 'retail_analytics.db')
                self.connection = sqlite3.connect(db_file, check_same_thread=False)
                self.connection.row_factory = sqlite3.Row  # Enable column access by name
                print(f">> Connected to SQLite database: {db_file}")
            else:
                # MySQL connection
                self.connection = mysql.connector.connect(
                    host=self.config['host'],
                    user=self.config['user'],
                    password=self.config['password'],
                    database=self.config['database'],
                    port=self.config.get('port', 3306)
                )
                print(f">> Connected to MySQL database: {self.config['database']}")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def _ensure_connection(self):
        """Make sure connection is alive"""
        if self.db_type == 'sqlite':
            if self.connection is None:
                self._connect()
        else:
            if self.connection is None or not self.connection.is_connected():
                self._connect()
    
    def list_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        self._ensure_connection()
        cursor = self.connection.cursor()
        
        try:
            if self.db_type == 'sqlite':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            else:
                cursor.execute("SHOW TABLES")
            
            tables = [table[0] for table in cursor.fetchall()]
            cursor.close()
            return tables
        except Exception as e:
            cursor.close()
            raise Exception(f"Error listing tables: {e}")
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get schema information for a specific table."""
        self._ensure_connection()
        cursor = self.connection.cursor()
        
        try:
            schema = {
                "table_name": table_name,
                "columns": []
            }
            
            if self.db_type == 'sqlite':
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                for col in columns:
                    schema["columns"].append({
                        "name": col[1],
                        "type": col[2],
                        "nullable": not col[3],
                        "key": "PRI" if col[5] else "",
                        "default": col[4],
                        "extra": ""
                    })
            else:
                # MySQL
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                
                for col in columns:
                    schema["columns"].append({
                        "name": col[0],
                        "type": col[1].decode() if isinstance(col[1], bytes) else col[1],
                        "nullable": col[2] == "YES",
                        "key": col[3],
                        "default": col[4],
                        "extra": col[5]
                    })
            
            cursor.close()
            return schema
            
        except Exception as e:
            cursor.close()
            raise Exception(f"Error getting schema for {table_name}: {e}")
    
    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute a SQL query and return results."""
        self._ensure_connection()
        cursor = self.connection.cursor()
        
        try:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            
            # Get column names
            column_names = [desc[0] for desc in cursor.description] if cursor.description else []
            
            # Format as list of dictionaries
            formatted_results = []
            for row in results:
                if self.db_type == 'sqlite':
                    # SQLite Row object
                    formatted_results.append(dict(row))
                else:
                    # MySQL tuple
                    formatted_results.append(dict(zip(column_names, row)))
            
            cursor.close()
            
            return {
                "success": True,
                "row_count": len(formatted_results),
                "columns": column_names,
                "data": formatted_results
            }
            
        except Exception as e:
            cursor.close()
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def get_sample_data(self, table_name: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get sample rows from a table."""
        result = self.execute_query(f"SELECT * FROM {table_name} LIMIT {limit}")
        
        if result["success"]:
            return result["data"]
        else:
            raise Exception(f"Error getting sample data: {result['error']}")
    
    def get_table_count(self, table_name: str) -> int:
        """Get total row count for a table."""
        result = self.execute_query(f"SELECT COUNT(*) as count FROM {table_name}")
        
        if result["success"] and len(result["data"]) > 0:
            return result["data"][0]["count"]
        else:
            return 0
    
    def get_all_tables(self) -> List[Dict[str, Any]]:
        """Get all tables with their row counts."""
        tables = self.list_tables()
        tables_info = []
        
        for table in tables:
            count = self.get_table_count(table)
            tables_info.append({
                "name": table,
                "row_count": count
            })
        
        return tables_info
    
    def get_table_data(
        self, 
        table_name: str, 
        page: int = 1, 
        page_size: int = 50,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated data from a table with optional search."""
        offset = (page - 1) * page_size
        
        # Build query with optional search
        if search:
            schema = self.get_table_schema(table_name)
            text_columns = [col["name"] for col in schema["columns"] 
                          if "char" in col["type"].lower() or "text" in col["type"].lower()]
            
            if text_columns:
                search_conditions = " OR ".join([
                    f"{col} LIKE '%{search}%'" for col in text_columns
                ])
                query = f"SELECT * FROM {table_name} WHERE {search_conditions} LIMIT {page_size} OFFSET {offset}"
                count_query = f"SELECT COUNT(*) as count FROM {table_name} WHERE {search_conditions}"
            else:
                query = f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}"
                count_query = f"SELECT COUNT(*) as count FROM {table_name}"
        else:
            query = f"SELECT * FROM {table_name} LIMIT {page_size} OFFSET {offset}"
            count_query = f"SELECT COUNT(*) as count FROM {table_name}"
        
        # Execute queries
        data_result = self.execute_query(query)
        count_result = self.execute_query(count_query)
        
        if not data_result["success"]:
            raise Exception(f"Error fetching data: {data_result['error']}")
        
        total_rows = count_result["data"][0]["count"] if count_result["success"] else 0
        total_pages = (total_rows + page_size - 1) // page_size
        
        return {
            "table_name": table_name,
            "columns": data_result["columns"],
            "data": data_result["data"],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_rows": total_rows,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        }
    
    def close(self):
        """Close database connection"""
        if self.connection:
            if self.db_type == 'sqlite':
                self.connection.close()
                print(">> SQLite connection closed")
            elif self.connection.is_connected():
                self.connection.close()
                print(">> MySQL connection closed")


# Tool wrapper functions for LangChain
def create_database_tools(config: Dict[str, Any]) -> Dict[str, callable]:
    """Create tool functions that can be used by the agent."""
    db_tools = DatabaseTools(config)
    
    return {
        "list_tables": db_tools.list_tables,
        "get_table_schema": db_tools.get_table_schema,
        "execute_query": db_tools.execute_query,
        "get_sample_data": db_tools.get_sample_data,
        "get_table_count": db_tools.get_table_count
    }
