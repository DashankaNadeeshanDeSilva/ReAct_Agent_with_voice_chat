import React from 'react';
import { Link } from 'react-router-dom';
import { MessageSquare, Upload, Database, Search, Zap, Shield } from 'lucide-react';

const LandingPage: React.FC = () => {
  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-4xl mx-auto">
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
          Your <span className="text-blue-600">Smart</span> Document Assistant <span className="text-blue-600">Agent</span>
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Upload your documents and chat with Agentic RAG to get instant, accurate answers based on your own content.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">
          <Link 
            to="/chat" 
            className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors duration-200 shadow-sm"
          >
            <MessageSquare className="mr-2 h-5 w-5" />
            Start Chatting
          </Link>
          <Link 
            to="/upload" 
            className="inline-flex items-center justify-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50 transition-colors duration-200 shadow-sm"
          >
            <Upload className="mr-2 h-5 w-5" />
            Upload Documents
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-6xl mx-auto">
        <h2 className="text-2xl md:text-3xl font-bold text-center text-gray-900 mb-12">
          How It Works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
            <div className="rounded-full bg-blue-100 w-12 h-12 flex items-center justify-center mb-4">
              <Upload className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Upload Your Documents</h3>
            <p className="text-gray-600">
              Upload any PDF, Word, or text documents that contain the information you want to chat with.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
            <div className="rounded-full bg-green-100 w-12 h-12 flex items-center justify-center mb-4">
              <Database className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Intelligent Indexing</h3>
            <p className="text-gray-600">
              Our system processes and indexes your documents for optimized retrieval and understanding.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow duration-200">
            <div className="rounded-full bg-purple-100 w-12 h-12 flex items-center justify-center mb-4">
              <MessageSquare className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Chat & Get Answers</h3>
            <p className="text-gray-600">
              Ask questions in natural language and get answers based directly on your documents.
            </p>
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="max-w-6xl mx-auto">
        <h2 className="text-2xl md:text-3xl font-bold text-center text-gray-900 mb-12">
          Key Benefits
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex items-start space-x-4">
            <div className="rounded-full bg-amber-100 w-10 h-10 flex items-center justify-center flex-shrink-0">
              <Search className="h-5 w-5 text-amber-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">Instant Information Retrieval</h3>
              <p className="text-gray-600">
                Find information in seconds that would take hours to manually search through documents.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="rounded-full bg-blue-100 w-10 h-10 flex items-center justify-center flex-shrink-0">
              <Zap className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">Enhanced Productivity</h3>
              <p className="text-gray-600">
                Get precise answers quickly without having to skim through lengthy documents.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="rounded-full bg-green-100 w-10 h-10 flex items-center justify-center flex-shrink-0">
              <Shield className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">Data Privacy</h3>
              <p className="text-gray-600">
                Your documents stay private and secure, with no data shared with external sources.
              </p>
            </div>
          </div>

          <div className="flex items-start space-x-4">
            <div className="rounded-full bg-purple-100 w-10 h-10 flex items-center justify-center flex-shrink-0">
              <MessageSquare className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">Contextual Conversations</h3>
              <p className="text-gray-600">
                Have natural conversations with your documents, with the system understanding context.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 text-white rounded-xl p-8 md:p-12 text-center max-w-5xl mx-auto">
        <h2 className="text-2xl md:text-3xl font-bold mb-4">
          Ready to Get Started?
        </h2>
        <p className="text-blue-100 mb-8 max-w-xl mx-auto">
          Upload your first document and experience the power of intelligent document chat.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Link 
            to="/upload" 
            className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-blue-50 transition-colors duration-200 shadow-sm"
          >
            <Upload className="mr-2 h-5 w-5" />
            Upload Your First Document
          </Link>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;