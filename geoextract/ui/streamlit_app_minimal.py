"""Minimal Streamlit app for GeoExtract."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import tempfile
import zipfile
import io
from typing import List, Dict, Any
import folium
from streamlit_folium import st_folium
import sys
import os

# Add the parent directory to the path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import minimal processing service
try:
    from processing_service_minimal import MinimalProcessingService
    print("✅ MinimalProcessingService imported successfully")
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Configure page
st.set_page_config(
    page_title="GeoExtract - Minimal",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.markdown('<h1 class="main-header">🗺️ GeoExtract - Minimal Version</h1>', unsafe_allow_html=True)
st.markdown("### Simplified Geological Report Data Extraction System")

# Sidebar
st.sidebar.title("Configuration")

# LLM Configuration
st.sidebar.subheader("LLM Settings")
llm_provider = st.sidebar.selectbox(
    "LLM Provider",
    ["ollama", "openai", "anthropic"],
    index=0
)
llm_model = st.sidebar.text_input(
    "LLM Model",
    value="llama3.1:8b" if llm_provider == "ollama" else "gpt-3.5-turbo"
)

# OCR Configuration
st.sidebar.subheader("OCR Settings")
ocr_engine = st.sidebar.selectbox(
    "OCR Engine",
    ["paddle", "tesseract", "both"],
    index=0
)
confidence_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.8,
    step=0.1
)
language = st.sidebar.selectbox(
    "Language",
    ["en", "es", "fr"],
    index=0
)

# Processing Configuration
st.sidebar.subheader("Processing Settings")
pdf_dpi = st.sidebar.slider(
    "PDF DPI",
    min_value=150,
    max_value=600,
    value=300,
    step=50
)
debug_mode = st.sidebar.checkbox("Debug Mode", value=False)

# Output Configuration
st.sidebar.subheader("Output Settings")
output_format = st.sidebar.multiselect(
    "Output Format",
    ["geojson", "csv"],
    default=["geojson"]
)

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload & Process", "🗺️ Map View", "📊 Data Analysis", "⚙️ Settings"])

with tab1:
    st.header("Document Processing")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF files containing geological reports"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")
        
        # Process button
        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing documents..."):
                # Create temporary directory for processing
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    
                    # Save uploaded files
                    for i, uploaded_file in enumerate(uploaded_files):
                        file_path = temp_path / uploaded_file.name
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    
                    # Process files using minimal processing service
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Initialize minimal processing service
                    processing_service = MinimalProcessingService(
                        llm_provider=llm_provider,
                        llm_model=llm_model,
                        ocr_engine=ocr_engine,
                        confidence_threshold=confidence_threshold,
                        language=language,
                        debug=debug_mode
                    )
                    
                    results = []
                    all_documents = []
                    
                    for i, uploaded_file in enumerate(uploaded_files):
                        status_text.text(f"Processing {uploaded_file.name}...")
                        
                        # Save file temporarily
                        file_path = temp_path / uploaded_file.name
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Process document with progress callback
                        def progress_callback(progress, message):
                            status_text.text(f"Processing {uploaded_file.name}: {message}")
                            progress_bar.progress(progress)
                        
                        result = processing_service.process_document(file_path, progress_callback)
                        
                        if result["success"]:
                            document = result["document"]
                            all_documents.append(document)
                            
                            result_summary = {
                                "filename": uploaded_file.name,
                                "status": "success",
                                "locations": len(document.locations),
                                "samples": len(document.samples),
                                "observations": len(document.observations),
                                "confidence": result["processing_stats"]["extraction_confidence_avg"]
                            }
                        else:
                            result_summary = {
                                "filename": uploaded_file.name,
                                "status": "failed",
                                "locations": 0,
                                "samples": 0,
                                "observations": 0,
                                "confidence": 0.0,
                                "error": result.get("error", "Unknown error")
                            }
                        
                        results.append(result_summary)
                        progress_bar.progress((i + 1) / len(uploaded_files))
                    
                    status_text.text("Processing completed!")
                    
                    # Display results
                    st.subheader("Processing Results")
                    
                    # Create results DataFrame
                    df_results = pd.DataFrame(results)
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Files", len(results))
                    with col2:
                        st.metric("Total Locations", df_results["locations"].sum())
                    with col3:
                        st.metric("Total Samples", df_results["samples"].sum())
                    with col4:
                        st.metric("Avg Confidence", f"{df_results['confidence'].mean():.2f}")
                    
                    # Display results table
                    st.dataframe(df_results, use_container_width=True)
                    
                    # Download results using minimal export
                    if all_documents:
                        # Export minimal data
                        output_dir = temp_path / "exports"
                        output_dir.mkdir()
                        
                        export_paths = processing_service.export_results(
                            all_documents, output_format, output_dir
                        )
                        
                        if "geojson" in output_format and "geojson" in export_paths:
                            geojson_path = export_paths["geojson"]
                            with open(geojson_path, 'r') as f:
                                geojson_data = f.read()
                            
                            st.download_button(
                                label="📥 Download GeoJSON",
                                data=geojson_data,
                                file_name="extracted_data.geojson",
                                mime="application/json"
                            )
                        
                        if "csv" in output_format and "csv" in export_paths:
                            csv_path = export_paths["csv"]
                            with open(csv_path, 'r') as f:
                                csv_data = f.read()
                            
                            st.download_button(
                                label="📥 Download CSV",
                                data=csv_data,
                                file_name="extracted_data.csv",
                                mime="text/csv"
                            )
                    else:
                        st.warning("No documents were successfully processed for export.")

with tab2:
    st.header("Interactive Map")
    
    # Map configuration
    col1, col2 = st.columns([3, 1])
    
    with col2:
        map_center_lat = st.number_input("Center Latitude", value=37.7749, step=0.1)
        map_center_lon = st.number_input("Center Longitude", value=-122.4194, step=0.1)
        map_zoom = st.slider("Zoom Level", min_value=1, max_value=20, value=10)
    
    with col1:
        # Create map
        m = folium.Map(
            location=[map_center_lat, map_center_lon],
            zoom_start=map_zoom,
            tiles="OpenStreetMap"
        )
        
        # Add sample markers (minimal version)
        sample_locations = [
            {"lat": 37.7749, "lon": -122.4194, "name": "Location 1", "type": "drill_hole"},
            {"lat": 37.7849, "lon": -122.4094, "name": "Location 2", "type": "sample_site"},
            {"lat": 37.7649, "lon": -122.4294, "name": "Location 3", "type": "mine"},
        ]
        
        for loc in sample_locations:
            folium.Marker(
                [loc["lat"], loc["lon"]],
                popup=f"{loc['name']} ({loc['type']})",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
        
        # Display map
        st_folium(m, width=700, height=500)
    
    # Map statistics
    st.subheader("Map Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Locations", len(sample_locations))
    with col2:
        st.metric("Drill Holes", len([l for l in sample_locations if l["type"] == "drill_hole"]))
    with col3:
        st.metric("Sample Sites", len([l for l in sample_locations if l["type"] == "sample_site"]))

with tab3:
    st.header("Data Analysis")
    
    # Sample data for analysis (minimal version)
    sample_data = {
        "Element": ["Au", "Ag", "Cu", "Pb", "Zn", "Fe"],
        "Value": [2.5, 15.3, 0.8, 1.2, 3.4, 45.2],
        "Unit": ["g/t", "g/t", "%", "%", "%", "%"],
        "Sample_ID": ["S001", "S001", "S002", "S002", "S003", "S003"]
    }
    
    df = pd.DataFrame(sample_data)
    
    # Element distribution chart
    st.subheader("Element Distribution")
    fig = px.bar(df, x="Element", y="Value", color="Unit", 
                 title="Assay Results by Element")
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

with tab4:
    st.header("Settings & Configuration")
    
    # Current configuration
    st.subheader("Current Configuration")
    
    config_data = {
        "Parameter": [
            "LLM Provider", "LLM Model", "OCR Engine", "Language",
            "Confidence Threshold", "PDF DPI", "Debug Mode", "Output Format"
        ],
        "Value": [
            llm_provider, llm_model, ocr_engine, language,
            str(confidence_threshold), str(pdf_dpi), str(debug_mode), ", ".join(output_format)
        ]
    }
    
    config_df = pd.DataFrame(config_data)
    st.dataframe(config_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "**GeoExtract - Minimal Version** - Simplified Geological Report Data Extraction System | "
    "Built with ❤️ using Python, Streamlit, and minimal dependencies"
)
