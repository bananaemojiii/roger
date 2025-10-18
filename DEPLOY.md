# 🚀 Quick Deployment Guide

Follow these steps to deploy your camera stream with YOLO to Railway.

## 📋 Step-by-Step Instructions

### Step 1: Setup ngrok Tunnel (5 minutes)

Your Raspberry Pi camera needs to be accessible from the internet. We'll use ngrok for this:

```bash
# Run this script to automatically setup ngrok
./setup_ngrok.sh
```

**OR manually:**

1. SSH into your Raspberry Pi:
   ```bash
   ssh admn@192.168.4.102
   ```

2. Install ngrok (if not already installed):
   ```bash
   curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
     sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
     echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
     sudo tee /etc/apt/sources.list.d/ngrok.list && \
     sudo apt update && sudo apt install ngrok
   ```

3. Sign up at [ngrok.com](https://ngrok.com) and get your authtoken

4. Configure ngrok:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

5. Start the tunnel:
   ```bash
   ngrok http 8000
   ```

6. **Copy the ngrok URL** - it will look like: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app`

7. Your camera URL will be: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app/stream.mjpg`

### Step 2: Deploy to Railway (3 minutes)

#### Option A: Deploy via Railway CLI (Recommended)

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   # or
   brew install railway
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Create a new project:
   ```bash
   railway init
   ```

4. Set your environment variable:
   ```bash
   railway variables set RASPBERRY_PI_URL="https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg"
   ```

5. Deploy!
   ```bash
   railway up
   ```

6. Get your deployment URL:
   ```bash
   railway open
   ```

#### Option B: Deploy via GitHub

1. Create a new repository on GitHub

2. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git commit -m "Initial commit: Camera stream with YOLO"
   git push -u origin main
   ```

3. Go to [railway.app](https://railway.app)

4. Click "New Project" → "Deploy from GitHub repo"

5. Select your repository

6. Add environment variable:
   - Go to Variables tab
   - Add `RASPBERRY_PI_URL` = `https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg`

7. Railway will automatically deploy!

### Step 3: Access Your Stream! 🎉

Once deployed, Railway will give you a URL like:
```
https://your-project-name.railway.app
```

**Open this URL from anywhere in the world!**

## 🔧 Troubleshooting

### Camera stream not showing

1. **Check if Raspberry Pi camera is running:**
   ```bash
   ssh admn@192.168.4.102
   ps aux | grep camera_stream
   ```

2. **Test the ngrok URL directly:**
   Open `https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg` in your browser

3. **Check Railway logs:**
   ```bash
   railway logs
   ```

### ngrok tunnel expired

Free ngrok tunnels expire after 2 hours. You need to:
- Restart ngrok
- Update the `RASPBERRY_PI_URL` in Railway
- Or upgrade to ngrok paid plan for permanent URLs

### YOLO model loading error

First deployment might take 2-3 minutes as it downloads the YOLO model. Just wait!

## 💡 Pro Tips

### Keep ngrok running permanently

Create a systemd service on your Raspberry Pi:

```bash
ssh admn@192.168.4.102

# Create service file
sudo nano /etc/systemd/system/camera-ngrok.service
```

Add this content:
```ini
[Unit]
Description=Ngrok tunnel for camera
After=network.target

[Service]
Type=simple
User=admn
WorkingDirectory=/home/admn
ExecStart=/usr/local/bin/ngrok http 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable camera-ngrok.service
sudo systemctl start camera-ngrok.service
```

### Monitor your deployment

```bash
# View live logs
railway logs -f

# Check deployment status
railway status

# SSH into Railway container
railway run bash
```

## 🌐 Alternative to ngrok

### Cloudflare Tunnel (Free, Permanent URL)

1. Install cloudflared on Raspberry Pi:
   ```bash
   curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb -o cloudflared.deb
   sudo dpkg -i cloudflared.deb
   ```

2. Start tunnel:
   ```bash
   cloudflared tunnel --url http://localhost:8000
   ```

3. Use the provided URL in Railway

## 📊 Monitoring

Railway provides:
- Real-time logs
- CPU/Memory usage
- Deployment history
- Automatic HTTPS
- Custom domains

## 🎯 Next Steps

- Add authentication to your stream
- Customize YOLO detection classes
- Add recording functionality
- Set up alerts for detected objects
- Use a custom domain

---

**Need help?** Check the main README.md or open an issue!

