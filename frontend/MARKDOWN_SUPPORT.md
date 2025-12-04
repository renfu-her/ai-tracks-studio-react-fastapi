# Markdown Support 前端 Markdown 支持

## Overview 概述

The frontend now supports rendering Markdown content as HTML for:
- **Projects** - Project descriptions
- **News** - Article excerpts and content
- **About Us** - Full about content

前端現在支持將 Markdown 內容渲染為 HTML：
- **專案** - 專案描述
- **新聞** - 文章摘要和內容
- **關於我們** - 完整關於內容

## Implementation 實現

### 1. Installed Packages 安裝的套件

**Added to `package.json`:**
```json
{
  "dependencies": {
    "react-markdown": "^9.0.1",
    "remark-gfm": "^4.0.0"
  }
}
```

- **react-markdown**: Renders Markdown as React components
- **remark-gfm**: GitHub Flavored Markdown support (tables, strikethrough, etc.)

### 2. Created MarkdownContent Component 創建 Markdown 組件

**File:** `frontend/components/MarkdownContent.tsx`

This component:
- Takes Markdown string as input
- Renders as styled HTML
- Supports all Markdown features
- Uses Tailwind CSS for styling

### 3. Updated Components 更新的組件

**ProjectDetail.tsx:**
```tsx
import { MarkdownContent } from './MarkdownContent';

<MarkdownContent content={project.description} />
```

**App.tsx (NewsPage):**
```tsx
<MarkdownContent content={item.excerpt} />
```

**App.tsx (AboutPage):**
```tsx
<MarkdownContent content={about.description} />
```

## Supported Markdown Features 支持的 Markdown 功能

### Headings 標題

```markdown
# H1 Heading
## H2 Heading
### H3 Heading
#### H4 Heading
##### H5 Heading
###### H6 Heading
```

**Styling:**
- H1: 4xl, bold, dark gray
- H2: 3xl, bold, dark gray
- H3: 2xl, bold, medium gray
- H4-H6: Progressively smaller

### Text Formatting 文字格式

```markdown
**Bold text**
*Italic text*
***Bold and italic***
~~Strikethrough~~ (with remark-gfm)
```

### Links 連結

```markdown
[Link text](https://example.com)
```

**Styling:**
- Accent color (purple)
- Underlined
- Opens in new tab
- Hover effect

### Lists 列表

**Unordered:**
```markdown
- Item 1
- Item 2
- Item 3
```

**Ordered:**
```markdown
1. First
2. Second
3. Third
```

**Styling:**
- Bullets/numbers inside
- Proper spacing
- Indented

### Blockquotes 引用

```markdown
> This is a blockquote
> It can span multiple lines
```

**Styling:**
- Left border (accent color)
- Light background
- Padding
- Italic text

### Code 代碼

**Inline:**
```markdown
Use `inline code` for short snippets
```

**Block:**
````markdown
```javascript
function hello() {
  console.log("Hello, World!");
}
```
````

**Styling:**
- Inline: Light gray background, accent color text
- Block: Dark background, monospace font, syntax highlighting ready

### Tables 表格

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

**Styling:**
- Bordered
- Header with background
- Hover effect on rows
- Responsive (scrollable on small screens)

### Images 圖片

```markdown
![Alt text](https://example.com/image.jpg)
```

**Styling:**
- Max width 100%
- Rounded corners
- Shadow
- Responsive

### Horizontal Rules 分隔線

```markdown
---
```

**Styling:**
- Thick border
- Light gray
- Spacing above and below

## Usage Examples 使用示例

### In Projects 在專案中

**Backend (admin panel):**
```markdown
## Introduction

NEON TETRIS is a modern take on the classic Tetris game...

### Features

- **Neon Graphics**: Beautiful glowing effects
- **Smooth Gameplay**: 60 FPS performance
- **Responsive Controls**: Works on all devices

[Play Now](https://example.com/play)
```

**Frontend display:**
- Headings styled with proper hierarchy
- Bold features highlighted
- Link styled with accent color
- All rendered as beautiful HTML

### In News 在新聞中

**Backend (excerpt):**
```markdown
We're excited to announce our **latest game release**! 

Check out the [announcement blog](https://example.com/blog) for details.
```

**Frontend display:**
- Bold text emphasized
- Link clickable
- Proper paragraph spacing

### In About Us 在關於我們中

**Backend (full content):**
```markdown
## Who We Are

AI-Tracks Studio is a creative technology studio...

## Our Values

We believe in:

1. **Innovation**: Always pushing boundaries
2. **Quality**: Never compromising on excellence
3. **Creativity**: Thinking outside the box

> "Great things are not done by impulse, but by a series of small things brought together." - Vincent van Gogh

---

## Get In Touch

Email us at: contact@ai-tracks.studio
```

**Frontend display:**
- Full Markdown rendered with all styles
- Professional appearance
- Easy to read
- Well-structured

## Styling Classes 樣式類別

### Component Wrapper

```tsx
<div className="markdown-content">
  {/* Rendered Markdown */}
</div>
```

### Custom Styles 自定義樣式

All elements use Tailwind CSS classes:

**Typography:**
- Text colors: `text-slate-700`, `text-slate-900`
- Font sizes: `text-xl`, `text-2xl`, `text-3xl`, `text-4xl`
- Font weights: `font-bold`, `font-semibold`
- Line height: `leading-relaxed`

