from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
# GenAI imports can differ between package versions. Try multiple import
# locations and fall back to None if unavailable so the app can still run
# for local testing.
try:
    import google.generativeai as genai
    from google.generativeai import types
except Exception:
    try:
        from google import genai
        from google.genai import types
    except Exception:
        genai = None
        types = None
import os
from dotenv import load_dotenv
import json
import re
import urllib.parse
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)
# Load environment variables from a local .env file if present
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

# Set SECRET_KEY for Flask sessions (required for session management)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(32).hex())

# Set RUN_ID for session validation (invalidates old sessions on server restart)
app.config['RUN_ID'] = str(uuid4())

# Use DATABASE_URL from .env if available, otherwise default to users.db in project folder
database_url = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'users.db')}")

# Optional debug: see exactly where the DB will be
print("Using database at:", os.path.abspath(database_url.replace('sqlite:///', '')))

if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'mentor'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'user_type': self.user_type,
            'created_at': self.created_at.isoformat()
        }

class QuestionSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.String(500), nullable=False)
    summary = db.Column(db.String(200), nullable=False)
    questions_data = db.Column(db.Text, nullable=False)  # JSON string of questions
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime, nullable=True)
    
    @property
    def formatted_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''

    @property
    def formatted_published_at(self):
        return self.published_at.strftime('%Y-%m-%d %H:%M') if self.published_at else ''

    def to_dict(self):
        # Parse questions data and ensure URLs are valid
        questions_data = json.loads(self.questions_data)
        if isinstance(questions_data, list):
            for q in questions_data:
                if isinstance(q, dict) and 'url' in q:
                    q['url'] = self._normalize_url(q.get('url', ''), q.get('platform', ''), q.get('topic', ''))
        
        return {
            'id': self.id,
            'query': self.query,
            'summary': self.summary,
            'questions_data': questions_data,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
    
    @staticmethod
    def _normalize_url(url, platform, topic):
        """Normalize URL to ensure it's valid"""
        if not url:
            topic_enc = urllib.parse.quote_plus(topic or 'coding problem')
            platform_enc = urllib.parse.quote_plus(platform or 'LeetCode')
            return f"https://www.google.com/search?q={platform_enc}+{topic_enc}"
        
        url = str(url).strip()
        
        # If already valid, return as-is
        if url.startswith(('http://', 'https://')):
            return url
        
        # Fix protocol-relative URLs
        if url.startswith('//'):
            return 'https:' + url
        
        # Fix relative URLs
        if url.startswith('/'):
            platform_lower = (platform or '').lower()
            if 'leetcode' in platform_lower:
                return 'https://leetcode.com' + url
            elif 'geeksforgeeks' in platform_lower or 'gfg' in platform_lower:
                return 'https://www.geeksforgeeks.org' + url
            elif 'hackerrank' in platform_lower:
                return 'https://www.hackerrank.com' + url
            elif 'interviewbit' in platform_lower:
                return 'https://www.interviewbit.com' + url
            elif 'codechef' in platform_lower:
                return 'https://www.codechef.com' + url
            else:
                return 'https://' + url.lstrip('/')
        
        # Add https:// if missing
        return 'https://' + url

# Initialize the Gemini client (resilient):
# If the Google Generative AI client isn't available or has a different API,
# provide a safe fallback so the app can start during local tests.
_GENAI_AVAILABLE = True
try:
    # Configure the client with the API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        api_key = api_key.strip()

    if not api_key:
        # The API key is essential for the app to work.
        print("\nFATAL ERROR: The 'GOOGLE_API_KEY' environment variable is not set.")
        print("Please get an API key from Google AI Studio and set the environment variable.\n")
        _GENAI_AVAILABLE = False
        raise ValueError("API key not configured. Please set the GOOGLE_API_KEY environment variable.")

    genai.configure(api_key=api_key)

    # List of models to try in order of preference.
    # 'gemini-pro' is a stable name often available on v1beta.
    # We keep others as fallbacks.
    # Discover available models dynamically; fall back to a reasonable default list
    DEFAULT_MODEL_CANDIDATES = [
        'gemini-pro',
        'gemini-1.0-pro',
        'gemini-1.5-flash',
    ]
    try:
        list_models = genai.list_models()
        # Filter models that support generateContent
        discovered_models = []
        for m in list_models:
            try:
                # Some SDKs expose supported_generation_methods; guard defensively
                methods = getattr(m, 'supported_generation_methods', None)
                name = getattr(m, 'name', None) or getattr(m, 'model', None)
                if name and (methods is None or 'generateContent' in methods or 'generate_content' in methods):
                    # Normalize name by stripping versioned prefix if present
                    if name.startswith('models/'):
                        name = name.split('/', 1)[1]
                    discovered_models.append(name)
            except Exception:
                continue
        MODEL_CANDIDATES = discovered_models or DEFAULT_MODEL_CANDIDATES
    except Exception:
        MODEL_CANDIDATES = DEFAULT_MODEL_CANDIDATES

    def get_completion(prompt):
        """Tries a list of models to get a completion."""
        last_error_message = None
        for model_name in MODEL_CANDIDATES:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt, generation_config={
                    "temperature": 0,
                    "max_output_tokens": 800,
                })
                return response.text
            except Exception as e:
                # Check for a common authentication error
                if "API_KEY_INVALID" in str(e):
                    raise ValueError("Your Google API key is invalid. Please check your key and try again.") from e
                last_error_message = str(e)
                print(f"Warning: Model '{model_name}' failed with error: {e}. Trying next model.")
        raise RuntimeError(
            (
                "All candidate models failed. This can happen if your API key is invalid, has expired, or if you have network issues. "
                f"Last error: {last_error_message}"
            )
        )
