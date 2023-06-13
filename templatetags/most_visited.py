from ..models import Visit

from cachetools.func import ttl_cache
from django.utils import timezone
from datetime import timedelta
from django import template
register = template.Library()

@register.simple_tag
@ttl_cache(ttl=60)
def most_visited(n=32, days=30):
    date_threshold = timezone.now() - timedelta(days=days)
    visits = Visit.objects.filter(timestamp__gt=date_threshold)
    return _most_visited(visits)[:n]

@register.simple_tag
@ttl_cache(ttl=3600)
def most_visited_all():
    return _most_visited(Visit.objects.all())

def _most_visited(visits):
    urls = visits.values_list("url", flat=True).distinct()
    counts = (visits.filter(url=url).values("ip").distinct().count() for url in urls)
    return sorted(zip(counts, urls), reverse=True)
