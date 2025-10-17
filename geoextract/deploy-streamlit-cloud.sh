#!/bin/bash

# GeoExtract Streamlit Cloud Deployment Script
echo "🚀 GeoExtract Streamlit Cloud Deployment"
echo "=========================================="

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
if [ ! -f "ui/streamlit_app.py" ]; then
    echo "❌ streamlit_app.py not found. Make sure you're in the geoextract directory."
    exit 1
fi

print_status "Found streamlit_app.py"

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_warning "Git not initialized. Initializing..."
    git init
    git add .
    git commit -m "Initial commit for Streamlit Cloud deployment"
fi

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    print_warning "No remote repository found. Please add your GitHub remote:"
    echo "git remote add origin https://github.com/yourusername/your-repo.git"
    echo "git push -u origin main"
    exit 1
fi

print_status "Git repository configured"

# Push to GitHub
print_info "Pushing to GitHub..."
git add .
git commit -m "Update for Streamlit Cloud deployment" || true
git push origin main

if [ $? -eq 0 ]; then
    print_status "Successfully pushed to GitHub!"
else
    print_warning "Failed to push to GitHub. Please check your git configuration."
    exit 1
fi

echo ""
print_info "🚀 Next Steps for Streamlit Cloud Deployment:"
echo ""
echo "1. Go to https://share.streamlit.io"
echo "2. Click 'New app'"
echo "3. Connect your GitHub account"
echo "4. Select your repository: $(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\/[^/]*\)\.git.*/\1/')"
echo "5. Select branch: main"
echo "6. Main file path: geoextract/ui/streamlit_app.py"
echo "7. Click 'Deploy!'"
echo ""
print_status "Your app will be available at: https://[app-name]-[hash].streamlit.app"
echo ""
print_info "Alternative: Use Railway or Heroku for deployment"
echo "See STREAMLIT_CLOUD_DEPLOYMENT.md for detailed instructions"

