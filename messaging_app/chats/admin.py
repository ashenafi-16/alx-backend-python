from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Message, Conversation

# Register your models for the admin interface
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(get_user_model())
