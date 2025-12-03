export enum Category {
  GAME = 'GAME',
  WEBSITE = 'WEBSITE',
}

export interface ProjectItem {
  id: string;
  title: string;
  description: string;
  thumbnail_url: string;
  category: Category;
  date: string;
  tags: string[];
  link?: string;
  created_at: string;
  updated_at: string;
}

export interface NewsItem {
  id: string;
  title: string;
  excerpt: string;
  content: string;
  date: string;
  image_url: string;
  author: string;
  created_at: string;
  updated_at: string;
}

export interface AboutValue {
  icon: string;
  title: string;
  description: string;
}

export interface AboutUs {
  id: number;
  title: string | null;
  subtitle: string | null;
  description: string | null;
  values: AboutValue[];
  contact_email: string | null;
  created_at: string;
  updated_at: string;
}

// API Response types
export interface ProjectListResponse {
  total: number;
  items: ProjectItem[];
}

export interface NewsListResponse {
  total: number;
  items: NewsItem[];
}

// Loading and Error states
export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}