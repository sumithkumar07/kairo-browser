#!/usr/bin/env node

/**
 * Core Functionality Test - Local-First Architecture
 * Tests the main components without Electron GUI
 */

const BrowserAutomation = require('./electron/browser-automation');
const AIIntegration = require('./orchestrator/ai-integration');
const WorkflowEngine = require('./orchestrator/workflow-engine');
const SyncClient = require('./sync/sync-client');
const { chromium } = require('playwright');

class CoreFunctionalityTest {
  constructor() {
    this.browserAutomation = new BrowserAutomation();
    this.aiIntegration = new AIIntegration();
    this.workflowEngine = new WorkflowEngine();
    this.syncClient = new SyncClient();
    this.browser = null;
    this.page = null;
  }

  async runAllTests() {
    console.log('🚀 Starting Core Functionality Tests for Local-First Architecture\n');
    
    const results = {
      chromiumInit: false,
      browserAutomation: false,
      aiIntegration: false,
      workflowEngine: false,
      youtubeAccess: false,
      syncClient: false
    };

    try {
      // Test 1: Chromium Initialization
      console.log('1️⃣ Testing Chromium Browser Initialization...');
      results.chromiumInit = await this.testChromiumInit();
      
      // Test 2: Browser Automation
      console.log('2️⃣ Testing Browser Automation Commands...');
      results.browserAutomation = await this.testBrowserAutomation();
      
      // Test 3: AI Integration
      console.log('3️⃣ Testing AI Integration...');
      results.aiIntegration = await this.testAIIntegration();
      
      // Test 4: Workflow Engine
      console.log('4️⃣ Testing Workflow Engine...');
      results.workflowEngine = await this.testWorkflowEngine();
      
      // Test 5: YouTube Access (The Big Test!)
      console.log('5️⃣ Testing YouTube Access (No Proxy Restrictions)...');
      results.youtubeAccess = await this.testYouTubeAccess();
      
      // Test 6: Sync Client
      console.log('6️⃣ Testing Local Sync Client...');
      results.syncClient = await this.testSyncClient();
      
      // Cleanup
      await this.cleanup();
      
      // Final Results
      this.printResults(results);
      
    } catch (error) {
      console.error('❌ Test suite failed:', error);
      await this.cleanup();
    }
  }

