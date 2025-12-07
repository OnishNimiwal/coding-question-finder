# Setup and Push to New GitHub Repository

## Step 1: Create New Repository on GitHub

1. Go to https://github.com and sign in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in:
   - **Repository name**: `coding-questions-finder` (or your choice)
   - **Description**: "AI-powered coding questions finder"
   - **Visibility**: Public or Private
   - **DO NOT** check "Initialize with README" ❌
   - **DO NOT** add .gitignore ❌
   - **DO NOT** add license ❌
4. Click **"Create repository"**
5. **Copy the repository URL** (you'll need it in Step 3)

## Step 2: Initialize Git in Your Project

Run these commands in your project folder:

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: Complete Coding Questions Finder application"
```

## Step 3: Add Your New Repository as Remote

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub details:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

**Example:**
```powershell
git remote add origin https://github.com/OnishNimiwal/coding-questions-finder.git
```

## Step 4: Push to GitHub

```powershell
# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

If you get authentication error, you may need to use a Personal Access Token:
- Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token with `repo` permissions
- Use token as password when pushing

## Step 5: Verify on GitHub

1. Go to your repository on GitHub
2. Check that all files are there
3. Verify `.gitignore` is working (no `.db` files visible)

## Step 6: Deploy to Render

### Option A: Create New Render Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub (if not already connected)
4. Select your **new repository**
5. Configure:
   - **Name**: `coding-questions-finder`
   - **Region**: Choose closest
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Click **"Advanced"** and add Environment Variables:
   ```
   GOOGLE_API_KEY = your_google_api_key
   SECRET_KEY = your_secret_key
   FLASK_ENV = production
   ```
7. Click **"Create Web Service"**
8. Wait 2-5 minutes for deployment

### Option B: Update Existing Render Service

1. Go to Render Dashboard
2. Find your existing service
3. **Settings** → **Service Details**
4. Click **"Change Repository"**
5. Select your **new repository**
6. **Save Changes**
7. **Manual Deploy** → **"Deploy latest commit"**

---

## Complete Command Sequence

Copy and paste these commands (replace repository URL):

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Complete Coding Questions Finder application"

# Add remote (REPLACE WITH YOUR REPO URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Generate Secret Key for Render

Before deploying, generate a secret key:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as `SECRET_KEY` in Render environment variables.

---

## Quick Checklist

- [ ] Created new repository on GitHub
- [ ] Initialized git: `git init`
- [ ] Added files: `git add .`
- [ ] Committed: `git commit -m "Initial commit"`
- [ ] Added remote: `git remote add origin https://github.com/...`
- [ ] Pushed: `git push -u origin main`
- [ ] Verified files on GitHub
- [ ] Created/Updated Render service
- [ ] Set environment variables in Render
- [ ] Deployed successfully
- [ ] Tested live site

---

## Troubleshooting

### "Repository not found"
- Make sure you created the repository on GitHub first
- Check the URL is correct
- Verify you have access to the repository

### "Authentication failed"
- GitHub requires Personal Access Token for HTTPS
- Generate token: GitHub → Settings → Developer settings → Personal access tokens
- Use token as password when pushing

### "Remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### "Nothing to commit"
- Files might already be committed
- Check: `git status`
- If clean, just push: `git push -u origin main`

---

## You're All Set! 🎉

After pushing, your code will be on GitHub and ready to deploy to Render!

Good luck! 🚀

