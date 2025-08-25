/**
 * Kairo AI Browser - Preload Script
 * Security bridge between main process and renderer
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose safe IPC methods to renderer process
contextBridge.exposeInMainWorld('kairoAPI', {
    // Browser Automation
    browser: {
        navigate: (url) => ipcRenderer.invoke('browser-navigate', url)
    },

    // AI Service (placeholder)
    ai: {
        query: (query) => ipcRenderer.invoke('ai-query', query)
    },

    // Window Management
    window: {
        minimize: () => ipcRenderer.invoke('window-minimize'),
        maximize: () => ipcRenderer.invoke('window-maximize'),
        close: () => ipcRenderer.invoke('window-close')
    },

    // System Info
    system: {
        platform: process.platform,
        isElectron: true
    }
});

console.log('✅ Kairo API exposed to renderer process');