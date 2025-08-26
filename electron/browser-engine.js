const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

class LocalBrowserEngine {
  constructor() {
    this.browser = null;
    this.pages = new Map(); // Track open pages/tabs
    this.isInitialized = false;
  }

  async initialize() {
    try {
      console.log('🔧 Initializing local browser engine...');
      
      // Find Chrome/Chromium executable
      const chromiumPath = await this.findChromiumExecutable();
      
      this.browser = await puppeteer.launch({
        executablePath: chromiumPath,
        headless: false, // Show browser window for local-first experience
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-web-security',
          '--allow-running-insecure-content',
          '--disable-features=VizDisplayCompositor',
          '--disable-background-timer-throttling',
          '--disable-backgrounding-occluded-windows',
          '--disable-renderer-backgrounding',
          '--disable-blink-features=AutomationControlled',
          '--no-first-run',
          '--no-default-browser-check',
          '--no-zygote',
          '--disable-gpu'
        ],
        userDataDir: path.join(process.cwd(), 'user-data'),
        defaultViewport: { width: 1920, height: 1080 }
      });
      
      this.isInitialized = true;
      console.log('✅ Local browser engine initialized successfully');
      return true;
    } catch (error) {
      console.error('❌ Failed to initialize browser engine:', error);
      this.isInitialized = false;
      return false;
    }
  }

  async findChromiumExecutable() {
    // Try to find system Chrome/Chromium
    const possiblePaths = [
      '/usr/bin/google-chrome',
      '/usr/bin/google-chrome-stable',
      '/usr/bin/chromium-browser',
      '/usr/bin/chromium',
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    ];

    for (const chromePath of possiblePaths) {
      if (fs.existsSync(chromePath)) {
        console.log('📍 Found Chrome at:', chromePath);
        return chromePath;
      }
    }

    // Fallback to puppeteer bundled Chromium if available
    try {
      const puppeteerChrome = puppeteer.executablePath();
      if (fs.existsSync(puppeteerChrome)) {
        console.log('📍 Using Puppeteer bundled Chromium');
        return puppeteerChrome;
      }
    } catch (e) {
      // Ignore error
    }

    throw new Error('No Chrome/Chromium executable found. Please install Chrome or Chromium.');
  }

  async createTab(sessionId) {
    if (!this.browser || !this.isInitialized) {
      throw new Error('Browser engine not initialized');
    }
    
    try {
      const page = await this.browser.newPage();
      
      // Set realistic viewport and user agent for better compatibility
      await page.setViewport({ width: 1920, height: 1080 });
      await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
      
      // Set additional headers for better site compatibility
      await page.setExtraHTTPHeaders({
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
      });

      // Add script to remove automation detection
      await page.evaluateOnNewDocument(() => {
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
      });
      
      this.pages.set(sessionId, page);
      console.log('✅ New tab created for session:', sessionId);
      return page;
    } catch (error) {
      console.error('❌ Failed to create tab:', error);
      throw error;
    }
  }

  async navigateToUrl(sessionId, url) {
    const page = this.pages.get(sessionId);
    if (!page) {
      throw new Error('No active page for session: ' + sessionId);
    }

    try {
      console.log('🌐 Navigating to:', url);
      const response = await page.goto(url, { 
        waitUntil: 'networkidle2',
        timeout: 30000 
      });
      
      const title = await page.title();
      const finalUrl = page.url();
      
      console.log('✅ Navigation successful:', title);
      
      return { 
        success: true, 
        url: finalUrl, 
        title,
        status: response.status(),
        sessionId
      };
    } catch (error) {
      console.error('❌ Navigation failed:', error);
      return { 
        success: false, 
        error: error.message,
        sessionId
      };
    }
  }

  async executeCommand(sessionId, command) {
    const page = this.pages.get(sessionId);
    if (!page) {
      throw new Error('No active page for session: ' + sessionId);
    }

    try {
      console.log('⚡ Executing command:', command.type);
      
      switch (command.type) {
        case 'click':
          await page.waitForSelector(command.selector, { timeout: 5000 });
          await page.click(command.selector);
          break;
          
        case 'type':
          await page.waitForSelector(command.selector, { timeout: 5000 });
          await page.click(command.selector); // Focus first
          await page.keyboard.down('Control');
          await page.keyboard.press('a');
          await page.keyboard.up('Control');
          await page.type(command.selector, command.text);
          break;
          
        case 'scroll':
          await page.evaluate((pixels) => {
            window.scrollBy(0, pixels || 500);
          }, command.pixels);
          break;
          
        case 'screenshot':
          const screenshot = await page.screenshot({ 
            encoding: 'base64',
            fullPage: false,
            quality: 80
          });
          return { success: true, screenshot, sessionId };
          
        case 'extract_text':
          const text = await page.$eval(command.selector, el => el.textContent);
          return { success: true, text, sessionId };
          
        case 'extract_links':
          const links = await page.$$eval('a[href]', anchors => 
            anchors.map(anchor => ({
              text: anchor.textContent.trim(),
              href: anchor.href
            }))
          );
          return { success: true, links, sessionId };
          
        case 'wait_for_element':
          await page.waitForSelector(command.selector, { 
            timeout: command.timeout || 10000 
          });
          break;
          
        case 'press_key':
          await page.keyboard.press(command.key);
          break;
          
        default:
          throw new Error('Unknown command type: ' + command.type);
      }
      
      console.log('✅ Command executed successfully');
      return { success: true, sessionId };
      
    } catch (error) {
      console.error('❌ Command execution failed:', error);
      return { 
        success: false, 
        error: error.message,
        sessionId 
      };
    }
  }

  async getPageContent(sessionId) {
    const page = this.pages.get(sessionId);
    if (!page) return null;

    try {
      const content = await page.content();
      const title = await page.title();
      const url = page.url();
      
      return { content, title, url, sessionId };
    } catch (error) {
      console.error('❌ Failed to get page content:', error);
      return null;
    }
  }

  async getPageInfo(sessionId) {
    const page = this.pages.get(sessionId);
    if (!page) return null;

    try {
      const title = await page.title();
      const url = page.url();
      const favicon = await page.$eval('link[rel="icon"]', el => el.href).catch(() => null);
      
      return { title, url, favicon, sessionId };
    } catch (error) {
      console.error('❌ Failed to get page info:', error);
      return { title: 'Unknown', url: '', favicon: null, sessionId };
    }
  }

  async closePage(sessionId) {
    const page = this.pages.get(sessionId);
    if (page) {
      try {
        await page.close();
        this.pages.delete(sessionId);
        console.log('✅ Page closed for session:', sessionId);
      } catch (error) {
        console.error('❌ Failed to close page:', error);
      }
    }
  }

  async getAllSessions() {
    const sessions = [];
    for (const [sessionId, page] of this.pages) {
      try {
        const info = await this.getPageInfo(sessionId);
        sessions.push(info);
      } catch (error) {
        console.error('Error getting session info:', error);
      }
    }
    return sessions;
  }

  async shutdown() {
    console.log('🔄 Shutting down browser engine...');
    
    // Close all pages first
    for (const [sessionId] of this.pages) {
      await this.closePage(sessionId);
    }
    
    if (this.browser) {
      try {
        await this.browser.close();
        this.browser = null;
        this.isInitialized = false;
        console.log('✅ Browser engine shutdown complete');
      } catch (error) {
        console.error('❌ Error during browser shutdown:', error);
      }
    }
  }

  // Health check
  isHealthy() {
    return this.isInitialized && this.browser && this.browser.isConnected();
  }

  getStats() {
    return {
      isInitialized: this.isInitialized,
      isConnected: this.browser ? this.browser.isConnected() : false,
      activeSessions: this.pages.size,
      sessions: Array.from(this.pages.keys())
    };
  }
}

module.exports = LocalBrowserEngine;