def get_thread(root_message):
    return Message.objects.filter(
        pk=root_message.pk
    ).prefetch_related(
        models.Prefetch(
            'replies',
            queryset=Message.objects.all().prefetch_related('replies')
        )
    ).first()