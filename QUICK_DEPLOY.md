# Quick Deploy to Render - Step by Step

## If You Already Have a Render Service (Replace Existing)

### 1. Initialize Git (if not already done)
```powershell
git init
git add .
git commit -m "Final version ready for deployment"
```

### 2. Push to GitHub
```powershell
# If you don't have a remote yet
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main

# If you already have a remote
git push origin main
```

### 3. Update Render Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Find your existing service
3. Go to "Settings" → "Build & Deploy"
4. Click "Manual Deploy" → "Deploy latest commit"
5. OR just wait - it will auto-deploy when you push

### 4. Update Environment Variables (if needed)
1. In Render service → "Environment" tab
2. Make sure these are set:
   - `GOOGLE_API_KEY` = your API key
   - `SECRET_KEY` = generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
   - `FLASK_ENV` = `production`

### 5. Done! Your site will update automatically

---

## If Starting Fresh (New Deployment)

### Step 1: Initialize Git Repository
```powershell
git init
git add .
git commit -m "Initial commit - Coding Questions Finder"
```

### Step 2: Create GitHub Repository
1. Go to [GitHub](https://github.com)
2. Click "New repository"
3. Name it (e.g., `coding-questions-finder`)
4. Don't initialize with README
5. Click "Create repository"

### Step 3: Push to GitHub
```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy on Render

1. **Go to Render Dashboard:**
   - https://dashboard.render.com
   - Sign in or create account

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select your repository

3. **Configure Service:**
   - **Name**: `coding-questions-finder` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Set Environment Variables:**
   Click "Advanced" → Add these:
   ```
   GOOGLE_API_KEY = your_google_api_key
   SECRET_KEY = your_secret_key (generate with command below)
   FLASK_ENV = production
   ```

   **Generate SECRET_KEY:**
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. **Create Service:**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment
   - Your app will be live!

---

## Important: Database Setup

### Option 1: Use SQLite (Simple, but data resets on deploy)
- No setup needed
- Data will be lost on each deployment
- Good for testing

### Option 2: Use PostgreSQL (Recommended for production)

1. **Create PostgreSQL Database:**
   - Render Dashboard → "New +" → "PostgreSQL"
   - Choose name and region
   - Click "Create Database"

2. **Get Connection String:**
   - Copy "Internal Database URL"
   - Format: `postgresql://user:pass@host:port/dbname`

3. **Add to Environment Variables:**
   - In your Web Service → Environment
   - Add: `DATABASE_URL` = (paste connection string)

4. **Your app will automatically use PostgreSQL!**

---

## Quick Commands Reference

```powershell
# Initialize Git
git init
git add .
git commit -m "Ready for deployment"

# Push to GitHub
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# Generate Secret Key
python -c "import secrets; print(secrets.token_hex(32))"

# Check Git Status
git status

# View Logs (after deployment)
# Go to Render Dashboard → Your Service → Logs tab
```

---

## After Deployment

1. **Test Your Live Site:**
   - Register a new account
   - Login
   - Search for questions
   - Verify company names appear
   - Check "View Problem" links work

2. **Monitor Logs:**
   - Render Dashboard → Your Service → Logs
   - Check for any errors

3. **Update Anytime:**
   - Just push to GitHub
   - Render auto-deploys (or manually trigger)

---

## Troubleshooting

**Build Fails:**
- Check `requirements.txt` has all dependencies
- Check Python version (Render uses 3.11 by default)

**App Crashes:**
- Check environment variables are set
- Check logs for error messages
- Verify `GOOGLE_API_KEY` is valid

**Database Issues:**
- If using SQLite, data resets on deploy (normal)
- Switch to PostgreSQL for persistent data

**Need Help?**
- Check Render logs
- Render support is available in dashboard
- See `DEPLOY_TO_RENDER.md` for detailed guide

---

## Your App is Now Live! 🎉

Your URL will be: `https://your-service-name.onrender.com`

Good luck! 🚀

