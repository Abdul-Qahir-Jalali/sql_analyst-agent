"""
Groq API Client
Handles communication with Groq LLM and tracks token usage.
"""

from groq import Groq
from typing import Dict, Any, List
import os


class GroqClient:
    """Client for Groq API with token tracking"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile", 
                 max_tokens: int = 500, temperature: float = 0.1):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key
            model: Model name to use
            max_tokens: Maximum tokens per response
            temperature: Temperature for generation (0.1 = focused/deterministic)
        """
        self.client = Groq(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Token tracking
        self.session_tokens = 0
        self.question_tokens = []
    
    def chat(self, messages: List[Dict[str, str]], 
             max_tokens: int = None) -> Dict[str, Any]:
        """
        Send chat request to Groq.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Override default max_tokens
            
        Returns:
            Dictionary with response and token usage
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens or self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract response
            content = response.choices[0].message.content
            
            # Track tokens
            tokens_used = response.usage.total_tokens
            self.session_tokens += tokens_used
            self.question_tokens.append(tokens_used)
            
            return {
                "success": True,
                "content": content,
                "tokens_used": tokens_used,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tokens_used": 0
            }
    
    def get_token_stats(self) -> Dict[str, Any]:
        """Get token usage statistics"""
        return {
            "session_total": self.session_tokens,
            "last_question": self.question_tokens[-1] if self.question_tokens else 0,
            "average_per_question": sum(self.question_tokens) // len(self.question_tokens) if self.question_tokens else 0,
            "questions_asked": len(self.question_tokens)
        }
    
    def reset_session(self):
        """Reset token tracking for new session"""
        self.session_tokens = 0
        self.question_tokens = []
