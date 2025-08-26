#!/usr/bin/env node

/**
 * Migration Test Script - Local-First Architecture
 * Tests Phase 1 completion and Phase 2 readiness
 */

const fs = require('fs');
const path = require('path');

class MigrationTester {
  constructor() {
    this.results = {
      phase1: {},
      phase2: {},
      overall: {}
    };
  }

  async runAllTests() {
    console.log('🧪 Starting Local-First Architecture Migration Tests\n');
    
    // Phase 1 Tests
    console.log('📋 PHASE 1 TESTS: Electron Foundation');
    await this.testPhase1();
    
    // Phase 2 Tests  
    console.log('\n📋 PHASE 2 TESTS: Local Browser Engine');
    await this.testPhase2();
    
    // Summary
    this.printSummary();
  }

  async testPhase1() {
    const tests = [
      () => this.testElectronSetup(),
      () => this.testLocalDatabase(),
      () => this.testIpcHandlers(),
      () => this.testEnvironmentConfig(),
      () => this.testDependencies()
    ];

    for (const test of tests) {
      await test();
    }
  }

  async testPhase2() {
    const tests = [
      () => this.testPlaywrightInstallation(),
      () => this.testBrowserAutomation(),
      () => this.testAIIntegration(),
      () => this.testWorkflowEngine(),
      () => this.testLocalFirstDetection()
    ];

    for (const test of tests) {
      await test();
    }
  }

  testElectronSetup() {
    console.log('  🔧 Testing Electron Setup...');
    
    const mainExists = fs.existsSync('/app/local-first/electron/main.js');
    const preloadExists = fs.existsSync('/app/local-first/electron/preload.js');
    const packageExists = fs.existsSync('/app/local-first/package.json');
    
    this.results.phase1.electronSetup = mainExists && preloadExists && packageExists;
    console.log(`    ${mainExists ? '✅' : '❌'} main.js exists`);
    console.log(`    ${preloadExists ? '✅' : '❌'} preload.js exists`);
    console.log(`    ${packageExists ? '✅' : '❌'} package.json exists`);
  }

  testLocalDatabase() {
    console.log('  💾 Testing Local Database Schema...');
    
    try {
      const mainContent = fs.readFileSync('/app/local-first/electron/main.js', 'utf8');
      const hasSessionsTable = mainContent.includes('CREATE TABLE IF NOT EXISTS sessions');
      const hasAITable = mainContent.includes('ai_interactions');
      const hasHistoryTable = mainContent.includes('browser_history');
      
      this.results.phase1.localDatabase = hasSessionsTable && hasAITable && hasHistoryTable;
      console.log(`    ${hasSessionsTable ? '✅' : '❌'} Sessions table schema`);
      console.log(`    ${hasAITable ? '✅' : '❌'} AI interactions table schema`);
      console.log(`    ${hasHistoryTable ? '✅' : '❌'} Browser history table schema`);
    } catch (error) {
      this.results.phase1.localDatabase = false;
      console.log('    ❌ Error reading database schema');
    }
  }

  testIpcHandlers() {
    console.log('  🔗 Testing IPC Handlers...');
    
    try {
      const preloadContent = fs.readFileSync('/app/local-first/electron/preload.js', 'utf8');
      const hasNavigate = preloadContent.includes('navigate');
      const hasAIQuery = preloadContent.includes('ai-query');
      const hasBrowserExecute = preloadContent.includes('browser-execute');
      const hasSystemInfo = preloadContent.includes('system-info');
      
      this.results.phase1.ipcHandlers = hasNavigate && hasAIQuery && hasBrowserExecute && hasSystemInfo;
      console.log(`    ${hasNavigate ? '✅' : '❌'} Navigation handler`);
      console.log(`    ${hasAIQuery ? '✅' : '❌'} AI query handler`);
      console.log(`    ${hasBrowserExecute ? '✅' : '❌'} Browser execute handler`);
      console.log(`    ${hasSystemInfo ? '✅' : '❌'} System info handler`);
    } catch (error) {
      this.results.phase1.ipcHandlers = false;
      console.log('    ❌ Error reading IPC handlers');
    }
  }

