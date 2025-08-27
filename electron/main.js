/**
 * Kairo AI Browser - Enhanced Main Process
 * Phase 1: Enhanced AI + Phase 2: Advanced Browser in Parallel
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { chromium } = require('playwright');
const os = require('os');

// Import Enhanced Components
const EnhancedAIIntegration = require('../orchestrator/ai-integration-enhanced');
const AutonomousBrowser = require('../orchestrator/autonomous-browser');

class AdvancedKairoBrowser {
  constructor() {
    this.mainWindow = null;
    
    // Phase 1: Enhanced AI System
    this.enhancedAI = new EnhancedAIIntegration();
    
    // Phase 2: Advanced Browser System  
    this.autonomousBrowser = new AutonomousBrowser();
    this.visibleBrowser = null;
    this.mainPage = null;
    this.browserTabs = new Map(); // Multi-tab support
    this.activeTabId = 'main';
    
    // System State
    this.isInitialized = false;
    this.capabilities = [];
    
    this.setupApp();
  }

  setupApp() {
    // Enhanced container environment compatibility
    app.commandLine.appendSwitch('no-sandbox');
    app.commandLine.appendSwitch('disable-setuid-sandbox'); 
    app.commandLine.appendSwitch('disable-dev-shm-usage');
    app.commandLine.appendSwitch('disable-web-security');
    app.commandLine.appendSwitch('enable-features', 'VaapiVideoDecoder');
    app.commandLine.appendSwitch('ignore-certificate-errors');

    app.whenReady().then(() => {
      this.createAdvancedWindow();
      this.initializeAdvancedSystems();
    });

    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        this.cleanup();
        app.quit();
      }
    });

    this.setupAdvancedIPC();
  }

  async createAdvancedWindow() {
    this.mainWindow = new BrowserWindow({
      width: 1500,
      height: 1000,
      minWidth: 1200,
      minHeight: 700,
      titleBarStyle: 'hiddenInset',
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload.js'),
        webSecurity: false
      },
      show: false,
      backgroundColor: '#1a1a1a'
    });

    // Load Enhanced Browser + AI Interface
    const isDev = process.env.NODE_ENV === 'development';
    const htmlFile = path.join(__dirname, '../renderer/index.html');
    
    this.mainWindow.loadFile(htmlFile);
    
    if (isDev) {
      this.mainWindow.webContents.openDevTools();
    }

    this.mainWindow.once('ready-to-show', () => {
      this.mainWindow.show();
    });
  }

  async initializeAdvancedSystems() {
    try {
      console.log('🚀 Initializing Advanced Kairo AI Browser...');
      console.log('   📈 Phase 1: Enhanced AI System');
      console.log('   📈 Phase 2: Advanced Browser System');
      
      // Phase 1 & 2: Initialize in parallel
      const [aiResult, browserResult] = await Promise.allSettled([
        this.initializeEnhancedAI(),
        this.initializeAdvancedBrowser()
      ]);

      // Check results
      const aiReady = aiResult.status === 'fulfilled';
      const browserReady = browserResult.status === 'fulfilled';
      
      this.isInitialized = aiReady && browserReady;
      
      // Set capabilities based on what's working
      this.capabilities = this.buildCapabilitiesList(aiReady, browserReady);
      
      console.log('✅ Advanced Systems Status:');
      console.log(`   🧠 Enhanced AI: ${aiReady ? 'READY' : 'LIMITED'}`);  
      console.log(`   🌐 Advanced Browser: ${browserReady ? 'READY' : 'LIMITED'}`);
      console.log(`   ⚡ Multi-Tab Support: ${browserReady ? 'ENABLED' : 'DISABLED'}`);
      console.log(`   🔄 Parallel Processing: ${aiReady && browserReady ? 'ENABLED' : 'DISABLED'}`);

      // Notify renderer with enhanced status
      if (this.mainWindow) {
        this.mainWindow.webContents.send('advanced-system-ready', {
          success: this.isInitialized,
          ai: { ready: aiReady, enhanced: true },
          browser: { ready: browserReady, advanced: true, multiTab: browserReady },
          capabilities: this.capabilities,
          message: this.isInitialized 
            ? '🚀 Enhanced AI + Advanced Browser ready! Try: "Search for iPhone prices on Amazon, Best Buy, and Apple simultaneously"'
            : 'Systems starting up with enhanced capabilities...'
        });
      }

    } catch (error) {
      console.error('❌ Advanced system initialization error:', error);
      this.isInitialized = false;
    }
  }

  /**
   * Phase 1: Initialize Enhanced AI System
   */
  async initializeEnhancedAI() {
    console.log('🧠 Starting Enhanced AI System...');
    
    // Enhanced AI is already initialized in constructor
    // Test AI capability
    try {
      const testResult = await this.enhancedAI.processNaturalLanguage(
        'Test initialization', 
        { test: true }
      );
      console.log('✅ Enhanced AI System: Online');
      return true;
    } catch (error) {
      console.error('❌ Enhanced AI System: Limited', error.message);
      throw error;
    }
  }

  /**
   * Phase 2: Initialize Advanced Browser System  
   */
  async initializeAdvancedBrowser() {
    console.log('🌐 Starting Advanced Browser System...');
    
    // Initialize autonomous browser for parallel operations
    await this.autonomousBrowser.initialize();
    
    // Initialize visible browser for main display
    await this.initializeVisibleBrowser();
    
    console.log('✅ Advanced Browser System: Multi-tab + Parallel ready');
    return true;
  }

  async initializeVisibleBrowser() {
    console.log('   🖥️ Starting main visible browser...');
    
    this.visibleBrowser = await chromium.launch({
      headless: false, // VISIBLE for user interaction
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage', 
        '--disable-web-security',
        '--disable-features=TranslateUI',
        '--start-maximized'
      ]
    });

    const context = await this.visibleBrowser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 KairoAI/Advanced/2.0.0'
    });

    // Create main tab
    this.mainPage = await context.newPage();
    this.browserTabs.set('main', {
      page: this.mainPage,
      title: 'New Tab',
      url: 'about:blank'
    });
    
    // Navigate to Google initially
    await this.mainPage.goto('https://www.google.com', { waitUntil: 'networkidle' });
    this.browserTabs.get('main').url = 'https://www.google.com';
    this.browserTabs.get('main').title = await this.mainPage.title();
    
    console.log('   ✅ Visible browser ready with multi-tab support');
  }

  buildCapabilitiesList(aiReady, browserReady) {
    const capabilities = [
      'Split-screen Browser + AI interface',
      'Natural language command processing'
    ];
    
    if (aiReady) {
      capabilities.push(
        '🧠 Enhanced AI: Multi-step task planning',
        '🧠 Enhanced AI: Learning & memory system', 
        '🧠 Enhanced AI: Proactive suggestions',
        '🧠 Enhanced AI: Parallel task execution'
      );
    }
    
    if (browserReady) {
      capabilities.push(
        '🌐 Advanced Browser: Multi-tab operations',
        '🌐 Advanced Browser: Parallel website automation', 
        '🌐 Advanced Browser: Smart data extraction',
        '🌐 Advanced Browser: Intelligent element detection'
      );
    }
    
    if (aiReady && browserReady) {
      capabilities.push(
        '⚡ Multi-site parallel operations',
        '⚡ Complex workflow automation',
        '⚡ Real-time data analysis',
        '⚡ Unlimited website access'
      );
    }
    
    return capabilities;
  }

  setupAdvancedIPC() {
    // Enhanced AI System Initialization
    ipcMain.handle('ai-initialize', async (event) => {
      try {
        return {
          success: this.isInitialized,
          enhanced: true,
          message: this.isInitialized 
            ? "Hello! I'm your Enhanced AI assistant with advanced browser control. I can handle complex multi-step tasks and parallel operations. Try asking me to compare prices across multiple websites!"
            : "Enhanced AI systems are starting up...",
          capabilities: this.capabilities
        };
      } catch (error) {
        return {
          success: false,
          enhanced: false,
          message: "Having trouble with enhanced systems. Let me try basic mode...",
          error: error.message
        };
      }
    });

    // Enhanced AI Processing with Parallel Execution
    ipcMain.handle('ai-process-input', async (event, userInput, context = {}) => {
      try {
        console.log(`🎯 Enhanced AI Processing: "${userInput}"`);
        
        if (!this.isInitialized) {
          return {
            success: false,
            message: "Enhanced systems are still starting up. Please wait a moment."
          };
        }

        // Build enhanced context
        const enhancedContext = {
          ...context,
          currentUrl: this.mainPage?.url(),
          pageTitle: await this.mainPage?.title().catch(() => ''),
          browserVisible: true,
          multiTabSupport: true,
          autonomousBrowserReady: true,
          availableTabs: Array.from(this.browserTabs.keys())
        };

        // Process with Enhanced AI (Phase 1)
        console.log('   🧠 Enhanced AI: Processing natural language...');
        const aiResponse = await this.enhancedAI.processNaturalLanguage(userInput, enhancedContext);
        
        // Execute with Advanced Browser (Phase 2) 
        console.log('   🌐 Advanced Browser: Executing parallel tasks...');
        const executionResults = await this.executeAdvancedTasks(aiResponse);

        // Notify UI of updates
        this.notifyBrowserUpdates();

        return {
          success: true,
          enhanced: true,
          message: aiResponse.message || `✅ Enhanced processing complete! Executed ${executionResults.length} operations.`,
          data: aiResponse.data,
          tasksSummary: aiResponse.tasksSummary,
          browserResults: executionResults,
          proactiveActions: aiResponse.proactiveActions || []
        };
        
      } catch (error) {
        console.error('❌ Enhanced AI processing error:', error);
        return {
          success: false,
          enhanced: false,
          message: "I had trouble with that enhanced request. Let me try a simpler approach - what would you like me to do?",
          error: error.message
        };
      }
    });

    // Advanced Multi-Tab Browser Operations
    ipcMain.handle('browser-create-tab', async (event, url = 'about:blank') => {
      try {
        const tabId = `tab_${Date.now()}`;
        const context = await this.visibleBrowser.newContext();
        const page = await context.newPage();
        
        if (url !== 'about:blank') {
          await page.goto(url, { waitUntil: 'networkidle' });
        }
        
        this.browserTabs.set(tabId, {
          page: page,
          title: await page.title() || 'New Tab',
          url: page.url()
        });

        return {
          success: true,
          tabId: tabId,
          url: page.url(),
          title: await page.title()
        };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('browser-switch-tab', async (event, tabId) => {
      try {
        if (this.browserTabs.has(tabId)) {
          this.activeTabId = tabId;
          this.mainPage = this.browserTabs.get(tabId).page;
          return { success: true };
        }
        return { success: false, error: 'Tab not found' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('browser-close-tab', async (event, tabId) => {
      try {
        if (this.browserTabs.has(tabId) && tabId !== 'main') {
          const tab = this.browserTabs.get(tabId);
          await tab.page.close();
          this.browserTabs.delete(tabId);
          
          if (this.activeTabId === tabId) {
            this.activeTabId = 'main';
            this.mainPage = this.browserTabs.get('main').page;
          }
          
          return { success: true };
        }
        return { success: false, error: 'Cannot close main tab' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Standard browser controls (enhanced)
    ipcMain.handle('browser-navigate', async (event, url) => {
      try {
        if (!this.mainPage) throw new Error('Browser not ready');

        console.log(`🌐 Enhanced navigation to: ${url}`);
        
        const response = await this.mainPage.goto(url, { 
          waitUntil: 'networkidle',
          timeout: 30000 
        });

        // Update tab info
        const currentTab = this.browserTabs.get(this.activeTabId);
        currentTab.url = this.mainPage.url();
        currentTab.title = await this.mainPage.title();

        return {
          success: true,
          url: this.mainPage.url(),
          title: currentTab.title,
          status: response?.status() || 200,
          enhanced: true
        };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // System information (enhanced)
    ipcMain.handle('system-info', async (event) => {
      return {
        success: true,
        enhanced: true,
        system: {
          platform: os.platform(),
          arch: os.arch(),
          memory: Math.round(os.totalmem() / 1024 / 1024 / 1024),
          version: app.getVersion(),
          browserReady: !!this.mainPage,
          aiEnhanced: true,
          browserAdvanced: true,
          multiTabSupport: true,
          parallelProcessing: true,
          activeTabs: this.browserTabs.size,
          autonomousBrowsers: 5
        }
      };
    });

    // Standard IPC handlers (kept for compatibility)
    ipcMain.handle('browser-go-back', async () => {
      try {
        if (this.mainPage) {
          await this.mainPage.goBack();
          return { success: true };
        }
        return { success: false, error: 'Browser not ready' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('browser-go-forward', async () => {
      try {
        if (this.mainPage) {
          await this.mainPage.goForward();
          return { success: true };
        }
        return { success: false, error: 'Browser not ready' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('browser-refresh', async () => {
      try {
        if (this.mainPage) {
          await this.mainPage.reload();
          return { success: true };
        }
        return { success: false, error: 'Browser not ready' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('report-error', async (event, errorData) => {
      console.error('🚨 Enhanced Frontend Error:', errorData);
      return { success: true, message: 'Error reported' };
    });
  }

  /**
   * Execute Advanced Tasks using both Enhanced AI + Advanced Browser
   */
  async executeAdvancedTasks(aiResponse) {
    const results = [];
    
    try {
      // Check if we have parallel tasks from Enhanced AI
      if (aiResponse.parallelTasks && aiResponse.parallelTasks.length > 0) {
        console.log(`   ⚡ Executing ${aiResponse.parallelTasks.length} parallel tasks...`);
        
        // Separate visible vs background tasks
        const visibleTasks = aiResponse.parallelTasks.filter(task => task.visible !== false);
        const backgroundTasks = aiResponse.parallelTasks.filter(task => task.visible === false);
        
        // Execute visible tasks on main browser
        for (const task of visibleTasks) {
          const result = await this.executeVisibleTask(task);
          results.push([task.id, result]);
        }
        
        // Execute background tasks on autonomous browsers
        if (backgroundTasks.length > 0) {
          const bgResults = await this.autonomousBrowser.executeParallelOperations(backgroundTasks);
          for (const [taskId, result] of bgResults) {
            results.push([taskId, result]);
          }
        }
      }
    } catch (error) {
      console.error('❌ Advanced task execution error:', error);
      results.push(['error', { success: false, error: error.message }]);
    }
    
    return results;
  }

  /**
   * Execute task on visible browser
   */
  async executeVisibleTask(task) {
    if (!this.mainPage) {
      throw new Error('No active browser page');
    }

    console.log(`   🎬 Visible: ${task.type} - ${task.description || task.id}`);

    try {
      switch (task.type) {
        case 'navigate':
        case 'browse':
          const url = task.params?.url || task.url;
          if (url) {
            await this.mainPage.goto(url, { waitUntil: 'networkidle' });
            
            // Update tab info
            const currentTab = this.browserTabs.get(this.activeTabId);
            currentTab.url = this.mainPage.url();
            currentTab.title = await this.mainPage.title();
            
            return {
              success: true,
              action: 'navigated',
              url: this.mainPage.url(),
              title: currentTab.title
            };
          }
          break;

        case 'search':
          const query = task.params?.query || task.query;
          if (query) {
            // Enhanced search with multiple selectors
            const searchSelectors = [
              'input[name="q"]', 'textarea[name="q"]', 'input[type="search"]',
              '#search', '.search-input', '[data-testid="search"]',
              'input[placeholder*="search" i]', 'input[aria-label*="search" i]'
            ];

            for (const selector of searchSelectors) {
              try {
                const element = await this.mainPage.$(selector);
                if (element) {
                  await element.click();
                  await element.fill(query);
                  await element.press('Enter');
                  await this.mainPage.waitForTimeout(2000);
                  return {
                    success: true,
                    action: 'searched',
                    query: query,
                    selector: selector
                  };
                }
              } catch (error) {
                continue;
              }
            }
          }
          break;

        case 'extract':
          const extractSelector = task.params?.selector;
          if (extractSelector) {
            const data = await this.mainPage.$$eval(extractSelector, els => 
              els.map(el => ({
                text: el.textContent?.trim() || '',
                html: el.innerHTML?.trim() || '',
                attributes: Object.fromEntries(
                  Array.from(el.attributes).map(attr => [attr.name, attr.value])
                )
              })).filter(item => item.text)
            );
            return {
              success: true,
              action: 'extracted',
              data: data,
              count: data.length,
              selector: extractSelector
            };
          }
          break;

        case 'click':
          const clickSelector = task.params?.selector;
          if (clickSelector) {
            await this.mainPage.waitForSelector(clickSelector, { timeout: 10000 });
            await this.mainPage.click(clickSelector);
            return {
              success: true,
              action: 'clicked',
              selector: clickSelector
            };
          }
          break;

        case 'screenshot':
          const screenshot = await this.mainPage.screenshot({ 
            fullPage: false,
            quality: 80 
          });
          return {
            success: true,
            action: 'screenshot',
            screenshot: screenshot.toString('base64')
          };

        default:
          console.warn(`Unknown visible task type: ${task.type}`);
          return {
            success: false,
            error: `Unsupported visible task type: ${task.type}`
          };
      }
    } catch (error) {
      console.error(`Visible task failed: ${task.type}`, error);
      return {
        success: false,
        error: error.message,
        task: task.type
      };
    }

    return {
      success: false,
      error: `Could not execute visible task: ${task.type}`
    };
  }

  notifyBrowserUpdates() {
    if (this.mainPage && this.mainWindow) {
      this.mainPage.title().then(title => {
        this.mainWindow.webContents.send('browser-updated', {
          url: this.mainPage.url(),
          title: title,
          tabId: this.activeTabId,
          totalTabs: this.browserTabs.size
        });
      }).catch(() => {});
    }
  }

  async cleanup() {
    console.log('🧹 Cleaning up Advanced Kairo Browser...');
    
    try {
      // Close all browser tabs
      for (const [tabId, tab] of this.browserTabs) {
        try {
          await tab.page.close();
        } catch (error) {
          console.error(`Error closing tab ${tabId}:`, error);
        }
      }
      
      // Close visible browser
      if (this.visibleBrowser) {
        await this.visibleBrowser.close();
      }
      
      // Cleanup autonomous browsers
      if (this.autonomousBrowser) {
        await this.autonomousBrowser.cleanup();
      }
      
      console.log('✅ Advanced cleanup completed');
    } catch (error) {
      console.error('❌ Cleanup error:', error);
    }
  }
}

// Initialize the Advanced Application
const advancedKairoBrowser = new AdvancedKairoBrowser();

// Enhanced Error Handling
process.on('uncaughtException', (error) => {
  console.error('❌ Advanced Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Advanced Unhandled Rejection:', reason);
});

module.exports = AdvancedKairoBrowser;