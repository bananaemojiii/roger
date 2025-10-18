#!/bin/bash
# Simple Cloudflare Quick Tunnel - No login needed!

echo "🚀 Starting Cloudflare Quick Tunnel (no login required)..."

# Kill old processes
ssh admn@192.168.4.102 "pkill cloudflared 2>/dev/null || true; pkill -f camera_stream 2>/dev/null || true"

# Start camera
echo "📹 Starting camera stream..."
ssh admn@192.168.4.102 "cd ~ && python3 camera_stream.py > /tmp/camera.log 2>&1 &"
sleep 3

# Start cloudflare with explicit logging
echo "🌐 Starting Cloudflare tunnel..."
ssh admn@192.168.4.102 "cloudflared tunnel --url http://localhost:8000 --logfile /tmp/cf.log > /tmp/cf_stdout.log 2>&1 &"
sleep 8

# Get URL
echo "🔍 Getting tunnel URL..."
URL=$(ssh admn@192.168.4.102 "cat /tmp/cf.log /tmp/cf_stdout.log 2>/dev/null | grep -o 'https://.*\.trycloudflare\.com' | head -1")

if [ -n "$URL" ]; then
    echo ""
    echo "✅ Tunnel is running!"
    echo "🌐 URL: $URL"
    echo "📹 Stream: $URL/stream.mjpg"
    echo ""
    echo "$URL/stream.mjpg"
else
    echo "⚠️  Could not get URL, checking logs..."
    ssh admn@192.168.4.102 "cat /tmp/cf_stdout.log 2>/dev/null | tail -20"
fi

