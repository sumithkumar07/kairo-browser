"""
Browser service for command execution and session management
"""
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from database.mongodb import db_manager

logger = logging.getLogger(__name__)

class BrowserService:
    """Browser command execution and session management"""
    
    def __init__(self):
        self.active_sessions = {}
        logger.info("✅ Browser service initialized")
    
    async def execute_command(self, command: str, url: Optional[str] = None, 
                            selector: Optional[str] = None, text: Optional[str] = None, 
                            session_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute a browser command"""
        try:
            session_id = session_id or str(uuid.uuid4())
            
            logger.info(f"🎮 Executing command: {command} for session {session_id}")
            
            result = {
                "session_id": session_id,
                "command": command,
                "status": "executed",
                "timestamp": datetime.now().isoformat()
            }
            
            # Process different command types
            if command == "open":
                result.update(await self._handle_open_command(url, session_id))
            elif command == "click":
                result.update(await self._handle_click_command(selector, session_id))
            elif command == "type":
                result.update(await self._handle_type_command(selector, text, session_id))
            elif command == "scroll":
                result.update(await self._handle_scroll_command(session_id))
            elif command == "screenshot":
                result.update(await self._handle_screenshot_command(session_id))
            elif command == "navigate":
                result.update(await self._handle_navigate_command(url, session_id))
            else:
                result["status"] = "unknown_command"
                result["error"] = f"Unknown command: {command}"
                logger.warning(f"⚠️ Unknown command: {command}")
            
            # Store command execution
            command_data = {
                "command": command,
                "url": url,
                "selector": selector,
                "text": text,
                "session_id": session_id
            }
            
            db_manager.store_browser_command(session_id, command_data, result)
            
            logger.info(f"✅ Command executed successfully: {command}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Command execution failed: {e}")
            error_result = {
                "session_id": session_id or "unknown",
                "command": command,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            return error_result
    
    async def _handle_open_command(self, url: str, session_id: str) -> Dict[str, Any]:
        """Handle open/navigation command"""
        if not url:
            raise ValueError("URL required for open command")
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Update session state
        self.active_sessions[session_id] = {
            "current_url": url,
            "last_activity": datetime.now(),
            "commands": self.active_sessions.get(session_id, {}).get("commands", 0) + 1
        }
        
        return {
            "data": {
                "url": url,
                "action": "navigate"
            },
            "message": f"Navigating to {url}"
        }
    
    async def _handle_click_command(self, selector: str, session_id: str) -> Dict[str, Any]:
        """Handle click command"""
        if not selector:
            raise ValueError("Selector required for click command")
        
        return {
            "data": {
                "selector": selector,
                "action": "click"
            },
            "message": f"Clicking element: {selector}"
        }
    
    async def _handle_type_command(self, selector: str, text: str, session_id: str) -> Dict[str, Any]:
        """Handle type command"""
        if not selector or not text:
            raise ValueError("Selector and text required for type command")
        
        return {
            "data": {
                "selector": selector,
                "text": text,
                "action": "type"
            },
            "message": f"Typing '{text}' into {selector}"
        }
    
    async def _handle_scroll_command(self, session_id: str) -> Dict[str, Any]:
        """Handle scroll command"""
        return {
            "data": {
                "action": "scroll"
            },
            "message": "Scrolling page"
        }
    
    async def _handle_screenshot_command(self, session_id: str) -> Dict[str, Any]:
        """Handle screenshot command"""
        screenshot_name = f"screenshot_{session_id}_{datetime.now().isoformat()}.png"
        
        return {
            "data": {
                "action": "screenshot",
                "filename": screenshot_name
            },
            "message": f"Taking screenshot: {screenshot_name}"
        }
    
    async def _handle_navigate_command(self, url: str, session_id: str) -> Dict[str, Any]:
        """Handle navigate command (similar to open but with additional processing)"""
        if not url:
            raise ValueError("URL required for navigate command")
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Update session state
        self.active_sessions[session_id] = {
            "current_url": url,
            "last_activity": datetime.now(),
            "commands": self.active_sessions.get(session_id, {}).get("commands", 0) + 1
        }
        
        return {
            "data": {
                "url": url,
                "action": "navigate"
            },
            "message": f"Navigating to {url}",
            "requires_proxy": True  # Signal that proxy loading is needed
        }
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information"""
        return self.active_sessions.get(session_id)
    
    def get_active_sessions(self) -> Dict[str, Any]:
        """Get all active sessions"""
        try:
            # Get sessions from database
            db_sessions = db_manager.get_active_sessions()
            
            # Combine with in-memory sessions
            all_sessions = {
                "memory_sessions": list(self.active_sessions.keys()),
                "database_sessions": db_sessions,
                "total_active": len(self.active_sessions)
            }
            
            logger.info(f"📊 Retrieved {len(db_sessions)} database sessions, {len(self.active_sessions)} memory sessions")
            return all_sessions
            
        except Exception as e:
            logger.error(f"❌ Failed to get active sessions: {e}")
            return {"error": str(e)}
    
    def cleanup_inactive_sessions(self, max_age_hours: int = 24):
        """Cleanup old inactive sessions"""
        try:
            cutoff_time = datetime.now().timestamp() - (max_age_hours * 3600)
            sessions_to_remove = []
            
            for session_id, session_data in self.active_sessions.items():
                if session_data.get("last_activity", datetime.now()).timestamp() < cutoff_time:
                    sessions_to_remove.append(session_id)
            
            for session_id in sessions_to_remove:
                del self.active_sessions[session_id]
            
            if sessions_to_remove:
                logger.info(f"🧹 Cleaned up {len(sessions_to_remove)} inactive sessions")
            
        except Exception as e:
            logger.error(f"❌ Session cleanup failed: {e}")

# Global browser service instance
browser_service = BrowserService()