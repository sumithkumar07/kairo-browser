"""
Proactive Intelligence Service - Context-Aware AI Suggestions
Provides intelligent suggestions based on browsing context and patterns
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json
from services.ai_service import ai_service
from services.memory_service import memory_service
from database.mongodb import db_manager

logger = logging.getLogger(__name__)

class ProactiveIntelligenceService:
    """Proactive intelligence engine for context-aware suggestions"""
    
    def __init__(self):
        self.context_analyzers = {
            'content': self._analyze_page_content,
            'behavior': self._analyze_user_behavior,
            'temporal': self._analyze_temporal_patterns,
            'workflow': self._analyze_workflow_patterns
        }
        self.suggestion_generators = {
            'navigation': self._generate_navigation_suggestions,
            'automation': self._generate_automation_suggestions,
            'research': self._generate_research_suggestions,
            'productivity': self._generate_productivity_suggestions
        }
        logger.info("🧠 Proactive Intelligence Service initialized")
    
    async def analyze_context_and_suggest(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current context and provide proactive suggestions"""
        try:
            # Gather context data
            full_context = await self._gather_full_context(user_id, context)
            
            # Analyze context from multiple angles
            context_analysis = await self._perform_context_analysis(full_context)
            
            # Generate suggestions based on analysis
            suggestions = await self._generate_contextual_suggestions(user_id, context_analysis)
            
            # Rank and filter suggestions
            ranked_suggestions = await self._rank_suggestions(suggestions, context_analysis)
            
            # Store analysis for learning
            await self._store_intelligence_session(user_id, full_context, context_analysis, ranked_suggestions)
            
            return {
                'context_analysis': context_analysis,
                'suggestions': ranked_suggestions,
                'confidence': self._calculate_confidence(context_analysis, ranked_suggestions),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Intelligence analysis failed: {e}")
            return {'error': str(e)}
    
    async def _gather_full_context(self, user_id: str, current_context: Dict[str, Any]) -> Dict[str, Any]:
        """Gather comprehensive context information"""
        full_context = current_context.copy()
        
        # Add user preferences and history
        user_prefs = await memory_service.get_user_preferences(user_id)
        full_context['user_preferences'] = user_prefs
        
        # Add recent activity
        recent_activity = await db_manager.get_recent_activity(user_id, hours=24)
        full_context['recent_activity'] = recent_activity
        
        # Add current time context
        now = datetime.now()
        full_context['temporal_context'] = {
            'hour': now.hour,
            'day_of_week': now.weekday(),
            'is_weekend': now.weekday() >= 5,
            'is_work_hours': 9 <= now.hour <= 17
        }
        
        # Add browser context
        full_context['browser_context'] = {
            'active_tabs': current_context.get('totalTabs', 1),
            'is_fullscreen': current_context.get('isFullscreen', False),
            'bookmarks_count': current_context.get('bookmarks', 0)
        }
        
        return full_context
    
    async def _perform_context_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform multi-dimensional context analysis"""
        analysis_results = {}
        
        for analyzer_name, analyzer_func in self.context_analyzers.items():
            try:
                result = await analyzer_func(context)
                analysis_results[analyzer_name] = result
            except Exception as e:
                logger.error(f"❌ {analyzer_name} analysis failed: {e}")
                analysis_results[analyzer_name] = {'error': str(e)}
        
        return analysis_results
    
    async def _analyze_page_content(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current page content for context clues"""
        current_url = context.get('currentUrl', '')
        
        if not current_url:
            return {'type': 'no_page', 'confidence': 0}
        
        # Extract domain and analyze URL patterns
        from urllib.parse import urlparse
        parsed_url = urlparse(current_url)
        domain = parsed_url.netloc.replace('www.', '')
        
        # Categorize website type
        website_categories = {
            'social': ['facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com'],
            'work': ['notion.so', 'slack.com', 'github.com', 'gmail.com'],
            'research': ['google.com', 'wikipedia.org', 'stackoverflow.com'],
            'entertainment': ['youtube.com', 'netflix.com', 'reddit.com'],
            'shopping': ['amazon.com', 'ebay.com', 'shopify.com'],
            'news': ['cnn.com', 'bbc.com', 'techcrunch.com']
        }
        
        category = 'unknown'
        for cat, domains in website_categories.items():
            if any(d in domain for d in domains):
                category = cat
                break
        
        return {
            'domain': domain,
            'category': category,
            'url_path': parsed_url.path,
            'confidence': 0.8 if category != 'unknown' else 0.4
        }
    
    async def _analyze_user_behavior(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze recent user behavior patterns"""
        recent_activity = context.get('recent_activity', [])
        
        if not recent_activity:
            return {'pattern': 'no_data', 'confidence': 0}
        
        # Analyze command patterns
        command_counts = {}
        domain_visits = {}
        
        for activity in recent_activity:
            command = activity.get('command', '')
            url = activity.get('url', '')
            
            if command:
                command_counts[command] = command_counts.get(command, 0) + 1
            
            if url:
                domain = self._extract_domain(url)
                domain_visits[domain] = domain_visits.get(domain, 0) + 1
        
        # Determine behavior pattern
        top_command = max(command_counts.items(), key=lambda x: x[1])[0] if command_counts else None
        top_domain = max(domain_visits.items(), key=lambda x: x[1])[0] if domain_visits else None
        
        return {
            'top_command': top_command,
            'top_domain': top_domain,
            'command_diversity': len(command_counts),
            'domain_diversity': len(domain_visits),
            'activity_level': len(recent_activity),
            'confidence': 0.7 if len(recent_activity) > 5 else 0.4
        }
    
    async def _analyze_temporal_patterns(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze temporal usage patterns"""
        temporal_context = context.get('temporal_context', {})
        hour = temporal_context.get('hour', 12)
        is_work_hours = temporal_context.get('is_work_hours', False)
        is_weekend = temporal_context.get('is_weekend', False)
        
        # Determine time-based activity pattern
        if is_work_hours and not is_weekend:
            pattern = 'work_time'
            suggested_activities = ['productivity', 'research', 'communication']
        elif 6 <= hour <= 9:
            pattern = 'morning'
            suggested_activities = ['news', 'planning', 'email']
        elif 18 <= hour <= 22:
            pattern = 'evening'
            suggested_activities = ['entertainment', 'social', 'learning']
        elif hour >= 22 or hour <= 6:
            pattern = 'late_night'
            suggested_activities = ['light_browsing', 'reading']
        else:
            pattern = 'general'
            suggested_activities = ['mixed']
        
        return {
            'pattern': pattern,
            'suggested_activities': suggested_activities,
            'hour': hour,
            'is_work_time': is_work_hours,
            'confidence': 0.6
        }
    
    async def _analyze_workflow_patterns(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow and task patterns"""
        browser_context = context.get('browser_context', {})
        active_tabs = browser_context.get('active_tabs', 1)
        
        # Analyze multitasking level
        if active_tabs > 10:
            multitasking_level = 'heavy'
        elif active_tabs > 5:
            multitasking_level = 'moderate'
        else:
            multitasking_level = 'light'
        
        return {
            'multitasking_level': multitasking_level,
            'active_tabs': active_tabs,
            'focus_level': 'low' if active_tabs > 8 else 'high',
            'suggested_workflow': self._suggest_workflow_optimization(active_tabs),
            'confidence': 0.5
        }
    
    async def _generate_contextual_suggestions(self, user_id: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate suggestions based on context analysis"""
        all_suggestions = []
        
        for generator_name, generator_func in self.suggestion_generators.items():
            try:
                suggestions = await generator_func(user_id, analysis)
                for suggestion in suggestions:
                    suggestion['generator'] = generator_name
                all_suggestions.extend(suggestions)
            except Exception as e:
                logger.error(f"❌ {generator_name} suggestion generation failed: {e}")
        
        return all_suggestions
    
    async def _generate_navigation_suggestions(self, user_id: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate navigation-related suggestions"""
        suggestions = []
        
        content_analysis = analysis.get('content', {})
        behavior_analysis = analysis.get('behavior', {})
        temporal_analysis = analysis.get('temporal', {})
        
        current_category = content_analysis.get('category', 'unknown')
        
        # Suggest related websites based on current context
        if current_category == 'work':
            suggestions.extend([
                {
                    'type': 'navigation',
                    'action': 'Open Gmail',
                    'reason': 'Check work emails',
                    'priority': 'high',
                    'confidence': 0.7
                },
                {
                    'type': 'navigation',
                    'action': 'Open Notion',
                    'reason': 'Access work notes',
                    'priority': 'medium',
                    'confidence': 0.6
                }
            ])
        elif current_category == 'research':
            suggestions.extend([
                {
                    'type': 'navigation',
                    'action': 'Search StackOverflow',
                    'reason': 'Find technical solutions',
                    'priority': 'high',
                    'confidence': 0.8
                },
                {
                    'type': 'navigation',
                    'action': 'Open GitHub',
                    'reason': 'Browse code repositories',
                    'priority': 'medium',
                    'confidence': 0.7
                }
            ])
        
        # Time-based suggestions
        pattern = temporal_analysis.get('pattern', 'general')
        if pattern == 'morning':
            suggestions.append({
                'type': 'navigation',
                'action': 'Check news',
                'reason': 'Morning news update',
                'priority': 'medium',
                'confidence': 0.6
            })
        elif pattern == 'evening':
            suggestions.append({
                'type': 'navigation',
                'action': 'Open YouTube',
                'reason': 'Evening entertainment',
                'priority': 'low',
                'confidence': 0.5
            })
        
        return suggestions
    
    async def _generate_automation_suggestions(self, user_id: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate automation-related suggestions"""
        suggestions = []
        
        behavior_analysis = analysis.get('behavior', {})
        workflow_analysis = analysis.get('workflow', {})
        
        top_command = behavior_analysis.get('top_command', '')
        multitasking_level = workflow_analysis.get('multitasking_level', 'light')
        
        # Suggest automation for repetitive tasks
        if top_command:
            suggestions.append({
                'type': 'automation',
                'action': f'Create workflow for "{top_command}"',
                'reason': 'Automate frequently used command',
                'priority': 'medium',
                'confidence': 0.7
            })
        
        # Suggest workflow optimization for heavy multitaskers
        if multitasking_level == 'heavy':
            suggestions.extend([
                {
                    'type': 'automation',
                    'action': 'Group similar tabs',
                    'reason': 'Reduce tab clutter',
                    'priority': 'high',
                    'confidence': 0.8
                },
                {
                    'type': 'automation',
                    'action': 'Save tab session',
                    'reason': 'Preserve current workflow',
                    'priority': 'medium',
                    'confidence': 0.6
                }
            ])
        
        return suggestions
    
    async def _generate_research_suggestions(self, user_id: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate research-related suggestions"""
        suggestions = []
        
        content_analysis = analysis.get('content', {})
        current_category = content_analysis.get('category', 'unknown')
        current_domain = content_analysis.get('domain', '')
        
        if current_category == 'research' or 'search' in current_domain:
            suggestions.extend([
                {
                    'type': 'research',
                    'action': 'Deep search current topic',
                    'reason': 'Comprehensive research across sources',
                    'priority': 'high',
                    'confidence': 0.8
                },
                {
                    'type': 'research',
                    'action': 'Generate research summary',
                    'reason': 'Summarize findings so far',
                    'priority': 'medium',
                    'confidence': 0.7
                }
            ])
        
        return suggestions
    
    async def _generate_productivity_suggestions(self, user_id: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate productivity-related suggestions"""
        suggestions = []
        
        temporal_analysis = analysis.get('temporal', {})
        workflow_analysis = analysis.get('workflow', {})
        
        is_work_time = temporal_analysis.get('is_work_time', False)
        focus_level = workflow_analysis.get('focus_level', 'high')
        
        if is_work_time and focus_level == 'low':
            suggestions.extend([
                {
                    'type': 'productivity',
                    'action': 'Take a break',
                    'reason': 'Improve focus and productivity',
                    'priority': 'medium',
                    'confidence': 0.6
                },
                {
                    'type': 'productivity',
                    'action': 'Close unused tabs',
                    'reason': 'Reduce distractions',
                    'priority': 'high',
                    'confidence': 0.8
                }
            ])
        
        return suggestions
    
    async def _rank_suggestions(self, suggestions: List[Dict[str, Any]], analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank suggestions by relevance and confidence"""
        # Calculate combined scores
        for suggestion in suggestions:
            priority_score = {'high': 1.0, 'medium': 0.7, 'low': 0.4}.get(suggestion.get('priority', 'low'), 0.4)
            confidence_score = suggestion.get('confidence', 0.5)
            
            # Boost score based on context relevance
            context_boost = 0
            suggestion_type = suggestion.get('type', '')
            
            if suggestion_type == 'navigation' and analysis.get('content', {}).get('confidence', 0) > 0.7:
                context_boost += 0.2
            elif suggestion_type == 'automation' and analysis.get('behavior', {}).get('activity_level', 0) > 10:
                context_boost += 0.3
            
            suggestion['combined_score'] = (priority_score + confidence_score + context_boost) / 2
        
        # Sort by combined score
        ranked = sorted(suggestions, key=lambda x: x.get('combined_score', 0), reverse=True)
        
        # Return top 5 suggestions
        return ranked[:5]
    
    def _calculate_confidence(self, analysis: Dict[str, Any], suggestions: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence in suggestions"""
        if not suggestions:
            return 0.0
        
        # Average confidence of analysis components
        analysis_confidences = []
        for component in analysis.values():
            if isinstance(component, dict) and 'confidence' in component:
                analysis_confidences.append(component['confidence'])
        
        analysis_confidence = sum(analysis_confidences) / len(analysis_confidences) if analysis_confidences else 0.5
        
        # Average confidence of suggestions
        suggestion_confidences = [s.get('confidence', 0.5) for s in suggestions]
        suggestion_confidence = sum(suggestion_confidences) / len(suggestion_confidences)
        
        # Combined confidence
        return (analysis_confidence + suggestion_confidence) / 2
    
    async def _store_intelligence_session(self, user_id: str, context: Dict[str, Any], analysis: Dict[str, Any], suggestions: List[Dict[str, Any]]):
        """Store intelligence session for learning"""
        try:
            session_data = {
                'user_id': user_id,
                'context': context,
                'analysis': analysis,
                'suggestions': suggestions,
                'timestamp': datetime.now()
            }
            
            await db_manager.store_intelligence_session(session_data)
            
        except Exception as e:
            logger.error(f"❌ Failed to store intelligence session: {e}")
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc.replace('www.', '')
        except:
            return url
    
    def _suggest_workflow_optimization(self, active_tabs: int) -> str:
        """Suggest workflow optimization based on tab count"""
        if active_tabs > 15:
            return 'heavy_cleanup'
        elif active_tabs > 8:
            return 'organize_tabs'
        elif active_tabs > 3:
            return 'group_similar'
        else:
            return 'maintain_focus'

# Global intelligence service instance
intelligence_service = ProactiveIntelligenceService()