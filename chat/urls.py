from django.urls import path
from .views import MessageList
from .consumers import ChatConsumer

urlpatterns = [
    path("messages/", MessageList.as_view()),
    path("<slug>/", ChatConsumer.as_asgi()),
]
