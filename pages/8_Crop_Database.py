import streamlit as st
import os
import json

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

        import joblib
        model = joblib.load(model_path)
        encoder = joblib.load(encoder_path)

        with open(plans_path, 'r', encoding='utf-8') as f:
            plans = json.load(f)

        return model, encoder, plans
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None, None, None

def main():
    """Crop database page"""
    from backend.auth import require_auth
    require_auth()

    st.markdown("### 🌾 Crop Database")

    model, encoder, plans = load_model_data()
    if model is None:
        return

    # Crop selection
    crops = list(plans.keys())
    selected_crop = st.selectbox("Select a Crop", crops)

    if selected_crop:
        crop_info = plans[selected_crop]

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"### {selected_crop}")
            st.markdown(f"**Summary:** {crop_info.get('summary', 'No summary available')}")

            variants = list(crop_info.get('variants', {}).keys())
            st.markdown(f"**Available Variants:** {', '.join(variants)}")

        with col2:
            # Variant selection
            if variants:
                selected_variant = st.selectbox("Select Variant", variants)

                if selected_variant in crop_info.get('variants', {}):
                    plan = crop_info['variants'][selected_variant]

                    st.markdown(f"### {selected_variant.title()} Implementation Plan")

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

if __name__ == "__main__":
    main()
