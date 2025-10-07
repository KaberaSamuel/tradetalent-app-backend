import os, django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tradetalent_app_backend.settings")

# setup django before loading applications
django.setup()
from chat.middleware import JWTAuthMiddleware
from chat import routing

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddleware(URLRouter(routing.websocket_urlpatterns)),
    }
)
