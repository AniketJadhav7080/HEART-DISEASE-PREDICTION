import streamlit as st
import sqlite3
import hashlib
import re
import html
from datetime import datetime, timedelta

# Clean CSS for professional design
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Login container styling */
    .login-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem auto;
        max-width: 500px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    
    /* Login header styling */
    .login-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    /* Form styling - clean and modern */
    .stForm {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }
    
    /* Input field styling - clean and modern */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        color: #495057;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        outline: none;
    }
    
    /* Button styling - modern and clean */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        font-size: 1rem;
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Success message styling */
    .success-msg {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
    }
    
    /* Error message styling */
    .error-msg {
        background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
    }
    
    /* Warning message styling */
    .warning-msg {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
    }
    
    /* Info message styling */
    .info-msg {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        color: white;
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.3);
    }
    
    /* User dashboard styling - clean and modern */
    .user-dashboard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* Custom animations */
    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(30px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Remove Streamlit default styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Clean up any remaining dark elements */
    .css-1v0mbdj {
        background: transparent !important;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .login-header {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .login-container {
            padding: 2rem;
            margin: 1rem;
        }
        
        .stForm {
            padding: 1.5rem;
            margin: 1rem 0;
        }
    }
    
    /* Enhanced text visibility - ensure all text is clearly visible */
    .stMarkdown {
        color: #2c3e50 !important;
    }
    
    .stText {
        color: #2c3e50 !important;
    }
    
    /* Ensure all text elements are visible */
    p, h1, h2, h3, h4, h5, h6, span, div {
        color: #2c3e50 !important;
    }
    
    /* Remove any dark backgrounds */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
    }
    
    /* Link styling */
    .stLink {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .stLink:hover {
        color: #5a6fd8;
        text-decoration: underline;
    }
    
    /* Divider styling */
    .divider {
        text-align: center;
        margin: 1.5rem 0;
        position: relative;
    }
    
    .divider::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e9ecef, transparent);
    }
    
    .divider span {
        background: rgba(255, 255, 255, 0.95);
        padding: 0 1rem;
        color: #6c757d;
        font-size: 0.9rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

def init_database():
    """Initialize the database with users table"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Create admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@ecg.com', admin_password, 'Administrator', 'admin'))
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

def register_user(username, email, password, full_name):
    """Register a new user"""
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return False, "Username already exists"
        
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return False, "Email already registered"
        
        # Hash password
        password_hash = hash_password(password)
        
        # Insert new user
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, 'user'))
        
        conn.commit()
        conn.close()
        return True, "Registration successful! Please log in."
        
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

def authenticate_user(username, password):
    """Authenticate user login"""
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        # Get user by username
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            # Check password
            if user[3] == hash_password(password):
                # Update last login
                cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.now(), user[0]))
                conn.commit()
                
                # Return user data as dictionary
                user_data = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'full_name': user[4],
                    'role': user[5],
                    'created_at': user[6],
                    'last_login': user[7]
                }
                conn.close()
                return True, user_data
            else:
                conn.close()
                return False, "Invalid password"
        else:
            conn.close()
            return False, "User not found"
            
    except Exception as e:
        return False, f"Authentication failed: {str(e)}"

def show_login_page():
    """Display the login page"""
    # Clean header
    st.markdown("""
    <div class="login-header fade-in">
        <h1 style="margin: 0; font-size: 3.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); font-weight: 700;">
            Heart Disease Prediction
        </h1>
        <h2 style="margin: 0.75rem 0; font-size: 1.8rem; opacity: 0.95; font-weight: 500;">
            Advanced ECG Analysis with AI
        </h2>
        <p style="margin: 0; font-size: 1.2rem; opacity: 0.9; font-weight: 400;">
            Secure Login • Professional Analysis • AI-Powered Results
        </p>
        <div style="margin-top: 1.5rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.75rem 1.5rem; border-radius: 25px; margin: 0 0.5rem; font-weight: 600;">
                Secure Authentication
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.75rem 1.5rem; border-radius: 25px; margin: 0 0.5rem; font-weight: 600;">
                AI Analysis
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.75rem 1.5rem; border-radius: 25px; margin: 0 0.5rem; font-weight: 600;">
                Real-time Results
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown("""
        <div class="login-container fade-in">
            <h3 style="color: #2c3e50; margin-bottom: 1.5rem; font-weight: 700; text-align: center;">🔐 Welcome Back</h3>
            <p style="color: #2c3e50; line-height: 1.7; font-size: 1.1rem; text-align: center; margin-bottom: 2rem;">
                Sign in to access the advanced ECG analysis system and start analyzing heart conditions with AI-powered accuracy.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit_login = st.form_submit_button("🔐 Login", use_container_width=True)
            with col2:
                if st.form_submit_button("🔄 Reset", use_container_width=True):
                    st.rerun()
            
            if submit_login:
                if username and password:
                    success, result = authenticate_user(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user = result
                        st.markdown('<div class="success-msg fade-in">✅ Login successful! Welcome back!</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-msg fade-in">❌ {html.escape(str(result))}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="warning-msg fade-in">⚠️ Please fill in all fields</div>', unsafe_allow_html=True)
        
        # Demo credentials - only show for admin users
        if 'user' in st.session_state and st.session_state.user.get('role') == 'admin':
            st.markdown("""
            <div class="stForm fade-in">
                <h4 style="color: #2c3e50; margin-bottom: 1rem; font-weight: 600;">🧪 Demo Credentials (Admin Only)</h4>
                <p style="color: #2c3e50; line-height: 1.6; font-size: 1rem;">
                    <strong>Username:</strong> admin<br>
                    <strong>Password:</strong> admin123
                </p>
                <p style="color: #6c757d; font-size: 0.9rem; font-style: italic; margin-top: 1rem;">
                    These credentials are for testing purposes only.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="login-container fade-in">
            <h3 style="color: #2c3e50; margin-bottom: 1.5rem; font-weight: 700; text-align: center;">📝 Create Account</h3>
            <p style="color: #2c3e50; line-height: 1.7; font-size: 1.1rem; text-align: center; margin-bottom: 2rem;">
                Join our platform to access advanced ECG analysis tools and track your health monitoring journey.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("register_form"):
            full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            email = st.text_input("📧 Email", placeholder="Enter your email address")
            new_username = st.text_input("🔑 Username", placeholder="Choose a username")
            new_password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit_register = st.form_submit_button("📝 Register", use_container_width=True)
            with col2:
                if st.form_submit_button("🔄 Clear", use_container_width=True):
                    st.rerun()
            
            if submit_register:
                if not all([full_name, email, new_username, new_password, confirm_password]):
                    st.markdown('<div class="warning-msg fade-in">⚠️ Please fill in all fields</div>', unsafe_allow_html=True)
                elif not validate_email(email):
                    st.markdown('<div class="error-msg fade-in">❌ Please enter a valid email address</div>', unsafe_allow_html=True)
                elif new_password != confirm_password:
                    st.markdown('<div class="error-msg fade-in">❌ Passwords do not match</div>', unsafe_allow_html=True)
                else:
                    is_valid, password_msg = validate_password(new_password)
                    if not is_valid:
                        st.markdown(f'<div class="error-msg fade-in">❌ {html.escape(str(password_msg))}</div>', unsafe_allow_html=True)
                    else:
                        success, result = register_user(new_username, email, new_password, full_name)
                        if success:
                            st.markdown(f'<div class="success-msg fade-in">✅ {html.escape(str(result))}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="error-msg fade-in">❌ {html.escape(str(result))}</div>', unsafe_allow_html=True)
        
        # Password requirements
        st.markdown("""
        <div class="stForm fade-in">
            <h4 style="color: #2c3e50; margin-bottom: 1rem; font-weight: 600;">🔒 Password Requirements</h4>
            <ul style="color: #2c3e50; line-height: 1.8; font-size: 1rem;">
                <li>At least 8 characters long</li>
                <li>Contains at least one uppercase letter</li>
                <li>Contains at least one lowercase letter</li>
                <li>Contains at least one number</li>
            </ul>
            <p style="color: #6c757d; font-size: 0.9rem; font-style: italic; margin-top: 1rem;">
                Strong passwords help protect your account and data.
            </p>
        </div>
        """, unsafe_allow_html=True)

def show_user_dashboard():
    """Display user dashboard in sidebar"""
    if 'user' in st.session_state:
        user = st.session_state.user
        
        st.markdown(f"""
        <div class="user-dashboard fade-in">
            <h4 style="margin: 0 0 0.5rem 0; font-weight: 700;">👤 {html.escape(user['full_name'])}</h4>
            <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">@{html.escape(user['username'])}</p>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.8; font-size: 0.8rem;">Role: {html.escape(user['role'].title())}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User actions
        st.markdown("""
        <div class="stForm fade-in">
            <h5 style="color: #2c3e50; margin-bottom: 1rem; font-weight: 600;">⚙️ Account Actions</h5>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👤 Profile", use_container_width=True):
                st.info("Profile management coming soon!")
        
        with col2:
            if st.button("🔐 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.markdown('<div class="success-msg fade-in">✅ Logged out successfully!</div>', unsafe_allow_html=True)
                st.rerun()

def check_authentication():
    """Check if user is authenticated"""
    # Initialize database
    init_database()
    
    # Check if user is already authenticated
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        return True
    
    # Show login page if not authenticated
    show_login_page()
    return False 