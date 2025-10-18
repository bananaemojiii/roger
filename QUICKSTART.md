# ⚡ Quick Start - 5 Minutes to Global Camera Stream!

## 🎯 Goal
Get your Raspberry Pi camera streaming worldwide with YOLO object detection in 5 minutes.

## 📝 Prerequisites Checklist
- ✅ Raspberry Pi with camera running at `192.168.4.102`
- ✅ SSH access configured (`admn@192.168.4.102` password: `angel`)
- ✅ Camera stream running on Pi (port 8000)
- ✅ Railway account (sign up at [railway.app](https://railway.app))
- ✅ Node.js or Homebrew installed (for Railway CLI)

## 🚀 Three Simple Steps

### Step 1: Setup ngrok (2 minutes)

**On your Raspberry Pi:**

```bash
# SSH into your Pi
ssh admn@192.168.4.102

# Install ngrok (skip if already installed)
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok -y

# Start ngrok
ngrok http 8000
```

**Copy the URL** shown (looks like: `https://xxxx.ngrok-free.app`)

**Your camera URL is:** `https://xxxx.ngrok-free.app/stream.mjpg`

---

### Step 2: Deploy to Railway (2 minutes)

**On your Mac:**

```bash
# Navigate to project
cd "/Users/lukaschmiell/Documents/Crafts and Tech/RASSSP"

# Install Railway CLI (pick one)
npm install -g @railway/cli
# or
brew install railway

# Run the automated deployment script
./deploy.sh
```

When prompted:
1. Login to Railway (opens browser)
2. Enter your ngrok URL with `/stream.mjpg` at the end
3. Wait for deployment

---

### Step 3: Enjoy! (1 minute)

Railway will give you a URL like:
```
https://your-app-name.railway.app
```

**Open it in any browser, anywhere in the world! 🌍**

You'll see:
- ✅ Live camera feed
- ✅ YOLO object detection with bounding boxes
- ✅ Beautiful web interface
- ✅ Works on mobile too!

---

## 🎉 That's It!

Share the Railway URL with anyone to let them view your camera!

## 💡 Quick Commands

```bash
# View deployment logs
railway logs

# Update camera URL
railway variables set RASPBERRY_PI_URL="your-new-url"

# Redeploy
railway up

# Open app
railway open
```

## ⚠️ Important Notes

1. **Free ngrok tunnels expire after 2 hours** - you'll need to restart ngrok and update the Railway URL
2. **Upgrade to ngrok Pro** for permanent URLs (recommended for production)
3. **Camera must be running** on your Raspberry Pi for this to work
4. **First load might be slow** as Railway downloads the YOLO model

## 🔧 If Something Goes Wrong

**Camera not showing?**
```bash
# Check if Pi camera is running
ssh admn@192.168.4.102 "ps aux | grep camera_stream"

# Test ngrok URL directly in browser
open "https://your-ngrok-url.ngrok-free.app/stream.mjpg"

# View Railway logs
railway logs
```

**ngrok expired?**
```bash
# Restart ngrok on Pi
ssh admn@192.168.4.102
ngrok http 8000

# Update Railway
railway variables set RASPBERRY_PI_URL="new-ngrok-url/stream.mjpg"
```

---

## 📚 Learn More

- Full documentation: See `README.md`
- Deployment details: See `DEPLOY.md`
- Customize YOLO settings: Edit `app.py`

---

**Questions?** Open an issue or check the documentation!

🎥 Happy streaming! 🚀

