/**
 * Kairo AI Browser - Local-First Main Process
 * Electron main process for local-first architecture
 */

const { app, BrowserWindow, session, ipcMain, protocol, net } = require('electron');
const path = require('path');
const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');

// Local modules
const BrowserAutomation = require('./browser-automation');
const WorkflowEngine = require('../orchestrator/workflow-engine');
const AIIntegration = require('../orchestrator/ai-integration');
const SyncClient = require('../sync/sync-client');

class KairoLocalBrowser {
  constructor() {
    this.mainWindow = null;
    this.browserAutomation = new BrowserAutomation();
    this.workflowEngine = new WorkflowEngine();
    this.aiIntegration = new AIIntegration();
    this.syncClient = new SyncClient();
    this.chromiumContext = null;
    this.activePage = null;
    
    this.setupApp();
  }

  setupApp() {
    // Enable hardware acceleration
    app.commandLine.appendSwitch('enable-features', 'VaapiVideoDecoder');
    app.commandLine.appendSwitch('ignore-certificate-errors');
    app.commandLine.appendSwitch('disable-web-security');
    
    // Handle app events
    app.whenReady().then(() => this.createWindow());
    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        this.cleanup();
        app.quit();
      }
    });
    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        this.createWindow();
      }
    });

    this.setupIPC();
  }

  async createWindow() {
    // Create the browser window
    this.mainWindow = new BrowserWindow({
      width: 1400,
      height: 900,
      minWidth: 1000,
      minHeight: 600,
      titleBarStyle: 'hiddenInset',
      trafficLightPosition: { x: 10, y: 10 },
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload.js'),
        webSecurity: false // For local development
      },
      show: false
    });

    // Load the React app
    const isDev = process.env.NODE_ENV === 'development';
    if (isDev) {
      this.mainWindow.loadURL('http://localhost:3000');
      this.mainWindow.webContents.openDevTools();
    } else {
      this.mainWindow.loadFile(path.join(__dirname, '../renderer/build/index.html'));
    }

    // Show window when ready
    this.mainWindow.once('ready-to-show', () => {
      this.mainWindow.show();
    });

    // Initialize embedded Chromium
    await this.initializeChromium();
  }

  async initializeChromium() {
    try {
      console.log('🚀 Initializing embedded Chromium browser...');
      
      const browser = await chromium.launch({
        headless: false, // Can be changed to true for headless mode
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-web-security',
          '--disable-features=TranslateUI',
          '--disable-ipc-flooding-protection',
          '--disable-background-timer-throttling',
          '--disable-backgrounding-occluded-windows',
          '--disable-renderer-backgrounding',
        ],
      });

      this.chromiumContext = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Kairo/1.0.0',
        locale: 'en-US',
        timezoneId: 'America/New_York',
      });

      // Create initial page
      this.activePage = await this.chromiumContext.newPage();
      
      console.log('✅ Embedded Chromium initialized successfully');
      
      // Set up page event listeners
      this.activePage.on('console', msg => {
        console.log(`🌐 Chromium Console [${msg.type()}]:`, msg.text());
      });

      this.activePage.on('pageerror', error => {
        console.error('🚨 Chromium Page Error:', error);
      });

      // Notify renderer that Chromium is ready
      if (this.mainWindow) {
        this.mainWindow.webContents.send('chromium-ready', {
          success: true,
          message: 'Embedded Chromium browser ready'
        });
      }

    } catch (error) {
      console.error('❌ Failed to initialize Chromium:', error);
      if (this.mainWindow) {
        this.mainWindow.webContents.send('chromium-ready', {
          success: false,
          error: error.message
        });
      }
    }
  }

  setupIPC() {
    // Browser navigation
    ipcMain.handle('browser-navigate', async (event, url) => {
      try {
        console.log(`🌐 Navigating to: ${url}`);
        
        if (!this.activePage) {
          throw new Error('Chromium not initialized');
        }

        const response = await this.activePage.goto(url, { 
          waitUntil: 'networkidle',
          timeout: 30000 
        });

        const title = await this.activePage.title();
        const finalUrl = this.activePage.url();

        return {
          success: true,
          url: finalUrl,
          title: title,
          status: response?.status() || 200
        };
      } catch (error) {
        console.error('❌ Navigation error:', error);
        return {
          success: false,
          error: error.message
        };
      }
    });

    // AI query processing
    ipcMain.handle('ai-query', async (event, query, context = {}) => {
      try {
        console.log(`🤖 Processing AI query: ${query}`);
        
        const result = await this.aiIntegration.processQuery(query, {
          ...context,
          currentUrl: this.activePage?.url(),
          pageTitle: await this.activePage?.title().catch(() => '')
        });

        return {
          success: true,
          response: result
        };
      } catch (error) {
        console.error('❌ AI query error:', error);
        return {
          success: false,
          error: error.message
        };
      }
    });

    // Browser automation
    ipcMain.handle('browser-execute', async (event, command, params = {}) => {
      try {
        console.log(`⚡ Executing browser command: ${command}`);
        
        if (!this.activePage) {
          throw new Error('No active page');
        }

        const result = await this.browserAutomation.executeCommand(
          this.activePage, 
          command, 
          params
        );

        return {
          success: true,
          result: result
        };
      } catch (error) {
        console.error('❌ Browser execution error:', error);
        return {
          success: false,
          error: error.message
        };
      }
    });

    // Workflow execution
    ipcMain.handle('workflow-execute', async (event, workflow) => {
      try {
        console.log(`🔄 Executing workflow: ${workflow.name}`);
        
        const result = await this.workflowEngine.execute(workflow, {
          page: this.activePage,
          browserAutomation: this.browserAutomation,
          aiIntegration: this.aiIntegration
        });

        return {
          success: true,
          workflowId: result.id,
          result: result
        };
      } catch (error) {
        console.error('❌ Workflow execution error:', error);
        return {
          success: false,
          error: error.message
        };
      }
    });

    // System information
    ipcMain.handle('system-info', async (event) => {
      return {
        success: true,
        system: {
          platform: os.platform(),
          arch: os.arch(),
          cpus: os.cpus().length,
          memory: Math.round(os.totalmem() / 1024 / 1024 / 1024), // GB
          version: app.getVersion(),
          electron: process.versions.electron,
          chrome: process.versions.chrome,
          node: process.versions.node
        }
      };
    });

    // App information (for LocalFirstDetector)
    ipcMain.handle('get-app-info', async (event) => {
      return {
        appName: 'Kairo AI Browser',
        version: app.getVersion(),
        platform: os.platform(),
        arch: os.arch(),
        isLocalFirst: true,
        environment: 'local-first'
      };
    });

    // File operations
    ipcMain.handle('file-save', async (event, filepath, content) => {
      try {
        fs.writeFileSync(filepath, content);
        return { success: true };
      } catch (error) {
        return { success: false, error: error.message };
      }
    });

    // Window controls
    ipcMain.handle('window-minimize', async (event) => {
      this.mainWindow?.minimize();
      return { success: true };
    });

    ipcMain.handle('window-maximize', async (event) => {
      if (this.mainWindow?.isMaximized()) {
        this.mainWindow?.unmaximize();
      } else {
        this.mainWindow?.maximize();
      }
      return { success: true };
    });

    ipcMain.handle('window-close', async (event) => {
      this.mainWindow?.close();
      return { success: true };
    });

    // Get page content (for UI embedding)
    ipcMain.handle('get-page-content', async (event) => {
      try {
        if (!this.activePage) {
          return { success: false, error: 'No active page' };
        }

        const content = await this.activePage.content();
        const url = this.activePage.url();
        const title = await this.activePage.title();

        return {
          success: true,
          content: content,
          url: url,
          title: title
        };
      } catch (error) {
        return {
          success: false,
          error: error.message
        };
      }
    });

    // Take screenshot
    ipcMain.handle('take-screenshot', async (event, options = {}) => {
      try {
        if (!this.activePage) {
          throw new Error('No active page');
        }

        const screenshot = await this.activePage.screenshot({
          fullPage: options.fullPage || false,
          quality: options.quality || 90
        });

        return {
          success: true,
          screenshot: screenshot.toString('base64')
        };
      } catch (error) {
        return {
          success: false,
          error: error.message
        };
      }
    });
  }

  async cleanup() {
    console.log('🧹 Cleaning up resources...');
    
    try {
      if (this.activePage) {
        await this.activePage.close();
      }
      
      if (this.chromiumContext) {
        await this.chromiumContext.close();
      }
      
      console.log('✅ Cleanup completed');
    } catch (error) {
      console.error('❌ Cleanup error:', error);
    }
  }
}

// Initialize the application
const kairoApp = new KairoLocalBrowser();

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Rejection at:', promise, 'reason:', reason);
});

module.exports = KairoLocalBrowser;