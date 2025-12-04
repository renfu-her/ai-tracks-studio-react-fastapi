import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { newsApi } from '../api';
import { getImageUrl, API_CONFIG } from '../api/config';
import { NewsItem } from '../types';
import { ArrowLeft, Calendar, User, Loader2, AlertCircle } from 'lucide-react';
import { MarkdownContent } from './MarkdownContent';
import { useSEO } from '../hooks/useSEO';
import { generateArticleData } from '../utils/seo';

export const NewsDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [news, setNews] = useState<NewsItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      if (!id) {
        setError('News ID is missing');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const data = await newsApi.getNewsItem(id);
        setNews(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load news article');
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, [id]);

  // Dynamic SEO based on news data
  useSEO(
    news ? {
      title: `${news.title} | AI-Tracks Studio News`,
      description: news.excerpt.substring(0, 160) || `Read ${news.title} on AI-Tracks Studio blog.`,
      keywords: `news, article, blog, ${news.title}, AI-Tracks Studio`,
      canonical: `https://studio.ai-tracks.com/news/${news.id}`,
      ogTitle: news.title,
      ogDescription: news.excerpt.substring(0, 160),
      ogImage: news.image ? `${API_CONFIG.BASE_URL}/backend/static/uploads/${news.image}` : undefined,
      ogType: 'article',
      ogUrl: `https://studio.ai-tracks.com/news/${news.id}`,
    } : {
      title: 'Loading Article | AI-Tracks Studio',
      description: 'Loading article...',
    },
    news ? generateArticleData({
      title: news.title,
      description: news.excerpt,
      image: news.image ? `${API_CONFIG.BASE_URL}/backend/static/uploads/${news.image}` : undefined,
      datePublished: news.date,
      author: news.author,
    }) : undefined
  );

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-16 h-16 text-accent-500 animate-spin mx-auto mb-4" />
          <p className="text-slate-600 text-lg">Loading article...</p>
        </div>
      </div>
    );
  }

  if (error || !news) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-900 mb-2">Error</h2>
          <p className="text-slate-600 mb-6">{error || 'Article not found'}</p>
          <button
            onClick={() => navigate(-1)}
            className="px-6 py-3 bg-accent-600 hover:bg-accent-700 text-white rounded-lg font-semibold transition-colors"
          >
            Go Back
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Header with back button */}
      <div className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link
            to="/news"
            className="inline-flex items-center gap-2 text-slate-600 hover:text-accent-600 transition-colors group"
          >
            <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            <span className="font-medium">All News</span>
          </Link>
        </div>
      </div>

      {/* Article Content */}
      <article className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Image */}
        {news.image && (
          <div className="relative h-96 rounded-2xl overflow-hidden mb-8 shadow-xl">
            <img
              src={getImageUrl(news.image)}
              alt={news.title}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/50 to-transparent"></div>
          </div>
        )}

        {/* Article Header */}
        <header className="mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4 leading-tight">
            {news.title}
          </h1>

          {/* Meta Information */}
          <div className="flex flex-wrap items-center gap-4 text-slate-600">
            {news.date && (
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5" />
                <time dateTime={news.date}>
                  {new Date(news.date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  })}
                </time>
              </div>
            )}
            {news.author && (
              <div className="flex items-center gap-2">
                <User className="w-5 h-5" />
                <span>{news.author}</span>
              </div>
            )}
          </div>
        </header>

        {/* Article Excerpt */}
        {news.excerpt && (
          <div className="bg-accent-50 border-l-4 border-accent-500 p-6 rounded-r-lg mb-8">
            <div className="text-lg text-slate-700 leading-relaxed">
              <MarkdownContent content={news.excerpt} />
            </div>
          </div>
        )}

        {/* Article Content */}
        <div className="prose prose-lg max-w-none">
          {news.content ? (
            <MarkdownContent content={news.content} />
          ) : (
            <p className="text-slate-500 italic">No content available.</p>
          )}
        </div>

        {/* Back to List */}
        <div className="mt-12 pt-8 border-t border-slate-200">
          <Link
            to="/news"
            className="inline-flex items-center gap-2 text-accent-600 hover:text-accent-700 font-semibold group"
          >
            <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            Back to All News
          </Link>
        </div>
      </article>

      {/* Related News (Optional - can be added later) */}
      {/* <section className="bg-slate-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-slate-900 mb-8">Related Articles</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            // Related news cards
          </div>
        </div>
      </section> */}
    </div>
  );
};

