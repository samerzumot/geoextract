# Manual Startup Instructions for GeoExtract

Since there seems to be an issue with the automated shell commands, here are the manual steps to get the web application running:

## Step 1: Open Terminal
Open a new terminal window and navigate to the project directory:
```bash
cd /Users/zumot/Desktop/ree/geoextract
```

## Step 2: Check Python Installation
First, verify Python is installed:
```bash
python3 --version
# OR
python --version
```

If Python is not installed, install it from https://python.org

## Step 3: Install Dependencies
Install the required packages:
```bash
pip3 install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings
```

If `pip3` doesn't work, try:
```bash
pip install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings
```

## Step 4: Run the Application
Start the Streamlit application:
```bash
streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## Step 5: Access the Application
Once the application starts, you should see output like:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://0.0.0.0:8501
```

Open your web browser and go to: **http://localhost:8501**

## Troubleshooting

### If you get "command not found" errors:
1. **Python not found**: Install Python 3.8+ from python.org
2. **pip not found**: Install pip or use `python -m pip` instead
3. **streamlit not found**: Make sure you're in the correct directory

### If the port is already in use:
Try a different port:
```bash
streamlit run ui/streamlit_app.py --server.port 8502 --server.address 0.0.0.0
```
Then access: http://localhost:8502

### If you get permission errors:
Make sure you have write permissions in the directory:
```bash
ls -la /Users/zumot/Desktop/ree/geoextract
```

## Alternative: Use Python Virtual Environment
If you have issues with global packages, create a virtual environment:

```bash
# Create virtual environment
python3 -m venv geoextract_env

# Activate it (macOS/Linux)
source geoextract_env/bin/activate

# Install packages
pip install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings

# Run the application
streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## Expected Output
When successful, you should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://0.0.0.0:8501

  For better performance, install the Watchdog module:
  $ xcode-select --install
```

Then open http://localhost:8501 in your browser to see the GeoExtract interface.
