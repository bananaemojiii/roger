# 🌐 ngrok Setup Required

ngrok is now installed on your Raspberry Pi, but needs an auth token to work.

## 🚀 Quick Setup (2 minutes):

### Step 1: Get ngrok Auth Token

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up for free (no credit card needed)
3. After signup, go to: https://dashboard.ngrok.com/get-started/your-authtoken
4. Copy your auth token (looks like: `2abcd...xyz`)

### Step 2: Configure ngrok on Your Raspberry Pi

Run this command (I'll do it for you once you provide the token):

```bash
ssh admn@192.168.4.102 "ngrok config add-authtoken YOUR_AUTH_TOKEN"
```

### Step 3: Start ngrok

Once configured, I'll start ngrok and get your URL automatically!

---

## 🔑 Provide Your Auth Token

Reply with your ngrok auth token and I'll configure everything automatically!

Or if you already have an account, just provide the token.

