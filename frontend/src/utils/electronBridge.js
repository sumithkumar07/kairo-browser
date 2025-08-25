/**
 * Electron Bridge - Handles communication between React and Electron
 */

class ElectronBridge {
    constructor() {
        this.isElectron = window.kairoAPI?.system?.isElectron || false;
        this.api = window.kairoAPI || null;
    }

    // Check if running in Electron
    isElectronApp() {
        return this.isElectron;
    }

    // Browser navigation
    async navigateToUrl(url) {
        if (!this.isElectronApp()) {
            // Fallback for web version - use existing proxy system
            return this.webNavigate(url);
        }

        try {
            const result = await this.api.browser.navigate(url);
            return result;
        } catch (error) {
            console.error('❌ Electron navigation error:', error);
            return { success: false, error: error.message };
        }
    }

    // AI query processing
    async processAIQuery(query) {
        if (!this.isElectronApp()) {
            // Fallback for web version - use existing backend
            return this.webAIQuery(query);
        }

        try {
            const result = await this.api.ai.query(query);
            return result;
        } catch (error) {
            console.error('❌ Electron AI query error:', error);
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

    // Fallback methods for web version
    async webNavigate(url) {
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
            
            // First try AI query to process the URL request
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
                
                // Execute the browser command
                if (aiResult.commands && aiResult.commands.length > 0) {
                    const command = aiResult.commands[0];
                    
                    const execResponse = await fetch(`${backendUrl}/api/browser/execute`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(command)
                    });

                    if (execResponse.ok) {
                        const execResult = await execResponse.json();
                        
                        // Try to load content via proxy
                        const proxyResponse = await fetch(`${backendUrl}/api/proxy/enhanced`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ url: url })
                        });

                        if (proxyResponse.ok) {
                            const proxyResult = await proxyResponse.json();
                            return {
                                success: true,
                                url: url,
                                content: proxyResult.content,
                                method: 'web_proxy'
                            };
                        }
                    }
                }
            }

            return {
                success: false,
                error: 'Navigation failed',
                fallback: true
            };

        } catch (error) {
            console.error('❌ Web navigation error:', error);
            return { success: false, error: error.message };
        }
    }

    async webAIQuery(query) {
        try {
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
                    response: result.response,
                    commands: result.commands || []
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