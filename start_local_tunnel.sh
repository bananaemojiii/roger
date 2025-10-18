#!/bin/bash
# Start Flask app with Cloudflare tunnel

set -e

cd "$(dirname "$0")"

echo "🚀 Starting Flask + Cloudflare Tunnel Setup"
echo ""

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f "python.*app.py" 2>/dev/null || true
pkill cloudflared 2>/dev/null || true
sleep 2

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip wheel setuptools
    pip install -r requirements.txt
else
    echo "✅ Virtual environment exists"
    source venv/bin/activate
fi

# Set environment variables
export RASPBERRY_PI_URL="http://192.168.4.102:8000/stream.mjpg"
export PORT=8080

# Start Flask app in background
echo "🐍 Starting Flask app on port 8080..."
python3 app.py > /tmp/flask_app.log 2>&1 &
FLASK_PID=$!

# Wait for Flask to start
echo "⏳ Waiting for Flask to start..."
for i in {1..30}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ Flask app is running (PID: $FLASK_PID)"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Flask failed to start. Check /tmp/flask_app.log for errors"
        cat /tmp/flask_app.log
        exit 1
    fi
    sleep 1
done

# Start Cloudflare tunnel
echo "🌐 Starting Cloudflare tunnel..."
cloudflared tunnel --url http://localhost:8080 > /tmp/cloudflared.log 2>&1 &
TUNNEL_PID=$!

# Wait for tunnel URL
echo "⏳ Waiting for tunnel URL..."
for i in {1..20}; do
    URL=$(grep -o "https://.*\.trycloudflare\.com" /tmp/cloudflared.log 2>/dev/null | head -1)
    if [ -n "$URL" ]; then
        break
    fi
    sleep 1
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ SUCCESS! Your camera stream is now accessible!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Public URL:"
echo "   $URL"
echo ""
echo "📹 Video Stream:"
echo "   $URL/video_feed"
echo ""
echo "🏥 Health Check:"
echo "   $URL/health"
echo ""
echo "💻 Local Access:"
echo "   http://localhost:8080"
echo ""
echo "📊 Process Info:"
echo "   Flask PID: $FLASK_PID"
echo "   Tunnel PID: $TUNNEL_PID"
echo ""
echo "📝 Logs:"
echo "   Flask:  tail -f /tmp/flask_app.log"
echo "   Tunnel: tail -f /tmp/cloudflared.log"
echo ""
echo "🛑 To stop:"
echo "   pkill -f 'python.*app.py' && pkill cloudflared"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Keep script running to show real-time status
echo "Press Ctrl+C to stop all services..."
trap "echo ''; echo '🛑 Stopping services...'; kill $FLASK_PID $TUNNEL_PID 2>/dev/null; exit 0" INT TERM

# Wait indefinitely
wait

