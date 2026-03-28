from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponseNotFound, HttpResponse
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import URL
from .serializers import URLSerializer
from .utils import *
# from .tasks import increment_clicks
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def index(request):
    return render(request, "index.html")

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['original_url'],
        properties={
            'original_url': openapi.Schema(type=openapi.TYPE_STRING, format='uri')
        },
    ),
    responses={200: openapi.Response('Short URL created')}
)
@api_view(['POST'])
# @ratelimited
def create_short_url(request):
    serializer = URLSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        domain = request.get_host()
        scheme = request.scheme
        return Response({
            "short_code": obj.short_code,
            "short_url": f"{scheme}://{domain}/{obj.short_code}",
            "original_url": obj.original_url
        })
    return Response(serializer.errors, status=400)

def redirect_url(request, code):
    cache_key = f"url:{code}"
    cacheinfo = "cache hit"
    key = f"count:{code}"
    try:
        original_url = cache.get(cache_key)
        if not original_url:
            try:
                # url_obj = get_object_or_404(URL, short_code=code)
                url_obj = URL.objects.only("original_url").filter(short_code=code).first()
            except Exception as e:
                return HttpResponseNotFound("This URL is not registered with us, kindly check the spelling")
            original_url = url_obj.original_url

            cache.set(cache_key, original_url, timeout=3600)
            cacheinfo = "cache miss, going in db"
        logging.info(cacheinfo)
        try:
            cache.incr(key)
        except:
            cache.set(key, 1, timeout=600)
        return redirect(original_url)
    except Exception as e:
        # Log the error (not shown here for brevity)
        logging.error(f"Cache error: {e}")
        return HttpResponse("Some error occurred while processing your request." +
        "Sorry for the inconvenience.", status=500)
    
@api_view(['GET'])
def resolve_url(request, code):
    start = time.time()

    cache_key = f"url:{code}"
    original_url = cache.get(cache_key)

    source = "cache"

    if not original_url:
        url_obj = URL.objects.get(short_code=code)
        original_url = url_obj.original_url
        cache.set(cache_key, original_url, timeout=3600)
        source = "database"

    duration = time.time() - start

    return Response({
        "original_url": original_url,
        "source": source,
        "response_time_ms": round(duration * 1000, 2)
    })
def live(request):
    return HttpResponse("Alive", status=200)
