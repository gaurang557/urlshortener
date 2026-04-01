from django.core.cache import cache
import time
from rest_framework.response import Response


def ratelimited(func):
    def wrapper(request, *args, **kwargs):
        ip = request.META.get('REMOTE_ADDR')

        if is_rate_limited(ip):
            return Response(
                {"error": "Rate limit exceeded. Try again later."},
                status=429
            )
        return func(request,*args, **kwargs)
    return wrapper
def is_rate_limited(ip, limit=100, window=60):
    key = f"rate_limit:{ip}"
    
    data = cache.get(key)

    if not data:
        # First request
        cache.set(key, {"count": 1, "start_time": time.time()}, timeout=window)
        return False

    count = data["count"]
    start_time = data["start_time"]

    if time.time() - start_time < window:
        if count >= limit:
            return True
        else:
            data["count"] += 1
            cache.set(key, data, timeout=window)
            return False
    else:
        # Reset window
        cache.set(key, {"count": 1, "start_time": time.time()}, timeout=window)
        return False