  testEnvironmentConfig() {
    console.log('  ⚙️ Testing Environment Configuration...');
    
    const envExists = fs.existsSync('/app/local-first/.env');
    let hasGroqKey = false;
    let hasLocalFirst = false;
    
    if (envExists) {
      try {
        const envContent = fs.readFileSync('/app/local-first/.env', 'utf8');
        hasGroqKey = envContent.includes('GROQ_API_KEY');
        hasLocalFirst = envContent.includes('NODE_ENV');
      } catch (error) {
        // Ignore read errors
      }
    }
    
    this.results.phase1.environmentConfig = envExists && hasGroqKey && hasLocalFirst;
    console.log(`    ${envExists ? '✅' : '❌'} .env file exists`);
    console.log(`    ${hasGroqKey ? '✅' : '❌'} Groq API key configured`);
    console.log(`    ${hasLocalFirst ? '✅' : '❌'} Local-first environment set`);
  }

  testDependencies() {
    console.log('  📦 Testing Dependencies...');
    
    const nodeModulesExists = fs.existsSync('/app/local-first/node_modules');
    const electronExists = fs.existsSync('/app/local-first/node_modules/electron');
    const playwrightExists = fs.existsSync('/app/local-first/node_modules/playwright');
    
    this.results.phase1.dependencies = nodeModulesExists && electronExists && playwrightExists;
    console.log(`    ${nodeModulesExists ? '✅' : '❌'} node_modules installed`);
    console.log(`    ${electronExists ? '✅' : '❌'} Electron installed`);
    console.log(`    ${playwrightExists ? '✅' : '❌'} Playwright installed`);
  }

  testPlaywrightInstallation() {
    console.log('  🌐 Testing Playwright Installation...');
    
    const playwrightBrowser = fs.existsSync('/pw-browsers') || fs.existsSync('/app/local-first/node_modules/playwright');
    
    this.results.phase2.playwrightInstallation = playwrightBrowser;
    console.log(`    ${playwrightBrowser ? '✅' : '❌'} Playwright browsers installed`);
  }

  testBrowserAutomation() {
    console.log('  🤖 Testing Browser Automation Classes...');
    
    const automationExists = fs.existsSync('/app/local-first/electron/browser-automation.js');
    let hasCommands = false;
    
    if (automationExists) {
      try {
        const content = fs.readFileSync('/app/local-first/electron/browser-automation.js', 'utf8');
        hasCommands = content.includes('executeCommand') && content.includes('navigate') && content.includes('youtube_video');
      } catch (error) {
        // Ignore read errors
      }
    }
    
    this.results.phase2.browserAutomation = automationExists && hasCommands;
    console.log(`    ${automationExists ? '✅' : '❌'} BrowserAutomation class exists`);
    console.log(`    ${hasCommands ? '✅' : '❌'} Command handlers implemented`);
  }

  testAIIntegration() {
    console.log('  🧠 Testing AI Integration...');
    
    const aiExists = fs.existsSync('/app/local-first/orchestrator/ai-integration.js');
    let hasProcessQuery = false;
    
    if (aiExists) {
      try {
        const content = fs.readFileSync('/app/local-first/orchestrator/ai-integration.js', 'utf8');
        hasProcessQuery = content.includes('processQuery') && content.includes('local-first');
      } catch (error) {
        // Ignore read errors
      }
    }
    
    this.results.phase2.aiIntegration = aiExists && hasProcessQuery;
    console.log(`    ${aiExists ? '✅' : '❌'} AIIntegration class exists`);
    console.log(`    ${hasProcessQuery ? '✅' : '❌'} Local-first AI processing`);
  }

