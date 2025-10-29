#!/usr/bin/env python3
"""
Test Script for VoiceNav Command Parser
Tests command parsing accuracy for all 8 core commands
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from brain.command_parser import CommandParser


def test_command_parser():
    """Test command parser with various inputs"""
    print("🧠 VoiceNav Command Parser Test")
    print("=" * 40)
    
    parser = CommandParser()
    
    # Test cases with expected results
    test_cases = [
        # Open URL commands
        ("open google", "open_url", "https://google.com"),
        ("go to youtube", "open_url", "https://youtube.com"),
        ("visit reddit.com", "open_url", "https://reddit.com"),
        ("navigate to github", "open_url", "https://github.com"),
        ("load news", "open_url", "https://news.google.com"),
        
        # Click element commands
        ("click login button", "click_element", "login"),
        ("click the search box", "click_element", "search"),
        ("tap the red button", "click_element", "red"),
        ("press submit", "click_element", "submit"),
        ("click on the first link", "click_element", "first link"),
        
        # Scroll commands
        ("scroll down", "scroll_down", "down"),
        ("scroll up", "scroll_up", "up"),
        ("page down", "scroll_down", "down"),
        ("go down", "scroll_down", "down"),
        ("move up", "scroll_up", "up"),
        
        # Navigation commands
        ("go back", "go_back", None),
        ("back", "go_back", None),
        ("previous page", "go_back", None),
        ("go forward", "go_forward", None),
        ("next page", "go_forward", None),
        
        # Content commands
        ("read page", "read_content", "main"),
        ("read this", "read_content", "main"),
        ("speak page", "read_content", "main"),
        ("tell me what it says", "read_content", "main"),
        
        # Control commands
        ("stop", "stop_action", None),
        ("halt", "stop_action", None),
        ("cancel", "stop_action", None),
        ("pause", "stop_action", None),
        
        # Help commands
        ("help", "help", None),
        ("what can you do", "help", None),
        ("show commands", "help", None),
        ("list commands", "help", None),
        
        # Refresh commands
        ("refresh", "refresh", None),
        ("reload page", "refresh", None),
        ("update page", "refresh", None),
        
        # Edge cases
        ("", "empty", None),
        ("some random nonsense", "unknown", None),
        ("maybe open google perhaps", "open_url", "https://google.com"),
    ]
    
    print(f"\n📝 Testing {len(test_cases)} command patterns:")
    print("-" * 40)
    
    passed = 0
    total = len(test_cases)
    
    for i, (input_text, expected_intent, expected_param) in enumerate(test_cases, 1):
        result = parser.parse(input_text)
        
        intent = result['intent']
        params = result['params']
        confidence = result['confidence']
        
        # Check if intent matches
        intent_correct = intent == expected_intent
        
        # Check specific parameter based on intent
        param_correct = True
        if expected_param is not None:
            if intent == 'open_url':
                param_correct = params.get('url') == expected_param
            elif intent == 'click_element':
                param_correct = expected_param.lower() in params.get('text', '').lower()
            elif intent in ['scroll_down', 'scroll_up']:
                param_correct = params.get('direction') == expected_param
            elif intent == 'read_content':
                param_correct = params.get('target') == expected_param
        
        # Overall result
        test_passed = intent_correct and param_correct
        if test_passed:
            passed += 1
        
        # Print result
        status = "✅" if test_passed else "❌"
        print(f"{status} Test {i:2d}: '{input_text[:30]:<30}' → {intent:<12} ({confidence:.1f})")
        
        if not test_passed:
            print(f"    Expected: {expected_intent}, Got: {intent}")
            if expected_param and not param_correct:
                if intent == 'open_url':
                    print(f"    Expected URL: {expected_param}, Got: {params.get('url')}")
                else:
                    print(f"    Expected param: {expected_param}, Got: {params}")
    
    print("\n" + "=" * 40)
    print(f"📊 RESULTS: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All command parsing tests PASSED!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Check patterns above.")
        return False


def test_url_normalization():
    """Test URL normalization functionality"""
    print("\n🔗 Testing URL Normalization")
    print("-" * 40)
    
    parser = CommandParser()
    
    url_tests = [
        ("google", "https://google.com"),
        ("youtube", "https://youtube.com"),
        ("reddit.com", "https://reddit.com"),
        ("github.com", "https://github.com"),
        ("https://example.com", "https://example.com"),
        ("search for cats", "https://google.com/search?q=search+for+cats"),
        ("bbc news", "https://bbc.com"),
        ("the weather website", "https://google.com/search?q=weather+website"),
    ]
    
    passed = 0
    
    for input_url, expected_url in url_tests:
        result_url = parser.normalize_url(input_url)
        
        test_passed = result_url == expected_url
        if test_passed:
            passed += 1
        
        status = "✅" if test_passed else "❌"
        print(f"{status} '{input_url}' → {result_url}")
        
        if not test_passed:
            print(f"    Expected: {expected_url}")
    
    print(f"\n📊 URL Tests: {passed}/{len(url_tests)} passed")
    return passed == len(url_tests)


def test_element_parsing():
    """Test element description parsing"""
    print("\n🎯 Testing Element Parsing")
    print("-" * 40)
    
    parser = CommandParser()
    
    element_tests = [
        ("login button", "button", "login"),
        ("search box", "input", "search"),
        ("red button", "button", "red"),
        ("email field", "input", "email"),
        ("submit", "any", "submit"),
        ("the first link", "any", "first link"),
    ]
    
    passed = 0
    
    for description, expected_type, expected_text in element_tests:
        result = parser.parse_element_description(description)
        
        type_correct = result['type'] == expected_type
        text_correct = expected_text.lower() in result.get('text', '').lower()
        
        test_passed = type_correct and text_correct
        if test_passed:
            passed += 1
        
        status = "✅" if test_passed else "❌"
        print(f"{status} '{description}' → type:{result['type']}, text:'{result['text']}'")
        
        if not test_passed:
            print(f"    Expected: type:{expected_type}, text containing:'{expected_text}'")
    
    print(f"\n📊 Element Tests: {passed}/{len(element_tests)} passed")
    return passed == len(element_tests)


def main():
    """Run all parser tests"""
    print("🧪 VoiceNav Command Parser - Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        # Run all test suites
        parser_passed = test_command_parser()
        url_passed = test_url_normalization()
        element_passed = test_element_parsing()
        
        # Overall results
        print("\n" + "=" * 60)
        print("🏁 FINAL RESULTS:")
        print(f"   Command Parsing: {'✅ PASS' if parser_passed else '❌ FAIL'}")
        print(f"   URL Normalization: {'✅ PASS' if url_passed else '❌ FAIL'}")
        print(f"   Element Parsing: {'✅ PASS' if element_passed else '❌ FAIL'}")
        
        if parser_passed and url_passed and element_passed:
            print("\n🎉 ALL TESTS PASSED! Command parser is ready for Stage 2.")
            print("✅ Ready to proceed with browser control integration.")
            return True
        else:
            print("\n⚠️  Some tests failed. Parser needs fixes before browser integration.")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the voicenav directory with venv activated")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
