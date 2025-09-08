# 📁 Truth Lab 2.0 - File Structure & Architecture Guide

## 🏗️ Project Architecture Overview

Truth Lab 2.0 follows a modern **microservices architecture** with clear separation of concerns:

```
📦 Truth Lab 2.0 Architecture
├── 🔧 Backend (FastAPI + Python) - API Services & Analysis Engine
├── 🎨 Frontend (React 18 + Vite) - User Interface & Experience
├── 📚 Documentation - Comprehensive Guides & References
├── 🐳 Docker - Containerization & Deployment
└── ⚙️ Configuration - Environment & Setup Files
```

## 📂 Complete Directory Structure

```
webapp/
├── 📋 MASTER-README.md               # Project Root Documentation
├── 📄 package.json                  # Node.js Dependencies & Scripts
├── 🐳 docker-compose.yml           # Multi-Container Development
├── 🔧 Dockerfile                   # Production Container Build
├── ⚙️ .env.example                 # Environment Variables Template
├── 📝 .gitignore                   # Git Ignore Configuration
├── 🔍 .eslintrc.js                 # Frontend Code Quality Rules
├── 🎨 tailwind.config.js           # Styling Configuration
├── ⚡ vite.config.js               # Frontend Build Configuration
│
├── 🔧 backend/                      # FastAPI Python Backend
│   ├── 📋 README.md                # Backend Specific Documentation
│   ├── 📄 requirements.txt         # Python Dependencies
│   ├── 🐳 Dockerfile              # Backend Container Configuration
│   ├── ⚙️ .env.example            # Backend Environment Variables
│   │
│   ├── 🚀 src/                     # Source Code Directory
│   │   ├── 🌐 api/                 # API Layer - HTTP Endpoints
│   │   │   ├── 🎯 main.py          # FastAPI Application Entry Point
│   │   │   ├── 📊 health.py        # System Health & Status Endpoints
│   │   │   ├── 🔍 analyze.py       # Text Analysis API Routes
│   │   │   ├── 📎 upload.py        # File Upload & Processing Routes
│   │   │   ├── 📋 report.py        # Report Generation & Export Routes
│   │   │   └── 📚 archive.py       # Analysis History & Archive Routes
│   │   │
│   │   ├── 🧠 analysis_engine/     # Core Analysis Logic
│   │   │   ├── 🎯 __init__.py      # Module Initialization
│   │   │   ├── 🔬 comprehensive_analysis.py  # Main Analysis Orchestrator
│   │   │   ├── 📝 text_analysis.py # Text Processing & AI Integration
│   │   │   ├── 🕵️ source_tracking.py # Origin Tracing & Source Analysis
│   │   │   ├── 🧩 tactics_breakdown.py # Manipulation Pattern Detection
│   │   │   ├── 🔒 safety_checker.py # Content Safety & Filtering
│   │   │   ├── 🌍 context_analyzer.py # Context & Background Analysis
│   │   │   └── 📊 scoring_system.py # Credibility Scoring Algorithm
│   │   │
│   │   ├── 📦 models/              # Data Models & Schemas
│   │   │   ├── 🎯 __init__.py      # Models Module Initialization
│   │   │   ├── 🔍 analysis_models.py # Analysis Request/Response Models
│   │   │   ├── 👤 user_models.py   # User Authentication & Profile Models
│   │   │   ├── 📋 report_models.py # Report & Export Data Models
│   │   │   └── ⚙️ config_models.py # Configuration & Settings Models
│   │   │
│   │   ├── 🔧 services/            # Business Logic Services
│   │   │   ├── 🎯 __init__.py      # Services Module Initialization
│   │   │   ├── 🤖 ai_service.py    # Google Gemini AI Integration
│   │   │   ├── 🔐 auth_service.py  # Authentication & Authorization
│   │   │   ├── 💾 database_service.py # Database Operations & Queries
│   │   │   ├── 📁 file_service.py  # File Upload & Management
│   │   │   └── 📧 notification_service.py # Email & Alert Services
│   │   │
│   │   ├── 🛠️ utils/               # Utility Functions & Helpers
│   │   │   ├── 🎯 __init__.py      # Utils Module Initialization
│   │   │   ├── 🔍 validators.py    # Input Validation & Sanitization
│   │   │   ├── 🛡️ security.py     # Security Utilities & Encryption
│   │   │   ├── 📊 formatters.py    # Data Formatting & Transformation
│   │   │   ├── ⏰ date_utils.py    # Date/Time Processing Utilities
│   │   │   └── 📝 logging.py       # Logging Configuration & Utilities
│   │   │
│   │   └── ⚙️ config/              # Configuration Management
│   │       ├── 🎯 __init__.py      # Config Module Initialization
│   │       ├── ⚙️ settings.py      # Application Settings & Environment
│   │       ├── 💾 database.py      # Database Connection & Configuration
│   │       └── 🔑 secrets.py       # API Keys & Sensitive Configuration
│   │
│   └── 🧪 tests/                   # Backend Testing Suite
│       ├── 🎯 __init__.py          # Tests Module Initialization
│       ├── ⚙️ conftest.py          # PyTest Configuration & Fixtures
│       ├── 🔍 test_analysis.py     # Analysis Engine Unit Tests
│       ├── 🌐 test_api.py          # API Endpoints Integration Tests
│       ├── 🔧 test_services.py     # Business Logic Service Tests
│       └── 🛠️ test_utils.py        # Utility Functions Unit Tests
│
├── 🎨 frontend/                    # React 18 Frontend Application
│   ├── 📋 README.md               # Frontend Specific Documentation
│   ├── 📄 package.json            # Frontend Dependencies & Scripts
│   ├── 🐳 Dockerfile              # Frontend Container Configuration
│   ├── ⚙️ .env.example            # Frontend Environment Variables
│   │
│   ├── 🚀 src/                     # React Source Code
│   │   ├── 🎯 App.jsx              # Main Application Component & Router
│   │   ├── 🎨 index.css            # Global Styles & Tailwind Imports
│   │   ├── 🚀 main.jsx             # React Application Entry Point
│   │   │
│   │   ├── 🧩 components/          # Reusable UI Components
│   │   │   ├── 🎯 index.js         # Component Exports Hub
│   │   │   ├── 🧭 Header.jsx       # Top Navigation Header
│   │   │   ├── 🦶 Footer.jsx       # Site Footer Component
│   │   │   ├── 📝 InputTabs.jsx    # Analysis Input Interface
│   │   │   ├── 📊 ResultsDisplay.jsx # Analysis Results Visualization
│   │   │   ├── 📈 StatsHeader.jsx  # Statistics & Metrics Display
│   │   │   ├── 🔐 AuthModal.jsx    # Authentication Modal Dialog
│   │   │   ├── ⚡ LoadingSpinner.jsx # Loading State Component
│   │   │   ├── 🚨 ErrorBoundary.jsx # Error Handling Component
│   │   │   ├── 🎛️ ControlPanel.jsx # Authority User Controls
│   │   │   └── 📱 MobileMenu.jsx   # Responsive Mobile Navigation
│   │   │
│   │   ├── 📄 pages/               # Main Application Pages
│   │   │   ├── 🎯 index.js         # Page Exports Hub
│   │   │   ├── 🏠 Home.jsx         # Main Analysis Interface
│   │   │   ├── 📚 Archive.jsx      # Analysis History & Archives
│   │   │   ├── 🎓 Learn.jsx        # Educational Resources & Guides
│   │   │   ├── 📊 Dashboard.jsx    # Authority User Dashboard
│   │   │   ├── ⚙️ Settings.jsx     # User Preferences & Configuration
│   │   │   └── ❓ About.jsx        # Platform Information & Mission
│   │   │
│   │   ├── 🎨 styles/              # Styling & Design System
│   │   │   ├── 🎯 index.js         # Style Exports Hub
│   │   │   ├── 🌈 colors.js        # Color Palette & Theme Variables
│   │   │   ├── ✨ animations.js    # Framer Motion Animation Configs
│   │   │   ├── 📱 responsive.js    # Breakpoint & Media Query Configs
│   │   │   └── 🎨 components.js    # Styled Component Definitions
│   │   │
│   │   ├── 🔧 services/            # Frontend Service Layer
│   │   │   ├── 🎯 index.js         # Service Exports Hub
│   │   │   ├── 🌐 api.js           # API Client & HTTP Requests
│   │   │   ├── 🔐 auth.js          # Authentication Service
│   │   │   ├── 💾 storage.js       # Local Storage Management
│   │   │   └── 📊 analytics.js     # User Analytics & Tracking
│   │   │
│   │   ├── 🛠️ utils/               # Frontend Utility Functions
│   │   │   ├── 🎯 index.js         # Utility Exports Hub
│   │   │   ├── 🔍 validators.js    # Form Validation Helpers
│   │   │   ├── 📊 formatters.js    # Data Display Formatting
│   │   │   ├── ⏰ date.js          # Date/Time Display Utilities
│   │   │   └── 📱 device.js        # Device Detection & Responsive Helpers
│   │   │
│   │   └── 🧪 __tests__/           # Frontend Testing Suite
│   │       ├── ⚙️ setup.js         # Test Environment Setup
│   │       ├── 🧩 components/      # Component Unit Tests
│   │       ├── 📄 pages/           # Page Integration Tests
│   │       └── 🔧 utils/           # Utility Function Tests
│   │
│   ├── 🌍 public/                  # Static Assets & Public Files
│   │   ├── 🖼️ favicon.ico          # Site Favicon
│   │   ├── 🏠 index.html           # HTML Template
│   │   ├── 📱 manifest.json        # Progressive Web App Manifest
│   │   ├── 🖼️ images/              # Image Assets Directory
│   │   └── 🎨 icons/               # Icon Assets Directory
│   │
│   └── 🔧 build/                   # Production Build Output (Generated)
│       ├── 🌍 static/              # Static Assets (CSS, JS, Images)
│       └── 🏠 index.html           # Built HTML Entry Point
│
├── 📚 docs/                        # Comprehensive Documentation
│   ├── 🏗️ FILE-STRUCTURE.md       # This File - Architecture Guide
│   ├── 🚀 GETTING-STARTED.md      # Developer Setup Instructions
│   ├── 🌐 DEPLOYMENT-GUIDE.md     # Production Deployment Guide
│   ├── 👤 USER-GUIDE.md           # End-User Manual & Tutorials
│   ├── 👩‍💻 DEVELOPER-GUIDE.md      # Technical Development Documentation
│   ├── 🧪 TESTING-GUIDE.md        # Testing Strategy & Procedures
│   ├── 🔄 WORKFLOW.md             # Development Workflow & Collaboration
│   └── 📸 screenshots/            # UI Screenshots & Visual Documentation
│
└── 🐳 docker/                      # Docker Configuration Files
    ├── 🔧 backend.Dockerfile       # Backend Container Definition
    ├── 🎨 frontend.Dockerfile      # Frontend Container Definition
    ├── 🗄️ nginx.conf              # Reverse Proxy Configuration
    └── 🌐 docker-compose.prod.yml  # Production Docker Compose
```

## 🏗️ Architecture Patterns & Design Principles

### 🔧 Backend Architecture (FastAPI)

**📦 Layered Architecture Pattern:**
```
🌐 API Layer (main.py, analyze.py, etc.)
    ↓ HTTP Requests & Responses
🧠 Business Logic Layer (analysis_engine/)
    ↓ Core Processing & AI Integration
🔧 Service Layer (services/)
    ↓ External Integrations & Database
📦 Data Layer (models/)
    ↓ Data Validation & Serialization
```

**🎯 Key Design Principles:**
- **🔄 Async/Await**: All I/O operations use async patterns for scalability
- **🏗️ Dependency Injection**: Services injected via FastAPI's dependency system
- **📋 Pydantic Models**: Type-safe data validation and serialization
- **🛡️ Security First**: Authentication, input validation, and rate limiting
- **🧪 Testable**: Clear separation of concerns for unit testing

### 🎨 Frontend Architecture (React 18)

**🧩 Component-Based Architecture:**
```
📱 App.jsx (Main Router & State Management)
    ↓ Route-Based Rendering
📄 Pages (Home, Archive, Learn, Dashboard)
    ↓ Page-Specific Logic
🧩 Components (Header, InputTabs, ResultsDisplay)
    ↓ Reusable UI Elements
🎨 Styles (colors.js, animations.js, responsive.js)
    ↓ Design System & Theming
```

