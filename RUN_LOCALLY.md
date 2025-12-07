# How to Run the Application Locally on Windows

## Prerequisites

1. **Python 3.8 or higher** - Check if installed:
   ```powershell
   python --version
   ```
   If not installed, download from [python.org](https://www.python.org/downloads/)

2. **Google API Key** (Optional but required for AI features)
   - Get one from [Google AI Studio](https://aistudio.google.com/)
   - You'll need this for the search functionality

## Step-by-Step Setup

### Step 1: Open PowerShell in the Project Folder

1. Navigate to your project folder:
   ```powershell
   cd "C:\Users\NIKKA\OneDrive\Desktop\Sequence needed (2)\Sequence needed"
   ```

### Step 2: Create a Virtual Environment (Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
# Make sure virtual environment is activated (you should see (venv) in prompt)
pip install -r requirements.txt
```

### Step 4: Set Up the Database

```powershell
python setup_sqlite.py
```

This will create the database tables automatically.

### Step 5: Set Environment Variables

#### Option A: Set for Current Session (Temporary)

```powershell
# Set Google API Key (replace with your actual key)
$env:GOOGLE_API_KEY = "your_google_api_key_here"

# Optional: Set Flask to development mode
$env:FLASK_ENV = "development"
```

#### Option B: Create .env File (Permanent - Recommended)

Create a file named `.env` in the project root:

```powershell
# Create .env file
@"
GOOGLE_API_KEY=your_google_api_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_key_here_optional
"@ | Out-File -FilePath .env -Encoding utf8
```

Replace `your_google_api_key_here` with your actual Google API key.

**Note**: The `.env` file is already in `.gitignore` (if you have one), so it won't be committed to version control.

### Step 6: Run the Application

```powershell
python app.py
```

You should see output like:
```
Using database at: C:\Users\NIKKA\OneDrive\Desktop\Sequence needed (2)\Sequence needed\users.db
Database tables created successfully!
```

The application will start on **http://localhost:8080** (or port 5000 if PORT is not set).

### Step 7: Open in Browser

Open your web browser and go to:
- **http://localhost:8080** (or the port shown in the terminal)

## Quick Start Script

I've also created a `run_local.ps1` script that automates most of this. See below.

## Testing the Application

1. **Register a User**:
   - Go to http://localhost:8080/register
   - Create an account as "Mentor" or "Student"
   - Click "Register"

2. **Login**:
   - Go to http://localhost:8080/login
   - Enter your credentials
   - Click "Login"

3. **Test Search** (Mentor only):
   - On the mentor dashboard, enter a query like "binary tree traversal"
   - Click "Search"
   - Wait for results (requires valid GOOGLE_API_KEY)

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Make sure virtual environment is activated and dependencies are installed:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "AI is not configured"
**Solution**: Set the GOOGLE_API_KEY environment variable:
```powershell
$env:GOOGLE_API_KEY = "your_key_here"
```

### Issue: Port already in use
**Solution**: The app uses port 8080 by default. To use a different port:
```powershell
$env:PORT = "5000"
python app.py
```

### Issue: Database errors
**Solution**: Delete the database files and recreate:
```powershell
Remove-Item users.db -ErrorAction SilentlyContinue
Remove-Item instance\*.db -ErrorAction SilentlyContinue
python setup_sqlite.py
```

### Issue: Execution Policy Error
**Solution**: Run this command:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Stopping the Application

Press `Ctrl+C` in the terminal where the app is running.

## Next Steps

- Test the application using `test_comprehensive.py`
- Check `TEST_RESULTS.md` for known issues and fixes
- Read `README.md` for more detailed documentation

