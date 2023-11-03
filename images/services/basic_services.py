import os
import uuid
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
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
    return UserImage.objects.filter(user=user).prefetch_related('thumbnails')


def create_image_obj(user, image: UserImage):
    user_profile = user.userprofile
    validate_image_format(image)
    new_image_name = f'{uuid.uuid4()}{os.path.splitext(image.name)[-1]}'
    image_obj = UserImage(user=user_profile, image=image)
    image_obj.image.name = new_image_name
    image_obj.save()
    if user_profile.account_tier in ['premium', 'enterprise']:
        resize_image.apply_async(args=(200, None, image_obj.pk))
        resize_image.apply_async(args=(400, None, image_obj.pk))
    elif user_profile.account_tier == 'basic':
        resize_image.apply_async(args=(200, None, image_obj.pk))
    else:
        custom_thumbnail_height = user_profile.custom_tier.thumbnail_height
        custom_thumbnail_width = user_profile.custom_tier.thumbnail_width
        resize_image.apply_async(args=(custom_thumbnail_height, custom_thumbnail_width, image_obj.pk))

    return image_obj
