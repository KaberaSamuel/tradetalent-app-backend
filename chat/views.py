from rest_framework import generics
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer


class MessageList(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    ordering = ("-timestamp",)


class ConversationListCreateView(ListCreateAPIView):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()

    def get_queryset(self):
        queryset = Conversation.objects.filter(name__contains=self.request.user.slug)
        return queryset

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}

    def create(self, request, *args, **kwargs):
        conversation_name = request.data.get("conversationName", "")

        if conversation_name == "":
            return Response({"message": "No conversation name provided"}, status=400)

        # create conversation in the db if not exists
        conversation,_ = Conversation.objects.get_or_create(name=conversation_name)
        serializer_context = {"request": self.request, "user": self.request.user}
        serializer = ConversationSerializer(conversation, context=serializer_context)
        return Response({"conversation": serializer.data}, status=201)
