#!/usr/bin/env python3
"""
Test script to detect default browser and test auto-detection feature
"""

import sys
import os
import asyncio
import subprocess

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.actions.applescript_browser import AppleScriptBrowserController


def detect_default_browser_manual():
    """Manually detect default browser using AppleScript"""
    print("🔍 Detecting your default browser...")
    
    try:
        # Get default browser using LaunchServices
        script = '''
        tell application "System Events"
            set defaultBrowser to get name of default application of (info for (POSIX file "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/public.html"))
        end tell
        return defaultBrowser
        '''
        
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            browser_name = result.stdout.strip()
            print(f"✅ System default browser: {browser_name}")
            return browser_name
        else:
            print(f"❌ Failed to detect: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error detecting browser: {e}")
        return None


async def test_browser_controllers():
    """Test different browser controllers"""
    print("\n🧪 Testing Browser Controllers")
    print("=" * 50)
    
    browsers_to_test = [
        ("auto", "Auto-detect default browser"),
        ("Safari", "Safari (Force)"),
        ("Google Chrome", "Chrome (Force)"),
        ("Arc", "Arc Browser (Force)"),
        ("Microsoft Edge", "Edge (Force)")
    ]
    
    for browser_name, description in browsers_to_test:
        print(f"\n📱 Testing {description}...")
        
        try:
            controller = AppleScriptBrowserController(browser_name)
            success = await controller.initialize()
            
            if success:
                print(f"   ✅ {controller.browser_app} - Initialized successfully!")
                await controller.cleanup()
            else:
                print(f"   ❌ {browser_name} - Failed to initialize")
                
        except Exception as e:
            print(f"   ❌ {browser_name} - Error: {e}")


async def test_url_opening():
    """Test opening URL with auto-detected browser"""
    print("\n🔗 Testing URL Opening with Auto-Detected Browser")
    print("=" * 50)
    
    try:
        # Use auto-detection
        controller = AppleScriptBrowserController("auto")
        success = await controller.initialize()
        
        if success:
            print(f"✅ Using detected browser: {controller.browser_app}")
            print("🔗 Opening example.com...")
            
            # Test opening a URL
            url_success = await controller.open_url("https://example.com", "example")
            
            if url_success:
                print("✅ URL opened successfully!")
            else:
                print("❌ Failed to open URL")
                
            await controller.cleanup()
        else:
            print("❌ Failed to initialize auto-detected browser")
            
    except Exception as e:
        print(f"❌ Auto-detection test failed: {e}")


async def main():
    """Main test function"""
    print("🌐 VoiceNav Default Browser Detection Test")
    print("=" * 60)
    
    # Test 1: Manual browser detection
    detect_default_browser_manual()
    
    # Test 2: Test different browser controllers
    await test_browser_controllers()
    
    # Test 3: Test URL opening with auto-detection
    await test_url_opening()
    
    print("\n🎉 Browser detection tests completed!")
    print("\nNow VoiceNav will automatically use your default browser!")
    print("🚀 Try: python3 src/main.py")


if __name__ == "__main__":
    asyncio.run(main())
