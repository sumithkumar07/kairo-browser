import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Globe, 
  Zap, 
  MousePointer2, 
  ArrowRight, 
  Bot,
  Search,
  Shield,
  Sparkles
} from 'lucide-react';
import LocalFirstDetector from './LocalFirstDetector';

const WelcomePage = ({ onStartBrowsing }) => {
  const [isHovering, setIsHovering] = useState(null);

  const features = [
    {
      id: 'browser',
      icon: Globe,
      iconBg: 'bg-green-100',
      iconColor: 'text-green-600',
      title: 'Enhanced Browser',
      description: 'Advanced browser engine with multiple tabs, bookmarks, and modern features',
      details: [
        'Multi-tab browsing support',
        'Bookmark management', 
        'Enhanced proxy routing',
        'Fullscreen mode & settings'
      ]
    },
    {
      id: 'ai',
      icon: Bot,
      iconBg: 'bg-blue-100', 
      iconColor: 'text-blue-600',
      title: 'Smart AI Assistant',
      description: 'Enhanced AI with context awareness and advanced commands',
      details: [
        'Advanced natural language processing',
        'Context-aware responses',
        'Quick command shortcuts',
        'Multi-session memory'
      ]
    },
    {
      id: 'interaction',
      icon: MousePointer2,
      iconBg: 'bg-purple-100',
      iconColor: 'text-purple-600', 
      title: 'Advanced Interactivity',
      description: 'Enhanced browsing with modern UI, gestures, and controls',
      details: [
        'Touch and gesture support',
        'Keyboard shortcuts',
        'Voice commands (coming soon)',
        'Smart form completion'
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-green-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-lg flex items-center justify-center">
                <Globe className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">Kairo AI</span>
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-600">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>AI Online</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="w-4 h-4" />
                <span>Secure</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <div className="flex justify-center mb-6">
            <div className="relative">
              <div className="w-20 h-20 bg-gradient-to-br from-green-400 via-green-500 to-green-600 rounded-2xl flex items-center justify-center shadow-kairo">
                <Sparkles className="w-10 h-10 text-white" />
              </div>
              <div className="absolute -top-2 -right-2 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                <Bot className="w-3 h-3 text-white" />
              </div>
            </div>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
            Welcome to <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-500 to-green-700">Kairo AI</span>
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Your Enhanced AI Assistant with Advanced Browser Engine
          </p>
          
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5, duration: 0.6 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <button
              onClick={onStartBrowsing}
              className="group bg-gradient-to-r from-green-500 to-green-600 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-300 hover:from-green-600 hover:to-green-700 hover:shadow-kairo-hover flex items-center space-x-2"
            >
              <span>Start Browsing</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
            
            <div className="text-sm text-gray-500 flex items-center space-x-2">
              <Search className="w-4 h-4" />
              <span>No setup required • Start immediately</span>
            </div>
          </motion.div>
        </motion.div>

        {/* Features Grid */}
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="grid md:grid-cols-3 gap-8 mb-16"
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 + index * 0.1, duration: 0.6 }}
              onMouseEnter={() => setIsHovering(feature.id)}
              onMouseLeave={() => setIsHovering(null)}
              className="feature-card bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl border border-gray-100 group cursor-pointer"
            >
              <div className="flex flex-col items-center text-center">
                <div className={`w-16 h-16 ${feature.iconBg} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className={`w-8 h-8 ${feature.iconColor}`} />
                </div>
                
                <h3 className="text-2xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 mb-6 leading-relaxed">{feature.description}</p>
                
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ 
                    height: isHovering === feature.id ? 'auto' : 0,
                    opacity: isHovering === feature.id ? 1 : 0
                  }}
                  transition={{ duration: 0.3 }}
                  className="overflow-hidden"
                >
                  <ul className="space-y-2 text-sm text-gray-500">
                    {feature.details.map((detail, idx) => (
                      <li key={idx} className="flex items-center space-x-2">
                        <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
                        <span>{detail}</span>
                      </li>
                    ))}
                  </ul>
                </motion.div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Getting Started Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="bg-gradient-to-r from-green-50 to-blue-50 rounded-3xl p-8 md:p-12 text-center"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Get started by opening the AI Assistant
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            Click the <span className="inline-flex items-center mx-1 px-2 py-1 bg-green-100 text-green-700 rounded-lg font-medium">
              <Bot className="w-4 h-4 mr-1" />
              AI
            </span> button in the bottom right
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
            <div className="bg-white p-6 rounded-2xl shadow-md">
              <h3 className="font-semibold text-gray-900 mb-2">Try these commands:</h3>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="bg-gray-50 px-3 py-2 rounded-lg">"Open YouTube"</div>
                <div className="bg-gray-50 px-3 py-2 rounded-lg">"Search for AI news"</div>
                <div className="bg-gray-50 px-3 py-2 rounded-lg">"Navigate to Google"</div>
              </div>
            </div>
            
            <ArrowRight className="w-6 h-6 text-gray-400 rotate-90 sm:rotate-0" />
            
            <div className="bg-white p-6 rounded-2xl shadow-md">
              <h3 className="font-semibold text-gray-900 mb-2">AI will:</h3>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-center space-x-2">
                  <Zap className="w-4 h-4 text-yellow-500" />
                  <span>Understand your request</span>
                </div>
                <div className="flex items-center space-x-2">
                  <MousePointer2 className="w-4 h-4 text-blue-500" />
                  <span>Execute browser actions</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Globe className="w-4 h-4 text-green-500" />
                  <span>Navigate to the website</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-100 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500">
            <p>&copy; 2025 Kairo AI Browser. Built with AI-powered automation.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default WelcomePage;