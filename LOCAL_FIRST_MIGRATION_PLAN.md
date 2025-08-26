# 🚀 LOCAL-FIRST ARCHITECTURE MIGRATION PLAN

## 📋 MIGRATION OVERVIEW

**Goal:** Transform Kairo AI Browser from server-first to local-first orchestration where:
- ✅ All tasks (AI, automation, browsing) run on user's machine
- ✅ Direct internet access without proxy restrictions  
- ✅ Local browser engine with full functionality
- ✅ Backend only for syncing/updates (optional)

---

## 🏗️ NEW LOCAL-FIRST ARCHITECTURE

### 1. **Frontend Layer (Electron-wrapped React)**
```
📱 Electron App Container
├── 🎨 React UI Components (existing)
├── 🖥️ Native Browser Window Management
├── 📊 Local Data Storage Interface
└── 🔗 IPC Communication Layer
```

### 2. **Local Runtime (User's Machine)**
```
🧠 Local Orchestration Engine
├── 🌐 Embedded Chromium Browser Engine
├── 🤖 AI Command Processor (direct API calls)
├── 🔄 Browser Automation Engine
├── 💾 Local Data Storage (SQLite)
├── 📡 Session Management
└── 🔧 Configuration Manager
```

### 3. **Minimal Cloud Backend (Optional)**
```
☁️ Sync & Update Service
├── 👤 User Accounts (optional)
├── 🔄 Settings Sync
├── 📦 App Updates
└── 📊 Usage Analytics (anonymized)
```

---

## 🔄 STEP-BY-STEP MIGRATION PLAN

### **Phase 1: Setup Local Environment**

#### 1.1 Initialize Electron Project
```bash
# Install Electron development dependencies
npm install --save-dev electron electron-builder
npm install --save electron-store sqlite3 node-fetch
```

#### 1.2 Create Electron Main Process
**File:** `/app/electron/main.js`
```javascript
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const Store = require('electron-store');
const sqlite3 = require('sqlite3').verbose();

// Local data storage
const store = new Store();
let mainWindow;
let db;

// Initialize local database
function initDatabase() {
  db = new sqlite3.Database('./kairo_local.db');
  
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
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'hidden',
    frame: false
  });

  // Load React app
  const isDev = process.env.NODE_ENV === 'development';
  if (isDev) {
    mainWindow.loadURL('http://localhost:3000');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../build/index.html'));
  }
}

app.whenReady().then(() => {
  initDatabase();
  createWindow();
});
```

#### 1.3 Create IPC Preload Script
**File:** `/app/electron/preload.js`
```javascript
const { contextBridge, ipcRenderer } = require('electron');

// Expose safe APIs to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Browser automation
  navigateToUrl: (url) => ipcRenderer.invoke('navigate-to-url', url),
  executeBrowserCommand: (command) => ipcRenderer.invoke('execute-browser-command', command),
  
  // AI processing
  processAIQuery: (query, context) => ipcRenderer.invoke('process-ai-query', query, context),
  
  // Local data storage
  saveSession: (sessionData) => ipcRenderer.invoke('save-session', sessionData),
  loadSession: (sessionId) => ipcRenderer.invoke('load-session', sessionId),
  
  // System controls
  minimizeWindow: () => ipcRenderer.send('minimize-window'),
  maximizeWindow: () => ipcRenderer.send('maximize-window'),
  closeWindow: () => ipcRenderer.send('close-window')
});
```

### **Phase 2: Local Browser Engine Integration**

#### 2.1 Install Chromium Embedded Framework
```bash
# Add CEF dependency for local browser engine
npm install --save puppeteer-core chromium
```

