import requests, hashlib
from django.utils import timezone
from ipware import get_client_ip
from cachetools.func import ttl_cache
from django.db import models

from .crawler_detection import is_crawler

@ttl_cache
def get_country(ip):
    try:
        response = requests.get(f"https://geolocation-db.com/json/{ip}", timeout=5)
        if (name := response.json().get("country_name", "Not found")) != "Not found":
            return name
    except requests.Timeout:
        pass
    except requests.RequestException as e:
        print(f"warning, failed to get_country with: {e}")

    return None

class IPAddress(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.GenericIPAddressField(unique=True)
    ip_hash = models.CharField(max_length=40)

    @classmethod
    def get_or_create(cls, ip_string):
        ip, created = cls.objects.get_or_create(ip=ip_string)
        if created:
            ip.ip_hash = hashlib.sha1(ip_string.encode()).hexdigest()
            ip.save()

        return ip

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)

    @classmethod
    def get_or_create(cls, country):
        return cls.objects.get_or_create(name=country)[0]

class URL(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=128, unique=True)

    @classmethod
    def get_or_create(cls, url):
        return cls.objects.get_or_create(url=url)[0]

class UserAgent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)

    @classmethod
    def get_or_create(cls, user_agent):
        return cls.objects.get_or_create(name=user_agent)[0]

class Visit(models.Model):
    id          = models.AutoField(primary_key=True)
    timestamp   = models.DateTimeField()
    ip          = models.ForeignKey(IPAddress, on_delete=models.PROTECT)
    country     = models.ForeignKey(Country, on_delete=models.PROTECT)
    url         = models.ForeignKey(URL, on_delete=models.PROTECT)
    status_code = models.IntegerField()
    is_crawler  = models.BooleanField()
    user_agent  = models.ForeignKey(UserAgent, on_delete=models.PROTECT)

    @classmethod
    def create(cls, request, response):
        ip, _ = get_client_ip(request)
        country = c if ip and (c := get_country(ip)) else "unknown"
        user_agent = request.META.get("HTTP_USER_AGENT", "None")

        visit = cls.objects.create(
            timestamp=timezone.now(),
            ip=IPAddress.get_or_create(ip),
            country=Country.get_or_create(country),
            url=URL.get_or_create(f"{request.get_host()}{request.path}"),
            status_code=response.status_code,
            is_crawler=is_crawler(user_agent),
            user_agent=UserAgent.get_or_create(user_agent),
        )
        visit.save()

        return visit

    def __str__(self):
        return f"{self.timestamp} {self.ip} {self.url}"

    def __lt__(self, other):
        return self.timestamp < other.timestamp
