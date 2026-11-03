"""
ThreadLab Backend Configuration.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "threadlab-super-secret-key-2026")
    JSON_SORT_KEYS = False
    DEBUG = True
    PORT = int(os.environ.get("PORT", 5000))
    HOST = os.environ.get("HOST", "127.0.0.1")

class TestingConfig(Config):
    TESTING = True
    DEBUG = False

