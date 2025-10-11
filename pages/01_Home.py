import streamlit as st
import datetime
from backend.auth import is_authenticated, get_user_role
from backend.cms_manager import get_home_content
from backend.contact_api import save_contact_message
from backend.newsletter_api import add_subscriber



# Custom CSS
st.markdown("""
<style>
    .navbar {
        background-color: #16a34a;
        padding: 1rem;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .logo {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
    }
    .nav-links {
        display: flex;
        gap: 1rem;
    }
    .nav-link {
        color: white;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        transition: background-color 0.3s;
    }
    .nav-link:hover {
        background-color: rgba(255,255,255,0.1);
    }
    .hero-section {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white;
        padding: 4rem 2rem;
        text-align: center;
        margin-top: 4rem; /* Account for fixed navbar */
    }
    .hero-title {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        opacity: 0.9;
    }
    .cta-button {
        background-color: white;
        color: #16a34a;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
    }
    .section {
        padding: 3rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .about-card, .vision-card, .mission-card {
        background: white;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .contact-form {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .footer {
        background-color: #1f2937;
        color: white;
        text-align: center;
        padding: 2rem;
        margin-top: 4rem;
    }
    .admin-link {
        background-color: #dc2626;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def render_navbar():
    """Render the dynamic navbar"""
    st.markdown("""
    <div class="navbar">
        <div class="logo">🌾 AgriSakha</div>
        <div class="nav-links">
    """, unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

    with col1:
        if st.button("🏠 Home", key="nav_home"):
            st.switch_page("pages/01_Home.py")

    if not is_authenticated():
        with col2:
            if st.button("Login", key="nav_login"):
                st.switch_page("pages/2_Login.py")
        with col3:
            if st.button("Signup", key="nav_signup"):
                st.switch_page("pages/3_Signup.py")
    else:
        username = st.session_state.get("username", "User")
        role = get_user_role()

        with col2:
            if st.button(f"👤 {username}", key="nav_dashboard"):
                st.switch_page("pages/4_Dashboard.py")

        if role in ["admin", "super_admin"]:
            with col3:
                if st.button("🛠️ Admin", key="nav_admin"):
                    st.switch_page("pages/5_Admin_Panel.py")

        with col4:
            if st.button("Logout", key="nav_logout"):
                from backend.auth import logout
                logout()
                st.success("Logged out successfully!")
                st.switch_page("pages/01_Home.py")

    st.markdown("</div>", unsafe_allow_html=True)

def hero_section():
    """Hero section with CTA"""
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Empowering Farmers with Smart Soil Intelligence 🌱</h1>
        <p class="hero-subtitle">AI-powered soil testing and crop recommendation platform for sustainable agriculture.</p>
    </div>
    """, unsafe_allow_html=True)

    # CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started Today", key="hero_cta", use_container_width=True):
            st.switch_page("pages/2_Login.py")

def about_section():
    """About Us section"""
    cms_content = get_home_content()
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="about-card">', unsafe_allow_html=True)
    st.header("🌾 About AgriSakha")
    st.markdown(cms_content.get("about", "Content not available"))
    st.markdown('</div></div>', unsafe_allow_html=True)

def vision_mission_section():
    """Vision and Mission sections with expanders"""
    cms_content = get_home_content()
    st.markdown('<div class="section">', unsafe_allow_html=True)

    # Vision
    st.markdown('<div class="vision-card">', unsafe_allow_html=True)
    st.header("🎯 Our Vision")
    st.markdown("> " + cms_content.get("vision", "Vision content not available").split('.')[0] + ".")

    with st.expander("Read More"):
        st.markdown(cms_content.get("vision", "Vision content not available"))
    st.markdown('</div>', unsafe_allow_html=True)

    # Mission
    st.markdown('<div class="mission-card">', unsafe_allow_html=True)
    st.header("🚀 Our Mission")
    st.markdown("> " + cms_content.get("mission", "Mission content not available").split('.')[0] + ".")

    with st.expander("Read More"):
        st.markdown(cms_content.get("mission", "Mission content not available"))
    st.markdown('</div></div>', unsafe_allow_html=True)

def newsletter_section():
    """Newsletter signup form"""
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="about-card">', unsafe_allow_html=True)
    st.header("📬 Subscribe to Our Newsletter")
    st.markdown("""
    Stay updated with the latest agricultural insights, new features, and farming tips. Join thousands of farmers 
    who trust AgriSakha for their agricultural intelligence needs.
    """)
    
    with st.form("newsletter_form"):
        email = st.text_input("Enter your email address", placeholder="your.email@example.com")
        col1, col2 = st.columns([3, 1])
        with col2:
            submit_button = st.form_submit_button("Subscribe", use_container_width=True)
        
        if submit_button:
            if email:
                if add_subscriber(email):
                    st.success("✅ You've been subscribed to our newsletter!")
                    st.balloons()
                else:
                    st.error("❌ Email already subscribed or invalid email address.")
            else:
                st.error("❌ Please enter a valid email address.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def contact_section():
    """Contact Us form"""
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    st.header("📞 Contact Us")
    st.markdown("""
    Have questions about our platform or need assistance? We'd love to hear from you. Fill out the form below 
    and our team will get back to you within 24 hours.
    """)
    
    with st.form("contact_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email Address", placeholder="your.email@example.com")
        
        with col2:
            subject = st.text_input("Subject", placeholder="Brief description")
        
        message = st.text_area("Message", placeholder="Write your message here...", height=150)
        
        col1, col2 = st.columns([3, 1])
        with col2:
            submit_button = st.form_submit_button("Send Message", use_container_width=True)
        
        if submit_button:
            if all([name, email, subject, message]):
                combined_message = f"{subject}: {message}"
                if save_contact_message(name, email, combined_message):
                    st.success("✅ Your message has been sent! We'll respond within 24 hours.")
                    st.balloons()
                else:
                    st.error("❌ Failed to send message. Please try again.")
            else:
                st.error("❌ Please fill in all fields.")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def footer():
    """Footer section"""
    st.markdown("""
    <div class="footer">
        <p>&copy; 2025 AgriSakha Technologies Pvt. Ltd. | All Rights Reserved</p>
        <p><a href="#" style="color: #9ca3af; text-decoration: none;">Privacy Policy</a> | 
           <a href="#" style="color: #9ca3af; text-decoration: none;">Terms of Use</a></p>
    </div>
    """, unsafe_allow_html=True)

# Main page content
def main():
    render_navbar()
    hero_section()
    about_section()
    vision_mission_section()
    newsletter_section()
    contact_section()
    footer()

if __name__ == "__main__":
    main()
