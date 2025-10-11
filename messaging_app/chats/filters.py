from django_filters import rest_framework as filters
from .models import Chat, Message

class ChatFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Chat
        fields = ['name', 'created_at']

class MessageFilter(filters.FilterSet):
    sender = filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    chat = filters.NumberFilter(field_name='chat__id')
    timestamp = filters.DateFromToRangeFilter(field_name='timestamp')

    class Meta:
        model = Message
        fields = ['sender', 'chat', 'timestamp']