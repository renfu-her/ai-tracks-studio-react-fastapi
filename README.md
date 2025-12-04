# AI-Tracks Studio

A full-stack web application featuring a modern frontend portfolio and a powerful backend admin panel.

一個全棧網站應用程序，具有現代化的前端展示和強大的後台管理面板。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)
![React](https://img.shields.io/badge/React-19+-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Development](#development)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Frontend (Public Website) 前端（公開網站）

- 🎮 **Game Showcase** - Display interactive games and web experiences
- 🌐 **Website Portfolio** - Showcase web development projects
- 📰 **News Section** - Latest updates and announcements
- 📖 **About Page** - Company/Studio information
- 📱 **Fully Responsive** - Works on all devices
- 🎨 **Modern UI/UX** - Beautiful design with smooth animations
- 📝 **Markdown Support** - Rich content formatting
- 🔍 **SEO Friendly** - Clean URLs and semantic HTML

### Backend (Admin Panel) 後端（管理面板）

- 🔐 **Secure Authentication** - Session-based login system
- 📊 **Dashboard** - Overview of all content
- 🎯 **Project Management** - Create and manage games/websites
- 📢 **News Management** - Publish and edit news articles
- ℹ️ **About Management** - Update company information
- 🖼️ **Image Upload** - Automatic WebP conversion
- 📝 **Markdown Editor** - Rich text editing with EasyMDE
- 🗂️ **Content Organization** - Filter, search, and sort
- 📅 **Date Picker** - Easy date selection with Flatpickr
- 🎨 **Modern UI** - Bootstrap 5 interface
- 📱 **Responsive Design** - Works on desktop and mobile

## 🛠️ Tech Stack

### Backend 後端

- **Framework:** FastAPI (Python 3.11+)
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Package Manager:** uv
- **Authentication:** Session-based
- **Image Processing:** Pillow (WebP conversion)
- **API Documentation:** Swagger/OpenAPI

### Frontend 前端

- **Framework:** React 19
- **Language:** TypeScript 5
- **Build Tool:** Vite 6
- **Router:** React Router v7
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Package Manager:** pnpm
- **Markdown:** react-markdown + remark-gfm

### Backend Admin UI 後端管理界面

- **Framework:** Bootstrap 5
- **JavaScript:** jQuery (for dynamic loading)
- **Editor:** EasyMDE (Markdown)
- **Date Picker:** Flatpickr
- **Icons:** Font Awesome 6

## 📁 Project Structure

```
ai-tracks-studio/
├── backend/                    # Backend application
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── repositories/      # Data access layer
│   │   ├── routers/           # API routes
│   │   │   ├── admin/        # Admin API endpoints
│   │   │   └── public/       # Public API endpoints
│   │   ├── static/            # Static files
│   │   │   ├── admin/        # Admin panel HTML
│   │   │   ├── js/           # JavaScript files
│   │   │   └── uploads/      # Uploaded images
│   │   ├── core/              # Core configurations
│   │   ├── database.py        # Database setup
│   │   ├── security.py        # Authentication
│   │   └── main.py            # FastAPI application
│   ├── pyproject.toml         # Python dependencies
│   └── README.md              # Backend documentation
│
├── frontend/                   # Frontend application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── api/               # API client
│   │   ├── types.ts           # TypeScript types
│   │   ├── constants.ts       # Constants
│   │   └── App.tsx            # Main application
│   ├── public/                # Public assets
│   ├── package.json           # Frontend dependencies
│   ├── vite.config.ts         # Vite configuration
│   └── tsconfig.json          # TypeScript config
│
├── CHANGED.md                  # Changelog
└── README.md                   # This file
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

### For Backend 後端

- **Python 3.11+**
  ```bash
  python --version
  ```

- **uv** (Python package manager)
  ```bash
  # Install uv (if not installed)
  curl -LsSf https://astral.sh/uv/install.sh | sh
  
  # Or on Windows (PowerShell)
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  
  # Verify installation
  uv --version
  ```

- **MySQL 8.0+**
  ```bash
  mysql --version
  ```

### For Frontend 前端

- **Node.js 18+**
  ```bash
  node --version
  ```

- **pnpm**
  ```bash
  # Install pnpm (if not installed)
  npm install -g pnpm
  
  # Verify installation
  pnpm --version
  ```

## 🚀 Installation

### 1. Clone the Repository 克隆倉庫

```bash
git clone https://github.com/yourusername/ai-tracks-studio.git
cd ai-tracks-studio
```

### 2. Backend Setup 後端設置

```bash
# Navigate to backend directory
cd backend

# Install dependencies with uv
uv sync

# Create MySQL database
mysql -u root -p
```

```sql
CREATE DATABASE studio CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

```bash
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
EOF

# IMPORTANT: Edit .env and set your MySQL password
# nano .env  (or use your preferred editor)

# Run database migrations and seed data
mysql -u root -p studio < seed_about.sql
```

**Note:** See [ENV_SETUP.md](ENV_SETUP.md) for detailed environment configuration.

### 3. Frontend Setup 前端設置

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies with pnpm
pnpm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
```

**Note:** For production, change `VITE_API_BASE_URL` to your production API URL.

## 🏃 Running the Application

### Development Mode 開發模式

#### Terminal 1: Start Backend 啟動後端

```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Admin Panel: http://localhost:8000/backend

**Default Admin Credentials:**
- Email: `admin@admin.com`
- Password: `admin123`

#### Terminal 2: Start Frontend 啟動前端

```bash
cd frontend
pnpm dev
```

**Frontend will be available at:**
- Website: http://localhost:3000 (or http://localhost:5173)

### Production Mode 生產模式

#### Backend

```bash
cd backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Build for production
pnpm build

# Preview production build
pnpm preview
```

## 🔧 Development

### Backend Development 後端開發

**Add new dependencies:**
```bash
cd backend
uv add package-name
```

**Run specific Python file:**
```bash
uv run python script.py
```

**Database operations:**
```bash
# Check database schema
mysql -u root studio -e "DESCRIBE projects;"

# Run migration script
mysql -u root studio < migration.sql
```

### Frontend Development 前端開發

**Add new dependencies:**
```bash
cd frontend
pnpm add package-name
```

**Development with type checking:**
```bash
pnpm dev
```

**Build for production:**
```bash
pnpm build
```

**Type checking:**
```bash
pnpm tsc --noEmit
```

## 📚 API Documentation

### Public API Endpoints 公開 API 端點

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/projects` | GET | Get all projects (games/websites) |
| `/api/projects/{id}` | GET | Get single project |
| `/api/news` | GET | Get all news articles |
| `/api/news/{id}` | GET | Get single news article |
| `/api/about` | GET | Get about us content |

### Admin API Endpoints 管理 API 端點

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/admin/login` | POST | Admin login |
| `/api/admin/logout` | POST | Admin logout |
| `/api/admin/projects` | GET/POST | List/Create projects |
| `/api/admin/projects/{id}` | GET/PUT/DELETE | Get/Update/Delete project |
| `/api/admin/news` | GET/POST | List/Create news |
| `/api/admin/news/{id}` | GET/PUT/DELETE | Get/Update/Delete news |
| `/api/admin/about` | GET/POST | List/Create about |
| `/api/admin/about/{id}` | GET/PUT/DELETE | Get/Update/Delete about |
| `/api/admin/upload/image` | POST | Upload image (converts to WebP) |

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🎨 Features in Detail

### Image Upload & WebP Conversion 圖片上傳與 WebP 轉換

All uploaded images are automatically converted to WebP format for optimal performance:

- **Format:** Automatic WebP conversion
- **Naming:** UUID4-based naming (`YYYYMMDD-{uuid}.webp`)
- **Storage:** `/backend/app/static/uploads/`
- **Access:** `http://localhost:8000/static/uploads/filename.webp`

### Markdown Support Markdown 支持

Rich content editing with Markdown:

**Supported features:**
- Headings (H1-H6)
- Bold, italic, strikethrough
- Lists (ordered, unordered)
- Links (external, open in new tab)
- Code blocks (inline and block)
- Blockquotes
- Tables (GitHub Flavored Markdown)
- Images
- Horizontal rules

**Usage:**
- Backend: EasyMDE editor in admin panel
- Frontend: react-markdown renderer with styling

### Responsive Design 響應式設計

**Frontend:**
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Hamburger menu on mobile
- Touch-friendly interactions

**Backend Admin:**
- Bootstrap 5 responsive grid
- Hamburger menu for mobile
- Touch-optimized forms
- Tablet-friendly layout

## 🚀 Deployment

### Backend Deployment 後端部署

**Option 1: Traditional Server**

```bash
# Install dependencies
uv sync

# Run with gunicorn (production server)
uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Option 2: Docker**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install uv
RUN uv sync
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment 前端部署

**Option 1: Vercel (Recommended)**

```bash
# Install Vercel CLI
pnpm add -g vercel

# Deploy
cd frontend
vercel
```

**Option 2: Netlify**

```bash
# Build
pnpm build

# Deploy dist/ folder to Netlify
```

**Option 3: Static Hosting**

```bash
# Build
pnpm build

# Upload dist/ folder to any static host
# (e.g., GitHub Pages, Cloudflare Pages)
```

## 🔒 Security

- **Backend:** Session-based authentication with secure cookies
- **Passwords:** Bcrypt hashing
- **CORS:** Configured for specific origins
- **SQL Injection:** Protected by SQLAlchemy ORM
- **XSS:** React's built-in protection
- **File Upload:** Type validation and size limits

## 📝 Environment Variables

### Backend (.env)

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=studio

# Security
SECRET_KEY=your-secret-key-change-in-production

# Application
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
uv run pytest
```

### Frontend Tests

```bash
cd frontend
pnpm test
```

## 📖 Documentation

Additional documentation:

- [Backend Architecture](backend/FINAL_ARCHITECTURE.md)
- [Frontend API Integration](frontend/API_INTEGRATION.md)
- [Markdown Support](frontend/MARKDOWN_SUPPORT.md)
- [Bootstrap Guide](backend/BOOTSTRAP_GUIDE.md)
- [RWD Design](backend/RWD_DESIGN.md)
- [Auto Migration](backend/AUTO_MIGRATION.md)
- [Changelog](CHANGED.md)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **AI-Tracks Studio** - *Initial work*

## 🙏 Acknowledgments

- FastAPI for the amazing backend framework
- React team for the frontend library
- Tailwind CSS for styling utilities
- Bootstrap for admin panel components
- All open source contributors

## 📞 Support

For support, email contact@ai-tracks.studio or open an issue in the repository.

---

**Built with ❤️ by AI-Tracks Studio**

## 🔗 Quick Links

- [Live Demo](#) (Add your demo URL)
- [Documentation](https://docs.example.com)
- [Report Bug](https://github.com/yourusername/ai-tracks-studio/issues)
- [Request Feature](https://github.com/yourusername/ai-tracks-studio/issues)

## 📊 Project Status

- ✅ Backend API - Complete
- ✅ Admin Panel - Complete
- ✅ Frontend Website - Complete
- ✅ Markdown Support - Complete
- ✅ Image Upload - Complete
- ✅ Responsive Design - Complete
- 🚧 Unit Tests - In Progress
- 📝 Additional Features - Planned

## 🎯 Roadmap

- [ ] Add unit tests
- [ ] Add integration tests
- [ ] Add CI/CD pipeline
- [ ] Add Docker Compose
- [ ] Add analytics integration
- [ ] Add comment system
- [ ] Add search functionality
- [ ] Add multi-language support
- [ ] Add dark mode
- [ ] Add PWA support

