import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-not-for-production')
    DEBUG = False
    TESTING = False
    AUTO_MIGRATE = False

    # Database
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    REDIS_URL = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"

    # API
    API_TITLE = 'Task Management API'
    API_VERSION = 'v1'
    API_PREFIX = '/api'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    AUTO_MIGRATE = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    AUTO_MIGRATE = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}_test"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    AUTO_MIGRATE = True
    # Use a strong secret key in production
    SECRET_KEY = os.getenv('SECRET_KEY')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# Get configuration based on environment
def get_config():
    env = os.getenv('APP_ENV', 'default')
    return config.get(env.lower(), config['default'])
