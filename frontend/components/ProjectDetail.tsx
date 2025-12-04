import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { projectsApi } from '../api';
import { getImageUrl } from '../api/config';
import { ProjectItem } from '../types';
import { ArrowLeft, Calendar, Tag, ExternalLink, Loader2, AlertCircle } from 'lucide-react';
import { MarkdownContent } from './MarkdownContent';

export const ProjectDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<ProjectItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProject = async () => {
      if (!id) {
        setError('Project ID is missing');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        const data = await projectsApi.getProject(id);
        setProject(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load project details');
      } finally {
        setLoading(false);
      }
    };

    fetchProject();
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-16 h-16 text-accent-500 animate-spin mx-auto mb-4" />
          <p className="text-slate-600 text-lg">Loading project details...</p>
        </div>
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-slate-900 mb-2">Error</h2>
          <p className="text-slate-600 mb-6">{error || 'Project not found'}</p>
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

  const backLink = project.category === 'GAME' ? '/game' : '/website';
  const backText = project.category === 'GAME' ? 'All Games' : 'All Websites';

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
      {/* Header with back button */}
      <div className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link
            to={backLink}
            className="inline-flex items-center gap-2 text-slate-600 hover:text-accent-600 transition-colors group"
          >
            <ArrowLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
            <span className="font-medium">{backText}</span>
          </Link>
        </div>
      </div>

      {/* Hero Section */}
      <div className="relative h-96 overflow-hidden">
        <img
          src={getImageUrl(project.image)}
          alt={project.title}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/50 to-transparent"></div>
        
        {/* Category Badge */}
        <div className="absolute top-8 right-8">
          <span className="px-4 py-2 rounded-full bg-accent-500 text-white text-sm font-bold uppercase tracking-wider shadow-lg">
            {project.category}
          </span>
        </div>

        {/* Title */}
        <div className="absolute bottom-0 left-0 right-0 p-8">
          <div className="max-w-7xl mx-auto">
            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
              {project.title}
            </h1>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Description */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">About This Project</h2>
              {project.description ? (
                <MarkdownContent content={project.description} />
              ) : (
                <p className="text-slate-500 italic">No description available.</p>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Project Info Card */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 space-y-4">
              <h3 className="text-lg font-bold text-slate-900">Project Details</h3>

              {/* Date */}
              {project.date && (
                <div className="flex items-start gap-3">
                  <Calendar className="w-5 h-5 text-accent-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium text-slate-900">Date</p>
                    <p className="text-sm text-slate-600">{project.date}</p>
                  </div>
                </div>
              )}

              {/* Tags */}
              {project.tags && project.tags.length > 0 && (
                <div className="flex items-start gap-3">
                  <Tag className="w-5 h-5 text-accent-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-slate-900 mb-2">Tags</p>
                    <div className="flex flex-wrap gap-2">
                      {project.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-medium"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* External Link */}
              {project.link && (
                <div className="pt-4 border-t border-slate-100">
                  <a
                    href={project.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center gap-2 w-full px-4 py-3 bg-gradient-to-r from-accent-600 to-accent-500 hover:from-accent-500 hover:to-accent-400 text-white rounded-lg font-semibold transition-all shadow-md hover:shadow-lg transform hover:scale-105"
                  >
                    <ExternalLink className="w-5 h-5" />
                    View Live Project
                  </a>
                </div>
              )}
            </div>

            {/* Share Card (Optional) */}
            <div className="bg-gradient-to-br from-accent-50 to-purple-50 rounded-2xl border border-accent-100 p-6">
              <h3 className="text-lg font-bold text-slate-900 mb-2">Like this project?</h3>
              <p className="text-sm text-slate-600 mb-4">
                Check out our other {project.category === 'GAME' ? 'games' : 'websites'} for more inspiration!
              </p>
              <Link
                to={backLink}
                className="inline-flex items-center gap-2 text-accent-600 hover:text-accent-700 font-semibold text-sm group"
              >
                Browse More
                <ArrowLeft className="w-4 h-4 rotate-180 group-hover:translate-x-1 transition-transform" />
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

