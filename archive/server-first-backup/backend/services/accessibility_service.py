"""
Accessibility Service - Text-to-Speech, Translations, and Adaptive Tools
Provides comprehensive accessibility features for enhanced usability
"""
import logging
import json
import base64
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from services.ai_service import ai_service

logger = logging.getLogger(__name__)

class AccessibilityService:
    """Comprehensive accessibility features service"""
    
    def __init__(self):
        self.tts_engines = {
            'browser': self._browser_tts,
            'cloud': self._cloud_tts,
            'system': self._system_tts
        }
        
        self.translation_services = {
            'ai': self._ai_translate,
            'browser': self._browser_translate
        }
        
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }
        
        logger.info("♿ Accessibility Service initialized")
    
    async def text_to_speech(self, text: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Convert text to speech with various options"""
        try:
            options = options or {}
            
            # Text processing and cleanup
            processed_text = await self._process_text_for_tts(text, options)
            
            # Select TTS engine based on options
            engine = options.get('engine', 'browser')
            voice = options.get('voice', 'default')
            speed = options.get('speed', 1.0)
            pitch = options.get('pitch', 1.0)
            
            if engine in self.tts_engines:
                result = await self.tts_engines[engine](processed_text, {
                    'voice': voice,
                    'speed': speed,
                    'pitch': pitch,
                    **options
                })
                
                # Store TTS session for analytics
                await self._store_tts_session(text, options, result)
                
                return result
            else:
                return {'error': f'Unsupported TTS engine: {engine}'}
                
        except Exception as e:
            logger.error(f"❌ Text-to-speech failed: {e}")
            return {'error': str(e)}
    
    async def translate_text(self, text: str, target_language: str, source_language: str = 'auto') -> Dict[str, Any]:
        """Translate text to target language"""
        try:
            if target_language not in self.supported_languages:
                return {'error': f'Unsupported target language: {target_language}'}
            
            # Use AI translation as primary method
            translation_result = await self._ai_translate(text, target_language, source_language)
            
            # Store translation session
            await self._store_translation_session(text, source_language, target_language, translation_result)
            
            return {
                'original_text': text,
                'translated_text': translation_result.get('translated_text', ''),
                'source_language': translation_result.get('detected_language', source_language),
                'target_language': target_language,
                'confidence': translation_result.get('confidence', 0.8),
                'method': 'ai_translation'
            }
            
        except Exception as e:
            logger.error(f"❌ Translation failed: {e}")
            return {'error': str(e)}
    
    async def adjust_page_layout(self, adjustments: Dict[str, Any]) -> Dict[str, Any]:
        """Generate CSS adjustments for improved accessibility"""
        try:
            css_rules = []
            
            # Font size adjustments
            if 'font_size' in adjustments:
                font_multiplier = adjustments['font_size']
                css_rules.append(f"""
                * {{
                    font-size: calc(1em * {font_multiplier}) !important;
                }}
                """)
            
            # High contrast mode
            if adjustments.get('high_contrast', False):
                css_rules.append("""
                * {
                    background-color: black !important;
                    color: white !important;
                    border-color: white !important;
                }
                a {
                    color: yellow !important;
                }
                button, input, select, textarea {
                    background-color: #333 !important;
                    color: white !important;
                    border: 2px solid white !important;
                }
                """)
            
            # Reduce motion
            if adjustments.get('reduce_motion', False):
                css_rules.append("""
                *, *::before, *::after {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                    scroll-behavior: auto !important;
                }
                """)
            
            # Focus indicators
            if adjustments.get('enhanced_focus', True):
                css_rules.append("""
                *:focus {
                    outline: 3px solid #ff6b6b !important;
                    outline-offset: 2px !important;
                }
                """)
            
            # Cursor size
            if 'cursor_size' in adjustments:
                cursor_size = adjustments['cursor_size']
                css_rules.append(f"""
                * {{
                    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="{cursor_size}" height="{cursor_size}" viewBox="0 0 32 32"><path d="M2 2v28l8-8h20V2H2z" fill="black"/></svg>') 0 0, auto !important;
                }}
                """)
            
            combined_css = '\n'.join(css_rules)
            
            return {
                'css': combined_css,
                'adjustments_applied': list(adjustments.keys()),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Layout adjustment failed: {e}")
            return {'error': str(e)}
    
    async def generate_alt_text(self, image_data: str, context: str = '') -> Dict[str, Any]:
        """Generate alt text for images using AI"""
        try:
            # Use AI to analyze image and generate description
            prompt = f"""
            Generate descriptive alt text for an image. Context: {context}
            
            Please provide:
            1. A concise, descriptive alt text (1-2 sentences)
            2. A detailed description for screen readers
            3. Key visual elements mentioned
            
            Return as JSON:
            {{
                "alt_text": "Brief description",
                "detailed_description": "Longer description for screen readers",
                "key_elements": ["element1", "element2", "element3"],
                "confidence": 0.8
            }}
            """
            
            ai_response = ai_service.process_query(prompt, {'image_context': context})
            
            try:
                result = json.loads(ai_response.get('explanation', '{}'))
            except json.JSONDecodeError:
                result = {
                    'alt_text': 'Image description generated by AI',
                    'detailed_description': ai_response.get('explanation', 'Unable to generate description'),
                    'key_elements': ['visual content'],
                    'confidence': 0.5
                }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Alt text generation failed: {e}")
            return {'error': str(e)}
    
    async def create_audio_description(self, video_url: str, transcript: str = '') -> Dict[str, Any]:
        """Create audio descriptions for video content"""
        try:
            # Use AI to generate audio descriptions based on video content
            prompt = f"""
            Create audio descriptions for a video to help visually impaired users.
            
            Video URL: {video_url}
            Existing transcript: {transcript}
            
            Generate detailed audio descriptions that describe:
            1. Visual scenes and settings
            2. Actions and gestures
            3. Important visual information not conveyed in audio
            4. Scene changes and transitions
            
            Format as timestamped descriptions.
            """
            
            ai_response = ai_service.process_query(prompt, {'video_url': video_url})
            
            return {
                'video_url': video_url,
                'audio_descriptions': ai_response.get('explanation', ''),
                'original_transcript': transcript,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Audio description generation failed: {e}")
            return {'error': str(e)}
    
    async def keyboard_navigation_helper(self, page_content: str) -> Dict[str, Any]:
        """Generate keyboard navigation shortcuts for web page"""
        try:
            # Analyze page content to generate keyboard shortcuts
            prompt = f"""
            Analyze this web page content and suggest keyboard navigation shortcuts:
            
            Content (first 1000 chars): {page_content[:1000]}
            
            Generate:
            1. Tab order suggestions
            2. Keyboard shortcuts for main actions
            3. Skip links for better navigation
            4. Focus management recommendations
            
            Return as JSON with actionable suggestions.
            """
            
            ai_response = ai_service.process_query(prompt, {'page_content': page_content[:1000]})
            
            return {
                'navigation_suggestions': ai_response.get('explanation', ''),
                'keyboard_shortcuts': self._generate_default_shortcuts(),
                'accessibility_score': await self._calculate_accessibility_score(page_content)
            }
            
        except Exception as e:
            logger.error(f"❌ Keyboard navigation helper failed: {e}")
            return {'error': str(e)}
    
    async def reading_assistance(self, text: str, reading_level: str = 'default') -> Dict[str, Any]:
        """Provide reading assistance with simplified text and definitions"""
        try:
            prompt = f"""
            Provide reading assistance for this text at {reading_level} level:
            
            Text: {text[:2000]}
            
            Provide:
            1. Simplified version of the text
            2. Key terms and definitions
            3. Summary of main points
            4. Reading difficulty assessment
            
            Return as structured JSON.
            """
            
            ai_response = ai_service.process_query(prompt, {'reading_level': reading_level})
            
            # Additional processing
            word_count = len(text.split())
            estimated_reading_time = max(1, word_count // 200)  # Assume 200 words per minute
            
            return {
                'original_text': text,
                'simplified_text': ai_response.get('explanation', text),
                'reading_level': reading_level,
                'word_count': word_count,
                'estimated_reading_time_minutes': estimated_reading_time,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Reading assistance failed: {e}")
            return {'error': str(e)}
    
    async def _process_text_for_tts(self, text: str, options: Dict[str, Any]) -> str:
        """Process and clean text for optimal TTS output"""
        # Remove HTML tags if present
        import re
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Handle abbreviations and numbers
        abbreviations = {
            'AI': 'Artificial Intelligence',
            'URL': 'U R L',
            'HTTP': 'H T T P',
            'API': 'A P I',
            'UI': 'User Interface',
            'UX': 'User Experience'
        }
        
        for abbr, expansion in abbreviations.items():
            text = text.replace(abbr, expansion)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    async def _browser_tts(self, text: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate browser-based TTS instructions"""
        return {
            'method': 'browser_tts',
            'text': text,
            'voice': options.get('voice', 'default'),
            'speed': options.get('speed', 1.0),
            'pitch': options.get('pitch', 1.0),
            'instructions': {
                'use_speech_synthesis': True,
                'text_to_speak': text,
                'voice_settings': options
            }
        }
    
    async def _cloud_tts(self, text: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate cloud TTS (placeholder for actual cloud service)"""
        return {
            'method': 'cloud_tts',
            'text': text,
            'note': 'Cloud TTS integration needed',
            'options': options
        }
    
    async def _system_tts(self, text: str, options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate system TTS (placeholder for system integration)"""
        return {
            'method': 'system_tts',
            'text': text,
            'note': 'System TTS integration needed',
            'options': options
        }
    
    async def _ai_translate(self, text: str, target_lang: str, source_lang: str = 'auto') -> Dict[str, Any]:
        """Use AI for text translation"""
        try:
            target_lang_name = self.supported_languages.get(target_lang, target_lang)
            
            prompt = f"""
            Translate this text to {target_lang_name}:
            
            Text: {text}
            
            Provide accurate, natural translation. If the source language is different from what's expected, detect it.
            
            Return as JSON:
            {{
                "translated_text": "translation here",
                "detected_language": "detected language code",
                "confidence": 0.9
            }}
            """
            
            ai_response = ai_service.process_query(prompt, {
                'source_language': source_lang,
                'target_language': target_lang
            })
            
            try:
                result = json.loads(ai_response.get('explanation', '{}'))
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    'translated_text': ai_response.get('explanation', text),
                    'detected_language': source_lang,
                    'confidence': 0.7
                }
            
            return result
            
        except Exception as e:
            logger.error(f"❌ AI translation failed: {e}")
            return {
                'translated_text': text,
                'detected_language': source_lang,
                'confidence': 0.0,
                'error': str(e)
            }
    
    async def _browser_translate(self, text: str, target_lang: str, source_lang: str = 'auto') -> Dict[str, Any]:
        """Browser-based translation (placeholder)"""
        return {
            'method': 'browser_translate',
            'note': 'Browser translation integration needed'
        }
    
    def _generate_default_shortcuts(self) -> Dict[str, str]:
        """Generate default keyboard shortcuts"""
        return {
            'Alt+H': 'Go to main navigation',
            'Alt+M': 'Go to main content', 
            'Alt+F': 'Go to footer',
            'Alt+S': 'Go to search',
            'Tab': 'Navigate forward through interactive elements',
            'Shift+Tab': 'Navigate backward through interactive elements',
            'Enter/Space': 'Activate buttons and links',
            'Escape': 'Close dialogs and menus'
        }
    
    async def _calculate_accessibility_score(self, content: str) -> float:
        """Calculate basic accessibility score for content"""
        score = 1.0
        
        # Check for common accessibility issues
        if len(content.split()) < 10:
            score -= 0.1  # Too little content
        
        # Simple checks (in real implementation, this would be more sophisticated)
        import re
        
        # Check for images without alt text (basic check)
        img_tags = re.findall(r'<img[^>]*>', content)
        img_without_alt = [img for img in img_tags if 'alt=' not in img]
        if img_without_alt:
            score -= 0.2
        
        # Check for headings structure
        headings = re.findall(r'<h[1-6][^>]*>', content)
        if not headings:
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    async def _store_tts_session(self, text: str, options: Dict[str, Any], result: Dict[str, Any]):
        """Store TTS session for analytics"""
        try:
            from database.mongodb import db_manager
            
            session_data = {
                'type': 'tts',
                'text_length': len(text),
                'options': options,
                'method': result.get('method', 'unknown'),
                'success': 'error' not in result,
                'timestamp': datetime.now()
            }
            
            await db_manager.store_accessibility_session(session_data)
            
        except Exception as e:
            logger.error(f"❌ Failed to store TTS session: {e}")
    
    async def _store_translation_session(self, text: str, source_lang: str, target_lang: str, result: Dict[str, Any]):
        """Store translation session for analytics"""
        try:
            from database.mongodb import db_manager
            
            session_data = {
                'type': 'translation',
                'text_length': len(text),
                'source_language': source_lang,
                'target_language': target_lang,
                'confidence': result.get('confidence', 0),
                'success': 'error' not in result,
                'timestamp': datetime.now()
            }
            
            await db_manager.store_accessibility_session(session_data)
            
        except Exception as e:
            logger.error(f"❌ Failed to store translation session: {e}")

# Global accessibility service instance
accessibility_service = AccessibilityService()