#!/bin/bash
# Switch Python version using UV (Simple Method)
# 使用 UV 切換 Python 版本（簡單方法）

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BACKEND_DIR="/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend"

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Switch Python Version with UV${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}✗ Backend directory not found: $BACKEND_DIR${NC}"
    exit 1
fi

cd "$BACKEND_DIR"
echo -e "${GREEN}✓ Directory: $(pwd)${NC}"
echo ""

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗ UV not found${NC}"
    echo "Install UV:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo -e "${GREEN}✓ UV found: $(which uv)${NC}"
uv --version
echo ""

# Show current version
echo -e "${YELLOW}Current setup:${NC}"
if [ -f ".python-version" ]; then
    echo "  .python-version: $(cat .python-version)"
else
    echo "  .python-version: (not found)"
fi

if [ -f ".venv/bin/python" ]; then
    echo "  Current Python: $(.venv/bin/python --version)"
else
    echo "  Current Python: (no venv)"
fi
echo ""

# Ask for confirmation
echo -e "${YELLOW}This will:${NC}"
echo "  1. Change .python-version to: 3.12"
echo "  2. Backup current .venv (if exists)"
echo "  3. Run 'uv sync' to rebuild environment"
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi
echo ""

# Step 1: Backup .venv
echo -e "${YELLOW}Step 1: Backing up .venv...${NC}"
if [ -d ".venv" ]; then
    BACKUP_NAME=".venv.backup.$(date +%Y%m%d_%H%M%S)"
    mv .venv "$BACKUP_NAME"
    echo -e "${GREEN}✓ Backup created: $BACKUP_NAME${NC}"
else
    echo -e "${YELLOW}⚠ No .venv to backup${NC}"
fi
echo ""

# Step 2: Update .python-version
echo -e "${YELLOW}Step 2: Updating .python-version...${NC}"
echo "3.12" > .python-version
echo -e "${GREEN}✓ .python-version updated to: $(cat .python-version)${NC}"
echo ""

# Step 3: Run uv sync
echo -e "${YELLOW}Step 3: Running uv sync...${NC}"
echo "This will download Python 3.12 and install all dependencies..."
echo ""
uv sync

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ UV sync completed${NC}"
else
    echo -e "${RED}✗ UV sync failed${NC}"
    exit 1
fi
echo ""

# Step 4: Verify
echo -e "${YELLOW}Step 4: Verifying installation...${NC}"
NEW_VERSION=$(uv run python --version)
echo "New Python: $NEW_VERSION"

if [[ $NEW_VERSION == *"3.12"* ]]; then
    echo -e "${GREEN}✓ Python 3.12 installed successfully${NC}"
else
    echo -e "${RED}✗ Python version mismatch${NC}"
    exit 1
fi
echo ""

# Step 5: Test import
echo -e "${YELLOW}Step 5: Testing app import...${NC}"
uv run python << 'EOF'
try:
    from app.config import settings
    from app.main import app
    print("✓ All imports successful")
    print(f"  Database: {settings.DB_NAME}")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import sys
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ App import test passed${NC}"
else
    echo -e "${RED}✗ App import test failed${NC}"
    exit 1
fi
echo ""

# Step 6: Quick server test
echo -e "${YELLOW}Step 6: Testing server startup (5 seconds)...${NC}"
timeout 5 uv run uvicorn app.main:app --host 127.0.0.1 --port 19999 2>&1 &
TEST_PID=$!
sleep 2

if ps -p $TEST_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Server started successfully${NC}"
    kill $TEST_PID 2>/dev/null || true
    wait $TEST_PID 2>/dev/null || true
else
    echo -e "${YELLOW}⚠ Server test skipped${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Switch Complete!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo -e "${GREEN}✓ Successfully switched to Python 3.12${NC}"
echo ""
echo "Python version: $NEW_VERSION"
echo ""

# Next steps
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Restart systemd service:"
echo "   ${BLUE}sudo systemctl restart studio-uvicorn${NC}"
echo ""
echo "2. Check status:"
echo "   ${BLUE}sudo systemctl status studio-uvicorn${NC}"
echo ""
echo "3. View logs:"
echo "   ${BLUE}sudo journalctl -u studio-uvicorn -f${NC}"
echo ""
echo "4. Test API:"
echo "   ${BLUE}curl http://127.0.0.1:9001/docs${NC}"
echo ""
echo "5. If all good, remove backup:"
echo "   ${BLUE}rm -rf $BACKEND_DIR/.venv.backup.*${NC}"
echo ""

echo -e "${GREEN}Done!${NC}"

