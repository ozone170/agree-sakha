import streamlit as st

def main():
    """About page"""
    from backend.auth import require_auth
    require_auth()

    st.markdown("### ℹ️ About ")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Agri_sakha:Smart Soil Testing & Recommendation System** is an AI-powered application
        that helps farmers and agricultural professionals make informed decisions
        about crop selection and soil management.

        ### 🌟 Key Features:
        - **AI-Powered Analysis**: 99.32% accuracy machine learning model
        - **Comprehensive Database**: 22+ crops with detailed implementation plans
        - **Interactive Visualizations**: Real-time charts and data analysis
        - **Export Functionality**: Download results in JSON, CSV, and PDF formats
        - **User Authentication**: Secure login and analysis history tracking
        """)

    with col2:
        st.markdown("""
        ### 📊 Model Performance:
        - **Algorithm**: Random Forest Classifier
        - **Accuracy**: 99.32%
        - **Training Data**: Comprehensive crop dataset
        - **Features**: 7 soil parameters

        ### 🌾 Supported Crops:
        The system supports 22+ crops including:
        - Rice, Wheat, Maize, Cotton
        - Sugarcane, Coffee, Tea
        - Vegetables, Fruits, and more

        ### 🔒 Security:
        - Secure user authentication
        - Password hashing
        - Session management
        - Data privacy protection
        """)

if __name__ == "__main__":
    main()
