#!/bin/bash
# Setup script for Vercel deployment

# Install system dependencies
apt-get update
apt-get install -y python3-dev python3-pip

# Install Python dependencies
pip install -r requirements_streamlit.txt

# Create necessary directories
mkdir -p backend

# Set permissions
chmod +x streamlit_app.py
