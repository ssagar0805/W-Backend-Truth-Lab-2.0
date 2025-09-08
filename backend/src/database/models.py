# Migrated from: TruthLens/utils/database.py - FirebaseService class and data models
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

class UserType(str, Enum):
    """User types for access control"""
    PUBLIC = "public"
    AUTHORITY = "authority"

class ThreatLevel(str, Enum):
    """Threat levels for content classification"""
    LOW = "LOW"
    MEDIUM = "MEDIUM" 
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AnalysisType(str, Enum):
    """Types of analysis supported"""
    TEXT = "text"
    IMAGE = "image"
    URL = "url"
    SOCIAL_MEDIA = "social_media"

class AnalysisRequest(BaseModel):
    """Base analysis request model"""
    content: str = Field(..., description="Content to analyze")
    content_type: AnalysisType = Field(default=AnalysisType.TEXT, description="Type of content")
    language: str = Field(default="en", description="Content language")
    analysis_level: str = Field(default="Quick Scan", description="Analysis depth")
    user_type: UserType = Field(default=UserType.PUBLIC, description="User type")
    safety_check: bool = Field(default=True, description="Enable safety checking")
    track_origin: bool = Field(default=False, description="Enable origin tracking")
    
class AnalysisResponse(BaseModel):
    """Base analysis response model"""
    analysis_id: str
    risk_score: int = Field(..., ge=0, le=100)
    credibility_score: int = Field(..., ge=0, le=100)
    threat_level: ThreatLevel
    timestamp: datetime
    
class SafetyAnalysis(BaseModel):
    """Safety analysis results model"""
    is_safe: bool
    safety_score: int = Field(..., ge=0, le=100)
    flagged_words: List[str] = []
    content_warnings: List[str] = []
    
class StructureAnalysis(BaseModel):
    """Text structure analysis model"""
    word_count: int
    sentence_count: int
    paragraph_count: int
    avg_sentence_length: float
    complexity_score: int = Field(..., ge=0, le=100)
    
class SourceLink(BaseModel):
    """Source link information"""
    name: str
    description: str
    url: Optional[str] = None
    credibility_rating: Optional[str] = None
    
class ReportingContact(BaseModel):
    """Reporting contact information"""
    description: str
    email: str
    organization: Optional[str] = None
    response_time: Optional[str] = None
    
class FactCheck(BaseModel):
    """Fact check result model"""
    title: str
    url: Optional[str] = None
    publisher: str
    verdict: str
    date: str
    confidence: Optional[float] = None
    
class TextAnalysisRecord(BaseModel):
    """
    Complete text analysis record for database storage
    Migrated from: TruthLens/utils/database.py - analysis record structure
    """
    id: str
    content_preview: str = Field(..., max_length=200)
    full_content: str
    content_type: AnalysisType = AnalysisType.TEXT
    
    # Core Analysis Results
    risk_score: int = Field(..., ge=0, le=100)
    credibility_score: int = Field(..., ge=0, le=100)
    threat_level: ThreatLevel
    
    # Detailed Analysis
    manipulation_tactics: List[str] = []
    ai_analysis: Optional[str] = None
    fact_checks: List[FactCheck] = []
    source_links: List[SourceLink] = []
    reporting_emails: List[ReportingContact] = []
    
    # Enhanced Forensic Analysis (One-in-a-Million features)
    origin_analysis: Optional[str] = None
    context_analysis: Optional[str] = None
    forensic_timeline: List[Dict[str, Any]] = []
    psychological_analysis: Optional[str] = None
    spread_pattern_analysis: Optional[str] = None
    
    # Safety & Structure Analysis
    safety_analysis: Optional[SafetyAnalysis] = None
    structure_analysis: Optional[StructureAnalysis] = None
    
    # Metadata
    user_type: UserType
    analysis_level: str
    language: str
    timestamp: datetime
    last_updated: Optional[datetime] = None
    
    # Authority-specific fields
    priority_level: Optional[str] = None
    assigned_officer: Optional[str] = None
    status: str = "active"  # active, archived, escalated
    
class ImageAnalysisRecord(BaseModel):
    """
    Image analysis record for database storage
    Migrated from: TruthLens/app.py - image analysis functionality
    """
    id: str
    image_name: str
    image_url: Optional[str] = None
    content_type: AnalysisType = AnalysisType.IMAGE
    
    # Image-specific Analysis
    manipulation_score: int = Field(..., ge=0, le=100)
    authenticity_score: int = Field(..., ge=0, le=100)
    threat_level: ThreatLevel
    
    # Image Forensics
    metadata: Dict[str, Any] = {}
    text_content: Optional[str] = None
    reverse_search_results: List[Dict[str, Any]] = []
    technical_analysis: Dict[str, Any] = {}
    
    # Common fields
    user_type: UserType
    timestamp: datetime
    status: str = "active"
    
class SystemStatistics(BaseModel):
    """
    System statistics model
    Migrated from: TruthLens/utils/database.py - statistics structure
    """
    analyzed_today: int = 0
    flagged_content: int = 0
    verified_claims: int = 0
    accuracy_rate: float = 0.0
    
    # Enhanced metrics
    total_analyses: int = 0
    high_risk_content: int = 0
    authority_reports: int = 0
    resolved_cases: int = 0
    
    last_updated: datetime
    
class TrendingThreat(BaseModel):
    """Trending threat information"""
    topic: str
    count: int
    growth: str
    risk: ThreatLevel
    description: Optional[str] = None
    last_seen: datetime
    
class UserActivity(BaseModel):
    """User activity log"""
    timestamp: datetime
    user_type: UserType
    action: str
    content_id: Optional[str] = None
    risk_score: Optional[int] = None
    
class AnalyticsData(BaseModel):
    """
    Analytics data for dashboards
    Migrated from: TruthLens/utils/database.py - analytics structure
    """
    risk_distribution: Dict[str, int] = {}
    daily_counts: List[int] = []
    threat_sources: Dict[str, int] = {}
    hourly_activity: List[int] = []
    top_tactics: List[str] = []
    user_types: Dict[str, int] = {}
    
    # Enhanced analytics
    geographic_distribution: Dict[str, int] = {}
    language_distribution: Dict[str, int] = {}
    platform_distribution: Dict[str, int] = {}
    resolution_times: Dict[str, float] = {}
    
class ReportSubmission(BaseModel):
    """Report submission model"""
    report_id: str
    content_id: str
    report_type: str
    priority: str
    reporter_name: Optional[str] = None
    reporter_email: Optional[str] = None
    additional_info: Optional[str] = None
    organization: str
    status: str = "submitted"  # submitted, under_review, resolved, rejected
    timestamp: datetime
    
class AuthorityUser(BaseModel):
    """Authority user model"""
    username: str
    department: str
    role: str
    permissions: List[str] = []
    last_login: Optional[datetime] = None
    is_active: bool = True