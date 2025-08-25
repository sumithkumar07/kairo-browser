"""
Shadow Browser Service - Background Browser Management
Manages multiple headless browser instances for parallel execution
"""
import asyncio
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Set
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from concurrent.futures import ThreadPoolExecutor
import json

logger = logging.getLogger(__name__)

class ShadowBrowserService:
    """Manages multiple background browser instances"""
    
    def __init__(self):
        self.browser_pool = {}
        self.active_tasks = {}
        self.task_queue = asyncio.Queue()
        self.worker_browsers = {}
        self.max_browsers = 5  # Maximum concurrent browsers
        self.browser_timeout = 300  # 5 minutes timeout
        self.executor = ThreadPoolExecutor(max_workers=10)
        logger.info("👻 Shadow Browser Service initialized")
    
    async def initialize_browser_pool(self):
        """Initialize browser pool with multiple instances"""
        try:
            playwright = await async_playwright().start()
            
            for i in range(self.max_browsers):
                browser_id = f"shadow_browser_{i}"
                browser = await playwright.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-web-security',
                        '--disable-features=VizDisplayCompositor'
                    ]
                )
                
                self.browser_pool[browser_id] = {
                    'browser': browser,
                    'contexts': {},
                    'busy': False,
                    'created_at': datetime.now(),
                    'last_used': datetime.now()
                }
                
                logger.info(f"🚀 Shadow browser {browser_id} initialized")
            
            # Start background worker
            asyncio.create_task(self._process_task_queue())
            
            logger.info(f"✅ Shadow browser pool initialized with {self.max_browsers} browsers")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize browser pool: {e}")
    
    async def execute_background_task(self, task_config: Dict[str, Any]) -> str:
        """Execute a task in background browser"""
        try:
            task_id = str(uuid.uuid4())
            task = {
                'id': task_id,
                'config': task_config,
                'status': 'queued',
                'created_at': datetime.now(),
                'result': None,
                'error': None
            }
            
            self.active_tasks[task_id] = task
            await self.task_queue.put(task)
            
            logger.info(f"📋 Background task {task_id} queued")
            return task_id
            
        except Exception as e:
            logger.error(f"❌ Failed to queue background task: {e}")
            return None
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of background task"""
        task = self.active_tasks.get(task_id)
        if not task:
            return {'error': 'Task not found'}
        
        return {
            'id': task_id,
            'status': task['status'],
            'created_at': task['created_at'].isoformat(),
            'result': task.get('result'),
            'error': task.get('error')
        }
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a background task"""
        if task_id in self.active_tasks:
            self.active_tasks[task_id]['status'] = 'cancelled'
            logger.info(f"🚫 Task {task_id} cancelled")
            return True
        return False
    
    async def get_available_browser(self) -> Optional[Dict[str, Any]]:
        """Get an available browser from the pool"""
        for browser_id, browser_info in self.browser_pool.items():
            if not browser_info['busy']:
                browser_info['busy'] = True
                browser_info['last_used'] = datetime.now()
                return {'id': browser_id, **browser_info}
        
        return None
    
    async def release_browser(self, browser_id: str):
        """Release browser back to pool"""
        if browser_id in self.browser_pool:
            self.browser_pool[browser_id]['busy'] = False
            logger.debug(f"🔓 Released browser {browser_id}")
    
    async def _process_task_queue(self):
        """Background worker to process queued tasks"""
        while True:
            try:
                # Wait for task
                task = await self.task_queue.get()
                
                if task['status'] == 'cancelled':
                    continue
                
                # Get available browser
                browser_info = await self.get_available_browser()
                if not browser_info:
                    # No available browsers, put task back in queue
                    await asyncio.sleep(1)
                    await self.task_queue.put(task)
                    continue
                
                # Execute task
                task['status'] = 'running'
                try:
                    result = await self._execute_task(task, browser_info)
                    task['result'] = result
                    task['status'] = 'completed'
                    logger.info(f"✅ Task {task['id']} completed")
                    
                except Exception as e:
                    task['error'] = str(e)
                    task['status'] = 'failed'
                    logger.error(f"❌ Task {task['id']} failed: {e}")
                
                finally:
                    # Release browser
                    await self.release_browser(browser_info['id'])
                
            except Exception as e:
                logger.error(f"❌ Task queue processing error: {e}")
                await asyncio.sleep(5)
    
    async def _execute_task(self, task: Dict[str, Any], browser_info: Dict[str, Any]) -> Dict[str, Any]:
        """Execute individual task"""
        config = task['config']
        task_type = config.get('type')
        
        browser = browser_info['browser']
        
        if task_type == 'web_scraping':
            return await self._execute_scraping_task(browser, config)
        elif task_type == 'automation':
            return await self._execute_automation_task(browser, config)
        elif task_type == 'monitoring':
            return await self._execute_monitoring_task(browser, config)
        elif task_type == 'parallel_search':
            return await self._execute_parallel_search(browser, config)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def _execute_scraping_task(self, browser: Browser, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute web scraping task"""
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        try:
            url = config['url']
            selectors = config.get('selectors', [])
            
            await page.goto(url, timeout=30000)
            await page.wait_for_load_state('networkidle')
            
            # Extract data based on selectors
            extracted_data = {}
            for selector in selectors:
                elements = await page.query_selector_all(selector)
                extracted_data[selector] = [await elem.text_content() for elem in elements]
            
            # Get page content and screenshot
            content = await page.content()
            screenshot = await page.screenshot()
            
            return {
                'url': url,
                'extracted_data': extracted_data,
                'content_length': len(content),
                'screenshot_size': len(screenshot),
                'success': True
            }
            
        finally:
            await context.close()
    
    async def _execute_automation_task(self, browser: Browser, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute automation task"""
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            steps = config.get('steps', [])
            results = []
            
            for step in steps:
                action = step.get('action')
                
                if action == 'goto':
                    await page.goto(step['url'])
                elif action == 'click':
                    await page.click(step['selector'])
                elif action == 'type':
                    await page.fill(step['selector'], step['text'])
                elif action == 'wait':
                    await page.wait_for_timeout(step.get('duration', 1000))
                elif action == 'screenshot':
                    screenshot = await page.screenshot()
                    results.append({'action': 'screenshot', 'size': len(screenshot)})
                
                results.append({'action': action, 'status': 'completed'})
            
            return {
                'steps_completed': len(results),
                'results': results,
                'success': True
            }
            
        finally:
            await context.close()
    
    async def _execute_monitoring_task(self, browser: Browser, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute monitoring task"""
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            url = config['url']
            check_interval = config.get('interval', 60)  # seconds
            monitor_duration = config.get('duration', 300)  # 5 minutes
            
            checks = []
            start_time = datetime.now()
            
            while (datetime.now() - start_time).seconds < monitor_duration:
                await page.goto(url, timeout=30000)
                
                # Check for changes or specific conditions
                title = await page.title()
                content_hash = hash(await page.content())
                
                check_result = {
                    'timestamp': datetime.now().isoformat(),
                    'title': title,
                    'content_hash': content_hash,
                    'status': 'online'
                }
                
                checks.append(check_result)
                await asyncio.sleep(check_interval)
            
            return {
                'url': url,
                'checks': checks,
                'total_checks': len(checks),
                'success': True
            }
            
        finally:
            await context.close()
    
    async def _execute_parallel_search(self, browser: Browser, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parallel search across multiple sources"""
        queries = config.get('queries', [])
        search_engines = config.get('search_engines', ['google', 'bing', 'duckduckgo'])
        
        results = {}
        
        for query in queries:
            query_results = {}
            
            for engine in search_engines:
                try:
                    context = await browser.new_context()
                    page = await context.new_page()
                    
                    # Build search URL
                    if engine == 'google':
                        search_url = f"https://www.google.com/search?q={query}"
                    elif engine == 'bing':
                        search_url = f"https://www.bing.com/search?q={query}"
                    elif engine == 'duckduckgo':
                        search_url = f"https://duckduckgo.com/?q={query}"
                    
                    await page.goto(search_url, timeout=30000)
                    
                    # Extract search results (simplified)
                    if engine == 'google':
                        results_selector = '.g'
                    elif engine == 'bing':
                        results_selector = '.b_algo'
                    else:
                        results_selector = '.result'
                    
                    elements = await page.query_selector_all(results_selector)
                    search_results = []
                    
                    for elem in elements[:5]:  # Top 5 results
                        try:
                            title_elem = await elem.query_selector('h3')
                            title = await title_elem.text_content() if title_elem else ''
                            
                            link_elem = await elem.query_selector('a')
                            link = await link_elem.get_attribute('href') if link_elem else ''
                            
                            search_results.append({
                                'title': title.strip(),
                                'link': link
                            })
                        except:
                            continue
                    
                    query_results[engine] = search_results
                    await context.close()
                    
                except Exception as e:
                    query_results[engine] = {'error': str(e)}
            
            results[query] = query_results
        
        return {
            'search_results': results,
            'queries_processed': len(queries),
            'engines_used': search_engines,
            'success': True
        }
    
    async def cleanup_old_browsers(self):
        """Cleanup old unused browsers"""
        try:
            cutoff_time = datetime.now() - timedelta(minutes=30)
            
            for browser_id, browser_info in list(self.browser_pool.items()):
                if browser_info['last_used'] < cutoff_time and not browser_info['busy']:
                    await browser_info['browser'].close()
                    del self.browser_pool[browser_id]
                    logger.info(f"🧹 Cleaned up old browser {browser_id}")
            
        except Exception as e:
            logger.error(f"❌ Browser cleanup failed: {e}")

# Global shadow browser service
shadow_browser_service = ShadowBrowserService()