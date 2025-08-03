import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_before = django_filters.IsoDateTimeFilter(field_name='timestamp', lookup_expr='lte')
    sent_after = django_filters.IsoDateTimeFilter(field_name='timestamp', lookup_expr='gte')
    sender = django_filters.NumberFilter(field_name='sender__id')

    class Meta:
        model = Message
        fields = ['sender', 'sent_before', 'sent_after']
