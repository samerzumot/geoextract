#!/usr/bin/env python3
"""
Quick Start Script for GeoExtract
This script will attempt to install dependencies and start the web application.
"""

import subprocess
import sys
import os
import socket
from pathlib import Path

def check_python():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def install_packages():
    """Install required packages."""
    print("📦 Installing required packages...")
    
    packages = [
        "streamlit", "fastapi", "uvicorn", "pandas", 
        "plotly", "folium", "streamlit-folium", 
        "pydantic", "pydantic-settings"
    ]
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install"] + packages
        )
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def find_available_port():
    """Find an available port."""
    print("🔌 Finding available port...")
    
    for port in range(8501, 8510):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                print(f"✅ Port {port} is available")
                return port
            except OSError:
                continue
    
    print("❌ No available ports found")
    return None

def start_streamlit(port):
    """Start the Streamlit application."""
    print(f"🚀 Starting Streamlit on port {port}...")
    
    try:
        # Change to the correct directory
        os.chdir(Path(__file__).parent)
        
        # Start streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "ui/streamlit_app.py",
            "--server.port", str(port),
            "--server.address", "0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main function."""
    print("🗺️  GeoExtract Quick Start")
    print("=" * 40)
    
    # Check Python
    if not check_python():
        return
    
    # Install packages
    if not install_packages():
        print("❌ Failed to install packages. Please install manually:")
        print("pip install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings")
        return
    
    # Find available port
    port = find_available_port()
    if not port:
        return
    
    # Start application
    print(f"\n🌐 The application will be available at: http://localhost:{port}")
    print("🛑 Press Ctrl+C to stop the application")
    print("=" * 40)
    
    start_streamlit(port)

if __name__ == "__main__":
    main()
