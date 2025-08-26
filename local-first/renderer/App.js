import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Bot, Globe, Settings, Minimize2, Maximize2, X, Home, ArrowLeft, ArrowRight, RotateCcw, Star } from 'lucide-react';
import './App.css';

function App() {
  // State management
  const [isLocalFirst, setIsLocalFirst] = useState(false);
  const [currentUrl, setCurrentUrl] = useState('');
  const [pageTitle, setPageTitle] = useState('Kairo AI Browser');
  const [aiChatOpen, setAiChatOpen] = useState(false);
  const [aiMessages, setAiMessages] = useState([]);
  const [aiInput, setAiInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [navigationHistory, setNavigationHistory] = useState([]);
  const [currentHistoryIndex, setCurrentHistoryIndex] = useState(-1);
  const [systemInfo, setSystemInfo] = useState(null);

  // Initialize local-first detection
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Check if running in Electron
        if (window.kairoAPI && window.kairoAPI.system) {
          const info = await window.kairoAPI.system.getInfo();
          setSystemInfo(info.system);
          setIsLocalFirst(true);
          console.log('🚀 Local-First Mode Activated');
          
          // Listen for Chromium ready event
          window.kairoAPI.on('chromium-ready', (event, data) => {
            if (data.success) {
              console.log('✅ Embedded Chromium Ready');
            } else {
              console.error('❌ Chromium initialization failed:', data.error);
            }
          });
        } else {
          console.log('🌐 Web fallback mode');
        }
      } catch (error) {
        console.error('Initialization error:', error);
      }
    };

    initializeApp();
  }, []);

  // Navigation functions
  const navigateToUrl = useCallback(async (url) => {
    if (!url) return;
    
    // Ensure proper URL format
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = 'https://' + url;
    }

    setIsLoading(true);
    try {
      if (isLocalFirst && window.kairoAPI) {
        const result = await window.kairoAPI.browser.navigate(url);
        if (result.success) {
          setCurrentUrl(result.url);
          setPageTitle(result.title);
          
          // Update navigation history
          const newHistory = navigationHistory.slice(0, currentHistoryIndex + 1);
          newHistory.push({ url: result.url, title: result.title });
          setNavigationHistory(newHistory);
          setCurrentHistoryIndex(newHistory.length - 1);
        }
      } else {
        // Web fallback
        setCurrentUrl(url);
        setPageTitle('Loading...');
      }
    } catch (error) {
      console.error('Navigation error:', error);
    } finally {
      setIsLoading(false);
    }
  }, [isLocalFirst, navigationHistory, currentHistoryIndex]);

  // AI chat functions
  const handleAIQuery = useCallback(async (query) => {
    if (!query.trim()) return;

    const userMessage = { role: 'user', content: query, timestamp: new Date() };
    setAiMessages(prev => [...prev, userMessage]);
    setAiInput('');
    setIsLoading(true);

    try {
      if (isLocalFirst && window.kairoAPI) {
        const result = await window.kairoAPI.ai.query(query, {
          currentUrl,
          pageTitle
        });
        
        if (result.success) {
          const aiMessage = { 
            role: 'assistant', 
            content: result.response.explanation,
            commands: result.response.commands,
            timestamp: new Date() 
          };
          setAiMessages(prev => [...prev, aiMessage]);

          // Execute commands if present
          if (result.response.commands && result.response.commands.length > 0) {
            for (const command of result.response.commands) {
              try {
                await window.kairoAPI.browser.execute(command.type, command.params);
              } catch (error) {
                console.error('Command execution error:', error);
              }
            }
          }
        }
      } else {
        // Web fallback
        const aiMessage = { 
          role: 'assistant', 
          content: `I understand you want to: "${query}". In local-first mode, I can execute this directly on websites. Currently running in web fallback mode.`,
          timestamp: new Date() 
        };
        setAiMessages(prev => [...prev, aiMessage]);
      }
    } catch (error) {
      console.error('AI query error:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error processing your request.',
        timestamp: new Date() 
      };
      setAiMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [isLocalFirst, currentUrl, pageTitle]);

  // Quick navigation shortcuts
  const quickNavigate = (site) => {
    const urls = {
      youtube: 'https://youtube.com',
      google: 'https://google.com',
      github: 'https://github.com',
      netflix: 'https://netflix.com'
    };
    navigateToUrl(urls[site]);
  };

  // Window controls (for Electron)
  const handleMinimize = () => window.kairoAPI?.window.minimize();
  const handleMaximize = () => window.kairoAPI?.window.maximize();
  const handleClose = () => window.kairoAPI?.window.close();

  return (
    <div className="app-container min-h-screen bg-gray-900 text-white flex flex-col">
      {/* Title Bar (Electron) */}
      {isLocalFirst && (
        <div className="title-bar bg-gray-800 px-4 py-2 flex items-center justify-between select-none">
          <div className="flex items-center space-x-2">
            <Globe className="w-5 h-5 text-blue-400" />
            <span className="font-semibold">Kairo AI Browser</span>
            <span className="text-xs text-green-400 bg-green-400/20 px-2 py-1 rounded">LOCAL-FIRST</span>
          </div>
          <div className="flex items-center space-x-1">
            <button onClick={handleMinimize} className="p-2 hover:bg-gray-700 rounded">
              <Minimize2 className="w-4 h-4" />
            </button>
            <button onClick={handleMaximize} className="p-2 hover:bg-gray-700 rounded">
              <Maximize2 className="w-4 h-4" />
            </button>
            <button onClick={handleClose} className="p-2 hover:bg-red-600 rounded">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* Navigation Bar */}
      <div className="nav-bar bg-gray-800 px-4 py-3 border-b border-gray-700">
        <div className="flex items-center space-x-4">
          {/* Navigation Controls */}
          <div className="flex items-center space-x-2">
            <button 
              className="p-2 hover:bg-gray-700 rounded disabled:opacity-50"
              disabled={currentHistoryIndex <= 0}
              onClick={() => {
                if (currentHistoryIndex > 0) {
                  const prevIndex = currentHistoryIndex - 1;
                  const prevPage = navigationHistory[prevIndex];
                  setCurrentHistoryIndex(prevIndex);
                  navigateToUrl(prevPage.url);
                }
              }}
            >
              <ArrowLeft className="w-4 h-4" />
            </button>
            <button 
              className="p-2 hover:bg-gray-700 rounded disabled:opacity-50"
              disabled={currentHistoryIndex >= navigationHistory.length - 1}
              onClick={() => {
                if (currentHistoryIndex < navigationHistory.length - 1) {
                  const nextIndex = currentHistoryIndex + 1;
                  const nextPage = navigationHistory[nextIndex];
                  setCurrentHistoryIndex(nextIndex);
                  navigateToUrl(nextPage.url);
                }
              }}
            >
              <ArrowRight className="w-4 h-4" />
            </button>
            <button 
              className="p-2 hover:bg-gray-700 rounded"
              onClick={() => navigateToUrl(currentUrl)}
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>

          {/* URL Bar */}
          <div className="flex-1 flex items-center">
            <input
              type="text"
              value={currentUrl}
              onChange={(e) => setCurrentUrl(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && navigateToUrl(currentUrl)}
              placeholder="Enter URL or search..."
              className="flex-1 bg-gray-900 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-blue-500 focus:outline-none"
            />
            <button
              onClick={() => navigateToUrl(currentUrl)}
              className="ml-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
              disabled={isLoading}
            >
              {isLoading ? '...' : 'Go'}
            </button>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setAiChatOpen(true)}
              className="p-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
              title="Open AI Assistant"
            >
              <Bot className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Quick Navigation */}
        <div className="flex items-center space-x-2 mt-3">
          <span className="text-sm text-gray-400">Quick Access:</span>
          <button onClick={() => quickNavigate('youtube')} className="px-3 py-1 bg-red-600/20 text-red-400 rounded hover:bg-red-600/30 transition-colors">
            YouTube
          </button>
          <button onClick={() => quickNavigate('google')} className="px-3 py-1 bg-blue-600/20 text-blue-400 rounded hover:bg-blue-600/30 transition-colors">
            Google
          </button>
          <button onClick={() => quickNavigate('github')} className="px-3 py-1 bg-gray-600/20 text-gray-400 rounded hover:bg-gray-600/30 transition-colors">
            GitHub
          </button>
          <button onClick={() => quickNavigate('netflix')} className="px-3 py-1 bg-red-600/20 text-red-400 rounded hover:bg-red-600/30 transition-colors">
            Netflix
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex">
        {/* Browser Content */}
        <div className="flex-1 bg-white">
          {isLocalFirst ? (
            <div className="h-full flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
              <div className="text-center p-8">
                <Globe className="w-16 h-16 text-blue-600 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">Embedded Browser Ready</h2>
                <p className="text-gray-600 mb-4">
                  Native Chromium browser with full website access.<br/>
                  No proxy restrictions - YouTube, Netflix, banking sites all work perfectly.
                </p>
                <p className="text-sm text-gray-500">
                  Current URL: {currentUrl || 'None'}
                </p>
                {systemInfo && (
                  <div className="mt-4 text-xs text-gray-400">
                    <p>Platform: {systemInfo.platform} | Memory: {systemInfo.memory}GB</p>
                    <p>Electron: {systemInfo.electron} | Chrome: {systemInfo.chrome}</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center bg-gray-100">
              <div className="text-center p-8">
                <Globe className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">Web Fallback Mode</h2>
                <p className="text-gray-600">
                  For full functionality, please use the desktop application.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* AI Chat Sidebar */}
      <AnimatePresence>
        {aiChatOpen && (
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            className="fixed right-0 top-0 h-full w-96 bg-gray-800 border-l border-gray-700 flex flex-col"
          >
            {/* Chat Header */}
            <div className="p-4 border-b border-gray-700 flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Bot className="w-6 h-6 text-green-400" />
                <span className="font-semibold">AI Assistant</span>
                {isLocalFirst && <span className="text-xs text-green-400">LOCAL</span>}
              </div>
              <button
                onClick={() => setAiChatOpen(false)}
                className="p-1 hover:bg-gray-700 rounded"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {aiMessages.length === 0 ? (
                <div className="text-center text-gray-400 py-8">
                  <Bot className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>Ask me to help you browse the web!</p>
                  <div className="mt-4 space-y-2 text-sm">
                    <p className="text-green-400">Try saying:</p>
                    <p>"Open YouTube and play AI tutorials"</p>
                    <p>"Navigate to Google and search for weather"</p>
                    <p>"Take me to Netflix"</p>
                  </div>
                </div>
              ) : (
                aiMessages.map((message, index) => (
                  <div key={index} className={`${message.role === 'user' ? 'ml-8' : 'mr-8'}`}>
                    <div className={`p-3 rounded-lg ${
                      message.role === 'user' 
                        ? 'bg-blue-600 text-white ml-auto' 
                        : 'bg-gray-700 text-gray-100'
                    }`}>
                      <p className="text-sm">{message.content}</p>
                      {message.commands && message.commands.length > 0 && (
                        <div className="mt-2 text-xs opacity-75">
                          <p>Executing {message.commands.length} action(s)...</p>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
              {isLoading && (
                <div className="mr-8">
                  <div className="bg-gray-700 text-gray-100 p-3 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-400"></div>
                      <span className="text-sm">Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Chat Input */}
            <div className="p-4 border-t border-gray-700">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={aiInput}
                  onChange={(e) => setAiInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleAIQuery(aiInput)}
                  placeholder="Ask me to do something..."
                  className="flex-1 bg-gray-900 text-white px-3 py-2 rounded border border-gray-600 focus:border-green-500 focus:outline-none"
                  disabled={isLoading}
                />
                <button
                  onClick={() => handleAIQuery(aiInput)}
                  disabled={isLoading || !aiInput.trim()}
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 rounded transition-colors"
                >
                  Send
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;