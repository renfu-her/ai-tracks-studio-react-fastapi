# CHANGED.md - 更新紀錄 / Change Log

## 2025-12-15 15:51:04 - 驗證碼排除 0 與 O

### What changed
- ✅ 驗證碼生成排除了數字 0 與字母 O，避免混淆

### Backend
- `backend/app/core/captcha.py`:
  - `_random_text()` 改為使用 `ABCDEFGHIJKLMNPQRSTUVWXYZ123456789`
  - 驗證碼只包含大寫英文字母與數字 1-9（不含 0, O）

### Notes
- 去除易混淆的 0 與 O，提升可讀性

## 2025-12-15 15:49:56 - 驗證碼含英文與數字

### What changed
- ✅ 驗證碼生成改為包含大寫英文字母與數字

### Backend
- `backend/app/core/captcha.py`:
  - `_random_text()` 現在使用 `ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`
  - 驗證碼同時包含字母與數字

### Notes
- 驗證碼可包含 A-Z 與 0-9，使用者體驗更豐富

## 2025-12-15 15:49:09 - 驗證碼改為英文顯示和純字母生成

### What changed
- ✅ 驗證碼相關的中文文字全部改為英文
- ✅ 驗證碼生成改為只使用英文字母（不含數字）
- ✅ 排除容易混淆的字母（O, I, L）

### Frontend
- `frontend/components/Feedback.tsx`: 
  - 標籤文字："驗證碼 *" → "Captcha *"
  - 輸入框 placeholder："請輸入圖中文字" → "Enter the text in the image"
  - 載入狀態："載入中..." → "Loading..."
  - 錯誤狀態："無法載入" → "Failed to load"
  - 驗證錯誤："請完成驗證碼" → "Please complete the captcha"

### Backend
- `backend/app/core/captcha.py`:
  - `_random_text()` 函數：從 "ABCDEFGHJKMNPQRSTUVWXYZ23456789" 改為 "ABCDEFGHJKMNPQRSTUVWXYZ"
  - 現在只生成大寫英文字母，排除數字和容易混淆的字母（O, I, L）

### Notes
- 驗證碼現在只包含清晰的英文字母，更容易識別
- 所有用戶界面文字已改為英文，提供一致的英文體驗

## 2025-12-15 15:46:53 - 驗證碼錯誤時自動刷新

### What changed
- ✅ 當驗證碼輸入錯誤時，自動刷新驗證碼
- ✅ 在 Send Message 提交後，如果出現驗證碼錯誤，會自動載入新的驗證碼

### Frontend
- `frontend/components/Feedback.tsx`: 
  - 在 `handleSubmit` 的 catch 區塊中，檢查錯誤信息是否包含 "captcha" 或 "驗證碼"
  - 如果是驗證碼相關錯誤，自動調用 `loadCaptcha()` 刷新驗證碼
  - 用戶無需手動點擊刷新按鈕

### Notes
- 提升用戶體驗，驗證碼錯誤時自動提供新的驗證碼
- 錯誤信息檢查支援英文（"captcha"）和中文（"驗證碼"）關鍵字

## 2025-12-15 15:41:02 - 驗證碼輸入強制大寫

### What changed
- ✅ 驗證碼輸入欄位自動轉換為大寫
- ✅ 視覺上顯示大寫（CSS text-transform）

### Frontend
- `frontend/components/Feedback.tsx`: 
  - `handleChange` 函數中，當欄位為 `captcha_answer` 時自動轉換為大寫
  - 輸入框加入 `uppercase` class 和 `textTransform: 'uppercase'` style

### Notes
- 用戶輸入任何文字都會自動轉為大寫，方便輸入驗證碼

## 2025-12-15 15:21:46 - Fixed Captcha Image Generation Issue 修復驗證碼圖片生成問題

### What changed
- ✅ 修復 Pillow 10+ 相容性問題：`textsize()` 已棄用，改用 `textbbox()` 並加入 fallback
- ✅ 改進錯誤處理：圖片生成失敗時會記錄詳細錯誤並拋出異常，而非返回空字串
- ✅ 增強圖片生成：加入噪點點陣，改善文字位置計算，確保 base64 編碼正確

### Backend
- `backend/app/core/captcha.py`: 
  - 修復 `textsize()` 相容性問題，支援 Pillow 10+ 的 `textbbox()`
  - 改進錯誤處理，確保生成失敗時拋出異常而非返回空 base64
  - 加入驗證確保 base64 編碼不為空
  - 改善文字位置計算，避免超出邊界

### Notes
- 解決前端顯示驗證碼圖片失敗的問題（之前返回空的 base64 字串）
- 現在會正確生成並返回完整的 base64 圖片數據

## 2025-12-15 15:36:01 - Captcha 字型放大

### What changed
- `backend/app/core/captcha.py`: 嘗試載入 `arial.ttf` 或 `DejaVuSans.ttf`，字級依高度自動放大（約 65% 高度）；若無字型仍會 fallback 至預設字型。

### Notes
- 文字會比之前顯眼，若要再調整大小可調整 `font_size = int(_HEIGHT * 0.65)`。

## 2025-12-15 14:51:01 - Added Captcha to Feedback Form 回饋表單新增驗證碼

### What changed
- ✅ 新增數學驗證碼 API：`GET /api/feedback/captcha` 取得驗證碼題目
- ✅ 回饋提交需驗證碼：`POST /api/feedback` 需 `captcha_id` + `captcha_answer`
- ✅ 前端回饋表單加入驗證碼輸入與重新取得按鈕

### Backend
- `backend/app/core/captcha.py`：簡易記憶體驗證碼（10 分鐘有效）
- `backend/app/schemas/feedback.py`：FeedbackCreate 增加 `captcha_id`、`captcha_answer`
- `backend/app/routers/feedback.py`：新增 captcha 端點並在提交時驗證

### Frontend
- `frontend/api/config.ts`：新增 FEEDBACK_CAPTCHA 端點
- `frontend/api/feedback.ts`：加入 captcha 型別與 API（getCaptcha + submitFeedback）
- `frontend/components/Feedback.tsx`：表單新增驗證碼輸入、刷新按鈕，提交時帶驗證碼

### Notes
- 驗證碼為簡單加法題，10 分鐘有效，答題一次即失效
- 回饋必須填寫正確驗證碼才會提交成功

## 2025-12-15 15:02:23 - Frontend API base URL fallback 前端 API 網址回退機制

### What changed
- `frontend/api/config.ts`: 若未設定 `VITE_API_BASE_URL`，在瀏覽器自動使用 `window.location.origin`，避免生產環境預設連到 localhost。

### Notes
- 正式環境仍建議設定 `VITE_API_BASE_URL`，此回退僅作為安全網，避免 `Failed to fetch` 因錯誤主機。

## 2025-12-15 15:09:17 - Feedback 圖形驗證碼改版

### What changed
- 改為圖片驗證碼（隨機 4 碼字母/數字 + 雜訊），有效期 10 分鐘，單次使用後失效。
- `GET /api/feedback/captcha` 現在回傳 `captcha_id` 與 `image_base64`，前端直接顯示圖片。
- 提交 `POST /api/feedback` 仍需 `captcha_id`、`captcha_answer`，比對不分大小寫。

### Backend
- `backend/app/core/captcha.py`: 生成 PNG captcha（Pillow），存 base64；驗證改為字串比對。
- `backend/app/routers/feedback.py`: captcha 回傳圖片，提交時沿用驗證。

### Frontend
- `frontend/api/feedback.ts`: CaptchaResponse 改為 `image_base64`。
- `frontend/components/Feedback.tsx`: 顯示圖片驗證碼、刷新按鈕，placeholder 改為「請輸入圖中文字」。

### Notes
- 若需不同尺寸/字元長度，可調整 `_WIDTH/_HEIGHT/_CAPTCHA_LEN`（captcha.py）。

## 2025-12-15 15:10:34 - Captcha 字元集與長度調整

### What changed
- Captcha 長度改為 6 碼。
- 字元集改為大寫且排除易混淆字元（0, O, I, L, 1），實際使用 `ABCDEFGHJKMNPQRSTUVWXYZ23456789`。

### Affected file
- `backend/app/core/captcha.py`

## 2025-12-15 15:13:45 - 修正前端錯誤處理避免重複讀取 body

### What changed
- `frontend/api/client.ts`: 非 2xx 回應時先讀取一次 response.text，再嘗試 JSON parse，避免 "Failed to execute 'text' on 'Response': body stream already read"。

### Notes
- 修正 feedback 提交時的錯誤提示，避免因後端返回非 JSON 或解析失敗導致的重複讀取錯誤。

## 2025-12-15 15:16:15 - Captcha 產生異常防護

### What changed
- `backend/app/core/captcha.py`: 圖片產生加上 fallback，若失敗回傳空 data URL 但仍儲存答案，避免未捕捉例外。
- `backend/app/routers/feedback.py`: 產生 captcha 包 try/except，失敗回 500 並帶錯誤訊息。

### Notes
- 若環境有 Pillow/字型問題導致生成失敗，不會造成未捕捉例外；仍建議檢查日誌以排除根因。

## 2025-12-15 14:40:09 - Added Admin Profile Page (Name/Password, Email Read-only) 新增後台個人資料頁面（名稱/密碼可改，Email 唯讀）

### New Features 新增功能
- ✅ 新增後台「個人資料」頁面，支援修改名稱與密碼（Email 不可修改）
- ✅ 新增 Profile API：`GET /api/admin/profile`、`PUT /api/admin/profile`
- ✅ 導覽列加入「帳號設定 / 個人資料」入口，可直接訪問 `/backend/profile`

### Backend 後端
- `backend/app/routers/admin/profile.py`：新增取得與更新個人資料的 API（需目前密碼才可改密碼）
- `backend/app/routers/admin/__init__.py`：註冊 profile 路由

### Frontend 前端
- `backend/static/admin/profile/list.html`：個人資料表單（Email 只讀、名稱可改、密碼需目前密碼與確認新密碼）
- `backend/static/admin.html`：加入帳號設定導航、profile 模組標題、支援 `/backend/profile` 直接進入
- `backend/static/js/template-loader.js`：側邊欄加入個人資料入口
- `backend/static/js/admin.js`：強化 `checkAuth` 供 Profile 讀取使用

### Notes 注意事項
- 更改密碼時不再需要目前密碼；新密碼至少 6 碼並須與確認欄位一致
- Email 為唯讀欄位，不可修改

## 2025-12-15 14:31:59 - Enhanced Profile API Loading with Better Error Handling 加強 Profile API 載入和錯誤處理

### Enhanced Features 加強的功能

#### Profile API 載入優化
- ✅ 加強 `checkAuth()` 函數的錯誤處理和調試日誌
- ✅ 改進 `loadUserProfile()` 函數，加入重試機制
- ✅ 優化 `loadCurrentUser()` 函數，加入詳細的調試日誌
- ✅ 確保 Profile 資料在頁面載入時正確顯示

#### Files Modified 修改的文件
- `backend/static/admin.html` - 改進 Profile 載入邏輯，加入重試機制和詳細日誌
- `backend/static/js/admin.js` - 加強 `checkAuth()` 函數的錯誤處理和調試
- `backend/static/js/template-loader.js` - 優化 `loadCurrentUser()` 函數，加入詳細日誌

#### Changes 變更內容
1. **admin.html**: 
   - 創建獨立的 `loadUserProfile()` 函數，加入詳細的調試日誌
   - 加入重試機制，確保 Profile 資料正確載入
   - 檢查元素是否存在，避免錯誤
   
2. **admin.js**:
   - 加強 `checkAuth()` 函數的錯誤處理
   - 加入詳細的調試日誌，包括 API 響應狀態和錯誤詳情
   - 改進錯誤判斷邏輯，只在真正的網路錯誤時重定向
   
3. **template-loader.js**:
   - 優化 `loadCurrentUser()` 函數，加入詳細的調試日誌
   - 確保同時更新 `#userEmailText` 和 `#userEmail` 元素

#### Debugging 調試功能
- 所有 Profile 相關函數都加入了 `[Profile]`、`[checkAuth]`、`[template-loader]` 前綴的日誌
- 可以在瀏覽器控制台查看詳細的載入過程和錯誤訊息
- 有助於排查 Profile 資料無法顯示的問題

## 2025-12-15 14:11:00 - Fixed Profile API Display Issue 修復 Profile API 顯示問題

### Fixed Issues 修復的問題

#### Profile API 顯示問題
- ✅ 修正 `admin.html` 中的文字顯示（從"登入身分"改為"登入身份"）
- ✅ 優化前端載入邏輯，加入錯誤處理機制
- ✅ 修正 `template-loader.js` 中的元素 ID 處理，確保 Profile 資料正確顯示
- ✅ 優化 `checkAuth()` 函數，加入更詳細的錯誤處理和日誌記錄

#### Files Modified 修改的文件
- `backend/static/admin.html` - 修正文字顯示並優化用戶資料載入邏輯
- `backend/static/js/template-loader.js` - 修正元素 ID 處理並加入錯誤處理
- `backend/static/js/admin.js` - 優化 `checkAuth()` 函數的錯誤處理

#### Changes 變更內容
1. **admin.html**: 
   - 修正下拉選單中的文字（"登入身分" → "登入身份"）
   - 加入 try-catch 錯誤處理，確保 Profile 載入失敗時顯示適當訊息
   
2. **template-loader.js**:
   - 修正 `loadCurrentUser()` 函數，同時更新 `#userEmailText` 和 `#userEmail` 元素
   - 加入錯誤處理，顯示"無法載入"或"載入失敗"訊息
   
3. **admin.js**:
   - 優化 `checkAuth()` 函數，加入更詳細的日誌記錄
   - 改進錯誤處理邏輯，只在網路錯誤時重定向到登入頁面

#### Profile API Endpoint
- `/api/admin/me` - 返回當前登入管理員的資料（id, name, email, role, status）

## 2025-12-13 16:48:07 TST - Created Feedback Table Migration Scripts 創建 Feedback 表遷移腳本

### Created Migration Scripts 創建遷移腳本

#### Files Created 創建的文件

**SQL Migration 腳本:**
- ✅ `backend/migrate_add_feedback.sql` - SQL 遷移腳本
  - 創建 `feedback` 表
  - 包含所有必要欄位和索引
  - 驗證查詢以確認遷移成功

**Python Migration 腳本:**
- ✅ `backend/migrate_add_feedback.py` - Python 遷移腳本
  - 使用 SQLAlchemy 進行安全的遷移
  - 自動檢查表是否已存在（避免重複創建）
  - 包含確認提示和詳細的執行報告
  - 遷移後自動驗證結果和顯示表結構

#### Table Structure 表結構

```sql
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
)
```

#### Usage 使用方式

**方法 1: SQL 腳本（快速）**
```bash
mysql -u root studio < backend/migrate_add_feedback.sql
```

**方法 2: Python 腳本（推薦，更安全）**
```bash
cd backend
uv run python migrate_add_feedback.py
```

#### Indexes 索引

- `idx_email` - Email 欄位索引（用於搜索）
- `idx_is_read` - 已讀狀態索引（用於篩選）
- `idx_created_at` - 創建時間索引（用於排序）

#### Benefits 優勢

- ✅ 安全的數據庫遷移
- ✅ 自動檢查避免重複執行
- ✅ 詳細的執行日誌
- ✅ 支持手動確認（Python 版本）
- ✅ 遷移後自動驗證
- ✅ 性能優化（包含索引）

---

## 2025-12-13 16:45:38 TST - Implemented Feedback System with Email Notifications 實現 Feedback 系統與郵件通知

