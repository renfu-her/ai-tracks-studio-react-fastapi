# Uploads Directory Git Configuration
# Uploads 目錄 Git 配置

## Overview 概述

The `backend/app/static/uploads/` directory is used to store uploaded images. This directory should **not** be tracked by Git because:

1. **Large Files** - Uploaded images can be large and bloat the repository
2. **Dynamic Content** - Upload files change frequently
3. **Environment-Specific** - Different environments have different uploads
4. **Security** - May contain sensitive user-uploaded content

`backend/app/static/uploads/` 目錄用於存儲上傳的圖片。此目錄**不應該**被 Git 追蹤，因為：

1. **大文件** - 上傳的圖片可能很大，會使倉庫膨脹
2. **動態內容** - 上傳文件頻繁變化
3. **環境特定** - 不同環境有不同的上傳文件
4. **安全性** - 可能包含敏感的用戶上傳內容

## Configuration 配置

### .gitignore Entry

The following has been added to `.gitignore`:

```gitignore
# Uploaded images (keep the directory, ignore contents)
backend/app/static/uploads/*
!backend/app/static/uploads/.gitkeep

# Also ignore any uploaded files in uploads subdirectories
backend/app/static/uploads/**/*
!backend/app/static/uploads/**/.gitkeep
```

### .gitkeep File

A `.gitkeep` file has been created at `backend/app/static/uploads/.gitkeep` to ensure:
- The directory structure is preserved in Git
- The uploads directory exists when cloning the repository
- No uploaded files are tracked

## How It Works 工作原理

```
backend/app/static/uploads/
├── .gitkeep              ← Tracked by Git (保留目錄結構)
├── 20251204-abc123.webp  ← Ignored by Git (上傳的圖片)
├── 20251204-def456.webp  ← Ignored by Git
└── 20251204-ghi789.webp  ← Ignored by Git
```

**Result:**
- ✅ Directory exists in repository
- ❌ Uploaded images are NOT tracked
- ✅ Clean repository without large files

## Remove Already Tracked Files 移除已追蹤的文件

If uploaded files were already tracked by Git before adding to `.gitignore`, you need to remove them from Git tracking:

如果上傳的文件在添加到 `.gitignore` 之前已經被 Git 追蹤，您需要將它們從 Git 追蹤中移除：

### Step 1: Check Current Status 檢查當前狀態

```bash
# Check what's currently tracked in uploads
git ls-files backend/app/static/uploads/

# If you see .webp or other image files, they need to be removed
```

### Step 2: Remove from Git (Keep Local Files) 從 Git 移除（保留本地文件）

```bash
# Remove all files from Git tracking (but keep local files)
git rm --cached -r backend/app/static/uploads/

# But add back the .gitkeep file
git add backend/app/static/uploads/.gitkeep
```

### Step 3: Commit Changes 提交更改

```bash
git commit -m "chore: stop tracking uploaded images in uploads directory"
```

### Step 4: Verify 驗證

```bash
# Check that only .gitkeep is tracked
git ls-files backend/app/static/uploads/

# Should only show:
# backend/app/static/uploads/.gitkeep
```

## One-Line Command 一行命令

If you want to do all the above in one go:

```bash
git rm --cached -r backend/app/static/uploads/ && \
git add backend/app/static/uploads/.gitkeep && \
git commit -m "chore: stop tracking uploaded images"
```

## Verification 驗證

### Check Git Tracking

```bash
# List tracked files in uploads directory
git ls-files backend/app/static/uploads/

# Should only show .gitkeep
```

### Test Upload

1. Upload an image through the admin panel
2. Check Git status:
   ```bash
   git status
   ```
3. The uploaded image should **NOT** appear in git status
4. Only changes to other files should show

### Check .gitignore

```bash
# Test if uploads are ignored
git check-ignore -v backend/app/static/uploads/test.webp

# Should show:
# .gitignore:123:backend/app/static/uploads/*    backend/app/static/uploads/test.webp
```

## Handling Different Environments 處理不同環境

### Development 開發環境

```bash
# Local uploads stay on your machine
# Not synced with Git
```

