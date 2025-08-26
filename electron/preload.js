const { contextBridge, ipcRenderer } = require('electron');

// Expose safe APIs to renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // App information
  getAppInfo: () => ipcRenderer.invoke('get-app-info'),
  
  // Browser automation (to be implemented in Phase 2)
  navigateToUrl: (url) => ipcRenderer.invoke('navigate-to-url', url),
  executeBrowserCommand: (command) => ipcRenderer.invoke('execute-browser-command', command),
  createNewTab: (sessionId) => ipcRenderer.invoke('create-new-tab', sessionId),
  closeTab: (sessionId) => ipcRenderer.invoke('close-tab', sessionId),
  
  // AI processing (to be implemented in Phase 3)
  processAIQuery: (query, context) => ipcRenderer.invoke('process-ai-query', query, context),
  
  // Local data storage
  saveSession: (sessionData) => ipcRenderer.invoke('save-session', sessionData),
  loadSession: (sessionId) => ipcRenderer.invoke('load-session', sessionId),
  
  // History management
  saveToHistory: (historyItem) => ipcRenderer.invoke('save-to-history', historyItem),
  getHistory: (limit) => ipcRenderer.invoke('get-history', limit),
  
  // Settings management
  getSetting: (key) => ipcRenderer.invoke('get-setting', key),
  setSetting: (key, value) => ipcRenderer.invoke('set-setting', key, value),
  
  // System controls
  minimizeWindow: () => ipcRenderer.send('minimize-window'),
  maximizeWindow: () => ipcRenderer.send('maximize-window'),
  closeWindow: () => ipcRenderer.send('close-window'),
  
  // Development helpers
  openDevTools: () => ipcRenderer.send('open-dev-tools'),
  
  // Event listeners for communication from main process
  onNavigationComplete: (callback) => ipcRenderer.on('navigation-complete', callback),
  onAIResponse: (callback) => ipcRenderer.on('ai-response', callback),
  onBrowserEvent: (callback) => ipcRenderer.on('browser-event', callback),
  
  // Remove event listeners
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel)
});

// Development mode detection
contextBridge.exposeInMainWorld('isDevelopment', process.env.NODE_ENV === 'development');

// Platform information
contextBridge.exposeInMainWorld('platform', process.platform);

console.log('🔗 Electron preload script loaded - IPC bridge ready');