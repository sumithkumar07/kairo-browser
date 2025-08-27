/**
 * Enhanced Preload Script - Pure AI Interface Bridge
 */

const { contextBridge, ipcRenderer } = require('electron');

// Secure API Bridge for Pure AI Interface
contextBridge.exposeInMainWorld('kairoAPI', {
  // AI System
  ai: {
    // Initialize AI system
    initialize: () => ipcRenderer.invoke('ai-initialize'),
    
    // Process natural language input
    processInput: (input, context) => ipcRenderer.invoke('ai-process-input', input, context),
    
    // Quick actions
    quickSearch: (query, platforms) => ipcRenderer.invoke('ai-quick-search', query, platforms),
    quickAnalyze: (url) => ipcRenderer.invoke('ai-quick-analyze', url),
    quickCompare: (items) => ipcRenderer.invoke('ai-quick-compare', items),
    
    // Conversation management
    getState: () => ipcRenderer.invoke('ai-get-state'),
    resetConversation: () => ipcRenderer.invoke('ai-reset-conversation')
  },

  // System Information
  system: {
    getInfo: () => ipcRenderer.invoke('system-info'),
    healthCheck: () => ipcRenderer.invoke('health-check')
  },

  // Window Controls
  window: {
    minimize: () => ipcRenderer.invoke('window-minimize'),
    maximize: () => ipcRenderer.invoke('window-maximize'),
    close: () => ipcRenderer.invoke('window-close')
  },

  // Error Reporting
  reportError: (errorData) => ipcRenderer.invoke('report-error', errorData),

  // Event Listeners
  on: (channel, func) => {
    const validChannels = ['ai-initialized', 'ai-response', 'system-notification'];
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
    getName: () => 'Kairo AI Browser - Pure AI',
    getVersion: () => '2.0.0',
    getMode: () => 'pure-ai'
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

console.log('🔗 Enhanced Preload Script loaded - Pure AI Bridge ready');