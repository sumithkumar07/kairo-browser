/**
 * Autonomous Browser Engine - Invisible Operations
 * Handles all browser tasks behind the scenes
 */

const { chromium } = require('playwright');

class AutonomousBrowser {
  constructor() {
    this.browsers = new Map(); // Multiple browser instances
    this.pages = new Map();    // Multiple page instances
    this.activeOperations = new Map();
    this.maxConcurrent = 5;
  }

  /**
   * Initialize invisible browser instances
   */
  async initialize() {
    console.log('🌐 Initializing autonomous browser engines...');
    
    // Create multiple browser instances for parallel operations
    for (let i = 0; i < this.maxConcurrent; i++) {
      const browser = await chromium.launch({
        headless: true, // Invisible operation
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-web-security',
          '--disable-features=TranslateUI',
          '--disable-background-timer-throttling',
          '--disable-backgrounding-occluded-windows',
          '--disable-renderer-backgrounding'
        ]
      });
      
      this.browsers.set(`browser_${i}`, browser);
      
      // Create initial pages
      const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 KairoAI/2.0.0'
      });
      
      const page = await context.newPage();
      this.pages.set(`page_${i}`, page);
    }
    
    console.log(`✅ ${this.maxConcurrent} autonomous browser instances ready`);
  }

  /**
   * Execute parallel browser operations
   */
  async executeParallelOperations(operations) {
    const results = new Map();
    const operationPromises = [];

    for (const [index, operation] of operations.entries()) {
      const browserId = `browser_${index % this.maxConcurrent}`;
      const pageId = `page_${index % this.maxConcurrent}`;
      
      const promise = this.executeSingleOperation(operation, browserId, pageId)
        .then(result => results.set(operation.id, result))
        .catch(error => results.set(operation.id, { error: error.message }));
        
      operationPromises.push(promise);
    }

    await Promise.allSettled(operationPromises);
    return results;
  }

  /**
   * Execute single browser operation
   */
  async executeSingleOperation(operation, browserId, pageId) {
    const page = this.pages.get(pageId);
    
    try {
      console.log(`🤖 Executing: ${operation.type} - ${operation.description}`);
      
      switch (operation.type) {
        case 'navigate':
          return await this.autonomousNavigate(page, operation.params);
          
        case 'search':
          return await this.autonomousSearch(page, operation.params);
          
        case 'extract':
          return await this.autonomousExtract(page, operation.params);
          
        case 'interact':
          return await this.autonomousInteract(page, operation.params);
          
        case 'analyze':
          return await this.autonomousAnalyze(page, operation.params);
          
        case 'monitor':
          return await this.autonomousMonitor(page, operation.params);
          
        default:
          throw new Error(`Unknown operation: ${operation.type}`);
      }
      
    } catch (error) {
      console.error(`❌ Operation failed: ${operation.type}`, error);
      throw error;
    }
  }

  /**
   * Autonomous Navigation - Smart website navigation
   */
  async autonomousNavigate(page, params) {
    const { url, waitFor, expectedContent } = params;
    
    console.log(`🌐 Navigating to: ${url}`);
    
    // Navigate with smart waiting
    const response = await page.goto(url, { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    // Wait for specific content if specified
    if (waitFor) {
      await page.waitForSelector(waitFor, { timeout: 15000 });
    }
    
    // Verify expected content
    if (expectedContent) {
      const content = await page.textContent('body');
      if (!content.includes(expectedContent)) {
        console.warn(`⚠️ Expected content not found: ${expectedContent}`);
      }
    }
    
    const pageInfo = {
      url: page.url(),
      title: await page.title(),
      status: response?.status() || 200,
      content: await page.textContent('body').catch(() => ''),
      timestamp: new Date().toISOString()
    };
    
    return {
      success: true,
      action: 'navigated',
      data: pageInfo
    };
  }

  /**
   * Autonomous Search - Intelligent search across platforms
   */
  async autonomousSearch(page, params) {
    const { platform, query, filters, maxResults } = params;
    
    console.log(`🔍 Searching ${platform} for: ${query}`);
    
    let searchUrl;
    let resultSelector;
    
    switch (platform.toLowerCase()) {
      case 'google':
        searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
        resultSelector = '.g h3';
        break;
        
      case 'youtube':
        searchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
        resultSelector = '#video-title';
        break;
        
      case 'github':
        searchUrl = `https://github.com/search?q=${encodeURIComponent(query)}`;
        resultSelector = '.repo-list-item h3 a';
        break;
        
      case 'amazon':
        searchUrl = `https://www.amazon.com/s?k=${encodeURIComponent(query)}`;
        resultSelector = '[data-component-type="s-search-result"] h2 a';
        break;
        
      default:
        throw new Error(`Unsupported platform: ${platform}`);
    }
    
    // Navigate to search
    await page.goto(searchUrl, { waitUntil: 'networkidle' });
    
    // Wait for results
    await page.waitForSelector(resultSelector, { timeout: 15000 });
    
    // Extract results
    const results = await page.$$eval(resultSelector, (elements, max) => {
      return elements.slice(0, max || 10).map(el => ({
        title: el.textContent?.trim() || '',
        link: el.href || '',
        snippet: el.closest('.g, .ytd-video-renderer, .repo-list-item, [data-component-type="s-search-result"]')
          ?.querySelector('span, .metadata, .f, .a-size-base')?.textContent?.trim() || ''
      }));
    }, maxResults);
    
    return {
      success: true,
      action: 'searched',
      platform: platform,
      query: query,
      results: results,
      count: results.length
    };
  }

  /**
   * Autonomous Extract - Smart data extraction
   */
  async autonomousExtract(page, params) {
    const { selectors, dataType, structure } = params;
    
    console.log(`📊 Extracting data: ${dataType}`);
    
    const extractedData = {};
    
    // Extract based on data type
    switch (dataType) {
      case 'prices':
        extractedData.prices = await this.extractPrices(page, selectors);
        break;
        
      case 'contact':
        extractedData.contact = await this.extractContactInfo(page, selectors);
        break;
        
      case 'products':
        extractedData.products = await this.extractProducts(page, selectors);
        break;
        
      case 'articles':
        extractedData.articles = await this.extractArticles(page, selectors);
        break;
        
      default:
        // Generic extraction
        for (const [key, selector] of Object.entries(selectors || {})) {
          extractedData[key] = await page.$$eval(selector, els => 
            els.map(el => el.textContent?.trim() || '')
          );
        }
    }
    
    return {
      success: true,
      action: 'extracted',
      dataType: dataType,
      data: extractedData,
      url: page.url()
    };
  }

  /**
   * Autonomous Interaction - Smart form filling and clicking
   */
  async autonomousInteract(page, params) {
    const { actions, waitBetween } = params;
    const results = [];
    
    for (const action of actions) {
      try {
        let result;
        
        switch (action.type) {
          case 'click':
            await page.click(action.selector);
            result = { type: 'click', selector: action.selector, success: true };
            break;
            
          case 'type':
            await page.fill(action.selector, action.text);
            result = { type: 'type', selector: action.selector, text: action.text, success: true };
            break;
            
          case 'select':
            await page.selectOption(action.selector, action.value);
            result = { type: 'select', selector: action.selector, value: action.value, success: true };
            break;
            
          case 'upload':
            await page.setInputFiles(action.selector, action.file);
            result = { type: 'upload', selector: action.selector, file: action.file, success: true };
            break;
            
          default:
            throw new Error(`Unknown interaction: ${action.type}`);
        }
        
        results.push(result);
        
        // Wait between actions if specified
        if (waitBetween) {
          await page.waitForTimeout(waitBetween);
        }
        
      } catch (error) {
        results.push({
          type: action.type,
          selector: action.selector,
          success: false,
          error: error.message
        });
      }
    }
    
    return {
      success: true,
      action: 'interacted',
      results: results
    };
  }

  /**
   * Autonomous Analysis - AI-powered page analysis
   */
  async autonomousAnalyze(page, params) {
    const { analysisType, focus } = params;
    
    console.log(`🔍 Analyzing page: ${analysisType}`);
    
    const pageData = {
      url: page.url(),
      title: await page.title(),
      content: await page.textContent('body'),
      links: await page.$$eval('a[href]', links => 
        links.map(l => ({ text: l.textContent?.trim(), href: l.href }))
      ),
      images: await page.$$eval('img[src]', imgs => 
        imgs.map(i => ({ alt: i.alt, src: i.src }))
      ),
      forms: await page.$$eval('form', forms => 
        forms.map(f => ({ action: f.action, method: f.method }))
      )
    };
    
    // Take screenshot for visual analysis
    const screenshot = await page.screenshot({ 
      fullPage: false,
      quality: 80 
    });
    
    return {
      success: true,
      action: 'analyzed',
      analysisType: analysisType,
      data: pageData,
      screenshot: screenshot.toString('base64'),
      insights: this.generatePageInsights(pageData, focus)
    };
  }

  /**
   * Helper Methods for Data Extraction
   */
  async extractPrices(page, selectors) {
    const priceSelectors = selectors || [
      '.price', '.cost', '[data-price]', '.amount', '.value',
      '.price-current', '.sale-price', '.regular-price'
    ];
    
    const prices = [];
    for (const selector of priceSelectors) {
      try {
        const elements = await page.$$(selector);
        for (const el of elements) {
          const text = await el.textContent();
          const price = text?.match(/[\d,]+\.?\d*/)?.[0];
          if (price) {
            prices.push({
              text: text.trim(),
              value: parseFloat(price.replace(/,/g, '')),
              selector: selector
            });
          }
        }
      } catch (error) {
        continue;
      }
    }
    
    return prices;
  }

  generatePageInsights(pageData, focus) {
    const insights = [];
    
    if (focus?.includes('ecommerce') || pageData.content.includes('price')) {
      insights.push('This appears to be an e-commerce page with pricing information');
    }
    
    if (pageData.forms.length > 0) {
      insights.push(`Found ${pageData.forms.length} form(s) - potential for automation`);
    }
    
    if (pageData.links.length > 50) {
      insights.push('High link density - likely a navigation or listing page');
    }
    
    return insights;
  }

  /**
   * Cleanup
   */
  async cleanup() {
    console.log('🧹 Cleaning up autonomous browser instances...');
    
    for (const browser of this.browsers.values()) {
      try {
        await browser.close();
      } catch (error) {
        console.error('Error closing browser:', error);
      }
    }
    
    this.browsers.clear();
    this.pages.clear();
    
    console.log('✅ Cleanup completed');
  }
}

module.exports = AutonomousBrowser;