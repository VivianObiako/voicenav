#!/usr/bin/env python3
"""
Script to create VoiceNav landing page structure and files
"""

import os

def create_landing_page_structure():
    """Create the landing page directory structure"""
    
    # Define the structure
    structure = {
        'docs': ['index.html', 'getting-started.html', 'commands.html', 'troubleshooting.html'],
        'css': ['styles.css', 'animations.css'],
        'js': ['main.js', 'demo.js'],
        'assets/images': [],
        'assets/videos': [],
        'assets/audio': []
    }
    
    # Create directories and files
    for directory, files in structure.items():
        os.makedirs(directory, exist_ok=True)
        for file in files:
            file_path = os.path.join(directory, file)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(f"/* {file} - VoiceNav Landing Page */\n")
    
    print("✅ Landing page structure created!")

def create_index_html():
    """Create the main landing page HTML"""
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoiceNav - Voice-Controlled Browser Automation</title>
    <meta name="description" content="Voice-controlled browser automation for macOS using Maya AI assistant. Navigate the web with natural language commands.">
    
    <!-- CSS -->
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="css/styles.css" rel="stylesheet">
    <link href="css/animations.css" rel="stylesheet">
</head>
<body class="bg-gray-900 text-white">
    
    <!-- Navigation -->
    <nav class="fixed top-0 w-full bg-gray-800 bg-opacity-90 backdrop-blur-sm z-50">
        <div class="container mx-auto px-6 py-3">
            <div class="flex justify-between items-center">
                <div class="flex items-center">
                    <i class="fas fa-microphone-alt text-blue-400 text-2xl mr-3"></i>
                    <span class="text-xl font-bold">VoiceNav</span>
                </div>
                <div class="hidden md:flex space-x-6">
                    <a href="#features" class="hover:text-blue-400 transition">Features</a>
                    <a href="#demo" class="hover:text-blue-400 transition">Demo</a>
                    <a href="#docs" class="hover:text-blue-400 transition">Docs</a>
                    <a href="https://github.com/VivianObiako/voicenav" class="hover:text-blue-400 transition">
                        <i class="fab fa-github"></i> GitHub
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-purple-900 to-gray-900">
        <div class="container mx-auto px-6 text-center">
            <div class="mb-8">
                <i class="fas fa-microphone-alt text-6xl text-blue-400 mb-6 voice-pulse"></i>
                <h1 class="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    VoiceNav
                </h1>
                <p class="text-xl md:text-2xl mb-8 text-gray-300">
                    Voice-controlled browser automation for macOS
                </p>
                <p class="text-lg mb-12 text-gray-400 max-w-2xl mx-auto">
                    Navigate the web using natural language commands with Maya, your AI assistant. 
                    Powered by offline speech recognition and native browser control.
                </p>
            </div>
            
            <!-- Voice Demo Animation -->
            <div class="voice-demo mb-12">
                <div class="bg-gray-800 rounded-lg p-6 max-w-md mx-auto mb-6">
                    <div class="flex items-center justify-center mb-4">
                        <i class="fas fa-user text-blue-400 mr-3"></i>
                        <span class="typing-text">"Hey Maya, open google"</span>
                    </div>
                    <div class="flex items-center justify-center">
                        <i class="fas fa-robot text-purple-400 mr-3"></i>
                        <span class="maya-response">"Opened google"</span>
                    </div>
                </div>
            </div>
            
            <!-- CTA Buttons -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
                <a href="#demo" class="bg-blue-600 hover:bg-blue-700 px-8 py-4 rounded-lg font-semibold transition transform hover:scale-105">
                    <i class="fas fa-play mr-2"></i>
                    Try Demo
                </a>
                <a href="https://github.com/VivianObiako/voicenav" class="bg-gray-700 hover:bg-gray-600 px-8 py-4 rounded-lg font-semibold transition transform hover:scale-105">
                    <i class="fab fa-github mr-2"></i>
                    View on GitHub
                </a>
                <a href="#install" class="bg-purple-600 hover:bg-purple-700 px-8 py-4 rounded-lg font-semibold transition transform hover:scale-105">
                    <i class="fas fa-download mr-2"></i>
                    Get Started
                </a>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 bg-gray-800">
        <div class="container mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-16">Powerful Features</h2>
            
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Feature 1: Voice Control -->
                <div class="bg-gray-900 rounded-lg p-6 hover:transform hover:scale-105 transition">
                    <div class="text-blue-400 text-3xl mb-4">
                        <i class="fas fa-microphone-alt"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Natural Voice Control</h3>
                    <p class="text-gray-400">
                        Wake word activation with offline speech recognition. 
                        No internet required for voice processing.
                    </p>
                </div>
                
                <!-- Feature 2: Multi-Browser -->
                <div class="bg-gray-900 rounded-lg p-6 hover:transform hover:scale-105 transition">
                    <div class="text-green-400 text-3xl mb-4">
                        <i class="fas fa-globe"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Universal Browser Support</h3>
                    <p class="text-gray-400">
                        Works with Safari, Chrome, Arc, Edge. 
                        Auto-detects your default browser.
                    </p>
                </div>
                
                <!-- Feature 3: Privacy -->
                <div class="bg-gray-900 rounded-lg p-6 hover:transform hover:scale-105 transition">
                    <div class="text-purple-400 text-3xl mb-4">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Privacy-First</h3>
                    <p class="text-gray-400">
                        Offline speech recognition. No data sent to external servers. 
                        Your voice stays on your Mac.
                    </p>
                </div>
                
                <!-- Feature 4: Native Integration -->
                <div class="bg-gray-900 rounded-lg p-6 hover:transform hover:scale-105 transition">
                    <div class="text-yellow-400 text-3xl mb-4">
                        <i class="fab fa-apple"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Native macOS Integration</h3>
                    <p class="text-gray-400">
                        Uses AppleScript for reliable browser control. 
                        Works with your existing browser setup.
                    </p>
                </div>
                
                <!-- Feature 5: Smart Commands -->
                <div class="bg-gray-900 rounded-lg p-6 hover:transform hover:scale-105 transition">
                    <div class="text-red-400 text-3xl mb-4">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Smart Command Parser</h3>
                    <p class="text-gray-400">
                        92% accuracy with 40+ website shortcuts. 
                        Natural language understanding.
                    </p>
                </div>
                
                <!-- Feature 6: Maya Assistant -->
                <div class="bg-gray-900 rounded-lg p-6 hover:transform hover:scale-105 transition">
                    <div class="text-pink-400 text-3xl mb-4">
                        <i class="fas fa-robot"></i>
                    </div>
                    <h3 class="text-xl font-semibold mb-3">Maya AI Assistant</h3>
                    <p class="text-gray-400">
                        Friendly voice feedback for all actions. 
                        Samantha voice confirms every command.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Demo Section -->
    <section id="demo" class="py-20 bg-gray-900">
        <div class="container mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-16">See VoiceNav in Action</h2>
            
            <div class="max-w-4xl mx-auto">
                <!-- Browser Mockup -->
                <div class="bg-gray-800 rounded-lg overflow-hidden shadow-2xl">
                    <!-- Browser Header -->
                    <div class="bg-gray-700 px-4 py-3 flex items-center">
                        <div class="flex space-x-2">
                            <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                            <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                        </div>
                        <div class="flex-1 text-center">
                            <span class="text-gray-300">Safari</span>
                        </div>
                    </div>
                    
                    <!-- Browser Content -->
                    <div class="p-8 text-center">
                        <div id="maya-status" class="mb-6 p-4 bg-blue-900 rounded-lg">
                            <i class="fas fa-ear-listen text-blue-400 mr-2"></i>
                            <span>👂 Listening for Maya...</span>
                        </div>
                        
                        <!-- Demo Commands -->
                        <div class="grid md:grid-cols-2 gap-4 mb-8">
                            <button onclick="playDemo('open-google')" class="demo-btn bg-green-600 hover:bg-green-700">
                                🎤 "Hey Maya, open google"
                            </button>
                            <button onclick="playDemo('scroll-down')" class="demo-btn bg-blue-600 hover:bg-blue-700">
                                🎤 "Hey Maya, scroll down"
                            </button>
                            <button onclick="playDemo('go-back')" class="demo-btn bg-purple-600 hover:bg-purple-700">
                                🎤 "Hey Maya, go back"
                            </button>
                            <button onclick="playDemo('help')" class="demo-btn bg-orange-600 hover:bg-orange-700">
                                🎤 "Hey Maya, help"
                            </button>
                        </div>
                        
                        <div id="demo-result" class="hidden p-4 bg-gray-700 rounded-lg">
                            <div class="flex items-center justify-center">
                                <i class="fas fa-robot text-purple-400 mr-3"></i>
                                <span id="maya-response"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Installation Section -->
    <section id="install" class="py-20 bg-gray-800">
        <div class="container mx-auto px-6">
            <h2 class="text-4xl font-bold text-center mb-16">Quick Start</h2>
            
            <div class="max-w-3xl mx-auto">
                <div class="bg-gray-900 rounded-lg p-6 mb-8">
                    <h3 class="text-xl font-semibold mb-4">1. Clone Repository</h3>
                    <div class="bg-black rounded p-4 font-mono text-sm">
                        <span class="text-green-400">$</span> git clone https://github.com/VivianObiako/voicenav.git<br>
                        <span class="text-green-400">$</span> cd voicenav
                    </div>
                </div>
                
                <div class="bg-gray-900 rounded-lg p-6 mb-8">
                    <h3 class="text-xl font-semibold mb-4">2. Setup Environment</h3>
                    <div class="bg-black rounded p-4 font-mono text-sm">
                        <span class="text-green-400">$</span> python3 -m venv venv<br>
                        <span class="text-green-400">$</span> source venv/bin/activate<br>
                        <span class="text-green-400">$</span> pip install -r requirements.txt
                    </div>
                </div>
                
                <div class="bg-gray-900 rounded-lg p-6 mb-8">
                    <h3 class="text-xl font-semibold mb-4">3. Run VoiceNav</h3>
                    <div class="bg-black rounded p-4 font-mono text-sm">
                        <span class="text-green-400">$</span> python3 src/main.py
                    </div>
                </div>
                
                <div class="text-center">
                    <p class="text-lg text-gray-300 mb-4">Then say:</p>
                    <div class="bg-blue-900 rounded-lg p-4 inline-block">
                        <span class="text-xl">"Hey Maya, open google"</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 py-8">
        <div class="container mx-auto px-6 text-center">
            <div class="flex justify-center space-x-6 mb-4">
                <a href="https://github.com/VivianObiako/voicenav" class="text-gray-400 hover:text-white">
                    <i class="fab fa-github text-2xl"></i>
                </a>
            </div>
            <p class="text-gray-400">
                © 2025 VoiceNav. Open source voice-controlled browser automation.
            </p>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="js/main.js"></script>
    <script src="js/demo.js"></script>
