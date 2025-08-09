# -*- coding: utf-8 -*-
"""
إعدادات منصة تواصل
"""

import os
from datetime import timedelta

class Config:
    """إعدادات التطبيق الأساسية"""
    
    # المفتاح السري للتطبيق
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey-tawasol-2024'
    
    # إعدادات قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # إعدادات رفع الملفات
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20MB للمنشورات
    UPLOAD_FOLDER = 'static/uploads'
    ALLOWED_EXTENSIONS = {
        'images': {'png', 'jpg', 'jpeg', 'gif', 'webp'},
        'videos': {'mp4', 'avi', 'mov', 'wmv', 'webm'},
        'files': {'pdf', 'doc', 'docx', 'txt', 'zip', 'rar'}
    }
    
    # إعدادات الجلسة
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # True في الإنتاج مع HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # إعدادات الأمان
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # إعدادات التطبيق
    POSTS_PER_PAGE = 10
    MESSAGES_PER_PAGE = 50
    SEARCH_RESULTS_PER_PAGE = 20
    
    # إعدادات الوسائط في المحادثات
    MESSAGE_MEDIA_MAX_SIZE = 10 * 1024 * 1024  # 10MB للمحادثات
    
    # إعدادات التطوير
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    """إعدادات التطوير"""
    DEBUG = True
    SQLALCHEMY_ECHO = False  # عرض استعلامات SQL

class ProductionConfig(Config):
    """إعدادات الإنتاج"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///production.db'

class TestingConfig(Config):
    """إعدادات الاختبار"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# تحديد الإعدادات حسب البيئة
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}