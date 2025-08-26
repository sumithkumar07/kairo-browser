"""
Streamlined Backend for Local-First Architecture
Only keeps essential endpoints that desktop app might need
Removes all proxy/iframe functionality
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
from groq import Groq
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Kairo AI Browser - Streamlined Backend", version="2.0.0")

# CORS middleware - only needed if desktop app makes web requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Pydantic models
class AIQuery(BaseModel):
    query: str
    session_id: Optional[str] = None
    context: Optional[Dict] = None

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0-streamlined",
        "architecture": "local-first-support"
    }

@app.post("/api/ai/query")
async def process_ai_query(query: AIQuery):
    """
    AI query processing - can be used by desktop app if needed
    Most AI processing should be done locally in desktop app
    """
    try:
        if not groq_client:
            raise HTTPException(status_code=500, detail="Groq API not configured")
        
        # Simplified system prompt for local-first environment
        system_prompt = """You are Kairo AI assistant for a local-first browser environment.
        
The user has a native desktop browser with embedded Chromium that can access ANY website directly.
No proxy limitations, no iframe restrictions, no CORS issues.

Available commands for desktop app:
- navigate: Go to any URL
- click: Click elements  
- type: Type text
- youtube_video: Play YouTube videos natively
- search: Search on current page

Respond with JSON:
{
  "intent": "user intent",
  "commands": [{"type": "command", "params": {...}}],
  "explanation": "what you'll do"
}"""

        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query.query}
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=800
        )
        
        ai_response = response.choices[0].message.content
        
        # Try to parse JSON response
        try:
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_content = ai_response[json_start:json_end]
                parsed_response = json.loads(json_content)
            else:
                parsed_response = json.loads(ai_response)
        except json.JSONDecodeError:
            parsed_response = {
                "intent": query.query,
                "commands": [],
                "explanation": ai_response
            }
        
        return parsed_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Optional: Keep minimal analytics endpoint
@app.get("/api/analytics/minimal")
async def minimal_analytics():
    """Minimal analytics for desktop app usage tracking (optional)"""
    return {
        "service": "kairo-streamlined-backend",
        "purpose": "minimal-cloud-support-for-local-first-app",
        "timestamp": datetime.now().isoformat(),
        "capabilities": [
            "ai_query_processing",
            "minimal_analytics",
            "health_checks"
        ]
    }

# Development info endpoint
@app.get("/api/info")
async def app_info():
    return {
        "name": "Kairo AI Browser - Streamlined Backend",
        "version": "2.0.0",
        "architecture": "local-first-support",
        "purpose": "Minimal cloud endpoints for desktop app",
        "removed_features": [
            "proxy_systems",
            "iframe_handling", 
            "cors_workarounds",
            "browser_automation", # Now done locally
            "session_management", # Now done locally
            "workflow_execution"  # Now done locally
        ],
        "remaining_features": [
            "ai_query_processing",
            "health_checks",
            "minimal_analytics"
        ],
        "primary_execution": "local_desktop_app"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)