import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Globe, Home, ArrowLeft, ArrowRight, RotateCcw, Search, Plus, X, Star,
  Settings, Shield, Wifi, WifiOff, Bot, Send, Brain, Zap, 
  Activity, Target, Layers, Cpu, CheckCircle, XCircle, Monitor
} from 'lucide-react';
import { useLocalSession } from '../contexts/LocalSessionContext';

const LocalFirstBrowserInterface = ({ onBackToWelcome }) => {
  const {
    sessionId,
    currentUrl,
    isLoading,
    isLocalFirst,
    systemStatus,
    navigateToUrl,
    processAIQuery,
    executeBrowserCommand,
    createNewTab,
    closeTab,
    getSystemStatus
  } = useLocalSession();

  // Core state
  const [tabs, setTabs] = useState([{ 
    id: sessionId || 1, 
    url: '', 
    title: 'New Tab', 
    active: true, 
    loading: false, 
    favicon: '🌐' 
  }]);
  const [activeTab, setActiveTab] = useState(sessionId || 1);
  const [urlInput, setUrlInput] = useState('');
  const [browserContent, setBrowserContent] = useState('');

  // Enhanced UI state
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showBookmarks, setShowBookmarks] = useState(false);
  const [isOnline, setIsOnline] = useState(true);

  // Chat state
  const [chatMessages, setChatMessages] = useState([
    { 
      type: 'ai', 
      content: isLocalFirst ? 
        '🚀 **Local-First AI Browser Active!**\n\n✅ Direct internet access\n✅ No proxy restrictions\n✅ Full website functionality\n✅ Better performance\n\nWhat would you like to browse?' :
        '🌐 **Browser Mode Active**\n\nRunning in server-first mode. Some websites may have restrictions.\n\nWhat would you like to browse?',
      timestamp: new Date() 
    }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const chatEndRef = useRef(null);

  // Enhanced bookmarks for local-first
  const [bookmarks, setBookmarks] = useState([
    { name: 'YouTube', url: 'https://youtube.com', favicon: '🎥' },
    { name: 'Google', url: 'https://google.com', favicon: '🔍' },
    { name: 'GitHub', url: 'https://github.com', favicon: '👨‍💻' },
    { name: 'Gmail', url: 'https://gmail.com', favicon: '📧' },
    { name: 'LinkedIn', url: 'https://linkedin.com', favicon: '💼' },
    { name: 'Twitter', url: 'https://twitter.com', favicon: '🐦' }
  ]);

  // Performance metrics
  const [performanceMetrics, setPerformanceMetrics] = useState({
    responseTime: 0,
    method: isLocalFirst ? 'local_direct' : 'server_proxy',
    mode: isLocalFirst ? 'Local-First' : 'Server-First'
  });

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  useEffect(() => {
    // Update system status periodically
    const updateStatus = async () => {
      try {
        const status = await getSystemStatus();
        setIsOnline(navigator.onLine);
      } catch (error) {
        console.error('Failed to update status:', error);
      }
    };

    updateStatus();
    const interval = setInterval(updateStatus, 30000); // Every 30 seconds
    
    return () => clearInterval(interval);
  }, [getSystemStatus]);

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    const startTime = Date.now();
    setActiveTabLoading(true);

    try {
      const result = await navigateToUrl(urlInput);
      
      if (result.success) {
        updateCurrentTab({ 
          url: result.url, 
          title: result.title || getDomainFromUrl(result.url),
          loading: false,
          favicon: getFaviconForUrl(result.url)
        });

        setBrowserContent(result.content || '');
        
        setPerformanceMetrics({
          responseTime: Date.now() - startTime,
          method: isLocalFirst ? 'local_direct' : 'server_proxy',
          mode: isLocalFirst ? 'Local-First' : 'Server-First'
        });

        setUrlInput('');
      }
    } catch (error) {
      console.error('Navigation error:', error);
      addChatMessage('ai', `❌ Navigation failed: ${error.message}`);
    } finally {
      setActiveTabLoading(false);
    }
  };

  const handleAIChat = async (e) => {
    e.preventDefault();
    if (!currentMessage.trim()) return;

    addChatMessage('user', currentMessage);
    const userMessage = currentMessage;
    setCurrentMessage('');

    try {
      const startTime = Date.now();
      const result = await processAIQuery(userMessage, {
        currentUrl,
        sessionId,
        isLocalFirst
      });

      const responseTime = Date.now() - startTime;

      if (result.success) {
        let responseText = result.aiResponse?.explanation || result.response?.explanation || 'Command processed';
        
        // Add local-first specific messaging
        if (isLocalFirst) {
          responseText += '\n\n🚀 **Local-First Benefits Active:**';
          responseText += '\n✅ Direct website access (no restrictions)';
          responseText += '\n✅ Full functionality available';
        }

        // Handle command execution results
        if (result.executionResults) {
          responseText += '\n\n**Command Results:**';
          result.executionResults.forEach(exec => {
            responseText += `\n${exec.success ? '✅' : '❌'} ${exec.command}`;
            if (exec.error) responseText += ` - ${exec.error}`;
          });
        }

        addChatMessage('ai', responseText);
        
        // Update performance metrics
        setPerformanceMetrics(prev => ({
          ...prev,
          responseTime,
          lastAIQuery: responseTime
        }));

      } else {
        addChatMessage('ai', `❌ ${result.error || 'AI processing failed'}`);
      }
    } catch (error) {
      console.error('AI chat error:', error);
      addChatMessage('ai', `❌ Error: ${error.message}`);
    }
  };

  const quickCommands = isLocalFirst ? [
    { text: 'Open YouTube and play music', icon: '🎵' },
    { text: 'Go to Gmail and check emails', icon: '📧' },
    { text: 'Search for AI news on Google', icon: '🔍' },
    { text: 'Browse GitHub trending repos', icon: '👨‍💻' },
    { text: 'Check LinkedIn messages', icon: '💼' },
    { text: 'Download latest Chrome browser', icon: '📥' }
  ] : [
    { text: 'Open YouTube', icon: '🎵' },
    { text: 'Search for news', icon: '🔍' },
    { text: 'Go to Google', icon: '🌐' },
    { text: 'Browse GitHub', icon: '👨‍💻' }
  ];

  // Helper functions
  const getDomainFromUrl = (url) => {
    try {
      return new URL(url).hostname.replace('www.', '');
    } catch {
      return url.slice(0, 30) + '...';
    }
  };

  const getFaviconForUrl = (url) => {
    const domain = getDomainFromUrl(url).toLowerCase();
    const faviconMap = {
      'youtube.com': '🎥', 'google.com': '🔍', 'gmail.com': '📧',
      'github.com': '👨‍💻', 'facebook.com': '👥', 'twitter.com': '🐦',
      'linkedin.com': '💼', 'instagram.com': '📸', 'reddit.com': '🤖'
    };
    return faviconMap[domain] || '🌐';
  };

  const addChatMessage = (type, content) => {
    setChatMessages(prev => [...prev, { type, content, timestamp: new Date() }]);
  };

  const updateCurrentTab = (updates) => {
    setTabs(prev => prev.map(tab => 
      tab.active ? { ...tab, ...updates } : tab
    ));
  };

  const setActiveTabLoading = (loading) => {
    setTabs(prev => prev.map(tab => 
      tab.active ? { ...tab, loading } : tab
    ));
  };

  const createNewTabHandler = useCallback(async () => {
    try {
      const newSessionId = await createNewTab();
      const newTabId = Math.max(...tabs.map(t => t.id)) + 1;
      const newTab = { 
        id: newTabId, 
        sessionId: newSessionId,
        url: '', 
        title: 'New Tab', 
        active: false, 
        loading: false, 
        favicon: '🌐'
      };
      
      setTabs(prev => prev.map(tab => ({ ...tab, active: false })).concat({ ...newTab, active: true }));
      setActiveTab(newTabId);
      setBrowserContent('');
      setUrlInput('');
    } catch (error) {
      console.error('Failed to create new tab:', error);
    }
  }, [tabs, createNewTab]);

  return (
    <div className="browser-container h-screen flex flex-col bg-gray-50">
      {/* Local-First Enhanced Browser Header */}
      <header className="browser-toolbar bg-white border-b border-gray-200 px-4 py-2 shadow-sm">
        <div className="flex items-center space-x-4">
          {/* Navigation Controls */}
          <div className="flex items-center space-x-1">
            <button 
              onClick={onBackToWelcome}
              className="p-2.5 hover:bg-gray-100 rounded-lg transition-all duration-200 group"
              title="Back to Welcome"
            >
              <Home className="w-4 h-4 text-gray-600 group-hover:text-green-600" />
            </button>
            <button className="p-2.5 hover:bg-gray-100 rounded-lg transition-all duration-200 group">
              <ArrowLeft className="w-4 h-4 text-gray-600 group-hover:text-blue-600" />
            </button>
            <button className="p-2.5 hover:bg-gray-100 rounded-lg transition-all duration-200 group">
              <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-blue-600" />
            </button>
            <button 
              onClick={() => window.location.reload()}
              className="p-2.5 hover:bg-gray-100 rounded-lg transition-all duration-200 group"
            >
              <RotateCcw className="w-4 h-4 text-gray-600 group-hover:text-purple-600" />
            </button>
          </div>

          {/* Enhanced URL Bar with Local-First Indicator */}
          <form onSubmit={handleUrlSubmit} className="flex-1 max-w-2xl">
            <div className="relative">
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
                {isLoading ? (
                  <div className="loading-spinner w-4 h-4"></div>
                ) : (
                  <>
                    <Shield className="w-4 h-4 text-green-500" />
                    <span className="text-xs text-green-600 font-medium">
                      {isLocalFirst ? 'LOCAL' : 'PROXY'}
                    </span>
                  </>
                )}
              </div>
              <input
                type="text"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder={currentUrl || `Enter URL - ${isLocalFirst ? 'Direct access' : 'Proxy mode'}`}
                className="w-full pl-20 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
              />
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <button type="submit" className="text-gray-400 hover:text-gray-600 transition-colors">
                  <Search className="w-4 h-4" />
                </button>
              </div>
            </div>
          </form>

          {/* Enhanced Browser Controls */}
          <div className="flex items-center space-x-2">
            {/* Performance Metrics */}
            <div className="flex items-center space-x-1 text-xs bg-gradient-to-r from-green-50 to-blue-50 px-3 py-1.5 rounded-lg border border-green-200">
              <Activity className="w-3 h-3 text-green-600" />
              <span className="text-green-700 font-medium">{performanceMetrics.responseTime}ms</span>
              <div className="w-1 h-1 bg-green-400 rounded-full mx-1"></div>
              <span className="text-blue-700 text-xs">{performanceMetrics.mode}</span>
            </div>
            
            {/* Connection Status */}
            <div className="flex items-center space-x-1 text-xs text-gray-500 bg-gray-100 px-3 py-1.5 rounded-lg">
              {isOnline ? (
                <Wifi className="w-3 h-3 text-green-500" />
              ) : (
                <WifiOff className="w-3 h-3 text-red-500" />
              )}
              <span>{isOnline ? 'Online' : 'Offline'}</span>
            </div>
            
            {/* System Status Indicator */}
            <div className="flex items-center space-x-1 text-xs bg-gray-50 px-2 py-1 rounded border">
              {isLocalFirst ? (
                <CheckCircle className="w-3 h-3 text-green-500" />
              ) : (
                <XCircle className="w-3 h-3 text-orange-500" />
              )}
              <span className="text-gray-600">
                {isLocalFirst ? 'Local-First' : 'Server-First'}
              </span>
            </div>
            
            <button 
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Settings"
            >
              <Settings className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>

        {/* Enhanced Tab Bar */}
        <div className="flex items-center justify-between mt-2 -mb-2">
          <div className="flex items-center space-x-1 flex-1 overflow-x-auto">
            {tabs.map(tab => (
              <div 
                key={tab.id}
                className={`flex items-center px-4 py-2 rounded-t-lg cursor-pointer transition-all duration-200 min-w-0 max-w-48 ${
                  tab.active 
                    ? 'bg-white border-t border-l border-r border-gray-200 shadow-sm' 
                    : 'bg-gray-50 hover:bg-gray-100'
                }`}
                onClick={() => setActiveTab(tab.id)}
              >
                <span className="text-sm mr-2">{tab.favicon}</span>
                {tab.loading ? (
                  <div className="loading-spinner w-3 h-3 mr-2"></div>
                ) : null}
                <span className="text-sm truncate flex-1">{tab.title}</span>
                {tabs.length > 1 && (
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      closeTab(tab.sessionId);
                    }}
                    className="ml-2 p-0.5 hover:bg-gray-200 rounded transition-colors"
                  >
                    <X className="w-3 h-3 text-gray-400" />
                  </button>
                )}
              </div>
            ))}
            <button 
              onClick={createNewTabHandler}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors ml-2"
              title="New Tab"
            >
              <Plus className="w-4 h-4 text-gray-500" />
            </button>
          </div>

          <button
            onClick={() => setShowBookmarks(!showBookmarks)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Bookmarks"
          >
            <Star className="w-4 h-4 text-gray-500" />
          </button>
        </div>

        {/* Enhanced Bookmarks Bar */}
        {showBookmarks && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="flex items-center space-x-2 mt-2 pt-2 border-t border-gray-100 overflow-x-auto"
          >
            {bookmarks.map((bookmark, index) => (
              <button
                key={index}
                onClick={() => {
                  setUrlInput(bookmark.url);
                  handleUrlSubmit({ preventDefault: () => {} });
                }}
                className="flex items-center space-x-2 px-3 py-1.5 bg-gradient-to-r from-gray-50 to-gray-100 hover:from-gray-100 hover:to-gray-200 rounded-lg transition-all whitespace-nowrap border border-gray-200"
              >
                <span className="text-sm">{bookmark.favicon}</span>
                <span className="text-xs text-gray-700 font-medium">{bookmark.name}</span>
              </button>
            ))}
          </motion.div>
        )}
      </header>

      {/* Browser Content Area */}
      <main className="flex-1 relative bg-white">        
        {browserContent ? (
          <div className="w-full h-full relative">
            <div 
              className="w-full h-full"
              dangerouslySetInnerHTML={{ __html: browserContent }}
            />
          </div>
        ) : (
          <div className="flex items-center justify-center h-full bg-gradient-to-br from-gray-50 via-blue-50 to-green-50">
            <div className="text-center max-w-md">
              <div className="w-20 h-20 bg-gradient-to-br from-green-400 via-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                {isLocalFirst ? <Monitor className="w-10 h-10 text-white" /> : <Globe className="w-10 h-10 text-white" />}
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-3">
                {isLocalFirst ? 'Local-First Browser Ready' : 'Browser Ready'}
              </h3>
              <p className="text-gray-600 mb-6 leading-relaxed">
                {isLocalFirst ? 
                  'Direct internet access with full website functionality. No restrictions!' :
                  'Server-first browsing with proxy support for website access.'
                }
              </p>
              
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <button 
                  onClick={() => setIsChatOpen(true)}
                  className="bg-gradient-to-r from-green-500 via-blue-500 to-purple-600 text-white px-6 py-3 rounded-xl font-medium hover:shadow-lg transition-all duration-200 flex items-center space-x-2 justify-center"
                >
                  <Bot className="w-5 h-5" />
                  <span>Open AI Assistant</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Enhanced AI Assistant Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsChatOpen(!isChatOpen)}
        className="ai-assistant fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-br from-green-500 via-blue-500 to-purple-600 rounded-full shadow-xl hover:shadow-2xl flex items-center justify-center text-white z-50 transition-all duration-200"
      >
        <AnimatePresence mode="wait">
          {isChatOpen ? (
            <motion.div key="close" initial={{ rotate: -90 }} animate={{ rotate: 0 }} exit={{ rotate: 90 }}>
              <X className="w-6 h-6" />
            </motion.div>
          ) : (
            <motion.div key="brain" initial={{ rotate: 90 }} animate={{ rotate: 0 }} exit={{ rotate: -90 }}>
              <Brain className="w-6 h-6" />
            </motion.div>
          )}
        </AnimatePresence>
        <div className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center">
          <Zap className="w-2 h-2 text-white" />
        </div>
      </motion.button>

      {/* Enhanced AI Chat Panel */}
      <AnimatePresence>
        {isChatOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="ai-chat-panel fixed bottom-24 right-6 w-96 h-[600px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col z-40 overflow-hidden"
          >
            {/* Enhanced Chat Header */}
            <div className="bg-gradient-to-r from-green-500 via-blue-500 to-purple-600 text-white rounded-t-2xl p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                    <Brain className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-semibold">
                      {isLocalFirst ? 'Local-First AI' : 'Kairo AI Assistant'}
                    </h3>
                    <p className="text-xs text-white/90">
                      {isLocalFirst ? 'Direct • Fast • Unrestricted' : 'Server-First • Proxy Mode'}
                    </p>
                  </div>
                </div>
                <button 
                  onClick={() => setIsChatOpen(false)}
                  className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
              {chatMessages.map((message, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-xs px-4 py-3 rounded-2xl shadow-sm ${
                    message.type === 'user' 
                      ? 'bg-gradient-to-r from-green-500 to-blue-600 text-white rounded-br-md' 
                      : 'bg-white text-gray-800 rounded-bl-md border border-gray-100 shadow-md'
                  }`}>
                    <p className="text-sm whitespace-pre-wrap leading-relaxed">{message.content}</p>
                    <p className="text-xs mt-2 opacity-60">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </motion.div>
              ))}
              <div ref={chatEndRef} />
            </div>

            {/* Quick Commands */}
            {chatMessages.length <= 2 && (
              <div className="px-4 py-3 border-t border-gray-100 bg-gradient-to-r from-gray-50 to-blue-50">
                <p className="text-xs text-gray-600 mb-3 font-medium">
                  {isLocalFirst ? '⚡ Local-First Commands:' : '🌐 Available Commands:'}
                </p>
                <div className="grid grid-cols-1 gap-2">
                  {quickCommands.slice(0, 4).map((cmd, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setCurrentMessage(cmd.text);
                        handleAIChat({ preventDefault: () => {} });
                      }}
                      className="text-xs bg-white border border-gray-200 rounded-lg px-3 py-2 hover:shadow-sm hover:border-blue-300 transition-all duration-200 flex items-center space-x-2 text-left"
                    >
                      <span className="text-base">{cmd.icon}</span>
                      <span className="truncate text-gray-700">{cmd.text}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Chat Input */}
            <form onSubmit={handleAIChat} className="p-4 border-t border-gray-100 bg-white rounded-b-2xl">
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={currentMessage}
                  onChange={(e) => setCurrentMessage(e.target.value)}
                  placeholder={isLocalFirst ? "Direct access to any website..." : "Ask me anything..."}
                  className="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-gray-50"
                />
                <button 
                  type="submit"
                  disabled={!currentMessage.trim() || isLoading}
                  className="p-3 bg-gradient-to-r from-green-500 to-blue-600 text-white rounded-xl hover:from-green-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
                >
                  {isLoading ? (
                    <div className="loading-spinner w-4 h-4"></div>
                  ) : (
                    <Send className="w-4 h-4" />
                  )}
                </button>
              </div>
            </form>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default LocalFirstBrowserInterface;