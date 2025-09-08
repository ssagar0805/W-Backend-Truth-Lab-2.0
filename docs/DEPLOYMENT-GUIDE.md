# 🌐 Truth Lab 2.0 - Production Deployment Guide

## 🎯 Deployment Overview

Truth Lab 2.0 is architected for **cloud-native deployment** with multiple platform options:

- **🥇 Primary**: Google Cloud Run (Recommended for FastAPI + React)
- **🔄 Alternative**: Vercel/Netlify (Frontend) + Railway/Render (Backend)
- **🐳 Enterprise**: Kubernetes (GKE, EKS, AKS)
- **🏠 Self-Hosted**: Docker Compose + Reverse Proxy

## 📋 Pre-Deployment Checklist

### ✅ Code Preparation
- [ ] All tests passing (`npm test`, `pytest`)
- [ ] Production build successful (`npm run build`)
- [ ] Environment variables configured
- [ ] API keys and secrets secured
- [ ] Database migrations completed
- [ ] Security audit completed
- [ ] Performance benchmarks met

### ✅ Infrastructure Requirements
- [ ] Domain name registered and configured
- [ ] SSL/TLS certificates ready
- [ ] CDN setup (optional but recommended)
- [ ] Monitoring and logging configured
- [ ] Backup and disaster recovery plan
- [ ] Load testing completed

---

## 🚀 Google Cloud Run Deployment (Recommended)

### 🎯 Why Google Cloud Run?
- **⚡ Serverless**: Auto-scaling, pay-per-use
- **🔒 Secure**: Built-in HTTPS, IAM integration
- **🌍 Global**: Multi-region deployment
- **🐳 Container-Based**: Docker-native deployment
- **💰 Cost-Effective**: Only pay for actual usage

### 📦 Prerequisites

```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth login
gcloud config set project your-project-id

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 🔧 Backend Deployment (FastAPI)

#### 1. Dockerfile for Backend
```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY .env ./

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### 2. Cloud Build Configuration
```yaml
# backend/cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/truth-lab-backend:$BUILD_ID', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/truth-lab-backend:$BUILD_ID']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args: [
      'run', 'deploy', 'truth-lab-backend',
      '--image', 'gcr.io/$PROJECT_ID/truth-lab-backend:$BUILD_ID',
      '--platform', 'managed',
      '--region', 'us-central1',
      '--allow-unauthenticated',
      '--port', '8080',
      '--memory', '2Gi',
      '--cpu', '1',
      '--min-instances', '0',
      '--max-instances', '10',
      '--set-env-vars', 'ENVIRONMENT=production'
    ]
```

#### 3. Deploy Backend
```bash
# Navigate to backend directory
cd backend

# Build and deploy
gcloud builds submit --config cloudbuild.yaml .

# Alternative: Direct deployment
gcloud run deploy truth-lab-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10

# Set environment variables
gcloud run services update truth-lab-backend \
  --set-env-vars="GOOGLE_API_KEY=$GOOGLE_API_KEY" \
  --set-env-vars="FIREBASE_PROJECT_ID=$FIREBASE_PROJECT_ID" \
  --set-env-vars="ENVIRONMENT=production" \
  --region us-central1
```

### 🎨 Frontend Deployment

#### 1. Build Frontend for Production
```bash
cd frontend

# Create production environment file
cat > .env.production << EOF
VITE_API_BASE_URL=https://truth-lab-backend-xxx-uc.a.run.app
VITE_APP_NAME=Truth Lab 2.0
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_DEBUG=false
EOF

# Build for production
npm run build

# Test production build locally
npm run preview
```

#### 2. Deploy to Google Cloud Storage + CDN
```bash
# Create storage bucket
gsutil mb gs://truth-lab-frontend

# Enable web hosting
gsutil web set -m index.html -e index.html gs://truth-lab-frontend

# Upload build files
gsutil -m rsync -r -d dist/ gs://truth-lab-frontend/

# Make files public
gsutil -m acl ch -r -u AllUsers:R gs://truth-lab-frontend

# Optional: Setup Cloud CDN
gcloud compute backend-buckets create truth-lab-frontend-backend \
  --gcs-bucket-name=truth-lab-frontend

# Create URL map
gcloud compute url-maps create truth-lab-frontend-map \
  --default-backend-bucket=truth-lab-frontend-backend
```

