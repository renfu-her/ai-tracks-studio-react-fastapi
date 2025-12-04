import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Layout } from './components/Layout';
import { SectionHero } from './components/SectionHero';
import { ItemGrid } from './components/ItemGrid';
import { ProjectDetail } from './components/ProjectDetail';
import { NewsDetail } from './components/NewsDetail';
import { MarkdownContent } from './components/MarkdownContent';
import { HERO_IMAGES } from './constants';
import { ArrowRight, Calendar, User, Star, Zap, Mail, Loader2, AlertCircle } from 'lucide-react';
import { projectsApi, newsApi, aboutApi } from './api';
import type { ProjectItem, NewsItem, AboutUs } from './types';
import { getImageUrl } from './api/config';
import { useSEO } from './hooks/useSEO';
import { generatePageSEO, ORGANIZATION_DATA, generateArticleData } from './utils/seo';

// --- Utility Components ---

const LoadingSpinner: React.FC<{ message?: string }> = ({ message = 'Loading...' }) => (
  <div className="flex flex-col items-center justify-center py-20">
    <Loader2 className="w-12 h-12 text-accent-500 animate-spin mb-4" />
    <p className="text-slate-600 text-lg">{message}</p>
  </div>
);

const ErrorMessage: React.FC<{ message: string; onRetry?: () => void }> = ({ message, onRetry }) => (
  <div className="flex flex-col items-center justify-center py-20">
    <div className="bg-red-50 rounded-2xl p-8 max-w-md text-center">
      <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
      <h3 className="text-xl font-bold text-red-900 mb-2">Oops! Something went wrong</h3>
      <p className="text-red-700 mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-6 py-2 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors font-medium"
        >
          Try Again
        </button>
      )}
    </div>
  </div>
);

// --- Page Components ---

const AboutPage: React.FC = () => {
  const [about, setAbout] = useState<AboutUs | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // SEO
  useSEO(
    generatePageSEO(
      'About Us',
      'Learn about AI-Tracks Studio, our mission, and the innovative team behind cutting-edge web and game experiences powered by artificial intelligence.',
      { 
        canonical: 'https://studio.ai-tracks.com/about',
        keywords: 'about us, AI studio, team, mission, innovation, web development, game development'
      }
    ),
    ORGANIZATION_DATA
  );

  const fetchAbout = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await aboutApi.getAbout();
      setAbout(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load about information');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAbout();
  }, []);

  return (
    <>
      <SectionHero
        title="About Us"
        subtitle="We are a passionate team dedicated to redefining web experiences through AI."
        bgImage={HERO_IMAGES.about}
        overlayColor="from-teal-900/90 to-emerald-900/80"
      />
      <div className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
          {loading ? (
            <LoadingSpinner message="Loading about information..." />
          ) : error ? (
            <ErrorMessage message={error} onRetry={fetchAbout} />
          ) : about ? (
            <>
              {/* Introduction */}
              <div className="max-w-4xl mx-auto animate-in slide-in-from-bottom-4 duration-700">
                <h2 className="text-3xl font-bold text-slate-800 mb-6 text-center">{about.title || 'Who We Are'}</h2>
                {about.description ? (
                  <MarkdownContent content={about.description} />
                ) : (
                  <p className="text-xl text-slate-600 leading-relaxed text-center">
                    AI-Tracks Studio is an innovative digital laboratory situated at the intersection of design, technology, and artificial intelligence.
                  </p>
                )}
              </div>

              {/* Grid of Values */}
              {about.values && about.values.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {about.values.map((value, index) => (
                    <div key={index} className="p-8 bg-slate-50 rounded-2xl border border-slate-100 hover:shadow-lg transition-shadow">
                      <div className={`w-12 h-12 ${index % 2 === 0 ? 'bg-lively-pink' : 'bg-accent-500'} rounded-lg mb-4 flex items-center justify-center text-white shadow-lg`}>
                        {value.icon === 'Star' ? <Star size={24} /> : <Zap size={24} />}
                      </div>
                      <h3 className="text-xl font-bold mb-3 text-slate-800">{value.title}</h3>
                      <p className="text-slate-600">{value.description}</p>
                    </div>
                  ))}
                </div>
              )}

              {/* Contact Section */}
              {about.contact_email && (
                <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-3xl p-10 text-white text-center shadow-2xl relative overflow-hidden group">
                  <div className="absolute top-0 right-0 w-64 h-64 bg-accent-500/10 rounded-full blur-3xl translate-x-1/2 -translate-y-1/2 group-hover:bg-accent-500/20 transition-colors"></div>
                  <div className="relative z-10">
                    <h2 className="text-3xl font-bold mb-6">Get In Touch</h2>
                    <p className="text-slate-300 mb-8 max-w-2xl mx-auto text-lg">
                      Whether you have a project in mind or just want to say hello, we'd love to hear from you.
                    </p>
                    <a
                      href={`mailto:${about.contact_email}`}
                      className="inline-flex items-center gap-2 px-8 py-4 bg-white text-slate-900 rounded-full font-bold hover:bg-lively-yellow transition-colors shadow-lg hover:scale-105 transform duration-300"
                    >
                      <Mail size={20} className="text-accent-600" /> {about.contact_email}
                    </a>
                  </div>
                </div>
              )}
            </>
          ) : null}
        </div>
      </div>
    </>
  );
};

