# 🚀 GeoExtract Deployment Guide

## Quick Start (Local Development)

### Option 1: Using the Deployment Script
```bash
cd /Users/zumot/Desktop/ree/geoextract
./deploy.sh
```

### Option 2: Manual Start
```bash
cd /Users/zumot/Desktop/ree/geoextract
python3 -m streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Option 3: Using Python Script
```bash
cd /Users/zumot/Desktop/ree/geoextract
python3 run_webapp.py
```

## 🌐 Access the Application
- **Local**: http://localhost:8501
- **Network**: http://0.0.0.0:8501

## 🐳 Docker Deployment

### Build and Run with Docker
```bash
# Build the Docker image
docker build -t geoextract .

# Run the container
docker run -p 8501:8501 -v $(pwd)/output:/app/output geoextract
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment Options

### 1. Heroku Deployment
```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run ui/streamlit_app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create geoextract-app
git push heroku main
```

### 2. Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 3. Streamlit Cloud
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Deploy automatically

## 🔧 Production Configuration

### Environment Variables
```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### Nginx Configuration (Production)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 📊 Monitoring and Health Checks

### Health Check Endpoint
```bash
curl http://localhost:8501/_stcore/health
```

### Process Monitoring
```bash
# Check if running
ps aux | grep streamlit

# Check port usage
lsof -i :8501

# View logs
tail -f logs/geoextract.log
```

## 🛠️ Troubleshooting

### Common Issues:

1. **Port Already in Use**
   ```bash
   # Find process using port
   lsof -i :8501
   # Kill process
   kill -9 <PID>
   ```

2. **Python/Package Issues**
   ```bash
   # Check Python version
   python3 --version
   
   # Reinstall packages
   pip3 install -r requirements.txt --force-reinstall
   ```

3. **Permission Issues**
   ```bash
   # Make scripts executable
   chmod +x deploy.sh
   chmod +x start_webapp.sh
   ```

4. **Memory Issues**
   ```bash
   # Check memory usage
   top -p $(pgrep streamlit)
   
   # Restart if needed
   pkill streamlit && ./deploy.sh
   ```

## 🔒 Security Considerations

### Production Security:
- Use HTTPS in production
- Configure firewall rules
- Set up authentication if needed
- Monitor resource usage
- Regular security updates

### Environment Isolation:
```bash
# Create virtual environment
python3 -m venv geoextract_env
source geoextract_env/bin/activate
pip install -r requirements.txt
```

## 📈 Scaling Options

### Horizontal Scaling:
- Use load balancer (nginx/HAProxy)
- Multiple Streamlit instances
- Session storage (Redis)
- Database for state management

### Vertical Scaling:
- Increase server resources
- Optimize Python performance
- Use faster storage (SSD)
- Monitor and tune parameters

## 🚀 Current Status

✅ **Application is currently running at: http://localhost:8501**

The GeoExtract web application is deployed and accessible with all features:
- Document processing interface
- Interactive mapping
- Data analysis tools
- Configuration options
