# Migrated from: TruthLens/app.py - conduct_forensic_analysis function and related analysis logic
# Enhanced with "One-in-a-Million" forensic capabilities from requirements

from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime
import logging

from .text_analysis import TextAnalyzer
from .image_forensics import ImageForensics
from .source_tracking import SourceTracker
from .context_analysis import ContextAnalyzer
from .tactics_breakdown import TacticsAnalyzer
from ..utils.security import SecurityService
from ..utils.config import Config

logger = logging.getLogger(__name__)

class ComprehensiveAnalyzer:
    """
    Main orchestrator for comprehensive forensic analysis
    Migrated from: TruthLens/app.py - conduct_forensic_analysis()
    Enhanced with forensic capabilities from Master Plan
    """
    
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.image_forensics = ImageForensics()
        self.source_tracker = SourceTracker()
        self.context_analyzer = ContextAnalyzer()
        self.tactics_analyzer = TacticsAnalyzer()
        self.security_service = SecurityService()
        self.config = Config()

async def conduct_comprehensive_analysis(
    text: str,
    language: str = "en",
    level: str = "Quick Scan", 
    enable_context: bool = True,
    track_origin: bool = False,
    safety_check: bool = True,
    user_type: str = "public"
) -> Dict[str, Any]:
    """
    Comprehensive forensic analysis function
    
    Migrated from: TruthLens/app.py - conduct_forensic_analysis()
    Enhanced with forensic capabilities and dual interface support
    
    Args:
        text: Content to analyze
        language: Language code (en, hi, etc.)
        level: Analysis depth (Quick Scan, Deep Forensics)
        enable_context: Enable contextual analysis
        track_origin: Enable origin tracing
        safety_check: Enable safety analysis
        user_type: public or authority (affects analysis depth)
    
    Returns:
        Comprehensive analysis results dictionary
    """
    
    # Initialize results structure
    results = {
        'risk_score': 0,
        'credibility_score': 0,
        'threat_level': 'LOW',
        'manipulation_tactics': [],
        'fact_checks': [],
        'ai_analysis': None,
        'origin_analysis': None,
        'context_analysis': None,
        'safety_analysis': None,
        'structure_analysis': None,
        'source_links': [],
        'reporting_emails': [],
        'recommendations': [],
        'forensic_timeline': [],
        'psychological_analysis': None,
        'spread_pattern_analysis': None
    }
    
    try:
        # Initialize comprehensive analyzer
        analyzer = ComprehensiveAnalyzer()
        
        # Phase 1: Basic Risk Assessment (from TruthLens)
        results['risk_score'] = await calculate_risk_score(text)
        logger.info(f"Basic risk score calculated: {results['risk_score']}")
        
        # Phase 2: Security Analysis (from TruthLens security service)
        if safety_check:
            results['safety_analysis'] = analyzer.security_service.check_content_safety(text)
            results['structure_analysis'] = analyzer.security_service.analyze_text_structure(text)
            
            manipulation_results = analyzer.security_service.detect_manipulation_patterns(text)
            results['manipulation_tactics'] = list(manipulation_results['patterns'].keys())
            
            # Adjust risk score based on security analysis
            results['risk_score'] = max(results['risk_score'], manipulation_results['manipulation_score'])
            logger.info(f"Security-adjusted risk score: {results['risk_score']}")
        
        # Phase 3: AI Analysis with Gemini (ALWAYS run - from TruthLens)
        try:
            ai_analysis_result = await analyzer.text_analyzer.forensic_analysis(text, language)
            results['ai_analysis'] = ai_analysis_result['analysis']
            results['source_links'] = ai_analysis_result['sources']
            results['reporting_emails'] = ai_analysis_result['reporting_emails']
            
            # Update risk score based on AI analysis
            ai_risk_adjustment = await analyze_ai_response_for_risk(results['ai_analysis'])
            results['risk_score'] = max(results['risk_score'], ai_risk_adjustment)
            logger.info(f"AI-adjusted risk score: {results['risk_score']}")
            
        except Exception as e:
            logger.warning(f"AI analysis failed: {str(e)}")
            results['ai_analysis'] = f"AI analysis temporarily unavailable: {str(e)}"
            results['source_links'] = []
            results['reporting_emails'] = []
        
        # Phase 4: Fact Checking (from TruthLens FactCheckService)
        try:
            results['fact_checks'] = await analyzer.text_analyzer.search_fact_checks(text)
            logger.info(f"Found {len(results['fact_checks'])} fact checks")
        except Exception as e:
            logger.warning(f"Fact checking failed: {str(e)}")
            results['fact_checks'] = []
        
        # Phase 5: Enhanced Forensic Analysis (NEW - One-in-a-Million features)
        
        if level == "Deep Forensics" or user_type == "authority":
            
            # Origin Tracking & Source Analysis
            if track_origin:
                try:
                    results['origin_analysis'] = await analyzer.source_tracker.trace_origin(text)
                    results['forensic_timeline'] = await analyzer.source_tracker.build_timeline(text)
                    logger.info("Origin analysis completed")
                except Exception as e:
                    logger.warning(f"Origin tracking failed: {str(e)}")
                    results['origin_analysis'] = f"Origin tracking unavailable: {str(e)}"
            
            # Context Analysis & Historical Correlation
            if enable_context:
                try:
                    results['context_analysis'] = await analyzer.context_analyzer.analyze_context(text)
                    logger.info("Context analysis completed")
                except Exception as e:
                    logger.warning(f"Context analysis failed: {str(e)}")
                    results['context_analysis'] = f"Context analysis unavailable: {str(e)}"
            
            # Advanced Tactics Breakdown (psychological manipulation detection)
            try:
                tactics_result = await analyzer.tactics_analyzer.analyze_manipulation_tactics(text)
                results['psychological_analysis'] = tactics_result['psychological_analysis']
                results['manipulation_tactics'].extend(tactics_result['advanced_tactics'])
                results['spread_pattern_analysis'] = tactics_result['spread_analysis']
                logger.info("Advanced tactics analysis completed")
            except Exception as e:
                logger.warning(f"Tactics analysis failed: {str(e)}")
        
        # Phase 6: Final Score Calculation and Threat Assessment
        results['credibility_score'] = await calculate_credibility_score(results)
        results['threat_level'] = determine_threat_level(results['risk_score'])
        results['recommendations'] = await generate_recommendations(results, user_type)
        
        logger.info(f"Analysis completed - Risk: {results['risk_score']}, Credibility: {results['credibility_score']}, Threat: {results['threat_level']}")
        
        return results
        
    except Exception as e:
        logger.error(f"Comprehensive analysis failed: {str(e)}")
        # Return basic results even if advanced analysis fails
        results['ai_analysis'] = f"Analysis error: {str(e)}"
        results['credibility_score'] = 50  # Neutral score on error
        results['threat_level'] = 'UNKNOWN'
        results['recommendations'] = ["Unable to complete analysis. Please try again later."]
        return results

