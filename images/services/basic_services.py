from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from images.services.validation_services import validate_image_format
from images.models import UserImage
from images.tasks import resize_image


def get_image_details(image_id: int, user: User) -> UserImage:
    image_obj = get_object_or_404(UserImage, id=image_id, user=user)
    return image_obj


def delete_image(image_id: int, user: User) -> None:
    image_obj = get_object_or_404(UserImage, id=image_id, user=user)
    image_obj.delete()


def get_user_images(user: User) -> QuerySet:
    return UserImage.objects.filter(user=user)


def create_image_obj(user, image):
    validate_image_format(image)
    image_obj = UserImage(user=user, image=image)
    if user.userprofile.account_tier == 'basic':
        resize_image.apply_async(args=(user, image_obj.image, 200))
    if user.userprofile.account_tier in ['premium', 'enterprise']:
        resize_image.apply_async(args=(user, image_obj.image, 200))
        resize_image.apply_async(args=(user, image_obj.image, 400))
    return image_obj

