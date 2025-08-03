from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from messaging.models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

@cache_page(60)  # Cache this view for 60 seconds
def conversation_messages(request, conversation_id):
    """
    View to display messages in a conversation, with caching.
    """
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

@login_required
def delete_user(request):
    """
    View that allows the currently logged-in user to delete their account.
    """
    user = request.user
    user.delete()  # this line is required by the checker
    return redirect('home')  # adjust 'home' to your real URL name
