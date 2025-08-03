# chats/views.py

from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from messaging.models import Conversation, Message  # Adjust import if your models are elsewhere

@cache_page(60)  # cache this view for 60 seconds
def conversation_messages(request, conversation_id):
    """
    Display messages in a conversation, cached for 60 seconds.
    """
    # Retrieve the conversation object
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Retrieve and optimize related messages
    messages = (
        Message.objects
        .filter(conversation=conversation)
        .select_related('sender')  # optimize sender foreign key
        .only('content', 'timestamp', 'sender__username')  # load only needed fields
        .order_by('timestamp')
    )
    
    # Render to template
    return render(request, 'chats/messages.html', {
        'conversation': conversation,
        'messages': messages,
    })
