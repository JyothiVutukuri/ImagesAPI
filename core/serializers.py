from rest_framework import serializers
from core.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("id", "title", "description", "url")
        read_only_fields = fields


class ImageUploadSerializer(serializers.Serializer):
    images_file_link = serializers.URLField()

