"""
API routes for Kairo AI Browser
"""
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import (
    BrowserCommand, AIQuery, Workflow, ProxyRequest, 
    APIResponse, HealthCheck
)
from services.ai_service import ai_service
from services.browser_service import browser_service
from services.proxy_service import proxy_service
from services.workflow_service import workflow_service
from database.mongodb import db_manager

# Import enhanced routes
from api.enhanced_routes import enhanced_router

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()

# Include enhanced routes
router.include_router(enhanced_router, prefix="", tags=["enhanced"])

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """System health check"""
    try:
        # Check database health
        db_health = db_manager.health_check()
        
        health_data = HealthCheck(
            status="healthy",
            timestamp=datetime.now(),
            services=db_health
        )
        
        logger.info("✅ Health check passed")
        return health_data
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")

@router.post("/ai/query")
async def process_ai_query(query: AIQuery):
    """Process AI natural language query"""
    try:
        logger.info(f"🤖 Processing AI query from session {query.session_id}")
        
        # Process with AI service
        response = ai_service.process_query(query.query, query.context)
        
        # Store interaction
        session_id = query.session_id or "anonymous"
        db_manager.store_ai_interaction(session_id, query.query, response, query.context)
        
        logger.info("✅ AI query processed successfully")
        return response
        
    except ValueError as ve:
        logger.error(f"❌ AI configuration error: {ve}")
        raise HTTPException(status_code=503, detail=str(ve))
    except Exception as e:
        logger.error(f"❌ AI query processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI processing error: {str(e)}")

@router.post("/browser/execute")
async def execute_browser_command(command: BrowserCommand):
    """Execute browser command"""
    try:
        logger.info(f"🎮 Executing browser command: {command.command}")
        
        result = await browser_service.execute_command(
            command=command.command,
            url=command.url,
            selector=command.selector,
            text=command.text,
            session_id=command.session_id
        )
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=400, detail=result.get("error", "Command execution failed"))
        
        logger.info("✅ Browser command executed successfully")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Browser command execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Command execution error: {str(e)}")

@router.post("/workflow/execute")
async def execute_workflow(workflow: Workflow, background_tasks: BackgroundTasks):
    """Execute automated workflow"""
    try:
        logger.info(f"⚙️ Starting workflow: {workflow.name}")
        
        result = await workflow_service.execute_workflow(
            name=workflow.name,
            steps=[step.dict() for step in workflow.steps],
            profile=workflow.profile,
            timeout_ms=workflow.timeout_ms
        )
        
        logger.info("✅ Workflow started successfully")
        return result
        
    except Exception as e:
        logger.error(f"❌ Workflow execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Workflow error: {str(e)}")

@router.get("/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get workflow execution status"""
    try:
        workflow = await workflow_service.get_workflow_status(workflow_id)
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        logger.info(f"📊 Retrieved workflow status: {workflow_id}")
        return workflow
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get workflow status: {e}")
        raise HTTPException(status_code=500, detail=f"Status retrieval error: {str(e)}")

@router.get("/sessions")
async def get_active_sessions():
    """Get active browser sessions"""
    try:
        sessions = browser_service.get_active_sessions()
        
        logger.info("📊 Retrieved active sessions")
        return sessions
        
    except Exception as e:
        logger.error(f"❌ Failed to get sessions: {e}")
        raise HTTPException(status_code=500, detail=f"Session retrieval error: {str(e)}")

@router.post("/proxy/enhanced")
async def enhanced_proxy_request(request_data: Dict[str, Any]):
    """Enhanced proxy with smart routing"""
    url = request_data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL required")
    
    try:
        logger.info(f"🚀 Enhanced proxy request for: {url}")
        
        result = await proxy_service.route_request(
            url=url,
            method=request_data.get("method", "GET"),
            headers=request_data.get("headers")
        )
        
        logger.info(f"✅ Enhanced proxy completed using: {result.get('method', 'unknown')}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Enhanced proxy failed: {e}")
        raise HTTPException(status_code=500, detail=f"Enhanced proxy error: {str(e)}")

@router.post("/proxy/browser")
async def browser_proxy_request(request_data: Dict[str, Any]):
    """Browser proxy with Playwright"""
    url = request_data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL required")
    
    try:
        logger.info(f"🖥️ Browser proxy request for: {url}")
        
        result = await proxy_service.browser_proxy(
            url=url,
            custom_headers=request_data.get("headers")
        )
        
        logger.info("✅ Browser proxy completed")
        return result
        
    except Exception as e:
        logger.error(f"❌ Browser proxy failed: {e}")
        raise HTTPException(status_code=500, detail=f"Browser proxy error: {str(e)}")

@router.post("/proxy")
async def basic_proxy_request(request_data: Dict[str, Any]):
    """Basic HTTP proxy"""
    url = request_data.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="URL required")
    
    try:
        logger.info(f"🌐 Basic proxy request for: {url}")
        
        result = await proxy_service.enhanced_http_proxy(
            url=url,
            custom_headers=request_data.get("headers")
        )
        
        logger.info("✅ Basic proxy completed")
        return result
        
    except Exception as e:
        logger.error(f"❌ Basic proxy failed: {e}")
        raise HTTPException(status_code=500, detail=f"Basic proxy error: {str(e)}")

@router.post("/navigate")
async def navigate_to_url(request_data: Dict[str, Any]):
    """Navigate to URL with enhanced proxy loading"""
    url = request_data.get("url")
    session_id = request_data.get("session_id")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL required")
    
    try:
        logger.info(f"🧭 Navigation request to: {url}")
        
        # Execute navigation command
        nav_result = await browser_service.execute_command(
            command="navigate",
            url=url,
            session_id=session_id
        )
        
        # Load content via enhanced proxy
        try:
            proxy_result = await proxy_service.route_request(url)
            nav_result["content"] = proxy_result.get("content", "")
            nav_result["proxy_method"] = proxy_result.get("method", "unknown")
        except Exception as proxy_error:
            logger.warning(f"Proxy loading failed: {proxy_error}")
            nav_result["proxy_error"] = str(proxy_error)
        
        logger.info("✅ Navigation completed")
        return nav_result
        
    except Exception as e:
        logger.error(f"❌ Navigation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Navigation error: {str(e)}")

# Additional utility endpoints
@router.get("/workflows/active")
async def get_active_workflows():
    """Get active workflows"""
    try:
        workflows = workflow_service.get_active_workflows()
        return workflows
    except Exception as e:
        logger.error(f"❌ Failed to get active workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/workflow/{workflow_id}")
async def cancel_workflow(workflow_id: str):
    """Cancel active workflow"""
    try:
        success = await workflow_service.cancel_workflow(workflow_id)
        if success:
            return {"message": f"Workflow {workflow_id} cancelled"}
        else:
            raise HTTPException(status_code=404, detail="Workflow not found or not active")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to cancel workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_session_info(session_id: str):
    """Get specific session information"""
    try:
        session_info = browser_service.get_session_info(session_id)
        if session_info:
            return session_info
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to get session info: {e}")
        raise HTTPException(status_code=500, detail=str(e))