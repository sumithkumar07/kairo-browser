"""
🛡️ PHASE 6: Bulletproof Fallback System
Military-grade robustness with intelligent routing and adaptive strategies
"""
import asyncio
import logging
import json
import time
import random
from typing import Dict, Any, Optional, List, Tuple
from urllib.parse import urlparse
import httpx
from playwright.async_api import async_playwright
from config import settings

logger = logging.getLogger(__name__)

class BulletproofFallbackSystem:
    """Military-grade fallback system with intelligent routing"""
    
    def __init__(self):
        self.fallback_tiers = self._initialize_fallback_tiers()
        self.success_metrics = {}
        self.failure_analysis = {}
        self.adaptive_intelligence = {}
        self.routing_decisions = {}
        logger.info("🛡️ Bulletproof Fallback System initialized")
    
    def _initialize_fallback_tiers(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive fallback tier system"""
        return {
            'tier_1_native_browser': {
                'name': 'Native Browser Engine',
                'description': 'Advanced browser engine with full JavaScript support',
                'priority': 1,
                'success_rate': 0.95,
                'avg_response_time': 3000,
                'capabilities': ['full_js', 'media_support', 'interactive_elements', 'real_dom'],
                'use_cases': ['complex_spas', 'javascript_heavy', 'media_rich', 'interactive_forms'],
                'anti_detection': 'maximum',
                'resource_usage': 'high'
            },
            'tier_2_enhanced_playwright': {
                'name': 'Enhanced Playwright Automation',
                'description': 'Playwright with advanced stealth and optimization',
                'priority': 2,
                'success_rate': 0.90,
                'avg_response_time': 2500,
                'capabilities': ['stealth_mode', 'script_injection', 'automation_hooks', 'screenshot'],
                'use_cases': ['automation_heavy', 'data_extraction', 'form_filling', 'navigation'],
                'anti_detection': 'high',
                'resource_usage': 'medium-high'
            },
            'tier_3_stealth_http_rendering': {
                'name': 'Stealth HTTP with JS Rendering',
                'description': 'HTTP proxy with JavaScript execution and anti-detection',
                'priority': 3,
                'success_rate': 0.80,
                'avg_response_time': 2000,
                'capabilities': ['http_proxy', 'js_rendering', 'header_rotation', 'fingerprint_masking'],
                'use_cases': ['content_fetching', 'api_requests', 'standard_websites', 'data_scraping'],
                'anti_detection': 'medium',
                'resource_usage': 'medium'
            },
            'tier_4_mobile_simulation': {
                'name': 'Mobile User Agent Simulation',
                'description': 'Mobile browser simulation with touch events',
                'priority': 4,
                'success_rate': 0.75,
                'avg_response_time': 1800,
                'capabilities': ['mobile_ua', 'touch_events', 'responsive_design', 'mobile_apis'],
                'use_cases': ['mobile_sites', 'responsive_content', 'mobile_apps', 'touch_interfaces'],
                'anti_detection': 'medium',
                'resource_usage': 'low-medium'
            },
            'tier_5_geographic_proxy': {
                'name': 'Geographic Proxy Rotation',
                'description': 'Multiple geographic locations with IP rotation',
                'priority': 5,
                'success_rate': 0.70,
                'avg_response_time': 3500,
                'capabilities': ['ip_rotation', 'geo_distribution', 'proxy_chains', 'location_spoofing'],
                'use_cases': ['geo_restricted', 'ip_blocking', 'regional_content', 'cdn_optimization'],
                'anti_detection': 'medium',
                'resource_usage': 'medium'
            },
            'tier_6_emergency_basic_http': {
                'name': 'Emergency Basic HTTP',
                'description': 'Last resort basic HTTP with minimal processing',
                'priority': 6,
                'success_rate': 0.60,
                'avg_response_time': 1000,
                'capabilities': ['basic_http', 'simple_parsing', 'text_extraction', 'minimal_processing'],
                'use_cases': ['emergency_access', 'basic_content', 'text_only', 'fallback_mode'],
                'anti_detection': 'low',
                'resource_usage': 'low'
            }
        }
    
    async def intelligent_route_request(self, url: str, 
                                      request_type: str = 'navigation',
                                      context: Optional[Dict[str, Any]] = None,
                                      user_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Intelligently route request through optimal fallback tier"""
        try:
            route_start = time.time()
            
            # Analyze target and determine optimal strategy
            site_analysis = await self._analyze_target_site(url, context)
            
            # Select optimal tier based on analysis
            selected_tier = await self._select_optimal_tier(site_analysis, request_type, user_preferences)
            
            # Execute request with selected tier
            result = await self._execute_tier_strategy(url, selected_tier, site_analysis, context)
            
            # If primary tier fails, cascade through fallbacks
            if not result.get('success'):
                result = await self._cascade_fallback_execution(url, selected_tier, site_analysis, context)
            
            # Update routing intelligence
            await self._update_routing_intelligence(url, selected_tier, result, site_analysis)
            
            route_time = (time.time() - route_start) * 1000
            
            return {
                'success': result.get('success', False),
                'content': result.get('content', ''),
                'method_used': result.get('method_used', 'unknown'),
                'tier_used': selected_tier,
                'route_time_ms': route_time,
                'fallback_attempts': result.get('fallback_attempts', 0),
                'site_analysis': site_analysis,
                'performance_metrics': result.get('performance_metrics', {})
            }
            
        except Exception as e:
            logger.error(f"❌ Intelligent routing failed: {e}")
            return await self._emergency_fallback(url)
    
    async def _analyze_target_site(self, url: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze target site for optimal routing decision"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            
            # Site complexity analysis
            complexity_indicators = {
                'spa_frameworks': any(fw in domain for fw in ['react', 'angular', 'vue']),
                'heavy_js_sites': domain in settings.HEAVY_JS_SITES,
                'social_media': any(sm in domain for sm in ['facebook', 'twitter', 'instagram', 'linkedin']),
                'google_services': 'google' in domain,
                'streaming_media': any(media in domain for media in ['youtube', 'netflix', 'twitch']),
                'e_commerce': any(shop in domain for shop in ['amazon', 'ebay', 'shopify']),
                'banking_finance': any(bank in domain for bank in ['bank', 'finance', 'paypal'])
            }
            
            # Security and anti-bot analysis
            security_indicators = {
                'cloudflare_protected': await self._check_cloudflare_protection(domain),
                'bot_detection': await self._estimate_bot_detection_level(domain),
                'captcha_likely': any(indicator for indicator in complexity_indicators.values()),
                'ip_restrictions': domain in ['netflix.com', 'hulu.com', 'bbc.co.uk'],
                'login_required': 'login' in url.lower() or 'auth' in url.lower()
            }
            
            # Performance characteristics
            performance_indicators = {
                'cdn_usage': await self._check_cdn_usage(domain),
                'page_size_estimate': await self._estimate_page_size(domain),
                'load_time_estimate': await self._estimate_load_time(domain, complexity_indicators),
                'mobile_optimized': await self._check_mobile_optimization(domain)
            }
            
            # Historical success rates
            historical_data = self.success_metrics.get(domain, {})
            
            analysis_result = {
                'domain': domain,
                'url': url,
                'complexity_score': sum(complexity_indicators.values()),
                'security_level': sum(security_indicators.values()),
                'performance_score': sum(performance_indicators.values()),
                'complexity_indicators': complexity_indicators,
                'security_indicators': security_indicators,
                'performance_indicators': performance_indicators,
                'historical_success_rates': historical_data,
                'recommended_tier': await self._recommend_tier(complexity_indicators, security_indicators),
                'analysis_timestamp': time.time()
            }
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Site analysis failed: {e}")
            return {
                'domain': urlparse(url).netloc,
                'complexity_score': 3,  # Default medium complexity
                'security_level': 2,    # Default medium security
                'recommended_tier': 'tier_2_enhanced_playwright'
            }
    
    async def _select_optimal_tier(self, site_analysis: Dict[str, Any], 
                                 request_type: str,
                                 user_preferences: Optional[Dict[str, Any]] = None) -> str:
        """Select optimal tier based on comprehensive analysis"""
        try:
            # Get recommended tier from analysis
            recommended_tier = site_analysis.get('recommended_tier')
            
            # Adjust based on request type
            tier_adjustments = {
                'navigation': 0,      # No adjustment for navigation
                'interaction': -1,    # Prefer higher tier for interaction
                'data_extraction': 1, # Can use lower tier for data extraction
                'form_submission': -1, # Prefer higher tier for forms
                'media_access': -2,   # Prefer highest tier for media
                'api_request': 2      # Can use much lower tier for APIs
            }
            
            adjustment = tier_adjustments.get(request_type, 0)
            
            # Apply user preferences
            if user_preferences:
                if user_preferences.get('prefer_speed', False):
                    adjustment += 1  # Use faster, lower tiers
                if user_preferences.get('prefer_reliability', False):
                    adjustment -= 1  # Use more reliable, higher tiers
                if user_preferences.get('prefer_stealth', False):
                    adjustment -= 1  # Use higher stealth tiers
            
            # Calculate final tier
            tier_names = list(self.fallback_tiers.keys())
            recommended_index = tier_names.index(recommended_tier) if recommended_tier in tier_names else 1
            
            final_index = max(0, min(len(tier_names) - 1, recommended_index + adjustment))
            selected_tier = tier_names[final_index]
            
            logger.info(f"🎯 Selected tier {selected_tier} for {site_analysis['domain']}")
            return selected_tier
            
        except Exception as e:
            logger.error(f"❌ Tier selection failed: {e}")
            return 'tier_2_enhanced_playwright'  # Safe default
    
    async def _execute_tier_strategy(self, url: str, tier_name: str,
                                   site_analysis: Dict[str, Any],
                                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute specific tier strategy"""
        try:
            tier_config = self.fallback_tiers[tier_name]
            execution_start = time.time()
            
            logger.info(f"🚀 Executing {tier_config['name']} for {url}")
            
            if tier_name == 'tier_1_native_browser':
                result = await self._execute_native_browser(url, site_analysis, context)
            elif tier_name == 'tier_2_enhanced_playwright':
                result = await self._execute_enhanced_playwright(url, site_analysis, context)
            elif tier_name == 'tier_3_stealth_http_rendering':
                result = await self._execute_stealth_http_rendering(url, site_analysis, context)
            elif tier_name == 'tier_4_mobile_simulation':
                result = await self._execute_mobile_simulation(url, site_analysis, context)
            elif tier_name == 'tier_5_geographic_proxy':
                result = await self._execute_geographic_proxy(url, site_analysis, context)
            elif tier_name == 'tier_6_emergency_basic_http':
                result = await self._execute_emergency_basic_http(url, site_analysis, context)
            else:
                raise ValueError(f"Unknown tier: {tier_name}")
            
            execution_time = (time.time() - execution_start) * 1000
            result['execution_time_ms'] = execution_time
            result['tier_used'] = tier_name
            result['method_used'] = tier_config['name']
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Tier strategy execution failed for {tier_name}: {e}")
            return {'success': False, 'error': str(e), 'tier_used': tier_name}
    
    async def _cascade_fallback_execution(self, url: str, failed_tier: str,
                                        site_analysis: Dict[str, Any],
                                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Cascade through fallback tiers when primary fails"""
        try:
            logger.info(f"🔄 Cascading fallback from {failed_tier} for {url}")
            
            # Get all tiers after the failed one
            tier_names = list(self.fallback_tiers.keys())
            failed_index = tier_names.index(failed_tier)
            
            fallback_attempts = 0
            
            # Try each subsequent tier
            for tier_name in tier_names[failed_index + 1:]:
                fallback_attempts += 1
                logger.info(f"🔄 Trying fallback tier {fallback_attempts}: {tier_name}")
                
                result = await self._execute_tier_strategy(url, tier_name, site_analysis, context)
                
                if result.get('success'):
                    result['fallback_attempts'] = fallback_attempts
                    result['cascade_success'] = True
                    logger.info(f"✅ Fallback successful with {tier_name}")
                    return result
                
                # Brief delay between attempts
                await asyncio.sleep(0.5)
            
            # All tiers failed
            logger.error(f"❌ All fallback tiers failed for {url}")
            return {
                'success': False,
                'error': 'All fallback tiers exhausted',
                'fallback_attempts': fallback_attempts,
                'cascade_failure': True
            }
            
        except Exception as e:
            logger.error(f"❌ Cascade fallback failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_native_browser(self, url: str, site_analysis: Dict[str, Any],
                                    context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute native browser engine strategy"""
        try:
            from .advanced_browser_engine import advanced_browser_engine
            from .stealth_engine_service import stealth_engine
            
            # Create enhanced context with maximum stealth
            context_obj = await advanced_browser_engine.create_enhanced_context('chromium', stealth_level=5)
            
            # Apply military-grade stealth
            await stealth_engine.apply_stealth_profile(context_obj, stealth_level=5)
            
            # Navigate with intelligence
            result = await advanced_browser_engine.navigate_with_intelligence(
                context_obj, url, 'stealth'
            )
            
            if result['success']:
                # Get page content
                page = await context_obj.new_page()
                await page.goto(url, wait_until='networkidle', timeout=60000)
                content = await page.content()
                
                await context_obj.close()
                
                return {
                    'success': True,
                    'content': content,
                    'method': 'native_browser_engine',
                    'stealth_level': 5,
                    'javascript_enabled': True,
                    'performance_metrics': result.get('page_metrics', {})
                }
            else:
                return {'success': False, 'error': result.get('error', 'Navigation failed')}
                
        except Exception as e:
            logger.error(f"❌ Native browser execution failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_enhanced_playwright(self, url: str, site_analysis: Dict[str, Any],
                                         context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute enhanced Playwright strategy"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
                )
                
                context_obj = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                page = await context_obj.new_page()
                
                # Add stealth script
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                """)
                
                await page.goto(url, wait_until='networkidle', timeout=45000)
                content = await page.content()
                
                await browser.close()
                
                return {
                    'success': True,
                    'content': content,
                    'method': 'enhanced_playwright',
                    'stealth_level': 3,
                    'javascript_enabled': True
                }
                
        except Exception as e:
            logger.error(f"❌ Enhanced Playwright execution failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_stealth_http_rendering(self, url: str, site_analysis: Dict[str, Any],
                                            context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute stealth HTTP with rendering strategy"""
        try:
            from .proxy_service import UltraProxyService
            
            proxy_service = UltraProxyService()
            result = await proxy_service.rotating_http_proxy(url)
            
            return {
                'success': True,
                'content': result['content'],
                'method': 'stealth_http_rendering',
                'stealth_level': 4,
                'javascript_enabled': False
            }
            
        except Exception as e:
            logger.error(f"❌ Stealth HTTP rendering failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_mobile_simulation(self, url: str, site_analysis: Dict[str, Any],
                                       context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute mobile simulation strategy"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                
                # Mobile device simulation
                context_obj = await browser.new_context(
                    viewport={'width': 375, 'height': 667},
                    user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
                    is_mobile=True,
                    has_touch=True
                )
                
                page = await context_obj.new_page()
                await page.goto(url, wait_until='networkidle', timeout=30000)
                content = await page.content()
                
                await browser.close()
                
                return {
                    'success': True,
                    'content': content,
                    'method': 'mobile_simulation',
                    'device_type': 'mobile',
                    'javascript_enabled': True
                }
                
        except Exception as e:
            logger.error(f"❌ Mobile simulation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_geographic_proxy(self, url: str, site_analysis: Dict[str, Any],
                                      context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute geographic proxy strategy"""
        try:
            # Simulate geographic proxy (in production would use real proxy service)
            headers = {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]),
                'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8']),
                'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
            }
            
            async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
                response = await client.get(url)
                
                return {
                    'success': True,
                    'content': response.text,
                    'method': 'geographic_proxy',
                    'proxy_location': 'simulated',
                    'status_code': response.status_code
                }
                
        except Exception as e:
            logger.error(f"❌ Geographic proxy failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _execute_emergency_basic_http(self, url: str, site_analysis: Dict[str, Any],
                                          context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute emergency basic HTTP strategy"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url)
                
                return {
                    'success': True,
                    'content': response.text,
                    'method': 'emergency_basic_http',
                    'minimal_processing': True,
                    'status_code': response.status_code
                }
                
        except Exception as e:
            logger.error(f"❌ Emergency basic HTTP failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _emergency_fallback(self, url: str) -> Dict[str, Any]:
        """Last resort emergency fallback"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                
                return {
                    'success': True,
                    'content': response.text,
                    'method': 'emergency_fallback',
                    'warning': 'Used emergency fallback due to routing failure'
                }
                
        except Exception as e:
            return {
                'success': False,
                'content': f'<html><body><h1>Access Failed</h1><p>Unable to access {url}</p><p>Error: {str(e)}</p></body></html>',
                'method': 'emergency_fallback',
                'error': str(e)
            }
    
    # Helper methods for site analysis
    async def _check_cloudflare_protection(self, domain: str) -> bool:
        """Check if site uses Cloudflare protection"""
        # Simplified check - in production would use actual detection
        cloudflare_indicators = ['cloudflare', 'cf-ray']
        return any(indicator in domain.lower() for indicator in cloudflare_indicators)
    
    async def _estimate_bot_detection_level(self, domain: str) -> int:
        """Estimate bot detection level (0-3)"""
        high_detection = ['google.com', 'facebook.com', 'amazon.com', 'netflix.com']
        medium_detection = ['twitter.com', 'linkedin.com', 'instagram.com']
        
        if any(hd in domain for hd in high_detection):
            return 3
        elif any(md in domain for md in medium_detection):
            return 2
        else:
            return 1
    
    async def _check_cdn_usage(self, domain: str) -> bool:
        """Check if site likely uses CDN"""
        cdn_indicators = ['cdn', 'cloudfront', 'fastly', 'cloudflare']
        return any(indicator in domain for indicator in cdn_indicators)
    
    async def _estimate_page_size(self, domain: str) -> str:
        """Estimate page size category"""
        heavy_sites = ['youtube.com', 'netflix.com', 'facebook.com']
        if any(hs in domain for hs in heavy_sites):
            return 'large'
        else:
            return 'medium'
    
    async def _estimate_load_time(self, domain: str, complexity: Dict[str, bool]) -> int:
        """Estimate load time in milliseconds"""
        base_time = 2000
        if complexity['heavy_js_sites']:
            base_time += 2000
        if complexity['streaming_media']:
            base_time += 3000
        return base_time
    
    async def _check_mobile_optimization(self, domain: str) -> bool:
        """Check if site is mobile optimized"""
        # Most modern sites are mobile optimized
        return True
    
    async def _recommend_tier(self, complexity: Dict[str, bool], security: Dict[str, bool]) -> str:
        """Recommend optimal tier based on indicators"""
        if complexity['heavy_js_sites'] or security['bot_detection']:
            return 'tier_1_native_browser'
        elif complexity['spa_frameworks']:
            return 'tier_2_enhanced_playwright'
        else:
            return 'tier_3_stealth_http_rendering'
    
    async def _update_routing_intelligence(self, url: str, tier_used: str,
                                         result: Dict[str, Any], site_analysis: Dict[str, Any]):
        """Update routing intelligence based on results"""
        try:
            domain = site_analysis.get('domain', urlparse(url).netloc)
            
            # Update success metrics
            if domain not in self.success_metrics:
                self.success_metrics[domain] = {}
            
            if tier_used not in self.success_metrics[domain]:
                self.success_metrics[domain][tier_used] = {'attempts': 0, 'successes': 0}
            
            self.success_metrics[domain][tier_used]['attempts'] += 1
            if result.get('success'):
                self.success_metrics[domain][tier_used]['successes'] += 1
            
            # Update routing decisions
            decision_key = f"{domain}_{tier_used}"
            self.routing_decisions[decision_key] = {
                'timestamp': time.time(),
                'success': result.get('success', False),
                'response_time': result.get('execution_time_ms', 0),
                'fallback_used': result.get('fallback_attempts', 0) > 0
            }
            
        except Exception as e:
            logger.debug(f"Routing intelligence update error: {e}")
    
    def get_system_analytics(self) -> Dict[str, Any]:
        """Get comprehensive system analytics"""
        try:
            total_attempts = 0
            total_successes = 0
            tier_performance = {}
            
            for domain, metrics in self.success_metrics.items():
                for tier, stats in metrics.items():
                    total_attempts += stats['attempts']
                    total_successes += stats['successes']
                    
                    if tier not in tier_performance:
                        tier_performance[tier] = {'attempts': 0, 'successes': 0}
                    
                    tier_performance[tier]['attempts'] += stats['attempts']
                    tier_performance[tier]['successes'] += stats['successes']
            
            # Calculate success rates
            for tier in tier_performance:
                attempts = tier_performance[tier]['attempts']
                successes = tier_performance[tier]['successes']
                tier_performance[tier]['success_rate'] = successes / attempts if attempts > 0 else 0
            
            return {
                'total_requests': total_attempts,
                'total_successes': total_successes,
                'overall_success_rate': total_successes / total_attempts if total_attempts > 0 else 0,
                'tier_performance': tier_performance,
                'domains_analyzed': len(self.success_metrics),
                'routing_decisions_made': len(self.routing_decisions),
                'fallback_tiers_available': len(self.fallback_tiers)
            }
            
        except Exception as e:
            logger.error(f"❌ System analytics error: {e}")
            return {'error': str(e)}

# Global bulletproof fallback system instance
bulletproof_fallback_system = BulletproofFallbackSystem()