</body>
</html>'''
    
    with open('docs/index.html', 'w') as f:
        f.write(html_content)
    
    print("✅ index.html created!")

def create_demo_js():
    """Create the demo JavaScript functionality"""
    
    js_content = '''// VoiceNav Landing Page Demo
function playDemo(command) {
    const statusEl = document.getElementById('maya-status');
    const resultEl = document.getElementById('demo-result');
    const responseEl = document.getElementById('maya-response');
    
    // Reset state
    resultEl.classList.add('hidden');
    
    // Show processing
    statusEl.innerHTML = '<i class="fas fa-microphone text-blue-400 mr-2"></i>🎤 Processing...';
    statusEl.className = 'mb-6 p-4 bg-yellow-900 rounded-lg';
    
    // Demo responses
    const responses = {
        'open-google': {
            text: 'Opened google',
            action: 'Opening Google in new tab...'
        },
        'scroll-down': {
            text: 'Scrolling down',
            action: 'Scrolling page content...'
        },
        'go-back': {
            text: 'Going back',
            action: 'Navigating to previous page...'
        },
        'help': {
            text: 'I can open websites, scroll pages, go back and forward, refresh pages, and read content. Try saying "open google" or "scroll down".',
            action: 'Showing available commands...'
        }
    };
    
    setTimeout(() => {
        // Show Maya response
        const response = responses[command];
        responseEl.textContent = response.text;
        resultEl.classList.remove('hidden');
        
        // Update status
        statusEl.innerHTML = `<i class="fas fa-check text-green-400 mr-2"></i>${response.action}`;
        statusEl.className = 'mb-6 p-4 bg-green-900 rounded-lg';
        
        // Reset after a few seconds
        setTimeout(() => {
            statusEl.innerHTML = '<i class="fas fa-ear-listen text-blue-400 mr-2"></i>👂 Listening for Maya...';
            statusEl.className = 'mb-6 p-4 bg-blue-900 rounded-lg';
            resultEl.classList.add('hidden');
        }, 3000);
        
    }, 1500);
}

