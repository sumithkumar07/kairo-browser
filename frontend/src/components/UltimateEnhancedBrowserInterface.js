import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Globe, Home, ArrowLeft, ArrowRight, RotateCcw, Search, Plus, X, Star,
  Settings, Download, BookmarkPlus, Wifi, WifiOff, Shield, Maximize2, Minimize2,
  Bot, Send, Volume2, VolumeX, Eye, Zap, Mic, Camera, Cpu, Activity,
  Layers, Target, Gauge, Brain, Headphones, Image as ImageIcon
} from 'lucide-react';

const UltimateEnhancedBrowserInterface = ({ onBackToWelcome }) => {
  // Core state
  const [tabs, setTabs] = useState([{ id: 1, url: '', title: 'New Tab', active: true, loading: false, favicon: '🌐' }]);
  const [activeTab, setActiveTab] = useState(1);
  const [urlInput, setUrlInput] = useState('');
  const [currentUrl, setCurrentUrl] = useState('');
  const [iframeContent, setIframeContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);

  // Enhanced UI state
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showBookmarks, setShowBookmarks] = useState(false);
  const [showDownloads, setShowDownloads] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const [isMuted, setIsMuted] = useState(false);

  // Session and chat state
  const [sessionId] = useState(`kairo_${Date.now()}`);
  const [chatMessages, setChatMessages] = useState([
    { type: 'ai', content: '🚀 Ultimate Kairo AI Browser ready! I now have enhanced capabilities:\n\n🤖 Multi-modal AI (text, voice, images)\n🎯 Real website interaction\n🎨 Advanced rendering optimization\n🥷 Military-grade stealth protection\n🛡️ Bulletproof fallback system\n\nWhat would you like to explore?', timestamp: new Date() }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const chatEndRef = useRef(null);

  // Enhanced features state
  const [systemAnalytics, setSystemAnalytics] = useState(null);
  const [userPreferences, setUserPreferences] = useState({
    prefer_speed: false,
    prefer_reliability: true,
    prefer_stealth: true,
    stealth_level: 5,
    rendering_profile: 'balanced'
  });
  const [voiceRecording, setVoiceRecording] = useState(false);
  const [imageAnalyzing, setImageAnalyzing] = useState(false);

  // Bookmarks with enhanced sites
  const [bookmarks, setBookmarks] = useState([
    { name: 'YouTube', url: 'https://youtube.com', favicon: '🎥' },
    { name: 'Google', url: 'https://google.com', favicon: '🔍' },
    { name: 'GitHub', url: 'https://github.com', favicon: '👨‍💻' },
    { name: 'LinkedIn', url: 'https://linkedin.com', favicon: '💼' },
    { name: 'Twitter', url: 'https://twitter.com', favicon: '🐦' },
    { name: 'Reddit', url: 'https://reddit.com', favicon: '🤖' }
  ]);

  // Enhanced performance monitoring
  const [performanceMetrics, setPerformanceMetrics] = useState({
    request_time: 0,
    method_used: '',
    tier_used: '',
    success_rate: 100,
    stealth_level: 5
  });

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  // Load system analytics on mount
  useEffect(() => {
    loadSystemAnalytics();
  }, []);

  const loadSystemAnalytics = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
      const response = await fetch(`${backendUrl}/api/system/analytics`);
      if (response.ok) {
        const analytics = await response.json();
        setSystemAnalytics(analytics);
      }
    } catch (error) {
      console.error('Failed to load system analytics:', error);
    }
  };

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    const url = normalizeUrl(urlInput);
    setIsLoading(true);
    setActiveTabLoading(true);
    setCurrentUrl(url);

    try {
      await navigateToUrl(url);
    } catch (error) {
      console.error('Navigation error:', error);
    }
  };

  const navigateToUrl = async (url) => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
      
      const requestBody = {
        url: url,
        method: "GET",
        headers: null,
        context: {
          currentUrl: currentUrl,
          sessionId: sessionId,
          userAction: 'navigation'
        },
        user_preferences: userPreferences,
        session_id: sessionId,
        enhance_rendering: true,
        stealth_level: userPreferences.stealth_level
      };

      const response = await fetch(`${backendUrl}/api/ultimate/proxy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      const result = await response.json();

      if (result.success && result.content) {
        setIframeContent(result.content);
        updateCurrentTab({ 
          url: url, 
          title: getDomainFromUrl(url),
          loading: false,
          favicon: getFaviconForUrl(url)
        });

        // Update performance metrics
        setPerformanceMetrics({
          request_time: result.request_time_ms || 0,
          method_used: result.method_used || 'unknown',
          tier_used: result.tier_used || 'unknown',
          success_rate: result.success ? 100 : 0,
          stealth_level: userPreferences.stealth_level
        });

        setHistory(prev => [...prev, url]);
        setUrlInput('');
      } else {
        throw new Error(result.error || 'Navigation failed');
      }
    } catch (error) {
      console.error('Ultimate navigation error:', error);
      setIframeContent(`<html><body><h1>Navigation Error</h1><p>${error.message}</p></body></html>`);
    } finally {
      setIsLoading(false);
      setActiveTabLoading(false);
    }
  };

  const handleAIChat = async (e) => {
    e.preventDefault();
    if (!currentMessage.trim()) return;

    addChatMessage('user', currentMessage);
    const userMessage = currentMessage;
    setCurrentMessage('');
    setIsLoading(true);

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
      
      const requestBody = {
        query: userMessage,
        context: {
          currentUrl: currentUrl,
          sessionId: sessionId,
          userAction: 'ai_query',
          performanceMetrics: performanceMetrics
        },
        session_id: sessionId,
        include_predictions: true,
        include_visual_feedback: true
      };

      const response = await fetch(`${backendUrl}/api/ai/multimodal-query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });

      const aiResponse = await response.json();

      if (aiResponse.success && aiResponse.response) {
        let responseText = aiResponse.response.explanation || 'I understand your request.';
        
        // Process commands if any
        if (aiResponse.response.commands && aiResponse.response.commands.length > 0) {
          for (const command of aiResponse.response.commands) {
            if (command.type === 'open' && command.params?.url) {
              responseText += `\n\n🚀 Opening ${command.params.url} with enhanced capabilities...`;
              await navigateToUrl(command.params.url);
            }
          }
        }

        // Add predictive suggestions
        if (aiResponse.response.next_suggestions && aiResponse.response.next_suggestions.length > 0) {
          responseText += '\n\n💡 **Suggestions:**\n';
          aiResponse.response.next_suggestions.forEach(suggestion => {
            responseText += `• ${suggestion}\n`;
          });
        }

        addChatMessage('ai', responseText, { 
          commands: aiResponse.response.commands,
          predictions: aiResponse.response.next_suggestions,
          visual_feedback: aiResponse.response.visual_feedback
        });

      } else {
        throw new Error(aiResponse.error || 'AI processing failed');
      }
    } catch (error) {
      console.error('Enhanced AI chat error:', error);
      addChatMessage('ai', `❌ I encountered an error: ${error.message}. Please try again.`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleVoiceCommand = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      addChatMessage('ai', '❌ Voice commands not supported in this browser.');
      return;
    }

    try {
      setVoiceRecording(true);
      addChatMessage('ai', '🎤 Listening... Speak your command now.');

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'voice_command.wav');
        formData.append('session_id', sessionId);

        try {
          const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
          const response = await fetch(`${backendUrl}/api/ai/voice-command`, {
            method: 'POST',
            body: formData
          });

          const result = await response.json();
          
          if (result.success) {
            const transcription = result.transcription?.transcription || 'Voice command received';
            addChatMessage('user', `🎤 ${transcription}`);
            
            if (result.response) {
              addChatMessage('ai', result.response.explanation || 'Voice command processed');
            }
          } else {
            throw new Error(result.error || 'Voice processing failed');
          }
        } catch (error) {
          addChatMessage('ai', `❌ Voice processing error: ${error.message}`);
        }

        stream.getTracks().forEach(track => track.stop());
        setVoiceRecording(false);
      };

      mediaRecorder.start();

      // Stop recording after 5 seconds
      setTimeout(() => {
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
        }
      }, 5000);

    } catch (error) {
      console.error('Voice command error:', error);
      addChatMessage('ai', `❌ Voice command failed: ${error.message}`);
      setVoiceRecording(false);
    }
  };

  const handleImageAnalysis = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setImageAnalyzing(true);
    addChatMessage('ai', '📸 Analyzing image...');

    try {
      const formData = new FormData();
      formData.append('image_file', file);
      formData.append('query', 'Analyze this image and tell me what you see');
      formData.append('session_id', sessionId);

      const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
      const response = await fetch(`${backendUrl}/api/ai/analyze-image`, {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.success) {
        const analysis = result.image_analysis;
        let analysisText = '📸 **Image Analysis Complete:**\n\n';
        
        if (analysis?.dimensions) {
          analysisText += `📏 **Dimensions:** ${analysis.dimensions[0]} × ${analysis.dimensions[1]} pixels\n`;
        }
        
        if (analysis?.dominant_colors?.length > 0) {
          analysisText += `🎨 **Dominant Colors:** ${analysis.dominant_colors.slice(0, 3).join(', ')}\n`;
        }
        
        if (analysis?.detected_elements) {
          analysisText += `🔍 **UI Elements Detected:** ${JSON.stringify(analysis.detected_elements, null, 2)}\n`;
        }

        if (result.response?.explanation) {
          analysisText += `\n💭 **AI Analysis:** ${result.response.explanation}`;
        }

        addChatMessage('ai', analysisText);
      } else {
        throw new Error(result.error || 'Image analysis failed');
      }
    } catch (error) {
      console.error('Image analysis error:', error);
      addChatMessage('ai', `❌ Image analysis failed: ${error.message}`);
    } finally {
      setImageAnalyzing(false);
    }
  };

  const enhancedQuickCommands = [
    { text: 'Test stealth on this site', icon: '🥷', action: 'stealth_test' },
    { text: 'Analyze page performance', icon: '📊', action: 'performance_analysis' },
    { text: 'Extract all links', icon: '🔗', action: 'extract_links' },
    { text: 'Take enhanced screenshot', icon: '📸', action: 'screenshot' },
    { text: 'Check anti-bot measures', icon: '🛡️', action: 'anti_bot_check' },
    { text: 'Optimize page rendering', icon: '⚡', action: 'optimize_rendering' }
  ];

  const handleQuickCommand = async (command) => {
    addChatMessage('user', command.text);
    
    try {
      if (command.action === 'stealth_test' && currentUrl) {
        const domain = new URL(currentUrl).hostname;
        const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
        
        const response = await fetch(`${backendUrl}/api/stealth/test/${domain}`);
        const result = await response.json();
        
        if (result.success) {
          let testResult = `🥷 **Stealth Test Results for ${domain}:**\n\n`;
          testResult += `🛡️ **Anti-Bot Detections:**\n`;
          
          const detections = result.anti_bot_detections || {};
          Object.entries(detections).forEach(([key, value]) => {
            if (value === true) {
              testResult += `• ${key.replace('_', ' ')}: ✅ Detected\n`;
            }
          });
          
          testResult += `\n🔧 **Adaptive Responses:**\n`;
          const responses = result.adaptive_responses?.responses_applied || [];
          responses.forEach(response => {
            testResult += `• ${response.replace('_', ' ')}: Applied\n`;
          });
          
          testResult += `\n⭐ **Stealth Level:** ${result.stealth_level}/5`;
          
          addChatMessage('ai', testResult);
        }
      } else {
        // Handle other commands with enhanced AI
        await handleAIChat({ preventDefault: () => {}, target: { value: command.text } });
      }
    } catch (error) {
      addChatMessage('ai', `❌ Command failed: ${error.message}`);
    }
  };

  // Helper functions
  const normalizeUrl = (url) => {
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      if (url.includes('.') && !url.includes(' ')) {
        return 'https://' + url;
      } else {
        return `https://www.google.com/search?q=${encodeURIComponent(url)}`;
      }
    }
    return url;
  };

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

  const addChatMessage = (type, content, metadata = {}) => {
    const message = { type, content, timestamp: new Date(), metadata };
    setChatMessages(prev => [...prev, message]);
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

  const createNewTab = useCallback(() => {
    const newTabId = Math.max(...tabs.map(t => t.id)) + 1;
    const newTab = { 
      id: newTabId, url: '', title: 'New Tab', 
      active: false, loading: false, favicon: '🌐'
    };
    setTabs(prev => prev.map(tab => ({ ...tab, active: false })).concat({ ...newTab, active: true }));
    setActiveTab(newTabId);
    setIframeContent('');
    setUrlInput('');
  }, [tabs]);

  return (
    <div className={`browser-container h-screen flex flex-col bg-gray-50 ${isFullscreen ? 'fullscreen' : ''}`}>
      {/* Ultimate Enhanced Browser Header */}
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

          {/* Ultimate Enhanced URL Bar */}
          <form onSubmit={handleUrlSubmit} className="flex-1 max-w-2xl">
            <div className="relative">
              <div className="absolute left-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-2">
                {isLoading ? (
                  <div className="loading-spinner w-4 h-4"></div>
                ) : (
                  <>
                    <Shield className="w-4 h-4 text-green-500" />
                    <span className="text-xs text-green-600 font-medium">ULTIMATE</span>
                  </>
                )}
              </div>
              <input
                type="text"
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder={currentUrl || "Enter URL for ultimate browsing experience..."}
                className="w-full pl-24 pr-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
              />
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <button type="submit" className="text-gray-400 hover:text-gray-600 transition-colors">
                  <Search className="w-4 h-4" />
                </button>
              </div>
            </div>
          </form>

          {/* Ultimate Browser Controls */}
          <div className="flex items-center space-x-2">
            {/* Performance Metrics Display */}
            <div className="flex items-center space-x-1 text-xs bg-gradient-to-r from-green-50 to-blue-50 px-3 py-1.5 rounded-lg border border-green-200">
              <Activity className="w-3 h-3 text-green-600" />
              <span className="text-green-700 font-medium">{performanceMetrics.request_time}ms</span>
              <div className="w-1 h-1 bg-green-400 rounded-full mx-1"></div>
              <span className="text-blue-700 text-xs">{performanceMetrics.tier_used?.split('_')[1] || 'Auto'}</span>
            </div>
            
            {/* Stealth Level Indicator */}
            <div className="flex items-center space-x-1 text-xs bg-purple-50 px-2 py-1 rounded border border-purple-200">
              <Target className="w-3 h-3 text-purple-600" />
              <span className="text-purple-700">Stealth {userPreferences.stealth_level}/5</span>
            </div>
            
            <div className="flex items-center space-x-1 text-xs text-gray-500 bg-gray-100 px-3 py-1.5 rounded-lg">
              {isOnline ? (
                <Wifi className="w-3 h-3 text-green-500" />
              ) : (
                <WifiOff className="w-3 h-3 text-red-500" />
              )}
              <span>{isOnline ? 'Ultimate Online' : 'Offline'}</span>
            </div>
            
            <div className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              Session: {sessionId?.slice(-8)}
            </div>
            
            <button 
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Ultimate Settings"
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
                      // Tab close logic here
                    }}
                    className="ml-2 p-0.5 hover:bg-gray-200 rounded transition-colors"
                  >
                    <X className="w-3 h-3 text-gray-400" />
                  </button>
                )}
              </div>
            ))}
            <button 
              onClick={createNewTab}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors ml-2"
              title="New Ultimate Tab"
            >
              <Plus className="w-4 h-4 text-gray-500" />
            </button>
          </div>

          <button
            onClick={() => setShowBookmarks(!showBookmarks)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Enhanced Bookmarks"
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

      {/* Ultimate Browser Content */}
      <main className="flex-1 relative bg-white">        
        {iframeContent ? (
          <div className="w-full h-full relative">
            <div 
              className="w-full h-full"
              dangerouslySetInnerHTML={{ __html: iframeContent }}
            />
          </div>
        ) : (
          <div className="flex items-center justify-center h-full bg-gradient-to-br from-gray-50 via-blue-50 to-green-50">
            <div className="text-center max-w-md">
              <div className="w-20 h-20 bg-gradient-to-br from-green-400 via-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-xl">
                <Brain className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-3">Ultimate AI Browser Ready</h3>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Experience the next generation of web browsing with military-grade stealth, 
                AI-powered interactions, and bulletproof reliability.
              </p>
              
              {/* System Status */}
              {systemAnalytics && (
                <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-200 mb-6">
                  <h4 className="font-semibold text-gray-800 mb-2">🚀 System Status</h4>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span>6 Phases Active</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                      <span>Stealth Level 5</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <button 
                  onClick={() => setIsChatOpen(true)}
                  className="bg-gradient-to-r from-green-500 via-blue-500 to-purple-600 text-white px-6 py-3 rounded-xl font-medium hover:shadow-lg transition-all duration-200 flex items-center space-x-2 justify-center"
                >
                  <Bot className="w-5 h-5" />
                  <span>Open Ultimate AI</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Ultimate Enhanced AI Assistant Button */}
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

      {/* Ultimate Enhanced AI Chat Panel */}
      <AnimatePresence>
        {isChatOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="ai-chat-panel fixed bottom-24 right-6 w-96 h-[650px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col z-40 overflow-hidden"
          >
            {/* Ultimate Chat Header */}
            <div className="bg-gradient-to-r from-green-500 via-blue-500 to-purple-600 text-white rounded-t-2xl p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                    <Brain className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-semibold">Ultimate Kairo AI</h3>
                    <p className="text-xs text-white/90">
                      Multi-Modal • Voice • Vision • Intelligence
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button 
                    onClick={handleVoiceCommand}
                    disabled={voiceRecording}
                    className={`p-2 rounded-lg transition-colors ${
                      voiceRecording 
                        ? 'bg-red-500/20 text-red-200' 
                        : 'hover:bg-white/20 text-white'
                    }`}
                    title="Voice Command"
                  >
                    {voiceRecording ? <Headphones className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                  </button>
                  
                  <label className="p-2 hover:bg-white/20 rounded-lg cursor-pointer transition-colors">
                    <ImageIcon className="w-4 h-4" />
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageAnalysis}
                      className="hidden"
                    />
                  </label>
                  
                  <button 
                    onClick={() => setIsChatOpen(false)}
                    className="p-2 hover:bg-white/20 rounded-lg transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            {/* Ultimate Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50 to-white">
              {chatMessages.map((message, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`ai-chat-bubble flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
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

            {/* Ultimate Quick Commands */}
            {chatMessages.length <= 3 && (
              <div className="px-4 py-3 border-t border-gray-100 bg-gradient-to-r from-gray-50 to-blue-50">
                <p className="text-xs text-gray-600 mb-3 font-medium">✨ Ultimate Commands:</p>
                <div className="grid grid-cols-1 gap-2">
                  {enhancedQuickCommands.slice(0, 4).map((cmd, index) => (
                    <button
                      key={index}
                      onClick={() => handleQuickCommand(cmd)}
                      className="text-xs bg-white border border-gray-200 rounded-lg px-3 py-2 hover:shadow-sm hover:border-blue-300 transition-all duration-200 flex items-center space-x-2 text-left"
                    >
                      <span className="text-base">{cmd.icon}</span>
                      <span className="truncate text-gray-700">{cmd.text}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Ultimate Chat Input */}
            <form onSubmit={handleAIChat} className="p-4 border-t border-gray-100 bg-white rounded-b-2xl">
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={currentMessage}
                  onChange={(e) => setCurrentMessage(e.target.value)}
                  placeholder="Ask anything... Voice, text, or images supported"
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

      {/* Ultimate Settings Panel */}
      <AnimatePresence>
        {showSettings && (
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className="fixed top-0 right-0 w-96 h-full bg-white shadow-2xl z-40 border-l border-gray-200 overflow-y-auto"
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-800">Ultimate Browser Settings</h3>
                <button onClick={() => setShowSettings(false)}>
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>
              
              <div className="space-y-6">
                {/* Performance Settings */}
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center space-x-2">
                    <Cpu className="w-4 h-4" />
                    <span>Performance & Routing</span>
                  </h4>
                  <div className="space-y-3">
                    <label className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Prefer Speed</span>
                      <input
                        type="checkbox"
                        checked={userPreferences.prefer_speed}
                        onChange={(e) => setUserPreferences(prev => ({
                          ...prev,
                          prefer_speed: e.target.checked
                        }))}
                        className="rounded border-gray-300"
                      />
                    </label>
                    <label className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Prefer Reliability</span>
                      <input
                        type="checkbox"
                        checked={userPreferences.prefer_reliability}
                        onChange={(e) => setUserPreferences(prev => ({
                          ...prev,
                          prefer_reliability: e.target.checked
                        }))}
                        className="rounded border-gray-300"
                      />
                    </label>
                  </div>
                </div>

                {/* Stealth Settings */}
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center space-x-2">
                    <Target className="w-4 h-4" />
                    <span>Stealth Protection</span>
                  </h4>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm text-gray-600 mb-2">
                        Stealth Level: {userPreferences.stealth_level}/5
                      </label>
                      <input
                        type="range"
                        min="1"
                        max="5"
                        value={userPreferences.stealth_level}
                        onChange={(e) => setUserPreferences(prev => ({
                          ...prev,
                          stealth_level: parseInt(e.target.value)
                        }))}
                        className="w-full"
                      />
                      <div className="flex justify-between text-xs text-gray-500 mt-1">
                        <span>Basic</span>
                        <span>Military</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Rendering Settings */}
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center space-x-2">
                    <Layers className="w-4 h-4" />
                    <span>Rendering Engine</span>
                  </h4>
                  <select 
                    value={userPreferences.rendering_profile}
                    onChange={(e) => setUserPreferences(prev => ({
                      ...prev,
                      rendering_profile: e.target.value
                    }))}
                    className="w-full p-2 border border-gray-300 rounded-lg text-sm"
                  >
                    <option value="performance_optimized">Performance Optimized</option>
                    <option value="quality_optimized">Quality Optimized</option>
                    <option value="balanced">Balanced</option>
                    <option value="mobile_optimized">Mobile Optimized</option>
                  </select>
                </div>

                {/* System Analytics */}
                {systemAnalytics && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-3 flex items-center space-x-2">
                      <Activity className="w-4 h-4" />
                      <span>System Status</span>
                    </h4>
                    <div className="bg-gray-50 rounded-lg p-3 space-y-2">
                      {systemAnalytics.integration_status && (
                        <div className="text-xs">
                          <span className="text-gray-600">Integration: </span>
                          <span className="text-green-600 font-medium">
                            {systemAnalytics.integration_status.phases_integrated} Phases Active
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default UltimateEnhancedBrowserInterface;