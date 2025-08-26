"""
Agent Builder Service - Eko Framework Implementation
Create custom agents using natural language or JavaScript
"""
import json
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import asyncio
import ast
from services.ai_service import ai_service
from services.shadow_browser_service import shadow_browser_service
from database.mongodb import db_manager

logger = logging.getLogger(__name__)

class AgentBuilderService:
    """Custom agent creation and management framework"""
    
    def __init__(self):
        self.active_agents = {}
        self.agent_templates = {
            'web_scraper': self._create_scraper_template,
            'monitor': self._create_monitor_template,
            'researcher': self._create_researcher_template,
            'automator': self._create_automator_template,
            'analyzer': self._create_analyzer_template
        }
        
        self.execution_environments = {
            'browser': self._execute_in_browser,
            'api': self._execute_via_api,
            'hybrid': self._execute_hybrid
        }
        
        logger.info("🤖 Agent Builder Service initialized")
    
    async def create_agent_from_description(self, description: str, user_id: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a custom agent from natural language description"""
        try:
            config = config or {}
            agent_id = str(uuid.uuid4())
            
            # Use AI to analyze description and generate agent specification
            agent_spec = await self._generate_agent_specification(description, config)
            
            # Generate agent code based on specification
            agent_code = await self._generate_agent_code(agent_spec)
            
            # Validate and test agent
            validation_result = await self._validate_agent(agent_code, agent_spec)
            
            if not validation_result['valid']:
                return {'error': f'Agent validation failed: {validation_result["error"]}'}
            
            # Create agent instance
            agent = {
                'id': agent_id,
                'name': agent_spec.get('name', 'Custom Agent'),
                'description': description,
                'specification': agent_spec,
                'code': agent_code,
                'user_id': user_id,
                'created_at': datetime.now(),
                'status': 'created',
                'execution_count': 0,
                'last_run': None,
                'capabilities': agent_spec.get('capabilities', []),
                'environment': agent_spec.get('environment', 'browser')
            }
            
            # Store agent
            await self._store_agent(agent)
            self.active_agents[agent_id] = agent
            
            logger.info(f"🤖 Created agent {agent_id}: {agent['name']}")
            
            return {
                'agent_id': agent_id,
                'agent': agent,
                'validation': validation_result,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Agent creation failed: {e}")
            return {'error': str(e)}
    
    async def create_agent_from_code(self, code: str, metadata: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Create agent from JavaScript/Python code"""
        try:
            agent_id = str(uuid.uuid4())
            
            # Parse and validate code
            code_analysis = await self._analyze_code(code)
            
            if not code_analysis['valid']:
                return {'error': f'Invalid code: {code_analysis["error"]}'}
            
            # Generate specification from code
            agent_spec = await self._generate_spec_from_code(code, metadata, code_analysis)
            
            # Validate agent
            validation_result = await self._validate_agent(code, agent_spec)
            
            if not validation_result['valid']:
                return {'error': f'Agent validation failed: {validation_result["error"]}'}
            
            agent = {
                'id': agent_id,
                'name': metadata.get('name', 'Custom Code Agent'),
                'description': metadata.get('description', 'Agent created from code'),
                'specification': agent_spec,
                'code': code,
                'code_language': code_analysis['language'],
                'user_id': user_id,
                'created_at': datetime.now(),
                'status': 'created',
                'execution_count': 0,
                'last_run': None,
                'capabilities': code_analysis['capabilities'],
                'environment': metadata.get('environment', 'browser')
            }
            
            await self._store_agent(agent)
            self.active_agents[agent_id] = agent
            
            logger.info(f"🤖 Created code-based agent {agent_id}: {agent['name']}")
            
            return {
                'agent_id': agent_id,
                'agent': agent,
                'code_analysis': code_analysis,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"❌ Code-based agent creation failed: {e}")
            return {'error': str(e)}
    
    async def execute_agent(self, agent_id: str, input_data: Dict[str, Any] = None, user_id: str = None) -> Dict[str, Any]:
        """Execute a custom agent"""
        try:
            # Get agent
            agent = await self._get_agent(agent_id)
            
            if not agent:
                return {'error': 'Agent not found'}
            
            # Check permissions
            if user_id and agent.get('user_id') != user_id:
                return {'error': 'Access denied'}
            
            execution_id = str(uuid.uuid4())
            
            # Prepare execution context
            execution_context = {
                'agent_id': agent_id,
                'execution_id': execution_id,
                'input_data': input_data or {},
                'user_id': user_id,
                'started_at': datetime.now()
            }
            
            # Execute based on agent environment
            environment = agent.get('environment', 'browser')
            
            if environment in self.execution_environments:
                result = await self.execution_environments[environment](agent, execution_context)
            else:
                return {'error': f'Unsupported execution environment: {environment}'}
            
            # Update agent statistics
            await self._update_agent_stats(agent_id, result)
            
            # Store execution result
            await self._store_execution_result(execution_context, result)
            
            logger.info(f"🚀 Agent {agent_id} executed: {result.get('status', 'unknown')}")
            
            return {
                'execution_id': execution_id,
                'agent_id': agent_id,
                'result': result,
                'success': result.get('status') == 'completed'
            }
            
        except Exception as e:
            logger.error(f"❌ Agent execution failed: {e}")
            return {'error': str(e)}
    
    async def list_user_agents(self, user_id: str) -> List[Dict[str, Any]]:
        """List all agents created by user"""
        try:
            agents = await db_manager.get_user_agents(user_id)
            return agents
        except Exception as e:
            logger.error(f"❌ Failed to list user agents: {e}")
            return []
    
    async def get_agent_marketplace(self) -> List[Dict[str, Any]]:
        """Get public agents from marketplace"""
        try:
            # Get public/shared agents
            public_agents = await db_manager.get_public_agents()
            
            # Add template agents
            template_agents = []
            for template_name, template_func in self.agent_templates.items():
                template = await template_func()
                template['id'] = f'template_{template_name}'
                template['type'] = 'template'
                template_agents.append(template)
            
            return public_agents + template_agents
            
        except Exception as e:
            logger.error(f"❌ Failed to get agent marketplace: {e}")
            return []
    
    async def _generate_agent_specification(self, description: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate agent specification from natural language description"""
        try:
            prompt = f"""
            Create an agent specification from this description:
            
            Description: {description}
            Config: {json.dumps(config, indent=2)}
            
            Generate a detailed specification including:
            1. Agent name and purpose
            2. Required capabilities (web_scraping, automation, analysis, etc.)
            3. Input/output formats
            4. Execution steps
            5. Error handling requirements
            6. Performance considerations
            
            Return as JSON:
            {{
                "name": "Agent Name",
                "purpose": "What the agent does",
                "capabilities": ["capability1", "capability2"],
                "inputs": {{"input1": "type", "input2": "type"}},
                "outputs": {{"output1": "type", "output2": "type"}},
                "steps": [
                    {{"action": "step1", "description": "what it does", "params": {{}}}},
                    {{"action": "step2", "description": "what it does", "params": {{}}}}
                ],
                "environment": "browser|api|hybrid",
                "error_handling": ["error1", "error2"],
                "performance_notes": "performance considerations"
            }}
            """
            
            ai_response = ai_service.process_query(prompt, config)
            
            try:
                spec = json.loads(ai_response.get('explanation', '{}'))
            except json.JSONDecodeError:
                # Fallback specification
                spec = {
                    'name': 'Custom Agent',
                    'purpose': description,
                    'capabilities': ['web_scraping'],
                    'inputs': {'url': 'string'},
                    'outputs': {'result': 'string'},
                    'steps': [
                        {'action': 'navigate', 'description': 'Navigate to URL', 'params': {'url': 'input.url'}}
                    ],
                    'environment': 'browser',
                    'error_handling': ['network_errors', 'timeout_errors'],
                    'performance_notes': 'Basic agent implementation'
                }
            
            return spec
            
        except Exception as e:
            logger.error(f"❌ Agent specification generation failed: {e}")
            raise
    
    async def _generate_agent_code(self, spec: Dict[str, Any]) -> str:
        """Generate agent code from specification"""
        try:
            prompt = f"""
            Generate Python code for an agent with this specification:
            
            Specification: {json.dumps(spec, indent=2)}
            
            Create a complete Python class that:
            1. Implements all required capabilities
            2. Handles the specified inputs/outputs
            3. Follows the execution steps
            4. Includes proper error handling
            5. Uses available services (shadow_browser_service, ai_service, etc.)
            
            Use this template structure:
            
            class CustomAgent:
                def __init__(self, config=None):
                    self.config = config or {{}}
                    self.name = "{spec.get('name', 'CustomAgent')}"
                
                async def execute(self, inputs):
                    # Implementation here
                    return {{"status": "completed", "result": result}}
                
                async def validate_inputs(self, inputs):
                    # Validation logic
                    return True
            
            Return complete, runnable Python code.
            """
            
            ai_response = ai_service.process_query(prompt, {'specification': spec})
            
            code = ai_response.get('explanation', '')
            
            # Clean up code if needed
            if '```python' in code:
                code = code.split('```python')[1].split('```')[0]
            elif '```' in code:
                code = code.split('```')[1].split('```')[0]
            
            return code.strip()
            
        except Exception as e:
            logger.error(f"❌ Agent code generation failed: {e}")
            raise
    
    async def _validate_agent(self, code: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Validate agent code and specification"""
        try:
            validation_issues = []
            
            # Basic Python syntax check
            try:
                ast.parse(code)
            except SyntaxError as e:
                validation_issues.append(f"Syntax error: {e}")
            
            # Check for required methods
            if 'async def execute(' not in code:
                validation_issues.append("Missing execute method")
            
            # Check for security issues
            dangerous_imports = ['os', 'subprocess', 'sys']
            for imp in dangerous_imports:
                if f'import {imp}' in code or f'from {imp}' in code:
                    validation_issues.append(f"Potentially dangerous import: {imp}")
            
            # Validate specification structure
            required_spec_fields = ['name', 'purpose', 'capabilities']
            for field in required_spec_fields:
                if field not in spec:
                    validation_issues.append(f"Missing specification field: {field}")
            
            return {
                'valid': len(validation_issues) == 0,
                'issues': validation_issues,
                'error': '; '.join(validation_issues) if validation_issues else None
            }
            
        except Exception as e:
            logger.error(f"❌ Agent validation failed: {e}")
            return {
                'valid': False,
                'issues': [str(e)],
                'error': str(e)
            }
    
    async def _analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze provided code for capabilities and language"""
        try:
            analysis = {
                'valid': True,
                'language': 'unknown',
                'capabilities': [],
                'dependencies': [],
                'security_issues': []
            }
            
            # Detect language
            if 'async def' in code or 'import ' in code:
                analysis['language'] = 'python'
            elif 'function' in code or 'const ' in code or 'let ' in code:
                analysis['language'] = 'javascript'
            
            # Analyze capabilities based on code content
            capability_keywords = {
                'web_scraping': ['page.goto', 'page.content', 'querySelector', 'scrape'],
                'automation': ['click', 'type', 'fill', 'submit', 'automate'],
                'api_calls': ['fetch', 'axios', 'httpx', 'requests', 'api'],
                'data_processing': ['json', 'csv', 'pandas', 'process', 'transform'],
                'ai_integration': ['ai_service', 'openai', 'gpt', 'llm', 'model']
            }
            
            for capability, keywords in capability_keywords.items():
                if any(keyword in code.lower() for keyword in keywords):
                    analysis['capabilities'].append(capability)
            
            # Check for security issues
            security_patterns = [
                'eval(', 'exec(', '__import__', 'subprocess', 'os.system',
                'shell=True', 'rm -rf', 'del ', 'delete'
            ]
            
            for pattern in security_patterns:
                if pattern in code:
                    analysis['security_issues'].append(f"Potentially dangerous: {pattern}")
            
            # Basic syntax validation
            if analysis['language'] == 'python':
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    analysis['valid'] = False
                    analysis['error'] = str(e)
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Code analysis failed: {e}")
            return {
                'valid': False,
                'language': 'unknown',
                'capabilities': [],
                'error': str(e)
            }
    
    async def _generate_spec_from_code(self, code: str, metadata: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specification from code analysis"""
        return {
            'name': metadata.get('name', 'Code Agent'),
            'purpose': metadata.get('description', 'Agent created from code'),
            'capabilities': analysis['capabilities'],
            'inputs': {'data': 'any'},
            'outputs': {'result': 'any'},
            'steps': [{'action': 'execute_code', 'description': 'Execute provided code'}],
            'environment': metadata.get('environment', 'browser'),
            'error_handling': ['syntax_errors', 'runtime_errors'],
            'performance_notes': 'Generated from user code'
        }
    
    async def _execute_in_browser(self, agent: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent in browser environment"""
        try:
            # Create execution namespace
            namespace = {
                'shadow_browser_service': shadow_browser_service,
                'ai_service': ai_service,
                'context': context,
                'inputs': context.get('input_data', {})
            }
            
            # Execute agent code
            exec(agent['code'], namespace)
            
            # Get agent instance and execute
            if 'CustomAgent' in namespace:
                agent_instance = namespace['CustomAgent']()
                result = await agent_instance.execute(context.get('input_data', {}))
                
                return {
                    'status': 'completed',
                    'result': result,
                    'environment': 'browser',
                    'execution_time': (datetime.now() - context['started_at']).total_seconds()
                }
            else:
                return {
                    'status': 'failed',
                    'error': 'No CustomAgent class found in code',
                    'environment': 'browser'
                }
                
        except Exception as e:
            logger.error(f"❌ Browser execution failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'environment': 'browser'
            }
    
    async def _execute_via_api(self, agent: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent via API calls"""
        # Implementation for API-based execution
        return {
            'status': 'failed',
            'error': 'API execution not yet implemented',
            'environment': 'api'
        }
    
    async def _execute_hybrid(self, agent: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent in hybrid environment"""
        # Implementation for hybrid execution
        return {
            'status': 'failed',
            'error': 'Hybrid execution not yet implemented',
            'environment': 'hybrid'
        }
    
    async def _create_scraper_template(self) -> Dict[str, Any]:
        """Create web scraper agent template"""
        return {
            'name': 'Web Scraper Agent',
            'description': 'Scrapes data from websites',
            'capabilities': ['web_scraping', 'data_extraction'],
            'template_code': '''
class WebScraperAgent:
    async def execute(self, inputs):
        url = inputs.get('url')
        selectors = inputs.get('selectors', [])
        
        task_config = {
            'type': 'web_scraping',
            'url': url,
            'selectors': selectors
        }
        
        task_id = await shadow_browser_service.execute_background_task(task_config)
        
        # Wait for completion
        for _ in range(30):
            status = await shadow_browser_service.get_task_status(task_id)
            if status['status'] in ['completed', 'failed']:
                break
            await asyncio.sleep(1)
        
        return status.get('result', {})
            ''',
            'inputs': {'url': 'string', 'selectors': 'array'},
            'outputs': {'extracted_data': 'object'}
        }
    
    async def _create_monitor_template(self) -> Dict[str, Any]:
        """Create monitoring agent template"""
        return {
            'name': 'Monitor Agent',
            'description': 'Monitors websites for changes',
            'capabilities': ['monitoring', 'alerts'],
            'template_code': '''
class MonitorAgent:
    async def execute(self, inputs):
        url = inputs.get('url')
        check_interval = inputs.get('interval', 300)
        
        task_config = {
            'type': 'monitoring',
            'url': url,
            'interval': check_interval,
            'duration': 3600  # 1 hour
        }
        
        task_id = await shadow_browser_service.execute_background_task(task_config)
        return {'monitoring_started': True, 'task_id': task_id}
            ''',
            'inputs': {'url': 'string', 'interval': 'number'},
            'outputs': {'monitoring_started': 'boolean', 'task_id': 'string'}
        }
    
    async def _create_researcher_template(self) -> Dict[str, Any]:
        """Create research agent template"""
        return {
            'name': 'Research Agent',
            'description': 'Conducts automated research',
            'capabilities': ['research', 'analysis', 'report_generation'],
            'template_code': '''
class ResearchAgent:
    async def execute(self, inputs):
        topic = inputs.get('topic')
        depth = inputs.get('depth', 'medium')
        
        # Use search service for research
        from services.search_service import search_service
        
        search_result = await search_service.execute_deep_search(topic)
        
        # Generate research report
        from services.report_service import report_service
        
        report_config = {
            'type': 'research',
            'topic': topic,
            'search_query': topic,
            'data_sources': ['search']
        }
        
        report = await report_service.generate_report(report_config)
        
        return {
            'research_completed': True,
            'report_id': report.get('report_id'),
            'findings': search_result.get('results', {})
        }
            ''',
            'inputs': {'topic': 'string', 'depth': 'string'},
            'outputs': {'research_completed': 'boolean', 'report_id': 'string'}
        }
    
    async def _create_automator_template(self) -> Dict[str, Any]:
        """Create automation agent template"""
        return {
            'name': 'Automation Agent',
            'description': 'Automates repetitive tasks',
            'capabilities': ['automation', 'workflow_execution'],
            'template_code': '''
class AutomationAgent:
    async def execute(self, inputs):
        steps = inputs.get('steps', [])
        
        results = []
        
        for step in steps:
            task_config = {
                'type': 'automation',
                'steps': [step]
            }
            
            task_id = await shadow_browser_service.execute_background_task(task_config)
            
            # Wait for completion
            for _ in range(30):
                status = await shadow_browser_service.get_task_status(task_id)
                if status['status'] in ['completed', 'failed']:
                    results.append(status)
                    break
                await asyncio.sleep(1)
        
        return {
            'automation_completed': True,
            'steps_executed': len(results),
            'results': results
        }
            ''',
            'inputs': {'steps': 'array'},
            'outputs': {'automation_completed': 'boolean', 'results': 'array'}
        }
    
    async def _create_analyzer_template(self) -> Dict[str, Any]:
        """Create data analyzer agent template"""
        return {
            'name': 'Analyzer Agent',
            'description': 'Analyzes data and generates insights',
            'capabilities': ['data_analysis', 'insights', 'visualization'],
            'template_code': '''
class AnalyzerAgent:
    async def execute(self, inputs):
        data = inputs.get('data')
        analysis_type = inputs.get('type', 'summary')
        
        # Use AI service for analysis
        prompt = f"Analyze this data and provide insights: {json.dumps(data)[:1000]}"
        
        analysis = ai_service.process_query(prompt, {'analysis_type': analysis_type})
        
        return {
            'analysis_completed': True,
            'insights': analysis.get('explanation', ''),
            'data_points': len(data) if isinstance(data, list) else 1
        }
            ''',
            'inputs': {'data': 'any', 'type': 'string'},
            'outputs': {'analysis_completed': 'boolean', 'insights': 'string'}
        }
    
    async def _get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID"""
        if agent_id in self.active_agents:
            return self.active_agents[agent_id]
        
        # Try to load from database
        try:
            agent = await db_manager.get_agent(agent_id)
            if agent:
                self.active_agents[agent_id] = agent
            return agent
        except Exception as e:
            logger.error(f"❌ Failed to get agent {agent_id}: {e}")
            return None
    
    async def _store_agent(self, agent: Dict[str, Any]):
        """Store agent in database"""
        try:
            await db_manager.store_agent(agent)
            logger.info(f"💾 Agent {agent['id']} stored")
        except Exception as e:
            logger.error(f"❌ Failed to store agent: {e}")
    
    async def _update_agent_stats(self, agent_id: str, result: Dict[str, Any]):
        """Update agent execution statistics"""
        try:
            if agent_id in self.active_agents:
                agent = self.active_agents[agent_id]
                agent['execution_count'] += 1
                agent['last_run'] = datetime.now()
                if result.get('status') == 'completed':
                    agent['status'] = 'active'
                
                await db_manager.update_agent_stats(agent_id, {
                    'execution_count': agent['execution_count'],
                    'last_run': agent['last_run'],
                    'status': agent['status']
                })
                
        except Exception as e:
            logger.error(f"❌ Failed to update agent stats: {e}")
    
    async def _store_execution_result(self, context: Dict[str, Any], result: Dict[str, Any]):
        """Store agent execution result"""
        try:
            execution_data = {
                'agent_id': context['agent_id'],
                'execution_id': context['execution_id'],
                'user_id': context['user_id'],
                'input_data': context['input_data'],
                'result': result,
                'started_at': context['started_at'],
                'completed_at': datetime.now(),
                'duration': result.get('execution_time', 0)
            }
            
            await db_manager.store_agent_execution(execution_data)
            
        except Exception as e:
            logger.error(f"❌ Failed to store execution result: {e}")

# Global agent builder service
agent_builder_service = AgentBuilderService()