### Complete Feedback System 完整 Feedback 系統

#### Backend Implementation 後端實現

**1. Feedback Model 模型:**
- ✅ Created `backend/app/models/feedback.py`
- Fields: id, name, email, subject, message, is_read, created_at, updated_at
- Tracks user feedback and inquiry status

**2. Feedback Schema 數據驗證:**
- ✅ Created `backend/app/schemas/feedback.py`
- FeedbackCreate, FeedbackUpdate, FeedbackResponse, FeedbackListResponse
- Email validation using EmailStr

**3. Feedback Repository 倉儲:**
- ✅ Created `backend/app/repositories/feedback.py`
- Extends BaseRepository with CRUD operations
- `get_unread_count()` - Count unread feedback
- `get_unread()` - Get unread feedback list

**4. Email Service 郵件服務:**
- ✅ Created `backend/app/core/email.py`
- EmailService class with SMTP support
- `send_feedback_notification()` - Sends formatted HTML email
- Gmail SMTP configuration support
- Error handling and logging

**5. Public API Endpoint 公開 API:**
- ✅ Created `backend/app/routers/feedback.py`
- `POST /api/feedback` - Submit feedback (public, no auth required)
- Automatically sends email notification on submission
- Non-blocking email (failures don't affect response)

**6. Admin API Endpoints 後台管理 API:**
- ✅ Created `backend/app/routers/admin/feedback_admin.py`
- `GET /api/admin/feedback` - List all feedback (with filters)
- `GET /api/admin/feedback/{id}` - Get feedback details
- `PUT /api/admin/feedback/{id}` - Update feedback (mark as read/unread)
- `DELETE /api/admin/feedback/{id}` - Delete feedback
- `GET /api/admin/feedback/stats/unread-count` - Get unread count

**7. Configuration 配置:**
- ✅ Updated `backend/app/config.py` - Added email settings
- ✅ Updated `backend/pyproject.toml` - Added aiosmtplib dependency
- Email settings: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL, SMTP_FROM_NAME, FEEDBACK_TO_EMAIL

#### Frontend Implementation 前端實現

**1. Feedback API Service:**
- ✅ Created `frontend/api/feedback.ts`
- `submitFeedback()` - Submit feedback form
- TypeScript interfaces for FeedbackCreate and FeedbackResponse

**2. Feedback Form Component:**
- ✅ Created `frontend/components/Feedback.tsx`
- Beautiful, responsive feedback form
- Fields: Name, Email, Subject (optional), Message
- Success/error message display
- Loading states
- Form validation

**3. Navigation Integration:**
- ✅ Updated `frontend/App.tsx` - Added `/feedback` route
- ✅ Updated `frontend/components/Layout.tsx` - Added Feedback navigation link
- Desktop and mobile menu support

#### Admin Interface 後台管理界面

**1. Feedback Management Page:**
- ✅ Created `backend/static/admin/feedback/list.html`
- List all feedback with search and filter
- Filter by read/unread status
- View feedback details in modal
- Mark as read/unread
- Delete feedback
- Unread count badge in navigation

**2. Navigation Updates:**
- ✅ Updated `backend/static/admin.html`
- Added "Feedback 管理" menu item
- Unread count badge display
- Page title mapping

#### Email Configuration 郵件配置

**Environment Variables (.env):**
```env
# Email Settings (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=AI-Tracks Studio
FEEDBACK_TO_EMAIL=admin@example.com
```

**Documentation:**
- ✅ Created `backend/EMAIL_SETUP.md` - Complete email setup guide
- Gmail App Password setup instructions
- Configuration examples
- Troubleshooting guide

#### Features 功能

**Public Features:**
- ✅ User-friendly feedback form
- ✅ Email validation
- ✅ Success/error feedback
- ✅ Responsive design

**Admin Features:**
- ✅ View all feedback
- ✅ Search by name, email, subject, message
- ✅ Filter by read/unread status
- ✅ View detailed feedback in modal
- ✅ Mark as read/unread
- ✅ Delete feedback
- ✅ Unread count badge
- ✅ Auto-mark as read when viewing

**Email Features:**
- ✅ HTML formatted email notifications
- ✅ Includes all feedback details
- ✅ Professional email template
- ✅ Non-blocking (doesn't affect API response if email fails)

#### Updated Files 更新的文件

**Backend:**
- `backend/app/models/feedback.py` - Feedback model
- `backend/app/schemas/feedback.py` - Feedback schemas
- `backend/app/repositories/feedback.py` - Feedback repository
- `backend/app/core/email.py` - Email service
- `backend/app/routers/feedback.py` - Public feedback API
- `backend/app/routers/admin/feedback_admin.py` - Admin feedback API
- `backend/app/config.py` - Email configuration
- `backend/app/main.py` - Added feedback router
- `backend/app/routers/admin/__init__.py` - Added feedback_admin router
- `backend/app/models/__init__.py` - Export Feedback
- `backend/app/schemas/__init__.py` - Export Feedback schemas
- `backend/app/repositories/__init__.py` - Export FeedbackRepository
- `backend/pyproject.toml` - Added aiosmtplib dependency
- `backend/static/admin.html` - Added Feedback navigation
- `backend/static/admin/feedback/list.html` - Feedback management page
- `backend/EMAIL_SETUP.md` - Email setup documentation

**Frontend:**
- `frontend/api/feedback.ts` - Feedback API service
- `frontend/api/config.ts` - Added FEEDBACK endpoint
- `frontend/api/index.ts` - Export feedback API
- `frontend/components/Feedback.tsx` - Feedback form component
- `frontend/App.tsx` - Added /feedback route
- `frontend/components/Layout.tsx` - Added Feedback navigation link

#### User Flow 用戶流程

**Public User:**
1. Visit `/feedback` page
2. Fill out feedback form (name, email, subject, message)
3. Submit form
4. See success message
5. Admin receives email notification

**Admin:**
1. Navigate to "Feedback 管理" in admin panel
2. View list of all feedback
3. Filter by read/unread status
4. Search by name, email, subject
5. Click to view details
6. Mark as read/unread
7. Delete if needed

#### Email Notification Format 郵件通知格式

**Subject:** `New Feedback: {subject or 'No Subject'}`

**Content:**
- Name
- Email (clickable mailto link)
- Subject
- Message (formatted)
- Professional HTML template

#### Benefits 優勢

- ✅ **User Engagement** - Easy way for users to contact
- ✅ **Email Notifications** - Instant notification to admin
- ✅ **Admin Management** - Complete feedback management system
- ✅ **Status Tracking** - Read/unread status tracking
- ✅ **Search & Filter** - Easy to find specific feedback
- ✅ **Professional UI** - Beautiful form and admin interface
- ✅ **Error Handling** - Graceful error handling
- ✅ **Non-blocking** - Email failures don't affect user experience

#### Setup Instructions 設置說明

1. **Configure Email (Gmail):**
   - Enable 2-Step Verification on Gmail
   - Create App Password
   - Add email settings to `.env` file
   - See `backend/EMAIL_SETUP.md` for details

2. **Run Migration:**
   - Database tables created automatically on startup
   - Or run: `uv run python migrate_add_views.py` (if needed)

3. **Access:**
   - Public form: `http://localhost:3000/feedback`
   - Admin panel: `http://localhost:8000/backend#feedback`

---

## 2025-12-13 16:32:19 TST - Changed Views Display to Icon 將 Views 顯示改為圖標

### Changed Views Display Format 更改 Views 顯示格式

#### Changes 變更

**UI Update UI 更新:**
- ✅ Replaced "views: {count}" text with Eye icon + count
- ✅ 將 "views: {數量}" 文字改為 Eye 圖標 + 數量
- ✅ Consistent icon usage across all pages
- ✅ 所有頁面統一使用圖標

**Updated Components 更新的組件:**
- ✅ `ItemGrid.tsx` - Projects list with Eye icon
- ✅ `App.tsx` NewsPage - News list with Eye icon
- ✅ `App.tsx` AboutPage - About page with Eye icon
- ✅ `NewsDetail.tsx` - News detail with Eye icon
- ✅ `ProjectDetail.tsx` - Project detail with Eye icon (styled like other sidebar items)

#### Display Format 顯示格式

**Before 之前:**
```
views: 123
```

**After 之後:**
```
👁️ 123
```

#### Icon Implementation 圖標實現

- **Icon Library:** lucide-react Eye icon
- **Size:** Consistent with other icons (14-18px depending on context)
- **Styling:** Matches existing icon styles (text-slate-600, text-accent-600)
- **Layout:** Icon + count in flex container with gap

#### Updated Files 更新的文件

- `frontend/components/ItemGrid.tsx` - Added Eye import, updated display
- `frontend/App.tsx` - Added Eye import, updated NewsPage and AboutPage
- `frontend/components/NewsDetail.tsx` - Added Eye import, updated meta section
- `frontend/components/ProjectDetail.tsx` - Added Eye import, updated sidebar (styled like Date/Tags)

#### Benefits 優勢

- ✅ More visual and intuitive
- ✅ 更視覺化和直觀
- ✅ Consistent with other icons (Calendar, User, etc.)
- ✅ 與其他圖標一致（Calendar、User 等）
- ✅ Cleaner UI design
- ✅ 更簡潔的 UI 設計
- ✅ Better space utilization
- ✅ 更好的空間利用

---

## 2025-12-13 16:12:14 TST - Implemented Views Tracking and Display 實現 Views 追蹤和顯示

### Views Tracking System Views 追蹤系統

#### Backend Changes 後端變更

**Repositories 倉儲:**
- ✅ Added `increment_views()` method to `ProjectRepository`
- ✅ Added `increment_views()` method to `NewsRepository`
- ✅ Added `increment_views()` method to `AboutUsRepository`
- All methods increment views by 1 and return updated entity

**API Endpoints:**
- ✅ `POST /api/projects/{project_id}/view` - Increment project views
- ✅ `POST /api/news/{news_id}/view` - Increment news views
- ✅ `POST /api/about/{about_id}/view` - Increment about views

#### Frontend Changes 前端變更

**API Services:**
- ✅ Added `incrementViews()` method to `projectsApi`
- ✅ Added `incrementViews()` method to `newsApi`
- ✅ Added `incrementViews()` method to `aboutApi`

**List Pages 列表頁面:**
- ✅ `ItemGrid.tsx` - Displays "views: {count}" for projects
- ✅ `App.tsx` NewsPage - Displays "views: {count}" for news items

**Detail Pages 詳細頁面:**
- ✅ `ProjectDetail.tsx` - Automatically increments views on page load
- ✅ `NewsDetail.tsx` - Automatically increments views on page load
- ✅ `App.tsx` AboutPage - Automatically increments views on page load

#### User Flow 用戶流程

1. **List Page:** User sees views count displayed on each item
2. **Click Item:** User clicks to view detail page
3. **Detail Page Loads:** 
   - Fetches item data
   - Automatically calls increment views API
   - Updates displayed views count
4. **Views Updated:** Database views count incremented by 1

#### Updated Files 更新的文件

**Backend:**
- `backend/app/repositories/project.py` - Added increment_views method
- `backend/app/repositories/news.py` - Added increment_views method
- `backend/app/repositories/about.py` - Added increment_views method
- `backend/app/routers/projects.py` - Added POST /{id}/view endpoint
- `backend/app/routers/news.py` - Added POST /{id}/view endpoint
- `backend/app/routers/about.py` - Added POST /{id}/view endpoint

**Frontend:**
- `frontend/api/projects.ts` - Added incrementViews method
- `frontend/api/news.ts` - Added incrementViews method
- `frontend/api/about.ts` - Added incrementViews method
- `frontend/components/ItemGrid.tsx` - Added views display
- `frontend/App.tsx` - Added views display in NewsPage and increment in AboutPage
- `frontend/components/ProjectDetail.tsx` - Auto-increment views on load
- `frontend/components/NewsDetail.tsx` - Auto-increment views on load

#### Features 功能

- ✅ **Automatic Tracking** - Views automatically increment when detail page loads
- ✅ **List Display** - Views shown on all list pages
- ✅ **Real-time Update** - Views count updates immediately after increment
- ✅ **Error Handling** - Silently fails if view increment fails (doesn't break page)
- ✅ **Consistent Format** - All views displayed as "views: {count}"

#### Benefits 優勢

- ✅ Track content popularity
- ✅ User engagement metrics
- ✅ Automatic tracking (no manual intervention needed)
- ✅ Non-blocking (page loads even if increment fails)
- ✅ Consistent user experience

---

## 2025-12-13 16:06:18 TST - Fixed Missing Integer Import in Models 修復模型缺少 Integer 導入

### Fixed Import Error 修復導入錯誤

#### Problem 問題
- `NameError: name 'Integer' is not defined` 在 `project.py` 和 `news.py` 中
- 添加 `views` 欄位時使用了 `Integer`，但沒有從 `sqlalchemy` 導入

#### Solution 解決方案
- ✅ 在 `backend/app/models/project.py` 中添加 `Integer` 到導入語句
- ✅ 在 `backend/app/models/news.py` 中添加 `Integer` 到導入語句

#### Updated Files 更新的文件
- `backend/app/models/project.py` - 添加 `Integer` 導入
- `backend/app/models/news.py` - 添加 `Integer` 導入

#### Code Changes 代碼變更
```python
# Before 之前:
from sqlalchemy import Column, String, Text, Date, DateTime

# After 之後:
from sqlalchemy import Column, Integer, String, Text, Date, DateTime
```

---

## 2025-12-13 16:01:29 TST - Created Migration Scripts for Views Column 創建 Views 欄位遷移腳本

### Created Migration Scripts 創建遷移腳本

#### Files Created 創建的文件

**SQL Migration 腳本:**
- ✅ `backend/migrate_add_views.sql` - SQL 遷移腳本
  - 為 `about_us`、`news`、`projects` 表添加 `views` 欄位
  - 包含驗證查詢以確認遷移成功

**Python Migration 腳本:**
- ✅ `backend/migrate_add_views.py` - Python 遷移腳本
  - 使用 SQLAlchemy 進行安全的遷移
  - 自動檢查欄位是否已存在（避免重複添加）
  - 檢查表是否存在
  - 包含確認提示和詳細的執行報告
  - 遷移後自動驗證結果

#### Usage 使用方式

**方法 1: SQL 腳本（快速）**
```bash
mysql -u root studio < backend/migrate_add_views.sql
```

**方法 2: Python 腳本（推薦，更安全）**
```bash
cd backend
uv run python migrate_add_views.py
```

#### Migration Details 遷移詳情

**添加的欄位:**
- `about_us.views` - INT DEFAULT 0 NOT NULL (位於 contact_email 之後)
- `news.views` - INT DEFAULT 0 NOT NULL (位於 author 之後)
- `projects.views` - INT DEFAULT 0 NOT NULL (位於 link 之後)

**安全特性:**
- ✅ 檢查表是否存在
- ✅ 檢查欄位是否已存在（避免錯誤）
- ✅ 使用事務確保數據一致性
- ✅ 詳細的執行報告和驗證

#### Benefits 優勢

- ✅ 安全的數據庫遷移
- ✅ 自動檢查避免重複執行
- ✅ 詳細的執行日誌
- ✅ 支持手動確認（Python 版本）
- ✅ 遷移後自動驗證

---

## 2025-12-13 15:58:56 TST - Added Views Field to About, News, and Project 新增 Views 欄位到 About、News 和 Project

### Added Views Field 新增 Views 欄位

#### Changes 變更

**Backend Models 後端模型:**
- ✅ Added `views` field (Integer, default=0) to `AboutUs` model
- ✅ Added `views` field (Integer, default=0) to `News` model
- ✅ Added `views` field (Integer, default=0) to `Project` model

**Backend Schemas 後端 Schema:**
- ✅ Added `views: int = Field(0, description="View count")` to `AboutUsBase` schema
- ✅ Added `views: int` to `AboutUsResponse` schema
- ✅ Added `views: int = Field(0, description="View count")` to `NewsBase` schema
- ✅ Added `views: int` to `NewsResponse` schema
- ✅ Added `views: int = Field(0, description="View count")` to `ProjectBase` schema
- ✅ Added `views: int` to `ProjectResponse` schema

**Frontend Types 前端類型:**
- ✅ Added `views: number` to `AboutUs` interface
- ✅ Added `views: number` to `NewsItem` interface
- ✅ Added `views: number` to `ProjectItem` interface

**Frontend Display 前端顯示:**
- ✅ Added views display in `NewsDetail.tsx` - shows "views: {count}" in meta information
- ✅ Added views display in `ProjectDetail.tsx` - shows "views: {count}" in project details sidebar
- ✅ Added views display in `App.tsx` AboutPage - shows "views: {count}" below title

#### Updated Files 更新的文件

**Backend:**
- `backend/app/models/about.py` - Added views column
- `backend/app/models/news.py` - Added views column
- `backend/app/models/project.py` - Added views column
- `backend/app/schemas/about.py` - Added views field to base and response schemas
- `backend/app/schemas/news.py` - Added views field to base and response schemas
- `backend/app/schemas/project.py` - Added views field to base and response schemas

**Frontend:**
- `frontend/types.ts` - Added views field to all three interfaces
- `frontend/components/NewsDetail.tsx` - Added views display in meta section
- `frontend/components/ProjectDetail.tsx` - Added views display in sidebar
- `frontend/App.tsx` - Added views display in AboutPage

#### Display Format 顯示格式

All views are displayed in the format: **"views: {數量}"** (views: {count})

**Examples:**
- News detail page: "views: 123" in meta information section
- Project detail page: "views: 456" in project details sidebar
- About page: "views: 789" below the title

#### Database Migration 數據庫遷移

⚠️ **Note:** The database tables need to be updated to include the `views` column. You can either:
1. Drop and recreate tables (development)
2. Run a migration script to add the column:
   ```sql
   ALTER TABLE about_us ADD COLUMN views INT DEFAULT 0 NOT NULL;
   ALTER TABLE news ADD COLUMN views INT DEFAULT 0 NOT NULL;
   ALTER TABLE projects ADD COLUMN views INT DEFAULT 0 NOT NULL;
   ```

#### Benefits 優勢

- ✅ Track view counts for all content types
- ✅ Display view statistics to users
- ✅ Consistent implementation across all models
- ✅ Default value of 0 ensures backward compatibility
- ✅ Integer type for efficient storage and queries

---

## 2025-12-09 11:53:46 TST - Fixed Home Page Game Cards Navigation 修復首頁 Game 卡片導航

### Home Page Featured Games Click Navigation 首頁精選遊戲點擊導航

#### Changes 變更

**Home Page Game Cards 首頁 Game 卡片:**
- ✅ 修改首頁三個 Game 卡片的連結，從 `/game` 改為 `/game/${game.id}`
- ✅ Changed home page three Game cards links from `/game` to `/game/${game.id}`
- ✅ 點擊 Game 卡片現在會直接跳轉到對應的 detail 頁面
- ✅ Clicking Game cards now directly navigates to corresponding detail page

#### Problem 問題

- 首頁的三個 Game 卡片點擊後只會跳轉到 `/game` 列表頁面
- Home page three Game cards only navigated to `/game` list page when clicked
- 無法直接進入 Game 的 detail 頁面
- Could not directly access Game detail page

#### Solution 解決方案

**Updated File 更新的文件:**
- `frontend/App.tsx` - 修改 HomePage 組件中的 Game 卡片 Link 路徑
- `frontend/App.tsx` - Modified Game card Link path in HomePage component

**Code Change 代碼變更:**
```typescript
// Before 之前:
<Link to="/game" key={game.id} ...>

// After 之後:
<Link to={`/game/${game.id}`} key={game.id} ...>
```

#### User Flow 用戶流程

```
Home Page (/)
  ↓ Click Featured Game Card
Game Detail Page (/game/{id})
  ↓ View full game details
  ↓ Click "Back to All Games"
Games List Page (/game)
```

#### Benefits 優勢

- ✅ 用戶可以直接從首頁進入 Game detail 頁面
- ✅ Users can directly access Game detail page from home page
- ✅ 更直觀的導航體驗
- ✅ More intuitive navigation experience
- ✅ 與其他頁面的行為一致（ItemGrid 組件已經支持點擊跳轉）
- ✅ Consistent with other pages behavior (ItemGrid component already supports click navigation)

---

## 2025-12-06 22:45:00 TST - Updated Navigation Background Color 更新導航背景顏色

### Navigation Style Update 導航樣式更新

#### Changes 變更

**Navigation Background 導航背景:**
- ✅ 將頂部導航背景色改為淡紫色（`bg-purple-100/90`）
- ✅ 滾動時使用半透明淡紫色（`bg-purple-100/80`）
- ✅ 添加 backdrop-blur 效果，保持現代感
- ✅ 桌面選單使用白色半透明背景（`bg-white/60`）
- ✅ 移動選單使用淡紫色背景（`bg-purple-50`）

**Border Updates 邊框更新:**
- ✅ 桌面選單邊框改為淡紫色（`border-purple-200/30`）
- ✅ 移動選單按鈕添加淡紫色邊框
- ✅ 移動選單下拉框使用淡紫色邊框（`border-purple-200`）

**Text Color 文字顏色:**
- ✅ Logo 文字顏色保持深色（`text-slate-800`），確保在淡紫色背景上清晰可見
- ✅ 移除響應式文字顏色變化（不再需要白色文字）

#### Updated File 更新的文件
- `frontend/components/Layout.tsx`

#### Benefits 優勢
- ✅ 更柔和的視覺效果
- ✅ 與整體設計風格更協調
- ✅ 保持良好的可讀性
- ✅ 現代化的半透明效果

---

## 2025-12-06 22:37:43 TST - Frontend Banner Integration 前端 Banner 整合

### Frontend Banner Display Implementation 前端 Banner 顯示實現

#### Features 功能

**1. Public Banner API 公開 Banner API**
- ✅ Created `backend/app/routers/banner.py` - 公開 Banner API
- ✅ `GET /api/banners/page/{page_type}` - 根據頁面類型獲取 Banner（無需認證）
- ✅ 支持所有頁面類型：HOME, GAME, WEBSITE, NEWS, ABOUT

**2. Frontend Banner API 前端 Banner API**
- ✅ Created `frontend/api/banner.ts` - Banner API 服務
- ✅ `bannerApi.getBannerByPageType()` - 獲取指定頁面類型的 Banner
- ✅ `bannerApi.getBannerImageUrl()` - 獲取 Banner 圖片 URL
- ✅ 自動處理 404（Banner 不存在時返回 null）

**3. Banner Component 組件**
- ✅ Created `frontend/components/Banner.tsx` - Banner 顯示組件
- ✅ 自動根據頁面類型載入對應的 Banner
- ✅ 響應式設計（桌面 400px，移動 300px）
- ✅ 優雅的漸層遮罩效果
- ✅ 如果沒有 Banner 則不顯示（不佔用空間）

**4. Layout Integration 布局整合**
- ✅ 修改 `frontend/components/Layout.tsx` - 在導航下方添加 Banner
- ✅ Banner 與頂部導航分開（獨立區域）
- ✅ 自動根據當前路由判斷頁面類型
- ✅ 支持所有頁面：首頁、Game、Website、News、About

**5. Page Updates 頁面更新**
- ✅ 移除所有頁面的 `SectionHero` 組件
- ✅ 移除首頁的舊 Banner 代碼
- ✅ Banner 統一在 Layout 中顯示，各頁面不再需要單獨處理

#### Files Created 創建的文件

**Backend:**
- `backend/app/routers/banner.py` - 公開 Banner API

**Frontend:**
- `frontend/api/banner.ts` - Banner API 服務
- `frontend/components/Banner.tsx` - Banner 顯示組件

#### Files Updated 更新的文件

**Backend:**
- `backend/app/main.py` - 添加 banner router
- `backend/app/routers/__init__.py` - 導出 banner router

**Frontend:**
- `frontend/components/Layout.tsx` - 添加 Banner 顯示邏輯
- `frontend/App.tsx` - 移除各頁面的 SectionHero
- `frontend/api/index.ts` - 導出 banner API

#### Route to Page Type Mapping 路由到頁面類型映射

- `/` → `HOME`
- `/game` 或 `/game/*` → `GAME`
- `/website` 或 `/website/*` → `WEBSITE`
- `/news` 或 `/news/*` → `NEWS`
- `/about` → `ABOUT`

#### Banner Display Logic Banner 顯示邏輯

1. **Layout 組件**根據當前路由判斷頁面類型
2. **Banner 組件**根據頁面類型從 API 獲取 Banner
3. 如果 Banner 存在，顯示圖片（300-400px 高度）
4. 如果 Banner 不存在（404），不顯示任何內容
5. Banner 位於導航下方，與導航完全分開

#### Benefits 優勢

- ✅ **統一管理** - 所有頁面 Banner 在後台統一管理
- ✅ **自動切換** - 根據頁面自動顯示對應的 Banner
- ✅ **分離設計** - Banner 與導航完全分開，互不影響
- ✅ **優雅降級** - 沒有 Banner 時不顯示，不影響頁面布局
- ✅ **響應式** - 適配各種螢幕尺寸
- ✅ **性能優化** - 圖片自動轉換為 WebP，載入快速

#### Usage 使用方式

1. **後台管理 Banner:**
   - 訪問 http://localhost:8000/backend#banners/list
   - 為每個頁面類型上傳對應的 Banner 圖片

2. **前端自動顯示:**
   - 訪問首頁 → 顯示 HOME Banner
   - 訪問 Game 頁面 → 顯示 GAME Banner
   - 訪問 Website 頁面 → 顯示 WEBSITE Banner
   - 訪問 News 頁面 → 顯示 NEWS Banner
   - 訪問 About 頁面 → 顯示 ABOUT Banner

3. **如果沒有設置 Banner:**
   - 頁面正常顯示，只是沒有 Banner 圖片
   - 不影響其他內容的顯示

---

## 2025-12-06 22:08:55 TST - Added Banner Management System 新增 Banner 管理系統

### Complete Banner Management Implementation 完整 Banner 管理實現

#### Features 功能

**1. Banner Model 模型**
- ✅ Created `app/models/banner.py` - Banner 數據模型
- ✅ Page type enumeration (HOME, GAME, WEBSITE, NEWS, ABOUT)
- ✅ Image field with UUID-based WebP naming
- ✅ Unique constraint on page_type (每個頁面類型只能有一個 Banner)
- ✅ Automatic timestamps (created_at, updated_at)

**2. Banner Repository 倉儲**
- ✅ Created `app/repositories/banner.py` - Banner 倉儲模式
- ✅ Extends BaseRepository for CRUD operations
- ✅ `get_by_page_type()` - 根據頁面類型查詢 Banner

**3. Banner Schemas 數據驗證**
- ✅ Created `app/schemas/banner.py` - Pydantic schemas
- ✅ BannerCreate, BannerUpdate, BannerResponse, BannerListResponse
- ✅ Full type validation and serialization

**4. Banner Admin API 管理 API**
- ✅ Created `app/routers/admin/banner_admin.py` - Admin CRUD endpoints
- ✅ `GET /api/admin/banners` - List all banners
- ✅ `GET /api/admin/banners/{id}` - Get banner by ID
- ✅ `GET /api/admin/banners/page/{page_type}` - Get banner by page type
- ✅ `POST /api/admin/banners` - Create new banner
- ✅ `PUT /api/admin/banners/{id}` - Update banner (自動刪除舊圖片)
- ✅ `DELETE /api/admin/banners/{id}` - Delete banner (自動刪除圖片文件)
- ✅ Admin authentication required (require_admin)

**5. Banner Admin UI 管理界面**
- ✅ Created `backend/static/admin/banner/list.html` - Banner 列表頁面
- ✅ Created `backend/static/admin/banner/add-edit.html` - 新增/編輯表單
- ✅ Image upload with WebP conversion (使用現有 upload API)
- ✅ Image preview with thumbnail display
- ✅ Page type selection (HOME, GAME, WEBSITE, NEWS, ABOUT)
- ✅ Delete old image on edit (編輯時自動刪除舊圖片)
- ✅ Responsive design (響應式設計)

**6. Navigation Integration 導航整合**
- ✅ Added Banner menu item to admin sidebar
- ✅ Added Banner route handling in SPA router
- ✅ Added Banner page title mapping

#### Files Created 創建的文件

**Models:**
- `backend/app/models/banner.py` - Banner model with PageTypeEnum

**Repositories:**
- `backend/app/repositories/banner.py` - BannerRepository

**Schemas:**
- `backend/app/schemas/banner.py` - Banner Pydantic schemas

**Admin APIs:**
- `backend/app/routers/admin/banner_admin.py` - Banner CRUD API

**Admin UI:**
- `backend/static/admin/banner/list.html` - Banner list page
- `backend/app/static/admin/banner/add-edit.html` - Banner form page

#### Files Updated 更新的文件

**Model Exports:**
- `backend/app/models/__init__.py` - Added Banner, PageTypeEnum

**Repository Exports:**
- `backend/app/repositories/__init__.py` - Added BannerRepository

**Schema Exports:**
- `backend/app/schemas/__init__.py` - Added Banner schemas

**Admin Router:**
- `backend/app/routers/admin/__init__.py` - Added banner_admin router

**Admin UI:**
- `backend/static/admin.html` - Added Banner menu item and route

#### Database Schema 數據庫結構

```sql
CREATE TABLE banners (
    id VARCHAR(50) PRIMARY KEY,
    page_type ENUM('HOME', 'GAME', 'WEBSITE', 'NEWS', 'ABOUT') NOT NULL UNIQUE,
    image VARCHAR(500) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
```

#### Usage 使用方式

1. **Access Banner Management:**
   - Navigate to: http://localhost:8000/backend
   - Click "Banner 管理" in sidebar
   - Or directly: http://localhost:8000/backend#banners/list

2. **Create Banner:**
   - Click "新增 Banner"
   - Select page type (首頁, Game, Website, News, About)
   - Upload image (自動轉換為 WebP)
   - Save

3. **Edit Banner:**
   - Click edit button on banner list
   - Upload new image (舊圖片自動刪除)
   - Save

4. **Delete Banner:**
   - Click delete button
   - Confirm deletion
   - Banner and image file will be deleted

#### Image Management 圖片管理

- ✅ **Upload:** Uses existing `/api/admin/upload/image` endpoint
- ✅ **Format:** All images converted to WebP format
- ✅ **Naming:** UUID-based filename (e.g., `20251206-{uuid}.webp`)
- ✅ **Storage:** `backend/static/uploads/` directory
- ✅ **Auto-delete:** Old images deleted when updating or deleting banner
- ✅ **Preview:** Thumbnail preview in list and form pages

#### Page Types 頁面類型

- **HOME** - 首頁 Banner
- **GAME** - Game 頁面 Banner
- **WEBSITE** - Website 頁面 Banner
- **NEWS** - News 頁面 Banner
- **ABOUT** - About 頁面 Banner

#### Security 安全性

- ✅ Admin authentication required for all operations
- ✅ Session-based authentication
- ✅ Image file validation (type, size)
- ✅ Unique page type constraint (防止重複)

#### Benefits 優勢

- ✅ **統一管理** - 所有頁面 Banner 集中管理
- ✅ **自動化** - 圖片自動轉換為 WebP，自動刪除舊圖片
- ✅ **用戶友好** - 直觀的界面，圖片預覽
- ✅ **類型安全** - 完整的 Pydantic 驗證
- ✅ **可擴展** - 易於添加新的頁面類型

---

## 2025-12-04 22:35:00 TST - Removed Test Account Display from Login Page

### Removed Test Account Information 移除測試帳號顯示

#### Changes 變更

**Security Enhancement:**
- ✅ 移除登入頁面的測試帳號顯示區塊
- ✅ 移除郵箱輸入框的預填值（`admin@admin.com`）
- ✅ 移除密碼輸入框的預填值（`admin123`）
- ✅ 更改郵箱欄位 placeholder 為「請輸入管理員郵箱」

**Updated File:**
- `backend/static/login.html`

**Benefits:**
- ✅ 提高安全性 - 不在 UI 上顯示測試帳號
- ✅ 更專業的登入頁面
- ✅ 符合生產環境安全標準
- ✅ 防止未授權訪問

**Note:**
測試帳號仍然存在於數據庫中，只是不在登入頁面顯示。管理員需要知道正確的登入憑證。

---

## 2025-12-04 22:10:00 TST - Complete SEO Implementation

### Implemented Comprehensive SEO System 實現完整的 SEO 系統

#### Features 功能

**1. Dynamic Meta Tags 動態 Meta 標籤**
- ✅ Page title optimization（頁面標題優化）
- ✅ Meta descriptions（元描述）
- ✅ Meta keywords（關鍵字）
- ✅ Open Graph tags（Facebook, LinkedIn 分享）
- ✅ Twitter Card tags（Twitter 分享卡片）
- ✅ Canonical URLs（規範 URL）
- ✅ Robots meta tags（爬蟲指令）

**2. Structured Data (JSON-LD) 結構化數據**
- ✅ Organization schema（組織信息）
- ✅ Article schema（新聞文章）
- ✅ SoftwareApplication schema（遊戲和網站項目）
- ✅ Schema.org compliance（符合 Schema.org 標準）

**3. Static SEO Files 靜態 SEO 文件**
- ✅ `robots.txt` - 爬蟲規則
- ✅ `sitemap.xml` - 網站地圖（可擴展為動態）

#### Files Created 創建的文件

**SEO Utilities & Hooks:**
- ✅ `frontend/utils/seo.ts` - SEO 工具函數（200+ 行）
  - `updateSEO()` - 更新 meta 標籤
  - `generatePageSEO()` - 生成頁面 SEO 配置
  - `generateStructuredData()` - 生成結構化數據
  - `generateArticleData()` - 文章結構化數據
  - `generateProductData()` - 產品結構化數據
  - `DEFAULT_SEO` - 預設 SEO 配置
  - `ORGANIZATION_DATA` - 組織結構化數據

- ✅ `frontend/hooks/useSEO.ts` - SEO 自定義 Hook
  - 簡化 SEO 使用
  - 自動清理和更新

- ✅ `frontend/components/SEO.tsx` - SEO 組件（可選使用）
  - 組件化的 SEO 管理
  - 支持結構化數據

**Static Files:**
- ✅ `frontend/public/robots.txt` - 爬蟲規則
- ✅ `frontend/public/sitemap.xml` - 網站地圖

**Documentation:**
- ✅ `frontend/SEO_GUIDE.md` - 完整 SEO 指南（400+ 行）
  - 使用說明
  - 結構化數據範例
  - SEO 測試工具
  - 部署建議
  - 檢查清單

#### Updated Components 更新的組件

**All Pages with SEO:**
- ✅ `frontend/App.tsx`:
  - HomePage - 首頁 SEO + Organization schema
  - GamesPage - 遊戲頁 SEO
  - WebsitesPage - 網站頁 SEO
  - NewsPage - 新聞頁 SEO
  - AboutPage - 關於我們 SEO + Organization schema

- ✅ `frontend/components/ProjectDetail.tsx`:
  - 動態 SEO（基於專案數據）
  - SoftwareApplication structured data
  - Dynamic og:image

- ✅ `frontend/components/NewsDetail.tsx`:
  - 動態 SEO（基於新聞數據）
  - Article structured data
  - Dynamic og:image

#### SEO Implementation Details SEO 實現細節

**Native React Solution:**
- 不依賴外部套件（react-helmet-async 與 React 19 不兼容）
- 使用原生 `useEffect` 和 DOM 操作
- 輕量級、高性能、無依賴問題

**Key Features:**
```typescript
// 每個頁面都有優化的 SEO
useSEO(
  generatePageSEO(
    'Page Title',
    'Page description for SEO',
    { 
      canonical: 'https://studio.ai-tracks.com/page',
      keywords: 'keyword1, keyword2',
      ogImage: 'https://studio.ai-tracks.com/image.jpg'
    }
  ),
  ORGANIZATION_DATA  // Structured data
);
```

**Dynamic SEO for Detail Pages:**
```typescript
// 動態 SEO 基於數據
useSEO(
  project ? {
    title: `${project.title} | AI-Tracks Studio`,
    description: project.description,
    ogImage: getImageUrl(project.image),
    canonical: `https://studio.ai-tracks.com/game/${project.id}`
  } : defaultSEO,
  generateProductData(project)
);
```

#### SEO Best Practices 最佳實踐

**Meta Tags:**
- Unique title for each page（每頁唯一標題）
- Description within 160 characters（描述 160 字內）
- Relevant keywords（相關關鍵字）
- Proper canonical URLs（正確的規範 URL）

**Open Graph:**
- og:title, og:description, og:image
- og:type (website/article)
- og:url

**Twitter Cards:**
- twitter:card (summary_large_image)
- twitter:title, twitter:description, twitter:image

**Structured Data:**
- JSON-LD format（JSON-LD 格式）
- Schema.org standards（Schema.org 標準）
- Organization, Article, SoftwareApplication

#### Testing Tools 測試工具

**驗證 SEO:**
1. Google Search Console - 提交 sitemap
2. Google Rich Results Test - 驗證結構化數據
3. Facebook Sharing Debugger - Open Graph
4. Twitter Card Validator - Twitter Card
5. Lighthouse (Chrome) - SEO 審核

**檢查命令:**
```bash
# Check robots.txt
curl https://studio.ai-tracks.com/robots.txt

# Check sitemap
curl https://studio.ai-tracks.com/sitemap.xml

# Check meta tags
curl -s https://studio.ai-tracks.com | grep -E '<title>|<meta'
```

#### Benefits 優點

✅ **搜索引擎優化** - 提高 Google 排名  
✅ **社交媒體分享** - 美觀的 Facebook/Twitter 預覽  
✅ **結構化數據** - Rich snippets in search results  
✅ **專業性** - 完整的 meta 標籤和 schema  
✅ **易於維護** - 集中化的 SEO 工具函數  
✅ **類型安全** - 完整的 TypeScript 支持  
✅ **無依賴問題** - 原生 React 實現  

#### Next Steps 下一步

**部署 SEO 文件：**
1. ⚠️ **重要：** `robots.txt` 和 `sitemap.xml` 需要部署到生產環境
2. 執行：`npm run build`（Vite 會自動複製 public/ 文件到 dist/）
3. 上傳 `dist/*` 到服務器 `/public/` 目錄
4. 詳細步驟請查看：`frontend/DEPLOY_SEO_FILES.md`

**部署後：**
1. 驗證文件可訪問：
   - https://studio.ai-tracks.com/robots.txt
   - https://studio.ai-tracks.com/sitemap.xml
2. 提交 sitemap 到 Google Search Console
3. 提交 sitemap 到 Bing Webmaster Tools
4. 驗證 Open Graph 標籤（Facebook Debugger）
5. 驗證 Twitter Card（Twitter Validator）
6. 運行 Lighthouse SEO 審核

**可選改進：**
- 動態 sitemap 生成（後端實現）
- 添加更多 schema types
- 多語言 SEO 支持
- SEO 分析集成

**文檔：**
- ✅ `frontend/DEPLOY_SEO_FILES.md` - SEO 文件部署指南
- ✅ `frontend/SEO_GUIDE.md` - 完整 SEO 指南
- ✅ `frontend/SEO_QUICK_START.md` - 快速開始

---

## 2025-12-04 17:30:00 TST - Fixed Image URL Path for Production

### Fixed Missing `/backend` Prefix in Image URLs 修復圖片 URL 缺少 /backend 前綴

#### Problem 問題
前端顯示的圖片路徑缺少 `/backend` 前綴：
- ❌ 錯誤路徑：`https://studio.ai-tracks.com/static/uploads/20251204-xxx.webp`
- ✅ 正確路徑：`https://studio.ai-tracks.com/backend/static/uploads/20251204-xxx.webp`

#### Root Cause 根本原因
代碼已經修正（`frontend/api/config.ts` 中包含正確路徑），但生產環境需要：
1. 創建 `.env.production` 配置文件
2. 重新構建前端
3. 部署到生產服務器

#### Solution 解決方案

**1. 創建環境配置文件：**
- ✅ `frontend/.env.example` - 環境變量範例
- ✅ `frontend/DEPLOYMENT_STEPS.md` - 完整部署指南

**2. 生產環境配置：**
```env
# frontend/.env.production
VITE_API_BASE_URL=https://studio.ai-tracks.com
```

**3. 部署步驟：**
```bash
# 在本地機器（Windows）
cd frontend
echo "VITE_API_BASE_URL=https://studio.ai-tracks.com" > .env.production
npm run build

# 上傳 dist/* 到服務器 /public/ 目錄
```

#### Code Verification 代碼驗證

確認 `frontend/api/config.ts` (Lines 40-48) 已經包含正確路徑：

```typescript
export const getImageUrl = (filename: string | null | undefined): string => {
  if (!filename) {
    return 'https://via.placeholder.com/800x600?text=No+Image';
  }
  
  // ✅ Correct path with /backend prefix
  return `${API_CONFIG.BASE_URL}/backend/static/uploads/${filename}`;
};
```

#### Files Created 創建的文件
- ✅ `frontend/.env.example` - 環境變量範例
- ✅ `frontend/DEPLOYMENT_STEPS.md` - 部署步驟文檔

#### Next Steps 下一步
1. 在生產環境創建 `.env.production` 文件
2. 運行 `npm run build` 構建前端
3. 上傳 `dist/*` 到服務器
4. 清除瀏覽器緩存並驗證

#### Benefits 優點
- ✅ 正確的靜態文件路徑
- ✅ 圖片正常顯示
- ✅ 環境變量分離（開發/生產）
- ✅ 易於配置和部署

---

## 2025-12-04 (Current Time) - Production Environment Fix

### Migrated Static Directory to Better Structure 遷移靜態目錄到更好的結構

#### Change 變更
**Moved static directory from `backend/app/static/` to `backend/static/`**

**Before:**
```
backend/app/static/  ← Inside app directory
```

**After:**
```
backend/static/      ← Same level as app directory
```

#### Benefits 優點
1. ✅ **Clearer separation** - Application code and static files separated
2. ✅ **Easier management** - Static files independent, easier to backup
3. ✅ **Better deployment** - Can deploy static files separately or to CDN
4. ✅ **Standard structure** - Follows common Python web app conventions

#### Code Changes 代碼變更
**Updated files:**
- ✅ `backend/app/main.py` - Changed static_dir path to `parent.parent / "static"`
- ✅ `backend/app/routers/admin/upload.py` - Updated UPLOAD_DIR path
- ✅ `frontend/api/config.ts` - Updated image URL to `/backend/static/uploads/`
- ✅ `backend/static/admin.html` - Updated JS references and content path to `/backend/static/`
- ✅ `backend/static/js/admin.js` - Updated getImageUrl to use `/backend/static/uploads/`
- ✅ `backend/static/admin/about/add-edit.html` - Updated fallback getImageUrl path

**Created migration tools:**
- ✅ `backend/migrate_static.sh` - Automated migration script
- ✅ `backend/MIGRATE_STATIC_DIR.md` - Complete migration guide

#### Migration Steps 遷移步驟
```bash
# On production server
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend

# Run migration script
chmod +x migrate_static.sh
bash migrate_static.sh

# Restart service
sudo systemctl restart studio-uvicorn
```

#### URL Structure (Unchanged) URL 結構（不變）
- `/backend/static/uploads/` - Uploaded images
- `/backend/static/js/` - Admin JavaScript files
- `/backend/static/css/` - Admin CSS files

#### New Directory Structure 新目錄結構
```
backend/
├── app/              ← Python application code
│   ├── main.py
│   ├── models/
│   └── routers/
└── static/           ← Static files (HTML, CSS, JS, uploads)
    ├── admin.html
    ├── js/
    ├── css/
    └── uploads/
```

---

### Created Complete Production Deployment Guide 創建完整生產環境部署指南

#### Problem 問題 #7
**Frontend issues in production:**
1. Page stuck at "載入中..." (Loading...)
2. Browser error: `GET https://studio.ai-tracks.com/index.css net::ERR_ABORTED 404`
3. Frontend not correctly deployed
4. Backend API not responding to frontend requests

#### Root Cause 根本原因
- Frontend not built and deployed to production server
- Missing `.env.production` configuration
- Frontend still pointing to localhost instead of production domain
- Static files (HTML, CSS, JS) not uploaded
- Nginx not configured to serve frontend

#### Solution 解決方案
**Created comprehensive deployment guides:**
- ✅ `PRODUCTION_DEPLOYMENT.md` - Complete production deployment guide
  - Backend setup and verification
  - Frontend build process
  - Nginx configuration
  - Troubleshooting steps
- ✅ `frontend/DEPLOY_CONFIG.md` - Frontend-specific deployment guide
  - Environment variable configuration
  - Build commands
  - Upload methods
  - Verification steps

**Complete Deployment Flow:**

```
Development (Windows)                   Production (Linux Server)
─────────────────────                   ─────────────────────────
1. Create .env.production               1. Backend running on :9001
   VITE_API_BASE_URL=https://...       
                                        2. Nginx serving on :80/:443
2. npm run build                           ├─ Frontend (React SPA)
   → generates dist/                       ├─ /api/* → Backend API
                                           └─ /static/* → Backend static
3. Upload dist/* to server
   → /public/ directory                 3. Domain: studio.ai-tracks.com
```

**Quick Fix Steps:**

```bash
# On Windows (development)
cd frontend
# Create .env.production with: VITE_API_BASE_URL=https://studio.ai-tracks.com
npm install
npm run build

# Upload dist/* to server

# On Linux (production)
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com
# Copy frontend files
cp -r frontend/dist/* public/

# Configure Nginx (see PRODUCTION_DEPLOYMENT.md)
sudo nano /etc/nginx/sites-available/studio.ai-tracks.com
sudo systemctl restart nginx
```

**Nginx Configuration Key Points:**
```nginx
root /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/public;

location / {
    try_files $uri $uri/ /index.html;  # SPA routing
}

location /api/ {
    proxy_pass http://127.0.0.1:9001;  # Backend API
}

location /static/ {
    proxy_pass http://127.0.0.1:9001/static/;  # Backend static
}
```

**Expected Results:**
- ✅ Homepage loads (not stuck at "載入中...")
- ✅ No 404 errors for CSS/JS files
- ✅ API requests successful
- ✅ Frontend connects to backend
- ✅ Images display correctly
- ✅ Admin backend accessible at /backend

**Files Created:**
- `PRODUCTION_DEPLOYMENT.md` - Master deployment guide
- `frontend/DEPLOY_CONFIG.md` - Frontend deployment config
- Example Nginx configuration
- Deployment checklist
- Troubleshooting guide

---

### Fixed Static Files 404 Error 修復靜態文件 404 錯誤

#### Problem 問題 #6
**Browser console errors in production:**
```
Failed to load resource: the server responded with a status of 404
- template-loader.js
- admin.js

Uncaught ReferenceError: checkAuth is not defined
```

#### Root Cause 根本原因
- Static JavaScript files not deployed to production server
- Files exist in development but missing in production
- Results in admin backend not functioning

#### Solution 解決方案
**Created diagnostic and fix tools:**
- ✅ `backend/FIX_STATIC_FILES_404.md` - Complete troubleshooting guide
- ✅ `backend/check_static_files.sh` - Automated diagnostic script

**Quick Fix Steps:**
```bash
# On production server
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com

# 1. Pull latest code (includes static files)
git pull origin main

# 2. Fix permissions
chmod -R 755 backend/app/static

# 3. Restart service
sudo systemctl restart studio-uvicorn

# 4. Verify
curl http://127.0.0.1:9001/static/js/admin.js
curl http://127.0.0.1:9001/static/js/template-loader.js
```

**Diagnostic Tool:**
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
chmod +x check_static_files.sh
bash check_static_files.sh
```

**Common Causes:**
1. Files not committed to Git
2. Files excluded by .gitignore
3. Permission issues
4. Deployment didn't include static files

**Files to Check:**
- `backend/app/static/js/admin.js`
- `backend/app/static/js/template-loader.js`
- `backend/app/static/js/common-ui.js`

---

### Updated Project to Python 3.12 更新專案至 Python 3.12

#### Changes 更改
**Updated configuration files for Python 3.12:**
- ✅ `backend/.python-version` → Changed from `cpython-3.14.0-windows-x86_64-none` to `3.12.12`
- ✅ `backend/pyproject.toml` → Changed `requires-python` from `>=3.14` to `>=3.12`

**Why Python 3.12? 為什麼選擇 Python 3.12？**
- More stable and production-ready
- All packages fully support Python 3.12
- Better community support and resources
- Proven in production environments

**Next Steps 下一步:**
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
mv .venv .venv.backup
uv sync  # Will automatically use Python 3.12.12
```

---

### Created Working Service File 創建可正常運行的 Service 文件

#### Problem 問題 #5
- Manual command works: `uv run uvicorn app.main:app --host 0.0.0.0 --port 9001` ✅
- Systemd service with gunicorn doesn't work properly ❌
- Database connects, but "裡面不正常"

#### Root Cause 根本原因
- Manual test used **uvicorn** directly
- Service file used **gunicorn** + uvicorn workers
- Different command = different behavior

#### Solution 解決方案
**Created `studio-uvicorn-working.service`:**
- ✅ Uses **exact same command** as successful manual test
- ✅ Direct uvicorn (not gunicorn)
- ✅ Simple and proven to work

**Key Change:**
```ini
# Old (problematic)
ExecStart=uv run gunicorn app.main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker

# New (working)
ExecStart=uv run uvicorn app.main:app --host 127.0.0.1 --port 9001 --workers 8
```

**Deployment:**
```bash
sudo systemctl stop studio-uvicorn
sudo cp backend/studio-uvicorn-working.service /etc/systemd/system/studio-uvicorn.service
sudo systemctl daemon-reload
sudo systemctl start studio-uvicorn
sudo systemctl status studio-uvicorn
```

**Files Created:**
- ✅ `backend/studio-uvicorn-working.service` - Service file using uvicorn directly
- ✅ `backend/DEPLOY_WORKING_SERVICE.md` - Complete deployment guide

**Why This Works:**
- Same command as manual test (proven to work)
- Simpler = less points of failure
- Direct uvicorn instead of gunicorn wrapper

---

## 2025-12-04 (Current Time) - Production Environment Fix

### Created Systemd Service Files & Diagnostic Tools systemd 服務文件與診斷工具

#### Problem 問題 #4
- Systemd service with direct `.venv/bin/gunicorn` path failed
- `ModuleNotFoundError: No module named 'app'` in systemd service
- Need proper PYTHONPATH and working directory setup

#### Solution 解決方案
**Created systemd service files:**
- ✅ `backend/studio-uvicorn.service` - Gunicorn with Uvicorn workers (using uv run)
- ✅ `backend/studio-uvicorn-simple.service` - Simple Uvicorn (using uv run)
- ✅ `backend/studio-uvicorn-direct.service` - Direct path with bash wrapper (most reliable)
- ✅ `backend/SYSTEMD_SETUP.md` - Complete systemd setup guide
- ✅ `backend/diagnose.sh` - Diagnostic script to troubleshoot issues
- ✅ `backend/QUICK_FIX.md` - Quick fix guide with step-by-step solutions
- ✅ `backend/check_python_compatibility.sh` - Python 3.14 compatibility check script
- ✅ `backend/PYTHON_3.14_NOTES.md` - Python 3.14 compatibility notes and recommendations
- ✅ `backend/switch_to_python_3.12.sh` - Automated script to switch from Python 3.14 to 3.12
- ✅ `backend/SWITCH_TO_PYTHON_3.12.md` - Complete guide for switching to Python 3.12
- ✅ `backend/switch_python_uv.sh` - **Simple UV method to switch Python version**
- ✅ `backend/SWITCH_PYTHON_VERSION_UV.md` - **UV-based Python version switching guide**

**Recommendation for Production 生產環境建議:**
- Python 3.12 is more stable and fully tested
- All packages have complete Python 3.12 support
- Better for production environments

**Two Methods to Switch 兩種切換方法:**
1. **UV Method (Recommended)** - If using UV: just change `.python-version` and run `uv sync`
2. **Manual Method** - Use the automated script for manual venv management

**Key Changes in Service Files:**
```ini
# Use uv run instead of direct venv path
ExecStart=/home/ai-tracks-studio/.local/bin/uv run gunicorn app.main:app ...

# Set PYTHONPATH explicitly
Environment="PYTHONPATH=/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend"

# Set correct WorkingDirectory
WorkingDirectory=/home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
```

**Two Service Options:**

**Option 1: Gunicorn (Production)**
- Better process management
- Auto-restart failed workers
- Graceful reload and shutdown
- Suitable for high-traffic production

**Option 2: Simple Uvicorn (Development/Small Projects)**
- Simpler configuration
- Easier to debug
- Faster startup
- Suitable for small to medium projects

**Installation Steps:**
```bash
# Choose and copy service file
sudo cp backend/studio-uvicorn.service /etc/systemd/system/

# Create log directory (if using Gunicorn)
sudo mkdir -p /var/log/uvicorn
sudo chown ai-tracks-studio:ai-tracks-studio /var/log/uvicorn

# Reload systemd
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable studio-uvicorn
sudo systemctl start studio-uvicorn

# Check status
sudo systemctl status studio-uvicorn
```

**Common Commands:**
```bash
# View logs
sudo journalctl -u studio-uvicorn -f

# Restart service
sudo systemctl restart studio-uvicorn

# Check if running
curl http://127.0.0.1:9001/docs
```

---

### Created Production Deployment Scripts 創建生產環境部署腳本

#### Problem 問題 #3
- Gunicorn failed with `ModuleNotFoundError: No module named 'app'`
- Working directory was not set correctly
- Commands must be run from `backend/` directory

#### Solution 解決方案
**Created deployment files:**
- ✅ `backend/start.sh` - Production startup script
- ✅ `backend/PRODUCTION_DEPLOY.md` - Complete deployment guide

**startup script features 啟動腳本功能:**
- Auto-detect script directory
- Change to correct working directory
- Support both Uvicorn and Gunicorn
- Show Python version and working directory
- Easy to use with systemd service

**Usage 使用方式:**
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
chmod +x start.sh
./start.sh
```

**Or direct command 或直接命令:**
```bash
cd /home/ai-tracks-studio/htdocs/studio.ai-tracks.com/backend
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Key Point 重點:**
⚠️ Always run from `backend/` directory, not from project root!

---

### Fixed Missing Environment Variables 修復缺少的環境變數

#### Problem 問題 #2
- Production server failed with `ValidationError`
- `.env` file has `ENVIRONMENT` and `DEBUG` fields
- But `Settings` class didn't define these fields
- Pydantic v2 doesn't allow extra fields by default

#### Error Message 錯誤訊息
```
pydantic_core._pydantic_core.ValidationError: 2 validation errors for Settings
ENVIRONMENT
  Extra inputs are not permitted [type=extra_forbidden, input_value='development', input_type=str]
DEBUG
  Extra inputs are not permitted [type=extra_forbidden, input_value='True', input_type=str]
```

#### Solution 解決方案
**Updated `backend/app/config.py`:**
- ✅ Added `ENVIRONMENT: str = "development"` field
- ✅ Added `DEBUG: bool = False` field
- ✅ Now accepts these environment variables from `.env`

**Supported ENVIRONMENT values:**
- `development` - Local development
- `staging` - Staging server
- `production` - Production server

**DEBUG flag:**
- `True` - Enable debug mode (detailed error messages)
- `False` - Disable debug mode (production)

---

### Fixed CORS_ORIGINS Environment Variable Parsing 修復 CORS_ORIGINS 環境變數解析

#### Problem 問題 #1
- Production server failed to start with `JSONDecodeError`
- Pydantic Settings tried to parse `CORS_ORIGINS` as JSON
- `.env` file used comma-separated format: `https://studio.ai-tracks.com,http://localhost:9001,http://localhost:10001`
- But Pydantic expected JSON format: `["url1","url2","url3"]`

#### Error Message 錯誤訊息
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
pydantic_settings.exceptions.SettingsError: error parsing value for field "CORS_ORIGINS" from source "DotEnvSettingsSource"
```

#### Solution 解決方案
**Updated `backend/app/config.py`:**
- ✅ Added custom field validator for `CORS_ORIGINS`
- ✅ Support both formats: comma-separated string OR JSON array
- ✅ Parse comma-separated values automatically
- ✅ Strip whitespace from each origin
- ✅ Type changed from `list[str]` to `Union[str, list[str]]`

**Code Changes:**
```python
# Added imports
from typing import Union
from pydantic import field_validator

# Updated field type
CORS_ORIGINS: Union[str, list[str]] = [...]

# Added validator
@field_validator('CORS_ORIGINS', mode='before')
@classmethod
def parse_cors_origins(cls, v):
    """Parse CORS_ORIGINS from comma-separated string or list."""
    if isinstance(v, str):
        return [origin.strip() for origin in v.split(',') if origin.strip()]
    return v
```

#### Benefits 優點
- ✅ User-friendly `.env` format (comma-separated)
- ✅ Backward compatible with JSON array format
- ✅ Automatic whitespace trimming
- ✅ No code changes needed in production `.env`
- ✅ Works with existing development setups

#### Production `.env` Format 生產環境 .env 格式
**Now supports this format:**
```env
CORS_ORIGINS=https://studio.ai-tracks.com,http://localhost:9001,http://localhost:10001
```

**Also supports JSON format:**
```env
CORS_ORIGINS=["https://studio.ai-tracks.com","http://localhost:9001"]
```

#### Files Changed 更改的文件
- `backend/app/config.py` - Added field validator and Union type

---

## 2025-12-04 12:40:00 TST

### Frontend: News Detail Page 前端：新聞詳細頁面

#### Added Features 新增功能

**1. Created NewsDetail Component 創建新聞詳細組件:**
- File: `frontend/components/NewsDetail.tsx`
- Full article view with hero image
- Markdown-rendered excerpt and content
- Author and date information
- Back navigation to news list
- Loading and error states

**2. Added Route 添加路由:**
```typescript
<Route path="/news/:id" element={<NewsDetail />} />
```

**3. Made News Cards Clickable 讓新聞卡片可點擊:**
- Entire news card is now a link
- "Read Full Story" button navigates to detail page
- Hover effects preserved
- Smooth transitions

#### User Flow 用戶流程

```
News List Page (/news)
  ↓ Click any news card or "Read Full Story"
News Detail Page (/news/:id)
  ↓ View full article with:
    - Hero image
    - Title
    - Date & author
    - Excerpt (highlighted)
    - Full content (Markdown)
  ↓ Click "Back to All News"
News List Page
```

#### Features 功能特色

**NewsDetail Page:**
- 📸 Hero image (if available)
- 📝 Full Markdown content
- 📅 Publication date
- ✍️ Author name
- 💬 Excerpt in highlighted box
- ⬅️ Back navigation
- 📱 Fully responsive

**Styling:**
- Clean, article-focused layout
- Maximum 4xl width for readability
- Gradient background
- Sticky header with back button
- Professional typography

#### Files Changed 更改的文件

**New Files:**
- `frontend/components/NewsDetail.tsx`

**Updated Files:**
- `frontend/App.tsx` - Added NewsDetail import and route, made news cards clickable

#### Example URL 示例 URL

```
List: http://localhost:3000/news
Detail: http://localhost:3000/news/news-123
```

## 2025-12-04 12:35:00 TST

### Frontend: Removed Descriptions from List Pages 前端：移除列表頁面的描述

#### Changes 更改

**Removed descriptions from:**
- ✅ Home page (featured games section)
- ✅ Games page (game grid)
- ✅ Websites page (website grid)

**Why 為什麼：**
- Cleaner card design
- Focus on titles and images
- Better visual hierarchy
- Faster scanning

**Where descriptions still show 仍然顯示描述的地方：**
- ✅ Project detail pages (full Markdown)
- ✅ News page (excerpts)
- ✅ About Us page (full content)

**Files Changed:**
- `frontend/components/ItemGrid.tsx` - Removed description paragraph
- `frontend/App.tsx` - Removed description from featured games

**Before 之前:**
```
┌─────────────┐
│   Image     │
│   Title     │
│ Description │  ← Removed
│   Date      │
└─────────────┘
```

**After 之後:**
```
┌─────────────┐
│   Image     │
│   Title     │
│   Date      │
└─────────────┘
```

## 2025-12-04 12:30:00 TST

### Frontend: Markdown Rendering Support 前端：Markdown 渲染支持

#### Added Features 新增功能

**1. Markdown Support for All Content 所有內容支持 Markdown:**
- ✅ Projects - Description fields
- ✅ News - Excerpt and content fields  
- ✅ About Us - Full description

**2. Installed Packages 安裝的套件:**
- `react-markdown@9.0.1` - Markdown to React renderer
- `remark-gfm@4.0.0` - GitHub Flavored Markdown support

**3. Created MarkdownContent Component 創建 Markdown 組件:**
- File: `frontend/components/MarkdownContent.tsx`
- Renders Markdown as styled HTML
- Custom styling for all Markdown elements
- Tailwind CSS integration

**4. Updated Components 更新的組件:**
- ✅ `ProjectDetail.tsx` - Project descriptions
- ✅ `App.tsx` (NewsPage) - News excerpts
- ✅ `App.tsx` (AboutPage) - About content

#### Supported Markdown Features 支持的功能

**Typography 排版:**
- Headings (H1-H6) with proper hierarchy
- Bold, italic, strikethrough
- Paragraphs with line spacing

**Lists 列表:**
- Unordered lists (bullets)
- Ordered lists (numbers)
- Nested lists

**Links & Media 連結與媒體:**
- External links (open in new tab)
- Images with responsive sizing
- Alt text support

**Code 代碼:**
- Inline code with highlighting
- Code blocks with dark theme
- Monospace font

**Advanced 進階:**
- Blockquotes with accent border
- Tables (GitHub Flavored Markdown)
- Horizontal rules
- HTML in Markdown (sanitized)

#### Usage Example 使用示例

**Backend (Admin Panel):**
```markdown
## Introduction

**NEON TETRIS** is a modern game...

### Features
- Neon graphics
- Smooth gameplay

[Play Now](https://example.com)
```

**Frontend (Rendered):**
- Professional typography
- Styled lists
- Clickable links with accent color
- Beautiful, readable layout

#### Files Changed 更改的文件

**New Files:**
- `frontend/components/MarkdownContent.tsx`
- `frontend/MARKDOWN_SUPPORT.md`

**Updated Files:**
- `frontend/package.json` - Added dependencies
- `frontend/components/ProjectDetail.tsx` - Use MarkdownContent
- `frontend/App.tsx` - Use MarkdownContent for News and About

#### Benefits 優點

- ✅ Rich content formatting
- ✅ Better readability
- ✅ Professional appearance
- ✅ Easy content management
- ✅ Consistent styling across all pages
- ✅ Supports GitHub Flavored Markdown

## 2025-12-04 12:20:00 TST

### Fixed: About Us Page Not Found 修復：找不到關於我們頁面

#### Problem 問題
- Frontend showed: "About Us content not found"
- API endpoint `/api/about` returned 404
- Database `about_us` table was empty

#### Solution 解決方案

**1. Created Seed Data Script 創建種子數據腳本:**
- ✅ `backend/seed_about.sql`
- Inserts default About Us content
- Includes title, subtitle, full description (Markdown)
- Contact email included

**2. Executed Seed Script 執行種子腳本:**
```bash
mysql -u root studio < seed_about.sql
```

**3. Verified Fix 驗證修復:**
```bash
curl http://localhost:8000/api/about
# ✅ Returns complete data
```

**Content Added:**
```
Title: AI-Tracks Studio
Subtitle: Innovative Web & Game Experiences Powered by AI
Description: Full Markdown content with:
  - Who We Are
  - Our Mission
  - What We Do
  - Our Approach
  - Get In Touch
Email: contact@ai-tracks.studio
```

**Files Created:**
- `backend/seed_about.sql` - SQL seed script
- `backend/ABOUT_US_SETUP.md` - Documentation

**Now Working:**
- ✅ Visit: http://localhost:3000/about
- ✅ API returns data
- ✅ Frontend displays content
- ✅ No more "not found" error

## 2025-12-04 12:15:00 TST

### Frontend: Clean URLs (Browser Router) 前端：清晰的 URL

#### Changed Routing 更改路由

**From Hash Router to Browser Router:**
- ✅ Changed `HashRouter` to `BrowserRouter` in `App.tsx`
- No more `#` in URLs!

**URL Changes:**
```
Before 之前:  /#/game  /#/website  /#/news
After  之後:  /game    /website    /news
```

**Benefits:**
- ✅ Cleaner, more professional URLs
- ✅ Better user experience
- ✅ Easier to share links
- ✅ Modern web standard
- ✅ Better for SEO (if needed)

**Examples:**
```
Old: http://localhost:3000/#/game/game-123
New: http://localhost:3000/game/game-123

Old: http://localhost:3000/#/news
New: http://localhost:3000/news
```

**Development:**
- Vite automatically handles History API fallback
- All routes work on direct access
- Page refresh works correctly
- No additional configuration needed

**Files Changed:**
- `frontend/App.tsx` - Changed import from `HashRouter` to `BrowserRouter`
- `frontend/ROUTING_CHANGE.md` - Documentation

## 2025-12-04 12:00:00 TST

### Frontend: Project Detail Page 前端：專案詳細頁面

#### Added Features 新增功能

**1. Project Detail Component 專案詳細組件:**
- ✅ Created `frontend/components/ProjectDetail.tsx`
- Full-screen hero image with gradient overlay
- Project title and category badge
- Detailed description section
- Metadata sidebar (date, tags, external link)
- Back navigation to list page
- Loading and error states
- Responsive design

**2. Clickable Project Cards 可點擊的專案卡片:**
- ✅ Updated `frontend/components/ItemGrid.tsx`
- Wrapped cards in `<Link>` components
- Dynamic routing: `/game/:id` or `/website/:id`
- Hover shows "View Details" button
- Smooth transitions

**3. New Routes 新路由:**
- ✅ `/game/:id` → Project detail (games)
- ✅ `/website/:id` → Project detail (websites)

**4. Fixed Image Display 修復圖片顯示:**
- ✅ Updated `frontend/types.ts` - Changed `thumbnail_url` to `image`, `image_url` to `image`
- ✅ Added `getImageUrl()` helper in `frontend/api/config.ts`
- ✅ Updated all components to use `getImageUrl(item.image)`
- Images now construct full URL from filename

#### User Flow 用戶流程

```
Games Page → Click Card → /#/game/game-123 → Detail Page → Back to Games
Websites Page → Click Card → /#/website/website-456 → Detail Page → Back to Websites
Home → Featured Game → Click → Games List → Click Card → Detail Page
```

#### Files Changed 更改的文件

**New Files 新文件:**
- `frontend/components/ProjectDetail.tsx` - Detail page component
- `frontend/PROJECT_DETAIL_PAGE.md` - Documentation
- `frontend/IMAGE_URL_FIX.md` - Image URL fix documentation

**Updated Files 更新的文件:**
- `frontend/App.tsx` - Added detail routes, imported `ProjectDetail`, added `getImageUrl`
- `frontend/components/ItemGrid.tsx` - Made cards clickable with `Link`
- `frontend/types.ts` - Changed image field names
- `frontend/api/config.ts` - Added `getImageUrl()` helper

#### Benefits 優點

- ✅ Users can view full project details
- ✅ Better UX with dedicated detail pages
- ✅ Clean, semantic URLs
- ✅ Images display correctly from backend
- ✅ Responsive on all devices
- ✅ Easy to navigate back to list

## 2025-12-04 11:45:00 TST

### Unified Add-Edit Form 統一新增編輯表單

#### Implementation 實作方式
**Created unified `add-edit.html` for all modules:**
- ✅ `projects/add-edit.html` (renamed from `add.html`)
- ✅ `news/add-edit.html` (renamed from `add.html`)
- ✅ `about/add-edit.html` (renamed from `add.html`)

**Routing Logic in `admin.html`:**
```javascript
// Map add and edit actions to add-edit.html (single form handles both)
let actualAction = action;
if (action === 'add' || action === 'edit') {
    actualAction = 'add-edit';
}
```

**URL Patterns:**
- `#projects/add` → Loads `add-edit.html` in create mode
- `#projects/edit/game-123` → Loads `add-edit.html` in edit mode
- Same for News and About

**Form Behavior:**
- Detects edit mode by checking for `/edit/ID` in URL
- Automatically loads existing data when in edit mode
- Shows correct title: "新增專案" or "編輯專案"
- Single source of truth for form logic

**Benefits:**
- ✅ Clean, semantic URLs
- ✅ Single file to maintain per module
- ✅ Consistent behavior across all modules
- ✅ Easy to understand and modify
- ✅ No duplicate code

## 2025-12-04 11:30:00 TST

### Fixed Edit URL Routing 修復編輯頁面路由 (DEPRECATED)

#### Problem 問題
- When clicking "Edit" button, URL showed `#projects/add/ID` instead of `#projects/edit/ID`
- This was confusing because "add" URL with ID looked wrong
- News and About had the same issue
- Old URLs with `/add/ID` format didn't work as edit mode

#### Root Cause 根本原因
- `edit.html` files were redirecting from `#module/edit/ID` to `#module/add/ID`
- This was done because `add.html` handles both add and edit modes
- But the URL looked incorrect to users
- `add.html` only checked for `/edit/ID` pattern, not `/add/ID`

#### Solution 解決方案
**1. Improved routing logic in `admin.html`:**
```javascript
// Map edit action to add.html (single form handles both add and edit)
let actualAction = action;
if (action === 'edit' && id) {
    actualAction = 'add'; // Use add.html for both add and edit
}
```

**2. Enhanced pattern matching in all `add.html` files:**
```javascript
// Support both /edit/ID and /add/ID for backward compatibility
const match = hash.match(/#projects\/(edit|add)\/(.+)/);
if (match && match[2]) {
    isEditMode = true;
    editingId = match[2];
    
    // Auto-redirect old /add/ID URLs to /edit/ID format
    if (match[1] === 'add') {
        window.location.hash = `projects/edit/${editingId}`;
        return;
    }
}
```

**3. Removed redirect files:**
- ❌ Deleted `projects/edit.html`
- ❌ Deleted `news/edit.html`
- ❌ Deleted `about/edit.html`

**Now routing works correctly:**
- ✅ `#projects/edit/game-123` → Loads `add.html` in edit mode
- ✅ `#projects/add` → Loads `add.html` in create mode
- ✅ `#projects/add/game-123` → Auto-redirects to `#projects/edit/game-123`
- ✅ URL stays clean as `#projects/edit/ID`
- ✅ Page title correctly shows "編輯專案" (Edit Project)
- ✅ Same for News and About

**Benefits:**
- ✅ Clean URLs that make sense
- ✅ No confusing redirects
- ✅ Backward compatible with old URLs
- ✅ Single source of truth (add.html handles both modes)
- ✅ Better user experience
- ✅ Correct page titles for edit mode

## 2025-12-04 09:15:00 TST

### Database LONGTEXT & Chinese Labels 資料庫 LONGTEXT 與中文標籤

#### Database Schema Update 資料庫結構更新
**Changed to LONGTEXT for Markdown content:**

**Projects Model:**
- ✅ `description` - TEXT → LONGTEXT

**News Model:**
- ✅ `excerpt` - TEXT → LONGTEXT
- ✅ `content` - TEXT → LONGTEXT

**About Model:**
- ✅ `subtitle` - TEXT → LONGTEXT
- ✅ `description` - TEXT → LONGTEXT

**Benefits:**
- Supports up to 4GB of text (vs 64KB for TEXT)
- Perfect for Markdown content with images/formatting
- No truncation issues
- Better for long-form content

#### Chinese Labels 中文標籤統一
**Standardized terminology across all pages:**

**Navigation & Titles:**
- Projects 管理 → **專案管理**
- News 管理 → **最新消息**
- About 管理 → **關於我們**

**Updated in:**
- ✅ Sidebar navigation (admin.html)
- ✅ Page titles (JavaScript titles object)
- ✅ Form titles (add.html)
- ✅ Button labels (list.html)
- ✅ Confirmation messages (delete dialogs)

**Consistency:**
- All pages use same terminology
- Professional Chinese labels
- Clear and concise
- User-friendly

#### Full-Width Form Fields 全寬表單欄位
**Changed from 2-column to single-column layout:**
- ✅ Projects: All fields `col-12` (was `col-12 col-lg-6`)
- ✅ News: All fields `col-12`
- ✅ About: Already `col-12`

**Benefits:**
- Clearer reading flow
- Better for long text fields
- Consistent on all screen sizes
- More professional appearance

---

## 2025-12-04 08:45:00 TST

### Final RWD & User Dropdown 最終 RWD 與用戶下拉選單

#### True RWD Implementation 真正的 RWD 實現
**Responsive Sidebar 響應式側邊欄:**
- ✅ Desktop (≥ 992px) - 固定在左側
- ✅ Mobile/Tablet (< 992px) - 隱藏，改用漢堡選單
- ✅ Hamburger Menu - 左上角漢堡按鈕（手機）
- ✅ Overlay - 半透明遮罩（點擊關閉）
- ✅ Slide Animation - 流暢的滑入/滑出動畫

**True Flexbox Layout 真正的 Flexbox 佈局:**
```html
<div class="d-flex justify-content-between flex-wrap gap-3">
    <div class="d-flex flex-wrap gap-3 flex-grow-1">
        <input style="flex: 1 1 auto; max-width: 300px;">
        <select style="width: auto;">
    </div>
    <button>新增</button>
</div>
```

**效果：**
- 寬螢幕：元素自然分散，按鈕自動推到最右
- 窄螢幕：元素自動換行，保持可用性
- 手機：垂直堆疊，按鈕全寬

#### User Dropdown 用戶下拉選單
**Header 改進:**
- ✅ 移除獨立的登出按鈕
- ✅ 用戶圖標 (fa-user-circle) + Email
- ✅ Bootstrap Dropdown 下拉選單
- ✅ 下拉內容：
  - 登入身分顯示
  - 分隔線
  - 登出選項（紅色文字 + 圖標）
- ✅ RWD: 手機上只顯示圖標，平板以上顯示 Email

**Dropdown Features:**
- Shadow 陰影效果
- 右對齊 (dropdown-menu-end)
- 懸停效果
- 觸控友好

#### Cleaned File Structure 清理檔案結構
**移除所有舊版/中間版 HTML:**
- ❌ Removed 10+ old HTML files
- ✅ Keep only: 1 base + 9 fragments
- ✅ Clean structure

**Final Structure:**
```
static/
├── admin.html (BASE - 唯一完整 HTML)
├── login.html
├── css/admin-bootstrap.css
├── js/
│   ├── admin.js
│   └── template-loader.js
└── admin/
    ├── projects/ (list.html, add.html, edit.html)
    ├── news/ (list.html, add.html, edit.html)
    └── about/ (list.html, add.html, edit.html)
```

#### Mobile-First RWD 手機優先 RWD
**Breakpoints:**
- < 576px (xs) - 手機小屏
- < 768px (sm) - 手機
- < 992px (md) - 平板
- ≥ 992px (lg) - 桌面
- ≥ 1200px (xl) - 大桌面

**Responsive Features:**
- ✅ Collapsible sidebar on mobile
- ✅ Hamburger menu button
- ✅ Touch-friendly overlay
- ✅ Flexible filter bar
- ✅ Auto-wrapping elements
- ✅ Proper font sizes
- ✅ Adequate touch targets (44x44px+)

---

## 2025-12-03 23:03:00 TST

### Bootstrap 5 + jQuery Integration Bootstrap 5 + jQuery 整合

#### Framework Integration 框架整合
**Added Frontend Frameworks:**
- **Bootstrap 5.3.2** - Modern responsive UI framework
- **jQuery 3.7.1** - Simplified DOM manipulation
- **Font Awesome 6.5.1** - Professional icon library (already integrated)

#### Base Template System 基礎模板系統
**Created Template Infrastructure:**
- `static/base.html` - Base template reference
- `static/js/common-ui.js` - Shared UI components with jQuery
- `static/css/admin-bootstrap.css` - Bootstrap 5 custom styles

**Shared Components 共用組件:**
- `loadSidebar()` - Auto-load navigation sidebar
- `loadHeader()` - Auto-load page header with user info
- `setPageTitle(title)` - Set page title dynamically

#### UI Components UI 組件
**Bootstrap 5 Components:**
- ✅ Responsive tables with hover effects
- ✅ Modern buttons (primary, secondary, outline)
- ✅ Dropdown menus for filters
- ✅ Toast notifications (success/error)
- ✅ Modal dialogs for confirmations
- ✅ Spinners for loading states
- ✅ Alerts for messages
- ✅ Badges for categories/status

**jQuery Utilities:**
- ✅ `$()` selectors for easy DOM access
- ✅ `.click()`, `.on()` event handling
- ✅ `.ajax()` for API requests
- ✅ `.html()`, `.val()` for content manipulation

#### Full-Width Filter Bar 全寬篩選欄
**New Design (matching reference image):**
- 搜尋輸入框（flex-grow）
- 類別下拉選單（Bootstrap dropdown）
- 每頁筆數下拉選單
- 新增按鈕（ms-auto 推到右側）
- 使用 `d-flex` 實現響應式佈局

#### Example Pages 示範頁面
**Created:**
- `admin/projects/index-bootstrap.html` - Complete Bootstrap 5 example
  - Full-width filter bar
  - Dropdown menus
  - Responsive table
  - Toast notifications
  - Delete confirmation modal

**Features:**
- jQuery event handling
- Bootstrap dropdown integration
- Dynamic content rendering
- Shared sidebar/header loading

#### Form Improvements 表單改進
**Full-Width Forms:**
- ✅ All forms now use `width: 100%` instead of `max-width: 800px`
- ✅ Better space utilization
- ✅ Larger input areas
- ✅ More comfortable editing experience

**Auto-Generated IDs:**
- Projects: Removed manual ID input (auto-gen: `{category}-{timestamp}`)
- News: Removed manual ID input (auto-gen: `news-{timestamp}`)

#### Documentation 文檔
**Created:**
- `backend/BOOTSTRAP_GUIDE.md` - Complete Bootstrap 5 + jQuery guide
  - Component usage examples
  - jQuery common operations
  - Template structure
  - Best practices

---

## 2025-12-03 22:57:03 TST

### Image Upload with WebP Conversion 圖片上傳與 WebP 轉換

#### New Dependency 新增依賴
- **Pillow 12.0.0** - Python imaging library for image processing

#### Image Upload API 圖片上傳 API
**Created `app/routers/admin/upload.py`:**
- `POST /api/admin/upload/image` - Upload image and convert to WebP
- `DELETE /api/admin/upload/image` - Delete uploaded image

**Features 功能：**
- ✅ Accepts: JPEG, PNG, GIF, WebP
- ✅ Auto-convert to WebP format
- ✅ Quality: 85% (optimal balance)
- ✅ Compression method: 6 (best)
- ✅ Transparency handling (convert to white background)
- ✅ File size limit: 10MB
- ✅ Unique filename: `{timestamp}.webp`
- ✅ Saved to: `backend/app/static/uploads/`

#### UI Improvements UI 改進
**Projects add-edit:**
- ✅ Image upload button next to URL input
- ✅ Live preview after upload
- ✅ Auto-fill URL after successful upload
- ✅ Upload progress indicator
- ✅ File size and format info display

**News add-edit:**
- ✅ Image upload functionality
- ✅ Preview support
- ✅ WebP conversion

**Common Features:**
- ✅ Drag-and-drop support (via file input)
- ✅ Image preview with max-width/height
- ✅ Success/error messages
- ✅ File info display (name, size, format)

#### ID Auto-Generation ID 自動生成
**Removed manual ID input:**
- ✅ Projects - Auto-generate: `{category}-{timestamp}`
  - Example: `game-123456`, `website-789012`
- ✅ News - Auto-generate: `news-{timestamp}`
  - Example: `news-12345678`

**Benefits:**
- ✅ Simpler user experience
- ✅ Guaranteed unique IDs
- ✅ No ID conflicts
- ✅ Faster data entry

#### Upload Workflow 上傳流程
1. User clicks "📤 上傳圖片" button
2. Selects image file (JPEG/PNG/GIF)
3. File uploads to `/api/admin/upload/image`
4. Server converts to WebP (Pillow)
5. Saves to `/static/uploads/{timestamp}.webp`
6. Returns URL: `/static/uploads/{filename}.webp`
7. Auto-fills URL input field
8. Shows preview image
9. Displays file info (size, format)

#### WebP Conversion Details 轉換細節
**Quality Settings:**
- Quality: 85% (balanced)
- Method: 6 (best compression)
- Optimize: true

**Transparency Handling:**
- RGBA/LA/P modes → Convert to RGB with white background
- Other modes → Convert to RGB
- Ensures compatibility

**File Naming:**
- Format: `YYYYMMDD_HHMMSS_microseconds.webp`
- Example: `20251203_225703_123456.webp`
- Guaranteed uniqueness

#### Storage Structure 儲存結構
```
backend/app/static/
├── uploads/              # Uploaded images (NEW)
│   ├── 20251203_*.webp
│   └── ...
├── css/
├── js/
└── admin/
```

**Public Access:**
- Images accessible at: `http://localhost:8000/static/uploads/{filename}.webp`
- No authentication required for viewing
- Suitable for frontend display

#### Testing 測試
**Via UI:**
1. 訪問 `/backend/projects/add`
2. 點擊「上傳圖片」
3. 選擇 JPG/PNG 圖片
4. 查看自動轉換為 WebP
5. 預覽圖片
6. 儲存表單

**Via API:**
```bash
curl -X POST http://localhost:8000/api/admin/upload/image \
  -F "file=@test.jpg" \
  --cookie cookies.txt
```

#### Benefits 優勢
✅ **省空間** - WebP 比 JPEG/PNG 小 30-80%  
✅ **更快載入** - 減少頻寬使用  
✅ **自動化** - 無需手動轉換  
✅ **透明支持** - PNG 透明背景轉白色  
✅ **唯一命名** - 時間戳避免衝突  

---

## 2025-12-03 22:50:46 TST

### Refactored to Repository Pattern & Improved UI 重構為 Repository 模式並改進 UI

#### Repository Pattern 倉儲模式
**重構 Admin API 使用 Repository：**
- ✅ `admin/projects_admin.py` - 使用 `ProjectRepository`
- ✅ `admin/news_admin.py` - 使用 `NewsRepository`
- ✅ `admin/about_admin.py` - 使用 `AboutUsRepository`

**優點：**
- ✅ Clean Architecture - 分離關注點
- ✅ DRY Principle - 消除重複代碼
- ✅ 易於測試 - Repository 可獨立測試
- ✅ 一致性 - Public 和 Admin API 使用相同 Repository

#### UI Improvements UI 改進
參考 shopping-react-flask 精確設計：

**側邊欄選單改進：**
- ✅ 分組結構 - "內容管理" 群組
- ✅ 可展開/摺疊 - 支持多層選單
- ✅ 圖標對齊 - 統一的 icon 樣式
- ✅ 高亮效果 - 當前頁面左側藍色邊條
- ✅ 深藍色背景 (#1e3a5f) - 專業風格

**按鈕樣式改進：**
- ✅ 編輯按鈕 - 藍色文字連結樣式
- ✅ 刪除按鈕 - 紅色文字，hover 時淺紅背景
- ✅ 新增按鈕 - 藍色實心按鈕 (#4299e1)
- ✅ 更簡潔的設計 - 符合現代 UI 標準

**標籤 (Tags) 樣式：**
- ✅ GAME - 淺綠色背景
- ✅ WEBSITE - 淺藍色背景
- ✅ ADMIN - 淺紅色背景
- ✅ USER - 淺粉色背景
- ✅ ACTIVE - 綠色背景
- ✅ INACTIVE - 紅色背景

**CSS 更新：**
- 更新 `static/css/admin.css` 匹配 shopping-react-flask 風格
- 側邊欄分組樣式
- 按鈕 hover 效果
- 表格樣式細節

---

## 2025-12-03 22:16:00 TST

### Admin UI - HTML Management Interface 後台管理界面

參考 shopping-react-flask 風格，創建完整的 HTML 後台管理界面。

#### Static Files 靜態文件
**Login Page 登入頁面:**
- `backend/app/static/login.html` - 精美的登入界面
  - 紫色漸層背景
  - 動畫效果
  - 表單驗證
  - 錯誤提示
  - 預填測試帳號

**Admin Styles 管理樣式:**
- `backend/app/static/css/admin.css` - 統一的管理界面樣式
  - 側邊欄導航
  - 表格樣式
  - 按鈕樣式
  - 表單樣式
  - Loading 動畫

**Admin JavaScript 管理腳本:**
- `backend/app/static/js/admin.js` - 通用功能
  - 認證檢查 (`checkAuth`)
  - API 請求封裝 (`apiRequest`)
  - 登出功能 (`logout`)
  - 日期格式化
  - Loading/Error 顯示

#### Management Pages 管理頁面
**Projects Management 專案管理:**
- `backend/app/static/admin/projects/index.html`
  - 列表顯示（表格）
  - 分類篩選（GAME/WEBSITE）
  - 新增/編輯/刪除功能
  - Modal 彈窗表單
  - 即時更新

**News Management 新聞管理:**
- `backend/app/static/admin/news/index.html`
  - 新聞列表
  - 完整的 CRUD 操作
  - 作者、日期顯示
  - 內容編輯

**About Management 關於我們管理:**
- `backend/app/static/admin/about/index.html`
  - About 內容管理
  - JSON 格式 values 編輯
  - 聯絡 Email 設定

#### Backend Routes 後台路由
Updated `backend/app/main.py`:
- `GET /backend` → 登入頁面
- `GET /backend/login` → 登入頁面
- `GET /backend/projects` → Projects 管理
- `GET /backend/news` → News 管理
- `GET /backend/about` → About 管理

#### Static Files Mounting 靜態文件掛載
```python
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
```

#### Features 功能特點
✅ **美觀的界面** - 漸層背景、圓角設計  
✅ **側邊欄導航** - 快速切換頁面  
✅ **即時驗證** - Session 自動檢查  
✅ **Modal 彈窗** - 新增/編輯表單  
✅ **錯誤處理** - 友好的錯誤提示  
✅ **Loading 狀態** - 載入動畫  
✅ **響應式設計** - 支持各種螢幕尺寸  

#### Usage 使用方式
1. 啟動後端：`cd backend && uv run python run.py`
2. 訪問後台：http://localhost:8000/backend
3. 登入帳號：
   - Email: `admin@admin.com`
   - Password: `admin123`
4. 管理內容：Projects、News、About

#### Admin Pages 管理頁面
- http://localhost:8000/backend - 登入頁面
- http://localhost:8000/backend/projects - Projects 管理
- http://localhost:8000/backend/news - News 管理
- http://localhost:8000/backend/about - About 管理

---

## 2025-12-03 22:01:56 TST

### Complete Admin Backend System 完整後台管理系統

參考 shopping-react-flask 項目，實現完整的後台管理系統。

#### New Dependencies 新增依賴
- `python-jose[cryptography]` - JWT token handling  
- `passlib` + `bcrypt` - Password hashing
- `python-multipart` - Form data handling
- `itsdangerous` - Session management

#### User Model & Authentication 用戶模型與認證
**Created `app/models/user.py`:**
- User model with roles (ADMIN, USER)
- User status (ACTIVE, INACTIVE, SUSPENDED)
- Password hash storage
- Email unique constraint

**Created `app/core/security.py`:**
- Password hashing with bcrypt
- JWT token creation/decoding
- Secure authentication utilities

#### Admin APIs 管理 API
**Authentication APIs** (`app/routers/admin/`):
- `POST /api/admin/login` - Admin login with session
- `POST /api/admin/logout` - Clear session
- `GET /api/admin/me` - Get current admin info

**Projects Management APIs:**
- `GET /api/admin/projects` - List all projects (admin only)
- `GET /api/admin/projects/{id}` - Get project details
- `POST /api/admin/projects` - Create new project
- `PUT /api/admin/projects/{id}` - Update project
- `DELETE /api/admin/projects/{id}` - Delete project

**News Management APIs:**
- `GET /api/admin/news` - List all news
- `POST /api/admin/news` - Create news article
- `PUT /api/admin/news/{id}` - Update news
- `DELETE /api/admin/news/{id}` - Delete news

**About Us Management APIs:**
- `GET /api/admin/about` - List about entries
- `POST /api/admin/about` - Create about entry
- `PUT /api/admin/about/{id}` - Update about
- `DELETE /api/admin/about/{id}` - Delete about

#### Dependencies & Security 依賴與安全
**Created `app/dependencies.py`:**
- `get_db()` - Database session dependency
- `get_current_user_from_session()` - Get user from session
- `require_admin()` - Admin authentication guard

**Session Management:**
- Session-based authentication (24 hour expiry)
- Secure cookie handling
- CSRF protection with same_site=lax

#### Admin Initialization 管理員初始化
**Created `app/init_admin.py`:**
- Auto-create admin user on startup
- Default credentials:
  - Email: `admin@admin.com`
  - Password: `admin123` ⚠️ (change in production!)
- Updates existing users to admin if needed

#### Configuration Updates 配置更新
**Updated `app/config.py`:**
- Added `SECRET_KEY` for JWT signing
- Added `SESSION_SECRET_KEY` for session encryption  
- Added `ALGORITHM` (HS256) for JWT
- Added `ACCESS_TOKEN_EXPIRE_MINUTES` (30)
- Added `FRONTEND_URL` and `BACKEND_URL`

#### Files Created 創建的文件
**Models:**
- `backend/app/models/user.py` - User model with roles

**Core:**
- `backend/app/core/security.py` - Security utilities
- `backend/app/core/__init__.py` - Core exports

**Admin APIs:**
- `backend/app/routers/admin/__init__.py` - Admin router
- `backend/app/routers/admin/login.py` - Login API
- `backend/app/routers/admin/logout.py` - Logout API
- `backend/app/routers/admin/me.py` - Current user API
- `backend/app/routers/admin/projects_admin.py` - Projects CRUD
- `backend/app/routers/admin/news_admin.py` - News CRUD
- `backend/app/routers/admin/about_admin.py` - About CRUD

**Dependencies:**
- `backend/app/dependencies.py` - FastAPI dependencies

**Initialization:**
- `backend/app/init_admin.py` - Admin user setup

**Documentation:**
- `backend/ADMIN_SYSTEM.md` - Complete admin system guide

#### Next Steps 下一步
**To complete the admin system:**
1. Update `backend/app/main.py`:
   - Add `SessionMiddleware`
   - Import and include `admin_router`
   - Call `init_admin_user()` on startup
   - (Optional) Add `/backend` routes for admin UI

2. Create admin frontend:
   - Login page at `/backend`
   - Admin dashboard
   - CRUD interfaces for Projects, News, About

#### Security Notes 安全提示
⚠️ **IMPORTANT - Change in Production:**
- `SECRET_KEY` - JWT signing key
- `SESSION_SECRET_KEY` - Session encryption key
- Admin password (currently: admin123)

Set via `.env` file:
```env
SECRET_KEY=your-super-secret-key-here
SESSION_SECRET_KEY=your-session-key-here
```

#### Features Implemented 實現功能
✅ **User Authentication** - Secure session-based auth  
✅ **Role-Based Access** - Admin-only endpoints  
✅ **Password Security** - Bcrypt hashing  
✅ **JWT Tokens** - Token generation/validation  
✅ **Auto Admin Init** - Default admin creation  
✅ **Complete CRUD** - All content management  
✅ **Type Safety** - Full Pydantic validation  
✅ **Clean Architecture** - Separated concerns  

---

## 2025-12-03 21:43:58 TST

### Frontend API Integration 前端 API 整合

#### Connected Frontend to Backend API 連接前端到後端 API

Successfully integrated the React frontend with the FastAPI backend, replacing all hardcoded data with real API calls.

#### New API Layer 新增 API 層
Created comprehensive API client layer:
- **`frontend/api/config.ts`** - API configuration and base URL management
- **`frontend/api/client.ts`** - HTTP client with error handling and timeouts
- **`frontend/api/projects.ts`** - Projects/Games API service
- **`frontend/api/news.ts`** - News API service
- **`frontend/api/about.ts`** - About Us API service
- **`frontend/api/index.ts`** - Central export point

#### Updated Types 更新類型
- Updated `frontend/types.ts` with API response types
- Added `ProjectListResponse`, `NewsListResponse`
- Added `AboutUs` and `AboutValue` interfaces
- Added `LoadingState` interface
- Matched backend schema (snake_case: `thumbnail_url`, `image_url`)

#### Route Changes 路由變更
Updated routing structure as requested:
- `/games` → `/game` (displays games from API: `category=GAME`)
- `/websites` → `/website` (displays websites from API: `category=WEBSITE`)
- `/news` → `/news` (fetches from news API)
- `/about` → `/about` (fetches from about API)
- `/` → Home (displays featured games)

#### Component Updates 組件更新
**`frontend/App.tsx`** - Complete rewrite:
- Removed hardcoded data (GAMES, WEBSITES, NEWS constants)
- Added data fetching with `useEffect` hooks
- Created separate page components: `GamesPage`, `WebsitesPage`, `NewsPage`, `AboutPage`
- Added `LoadingSpinner` component
- Added `ErrorMessage` component with retry functionality
- Implemented proper error handling for all API calls

**`frontend/components/Layout.tsx`**:
- Updated navigation links to use new routes
- Desktop menu: `/game`, `/website` instead of `/games`, `/websites`
- Mobile menu: Updated all route references
- Footer: Updated quick links

**`frontend/components/ItemGrid.tsx`**:
- Updated to use `thumbnail_url` instead of `thumbnailUrl`
- Matches backend API response format

**`frontend/constants.ts`**:
- Removed hardcoded GAMES, WEBSITES, NEWS arrays
- Kept HERO_IMAGES for hero sections

#### Features Implemented 實現功能
✅ **Dynamic Data Loading** - All content from backend API  
✅ **Loading States** - Spinner during data fetch  
✅ **Error Handling** - User-friendly error messages  
✅ **Retry Functionality** - Try again on failed requests  
✅ **Empty States** - Handled when no data available  
✅ **Type Safety** - Full TypeScript throughout  
✅ **Clean Architecture** - Separated API layer from components  

#### API Configuration API 配置
- Base URL: `http://localhost:8000` (development)
- Configurable via `VITE_API_BASE_URL` environment variable
- 30-second timeout for requests
- Proper error handling for network issues

#### Data Flow 數據流
1. Component mounts → `useEffect` triggered
2. Display loading spinner
3. API call via service layer
4. On success: Display data
5. On error: Show error message with retry option

---

## 2025-12-03 21:31:51 TST

### Added Gunicorn for Production Deployment

#### New Dependency 新增依賴
- **Gunicorn 23.0.0** - Python WSGI HTTP Server for production

#### Production Server Setup 生產環境設定
- Added Gunicorn with Uvicorn workers configuration
- Created `run_production.py` with optimal production settings
- Updated documentation with production deployment instructions

#### Running Commands 執行命令
**Development 開發環境:**
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production 生產環境:**
```bash
uv run gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## 2025-12-03 21:17:04 TST

### Created FastAPI Backend with Clean Architecture

**Update:** Changed to Python 3.14 (standard version, non-freethreaded) for better compatibility.

#### Project Structure 專案結構
- Created `backend/` directory with clean architecture
- Initialized UV project with Python 3.12
- Organized code into layers: models, schemas, repositories, routers

#### Dependencies 依賴套件
- **Python**: 3.14.0 (standard version, non-freethreaded)
- FastAPI >= 0.109.0 - Modern web framework
- Uvicorn >= 0.27.0 - ASGI server (development)
- Gunicorn >= 23.0.0 - WSGI server (production)
- SQLAlchemy >= 2.0.25 - ORM for database
- PyMySQL >= 1.1.0 - MySQL connector
- Pydantic >= 2.5.3 - Data validation
- Pydantic-settings >= 2.1.0 - Configuration management

#### Database Models 資料庫模型
Created three main models:
1. **Project** (`projects` table)
   - Fields: id, title, description, thumbnail_url, category (GAME/WEBSITE), date, tags, link
   - Supports both games and websites
   
2. **News** (`news` table)
   - Fields: id, title, excerpt, content, date, image_url, author
   - For blog posts and announcements
   
3. **AboutUs** (`about_us` table)
   - Fields: id, title, subtitle, description, values (JSON), contact_email
   - Dynamic content management for About page

#### API Endpoints API 端點
Implemented full CRUD operations for all resources:

**Projects 專案:**
- `GET /api/projects` - List with optional category filter
- `GET /api/projects/{id}` - Get single project
- `POST /api/projects` - Create new project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

**News 新聞:**
- `GET /api/news` - List all news
- `GET /api/news/{id}` - Get single article
- `POST /api/news` - Create article
- `PUT /api/news/{id}` - Update article
- `DELETE /api/news/{id}` - Delete article

**About Us 關於我們:**
- `GET /api/about` - Get current content
- `GET /api/about/{id}` - Get by ID
- `POST /api/about` - Create content
- `PUT /api/about/{id}` - Update content
- `DELETE /api/about/{id}` - Delete content

#### Clean Code Architecture 乾淨架構
Implemented clean code principles:
- **Repository Pattern**: Abstracted data access layer
- **Dependency Injection**: Using FastAPI's dependency system
- **Separation of Concerns**: Models, Schemas, Repositories, Routers
- **Type Safety**: Full type hints throughout
- **Error Handling**: Proper HTTP exceptions
- **Validation**: Pydantic schemas for request/response

#### Configuration 設定
- Database: MySQL (root user, no password, studio database)
- CORS: Enabled for frontend (localhost:5173, localhost:3000)
- API Prefix: `/api`
- Auto-create tables on startup

#### Files Created 建立的檔案

**Core Application:**
- `backend/app/main.py` - FastAPI application entry point
- `backend/app/config.py` - Configuration settings
- `backend/app/database.py` - Database connection

**Models (SQLAlchemy ORM):**
- `backend/app/models/project.py` - Project model (games/websites)
- `backend/app/models/news.py` - News model
- `backend/app/models/about.py` - About Us model

**Schemas (Pydantic Validation):**
- `backend/app/schemas/project.py` - Project validation schemas
- `backend/app/schemas/news.py` - News validation schemas
- `backend/app/schemas/about.py` - About Us validation schemas

**Repositories (Data Access Layer):**
- `backend/app/repositories/base.py` - Base repository with CRUD operations
- `backend/app/repositories/project.py` - Project repository
- `backend/app/repositories/news.py` - News repository
- `backend/app/repositories/about.py` - About Us repository

**Routers (API Endpoints):**
- `backend/app/routers/projects.py` - Projects CRUD endpoints
- `backend/app/routers/news.py` - News CRUD endpoints
- `backend/app/routers/about.py` - About Us CRUD endpoints

**Configuration & Documentation:**
- `backend/pyproject.toml` - UV project configuration
- `backend/run.py` - Quick start script
- `backend/README.md` - Project overview
- `backend/API_DOCUMENTATION.md` - Complete API reference
- `backend/GETTING_STARTED.md` - Setup and usage guide
- `backend/.gitignore` - Git ignore file

#### Running the Server 啟動伺服器
```bash
cd backend
uv run python run.py
```

Or alternatively:
```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Notes 備註
- Database tables will be created automatically on first run
- Make sure MySQL is running with `studio` database created
- All code follows clean code and SOLID principles
- Type hints and docstrings throughout for better maintainability
- Fixed type annotations to use modern Python 3.12 syntax (str | None instead of Optional[str])
- Resolved date type name collision in Pydantic schemas
- Verified all imports load successfully

---

## 2025-12-07 08:11:39 - Detail 頁面 Top Navigator 顏色配置統一

### 變更內容 / Changes

統一 detail 頁面的 top navigator 顏色配置，使其與首頁一致。

Unified the top navigator color configuration for detail pages to match the homepage.

### 修改的檔案 / Modified Files

1. **frontend/components/ProjectDetail.tsx**
   - 將 header 的背景色從 `bg-white border-b border-slate-200` 改為 `bg-purple-100/90 backdrop-blur-sm border-b border-purple-200/30`
   - Changed header background from `bg-white border-b border-slate-200` to `bg-purple-100/90 backdrop-blur-sm border-b border-purple-200/30`

2. **frontend/components/NewsDetail.tsx**
   - 將 header 的背景色從 `bg-white border-b border-slate-200` 改為 `bg-purple-100/90 backdrop-blur-sm border-b border-purple-200/30`
   - Changed header background from `bg-white border-b border-slate-200` to `bg-purple-100/90 backdrop-blur-sm border-b border-purple-200/30`

### 效果 / Effects

- Detail 頁面的 top navigator 現在使用與首頁相同的 purple-100 顏色配置
- Detail pages' top navigator now uses the same purple-100 color configuration as the homepage
- 保持一致的視覺風格和用戶體驗
- Maintains consistent visual style and user experience

---

## 2025-12-07 08:13:04 - Detail 頁面根據類型設置不同顏色

### 變更內容 / Changes

根據 detail 頁面的類型（GAME、WEBSITE、NEWS）設置不同的 top navigator 顏色配置，讓用戶可以通過顏色快速識別頁面類型。

Set different top navigator color configurations based on detail page type (GAME, WEBSITE, NEWS) to help users quickly identify page types through color.

### 顏色配置 / Color Configuration

1. **GAME (遊戲)**: 藍色系
   - Background: `bg-blue-100/90`
   - Border: `border-blue-200/30`
   - 使用藍色系突出遊戲頁面
   - Uses blue color scheme to highlight game pages

2. **WEBSITE (網站)**: 綠色系
   - Background: `bg-emerald-100/90`
   - Border: `border-emerald-200/30`
   - 使用綠色系突出網站頁面
   - Uses green color scheme to highlight website pages

3. **NEWS (新聞)**: 橙色系
   - Background: `bg-orange-100/90`
   - Border: `border-orange-200/30`
   - 使用橙色系突出新聞頁面
   - Uses orange color scheme to highlight news pages

### 修改的檔案 / Modified Files

1. **frontend/components/ProjectDetail.tsx**
   - 添加 `getHeaderColor()` 函數，根據 project.category 返回對應的顏色配置
   - Added `getHeaderColor()` function that returns color configuration based on project.category
   - GAME 類型使用藍色，WEBSITE 類型使用綠色
   - GAME type uses blue, WEBSITE type uses green

2. **frontend/components/NewsDetail.tsx**
   - 將 header 顏色從 purple-100 改為 orange-100
   - Changed header color from purple-100 to orange-100
   - 使用橙色系突出新聞頁面
   - Uses orange color scheme to highlight news pages

### 效果 / Effects

- 不同類型的 detail 頁面現在有獨特的顏色標識
- Different types of detail pages now have unique color identifiers
- 提升用戶體驗，讓用戶可以快速識別當前頁面類型
- Improves user experience by allowing users to quickly identify the current page type
- 保持視覺一致性的同時增加區分度
- Maintains visual consistency while adding distinction

---

## 2025-12-07 08:17:30 - Detail 頁面 Category Badge 顏色配置

### 變更內容 / Changes

更新 detail 頁面中的 category badge（例如 "GAME"、"WEBSITE"、"NEWS"），使其根據類型顯示對應的顏色，與頁面 header 顏色保持一致。

Updated category badges (e.g., "GAME", "WEBSITE", "NEWS") in detail pages to display corresponding colors based on type, matching the page header colors.

### 修改的檔案 / Modified Files

1. **frontend/components/ProjectDetail.tsx**
   - 添加 `getCategoryBadgeColor()` 函數，根據 project.category 返回對應的 badge 顏色
   - Added `getCategoryBadgeColor()` function that returns badge color based on project.category
   - **GAME**: `bg-blue-500` (藍色)
   - **WEBSITE**: `bg-emerald-500` (綠色)
   - 更新 category badge 使用動態顏色
   - Updated category badge to use dynamic color

2. **frontend/components/NewsDetail.tsx**
   - 在 hero image 上添加 "NEWS" category badge
   - Added "NEWS" category badge on hero image
   - 使用 `bg-orange-500` (橙色) 與頁面 header 顏色一致
   - Uses `bg-orange-500` (orange) to match page header color

### 顏色配置 / Color Configuration

- **GAME Badge**: `bg-blue-500` - 藍色 badge，與藍色 header 一致
- **WEBSITE Badge**: `bg-emerald-500` - 綠色 badge，與綠色 header 一致
- **NEWS Badge**: `bg-orange-500` - 橙色 badge，與橙色 header 一致

### 效果 / Effects

- Category badge 現在與頁面 header 使用相同的顏色主題
- Category badges now use the same color theme as page headers
- 視覺一致性更好，用戶可以通過顏色快速識別頁面類型
- Better visual consistency, users can quickly identify page types through color
- News detail 頁面現在也有 category badge，與其他 detail 頁面保持一致
- News detail page now also has category badge, consistent with other detail pages

---

## 2025-12-07 08:20:14 - 修復導航欄 Active 狀態判斷

### 變更內容 / Changes

修復導航欄的 active 狀態判斷邏輯，現在當進入 detail 頁面（如 `/game/123`、`/website/456`、`/news/789`）時，對應的導航項目會正確顯示為 active 狀態。

Fixed navigation bar active state logic. Now when entering detail pages (e.g., `/game/123`, `/website/456`, `/news/789`), the corresponding navigation items will correctly display as active.

### 問題描述 / Issue

- 當點選 "Games" 進入 detail 頁面（如 `/game/123`）時，導航欄中的 "Games" 不會顯示為 active 狀態
- When clicking "Games" to enter detail page (e.g., `/game/123`), the "Games" item in navigation bar doesn't show as active
- 同樣的問題也存在於 "Websites" 和 "News" 導航項目
- Same issue exists for "Websites" and "News" navigation items

### 修改的檔案 / Modified Files

**frontend/components/Layout.tsx**
- 更新 `isActive()` 函數，支援子路徑匹配
- Updated `isActive()` function to support sub-path matching
- 首頁 (`/`) 需要完全匹配
- Home page (`/`) requires exact match
- 其他路徑（`/game`、`/website`、`/news`、`/about`）使用 `startsWith` 判斷，支援 detail 頁面
- Other paths (`/game`, `/website`, `/news`, `/about`) use `startsWith` check to support detail pages

### 邏輯說明 / Logic

```typescript
const isActive = (path: string) => {
  // 首頁需要完全匹配
  if (path === '/') {
    return location.pathname === '/';
  }
  // 其他路徑：完全匹配或子路徑匹配
  // 例如：/game 匹配 /game 和 /game/123
  return location.pathname === path || location.pathname.startsWith(`${path}/`);
};
```

### 效果 / Effects

- ✅ 進入 `/game/123` 時，"Games" 導航項目顯示為 active
- ✅ When entering `/game/123`, "Games" navigation item shows as active
- ✅ 進入 `/website/456` 時，"Websites" 導航項目顯示為 active
- ✅ When entering `/website/456`, "Websites" navigation item shows as active
- ✅ 進入 `/news/789` 時，"News" 導航項目顯示為 active
- ✅ When entering `/news/789`, "News" navigation item shows as active
- ✅ 首頁 (`/`) 仍然正確判斷
- ✅ Home page (`/`) still correctly identified
- ✅ 桌面版和移動版導航都正確工作
- ✅ Both desktop and mobile navigation work correctly

