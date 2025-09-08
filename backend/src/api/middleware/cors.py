# backend/src/api/middleware/cors.py
"""
CORS middleware setup for Truth Lab 2.0
Configured for React frontend development and production deployment
"""

from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List

def setup_cors(app):
    """
    Configure CORS middleware for Truth Lab 2.0 API
    
    Supports:
    - React dev server (localhost:3000, localhost:5173)
    - Production frontend domains 
    - Cloudflare Pages deployment
    """
    
    # Default origins for local development
    development_origins = [
        "http://localhost:3000",      # React dev server (Create React App)
        "http://127.0.0.1:3000",
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:8080",      # Alternative dev ports
        "http://127.0.0.1:8080"
    ]
    
    # Production origins from environment
    cors_origins_env = os.getenv("CORS_ORIGINS", "")
    production_origins = []
    if cors_origins_env:
        production_origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    
    # Combine origins
    allowed_origins = development_origins + production_origins
    
    # Development mode: allow all origins if DEBUG is True
    if os.getenv("DEBUG", "false").lower() == "true":
        allowed_origins = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=[
            "Accept",
            "Accept-Language", 
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-API-Key",
            "X-Requested-With",
            "Origin",
            "Cache-Control"
        ],
        expose_headers=["Content-Disposition", "X-Total-Count"],
        max_age=600  # 10 minutes preflight cache
    )
