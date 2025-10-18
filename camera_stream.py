#!/usr/bin/env python3
"""
Simple Camera Stream Server for Raspberry Pi
Streams camera feed via web browser
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition
import io
import time

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/stream.html')
            self.end_headers()
        elif self.path == '/stream.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                print(f'Removed streaming client {self.client_address}: {str(e)}')
        else:
            self.send_error(404)
            self.end_headers()


PAGE = """\
<html>
<head>
<title>Raspberry Pi Camera Stream</title>
<style>
body {
    margin: 0;
    padding: 20px;
    background-color: #1a1a1a;
    color: white;
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}
h1 {
    margin-bottom: 20px;
}
img {
    max-width: 90vw;
    max-height: 80vh;
    border: 2px solid #333;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}
.info {
    margin-top: 20px;
    font-size: 14px;
    color: #888;
}
</style>
</head>
<body>
<h1>📹 Raspberry Pi Camera Stream</h1>
<img src="stream.mjpg" />
<div class="info">
    Stream active | Press Ctrl+C on the Pi to stop
</div>
</body>
</html>
"""


if __name__ == '__main__':
    try:
        # Initialize camera
        print("Initializing camera...")
        picam2 = Picamera2()
        config = picam2.create_video_configuration(main={"size": (640, 480)})
        picam2.configure(config)
        
        output = StreamingOutput()
        encoder = JpegEncoder()
        
        print("Starting camera...")
        picam2.start_recording(encoder, FileOutput(output))
        
        # Start web server
        address = ('', 8000)
        server = HTTPServer(address, StreamingHandler)
        print(f"\n✅ Camera stream started!")
        print(f"📺 View at: http://192.168.4.102:8000")
        print(f"Press Ctrl+C to stop\n")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n\nStopping camera stream...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'picam2' in locals():
            picam2.stop_recording()
        print("Camera stopped.")