const NewsPage: React.FC = () => {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // SEO
  useSEO(
    generatePageSEO(
      'Latest News',
      'Stay updated with the latest insights, announcements, and developments from AI-Tracks Studio. Explore our articles on AI, web development, and game design.',
      { 
        canonical: 'https://studio.ai-tracks.com/news',
        keywords: 'news, blog, updates, AI news, tech articles, announcements',
        ogType: 'website'
      }
    )
  );

  const fetchNews = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await newsApi.getNews();
      setNews(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load news');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, []);

  return (
    <>
      <SectionHero
        title="Latest News"
        subtitle="Insights, updates, and announcements from the AI-Tracks Studio team."
        bgImage={HERO_IMAGES.news}
        overlayColor="from-lively-pink/90 to-purple-900/80"
      />
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <LoadingSpinner message="Loading news..." />
          ) : error ? (
            <ErrorMessage message={error} onRetry={fetchNews} />
          ) : news.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-slate-600 text-lg">No news articles available yet.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-12 max-w-4xl mx-auto">
              {news.map((item) => (
                <Link
                  key={item.id}
                  to={`/news/${item.id}`}
                  className="flex flex-col md:flex-row gap-8 items-start border-b border-slate-100 pb-12 last:border-0 group block"
                >
                  <div className="w-full md:w-1/3 aspect-video rounded-2xl overflow-hidden shadow-md relative">
                    <img
                      src={getImageUrl(item.image)}
                      alt={item.title}
                      className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                    />
                    <div className="absolute inset-0 bg-accent-500/0 group-hover:bg-accent-500/10 transition-colors duration-300"></div>
                  </div>
                  <div className="w-full md:w-2/3 space-y-4">
                    <div className="flex items-center gap-4 text-sm font-medium text-slate-400">
                      <span className="flex items-center gap-1 text-lively-orange">
                        <Calendar size={16} /> {item.date}
                      </span>
                      <span className="flex items-center gap-1">
                        <User size={16} /> {item.author}
                      </span>
                    </div>
                    <h2 className="text-2xl md:text-3xl font-bold text-slate-800 group-hover:text-accent-600 transition-colors duration-300">
                      {item.title}
                    </h2>
                    <div className="text-slate-600 leading-relaxed text-lg">
                      <MarkdownContent content={item.excerpt} />
                    </div>
                    <div className="flex items-center gap-2 text-accent-600 font-bold group-hover:gap-3 transition-all mt-2">
                      Read Full Story <ArrowRight size={18} />
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

const HomePage: React.FC = () => {
  const [featuredGames, setFeaturedGames] = useState<ProjectItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // SEO - Home Page
  useSEO(
    {
      title: 'AI-Tracks Studio - Innovative Web & Game Experiences Powered by AI',
      description: 'Discover cutting-edge web applications and interactive games created with artificial intelligence. Explore immersive experiences and innovative digital solutions from AI-Tracks Studio.',
      keywords: 'AI studio, web development, game development, interactive experiences, AI-powered games, web demos, React, TypeScript',
      canonical: 'https://studio.ai-tracks.com',
      ogType: 'website',
      ogImage: 'https://studio.ai-tracks.com/og-image.jpg',
      ogUrl: 'https://studio.ai-tracks.com',
    },
    ORGANIZATION_DATA
  );

  useEffect(() => {
    const fetchFeatured = async () => {
      try {
        const response = await projectsApi.getGames(0, 3);
        setFeaturedGames(response.items);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load featured games');
      } finally {
        setLoading(false);
      }
    };
    fetchFeatured();
  }, []);

  return (
    <>
      {/* Home Banner */}
      <div className="relative h-[450px] flex items-center justify-center overflow-hidden">
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: `url(${HERO_IMAGES.home})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/95 via-accent-900/80 to-lively-pink/30" />

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-white space-y-6 animate-in fade-in slide-in-from-bottom-8 duration-1000">
          <div className="inline-block px-4 py-1.5 rounded-full border border-white/20 bg-white/10 backdrop-blur-md text-sm font-semibold tracking-wide mb-2 text-lively-yellow">
            <span className="mr-2">✨</span> Welcome to the future of play
          </div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tighter mb-2 leading-tight">
            Design. <span className="text-transparent bg-clip-text bg-gradient-to-r from-lively-orange to-lively-yellow">Play.</span> <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-400 to-lively-pink">Innovate.</span>
          </h1>
          <p className="text-lg md:text-xl font-light text-slate-200 max-w-2xl mx-auto leading-relaxed">
            AI-Tracks Studio brings you immersive mini-games and cutting-edge web demos driven by vibrant creativity.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <Link
              to="/game"
              className="px-6 py-3 bg-gradient-to-r from-accent-600 to-accent-500 hover:from-accent-500 hover:to-accent-400 text-white rounded-full font-bold text-base transition-all transform hover:scale-105 shadow-xl hover:shadow-accent-500/25 flex items-center justify-center gap-2"
            >
              Explore Games <Star size={18} fill="currentColor" />
            </Link>
            <Link
              to="/website"
              className="px-6 py-3 bg-white/10 hover:bg-white/20 backdrop-blur-md text-white border border-white/30 rounded-full font-bold text-base transition-all transform hover:scale-105 shadow-xl flex items-center justify-center gap-2"
            >
              View Demos <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </div>

      {/* Featured Section */}
      <div className="py-24 bg-slate-50 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-accent-500/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-lively-pink/5 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="flex flex-col md:flex-row justify-between items-end mb-16 gap-4">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
                Featured <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-600 to-lively-pink">Experiences</span>
              </h2>
              <p className="text-slate-600 text-lg max-w-xl">Check out our latest releases and most popular web experiments.</p>
            </div>
            <Link to="/game" className="hidden md:flex items-center gap-2 text-accent-600 font-bold hover:text-accent-700 transition-colors text-lg group">
              View All Games <ArrowRight size={24} className="group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          {loading ? (
            <LoadingSpinner message="Loading featured games..." />
          ) : error ? (
            <ErrorMessage message={error} />
          ) : featuredGames.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-slate-600 text-lg">No games available yet.</p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {featuredGames.map((game) => (
                  <Link to="/game" key={game.id} className="group relative rounded-3xl overflow-hidden aspect-[4/5] shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2">
                    <img src={getImageUrl(game.image)} alt={game.title} className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" />
                    <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/20 to-transparent opacity-90"></div>
                    <div className="absolute bottom-0 left-0 p-8 w-full">
                      <div className="mb-3">
                        <span className="px-3 py-1 rounded-full bg-accent-500 text-white text-xs font-bold uppercase tracking-wider shadow-lg">
                          {game.category}
                        </span>
                      </div>
                      <h3 className="text-white text-2xl font-bold">{game.title}</h3>
                    </div>
                  </Link>
                ))}
              </div>

              <div className="mt-12 text-center md:hidden">
                <Link to="/game" className="inline-flex items-center gap-2 text-accent-600 font-bold text-lg">
                  View All Games <ArrowRight size={20} />
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </>
  );
};

// Page components that fetch data for games and websites
const GamesPage: React.FC = () => {
  const [games, setGames] = useState<ProjectItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // SEO
  useSEO(
    generatePageSEO(
      'Game Projects',
      'Explore our collection of interactive games and gaming experiences powered by AI. From puzzle games to action adventures, discover innovative gameplay mechanics.',
      { 
        canonical: 'https://studio.ai-tracks.com/game',
        keywords: 'games, interactive games, web games, AI games, mini games, browser games',
        ogType: 'website'
      }
    )
  );

  const fetchGames = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await projectsApi.getGames();
      setGames(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load games');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGames();
  }, []);

  return (
    <>
      <SectionHero
        title="Game Projects"
        subtitle="Explore our collection of interactive experiences and mini-games."
        bgImage={HERO_IMAGES.games}
        overlayColor="from-indigo-900/90 to-accent-800/80"
      />
      {loading ? (
        <LoadingSpinner message="Loading games..." />
      ) : error ? (
        <ErrorMessage message={error} onRetry={fetchGames} />
      ) : (
        <ItemGrid items={games} title="All Games" itemsPerPage={9} />
      )}
    </>
  );
};

const WebsitesPage: React.FC = () => {
  const [websites, setWebsites] = useState<ProjectItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // SEO
  useSEO(
    generatePageSEO(
      'Web Demos',
      'Discover our portfolio of responsive, high-performance web applications and demos. Explore cutting-edge web development techniques and innovative UI/UX designs.',
      { 
        canonical: 'https://studio.ai-tracks.com/website',
        keywords: 'web demos, web development, responsive design, UI/UX, web applications, prototypes',
        ogType: 'website'
      }
    )
  );

  const fetchWebsites = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await projectsApi.getWebsites();
      setWebsites(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load websites');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWebsites();
  }, []);

  return (
    <>
      <SectionHero
        title="Web Demos"
        subtitle="A showcase of responsive, high-performance web development."
        bgImage={HERO_IMAGES.websites}
        overlayColor="from-blue-900/90 to-cyan-800/80"
      />
      {loading ? (
        <LoadingSpinner message="Loading websites..." />
      ) : error ? (
        <ErrorMessage message={error} onRetry={fetchWebsites} />
      ) : (
        <ItemGrid items={websites} title="Website Prototypes" itemsPerPage={9} />
      )}
    </>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/game" element={<GamesPage />} />
          <Route path="/game/:id" element={<ProjectDetail />} />
          <Route path="/website" element={<WebsitesPage />} />
          <Route path="/website/:id" element={<ProjectDetail />} />
          <Route path="/news" element={<NewsPage />} />
          <Route path="/news/:id" element={<NewsDetail />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
