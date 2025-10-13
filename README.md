# 🌱 Smart Soil Testing & Recommendation System

A modern, AI-powered soil analysis application built with Streamlit that provides intelligent crop recommendations and detailed implementation plans.

## ✨ Features

- **🔐 User Authentication**: Secure signup/login system with session management
- **👤 User Dashboard**: Personal analysis history and profile management
- **🧠 AI-Powered Analysis**: 99.32% accuracy machine learning model for crop prediction
- **📊 Interactive Visualizations**: Real-time charts and data visualization with Plotly
- **🌾 Comprehensive Crop Database**: 22+ crops with 4 implementation variants each
- **📈 Data Export**: Export analysis results to JSON and CSV formats
- **📱 Modern UI**: Clean, responsive interface built with Streamlit
- **🔬 Soil Parameter Analysis**: N, P, K, pH, Temperature, Humidity, Rainfall analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd agree-sakha
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements_streamlit.txt
   ```

3. **Run the application**

   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the application**
   Open your browser and go to: http://localhost:8501

## 📁 Project Structure

```
agree-sakha/
├── streamlit_app.py              # Main Streamlit application
├── requirements_streamlit.txt    # Python dependencies
├── README.md                    # This file
└── backend/                     # ML model and data
    ├── crop_dataset.csv         # Training dataset
    ├── crop_model.pkl           # Trained ML model
    ├── label_encoder.pkl        # Label encoder
    ├── implementation_plans.json # Base crop plans
    ├── implementation_plans_expanded.json # Expanded plans
    ├── train_model.py           # Model training script
    └── expand_plans.py          # Plan expansion script
```

## 🎯 How to Use

1. **Soil Analysis Page**

   - Enter soil parameters (N, P, K, pH, Temperature, Humidity, Rainfall)
   - Specify area size and unit
   - Click "Analyze Soil" to get crop recommendations
   - View interactive charts and detailed analysis
   - Export results to JSON or CSV

2. **Crop Database Page**

   - Browse all available crops
   - View detailed implementation plans
   - Compare different variants (Default, High Yield, Organic, Low Input)

3. **About Page**
   - Learn about the application
   - View model accuracy and features

## 🔧 Technical Details

- **Framework**: Streamlit
- **ML Model**: Random Forest Classifier (99.32% accuracy)
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **Export Formats**: JSON, CSV

## 📊 Model Performance

- **Accuracy**: 99.32%
- **Algorithm**: Random Forest Classifier
- **Training Data**: Comprehensive crop dataset
- **Features**: 7 soil parameters

## 🌾 Supported Crops

The system supports 22+ crops including:

- Rice, Wheat, Maize, Cotton
- Sugarcane, Coffee, Tea
- Vegetables, Fruits, and more

Each crop has 4 implementation variants:

- **Default**: Standard farming practices
- **High Yield**: Optimized for maximum production
- **Organic**: Sustainable, chemical-free approach
- **Low Input**: Cost-effective, minimal resource usage

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For support or questions, please open an issue in the repository.

---

**Built with ❤️ using Streamlit and Machine Learning**
