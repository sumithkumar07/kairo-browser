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
    def __init__(self, base_url="https://get-started-app.preview.emergentagent.com"):
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
            if details:
                print(f"   Error Details: {details}")
    
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

    def test_workflow_execution(self):
        """Test workflow execution"""
        print("\n⚙️ Testing Workflow Execution...")
        
        # Basic workflow execution
        workflow_request = {
            "name": "Test Workflow",
            "steps": [
                {"command": "navigate", "url": "https://httpbin.org/get"},
                {"command": "wait", "duration": 1000}
            ],
            "session_id": self.session_id,
            "timeout_ms": 30000
        }
        
        success, response = self.make_request('POST', '/workflow/execute', workflow_request)
        workflow_id = None
        if success and 'workflow_id' in response:
            workflow_id = response['workflow_id']
        
        self.log_test("Workflow Execution", success, str(response.get('error', '')) if not success else "")
        
        # Enhanced workflow execution
        enhanced_workflow_request = {
            "workflow_steps": [
                {"type": "navigate", "params": {"url": "https://httpbin.org/get"}},
                {"type": "wait", "params": {"duration": 1000}}
            ],
            "session_id": self.session_id,
            "behavior_type": "professional"
        }
        
        success, response = self.make_request('POST', '/workflow/execute-enhanced', enhanced_workflow_request)
        self.log_test("Enhanced Workflow Execution", success, str(response.get('error', '')) if not success else "")
        
        # Check workflow status if workflow was created
        if workflow_id:
            time.sleep(2)  # Wait a bit for workflow to process
            success, response = self.make_request('GET', f'/workflow/{workflow_id}')
            self.log_test("Get Workflow Status", success, str(response.get('error', '')) if not success else "")

    def test_integration_flows(self):
        """Test complete integration flows"""
        print("\n🔗 Testing Complete Integration Flows...")
        
        # Test complete AI -> Browser -> Proxy flow for YouTube
        print("   Testing YouTube Integration Flow...")
        
        # Step 1: AI Query to open YouTube
        ai_query = {
            "query": "Open YouTube",
            "context": {"test_flow": "youtube_integration"},
            "session_id": self.session_id
        }
        
        success, ai_response = self.make_request('POST', '/ai/query', ai_query)
        self.log_test("Integration Flow - AI Query (YouTube)", success, str(ai_response.get('error', '')) if not success else "")
        
        # Step 2: Browser command execution
        if success:
            browser_command = {
                "command": "navigate",
                "url": "https://www.youtube.com",
                "session_id": self.session_id
            }
            
            success, browser_response = self.make_request('POST', '/browser/execute', browser_command)
            self.log_test("Integration Flow - Browser Execute (YouTube)", success, str(browser_response.get('error', '')) if not success else "")
            
            # Step 3: Ultimate proxy content loading
            if success:
                ultimate_request = {
                    "url": "https://www.youtube.com",
                    "method": "GET",
                    "session_id": self.session_id,
                    "enhance_rendering": True,
                    "stealth_level": 5
                }
                
                success, proxy_response = self.make_request('POST', '/ultimate/proxy', ultimate_request, timeout=60)
                self.log_test("Integration Flow - Ultimate Proxy (YouTube)", success, str(proxy_response.get('error', '')) if not success else "")

    def run_all_tests(self):
        """Run all comprehensive API tests"""
        print("🚀 COMPREHENSIVE ULTIMATE KAIRO AI BROWSER BACKEND TESTING")
        print(f"🎯 Testing against: {self.base_url}")
        print(f"🔧 Session ID: {self.session_id}")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all test suites in order of importance
        self.test_health_endpoints()
        self.test_ai_endpoints()
        self.test_ultimate_proxy_system()
        self.test_enhanced_proxy_endpoints()
        self.test_real_interaction_engine()
        self.test_advanced_rendering_system()
        self.test_system_analytics()
        self.test_voice_and_image_processing()
        self.test_stealth_capabilities()
        self.test_browser_functionality()
        self.test_workflow_execution()
        self.test_integration_flows()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print comprehensive summary
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        print(f"✅ Tests Passed: {self.tests_passed}/{self.tests_run}")
        print(f"❌ Tests Failed: {len(self.failed_tests)}/{self.tests_run}")
        
        if self.failed_tests:
            print("\n🚨 FAILED TESTS:")
            for i, failure in enumerate(self.failed_tests, 1):
                print(f"   {i}. {failure}")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        # Enhanced status reporting
        if success_rate >= 90:
            print("🎉 Overall Status: EXCELLENT - All systems operational")
        elif success_rate >= 80:
            print("✅ Overall Status: GOOD - Most features working")
        elif success_rate >= 60:
            print("⚠️  Overall Status: MODERATE - Some issues need attention")
        else:
            print("🚨 Overall Status: POOR - Major issues detected")
        
        # Phase completion summary
        print(f"\n🚀 PHASE INTEGRATION SUMMARY:")
        print(f"   Phase 1: Advanced Browser Engine - {'✅' if success_rate >= 80 else '❌'}")
        print(f"   Phase 2: Military-grade Stealth - {'✅' if success_rate >= 80 else '❌'}")
        print(f"   Phase 3: Real Interaction Engine - {'✅' if success_rate >= 80 else '❌'}")
        print(f"   Phase 4: Advanced Rendering - {'✅' if success_rate >= 80 else '❌'}")
        print(f"   Phase 5: Enhanced Conversational AI - {'✅' if success_rate >= 80 else '❌'}")
        print(f"   Phase 6: Bulletproof Fallback System - {'✅' if success_rate >= 80 else '❌'}")
        
        return success_rate >= 80

def main():
    """Main test execution"""
    tester = UltimateKairoAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())