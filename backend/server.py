from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from playwright.async_api import async_playwright
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

@app.post("/api/proxy/browser")
async def proxy_with_browser(request_data: Dict[str, Any]):
    """Advanced proxy using headless browser for JavaScript-heavy sites with enhanced anti-detection"""
    try:
        url = request_data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL required")
        
        async with async_playwright() as p:
            # Launch browser with enhanced stealth configuration
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            
            # Enhanced browser context with real browser fingerprint
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York',
                permissions=['geolocation'],
                extra_http_headers={
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1'
                }
            )
            
            # Add script to override webdriver detection
            await context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                window.chrome = {
                    runtime: {},
                };
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                // Remove automation indicators
                delete navigator.__proto__.webdriver;
            """)
            
            page = await context.new_page()
            
            # Navigate with enhanced options
            try:
                await page.goto(url, wait_until='networkidle', timeout=45000)
                
                # Wait for dynamic content to load
                await page.wait_for_timeout(5000)
                
                # Try to wait for main content containers
                try:
                    await page.wait_for_selector('body', timeout=10000)
                except:
                    pass
                
            except Exception as nav_error:
                logger.warning(f"Navigation warning for {url}: {str(nav_error)}")
                # Continue with whatever content was loaded
            
            # Get the fully rendered page content
            content = await page.content()
            
            # Parse and enhance HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Enhanced frame-busting script removal
            scripts_to_remove = []
            for script in soup.find_all('script'):
                script_content = script.string or ''
                script_src = script.get('src', '')
                
                # Remove various anti-iframe and detection scripts
                removal_keywords = [
                    'top.location', 'frameElement', 'self !== top', 'parent.frames',
                    'window.top', 'top != self', 'parent != window', 'top != window',
                    'self != top', 'frameElement != null', 'window.frameElement',
                    'document.referrer', 'window.parent', 'top.document',
                    'webdriver', 'automation', 'headless'
                ]
                
                if any(keyword in script_content.lower() for keyword in removal_keywords):
                    scripts_to_remove.append(script)
                elif 'analytics' in script_src or 'tracking' in script_src:
                    scripts_to_remove.append(script)
            
            # Remove problematic scripts
            for script in scripts_to_remove:
                script.decompose()
            
            # Remove/modify problematic meta tags
            meta_tags_to_remove = []
            for meta in soup.find_all('meta'):
                http_equiv = meta.get('http-equiv', '').lower()
                name = meta.get('name', '').lower()
                
                if http_equiv in ['x-frame-options', 'content-security-policy']:
                    meta_tags_to_remove.append(meta)
                elif name in ['referrer'] and 'no-referrer' in meta.get('content', ''):
                    meta['content'] = 'unsafe-url'
            
            for meta in meta_tags_to_remove:
                meta.decompose()
            
            # Add enhanced base tag and meta tags
            if soup.head:
                # Base tag for relative URLs
                base_tag = soup.new_tag("base", href=url)
                soup.head.insert(0, base_tag)
                
                # Override CSP
                csp_meta = soup.new_tag("meta")
                csp_meta.attrs['http-equiv'] = 'Content-Security-Policy'
                csp_meta.attrs['content'] = "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:; frame-ancestors *;"
                soup.head.append(csp_meta)
                
                # Ensure viewport
                viewport_meta = soup.new_tag("meta", name="viewport", content="width=device-width, initial-scale=1.0")
                soup.head.append(viewport_meta)
            
            # Enhanced CSS injection
            style_tag = soup.new_tag("style")
            style_tag.string = """
                /* Enhanced iframe compatibility styles */
                body { 
                    margin: 0 !important; 
                    padding: 0 !important; 
                    overflow-x: auto !important;
                    min-height: 100vh !important;
                    width: 100% !important;
                }
                
                * { 
                    box-sizing: border-box !important; 
                }
                
                iframe, embed, object { 
                    max-width: 100% !important; 
                    height: auto !important; 
                }
                
                /* Fix common layout issues */
                .header, .navigation, nav, header { 
                    position: relative !important; 
                }
                
                /* Ensure content is visible */
                [style*="display: none"], [style*="visibility: hidden"] {
                    display: block !important;
                    visibility: visible !important;
                }
                
                /* Override fixed positioning that might break iframe */
                .fixed, [style*="position: fixed"] {
                    position: relative !important;
                }
            """
            if soup.head:
                soup.head.append(style_tag)
            elif soup.body:
                soup.body.insert(0, style_tag)
            
            # Add JavaScript to enhance compatibility
            js_tag = soup.new_tag("script")
            js_tag.string = """
                // Enhanced iframe compatibility JavaScript
                (function() {
                    'use strict';
                    
                    // Override common frame-busting attempts
                    try {
                        if (window.top !== window.self) {
                            window.top = window.self;
                        }
                        if (window.parent !== window.self) {
                            window.parent = window.self;
                        }
                        
                        // Override frame detection
                        Object.defineProperty(window, 'frameElement', {
                            get: function() { return null; },
                            configurable: true
                        });
                        
                        // Prevent redirect attempts
                        var originalReplace = window.location.replace;
                        window.location.replace = function(url) {
                            console.log('Blocked redirect attempt to:', url);
                        };
                        
                        var originalAssign = window.location.assign;
                        window.location.assign = function(url) {
                            console.log('Blocked navigation attempt to:', url);
                        };
                        
                    } catch (e) {
                        console.log('Frame compatibility script error:', e);
                    }
                })();
            """
            if soup.body:
                soup.body.append(js_tag)
            
            await browser.close()
            
            return {
                "content": str(soup),
                "status_code": 200,
                "headers": {"Content-Type": "text/html; charset=utf-8"},
                "url": url,
                "method": "enhanced_browser_rendered",
                "iframe_safe": True,
                "anti_detection": True
            }
            
    except Exception as e:
        logger.error(f"Error with enhanced browser proxy: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced browser proxy error: {str(e)}")

@app.post("/api/proxy/enhanced")
async def enhanced_proxy_request(request_data: Dict[str, Any]):
    """Enhanced proxy with better header handling and iframe support"""
    try:
        url = request_data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL required")
        
        # For YouTube, try a different approach - return iframe HTML directly
        if 'youtube.com' in url:
            iframe_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>YouTube - Kairo Browser</title>
                <style>
                    body {{ 
                        margin: 0; 
                        padding: 0; 
                        overflow: hidden;
                        background: #000;
                    }}
                    iframe {{ 
                        width: 100vw; 
                        height: 100vh; 
                        border: none; 
                    }}
                    .youtube-container {{
                        position: relative;
                        width: 100%;
                        height: 100vh;
                        background: #0f0f0f;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-family: Arial, sans-serif;
                    }}
                    .youtube-message {{
                        text-align: center;
                        padding: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="youtube-container">
                    <div class="youtube-message">
                        <h2>🎥 YouTube Integration</h2>
                        <p>AI successfully opened YouTube!</p>
                        <p>URL: {url}</p>
                        <p style="font-size: 14px; opacity: 0.7;">
                            Note: YouTube prevents embedding in iframes for security.<br>
                            Try asking AI to open other sites like "Open Google" or "Open Wikipedia"
                        </p>
                        <button onclick="window.open('{url}', '_blank')" 
                                style="background: #ff0000; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px;">
                            Open YouTube in New Tab
                        </button>
                    </div>
                </div>
            </body>
            </html>
            """
            
            return {
                "content": iframe_html,
                "status_code": 200,
                "headers": {"Content-Type": "text/html"},
                "url": url,
                "iframe_safe": True,
                "method": "youtube_fallback"
            }
        
        # For other sites, use the enhanced proxy
        return await proxy_request(request_data)
            
    except Exception as e:
        logger.error(f"Error with enhanced proxy: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced proxy error: {str(e)}")

