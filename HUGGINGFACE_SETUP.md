# 🤗 Hugging Face Model Storage Setup

## What I Need From You:

### Option 1: Hugging Face Token (Recommended)
1. Go to: https://huggingface.co/settings/tokens
2. Create a new token (read access is enough for downloading)
3. Give me the token (starts with `hf_...`)

### Option 2: Public Repository (No token needed)
Just your Hugging Face username and we'll create a public model repo

## How It Will Work:

```
┌──────────────────────────────────────────────────┐
│  Hugging Face (Model Storage)                    │
├──────────────────────────────────────────────────┤
│  📦 your-username/yolov8-camera-model            │
│     • yolov8n.pt (6MB)                           │
│     • Or your custom trained model               │
│     • Version controlled                         │
│     • Free hosting                               │
└──────────────────────────────────────────────────┘
                      ↓ downloads on startup
┌──────────────────────────────────────────────────┐
│  Railway Container                               │
├──────────────────────────────────────────────────┤
│  • Downloads model from HF on startup            │
│  • Caches locally                                │
│  • Updates when you push new version            │
└──────────────────────────────────────────────────┘
```

## Benefits:

✅ **Version Control**: Track model versions
✅ **Easy Updates**: Push new model, Railway auto-downloads
✅ **Free Storage**: Unlimited model hosting
✅ **Model Cards**: Document your model
✅ **Share**: Make public or keep private
✅ **Fast CDN**: Quick downloads worldwide

## Setup Steps:

### 1. Create Repository
I'll create: `your-username/yolov8-camera-model`

### 2. Upload Current Model
```python
# Will upload yolov8n.pt (the one we're using now)
```

### 3. Update app.py
```python
from huggingface_hub import hf_hub_download

# Download model from your HF repo
model_path = hf_hub_download(
    repo_id="your-username/yolov8-camera-model",
    filename="yolov8n.pt",
    token="YOUR_TOKEN"  # Optional for public repos
)
model = YOLO(model_path)
```

### 4. Set Railway Environment Variable
```bash
HUGGINGFACE_TOKEN=hf_your_token_here
```

## Custom Model Training & Upload

### If you train a custom model:

```python
from huggingface_hub import HfApi

# After training
api = HfApi()
api.upload_file(
    path_or_fileobj="runs/detect/train/weights/best.pt",
    path_in_repo="yolov8-custom.pt",
    repo_id="your-username/yolov8-camera-model",
    token="YOUR_TOKEN"
)
```

Then Railway automatically uses the new model!

## Cost:

**FREE!** ✅
- Unlimited public models
- Private repos: Free for small models (<50GB)


