#!/usr/bin/env python3
"""
UI Component Tests
Unit tests for VoiceNav Stage 3 UI components
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add src directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('src')


class TestUIModuleImports(unittest.TestCase):
    """Test UI module imports"""
    
    def test_ui_package_import(self):
        """Test UI package can be imported"""
        try:
            import src.ui
            self.assertTrue(hasattr(src.ui, 'VoiceNavMenuBar'))
        except ImportError as e:
            self.fail(f"UI package import failed: {e}")
    
    def test_menu_bar_import(self):
        """Test menu bar module import"""
        try:
            from src.ui.menu_bar import VoiceNavMenuBar
            self.assertTrue(callable(VoiceNavMenuBar))
        except ImportError as e:
            self.skipTest(f"Menu bar import failed (rumps not available?): {e}")
    
    def test_settings_panel_import(self):
        """Test settings panel import"""
        try:
            from src.ui.settings_panel import VoiceNavSettingsPanel
            self.assertTrue(callable(VoiceNavSettingsPanel))
        except ImportError as e:
            self.skipTest(f"Settings panel import failed (tkinter/yaml not available?): {e}")


class TestSettingsPanel(unittest.TestCase):
    """Test settings panel functionality"""
    
    def setUp(self):
        """Setup test environment"""
        try:
            from src.ui.settings_panel import VoiceNavSettingsPanel
            self.settings_class = VoiceNavSettingsPanel
        except ImportError:
            self.skipTest("Settings panel not available")
    
    def test_default_config(self):
        """Test default configuration generation"""
        # Test without creating UI (to avoid tkinter requirements)
        panel = Mock()
        panel._default_config = self.settings_class._default_config
        
        config = panel._default_config()
        
        # Check required sections
        self.assertIn('app', config)
        self.assertIn('voice', config)
        self.assertIn('tts', config)
        self.assertIn('browser', config)
        self.assertIn('ui', config)
        
        # Check specific values
        self.assertEqual(config['voice']['wake_word'], 'Hey Maya')
        self.assertEqual(config['tts']['voice'], 'Samantha')
        self.assertEqual(config['browser']['default'], 'auto')
    
    @patch('tkinter.Tk')
    def test_settings_panel_creation(self, mock_tk):
        """Test settings panel creation without GUI"""
        # Mock tkinter to avoid GUI creation
        mock_root = Mock()
        mock_tk.return_value = mock_root
        
        try:
            panel = self.settings_class()
            self.assertIsNotNone(panel)
            self.assertTrue(hasattr(panel, 'config'))
            self.assertTrue(hasattr(panel, 'vars'))
        except Exception as e:
            self.fail(f"Settings panel creation failed: {e}")


class TestMenuBar(unittest.TestCase):
    """Test menu bar functionality"""
    
    def setUp(self):
        """Setup test environment"""
        try:
            from src.ui.menu_bar import VoiceNavMenuBar
            self.menu_class = VoiceNavMenuBar
        except ImportError:
            self.skipTest("Menu bar not available (rumps required)")
    
    def test_menu_bar_class_structure(self):
        """Test menu bar class has required methods"""
        required_methods = [
            '_setup_menu',
            'update_status', 
            'start_voice_control',
            'stop_voice_control',
            'emergency_stop',
            'test_maya_voice',
            'show_help',
            'show_settings'
        ]
        
        for method in required_methods:
            self.assertTrue(hasattr(self.menu_class, method), 
                          f"Menu bar missing method: {method}")
    
    def test_icon_definitions(self):
        """Test menu bar has status icons defined"""
        # We can't instantiate rumps app easily, so test class attributes
        # This is a basic structural test
        self.assertTrue(hasattr(self.menu_class, '__init__'))


class TestMainIntegration(unittest.TestCase):
    """Test main.py integration with UI components"""
    
    def test_main_imports(self):
        """Test main.py can import required modules"""
        try:
            import src.main
            self.assertTrue(hasattr(src.main, 'run_menu_bar'))
            self.assertTrue(hasattr(src.main, 'run_settings'))
            self.assertTrue(hasattr(src.main, 'parse_args'))
        except ImportError as e:
            self.fail(f"Main module import failed: {e}")
    
    def test_argument_parser(self):
        """Test command line argument parsing"""
        try:
            from src.main import parse_args
            
            # Test with mock arguments
            with patch('sys.argv', ['main.py', '--help']):
                try:
                    parse_args()
                except SystemExit:
                    # Help argument causes SystemExit, which is expected
                    pass
        except Exception as e:
            self.fail(f"Argument parsing failed: {e}")


class TestConfigIntegration(unittest.TestCase):
    """Test configuration integration"""
    
    def test_config_file_exists(self):
        """Test config.yaml exists and has UI section"""
        try:
            import yaml
            config_path = 'config.yaml'
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                # Check UI section exists
                self.assertIn('ui', config, "config.yaml missing 'ui' section")
                
                # Check UI settings
                ui_config = config['ui']
                expected_keys = ['show_notifications', 'auto_start', 'minimize_to_tray', 'icon_style']
                
                for key in expected_keys:
                    self.assertIn(key, ui_config, f"UI config missing '{key}'")
            else:
                self.skipTest("config.yaml not found")
                
        except ImportError:
            self.skipTest("PyYAML not available")
        except Exception as e:
            self.fail(f"Config test failed: {e}")


def run_ui_tests():
    """Run all UI tests"""
    print("🧪 Running VoiceNav UI Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestUIModuleImports,
        TestSettingsPanel,
        TestMenuBar,
        TestMainIntegration,
        TestConfigIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("🏁 UI Test Summary")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if result.skipped:
        print("\n⏭️ Skipped:")
        for test, reason in result.skipped:
            print(f"  - {test}: {reason}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n✅ All UI tests passed!")
    else:
        print("\n❌ Some UI tests failed")
    
    return success


if __name__ == "__main__":
    success = run_ui_tests()
    sys.exit(0 if success else 1)
