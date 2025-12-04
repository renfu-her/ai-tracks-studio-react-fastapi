import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ProjectItem } from '../types';
import { ArrowRight, Calendar, Tag } from 'lucide-react';
import { getImageUrl } from '../api/config';

interface ItemGridProps {
  items: ProjectItem[];
  title: string;
  itemsPerPage?: number;
}

export const ItemGrid: React.FC<ItemGridProps> = ({ items, title, itemsPerPage = 9 }) => {
  // Simple mock pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = Math.ceil(items.length / itemsPerPage);
  
  const displayItems = items.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto bg-slate-50">
      <div className="text-center mb-16">
        <h2 className="text-4xl font-bold text-slate-800 mb-4 inline-block relative">
          {title}
          <span className="absolute -bottom-2 left-0 w-full h-1 bg-gradient-to-r from-accent-500 to-transparent"></span>
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {displayItems.map((item) => {
          const detailPath = item.category === 'GAME' ? `/game/${item.id}` : `/website/${item.id}`;
          
          return (
            <Link
              key={item.id}
              to={detailPath}
              className="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 border border-slate-100 block"
            >
              {/* Image Container */}
              <div className="relative h-56 overflow-hidden">
                <img 
                  src={getImageUrl(item.image)} 
                  alt={item.title} 
                  className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <span className="bg-white text-slate-900 px-6 py-2 rounded-full font-bold transform translate-y-4 group-hover:translate-y-0 transition-all duration-300 shadow-lg">
                    View Details
                  </span>
                </div>
                <div className="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-bold text-accent-600 shadow-sm">
                  {item.category}
                </div>
              </div>

            {/* Content */}
            <div className="p-6">
              <div className="flex gap-2 mb-3 flex-wrap">
                {item.tags.map(tag => (
                  <span key={tag} className="text-xs px-2 py-1 bg-slate-100 text-slate-600 rounded-md font-medium">
                    #{tag}
                  </span>
                ))}
              </div>
              <h3 className="text-xl font-bold text-slate-800 mb-4 group-hover:text-accent-600 transition-colors">
                {item.title}
              </h3>
              
              <div className="flex items-center justify-between pt-4 border-t border-slate-100">
                <div className="flex items-center text-slate-400 text-xs gap-1">
                  <Calendar size={14} />
                  {item.date}
                </div>
                <div className="text-accent-500 font-semibold text-sm flex items-center gap-1 group/link">
                  Learn More <ArrowRight size={16} className="group-hover/link:translate-x-1 transition-transform" />
                </div>
              </div>
            </div>
          </Link>
          );
        })}
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="mt-16 flex justify-center gap-2">
          {Array.from({ length: totalPages }).map((_, idx) => (
            <button
              key={idx}
              onClick={() => setCurrentPage(idx + 1)}
              className={`w-10 h-10 rounded-full flex items-center justify-center font-bold transition-all ${
                currentPage === idx + 1
                  ? 'bg-accent-600 text-white shadow-lg scale-110'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              {idx + 1}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};