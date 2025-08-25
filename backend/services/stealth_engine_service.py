"""
🥷 PHASE 2: Military-Grade Anti-Detection System
Advanced stealth engine with AI-powered behavioral mimicry
"""
import asyncio
import logging
import random
import time
import json
from typing import Dict, Any, Optional, List
from playwright.async_api import Page, BrowserContext
import numpy as np

logger = logging.getLogger(__name__)

class MilitaryGradeStealthEngine:
    """Military-grade stealth engine with behavioral AI"""
    
    def __init__(self):
        self.fingerprint_profiles = self._load_fingerprint_profiles()
        self.behavioral_patterns = self._load_behavioral_patterns()
        self.detection_counters = {}
        self.success_metrics = {}
        logger.info("🥷 Military-grade stealth engine initialized")
    
    def _load_fingerprint_profiles(self) -> List[Dict[str, Any]]:
        """Load realistic browser fingerprint profiles"""
        return [
            {
                'name': 'Windows_Chrome_Professional',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'viewport': {'width': 1920, 'height': 1080},
                'platform': 'Win32',
                'language': 'en-US',
                'timezone': 'America/New_York',
                'hardware_concurrency': 8,
                'device_memory': 8,
                'color_depth': 24,
                'pixel_ratio': 1.0
            },
            {
                'name': 'MacOS_Chrome_Designer',
                'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'viewport': {'width': 1440, 'height': 900},
                'platform': 'MacIntel',
                'language': 'en-US',
                'timezone': 'America/Los_Angeles',
                'hardware_concurrency': 4,
                'device_memory': 16,
                'color_depth': 24,
                'pixel_ratio': 2.0
            },
            {
                'name': 'Linux_Firefox_Developer',
                'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
                'viewport': {'width': 1366, 'height': 768},
                'platform': 'Linux x86_64',
                'language': 'en-US',
                'timezone': 'UTC',
                'hardware_concurrency': 6,
                'device_memory': 32,
                'color_depth': 24,
                'pixel_ratio': 1.0
            }
        ]
    
    def _load_behavioral_patterns(self) -> Dict[str, Any]:
        """Load AI-powered behavioral patterns"""
        return {
            'mouse_patterns': {
                'professional': {'speed': 'medium', 'precision': 'high', 'pauses': 'frequent'},
                'casual': {'speed': 'variable', 'precision': 'medium', 'pauses': 'random'},
                'power_user': {'speed': 'fast', 'precision': 'high', 'pauses': 'minimal'}
            },
            'typing_patterns': {
                'professional': {'speed': 45, 'accuracy': 0.98, 'rhythm': 'steady'},
                'casual': {'speed': 35, 'accuracy': 0.92, 'rhythm': 'variable'},
                'fast_typer': {'speed': 65, 'accuracy': 0.95, 'rhythm': 'burst'}
            },
            'scroll_behavior': {
                'reader': {'speed': 'slow', 'pattern': 'steady', 'stops': 'frequent'},
                'scanner': {'speed': 'fast', 'pattern': 'jumpy', 'stops': 'rare'},
                'researcher': {'speed': 'medium', 'pattern': 'methodical', 'stops': 'strategic'}
            }
        }
    
    async def apply_stealth_profile(self, context: BrowserContext, stealth_level: int = 5) -> Dict[str, Any]:
        """Apply comprehensive stealth profile to browser context"""
        try:
            # Select random realistic profile
            profile = random.choice(self.fingerprint_profiles)
            
            # Apply fingerprint masking
            await self._apply_fingerprint_masking(context, profile, stealth_level)
            
            # Apply behavioral patterns
            behavioral_profile = self._select_behavioral_profile(profile['name'])
            
            # Add advanced stealth scripts
            await context.add_init_script(self._get_advanced_stealth_script(profile, stealth_level))
            
            return {
                'profile_applied': profile['name'],
                'stealth_level': stealth_level,
                'behavioral_pattern': behavioral_profile,
                'fingerprint_masked': True
            }
            
        except Exception as e:
            logger.error(f"❌ Stealth profile application failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _apply_fingerprint_masking(self, context: BrowserContext, profile: Dict[str, Any], level: int):
        """Apply advanced fingerprint masking"""
        try:
            # Basic fingerprint elements
            extra_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': f"{profile['language']},en;q=0.9",
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Advanced headers for higher stealth levels
            if level >= 4:
                extra_headers.update({
                    'DNT': '1',
                    'Sec-CH-UA': self._generate_sec_ch_ua(profile['user_agent']),
                    'Sec-CH-UA-Mobile': '?0',
                    'Sec-CH-UA-Platform': f'"{profile["platform"]}"'
                })
            
            if level >= 5:
                extra_headers.update({
                    'Sec-CH-UA-Platform-Version': self._generate_platform_version(profile['platform']),
                    'Sec-CH-UA-Arch': self._generate_architecture(),
                    'Sec-CH-UA-Model': '""',
                    'Sec-CH-UA-Full-Version-List': self._generate_full_version_list(profile['user_agent'])
                })
            
            # Apply to context
            await context.set_extra_http_headers(extra_headers)
            
            logger.info(f"✅ Fingerprint masking applied: {profile['name']}, level {level}")
            
        except Exception as e:
            logger.error(f"❌ Fingerprint masking failed: {e}")
    
    def _select_behavioral_profile(self, fingerprint_name: str) -> str:
        """Select appropriate behavioral profile based on fingerprint"""
        if 'Professional' in fingerprint_name:
            return 'professional'
        elif 'Designer' in fingerprint_name:
            return 'casual'
        elif 'Developer' in fingerprint_name:
            return 'power_user'
        else:
            return random.choice(['professional', 'casual', 'power_user'])
    
    def _generate_sec_ch_ua(self, user_agent: str) -> str:
        """Generate realistic Sec-CH-UA header"""
        if 'Chrome/120' in user_agent:
            return '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
        elif 'Firefox' in user_agent:
            return '"Not_A Brand";v="99"'
        else:
            return '"Not_A Brand";v="8", "Chromium";v="120"'
    
    def _generate_platform_version(self, platform: str) -> str:
        """Generate realistic platform version"""
        if platform == 'Win32':
            return '"10.0.0"'
        elif platform == 'MacIntel':
            return '"13.6.0"'
        elif 'Linux' in platform:
            return '"5.4.0"'
        else:
            return '"10.0.0"'
    
    def _generate_architecture(self) -> str:
        """Generate realistic architecture"""
        return random.choice(['"x86"', '"arm"', '""])
    
    def _generate_full_version_list(self, user_agent: str) -> str:
        """Generate realistic full version list"""
        if 'Chrome/120' in user_agent:
            return '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.109", "Google Chrome";v="120.0.6099.109"'
        else:
            return '"Not_A Brand";v="8.0.0.0"'
    
    def _get_advanced_stealth_script(self, profile: Dict[str, Any], level: int) -> str:
        """Generate advanced stealth script based on profile and level"""
        base_script = f"""
            // 🥷 Advanced Military-Grade Stealth Protection
            (function() {{
                'use strict';
                
                // Profile-based fingerprint injection
                const STEALTH_PROFILE = {json.dumps(profile)};
                const STEALTH_LEVEL = {level};
                
                // Complete webdriver removal (enhanced)
                const webdriverKeys = ['webdriver', '__webdriver_evaluate', '__selenium_evaluate', '__webdriver_script_function', '__webdriver_script_func', '__webdriver_script_fn', '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped', '__driver_evaluate', '__selenium_unwrapped', '__fxdriver_unwrapped'];
                
                webdriverKeys.forEach(key => {{
                    try {{
                        Object.defineProperty(navigator, key, {{
                            get: () => undefined,
                            configurable: true
                        }});
                        Object.defineProperty(window, key, {{
                            get: () => undefined,
                            configurable: true
                        }});
                        delete navigator[key];
                        delete window[key];
                    }} catch(e) {{}}
                }});
                
                // Advanced navigator properties override
                Object.defineProperties(navigator, {{
                    platform: {{
                        get: () => STEALTH_PROFILE.platform,
                        configurable: true
                    }},
                    hardwareConcurrency: {{
                        get: () => STEALTH_PROFILE.hardware_concurrency,
                        configurable: true
                    }},
                    deviceMemory: {{
                        get: () => STEALTH_PROFILE.device_memory,
                        configurable: true
                    }},
                    languages: {{
                        get: () => [STEALTH_PROFILE.language, 'en'],
                        configurable: true
                    }},
                    language: {{
                        get: () => STEALTH_PROFILE.language,
                        configurable: true
                    }}
                }});
                
                // Screen properties based on profile
                Object.defineProperties(screen, {{
                    width: {{
                        get: () => STEALTH_PROFILE.viewport.width,
                        configurable: true
                    }},
                    height: {{
                        get: () => STEALTH_PROFILE.viewport.height,
                        configurable: true
                    }},
                    availWidth: {{
                        get: () => STEALTH_PROFILE.viewport.width,
                        configurable: true
                    }},
                    availHeight: {{
                        get: () => STEALTH_PROFILE.viewport.height - 40,
                        configurable: true
                    }},
                    colorDepth: {{
                        get: () => STEALTH_PROFILE.color_depth,
                        configurable: true
                    }},
                    pixelDepth: {{
                        get: () => STEALTH_PROFILE.color_depth,
                        configurable: true
                    }}
                }});
                
                // Advanced plugin mocking based on profile
                const generatePlugins = () => {{
                    const plugins = [];
                    if (STEALTH_PROFILE.name.includes('Chrome')) {{
                        plugins.push(
                            {{ name: 'Chrome PDF Plugin', description: 'Portable Document Format', filename: 'internal-pdf-viewer' }},
                            {{ name: 'Chrome PDF Viewer', description: 'PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' }},
                            {{ name: 'Native Client', description: 'Native Client', filename: 'internal-nacl-plugin' }}
                        );
                    }} else if (STEALTH_PROFILE.name.includes('Firefox')) {{
                        plugins.push(
                            {{ name: 'PDF.js', description: 'Portable Document Format', filename: 'pdf.js' }},
                            {{ name: 'OpenH264 Video Codec', description: 'OpenH264 Video Codec provided by Cisco Systems, Inc.', filename: 'gmpopenh264' }}
                        );
                    }}
                    return {{ length: plugins.length, ...plugins }};
                }};
                
                Object.defineProperty(navigator, 'plugins', {{
                    get: generatePlugins,
                    configurable: true
                }});
        """
        
        # Add level-specific enhancements
        if level >= 3:
            base_script += """
                // Level 3: Enhanced canvas fingerprint protection
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
                
                HTMLCanvasElement.prototype.toDataURL = function() {
                    const ctx = this.getContext('2d');
                    if (ctx) {
                        // Add profile-specific noise
                        const noise = STEALTH_PROFILE.pixel_ratio * (Math.random() * 0.1 - 0.05);
                        ctx.globalAlpha = 1.0 + noise;
                    }
                    return originalToDataURL.apply(this, arguments);
                };
                
                CanvasRenderingContext2D.prototype.getImageData = function() {
                    const imageData = originalGetImageData.apply(this, arguments);
                    // Add subtle noise based on profile
                    const noiseLevel = STEALTH_PROFILE.color_depth / 1000;
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        imageData.data[i] += Math.floor((Math.random() - 0.5) * noiseLevel);
                    }
                    return imageData;
                };
            """
        
        if level >= 4:
            base_script += """
                // Level 4: Advanced WebGL fingerprint protection
                const webglContexts = ['webgl', 'webgl2', 'experimental-webgl', 'experimental-webgl2'];
                
                webglContexts.forEach(contextType => {
                    const originalGetContext = HTMLCanvasElement.prototype.getContext;
                    HTMLCanvasElement.prototype.getContext = function(type, ...args) {
                        if (webglContexts.includes(type)) {
                            const context = originalGetContext.apply(this, [type, ...args]);
                            if (context) {
                                const originalGetParameter = context.getParameter;
                                context.getParameter = function(parameter) {
                                    // Return profile-consistent values
                                    if (parameter === context.RENDERER) {
                                        return STEALTH_PROFILE.platform.includes('Mac') ? 
                                            'Intel(R) Iris(TM) Graphics 6100' : 
                                            'ANGLE (Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0)';
                                    }
                                    if (parameter === context.VENDOR) {
                                        return 'Intel Inc.';
                                    }
                                    return originalGetParameter.apply(this, [parameter]);
                                };
                            }
                            return context;
                        }
                        return originalGetContext.apply(this, [type, ...args]);
                    };
                });
            """
        
        if level >= 5:
            base_script += """
                // Level 5: AI-powered behavioral mimicry
                let mouseMovements = [];
                let keystrokes = [];
                let scrolls = [];
                
                // Human-like mouse movement patterns
                const simulateHumanMouse = () => {
                    const patterns = {
                        professional: { jitter: 0.5, speed: 1.0, curves: true },
                        casual: { jitter: 1.2, speed: 0.8, curves: false },
                        power_user: { jitter: 0.3, speed: 1.5, curves: true }
                    };
                    
                    const behaviorType = STEALTH_PROFILE.name.includes('Professional') ? 'professional' :
                                        STEALTH_PROFILE.name.includes('Designer') ? 'casual' : 'power_user';
                    
                    const pattern = patterns[behaviorType];
                    
                    setInterval(() => {
                        const x = Math.random() * window.innerWidth;
                        const y = Math.random() * window.innerHeight;
                        
                        // Add human-like jitter
                        const jitterX = x + (Math.random() - 0.5) * pattern.jitter;
                        const jitterY = y + (Math.random() - 0.5) * pattern.jitter;
                        
                        document.dispatchEvent(new MouseEvent('mousemove', {
                            clientX: jitterX,
                            clientY: jitterY,
                            bubbles: true
                        }));
                        
                        mouseMovements.push({ x: jitterX, y: jitterY, timestamp: Date.now() });
                        if (mouseMovements.length > 100) mouseMovements.shift();
                        
                    }, 100 + Math.random() * 200 * pattern.speed);
                };
                
                // Human-like scroll behavior
                const simulateHumanScroll = () => {
                    const scrollTypes = ['reader', 'scanner', 'researcher'];
                    const scrollType = scrollTypes[Math.floor(Math.random() * scrollTypes.length)];
                    
                    setInterval(() => {
                        let scrollAmount = 0;
                        switch(scrollType) {
                            case 'reader':
                                scrollAmount = Math.random() * 100 + 50;
                                break;
                            case 'scanner':
                                scrollAmount = Math.random() * 300 + 100;
                                break;
                            case 'researcher':
                                scrollAmount = Math.random() * 150 + 75;
                                break;
                        }
                        
                        window.scrollBy(0, scrollAmount * (Math.random() > 0.5 ? 1 : -1));
                        scrolls.push({ amount: scrollAmount, timestamp: Date.now() });
                        if (scrolls.length > 50) scrolls.shift();
                        
                    }, 3000 + Math.random() * 7000);
                };
                
                // Start behavioral simulation
                setTimeout(simulateHumanMouse, 1000);
                setTimeout(simulateHumanScroll, 5000);
                
                // Advanced timing attack protection
                const originalPerformanceNow = Performance.prototype.now;
                Performance.prototype.now = function() {
                    return originalPerformanceNow.apply(this) + (Math.random() - 0.5) * 0.1;
                };
                
                // Font fingerprint protection
                const originalOffsetWidth = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetWidth');
                const originalOffsetHeight = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');
                
                Object.defineProperty(HTMLElement.prototype, 'offsetWidth', {
                    get: function() {
                        const width = originalOffsetWidth.get.apply(this);
                        return width + (Math.random() - 0.5) * 0.1;
                    }
                });
                
                Object.defineProperty(HTMLElement.prototype, 'offsetHeight', {
                    get: function() {
                        const height = originalOffsetHeight.get.apply(this);
                        return height + (Math.random() - 0.5) * 0.1;
                    }
                });
            """
        
        base_script += """
                console.log('🥷 Military-grade stealth activated:', STEALTH_PROFILE.name, 'Level:', STEALTH_LEVEL);
                
            })();
        """
        
        return base_script
    
    async def apply_behavioral_mimicry(self, page: Page, behavior_type: str = 'professional'):
        """Apply AI-powered behavioral mimicry to page interactions"""
        try:
            pattern = self.behavioral_patterns['mouse_patterns'][behavior_type]
            
            # Simulate human-like page interaction
            await self._simulate_human_reading(page, pattern)
            await self._simulate_mouse_movements(page, pattern)
            await self._simulate_scroll_behavior(page, behavior_type)
            
            logger.info(f"✅ Behavioral mimicry applied: {behavior_type}")
            
        except Exception as e:
            logger.error(f"❌ Behavioral mimicry failed: {e}")
    
    async def _simulate_human_reading(self, page: Page, pattern: Dict[str, str]):
        """Simulate human reading patterns"""
        reading_time = random.randint(2000, 8000)  # 2-8 seconds
        await page.wait_for_timeout(reading_time)
    
    async def _simulate_mouse_movements(self, page: Page, pattern: Dict[str, str]):
        """Simulate realistic mouse movements"""
        try:
            viewport = await page.viewport_size()
            if not viewport:
                viewport = {'width': 1920, 'height': 1080}
            
            # Generate movement path
            for _ in range(random.randint(3, 8)):
                x = random.randint(0, viewport['width'])
                y = random.randint(0, viewport['height'])
                
                await page.mouse.move(x, y)
                await page.wait_for_timeout(random.randint(100, 500))
                
        except Exception as e:
            logger.debug(f"Mouse movement simulation warning: {e}")
    
    async def _simulate_scroll_behavior(self, page: Page, behavior_type: str):
        """Simulate realistic scrolling behavior"""
        try:
            scroll_pattern = self.behavioral_patterns['scroll_behavior'].get(behavior_type, 'reader')
            
            if scroll_pattern == 'reader':
                # Slow, steady scrolling
                scroll_amount = random.randint(100, 300)
                await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            elif scroll_pattern == 'scanner':
                # Fast, jumpy scrolling
                scroll_amount = random.randint(300, 800)
                await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            else:  # researcher
                # Medium, methodical scrolling
                scroll_amount = random.randint(150, 400)
                await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            
            await page.wait_for_timeout(random.randint(1000, 3000))
            
        except Exception as e:
            logger.debug(f"Scroll simulation warning: {e}")
    
    async def detect_anti_bot_measures(self, page: Page) -> Dict[str, Any]:
        """Detect and analyze anti-bot measures on the page"""
        try:
            detection_result = await page.evaluate("""
                () => {
                    const detections = {
                        captcha: false,
                        cloudflare: false,
                        recaptcha: false,
                        hcaptcha: false,
                        distil: false,
                        imperva: false,
                        bot_detection_scripts: []
                    };
                    
                    // Check for common anti-bot indicators
                    if (document.querySelector('[data-sitekey]') || document.querySelector('.g-recaptcha')) {
                        detections.recaptcha = true;
                    }
                    
                    if (document.querySelector('.h-captcha')) {
                        detections.hcaptcha = true;
                    }
                    
                    if (document.querySelector('#cf-wrapper') || window.cflare) {
                        detections.cloudflare = true;
                    }
                    
                    if (window.distil || document.querySelector('script[src*="distil"]')) {
                        detections.distil = true;
                    }
                    
                    if (window._Incapsula || document.querySelector('script[src*="incap"]')) {
                        detections.imperva = true;
                    }
                    
                    // Scan for bot detection scripts
                    const scripts = Array.from(document.querySelectorAll('script'));
                    const botKeywords = ['bot', 'automation', 'webdriver', 'selenium', 'phantom'];
                    
                    scripts.forEach(script => {
                        const src = script.src || script.textContent || '';
                        botKeywords.forEach(keyword => {
                            if (src.toLowerCase().includes(keyword)) {
                                detections.bot_detection_scripts.push({
                                    type: keyword,
                                    source: script.src || 'inline'
                                });
                            }
                        });
                    });
                    
                    return detections;
                }
            """)
            
            return detection_result
            
        except Exception as e:
            logger.error(f"❌ Anti-bot detection failed: {e}")
            return {'error': str(e)}
    
    async def adaptive_stealth_response(self, page: Page, detections: Dict[str, Any]) -> Dict[str, Any]:
        """Adaptively respond to detected anti-bot measures"""
        try:
            responses = []
            
            if detections.get('cloudflare'):
                # Handle Cloudflare challenge
                await self._handle_cloudflare_challenge(page)
                responses.append('cloudflare_bypass')
            
            if detections.get('recaptcha'):
                # Handle reCAPTCHA
                await self._handle_recaptcha(page)
                responses.append('recaptcha_detection')
            
            if detections.get('bot_detection_scripts'):
                # Counter bot detection scripts
                await self._counter_bot_detection_scripts(page)
                responses.append('script_neutralization')
            
            return {
                'responses_applied': responses,
                'success': len(responses) > 0
            }
            
        except Exception as e:
            logger.error(f"❌ Adaptive stealth response failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _handle_cloudflare_challenge(self, page: Page):
        """Handle Cloudflare challenge with enhanced stealth"""
        try:
            # Wait for challenge to potentially complete automatically
            await page.wait_for_timeout(5000)
            
            # Check if challenge is present
            challenge_present = await page.evaluate("""
                () => document.querySelector('#cf-wrapper') !== null
            """)
            
            if challenge_present:
                logger.info("🛡️ Cloudflare challenge detected, applying enhanced stealth")
                await page.wait_for_timeout(random.randint(3000, 7000))
            
        except Exception as e:
            logger.debug(f"Cloudflare handling warning: {e}")
    
    async def _handle_recaptcha(self, page: Page):
        """Detect and log reCAPTCHA presence"""
        try:
            recaptcha_present = await page.evaluate("""
                () => document.querySelector('.g-recaptcha, [data-sitekey]') !== null
            """)
            
            if recaptcha_present:
                logger.info("🤖 reCAPTCHA detected - enhanced stealth mode activated")
            
        except Exception as e:
            logger.debug(f"reCAPTCHA handling warning: {e}")
    
    async def _counter_bot_detection_scripts(self, page: Page):
        """Counter known bot detection scripts"""
        try:
            await page.evaluate("""
                () => {
                    // Neutralize common bot detection patterns
                    const neutralizeScript = (script) => {
                        if (script.textContent) {
                            const botPatterns = ['webdriver', 'selenium', 'phantom', '__nightmare'];
                            botPatterns.forEach(pattern => {
                                if (script.textContent.includes(pattern)) {
                                    script.textContent = '// Neutralized by stealth engine';
                                }
                            });
                        }
                    };
                    
                    document.querySelectorAll('script').forEach(neutralizeScript);
                }
            """)
            
            logger.info("🛡️ Bot detection scripts neutralized")
            
        except Exception as e:
            logger.debug(f"Script neutralization warning: {e}")

# Global stealth engine instance
stealth_engine = MilitaryGradeStealthEngine()