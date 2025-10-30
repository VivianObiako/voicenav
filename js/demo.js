// VoiceNav Landing Page Demo
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
});