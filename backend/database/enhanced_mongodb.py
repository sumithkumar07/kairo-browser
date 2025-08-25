"""
Enhanced MongoDB Operations for All New Features
Database operations for memory, search, reports, agents, etc.
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import uuid
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

logger = logging.getLogger(__name__)

class EnhancedMongoDBManager:
    """Enhanced MongoDB manager with support for all new features"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collections = {
            # Original collections
            'ai_interactions': 'ai_interactions',
            'browser_commands': 'browser_commands', 
            'workflows': 'workflows',
            
            # Enhanced collections for new features
            'user_memories': 'user_memories',
            'interaction_patterns': 'interaction_patterns',
            'context_associations': 'context_associations',
            'temporal_patterns': 'temporal_patterns',
            'user_preferences': 'user_preferences',
            
            'search_sessions': 'search_sessions',
            'intelligence_sessions': 'intelligence_sessions',
            
            'reports': 'reports',
            'accessibility_sessions': 'accessibility_sessions',
            
            'agents': 'agents',
            'agent_executions': 'agent_executions',
            
            'workspaces': 'workspaces',
            'timeline_events': 'timeline_events',
            'user_analytics': 'user_analytics'
        }
        
    def connect(self):
        """Connect to MongoDB with enhanced collections"""
        try:
            mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/kairo_browser')
            self.client = MongoClient(mongo_url)
            
            # Extract database name from URL
            db_name = mongo_url.split('/')[-1] if '/' in mongo_url else 'kairo_browser'
            self.db = self.client[db_name]
            
            # Test connection
            self.client.admin.command('ping')
            
            # Create indexes for new collections
            self._create_enhanced_indexes()
            
            logger.info(f"✅ Enhanced MongoDB connected: {db_name}")
            return True
            
        except ConnectionFailure as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            return False
    
    def _create_enhanced_indexes(self):
        """Create indexes for enhanced collections"""
        try:
            # User memories indexes
            self.db[self.collections['user_memories']].create_index([('user_id', 1), ('timestamp', -1)])
            
            # Search sessions indexes
            self.db[self.collections['search_sessions']].create_index([('search_id', 1)])
            self.db[self.collections['search_sessions']].create_index([('timestamp', -1)])
            
            # Agent indexes
            self.db[self.collections['agents']].create_index([('user_id', 1), ('created_at', -1)])
            self.db[self.collections['agents']].create_index([('name', 'text')])
            
            # Timeline indexes
            self.db[self.collections['timeline_events']].create_index([('user_id', 1), ('timestamp', -1)])
            self.db[self.collections['timeline_events']].create_index([('user_id', 1), ('type', 1)])
            
            # Workspace indexes
            self.db[self.collections['workspaces']].create_index([('user_id', 1)])
            
            logger.info("✅ Enhanced MongoDB indexes created")
            
        except Exception as e:
            logger.error(f"❌ Index creation failed: {e}")
    
    # ============================================================================
    # MEMORY SERVICE DATABASE OPERATIONS
    # ============================================================================
    
    async def store_interaction_pattern(self, user_id: str, pattern: Dict[str, Any]):
        """Store user interaction pattern"""
        try:
            pattern_data = {
                'user_id': user_id,
                'pattern': pattern,
                'stored_at': datetime.now()
            }
            
            result = self.db[self.collections['interaction_patterns']].insert_one(pattern_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to store interaction pattern: {e}")
            return None
    
    async def store_context_association(self, user_id: str, association: Dict[str, Any]):
        """Store context association"""
        try:
            association_data = {
                'user_id': user_id,
                'association': association,
                'stored_at': datetime.now()
            }
            
            result = self.db[self.collections['context_associations']].insert_one(association_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to store context association: {e}")
            return None
    
    async def update_temporal_pattern(self, user_id: str, temporal_key: str, command: str):
        """Update temporal usage patterns"""
        try:
            filter_query = {'user_id': user_id, 'temporal_key': temporal_key}
            update_query = {
                '$inc': {f'commands.{command}': 1},
                '$set': {'last_updated': datetime.now()}
            }
            
            self.db[self.collections['temporal_patterns']].update_one(
                filter_query, 
                update_query, 
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to update temporal pattern: {e}")
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences"""
        try:
            prefs = self.db[self.collections['user_preferences']].find_one({'user_id': user_id})
            return prefs.get('preferences', {}) if prefs else {}
            
        except Exception as e:
            logger.error(f"❌ Failed to get user preferences: {e}")
            return {}
    
    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences"""
        try:
            filter_query = {'user_id': user_id}
            update_query = {
                '$set': {
                    'preferences': preferences,
                    'updated_at': datetime.now()
                }
            }
            
            self.db[self.collections['user_preferences']].update_one(
                filter_query,
                update_query,
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to update user preferences: {e}")
    
    async def get_domain_commands(self, user_id: str, domain: str) -> List[str]:
        """Get commands commonly used on domain"""
        try:
            pipeline = [
                {'$match': {'user_id': user_id, 'association.domain': domain}},
                {'$group': {'_id': '$association.command', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 5}
            ]
            
            results = list(self.db[self.collections['context_associations']].aggregate(pipeline))
            return [result['_id'] for result in results]
            
        except Exception as e:
            logger.error(f"❌ Failed to get domain commands: {e}")
            return []
    
    async def get_temporal_commands(self, user_id: str, temporal_key: str) -> List[str]:
        """Get commands used at specific times"""
        try:
            pattern = self.db[self.collections['temporal_patterns']].find_one({
                'user_id': user_id,
                'temporal_key': temporal_key
            })
            
            if pattern and 'commands' in pattern:
                # Sort by frequency
                sorted_commands = sorted(
                    pattern['commands'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )
                return [cmd[0] for cmd in sorted_commands[:3]]
            
            return []
            
        except Exception as e:
            logger.error(f"❌ Failed to get temporal commands: {e}")
            return []
    
    # ============================================================================
    # SEARCH & INTELLIGENCE DATABASE OPERATIONS
    # ============================================================================
    
    async def store_search_session(self, session_data: Dict[str, Any]):
        """Store search session"""
        try:
            result = self.db[self.collections['search_sessions']].insert_one(session_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to store search session: {e}")
            return None
    
    async def store_intelligence_session(self, session_data: Dict[str, Any]):
        """Store intelligence analysis session"""
        try:
            result = self.db[self.collections['intelligence_sessions']].insert_one(session_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to store intelligence session: {e}")
            return None
    
    async def get_recent_activity(self, user_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent user activity"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Get from multiple collections
            activity = []
            
            # Browser commands
            commands = list(self.db[self.collections['browser_commands']].find({
                'session_id': {'$regex': f'^{user_id}'},
                'timestamp': {'$gte': cutoff_time}
            }).sort('timestamp', -1).limit(50))
            
            # AI interactions
            ai_interactions = list(self.db[self.collections['ai_interactions']].find({
                'session_id': {'$regex': f'^{user_id}'},
                'timestamp': {'$gte': cutoff_time}
            }).sort('timestamp', -1).limit(50))
            
            activity.extend(commands)
            activity.extend(ai_interactions)
            
            # Sort by timestamp
            activity.sort(key=lambda x: x.get('timestamp', datetime.now()), reverse=True)
            
            return activity[:50]  # Return most recent 50
            
        except Exception as e:
            logger.error(f"❌ Failed to get recent activity: {e}")
            return []
    
    # ============================================================================
    # REPORT DATABASE OPERATIONS
    # ============================================================================
    
    async def store_report(self, report: Dict[str, Any]):
        """Store generated report"""
        try:
            result = self.db[self.collections['reports']].insert_one(report)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to store report: {e}")
            return None
    
    async def get_activity_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get activity data for reports"""
        try:
            # Combine data from various collections
            data = []
            
            # Browser commands
            commands = list(self.db[self.collections['browser_commands']].find({
                'timestamp': {'$gte': start_date, '$lte': end_date}
            }))
            
            # AI interactions  
            interactions = list(self.db[self.collections['ai_interactions']].find({
                'timestamp': {'$gte': start_date, '$lte': end_date}
            }))
            
            data.extend(commands)
            data.extend(interactions)
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Failed to get activity data: {e}")
            return []
    
    async def get_search_sessions(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get search sessions for reports"""
        try:
            sessions = list(self.db[self.collections['search_sessions']].find({
                'timestamp': {'$gte': start_date, '$lte': end_date}
            }))
            return sessions
            
        except Exception as e:
            logger.error(f"❌ Failed to get search sessions: {e}")
            return []
    
    async def get_workflow_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get workflow data for reports"""
        try:
            workflows = list(self.db[self.collections['workflows']].find({
                'created_at': {'$gte': start_date, '$lte': end_date}
            }))
            return workflows
            
        except Exception as e:
            logger.error(f"❌ Failed to get workflow data: {e}")
            return []
    
    async def get_browser_sessions(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Get browser sessions for reports"""
        try:
            # Aggregate browser commands by session
            pipeline = [
                {'$match': {'timestamp': {'$gte': start_date, '$lte': end_date}}},
                {'$group': {
                    '_id': '$session_id',
                    'command_count': {'$sum': 1},
                    'first_activity': {'$min': '$timestamp'},
                    'last_activity': {'$max': '$timestamp'}
                }}
            ]
            
            sessions = list(self.db[self.collections['browser_commands']].aggregate(pipeline))
            return sessions
            
        except Exception as e:
            logger.error(f"❌ Failed to get browser sessions: {e}")
            return []
    
    # ============================================================================
    # ACCESSIBILITY DATABASE OPERATIONS
    # ============================================================================
    
    async def store_accessibility_session(self, session_data: Dict[str, Any]):
        """Store accessibility session"""
        try:
            result = self.db[self.collections['accessibility_sessions']].insert_one(session_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to store accessibility session: {e}")
            return None
    
    # ============================================================================
    # AGENT BUILDER DATABASE OPERATIONS
    # ============================================================================
    
    async def store_agent(self, agent: Dict[str, Any]):
        """Store custom agent"""
        try:
            result = self.db[self.collections['agents']].insert_one(agent)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to store agent: {e}")
            return None
    
    async def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        try:
            agent = self.db[self.collections['agents']].find_one({'id': agent_id})
            return agent
            
        except Exception as e:
            logger.error(f"❌ Failed to get agent: {e}")
            return None
    
    async def get_user_agents(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all agents created by user"""
        try:
            agents = list(self.db[self.collections['agents']].find({
                'user_id': user_id
            }).sort('created_at', -1))
            
            return agents
            
        except Exception as e:
            logger.error(f"❌ Failed to get user agents: {e}")
            return []
    
    async def get_public_agents(self) -> List[Dict[str, Any]]:
        """Get public/shared agents"""
        try:
            agents = list(self.db[self.collections['agents']].find({
                'public': True
            }).sort('created_at', -1))
            
            return agents
            
        except Exception as e:
            logger.error(f"❌ Failed to get public agents: {e}")
            return []
    
    async def update_agent_stats(self, agent_id: str, stats: Dict[str, Any]):
        """Update agent execution statistics"""
        try:
            self.db[self.collections['agents']].update_one(
                {'id': agent_id},
                {'$set': stats}
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to update agent stats: {e}")
    
    async def store_agent_execution(self, execution_data: Dict[str, Any]):
        """Store agent execution result"""
        try:
            result = self.db[self.collections['agent_executions']].insert_one(execution_data)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"❌ Failed to store agent execution: {e}")
            return None
    
    # ============================================================================
    # WORKSPACE & TIMELINE DATABASE OPERATIONS
    # ============================================================================
    
    async def create_workspace(self, workspace_data: Dict[str, Any]) -> str:
        """Create new workspace"""
        try:
            workspace_data['id'] = str(uuid.uuid4())
            result = self.db[self.collections['workspaces']].insert_one(workspace_data)
            return workspace_data['id']
            
        except Exception as e:
            logger.error(f"❌ Failed to create workspace: {e}")
            return None
    
    async def get_user_workspaces(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user workspaces"""
        try:
            workspaces = list(self.db[self.collections['workspaces']].find({
                'user_id': user_id
            }).sort('created_at', -1))
            
            return workspaces
            
        except Exception as e:
            logger.error(f"❌ Failed to get user workspaces: {e}")
            return []
    
    async def store_timeline_event(self, event_data: Dict[str, Any]):
        """Store timeline event"""
        try:
            event_data['id'] = str(uuid.uuid4())
            result = self.db[self.collections['timeline_events']].insert_one(event_data)
            return event_data['id']
            
        except Exception as e:
            logger.error(f"❌ Failed to store timeline event: {e}")
            return None
    
    async def get_user_timeline(self, user_id: str, date_range: str, activity_type: str, workspace: str) -> List[Dict[str, Any]]:
        """Get user timeline data"""
        try:
            # Build query based on filters
            query = {'user_id': user_id}
            
            # Date range filter
            now = datetime.now()
            if date_range == 'today':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif date_range == 'week':
                start_date = now - timedelta(days=7)
            elif date_range == 'month':
                start_date = now - timedelta(days=30)
            else:  # all
                start_date = None
            
            if start_date:
                query['timestamp'] = {'$gte': start_date}
            
            # Activity type filter
            if activity_type != 'all':
                query['type'] = activity_type
            
            # Workspace filter
            if workspace != 'all':
                query['workspace'] = workspace
            
            events = list(self.db[self.collections['timeline_events']].find(query).sort('timestamp', -1).limit(100))
            
            return events
            
        except Exception as e:
            logger.error(f"❌ Failed to get user timeline: {e}")
            return []
    
    async def get_user_analytics(self, user_id: str, period: str) -> Dict[str, Any]:
        """Get user analytics data"""
        try:
            # Calculate time range
            now = datetime.now()
            if period == 'day':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - timedelta(days=7)
            elif period == 'month':
                start_date = now - timedelta(days=30)
            else:  # all
                start_date = now - timedelta(days=365)
            
            # Aggregate analytics from various sources
            analytics = {
                'period': period,
                'start_date': start_date.isoformat(),
                'end_date': now.isoformat(),
                'activity_summary': {},
                'productivity_metrics': {},
                'usage_patterns': {}
            }
            
            # Get activity counts
            activity_pipeline = [
                {'$match': {'user_id': user_id, 'timestamp': {'$gte': start_date}}},
                {'$group': {'_id': '$type', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            
            activity_counts = list(self.db[self.collections['timeline_events']].aggregate(activity_pipeline))
            analytics['activity_summary'] = {item['_id']: item['count'] for item in activity_counts}
            
            return analytics
            
        except Exception as e:
            logger.error(f"❌ Failed to get user analytics: {e}")
            return {}

# Create enhanced database manager instance
enhanced_db_manager = EnhancedMongoDBManager()

# Initialize connection
if enhanced_db_manager.connect():
    logger.info("✅ Enhanced database manager ready")
else:
    logger.error("❌ Enhanced database manager failed to initialize")