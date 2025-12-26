from .base import *
import os

# =========================
# PRODUCTION SETTINGS
# =========================
DEBUG = False

# Allowed hosts (Railway + future domain)
ALLOWED_HOSTS = [
    ".railway.app",
    "vedaportal.com",
    ".vedaportal.com",
]

# CSRF protection (Railway)
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://vedaportal.com",
    "https://*.vedaportal.com",
]

# =========================
# STATIC FILES (PRODUCTION)
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# =========================
# SECURITY (REQUIRED FOR RAILWAY)
# =========================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = False  # Railway already handles HTTPS

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
