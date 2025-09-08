# backend/src/api/middleware/auth.py
"""
Authentication and authorization middleware for Truth Lab 2.0
Compatible with SecurityService and validate_request dependency injection
"""

import os
import logging
from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from datetime import datetime

logger = logging.getLogger(__name__)

class TruthLabAuthMiddleware(BaseHTTPMiddleware):
    """
    Truth Lab 2.0 authentication middleware
    
    Features:
    - Optional API key protection for production
    - Request rate limiting awareness
    - User context setup for downstream handlers
    - Compatible with existing SecurityService validation
    """
    
    def __init__(self, app, api_key: Optional[str] = None):
        super().__init__(app)
        self.api_key = api_key
        self.protected_paths = ["/api/fact-check", "/api/upload", "/api/report"]
        self.public_paths = ["/", "/health", "/api/status", "/api/docs", "/api/redoc"]
        
    async def dispatch(self, request: Request, call_next):
        # Set default user context
        request.state.user = "public"
        request.state.user_type = "public"
        request.state.authenticated = False
        request.state.request_id = f"req_{int(datetime.utcnow().timestamp())}"
        
        path = request.url.path
        
        # Skip auth for public endpoints
        if any(path.startswith(public_path) for public_path in self.public_paths):
            return await call_next(request)
        
        # API key authentication (optional, for production)
        if self.api_key and path.startswith("/api"):
            provided_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
            
            if not provided_key:
                logger.warning(f"Missing API key for protected path: {path}")
                return JSONResponse(
                    {
                        "success": False,
                        "error": "API key required for this endpoint",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    status_code=401
                )
            
            if provided_key != self.api_key:
                logger.warning(f"Invalid API key for path: {path}")
                return JSONResponse(
                    {
                        "success": False, 
                        "error": "Invalid API key",
                        "timestamp": datetime.utcnow().isoformat()
                    },
                    status_code=401
                )
            
            # Valid API key - mark as authenticated
            request.state.authenticated = True
            request.state.user_type = "authority"  # API key users are authorities
        
        # Authority user detection (for enhanced features)
        auth_header = request.headers.get("authorization", "")
        if "authority" in auth_header.lower():
            request.state.user_type = "authority"
        
        # Add request logging for monitoring
        logger.info(f"Request: {request.method} {path} - User: {request.state.user_type}")
        
        return await call_next(request)

def setup_auth(app):
    """
    Setup authentication middleware for Truth Lab 2.0
    
    Configuration:
    - TL_API_KEY: Optional API key for production protection
    - ENVIRONMENT: If 'development', auth is more relaxed
    """
    
    # Get API key from environment (optional)
    api_key = os.getenv("TL_API_KEY")
    environment = os.getenv("ENVIRONMENT", "development")
    
    # In development, API key is optional
    if environment == "development":
        logger.info("Auth middleware: Development mode - API key protection is optional")
    elif api_key:
        logger.info("Auth middleware: Production mode - API key protection enabled")
    else:
        logger.warning("Auth middleware: Production mode without API key - consider setting TL_API_KEY")
    
    # Add the middleware
    app.add_middleware(TruthLabAuthMiddleware, api_key=api_key)
