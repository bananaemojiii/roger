#!/bin/bash

# One-command deployment script for Railway
# This will guide you through the entire deployment process

set -e

echo "🚀 Railway Camera Stream Deployment Script"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git branch -m main
    git add .
    git commit -m "Initial commit: Camera stream with YOLO"
    echo "✅ Git repository initialized"
    echo ""
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI is not installed"
    echo ""
    echo "Please install it first:"
    echo "  npm install -g @railway/cli"
    echo "  or"
    echo "  brew install railway"
    echo ""
    exit 1
fi

echo "✅ Railway CLI found"
echo ""

# Check if logged in to Railway
echo "🔐 Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "Please login to Railway:"
    railway login
    echo ""
fi

echo "✅ Authenticated with Railway"
echo ""

# Get ngrok URL
echo "📡 Camera Stream Configuration"
echo "================================"
echo ""
echo "Enter your Raspberry Pi camera stream URL:"
echo "(Example: https://xxxx-xx-xx-xxx-xx.ngrok-free.app/stream.mjpg)"
echo ""
read -p "RASPBERRY_PI_URL: " CAMERA_URL

if [ -z "$CAMERA_URL" ]; then
    echo "❌ URL cannot be empty"
    exit 1
fi

echo ""
echo "Testing camera URL..."
if curl -s --head --request GET "$CAMERA_URL" | grep "200\|301\|302" > /dev/null; then
    echo "✅ Camera URL is accessible"
else
    echo "⚠️  Warning: Could not verify camera URL"
    echo "Continuing anyway..."
fi

echo ""

# Check if project exists
if ! railway status &> /dev/null; then
    echo "📦 Creating new Railway project..."
    railway init
    echo ""
fi

echo "⚙️  Setting environment variable..."
railway variables set RASPBERRY_PI_URL="$CAMERA_URL"
echo "✅ Environment variable set"
echo ""

echo "🚀 Deploying to Railway..."
echo ""
railway up

echo ""
echo "======================================"
echo "✅ Deployment Complete!"
echo "======================================"
echo ""
echo "🌐 Opening your deployed app..."
railway open

echo ""
echo "📊 Useful commands:"
echo "  railway logs       - View live logs"
echo "  railway status     - Check deployment status"
echo "  railway open       - Open your app in browser"
echo "  railway variables  - View/edit environment variables"
echo ""
echo "🎉 Your camera is now accessible worldwide!"
echo ""

