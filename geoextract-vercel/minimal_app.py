"""
GeoExtract - Minimal Version for Vercel
"""

import streamlit as st
import pandas as pd
import json

# Configure page
st.set_page_config(
    page_title="GeoExtract",
    page_icon="🗺️",
    layout="wide"
)

# Title
st.title("🗺️ GeoExtract")
st.subtitle("Geological Report Data Extraction System")
st.markdown("🚀 **Deployed on Vercel**")

# Sidebar
st.sidebar.title("Configuration")
llm_provider = st.sidebar.selectbox("LLM Provider", ["ollama", "openai", "anthropic"])
ocr_engine = st.sidebar.selectbox("OCR Engine", ["paddle", "tesseract", "both"])

# Main content
tab1, tab2, tab3 = st.tabs(["📄 Upload & Process", "🗺️ Map View", "📊 Data Analysis"])

with tab1:
    st.header("Document Processing")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")
        
        if st.button("🚀 Process Documents", type="primary"):
            with st.spinner("Processing documents..."):
                # Simulate processing
                results = []
                for uploaded_file in uploaded_files:
                    result = {
                        "filename": uploaded_file.name,
                        "status": "success",
                        "locations": 5,
                        "samples": 12,
                        "observations": 3,
                        "confidence": 0.85
                    }
                    results.append(result)
                
                # Display results
                st.subheader("Processing Results")
                df_results = pd.DataFrame(results)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Files", len(results))
                with col2:
                    st.metric("Total Locations", df_results["locations"].sum())
                with col3:
                    st.metric("Total Samples", df_results["samples"].sum())
                with col4:
                    st.metric("Avg Confidence", f"{df_results['confidence'].mean():.2f}")
                
                st.dataframe(df_results)
                
                # Download GeoJSON
                geojson_data = {
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
                
                geojson_str = json.dumps(geojson_data, indent=2)
                st.download_button(
                    label="📥 Download GeoJSON",
                    data=geojson_str,
                    file_name="extracted_data.geojson",
                    mime="application/json"
                )

with tab2:
    st.header("Interactive Map")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        map_center_lat = st.number_input("Center Latitude", value=37.7749, step=0.1)
        map_center_lon = st.number_input("Center Longitude", value=-122.4194, step=0.1)
        map_zoom = st.slider("Zoom Level", min_value=1, max_value=20, value=10)
    
    with col1:
        # Simple map visualization
        st.map({
            "lat": [37.7749, 37.7849, 37.7649],
            "lon": [-122.4194, -122.4094, -122.4294]
        })
    
    st.subheader("Map Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Locations", 3)
    with col2:
        st.metric("Drill Holes", 1)
    with col3:
        st.metric("Sample Sites", 2)

with tab3:
    st.header("Data Analysis")
    
    sample_data = {
        "Element": ["Au", "Ag", "Cu", "Pb", "Zn", "Fe"],
        "Value": [2.5, 15.3, 0.8, 1.2, 3.4, 45.2],
        "Unit": ["g/t", "g/t", "%", "%", "%", "%"],
        "Sample_ID": ["S001", "S001", "S002", "S002", "S003", "S003"]
    }
    
    df = pd.DataFrame(sample_data)
    
    st.subheader("Element Distribution")
    st.bar_chart(df.set_index('Element')['Value'])
    
    st.subheader("Raw Data")
    st.dataframe(df)

# Footer
st.markdown("---")
st.markdown(
    "**GeoExtract** - Open-Source Geological Report Data Extraction System | "
    "Built with ❤️ using Python, Streamlit, and modern AI technologies | "
    "🚀 **Deployed on Vercel**"
)
