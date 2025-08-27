/**
 * Browser + AI Main Process
 * Split-screen interface with visible browser + AI chat
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { chromium } = require('playwright');

// Import AI components
const EnhancedAIIntegration = require('../orchestrator/ai-integration-enhanced');

class BrowserAIApp {
  constructor() {
    this.mainWindow = null;
    this.ai = new EnhancedAIIntegration();
    this.chromiumBrowser = null;
    this.activePage = null;
    this.isInitialized = false;
    
    this.setupApp();
  }

  setupApp() {
    // Container environment compatibility
    app.commandLine.appendSwitch('no-sandbox');
    app.commandLine.appendSwitch('disable-setuid-sandbox'); 
    app.commandLine.appendSwitch('disable-dev-shm-usage');
    app.commandLine.appendSwitch('disable-web-security');

    app.whenReady().then(() => {
      this.createWindow();
      this.initializeBrowserAI();
    });

    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        this.cleanup();
        app.quit();
      }
    });

    this.setupIPC();
  }

  async createWindow() {
    this.mainWindow = new BrowserWindow({
      width: 1400,
      height: 900,
      minWidth: 1200,
      minHeight: 700,
      titleBarStyle: 'hiddenInset',
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload-browser-ai.js'),
        webSecurity: false
      },
      show: false,
      backgroundColor: '#1a1a1a'
    });

    // Load Browser + AI Interface
    const isDev = process.env.NODE_ENV === 'development';
    if (isDev) {
      this.mainWindow.loadFile(path.join(__dirname, '../renderer/index-browser-ai.html'));
      this.mainWindow.webContents.openDevTools();
    } else {
      this.mainWindow.loadFile(path.join(__dirname, '../renderer/index-browser-ai.html'));
    }

    this.mainWindow.once('ready-to-show', () => {
      this.mainWindow.show();
    });
  }

  async initializeBrowserAI() {
    try {
      console.log('🚀 Initializing Browser + AI System...');
      
      // Initialize visible Chromium browser
      await this.initializeVisibleBrowser();
      
      // Mark as initialized
      this.isInitialized = true;
      
      console.log('✅ Browser + AI System ready!');

      // Notify renderer
      if (this.mainWindow) {
        this.mainWindow.webContents.send('system-ready', {
          success: true,
          message: 'Browser and AI systems are ready!'
        });
      }

    } catch (error) {
      console.error('❌ Browser + AI initialization error:', error);
      this.isInitialized = false;
    }
  }

  async initializeVisibleBrowser() {
    try {
      console.log('🌐 Starting visible browser engine...');
      
      // Launch Chromium in non-headless mode for visible control
      this.chromiumBrowser = await chromium.launch({
        headless: false, // VISIBLE browser
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-web-security',
          '--disable-features=TranslateUI',
          '--start-maximized'
        ]
      });

      const context = await this.chromiumBrowser.newContext({
        viewport: { width: 1920, height: 1080 },
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 KairoAI/2.0.0'
      });

      this.activePage = await context.newPage();
      
      // Navigate to Google initially
      await this.activePage.goto('https://www.google.com', { waitUntil: 'networkidle' });
      
      console.log('✅ Visible browser ready and showing Google');

    } catch (error) {
      console.error('❌ Visible browser initialization failed:', error);
      throw error;
    }
  }

  setupIPC() {
    // AI System Initialization
    ipcMain.handle('ai-initialize', async (event) => {
      try {
        return {
          success: this.isInitialized,
          message: this.isInitialized 
            ? "Hello! I'm your AI assistant. I can control the visible browser for you. Just tell me what you want to do!"
            : "Starting up browser and AI systems...",
          capabilities: [
            "Navigate to any website",
            "Search and extract data",
            "Control browser interactions",
            "Multi-step automation",
            "Real-time visual feedback",
            "Natural language commands"
          ]
        };
      } catch (error) {
        return {
          success: false,
          message: "I'm having trouble starting up. Let me try again...",
          error: error.message
        };
      }
    });

    // AI Input Processing with Visible Browser Control
    ipcMain.handle('ai-process-input', async (event, userInput, context = {}) => {
      try {
        console.log(`🎯 AI Processing: "${userInput}"`);
        
        if (!this.isInitialized || !this.activePage) {
          return {
            success: false,
            message: "Browser is still starting up. Please wait a moment."
          };
        }

        // Enhanced context with current page info
        const enhancedContext = {
          ...context,
          currentUrl: this.activePage.url(),
          pageTitle: await this.activePage.title().catch(() => ''),
          browserVisible: true
        };

        // Process with AI
        const aiResponse = await this.ai.processNaturalLanguage(userInput, enhancedContext);
        
        // Execute browser commands if generated
        const browserResults = [];
        if (aiResponse.parallelTasks && aiResponse.parallelTasks.length > 0) {
          for (const task of aiResponse.parallelTasks) {
            try {
              const result = await this.executeBrowserTask(task);
              browserResults.push([task.id, result]);
              
              // Notify renderer of browser updates
              this.mainWindow?.webContents.send('browser-updated', {
                url: this.activePage.url(),
                title: await this.activePage.title().catch(() => '')
              });
              
              // Small delay between actions for visibility
              await new Promise(resolve => setTimeout(resolve, 1000));
              
            } catch (error) {
              console.error(`Browser task failed: ${task.id}`, error);
              browserResults.push([task.id, { success: false, error: error.message }]);
            }
          }
        }

        return {
          success: true,
          message: aiResponse.explanation || `I've processed your request: "${userInput}". Check the browser for results!`,
          data: aiResponse,
          browserResults: browserResults,
          proactiveActions: aiResponse.proactiveActions || []
        };
        
      } catch (error) {
        console.error('❌ AI processing error:', error);
        return {
          success: false,
          message: "I had trouble processing that request. Could you try rephrasing it?",
          error: error.message
        };
      }
    });

    // Browser Navigation Controls
    ipcMain.handle('browser-navigate', async (event, url) => {
      try {
        if (!this.activePage) {
          throw new Error('Browser not ready');
        }

        console.log(`🌐 Navigating to: ${url}`);
        
        const response = await this.activePage.goto(url, { 
          waitUntil: 'networkidle',
          timeout: 30000 
        });

        return {
          success: true,
          url: this.activePage.url(),
          title: await this.activePage.title().catch(() => ''),
          status: response?.status() || 200
        };
      } catch (error) {
        console.error('Navigation error:', error);
        return {
          success: false,
          error: error.message
        };
      }
    });

    ipcMain.handle('browser-go-back', async (event) => {
      try {
        if (this.activePage) {
          await this.activePage.goBack();
          return { success: true };
        }
        return { success: false, error: 'Browser not ready' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('browser-go-forward', async (event) => {
      try {
        if (this.activePage) {
          await this.activePage.goForward();
          return { success: true };
        }
        return { success: false, error: 'Browser not ready' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    ipcMain.handle('browser-refresh', async (event) => {
      try {
        if (this.activePage) {
          await this.activePage.reload();
          return { success: true };
        }
        return { success: false, error: 'Browser not ready' };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // System Information
    ipcMain.handle('system-info', async (event) => {
      const os = require('os');
      return {
        success: true,
        system: {
          platform: os.platform(),
          arch: os.arch(),
          memory: Math.round(os.totalmem() / 1024 / 1024 / 1024),
          version: app.getVersion(),
          browserReady: !!this.activePage,
          aiInitialized: this.isInitialized
        }
      };
    });

    // Error Reporting
    ipcMain.handle('report-error', async (event, errorData) => {
      console.error('🚨 Frontend Error:', errorData);
      return { success: true, message: 'Error reported' };
    });
  }

  /**
   * Execute browser tasks based on AI commands
   */
  async executeBrowserTask(task) {
    if (!this.activePage) {
      throw new Error('No active browser page');
    }

    console.log(`⚡ Executing browser task: ${task.type}`);

    switch (task.type) {
      case 'browse':
      case 'navigate':
        const url = task.params?.url || task.url;
        if (url) {
          await this.activePage.goto(url, { waitUntil: 'networkidle' });
          return {
            success: true,
            action: 'navigated',
            url: this.activePage.url(),
            title: await this.activePage.title().catch(() => '')
          };
        }
        break;

      case 'search':
        const query = task.params?.query || task.query;
        if (query) {
          // Try to find search box and search
          const searchSelectors = [
            'input[name="q"]',
            'textarea[name="q"]', 
            'input[type="search"]',
            '#search',
            '.search-input'
          ];

          for (const selector of searchSelectors) {
            try {
              const element = await this.activePage.$(selector);
              if (element) {
                await element.click();
                await element.fill(query);
                await element.press('Enter');
                await this.activePage.waitForTimeout(2000);
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

      case 'click':
        const clickSelector = task.params?.selector;
        if (clickSelector) {
          await this.activePage.waitForSelector(clickSelector, { timeout: 10000 });
          await this.activePage.click(clickSelector);
          return {
            success: true,
            action: 'clicked',
            selector: clickSelector
          };
        }
        break;

      case 'extract':
        const extractSelector = task.params?.selector;
        if (extractSelector) {
          const data = await this.activePage.$$eval(extractSelector, els => 
            els.map(el => el.textContent?.trim()).filter(text => text)
          );
          return {
            success: true,
            action: 'extracted',
            data: data,
            count: data.length
          };
        }
        break;

      case 'screenshot':
        const screenshot = await this.activePage.screenshot({ 
          fullPage: false,
          quality: 80 
        });
        return {
          success: true,
          action: 'screenshot',
          screenshot: screenshot.toString('base64')
        };

      default:
        console.warn(`Unknown browser task type: ${task.type}`);
    }

    return {
      success: false,
      error: `Could not execute task: ${task.type}`
    };
  }

  async cleanup() {
    console.log('🧹 Cleaning up Browser + AI App...');
    
    try {
      if (this.activePage) {
        await this.activePage.close();
      }
      
      if (this.chromiumBrowser) {
        await this.chromiumBrowser.close();
      }
      
      console.log('✅ Cleanup completed');
    } catch (error) {
      console.error('❌ Cleanup error:', error);
    }
  }
}

// Initialize the application
const browserAIApp = new BrowserAIApp();

// Error Handling
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Rejection:', reason);
});

module.exports = BrowserAIApp;