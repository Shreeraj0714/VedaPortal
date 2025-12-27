from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "web-production-5294.up.railway.app",  # <--- Add this!
    ".vercel.app",                         # <--- Add this for frontend!
    "127.0.0.1",
    "localhost",
]

# Security: Trust requests from your Railway URL
CSRF_TRUSTED_ORIGINS = [
    "https://web-production-5294.up.railway.app",
]