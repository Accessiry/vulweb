import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'uploads')
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB max file size
    ALLOWED_EXTENSIONS = {'py', 'json', 'csv', 'txt', 'zip', 'pkl', 'pt', 'pth', 'h5'}
    
    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    
    # Training settings
    TRAINING_OUTPUT_FOLDER = os.path.join(basedir, '..', 'training_outputs')
    
    # AI/LLM configuration
    AI_PROVIDER = os.environ.get('AI_PROVIDER') or 'none'  # qwen, ernie, zhipu, openai, none
    AI_API_KEY = os.environ.get('AI_API_KEY') or ''
    AI_SECRET_KEY = os.environ.get('AI_SECRET_KEY') or ''  # For ERNIE
    AI_ENDPOINT = os.environ.get('AI_ENDPOINT') or ''
    AI_MODEL = os.environ.get('AI_MODEL') or 'qwen-turbo'
    
    @staticmethod
    def init_app(app):
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.TRAINING_OUTPUT_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
