"""
Environment Test Script for VoiceNav
Tests Python version, dependencies, and system capabilities
"""
import sys
import platform
import importlib
from pathlib import Path

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text):
    """Print a formatted header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓{RESET} {text}")


def print_error(text):
    """Print error message"""
    print(f"{RED}✗{RESET} {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠{RESET} {text}")


def check_python_version():
    """Check if Python version is 3.11 or higher"""
    print_header("Python Version Check")
    
    version_info = sys.version_info
    version_string = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    
    print(f"Detected Python version: {version_string}")
    
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 11):
        print_error(f"Python 3.11+ required, but {version_string} found")
        return False
    else:
        print_success(f"Python version {version_string} is compatible")
        return True


def check_system_info():
    """Print system information"""
    print_header("System Information")
    
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Executable: {sys.executable}")
    
    # Check for macOS
    if sys.platform != "darwin":
        print_warning("This app is designed for macOS. Current platform: " + sys.platform)
        return False
    else:
        print_success("Running on macOS")
        return True


def check_dependencies():
    """Check if required dependencies can be imported"""
    print_header("Dependency Check")
    
    dependencies = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "PyAudio"),
        ("pyttsx3", "pyttsx3"),
        ("playwright", "Playwright"),
        ("rumps", "rumps"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_ok = True
    
    for module_name, package_name in dependencies:
        try:
            importlib.import_module(module_name)
            print_success(f"{package_name} is installed")
        except ImportError as e:
            print_error(f"{package_name} is NOT installed: {e}")
            all_ok = False
    
    return all_ok


def check_microphone_access():
    """Check if microphone access is available"""
    print_header("Microphone Check")
    
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        p.terminate()
        
        if device_count > 0:
            print_success(f"Microphone access available ({device_count} audio devices detected)")
            return True
        else:
            print_error("No audio devices detected")
            return False
    except Exception as e:
        print_error(f"Could not access microphone: {e}")
        print_warning("You may need to grant microphone permissions or install portaudio")
        return False


def check_project_structure():
    """Check if project structure is correct"""
    print_header("Project Structure Check")
    
    project_root = Path(__file__).parent.parent
    required_dirs = [
        "src",
        "src/utils",
        "tests",
    ]
    
    required_files = [
        "requirements.txt",
        ".gitignore",
        "config.yaml",
        "src/__init__.py",
        "src/main.py",
        "src/utils/__init__.py",
        "src/utils/logger.py",
    ]
    
    all_ok = True
    
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print_success(f"Directory exists: {dir_name}")
        else:
            print_error(f"Directory missing: {dir_name}")
            all_ok = False
    
    for file_name in required_files:
        file_path = project_root / file_name
        if file_path.exists() and file_path.is_file():
            print_success(f"File exists: {file_name}")
        else:
            print_error(f"File missing: {file_name}")
            all_ok = False
    
    return all_ok


def main():
    """Run all environment checks"""
    print(f"\n{BLUE}VoiceNav Environment Test Suite{RESET}")
    print(f"{BLUE}MacBook M3 Pro Edition - MVP{RESET}")
    
    results = {
        "Python Version": check_python_version(),
        "System Info": check_system_info(),
        "Project Structure": check_project_structure(),
        "Dependencies": check_dependencies(),
        "Microphone Access": check_microphone_access(),
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print(f"\n{GREEN}✓ All checks passed! VoiceNav environment is ready.{RESET}")
        return 0
    else:
        print(f"\n{RED}✗ Some checks failed. Please review the errors above.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
