import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import joblib
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

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

def generate_group_report(analyses_group, model, encoder, plans):
    """Generate report for a group of 5 analyses"""
    # Calculate averages
    avg_nitrogen = np.mean([a['data']['nitrogen'] for a in analyses_group])
    avg_phosphorus = np.mean([a['data']['phosphorus'] for a in analyses_group])
    avg_potassium = np.mean([a['data']['potassium'] for a in analyses_group])
    avg_ph = np.mean([a['data']['ph'] for a in analyses_group])
    avg_temperature = np.mean([a['data']['temperature'] for a in analyses_group])
    avg_humidity = np.mean([a['data']['humidity'] for a in analyses_group])
    avg_rainfall = np.mean([a['data']['rainfall'] for a in analyses_group])

    # Predict crop using averaged values
    input_data = np.array([[avg_nitrogen, avg_phosphorus, avg_potassium, avg_ph, avg_temperature, avg_humidity, avg_rainfall]])
    prediction_encoded = model.predict(input_data)[0]
    predicted_crop = encoder.inverse_transform([prediction_encoded])[0]

    # Get implementation plan
    crop_info = plans.get(predicted_crop, {})
    variants = list(crop_info.get('variants', {}).keys())
    plan = None
    if variants:
        # Check if all analyses in group have the same selected variant
        selected_variants = [a['data'].get('selected_variant') for a in analyses_group if a['data'].get('selected_variant')]
        if selected_variants and len(set(selected_variants)) == 1 and selected_variants[0] in variants:
            # Use the commonly selected variant
            plan = crop_info['variants'][selected_variants[0]]
        else:
            # Use first variant as default
            plan = crop_info['variants'][variants[0]]

    # Get date range
    dates = [datetime.fromisoformat(a['timestamp']) for a in analyses_group]
    start_date = min(dates).strftime('%Y-%m-%d')
    end_date = max(dates).strftime('%Y-%m-%d')

    return {
        'group_id': f"Group {len(analyses_group)} analyses ({start_date} to {end_date})",
        'predicted_crop': predicted_crop,
        'avg_parameters': {
            'nitrogen': avg_nitrogen,
            'phosphorus': avg_phosphorus,
            'potassium': avg_potassium,
            'ph': avg_ph,
            'temperature': avg_temperature,
            'humidity': avg_humidity,
            'rainfall': avg_rainfall
        },
        'plan': plan,
        'analyses_count': len(analyses_group)
    }

