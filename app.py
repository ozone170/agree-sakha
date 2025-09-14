# Vercel entry point for Streamlit app
import subprocess
import sys
import os

def main():
    # Set environment variables for Streamlit
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Run Streamlit app
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
        '--server.port=8501',
        '--server.address=0.0.0.0',
        '--server.headless=true'
    ])

if __name__ == '__main__':
    main()
