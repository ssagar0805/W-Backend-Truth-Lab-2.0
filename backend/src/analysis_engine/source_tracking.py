# Enhanced forensic capabilities - Source tracking and origin analysis
# Part of "One-in-a-Million" features for Truth Lab 2.0

import asyncio
import aiohttp
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from urllib.parse import urlparse

from ..utils.config import Config

logger = logging.getLogger(__name__)

class SourceTracker:
    """
    Advanced source tracking and origin analysis
    Enhanced forensic capability for Truth Lab 2.0
    """
    
    def __init__(self):
        self.config = Config()
        
        # Reverse image search engines
        self.search_engines = {
            "google": "https://www.google.com/searchbyimage",
            "tineye": "https://tineye.com/search",
            "yandex": "https://yandex.com/images/search"
        }
        
        # Known misinformation sources and their patterns
        self.suspicious_domains = [
            'fakenews.com', 'conspiracy.net', 'truthexposed.info',
            'alternative-facts.org', 'realtruth.blog', 'hidden-news.site'
        ]
        
        # Platform-specific patterns for content identification
        self.platform_patterns = {
            'twitter': [
                r'@\w+',  # mentions
                r'#\w+',  # hashtags
                r'RT\s+@',  # retweets
                r'twitter\.com/\w+/status/\d+'  # twitter URLs
            ],
            'facebook': [
                r'facebook\.com/\w+',
                r'fb\.me/\w+',
                r'\bFB\b',
                r'shared a post'
            ],
            'instagram': [
                r'instagram\.com/p/\w+',
                r'instagr\.am/p/\w+',
                r'#\w+',  # hashtags common on Instagram
                r'@\w+'   # mentions
            ],
            'whatsapp': [
                r'forwarded message',
                r'forward this',
                r'share with everyone',
                r'wa\.me/\w+'
            ],
            'telegram': [
                r't\.me/\w+',
                r'telegram\.me/\w+',
                r'channel:',
                r'@\w+channel'
            ],
            'youtube': [
                r'youtube\.com/watch\?v=\w+',
                r'youtu\.be/\w+',
                r'subscribe to my channel',
                r'like and subscribe'
            ],
            'tiktok': [
                r'tiktok\.com/@\w+',
                r'#fyp',
                r'#foryou',
                r'viral on TikTok'
            ]
        }
    
    async def trace_origin(self, content: str) -> str:
        """
        Comprehensive origin tracing using multiple techniques
        Enhanced with forensic timeline and spread pattern analysis
        """
        try:
            analysis_results = []
            
            # Platform identification
            platform_analysis = await self._identify_platform_origins(content)
            if platform_analysis:
                analysis_results.append(f"🔍 PLATFORM ANALYSIS:\n{platform_analysis}")
            
            # Linguistic forensics
            linguistic_analysis = await self._analyze_linguistic_patterns(content)
            if linguistic_analysis:
                analysis_results.append(f"🗣️ LINGUISTIC FORENSICS:\n{linguistic_analysis}")
            
            # Temporal analysis
            temporal_analysis = await self._analyze_temporal_patterns(content)
            if temporal_analysis:
                analysis_results.append(f"⏰ TEMPORAL ANALYSIS:\n{temporal_analysis}")
            
            # URL and domain analysis
            domain_analysis = await self._analyze_domains_and_urls(content)
            if domain_analysis:
                analysis_results.append(f"🌐 DOMAIN ANALYSIS:\n{domain_analysis}")
            
            # Content propagation patterns
            propagation_analysis = await self._analyze_propagation_patterns(content)
            if propagation_analysis:
                analysis_results.append(f"📈 PROPAGATION ANALYSIS:\n{propagation_analysis}")
            
            # Content fingerprinting
            fingerprint_analysis = await self._generate_content_fingerprint(content)
            if fingerprint_analysis:
                analysis_results.append(f"🔐 CONTENT FINGERPRINT:\n{fingerprint_analysis}")
            
            return "\n\n".join(analysis_results) if analysis_results else "Origin analysis completed - no specific patterns detected"
            
        except Exception as e:
            logger.error(f"Origin tracing failed: {str(e)}")
            return f"Origin analysis error: {str(e)}"
    
    async def build_timeline(self, content: str) -> List[Dict[str, Any]]:
        """
        Build forensic timeline of content spread
        Enhanced capability for tracking misinformation lifecycle
        """
        timeline_events = []
        
        try:
            # Extract temporal references
            temporal_refs = await self._extract_temporal_references(content)
            
            for ref in temporal_refs:
                event = {
                    'timestamp': ref.get('timestamp'),
                    'event_type': ref.get('type', 'content_reference'),
                    'description': ref.get('description'),
                    'confidence': ref.get('confidence', 0.5),
                    'source': 'content_analysis'
                }
                timeline_events.append(event)
            
            # Add platform-specific timeline markers
            platform_events = await self._extract_platform_timeline(content)
            timeline_events.extend(platform_events)
            
            # Sort by timestamp
            timeline_events.sort(key=lambda x: x.get('timestamp', datetime.min))
            
            return timeline_events
            
        except Exception as e:
            logger.error(f"Timeline building failed: {str(e)}")
            return []
    
    async def reverse_image_search(self, image_url: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Perform reverse image search across multiple engines
        """
        results = {}
        
        try:
            # Simulate reverse image search results
            # In production, this would make actual API calls
            
            engines = ['google', 'tineye', 'yandex']
            
            for engine in engines:
                engine_results = await self._simulate_reverse_search(image_url, engine)
                results[engine] = engine_results
            
            return results
            
        except Exception as e:
            logger.error(f"Reverse image search failed: {str(e)}")
            return {}
    
    async def _identify_platform_origins(self, content: str) -> str:
        """Identify likely platform origins based on content patterns"""
        content_lower = content.lower()
        platform_scores = {}
        
        for platform, patterns in self.platform_patterns.items():
            score = 0
            matches = []
            
            for pattern in patterns:
                pattern_matches = re.findall(pattern, content_lower, re.IGNORECASE)
                if pattern_matches:
                    matches.extend(pattern_matches)
                    score += len(pattern_matches)
            
            if score > 0:
                platform_scores[platform] = {
                    'score': score,
                    'matches': matches[:5]  # Limit matches shown
                }
        
        if not platform_scores:
            return "No specific platform patterns detected"
        
        # Sort by score
        sorted_platforms = sorted(platform_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        analysis = []
        for platform, data in sorted_platforms[:3]:  # Top 3 platforms
            match_text = ", ".join(data['matches'][:3])
            analysis.append(f"• {platform.title()}: {data['score']} indicators ({match_text}...)")
        
        return "\n".join(analysis)
    
    async def _analyze_linguistic_patterns(self, content: str) -> str:
        """Analyze linguistic patterns for geographic and demographic clues"""
        patterns = []
        
        # Spelling patterns (US vs UK vs other)
        us_spellings = ['color', 'honor', 'center', 'defense', 'analyze']
        uk_spellings = ['colour', 'honour', 'centre', 'defence', 'analyse']
        
        us_count = sum(1 for word in us_spellings if word in content.lower())
        uk_count = sum(1 for word in uk_spellings if word in content.lower())
        
        if us_count > uk_count and us_count > 0:
            patterns.append("• American English spelling patterns detected")
        elif uk_count > us_count and uk_count > 0:
            patterns.append("• British English spelling patterns detected")
        
        # Colloquialisms and regional expressions
        regional_expressions = {
            'american': ['y\'all', 'gonna', 'wanna', 'awesome', 'dude'],
            'british': ['bloody', 'brilliant', 'mate', 'cheers', 'bloke'],
            'australian': ['mate', 'g\'day', 'bloody', 'fair dinkum'],
            'indian': ['prepone', 'good name', 'out of station', 'do the needful']
        }
        
        for region, expressions in regional_expressions.items():
            matches = [expr for expr in expressions if expr in content.lower()]
            if matches:
                patterns.append(f"• {region.title()} expressions: {', '.join(matches)}")
        
        # Formality indicators
        formal_words = ['furthermore', 'however', 'nevertheless', 'consequently', 'therefore']
        informal_words = ['yeah', 'nope', 'gonna', 'wanna', 'stuff', 'things']
        
        formal_count = sum(1 for word in formal_words if word in content.lower())
        informal_count = sum(1 for word in informal_words if word in content.lower())
        
        if formal_count > informal_count + 2:
            patterns.append("• Formal writing style detected")
        elif informal_count > formal_count + 2:
            patterns.append("• Informal/conversational style detected")
        
        return "\n".join(patterns) if patterns else "No distinctive linguistic patterns detected"
    
    async def _analyze_temporal_patterns(self, content: str) -> str:
        """Analyze temporal references and timing patterns"""
        temporal_patterns = []
        
        # Date patterns
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # DD/MM/YYYY or MM/DD/YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY/MM/DD
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s*\d{4}\b'
        ]
        
        dates_found = []
        for pattern in date_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dates_found.extend(matches)
        
        if dates_found:
            temporal_patterns.append(f"• Date references found: {', '.join(dates_found[:3])}")
        
        # Time-sensitive language
        urgency_terms = ['breaking', 'just in', 'urgent', 'developing', 'live', 'now', 'immediate']
        found_urgency = [term for term in urgency_terms if term in content.lower()]
        
        if found_urgency:
            temporal_patterns.append(f"• Urgency indicators: {', '.join(found_urgency)}")
        
        # Temporal context clues
        context_terms = ['yesterday', 'today', 'tomorrow', 'this morning', 'last night', 'currently', 'recently']
        found_context = [term for term in context_terms if term in content.lower()]
        
        if found_context:
            temporal_patterns.append(f"• Temporal context: {', '.join(found_context)}")
        
        return "\n".join(temporal_patterns) if temporal_patterns else "No specific temporal patterns detected"
    
    async def _analyze_domains_and_urls(self, content: str) -> str:
        """Analyze URLs and domains for credibility and origin"""
        domain_analysis = []
        
        # Extract URLs
        url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        urls = re.findall(url_pattern, content, re.IGNORECASE)
        
        if urls:
            domain_analysis.append(f"• {len(urls)} URL(s) found")
            
            # Analyze domains
            domains = []
            suspicious_found = []
            
            for url in urls:
                try:
                    parsed = urlparse(url)
                    domain = parsed.netloc
                    domains.append(domain)
                    
                    # Check against suspicious domains
                    if any(sus_domain in domain for sus_domain in self.suspicious_domains):
                        suspicious_found.append(domain)
                        
                except Exception:
                    continue
            
            if domains:
                unique_domains = list(set(domains))
                domain_analysis.append(f"• Domains: {', '.join(unique_domains[:3])}")
            
            if suspicious_found:
                domain_analysis.append(f"• ⚠️ Suspicious domains detected: {', '.join(suspicious_found)}")
        
        # Check for URL shorteners
        shortener_patterns = ['bit.ly', 'tinyurl.com', 'short.link', 't.co', 'goo.gl']
        found_shorteners = [pattern for pattern in shortener_patterns if pattern in content.lower()]
        
        if found_shorteners:
            domain_analysis.append(f"• URL shorteners used: {', '.join(found_shorteners)}")
        
        return "\n".join(domain_analysis) if domain_analysis else "No URLs or domains detected"
    
    async def _analyze_propagation_patterns(self, content: str) -> str:
        """Analyze how content is designed to spread"""
        propagation_patterns = []
        
        # Viral indicators
        viral_terms = ['share', 'retweet', 'forward', 'spread the word', 'tell everyone', 'viral', 'trending']
        found_viral = [term for term in viral_terms if term in content.lower()]
        
        if found_viral:
            propagation_patterns.append(f"• Viral language: {', '.join(found_viral)}")
        
        # Call-to-action patterns
        cta_patterns = ['click here', 'read more', 'sign up', 'subscribe', 'follow', 'like and share']
        found_cta = [pattern for pattern in cta_patterns if pattern in content.lower()]
        
        if found_cta:
            propagation_patterns.append(f"• Call-to-action elements: {', '.join(found_cta)}")
        
        # Emotional hooks
        emotional_hooks = ['shocking', 'unbelievable', 'amazing', 'incredible', 'must see', 'you won\'t believe']
        found_hooks = [hook for hook in emotional_hooks if hook in content.lower()]
        
        if found_hooks:
            propagation_patterns.append(f"• Emotional hooks: {', '.join(found_hooks)}")
        
        # Network amplification terms
        network_terms = ['everyone is talking', 'going viral', 'millions are sharing', 'breaking the internet']
        found_network = [term for term in network_terms if term in content.lower()]
        
        if found_network:
            propagation_patterns.append(f"• Network amplification language: {', '.join(found_network)}")
        
        return "\n".join(propagation_patterns) if propagation_patterns else "Standard propagation patterns"
    
    async def _generate_content_fingerprint(self, content: str) -> str:
        """Generate unique fingerprint for content tracking"""
        # Create content characteristics for fingerprinting
        characteristics = []
        
        # Length characteristics
        characteristics.append(f"Length: {len(content)} chars, {len(content.split())} words")
        
        # Character frequency (simplified)
        char_freq = {}
        for char in content.lower():
            if char.isalpha():
                char_freq[char] = char_freq.get(char, 0) + 1
        
        if char_freq:
            top_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            characteristics.append(f"Top characters: {', '.join([f'{c}({n})' for c, n in top_chars])}")
        
        # Structural elements
        sentences = len(re.split(r'[.!?]+', content))
        paragraphs = len(content.split('\n\n'))
        characteristics.append(f"Structure: {sentences} sentences, {paragraphs} paragraphs")
        
        # Unique word patterns
        words = content.lower().split()
        unique_words = len(set(words))
        if len(words) > 0:
            uniqueness_ratio = unique_words / len(words)
            characteristics.append(f"Vocabulary diversity: {uniqueness_ratio:.2f}")
        
        return "\n".join([f"• {char}" for char in characteristics])
    
    async def _extract_temporal_references(self, content: str) -> List[Dict[str, Any]]:
        """Extract temporal references for timeline building"""
        references = []
        
        # Simple temporal extraction (can be enhanced with NLP)
        patterns = {
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'recent': r'\b(?:yesterday|today|this morning|last night)\b',
            'urgent': r'\b(?:breaking|just in|developing now)\b'
        }
        
        for ref_type, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                references.append({
                    'type': ref_type,
                    'text': match,
                    'timestamp': datetime.now() - timedelta(hours=1),  # Simplified
                    'confidence': 0.7,
                    'description': f"{ref_type} reference: {match}"
                })
        
        return references
    
    async def _extract_platform_timeline(self, content: str) -> List[Dict[str, Any]]:
        """Extract platform-specific timeline markers"""
        events = []
        
        # Look for retweet patterns, shares, etc.
        if 'rt @' in content.lower() or 'retweet' in content.lower():
            events.append({
                'timestamp': datetime.now() - timedelta(minutes=30),
                'event_type': 'social_share',
                'description': 'Content appears to be shared/retweeted',
                'confidence': 0.8,
                'source': 'pattern_analysis'
            })
        
        if 'forwarded message' in content.lower():
            events.append({
                'timestamp': datetime.now() - timedelta(minutes=15),
                'event_type': 'message_forward',
                'description': 'Content appears to be forwarded message',
                'confidence': 0.9,
                'source': 'pattern_analysis'
            })
        
        return events
    
    async def _simulate_reverse_search(self, image_url: str, engine: str) -> List[Dict[str, Any]]:
        """Simulate reverse image search results"""
        # In production, this would make actual API calls to search engines
        return [
            {
                'url': f'https://example.com/similar-image-1',
                'title': f'Similar image found on {engine}',
                'domain': 'example.com',
                'first_seen': (datetime.now() - timedelta(days=5)).isoformat(),
                'confidence': 0.85
            },
            {
                'url': f'https://news.example.com/article-123',
                'title': f'Image used in news article',
                'domain': 'news.example.com',
                'first_seen': (datetime.now() - timedelta(days=2)).isoformat(),
                'confidence': 0.92
            }
        ]