except Exception as e:
    _GENAI_AVAILABLE = False
    print(f"Warning: Google Generative AI not available. {e}")
    def get_completion(prompt):
        return "[AI unavailable in this environment]"

@app.route('/health/genai')
def genai_health():
    """Return status about Generative AI configuration and availability."""
    raw_key = os.getenv("GOOGLE_API_KEY") or ""
    api_key_present = bool(raw_key)
    api_key_masked = None
    if raw_key:
        # Mask key to avoid leaking secrets; show prefix and length for debugging
        prefix = raw_key[:4]
        suffix = raw_key[-4:]
        api_key_masked = f"{prefix}...{suffix} (len={len(raw_key)})"
    status = {
        'success': True,
        'ai_available': _GENAI_AVAILABLE,
        'api_key_present': api_key_present,
        'api_key_masked': api_key_masked,
        'model_candidates': [] if not _GENAI_AVAILABLE else MODEL_CANDIDATES,
    }
    if not api_key_present:
        status['message'] = 'GOOGLE_API_KEY not found in environment.'
    elif not _GENAI_AVAILABLE:
        status['message'] = 'AI client failed to initialize. Check key validity and network.'
    else:
        status['message'] = 'AI configured and available.'
    return jsonify(status)

@app.route('/health/genai/test')
def genai_live_test():
    """Perform a live completion call to verify end-to-end function and return detailed diagnostics."""
    if not os.getenv("GOOGLE_API_KEY"):
        return jsonify({'success': False, 'error': 'GOOGLE_API_KEY not set in environment.'}), 400
    if not _GENAI_AVAILABLE:
        return jsonify({'success': False, 'error': 'AI client not available. Initialization failed.'}), 500
    try:
        text = get_completion("Reply with the single word: OK")
        return jsonify({'success': True, 'result': text, 'model_candidates': MODEL_CANDIDATES})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        if not user_id:
            # No user id in session -> ensure session is clean and redirect
            session.clear()
            return redirect(url_for('login'))

        # Verify the user exists and is active in the database. This prevents
        # stale or forged session cookies from granting access.
        try:
            user = db.session.get(User, user_id)
        except Exception:
            user = None

        if not user or not getattr(user, 'is_active', False):
            session.clear()
            return redirect(url_for('login'))

        # If the server restarted, previous sessions should be invalidated.
        session_run_id = session.get('run_id')
        if session_run_id != app.config.get('RUN_ID'):
            session.clear()
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            # stamp the session with current run id so old cookies are invalidated
            session['run_id'] = app.config.get('RUN_ID')
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type', 'student')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': 'Email already exists'
            }), 400
        
        # Create new user
        user = User(
            username=username,
            email=email,
            user_type=user_type
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Registration successful'
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Registration failed'
            }), 500
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    """Main entry point.

    Behavior:
    - If the user is not authenticated, show the login/signup page so visitors land there first.
    - If the user is authenticated, redirect them to their dashboard based on user_type.
    """
    # If not logged in, show the login page (so opening the app lands on login/signup)
    user_id = session.get('user_id')
    if not user_id:
        session.clear()
        return redirect(url_for('login'))

    # Verify user still exists and is active
    try:
        user = db.session.get(User, user_id)
    except Exception:
        user = None

    if not user or not getattr(user, 'is_active', False):
        session.clear()
        return redirect(url_for('login'))

    # If logged in, direct to appropriate dashboard
    # Invalidate sessions generated by previous server runs
    if session.get('run_id') != app.config.get('RUN_ID'):
        session.clear()
        return redirect(url_for('login'))

    user_type = session.get('user_type')
    if user_type == 'mentor':
        return redirect(url_for('mentor_dashboard'))
    return redirect(url_for('student_dashboard'))

