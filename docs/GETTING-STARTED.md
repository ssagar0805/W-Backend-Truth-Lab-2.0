# 🚀 Truth Lab 2.0 - Getting Started Guide

## 📋 Quick Start Checklist

✅ **Prerequisites Setup** (15 minutes)  
✅ **Project Installation** (10 minutes)  
✅ **Environment Configuration** (5 minutes)  
✅ **Development Server Launch** (5 minutes)  
✅ **Verification & Testing** (10 minutes)  

**⏱️ Total Setup Time: ~45 minutes**

---

## 🛠️ Prerequisites & System Requirements

### 💻 Required Software

#### 🎯 Core Development Tools
```bash
# Node.js (v18+ Required)
node --version  # Should be v18.0.0 or higher
npm --version   # Should be v8.0.0 or higher

# Python (v3.9+ Required) 
python --version  # Should be v3.9.0 or higher
pip --version     # Should be v21.0.0 or higher

# Git (Latest Stable)
git --version     # Any recent version

# Docker (Optional but Recommended)
docker --version        # v20.0.0 or higher
docker-compose --version # v2.0.0 or higher
```

#### 📱 Development Environment
- **💻 OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **🧠 RAM**: 8GB minimum, 16GB recommended
- **💾 Storage**: 5GB free space for project and dependencies
- **🌐 Internet**: Stable connection for API services and package downloads

### 🔧 Recommended Tools & Extensions

#### 📝 Code Editor (VS Code Recommended)
```bash
# Essential Extensions
- Python Extension Pack
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Prettier - Code formatter
- ESLint
- GitLens
- Docker (if using containers)
```

#### 🔍 Browser Development Tools
- **Chrome DevTools** or **Firefox Developer Edition**
- **React Developer Tools** browser extension
- **Redux DevTools** browser extension (if using Redux)

---

## 📦 Project Installation

### 🎯 Method 1: Clone from Repository (Recommended)

```bash
# 1. Clone the Repository
git clone https://github.com/your-username/truth-lab-2.0.git
cd truth-lab-2.0

# 2. Verify Project Structure
ls -la
# Should see: backend/ frontend/ docs/ docker-compose.yml README.md etc.

# 3. Create Main Environment File
cp .env.example .env
```

### 🏗️ Method 2: Manual Setup (If Repository Not Available)

```bash
# 1. Create Project Directory
mkdir truth-lab-2.0
cd truth-lab-2.0

# 2. Initialize Git Repository
git init
echo "# Truth Lab 2.0" > README.md

# 3. Create Basic Structure
mkdir -p backend/src frontend/src docs docker
mkdir -p backend/src/{api,analysis_engine,models,services,utils,config}
mkdir -p frontend/src/{components,pages,styles,services,utils}
```

---

## 🔧 Backend Setup (FastAPI + Python)

### 📦 Install Python Dependencies

```bash
# Navigate to Backend Directory
cd backend

# Create Virtual Environment (Recommended)
python -m venv venv

# Activate Virtual Environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install Dependencies
pip install -r requirements.txt

# If requirements.txt doesn't exist, install core packages:
pip install fastapi uvicorn python-multipart python-dotenv
pip install google-generativeai pydantic firebase-admin
pip install pytest pytest-asyncio httpx
```

### ⚙️ Backend Environment Configuration

```bash
# Create Backend Environment File
cp .env.example .env

# Edit .env file with your configurations
nano .env  # or use your preferred editor
```

**📝 Backend .env Template:**
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
API_RELOAD=true

# Google AI Configuration
GOOGLE_API_KEY=your_google_gemini_api_key_here
GOOGLE_MODEL_NAME=gemini-1.5-flash

# Database Configuration (Firebase)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_CREDENTIALS_PATH=path/to/firebase-credentials.json

# Security Configuration
SECRET_KEY=your_super_secret_key_here_change_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/truth_lab.log
```

### 🔑 API Keys & Credentials Setup

#### 🤖 Google Gemini AI API Key
```bash
# 1. Visit Google AI Studio
# https://aistudio.google.com/app/apikey

# 2. Create New API Key
# - Click "Create API Key"
# - Select your Google Cloud Project
# - Copy the generated key

# 3. Add to Environment
echo "GOOGLE_API_KEY=your_actual_api_key_here" >> .env
```

#### 🔥 Firebase Setup (Optional - for Data Persistence)
```bash
# 1. Go to Firebase Console
# https://console.firebase.google.com/

# 2. Create New Project or Select Existing
# - Project Name: "truth-lab-2-0"
# - Enable Google Analytics (Optional)

