import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from board import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ci1.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/board/", consumers.BoardConsumer.as_asgi()),
        ])
    ),
})
