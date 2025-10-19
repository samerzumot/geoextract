"""
GeoExtract - Main Streamlit Application
Optimized for Streamlit Cloud deployment
"""

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

# Configure page
st.set_page_config(
    page_title="GeoExtract",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    .streamlit-badge {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background: #ff4b4b;
        color: #fff;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🗺️ GeoExtract</h1>', unsafe_allow_html=True)
st.markdown("### Open-Source Geological Report Data Extraction System")
st.markdown("☁️ **Deployed on Streamlit Cloud**")

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
save_intermediate = st.sidebar.checkbox("Save Intermediate Files", value=False)

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
    st.markdown("""
    **GeoExtract** is an AI-powered geological data extraction system designed for geologists, mining engineers, and exploration professionals. 
    It automatically processes geological PDF reports to extract coordinates, sample data, and geological features using advanced OCR and LLM technology. 
    The system generates interactive maps and structured datasets for geological analysis and exploration planning. 
    Perfect for mining companies, geological surveys, and research institutions working with geological documentation.
    """)
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
                    
                    # Process files (simplified - in real implementation, call the actual processing functions)
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results = []
                    for i, uploaded_file in enumerate(uploaded_files):
                        status_text.text(f"Processing {uploaded_file.name}...")
                        progress_bar.progress((i + 1) / len(uploaded_files))
                        
                        # Simulate processing (replace with actual processing)
                        result = {
                            "filename": uploaded_file.name,
                            "status": "success",
                            "locations": 5,  # Simulated
                            "samples": 12,   # Simulated
                            "observations": 3,  # Simulated
                            "confidence": 0.85  # Simulated
                        }
                        results.append(result)
                    
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
                    
                    # Download results
                    if "geojson" in output_format:
                        # Create sample GeoJSON (in real implementation, use actual results)
                        sample_geojson = {
                            "type": "FeatureCollection",
                            "features": [
                                {
                                    "type": "Feature",
                                    "geometry": {
                                        "type": "Point",
                                        "coordinates": [-122.4194, 37.7749]
                                    },
                                    "properties": {
                                        "name": "Sample Location",
                                        "location_type": "sample_site",
                                        "confidence": 0.85
                                    }
                                }
                            ]
                        }
                        
                        geojson_str = json.dumps(sample_geojson, indent=2)
                        st.download_button(
                            label="📥 Download GeoJSON",
                            data=geojson_str,
                            file_name="extracted_data.geojson",
                            mime="application/json"
                        )
                    
                    if "csv" in output_format:
                        # Create sample CSV (in real implementation, use actual results)
                        csv_data = df_results.to_csv(index=False)
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv_data,
                            file_name="extracted_data.csv",
                            mime="text/csv"
                        )

with tab2:
    st.header("Interactive Map")
    
    # Map configuration
    col1, col2 = st.columns([3, 1])
    
    with col2:
        map_center_lat = st.number_input("Center Latitude", value=36.0, step=0.1)
        map_center_lon = st.number_input("Center Longitude", value=-115.0, step=0.1)
        map_zoom = st.slider("Zoom Level", min_value=1, max_value=20, value=7)
    
    with col1:
        # Create map
        m = folium.Map(
            location=[map_center_lat, map_center_lon],
            zoom_start=map_zoom,
            tiles="OpenStreetMap"
        )
        
        # Realistic rare earth element deposits near Nevada border
        ree_deposits = [
            # Mountain Pass, California - Largest REE deposit in US
            {"lat": 35.4667, "lon": -115.5333, "name": "Mountain Pass Mine", "type": "active_mine", 
             "description": "Largest REE deposit in US, operated by MP Materials", "elements": "LREE, Ce, La, Nd"},
            
            # Music Valley, California - Southeast Mojave Desert
            {"lat": 33.8333, "lon": -115.6667, "name": "Music Valley", "type": "prospect", 
             "description": "REE deposits in alkaline Proterozoic rocks", "elements": "LREE, HREE"},
            
            # Pinto Mountains, California
            {"lat": 33.9167, "lon": -115.5833, "name": "Pinto Mountains", "type": "prospect", 
             "description": "Alkaline rock-hosted REE mineralization", "elements": "LREE, Th"},
            
            # Halleck Creek, Wyoming - World-class deposit
            {"lat": 42.0833, "lon": -105.0833, "name": "Halleck Creek", "type": "prospect", 
             "description": "2.34B metric tons - potentially world's largest REE deposit", "elements": "LREE, HREE"},
            
            # Round Top Mountain, Texas (near border region)
            {"lat": 30.3333, "lon": -103.6667, "name": "Round Top Mountain", "type": "prospect", 
             "description": "Peralkaline granite-hosted REE deposit", "elements": "HREE, Y, Zr"},
            
            # Bear Lodge, Wyoming
            {"lat": 44.4167, "lon": -104.2500, "name": "Bear Lodge", "type": "prospect", 
             "description": "Carbonatite-hosted REE mineralization", "elements": "LREE, Nd, Pr"},
            
            # Bokan Mountain, Alaska (for reference)
            {"lat": 55.9167, "lon": -133.1667, "name": "Bokan Mountain", "type": "prospect", 
             "description": "Peralkaline granite with HREE enrichment", "elements": "HREE, Y, Dy"},
        ]
        
        for deposit in ree_deposits:
            # Choose icon and color based on deposit type
            if deposit["type"] == "active_mine":
                icon_color = "red"
                icon_name = "home"
            elif deposit["type"] == "prospect":
                icon_color = "blue"
                icon_name = "star"
            else:
                icon_color = "green"
                icon_name = "info-sign"
            
            # Create detailed popup with deposit information
            popup_html = f"""
            <div style="width: 250px;">
                <h4>{deposit['name']}</h4>
                <p><strong>Type:</strong> {deposit['type'].replace('_', ' ').title()}</p>
                <p><strong>Description:</strong> {deposit['description']}</p>
                <p><strong>Elements:</strong> {deposit['elements']}</p>
            </div>
            """
            
            folium.Marker(
                [deposit["lat"], deposit["lon"]],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color=icon_color, icon=icon_name, prefix="fa")
            ).add_to(m)
        
        # Display map
        st_folium(m, width=700, height=500)
    
    # Map statistics
    st.subheader("REE Deposit Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Deposits", len(ree_deposits))
    with col2:
        st.metric("Active Mines", len([d for d in ree_deposits if d["type"] == "active_mine"]))
    with col3:
        st.metric("Prospects", len([d for d in ree_deposits if d["type"] == "prospect"]))
    with col4:
        st.metric("LREE Deposits", len([d for d in ree_deposits if "LREE" in d["elements"]]))
    
    # Additional information
    st.subheader("Key REE Deposits")
    st.info("""
    **Mountain Pass Mine** (California): The largest REE deposit in the United States, currently operated by MP Materials.
    
    **Halleck Creek** (Wyoming): Potentially the world's largest REE deposit with 2.34 billion metric tons of reserves.
    
    **Music Valley & Pinto Mountains** (California): Part of the 130km alkaline rock belt in the Southeast Mojave Desert.
    """)

