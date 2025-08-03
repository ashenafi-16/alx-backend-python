from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory, User

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.pk:  # Only for existing messages
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                content=original.content
            )
            instance.edited = True

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete all related objects
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()