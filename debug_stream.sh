#!/bin/bash
# Debug script to check stream connectivity

echo "🔍 Debugging camera stream connection..."
echo ""

echo "1. Checking Raspberry Pi processes:"
ssh admn@192.168.4.102 "ps aux | grep -E '(camera_stream|ngrok)' | grep -v grep"
echo ""

echo "2. Testing local camera stream:"
ssh admn@192.168.4.102 "timeout 2 curl -s http://localhost:8000/ 2>&1 | head -5"
echo ""

echo "3. Getting current ngrok URL:"
NGROK_URL=$(ssh admn@192.168.4.102 "curl -s http://localhost:4040/api/tunnels 2>/dev/null" | grep -o '"public_url":"https://[^"]*' | cut -d'"' -f4)
echo "Current ngrok URL: $NGROK_URL"
echo ""

echo "4. Testing ngrok tunnel homepage:"
curl -s "$NGROK_URL/" 2>&1 | head -5
echo ""

echo "5. Current Railway variable should be:"
echo "RASPBERRY_PI_URL=\"${NGROK_URL}/stream.mjpg\""
echo ""

echo "✅ If all tests pass, the issue might be ngrok's browser warning page."
echo "   ngrok free tier shows a warning page before allowing access."
echo "   Solution: Railway needs to handle the redirect or upgrade ngrok plan."

