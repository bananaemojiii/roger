# 🚀 Railway Deployment Checklist

Use this checklist to ensure a smooth deployment to Railway.

## ✅ Pre-Deployment Checklist

### Local Environment
- [ ] All files are saved and up-to-date
- [ ] Git repository is initialized (`git init`)
- [ ] Changes are committed (`git add . && git commit -m "Fix for Railway deployment"`)

### Raspberry Pi Setup
- [ ] Raspberry Pi camera is connected and working
- [ ] Camera stream script is running: `python3 camera_stream.py`
- [ ] Camera stream is accessible locally at `http://192.168.4.102:8000/stream.mjpg`
- [ ] ngrok is installed on Raspberry Pi
- [ ] ngrok tunnel is active: `ngrok http 8000`
- [ ] ngrok URL is copied (looks like: `https://xxxx-xx-xx-xxx-xx.ngrok-free.app`)

### Railway Account
- [ ] Railway account created at [railway.app](https://railway.app)
- [ ] Railway CLI installed (`npm install -g @railway/cli` or `brew install railway`)
- [ ] Logged into Railway CLI (`railway login`)

## 🚀 Deployment Steps

### Step 1: Initialize Railway Project
```bash
cd /Users/lukaschmiell/Documents/SOFT/roger
railway init
```
- [ ] Railway project created successfully
- [ ] Project name noted

### Step 2: Set Environment Variables
```bash
railway variables set RASPBERRY_PI_URL="https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg"
```
- [ ] Environment variable set correctly
- [ ] ngrok URL includes `/stream.mjpg` at the end

### Step 3: Deploy Application
```bash
railway up
```
- [ ] Build started successfully
- [ ] No build errors in the logs
- [ ] Deployment completed

### Step 4: Get Deployment URL
```bash
railway open
```
- [ ] Deployment URL obtained (format: `https://your-project-name.up.railway.app`)
- [ ] URL saved for future reference

## ✅ Post-Deployment Verification

### Health Checks
- [ ] Open Railway dashboard and check deployment status
- [ ] Visit `/health` endpoint: `https://your-project-name.up.railway.app/health`
- [ ] Health check returns: `{"status": "healthy", "raspberry_pi_url": "..."}`

### Application Testing
- [ ] Visit main URL: `https://your-project-name.up.railway.app`
- [ ] Website loads without errors
- [ ] Video stream is visible
- [ ] YOLO object detection is working (bounding boxes appear)
- [ ] UI is responsive and looks correct

### Monitoring
- [ ] Check Railway logs: `railway logs`
- [ ] No error messages in logs
- [ ] YOLO model loaded successfully
- [ ] Frames are being processed

## 🐛 Troubleshooting Guide

### If video stream doesn't show:

1. **Check ngrok tunnel:**
   ```bash
   # On Raspberry Pi
   curl https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg
   ```
   - [ ] ngrok tunnel responds correctly

2. **Check Railway environment variable:**
   ```bash
   railway variables
   ```
   - [ ] `RASPBERRY_PI_URL` is set correctly

3. **Check Railway logs:**
   ```bash
   railway logs -f
   ```
   - [ ] Look for connection errors
   - [ ] Check if YOLO model loaded

4. **Test camera stream directly:**
   - [ ] Open ngrok URL in browser: `https://YOUR-NGROK-URL.ngrok-free.app/stream.mjpg`

### If build fails:

1. **Check Dockerfile:**
   - [ ] Dockerfile syntax is correct
   - [ ] All required files are present

2. **Check requirements.txt:**
   - [ ] All package versions are valid
   - [ ] No typos in package names

3. **Review build logs:**
   - [ ] Read Railway build logs carefully
   - [ ] Note any error messages

### If app crashes:

1. **Check application logs:**
   ```bash
   railway logs
   ```
   - [ ] Look for Python errors
   - [ ] Check for missing dependencies

2. **Verify environment:**
   - [ ] PORT is being set by Railway
   - [ ] RASPBERRY_PI_URL is accessible

## 📊 Success Criteria

Your deployment is successful when:
- ✅ Railway deployment shows "Active" status
- ✅ Health check endpoint returns healthy status
- ✅ Main page loads without errors
- ✅ Video stream is visible and updating
- ✅ YOLO bounding boxes appear on detected objects
- ✅ No errors in Railway logs

## 🔄 Redeployment

If you need to redeploy:

```bash
# Make your changes
git add .
git commit -m "Your changes"

# Redeploy
railway up
```

Or if using GitHub:
```bash
git push origin main
# Railway will auto-deploy
```

## 💡 Quick Commands Reference

```bash
# View logs
railway logs
railway logs -f    # Follow logs

# Check status
railway status

# List variables
railway variables

# Set variable
railway variables set KEY=value

# Open app
railway open

# SSH into container
railway run bash
```

## 📞 Support

If you encounter issues:

1. Check Railway documentation: https://docs.railway.app/
2. Review application logs: `railway logs`
3. Verify all checklist items above
4. Check Railway status page: https://railway.app/status

---

**Happy Deploying! 🎉**

Created: October 18, 2025
Project: Roger - Global Camera Stream with YOLO

