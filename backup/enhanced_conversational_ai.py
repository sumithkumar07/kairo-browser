"""
🤖 PHASE 5: Enhanced Conversational AI
Advanced AI conversation system with vision, voice, and learning capabilities
"""
import asyncio
import logging
import json
import time
from typing import Dict, Any, Optional, List
from groq import Groq
from config import settings
import base64
import io
from PIL import Image
import speech_recognition as sr
import tempfile
import os

logger = logging.getLogger(__name__)

class EnhancedConversationalAI:
    """Enhanced conversational AI with multi-modal capabilities"""
    
    def __init__(self):
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY) if settings.GROQ_API_KEY else None
        self.conversation_memory = {}
        self.user_patterns = {}
        self.learning_data = {}
        self.speech_recognizer = sr.Recognizer()
        self.context_window = 50  # Remember last 50 interactions
        logger.info("🤖 Enhanced Conversational AI initialized")
    
    async def process_multimodal_query(self, query: str, 
                                     context: Optional[Dict[str, Any]] = None,
                                     image_data: Optional[str] = None,
                                     audio_data: Optional[bytes] = None,
                                     session_id: str = 'default') -> Dict[str, Any]:
        """Process multi-modal query with text, image, and audio"""
        try:
            # Initialize session memory if needed
            if session_id not in self.conversation_memory:
                self.conversation_memory[session_id] = []
            
            # Process different input types
            processed_inputs = {
                'text': query,
                'image_analysis': await self._process_image_input(image_data) if image_data else None,
                'audio_transcription': await self._process_audio_input(audio_data) if audio_data else None
            }
            
            # Enhance query with context and memory
            enhanced_query = await self._enhance_query_with_context(
                query, context, processed_inputs, session_id
            )
            
            # Generate AI response
            ai_response = await self._generate_enhanced_response(enhanced_query, session_id)
            
            # Learn from interaction
            await self._learn_from_interaction(query, ai_response, context, session_id)
            
            # Update conversation memory
            self._update_conversation_memory(session_id, query, ai_response)
            
            return {
                'success': True,
                'response': ai_response,
                'processed_inputs': processed_inputs,
                'session_id': session_id,
                'memory_size': len(self.conversation_memory[session_id])
            }
            
        except Exception as e:
            logger.error(f"❌ Multi-modal query processing failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _process_image_input(self, image_data: str) -> Dict[str, Any]:
        """Process and analyze image input"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Perform image analysis
            analysis = {
                'dimensions': image.size,
                'format': image.format,
                'mode': image.mode,
                'dominant_colors': await self._extract_dominant_colors(image),
                'detected_elements': await self._detect_ui_elements(image),
                'text_content': await self._extract_text_from_image(image),
                'scene_analysis': await self._analyze_scene(image)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Image processing failed: {e}")
            return {'error': str(e)}
    
    async def _process_audio_input(self, audio_data: bytes) -> Dict[str, Any]:
        """Process and transcribe audio input"""
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            # Transcribe audio
            try:
                with sr.AudioFile(temp_audio_path) as source:
                    audio = self.speech_recognizer.record(source)
                    transcription = self.speech_recognizer.recognize_google(audio)
                
                # Clean up
                os.unlink(temp_audio_path)
                
                return {
                    'transcription': transcription,
                    'confidence': 0.85,  # Placeholder
                    'language': 'en-US',
                    'duration': len(audio_data) / 16000  # Approximate duration
                }
                
            except sr.UnknownValueError:
                return {'error': 'Could not understand audio'}
            except sr.RequestError as e:
                return {'error': f'Speech recognition error: {e}'}
            
        except Exception as e:
            logger.error(f"❌ Audio processing failed: {e}")
            return {'error': str(e)}
    
    async def _extract_dominant_colors(self, image: Image.Image) -> List[str]:
        """Extract dominant colors from image"""
        try:
            # Resize image for faster processing
            image = image.resize((100, 100))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get color histogram
            colors = image.getcolors(maxcolors=256*256*256)
            if colors:
                # Sort by frequency and get top 5
                top_colors = sorted(colors, key=lambda x: x[0], reverse=True)[:5]
                return [f'rgb{color[1]}' for color in top_colors]
            
            return []
            
        except Exception as e:
            logger.debug(f"Color extraction warning: {e}")
            return []
    
    async def _detect_ui_elements(self, image: Image.Image) -> Dict[str, Any]:
        """Detect UI elements in image (simplified implementation)"""
        try:
            # This would use computer vision in production
            # For now, return placeholder analysis
            width, height = image.size
            
            return {
                'buttons_detected': 0,  # Would use CV to detect
                'text_regions': 0,      # Would use OCR regions
                'input_fields': 0,      # Would use form detection
                'navigation_elements': 0, # Would use UI pattern recognition
                'layout_analysis': {
                    'header_region': {'x': 0, 'y': 0, 'width': width, 'height': height * 0.1},
                    'content_region': {'x': 0, 'y': height * 0.1, 'width': width, 'height': height * 0.8},
                    'footer_region': {'x': 0, 'y': height * 0.9, 'width': width, 'height': height * 0.1}
                }
            }
            
        except Exception as e:
            logger.debug(f"UI element detection warning: {e}")
            return {}
    
    async def _extract_text_from_image(self, image: Image.Image) -> str:
        """Extract text content from image using OCR"""
        try:
            # This would use Tesseract OCR in production
            # For now, return placeholder
            return "Text extraction would be implemented with OCR library"
            
        except Exception as e:
            logger.debug(f"Text extraction warning: {e}")
            return ""
    
    async def _analyze_scene(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze the overall scene in the image"""
        try:
            # This would use advanced computer vision in production
            return {
                'scene_type': 'webpage',
                'complexity': 'medium',
                'primary_content': 'interface',
                'interaction_opportunities': ['buttons', 'links', 'forms']
            }
            
        except Exception as e:
            logger.debug(f"Scene analysis warning: {e}")
            return {}
    
    async def _enhance_query_with_context(self, query: str, context: Optional[Dict[str, Any]], 
                                        processed_inputs: Dict[str, Any], session_id: str) -> str:
        """Enhance query with context and memory"""
        try:
            enhanced_parts = [f"User Query: {query}"]
            
            # Add context information
            if context:
                if context.get('currentUrl'):
                    enhanced_parts.append(f"Current Page: {context['currentUrl']}")
                if context.get('pageTitle'):
                    enhanced_parts.append(f"Page Title: {context['pageTitle']}")
                if context.get('userAction'):
                    enhanced_parts.append(f"User Action Context: {context['userAction']}")
            
            # Add conversation memory
            memory = self.conversation_memory.get(session_id, [])
            if memory:
                recent_context = memory[-3:]  # Last 3 interactions
                context_summary = "Recent conversation context:\n"
                for interaction in recent_context:
                    context_summary += f"User: {interaction['query']}\nAI: {interaction['response'][:100]}...\n"
                enhanced_parts.append(context_summary)
            
            # Add image analysis if available
            if processed_inputs.get('image_analysis'):
                img_analysis = processed_inputs['image_analysis']
                enhanced_parts.append(f"Image Analysis: {json.dumps(img_analysis, indent=2)}")
            
            # Add audio transcription if available
            if processed_inputs.get('audio_transcription'):
                audio_analysis = processed_inputs['audio_transcription']
                enhanced_parts.append(f"Audio Input: {audio_analysis.get('transcription', 'N/A')}")
            
            # Add user patterns
            if session_id in self.user_patterns:
                patterns = self.user_patterns[session_id]
                enhanced_parts.append(f"User Patterns: {json.dumps(patterns, indent=2)}")
            
            return "\n\n".join(enhanced_parts)
            
        except Exception as e:
            logger.error(f"❌ Query enhancement failed: {e}")
            return query
    
    async def _generate_enhanced_response(self, enhanced_query: str, session_id: str) -> Dict[str, Any]:
        """Generate enhanced AI response with advanced capabilities"""
        try:
            if not self.groq_client:
                return {'explanation': 'AI service not configured', 'commands': []}
            
            # Enhanced system prompt with multi-modal capabilities
            system_prompt = self._get_enhanced_system_prompt()
            
            # Generate response
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": enhanced_query}
                ],
                model=settings.GROQ_MODEL,
                temperature=0.3,
                max_tokens=2000
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse and enhance response
            parsed_response = self._parse_enhanced_response(ai_response)
            
            # Add predictive suggestions
            parsed_response['predictive_suggestions'] = await self._generate_predictive_suggestions(
                enhanced_query, session_id
            )
            
            # Add visual feedback suggestions
            parsed_response['visual_feedback'] = await self._generate_visual_feedback_suggestions(
                enhanced_query, parsed_response
            )
            
            return parsed_response
            
        except Exception as e:
            logger.error(f"❌ Enhanced response generation failed: {e}")
            return {
                'explanation': f'Error generating response: {str(e)}',
                'commands': [],
                'error': str(e)
            }
    
    def _get_enhanced_system_prompt(self) -> str:
        """Get enhanced system prompt with multi-modal capabilities"""
        return """You are Kairo AI, an advanced intelligent browser assistant with comprehensive multi-modal capabilities. You excel at:

🌟 ENHANCED CAPABILITIES:
1. **Multi-Modal Understanding**: Process text, images, and audio simultaneously
2. **Visual Intelligence**: Analyze screenshots, detect UI elements, understand layouts
3. **Conversational Memory**: Remember context across interactions and learn user patterns
4. **Predictive Intelligence**: Anticipate user needs and suggest next actions
5. **Advanced Workflow Building**: Create complex automations through natural conversation

🧠 CORE COMPETENCIES:
- **Browser Automation**: Navigate, click, type, scroll, extract data
- **Visual Analysis**: Screenshot understanding, UI element detection, layout analysis
- **Workflow Intelligence**: Multi-step automation, conditional logic, scheduling
- **Learning System**: Adapt to user behavior and preferences over time
- **Context Awareness**: Understand current page, user goals, and interaction history

🎯 RESPONSE FORMAT:
For multi-modal queries, provide comprehensive responses:
```json
{
  "intent": "Clear description of user intent",
  "commands": [
    {
      "type": "action_type",
      "params": {...},
      "confidence": 0.95,
      "reasoning": "Why this action is appropriate"
    }
  ],
  "explanation": "Clear explanation of what will be done",
  "visual_analysis": "Description of any visual elements analyzed",
  "audio_analysis": "Description of any audio content processed",
  "context_awareness": "How current context influences the response",
  "learning_insights": "Any patterns or preferences detected",
  "next_suggestions": ["suggestion1", "suggestion2", "suggestion3"],
  "workflow_opportunities": "Potential for automation or workflow creation"
}
```

🔄 CONVERSATION FLOW:
- Always acknowledge multi-modal inputs (images, audio)
- Reference previous interactions when relevant
- Suggest workflow creation for repetitive tasks
- Provide visual confirmation for actions
- Learn and adapt to user preferences
- Ask clarifying questions when needed

🛡️ ENHANCED FEATURES:
- **Smart Error Recovery**: Handle failures gracefully with alternatives
- **Context Preservation**: Maintain conversation context across sessions
- **Adaptive Learning**: Improve responses based on user feedback
- **Predictive Assistance**: Suggest actions before user asks
- **Visual Confirmation**: Provide screenshots and visual feedback

Always strive to be helpful, intelligent, and proactive while maintaining conversation flow and context awareness."""

    def _parse_enhanced_response(self, response: str) -> Dict[str, Any]:
        """Parse enhanced AI response with multi-modal support"""
        try:
            # Try to parse JSON response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = response[json_start:json_end]
                parsed = json.loads(json_content)
            else:
                parsed = json.loads(response)
            
            # Ensure required fields
            parsed.setdefault('intent', 'Process user request')
            parsed.setdefault('commands', [])
            parsed.setdefault('explanation', response)
            parsed.setdefault('confidence', 0.8)
            
            # Add enhanced fields
            parsed.setdefault('visual_analysis', None)
            parsed.setdefault('audio_analysis', None)
            parsed.setdefault('context_awareness', None)
            parsed.setdefault('learning_insights', None)
            parsed.setdefault('next_suggestions', [])
            parsed.setdefault('workflow_opportunities', None)
            
            return parsed
            
        except json.JSONDecodeError:
            return {
                'intent': 'Process user request',
                'commands': [],
                'explanation': response,
                'confidence': 0.6,
                'parsing_error': True
            }
    
    async def _generate_predictive_suggestions(self, query: str, session_id: str) -> List[str]:
        """Generate predictive suggestions based on context and patterns"""
        try:
            suggestions = []
            
            # Pattern-based suggestions
            memory = self.conversation_memory.get(session_id, [])
            if memory:
                # Analyze recent patterns
                recent_actions = [interaction.get('commands', []) for interaction in memory[-5:]]
                
                # Common follow-up actions
                if any('open' in str(actions) for actions in recent_actions):
                    suggestions.extend([
                        "Take a screenshot of this page",
                        "Extract key information from the page",
                        "Create a workflow for similar tasks"
                    ])
                
                if any('type' in str(actions) or 'form' in query.lower() for actions in recent_actions):
                    suggestions.extend([
                        "Save this form data for future use",
                        "Create an auto-fill workflow",
                        "Set up form monitoring"
                    ])
            
            # Context-based suggestions
            if 'search' in query.lower():
                suggestions.extend([
                    "Set up search result monitoring",
                    "Create a research workflow",
                    "Extract and summarize results"
                ])
            
            if 'login' in query.lower():
                suggestions.extend([
                    "Save login credentials securely",
                    "Create automated login workflow",
                    "Set up session monitoring"
                ])
            
            # Remove duplicates and limit
            suggestions = list(dict.fromkeys(suggestions))[:5]
            return suggestions
            
        except Exception as e:
            logger.debug(f"Predictive suggestions error: {e}")
            return []
    
    async def _generate_visual_feedback_suggestions(self, query: str, response: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visual feedback suggestions"""
        try:
            feedback = {
                'screenshot_recommended': False,
                'highlight_elements': [],
                'visual_confirmation': False,
                'progress_indicator': False
            }
            
            # Determine if screenshot is recommended
            if any(cmd.get('type') in ['click', 'type', 'navigate'] for cmd in response.get('commands', [])):
                feedback['screenshot_recommended'] = True
                feedback['visual_confirmation'] = True
            
            # Suggest element highlighting
            for cmd in response.get('commands', []):
                if cmd.get('type') == 'click' and cmd.get('params', {}).get('selector'):
                    feedback['highlight_elements'].append(cmd['params']['selector'])
            
            # Progress indicator for multi-step workflows
            if len(response.get('commands', [])) > 1:
                feedback['progress_indicator'] = True
            
            return feedback
            
        except Exception as e:
            logger.debug(f"Visual feedback generation error: {e}")
            return {}
    
    async def _learn_from_interaction(self, query: str, response: Dict[str, Any], 
                                    context: Optional[Dict[str, Any]], session_id: str):
        """Learn from user interactions to improve future responses"""
        try:
            # Initialize user patterns for session
            if session_id not in self.user_patterns:
                self.user_patterns[session_id] = {
                    'common_actions': {},
                    'preferred_sites': {},
                    'interaction_style': 'balanced',
                    'workflow_preferences': [],
                    'error_patterns': [],
                    'success_patterns': []
                }
            
            patterns = self.user_patterns[session_id]
            
            # Learn from commands
            for cmd in response.get('commands', []):
                action_type = cmd.get('type', 'unknown')
                patterns['common_actions'][action_type] = patterns['common_actions'].get(action_type, 0) + 1
            
            # Learn from context
            if context and context.get('currentUrl'):
                domain = context['currentUrl'].split('/')[2] if '://' in context['currentUrl'] else 'unknown'
                patterns['preferred_sites'][domain] = patterns['preferred_sites'].get(domain, 0) + 1
            
            # Analyze interaction style
            query_length = len(query.split())
            if query_length < 5:
                interaction_style = 'concise'
            elif query_length > 15:
                interaction_style = 'detailed'
            else:
                interaction_style = 'balanced'
            
            # Update interaction style preference
            patterns['interaction_style'] = interaction_style
            
            # Store learning data
            if session_id not in self.learning_data:
                self.learning_data[session_id] = []
            
            self.learning_data[session_id].append({
                'timestamp': time.time(),
                'query': query,
                'response_quality': response.get('confidence', 0.8),
                'context': context,
                'patterns_detected': patterns
            })
            
            # Limit learning data size
            if len(self.learning_data[session_id]) > 100:
                self.learning_data[session_id] = self.learning_data[session_id][-100:]
            
        except Exception as e:
            logger.debug(f"Learning from interaction error: {e}")
    
    def _update_conversation_memory(self, session_id: str, query: str, response: Dict[str, Any]):
        """Update conversation memory for context preservation"""
        try:
            memory_entry = {
                'timestamp': time.time(),
                'query': query,
                'response': response.get('explanation', ''),
                'commands': response.get('commands', []),
                'intent': response.get('intent', ''),
                'success': response.get('success', True)
            }
            
            if session_id not in self.conversation_memory:
                self.conversation_memory[session_id] = []
            
            self.conversation_memory[session_id].append(memory_entry)
            
            # Maintain context window size
            if len(self.conversation_memory[session_id]) > self.context_window:
                self.conversation_memory[session_id] = self.conversation_memory[session_id][-self.context_window:]
            
        except Exception as e:
            logger.debug(f"Memory update error: {e}")
    
    def get_user_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get analytics for a specific user session"""
        try:
            if session_id not in self.user_patterns:
                return {'session_id': session_id, 'no_data': True}
            
            patterns = self.user_patterns[session_id]
            memory = self.conversation_memory.get(session_id, [])
            learning = self.learning_data.get(session_id, [])
            
            return {
                'session_id': session_id,
                'total_interactions': len(memory),
                'common_actions': patterns['common_actions'],
                'preferred_sites': patterns['preferred_sites'],
                'interaction_style': patterns['interaction_style'],
                'average_response_quality': sum(l['response_quality'] for l in learning) / len(learning) if learning else 0,
                'learning_progress': len(learning),
                'memory_size': len(memory),
                'last_interaction': memory[-1]['timestamp'] if memory else None
            }
            
        except Exception as e:
            logger.error(f"❌ User analytics error: {e}")
            return {'session_id': session_id, 'error': str(e)}
    
    def get_global_analytics(self) -> Dict[str, Any]:
        """Get global analytics across all sessions"""
        try:
            return {
                'total_sessions': len(self.conversation_memory),
                'total_interactions': sum(len(memory) for memory in self.conversation_memory.values()),
                'active_sessions': len([s for s, m in self.conversation_memory.items() if m]),
                'learning_data_points': sum(len(data) for data in self.learning_data.values()),
                'memory_usage': {
                    'conversation_memory_mb': len(str(self.conversation_memory)) / 1024 / 1024,
                    'learning_data_mb': len(str(self.learning_data)) / 1024 / 1024,
                    'user_patterns_mb': len(str(self.user_patterns)) / 1024 / 1024
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Global analytics error: {e}")
            return {'error': str(e)}

# Global enhanced conversational AI instance
enhanced_conversational_ai = EnhancedConversationalAI()