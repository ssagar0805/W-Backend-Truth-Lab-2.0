# Enhanced forensic capabilities - Psychological manipulation tactics analysis
# Part of "One-in-a-Million" features for Truth Lab 2.0

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class TacticsAnalyzer:
    """
    Advanced psychological manipulation tactics analyzer
    Enhanced forensic capability for Truth Lab 2.0
    """
    
    def __init__(self):
        # Comprehensive manipulation tactics database
        self.manipulation_tactics = {
            'emotional_manipulation': {
                'patterns': [
                    r'\b(?:shocking|outrageous|disgusting|terrifying|heartbreaking|infuriating|devastating)\b',
                    r'\b(?:horrified|sickening|appalling|disturbing|traumatic|devastating)\b',
                    r'\b(?:rage|fury|anger|hate|disgust|terror|panic|fear)\b'
                ],
                'description': 'Uses extreme emotional language to bypass rational thinking',
                'psychological_effect': 'Triggers emotional responses that override critical thinking',
                'severity': 'high',
                'counter_strategy': 'Take time to process information emotionally before making decisions'
            },
            
            'urgency_tactics': {
                'patterns': [
                    r'\b(?:urgent|quickly|immediately|act now|before it\'s too late|limited time)\b',
                    r'\b(?:breaking|alert|emergency|crisis|deadline|expires)\b',
                    r'\b(?:hurry|rush|fast|instant|right now|don\'t wait)\b'
                ],
                'description': 'Creates artificial time pressure to prevent careful consideration',
                'psychological_effect': 'Prevents deliberate decision-making through time pressure',
                'severity': 'high',
                'counter_strategy': 'Take time to verify claims regardless of stated urgency'
            },
            
            'authority_appeal': {
                'patterns': [
                    r'\b(?:experts say|scientists confirm|doctors recommend|studies show)\b',
                    r'\b(?:research proves|data shows|statistics reveal|analysis indicates)\b',
                    r'\b(?:according to|as reported by|officials state|sources confirm)\b'
                ],
                'description': 'Claims authority support without providing specific sources',
                'psychological_effect': 'Exploits trust in authority figures and institutions',
                'severity': 'medium',
                'counter_strategy': 'Ask for specific sources and verify their credibility'
            },
            
            'authority_undermining': {
                'patterns': [
                    r'\b(?:mainstream media lies|experts are wrong|don\'t trust|cover-up)\b',
                    r'\b(?:they don\'t want you to know|hidden truth|conspiracy|suppressed)\b',
                    r'\b(?:fake news|propaganda|controlled|manipulated|censored)\b'
                ],
                'description': 'Attacks credible sources to promote alternative narratives',
                'psychological_effect': 'Creates distrust in legitimate authorities and institutions',
                'severity': 'high',
                'counter_strategy': 'Evaluate sources independently and check multiple credible outlets'
            },
            
            'bandwagon_effect': {
                'patterns': [
                    r'\b(?:everyone knows|everybody says|all experts agree|millions believe)\b',
                    r'\b(?:thousands confirm|widely accepted|common knowledge|obvious to all)\b',
                    r'\b(?:join millions|don\'t be left out|everyone is doing|trending)\b'
                ],
                'description': 'Claims widespread acceptance without evidence',
                'psychological_effect': 'Exploits human tendency to conform to perceived group behavior',
                'severity': 'medium',
                'counter_strategy': 'Seek independent verification rather than following crowds'
            },
            
            'false_dichotomy': {
                'patterns': [
                    r'\b(?:either.*or|only two choices|must choose|no other option)\b',
                    r'\b(?:black and white|us vs them|good vs evil|right vs wrong)\b',
                    r'\b(?:with us or against us|no middle ground|simple choice)\b'
                ],
                'description': 'Presents only two options when more exist',
                'psychological_effect': 'Limits critical thinking by oversimplifying complex issues',
                'severity': 'medium',
                'counter_strategy': 'Look for additional options and nuanced perspectives'
            },
            
            'fear_mongering': {
                'patterns': [
                    r'\b(?:dangerous|deadly|toxic|poison|contaminated|fatal)\b',
                    r'\b(?:epidemic|pandemic|outbreak|spreading fast|contagious)\b',
                    r'\b(?:threat|risk|danger|hazard|warning|caution|alarm)\b'
                ],
                'description': 'Exploits fear to motivate behavior or belief changes',
                'psychological_effect': 'Triggers fight-or-flight responses that impair judgment',
                'severity': 'high',
                'counter_strategy': 'Assess actual risk levels using credible data and statistics'
            },
            
            'cherry_picking': {
                'patterns': [
                    r'\b(?:one study shows|a report says|an expert claims|some evidence)\b',
                    r'\b(?:this proves|clearly shows|obviously indicates|demonstrates)\b',
                    r'\b(?:the data shows|statistics prove|numbers don\'t lie)\b'
                ],
                'description': 'Selects only supporting evidence while ignoring contrary data',
                'psychological_effect': 'Creates false impression of scientific consensus',
                'severity': 'medium',
                'counter_strategy': 'Look for systematic reviews and meta-analyses'
            },
            
            'ad_hominem': {
                'patterns': [
                    r'\b(?:stupid|ignorant|naive|foolish|brainwashed|sheep)\b',
                    r'\b(?:corrupt|biased|paid|shill|puppet|controlled)\b',
                    r'\b(?:dishonest|lying|deceiving|manipulating|hiding)\b'
                ],
                'description': 'Attacks the person rather than addressing their arguments',
                'psychological_effect': 'Diverts attention from evidence to personal characteristics',
                'severity': 'medium',
                'counter_strategy': 'Focus on the evidence and arguments, not personal attacks'
            },
            
            'loaded_language': {
                'patterns': [
                    r'\b(?:toxic|evil|corrupt|sinister|malicious|vicious)\b',
                    r'\b(?:pure|innocent|natural|clean|safe|harmless)\b',
                    r'\b(?:freedom|liberty|rights|truth|justice|patriotic)\b'
                ],
                'description': 'Uses emotionally charged words to influence perception',
                'psychological_effect': 'Shapes emotional response through word choice',
                'severity': 'medium',
                'counter_strategy': 'Look past emotional language to underlying facts'
            },
            
            'scarcity_manipulation': {
                'patterns': [
                    r'\b(?:limited time|exclusive|rare|scarce|running out)\b',
                    r'\b(?:only.*left|last chance|won\'t last|disappearing)\b',
                    r'\b(?:special offer|unique opportunity|one-time only)\b'
                ],
                'description': 'Creates false sense of scarcity to motivate immediate action',
                'psychological_effect': 'Triggers loss aversion and impulsive decision-making',
                'severity': 'medium',
                'counter_strategy': 'Research availability and alternatives before acting'
            },
            
            'false_expertise': {
                'patterns': [
                    r'\b(?:as an expert|my research shows|I discovered|my analysis)\b',
                    r'\b(?:trust me|believe me|I know|my experience|insider knowledge)\b',
                    r'\b(?:years of study|extensive research|deep investigation)\b'
                ],
                'description': 'Claims expertise without providing credentials or evidence',
                'psychological_effect': 'Exploits respect for expertise without demonstrating qualifications',
                'severity': 'medium',
                'counter_strategy': 'Verify credentials and look for peer-reviewed work'
            }
        }
        
        # Psychological vulnerability patterns
        self.vulnerability_patterns = {
            'confirmation_bias': [
                r'\b(?:as I always said|proves me right|I knew it|exactly what I thought)\b',
                r'\b(?:confirms|validates|supports what|backs up my)\b'
            ],
            'social_proof': [
                r'\b(?:millions of people|thousands agree|everyone believes|popular opinion)\b',
                r'\b(?:trending|viral|widespread|commonly accepted)\b'
            ],
            'cognitive_dissonance': [
                r'\b(?:don\'t think about|ignore|dismiss|forget about)\b',
                r'\b(?:doesn\'t matter|not important|irrelevant|meaningless)\b'
            ]
        }
        
        # Target audience indicators
        self.audience_patterns = {
            'parents': [
                r'\b(?:your children|kids|babies|infants|toddlers|teenagers)\b',
                r'\b(?:protect your family|child safety|parental rights)\b'
            ],
            'elderly': [
                r'\b(?:seniors|elderly|retirement|social security|medicare)\b',
                r'\b(?:health issues|medical concerns|aging|golden years)\b'
            ],
            'political': [
                r'\b(?:liberals|conservatives|democrats|republicans|government)\b',
                r'\b(?:politics|election|voting|democracy|freedom|rights)\b'
            ],
            'health_conscious': [
                r'\b(?:health|wellness|fitness|nutrition|natural|organic)\b',
                r'\b(?:medicine|treatment|cure|healing|therapy)\b'
            ],
            'financially_stressed': [
                r'\b(?:money|income|debt|bills|expenses|financial)\b',
                r'\b(?:poor|struggling|economic|recession|unemployment)\b'
            ]
        }
    
    async def analyze_manipulation_tactics(self, content: str) -> Dict[str, Any]:
        """
        Comprehensive analysis of manipulation tactics in content
        Enhanced with psychological profiling and spread analysis
        """
        try:
            content_lower = content.lower()
            
            # Detect manipulation tactics
            detected_tactics = await self._detect_tactics(content_lower)
            
            # Analyze psychological targeting
            psychological_analysis = await self._analyze_psychological_targeting(content_lower)
            
            # Identify target audience
            target_analysis = await self._analyze_target_audience(content_lower)
            
            # Analyze spread mechanisms
            spread_analysis = await self._analyze_spread_mechanisms(content_lower)
            
            # Generate overall manipulation score
            manipulation_score = await self._calculate_manipulation_score(detected_tactics)
            
            # Provide counter-strategies
            counter_strategies = await self._generate_counter_strategies(detected_tactics)
            
            return {
                'psychological_analysis': psychological_analysis,
                'advanced_tactics': list(detected_tactics.keys()),
                'spread_analysis': spread_analysis,
                'target_audience': target_analysis,
                'manipulation_score': manipulation_score,
                'detected_tactics_detailed': detected_tactics,
                'counter_strategies': counter_strategies,
                'risk_assessment': await self._assess_manipulation_risk(detected_tactics, manipulation_score)
            }
            
        except Exception as e:
            logger.error(f"Tactics analysis failed: {str(e)}")
            return {
                'psychological_analysis': f"Analysis error: {str(e)}",
                'advanced_tactics': [],
                'spread_analysis': "Analysis unavailable",
                'target_audience': "Unknown",
                'manipulation_score': 0,
                'detected_tactics_detailed': {},
                'counter_strategies': [],
                'risk_assessment': "Unable to assess"
            }
    
    async def _detect_tactics(self, content_lower: str) -> Dict[str, Dict[str, Any]]:
        """Detect specific manipulation tactics in content"""
        detected_tactics = {}
        
        for tactic_name, tactic_info in self.manipulation_tactics.items():
            matches = []
            match_count = 0
            
            for pattern in tactic_info['patterns']:
                pattern_matches = re.findall(pattern, content_lower, re.IGNORECASE)
                if pattern_matches:
                    matches.extend(pattern_matches)
                    match_count += len(pattern_matches)
            
            if match_count > 0:
                detected_tactics[tactic_name] = {
                    'matches': matches[:5],  # Limit displayed matches
                    'count': match_count,
                    'description': tactic_info['description'],
                    'psychological_effect': tactic_info['psychological_effect'],
                    'severity': tactic_info['severity'],
                    'counter_strategy': tactic_info['counter_strategy']
                }
        
        return detected_tactics
    
    async def _analyze_psychological_targeting(self, content_lower: str) -> str:
        """Analyze psychological vulnerabilities being targeted"""
        targeting_analysis = []
        
        # Check for confirmation bias targeting
        for pattern in self.vulnerability_patterns['confirmation_bias']:
            if re.search(pattern, content_lower, re.IGNORECASE):
                targeting_analysis.append("• Confirmation Bias: Reinforces existing beliefs")
                break
        
        # Check for social proof manipulation
        for pattern in self.vulnerability_patterns['social_proof']:
            if re.search(pattern, content_lower, re.IGNORECASE):
                targeting_analysis.append("• Social Proof: Uses perceived popularity as validation")
                break
        
        # Check for cognitive dissonance exploitation
        for pattern in self.vulnerability_patterns['cognitive_dissonance']:
            if re.search(pattern, content_lower, re.IGNORECASE):
                targeting_analysis.append("• Cognitive Dissonance: Encourages ignoring contradictory evidence")
                break
        
        # Analyze emotional state targeting
        emotional_states = {
            'anger': [r'\b(?:angry|furious|outraged|mad|pissed)\b', 'anger'],
            'fear': [r'\b(?:scared|afraid|worried|anxious|terrified)\b', 'fear'],
            'sadness': [r'\b(?:sad|depressed|hopeless|devastated|heartbroken)\b', 'sadness'],
            'greed': [r'\b(?:money|profit|wealth|rich|financial gain)\b', 'greed']
        }
        
        for emotion, (pattern, name) in emotional_states.items():
            if re.search(pattern, content_lower, re.IGNORECASE):
                targeting_analysis.append(f"• Emotional State: Targets {name} for manipulation")
        
        # Analyze decision-making interference
        decision_interference = [
            r'\b(?:don\'t think|just believe|trust blindly|follow orders)\b',
            r'\b(?:no time to research|obvious choice|simple decision)\b'
        ]
        
        for pattern in decision_interference:
            if re.search(pattern, content_lower, re.IGNORECASE):
                targeting_analysis.append("• Decision Interference: Discourages critical thinking")
                break
        
        if not targeting_analysis:
            targeting_analysis.append("• No specific psychological targeting detected")
        
        return "\n".join(targeting_analysis)
    
    async def _analyze_target_audience(self, content_lower: str) -> str:
        """Identify likely target audience based on content patterns"""
        target_scores = {}
        
        for audience, patterns in self.audience_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content_lower, re.IGNORECASE))
                score += matches
            
            if score > 0:
                target_scores[audience] = score
        
        if not target_scores:
            return "General audience - no specific targeting detected"
        
        # Sort by score and return top targets
        sorted_targets = sorted(target_scores.items(), key=lambda x: x[1], reverse=True)
        
        target_analysis = []
        for audience, score in sorted_targets[:3]:  # Top 3 targets
            readable_audience = audience.replace('_', ' ').title()
            target_analysis.append(f"• {readable_audience}: {score} targeting indicators")
        
        return "\n".join(target_analysis)
    
    async def _analyze_spread_mechanisms(self, content_lower: str) -> str:
        """Analyze how content is designed to spread"""
        spread_mechanisms = []
        
        # Viral design patterns
        viral_patterns = {
            'shareability': [
                r'\b(?:share|retweet|forward|send|pass along)\b',
                r'\b(?:tell your friends|spread the word|let others know)\b'
            ],
            'engagement_hooks': [
                r'\b(?:comment below|what do you think|agree or disagree)\b',
                r'\b(?:like if you|share if you agree|retweet if)\b'
            ],
            'controversy': [
                r'\b(?:controversial|shocking|banned|censored|forbidden)\b',
                r'\b(?:they don\'t want|hidden truth|secret information)\b'
            ],
            'urgency_spread': [
                r'\b(?:before it\'s deleted|share quickly|going viral)\b',
                r'\b(?:limited time|disappearing soon|act fast)\b'
            ]
        }
        
        for mechanism, patterns in viral_patterns.items():
            found_patterns = []
            for pattern in patterns:
                matches = re.findall(pattern, content_lower, re.IGNORECASE)
                found_patterns.extend(matches)
            
            if found_patterns:
                readable_mechanism = mechanism.replace('_', ' ').title()
                spread_mechanisms.append(f"• {readable_mechanism}: {', '.join(found_patterns[:3])}")
        
        # Platform-specific spread indicators
        platform_indicators = {
            'social_media': r'\b(?:#\w+|@\w+|hashtag|trending|viral)\b',
            'messaging_apps': r'\b(?:forward|broadcast|group chat|family group)\b',
            'email_chains': r'\b(?:forward this|send to everyone|email your friends)\b'
        }
        
        for platform, pattern in platform_indicators.items():
            if re.search(pattern, content_lower, re.IGNORECASE):
                readable_platform = platform.replace('_', ' ').title()
                spread_mechanisms.append(f"• {readable_platform}: Optimized for platform sharing")
        
        if not spread_mechanisms:
            spread_mechanisms.append("• Standard content sharing patterns")
        
        return "\n".join(spread_mechanisms)
    
    async def _calculate_manipulation_score(self, detected_tactics: Dict[str, Dict[str, Any]]) -> int:
        """Calculate overall manipulation score based on detected tactics"""
        total_score = 0
        
        # Severity weights
        severity_weights = {
            'high': 25,
            'medium': 15,
            'low': 5
        }
        
        for tactic_name, tactic_data in detected_tactics.items():
            severity = tactic_data.get('severity', 'low')
            count = tactic_data.get('count', 0)
            weight = severity_weights.get(severity, 5)
            
            # Score = base weight * count * multiplier
            tactic_score = weight * count * 1.5
            total_score += tactic_score
        
        # Additional scoring factors
        
        # Multiple high-severity tactics (compound effect)
        high_severity_tactics = [t for t in detected_tactics.values() if t.get('severity') == 'high']
        if len(high_severity_tactics) > 2:
            total_score += 30  # Bonus for multiple high-severity tactics
        
        # Specific high-risk combinations
        high_risk_combinations = [
            ('emotional_manipulation', 'urgency_tactics'),
            ('authority_undermining', 'fear_mongering'),
            ('false_expertise', 'authority_appeal')
        ]
        
        for combo in high_risk_combinations:
            if combo[0] in detected_tactics and combo[1] in detected_tactics:
                total_score += 25  # Bonus for dangerous combinations
        
        return min(100, int(total_score))  # Cap at 100
    
    async def _generate_counter_strategies(self, detected_tactics: Dict[str, Dict[str, Any]]) -> List[str]:
        """Generate specific counter-strategies for detected tactics"""
        strategies = []
        
        # Add specific counter-strategies for each detected tactic
        for tactic_name, tactic_data in detected_tactics.items():
            counter_strategy = tactic_data.get('counter_strategy')
            if counter_strategy:
                tactic_readable = tactic_name.replace('_', ' ').title()
                strategies.append(f"• {tactic_readable}: {counter_strategy}")
        
        # Add general strategies if multiple tactics detected
        if len(detected_tactics) > 3:
            strategies.extend([
                "• Multiple Tactics Detected: Use extra caution and verify with multiple sources",
                "• Consider the motivation: Ask who benefits from you believing this information",
                "• Take time: Don't make immediate decisions based on emotional content"
            ])
        
        # Add educational resources
        if any(severity == 'high' for tactic_data in detected_tactics.values() 
               if tactic_data.get('severity') == 'high'):
            strategies.append("• Learn more about manipulation tactics to build resistance")
        
        return strategies if strategies else ["• No specific counter-strategies needed"]
    
    async def _assess_manipulation_risk(self, detected_tactics: Dict[str, Dict[str, Any]], manipulation_score: int) -> str:
        """Assess overall risk level and provide summary"""
        risk_factors = []
        
        # Score-based risk assessment
        if manipulation_score >= 80:
            risk_level = "CRITICAL"
            risk_factors.append("Extremely high manipulation score")
        elif manipulation_score >= 60:
            risk_level = "HIGH"
            risk_factors.append("High manipulation score")
        elif manipulation_score >= 40:
            risk_level = "MEDIUM"
            risk_factors.append("Moderate manipulation indicators")
        else:
            risk_level = "LOW"
            risk_factors.append("Low manipulation score")
        
        # Specific risk factors
        high_severity_count = len([t for t in detected_tactics.values() if t.get('severity') == 'high'])
        if high_severity_count > 0:
            risk_factors.append(f"{high_severity_count} high-severity tactics detected")
        
        total_tactics = len(detected_tactics)
        if total_tactics > 5:
            risk_factors.append(f"Multiple tactics used ({total_tactics} different types)")
        
        # Dangerous combinations
        if 'emotional_manipulation' in detected_tactics and 'urgency_tactics' in detected_tactics:
            risk_factors.append("Emotional manipulation combined with urgency tactics")
        
        if 'authority_undermining' in detected_tactics:
            risk_factors.append("Attempts to undermine credible authorities")
        
        summary = f"Risk Level: {risk_level}\n"
        summary += f"Manipulation Score: {manipulation_score}/100\n"
        summary += f"Risk Factors: {', '.join(risk_factors) if risk_factors else 'None identified'}"
        
        return summary