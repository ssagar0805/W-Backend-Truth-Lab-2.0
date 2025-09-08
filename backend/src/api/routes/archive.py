# backend/src/api/routes/archive.py
# Migrated from: TruthLens/app.py - historical data and case management capabilities
from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Literal, List, Dict, Any
from datetime import datetime, timedelta
import logging

from ...utils.security import validate_request
from ...database.archive_service import ArchiveService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
archive_service = ArchiveService()

class ArchiveFilter(BaseModel):
    """Archive filtering options"""
    category: Optional[Literal["health", "politics", "finance", "social", "other", "all"]] = None
    verdict: Optional[Literal["verified", "caution", "false", "all"]] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    location: Optional[str] = None
    analysis_type: Optional[str] = None

@router.get("/archive")
async def get_archive_cases(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Items per page"),
    category: Optional[Literal["health", "politics", "finance", "social", "other", "all"]] = Query(None),
    verdict: Optional[Literal["verified", "caution", "false", "all"]] = Query(None),
    search: Optional[str] = Query(None, max_length=200, description="Search term"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    location: Optional[str] = Query(None, description="Filter by location"),
    sort_by: Optional[Literal["date", "risk_score", "credibility"]] = Query("date"),
    sort_order: Optional[Literal["asc", "desc"]] = Query("desc"),
    validated_request: dict = Depends(validate_request)
):
    """
    Retrieve archived misinformation cases with comprehensive filtering and analysis
    Enhanced with Truth Lab forensic data and detailed case information
    """
    
    try:
        # Try to get data from database first
        try:
            archive_data = await archive_service.list_archive_cases(
                page=page,
                limit=limit,
                filters={
                    "category": category,
                    "verdict": verdict,
                    "search": search,
                    "date_from": date_from,
                    "date_to": date_to,
                    "location": location,
                    "sort_by": sort_by,
                    "sort_order": sort_order
                }
            )
            
            if archive_data:
                return {
                    "success": True,
                    "data": archive_data,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.info(f"Database archive unavailable, using mock data: {e}")
        
        # Fallback to enhanced mock data for development
        mock_cases = _generate_mock_archive_cases()
        
        # Apply filters to mock data
        filtered_cases = _apply_filters(mock_cases, {
            "category": category,
            "verdict": verdict,
            "search": search,
            "date_from": date_from,
            "date_to": date_to,
            "location": location
        })
        
        # Apply sorting
        sorted_cases = _apply_sorting(filtered_cases, sort_by, sort_order)
        
        # Apply pagination
        total_count = len(sorted_cases)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_cases = sorted_cases[start_idx:end_idx]
        
        # Generate comprehensive response
        response_data = {
            "items": paginated_cases,
            "pagination": {
                "total_cases": total_count,
                "page": page,
                "per_page": limit,
                "total_pages": (total_count + limit - 1) // limit,
                "has_more": end_idx < total_count,
                "next_page": page + 1 if end_idx < total_count else None
            },
            "filters_applied": {
                "category": category,
                "verdict": verdict,
                "search": search,
                "date_range": f"{date_from} to {date_to}" if date_from and date_to else None,
                "location": location,
                "sort_by": sort_by,
                "sort_order": sort_order
            },
            "summary_stats": _generate_summary_stats(mock_cases),
            "trending_categories": _get_trending_categories(mock_cases),
            "recent_activity": _get_recent_activity(mock_cases[:5])
        }
        
        return {
            "success": True,
            "data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Archive retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Archive retrieval failed: {str(e)}")

@router.get("/archive/{case_id}")
async def get_case_details(
    case_id: str,
    validated_request: dict = Depends(validate_request)
):
    """Get detailed forensic analysis for specific case"""
    
    try:
        # Try database first
        try:
            case_details = await archive_service.get_case_details(case_id)
            if case_details:
                return {
                    "success": True,
                    "data": case_details,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.info(f"Database unavailable, using mock: {e}")
        
        # Mock detailed case for development
        detailed_case = {
            "case_id": case_id,
            "title": "COVID-19 Misinformation Analysis - Turmeric False Cure Claims",
            "summary": "Comprehensive forensic analysis of viral social media post claiming turmeric cures COVID-19",
            "analysis_metadata": {
                "analysis_date": "2024-01-15T10:30:00Z",
                "analysis_type": "Deep Forensics",
                "processing_time": "2.34 seconds",
                "confidence_level": 0.92
            },
            "original_content": {
                "text": "BREAKING: Doctors don't want you to know this! Turmeric mixed with warm water cures COVID-19 in 24 hours. Share immediately!",
                "source_platform": "WhatsApp",
                "first_detected": "2024-01-14T08:15:00Z",
                "language": "English"
            },
            "forensic_analysis": {
                "overall_credibility_score": 15,
                "risk_score": 88,
                "threat_level": "HIGH",
                "credibility_breakdown": {
                    "factual_accuracy": 5,
                    "source_quality": 10,
                    "logical_consistency": 15,
                    "bias_score": 90,
                    "manipulation_score": 95
                },
                "manipulation_tactics": [
                    "False urgency ('Share immediately!')",
                    "Authority appeal ('Doctors don't want you to know')",
                    "Medical misinformation",
                    "Conspiracy theory elements",
                    "Emotional manipulation"
                ]
            },
            "source_tracking": {
                "origin_analysis": {
                    "first_appearance": "2024-01-14T08:15:00Z",
                    "suspected_origin": "Unverified social media account",
                    "propagation_pattern": "Viral sharing in WhatsApp groups",
                    "geographic_spread": ["Maharashtra", "Delhi", "Karnataka"],
                    "platform_distribution": {"WhatsApp": 65, "Facebook": 25, "Twitter": 10}
                },
                "content_fingerprint": "sha256:abc123...",
                "similar_claims": 127,
                "variation_analysis": "Multiple language adaptations found"
            },
            "context_analysis": {
                "temporal_context": "Spread during COVID-19 vaccine rollout period",
                "event_correlation": "High correlation with anti-vaccine sentiment",
                "regional_sensitivity": "Health misinformation during pandemic",
                "trending_patterns": "Peak sharing during evening hours"
            },
            "authority_actions": [
                {
                    "action": "Flagged to Ministry of Health",
                    "timestamp": "2024-01-15T12:00:00Z",
                    "status": "Acknowledged"
                },
                {
                    "action": "Added to misinformation database",
                    "timestamp": "2024-01-15T14:30:00Z",
                    "status": "Completed"
                },
                {
                    "action": "Social media platforms notified",
                    "timestamp": "2024-01-15T16:45:00Z",
                    "status": "In Progress"
                }
            ],
            "educational_insights": {
                "key_learnings": [
                    "Medical claims require peer-reviewed scientific evidence",
                    "Urgency tactics are common in health misinformation",
                    "Cross-verification with health authorities is essential"
                ],
                "verification_steps": [
                    "Check with official health ministry guidelines",
                    "Look for scientific studies from reputable journals",
                    "Verify with medical professionals"
                ],
                "similar_case_references": ["TL_CASE_001", "TL_CASE_045", "TL_CASE_078"]
            },
            "impact_assessment": {
                "estimated_reach": "500,000+ people",
                "potential_harm_level": "High",
                "demographic_impact": "Primarily older adults",
                "follow_up_required": True
            }
        }
        
        return {
            "success": True,
            "data": detailed_case,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Case detail retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Case detail retrieval failed: {str(e)}")

@router.get("/archive/stats")
async def get_archive_statistics():
    """Get comprehensive archive statistics for dashboard"""
    
    try:
        stats = await archive_service.get_archive_statistics()
        
        if not stats:
            # Mock statistics for development
            stats = {
                "total_cases": 1247,
                "cases_this_month": 89,
                "high_risk_cases": 156,
                "resolved_cases": 1091,
                "pending_cases": 156,
                "category_distribution": {
                    "health": 412,
                    "politics": 289, 
                    "finance": 234,
                    "social": 201,
                    "other": 111
                },
                "verdict_distribution": {
                    "false": 687,
                    "caution": 324,
                    "verified": 236
                },
                "geographic_distribution": {
                    "Maharashtra": 186,
                    "Delhi": 145,
                    "Karnataka": 132,
                    "Tamil Nadu": 98,
                    "Other": 686
                },
                "trend_analysis": {
                    "weekly_growth": "+12%",
                    "most_active_category": "health",
                    "peak_activity_hours": "18:00-22:00",
                    "average_resolution_time": "2.3 days"
                }
            }
        
        return {
            "success": True,
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Statistics retrieval failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}")

# Helper functions for mock data and filtering
def _generate_mock_archive_cases() -> List[Dict[str, Any]]:
    """Generate comprehensive mock archive cases"""
    
    cases = []
    categories = ["health", "politics", "finance", "social"]
    verdicts = ["false", "caution", "verified"]
    locations = ["Maharashtra", "Delhi", "Karnataka", "Tamil Nadu"]
    
    for i in range(1, 101):
        case_date = datetime.now() - timedelta(days=i)
        
        cases.append({
            "id": f"case_{i:03d}",
            "title": f"Misinformation Case #{i}: {categories[i % 4].title()} Related Analysis",
            "summary": f"Comprehensive analysis of {categories[i % 4]} misinformation case with forensic investigation",
            "verdict": verdicts[i % 3],
            "category": categories[i % 4],
            "date": case_date.strftime("%Y-%m-%d"),
            "location": locations[i % 4],
            "risk_score": 85 - (i % 60),
            "credibility_score": 30 + (i % 40),
            "analysis_type": ["Deep Forensics", "Quick Scan", "Comprehensive Analysis"][i % 3],
            "threat_level": ["LOW", "MEDIUM", "HIGH"][i % 3],
            "source_tracked": i % 2 == 0,
            "reported_count": (i * 2) % 20,
            "authority_action": i % 3 == 0,
            "impact_level": ["Low", "Medium", "High"][i % 3],
            "processing_time": round(1.2 + (i % 5) * 0.3, 2),
            "languages_detected": ["English", "Hindi", "Tamil", "Telugu"][i % 4]
        })
    
    return cases

def _apply_filters(cases: List[Dict], filters: Dict) -> List[Dict]:
    """Apply filters to case list"""
    
    filtered = cases
    
    if filters.get("category") and filters["category"] != "all":
        filtered = [c for c in filtered if c["category"] == filters["category"]]
    
    if filters.get("verdict") and filters["verdict"] != "all":
        filtered = [c for c in filtered if c["verdict"] == filters["verdict"]]
    
    if filters.get("search"):
        search_term = filters["search"].lower()
        filtered = [c for c in filtered if search_term in c["title"].lower() or search_term in c["summary"].lower()]
    
    if filters.get("location"):
        filtered = [c for c in filtered if c["location"] == filters["location"]]
    
    return filtered

def _apply_sorting(cases: List[Dict], sort_by: Optional[str], sort_order: Optional[str]) -> List[Dict]:
    """Apply sorting to case list"""
    
    if not sort_by:
        return cases
    
    reverse = sort_order == "desc"
    
    if sort_by == "date":
        return sorted(cases, key=lambda x: x["date"], reverse=reverse)
    elif sort_by == "risk_score":
        return sorted(cases, key=lambda x: x["risk_score"], reverse=reverse)
    elif sort_by == "credibility":
        return sorted(cases, key=lambda x: x["credibility_score"], reverse=reverse)
    
    return cases

def _generate_summary_stats(cases: List[Dict]) -> Dict[str, Any]:
    """Generate summary statistics from cases"""
    
    total = len(cases)
    if total == 0:
        return {}
    
    return {
        "total_cases": total,
        "high_risk_cases": len([c for c in cases if c["risk_score"] > 70]),
        "cases_this_week": len([c for c in cases if (datetime.now() - datetime.strptime(c["date"], "%Y-%m-%d")).days <= 7]),
        "average_risk_score": round(sum(c["risk_score"] for c in cases) / total, 1),
        "average_credibility": round(sum(c["credibility_score"] for c in cases) / total, 1),
        "most_common_category": max(set(c["category"] for c in cases), key=lambda x: sum(1 for c in cases if c["category"] == x))
    }

def _get_trending_categories(cases: List[Dict]) -> List[Dict[str, Any]]:
    """Get trending categories analysis"""
    
    recent_cases = [c for c in cases if (datetime.now() - datetime.strptime(c["date"], "%Y-%m-%d")).days <= 30]
    
    category_counts = {}
    for case in recent_cases:
        cat = case["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    return [{"category": k, "count": v, "trend": "+15%"} for k, v in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)]

def _get_recent_activity(cases: List[Dict]) -> List[Dict[str, Any]]:
    """Get recent activity summary"""
    
    return [
        {
            "case_id": case["id"],
            "activity": f"New {case['category']} case analyzed",
            "timestamp": case["date"],
            "severity": case["threat_level"]
        }
        for case in cases[:5]
    ]