**✨ Modern React Patterns:**
- **🎣 Hooks**: useState, useEffect, useCallback, useMemo for state management
- **🎭 Context**: Global state for authentication and app configuration
- **🌊 Framer Motion**: Smooth animations and page transitions
- **📱 Responsive Design**: Mobile-first approach with Tailwind CSS
- **⚡ Performance**: Code splitting, lazy loading, and memoization

## 📦 Module Responsibilities & Data Flow

### 🔧 Backend Modules

#### 🌐 API Layer (`api/`)
**Purpose**: HTTP request handling and response formatting
- **🎯 main.py**: FastAPI app initialization, middleware, CORS
- **🔍 analyze.py**: Text analysis endpoints, batch processing
- **📎 upload.py**: File upload, image analysis, URL processing
- **📋 report.py**: Report generation, PDF export, data visualization
- **📚 archive.py**: Analysis history, search, filtering

#### 🧠 Analysis Engine (`analysis_engine/`)
**Purpose**: Core AI processing and forensic analysis
- **🔬 comprehensive_analysis.py**: Main orchestrator, coordinates all analysis
- **📝 text_analysis.py**: Google Gemini integration, prompt engineering
- **🕵️ source_tracking.py**: Origin tracing, metadata extraction
- **🧩 tactics_breakdown.py**: Manipulation pattern detection
- **🔒 safety_checker.py**: Content filtering, harm detection