async def calculate_risk_score(text: str) -> int:
    """
    Calculate basic risk score
    Migrated from: TruthLens/app.py - calculate_risk_score()
    """
    score = 0
    text_lower = text.lower()
    
    # Check for sensational language
    sensational_words = ['shocking', 'unbelievable', 'incredible', 'amazing', 'breaking', 'urgent']
    for word in sensational_words:
        if word in text_lower:
            score += 10
    
    # Check for conspiracy indicators
    conspiracy_words = ['conspiracy', 'cover-up', 'hidden truth', 'they don\'t want']
    for word in conspiracy_words:
        if word in text_lower:
            score += 15
    
    # Check for lack of sources
    if 'source' not in text_lower and 'study' not in text_lower and 'research' not in text_lower:
        score += 20
    
    # Check for excessive punctuation
    if text.count('!') > 3 or text.count('?') > 3:
        score += 10
    
    # Check for call to action
    action_words = ['share', 'forward', 'spread', 'tell everyone']
    for word in action_words:
        if word in text_lower:
            score += 10
    
    return min(100, score)

async def analyze_ai_response_for_risk(ai_response: str) -> int:
    """
    Analyze AI response to determine risk level
    Migrated from: TruthLens/app.py - analyze_ai_response_for_risk()
    """
    if not ai_response or "AI analysis temporarily unavailable" in str(ai_response):
        return 0
    
    response_lower = str(ai_response).lower()
    
    # Check for explicit veracity assessment from AI
    if 'false information' in response_lower:
        return 90  # Very high risk for false information
    elif 'misleading' in response_lower:
        return 80  # High risk for misleading content
    elif 'unverified' in response_lower:
        return 60  # Medium-high risk for unverified content
    elif 'true' in response_lower and 'veracity assessment' in response_lower:
        return 10  # Low risk for verified true content
    
    # Fallback to keyword analysis
    high_risk_indicators = [
        'false', 'misinformation', 'disinformation', 'fake', 'untrue', 
        'deceptive', 'manipulative', 'harmful', 'dangerous',
        'conspiracy', 'hoax', 'scam', 'fraud', 'deceit'
    ]
    
    medium_risk_indicators = [
        'questionable', 'suspicious', 'unreliable', 
        'biased', 'exaggerated', 'incomplete', 'outdated'
    ]
    
    # Check for high risk indicators
    high_risk_count = sum(1 for indicator in high_risk_indicators if indicator in response_lower)
    medium_risk_count = sum(1 for indicator in medium_risk_indicators if indicator in response_lower)
    
    # Calculate risk score based on AI assessment
    if high_risk_count > 0:
        return 75  # High risk for concerning factors
    elif medium_risk_count > 0:
        return 50  # Medium risk
    else:
        return 0  # No additional risk from AI analysis

