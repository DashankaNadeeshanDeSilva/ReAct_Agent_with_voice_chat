import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MessageSquare, Upload, BookOpen } from 'lucide-react';

const Navbar: React.FC = () => {
  const location = useLocation();
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`sticky top-0 z-10 transition-all duration-300 ${
      isScrolled ? 'bg-white shadow-md' : 'bg-transparent'
    }`}>
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2">
            <BookOpen className="h-6 w-6 text-blue-600" />
            <span className="font-semibold text-lg text-gray-900">RAG Chat</span>
          </Link>
          <div className="flex space-x-4">
            <Link 
              to="/chat"
              className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                location.pathname === '/chat' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-700 hover:bg-blue-100 hover:text-blue-600'
              }`}
            >
              <MessageSquare className="h-5 w-5 mr-1" />
              <span>Chat</span>
            </Link>
            <Link 
              to="/upload"
              className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                location.pathname === '/upload' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-700 hover:bg-blue-100 hover:text-blue-600'
              }`}
            >
              <Upload className="h-5 w-5 mr-1" />
              <span>Upload</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;