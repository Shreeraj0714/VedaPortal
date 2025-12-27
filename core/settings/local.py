from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    '*',                                    # ✅ Comma added
    "web-production-5294.up.railway.app",
    '.railway.app',
    ".vercel.app",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://*.vercel.app']