# SEO Quick Start - 快速開始

## ⚡ 快速使用

### 在任何頁面添加 SEO

```typescript
import { useSEO } from './hooks/useSEO';
import { generatePageSEO } from './utils/seo';

function MyPage() {
  // 添加這兩行就完成了！
  useSEO(generatePageSEO(
    'Page Title',                           // 頁面標題
    'Page description for search engines'   // 頁面描述
  ));

  return <div>Your content</div>;
}
```

### 帶更多選項

```typescript
useSEO(
  generatePageSEO(
    'Page Title',
    'Page description',
    {
      canonical: 'https://studio.ai-tracks.com/page',
      keywords: 'keyword1, keyword2, keyword3',
      ogImage: 'https://studio.ai-tracks.com/image.jpg'
    }
  )
);
```

### 動態頁面 SEO（基於數據）

```typescript
function ProjectDetail() {
  const [project, setProject] = useState(null);

  useSEO(
    project ? {
      title: `${project.title} | AI-Tracks Studio`,
      description: project.description.substring(0, 160),
      canonical: `https://studio.ai-tracks.com/game/${project.id}`,
      ogImage: getImageUrl(project.image),
    } : {
      title: 'Loading...',
      description: 'Loading project...'
    }
  );

  return <div>Project content</div>;
}
```

## 📋 SEO 檢查清單

部署前檢查：

- [ ] 每個頁面都有 `useSEO()` 調用
- [ ] Title 唯一且描述性
- [ ] Description 在 160 字內
- [ ] 設置了 canonical URL
- [ ] 圖片有適當的 og:image
- [ ] `robots.txt` 在 public/
- [ ] `sitemap.xml` 在 public/

## 🚀 部署後

1. **提交 Sitemap：**
   - Google Search Console: https://search.google.com/search-console
   - Bing Webmaster: https://www.bing.com/webmasters

2. **驗證 SEO：**
   - Rich Results Test: https://search.google.com/test/rich-results
   - Facebook Debugger: https://developers.facebook.com/tools/debug/
   - Twitter Validator: https://cards-dev.twitter.com/validator

3. **檢查 Lighthouse SEO 分數**（Chrome DevTools）

## 📚 更多信息

詳細文檔：`SEO_GUIDE.md`






