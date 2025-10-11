import streamlit as st
from backend.auth import require_auth, get_user_role, get_current_user, get_all_users, update_user_role, deactivate_user, activate_user, get_user_activity, register_user
from backend.cms_manager import load_cms_content, update_home_content, get_cms_metadata
from backend.contact_api import load_contact_messages, save_contact_message
from backend.newsletter_api import load_subscribers, add_subscriber
import json
from datetime import datetime
import csv
from io import StringIO



# Require admin authentication
require_auth()
if get_user_role() not in ["admin", "super_admin"]:
    st.error("❌ Access denied. Admin privileges required.")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: white;
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .admin-title {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .admin-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .admin-tabs {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    .tab-content {
        background: white;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .cms-editor {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .save-button {
        background-color: #16a34a;
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        font-weight: bold;
    }
    .preview-button {
        background-color: #3b82f6;
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 0.5rem;
        cursor: pointer;
        margin-right: 1rem;
    }
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
    }
    .data-table th, .data-table td {
        border: 1px solid #e5e7eb;
        padding: 0.75rem;
        text-align: left;
    }
    .data-table th {
        background-color: #f3f4f6;
        font-weight: bold;
    }
    .metadata {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        font-size: 0.875rem;
        color: #6b7280;
    }
</style>
""", unsafe_allow_html=True)

def main():
    user = get_current_user()
    role = get_user_role()
    
    # Admin Header
    st.markdown(f"""
    <div class="admin-header">
        <h1 class="admin-title">🛠️ Admin Panel</h1>
        <p class="admin-subtitle">Welcome, {user.get('name', 'Admin')} ({role})</p>
    </div>
    """, unsafe_allow_html=True)

    # Admin Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Content Management (CMS)", "📧 Newsletter Subscribers", "💬 Contact Messages", "👥 User Management"])

    with tab1:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.header("📝 Content Management System")
        
        # Load current content
        content = load_cms_content()
        home_content = content["home_content"]
        metadata = get_cms_metadata()
        
        # Metadata display
        st.markdown(f"""
        <div class="metadata">
            Last Updated: {metadata.get('last_updated', 'Never')} by {metadata.get('updated_by', 'System')}
        </div>
        """, unsafe_allow_html=True)
        
        # CMS Editor
        st.subheader("Edit Home Page Content")
        
        # About Section
        st.markdown("### About Us Section")
        with st.form("about_form"):
            about_text = st.text_area(
                "About Content",
                value=home_content.get("about", ""),
                height=150,
                help="Edit the About Us section content"
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                preview_col, save_col = st.columns([1, 1])
                with preview_col:
                    preview_btn = st.form_submit_button("👁️ Preview")
                with save_col:
                    save_btn = st.form_submit_button("💾 Save About")
            
            if save_btn:
                update_home_content({"about": about_text}, user.get('username'))
                st.success("✅ About section updated!")
                st.rerun()
        
        # Vision Section
        st.markdown("### Vision Section")
        with st.form("vision_form"):
            vision_text = st.text_area(
                "Vision Content",
                value=home_content.get("vision", ""),
                height=150,
                help="Edit the Vision section content"
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                preview_col, save_col = st.columns([1, 1])
                with preview_col:
                    preview_btn = st.form_submit_button("👁️ Preview")
                with save_col:
                    save_btn = st.form_submit_button("💾 Save Vision")
            
            if save_btn:
                update_home_content({"vision": vision_text}, user.get('username'))
                st.success("✅ Vision section updated!")
                st.rerun()
        
        # Mission Section
        st.markdown("### Mission Section")
        with st.form("mission_form"):
            mission_text = st.text_area(
                "Mission Content",
                value=home_content.get("mission", ""),
                height=150,
                help="Edit the Mission section content"
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                preview_col, save_col = st.columns([1, 1])
                with preview_col:
                    preview_btn = st.form_submit_button("👁️ Preview")
                with save_col:
                    save_btn = st.form_submit_button("💾 Save Mission")
            
            if save_btn:
                update_home_content({"mission": mission_text}, user.get('username'))
                st.success("✅ Mission section updated!")
                st.rerun()
        
        # Contact Info
        st.markdown("### Contact Information")
        with st.form("contact_form"):
            col1, col2 = st.columns(2)
            with col1:
                contact_email = st.text_input("Contact Email", value=home_content.get("contact", {}).get("email", ""))
                contact_phone = st.text_input("Contact Phone", value=home_content.get("contact", {}).get("phone", ""))
            with col2:
                contact_address = st.text_area("Contact Address", value=home_content.get("contact", {}).get("address", ""), height=100)
            
            save_btn = st.form_submit_button("💾 Save Contact Info")
            
            if save_btn:
                contact_info = {
                    "email": contact_email,
                    "phone": contact_phone,
                    "address": contact_address
                }
                update_home_content({"contact": contact_info}, user.get('username'))
                st.success("✅ Contact information updated!")
                st.rerun()
        
        # Preview Section
        st.markdown("### 👁️ Live Preview")
        st.markdown("**About Us:**")
        st.markdown(home_content.get("about", ""))
        
        st.markdown("**Vision:**")
        st.markdown(home_content.get("vision", ""))
        
        st.markdown("**Mission:**")
        st.markdown(home_content.get("mission", ""))
        
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.header("📧 Newsletter Subscribers")
        
        # Add new subscriber
        st.subheader("Add New Subscriber")
        with st.form("add_subscriber_form"):
            email = st.text_input("Email Address")
            submit_btn = st.form_submit_button("Add Subscriber")
            
            if submit_btn and email:
                if add_subscriber(email):
                    st.success("✅ Subscriber added successfully!")
                else:
                    st.error("❌ Email already subscribed or invalid")
        
        # Display subscribers
        st.subheader("Current Subscribers")
        subscribers = load_subscribers()
        
        if subscribers:
            df_data = []
            for subscriber in subscribers:
                df_data.append({
                    "Email": subscriber.get("email"),
                    "Subscribed At": subscriber.get("subscribed_at", ""),
                    "Status": "Active"
                })

            st.dataframe(df_data, use_container_width=True)

            # Export option
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=["Email", "Subscribed At", "Status"])
            writer.writeheader()
            writer.writerows(df_data)
            csv_str = output.getvalue()
            st.download_button(
                "📥 Export Subscribers",
                csv_str,
                "newsletter_subscribers.csv",
                "text/csv"
            )
        else:
            st.info("No subscribers yet.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.header("💬 Contact Messages")
        
        # Display messages
        messages = load_contact_messages()
        
        if messages:
            st.subheader("Recent Messages")
            for message in reversed(messages[-10:]):  # Last 10 messages
                with st.expander(f"Message from {message.get('name', 'Unknown')} - {message.get('created_at', '')}"):
                    st.write(f"**Email:** {message.get('email')}")
                    st.write(f"**Subject:** {message.get('subject')}")
                    st.write(f"**Message:** {message.get('message')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Mark as Read", key=f"read_{message.get('id', '')}"):
                            # TODO: Mark as read
                            st.success("Marked as read!")
                    with col2:
                        if st.button(f"📧 Reply", key=f"reply_{message.get('id', '')}"):
                            st.info("Reply functionality coming soon!")
            
            # Export all messages
            df_data = []
            for message in messages:
                df_data.append({
                    "Name": message.get("name"),
                    "Email": message.get("email"),
                    "Subject": message.get("subject"),
                    "Created At": message.get("created_at"),
                    "Status": "Unread"  # TODO: Implement status
                })

            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=["Name", "Email", "Subject", "Created At", "Status"])
            writer.writeheader()
            writer.writerows(df_data)
            csv_str = output.getvalue()
            st.download_button(
                "📥 Export Messages",
                csv_str,
                "contact_messages.csv",
                "text/csv"
            )
        else:
            st.info("No contact messages yet.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        st.header("👥 User Management")

        # Get all users
        users = get_all_users()
        if users is None:
            st.error("❌ Access denied. Admin privileges required.")
        else:
            st.subheader("All Registered Users")

            # Prepare user data for display
            user_data = []
            for username, user_info in users.items():
                activity = get_user_activity(username)
                user_data.append({
                    "Username": username,
                    "Name": user_info.get("name", ""),
                    "Email": user_info.get("email", ""),
                    "Role": user_info.get("role", "user"),
                    "Status": "Active" if user_info.get("active", True) else "Inactive",
                    "Created At": user_info.get("created_at", ""),
                    "Analyses Count": activity.get("analyses_count", 0) if activity else 0
                })

            if user_data:
                st.dataframe(user_data, use_container_width=True)

                # Create new user (Super Admin only)
                if role == "super_admin":
                    st.subheader("➕ Create New User")
                    with st.form("create_user_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_username = st.text_input("Username")
                            new_email = st.text_input("Email")
                        with col2:
                            new_name = st.text_input("Full Name")
                            new_password = st.text_input("Password", type="password")
                            new_role = st.selectbox("Role", ["user", "admin", "super_admin"])

                        create_btn = st.form_submit_button("Create User")

                        if create_btn:
                            if new_username and new_password and new_email and new_name:
                                success, message = register_user(new_username, new_password, new_email, new_name, new_role)
                                if success:
                                    st.success(f"✅ User '{new_username}' created successfully with role '{new_role}'!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                            else:
                                st.error("❌ All fields are required")

                # User management actions
                st.subheader("User Actions")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("### Change User Role")
                    selected_user = st.selectbox("Select User", [u["Username"] for u in user_data])
                    user_dict = next((u for u in user_data if u["Username"] == selected_user), None)
                    current_role = user_dict["Role"] if user_dict else "user"

                    # Get allowed roles based on current admin's role
                    admin_role = get_user_role()
                    allowed_roles = {
                        "super_admin": ["user", "admin", "super_admin"],
                        "admin": ["user", "admin"]
                    }.get(admin_role, ["user"])

                    new_role = st.selectbox("New Role", allowed_roles, index=allowed_roles.index(current_role) if current_role in allowed_roles else 0)
                    if st.button("Update Role"):
                        success, message = update_user_role(selected_user, new_role)
                        if success:
                            st.success(f"✅ {message}")
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")

                with col2:
                    st.markdown("### Account Status")
                    selected_user_status = st.selectbox("Select User for Status Change", [u["Username"] for u in user_data])
                    user_dict_status = next((u for u in user_data if u["Username"] == selected_user_status), None)
                    current_status = user_dict_status["Status"] if user_dict_status else "Active"
                    if current_status == "Active":
                        if st.button("Deactivate Account"):
                            success, message = deactivate_user(selected_user_status)
                            if success:
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                    else:
                        if st.button("Activate Account"):
                            success, message = activate_user(selected_user_status)
                            if success:
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")

                with col3:
                    st.markdown("### User Activity")
                    selected_user_activity = st.selectbox("Select User for Activity", [u["Username"] for u in user_data])
                    if st.button("View Activity Details"):
                        activity = get_user_activity(selected_user_activity)
                        if activity:
                            st.info(f"""
                            **User Activity for {selected_user_activity}:**
                            - Total Analyses: {activity.get('analyses_count', 0)}
                            - Account Created: {activity.get('created_at', 'Unknown')}
                            - Last Analysis: {activity.get('last_analysis', 'None')}
                            """)
                        else:
                            st.error("❌ Could not retrieve activity data")

                # Export users
                output = StringIO()
                writer = csv.DictWriter(output, fieldnames=["Username", "Name", "Email", "Role", "Status", "Created At", "Analyses Count"])
                writer.writeheader()
                writer.writerows(user_data)
                csv_str = output.getvalue()
                st.download_button(
                    "📥 Export Users",
                    csv_str,
                    "users.csv",
                    "text/csv"
                )
            else:
                st.info("No users found.")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
