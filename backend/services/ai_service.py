"""
AI service for natural language processing using Groq
"""
import json
import logging
from typing import Dict, Any, Optional
from groq import Groq
from config import settings

logger = logging.getLogger(__name__)

class AIService:
    """AI service for processing natural language queries"""
    
    def __init__(self):
        if not settings.GROQ_API_KEY:
            logger.warning("⚠️ Groq API key not configured")
            self.client = None
        else:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            logger.info("✅ Groq AI client initialized")
    
    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process natural language query and return browser commands"""
        if not self.client:
            raise ValueError("Groq AI not configured")
        
        try:
            logger.info(f"🔍 Processing AI query: {query}")
            
            # Enhanced system prompt for better browser automation
            system_prompt = self._get_system_prompt()
            
            # Prepare context-aware user message
            user_message = self._prepare_user_message(query, context)
            
            logger.info("📡 Making Groq API request")
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model=settings.GROQ_MODEL,
                temperature=0.3,
                max_tokens=1500
            )
            
            logger.info("✅ Groq API response received")
            ai_response = response.choices[0].message.content
            logger.debug(f"AI response preview: {ai_response[:100]}...")
            
            # Parse and validate response
            parsed_response = self._parse_response(ai_response)
            
            logger.info("✅ AI query processed successfully")
            return parsed_response
            
        except Exception as e:
            logger.error(f"❌ AI query processing failed: {str(e)}")
            return {
                "intent": query,
                "commands": [],
                "explanation": f"I encountered an error processing your request: {str(e)}",
                "error": str(e)
            }
    
    def _get_system_prompt(self) -> str:
        """Get enhanced system prompt for AI"""
        return """You are Kairo AI, an advanced intelligent browser assistant. You help users navigate and interact with websites through natural language commands.

Your capabilities include:
- Website navigation and browsing
- Form filling and interaction
- Information extraction
- Web automation workflows
- Search and research tasks

When a user asks you to do something, break it down into specific browser actions:
- open: Navigate to a URL
- click: Click on an element (provide CSS selector)  
- type: Type text into an input field
- scroll: Scroll the page
- extract: Extract information from the page
- screenshot: Take a screenshot
- wait: Wait for an element to appear
- search: Perform a search query

Always respond with a JSON object containing:
{
  "intent": "clear description of what user wants",
  "commands": [
    {
      "type": "action_type",
      "params": {
        "url": "full URL with https:// if needed",
        "selector": "specific CSS selector if needed", 
        "text": "exact text to type if needed",
        "element": "description of element to interact with",
        "wait_time": "milliseconds to wait if needed"
      }
    }
  ],
  "explanation": "Human readable explanation of what you'll do step by step"
}

Enhanced Examples:
- "Open YouTube" -> {"intent": "open YouTube video platform", "commands": [{"type": "open", "params": {"url": "https://www.youtube.com"}}], "explanation": "I will navigate to the YouTube website where you can watch videos and browse content."}

- "Search for AI tutorials" -> {"intent": "search for AI learning content", "commands": [{"type": "open", "params": {"url": "https://www.google.com"}}, {"type": "type", "params": {"selector": "input[name='q']", "text": "AI tutorials"}}, {"type": "click", "params": {"selector": "input[type='submit']"}}], "explanation": "I will open Google and search for AI tutorials to help you find learning resources."}

- "Go to Gmail" -> {"intent": "access email service", "commands": [{"type": "open", "params": {"url": "https://mail.google.com"}}], "explanation": "I will navigate to Gmail so you can access your email."}

Always provide helpful, accurate responses and ensure URLs are complete with protocols."""

    def _prepare_user_message(self, query: str, context: Optional[Dict[str, Any]]) -> str:
        """Prepare context-aware user message"""
        base_message = f"User request: {query}"
        
        if context:
            context_parts = []
            if context.get("currentUrl"):
                context_parts.append(f"Current page: {context['currentUrl']}")
            if context.get("sessionId"):
                context_parts.append(f"Session: {context['sessionId']}")
            
            if context_parts:
                base_message += f"\n\nContext: {'; '.join(context_parts)}"
        
        return base_message
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate AI response"""
        try:
            # Extract JSON from response if it contains extra text
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = response[json_start:json_end]
                parsed = json.loads(json_content)
            else:
                parsed = json.loads(response)
            
            # Validate required fields
            if not isinstance(parsed, dict):
                raise ValueError("Response must be a JSON object")
            
            # Ensure required fields exist
            parsed.setdefault("intent", "Process user request")
            parsed.setdefault("commands", [])
            parsed.setdefault("explanation", "I understand your request.")
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed: {e}")
            # Return a simple fallback response
            return {
                "intent": "Process user request",
                "commands": [],
                "explanation": response,
                "parsing_error": str(e)
            }

# Global AI service instance
ai_service = AIService()