from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    ".railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
]

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Security
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
