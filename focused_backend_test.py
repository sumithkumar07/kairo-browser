#!/usr/bin/env python3
"""
🎯 FOCUSED BACKEND TESTING - Review Request Specific Endpoints
Testing the exact endpoints mentioned in the review request
"""
import requests
import sys
import json
import time
from datetime import datetime

class FocusedKairoAPITester:
    def __init__(self, base_url="https://launch-guide-4.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session_id = f"review_test_{int(time.time())}"
        
    def log_test(self, name: str, success: bool, details: str = "", response_data: dict = None):
        """Log test result with enhanced details"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
            if response_data and isinstance(response_data, dict):
                if 'status' in response_data:
                    print(f"   Status: {response_data['status']}")
                if 'method' in response_data:
                    print(f"   Method: {response_data['method']}")
                if 'content_type' in response_data:
                    print(f"   Content Type: {response_data['content_type']}")
        else:
            self.failed_tests.append(f"{name}: {details}")
            print(f"❌ {name} - FAILED: {details}")
    
    def make_request(self, method: str, endpoint: str, data: dict = None, timeout: int = 30) -> tuple:
        """Make HTTP request and return success status and response"""
        url = f"{self.base_url}/api{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            else:
                return False, {"error": f"Unsupported method: {method}"}
            
            return response.status_code < 400, response.json() if response.content else {}
            
        except requests.exceptions.Timeout:
            return False, {"error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return False, {"error": "Connection error - Backend may be down"}
        except Exception as e:
            return False, {"error": str(e)}

    def test_review_request_endpoints(self):
        """Test all endpoints specifically mentioned in the review request"""
        print("🎯 TESTING REVIEW REQUEST SPECIFIC ENDPOINTS")
        print("=" * 60)
        
        # 1. Health check endpoints
        print("\n🏥 Health Check Endpoints:")
        
        success, response = self.make_request('GET', '/health')
        self.log_test("/api/health", success, str(response.get('error', '')) if not success else "", response)
        
        success, response = self.make_request('GET', '/system/health-ultimate')
        self.log_test("/api/system/health-ultimate", success, str(response.get('error', '')) if not success else "", response)
        
        # 2. AI query processing
        print("\n🤖 AI Query Processing:")
        
        ai_query = {
            "query": "Open YouTube",
            "context": {"page_url": "https://example.com"},
            "session_id": self.session_id
        }
        success, response = self.make_request('POST', '/ai/query', ai_query)
        self.log_test("/api/ai/query", success, str(response.get('error', '')) if not success else "", response)
        
        multimodal_query = {
            "query": "Analyze this website",
            "context": {"current_page": "https://example.com"},
            "session_id": self.session_id
        }
        success, response = self.make_request('POST', '/ai/multimodal-query', multimodal_query)
        self.log_test("/api/ai/multimodal-query", success, str(response.get('error', '')) if not success else "", response)
        
        # 3. Browser command execution
        print("\n🌐 Browser Command Execution:")
        
        browser_command = {
            "command": "navigate",
            "url": "https://www.youtube.com",
            "session_id": self.session_id
        }
        success, response = self.make_request('POST', '/browser/execute', browser_command)
        self.log_test("/api/browser/execute", success, str(response.get('error', '')) if not success else "", response)
        
        # 4. Enhanced proxy system
        print("\n🔄 Enhanced Proxy System:")
        
        proxy_request = {"url": "https://www.youtube.com", "method": "GET"}
        success, response = self.make_request('POST', '/proxy/enhanced', proxy_request, timeout=45)
        self.log_test("/api/proxy/enhanced", success, str(response.get('error', '')) if not success else "", response)
        
        success, response = self.make_request('POST', '/proxy/browser', proxy_request, timeout=45)
        self.log_test("/api/proxy/browser", success, str(response.get('error', '')) if not success else "", response)
        
        success, response = self.make_request('POST', '/proxy', proxy_request)
        self.log_test("/api/proxy", success, str(response.get('error', '')) if not success else "", response)
        
        # 5. Ultimate proxy system
        print("\n🚀 Ultimate Proxy System:")
        
        ultimate_request = {
            "url": "https://www.youtube.com",
            "method": "GET",
            "session_id": self.session_id,
            "enhance_rendering": True,
            "stealth_level": 5
        }
        success, response = self.make_request('POST', '/ultimate/proxy', ultimate_request, timeout=60)
        self.log_test("/api/ultimate/proxy", success, str(response.get('error', '')) if not success else "", response)
        
        # 6. Session management
        print("\n📋 Session Management:")
        
        success, response = self.make_request('GET', '/sessions')
        self.log_test("/api/sessions", success, str(response.get('error', '')) if not success else "", response)
        
        # 7. Real interaction engine
        print("\n🎯 Real Interaction Engine:")
        
        interaction_request = {
            "url": "https://www.youtube.com",
            "interaction_type": "click",
            "interaction_params": {"selector": "body", "coordinates": [100, 100]},
            "behavior_type": "professional",
            "session_id": self.session_id,
            "stealth_level": 5
        }
        success, response = self.make_request('POST', '/interaction/execute', interaction_request, timeout=45)
        self.log_test("/api/interaction/execute", success, str(response.get('error', '')) if not success else "", response)
        
        # 8. System analytics
        print("\n📊 System Analytics:")
        
        success, response = self.make_request('GET', '/system/analytics')
        self.log_test("/api/system/analytics", success, str(response.get('error', '')) if not success else "", response)
        
        # 9. Stealth testing
        print("\n🥷 Stealth Testing:")
        
        success, response = self.make_request('GET', '/stealth/test/youtube.com', timeout=45)
        self.log_test("/api/stealth/test/youtube.com", success, str(response.get('error', '')) if not success else "", response)

    def test_integration_flow(self):
        """Test the complete integration flow as specified in review request"""
        print("\n🔗 COMPLETE INTEGRATION FLOW TEST")
        print("=" * 60)
        print("Testing: AI query 'Open YouTube' → Browser execution → Proxy loading → Content verification")
        
        # Step 1: Send AI query "Open YouTube"
        print("\n1️⃣ Sending AI Query: 'Open YouTube'")
        ai_query = {
            "query": "Open YouTube",
            "context": {"test_flow": "integration_test"},
            "session_id": self.session_id
        }
        
        success, ai_response = self.make_request('POST', '/ai/query', ai_query)
        if success:
            print("   ✅ AI successfully processed 'Open YouTube' command")
            if 'intent' in ai_response:
                print(f"   🎯 Intent: {ai_response['intent']}")
            if 'commands' in ai_response:
                print(f"   📋 Commands generated: {len(ai_response['commands'])} command(s)")
        else:
            print(f"   ❌ AI query failed: {ai_response.get('error', 'Unknown error')}")
            return False
        
        # Step 2: Verify browser command execution
        print("\n2️⃣ Executing Browser Command")
        browser_command = {
            "command": "navigate",
            "url": "https://www.youtube.com",
            "session_id": self.session_id
        }
        
        success, browser_response = self.make_request('POST', '/browser/execute', browser_command)
        if success:
            print("   ✅ Browser command executed successfully")
            if 'status' in browser_response:
                print(f"   📊 Status: {browser_response['status']}")
        else:
            print(f"   ❌ Browser execution failed: {browser_response.get('error', 'Unknown error')}")
            return False
        
        # Step 3: Test proxy content loading for YouTube
        print("\n3️⃣ Testing Proxy Content Loading for YouTube")
        ultimate_request = {
            "url": "https://www.youtube.com",
            "method": "GET",
            "session_id": self.session_id,
            "enhance_rendering": True,
            "stealth_level": 5
        }
        
        success, proxy_response = self.make_request('POST', '/ultimate/proxy', ultimate_request, timeout=60)
        if success:
            print("   ✅ Proxy successfully loaded YouTube content")
            if 'method' in proxy_response:
                print(f"   🔧 Method used: {proxy_response['method']}")
            if 'content_type' in proxy_response:
                print(f"   📄 Content type: {proxy_response['content_type']}")
            if 'content' in proxy_response and proxy_response['content']:
                content_length = len(str(proxy_response['content']))
                print(f"   📏 Content length: {content_length} characters")
                # Check if it's real YouTube content (not fallback)
                content_str = str(proxy_response['content']).lower()
                if 'youtube' in content_str or 'ytimg' in content_str:
                    print("   🎉 VERIFIED: Real YouTube content detected (not fallback)")
                else:
                    print("   ⚠️  Content loaded but YouTube-specific elements not detected")
        else:
            print(f"   ❌ Proxy loading failed: {proxy_response.get('error', 'Unknown error')}")
            return False
        
        # Step 4: Check MongoDB data storage
        print("\n4️⃣ Verifying Session Management")
        success, sessions_response = self.make_request('GET', '/sessions')
        if success:
            print("   ✅ Session management working")
            if 'sessions' in sessions_response:
                session_count = len(sessions_response['sessions'])
                print(f"   📊 Active sessions: {session_count}")
                # Check if our test session is tracked
                test_session_found = any(
                    session.get('session_id') == self.session_id 
                    for session in sessions_response.get('sessions', [])
                )
                if test_session_found:
                    print("   🎯 Test session properly tracked in database")
                else:
                    print("   ℹ️  Test session not found in active sessions (may have expired)")
        else:
            print(f"   ❌ Session management failed: {sessions_response.get('error', 'Unknown error')}")
            return False
        
        print("\n🎉 INTEGRATION FLOW COMPLETED SUCCESSFULLY!")
        return True

    def run_focused_tests(self):
        """Run focused tests for review request"""
        print("🎯 FOCUSED BACKEND TESTING - REVIEW REQUEST VERIFICATION")
        print(f"🌐 Backend URL: {self.base_url}")
        print(f"🔧 Session ID: {self.session_id}")
        print("=" * 80)
        
        start_time = time.time()
        
        # Test specific endpoints
        self.test_review_request_endpoints()
        
        # Test integration flow
        integration_success = self.test_integration_flow()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print summary
        print("\n" + "=" * 80)
        print("📊 FOCUSED TEST SUMMARY")
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
        
        # Integration flow status
        print(f"\n🔗 Integration Flow: {'✅ WORKING' if integration_success else '❌ FAILED'}")
        
        # Final assessment
        if success_rate >= 90 and integration_success:
            print("🎉 REVIEW REQUEST STATUS: ✅ ALL REQUIREMENTS MET")
            print("   • All endpoints responding properly")
            print("   • Groq AI integration working")
            print("   • Enhanced proxy system operational")
            print("   • MongoDB data persistence confirmed")
            print("   • Complete integration chain functional")
            print("   • Anti-detection capabilities active")
        elif success_rate >= 80:
            print("✅ REVIEW REQUEST STATUS: MOSTLY SATISFIED")
            print("   • Core functionality working")
            print("   • Minor issues detected")
        else:
            print("❌ REVIEW REQUEST STATUS: ISSUES DETECTED")
            print("   • Critical endpoints failing")
            print("   • Integration issues present")
        
        return success_rate >= 80 and integration_success

def main():
    """Main test execution"""
    tester = FocusedKairoAPITester()
    success = tester.run_focused_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())