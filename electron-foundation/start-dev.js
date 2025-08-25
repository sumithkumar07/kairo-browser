/**
 * Development starter for Kairo AI Browser Electron app
 * Connects to the existing React development server
 */

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

// Handle sandbox issues in containerized environments
app.commandLine.appendSwitch('--no-sandbox');
app.commandLine.appendSwitch('--disable-setuid-sandbox');

let mainWindow;

async function createWindow() {
    console.log('🚀 Starting Kairo AI Browser in Electron...');
    
    // Create the browser window
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: false, // Allow loading any website
            preload: path.join(__dirname, 'preload.js')
        },
        show: false
    });

    // Load the React development server
    await mainWindow.loadURL('http://localhost:3000');
    
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        console.log('✅ Kairo AI Browser loaded in Electron!');
        console.log('🎯 Now testing native website access...');
        
        // Open DevTools to see console
        mainWindow.webContents.openDevTools();
    });

    // Test native website access after window loads
    setTimeout(() => {
        testNativeWebsiteAccess();
    }, 3000);
}

function testNativeWebsiteAccess() {
    console.log('🧪 Testing if Electron can access websites directly...');
    
    // This simulates what happens when we use BrowserView
    const { BrowserView } = require('electron');
    
    const testView = new BrowserView({
        webPreferences: {
            webSecurity: false,
            allowRunningInsecureContent: true
        }
    });

    // Try loading YouTube
    testView.webContents.loadURL('https://www.youtube.com');
    
    testView.webContents.on('did-finish-load', () => {
        console.log('🎉 SUCCESS: YouTube loaded in native Electron BrowserView!');
        console.log('✅ This confirms local-first architecture will work!');
        
        // Clean up test view
        testView.destroy();
    });

    testView.webContents.on('did-fail-load', (event, errorCode, errorDescription) => {
        console.log('❌ YouTube test failed:', errorDescription);
        testView.destroy();
    });
}

// IPC handlers for React app communication
ipcMain.handle('test-native-navigation', async (event, url) => {
    console.log(`🧪 Testing native navigation to: ${url}`);
    
    try {
        const { BrowserView } = require('electron');
        
        const browserView = new BrowserView({
            webPreferences: {
                webSecurity: false,
                allowRunningInsecureContent: true
            }
        });

        mainWindow.addBrowserView(browserView);
        
        // Position the browser view (leave space for UI)
        const bounds = mainWindow.getBounds();
        browserView.setBounds({ 
            x: 0, 
            y: 120, 
            width: bounds.width, 
            height: bounds.height - 120 
        });

        // Load the URL
        await browserView.webContents.loadURL(url);
        
        return { 
            success: true, 
            message: `Successfully loaded ${url} in native browser view`,
            method: 'native_electron_browserview'
        };
        
    } catch (error) {
        console.error('❌ Native navigation failed:', error);
        return { 
            success: false, 
            error: error.message 
        };
    }
});

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

console.log('🔄 Electron app starting...');