"""
VoiceNav Settings Panel
Configuration interface for VoiceNav preferences
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yaml
import os
import sys
from typing import Dict, Any

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.logger import setup_logger

logger = setup_logger("settings_panel")


class VoiceNavSettingsPanel:
    """
    Settings panel for VoiceNav configuration
    
    Provides GUI for:
    - Voice recognition settings
    - Maya voice preferences  
    - Browser configuration
    - Audio feedback controls
    - Advanced options
    """
    
    def __init__(self, config_path: str = None):
        """
        Initialize settings panel
        
        Args:
            config_path: Path to config.yaml file
        """
        self.config_path = config_path or self._find_config_path()
        self.config = self._load_config()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("VoiceNav Settings")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables for settings
        self.vars = {}
        
        # Create UI
        self._create_ui()
        
        logger.info("Settings panel initialized")
    
    def _find_config_path(self) -> str:
        """Find config.yaml file"""
        # Try relative to this file
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_path = os.path.join(base_dir, "config.yaml")
        
        if os.path.exists(config_path):
            return config_path
        
        # Try current directory
        if os.path.exists("config.yaml"):
            return "config.yaml"
        
        # Default path
        return "config.yaml"
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                return self._default_config()
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'app': {
                'name': 'VoiceNav',
                'version': '0.1.0'
            },
            'voice': {
                'wake_word': 'Hey Maya',
                'timeout': 5,
                'language': 'en-US',
                'recognizer': 'whisper',
                'whisper_model': 'base'
            },
            'tts': {
                'engine': 'macos_say',
                'voice': 'Samantha',
                'rate': 150,
                'volume': 1.0
            },
            'browser': {
                'default': 'auto',
                'timeout': 30
            },
            'ui': {
                'show_notifications': True,
                'auto_start': False,
                'minimize_to_tray': True
            }
        }
    
    def _create_ui(self):
        """Create the settings user interface"""
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Voice Recognition Tab
        self._create_voice_tab(notebook)
        
        # Audio & TTS Tab
        self._create_audio_tab(notebook)
        
        # Browser Tab
        self._create_browser_tab(notebook)
        
        # Interface Tab
        self._create_interface_tab(notebook)
        
        # Advanced Tab
        self._create_advanced_tab(notebook)
        
        # Buttons frame
        self._create_buttons()
    
    def _create_voice_tab(self, notebook):
        """Create voice recognition settings tab"""
        voice_frame = ttk.Frame(notebook)
        notebook.add(voice_frame, text="Voice Recognition")
        
        # Wake word setting
        ttk.Label(voice_frame, text="Wake Word:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.vars['wake_word'] = tk.StringVar(value=self.config.get('voice', {}).get('wake_word', 'Hey Maya'))
        wake_word_entry = ttk.Entry(voice_frame, textvariable=self.vars['wake_word'], width=30)
        wake_word_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Recognition engine
        ttk.Label(voice_frame, text="Recognition Engine:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.vars['recognizer'] = tk.StringVar(value=self.config.get('voice', {}).get('recognizer', 'whisper'))
        recognizer_combo = ttk.Combobox(voice_frame, textvariable=self.vars['recognizer'], 
                                       values=['whisper', 'google', 'enhanced'], state='readonly')
        recognizer_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Whisper model
        ttk.Label(voice_frame, text="Whisper Model:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.vars['whisper_model'] = tk.StringVar(value=self.config.get('voice', {}).get('whisper_model', 'base'))
        model_combo = ttk.Combobox(voice_frame, textvariable=self.vars['whisper_model'],
                                  values=['tiny', 'base', 'small', 'medium', 'large'], state='readonly')
        model_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Timeout
        ttk.Label(voice_frame, text="Command Timeout (seconds):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.vars['timeout'] = tk.IntVar(value=self.config.get('voice', {}).get('timeout', 5))
        timeout_spin = ttk.Spinbox(voice_frame, from_=1, to=30, textvariable=self.vars['timeout'], width=10)
        timeout_spin.grid(row=3, column=1, padx=5, pady=5)
        
        # Language
        ttk.Label(voice_frame, text="Language:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.vars['language'] = tk.StringVar(value=self.config.get('voice', {}).get('language', 'en-US'))
        lang_combo = ttk.Combobox(voice_frame, textvariable=self.vars['language'],
                                 values=['en-US', 'en-GB', 'es-ES', 'fr-FR', 'de-DE'], state='readonly')
        lang_combo.grid(row=4, column=1, padx=5, pady=5)
    
    def _create_audio_tab(self, notebook):
        """Create audio and TTS settings tab"""
        audio_frame = ttk.Frame(notebook)
        notebook.add(audio_frame, text="Audio & Voice")
        
        # TTS Engine
        ttk.Label(audio_frame, text="Text-to-Speech Engine:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.vars['tts_engine'] = tk.StringVar(value=self.config.get('tts', {}).get('engine', 'macos_say'))
        tts_combo = ttk.Combobox(audio_frame, textvariable=self.vars['tts_engine'],
                                values=['macos_say', 'pyttsx3', 'edge_tts'], state='readonly')
        tts_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Voice selection
        ttk.Label(audio_frame, text="Maya Voice:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.vars['voice'] = tk.StringVar(value=self.config.get('tts', {}).get('voice', 'Samantha'))
        voice_combo = ttk.Combobox(audio_frame, textvariable=self.vars['voice'],
                                  values=['Samantha', 'Alex', 'Victoria', 'Allison', 'Ava'], state='readonly')
        voice_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Speech rate
        ttk.Label(audio_frame, text="Speech Rate:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.vars['rate'] = tk.IntVar(value=self.config.get('tts', {}).get('rate', 150))
        rate_scale = ttk.Scale(audio_frame, from_=50, to=300, variable=self.vars['rate'], orient=tk.HORIZONTAL)
        rate_scale.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Volume
        ttk.Label(audio_frame, text="Volume:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.vars['volume'] = tk.DoubleVar(value=self.config.get('tts', {}).get('volume', 1.0))
        volume_scale = ttk.Scale(audio_frame, from_=0.0, to=1.0, variable=self.vars['volume'], orient=tk.HORIZONTAL)
        volume_scale.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Test voice button
        test_button = ttk.Button(audio_frame, text="Test Maya Voice", command=self._test_voice)
        test_button.grid(row=4, column=1, padx=5, pady=10)
    
    def _create_browser_tab(self, notebook):
        """Create browser settings tab"""
        browser_frame = ttk.Frame(notebook)
        notebook.add(browser_frame, text="Browser")
        
        # Default browser
        ttk.Label(browser_frame, text="Default Browser:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.vars['browser'] = tk.StringVar(value=self.config.get('browser', {}).get('default', 'auto'))
        browser_combo = ttk.Combobox(browser_frame, textvariable=self.vars['browser'],
                                    values=['auto', 'safari', 'chrome', 'firefox'], state='readonly')
        browser_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Browser timeout
        ttk.Label(browser_frame, text="Browser Timeout (seconds):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.vars['browser_timeout'] = tk.IntVar(value=self.config.get('browser', {}).get('timeout', 30))
        timeout_spin = ttk.Spinbox(browser_frame, from_=5, to=120, textvariable=self.vars['browser_timeout'], width=10)
        timeout_spin.grid(row=1, column=1, padx=5, pady=5)
        
        # AppleScript vs Playwright
        ttk.Label(browser_frame, text="Browser Control Method:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.vars['control_method'] = tk.StringVar(value=self.config.get('browser', {}).get('method', 'applescript'))
        method_combo = ttk.Combobox(browser_frame, textvariable=self.vars['control_method'],
                                   values=['applescript', 'playwright'], state='readonly')
        method_combo.grid(row=2, column=1, padx=5, pady=5)
    
    def _create_interface_tab(self, notebook):
        """Create interface settings tab"""
        ui_frame = ttk.Frame(notebook)
        notebook.add(ui_frame, text="Interface")
        
        # Notifications
        self.vars['show_notifications'] = tk.BooleanVar(value=self.config.get('ui', {}).get('show_notifications', True))
        notifications_check = ttk.Checkbutton(ui_frame, text="Show Notifications", 
                                             variable=self.vars['show_notifications'])
        notifications_check.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Auto start
        self.vars['auto_start'] = tk.BooleanVar(value=self.config.get('ui', {}).get('auto_start', False))
        autostart_check = ttk.Checkbutton(ui_frame, text="Start with macOS", 
                                         variable=self.vars['auto_start'])
        autostart_check.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        
        # Minimize to tray
        self.vars['minimize_to_tray'] = tk.BooleanVar(value=self.config.get('ui', {}).get('minimize_to_tray', True))
        minimize_check = ttk.Checkbutton(ui_frame, text="Minimize to Menu Bar", 
                                        variable=self.vars['minimize_to_tray'])
        minimize_check.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        
        # Menu bar icon
        ttk.Label(ui_frame, text="Menu Bar Icon Style:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.vars['icon_style'] = tk.StringVar(value=self.config.get('ui', {}).get('icon_style', 'emoji'))
        icon_combo = ttk.Combobox(ui_frame, textvariable=self.vars['icon_style'],
                                 values=['emoji', 'text', 'minimal'], state='readonly')
        icon_combo.grid(row=3, column=1, padx=5, pady=5)
    
    def _create_advanced_tab(self, notebook):
        """Create advanced settings tab"""
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Advanced")
        
        # Logging level
        ttk.Label(advanced_frame, text="Logging Level:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.vars['log_level'] = tk.StringVar(value=self.config.get('logging', {}).get('level', 'INFO'))
        log_combo = ttk.Combobox(advanced_frame, textvariable=self.vars['log_level'],
                                values=['DEBUG', 'INFO', 'WARNING', 'ERROR'], state='readonly')
        log_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Config file path
        ttk.Label(advanced_frame, text="Config File:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(advanced_frame, text=self.config_path, foreground="gray").grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Raw config editor button
        edit_button = ttk.Button(advanced_frame, text="Edit Raw Config", command=self._edit_raw_config)
        edit_button.grid(row=2, column=1, padx=5, pady=10)
        
        # Reset to defaults button
        reset_button = ttk.Button(advanced_frame, text="Reset to Defaults", command=self._reset_defaults)
        reset_button.grid(row=3, column=1, padx=5, pady=5)
    
    def _create_buttons(self):
        """Create action buttons"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Save button
        save_button = ttk.Button(button_frame, text="Save Settings", command=self._save_settings)
        save_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self._cancel)
        cancel_button.pack(side=tk.RIGHT)
        
        # Apply button
        apply_button = ttk.Button(button_frame, text="Apply", command=self._apply_settings)
        apply_button.pack(side=tk.RIGHT, padx=(0, 5))
    
    def _test_voice(self):
        """Test Maya voice with current settings"""
        try:
            import subprocess
            voice = self.vars['voice'].get()
            subprocess.run(['say', '-v', voice, 'Hello! This is Maya voice test.'], check=True)
        except Exception as e:
            messagebox.showerror("Voice Test Failed", f"Failed to test voice: {e}")
    
    def _edit_raw_config(self):
        """Open raw config file in default editor"""
        try:
            import subprocess
            subprocess.run(['open', '-t', self.config_path])
        except Exception as e:
            messagebox.showerror("Edit Failed", f"Failed to open config file: {e}")
    
    def _reset_defaults(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults? This cannot be undone."):
            self.config = self._default_config()
            self._update_ui_from_config()
    
    def _update_ui_from_config(self):
        """Update UI elements from current config"""
        # Voice settings
        self.vars['wake_word'].set(self.config.get('voice', {}).get('wake_word', 'Hey Maya'))
        self.vars['recognizer'].set(self.config.get('voice', {}).get('recognizer', 'whisper'))
        self.vars['whisper_model'].set(self.config.get('voice', {}).get('whisper_model', 'base'))
        self.vars['timeout'].set(self.config.get('voice', {}).get('timeout', 5))
        self.vars['language'].set(self.config.get('voice', {}).get('language', 'en-US'))
        
        # Audio settings
        self.vars['tts_engine'].set(self.config.get('tts', {}).get('engine', 'macos_say'))
        self.vars['voice'].set(self.config.get('tts', {}).get('voice', 'Samantha'))
        self.vars['rate'].set(self.config.get('tts', {}).get('rate', 150))
        self.vars['volume'].set(self.config.get('tts', {}).get('volume', 1.0))
        
        # Browser settings
        self.vars['browser'].set(self.config.get('browser', {}).get('default', 'auto'))
        self.vars['browser_timeout'].set(self.config.get('browser', {}).get('timeout', 30))
        self.vars['control_method'].set(self.config.get('browser', {}).get('method', 'applescript'))
        
        # UI settings
        self.vars['show_notifications'].set(self.config.get('ui', {}).get('show_notifications', True))
        self.vars['auto_start'].set(self.config.get('ui', {}).get('auto_start', False))
        self.vars['minimize_to_tray'].set(self.config.get('ui', {}).get('minimize_to_tray', True))
        self.vars['icon_style'].set(self.config.get('ui', {}).get('icon_style', 'emoji'))
        
        # Advanced settings
        self.vars['log_level'].set(self.config.get('logging', {}).get('level', 'INFO'))
    
    def _apply_settings(self):
        """Apply settings without closing"""
        self._save_config()
        messagebox.showinfo("Settings Applied", "Settings have been applied successfully.")
    
    def _save_settings(self):
        """Save settings and close"""
        self._save_config()
        self.root.destroy()
    
    def _cancel(self):
        """Cancel without saving"""
        self.root.destroy()
    
    def _save_config(self):
        """Save current settings to config file"""
        try:
            # Update config from UI
            self.config['voice'] = {
                'wake_word': self.vars['wake_word'].get(),
                'recognizer': self.vars['recognizer'].get(),
                'whisper_model': self.vars['whisper_model'].get(),
                'timeout': self.vars['timeout'].get(),
                'language': self.vars['language'].get()
            }
            
            self.config['tts'] = {
                'engine': self.vars['tts_engine'].get(),
                'voice': self.vars['voice'].get(),
                'rate': self.vars['rate'].get(),
                'volume': self.vars['volume'].get()
            }
            
            self.config['browser'] = {
                'default': self.vars['browser'].get(),
                'timeout': self.vars['browser_timeout'].get(),
                'method': self.vars['control_method'].get()
            }
            
            self.config['ui'] = {
                'show_notifications': self.vars['show_notifications'].get(),
                'auto_start': self.vars['auto_start'].get(),
                'minimize_to_tray': self.vars['minimize_to_tray'].get(),
                'icon_style': self.vars['icon_style'].get()
            }
            
            if 'logging' not in self.config:
                self.config['logging'] = {}
            self.config['logging']['level'] = self.vars['log_level'].get()
            
            # Save to file
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
            logger.info(f"Settings saved to {self.config_path}")
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            messagebox.showerror("Save Failed", f"Failed to save settings: {e}")
    
    def run(self):
        """Run the settings panel"""
        self.root.mainloop()


def main():
    """Main entry point for settings panel"""
    try:
        panel = VoiceNavSettingsPanel()
        panel.run()
    except Exception as e:
        print(f"❌ Settings panel error: {e}")


if __name__ == "__main__":
    main()
