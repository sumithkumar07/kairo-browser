/**
 * Kairo AI Browser - Preload Script
 * Secure bridge between main process and renderer process
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose secure API to renderer process
contextBridge.exposeInMainWorld('kairoAPI', {
  // System information
  system: {
    isElectron: true,
    getInfo: () => ipcRenderer.invoke('system-info')
  },

  // Browser controls
  browser: {
    navigate: (url) => ipcRenderer.invoke('browser-navigate', url),
    execute: (command, params) => ipcRenderer.invoke('browser-execute', command, params),
    getContent: () => ipcRenderer.invoke('get-page-content'),
    screenshot: (options) => ipcRenderer.invoke('take-screenshot', options)
  },

  // AI integration
  ai: {
    query: (query, context) => ipcRenderer.invoke('ai-query', query, context)
  },

  // Workflow management
  workflow: {
    execute: (workflow) => ipcRenderer.invoke('workflow-execute', workflow)
  },

  // Window controls
  window: {
    minimize: () => ipcRenderer.invoke('window-minimize'),
    maximize: () => ipcRenderer.invoke('window-maximize'),
    close: () => ipcRenderer.invoke('window-close')
  },

  // File operations
  file: {
    save: (filepath, content) => ipcRenderer.invoke('file-save', filepath, content)
  },

  // Event listeners
  on: (channel, callback) => {
    const validChannels = ['chromium-ready', 'workflow-progress', 'ai-response'];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, callback);
    }
  },

  off: (channel, callback) => {
    ipcRenderer.removeListener(channel, callback);
  }
});

// Enhance console with local-first indicators
console.log('🚀 Kairo AI Browser - Local-First Mode Activated');
console.log('🖥️  Running with embedded Chromium engine');
console.log('🤖 AI processing available locally');
console.log('⚡ Native browser automation enabled');