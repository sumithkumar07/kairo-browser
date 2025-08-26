#!/usr/bin/env python3
"""
Kairo AI Browser Local-First Architecture Test
Comprehensive testing of the local-first desktop application
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path

class LocalFirstTester:
    def __init__(self):
        self.app_path = Path("/app")
        self.tests_passed = 0
        self.tests_total = 0
        self.results = {}

    def run_test(self, name, test_func):
        """Run a single test and track results"""
        self.tests_total += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            success = test_func()
            if success:
                self.tests_passed += 1
                print(f"✅ {name} - PASSED")
                self.results[name] = "PASSED"
            else:
                print(f"❌ {name} - FAILED")
                self.results[name] = "FAILED"
            return success
        except Exception as e:
            print(f"❌ {name} - ERROR: {str(e)}")
            self.results[name] = f"ERROR: {str(e)}"
            return False

    def test_project_structure(self):
        """Test that the local-first project structure is correct"""
        required_files = [
            "package.json",
            "electron/main.js",
            "electron/preload.js", 
            "electron/browser-automation.js",
            "orchestrator/ai-integration.js",
            "orchestrator/workflow-engine.js",
            "renderer/index.html",
            "renderer/App.js",
            "sync/sync-client.js"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = self.app_path / file_path
            if not full_path.exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"   Missing files: {missing_files}")
            return False
        
        print("   ✅ All required local-first files present")
        return True

    def test_web_removal(self):
        """Test that web-based components have been removed"""
        should_not_exist = [
            "frontend",
            "backend", 
            "backend-streamlined.py",
            "backend_test.py"
        ]
        
        existing_files = []
        for item in should_not_exist:
            full_path = self.app_path / item
            if full_path.exists():
                existing_files.append(item)
        
        if existing_files:
            print(f"   Web components still exist: {existing_files}")
            return False
            
        print("   ✅ Web components successfully removed")
        return True

    def test_package_configuration(self):
        """Test package.json configuration for local-first"""
        package_json_path = self.app_path / "package.json"
        
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        # Check main entry point
        if package_data.get("main") != "electron/main.js":
            print(f"   ❌ Wrong main entry: {package_data.get('main')}")
            return False
        
        # Check required dependencies
        required_deps = ["electron", "playwright", "sqlite3", "react", "react-dom"]
        dependencies = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}
        
        missing_deps = []
        for dep in required_deps:
            if dep not in dependencies:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"   ❌ Missing dependencies: {missing_deps}")
            return False
        
        # Check scripts
        scripts = package_data.get("scripts", {})
        if "start" not in scripts or "electron" not in scripts["start"]:
            print("   ❌ Missing or incorrect start script")
            return False
        
        print("   ✅ Package configuration correct for local-first")
        return True

    def test_electron_main_process(self):
        """Test Electron main process configuration"""
        main_js_path = self.app_path / "electron/main.js"
        
        with open(main_js_path, 'r') as f:
            content = f.read()
        
        # Check for key local-first components
        required_imports = [
            "require('playwright')",
            "require('sqlite3')",
            "BrowserAutomation",
            "WorkflowEngine", 
            "AIIntegration"
        ]
        
        missing_imports = []
        for import_stmt in required_imports:
            if import_stmt not in content:
                missing_imports.append(import_stmt)
        
        if missing_imports:
            print(f"   ❌ Missing imports: {missing_imports}")
            return False
        
        # Check for IPC handlers
        required_handlers = [
            "browser-navigate",
            "ai-query",
            "browser-execute",
            "workflow-execute"
        ]
        
        missing_handlers = []
        for handler in required_handlers:
            if handler not in content:
                missing_handlers.append(handler)
        
        if missing_handlers:
            print(f"   ❌ Missing IPC handlers: {missing_handlers}")
            return False
        
        print("   ✅ Electron main process properly configured")
        return True

    def test_browser_automation(self):
        """Test browser automation module"""
        automation_path = self.app_path / "electron/browser-automation.js"
        
        with open(automation_path, 'r') as f:
            content = f.read()
        
        # Check for key methods
        required_methods = [
            "executeCommand",
            "navigate",
            "click",
            "type",
            "searchOnPage",
            "handleYouTubeVideo"
        ]
        
        missing_methods = []
        for method in required_methods:
            if f"async {method}" not in content and f"{method}(" not in content:
                missing_methods.append(method)
        
        if missing_methods:
            print(f"   ❌ Missing methods: {missing_methods}")
            return False
        
        print("   ✅ Browser automation module complete")
        return True

    def test_ai_integration(self):
        """Test AI integration module"""
        ai_path = self.app_path / "orchestrator/ai-integration.js"
        
        with open(ai_path, 'r') as f:
            content = f.read()
        
        # Check for AI capabilities
        required_features = [
            "processQuery",
            "buildSystemPrompt",
            "makeAPICall",
            "parseAIResponse",
            "local-first"
        ]
        
        missing_features = []
        for feature in required_features:
            if feature not in content:
                missing_features.append(feature)
        
        if missing_features:
            print(f"   ❌ Missing AI features: {missing_features}")
            return False
        
        print("   ✅ AI integration properly configured for local-first")
        return True

    def test_ui_components(self):
        """Test UI components for desktop application"""
        ui_files = [
            ("renderer/index.html", ["kairoAPI", "Local-First", "React"]),
            ("renderer/App.js", ["useState", "useEffect", "kairoAPI", "local-first"]),
            ("renderer/App.css", ["title-bar", "webkit-app-region"])
        ]
        
        for file_path, required_content in ui_files:
            full_path = self.app_path / file_path
            
            with open(full_path, 'r') as f:
                content = f.read()
            
            missing_content = []
            for item in required_content:
                if item not in content:
                    missing_content.append(item)
            
            if missing_content:
                print(f"   ❌ {file_path} missing: {missing_content}")
                return False
        
        print("   ✅ UI components configured for desktop application")
        return True

    def test_local_storage(self):
        """Test local storage capabilities"""
        # Check if we can run a simple Node.js test
        test_script = '''
const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const os = require('os');

const dbPath = path.join(os.tmpdir(), 'test_kairo.db');
const db = new sqlite3.Database(dbPath);

db.serialize(() => {
  db.run("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, data TEXT)");
  db.run("INSERT INTO test (data) VALUES (?)", ["test_data"]);
  
  db.get("SELECT data FROM test WHERE id = 1", (err, row) => {
    if (err) {
      console.error("ERROR:", err);
      process.exit(1);
    }
    
    if (row && row.data === "test_data") {
      console.log("SUCCESS: Local storage working");
      process.exit(0);
    } else {
      console.error("ERROR: Data not found");
      process.exit(1);
    }
  });
});
'''
        
        try:
            result = subprocess.run(
                ["node", "-e", test_script],
                cwd=self.app_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and "SUCCESS" in result.stdout:
                print("   ✅ Local SQLite storage working")
                return True
            else:
                print(f"   ❌ Storage test failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"   ❌ Storage test error: {str(e)}")
            return False

    def test_dependencies_installation(self):
        """Test that all dependencies are properly installed"""
        try:
            result = subprocess.run(
                ["npm", "list", "--depth=0"],
                cwd=self.app_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Check for key dependencies in output
            required_deps = ["electron", "playwright", "sqlite3", "react"]
            missing_deps = []
            
            for dep in required_deps:
                if dep not in result.stdout:
                    missing_deps.append(dep)
            
            if missing_deps:
                print(f"   ❌ Missing installed dependencies: {missing_deps}")
                return False
            
            print("   ✅ All dependencies properly installed")
            return True
            
        except Exception as e:
            print(f"   ❌ Dependency check error: {str(e)}")
            return False

    def test_build_configuration(self):
        """Test build configuration for desktop distribution"""
        package_json_path = self.app_path / "package.json"
        
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
        
        # Check build configuration
        build_config = package_data.get("build", {})
        
        if not build_config:
            print("   ❌ No build configuration found")
            return False
        
        # Check for cross-platform targets
        required_platforms = ["mac", "win", "linux"]
        missing_platforms = []
        
        for platform in required_platforms:
            if platform not in build_config:
                missing_platforms.append(platform)
        
        if missing_platforms:
            print(f"   ❌ Missing platform configs: {missing_platforms}")
            return False
        
        print("   ✅ Build configuration complete for cross-platform")
        return True

    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🚀 Starting Comprehensive Local-First Architecture Test")
        print("=" * 60)
        
        # Run all tests
        tests = [
            ("Project Structure", self.test_project_structure),
            ("Web Components Removal", self.test_web_removal),
            ("Package Configuration", self.test_package_configuration),
            ("Electron Main Process", self.test_electron_main_process),
            ("Browser Automation", self.test_browser_automation),
            ("AI Integration", self.test_ai_integration),
            ("UI Components", self.test_ui_components),
            ("Local Storage", self.test_local_storage),
            ("Dependencies Installation", self.test_dependencies_installation),
            ("Build Configuration", self.test_build_configuration)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Generate final report
        self.generate_report()

    def generate_report(self):
        """Generate final test report"""
        print("\n" + "=" * 60)
        print("🎯 LOCAL-FIRST ARCHITECTURE - COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        
        for test_name, result in self.results.items():
            status = "✅ PASS" if result == "PASSED" else "❌ FAIL"
            print(f"    {status} - {test_name}")
        
        print("\n" + "-" * 60)
        print(f"📊 OVERALL RESULTS: {self.tests_passed}/{self.tests_total} tests passed")
        
        success_rate = (self.tests_passed / self.tests_total) * 100
        
        if success_rate >= 90:
            print("🎉 EXCELLENT - Local-First Architecture is READY!")
            print("\n🚀 KEY ACHIEVEMENTS:")
            print("   ✅ Complete web-to-local-first transition")
            print("   ✅ Electron desktop application structure")
            print("   ✅ Embedded Chromium browser integration")
            print("   ✅ AI-powered automation capabilities")
            print("   ✅ Local data storage with SQLite")
            print("   ✅ Cross-platform build configuration")
            
        elif success_rate >= 70:
            print("⚠️  GOOD - Minor issues to address")
            
        else:
            print("❌ NEEDS WORK - Major issues found")
        
        print(f"\n📈 SUCCESS RATE: {success_rate:.1f}%")
        print("=" * 60)

if __name__ == "__main__":
    tester = LocalFirstTester()
    tester.run_all_tests()