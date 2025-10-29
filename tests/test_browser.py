#!/usr/bin/env python3
"""
Test Script for VoiceNav Browser Control
Tests browser automation functionality
"""

import sys
import os
import asyncio

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from actions.browser_control import BrowserController


async def test_browser_initialization():
    """Test browser initialization"""
    print("🌐 Testing Browser Initialization")
    print("-" * 40)
    
    controller = BrowserController()
    
    try:
        print("Initializing browser...")
        success = await controller.initialize()
        
        if success:
            print("✅ Browser initialized successfully!")
            print(f"   Browser ready: {controller.is_initialized}")
            print(f"   Page available: {controller.page is not None}")
            
            # Test page properties
            if controller.page:
                viewport = await controller.page.viewport_size()
                print(f"   Viewport: {viewport['width']}x{viewport['height']}")
            
            return controller
        else:
            print("❌ Browser initialization failed")
            return None
            
    except Exception as e:
        print(f"❌ Browser initialization error: {e}")
        return None


async def test_navigation(controller):
    """Test URL navigation"""
    print("\n🔗 Testing Navigation")
    print("-" * 40)
    
    if not controller:
        print("❌ No browser controller available")
        return False
    
    # Test URLs
    test_urls = [
        ("https://example.com", "example"),
        ("https://httpbin.org/html", "httpbin"),
    ]
    
    passed = 0
    
    for url, name in test_urls:
        try:
            print(f"Navigating to {name}...")
            success = await controller.open_url(url, name)
            
            if success:
                print(f"✅ Successfully opened {name}")
                
                # Check if page loaded
                if controller.page:
                    title = await controller.page.title()
                    print(f"   Page title: {title}")
                    
                    current_url = controller.page.url
                    print(f"   Current URL: {current_url}")
                
                passed += 1
                
                # Wait a bit between tests
                await asyncio.sleep(2)
            else:
                print(f"❌ Failed to open {name}")
                
        except Exception as e:
            print(f"❌ Navigation error for {name}: {e}")
    
    print(f"\n📊 Navigation: {passed}/{len(test_urls)} tests passed")
    return passed == len(test_urls)


async def test_scrolling(controller):
    """Test page scrolling"""
    print("\n📜 Testing Scrolling")
    print("-" * 40)
    
    if not controller or not controller.page:
        print("❌ No browser page available")
        return False
    
    try:
        # Ensure we're on a page with content
        await controller.open_url("https://example.com", "example")
        await asyncio.sleep(1)
        
        # Test scroll down
        print("Testing scroll down...")
        success_down = await controller.scroll_page('down', 200)
        
        if success_down:
            print("✅ Scroll down successful")
        else:
            print("❌ Scroll down failed")
        
        await asyncio.sleep(1)
        
        # Test scroll up
        print("Testing scroll up...")
        success_up = await controller.scroll_page('up', 200)
        
        if success_up:
            print("✅ Scroll up successful")
        else:
            print("❌ Scroll up failed")
        
        print(f"\n📊 Scrolling: {2 if success_down and success_up else 1 if success_down or success_up else 0}/2 tests passed")
        return success_down and success_up
        
    except Exception as e:
        print(f"❌ Scrolling error: {e}")
        return False


async def test_content_reading(controller):
    """Test content reading"""
    print("\n📖 Testing Content Reading")
    print("-" * 40)
    
    if not controller or not controller.page:
        print("❌ No browser page available")
        return False
    
    try:
        # Navigate to a page with content
        await controller.open_url("https://example.com", "example")
        await asyncio.sleep(2)
        
        print("Testing content reading...")
        success = await controller.read_content('main')
        
        if success:
            print("✅ Content reading successful")
            print("   (Check if Maya spoke the content)")
        else:
            print("❌ Content reading failed")
        
        print(f"\n📊 Content Reading: {1 if success else 0}/1 tests passed")
        return success
        
    except Exception as e:
        print(f"❌ Content reading error: {e}")
        return False