#### 2.2 Create Local Browser Engine
**File:** `/app/electron/browser-engine.js`
```javascript
const puppeteer = require('puppeteer-core');
const chromium = require('chromium');
const path = require('path');

class LocalBrowserEngine {
  constructor() {
    this.browser = null;
    this.pages = new Map(); // Track open pages/tabs
  }

  async initialize() {
    try {
      this.browser = await puppeteer.launch({
        executablePath: chromium.path,
        headless: false,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-web-security',
          '--allow-running-insecure-content',
          '--disable-features=VizDisplayCompositor'
        ],
        userDataDir: path.join(process.cwd(), 'user-data')
      });
      
      console.log('Local browser engine initialized');
      return true;
    } catch (error) {
      console.error('Failed to initialize browser engine:', error);
      return false;
    }
  }

  async createTab(sessionId) {
    if (!this.browser) return null;
    
    try {
      const page = await this.browser.newPage();
      
      // Set realistic viewport and user agent
      await page.setViewport({ width: 1920, height: 1080 });
      await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
      
      this.pages.set(sessionId, page);
      return page;
    } catch (error) {
      console.error('Failed to create tab:', error);
      return null;
    }
  }

  async navigateToUrl(sessionId, url) {
    const page = this.pages.get(sessionId);
    if (!page) return { success: false, error: 'No active page' };

    try {
      const response = await page.goto(url, { 
        waitUntil: 'networkidle2',
        timeout: 30000 
      });
      
      const title = await page.title();
      return { 
        success: true, 
        url: page.url(), 
        title,
        status: response.status()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async executeCommand(sessionId, command) {
    const page = this.pages.get(sessionId);
    if (!page) return { success: false, error: 'No active page' };

    try {
      switch (command.type) {
        case 'click':
          await page.click(command.selector);
          break;
        case 'type':
          await page.type(command.selector, command.text);
          break;
        case 'scroll':
          await page.evaluate(() => window.scrollBy(0, 500));
          break;
        case 'screenshot':
          const screenshot = await page.screenshot({ encoding: 'base64' });
          return { success: true, screenshot };
        default:
          return { success: false, error: 'Unknown command' };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  async getPageContent(sessionId) {
    const page = this.pages.get(sessionId);
    if (!page) return null;

    try {
      const content = await page.content();
      const title = await page.title();
      const url = page.url();
      
      return { content, title, url };
    } catch (error) {
      console.error('Failed to get page content:', error);
      return null;
    }
  }

  async closePage(sessionId) {
    const page = this.pages.get(sessionId);
    if (page) {
      await page.close();
      this.pages.delete(sessionId);
    }
  }

  async shutdown() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }
}

module.exports = LocalBrowserEngine;
```

### **Phase 3: Local AI Processing**

#### 3.1 Create Local AI Handler
**File:** `/app/electron/ai-processor.js`
```javascript
const fetch = require('node-fetch');

class LocalAIProcessor {
  constructor() {
    // Use environment variable or user-provided API key
    this.groqApiKey = process.env.GROQ_API_KEY || null;
    this.apiEndpoint = 'https://api.groq.com/openai/v1/chat/completions';
  }

  setApiKey(apiKey) {
    this.groqApiKey = apiKey;
  }

  async processQuery(query, context = {}) {
    if (!this.groqApiKey) {
      return {
        success: false,
        error: 'AI API key not configured. Please add your Groq API key in settings.'
      };
    }

    try {
      const systemPrompt = `You are Kairo AI, running locally on the user's machine. You help users navigate and interact with websites through natural language commands.

Available browser actions:
- navigate: Go to a URL
- click: Click on an element (provide CSS selector)
- type: Type text into an input field  
- scroll: Scroll the page
- screenshot: Take a screenshot
- search: Search on current page

You have DIRECT access to real websites without restrictions. No proxies needed.

