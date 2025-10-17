#!/bin/bash

# GeoExtract New Repository Setup Script
echo "🚀 Setting up new GitHub repository for GeoExtract"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "geoextract/streamlit_app.py" ]; then
    echo "❌ streamlit_app.py not found. Make sure you're in the right directory."
    exit 1
fi

print_status "Found GeoExtract application files"

# Instructions for creating new repository
echo ""
print_info "STEP 1: Create a new repository on GitHub"
echo "1. Go to https://github.com/new"
echo "2. Repository name: geoextract"
echo "3. Description: Open-Source Geological Report Data Extraction System"
echo "4. Make it Public"
echo "5. DO NOT initialize with README, .gitignore, or license"
echo "6. Click 'Create repository'"
echo ""

print_warning "After creating the repository, GitHub will show you the commands to push."
print_warning "Use the HTTPS URL (not SSH) for easier authentication."
echo ""

print_info "STEP 2: Once you have the repository URL, run these commands:"
echo ""
echo "# Set the new remote URL (replace with your actual URL):"
echo "git remote set-url origin https://github.com/YOUR_USERNAME/geoextract.git"
echo ""
echo "# Push to the new repository:"
echo "git push -u origin main"
echo ""

print_info "STEP 3: Deploy to Streamlit Cloud"
echo "1. Go to https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Repository: YOUR_USERNAME/geoextract"
echo "5. Branch: main"
echo "6. Main file path: geoextract/streamlit_app.py"
echo "7. App URL: geoextract"
echo "8. Click 'Deploy!'"
echo ""

print_status "Your GeoExtract app will be live at: https://geoextract.streamlit.app"
