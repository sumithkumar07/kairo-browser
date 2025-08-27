/**
 * AI Integration - Local-First Implementation
 * Handles AI processing with local context and remote API calls
 */

const https = require('https');
require('dotenv').config();

class AIIntegration {
  constructor() {
    this.apiKey = process.env.GROQ_API_KEY;
    this.apiUrl = 'https://api.groq.com/openai/v1/chat/completions';
    this.model = 'llama-3.3-70b-versatile'; // Llama 4 Scout (17Bx16E) equivalent
    this.contextMemory = [];
    this.maxContextLength = 10;
  }

  /**
   * Process AI query with local context
   */
  async processQuery(query, context = {}) {
    try {
      console.log(`🤖 Processing AI query: ${query}`);

      if (!this.apiKey) {
        throw new Error('Groq API key not configured');
      }

      // Build enhanced context for local-first environment
      const enhancedContext = {
        ...context,
        environment: 'local-first',
        capabilities: [
          'native_browser_automation',
          'direct_website_access',
          'local_file_system',
          'offline_operation',
          'no_proxy_restrictions'
        ],
        browserEngine: 'chromium_embedded',
        timestamp: new Date().toISOString()
      };

      // Create system prompt for local-first capabilities
      const systemPrompt = this.buildSystemPrompt(enhancedContext);

      // Build conversation history
      const messages = [
        { role: 'system', content: systemPrompt },
        ...this.contextMemory.slice(-this.maxContextLength),
        { role: 'user', content: query }
      ];

      // Make API call to Groq
      const response = await this.makeAPICall(messages);
      
      // Process and parse response
      const parsedResponse = this.parseAIResponse(response);

      // Update context memory
      this.updateContextMemory(query, parsedResponse);

      return parsedResponse;

    } catch (error) {
      console.error(`❌ AI processing error:`, error);
      throw error;
    }
  }

  /**
   * Build system prompt for local-first environment
   */
  buildSystemPrompt(context) {
    return `You are Kairo AI, an intelligent browser assistant running in LOCAL-FIRST MODE with enhanced capabilities.

ENVIRONMENT CAPABILITIES:
- Native Chromium browser engine (no proxy limitations)
- Direct website access (YouTube, Netflix, banking sites all work perfectly)
- Local file system access
- Offline operation capability
- Real browser automation (not iframe-based)

CURRENT CONTEXT:
- Current URL: ${context.currentUrl || 'None'}
- Page Title: ${context.pageTitle || 'None'}
- Browser Engine: ${context.browserEngine || 'Chromium'}
- Environment: ${context.environment || 'local-first'}

AVAILABLE COMMANDS:
- navigate: Direct navigation to any website
- click: Click any element using CSS selectors
- type: Type text into any input field
- search: Search on current website
- youtube_video: Enhanced YouTube video access with native playback
- wait: Wait for specified duration
- wait_for: Wait for element to appear
- extract: Extract data from page elements
- screenshot: Take screenshots
- script: Execute custom JavaScript
- ai_process: Process content with AI

For YouTube video requests like "play video X":
1. Use youtube_video command with search_query parameter
2. The system can directly access YouTube without restrictions
3. Videos will play natively in the embedded browser

RESPONSE FORMAT:
{
  "intent": "description of user's request",
  "commands": [
    {
      "type": "command_type",
      "params": {
        "url": "for navigation",
        "selector": "CSS selector for clicks/typing",
        "text": "text to type",
        "search_query": "for YouTube videos",
        "enhanced_search": true/false
      }
    }
  ],
  "explanation": "Human-readable explanation"
}

Remember: This is a native desktop browser, not web-based, so ALL websites work perfectly including YouTube videos, Netflix, banking sites, etc.`;
  }

