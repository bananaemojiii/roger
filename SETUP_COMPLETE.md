# ✅ Flask + Cloudflare Tunnel - Setup Complete!

## 🎉 Your Camera Stream is Now Live!

**Public URL:** https://root-brown-promotions-acknowledge.trycloudflare.com

### Quick Links
- 🌐 Main Page: https://root-brown-promotions-acknowledge.trycloudflare.com/
- 📹 Video Stream: https://root-brown-promotions-acknowledge.trycloudflare.com/video_feed
- 🏥 Health Check: https://root-brown-promotions-acknowledge.trycloudflare.com/health
- 📊 Status: https://root-brown-promotions-acknowledge.trycloudflare.com/status

## 🚀 Quick Start

### Start Everything (Easy Way)
```bash
./start_local_tunnel.sh
```

### Manual Start
```bash
# Terminal 1 - Flask App
cd /Users/lukaschmiell/Documents/SOFT/roger
source venv/bin/activate
export RASPBERRY_PI_URL="http://192.168.4.102:8000/stream.mjpg"
export PORT=8080
python3 app.py

# Terminal 2 - Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8080
```

## 🛑 Stop Services
```bash
pkill -f 'python.*app.py' && pkill cloudflared
```

## 📝 What Was Fixed

### 1. **502 Bad Gateway Issue** ✅
   - **Problem**: Cloudflare tunnel had no service to connect to
   - **Solution**: Started Flask app on port 8080 and connected Cloudflare tunnel

### 2. **Python Dependencies** ✅
   - **Problem**: Required packages not installed
   - **Solution**: Created virtual environment and installed all requirements

### 3. **YOLO Model Loading** ✅
   - **Problem**: Hugging Face token expired/invalid
   - **Solution**: Modified app.py to use local yolov8n.pt file first, fallback to HF

### 4. **Cloudflared Not Installed** ✅
   - **Problem**: cloudflared command not found
   - **Solution**: Installed via `brew install cloudflared`

## 🔧 Technical Details

### Current Setup
- **Flask App**: Running on `0.0.0.0:8080`
- **Virtual Environment**: `/Users/lukaschmiell/Documents/SOFT/roger/venv`
- **YOLO Model**: Local file `yolov8n.pt`
- **Cloudflare Tunnel**: Quick tunnel (no login required)
- **Raspberry Pi Stream**: `http://192.168.4.102:8000/stream.mjpg`

### Logs
- Flask: `/tmp/flask_app.log`
- Cloudflare: `/tmp/cloudflared.log`

### Check Status
```bash
# Check if Flask is running
curl http://localhost:8080/health

# Check if tunnel is working
curl https://root-brown-promotions-acknowledge.trycloudflare.com/health

# View processes
ps aux | grep -E "(app.py|cloudflared)" | grep -v grep
```

## 📦 Files Modified
1. **app.py** - Fixed YOLO model loading to use local file
2. **start_local_tunnel.sh** - New script for easy startup

## 🎯 Next Steps

### Option 1: Keep Current Setup (Quick Tunnel)
- ✅ Works immediately
- ⚠️ URL changes each time you restart
- 🔄 Run `./start_local_tunnel.sh` to get new URL

### Option 2: Permanent Cloudflare Tunnel (Recommended)
```bash
# Login to Cloudflare (one-time)
cloudflared tunnel login

# Create named tunnel
cloudflared tunnel create roger-camera

# Configure tunnel
mkdir -p ~/.cloudflared
cat > ~/.cloudflared/config.yml << EOF
tunnel: roger-camera
credentials-file: ~/.cloudflared/<TUNNEL-ID>.json

ingress:
  - hostname: your-domain.com
    service: http://localhost:8080
  - service: http_status:404
EOF

# Route DNS (requires domain)
cloudflared tunnel route dns roger-camera your-domain.com

# Run tunnel
cloudflared tunnel run roger-camera
```

### Option 3: Use Ngrok Instead
```bash
# Install ngrok
brew install ngrok

# Start tunnel
ngrok http 8080

# Get URL from output
```

## 💡 Tips

1. **Raspberry Pi Connection**: Make sure your Raspberry Pi camera stream is running:
   ```bash
   ssh admn@192.168.4.102 "python3 camera_stream.py"
   ```

2. **Port Already in Use**: If port 8080 is busy, change it:
   ```bash
   export PORT=8081
   # Then update cloudflared: cloudflared tunnel --url http://localhost:8081
   ```

3. **Virtual Environment**: Always activate before running:
   ```bash
   source venv/bin/activate
   ```

4. **Check Logs**: If something doesn't work:
   ```bash
   tail -f /tmp/flask_app.log
   tail -f /tmp/cloudflared.log
   ```

## 🐛 Troubleshooting

### Flask Won't Start
```bash
# Check for errors
python3 app.py
# If model issues, ensure yolov8n.pt exists
ls -lh yolov8n.pt
```

### Tunnel Shows 502 Error
```bash
# Verify Flask is running
curl http://localhost:8080/health
# Should return: {"status": "healthy", ...}
```

### Can't Access Raspberry Pi
```bash
# Test connection
curl http://192.168.4.102:8000/stream.mjpg
# Or check if Pi is reachable
ping 192.168.4.102
```

## 📱 Share Your Stream

Your stream is now accessible from anywhere! Just share:
```
https://root-brown-promotions-acknowledge.trycloudflare.com
```

**Note**: This URL is temporary. Use the permanent setup above for a fixed URL.

---

**✨ Everything is working! Your Flask app is serving AI-powered camera detection globally!**

