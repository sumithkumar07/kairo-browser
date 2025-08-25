#!/usr/bin/env python3
"""
🚀 COMPREHENSIVE ULTIMATE KAIRO AI BROWSER BACKEND TESTING
Testing all 6 phases and integration points as requested in review
"""
import requests
import sys
import json
import time
import base64
from datetime import datetime
from typing import Dict, Any

class UltimateKairoAPITester:
    def __init__(self, base_url="https://native-browser-1.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session_id = f"test_session_{int(time.time())}"
        
    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            self.failed_tests.append(f"{name}: {details}")
            print(f"❌ {name} - FAILED: {details}")
    
    def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, timeout: int = 30) -> tuple:
        """Make HTTP request and return success status and response"""
        url = f"{self.base_url}/api{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=timeout)
            else:
                return False, {"error": f"Unsupported method: {method}"}
            
            return response.status_code < 400, response.json() if response.content else {}
            
        except requests.exceptions.Timeout:
            return False, {"error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return False, {"error": "Connection error"}
        except Exception as e:
            return False, {"error": str(e)}

    def test_health_endpoints(self):
        """Test health check endpoints"""
        print("\n🏥 Testing Health Check Endpoints...")
        
        # Basic health check
        success, response = self.make_request('GET', '/health')
        self.log_test("Basic Health Check", success, str(response.get('error', '')) if not success else "")
        
        # Ultimate health check
        success, response = self.make_request('GET', '/system/health-ultimate')
        self.log_test("Ultimate Health Check", success, str(response.get('error', '')) if not success else "")
        
        # Enhanced system status
        success, response = self.make_request('GET', '/system/status')
        self.log_test("Enhanced System Status", success, str(response.get('error', '')) if not success else "")
        
    def test_ai_endpoints(self):
        """Test AI processing endpoints"""
        print("\n🤖 Testing AI Processing Endpoints...")
        
        # Basic AI query
        test_query = {
            "query": "Open YouTube",
            "context": {"page_url": "https://example.com"},
            "session_id": self.session_id
        }
        
        success, response = self.make_request('POST', '/ai/query', test_query)
        self.log_test("Basic AI Query Processing", success, str(response.get('error', '')) if not success else "")
        
        # Enhanced multimodal AI query
        multimodal_query = {
            "query": "Analyze this website content",
            "context": {"current_page": "https://example.com"},
            "session_id": self.session_id,
            "include_predictions": True,
            "include_visual_feedback": True
        }
        
        success, response = self.make_request('POST', '/ai/multimodal-query', multimodal_query)
        self.log_test("Enhanced Multimodal AI Query", success, str(response.get('error', '')) if not success else "")

    def test_ultimate_proxy_system(self):
        """Test ultimate proxy system with all 6 phases"""
        print("\n🚀 Testing Ultimate Proxy System (All 6 Phases)...")
        
        # Ultimate proxy request for YouTube
        ultimate_request = {
            "url": "https://www.youtube.com",
            "method": "GET",
            "context": {"test": "ultimate_proxy"},
            "session_id": self.session_id,
            "enhance_rendering": True,
            "stealth_level": 5
        }
        
        success, response = self.make_request('POST', '/ultimate/proxy', ultimate_request, timeout=60)
        self.log_test("Ultimate Proxy - YouTube", success, str(response.get('error', '')) if not success else "")
        
        # Ultimate proxy request for Google
        ultimate_request["url"] = "https://www.google.com"
        success, response = self.make_request('POST', '/ultimate/proxy', ultimate_request, timeout=60)
        self.log_test("Ultimate Proxy - Google", success, str(response.get('error', '')) if not success else "")
        
        # Ultimate proxy request for Wikipedia
        ultimate_request["url"] = "https://en.wikipedia.org"
        success, response = self.make_request('POST', '/ultimate/proxy', ultimate_request, timeout=60)
        self.log_test("Ultimate Proxy - Wikipedia", success, str(response.get('error', '')) if not success else "")

    def test_enhanced_proxy_endpoints(self):
        """Test enhanced proxy capabilities"""
        print("\n🔄 Testing Enhanced Proxy Endpoints...")
        
        # Enhanced proxy
        proxy_request = {
            "url": "https://httpbin.org/get",
            "method": "GET"
        }
        
        success, response = self.make_request('POST', '/proxy/enhanced', proxy_request)
        self.log_test("Enhanced Proxy", success, str(response.get('error', '')) if not success else "")
        
        # Browser proxy with Playwright
        success, response = self.make_request('POST', '/proxy/browser', proxy_request)
        self.log_test("Browser Proxy (Playwright)", success, str(response.get('error', '')) if not success else "")
        
        # Basic proxy
        success, response = self.make_request('POST', '/proxy', proxy_request)
        self.log_test("Basic HTTP Proxy", success, str(response.get('error', '')) if not success else "")

    def test_real_interaction_engine(self):
        """Test real interaction engine capabilities"""
        print("\n🎯 Testing Real Interaction Engine...")
        
        # Test click interaction
        interaction_request = {
            "url": "https://httpbin.org/get",
            "interaction_type": "click",
            "interaction_params": {"selector": "body", "coordinates": [100, 100]},
            "behavior_type": "professional",
            "session_id": self.session_id,
            "stealth_level": 5
        }
        
        success, response = self.make_request('POST', '/interaction/execute', interaction_request)
        self.log_test("Real Interaction - Click", success, str(response.get('error', '')) if not success else "")
        
        # Test type interaction
        interaction_request["interaction_type"] = "type"
        interaction_request["interaction_params"] = {"selector": "input", "text": "test input"}
        
        success, response = self.make_request('POST', '/interaction/execute', interaction_request)
        self.log_test("Real Interaction - Type", success, str(response.get('error', '')) if not success else "")

    def test_advanced_rendering_system(self):
        """Test advanced rendering system"""
        print("\n🎨 Testing Advanced Rendering System...")
        
        # Enhanced rendering
        rendering_request = {
            "url": "https://httpbin.org/get",
            "rendering_profile": "balanced",
            "optimization_level": 3,
            "session_id": self.session_id
        }
        
        success, response = self.make_request('POST', '/rendering/enhanced', rendering_request, timeout=60)
        self.log_test("Advanced Rendering - Balanced Profile", success, str(response.get('error', '')) if not success else "")
        
        # Performance optimized rendering
        rendering_request["rendering_profile"] = "performance_optimized"
        rendering_request["optimization_level"] = 5
        
        success, response = self.make_request('POST', '/rendering/enhanced', rendering_request, timeout=60)
        self.log_test("Advanced Rendering - Performance Optimized", success, str(response.get('error', '')) if not success else "")

    def test_system_analytics(self):
        """Test system analytics"""
        print("\n📊 Testing System Analytics...")
        
        # System analytics
        success, response = self.make_request('GET', '/system/analytics')
        self.log_test("System Analytics", success, str(response.get('error', '')) if not success else "")
        
        # User analytics
        success, response = self.make_request('GET', f'/user/{self.session_id}/analytics')
        self.log_test("User Analytics", success, str(response.get('error', '')) if not success else "")

    def test_voice_and_image_processing(self):
        """Test voice commands and image analysis"""
        print("\n🎤📸 Testing Voice Commands & Image Analysis...")
        
        # Note: These endpoints require file uploads, so we'll test the endpoint availability
        # Voice command endpoint check
        success, response = self.make_request('POST', '/ai/voice-command', {})
        # Expect 422 (validation error) since we're not sending a file - this means endpoint exists
        if response.get('error') and '422' in str(response.get('error', '')):
            self.log_test("Voice Command Endpoint Available", True, "")
        else:
            self.log_test("Voice Command Endpoint Available", success, str(response.get('error', '')) if not success else "")
        
        # Image analysis endpoint check
        success, response = self.make_request('POST', '/ai/analyze-image', {})
        # Expect 422 (validation error) since we're not sending a file - this means endpoint exists
        if response.get('error') and '422' in str(response.get('error', '')):
            self.log_test("Image Analysis Endpoint Available", True, "")
        else:
            self.log_test("Image Analysis Endpoint Available", success, str(response.get('error', '')) if not success else "")

    def test_stealth_capabilities(self):
        """Test stealth testing capabilities"""
        print("\n🥷 Testing Stealth Capabilities...")
        
        # Test stealth against different domains
        test_domains = ["httpbin.org", "example.com"]
        
        for domain in test_domains:
            success, response = self.make_request('GET', f'/stealth/test/{domain}', timeout=45)
            self.log_test(f"Stealth Test - {domain}", success, str(response.get('error', '')) if not success else "")

    def test_browser_functionality(self):
        """Test browser functionality"""
        print("\n🌐 Testing Browser Functionality...")
        
        # Execute browser command
        browser_command = {
            "command": "navigate",
            "url": "https://httpbin.org/get",
            "session_id": self.session_id
        }
        
        success, response = self.make_request('POST', '/browser/execute', browser_command)
        self.log_test("Browser Command Execution", success, str(response.get('error', '')) if not success else "")
        
        # Get active sessions
        success, response = self.make_request('GET', '/sessions')
        self.log_test("Get Active Sessions", success, str(response.get('error', '')) if not success else "")
        
        # Navigation with proxy
        nav_request = {
            "url": "https://httpbin.org/get",
            "session_id": self.session_id
        }
        
        success, response = self.make_request('POST', '/navigate', nav_request)
        self.log_test("Navigation with Proxy", success, str(response.get('error', '')) if not success else "")

    def test_browser_endpoints(self):
        """Test browser functionality"""
        print("\n🌐 Testing Browser Endpoints...")
        
        # Execute browser command
        browser_command = {
            "command": "navigate",
            "url": "https://example.com",
            "session_id": "test_session_123"
        }
        
        success, response = self.make_request('POST', '/browser/execute', browser_command)
        self.log_test("Browser Command Execution", success, str(response.get('error', '')) if not success else "")
        
        # Get active sessions
        success, response = self.make_request('GET', '/sessions')
        self.log_test("Get Active Sessions", success, str(response.get('error', '')) if not success else "")

    def test_proxy_endpoints(self):
        """Test proxy functionality"""
        print("\n🔄 Testing Proxy Endpoints...")
        
        # Enhanced proxy
        proxy_request = {
            "url": "https://httpbin.org/get",
            "method": "GET"
        }
        
        success, response = self.make_request('POST', '/proxy/enhanced', proxy_request)
        self.log_test("Enhanced Proxy", success, str(response.get('error', '')) if not success else "")
        
        # Navigation with proxy
        nav_request = {
            "url": "https://httpbin.org/get",
            "session_id": "test_session_123"
        }
        
        success, response = self.make_request('POST', '/navigate', nav_request)
        self.log_test("Navigation with Proxy", success, str(response.get('error', '')) if not success else "")

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Comprehensive Kairo AI Browser API Tests")
        print(f"🎯 Testing against: {self.base_url}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test suites
        self.test_basic_endpoints()
        self.test_ai_query_endpoint()
        self.test_enhanced_search_endpoints()
        self.test_agent_builder_endpoints()
        self.test_report_generation_endpoints()
        self.test_accessibility_endpoints()
        self.test_shadow_browser_endpoints()
        self.test_memory_endpoints()
        self.test_intelligence_endpoints()
        self.test_workspace_endpoints()
        self.test_browser_endpoints()
        self.test_proxy_endpoints()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        print(f"✅ Tests Passed: {self.tests_passed}/{self.tests_run}")
        print(f"❌ Tests Failed: {len(self.failed_tests)}/{self.tests_run}")
        
        if self.failed_tests:
            print("\n🚨 FAILED TESTS:")
            for i, failure in enumerate(self.failed_tests, 1):
                print(f"   {i}. {failure}")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 Overall Status: GOOD - Most features working")
        elif success_rate >= 60:
            print("⚠️  Overall Status: MODERATE - Some issues need attention")
        else:
            print("🚨 Overall Status: POOR - Major issues detected")
        
        return success_rate >= 80

def main():
    """Main test execution"""
    tester = KairoAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())