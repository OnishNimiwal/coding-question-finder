# Push Your Code to GitHub - Quick Steps

Since you already have the remote configured, follow these steps:

## Step 1: Check Current Status
```powershell
git status
```

## Step 2: Add All Files
```powershell
git add .
```

## Step 3: Commit Changes
```powershell
git commit -m "Final version: Fixed URLs, company extraction, and all features working"
```

## Step 4: Push to GitHub
```powershell
git push origin main
```

If you get an error about branch name, try:
```powershell
git push origin master
```

Or check your branch name:
```powershell
git branch
```

## Step 5: Update Render Service

After pushing to GitHub:

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Find your service** (coding-question-finder or similar)
3. **Click "Manual Deploy"** → **"Deploy latest commit"**
   - OR it will auto-deploy if auto-deploy is enabled

## Step 6: Verify Environment Variables

Make sure these are set in Render:
- `GOOGLE_API_KEY` = your Google API key
- `SECRET_KEY` = generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
- `FLASK_ENV` = `production`

## Step 7: Test Your Live Site

Once deployed (2-5 minutes), test:
- ✅ Login/Register
- ✅ Search functionality
- ✅ Company names appear
- ✅ "View Problem" links work

---

## If You Get Errors

### "Branch not found" or "Branch name mismatch"
```powershell
# Check current branch
git branch

# If you're on 'master', push to master
git push origin master

# Or rename to main
git branch -M main
git push origin main
```

### "Remote already exists" (you already saw this)
- That's fine! Just skip adding the remote and push directly

### "Nothing to commit"
- All changes are already committed
- Just push: `git push origin main`

---

## Quick Command Summary

```powershell
git add .
git commit -m "Final deployment version"
git push origin main
```

Then go to Render and deploy! 🚀

