from celery import shared_task
from .models import URL

@shared_task
def increment_clicks(short_code):
    print("Hi")
    try:
        url = URL.objects.get(short_code=short_code)
        url.clicks += 1
        url.save()
    except URL.DoesNotExist:
        pass