// Typing animation for hero text
document.addEventListener('DOMContentLoaded', function() {
    const typingText = document.querySelector('.typing-text');
    if (typingText) {
        const text = '"Hey Maya, open google"';
        typingText.textContent = '';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                typingText.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            } else {
                // Show Maya response after typing
                setTimeout(() => {
                    document.querySelector('.maya-response').style.opacity = '1';
                }, 500);
            }
        };
        
        setTimeout(typeWriter, 1000);
    }
});'''
    
    with open('js/demo.js', 'w') as f:
        f.write(js_content)
    
    print("✅ demo.js created!")

def create_animations_css():
    """Create CSS animations"""
    
    css_content = '''/* VoiceNav Landing Page Animations */

.voice-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.7;
        transform: scale(1.1);
    }
}

.typing-text {
    border-right: 2px solid #60a5fa;
    animation: typing 3s steps(22, end), blink-caret 0.75s step-end infinite;
}

@keyframes typing {
    from { width: 0 }
    to { width: 100% }
}

@keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: #60a5fa; }
}

.maya-response {
    opacity: 0;
    transition: opacity 0.5s ease-in-out;
}

.demo-btn {
    @apply px-6 py-3 rounded-lg font-semibold transition transform hover:scale-105;
}

.hero {
    background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 50%, #374151 100%);
}

/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* Responsive design helpers */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 3rem;
    }
    
    .demo-btn {
        font-size: 0.875rem;
        padding: 0.75rem 1rem;
    }
}'''
    
    with open('css/animations.css', 'w') as f:
        f.write(css_content)
    
    print("✅ animations.css created!")

def main():
    """Main function to create landing page"""
    print("🌐 Creating VoiceNav Landing Page...")
    
    create_landing_page_structure()
    create_index_html()
    create_demo_js()
    create_animations_css()
    
    print("\n🎉 Landing page created successfully!")
    print("\nNext steps:")
    print("1. Open docs/index.html in your browser to preview")
    print("2. Deploy to GitHub Pages:")
    print("   - Push to a 'gh-pages' branch")
    print("   - Enable GitHub Pages in repo settings")
    print("3. Customize content and styling as needed")
    print("\n🚀 Your landing page will be available at:")
    print("   https://VivianObiako.github.io/voicenav")

if __name__ == "__main__":
    main()
