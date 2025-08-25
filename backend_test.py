#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Kairo AI Browser
Testing all enhanced Fellou-level capabilities
"""
import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any

class KairoAPITester:
    def __init__(self, base_url="https://initial-ui-setup.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        
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

    def test_basic_endpoints(self):
        """Test basic system endpoints"""
        print("\n🔍 Testing Basic System Endpoints...")
        
        # Health check
        success, response = self.make_request('GET', '/health')
        self.log_test("Health Check", success, str(response.get('error', '')) if not success else "")
        
        # Root endpoint
        success, response = self.make_request('GET', '')
        self.log_test("Root Endpoint", success, str(response.get('error', '')) if not success else "")
        
        # Enhanced system status
        success, response = self.make_request('GET', '/system/status')
        self.log_test("Enhanced System Status", success, str(response.get('error', '')) if not success else "")
        
    def test_ai_query_endpoint(self):
        """Test AI query processing"""
        print("\n🤖 Testing AI Query Endpoint...")
        
        test_query = {
            "query": "What is artificial intelligence?",
            "context": {"page_url": "https://example.com"},
            "session_id": "test_session_123"
        }
        
        success, response = self.make_request('POST', '/ai/query', test_query)
        self.log_test("AI Query Processing", success, str(response.get('error', '')) if not success else "")

    def test_enhanced_search_endpoints(self):
        """Test enhanced search capabilities"""
        print("\n🔍 Testing Enhanced Search Endpoints...")
        
        # Deep search
        search_request = {
            "query": "AI trends 2024",
            "config": {"sources": ["google", "bing"], "max_results": 5}
        }
        
        success, response = self.make_request('POST', '/search/deep', search_request, timeout=60)
        self.log_test("Deep Search", success, str(response.get('error', '')) if not success else "")

    def test_agent_builder_endpoints(self):
        """Test agent builder capabilities"""
        print("\n🤖 Testing Agent Builder Endpoints...")
        
        # Create agent from description
        agent_request = {
            "description": "Create an agent that scrapes product prices from e-commerce sites",
            "user_id": "test_user_123",
            "config": {"timeout": 30}
        }
        
        success, response = self.make_request('POST', '/agents/create/description', agent_request)
        self.log_test("Create Agent from Description", success, str(response.get('error', '')) if not success else "")
        
        # List user agents
        success, response = self.make_request('GET', '/agents/user/test_user_123')
        self.log_test("List User Agents", success, str(response.get('error', '')) if not success else "")
        
        # Get agent marketplace
        success, response = self.make_request('GET', '/agents/marketplace')
        self.log_test("Agent Marketplace", success, str(response.get('error', '')) if not success else "")

    def test_report_generation_endpoints(self):
        """Test report generation capabilities"""
        print("\n📊 Testing Report Generation Endpoints...")
        
        report_request = {
            "type": "analytics",
            "config": {"data_source": "web_activity", "period": "week", "async": False}
        }
        
        success, response = self.make_request('POST', '/reports/generate', report_request, timeout=60)
        self.log_test("Generate Analytics Report", success, str(response.get('error', '')) if not success else "")

    def test_accessibility_endpoints(self):
        """Test accessibility features"""
        print("\n♿ Testing Accessibility Endpoints...")
        
        # Text-to-speech
        tts_request = {
            "text": "Hello, this is a test of the text-to-speech functionality.",
            "options": {"voice": "default", "speed": 1.0}
        }
        
        success, response = self.make_request('POST', '/accessibility/tts', tts_request)
        self.log_test("Text-to-Speech", success, str(response.get('error', '')) if not success else "")
        
        # Translation
        translate_request = {
            "text": "Hello world",
            "target_language": "es",
            "source_language": "en"
        }
        
        success, response = self.make_request('POST', '/accessibility/translate', translate_request)
        self.log_test("Text Translation", success, str(response.get('error', '')) if not success else "")
        
        # Reading assistance
        reading_request = {
            "text": "This is a complex sentence that needs to be simplified for better readability.",
            "reading_level": "simple"
        }
        
        success, response = self.make_request('POST', '/accessibility/reading', reading_request)
        self.log_test("Reading Assistance", success, str(response.get('error', '')) if not success else "")

    def test_shadow_browser_endpoints(self):
        """Test shadow browser capabilities"""
        print("\n👤 Testing Shadow Browser Endpoints...")
        
        # Execute background task
        task_request = {
            "type": "scraping",
            "config": {
                "url": "https://example.com",
                "selectors": ["title", "h1"],
                "timeout": 30
            }
        }
        
        success, response = self.make_request('POST', '/shadow/execute', task_request)
        task_id = None
        if success and 'task_id' in response:
            task_id = response['task_id']
        
        self.log_test("Execute Shadow Browser Task", success, str(response.get('error', '')) if not success else "")
        
        # Check task status if task was created
        if task_id:
            time.sleep(2)  # Wait a bit for task to process
            success, response = self.make_request('GET', f'/shadow/status/{task_id}')
            self.log_test("Get Shadow Task Status", success, str(response.get('error', '')) if not success else "")

    def test_memory_endpoints(self):
        """Test memory and personalization"""
        print("\n🧠 Testing Memory Endpoints...")
        
        # Learn from interaction
        interaction_request = {
            "user_id": "test_user_123",
            "command": "search for AI trends",
            "context": {"page": "dashboard", "time": "morning"},
            "outcome": "success"
        }
        
        success, response = self.make_request('POST', '/memory/learn', interaction_request)
        self.log_test("Memory Learning", success, str(response.get('error', '')) if not success else "")
        
        # Get personalized suggestions
        success, response = self.make_request('GET', '/memory/suggestions/test_user_123?context={"page":"dashboard"}')
        self.log_test("Personalized Suggestions", success, str(response.get('error', '')) if not success else "")

    def test_intelligence_endpoints(self):
        """Test intelligence analysis"""
        print("\n🧠 Testing Intelligence Endpoints...")
        
        intelligence_request = {
            "user_id": "test_user_123",
            "context": {
                "current_page": "https://example.com",
                "user_activity": "research",
                "time_of_day": "afternoon"
            }
        }
        
        success, response = self.make_request('POST', '/intelligence/analyze', intelligence_request)
        self.log_test("Intelligence Analysis", success, str(response.get('error', '')) if not success else "")

    def test_workspace_endpoints(self):
        """Test workspace management"""
        print("\n🏢 Testing Workspace Endpoints...")
        
        # Create workspace
        workspace_request = {
            "name": "Test Workspace",
            "description": "A test workspace for API testing",
            "user_id": "test_user_123",
            "settings": {"theme": "dark", "auto_save": True}
        }
        
        success, response = self.make_request('POST', '/workspaces/create', workspace_request)
        self.log_test("Create Workspace", success, str(response.get('error', '')) if not success else "")
        
        # List user workspaces
        success, response = self.make_request('GET', '/workspaces/user/test_user_123')
        self.log_test("List User Workspaces", success, str(response.get('error', '')) if not success else "")

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