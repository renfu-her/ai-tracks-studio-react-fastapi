/**
 * News API Service
 * Handles all news-related API calls
 */

import { apiClient } from './client';
import { API_ENDPOINTS } from './config';
import type { NewsItem, NewsListResponse } from '../types';

export const newsApi = {
  /**
   * Get all news articles
   */
  getNews: async (params?: {
    skip?: number;
    limit?: number;
  }): Promise<NewsListResponse> => {
    const searchParams = new URLSearchParams();
    
    if (params?.skip !== undefined) {
      searchParams.append('skip', params.skip.toString());
    }
    if (params?.limit !== undefined) {
      searchParams.append('limit', params.limit.toString());
    }
    
    const query = searchParams.toString();
    const endpoint = query ? `${API_ENDPOINTS.NEWS}?${query}` : API_ENDPOINTS.NEWS;
    
    return apiClient.get<NewsListResponse>(endpoint);
  },
  
  /**
   * Get a single news article by ID
   */
  getNewsItem: async (id: string): Promise<NewsItem> => {
    return apiClient.get<NewsItem>(`${API_ENDPOINTS.NEWS}/${id}`);
  },
};

