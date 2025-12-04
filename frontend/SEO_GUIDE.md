# SEO Implementation Guide - AI-Tracks Studio

## 概述 Overview

This document describes the SEO (Search Engine Optimization) implementation for AI-Tracks Studio frontend.

本文檔描述了 AI-Tracks Studio 前端的 SEO（搜索引擎優化）實現。

## 🎯 SEO 功能 Features

### 1. Dynamic Meta Tags 動態 Meta 標籤

每個頁面都有優化的 meta 標籤：

- **Title** - 頁面標題
- **Description** - 頁面描述（160 字符內）
- **Keywords** - 關鍵字
- **Open Graph** - 社交媒體分享（Facebook, LinkedIn）
- **Twitter Card** - Twitter 分享卡片
- **Canonical URL** - 規範 URL（避免重複內容）
- **Robots** - 爬蟲指令

### 2. Structured Data 結構化數據 (JSON-LD)

實現了 Schema.org 結構化數據：

- **Organization** - 組織信息
- **Article** - 新聞文章
- **SoftwareApplication** - 遊戲和網站項目

### 3. Sitemap & Robots.txt

- **sitemap.xml** - 網站地圖
- **robots.txt** - 爬蟲規則

## 📁 文件結構 File Structure

```
frontend/
├── utils/
│   └── seo.ts                    # SEO 工具函數
├── hooks/
│   └── useSEO.ts                 # SEO 自定義 Hook
├── components/
│   ├── SEO.tsx                   # SEO 組件（可選）
│   ├── App.tsx                   # 各頁面 SEO 實現
│   ├── ProjectDetail.tsx         # 專案詳情頁 SEO
│   └── NewsDetail.tsx            # 新聞詳情頁 SEO
└── public/
    ├── robots.txt                # 爬蟲規則
    └── sitemap.xml               # 網站地圖
```

## 🔧 使用方式 Usage

### 1. 使用 useSEO Hook

在任何頁面組件中使用：

```typescript
import { useSEO } from '../hooks/useSEO';
import { generatePageSEO, ORGANIZATION_DATA } from '../utils/seo';

function MyPage() {
  useSEO(
    generatePageSEO(
      'Page Title',
      'Page description for SEO',
      { 
        canonical: 'https://studio.ai-tracks.com/my-page',
        keywords: 'keyword1, keyword2, keyword3'
      }
    ),
    ORGANIZATION_DATA  // Optional: structured data
  );

  return <div>My Page Content</div>;
}
```

### 2. 使用 SEO 組件

或者使用組件方式：

```typescript
import SEO from '../components/SEO';
import { generatePageSEO } from '../utils/seo';

function MyPage() {
  return (
    <>
      <SEO
        {...generatePageSEO('Page Title', 'Page description')}
      />
      <div>My Page Content</div>
    </>
  );
}
```

### 3. 動態 SEO（基於數據）

對於動態內容頁面：

```typescript
import { useSEO } from '../hooks/useSEO';
import { generateArticleData, API_CONFIG } from '../utils/seo';

function ArticlePage() {
  const [article, setArticle] = useState(null);

  useSEO(
    article ? {
      title: `${article.title} | AI-Tracks Studio`,
      description: article.excerpt,
      canonical: `https://studio.ai-tracks.com/article/${article.id}`,
      ogImage: `${API_CONFIG.BASE_URL}/backend/static/uploads/${article.image}`,
      ogType: 'article',
    } : {
      title: 'Loading...',
      description: 'Loading article...',
    },
    article ? generateArticleData({
      title: article.title,
      description: article.excerpt,
      datePublished: article.date,
      author: article.author,
    }) : undefined
  );

  return <div>Article Content</div>;
}
```

## 📊 結構化數據 Structured Data

### Organization 組織

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "AI-Tracks Studio",
  "url": "https://studio.ai-tracks.com",
  "logo": "https://studio.ai-tracks.com/logo.png"
}
```

### Article 文章

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "description": "Article description",
  "datePublished": "2025-12-04",
  "author": {
    "@type": "Person",
    "name": "Author Name"
  }
}
```

### Software Application 軟體應用

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Game Title",
  "applicationCategory": "GameApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }
}
```

## 🌐 Sitemap.xml

靜態網站地圖已創建在 `public/sitemap.xml`。

### 動態 Sitemap（進階）