  /**
   * Make API call to Groq
   */
  async makeAPICall(messages) {
    return new Promise((resolve, reject) => {
      const postData = JSON.stringify({
        model: this.model,
        messages: messages,
        temperature: 0.3,
        max_tokens: 1000,
        top_p: 1,
        stream: false
      });

      const options = {
        hostname: 'api.groq.com',
        port: 443,
        path: '/openai/v1/chat/completions',
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(postData)
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
          data += chunk;
        });
        
        res.on('end', () => {
          try {
            const response = JSON.parse(data);
            if (response.error) {
              reject(new Error(response.error.message));
            } else {
              resolve(response.choices[0].message.content);
            }
          } catch (error) {
            reject(new Error(`Failed to parse API response: ${error.message}`));
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`API request failed: ${error.message}`));
      });

      req.write(postData);
      req.end();
    });
  }

  /**
   * Parse AI response into structured format
   */
  parseAIResponse(responseContent) {
    try {
      // Try to extract JSON from response
      const jsonMatch = responseContent.match(/\{[\s\S]*\}/);
      
      if (jsonMatch) {
        const parsedJSON = JSON.parse(jsonMatch[0]);
        return {
          intent: parsedJSON.intent || 'Unknown intent',
          commands: parsedJSON.commands || [],
          explanation: parsedJSON.explanation || responseContent,
          raw: responseContent
        };
      } else {
        // If no JSON found, create a simple structure
        return {
          intent: 'General query',
          commands: [],
          explanation: responseContent,
          raw: responseContent
        };
      }
    } catch (error) {
      console.warn('Failed to parse AI response as JSON, using as plain text');
      return {
        intent: 'General query',
        commands: [],
        explanation: responseContent,
        raw: responseContent
      };
    }
  }

  /**
   * Update context memory for conversation continuity
   */
  updateContextMemory(userQuery, aiResponse) {
    this.contextMemory.push(
      { role: 'user', content: userQuery },
      { role: 'assistant', content: aiResponse.explanation }
    );

    // Keep only recent context to avoid token limits
    if (this.contextMemory.length > this.maxContextLength * 2) {
      this.contextMemory = this.contextMemory.slice(-this.maxContextLength * 2);
    }
  }

  /**
   * Clear context memory
   */
  clearContext() {
    this.contextMemory = [];
    console.log('🧹 AI context memory cleared');
  }

  /**
   * Get context summary
   */
  getContextSummary() {
    return {
      memoryLength: this.contextMemory.length,
      lastQueries: this.contextMemory
        .filter(msg => msg.role === 'user')
        .slice(-3)
        .map(msg => msg.content.slice(0, 100))
    };
  }

  /**
   * Process image with AI (for future multimodal capabilities)
   */
  async processImage(imageBuffer, query = 'Analyze this image') {
    // Placeholder for future multimodal AI capabilities
    // Could integrate with GPT-4V or similar when available
    throw new Error('Image processing not yet implemented');
  }

  /**
   * Process voice command (for future voice capabilities)
   */
  async processVoice(audioBuffer) {
    // Placeholder for future voice processing capabilities
    // Could integrate with Whisper or similar when available
    throw new Error('Voice processing not yet implemented');
  }

  /**
   * Generate workflow from natural language
   */
  async generateWorkflow(description, context = {}) {
    const workflowQuery = `Create a detailed browser automation workflow for: "${description}". 
    
Please provide a workflow with multiple steps that can accomplish this task. Each step should be specific and actionable.

Context: ${JSON.stringify(context)}

Format as a workflow with these step types: navigate, click, type, wait, extract, screenshot.`;

    const response = await this.processQuery(workflowQuery, context);
    
    if (response.commands && response.commands.length > 0) {
      return {
        name: description.slice(0, 50),
        description: response.explanation,
        steps: response.commands.map((cmd, index) => ({
          id: `step_${index + 1}`,
          type: cmd.type,
          params: cmd.params,
          description: `Step ${index + 1}: ${cmd.type}`
        }))
      };
    }

    return null;
  }
}

module.exports = AIIntegration;