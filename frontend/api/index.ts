/**
 * API Module
 * Central export point for all API services
 */

export * from './config';
export * from './client';
export * from './projects';
export * from './news';
export * from './about';
export * from './banner';

// Re-export types that are commonly used with API
export type { ProjectItem, NewsItem, AboutUs, Category } from '../types';
export { Category as CategoryEnum } from '../types';

