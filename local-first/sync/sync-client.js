/**
 * Sync Client - Local-First Synchronization
 * Handles minimal cloud sync for preferences and workflows
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');

class SyncClient {
  constructor() {
    this.syncEnabled = false;
    this.userId = null;
    this.syncUrl = process.env.KAIRO_SYNC_URL || 'https://sync.kairoai.com';
    this.localDataPath = path.join(os.homedir(), '.kairo-browser');
    this.lastSyncTime = null;
    
    this.ensureLocalDataDir();
  }

  /**
   * Initialize sync client
   */
  async initialize(userId = null, apiKey = null) {
    try {
      this.userId = userId;
      this.apiKey = apiKey;
      
      if (userId && apiKey) {
        this.syncEnabled = true;
        console.log('✅ Sync client initialized for user:', userId);
        
        // Perform initial sync
        await this.performSync();
      } else {
        console.log('📴 Sync disabled - running in offline-only mode');
      }
      
    } catch (error) {
      console.error('❌ Sync initialization failed:', error);
      this.syncEnabled = false;
    }
  }

  /**
   * Ensure local data directory exists
   */
  ensureLocalDataDir() {
    if (!fs.existsSync(this.localDataPath)) {
      fs.mkdirSync(this.localDataPath, { recursive: true });
      console.log('📁 Created local data directory:', this.localDataPath);
    }
  }

  /**
   * Save data locally
   */
  async saveLocal(category, key, data) {
    try {
      const categoryPath = path.join(this.localDataPath, category);
      if (!fs.existsSync(categoryPath)) {
        fs.mkdirSync(categoryPath, { recursive: true });
      }
      
      const filePath = path.join(categoryPath, `${key}.json`);
      const dataWithMeta = {
        data: data,
        timestamp: new Date().toISOString(),
        id: key,
        category: category,
        version: 1
      };
      
      fs.writeFileSync(filePath, JSON.stringify(dataWithMeta, null, 2));
      console.log(`💾 Saved locally: ${category}/${key}`);
      
      // Trigger sync if enabled
      if (this.syncEnabled) {
        this.scheduleSyncUpload(category, key, dataWithMeta);
      }
      
      return true;
    } catch (error) {
      console.error(`❌ Local save failed for ${category}/${key}:`, error);
      return false;
    }
  }

  /**
   * Load data locally
   */
  async loadLocal(category, key) {
    try {
      const filePath = path.join(this.localDataPath, category, `${key}.json`);
      
      if (!fs.existsSync(filePath)) {
        return null;
      }
      
      const fileContent = fs.readFileSync(filePath, 'utf8');
      const dataWithMeta = JSON.parse(fileContent);
      
      console.log(`📂 Loaded locally: ${category}/${key}`);
      return dataWithMeta.data;
      
    } catch (error) {
      console.error(`❌ Local load failed for ${category}/${key}:`, error);
      return null;
    }
  }

  /**
   * List local data
   */
  async listLocal(category) {
    try {
      const categoryPath = path.join(this.localDataPath, category);
      
      if (!fs.existsSync(categoryPath)) {
        return [];
      }
      
      const files = fs.readdirSync(categoryPath);
      const items = [];
      
      for (const file of files) {
        if (file.endsWith('.json')) {
          const key = file.replace('.json', '');
          const data = await this.loadLocal(category, key);
          if (data) {
            items.push({ key, data });
          }
        }
      }
      
      return items;
    } catch (error) {
      console.error(`❌ Local list failed for ${category}:`, error);
      return [];
    }
  }

  /**
   * Delete local data
   */
  async deleteLocal(category, key) {
    try {
      const filePath = path.join(this.localDataPath, category, `${key}.json`);
      
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
        console.log(`🗑️ Deleted locally: ${category}/${key}`);
      }
      
      // Trigger sync deletion if enabled
      if (this.syncEnabled) {
        this.scheduleSyncDeletion(category, key);
      }
      
      return true;
    } catch (error) {
      console.error(`❌ Local delete failed for ${category}/${key}:`, error);
      return false;
    }
  }

  /**
   * Schedule sync upload (debounced)
   */
  scheduleSyncUpload(category, key, data) {
    // Implement debounced sync upload
    clearTimeout(this.syncTimeout);
    this.syncTimeout = setTimeout(() => {
      this.uploadToSync(category, key, data);
    }, 5000); // 5 second delay
  }

  /**
   * Schedule sync deletion (debounced)
   */
  scheduleSyncDeletion(category, key) {
    clearTimeout(this.syncDeleteTimeout);
    this.syncDeleteTimeout = setTimeout(() => {
      this.deleteFromSync(category, key);
    }, 2000); // 2 second delay
  }

  /**
   * Upload data to sync server
   */
  async uploadToSync(category, key, data) {
    if (!this.syncEnabled) return;

    try {
      const payload = {
        userId: this.userId,
        category: category,
        key: key,
        data: data,
        timestamp: new Date().toISOString()
      };

      await this.makeRequest('POST', '/api/sync/upload', payload);
      console.log(`☁️ Synced to cloud: ${category}/${key}`);
      
    } catch (error) {
      console.error(`❌ Sync upload failed for ${category}/${key}:`, error);
      // Continue working offline
    }
  }

  /**
   * Download data from sync server
   */
  async downloadFromSync(category, key) {
    if (!this.syncEnabled) return null;

    try {
      const response = await this.makeRequest('GET', `/api/sync/download/${category}/${key}`);
      console.log(`☁️ Downloaded from cloud: ${category}/${key}`);
      return response.data;
      
    } catch (error) {
      console.error(`❌ Sync download failed for ${category}/${key}:`, error);
      return null;
    }
  }

  /**
   * Delete from sync server
   */
  async deleteFromSync(category, key) {
    if (!this.syncEnabled) return;

    try {
      await this.makeRequest('DELETE', `/api/sync/delete/${category}/${key}`);
      console.log(`☁️ Deleted from cloud: ${category}/${key}`);
      
    } catch (error) {
      console.error(`❌ Sync delete failed for ${category}/${key}:`, error);
    }
  }

  /**
   * Perform full sync
   */
  async performSync() {
    if (!this.syncEnabled) return;

    try {
      console.log('🔄 Performing full sync...');
      
      const syncData = await this.makeRequest('GET', '/api/sync/list');
      
      // Download any newer items from cloud
      for (const item of syncData.items || []) {
        const localData = await this.loadLocal(item.category, item.key);
        
        if (!localData || new Date(item.timestamp) > new Date(localData.timestamp)) {
          const cloudData = await this.downloadFromSync(item.category, item.key);
          if (cloudData) {
            await this.saveLocal(item.category, item.key, cloudData);
          }
        }
      }
      
      this.lastSyncTime = new Date();
      console.log('✅ Full sync completed');
      
    } catch (error) {
      console.error('❌ Full sync failed:', error);
    }
  }

  /**
   * Make HTTP request to sync server
   */
  async makeRequest(method, endpoint, data = null) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.syncUrl + endpoint);
      
      const options = {
        hostname: url.hostname,
        port: url.port || 443,
        path: url.pathname + url.search,
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`,
          'User-Agent': 'Kairo-Browser-Local/1.0.0'
        }
      };

      const req = https.request(options, (res) => {
        let responseData = '';
        
        res.on('data', (chunk) => {
          responseData += chunk;
        });
        
        res.on('end', () => {
          try {
            const response = JSON.parse(responseData);
            if (res.statusCode >= 200 && res.statusCode < 300) {
              resolve(response);
            } else {
              reject(new Error(response.error || `HTTP ${res.statusCode}`));
            }
          } catch (error) {
            reject(new Error(`Failed to parse response: ${error.message}`));
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`Request failed: ${error.message}`));
      });

      if (data) {
        req.write(JSON.stringify(data));
      }
      
      req.end();
    });
  }

  /**
   * Get sync status
   */
  getSyncStatus() {
    return {
      enabled: this.syncEnabled,
      userId: this.userId,
      lastSync: this.lastSyncTime,
      localDataPath: this.localDataPath
    };
  }

  /**
   * Disable sync
   */
  disableSync() {
    this.syncEnabled = false;
    this.userId = null;
    this.apiKey = null;
    console.log('📴 Sync disabled');
  }
}

module.exports = SyncClient;