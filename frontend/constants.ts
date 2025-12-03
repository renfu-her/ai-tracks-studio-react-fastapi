import { Category, ProjectItem, NewsItem } from './types';

export const HERO_IMAGES = {
  home: "https://picsum.photos/1920/600?grayscale&blur=2",
  games: "https://picsum.photos/1920/400?random=100",
  websites: "https://picsum.photos/1920/400?random=200",
  news: "https://picsum.photos/1920/400?random=300",
  about: "https://picsum.photos/1920/400?random=400",
};

// Generate 12 items to demonstrate pagination/grid (displaying 9)
const generateProjects = (category: Category, count: number): ProjectItem[] => {
  return Array.from({ length: count }).map((_, i) => ({
    id: `${category.toLowerCase()}-${i}`,
    title: `${category === Category.GAME ? 'Super' : 'Modern'} ${category === Category.GAME ? 'Adventure' : 'Dashboard'} ${i + 1}`,
    description: category === Category.GAME 
      ? "An immersive experience challenging your reflexes and puzzle-solving skills in a vibrant world." 
      : "A fully responsive, high-performance web solution designed with the latest React technologies.",
    thumbnailUrl: `https://picsum.photos/600/400?random=${category === Category.GAME ? 10 + i : 50 + i}`,
    category: category,
    date: `2024-0${(i % 9) + 1}-15`,
    tags: category === Category.GAME ? ['Action', 'Unity', 'WebGL'] : ['React', 'Next.js', 'Tailwind'],
  }));
};

export const GAMES: ProjectItem[] = generateProjects(Category.GAME, 12);
export const WEBSITES: ProjectItem[] = generateProjects(Category.WEBSITE, 12);

export const NEWS: NewsItem[] = [
  {
    id: 'news-1',
    title: "AI-Tracks Studio Launches New AI Engine",
    excerpt: "We are proud to announce the release of our proprietary generative engine for dynamic gameplay.",
    content: "Full content here...",
    date: "2024-05-20",
    imageUrl: "https://picsum.photos/800/600?random=1",
    author: "Renfu Her"
  },
  {
    id: 'news-2',
    title: "Upcoming Web Design Trends for 2025",
    excerpt: "Our design team breaks down what to expect in the next wave of immersive web experiences.",
    content: "Full content here...",
    date: "2024-05-18",
    imageUrl: "https://picsum.photos/800/600?random=2",
    author: "Design Team"
  },
  {
    id: 'news-3',
    title: "Community Game Jam Results",
    excerpt: "The results are in! Check out the top rated submissions from our Spring code jam.",
    content: "Full content here...",
    date: "2024-05-10",
    imageUrl: "https://picsum.photos/800/600?random=3",
    author: "Community Mgr"
  },
  {
    id: 'news-4',
    title: "Partnering with Tech Giants",
    excerpt: "We are expanding our horizons with new strategic partnerships.",
    content: "Full content here...",
    date: "2024-04-22",
    imageUrl: "https://picsum.photos/800/600?random=4",
    author: "Renfu Her"
  }
];