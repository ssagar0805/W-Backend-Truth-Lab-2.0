# Migrated from: TruthLens/app.py - text_analyzer_interface and conduct_forensic_analysis functions
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import asyncio

from ...analysis_engine.comprehensive_analysis import conduct_comprehensive_analysis
from ...database.models import AnalysisRequest, AnalysisResponse
from ...utils.security import SecurityService, validate_request
from ...database.archive_service import ArchiveService

router = APIRouter()

class TextAnalysisRequest(BaseModel):
    """Text analysis request model"""
    content: str = Field(..., min_length=10, max_length=10000, description="Text content to analyze")
    language: str = Field(default="en", description="Content language (en, hi, ta, te, bn, mr)")
    analysis_level: str = Field(default="Quick Scan", description="Analysis depth: Quick Scan, Deep Analysis")
    safety_check: bool = Field(default=True, description="Enable safety checking")
    track_origin: bool = Field(default=False, description="Enable origin tracking")
    user_type: str = Field(default="public", description="User type: public, authority")

class AnalysisResults(BaseModel):
    """Analysis results response model"""
    risk_score: int = Field(..., ge=0, le=100)
    credibility_score: int = Field(..., ge=0, le=100) 
    threat_level: str
    manipulation_tactics: List[str]
    ai_analysis: Optional[str]
    fact_checks: List[Dict[str, Any]]
    source_links: List[Dict[str, str]]
    reporting_emails: List[Dict[str, str]]
    origin_analysis: Optional[str]
    context_analysis: Optional[str]
    safety_analysis: Optional[Dict[str, Any]]
    structure_analysis: Optional[Dict[str, Any]]
    recommendations: List[str]
    analysis_id: str
    timestamp: str

# Initialize services
security_service = SecurityService()
archive_service = ArchiveService()

@router.post("/fact-check", response_model=AnalysisResults)
async def analyze_text_content(
    request: TextAnalysisRequest,
    validated_request: dict = Depends(validate_request)
):
    """
    Comprehensive text analysis for misinformation detection
    
    Migrated from: TruthLens/app.py - conduct_forensic_analysis()
    Enhanced with forensic capabilities from Master Plan requirements
    """
    
    try:
        # Validate and sanitize input
        is_valid, validation_msg = security_service.validate_input(request.content)
        if not is_valid:
            raise HTTPException(status_code=400, detail=f"Invalid input: {validation_msg}")
        
        sanitized_content = security_service.sanitize_input(request.content)
        
        # Determine analysis parameters based on request
        forensic_level = "Deep Forensics" if request.analysis_level == "Deep Analysis" else "Quick Scan"
        
        # Conduct comprehensive analysis
        analysis_results = await conduct_comprehensive_analysis(
            text=sanitized_content,
            language=request.language,
            level=forensic_level,
            enable_context=True,
            track_origin=request.track_origin or (request.analysis_level == "Deep Analysis"),
            safety_check=request.safety_check,
            user_type=request.user_type
        )
        
        # Save to database
        analysis_id = await archive_service.save_text_analysis(
            content=sanitized_content,
            results=analysis_results,
            user_type=request.user_type
        )
        
        # Format response
        response = AnalysisResults(
            risk_score=analysis_results['risk_score'],
            credibility_score=analysis_results['credibility_score'],
            threat_level=analysis_results['threat_level'],
            manipulation_tactics=analysis_results['manipulation_tactics'],
            ai_analysis=analysis_results.get('ai_analysis'),
            fact_checks=analysis_results.get('fact_checks', []),
            source_links=analysis_results.get('source_links', []),
            reporting_emails=analysis_results.get('reporting_emails', []),
            origin_analysis=analysis_results.get('origin_analysis'),
            context_analysis=analysis_results.get('context_analysis'),
            safety_analysis=analysis_results.get('safety_analysis'),
            structure_analysis=analysis_results.get('structure_analysis'),
            recommendations=analysis_results['recommendations'],
            analysis_id=analysis_id or "unknown",
            timestamp=datetime.now().isoformat()
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/fact-check/batch")
async def analyze_batch_content(
    requests: List[TextAnalysisRequest],
    validated_request: dict = Depends(validate_request)
):
    """
    Batch analysis for multiple text contents
    Enhanced capability for authority users
    """
    
    if len(requests) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 texts per batch")
    
    try:
        # Process all requests concurrently
        tasks = []
        for req in requests:
            task = analyze_text_content(req, validated_request)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Format batch response
        batch_response = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                batch_response.append({
                    "index": i,
                    "error": str(result),
                    "status": "failed"
                })
            else:
                batch_response.append({
                    "index": i,
                    "result": result,
                    "status": "success"
                })
        
        return {
            "batch_id": f"batch_{datetime.now().timestamp()}",
            "total": len(requests),
            "successful": len([r for r in batch_response if r["status"] == "success"]),
            "failed": len([r for r in batch_response if r["status"] == "failed"]),
            "results": batch_response,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch analysis failed: {str(e)}")

@router.get("/fact-check/stats")
async def get_analysis_statistics():
    """
    Get analysis statistics for dashboard
    Migrated from: TruthLens/app.py - display_header_stats()
    """
    
    try:
        stats = await archive_service.get_statistics()
        return {
            "analyzed_today": stats.get('analyzed_today', 0),
            "flagged_content": stats.get('flagged_content', 0), 
            "verified_claims": stats.get('verified_claims', 0),
            "accuracy_rate": stats.get('accuracy_rate', 0.0),
            "trending_threats": await archive_service.get_trending_threats(),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")

@router.get("/fact-check/quick-test")
async def quick_test_analysis():
    """Quick test endpoint for system validation"""
    
    test_text = "This is a test message to verify the analysis system is working properly."
    
    try:
        results = await conduct_comprehensive_analysis(
            text=test_text,
            language="en",
            level="Quick Scan",
            enable_context=False,
            track_origin=False,
            safety_check=True,
            user_type="public"
        )
        
        return {
            "status": "system_operational",
            "test_completed": True,
            "risk_score": results['risk_score'],
            "credibility_score": results['credibility_score'],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "system_error",
            "test_completed": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }