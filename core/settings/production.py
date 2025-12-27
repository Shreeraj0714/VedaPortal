# from .base import *
# import os

# DEBUG = False

# ALLOWED_HOSTS = [
#     ".railway.app",
# ]


# CSRF_TRUSTED_ORIGINS = [
#     "https://*.railway.app",
# ]

# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

from .base import *
import os

# ==============================================
# 1. RESCUE MODE (Fixes 500 Error)
# ==============================================
# We force Debug to True so you can see the site immediately.
DEBUG = True 

# Allow ALL hosts so Railway doesn't block the connection.
ALLOWED_HOSTS = ['*']

# Security: Trust requests from your Railway URL
CSRF_TRUSTED_ORIGINS = ['https://*.railway.app', 'https://*.vercel.app']


# ==============================================
# 2. STATIC FILES (Fixes CSS/Colors)
# ==============================================
# This moves the folder UP one level to /app/staticfiles where Railway looks.
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')

# Use "Safe Mode" storage so the build doesn't crash on missing files.
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

