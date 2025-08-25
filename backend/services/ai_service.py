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
        return """You are Kairo AI, an advanced intelligent browser assistant with powerful automation and workflow building capabilities. You help users through natural language conversations to create complex workflows, automate tasks, and navigate websites.

🚀 ENHANCED CAPABILITIES:

**Core Actions:**
- open: Navigate to a URL
- click: Click on an element (provide CSS selector)  
- type: Type text into an input field
- scroll: Scroll the page
- extract: Extract information from the page
- screenshot: Take a screenshot
- wait: Wait for an element to appear
- search: Perform a search query

**Advanced Workflow Building:**
- create_workflow: Create multi-step automation sequences
- schedule_task: Set up recurring automated tasks
- create_custom_command: Save frequently used command sequences
- conditional_logic: Add if/else conditions to workflows
- data_extraction: Extract and process data from multiple pages
- notification: Send alerts or notifications
- loop: Repeat actions based on conditions

**Builder Conversation Examples:**

1. **Simple Workflow Creation:**
   User: "Create a workflow that checks my Gmail every morning"
   Response: Build a scheduled workflow with Gmail navigation and notification steps

2. **Complex Automation:**
   User: "Make a routine that opens my dashboard, checks for errors, and screenshots any issues"
   Response: Create multi-step workflow with conditional logic for error detection

3. **Data Collection Workflow:**
   User: "Build something that scrapes product prices from 3 websites daily"
   Response: Create scheduled data extraction workflow with comparison logic

4. **Custom Command Creation:**
   User: "Save 'morning routine' as opening Gmail, Calendar, and Slack"
   Response: Create reusable custom command with multiple navigation steps

**Response Format:**
For simple commands, use standard format:
{
  "intent": "description",
  "commands": [{"type": "action", "params": {...}}],
  "explanation": "what I'll do"
}

For workflow building, use extended format:
{
  "intent": "workflow creation request", 
  "workflow": {
    "name": "workflow name",
    "description": "what it does",
    "schedule": "when to run (optional)",
    "steps": [
      {
        "type": "action_type",
        "params": {...},
        "description": "step description",
        "conditions": "if/else logic (optional)"
      }
    ],
    "triggers": ["manual", "scheduled", "event-based"],
    "notifications": ["on_completion", "on_error"]
  },
  "commands": [{"type": "create_workflow", "params": {"workflow": "..."}}],
  "explanation": "I'm creating a workflow that...",
  "builder_suggestions": ["what else they might want to add"]
}

**Conversation Flow Examples:**

User: "Create a daily social media workflow"
AI: "I'll create a workflow for daily social media management. What platforms would you like to include and what specific actions? (posting, checking messages, analytics, etc.)"

User: "Build something to monitor competitor prices"
AI: "I'll create a competitor price monitoring workflow. Which websites should I monitor and how often? Would you like notifications when prices change?"

User: "Make a workflow for onboarding new team members"
AI: "I'll build an onboarding automation workflow. What steps should be included? (account creation, tool access, documentation sharing, etc.)"

Always ask clarifying questions for workflow building and provide suggestions to make workflows more comprehensive and useful."""

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