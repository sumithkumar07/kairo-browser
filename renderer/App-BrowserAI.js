import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, Send, Loader, Globe, Maximize2, Minimize2, RotateCcw, Home, ArrowLeft, ArrowRight } from 'lucide-react';
import './App.css';

function BrowserAIApp() {
  // Browser State
  const [currentUrl, setCurrentUrl] = useState('https://www.google.com');
  const [pageTitle, setPageTitle] = useState('Google');
  const [isLoading, setIsLoading] = useState(false);
  const [browserReady, setBrowserReady] = useState(false);

  // AI Chat State
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [aiProcessing, setAiProcessing] = useState(false);
  const [aiStatus, setAiStatus] = useState('initializing');

  // Navigation State
  const [canGoBack, setCanGoBack] = useState(false);
  const [canGoForward, setCanGoForward] = useState(false);

  // Refs
  const messagesEndRef = useRef(null);
  const browserFrameRef = useRef(null);

  // Initialize System
  useEffect(() => {
    initializeSystem();
  }, []);

  // Auto-scroll chat
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const initializeSystem = async () => {
    try {
      console.log('🚀 Initializing Browser + AI System...');
      
      if (window.kairoAPI) {
        // Initialize AI
        const aiResult = await window.kairoAPI.ai.initialize();
        
        if (aiResult.success) {
          setAiStatus('ready');
          setBrowserReady(true);
          
          // Add welcome message
          addMessage({
            role: 'assistant',
            content: "Hello! I'm your AI assistant. I can control the browser for you. Just tell me what you want to do and watch me work! Try saying: 'Go to YouTube' or 'Search for iPhone prices on Amazon'",
            type: 'welcome',
            timestamp: new Date()
          });
          
          console.log('✅ AI System ready');
        } else {
          setAiStatus('error');
          addMessage({
            role: 'assistant',
            content: 'I had trouble starting up. The browser works, but AI control might be limited.',
            type: 'error',
            timestamp: new Date()
          });
        }
        
        // Listen for browser events
        window.kairoAPI.on('browser-updated', (event, data) => {
          if (data.url) setCurrentUrl(data.url);
          if (data.title) setPageTitle(data.title);
          setIsLoading(false);
        });
        
      } else {
        // Fallback mode
        setAiStatus('demo');
        setBrowserReady(true);
        addMessage({
          role: 'assistant',
          content: 'Demo mode active. I can show you how the interface works, but full AI browser control requires the desktop app.',
          type: 'demo',
          timestamp: new Date()
        });
      }
    } catch (error) {
      console.error('Initialization error:', error);
      setAiStatus('error');
    }
  };

  const addMessage = (message) => {
    setMessages(prev => [...prev, { ...message, id: Date.now() + Math.random() }]);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Browser Navigation Functions
  const navigateToUrl = async (url) => {
    if (!url || isLoading) return;
    
    // Ensure proper URL format
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = 'https://' + url;
    }

    setIsLoading(true);
    
    try {
      if (window.kairoAPI && browserReady) {
        const result = await window.kairoAPI.browser.navigate(url);
        if (result.success) {
          setCurrentUrl(result.url);
          setPageTitle(result.title || 'Loading...');
        }
      } else {
        // Demo mode - simulate navigation
        setCurrentUrl(url);
        setPageTitle('Demo - ' + new URL(url).hostname);
        setTimeout(() => setIsLoading(false), 1000);
      }
    } catch (error) {
      console.error('Navigation error:', error);
      setIsLoading(false);
    }
  };

  const goBack = async () => {
    if (window.kairoAPI) {
      await window.kairoAPI.browser.goBack();
    }
  };

  const goForward = async () => {
    if (window.kairoAPI) {
      await window.kairoAPI.browser.goForward();
    }
  };

  const refresh = async () => {
    if (window.kairoAPI) {
      setIsLoading(true);
      await window.kairoAPI.browser.refresh();
    } else {
      setIsLoading(true);
      setTimeout(() => setIsLoading(false), 1000);
    }
  };

  const goHome = () => {
    navigateToUrl('https://www.google.com');
  };

  // AI Chat Functions
  const handleAICommand = async (command) => {
    if (!command.trim() || aiProcessing) return;

    // Add user message
    addMessage({
      role: 'user',
      content: command,
      timestamp: new Date()
    });

    setInputValue('');
    setAiProcessing(true);

    try {
      if (window.kairoAPI && aiStatus === 'ready') {
        // Add AI thinking message
        addMessage({
          role: 'assistant',
          content: 'Let me handle that for you. Watch the browser!',
          type: 'working',
          timestamp: new Date()
        });

        // Process AI command
        const response = await window.kairoAPI.ai.processInput(command, {
          currentUrl: currentUrl,
          pageTitle: pageTitle,
          timestamp: new Date().toISOString()
        });

        if (response.success) {
          addMessage({
            role: 'assistant',
            content: response.message,
            data: response.data,
            browserResults: response.browserResults,
            timestamp: new Date()
          });

          // Add proactive suggestions
          if (response.proactiveActions?.length > 0) {
            setTimeout(() => {
              addMessage({
                role: 'assistant',
                content: 'Here are some things you might want to do next:',
                type: 'suggestions',
                suggestions: response.proactiveActions,
                timestamp: new Date()
              });
            }, 2000);
          }
        } else {
          addMessage({
            role: 'assistant',
            content: response.message || "I couldn't complete that action. Could you try rephrasing your request?",
            type: 'error',
            timestamp: new Date()
          });
        }
      } else {
        // Demo responses
        const demoResponses = {
          'go to youtube': 'I would navigate to YouTube.com for you',
          'search': 'I would search for that on the current website',
          'find': 'I would find and extract that information',
          'compare': 'I would open multiple tabs and compare the data',
          'default': `I understand you want: "${command}". In full mode, I would control the browser automatically to do this.`
        };

        const responseKey = Object.keys(demoResponses).find(key => 
          command.toLowerCase().includes(key)
        ) || 'default';

        // Simulate browser action
        if (command.toLowerCase().includes('youtube')) {
          navigateToUrl('https://www.youtube.com');
        } else if (command.toLowerCase().includes('amazon')) {
          navigateToUrl('https://www.amazon.com');
        } else if (command.toLowerCase().includes('google')) {
          navigateToUrl('https://www.google.com');
        }

        setTimeout(() => {
          addMessage({
            role: 'assistant',
            content: demoResponses[responseKey],
            type: 'demo',
            timestamp: new Date()
          });
        }, 1500);
      }
    } catch (error) {
      console.error('AI command error:', error);
      addMessage({
        role: 'assistant',
        content: "I encountered an error. Let me try a different approach. What would you like me to do?",
        type: 'error',
        timestamp: new Date()
      });
    } finally {
      setAiProcessing(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    handleAICommand(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAICommand(inputValue);
    }
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 p-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Globe className="w-6 h-6 text-blue-400" />
            <span className="text-lg font-semibold">Kairo AI Browser</span>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${
                aiStatus === 'ready' ? 'bg-green-400' :
                aiStatus === 'initializing' ? 'bg-yellow-400 animate-pulse' :
                aiStatus === 'demo' ? 'bg-blue-400' :
                'bg-red-400'
              }`}></div>
              <span className="text-sm text-gray-400">
                {aiStatus === 'ready' && 'AI Ready'}
                {aiStatus === 'initializing' && 'Starting...'}
                {aiStatus === 'demo' && 'Demo Mode'}
                {aiStatus === 'error' && 'Limited Mode'}
              </span>
            </div>
          </div>
          
          <div className="text-sm text-gray-400">
            Browser + AI Assistant
          </div>
        </div>
      </div>

      {/* Main Content - Split Screen */}
      <div className="flex-1 flex">
        {/* Browser Panel */}
        <div className="flex-1 flex flex-col bg-gray-100">
          {/* Browser Controls */}
          <div className="bg-gray-800 border-b border-gray-700 p-3">
            <div className="flex items-center space-x-3">
              {/* Navigation Controls */}
              <div className="flex items-center space-x-1">
                <button 
                  onClick={goBack}
                  disabled={!canGoBack}
                  className="p-2 hover:bg-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <ArrowLeft className="w-4 h-4" />
                </button>
                <button 
                  onClick={goForward}
                  disabled={!canGoForward}
                  className="p-2 hover:bg-gray-700 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <ArrowRight className="w-4 h-4" />
                </button>
                <button 
                  onClick={refresh}
                  className="p-2 hover:bg-gray-700 rounded"
                >
                  <RotateCcw className="w-4 h-4" />
                </button>
                <button 
                  onClick={goHome}
                  className="p-2 hover:bg-gray-700 rounded"
                >
                  <Home className="w-4 h-4" />
                </button>
              </div>

              {/* URL Bar */}
              <div className="flex-1">
                <input
                  type="text"
                  value={currentUrl}
                  onChange={(e) => setCurrentUrl(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && navigateToUrl(currentUrl)}
                  className="w-full bg-gray-900 text-white px-3 py-2 rounded border border-gray-600 focus:border-blue-500 focus:outline-none"
                  placeholder="Enter URL or let AI navigate for you..."
                />
              </div>

              {/* Loading Indicator */}
              {isLoading && (
                <Loader className="w-5 h-5 animate-spin text-blue-400" />
              )}
            </div>

            {/* Page Info */}
            <div className="mt-2 text-sm text-gray-400">
              📄 {pageTitle} {aiProcessing && '• AI is working...'}
            </div>
          </div>

          {/* Browser Content */}
          <div className="flex-1 bg-white relative">
            {browserReady ? (
              <div className="h-full flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
                <div className="text-center p-8">
                  <Globe className="w-24 h-24 text-blue-600 mx-auto mb-6" />
                  <h2 className="text-3xl font-bold text-gray-800 mb-4">Browser Ready</h2>
                  <p className="text-gray-600 mb-6 max-w-md">
                    Tell the AI what you want to do, and watch me control this browser automatically!
                  </p>
                  <div className="bg-white/80 p-4 rounded-lg border border-gray-200">
                    <p className="text-sm text-gray-700">
                      <strong>Current URL:</strong> {currentUrl}
                    </p>
                    <p className="text-sm text-gray-700 mt-1">
                      <strong>Status:</strong> {isLoading ? 'Loading...' : 'Ready for AI control'}
                    </p>
                  </div>
                  
                  {/* Quick Navigation */}
                  <div className="mt-6 flex flex-wrap justify-center gap-2">
                    <button 
                      onClick={() => navigateToUrl('https://youtube.com')}
                      className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                    >
                      YouTube
                    </button>
                    <button 
                      onClick={() => navigateToUrl('https://amazon.com')}
                      className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 transition-colors"
                    >
                      Amazon
                    </button>
                    <button 
                      onClick={() => navigateToUrl('https://google.com')}
                      className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                    >
                      Google
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center bg-gray-100">
                <div className="text-center">
                  <Loader className="w-12 h-12 text-gray-400 mx-auto mb-4 animate-spin" />
                  <p className="text-gray-600">Initializing browser...</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* AI Chat Panel */}
        <div className="w-96 bg-gray-800 border-l border-gray-700 flex flex-col">
          {/* Chat Header */}
          <div className="bg-gray-900 p-4 border-b border-gray-700">
            <div className="flex items-center space-x-3">
              <Bot className="w-6 h-6 text-green-400" />
              <div>
                <h3 className="font-semibold text-white">AI Assistant</h3>
                <p className="text-sm text-gray-400">
                  {aiProcessing ? 'Working on your request...' : 'Ready to help'}
                </p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length === 0 && (
              <div className="text-center py-8">
                <Bot className="w-12 h-12 text-gray-600 mx-auto mb-4" />
                <p className="text-gray-400 text-sm">
                  Tell me what you want to do and watch me control the browser!
                </p>
                <div className="mt-4 space-y-2 text-xs text-gray-500">
                  <p>"Go to YouTube"</p>
                  <p>"Search for iPhone prices"</p>
                  <p>"Find AI tutorials"</p>
                  <p>"Compare products on Amazon"</p>
                </div>
              </div>
            )}

            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className={`${message.role === 'user' ? 'ml-4' : 'mr-4'}`}
                >
                  <div className={`p-3 rounded-lg text-sm ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white ml-auto'
                      : message.type === 'error'
                      ? 'bg-red-900/50 border border-red-500/50 text-red-100'
                      : message.type === 'welcome'
                      ? 'bg-green-900/50 border border-green-500/50 text-green-100'
                      : message.type === 'working'
                      ? 'bg-yellow-900/50 border border-yellow-500/50 text-yellow-100'
                      : 'bg-gray-700 text-gray-100'
                  }`}>
                    <p className="leading-relaxed">{message.content}</p>

                    {/* Browser Results */}
                    {message.browserResults && message.browserResults.length > 0 && (
                      <div className="mt-2 space-y-1">
                        <div className="text-xs text-gray-400">Browser Actions:</div>
                        {message.browserResults.slice(0, 2).map(([taskId, result], index) => (
                          <div key={index} className="text-xs bg-black/20 p-1 rounded">
                            <span className={result.success ? 'text-green-400' : 'text-red-400'}>
                              {result.success ? '✅' : '❌'}
                            </span>
                            <span className="ml-1">{result.action || taskId}</span>
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Suggestions */}
                    {message.type === 'suggestions' && message.suggestions && (
                      <div className="mt-2 space-y-1">
                        {message.suggestions.map((suggestion, index) => (
                          <button
                            key={index}
                            onClick={() => handleSuggestionClick(suggestion)}
                            className="block w-full p-2 bg-blue-600/20 hover:bg-blue-600/30 border border-blue-500/30 rounded text-left text-xs transition-colors"
                          >
                            💡 {suggestion}
                          </button>
                        ))}
                      </div>
                    )}

                    <div className="mt-1 text-xs text-gray-500">
                      {formatTimestamp(message.timestamp)}
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {/* AI Processing Indicator */}
            {aiProcessing && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mr-4"
              >
                <div className="bg-gray-700 p-3 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <Bot className="w-4 h-4 text-green-400" />
                    <div className="flex space-x-1">
                      <div className="w-1 h-1 bg-green-400 rounded-full animate-bounce"></div>
                      <div className="w-1 h-1 bg-green-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-1 h-1 bg-green-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                    <span className="text-xs text-gray-300">Working...</span>
                  </div>
                </div>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="p-4 border-t border-gray-700">
            <div className="flex space-x-2">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Tell me what to do..."
                className="flex-1 bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none resize-none text-sm"
                rows={2}
                disabled={aiProcessing}
              />
              <button
                onClick={() => handleAICommand(inputValue)}
                disabled={!inputValue.trim() || aiProcessing}
                className="px-3 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed rounded transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
            <div className="text-xs text-gray-500 mt-1">
              Press Enter to send • Watch the browser work!
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default BrowserAIApp;