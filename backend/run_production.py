"""
Production server startup script using Gunicorn with Uvicorn workers.

Usage:
    uv run python run_production.py
    
This script is for production deployment. For development, use run.py instead.
"""

import multiprocessing
import os

# Gunicorn configuration
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 60
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "ai-tracks-studio-api"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

print(f"Starting production server with {workers} workers...")
print(f"Binding to {bind}")
print(f"Worker class: {worker_class}")

