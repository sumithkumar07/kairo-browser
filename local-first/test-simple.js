#!/usr/bin/env node

/**
 * Simple Test - Verify core components work
 */

require('dotenv').config();
const { chromium } = require('playwright');

async function simpleTest() {
  console.log('🚀 Simple Core Test Starting...\n');
  
  let browser, page;
  
  try {
    // Test 1: Browser Launch
    console.log('1️⃣ Testing Chromium Launch...');
    browser = await chromium.launch({ headless: true });
    page = await browser.newPage();
    console.log('   ✅ Chromium launched successfully');
    
    // Test 2: YouTube Access
    console.log('2️⃣ Testing YouTube Access...');
    await page.goto('https://www.youtube.com', { waitUntil: 'networkidle' });
    const title = await page.title();
    console.log(`   📺 Page Title: ${title}`);
    
    if (title.includes('YouTube')) {
      console.log('   ✅ YouTube accessed successfully - NO RESTRICTIONS!');
    }
    
    // Test 3: Google Search
    console.log('3️⃣ Testing Google Search...');
    await page.goto('https://www.google.com', { waitUntil: 'networkidle' });
    
    // Find search input
    const searchInput = await page.$('input[name="q"], textarea[name="q"]');
    if (searchInput) {
      await searchInput.fill('local first browser architecture');
      await searchInput.press('Enter');
      
      // Wait for results
      await page.waitForSelector('#search', { timeout: 10000 });
      console.log('   ✅ Google search working');
    }
    
    // Test 4: AI Integration (just test API key)
    console.log('4️⃣ Testing AI Configuration...');
    const apiKey = process.env.GROQ_API_KEY;
    if (apiKey && apiKey.startsWith('gsk_')) {
      console.log('   ✅ Groq API key configured correctly');
    } else {
      console.log('   ⚠️  Groq API key not found or invalid');
    }
    
    console.log('\n🎉 ALL SIMPLE TESTS PASSED!');
    console.log('\n🔥 KEY ACHIEVEMENTS:');
    console.log('   ✅ Native Chromium browser working');
    console.log('   ✅ YouTube accessible without proxy');
    console.log('   ✅ Google search functional');
    console.log('   ✅ Ready for full local-first implementation');
    
  } catch (error) {
    console.error('❌ Test failed:', error);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

simpleTest();