#!/bin/bash
# Git push script for VoiceNav
# Run this after setting up SSH keys or GitHub CLI

echo "🚀 Pushing VoiceNav updates to GitHub..."
echo ""

# Check if we have access
echo "Testing GitHub access..."
if ssh -T git@github.com-personal 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ SSH access confirmed"
    git push origin main
    echo "✅ Successfully pushed to GitHub!"
else
    echo "❌ SSH access not configured"
    echo ""
    echo "Options to fix:"
    echo "1. Set up SSH keys:"
    echo "   ssh-keygen -t ed25519 -C 'your_email@example.com'"
    echo "   pbcopy < ~/.ssh/id_ed25519.pub"
    echo "   # Add to GitHub → Settings → SSH Keys"
    echo ""
    echo "2. Use GitHub CLI:"
    echo "   brew install gh"
    echo "   gh auth login"
    echo "   git push origin main"
    echo ""
    echo "3. Use HTTPS with token:"
    echo "   git remote set-url origin https://github.com/VivianObiako/voicenav.git"
    echo "   git push origin main"
    echo "   # Use personal access token as password"
fi
