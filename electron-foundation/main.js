/**
 * Kairo AI Browser - Electron Main Process
 * Local-First Architecture with Native Chromium Integration
 */

const { app, BrowserWindow, ipcMain, session } = require('electron');
const path = require('path');
const { autoUpdater } = require('electron-updater');
const LocalAIService = require('./services/local-ai-service');
const NativeBrowserService = require('./services/native-browser-service'); 
const LocalStorageService = require('./services/local-storage-service');

class KairoAIBrowser {
    constructor() {
        this.mainWindow = null;
        this.browserView = null;
        this.aiService = new LocalAIService();
        this.browserService = new NativeBrowserService();
        this.storageService = new LocalStorageService();
        
        this.isDevelopment = process.env.NODE_ENV === 'development';
        this.isReady = false;
    }

    async initialize() {
        console.log('🚀 Initializing Kairo AI Browser...');
        
        // Initialize services
        await this.aiService.initialize();
        await this.browserService.initialize();
        await this.storageService.initialize();
        
        // Setup auto-updater
        if (!this.isDevelopment) {
            autoUpdater.checkForUpdatesAndNotify();
        }
        
        this.isReady = true;
        console.log('✅ Kairo AI Browser initialized successfully');
    }

    createMainWindow() {
        // Create the main application window
        this.mainWindow = new BrowserWindow({
            width: 1400,
            height: 900,
            minWidth: 1000,
            minHeight: 700,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                enableRemoteModule: false,
                preload: path.join(__dirname, 'preload.js'),
                webSecurity: true // Keep security enabled
            },
            icon: path.join(__dirname, 'assets', 'icon.png'),
            show: false, // Don't show until ready
            titleBarStyle: 'default'
        });

        // Load the renderer (React app)
        const rendererPath = this.isDevelopment 
            ? 'http://localhost:3000'  // Development server
            : `file://${path.join(__dirname, 'renderer', 'index.html')}`; // Production build
            
        this.mainWindow.loadURL(rendererPath);

        // Show window when ready
        this.mainWindow.once('ready-to-show', () => {
            this.mainWindow.show();
            
            if (this.isDevelopment) {
                this.mainWindow.webContents.openDevTools();
            }
        });

        // Handle window closed
        this.mainWindow.on('closed', () => {
            this.mainWindow = null;
            this.browserView = null;
        });

        return this.mainWindow;
    }

    setupIpcHandlers() {
        // AI Service Handlers
        ipcMain.handle('ai-query', async (event, query) => {
            try {
                return await this.aiService.processQuery(query);
            } catch (error) {
                console.error('❌ AI Query Error:', error);
                return { error: error.message };
            }
        });

        // Browser Automation Handlers  
        ipcMain.handle('browser-navigate', async (event, url) => {
            try {
                return await this.browserService.navigate(url);
            } catch (error) {
                console.error('❌ Navigation Error:', error);
                return { error: error.message };
            }
        });

        ipcMain.handle('browser-execute', async (event, command) => {
            try {
                return await this.browserService.executeCommand(command);
            } catch (error) {
                console.error('❌ Command Execution Error:', error);
                return { error: error.message };
            }
        });

        // Storage Handlers
        ipcMain.handle('storage-get', async (event, key) => {
            return this.storageService.get(key);
        });

        ipcMain.handle('storage-set', async (event, key, value) => {
            return this.storageService.set(key, value);
        });

        // Window Management
        ipcMain.handle('window-minimize', () => {
            this.mainWindow?.minimize();
        });

        ipcMain.handle('window-maximize', () => {
            if (this.mainWindow?.isMaximized()) {
                this.mainWindow.unmaximize();
            } else {
                this.mainWindow?.maximize();
            }
        });

        ipcMain.handle('window-close', () => {
            this.mainWindow?.close();
        });

        console.log('✅ IPC handlers registered');
    }

    setupAppEventHandlers() {
        // App ready handler
        app.whenReady().then(async () => {
            await this.initialize();
            this.createMainWindow();
            this.setupIpcHandlers();
        });

        // All windows closed handler
        app.on('window-all-closed', () => {
            if (process.platform !== 'darwin') {
                app.quit();
            }
        });

        // App activated handler (macOS)
        app.on('activate', () => {
            if (BrowserWindow.getAllWindows().length === 0) {
                this.createMainWindow();
            }
        });

        // Before quit handler
        app.on('before-quit', async () => {
            console.log('🛑 Shutting down Kairo AI Browser...');
            
            // Cleanup services
            await this.aiService.cleanup();
            await this.browserService.cleanup();
            await this.storageService.cleanup();
            
            console.log('👋 Kairo AI Browser shutdown complete');
        });
    }
}

// Initialize the application
const kairoApp = new KairoAIBrowser();
kairoApp.setupAppEventHandlers();

// Export for testing
module.exports = KairoAIBrowser;