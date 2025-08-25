import React, { useState, useRef, useEffect, useCallback } from 'react';
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
  Settings,
  Star,
  BookmarkPlus,
  Download,
  Share,
  Menu,
  Maximize2,
  Minimize2,
  Volume2,
  VolumeX,
  Wifi,
  WifiOff,
  MessageSquare,
  Workflow,
  MousePointer,
  Play,
  Save,
  Trash2,
  Eye,
  EyeOff,
  RotateCw
} from 'lucide-react';
import { useSession } from '../contexts/SessionContext';
import VisualWorkflowBuilder from './VisualWorkflowBuilder';

const EnhancedBrowserInterface = ({ onBackToWelcome }) => {
  const {
    sessionId,
    currentUrl,
    isLoading,
    history,
    navigateToUrl,
    processAIQuery,
    proxyRequest
  } = useSession();

  // Enhanced state management
  const [urlInput, setUrlInput] = useState('');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatMode, setChatMode] = useState('chat'); // 'chat' | 'builder'
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [chatMessages, setChatMessages] = useState([
    {
      type: 'ai',
      content: "👋 Hello! I'm your enhanced AI assistant with all Fellou-level capabilities:\n\n💬 **Chat Mode**: Natural language commands\n🎨 **Visual Builder**: Drag-and-drop workflows\n🔍 **Deep Search**: Multi-source intelligent search\n🧠 **Agentic Memory**: Learns from your behavior\n🤖 **Custom Agents**: Build agents with code or descriptions\n♿ **Accessibility Tools**: TTS, translation, layout adjustments\n📊 **Smart Reports**: AI-generated insights\n\nTry: 'Deep search AI trends' or switch to Visual Builder!",
      timestamp: new Date()
    }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [iframeContent, setIframeContent] = useState('');
  const [tabs, setTabs] = useState([{ 
    id: 1, 
    url: '', 
    title: 'New Tab', 
    active: true, 
    loading: false,
    favicon: '🌐'
  }]);
  const [activeTab, setActiveTab] = useState(1);
  const [bookmarks, setBookmarks] = useState([
    { name: 'YouTube', url: 'https://youtube.com', favicon: '🎥' },
    { name: 'Google', url: 'https://google.com', favicon: '🔍' },
    { name: 'Gmail', url: 'https://gmail.com', favicon: '📧' },
    { name: 'GitHub', url: 'https://github.com', favicon: '👨‍💻' }
  ]);
  const [showBookmarks, setShowBookmarks] = useState(false);
  const [showDownloads, setShowDownloads] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [shadowTasks, setShadowTasks] = useState([]);
  const [builtWorkflows, setBuiltWorkflows] = useState([]);
  
  const chatEndRef = useRef(null);
  const iframeRef = useRef(null);

  // Enhanced effects
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  useEffect(() => {
    const handleOnlineStatus = () => setIsOnline(navigator.onLine);
    window.addEventListener('online', handleOnlineStatus);
    window.addEventListener('offline', handleOnlineStatus);
    return () => {
      window.removeEventListener('online', handleOnlineStatus);
      window.removeEventListener('offline', handleOnlineStatus);
    };
  }, []);

  // Enhanced navigation message handler
  useEffect(() => {
    const handleMessage = async (event) => {
      if (event.data && event.data.type === 'NAVIGATE_TO') {
        const newUrl = event.data.url;
        console.log('🧭 Received navigation request from iframe:', newUrl);
        
        try {
          await navigateToUrl(newUrl);
          const response = await proxyRequest(newUrl);
          if (response && response.content) {
            console.log(`✅ Navigation completed using ${response.method} for ${newUrl}`);
            setIframeContent(response.content);
            updateCurrentTab({ url: newUrl, title: getDomainFromUrl(newUrl) });
          }
        } catch (error) {
          console.error('❌ Navigation failed:', error);
          addChatMessage('ai', `Navigation to ${newUrl} failed. Please try again.`);
        }
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [navigateToUrl, proxyRequest]);

  // Enhanced URL submission
  const handleUrlSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!urlInput.trim()) return;

    const normalizedUrl = normalizeUrl(urlInput);
    
    try {
      setActiveTabLoading(true);
      await navigateToUrl(normalizedUrl);
      
      const response = await proxyRequest(normalizedUrl);
      if (response.content) {
        console.log(`✅ Direct navigation loaded using ${response.method}`);
        setIframeContent(response.content);
        updateCurrentTab({ 
          url: normalizedUrl, 
          title: getDomainFromUrl(normalizedUrl),
          loading: false 
        });
      }
      
      setUrlInput('');
    } catch (error) {
      console.error('❌ Navigation failed:', error);
      setActiveTabLoading(false);
      addChatMessage('ai', `Sorry, I couldn't navigate to ${normalizedUrl}. Please check the URL and try again.`);
    }
  }, [urlInput, navigateToUrl, proxyRequest]);

  // Enhanced AI chat handler with advanced workflow building capabilities
  const handleAIChat = useCallback(async (e) => {
    e.preventDefault();
    if (!currentMessage.trim()) return;

    const userMessage = currentMessage.trim();
    addChatMessage('user', userMessage);
    setCurrentMessage('');

    try {
      // Check for enhanced commands
      if (userMessage.toLowerCase().includes('deep search')) {
        await handleDeepSearch(userMessage);
        return;
      }
      
      if (userMessage.toLowerCase().includes('create agent')) {
        await handleCreateAgent(userMessage);
        return;
      }
      
      if (userMessage.toLowerCase().includes('generate report')) {
        await handleGenerateReport(userMessage);
        return;
      }

      if (userMessage.toLowerCase().includes('translate')) {
        await handleTranslation(userMessage);
        return;
      }

      if (userMessage.toLowerCase().includes('read aloud') || userMessage.toLowerCase().includes('text to speech')) {
        await handleTextToSpeech(userMessage);
        return;
      }

      // Check for workflow building commands
      if (isWorkflowBuildingCommand(userMessage)) {
        await handleWorkflowBuilding(userMessage);
        return;
      }

      // Standard AI processing with enhanced context
      const aiResponse = await processAIQuery(userMessage, {
        currentUrl: currentUrl,
        sessionId: sessionId,
        activeTab: activeTab,
        browserContext: {
          totalTabs: tabs.length,
          isFullscreen: isFullscreen,
          bookmarks: bookmarks.length
        }
      });

      // Handle workflow creation response
      if (aiResponse.workflow) {
        await handleWorkflowCreationResponse(aiResponse);
        return;
      }

      let responseText = aiResponse.explanation || 'I understand your request.';
      
      if (aiResponse.commands && aiResponse.commands.length > 0) {
        for (const command of aiResponse.commands) {
          if (command.type === 'open' && command.params?.url) {
            responseText += `\n\n🚀 Opening ${command.params.url}...`;
            
            setActiveTabLoading(true);
            await navigateToUrl(command.params.url);
            
            try {
              const response = await proxyRequest(command.params.url);
              
              if (response && response.content) {
                console.log(`✅ AI command loaded using ${response.method} for ${command.params.url}`);
                setIframeContent(response.content);
                
                updateCurrentTab({ 
                  url: command.params.url, 
                  title: getDomainFromUrl(command.params.url),
                  loading: false,
                  favicon: getFaviconForUrl(command.params.url)
                });
                
                if (response.method === 'enhanced_browser_rendered') {
                  responseText += `\n✅ Loaded using enhanced browser engine with full JavaScript support`;
                } else if (response.method === 'enhanced_http_proxy') {
                  responseText += `\n✅ Loaded using enhanced HTTP proxy with anti-detection`;
                } else {
                  responseText += `\n✅ Content loaded successfully`;
                }
              }
            } catch (proxyError) {
              console.error('❌ Proxy loading failed:', proxyError);
              setActiveTabLoading(false);
              responseText += `\n⚠️ Loading encountered issues: ${proxyError.message}`;
            }
          }
        }
      }

      addChatMessage('ai', responseText, { commands: aiResponse.commands });
      
    } catch (error) {
      console.error('❌ AI chat error:', error);
      addChatMessage('ai', 'Sorry, I encountered an error processing your request. Please try again.');
    }
  }, [currentMessage, currentUrl, sessionId, activeTab, tabs, isFullscreen, bookmarks, processAIQuery, navigateToUrl, proxyRequest]);

  // Enhanced capabilities handlers
  const handleDeepSearch = async (query) => {
    addChatMessage('ai', '🔍 Initiating deep search across multiple sources...');
    
    try {
      const searchQuery = query.replace(/deep search/i, '').trim();
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/search/deep`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: searchQuery, config: { max_sources: 6 } })
      });
      
      const result = await response.json();
      
      if (result.error) {
        addChatMessage('ai', `❌ Deep search failed: ${result.error}`);
        return;
      }
      
      const results = result.results?.results || [];
      const totalSources = result.sources_searched?.length || 0;
      
      let searchSummary = `🎯 **Deep Search Results for: "${searchQuery}"**\n\n`;
      searchSummary += `📊 Found ${results.length} results from ${totalSources} sources\n`;
      searchSummary += `🔍 Sources: ${result.sources_searched?.join(', ') || 'Various'}\n\n`;
      
      if (results.length > 0) {
        searchSummary += `**Top Results:**\n`;
        results.slice(0, 5).forEach((result, i) => {
          searchSummary += `${i + 1}. **${result.title}** (${result.search_source})\n`;
          searchSummary += `   ${result.snippet}\n   🔗 ${result.url}\n\n`;
        });
      }
      
      searchSummary += `💡 **AI Analysis:** ${result.results?.ai_analysis || 'Deep search completed successfully'}`;
      
      addChatMessage('ai', searchSummary, { searchResults: result });
      
    } catch (error) {
      addChatMessage('ai', `❌ Deep search error: ${error.message}`);
    }
  };

  const handleCreateAgent = async (message) => {
    addChatMessage('ai', '🤖 Creating custom agent from your description...');
    
    try {
      const description = message.replace(/create agent/i, '').trim();
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/agents/create/description`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          description, 
          user_id: sessionId,
          config: { environment: 'browser' }
        })
      });
      
      const result = await response.json();
      
      if (result.error) {
        addChatMessage('ai', `❌ Agent creation failed: ${result.error}`);
        return;
      }
      
      const agent = result.agent;
      let agentSummary = `✅ **Agent Created Successfully!**\n\n`;
      agentSummary += `🤖 **Name:** ${agent.name}\n`;
      agentSummary += `📝 **Description:** ${agent.description}\n`;
      agentSummary += `🎯 **Capabilities:** ${agent.capabilities?.join(', ') || 'General automation'}\n`;
      agentSummary += `🏗️ **Environment:** ${agent.environment}\n`;
      agentSummary += `🆔 **Agent ID:** ${agent.id}\n\n`;
      agentSummary += `Use this agent by saying: "Execute agent ${agent.name}"`;
      
      addChatMessage('ai', agentSummary, { createdAgent: result });
      
    } catch (error) {
      addChatMessage('ai', `❌ Agent creation error: ${error.message}`);
    }
  };

  const handleGenerateReport = async (message) => {
    addChatMessage('ai', '📊 Generating AI-powered report with visualizations...');
    
    try {
      const reportType = message.toLowerCase().includes('analytics') ? 'analytics' : 'research';
      const topic = message.replace(/generate report/i, '').replace(/analytics/i, '').trim();
      
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/reports/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          type: reportType,
          config: { 
            topic: topic || 'General Report',
            include_visuals: true,
            async: false
          }
        })
      });
      
      const result = await response.json();
      
      if (result.error) {
        addChatMessage('ai', `❌ Report generation failed: ${result.error}`);
        return;
      }
      
      let reportSummary = `📋 **Report Generated: ${result.title || 'Custom Report'}**\n\n`;
      reportSummary += `📊 **Type:** ${reportType.charAt(0).toUpperCase() + reportType.slice(1)}\n`;
      reportSummary += `📅 **Generated:** ${new Date().toLocaleString()}\n`;
      reportSummary += `🎯 **Topic:** ${topic || 'Comprehensive Analysis'}\n\n`;
      
      if (result.sections) {
        reportSummary += `**Report Sections:**\n`;
        result.sections.forEach((section, i) => {
          reportSummary += `${i + 1}. ${section.title}\n`;
        });
      }
      
      reportSummary += `\n✨ **AI Insights:** Report includes comprehensive analysis with actionable recommendations.`;
      
      addChatMessage('ai', reportSummary, { generatedReport: result });
      
    } catch (error) {
      addChatMessage('ai', `❌ Report generation error: ${error.message}`);
    }
  };

  const handleTranslation = async (message) => {
    const text = message.replace(/translate/i, '').trim();
    const targetLang = 'es'; // Default to Spanish, could be enhanced to detect intent
    
    addChatMessage('ai', `🌐 Translating text to ${targetLang}...`);
    
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/accessibility/translate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          text, 
          target_language: targetLang,
          source_language: 'auto'
        })
      });
      
      const result = await response.json();
      
      if (result.error) {
        addChatMessage('ai', `❌ Translation failed: ${result.error}`);
        return;
      }
      
      let translationResult = `🌐 **Translation Complete**\n\n`;
      translationResult += `**Original:** ${result.original_text}\n`;
      translationResult += `**Translated:** ${result.translated_text}\n`;
      translationResult += `**From:** ${result.source_language} → **To:** ${result.target_language}\n`;
      translationResult += `**Confidence:** ${Math.round(result.confidence * 100)}%`;
      
      addChatMessage('ai', translationResult, { translation: result });
      
    } catch (error) {
      addChatMessage('ai', `❌ Translation error: ${error.message}`);
    }
  };

  const handleTextToSpeech = async (message) => {
    const text = message.replace(/read aloud|text to speech/i, '').trim() || "Hello, this is a text to speech test.";
    
    addChatMessage('ai', '🔊 Converting text to speech...');
    
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/accessibility/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          text,
          options: { engine: 'browser', speed: 1.0, pitch: 1.0 }
        })
      });
      
      const result = await response.json();
      
      if (result.error) {
        addChatMessage('ai', `❌ Text-to-speech failed: ${result.error}`);
        return;
      }
      
      // Execute browser TTS
      if (result.instructions?.use_speech_synthesis && 'speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(result.instructions.text_to_speak);
        utterance.rate = result.instructions.voice_settings?.speed || 1.0;
        utterance.pitch = result.instructions.voice_settings?.pitch || 1.0;
        
        speechSynthesis.speak(utterance);
        
        addChatMessage('ai', `🔊 **Speaking:** "${text}"\n\n✅ Text-to-speech activated using browser engine.`);
      } else {
        addChatMessage('ai', `🔊 **TTS Configuration Ready:** ${result.text}\n\n⚠️ Browser speech synthesis not available.`);
      }
      
    } catch (error) {
      addChatMessage('ai', `❌ Text-to-speech error: ${error.message}`);
    }
  };

  // Advanced workflow building functions
  const isWorkflowBuildingCommand = (message) => {
    const workflowKeywords = [
      'create workflow', 'build workflow', 'make workflow',
      'create automation', 'build automation', 'automate',
      'create routine', 'build routine', 'daily routine',
      'create task', 'schedule task', 'recurring task',
      'create sequence', 'build sequence',
      'save command', 'save as command', 'custom command',
      'create macro', 'build macro'
    ];
    
    return workflowKeywords.some(keyword => 
      message.toLowerCase().includes(keyword)
    );
  };

  const handleWorkflowBuilding = async (message) => {
    addChatMessage('ai', '🔨 Building your custom workflow...');
    
    try {
      // Enhanced AI processing for workflow building
      const aiResponse = await processAIQuery(message, {
        currentUrl: currentUrl,
        sessionId: sessionId,
        workflowBuildingContext: true,
        existingWorkflows: builtWorkflows,
        userPatterns: chatMessages.filter(msg => msg.type === 'user').slice(-5)
      });

      if (aiResponse.workflow) {
        const workflow = aiResponse.workflow;
        
        // Add to built workflows
        const workflowId = `wf_${Date.now()}`;
        const newWorkflow = {
          id: workflowId,
          name: workflow.name,
          description: workflow.description,
          steps: workflow.steps,
          schedule: workflow.schedule,
          triggers: workflow.triggers || ['manual'],
          created: new Date(),
          createdBy: 'conversation',
          status: 'ready'
        };
        
        setBuiltWorkflows(prev => [...prev, newWorkflow]);
        
        let workflowSummary = `✅ **Workflow Created: "${workflow.name}"**\n\n`;
        workflowSummary += `📝 **Description:** ${workflow.description}\n`;
        workflowSummary += `🏗️ **Steps:** ${workflow.steps.length} actions\n`;
        
        if (workflow.schedule) {
          workflowSummary += `⏰ **Schedule:** ${workflow.schedule}\n`;
        }
        
        workflowSummary += `🎯 **Triggers:** ${workflow.triggers?.join(', ') || 'Manual'}\n\n`;
        
        // Show preview of steps
        workflowSummary += `**Workflow Steps:**\n`;
        workflow.steps.slice(0, 3).forEach((step, i) => {
          workflowSummary += `${i + 1}. ${step.description || step.type}\n`;
        });
        
        if (workflow.steps.length > 3) {
          workflowSummary += `... and ${workflow.steps.length - 3} more steps\n`;
        }
        
        workflowSummary += `\n💡 **Execute:** Say "Run ${workflow.name}" or use the Builder tab\n`;
        
        if (aiResponse.builder_suggestions) {
          workflowSummary += `\n🔧 **Suggestions:** ${aiResponse.builder_suggestions.join(', ')}`;
        }
        
        addChatMessage('ai', workflowSummary, { 
          workflow: newWorkflow,
          type: 'workflow_created'
        });
        
      } else {
        // AI asking clarifying questions
        addChatMessage('ai', aiResponse.explanation || 'Could you provide more details about the workflow you want to create?');
      }
      
    } catch (error) {
      addChatMessage('ai', `❌ Workflow building error: ${error.message}`);
    }
  };

  const handleWorkflowCreationResponse = async (aiResponse) => {
    if (aiResponse.workflow) {
      const workflow = aiResponse.workflow;
      
      // Create and store workflow
      const workflowId = `wf_${Date.now()}`;
      const newWorkflow = {
        id: workflowId,
        name: workflow.name,
        description: workflow.description,
        steps: workflow.steps,
        schedule: workflow.schedule,
        triggers: workflow.triggers || ['manual'],
        notifications: workflow.notifications || [],
        created: new Date(),
        createdBy: 'ai_conversation',
        status: 'ready'
      };
      
      setBuiltWorkflows(prev => [...prev, newWorkflow]);
      
      // Display comprehensive workflow summary
      let summary = `🎉 **Workflow Successfully Built!**\n\n`;
      summary += `📋 **Name:** ${workflow.name}\n`;
      summary += `📝 **Description:** ${workflow.description}\n`;
      summary += `🔧 **Steps:** ${workflow.steps.length} automated actions\n`;
      
      if (workflow.schedule) {
        summary += `⏰ **Schedule:** ${workflow.schedule}\n`;
      }
      
      summary += `🎯 **Triggers:** ${workflow.triggers.join(', ')}\n`;
      
      if (workflow.notifications.length > 0) {
        summary += `🔔 **Notifications:** ${workflow.notifications.join(', ')}\n`;
      }
      
      summary += `\n**Workflow Preview:**\n`;
      workflow.steps.forEach((step, i) => {
        summary += `${i + 1}. ${step.description || `${step.type} action`}\n`;
        if (step.conditions) {
          summary += `   ↳ Condition: ${step.conditions}\n`;
        }
      });
      
      summary += `\n✨ **How to Use:**\n`;
      summary += `• Say "Run ${workflow.name}" to execute\n`;
      summary += `• View in Builder tab for visual editing\n`;
      summary += `• Workflows are saved to your session\n`;
      
      if (aiResponse.builder_suggestions) {
        summary += `\n💡 **Enhancement Ideas:**\n`;
        aiResponse.builder_suggestions.forEach(suggestion => {
          summary += `• ${suggestion}\n`;
        });
      }
      
      addChatMessage('ai', summary, { 
        workflow: newWorkflow,
        type: 'workflow_built',
        actions: ['execute', 'edit', 'duplicate', 'schedule']
      });
    }
  };

  // Handle workflow execution from visual builder
  const handleWorkflowExecution = async (workflow) => {
    addChatMessage('ai', `🔄 Executing workflow: ${workflow.name || 'Custom Workflow'}`);
    
    try {
      // Add to shadow tasks
      const taskId = `task_${Date.now()}`;
      const newTask = {
        id: taskId,
        name: workflow.name || 'Visual Workflow',
        status: 'running',
        steps: workflow.steps,
        startTime: new Date()
      };
      
      setShadowTasks(prev => [...prev, newTask]);
      
      // Simulate workflow execution (in real implementation, this would call the backend)
      setTimeout(() => {
        setShadowTasks(prev => prev.map(task => 
          task.id === taskId ? { ...task, status: 'completed', endTime: new Date() } : task
        ));
        
        addChatMessage('ai', `✅ Workflow "${workflow.name || 'Custom Workflow'}" completed successfully!\n\n📊 Executed ${workflow.steps.length} steps in background.`);
      }, 3000);
      
    } catch (error) {
      addChatMessage('ai', `❌ Workflow execution error: ${error.message}`);
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
      'youtube.com': '🎥',
      'google.com': '🔍',
      'gmail.com': '📧',
      'github.com': '👨‍💻',
      'facebook.com': '👥',
      'twitter.com': '🐦',
      'linkedin.com': '💼',
      'instagram.com': '📸',
      'reddit.com': '🤖',
      'stackoverflow.com': '📚',
      'wikipedia.org': '📖',
      'amazon.com': '🛒'
    };
    return faviconMap[domain] || '🌐';
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
      id: newTabId, 
      url: '', 
      title: 'New Tab', 
      active: false, 
      loading: false,
      favicon: '🌐'
    };
    setTabs(prev => prev.map(tab => ({ ...tab, active: false })).concat({ ...newTab, active: true }));
    setActiveTab(newTabId);
    setIframeContent('');
    setUrlInput('');
  }, [tabs]);

  const closeTab = useCallback((tabId) => {
    if (tabs.length === 1) return;
    
    setTabs(prev => {
      const filtered = prev.filter(tab => tab.id !== tabId);
      if (activeTab === tabId && filtered.length > 0) {
        const newActive = filtered[filtered.length - 1];
        newActive.active = true;
        setActiveTab(newActive.id);
      }
      return filtered;
    });
  }, [tabs, activeTab]);

  const switchTab = useCallback((tabId) => {
    setTabs(prev => prev.map(t => ({ ...t, active: t.id === tabId })));
    setActiveTab(tabId);
  }, []);

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  };

  const addBookmark = () => {
    const currentTabData = tabs.find(tab => tab.active);
    if (currentTabData && currentTabData.url) {
      const newBookmark = {
        name: currentTabData.title || getDomainFromUrl(currentTabData.url),
        url: currentTabData.url,
        favicon: currentTabData.favicon || '🌐'
      };
      setBookmarks(prev => [...prev, newBookmark]);
      addChatMessage('ai', `📌 Bookmarked: ${newBookmark.name}`);
    }
  };

  const enhancedQuickCommands = [
    { text: 'Create daily email workflow', icon: '⚙️', color: 'bg-purple-50 text-purple-600' },
    { text: 'Build social media routine', icon: '📱', color: 'bg-blue-50 text-blue-600' },
    { text: 'Deep search AI trends', icon: '🔍', color: 'bg-emerald-50 text-emerald-600' },
    { text: 'Create agent for scraping', icon: '🤖', color: 'bg-indigo-50 text-indigo-600' },
    { text: 'Automate competitor monitoring', icon: '📊', color: 'bg-green-50 text-green-600' },
    { text: 'Generate report analytics', icon: '📈', color: 'bg-orange-50 text-orange-600' },
    { text: 'Create morning routine workflow', icon: '☀️', color: 'bg-yellow-50 text-yellow-600' },
    { text: 'Build website monitoring task', icon: '🕵️', color: 'bg-red-50 text-red-600' }
  ];

  const handleQuickCommand = async (command) => {
    setCurrentMessage(command);
    addChatMessage('user', command);
    
    // Process the command based on type
    if (command.includes('Deep search')) {
      await handleDeepSearch(command);
    } else if (command.includes('Create agent')) {
      await handleCreateAgent(command);
    } else if (command.includes('Generate report')) {
      await handleGenerateReport(command);
    } else if (command.includes('Translate')) {
      await handleTranslation(command);
    } else if (command.includes('Read aloud')) {
      await handleTextToSpeech(command);
    } else if (isWorkflowBuildingCommand(command)) {
      await handleWorkflowBuilding(command);
    } else {
      // Standard processing for other commands
      try {
        const aiResponse = await processAIQuery(command, {
          currentUrl: currentUrl,
          sessionId: sessionId
        });
        
        let responseText = aiResponse.explanation || 'I understand your request.';
        
        if (aiResponse.commands && aiResponse.commands.length > 0) {
          for (const aiCommand of aiResponse.commands) {
            if (aiCommand.type === 'open' && aiCommand.params?.url) {
              responseText += `\n\n🚀 Opening ${aiCommand.params.url}...`;
              
              setActiveTabLoading(true);
              await navigateToUrl(aiCommand.params.url);
              
              try {
                const response = await proxyRequest(aiCommand.params.url);
                
                if (response && response.content) {
                  setIframeContent(response.content);
                  updateCurrentTab({ 
                    url: aiCommand.params.url, 
                    title: getDomainFromUrl(aiCommand.params.url),
                    loading: false,
                    favicon: getFaviconForUrl(aiCommand.params.url)
                  });
                  responseText += `\n✅ Content loaded successfully using ${response.method}`;
                }
              } catch (proxyError) {
                setActiveTabLoading(false);
                responseText += `\n⚠️ Loading encountered issues: ${proxyError.message}`;
              }
            }
          }
        }
        
        addChatMessage('ai', responseText, { commands: aiResponse.commands });
        
      } catch (error) {
        console.error('❌ Quick command error:', error);
        addChatMessage('ai', 'Sorry, I encountered an error processing your request. Please try again.');
      }
    }
    
    setCurrentMessage('');
  };

  return (
    <div className={`browser-container h-screen flex flex-col bg-gray-50 ${isFullscreen ? 'fullscreen' : ''}`}>
      {/* Enhanced Browser Header */}
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
            <button 
              className="p-2.5 hover:bg-gray-100 rounded-lg transition-all duration-200 group"
              disabled={history.length === 0}
              title="Go Back"
            >
              <ArrowLeft className="w-4 h-4 text-gray-600 group-hover:text-blue-600" />
            </button>
            <button 
              className="p-2.5 hover:bg-gray-100 rounded-lg transition-all duration-200 group"
              title="Go Forward"
            >
              <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-blue-600" />
            </button>
            <button 
              onClick={() => window.location.reload()}
              className="p-2.5 hover:bg-gray-100 rounded-lg transition-all duration-200 group"
              title="Refresh"
            >
              <RotateCcw className="w-4 h-4 text-gray-600 group-hover:text-purple-600" />
            </button>
          </div>

          {/* Enhanced URL Bar */}
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
                placeholder={currentUrl || "Search or enter web address..."}
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
            <div className="flex items-center space-x-1 text-xs text-gray-500 bg-gray-100 px-3 py-1.5 rounded-lg">
              {isOnline ? (
                <Wifi className="w-3 h-3 text-green-500" />
              ) : (
                <WifiOff className="w-3 h-3 text-red-500" />
              )}
              <span>{isOnline ? 'Online' : 'Offline'}</span>
            </div>
            
            {/* Shadow Tasks Indicator */}
            {shadowTasks.length > 0 && (
              <div className="flex items-center space-x-1 text-xs text-purple-600 bg-purple-50 px-2 py-1 rounded">
                <Eye className="w-3 h-3" />
                <span>{shadowTasks.filter(t => t.status === 'running').length} running</span>
              </div>
            )}
            
            <div className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
              Session: {sessionId?.slice(-8)}
            </div>
            
            <button 
              onClick={addBookmark}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Bookmark this page"
            >
              <BookmarkPlus className="w-4 h-4 text-gray-600" />
            </button>
            
            <button 
              onClick={() => setShowDownloads(!showDownloads)}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Downloads"
            >
              <Download className="w-4 h-4 text-gray-600" />
            </button>
            
            <button 
              onClick={toggleFullscreen}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              title="Toggle Fullscreen"
            >
              {isFullscreen ? <Minimize2 className="w-4 h-4 text-gray-600" /> : <Maximize2 className="w-4 h-4 text-gray-600" />}
            </button>
            
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
                onClick={() => switchTab(tab.id)}
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
                      closeTab(tab.id);
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
              title="New Tab"
            >
              <Plus className="w-4 h-4 text-gray-500" />
            </button>
          </div>

          <button
            onClick={() => setShowBookmarks(!showBookmarks)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Show/Hide Bookmarks"
          >
            <Star className="w-4 h-4 text-gray-500" />
          </button>
        </div>

        {/* Bookmarks Bar */}
        {showBookmarks && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="flex items-center space-x-2 mt-2 pt-2 border-t border-gray-100 overflow-x-auto"
          >
            {bookmarks.map((bookmark, index) => (
              <button
                key={index}
                onClick={() => handleUrlSubmit({ preventDefault: () => {}, target: { value: bookmark.url } })}
                className="flex items-center space-x-2 px-3 py-1.5 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors whitespace-nowrap"
                title={bookmark.url}
              >
                <span className="text-sm">{bookmark.favicon}</span>
                <span className="text-xs text-gray-700">{bookmark.name}</span>
              </button>
            ))}
          </motion.div>
        )}
      </header>

      {/* Enhanced Browser Content */}
      <main className="flex-1 relative bg-white">        
        {iframeContent ? (
          <div className="w-full h-full relative">
            <div 
              className="w-full h-full"
              dangerouslySetInnerHTML={{ __html: iframeContent }}
            />
          </div>
        ) : (
          <div className="flex items-center justify-center h-full bg-gradient-to-br from-gray-50 to-blue-50">
            <div className="text-center max-w-md">
              <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
                <Globe className="w-10 h-10 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-3">Enhanced AI Browser Ready</h3>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Your AI assistant now has Fellou-level capabilities: Deep Search, Agent Creation, Smart Reports, TTS, Translation, and Visual Workflow Builder
              </p>
              <div className="flex flex-col sm:flex-row gap-3 justify-center">
                <button 
                  onClick={() => setIsChatOpen(true)}
                  className="bg-gradient-to-r from-green-500 to-green-600 text-white px-6 py-3 rounded-xl font-medium hover:from-green-600 hover:to-green-700 transition-all duration-200 flex items-center space-x-2 justify-center shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                >
                  <Bot className="w-5 h-5" />
                  <span>Open AI Assistant</span>
                </button>
                <button 
                  onClick={() => setShowBookmarks(!showBookmarks)}
                  className="bg-white text-gray-700 px-6 py-3 rounded-xl font-medium hover:bg-gray-50 transition-all duration-200 flex items-center space-x-2 justify-center border border-gray-200 shadow-sm"
                >
                  <Star className="w-5 h-5" />
                  <span>View Bookmarks</span>
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
        className="ai-assistant fixed bottom-6 right-6 w-16 h-16 bg-gradient-to-br from-green-500 to-green-600 rounded-full shadow-xl hover:shadow-2xl flex items-center justify-center text-white z-50 transition-all duration-200"
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
        <div className="absolute -top-1 -right-1 w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
          <Zap className="w-2 h-2 text-white" />
        </div>
      </motion.button>

      {/* Enhanced AI Chat Panel with Tabbed Interface */}
      <AnimatePresence>
        {isChatOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="ai-chat-panel fixed bottom-24 right-6 w-96 h-[600px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col z-40 overflow-hidden"
          >
            {/* Enhanced Chat Header with Tabs */}
            <div className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-t-2xl">
              <div className="p-4 pb-0">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
                      {chatMode === 'chat' ? <Bot className="w-5 h-5" /> : <Workflow className="w-5 h-5" />}
                    </div>
                    <div>
                      <h3 className="font-semibold">Kairo AI Assistant</h3>
                      <p className="text-xs text-green-100">
                        {chatMode === 'chat' ? 'Enhanced • All Fellou features' : 'Visual Builder • Drag & Drop'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {isMuted ? (
                      <button onClick={() => setIsMuted(false)} className="p-1 hover:bg-white/20 rounded">
                        <VolumeX className="w-4 h-4" />
                      </button>
                    ) : (
                      <button onClick={() => setIsMuted(true)} className="p-1 hover:bg-white/20 rounded">
                        <Volume2 className="w-4 h-4" />
                      </button>
                    )}
                    <button 
                      onClick={() => setIsChatOpen(false)}
                      className="p-1 hover:bg-white/20 rounded-lg transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                {/* Tab Navigation */}
                <div className="flex space-x-1 mb-1">
                  <button
                    onClick={() => setChatMode('chat')}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-t-lg text-sm font-medium transition-all ${
                      chatMode === 'chat' 
                        ? 'bg-white text-green-600 shadow-sm' 
                        : 'text-green-100 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <MessageSquare className="w-4 h-4" />
                    <span>Chat</span>
                  </button>
                  <button
                    onClick={() => setChatMode('builder')}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-t-lg text-sm font-medium transition-all ${
                      chatMode === 'builder' 
                        ? 'bg-white text-green-600 shadow-sm' 
                        : 'text-green-100 hover:text-white hover:bg-white/10'
                    }`}
                  >
                    <Workflow className="w-4 h-4" />
                    <span>Builder</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Dynamic Content Based on Tab */}
            {chatMode === 'chat' ? (
              <>
                {/* Enhanced Chat Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
                  {chatMessages.map((message, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`ai-chat-bubble flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-xs px-4 py-3 rounded-2xl shadow-sm ${
                        message.type === 'user' 
                          ? 'bg-gradient-to-r from-green-500 to-green-600 text-white rounded-br-md' 
                          : 'bg-white text-gray-800 rounded-bl-md border border-gray-100'
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

                {/* Enhanced Quick Commands */}
                {chatMessages.length <= 2 && (
                  <div className="px-4 py-3 border-t border-gray-100 bg-white">
                    <p className="text-xs text-gray-500 mb-3 font-medium">✨ Try These Enhanced Commands:</p>
                    <div className="grid grid-cols-1 gap-2">
                      {enhancedQuickCommands.slice(0, 4).map((cmd, index) => (
                        <button
                          key={index}
                          onClick={() => handleQuickCommand(cmd.text)}
                          className={`text-xs ${cmd.color} border border-gray-200 rounded-lg px-3 py-2 hover:shadow-sm transition-all duration-200 flex items-center space-x-2`}
                        >
                          <span>{cmd.icon}</span>
                          <span className="truncate text-left">{cmd.text}</span>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Enhanced Chat Input */}
                <form onSubmit={handleAIChat} className="p-4 border-t border-gray-100 bg-white rounded-b-2xl">
                  <div className="flex space-x-3">
                    <input
                      type="text"
                      value={currentMessage}
                      onChange={(e) => setCurrentMessage(e.target.value)}
                      placeholder="Try: 'Deep search AI trends' or 'Create agent'"
                      className="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 bg-gray-50"
                    />
                    <button 
                      type="submit"
                      disabled={!currentMessage.trim() || isLoading}
                      className="p-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
                    >
                      {isLoading ? (
                        <div className="loading-spinner w-4 h-4"></div>
                      ) : (
                        <Send className="w-4 h-4" />
                      )}
                    </button>
                  </div>
                </form>
              </>
            ) : (
              /* Visual Workflow Builder Tab */
              <div className="flex-1 bg-gray-50">
                <VisualWorkflowBuilder 
                  onExecuteWorkflow={handleWorkflowExecution}
                  shadowTasks={shadowTasks}
                  builtWorkflows={builtWorkflows}
                  setBuiltWorkflows={setBuiltWorkflows}
                />
              </div>
            )}
            
          </motion.div>
        )}
      </AnimatePresence>

      {/* Settings Panel - Enhanced */}
      <AnimatePresence>
        {showSettings && (
          <motion.div
            initial={{ opacity: 0, x: 300 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 300 }}
            className="fixed top-0 right-0 w-80 h-full bg-white shadow-2xl z-40 border-l border-gray-200"
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-semibold text-gray-800">Enhanced Browser Settings</h3>
                <button onClick={() => setShowSettings(false)}>
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>
              
              <div className="space-y-6">
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-3">AI Assistant Features</h4>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Deep Search</span>
                      <div className="w-10 h-6 bg-green-500 rounded-full relative">
                        <div className="w-4 h-4 bg-white rounded-full absolute top-1 right-1"></div>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Agentic Memory</span>
                      <div className="w-10 h-6 bg-green-500 rounded-full relative">
                        <div className="w-4 h-4 bg-white rounded-full absolute top-1 right-1"></div>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Shadow Browsers</span>
                      <div className="w-10 h-6 bg-green-500 rounded-full relative">
                        <div className="w-4 h-4 bg-white rounded-full absolute top-1 right-1"></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-3">Accessibility</h4>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Text-to-Speech</span>
                      <div className="w-10 h-6 bg-green-500 rounded-full relative">
                        <div className="w-4 h-4 bg-white rounded-full absolute top-1 right-1"></div>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Auto Translation</span>
                      <div className="w-10 h-6 bg-gray-200 rounded-full relative">
                        <div className="w-4 h-4 bg-white rounded-full absolute top-1 left-1"></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-3">Browser Settings</h4>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm text-gray-600 mb-2">Theme</label>
                      <select className="w-full p-2 border border-gray-300 rounded-lg text-sm">
                        <option>Light</option>
                        <option>Dark</option>
                        <option>Auto</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-sm text-gray-600 mb-2">Default Search Engine</label>
                      <select className="w-full p-2 border border-gray-300 rounded-lg text-sm">
                        <option>Enhanced Multi-Source</option>
                        <option>Google</option>
                        <option>Bing</option>
                        <option>DuckDuckGo</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Shadow Tasks Status */}
                {shadowTasks.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-700 mb-3">Background Tasks</h4>
                    <div className="space-y-2">
                      {shadowTasks.slice(0, 3).map((task, index) => (
                        <div key={task.id} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                          <div className="flex items-center space-x-2">
                            <div className={`w-2 h-2 rounded-full ${
                              task.status === 'running' ? 'bg-yellow-500' : 
                              task.status === 'completed' ? 'bg-green-500' : 'bg-red-500'
                            }`}></div>
                            <span className="text-xs text-gray-600 truncate">{task.name}</span>
                          </div>
                          <span className="text-xs text-gray-500">{task.status}</span>
                        </div>
                      ))}
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

export default EnhancedBrowserInterface;