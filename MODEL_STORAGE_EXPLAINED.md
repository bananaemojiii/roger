# 🤖 YOLO Model Storage & Architecture

## Current Setup

### Where is the YOLO model stored?

**Answer: On Railway (in the Docker container)**

```python
model = YOLO('yolov8n.pt')  # Line 24 in app.py
```

### How it works:

```
┌─────────────────────────────────────────────────────────────┐
│                    CURRENT ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────┘

1. Raspberry Pi (192.168.4.102)
   ├── camera_stream.py running
   ├── Captures video from camera
   ├── Serves raw MJPEG stream on port 8000
   └── No AI processing here!

2. Cloudflare Tunnel
   ├── Exposes Pi stream to internet
   └── URL: bundle-payday-nelson-dim.trycloudflare.com

3. Railway Server (app.py)
   ├── Downloads yolov8n.pt on first startup (~6MB)
   ├── Stored in: /root/.cache/ultralytics/ (inside container)
   ├── Fetches frames from Cloudflare URL
   ├── Runs YOLO inference on each frame
   ├── Draws bounding boxes
   └── Streams to user's browser

4. User's Browser
   └── Sees processed video with bounding boxes
```

## Model Details

### YOLOv8 Nano (`yolov8n.pt`)

**What it is:**
- Pre-trained model by Ultralytics
- Trained on COCO dataset (80 object classes)
- Size: ~6 MB
- Speed: ~45 FPS on CPU

**Where it's downloaded from:**
```
https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

**When it's downloaded:**
- First time Railway container starts
- Automatically by ultralytics library
- Cached in container

**Storage locations:**

| Environment | Location | Persistent? |
|-------------|----------|-------------|
| **Railway Container** | `/root/.cache/ultralytics/` | ❌ No (rebuilds wipe it) |
| **Your Mac** | `~/.cache/ultralytics/` | ✅ Yes (if you run locally) |
| **Raspberry Pi** | N/A (not used there) | N/A |

## Training Data vs Pre-trained Model

### What you're using: **Pre-trained Model**

```python
model = YOLO('yolov8n.pt')  # Pre-trained on COCO dataset
```

**COCO Dataset (what it knows):**
- 80 object classes
- Examples: person, car, dog, cat, cup, laptop, phone, etc.
- Trained on 120,000+ images
- You don't need the training data - just the model!

### If you want Custom Training:

You would need to:
1. Collect your own images
2. Label them (bounding boxes)
3. Train a new model
4. Replace `yolov8n.pt` with your custom model

## Storage Options for Custom Models

### Option 1: Include in Docker Image (Current approach)
```dockerfile
# In Dockerfile
COPY my_custom_model.pt /app/
```

**Pros:**
- ✅ Model always available
- ✅ Fast startup

**Cons:**
- ❌ Larger Docker image
- ❌ Must rebuild to update model

### Option 2: Download on Startup
```python
import urllib.request
urllib.request.urlretrieve(
    'https://your-server.com/model.pt',
    'model.pt'
)
model = YOLO('model.pt')
```

**Pros:**
- ✅ Can update model without rebuild
- ✅ Smaller Docker image

**Cons:**
- ❌ Slower startup (downloads each time)
- ❌ Needs external hosting

### Option 3: Railway Volume (Persistent Storage)
```python
# Store in mounted volume
model = YOLO('/data/model.pt')
```

**Pros:**
- ✅ Persistent across deployments
- ✅ Can update without rebuild
- ✅ Download once

**Cons:**
- ❌ Costs extra on Railway
- ❌ More complex setup

### Option 4: Cloud Storage (S3, Google Cloud Storage)
```python
import boto3
s3 = boto3.client('s3')
s3.download_file('my-bucket', 'model.pt', 'model.pt')
model = YOLO('model.pt')
```

**Pros:**
- ✅ Centralized model management
- ✅ Easy to update
- ✅ Can version models

**Cons:**
- ❌ Costs money
- ❌ Slower startup
- ❌ Needs credentials

## Current Model Performance

### YOLOv8n Statistics:
- **Speed**: ~45 FPS on CPU
- **Accuracy**: 37.3% mAP (COCO)
- **Size**: 6.2 MB
- **Parameters**: 3.2M

### Available YOLO Models:

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `yolov8n.pt` | 6MB | Fastest | Good | **Current (best for Railway free tier)** |
| `yolov8s.pt` | 22MB | Fast | Better | More accurate, still fast |
| `yolov8m.pt` | 52MB | Medium | Great | Balanced |
| `yolov8l.pt` | 87MB | Slow | Excellent | High accuracy |
| `yolov8x.pt` | 136MB | Slowest | Best | Maximum accuracy |

## Where Training Data Would Go (if you train custom models)

### For Training:
```
Your Local Machine / Training Server
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   └── labels/
│       ├── train/
│       └── val/
├── train.py
└── yolov8n.pt (starting point)
```

### After Training:
```
1. Train locally → produces: my_custom_model.pt
2. Upload to Railway (one of options above)
3. Update app.py: model = YOLO('my_custom_model.pt')
```

## Current Storage Summary

**Right Now:**

```
Raspberry Pi:
├── camera_stream.py ✅
├── Video frames (not stored, streamed) ✅
└── No YOLO model ✅

Railway Container:
├── app.py ✅
├── yolov8n.pt (downloaded on startup) ✅
├── Python packages ✅
└── Temporary: deleted on redeploy ⚠️

Your Mac (this project):
├── app.py (source code) ✅
├── Dockerfile ✅
├── requirements.txt ✅
└── No model files (not needed) ✅
```

## If You Want to Train Your Own Model

### Quick Guide:

1. **Collect & Label Data** (locally):
   ```bash
   # Use tools like:
   - Roboflow (easiest)
   - LabelImg
   - CVAT
   ```

2. **Train Model** (locally or Colab):
   ```python
   from ultralytics import YOLO
   model = YOLO('yolov8n.pt')
   model.train(data='your_dataset.yaml', epochs=100)
   ```

3. **Export Best Model**:
   ```bash
   runs/detect/train/weights/best.pt
   ```

4. **Deploy to Railway**:
   ```python
   # In app.py, change:
   model = YOLO('best.pt')  # Your custom model
   ```

5. **Copy to Docker**:
   ```dockerfile
   # In Dockerfile, add:
   COPY best.pt /app/
   ```

## Recommendations

### For Current Setup (Pre-trained):
✅ Perfect! No changes needed
- Model downloads automatically
- Works great for general objects
- Free tier friendly

### If You Need Custom Objects:
- Train locally or on Colab (free GPU)
- Store trained model in Docker image
- ~100-500 images per class needed

### If You Need Multiple Models:
- Use Railway volumes ($5/month)
- Or S3/Cloud Storage ($0.02/GB)
- Load different models dynamically

---

**Bottom Line**: 
- ✅ YOLO model lives on **Railway** (downloads on startup)
- ✅ Training data **not needed** (using pre-trained)
- ✅ Raspberry Pi **only streams video** (no AI)
- ✅ Current setup is **optimal for your use case**!

Want to train a custom model for specific objects?

