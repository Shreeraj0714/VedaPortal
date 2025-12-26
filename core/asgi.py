"""
ASGI config for core project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing  # This file will link the URL to your Consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize the standard Django ASGI application early
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # Standard HTTP requests
    "http": django_asgi_app,

    # WebSocket connections (Real-time logout signals)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})