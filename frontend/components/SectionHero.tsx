import React from 'react';

interface SectionHeroProps {
  title: string;
  subtitle: string;
  bgImage: string;
  overlayColor?: string;
}

export const SectionHero: React.FC<SectionHeroProps> = ({ title, subtitle, bgImage, overlayColor = "from-accent-900/90 to-slate-900/80" }) => {
  return (
    <div className="relative h-[400px] flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center z-0 transform hover:scale-105 transition-transform duration-[20s]"
        style={{ backgroundImage: `url(${bgImage})` }}
      />
      
      {/* Gradient Overlay */}
      <div className={`absolute inset-0 bg-gradient-to-r ${overlayColor} z-10 backdrop-blur-[2px]`} />

      {/* Content */}
      <div className="relative z-20 text-center px-4 max-w-4xl mx-auto animate-in fade-in zoom-in duration-700">
        <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-6 drop-shadow-lg tracking-tight">
          {title}
        </h1>
        <p className="text-xl md:text-2xl text-slate-200 font-light max-w-2xl mx-auto leading-relaxed">
          {subtitle}
        </p>
        <div className="mt-8 w-24 h-1.5 bg-gradient-to-r from-lively-orange to-lively-pink mx-auto rounded-full"></div>
      </div>
    </div>
  );
};