#!/usr/bin/env python3
"""
VoiceNav Launch Script
Easy launcher for VoiceNav in different modes
"""

import sys
import os
import subprocess

def print_banner():
    """Print VoiceNav banner"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                VoiceNav                                       ║
║                     Voice-Controlled Browser Automation                       ║
║                        Powered by Maya AI Assistant                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""")

def print_modes():
    """Print available modes"""
    print("🚀 Available Modes:")
    print("1. 📱 Menu Bar Mode     - Run VoiceNav in macOS menu bar (Recommended)")
    print("2. ⚙️  Settings Panel    - Configure VoiceNav preferences")
    print("3. 💻 Command Line Mode - Original terminal interface")
    print("4. 🧪 Test Suite        - Validate VoiceNav functionality")
    print("5. ❓ Help             - Show detailed help information")
    print("6. 🚪 Exit             - Quit launcher")

def launch_menu_bar():
    """Launch VoiceNav menu bar"""
    print("📱 Launching VoiceNav Menu Bar...")
    print("Look for the microphone icon in your macOS menu bar!")
    subprocess.run([sys.executable, "src/main.py", "--menu-bar"])

def launch_settings():
    """Launch settings panel"""
    print("⚙️ Launching VoiceNav Settings Panel...")
    subprocess.run([sys.executable, "src/main.py", "--settings"])

def launch_command_line():
    """Launch command-line mode"""
    print("💻 Launching VoiceNav Command Line Mode...")
    subprocess.run([sys.executable, "src/main.py"])

def launch_tests():
    """Launch test suite"""
    print("🧪 Launching VoiceNav Test Suite...")
    print("This will run all VoiceNav tests to validate your system")
    subprocess.run([sys.executable, "run_all_tests.py"])

def show_help():
    """Show help information"""
    print("❓ VoiceNav Help:")
    subprocess.run([sys.executable, "src/main.py", "--help"])

def check_environment():
    """Check if we're in the right directory and environment"""
    # Check if we're in VoiceNav directory
    if not os.path.exists("src/main.py"):
        print("❌ Error: Not in VoiceNav project directory")
        print("Please run this script from: ~/Github/Personal/voicenav")
        return False
    
    # Check virtual environment (recommended but not required)
    if not os.environ.get('VIRTUAL_ENV'):
        print("⚠️  Warning: Virtual environment not activated")
        print("Recommended: source venv/bin/activate")
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            return False
    
    return True

def main():
    """Main launcher interface"""
    if not check_environment():
        return
    
    print_banner()
    
    while True:
        print_modes()
        
        try:
            choice = input("\n🎯 Select mode (1-6): ").strip()
            
            if choice == '1':
                launch_menu_bar()
            elif choice == '2':
                launch_settings()
            elif choice == '3':
                launch_command_line()
            elif choice == '4':
                launch_tests()
            elif choice == '5':
                show_help()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
                continue
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
        
        print("\n" + "─" * 80)
        response = input("🔄 Return to launcher menu? (y/n): ").lower().strip()
        if response != 'y':
            break

if __name__ == "__main__":
    main()
