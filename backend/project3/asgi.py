"""
ASGI config for project3 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
# new
from channels.routing import ProtocolTypeRouter, URLRouter
from posts.routing  import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project3.settings")

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": URLRouter(websocket_urlpatterns)
})

# async def application(scope, receive, send):
#     await websocket_application(scope, receive, send)