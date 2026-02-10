# 🚀 Vercel Deployment - Step by Step Fix

## 🔍 Problem Summary

**You have 6 Vercel deployments, all showing 404 errors because:**
1. Multiple duplicate projects created (`vibe-coder2-0`, `vibe-coder2-0-w22r`, etc.)
2. Root directory not set to `frontend`
3. Build command using `cd frontend &&` which Vercel doesn't handle properly

---

## ✅ Solution (Follow These Steps)

### Step 1: Delete Extra Vercel Projects

1. Go to **[Vercel Dashboard](https://vercel.com/dashboard)**
2. You'll see 6 projects - **delete 5 of them**, keep only **`vibe-coder2.0`** (or your preferred one)
3. For each project to delete:
   - Click on the project name
   - Go to **Settings** tab
   - Scroll to bottom → **Delete Project**
   - Type the project name to confirm

### Step 2: Configure the Remaining Project

1. **Open your kept project** (e.g., `vibe-coder2.0`)
2. Go to **Settings** → **General**
3. **Root Directory** section:
   - Click **Edit**
   - Change from `.` (root) to `frontend`
   - Click **Save**

4. **Build & Development Settings**:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
   - Click **Save**

5. **Environment Variables**:
   - Click **Environment Variables** tab
   - Add new variable:
     - **Key**: `VITE_API_URL`
     - **Value**: `https://vibeframe-backend.onrender.com` (update with your actual backend URL)
     - **Environment**: Production, Preview, Development (select all)
   - Click **Save**

### Step 3: Trigger Redeploy

1. Go to **Deployments** tab
2. Click the **⋯** (three dots) on the latest deployment
3. Click **Redeploy**
4. Wait 2-3 minutes for build to complete

### Step 4: Test Your Deployment

1. Once deployed, click **Visit** to open your site
2. You should see your VibeFrame landing page (no more 404!)
3. Test uploading a video (it will fail until backend is deployed)

---

## 🎯 Alternative: Fresh Deployment

If you want to start clean:

### Delete All Projects
1. Delete all 6 Vercel projects from dashboard

### Create New Deployment
1. Go to https://vercel.com/new
2. **Import Git Repository**
3. Select `Prince2005kumar/vibe-coder2.0`
4. **Configure Project**:
   - **Project Name**: `vibeframe` (or your choice)
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend` ← **IMPORTANT!**
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`
5. **Environment Variables**:
   - Add `VITE_API_URL` = `https://vibeframe-backend.onrender.com`
6. Click **Deploy**
7. Wait 2-3 minutes

---

## 📋 Updated Files

I've updated your `vercel.json` to work correctly with the Root Directory setting:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install"
}
```

**Note**: The `vercel.json` file should be in the `frontend/` directory, not the repository root. Let me move it there.

---

## 🔧 What Changed

### Before (Broken):
- `vercel.json` in root with `cd frontend &&` command
- No root directory set in Vercel
- Result: 404 errors

### After (Fixed):
- Root Directory set to `frontend` in Vercel dashboard
- Simple build commands in `vercel.json`
- `vercel.json` moved to `frontend/` directory
- Result: ✅ Working deployment

---

## 🆘 Still Getting 404?

### Check These:

1. **Root Directory**: Must be set to `frontend` in Vercel dashboard
2. **Build Logs**: Check if build succeeded
   - Go to Deployments → Click on deployment → View Build Logs
   - Look for errors
3. **Output Directory**: Should show files in `dist/`
4. **Environment Variables**: `VITE_API_URL` must be set

### Common Issues:

| Issue | Solution |
|-------|----------|
| "Cannot find package.json" | Root directory not set to `frontend` |
| "Build failed" | Check build logs for errors |
| "404 on all pages" | Output directory wrong or build didn't produce files |
| "CORS errors" | Backend not deployed or FRONTEND_URL not set |

---

## ✅ Success Checklist

- [ ] Deleted extra Vercel projects (keep only 1)
- [ ] Set Root Directory to `frontend`
- [ ] Configured build settings correctly
- [ ] Added `VITE_API_URL` environment variable
- [ ] Redeployed successfully
- [ ] Site loads without 404
- [ ] (Optional) Deploy backend to Render
- [ ] (Optional) Update `VITE_API_URL` with actual backend URL

---

## 🎉 Next Steps

Once your frontend is working:

1. **Deploy Backend to Render** (see `QUICK_DEPLOY.md`)
2. **Update Environment Variables**:
   - In Vercel: Set `VITE_API_URL` to your Render backend URL
   - In Render: Set `FRONTEND_URL` to your Vercel frontend URL
3. **Test End-to-End**: Upload a video and verify frame extraction works

---

**Need help?** Share:
- Your Vercel project URL
- Build logs (if deployment fails)
- Error messages from browser console (F12)
