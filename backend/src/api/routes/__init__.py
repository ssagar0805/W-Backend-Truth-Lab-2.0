# backend/src/api/routes/__init__.py
"""
API Routes package for Truth Lab 2.0
Exposes all route modules for main.py imports
"""

from . import fact_check
from . import upload
from . import report
from . import archive

__all__ = ["fact_check", "upload", "report", "archive"]
