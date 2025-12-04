#!/bin/bash
# Migrate static directory from backend/app/static to backend/static
# 將靜態目錄從 backend/app/static 遷移到 backend/static

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BACKEND_DIR="/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend"

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Migrate Static Directory${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""

# Check if we're in the right directory
if [ ! -d "$BACKEND_DIR" ]; then
    echo -e "${RED}✗ Backend directory not found: $BACKEND_DIR${NC}"
    echo "Please run this script from the backend directory."
    exit 1
fi

cd "$BACKEND_DIR"
echo -e "${GREEN}✓ Working directory: $(pwd)${NC}"
echo ""

# Check if old static directory exists
OLD_STATIC="$BACKEND_DIR/app/static"
NEW_STATIC="$BACKEND_DIR/static"

if [ ! -d "$OLD_STATIC" ]; then
    echo -e "${RED}✗ Old static directory not found: $OLD_STATIC${NC}"
    exit 1
fi

echo -e "${YELLOW}Old location:${NC} $OLD_STATIC"
echo -e "${YELLOW}New location:${NC} $NEW_STATIC"
echo ""

# Check if new location already exists
if [ -d "$NEW_STATIC" ]; then
    echo -e "${YELLOW}⚠ New static directory already exists!${NC}"
    echo "Do you want to:"
    echo "  1. Merge (copy files from old to new)"
    echo "  2. Replace (delete new and move old)"
    echo "  3. Backup and replace"
    echo "  4. Cancel"
    read -p "Choose (1-4): " choice
    
    case $choice in
        1)
            echo "Merging..."
            cp -r "$OLD_STATIC"/* "$NEW_STATIC/"
            echo -e "${GREEN}✓ Files merged${NC}"
            ;;
        2)
            echo "Replacing..."
            rm -rf "$NEW_STATIC"
            mv "$OLD_STATIC" "$NEW_STATIC"
            echo -e "${GREEN}✓ Directory moved${NC}"
            ;;
        3)
            BACKUP="$NEW_STATIC.backup.$(date +%Y%m%d_%H%M%S)"
            echo "Backing up to: $BACKUP"
            mv "$NEW_STATIC" "$BACKUP"
            mv "$OLD_STATIC" "$NEW_STATIC"
            echo -e "${GREEN}✓ Backup created and directory moved${NC}"
            ;;
        *)
            echo "Cancelled."
            exit 0
            ;;
    esac
else
    # Simply move the directory
    echo "Moving directory..."
    mv "$OLD_STATIC" "$NEW_STATIC"
    echo -e "${GREEN}✓ Directory moved successfully${NC}"
fi

echo ""

# Verify the new structure
echo "Verifying new structure..."
if [ -d "$NEW_STATIC" ]; then
    echo -e "${GREEN}✓ New static directory exists${NC}"
    
    # Check key directories
    for dir in "js" "css" "uploads" "admin"; do
        if [ -d "$NEW_STATIC/$dir" ]; then
            echo -e "${GREEN}  ✓ $dir/${NC}"
        else
            echo -e "${YELLOW}  ⚠ $dir/ not found${NC}"
        fi
    done
    
    # Check key files
    for file in "admin.html" "login.html"; do
        if [ -f "$NEW_STATIC/$file" ]; then
            echo -e "${GREEN}  ✓ $file${NC}"
        else
            echo -e "${YELLOW}  ⚠ $file not found${NC}"
        fi
    done
else
    echo -e "${RED}✗ New static directory not found${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}Migration Complete!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo ""
echo "New structure:"
echo "backend/"
echo "├── app/"
echo "│   ├── main.py"
echo "│   ├── models/"
echo "│   └── routers/"
echo "└── static/          ← Static files are here now"
echo "    ├── admin.html"
echo "    ├── login.html"
echo "    ├── js/"
echo "    ├── css/"
echo "    └── uploads/"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Restart backend service:"
echo "   ${BLUE}sudo systemctl restart studio-uvicorn${NC}"
echo ""
echo "2. Test backend:"
echo "   ${BLUE}curl http://127.0.0.1:9001/backend${NC}"
echo "   ${BLUE}curl http://127.0.0.1:9001/backend/static/js/admin.js${NC}"
echo ""
echo "3. Test through Nginx:"
echo "   ${BLUE}curl https://studio.ai-tracks.com/backend${NC}"
echo ""
echo -e "${GREEN}Done!${NC}"