with tab3:
    st.header("Data Analysis")
    
    # Sample data for analysis (in real implementation, use actual extracted data)
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
    
    # Sample analysis
    st.subheader("Sample Analysis")
    
    # Element correlation
    if len(df) > 1:
        correlation_data = df.pivot_table(
            index="Sample_ID", 
            columns="Element", 
            values="Value", 
            fill_value=0
        )
        
        if not correlation_data.empty:
            fig_corr = px.imshow(
                correlation_data.corr(),
                title="Element Correlation Matrix",
                color_continuous_scale="RdBu"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
    
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
    
    # Export configuration
    config_json = {
        "llm_provider": llm_provider,
        "llm_model": llm_model,
        "ocr_engine": ocr_engine,
        "language": language,
        "confidence_threshold": confidence_threshold,
        "pdf_dpi": pdf_dpi,
        "debug_mode": debug_mode,
        "output_format": output_format
    }
    
    config_str = json.dumps(config_json, indent=2)
    st.download_button(
        label="📥 Download Configuration",
        data=config_str,
        file_name="geoextract_config.json",
        mime="application/json"
    )
    
    # System information
    st.subheader("System Information")
    
    import sys
    import platform
    
    sys_info = {
        "Python Version": sys.version,
        "Platform": platform.platform(),
        "Streamlit Version": st.__version__,
        "Deployment": "Streamlit Cloud"
    }
    
    for key, value in sys_info.items():
        st.text(f"{key}: {value}")

# Footer
st.markdown("---")
st.markdown(
    "**GeoExtract** - Open-Source Geological Report Data Extraction System | "
    "Built with ❤️ using Python, Streamlit, and modern AI technologies | "
    "☁️ **Deployed on Streamlit Cloud**"
)

# Streamlit badge
st.markdown('<div class="streamlit-badge">Powered by Streamlit</div>', unsafe_allow_html=True)
