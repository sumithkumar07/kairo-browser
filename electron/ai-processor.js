const fetch = require('node-fetch');

class LocalAIProcessor {
  constructor() {
    // Use environment variable or user-provided API key
    this.groqApiKey = process.env.GROQ_API_KEY || null;
    this.apiEndpoint = 'https://api.groq.com/openai/v1/chat/completions';
    this.conversationHistory = new Map(); // Store conversation history per session
  }

  setApiKey(apiKey) {
    this.groqApiKey = apiKey;
    console.log('✅ AI API key configured');
  }

  async processQuery(query, context = {}) {
    if (!this.groqApiKey) {
      return {
        success: false,
        error: 'AI API key not configured. Please add your Groq API key in settings.',
        suggestion: 'You can get a free API key from https://console.groq.com/'
      };
    }

    try {
      console.log('🤖 Processing AI query:', query.substring(0, 100) + '...');
      
      const systemPrompt = `You are Kairo AI, running locally on the user's machine with DIRECT internet access. You help users navigate and interact with websites through natural language commands.

IMPORTANT: You have FULL access to real websites without any restrictions. No proxies needed - direct browser automation.

Available browser actions:
- navigate: Go directly to any URL (YouTube, Google, etc.)
- click: Click on elements with CSS selectors
- type: Type text into input fields  
- scroll: Scroll the page up/down
- screenshot: Take screenshots
- search: Search on current page
- extract_text: Extract text from elements
- extract_links: Get all links from page
- wait_for_element: Wait for elements to appear
- press_key: Press keyboard keys (Enter, Tab, etc.)

LOCAL-FIRST BENEFITS:
✅ Direct YouTube video access (no restrictions)
✅ Real login sessions and cookies
✅ Full JavaScript support
✅ Faster performance (no server bottleneck)
✅ Complete website functionality
✅ File downloads directly to user's machine

Current context:
- Current URL: ${context.currentUrl || 'None'}
- Session ID: ${context.sessionId || 'Unknown'}
- Platform: Local Desktop App

Respond with JSON:
{
  "intent": "what user wants to accomplish",
  "commands": [
    {
      "type": "action_type",
      "params": {
        "url": "url if navigating",
        "selector": "css selector if needed",
        "text": "text to type if needed",
        "key": "key to press if needed",
        "pixels": "scroll amount if needed"
      }
    }
  ],
  "explanation": "detailed explanation of what you'll do",
  "next_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
}

Examples:
- "Open YouTube" → Navigate directly to youtube.com
- "Play video yeh raatein" → Navigate to YouTube search, then click first result
- "Login to Gmail" → Navigate to gmail.com, handle login process
- "Download this file" → Click download links (files save locally)`;

      // Get conversation history for this session
      const sessionId = context.sessionId || 'default';
      const history = this.conversationHistory.get(sessionId) || [];
      
      // Build messages array with history
      const messages = [
        { role: 'system', content: systemPrompt },
        ...history.slice(-6), // Keep last 6 messages for context
        { role: 'user', content: query }
      ];

      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.groqApiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'llama3-8b-8192',
          messages: messages,
          temperature: 0.3,
          max_tokens: 1200
        })
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error?.message || 'AI API request failed');
      }

      const aiResponse = result.choices[0].message.content;
      
      // Parse JSON response
      let parsedResponse;
      try {
        const jsonStart = aiResponse.indexOf('{');
        const jsonEnd = aiResponse.lastIndexOf('}') + 1;
        if (jsonStart !== -1 && jsonEnd > jsonStart) {
          const jsonContent = aiResponse.slice(jsonStart, jsonEnd);
          parsedResponse = JSON.parse(jsonContent);
        } else {
          throw new Error('No JSON found in response');
        }
      } catch (parseError) {
        console.warn('Failed to parse AI response as JSON, creating fallback response');
        parsedResponse = {
          intent: query,
          commands: [],
          explanation: aiResponse,
          next_suggestions: ['Try rephrasing your request', 'Be more specific', 'Ask for help']
        };
      }

      // Update conversation history
      history.push(
        { role: 'user', content: query },
        { role: 'assistant', content: JSON.stringify(parsedResponse) }
      );
      this.conversationHistory.set(sessionId, history);

      console.log('✅ AI query processed successfully');
      
      return {
        success: true,
        response: parsedResponse,
        sessionId: sessionId
      };

    } catch (error) {
      console.error('❌ AI processing error:', error);
      return {
        success: false,
        error: error.message,
        suggestion: error.message.includes('API key') ? 
          'Please check your Groq API key in settings' : 
          'Please try again or rephrase your request'
      };
    }
  }

  async processMultiModalQuery(query, context = {}, mediaFiles = []) {
    // Enhanced multimodal processing for images, voice, etc.
    // For now, fallback to text processing
    console.log('🎨 Multimodal query processing (fallback to text)');
    
    let enhancedQuery = query;
    
    // If media files are provided, add context
    if (mediaFiles && mediaFiles.length > 0) {
      enhancedQuery += '\n\nNote: User provided media files for analysis.';
    }
    
    return await this.processQuery(enhancedQuery, context);
  }

  clearHistory(sessionId) {
    if (sessionId) {
      this.conversationHistory.delete(sessionId);
      console.log('🗑️ Cleared conversation history for session:', sessionId);
    } else {
      this.conversationHistory.clear();
      console.log('🗑️ Cleared all conversation history');
    }
  }

  getHistoryStats() {
    return {
      activeSessions: this.conversationHistory.size,
      totalMessages: Array.from(this.conversationHistory.values())
        .reduce((sum, history) => sum + history.length, 0)
    };
  }

  // Health check
  isConfigured() {
    return !!this.groqApiKey;
  }

  // Test connection
  async testConnection() {
    if (!this.groqApiKey) {
      return { success: false, error: 'No API key configured' };
    }

    try {
      const response = await this.processQuery('Hello, can you hear me?', { sessionId: 'test' });
      return { 
        success: response.success, 
        message: response.success ? 'AI connection working' : response.error 
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

module.exports = LocalAIProcessor;