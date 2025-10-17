#!/usr/bin/env python3
"""
GeoExtract Web Application Launcher
Run this script to start the GeoExtract web interface.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "streamlit", "fastapi", "uvicorn", "pandas", 
            "plotly", "folium", "streamlit-folium", "pydantic", "pydantic-settings"
        ])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def run_streamlit():
    """Run the Streamlit application."""
    print("Starting GeoExtract web interface...")
    try:
        # Change to the geoextract directory
        os.chdir(Path(__file__).parent)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "ui/streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main function."""
    print("🗺️  GeoExtract - Geological Report Data Extraction System")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("ui/streamlit_app.py").exists():
        print("❌ Error: streamlit_app.py not found. Make sure you're in the geoextract directory.")
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements. Please install manually:")
        print("pip install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings")
        return
    
    # Run the application
    print("\n🚀 Starting web application...")
    print("📱 The application will be available at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("=" * 60)
    
    run_streamlit()

if __name__ == "__main__":
    main()
