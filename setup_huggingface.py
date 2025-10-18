#!/usr/bin/env python3
"""
Setup script to upload YOLO model to Hugging Face
"""

import os
import sys
from pathlib import Path

def setup_huggingface():
    print("🤗 Hugging Face Model Storage Setup\n")
    
    # Get user info
    print("Please provide:")
    hf_username = input("1. Your Hugging Face username: ").strip()
    hf_token = input("2. Your HF token (from https://huggingface.co/settings/tokens): ").strip()
    
    if not hf_username or not hf_token:
        print("❌ Username and token are required!")
        sys.exit(1)
    
    print(f"\n✅ Configuration:")
    print(f"   Username: {hf_username}")
    print(f"   Token: hf_{'*' * 30}")
    
    # Install required packages
    print("\n📦 Installing huggingface_hub...")
    os.system("pip install -q huggingface_hub")
    
    from huggingface_hub import HfApi, create_repo, hf_hub_download
    
    # Create repository
    repo_name = f"{hf_username}/yolov8-camera-model"
    print(f"\n🏗️  Creating repository: {repo_name}")
    
    try:
        api = HfApi()
        create_repo(
            repo_id=repo_name,
            token=hf_token,
            exist_ok=True,
            private=False  # Public repo (change to True for private)
        )
        print(f"✅ Repository created: https://huggingface.co/{repo_name}")
    except Exception as e:
        print(f"⚠️  Repository might already exist or error: {e}")
    
    # Download YOLOv8n model locally first
    print("\n📥 Downloading YOLOv8n model...")
    from ultralytics import YOLO
    model = YOLO('yolov8n.pt')  # This downloads it
    model_path = Path.home() / '.cache' / 'ultralytics' / 'yolov8n.pt'
    
    if not model_path.exists():
        # Try current directory
        model_path = Path('yolov8n.pt')
        if not model_path.exists():
            print("❌ Could not find yolov8n.pt")
            sys.exit(1)
    
    print(f"✅ Model found: {model_path}")
    
    # Upload to Hugging Face
    print(f"\n📤 Uploading to Hugging Face...")
    try:
        api.upload_file(
            path_or_fileobj=str(model_path),
            path_in_repo="yolov8n.pt",
            repo_id=repo_name,
            token=hf_token,
            commit_message="Add YOLOv8n model"
        )
        print(f"✅ Model uploaded successfully!")
        print(f"   View at: https://huggingface.co/{repo_name}/blob/main/yolov8n.pt")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        sys.exit(1)
    
    # Generate updated app.py code
    print("\n" + "="*60)
    print("📝 NEXT STEPS:")
    print("="*60)
    
    print("\n1. Add to Railway environment variables:")
    print(f"   HUGGINGFACE_TOKEN={hf_token}")
    print(f"   HUGGINGFACE_REPO={repo_name}")
    
    print("\n2. Update requirements.txt - add:")
    print("   huggingface_hub")
    
    print("\n3. I'll update app.py to use your HF model!")
    print("\n✅ Setup complete!")
    
    return {
        'username': hf_username,
        'token': hf_token,
        'repo': repo_name
    }

if __name__ == "__main__":
    try:
        config = setup_huggingface()
        
        # Save config for later use
        with open('hf_config.txt', 'w') as f:
            f.write(f"HUGGINGFACE_REPO={config['repo']}\n")
            f.write(f"HUGGINGFACE_TOKEN={config['token']}\n")
        
        print(f"\n💾 Config saved to: hf_config.txt")
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

