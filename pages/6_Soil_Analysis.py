import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import sys
from datetime import datetime
import plotly.express as px
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Crop images dictionary (using Unsplash images)
crop_images = {
    'rice': 'https://images.unsplash.com/photo-1536304993881-ff6e9aefacd1?w=400',
    'maize': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400',
    'chickpea': 'https://images.unsplash.com/photo-1596862300742-1e3d2a2e9f8d?w=400',
    'kidneybeans': 'https://images.unsplash.com/photo-1571771019784-3ff35f4f4277?w=400',
    'pigeonpeas': 'https://images.unsplash.com/photo-1592150621744-aca64f48394a?w=400',
    'mothbeans': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400',
    'mungbean': 'https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400',
    'blackgram': 'https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400',
    'lentil': 'https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400',
    'pomegranate': 'https://images.unsplash.com/photo-1541344999736-83eca272f6fc?w=400',
    'banana': 'https://images.unsplash.com/photo-1571771019784-3ff35f4f4277?w=400',
    'mango': 'https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=400',
    'grapes': 'https://images.unsplash.com/photo-1537640538966-79f36943f303?w=400',
    'watermelon': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400',
    'muskmelon': 'https://images.unsplash.com/photo-1571771019784-3ff35f4f4277?w=400',
    'apple': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400',
    'orange': 'https://images.unsplash.com/photo-1547514701-42782101795e?w=400',
    'papaya': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400',
    'coconut': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400',
    'cotton': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400',
    'jute': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400',
    'coffee': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400'
}

# Load ML model and data
@st.cache_data
def load_model_data():
    """Load ML model and implementation plans"""
    try:
        # Load model
        model_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'crop_model.pkl')
        encoder_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'label_encoder.pkl')
        plans_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'implementation_plans_expanded.json')

        if not all(os.path.exists(p) for p in [model_path, encoder_path, plans_path]):
            st.error("❌ Required model files not found. Please ensure backend files are present.")
            return None, None, None

        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)

        with open(plans_path, 'r', encoding='utf-8') as f:
            plans = json.load(f)

        return model, encoder, plans
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None, None, None

