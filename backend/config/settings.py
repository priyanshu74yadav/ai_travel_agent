"""
Configuration settings for the Flask application.
Loads environment variables from .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # RapidAPI Travel Advisor Configuration
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
    RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "travel-advisor.p.rapidapi.com")
    
    # Server Configuration
    PORT = int(os.getenv("PORT", 5000))
    
    # Feature Flags
    USE_REAL_API = os.getenv("USE_REAL_API", "false").lower() == "true"
    
    # Flask Configuration
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"


