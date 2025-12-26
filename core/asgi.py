"""
ASGI config for core project.
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import main.routing

# --------------------------------------------------
# FORCE Django settings module (OVERRIDES EVERYTHING)
# --------------------------------------------------
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings.local"

django.setup()

# --------------------------------------------------
# Django ASGI application
# --------------------------------------------------
django_asgi_app = get_asgi_application()

# --------------------------------------------------
# Protocol router
# --------------------------------------------------
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                main.routing.websocket_urlpatterns
            )
        ),
    }
)
