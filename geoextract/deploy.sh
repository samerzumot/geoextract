#!/bin/bash

# GeoExtract Deployment Script
echo "🗺️  GeoExtract Deployment Script"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "ui/streamlit_app.py" ]; then
    print_error "streamlit_app.py not found. Make sure you're in the geoextract directory."
    exit 1
fi

print_status "Found streamlit_app.py"

# Check Python installation
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    print_status "Found python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    print_status "Found python"
else
    print_error "Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if packages are installed
print_info "Checking required packages..."
$PYTHON_CMD -c "import streamlit, pandas, plotly, folium" 2>/dev/null
if [ $? -ne 0 ]; then
    print_warning "Some packages missing. Installing required packages..."
    pip3 install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings
    if [ $? -ne 0 ]; then
        print_error "Failed to install packages. Please install manually."
        exit 1
    fi
    print_status "Packages installed successfully"
else
    print_status "All required packages are available"
fi

# Check for running instances
print_info "Checking for existing Streamlit processes..."
EXISTING_PROCESSES=$(ps aux | grep streamlit | grep -v grep | wc -l)
if [ $EXISTING_PROCESSES -gt 0 ]; then
    print_warning "Found existing Streamlit processes. Stopping them..."
    pkill -f streamlit
    sleep 2
fi

# Find available port
print_info "Finding available port..."
for port in 8501 8502 8503 8504 8505; do
    if ! lsof -i :$port &> /dev/null; then
        AVAILABLE_PORT=$port
        print_status "Port $port is available"
        break
    else
        print_warning "Port $port is in use"
    fi
done

if [ -z "$AVAILABLE_PORT" ]; then
    print_error "No available ports found. Please free up a port."
    exit 1
fi

# Create output directories
print_info "Creating output directories..."
mkdir -p output temp logs
print_status "Directories created"

# Start the application
print_info "Starting GeoExtract web application..."
echo ""
echo "🚀 Starting on port $AVAILABLE_PORT"
echo "📱 Access the application at: http://localhost:$AVAILABLE_PORT"
echo "🛑 Press Ctrl+C to stop the application"
echo "================================="

# Start Streamlit
$PYTHON_CMD -m streamlit run ui/streamlit_app.py --server.port $AVAILABLE_PORT --server.address 0.0.0.0
