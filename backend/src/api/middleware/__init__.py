# backend/src/api/middleware/__init__.py
"""
API Middleware package for Truth Lab 2.0
Exposes CORS and authentication setup functions for main.py
"""

from .cors import setup_cors
from .auth import setup_auth

__all__ = ["setup_cors", "setup_auth"]