  async testChromiumInit() {
    try {
      console.log('   📦 Launching Chromium browser...');
      
      this.browser = await chromium.launch({
        headless: true, // Headless for testing
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage'
        ]
      });

      this.page = await this.browser.newPage();
      
      console.log('   ✅ Chromium browser initialized successfully');
      return true;
      
    } catch (error) {
      console.error('   ❌ Chromium initialization failed:', error.message);
      return false;
    }
  }

  async testBrowserAutomation() {
    try {
      if (!this.page) {
        throw new Error('No browser page available');
      }

      // Test basic navigation
      console.log('   🌐 Testing navigation to Google...');
      const navResult = await this.browserAutomation.executeCommand(this.page, 'navigate', {
        url: 'https://www.google.com'
      });

      if (!navResult.success) {
        throw new Error('Navigation failed');
      }

      // Test element interaction
      console.log('   🔍 Testing search functionality...');
      const searchResult = await this.browserAutomation.executeCommand(this.page, 'search', {
        query: 'local first browser'
      });

      console.log('   ✅ Browser automation working');
      return true;

    } catch (error) {
      console.error('   ❌ Browser automation failed:', error.message);
      return false;
    }
  }

  async testAIIntegration() {
    try {
      console.log('   🤖 Testing AI query processing...');
      
      const aiResult = await this.aiIntegration.processQuery(
        'Navigate to YouTube and search for AI tutorials',
        {
          currentUrl: this.page ? this.page.url() : 'about:blank',
          browserEngine: 'chromium_embedded'
        }
      );

      if (aiResult.intent && aiResult.commands) {
        console.log(`   📝 AI Intent: ${aiResult.intent}`);
        console.log(`   ⚡ Commands Generated: ${aiResult.commands.length}`);
        console.log('   ✅ AI integration working');
        return true;
      }

      throw new Error('AI response format invalid');

    } catch (error) {
      console.error('   ❌ AI integration failed:', error.message);
      return false;
    }
  }

  async testWorkflowEngine() {
    try {
      console.log('   🔄 Testing workflow execution...');
      
      const testWorkflow = {
        id: 'test-workflow-001',
        name: 'Test Google Search',
        steps: [
          {
            type: 'navigate',
            params: { url: 'https://www.google.com' }
          },
          {
            type: 'search',
            params: { query: 'local first architecture' }
          }
        ]
      };

      const workflowResult = await this.workflowEngine.execute(testWorkflow, {
        page: this.page,
        browserAutomation: this.browserAutomation,
        aiIntegration: this.aiIntegration
      });

      if (workflowResult.status === 'completed') {
        console.log(`   📊 Workflow Steps: ${workflowResult.results.length}`);
        console.log('   ✅ Workflow engine working');
        return true;
      }

      throw new Error(`Workflow failed with status: ${workflowResult.status}`);

    } catch (error) {
      console.error('   ❌ Workflow engine failed:', error.message);
      return false;
    }
  }

  async testYouTubeAccess() {
    try {
      console.log('   🎥 Testing direct YouTube access...');
      
      if (!this.page) {
        throw new Error('No browser page available');
      }

      // Navigate directly to YouTube
      const response = await this.page.goto('https://www.youtube.com', {
        waitUntil: 'networkidle',
        timeout: 15000
      });

      if (response && response.status() === 200) {
        const title = await this.page.title();
        console.log(`   📺 YouTube Page Title: ${title}`);
        
        // Check if we can see the search box (indicates full access)
        const searchBox = await this.page.$('input[name="search_query"]');
        if (searchBox) {
          console.log('   🔍 YouTube search functionality accessible');
          
          // Test search
          await searchBox.fill('AI browser automation');
          await searchBox.press('Enter');
          
          // Wait for results
          await this.page.waitForSelector('#contents', { timeout: 10000 });
          
          console.log('   ✅ YouTube fully accessible - NO PROXY RESTRICTIONS!');
          return true;
        }
      }

      throw new Error('YouTube access limited or failed');

    } catch (error) {
      console.error('   ❌ YouTube access test failed:', error.message);
      return false;
    }
  }

  async testSyncClient() {
    try {
      console.log('   💾 Testing local sync client...');
      
      // Test local storage
      const testData = { 
        setting: 'test_value', 
        timestamp: new Date().toISOString() 
      };
      
      await this.syncClient.saveLocal('preferences', 'test_setting', testData);
      const retrievedData = await this.syncClient.loadLocal('preferences', 'test_setting');
      
      if (retrievedData && retrievedData.setting === 'test_value') {
        console.log('   📁 Local storage working');
        
        // Test list functionality
        const items = await this.syncClient.listLocal('preferences');
        console.log(`   📋 Local items count: ${items.length}`);
        
        // Cleanup test data
        await this.syncClient.deleteLocal('preferences', 'test_setting');
        
        console.log('   ✅ Sync client working');
        return true;
      }

      throw new Error('Sync client storage failed');

    } catch (error) {
      console.error('   ❌ Sync client failed:', error.message);
      return false;
    }
  }

  async cleanup() {
    console.log('\n🧹 Cleaning up test resources...');
    
    try {
      if (this.page) {
        await this.page.close();
      }
      if (this.browser) {
        await this.browser.close();
      }
      console.log('✅ Cleanup completed');
    } catch (error) {
      console.error('❌ Cleanup error:', error);
    }
  }

  printResults(results) {
    console.log('\n' + '='.repeat(60));
    console.log('🎯 LOCAL-FIRST ARCHITECTURE - TEST RESULTS');
    console.log('='.repeat(60));
    
    const tests = [
      ['Chromium Browser Init', results.chromiumInit],
      ['Browser Automation', results.browserAutomation],
      ['AI Integration', results.aiIntegration],
      ['Workflow Engine', results.workflowEngine],
      ['YouTube Access (KEY TEST)', results.youtubeAccess],
      ['Sync Client', results.syncClient]
    ];

    let passedTests = 0;
    
    tests.forEach(([name, passed]) => {
      const status = passed ? '✅ PASS' : '❌ FAIL';
      const emphasis = name.includes('KEY TEST') ? '*** ' : '    ';
      console.log(`${emphasis}${status} - ${name}`);
      if (passed) passedTests++;
    });

    console.log('\n' + '-'.repeat(60));
    console.log(`📊 OVERALL RESULTS: ${passedTests}/${tests.length} tests passed`);
    
    if (passedTests === tests.length) {
      console.log('🎉 ALL TESTS PASSED - Local-First Architecture is WORKING!');
      console.log('');
      console.log('🚀 KEY ACHIEVEMENTS:');
      console.log('   ✅ Native Chromium browser working');
      console.log('   ✅ Direct website access (no proxy needed)');
      console.log('   ✅ YouTube accessible without restrictions');
      console.log('   ✅ AI + browser automation integrated');
      console.log('   ✅ Local-first data storage working');
      console.log('');
      console.log('🎯 READY FOR: Phase 2 UI Integration');
    } else {
      console.log('⚠️  SOME TESTS FAILED - Review logs above');
      console.log('');
      console.log('📋 NEXT STEPS:');
      console.log('   1. Fix failing components');
      console.log('   2. Re-run tests');
      console.log('   3. Proceed to UI integration when all pass');
    }
    
    console.log('='.repeat(60));
  }
}

// Run tests if called directly
if (require.main === module) {
  const tester = new CoreFunctionalityTest();
  tester.runAllTests().catch(console.error);
}

module.exports = CoreFunctionalityTest;