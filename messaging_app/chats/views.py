from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from rest_framework import filters
# Conversation ViewSet

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants")
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    # Enable filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["participants"]   # allows ?participants=<user_id>
    search_fields = ["participants__email"]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants", [])
        if not participants or len(participants) < 2:
            return Response(
                {"detail": "A conversation must have at least 2 participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # Enable filtering (e.g., ?conversation_id=<uuid>)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["conversation"]
    ordering_fields = ["sent_at"]
    ordering = ["sent_at"]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation__id=conversation_id, conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        message_body = request.data.get("message_body")

        conversation = get_object_or_404(Conversation, pk=conversation_id)

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class SomeChatView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    # ...existing code...

class MessageFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        conversation_id = view.kwargs.get('conversation_pk')
        if conversation_id:
            return queryset.filter(conversation__id=conversation_id)
        return queryset 
    