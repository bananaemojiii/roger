#!/bin/bash
set -e

echo "🔧 Setting up Cloudflare Tunnel..."

# Copy script to Pi
cat > /tmp/pi_setup.sh << 'EOF'
#!/bin/bash
# Kill old processes
pkill -f camera_stream.py 2>/dev/null || true
pkill cloudflared 2>/dev/null || true
pkill ngrok 2>/dev/null || true

# Start camera stream
cd ~
python3 camera_stream.py > /tmp/camera.log 2>&1 &
sleep 3

# Start cloudflare tunnel
cloudflared tunnel --url http://localhost:8000 > /tmp/cloudflared.log 2>&1 &
sleep 5

# Get URL
grep -o 'https://[^[:space:]]*trycloudflare.com' /tmp/cloudflared.log | head -1

echo "✅ Setup complete!"
EOF

# Copy and run on Pi
scp /tmp/pi_setup.sh admn@192.168.4.102:/tmp/
ssh admn@192.168.4.102 "bash /tmp/pi_setup.sh"

