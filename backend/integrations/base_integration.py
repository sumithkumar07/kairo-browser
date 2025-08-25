"""
Base Integration Framework for External Services
Provides common interface for all third-party integrations
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseIntegration(ABC):
    """Base class for all external service integrations"""
    
    def __init__(self, service_name: str, config: Dict[str, Any] = None):
        self.service_name = service_name
        self.config = config or {}
        self.authenticated = False
        self.last_error = None
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
        
        logger.info(f"🔌 {service_name} integration initialized")
    
    @abstractmethod
    async def authenticate(self, credentials: Dict[str, Any]) -> bool:
        """Authenticate with the service"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test connection to the service"""
        pass
    
    @abstractmethod
    async def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Search within the service"""
        pass
    
    @abstractmethod
    async def create(self, item_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an item in the service"""
        pass
    
    @abstractmethod
    async def read(self, item_type: str, item_id: str) -> Dict[str, Any]:
        """Read an item from the service"""
        pass
    
    @abstractmethod
    async def update(self, item_type: str, item_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an item in the service"""
        pass
    
    @abstractmethod
    async def delete(self, item_type: str, item_id: str) -> bool:
        """Delete an item from the service"""
        pass
    
    async def get_user_info(self) -> Dict[str, Any]:
        """Get current user information"""
        return {'error': 'Not implemented'}
    
    async def list_items(self, item_type: str, **kwargs) -> List[Dict[str, Any]]:
        """List items from the service"""
        return []
    
    def is_authenticated(self) -> bool:
        """Check if integration is authenticated"""
        return self.authenticated
    
    def get_rate_limit_info(self) -> Dict[str, Any]:
        """Get rate limiting information"""
        return {
            'remaining': self.rate_limit_remaining,
            'reset': self.rate_limit_reset,
            'service': self.service_name
        }
    
    def handle_error(self, error: Exception, context: str = '') -> Dict[str, Any]:
        """Handle and log errors consistently"""
        error_msg = f"{self.service_name} error {context}: {str(error)}"
        logger.error(f"❌ {error_msg}")
        self.last_error = error_msg
        
        return {
            'error': True,
            'message': error_msg,
            'service': self.service_name,
            'context': context
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get integration capabilities"""
        return {
            'service': self.service_name,
            'authenticated': self.authenticated,
            'supports_search': True,
            'supports_create': True,
            'supports_read': True,
            'supports_update': True,
            'supports_delete': True,
            'rate_limited': self.rate_limit_remaining is not None
        }

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass

class RateLimitError(Exception):
    """Raised when rate limit is exceeded"""
    pass

class IntegrationError(Exception):
    """General integration error"""
    pass