@app.route('/mentor')
@login_required
def mentor_dashboard():
    """Mentor dashboard with question finder and management"""
    if session.get('user_type') != 'mentor':
        return redirect(url_for('student_dashboard'))
    
    try:
        # Get all of the mentor's saved questions (both drafts and published)
        mentor_id = session.get('user_id')
        saved_questions = db.session.query(QuestionSet).filter_by(mentor_id=mentor_id).order_by(QuestionSet.created_at.desc()).all()

        return render_template('mentor_dashboard.html', 
                             user=session.get('username'), 
                             user_type=session.get('user_type'),
                             saved_questions=saved_questions)
    except Exception as e:
        print(f"Error in mentor dashboard: {str(e)}")
        # Return empty list if there's an error
        return render_template('mentor_dashboard.html', 
                             user=session.get('username'), 
                             user_type=session.get('user_type'),
                             saved_questions=[])

@app.route('/student')
@login_required
def student_dashboard():
    """Student dashboard with published questions"""
    if session.get('user_type') != 'student':
        return redirect(url_for('mentor_dashboard'))
    
    try:
        # Get all published questions
        published_questions = db.session.query(QuestionSet).filter_by(is_published=True).order_by(QuestionSet.created_at.desc()).all()

        return render_template('student_dashboard.html', 
                             user=session.get('username'), 
                             user_type=session.get('user_type'),
                             published_questions=published_questions)
    except Exception as e:
        print(f"Error in student dashboard: {str(e)}")
        # Return empty list if there's an error
        return render_template('student_dashboard.html', 
                             user=session.get('username'), 
                             user_type=session.get('user_type'),
                             published_questions=[])

