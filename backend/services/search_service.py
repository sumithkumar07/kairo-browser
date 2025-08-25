"""
Deep Search Service - Advanced Multi-Source Search System
Parallel intelligent searching across multiple platforms and sources
"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import json
from concurrent.futures import ThreadPoolExecutor
from services.shadow_browser_service import shadow_browser_service
from services.ai_service import ai_service
from database.mongodb import db_manager

logger = logging.getLogger(__name__)

class DeepSearchService:
    """Advanced search system with parallel processing and AI analysis"""
    
    def __init__(self):
        self.search_engines = {
            'google': self._google_search,
            'bing': self._bing_search,
            'duckduckgo': self._duckduckgo_search,
            'youtube': self._youtube_search,
            'reddit': self._reddit_search,
            'twitter': self._twitter_search,
            'github': self._github_search,
            'stackoverflow': self._stackoverflow_search
        }
        self.private_sources = {
            'notion': self._notion_search,
            'gmail': self._gmail_search,
            'gdrive': self._gdrive_search,
            'slack': self._slack_search
        }
        logger.info("🔍 Deep Search Service initialized")
    
    async def execute_deep_search(self, query: str, search_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute comprehensive deep search across multiple sources"""
        try:
            search_config = search_config or {}
            
            # Generate search session ID
            search_id = f"search_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Analyze query with AI to optimize search strategy
            query_analysis = await self._analyze_query(query)
            
            # Determine search sources based on query analysis
            sources = self._select_search_sources(query_analysis, search_config)
            
            # Execute parallel searches
            search_results = await self._execute_parallel_searches(query, sources, search_id)
            
            # Analyze and rank results with AI
            analyzed_results = await self._analyze_search_results(query, search_results, query_analysis)
            
            # Store search session
            await self._store_search_session(search_id, query, analyzed_results)
            
            logger.info(f"🎯 Deep search completed: {len(analyzed_results.get('results', []))} results")
            
            return {
                'search_id': search_id,
                'query': query,
                'query_analysis': query_analysis,
                'sources_searched': sources,
                'results': analyzed_results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Deep search failed: {e}")
            return {'error': str(e)}
    
    async def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Use AI to analyze search query and optimize strategy"""
        try:
            analysis_prompt = f"""
            Analyze this search query for optimal search strategy:
            Query: "{query}"
            
            Provide analysis in JSON format:
            {{
                "intent": "research/shopping/news/technical/personal/entertainment",
                "keywords": ["key", "words", "extracted"],
                "suggested_sources": ["google", "youtube", "reddit", etc],
                "search_depth": "shallow/medium/deep",
                "content_type": "text/images/videos/mixed",
                "time_sensitivity": "current/recent/historical/any",
                "complexity": "simple/moderate/complex"
            }}
            """
            
            response = ai_service.process_query(analysis_prompt, {})
            
            # Parse AI response
            analysis_text = response.get('explanation', '{}')
            try:
                analysis = json.loads(analysis_text)
            except:
                # Fallback analysis
                analysis = {
                    'intent': 'research',
                    'keywords': query.split(),
                    'suggested_sources': ['google', 'bing', 'duckduckgo'],
                    'search_depth': 'medium',
                    'content_type': 'mixed',
                    'time_sensitivity': 'any',
                    'complexity': 'moderate'
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Query analysis failed: {e}")
            return {
                'intent': 'research',
                'keywords': query.split(),
                'suggested_sources': ['google', 'bing'],
                'search_depth': 'medium',
                'content_type': 'text',
                'time_sensitivity': 'any',
                'complexity': 'simple'
            }
    
    def _select_search_sources(self, query_analysis: Dict[str, Any], config: Dict[str, Any]) -> List[str]:
        """Select optimal search sources based on query analysis"""
        suggested_sources = query_analysis.get('suggested_sources', ['google'])
        
        # Add sources based on intent
        intent = query_analysis.get('intent', 'research')
        
        if intent == 'technical':
            suggested_sources.extend(['stackoverflow', 'github'])
        elif intent == 'news':
            suggested_sources.extend(['reddit', 'twitter'])
        elif intent == 'entertainment':
            suggested_sources.extend(['youtube', 'reddit'])
        elif intent == 'research':
            suggested_sources.extend(['bing', 'duckduckgo'])
        
        # Remove duplicates and limit sources
        sources = list(set(suggested_sources))
        max_sources = config.get('max_sources', 5)
        
        return sources[:max_sources]
    
    async def _execute_parallel_searches(self, query: str, sources: List[str], search_id: str) -> Dict[str, Any]:
        """Execute searches across multiple sources in parallel"""
        tasks = []
        
        for source in sources:
            if source in self.search_engines:
                task = asyncio.create_task(
                    self._execute_single_search(source, query, search_id)
                )
                tasks.append((source, task))
        
        # Wait for all searches to complete
        results = {}
        completed_tasks = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
        
        for (source, _), result in zip(tasks, completed_tasks):
            if isinstance(result, Exception):
                results[source] = {'error': str(result)}
            else:
                results[source] = result
        
        return results
    
    async def _execute_single_search(self, source: str, query: str, search_id: str) -> Dict[str, Any]:
        """Execute search on a single source"""
        try:
            search_func = self.search_engines[source]
            result = await search_func(query)
            
            logger.info(f"✅ {source} search completed: {len(result.get('results', []))} results")
            return result
            
        except Exception as e:
            logger.error(f"❌ {source} search failed: {e}")
            return {'error': str(e)}
    
    async def _google_search(self, query: str) -> Dict[str, Any]:
        """Execute Google search using shadow browser"""
        task_config = {
            'type': 'web_scraping',
            'url': f'https://www.google.com/search?q={query}',
            'selectors': ['.g h3', '.g .VwiC3b', '.g cite']
        }
        
        task_id = await shadow_browser_service.execute_background_task(task_config)
        
        # Wait for completion (with timeout)
        for _ in range(30):  # 30 second timeout
            status = await shadow_browser_service.get_task_status(task_id)
            if status['status'] in ['completed', 'failed']:
                break
            await asyncio.sleep(1)
        
        if status['status'] == 'completed':
            extracted_data = status['result']['extracted_data']
            
            # Process Google results
            titles = extracted_data.get('.g h3', [])
            snippets = extracted_data.get('.g .VwiC3b', [])
            urls = extracted_data.get('.g cite', [])
            
            results = []
            for i in range(min(len(titles), len(snippets), len(urls))):
                results.append({
                    'title': titles[i],
                    'snippet': snippets[i],
                    'url': urls[i],
                    'source': 'google',
                    'relevance_score': 1.0 - (i * 0.1)  # Simple relevance scoring
                })
            
            return {
                'source': 'google',
                'query': query,
                'results': results,
                'total_results': len(results)
            }
        
        return {'source': 'google', 'error': 'Search timeout or failed'}
    
    async def _bing_search(self, query: str) -> Dict[str, Any]:
        """Execute Bing search"""
        task_config = {
            'type': 'web_scraping',
            'url': f'https://www.bing.com/search?q={query}',
            'selectors': ['.b_algo h2', '.b_algo .b_caption p', '.b_algo cite']
        }
        
        task_id = await shadow_browser_service.execute_background_task(task_config)
        
        # Wait for completion
        for _ in range(30):
            status = await shadow_browser_service.get_task_status(task_id)
            if status['status'] in ['completed', 'failed']:
                break
            await asyncio.sleep(1)
        
        if status['status'] == 'completed':
            extracted_data = status['result']['extracted_data']
            
            titles = extracted_data.get('.b_algo h2', [])
            snippets = extracted_data.get('.b_algo .b_caption p', [])
            urls = extracted_data.get('.b_algo cite', [])
            
            results = []
            for i in range(min(len(titles), len(snippets), len(urls))):
                results.append({
                    'title': titles[i],
                    'snippet': snippets[i],
                    'url': urls[i],
                    'source': 'bing',
                    'relevance_score': 1.0 - (i * 0.1)
                })
            
            return {
                'source': 'bing',
                'query': query,
                'results': results,
                'total_results': len(results)
            }
        
        return {'source': 'bing', 'error': 'Search timeout or failed'}
    
    async def _duckduckgo_search(self, query: str) -> Dict[str, Any]:
        """Execute DuckDuckGo search"""
        task_config = {
            'type': 'web_scraping',
            'url': f'https://duckduckgo.com/?q={query}',
            'selectors': ['.result__title', '.result__snippet', '.result__url']
        }
        
        task_id = await shadow_browser_service.execute_background_task(task_config)
        
        for _ in range(30):
            status = await shadow_browser_service.get_task_status(task_id)
            if status['status'] in ['completed', 'failed']:
                break
            await asyncio.sleep(1)
        
        if status['status'] == 'completed':
            extracted_data = status['result']['extracted_data']
            
            titles = extracted_data.get('.result__title', [])
            snippets = extracted_data.get('.result__snippet', [])
            urls = extracted_data.get('.result__url', [])
            
            results = []
            for i in range(min(len(titles), len(snippets), len(urls))):
                results.append({
                    'title': titles[i],
                    'snippet': snippets[i],
                    'url': urls[i],
                    'source': 'duckduckgo',
                    'relevance_score': 1.0 - (i * 0.1)
                })
            
            return {
                'source': 'duckduckgo',
                'query': query,
                'results': results,
                'total_results': len(results)
            }
        
        return {'source': 'duckduckgo', 'error': 'Search timeout or failed'}
    
    async def _youtube_search(self, query: str) -> Dict[str, Any]:
        """Execute YouTube search"""
        # Implementation for YouTube search
        return {'source': 'youtube', 'results': [], 'note': 'YouTube search implementation needed'}
    
    async def _reddit_search(self, query: str) -> Dict[str, Any]:
        """Execute Reddit search"""
        # Implementation for Reddit search
        return {'source': 'reddit', 'results': [], 'note': 'Reddit search implementation needed'}
    
    async def _twitter_search(self, query: str) -> Dict[str, Any]:
        """Execute Twitter search"""
        # Implementation for Twitter search
        return {'source': 'twitter', 'results': [], 'note': 'Twitter search implementation needed'}
    
    async def _github_search(self, query: str) -> Dict[str, Any]:
        """Execute GitHub search"""
        # Implementation for GitHub search
        return {'source': 'github', 'results': [], 'note': 'GitHub search implementation needed'}
    
    async def _stackoverflow_search(self, query: str) -> Dict[str, Any]:
        """Execute StackOverflow search"""
        # Implementation for StackOverflow search
        return {'source': 'stackoverflow', 'results': [], 'note': 'StackOverflow search implementation needed'}
    
    async def _notion_search(self, query: str) -> Dict[str, Any]:
        """Search private Notion workspace"""
        # Implementation for private Notion search
        return {'source': 'notion', 'results': [], 'note': 'Notion integration needed'}
    
    async def _gmail_search(self, query: str) -> Dict[str, Any]:
        """Search Gmail"""
        # Implementation for Gmail search
        return {'source': 'gmail', 'results': [], 'note': 'Gmail integration needed'}
    
    async def _gdrive_search(self, query: str) -> Dict[str, Any]:
        """Search Google Drive"""
        # Implementation for Google Drive search
        return {'source': 'gdrive', 'results': [], 'note': 'Google Drive integration needed'}
    
    async def _slack_search(self, query: str) -> Dict[str, Any]:
        """Search Slack workspace"""
        # Implementation for Slack search
        return {'source': 'slack', 'results': [], 'note': 'Slack integration needed'}
    
    async def _analyze_search_results(self, query: str, search_results: Dict[str, Any], query_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze and rank search results"""
        try:
            # Combine all results
            all_results = []
            
            for source, source_results in search_results.items():
                if isinstance(source_results, dict) and 'results' in source_results:
                    for result in source_results['results']:
                        result['search_source'] = source
                        all_results.append(result)
            
            # AI analysis of results
            analysis_prompt = f"""
            Analyze and rank these search results for query: "{query}"
            
            Query Intent: {query_analysis.get('intent', 'unknown')}
            
            Results: {json.dumps(all_results[:20], indent=2)}  # Limit for AI processing
            
            Please provide:
            1. Relevance ranking (1-10)
            2. Content quality assessment
            3. Duplicate detection
            4. Key insights summary
            5. Recommended follow-up searches
            
            Return JSON format with enhanced results.
            """
            
            ai_response = ai_service.process_query(analysis_prompt, {})
            
            # Process AI analysis and enhance results
            enhanced_results = {
                'total_sources': len(search_results),
                'total_results': len(all_results),
                'results': all_results,  # For now, return all results
                'ai_analysis': ai_response.get('explanation', ''),
                'search_quality': self._assess_search_quality(search_results),
                'recommended_actions': self._generate_recommended_actions(query_analysis, all_results)
            }
            
            return enhanced_results
            
        except Exception as e:
            logger.error(f"❌ Result analysis failed: {e}")
            # Return basic results without AI enhancement
            all_results = []
            for source, source_results in search_results.items():
                if isinstance(source_results, dict) and 'results' in source_results:
                    all_results.extend(source_results['results'])
            
            return {
                'total_sources': len(search_results),
                'total_results': len(all_results),
                'results': all_results,
                'ai_analysis': f'Analysis failed: {str(e)}',
                'search_quality': 'unknown',
                'recommended_actions': []
            }
    
    def _assess_search_quality(self, search_results: Dict[str, Any]) -> str:
        """Assess overall search quality"""
        total_results = 0
        successful_sources = 0
        
        for source, results in search_results.items():
            if isinstance(results, dict):
                if 'error' not in results:
                    successful_sources += 1
                    total_results += len(results.get('results', []))
        
        success_rate = successful_sources / len(search_results) if search_results else 0
        
        if success_rate >= 0.8 and total_results >= 15:
            return 'excellent'
        elif success_rate >= 0.6 and total_results >= 10:
            return 'good'
        elif success_rate >= 0.4 and total_results >= 5:
            return 'fair'
        else:
            return 'poor'
    
    def _generate_recommended_actions(self, query_analysis: Dict[str, Any], results: List[Dict[str, Any]]) -> List[str]:
        """Generate recommended follow-up actions"""
        actions = []
        
        if len(results) > 20:
            actions.append("Narrow search with more specific keywords")
        elif len(results) < 5:
            actions.append("Broaden search with related terms")
        
        intent = query_analysis.get('intent', '')
        if intent == 'research':
            actions.append("Consider deep-diving into top 3 results")
        elif intent == 'technical':
            actions.append("Check documentation and code examples")
        elif intent == 'news':
            actions.append("Sort by recency and check multiple sources")
        
        return actions
    
    async def _store_search_session(self, search_id: str, query: str, results: Dict[str, Any]):
        """Store search session for future reference"""
        try:
            session_data = {
                'search_id': search_id,
                'query': query,
                'results': results,
                'timestamp': datetime.now(),
                'result_count': results.get('total_results', 0)
            }
            
            await db_manager.store_search_session(session_data)
            logger.info(f"💾 Search session {search_id} stored")
            
        except Exception as e:
            logger.error(f"❌ Failed to store search session: {e}")

# Global search service instance
search_service = DeepSearchService()