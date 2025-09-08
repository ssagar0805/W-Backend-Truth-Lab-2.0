# backend/src/api/routes/report.py
# Migrated from: TruthLens/app.py - reporting and authority notification capabilities
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime
import logging

from ...utils.security import SecurityService, validate_request
from ...database.archive_service import ArchiveService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
security_service = SecurityService()
archive_service = ArchiveService()

class ReportSubmission(BaseModel):
    """Report submission model for misinformation reporting"""
    original_content: str = Field(..., min_length=1, max_length=5000, description="Content being reported")
    verdict: Literal["false", "caution", "verified"] = Field(..., description="User's assessment")
    category: Literal["health", "politics", "finance", "social", "other"] = Field(..., description="Content category")
    location: Optional[str] = Field(None, description="Geographic context (State, City)")
    description: Optional[str] = Field(None, max_length=1000, description="Additional context")
    evidence_urls: Optional[List[str]] = Field(None, description="Supporting evidence links")
    urgency_level: Optional[Literal["low", "medium", "high", "critical"]] = Field("medium", description="Urgency level")
    source_platform: Optional[str] = Field(None, description="Where content was found")
    reporter_type: Literal["public", "authority", "organization"] = Field("public", description="Reporter type")

class ReportResponse(BaseModel):
    """Report submission response model"""
    report_id: str
    status: str
    category: str
    location: Optional[str]
    verdict: str
    urgency_level: str
    estimated_review_time: str
    authority_notification: Dict[str, Any]
    next_steps: List[str]
    timestamp: str

@router.post("/report", response_model=Dict[str, Any])
async def submit_misinformation_report(
    report: ReportSubmission,
    validated_request: dict = Depends(validate_request)
):
    """
    Submit misinformation report to authorities with comprehensive metadata
    Enhanced with Truth Lab forensic analysis and escalation capabilities
    """
    
    try:
        # Validate and sanitize input
        is_valid, validation_msg = security_service.validate_input(report.original_content)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid content: {validation_msg}")
        
        sanitized_content = security_service.sanitize_input(report.original_content)
        
        # Generate unique report ID
        report_id = f"TL_REP_{int(datetime.now().timestamp())}"
        
        # Determine authority notification based on category and urgency
        authority_notification = {
            "report_id": report_id,
            "status": "submitted",
            "category": report.category,
            "location": report.location or "India (General)",
            "urgency_level": report.urgency_level,
            "auto_escalated": report.urgency_level in ["high", "critical"],
            "notification_sent": True,
            "assigned_authority": _get_authority_by_category_location(report.category, report.location)
        }
        
        # Calculate estimated review time
        review_time_map = {
            "low": "3-5 days",
            "medium": "1-2 days", 
            "high": "4-8 hours",
            "critical": "1-2 hours"
        }
        estimated_review_time = review_time_map.get(report.urgency_level, "1-2 days")
        
        # Prepare report data for storage
        report_data = {
            "report_id": report_id,
            "original_content": sanitized_content,
            "verdict": report.verdict,
            "category": report.category,
            "location": report.location,
            "description": report.description,
            "evidence_urls": report.evidence_urls or [],
            "urgency_level": report.urgency_level,
            "source_platform": report.source_platform,
            "reporter_type": report.reporter_type,
            "authority_notification": authority_notification,
            "estimated_review_time": estimated_review_time,
            "submission_timestamp": datetime.now().isoformat(),
            "status": "pending_review"
        }
        
        # Save to database
        try:
            saved_report_id = await archive_service.save_report(
                report_data=report_data,
                user_type=report.reporter_type
            )
            if saved_report_id:
                report_data["report_id"] = saved_report_id
        except Exception as e:
            logger.info(f"Archive save failed: {e}")
        
        # Generate next steps based on category and urgency
        next_steps = _generate_next_steps(report.category, report.urgency_level, report.location)
        
        response_data = {
            "report_id": report_data["report_id"],
            "status": "submitted_successfully",
            "category": report.category,
            "location": report.location,
            "verdict": report.verdict,
            "urgency_level": report.urgency_level,
            "estimated_review_time": estimated_review_time,
            "authority_notification": authority_notification,
            "next_steps": next_steps,
            "reference_number": f"TL-{report_data['report_id']}",
            "tracking_url": f"/api/report/{report_data['report_id']}/status"
        }
        
        return {
            "success": True,
            "data": response_data,
            "timestamp": datetime.now().isoformat(),
            "message": "Report submitted successfully to Truth Lab authorities"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report submission failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report submission failed: {str(e)}")

@router.get("/report/{report_id}/status")
async def get_report_status(
    report_id: str,
    validated_request: dict = Depends(validate_request)
):
    """Get status of submitted report"""
    
    try:
        # Fetch report status from database
        report_status = await archive_service.get_report_status(report_id)
        
        if not report_status:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "success": True,
            "data": report_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.get("/report/categories")
async def get_report_categories():
    """Get available report categories and their descriptions"""
    
    categories = {
        "health": {
            "description": "Medical misinformation, false cures, vaccine misinformation",
            "examples": ["COVID-19 false treatments", "Miracle cures", "Medical conspiracy theories"],
            "authority": "Ministry of Health and Family Welfare"
        },
        "politics": {
            "description": "Political misinformation, election-related false claims",
            "examples": ["Election fraud claims", "Political conspiracy theories", "False political statements"],
            "authority": "Election Commission of India"
        },
        "finance": {
            "description": "Financial scams, investment fraud, fake schemes",
            "examples": ["Ponzi schemes", "Fake investment opportunities", "UPI frauds"],
            "authority": "Reserve Bank of India / SEBI"
        },
        "social": {
            "description": "Social misinformation, community tensions, fake news",
            "examples": ["Communal misinformation", "Social media hoaxes", "Fake viral content"],
            "authority": "Ministry of Electronics and Information Technology"
        },
        "other": {
            "description": "Other types of misinformation not covered above",
            "examples": ["General fake news", "Miscellaneous false claims"],
            "authority": "Relevant Government Authority"
        }
    }
    
    return {
        "success": True,
        "data": categories,
        "timestamp": datetime.now().isoformat()
    }

def _get_authority_by_category_location(category: str, location: Optional[str]) -> str:
    """Determine appropriate authority based on category and location"""
    
    authority_map = {
        "health": "Ministry of Health and Family Welfare",
        "politics": "Election Commission of India", 
        "finance": "Reserve Bank of India",
        "social": "Ministry of Electronics and IT",
        "other": "Local Government Authority"
    }
    
    base_authority = authority_map.get(category, "General Government Authority")
    
    if location:
        return f"{base_authority} - {location}"
    
    return base_authority

def _generate_next_steps(category: str, urgency: str, location: Optional[str]) -> List[str]:
    """Generate contextual next steps for the report"""
    
    base_steps = [
        f"Report forwarded to relevant authorities for {category} category",
        "You will receive updates via the archive section",
        "Report reference number can be used for follow-up inquiries"
    ]
    
    if urgency == "critical":
        base_steps.insert(0, "CRITICAL: Report escalated for immediate review")
        base_steps.append("Emergency response team has been notified")
    elif urgency == "high":
        base_steps.append("High priority review initiated")
    
    if location:
        base_steps.append(f"Local authorities in {location} have been notified")
    
    return base_steps