# 3. Generate Service Account Key
# - Project Settings → Service Accounts
# - Generate new private key (JSON)
# - Download and save as firebase-credentials.json

# 4. Update Environment
echo "FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json" >> .env
echo "FIREBASE_PROJECT_ID=your_project_id" >> .env
```

### ✅ Verify Backend Installation

```bash
# Test Python Installation
python --version
python -c "import fastapi; print('FastAPI installed successfully')"
python -c "import google.generativeai; print('Google AI installed successfully')"

# Test Environment Loading
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(f'API Host: {os.getenv(\"API_HOST\", \"Not set\")}')
print(f'Google API Key: {\"Set\" if os.getenv(\"GOOGLE_API_KEY\") else \"Not set\"}')
"
```

---

## 🎨 Frontend Setup (React 18 + Vite)

### 📦 Install Node.js Dependencies

```bash
# Navigate to Frontend Directory
cd ../frontend

# Install Dependencies
npm install

# If package.json doesn't exist, initialize and install:
npm init -y
npm install react react-dom react-router-dom
npm install @vitejs/plugin-react vite
npm install tailwindcss @tailwindcss/forms @tailwindcss/typography
npm install framer-motion lucide-react
npm install axios date-fns
npm install --save-dev @types/react @types/react-dom
npm install --save-dev eslint eslint-plugin-react eslint-plugin-react-hooks
npm install --save-dev prettier eslint-config-prettier
```

### ⚙️ Frontend Environment Configuration

```bash
# Create Frontend Environment File
cp .env.example .env.local

# Edit environment file
nano .env.local
```

**📝 Frontend .env.local Template:**
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Application Configuration
VITE_APP_NAME=Truth Lab 2.0
VITE_APP_VERSION=2.0.0
VITE_APP_DESCRIPTION=AI-Powered Misinformation Detection Platform

# Feature Flags
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG=true
VITE_ENABLE_AUTH=true

# Authentication Configuration
VITE_AUTH_REDIRECT_URL=http://localhost:3000/auth/callback
VITE_SESSION_TIMEOUT=1800000

# UI Configuration
VITE_THEME_PRIMARY=#3B82F6
VITE_THEME_SECONDARY=#8B5CF6
VITE_ANIMATION_DURATION=300
```

### 🎨 Configure Tailwind CSS

```bash
# Initialize Tailwind Configuration
npx tailwindcss init -p

# Update tailwind.config.js
```

**📝 tailwind.config.js:**
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          50: '#f5f3ff',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
        }
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-slow': 'pulse 2s infinite',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### ⚡ Configure Vite

```bash
# Update vite.config.js
```

**📝 vite.config.js:**
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@services': path.resolve(__dirname, './src/services'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@styles': path.resolve(__dirname, './src/styles'),
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          ui: ['framer-motion', 'lucide-react'],
          utils: ['axios', 'date-fns'],
        }
      }
    }
  }
})
```

### ✅ Verify Frontend Installation

```bash
# Test Node.js Installation
node --version
npm --version

# Test Package Installation
npm list react react-dom react-router-dom
npm list vite tailwindcss framer-motion

# Test Build System
npm run build
# Should create dist/ directory without errors

# Clean up test build
rm -rf dist
```

---

## 🚀 Development Server Launch

### 🔧 Start Backend Server

```bash
# Navigate to Backend Directory
cd backend

# Activate Virtual Environment (if not already active)
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Start FastAPI Development Server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# Alternative: Using Python directly
python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

# You should see:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Started server process
```

### 🎨 Start Frontend Server

```bash
# Open New Terminal Window/Tab
# Navigate to Frontend Directory
cd frontend

# Start Vite Development Server
npm run dev

# Alternative commands:
npm start              # If configured in package.json
npx vite              # Direct Vite command
npx vite --host       # Expose on network

# You should see:
# ➜  Local:   http://localhost:3000/
# ➜  Network: http://192.168.1.100:3000/
# ➜  ready in 1ms
```

### 🐳 Docker Development (Alternative Method)

```bash
# Navigate to Project Root
cd ../

# Start All Services with Docker Compose
docker-compose up --build

# Start in Background
docker-compose up -d --build

# View Logs
docker-compose logs -f

# Stop Services
docker-compose down
```

---

## ✅ Verification & Testing

### 🔍 Backend API Testing

```bash
# Test Health Check Endpoint
curl http://localhost:8000/health
# Expected: {"status":"healthy","timestamp":"..."}

# Test API Status
curl http://localhost:8000/api/status
# Expected: {"api_version":"2.0.0","status":"operational"}

# Test Analysis Endpoint (POST request)
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"This is a test message","language":"en","level":"Quick Scan"}'

