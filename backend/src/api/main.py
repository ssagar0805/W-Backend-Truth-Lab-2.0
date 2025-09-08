# Migrated from: TruthLens/app.py - main application entry point
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from datetime import datetime
import uvicorn

from .routes import fact_check, upload, report, archive
from .middleware.cors import setup_cors
from .middleware.auth import setup_auth

# Initialize FastAPI app
app = FastAPI(
    title="Truth Lab 2.0 API",
    description="AI-Powered Misinformation Detection & Forensic Analysis Platform",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Setup middleware
setup_cors(app)
setup_auth(app)

# Include route modules
app.include_router(fact_check.router, prefix="/api", tags=["fact-check"])
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(report.router, prefix="/api", tags=["report"])
app.include_router(archive.router, prefix="/api", tags=["archive"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Truth Lab 2.0 API",
        "version": "2.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "fact_check": "/api/fact-check",
            "upload": "/api/upload", 
            "report": "/api/report",
            "archive": "/api/archive",
            "docs": "/api/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check for monitoring"""
    # Test connections to external services
    from ..analysis_engine.comprehensive_analysis import test_all_services
    
    service_status = await test_all_services()
    
    return {
        "status": "healthy" if all(service_status.values()) else "degraded",
        "timestamp": datetime.now().isoformat(),
        "services": service_status,
        "version": "2.0.0"
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint for frontend"""
    from ..analysis_engine.comprehensive_analysis import test_all_services
    
    services = await test_all_services()
    
    return {
        "🤖 Gemini AI": services.get("gemini", False),
        "✅ Fact Check": services.get("fact_check", False), 
        "📰 News APIs": services.get("news", False),
        "🔒 Security": services.get("security", False),
        "☁️ Database": services.get("database", False)
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )