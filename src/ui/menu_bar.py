"""
VoiceNav Menu Bar Interface
macOS menu bar application using rumps
"""

import rumps
import asyncio
import threading
import subprocess
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.logger import setup_logger
from src.input.voice_listener import create_voice_listener
from src.brain.command_parser import CommandParser
from src.actions.applescript_browser import AppleScriptBrowserController

logger = setup_logger("menu_bar")


class VoiceNavMenuBar(rumps.App):
    """
    VoiceNav Menu Bar Application
    
    Provides:
    - Menu bar icon with status indicators
    - Start/Stop voice control
    - Settings and preferences
    - Help and documentation
    - Status monitoring
    """
    
    def __init__(self):
        """Initialize menu bar application"""
        # Get the path to our icons
        self.assets_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "assets", "images"
        )
        
        # Initialize with ear icon
        ear_icon_path = os.path.join(self.assets_path, "ear_icon.svg")
        
        super(VoiceNavMenuBar, self).__init__(
            "VoiceNav",
            icon=ear_icon_path if os.path.exists(ear_icon_path) else None,
            template=True
        )
        
        # Application state
        self.is_voice_active = False
        self.is_maya_listening = False
        self.maya = None
        self.parser = None
        self.browser = None
        self.voice_thread = None
        self.loop = None
        self.loop_thread = None
        
        # Status icon paths
        self.icon_paths = {
            'idle': os.path.join(self.assets_path, "ear_icon.svg"),
            'listening': os.path.join(self.assets_path, "ear_listening.svg"),
            'processing': os.path.join(self.assets_path, "ear_processing.svg"),
            'speaking': os.path.join(self.assets_path, "ear_icon.svg"),  # Same as idle for now
            'error': os.path.join(self.assets_path, "ear_error.svg"),
            'stopped': os.path.join(self.assets_path, "ear_icon.svg")  # Same as idle for now
        }
        
        # Fallback text icons if SVGs don't work
        self.text_icons = {
            'idle': '👂',
            'listening': '👂',
            'processing': '🧠',
            'speaking': '🗣️',
            'error': '❌',
            'stopped': '⏸️'
        }
        
        # Initialize menu items
        self._setup_menu()
        
        logger.info("VoiceNav menu bar initialized")
    
    def _setup_menu(self):
        """Setup menu bar items"""
        
        # Main controls
        self.start_item = rumps.MenuItem(
            "Start Voice Control",
            callback=self.start_voice_control
        )
        self.stop_item = rumps.MenuItem(
            "Stop Voice Control", 
            callback=self.stop_voice_control
        )
        self.stop_item.set_callback(None)  # Disabled initially
        
        # Status display
        self.status_item = rumps.MenuItem("Status: Stopped", callback=None)
        
        # Separator
        separator1 = rumps.separator
        
        # Voice settings
        self.mute_item = rumps.MenuItem(
            "Mute Maya",
            callback=self.toggle_mute
        )
        
        # Quick actions
        self.test_maya_item = rumps.MenuItem(
            "Test Maya Voice",
            callback=self.test_maya_voice
        )
        
        # Browser controls
        self.emergency_stop_item = rumps.MenuItem(
            "Emergency Stop",
            callback=self.emergency_stop
        )
        
        # Separator
        separator2 = rumps.separator
        
        # Help and info
        self.help_item = rumps.MenuItem(
            "Voice Commands Help",
            callback=self.show_help
        )
        
        self.about_item = rumps.MenuItem(
            "About VoiceNav",
            callback=self.show_about
        )
        
        # Settings
        self.settings_item = rumps.MenuItem(
            "Settings",
            callback=self.show_settings
        )
        
        # Separator
        separator3 = rumps.separator
        
        # Quit
        self.quit_item = rumps.MenuItem(
            "Quit VoiceNav",
            callback=rumps.quit_application
        )
        
        # Add all items to menu
        self.menu = [
            self.start_item,
            self.stop_item,
            separator1,
            self.status_item,
            separator2,
            self.mute_item,
            self.test_maya_item,
            self.emergency_stop_item,
            separator2,
            self.help_item,
            self.about_item,
            self.settings_item,
            separator3,
            self.quit_item
        ]
    
    def update_status(self, status: str, icon_key: str = 'idle'):
        """
        Update menu bar status
        
        Args:
            status: Status text
            icon_key: Icon key for choosing icon
        """
        # Try to use SVG icon first, fallback to text or just title
        icon_path = self.icon_paths.get(icon_key)
        if icon_path and os.path.exists(icon_path):
            try:
                self.icon = icon_path
            except Exception as e:
                logger.debug(f"SVG icon failed: {e}, using text fallback")
                # Fallback to text-based title
                self.title = self.text_icons.get(icon_key, '👂')
        else:
            # Use text-based title
            self.title = self.text_icons.get(icon_key, '👂')
        
        self.status_item.title = f"Status: {status}"
        logger.debug(f"Status updated: {status} ({icon_key})")
    
    @rumps.clicked("Start Voice Control")
    def start_voice_control(self, _):
        """Start Maya voice control system"""
        if self.is_voice_active:
            return
        
        logger.info("Starting voice control...")
        self.update_status("Initializing...", 'processing')
        
        try:
            # Start async loop in separate thread
            self.loop_thread = threading.Thread(
                target=self._start_async_loop,
                daemon=True
            )
            self.loop_thread.start()
            
            # Update menu state
            self.start_item.set_callback(None)  # Disable start
            self.stop_item.set_callback(self.stop_voice_control)  # Enable stop
            
            self.is_voice_active = True
            
            # Show startup notification
            rumps.notification(
                title="VoiceNav Started",
                subtitle="Maya is ready for voice commands",
                message="Say 'Hey Maya' to get started"
            )
            
        except Exception as e:
            logger.error(f"Failed to start voice control: {e}")
            self.update_status("Start Failed", 'error')
            
            rumps.notification(
                title="VoiceNav Error",
                subtitle="Failed to start voice control",
                message=str(e)
            )
    
    def _start_async_loop(self):
        """Start the async event loop for voice control"""
        try:
            # Create new event loop for this thread
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # Run the voice control system
            self.loop.run_until_complete(self._initialize_and_run())
            
        except Exception as e:
            logger.error(f"Async loop error: {e}")
            self.update_status("Error", 'error')
    
    async def _initialize_and_run(self):
        """Initialize components and run voice control"""
        try:
            # Initialize Maya (Stage 1)
            self.update_status("Loading Maya...", 'processing')
            self.maya = create_voice_listener(wake_word="hey maya")
            logger.info("Maya initialized")
            
            # Initialize command parser (Stage 2)
            self.update_status("Loading Parser...", 'processing')
            self.parser = CommandParser()
            logger.info("Command parser initialized")
            
            # Initialize browser controller (Stage 2)
            self.update_status("Loading Browser...", 'processing')
            self.browser = AppleScriptBrowserController("auto")
            browser_ready = await self.browser.initialize()
            
            if not browser_ready:
                raise Exception("Browser initialization failed")
            
            logger.info("Browser controller initialized")
            
            # All components ready
            self.update_status("Ready - Say 'Hey Maya'", 'listening')
            
            # Start voice listening loop
            await self._voice_listening_loop()
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            self.update_status("Initialization Failed", 'error')
            
            rumps.notification(
                title="VoiceNav Error",
                subtitle="Initialization failed",
                message=str(e)
            )
    
    async def _voice_listening_loop(self):
        """Main voice listening and command processing loop"""
        logger.info("Voice listening loop started")
        
        while self.is_voice_active:
            try:
                # Update status to show listening
                if not self.is_maya_listening:
                    self.update_status("Listening for 'Hey Maya'", 'listening')
                    self.is_maya_listening = True
                
                # Listen for Maya wake word + command
                result = self.maya.listen_once()
                
                if result and result.get('raw_text'):
                    command_text = result.get('raw_text', '').strip()
                    
                    if command_text:
                        logger.info(f"Processing command: '{command_text}'")
                        
                        # Update status to show processing
                        self.update_status(f"Processing: {command_text[:20]}...", 'processing')
                        
                        # Parse the command (Stage 2)
                        parsed_command = self.parser.parse(command_text)
                        
                        logger.info(f"Parsed intent: {parsed_command['intent']}")
                        
                        # Update status to show execution
                        self.update_status("Executing command...", 'speaking')
                        
                        # Execute browser action (Stage 2)
                        success = await self.browser.execute_command(parsed_command)
                        
                        if success:
                            logger.info("Command executed successfully")
                            self.update_status("Command completed", 'idle')
                        else:
                            logger.warning("Command execution failed")
                            self.update_status("Command failed", 'error')
                        
                        # Brief pause before returning to listening
                        await asyncio.sleep(1)
                        self.is_maya_listening = False
                
                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Voice loop error: {e}")
                self.update_status("Voice Error", 'error')
                await asyncio.sleep(1)
        
        logger.info("Voice listening loop stopped")
        self.update_status("Stopped", 'stopped')
    
    @rumps.clicked("Stop Voice Control")
    def stop_voice_control(self, _):
        """Stop Maya voice control system"""
        if not self.is_voice_active:
            return
        
        logger.info("Stopping voice control...")
        self.update_status("Stopping...", 'processing')
        
        try:
            # Stop voice system
            self.is_voice_active = False
            self.is_maya_listening = False
            
            # Cleanup components
            if self.maya:
                try:
                    self.maya.cleanup()
                except:
                    pass
            
            if self.browser:
                try:
                    # Schedule cleanup in the async loop
                    if self.loop and not self.loop.is_closed():
                        asyncio.run_coroutine_threadsafe(
                            self.browser.cleanup(),
                            self.loop
                        )
                except:
                    pass
            
            # Update menu state
            self.start_item.set_callback(self.start_voice_control)  # Enable start
            self.stop_item.set_callback(None)  # Disable stop
            
            self.update_status("Stopped", 'stopped')
            
            # Show stop notification
            rumps.notification(
                title="VoiceNav Stopped",
                subtitle="Voice control deactivated",
                message="Click 'Start Voice Control' to resume"
            )
            
        except Exception as e:
            logger.error(f"Failed to stop voice control: {e}")
            self.update_status("Stop Failed", 'error')
    
    @rumps.clicked("Mute Maya")
    def toggle_mute(self, sender):
        """Toggle Maya voice feedback mute"""
        # This would toggle Maya's speech output
        # For now, just toggle the menu item text
        if sender.title == "Mute Maya":
            sender.title = "Unmute Maya"
            rumps.notification(
                title="Maya Muted",
                subtitle="Voice feedback disabled",
                message=""
            )
        else:
            sender.title = "Mute Maya"
            rumps.notification(
                title="Maya Unmuted", 
                subtitle="Voice feedback enabled",
                message=""
            )
    
    @rumps.clicked("Test Maya Voice")
    def test_maya_voice(self, _):
        """Test Maya voice feedback"""
        try:
            # Test macOS say command
            subprocess.run(['say', '-v', 'Samantha', 'Hello! Maya voice test successful.'], check=True)
            
            rumps.notification(
                title="Voice Test",
                subtitle="Maya voice test completed",
                message=""
            )
            
        except Exception as e:
            logger.error(f"Voice test failed: {e}")
            
            rumps.notification(
                title="Voice Test Failed",
                subtitle="Maya voice test failed",
                message=str(e)
            )
    
    @rumps.clicked("Emergency Stop")
    def emergency_stop(self, _):
        """Emergency stop all VoiceNav operations"""
        logger.warning("Emergency stop activated")
        
        # Force stop everything
        self.is_voice_active = False
        self.is_maya_listening = False
        
        # Update status
        self.update_status("Emergency Stop", 'error')
        
        # Update menu
        self.start_item.set_callback(self.start_voice_control)
        self.stop_item.set_callback(None)
        
        rumps.notification(
            title="Emergency Stop",
            subtitle="All VoiceNav operations stopped",
            message="Click 'Start Voice Control' to resume",
            
        )
    
    @rumps.clicked("Voice Commands Help")
    def show_help(self, _):
        """Show voice commands help"""
        help_text = """
VoiceNav Voice Commands:

• "Hey Maya, open [website]" - Navigate to website
• "Hey Maya, click [element]" - Click page element  
• "Hey Maya, scroll up/down" - Scroll page
• "Hey Maya, go back" - Browser back
• "Hey Maya, go forward" - Browser forward
• "Hey Maya, refresh" - Reload page
• "Hey Maya, read page" - Read page content
• "Hey Maya, help" - List commands
• "Hey Maya, stop" - Stop VoiceNav

Examples:
• "Hey Maya, open google"
• "Hey Maya, click login button"
• "Hey Maya, scroll down"
"""
        
        # Show help in notification (macOS limitation)
        rumps.notification(
            title="VoiceNav Commands",
            subtitle="Voice commands available",
            message="Check console for full command list",
            
        )
        
        # Print to console for full details
        print(help_text)
        logger.info("Help displayed")
    
    @rumps.clicked("About VoiceNav")
    def show_about(self, _):
        """Show about information"""
        about_text = """
VoiceNav v0.1.0

Voice-controlled browser automation for macOS
Powered by Maya AI Assistant + OpenAI Whisper

Components:
• Stage 1: Maya Voice Assistant (Whisper Recognition)
• Stage 2: Command Parser + Browser Control
• Stage 3: Menu Bar Interface

Created for hands-free web browsing accessibility.
"""
        
        rumps.notification(
            title="About VoiceNav",
            subtitle="Voice-controlled browser automation",
            message="v0.1.0 - Maya AI Assistant",
            
        )
        
        print(about_text)
        logger.info("About displayed")
    
    @rumps.clicked("Settings")
    def show_settings(self, _):
        """Show settings panel"""
        # For now, just show notification
        # In future, could open a separate settings window
        
        rumps.notification(
            title="Settings",
            subtitle="Settings panel",
            message="Advanced settings via config.yaml",
            
        )
        
        # Could open config file in default editor
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "config.yaml"
            )
            subprocess.run(['open', '-t', config_path])
        except:
            pass
        
        logger.info("Settings accessed")
    
    def run(self):
        """Run the menu bar application"""
        logger.info("Starting VoiceNav menu bar application")
        
        # Show startup notification
        rumps.notification(
            title="VoiceNav Ready",
            subtitle="Menu bar application started",
            message="Click the microphone icon to control",
            
        )
        
        # Start the rumps app (this blocks)
        super(VoiceNavMenuBar, self).run()


def main():
    """Main entry point for menu bar application"""
    try:
        app = VoiceNavMenuBar()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 VoiceNav menu bar stopped")
    except Exception as e:
        print(f"❌ Menu bar error: {e}")
        logger.error(f"Menu bar error: {e}")


if __name__ == "__main__":
    main()
