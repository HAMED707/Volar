# backend/settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(",")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True