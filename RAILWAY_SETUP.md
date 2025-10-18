# Railway Deployment Setup - Summary

This document summarizes the fixes and optimizations made for Railway deployment.

## ✅ Changes Made

### 1. **Dockerfile Improvements**
- Added explicit `PORT` environment variable with default value (8080)
- Fixed port binding to use `${PORT}` syntax for proper shell expansion
- Added `--worker-class gthread` for better thread handling
- Optimized for Railway's environment

**Key Changes:**
```dockerfile
ENV PORT=8080
EXPOSE $PORT
CMD gunicorn --bind 0.0.0.0:${PORT} --workers 2 --threads 4 --timeout 120 --worker-class gthread app:app
```

### 2. **Railway Configuration (railway.json)**
- Removed redundant `startCommand` (handled by Dockerfile)
- Added health check configuration
- Configured restart policy for reliability

**Configuration:**
```json
{
  "deploy": {
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10,
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100
  }
}
```

### 3. **Updated Dependencies (requirements.txt)**
Updated all packages to latest stable versions:
- `flask==3.0.3` (was 3.0.0)
- `opencv-python-headless==4.10.0.84` (was 4.8.1.78)
- `numpy==1.26.4` (was 1.26.2)
- `ultralytics==8.2.103` (was 8.0.228)
- `requests==2.32.3` (was 2.31.0)
- `Pillow==10.4.0` (was 10.1.0)
- `gunicorn==23.0.0` (was 21.2.0)

### 4. **Created .dockerignore**
Added comprehensive `.dockerignore` file to:
- Reduce Docker build context size
- Speed up builds
- Exclude unnecessary files from the container

Excludes:
- Python cache files (`__pycache__`, `*.pyc`)
- Documentation files (`*.md`)
- Git files
- IDE configurations
- Raspberry Pi specific files (`camera_stream.py`)
- Development scripts

### 5. **Updated Documentation**
- Enhanced `README.md` with Railway-specific instructions
- Improved `DEPLOY.md` with step-by-step Railway deployment guide
- Added detailed CLI command reference
- Included troubleshooting tips
- Added monitoring and health check information

## 🚀 Quick Deployment

### Prerequisites
1. Railway account ([railway.app](https://railway.app))
2. Raspberry Pi with camera stream running
3. ngrok tunnel active on Raspberry Pi

### Deploy Steps

```bash
# 1. Install Railway CLI
npm install -g @railway/cli
# or: brew install railway

# 2. Login to Railway
railway login

# 3. Initialize project (from project directory)
cd /Users/lukaschmiell/Documents/SOFT/roger
railway init

# 4. Set environment variable
railway variables set RASPBERRY_PI_URL="https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg"

# 5. Deploy!
railway up

# 6. Open your app
railway open
```

## 🔧 Configuration

### Required Environment Variable
- `RASPBERRY_PI_URL`: Your ngrok or public URL to the Raspberry Pi camera stream

### Application Features
- Health check endpoint: `/health`
- Video feed endpoint: `/video_feed`
- Main page: `/`
- Default port: 8080 (overridden by Railway's `PORT` env var)

## 📊 Monitoring

Access Railway dashboard to monitor:
- Deployment status
- Application logs
- Resource usage (CPU, Memory)
- Request metrics
- Build logs

Use CLI for logs:
```bash
railway logs           # View recent logs
railway logs -f        # Follow logs in real-time
railway status         # Check deployment status
```

## 🐛 Troubleshooting

### Build Failures
1. Check Railway build logs
2. Verify Dockerfile syntax
3. Ensure all dependencies in requirements.txt are valid

### Runtime Issues
1. Check application logs: `railway logs`
2. Verify `RASPBERRY_PI_URL` environment variable is set correctly
3. Test ngrok tunnel is active and accessible
4. Check health endpoint: `https://your-app.up.railway.app/health`

### Camera Stream Not Showing
1. Verify Raspberry Pi camera is running
2. Test ngrok URL directly in browser
3. Check if ngrok tunnel has expired (free tier has time limits)
4. Verify firewall settings on Raspberry Pi

## 📝 File Structure

```
roger/
├── app.py                  # Main Flask application
├── camera_stream.py        # Raspberry Pi camera server (not deployed)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker build configuration
├── railway.json            # Railway deployment settings
├── .dockerignore           # Files to exclude from Docker build
├── README.md               # Main documentation
├── DEPLOY.md               # Detailed deployment guide
├── RAILWAY_SETUP.md        # This file
└── ...
```

## 🎯 Next Steps

After successful deployment:
1. ✅ Test the deployed URL
2. ✅ Verify video stream is working
3. ✅ Check YOLO object detection is running
4. 🔒 Consider adding authentication
5. 🌐 Set up custom domain (optional)
6. 📊 Monitor resource usage and optimize if needed

## 💡 Pro Tips

1. **Keep ngrok Running**: Use systemd service on Raspberry Pi for persistent tunnel
2. **Monitor Costs**: Railway free tier has limits; monitor usage
3. **Optimize Performance**: Adjust worker count in Dockerfile based on usage
4. **Security**: Add authentication before sharing URL publicly
5. **Logging**: Use `railway logs -f` during first deployment to monitor startup

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app/
- ngrok Dashboard: https://dashboard.ngrok.com/
- YOLOv8 Docs: https://docs.ultralytics.com/

---

**Status**: ✅ Ready for Railway deployment!

Last updated: October 18, 2025

