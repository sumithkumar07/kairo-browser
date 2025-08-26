const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');
const Store = require('electron-store');
const sqlite3 = require('sqlite3').verbose();

// Disable sandbox for compatibility
app.commandLine.appendSwitch('--no-sandbox');
app.commandLine.appendSwitch('--disable-setuid-sandbox');

// Local data storage
const store = new Store();
let mainWindow;
let db;

// Initialize local database
function initDatabase() {
  const dbPath = path.join(app.getPath('userData'), 'kairo_local.db');
  db = new sqlite3.Database(dbPath);
  
  console.log('📂 Database initialized at:', dbPath);
  
  // Create tables for local storage
  db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      data TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
    
    db.run(`CREATE TABLE IF NOT EXISTS ai_interactions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id TEXT,
      query TEXT,
      response TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
    
    db.run(`CREATE TABLE IF NOT EXISTS browser_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id TEXT,
      url TEXT,
      title TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);
    
    console.log('✅ Database tables created successfully');
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
      webSecurity: false // Allow loading external content
    },
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    show: false, // Don't show until ready
    icon: path.join(__dirname, '../frontend/public/favicon.ico')
  });

  // Load React app
  const isDev = process.env.NODE_ENV === 'development';
  if (isDev) {
    mainWindow.loadURL('http://localhost:3000');
    // Open DevTools in development
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../frontend/build/index.html'));
  }

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    console.log('🚀 Kairo AI Browser (Local-First) Ready!');
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Create application menu
function createMenu() {
  const template = [
    {
      label: 'Kairo AI Browser',
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideothers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
        { role: 'selectall' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Window',
      submenu: [
        { role: 'minimize' },
        { role: 'close' }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// App event handlers
app.whenReady().then(async () => {
  console.log('🔧 Initializing Kairo AI Browser Local-First Edition...');
  
  // Disable sandbox for root execution
  app.commandLine.appendSwitch('--no-sandbox');
  app.commandLine.appendSwitch('--disable-setuid-sandbox');
  
  initDatabase();
  createMenu();
  createWindow();
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Basic IPC Handlers (will be expanded)
ipcMain.handle('get-app-info', async () => {
  return {
    appName: 'Kairo AI Browser',
    version: app.getVersion(),
    platform: process.platform,
    arch: process.arch,
    isLocalFirst: true
  };
});

ipcMain.handle('save-session', async (event, sessionData) => {
  return new Promise((resolve, reject) => {
    db.run("INSERT OR REPLACE INTO sessions (id, data) VALUES (?, ?)", 
      [sessionData.id, JSON.stringify(sessionData)], 
      function(err) {
        if (err) {
          console.error('❌ Failed to save session:', err);
          reject(err);
        } else {
          console.log('✅ Session saved:', sessionData.id);
          resolve({ success: true, sessionId: sessionData.id });
        }
      });
  });
});

ipcMain.handle('load-session', async (event, sessionId) => {
  return new Promise((resolve, reject) => {
    db.get("SELECT * FROM sessions WHERE id = ?", [sessionId], (err, row) => {
      if (err) {
        console.error('❌ Failed to load session:', err);
        reject(err);
      } else {
        const sessionData = row ? JSON.parse(row.data) : null;
        console.log('📖 Session loaded:', sessionId, sessionData ? '✅' : '❌');
        resolve(sessionData);
      }
    });
  });
});

// Window controls
ipcMain.on('minimize-window', () => {
  if (mainWindow) mainWindow.minimize();
});

ipcMain.on('maximize-window', () => {
  if (mainWindow) {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  }
});

ipcMain.on('close-window', () => {
  if (mainWindow) mainWindow.close();
});

// Cleanup on app exit
app.on('before-quit', async () => {
  console.log('🔄 Cleaning up before quit...');
  
  if (db) {
    db.close((err) => {
      if (err) {
        console.error('❌ Error closing database:', err);
      } else {
        console.log('✅ Database closed successfully');
      }
    });
  }
});

// Error handling
process.on('uncaughtException', (error) => {
  console.error('❌ Uncaught Exception:', error);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('❌ Unhandled Rejection at:', promise, 'reason:', reason);
});