/**
 * Projects API Service
 * Handles all project-related API calls (Games & Websites)
 */

import { apiClient } from './client';
import { API_ENDPOINTS } from './config';
import { Category } from '../types';
import type { ProjectItem, ProjectListResponse } from '../types';

export const projectsApi = {
  /**
   * Get all projects with optional category filter
   */
  getProjects: async (params?: {
    category?: Category;
    skip?: number;
    limit?: number;
  }): Promise<ProjectListResponse> => {
    const searchParams = new URLSearchParams();
    
    if (params?.category) {
      searchParams.append('category', params.category);
    }
    if (params?.skip !== undefined) {
      searchParams.append('skip', params.skip.toString());
    }
    if (params?.limit !== undefined) {
      searchParams.append('limit', params.limit.toString());
    }
    
    const query = searchParams.toString();
    const endpoint = query ? `${API_ENDPOINTS.PROJECTS}?${query}` : API_ENDPOINTS.PROJECTS;
    
    return apiClient.get<ProjectListResponse>(endpoint);
  },
  
  /**
   * Get a single project by ID
   */
  getProject: async (id: string): Promise<ProjectItem> => {
    return apiClient.get<ProjectItem>(`${API_ENDPOINTS.PROJECTS}/${id}`);
  },
  
  /**
   * Get games only
   */
  getGames: async (skip?: number, limit?: number): Promise<ProjectListResponse> => {
    return projectsApi.getProjects({ category: Category.GAME, skip, limit });
  },
  
  /**
   * Get websites only
   */
  getWebsites: async (skip?: number, limit?: number): Promise<ProjectListResponse> => {
    return projectsApi.getProjects({ category: Category.WEBSITE, skip, limit });
  },
  
  /**
   * Increment view count for a project
   */
  incrementViews: async (id: string): Promise<ProjectItem> => {
    return apiClient.post<ProjectItem>(`${API_ENDPOINTS.PROJECTS}/${id}/view`);
  },
};

