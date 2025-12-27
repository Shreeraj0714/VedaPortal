"""
Django settings for core project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# ✅ CORRECT (Standard Django structure)
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# =========================
# SECURITY (RESCUE MODE)
# =========================
SECRET_KEY = 'django-insecure-change-this-later'

# ✅ DEBUG = True prevents the 500 Server Error
DEBUG = True

# ✅ ALLOWED_HOSTS: accepting all temporarily to ensure site loads
ALLOWED_HOSTS = ['*']

# CSRF Trusted Origins (Helps with login issues)
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-5294.up.railway.app',
    'https://*.railway.app',
    'https://*.vercel.app'
]


# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'channels',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'main.apps.MainConfig',
    'api.apps.ApiConfig',
]


# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ Correctly placed
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =========================
# ASGI / CHANNELS
# =========================
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# =========================
# DATABASE
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.xkbjeuwbsfcnvfjshdvb',
        'PASSWORD': 'sHreeraj@2005',
        'HOST': 'aws-1-ap-southeast-2.pooler.supabase.com',
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
    }
}


# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# =========================
# STATIC FILES (THE FIX)
# =========================
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ This moves the folder UP one level so Railway can find it
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')

# ✅ Safe Mode storage (Prevents build crashes)
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


# =========================
# CKEDITOR
# =========================
CKEDITOR_UPLOAD_PATH = "uploads/"


# =========================
# DEFAULT FIELD TYPE
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'