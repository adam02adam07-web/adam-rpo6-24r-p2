from rest_framework import serializers
from .models import Ad

class AdSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    city_name = serializers.ReadOnlyField(source='city.name')

    class ImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = Ad
            fields = ('uuid', 'title', 'price', 'is_top', 'author_name', 'city_name')

    class Meta:
        model = Ad
        fields = [
            'uuid', 'title', 'price', 'description', 
            'category', 'city', 'author', 'is_top',
            'author_name', 'city_name', 'created_at'
        ]