async def test_navigation_controls(controller):
    """Test back/forward navigation"""
    print("\n⬅️➡️ Testing Navigation Controls")
    print("-" * 40)
    
    if not controller or not controller.page:
        print("❌ No browser page available")
        return False
    
    try:
        # Navigate to first page
        await controller.open_url("https://example.com", "example")
        await asyncio.sleep(1)
        
        # Navigate to second page
        await controller.open_url("https://httpbin.org/html", "httpbin")
        await asyncio.sleep(1)
        
        # Test go back
        print("Testing go back...")
        success_back = await controller.go_back()
        
        if success_back:
            print("✅ Go back successful")
            if controller.page:
                current_url = controller.page.url
                print(f"   Current URL: {current_url}")
        else:
            print("❌ Go back failed")
        
        await asyncio.sleep(1)
        
        # Test go forward
        print("Testing go forward...")
        success_forward = await controller.go_forward()
        
        if success_forward:
            print("✅ Go forward successful") 
            if controller.page:
                current_url = controller.page.url
                print(f"   Current URL: {current_url}")
        else:
            print("❌ Go forward failed")
        
        passed = sum([success_back, success_forward])
        print(f"\n📊 Navigation Controls: {passed}/2 tests passed")
        return passed == 2
        
    except Exception as e:
        print(f"❌ Navigation controls error: {e}")
        return False


async def test_command_execution(controller):
    """Test complete command execution"""
    print("\n🎯 Testing Command Execution")
    print("-" * 40)
    
    if not controller:
        print("❌ No browser controller available")
        return False
    
    # Test commands
    test_commands = [
        {
            'intent': 'open_url',
            'params': {'url': 'https://example.com', 'original_input': 'example'}
        },
        {
            'intent': 'scroll_down',
            'params': {'direction': 'down', 'amount': 200}
        },
        {
            'intent': 'scroll_up', 
            'params': {'direction': 'up', 'amount': 200}
        },
        {
            'intent': 'help',
            'params': {}
        },
        {
            'intent': 'stop_action',
            'params': {}
        }
    ]
    
    passed = 0
    
    for i, command in enumerate(test_commands, 1):
        try:
            intent = command['intent']
            print(f"Executing command {i}: {intent}")
            
            success = await controller.execute_command(command)
            
            if success:
                print(f"✅ Command {intent} executed successfully")
                passed += 1
            else:
                print(f"❌ Command {intent} failed")
            
            # Wait between commands
            if i < len(test_commands):
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"❌ Command execution error for {intent}: {e}")
    
    print(f"\n📊 Command Execution: {passed}/{len(test_commands)} tests passed")
    return passed == len(test_commands)


async def run_all_tests():
    """Run all browser tests"""
    print("🧪 VoiceNav Browser Control - Comprehensive Test Suite")
    print("=" * 60)
    
    controller = None
    
    try:
        # Test 1: Initialization
        controller = await test_browser_initialization()
        if not controller:
            print("\n❌ Cannot proceed without browser controller")
            return False
        
        # Test 2: Navigation
        nav_passed = await test_navigation(controller)
        
        # Test 3: Scrolling
        scroll_passed = await test_scrolling(controller)
        
        # Test 4: Content Reading
        content_passed = await test_content_reading(controller)
        
        # Test 5: Navigation Controls
        controls_passed = await test_navigation_controls(controller)
        
        # Test 6: Command Execution
        commands_passed = await test_command_execution(controller)
        
        # Results summary
        tests = [
            ("Browser Initialization", True),  # Always true if we get here
            ("URL Navigation", nav_passed),
            ("Page Scrolling", scroll_passed),
            ("Content Reading", content_passed),
            ("Navigation Controls", controls_passed),
            ("Command Execution", commands_passed)
        ]
        
        passed_count = sum(1 for _, passed in tests if passed)
        total_count = len(tests)
        
        print("\n" + "=" * 60)
        print("🏁 FINAL RESULTS:")
        for test_name, passed in tests:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test_name}: {status}")
        
        print(f"\n📊 Overall: {passed_count}/{total_count} tests passed ({passed_count/total_count*100:.1f}%)")
        
        if passed_count == total_count:
            print("\n🎉 ALL BROWSER TESTS PASSED!")
            print("✅ Browser control is ready for Maya integration!")
            return True
        else:
            print(f"\n⚠️  {total_count - passed_count} tests failed.")
            print("Browser control needs fixes before Maya integration.")
            return False
            
    except Exception as e:
        print(f"❌ Test suite error: {e}")
        return False
    
    finally:
        # Cleanup
        if controller:
            print("\n🧹 Cleaning up browser...")
            await controller.cleanup()
            print("✅ Cleanup complete")


def main():
    """Run browser tests"""
    try:
        success = asyncio.run(run_all_tests())
        return success
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Test runner error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 SUCCESS' if success else '❌ FAILURE'}")
    sys.exit(0 if success else 1)
