# Environment Variables Setup 環境變量設置

## 📋 Overview 概述

This document explains how to set up environment variables for both backend and frontend.

本文檔說明如何為後端和前端設置環境變量。

## 🔧 Backend Environment Variables 後端環境變量

### Step 1: Create `.env` file 創建 `.env` 文件

```bash
cd backend
touch .env
```

### Step 2: Add Configuration 添加配置

Copy and paste the following into `backend/.env`:

```env
# ==========================================
# Database Configuration 資料庫配置
# ==========================================

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=studio

# ==========================================
# Security Configuration 安全配置
# ==========================================

SECRET_KEY=dev-secret-key-please-change-in-production

# ==========================================
# Application Configuration 應用配置
# ==========================================

ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000

# ==========================================
# Upload Configuration 上傳配置
# ==========================================

MAX_UPLOAD_SIZE=10
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp

# ==========================================
# Admin Configuration 管理員配置
# ==========================================

ADMIN_EMAIL=admin@admin.com
ADMIN_PASSWORD=admin123
```

### Step 3: Update Values 更新值

**Important configurations to change:**

1. **DB_PASSWORD** - Set your MySQL root password
   ```env
   DB_PASSWORD=your_mysql_password
   ```

2. **SECRET_KEY** - Change in production (use a random string)
   ```env
   SECRET_KEY=your-super-secret-random-key-here
   ```

3. **CORS_ORIGINS** - Add your production domain
   ```env
   CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
   ```

### Configuration Details 配置詳情

#### Database Settings 資料庫設置

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DB_HOST` | MySQL host address | `localhost` | `localhost` or `192.168.1.100` |
| `DB_PORT` | MySQL port | `3306` | `3306` |
| `DB_USER` | MySQL username | `root` | `root` or `studio_user` |
| `DB_PASSWORD` | MySQL password | (empty) | `your_password` |
| `DB_NAME` | Database name | `studio` | `studio` |

#### Security Settings 安全設置

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Session secret key | `dev-secret-key...` |

**Generate a secure SECRET_KEY:**

```bash
# Python method
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use OpenSSL
openssl rand -hex 32
```

#### Application Settings 應用設置

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment mode | `development` |
| `DEBUG` | Enable debug mode | `True` |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:3000,...` |

#### Upload Settings 上傳設置

| Variable | Description | Default |
|----------|-------------|---------|
| `MAX_UPLOAD_SIZE` | Max file size (MB) | `10` |
| `ALLOWED_EXTENSIONS` | Allowed file types | `jpg,jpeg,png,gif,webp` |

#### Admin Settings 管理員設置

| Variable | Description | Default |
|----------|-------------|---------|
| `ADMIN_EMAIL` | Default admin email | `admin@admin.com` |
| `ADMIN_PASSWORD` | Default admin password | `admin123` |

## 🎨 Frontend Environment Variables 前端環境變量

### Step 1: Create `.env` file 創建 `.env` 文件

```bash
cd frontend
touch .env
```

### Step 2: Add Configuration 添加配置

Copy and paste the following into `frontend/.env`:

```env
# ==========================================
# API Configuration API 配置
# ==========================================

VITE_API_BASE_URL=http://localhost:8000
```

### Step 3: Update for Different Environments 更新不同環境

#### Development 開發環境

```env
VITE_API_BASE_URL=http://localhost:8000
```

#### Production 生產環境

```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

#### Staging 測試環境

```env
VITE_API_BASE_URL=https://staging-api.yourdomain.com
```

### Configuration Details 配置詳情

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000` |

**Note:** All Vite environment variables must be prefixed with `VITE_` to be exposed to the client code.

注意：所有 Vite 環境變量必須以 `VITE_` 開頭才能在客戶端代碼中使用。

## 🚀 Quick Setup Commands 快速設置命令

### Backend 後端

