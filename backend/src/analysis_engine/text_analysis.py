# Migrated from: TruthLens/utils/ai_services.py - GeminiService and FactCheckService classes
import asyncio
import aiohttp
import logging
from typing import Dict, List, Any, Optional

from ..utils.config import Config

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """
    Advanced text analysis using Gemini AI and fact-checking APIs
    Migrated from: TruthLens/utils/ai_services.py - GeminiService class
    Enhanced with async capabilities and improved error handling
    """
    
    def __init__(self):
        self.config = Config()
        self.gemini_api_key = self.config.GEMINI_API_KEY
        self.google_api_key = self.config.GOOGLE_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.fact_check_url = "https://factchecktools.googleapis.com/v1alpha1"
        
    async def test_connection(self) -> bool:
        """Test Gemini AI connection"""
        try:
            response = await self._make_gemini_request("Hello", model="gemini-1.5-flash")
            return response is not None
        except:
            return False
    
    async def test_fact_check_connection(self) -> bool:
        """Test fact check API connection"""
        try:
            result = await self.search_fact_checks("test")
            return True
        except:
            return False
    
    async def forensic_analysis(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Specialized forensic analysis using Gemini AI
        Migrated from: TruthLens/utils/ai_services.py - forensic_analysis()
        Enhanced with structured response parsing
        """
        
        prompt = f"""
        As a digital forensics expert, analyze this content for misinformation:
        
        CONTENT: "{text}"
        
        IMPORTANT: Start your VERACITY ASSESSMENT with one of these clear statements:
        - "FALSE INFORMATION" if the content is factually incorrect
        - "MISLEADING" if the content is partially true but deceptive
        - "TRUE" if the content is factually accurate
        - "UNVERIFIED" if you cannot determine accuracy
        
        Provide analysis in this format:
        
        🔍 VERACITY ASSESSMENT:
        [Start with FALSE INFORMATION/MISLEADING/TRUE/UNVERIFIED, then explain why]
        
        🧬 MANIPULATION TACTICS:
        [What psychological tricks are used?]
        
        📊 EVIDENCE EVALUATION:
        [What evidence supports/contradicts this? Include specific sources, studies, or articles]
        
        🎯 TARGET ANALYSIS:
        [Who is this meant to influence and how?]
        
        ⚠️ HARM POTENTIAL:
        [What damage could this cause if it spreads?]
        
        🛡️ COUNTER-NARRATIVE:
        [What's the accurate information? Include links to credible sources]
        
        📋 VERIFICATION STEPS:
        [How can users verify this themselves? Include specific websites and search terms]
        
        🔗 SOURCE LINKS & ARTICLES:
        [Provide 3-5 credible source links that refute or support this claim. Format as:
        - Source Name: [Brief description] - [URL or searchable reference]
        - Example: "Snopes Fact Check: Debunks this claim" - "https://snopes.com/fact-check/..."
        - Example: "Reuters Investigation: Confirms this is false" - "https://reuters.com/..."]
        
        📧 REPORTING INFORMATION:
        [If this is false/misleading content, provide relevant reporting emails:
        - Platform Reporting: [email addresses for social media platforms]
        - Fact-Check Organizations: [emails for fact-checking bodies]
        - Government Agencies: [relevant authorities for this type of content]
        - Example: "Report to Facebook: report@facebook.com"
        - Example: "Report to Snopes: tips@snopes.com"]
        
        Language: {language}
        Be specific, cite sources with links, use emojis for readability.
        """
        
        try:
            ai_response = await self._make_gemini_request(prompt, model="gemini-1.5-pro")
            
            if ai_response:
                # Extract structured information from response
                sources_and_reporting = self._extract_sources_and_reporting(ai_response)
                
                return {
                    'analysis': ai_response,
                    'sources': sources_and_reporting['sources'],
                    'reporting_emails': sources_and_reporting['reporting_emails']
                }
            else:
                return {
                    'analysis': "AI analysis temporarily unavailable",
                    'sources': [],
                    'reporting_emails': []
                }
                
        except Exception as e:
            logger.error(f"Gemini analysis failed: {str(e)}")
            return {
                'analysis': f"AI analysis error: {str(e)}",
                'sources': [],
                'reporting_emails': []
            }
    
    async def trace_origin(self, text: str) -> str:
        """
        Trace content origins
        Migrated from: TruthLens/utils/ai_services.py - trace_origin()
        """
        prompt = f"""
        As a digital investigator, analyze the potential origins of this content:
        
        CONTENT: "{text}"
        
        Analyze:
        🕵️ LINGUISTIC PATTERNS: [Writing style, grammar, vocabulary clues]
        📅 TEMPORAL CLUES: [References to dates, events, timing]
        🌍 GEOGRAPHIC INDICATORS: [Location references, cultural context]
        📱 PLATFORM INDICATORS: [Formatting, hashtags, platform-specific language]
        🔄 PROPAGATION PATTERN: [How this might spread, typical vectors]
        
        Provide your best assessment of where/when this originated.
        """
        
        try:
            return await self._make_gemini_request(prompt, model="gemini-1.5-pro") or "Origin analysis unavailable"
        except Exception as e:
            return f"Origin analysis error: {str(e)}"
    
    async def analyze_context(self, text: str) -> str:
        """
        Analyze missing context
        Migrated from: TruthLens/utils/ai_services.py - analyze_context()
        """
        prompt = f"""
        As a context analyst, identify what crucial context is missing from this content:
        
        CONTENT: "{text}"
        
        Identify:
        📚 MISSING BACKGROUND: [What background info is needed?]
        📊 MISSING DATA: [What statistics or data are omitted?]
        ⏰ MISSING TIMELINE: [What timeline context is missing?]
        🔗 MISSING CONNECTIONS: [What related events/facts aren't mentioned?]
        📝 CHERRY-PICKING: [What contradictory evidence might exist?]
        
        Explain why this missing context matters for understanding the truth.
        """
        
        try:
            return await self._make_gemini_request(prompt, model="gemini-1.5-flash") or "Context analysis unavailable"
        except Exception as e:
            return f"Context analysis error: {str(e)}"
    
    async def search_fact_checks(self, query: str) -> List[Dict[str, str]]:
        """
        Search for fact-checked claims
        Migrated from: TruthLens/utils/ai_services.py - FactCheckService.search_claims()
        """
        try:
            params = {
                'query': query[:100],
                'key': self.google_api_key,
                'languageCode': 'en'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.fact_check_url}/claims:search", 
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_fact_checks(data)
                    else:
                        logger.warning(f"Fact check API returned status {response.status}")
                        return []
                        
        except Exception as e:
            logger.warning(f"Fact check search failed: {str(e)}")
            return []
    
    def _extract_sources_and_reporting(self, ai_response: str) -> Dict[str, List[Dict[str, str]]]:
        """
        Extract source links and reporting information from AI response
        Migrated from: TruthLens/utils/ai_services.py - extract_sources_and_reporting()
        """
        if not ai_response:
            return {'sources': [], 'reporting_emails': []}
        
        sources = []
        reporting_emails = []
        
        # Extract source links
        source_section = self._extract_section(ai_response, "🔗 SOURCE LINKS & ARTICLES:")
        if source_section:
            lines = source_section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') and ':' in line:
                    # Parse format: "- Source Name: [description] - [URL]"
                    parts = line[1:].split(':', 1)
                    if len(parts) == 2:
                        source_name = parts[0].strip()
                        description_url = parts[1].strip()
                        
                        # Split description and URL
                        if ' - ' in description_url:
                            desc, url = description_url.rsplit(' - ', 1)
                            sources.append({
                                'name': source_name,
                                'description': desc.strip(),
                                'url': url.strip()
                            })
                        else:
                            sources.append({
                                'name': source_name,
                                'description': description_url,
                                'url': ""
                            })
        
        # Extract reporting emails
        reporting_section = self._extract_section(ai_response, "📧 REPORTING INFORMATION:")
        if reporting_section:
            lines = reporting_section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('-') and '@' in line:
                    # Parse format: "- Description: email@domain.com"
                    if ':' in line:
                        desc, email = line[1:].split(':', 1)
                        reporting_emails.append({
                            'description': desc.strip(),
                            'email': email.strip()
                        })
        
        return {
            'sources': sources,
            'reporting_emails': reporting_emails
        }
    
    def _extract_section(self, text: str, section_header: str) -> str:
        """Extract a specific section from AI response"""
        lines = text.split('\n')
        in_section = False
        section_content = []
        
        for line in lines:
            if section_header in line:
                in_section = True
                continue
            elif in_section and any(line.startswith(emoji) for emoji in ['🔍', '🧬', '📊', '🎯', '⚠️', '🛡️', '📋']):
                break
            elif in_section:
                section_content.append(line)
        
        return '\n'.join(section_content).strip()
    
    async def _make_gemini_request(self, prompt: str, model: str = "gemini-1.5-flash") -> Optional[str]:
        """
        Make async request to Gemini API
        Migrated from: TruthLens/utils/ai_services.py - _make_request()
        Enhanced with async support and better error handling
        """
        try:
            url = f"{self.base_url}/{model}:generateContent"
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.gemini_api_key
            }
            
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, 
                    headers=headers, 
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        # Extract generated text from Gemini API response
                        return result['candidates'][0]['content']['parts'][0]['text']
                    else:
                        logger.error(f"Gemini API Error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Gemini API Exception: {str(e)}")
            return None
    
    def _parse_fact_checks(self, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Parse fact check API response
        Migrated from: TruthLens/utils/ai_services.py - _parse_fact_checks()
        """
        results = []
        
        if 'claims' in data:
            for claim in data['claims'][:5]:  # Limit to 5 results
                for review in claim.get('claimReview', []):
                    results.append({
                        'title': review.get('title', 'No title'),
                        'url': review.get('url', ''),
                        'publisher': review.get('publisher', {}).get('name', 'Unknown'),
                        'verdict': review.get('textualRating', 'No verdict'),
                        'date': review.get('reviewDate', 'Unknown date')
                    })
        
        return results