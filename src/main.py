"""
VoiceNav Main Application
Entry point for the voice-controlled browser automation system
Integrates Maya voice assistant with browser control
"""

import sys
import os
import asyncio
import threading
import queue
import signal
from datetime import datetime

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.logger import setup_logger
from src.input.voice_listener import create_voice_listener
from src.brain.command_parser import CommandParser
from src.actions.applescript_browser import AppleScriptBrowserController

# Initialize logger
logger = setup_logger("main")


class VoiceNavApp:
    """
    Main VoiceNav Application
    
    Integrates:
    - Maya voice assistant (Stage 1)
    - Command parsing (Stage 2)
    - Browser control (Stage 2)
    """
    
    def __init__(self):
        """Initialize VoiceNav application"""
        self.maya = None
        self.parser = None
        self.browser = None
        self.command_queue = queue.Queue()
        self.is_running = False
        self.voice_thread = None
        
        logger.info("VoiceNavApp initialized")
    
    async def initialize(self) -> bool:
        """
        Initialize all components
        
        Returns:
            bool: Success status
        """
        try:
            print("🎤 Initializing Maya voice assistant...")
            
            # Initialize Maya (Stage 1 - working system)
            self.maya = create_voice_listener(wake_word="hey maya")
            print("✅ Maya ready!")
            
            # Initialize command parser (Stage 2)
            print("🧠 Initializing command parser...")
            self.parser = CommandParser()
            print("✅ Command parser ready!")
            
            # Initialize browser controller (Stage 2) - Auto-detect default browser
            print("🌐 Initializing browser controller...")
            self.browser = AppleScriptBrowserController("auto")
            browser_ready = await self.browser.initialize()
            
            if not browser_ready:
                print("❌ Browser initialization failed")
                return False
            
            print("✅ Browser ready!")
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            print(f"❌ Initialization failed: {e}")
            return False
    
    def voice_listener_thread(self):
        """
        Voice listening thread
        Runs Maya voice detection in background
        """
        logger.info("Voice listener thread started")
        
        try:
            while self.is_running:
                # Listen for Maya wake word + command
                result = self.maya.listen_once()
                
                if result and result.get('raw_text'):
                    # Put command in queue for main thread to process
                    self.command_queue.put(result)
                
                # Small delay to prevent CPU spinning
                if self.is_running:
                    import time
                    time.sleep(0.1)
                    
        except Exception as e:
            logger.error(f"Voice listener error: {e}")
        
        logger.info("Voice listener thread stopped")
    
    async def process_commands(self):
        """
        Process voice commands from queue
        Main application loop
        """
        logger.info("Command processing started")
        
        while self.is_running:
            try:
                # Check for voice commands (non-blocking)
                try:
                    voice_result = self.command_queue.get_nowait()
                    
                    command_text = voice_result.get('raw_text', '').strip()
                    if command_text:
                        logger.info(f"Processing command: '{command_text}'")
                        
                        # Parse the command (Stage 2)
                        parsed_command = self.parser.parse(command_text)
                        
                        logger.info(f"Parsed intent: {parsed_command['intent']}")
                        
                        # Execute browser action (Stage 2)
                        success = await self.browser.execute_command(parsed_command)
                        
                        if success:
                            logger.info("Command executed successfully")
                        else:
                            logger.warning("Command execution failed")
                    
                except queue.Empty:
                    # No commands in queue, continue
                    pass
                
                # Small async delay
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Command processing error: {e}")
                await asyncio.sleep(1)  # Longer delay on error
        
        logger.info("Command processing stopped")
    
    async def run(self):
        """
        Run the main application
        """
        print("\n🎤 VoiceNav - Voice-Controlled Browser")
        print("=" * 50)
        print("Powered by Maya AI Assistant + Whisper Recognition")
        print("=" * 50)
        
        # Initialize components
        success = await self.initialize()
        if not success:
            print("❌ Failed to initialize VoiceNav")
            return
        
        print(f"\n🎉 VoiceNav is ready!")
        print(f"🎤 Say 'Hey Maya' followed by your command")
        print(f"📝 Example: 'Hey Maya, open google'")
        print(f"🆘 Say 'Hey Maya, help' for available commands")
        print(f"🛑 Press Ctrl+C to stop")
        print("-" * 50)
        
        # Start voice listening in background thread
        self.is_running = True
        self.voice_thread = threading.Thread(target=self.voice_listener_thread, daemon=True)
        self.voice_thread.start()
        
        try:
            # Run main command processing loop
            await self.process_commands()
            
        except KeyboardInterrupt:
            print("\n🛑 Shutting down VoiceNav...")
            logger.info("Shutdown requested by user")
        
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Clean up all resources"""
        logger.info("Starting cleanup...")
        
        # Stop voice listening
        self.is_running = False
        
        # Wait for voice thread to finish (with timeout)
        if self.voice_thread and self.voice_thread.is_alive():
            self.voice_thread.join(timeout=2)
        
        # Cleanup Maya
        if self.maya:
            try:
                self.maya.cleanup()
            except:
                pass
        
        # Cleanup browser
        if self.browser:
            await self.browser.cleanup()
        
        print("✅ VoiceNav shutdown complete")
        logger.info("Cleanup completed")


async def main():
    """Main application entry point"""
    logger.info("VoiceNav starting...")
    
    # Create and run the application
    app = VoiceNavApp()
    
    # Handle Ctrl+C gracefully
    def signal_handler(signum, frame):
        print("\n🛑 Interrupted! Shutting down...")
        app.is_running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        await app.run()
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Application error: {e}")


def run_voicenav():
    """
    Synchronous entry point for VoiceNav
    Handles the async main loop
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logger.error(f"Fatal error: {e}")


if __name__ == "__main__":
    run_voicenav()
