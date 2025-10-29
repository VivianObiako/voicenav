"""
VoiceNav Browser Control
Executes parsed commands in actual browser using Playwright
"""

import asyncio
import subprocess
import time
from datetime import datetime
from typing import Dict, Any, Optional
import sys
import os

try:
    from playwright.async_api import async_playwright, Browser, Page, ElementHandle
except ImportError:
    print("⚠️  Playwright not installed. Run: pip install playwright && playwright install chromium")
    async_playwright = None

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.logger import setup_logger

# Initialize logger
logger = setup_logger("browser_control")


class BrowserController:
    """
    Controls web browser through Playwright for voice commands
    
    Features:
    - Browser initialization and management
    - URL navigation with Maya feedback
    - Element clicking with visual highlighting
    - Page scrolling with confirmation
    - Content reading with text extraction
    - Navigation controls (back/forward)
    """
    
    def __init__(self):
        """Initialize browser controller"""
        self.playwright = None
        self.browser = None
        self.page = None
        self.is_initialized = False
        logger.info("BrowserController initialized")
    
    async def initialize(self) -> bool:
        """
        Initialize Playwright browser
        
        Returns:
            bool: Success status
        """
        if async_playwright is None:
            logger.error("Playwright not available")
            return False
        
        try:
            logger.info("Starting Playwright browser...")
            self.playwright = await async_playwright().start()
            
            # Launch Chromium in headed mode (visible) with macOS-specific settings
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Show browser window
                slow_mo=100,     # Add small delay between actions for stability
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--no-first-run'
                ]
            )
            
            # Create new page
            self.page = await self.browser.new_page()
            
            # Set viewport
            await self.page.set_viewport_size({"width": 1280, "height": 720})
            
            # Set user agent to avoid bot detection
            await self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            self.is_initialized = True
            logger.info("Browser initialized successfully")
            
            # Maya announces browser is ready
            self._speak("Browser ready")
            
            return True
            
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
    
    async def open_url(self, url: str, original_input: str = "") -> bool:
        """
        Navigate to URL
        
        Args:
            url (str): URL to navigate to
            original_input (str): Original user input for feedback
            
        Returns:
            bool: Success status
        """
        if not self.is_initialized:
            await self.initialize()
        
        if not self.page:
            logger.error("No page available")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info(f"Navigating to: {url}")
            
            # Navigate to URL
            await self.page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Get domain name for feedback
            domain = url.replace('https://', '').replace('http://', '').split('/')[0]
            domain = domain.replace('www.', '')
            
            # Maya provides feedback
            if original_input and original_input.lower() != domain:
                self._speak(f"Opened {original_input}")
            else:
                self._speak(f"Opened {domain}")
            
            logger.info(f"Successfully navigated to {url}")
            return True
            
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            self._speak("Sorry, I couldn't open that page")
            return False
    
    async def click_element(self, element_desc: Dict[str, Any]) -> bool:
        """
        Click element based on description
        
        Args:
            element_desc (dict): Element description from parser
            
        Returns:
            bool: Success status
        """
        if not self.page:
            logger.error("No page available")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info(f"Looking for element: {element_desc}")
            
            element = await self._find_element(element_desc)
            
            if element:
                # Highlight element briefly
                await self._highlight_element(element)
                
                # Click the element
                await element.click()
                
                # Maya provides feedback
                element_name = element_desc.get('text', 'element')
                self._speak(f"Clicked {element_name}")
                
                logger.info(f"Successfully clicked element: {element_desc}")
                return True
            else:
                logger.warning(f"Element not found: {element_desc}")
                self._speak("I couldn't find that element")
                return False
                
        except Exception as e:
            logger.error(f"Click failed: {e}")
            self._speak("Sorry, I couldn't click that")
            return False
    
    async def _find_element(self, element_desc: Dict[str, Any]) -> Optional[ElementHandle]:
        """
        Find element using multiple strategies
        
        Args:
            element_desc (dict): Element description
            
        Returns:
            ElementHandle or None: Found element
        """
        if not self.page:
            return None
        
        text = element_desc.get('text', '')
        element_type = element_desc.get('type', 'any')
        
        # Strategy 1: Role-based selectors (most reliable)
        if element_type == 'button':
            selectors = [
                f'button:has-text("{text}")',
                f'[role="button"]:has-text("{text}")',
                f'input[type="button"][value*="{text}"]',
                f'input[type="submit"][value*="{text}"]'
            ]
        elif element_type == 'link':
            selectors = [
                f'a:has-text("{text}")',
                f'[role="link"]:has-text("{text}")'
            ]
        elif element_type == 'input':
            purpose = element_desc.get('attributes', {}).get('purpose', '')
            if purpose == 'search':
                selectors = [
                    'input[type="search"]',
                    'input[name*="search"]',
                    'input[placeholder*="search"]',
                    '[role="searchbox"]'
                ]
            else:
                selectors = [
                    f'input[placeholder*="{text}"]',
                    f'input[name*="{text}"]',
                    f'label:has-text("{text}") + input'
                ]
        else:
            # Generic text search
            selectors = [
                f'text="{text}"',
                f'[aria-label*="{text}"]',
                f'[title*="{text}"]',
                f'*:has-text("{text}")'
            ]
        
        # Try each selector
        for selector in selectors:
            try:
                element = await self.page.query_selector(selector)
                if element:
                    logger.debug(f"Found element with selector: {selector}")
                    return element
            except Exception as e:
                logger.debug(f"Selector failed: {selector} - {e}")
                continue
        
        # Strategy 2: Partial text match
        if text:
            try:
                elements = await self.page.query_selector_all(f'*:has-text("{text}")')
                for element in elements:
                    if await element.is_visible():
                        return element
            except:
                pass
        
        return None
    
    async def _highlight_element(self, element: ElementHandle):
        """
        Briefly highlight element with yellow border
        
        Args:
            element (ElementHandle): Element to highlight
        """
        try:
            # Add yellow border
            await element.evaluate('el => el.style.border = "3px solid yellow"')
            
            # Wait 1 second
            await asyncio.sleep(1)
            
            # Remove border
            await element.evaluate('el => el.style.border = ""')
            
        except Exception as e:
            logger.debug(f"Highlight failed: {e}")
    
    async def scroll_page(self, direction: str, amount: int = 300) -> bool:
        """
        Scroll page up or down
        
        Args:
            direction (str): 'up' or 'down'
            amount (int): Pixels to scroll
            
        Returns:
            bool: Success status
        """
        if not self.page:
            logger.error("No page available")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info(f"Scrolling {direction} by {amount}px")
            
            if direction == 'down':
                await self.page.evaluate(f'window.scrollBy(0, {amount})')
            else:  # up
                await self.page.evaluate(f'window.scrollBy(0, -{amount})')
            
            # Maya provides feedback
            self._speak(f"Scrolling {direction}")
            
            logger.info(f"Successfully scrolled {direction}")
            return True
            
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
        if not self.page:
            logger.error("No page available")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info("Navigating back")
            await self.page.go_back(wait_until="networkidle")
            
            # Maya provides feedback
            self._speak("Going back")
            
            logger.info("Successfully navigated back")
            return True
            
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
        if not self.page:
            logger.error("No page available")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info("Navigating forward")
            await self.page.go_forward(wait_until="networkidle")
            
            # Maya provides feedback
            self._speak("Going forward")
            
            logger.info("Successfully navigated forward")
            return True
            
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
        if not self.page:
            logger.error("No page available")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info("Refreshing page")
            await self.page.reload(wait_until="networkidle")
            
            # Maya provides feedback
            self._speak("Page refreshed")
            
            logger.info("Successfully refreshed page")
            return True
            
        except Exception as e:
            logger.error(f"Refresh failed: {e}")
            self._speak("Sorry, I couldn't refresh the page")
            return False
    
    async def read_content(self, target: str = 'main') -> bool:
        """
        Extract and read main page content aloud
        
        Args:
            target (str): Content target ('main', 'all', 'title')
            
        Returns:
            bool: Success status
        """
        if not self.page:
            logger.error("No page available")
            self._speak("Browser not ready")
            return False
        
        try:
            logger.info(f"Reading page content: {target}")
            
            content = ""
            
            if target == 'title':
                content = await self.page.title()
            elif target == 'main':
                # Try to extract main content
                selectors = [
                    'main',
                    'article', 
                    '[role="main"]',
                    '.content',
                    '#content',
                    '.post-content',
                    '.entry-content'
                ]
                
                for selector in selectors:
                    try:
                        element = await self.page.query_selector(selector)
                        if element:
                            content = await element.inner_text()
                            break
                    except:
                        continue
                
                # Fallback: get body text but limit it
                if not content:
                    content = await self.page.evaluate('''
                        () => {
                            // Remove script and style elements
                            const scripts = document.querySelectorAll('script, style, nav, header, footer, aside');
                            scripts.forEach(el => el.remove());
                            
                            // Get main content
                            const main = document.querySelector('main, article, .content, #content');
                            if (main) return main.innerText;
                            
                            // Fallback to body but limit
                            return document.body.innerText.substring(0, 1000);
                        }
                    ''')
            
            if content:
                # Clean up the content
                content = content.strip()
                
                # Limit content length for reading
                if len(content) > 500:
                    content = content[:500] + "..."
                
                # Maya reads the content
                self._speak(content)
                
                logger.info("Successfully read page content")
                return True
            else:
                self._speak("I couldn't find any content to read")
                return False
                
        except Exception as e:
            logger.error(f"Read content failed: {e}")
            self._speak("Sorry, I couldn't read the page")
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
                self._speak("I can open websites, click elements, scroll pages, go back, read content, and more. Try saying 'open google' or 'click search box'.")
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
        """Clean up browser resources"""
        try:
            if self.page:
                await self.page.close()
                self.page = None
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            self.is_initialized = False
            logger.info("Browser cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


async def main():
    """Test the browser controller directly"""
    print("VoiceNav Browser Controller Test")
    print("="*40)
    
    controller = BrowserController()
    
    try:
        # Initialize browser
        print("🌐 Initializing browser...")
        success = await controller.initialize()
        
        if not success:
            print("❌ Browser initialization failed")
            return
        
        print("✅ Browser ready!")
        
        # Test navigation
        print("\n🔗 Testing navigation...")
        await controller.open_url("https://example.com", "example")
        
        # Wait a bit
        await asyncio.sleep(2)
        
        # Test scrolling
        print("\n📜 Testing scroll...")
        await controller.scroll_page('down', 300)
        
        await asyncio.sleep(1)
        
        # Test back navigation
        print("\n⬅️ Testing back navigation...")
        await controller.go_back()
        
        print("\n✅ All browser actions completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        await controller.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
