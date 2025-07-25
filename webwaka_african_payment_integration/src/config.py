"""
WebWaka Universal African Payment Integration Framework Configuration
===================================================================

Production configuration settings for HTTPS and security.
"""

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdf#FGSgvasgf$5$WGT'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # HTTPS Configuration
    PREFERRED_URL_SCHEME = 'https'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS Configuration
    CORS_ORIGINS = ['*']
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']

class DevelopmentConfig(Config):
    DEBUG = True
    PREFERRED_URL_SCHEME = 'http'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    PREFERRED_URL_SCHEME = 'https'
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
