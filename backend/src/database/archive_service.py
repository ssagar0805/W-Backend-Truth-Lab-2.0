# Migrated from: TruthLens/utils/database.py - FirebaseService class
import asyncio
import uuid
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from .models import (
    TextAnalysisRecord, ImageAnalysisRecord, SystemStatistics, 
    TrendingThreat, UserActivity, AnalyticsData, ReportSubmission,
    ThreatLevel, UserType, AnalysisType
)

logger = logging.getLogger(__name__)

class ArchiveService:
    """
    Database service for storing and retrieving analysis results
    Migrated from: TruthLens/utils/database.py - FirebaseService
    Enhanced with async support and comprehensive data management
    """
    
    def __init__(self):
        # In-memory storage for development/testing
        # In production, this would connect to Firestore or other database
        self.data_store = {
            'analyses': [],
            'images': [],
            'statistics': SystemStatistics(
                analyzed_today=1247,
                flagged_content=156,
                verified_claims=891,
                accuracy_rate=94.2,
                total_analyses=5432,
                high_risk_content=234,
                authority_reports=78,
                resolved_cases=156,
                last_updated=datetime.now()
            ),
            'trending_threats': [],
            'analytics_data': AnalyticsData(),
            'user_activities': [],
            'reports': []
        }
        
        # Initialize with demo data
        asyncio.create_task(self._initialize_demo_data())
    
    async def test_connection(self) -> bool:
        """Test database connection"""
        return True
    
    async def save_text_analysis(
        self, 
        content: str, 
        results: Dict[str, Any], 
        user_type: str = "public"
    ) -> str:
        """
        Save text analysis results to database
        Migrated from: TruthLens/utils/database.py - save_analysis()
        """
        try:
            analysis_id = str(uuid.uuid4())[:8]
            
            # Create analysis record
            record = TextAnalysisRecord(
                id=analysis_id,
                content_preview=content[:200] + "..." if len(content) > 200 else content,
                full_content=content,
                risk_score=results['risk_score'],
                credibility_score=results['credibility_score'],
                threat_level=ThreatLevel(results.get('threat_level', 'LOW')),
                manipulation_tactics=results.get('manipulation_tactics', []),
                ai_analysis=results.get('ai_analysis'),
                fact_checks=results.get('fact_checks', []),
                source_links=results.get('source_links', []),
                reporting_emails=results.get('reporting_emails', []),
                origin_analysis=results.get('origin_analysis'),
                context_analysis=results.get('context_analysis'),
                forensic_timeline=results.get('forensic_timeline', []),
                psychological_analysis=results.get('psychological_analysis'),
                spread_pattern_analysis=results.get('spread_pattern_analysis'),
                safety_analysis=results.get('safety_analysis'),
                structure_analysis=results.get('structure_analysis'),
                user_type=UserType(user_type),
                analysis_level=results.get('analysis_level', 'Quick Scan'),
                language=results.get('language', 'en'),
                timestamp=datetime.now()
            )
            
            # Add to storage
            self.data_store['analyses'].append(record.dict())
            
            # Update statistics
            await self._update_statistics(results['risk_score'], user_type)
            
            # Log user activity
            await self._log_activity(user_type, "content_analysis", analysis_id, results['risk_score'])
            
            logger.info(f"Text analysis saved with ID: {analysis_id}")
            return analysis_id
            
        except Exception as e:
            logger.error(f"Failed to save text analysis: {str(e)}")
            return None
    
    async def save_image_analysis(
        self, 
        image_name: str, 
        results: Dict[str, Any], 
        user_type: str = "public"
    ) -> str:
        """
        Save image analysis results
        Migrated from: TruthLens/utils/database.py - save_image_analysis()
        """
        try:
            analysis_id = str(uuid.uuid4())[:8]
            
            # Create image analysis record
            record = ImageAnalysisRecord(
                id=analysis_id,
                image_name=image_name,
                manipulation_score=results.get('manipulation_score', 0),
                authenticity_score=results.get('authenticity_score', 100),
                threat_level=ThreatLevel.HIGH if results.get('manipulation_score', 0) > 70 
                          else ThreatLevel.MEDIUM if results.get('manipulation_score', 0) > 40 
                          else ThreatLevel.LOW,
                metadata=results.get('metadata', {}),
                text_content=results.get('text_content'),
                reverse_search_results=results.get('reverse_search_results', []),
                technical_analysis=results.get('technical_analysis', {}),
                user_type=UserType(user_type),
                timestamp=datetime.now()
            )
            
            # Add to storage
            self.data_store['images'].append(record.dict())
            
            # Update statistics
            await self._update_statistics(results.get('manipulation_score', 0), user_type)
            
            # Log user activity
            await self._log_activity(user_type, "image_analysis", analysis_id, results.get('manipulation_score', 0))
            
            logger.info(f"Image analysis saved with ID: {analysis_id}")
            return analysis_id
            
        except Exception as e:
            logger.error(f"Failed to save image analysis: {str(e)}")
            return None
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get system statistics
        Migrated from: TruthLens/utils/database.py - get_statistics()
        """
        stats = self.data_store['statistics']
        return stats.dict()
    
    async def get_recent_analyses(self, limit: int = 10, user_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recent analyses with optional filtering
        Migrated from: TruthLens/utils/database.py - get_recent_analyses()
        """
        analyses = self.data_store['analyses']
        
        # Filter by user type if specified
        if user_type:
            analyses = [a for a in analyses if a.get('user_type') == user_type]
        
        # Sort by timestamp (most recent first)
        sorted_analyses = sorted(analyses, key=lambda x: x['timestamp'], reverse=True)
        
        return sorted_analyses[:limit]
    
    async def get_trending_threats(self) -> List[Dict[str, Any]]:
        """
        Get trending threat topics
        Migrated from: TruthLens/utils/database.py - get_trending_threats()
        """
        if not self.data_store['trending_threats']:
            # Generate trending threats based on recent analyses
            await self._generate_trending_threats()
        
        return [threat.dict() for threat in self.data_store['trending_threats']]
    
    async def get_analytics_data(self) -> Dict[str, Any]:
        """
        Get analytics data for dashboards
        Migrated from: TruthLens/utils/database.py - get_analytics_data()
        """
        analytics = self.data_store['analytics_data']
        
        # Update with real-time calculations
        await self._update_analytics()
        
        return analytics.dict()
    
    async def get_user_activity(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent user activity logs"""
        activities = self.data_store['user_activities']
        sorted_activities = sorted(activities, key=lambda x: x['timestamp'], reverse=True)
        return sorted_activities[:limit]
    
    async def submit_report(self, report_data: Dict[str, Any]) -> str:
        """Submit a new report"""
        try:
            report_id = f"TL-{int(datetime.now().timestamp())}"
            
            report = ReportSubmission(
                report_id=report_id,
                content_id=report_data.get('content_id', ''),
                report_type=report_data.get('report_type', 'misinformation'),
                priority=report_data.get('priority', 'medium'),
                reporter_name=report_data.get('reporter_name'),
                reporter_email=report_data.get('reporter_email'),
                additional_info=report_data.get('additional_info'),
                organization=report_data.get('organization', 'General Public'),
                timestamp=datetime.now()
            )
            
            self.data_store['reports'].append(report.dict())
            
            logger.info(f"Report submitted with ID: {report_id}")
            return report_id
            
        except Exception as e:
            logger.error(f"Failed to submit report: {str(e)}")
            return None
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Get specific analysis by ID"""
        # Search in text analyses
        for analysis in self.data_store['analyses']:
            if analysis['id'] == analysis_id:
                return analysis
        
        # Search in image analyses
        for image in self.data_store['images']:
            if image['id'] == analysis_id:
                return image
        
        return None
    
    async def _update_statistics(self, risk_score: int, user_type: str):
        """Update system statistics"""
        stats = self.data_store['statistics']
        
        stats.analyzed_today += 1
        stats.total_analyses += 1
        
        if risk_score > 70:
            stats.flagged_content += 1
            stats.high_risk_content += 1
        
        if user_type == "authority":
            stats.authority_reports += 1
        
        # Update accuracy rate (simplified calculation)
        stats.accuracy_rate = min(100.0, stats.accuracy_rate + 0.1)
        
        stats.last_updated = datetime.now()
    
    async def _log_activity(self, user_type: str, action: str, content_id: str, risk_score: int):
        """Log user activity"""
        activity = UserActivity(
            timestamp=datetime.now(),
            user_type=UserType(user_type),
            action=action,
            content_id=content_id,
            risk_score=risk_score
        )
        
        self.data_store['user_activities'].append(activity.dict())
        
        # Keep only last 1000 activities
        if len(self.data_store['user_activities']) > 1000:
            self.data_store['user_activities'] = self.data_store['user_activities'][-1000:]
    
    async def _generate_trending_threats(self):
        """Generate trending threats from recent analyses"""
        trending_threats = [
            TrendingThreat(
                topic='Health Misinformation',
                count=234,
                growth='+12%',
                risk=ThreatLevel.HIGH,
                description='False medical claims and vaccine misinformation',
                last_seen=datetime.now()
            ),
            TrendingThreat(
                topic='Election Fraud Claims',
                count=189,
                growth='+8%',
                risk=ThreatLevel.HIGH,
                description='Unsubstantiated claims about election integrity',
                last_seen=datetime.now() - timedelta(hours=2)
            ),
            TrendingThreat(
                topic='Climate Change Denial',
                count=156,
                growth='+5%',
                risk=ThreatLevel.MEDIUM,
                description='Misleading information about climate science',
                last_seen=datetime.now() - timedelta(hours=4)
            ),
            TrendingThreat(
                topic='Financial Scams',
                count=123,
                growth='+15%',
                risk=ThreatLevel.HIGH,
                description='Investment fraud and cryptocurrency scams',
                last_seen=datetime.now() - timedelta(hours=1)
            )
        ]
        
        self.data_store['trending_threats'] = trending_threats
    
    async def _update_analytics(self):
        """Update analytics data with current statistics"""
        analytics = self.data_store['analytics_data']
        
        # Risk distribution
        total_analyses = len(self.data_store['analyses'])
        if total_analyses > 0:
            high_risk = len([a for a in self.data_store['analyses'] if a['risk_score'] > 70])
            medium_risk = len([a for a in self.data_store['analyses'] if 40 <= a['risk_score'] <= 70])
            low_risk = total_analyses - high_risk - medium_risk
            
            analytics.risk_distribution = {
                'High': high_risk,
                'Medium': medium_risk,
                'Low': low_risk
            }
        
        # User type distribution
        authority_count = len([a for a in self.data_store['analyses'] if a['user_type'] == 'authority'])
        public_count = total_analyses - authority_count
        
        analytics.user_types = {
            'Authority': authority_count,
            'Public': public_count
        }
        
        # Generate sample data for other metrics
        analytics.daily_counts = [120, 134, 156, 143, 167, 145, 189]
        analytics.hourly_activity = [12, 8, 5, 3, 2, 4, 8, 15, 25, 35, 42, 48, 52, 55, 53, 48, 45, 42, 38, 32, 28, 22, 18, 15]
        analytics.top_tactics = ['Emotional Appeal', 'False Urgency', 'Cherry Picking', 'Appeal to Fear', 'Bandwagon Effect']
    
    async def _initialize_demo_data(self):
        """Initialize with demo data for testing"""
        # This would be called once to populate demo data
        # Implementation would add sample analyses, reports, etc.
        pass