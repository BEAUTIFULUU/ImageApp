from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import UserImage, ImageThumbnail
from .services.serializer_services import original_image_size


class ThumbnailOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageThumbnail
        fields = ['image_thumb']


class ImageOutputSerializer(serializers.ModelSerializer):
    image_thumb = ThumbnailOutputSerializer(many=True, read_only=True, source='thumbnails')

    class Meta:
        model = UserImage
        fields = ['id', 'upload_date', 'image', 'image_thumb']


class ImageDetailInputSerializer(serializers.Serializer):
    image_link_time = serializers.IntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(30000)], required=True)


class ImageDetailOutputSerializer(serializers.ModelSerializer):
    # original_image_size = serializers.SerializerMethodField()
    # thumbnail_200px_size = serializers.SerializerMethodField()
    # thumbnail_400px_size = serializers.SerializerMethodField()

    # def get_original_image_size(self, obj):
    #     return original_image_size(obj=obj)
    #
    # def get_thumbnail_200px_size(self, obj):
    #     return thumbnail_200px_size(obj=obj)
    #
    # def get_thumbnail_400px_size(self, obj):
    #     return thumbnail_400px_size(obj=obj)

    class Meta:
        model = UserImage
        fields = [
            'id',
            'image',
            # 'original_image_size',
            # 'thumbnail_200px_size',
            # 'thumbnail_400px_size',
        ]
