#!/bin/bash
# Diagnostic script to troubleshoot systemd service issues
# 診斷腳本，用於排查 systemd 服務問題

echo "========================================="
echo "AI-Tracks Studio Backend Diagnostics"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check working directory
echo "1. Checking working directory..."
BACKEND_DIR="/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend"
if [ -d "$BACKEND_DIR" ]; then
    echo -e "${GREEN}✓ Backend directory exists${NC}"
    ls -la "$BACKEND_DIR" | grep -E "^d" | head -5
else
    echo -e "${RED}✗ Backend directory NOT found: $BACKEND_DIR${NC}"
fi
echo ""

# 2. Check app directory
echo "2. Checking app module..."
if [ -d "$BACKEND_DIR/app" ]; then
    echo -e "${GREEN}✓ app directory exists${NC}"
    ls -la "$BACKEND_DIR/app" | head -5
else
    echo -e "${RED}✗ app directory NOT found${NC}"
fi
echo ""

# 3. Check uv installation
echo "3. Checking uv installation..."
if command -v uv &> /dev/null; then
    echo -e "${GREEN}✓ uv is installed${NC}"
    echo "Location: $(which uv)"
    uv --version
else
    echo -e "${RED}✗ uv is NOT installed${NC}"
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi
echo ""

# 4. Check Python environment
echo "4. Checking Python environment..."
cd "$BACKEND_DIR"
if [ -d ".venv" ]; then
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
    echo "Python version in venv:"
    .venv/bin/python --version
else
    echo -e "${RED}✗ Virtual environment NOT found${NC}"
fi
echo ""

# 5. Test import
echo "5. Testing Python import..."
cd "$BACKEND_DIR"
if command -v uv &> /dev/null; then
    echo "Testing: uv run python -c 'from app.config import settings; print(\"Import OK\")'"
    if uv run python -c "from app.config import settings; print('✓ Import successful')" 2>/dev/null; then
        echo -e "${GREEN}✓ Can import app module${NC}"
    else
        echo -e "${RED}✗ Cannot import app module${NC}"
        echo "Error output:"
        uv run python -c "from app.config import settings" 2>&1 || true
    fi
else
    echo -e "${YELLOW}⚠ Skipping (uv not installed)${NC}"
fi
echo ""

# 6. Check .env file
echo "6. Checking .env file..."
if [ -f "$BACKEND_DIR/.env" ]; then
    echo -e "${GREEN}✓ .env file exists${NC}"
    echo "Key variables:"
    grep -E "^(DB_|SECRET_KEY|ENVIRONMENT|DEBUG|CORS_)" "$BACKEND_DIR/.env" | sed 's/=.*/=***/' || true
else
    echo -e "${RED}✗ .env file NOT found${NC}"
fi
echo ""

# 7. Check permissions
echo "7. Checking file permissions..."
echo "Backend directory owner:"
ls -ld "$BACKEND_DIR"
echo "app directory owner:"
ls -ld "$BACKEND_DIR/app"
echo ""

# 8. Check if service exists
echo "8. Checking systemd service..."
if [ -f "/etc/systemd/system/studio-uvicorn.service" ]; then
    echo -e "${GREEN}✓ Service file exists${NC}"
    echo "Service file location: /etc/systemd/system/studio-uvicorn.service"
    echo ""
    echo "ExecStart line:"
    grep "ExecStart=" /etc/systemd/system/studio-uvicorn.service || true
    echo ""
    echo "WorkingDirectory line:"
    grep "WorkingDirectory=" /etc/systemd/system/studio-uvicorn.service || true
else
    echo -e "${YELLOW}⚠ Service file not found at /etc/systemd/system/studio-uvicorn.service${NC}"
fi
echo ""

# 9. Check service status
echo "9. Checking service status..."
if systemctl list-unit-files | grep -q studio-uvicorn; then
    echo "Service status:"
    systemctl status studio-uvicorn --no-pager -l || true
else
    echo -e "${YELLOW}⚠ Service not installed${NC}"
fi
echo ""

# 10. Test manual startup
echo "10. Testing manual startup command..."
echo "Command: cd $BACKEND_DIR && uv run uvicorn app.main:app --host 127.0.0.1 --port 9999 &"
echo -e "${YELLOW}Note: This will start server on port 9999 for 5 seconds${NC}"
read -p "Press Enter to test, or Ctrl+C to skip..."
cd "$BACKEND_DIR"
timeout 5 uv run uvicorn app.main:app --host 127.0.0.1 --port 9999 &
PID=$!
sleep 2
if ps -p $PID > /dev/null; then
    echo -e "${GREEN}✓ Server started successfully${NC}"
    curl -s http://127.0.0.1:9999/docs > /dev/null && echo -e "${GREEN}✓ API is responding${NC}" || echo -e "${RED}✗ API not responding${NC}"
    kill $PID 2>/dev/null || true
else
    echo -e "${RED}✗ Server failed to start${NC}"
fi
echo ""

# Summary
echo "========================================="
echo "Diagnostic Summary"
echo "========================================="
echo ""
echo "If you see any ✗ marks above, those need to be fixed."
echo ""
echo "Common fixes:"
echo "1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
echo "2. Fix permissions: sudo chown -R ai-tracks-studio:ai-tracks-studio $BACKEND_DIR"
echo "3. Create .env file with required variables"
echo "4. Copy service file: sudo cp $BACKEND_DIR/studio-uvicorn.service /etc/systemd/system/"
echo "5. Reload systemd: sudo systemctl daemon-reload"
echo "6. Restart service: sudo systemctl restart studio-uvicorn"
echo ""

