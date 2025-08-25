"""
Notion Integration - Connect with Notion workspace
Provides search, create, read, update operations for Notion content
"""
import httpx
import logging
from typing import Dict, Any, List, Optional
from integrations.base_integration import BaseIntegration, AuthenticationError, RateLimitError

logger = logging.getLogger(__name__)

class NotionIntegration(BaseIntegration):
    """Notion workspace integration"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__('Notion', config)
        self.base_url = 'https://api.notion.com/v1'
        self.headers = {
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
        self.client = None
    
    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with Notion API"""
        try:
            token = credentials.get('token') or credentials.get('integration_token')
            if not token:
                raise AuthenticationError("Notion integration token required")
            
            self.headers['Authorization'] = f'Bearer {token}'
            
            # Create HTTP client
            self.client = httpx.AsyncClient(
                headers=self.headers,
                timeout=30.0
            )
            
            # Test authentication
            response = await self.client.get(f'{self.base_url}/users/me')
            
            if response.status_code == 200:
                self.authenticated = True
                logger.info("✅ Notion authentication successful")
                return True
            else:
                raise AuthenticationError(f"Authentication failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Notion authentication failed: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test connection to Notion"""
        if not self.authenticated or not self.client:
            return False
        
        try:
            response = await self.client.get(f'{self.base_url}/users/me')
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ Notion connection test failed: {e}")
            return False
    
    async def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search Notion workspace"""
        if not self.authenticated:
            return {'error': 'Not authenticated with Notion'}
        
        try:
            search_payload = {
                'query': query,
                'filter': {
                    'value': 'page',
                    'property': 'object'
                }
            }
            
            # Add additional filters from kwargs
            page_size = kwargs.get('page_size', 10)
            search_payload['page_size'] = min(page_size, 100)
            
            response = await self.client.post(
                f'{self.base_url}/search',
                json=search_payload
            )
            
            if response.status_code == 200:
                data = response.json()
                
                results = []
                for page in data.get('results', []):
                    result = {
                        'id': page.get('id'),
                        'title': self._extract_page_title(page),
                        'url': page.get('url'),
                        'last_edited': page.get('last_edited_time'),
                        'created': page.get('created_time'),
                        'type': 'notion_page'
                    }
                    results.append(result)
                
                return {
                    'results': results,
                    'total': len(results),
                    'has_more': data.get('has_more', False)
                }
            
            return self.handle_error(Exception(f"Search failed: {response.status_code}"))
            
        except Exception as e:
            return self.handle_error(e, 'search')
    
    async def create(self, item_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create item in Notion"""
        if not self.authenticated:
            return {'error': 'Not authenticated with Notion'}
        
        try:
            if item_type == 'page':
                return await self._create_page(data)
            elif item_type == 'database':
                return await self._create_database(data)
            else:
                return {'error': f'Unsupported item type: {item_type}'}
                
        except Exception as e:
            return self.handle_error(e, f'create {item_type}')
    
    async def read(self, item_type: str, item_id: str) -> Dict[str, Any]:
        """Read item from Notion"""
        if not self.authenticated:
            return {'error': 'Not authenticated with Notion'}
        
        try:
            if item_type == 'page':
                response = await self.client.get(f'{self.base_url}/pages/{item_id}')
            elif item_type == 'database':
                response = await self.client.get(f'{self.base_url}/databases/{item_id}')
            elif item_type == 'block':
                response = await self.client.get(f'{self.base_url}/blocks/{item_id}')
            else:
                return {'error': f'Unsupported item type: {item_type}'}
            
            if response.status_code == 200:
                return response.json()
            
            return self.handle_error(Exception(f"Read failed: {response.status_code}"))
            
        except Exception as e:
            return self.handle_error(e, f'read {item_type}')
    
    async def update(self, item_type: str, item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update item in Notion"""
        if not self.authenticated:
            return {'error': 'Not authenticated with Notion'}
        
        try:
            if item_type == 'page':
                response = await self.client.patch(
                    f'{self.base_url}/pages/{item_id}',
                    json=data
                )
            elif item_type == 'database':
                response = await self.client.patch(
                    f'{self.base_url}/databases/{item_id}',
                    json=data
                )
            else:
                return {'error': f'Unsupported item type: {item_type}'}
            
            if response.status_code == 200:
                return response.json()
            
            return self.handle_error(Exception(f"Update failed: {response.status_code}"))
            
        except Exception as e:
            return self.handle_error(e, f'update {item_type}')
    
    async def delete(self, item_type: str, item_id: str) -> bool:
        """Delete (archive) item in Notion"""
        if not self.authenticated:
            return False
        
        try:
            # Notion doesn't support true deletion, only archiving
            data = {'archived': True}
            
            if item_type == 'page':
                response = await self.client.patch(
                    f'{self.base_url}/pages/{item_id}',
                    json=data
                )
            elif item_type == 'database':
                response = await self.client.patch(
                    f'{self.base_url}/databases/{item_id}',
                    json=data
                )
            else:
                return False
            
            return response.status_code == 200
            
        except Exception as e:
            self.handle_error(e, f'delete {item_type}')
            return False
    
    async def list_items(self, item_type: str, **kwargs) -> List[Dict[str, Any]]:
        """List items from Notion"""
        if not self.authenticated:
            return []
        
        try:
            if item_type == 'databases':
                # List all databases
                response = await self.client.post(
                    f'{self.base_url}/search',
                    json={
                        'filter': {
                            'value': 'database',
                            'property': 'object'
                        }
                    }
                )
            elif item_type == 'pages':
                # List all pages
                response = await self.client.post(
                    f'{self.base_url}/search',
                    json={
                        'filter': {
                            'value': 'page',
                            'property': 'object'
                        }
                    }
                )
            else:
                return []
            
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            
            return []
            
        except Exception as e:
            self.handle_error(e, f'list {item_type}')
            return []
    
    async def _create_page(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Notion page"""
        parent_id = data.get('parent_id')
        title = data.get('title', 'Untitled')
        content = data.get('content', '')
        
        if not parent_id:
            return {'error': 'parent_id required for page creation'}
        
        page_data = {
            'parent': {
                'type': 'page_id',
                'page_id': parent_id
            },
            'properties': {
                'title': {
                    'title': [
                        {
                            'text': {
                                'content': title
                            }
                        }
                    ]
                }
            }
        }
        
        # Add content blocks if provided
        if content:
            page_data['children'] = [
                {
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {
                                    'content': content
                                }
                            }
                        ]
                    }
                }
            ]
        
        response = await self.client.post(
            f'{self.base_url}/pages',
            json=page_data
        )
        
        if response.status_code == 200:
            return response.json()
        
        raise Exception(f"Page creation failed: {response.status_code}")
    
    async def _create_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Notion database"""
        # Implementation for database creation
        return {'error': 'Database creation not yet implemented'}
    
    def _extract_page_title(self, page: Dict[str, Any]) -> str:
        """Extract title from Notion page object"""
        try:
            properties = page.get('properties', {})
            
            # Look for title property
            for prop_name, prop_data in properties.items():
                if prop_data.get('type') == 'title':
                    title_array = prop_data.get('title', [])
                    if title_array:
                        return title_array[0].get('plain_text', 'Untitled')
            
            return 'Untitled'
            
        except Exception:
            return 'Untitled'
    
    async def get_user_info(self) -> Dict[str, Any]:
        """Get current user information from Notion"""
        if not self.authenticated:
            return {'error': 'Not authenticated with Notion'}
        
        try:
            response = await self.client.get(f'{self.base_url}/users/me')
            
            if response.status_code == 200:
                return response.json()
            
            return self.handle_error(Exception(f"User info failed: {response.status_code}"))
            
        except Exception as e:
            return self.handle_error(e, 'get user info')

# Create global instance
notion_integration = NotionIntegration()