def generate_group_pdf_report(report):
    """Generate PDF report for group analysis"""
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
    elements.append(Paragraph("Group Soil Analysis Report", title_style))
    elements.append(Spacer(1, 12))

    # Group Info
    elements.append(Paragraph(f"Report ID: {report['group_id']}", normal_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    elements.append(Spacer(1, 12))

    # Predicted Crop
    elements.append(Paragraph(f"Predicted Crop: {report['predicted_crop']}", heading_style))
    elements.append(Paragraph("Confidence: Based on averaged parameters", normal_style))
    elements.append(Spacer(1, 12))

    # Averaged Soil Parameters Table
    elements.append(Paragraph("Averaged Soil Parameters:", heading_style))

    param_data = [
        ['Parameter', 'Average Value', 'Unit'],
        ['Nitrogen', f"{report['avg_parameters']['nitrogen']:.1f}", 'ppm'],
        ['Phosphorus', f"{report['avg_parameters']['phosphorus']:.1f}", 'ppm'],
        ['Potassium', f"{report['avg_parameters']['potassium']:.1f}", 'ppm'],
        ['pH', f"{report['avg_parameters']['ph']:.1f}", ''],
        ['Temperature', f"{report['avg_parameters']['temperature']:.1f}", '°C'],
        ['Humidity', f"{report['avg_parameters']['humidity']:.1f}", '%'],
        ['Rainfall', f"{report['avg_parameters']['rainfall']:.1f}", 'cm']
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
    if report['plan']:
        elements.append(Paragraph("Implementation Plan:", heading_style))
        for key, value in report['plan'].items():
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
    """Reports page"""
    from backend.auth import require_auth, get_user_role, get_all_users
    require_auth()

    role = get_user_role()

    st.markdown("### 📊 Group Reports")

    from backend.auth import get_user_analyses

    # Super admin can select user
    if role == "super_admin":
        users = get_all_users()
        if users:
            user_options = list(users.keys())
            selected_username = st.selectbox("Select User", user_options, index=user_options.index(st.session_state.username) if st.session_state.username in user_options else 0)
        else:
            selected_username = st.session_state.username
    else:
        selected_username = st.session_state.username

    analyses = get_user_analyses(selected_username)

    if not analyses:
        st.info("No analysis reports available.")
        return

    # Load model data
    model, encoder, plans = load_model_data()
    if model is None:
        return

    # Group analyses in chunks of 5
    group_size = 5
    groups = [analyses[i:i + group_size] for i in range(0, len(analyses), group_size)]

    # Filter out incomplete groups
    complete_groups = [g for g in groups if len(g) == group_size]

    if not complete_groups:
        st.info("Not enough analyses to generate group reports. Need at least 5 analyses per group.")
        return

    st.markdown(f"### Group Reports ({len(complete_groups)} groups)")

    for group_report in complete_groups:
        report = generate_group_report(group_report, model, encoder, plans)

        with st.expander(f"📊 {report['group_id']} - Predicted: {report['predicted_crop']}"):
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown(f"### 🌾 **Predicted Crop**")
                st.markdown(f"# {report['predicted_crop']}")
                st.markdown(f"**Analyses in Group:** {report['analyses_count']}")

                # Display averaged parameters
                st.markdown("### 📋 Averaged Soil Parameters")
                params = report['avg_parameters']
                st.markdown(f"**Nitrogen:** {params['nitrogen']:.1f} ppm")
                st.markdown(f"**Phosphorus:** {params['phosphorus']:.1f} ppm")
                st.markdown(f"**Potassium:** {params['potassium']:.1f} ppm")
                st.markdown(f"**pH:** {params['ph']:.1f}")
                st.markdown(f"**Temperature:** {params['temperature']:.1f}°C")
                st.markdown(f"**Humidity:** {params['humidity']:.1f}%")
                st.markdown(f"**Rainfall:** {params['rainfall']:.1f} cm")

            with col2:
                # Implementation plan
                if report['plan']:
                    st.markdown("### 📋 Implementation Plan")

                    for key, value in report['plan'].items():
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
                else:
                    st.info("No implementation plan available for this crop.")

                # Download section
                st.markdown("### 📤 Download Report")
                col_pdf, col_csv = st.columns(2)

                with col_pdf:
                    pdf_buffer = generate_group_pdf_report(report)
                    pdf_data = pdf_buffer.getvalue()
                    st.download_button(
                        label="📋 Download PDF",
                        data=pdf_data,
                        file_name=f"group_report_{report['group_id'].replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                with col_csv:
                    # Create CSV data
                    csv_data = {
                        'Group ID': report['group_id'],
                        'Predicted Crop': report['predicted_crop'],
                        'Analyses Count': report['analyses_count'],
                        'Avg Nitrogen (ppm)': report['avg_parameters']['nitrogen'],
                        'Avg Phosphorus (ppm)': report['avg_parameters']['phosphorus'],
                        'Avg Potassium (ppm)': report['avg_parameters']['potassium'],
                        'Avg pH': report['avg_parameters']['ph'],
                        'Avg Temperature (°C)': report['avg_parameters']['temperature'],
                        'Avg Humidity (%)': report['avg_parameters']['humidity'],
                        'Avg Rainfall (cm)': report['avg_parameters']['rainfall']
                    }
                    df = pd.DataFrame([csv_data])
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📊 Download CSV",
                        data=csv,
                        file_name=f"group_report_{report['group_id'].replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

if __name__ == "__main__":
    main()