@app.route('/search', methods=['POST'])
@login_required
def search_questions():
    """Handle the search request and return related questions"""
    try:
        # If AI is not available (e.g., missing/invalid API key), return a friendly error.
        if not _GENAI_AVAILABLE:
            return jsonify({'success': False, 'error': 'AI is not configured. Set GOOGLE_API_KEY and restart the server.'}), 503

        query = request.json.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Step 1: Extract company name and summarize the query
        extract_prompt = f"""
        Analyze the following query and extract:
        1. The company name mentioned (if any)
        2. A brief summary of the coding problem/topic
        
        Query: {query}
        
        Respond in JSON format with two keys: "company" and "summary"
        If no company is mentioned, set "company" to "General"
        Example: {{"company": "Capgemini", "summary": "Palindrome check using dynamic programming"}}
        """
        
        extract_response = get_completion(extract_prompt)
        if isinstance(extract_response, str) and '[AI unavailable' in extract_response:
            return jsonify({'success': False, 'error': 'AI is unavailable in this environment. Configure GOOGLE_API_KEY and try again.'}), 503
        
        # Parse extracted information
        extracted_company = "General"
        summary_text = query
        
        try:
            # Try to extract JSON from response
            extract_clean = extract_response.strip()
            if extract_clean.startswith('```'):
                first_nl = extract_clean.find('\n')
                if first_nl != -1:
                    extract_clean = extract_clean[first_nl:].strip()
                if extract_clean.endswith('```'):
                    extract_clean = extract_clean[:-3].strip()
            
            json_start = extract_clean.find('{')
            json_end = extract_clean.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                extract_data = json.loads(extract_clean[json_start:json_end])
                extracted_company = extract_data.get('company', 'General')
                summary_text = extract_data.get('summary', query)
        except:
            # If extraction fails, try to find company name in query using simple pattern
            query_lower = query.lower()
            common_companies = ['capgemini', 'google', 'microsoft', 'amazon', 'facebook', 'meta', 'apple', 
                             'netflix', 'uber', 'airbnb', 'oracle', 'ibm', 'adobe', 'salesforce', 
                             'twitter', 'linkedin', 'paypal', 'visa', 'mastercard', 'goldman sachs',
                             'morgan stanley', 'jpmorgan', 'accenture', 'tcs', 'infosys', 'wipro',
                             'cognizant', 'hcl', 'tech mahindra', 'deloitte', 'pwc', 'ey', 'kpmg']
            for company in common_companies:
                if company in query_lower:
                    extracted_company = company.title()
                    break
        
        # Step 2: Generate related questions with extracted company
        final_prompt = f"""
        Generate a list of exactly 5 coding problems related to: {summary_text}
        
        IMPORTANT: The user mentioned the company "{extracted_company}" in their query. Use this company name for the "company" field in ALL 5 questions.
        
        For each problem, provide a JSON object with the following keys:
        - "url": A COMPLETE, VALID absolute URL starting with https:// to the actual problem page. Examples:
          * LeetCode: "https://leetcode.com/problems/palindrome-partitioning/"
          * GeeksforGeeks: "https://www.geeksforgeeks.org/palindrome-partitioning-dp-17/"
          * HackerRank: "https://www.hackerrank.com/challenges/palindrome-index/problem"
          * InterviewBit: "https://www.interviewbit.com/problems/palindrome-partitioning/"
          * CodeChef: "https://www.codechef.com/problems/PALIN"
          CRITICAL: The URL must be a complete, working URL that starts with https://
        - "platform": The coding platform name (e.g., "LeetCode", "GeeksforGeeks", "HackerRank", "InterviewBit", "CodeChef")
        - "topic": The topic name of the problem (e.g., "Palindrome Check", "Palindrome Partitioning")
        - "difficulty_level": The difficulty (e.g., "Easy", "Medium", "Hard")
        - "company": MUST be "{extracted_company}" (use this exact company name from the user's query)
        - "category": The category/type of problem (e.g., "String", "Dynamic Programming", "Array")
        
        Return ONLY a valid JSON array with 5 objects. Do not include any markdown formatting, code blocks, or extra text.
        CRITICAL: 
        1. All URLs must be complete absolute URLs starting with https://
        2. ALL 5 questions must have "company": "{extracted_company}"
        
        Example format:
        [
          {{"url": "https://leetcode.com/problems/palindrome-partitioning/", "platform": "LeetCode", "topic": "Palindrome Partitioning", "difficulty_level": "Medium", "company": "{extracted_company}", "category": "Dynamic Programming"}},
          {{"url": "https://www.geeksforgeeks.org/palindrome-partitioning-dp-17/", "platform": "GeeksforGeeks", "topic": "Palindrome Partitioning", "difficulty_level": "Medium", "company": "{extracted_company}", "category": "Dynamic Programming"}},
          ... (3 more questions, ALL with company: "{extracted_company}")
        ]
        """
        
        final_response = get_completion(final_prompt)
        if isinstance(final_response, str) and '[AI unavailable' in final_response:
            return jsonify({'success': False, 'error': 'AI is unavailable in this environment. Configure GOOGLE_API_KEY and try again.'}), 503
        
        # Clean the response
        # Find the start and end of the JSON block to handle responses
        # that might include extra text like "```json\n[...]\n```"
        clean_response = final_response.strip()
        
        # Remove markdown code blocks if present
        if clean_response.startswith('```'):
            # Find the first newline after ```
            first_newline = clean_response.find('\n')
            if first_newline != -1:
                clean_response = clean_response[first_newline:].strip()
            # Remove trailing ```
            if clean_response.endswith('```'):
                clean_response = clean_response[:-3].strip()
        
        # Find JSON array boundaries
        json_start = clean_response.find('[')
        json_end = clean_response.rfind(']') + 1
        
        if json_start == -1 or json_end == 0:
            # Try to find any JSON structure
            json_start = clean_response.find('{')
            if json_start != -1:
                # Might be a single object, wrap in array
                json_end = clean_response.rfind('}') + 1
                if json_end > json_start:
                    clean_response = '[' + clean_response[json_start:json_end] + ']'
                    json_start = 0
                    json_end = len(clean_response)
            
            if json_start == -1 or json_end == 0:
                raise json.JSONDecodeError("No JSON array found in AI response", final_response, 0)
        else:
            clean_response = clean_response[json_start:json_end]
        
        # Parse JSON response
        try:
            questions_list = json.loads(clean_response)
        except json.JSONDecodeError as e:
            # Try to fix common issues
            # Remove any trailing commas before closing brackets
            clean_response = re.sub(r',\s*}', '}', clean_response)
            clean_response = re.sub(r',\s*]', ']', clean_response)
            questions_list = json.loads(clean_response)
        
        # Ensure it's a list
        if not isinstance(questions_list, list):
            questions_list = [questions_list]
        
        # Validate and ensure we have exactly 5 items (or at least some items)
        if len(questions_list) == 0:
            raise ValueError("AI returned an empty list of questions")
        
        # Ensure all required fields are present and validate URLs
        required_fields = ['url', 'platform', 'topic', 'difficulty_level', 'company', 'category']
        for i, q in enumerate(questions_list):
            if not isinstance(q, dict):
                raise ValueError(f"Question {i+1} is not a valid object")
            
            # Ensure company field exists - use extracted company or default to "General"
            company_name = str(q.get('company', '')).strip()
            if not company_name or company_name.lower() == 'general':
                # Use extracted company from query, or keep existing if it's valid
                q['company'] = extracted_company
            else:
                # Ensure company name is properly capitalized
                q['company'] = company_name.title()
            
            # Ensure all other required fields exist
            missing = [f for f in required_fields if f not in q or (f != 'company' and not q[f])]
            if missing:
                print(f"Warning: Question {i+1} missing fields: {missing}")
            
            # Use the same normalization function
            q['url'] = QuestionSet._normalize_url(
                q.get('url', ''),
                q.get('platform', ''),
                q.get('topic', '')
            )
        
        # Save to file (optional)
        with open("related_questions.json", "w") as f:
            json.dump(questions_list, f, indent=2)
        
        return jsonify({
            'success': True,
            'summary': summary_text,
            'questions': questions_list
        })
        
    except json.JSONDecodeError as e:
        return jsonify({'success': False, 'error': f'Failed to parse AI response: {str(e)}.'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': f'An error occurred: {str(e)}'}), 500

@app.route('/save_search', methods=['POST'])
@login_required
def save_search():
    """Save search results for mentor"""
    if session.get('user_type') != 'mentor':
        return jsonify({'error': 'Only mentors can save searches'}), 403
    
    try:
        data = request.get_json()
        query = data.get('query')
        summary_text = data.get('summary')
        questions_data = data.get('questions')

        # Defensive handling: if query is missing, derive one from the summary.
        if not query:
            if summary_text:
                query = (summary_text[:200])
            elif isinstance(questions_data, list) and questions_data:
                query = questions_data[0].get('topic') or "Untitled Question Set"

        # Ensure questions_data is a list (it might be sent as a string)
        if isinstance(questions_data, str):
            try:
                questions_data = json.loads(questions_data)
            except Exception:
                questions_data = None

        if not all([query, summary_text, questions_data]):
            return jsonify({'success': False, 'message': 'Missing required data: query, summary, and questions are needed.'}), 400
        
        # Validate and normalize URLs before saving
        if isinstance(questions_data, list):
            for q in questions_data:
                if isinstance(q, dict) and 'url' in q:
                    q['url'] = QuestionSet._normalize_url(
                        q.get('url', ''),
                        q.get('platform', ''),
                        q.get('topic', '')
                    )
                # Ensure company field exists
                if isinstance(q, dict) and 'company' not in q:
                    q['company'] = 'General'
        
        # Save to database
        published_question = QuestionSet(
            mentor_id=session.get('user_id'),
            query=query,
            summary=summary_text,
            questions_data=json.dumps(questions_data),
            is_published=False
        )
        
        db.session.add(published_question)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Search results saved successfully',
            'question_id': published_question.id
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in save_search: {str(e)}")
        return jsonify({'success': False, 'message': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/publish_question', methods=['POST'])
@login_required
def publish_question():
    """Publish/unpublish a question"""
    if session.get('user_type') != 'mentor':
        return jsonify({'error': 'Only mentors can publish questions'}), 403
    
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        action = data.get('action')  # 'publish' or 'unpublish'
        
        question = db.session.query(QuestionSet).filter_by(
            id=question_id, 
            mentor_id=session.get('user_id')
        ).first()
        
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        if action == 'publish':
            question.is_published = True
            question.published_at = datetime.utcnow()
        elif action == 'unpublish':
            question.is_published = False
            question.published_at = None
        else:
            return jsonify({'error': 'Invalid action'}), 400
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Question {action}ed successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to {action} question: {str(e)}'}), 500

@app.route('/delete_question', methods=['POST'])
@login_required
def delete_question():
    """Delete a saved question"""
    if session.get('user_type') != 'mentor':
        return jsonify({'error': 'Only mentors can delete questions'}), 403
    
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        
        question = db.session.query(QuestionSet).filter_by(
            id=question_id, 
            mentor_id=session.get('user_id')
        ).first()
        
        if not question:
            return jsonify({'error': 'Question not found'}), 404
        
        db.session.delete(question)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Question deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete question: {str(e)}'}), 500

@app.route('/get_question_details/<int:question_id>', methods=['GET'])
@login_required
def get_question_details(question_id):
    """Get details for a single question set to display in a modal."""
    if session.get('user_type') != 'mentor':
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        question = db.session.query(QuestionSet).filter_by(
            id=question_id, 
            mentor_id=session.get('user_id')
        ).first()

        if not question:
            return jsonify({'error': 'Question not found'}), 404

        return jsonify({'success': True, 'question': question.to_dict()})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/get_published_question_details/<int:question_id>', methods=['GET'])
@login_required
def get_published_question_details(question_id):
    """Get details for a single PUBLISHED question set for students."""
    try:
        question = db.session.query(QuestionSet).filter_by(
            id=question_id,
            is_published=True
        ).first()

        if not question:
            return jsonify({'error': 'Published question not found or not available.'}), 404

        return jsonify({'success': True, 'question': question.to_dict()})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/captcha')
def captcha():
    """Captcha page"""
    return render_template('captcha.html')


@app.route('/init-db')
def init_db():
    """Initialize database tables"""
    try:
        with app.app_context():
            db.create_all()
        return jsonify({'success': True, 'message': 'Database initialized successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error initializing database: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    # For production deployment on Render
    from waitress import serve
    port = int(os.getenv('PORT', 8080))
    serve(app, host='0.0.0.0', port=port)