#### 3. Custom Domain & SSL
```bash
# Reserve static IP
gcloud compute addresses create truth-lab-ip --global

# Create SSL certificate
gcloud compute ssl-certificates create truth-lab-ssl \
  --domains=truthlab.example.com

# Create HTTPS load balancer
gcloud compute target-https-proxies create truth-lab-https-proxy \
  --url-map=truth-lab-frontend-map \
  --ssl-certificates=truth-lab-ssl

# Create forwarding rule
gcloud compute forwarding-rules create truth-lab-https-rule \
  --address=truth-lab-ip \
  --global \
  --target-https-proxy=truth-lab-https-proxy \
  --ports=443
```

---

## 🔄 Alternative Deployments

### 🌐 Vercel (Frontend) + Railway (Backend)

#### Frontend on Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Configure environment variables in Vercel dashboard
# VITE_API_BASE_URL=https://your-backend.railway.app
```

#### Backend on Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Navigate to backend directory
cd backend

# Initialize Railway project
railway init

# Deploy
railway up

# Set environment variables
railway variables set GOOGLE_API_KEY=your_api_key
railway variables set FIREBASE_PROJECT_ID=your_project_id
```

### ☁️ AWS Deployment

#### Frontend on AWS S3 + CloudFront
```bash
# Install AWS CLI
pip install awscli

# Configure AWS
aws configure

# Create S3 bucket
aws s3 mb s3://truth-lab-frontend

# Enable static web hosting
aws s3 website s3://truth-lab-frontend \
  --index-document index.html \
  --error-document index.html

# Upload files
aws s3 sync dist/ s3://truth-lab-frontend/ --delete

# Create CloudFront distribution
aws cloudfront create-distribution \
  --distribution-config file://cloudfront-config.json
```

#### Backend on AWS ECS Fargate
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name truth-lab-cluster

# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster truth-lab-cluster \
  --service-name truth-lab-backend \
  --task-definition truth-lab-backend:1 \
  --desired-count 2
```

---

## 🐳 Docker Compose Production

### 📝 Production Docker Compose
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8080"
    environment:
      - ENVIRONMENT=production
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - FIREBASE_PROJECT_ID=${FIREBASE_PROJECT_ID}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    
  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    restart: unless-stopped

  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command: --interval 300
    restart: unless-stopped
```

### 🔒 Nginx Configuration
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8080;
    }
    
    upstream frontend {
        server frontend:80;
    }
    
    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name truthlab.example.com;
        return 301 https://$server_name$request_uri;
    }
    
    # HTTPS Server
    server {
        listen 443 ssl http2;
        server_name truthlab.example.com;
        
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
        
        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Backend API
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # CORS headers
            add_header Access-Control-Allow-Origin *;
            add_header Access-Control-Allow-Methods "GET, POST, OPTIONS, PUT, DELETE";
            add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization";
        }
        
        # Health checks
        location /health {
            proxy_pass http://backend/health;
        }
    }
}
```

### 🚀 Deploy with Docker Compose
```bash
# Create production environment file
cp .env.example .env.prod

# Build and deploy
docker-compose -f docker-compose.prod.yml up --build -d

# Monitor logs
docker-compose -f docker-compose.prod.yml logs -f

# Update deployment
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔒 Security Configuration

### 🛡️ Environment Variables & Secrets

#### Production Environment Template
```bash
# .env.prod
# API Configuration
API_HOST=0.0.0.0
API_PORT=8080
ENVIRONMENT=production
DEBUG=false

# Security
SECRET_KEY=your_super_secure_secret_key_here_64_chars_minimum
ALLOWED_HOSTS=truthlab.example.com,api.truthlab.example.com
CORS_ORIGINS=https://truthlab.example.com

# Google AI
GOOGLE_API_KEY=your_production_google_api_key

# Firebase
FIREBASE_PROJECT_ID=truth-lab-production
FIREBASE_CREDENTIALS_PATH=/app/firebase-credentials.json

# Database
DATABASE_URL=postgresql://user:pass@host:5432/truthlab_prod

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=100
RATE_LIMIT_REQUESTS_PER_HOUR=1000
```