# View API Documentation
# Open browser: http://localhost:8000/docs
```

### 🎨 Frontend Application Testing

```bash
# Open Frontend in Browser
# http://localhost:3000

# Test Key Pages:
# - Home Page: Should load with analysis interface
# - Navigation: Header menu should work
# - Responsive: Test mobile view (DevTools)
# - API Integration: Try submitting test analysis
```

### 🧪 Integration Testing

```bash
# Test Frontend → Backend Communication
# 1. Open browser developer console (F12)
# 2. Navigate to Truth Lab 2.0 home page
# 3. Enter test text in analysis form
# 4. Submit analysis request
# 5. Check Network tab for successful API calls
# 6. Verify results display correctly
```

### 📊 Performance Testing

```bash
# Backend Performance
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Frontend Performance
# Use Chrome DevTools → Lighthouse
# Run performance audit on localhost:3000
```

---

## 🛠️ Common Setup Issues & Solutions

### 🔧 Backend Issues

#### ❌ ImportError: No module named 'fastapi'
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install fastapi uvicorn
```

#### ❌ Google API Authentication Error
```bash
# Solution: Verify API key in .env file
cat .env | grep GOOGLE_API_KEY
# Test API key validity:
python -c "
import google.generativeai as genai
genai.configure(api_key='YOUR_API_KEY')
print('API key is valid')
"
```

#### ❌ Port 8000 Already in Use
```bash
# Solution: Kill existing process or use different port
lsof -ti:8000 | xargs kill -9  # Kill process on port 8000
# Or use different port:
uvicorn src.api.main:app --port 8001 --reload
```

### 🎨 Frontend Issues

#### ❌ Node.js Version Compatibility
```bash
# Solution: Update Node.js to v18+
# Using nvm (recommended):
nvm install 18
nvm use 18

# Verify:
node --version  # Should show v18.x.x
```

#### ❌ Package Installation Failures
```bash
# Solution: Clear cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### ❌ Tailwind CSS Not Working
```bash
# Solution: Ensure proper configuration
# 1. Check tailwind.config.js content paths
# 2. Verify @tailwind directives in CSS file
# 3. Restart development server
npm run dev
```

### 🐳 Docker Issues

#### ❌ Docker Build Failures
```bash
# Solution: Clean Docker cache
docker system prune -a
docker-compose build --no-cache

# Check Docker resources:
docker system df
```

#### ❌ Port Conflicts in Docker
```bash
# Solution: Modify docker-compose.yml ports
# Change from 8000:8000 to 8001:8000 if needed
```

---

## 🎯 Next Steps

### 📚 Recommended Learning Path

1. **📖 Read Documentation**
   - [Architecture Guide](FILE-STRUCTURE.md)
   - [Development Workflow](WORKFLOW.md)
   - [User Guide](USER-GUIDE.md)

2. **🧪 Explore Codebase**
   - Backend API endpoints in `backend/src/api/`
   - React components in `frontend/src/components/`
   - Analysis engine in `backend/src/analysis_engine/`

3. **🛠️ Make First Changes**
   - Customize UI colors in Tailwind config
   - Add new API endpoint in backend
   - Create new React component

4. **📊 Test & Deploy**
   - Run test suite: `npm test`
   - Build production version: `npm run build`
   - Deploy to cloud platform

### 🤝 Getting Help

- **📚 Documentation**: Check all docs/ files for detailed guides
- **🐛 Issues**: Report bugs via GitHub issues
- **💬 Discussions**: Join community discussions
- **📧 Support**: Contact development team

### 🚀 Development Workflow

```bash
# Daily Development Routine:
1. git pull origin main          # Get latest changes
2. source venv/bin/activate      # Activate Python environment
3. cd backend && uvicorn src.api.main:app --reload  # Start backend
4. cd ../frontend && npm run dev # Start frontend
5. # Make your changes
6. npm test                      # Run tests
7. git add . && git commit -m "Description"  # Commit changes
8. git push origin feature-branch  # Push to feature branch
```

---

**🎉 Congratulations!** You now have Truth Lab 2.0 running locally with:
- ✅ FastAPI backend serving AI-powered analysis
- ✅ React frontend with modern UI/UX
- ✅ Complete development environment
- ✅ Integration between frontend and backend
- ✅ Ready for feature development and testing

**🔗 Next Documentation:**
- [Developer Guide](DEVELOPER-GUIDE.md) - Deep technical implementation details
- [User Guide](USER-GUIDE.md) - How to use the platform effectively
- [Deployment Guide](DEPLOYMENT-GUIDE.md) - Production deployment instructions

*Ready to build the future of misinformation detection! 🚀*