from django.db import models
from django.contrib.auth.models import User  # or use get_user_model() if you prefer
from .managers import UnreadMessagesManager  # Custom manager for unread messages


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Edit tracking
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name='edited_messages',
        on_delete=models.SET_NULL
    )
    
    # Threading (self-referencing FK)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    
    # Read tracking
    read = models.BooleanField(default=False)
    
    # Managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}: {self.content[:20]}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name='history', on_delete=models.CASCADE
    )
    content = models.TextField()  # old content before edit
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message {self.message.id} edited at {self.edited_at}"
