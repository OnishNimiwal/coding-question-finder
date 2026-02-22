import os
import sys

# Add the project root to the Python path so Vercel can find app.py
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

# Vercel's Python runtime searches for an 'app' or 'handler' object
app = app
