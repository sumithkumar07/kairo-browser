const LocalBrowserEngine = require('./browser-engine');
const LocalAIProcessor = require('./ai-processor');
const LocalStorage = require('./local-storage');

class LocalOrchestrator {
  constructor() {
    this.browserEngine = new LocalBrowserEngine();
    this.aiProcessor = new LocalAIProcessor();
    this.localStorage = new LocalStorage();
    this.isInitialized = false;
    this.activeSessions = new Map();
  }

  async initialize() {
    try {
      console.log('🔧 Initializing Local Orchestrator...');
      
      // Initialize browser engine
      const browserInitialized = await this.browserEngine.initialize();
      if (!browserInitialized) {
        console.warn('⚠️ Browser engine initialization failed');
      }
      
      // Set AI API key if available
      const apiKey = this.localStorage.getSetting('groq_api_key');
      if (apiKey) {
        this.aiProcessor.setApiKey(apiKey);
      }
      
      this.isInitialized = true;
      console.log('✅ Local Orchestrator initialized successfully');
      
      return {
        success: true,
        browserEngine: browserInitialized,
        aiProcessor: this.aiProcessor.isConfigured(),
        localStorage: true
      };
    } catch (error) {
      console.error('❌ Failed to initialize Local Orchestrator:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  async createSession() {
    const sessionId = 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    
    try {
      // Create browser tab
      await this.browserEngine.createTab(sessionId);
      
      // Initialize session data
      const sessionData = {
        id: sessionId,
        created: new Date(),
        lastActivity: new Date(),
        currentUrl: '',
        title: 'New Tab'
      };
      
      this.activeSessions.set(sessionId, sessionData);
      
      console.log('✅ New session created:', sessionId);
      return { success: true, sessionId, sessionData };
    } catch (error) {
      console.error('❌ Failed to create session:', error);
      return { success: false, error: error.message };
    }
  }

  async navigateToUrl(sessionId, url) {
    try {
      // Normalize URL
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        if (url.includes('.') && !url.includes(' ')) {
          url = 'https://' + url;
        } else {
          // Treat as search query
          url = `https://www.google.com/search?q=${encodeURIComponent(url)}`;
        }
      }

      console.log('🌐 Orchestrator navigating to:', url);
      
      // Navigate using browser engine
      const result = await this.browserEngine.navigateToUrl(sessionId, url);
      
      if (result.success) {
        // Update session data
        const sessionData = this.activeSessions.get(sessionId);
        if (sessionData) {
          sessionData.currentUrl = result.url;
          sessionData.title = result.title;
          sessionData.lastActivity = new Date();
          this.activeSessions.set(sessionId, sessionData);
        }
        
        // Save to history
        await this.saveToHistory({
          sessionId,
          url: result.url,
          title: result.title,
          timestamp: new Date()
        });
        
        // Add to recent sites
        this.localStorage.addRecentSite({
          url: result.url,
          title: result.title,
          timestamp: new Date()
        });
      }
      
      return result;
    } catch (error) {
      console.error('❌ Navigation orchestration failed:', error);
      return { success: false, error: error.message };
    }
  }

  async processAIQuery(query, context = {}) {
    try {
      console.log('🤖 Orchestrator processing AI query');
      
      // Add current session context
      const sessionData = this.activeSessions.get(context.sessionId);
      if (sessionData) {
        context.currentUrl = sessionData.currentUrl;
        context.currentTitle = sessionData.title;
      }
      
      // Process with AI
      const aiResult = await this.aiProcessor.processQuery(query, context);
      
      if (aiResult.success && aiResult.response.commands) {
        // Execute AI-generated commands
        const executionResults = [];
        
        for (const command of aiResult.response.commands) {
          console.log('⚡ Executing AI command:', command.type);
          
          let result;
          switch (command.type) {
            case 'navigate':
            case 'open':
              result = await this.navigateToUrl(context.sessionId, command.params.url);
              break;
              
            case 'click':
            case 'type':
            case 'scroll':
            case 'screenshot':
            case 'extract_text':
            case 'extract_links':
            case 'wait_for_element':
            case 'press_key':
              result = await this.browserEngine.executeCommand(context.sessionId, {
                type: command.type,
                ...command.params
              });
              break;
              
            default:
              result = { success: false, error: 'Unknown command type: ' + command.type };
          }
          
          executionResults.push({
            command: command.type,
            success: result.success,
            error: result.error,
            data: result.data
          });
          
          // Add delay between commands
          if (command.type !== 'screenshot') {
            await new Promise(resolve => setTimeout(resolve, 1000));
          }
        }
        
        return {
          success: true,
          aiResponse: aiResult.response,
          executionResults
        };
      }
      
      return aiResult;
    } catch (error) {
      console.error('❌ AI query orchestration failed:', error);
      return { success: false, error: error.message };
    }
  }

  async executeBrowserCommand(sessionId, command) {
    try {
      console.log('⚡ Orchestrator executing browser command:', command.type);
      
      const result = await this.browserEngine.executeCommand(sessionId, command);
      
      // Update session activity
      const sessionData = this.activeSessions.get(sessionId);
      if (sessionData) {
        sessionData.lastActivity = new Date();
        this.activeSessions.set(sessionId, sessionData);
      }
      
      return result;
    } catch (error) {
      console.error('❌ Browser command orchestration failed:', error);
      return { success: false, error: error.message };
    }
  }

  async saveToHistory(historyItem) {
    try {
      // Save to local storage
      const history = this.localStorage.getSetting('browsing_history', []);
      history.unshift(historyItem);
      
      // Keep only last 1000 items
      if (history.length > 1000) {
        history.splice(1000);
      }
      
      this.localStorage.setSetting('browsing_history', history);
      return { success: true };
    } catch (error) {
      console.error('❌ Failed to save history:', error);
      return { success: false, error: error.message };
    }
  }

  async getHistory(limit = 50) {
    try {
      const history = this.localStorage.getSetting('browsing_history', []);
      return { success: true, history: history.slice(0, limit) };
    } catch (error) {
      console.error('❌ Failed to get history:', error);
      return { success: false, error: error.message };
    }
  }

  async closeSession(sessionId) {
    try {
      await this.browserEngine.closePage(sessionId);
      this.activeSessions.delete(sessionId);
      this.aiProcessor.clearHistory(sessionId);
      
      console.log('✅ Session closed:', sessionId);
      return { success: true };
    } catch (error) {
      console.error('❌ Failed to close session:', error);
      return { success: false, error: error.message };
    }
  }

  async getAllSessions() {
    try {
      const sessions = Array.from(this.activeSessions.values());
      return { success: true, sessions };
    } catch (error) {
      console.error('❌ Failed to get sessions:', error);
      return { success: false, error: error.message };
    }
  }

  async getSystemStatus() {
    return {
      orchestrator: this.isInitialized,
      browserEngine: this.browserEngine.isHealthy(),
      aiProcessor: this.aiProcessor.isConfigured(),
      activeSessions: this.activeSessions.size,
      browserStats: this.browserEngine.getStats(),
      aiStats: this.aiProcessor.getHistoryStats()
    };
  }

  async shutdown() {
    console.log('🔄 Shutting down Local Orchestrator...');
    
    try {
      // Clear all sessions
      for (const sessionId of this.activeSessions.keys()) {
        await this.closeSession(sessionId);
      }
      
      // Shutdown browser engine
      await this.browserEngine.shutdown();
      
      // Clear AI history
      this.aiProcessor.clearHistory();
      
      this.isInitialized = false;
      console.log('✅ Local Orchestrator shutdown complete');
    } catch (error) {
      console.error('❌ Error during shutdown:', error);
    }
  }

  // Configuration methods
  async setApiKey(apiKey) {
    this.localStorage.setSetting('groq_api_key', apiKey);
    this.aiProcessor.setApiKey(apiKey);
    return { success: true, message: 'API key configured' };
  }

  async testAIConnection() {
    return await this.aiProcessor.testConnection();
  }
}

module.exports = LocalOrchestrator;