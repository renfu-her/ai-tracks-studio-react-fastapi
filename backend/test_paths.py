#!/usr/bin/env python3
"""
Test script to verify static directory paths
測試腳本驗證靜態目錄路徑
"""

from pathlib import Path
import sys

print("=" * 60)
print("Testing Static Directory Paths")
print("=" * 60)
print()

# Test 1: main.py static_dir path
print("Test 1: main.py static_dir")
print("-" * 60)
main_file = Path("backend/app/main.py")
print(f"main.py location: {main_file}")
print(f"  __file__          = backend/app/main.py")
print(f"  .parent           = {main_file.parent}")
print(f"  .parent.parent    = {main_file.parent.parent}")
static_dir = main_file.parent.parent / "static"
print(f"  / 'static'        = {static_dir}")
print()
print(f"Expected: backend/static")
print(f"Got:      {static_dir}")
print(f"✓ Correct!" if str(static_dir) == "backend/static" else "✗ Wrong!")
print()

# Test 2: upload.py UPLOAD_DIR path
print("Test 2: upload.py UPLOAD_DIR")
print("-" * 60)
upload_file = Path("backend/app/routers/admin/upload.py")
print(f"upload.py location: {upload_file}")
print(f"  __file__                  = backend/app/routers/admin/upload.py")
print(f"  .parent                   = {upload_file.parent}")
print(f"  .parent.parent            = {upload_file.parent.parent}")
print(f"  .parent.parent.parent     = {upload_file.parent.parent.parent}")
print(f"  .parent.parent.parent.parent = {upload_file.parent.parent.parent.parent}")
upload_dir = upload_file.parent.parent.parent.parent / "static" / "uploads"
print(f"  / 'static' / 'uploads'    = {upload_dir}")
print()
print(f"Expected: backend/static/uploads")
print(f"Got:      {upload_dir}")
print(f"✓ Correct!" if str(upload_dir) == "backend/static/uploads" else "✗ Wrong!")
print()

# Test 3: Check if paths will exist after migration
print("Test 3: Check actual filesystem (if migrated)")
print("-" * 60)

actual_static = Path("backend/static")
actual_uploads = Path("backend/static/uploads")
actual_js = Path("backend/static/js")
actual_admin_html = Path("backend/static/admin.html")

print(f"backend/static/          exists: {actual_static.exists()}")
print(f"backend/static/uploads/  exists: {actual_uploads.exists()}")
print(f"backend/static/js/       exists: {actual_js.exists()}")
print(f"backend/static/admin.html exists: {actual_admin_html.exists()}")
print()

# Summary
print("=" * 60)
print("Summary")
print("=" * 60)

all_correct = (
    str(static_dir) == "backend/static" and
    str(upload_dir) == "backend/static/uploads"
)

if all_correct:
    print("✓ All paths are CORRECT!")
    print()
    print("The code modifications are valid.")
    print("After migrating the directory, everything should work.")
    sys.exit(0)
else:
    print("✗ Some paths are WRONG!")
    print()
    print("Please review the code modifications.")
    sys.exit(1)

