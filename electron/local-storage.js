const Store = require('electron-store');
const path = require('path');
const { app } = require('electron');

class LocalStorage {
  constructor() {
    this.store = new Store({
      name: 'kairo-ai-browser',
      defaults: {
        windowBounds: {
          width: 1400,
          height: 900
        },
        userPreferences: {
          stealth_level: 5,
          rendering_profile: 'balanced',
          prefer_speed: false,
          prefer_reliability: true,
          theme: 'light'
        },
        bookmarks: [
          { name: 'YouTube', url: 'https://youtube.com', favicon: '🎥' },
          { name: 'Google', url: 'https://google.com', favicon: '🔍' },
          { name: 'GitHub', url: 'https://github.com', favicon: '👨‍💻' },
          { name: 'LinkedIn', url: 'https://linkedin.com', favicon: '💼' }
        ],
        recentSites: []
      }
    });
    
    console.log('💾 Local storage initialized at:', this.store.path);
  }

  // Window state management
  getWindowBounds() {
    return this.store.get('windowBounds');
  }

  setWindowBounds(bounds) {
    this.store.set('windowBounds', bounds);
  }

  // User preferences
  getUserPreferences() {
    return this.store.get('userPreferences');
  }

  setUserPreferences(preferences) {
    this.store.set('userPreferences', preferences);
  }

  updateUserPreference(key, value) {
    this.store.set(`userPreferences.${key}`, value);
  }

  // Bookmarks management
  getBookmarks() {
    return this.store.get('bookmarks');
  }

  addBookmark(bookmark) {
    const bookmarks = this.getBookmarks();
    bookmarks.push(bookmark);
    this.store.set('bookmarks', bookmarks);
  }

  removeBookmark(url) {
    const bookmarks = this.getBookmarks().filter(b => b.url !== url);
    this.store.set('bookmarks', bookmarks);
  }

  // Recent sites
  getRecentSites() {
    return this.store.get('recentSites', []);
  }

  addRecentSite(site) {
    let recent = this.getRecentSites();
    
    // Remove if already exists
    recent = recent.filter(r => r.url !== site.url);
    
    // Add to beginning
    recent.unshift(site);
    
    // Keep only last 20
    recent = recent.slice(0, 20);
    
    this.store.set('recentSites', recent);
  }

  // Generic settings
  getSetting(key, defaultValue = null) {
    return this.store.get(key, defaultValue);
  }

  setSetting(key, value) {
    this.store.set(key, value);
  }

  // Clear all data
  clearAllData() {
    this.store.clear();
    console.log('🗑️ All local data cleared');
  }

  // Export/Import settings
  exportSettings() {
    return {
      userPreferences: this.getUserPreferences(),
      bookmarks: this.getBookmarks(),
      recentSites: this.getRecentSites()
    };
  }

  importSettings(settings) {
    if (settings.userPreferences) {
      this.setUserPreferences(settings.userPreferences);
    }
    if (settings.bookmarks) {
      this.store.set('bookmarks', settings.bookmarks);
    }
    if (settings.recentSites) {
      this.store.set('recentSites', settings.recentSites);
    }
    console.log('📥 Settings imported successfully');
  }
}

module.exports = LocalStorage;