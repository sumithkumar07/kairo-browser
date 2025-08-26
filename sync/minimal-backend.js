/**
 * Minimal Sync Backend - Local-First Architecture
 * Lightweight cloud sync server for preferences only
 */

const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');

class MinimalSyncBackend {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 8080;
    this.users = new Map(); // In production, use proper database
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    // CORS
    this.app.use(cors({
      origin: ['http://localhost:3000', 'http://localhost:8001'],
      credentials: true
    }));

    // Rate limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100 // limit each IP to 100 requests per windowMs
    });
    this.app.use(limiter);

    // JSON parsing
    this.app.use(express.json({ limit: '10mb' }));

    // Logging
    this.app.use((req, res, next) => {
      console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
      next();
    });
  }

  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ 
        status: 'healthy', 
        service: 'kairo-sync-minimal',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      });
    });

    // User sync data endpoints
    this.app.post('/api/sync/upload', this.authenticateUser, (req, res) => {
      try {
        const { userId, category, key, data } = req.body;
        
        if (!userId || !category || !key || !data) {
          return res.status(400).json({ error: 'Missing required fields' });
        }

        // Store user data
        if (!this.users.has(userId)) {
          this.users.set(userId, new Map());
        }
        
        const userData = this.users.get(userId);
        if (!userData.has(category)) {
          userData.set(category, new Map());
        }
        
        userData.get(category).set(key, {
          data: data,
          timestamp: new Date().toISOString(),
          id: key,
          category: category
        });

        res.json({ success: true, message: 'Data uploaded successfully' });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    this.app.get('/api/sync/download/:category/:key', this.authenticateUser, (req, res) => {
      try {
        const { category, key } = req.params;
        const userId = req.userId;
        
        const userData = this.users.get(userId);
        if (!userData || !userData.has(category)) {
          return res.status(404).json({ error: 'Data not found' });
        }
        
        const categoryData = userData.get(category);
        const item = categoryData.get(key);
        
        if (!item) {
          return res.status(404).json({ error: 'Data not found' });
        }

        res.json({ success: true, data: item.data, timestamp: item.timestamp });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    this.app.get('/api/sync/list', this.authenticateUser, (req, res) => {
      try {
        const userId = req.userId;
        const userData = this.users.get(userId);
        
        if (!userData) {
          return res.json({ success: true, items: [] });
        }

        const items = [];
        for (const [category, categoryData] of userData.entries()) {
          for (const [key, item] of categoryData.entries()) {
            items.push({
              category: category,
              key: key,
              timestamp: item.timestamp
            });
          }
        }

        res.json({ success: true, items: items });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    this.app.delete('/api/sync/delete/:category/:key', this.authenticateUser, (req, res) => {
      try {
        const { category, key } = req.params;
        const userId = req.userId;
        
        const userData = this.users.get(userId);
        if (userData && userData.has(category)) {
          userData.get(category).delete(key);
        }

        res.json({ success: true, message: 'Data deleted successfully' });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    // Analytics endpoint (minimal)
    this.app.get('/api/analytics', (req, res) => {
      res.json({
        success: true,
        stats: {
          totalUsers: this.users.size,
          totalSyncedItems: Array.from(this.users.values())
            .reduce((total, userData) => {
              return total + Array.from(userData.values())
                .reduce((catTotal, catData) => catTotal + catData.size, 0);
            }, 0),
          timestamp: new Date().toISOString()
        }
      });
    });

    // Catch-all for undefined routes
    this.app.use('*', (req, res) => {
      res.status(404).json({ 
        error: 'Endpoint not found',
        message: 'This is a minimal sync server for Kairo AI Browser local-first architecture'
      });
    });
  }

  // Simple authentication middleware
  authenticateUser = (req, res, next) => {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    // In production, validate JWT token properly
    // For demo, extract userId from token directly
    const token = authHeader.substring(7);
    req.userId = token; // Simplified - in production, decode JWT
    
    next();
  };

  start() {
    this.app.listen(this.port, () => {
      console.log(`🚀 Kairo Sync Server running on port ${this.port}`);
      console.log(`📊 Health check: http://localhost:${this.port}/health`);
      console.log(`💾 Data storage: In-memory (use proper DB in production)`);
      console.log(`🔒 CORS enabled for local development`);
    });
  }
}

// Start server if run directly
if (require.main === module) {
  const server = new MinimalSyncBackend();
  server.start();
}

module.exports = MinimalSyncBackend;