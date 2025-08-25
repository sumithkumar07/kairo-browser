"""
Pydantic models for API request/response schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

class BrowserCommand(BaseModel):
    """Browser command schema"""
    command: str = Field(..., description="Command type: open, click, type, etc.")
    url: Optional[str] = Field(None, description="URL for navigation commands")
    selector: Optional[str] = Field(None, description="CSS selector for element interaction")
    text: Optional[str] = Field(None, description="Text to type or search")
    session_id: Optional[str] = Field(None, description="Browser session identifier")
    
    @validator('url')
    def validate_url(cls, v):
        if v and not re.match(r'^https?://', v) and not v.startswith('//'):
            # Auto-add https:// if missing
            return f"https://{v}"
        return v

class AIQuery(BaseModel):
    """AI query schema"""
    query: str = Field(..., min_length=1, max_length=1000, description="User's natural language query")
    session_id: Optional[str] = Field(None, description="Session identifier for context")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional context")
    
class WorkflowStep(BaseModel):
    """Individual workflow step schema"""
    type: str = Field(..., description="Step type: open, click, type, wait_for, extract, screenshot")
    url: Optional[str] = Field(None, description="URL for navigation steps")
    selector: Optional[str] = Field(None, description="CSS selector for element interaction")
    text: Optional[str] = Field(None, description="Text input for type steps")
    timeout_ms: Optional[int] = Field(5000, description="Timeout in milliseconds")
    
class Workflow(BaseModel):
    """Workflow execution schema"""
    name: str = Field(..., min_length=1, max_length=100, description="Workflow name")
    steps: List[WorkflowStep] = Field(..., description="List of workflow steps")
    profile: Optional[str] = Field("default", description="Browser profile to use")
    timeout_ms: Optional[int] = Field(60000, description="Total workflow timeout")

class ProxyRequest(BaseModel):
    """Proxy request schema"""
    url: str = Field(..., description="URL to proxy")
    method: Optional[str] = Field("GET", description="HTTP method")
    headers: Optional[Dict[str, str]] = Field(default_factory=dict, description="Custom headers")
    
    @validator('url')
    def validate_proxy_url(cls, v):
        if not re.match(r'^https?://', v):
            return f"https://{v}"
        return v

class APIResponse(BaseModel):
    """Standard API response schema"""
    status: str = Field(..., description="Response status: success, error")
    message: str = Field(..., description="Human readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

class HealthCheck(BaseModel):
    """Health check response schema"""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
    services: Dict[str, str] = Field(default_factory=dict)