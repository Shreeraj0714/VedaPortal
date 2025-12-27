"""
WSGI config for core project.
"""

import os
from django.core.wsgi import get_wsgi_application

# --------------------------------------------------
# Force production settings on Railway
# --------------------------------------------------
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings.production"
)

application = get_wsgi_application()