**Spacing:**
- Margins: `mb-2`, `mb-4`, `mb-6`, `mt-4`, `mt-6`, `mt-8`
- Padding: `p-4`, `px-2`, `py-0.5`, `pl-4`, `py-2`

**Colors:**
- Accent: `text-accent-600`, `border-accent-500`, `bg-accent-500`
- Slate: `text-slate-700`, `bg-slate-100`, `border-slate-300`

**Effects:**
- Rounded: `rounded`, `rounded-lg`, `rounded-r-lg`
- Shadows: `shadow-md`
- Transitions: `transition-colors`, `transition-all`

## Best Practices 最佳實踐

### 1. Use Semantic Headings 使用語義標題

```markdown
## Main Section
### Subsection
#### Detail
```

**Why:**
- Better structure
- Easier to read
- Good for SEO

### 2. Format Lists Properly 正確格式化列表

```markdown
- Clear point
- Another point
- Final point
```

**Not:**
```markdown
-Unclear
- Missing space
-  Too many spaces
```

### 3. Use Links for External Resources 使用連結

```markdown
[Read more](https://example.com)
```

**Not:**
```
Visit https://example.com for more
```

### 4. Add Alt Text to Images 為圖片添加 Alt 文字

```markdown
![Game screenshot showing neon effects](image.jpg)
```

**Why:**
- Accessibility
- Better SEO
- Context when image fails to load

### 5. Use Code Blocks for Code 使用代碼塊

````markdown
```javascript
const greeting = "Hello";
```
````

**Not:**
```markdown
const greeting = "Hello";
```

## Testing Markdown 測試 Markdown

### 1. In Admin Panel 在後台管理

1. Login to backend admin
2. Go to any module (Projects/News/About)
3. Edit or create content
4. Use Markdown in description fields
5. Save
6. View on frontend

### 2. Preview on Frontend 在前端預覽

1. Visit the page (e.g., `/game/game-123`)
2. Check that Markdown is rendered
3. Verify styling is correct
4. Test links (should open in new tab)
5. Check responsiveness

### 3. Test All Features 測試所有功能

Create test content with:
- All heading levels
- Bold, italic, strikethrough
- Lists (ordered and unordered)
- Links
- Code blocks
- Blockquotes
- Tables
- Images

## Troubleshooting 故障排除

### Issue: Markdown Not Rendering Markdown 未渲染

**Check:**
1. Is `react-markdown` installed?
2. Is `MarkdownContent` imported?
3. Is content passed as string (not null)?

**Fix:**
```tsx
{content && <MarkdownContent content={content} />}
```

### Issue: Styling Not Applied 樣式未應用

**Check:**
1. Tailwind CSS loaded?
2. Custom classes defined?
3. Component wrapper present?

**Fix:**
Ensure parent has proper container classes.

### Issue: Links Not Working 連結不工作

**Check:**
1. URL format correct?
2. `target="_blank"` set?
3. `rel="noopener noreferrer"` present?

**Fix:**
Already handled in `MarkdownContent` component.

### Issue: Code Blocks Not Styled 代碼塊未樣式化

**Check:**
1. Using triple backticks?
2. Component handles `code` element?

**Example:**
````markdown
```javascript
console.log("test");
```
````

## Performance Considerations 性能考慮

### 1. Memoization 記憶化

For large Markdown content, consider memoization:

```tsx
import { memo } from 'react';

export const MarkdownContent = memo(({ content }) => {
  // Component code
});
```

### 2. Lazy Loading 懶加載

For pages with lots of Markdown:

```tsx
import { lazy, Suspense } from 'react';

const MarkdownContent = lazy(() => import('./components/MarkdownContent'));

<Suspense fallback={<LoadingSpinner />}>
  <MarkdownContent content={content} />
</Suspense>
```

### 3. Code Splitting 代碼分割

`react-markdown` is automatically code-split with Vite.

## Future Enhancements 未來改進

### 1. Syntax Highlighting 語法高亮

Install `react-syntax-highlighter`:

```tsx
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';

code: ({ className, children }) => {
  const match = /language-(\w+)/.exec(className || '');
  return match ? (
    <SyntaxHighlighter language={match[1]}>
      {String(children)}
    </SyntaxHighlighter>
  ) : (
    <code>{children}</code>
  );
}
```

### 2. Custom Plugins 自定義插件

Add more remark/rehype plugins:

```tsx
import remarkToc from 'remark-toc';
import rehypeSlug from 'rehype-slug';

<ReactMarkdown
  remarkPlugins={[remarkGfm, remarkToc]}
  rehypePlugins={[rehypeSlug]}
>
  {content}
</ReactMarkdown>
```

### 3. LaTeX Support LaTeX 支持

For mathematical expressions:

```bash
npm install remark-math rehype-katex
```

### 4. Copy Code Button 複製代碼按鈕

Add copy button to code blocks for better UX.

---

**Created:** 2025-12-04  
**Status:** ✅ Implemented  
**Files:** 
- `frontend/components/MarkdownContent.tsx`
- `frontend/package.json`
- `frontend/components/ProjectDetail.tsx`
- `frontend/App.tsx`

