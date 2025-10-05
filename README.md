# 🚀 Coding Questions Finder

A secure, beautiful web application that uses AI to find the top 5 matching coding questions from different platforms like LeetCode, GeeksforGeeks, HackerRank, InterviewBit, and CodeChef.

## ✨ Features

- 🔐 **Secure Authentication**: Student and Mentor login system with password hashing
- 🤖 **AI-Powered Search**: Uses Google's Gemini AI to understand your query and find relevant questions
- 🎨 **Modern UI**: Beautiful, responsive design with smooth animations
- 🔗 **Multiple Platforms**: Searches across 5 major coding platforms
- 📊 **Detailed Information**: Shows difficulty level, company, topic, and category for each question
- ⚡ **Fast Results**: Quick search and results display
- 👥 **Role-Based Access**: Separate dashboards for students and mentors
- 🛡️ **Session Management**: Secure session handling with automatic logout
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Database (SQLite - No Server Required!)

```bash
python setup_sqlite.py
```

This will:
- Create the SQLite database file
- Create all required tables
- Set up the database schema

### 3. Run the Application

PowerShell (recommended when using the included virtual environment):

```powershell
# Activate the project's virtual environment (Windows PowerShell)
& .\.venv\Scripts\Activate.ps1

# Start the app (default: debug mode with reloader)
python app.py
```

If you want to run the server without the Flask reloader (this makes scripting start/stop and smoke tests more reliable), set `debug=False` or run with the Flask CLI and disable the reloader:

```powershell
# Using the venv Python and Flask CLI (no reloader)
$env:FLASK_APP = 'app.py'; $env:FLASK_ENV = 'production'
& .\.venv\Scripts\python.exe -m flask run --host=0.0.0.0 --port=5000
```

The application will be available at: `http://localhost:5000`

### 4. Optional: Custom API Key

The application uses a built-in Google API key by default. If you want to use your own:

**Windows:**
```cmd
set GOOGLE_API_KEY=your_google_api_key_here
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

## How to Use

## Run tests

If you created and activated the virtual environment (see step 3), run:

```powershell
# Install test dependencies (if not already installed)
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt pytest requests

# Run the test suite
& .\.venv\Scripts\python.exe -m pytest -q
```

The test suite includes a quick smoke test (`test_app.py`) that will try to connect to a running server at `http://localhost:5000`. Make sure the server is running before executing the tests.


1. **Register/Login**: 
   - Go to `http://localhost:5000` (will redirect to login if not authenticated)
   - Create a new account as a Student or Mentor
   - Or login with existing credentials

2. **Search for Questions**:
   - Enter your coding question or topic in the search box
   - Click "Search" and wait for the AI to find relevant questions
   - Browse through the top 5 matching questions from different platforms
   - Click "View Problem" to open any question in a new tab

3. **User Management**:
   - View your user type (Student/Mentor) in the header
   - Logout when finished using the application

## 🏗️ Project Structure

```
project-folder/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies (includes waitress for production)
├── setup_sqlite.py          # Database setup script
├── test_app.py              # Application test suite
├── templates/
│   ├── index.html           # Main dashboard (redirects based on role)
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── mentor_dashboard.html # Mentor dashboard with question finder
│   └── student_dashboard.html # Student dashboard (published questions only)
├── static/
│   └── style.css            # Complete CSS styling
├── instance/
│   └── users.db             # SQLite database (auto-created)
└── README.md                # This file
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Bcrypt for password hashing
- **AI**: Google Gemini AI for intelligent question matching
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern design principles
- **Icons**: Font Awesome

## API Endpoints

### Authentication (Public)
- `GET /login` - Login page
- `POST /login` - User login (expects JSON with 'username' and 'password')
- `GET /register` - Registration page
- `POST /register` - User registration (expects JSON with 'username', 'email', 'password', 'user_type')
- `GET /logout` - User logout

### Protected Routes (Require Authentication)
- `GET /` - Main page (redirects to login if not authenticated)
- `POST /search` - Search for questions (expects JSON with 'query' field)

## Example Usage

1. Search for "binary tree traversal"
2. Search for "dynamic programming problems"
3. Search for "array manipulation"
4. Search for "graph algorithms"

The AI will understand your query and return the most relevant questions from different coding platforms with detailed information about each problem.

## 🚀 Deployment on Render

### Prerequisites
- A Render account (free tier available)
- A Google AI Studio API key

### Deployment Steps

1. **Prepare Repository**
   - Commit all files to your Git repository
   - Ensure `app.py` and `requirements.txt` are in the root directory

2. **Create Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: Choose a name for your service
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Set Environment Variables**
   ```
   GOOGLE_API_KEY=your_google_ai_studio_api_key_here
   SECRET_KEY=your_secret_key_for_flask_sessions
   FLASK_ENV=production
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Access your app at the provided URL

### Environment Variables
- `GOOGLE_API_KEY`: Get from [Google AI Studio](https://aistudio.google.com/)
- `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
- `PORT`: Automatically set by Render (defaults to 8080)

## 🎯 User Roles & Workflows

### Mentor Workflow
1. Register as "Mentor"
2. Login to mentor dashboard
3. Use AI-powered question finder
4. Save interesting question sets
5. Publish them for students to see

### Student Workflow
1. Register as "Student"
2. Login to student dashboard
3. View published questions from mentors
4. Practice with curated content

## 🔧 Troubleshooting

### Local Development
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Run database setup: `python setup_sqlite.py`
- Check if port 5000 is available

### Production Deployment
- Verify environment variables are set correctly
- Check Render logs for deployment issues
- Ensure Google API key has proper permissions
