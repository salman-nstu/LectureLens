"""
Configuration settings for AI Lecture Summarizer
Centralized configuration management for the application
"""

import os

# ==================== Application Configuration ====================

class Config:
    """Base configuration class"""
    
    # Application Info
    APP_NAME = "AI Lecture Summarizer"
    VERSION = "2.0.0"
    
    # Server Settings
    HOST = "127.0.0.1"
    PORT = 5000
    DEBUG = True
    
    # File Upload Settings
    UPLOAD_FOLDER = "uploads"
    MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB in bytes
    ALLOWED_EXTENSIONS = {
        'mp3', 'mp4', 'wav', 'avi', 'mov', 
        'flac', 'm4a', 'webm', 'ogg', 'mkv'
    }
    
    # Audio Recording Settings
    AUDIO_SAMPLE_RATE = 44100
    AUDIO_CHANNELS = 1
    AUDIO_DTYPE = 'float32'
    DEFAULT_RECORDING_DURATION = 60  # seconds
    MAX_RECORDING_DURATION = 600  # 10 minutes
    
    # AI Model Configuration
    WHISPER_MODEL = "medium"  # Options: tiny, base, small, medium, large
    SUMMARIZATION_MODEL = "google/flan-t5-large"
    
    # Text Processing Settings
    MAX_CHUNK_WORDS = 1000
    SUMMARY_MAX_LENGTH = 350
    SUMMARY_MIN_LENGTH = 30
    KEYPOINTS_MAX_LENGTH = 400
    KEYPOINTS_MIN_LENGTH = 50
    
    # Export Settings
    OUTPUT_FOLDER = "outputs"
    PDF_FILENAME = "lecture_summary.pdf"
    WORD_FILENAME = "lecture_summary.docx"
    JSON_FILENAME = "lecture_summary.json"
    
    # YouTube Download Settings
    YOUTUBE_AUDIO_FORMAT = 'bestaudio/best'
    YOUTUBE_AUDIO_QUALITY = '192'
    YOUTUBE_OUTPUT_TEMPLATE = 'youtube_audio.%(ext)s'
    
    # CORS Settings
    CORS_ORIGINS = "*"  # In production, specify allowed origins
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    CORS_ORIGINS = ["https://yourdomain.com"]  # Specify allowed origins
    
    # Use environment variables for sensitive settings
    HOST = os.getenv("APP_HOST", "0.0.0.0")
    PORT = int(os.getenv("APP_PORT", 5000))


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    WHISPER_MODEL = "tiny"  # Use smaller model for faster tests


# ==================== Configuration Selection ====================

def get_config(env=None):
    """
    Get configuration based on environment
    
    Args:
        env (str): Environment name ('development', 'production', 'testing')
        
    Returns:
        Config: Configuration object
    """
    if env is None:
        env = os.getenv("FLASK_ENV", "development")
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    return config_map.get(env.lower(), DevelopmentConfig)


# ==================== Export Default Config ====================

# Default configuration for import
config = get_config()
