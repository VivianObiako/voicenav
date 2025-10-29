"""
VoiceNav Command Parser
Interprets voice commands into actionable intents
"""

import re
from datetime import datetime
from typing import Dict, Any, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.logger import setup_logger

# Initialize logger
logger = setup_logger("command_parser")


class CommandParser:
    """
    Parses voice commands into structured actions for browser control
    
    Supports 8 core commands:
    1. "open [website]" / "go to [website]" → Open URL
    2. "click [element]" → Click described element
    3. "scroll down" → Scroll down page
    4. "scroll up" → Scroll up page
    5. "go back" → Browser back button
    6. "read page" → Read main content aloud
    7. "stop" → Stop current action
    8. "help" / "what can you do" → Show available commands
    """
    
    def __init__(self):
        """Initialize the command parser with patterns and URL mappings"""
        self.setup_patterns()
        self.setup_url_mappings()
        logger.info("CommandParser initialized")
    
    def setup_patterns(self):
        """Setup regex patterns for command recognition"""
        self.patterns = {
            # Open/navigate commands
            'open_url': [
                r'\b(?:open|go to|navigate to|visit)\s+(.+)',
                r'\b(?:load|browse to)\s+(.+)',
            ],
            
            # Click commands
            'click_element': [
                r'\b(?:click|tap|press)\s+(?:on\s+)?(.+)',
                r'\b(?:select|choose)\s+(.+)',
            ],
            
            # Scroll commands
            'scroll_down': [
                r'\b(?:scroll down|scroll|page down|go down)',
                r'\b(?:move down|down)',
            ],
            
            'scroll_up': [
                r'\b(?:scroll up|page up|go up)',
                r'\b(?:move up|up)',
            ],
            
            # Navigation commands
            'go_back': [
                r'\b(?:go back|back|previous|previous page)',
                r'\b(?:navigate back|return)',
            ],
            
            'go_forward': [
                r'\b(?:go forward|forward|next|next page)',
                r'\b(?:navigate forward|advance)',
            ],
            
            # Content commands
            'read_content': [
                r'\b(?:read|read page|read this|speak|speak page)',
                r'\b(?:tell me what|what does it say)',
            ],
            
            # Control commands
            'stop_action': [
                r'\b(?:stop|halt|cancel|quit|pause)',
                r'\b(?:enough|that\'s enough)',
            ],
            
            # Help commands
            'help': [
                r'\b(?:help|what can you do|commands|options)',
                r'\b(?:what commands|show commands|list commands)',
            ],
            
            # Refresh commands
            'refresh': [
                r'\b(?:refresh|reload|update page)',
                r'\b(?:refresh page|reload page)',
                r'\b(?:update page)',
            ]
        }
    
    def setup_url_mappings(self):
        """Setup common website URL mappings"""
        self.url_mappings = {
            # Popular sites
            'google': 'https://google.com',
            'youtube': 'https://youtube.com',
            'gmail': 'https://gmail.com',
            'reddit': 'https://reddit.com',
            'twitter': 'https://twitter.com',
            'facebook': 'https://facebook.com',
            'instagram': 'https://instagram.com',
            'linkedin': 'https://linkedin.com',
            'github': 'https://github.com',
            'stackoverflow': 'https://stackoverflow.com',
            
            # News sites
            'bbc': 'https://bbc.com',
            'cnn': 'https://cnn.com',
            'news': 'https://news.google.com',
            'reuters': 'https://reuters.com',
            
            # Shopping
            'amazon': 'https://amazon.com',
            'ebay': 'https://ebay.com',
            'walmart': 'https://walmart.com',
            
            # Entertainment
            'netflix': 'https://netflix.com',
            'spotify': 'https://spotify.com',
            'twitch': 'https://twitch.tv',
            
            # Productivity
            'docs': 'https://docs.google.com',
            'drive': 'https://drive.google.com',
            'calendar': 'https://calendar.google.com',
            'outlook': 'https://outlook.com',
            
            # Development
            'codepen': 'https://codepen.io',
            'replit': 'https://replit.com',
            'npmjs': 'https://npmjs.com',
        }
    
    def normalize_url(self, url_input: str) -> str:
        """
        Convert natural language to proper URL
        
        Args:
            url_input (str): User's URL input (e.g., "google", "reddit.com")
            
        Returns:
            str: Properly formatted URL
        """
        url_input = url_input.lower().strip()
        
        # Remove common phrases
        url_input = re.sub(r'\b(?:the|website|site|page)\b', '', url_input).strip()
        
        # Check direct mappings first
        if url_input in self.url_mappings:
            return self.url_mappings[url_input]
        
        # Handle partial matches (e.g., "google search" → "google")
        for site, url in self.url_mappings.items():
            if site in url_input or url_input in site:
                return url
        
        # If it looks like a domain, add https://
        if '.' in url_input and ' ' not in url_input:
            if not url_input.startswith(('http://', 'https://')):
                return f'https://{url_input}'
            return url_input
        
        # Default: Google search
        search_query = url_input.replace(' ', '+')
        return f'https://google.com/search?q={search_query}'
    
    def parse_element_description(self, description: str) -> Dict[str, Any]:
        """
        Parse element description into searchable attributes
        
        Args:
            description (str): Natural language element description
            
        Returns:
            dict: Structured element attributes
        """
        description = description.lower().strip()
        element = {
            'original': description,
            'type': None,
            'text': None,
            'attributes': {}
        }
        
        # Button patterns
        if any(word in description for word in ['button', 'btn']):
            element['type'] = 'button'
            # Extract button text
            text_match = re.search(r'(?:the\s+)?(.+?)\s+button', description)
            if text_match:
                element['text'] = text_match.group(1).strip()
            else:
                element['text'] = re.sub(r'\bbutton\b', '', description).strip()
        
        # Link patterns
        elif any(word in description for word in ['link', 'hyperlink']):
            element['type'] = 'link'
            text_match = re.search(r'(?:the\s+)?(.+?)\s+link', description)
            if text_match:
                element['text'] = text_match.group(1).strip()
            else:
                element['text'] = re.sub(r'\blink\b', '', description).strip()
        
        # Input patterns
        elif any(word in description for word in ['input', 'field', 'box', 'textbox']):
            element['type'] = 'input'
            if 'search' in description:
                element['attributes']['purpose'] = 'search'
            elif 'email' in description:
                element['attributes']['type'] = 'email'
            elif 'password' in description:
                element['attributes']['type'] = 'password'
            
            # Extract field name
            for keyword in ['search', 'email', 'password', 'username', 'name']:
                if keyword in description:
                    element['text'] = keyword
                    break
        
        # Generic text-based elements
        else:
            # Check for specific text content
            # Remove articles and common words
            clean_text = re.sub(r'\b(?:the|a|an|this|that)\b', '', description).strip()
            element['text'] = clean_text
            element['type'] = 'any'  # Will try multiple selectors
        
        # Color detection
        colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'black', 'white', 'gray', 'grey']
        for color in colors:
            if color in description:
                element['attributes']['color'] = color
                break
        
        # Position detection
        positions = ['top', 'bottom', 'left', 'right', 'center', 'first', 'last']
        for position in positions:
            if position in description:
                element['attributes']['position'] = position
                break
        
        logger.debug(f"Parsed element: {element}")
        return element
    
    def match_command_pattern(self, text: str) -> tuple:
        """
        Match text against command patterns
        
        Args:
            text (str): Input text to match
            
        Returns:
            tuple: (intent, matched_text) or (None, None)
        """
        text = text.lower().strip()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    # Return the matched groups if any, otherwise the full match
                    matched_text = match.groups()[0] if match.groups() else match.group(0)
                    logger.debug(f"Matched intent '{intent}' with pattern '{pattern}'")
                    return intent, matched_text
        
        return None, None
    
    def parse(self, command_text: str) -> Dict[str, Any]:
        """
        Parse a voice command into structured action
        
        Args:
            command_text (str): Raw voice command text
            
        Returns:
            dict: Structured command with intent, params, and metadata
        """
        logger.info(f"Parsing command: '{command_text}'")
        
        command = {
            'timestamp': datetime.now().isoformat(),
            'original': command_text,
            'intent': 'unknown',
            'params': {},
            'confidence': 0.0
        }
        
        if not command_text or not command_text.strip():
            command['intent'] = 'empty'
            return command
        
        # Match against patterns
        intent, matched_text = self.match_command_pattern(command_text)
        
        if intent:
            command['intent'] = intent
            command['confidence'] = 0.9  # High confidence for pattern matches
            
            # Parse parameters based on intent
            if intent == 'open_url':
                url = self.normalize_url(matched_text)
                command['params'] = {
                    'url': url,
                    'original_input': matched_text
                }
                
            elif intent == 'click_element':
                element = self.parse_element_description(matched_text)
                command['params'] = element
                
            elif intent in ['scroll_down', 'scroll_up']:
                direction = 'down' if 'down' in intent else 'up'
                command['params'] = {
                    'direction': direction,
                    'amount': 300  # Default scroll amount in pixels
                }
                
            elif intent in ['go_back', 'go_forward', 'refresh']:
                command['params'] = {}  # No additional params needed
                
            elif intent == 'read_content':
                command['params'] = {
                    'target': 'main'  # Read main content by default
                }
                
            elif intent in ['stop_action', 'help']:
                command['params'] = {}
                
        else:
            # No pattern matched - try to infer intent
            command['confidence'] = 0.3  # Lower confidence for inferred commands
            
            # Check for URLs in the text
            if any(tld in command_text.lower() for tld in ['.com', '.org', '.net', '.edu', '.gov']):
                command['intent'] = 'open_url'
                command['params'] = {
                    'url': self.normalize_url(command_text),
                    'original_input': command_text
                }
            
            # Check for common action words
            elif any(word in command_text.lower() for word in ['click', 'tap', 'press']):
                command['intent'] = 'click_element'
                # Extract everything after the action word
                for word in ['click', 'tap', 'press']:
                    if word in command_text.lower():
                        parts = command_text.lower().split(word, 1)
                        if len(parts) > 1:
                            element_desc = parts[1].strip()
                            command['params'] = self.parse_element_description(element_desc)
                            break
            
            else:
                command['intent'] = 'unknown'
                command['params'] = {'suggestion': 'Try saying "help" to see available commands'}
        
        logger.info(f"Parsed command: {command['intent']} with confidence {command['confidence']}")
        return command
    
    def get_available_commands(self) -> list:
        """
        Get list of available commands with descriptions
        
        Returns:
            list: Command descriptions
        """
        commands = [
            "Open website: 'open google' or 'go to youtube'",
            "Click element: 'click login button' or 'click search box'", 
            "Scroll page: 'scroll down' or 'scroll up'",
            "Navigate: 'go back' or 'go forward'",
            "Read content: 'read page' or 'read this'",
            "Stop action: 'stop' or 'cancel'",
            "Refresh page: 'refresh' or 'reload'",
            "Get help: 'help' or 'what can you do'"
        ]
        return commands


def main():
    """Test the command parser directly"""
    print("VoiceNav Command Parser Test")
    print("="*40)
    
    parser = CommandParser()
    
    # Test commands
    test_commands = [
        "open google",
        "go to reddit.com", 
        "click login button",
        "click the red search box",
        "scroll down",
        "scroll up",
        "go back",
        "read page",
        "stop",
        "help",
        "refresh page",
        "click on the first link",
        "open news",
        "visit github",
        "some random text that shouldn't match"
    ]
    
    print("\n🧠 Testing command parsing:")
    for command in test_commands:
        result = parser.parse(command)
        print(f"\nInput: '{command}'")
        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result['confidence']}")
        if result['params']:
            print(f"Params: {result['params']}")
    
    print(f"\n📋 Available commands:")
    for cmd in parser.get_available_commands():
        print(f"  • {cmd}")


if __name__ == "__main__":
    main()