  testWorkflowEngine() {
    console.log('  ⚡ Testing Workflow Engine...');
    
    const workflowExists = fs.existsSync('/app/local-first/orchestrator/workflow-engine.js');
    let hasExecute = false;
    
    if (workflowExists) {
      try {
        const content = fs.readFileSync('/app/local-first/orchestrator/workflow-engine.js', 'utf8');
        hasExecute = content.includes('execute') && content.includes('executeStep');
      } catch (error) {
        // Ignore read errors
      }
    }
    
    this.results.phase2.workflowEngine = workflowExists && hasExecute;
    console.log(`    ${workflowExists ? '✅' : '❌'} WorkflowEngine class exists`);
    console.log(`    ${hasExecute ? '✅' : '❌'} Workflow execution implemented`);
  }

  testLocalFirstDetection() {
    console.log('  🔍 Testing Local-First Detection...');
    
    const detectorExists = fs.existsSync('/app/frontend/src/components/LocalFirstDetector.js');
    let hasElectronCheck = false;
    
    if (detectorExists) {
      try {
        const content = fs.readFileSync('/app/frontend/src/components/LocalFirstDetector.js', 'utf8');
        hasElectronCheck = content.includes('window.electronAPI') && content.includes('isLocalFirst');
      } catch (error) {
        // Ignore read errors
      }
    }
    
    this.results.phase2.localFirstDetection = detectorExists && hasElectronCheck;
    console.log(`    ${detectorExists ? '✅' : '❌'} LocalFirstDetector component exists`);
    console.log(`    ${hasElectronCheck ? '✅' : '❌'} Electron API detection implemented`);
  }

  printSummary() {
    console.log('\n' + '='.repeat(60));
    console.log('📊 MIGRATION TEST SUMMARY');
    console.log('='.repeat(60));
    
    // Phase 1 Summary
    const phase1Tests = Object.values(this.results.phase1);
    const phase1Passed = phase1Tests.filter(Boolean).length;
    const phase1Total = phase1Tests.length;
    const phase1Success = phase1Passed === phase1Total;
    
    console.log(`\n📋 PHASE 1: Electron Foundation`);
    console.log(`   Status: ${phase1Success ? '✅ COMPLETED' : '⚠️ PARTIAL'} (${phase1Passed}/${phase1Total} tests passed)`);
    
    // Phase 2 Summary
    const phase2Tests = Object.values(this.results.phase2);
    const phase2Passed = phase2Tests.filter(Boolean).length;
    const phase2Total = phase2Tests.length;
    const phase2Success = phase2Passed === phase2Total;
    
    console.log(`\n📋 PHASE 2: Local Browser Engine`);
    console.log(`   Status: ${phase2Success ? '✅ COMPLETED' : '⚠️ IN PROGRESS'} (${phase2Passed}/${phase2Total} tests passed)`);
    
    // Overall Status
    const totalPassed = phase1Passed + phase2Passed;
    const totalTests = phase1Total + phase2Total;
    const overallSuccess = phase1Success && phase2Success;
    
    console.log(`\n🎯 OVERALL MIGRATION STATUS:`);
    console.log(`   Progress: ${Math.round((totalPassed / totalTests) * 100)}% (${totalPassed}/${totalTests} tests passed)`);
    console.log(`   Phase 1: ${phase1Success ? '✅ READY' : '❌ NEEDS WORK'}`);
    console.log(`   Phase 2: ${phase2Success ? '✅ READY' : '🔄 IN PROGRESS'}`);
    
    if (overallSuccess) {
      console.log('\n🎉 LOCAL-FIRST MIGRATION READY FOR TESTING!');
      console.log('   Next steps:');
      console.log('   1. Test Electron app: cd /app/local-first && npm run dev');
      console.log('   2. Verify LocalFirstDetector shows "Local-First" status');
      console.log('   3. Test AI integration and browser automation');
    } else {
      console.log('\n🔧 MIGRATION NEEDS COMPLETION:');
      if (!phase1Success) {
        console.log('   - Complete Phase 1 foundation setup');
      }
      if (!phase2Success) {
        console.log('   - Complete Phase 2 browser engine integration');
      }
    }
    
    console.log('\n' + '='.repeat(60));
  }
}

// Run tests
const tester = new MigrationTester();
tester.runAllTests().catch(console.error);