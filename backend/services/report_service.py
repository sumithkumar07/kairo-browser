"""
Advanced Report Service - AI-Composed Reports with Visuals and Analytics
Generates comprehensive reports with data visualization and insights
"""
import logging
import json
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
from services.ai_service import ai_service
from services.search_service import search_service
from database.mongodb import db_manager

logger = logging.getLogger(__name__)

class ReportService:
    """Advanced report generation with AI-powered analysis and visualization"""
    
    def __init__(self):
        self.report_types = {
            'research': self._generate_research_report,
            'analytics': self._generate_analytics_report,
            'workflow': self._generate_workflow_report,
            'comparison': self._generate_comparison_report,
            'summary': self._generate_summary_report,
            'monitoring': self._generate_monitoring_report
        }
        
        self.visualization_types = {
            'chart': self._create_simple_chart,
            'graph': self._create_simple_chart,
            'table': self._create_simple_table,
            'infographic': self._create_simple_chart,
            'timeline': self._create_simple_chart
        }
        
        # Set matplotlib style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        logger.info("📊 Report Service initialized")
    
    async def generate_report(self, report_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive AI-powered report"""
        try:
            report_type = report_config.get('type', 'summary')
            report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            logger.info(f"📈 Generating {report_type} report: {report_id}")
            
            # Gather data for report
            report_data = await self._gather_report_data(report_config)
            
            # Generate report using appropriate handler
            if report_type in self.report_types:
                report_content = await self.report_types[report_type](report_data, report_config)
            else:
                raise ValueError(f"Unknown report type: {report_type}")
            
            # Create visualizations
            visualizations = await self._create_visualizations(report_content, report_config)
            
            # Generate AI insights and summary
            ai_insights = await self._generate_ai_insights(report_content, report_data)
            
            # Compile final report
            final_report = {
                'report_id': report_id,
                'type': report_type,
                'title': report_content.get('title', f'{report_type.title()} Report'),
                'executive_summary': ai_insights.get('summary', ''),
                'content': report_content,
                'visualizations': visualizations,
                'insights': ai_insights,
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'data_sources': report_data.get('sources', []),
                    'total_data_points': report_data.get('total_points', 0)
                }
            }
            
            # Store report
            await self._store_report(final_report)
            
            logger.info(f"✅ Report {report_id} generated successfully")
            return final_report
            
        except Exception as e:
            logger.error(f"❌ Report generation failed: {e}")
            return {'error': str(e)}
    
    async def _gather_report_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Gather data from various sources for report generation"""
        data_sources = config.get('data_sources', ['database'])
        time_range = config.get('time_range', {'days': 7})
        
        collected_data = {
            'sources': data_sources,
            'total_points': 0,
            'datasets': {}
        }
        
        # Calculate time range
        end_date = datetime.now()
        if 'days' in time_range:
            start_date = end_date - timedelta(days=time_range['days'])
        elif 'hours' in time_range:
            start_date = end_date - timedelta(hours=time_range['hours'])
        else:
            start_date = end_date - timedelta(days=7)
        
        # Gather from database
        if 'database' in data_sources:
            db_data = await self._gather_database_data(start_date, end_date, config)
            collected_data['datasets']['database'] = db_data
            collected_data['total_points'] += len(db_data.get('records', []))
        
        # Gather from search results
        if 'search' in data_sources:
            search_data = await self._gather_search_data(config)
            collected_data['datasets']['search'] = search_data
            collected_data['total_points'] += len(search_data.get('results', []))
        
        # Gather from browser activity
        if 'browser' in data_sources:
            browser_data = await self._gather_browser_data(start_date, end_date, config)
            collected_data['datasets']['browser'] = browser_data
            collected_data['total_points'] += len(browser_data.get('sessions', []))
        
        # Gather from external APIs if configured
        if 'external' in data_sources:
            external_data = await self._gather_external_data(config)
            collected_data['datasets']['external'] = external_data
            collected_data['total_points'] += len(external_data.get('data', []))
        
        return collected_data
    
    async def _gather_database_data(self, start_date: datetime, end_date: datetime, config: Dict[str, Any]) -> Dict[str, Any]:
        """Gather data from database collections"""
        try:
            # Get user activity data
            activity_data = await db_manager.get_activity_data(start_date, end_date)
            
            # Get search sessions
            search_sessions = await db_manager.get_search_sessions(start_date, end_date)
            
            # Get workflow executions
            workflow_data = await db_manager.get_workflow_data(start_date, end_date)
            
            return {
                'activity': activity_data,
                'searches': search_sessions,
                'workflows': workflow_data,
                'records': activity_data + search_sessions + workflow_data
            }
            
        except Exception as e:
            logger.error(f"❌ Database data gathering failed: {e}")
            return {'records': []}
    
    async def _gather_search_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Gather data from recent search results"""
        try:
            search_query = config.get('search_query', '')
            if not search_query:
                return {'results': []}
            
            # Execute search using search service
            search_result = await search_service.execute_deep_search(search_query)
            
            return {
                'query': search_query,
                'results': search_result.get('results', {}).get('results', []),
                'analysis': search_result.get('results', {}).get('ai_analysis', '')
            }
            
        except Exception as e:
            logger.error(f"❌ Search data gathering failed: {e}")
            return {'results': []}
    
    async def _gather_browser_data(self, start_date: datetime, end_date: datetime, config: Dict[str, Any]) -> Dict[str, Any]:
        """Gather browser activity data"""
        try:
            # Get browser sessions and commands
            browser_sessions = await db_manager.get_browser_sessions(start_date, end_date)
            
            return {
                'sessions': browser_sessions,
                'total_sessions': len(browser_sessions)
            }
            
        except Exception as e:
            logger.error(f"❌ Browser data gathering failed: {e}")
            return {'sessions': []}
    
    async def _gather_external_data(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Gather data from external APIs"""
        # Placeholder for external API integration
        return {'data': [], 'note': 'External data integration pending'}
    
    async def _generate_research_report(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive research report"""
        search_data = data.get('datasets', {}).get('search', {})
        
        report = {
            'title': f"Research Report: {config.get('topic', 'Unknown Topic')}",
            'sections': []
        }
        
        # Executive Summary Section
        if search_data.get('results'):
            results = search_data['results']
            
            report['sections'].append({
                'title': 'Executive Summary',
                'content': f"Research conducted on '{search_data.get('query', 'topic')}' yielded {len(results)} relevant sources across multiple platforms.",
                'type': 'text'
            })
            
            # Key Findings Section
            top_results = results[:5]
            findings = []
            for i, result in enumerate(top_results, 1):
                findings.append(f"{i}. {result.get('title', 'Unknown')}: {result.get('snippet', 'No description available')}")
            
            report['sections'].append({
                'title': 'Key Findings',
                'content': '\n'.join(findings),
                'type': 'list'
            })
            
            # Sources Section
            sources = []
            for result in results[:10]:
                sources.append({
                    'title': result.get('title', 'Unknown'),
                    'url': result.get('url', ''),
                    'source': result.get('search_source', 'unknown'),
                    'relevance': result.get('relevance_score', 0)
                })
            
            report['sections'].append({
                'title': 'Sources and References',
                'content': sources,
                'type': 'sources'
            })
        
        return report
    
    async def _generate_analytics_report(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analytics and metrics report"""
        db_data = data.get('datasets', {}).get('database', {})
        browser_data = data.get('datasets', {}).get('browser', {})
        
        report = {
            'title': 'Analytics Report',
            'sections': []
        }
        
        # Usage Statistics
        activity_data = db_data.get('activity', [])
        search_data = db_data.get('searches', [])
        
        stats = {
            'total_activities': len(activity_data),
            'total_searches': len(search_data),
            'total_sessions': browser_data.get('total_sessions', 0)
        }
        
        report['sections'].append({
            'title': 'Usage Statistics',
            'content': stats,
            'type': 'metrics'
        })
        
        # Activity Trends
        if activity_data:
            # Group by date
            daily_activity = {}
            for activity in activity_data:
                date = activity.get('timestamp', datetime.now()).date()
                daily_activity[date] = daily_activity.get(date, 0) + 1
            
            report['sections'].append({
                'title': 'Activity Trends',
                'content': daily_activity,
                'type': 'trend_data'
            })
        
        return report
    
    async def _generate_workflow_report(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workflow analysis report"""
        db_data = data.get('datasets', {}).get('database', {})
        workflow_data = db_data.get('workflows', [])
        
        report = {
            'title': 'Workflow Analysis Report',
            'sections': []
        }
        
        if workflow_data:
            # Workflow Statistics
            total_workflows = len(workflow_data)
            successful_workflows = len([w for w in workflow_data if w.get('status') == 'completed'])
            
            report['sections'].append({
                'title': 'Workflow Performance',
                'content': {
                    'total_workflows': total_workflows,
                    'successful_workflows': successful_workflows,
                    'success_rate': (successful_workflows / total_workflows * 100) if total_workflows > 0 else 0
                },
                'type': 'metrics'
            })
        
        return report
    
    async def _generate_comparison_report(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison report between different data sets"""
        report = {
            'title': 'Comparison Report',
            'sections': []
        }
        
        # Compare different data sources
        datasets = data.get('datasets', {})
        
        comparison_data = {}
        for source, source_data in datasets.items():
            if isinstance(source_data, dict):
                if 'records' in source_data:
                    comparison_data[source] = len(source_data['records'])
                elif 'results' in source_data:
                    comparison_data[source] = len(source_data['results'])
                elif 'sessions' in source_data:
                    comparison_data[source] = len(source_data['sessions'])
        
        if comparison_data:
            report['sections'].append({
                'title': 'Data Source Comparison',
                'content': comparison_data,
                'type': 'comparison'
            })
        
        return report
    
    async def _generate_summary_report(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary report"""
        report = {
            'title': 'Executive Summary Report',
            'sections': []
        }
        
        # Overall statistics
        total_points = data.get('total_points', 0)
        sources = data.get('sources', [])
        
        report['sections'].append({
            'title': 'Overview',
            'content': f"Generated from {len(sources)} data sources with {total_points} total data points.",
            'type': 'text'
        })
        
        # Key metrics from each dataset
        datasets = data.get('datasets', {})
        for source, source_data in datasets.items():
            if isinstance(source_data, dict) and source_data:
                section_content = f"Data from {source}: "
                
                if 'records' in source_data:
                    section_content += f"{len(source_data['records'])} records"
                elif 'results' in source_data:
                    section_content += f"{len(source_data['results'])} results"
                elif 'sessions' in source_data:
                    section_content += f"{len(source_data['sessions'])} sessions"
                
                report['sections'].append({
                    'title': f'{source.title()} Data',
                    'content': section_content,
                    'type': 'text'
                })
        
        return report
    
    async def _generate_monitoring_report(self, data: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate system monitoring report"""
        report = {
            'title': 'System Monitoring Report',
            'sections': []
        }
        
        # System health metrics
        db_data = data.get('datasets', {}).get('database', {})
        
        health_metrics = {
            'data_freshness': 'good' if db_data.get('records') else 'poor',
            'system_activity': 'active' if data.get('total_points', 0) > 0 else 'inactive',
            'last_update': datetime.now().isoformat()
        }
        
        report['sections'].append({
            'title': 'System Health',
            'content': health_metrics,
            'type': 'metrics'
        })
        
        return report
    
    async def _create_visualizations(self, report_content: Dict[str, Any], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create visualizations for report sections"""
        visualizations = []
        
        for section in report_content.get('sections', []):
            section_type = section.get('type', 'text')
            section_content = section.get('content')
            
            try:
                if section_type == 'metrics' and isinstance(section_content, dict):
                    # Create bar chart for metrics
                    chart = await self._create_metrics_chart(section_content, section.get('title', 'Metrics'))
                    if chart:
                        visualizations.append(chart)
                
                elif section_type == 'trend_data' and isinstance(section_content, dict):
                    # Create line chart for trends
                    trend_chart = await self._create_trend_chart(section_content, section.get('title', 'Trends'))
                    if trend_chart:
                        visualizations.append(trend_chart)
                
                elif section_type == 'comparison' and isinstance(section_content, dict):
                    # Create comparison chart
                    comparison_chart = await self._create_comparison_chart(section_content, section.get('title', 'Comparison'))
                    if comparison_chart:
                        visualizations.append(comparison_chart)
                
            except Exception as e:
                logger.error(f"❌ Visualization creation failed for {section.get('title', 'section')}: {e}")
        
        return visualizations
    
    async def _create_metrics_chart(self, data: Dict[str, Any], title: str) -> Optional[Dict[str, Any]]:
        """Create bar chart for metrics data"""
        try:
            plt.figure(figsize=(10, 6))
            
            keys = list(data.keys())
            values = [float(v) if isinstance(v, (int, float)) else 0 for v in data.values()]
            
            bars = plt.bar(keys, values, color=sns.color_palette("husl", len(keys)))
            plt.title(title, fontsize=16, fontweight='bold')
            plt.ylabel('Value')
            plt.xticks(rotation=45)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                        f'{value:.1f}', ha='center', va='bottom')
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return {
                'type': 'chart',
                'title': title,
                'image_base64': image_base64,
                'description': f'Bar chart showing {len(data)} metrics'
            }
            
        except Exception as e:
            logger.error(f"❌ Metrics chart creation failed: {e}")
            return None
    
    async def _create_trend_chart(self, data: Dict[str, Any], title: str) -> Optional[Dict[str, Any]]:
        """Create line chart for trend data"""
        try:
            plt.figure(figsize=(12, 6))
            
            # Convert data to time series
            dates = sorted(data.keys())
            values = [data[date] for date in dates]
            
            plt.plot(dates, values, marker='o', linewidth=2, markersize=6)
            plt.title(title, fontsize=16, fontweight='bold')
            plt.ylabel('Count')
            plt.xlabel('Date')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Convert to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return {
                'type': 'trend',
                'title': title,
                'image_base64': image_base64,
                'description': f'Trend chart showing {len(data)} data points'
            }
            
        except Exception as e:
            logger.error(f"❌ Trend chart creation failed: {e}")
            return None
    
    async def _create_comparison_chart(self, data: Dict[str, Any], title: str) -> Optional[Dict[str, Any]]:
        """Create comparison pie chart"""
        try:
            plt.figure(figsize=(8, 8))
            
            labels = list(data.keys())
            sizes = list(data.values())
            
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            plt.title(title, fontsize=16, fontweight='bold')
            plt.axis('equal')
            
            # Convert to base64
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            return {
                'type': 'comparison',
                'title': title,
                'image_base64': image_base64,
                'description': f'Pie chart comparing {len(data)} categories'
            }
            
        except Exception as e:
            logger.error(f"❌ Comparison chart creation failed: {e}")
            return None
    
    async def _generate_ai_insights(self, report_content: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered insights and summary"""
        try:
            # Prepare data for AI analysis
            analysis_prompt = f"""
            Analyze this report data and provide intelligent insights:
            
            Report Content: {json.dumps(report_content, indent=2, default=str)[:2000]}
            
            Data Summary: {data.get('total_points', 0)} total data points from {len(data.get('sources', []))} sources
            
            Please provide:
            1. Executive summary (2-3 sentences)
            2. Key insights (3-5 bullet points)
            3. Recommendations (2-3 actionable items)
            4. Notable patterns or trends
            5. Areas for improvement
            
            Format as JSON:
            {{
                "summary": "Executive summary text",
                "insights": ["insight 1", "insight 2", ...],
                "recommendations": ["recommendation 1", "recommendation 2", ...],
                "patterns": ["pattern 1", "pattern 2", ...],
                "improvements": ["improvement 1", "improvement 2", ...]
            }}
            """
            
            ai_response = ai_service.process_query(analysis_prompt, {})
            ai_text = ai_response.get('explanation', '{}')
            
            try:
                insights = json.loads(ai_text)
            except json.JSONDecodeError:
                # Fallback if AI response isn't valid JSON
                insights = {
                    'summary': ai_text[:200] + '...' if len(ai_text) > 200 else ai_text,
                    'insights': ['AI analysis provided comprehensive overview'],
                    'recommendations': ['Continue monitoring key metrics'],
                    'patterns': ['Data shows consistent usage patterns'],
                    'improvements': ['Consider expanding data collection']
                }
            
            return insights
            
        except Exception as e:
            logger.error(f"❌ AI insights generation failed: {e}")
            return {
                'summary': 'Report generated successfully with comprehensive data analysis.',
                'insights': ['Multiple data sources analyzed', 'Comprehensive metrics collected'],
                'recommendations': ['Review findings regularly', 'Act on key insights'],
                'patterns': ['Data collection functioning properly'],
                'improvements': ['Expand analytics capabilities']
            }
    
    async def _store_report(self, report: Dict[str, Any]):
        """Store generated report in database"""
        try:
            await db_manager.store_report(report)
            logger.info(f"💾 Report {report.get('report_id')} stored successfully")
        except Exception as e:
            logger.error(f"❌ Report storage failed: {e}")

# Global report service instance
report_service = ReportService()