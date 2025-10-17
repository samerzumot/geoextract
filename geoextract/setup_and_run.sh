#!/bin/bash

# GeoExtract Complete Setup and Run Script
echo "🗺️  GeoExtract - Complete Setup and Launch"
echo "=============================================="

# Change to the correct directory
cd /Users/zumot/Desktop/ree/geoextract

# Check if we're in the right directory
if [ ! -f "ui/streamlit_app.py" ]; then
    echo "❌ Error: streamlit_app.py not found. Make sure you're in the geoextract directory."
    exit 1
fi

echo "✅ Found streamlit_app.py"

# Check Python installation
echo "🐍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✅ Found python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✅ Found python"
else
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check pip installation
echo "📦 Checking pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    echo "✅ Found pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    echo "✅ Found pip"
else
    echo "❌ pip not found. Please install pip."
    exit 1
fi

# Install required packages
echo "📦 Installing required packages..."
$PIP_CMD install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings

if [ $? -ne 0 ]; then
    echo "❌ Failed to install packages. Trying alternative method..."
    $PYTHON_CMD -m pip install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings
    
    if [ $? -ne 0 ]; then
        echo "❌ Package installation failed. Please install manually:"
        echo "pip install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings"
        exit 1
    fi
fi

echo "✅ Packages installed successfully!"

# Test if streamlit can be imported
echo "🧪 Testing streamlit installation..."
$PYTHON_CMD -c "import streamlit; print('✅ Streamlit import successful')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Streamlit import failed. Please check your Python environment."
    exit 1
fi

# Check for available ports
echo "🔌 Checking port availability..."
for port in 8501 8502 8503 8504; do
    if ! lsof -i :$port &> /dev/null; then
        AVAILABLE_PORT=$port
        echo "✅ Port $port is available"
        break
    else
        echo "⚠️  Port $port is in use"
    fi
done

if [ -z "$AVAILABLE_PORT" ]; then
    echo "❌ No available ports found. Please free up a port or kill existing processes."
    exit 1
fi

# Start the Streamlit application
echo ""
echo "🚀 Starting GeoExtract web interface..."
echo "📱 The application will be available at: http://localhost:$AVAILABLE_PORT"
echo "🛑 Press Ctrl+C to stop the application"
echo "=============================================="

# Run Streamlit
$PYTHON_CMD -m streamlit run ui/streamlit_app.py --server.port $AVAILABLE_PORT --server.address 0.0.0.0
