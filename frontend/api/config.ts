/**
 * API Configuration
 * Manages API base URL and environment settings
 */

// Get API base URL from environment or use default
const getApiBaseUrl = (): string => {
  const env = (import.meta as any)?.env;
  // Check for Vite environment variable
  if (env?.VITE_API_BASE_URL) {
    return env.VITE_API_BASE_URL;
  }

  // Fallback to current origin in browser (useful in production)
  if (typeof window !== 'undefined' && window?.location?.origin) {
    return window.location.origin;
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
  FEEDBACK: '/feedback',
  FEEDBACK_CAPTCHA: '/feedback/captcha',
} as const;

/**
 * Build full image URL from filename
 * Backend now returns only filename, not full URL
 */
export const getImageUrl = (filename: string | null | undefined): string => {
  if (!filename) {
    // Return placeholder image if no filename
    return 'https://via.placeholder.com/800x600?text=No+Image';
  }
  
  // Build full URL: http://localhost:8000/backend/static/uploads/filename.webp
  return `${API_CONFIG.BASE_URL}/backend/static/uploads/${filename}`;
};

