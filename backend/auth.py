import streamlit as st
import yaml
import os
import hashlib
from datetime import datetime

# User data file
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.yaml')

def load_user_data():
    """Load user data from YAML file"""
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return yaml.safe_load(file) or {}
    return {}

def save_user_data(data):
    """Save user data to YAML file"""
    os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)
    with open(USER_DATA_FILE, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, email, name, role="user"):
    """Register a new user"""
    user_data = load_user_data()

    if username in user_data:
        return False, "Username already exists"

    if not all([username, password, email, name]):
        return False, "All fields are required"

    if len(password) < 6:
        return False, "Password must be at least 6 characters long"

    hashed_password = hash_password(password)
    user_data[username] = {
        'password': hashed_password,
        'email': email,
        'name': name,
        'role': role,
        'created_at': datetime.now().isoformat(),
        'analyses': []
    }

    save_user_data(user_data)
    return True, "Registration successful"

def authenticate_user(username, password):
    """Authenticate user login"""
    user_data = load_user_data()

    if username not in user_data:
        return False, "Username not found"

    hashed_password = hash_password(password)
    if user_data[username]['password'] != hashed_password:
        return False, "Incorrect password"

    return True, user_data[username]

def is_authenticated():
    """Check if user is currently authenticated"""
    return st.session_state.get("authenticated", False)

def get_user_role():
    """Get current user's role"""
    if is_authenticated():
        return st.session_state.get("role", "user")
    return None

def get_current_user():
    """Get current user data"""
    if is_authenticated():
        username = st.session_state.get("username")
        user_data = load_user_data()
        return user_data.get(username)
    return None

def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.user_data = {}

def login_user(username, user_info):
    """Set session state for logged in user"""
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.role = user_info.get('role', 'user')
    st.session_state.user_data = user_info

def require_auth():
    """Require authentication for a page"""
    if not is_authenticated():
        st.error("Please login to access this page")
        st.stop()

def require_role(required_role):
    """Require specific role for a page"""
    if not is_authenticated():
        st.error("Please login to access this page")
        st.stop()

    user_role = get_user_role()
    if user_role not in required_role:
        st.error("You don't have permission to access this page")
        st.stop()

def get_all_users():
    """Get all users (admin only)"""
    if get_user_role() not in ["admin", "super_admin"]:
        return None
    return load_user_data()

def update_user_role(username, new_role):
    """Update user role (admin only)"""
    current_role = get_user_role()
    if current_role not in ["admin", "super_admin"]:
        return False, "Permission denied"

    # Role hierarchy: super_admin > admin > user
    allowed_roles = {
        "super_admin": ["user", "admin", "super_admin"],
        "admin": ["user", "admin"]  # admin cannot promote to super_admin
    }

    if new_role not in allowed_roles.get(current_role, []):
        return False, f"You cannot assign the '{new_role}' role"

    user_data = load_user_data()
    if username not in user_data:
        return False, "User not found"

    user_data[username]['role'] = new_role
    save_user_data(user_data)
    return True, "Role updated successfully"

def deactivate_user(username):
    """Deactivate user account (admin only)"""
    if get_user_role() not in ["admin", "super_admin"]:
        return False, "Permission denied"

    user_data = load_user_data()
    if username not in user_data:
        return False, "User not found"

    # Add deactivated status
    user_data[username]['active'] = False
    save_user_data(user_data)
    return True, "User deactivated successfully"

def activate_user(username):
    """Activate user account (admin only)"""
    if get_user_role() not in ["admin", "super_admin"]:
        return False, "Permission denied"

    user_data = load_user_data()
    if username not in user_data:
        return False, "User not found"

    user_data[username]['active'] = True
    save_user_data(user_data)
    return True, "User activated successfully"

def get_user_activity(username):
    """Get user activity data"""
    user_data = load_user_data()
    if username not in user_data:
        return None
    user = user_data[username]
    return {
        'analyses_count': len(user.get('analyses', [])),
        'created_at': user.get('created_at'),
        'last_analysis': user.get('analyses', [])[-1] if user.get('analyses') else None
    }

def get_user_analyses(username):
    """Get user's analysis history"""
    user_data = load_user_data()
    if username in user_data:
        return user_data[username]['analyses']
    return []

def save_analysis(username, analysis_data):
    """Save analysis data for user"""
    user_data = load_user_data()
    if username in user_data:
        if 'analyses' not in user_data[username]:
            user_data[username]['analyses'] = []
        analysis_entry = {
            "timestamp": datetime.now().isoformat(),
            "data": analysis_data
        }
        user_data[username]['analyses'].append(analysis_entry)
        save_user_data(user_data)
        return True
    return False

# Initialize default admin user if not exists
def initialize_default_admin():
    """Create default admin user if no users exist"""
    user_data = load_user_data()
    if not user_data:
        # Create default admin
        register_user("admin", "admin123", "admin@agrisakha.com", "System Admin", "super_admin")
        print("Default admin user created: admin/admin123")

# Call this when module is imported
initialize_default_admin()
