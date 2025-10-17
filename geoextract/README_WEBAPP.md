# GeoExtract Web Application

🗺️ **GeoExtract** - Open-Source Geological Report Data Extraction System

## Quick Start

To run the GeoExtract web application, follow these steps:

### Option 1: Using the Python Script
```bash
cd /Users/zumot/Desktop/ree/geoextract
python3 run_webapp.py
```

### Option 2: Using the Shell Script
```bash
cd /Users/zumot/Desktop/ree/geoextract
chmod +x start_webapp.sh
./start_webapp.sh
```

### Option 3: Manual Installation and Run
```bash
# Install dependencies
pip3 install streamlit fastapi uvicorn pandas plotly folium streamlit-folium pydantic pydantic-settings

# Run the application
cd /Users/zumot/Desktop/ree/geoextract
streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

## Access the Application

Once running, open your web browser and navigate to:
- **Local**: http://localhost:8501
- **Network**: http://0.0.0.0:8501

## Features

The web application provides:

1. **📄 Document Processing**
   - Upload PDF files containing geological reports
   - Process multiple documents simultaneously
   - Extract geological data using AI/LLM

2. **🗺️ Interactive Map**
   - Visualize extracted locations on an interactive map
   - Configure map center and zoom level
   - View different types of geological features

3. **📊 Data Analysis**
   - Element distribution charts
   - Sample analysis and correlation matrices
   - Raw data tables

4. **⚙️ Configuration**
   - LLM provider settings (Ollama, OpenAI, Anthropic)
   - OCR engine configuration (Paddle, Tesseract)
   - Processing parameters
   - Output format selection

## Configuration

The application supports various configuration options:

- **LLM Providers**: Ollama (default), OpenAI, Anthropic
- **OCR Engines**: Paddle, Tesseract, or both
- **Languages**: English, Spanish, French
- **Output Formats**: GeoJSON, CSV
- **Processing**: PDF DPI, confidence thresholds, debug mode

## Troubleshooting

If you encounter issues:

1. **Python not found**: Install Python 3.8 or higher
2. **Package installation fails**: Try using `pip3` instead of `pip`
3. **Port already in use**: Change the port with `--server.port 8502`
4. **Permission denied**: Make sure the script is executable with `chmod +x start_webapp.sh`

## Stopping the Application

Press `Ctrl+C` in the terminal to stop the application.

## Support

For issues or questions, please check the project documentation or create an issue in the repository.