#### Secrets Management Best Practices
```bash
# Google Cloud Secret Manager
echo -n "your-secret-value" | gcloud secrets create google-api-key --data-file=-

# AWS Secrets Manager
aws secretsmanager create-secret \
  --name "truth-lab/google-api-key" \
  --secret-string "your-secret-value"

# Kubernetes Secrets
kubectl create secret generic truth-lab-secrets \
  --from-literal=google-api-key=your-secret-value \
  --from-literal=firebase-project-id=your-project-id
```

### 🔐 SSL/TLS Configuration

#### Let's Encrypt with Certbot
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d truthlab.example.com -d api.truthlab.example.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Certificate Monitoring
```bash
# Check certificate expiry
echo | openssl s_client -servername truthlab.example.com -connect truthlab.example.com:443 2>/dev/null | openssl x509 -noout -dates

# Automated certificate monitoring script
#!/bin/bash
DOMAIN="truthlab.example.com"
EXPIRY=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
EXPIRY_TIMESTAMP=$(date -d "$EXPIRY" +%s)
CURRENT_TIMESTAMP=$(date +%s)
DAYS_UNTIL_EXPIRY=$(( ($EXPIRY_TIMESTAMP - $CURRENT_TIMESTAMP) / 86400 ))

if [ $DAYS_UNTIL_EXPIRY -lt 30 ]; then
    echo "Certificate expires in $DAYS_UNTIL_EXPIRY days!"
    # Send alert notification
fi
```

---

## 📊 Monitoring & Observability

### 📈 Application Performance Monitoring

#### Google Cloud Monitoring
```bash
# Install monitoring agent
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install

# Configure custom metrics
gcloud logging metrics create truth_lab_errors \
  --description="Truth Lab API errors" \
  --log-filter='resource.type="cloud_run_revision" AND severity>=ERROR'
```

#### Sentry Integration
```python
# backend/src/config/monitoring.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        FastApiIntegration(auto_enabling_integrations=False),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=1.0,
    environment=os.getenv("ENVIRONMENT", "production"),
)
```

#### Custom Health Checks
```python
# backend/src/api/health.py
from fastapi import APIRouter, Depends
import asyncio
import aiohttp

router = APIRouter()

@router.get("/health/detailed")
async def detailed_health_check():
    checks = {
        "database": await check_database_connection(),
        "google_ai": await check_google_ai_api(),
        "firebase": await check_firebase_connection(),
        "external_apis": await check_external_services(),
    }
    
    overall_status = "healthy" if all(checks.values()) else "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
        "version": "2.0.0"
    }
```

### 📊 Log Management

#### Structured Logging Configuration
```python
# backend/src/utils/logging.py
import structlog
import logging.config

def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(30),  # INFO level
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Usage in application
logger = structlog.get_logger()
logger.info("Analysis completed", 
           user_id="12345", 
           analysis_time=1.2, 
           confidence_score=0.85)
```

#### Log Aggregation with ELK Stack
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    
  kibana:
    image: docker.elastic.co/kibana/kibana:8.8.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    
  logstash:
    image: docker.elastic.co/logstash/logstash:8.8.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    depends_on:
      - elasticsearch
