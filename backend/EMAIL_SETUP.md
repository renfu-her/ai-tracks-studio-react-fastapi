# Email Configuration Guide 郵件配置指南

## Gmail SMTP Setup Gmail SMTP 設置

### Step 1: Enable Gmail App Password 啟用 Gmail 應用程式密碼

1. Go to your Google Account settings
2. Navigate to **Security** → **2-Step Verification** (must be enabled)
3. Scroll down to **App passwords**
4. Create a new app password for "Mail"
5. Copy the 16-character password (you'll use this as `SMTP_PASSWORD`)

### Step 2: Configure .env File 配置 .env 文件

Add the following to your `backend/.env` file:

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

### Configuration Details 配置詳情

- **SMTP_HOST**: Gmail SMTP server (`smtp.gmail.com`)
- **SMTP_PORT**: Gmail SMTP port (`587` for TLS)
- **SMTP_USER**: Your Gmail address
- **SMTP_PASSWORD**: Gmail App Password (16 characters, no spaces)
- **SMTP_FROM_EMAIL**: Email address shown as sender (usually same as SMTP_USER)
- **SMTP_FROM_NAME**: Display name for sender
- **FEEDBACK_TO_EMAIL**: Email address to receive feedback notifications

### Testing Email Configuration 測試郵件配置

After configuring, restart the backend server. When a user submits feedback:

1. Feedback is saved to database
2. Email notification is sent to `FEEDBACK_TO_EMAIL`
3. Email includes feedback details (name, email, subject, message)

### Troubleshooting 故障排除

**Email not sending:**
- Check that 2-Step Verification is enabled on Gmail account
- Verify App Password is correct (16 characters)
- Check SMTP_USER matches the Gmail account
- Check FEEDBACK_TO_EMAIL is set correctly

**Connection errors:**
- Ensure SMTP_PORT is 587 (TLS) or 465 (SSL)
- Check firewall/network allows SMTP connections
- Verify Gmail account is not locked

### Security Notes 安全提示

⚠️ **Important:**
- Never commit `.env` file to version control
- Use App Passwords, not your main Gmail password
- Keep App Passwords secure and rotate regularly
- In production, use environment variables or secure secret management
