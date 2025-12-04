/**
 * SEO Component - Manages SEO meta tags for each page
 * SEO 組件 - 管理每個頁面的 SEO meta 標籤
 */

import { useEffect } from 'react';
import { updateSEO, SEOConfig } from '../utils/seo';

interface SEOProps extends SEOConfig {
  structuredData?: Record<string, any>;
}

/**
 * SEO Component
 * Use this component in any page to set SEO metadata
 * 
 * @example
 * ```tsx
 * <SEO
 *   title="Games | AI-Tracks Studio"
 *   description="Explore our collection of AI-powered games"
 *   keywords="games, AI, interactive"
 *   canonical="https://studio.ai-tracks.com/game"
 * />
 * ```
 */
export const SEO: React.FC<SEOProps> = ({ structuredData, ...seoConfig }) => {
  useEffect(() => {
    // Update meta tags
    updateSEO(seoConfig);

    // Add structured data if provided
    if (structuredData) {
      const script = document.createElement('script');
      script.type = 'application/ld+json';
      script.text = JSON.stringify(structuredData);
      document.head.appendChild(script);

      return () => {
        // Cleanup: remove structured data script on unmount
        document.head.removeChild(script);
      };
    }
  }, [seoConfig, structuredData]);

  // This component doesn't render anything
  return null;
};

export default SEO;

