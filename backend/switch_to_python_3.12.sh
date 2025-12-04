#!/bin/bash
# Switch from Python 3.14 to Python 3.12
# 從 Python 3.14 切換到 Python 3.12

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKEND_DIR="/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend"

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Switch to Python 3.12${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}✗ Backend directory not found: $BACKEND_DIR${NC}"
    exit 1
fi

cd "$BACKEND_DIR"
echo -e "${GREEN}✓ Changed to: $(pwd)${NC}"
echo ""

# 1. Check current Python version
echo -e "${YELLOW}Step 1: Checking current Python version...${NC}"
if [ -f ".venv/bin/python" ]; then
    CURRENT_VERSION=$(.venv/bin/python --version)
    echo "Current virtual environment: $CURRENT_VERSION"
else
    echo -e "${YELLOW}⚠ No virtual environment found${NC}"
fi
echo ""

# 2. Check if Python 3.12 is available
echo -e "${YELLOW}Step 2: Checking if Python 3.12 is available...${NC}"
if command -v python3.12 &> /dev/null; then
    PYTHON312=$(which python3.12)
    echo -e "${GREEN}✓ Python 3.12 found: $PYTHON312${NC}"
    python3.12 --version
elif command -v python3 &> /dev/null; then
    PYTHON3_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
    if [[ "$PYTHON3_VERSION" == "3.12" ]]; then
        PYTHON312=$(which python3)
        echo -e "${GREEN}✓ Python 3.12 found as python3: $PYTHON312${NC}"
    else
        echo -e "${RED}✗ Python 3.12 not found${NC}"
        echo "Available Python versions:"
        ls -la /usr/bin/python* 2>/dev/null || true
        echo ""
        echo "Install Python 3.12:"
        echo "  sudo apt update"
        echo "  sudo apt install python3.12 python3.12-venv python3.12-dev"
        exit 1
    fi
else
    echo -e "${RED}✗ Python not found${NC}"
    exit 1
fi
echo ""

# 3. Backup current .venv
echo -e "${YELLOW}Step 3: Backing up current virtual environment...${NC}"
if [ -d ".venv" ]; then
    BACKUP_NAME=".venv.backup.$(date +%Y%m%d_%H%M%S)"
    echo "Creating backup: $BACKUP_NAME"
    mv .venv "$BACKUP_NAME"
    echo -e "${GREEN}✓ Backup created: $BACKUP_NAME${NC}"
else
    echo -e "${YELLOW}⚠ No .venv to backup${NC}"
fi
echo ""

# 4. Check if uv is available
echo -e "${YELLOW}Step 4: Checking package manager...${NC}"
USE_UV=false
if command -v uv &> /dev/null; then
    echo -e "${GREEN}✓ uv found: $(which uv)${NC}"
    uv --version
    USE_UV=true
else
    echo -e "${YELLOW}⚠ uv not found, will use venv + pip${NC}"
fi
echo ""

# 5. Create new virtual environment with Python 3.12
echo -e "${YELLOW}Step 5: Creating new virtual environment with Python 3.12...${NC}"
if [ "$USE_UV" = true ]; then
    echo "Using uv to create venv..."
    uv venv --python 3.12
else
    echo "Using python3.12 venv..."
    $PYTHON312 -m venv .venv
fi
echo -e "${GREEN}✓ Virtual environment created${NC}"
echo ""

# Verify new Python version
NEW_VERSION=$(.venv/bin/python --version)
echo "New virtual environment: $NEW_VERSION"
echo ""

# 6. Install dependencies
echo -e "${YELLOW}Step 6: Installing dependencies...${NC}"
if [ "$USE_UV" = true ]; then
    echo "Using uv sync..."
    uv sync
elif [ -f "requirements.txt" ]; then
    echo "Using pip install from requirements.txt..."
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    echo "Using pip install from pyproject.toml..."
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -e .
else
    echo -e "${RED}✗ No requirements.txt or pyproject.toml found${NC}"
    echo "Manual installation needed"
    exit 1
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# 7. Verify installation
echo -e "${YELLOW}Step 7: Verifying installation...${NC}"
echo "Testing imports..."
.venv/bin/python << 'PYTHON_TEST'
import sys
print(f"Python version: {sys.version}")
print()

# Test imports
packages = [
    ('fastapi', 'FastAPI'),
    ('uvicorn', 'Uvicorn'),
    ('gunicorn', 'Gunicorn'),
    ('pydantic', 'Pydantic'),
    ('sqlalchemy', 'SQLAlchemy'),
    ('pymysql', 'PyMySQL'),
]

print("Testing package imports:")
all_ok = True
for module, name in packages:
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'unknown')
        print(f"  ✓ {name:15s} - {version}")
    except ImportError as e:
        print(f"  ✗ {name:15s} - NOT FOUND")
        all_ok = False

print()
if all_ok:
    print("✓ All packages installed successfully")
else:
    print("✗ Some packages are missing")
    sys.exit(1)
PYTHON_TEST

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Package import test passed${NC}"
else
    echo -e "${RED}✗ Package import test failed${NC}"
    exit 1
fi
echo ""

# 8. Test app module import
echo -e "${YELLOW}Step 8: Testing app module import...${NC}"
.venv/bin/python << 'APP_TEST'
import sys
import os

try:
    from app.config import settings
    print("✓ app.config imported successfully")
    print(f"  Database: {settings.DB_NAME}")
    
    from app.main import app
    print("✓ app.main imported successfully")
    print(f"  API Prefix: {settings.API_PREFIX}")
    
    print("\n✓ All app imports successful!")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
APP_TEST

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ App module test passed${NC}"
else
    echo -e "${RED}✗ App module test failed${NC}"
    exit 1
fi
echo ""

# 9. Quick server test
echo -e "${YELLOW}Step 9: Testing server startup (5 seconds)...${NC}"
echo "Starting uvicorn on port 19999..."
timeout 5 .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 19999 2>&1 &
TEST_PID=$!
sleep 2

if ps -p $TEST_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server started successfully${NC}"
    
    if curl -s http://127.0.0.1:19999/docs > /dev/null 2>&1; then
        echo -e "${GREEN}✓ API responding correctly${NC}"
    fi
    
    kill $TEST_PID 2>/dev/null || true
    wait $TEST_PID 2>/dev/null || true
else
    echo -e "${YELLOW}⚠ Server test skipped or failed${NC}"
fi
echo ""

# 10. Summary
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Migration Complete!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo -e "${GREEN}✓ Successfully switched to Python 3.12${NC}"
echo ""
echo "Old environment backed up to: $BACKUP_NAME"
echo "New Python version: $NEW_VERSION"
echo ""

# 11. Next steps
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Restart systemd service:"
echo "   ${BLUE}sudo systemctl restart studio-uvicorn${NC}"
echo ""
echo "2. Check service status:"
echo "   ${BLUE}sudo systemctl status studio-uvicorn${NC}"
echo ""
echo "3. View logs:"
echo "   ${BLUE}sudo journalctl -u studio-uvicorn -f${NC}"
echo ""
echo "4. Test API:"
echo "   ${BLUE}curl http://127.0.0.1:9001/docs${NC}"
echo ""
echo "5. If everything works, remove backup:"
echo "   ${BLUE}rm -rf $BACKEND_DIR/$BACKUP_NAME${NC}"
echo ""

echo -e "${GREEN}Migration completed successfully!${NC}"

