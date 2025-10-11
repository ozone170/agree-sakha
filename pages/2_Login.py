import streamlit as st
from backend.auth import authenticate_user, login_user, is_authenticated



# Redirect if already authenticated
if is_authenticated():
    st.success("You are already logged in!")
    st.markdown("[Go to Dashboard](/dashboard)")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #f8fafc;
        border-radius: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-title {
        color: #16a34a;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        color: #6b7280;
        font-size: 1rem;
    }
    .form-group {
        margin-bottom: 1.5rem;
    }
    .login-button {
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
    .signup-link {
        text-align: center;
        margin-top: 1.5rem;
        color: #6b7280;
    }
    .signup-link a {
        color: #16a34a;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <h1 class="login-title">🔐 Login to AgriSakha</h1>
            <p class="login-subtitle">Access your smart farming dashboard</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Login form
    with st.form("login_form"):
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter your username")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        st.markdown('</div>', unsafe_allow_html=True)

        # Login button
        submit_button = st.form_submit_button("Login", use_container_width=True)

        if submit_button:
            if username and password:
                success, result = authenticate_user(username, password)
                if success:
                    login_user(username, result)
                    role = result.get('role', 'user')
                    if role in ["admin", "super_admin"]:
                        st.success("✅ Login successful! Redirecting to admin panel...")
                        st.switch_page("pages/5_Admin_Panel.py")
                    else:
                        st.success("✅ Login successful! Redirecting to dashboard...")
                        st.switch_page("pages/4_Dashboard.py")
                    st.balloons()
                else:
                    st.error(f"❌ {result}")
            else:
                st.error("❌ Please fill in all fields")

    # Signup link
    st.markdown("""
    <div class="signup-link">
        Don't have an account? <a href="/signup">Sign up here</a>
    </div>
    """, unsafe_allow_html=True)

    # Demo credentials
    with st.expander("🔑 Demo Credentials"):
        st.markdown("""
        **Default Admin Account:**
        - Username: `admin`
        - Password: `admin123`

        **Note:** This is for testing purposes. In production, use secure credentials.
        """)

if __name__ == "__main__":
    main()