#### 🔧 Services (`services/`)
**Purpose**: External integrations and business logic
- **🤖 ai_service.py**: Google AI client, model management
- **🔐 auth_service.py**: JWT tokens, user sessions
- **💾 database_service.py**: Firebase/Firestore operations
- **📁 file_service.py**: Cloud storage, file processing
- **📧 notification_service.py**: Email alerts, admin notifications

### 🎨 Frontend Modules

#### 📄 Pages (`pages/`)
**Purpose**: Main application views and user journeys
- **🏠 Home.jsx**: Primary analysis interface
- **📚 Archive.jsx**: Historical analysis browser
- **🎓 Learn.jsx**: Educational content and tutorials
- **📊 Dashboard.jsx**: Authority user control panel

#### 🧩 Components (`components/`)
**Purpose**: Reusable UI elements and interactions
- **🧭 Header.jsx**: Top navigation, authentication status
- **📝 InputTabs.jsx**: Multi-modal input (text, file, URL)
- **📊 ResultsDisplay.jsx**: Analysis visualization and charts
- **🔐 AuthModal.jsx**: Login/register forms

#### 🔧 Services (`services/`)
**Purpose**: Frontend data management and API communication
- **🌐 api.js**: HTTP client, request/response handling
- **🔐 auth.js**: Authentication state, token management
- **💾 storage.js**: Local storage, user preferences
- **📊 analytics.js**: User behavior tracking

## 🔄 Data Flow Architecture

### 📊 Analysis Request Flow
```
1. 👤 User Input (Text/File/URL)
   ↓
2. 📝 Frontend Validation & Preprocessing
   ↓
3. 🌐 API Request to /api/analyze
   ↓
4. 🔬 comprehensive_analysis.py Orchestration
   ↓
5. 🧠 Parallel Analysis Modules:
   ├── 📝 Text Analysis (Gemini AI)
   ├── 🕵️ Source Tracking
   ├── 🧩 Tactics Breakdown
   └── 🔒 Safety Checking
   ↓
6. 📊 Results Aggregation & Scoring
   ↓
7. 💾 Database Storage (Optional)
   ↓
8. 📤 JSON Response to Frontend
   ↓
9. 📊 Results Visualization & Display
```

