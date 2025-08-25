"""
Configuration settings for Kairo AI Browser Backend
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Database Configuration
    MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017/kairo_browser")
    
    # AI Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3-8b-8192")
    
    # Browser Configuration
    PLAYWRIGHT_BROWSERS_PATH: str = os.getenv("PLAYWRIGHT_BROWSERS_PATH", "/pw-browsers")
    
    # Security Configuration
    CORS_ORIGINS: list = ["*"]  # In production, specify exact origins
    
    # Performance Configuration
    HTTP_TIMEOUT: float = 30.0
    BROWSER_TIMEOUT: float = 45000  # milliseconds
    MAX_CONNECTIONS: int = 10
    
    # Proxy Configuration
    HEAVY_JS_SITES: list = [
        'youtube.com', 'gmail.com', 'docs.google.com', 'sheets.google.com',
        'facebook.com', 'instagram.com', 'twitter.com', 'x.com',
        'linkedin.com', 'reddit.com', 'discord.com', 'slack.com',
        'notion.so', 'figma.com', 'canva.com', 'whatsapp.com'
    ]

# Global settings instance
settings = Settings()