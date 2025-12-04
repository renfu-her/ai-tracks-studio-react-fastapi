#!/bin/bash
# Check static files on production server
# 檢查生產服務器上的靜態文件

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

BACKEND_DIR="/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend"

echo "========================================="
echo "Static Files Diagnostic"
echo "========================================="
echo ""

# 1. Check if directory exists
echo "1. Checking backend directory..."
if [ -d "$BACKEND_DIR" ]; then
    echo -e "${GREEN}✓ Backend directory exists${NC}"
    cd "$BACKEND_DIR"
else
    echo -e "${RED}✗ Backend directory not found${NC}"
    exit 1
fi
echo ""

# 2. Check static directory structure
echo "2. Checking static directory structure..."
STATIC_DIR="$BACKEND_DIR/app/static"
if [ -d "$STATIC_DIR" ]; then
    echo -e "${GREEN}✓ Static directory exists${NC}"
else
    echo -e "${RED}✗ Static directory not found${NC}"
    exit 1
fi

JS_DIR="$STATIC_DIR/js"
if [ -d "$JS_DIR" ]; then
    echo -e "${GREEN}✓ JS directory exists${NC}"
else
    echo -e "${RED}✗ JS directory not found${NC}"
    exit 1
fi
echo ""

# 3. Check required files
echo "3. Checking required JavaScript files..."
FILES=("admin.js" "template-loader.js" "common-ui.js")
MISSING=()

for file in "${FILES[@]}"; do
    if [ -f "$JS_DIR/$file" ]; then
        SIZE=$(stat -f%z "$JS_DIR/$file" 2>/dev/null || stat -c%s "$JS_DIR/$file" 2>/dev/null)
        echo -e "${GREEN}✓ $file${NC} ($SIZE bytes)"
    else
        echo -e "${RED}✗ $file - NOT FOUND${NC}"
        MISSING+=("$file")
    fi
done
echo ""

# 4. Check file permissions
echo "4. Checking file permissions..."
echo "Static directory:"
ls -ld "$STATIC_DIR"
echo ""
echo "JS directory:"
ls -ld "$JS_DIR"
echo ""
echo "JS files:"
ls -l "$JS_DIR"/*.js 2>/dev/null || echo "No JS files found"
echo ""

# 5. Test HTTP access
echo "5. Testing HTTP access to static files..."
SERVICE_URL="http://127.0.0.1:9001"

for file in "${FILES[@]}"; do
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL/static/js/$file" 2>/dev/null)
    if [ "$HTTP_STATUS" == "200" ]; then
        echo -e "${GREEN}✓ $file - HTTP $HTTP_STATUS${NC}"
    else
        echo -e "${RED}✗ $file - HTTP $HTTP_STATUS${NC}"
    fi
done
echo ""

# 6. Check service status
echo "6. Checking service status..."
if systemctl is-active --quiet studio-uvicorn; then
    echo -e "${GREEN}✓ studio-uvicorn service is running${NC}"
else
    echo -e "${RED}✗ studio-uvicorn service is NOT running${NC}"
fi
echo ""

# Summary
echo "========================================="
echo "Summary"
echo "========================================="
echo ""

if [ ${#MISSING[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All required files exist${NC}"
else
    echo -e "${RED}✗ Missing files:${NC}"
    for file in "${MISSING[@]}"; do
        echo "  - $file"
    done
fi
echo ""

# Recommendations
if [ ${#MISSING[@]} -gt 0 ]; then
    echo "Recommended actions:"
    echo "1. Pull latest code: git pull origin main"
    echo "2. Check .gitignore: cat backend/.gitignore"
    echo "3. Fix permissions: chmod -R 755 $STATIC_DIR"
    echo "4. Restart service: sudo systemctl restart studio-uvicorn"
    echo ""
fi

echo "For detailed troubleshooting, see:"
echo "  backend/FIX_STATIC_FILES_404.md"

