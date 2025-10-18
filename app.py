#!/usr/bin/env python3
"""
Remote Camera Stream with YOLO Object Detection
Accessible from anywhere via Railway deployment
"""

from flask import Flask, Response, render_template_string
import cv2
import numpy as np
from ultralytics import YOLO
import requests
from io import BytesIO
import time
import os

app = Flask(__name__)

# Configuration
RASPBERRY_PI_URL = os.environ.get('RASPBERRY_PI_URL', 'http://192.168.4.102:8000/stream.mjpg')
PORT = int(os.environ.get('PORT', 8080))

# Initialize YOLO model
print("Loading YOLO model...")
model = YOLO('yolov8n.pt')  # Using YOLOv8 nano for speed
print("YOLO model loaded!")

class CameraStream:
    def __init__(self):
        self.frame = None
        self.last_update = time.time()
        
    def get_frame_from_pi(self):
        """Fetch frame from Raspberry Pi camera stream"""
        try:
            response = requests.get(RASPBERRY_PI_URL, stream=True, timeout=5)
            bytes_data = b''
            
            for chunk in response.iter_content(chunk_size=1024):
                bytes_data += chunk
                a = bytes_data.find(b'\xff\xd8')  # JPEG start
                b = bytes_data.find(b'\xff\xd9')  # JPEG end
                
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b+2]
                    bytes_data = bytes_data[b+2:]
                    
                    # Decode JPEG
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if frame is not None:
                        return frame
                        
        except Exception as e:
            print(f"Error fetching frame: {e}")
            return None
    
    def process_frame_with_yolo(self, frame):
        """Apply YOLO object detection to frame"""
        if frame is None:
            return None
            
        # Run YOLO inference
        results = model(frame, verbose=False)
        
        # Draw bounding boxes and labels
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Get box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Get confidence and class
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                
                # Draw bounding box
                color = (0, 255, 0)  # Green
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                
                # Draw label background
                label = f'{class_name} {confidence:.2f}'
                (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame, (x1, y1 - label_height - 10), (x1 + label_width, y1), color, -1)
                
                # Draw label text
                cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.6, (0, 0, 0), 2)
        
        return frame
    
    def generate_frames(self):
        """Generate frames with YOLO detection"""
        while True:
            frame = self.get_frame_from_pi()
            
            if frame is not None:
                # Process with YOLO
                processed_frame = self.process_frame_with_yolo(frame)
                
                if processed_frame is not None:
                    # Encode frame as JPEG
                    ret, buffer = cv2.imencode('.jpg', processed_frame)
                    if ret:
                        frame_bytes = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            time.sleep(0.033)  # ~30 FPS

camera = CameraStream()

@app.route('/')
def index():
    """Home page with camera stream"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(camera.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/health')
def health():
    """Health check endpoint for Railway"""
    return {'status': 'healthy', 'raspberry_pi_url': RASPBERRY_PI_URL}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🌍 Global Camera Stream with YOLO</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 1200px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .video-container {
            position: relative;
            width: 100%;
            background: #000;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        
        #stream {
            width: 100%;
            height: auto;
            display: block;
        }
        
        .status-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(34, 197, 94, 0.9);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .pulse {
            width: 10px;
            height: 10px;
            background: white;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        .info-panel {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .info-item {
            text-align: center;
        }
        
        .info-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }
        
        .footer {
            margin-top: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 1.8em;
            }
            
            .container {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 Global Camera Stream</h1>
        <p class="subtitle">Live feed with AI-powered YOLO object detection</p>
        
        <div class="video-container">
            <img id="stream" src="{{ url_for('video_feed') }}" alt="Camera Stream">
            <div class="status-badge">
                <span class="pulse"></span>
                LIVE
            </div>
        </div>
        
        <div class="info-panel">
            <div class="info-item">
                <div class="info-label">🤖 AI Model</div>
                <div class="info-value">YOLOv8</div>
            </div>
            <div class="info-item">
                <div class="info-label">📡 Status</div>
                <div class="info-value">Streaming</div>
            </div>
            <div class="info-item">
                <div class="info-label">🌐 Access</div>
                <div class="info-value">Worldwide</div>
            </div>
        </div>
        
        <div class="footer">
            <p>🚀 Powered by Railway | YOLOv8 Object Detection | Raspberry Pi Camera</p>
        </div>
    </div>
    
    <script>
        // Reload image if it fails to load
        document.getElementById('stream').onerror = function() {
            setTimeout(() => {
                this.src = "{{ url_for('video_feed') }}?" + new Date().getTime();
            }, 5000);
        };
        
        // Update timestamp
        setInterval(() => {
            const img = document.getElementById('stream');
            const current = img.src;
            if (!current.includes('?')) {
                img.src = current + '?' + new Date().getTime();
            }
        }, 60000); // Refresh every minute
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print(f"Starting server on port {PORT}...")
    print(f"Connecting to Raspberry Pi at: {RASPBERRY_PI_URL}")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)

