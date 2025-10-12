from rest_framework import generics
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    ordering = ("-timestamp",)


class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        queryset = Conversation.objects.filter(name__contains=self.request.user.slug)
        return queryset

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}
