#!/bin/bash

# Setup ngrok tunnel for Raspberry Pi camera
# This allows Railway to access your local camera stream

echo "🚀 Setting up ngrok tunnel for your Raspberry Pi camera..."
echo ""

# Check if ngrok is installed on Raspberry Pi
ssh admn@192.168.4.102 "which ngrok" > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "📦 Installing ngrok on Raspberry Pi..."
    ssh admn@192.168.4.102 "curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok -y"
fi

echo ""
echo "⚙️  Starting ngrok tunnel..."
echo ""

# Start ngrok in background
ssh admn@192.168.4.102 "pkill ngrok; nohup ngrok http 8000 > /dev/null 2>&1 &"

# Wait for ngrok to start
sleep 3

# Get the public URL
NGROK_URL=$(ssh admn@192.168.4.102 "curl -s http://localhost:4040/api/tunnels | python3 -c 'import sys, json; print(json.load(sys.stdin)[\"tunnels\"][0][\"public_url\"])' 2>/dev/null")

if [ -z "$NGROK_URL" ]; then
    echo "❌ Failed to get ngrok URL"
    echo "Please manually start ngrok on your Raspberry Pi:"
    echo "  ssh admn@192.168.4.102"
    echo "  ngrok http 8000"
    exit 1
fi

# Append /stream.mjpg to the URL
FULL_URL="$NGROK_URL/stream.mjpg"

echo "✅ Ngrok tunnel is running!"
echo ""
echo "📋 Your camera stream URL:"
echo "   $FULL_URL"
echo ""
echo "🔧 Next steps:"
echo "   1. Copy the URL above"
echo "   2. Deploy to Railway"
echo "   3. Set RASPBERRY_PI_URL environment variable in Railway to:"
echo "      $FULL_URL"
echo ""
echo "💡 To stop ngrok: ssh admn@192.168.4.102 'pkill ngrok'"
echo ""

