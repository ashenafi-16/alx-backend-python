# messaging/views.py

from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from messaging.models import Conversation, Message  # adjust if needed

@cache_page(60)  # cache this view for 60 seconds
def conversation_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = (
        Message.objects
        .filter(conversation=conversation)
        .select_related('sender')
        .only('content', 'timestamp', 'sender__username')
        .order_by('timestamp')
    )
    return render(request, 'chats/messages.html', {
        'conversation': conversation,
        'messages': messages,
    })
