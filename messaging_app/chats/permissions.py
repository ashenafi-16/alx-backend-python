from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it.
    """

    def has_permission(self, request, view):
        # ✅ Ensure user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Messages: check if request.user is part of obj.conversation.participants
        - Conversations: check if user is in obj.participants
        """
        # Handle messages
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        
        # Handle conversations
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()
        
        return False
