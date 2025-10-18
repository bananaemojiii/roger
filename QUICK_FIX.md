# 🔧 Quick Fix - Get Video Stream Working

Your Railway app is deployed but the video stream isn't showing because the Raspberry Pi camera isn't accessible yet.

## ✅ What I Just Fixed

1. **Added placeholder image** - Shows helpful error message when camera isn't connected
2. **Added `/status` endpoint** - Check camera connection status
3. **Better error handling** - App won't crash if camera is unavailable
4. **Status indicator** - Badge turns red when disconnected

## 🚀 Quick Setup (3 Steps)

### Step 1: Start Camera on Raspberry Pi

```bash
# SSH into your Raspberry Pi
ssh admn@192.168.4.102

# Start the camera stream
python3 camera_stream.py
```

Keep this running! You should see: "✅ Camera stream started!"

### Step 2: Start ngrok Tunnel

```bash
# On Raspberry Pi (in a new terminal/tmux session)
ngrok http 8000
```

You'll see output like:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

### Step 3: Set Railway Environment Variable

```bash
# On your local machine
railway variables set RASPBERRY_PI_URL="https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg"

# Important: Add /stream.mjpg at the end!
# Example: 
# railway variables set RASPBERRY_PI_URL="https://abc123.ngrok-free.app/stream.mjpg"
```

### Step 4: Redeploy to Railway

```bash
# Commit the fixes
git add app.py
git commit -m "Add camera error handling and status endpoint"

# Deploy
railway up
```

## 🔍 Verify It's Working

1. **Check camera locally:**
   - Open: `http://192.168.4.102:8000` (should show camera feed)

2. **Check ngrok tunnel:**
   - Open your ngrok URL in browser: `https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg`
   - Should show the camera stream

3. **Check Railway status:**
   - Open: `https://your-railway-app.up.railway.app/status`
   - Should return: `{"status": "connected", ...}`

4. **Check the main page:**
   - Open: `https://your-railway-app.up.railway.app`
   - Should now show live video with YOLO detection!

## 🐛 Troubleshooting

### Issue: Camera stream shows "Camera Not Connected"

**Check each component:**

```bash
# 1. Test camera locally on Pi
curl http://localhost:8000/stream.mjpg

# 2. Test ngrok tunnel
curl https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg

# 3. Check Railway variables
railway variables

# 4. Check Railway logs
railway logs -f
```

### Issue: ngrok tunnel keeps disconnecting

Free ngrok tunnels expire after 2 hours. Solutions:

**Quick fix:**
```bash
# Restart ngrok
pkill ngrok
ngrok http 8000
# Update Railway with new URL
railway variables set RASPBERRY_PI_URL="https://NEW-URL.ngrok-free.app/stream.mjpg"
```

**Permanent fix:**
- Upgrade to ngrok paid plan ($8/month) for persistent URLs
- Or use Cloudflare Tunnel (free)

### Issue: Railway environment variable not updating

```bash
# Force refresh
railway variables set RASPBERRY_PI_URL="your-url"
railway up --detach
```

## 📊 Check Status in Real-Time

Use these endpoints to debug:

- `/health` - Railway health check (always returns healthy)
- `/status` - Camera connection status (shows if Pi is accessible)
- `/video_feed` - The actual video stream

Example:
```bash
curl https://your-railway-app.up.railway.app/status
```

## 🎯 Expected Result

Once everything is set up:
- ✅ Status badge shows "LIVE" (green)
- ✅ Video feed appears in the box
- ✅ YOLO bounding boxes appear on detected objects
- ✅ Stream updates in real-time

## 💡 Pro Tips

1. **Keep both running:**
   - Use `screen` or `tmux` on Raspberry Pi to keep camera stream running
   - Keep ngrok running in another session

2. **Quick tmux setup:**
   ```bash
   # On Raspberry Pi
   tmux new -s camera
   python3 camera_stream.py
   # Press Ctrl+B then D to detach
   
   tmux new -s ngrok
   ngrok http 8000
   # Press Ctrl+B then D to detach
   ```

3. **Auto-restart on boot:**
   Create systemd services for both camera stream and ngrok (see DEPLOY.md)

---

**Current Status:** App deployed, waiting for camera connection!

Once you complete the 3 steps above, refresh your Railway URL and you'll see the live stream! 🎉

