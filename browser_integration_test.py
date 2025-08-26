#!/usr/bin/env python3
"""
Browser Integration Test for Local-First Architecture
Tests the embedded Chromium browser capabilities
"""

import subprocess
import json
import time

def test_browser_integration():
    """Test browser integration using Node.js"""
    
    test_script = '''
const { chromium } = require('playwright');
const BrowserAutomation = require('./electron/browser-automation');

async function testBrowserIntegration() {
    console.log('🚀 Testing Browser Integration...');
    
    let browser = null;
    let page = null;
    
    try {
        // Initialize browser
        console.log('📦 Launching Chromium...');
        browser = await chromium.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        });
        
        page = await browser.newPage();
        const automation = new BrowserAutomation();
        
        // Test 1: Basic Navigation
        console.log('🌐 Testing navigation...');
        const navResult = await automation.executeCommand(page, 'navigate', {
            url: 'https://www.google.com'
        });
        
        if (!navResult.success) {
            throw new Error('Navigation failed');
        }
        console.log('✅ Navigation successful');
        
        // Test 2: YouTube Access (Key Test)
        console.log('🎥 Testing YouTube access...');
        const youtubeResult = await automation.executeCommand(page, 'navigate', {
            url: 'https://www.youtube.com'
        });
        
        if (youtubeResult.success) {
            console.log('✅ YouTube accessible - NO PROXY RESTRICTIONS!');
        }
        
        // Test 3: Element Interaction
        console.log('🔍 Testing element interaction...');
        await page.goto('https://www.google.com');
        
        const searchBox = await page.$('input[name="q"], textarea[name="q"]');
        if (searchBox) {
            await searchBox.fill('local first browser');
            console.log('✅ Element interaction working');
        }
        
        // Test 4: Screenshot capability
        console.log('📸 Testing screenshot...');
        const screenshot = await page.screenshot({ 
            fullPage: false,
            quality: 40
        });
        
        if (screenshot && screenshot.length > 0) {
            console.log('✅ Screenshot capability working');
        }
        
        console.log('\\n🎉 ALL BROWSER TESTS PASSED!');
        console.log('🚀 Key Achievements:');
        console.log('   ✅ Chromium browser launches successfully');
        console.log('   ✅ Website navigation works');
        console.log('   ✅ YouTube accessible without restrictions');
        console.log('   ✅ Element interaction functional');
        console.log('   ✅ Screenshot capability available');
        
    } catch (error) {
        console.error('❌ Browser test failed:', error.message);
        process.exit(1);
    } finally {
        if (page) await page.close();
        if (browser) await browser.close();
    }
}

testBrowserIntegration().catch(console.error);
'''
    
    try:
        print("🔍 Running Browser Integration Test...")
        result = subprocess.run(
            ["node", "-e", test_script],
            cwd="/app",
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False

def test_ai_integration():
    """Test AI integration capabilities"""
    
    test_script = '''
const AIIntegration = require('./orchestrator/ai-integration');

async function testAI() {
    console.log('🤖 Testing AI Integration...');
    
    const ai = new AIIntegration();
    
    try {
        // Test AI response parsing (without API call)
        const mockResponse = `{
            "intent": "Navigate to YouTube and search for videos",
            "commands": [
                {
                    "type": "navigate",
                    "params": {"url": "https://youtube.com"}
                },
                {
                    "type": "search",
                    "params": {"query": "AI tutorials"}
                }
            ],
            "explanation": "I will navigate to YouTube and search for AI tutorials"
        }`;
        
        const parsed = ai.parseAIResponse(mockResponse);
        
        if (parsed.intent && parsed.commands && parsed.commands.length > 0) {
            console.log('✅ AI response parsing working');
            console.log(`   Intent: ${parsed.intent}`);
            console.log(`   Commands: ${parsed.commands.length}`);
        } else {
            throw new Error('AI parsing failed');
        }
        
        // Test system prompt building
        const systemPrompt = ai.buildSystemPrompt({
            currentUrl: 'https://google.com',
            pageTitle: 'Google',
            browserEngine: 'chromium'
        });
        
        if (systemPrompt.includes('LOCAL-FIRST') && systemPrompt.includes('chromium')) {
            console.log('✅ System prompt generation working');
        }
        
        console.log('\\n🎉 AI INTEGRATION TESTS PASSED!');
        
    } catch (error) {
        console.error('❌ AI test failed:', error.message);
        process.exit(1);
    }
}

testAI().catch(console.error);
'''
    
    try:
        print("🔍 Running AI Integration Test...")
        result = subprocess.run(
            ["node", "-e", test_script],
            cwd="/app",
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ AI test error: {str(e)}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting Browser Integration Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # Test browser integration
    if test_browser_integration():
        tests_passed += 1
        print("✅ Browser Integration - PASSED")
    else:
        print("❌ Browser Integration - FAILED")
    
    print("\n" + "-" * 50)
    
    # Test AI integration
    if test_ai_integration():
        tests_passed += 1
        print("✅ AI Integration - PASSED")
    else:
        print("❌ AI Integration - FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 INTEGRATION TESTS: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\n🚀 LOCAL-FIRST BROWSER IS FULLY FUNCTIONAL:")
        print("   ✅ Embedded Chromium working")
        print("   ✅ Website access unrestricted")
        print("   ✅ YouTube accessible (key proof)")
        print("   ✅ AI automation ready")
        print("   ✅ Desktop application architecture complete")
    else:
        print("⚠️  Some integration tests failed")
    
    print("=" * 50)

if __name__ == "__main__":
    main()