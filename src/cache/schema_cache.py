"""
Schema Cache
Caches table schemas to avoid repeatedly fetching them.
Saves ~100 tokens per table per question after first fetch.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class SchemaCache:
    """Caches database schema information to save tokens"""
    
    def __init__(self, ttl_minutes: int = 30, max_questions: int = 20):
        """
        Initialize schema cache.
        
        Args:
            ttl_minutes: Time-to-live for cache entries (minutes)
            max_questions: Clear cache after this many questions
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl_minutes
        self.max_questions = max_questions
        self.question_count = 0
        self.created_at = datetime.now()
    
    def get(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Get cached schema for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Cached schema or None if not found/expired
        """
        if table_name not in self.cache:
            return None
        
        entry = self.cache[table_name]
        
        # Check if expired
        if datetime.now() - entry["timestamp"] > timedelta(minutes=self.ttl):
            del self.cache[table_name]
            return None
        
        return entry["schema"]
    
    def set(self, table_name: str, schema: Dict[str, Any]):
        """
        Cache a table schema.
        
        Args:
            table_name: Name of the table
            schema: Schema dictionary
        """
        self.cache[table_name] = {
            "schema": schema,
            "timestamp": datetime.now()
        }
    
    def increment_question_count(self):
        """Increment question counter and clear if limit reached"""
        self.question_count += 1
        
        if self.question_count >= self.max_questions:
            self.clear()
            print(f">> Cache cleared after {self.max_questions} questions")
    
    def clear(self):
        """Clear all cached schemas"""
        self.cache = {}
        self.question_count = 0
        self.created_at = datetime.now()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "cached_tables": list(self.cache.keys()),
            "cache_size": len(self.cache),
            "questions_asked": self.question_count,
            "cache_age_minutes": (datetime.now() - self.created_at).seconds // 60
        }
