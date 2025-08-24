from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import asyncio
import json
import uuid
from datetime import datetime
import logging
from pymongo import MongoClient
from groq import Groq
import httpx
from bs4 import BeautifulSoup
import base64
from io import BytesIO
from PIL import Image
import aiofiles
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Kairo AI Browser Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/kairo_browser")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize MongoDB client
client = MongoClient(MONGO_URL)
db = client.kairo_browser

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models
class BrowserCommand(BaseModel):
    command: str
    url: Optional[str] = None
    selector: Optional[str] = None
    text: Optional[str] = None
    session_id: Optional[str] = None

class AIQuery(BaseModel):
    query: str
    session_id: Optional[str] = None
    context: Optional[Dict] = None

class WorkflowStep(BaseModel):
    type: str  # open, click, type, wait_for, extract, screenshot
    url: Optional[str] = None
    selector: Optional[str] = None
    text: Optional[str] = None
    timeout_ms: Optional[int] = 5000

class Workflow(BaseModel):
    name: str
    steps: List[WorkflowStep]
    profile: Optional[str] = "default"
    timeout_ms: Optional[int] = 60000

# Global state for browser sessions
active_sessions = {}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/ai/query")
async def process_ai_query(query: AIQuery):
    """Process AI query and return browser commands"""
    try:
        logger.info(f"Processing AI query: {query.query}")
        if not groq_client:
            logger.error("Groq API not configured")
            raise HTTPException(status_code=500, detail="Groq API not configured")
        
        logger.info("Groq client available, making API call")
        # System prompt for browser automation
        system_prompt = """You are Kairo AI, an intelligent browser assistant. You help users navigate and interact with websites through natural language commands.

When a user asks you to do something, break it down into specific browser actions:
- open: Navigate to a URL
- click: Click on an element (provide CSS selector)  
- type: Type text into an input field
- scroll: Scroll the page
- extract: Extract information from the page
- screenshot: Take a screenshot
- wait: Wait for an element to appear

Respond with a JSON object containing:
{
  "intent": "description of what user wants",
  "commands": [
    {
      "type": "action_type",
      "params": {
        "url": "url if needed",
        "selector": "css selector if needed", 
        "text": "text to type if needed",
        "element": "description of element to interact with"
      }
    }
  ],
  "explanation": "Human readable explanation of what you'll do"
}

Examples:
- "Open YouTube" -> {"intent": "open YouTube", "commands": [{"type": "open", "params": {"url": "https://youtube.com"}}]}
- "Search for cats" -> {"intent": "search for cats", "commands": [{"type": "click", "params": {"selector": "input[type='search']"}}, {"type": "type", "params": {"text": "cats"}}]}
"""

        logger.info("Making Groq API request")
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query.query}
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=1000
        )
        
        logger.info("Groq API response received")
        ai_response = response.choices[0].message.content
        logger.info(f"AI response: {ai_response[:100]}...")
        
        # Try to parse JSON response
        try:
            # Extract JSON from response if it contains extra text
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_content = ai_response[json_start:json_end]
                parsed_response = json.loads(json_content)
            else:
                parsed_response = json.loads(ai_response)
        except json.JSONDecodeError:
            # If not JSON, create a simple response
            parsed_response = {
                "intent": query.query,
                "commands": [],
                "explanation": ai_response
            }
        
        # Store the interaction
        logger.info("Storing interaction in database")
        interaction = {
            "session_id": query.session_id or str(uuid.uuid4()),
            "query": query.query,
            "response": parsed_response,
            "timestamp": datetime.now(),
            "context": query.context
        }
        db.ai_interactions.insert_one(interaction)
        logger.info("Interaction stored successfully")
        
        return parsed_response
        
    except Exception as e:
        logger.error(f"Error processing AI query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.post("/api/browser/execute")
async def execute_browser_command(command: BrowserCommand):
    """Execute a browser command"""
    try:
        session_id = command.session_id or str(uuid.uuid4())
        
        result = {
            "session_id": session_id,
            "command": command.command,
            "status": "executed",
            "timestamp": datetime.now().isoformat()
        }
        
        if command.command == "open":
            if not command.url:
                raise HTTPException(status_code=400, detail="URL required for open command")
            
            # For web-based implementation, we'll return the URL to be loaded in iframe
            result["data"] = {
                "url": command.url,
                "action": "navigate"
            }
            
        elif command.command == "click":
            if not command.selector:
                raise HTTPException(status_code=400, detail="Selector required for click command")
            
            result["data"] = {
                "selector": command.selector,
                "action": "click"
            }
            
        elif command.command == "type":
            if not command.selector or not command.text:
                raise HTTPException(status_code=400, detail="Selector and text required for type command")
            
            result["data"] = {
                "selector": command.selector,
                "text": command.text,
                "action": "type"
            }
            
        else:
            result["status"] = "unknown_command"
            result["error"] = f"Unknown command: {command.command}"
        
        # Store command execution
        db.browser_commands.insert_one({
            "session_id": session_id,
            "command": command.dict(),
            "result": result,
            "timestamp": datetime.now()
        })
        
        return result
        
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except Exception as e:
        logger.error(f"Error executing browser command: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error executing command: {str(e)}")

@app.post("/api/workflow/execute")
async def execute_workflow(workflow: Workflow, background_tasks: BackgroundTasks):
    """Execute a browser workflow"""
    try:
        workflow_id = str(uuid.uuid4())
        
        # Store workflow
        workflow_doc = {
            "id": workflow_id,
            "name": workflow.name,
            "steps": [step.dict() for step in workflow.steps],
            "profile": workflow.profile,
            "timeout_ms": workflow.timeout_ms,
            "status": "pending",
            "created_at": datetime.now(),
            "results": []
        }
        db.workflows.insert_one(workflow_doc)
        
        # Execute workflow in background
        background_tasks.add_task(execute_workflow_background, workflow_id, workflow)
        
        return {
            "workflow_id": workflow_id,
            "status": "started",
            "message": f"Workflow '{workflow.name}' started with {len(workflow.steps)} steps"
        }
        
    except Exception as e:
        logger.error(f"Error starting workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting workflow: {str(e)}")

async def execute_workflow_background(workflow_id: str, workflow: Workflow):
    """Background task to execute workflow steps"""
    try:
        # Update status to running
        db.workflows.update_one(
            {"id": workflow_id},
            {"$set": {"status": "running", "started_at": datetime.now()}}
        )
        
        results = []
        
        for i, step in enumerate(workflow.steps):
            try:
                # Execute each step
                step_result = await execute_workflow_step(step)
                results.append({
                    "step": i,
                    "type": step.type,
                    "result": step_result,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Update progress
                db.workflows.update_one(
                    {"id": workflow_id},
                    {"$set": {"results": results, "current_step": i}}
                )
                
            except Exception as step_error:
                logger.error(f"Error in workflow step {i}: {str(step_error)}")
                results.append({
                    "step": i,
                    "type": step.type,
                    "error": str(step_error),
                    "timestamp": datetime.now().isoformat()
                })
                break
        
        # Mark as completed
        db.workflows.update_one(
            {"id": workflow_id},
            {
                "$set": {
                    "status": "completed",
                    "finished_at": datetime.now(),
                    "results": results
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error executing workflow {workflow_id}: {str(e)}")
        db.workflows.update_one(
            {"id": workflow_id},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e),
                    "finished_at": datetime.now()
                }
            }
        )

async def execute_workflow_step(step: WorkflowStep):
    """Execute a single workflow step"""
    if step.type == "open":
        return {"action": "navigate", "url": step.url}
    elif step.type == "wait":
        await asyncio.sleep(step.timeout_ms / 1000 if step.timeout_ms else 1)
        return {"action": "waited", "duration_ms": step.timeout_ms}
    elif step.type == "click":
        return {"action": "click", "selector": step.selector}
    elif step.type == "type":
        return {"action": "type", "selector": step.selector, "text": step.text}
    elif step.type == "screenshot":
        return {"action": "screenshot", "filename": f"screenshot_{datetime.now().isoformat()}.png"}
    else:
        return {"action": "unknown", "type": step.type}

@app.get("/api/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get workflow status and results"""
    try:
        workflow = db.workflows.find_one({"id": workflow_id})
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Remove MongoDB _id for JSON serialization
        workflow.pop("_id", None)
        return workflow
        
    except Exception as e:
        logger.error(f"Error getting workflow status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting workflow status: {str(e)}")

@app.get("/api/sessions")
async def get_active_sessions():
    """Get list of active browser sessions"""
    try:
        sessions = list(db.browser_commands.aggregate([
            {"$group": {"_id": "$session_id", "last_activity": {"$max": "$timestamp"}, "command_count": {"$sum": 1}}},
            {"$sort": {"last_activity": -1}},
            {"$limit": 10}
        ]))
        
        return {"sessions": sessions}
        
    except Exception as e:
        logger.error(f"Error getting sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting sessions: {str(e)}")

@app.post("/api/proxy")
async def proxy_request(request_data: Dict[str, Any]):
    """Proxy requests to external websites"""
    try:
        url = request_data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL required")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            
            # Parse and clean HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Add base tag for relative URLs
            base_tag = soup.new_tag("base", href=url)
            if soup.head:
                soup.head.insert(0, base_tag)
            
            return {
                "content": str(soup),
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "url": str(response.url)
            }
            
    except Exception as e:
        logger.error(f"Error proxying request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error proxying request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)