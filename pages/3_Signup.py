import streamlit as st
from backend.auth import register_user, is_authenticated

# Page configuration
st.set_page_config(
    page_title="Sign Up - AgriSakha",
    page_icon="📝",
    layout="centered"
)

# Redirect if already authenticated
if is_authenticated():
    st.success("You are already logged in!")
    st.markdown("[Go to Dashboard](/dashboard)")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .signup-container {
        max-width: 500px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #f8fafc;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .signup-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .signup-title {
        color: #16a34a;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .signup-subtitle {
        color: #6b7280;
        font-size: 1rem;
    }
    .form-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .form-group {
        flex: 1;
    }
    .signup-button {
        width: 100%;
        background-color: #16a34a;
        color: white;
        padding: 0.75rem;
        border: none;
        border-radius: 0.5rem;
        font-size: 1rem;
        cursor: pointer;
        margin-top: 1rem;
    }
    .login-link {
        text-align: center;
        margin-top: 1.5rem;
        color: #6b7280;
    }
    .login-link a {
        color: #16a34a;
        text-decoration: none;
    }
    .password-requirements {
        font-size: 0.875rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="signup-container">
        <div class="signup-header">
            <h1 class="signup-title">📝 Create AgriSakha Account</h1>
            <p class="signup-subtitle">Join our community of smart farmers</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Signup form
    with st.form("signup_form"):
        # Name and Email row
        st.markdown('<div class="form-row">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="Enter your full name")
        with col2:
            email = st.text_input("Email Address", placeholder="your.email@example.com")
        st.markdown('</div>', unsafe_allow_html=True)

        # Username
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Choose a unique username")
        st.markdown('</div>', unsafe_allow_html=True)

        # Password fields
        st.markdown('<div class="form-row">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", placeholder="Create a password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="password-requirements">
            Password must be at least 6 characters long
        </div>
        """, unsafe_allow_html=True)

        # Signup button
        submit_button = st.form_submit_button("Create Account", use_container_width=True)

        if submit_button:
            if all([name, email, username, password, confirm_password]):
                if password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters long")
                else:
                    success, message = register_user(username, password, email, name)
                    if success:
                        st.success("✅ Registration successful! Please login with your credentials.")
                        st.balloons()
                        st.markdown("""
                        <div style="text-align: center; margin-top: 1rem;">
                            <a href="/login" style="color: #16a34a; text-decoration: none; font-weight: bold;">
                                Go to Login →
                            </a>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ {message}")
            else:
                st.error("❌ Please fill in all fields")

    # Login link
    st.markdown("""
    <div class="login-link">
        Already have an account? <a href="/login">Login here</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