為了包含所有動態頁面（遊戲、網站、新聞），建議創建動態 sitemap：

**後端實現示例：**

```python
# backend/app/routers/sitemap.py
from fastapi import APIRouter
from fastapi.responses import Response
from app.repositories.project import ProjectRepository
from app.repositories.news import NewsRepository

router = APIRouter()

@router.get("/sitemap.xml")
async def get_sitemap():
    # Fetch all projects and news
    projects = await ProjectRepository.get_all()
    news = await NewsRepository.get_all()
    
    # Generate XML
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    """
    
    # Add homepage, static pages
    xml += """
      <url>
        <loc>https://studio.ai-tracks.com/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
      </url>
    """
    
    # Add dynamic pages
    for project in projects:
        category = 'game' if project.category == 'GAME' else 'website'
        xml += f"""
      <url>
        <loc>https://studio.ai-tracks.com/{category}/{project.id}</loc>
        <lastmod>{project.updated_at}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
      </url>
        """
    
    for article in news:
        xml += f"""
      <url>
        <loc>https://studio.ai-tracks.com/news/{article.id}</loc>
        <lastmod>{article.updated_at}</lastmod>
        <changefreq>yearly</changefreq>
        <priority>0.6</priority>
      </url>
        """
    
    xml += "</urlset>"
    
    return Response(content=xml, media_type="application/xml")
```

## 🤖 Robots.txt

已創建 `public/robots.txt`：

```
User-agent: *
Allow: /
Sitemap: https://studio.ai-tracks.com/sitemap.xml
```

## ✅ SEO 檢查清單 Checklist

### 基礎 SEO

- [x] 每個頁面都有唯一的 title
- [x] 每個頁面都有描述性的 meta description
- [x] 使用語義化 HTML 標籤
- [x] 設置 canonical URLs
- [x] 創建 robots.txt
- [x] 創建 sitemap.xml

### 社交媒體

- [x] Open Graph 標籤（Facebook, LinkedIn）
- [x] Twitter Card 標籤
- [x] 設置 og:image（社交分享圖片）

### 結構化數據

- [x] Organization schema
- [x] Article schema（新聞頁）
- [x] SoftwareApplication schema（遊戲/網站）

### 技術 SEO

- [x] 使用語義化 HTML5 標籤
- [x] 正確的標題層級（h1, h2, h3）
- [x] 圖片有 alt 屬性
- [x] 內部連結優化
- [x] URL 結構清晰

## 📈 SEO 測試工具

### 驗證工具

1. **Google Search Console**
   - 提交 sitemap.xml
   - 檢查索引狀態
   - 查看搜索表現

2. **Google Rich Results Test**
   - https://search.google.com/test/rich-results
   - 驗證結構化數據

3. **Facebook Sharing Debugger**
   - https://developers.facebook.com/tools/debug/
   - 驗證 Open Graph 標籤

4. **Twitter Card Validator**
   - https://cards-dev.twitter.com/validator
   - 驗證 Twitter Card

5. **Lighthouse (Chrome DevTools)**
   - SEO 審核
   - 性能測試
   - 最佳實踐檢查

### 檢查命令

```bash
# 檢查 robots.txt
curl https://studio.ai-tracks.com/robots.txt

# 檢查 sitemap.xml
curl https://studio.ai-tracks.com/sitemap.xml

# 檢查頁面 meta 標籤
curl -s https://studio.ai-tracks.com | grep -E '<title>|<meta'
```

## 🚀 部署建議

### 1. 更新 sitemap.xml

每次添加新內容時：
- 手動更新 `public/sitemap.xml`
- 或實現動態 sitemap 生成

### 2. 提交到搜索引擎

- **Google Search Console**: 提交 sitemap
- **Bing Webmaster Tools**: 提交 sitemap

### 3. 監控 SEO 表現

- 定期檢查 Search Console
- 追蹤關鍵字排名
- 監控頁面索引狀態

## 📚 參考資源

- [Google SEO Starter Guide](https://developers.google.com/search/docs/beginner/seo-starter-guide)
- [Schema.org Documentation](https://schema.org/)
- [Open Graph Protocol](https://ogp.me/)
- [Twitter Cards Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards)

---

**最後更新：** 2025-12-04  
**版本：** 1.0  
**狀態：** ✅ 完整實現

