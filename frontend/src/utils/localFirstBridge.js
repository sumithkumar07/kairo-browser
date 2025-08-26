/**
 * Local-First API Bridge
 * Replaces backend API calls with Electron IPC calls
 */

class LocalFirstBridge {
  constructor() {
    this.isElectron = window.kairoAPI !== undefined;
    this.backendUrl = process.env.REACT_APP_BACKEND_URL;
  }

  /**
   * AI Query Processing
   */
  async processAIQuery(query, context = {}) {
    if (this.isElectron) {
      // Use Electron IPC for local-first mode
      return await window.kairoAPI.ai.query(query, context);
    } else {
      // Fallback to backend API for server-first mode
      const response = await fetch(`${this.backendUrl}/api/ai/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, context })
      });
      return await response.json();
    }
  }

  /**
   * Multimodal AI Query (enhanced)
   */
  async processMultimodalQuery(query, context = {}) {
    if (this.isElectron) {
      // Use enhanced AI processing in local-first mode
      return await window.kairoAPI.ai.query(query, {
        ...context,
        multimodal: true,
        enhanced: true
      });
    } else {
      // Fallback to backend API
      const response = await fetch(`${this.backendUrl}/api/ai/multimodal-query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, context })
      });
      return await response.json();
    }
  }

  /**
   * Browser Navigation
   */
  async navigateToUrl(url) {
    if (this.isElectron) {
      // Direct browser navigation in local-first mode
      return await window.kairoAPI.browser.navigate(url);
    } else {
      // Proxy navigation in server-first mode
      const response = await fetch(`${this.backendUrl}/api/browser/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          command: 'navigate',
          params: { url }
        })
      });
      return await response.json();
    }
  }

  /**
   * Browser Command Execution
   */
  async executeBrowserCommand(command, params = {}) {
    if (this.isElectron) {
      // Direct browser automation in local-first mode
      return await window.kairoAPI.browser.execute(command, params);
    } else {
      // Backend automation in server-first mode
      const response = await fetch(`${this.backendUrl}/api/browser/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command, params })
      });
      return await response.json();
    }
  }

  /**
   * Workflow Execution
   */
  async executeWorkflow(workflow) {
    if (this.isElectron) {
      // Local workflow execution
      return await window.kairoAPI.workflow.execute(workflow);
    } else {
      // Backend workflow execution
      const response = await fetch(`${this.backendUrl}/api/workflow/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(workflow)
      });
      return await response.json();
    }
  }

  /**
   * Enhanced Proxy (Website Loading)
   */
  async loadWebsite(url) {
    if (this.isElectron) {
      // Direct website access in local-first mode (no proxy needed)
      return await window.kairoAPI.browser.navigate(url);
    } else {
      // Enhanced proxy system for server-first mode
      try {
        const response = await fetch(`${this.backendUrl}/api/proxy/enhanced`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url })
        });
        return await response.json();
      } catch (error) {
        // Fallback to basic proxy
        const fallbackResponse = await fetch(`${this.backendUrl}/api/proxy`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url })
        });
        return await fallbackResponse.json();
      }
    }
  }

  /**
   * Get Page Content
   */
  async getPageContent() {
    if (this.isElectron) {
      return await window.kairoAPI.browser.getContent();
    } else {
      // Not available in server-first mode
      return { success: false, error: 'Not available in server-first mode' };
    }
  }

  /**
   * Take Screenshot
   */
  async takeScreenshot(options = {}) {
    if (this.isElectron) {
      return await window.kairoAPI.browser.screenshot(options);
    } else {
      // Not available in server-first mode
      return { success: false, error: 'Not available in server-first mode' };
    }
  }

  /**
   * System Information
   */
  async getSystemInfo() {
    if (this.isElectron) {
      return await window.kairoAPI.system.getInfo();
    } else {
      return {
        success: true,
        system: {
          platform: 'web',
          arch: 'unknown',
          environment: 'server-first',
          isElectron: false
        }
      };
    }
  }

  /**
   * Window Controls (Electron only)
   */
  async minimizeWindow() {
    if (this.isElectron) {
      return await window.kairoAPI.window.minimize();
    }
  }

  async maximizeWindow() {
    if (this.isElectron) {
      return await window.kairoAPI.window.maximize();
    }
  }

  async closeWindow() {
    if (this.isElectron) {
      return await window.kairoAPI.window.close();
    }
  }

  /**
   * Architecture Detection
   */
  isLocalFirst() {
    return this.isElectron;
  }

  getArchitectureType() {
    return this.isElectron ? 'local-first' : 'server-first';
  }

  /**
   * Feature Availability
   */
  getAvailableFeatures() {
    if (this.isElectron) {
      return {
        directBrowserAccess: true,
        nativeWindowControls: true,
        localFileSystem: true,
        offlineMode: true,
        enhancedSecurity: true,
        noProxyRestrictions: true,
        localDataStorage: true,
        systemIntegration: true
      };
    } else {
      return {
        directBrowserAccess: false,
        nativeWindowControls: false,
        localFileSystem: false,
        offlineMode: false,
        enhancedSecurity: false,
        noProxyRestrictions: false,
        localDataStorage: false,
        systemIntegration: false
      };
    }
  }
}

// Export singleton instance
export default new LocalFirstBridge();