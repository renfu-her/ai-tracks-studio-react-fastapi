/**
 * API Configuration
 * Manages API base URL and environment settings
 */

// Get API base URL from environment or use default
const getApiBaseUrl = (): string => {
  // Check for Vite environment variable
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL;
  }
  
  // Default to localhost in development
  return 'http://localhost:8000';
};

export const API_CONFIG = {
  BASE_URL: getApiBaseUrl(),
  API_PREFIX: '/api',
  TIMEOUT: 30000, // 30 seconds
} as const;

// Build full API URL
export const getApiUrl = (endpoint: string): string => {
  const url = `${API_CONFIG.BASE_URL}${API_CONFIG.API_PREFIX}${endpoint}`;
  return url;
};

// API endpoints
export const API_ENDPOINTS = {
  PROJECTS: '/projects',
  NEWS: '/news',
  ABOUT: '/about',
} as const;

