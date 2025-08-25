/**
 * Kairo AI Browser - Electron Main Process
 * Local-First Architecture with Native Chromium Integration
 */

const { app, BrowserWindow, ipcMain, BrowserView } = require('electron');
const path = require('path');

class KairoAIBrowser {
    constructor() {
        this.mainWindow = null;
        this.browserView = null;
        this.isDevelopment = process.env.NODE_ENV === 'development';
        this.isReady = false;
    }

    async initialize() {
        console.log('🚀 Initializing Kairo AI Browser...');
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
                webSecurity: false // Allow loading any website
            },
            show: false, // Don't show until ready
            titleBarStyle: 'default'
        });

        // For now, load the existing React app
        const rendererPath = 'http://localhost:3000';
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

    createBrowserView(url) {
        // Create a BrowserView for native website access
        if (this.browserView) {
            this.mainWindow.removeBrowserView(this.browserView);
        }

        this.browserView = new BrowserView({
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true,
                webSecurity: false, // Allow all websites
                allowRunningInsecureContent: true
            }
        });

        this.mainWindow.addBrowserView(this.browserView);
        
        // Set initial bounds (adjust based on UI)
        this.browserView.setBounds({ 
            x: 0, 
            y: 120, // Leave space for UI header
            width: this.mainWindow.getBounds().width, 
            height: this.mainWindow.getBounds().height - 120 
        });

        // Navigate to the URL
        this.browserView.webContents.loadURL(url);
        
        return this.browserView;
    }

    setupIpcHandlers() {
        // Browser Navigation Handler
        ipcMain.handle('browser-navigate', async (event, url) => {
            try {
                console.log(`🌐 Navigating to: ${url}`);
                
                // Ensure URL has protocol
                if (!url.startsWith('http://') && !url.startsWith('https://')) {
                    url = 'https://' + url;
                }
                
                // Create or update browser view
                this.createBrowserView(url);
                
                return { 
                    success: true, 
                    url: url,
                    message: `Navigated to ${url}` 
                };
            } catch (error) {
                console.error('❌ Navigation Error:', error);
                return { 
                    success: false, 
                    error: error.message 
                };
            }
        });

        // Simple AI Query Handler (placeholder)
        ipcMain.handle('ai-query', async (event, query) => {
            try {
                console.log(`🤖 AI Query: ${query}`);
                
                // For now, return a mock response
                // TODO: Integrate with local AI service
                return {
                    success: true,
                    response: `I understand you want to: ${query}. This is a local AI response!`,
                    commands: []
                };
            } catch (error) {
                console.error('❌ AI Query Error:', error);
                return { 
                    success: false, 
                    error: error.message 
                };
            }
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
            console.log('👋 Kairo AI Browser shutdown complete');
        });
    }
}

// Initialize the application
const kairoApp = new KairoAIBrowser();
kairoApp.setupAppEventHandlers();

// Export for testing
module.exports = KairoAIBrowser;