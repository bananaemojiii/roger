#!/bin/bash
# Remote setup script for Raspberry Pi

echo "🚀 Setting up Raspberry Pi remotely..."

# Kill existing processes
pkill -f camera_stream.py 2>/dev/null
pkill ngrok 2>/dev/null

# Start camera stream in background
echo "📹 Starting camera stream..."
nohup python3 ~/camera_stream.py > ~/camera_stream.log 2>&1 &
sleep 3

# Start ngrok in background
echo "🌐 Starting ngrok tunnel..."
nohup ngrok http 8000 > ~/ngrok.log 2>&1 &
sleep 5

# Get ngrok URL
echo "🔍 Getting ngrok URL..."
sleep 2
curl -s http://localhost:4040/api/tunnels | grep -o 'https://[^"]*\.ngrok[^"]*' | head -1

echo ""
echo "✅ Setup complete!"