Respond with JSON:
{
  "intent": "what user wants",
  "commands": [
    {
      "type": "action_type",
      "params": {
        "url": "url if needed",
        "selector": "css selector if needed",
        "text": "text to type if needed"
      }
    }
  ],
  "explanation": "what you'll do"
}`;

      const response = await fetch(this.apiEndpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.groqApiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'llama3-8b-8192',
          messages: [
            { role: 'system', content: systemPrompt },
            { role: 'user', content: query }
          ],
          temperature: 0.3,
          max_tokens: 1000
        })
      });

      const result = await response.json();
      
      if (!response.ok) {
        throw new Error(result.error?.message || 'AI API request failed');
      }

      const aiResponse = result.choices[0].message.content;
      
      // Parse JSON response
      let parsedResponse;
      try {
        const jsonStart = aiResponse.indexOf('{');
        const jsonEnd = aiResponse.lastIndexOf('}') + 1;
        const jsonContent = aiResponse.slice(jsonStart, jsonEnd);
        parsedResponse = JSON.parse(jsonContent);
      } catch (parseError) {
        parsedResponse = {
          intent: query,
          commands: [],
          explanation: aiResponse
        };
      }

      return {
        success: true,
        response: parsedResponse
      };

    } catch (error) {
      console.error('AI processing error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
}

module.exports = LocalAIProcessor;
```

### **Phase 4: Update React Frontend for Local**

#### 4.1 Update App.js for Electron
**Replace existing API calls with Electron IPC:**

```javascript
// Instead of: fetch(`${backendUrl}/api/ai/query`, ...)
// Use: await window.electronAPI.processAIQuery(query, context)

// Instead of: fetch(`${backendUrl}/api/browser/execute`, ...)  
// Use: await window.electronAPI.executeBrowserCommand(command)

// Instead of: fetch(`${backendUrl}/api/proxy`, ...)
// Use: await window.electronAPI.navigateToUrl(url) // Direct navigation
```

#### 4.2 Update Context Provider
**File:** `/app/frontend/src/contexts/LocalSessionContext.js`
```javascript
import React, { createContext, useContext, useState, useEffect } from 'react';

const LocalSessionContext = createContext();

export const useLocalSession = () => {
  const context = useContext(LocalSessionContext);
  if (!context) {
    throw new Error('useLocalSession must be used within a LocalSessionProvider');
  }
  return context;
};

export const LocalSessionProvider = ({ children }) => {
  const [sessionId, setSessionId] = useState(null);
  const [currentUrl, setCurrentUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const generateSessionId = () => {
      return 'local_session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    };
    setSessionId(generateSessionId());
  }, []);

  // Local navigation (direct browser access)
  const navigateToUrl = async (url) => {
    setIsLoading(true);
    try {
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = 'https://' + url;
      }
      
      const result = await window.electronAPI.navigateToUrl(url);
      
      if (result.success) {
        setCurrentUrl(result.url);
        setHistory(prev => [...prev, { 
          url: result.url, 
          title: result.title,
          timestamp: new Date() 
        }]);
      }
      
      return result;
    } catch (error) {
      console.error('Local navigation error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Local AI processing
  const processAIQuery = async (query, context = {}) => {
    try {
      setIsLoading(true);
      
      const result = await window.electronAPI.processAIQuery(query, {
        currentUrl,
        sessionId,
        ...context
      });
      
      return result;
    } catch (error) {
      console.error('Local AI query error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Local browser commands
  const executeBrowserCommand = async (command) => {
    try {
      const result = await window.electronAPI.executeBrowserCommand({
        sessionId,
        ...command
      });
      
      return result;
    } catch (error) {
      console.error('Local browser command error:', error);
      throw error;
    }
  };

  const value = {
    sessionId,
    currentUrl,
    isLoading,
    history,
    navigateToUrl,
    processAIQuery,
    executeBrowserCommand,
    setCurrentUrl
  };

  return (
    <LocalSessionContext.Provider value={value}>
      {children}
    </LocalSessionContext.Provider>
  );
};
```

### **Phase 5: Main Process IPC Handlers**

