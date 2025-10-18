#!/bin/bash
set -e

echo "🌐 Setting up Permanent Cloudflare Tunnel (Free)"
echo ""
echo "This will create a tunnel that:"
echo "  ✅ Never expires"
echo "  ✅ Has a permanent URL"
echo "  ✅ Restarts automatically"
echo ""

# Step 1: Login to Cloudflare (will open browser)
echo "📝 Step 1: Logging in to Cloudflare..."
echo "  (A browser window will open - just log in or create free account)"
ssh admn@192.168.4.102 "cloudflared tunnel login"

echo ""
echo "✅ Login successful!"
echo ""

# Step 2: Create tunnel
echo "🔧 Step 2: Creating tunnel 'roger-camera'..."
TUNNEL_ID=$(ssh admn@192.168.4.102 "cloudflared tunnel create roger-camera 2>&1 | grep -o '[a-f0-9-]\{36\}' | head -1")
echo "  Tunnel ID: $TUNNEL_ID"

# Step 3: Create config file
echo "🔧 Step 3: Creating configuration..."
ssh admn@192.168.4.102 "mkdir -p ~/.cloudflared && cat > ~/.cloudflared/config.yml << 'EOF'
tunnel: $TUNNEL_ID
credentials-file: /home/admn/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: roger-camera-${TUNNEL_ID:0:8}.trycloudflare.com
    service: http://localhost:8000
  - service: http_status:404
EOF"

# Step 4: Route DNS
echo "🌐 Step 4: Setting up DNS..."
TUNNEL_URL="roger-camera-${TUNNEL_ID:0:8}.trycloudflare.com"
ssh admn@192.168.4.102 "cloudflared tunnel route dns roger-camera $TUNNEL_URL"

# Step 5: Start tunnel
echo "🚀 Step 5: Starting tunnel..."
ssh admn@192.168.4.102 "pkill cloudflared 2>/dev/null || true"
ssh admn@192.168.4.102 "nohup cloudflared tunnel run roger-camera > /tmp/cloudflared_permanent.log 2>&1 &"
sleep 5

echo ""
echo "✅ Permanent Cloudflare Tunnel Setup Complete!"
echo ""
echo "🌐 Your permanent URL:"
echo "   https://$TUNNEL_URL/stream.mjpg"
echo ""
echo "📝 This URL will NEVER change!"
echo ""

