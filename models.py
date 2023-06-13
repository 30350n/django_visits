import requests, hashlib
from django.utils import timezone
from ipware import get_client_ip
from cachetools.func import ttl_cache
from functools import cache
from django.db import models

@ttl_cache
def get_country(ip):
    response = requests.get(f"https://geolocation-db.com/json/{ip}")
    return name if (name := response.json().get("country_name")) != "Not found" else None

@cache
def ip_hash(ip):
    return hashlib.sha1(ip.encode()).hexdigest()

class Visit(models.Model):
    id          = models.AutoField(primary_key=True)
    timestamp   = models.DateTimeField()
    ip          = models.GenericIPAddressField()
    ip_sha1     = models.CharField(max_length=40)
    country     = models.CharField(max_length=64)
    url         = models.CharField(max_length=128)
    status_code = models.IntegerField()

    @classmethod
    def create(cls, request, response):
        ip, _ = get_client_ip(request)
        country = c if ip and (c := get_country(ip)) else "unknown"
        return cls(
            timestamp=timezone.now(),
            ip=ip, ip_sha1=ip_hash(ip),
            country=country,
            url=f"{request.get_host()}{request.path}",
            status_code=response.status_code,
        )

    def __str__(self):
        return f"{self.timestamp} {self.ip} {self.url}"

    def __lt__(self, other):
        return self.timestamp < other.timestamp
