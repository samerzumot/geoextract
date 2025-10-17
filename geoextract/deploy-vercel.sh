#!/bin/bash

# GeoExtract Vercel Deployment Script
echo "🚀 GeoExtract Vercel Deployment"
echo "==============================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found. Make sure you're in the geoextract directory."
    exit 1
fi

print_status "Found Vercel configuration files"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    print_warning "Vercel CLI not found. Installing..."
    npm install -g vercel
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Vercel CLI. Please install manually: npm install -g vercel"
        exit 1
    fi
fi

print_status "Vercel CLI is available"

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    print_warning "Not logged in to Vercel. Please login:"
    vercel login
fi

print_status "Logged in to Vercel"

# Deploy to Vercel
print_info "Deploying to Vercel..."
echo ""

# Deploy with production flag
vercel --prod

if [ $? -eq 0 ]; then
    print_status "Deployment successful!"
    echo ""
    echo "🌐 Your GeoExtract app is now live on Vercel!"
    echo "📱 Check your Vercel dashboard for the deployment URL"
    echo "🔗 https://vercel.com/dashboard"
else
    echo "❌ Deployment failed. Check the error messages above."
    exit 1
fi

