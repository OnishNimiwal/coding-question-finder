# Push to New GitHub Repository - Step by Step

## Step 1: Create New Repository on GitHub

1. Go to https://github.com
2. Click the **"+"** icon → **"New repository"**
3. Fill in:
   - **Repository name**: `coding-questions-finder` (or your choice)
   - **Description**: "AI-powered coding questions finder with company extraction"
   - **Visibility**: Public or Private (your choice)
   - **DO NOT** check "Initialize with README" (we already have files)
4. Click **"Create repository"**

## Step 2: Remove Old Remote (if exists)

```powershell
# Check current remote
git remote -v

# Remove old remote
git remote remove origin
```

## Step 3: Add New Remote

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

Example:
```powershell
git remote add origin https://github.com/OnishNimiwal/coding-questions-finder.git
```

## Step 4: Add All Files

```powershell
git add .
```

## Step 5: Commit

```powershell
git commit -m "Initial commit: Coding Questions Finder with all features"
```

If you get "nothing to commit", your files are already committed. Skip to Step 6.

## Step 6: Push to New Repository

```powershell
# Push to main branch
git branch -M main
git push -u origin main
```

If you get an error about branch name, try:
```powershell
git push -u origin master
```

## Step 7: Verify on GitHub

1. Go to your new repository on GitHub
2. Verify all files are there
3. Check that `.gitignore` is working (no `.db` files, no `__pycache__`)

## Step 8: Connect to Render

### If Creating New Render Service:

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your **new repository**
5. Configure:
   - **Name**: `coding-questions-finder`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Add Environment Variables:
   - `GOOGLE_API_KEY` = your API key
   - `SECRET_KEY` = generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
   - `FLASK_ENV` = `production`
7. Click **"Create Web Service"**

### If Updating Existing Render Service:

1. Go to Render Dashboard
2. Find your service
3. Go to **"Settings"** → **"Service Details"**
4. Click **"Change Repository"**
5. Select your **new repository**
6. Click **"Save Changes"**
7. Go to **"Manual Deploy"** → **"Deploy latest commit"**

---

## Complete Command Sequence

Copy and paste these commands one by one (replace with your details):

```powershell
# 1. Remove old remote (if exists)
git remote remove origin

# 2. Add new remote (REPLACE WITH YOUR REPO URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# 3. Check status
git status

# 4. Add all files
git add .

# 5. Commit
git commit -m "Initial commit: Complete Coding Questions Finder application"

# 6. Push to new repository
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### "Remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### "Repository not found"
- Make sure you created the repository on GitHub first
- Check the repository name and username are correct
- Make sure the repository is not private if you're having auth issues

### "Authentication failed"
- GitHub may require a Personal Access Token instead of password
- Go to GitHub → Settings → Developer settings → Personal access tokens
- Generate a new token with `repo` permissions
- Use the token as password when pushing

### "Nothing to commit"
- Your files are already committed
- Just push: `git push -u origin main`

---

## After Pushing

✅ Your code is now on GitHub  
✅ Connect to Render (new service or update existing)  
✅ Set environment variables  
✅ Deploy!  

Your app will be live in 5 minutes! 🚀

