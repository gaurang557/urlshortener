from django.contrib import admin
from django.urls import path, re_path
from core.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="URL Shortener API",
      default_version='v1',
      description="API documentation for URL Shortener",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('live/', live),
    path('', index),
    path('api/shorten/', create_short_url),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0)),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0)),
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("edit/<int:pk>/", edit_url, name="edit_url"),
    path("delete/<int:pk>/", delete_url, name="delete_url"),
    path('<str:code>/', redirect_url),
    path('api/resolve/<str:code>/', resolve_url),
]
