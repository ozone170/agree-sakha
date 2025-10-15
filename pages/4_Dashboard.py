import streamlit as st
from backend.auth import require_auth, get_current_user, get_user_role, logout
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Dashboard - AgriSakha",
    page_icon="👤",
    layout="wide"
)

# Require authentication
require_auth()

# Custom CSS
st.markdown("""
<style>
    .dashboard-header {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white;
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .welcome-title {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .welcome-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #16a34a;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #16a34a;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
    }
    .quick-actions {
        background: #367CB5;
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .action-buttons {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    .action-button {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        text-decoration: none;
        color: #374151;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        border: 1px solid #e5e7eb;
    }
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    .recent-analyses {
        background: white;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .analysis-item {
        border-bottom: 1px solid #e5e7eb;
        padding: 1rem 0;
    }
    .analysis-item:last-child {
        border-bottom: none;
    }
    .admin-notice {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        color: #92400e;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    from backend.auth import get_all_users, get_user_analyses

    role = get_user_role()

    # Super admin can select user
    if role == "super_admin":
        users = get_all_users()
        if users:
            user_options = list(users.keys())
            selected_username = st.selectbox("Select User", user_options, index=user_options.index(st.session_state.username) if st.session_state.username in user_options else 0)
            user_data = users.get(selected_username, {})
            username = selected_username
        else:
            user_data = get_current_user()
            username = st.session_state.get("username")
    else:
        user_data = get_current_user()
        username = st.session_state.get("username")

    # Dashboard Header
    st.markdown(f"""
    <div class="dashboard-header">
        <h1 class="welcome-title">👋 Welcome back, {user_data.get('name', username)}!</h1>
        <p class="welcome-subtitle">Your smart farming dashboard is ready</p>
    </div>
    """, unsafe_allow_html=True)

    # Admin Notice
    if role in ["admin", "super_admin"]:
        st.markdown("""
        <div class="admin-notice">
            <strong>🛠️ Admin Access:</strong> You have administrative privileges.
            <a href="/admin" style="color: #92400e; text-decoration: underline;">Access Admin Panel</a>
        </div>
        """, unsafe_allow_html=True)

    # Stats Grid
    analyses = user_data.get('analyses', [])
    total_analyses = len(analyses)

    # Calculate some stats
    recent_analyses = [a for a in analyses if (datetime.now() - datetime.fromisoformat(a['timestamp'])).days <= 30]
    crops_predicted = len(set(a['data'].get('predicted_crop', '') for a in analyses if a['data'].get('predicted_crop')))

    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">{total_analyses}</div>
            <div class="stat-label">Total Analyses</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{recent_analyses}</div>
            <div class="stat-label">This Month</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{crops_predicted}</div>
            <div class="stat-label">Crops Predicted</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{role}</div>
            <div class="stat-label">Account Type</div>
        </div>
    </div>
    """.format(total_analyses=total_analyses, recent_analyses=len(recent_analyses), crops_predicted=crops_predicted, role=role.title()), unsafe_allow_html=True)

    # Quick Actions
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    st.markdown("### 🚀 Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🧠 New Analysis", key="nav_SoilAnalysis"):
                st.switch_page("pages/6_Soil_Analysis.py")
            
    with col2:
        if st.button("🌾 Crop Database", key="nav_CropDatabase"):
            st.switch_page("pages/8_Crop_Database.py")

    with col3:
        if st.button("📊 Reports", key="nav_Reports"):
            st.switch_page("pages/7_Reports.py")

    with col4:
        if st.button("ℹ️ About", key="nav_About"):
            st.switch_page("pages/8_About.py")

    st.markdown('</div>', unsafe_allow_html=True)

    # Recent Analyses
    st.markdown('<div class="recent-analyses">', unsafe_allow_html=True)
    st.markdown("### 📈 Recent Analyses")

    if analyses:
        # Show last 5 analyses
        for analysis in reversed(analyses[-5:]):
            timestamp = datetime.fromisoformat(analysis['timestamp'])
            data = analysis['data']

            selected_plan = data.get('selected_variant', 'N/A')
            st.markdown(f"""
            <div class="analysis-item">
                <strong>{timestamp.strftime('%Y-%m-%d %H:%M')}</strong> -
                Predicted: <strong>{data.get('predicted_crop', 'N/A')}</strong> -
                Area: {data.get('area', 'N/A')} {data.get('area_unit', 'ha')} -
                Plan: {selected_plan}
            </div>
            """, unsafe_allow_html=True)

        if st.button("View All Analyses"):
            st.markdown("### 📋 All Analysis History")
            if analyses:
                # Create a dataframe for better display
                df_data = []
                for analysis in reversed(analyses):
                    timestamp = datetime.fromisoformat(analysis['timestamp'])
                    data = analysis['data']
                    df_data.append({
                        'Date': timestamp.strftime('%Y-%m-%d'),
                        'Time': timestamp.strftime('%H:%M'),
                        'Crop': data.get('predicted_crop', 'N/A'),
                        'Area': f"{data.get('area', 'N/A')} {data.get('area_unit', 'ha')}",
                        'pH': data.get('ph', 'N/A'),
                        'Temperature': f"{data.get('temperature', 'N/A')}°C",
                        'Selected Plan': data.get('selected_variant', 'N/A')
                    })

                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No analysis history yet. Start by analyzing your soil!")
    else:
        st.info("No analysis history yet. Start by analyzing your soil!")

    st.markdown('</div>', unsafe_allow_html=True)

    # Logout button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.success("Logged out successfully!")
            st.markdown("""
            <meta http-equiv="refresh" content="1;url=/">
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
