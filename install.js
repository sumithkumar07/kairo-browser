#!/usr/bin/env node

/**
 * Kairo AI Browser - Local-First Installation Script
 * Sets up the application for first-time use
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

console.log('🚀 Setting up Kairo AI Browser - Local-First Edition...\n');

// 1. Check Node.js version
const nodeVersion = process.version;
const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);

if (majorVersion < 18) {
  console.error('❌ Node.js 18 or higher is required. Current version:', nodeVersion);
  process.exit(1);
}

console.log('✅ Node.js version check passed:', nodeVersion);

// 2. Install dependencies
console.log('📦 Installing dependencies...');
try {
  execSync('npm install', { stdio: 'inherit' });
  console.log('✅ Dependencies installed successfully');
} catch (error) {
  console.error('❌ Failed to install dependencies:', error.message);
  process.exit(1);
}

// 3. Setup environment file
const envPath = path.join(__dirname, '.env');
const envExamplePath = path.join(__dirname, '.env.example');

if (!fs.existsSync(envPath) && fs.existsSync(envExamplePath)) {
  console.log('📝 Creating environment configuration...');
  fs.copyFileSync(envExamplePath, envPath);
  console.log('✅ Environment file created (.env)');
  console.log('ℹ️  Please edit .env file to add your API keys if needed');
}

// 4. Install Playwright browsers
console.log('🌐 Installing Playwright browsers...');
try {
  execSync('npx playwright install chromium', { stdio: 'inherit' });
  console.log('✅ Chromium browser installed');
} catch (error) {
  console.error('⚠️  Playwright browser installation failed:', error.message);
  console.log('ℹ️  The app will try to use system browser as fallback');
}

// 5. Create user data directory
const os = require('os');
const userDataDir = path.join(os.homedir(), '.kairo-browser');
if (!fs.existsSync(userDataDir)) {
  fs.mkdirSync(userDataDir, { recursive: true });
  console.log('✅ User data directory created:', userDataDir);
}

// 6. Setup complete
console.log('\n🎉 Setup completed successfully!');
console.log('\n📋 Next steps:');
console.log('   1. Edit .env file to add your Groq API key (optional)');
console.log('   2. Run "npm run dev" to start in development mode');
console.log('   3. Run "npm run build" to create production build');
console.log('   4. Run "npm run dist" to create installers');

console.log('\n🔍 What you get:');
console.log('   ✅ Native browser with full website access');
console.log('   ✅ YouTube videos play without restrictions');
console.log('   ✅ Banking sites work fully');
console.log('   ✅ AI-powered automation');
console.log('   ✅ 100% privacy (all data local)');
console.log('   ✅ Offline functionality');

console.log('\n🚀 Ready to launch your local-first AI browser!');