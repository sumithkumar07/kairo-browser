#!/usr/bin/env python3
"""
Kairo AI Browser - Cleanup Script for Local-First Transition
Removes unnecessary components for Electron migration
"""

import os
import shutil
from pathlib import Path

def remove_file_if_exists(filepath):
    """Remove file if it exists"""
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"❌ Removed: {filepath}")
    else:
        print(f"⚠️  Not found: {filepath}")

def remove_dir_if_exists(dirpath):
    """Remove directory if it exists"""
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
        print(f"❌ Removed directory: {dirpath}")
    else:
        print(f"⚠️  Directory not found: {dirpath}")

def backup_file(filepath, backup_dir="/app/backup"):
    """Backup file before removal"""
    if os.path.exists(filepath):
        os.makedirs(backup_dir, exist_ok=True)
        filename = os.path.basename(filepath)
        backup_path = os.path.join(backup_dir, filename)
        shutil.copy2(filepath, backup_path)
        print(f"📦 Backed up: {filepath} → {backup_path}")

def main():
    print("🚀 Starting Kairo AI Browser cleanup for Local-First transition...")
    print()
    
    # Create backup directory
    backup_dir = "/app/backup"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Files to remove (with backup)
    files_to_remove = [
        # Complex Proxy Services (Not needed with native Chromium)
        "/app/backend/services/proxy_service.py",
        "/app/backend/services/enhanced_proxy_service.py",
        "/app/backend/services/advanced_browser_engine.py",
        "/app/backend/services/stealth_engine_service.py", 
        "/app/backend/services/bulletproof_fallback_system.py",
        "/app/backend/services/shadow_browser_service.py",
        "/app/backend/services/advanced_rendering_service.py",
        
        # Heavy Backend Services (Will be local)
        "/app/backend/services/ultimate_youtube_service.py",
        "/app/backend/services/real_interaction_engine.py",
        "/app/backend/services/enhanced_conversational_ai.py",
        
        # Database Layer (Local storage instead)
        "/app/backend/database/mongodb.py", 
        "/app/backend/database/enhanced_mongodb.py",
        
        # Multiple UI Layers (Keep only Ultimate)
        "/app/frontend/src/components/BrowserInterface.js",
        "/app/frontend/src/components/EnhancedBrowserInterface.js",
        
        # API Routes for removed services
        "/app/backend/api/enhanced_routes.py",
        "/app/backend/api/ultimate_enhanced_routes.py",
    ]
    
    print("📦 Creating backups...")
    for filepath in files_to_remove:
        backup_file(filepath, backup_dir)
    
    print()
    print("❌ Removing unnecessary files...")
    for filepath in files_to_remove:
        remove_file_if_exists(filepath)
    
    # Remove __pycache__ directories 
    print()
    print("🧹 Cleaning __pycache__ directories...")
    for root, dirs, files in os.walk("/app/backend"):
        for dirname in dirs[:]:
            if dirname == "__pycache__":
                remove_dir_if_exists(os.path.join(root, dirname))
                dirs.remove(dirname)
    
    print()
    print("✅ Cleanup completed!")
    print(f"📦 Backups saved in: {backup_dir}")
    print()
    print("🎯 Next Steps:")
    print("1. Review removed files in backup directory")
    print("2. Update imports in remaining files")
    print("3. Start Electron foundation setup")
    print("4. Test that essential components still work")

if __name__ == "__main__":
    main()