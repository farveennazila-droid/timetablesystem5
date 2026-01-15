"""
Timetable Management System - Main Entry Point for Render
This file wraps the Flask app from the backend for easier deployment
"""

import os
import sys

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import and run the Flask app
from app import app

if __name__ == "__main__":
    # Get port from environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Run with proper configuration for production
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
