"""
Vercel Handler for FastAPI Application
This file imports the FastAPI app and exposes it for Vercel's serverless functions.
"""

import sys
import os

# Add parent directory to path so we can import from src/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app from app.py
from app import app

# Vercel will use this app instance
# No need to run uvicorn here - Vercel handles that