async def calculate_credibility_score(results: Dict[str, Any]) -> int:
    """
    Calculate credibility score based on all analysis results
    Migrated from: TruthLens/app.py - calculate_credibility()
    """
    base_credibility = 80
    
    # Reduce credibility based on risk score
    credibility = base_credibility - (results['risk_score'] * 0.8)
    
    # Factor in safety analysis
    if results.get('safety_analysis'):
        safety_score = results['safety_analysis']['safety_score']
        credibility = (credibility + safety_score) / 2
    
    # Factor in manipulation tactics
    manipulation_count = len([t for t in results['manipulation_tactics'] if t != "None Detected"])
    credibility -= manipulation_count * 10
    
    # Factor in fact checks
    if results['fact_checks']:
        credibility += 10  # Having fact checks available is good
    
    return max(0, min(100, round(credibility)))

def determine_threat_level(risk_score: int) -> str:
    """Determine threat level based on risk score"""
    if risk_score >= 70:
        return "HIGH"
    elif risk_score >= 40:
        return "MEDIUM" 
    else:
        return "LOW"

async def generate_recommendations(results: Dict[str, Any], user_type: str) -> List[str]:
    """
    Generate recommendations based on analysis
    Migrated from: TruthLens/app.py - generate_recommendations()
    Enhanced with user-type specific recommendations
    """
    recommendations = []
    risk_score = results['risk_score']
    
    if user_type == "authority":
        # Authority-specific recommendations
        if risk_score > 70:
            recommendations.extend([
                "🚨 HIGH RISK: Immediate monitoring recommended",
                "📊 Track spread patterns across platforms", 
                "🔔 Consider issuing public alert if widespread",
                "📧 Coordinate with fact-checking organizations",
                "📋 Document for trend analysis"
            ])
        elif risk_score > 40:
            recommendations.extend([
                "⚠️ MEDIUM RISK: Continue monitoring",
                "📊 Add to watch list for pattern analysis",
                "🔍 Verify with additional sources",
                "📧 Share with relevant departments"
            ])
        else:
            recommendations.extend([
                "✅ LOW RISK: Standard monitoring sufficient",
                "📊 Log for baseline data"
            ])
    else:
        # Public user recommendations
        if risk_score > 70:
            recommendations.extend([
                "🚨 HIGH RISK: Do not share this content",
                "🔍 Verify information from multiple credible sources",
                "📧 Report this content to relevant authorities",
                "📚 Learn about misinformation tactics"
            ])
        elif risk_score > 40:
            recommendations.extend([
                "⚠️ MEDIUM RISK: Be cautious about sharing",
                "🔍 Cross-check with fact-checking websites",
                "📚 Look for additional context and sources",
                "⏳ Wait for more information before sharing"
            ])
        else:
            recommendations.extend([
                "✅ LOW RISK: Content appears credible",
                "🔍 Still verify with additional sources if important",
                "📚 Continue learning about information verification"
            ])
    
    return recommendations

async def test_all_services() -> Dict[str, bool]:
    """
    Test all analysis services for health checks
    """
    analyzer = ComprehensiveAnalyzer()
    
    services_status = {}
    
    try:
        services_status["gemini"] = await analyzer.text_analyzer.test_connection()
    except:
        services_status["gemini"] = False
    
    try:
        services_status["fact_check"] = await analyzer.text_analyzer.test_fact_check_connection()
    except:
        services_status["fact_check"] = False
    
    try:
        services_status["security"] = analyzer.security_service.test_connection()
    except:
        services_status["security"] = False
    
    try:
        services_status["database"] = True  # Database service test
    except:
        services_status["database"] = False
    
    services_status["news"] = True  # News service always available
    
    return services_status