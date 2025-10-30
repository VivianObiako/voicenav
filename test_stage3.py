#!/usr/bin/env python3
"""
Stage 3 Testing Guide - Menu Bar UI & Complete Application
Comprehensive validation of VoiceNav Stage 3 implementation
"""

import sys
import os
import subprocess
import threading
import time
from datetime import datetime

# Add src directory to path
sys.path.append('src')

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print section header"""
    print(f"\n{'─'*40}")
    print(f"📋 {title}")
    print(f"{'─'*40}")

def test_ui_imports():
    """Test UI module imports"""
    print_section("Testing UI Module Imports")
    
    try:
        # Test menu bar import
        print("🔄 Testing menu bar import...")
        from src.ui.menu_bar import VoiceNavMenuBar
        print("✅ Menu bar module imported successfully")
        
        # Test settings panel import
        print("🔄 Testing settings panel import...")
        from src.ui.settings_panel import VoiceNavSettingsPanel
        print("✅ Settings panel module imported successfully")
        
        # Test UI package import
        print("🔄 Testing UI package import...")
        from src.ui import VoiceNavMenuBar as MenuBarFromPackage
        print("✅ UI package imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure rumps is installed: pip install rumps")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_dependencies():
    """Test Stage 3 dependencies"""
    print_section("Testing Stage 3 Dependencies")
    
    required_packages = [
        ('rumps', 'Menu bar functionality'),
        ('yaml', 'Settings configuration'),
        ('tkinter', 'Settings panel GUI')
    ]
    
    all_good = True
    
    for package, purpose in required_packages:
        try:
            print(f"🔄 Testing {package}...")
            if package == 'tkinter':
                import tkinter
            elif package == 'yaml':
                import yaml
            elif package == 'rumps':
                import rumps
            
            print(f"✅ {package} available - {purpose}")
            
        except ImportError:
            print(f"❌ {package} not available - {purpose}")
            if package == 'rumps':
                print("💡 Install with: pip install rumps")
            elif package == 'yaml':
                print("💡 Install with: pip install PyYAML")
            elif package == 'tkinter':
                print("💡 tkinter should be included with Python")
            all_good = False
    
    return all_good

def test_config_updates():
    """Test updated configuration"""
    print_section("Testing Updated Configuration")
    
    try:
        import yaml
        
        # Load config
        print("🔄 Loading config.yaml...")
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Check UI section
        if 'ui' in config:
            ui_config = config['ui']
            print("✅ UI configuration section found")
            
            expected_keys = ['show_notifications', 'auto_start', 'minimize_to_tray', 'icon_style']
            for key in expected_keys:
                if key in ui_config:
                    print(f"  ✅ {key}: {ui_config[key]}")
                else:
                    print(f"  ❌ Missing UI setting: {key}")
        else:
            print("❌ UI configuration section not found")
            return False
        
        # Check updated TTS settings
        if 'tts' in config:
            tts_config = config['tts']
            if tts_config.get('engine') == 'macos_say':
                print("✅ TTS engine updated to macos_say")
            if tts_config.get('voice') == 'Samantha':
                print("✅ Maya voice set to Samantha")
        
        # Check browser method
        if 'browser' in config:
            browser_config = config['browser']
            if browser_config.get('method') == 'applescript':
                print("✅ Browser method set to AppleScript")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_main_arguments():
    """Test main.py command-line arguments"""
    print_section("Testing Main Application Arguments")
    
    try:
        # Test help argument
        print("🔄 Testing --help argument...")
        result = subprocess.run([sys.executable, 'src/main.py', '--help'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'VoiceNav' in result.stdout:
            print("✅ Help argument works")
        else:
            print("❌ Help argument failed")
            return False
        
        # Test version argument
        print("🔄 Testing --version argument...")
        result = subprocess.run([sys.executable, 'src/main.py', '--version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and 'VoiceNav' in result.stdout:
            print("✅ Version argument works")
        else:
            print("❌ Version argument failed")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Argument test failed: {e}")
        return False

def test_settings_panel_standalone():
    """Test settings panel in standalone mode"""
    print_section("Testing Settings Panel (Standalone)")
    
    try:
        print("🔄 Testing settings panel initialization...")
        
        # Import and create settings panel
        from src.ui.settings_panel import VoiceNavSettingsPanel
        
        # Create panel (don't run it)
        panel = VoiceNavSettingsPanel()
        print("✅ Settings panel created successfully")
        
        # Test configuration loading
        if hasattr(panel, 'config') and panel.config:
            print("✅ Configuration loaded in settings panel")
        else:
            print("❌ Configuration not loaded properly")
            return False
        
        # Test UI variables
        if hasattr(panel, 'vars') and panel.vars:
            print("✅ UI variables initialized")
        else:
            print("❌ UI variables not initialized")
            return False
        
        # Cleanup
        panel.root.destroy()
        print("✅ Settings panel cleanup successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Settings panel test failed: {e}")
        return False

def test_menu_bar_creation():
    """Test menu bar creation (without running)"""
    print_section("Testing Menu Bar Creation")
    
    try:
        print("🔄 Testing menu bar initialization...")
        
        # Import menu bar
        from src.ui.menu_bar import VoiceNavMenuBar
        
        # Note: We can't easily test rumps app creation without running it
        # But we can test that the class exists and has required methods
        
        required_methods = ['_setup_menu', 'update_status', 'start_voice_control', 
                          'stop_voice_control', 'emergency_stop']
        
        for method in required_methods:
            if hasattr(VoiceNavMenuBar, method):
                print(f"✅ Method {method} exists")
            else:
                print(f"❌ Missing method: {method}")
                return False
        
        print("✅ Menu bar class structure valid")
        return True
        
    except Exception as e:
        print(f"❌ Menu bar test failed: {e}")
        return False

def test_integration_with_stages():
    """Test integration with existing Stage 1 & 2"""
    print_section("Testing Integration with Existing Stages")
    
    try:
        print("🔄 Testing Stage 1 integration...")
        
        # Test voice listener import
        from src.input.voice_listener import create_voice_listener
        print("✅ Stage 1 (Voice) integration available")
        
        # Test command parser import
        from src.brain.command_parser import CommandParser
        print("✅ Stage 2 (Parser) integration available")
        
        # Test browser controller import
        from src.actions.applescript_browser import AppleScriptBrowserController
        print("✅ Stage 2 (Browser) integration available")
        
        # Test that main.py can import all components
        print("🔄 Testing complete integration...")
        maya = create_voice_listener(wake_word="hey maya")
        parser = CommandParser()
        browser = AppleScriptBrowserController("auto")
        
        print("✅ All stages integrate successfully")
        
        # Cleanup
        if hasattr(maya, 'cleanup'):
            maya.cleanup()
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def run_interactive_menu_bar_test():
    """Interactive test for menu bar (requires user)"""
    print_section("Interactive Menu Bar Test")
    
    print("🎤 This test will start the VoiceNav menu bar.")
    print("📱 You should see a microphone icon appear in your menu bar.")
    print("🖱️ Click the icon to test the menu options.")
    print("⏰ The test will auto-stop after 30 seconds.")
    print("")
    
    response = input("🤔 Run interactive menu bar test? (y/n): ").strip().lower()
    
    if response != 'y':
        print("⏭️ Skipping interactive menu bar test")
        return True
    
    try:
        print("🚀 Starting menu bar test...")
        print("💡 Look for the microphone icon in your menu bar!")
        
        # Start menu bar in subprocess with timeout
        process = subprocess.Popen([sys.executable, 'src/main.py', '--menu-bar'])
        
        # Wait for user to test
        print("\n⏱️ Testing for 30 seconds...")
        print("🖱️ Click the microphone icon in your menu bar")
        print("📋 Try the menu options")
        print("🛑 Menu bar will auto-stop in 30 seconds")
        
        time.sleep(30)
        
        # Terminate the process
        process.terminate()
        process.wait(timeout=5)
        
        print("✅ Menu bar test completed")
        
        # Ask user for feedback
        feedback = input("🤔 Did the menu bar work correctly? (y/n): ").strip().lower()
        return feedback == 'y'
        
    except Exception as e:
        print(f"❌ Interactive menu bar test failed: {e}")
        return False

def run_interactive_settings_test():
    """Interactive test for settings panel"""
    print_section("Interactive Settings Panel Test")
    
    print("⚙️ This test will open the VoiceNav settings panel.")
    print("🖱️ You can test the various settings tabs and options.")
    print("💾 Try changing some settings and saving.")
    print("")
    
    response = input("🤔 Run interactive settings test? (y/n): ").strip().lower()
    
    if response != 'y':
        print("⏭️ Skipping interactive settings test")
        return True
    
    try:
        print("🚀 Opening settings panel...")
        
        # Run settings panel
        result = subprocess.run([sys.executable, 'src/main.py', '--settings'], 
                              timeout=120)  # 2 minute timeout
        
        print("✅ Settings panel test completed")
        
        # Ask user for feedback
        feedback = input("🤔 Did the settings panel work correctly? (y/n): ").strip().lower()
        return feedback == 'y'
        
    except subprocess.TimeoutExpired:
        print("⏰ Settings panel test timed out (normal if user closed it)")
        feedback = input("🤔 Did the settings panel open and work? (y/n): ").strip().lower()
        return feedback == 'y'
    except Exception as e:
        print(f"❌ Interactive settings test failed: {e}")
        return False

def main():
    """Main testing function"""
    print_header("VoiceNav Stage 3 Testing - Menu Bar UI & Complete Application")
    
    print("🧪 This test validates the Stage 3 implementation:")
    print("  • Menu bar interface with rumps")
    print("  • Settings panel with tkinter")
    print("  • Integration with Stage 1 & 2")
    print("  • Complete application modes")
    print("")
    
    # Track test results
    results = {}
    
    # Run all tests
    tests = [
        ("UI Imports", test_ui_imports),
        ("Dependencies", test_dependencies),
        ("Config Updates", test_config_updates),
        ("Main Arguments", test_main_arguments),
        ("Settings Panel", test_settings_panel_standalone),
        ("Menu Bar Creation", test_menu_bar_creation),
        ("Stage Integration", test_integration_with_stages),
    ]
    
    for test_name, test_func in tests:
        print(f"\n🔄 Running {test_name} test...")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Interactive tests
    print_section("Interactive Tests (Optional)")
    print("👤 These tests require user interaction:")
    
    interactive_tests = [
        ("Menu Bar", run_interactive_menu_bar_test),
        ("Settings Panel", run_interactive_settings_test),
    ]
    
    for test_name, test_func in interactive_tests:
        try:
            results[f"Interactive {test_name}"] = test_func()
        except Exception as e:
            print(f"❌ Interactive {test_name} test crashed: {e}")
            results[f"Interactive {test_name}"] = False
    
    # Show results summary
    print_header("Stage 3 Test Results Summary")
    
    passed = 0
    total = 0
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
        total += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Stage 3 tests passed! Menu bar UI implementation complete.")
        print("\n🚀 VoiceNav Stage 3 is ready!")
        print("📱 Run with: python src/main.py --menu-bar")
        print("⚙️ Settings: python src/main.py --settings")
    else:
        print("⚠️ Some Stage 3 tests failed. Review the errors above.")
        print("💡 Common issues:")
        print("  • Missing rumps: pip install rumps")
        print("  • Missing PyYAML: pip install PyYAML")
        print("  • tkinter not available (should be with Python)")
    
    print(f"\n📅 Test completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Testing crashed: {e}")
        sys.exit(1)
