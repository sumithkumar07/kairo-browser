import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const SessionContext = createContext();

export const useSession = () => {
  const context = useContext(SessionContext);
  if (!context) {
    throw new Error('useSession must be used within a SessionProvider');
  }
  return context;
};

export const SessionProvider = ({ children }) => {
  const [sessionId, setSessionId] = useState(null);
  const [currentUrl, setCurrentUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [aiContext, setAiContext] = useState({});

  // Initialize session
  useEffect(() => {
    const generateSessionId = () => {
      return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    };
    
    setSessionId(generateSessionId());
  }, []);

  // API base URL
  const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  // Browser navigation functions
  const navigateToUrl = async (url) => {
    setIsLoading(true);
    try {
      // Ensure URL has protocol
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
      }
      
      const response = await axios.post(`${API_BASE}/api/browser/execute`, {
        command: 'open',
        url: url,
        session_id: sessionId
      });
      
      setCurrentUrl(url);
      setHistory(prev => [...prev, { url, timestamp: new Date(), title: url }]);
      
      return response.data;
    } catch (error) {
      console.error('Navigation error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Execute browser command
  const executeBrowserCommand = async (command, params = {}) => {
    try {
      const response = await axios.post(`${API_BASE}/api/browser/execute`, {
        command: command,
        session_id: sessionId,
        ...params
      });
      
      return response.data;
    } catch (error) {
      console.error('Command execution error:', error);
      throw error;
    }
  };

  // AI query processing
  const processAIQuery = async (query, context = {}) => {
    try {
      setIsLoading(true);
      
      const response = await axios.post(`${API_BASE}/api/ai/query`, {
        query: query,
        session_id: sessionId,
        context: {
          currentUrl,
          ...aiContext,
          ...context
        }
      });
      
      // Update AI context with new information
      setAiContext(prev => ({
        ...prev,
        lastQuery: query,
        lastResponse: response.data,
        timestamp: new Date().toISOString()
      }));
      
      return response.data;
    } catch (error) {
      console.error('AI query error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Execute workflow
  const executeWorkflow = async (workflow) => {
    try {
      const response = await axios.post(`${API_BASE}/api/workflow/execute`, workflow);
      return response.data;
    } catch (error) {
      console.error('Workflow execution error:', error);
      throw error;
    }
  };

  // Get workflow status
  const getWorkflowStatus = async (workflowId) => {
    try {
      const response = await axios.get(`${API_BASE}/api/workflow/${workflowId}`);
      return response.data;
    } catch (error) {
      console.error('Workflow status error:', error);
      throw error;
    }
  };

  // Proxy request for loading external content
  const proxyRequest = async (url) => {
    try {
      const response = await axios.post(`${API_BASE}/api/proxy`, { url });
      return response.data;
    } catch (error) {
      console.error('Proxy request error:', error);
      throw error;
    }
  };

  const value = {
    sessionId,
    currentUrl,
    isLoading,
    history,
    aiContext,
    navigateToUrl,
    executeBrowserCommand,
    processAIQuery,
    executeWorkflow,
    getWorkflowStatus,
    proxyRequest,
    setCurrentUrl,
    setAiContext
  };

  return (
    <SessionContext.Provider value={value}>
      {children}
    </SessionContext.Provider>
  );
};