from rest_framework import serializers
from .models import URL

class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['id', 'original_url', 'short_code','clicks']
        read_only_fields = ['short_code']