# Deploy to Render - Complete Guide

## Option 1: Update Existing Render Service (Recommended)

If you already have a live website on Render and want to replace it:

### Step 1: Prepare Your Code

1. **Make sure all changes are committed to Git:**
   ```powershell
   git status
   git add .
   git commit -m "Final version with URL fixes and company extraction"
   git push origin main
   ```

2. **Verify your repository is connected to Render:**
   - Go to your Render Dashboard
   - Find your existing service
   - Check that it's connected to the correct GitHub repository

### Step 2: Update Environment Variables

1. **Go to your Render service dashboard**
2. **Click on "Environment" tab**
3. **Update/Add these environment variables:**

   ```
   GOOGLE_API_KEY=your_google_api_key_here
   SECRET_KEY=your_secret_key_here
   FLASK_ENV=production
   PORT=10000
   ```

   **To generate SECRET_KEY:**
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Step 3: Trigger Manual Deploy

1. **In your Render service dashboard:**
   - Click on "Manual Deploy" → "Deploy latest commit"
   - OR just push to your main branch (auto-deploy)

2. **Wait for deployment to complete**
   - Check the "Logs" tab for any errors
   - Deployment usually takes 2-5 minutes

### Step 4: Verify Deployment

1. **Check your live URL**
2. **Test the application:**
   - Login/Register
   - Search for questions
   - Verify company names appear
   - Check that "View Problem" links work

---

## Option 2: Create New Service (If Starting Fresh)

### Step 1: Prepare Repository

1. **Create/Update .gitignore:**
   ```
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   venv/
   env/
   ENV/

   # Database
   *.db
   instance/
   users.db

   # Environment
   .env
   .env.local

   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo

   # OS
   .DS_Store
   Thumbs.db

   # Logs
   *.log
   related_questions.json
   ```

2. **Commit and push to GitHub:**
   ```powershell
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

### Step 2: Create Web Service on Render

1. **Go to [Render Dashboard](https://dashboard.render.com)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository:**
   - Select your repository
   - Authorize Render if needed

### Step 3: Configure Service

**Basic Settings:**
- **Name**: `coding-questions-finder` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main` (or `master`)
- **Root Directory**: Leave empty (if app.py is in root)

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

### Step 4: Set Environment Variables

Click "Advanced" → "Add Environment Variable" and add:

```
GOOGLE_API_KEY=your_google_api_key_here
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
```

**Generate SECRET_KEY:**
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 5: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (2-5 minutes)
3. **Check logs** for any errors
4. **Access your app** at the provided URL

---

## Important Notes for Render Deployment

### Database Considerations

⚠️ **SQLite Limitation**: SQLite files are stored on disk and will be lost on each deployment. For production, consider:

1. **Option A: Use Render PostgreSQL (Recommended)**
   - Create a PostgreSQL database on Render
   - Update `DATABASE_URL` environment variable
   - The app will automatically use PostgreSQL if `DATABASE_URL` is set

2. **Option B: Keep SQLite (For Testing)**
   - Data will reset on each deployment
   - Not recommended for production

### To Use PostgreSQL on Render:

1. **Create PostgreSQL Database:**
   - Render Dashboard → "New +" → "PostgreSQL"
   - Choose a name and region
   - Click "Create Database"

2. **Get Connection String:**
   - Copy the "Internal Database URL" or "External Database URL"
   - Format: `postgresql://user:password@host:port/dbname`

3. **Set Environment Variable:**
   - In your Web Service → Environment
   - Add: `DATABASE_URL=postgresql://...` (paste the connection string)

4. **Update app.py** (Already done - it auto-detects PostgreSQL)

### Port Configuration

- Render automatically sets `PORT` environment variable
- Your app already uses: `port = int(os.getenv('PORT', 8080))`
- No changes needed!

---

## Troubleshooting

### Deployment Fails

1. **Check Build Logs:**
   - Look for import errors
   - Verify all dependencies in `requirements.txt`

2. **Check Runtime Logs:**
   - Look for startup errors
   - Verify environment variables are set

### App Crashes on Startup

1. **Missing Environment Variables:**
   - Ensure `GOOGLE_API_KEY` is set
   - Ensure `SECRET_KEY` is set

2. **Database Issues:**
   - Check database connection string
   - Verify database is running

### "View Problem" Links Don't Work

- This should be fixed in the current version
- If still broken, check logs for URL validation errors

### Company Names Not Showing

- Verify `GOOGLE_API_KEY` is valid
- Check AI response in logs

---

## Quick Deployment Checklist

- [ ] Code committed and pushed to GitHub
- [ ] Repository connected to Render
- [ ] Environment variables set:
  - [ ] `GOOGLE_API_KEY`
  - [ ] `SECRET_KEY`
  - [ ] `FLASK_ENV=production`
  - [ ] `DATABASE_URL` (if using PostgreSQL)
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `python app.py`
- [ ] Deployment successful
- [ ] Tested on live URL:
  - [ ] Login/Register works
  - [ ] Search works
  - [ ] Company names appear
  - [ ] URLs work correctly

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Render Support**: Available in dashboard
- **Check Logs**: Always check the "Logs" tab in Render dashboard for errors

Good luck with your deployment! 🚀