@app.post("/api/proxy")
async def proxy_request(request_data: Dict[str, Any]):
    """Proxy requests to external websites with header manipulation to bypass iframe restrictions"""
    try:
        url = request_data.get("url")
        if not url:
            raise HTTPException(status_code=400, detail="URL required")
        
        # Custom headers to mimic a regular browser
        custom_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=custom_headers, follow_redirects=True)
            
            # Parse and clean HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove or modify meta tags that prevent embedding
            for meta in soup.find_all('meta'):
                if meta.get('http-equiv') == 'X-Frame-Options':
                    meta.decompose()
                elif meta.get('http-equiv') == 'Content-Security-Policy':
                    meta.decompose()
            
            # Remove or modify headers that prevent iframe embedding
            for script in soup.find_all('script'):
                script_content = script.string
                if script_content and ('frameElement' in script_content or 'top.location' in script_content):
                    # Remove scripts that detect iframe embedding
                    script.decompose()
            
            # Add base tag for relative URLs
            base_tag = soup.new_tag("base", href=url)
            if soup.head:
                soup.head.insert(0, base_tag)
            
            # Add custom CSS to ensure content is visible
            style_tag = soup.new_tag("style")
            style_tag.string = """
                body { margin: 0; padding: 0; overflow-x: auto; }
                * { box-sizing: border-box; }
            """
            if soup.head:
                soup.head.append(style_tag)
            
            # Clean headers for response (remove blocking headers)
            clean_headers = dict(response.headers)
            headers_to_remove = [
                'x-frame-options', 'X-Frame-Options',
                'content-security-policy', 'Content-Security-Policy',
                'x-content-type-options', 'X-Content-Type-Options'
            ]
            
            for header in headers_to_remove:
                clean_headers.pop(header, None)
            
            return {
                "content": str(soup),
                "status_code": response.status_code,
                "headers": clean_headers,
                "url": str(response.url),
                "iframe_safe": True
            }
            
    except Exception as e:
        logger.error(f"Error proxying request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error proxying request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)