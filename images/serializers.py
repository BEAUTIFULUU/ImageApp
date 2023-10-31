import os
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import UserImage, ImageThumbnail
from .services.serializer_services import original_image_size


class ThumbnailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageThumbnail
        fields = ['image_thumb']

    def to_representation(self, instance):
        image_thumb = instance.image_thumb.url
        if image_thumb:
            base_url = os.environ.get('BASE_URL', '')
            image_thumb_url = f'{base_url}{image_thumb}'
            return {image_thumb_url}
        return super().to_representation(instance)


class ImageOutputSerializer(serializers.ModelSerializer):
    image_thumb = ThumbnailOutputSerializer(many=True, read_only=True, source='thumbnails')

    class Meta:
        model = UserImage
        fields = ['id', 'upload_date', 'image', 'image_thumb']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image = instance.image.url
        if image:
            base_url = os.environ.get('BASE_URL', '')
            image_url = f'{base_url}{image}'
            representation['image'] = image_url
        return representation


class BasicImageOutputSerializer(serializers.ModelSerializer):
    image_thumb = ThumbnailOutputSerializer(many=True, read_only=True, source='thumbnails')

    class Meta:
        model = UserImage
        fields = ['id', 'upload_date', 'image_thumb']


class ImageDetailInputSerializer(serializers.Serializer):
    image_link_time = serializers.IntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(30000)], required=True)


class ImageDetailOutputSerializer(serializers.ModelSerializer):
    original_image_size = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = [
            'id',
            'image',
            'original_image_size'
        ]

    def get_original_image_size(self, obj):
        return original_image_size(obj=obj)
