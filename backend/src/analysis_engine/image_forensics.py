# backend/src/analysis_engine/image_forensics.py

import asyncio
import aiohttp
import hashlib
import json
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional
from PIL import Image
from PIL.ExifTags import TAGS
import google.generativeai as genai
from google.cloud import vision
import io
import os
import logging

logger = logging.getLogger(__name__)

class ImageForensics:
    """Advanced image forensics analysis for Truth Lab 2.0"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.google_api_key = config.get('google_api_key')
        self.vision_client = None
        self.gemini_model = None
        
        # Initialize Google services
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize Google Cloud Vision and Gemini services"""
        try:
            if self.google_api_key:
                # Initialize Gemini
                genai.configure(api_key=self.google_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Initialize Vision API (will use same credentials)
                self.vision_client = vision.ImageAnnotatorClient()
                
                logger.info("Google services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google services: {e}")
    
    async def analyze_image(self, image_data: bytes, filename: str = None) -> Dict[str, Any]:
        """
        Comprehensive image forensics analysis
        
        Args:
            image_data: Raw image bytes
            filename: Optional filename for context
            
        Returns:
            Dictionary containing forensic analysis results
        """
        try:
            analysis_start = datetime.utcnow()
            
            # Run all forensic analyses in parallel
            tasks = [
                self._extract_metadata(image_data, filename),
                self._analyze_image_content(image_data),
                self._detect_text_in_image(image_data),
                self._check_image_manipulation(image_data),
                self._generate_image_hash(image_data),
                self._analyze_image_properties(image_data)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine results
            forensic_report = {
                'analysis_id': hashlib.md5(image_data[:1024]).hexdigest(),
                'timestamp': analysis_start.isoformat(),
                'filename': filename,
                'file_size': len(image_data),
                'metadata_analysis': results[0] if not isinstance(results[0], Exception) else {'error': str(results[0])},
                'content_analysis': results[1] if not isinstance(results[1], Exception) else {'error': str(results[1])},
                'text_detection': results[2] if not isinstance(results[2], Exception) else {'error': str(results[2])},
                'manipulation_detection': results[3] if not isinstance(results[3], Exception) else {'error': str(results[3])},
                'image_hash': results[4] if not isinstance(results[4], Exception) else {'error': str(results[4])},
                'image_properties': results[5] if not isinstance(results[5], Exception) else {'error': str(results[5])},
                'processing_time': (datetime.utcnow() - analysis_start).total_seconds(),
                'forensic_score': 0  # Will be calculated
            }
            
            # Calculate overall forensic score
            forensic_report['forensic_score'] = self._calculate_forensic_score(forensic_report)
            
            return forensic_report
            
        except Exception as e:
            logger.error(f"Image forensics analysis failed: {e}")
            return {
                'error': f"Analysis failed: {str(e)}",
                'timestamp': datetime.utcnow().isoformat(),
                'forensic_score': 0
            }
    
    async def _extract_metadata(self, image_data: bytes, filename: str) -> Dict[str, Any]:
        """Extract EXIF and metadata from image"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Basic image info
            metadata = {
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'has_exif': False,
                'exif_data': {},
                'suspicious_indicators': []
            }
            
            # Extract EXIF data if available
            if hasattr(image, '_getexif'):
                exif_data = image._getexif()
                if exif_data:
                    metadata['has_exif'] = True
                    
                    # Parse EXIF tags
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        metadata['exif_data'][tag] = str(value)
                    
                    # Check for suspicious indicators
                    if 'Software' in metadata['exif_data']:
                        software = metadata['exif_data']['Software'].lower()
                        editing_software = ['photoshop', 'gimp', 'paint.net', 'canva', 'pixlr']
                        if any(editor in software for editor in editing_software):
                            metadata['suspicious_indicators'].append(f"Edited with: {software}")
                    
                    # Check for missing typical camera data
                    camera_fields = ['Make', 'Model', 'DateTime']
                    missing_fields = [field for field in camera_fields if field not in metadata['exif_data']]
                    if len(missing_fields) == len(camera_fields):
                        metadata['suspicious_indicators'].append("Missing camera metadata")
            
            return metadata
            
        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")
            return {'error': f"Metadata extraction failed: {str(e)}"}
    
    async def _analyze_image_content(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze image content using Google Vision API"""
        try:
            if not self.vision_client:
                return {'error': 'Vision API not initialized'}
            
            # Prepare image for Vision API
            image = vision.Image(content=image_data)
            
            # Run multiple Vision API analyses
            tasks = []
            
            # Object detection
            tasks.append(self.vision_client.object_localization(image=image))
            
            # Label detection
            tasks.append(self.vision_client.label_detection(image=image))
            
            # Face detection
            tasks.append(self.vision_client.face_detection(image=image))
            
            # Logo detection
            tasks.append(self.vision_client.logo_detection(image=image))
            
            # Web detection (for reverse image search)
            tasks.append(self.vision_client.web_detection(image=image))
            
            # Execute all tasks
            responses = await asyncio.gather(*[
                asyncio.to_thread(task.result) for task in tasks
            ], return_exceptions=True)
            
            content_analysis = {
                'objects': [],
                'labels': [],
                'faces_detected': 0,
                'logos': [],
                'web_entities': [],
                'similar_images': [],
                'content_warnings': []
            }
            
            # Process object detection
            if not isinstance(responses[0], Exception) and responses[0].localized_object_annotations:
                content_analysis['objects'] = [
                    {
                        'name': obj.name,
                        'confidence': obj.score,
                        'bounding_box': {
                            'vertices': [(vertex.x, vertex.y) for vertex in obj.bounding_poly.normalized_vertices]
                        }
                    }
                    for obj in responses[0].localized_object_annotations
                ]
            
            # Process labels
            if not isinstance(responses[1], Exception) and responses[1].label_annotations:
                content_analysis['labels'] = [
                    {
                        'description': label.description,
                        'confidence': label.score
                    }
                    for label in responses[1].label_annotations
                ]
            
            # Process faces
            if not isinstance(responses[2], Exception) and responses[2].face_annotations:
                content_analysis['faces_detected'] = len(responses[2].face_annotations)
                
                # Check for unusual face properties that might indicate manipulation
                for face in responses[2].face_annotations:
                    if face.detection_confidence < 0.5:
                        content_analysis['content_warnings'].append("Low confidence face detection - possible manipulation")
            
            # Process logos
            if not isinstance(responses[3], Exception) and responses[3].logo_annotations:
                content_analysis['logos'] = [
                    {
                        'description': logo.description,
                        'confidence': logo.score
                    }
                    for logo in responses[3].logo_annotations
                ]
            
            # Process web detection
            if not isinstance(responses[4], Exception) and responses[4].web_detection:
                web_detection = responses[4].web_detection
                
                if web_detection.web_entities:
                    content_analysis['web_entities'] = [
                        {
                            'entity_id': entity.entity_id,
                            'description': entity.description,
                            'confidence': entity.score
                        }
                        for entity in web_detection.web_entities[:10]  # Limit to top 10
                    ]
                
                if web_detection.full_matching_images:
                    content_analysis['similar_images'] = [
                        img.url for img in web_detection.full_matching_images[:5]  # Top 5 matches
                    ]
            
            return content_analysis
            
        except Exception as e:
            logger.error(f"Image content analysis failed: {e}")
            return {'error': f"Content analysis failed: {str(e)}"}
    
    async def _detect_text_in_image(self, image_data: bytes) -> Dict[str, Any]:
        """Detect and extract text from image"""
        try:
            if not self.vision_client:
                return {'error': 'Vision API not initialized'}
            
            image = vision.Image(content=image_data)
            response = await asyncio.to_thread(
                self.vision_client.text_detection, image=image
            )
            
            text_analysis = {
                'detected_text': '',
                'text_blocks': [],
                'languages_detected': [],
                'suspicious_text_patterns': []
            }
            
            if response.text_annotations:
                # Full detected text
                text_analysis['detected_text'] = response.text_annotations[0].description
                
                # Individual text blocks
                for text in response.text_annotations[1:]:  # Skip first one (full text)
                    text_analysis['text_blocks'].append({
                        'text': text.description,
                        'confidence': text.confidence if hasattr(text, 'confidence') else 1.0,
                        'bounding_box': {
                            'vertices': [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
                        }
                    })
                
                # Check for suspicious patterns
                detected_text = text_analysis['detected_text'].lower()
                suspicious_patterns = [
                    'breaking news', 'urgent', 'share immediately', 'before it\'s deleted',
                    'doctors hate this', 'shocking truth', 'government hiding',
                    'click here', 'limited time', 'act now'
                ]
                
                for pattern in suspicious_patterns:
                    if pattern in detected_text:
                        text_analysis['suspicious_text_patterns'].append(pattern)
            
            return text_analysis
            
        except Exception as e:
            logger.error(f"Text detection failed: {e}")
            return {'error': f"Text detection failed: {str(e)}"}
    
    async def _check_image_manipulation(self, image_data: bytes) -> Dict[str, Any]:
        """Check for signs of image manipulation using AI analysis"""
        try:
            if not self.gemini_model:
                return {'error': 'Gemini model not initialized'}
            
            # Convert image to base64 for Gemini
            image_b64 = base64.b64encode(image_data).decode()
            
            # Prepare prompt for manipulation detection
            prompt = """
            Analyze this image for signs of digital manipulation or editing. Look for:
            1. Inconsistent lighting or shadows
            2. Unnatural edges or blending
            3. Repeated patterns or clone stamping
            4. Color or pixel inconsistencies
            5. Compression artifacts that suggest editing
            6. Any other signs of photo manipulation
            
            Provide your analysis as a JSON response with:
            - manipulation_likelihood: score from 0-100
            - detected_issues: list of specific issues found
            - confidence: your confidence in the analysis (0-1)
            - explanation: detailed explanation
            """
            
            # Analyze with Gemini
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                [prompt, {"mime_type": "image/jpeg", "data": image_b64}]
            )
            
            # Parse response
            try:
                # Try to extract JSON from response
                response_text = response.text
                if '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_str = response_text[json_start:json_end]
                    manipulation_analysis = json.loads(json_str)
                else:
                    # Fallback if no JSON structure
                    manipulation_analysis = {
                        'manipulation_likelihood': 50,
                        'detected_issues': [],
                        'confidence': 0.5,
                        'explanation': response_text
                    }
                    
            except json.JSONDecodeError:
                manipulation_analysis = {
                    'manipulation_likelihood': 50,
                    'detected_issues': [],
                    'confidence': 0.5,
                    'explanation': response.text,
                    'raw_response': response.text
                }
            
            return manipulation_analysis
            
        except Exception as e:
            logger.error(f"Manipulation detection failed: {e}")
            return {'error': f"Manipulation detection failed: {str(e)}"}
    
    async def _generate_image_hash(self, image_data: bytes) -> Dict[str, Any]:
        """Generate multiple hashes for image identification"""
        try:
            hashes = {
                'md5': hashlib.md5(image_data).hexdigest(),
                'sha256': hashlib.sha256(image_data).hexdigest(),
                'size_bytes': len(image_data)
            }
            
            # Generate perceptual hash using PIL
            try:
                image = Image.open(io.BytesIO(image_data))
                # Simple perceptual hash (difference hash)
                image = image.convert('L').resize((8, 8), Image.LANCZOS)
                pixels = list(image.getdata())
                
                # Calculate difference hash
                dhash = ""
                for row in range(8):
                    for col in range(7):
                        pixel_left = pixels[row * 8 + col]
                        pixel_right = pixels[row * 8 + col + 1]
                        dhash += "1" if pixel_left > pixel_right else "0"
                
                hashes['perceptual_hash'] = dhash
                
            except Exception as e:
                logger.warning(f"Perceptual hash generation failed: {e}")
                hashes['perceptual_hash'] = None
            
            return hashes
            
        except Exception as e:
            logger.error(f"Hash generation failed: {e}")
            return {'error': f"Hash generation failed: {str(e)}"}
    
    async def _analyze_image_properties(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze technical image properties"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            properties = {
                'dimensions': f"{image.size[0]}x{image.size[1]}",
                'aspect_ratio': round(image.size[0] / image.size[1], 2),
                'color_mode': image.mode,
                'format': image.format,
                'has_transparency': image.mode in ('RGBA', 'LA') or 'transparency' in image.info,
                'compression_quality': None,
                'suspicious_properties': []
            }
            
            # Check for unusual properties
            if image.size[0] * image.size[1] > 10000000:  # Very large image
                properties['suspicious_properties'].append("Unusually large dimensions")
            
            if image.size[0] < 100 or image.size[1] < 100:  # Very small image
                properties['suspicious_properties'].append("Unusually small dimensions")
            
            # Check aspect ratio
            if properties['aspect_ratio'] > 5 or properties['aspect_ratio'] < 0.2:
                properties['suspicious_properties'].append("Unusual aspect ratio")
            
            return properties
            
        except Exception as e:
            logger.error(f"Image properties analysis failed: {e}")
            return {'error': f"Properties analysis failed: {str(e)}"}
    
    def _calculate_forensic_score(self, forensic_report: Dict[str, Any]) -> float:
        """Calculate overall forensic credibility score"""
        try:
            score = 50.0  # Start with neutral score
            
            # Metadata analysis
            if 'metadata_analysis' in forensic_report and 'error' not in forensic_report['metadata_analysis']:
                metadata = forensic_report['metadata_analysis']
                
                # Bonus for having EXIF data
                if metadata.get('has_exif', False):
                    score += 15
                
                # Penalty for suspicious indicators
                suspicious_count = len(metadata.get('suspicious_indicators', []))
                score -= suspicious_count * 5
            
            # Content analysis
            if 'content_analysis' in forensic_report and 'error' not in forensic_report['content_analysis']:
                content = forensic_report['content_analysis']
                
                # Penalty for content warnings
                warning_count = len(content.get('content_warnings', []))
                score -= warning_count * 10
                
                # Bonus for having web matches (indicates image has been seen before)
                if content.get('similar_images'):
                    score += 10
            
            # Manipulation detection
            if 'manipulation_detection' in forensic_report and 'error' not in forensic_report['manipulation_detection']:
                manipulation = forensic_report['manipulation_detection']
                
                if 'manipulation_likelihood' in manipulation:
                    # Higher manipulation likelihood = lower score
                    manipulation_penalty = manipulation['manipulation_likelihood'] * 0.3
                    score -= manipulation_penalty
            
            # Text analysis
            if 'text_detection' in forensic_report and 'error' not in forensic_report['text_detection']:
                text = forensic_report['text_detection']
                
                # Penalty for suspicious text patterns
                suspicious_patterns = len(text.get('suspicious_text_patterns', []))
                score -= suspicious_patterns * 8
            
            # Ensure score is within bounds
            return max(0, min(100, score))
            
        except Exception as e:
            logger.error(f"Forensic score calculation failed: {e}")
            return 50.0  # Return neutral score on error

# Export the class for use in comprehensive_analysis.py
__all__ = ['ImageForensics']
