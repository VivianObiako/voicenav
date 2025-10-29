"""
VoiceNav AppleScript Browser Control
Controls user's actual browser (Safari/Chrome) via native macOS AppleScript
"""

import subprocess
import time
from datetime import datetime
from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.logger import setup_logger

# Initialize logger
logger = setup_logger("applescript_browser")


class AppleScriptBrowserController:
    """
    Controls web browser through AppleScript for voice commands
    
    Features:
    - Native macOS browser control (Safari/Chrome)
    - Uses your existing browser, not a separate process
    - Maya voice feedback for all actions
    - Cross-browser compatibility
    - Lightweight and reliable
    """
    
    def __init__(self, browser_app="Safari"):
        """
        Initialize AppleScript browser controller
        
        Args:
            browser_app (str): Browser to control ("Safari" or "Google Chrome")
        """
        self.browser_app = browser_app
        self.is_initialized = False
        self.current_url = None
        
        # Validate browser choice
        if browser_app not in ["Safari", "Google Chrome"]:
            logger.warning(f"Unknown browser: {browser_app}, defaulting to Safari")
            self.browser_app = "Safari"
        
        logger.info(f"AppleScriptBrowserController initialized for {self.browser_app}")
    
    async def initialize(self) -> bool:
        """
        Initialize browser controller
        
        Returns:
            bool: Success status
        """
        try:
            logger.info(f"Initializing {self.browser_app} control...")
            
            # Test if browser is available
            test_script = f'''
            tell application "{self.browser_app}"
                return name
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', test_script], 
                capture_output=True, 
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                self.is_initialized = True
                logger.info(f"{self.browser_app} control initialized successfully")
                self._speak(f"{self.browser_app} ready")
                return True
            else:
                logger.error(f"Failed to initialize {self.browser_app}: {result.stderr}")
                self._speak(f"Could not initialize {self.browser_app}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"Timeout initializing {self.browser_app}")
            self._speak("Browser initialization timed out")
            return False
        except Exception as e:
            logger.error(f"Browser initialization failed: {e}")
            self._speak("Browser initialization failed")
            return False
    
    def _speak(self, text: str):
        """
        Use Maya's voice to provide feedback
        
        Args:
            text (str): Text for Maya to speak
        """
        try:
            # Use macOS built-in 'say' command with Samantha voice (Maya's voice)
            subprocess.run(['say', '-v', 'Samantha', text], check=True)
            logger.info(f"Maya spoke: {text}")
        except subprocess.CalledProcessError:
            # Fallback to default voice
            try:
                subprocess.run(['say', text], check=True)
            except:
                print(f"🔊 Maya would say: {text}")
        except Exception as e:
            logger.error(f"TTS error: {e}")
            print(f"🔊 Maya would say: {text}")
    
    def _run_applescript(self, script: str, timeout: int = 10) -> tuple:
        """
        Run AppleScript and return result
        
        Args:
            script (str): AppleScript to execute
            timeout (int): Timeout in seconds
            
        Returns:
            tuple: (success: bool, output: str, error: str)
        """
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            output = result.stdout.strip()
            error = result.stderr.strip()
            
            if success:
                logger.debug(f"AppleScript success: {output}")
            else:
                logger.warning(f"AppleScript error: {error}")
            
            return success, output, error
            
        except subprocess.TimeoutExpired:
            logger.error(f"AppleScript timeout after {timeout}s")
            return False, "", "Script timed out"
        except Exception as e:
            logger.error(f"AppleScript execution error: {e}")
            return False, "", str(e)
    
    async def open_url(self, url: str, original_input: str = "") -> bool:
        """
        Navigate to URL in browser
        
        Args:
            url (str): URL to navigate to
            original_input (str): Original user input for feedback
            
        Returns:
            bool: Success status
        """
        if not self.is_initialized:
            await self.initialize()
        
        try:
            logger.info(f"Opening URL: {url}")
            
            # AppleScript to open URL
            if self.browser_app == "Safari":
                script = f'''
                tell application "Safari"
                    activate
                    open location "{url}"
                end tell
                '''
            else:  # Google Chrome
                script = f'''
                tell application "Google Chrome"
                    activate
                    open location "{url}"
                end tell
                '''
            
            success, output, error = self._run_applescript(script)
            
            if success:
                self.current_url = url
                
                # Get domain name for feedback
                domain = url.replace('https://', '').replace('http://', '').split('/')[0]
                domain = domain.replace('www.', '')
                
                # Maya provides feedback
                if original_input and original_input.lower() != domain:
                    self._speak(f"Opened {original_input}")
                else:
                    self._speak(f"Opened {domain}")
                
                logger.info(f"Successfully opened {url}")
                return True
            else:
                logger.error(f"Failed to open URL: {error}")
                self._speak("Sorry, I couldn't open that page")
                return False
                
        except Exception as e:
            logger.error(f"URL opening failed: {e}")
            self._speak("Sorry, I couldn't open that page")
            return False
    
    async def scroll_page(self, direction: str, amount: int = 300) -> bool:
        """
        Scroll page up or down
        
        Args:
            direction (str): 'up' or 'down'
            amount (int): Scroll amount (AppleScript uses page units)
            
        Returns:
            bool: Success status
        """
        if not self.is_initialized:
            logger.error("Browser not initialized")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info(f"Scrolling {direction}")
            
            # Convert amount to page units (AppleScript scrolls by pages)
            pages = max(1, amount // 300)  # 300px ≈ 1 page
            
            if self.browser_app == "Safari":
                if direction == 'down':
                    script = f'''
                    tell application "Safari"
                        tell front document
                            repeat {pages} times
                                do JavaScript "window.scrollBy(0, 300);"
                            end repeat
                        end tell
                    end tell
                    '''
                else:  # up
                    script = f'''
                    tell application "Safari"
                        tell front document
                            repeat {pages} times
                                do JavaScript "window.scrollBy(0, -300);"
                            end repeat
                        end tell
                    end tell
                    '''
            else:  # Google Chrome
                if direction == 'down':
                    script = f'''
                    tell application "Google Chrome"
                        tell active tab of front window
                            repeat {pages} times
                                execute javascript "window.scrollBy(0, 300);"
                            end repeat
                        end tell
                    end tell
                    '''
                else:  # up
                    script = f'''
                    tell application "Google Chrome"
                        tell active tab of front window
                            repeat {pages} times
                                execute javascript "window.scrollBy(0, -300);"
                            end repeat
                        end tell
                    end tell
                    '''
            
            success, output, error = self._run_applescript(script)
            
            if success:
                self._speak(f"Scrolling {direction}")
                logger.info(f"Successfully scrolled {direction}")
                return True
            else:
                logger.error(f"Scroll failed: {error}")
                self._speak("Sorry, I couldn't scroll")
                return False
                
        except Exception as e:
            logger.error(f"Scroll failed: {e}")
            self._speak("Sorry, I couldn't scroll")
            return False
    
    async def go_back(self) -> bool:
        """
        Navigate back in browser history
        
        Returns:
            bool: Success status
        """
        if not self.is_initialized:
            logger.error("Browser not initialized")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info("Navigating back")
            
            if self.browser_app == "Safari":
                script = '''
                tell application "Safari"
                    tell front document
                        go back
                    end tell
                end tell
                '''
            else:  # Google Chrome
                script = '''
                tell application "Google Chrome"
                    tell active tab of front window
                        go back
                    end tell
                end tell
                '''
            
            success, output, error = self._run_applescript(script)
            
            if success:
                self._speak("Going back")
                logger.info("Successfully navigated back")
                return True
            else:
                logger.error(f"Go back failed: {error}")
                self._speak("Sorry, I couldn't go back")
                return False
                
        except Exception as e:
            logger.error(f"Go back failed: {e}")
            self._speak("Sorry, I couldn't go back")
            return False
    
    async def go_forward(self) -> bool:
        """
        Navigate forward in browser history
        
        Returns:
            bool: Success status
        """
        if not self.is_initialized:
            logger.error("Browser not initialized")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info("Navigating forward")
            
            if self.browser_app == "Safari":
                script = '''
                tell application "Safari"
                    tell front document
                        go forward
                    end tell
                end tell
                '''
            else:  # Google Chrome
                script = '''
                tell application "Google Chrome"
                    tell active tab of front window
                        go forward
                    end tell
                end tell
                '''
            
            success, output, error = self._run_applescript(script)
            
            if success:
                self._speak("Going forward")
                logger.info("Successfully navigated forward")
                return True
            else:
                logger.error(f"Go forward failed: {error}")
                self._speak("Sorry, I couldn't go forward")
                return False
                
        except Exception as e:
            logger.error(f"Go forward failed: {e}")
            self._speak("Sorry, I couldn't go forward")
            return False
    
    async def refresh_page(self) -> bool:
        """
        Refresh the current page
        
        Returns:
            bool: Success status
        """
        if not self.is_initialized:
            logger.error("Browser not initialized")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info("Refreshing page")
            
            if self.browser_app == "Safari":
                script = '''
                tell application "Safari"
                    tell front document
                        reload
                    end tell
                end tell
                '''
            else:  # Google Chrome
                script = '''
                tell application "Google Chrome"
                    tell active tab of front window
                        reload
                    end tell
                end tell
                '''
            
            success, output, error = self._run_applescript(script)
            
            if success:
                self._speak("Page refreshed")
                logger.info("Successfully refreshed page")
                return True
            else:
                logger.error(f"Refresh failed: {error}")
                self._speak("Sorry, I couldn't refresh the page")
                return False
                
        except Exception as e:
            logger.error(f"Refresh failed: {e}")
            self._speak("Sorry, I couldn't refresh the page")
            return False
    
    async def read_content(self, target: str = 'main') -> bool:
        """
        Extract and read page content aloud
        
        Args:
            target (str): Content target ('main', 'title')
            
        Returns:
            bool: Success status
        """
        if not self.is_initialized:
            logger.error("Browser not initialized")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info(f"Reading page content: {target}")
            
            if target == 'title':
                # Get page title
                if self.browser_app == "Safari":
                    script = '''
                    tell application "Safari"
                        tell front document
                            return name
                        end tell
                    end tell
                    '''
                else:  # Google Chrome
                    script = '''
                    tell application "Google Chrome"
                        tell active tab of front window
                            return title
                        end tell
                    end tell
                    '''
                
                success, output, error = self._run_applescript(script)
                
                if success and output:
                    self._speak(f"Page title: {output}")
                    return True
            
            else:  # main content
                # Get page content via JavaScript
                if self.browser_app == "Safari":
                    script = '''
                    tell application "Safari"
                        tell front document
                            return do JavaScript "
                                var content = '';
                                var main = document.querySelector('main, article, .content, #content');
                                if (main) {
                                    content = main.innerText;
                                } else {
                                    content = document.body.innerText;
                                }
                                content.substring(0, 500);
                            "
                        end tell
                    end tell
                    '''
                else:  # Google Chrome
                    script = '''
                    tell application "Google Chrome"
                        tell active tab of front window
                            return execute javascript "
                                var content = '';
                                var main = document.querySelector('main, article, .content, #content');
                                if (main) {
                                    content = main.innerText;
                                } else {
                                    content = document.body.innerText;
                                }
                                content.substring(0, 500);
                            "
                        end tell
                    end tell
                    '''
                
                success, output, error = self._run_applescript(script, timeout=15)
                
                if success and output:
                    # Clean up the content
                    content = output.strip()
                    if len(content) > 500:
                        content = content[:500] + "..."
                    
                    if content:
                        self._speak(content)
                        logger.info("Successfully read page content")
                        return True
            
            # Fallback
            self._speak("I couldn't find any content to read")
            return False
                
        except Exception as e:
            logger.error(f"Read content failed: {e}")
            self._speak("Sorry, I couldn't read the page")
            return False
    
    async def click_element(self, element_desc: Dict[str, Any]) -> bool:
        """
        Click element (limited AppleScript support)
        
        Args:
            element_desc (dict): Element description
            
        Returns:
            bool: Success status
        """
        # AppleScript has limited element clicking capabilities
        # This is a basic implementation
        
        logger.info(f"Attempting to click element: {element_desc}")
        
        element_text = element_desc.get('text', '')
        
        if not element_text:
            self._speak("I need more specific information to click that element")
            return False
        
        try:
            # Try to click by text content (basic implementation)
            if self.browser_app == "Safari":
                script = f'''
                tell application "Safari"
                    tell front document
                        do JavaScript "
                            var elements = document.querySelectorAll('*');
                            for (var i = 0; i < elements.length; i++) {{
                                if (elements[i].innerText && elements[i].innerText.toLowerCase().includes('{element_text.lower()}')) {{
                                    elements[i].click();
                                    break;
                                }}
                            }}
                        "
                    end tell
                end tell
                '''
            else:  # Google Chrome
                script = f'''
                tell application "Google Chrome"
                    tell active tab of front window
                        execute javascript "
                            var elements = document.querySelectorAll('*');
                            for (var i = 0; i < elements.length; i++) {{
                                if (elements[i].innerText && elements[i].innerText.toLowerCase().includes('{element_text.lower()}')) {{
                                    elements[i].click();
                                    break;
                                }}
                            }}
                        "
                    end tell
                end tell
                '''
            
            success, output, error = self._run_applescript(script)
            
            if success:
                self._speak(f"Clicked {element_text}")
                logger.info(f"Successfully clicked element: {element_text}")
                return True
            else:
                logger.warning(f"Click failed: {error}")
                self._speak("I couldn't find that element to click")
                return False
                
        except Exception as e:
            logger.error(f"Click failed: {e}")
            self._speak("Sorry, I couldn't click that")
            return False
    
    async def execute_command(self, command: Dict[str, Any]) -> bool:
        """
        Execute a parsed command
        
        Args:
            command (dict): Parsed command from CommandParser
            
        Returns:
            bool: Success status
        """
        intent = command.get('intent')
        params = command.get('params', {})
        
        logger.info(f"Executing command: {intent}")
        
        try:
            if intent == 'open_url':
                return await self.open_url(
                    params['url'], 
                    params.get('original_input', '')
                )
            
            elif intent == 'click_element':
                return await self.click_element(params)
            
            elif intent == 'scroll_down':
                return await self.scroll_page('down', params.get('amount', 300))
            
            elif intent == 'scroll_up':
                return await self.scroll_page('up', params.get('amount', 300))
            
            elif intent == 'go_back':
                return await self.go_back()
            
            elif intent == 'go_forward':
                return await self.go_forward()
            
            elif intent == 'refresh':
                return await self.refresh_page()
            
            elif intent == 'read_content':
                return await self.read_content(params.get('target', 'main'))
            
            elif intent == 'stop_action':
                self._speak("Stopping")
                return True
            
            elif intent == 'help':
                self._speak("I can open websites, scroll pages, go back and forward, refresh pages, and read content. Try saying 'open google' or 'scroll down'.")
                return True
            
            elif intent == 'unknown':
                suggestion = params.get('suggestion', '')
                if suggestion:
                    self._speak(suggestion)
                else:
                    self._speak("I didn't understand that command. Try saying 'help' for available commands.")
                return False
            
            else:
                self._speak(f"I don't know how to {intent} yet")
                return False
                
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            self._speak("Sorry, something went wrong")
            return False
    
    async def cleanup(self):
        """Clean up resources (minimal for AppleScript)"""
        self.is_initialized = False
        logger.info("AppleScript browser cleanup completed")


# Alias for compatibility with existing code
BrowserController = AppleScriptBrowserController


async def main():
    """Test the AppleScript browser controller"""
    print("VoiceNav AppleScript Browser Controller Test")
    print("="*50)
    
    # Test with Safari (change to "Google Chrome" if preferred)
    controller = AppleScriptBrowserController("Safari")
    
    try:
        # Initialize
        print("🍎 Initializing Safari control...")
        success = await controller.initialize()
        
        if not success:
            print("❌ Safari initialization failed")
            return
        
        print("✅ Safari ready!")
        
        # Test navigation
        print("\n🔗 Testing navigation...")
        await controller.open_url("https://example.com", "example")
        
        # Wait a bit
        time.sleep(3)
        
        # Test scrolling
        print("\n📜 Testing scroll...")
        await controller.scroll_page('down', 300)
        
        time.sleep(2)
        
        # Test reading content
        print("\n📖 Testing content reading...")
        await controller.read_content('title')
        
        print("\n✅ All AppleScript browser actions completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        await controller.cleanup()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
