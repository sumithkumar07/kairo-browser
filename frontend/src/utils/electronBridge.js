/**
 * Electron Bridge - Local-First Communication Layer
 * Handles communication between React UI and Electron main process
 */

class ElectronBridge {
    constructor() {
        this.isElectron = window.kairoAPI?.system?.isElectron || false;
        this.api = window.kairoAPI || null;
        
        if (this.isElectron) {
            console.log('🚀 Local-First Mode: Electron bridge initialized');
            this.setupEventListeners();
        } else {
            console.log('🌐 Web Mode: Using fallback to existing backend');
        }
    }

    // Check if running in Electron (local-first mode)
    isElectronApp() {
        return this.isElectron;
    }

    // Setup event listeners for Electron events
    setupEventListeners() {
        if (!this.api) return;

        // Listen for Chromium ready event
        this.api.on('chromium-ready', (event, data) => {
            console.log('🌐 Embedded Chromium ready:', data);
            window.dispatchEvent(new CustomEvent('chromiumReady', { detail: data }));
        });

        // Listen for workflow progress
        this.api.on('workflow-progress', (event, data) => {
            console.log('🔄 Workflow progress:', data);
            window.dispatchEvent(new CustomEvent('workflowProgress', { detail: data }));
        });
    }

    // Browser navigation - Local-First Implementation
    async navigateToUrl(url) {
        if (!this.isElectronApp()) {
            return this.webNavigate(url);
        }

        try {
            console.log(`🌐 Local-First Navigation: ${url}`);
            const result = await this.api.browser.navigate(url);
            
            if (result.success) {
                console.log(`✅ Navigation successful: ${result.title}`);
                
                // Get page content for UI display (if needed)
                const content = await this.api.browser.getContent();
                return {
                    ...result,
                    content: content.success ? content.content : null
                };
            }
            
            return result;
        } catch (error) {
            console.error('❌ Local-First navigation error:', error);
            return { success: false, error: error.message };
        }
    }

    // AI query processing - Local-First Implementation  
    async processAIQuery(query, context = {}) {
        if (!this.isElectronApp()) {
            return this.webAIQuery(query);
        }

        try {
            console.log(`🤖 Local-First AI Query: ${query}`);
            const result = await this.api.ai.query(query, context);
            
            if (result.success) {
                console.log(`✅ AI processing successful`);
                
                // Execute any commands returned by AI
                if (result.response?.commands && result.response.commands.length > 0) {
                    console.log(`⚡ Executing ${result.response.commands.length} AI commands`);
                    
                    for (const command of result.response.commands) {
                        try {
                            const cmdResult = await this.api.browser.execute(command.type, command.params);
                            console.log(`✅ Command ${command.type} executed:`, cmdResult);
                        } catch (cmdError) {
                            console.error(`❌ Command ${command.type} failed:`, cmdError);
                        }
                    }
                }
            }
            
            return result;
        } catch (error) {
            console.error('❌ Local-First AI query error:', error);
            return { success: false, error: error.message };
        }
    }

    // Browser automation commands
    async executeBrowserCommand(command, params = {}) {
        if (!this.isElectronApp()) {
            return { success: false, error: 'Local-First commands only available in desktop app' };
        }

        try {
            console.log(`⚡ Executing browser command: ${command}`);
            const result = await this.api.browser.execute(command, params);
            return result;
        } catch (error) {
            console.error(`❌ Browser command error:`, error);
            return { success: false, error: error.message };
        }
    }

    // Workflow execution
    async executeWorkflow(workflow) {
        if (!this.isElectronApp()) {
            return { success: false, error: 'Workflows only available in desktop app' };
        }

        try {
            console.log(`🔄 Executing workflow: ${workflow.name}`);
            const result = await this.api.workflow.execute(workflow);
            return result;
        } catch (error) {
            console.error(`❌ Workflow execution error:`, error);
            return { success: false, error: error.message };
        }
    }

    // System information
    async getSystemInfo() {
        if (!this.isElectronApp()) {
            return { success: false, error: 'System info only available in desktop app' };
        }

        try {
            const result = await this.api.system.getInfo();
            return result;
        } catch (error) {
            console.error(`❌ System info error:`, error);
            return { success: false, error: error.message };
        }
    }

    // Window management
    async minimizeWindow() {
        if (this.isElectronApp()) {
            await this.api.window.minimize();
        }
    }

    async maximizeWindow() {
        if (this.isElectronApp()) {
            await this.api.window.maximize();
        }
    }

    async closeWindow() {
        if (this.isElectronApp()) {
            await this.api.window.close();
        }
    }

    // Take screenshot
    async takeScreenshot(options = {}) {
        if (!this.isElectronApp()) {
            return { success: false, error: 'Screenshots only available in desktop app' };
        }

        try {
            const result = await this.api.browser.screenshot(options);
            return result;
        } catch (error) {
            console.error(`❌ Screenshot error:`, error);
            return { success: false, error: error.message };
        }
    }

    // File operations
    async saveFile(filepath, content) {
        if (!this.isElectronApp()) {
            return { success: false, error: 'File operations only available in desktop app' };
        }

        try {
            const result = await this.api.file.save(filepath, content);
            return result;
        } catch (error) {
            console.error(`❌ File save error:`, error);
            return { success: false, error: error.message };
        }
    }

    // Fallback methods for web version (legacy support)
    async webNavigate(url) {
        try {
            console.log('🌐 Web fallback navigation - Consider upgrading to desktop app for better experience');
            const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
            
            // Use streamlined backend for basic AI processing
            const aiResponse = await fetch(`${backendUrl}/api/ai/query`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: `Navigate to ${url}`,
                    session_id: `web_${Date.now()}`
                })
            });

            if (aiResponse.ok) {
                const aiResult = await aiResponse.json();
                
                return {
                    success: true,
                    url: url,
                    explanation: aiResult.explanation,
                    commands: aiResult.commands || [],
                    method: 'web_legacy',
                    recommendation: 'For full website access, please use the desktop app'
                };
            }

            return {
                success: false,
                error: 'Web version has limited capabilities. Please use desktop app.',
                fallback: true
            };

        } catch (error) {
            console.error('❌ Web navigation error:', error);
            return { 
                success: false, 
                error: error.message,
                recommendation: 'Desktop app provides full website access without restrictions'
            };
        }
    }

    async webAIQuery(query) {
        try {
            console.log('🤖 Web fallback AI query - Consider upgrading to desktop app for enhanced features');
            const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
            
            const response = await fetch(`${backendUrl}/api/ai/query`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    query: query,
                    session_id: `web_${Date.now()}`
                })
            });

            if (response.ok) {
                const result = await response.json();
                return {
                    success: true,
                    response: result,
                    commands: result.commands || [],
                    method: 'web_legacy',
                    limitation: 'Web version cannot execute browser commands. Desktop app provides full automation.'
                };
            }

            return { success: false, error: 'AI query failed' };

        } catch (error) {
            console.error('❌ Web AI query error:', error);
            return { success: false, error: error.message };
        }
    }
}

// Create singleton instance
const electronBridge = new ElectronBridge();

export default electronBridge;