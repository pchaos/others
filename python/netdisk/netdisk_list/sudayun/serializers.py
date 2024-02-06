from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'  # 或者指定字段列表 ['id', 'alias', 'uk', ...]


