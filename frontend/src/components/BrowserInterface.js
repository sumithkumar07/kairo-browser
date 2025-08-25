import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, 
  ArrowRight, 
  RotateCcw, 
  Home, 
  Search,
  Bot,
  Send,
  X,
  Globe,
  Shield,
  Zap,
  ExternalLink,
  ChevronDown,
  Plus,
  Settings
} from 'lucide-react';
import { useSession } from '../contexts/SessionContext';

const BrowserInterface = ({ onBackToWelcome }) => {
  const {
    sessionId,
    currentUrl,
    isLoading,
    history,
    navigateToUrl,
    processAIQuery,
    proxyRequest
  } = useSession();

  const [urlInput, setUrlInput] = useState('');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState([
    {
      type: 'ai',
      content: "Hello! I'm your AI assistant. I can help you navigate websites, search for information, and automate browsing tasks. Try asking me to 'open YouTube' or 'search for AI news'!",
      timestamp: new Date()
    }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [iframeContent, setIframeContent] = useState('');
  const [tabs, setTabs] = useState([{ id: 1, url: '', title: 'New Tab', active: true }]);
  const [activeTab, setActiveTab] = useState(1);
  
  const chatEndRef = useRef(null);
  const iframeRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  // Listen for navigation messages from iframe content
  useEffect(() => {
    const handleMessage = async (event) => {
      // Only handle messages from our iframe content
      if (event.data && event.data.type === 'NAVIGATE_TO') {
        const newUrl = event.data.url;
        console.log('Received navigation request from iframe:', newUrl);
        
        try {
          // Navigate using our browser system
          await navigateToUrl(newUrl);
          
          // Load content via enhanced proxy system
          const response = await proxyRequest(newUrl);
          if (response && response.content) {
            console.log(`Navigation completed using ${response.method} for ${newUrl}`);
            setIframeContent(response.content);
          }
        } catch (error) {
          console.error('Navigation failed:', error);
          addChatMessage('ai', `Navigation to ${newUrl} failed. Please try again.`);
        }
      }
    };

    // Add message listener
    window.addEventListener('message', handleMessage);
    
    // Cleanup
    return () => {
      window.removeEventListener('message', handleMessage);
    };
  }, [navigateToUrl, proxyRequest]);

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    try {
      await navigateToUrl(urlInput);
      
      // Load content via enhanced proxy system for display
      const response = await proxyRequest(urlInput);
      if (response.content) {
        console.log(`Direct navigation loaded using ${response.method}`);
        setIframeContent(response.content);
      }
      
      setUrlInput('');
    } catch (error) {
      console.error('Navigation failed:', error);
      addChatMessage('ai', `Sorry, I couldn't navigate to ${urlInput}. Please check the URL and try again.`);
    }
  };

  const addChatMessage = (type, content, metadata = {}) => {
    const message = {
      type,
      content,
      timestamp: new Date(),
      metadata
    };
    setChatMessages(prev => [...prev, message]);
  };

  const handleAIChat = async (e) => {
    e.preventDefault();
    if (!currentMessage.trim()) return;

    const userMessage = currentMessage.trim();
    addChatMessage('user', userMessage);
    setCurrentMessage('');

    try {
      const aiResponse = await processAIQuery(userMessage, {
        currentUrl: currentUrl,
        sessionId: sessionId
      });

      let responseText = aiResponse.explanation || 'I understand your request.';
      
      // Execute AI commands
      if (aiResponse.commands && aiResponse.commands.length > 0) {
        for (const command of aiResponse.commands) {
          if (command.type === 'open' && command.params?.url) {
            responseText += `\n\nOpening ${command.params.url}...`;
            await navigateToUrl(command.params.url);
            
            // Load content via enhanced proxy system
            try {
              console.log(`🔍 Attempting to load content for: ${command.params.url}`);
              const response = await proxyRequest(command.params.url);
              console.log(`📡 Proxy response received:`, response);
              
              if (response && response.content) {
                console.log(`✅ Content loaded using ${response.method} for ${command.params.url}`);
                console.log(`📄 Content length: ${response.content.length} characters`);
                setIframeContent(response.content);
                
                // Update response text with method info
                if (response.method === 'enhanced_browser_rendered') {
                  responseText += `\n✅ Loaded using enhanced browser engine with anti-detection`;
                } else if (response.method === 'enhanced_http_proxy') {
                  responseText += `\n✅ Loaded using enhanced HTTP proxy`;
                } else {
                  responseText += `\n✅ Loaded using ${response.method}`;
                }
              } else {
                console.error('❌ No content in proxy response:', response);
                responseText += `\n⚠️ Received response but no content found`;
              }
            } catch (proxyError) {
              console.error('❌ All proxy methods failed:', proxyError);
              responseText += `\n⚠️ Unable to load content directly. Error: ${proxyError.message}`;
            }
          }
        }
      }

      addChatMessage('ai', responseText, { commands: aiResponse.commands });
      
    } catch (error) {
      console.error('AI chat error:', error);
      addChatMessage('ai', 'Sorry, I encountered an error processing your request. Please try again.');
    }
  };

  const quickCommands = [
    { text: 'Open YouTube', icon: '📺' },
    { text: 'Search Google', icon: '🔍' },
    { text: 'Open GitHub', icon: '👨‍💻' },
    { text: 'Check the news', icon: '📰' }
  ];

  const handleQuickCommand = async (command) => {
    setCurrentMessage(command);
    
    // Also immediately process the command
    addChatMessage('user', command);
    
    try {
      const aiResponse = await processAIQuery(command, {
        currentUrl: currentUrl,
        sessionId: sessionId
      });

      let responseText = aiResponse.explanation || 'I understand your request.';
      
      // Execute AI commands
      if (aiResponse.commands && aiResponse.commands.length > 0) {
        for (const aiCommand of aiResponse.commands) {
          if (aiCommand.type === 'open' && aiCommand.params?.url) {
            responseText += `\n\nOpening ${aiCommand.params.url}...`;
            await navigateToUrl(aiCommand.params.url);
            
            // Load content via enhanced proxy system
            try {
              console.log(`🔍 Attempting to load content for: ${aiCommand.params.url}`);
              const response = await proxyRequest(aiCommand.params.url);
              console.log(`📡 Proxy response received:`, response);
              
              if (response && response.content) {
                console.log(`✅ Content loaded using ${response.method} for ${aiCommand.params.url}`);
                console.log(`📄 Content length: ${response.content.length} characters`);
                setIframeContent(response.content);
                
                // Update response text with method info
                if (response.method === 'enhanced_browser_rendered') {
                  responseText += `\n✅ Loaded using enhanced browser engine with anti-detection`;
                } else if (response.method === 'enhanced_http_proxy') {
                  responseText += `\n✅ Loaded using enhanced HTTP proxy`;
                } else {
                  responseText += `\n✅ Loaded using ${response.method}`;
                }
              } else {
                console.error('❌ No content in proxy response:', response);
                responseText += `\n⚠️ Received response but no content found`;
              }
            } catch (proxyError) {
              console.error('❌ All proxy methods failed:', proxyError);
              responseText += `\n⚠️ Unable to load content directly. Error: ${proxyError.message}`;
            }
          }
        }
      }

      addChatMessage('ai', responseText, { commands: aiResponse.commands });
      
    } catch (error) {
      console.error('AI chat error:', error);
      addChatMessage('ai', 'Sorry, I encountered an error processing your request. Please try again.');
    }
    
    setCurrentMessage('');
  };

  const createNewTab = () => {
    const newTabId = Math.max(...tabs.map(t => t.id)) + 1;
    const newTab = { id: newTabId, url: '', title: 'New Tab', active: false };
    setTabs(prev => prev.map(tab => ({ ...tab, active: false })).concat({ ...newTab, active: true }));
    setActiveTab(newTabId);
  };

  const closeTab = (tabId) => {
    if (tabs.length === 1) return; // Don't close the last tab
    
    setTabs(prev => {
      const filtered = prev.filter(tab => tab.id !== tabId);
      if (activeTab === tabId && filtered.length > 0) {
        const newActive = filtered[filtered.length - 1];
        newActive.active = true;
        setActiveTab(newActive.id);
      }
      return filtered;
    });
  };

  return (
    <div className="browser-container h-screen flex flex-col bg-gray-50">
      {/* Browser Header */}
      <header className="browser-toolbar bg-white border-b border-gray-200 px-4 py-2">
        <div className="flex items-center space-x-4">
          {/* Navigation Controls */}
          <div className="flex items-center space-x-1">
            <button 
              onClick={onBackToWelcome}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Back to Welcome"
            >
              <Home className="w-4 h-4 text-gray-600" />
            </button>
            <button 
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              disabled={history.length === 0}
            >
              <ArrowLeft className="w-4 h-4 text-gray-600" />
            </button>
            <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <ArrowRight className="w-4 h-4 text-gray-600" />
            </button>
            <button 
              onClick={() => window.location.reload()}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <RotateCcw className="w-4 h-4 text-gray-600" />
            </button>
          </div>

          {/* URL Bar */}
          <form onSubmit={handleUrlSubmit} className="flex-1 max-w-2xl">
            <div className="relative">
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
                {isLoading ? (
                  <div className="loading-spinner w-4 h-4"></div>
                ) : (
                  <>
                    <Shield className="w-4 h-4 text-green-500" />
                    <span className="text-xs text-green-600 font-medium">SECURE</span>
                  </>
                )}
              </div>
              <input
                type="text"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder={currentUrl || "Enter URL or search..."}
                className="w-full pl-20 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <button type="submit" className="text-gray-400 hover:text-gray-600">
                  <Search className="w-4 h-4" />
                </button>
              </div>
            </div>
          </form>

          {/* Browser Controls */}
          <div className="flex items-center space-x-2">
            <div className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              Session: {sessionId?.slice(-8)}
            </div>
            <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <Settings className="w-4 h-4 text-gray-600" />
            </button>
          </div>
        </div>

        {/* Tab Bar */}
        <div className="flex items-center space-x-1 mt-2 -mb-2">
          {tabs.map(tab => (
            <div 
              key={tab.id}
              className={`flex items-center px-3 py-2 rounded-t-lg cursor-pointer transition-colors ${
                tab.active ? 'bg-white border-t border-l border-r border-gray-200' : 'bg-gray-50 hover:bg-gray-100'
              }`}
              onClick={() => {
                setTabs(prev => prev.map(t => ({ ...t, active: t.id === tab.id })));
                setActiveTab(tab.id);
              }}
            >
              <Globe className="w-3 h-3 mr-2 text-gray-500" />
              <span className="text-sm max-w-32 truncate">{tab.title}</span>
              {tabs.length > 1 && (
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    closeTab(tab.id);
                  }}
                  className="ml-2 p-0.5 hover:bg-gray-200 rounded"
                >
                  <X className="w-3 h-3 text-gray-400" />
                </button>
              )}
            </div>
          ))}
          <button 
            onClick={createNewTab}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Plus className="w-4 h-4 text-gray-500" />
          </button>
        </div>
      </header>

      {/* Browser Content */}
      <main className="flex-1 relative bg-white">        
        {iframeContent ? (
          <div className="w-full h-full relative">
            <div 
              className="w-full h-full"
              dangerouslySetInnerHTML={{ __html: iframeContent }}
            />
            {/* Fallback iframe for sites that still block embedding */}
            {!iframeContent.includes('<html') && (
              <iframe 
                src={currentUrl}
                className="absolute inset-0 w-full h-full border-none"
                title="Website Content"
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms allow-top-navigation"
                onLoad={() => console.log('Iframe loaded successfully')}
                onError={() => console.log('Iframe failed to load')}
              />
            )}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full bg-gray-50">
            <div className="text-center">
              <Globe className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-600 mb-2">Ready to browse</h3>
              <p className="text-gray-500 mb-4">Enter a URL above or ask the AI assistant to navigate</p>
              <button 
                onClick={() => setIsChatOpen(true)}
                className="bg-green-500 text-white px-6 py-3 rounded-xl font-medium hover:bg-green-600 transition-colors flex items-center space-x-2 mx-auto"
              >
                <Bot className="w-5 h-5" />
                <span>Ask AI Assistant</span>
              </button>
            </div>
          </div>
        )}
      </main>

      {/* AI Assistant Button */}
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsChatOpen(!isChatOpen)}
        className="ai-assistant fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-br from-green-500 to-green-600 rounded-full shadow-lg hover:shadow-xl flex items-center justify-center text-white z-50"
      >
        <AnimatePresence mode="wait">
          {isChatOpen ? (
            <motion.div key="close" initial={{ rotate: -90 }} animate={{ rotate: 0 }} exit={{ rotate: 90 }}>
              <X className="w-6 h-6" />
            </motion.div>
          ) : (
            <motion.div key="bot" initial={{ rotate: 90 }} animate={{ rotate: 0 }} exit={{ rotate: -90 }}>
              <Bot className="w-6 h-6" />
            </motion.div>
          )}
        </AnimatePresence>
      </motion.button>

      {/* AI Chat Panel */}
      <AnimatePresence>
        {isChatOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="ai-chat-panel fixed bottom-24 right-6 w-96 h-[500px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col z-40"
          >
            {/* Chat Header */}
            <div className="p-4 border-b border-gray-100 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-t-2xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                    <Bot className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="font-semibold">AI Assistant</h3>
                    <p className="text-xs text-green-100">Ready to help</p>
                  </div>
                </div>
                <button 
                  onClick={() => setIsChatOpen(false)}
                  className="p-1 hover:bg-white/20 rounded-lg transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {chatMessages.map((message, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`ai-chat-bubble flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-xs px-4 py-2 rounded-2xl ${
                    message.type === 'user' 
                      ? 'bg-green-500 text-white rounded-br-md' 
                      : 'bg-gray-100 text-gray-800 rounded-bl-md'
                  }`}>
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <p className="text-xs mt-1 opacity-60">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </motion.div>
              ))}
              <div ref={chatEndRef} />
            </div>

            {/* Quick Commands */}
            {chatMessages.length <= 2 && (
              <div className="px-4 py-2 border-t border-gray-100 bg-gray-50">
                <p className="text-xs text-gray-500 mb-2">Quick commands:</p>
                <div className="flex flex-wrap gap-1">
                  {quickCommands.map((cmd, index) => (
                    <button
                      key={index}
                      onClick={() => handleQuickCommand(cmd.text)}
                      className="text-xs bg-white border border-gray-200 rounded-lg px-2 py-1 hover:bg-gray-50 transition-colors flex items-center space-x-1"
                    >
                      <span>{cmd.icon}</span>
                      <span>{cmd.text}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Chat Input */}
            <form onSubmit={handleAIChat} className="p-4 border-t border-gray-100">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={currentMessage}
                  onChange={(e) => setCurrentMessage(e.target.value)}
                  placeholder="Ask me anything..."
                  className="flex-1 px-3 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <button 
                  type="submit"
                  disabled={!currentMessage.trim() || isLoading}
                  className="p-2 bg-green-500 text-white rounded-xl hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
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

export default BrowserInterface;