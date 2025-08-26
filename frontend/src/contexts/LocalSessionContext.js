import React, { createContext, useContext, useState, useEffect } from 'react';

const LocalSessionContext = createContext();

export const useLocalSession = () => {
  const context = useContext(LocalSessionContext);
  if (!context) {
    throw new Error('useLocalSession must be used within a LocalSessionProvider');
  }
  return context;
};

export const LocalSessionProvider = ({ children }) => {
  const [sessionId, setSessionId] = useState(null);
  const [currentUrl, setCurrentUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [isLocalFirst, setIsLocalFirst] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);

  useEffect(() => {
    const initializeLocalSession = async () => {
      // Check if running in Electron
      if (window.electronAPI) {
        setIsLocalFirst(true);
        
        try {
          // Get app info
          const appInfo = await window.electronAPI.getAppInfo();
          console.log('✅ Local-First mode detected:', appInfo);
          
          // Initialize new session
          const sessionResult = await window.electronAPI.createSession();
          if (sessionResult.success) {
            setSessionId(sessionResult.sessionId);
            console.log('✅ Local session created:', sessionResult.sessionId);
          }
          
          // Get system status
          const status = await window.electronAPI.getSystemStatus();
          setSystemStatus(status);
          
        } catch (error) {
          console.error('❌ Failed to initialize local session:', error);
        }
      } else {
        // Running in browser (server-first mode)
        setIsLocalFirst(false);
        const browserSessionId = 'browser_session_' + Math.random().toString(36).substr(2, 9);
        setSessionId(browserSessionId);
        console.log('🌐 Browser session created:', browserSessionId);
      }
    };

    initializeLocalSession();
  }, []);

  // Local navigation (direct browser access)
  const navigateToUrl = async (url) => {
    setIsLoading(true);
    try {
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        if (url.includes('.') && !url.includes(' ')) {
          url = 'https://' + url;
        } else {
          url = `https://www.google.com/search?q=${encodeURIComponent(url)}`;
        }
      }
      
      let result;
      
      if (isLocalFirst && window.electronAPI) {
        // Local-first: Direct browser navigation
        result = await window.electronAPI.navigateToUrl(sessionId, url);
      } else {
        // Server-first: Fallback to existing proxy system
        const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
        const response = await fetch(`${backendUrl}/api/proxy/enhanced`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url })
        });
        
        const proxyResult = await response.json();
        result = {
          success: response.ok,
          url: proxyResult.url || url,
          title: proxyResult.title || new URL(url).hostname,
          content: proxyResult.content
        };
      }
      
      if (result.success) {
        setCurrentUrl(result.url);
        setHistory(prev => [...prev, { 
          url: result.url, 
          title: result.title,
          timestamp: new Date(),
          sessionId
        }]);
        
        return result;
      } else {
        throw new Error(result.error || 'Navigation failed');
      }
      
    } catch (error) {
      console.error('❌ Navigation error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Local AI processing
  const processAIQuery = async (query, context = {}) => {
    try {
      setIsLoading(true);
      
      let result;
      
      if (isLocalFirst && window.electronAPI) {
        // Local-first: Direct AI processing
        result = await window.electronAPI.processAIQuery(query, {
          currentUrl,
          sessionId,
          ...context
        });
      } else {
        // Server-first: Fallback to existing API
        const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
        const response = await fetch(`${backendUrl}/api/ai/multimodal-query`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query,
            session_id: sessionId,
            context: { currentUrl, ...context }
          })
        });
        
        result = await response.json();
      }
      
      return result;
    } catch (error) {
      console.error('❌ AI query error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Local browser commands
  const executeBrowserCommand = async (command) => {
    try {
      let result;
      
      if (isLocalFirst && window.electronAPI) {
        // Local-first: Direct browser automation
        result = await window.electronAPI.executeBrowserCommand({
          sessionId,
          ...command
        });
      } else {
        // Server-first: Fallback to existing API
        const backendUrl = process.env.REACT_APP_BACKEND_URL || window.location.origin;
        const response = await fetch(`${backendUrl}/api/browser/execute`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            command: command.type,
            session_id: sessionId,
            ...command
          })
        });
        
        result = await response.json();
      }
      
      return result;
    } catch (error) {
      console.error('❌ Browser command error:', error);
      throw error;
    }
  };

  // Create new tab/session
  const createNewTab = async () => {
    try {
      if (isLocalFirst && window.electronAPI) {
        const result = await window.electronAPI.createSession();
        if (result.success) {
          return result.sessionId;
        }
      }
      
      // Fallback: generate new session ID
      const newSessionId = 'session_' + Math.random().toString(36).substr(2, 9);
      return newSessionId;
    } catch (error) {
      console.error('❌ Failed to create new tab:', error);
      throw error;
    }
  };

  // Close tab/session
  const closeTab = async (targetSessionId) => {
    try {
      if (isLocalFirst && window.electronAPI) {
        await window.electronAPI.closeSession(targetSessionId);
      }
      
      // Update local state if it's current session
      if (targetSessionId === sessionId) {
        const newSessionId = await createNewTab();
        setSessionId(newSessionId);
        setCurrentUrl('');
      }
    } catch (error) {
      console.error('❌ Failed to close tab:', error);
    }
  };

  // Get browsing history
  const getBrowsingHistory = async (limit = 50) => {
    try {
      if (isLocalFirst && window.electronAPI) {
        const result = await window.electronAPI.getHistory(limit);
        return result.success ? result.history : [];
      }
      
      // Fallback to local state
      return history.slice(0, limit);
    } catch (error) {
      console.error('❌ Failed to get history:', error);
      return [];
    }
  };

  // Settings management
  const updateSettings = async (key, value) => {
    try {
      if (isLocalFirst && window.electronAPI) {
        await window.electronAPI.setSetting(key, value);
      }
      
      // Update local storage as fallback
      localStorage.setItem(`kairo_${key}`, JSON.stringify(value));
    } catch (error) {
      console.error('❌ Failed to update settings:', error);
    }
  };

  const getSetting = async (key, defaultValue = null) => {
    try {
      if (isLocalFirst && window.electronAPI) {
        return await window.electronAPI.getSetting(key, defaultValue);
      }
      
      // Fallback to localStorage
      const stored = localStorage.getItem(`kairo_${key}`);
      return stored ? JSON.parse(stored) : defaultValue;
    } catch (error) {
      console.error('❌ Failed to get setting:', error);
      return defaultValue;
    }
  };

  // System status
  const getSystemStatus = async () => {
    try {
      if (isLocalFirst && window.electronAPI) {
        return await window.electronAPI.getSystemStatus();
      }
      
      return {
        isLocalFirst: false,
        browserEngine: false,
        aiProcessor: true, // Assume server AI works
        orchestrator: false
      };
    } catch (error) {
      console.error('❌ Failed to get system status:', error);
      return null;
    }
  };

  const value = {
    // State
    sessionId,
    currentUrl,
    isLoading,
    history,
    isLocalFirst,
    systemStatus,
    
    // Navigation
    navigateToUrl,
    setCurrentUrl,
    
    // AI Processing
    processAIQuery,
    
    // Browser Commands
    executeBrowserCommand,
    
    // Tab Management
    createNewTab,
    closeTab,
    
    // History
    getBrowsingHistory,
    
    // Settings
    updateSettings,
    getSetting,
    
    // System
    getSystemStatus
  };

  return (
    <LocalSessionContext.Provider value={value}>
      {children}
    </LocalSessionContext.Provider>
  );
};