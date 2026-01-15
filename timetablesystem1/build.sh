#!/bin/bash
set -e

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations/setup if needed
echo "Setting up database..."

# Start the application
exec gunicorn app:app --bind 0.0.0.0:$PORT
