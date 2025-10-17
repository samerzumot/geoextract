#!/usr/bin/env python3
"""
Test script to verify GeoExtract setup and dependencies.
Run this script to check if everything is properly configured.
"""

import sys
import subprocess
import importlib
from pathlib import Path

def test_python_version():
    """Test Python version."""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.8+")
        return False

def test_imports():
    """Test if required packages can be imported."""
    print("\n📦 Testing package imports...")
    
    packages = [
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('plotly', 'Plotly'),
        ('folium', 'Folium'),
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pydantic', 'Pydantic')
    ]
    
    all_ok = True
    for package, name in packages:
        try:
            importlib.import_module(package)
            print(f"✅ {name} - OK")
        except ImportError:
            print(f"❌ {name} - Missing")
            all_ok = False
    
    return all_ok

def test_streamlit_app():
    """Test if the Streamlit app file exists and is readable."""
    print("\n📄 Testing Streamlit app file...")
    
    app_path = Path("ui/streamlit_app.py")
    if app_path.exists():
        print("✅ streamlit_app.py found")
        try:
            with open(app_path, 'r') as f:
                content = f.read()
                if 'streamlit' in content.lower():
                    print("✅ Streamlit app content looks good")
                    return True
                else:
                    print("❌ Streamlit app content seems invalid")
                    return False
        except Exception as e:
            print(f"❌ Error reading streamlit_app.py: {e}")
            return False
    else:
        print("❌ streamlit_app.py not found")
        return False

def test_port_availability():
    """Test if port 8501 is available."""
    print("\n🔌 Testing port availability...")
    
    import socket
    
    def is_port_available(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return True
            except OSError:
                return False
    
    if is_port_available(8501):
        print("✅ Port 8501 is available")
        return True
    else:
        print("❌ Port 8501 is in use")
        print("💡 Try using port 8502 instead")
        return False

def main():
    """Main test function."""
    print("🧪 GeoExtract Setup Test")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_imports,
        test_streamlit_app,
        test_port_availability
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    if all(results):
        print("✅ All tests passed! You're ready to run the web app.")
        print("\n🚀 To start the application, run:")
        print("   streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0")
        print("\n🌐 Then open: http://localhost:8501")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   - Install missing packages: pip install streamlit pandas plotly folium")
        print("   - Use a different port: --server.port 8502")
        print("   - Check Python version: python --version")

if __name__ == "__main__":
    main()
