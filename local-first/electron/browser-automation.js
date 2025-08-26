/**
 * Browser Automation - Local-First Implementation
 * Native browser automation using Playwright directly
 */

class BrowserAutomation {
  constructor() {
    this.commandQueue = [];
    this.isExecuting = false;
  }

  /**
   * Execute a browser command on the active page
   * @param {Page} page - Playwright page instance
   * @param {string} command - Command to execute
   * @param {Object} params - Command parameters
   */
  async executeCommand(page, command, params = {}) {
    try {
      console.log(`⚡ Executing command: ${command}`, params);

      switch (command) {
        case 'navigate':
        case 'open':
          return await this.navigate(page, params.url);

        case 'click':
          return await this.click(page, params.selector);

        case 'type':
          return await this.type(page, params.selector, params.text);

        case 'scroll':
          return await this.scroll(page, params.direction, params.amount);

        case 'wait':
          return await this.wait(page, params.duration);

        case 'waitForSelector':
          return await this.waitForSelector(page, params.selector, params.timeout);

        case 'evaluate':
          return await this.evaluate(page, params.script);

        case 'screenshot':
          return await this.screenshot(page, params.options);

        case 'extract':
          return await this.extractData(page, params.selector, params.attribute);

        case 'search':
          return await this.searchOnPage(page, params.query);

        case 'youtube_video':
          return await this.handleYouTubeVideo(page, params);

        default:
          throw new Error(`Unknown command: ${command}`);
      }
    } catch (error) {
      console.error(`❌ Command execution failed:`, error);
      throw error;
    }
  }

  async navigate(page, url) {
    const response = await page.goto(url, { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    return {
      url: page.url(),
      title: await page.title(),
      status: response?.status() || 200
    };
  }

  async click(page, selector) {
    await page.waitForSelector(selector, { timeout: 10000 });
    await page.click(selector);
    
    return {
      action: 'clicked',
      selector: selector,
      success: true
    };
  }

  async type(page, selector, text) {
    await page.waitForSelector(selector, { timeout: 10000 });
    await page.fill(selector, text);
    
    return {
      action: 'typed',
      selector: selector,
      text: text,
      success: true
    };
  }

  async scroll(page, direction = 'down', amount = 500) {
    const scrollY = direction === 'down' ? amount : -amount;
    await page.evaluate((y) => window.scrollBy(0, y), scrollY);
    
    return {
      action: 'scrolled',
      direction: direction,
      amount: amount,
      success: true
    };
  }

  async wait(page, duration = 1000) {
    await page.waitForTimeout(duration);
    
    return {
      action: 'waited',
      duration: duration,
      success: true
    };
  }

  async waitForSelector(page, selector, timeout = 10000) {
    await page.waitForSelector(selector, { timeout });
    
    return {
      action: 'waited_for_selector',
      selector: selector,
      found: true,
      success: true
    };
  }

  async evaluate(page, script) {
    const result = await page.evaluate(script);
    
    return {
      action: 'evaluated',
      script: script,
      result: result,
      success: true
    };
  }

  async screenshot(page, options = {}) {
    const screenshot = await page.screenshot({
      fullPage: options.fullPage || false,
      quality: options.quality || 90,
      type: options.type || 'png'
    });
    
    return {
      action: 'screenshot',
      screenshot: screenshot.toString('base64'),
      success: true
    };
  }

  async extractData(page, selector, attribute = 'textContent') {
    const elements = await page.$$eval(selector, (els, attr) => {
      return els.map(el => {
        if (attr === 'textContent') return el.textContent.trim();
        if (attr === 'innerHTML') return el.innerHTML;
        if (attr === 'href') return el.href;
        if (attr === 'src') return el.src;
        return el.getAttribute(attr);
      });
    }, attribute);
    
    return {
      action: 'extracted',
      selector: selector,
      attribute: attribute,
      data: elements,
      count: elements.length,
      success: true
    };
  }

  async searchOnPage(page, query) {
    // Try common search selectors including Google's specific ones
    const searchSelectors = [
      'input[name="q"]',           // Google search
      'textarea[name="q"]',        // Google's new search box
      'input[name="search"]',
      'input[placeholder*="search" i]',
      'input[placeholder*="Search" i]',
      '#search',
      '.search-input',
      '[role="searchbox"]',
      '[role="combobox"]'
    ];

    for (const selector of searchSelectors) {
      try {
        // Wait for element to be present
        await page.waitForSelector(selector, { timeout: 3000 });
        const element = await page.$(selector);
        
        if (element) {
          // Clear any existing text and type the query
          await element.click();
          await element.fill('');
          await element.fill(query);
          await page.waitForTimeout(500); // Brief pause for stability
          await element.press('Enter');
          
          // Wait for search results to start loading
          await page.waitForTimeout(2000);
          
          return {
            action: 'searched',
            query: query,
            selector: selector,
            success: true
          };
        }
      } catch (error) {
        // Continue to next selector
        continue;
      }
    }

    throw new Error('No search input found on the page');
  }

  async handleYouTubeVideo(page, params) {
    try {
      const { search_query, enhanced_search, stealth_mode } = params;
      
      // Navigate to YouTube search
      const searchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(search_query)}`;
      await this.navigate(page, searchUrl);
      
      // Wait for search results to load
      await page.waitForSelector('#contents', { timeout: 15000 });
      
      // If enhanced_search is enabled, try to click first video
      if (enhanced_search) {
        const videoSelectors = [
          'a#video-title',
          '.ytd-video-renderer a[href*="/watch"]',
          '#video-title-link',
          'h3 a[href*="/watch"]'
        ];
        
        for (const selector of videoSelectors) {
          try {
            const element = await page.$(selector);
            if (element) {
              await element.click();
              
              // Wait for video page to load
              await page.waitForSelector('#movie_player', { timeout: 10000 });
              
              return {
                action: 'youtube_video',
                search_query: search_query,
                video_opened: true,
                url: page.url(),
                success: true
              };
            }
          } catch (error) {
            continue;
          }
        }
      }
      
      return {
        action: 'youtube_video',
        search_query: search_query,
        search_results_loaded: true,
        url: page.url(),
        success: true
      };
      
    } catch (error) {
      console.error('YouTube video handling error:', error);
      throw error;
    }
  }

  /**
   * Execute multiple commands in sequence
   */
  async executeSequence(page, commands) {
    const results = [];
    
    for (const command of commands) {
      try {
        const result = await this.executeCommand(page, command.type, command.params);
        results.push({ ...result, commandId: command.id });
      } catch (error) {
        results.push({ 
          commandId: command.id, 
          success: false, 
          error: error.message 
        });
        break; // Stop on first error
      }
    }
    
    return results;
  }

  /**
   * Get page information
   */
  async getPageInfo(page) {
    return {
      url: page.url(),
      title: await page.title(),
      ready: await page.evaluate(() => document.readyState === 'complete')
    };
  }
}

module.exports = BrowserAutomation;