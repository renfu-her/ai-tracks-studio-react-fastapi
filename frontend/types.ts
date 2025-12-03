export enum Category {
  GAME = 'GAME',
  WEBSITE = 'WEBSITE',
}

export interface ProjectItem {
  id: string;
  title: string;
  description: string;
  thumbnailUrl: string;
  category: Category;
  date: string;
  tags: string[];
  link?: string;
}

export interface NewsItem {
  id: string;
  title: string;
  excerpt: string;
  content: string;
  date: string;
  imageUrl: string;
  author: string;
}