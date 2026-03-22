from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import URL
from .serializers import URLSerializer
from .utils import *
from .tasks import increment_clicks
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@api_view(['POST'])
@ratelimited
def create_short_url(request):
    serializer = URLSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return Response({
            "short_url": f"http://localhost:8000/{obj.short_code}"
        })
    return Response(serializer.errors, status=400)

def redirect_url(request, code):
    cache_key = f"url:{code}"
    cacheinfo = "cache hit"
    try:
        original_url = cache.get(cache_key)
        if not original_url:
            try:
                url_obj = get_object_or_404(URL, short_code=code)
            except Exception as e:
                return HttpResponseNotFound("This URL is not registered with us, kindly check the spelling")
            original_url = url_obj.original_url

            cache.set(cache_key, original_url, timeout=3600)
            increment_clicks.delay(code)
            cacheinfo = "cache miss, going in db"
        else:
            increment_clicks.delay(code)
            # url_obj = URL.objects.filter(short_code=code).first()
            # if url_obj:
            #     url_obj.clicks += 1
            #     url_obj.save()
        logging.info(cacheinfo)
        return redirect(original_url)
    except Exception as e:
        # Log the error (not shown here for brevity)
        logging.error(f"Cache error: {e}")
        return HttpResponse("Some error occurred while processing your request." +
        "Sorry for the inconvenience.", status=500)