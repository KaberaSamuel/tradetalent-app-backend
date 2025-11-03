from django.urls import path
from .consumers import ChatConsumer, ChatNotificationConsumer

websocket_urlpatterns = [
    path("notifications/", ChatNotificationConsumer.as_asgi()),
    path("<conversation_name>/", ChatConsumer.as_asgi()),
]
