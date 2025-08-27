/**
 * Enhanced Electron Main Process - Pure AI Integration
 * Bridges Pure NLP Interface with Electron
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

// Import Pure AI System
const PureNLPInterface = require('../orchestrator/pure-nlp-interface');

class EnhancedKairoApp {
  constructor() {
    this.mainWindow = null;
    this.pureAI = new PureNLPInterface();
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
      this.initializeAI();
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
      width: 1200,
      height: 800,
      minWidth: 800,
      minHeight: 600,
      titleBarStyle: 'hiddenInset',
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true,
        preload: path.join(__dirname, 'preload-enhanced.js'),
        webSecurity: false
      },
      show: false,
      backgroundColor: '#1a1a1a'
    });

    // Load Pure AI Interface
    const isDev = process.env.NODE_ENV === 'development';
    if (isDev) {
      this.mainWindow.loadFile(path.join(__dirname, '../renderer/index-pure-ai.html'));
      this.mainWindow.webContents.openDevTools();
    } else {
      this.mainWindow.loadFile(path.join(__dirname, '../renderer/index-pure-ai.html'));
    }

    this.mainWindow.once('ready-to-show', () => {
      this.mainWindow.show();
    });
  }

  async initializeAI() {
    try {
      console.log('🚀 Initializing Pure AI System...');
      
      const result = await this.pureAI.initialize();
      this.isInitialized = result.success;
      
      if (this.isInitialized) {
        console.log('✅ Pure AI System ready!');
      } else {
        console.error('❌ AI initialization failed');
      }

      // Notify renderer
      if (this.mainWindow) {
        this.mainWindow.webContents.send('ai-initialized', {
          success: this.isInitialized,
          message: result.message,
          capabilities: result.capabilities
        });
      }

    } catch (error) {
      console.error('❌ AI initialization error:', error);
      this.isInitialized = false;
    }
  }

  setupIPC() {
    // AI System Initialization
    ipcMain.handle('ai-initialize', async (event) => {
      try {
        if (!this.isInitialized) {
          await this.initializeAI();
        }
        
        const state = this.pureAI.getConversationState();
        
        return {
          success: this.isInitialized,
          message: this.isInitialized 
            ? "Hello! I'm your AI assistant. Tell me anything you want to do, and I'll handle it completely!"
            : "AI system is starting up...",
          capabilities: state.capabilities || []
        };
      } catch (error) {
        return {
          success: false,
          message: "I'm having trouble starting up. Let me try again...",
          error: error.message
        };
      }
    });

    // Main AI Processing
    ipcMain.handle('ai-process-input', async (event, userInput, context = {}) => {
      try {
        console.log(`🎯 Processing: "${userInput}"`);
        
        if (!this.isInitialized) {
          return {
            success: false,
            message: "I'm still starting up. Please wait a moment and try again."
          };
        }

        // Process through Pure NLP Interface
        const result = await this.pureAI.handleUserInput(userInput, context);
        
        return result;
        
      } catch (error) {
        console.error('❌ AI processing error:', error);
        return {
          success: false,
          message: "I encountered an issue processing that. Could you try rephrasing your request?",
          error: error.message
        };
      }
    });

    // Quick Actions
    ipcMain.handle('ai-quick-search', async (event, query, platforms) => {
      try {
        return await this.pureAI.quickSearch(query, platforms);
      } catch (error) {
        return {
          success: false,
          message: `Error with quick search: ${error.message}`
        };
      }
    });

    ipcMain.handle('ai-quick-analyze', async (event, url) => {
      try {
        return await this.pureAI.quickAnalyze(url);
      } catch (error) {
        return {
          success: false,
          message: `Error analyzing URL: ${error.message}`
        };
      }
    });

    ipcMain.handle('ai-quick-compare', async (event, items) => {
      try {
        return await this.pureAI.quickCompare(items);
      } catch (error) {
        return {
          success: false,
          message: `Error with comparison: ${error.message}`
        };
      }
    });

    // Conversation Management
    ipcMain.handle('ai-get-state', async (event) => {
      return this.pureAI.getConversationState();
    });

    ipcMain.handle('ai-reset-conversation', async (event) => {
      return this.pureAI.resetConversation();
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
          aiInitialized: this.isInitialized,
          conversationActive: this.pureAI.getConversationState().active
        }
      };
    });

    // Window Controls
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

    // Health Check
    ipcMain.handle('health-check', async (event) => {
      return {
        success: true,
        status: 'healthy',
        aiInitialized: this.isInitialized,
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
      };
    });

    // Error Reporting
    ipcMain.handle('report-error', async (event, errorData) => {
      console.error('🚨 Frontend Error:', errorData);
      
      // Could integrate with error reporting service
      return {
        success: true,
        message: 'Error reported successfully'
      };
    });
  }

  async cleanup() {
    console.log('🧹 Cleaning up Enhanced Kairo App...');
    
    try {
      if (this.pureAI) {
        await this.pureAI.shutdown();
      }
      
      console.log('✅ Cleanup completed');
    } catch (error) {
      console.error('❌ Cleanup error:', error);
    }
  }
}

// Initialize the enhanced application
const enhancedApp = new EnhancedKairoApp();

// Error Handling
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Rejection:', reason);
});

module.exports = EnhancedKairoApp;