### 🔐 Authentication Flow
```
1. 👤 User Login Request
   ↓
2. 🔐 Credential Validation
   ↓
3. 🎫 JWT Token Generation
   ↓
4. 💾 Token Storage (Secure)
   ↓
5. 🛡️ Request Authentication Middleware
   ↓
6. 👤 User Context & Permissions
```

## 🛡️ Security Architecture

### 🔒 Backend Security Layers
- **🌐 API Gateway**: Rate limiting, DDoS protection
- **🔐 Authentication**: JWT tokens, secure sessions
- **📋 Input Validation**: Pydantic models, sanitization
- **🛡️ Authorization**: Role-based access control
- **🔍 Audit Logging**: All actions tracked and logged

### 🛡️ Frontend Security Measures
- **🔒 HTTPS Only**: All communications encrypted
- **🎫 Token Security**: Secure storage, automatic refresh
- **📋 Input Sanitization**: XSS prevention, data validation
- **🔐 Content Security Policy**: Script injection protection
- **📱 Secure Headers**: HSTS, X-Frame-Options, etc.

## 📈 Performance & Scalability

### ⚡ Backend Optimization
- **🔄 Async Processing**: Non-blocking I/O operations
- **📊 Connection Pooling**: Efficient database connections
- **💾 Caching**: Redis for frequently accessed data
- **📈 Load Balancing**: Horizontal scaling capability
- **📊 Monitoring**: Health checks, performance metrics

### 🚀 Frontend Optimization
- **⚡ Code Splitting**: Lazy loading of routes and components
- **🎯 Bundle Optimization**: Tree shaking, minification
- **📱 Progressive Loading**: Skeleton screens, incremental updates
- **💾 Client Caching**: Service workers, local storage
- **📊 Performance Monitoring**: Core Web Vitals, user metrics

## 🧪 Testing Architecture

### 🔧 Backend Testing Strategy
- **📋 Unit Tests**: Individual function and class testing
- **🔗 Integration Tests**: API endpoint and service testing
- **🎯 End-to-End Tests**: Complete user journey testing
- **📊 Performance Tests**: Load testing and benchmarking
- **🛡️ Security Tests**: Vulnerability scanning and penetration testing

### 🎨 Frontend Testing Strategy
- **🧩 Component Tests**: React component unit testing
- **📱 User Interface Tests**: Visual regression testing
- **🔗 Integration Tests**: API integration and data flow
- **📱 Cross-Browser Tests**: Compatibility across browsers
- **♿ Accessibility Tests**: WCAG compliance and usability

## 🚀 Deployment Architecture

### 🌍 Production Environment
- **🐳 Containerization**: Docker containers for consistency
- **☁️ Cloud Platform**: Google Cloud Run for auto-scaling
- **🌐 CDN**: Global content delivery for static assets
- **💾 Database**: Firebase/Firestore for data persistence
- **📊 Monitoring**: Logging, metrics, and alerting systems

### 🔄 CI/CD Pipeline
- **📝 Code Commit**: Git-based version control
- **🧪 Automated Testing**: Full test suite execution
- **🏗️ Build Process**: Docker image creation and optimization
- **🚀 Deployment**: Zero-downtime rolling deployments
- **📊 Health Checks**: Post-deployment verification and monitoring

---

**📋 Next Steps:**
1. Review this architecture guide alongside the Master Plan PDF
2. Follow GETTING-STARTED.md for development environment setup
3. Consult DEVELOPER-GUIDE.md for detailed implementation guidelines
4. Reference DEPLOYMENT-GUIDE.md for production deployment procedures

**🔗 Related Documentation:**
- [Master README](../MASTER-README.md) - Project Overview
- [Development Workflow](WORKFLOW.md) - Team Collaboration Process
- [Getting Started Guide](GETTING-STARTED.md) - Setup Instructions
- [Deployment Guide](DEPLOYMENT-GUIDE.md) - Production Deployment

*This architecture is designed to be scalable, maintainable, and aligned with modern best practices while preserving all TruthLens functionality and adding enhanced forensic capabilities.*