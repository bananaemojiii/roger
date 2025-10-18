# 🌍 Global Raspberry Pi Camera Stream with YOLO

A web application that streams your Raspberry Pi camera feed globally with real-time YOLO object detection, deployed on Railway.

## 🚀 Features

- **Global Access**: View your camera from anywhere in the world
- **AI-Powered**: Real-time object detection using YOLOv8
- **Beautiful UI**: Modern, responsive web interface
- **Production Ready**: Deployed on Railway with auto-scaling

## 📋 Prerequisites

1. Raspberry Pi with camera module
2. Railway account (free tier works!)
3. Git installed on your local machine

## 🛠️ Setup Instructions

### Step 1: Prepare Your Raspberry Pi

Make sure the camera stream is running on your Raspberry Pi:

```bash
ssh admn@192.168.4.102
python3 camera_stream.py &
```

The camera stream should be accessible at `http://192.168.4.102:8000/stream.mjpg`

### Step 2: Setup Port Forwarding (Important!)

For Railway to access your Raspberry Pi camera, you need to:

**Option A: Use ngrok (Recommended for testing)**
```bash
# On your Raspberry Pi
ngrok http 8000
```
This will give you a public URL like: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app`

**Option B: Setup your router's port forwarding**
1. Find your public IP address
2. Forward port 8000 to your Raspberry Pi's local IP (192.168.4.102)
3. Use your public IP as: `http://YOUR_PUBLIC_IP:8000/stream.mjpg`

### Step 3: Deploy to Railway

1. **Initialize Git Repository**
```bash
cd "/Users/lukaschmiell/Documents/Crafts and Tech/RASSSP"
git init
git add .
git commit -m "Initial commit: Camera stream with YOLO"
```

2. **Create Railway Project**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo" or "Deploy from local"
   - Connect your repository

3. **Set Environment Variable**
   In Railway dashboard, add this environment variable:
   ```
   RASPBERRY_PI_URL=http://YOUR_NGROK_URL/stream.mjpg
   ```
   or
   ```
   RASPBERRY_PI_URL=http://YOUR_PUBLIC_IP:8000/stream.mjpg
   ```

4. **Deploy!**
   Railway will automatically build and deploy your app.

### Step 4: Access Your Stream

Once deployed, Railway will give you a URL like:
```
https://your-app-name.railway.app
```

Open this URL from anywhere in the world to see your camera feed with YOLO detection! 🎉

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RASPBERRY_PI_URL` | URL to your Raspberry Pi camera stream | `http://192.168.4.102:8000/stream.mjpg` |
| `PORT` | Port for the web server (Railway sets this automatically) | `8080` |

## 📱 Usage

Once deployed:
1. Open the Railway URL in any browser
2. You'll see your live camera feed with YOLO object detection
3. Objects will be automatically detected and labeled with bounding boxes
4. Share the URL with anyone to give them access!

## 🎯 YOLO Detection

The app uses YOLOv8 nano model which can detect 80 different object classes including:
- People
- Vehicles (cars, trucks, buses, motorcycles)
- Animals (cats, dogs, birds, etc.)
- Common objects (phones, laptops, bottles, etc.)

## 🔒 Security Notes

**Important**: This setup makes your camera accessible worldwide. Consider:
- Using authentication (add Flask-Login)
- Restricting access by IP
- Using HTTPS only
- Setting up proper firewall rules
- Not pointing the camera at sensitive areas

## 🐛 Troubleshooting

### Camera Not Connecting
- Check if Raspberry Pi is online
- Verify the RASPBERRY_PI_URL is correct
- Test the URL directly in a browser
- Check firewall/router settings

### YOLO Model Loading Slowly
- First deployment may take time to download the model
- Consider using a lighter model (yolov8n.pt)
- Railway may need to cold start (first load is slower)

### Stream Lagging
- Check your Raspberry Pi's internet upload speed
- Reduce camera resolution in `camera_stream.py`
- Consider upgrading Railway plan for more resources

## 📦 Local Testing

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export RASPBERRY_PI_URL="http://192.168.4.102:8000/stream.mjpg"

# Run the app
python app.py
```

Visit `http://localhost:8080` to test.

## 🚀 Deployment Commands

```bash
# Initial setup
git init
git add .
git commit -m "Initial commit"

# Connect to Railway
railway login
railway init
railway up

# Set environment variable
railway variables set RASPBERRY_PI_URL=your_camera_url

# View logs
railway logs

# Open deployed app
railway open
```

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Feel free to open issues or submit PRs!

---

Made with ❤️ using Raspberry Pi, YOLOv8, Flask, and Railway

