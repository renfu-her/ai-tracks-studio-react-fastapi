/**
 * useSEO Hook - Custom hook for managing SEO in components
 * useSEO 鉤子 - 在組件中管理 SEO 的自定義鉤子
 */

import { useEffect } from 'react';
import { updateSEO, SEOConfig, generateStructuredData } from '../utils/seo';

/**
 * Hook to manage SEO meta tags
 * 管理 SEO meta 標籤的鉤子
 * 
 * @example
 * ```tsx
 * function MyPage() {
 *   useSEO({
 *     title: 'My Page',
 *     description: 'Page description',
 *     canonical: 'https://studio.ai-tracks.com/my-page'
 *   });
 *   
 *   return <div>Content</div>;
 * }
 * ```
 */
export const useSEO = (config: SEOConfig, structuredData?: Record<string, any>): void => {
  useEffect(() => {
    // Update meta tags
    updateSEO(config);

    // Update structured data if provided
    if (structuredData) {
      generateStructuredData(structuredData);
    }

    // Cleanup is not necessary for meta tags as they will be updated
    // by the next page. However, we clean up structured data.
    return () => {
      if (structuredData) {
        const script = document.querySelector('script[type="application/ld+json"]');
        if (script) {
          script.remove();
        }
      }
    };
  }, [config, structuredData]);
};

export default useSEO;











