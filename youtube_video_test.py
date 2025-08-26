#!/usr/bin/env python3
"""
🎯 YOUTUBE VIDEO INTEGRATION TEST - DECEMBER 25, 2025
Testing the complete integration flow for YouTube video access with specific request:
"play this video in youtube yeh raatein yeh mausam"

This test verifies:
1. AI query processing for YouTube video requests
2. Whether the AI can generate youtube_video commands as mentioned in the system prompt
3. If the browser can actually access YouTube and search for videos
4. Complete integration chain: AI processing → Browser commands → YouTube access → Video display
"""
import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, Any

class YouTubeVideoIntegrationTester:
    def __init__(self, base_url="https://youtube-test.preview.emergentagent.com"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session_id = f"youtube_test_{int(time.time())}"
        self.test_query = "play this video in youtube yeh raatein yeh mausam"
        
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
    
    def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, timeout: int = 60) -> tuple:
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
            return False, {"error": "Connection error"}
        except Exception as e:
            return False, {"error": str(e)}

    def test_ai_youtube_video_processing(self):
        """Test AI processing of YouTube video request"""
        print(f"\n🤖 Testing AI Processing of YouTube Video Request...")
        print(f"   Query: '{self.test_query}'")
        
        # Test AI query processing for YouTube video request
        ai_query = {
            "query": self.test_query,
            "context": {
                "page_url": "https://www.youtube.com",
                "user_intent": "video_search_and_play"
            },
            "session_id": self.session_id
        }
        
        success, response = self.make_request('POST', '/ai/query', ai_query)
        
        if success:
            print(f"   ✅ AI Response received successfully")
            print(f"   📝 Response keys: {list(response.keys())}")
            
            # Check if AI generated commands
            if 'commands' in response:
                commands = response['commands']
                print(f"   🎯 Commands generated: {len(commands)}")
                
                # Look for youtube_video command type
                youtube_video_commands = [cmd for cmd in commands if cmd.get('type') == 'youtube_video']
                if youtube_video_commands:
                    print(f"   🎬 YouTube video commands found: {len(youtube_video_commands)}")
                    for cmd in youtube_video_commands:
                        print(f"      - Command: {cmd}")
                    self.log_test("AI Generated YouTube Video Commands", True, f"Found {len(youtube_video_commands)} youtube_video commands")
                else:
                    # Check for other video-related commands
                    video_related = [cmd for cmd in commands if 'video' in str(cmd).lower() or 'youtube' in str(cmd).lower()]
                    if video_related:
                        print(f"   📺 Video-related commands found: {len(video_related)}")
                        for cmd in video_related:
                            print(f"      - Command: {cmd}")
                        self.log_test("AI Generated Video-Related Commands", True, f"Found {len(video_related)} video-related commands")
                    else:
                        self.log_test("AI Generated YouTube Video Commands", False, "No youtube_video or video-related commands found")
            else:
                self.log_test("AI Command Generation", False, "No commands field in response")
            
            # Check AI intent recognition
            if 'intent' in response:
                intent = response['intent']
                print(f"   🎯 AI Intent: {intent}")
                video_intent = 'video' in intent.lower() or 'youtube' in intent.lower() or 'play' in intent.lower()
                self.log_test("AI Video Intent Recognition", video_intent, f"Intent: {intent}")
            
            # Check AI explanation
            if 'explanation' in response:
                explanation = response['explanation']
                print(f"   💬 AI Explanation: {explanation[:200]}...")
                self.log_test("AI Explanation Generated", True, "")
            
        else:
            self.log_test("AI YouTube Video Processing", success, str(response.get('error', '')))
        
        return success, response

    def test_browser_youtube_access(self):
        """Test browser access to YouTube"""
        print(f"\n🌐 Testing Browser Access to YouTube...")
        
        # Test browser navigation to YouTube
        browser_command = {
            "command": "navigate",
            "url": "https://www.youtube.com",
            "session_id": self.session_id
        }
        
        success, response = self.make_request('POST', '/browser/execute', browser_command)
        self.log_test("Browser YouTube Navigation", success, str(response.get('error', '')) if not success else "")
        
        if success:
            print(f"   ✅ Browser successfully navigated to YouTube")
            print(f"   📝 Response: {response}")
        
        return success, response

    def test_youtube_proxy_access(self):
        """Test proxy system access to YouTube"""
        print(f"\n🔄 Testing Proxy System YouTube Access...")
        
        # Test enhanced proxy access to YouTube
        proxy_request = {
            "url": "https://www.youtube.com",
            "method": "GET",
            "session_id": self.session_id,
            "enhance_rendering": True,
            "stealth_level": 5
        }
        
        success, response = self.make_request('POST', '/proxy/enhanced', proxy_request, timeout=90)
        
        if success:
            print(f"   ✅ Enhanced proxy successfully accessed YouTube")
            
            # Check if we got actual YouTube content
            if 'content' in response:
                content = response['content']
                content_length = len(content)
                print(f"   📊 Content length: {content_length} characters")
                
                # Look for YouTube-specific content
                youtube_indicators = ['youtube', 'ytimg', 'google', 'video']
                found_indicators = [indicator for indicator in youtube_indicators if indicator.lower() in content.lower()]
                
                if found_indicators:
                    print(f"   🎬 YouTube content indicators found: {found_indicators}")
                    self.log_test("YouTube Content Verification", True, f"Found indicators: {found_indicators}")
                else:
                    self.log_test("YouTube Content Verification", False, "No YouTube content indicators found")
                
                # Check for video-related elements
                video_elements = ['<video', 'player', 'watch?v=', '/embed/']
                found_video_elements = [elem for elem in video_elements if elem in content.lower()]
                
                if found_video_elements:
                    print(f"   📺 Video elements found: {found_video_elements}")
                    self.log_test("Video Elements Detection", True, f"Found elements: {found_video_elements}")
                else:
                    print(f"   ⚠️  No video elements detected in content")
                    self.log_test("Video Elements Detection", False, "No video elements found")
            
            # Check proxy method used
            if 'method' in response:
                method = response['method']
                print(f"   🔧 Proxy method used: {method}")
                self.log_test("Proxy Method Selection", True, f"Method: {method}")
        else:
            self.log_test("Enhanced Proxy YouTube Access", success, str(response.get('error', '')))
        
        return success, response

    def test_youtube_video_search_simulation(self):
        """Test YouTube video search simulation"""
        print(f"\n🔍 Testing YouTube Video Search Simulation...")
        
        # Simulate a search for the specific video
        search_query = "yeh raatein yeh mausam"
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        
        print(f"   🎯 Search URL: {search_url}")
        
        # Test proxy access to search results
        search_request = {
            "url": search_url,
            "method": "GET",
            "session_id": self.session_id,
            "enhance_rendering": True,
            "stealth_level": 5
        }
        
        success, response = self.make_request('POST', '/proxy/enhanced', search_request, timeout=90)
        
        if success:
            print(f"   ✅ Successfully accessed YouTube search results")
            
            if 'content' in response:
                content = response['content']
                content_length = len(content)
                print(f"   📊 Search results content length: {content_length} characters")
                
                # Look for search result indicators
                search_indicators = ['search_query', 'results', 'video-title', 'ytd-video-renderer']
                found_search_indicators = [indicator for indicator in search_indicators if indicator in content.lower()]
                
                if found_search_indicators:
                    print(f"   🔍 Search result indicators found: {found_search_indicators}")
                    self.log_test("YouTube Search Results Access", True, f"Found indicators: {found_search_indicators}")
                else:
                    self.log_test("YouTube Search Results Access", False, "No search result indicators found")
                
                # Look for the specific song/video
                song_keywords = ['yeh raatein', 'yeh mausam', 'raatein', 'mausam']
                found_keywords = [keyword for keyword in song_keywords if keyword.lower() in content.lower()]
                
                if found_keywords:
                    print(f"   🎵 Song keywords found in results: {found_keywords}")
                    self.log_test("Specific Video Search Results", True, f"Found keywords: {found_keywords}")
                else:
                    print(f"   ⚠️  Specific song keywords not found in results")
                    self.log_test("Specific Video Search Results", False, "Song keywords not found")
        else:
            self.log_test("YouTube Video Search Access", success, str(response.get('error', '')))
        
        return success, response

    def test_complete_integration_flow(self):
        """Test complete integration flow for YouTube video request"""
        print(f"\n🔗 Testing Complete Integration Flow...")
        print(f"   Flow: AI Processing → Browser Commands → YouTube Access → Video Display")
        
        integration_success = True
        flow_details = []
        
        # Step 1: AI Processing
        print(f"\n   Step 1: AI Processing...")
        ai_success, ai_response = self.test_ai_youtube_video_processing()
        if ai_success:
            flow_details.append("✅ AI Processing: SUCCESS")
        else:
            flow_details.append("❌ AI Processing: FAILED")
            integration_success = False
        
        # Step 2: Browser Commands
        print(f"\n   Step 2: Browser Commands...")
        browser_success, browser_response = self.test_browser_youtube_access()
        if browser_success:
            flow_details.append("✅ Browser Commands: SUCCESS")
        else:
            flow_details.append("❌ Browser Commands: FAILED")
            integration_success = False
        
        # Step 3: YouTube Access
        print(f"\n   Step 3: YouTube Access...")
        proxy_success, proxy_response = self.test_youtube_proxy_access()
        if proxy_success:
            flow_details.append("✅ YouTube Access: SUCCESS")
        else:
            flow_details.append("❌ YouTube Access: FAILED")
            integration_success = False
        
        # Step 4: Video Search
        print(f"\n   Step 4: Video Search...")
        search_success, search_response = self.test_youtube_video_search_simulation()
        if search_success:
            flow_details.append("✅ Video Search: SUCCESS")
        else:
            flow_details.append("❌ Video Search: FAILED")
            integration_success = False
        
        # Integration flow summary
        print(f"\n   🔗 Integration Flow Summary:")
        for detail in flow_details:
            print(f"      {detail}")
        
        self.log_test("Complete Integration Flow", integration_success, 
                     "All steps completed successfully" if integration_success else "Some steps failed")
        
        return integration_success

    def test_youtube_video_command_bypass(self):
        """Test if the system can bypass YouTube restrictions as mentioned in system prompt"""
        print(f"\n🚫 Testing YouTube Restriction Bypass...")
        
        # Test if the system can handle YouTube's restrictions
        bypass_request = {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Test video URL
            "method": "GET",
            "session_id": self.session_id,
            "enhance_rendering": True,
            "stealth_level": 5,
            "bypass_restrictions": True
        }
        
        success, response = self.make_request('POST', '/ultimate/proxy', bypass_request, timeout=120)
        
        if success:
            print(f"   ✅ Ultimate proxy accessed YouTube video page")
            
            if 'content' in response:
                content = response['content']
                content_length = len(content)
                print(f"   📊 Video page content length: {content_length} characters")
                
                # Look for video player elements
                video_indicators = ['player', 'video', 'ytplayer', 'watch-video']
                found_video_indicators = [indicator for indicator in video_indicators if indicator in content.lower()]
                
                if found_video_indicators:
                    print(f"   🎬 Video player indicators found: {found_video_indicators}")
                    self.log_test("YouTube Video Page Access", True, f"Found indicators: {found_video_indicators}")
                else:
                    self.log_test("YouTube Video Page Access", False, "No video player indicators found")
                
                # Check if restrictions were bypassed
                restriction_indicators = ['restricted', 'blocked', 'unavailable', 'error']
                found_restrictions = [indicator for indicator in restriction_indicators if indicator in content.lower()]
                
                if found_restrictions:
                    print(f"   ⚠️  Restriction indicators found: {found_restrictions}")
                    self.log_test("YouTube Restriction Bypass", False, f"Restrictions detected: {found_restrictions}")
                else:
                    print(f"   ✅ No restriction indicators found - bypass successful")
                    self.log_test("YouTube Restriction Bypass", True, "No restrictions detected")
        else:
            self.log_test("YouTube Video Page Access", success, str(response.get('error', '')))
        
        return success, response

    def run_youtube_video_tests(self):
        """Run all YouTube video integration tests"""
        print("🎯 YOUTUBE VIDEO INTEGRATION TEST - DECEMBER 25, 2025")
        print(f"🎬 Testing query: '{self.test_query}'")
        print(f"🔧 Testing against: {self.base_url}")
        print(f"🆔 Session ID: {self.session_id}")
        print("=" * 80)
        
        start_time = time.time()
        
        # Run all YouTube video tests
        print(f"\n🎬 TESTING YOUTUBE VIDEO FUNCTIONALITY...")
        
        # Test 1: AI Processing
        self.test_ai_youtube_video_processing()
        
        # Test 2: Browser Access
        self.test_browser_youtube_access()
        
        # Test 3: Proxy Access
        self.test_youtube_proxy_access()
        
        # Test 4: Video Search
        self.test_youtube_video_search_simulation()
        
        # Test 5: Restriction Bypass
        self.test_youtube_video_command_bypass()
        
        # Test 6: Complete Integration Flow
        self.test_complete_integration_flow()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Print comprehensive summary
        print("\n" + "=" * 80)
        print("📊 YOUTUBE VIDEO INTEGRATION TEST SUMMARY")
        print("=" * 80)
        print(f"🎬 Test Query: '{self.test_query}'")
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        print(f"✅ Tests Passed: {self.tests_passed}/{self.tests_run}")
        print(f"❌ Tests Failed: {len(self.failed_tests)}/{self.tests_run}")
        
        if self.failed_tests:
            print("\n🚨 FAILED TESTS:")
            for i, failure in enumerate(self.failed_tests, 1):
                print(f"   {i}. {failure}")
        
        success_rate = (self.tests_passed / self.tests_run) * 100 if self.tests_run > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        # YouTube video functionality assessment
        print(f"\n🎬 YOUTUBE VIDEO FUNCTIONALITY ASSESSMENT:")
        if success_rate >= 90:
            print("🎉 Status: EXCELLENT - YouTube video functionality fully operational")
            print("   ✅ AI can process YouTube video requests")
            print("   ✅ Browser can access YouTube successfully")
            print("   ✅ Proxy system can bypass restrictions")
            print("   ✅ Complete integration chain working")
        elif success_rate >= 70:
            print("✅ Status: GOOD - YouTube video functionality mostly working")
            print("   ✅ Core functionality operational")
            print("   ⚠️  Some minor issues detected")
        elif success_rate >= 50:
            print("⚠️  Status: MODERATE - YouTube video functionality partially working")
            print("   ⚠️  Some components working, others need attention")
        else:
            print("🚨 Status: POOR - YouTube video functionality needs major fixes")
            print("   ❌ Multiple critical issues detected")
        
        # Specific findings
        print(f"\n🔍 SPECIFIC FINDINGS:")
        ai_working = not any('AI' in failure for failure in self.failed_tests)
        browser_working = not any('Browser' in failure for failure in self.failed_tests)
        proxy_working = not any('Proxy' in failure for failure in self.failed_tests)
        
        print(f"   🤖 AI Processing: {'✅ Working' if ai_working else '❌ Issues detected'}")
        print(f"   🌐 Browser Access: {'✅ Working' if browser_working else '❌ Issues detected'}")
        print(f"   🔄 Proxy System: {'✅ Working' if proxy_working else '❌ Issues detected'}")
        print(f"   🎬 Video Functionality: {'✅ Working' if success_rate >= 70 else '❌ Issues detected'}")
        
        return success_rate >= 70

def main():
    """Main test execution"""
    tester = YouTubeVideoIntegrationTester()
    success = tester.run_youtube_video_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())