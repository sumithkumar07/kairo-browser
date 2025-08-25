"""
Ultra-Enhanced Proxy Service with Advanced Anti-Detection & Website Access
"""
import asyncio
import logging
import random
import time
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin, urlparse
import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from config import settings

logger = logging.getLogger(__name__)

class UltraProxyService:
    """Ultra-enhanced proxy service with advanced anti-detection"""
    
    def __init__(self):
        self.http_client = None
        self.user_agents = self._get_real_user_agents()
        self.proxy_sessions = {}
        logger.info("🚀 Ultra-Enhanced Proxy Service initialized with advanced anti-detection")
    
    def _get_real_user_agents(self) -> List[str]:
        """Get list of real user agents for rotation"""
        return [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
    
    async def route_request(self, url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Ultra-smart routing with multiple fallback strategies"""
        try:
            logger.info(f"🔍 Ultra-routing request for: {url}")
            
            # Multi-layer approach for maximum success
            strategies = [
                ("ultra_stealth_browser", "🥷 Ultra-stealth browser engine"),
                ("rotating_http_proxy", "🔄 Rotating HTTP proxy with random delays"),
                ("enhanced_browser_fallback", "📱 Enhanced browser fallback"),
                ("basic_http_fallback", "🌐 Basic HTTP fallback")
            ]
            
            for strategy, description in strategies:
                try:
                    logger.info(f"{description} for: {url}")
                    
                    if strategy == "ultra_stealth_browser":
                        return await self.ultra_stealth_browser_proxy(url, headers)
                    elif strategy == "rotating_http_proxy":
                        return await self.rotating_http_proxy(url, headers)
                    elif strategy == "enhanced_browser_fallback":
                        return await self.browser_proxy(url, headers)
                    else:  # basic_http_fallback
                        return await self.enhanced_http_proxy(url, headers)
                        
                except Exception as strategy_error:
                    logger.warning(f"Strategy {strategy} failed: {strategy_error}")
                    continue
                    
            # If all strategies fail
            logger.error(f"❌ All proxy strategies failed for {url}")
            return await self._advanced_fallback_response(url, "All access methods exhausted")
                    
        except Exception as e:
            logger.error(f"❌ Critical routing failure for {url}: {e}")
            return await self._advanced_fallback_response(url, str(e))
    
    def _requires_browser_engine(self, url: str) -> bool:
        """Check if site requires browser engine"""
        return any(site in url.lower() for site in settings.HEAVY_JS_SITES)
    
    async def ultra_stealth_browser_proxy(self, url: str, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Ultra-stealth browser proxy with maximum anti-detection"""
        try:
            logger.info(f"🥷 Launching ultra-stealth browser for: {url}")
            
            async with async_playwright() as p:
                # Random user agent selection
                user_agent = random.choice(self.user_agents)
                
                # Ultra-stealth browser launch with randomization
                browser = await p.chromium.launch(
                    headless=True,
                    args=self._get_ultra_stealth_args(),
                    executable_path=None
                )
                
                # Randomized viewport sizes (common resolutions)
                viewports = [
                    {'width': 1920, 'height': 1080},
                    {'width': 1366, 'height': 768},
                    {'width': 1536, 'height': 864},
                    {'width': 1440, 'height': 900},
                    {'width': 1280, 'height': 720}
                ]
                
                viewport = random.choice(viewports)
                
                # Ultra-enhanced context with randomization
                context = await browser.new_context(
                    viewport=viewport,
                    user_agent=user_agent,
                    locale=random.choice(['en-US', 'en-GB', 'en-CA']),
                    timezone_id=random.choice(['America/New_York', 'Europe/London', 'America/Los_Angeles']),
                    permissions=['geolocation', 'notifications'],
                    geolocation={'latitude': 40.7128 + random.uniform(-0.1, 0.1), 'longitude': -74.0060 + random.uniform(-0.1, 0.1)},
                    extra_http_headers=self._get_ultra_stealth_headers(custom_headers, user_agent)
                )
                
                # Ultra-comprehensive anti-detection script injection
                await context.add_init_script(self._get_ultra_anti_detection_script())
                
                page = await context.new_page()
                
                # Set additional page properties for stealth
                await page.evaluate(self._get_page_stealth_script())
                
                # Random delay before navigation (human-like behavior)
                await asyncio.sleep(random.uniform(1.0, 3.0))
                
                # Navigate with enhanced options and retry mechanism
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        logger.info(f"🔄 Navigation attempt {attempt + 1} for {url}")
                        
                        await page.goto(
                            url, 
                            wait_until='networkidle', 
                            timeout=settings.BROWSER_TIMEOUT * 2  # Longer timeout for stealth
                        )
                        
                        # Wait for dynamic content with random delay
                        await asyncio.sleep(random.uniform(3.0, 7.0))
                        
                        # Try to wait for main content areas
                        content_selectors = ['body', 'main', '#content', '.content', '#main', '.main']
                        for selector in content_selectors:
                            try:
                                await page.wait_for_selector(selector, timeout=5000)
                                break
                            except:
                                continue
                                
                        break  # Success, exit retry loop
                        
                    except Exception as nav_error:
                        logger.warning(f"Navigation attempt {attempt + 1} failed: {nav_error}")
                        if attempt == max_retries - 1:
                            raise nav_error
                        await asyncio.sleep(random.uniform(2.0, 5.0))
                
                # Execute additional stealth measures
                await self._execute_stealth_measures(page)
                
                # Get rendered content
                content = await page.content()
                
                # Ultra-enhanced HTML processing
                enhanced_content = await self._process_ultra_browser_content(content, url)
                
                await browser.close()
                
                return {
                    "content": enhanced_content,
                    "status_code": 200,
                    "headers": {"Content-Type": "text/html; charset=utf-8"},
                    "url": url,
                    "method": "ultra_stealth_browser",
                    "iframe_safe": True,
                    "anti_detection": True,
                    "javascript_rendered": True,
                    "stealth_level": "maximum",
                    "user_agent": user_agent
                }
                
        except Exception as e:
            logger.error(f"❌ Ultra-stealth browser proxy failed: {e}")
            raise
            
    async def rotating_http_proxy(self, url: str, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """HTTP proxy with user agent rotation and timing randomization"""
        try:
            # Random user agent and headers
            user_agent = random.choice(self.user_agents)
            headers = self._get_rotating_headers(user_agent)
            
            if custom_headers:
                headers.update(custom_headers)
            
            # Random delay to mimic human behavior
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            # Enhanced HTTP client with randomization
            timeout = httpx.Timeout(
                connect=random.uniform(5.0, 15.0),
                read=random.uniform(15.0, 45.0),
                write=5.0,
                pool=5.0
            )
            
            async with httpx.AsyncClient(
                timeout=timeout,
                follow_redirects=True,
                limits=httpx.Limits(max_keepalive_connections=random.randint(3, 8), max_connections=settings.MAX_CONNECTIONS),
                headers=headers
            ) as client:
                
                # Make request with retry mechanism
                max_retries = 2
                for attempt in range(max_retries):
                    try:
                        response = await client.get(url, headers=headers)
                        break
                    except Exception as req_error:
                        if attempt == max_retries - 1:
                            raise req_error
                        await asyncio.sleep(random.uniform(1.0, 3.0))
                
                # Process and enhance HTML with ultra-processing
                enhanced_content = await self._process_ultra_html_content(response.text, url, user_agent)
                
                # Ultra-clean response headers
                clean_headers = self._ultra_clean_response_headers(response.headers)
                
                return {
                    "content": enhanced_content,
                    "status_code": response.status_code,
                    "headers": clean_headers,
                    "url": str(response.url),
                    "method": "rotating_http_proxy",
                    "iframe_safe": True,
                    "anti_detection": True,
                    "user_agent": user_agent,
                    "rotation": True
                }
                
        except Exception as e:
            logger.error(f"❌ Rotating HTTP proxy failed: {e}")
            raise
    
    async def enhanced_http_proxy(self, url: str, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Enhanced HTTP proxy with anti-detection measures"""
        try:
            headers = self._get_browser_headers()
            if custom_headers:
                headers.update(custom_headers)
            
            async with httpx.AsyncClient(
                timeout=settings.HTTP_TIMEOUT,
                follow_redirects=True,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=settings.MAX_CONNECTIONS)
            ) as client:
                response = await client.get(url, headers=headers)
                
                # Process and enhance HTML
                enhanced_content = await self._process_html_content(response.text, url)
                
                # Clean response headers
                clean_headers = self._clean_response_headers(response.headers)
                
                return {
                    "content": enhanced_content,
                    "status_code": response.status_code,
                    "headers": clean_headers,
                    "url": str(response.url),
                    "method": "enhanced_http_proxy",
                    "iframe_safe": True,
                    "anti_detection": True
                }
                
        except Exception as e:
            logger.error(f"❌ Enhanced HTTP proxy failed: {e}")
            raise
    
    async def browser_proxy(self, url: str, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Advanced browser proxy using Playwright with enhanced anti-detection"""
        try:
            async with async_playwright() as p:
                # Launch browser with stealth configuration
                browser = await p.chromium.launch(
                    headless=True,
                    args=self._get_browser_args()
                )
                
                # Enhanced browser context
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent=self._get_stealth_user_agent(),
                    locale='en-US',
                    timezone_id='America/New_York',
                    permissions=['geolocation'],
                    extra_http_headers=self._get_stealth_headers(custom_headers)
                )
                
                # Add anti-detection script
                await context.add_init_script(self._get_anti_detection_script())
                
                page = await context.new_page()
                
                # Navigate with enhanced options
                try:
                    await page.goto(url, wait_until='networkidle', timeout=settings.BROWSER_TIMEOUT)
                    await page.wait_for_timeout(5000)  # Wait for dynamic content
                    
                    # Try to wait for main content
                    try:
                        await page.wait_for_selector('body', timeout=10000)
                    except:
                        pass  # Continue with whatever loaded
                        
                except Exception as nav_error:
                    logger.warning(f"Navigation warning for {url}: {nav_error}")
                
                # Get rendered content
                content = await page.content()
                
                # Enhanced HTML processing
                enhanced_content = await self._process_browser_content(content, url)
                
                await browser.close()
                
                return {
                    "content": enhanced_content,
                    "status_code": 200,
                    "headers": {"Content-Type": "text/html; charset=utf-8"},
                    "url": url,
                    "method": "enhanced_browser_rendered",
                    "iframe_safe": True,
                    "anti_detection": True,
                    "javascript_rendered": True
                }
                
        except Exception as e:
            logger.error(f"❌ Browser proxy failed: {e}")
            raise
    
    async def _process_ultra_html_content(self, html: str, base_url: str, user_agent: str) -> str:
        """Ultra-enhanced HTML processing for maximum compatibility"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Ultra-comprehensive blocking element removal
            self._ultra_remove_blocking_elements(soup)
            
            # Enhanced frame-busting script removal
            self._ultra_remove_frame_busting_scripts(soup)
            
            # Advanced base tag and header injection
            self._ultra_add_base_and_headers(soup, base_url)
            
            # Enhanced link and form rewriting
            self._ultra_rewrite_links_and_forms(soup, base_url)
            
            # Ultra-compatibility enhancements
            self._add_ultra_compatibility_enhancements(soup, "ultra_http_proxy", user_agent)
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Ultra HTML processing failed: {e}")
            return html
    
    async def _process_ultra_browser_content(self, html: str, base_url: str) -> str:
        """Ultra-process browser-rendered content"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Ultra-enhanced processing for browser-rendered content
            self._ultra_remove_blocking_elements(soup)
            self._ultra_remove_frame_busting_scripts(soup)
            self._ultra_add_base_and_headers(soup, base_url)
            self._ultra_rewrite_links_and_forms(soup, base_url)
            self._add_ultra_compatibility_enhancements(soup, "ultra_stealth_browser", "")
            
            return str(soup)
            
        except Exception as e:
            logger.error(f"Ultra browser content processing failed: {e}")
            return html
    
    def _ultra_remove_blocking_elements(self, soup):
        """Ultra-comprehensive removal of blocking elements"""
        # Remove all known blocking meta tags
        for meta in soup.find_all('meta'):
            http_equiv = meta.get('http-equiv', '').lower()
            content = meta.get('content', '').lower()
            name = meta.get('name', '').lower()
            
            blocking_patterns = [
                'x-frame-options', 'content-security-policy', 'x-content-type-options',
                'frame-options', 'sameorigin', 'deny', 'frame-ancestors',
                'referrer-policy', 'permissions-policy'
            ]
            
            if any(pattern in http_equiv or pattern in content or pattern in name for pattern in blocking_patterns):
                meta.decompose()
        
        # Remove noscript tags that might contain blocking code
        for noscript in soup.find_all('noscript'):
            noscript.decompose()
        
        # Remove potentially problematic style blocks
        for style in soup.find_all('style'):
            style_content = style.string or ''
            if any(pattern in style_content for pattern in ['frame-busting', 'top.location', 'parent.location']):
                style.decompose()
    
    def _ultra_remove_frame_busting_scripts(self, soup):
        """Ultra-comprehensive frame-busting script removal"""
        ultra_blocking_patterns = [
            'top.location', 'frameElement', 'self !== top', 'parent.frames',
            'window.top', 'top != self', 'parent != window', 'top != window',
            'self != top', 'frameElement != null', 'window.frameElement',
            'parent.document', 'top.document', 'window.parent',
            'top === window', 'window === top', 'parent === window',
            'document.domain', 'location.ancestorOrigins',
            'window.opener', 'self.location', 'parent.location',
            'top.frames', 'parent.postMessage', 'postMessage(',
            'document.referrer', 'window.name', 'opener',
            'frame-busting', 'framebusting', 'clickjacking',
            'X-Frame-Options', 'frame-ancestors', 'sandbox'
        ]
        
        for script in soup.find_all('script'):
            if script.string:
                script_content = script.string.lower()
                if any(pattern.lower() in script_content for pattern in ultra_blocking_patterns):
                    # Replace with harmless comment
                    script.string = '/* Ultra frame compatibility - original script neutralized by Kairo Browser */'
            elif script.get('src'):
                # Check for external scripts that might contain frame busting
                src = script.get('src', '').lower()
                suspicious_sources = ['framebreaker', 'clickjack', 'security', 'protection']
                if any(sus in src for sus in suspicious_sources):
                    script.decompose()
    
    def _ultra_add_base_and_headers(self, soup, base_url: str):
        """Ultra-enhanced base tag and header injection"""
        if not soup.head:
            soup.insert(0, soup.new_tag("head"))
        
        # Ultra-permissive base tag
        base_tag = soup.new_tag("base", href=base_url, target="_self")
        soup.head.insert(0, base_tag)
        
        # Ultra-permissive CSP that allows everything
        ultra_csp = soup.new_tag("meta")
        ultra_csp.attrs['http-equiv'] = 'Content-Security-Policy'
        ultra_csp.attrs['content'] = "default-src * 'unsafe-inline' 'unsafe-eval' data: blob: filesystem: about: ws: wss: 'unsafe-hashes'; script-src * 'unsafe-inline' 'unsafe-eval'; connect-src * 'unsafe-inline'; img-src * data: blob: 'unsafe-inline'; frame-src *; style-src * 'unsafe-inline'; font-src * data:; frame-ancestors *; form-action *;"
        soup.head.append(ultra_csp)
        
        # Multiple X-Frame-Options overrides
        for value in ['ALLOWALL', 'SAMEORIGIN', 'DENY']:  # Try all values
            frame_options = soup.new_tag("meta")
            frame_options.attrs['http-equiv'] = 'X-Frame-Options'
            frame_options.attrs['content'] = 'ALLOWALL'  # Always use ALLOWALL
            soup.head.append(frame_options)
        
        # Additional compatibility headers
        compatibility_headers = [
            ('Referrer-Policy', 'no-referrer-when-downgrade'),
            ('Permissions-Policy', 'geolocation=*, microphone=*, camera=*'),
            ('Cross-Origin-Embedder-Policy', 'unsafe-none'),
            ('Cross-Origin-Opener-Policy', 'same-origin-allow-popups'),
            ('Cross-Origin-Resource-Policy', 'cross-origin')
        ]
        
        for header, value in compatibility_headers:
            meta_tag = soup.new_tag("meta")
            meta_tag.attrs['http-equiv'] = header
            meta_tag.attrs['content'] = value
            soup.head.append(meta_tag)
    
    def _ultra_rewrite_links_and_forms(self, soup, base_url: str):
        """Ultra-enhanced link and form rewriting"""
        # Enhanced link rewriting
        for link in soup.find_all(['a', 'link']):
            href = link.get('href')
            if href and not href.startswith('#') and not href.startswith('javascript:') and not href.startswith('mailto:'):
                try:
                    full_url = self._resolve_url(href, base_url)
                    link['data-kairo-original-href'] = href
                    link['data-kairo-proxy-url'] = full_url
                    link['href'] = '#kairo-intercepted'
                    # Add click handler class
                    existing_classes = link.get('class', [])
                    if isinstance(existing_classes, str):
                        existing_classes = existing_classes.split()
                    existing_classes.append('kairo-intercepted-link')
                    link['class'] = ' '.join(existing_classes)
                except:
                    pass
        
        # Enhanced form rewriting
        for form in soup.find_all('form'):
            action = form.get('action')
            if action and not action.startswith('#') and not action.startswith('javascript:'):
                try:
                    full_url = self._resolve_url(action, base_url)
                    form['data-kairo-original-action'] = action
                    form['data-kairo-proxy-action'] = full_url
                    form['action'] = '#kairo-form-intercepted'
                    # Add form handler class
                    existing_classes = form.get('class', [])
                    if isinstance(existing_classes, str):
                        existing_classes = existing_classes.split()
                    existing_classes.append('kairo-intercepted-form')
                    form['class'] = ' '.join(existing_classes)
                except:
                    pass
        
        # Rewrite iframe sources for recursive proxying
        for iframe in soup.find_all('iframe'):
            src = iframe.get('src')
            if src and not src.startswith('data:') and not src.startswith('javascript:'):
                try:
                    full_url = self._resolve_url(src, base_url)
                    iframe['data-kairo-original-src'] = src
                    iframe['data-kairo-proxy-src'] = full_url
                    # Keep original src but mark for potential re-proxying
                except:
                    pass
    
    def _get_browser_headers(self) -> Dict[str, str]:
        """Get enhanced browser headers"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Sec-CH-UA': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"'
        }
    
    def _get_ultra_stealth_args(self) -> list:
        """Get ultra-stealth browser launch arguments"""
        return [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            # Ultra-stealth additions
            '--disable-infobars',
            '--disable-notifications',
            '--disable-default-apps',
            '--disable-extensions-file-access-check',
            '--disable-extensions-http-throttling',
            '--disable-client-side-phishing-detection',
            '--disable-component-extensions-with-background-pages',
            '--disable-background-networking',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--mute-audio',
            '--disable-plugins-discovery',
            '--disable-prerender-local-predictor',
            '--disable-device-discovery-notifications'
        ]
    
    def _get_ultra_stealth_headers(self, custom_headers: Optional[Dict[str, str]], user_agent: str) -> Dict[str, str]:
        """Get ultra-realistic headers with randomization"""
        # Base headers that match the user agent
        base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.9', 'en-US,en;q=0.8,es;q=0.6']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
            'Pragma': 'no-cache' if random.random() > 0.3 else None,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1' if random.random() > 0.7 else None,
            'Connection': 'keep-alive'
        }
        
        # Add realistic Sec-CH-UA headers based on user agent
        if 'Chrome' in user_agent:
            version_match = user_agent.split('Chrome/')[1].split('.')[0] if 'Chrome/' in user_agent else '120'
            base_headers.update({
                'Sec-CH-UA': f'"Not_A Brand";v="8", "Chromium";v="{version_match}", "Google Chrome";v="{version_match}"',
                'Sec-CH-UA-Mobile': '?0',
                'Sec-CH-UA-Platform': random.choice(['"Windows"', '"macOS"', '"Linux"'])
            })
        
        # Remove None values
        headers = {k: v for k, v in base_headers.items() if v is not None}
        
        if custom_headers:
            headers.update(custom_headers)
        
        return headers
    
    def _get_rotating_headers(self, user_agent: str) -> Dict[str, str]:
        """Get rotating HTTP headers for stealth requests"""
        return {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en-US;q=0.9,en;q=0.8', 'en-US,en;q=0.8']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': random.choice(['no-cache', 'max-age=0']),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': '1' if random.random() > 0.5 else '0'
        }
    
    def _get_ultra_anti_detection_script(self) -> str:
        """Get comprehensive ultra-anti-detection script"""
        return """
            // Ultra-comprehensive anti-detection measures
            (function() {
                'use strict';
                
                // Remove webdriver property completely
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                
                // Remove automation indicators
                delete navigator.__proto__.webdriver;
                delete window.navigator.webdriver;
                
                // Mock chrome object
                window.chrome = {
                    runtime: {
                        onConnect: undefined,
                        onMessage: undefined
                    },
                    app: {
                        isInstalled: false
                    }
                };
                
                // Override languages with realistic values
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                    configurable: true
                });
                
                // Mock realistic plugin array
                Object.defineProperty(navigator, 'plugins', {
                    get: () => ({
                        length: 3,
                        0: {name: 'Chrome PDF Plugin', description: 'Portable Document Format'},
                        1: {name: 'Chrome PDF Viewer', description: 'PDF Viewer'},
                        2: {name: 'Native Client', description: 'Native Client'}
                    }),
                    configurable: true
                });
                
                // Override permissions query
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Mock realistic hardware concurrency
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => Math.floor(Math.random() * 8) + 2,
                    configurable: true
                });
                
                // Override connection property
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        type: 'wifi'
                    }),
                    configurable: true
                });
                
                // Hide automation traces
                const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'click');
                if (elementDescriptor) {
                    Object.defineProperty(HTMLElement.prototype, 'click', {
                        ...elementDescriptor,
                        value: function(...args) {
                            return elementDescriptor.value.apply(this, args);
                        }
                    });
                }
                
            })();
        """
    
    def _get_page_stealth_script(self) -> str:
        """Get page-level stealth script executed after page load"""
        return """
            // Page-level stealth measures
            Object.defineProperty(document, 'hidden', {
                get: () => false,
                configurable: true
            });
            
            Object.defineProperty(document, 'visibilityState', {
                get: () => 'visible',
                configurable: true
            });
            
            // Mock realistic screen properties
            Object.defineProperties(screen, {
                availHeight: { get: () => screen.height - Math.floor(Math.random() * 100) + 50 },
                availWidth: { get: () => screen.width },
                colorDepth: { get: () => 24 },
                pixelDepth: { get: () => 24 }
            });
        """
    
    async def _execute_stealth_measures(self, page) -> None:
        """Execute additional stealth measures on the page"""
        try:
            # Remove automation-specific properties
            await page.evaluate("""
                () => {
                    // Remove any automation traces
                    if (window.outerHeight === 0) {
                        Object.defineProperty(window, 'outerHeight', {
                            get: () => window.innerHeight + 85
                        });
                    }
                    
                    if (window.outerWidth === 0) {
                        Object.defineProperty(window, 'outerWidth', {
                            get: () => window.innerWidth + 16
                        });
                    }
                }
            """)
            
            # Simulate human-like mouse movements (invisible)
            await page.mouse.move(
                random.randint(100, 800), 
                random.randint(100, 600)
            )
            
            # Random scroll to simulate reading
            await page.evaluate(f"""
                window.scrollTo(0, {random.randint(0, 500)});
            """)
            
        except Exception as e:
            logger.debug(f"Stealth measures warning: {e}")
            # Not critical, continue
    
    def _get_stealth_user_agent(self) -> str:
        """Get stealth user agent"""
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    def _get_stealth_headers(self, custom_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Get stealth headers for browser"""
        headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        if custom_headers:
            headers.update(custom_headers)
        return headers
    
    def _get_anti_detection_script(self) -> str:
        """Get comprehensive anti-detection script"""
        return """
            // Enhanced anti-detection measures
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            window.chrome = {
                runtime: {},
            };
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Remove automation indicators
            delete navigator.__proto__.webdriver;
            
            // Override permission methods
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """
    
    def _remove_blocking_meta_tags(self, soup):
        """Remove meta tags that block iframe embedding"""
        for meta in soup.find_all('meta'):
            http_equiv = meta.get('http-equiv', '').lower()
            content = meta.get('content', '').lower()
            
            if http_equiv in ['x-frame-options', 'content-security-policy'] or \
               'frame-options' in content or 'sameorigin' in content or 'deny' in content:
                meta.decompose()
    
    def _remove_frame_busting_scripts(self, soup):
        """Remove frame-busting JavaScript"""
        blocking_patterns = [
            'top.location', 'frameElement', 'self !== top', 'parent.frames',
            'window.top', 'top != self', 'parent != window', 'top != window',
            'self != top', 'frameElement != null', 'window.frameElement',
            'parent.document', 'top.document', 'window.parent'
        ]
        
        for script in soup.find_all('script'):
            script_content = script.string or ''
            if any(pattern in script_content for pattern in blocking_patterns):
                script.string = '/* Frame compatibility - script modified by Kairo Browser */'
    
    def _add_base_and_headers(self, soup, base_url: str):
        """Add base tag and iframe-friendly headers"""
        if soup.head:
            # Base tag
            base_tag = soup.new_tag("base", href=base_url)
            soup.head.insert(0, base_tag)
            
            # Permissive CSP
            csp_meta = soup.new_tag("meta")
            csp_meta.attrs['http-equiv'] = 'Content-Security-Policy'
            csp_meta.attrs['content'] = "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:; frame-ancestors *; frame-src *;"
            soup.head.append(csp_meta)
            
            # X-Frame-Options override
            frame_options = soup.new_tag("meta")
            frame_options.attrs['http-equiv'] = 'X-Frame-Options'
            frame_options.attrs['content'] = 'ALLOWALL'
            soup.head.append(frame_options)
    
    def _rewrite_links_and_forms(self, soup, base_url: str):
        """Rewrite links and forms for proxy handling"""
        # Rewrite links
        for link in soup.find_all(['a', 'link']):
            href = link.get('href')
            if href and not href.startswith('#') and not href.startswith('javascript:'):
                full_url = self._resolve_url(href, base_url)
                link['data-proxy-url'] = full_url
                link['href'] = '#'
        
        # Rewrite forms
        for form in soup.find_all('form'):
            action = form.get('action')
            if action and not action.startswith('#') and not action.startswith('javascript:'):
                full_url = self._resolve_url(action, base_url)
                form['data-proxy-action'] = full_url
                form['action'] = '#'
    
    def _resolve_url(self, url: str, base_url: str) -> str:
        """Resolve relative URLs to absolute"""
        if url.startswith('//'):
            return 'https:' + url
        elif url.startswith('/'):
            return urljoin(base_url, url)
        elif not url.startswith(('http:', 'https:')):
            return urljoin(base_url, url)
        return url
    
    def _add_compatibility_enhancements(self, soup, proxy_type: str):
        """Add CSS and JavaScript enhancements"""
        # Enhanced CSS
        style_tag = soup.new_tag("style")
        style_tag.string = self._get_compatibility_css()
        
        if soup.head:
            soup.head.append(style_tag)
        elif soup.body:
            soup.body.insert(0, style_tag)
        
        # Enhanced JavaScript
        js_tag = soup.new_tag("script")
        js_tag.string = self._get_compatibility_js(proxy_type)
        
        if soup.body:
            soup.body.append(js_tag)
    
    def _get_compatibility_css(self) -> str:
        """Get enhanced compatibility CSS"""
        return """
            /* Kairo Browser Enhanced Compatibility Styles */
            body { 
                margin: 0 !important; 
                padding: 0 !important; 
                overflow-x: auto !important;
                min-height: 100vh !important;
                width: 100% !important;
            }
            
            * { 
                box-sizing: border-box !important; 
            }
            
            /* Fix iframe breaking elements */
            iframe, embed, object { 
                max-width: 100% !important; 
            }
            
            /* Prevent fixed positioning issues */
            .fixed-header, .fixed-nav, .sticky-header, 
            [style*="position: fixed"], [class*="fixed"], [id*="fixed"] {
                position: relative !important;
                top: auto !important;
                left: auto !important;
                right: auto !important;
                bottom: auto !important;
                z-index: auto !important;
            }
            
            /* Ensure content visibility */
            [style*="display: none"], [style*="visibility: hidden"] {
                display: block !important;
                visibility: visible !important;
            }
            
            /* Override breakout attempts */
            .breakout, .fullscreen, [class*="overlay"], [id*="overlay"] {
                position: relative !important;
                width: 100% !important;
                height: auto !important;
            }
        """
    
    def _get_compatibility_js(self, proxy_type: str) -> str:
        """Get enhanced compatibility JavaScript"""
        return f"""
            // Kairo Browser Enhanced Navigation Interception
            (function() {{
                'use strict';
                
                console.log('Kairo Browser: Loading enhanced compatibility for {proxy_type}');
                
                try {{
                    // Override frame detection
                    Object.defineProperty(window, 'top', {{
                        get: function() {{ return window.self; }},
                        set: function() {{}},
                        configurable: false
                    }});
                    
                    Object.defineProperty(window, 'parent', {{
                        get: function() {{ return window.self; }},
                        set: function() {{}},
                        configurable: false
                    }});
                    
                    Object.defineProperty(window, 'frameElement', {{
                        get: function() {{ return null; }},
                        set: function() {{}},
                        configurable: false
                    }});
                    
                    // Intercept navigation attempts
                    const originalOpen = window.open;
                    window.open = function(url, target, features) {{
                        console.log('Kairo Browser: Intercepted window.open to', url);
                        if (window.parent && window.parent.postMessage) {{
                            window.parent.postMessage({{
                                type: 'NAVIGATE_TO',
                                url: url
                            }}, '*');
                        }}
                        return null;
                    }};
                    
                    // Override location methods
                    ['replace', 'assign'].forEach(method => {{
                        const original = window.location[method];
                        window.location[method] = function(url) {{
                            console.log(`Kairo Browser: Intercepted location.${{method}} to`, url);
                            if (window.parent && window.parent.postMessage) {{
                                window.parent.postMessage({{
                                    type: 'NAVIGATE_TO',
                                    url: url
                                }}, '*');
                            }}
                        }};
                    }});
                    
                    // Enhanced link click interception
                    document.addEventListener('click', function(e) {{
                        var target = e.target;
                        
                        while (target && target.tagName !== 'A') {{
                            target = target.parentElement;
                        }}
                        
                        if (target && target.tagName === 'A') {{
                            var proxyUrl = target.getAttribute('data-proxy-url');
                            var href = target.getAttribute('href');
                            
                            if (proxyUrl || (href && href !== '#' && !href.startsWith('javascript:'))) {{
                                e.preventDefault();
                                e.stopPropagation();
                                
                                var navigateUrl = proxyUrl || href;
                                console.log('Kairo Browser: Intercepted link click to', navigateUrl);
                                
                                if (window.parent && window.parent.postMessage) {{
                                    window.parent.postMessage({{
                                        type: 'NAVIGATE_TO',
                                        url: navigateUrl
                                    }}, '*');
                                }}
                            }}
                        }}
                    }}, true);
                    
                    // Form submission interception
                    document.addEventListener('submit', function(e) {{
                        var form = e.target;
                        if (form && form.tagName === 'FORM') {{
                            var proxyAction = form.getAttribute('data-proxy-action');
                            if (proxyAction) {{
                                e.preventDefault();
                                
                                var formData = new FormData(form);
                                var params = new URLSearchParams();
                                for (var pair of formData.entries()) {{
                                    params.append(pair[0], pair[1]);
                                }}
                                
                                var finalUrl = proxyAction;
                                if (form.method.toLowerCase() === 'get' && params.toString()) {{
                                    finalUrl += (proxyAction.includes('?') ? '&' : '?') + params.toString();
                                }}
                                
                                if (window.parent && window.parent.postMessage) {{
                                    window.parent.postMessage({{
                                        type: 'NAVIGATE_TO',
                                        url: finalUrl
                                    }}, '*');
                                }}
                            }}
                        }}
                    }}, true);
                    
                    console.log('Kairo Browser: Enhanced navigation interception loaded');
                    
                }} catch (e) {{
                    console.log('Kairo Browser compatibility error:', e);
                }}
            }})();
        """
    
    def _clean_response_headers(self, headers) -> Dict[str, str]:
        """Clean response headers for iframe compatibility"""
        clean_headers = {}
        blocked_headers = ['x-frame-options', 'content-security-policy', 'x-content-type-options']
        
        for key, value in headers.items():
            if key.lower() not in blocked_headers:
                clean_headers[key] = value
        
        # Add iframe-friendly headers
        clean_headers['X-Frame-Options'] = 'ALLOWALL'
        clean_headers['Content-Security-Policy'] = "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:; frame-ancestors *;"
        
        return clean_headers
    
    async def _fallback_response(self, url: str, error: str) -> Dict[str, Any]:
        """Fallback response when all proxy methods fail"""
        fallback_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Kairo Browser - Content Loading</title>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
                    margin: 0;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-align: center;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                    max-width: 500px;
                }}
                .icon {{ font-size: 48px; margin-bottom: 20px; }}
                h1 {{ margin: 0 0 15px 0; font-size: 24px; }}
                p {{ margin: 10px 0; opacity: 0.9; }}
                .url {{ 
                    background: rgba(255, 255, 255, 0.2); 
                    padding: 10px; 
                    border-radius: 8px; 
                    word-break: break-all; 
                    font-family: monospace;
                }}
                .retry {{
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    cursor: pointer;
                    margin-top: 20px;
                    font-size: 16px;
                }}
                .retry:hover {{ background: #45a049; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="icon">🌐</div>
                <h1>Content Loading</h1>
                <p>Kairo Browser is working to load content from:</p>
                <div class="url">{url}</div>
                <p><small>If the site has restrictions, try using the AI assistant for alternative access methods.</small></p>
                <button class="retry" onclick="location.reload()">Retry Loading</button>
            </div>
        </body>
        </html>
        """
        
        return {
            "content": fallback_html,
            "status_code": 200,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "url": url,
            "method": "fallback",
            "iframe_safe": True,
            "error": error
        }

# Global proxy service instance
proxy_service = UltraProxyService()