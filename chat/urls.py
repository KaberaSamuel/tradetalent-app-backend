from django.urls import path
from .views import MessageList, ConversationListCreateView
from .consumers import ChatConsumer


urlpatterns = [
    path("conversations/", ConversationListCreateView.as_view()),
    path("messages/", MessageList.as_view()),
    path("<slug>/", ChatConsumer.as_asgi()),
]
