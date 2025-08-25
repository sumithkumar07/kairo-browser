"""
🎯 PHASE 3: Real Website Interaction Engine
Advanced real-time website interaction with native browser capabilities
"""
import asyncio
import logging
import random
import time
import json
from typing import Dict, Any, Optional, List, Union
from playwright.async_api import Page, ElementHandle, Locator
import re

logger = logging.getLogger(__name__)

class RealWebsiteInteractionEngine:
    """Real-time website interaction engine with human-like behavior"""
    
    def __init__(self):
        self.interaction_history = []
        self.element_cache = {}
        self.interaction_patterns = self._load_interaction_patterns()
        self.smart_selectors = self._load_smart_selectors()
        logger.info("🎯 Real Website Interaction Engine initialized")
    
    def _load_interaction_patterns(self) -> Dict[str, Any]:
        """Load human-like interaction patterns"""
        return {
            'click_patterns': {
                'professional': {'delay_before': 500, 'delay_after': 300, 'precision': 'high'},
                'casual': {'delay_before': 800, 'delay_after': 600, 'precision': 'medium'},
                'fast_user': {'delay_before': 200, 'delay_after': 100, 'precision': 'high'}
            },
            'typing_patterns': {
                'professional': {'wpm': 45, 'error_rate': 0.02, 'thinking_pauses': True},
                'casual': {'wpm': 35, 'error_rate': 0.05, 'thinking_pauses': True},
                'fast_typer': {'wpm': 65, 'error_rate': 0.03, 'thinking_pauses': False}
            },
            'scroll_patterns': {
                'reader': {'speed': 'slow', 'direction': 'down', 'pauses': 'frequent'},
                'scanner': {'speed': 'fast', 'direction': 'variable', 'pauses': 'rare'},
                'researcher': {'speed': 'medium', 'direction': 'strategic', 'pauses': 'context-based'}
            }
        }
    
    def _load_smart_selectors(self) -> Dict[str, List[str]]:
        """Load smart selectors for common elements"""
        return {
            'buttons': [
                'button', 'input[type="button"]', 'input[type="submit"]', 
                '[role="button"]', '.btn', '.button', '[onclick]'
            ],
            'links': [
                'a[href]', '[role="link"]', '.link'
            ],
            'inputs': [
                'input[type="text"]', 'input[type="email"]', 'input[type="password"]',
                'textarea', '[contenteditable="true"]'
            ],
            'search_boxes': [
                'input[type="search"]', 'input[name*="search"]', 'input[placeholder*="search"]',
                'input[class*="search"]', 'input[id*="search"]'
            ],
            'forms': [
                'form', '[role="form"]'
            ],
            'navigation': [
                'nav', '.navigation', '.nav', '.menu', '[role="navigation"]'
            ],
            'content': [
                'main', '[role="main"]', '.content', '.main-content', 'article'
            ]
        }
    
    async def intelligent_click(self, page: Page, selector: str, 
                               behavior_type: str = 'professional',
                               wait_strategy: str = 'smart') -> Dict[str, Any]:
        """Perform intelligent click with human-like behavior"""
        try:
            # Find element with smart waiting
            element = await self._smart_element_finder(page, selector, wait_strategy)
            if not element:
                return {'success': False, 'error': 'Element not found'}
            
            # Pre-click analysis
            element_info = await self._analyze_element(element)
            
            # Apply behavioral pattern
            pattern = self.interaction_patterns['click_patterns'][behavior_type]
            
            # Pre-click delay (human thinking time)
            await page.wait_for_timeout(random.randint(200, pattern['delay_before']))
            
            # Get element position for precise clicking
            box = await element.bounding_box()
            if box:
                # Calculate click position with human-like variation
                click_x = box['x'] + box['width'] / 2
                click_y = box['y'] + box['height'] / 2
                
                if pattern['precision'] == 'medium':
                    click_x += random.uniform(-5, 5)
                    click_y += random.uniform(-5, 5)
                elif pattern['precision'] == 'low':
                    click_x += random.uniform(-10, 10)
                    click_y += random.uniform(-10, 10)
                
                # Perform human-like mouse movement and click
                await page.mouse.move(click_x, click_y)
                await page.wait_for_timeout(random.randint(50, 150))
                await page.mouse.click(click_x, click_y)
            else:
                # Fallback to element click
                await element.click(force=True)
            
            # Post-click delay
            await page.wait_for_timeout(random.randint(100, pattern['delay_after']))
            
            # Record interaction
            self._record_interaction('click', selector, element_info, behavior_type)
            
            return {
                'success': True,
                'element_info': element_info,
                'behavior_applied': behavior_type,
                'click_position': {'x': click_x, 'y': click_y} if box else None
            }
            
        except Exception as e:
            logger.error(f"❌ Intelligent click failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def human_like_typing(self, page: Page, selector: str, text: str,
                               behavior_type: str = 'professional',
                               clear_first: bool = True) -> Dict[str, Any]:
        """Perform human-like typing with realistic patterns"""
        try:
            # Find input element
            element = await self._smart_element_finder(page, selector, 'input')
            if not element:
                return {'success': False, 'error': 'Input element not found'}
            
            # Focus on element first
            await element.focus()
            await page.wait_for_timeout(random.randint(100, 300))
            
            # Clear existing content if requested
            if clear_first:
                await element.fill('')
                await page.wait_for_timeout(random.randint(50, 150))
            
            # Get typing pattern
            pattern = self.interaction_patterns['typing_patterns'][behavior_type]
            
            # Calculate typing delays
            base_delay = 60000 / pattern['wpm'] / 5  # Convert WPM to delay between characters
            
            # Type character by character with human-like rhythm
            typed_text = ""
            for i, char in enumerate(text):
                # Add thinking pauses for complex words
                if pattern['thinking_pauses'] and char in [' ', '.', ',', '!', '?']:
                    await page.wait_for_timeout(random.randint(200, 800))
                
                # Simulate typing errors occasionally
                if random.random() < pattern['error_rate']:
                    # Type wrong character, then correct it
                    wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                    await element.type(wrong_char)
                    await page.wait_for_timeout(random.randint(100, 300))
                    await page.keyboard.press('Backspace')
                    await page.wait_for_timeout(random.randint(50, 200))
                
                # Type the correct character
                await element.type(char)
                typed_text += char
                
                # Variable delay between characters
                char_delay = base_delay + random.uniform(-base_delay * 0.3, base_delay * 0.5)
                await page.wait_for_timeout(int(char_delay))
                
                # Longer pauses for word boundaries
                if char == ' ':
                    await page.wait_for_timeout(random.randint(50, 200))
            
            # Record interaction
            self._record_interaction('type', selector, {'text_length': len(text)}, behavior_type)
            
            return {
                'success': True,
                'typed_text': typed_text,
                'behavior_applied': behavior_type,
                'typing_speed': pattern['wpm']
            }
            
        except Exception as e:
            logger.error(f"❌ Human-like typing failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def intelligent_scroll(self, page: Page, direction: str = 'down',
                                amount: Optional[int] = None,
                                behavior_type: str = 'reader') -> Dict[str, Any]:
        """Perform intelligent scrolling with human-like patterns"""
        try:
            pattern = self.interaction_patterns['scroll_patterns'][behavior_type]
            
            # Determine scroll amount based on behavior
            if amount is None:
                if pattern['speed'] == 'slow':
                    amount = random.randint(100, 300)
                elif pattern['speed'] == 'fast':
                    amount = random.randint(400, 800)
                else:  # medium
                    amount = random.randint(200, 500)
            
            # Determine direction
            if direction == 'auto':
                direction = 'down' if random.random() > 0.2 else 'up'
            
            # Apply scroll direction
            scroll_delta = amount if direction == 'down' else -amount
            
            # Perform scroll with human-like acceleration
            steps = random.randint(3, 8)
            step_size = scroll_delta / steps
            
            for step in range(steps):
                # Variable step size for natural feel
                current_step = step_size + random.uniform(-step_size * 0.2, step_size * 0.2)
                await page.evaluate(f'window.scrollBy(0, {current_step})')
                
                # Variable delay between scroll steps
                delay = random.randint(20, 100)
                await page.wait_for_timeout(delay)
            
            # Pause after scrolling (reading/scanning time)
            if pattern['pauses'] == 'frequent':
                pause_time = random.randint(1000, 3000)
            elif pattern['pauses'] == 'rare':
                pause_time = random.randint(100, 500)
            else:  # context-based
                pause_time = random.randint(500, 1500)
            
            await page.wait_for_timeout(pause_time)
            
            # Record interaction
            self._record_interaction('scroll', f'{direction}_{amount}px', 
                                   {'direction': direction, 'amount': amount}, behavior_type)
            
            return {
                'success': True,
                'scroll_amount': amount,
                'direction': direction,
                'behavior_applied': behavior_type
            }
            
        except Exception as e:
            logger.error(f"❌ Intelligent scroll failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def smart_form_filling(self, page: Page, form_data: Dict[str, str],
                                behavior_type: str = 'professional') -> Dict[str, Any]:
        """Fill forms intelligently with human-like behavior"""
        try:
            filled_fields = []
            
            for field_name, value in form_data.items():
                # Try multiple strategies to find the field
                field_selectors = [
                    f'[name="{field_name}"]',
                    f'[id="{field_name}"]', 
                    f'[placeholder*="{field_name}"]',
                    f'[class*="{field_name}"]',
                    f'label:has-text("{field_name}") + input',
                    f'label:has-text("{field_name}") input'
                ]
                
                field_found = False
                for selector in field_selectors:
                    try:
                        element = await page.locator(selector).first
                        if await element.is_visible():
                            # Human-like delay before focusing on field
                            await page.wait_for_timeout(random.randint(300, 800))
                            
                            # Fill the field with human-like typing
                            result = await self.human_like_typing(page, selector, value, behavior_type)
                            
                            if result['success']:
                                filled_fields.append({
                                    'field': field_name,
                                    'selector': selector,
                                    'value_length': len(value)
                                })
                                field_found = True
                                break
                                
                    except Exception as e:
                        logger.debug(f"Field selector {selector} failed: {e}")
                        continue
                
                if not field_found:
                    logger.warning(f"⚠️ Could not find field: {field_name}")
            
            return {
                'success': True,
                'filled_fields': filled_fields,
                'total_fields': len(form_data),
                'success_rate': len(filled_fields) / len(form_data) if form_data else 0
            }
            
        except Exception as e:
            logger.error(f"❌ Smart form filling failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def extract_page_data(self, page: Page, extraction_rules: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured data from page using intelligent selectors"""
        try:
            extracted_data = {}
            
            for data_key, rule in extraction_rules.items():
                try:
                    if isinstance(rule, str):
                        # Simple selector
                        element = await page.locator(rule).first
                        if await element.is_visible():
                            extracted_data[data_key] = await element.inner_text()
                    
                    elif isinstance(rule, dict):
                        # Complex extraction rule
                        selector = rule.get('selector')
                        attribute = rule.get('attribute', 'text')
                        multiple = rule.get('multiple', False)
                        
                        if multiple:
                            elements = await page.locator(selector).all()
                            values = []
                            for elem in elements:
                                if attribute == 'text':
                                    value = await elem.inner_text()
                                else:
                                    value = await elem.get_attribute(attribute)
                                if value:
                                    values.append(value.strip())
                            extracted_data[data_key] = values
                        else:
                            element = await page.locator(selector).first
                            if await element.is_visible():
                                if attribute == 'text':
                                    extracted_data[data_key] = await element.inner_text()
                                else:
                                    extracted_data[data_key] = await element.get_attribute(attribute)
                
                except Exception as e:
                    logger.debug(f"Extraction failed for {data_key}: {e}")
                    extracted_data[data_key] = None
            
            return {
                'success': True,
                'extracted_data': extracted_data,
                'extraction_rate': len([v for v in extracted_data.values() if v is not None]) / len(extraction_rules)
            }
            
        except Exception as e:
            logger.error(f"❌ Page data extraction failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def wait_for_dynamic_content(self, page: Page, 
                                     content_indicators: List[str],
                                     timeout: int = 30000) -> Dict[str, Any]:
        """Wait for dynamic content to load with intelligent detection"""
        try:
            start_time = time.time()
            
            # Wait strategies
            strategies = [
                # Wait for network idle
                lambda: page.wait_for_load_state('networkidle', timeout=10000),
                # Wait for specific elements
                lambda: self._wait_for_any_element(page, content_indicators, timeout=10000),
                # Wait for JavaScript completion
                lambda: self._wait_for_js_completion(page, timeout=10000)
            ]
            
            # Try strategies in parallel
            completed_strategies = []
            for i, strategy in enumerate(strategies):
                try:
                    await strategy()
                    completed_strategies.append(f'strategy_{i+1}')
                except Exception as e:
                    logger.debug(f"Strategy {i+1} failed: {e}")
            
            # Additional smart waiting based on page complexity
            await self._smart_content_wait(page)
            
            total_time = (time.time() - start_time) * 1000
            
            return {
                'success': True,
                'wait_time_ms': total_time,
                'strategies_completed': completed_strategies,
                'content_ready': True
            }
            
        except Exception as e:
            logger.error(f"❌ Dynamic content wait failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _smart_element_finder(self, page: Page, selector: str, 
                                   element_type: str = 'any') -> Optional[ElementHandle]:
        """Smart element finder with fallback strategies"""
        try:
            # Try direct selector first
            try:
                element = await page.locator(selector).first
                if await element.is_visible():
                    return element
            except:
                pass
            
            # Try smart selectors based on element type
            if element_type in self.smart_selectors:
                for smart_selector in self.smart_selectors[element_type]:
                    try:
                        # Combine with partial selector match
                        combined_selector = f'{smart_selector}:has-text("{selector}")'
                        element = await page.locator(combined_selector).first
                        if await element.is_visible():
                            return element
                    except:
                        continue
            
            # Try text-based search
            try:
                element = await page.locator(f'text="{selector}"').first
                if await element.is_visible():
                    return element
            except:
                pass
            
            # Try partial text match
            try:
                element = await page.locator(f'text*="{selector}"').first
                if await element.is_visible():
                    return element
            except:
                pass
            
            return None
            
        except Exception as e:
            logger.debug(f"Smart element finder error: {e}")
            return None
    
    async def _analyze_element(self, element: ElementHandle) -> Dict[str, Any]:
        """Analyze element properties for intelligent interaction"""
        try:
            tag_name = await element.evaluate('el => el.tagName.toLowerCase()')
            element_type = await element.get_attribute('type') or ''
            class_name = await element.get_attribute('class') or ''
            id_attr = await element.get_attribute('id') or ''
            
            return {
                'tag': tag_name,
                'type': element_type,
                'class': class_name,
                'id': id_attr,
                'interactive': tag_name in ['button', 'a', 'input', 'select', 'textarea']
            }
            
        except Exception as e:
            logger.debug(f"Element analysis error: {e}")
            return {'tag': 'unknown', 'interactive': False}
    
    async def _wait_for_any_element(self, page: Page, selectors: List[str], timeout: int):
        """Wait for any of the specified elements to appear"""
        end_time = time.time() + (timeout / 1000)
        
        while time.time() < end_time:
            for selector in selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.is_visible():
                        return
                except:
                    continue
            await asyncio.sleep(0.1)
        
        raise TimeoutError("No elements found within timeout")
    
    async def _wait_for_js_completion(self, page: Page, timeout: int):
        """Wait for JavaScript execution to complete"""
        try:
            await page.wait_for_function(
                '() => document.readyState === "complete" && window.jQuery === undefined || jQuery.active === 0',
                timeout=timeout
            )
        except:
            # Fallback to simple ready state check
            await page.wait_for_function('() => document.readyState === "complete"', timeout=timeout)
    
    async def _smart_content_wait(self, page: Page):
        """Smart waiting based on page complexity analysis"""
        try:
            # Analyze page complexity
            complexity = await page.evaluate('''
                () => {
                    const scripts = document.querySelectorAll('script').length;
                    const images = document.querySelectorAll('img').length;
                    const iframes = document.querySelectorAll('iframe').length;
                    const complexity_score = scripts + images * 2 + iframes * 3;
                    
                    return {
                        scripts,
                        images,
                        iframes,
                        score: complexity_score,
                        has_react: !!window.React,
                        has_angular: !!window.angular,
                        has_vue: !!window.Vue
                    };
                }
            ''')
            
            # Adjust wait time based on complexity
            base_wait = 1000
            if complexity['score'] > 50:
                base_wait = 3000
            elif complexity['score'] > 20:
                base_wait = 2000
            
            # Additional wait for SPA frameworks
            if complexity['has_react'] or complexity['has_angular'] or complexity['has_vue']:
                base_wait += 2000
            
            await page.wait_for_timeout(base_wait)
            
        except Exception as e:
            logger.debug(f"Smart content wait error: {e}")
            await page.wait_for_timeout(1000)  # Fallback wait
    
    def _record_interaction(self, action: str, target: str, metadata: Dict[str, Any], behavior_type: str):
        """Record interaction for learning and analysis"""
        interaction = {
            'timestamp': time.time(),
            'action': action,
            'target': target,
            'metadata': metadata,
            'behavior_type': behavior_type
        }
        
        self.interaction_history.append(interaction)
        
        # Keep only last 1000 interactions
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]
    
    def get_interaction_analytics(self) -> Dict[str, Any]:
        """Get analytics on interaction patterns"""
        if not self.interaction_history:
            return {'total_interactions': 0}
        
        actions = [i['action'] for i in self.interaction_history]
        behavior_types = [i['behavior_type'] for i in self.interaction_history]
        
        return {
            'total_interactions': len(self.interaction_history),
            'action_breakdown': {action: actions.count(action) for action in set(actions)},
            'behavior_breakdown': {bt: behavior_types.count(bt) for bt in set(behavior_types)},
            'recent_interactions': self.interaction_history[-10:],
            'success_rate': 1.0  # Placeholder for future success tracking
        }

# Global real interaction engine instance
real_interaction_engine = RealWebsiteInteractionEngine()