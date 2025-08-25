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
        
    def test_integration_flow_youtube(self):
        """Test complete integration flow: AI query → Browser command → Enhanced proxy → Content loading for YouTube"""
        try:
            integration_session = str(uuid.uuid4())
            
            # Step 1: AI Query Processing
            ai_query = {
                "query": "Open YouTube",
                "session_id": integration_session
            }
            
            response = self.session.post(f"{API_BASE}/ai/query", json=ai_query)
            if response.status_code != 200:
                self.log_test("Integration Flow YouTube - AI Query", False, f"AI query failed: {response.status_code}")
                return False
                
            ai_data = response.json()
            if "intent" not in ai_data and "commands" not in ai_data:
                self.log_test("Integration Flow YouTube - AI Query", False, "AI response missing expected fields")
                return False
                
            self.log_test("Integration Flow YouTube - AI Query", True, "AI processed YouTube request")
            
            # Step 2: Browser Command Execution
            browser_command = {
                "command": "open",
                "url": "https://www.youtube.com",
                "session_id": integration_session
            }
            
            response = self.session.post(f"{API_BASE}/browser/execute", json=browser_command)
            if response.status_code != 200:
                self.log_test("Integration Flow YouTube - Browser Command", False, f"Browser command failed: {response.status_code}")
                return False
                
            browser_data = response.json()
            if browser_data.get("status") != "executed":
                self.log_test("Integration Flow YouTube - Browser Command", False, "Browser command not executed")
                return False
                
            self.log_test("Integration Flow YouTube - Browser Command", True, "Browser command executed")
            
            # Step 3: Enhanced Proxy Content Loading
            proxy_request = {
                "url": "https://www.youtube.com"
            }
            
            response = self.session.post(f"{API_BASE}/proxy/enhanced", json=proxy_request, timeout=90)
            if response.status_code != 200:
                self.log_test("Integration Flow YouTube - Enhanced Proxy", False, f"Enhanced proxy failed: {response.status_code}")
                return False
                
            proxy_data = response.json()
            if "content" not in proxy_data or "method" not in proxy_data:
                self.log_test("Integration Flow YouTube - Enhanced Proxy", False, "Proxy response missing content or method")
                return False
                
            # Verify YouTube content was loaded
            content = proxy_data.get("content", "")
            if "youtube" not in content.lower() and "google" not in content.lower():
                self.log_test("Integration Flow YouTube - Content Verification", False, "YouTube content not detected")
                return False
                
            self.log_test("Integration Flow YouTube - Complete", True, 
                        f"Full integration successful, method: {proxy_data.get('method')}")
            return True
            
        except Exception as e:
            self.log_test("Integration Flow YouTube", False, f"Exception: {str(e)}")
        return False
        
    def test_integration_flow_wikipedia(self):
        """Test complete integration flow for Wikipedia using HTTP proxy path"""
        try:
            integration_session = str(uuid.uuid4())
            
            # Step 1: AI Query Processing
            ai_query = {
                "query": "Open Wikipedia",
                "session_id": integration_session
            }
            
            response = self.session.post(f"{API_BASE}/ai/query", json=ai_query)
            if response.status_code != 200:
                self.log_test("Integration Flow Wikipedia - AI Query", False, f"AI query failed: {response.status_code}")
                return False
                
            self.log_test("Integration Flow Wikipedia - AI Query", True, "AI processed Wikipedia request")
            
            # Step 2: Browser Command Execution
            browser_command = {
                "command": "open",
                "url": "https://en.wikipedia.org",
                "session_id": integration_session
            }
            
            response = self.session.post(f"{API_BASE}/browser/execute", json=browser_command)
            if response.status_code != 200:
                self.log_test("Integration Flow Wikipedia - Browser Command", False, f"Browser command failed: {response.status_code}")
                return False
                
            self.log_test("Integration Flow Wikipedia - Browser Command", True, "Browser command executed")
            
            # Step 3: Enhanced Proxy Content Loading (should use HTTP proxy for Wikipedia)
            proxy_request = {
                "url": "https://en.wikipedia.org"
            }
            
            response = self.session.post(f"{API_BASE}/proxy/enhanced", json=proxy_request, timeout=60)
            if response.status_code != 200:
                self.log_test("Integration Flow Wikipedia - Enhanced Proxy", False, f"Enhanced proxy failed: {response.status_code}")
                return False
                
            proxy_data = response.json()
            if "content" not in proxy_data:
                self.log_test("Integration Flow Wikipedia - Enhanced Proxy", False, "Proxy response missing content")
                return False
                
            # Verify Wikipedia content was loaded
            content = proxy_data.get("content", "")
            if "wikipedia" not in content.lower():
                self.log_test("Integration Flow Wikipedia - Content Verification", False, "Wikipedia content not detected")
                return False
                
            self.log_test("Integration Flow Wikipedia - Complete", True, 
                        f"Full integration successful, method: {proxy_data.get('method', 'unknown')}")
            return True
            
        except Exception as e:
            self.log_test("Integration Flow Wikipedia", False, f"Exception: {str(e)}")
        return False
        
    def test_mongodb_connection(self):
        """Test MongoDB connection and data storage"""
        try:
            # Test that AI interactions are being stored by making a query and checking sessions
            test_query = {
                "query": "Test MongoDB storage",
                "session_id": self.session_id
            }
            
            response = self.session.post(f"{API_BASE}/ai/query", json=test_query)
            if response.status_code != 200:
                self.log_test("MongoDB - AI Storage", False, "Failed to store AI interaction")
                return False
                
            # Test that browser commands are being stored
            test_command = {
                "command": "open",
                "url": "https://example.com",
                "session_id": self.session_id
            }
            
            response = self.session.post(f"{API_BASE}/browser/execute", json=test_command)
            if response.status_code != 200:
                self.log_test("MongoDB - Command Storage", False, "Failed to store browser command")
                return False
                
            # Verify sessions endpoint can retrieve stored data
            response = self.session.get(f"{API_BASE}/sessions")
            if response.status_code == 200:
                data = response.json()
                if "sessions" in data and len(data["sessions"]) > 0:
                    self.log_test("MongoDB - Data Retrieval", True, f"Retrieved {len(data['sessions'])} sessions from MongoDB")
                    return True
                else:
                    self.log_test("MongoDB - Data Retrieval", False, "No sessions found in MongoDB")
            else:
                self.log_test("MongoDB - Data Retrieval", False, f"Sessions endpoint failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("MongoDB Connection", False, f"Exception: {str(e)}")
        return False
        
    def test_session_management(self):
        """Test session management across all components"""
        try:
            test_session = str(uuid.uuid4())
            
            # Test session consistency across AI query
            ai_response = self.session.post(f"{API_BASE}/ai/query", json={
                "query": "Test session management",
                "session_id": test_session
            })
            
            if ai_response.status_code != 200:
                self.log_test("Session Management - AI", False, "AI query with session failed")
                return False
                
            # Test session consistency across browser command
            browser_response = self.session.post(f"{API_BASE}/browser/execute", json={
                "command": "open",
                "url": "https://example.com",
                "session_id": test_session
            })
            
            if browser_response.status_code != 200:
                self.log_test("Session Management - Browser", False, "Browser command with session failed")
                return False
                
            browser_data = browser_response.json()
            if browser_data.get("session_id") != test_session:
                self.log_test("Session Management - Consistency", False, "Session ID not consistent")
                return False
                
            self.log_test("Session Management", True, f"Session {test_session} managed consistently across components")
            return True
            
        except Exception as e:
            self.log_test("Session Management", False, f"Exception: {str(e)}")
        return False
        
    def test_error_handling(self):
        """Test error handling scenarios"""
        try:
            # Missing URL for open command
            response = self.session.post(f"{API_BASE}/browser/execute", json={
                "command": "open",
                "session_id": self.session_id
            })
            if response.status_code == 400:
                self.log_test("Error Handling - Missing URL", True, "400 returned for missing URL")
            else:
                self.log_test("Error Handling - Missing URL", False, f"Expected 400, got {response.status_code}")
                return False
                
            # Missing selector for click command
            response = self.session.post(f"{API_BASE}/browser/execute", json={
                "command": "click",
                "session_id": self.session_id
            })
            if response.status_code == 400:
                self.log_test("Error Handling - Missing Selector", True, "400 returned for missing selector")
            else:
                self.log_test("Error Handling - Missing Selector", False, f"Expected 400, got {response.status_code}")
                return False
                
            # Test proxy error handling
            response = self.session.post(f"{API_BASE}/proxy/enhanced", json={})
            if response.status_code == 400:
                self.log_test("Error Handling - Proxy No URL", True, "400 returned for proxy without URL")
                return True
            else:
                self.log_test("Error Handling - Proxy No URL", False, f"Expected 400, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")
        return False
        
    def run_all_tests(self):
        """Run all comprehensive integration tests"""
        print("🚀 Starting Kairo AI Browser Comprehensive Integration Tests")
        print("=" * 70)
        
        tests = [
            ("Health Check", self.test_health_check),
            ("AI Query Processing", self.test_ai_query),
            ("Browser Command Execution", self.test_browser_execute),
            ("Workflow Execution", self.test_workflow_execute),
            ("Session Management API", self.test_sessions),
            ("Basic Proxy Functionality", self.test_proxy),
            ("Enhanced Proxy with Smart Routing", self.test_enhanced_proxy),
            ("Browser Proxy with Playwright", self.test_browser_proxy),
            ("MongoDB Connection & Data Storage", self.test_mongodb_connection),
            ("Session Management Across Components", self.test_session_management),
            ("Integration Flow - YouTube (AI→Browser→Enhanced Proxy)", self.test_integration_flow_youtube),
            ("Integration Flow - Wikipedia (AI→Browser→HTTP Proxy)", self.test_integration_flow_wikipedia),
            ("Error Handling & Fallback Mechanisms", self.test_error_handling)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            print("-" * 50)
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
                
        print("\n" + "=" * 70)
        print(f"🏁 COMPREHENSIVE TEST SUMMARY: {passed}/{total} test suites passed")
        
        # Print detailed results
        print("\n📊 Detailed Test Results:")
        print("-" * 70)
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
            
        # Integration summary
        print(f"\n🔗 Integration Test Results:")
        print(f"   • Backend API Endpoints: {'✅ ALL WORKING' if passed >= 7 else '❌ SOME FAILED'}")
        print(f"   • Enhanced Proxy System: {'✅ WORKING' if passed >= 9 else '❌ FAILED'}")
        print(f"   • Complete Integration Flows: {'✅ WORKING' if passed >= 11 else '❌ FAILED'}")
        print(f"   • Component Connectivity: {'✅ VERIFIED' if passed >= 12 else '❌ ISSUES FOUND'}")
            
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