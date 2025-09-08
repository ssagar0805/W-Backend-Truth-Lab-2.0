# Migrated from: TruthLens/config.py - Config class
import os
from typing import Dict, Any

class Config:
    """
    Centralized configuration management
    Migrated from: TruthLens/config.py
    Enhanced for production deployment
    """
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDCGUgJR20zmhvlrkYVa4HUDE-W_Wk7Tbs")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", GEMINI_API_KEY)
    
    # News APIs
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "27fc63acd5064608a6a1387488c7208b")
    NEWSDATA_KEY = os.getenv("NEWSDATA_API_KEY", "ub_5b6d7697fe6c4f9d8cb9ce964f292760")
    
    # Firebase Configuration
    FIREBASE_CONFIG = {
        "apiKey": os.getenv("FIREBASE_API_KEY", ""),
        "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
        "projectId": os.getenv("FIREBASE_PROJECT_ID", "truthlens-2025"),
        "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
        "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
        "appId": os.getenv("FIREBASE_APP_ID", "")
    }
    
    # Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "truth-lab-2025")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Application Settings
    APP_NAME = "Truth Lab 2.0"
    VERSION = "2.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # API Settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("PORT", 8000))
    API_WORKERS = int(os.getenv("API_WORKERS", 1))
    
    # Security Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # CORS Settings
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://localhost:3000").split(",")
    
    # Analysis Settings
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10000))
    MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", 10))
    ANALYSIS_TIMEOUT = int(os.getenv("ANALYSIS_TIMEOUT", 30))
    
    # Rate Limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 3600))  # seconds
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Database Configuration (for production)
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    FIRESTORE_COLLECTION_PREFIX = os.getenv("FIRESTORE_COLLECTION_PREFIX", "truthlab_")
    
    # External Service URLs
    GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
    FACT_CHECK_BASE_URL = "https://factchecktools.googleapis.com/v1alpha1"
    NEWS_API_BASE_URL = "https://newsapi.org/v2"
    
    # Feature Flags
    ENABLE_ORIGIN_TRACKING = os.getenv("ENABLE_ORIGIN_TRACKING", "True").lower() == "true"
    ENABLE_CONTEXT_ANALYSIS = os.getenv("ENABLE_CONTEXT_ANALYSIS", "True").lower() == "true"
    ENABLE_IMAGE_ANALYSIS = os.getenv("ENABLE_IMAGE_ANALYSIS", "True").lower() == "true"
    ENABLE_BATCH_ANALYSIS = os.getenv("ENABLE_BATCH_ANALYSIS", "True").lower() == "true"
    
    # Authority Dashboard Settings
    AUTHORITY_DASHBOARD_ENABLED = os.getenv("AUTHORITY_DASHBOARD_ENABLED", "True").lower() == "true"
    MAX_AUTHORITY_REPORTS = int(os.getenv("MAX_AUTHORITY_REPORTS", 1000))
    
    # Monitoring and Analytics
    ENABLE_ANALYTICS = os.getenv("ENABLE_ANALYTICS", "True").lower() == "true"
    ANALYTICS_RETENTION_DAYS = int(os.getenv("ANALYTICS_RETENTION_DAYS", 90))
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            "project_id": cls.FIREBASE_CONFIG["projectId"],
            "collection_prefix": cls.FIRESTORE_COLLECTION_PREFIX,
            "database_url": cls.DATABASE_URL
        }
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Get API configuration"""
        return {
            "host": cls.API_HOST,
            "port": cls.API_PORT,
            "workers": cls.API_WORKERS,
            "debug": cls.DEBUG,
            "cors_origins": cls.CORS_ORIGINS
        }
    
    @classmethod
    def get_security_config(cls) -> Dict[str, Any]:
        """Get security configuration"""
        return {
            "secret_key": cls.SECRET_KEY,
            "token_expire_minutes": cls.ACCESS_TOKEN_EXPIRE_MINUTES,
            "max_content_length": cls.MAX_CONTENT_LENGTH,
            "rate_limit_enabled": cls.RATE_LIMIT_ENABLED,
            "rate_limit_requests": cls.RATE_LIMIT_REQUESTS,
            "rate_limit_window": cls.RATE_LIMIT_WINDOW
        }
    
    @classmethod
    def get_analysis_config(cls) -> Dict[str, Any]:
        """Get analysis configuration"""
        return {
            "max_content_length": cls.MAX_CONTENT_LENGTH,
            "max_batch_size": cls.MAX_BATCH_SIZE,
            "timeout": cls.ANALYSIS_TIMEOUT,
            "enable_origin_tracking": cls.ENABLE_ORIGIN_TRACKING,
            "enable_context_analysis": cls.ENABLE_CONTEXT_ANALYSIS,
            "enable_image_analysis": cls.ENABLE_IMAGE_ANALYSIS,
            "enable_batch_analysis": cls.ENABLE_BATCH_ANALYSIS
        }
    
    @classmethod
    def get_feature_flags(cls) -> Dict[str, bool]:
        """Get all feature flags"""
        return {
            "origin_tracking": cls.ENABLE_ORIGIN_TRACKING,
            "context_analysis": cls.ENABLE_CONTEXT_ANALYSIS,
            "image_analysis": cls.ENABLE_IMAGE_ANALYSIS,
            "batch_analysis": cls.ENABLE_BATCH_ANALYSIS,
            "authority_dashboard": cls.AUTHORITY_DASHBOARD_ENABLED,
            "analytics": cls.ENABLE_ANALYTICS
        }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        issues = []
        warnings = []
        
        # Check required API keys
        if not cls.GEMINI_API_KEY or cls.GEMINI_API_KEY == "your-api-key-here":
            issues.append("GEMINI_API_KEY not configured")
        
        if not cls.SECRET_KEY or cls.SECRET_KEY == "your-secret-key-here":
            warnings.append("SECRET_KEY using default value (not secure for production)")
        
        if cls.ENVIRONMENT == "production" and cls.DEBUG:
            warnings.append("DEBUG mode enabled in production environment")
        
        # Check Firebase configuration
        firebase_required = ["projectId"]
        for field in firebase_required:
            if not cls.FIREBASE_CONFIG.get(field):
                issues.append(f"Firebase {field} not configured")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "environment": cls.ENVIRONMENT,
            "debug_mode": cls.DEBUG
        }