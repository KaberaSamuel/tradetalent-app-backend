from django.urls import path
from .views import MessageList, ConversationViewSet
from .consumers import ChatConsumer


urlpatterns = [
    path("conversations/", ConversationViewSet.as_view({"get": "list"})),
    path("messages/", MessageList.as_view()),
    path("<slug>/", ChatConsumer.as_asgi()),
]
