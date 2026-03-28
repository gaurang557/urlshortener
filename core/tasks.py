from celery import shared_task
from .models import URL
from django.core.cache import cache
from django.db.models import F


@shared_task
def flush_click_counts():
    redis_client = cache._cache.get_client()
    c = 0
    while True:
        c, keys = redis_client.scan(cursor=c, match="*count:*", count=100)
        for key in keys:
            code = key.decode().split(":")[-1]
            count = int(redis_client.get(key))

            URL.objects.filter(short_code=code).update(
                clicks= F('clicks') + count
            )
            redis_client.delete(key)
        if c == 0:
            break