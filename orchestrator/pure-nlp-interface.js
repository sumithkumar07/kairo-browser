/**
 * Pure NLP Interface - Clean AI-Only Experience
 * No complex UI - just natural language interaction
 */

const EnhancedAIIntegration = require('./ai-integration-enhanced');
const AutonomousBrowser = require('./autonomous-browser');
const WorkflowEngine = require('./workflow-engine');

class PureNLPInterface {
  constructor() {
    this.ai = new EnhancedAIIntegration();
    this.browser = new AutonomousBrowser();
    this.workflow = new WorkflowEngine();
    
    // Simple conversation state
    this.conversationActive = false;
    this.currentContext = {};
    
    console.log('🤖 Pure NLP Interface initialized - AI handles everything!');
  }

  /**
   * Initialize the system
   */
  async initialize() {
    try {
      console.log('🚀 Starting AI-only system...');
      
      // Initialize browser engines
      await this.browser.initialize();
      
      this.conversationActive = true;
      
      console.log('✅ AI Assistant ready - just talk naturally!');
      
      return {
        success: true,
        message: "Hello! I'm your AI assistant. Tell me anything you want to do, and I'll handle it completely. No buttons, no complexity - just natural conversation!",
        capabilities: [
          "Browse any website automatically",
          "Search across multiple platforms simultaneously", 
          "Extract and analyze data intelligently",
          "Create reports with AI insights",
          "Handle complex multi-step tasks",
          "Learn your preferences over time",
          "Suggest proactive actions"
        ]
      };
      
    } catch (error) {
      console.error('❌ Initialization failed:', error);
      throw error;
    }
  }

  /**
   * MAIN INTERFACE - Handle any natural language input
   */
  async handleUserInput(userMessage, context = {}) {
    try {
      console.log(`👤 User: "${userMessage}"`);
      
      // Update context
      this.currentContext = { ...this.currentContext, ...context };
      
      // Let AI handle EVERYTHING
      const response = await this.ai.processNaturalLanguage(userMessage, this.currentContext);
      
      // Execute any browser operations invisibly
      if (response.data && response.data.parallelTasks) {
        console.log('🌐 Executing browser operations invisibly...');
        
        const browserOps = this.convertToOperations(response.data.parallelTasks);
        const browserResults = await this.browser.executeParallelOperations(browserOps);
        
        // Merge browser results back into response
        response.browserResults = Array.from(browserResults.entries());
      }
      
      // Update conversation context
      this.currentContext.lastResponse = response;
      this.currentContext.timestamp = new Date().toISOString();
      
      console.log(`🤖 AI: ${response.message}`);
      
      return {
        success: true,
        message: response.message,
        data: response.data,
        proactiveActions: response.proactiveActions,
        tasksSummary: response.tasksSummary,
        browserResults: response.browserResults,
        conversationActive: this.conversationActive
      };
      
    } catch (error) {
      console.error('❌ Error processing user input:', error);
      
      return {
        success: false,
        message: "I encountered an issue, but let me try a different approach. Can you tell me again what you'd like me to do?",
        error: error.message,
        conversationActive: this.conversationActive
      };
    }
  }

  /**
   * Convert AI tasks to browser operations
   */
  convertToOperations(aiTasks) {
    return aiTasks.map(task => ({
      id: task.id,
      type: this.mapTaskType(task.type),
      description: task.description,
      params: this.extractParams(task)
    }));
  }

  mapTaskType(aiType) {
    const mapping = {
      'browse': 'navigate',
      'search': 'search', 
      'extract': 'extract',
      'analyze': 'analyze',
      'create': 'interact',
      'report': 'extract'
    };
    
    return mapping[aiType] || 'navigate';
  }

  extractParams(task) {
    // Extract parameters from AI task for browser operations
    const params = {};
    
    if (task.description.includes('search')) {
      params.platform = this.detectPlatform(task.description);
      params.query = this.extractSearchQuery(task.description);
    }
    
    if (task.description.includes('navigate') || task.description.includes('go to')) {
      params.url = this.extractUrl(task.description);
    }
    
    if (task.description.includes('extract') || task.description.includes('get data')) {
      params.dataType = this.detectDataType(task.description);
    }
    
    return params;
  }

  detectPlatform(description) {
    const platforms = ['google', 'youtube', 'amazon', 'github', 'linkedin'];
    return platforms.find(p => description.toLowerCase().includes(p)) || 'google';
  }

  extractSearchQuery(description) {
    // Simple extraction - can be enhanced with better NLP
    const matches = description.match(/search for ["']([^"']+)["']/) || 
                   description.match(/search for (.+)/);
    return matches ? matches[1] : 'search query';
  }

  extractUrl(description) {
    const urlPattern = /https?:\/\/[^\s]+/;
    const match = description.match(urlPattern);
    return match ? match[0] : null;
  }

  detectDataType(description) {
    if (description.includes('price')) return 'prices';
    if (description.includes('contact')) return 'contact';
    if (description.includes('product')) return 'products';
    if (description.includes('article')) return 'articles';
    return 'general';
  }

  /**
   * Quick actions for common requests
   */
  async quickSearch(query, platforms = ['google']) {
    return await this.handleUserInput(`Search for "${query}" on ${platforms.join(' and ')}`);
  }

  async quickAnalyze(url) {
    return await this.handleUserInput(`Analyze the website ${url} and give me insights`);
  }

  async quickCompare(items) {
    return await this.handleUserInput(`Compare ${items.join(' vs ')} and create a detailed comparison`);
  }

  /**
   * Get conversation state
   */
  getConversationState() {
    return {
      active: this.conversationActive,
      context: this.currentContext,
      capabilities: [
        "Natural language processing",
        "Autonomous browser control", 
        "Parallel task execution",
        "Intelligent data analysis",
        "Proactive suggestions",
        "Learning from interactions"
      ]
    };
  }

  /**
   * Reset conversation
   */
  resetConversation() {
    this.currentContext = {};
    this.conversationActive = true;
    
    return {
      success: true,
      message: "Conversation reset. What would you like me to help you with?"
    };
  }

  /**
   * Cleanup
   */
  async shutdown() {
    console.log('🛑 Shutting down Pure NLP Interface...');
    
    this.conversationActive = false;
    
    if (this.browser) {
      await this.browser.cleanup();
    }
    
    console.log('✅ Shutdown complete');
  }
}

module.exports = PureNLPInterface;