from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import UserImage
from .services.serializer_services import original_image_size, thumbnail_200px_size, thumbnail_400px_size
from .tasks import resize_image_to_200px_height, resize_image_to_400px_height, thumbnail_400px_height, \
    thumbnail_200px_height


class ImageInputSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True)
    title = serializers.CharField(max_length=100, required=True)


class BasicImageOutputSerializer(serializers.ModelSerializer):
    thumbnail_200px_height = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ['id', 'upload_date', 'thumbnail_200px_height']

    def get_thumbnail_200px_height(self, obj):
        return thumbnail_200px_height(obj=obj, self=self)


class PremiumImageOutputSerializer(serializers.ModelSerializer):
    thumbnail_200px_height = serializers.SerializerMethodField()
    thumbnail_400px_height = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ['id', 'upload_date', 'image', 'thumbnail_200px_height', 'thumbnail_400px_height']

    def get_thumbnail_200px_height(self, obj):
        return thumbnail_200px_height(obj=obj, self=self)

    def get_thumbnail_400px_height(self, obj):
        return thumbnail_400px_height(obj=obj, self=self)


class EnterpriseImageOutputSerializer(serializers.ModelSerializer):
    thumbnail_200px_height = serializers.SerializerMethodField()
    thumbnail_400px_height = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ['id', 'upload_date', 'image', 'thumbnail_200px_height', 'thumbnail_400px_height']

    def get_thumbnail_200px_height(self, obj):
        return thumbnail_200px_height(obj=obj, self=self)

    def get_thumbnail_400px_height(self, obj):
        return thumbnail_400px_height(self, obj=obj, self=self)


class ImageDetailInputSerializer(serializers.Serializer):
    image_link_time = serializers.IntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(30000)], required=True)


class ImageDetailOutputSerializer(serializers.ModelSerializer):
    original_image_size = serializers.SerializerMethodField()
    thumbnail_200px_size = serializers.SerializerMethodField()
    thumbnail_400px_size = serializers.SerializerMethodField()

    def get_original_image_size(self, obj):
        return original_image_size(obj=obj)

    def get_thumbnail_200px_size(self, obj):
        return thumbnail_200px_size(obj=obj)

    def get_thumbnail_400px_size(self, obj):
        return thumbnail_400px_size(obj=obj)

    class Meta:
        model = UserImage
        fields = [
            'id',
            'image',
            'original_image_size',
            'thumbnail_200px_size',
            'thumbnail_400px_size',
        ]
