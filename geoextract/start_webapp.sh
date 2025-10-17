#!/bin/bash

# GeoExtract Web Application Startup Script
echo "🗺️  GeoExtract - Geological Report Data Extraction System"
echo "============================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
pip3 install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings

if [ $? -ne 0 ]; then
    echo "❌ Failed to install packages. Please install manually:"
    echo "pip3 install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings"
    exit 1
fi

echo "✅ Packages installed successfully!"

# Start the Streamlit application
echo ""
echo "🚀 Starting GeoExtract web interface..."
echo "📱 The application will be available at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the application"
echo "============================================================"

# Run Streamlit
python3 -m streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
