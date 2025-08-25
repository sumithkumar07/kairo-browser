"""
Kairo AI Browser - Enhanced Modular Backend
Main application entry point with improved architecture
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time

# Import configuration and routes
from config import settings
from api.routes import router
from api.ultimate_enhanced_routes import router as ultimate_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    # Startup
    logger.info("🚀 Starting Kairo AI Browser Backend...")
    
    # Initialize services (they're already initialized when imported)
    from services.ai_service import ai_service
    from services.browser_service import browser_service
    from services.proxy_service import proxy_service
    from services.workflow_service import workflow_service
    from database.mongodb import db_manager
    
    logger.info("✅ All services initialized")
    
    # Cleanup old sessions on startup
    browser_service.cleanup_inactive_sessions(max_age_hours=24)
    
    logger.info("🎉 Kairo AI Browser Backend started successfully!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Kairo AI Browser Backend...")
    
    # Cleanup resources if needed
    try:
        if hasattr(db_manager, 'client') and db_manager.client:
            db_manager.client.close()
            logger.info("📡 Database connection closed")
    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")
    
    logger.info("👋 Kairo AI Browser Backend shutdown complete")

# Create FastAPI app with enhanced configuration
app = FastAPI(
    title="Kairo AI Browser Backend",
    description="Enhanced AI-powered browser with smart proxy routing and automation capabilities",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # In production, specify exact hosts
)

# CORS middleware with enhanced configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for debugging"""
    start_time = time.time()
    
    # Log request
    logger.info(f"📥 {request.method} {request.url.path} - {request.client.host}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"📤 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"❌ Unhandled exception on {request.method} {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "path": str(request.url.path),
            "method": request.method
        }
    )

# Include API routes
app.include_router(router, prefix="/api")
app.include_router(ultimate_router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🌐 Kairo AI Browser Backend",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health"
    }

# Health check endpoint (also available at root level)
@app.get("/health")
async def health():
    """Simple health check"""
    return {"status": "healthy", "service": "kairo-browser-backend"}

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Kairo AI Browser Backend directly...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,  # Set to True for development
        log_level="info",
        access_log=True
    )