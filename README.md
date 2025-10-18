# 🌍 Global Raspberry Pi Camera Stream with YOLO

A web application that streams your Raspberry Pi camera feed globally with real-time YOLO object detection, deployed on Railway.

## 🚀 Features

- **Global Access**: View your camera from anywhere in the world
- **AI-Powered**: Real-time object detection using YOLOv8
- **Beautiful UI**: Modern, responsive web interface
- **Production Ready**: Deployed on Railway with Docker
- **Health Monitoring**: Built-in health check endpoint
- **Optimized**: Efficient Docker builds with layer caching

## 📋 Prerequisites

1. Raspberry Pi with camera module
2. Railway account (free tier available at [railway.app](https://railway.app))
3. Git installed on your local machine
4. ngrok account (free tier works for testing)

## 🛠️ Quick Start

### Step 1: Prepare Your Raspberry Pi

1. Make sure the camera stream is running on your Raspberry Pi:
   ```bash
   ssh admn@192.168.4.102
   python3 camera_stream.py &
   ```

2. The camera stream should be accessible at `http://192.168.4.102:8000/stream.mjpg`

### Step 2: Setup ngrok Tunnel

To make your Raspberry Pi camera accessible from Railway:

```bash
# On your Raspberry Pi
ngrok http 8000
```

Copy the ngrok URL (e.g., `https://xxxx-xx-xx-xxx-xx.ngrok-free.app`)

### Step 3: Deploy to Railway

**Using Railway CLI (Recommended):**

```bash
# Install Railway CLI
npm install -g @railway/cli
# or: brew install railway

# Login and initialize
railway login
railway init

# Set environment variable
railway variables set RASPBERRY_PI_URL="https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg"

# Deploy!
railway up

# Open your deployed app
railway open
```

**Using GitHub:**

1. Push to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Camera stream with YOLO"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. Connect repository in Railway dashboard
3. Add `RASPBERRY_PI_URL` environment variable
4. Railway will automatically deploy!

### Step 4: Access Your Stream! 🎉

Visit your Railway URL: `https://your-project-name.up.railway.app`

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RASPBERRY_PI_URL` | URL to your Raspberry Pi camera stream (required) | `http://192.168.4.102:8000/stream.mjpg` |
| `PORT` | Port for the web server (Railway sets this automatically) | `8080` |

### Railway Configuration

The project includes:
- `Dockerfile`: Optimized multi-stage Docker build
- `railway.json`: Railway deployment configuration with health checks
- `.dockerignore`: Excludes unnecessary files for faster builds
- Health check endpoint at `/health`

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

## 🚀 Deployment Commands Reference

```bash
# Railway CLI commands
railway login                    # Login to Railway
railway init                     # Initialize new project
railway up                       # Deploy current directory
railway logs                     # View application logs
railway logs -f                  # Follow logs in real-time
railway open                     # Open deployed app in browser
railway status                   # Check deployment status
railway variables                # List environment variables
railway variables set KEY=value  # Set environment variable
railway run bash                 # SSH into container
railway link                     # Link to existing project
```

## 📊 Monitoring

Railway provides:
- Real-time logs and deployment status
- CPU and memory usage metrics
- Automatic HTTPS and SSL certificates
- Custom domain support
- Environment variable management
- Deployment history and rollbacks

## 📝 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Feel free to open issues or submit PRs!

---

Made with ❤️ using Raspberry Pi, YOLOv8, Flask, and Railway

