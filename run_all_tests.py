#!/usr/bin/env python3
"""
VoiceNav Master Test Runner
Runs all tests in proper sequence to validate complete system
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"🎯 {title}")
    print("="*70)

def print_test_info(test_name, description):
    """Print test information"""
    print(f"\n🧪 TEST: {test_name}")
    print(f"📋 {description}")
    print("-" * 50)

def run_test_script(script_path, test_name, timeout=120, interactive=False):
    """Run a test script and return results"""
    print(f"▶️  Running {test_name}...")
    
    if interactive:
        print(f"🎤 {test_name} requires voice interaction...")
        print("You will need to speak to Maya during this test.")
        print("The test will run in your terminal - follow all prompts!")
        
        ready = input("\n🎯 Ready to start interactive test? (y/n): ").lower().strip()
        if ready != 'y':
            print(f"⏭️ Skipping {test_name}")
            return None, 0, "Skipped by user", ""
        
        print(f"\n🚀 Starting {test_name}...")
        print("=" * 50)
        
        try:
            start_time = time.time()
            # Run interactive test with direct terminal access (no capture)
            result = subprocess.run([sys.executable, script_path])
            end_time = time.time()
            
            duration = end_time - start_time
            
            # Ask user for test result since we can't capture output
            print(f"\n📊 {test_name} completed in {duration:.1f}s")
            user_result = input("Did the test pass? (y/n): ").lower().strip()
            
            if user_result == 'y':
                print(f"✅ {test_name} PASSED")
                return True, duration, "Interactive test passed (user confirmed)", ""
            else:
                print(f"❌ {test_name} FAILED")
                issue = input("What was the issue? (optional): ").strip()
                return False, duration, "Interactive test failed (user confirmed)", issue
                
        except KeyboardInterrupt:
            print(f"\n⚠️ {test_name} STOPPED BY USER")
            return False, 0, "", "Stopped by user with Ctrl+C"
        except Exception as e:
            print(f"💥 {test_name} ERROR: {e}")
            return False, 0, "", str(e)
    else:
        # Non-interactive test
        try:
            start_time = time.time()
            result = subprocess.run([
                sys.executable, script_path
            ], timeout=timeout, capture_output=True, text=True)
            end_time = time.time()
            
            duration = end_time - start_time
            
            if result.returncode == 0:
                print(f"✅ {test_name} PASSED ({duration:.1f}s)")
                return True, duration, result.stdout, result.stderr
            else:
                print(f"❌ {test_name} FAILED ({duration:.1f}s)")
                return False, duration, result.stdout, result.stderr
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_name} TIMED OUT")
            return False, timeout, "", "Test timed out"
        except Exception as e:
            print(f"💥 {test_name} ERROR: {e}")
            return False, 0, "", str(e)

def check_environment():
    """Check basic environment setup"""
    print_test_info("Environment Check", "Validate Python, virtual env, and basic setup")
    
    # Check if we're in the right directory
    if not os.path.exists("src/input/voice_listener.py"):
        print("❌ Not in VoiceNav project directory")
        print("Run from: ~/Github/Personal/voicenav")
        return False
    
    # Check virtual environment
    if not os.environ.get('VIRTUAL_ENV'):
        print("❌ Virtual environment not activated")
        print("Run: source venv/bin/activate")
        return False
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python {version.major}.{version.minor} too old, need 3.11+")
        return False
    
    print(f"✅ Environment OK (Python {version.major}.{version.minor}.{version.micro})")
    return True

def main():
    """Run all VoiceNav tests in sequence"""
    print_header("VOICENAV MASTER TEST RUNNER")
    
    print("This will run ALL VoiceNav tests to validate your system:")
    print("• Environment validation")
    print("• REVERTED Maya system (original working version)")
    print("• Maya wake word detection") 
    print("• Whisper AI recognition (without complex thresholds)")
    print("• Audio feedback (Samantha voice)")
    print("• Complete Stage 1 validation")
    
    print(f"\n📍 Current directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    print(f"🌍 Virtual env: {os.environ.get('VIRTUAL_ENV', 'Not activated')}")
    
    response = input("\n🚀 Ready to run all tests? (y/n): ").lower().strip()
    if response != 'y':
        print("Test run cancelled.")
        return
    
    # Test sequence (script, name, description, timeout, interactive)
    tests = [
        ("tests/test_environment.py", "Environment Test", "Basic environment validation", 60, False),
        ("test_maya.py", "Maya Quick Test", "Basic Maya wake word test", 120, True), 
        ("test_maya_whisper.py", "Maya + Whisper Test", "REVERTED - Original working system", 180, True),
        ("tests/test_voice.py", "Full Voice Test", "3-round comprehensive test", 300, True),
        ("test_maya_voice.py", "Voice Integration", "Audio feedback validation", 120, True),
        ("test_original_maya.py", "Original Maya Test", "Test reverted working system", 120, True)
    ]
    
    # Pre-flight check
    print_header("PRE-FLIGHT CHECK")
    if not check_environment():
        print("\n❌ Environment check failed. Fix issues and try again.")
        return
    
    # Run tests
    results = []
    total_start = time.time()
    
    for i, (script, name, desc, timeout, interactive) in enumerate(tests, 1):
        print_header(f"TEST {i}/{len(tests)}: {name.upper()}")
        print_test_info(name, desc)
        
        if not os.path.exists(script):
            print(f"❌ Test script not found: {script}")
            results.append((name, False, 0, "", f"Script not found: {script}"))
            continue
        
        # Ask user if they want to run this test
        if i > 1:  # Skip prompt for first test
            response = input(f"\n▶️  Run {name}? (y/n/q): ").lower().strip()
            if response == 'q':
                print("Test run stopped by user.")
                break
            elif response != 'y':
                print(f"⏭️  Skipping {name}")
                results.append((name, None, 0, "", "Skipped by user"))
                continue
        
        # Run the test (with interactive flag)
        passed, duration, stdout, stderr = run_test_script(script, name, timeout, interactive)
        results.append((name, passed, duration, stdout, stderr))
        
        # Show brief output for failed tests
        if not passed and stderr:
            print(f"💬 Error details:")
            print(stderr[:300] + ("..." if len(stderr) > 300 else ""))
        
        # Pause between tests
        if i < len(tests):
            print("\n⏸️  Pausing 3 seconds before next test...")
            time.sleep(3)
    
    # Final results
    total_end = time.time()
    total_duration = total_end - total_start
    
    print_header("FINAL TEST RESULTS")
    
    passed_count = 0
    failed_count = 0
    skipped_count = 0
    total_test_time = 0
    
    for name, passed, duration, stdout, stderr in results:
        total_test_time += duration
        
        if passed is True:
            print(f"✅ {name:<25} PASSED ({duration:.1f}s)")
            passed_count += 1
        elif passed is False:
            print(f"❌ {name:<25} FAILED ({duration:.1f}s)")
            failed_count += 1
        else:
            print(f"⏭️  {name:<25} SKIPPED")
            skipped_count += 1
    
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ Passed: {passed_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   ⏱️  Total time: {total_duration:.1f}s")
    print(f"   🧪 Test time: {total_test_time:.1f}s")
    
    # Overall assessment
    if failed_count == 0 and passed_count > 0:
        print_header("🎉 ALL TESTS PASSED!")
        print("✅ VoiceNav Stage 1 is working perfectly!")
        print("🚀 Ready for Stage 2: Browser Control")
        print("\n📝 Next steps:")
        print("1. Update DEVLOG.md with test results")
        print("2. Commit changes to git")
        print("3. Begin Stage 2 development")
        
    elif passed_count > failed_count:
        print_header("⚠️  MOSTLY WORKING")
        print(f"✅ {passed_count} tests passed, {failed_count} failed")
        print("🔧 Fix failing tests before proceeding to Stage 2")
        
    else:
        print_header("❌ TESTS FAILED")
        print("🔧 Fix the failing tests before proceeding")
        print("📖 Check SETUP_GUIDE.md for troubleshooting")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"test_results_{timestamp}.log"
    
    with open(log_file, 'w') as f:
        f.write(f"VoiceNav Test Results - {datetime.now()}\n")
        f.write("="*50 + "\n\n")
        
        for name, passed, duration, stdout, stderr in results:
            f.write(f"TEST: {name}\n")
            f.write(f"Result: {'PASSED' if passed else 'FAILED' if passed is False else 'SKIPPED'}\n")
            f.write(f"Duration: {duration:.1f}s\n")
            f.write(f"STDOUT:\n{stdout}\n")
            f.write(f"STDERR:\n{stderr}\n")
            f.write("-" * 30 + "\n\n")
    
    print(f"\n📄 Detailed results saved to: {log_file}")
    print("="*70)

if __name__ == "__main__":
    main()
