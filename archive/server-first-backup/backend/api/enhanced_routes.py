"""
Enhanced API Routes - All New Fellou.ai Feature Endpoints
Complete API integration for all advanced features
"""
import logging
from datetime import datetime
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel

# Import all new services
from services.memory_service import memory_service
from services.search_service import search_service
from services.intelligence_service import intelligence_service
from services.report_service import report_service
from services.accessibility_service import accessibility_service
from services.shadow_browser_service import shadow_browser_service
from services.agent_builder_service import agent_builder_service
from integrations.notion_integration import notion_integration
from database.mongodb import db_manager

logger = logging.getLogger(__name__)

# Enhanced API router
enhanced_router = APIRouter()

# ============================================================================
# PHASE 1: MEMORY & WORKFLOW ENDPOINTS
# ============================================================================

class MemoryInteraction(BaseModel):
    user_id: str
    command: str
    context: Dict[str, Any] = {}
    outcome: str = 'success'

@enhanced_router.post("/memory/learn")
async def learn_from_interaction(interaction: MemoryInteraction):
    """Learn from user interaction for personalization"""
    try:
        interaction_data = {
            'command': interaction.command,
            'context': interaction.context,
            'outcome': interaction.outcome
        }
        
        await memory_service.learn_from_interaction(interaction.user_id, interaction_data)
        
        return {
            'success': True,
            'message': 'Interaction learned successfully'
        }
    except Exception as e:
        logger.error(f"❌ Memory learning failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@enhanced_router.get("/memory/suggestions/{user_id}")
async def get_personalized_suggestions(user_id: str, context: str = Query(None)):
    """Get personalized suggestions for user"""
    try:
        current_context = {}
        if context:
            import json
            current_context = json.loads(context)
        
        suggestions = await memory_service.get_personalized_suggestions(user_id, current_context)
        
        return {
            'user_id': user_id,
            'suggestions': suggestions,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Suggestions generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class BackgroundTask(BaseModel):
    type: str
    config: Dict[str, Any]

@enhanced_router.post("/shadow/execute")
async def execute_background_task(task: BackgroundTask):
    """Execute task in background shadow browser"""
    try:
        task_id = await shadow_browser_service.execute_background_task(task.config)
        
        return {
            'task_id': task_id,
            'status': 'queued',
            'message': 'Background task started'
        }
    except Exception as e:
        logger.error(f"❌ Background task failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@enhanced_router.get("/shadow/status/{task_id}")
async def get_task_status(task_id: str):
    """Get background task status"""
    try:
        status = await shadow_browser_service.get_task_status(task_id)
        return status
    except Exception as e:
        logger.error(f"❌ Task status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PHASE 2: DEEP SEARCH & INTELLIGENCE ENDPOINTS
# ============================================================================

class SearchRequest(BaseModel):
    query: str
    config: Dict[str, Any] = {}

@enhanced_router.post("/search/deep")
async def execute_deep_search(request: SearchRequest):
    """Execute comprehensive deep search"""
    try:
        result = await search_service.execute_deep_search(request.query, request.config)
        
        return result
    except Exception as e:
        logger.error(f"❌ Deep search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class IntelligenceRequest(BaseModel):
    user_id: str
    context: Dict[str, Any]

@enhanced_router.post("/intelligence/analyze")
async def analyze_context_and_suggest(request: IntelligenceRequest):
    """Analyze context and provide proactive suggestions"""
    try:
        result = await intelligence_service.analyze_context_and_suggest(
            request.user_id, 
            request.context
        )
        
        return result
    except Exception as e:
        logger.error(f"❌ Intelligence analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PHASE 3: REPORT GENERATION & INTEGRATIONS
# ============================================================================

class ReportRequest(BaseModel):
    type: str
    config: Dict[str, Any] = {}

@enhanced_router.post("/reports/generate")
async def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    """Generate comprehensive AI-powered report"""
    try:
        # Execute report generation in background for large reports
        if request.config.get('async', True):
            background_tasks.add_task(
                report_service.generate_report, 
                {'type': request.type, **request.config}
            )
            return {
                'message': 'Report generation started',
                'status': 'processing'
            }
        else:
            result = await report_service.generate_report({'type': request.type, **request.config})
            return result
            
    except Exception as e:
        logger.error(f"❌ Report generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class IntegrationAuth(BaseModel):
    service: str
    credentials: Dict[str, Any]

@enhanced_router.post("/integrations/authenticate")
async def authenticate_integration(auth: IntegrationAuth):
    """Authenticate with external service integration"""
    try:
        if auth.service.lower() == 'notion':
            success = await notion_integration.authenticate(auth.credentials)
            
            return {
                'service': auth.service,
                'authenticated': success,
                'capabilities': notion_integration.get_capabilities() if success else None
            }
        else:
            return {'error': f'Integration {auth.service} not supported yet'}
            
    except Exception as e:
        logger.error(f"❌ Integration authentication failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class IntegrationSearch(BaseModel):
    service: str
    query: str
    config: Dict[str, Any] = {}

@enhanced_router.post("/integrations/search")
async def search_integration(search: IntegrationSearch):
    """Search within external service integration"""
    try:
        if search.service.lower() == 'notion':
            if not notion_integration.is_authenticated():
                raise HTTPException(status_code=401, detail="Not authenticated with Notion")
            
            result = await notion_integration.search(search.query, **search.config)
            return result
        else:
            return {'error': f'Integration {search.service} not supported yet'}
            
    except Exception as e:
        logger.error(f"❌ Integration search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PHASE 4: ACCESSIBILITY ENDPOINTS
# ============================================================================

class TTSRequest(BaseModel):
    text: str
    options: Dict[str, Any] = {}

@enhanced_router.post("/accessibility/tts")
async def text_to_speech(request: TTSRequest):
    """Convert text to speech"""
    try:
        result = await accessibility_service.text_to_speech(request.text, request.options)
        return result
    except Exception as e:
        logger.error(f"❌ Text-to-speech failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = 'auto'

@enhanced_router.post("/accessibility/translate")
async def translate_text(request: TranslateRequest):
    """Translate text to target language"""
    try:
        result = await accessibility_service.translate_text(
            request.text, 
            request.target_language, 
            request.source_language
        )
        return result
    except Exception as e:
        logger.error(f"❌ Translation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class LayoutAdjustment(BaseModel):
    adjustments: Dict[str, Any]

@enhanced_router.post("/accessibility/layout")
async def adjust_page_layout(request: LayoutAdjustment):
    """Generate accessibility layout adjustments"""
    try:
        result = await accessibility_service.adjust_page_layout(request.adjustments)
        return result
    except Exception as e:
        logger.error(f"❌ Layout adjustment failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class ReadingAssist(BaseModel):
    text: str
    reading_level: str = 'default'

@enhanced_router.post("/accessibility/reading")
async def reading_assistance(request: ReadingAssist):
    """Provide reading assistance"""
    try:
        result = await accessibility_service.reading_assistance(
            request.text, 
            request.reading_level
        )
        return result
    except Exception as e:
        logger.error(f"❌ Reading assistance failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# PHASE 5: AGENT BUILDER ENDPOINTS
# ============================================================================

class AgentFromDescription(BaseModel):
    description: str
    user_id: str
    config: Dict[str, Any] = {}

@enhanced_router.post("/agents/create/description")
async def create_agent_from_description(request: AgentFromDescription):
    """Create custom agent from natural language description"""
    try:
        result = await agent_builder_service.create_agent_from_description(
            request.description,
            request.user_id,
            request.config
        )
        return result
    except Exception as e:
        logger.error(f"❌ Agent creation from description failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class AgentFromCode(BaseModel):
    code: str
    metadata: Dict[str, Any]
    user_id: str

@enhanced_router.post("/agents/create/code")
async def create_agent_from_code(request: AgentFromCode):
    """Create agent from JavaScript/Python code"""
    try:
        result = await agent_builder_service.create_agent_from_code(
            request.code,
            request.metadata,
            request.user_id
        )
        return result
    except Exception as e:
        logger.error(f"❌ Agent creation from code failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class AgentExecution(BaseModel):
    agent_id: str
    input_data: Dict[str, Any] = {}
    user_id: str

@enhanced_router.post("/agents/execute")
async def execute_agent(request: AgentExecution):
    """Execute a custom agent"""
    try:
        result = await agent_builder_service.execute_agent(
            request.agent_id,
            request.input_data,
            request.user_id
        )
        return result
    except Exception as e:
        logger.error(f"❌ Agent execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@enhanced_router.get("/agents/user/{user_id}")
async def list_user_agents(user_id: str):
    """List all agents created by user"""
    try:
        agents = await agent_builder_service.list_user_agents(user_id)
        return {
            'user_id': user_id,
            'agents': agents,
            'total': len(agents)
        }
    except Exception as e:
        logger.error(f"❌ Agent listing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@enhanced_router.get("/agents/marketplace")
async def get_agent_marketplace():
    """Get agent marketplace with templates and public agents"""
    try:
        marketplace = await agent_builder_service.get_agent_marketplace()
        return {
            'agents': marketplace,
            'total': len(marketplace)
        }
    except Exception as e:
        logger.error(f"❌ Marketplace loading failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# TIMELINE & ANALYTICS ENDPOINTS
# ============================================================================

@enhanced_router.get("/timeline/{user_id}")
async def get_user_timeline(
    user_id: str,
    date_range: str = Query('today'),
    activity_type: str = Query('all'),
    workspace: str = Query('all')
):
    """Get user activity timeline"""
    try:
        # Get timeline data from database
        timeline_data = await db_manager.get_user_timeline(
            user_id, 
            date_range, 
            activity_type, 
            workspace
        )
        
        return {
            'user_id': user_id,
            'timeline': timeline_data,
            'filters': {
                'date_range': date_range,
                'activity_type': activity_type,
                'workspace': workspace
            }
        }
    except Exception as e:
        logger.error(f"❌ Timeline retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@enhanced_router.get("/analytics/user/{user_id}")
async def get_user_analytics(user_id: str, period: str = Query('week')):
    """Get user analytics and insights"""
    try:
        analytics = await db_manager.get_user_analytics(user_id, period)
        
        return {
            'user_id': user_id,
            'period': period,
            'analytics': analytics,
            'generated_at': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Analytics generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# WORKSPACE MANAGEMENT ENDPOINTS
# ============================================================================

class WorkspaceCreate(BaseModel):
    name: str
    description: str
    user_id: str
    settings: Dict[str, Any] = {}

@enhanced_router.post("/workspaces/create")
async def create_workspace(workspace: WorkspaceCreate):
    """Create new workspace"""
    try:
        workspace_data = {
            'name': workspace.name,
            'description': workspace.description,
            'user_id': workspace.user_id,
            'settings': workspace.settings,
            'created_at': datetime.now()
        }
        
        workspace_id = await db_manager.create_workspace(workspace_data)
        
        return {
            'workspace_id': workspace_id,
            'workspace': workspace_data,
            'success': True
        }
    except Exception as e:
        logger.error(f"❌ Workspace creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@enhanced_router.get("/workspaces/user/{user_id}")
async def list_user_workspaces(user_id: str):
    """List user workspaces"""
    try:
        workspaces = await db_manager.get_user_workspaces(user_id)
        
        return {
            'user_id': user_id,
            'workspaces': workspaces,
            'total': len(workspaces)
        }
    except Exception as e:
        logger.error(f"❌ Workspace listing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ENHANCED SYSTEM STATUS
# ============================================================================

@enhanced_router.get("/system/status")
async def get_enhanced_system_status():
    """Get comprehensive system status including all new features"""
    try:
        status = {
            'timestamp': datetime.now().isoformat(),
            'services': {
                'memory_service': 'active',
                'search_service': 'active',
                'intelligence_service': 'active',
                'report_service': 'active',
                'accessibility_service': 'active',
                'shadow_browser_service': 'active',
                'agent_builder_service': 'active'
            },
            'integrations': {
                'notion': notion_integration.is_authenticated()
            },
            'shadow_browsers': {
                'active_browsers': len(shadow_browser_service.browser_pool),
                'active_tasks': len(shadow_browser_service.active_tasks)
            },
            'agents': {
                'active_agents': len(agent_builder_service.active_agents)
            }
        }
        
        return status
    except Exception as e:
        logger.error(f"❌ System status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))