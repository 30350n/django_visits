from datetime import timedelta

from cachetools.func import ttl_cache
from django import template
from django.utils import timezone

from ..models import Visit

register = template.Library()


@register.simple_tag
@ttl_cache(ttl=60)
def most_visited(n=32, days=30):
    date_threshold = timezone.now() - timedelta(days=days)
    visits = Visit.objects.filter(is_crawler=False, timestamp__gt=date_threshold)
    return _most_visited(visits)[:n]


@register.simple_tag
@ttl_cache(ttl=3600)
def most_visited_all():
    return _most_visited(Visit.objects.filter(is_crawler=False))


def _most_visited(visits):
    url_ids, urls = tuple(zip(*visits.values_list("url", "url__url").distinct()))
    counts = (visits.filter(url=url).values("ip").distinct().count() for url in url_ids)
    return sorted(zip(counts, urls), reverse=True)