### Production 生產環境

**Option 1: Local Storage**
- Keep uploads on the server
- Not tracked by Git
- Backup separately from code

**Option 2: Cloud Storage (Recommended)**
- Upload to AWS S3, Cloudflare R2, etc.
- Only store filenames in database
- Much better for production

### Backup Uploads 備份上傳文件

Since uploads are not in Git, you need a separate backup strategy:

```bash
# Create backup of uploads
tar -czf uploads-backup-$(date +%Y%m%d).tar.gz backend/app/static/uploads/

# Or use rsync
rsync -av backend/app/static/uploads/ /path/to/backup/uploads/
```

## Best Practices 最佳實踐

### ✅ Do 應該做的

1. **Ignore Uploads in Git**
   - Keep repository clean
   - Avoid large binary files

2. **Use .gitkeep**
   - Preserve directory structure
   - Easy setup for new developers

3. **Backup Separately**
   - Regular backups of uploads
   - Separate from code backups

4. **Use Cloud Storage in Production**
   - AWS S3, Cloudflare R2
   - Better scalability and reliability

### ❌ Don't 不應該做的

1. **Don't Track Uploads in Git**
   - Makes repository bloated
   - Slows down clone/pull operations

2. **Don't Commit Large Files**
   - Use Git LFS if you must
   - Better: use cloud storage

3. **Don't Delete .gitkeep**
   - Needed to preserve directory structure
   - Other developers won't have uploads folder

## Troubleshooting 故障排除

### Issue: Uploads Still Showing in Git Status

**Problem:**
```bash
git status
# Shows: backend/app/static/uploads/image.webp
```

**Solution:**
```bash
# Remove from Git cache
git rm --cached backend/app/static/uploads/image.webp

# Or remove all
git rm --cached -r backend/app/static/uploads/
git add backend/app/static/uploads/.gitkeep

# Commit
git commit -m "chore: remove tracked uploads"
```

### Issue: Directory Doesn't Exist After Clone

**Problem:**
After cloning the repository, `backend/app/static/uploads/` doesn't exist.

**Solution:**
Make sure `.gitkeep` file is committed:
```bash
git add backend/app/static/uploads/.gitkeep
git commit -m "chore: add .gitkeep to preserve uploads directory"
git push
```

### Issue: .gitignore Not Working

**Problem:**
Files are still being tracked even after adding to `.gitignore`.

**Solution:**
```bash
# .gitignore only affects untracked files
# Remove from cache first
git rm --cached -r backend/app/static/uploads/
git add backend/app/static/uploads/.gitkeep

# Then commit
git commit -m "chore: apply .gitignore to uploads"
```

## Migration to Cloud Storage 遷移到雲存儲

If you want to move to cloud storage later:

### AWS S3 Example

```python
# backend/app/core/storage.py
import boto3
from app.core.config import settings

s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY
)

def upload_to_s3(file, filename):
    s3_client.upload_fileobj(
        file,
        settings.AWS_BUCKET_NAME,
        f'uploads/{filename}',
        ExtraArgs={'ContentType': 'image/webp'}
    )
    return f"https://{settings.AWS_BUCKET_NAME}.s3.amazonaws.com/uploads/{filename}"
```

### Benefits of Cloud Storage

- ✅ Unlimited scalability
- ✅ CDN integration
- ✅ Automatic backups
- ✅ Better performance
- ✅ Reduced server storage needs

## Summary 總結

**What's Tracked 被追蹤的：**
- ✅ `.gitkeep` file (preserves directory)

**What's Ignored 被忽略的：**
- ❌ All uploaded images (*.webp)
- ❌ Any other files in uploads/

**Commands to Remember 要記住的命令：**

```bash
# Check what's tracked
git ls-files backend/app/static/uploads/

# Remove from tracking
git rm --cached -r backend/app/static/uploads/

# Add .gitkeep back
git add backend/app/static/uploads/.gitkeep

# Verify .gitignore works
git check-ignore -v backend/app/static/uploads/test.webp
```

---

**Last Updated:** 2025-12-04  
**Status:** ✅ Configured and Documented

