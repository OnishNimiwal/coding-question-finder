# Quick Start Guide - Run Locally

## Fastest Way to Run (Automated)

1. **Open PowerShell** in the project folder

2. **Run the setup script**:
   ```powershell
   .\run_local.ps1
   ```

   This script will:
   - Check Python installation
   - Create/activate virtual environment
   - Install all dependencies
   - Set up the database
   - Ask for your Google API key (optional)
   - Start the application

3. **Open your browser** to: http://localhost:8080

## Manual Setup (Step by Step)

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Setup Database
```powershell
python setup_sqlite.py
```

### 3. Set API Key (Optional - for AI features)
```powershell
$env:GOOGLE_API_KEY = "your_google_api_key_here"
```

Or create a `.env` file:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the Application
```powershell
python app.py
```

### 5. Open Browser
Go to: **http://localhost:8080**

## First Time Using the App

1. **Register**: Go to http://localhost:8080/register
   - Create an account as "Mentor" or "Student"
   - Remember your username and password

2. **Login**: Go to http://localhost:8080/login
   - Enter your credentials

3. **Use the App**:
   - **Mentors**: Can search for coding questions and publish them
   - **Students**: Can view published questions

## Need Help?

- See `RUN_LOCALLY.md` for detailed instructions
- See `TEST_RESULTS.md` for troubleshooting
- See `README.md` for full documentation

## Common Commands

```powershell
# Activate virtual environment (if using one)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_comprehensive.py

# Stop the server
# Press Ctrl+C in the terminal
```

