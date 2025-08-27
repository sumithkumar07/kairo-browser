/**
 * Kairo AI Browser - Preload Script
 * Secure bridge for Browser + AI interface
 */

const { contextBridge, ipcRenderer } = require('electron');

// Secure API Bridge for Browser + AI Interface
contextBridge.exposeInMainWorld('kairoAPI', {
  // AI System
  ai: {
    // Initialize AI system
    initialize: () => ipcRenderer.invoke('ai-initialize'),
    
    // Process natural language input with browser control
    processInput: (input, context) => ipcRenderer.invoke('ai-process-input', input, context),
  },

  // Browser Controls
  browser: {
    // Navigation
    navigate: (url) => ipcRenderer.invoke('browser-navigate', url),
    goBack: () => ipcRenderer.invoke('browser-go-back'),
    goForward: () => ipcRenderer.invoke('browser-go-forward'),
    refresh: () => ipcRenderer.invoke('browser-refresh'),
  },

  // System Information
  system: {
    getInfo: () => ipcRenderer.invoke('system-info'),
  },

  // Error Reporting
  reportError: (errorData) => ipcRenderer.invoke('report-error', errorData),

  // Event Listeners
  on: (channel, func) => {
    const validChannels = ['system-ready', 'browser-updated', 'ai-response'];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, func);
    }
  },

  // Remove Event Listeners
  removeListener: (channel, func) => {
    ipcRenderer.removeListener(channel, func);
  },

  // App Information
  app: {
    getName: () => 'Kairo AI Browser',
    getVersion: () => '2.0.0',
    getMode: () => 'browser-ai-split'
  }
});

// Global error handler
window.addEventListener('error', (error) => {
  ipcRenderer.invoke('report-error', {
    type: 'javascript-error',
    message: error.message,
    filename: error.filename,
    lineno: error.lineno,
    colno: error.colno,
    timestamp: new Date().toISOString()
  });
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
  ipcRenderer.invoke('report-error', {
    type: 'unhandled-promise-rejection',
    reason: event.reason.toString(),
    timestamp: new Date().toISOString()
  });
});

console.log('🔗 Kairo AI Browser Preload Script loaded - Bridge ready');