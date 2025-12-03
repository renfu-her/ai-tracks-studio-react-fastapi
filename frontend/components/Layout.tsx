import React, { useState, useEffect } from 'react';
import { Menu, X, Gamepad2, Globe, Newspaper, Home, Mail, Facebook, Twitter, Instagram, Info } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

interface LayoutProps {
  children: React.ReactNode;
}

interface NavLinkProps {
  to: string;
  children?: React.ReactNode;
  icon: any;
  active: boolean;
}

const NavLink: React.FC<NavLinkProps> = ({ to, children, icon: Icon, active }) => (
  <Link
    to={to}
    className={`flex items-center gap-2 px-4 py-2 rounded-full transition-all duration-300 font-medium ${
      active 
        ? 'bg-gradient-to-r from-accent-500 to-lively-pink text-white shadow-lg scale-105' 
        : 'text-slate-600 hover:bg-slate-100 hover:text-accent-600'
    }`}
  >
    <Icon size={18} />
    {children}
  </Link>
);

interface MobileNavLinkProps {
  to: string;
  children?: React.ReactNode;
  onClick: () => void;
  active: boolean;
}

const MobileNavLink: React.FC<MobileNavLinkProps> = ({ to, children, onClick, active }) => (
  <Link
    to={to}
    onClick={onClick}
    className={`block px-6 py-4 text-lg font-semibold border-b border-slate-100 ${
      active ? 'text-accent-600 bg-slate-50' : 'text-slate-600'
    }`}
  >
    {children}
  </Link>
);

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen flex flex-col font-sans">
      {/* Navigation */}
      <nav
        className={`fixed top-0 w-full z-50 transition-all duration-300 ${
          isScrolled ? 'bg-white/80 backdrop-blur-md shadow-md py-2' : 'bg-transparent py-4'
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="bg-gradient-to-br from-accent-500 to-lively-orange p-2 rounded-xl text-white shadow-lg group-hover:rotate-12 transition-transform duration-300">
              <Gamepad2 size={24} />
            </div>
            <span className={`text-2xl font-bold tracking-tight ${isScrolled ? 'text-slate-800' : 'text-slate-800 md:text-white'} transition-colors`}>
              AI-Tracks <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-500 to-lively-pink">Studio</span>
            </span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-2 bg-white/50 backdrop-blur-sm p-1 rounded-full border border-white/20 shadow-sm">
            <NavLink to="/" icon={Home} active={isActive('/')}>Home</NavLink>
            <NavLink to="/games" icon={Gamepad2} active={isActive('/games')}>Games</NavLink>
            <NavLink to="/websites" icon={Globe} active={isActive('/websites')}>Websites</NavLink>
            <NavLink to="/news" icon={Newspaper} active={isActive('/news')}>News</NavLink>
            <NavLink to="/about" icon={Info} active={isActive('/about')}>About</NavLink>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 text-slate-700 bg-white/80 rounded-lg backdrop-blur-sm"
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Menu Overlay */}
        {isMobileMenuOpen && (
          <div className="absolute top-full left-0 w-full bg-white shadow-xl border-t border-slate-100 flex flex-col md:hidden animate-in slide-in-from-top-5">
            <MobileNavLink to="/" onClick={() => setIsMobileMenuOpen(false)} active={isActive('/')}>Home</MobileNavLink>
            <MobileNavLink to="/games" onClick={() => setIsMobileMenuOpen(false)} active={isActive('/games')}>Games</MobileNavLink>
            <MobileNavLink to="/websites" onClick={() => setIsMobileMenuOpen(false)} active={isActive('/websites')}>Websites</MobileNavLink>
            <MobileNavLink to="/news" onClick={() => setIsMobileMenuOpen(false)} active={isActive('/news')}>News</MobileNavLink>
            <MobileNavLink to="/about" onClick={() => setIsMobileMenuOpen(false)} active={isActive('/about')}>About</MobileNavLink>
          </div>
        )}
      </nav>

      {/* Main Content */}
      <main className="flex-grow">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-white pt-16 pb-8 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <div className="bg-gradient-to-br from-accent-500 to-lively-orange p-2 rounded-lg text-white">
                  <Gamepad2 size={20} />
                </div>
                <span className="text-2xl font-bold">AI-Tracks Studio</span>
              </div>
              <p className="text-slate-400 mb-6 max-w-md">
                Pushing the boundaries of interactive entertainment and web technologies with Artificial Intelligence. 
                Experience the future of digital creativity.
              </p>
              <div className="flex gap-4">
                <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-accent-500 transition-colors">
                  <Twitter size={18} />
                </a>
                <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-lively-pink transition-colors">
                  <Instagram size={18} />
                </a>
                <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-blue-600 transition-colors">
                  <Facebook size={18} />
                </a>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-bold mb-6 text-lively-yellow">Quick Links</h3>
              <ul className="space-y-3">
                <li><Link to="/games" className="text-slate-400 hover:text-white transition-colors">Our Games</Link></li>
                <li><Link to="/websites" className="text-slate-400 hover:text-white transition-colors">Web Demos</Link></li>
                <li><Link to="/news" className="text-slate-400 hover:text-white transition-colors">Latest News</Link></li>
                <li><Link to="/about" className="text-slate-400 hover:text-white transition-colors">About Us</Link></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-bold mb-6 text-lively-orange">Contact</h3>
              <ul className="space-y-4">
                <li className="flex items-center gap-3">
                  <Mail className="text-accent-500" size={20} />
                  <a href="mailto:renfu.her@gmail.com" className="text-slate-300 hover:text-white transition-colors font-medium">
                    renfu.her@gmail.com
                  </a>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-slate-800 pt-8 text-center text-slate-500 text-sm">
            &copy; {new Date().getFullYear()} AI-Tracks Studio. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};