```

---

## 🔧 CI/CD Pipeline

### 🚀 GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy Truth Lab 2.0

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PROJECT_ID: your-gcp-project-id
  SERVICE_NAME: truth-lab-backend
  REGION: us-central1

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pytest pytest-asyncio
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install frontend dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm test
    
    - name: Build frontend
      run: |
        cd frontend
        npm run build

  deploy-backend:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - id: 'auth'
      uses: 'google-github-actions/auth@v1'
      with:
        credentials_json: '${{ secrets.GCP_SA_KEY }}'
    
    - name: 'Set up Cloud SDK'
      uses: 'google-github-actions/setup-gcloud@v1'
    
    - name: Configure Docker
      run: gcloud auth configure-docker
    
    - name: Build and push Docker image
      run: |
        cd backend
        docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA .
        docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA
    
    - name: Deploy to Cloud Run
      run: |
        gcloud run deploy $SERVICE_NAME \
          --image gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA \
          --platform managed \
          --region $REGION \
          --allow-unauthenticated \
          --set-env-vars="ENVIRONMENT=production" \
          --set-env-vars="GOOGLE_API_KEY=${{ secrets.GOOGLE_API_KEY }}"

  deploy-frontend:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies and build
      run: |
        cd frontend
        npm ci
        npm run build
      env:
        VITE_API_BASE_URL: ${{ secrets.API_BASE_URL }}
    
    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v25
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.ORG_ID }}
        vercel-project-id: ${{ secrets.PROJECT_ID }}
        working-directory: ./frontend
```

### 🔄 Blue-Green Deployment Strategy
```bash
#!/bin/bash
# deploy-blue-green.sh

# Current service (Blue)
CURRENT_SERVICE="truth-lab-backend"
NEW_SERVICE="truth-lab-backend-green"

# Deploy new version (Green)
gcloud run deploy $NEW_SERVICE \
  --image gcr.io/$PROJECT_ID/truth-lab-backend:$BUILD_ID \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated \
  --tag green

# Health check on green deployment
GREEN_URL=$(gcloud run services describe $NEW_SERVICE --region=us-central1 --format="value(status.url)")
if curl -f "$GREEN_URL/health" > /dev/null 2>&1; then
    echo "Green deployment healthy, switching traffic..."
    
    # Switch 100% traffic to green
    gcloud run services update-traffic $NEW_SERVICE \
      --to-revisions green=100 \
      --region us-central1
    
    # Update DNS/Load Balancer to point to green
    # Clean up blue deployment after verification
    sleep 300  # Wait 5 minutes
    gcloud run services delete $CURRENT_SERVICE --region=us-central1 --quiet
    
    # Rename green to current
    gcloud run services replace-traffic $NEW_SERVICE \
      --to-latest --region us-central1
else
    echo "Green deployment failed health check, rolling back..."
    gcloud run services delete $NEW_SERVICE --region=us-central1 --quiet
    exit 1
fi
```

---

## 📊 Performance Optimization

### ⚡ Backend Performance
```python
# backend/src/config/performance.py
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvloop

# Use uvloop for better async performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await setup_connection_pools()
    await warm_up_ai_models()
    yield
    # Shutdown
    await cleanup_resources()

# Connection pooling
import aiohttp
import asyncpg

async def setup_connection_pools():
    # HTTP connection pool
    connector = aiohttp.TCPConnector(
        limit=100,
        limit_per_host=30,
        keepalive_timeout=30,
        enable_cleanup_closed=True
    )
    app.state.http_session = aiohttp.ClientSession(connector=connector)
    
    # Database connection pool
    app.state.db_pool = await asyncpg.create_pool(
        DATABASE_URL,
        min_size=10,
        max_size=20,
        command_timeout=60
    )
```

### 🎨 Frontend Performance
```javascript
// frontend/src/utils/performance.js
import { lazy, Suspense } from 'react';

// Code splitting for better performance
const Home = lazy(() => import('../pages/Home'));
const Archive = lazy(() => import('../pages/Archive'));
const Dashboard = lazy(() => import('../pages/Dashboard'));

// Performance monitoring
export const measurePerformance = (name, fn) => {
  return async (...args) => {
    const start = performance.now();
    const result = await fn(...args);
    const end = performance.now();
    
    // Send to analytics
    if (window.gtag) {
      window.gtag('event', 'timing_complete', {
        name: name,
        value: Math.round(end - start)
      });
    }
    
    return result;
  };
};

// Service Worker for caching
// public/sw.js
const CACHE_NAME = 'truth-lab-v2.0.0';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
  );
});
```

