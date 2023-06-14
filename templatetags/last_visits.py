from ..models import Visit

from django.utils import timezone
from datetime import timedelta
from django import template
register = template.Library()

@register.simple_tag
def last_visits(n=128, days=7):
    date_threshold = timezone.now() - timedelta(days=days)
    visits = Visit.objects.filter(is_crawler=False, timestamp__gt=date_threshold)
    return sorted(visits, reverse=True)[:n]
