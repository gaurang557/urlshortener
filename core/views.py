from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import URL
from .serializers import URLSerializer
from django.shortcuts import redirect, get_object_or_404

@api_view(['POST'])
def create_short_url(request):
    serializer = URLSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
        return Response({
            "short_url": f"http://localhost:8000/{obj.short_code}"
        })
    return Response(serializer.errors, status=400)


def redirect_url(request, code):
    url_obj = get_object_or_404(URL, short_code=code)
    url_obj.clicks += 1
    url_obj.save()
    return redirect(url_obj.original_url)