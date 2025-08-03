from django.views.decorators.cache import cache_page
from django.shortcuts import render, get_object_or_404
from messaging.models import Conversation, Message  # Adjust to your models

@cache_page(60)  # 60 seconds cache
def conversation_messages(request, conversation_id):
    # Get conversation
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Get messages with optimization
    messages = Message.objects.filter(
        conversation=conversation
    ).select_related('sender').only(
        'content', 'timestamp', 'sender__username'
    ).order_by('timestamp')
    
    return render(request, 'chats/messages.html', {
        'conversation': conversation,
        'messages': messages
    })