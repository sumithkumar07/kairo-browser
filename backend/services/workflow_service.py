"""
Workflow service for automated browser task execution
"""
import uuid
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from database.mongodb import db_manager
from services.browser_service import browser_service

logger = logging.getLogger(__name__)

class WorkflowService:
    """Automated workflow execution service"""
    
    def __init__(self):
        self.active_workflows = {}
        logger.info("✅ Workflow service initialized")
    
    async def execute_workflow(self, name: str, steps: List[Dict[str, Any]], 
                             profile: str = "default", timeout_ms: int = 60000) -> Dict[str, Any]:
        """Execute a multi-step browser workflow"""
        workflow_id = str(uuid.uuid4())
        
        try:
            logger.info(f"🚀 Starting workflow: {name} with {len(steps)} steps")
            
            # Create workflow document
            workflow_doc = {
                "id": workflow_id,
                "name": name,
                "steps": steps,
                "profile": profile,
                "timeout_ms": timeout_ms,
                "status": "pending",
                "created_at": datetime.now(),
                "results": []
            }
            
            # Store workflow
            db_manager.store_workflow(workflow_doc)
            
            # Add to active workflows
            self.active_workflows[workflow_id] = {
                "status": "starting",
                "created_at": datetime.now(),
                "name": name
            }
            
            # Execute workflow in background
            asyncio.create_task(self._execute_workflow_background(workflow_id, name, steps, timeout_ms))
            
            logger.info(f"✅ Workflow started: {workflow_id}")
            return {
                "workflow_id": workflow_id,
                "status": "started",
                "message": f"Workflow '{name}' started with {len(steps)} steps"
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to start workflow: {e}")
            raise
    
    async def _execute_workflow_background(self, workflow_id: str, name: str, 
                                         steps: List[Dict[str, Any]], timeout_ms: int):
        """Background task to execute workflow steps"""
        try:
            logger.info(f"⚙️ Executing workflow {workflow_id} in background")
            
            # Update status to running
            db_manager.update_workflow(workflow_id, {
                "status": "running",
                "started_at": datetime.now()
            })
            
            self.active_workflows[workflow_id]["status"] = "running"
            
            results = []
            session_id = f"workflow_{workflow_id}"
            
            # Execute each step
            for i, step in enumerate(steps):
                try:
                    logger.info(f"📋 Executing step {i+1}/{len(steps)}: {step.get('type', 'unknown')}")
                    
                    step_result = await self._execute_workflow_step(step, session_id)
                    
                    results.append({
                        "step": i,
                        "type": step.get("type"),
                        "result": step_result,
                        "status": "completed",
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Update progress
                    db_manager.update_workflow(workflow_id, {
                        "results": results,
                        "current_step": i,
                        "progress": f"{i+1}/{len(steps)}"
                    })
                    
                    logger.info(f"✅ Step {i+1} completed")
                    
                except Exception as step_error:
                    logger.error(f"❌ Step {i+1} failed: {step_error}")
                    
                    results.append({
                        "step": i,
                        "type": step.get("type"),
                        "error": str(step_error),
                        "status": "failed",
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    # Mark workflow as failed and exit
                    db_manager.update_workflow(workflow_id, {
                        "status": "failed",
                        "error": f"Step {i+1} failed: {str(step_error)}",
                        "results": results,
                        "finished_at": datetime.now()
                    })
                    
                    self.active_workflows[workflow_id]["status"] = "failed"
                    return
            
            # Mark as completed
            db_manager.update_workflow(workflow_id, {
                "status": "completed",
                "finished_at": datetime.now(),
                "results": results
            })
            
            self.active_workflows[workflow_id]["status"] = "completed"
            logger.info(f"🎉 Workflow {workflow_id} completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Workflow {workflow_id} execution failed: {e}")
            
            # Mark as failed
            db_manager.update_workflow(workflow_id, {
                "status": "failed",
                "error": str(e),
                "finished_at": datetime.now()
            })
            
            self.active_workflows[workflow_id]["status"] = "failed"
        
        finally:
            # Clean up from active workflows after completion
            asyncio.create_task(self._cleanup_workflow(workflow_id))
    
    async def _execute_workflow_step(self, step: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Execute a single workflow step"""
        step_type = step.get("type", "unknown")
        
        if step_type == "open":
            return await browser_service.execute_command(
                command="open",
                url=step.get("url"),
                session_id=session_id
            )
            
        elif step_type == "click":
            return await browser_service.execute_command(
                command="click",
                selector=step.get("selector"),
                session_id=session_id
            )
            
        elif step_type == "type":
            return await browser_service.execute_command(
                command="type",
                selector=step.get("selector"),
                text=step.get("text"),
                session_id=session_id
            )
            
        elif step_type == "wait" or step_type == "wait_for":
            timeout_ms = step.get("timeout_ms", 1000)
            await asyncio.sleep(timeout_ms / 1000)
            return {
                "action": "waited",
                "duration_ms": timeout_ms,
                "message": f"Waited for {timeout_ms}ms"
            }
            
        elif step_type == "screenshot":
            return await browser_service.execute_command(
                command="screenshot",
                session_id=session_id
            )
            
        elif step_type == "extract":
            return {
                "action": "extract",
                "selector": step.get("selector"),
                "message": f"Extracting data from {step.get('selector', 'page')}"
            }
            
        else:
            logger.warning(f"⚠️ Unknown workflow step type: {step_type}")
            return {
                "action": "unknown",
                "type": step_type,
                "message": f"Unknown step type: {step_type}"
            }
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow execution status"""
        try:
            # Check in-memory first
            if workflow_id in self.active_workflows:
                memory_status = self.active_workflows[workflow_id]
                
            # Get from database
            workflow = db_manager.get_workflow(workflow_id)
            if not workflow:
                logger.warning(f"⚠️ Workflow not found: {workflow_id}")
                return None
            
            # Combine memory and database info
            if workflow_id in self.active_workflows:
                workflow["memory_status"] = self.active_workflows[workflow_id]["status"]
            
            logger.info(f"📊 Retrieved workflow status: {workflow_id}")
            return workflow
            
        except Exception as e:
            logger.error(f"❌ Failed to get workflow status: {e}")
            return None
    
    async def _cleanup_workflow(self, workflow_id: str):
        """Clean up completed workflow from memory after delay"""
        await asyncio.sleep(300)  # Keep in memory for 5 minutes after completion
        if workflow_id in self.active_workflows:
            del self.active_workflows[workflow_id]
            logger.info(f"🧹 Cleaned up workflow from memory: {workflow_id}")
    
    def get_active_workflows(self) -> Dict[str, Any]:
        """Get list of currently active workflows"""
        return {
            "active_workflows": self.active_workflows,
            "count": len(self.active_workflows)
        }
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel an active workflow"""
        try:
            if workflow_id in self.active_workflows:
                # Update database status
                db_manager.update_workflow(workflow_id, {
                    "status": "cancelled",
                    "cancelled_at": datetime.now()
                })
                
                # Update memory status
                self.active_workflows[workflow_id]["status"] = "cancelled"
                
                logger.info(f"⏹️ Workflow cancelled: {workflow_id}")
                return True
            else:
                logger.warning(f"⚠️ Cannot cancel - workflow not active: {workflow_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to cancel workflow: {e}")
            return False

# Global workflow service instance
workflow_service = WorkflowService()