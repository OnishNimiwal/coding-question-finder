# Update API Key on Render - Quick Guide

## Step 1: Update API Key in Render Dashboard

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Find your service**: Look for "coding-easy" or your service name
3. **Click on your service** to open it
4. **Go to "Environment" tab** (left sidebar)
5. **Find `GOOGLE_API_KEY`** in the environment variables list
6. **Click on it** to edit
7. **Replace with new API key**: `AIzaSyAoytEbV3r_wtpG4yFjd9Y8vf0spu53S3w`
8. **Click "Save Changes"**

## Step 2: Redeploy Service

After updating the API key:

1. **Go to "Manual Deploy"** tab (or "Events" tab)
2. **Click "Manual Deploy"** → **"Deploy latest commit"**
   - OR wait for auto-deploy if enabled
3. **Wait 2-5 minutes** for deployment to complete
4. **Check "Logs" tab** to verify deployment is successful

## Step 3: Test Your Live Site

1. Go to: https://coding-easy.onrender.com
2. Test the search functionality
3. Verify it's working correctly

---

## Alternative: Update via Render Dashboard UI

### Quick Steps:
1. Render Dashboard → Your Service
2. **Settings** → **Environment**
3. Find `GOOGLE_API_KEY`
4. Click **Edit** (pencil icon)
5. Paste new key: `AIzaSyAoytEbV3r_wtpG4yFjd9Y8vf0spu53S3w`
6. **Save**
7. **Manual Deploy** → **"Deploy latest commit"**

---

## Verify API Key is Updated

1. Check **Environment** tab - should show new key
2. Check **Logs** tab after deployment - should not show API key errors
3. Test search on live site - should work

---

## Troubleshooting

### API Key Not Saving
- Make sure you click "Save Changes" after editing
- Check for typos in the key

### Still Getting Errors After Update
- Wait for deployment to complete (check Logs)
- Clear browser cache and try again
- Check Logs tab for specific error messages

### Deployment Fails
- Check Logs tab for error details
- Verify API key format is correct
- Ensure no extra spaces in the key

---

## Your New API Key

```
AIzaSyAoytEbV3r_wtpG4yFjd9Y8vf0spu53S3w
```

Make sure to copy it exactly as shown above (no extra spaces).

---

## After Update

✅ API key updated  
✅ Service redeployed  
✅ Test search functionality  
✅ Verify company extraction works  
✅ Check URLs are working  

Your app should be working now! 🚀

