# Migrated from: TruthLens/utils/security.py - SecurityService class
import re
import hashlib
import logging
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import html
import bleach

logger = logging.getLogger(__name__)

class SecurityService:
    """
    Security service for input validation and content safety
    Migrated from: TruthLens/utils/security.py - SecurityService
    Enhanced with additional security features and async support
    """
    
    def __init__(self):
        self.max_content_length = 10000
        self.blocked_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'data:text/html',
            r'vbscript:',
            r'onload=',
            r'onerror='
        ]
        
        # Authority credentials (in production, this would be in a secure database)
        self.authority_credentials = {
            "admin": {"password": "admin123", "department": "Central Command", "role": "Administrator"},
            "officer1": {"password": "secure456", "department": "Cyber Crime", "role": "Senior Officer"},
            "analyst": {"password": "analyze789", "department": "Intelligence", "role": "Data Analyst"},
            "supervisor": {"password": "super999", "department": "Operations", "role": "Supervisor"}
        }
        
        # Content safety patterns
        self.unsafe_patterns = {
            'violence': [
                r'\b(?:kill|murder|violence|harm|attack|assault)\b',
                r'\b(?:bomb|weapon|gun|knife|explosive)\b'
            ],
            'hate_speech': [
                r'\b(?:hate|racist|discrimination|bigot)\b',
                r'\b(?:nazi|fascist|supremacist)\b'
            ],
            'harassment': [
                r'\b(?:harass|stalk|threaten|intimidate)\b',
                r'\b(?:doxx|dox|expose|leak)\b'
            ],
            'adult_content': [
                r'\b(?:porn|sex|nude|adult|explicit)\b',
                r'\b(?:xxx|nsfw|mature)\b'
            ],
            'spam': [
                r'\b(?:click here|buy now|free money|urgent|limited time)\b',
                r'\b(?:congratulations|winner|prize|lottery)\b'
            ]
        }
        
        # Manipulation patterns for detection
        self.manipulation_patterns = {
            'emotional_manipulation': {
                'patterns': [
                    r'\b(?:shocking|outrageous|disgusting|terrifying|heartbreaking|infuriating)\b',
                    r'\b(?:devastated|horrified|sickening|appalling)\b'
                ],
                'weight': 15
            },
            'urgency_tactics': {
                'patterns': [
                    r'\b(?:urgent|quickly|immediately|act now|before it\'s too late)\b',
                    r'\b(?:breaking|alert|emergency|crisis)\b'
                ],
                'weight': 12
            },
            'authority_undermining': {
                'patterns': [
                    r'\b(?:mainstream media lies|experts are wrong|don\'t trust|cover-up)\b',
                    r'\b(?:they don\'t want you to know|hidden truth|conspiracy)\b'
                ],
                'weight': 18
            },
            'false_consensus': {
                'patterns': [
                    r'\b(?:everyone knows|everybody says|all experts agree)\b',
                    r'\b(?:millions believe|thousands confirm|widely accepted)\b'
                ],
                'weight': 10
            },
            'fear_mongering': {
                'patterns': [
                    r'\b(?:dangerous|deadly|toxic|poison|contaminated)\b',
                    r'\b(?:epidemic|pandemic|outbreak|spreading fast)\b'
                ],
                'weight': 14
            },
            'false_urgency': {
                'patterns': [
                    r'\b(?:share before deleted|going viral|disappearing soon)\b',
                    r'\b(?:limited time|expires today|act fast)\b'
                ],
                'weight': 13
            }
        }
    
    def test_connection(self) -> bool:
        """Test security service availability"""
        return True
    
    def validate_input(self, content: str) -> Tuple[bool, str]:
        """
        Validate input content for security and policy compliance
        Migrated from: TruthLens security validation logic
        """
        
        # Check content length
        if len(content) > self.max_content_length:
            return False, f"Content too long. Maximum {self.max_content_length} characters allowed."
        
        if len(content.strip()) < 10:
            return False, "Content too short. Minimum 10 characters required."
        
        # Check for malicious patterns
        content_lower = content.lower()
        for pattern in self.blocked_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                return False, "Content contains potentially malicious elements."
        
        # Check for excessive repetition (spam indicator)
        words = content.split()
        if len(words) > 0:
            word_counts = {}
            for word in words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            max_repetition = max(word_counts.values())
            if max_repetition > len(words) * 0.3:  # More than 30% repetition
                return False, "Content appears to be spam or excessively repetitive."
        
        return True, "Content validation passed."
    
    def sanitize_input(self, content: str) -> str:
        """
        Sanitize input content to remove potentially harmful elements
        """
        # HTML escape
        sanitized = html.escape(content)
        
        # Remove HTML tags using bleach
        sanitized = bleach.clean(sanitized, tags=[], strip=True)
        
        # Remove excessive whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        return sanitized
    
    def check_content_safety(self, content: str) -> Dict[str, Any]:
        """
        Comprehensive content safety analysis
        Migrated from: TruthLens security analysis functionality
        """
        content_lower = content.lower()
        flagged_categories = []
        flagged_words = []
        safety_score = 100
        
        # Check each safety category
        for category, patterns in self.unsafe_patterns.items():
            category_matches = []
            for pattern in patterns:
                matches = re.findall(pattern, content_lower, re.IGNORECASE)
                if matches:
                    category_matches.extend(matches)
            
            if category_matches:
                flagged_categories.append(category)
                flagged_words.extend(category_matches)
                safety_score -= len(category_matches) * 15  # Reduce score per match
        
        # Additional safety checks
        
        # Check for personal information patterns
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        
        if re.search(email_pattern, content):
            flagged_categories.append('personal_info')
            safety_score -= 10
        
        if re.search(phone_pattern, content):
            flagged_categories.append('personal_info')
            safety_score -= 10
        
        # Check for excessive caps (shouting)
        caps_ratio = sum(1 for c in content if c.isupper()) / len(content) if len(content) > 0 else 0
        if caps_ratio > 0.5:
            flagged_categories.append('aggressive_tone')
            safety_score -= 20
        
        safety_score = max(0, safety_score)
        is_safe = safety_score >= 70 and len(flagged_categories) == 0
        
        return {
            'is_safe': is_safe,
            'safety_score': safety_score,
            'flagged_categories': flagged_categories,
            'flagged_words': list(set(flagged_words)),
            'recommendations': self._generate_safety_recommendations(flagged_categories)
        }
    
    def analyze_text_structure(self, content: str) -> Dict[str, Any]:
        """
        Analyze text structure for manipulation indicators
        """
        # Basic text statistics
        sentences = re.split(r'[.!?]+', content)
        paragraphs = content.split('\n\n')
        words = content.split()
        
        # Calculate metrics
        avg_sentence_length = len(words) / max(len(sentences), 1)
        exclamation_count = content.count('!')
        question_count = content.count('?')
        caps_words = sum(1 for word in words if word.isupper() and len(word) > 1)
        
        # Complexity score (simplified readability)
        complexity_score = min(100, int(avg_sentence_length * 2))
        
        # Structure analysis
        structure_flags = []
        
        if exclamation_count > len(sentences) * 0.3:
            structure_flags.append('excessive_exclamation')
        
        if question_count > len(sentences) * 0.4:
            structure_flags.append('excessive_questions')
        
        if caps_words > len(words) * 0.1:
            structure_flags.append('excessive_capitalization')
        
        if avg_sentence_length > 25:
            structure_flags.append('overly_complex')
        elif avg_sentence_length < 5:
            structure_flags.append('overly_simple')
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': avg_sentence_length,
            'complexity_score': complexity_score,
            'exclamation_count': exclamation_count,
            'question_count': question_count,
            'caps_words': caps_words,
            'structure_flags': structure_flags
        }
    
    def detect_manipulation_patterns(self, content: str) -> Dict[str, Any]:
        """
        Detect psychological manipulation patterns in content
        Migrated from: TruthLens manipulation detection logic
        Enhanced with scoring system
        """
        content_lower = content.lower()
        detected_patterns = {}
        manipulation_score = 0
        
        # Analyze each manipulation category
        for category, config in self.manipulation_patterns.items():
            matches = []
            for pattern in config['patterns']:
                pattern_matches = re.findall(pattern, content_lower, re.IGNORECASE)
                matches.extend(pattern_matches)
            
            if matches:
                detected_patterns[category] = {
                    'matches': matches,
                    'count': len(matches),
                    'weight': config['weight']
                }
                manipulation_score += len(matches) * config['weight']
        
        # Additional manipulation indicators
        
        # Check for unsubstantiated claims
        claim_patterns = [r'\bstudies show\b', r'\bexperts say\b', r'\bresearch proves\b']
        source_patterns = [r'\baccording to\b', r'\bsource:\b', r'\bcited in\b']
        
        has_claims = any(re.search(pattern, content_lower) for pattern in claim_patterns)
        has_sources = any(re.search(pattern, content_lower) for pattern in source_patterns)
        
        if has_claims and not has_sources:
            detected_patterns['unsubstantiated_claims'] = {
                'matches': ['unsourced claims'],
                'count': 1,
                'weight': 20
            }
            manipulation_score += 20
        
        # Check for bandwagon effect
        bandwagon_patterns = [r'\beveryone is doing\b', r'\bdon\'t be left out\b', r'\bjoin millions\b']
        bandwagon_matches = []
        for pattern in bandwagon_patterns:
            matches = re.findall(pattern, content_lower)
            bandwagon_matches.extend(matches)
        
        if bandwagon_matches:
            detected_patterns['bandwagon_effect'] = {
                'matches': bandwagon_matches,
                'count': len(bandwagon_matches),
                'weight': 12
            }
            manipulation_score += len(bandwagon_matches) * 12
        
        manipulation_score = min(100, manipulation_score)
        
        return {
            'patterns': detected_patterns,
            'manipulation_score': manipulation_score,
            'risk_level': 'HIGH' if manipulation_score > 70 else 'MEDIUM' if manipulation_score > 40 else 'LOW',
            'summary': self._generate_manipulation_summary(detected_patterns)
        }
    
    def verify_authority_credentials(self, username: str, password: str) -> bool:
        """
        Verify authority user credentials
        Migrated from: TruthLens authentication logic
        """
        if username in self.authority_credentials:
            stored_password = self.authority_credentials[username]['password']
            return password == stored_password
        return False
    
    def get_authority_info(self, username: str) -> Dict[str, str]:
        """Get authority user information"""
        if username in self.authority_credentials:
            user_info = self.authority_credentials[username].copy()
            user_info.pop('password', None)  # Remove password from response
            return user_info
        return {'department': 'Unknown', 'role': 'Unknown'}
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events for monitoring"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details
        }
        logger.info(f"Security event: {event}")
    
    def _generate_safety_recommendations(self, flagged_categories: List[str]) -> List[str]:
        """Generate safety recommendations based on flagged content"""
        recommendations = []
        
        if 'violence' in flagged_categories:
            recommendations.append("Content contains violent language or threats")
        if 'hate_speech' in flagged_categories:
            recommendations.append("Content may contain hate speech or discriminatory language")
        if 'harassment' in flagged_categories:
            recommendations.append("Content may constitute harassment or intimidation")
        if 'adult_content' in flagged_categories:
            recommendations.append("Content may not be suitable for all audiences")
        if 'spam' in flagged_categories:
            recommendations.append("Content appears to be promotional or spam")
        if 'personal_info' in flagged_categories:
            recommendations.append("Content may contain personal information")
        if 'aggressive_tone' in flagged_categories:
            recommendations.append("Content uses aggressive or confrontational tone")
        
        return recommendations
    
    def _generate_manipulation_summary(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate summary of manipulation tactics detected"""
        summary = []
        
        for category, data in patterns.items():
            readable_name = category.replace('_', ' ').title()
            count = data['count']
            if count == 1:
                summary.append(f"{readable_name} detected")
            else:
                summary.append(f"{readable_name} detected ({count} instances)")
        
        return summary

# FastAPI dependency for request validation
async def validate_request(request_data: dict = None) -> dict:
    """FastAPI dependency for request validation"""
    # This would contain request-level validation logic
    # For now, we'll just pass through
    return request_data or {}