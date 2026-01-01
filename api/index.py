"""
Vercel Handler for FastAPI Application
This file imports the FastAPI app and exposes it for Vercel's serverless functions.
"""

import sys
import os

# Get the root directory (parent of api/)
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add root directory to Python path for imports
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Import the FastAPI app - app.py now uses absolute paths for all files
from app import app

# Export the app for Vercel


