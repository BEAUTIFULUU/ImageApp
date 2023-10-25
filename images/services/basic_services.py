from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from images.models import UserImage
from images.serializers import BasicImageOutputSerializer, PremiumImageOutputSerializer, EnterpriseImageOutputSerializer


def get_image_details(image_id: int, user: User) -> UserImage:
    image_obj = get_object_or_404(UserImage, id=image_id, user=user)
    return image_obj


def delete_image(image_id: int, user: User) -> None:
    image_obj = get_object_or_404(UserImage, id=image_id, user=user)
    image_obj.delete()


def get_user_images(user: User) -> QuerySet:
    return UserImage.objects.filter(user=user)


def create_image_obj(request: Request, serializer: Serializer) -> UserImage:
    user = request.user.userprofile
    image_obj = UserImage(user=user, image=serializer.validated_data['image'])
    image_obj.save()
    return image_obj


def get_user_images_based_on_account_level(
        user: User, images: QuerySet[UserImage], request: Request) -> list[UserImage] | None:
    error_message = 'Error while displaying images.'
    account_tier = user.userprofile.account_tier

    if account_tier == 'basic':
        serializer = BasicImageOutputSerializer(images, many=True, context={'request': request})
        return serializer.data
    elif account_tier == 'premium':
        serializer = PremiumImageOutputSerializer(images, many=True, context={'request': request})
        return serializer.data
    elif account_tier == 'enterprise':
        serializer = EnterpriseImageOutputSerializer(images, many=True, context={'request': request})
        return serializer.data

    else:
        raise serializers.ValidationError(error_message)


def create_user_images_based_on_account_level(user: User, image_obj: UserImage, request: Request):
    error_message = 'Error while displaying images.'
    account_tier = user.userprofile.account_tier

    if account_tier == 'basic':
        serializer = BasicImageOutputSerializer(image_obj, context={'request': request})
        return serializer.data
    elif account_tier == 'premium':
        serializer = PremiumImageOutputSerializer(image_obj, context={'request': request})
        return serializer.data
    elif account_tier == 'enterprise':
        serializer = EnterpriseImageOutputSerializer(image_obj, context={'request': request})
        return serializer.data
    else:
        raise serializers.ValidationError(error_message)






