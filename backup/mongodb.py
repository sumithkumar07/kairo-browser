"""
MongoDB database operations
"""
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import settings

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database manager"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self._connect()
    
    def _connect(self):
        """Establish database connection"""
        try:
            self.client = MongoClient(
                settings.MONGO_URL,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            # Test connection
            self.client.server_info()
            self.db = self.client.kairo_browser
            logger.info("✅ MongoDB connected successfully")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            raise
    
    def health_check(self) -> Dict[str, str]:
        """Check database health"""
        try:
            self.client.server_info()
            return {"mongodb": "healthy"}
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {"mongodb": "unhealthy"}
    
    def store_ai_interaction(self, session_id: str, query: str, response: Dict[str, Any], context: Optional[Dict] = None) -> str:
        """Store AI interaction"""
        try:
            interaction = {
                "session_id": session_id,
                "query": query,
                "response": response,
                "context": context or {},
                "timestamp": datetime.now(),
                "type": "ai_interaction"
            }
            result = self.db.ai_interactions.insert_one(interaction)
            logger.info(f"✅ AI interaction stored: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"❌ Failed to store AI interaction: {e}")
            raise
    
    def store_browser_command(self, session_id: str, command: Dict[str, Any], result: Dict[str, Any]) -> str:
        """Store browser command execution"""
        try:
            command_record = {
                "session_id": session_id,
                "command": command,
                "result": result,
                "timestamp": datetime.now(),
                "type": "browser_command"
            }
            result = self.db.browser_commands.insert_one(command_record)
            logger.info(f"✅ Browser command stored: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"❌ Failed to store browser command: {e}")
            raise
    
    def store_workflow(self, workflow_data: Dict[str, Any]) -> str:
        """Store workflow execution"""
        try:
            workflow_data["created_at"] = datetime.now()
            result = self.db.workflows.insert_one(workflow_data)
            logger.info(f"✅ Workflow stored: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"❌ Failed to store workflow: {e}")
            raise
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve workflow by ID"""
        try:
            workflow = self.db.workflows.find_one({"id": workflow_id})
            if workflow:
                workflow.pop("_id", None)  # Remove MongoDB ObjectId
            return workflow
        except Exception as e:
            logger.error(f"❌ Failed to retrieve workflow: {e}")
            return None
    
    def update_workflow(self, workflow_id: str, update_data: Dict[str, Any]) -> bool:
        """Update workflow status/results"""
        try:
            result = self.db.workflows.update_one(
                {"id": workflow_id},
                {"$set": {**update_data, "updated_at": datetime.now()}}
            )
            success = result.modified_count > 0
            if success:
                logger.info(f"✅ Workflow updated: {workflow_id}")
            return success
        except Exception as e:
            logger.error(f"❌ Failed to update workflow: {e}")
            return False
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get list of active browser sessions"""
        try:
            sessions = list(self.db.browser_commands.aggregate([
                {"$group": {
                    "_id": "$session_id", 
                    "last_activity": {"$max": "$timestamp"}, 
                    "command_count": {"$sum": 1}
                }},
                {"$sort": {"last_activity": -1}},
                {"$limit": 10}
            ]))
            logger.info(f"✅ Retrieved {len(sessions)} active sessions")
            return sessions
        except Exception as e:
            logger.error(f"❌ Failed to retrieve sessions: {e}")
            return []

# Global database instance
db_manager = Database()