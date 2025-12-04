#!/bin/bash
# Production startup script for AI-Tracks Studio Backend

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the backend directory
cd "$SCRIPT_DIR"

echo "Starting AI-Tracks Studio Backend..."
echo "Working directory: $(pwd)"
echo "Python version: $(uv run python --version)"

# Start the server using uvicorn (recommended for production)
echo "Starting Uvicorn server..."
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Alternative: Use Gunicorn with Uvicorn workers (uncomment to use)
# echo "Starting Gunicorn server with Uvicorn workers..."
# uv run gunicorn app.main:app \
#   --workers 4 \
#   --worker-class uvicorn.workers.UvicornWorker \
#   --bind 0.0.0.0:8000 \
#   --timeout 60 \
#   --access-logfile - \
#   --error-logfile -

