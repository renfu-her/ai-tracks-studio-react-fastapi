"""
Quick start script for running the FastAPI server.

Usage:
    uv run python run.py
    
Or with custom settings:
    uv run python run.py --port 8080 --host 127.0.0.1
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

