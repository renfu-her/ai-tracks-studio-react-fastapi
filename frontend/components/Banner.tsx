import React, { useState, useEffect } from 'react';
import { bannerApi, PageType } from '../api/banner';
import { Loader2 } from 'lucide-react';

interface BannerProps {
  pageType: PageType;
  className?: string;
}

export const Banner: React.FC<BannerProps> = ({ pageType, className = '' }) => {
  const [bannerImage, setBannerImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBanner = async () => {
      setLoading(true);
      try {
        const banner = await bannerApi.getBannerByPageType(pageType);
        if (banner) {
          const imageUrl = bannerApi.getBannerImageUrl(banner);
          setBannerImage(imageUrl);
        } else {
          setBannerImage(null);
        }
      } catch (error) {
        console.error('Failed to load banner:', error);
        setBannerImage(null);
      } finally {
        setLoading(false);
      }
    };

    fetchBanner();
  }, [pageType]);

  // Don't render anything if no banner or still loading
  if (loading) {
    return null; // Or return a loading placeholder if needed
  }

  if (!bannerImage) {
    return null;
  }

  return (
    <div className={`relative w-full ${className}`}>
      <div className="relative w-full h-[300px] md:h-[400px] overflow-hidden">
        <img
          src={bannerImage}
          alt={`${pageType} Banner`}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-black/20" />
      </div>
    </div>
  );
};

