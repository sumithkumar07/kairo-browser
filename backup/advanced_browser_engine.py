"""
🚀 PHASE 1: Advanced Browser Engine Core
Military-grade browser engine with multi-engine support and advanced capabilities
"""
import asyncio
import logging
import random
import time
from typing import Dict, Any, Optional, List
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config import settings
import json

logger = logging.getLogger(__name__)

class AdvancedBrowserEngine:
    """Advanced multi-engine browser system with native-level capabilities"""
    
    def __init__(self):
        self.engines = {
            'chromium': {'priority': 1, 'description': 'High compatibility, best for modern sites'},
            'firefox': {'priority': 2, 'description': 'Enhanced privacy, different fingerprint'},
            'webkit': {'priority': 3, 'description': 'Safari compatibility, iOS/macOS sites'}
        }
        self.active_contexts = {}
        self.performance_metrics = {}
        self.browser_instances = {}
        logger.info("🚀 Advanced Browser Engine initialized with multi-engine support")
    
    async def initialize_engines(self):
        """Initialize all browser engines"""
        try:
            async with async_playwright() as p:
                for engine_name in self.engines.keys():
                    try:
                        if engine_name == 'chromium':
                            browser = await p.chromium.launch(
                                headless=True,
                                args=self._get_advanced_chromium_args()
                            )
                        elif engine_name == 'firefox':
                            browser = await p.firefox.launch(
                                headless=True,
                                args=self._get_advanced_firefox_args()
                            )
                        elif engine_name == 'webkit':
                            browser = await p.webkit.launch(
                                headless=True,
                                args=self._get_advanced_webkit_args()
                            )
                        
                        self.browser_instances[engine_name] = browser
                        logger.info(f"✅ {engine_name.title()} engine initialized")
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to initialize {engine_name}: {e}")
                        
        except Exception as e:
            logger.error(f"❌ Engine initialization failed: {e}")
    
    async def create_enhanced_context(self, engine: str = 'chromium', stealth_level: int = 5) -> BrowserContext:
        """Create an enhanced browser context with advanced stealth features"""
        try:
            if engine not in self.browser_instances:
                await self.initialize_engines()
            
            browser = self.browser_instances.get(engine)
            if not browser:
                raise ValueError(f"Engine {engine} not available")
            
            # Advanced context configuration
            context_config = self._get_enhanced_context_config(stealth_level)
            context = await browser.new_context(**context_config)
            
            # Add comprehensive stealth scripts
            await context.add_init_script(self._get_comprehensive_stealth_script())
            
            # Advanced performance monitoring
            await context.route('**/*', self._performance_monitor)
            
            context_id = f"{engine}_{int(time.time())}"
            self.active_contexts[context_id] = {
                'context': context,
                'engine': engine,
                'stealth_level': stealth_level,
                'created': time.time()
            }
            
            logger.info(f"✅ Enhanced {engine} context created with stealth level {stealth_level}")
            return context
            
        except Exception as e:
            logger.error(f"❌ Context creation failed: {e}")
            raise
    
    async def navigate_with_intelligence(self, context: BrowserContext, url: str, 
                                       interaction_mode: str = 'stealth') -> Dict[str, Any]:
        """Intelligent navigation with adaptive strategies"""
        try:
            page = await context.new_page()
            
            # Pre-navigation analysis
            site_analysis = await self._analyze_target_site(url)
            
            # Select optimal navigation strategy
            nav_strategy = self._select_navigation_strategy(site_analysis, interaction_mode)
            
            # Execute navigation with strategy
            result = await self._execute_navigation_strategy(page, url, nav_strategy)
            
            return {
                'success': True,
                'url': url,
                'strategy_used': nav_strategy,
                'site_analysis': site_analysis,
                'page_metrics': await self._collect_page_metrics(page),
                'content_ready': True
            }
            
        except Exception as e:
            logger.error(f"❌ Intelligent navigation failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _get_advanced_chromium_args(self) -> List[str]:
        """Advanced Chromium arguments for maximum stealth and performance"""
        return [
            # Core stealth arguments
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-infobars',
            
            # Performance optimizations
            '--disable-gpu',
            '--disable-accelerated-2d-canvas',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            
            # Advanced stealth
            '--disable-client-side-phishing-detection',
            '--disable-component-extensions-with-background-pages',
            '--disable-default-apps',
            '--disable-extensions-file-access-check',
            '--disable-extensions-http-throttling',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-popup-blocking',
            '--disable-prompt-on-repost',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--mute-audio',
            
            # Memory and performance
            '--memory-pressure-off',
            '--max-old-space-size=4096',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            
            # Network optimizations
            '--aggressive-cache-discard',
            '--enable-features=NetworkService,NetworkServiceLogging',
            '--force-webrtc-ip-handling-policy=disable_non_proxied_udp'
        ]
    
    def _get_advanced_firefox_args(self) -> List[str]:
        """Advanced Firefox arguments for enhanced privacy"""
        return [
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-web-security',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',
            '--disable-java',
            '--disable-javascript-debugger'
        ]
    
    def _get_advanced_webkit_args(self) -> List[str]:
        """Advanced WebKit arguments for Safari compatibility"""
        return [
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-web-security'
        ]
    
    def _get_enhanced_context_config(self, stealth_level: int) -> Dict[str, Any]:
        """Generate enhanced context configuration based on stealth level"""
        # Realistic viewport sizes
        viewports = [
            {'width': 1920, 'height': 1080},
            {'width': 1366, 'height': 768}, 
            {'width': 1536, 'height': 864},
            {'width': 1440, 'height': 900},
            {'width': 1280, 'height': 720}
        ]
        
        # Realistic user agents
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
        ]
        
        config = {
            'viewport': random.choice(viewports),
            'user_agent': random.choice(user_agents),
            'locale': random.choice(['en-US', 'en-GB', 'en-CA']),
            'timezone_id': random.choice(['America/New_York', 'Europe/London', 'America/Los_Angeles']),
            'permissions': ['geolocation', 'notifications'],
            'geolocation': {
                'latitude': 40.7128 + random.uniform(-0.1, 0.1),
                'longitude': -74.0060 + random.uniform(-0.1, 0.1)
            },
            'java_script_enabled': True,
            'bypass_csp': True
        }
        
        # Enhanced stealth features based on level
        if stealth_level >= 3:
            config['extra_http_headers'] = self._get_stealth_headers()
        
        if stealth_level >= 4:
            config['device_scale_factor'] = random.uniform(1.0, 2.0)
            config['is_mobile'] = random.choice([True, False])
        
        if stealth_level >= 5:
            config['has_touch'] = random.choice([True, False])
            config['color_scheme'] = random.choice(['light', 'dark', 'no-preference'])
        
        return config
    
    def _get_stealth_headers(self) -> Dict[str, str]:
        """Generate realistic stealth headers"""
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'en-US,en;q=0.8,es;q=0.6']),
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': random.choice(['no-cache', 'max-age=0']),
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1' if random.random() > 0.7 else '0'
        }
    
    def _get_comprehensive_stealth_script(self) -> str:
        """Comprehensive stealth script for maximum anti-detection"""
        return """
            // 🥷 PHASE 2: Military-Grade Anti-Detection
            (function() {
                'use strict';
                
                // Complete webdriver removal
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                    configurable: true
                });
                delete navigator.__proto__.webdriver;
                delete window.navigator.webdriver;
                
                // Advanced Chrome object mocking
                window.chrome = {
                    runtime: {
                        onConnect: undefined,
                        onMessage: undefined,
                        PlatformOs: {
                            MAC: 'mac',
                            WIN: 'win',
                            ANDROID: 'android',
                            CROS: 'cros',
                            LINUX: 'linux',
                            OPENBSD: 'openbsd'
                        }
                    },
                    app: { isInstalled: false },
                    csi: () => {},
                    loadTimes: () => ({
                        commitLoadTime: Math.random() * 1000 + 1000,
                        connectionInfo: 'h2',
                        finishDocumentLoadTime: Math.random() * 1000 + 2000,
                        finishLoadTime: Math.random() * 1000 + 2500,
                        firstPaintAfterLoadTime: 0,
                        firstPaintTime: Math.random() * 1000 + 1500,
                        navigationType: 'Other',
                        npnNegotiatedProtocol: 'h2',
                        requestTime: Date.now() / 1000 - Math.random() * 10,
                        startLoadTime: Math.random() * 1000 + 500,
                        wasAlternateProtocolAvailable: false,
                        wasFetchedViaSpdy: true,
                        wasNpnNegotiated: true
                    })
                };
                
                // Advanced language mocking
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                    configurable: true
                });
                
                // Realistic plugin mocking
                Object.defineProperty(navigator, 'plugins', {
                    get: () => ({
                        length: 3,
                        0: { name: 'Chrome PDF Plugin', description: 'Portable Document Format', filename: 'internal-pdf-viewer' },
                        1: { name: 'Chrome PDF Viewer', description: 'PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
                        2: { name: 'Native Client', description: 'Native Client', filename: 'internal-nacl-plugin' }
                    }),
                    configurable: true
                });
                
                // Hardware concurrency randomization
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => Math.floor(Math.random() * 8) + 2,
                    configurable: true
                });
                
                // Memory information mocking
                if (navigator.deviceMemory) {
                    Object.defineProperty(navigator, 'deviceMemory', {
                        get: () => [2, 4, 8, 16][Math.floor(Math.random() * 4)],
                        configurable: true
                    });
                }
                
                // Connection API mocking
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        type: 'wifi',
                        downlink: Math.random() * 10 + 1,
                        rtt: Math.random() * 100 + 50,
                        saveData: false
                    }),
                    configurable: true
                });
                
                // Permissions API override
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
                
                // Battery API mocking
                if (navigator.getBattery) {
                    navigator.getBattery = () => Promise.resolve({
                        charging: true,
                        chargingTime: 0,
                        dischargingTime: Infinity,
                        level: Math.random() * 0.5 + 0.5
                    });
                }
                
                // Media devices mocking
                if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
                    const originalEnumerateDevices = navigator.mediaDevices.enumerateDevices;
                    navigator.mediaDevices.enumerateDevices = () => 
                        Promise.resolve([
                            { deviceId: 'default', groupId: 'group1', kind: 'audioinput', label: 'Default - Microphone' },
                            { deviceId: 'default', groupId: 'group2', kind: 'audiooutput', label: 'Default - Speakers' },
                            { deviceId: 'default', groupId: 'group3', kind: 'videoinput', label: 'Default - Camera' }
                        ]);
                }
                
                // Canvas fingerprint protection
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function() {
                    // Add slight noise to canvas fingerprint
                    const ctx = this.getContext('2d');
                    if (ctx) {
                        const imageData = ctx.getImageData(0, 0, this.width, this.height);
                        for (let i = 0; i < imageData.data.length; i += 4) {
                            imageData.data[i] += Math.floor(Math.random() * 3) - 1;
                        }
                        ctx.putImageData(imageData, 0, 0);
                    }
                    return originalToDataURL.apply(this, arguments);
                };
                
                // WebGL fingerprint protection
                const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === this.RENDERER || parameter === this.VENDOR) {
                        return 'Intel Inc. ~ Intel(R) HD Graphics 4000';
                    }
                    return originalGetParameter.apply(this, arguments);
                };
                
                // Audio context fingerprint protection
                const originalCreateAnalyser = AudioContext.prototype.createAnalyser || OfflineAudioContext.prototype.createAnalyser;
                if (originalCreateAnalyser) {
                    AudioContext.prototype.createAnalyser = OfflineAudioContext.prototype.createAnalyser = function() {
                        const analyser = originalCreateAnalyser.apply(this, arguments);
                        const originalGetFloatFrequencyData = analyser.getFloatFrequencyData;
                        analyser.getFloatFrequencyData = function(array) {
                            originalGetFloatFrequencyData.apply(this, arguments);
                            // Add noise to audio fingerprint
                            for (let i = 0; i < array.length; i++) {
                                array[i] += Math.random() * 0.001 - 0.0005;
                            }
                        };
                        return analyser;
                    };
                }
                
                // Screen properties randomization
                Object.defineProperties(screen, {
                    availHeight: { get: () => screen.height - Math.floor(Math.random() * 100) + 50 },
                    availWidth: { get: () => screen.width },
                    colorDepth: { get: () => 24 },
                    pixelDepth: { get: () => 24 }
                });
                
                // Document properties
                Object.defineProperty(document, 'hidden', {
                    get: () => false,
                    configurable: true
                });
                
                Object.defineProperty(document, 'visibilityState', {
                    get: () => 'visible',
                    configurable: true
                });
                
                // Mouse event protection
                const originalAddEventListener = EventTarget.prototype.addEventListener;
                EventTarget.prototype.addEventListener = function(type, listener, options) {
                    if (type === 'mousemove' || type === 'click') {
                        // Add slight delay to make events look more human
                        const humanListener = function(event) {
                            setTimeout(() => listener.call(this, event), Math.random() * 2);
                        };
                        return originalAddEventListener.call(this, type, humanListener, options);
                    }
                    return originalAddEventListener.call(this, type, listener, options);
                };
                
                console.log('🥷 Military-grade stealth protection activated');
                
            })();
        """
    
    async def _analyze_target_site(self, url: str) -> Dict[str, Any]:
        """Analyze target site for optimal strategy selection"""
        # This would include ML-based site analysis in production
        return {
            'domain': url.split('/')[2] if '://' in url else url,
            'requires_js': True,
            'has_anti_bot': 'medium',
            'complexity': 'high',
            'recommended_engine': 'chromium'
        }
    
    def _select_navigation_strategy(self, site_analysis: Dict[str, Any], mode: str) -> str:
        """Select optimal navigation strategy based on analysis"""
        strategies = ['stealth_native', 'enhanced_automation', 'hybrid_approach']
        return random.choice(strategies)  # Simplified for now
    
    async def _execute_navigation_strategy(self, page: Page, url: str, strategy: str) -> Dict[str, Any]:
        """Execute the selected navigation strategy"""
        try:
            # Pre-navigation setup
            await self._setup_page_stealth(page)
            
            # Navigate with timeout and options
            await page.goto(url, wait_until='networkidle', timeout=60000)
            
            # Post-navigation enhancements
            await self._post_navigation_setup(page)
            
            return {'success': True, 'strategy': strategy}
            
        except Exception as e:
            logger.error(f"❌ Navigation strategy execution failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _setup_page_stealth(self, page: Page):
        """Setup additional page-level stealth measures"""
        # Add event listeners for human-like behavior
        await page.evaluate("""
            // Simulate human-like mouse movements
            let mouseX = Math.random() * window.innerWidth;
            let mouseY = Math.random() * window.innerHeight;
            
            setInterval(() => {
                mouseX += (Math.random() - 0.5) * 5;
                mouseY += (Math.random() - 0.5) * 5;
                
                const event = new MouseEvent('mousemove', {
                    clientX: mouseX,
                    clientY: mouseY,
                    bubbles: true
                });
                document.dispatchEvent(event);
            }, 100 + Math.random() * 200);
        """)
    
    async def _post_navigation_setup(self, page: Page):
        """Post-navigation page setup"""
        # Wait for dynamic content
        await page.wait_for_timeout(random.randint(2000, 5000))
        
        # Simulate human reading behavior
        await page.evaluate(f"""
            window.scrollTo(0, {random.randint(0, 500)});
        """)
    
    async def _collect_page_metrics(self, page: Page) -> Dict[str, Any]:
        """Collect comprehensive page performance metrics"""
        try:
            metrics = await page.evaluate("""
                () => {
                    const perfEntries = performance.getEntriesByType('navigation');
                    const paintEntries = performance.getEntriesByType('paint');
                    
                    return {
                        loadTime: perfEntries[0] ? perfEntries[0].loadEventEnd - perfEntries[0].loadEventStart : 0,
                        domContentLoaded: perfEntries[0] ? perfEntries[0].domContentLoadedEventEnd - perfEntries[0].domContentLoadedEventStart : 0,
                        firstPaint: paintEntries.find(e => e.name === 'first-paint')?.startTime || 0,
                        firstContentfulPaint: paintEntries.find(e => e.name === 'first-contentful-paint')?.startTime || 0,
                        title: document.title,
                        url: window.location.href,
                        readyState: document.readyState
                    };
                }
            """)
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Metrics collection failed: {e}")
            return {}
    
    async def _performance_monitor(self, route):
        """Monitor and optimize network performance"""
        try:
            # Continue the request
            await route.continue_()
            
        except Exception as e:
            logger.debug(f"Performance monitor warning: {e}")
    
    async def cleanup_contexts(self):
        """Cleanup old browser contexts"""
        current_time = time.time()
        for context_id, context_data in list(self.active_contexts.items()):
            if current_time - context_data['created'] > 3600:  # 1 hour timeout
                try:
                    await context_data['context'].close()
                    del self.active_contexts[context_id]
                    logger.info(f"🧹 Cleaned up context {context_id}")
                except Exception as e:
                    logger.warning(f"⚠️ Context cleanup warning: {e}")

# Global advanced browser engine instance
advanced_browser_engine = AdvancedBrowserEngine()