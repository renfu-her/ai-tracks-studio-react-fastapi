/**
 * SEO Utilities - Native React SEO without external dependencies
 * 原生 React SEO 工具 - 不依賴外部套件
 */

export interface SEOConfig {
  title: string;
  description: string;
  keywords?: string;
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  ogUrl?: string;
  ogType?: 'website' | 'article';
  twitterCard?: 'summary' | 'summary_large_image';
  canonical?: string;
  noindex?: boolean;
}

/**
 * Update document meta tags for SEO
 * 更新文檔 meta 標籤以優化 SEO
 */
export const updateSEO = (config: SEOConfig): void => {
  // Update title
  document.title = config.title;

  // Helper function to update or create meta tag
  const setMetaTag = (attribute: string, value: string, content: string) => {
    let element = document.querySelector(`meta[${attribute}="${value}"]`);
    if (!element) {
      element = document.createElement('meta');
      element.setAttribute(attribute, value);
      document.head.appendChild(element);
    }
    element.setAttribute('content', content);
  };

  // Update description
  setMetaTag('name', 'description', config.description);

  // Update keywords
  if (config.keywords) {
    setMetaTag('name', 'keywords', config.keywords);
  }

  // Open Graph tags
  setMetaTag('property', 'og:title', config.ogTitle || config.title);
  setMetaTag('property', 'og:description', config.ogDescription || config.description);
  setMetaTag('property', 'og:type', config.ogType || 'website');
  
  if (config.ogImage) {
    setMetaTag('property', 'og:image', config.ogImage);
  }
  
  if (config.ogUrl) {
    setMetaTag('property', 'og:url', config.ogUrl);
  }

  // Twitter Card tags
  setMetaTag('name', 'twitter:card', config.twitterCard || 'summary_large_image');
  setMetaTag('name', 'twitter:title', config.ogTitle || config.title);
  setMetaTag('name', 'twitter:description', config.ogDescription || config.description);
  
  if (config.ogImage) {
    setMetaTag('name', 'twitter:image', config.ogImage);
  }

  // Canonical URL
  if (config.canonical) {
    let link = document.querySelector('link[rel="canonical"]') as HTMLLinkElement;
    if (!link) {
      link = document.createElement('link');
      link.rel = 'canonical';
      document.head.appendChild(link);
    }
    link.href = config.canonical;
  }

  // Robots meta tag
  if (config.noindex) {
    setMetaTag('name', 'robots', 'noindex, nofollow');
  } else {
    setMetaTag('name', 'robots', 'index, follow');
  }
};

/**
 * Default SEO configuration for the site
 * 網站的預設 SEO 配置
 */
export const DEFAULT_SEO: SEOConfig = {
  title: 'AI-Tracks Studio - Innovative Web & Game Experiences',
  description: 'AI-Tracks Studio creates cutting-edge web applications and games powered by artificial intelligence. Explore our portfolio of innovative projects.',
  keywords: 'AI, web development, game development, interactive experiences, React, TypeScript',
  ogType: 'website',
  ogImage: 'https://studio.ai-tracks.com/og-image.jpg',
  twitterCard: 'summary_large_image',
};

/**
 * Generate page-specific SEO config
 * 生成頁面專用的 SEO 配置
 */
export const generatePageSEO = (
  title: string,
  description: string,
  options?: Partial<SEOConfig>
): SEOConfig => {
  return {
    ...DEFAULT_SEO,
    title: `${title} | AI-Tracks Studio`,
    description,
    ogTitle: `${title} | AI-Tracks Studio`,
    ogDescription: description,
    ...options,
  };
};

/**
 * Generate structured data (JSON-LD) for search engines
 * 為搜索引擎生成結構化數據（JSON-LD）
 */
export const generateStructuredData = (data: Record<string, any>): void => {
  // Remove existing structured data
  const existing = document.querySelector('script[type="application/ld+json"]');
  if (existing) {
    existing.remove();
  }

  // Create new structured data script
  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.text = JSON.stringify(data);
  document.head.appendChild(script);
};

/**
 * Organization structured data
 * 組織結構化數據
 */
export const ORGANIZATION_DATA = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'AI-Tracks Studio',
  url: 'https://studio.ai-tracks.com',
  logo: 'https://studio.ai-tracks.com/logo.png',
  description: 'Innovative Web & Game Experiences Powered by AI',
  sameAs: [
    // Add social media links here
    // 'https://twitter.com/ai-tracks',
    // 'https://github.com/ai-tracks',
  ],
};

/**
 * Generate article structured data
 * 生成文章結構化數據
 */
export const generateArticleData = (article: {
  title: string;
  description: string;
  image?: string;
  datePublished: string;
  dateModified?: string;
  author?: string;
}) => ({
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: article.title,
  description: article.description,
  image: article.image,
  datePublished: article.datePublished,
  dateModified: article.dateModified || article.datePublished,
  author: {
    '@type': 'Person',
    name: article.author || 'AI-Tracks Studio',
  },
  publisher: {
    '@type': 'Organization',
    name: 'AI-Tracks Studio',
    logo: {
      '@type': 'ImageObject',
      url: 'https://studio.ai-tracks.com/logo.png',
    },
  },
});

/**
 * Generate product structured data for games/projects
 * 為遊戲/專案生成產品結構化數據
 */
export const generateProductData = (product: {
  name: string;
  description: string;
  image?: string;
  category: string;
  url?: string;
}) => ({
  '@context': 'https://schema.org',
  '@type': 'SoftwareApplication',
  name: product.name,
  description: product.description,
  image: product.image,
  applicationCategory: product.category === 'GAME' ? 'GameApplication' : 'WebApplication',
  url: product.url,
  offers: {
    '@type': 'Offer',
    price: '0',
    priceCurrency: 'USD',
    availability: 'https://schema.org/InStock',
  },
  author: ORGANIZATION_DATA,
});











