/**
 * Test Electron Integration
 * Quick test to verify Electron can load websites natively
 */

const { app, BrowserWindow, BrowserView } = require('electron');
const path = require('path');

let mainWindow;
let browserView;

function createWindow() {
    // Create main window
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: false // Allow loading any website
        }
    });

    // Create browser view for YouTube test
    browserView = new BrowserView({
        webPreferences: {
            webSecurity: false,
            allowRunningInsecureContent: true
        }
    });

    mainWindow.addBrowserView(browserView);
    
    // Set browser view bounds
    browserView.setBounds({ x: 0, y: 0, width: 1200, height: 800 });

    // Try to load YouTube directly
    console.log('🎯 Testing direct YouTube access...');
    browserView.webContents.loadURL('https://www.youtube.com');
    
    browserView.webContents.on('did-finish-load', () => {
        console.log('✅ YouTube loaded successfully!');
        console.log('🎉 BREAKTHROUGH: Native Chromium can access YouTube directly!');
        console.log('🚀 This proves the local-first architecture will work!');
    });

    browserView.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
        console.log('❌ YouTube load failed:', errorDescription);
    });

    // Test Netflix after 5 seconds
    setTimeout(() => {
        console.log('🎯 Testing Netflix access...');
        browserView.webContents.loadURL('https://www.netflix.com');
        
        browserView.webContents.on('did-finish-load', () => {
            console.log('✅ Netflix loaded successfully!');
        });
    }, 5000);

    // Test a search query after 10 seconds  
    setTimeout(() => {
        console.log('🎯 Testing YouTube search...');
        browserView.webContents.loadURL('https://www.youtube.com/results?search_query=yeh+raatein+yeh+mausam');
        
        browserView.webContents.on('did-finish-load', () => {
            console.log('✅ YouTube search loaded successfully!');
            console.log('🎯 SUCCESS: We can search for "yeh raatein yeh mausam" directly!');
        });
    }, 10000);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});