```bash
# Navigate to backend
cd backend

# Create .env file
cat > .env << 'EOF'
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=studio
SECRET_KEY=dev-secret-key-please-change-in-production
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
MAX_UPLOAD_SIZE=10
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,webp
ADMIN_EMAIL=admin@admin.com
ADMIN_PASSWORD=admin123
EOF

# Edit DB_PASSWORD
nano .env  # or use your preferred editor
```

### Frontend 前端

```bash
# Navigate to frontend
cd frontend

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
```

## ✅ Verify Configuration 驗證配置

### Backend Verification 後端驗證

```bash
cd backend

# Check if .env exists
ls -la .env

# View content (be careful not to expose passwords!)
cat .env
```

### Frontend Verification 前端驗證

```bash
cd frontend

# Check if .env exists
ls -la .env

# View content
cat .env
```

## 🔒 Security Best Practices 安全最佳實踐

### 1. Never Commit `.env` Files 永遠不要提交 `.env` 文件

The `.env` files are already in `.gitignore`. Make sure they stay there!

```bash
# Verify .env is in .gitignore
grep ".env" ../.gitignore
```

### 2. Use Strong SECRET_KEY 使用強密鑰

**Bad:** ❌
```env
SECRET_KEY=123456
SECRET_KEY=secret
SECRET_KEY=myapp
```

**Good:** ✅
```env
SECRET_KEY=8f9a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8
```

### 3. Different Keys for Different Environments 不同環境使用不同密鑰

- **Development:** Can use simple keys
- **Production:** MUST use strong, unique keys

### 4. Restrict CORS Origins 限制 CORS 來源

**Development:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Production:**
```env
CORS_ORIGINS=https://yourdomain.com
```

### 5. Change Default Admin Credentials 更改預設管理員憑證

After first login, change the admin password in the admin panel!

首次登入後，在管理面板中更改管理員密碼！

## 🌍 Environment-Specific Configurations 特定環境配置

### Development 開發環境

**Backend:**
```env
ENVIRONMENT=development
DEBUG=True
DB_HOST=localhost
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend:**
```env
VITE_API_BASE_URL=http://localhost:8000
```

### Production 生產環境

**Backend:**
```env
ENVIRONMENT=production
DEBUG=False
DB_HOST=your-production-db-host
CORS_ORIGINS=https://yourdomain.com
SECRET_KEY=your-super-secure-production-key
```

**Frontend:**
```env
VITE_API_BASE_URL=https://api.yourdomain.com
```

### Docker Environment Docker 環境

**Backend:**
```env
DB_HOST=mysql  # Docker service name
DB_PORT=3306
DB_USER=root
DB_PASSWORD=secure_password
DB_NAME=studio
```

## 🐛 Troubleshooting 故障排除

### Backend Issues 後端問題

**Problem:** Cannot connect to database

**Solution:**
1. Check MySQL is running: `mysql -u root -p`
2. Verify DB_PASSWORD is correct
3. Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`

**Problem:** CORS errors

**Solution:**
1. Check CORS_ORIGINS includes your frontend URL
2. Restart backend after changing .env

### Frontend Issues 前端問題

**Problem:** API calls failing

**Solution:**
1. Check VITE_API_BASE_URL is correct
2. Ensure backend is running
3. Check browser console for CORS errors
4. Restart frontend after changing .env

**Problem:** Environment variable not loading

**Solution:**
1. Verify variable name starts with `VITE_`
2. Restart Vite dev server (`pnpm dev`)
3. Clear browser cache

## 📝 Example Files 範例文件

We provide `.env.example` files that you can copy:

**Backend:**
```bash
cd backend
cp .env.example .env
# Then edit .env with your values
```

**Frontend:**
```bash
cd frontend
cp .env.example .env
# Then edit .env with your values
```

## 🔗 Related Documentation 相關文檔

- [README.md](README.md) - Main project documentation
- [Backend Architecture](backend/FINAL_ARCHITECTURE.md)
- [Frontend API Integration](frontend/API_INTEGRATION.md)

---

**Remember:** Never commit `.env` files to version control!

**記住：** 永遠不要將 `.env` 文件提交到版本控制！

