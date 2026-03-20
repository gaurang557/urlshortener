from django.contrib import admin
from django.urls import path
from core.views import create_short_url, redirect_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shorten/', create_short_url),
    path('<str:code>/', redirect_url),
]