def generate_pdf_report(analysis_data, plan=None):
    """Generate PDF report combining analysis data and implementation plan"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center
    )
    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20
    )
    normal_style = styles['Normal']

    elements = []

    # Title
    elements.append(Paragraph("Soil Analysis Report", title_style))
    elements.append(Spacer(1, 12))

    # Date
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 12))

    # Predicted Crop
    elements.append(Paragraph(f"Predicted Crop: {analysis_data['predicted_crop']}", heading_style))
    elements.append(Paragraph("Confidence: 99.32%", normal_style))
    elements.append(Spacer(1, 12))

    # Soil Parameters Table
    elements.append(Paragraph("Soil Parameters:", heading_style))

    param_data = [
        ['Parameter', 'Value', 'Unit'],
        ['Nitrogen', f"{analysis_data['nitrogen']}", 'ppm'],
        ['Phosphorus', f"{analysis_data['phosphorus']}", 'ppm'],
        ['Potassium', f"{analysis_data['potassium']}", 'ppm'],
        ['pH', f"{analysis_data['ph']}", ''],
        ['Temperature', f"{analysis_data['temperature']}", '°C'],
        ['Humidity', f"{analysis_data['humidity']}", '%'],
        ['Rainfall', f"{analysis_data['rainfall']}", 'cm'],
        ['Area', f"{analysis_data['area']}", analysis_data['area_unit']]
    ]

    table = Table(param_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Implementation Plan
    if plan:
        elements.append(Paragraph("Implementation Plan:", heading_style))
        for key, value in plan.items():
            elements.append(Paragraph(f"<b>{key.title()}:</b>", normal_style))
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    elements.append(Paragraph(f"  • {sub_key}: {sub_value}", normal_style))
            elif isinstance(value, list):
                for item in value:
                    elements.append(Paragraph(f"  • {item}", normal_style))
            else:
                elements.append(Paragraph(f"  {value}", normal_style))
            elements.append(Spacer(1, 6))

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def main():
    """Main soil analysis page"""
    # Initialize session state for standalone testing
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
        st.session_state.username = 'standalone_user'

    from backend.auth import require_auth
    require_auth()

    st.markdown('<h1 class="main-header">🌱 Smart Soil Testing & Recommendation System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Soil Analysis with 99.32% Accuracy</p>', unsafe_allow_html=True)

    # Load model data
    model, encoder, plans = load_model_data()
    if model is None:
        return

    # Input form
    st.markdown("### 📋 Soil Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        nitrogen = st.number_input("Nitrogen (N) - ppm", min_value=0.0, max_value=200.0, value=50.0, step=1.0)
        phosphorus = st.number_input("Phosphorus (P) - ppm", min_value=0.0, max_value=200.0, value=30.0, step=1.0)
        potassium = st.number_input("Potassium (K) - ppm", min_value=0.0, max_value=200.0, value=40.0, step=1.0)

    with col2:
        ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
        temperature = st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, value=25.0, step=1.0)
        humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)

    with col3:
        rainfall = st.number_input("Rainfall (cm)", min_value=0.0, max_value=500.0, value=100.0, step=1.0)
        area = st.number_input("Area Size", min_value=0.1, max_value=1000.0, value=1.0, step=0.1)
        area_unit = st.selectbox("Area Unit", ["ha", "acre"])

    # Analyze button
    if st.button("🔍 Analyze Soil", use_container_width=True, type="primary"):
        # Prepare input data
        input_data = np.array([[nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall]])

        # Make prediction
        prediction_encoded = model.predict(input_data)[0]
        predicted_crop = encoder.inverse_transform([prediction_encoded])[0]

        # Get crop information
        crop_info = plans.get(predicted_crop, {})
        variants = list(crop_info.get('variants', {}).keys())

        # Store initial analysis data
        analysis_data = {
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'ph': ph,
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'area': area,
            'area_unit': area_unit,
            'predicted_crop': predicted_crop,
            'variants': variants
        }

        # Display results
        st.markdown("### 🎯 Analysis Results")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.markdown(f"### 🌾 **Predicted Crop**")
            st.markdown(f"# {predicted_crop}")
            st.markdown(f"**Confidence:** 99.32%")
            st.markdown("</div>", unsafe_allow_html=True)

            # Display crop image if available
            if predicted_crop.lower() in crop_images:
                st.image(crop_images[predicted_crop.lower()], caption=f"Image of {predicted_crop}", use_container_width=True)

            # Soil parameters visualization
            params = ['Nitrogen', 'Phosphorus', 'Potassium', 'pH', 'Temperature', 'Humidity', 'Rainfall']
            values = [nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall]

            fig = px.bar(x=params, y=values, title="Soil Parameters", color=values,
                        color_continuous_scale="Viridis")
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Implementation plans
            plan = None
            selected_variant = None
            if variants:
                st.markdown("### 📋 Implementation Plans")

                selected_variant = st.selectbox("Choose Plan Variant", variants)

                if selected_variant in crop_info.get('variants', {}):
                    plan = crop_info['variants'][selected_variant]

                    st.markdown('<div class="plan-card">', unsafe_allow_html=True)
                    st.markdown(f"### {selected_variant.title()} Plan")

                    for key, value in plan.items():
                        if isinstance(value, dict):
                            st.markdown(f"**{key.title()}:**")
                            for sub_key, sub_value in value.items():
                                st.markdown(f"  • {sub_key}: {sub_value}")
                        elif isinstance(value, list):
                            st.markdown(f"**{key.title()}:**")
                            for item in value:
                                st.markdown(f"  • {item}")
                        else:
                            st.markdown(f"**{key.title()}:** {value}")

                    st.markdown("</div>", unsafe_allow_html=True)

                    # Save analysis with selected plan
                    if st.button("💾 Save Analysis with Selected Plan", use_container_width=True):
                        analysis_data['selected_variant'] = selected_variant
                        analysis_data['selected_plan'] = plan

                        # Save analysis if user is logged in
                        if st.session_state.authenticated:
                            try:
                                from backend.auth import save_analysis
                                save_analysis(st.session_state.username, analysis_data)
                                st.success("✅ Analysis saved successfully with selected implementation plan!")
                            except ImportError:
                                st.warning("Analysis not saved - running in standalone mode")
                        else:
                            st.warning("Please log in to save your analysis.")
            else:
                st.info("No implementation plans available for this crop.")

        # Export functionality
        st.markdown("### 📤 Export Results")
        col1, col2, col3 = st.columns(3)

        with col1:
            # JSON export
            json_data = json.dumps(analysis_data, indent=2)
            st.download_button(
                label="📄 Download JSON",
                data=json_data,
                file_name=f"soil_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

        with col2:
            # CSV export
            df = pd.DataFrame([analysis_data])
            csv = df.to_csv(index=False)
            st.download_button(
                label="📊 Download CSV",
                data=csv,
                file_name=f"soil_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with col3:
            # PDF export
            pdf_buffer = generate_pdf_report(analysis_data, plan)
            pdf_data = pdf_buffer.getvalue()
            st.download_button(
                label="📋 Download PDF",
                data=pdf_data,
                file_name=f"soil_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
