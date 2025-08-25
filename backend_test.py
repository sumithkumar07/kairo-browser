#!/usr/bin/env python3
"""
Comprehensive Backend Test Suite for Kairo AI Browser
Tests all API endpoints and functionality
"""

import requests
import json
import time
import uuid
from datetime import datetime
import sys

# Configuration
BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api"

class KairoBackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.session_id = str(uuid.uuid4())
        
    def log_test(self, test_name, success, message="", response_data=None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        
    def test_health_check(self):
        """Test /api/health endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/health")
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "healthy":
                    self.log_test("Health Check", True, "API is healthy", data)
                    return True
                else:
                    self.log_test("Health Check", False, f"Unexpected response format: {data}")
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Health Check", False, f"Exception: {str(e)}")
        return False
        
    def test_ai_query(self):
        """Test /api/ai/query endpoint"""
        try:
            # Test basic AI query
            query_data = {
                "query": "Open YouTube",
                "session_id": self.session_id
            }
            
            response = self.session.post(f"{API_BASE}/ai/query", json=query_data)
            if response.status_code == 200:
                data = response.json()
                # Check if response has expected structure
                if "intent" in data or "commands" in data or "explanation" in data:
                    self.log_test("AI Query - Basic", True, "AI query processed successfully", data)
                    
                    # Test another query
                    search_query = {
                        "query": "Search for artificial intelligence tutorials",
                        "session_id": self.session_id,
                        "context": {"page": "youtube"}
                    }
                    
                    response2 = self.session.post(f"{API_BASE}/ai/query", json=search_query)
                    if response2.status_code == 200:
                        data2 = response2.json()
                        self.log_test("AI Query - With Context", True, "AI query with context processed", data2)
                        return True
                    else:
                        self.log_test("AI Query - With Context", False, f"HTTP {response2.status_code}: {response2.text}")
                else:
                    self.log_test("AI Query - Basic", False, f"Unexpected response format: {data}")
            else:
                self.log_test("AI Query - Basic", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("AI Query", False, f"Exception: {str(e)}")
        return False
        
    def test_browser_execute(self):
        """Test /api/browser/execute endpoint"""
        try:
            # Test open command
            open_command = {
                "command": "open",
                "url": "https://youtube.com",
                "session_id": self.session_id
            }
            
            response = self.session.post(f"{API_BASE}/browser/execute", json=open_command)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "executed" and "data" in data:
                    self.log_test("Browser Execute - Open", True, "Open command executed", data)
                else:
                    self.log_test("Browser Execute - Open", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Browser Execute - Open", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
            # Test click command
            click_command = {
                "command": "click",
                "selector": "input[type='search']",
                "session_id": self.session_id
            }
            
            response = self.session.post(f"{API_BASE}/browser/execute", json=click_command)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "executed":
                    self.log_test("Browser Execute - Click", True, "Click command executed", data)
                else:
                    self.log_test("Browser Execute - Click", False, f"Unexpected response: {data}")
                    return False
            else:
                self.log_test("Browser Execute - Click", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
            # Test type command
            type_command = {
                "command": "type",
                "selector": "input[type='search']",
                "text": "AI tutorials",
                "session_id": self.session_id
            }
            
            response = self.session.post(f"{API_BASE}/browser/execute", json=type_command)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "executed":
                    self.log_test("Browser Execute - Type", True, "Type command executed", data)
                    return True
                else:
                    self.log_test("Browser Execute - Type", False, f"Unexpected response: {data}")
            else:
                self.log_test("Browser Execute - Type", False, f"HTTP {response.status_code}: {response.text}")
                
            # Test invalid command
            invalid_command = {
                "command": "invalid_command",
                "session_id": self.session_id
            }
            
            response = self.session.post(f"{API_BASE}/browser/execute", json=invalid_command)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "unknown_command":
                    self.log_test("Browser Execute - Invalid Command", True, "Invalid command handled correctly", data)
                else:
                    self.log_test("Browser Execute - Invalid Command", False, f"Unexpected response: {data}")
            else:
                self.log_test("Browser Execute - Invalid Command", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Browser Execute", False, f"Exception: {str(e)}")
        return False
        
    def test_workflow_execute(self):
        """Test /api/workflow/execute endpoint"""
        try:
            # Create a test workflow
            workflow_data = {
                "name": "YouTube Search Workflow",
                "steps": [
                    {
                        "type": "open",
                        "url": "https://youtube.com",
                        "timeout_ms": 5000
                    },
                    {
                        "type": "wait",
                        "timeout_ms": 2000
                    },
                    {
                        "type": "click",
                        "selector": "input[type='search']",
                        "timeout_ms": 3000
                    },
                    {
                        "type": "type",
                        "selector": "input[type='search']",
                        "text": "AI browser automation",
                        "timeout_ms": 2000
                    },
                    {
                        "type": "screenshot",
                        "timeout_ms": 1000
                    }
                ],
                "profile": "default",
                "timeout_ms": 60000
            }
            
            response = self.session.post(f"{API_BASE}/workflow/execute", json=workflow_data)
            if response.status_code == 200:
                data = response.json()
                if "workflow_id" in data and data.get("status") == "started":
                    workflow_id = data["workflow_id"]
                    self.log_test("Workflow Execute", True, f"Workflow started with ID: {workflow_id}", data)
                    
                    # Wait a bit for workflow to process
                    time.sleep(3)
                    
                    # Test workflow status endpoint
                    return self.test_workflow_status(workflow_id)
                else:
                    self.log_test("Workflow Execute", False, f"Unexpected response: {data}")
            else:
                self.log_test("Workflow Execute", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Workflow Execute", False, f"Exception: {str(e)}")
        return False
        
    def test_workflow_status(self, workflow_id):
        """Test /api/workflow/{workflow_id} endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/workflow/{workflow_id}")
            if response.status_code == 200:
                data = response.json()
                if "id" in data and "status" in data:
                    self.log_test("Workflow Status", True, f"Workflow status: {data.get('status')}", data)
                    return True
                else:
                    self.log_test("Workflow Status", False, f"Unexpected response format: {data}")
            else:
                self.log_test("Workflow Status", False, f"HTTP {response.status_code}: {response.text}")
                
            # Test non-existent workflow
            fake_id = str(uuid.uuid4())
            response = self.session.get(f"{API_BASE}/workflow/{fake_id}")
            if response.status_code == 404:
                self.log_test("Workflow Status - Not Found", True, "404 returned for non-existent workflow")
            else:
                self.log_test("Workflow Status - Not Found", False, f"Expected 404, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Workflow Status", False, f"Exception: {str(e)}")
        return False
        
    def test_sessions(self):
        """Test /api/sessions endpoint"""
        try:
            response = self.session.get(f"{API_BASE}/sessions")
            if response.status_code == 200:
                data = response.json()
                if "sessions" in data and isinstance(data["sessions"], list):
                    self.log_test("Sessions", True, f"Retrieved {len(data['sessions'])} sessions", data)
                    return True
                else:
                    self.log_test("Sessions", False, f"Unexpected response format: {data}")
            else:
                self.log_test("Sessions", False, f"HTTP {response.status_code}: {response.text}")
        except Exception as e:
            self.log_test("Sessions", False, f"Exception: {str(e)}")
        return False
        
    def test_proxy(self):
        """Test /api/proxy endpoint"""
        try:
            # Test proxying a simple website
            proxy_data = {
                "url": "https://httpbin.org/json"
            }
            
            response = self.session.post(f"{API_BASE}/proxy", json=proxy_data)
            if response.status_code == 200:
                data = response.json()
                if "content" in data and "status_code" in data:
                    self.log_test("Proxy - Basic", True, f"Basic proxy successful, status: {data.get('status_code')}", 
                                {"url": data.get("url"), "status_code": data.get("status_code")})
                else:
                    self.log_test("Proxy - Basic", False, f"Unexpected response format: {data}")
                    return False
            else:
                self.log_test("Proxy - Basic", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
            # Test proxy without URL
            response = self.session.post(f"{API_BASE}/proxy", json={})
            if response.status_code == 400:
                self.log_test("Proxy - No URL", True, "400 returned when URL missing")
                return True
            else:
                self.log_test("Proxy - No URL", False, f"Expected 400, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Proxy - Basic", False, f"Exception: {str(e)}")
        return False
        
    def test_enhanced_proxy(self):
        """Test /api/proxy/enhanced endpoint with smart routing"""
        try:
            # Test enhanced proxy with Wikipedia (should use HTTP proxy)
            wikipedia_data = {
                "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
            }
            
            response = self.session.post(f"{API_BASE}/proxy/enhanced", json=wikipedia_data, timeout=60)
            if response.status_code == 200:
                data = response.json()
                if "content" in data and "method" in data and "iframe_safe" in data:
                    method_used = data.get("method", "unknown")
                    self.log_test("Enhanced Proxy - Wikipedia", True, 
                                f"Enhanced proxy successful, method: {method_used}", 
                                {"url": data.get("url"), "method": method_used, "iframe_safe": data.get("iframe_safe")})
                else:
                    self.log_test("Enhanced Proxy - Wikipedia", False, f"Unexpected response format: {data}")
                    return False
            else:
                self.log_test("Enhanced Proxy - Wikipedia", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
            # Test enhanced proxy with YouTube (should use browser engine)
            youtube_data = {
                "url": "https://www.youtube.com"
            }
            
            response = self.session.post(f"{API_BASE}/proxy/enhanced", json=youtube_data, timeout=90)
            if response.status_code == 200:
                data = response.json()
                if "content" in data and "method" in data:
                    method_used = data.get("method", "unknown")
                    self.log_test("Enhanced Proxy - YouTube", True, 
                                f"Enhanced proxy successful, method: {method_used}", 
                                {"url": data.get("url"), "method": method_used})
                    return True
                else:
                    self.log_test("Enhanced Proxy - YouTube", False, f"Unexpected response format: {data}")
            else:
                self.log_test("Enhanced Proxy - YouTube", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Enhanced Proxy", False, f"Exception: {str(e)}")
        return False
        
    def test_browser_proxy(self):
        """Test /api/proxy/browser endpoint with Playwright"""
        try:
            # Test browser proxy with a JavaScript-heavy site
            browser_data = {
                "url": "https://www.google.com"
            }
            
            response = self.session.post(f"{API_BASE}/proxy/browser", json=browser_data, timeout=90)
            if response.status_code == 200:
                data = response.json()
                if "content" in data and "method" in data and "anti_detection" in data:
                    self.log_test("Browser Proxy - Google", True, 
                                f"Browser proxy successful with anti-detection", 
                                {"url": data.get("url"), "method": data.get("method"), 
                                 "anti_detection": data.get("anti_detection")})
                    return True
                else:
                    self.log_test("Browser Proxy - Google", False, f"Unexpected response format: {data}")
            else:
                self.log_test("Browser Proxy - Google", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Browser Proxy", False, f"Exception: {str(e)}")
        return False
        
    def test_error_handling(self):
        """Test error handling scenarios"""
        try:
            # Test AI query without Groq key (if applicable)
            # Test browser command with missing parameters
            
            # Missing URL for open command
            response = self.session.post(f"{API_BASE}/browser/execute", json={
                "command": "open",
                "session_id": self.session_id
            })
            if response.status_code == 400:
                self.log_test("Error Handling - Missing URL", True, "400 returned for missing URL")
            else:
                self.log_test("Error Handling - Missing URL", False, f"Expected 400, got {response.status_code}")
                
            # Missing selector for click command
            response = self.session.post(f"{API_BASE}/browser/execute", json={
                "command": "click",
                "session_id": self.session_id
            })
            if response.status_code == 400:
                self.log_test("Error Handling - Missing Selector", True, "400 returned for missing selector")
            else:
                self.log_test("Error Handling - Missing Selector", False, f"Expected 400, got {response.status_code}")
                
            return True
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")
        return False
        
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Kairo AI Browser Backend Tests")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("AI Query Processing", self.test_ai_query),
            ("Browser Command Execution", self.test_browser_execute),
            ("Workflow Execution", self.test_workflow_execute),
            ("Session Management", self.test_sessions),
            ("Proxy Functionality", self.test_proxy),
            ("Error Handling", self.test_error_handling)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            if test_func():
                passed += 1
                
        print("\n" + "=" * 50)
        print(f"🏁 Test Summary: {passed}/{total} test suites passed")
        
        # Print detailed results
        print("\n📊 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
            
        return passed == total

if __name__ == "__main__":
    tester = KairoBackendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check the results above.")
        sys.exit(1)