#### 5.1 Add IPC Handlers to main.js
```javascript
const LocalBrowserEngine = require('./browser-engine');
const LocalAIProcessor = require('./ai-processor');

const browserEngine = new LocalBrowserEngine();
const aiProcessor = new LocalAIProcessor();

// Initialize on app ready
app.whenReady().then(async () => {
  initDatabase();
  createWindow();
  
  // Initialize local browser engine
  await browserEngine.initialize();
});

// IPC Handlers
ipcMain.handle('navigate-to-url', async (event, url) => {
  const sessionId = 'main_session'; // Could be dynamic
  await browserEngine.createTab(sessionId);
  return await browserEngine.navigateToUrl(sessionId, url);
});

ipcMain.handle('execute-browser-command', async (event, command) => {
  return await browserEngine.executeCommand(command.sessionId, command);
});

ipcMain.handle('process-ai-query', async (event, query, context) => {
  return await aiProcessor.processQuery(query, context);
});

ipcMain.handle('save-session', async (event, sessionData) => {
  return new Promise((resolve, reject) => {
    db.run("INSERT OR REPLACE INTO sessions (id, data) VALUES (?, ?)", 
      [sessionData.id, JSON.stringify(sessionData)], 
      function(err) {
        if (err) reject(err);
        else resolve({ success: true });
      });
  });
});

ipcMain.handle('load-session', async (event, sessionId) => {
  return new Promise((resolve, reject) => {
    db.get("SELECT * FROM sessions WHERE id = ?", [sessionId], (err, row) => {
      if (err) reject(err);
      else resolve(row ? JSON.parse(row.data) : null);
    });
  });
});

// Window controls
ipcMain.on('minimize-window', () => mainWindow.minimize());
ipcMain.on('maximize-window', () => {
  if (mainWindow.isMaximized()) {
    mainWindow.unmaximize();
  } else {
    mainWindow.maximize();
  }
});
ipcMain.on('close-window', () => mainWindow.close());

// Cleanup on app exit
app.on('before-quit', async () => {
  await browserEngine.shutdown();
});
```

### **Phase 6: Package Scripts & Build**

#### 6.1 Update package.json
```json
{
  "main": "electron/main.js",
  "scripts": {
    "electron": "electron .",
    "electron-dev": "NODE_ENV=development electron .",
    "build-electron": "npm run build && electron-builder",
    "dist": "npm run build && electron-builder --publish=never"
  },
  "build": {
    "appId": "com.kairo.ai-browser",
    "productName": "Kairo AI Browser",
    "directories": {
      "output": "dist"
    },
    "files": [
      "build/**/*",
      "electron/**/*",
      "node_modules/**/*"
    ],
    "mac": {
      "category": "public.app-category.productivity"
    },
    "win": {
      "target": "nsis"
    },
    "linux": {
      "target": "AppImage"
    }
  }
}
```

---

## 🗂️ FINAL FILE STRUCTURE

```
/app/
├── electron/                    # Local runtime
│   ├── main.js                 # Electron main process
│   ├── preload.js              # IPC bridge
│   ├── browser-engine.js       # Local Chromium engine
│   └── ai-processor.js         # Local AI processing
├── frontend/                   # React UI (electron-wrapped)
│   ├── src/
│   │   ├── contexts/LocalSessionContext.js
│   │   └── components/         # Existing components (minimal changes)
│   └── public/
├── build/                      # Built React app
├── dist/                       # Packaged Electron app
├── user-data/                  # Local browser data
├── kairo_local.db             # Local SQLite database
└── package.json               # Updated with Electron
```

---

## ✅ MIGRATION BENEFITS

**🚀 Better Internet Access:**
- ✅ Direct website access (no proxy restrictions)
- ✅ Full YouTube functionality with real videos
- ✅ Better authentication and cookies
- ✅ Faster performance (no server bottleneck)
- ✅ Complete JavaScript support

**🔒 Privacy & Performance:**
- ✅ User data stays local
- ✅ No server costs for execution
- ✅ Works offline (except AI API calls)
- ✅ Unlimited website access

**📦 User Experience:**
- ✅ Native app feel
- ✅ Better system integration
- ✅ Auto-updates possible
- ✅ No browser restrictions

---

## 🚦 MIGRATION STEPS SUMMARY

1. **✅ Phase 1:** Setup Electron environment
2. **✅ Phase 2:** Integrate local browser engine  
3. **✅ Phase 3:** Setup local AI processing
4. **✅ Phase 4:** Update React frontend for local IPC
5. **✅ Phase 5:** Implement IPC communication
6. **✅ Phase 6:** Package and distribute

This migration will transform your app into a true local-first architecture with direct internet access and better website compatibility!