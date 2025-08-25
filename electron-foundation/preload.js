/**
 * Kairo AI Browser - Preload Script
 * Security bridge between main process and renderer
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose safe IPC methods to renderer process
contextBridge.exposeInMainWorld('kairoAPI', {
    // AI Service
    ai: {
        query: (query) => ipcRenderer.invoke('ai-query', query)
    },

    // Browser Automation
    browser: {
        navigate: (url) => ipcRenderer.invoke('browser-navigate', url),
        execute: (command) => ipcRenderer.invoke('browser-execute', command)
    },

    // Local Storage
    storage: {
        get: (key) => ipcRenderer.invoke('storage-get', key),
        set: (key, value) => ipcRenderer.invoke('storage-set', key, value)
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
        version: process.versions
    },

    // Events (for real-time updates)
    on: (channel, callback) => {
        const validChannels = ['browser-update', 'ai-response', 'system-notification'];
        if (validChannels.includes(channel)) {
            ipcRenderer.on(channel, callback);
        }
    },

    off: (channel, callback) => {
        ipcRenderer.removeListener(channel, callback);
    }
});

console.log('✅ Kairo API exposed to renderer process');