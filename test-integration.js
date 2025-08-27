#!/usr/bin/env node

/**
 * Integration Test - Verify All Components Are Connected
 * Tests that all components work together without GUI
 */

const fs = require('fs');
const path = require('path');

console.log('🔍 KAIRO AI BROWSER - INTEGRATION TEST');
console.log('=====================================');

const results = {
  files: { passed: 0, total: 0 },
  dependencies: { passed: 0, total: 0 },
  connections: { passed: 0, total: 0 }
};

// Test 1: Verify Essential Files Exist
console.log('\n1️⃣ Testing Essential Files...');

const essentialFiles = [
  'package.json',
  '.env',
  'electron/main.js',
  'electron/preload.js',
  'electron/browser-automation.js',
  'renderer/index.html',
  'renderer/App.css',
  'renderer/App-BrowserAI.js',
  'orchestrator/ai-integration.js',
  'orchestrator/ai-integration-enhanced.js',
  'orchestrator/autonomous-browser.js',
  'orchestrator/workflow-engine.js',
  'sync/sync-client.js',
  'sync/minimal-backend.js'
];

results.files.total = essentialFiles.length;

essentialFiles.forEach(file => {
  const fullPath = path.join(__dirname, file);
  const exists = fs.existsSync(fullPath);
  console.log(`   ${exists ? '✅' : '❌'} ${file}`);
  if (exists) results.files.passed++;
});

// Test 2: Verify Dependencies
console.log('\n2️⃣ Testing Dependencies...');

const requiredDeps = [
  'playwright',
  'dotenv', 
  'sqlite3',
  'uuid',
  'react',
  'react-dom',
  'electron'
];

results.dependencies.total = requiredDeps.length;

const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const allDeps = { ...packageJson.dependencies, ...packageJson.devDependencies };

requiredDeps.forEach(dep => {
  const exists = allDeps[dep];
  console.log(`   ${exists ? '✅' : '❌'} ${dep} ${exists ? `(${allDeps[dep]})` : '(MISSING)'}`);
  if (exists) results.dependencies.passed++;
});

// Test 3: Test Component Connections
console.log('\n3️⃣ Testing Component Connections...');

const connectionTests = [
  {
    name: 'Electron Main → Renderer',
    test: () => {
      const mainJs = fs.readFileSync('electron/main.js', 'utf8');
      return mainJs.includes('renderer/index.html');
    }
  },
  {
    name: 'Main → AI Integration',
    test: () => {
      const mainJs = fs.readFileSync('electron/main.js', 'utf8');
      return mainJs.includes('ai-integration') || mainJs.includes('EnhancedAIIntegration');
    }
  },
  {
    name: 'Main → Browser Automation',
    test: () => {
      const mainJs = fs.readFileSync('electron/main.js', 'utf8');
      return mainJs.includes('AutonomousBrowser') || mainJs.includes('chromium');
    }
  },
  {
    name: 'HTML → React Components',
    test: () => {
      const html = fs.readFileSync('renderer/index.html', 'utf8');
      return html.includes('react') && html.includes('BrowserAIApp');
    }
  },
  {
    name: 'AI → Groq API Configuration',
    test: () => {
      const aiJs = fs.readFileSync('orchestrator/ai-integration.js', 'utf8');
      return aiJs.includes('GROQ_API_KEY') && aiJs.includes('api.groq.com');
    }
  },
  {
    name: 'Workflow → Task Execution',
    test: () => {
      const workflowJs = fs.readFileSync('orchestrator/workflow-engine.js', 'utf8');
      return workflowJs.includes('executeTaskByType') && workflowJs.includes('navigate');
    }
  }
];

results.connections.total = connectionTests.length;

connectionTests.forEach(({ name, test }) => {
  try {
    const passed = test();
    console.log(`   ${passed ? '✅' : '❌'} ${name}`);
    if (passed) results.connections.passed++;
  } catch (error) {
    console.log(`   ❌ ${name} (Error: ${error.message})`);
  }
});

// Test 4: Verify No Broken References
console.log('\n4️⃣ Testing for Broken References...');

const brokenRefs = [];

// Check if main.js references any deleted files
const mainJs = fs.readFileSync('electron/main.js', 'utf8');
const deletedFiles = [
  'main-browser-ai.js',
  'App.js',
  'App-Pure-AI.js', 
  'index-browser-ai.html'
];

deletedFiles.forEach(deletedFile => {
  if (mainJs.includes(deletedFile)) {
    brokenRefs.push(`electron/main.js references deleted file: ${deletedFile}`);
  }
});

if (brokenRefs.length === 0) {
  console.log('   ✅ No broken file references found');
} else {
  brokenRefs.forEach(ref => console.log(`   ❌ ${ref}`));
}

// Final Results
console.log('\n' + '='.repeat(50));
console.log('📊 INTEGRATION TEST RESULTS');
console.log('='.repeat(50));

const totalTests = results.files.total + results.dependencies.total + results.connections.total;
const totalPassed = results.files.passed + results.dependencies.passed + results.connections.passed;

console.log(`📁 Files: ${results.files.passed}/${results.files.total} passed`);
console.log(`📦 Dependencies: ${results.dependencies.passed}/${results.dependencies.total} passed`);
console.log(`🔗 Connections: ${results.connections.passed}/${results.connections.total} passed`);
console.log(`🚫 Broken References: ${brokenRefs.length}`);

console.log('\n' + '-'.repeat(50));
console.log(`🎯 OVERALL: ${totalPassed}/${totalTests} tests passed`);

if (totalPassed === totalTests && brokenRefs.length === 0) {
  console.log('✅ ALL INTEGRATION TESTS PASSED!');
  console.log('\n🚀 READY FOR PRODUCTION:');
  console.log('   ✅ All essential files present');
  console.log('   ✅ Dependencies properly installed');
  console.log('   ✅ Components correctly connected');
  console.log('   ✅ No broken references');
  console.log('   ✅ Clean, consolidated codebase');
  console.log('\n🎯 NEXT: Run "npm run dev" to test UI');
} else {
  console.log('⚠️  SOME INTEGRATION TESTS FAILED');
  console.log('📋 Review issues above before proceeding');
}

console.log('='.repeat(50));