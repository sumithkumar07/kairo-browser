"""
Advanced Memory Service - Agentic Memory System
Learns from user behavior and personalizes interactions
"""
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict
import numpy as np
from database.mongodb import db_manager

logger = logging.getLogger(__name__)

class AgenticMemoryService:
    """Advanced memory system that learns from user behavior"""
    
    def __init__(self):
        self.interaction_patterns = defaultdict(list)
        self.user_preferences = {}
        self.command_frequency = defaultdict(int)
        self.context_associations = defaultdict(list)
        logger.info("🧠 Agentic Memory Service initialized")
    
    async def learn_from_interaction(self, user_id: str, interaction_data: Dict[str, Any]):
        """Learn from user interaction and update memory"""
        try:
            # Extract learning signals
            command = interaction_data.get('command', '')
            context = interaction_data.get('context', {})
            outcome = interaction_data.get('outcome', 'success')
            timestamp = datetime.now()
            
            # Store interaction pattern
            pattern = {
                'command': command,
                'context': context,
                'outcome': outcome,
                'timestamp': timestamp,
                'day_of_week': timestamp.weekday(),
                'hour': timestamp.hour
            }
            
            # Update memory collections
            await self._update_command_patterns(user_id, pattern)
            await self._update_context_associations(user_id, command, context)
            await self._update_temporal_patterns(user_id, pattern)
            
            # Update frequency tracking
            self.command_frequency[f"{user_id}:{command}"] += 1
            
            logger.info(f"🎯 Learned from interaction: {command}")
            
        except Exception as e:
            logger.error(f"❌ Memory learning failed: {e}")
    
    async def get_personalized_suggestions(self, user_id: str, current_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized suggestions based on memory"""
        try:
            suggestions = []
            
            # Context-based suggestions
            context_suggestions = await self._get_context_suggestions(user_id, current_context)
            suggestions.extend(context_suggestions)
            
            # Temporal suggestions (based on time patterns)
            temporal_suggestions = await self._get_temporal_suggestions(user_id)
            suggestions.extend(temporal_suggestions)
            
            # Frequency-based suggestions
            frequency_suggestions = await self._get_frequency_suggestions(user_id)
            suggestions.extend(frequency_suggestions)
            
            # Remove duplicates and rank
            suggestions = self._rank_suggestions(suggestions)
            
            logger.info(f"🎯 Generated {len(suggestions)} personalized suggestions")
            return suggestions[:5]  # Return top 5
            
        except Exception as e:
            logger.error(f"❌ Suggestion generation failed: {e}")
            return []
    
    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get learned user preferences"""
        try:
            preferences = await db_manager.get_user_preferences(user_id)
            return preferences or {
                'preferred_search_engines': ['google'],
                'common_websites': [],
                'automation_preferences': {},
                'ui_preferences': {},
                'work_patterns': {}
            }
        except Exception as e:
            logger.error(f"❌ Failed to get preferences: {e}")
            return {}
    
    async def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]):
        """Update user preferences"""
        try:
            await db_manager.update_user_preferences(user_id, preferences)
            logger.info(f"✅ Updated preferences for user {user_id}")
        except Exception as e:
            logger.error(f"❌ Failed to update preferences: {e}")
    
    async def _update_command_patterns(self, user_id: str, pattern: Dict[str, Any]):
        """Update command usage patterns"""
        await db_manager.store_interaction_pattern(user_id, pattern)
    
    async def _update_context_associations(self, user_id: str, command: str, context: Dict[str, Any]):
        """Learn associations between commands and contexts"""
        current_url = context.get('currentUrl', '')
        if current_url:
            association = {
                'command': command,
                'url': current_url,
                'domain': self._extract_domain(current_url),
                'timestamp': datetime.now()
            }
            await db_manager.store_context_association(user_id, association)
    
    async def _update_temporal_patterns(self, user_id: str, pattern: Dict[str, Any]):
        """Learn temporal usage patterns"""
        temporal_key = f"{pattern['day_of_week']}:{pattern['hour']}"
        await db_manager.update_temporal_pattern(user_id, temporal_key, pattern['command'])
    
    async def _get_context_suggestions(self, user_id: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get suggestions based on current context"""
        suggestions = []
        current_url = context.get('currentUrl', '')
        
        if current_url:
            domain = self._extract_domain(current_url)
            # Get commands commonly used on this domain
            domain_commands = await db_manager.get_domain_commands(user_id, domain)
            
            for cmd in domain_commands:
                suggestions.append({
                    'command': cmd,
                    'type': 'context',
                    'confidence': 0.8,
                    'reason': f'Often used on {domain}'
                })
        
        return suggestions
    
    async def _get_temporal_suggestions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get suggestions based on temporal patterns"""
        now = datetime.now()
        temporal_key = f"{now.weekday()}:{now.hour}"
        
        temporal_commands = await db_manager.get_temporal_commands(user_id, temporal_key)
        
        suggestions = []
        for cmd in temporal_commands:
            suggestions.append({
                'command': cmd,
                'type': 'temporal',
                'confidence': 0.7,
                'reason': f'Usually done around this time'
            })
        
        return suggestions
    
    async def _get_frequency_suggestions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get suggestions based on command frequency"""
        # Get most frequent commands for user
        user_commands = {k: v for k, v in self.command_frequency.items() 
                        if k.startswith(f"{user_id}:")}
        
        # Sort by frequency
        sorted_commands = sorted(user_commands.items(), key=lambda x: x[1], reverse=True)
        
        suggestions = []
        for cmd_key, freq in sorted_commands[:3]:
            command = cmd_key.split(':', 1)[1]
            suggestions.append({
                'command': command,
                'type': 'frequent',
                'confidence': 0.6,
                'reason': f'Used {freq} times'
            })
        
        return suggestions
    
    def _rank_suggestions(self, suggestions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank suggestions by confidence and remove duplicates"""
        unique_suggestions = {}
        
        for suggestion in suggestions:
            cmd = suggestion['command']
            if cmd not in unique_suggestions or suggestion['confidence'] > unique_suggestions[cmd]['confidence']:
                unique_suggestions[cmd] = suggestion
        
        # Sort by confidence
        ranked = sorted(unique_suggestions.values(), key=lambda x: x['confidence'], reverse=True)
        return ranked
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.replace('www.', '')
        except:
            return url

# Global memory service instance
memory_service = AgenticMemoryService()