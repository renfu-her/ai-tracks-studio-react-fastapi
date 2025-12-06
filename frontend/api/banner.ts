/**
 * Banner API Service
 * Handles all banner-related API calls
 */

import { apiClient } from './client';
import { getImageUrl } from './config';

export enum PageType {
  HOME = 'HOME',
  GAME = 'GAME',
  WEBSITE = 'WEBSITE',
  NEWS = 'NEWS',
  ABOUT = 'ABOUT',
}

export interface Banner {
  id: string;
  page_type: PageType;
  image: string; // Filename only
  created_at: string;
  updated_at: string;
}

export const bannerApi = {
  /**
   * Get banner by page type
   */
  getBannerByPageType: async (pageType: PageType): Promise<Banner | null> => {
    try {
      return await apiClient.get<Banner>(`/banners/page/${pageType}`);
    } catch (error: any) {
      // Return null if banner not found (404), throw other errors
      if (error?.response?.status === 404) {
        return null;
      }
      throw error;
    }
  },
  
  /**
   * Get banner image URL
   */
  getBannerImageUrl: (banner: Banner | null): string | null => {
    if (!banner || !banner.image) {
      return null;
    }
    return getImageUrl(banner.image);
  },
};

