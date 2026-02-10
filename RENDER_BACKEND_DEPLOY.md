# 🚀 Deploy Backend to Render - Step by Step

## Prerequisites
- ✅ GitHub repository: `https://github.com/Prince2005kumar/vibe-coder2.0.git`
- ✅ Render account (free): https://render.com/

---

## 📋 Step-by-Step Deployment

### Step 1: Sign Up / Log In to Render

1. Go to **[Render.com](https://render.com/)**
2. Click **"Get Started for Free"** or **"Sign In"**
3. Sign in with GitHub (recommended for easy repo access)

### Step 2: Create New Web Service

1. Once logged in, click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see "Create a new Web Service" page

### Step 3: Connect Your Repository

1. **Connect GitHub Account** (if not already connected):
   - Click **"Connect GitHub"**
   - Authorize Render to access your repositories
   
2. **Find Your Repository**:
   - Search for `vibe-coder2.0` or `Prince2005kumar/vibe-coder2.0`
   - Click **"Connect"** next to your repository

### Step 4: Configure Your Service

Fill in these settings **exactly**:

#### Basic Settings
- **Name**: `vibeframe-backend` (or any name you prefer)
- **Region**: `Oregon` (or closest to you: Frankfurt, Singapore)
- **Branch**: `main`
- **Root Directory**: `backend` ← **IMPORTANT!**

#### Build Settings
- **Runtime**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

#### Instance Type
- **Free** (for testing) or **Starter** ($7/month, recommended for production)

### Step 5: Add Environment Variables

Scroll down to **"Environment Variables"** section:

1. Click **"Add Environment Variable"**
2. Add these variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `FRONTEND_URL` | `https://your-vercel-app.vercel.app` (update after deploying frontend) |

> **Note**: You can add `FRONTEND_URL` later once you have your Vercel URL

### Step 6: Add Persistent Disk (Important!)

Your app needs storage for uploaded videos and extracted frames.

1. Scroll to **"Disks"** section
2. Click **"Add Disk"**
3. Configure:
   - **Name**: `vibeframe-storage`
   - **Mount Path**: `/opt/render/project/src/uploads`
   - **Size**: `10 GB` (free tier allows up to 10GB)
4. Click **"Add Disk"**

### Step 7: Create Web Service

1. Review all settings
2. Click **"Create Web Service"** button at the bottom
3. Render will start building your app

### Step 8: Monitor the Build

1. You'll be redirected to your service dashboard
2. Click on **"Logs"** tab to watch the build progress
3. Build process takes **5-10 minutes** (downloading PyTorch, CLIP, YOLO models)

**Expected log output:**
```
==> Cloning from https://github.com/Prince2005kumar/vibe-coder2.0...
==> Checking out commit 99a2e33...
==> Running build command 'pip install -r requirements.txt'...
Collecting fastapi
Collecting uvicorn[standard]
...
Installing collected packages: torch, torchvision, clip, ultralytics...
==> Build successful!
==> Starting service with 'uvicorn main:app --host 0.0.0.0 --port $PORT'
INFO: Started server process
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:10000
```

### Step 9: Get Your Backend URL

1. Once build completes, you'll see **"Live"** status (green dot)
2. Your backend URL will be shown at the top:
   ```
   https://vibeframe-backend.onrender.com
   ```
3. **Copy this URL** - you'll need it for the frontend

### Step 10: Test Your Backend

1. Click on your backend URL or visit:
   ```
   https://vibeframe-backend.onrender.com/docs
   ```
2. You should see the **FastAPI Swagger documentation** page
3. Try the **GET /** endpoint - should return:
   ```json
   {"message": "VibeFrame API is running"}
   ```

---

## ✅ Success Checklist

- [ ] Render account created
- [ ] Repository connected
- [ ] Root directory set to `backend`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables added (`PYTHON_VERSION`)
- [ ] Persistent disk added (10GB)
- [ ] Service created and building
- [ ] Build completed successfully
- [ ] Service shows "Live" status
- [ ] Backend URL copied
- [ ] API docs accessible at `/docs`

---

## 🔧 Common Issues & Solutions

### Issue 1: Build Fails - "No module named 'cv2'"

**Cause**: Missing OpenCV dependency

**Solution**: Already fixed! Your `requirements.txt` has `opencv-python-headless`

### Issue 2: Build Fails - "Could not find a version that satisfies torch"

**Cause**: Python version too old

**Solution**: Add environment variable `PYTHON_VERSION=3.11.0`

### Issue 3: Service Crashes on Startup

**Cause**: Port not configured correctly

**Solution**: Ensure start command uses `$PORT` (not hardcoded 8000)

### Issue 4: "502 Bad Gateway" When Accessing URL

**Cause**: Service crashed after starting

**Solution**: 
1. Check **Logs** tab for errors
2. Look for Python errors or missing dependencies
3. Common fix: Restart the service (Settings → Manual Deploy → Deploy Latest Commit)

### Issue 5: Disk Not Mounted

**Cause**: Mount path incorrect

**Solution**: Ensure mount path is `/opt/render/project/src/uploads` (matches your code)

---

## 🔄 Update Your Frontend

Once backend is deployed, update your frontend to use the backend URL:

1. **Update `frontend/.env.production`**:
   ```env
   VITE_API_URL=https://vibeframe-backend.onrender.com
   ```

2. **Commit and push**:
   ```bash
   git add frontend/.env.production
   git commit -m "Update backend URL for production"
   git push
   ```

3. **Vercel will auto-redeploy** with the new backend URL

---

## 💰 Render Free Tier Limitations

- **Spins down after 15 minutes** of inactivity
- **First request takes ~30 seconds** to wake up
- **750 hours/month** of runtime

**For production**: Upgrade to Starter plan ($7/month) for:
- Always-on service
- No spin-down delays
- Better performance

---

## 🎉 Next Steps

1. ✅ Backend deployed on Render
2. ⏭️ Update frontend environment variables
3. ⏭️ Update Render `FRONTEND_URL` with your Vercel URL
4. ⏭️ Test end-to-end: Upload video → Extract frames

---

## 📞 Need Help?

**If deployment fails:**
1. Check the **Logs** tab in Render dashboard
2. Look for the first error message
3. Share the error with me for troubleshooting

**Common log locations:**
- Build logs: During "Building..." phase
- Runtime logs: After "Live" status
- Error logs: Red text in logs

---

**Your backend will be live at**: `https://vibeframe-backend-XXXX.onrender.com`

(Replace XXXX with your actual service name)
