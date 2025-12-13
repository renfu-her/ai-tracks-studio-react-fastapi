/**
 * About Us API Service
 * Handles About page content API calls
 */

import { apiClient } from './client';
import { API_ENDPOINTS } from './config';
import type { AboutUs } from '../types';

export const aboutApi = {
  /**
   * Get the current About Us content
   */
  getAbout: async (): Promise<AboutUs> => {
    return apiClient.get<AboutUs>(API_ENDPOINTS.ABOUT);
  },
  
  /**
   * Get specific About Us content by ID
   */
  getAboutById: async (id: number): Promise<AboutUs> => {
    return apiClient.get<AboutUs>(`${API_ENDPOINTS.ABOUT}/${id}`);
  },
  
  /**
   * Increment view count for About Us content
   */
  incrementViews: async (id: number): Promise<AboutUs> => {
    return apiClient.post<AboutUs>(`${API_ENDPOINTS.ABOUT}/${id}/view`);
  },
};

