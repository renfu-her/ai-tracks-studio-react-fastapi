#!/bin/bash
# Check Python 3.14 compatibility
# 檢查 Python 3.14 相容性

echo "========================================="
echo "Python 3.14 Compatibility Check"
echo "========================================="
echo ""

BACKEND_DIR="/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend"
cd "$BACKEND_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Check Python version
echo "1. Python version check..."
if [ -f ".venv/bin/python" ]; then
    PYTHON_VERSION=$(.venv/bin/python --version)
    echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"
    
    # Check if it's really 3.14
    if [[ $PYTHON_VERSION == *"3.14"* ]]; then
        echo -e "${YELLOW}⚠ Using Python 3.14 (very new, check package compatibility)${NC}"
    fi
else
    echo -e "${RED}✗ Virtual environment not found${NC}"
fi
echo ""

# 2. Test basic import
echo "2. Testing basic Python import..."
cd "$BACKEND_DIR"
if .venv/bin/python -c "import sys; print('Python path:', sys.path)" 2>&1; then
    echo -e "${GREEN}✓ Python can execute${NC}"
else
    echo -e "${RED}✗ Python execution failed${NC}"
fi
echo ""

# 3. Test app module import with detailed error
echo "3. Testing app module import (detailed)..."
cd "$BACKEND_DIR"
.venv/bin/python << 'PYTHON_SCRIPT'
import sys
import os

print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"\nPython path (sys.path):")
for i, path in enumerate(sys.path):
    print(f"  [{i}] {path}")

print("\nAttempting to import app module...")
try:
    import app
    print("✓ Successfully imported 'app' module")
    print(f"  app location: {app.__file__}")
except ImportError as e:
    print(f"✗ Failed to import 'app': {e}")
    print("\nChecking if 'app' directory exists...")
    if os.path.exists('app'):
        print(f"  ✓ 'app' directory exists")
        print(f"  Contents: {os.listdir('app')[:10]}")
        if os.path.exists('app/__init__.py'):
            print("  ✓ 'app/__init__.py' exists")
        else:
            print("  ✗ 'app/__init__.py' NOT found (required for package)")
    else:
        print(f"  ✗ 'app' directory NOT found")

print("\nAttempting to import app.main...")
try:
    from app.main import app as fastapi_app
    print("✓ Successfully imported FastAPI app")
except ImportError as e:
    print(f"✗ Failed to import app.main: {e}")

print("\nAttempting to import app.config...")
try:
    from app.config import settings
    print("✓ Successfully imported settings")
    print(f"  Database: {settings.DB_NAME}")
except ImportError as e:
    print(f"✗ Failed to import app.config: {e}")
except Exception as e:
    print(f"✗ Error loading settings: {e}")
PYTHON_SCRIPT
echo ""

# 4. Check key dependencies compatibility
echo "4. Checking key dependencies..."
.venv/bin/python << 'PYTHON_SCRIPT'
import sys

packages_to_check = [
    'fastapi',
    'uvicorn',
    'gunicorn',
    'pydantic',
    'pydantic_settings',
    'sqlalchemy',
    'pymysql',
]

print("Checking if packages are installed and importable:\n")
for package in packages_to_check:
    try:
        if package == 'pydantic_settings':
            import pydantic_settings
            version = getattr(pydantic_settings, '__version__', 'unknown')
        else:
            mod = __import__(package)
            version = getattr(mod, '__version__', 'unknown')
        print(f"✓ {package:20s} - version {version}")
    except ImportError:
        print(f"✗ {package:20s} - NOT INSTALLED")
    except Exception as e:
        print(f"⚠ {package:20s} - Error: {e}")
PYTHON_SCRIPT
echo ""

# 5. Test if we can import from correct directory
echo "5. Testing import from correct directory..."
cd "$BACKEND_DIR"
.venv/bin/python << 'PYTHON_SCRIPT'
import sys
import os

# Add current directory to path (this is what should happen automatically)
current_dir = os.getcwd()
if current_dir not in sys.path:
    print(f"⚠ Current directory not in sys.path, adding it...")
    sys.path.insert(0, current_dir)
else:
    print(f"✓ Current directory already in sys.path")

print(f"\nCurrent directory: {current_dir}")
print(f"Attempting import with current directory in path...")

try:
    import app
    from app.main import app as fastapi_app
    from app.config import settings
    print("✓ All imports successful!")
    print(f"  Database URL: {settings.database_url}")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
PYTHON_SCRIPT
echo ""

# 6. Test gunicorn/uvicorn compatibility with Python 3.14
echo "6. Testing gunicorn/uvicorn compatibility..."
.venv/bin/python << 'PYTHON_SCRIPT'
import sys

print(f"Python: {sys.version}\n")

try:
    import gunicorn
    print(f"✓ gunicorn: {gunicorn.__version__}")
except ImportError:
    print("✗ gunicorn not installed")

try:
    import uvicorn
    print(f"✓ uvicorn: {uvicorn.__version__}")
except ImportError:
    print("✗ uvicorn not installed")

try:
    import uvicorn.workers
    print("✓ uvicorn.workers available")
except ImportError:
    print("✗ uvicorn.workers not available")
PYTHON_SCRIPT
echo ""

# 7. Test actual uvicorn startup (short test)
echo "7. Testing actual uvicorn startup (5 second test)..."
echo "Command: cd $BACKEND_DIR && .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 19999"
cd "$BACKEND_DIR"

# Start uvicorn in background with timeout
timeout 5 .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 19999 2>&1 &
UVICORN_PID=$!

# Wait a bit for startup
sleep 2

# Check if process is still running
if ps -p $UVICORN_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Uvicorn started successfully${NC}"
    
    # Try to access the API
    if curl -s http://127.0.0.1:19999/docs > /dev/null 2>&1; then
        echo -e "${GREEN}✓ API is responding${NC}"
    else
        echo -e "${YELLOW}⚠ API not responding (might need more time)${NC}"
    fi
    
    # Kill the test process
    kill $UVICORN_PID 2>/dev/null
    wait $UVICORN_PID 2>/dev/null
else
    echo -e "${RED}✗ Uvicorn failed to start${NC}"
fi
echo ""

# Summary
echo "========================================="
echo "Summary & Recommendations"
echo "========================================="
echo ""

echo "If you see '✓ All imports successful!' in test #5, then:"
echo "  → Python 3.14 is NOT the problem"
echo "  → The issue is with how systemd runs the service"
echo "  → Solution: Use the studio-uvicorn-direct.service file"
echo ""

echo "If imports are failing:"
echo "  1. Check if you're in the correct directory"
echo "  2. Ensure app/__init__.py exists"
echo "  3. Try: cd $BACKEND_DIR && .venv/bin/python -c 'from app.config import settings'"
echo ""

echo "Python 3.14 specific issues to watch for:"
echo "  - Some packages might not fully support Python 3.14 yet"
echo "  - Consider using Python 3.12 or 3.13 if you encounter package issues"
echo "  - Most FastAPI/Uvicorn/Gunicorn packages should work fine"
echo ""

