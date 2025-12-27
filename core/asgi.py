"""
ASGI config for core project.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import main.routing

# --------------------------------------------------
# DO NOT hardcode settings module
# Let Railway ENV decide
# --------------------------------------------------

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(main.routing.websocket_urlpatterns)
        ),
    }
)