---

## 🆘 Troubleshooting & Rollback

### 🔧 Common Deployment Issues

#### Issue: Container Build Failures
```bash
# Debug build process
docker build --no-cache --progress=plain -t debug-image .

# Check build logs
gcloud builds log BUILD_ID

# Test locally first
docker run -p 8080:8080 debug-image
curl http://localhost:8080/health
```

#### Issue: Service Unreachable
```bash
# Check service status
gcloud run services describe truth-lab-backend --region=us-central1

# Check logs
gcloud logs read "resource.type=cloud_run_revision" --limit=50

# Test connectivity
gcloud run services proxy truth-lab-backend --port=8080
```

#### Issue: Environment Variables Not Loading
```bash
# List current environment variables
gcloud run services describe truth-lab-backend \
  --region=us-central1 \
  --format="value(spec.template.spec.template.spec.containers[0].env[].name,spec.template.spec.template.spec.containers[0].env[].value)"

# Update environment variables
gcloud run services update truth-lab-backend \
  --set-env-vars="KEY=VALUE" \
  --region=us-central1
```

### 🔄 Rollback Procedures

#### Quick Rollback to Previous Version
```bash
# List revisions
gcloud run revisions list --service=truth-lab-backend --region=us-central1

# Rollback to specific revision
gcloud run services update-traffic truth-lab-backend \
  --to-revisions=truth-lab-backend-00002-abc=100 \
  --region=us-central1

# Verify rollback
curl https://your-service-url.run.app/health
```

#### Database Rollback (if needed)
```bash
# Backup current state
pg_dump $DATABASE_URL > backup-$(date +%Y%m%d-%H%M%S).sql

# Restore from previous backup
psql $DATABASE_URL < backup-previous.sql

# Verify data integrity
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"
```

#### Frontend Rollback
```bash
# Vercel rollback
vercel rollback --token $VERCEL_TOKEN

# Manual S3 rollback
aws s3 sync s3://truth-lab-frontend-backup/ s3://truth-lab-frontend/ --delete

# CDN cache invalidation
aws cloudfront create-invalidation --distribution-id E123456789 --paths "/*"
```

---

## 📊 Post-Deployment Verification

### ✅ Automated Health Checks
```bash
#!/bin/bash
# post-deploy-verification.sh

BACKEND_URL="https://your-backend-url"
FRONTEND_URL="https://your-frontend-url"

# Backend health checks
echo "Checking backend health..."
curl -f "$BACKEND_URL/health" || exit 1
curl -f "$BACKEND_URL/api/status" || exit 1

# Frontend health checks
echo "Checking frontend..."
curl -f "$FRONTEND_URL" || exit 1

# API integration test
echo "Testing API integration..."
RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text":"Test message","language":"en","level":"Quick Scan"}')

if [[ $RESPONSE == *"confidence_score"* ]]; then
    echo "API integration test passed"
else
    echo "API integration test failed"
    exit 1
fi

echo "All health checks passed!"
```

### 📊 Performance Verification
```bash
#!/bin/bash
# performance-test.sh

# Load testing with Apache Bench
ab -n 1000 -c 10 https://your-backend-url/health

# Response time testing
curl -o /dev/null -s -w "Total time: %{time_total}s\n" https://your-frontend-url/

# Memory and CPU monitoring
docker stats --no-stream
```

---

**🎉 Deployment Complete!**

Your Truth Lab 2.0 is now live in production with:
- ✅ Scalable cloud infrastructure
- ✅ Automated CI/CD pipeline
- ✅ Comprehensive monitoring
- ✅ Security best practices
- ✅ Performance optimization
- ✅ Disaster recovery procedures

**🔗 Next Steps:**
- Monitor application performance and user feedback
- Set up alerts for critical metrics
- Plan regular security updates
- Scale infrastructure based on usage patterns

*Truth Lab 2.0 is ready to serve users globally with enterprise-grade reliability and performance! 🚀*