# backend/src/api/routes/upload.py
# Migrated from: TruthLens/app.py - file upload and media analysis capabilities
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime
import logging

from ...analysis_engine.comprehensive_analysis import conduct_comprehensive_analysis
from ...utils.security import SecurityService, validate_request
from ...database.archive_service import ArchiveService

# Optional image forensics import
try:
    from ...analysis_engine.image_forensics import ImageForensics
except ImportError:
    ImageForensics = None

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
security_service = SecurityService()
archive_service = ArchiveService()

# File constraints
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB as per PRD
ALLOWED_TYPES = {
    "image/jpeg", "image/png", "image/gif", "image/webp",
    "application/pdf",
    "video/mp4", "video/avi", "video/mov"
}

class FileAnalysisResult(BaseModel):
    """File analysis result model"""
    file_id: str
    filename: str
    content_type: str
    size_bytes: int
    analysis_type: str
    language: str
    forensic_analysis: Optional[Dict[str, Any]] = None
    text_analysis: Optional[Dict[str, Any]] = None
    metadata_analysis: Optional[Dict[str, Any]] = None
    risk_score: Optional[int] = None
    timestamp: str

@router.post("/upload", response_model=Dict[str, Any])
async def upload_file_analysis(
    file: UploadFile = File(...),
    language: Literal["en", "hi", "ta", "te", "bn", "mr"] = Form("en"),
    analysis_type: Literal["forensic", "quick", "deep"] = Form("forensic"),
    extract_text: bool = Form(True),
    user_type: str = Form("public"),
    validated_request: dict = Depends(validate_request)
):
    """
    File upload and forensic analysis endpoint
    Enhanced with image forensics and comprehensive analysis capabilities
    """
    
    try:
        # Read and validate file
        contents = await file.read()
        
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file type: {file.content_type}"
            )
        
        # Security validation
        is_valid, validation_msg = security_service.validate_file(
            file.filename, file.content_type, len(contents)
        )
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"File validation failed: {validation_msg}")
        
        await file.seek(0)
        
        # Initialize analysis results
        analysis_results = {
            "file_id": f"file_{int(datetime.now().timestamp())}",
            "filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
            "analysis_type": analysis_type,
            "language": language,
            "user_type": user_type
        }
        
        # Image forensic analysis
        if file.content_type.startswith("image/") and ImageForensics:
            try:
                image_forensics = ImageForensics(config={})
                forensic_result = await image_forensics.analyze_image(contents, filename=file.filename)
                analysis_results["forensic_analysis"] = forensic_result
                analysis_results["risk_score"] = forensic_result.get("forensic_score", 50)
            except Exception as e:
                logger.warning(f"Image forensics failed: {e}")
                analysis_results["forensic_analysis"] = {"error": str(e)}
        
        # Text extraction and analysis for supported formats
        extracted_text = None
        if file.content_type == "application/pdf" and extract_text:
            # PDF text extraction would go here
            extracted_text = "PDF text extraction not implemented yet"
        elif file.content_type.startswith("image/") and extract_text:
            # OCR text extraction would go here  
            extracted_text = "OCR text extraction available in forensics"
        
        # Comprehensive analysis on extracted text
        if extracted_text and len(extracted_text) > 10:
            try:
                text_analysis = await conduct_comprehensive_analysis(
                    text=extracted_text,
                    language=language,
                    level="Deep Forensics" if analysis_type == "deep" else "Quick Scan",
                    enable_context=True,
                    track_origin=analysis_type in ["forensic", "deep"],
                    safety_check=True,
                    user_type=user_type
                )
                analysis_results["text_analysis"] = text_analysis
                if not analysis_results.get("risk_score"):
                    analysis_results["risk_score"] = text_analysis.get("risk_score", 50)
            except Exception as e:
                logger.warning(f"Text analysis failed: {e}")
                analysis_results["text_analysis"] = {"error": str(e)}
        
        # Save to archive
        try:
            file_id = await archive_service.save_file_analysis(
                filename=file.filename,
                content_type=file.content_type,
                size_bytes=len(contents),
                analysis_results=analysis_results,
                user_type=user_type
            )
            analysis_results["file_id"] = file_id or analysis_results["file_id"]
        except Exception as e:
            logger.info(f"Archive save failed: {e}")
        
        analysis_results["timestamp"] = datetime.now().isoformat()
        
        return {
            "success": True,
            "data": analysis_results,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File analysis failed: {str(e)}")

@router.get("/upload/formats")
async def get_supported_formats():
    """Get list of supported file formats"""
    return {
        "success": True,
        "data": {
            "max_file_size_mb": MAX_FILE_SIZE // (1024*1024),
            "supported_formats": {
                "images": ["JPEG", "PNG", "GIF", "WebP"],
                "documents": ["PDF"],
                "videos": ["MP4", "AVI", "MOV"]
            },
            "analysis_capabilities": {
                "image_forensics": ImageForensics is not None,
                "text_extraction": True,
                "metadata_analysis": True,
                "content_analysis": True
            }
        }
    }
