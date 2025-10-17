# 🚀 Deploy GeoExtract to Vercel

## Quick Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy from Project Directory
```bash
cd /Users/zumot/Desktop/ree/geoextract
vercel
```

### 4. Follow the Prompts
- **Set up and deploy?** → Yes
- **Which scope?** → Your account
- **Link to existing project?** → No
- **Project name** → geoextract (or your preferred name)
- **Directory** → ./
- **Override settings?** → No

## Alternative: GitHub Integration

### 1. Push to GitHub (if not already done)
```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

### 2. Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import from GitHub repository
4. Select your geo-explore repository
5. Configure build settings:
   - **Framework Preset**: Other
   - **Root Directory**: geoextract
   - **Build Command**: `pip install -r requirements-vercel.txt`
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements-vercel.txt`

## Configuration Files Created

### ✅ Files Added for Vercel:
- `vercel.json` - Vercel configuration
- `requirements-vercel.txt` - Optimized dependencies
- `streamlit_app_vercel.py` - Vercel-optimized Streamlit app
- `api/index.py` - Serverless API function
- `package.json` - Node.js configuration

## Environment Variables (Optional)

Set these in Vercel dashboard under Project Settings → Environment Variables:

```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## Deployment Commands

### Deploy to Production
```bash
vercel --prod
```

### Deploy Preview
```bash
vercel
```

### Check Deployment Status
```bash
vercel ls
```

## Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check `requirements-vercel.txt` for missing dependencies
   - Ensure all imports are available
   - Check Vercel build logs

2. **Runtime Errors**
   - Verify Python version compatibility
   - Check environment variables
   - Review function logs in Vercel dashboard

3. **Import Errors**
   - Ensure all modules are in requirements-vercel.txt
   - Check file paths and imports
   - Verify package versions

### Debug Commands:
```bash
# Check deployment logs
vercel logs

# View function logs
vercel logs --follow

# Check build output
vercel build
```

## Expected Result

After successful deployment, you'll get:
- **Production URL**: `https://geoextract-[hash].vercel.app`
- **Preview URL**: `https://geoextract-git-[branch]-[hash].vercel.app`

## Features Available on Vercel

✅ **Streamlit Web Interface**
- Document processing interface
- Interactive mapping
- Data analysis tools
- Configuration options

✅ **Serverless API**
- FastAPI backend
- File upload handling
- Background processing
- RESTful endpoints

✅ **Scalable Infrastructure**
- Automatic scaling
- Global CDN
- HTTPS by default
- Zero-config deployments

## Next Steps

1. **Custom Domain** (Optional)
   - Add custom domain in Vercel dashboard
   - Configure DNS settings
   - Enable SSL certificate

2. **Environment Variables**
   - Add API keys for LLM providers
   - Configure database connections
   - Set up external services

3. **Monitoring**
   - Set up Vercel Analytics
   - Configure error tracking
   - Monitor performance metrics

## 🎉 Your GeoExtract app will be live at: `https://your-app.vercel.app`

