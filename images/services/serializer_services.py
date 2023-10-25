import os
from .resizing_services import resize_image_to_200px_height, resize_image_to_400px_height
from ..models import UserImage


def original_image_size(obj: UserImage):
    size_in_bytes = obj.image.size
    size_in_kb = round(size_in_bytes / 1024, 2)
    return f'{size_in_kb} KB'


def thumbnail_200px_size(obj: UserImage):
    thumbnail_200px_path = resize_image_to_200px_height(obj.image)
    thumbnail_200px_size_in_bytes = os.path.getsize(thumbnail_200px_path)
    thumbnail_200px_size_in_kb = round(thumbnail_200px_size_in_bytes / 1024, 2)
    return f'{thumbnail_200px_size_in_kb} KB'


def thumbnail_400px_size(obj: UserImage):
    thumbnail_400px_path = resize_image_to_400px_height(obj.image)
    thumbnail_400px_size_in_bytes = os.path.getsize(thumbnail_400px_path)
    thumbnail_400px_size_in_kb = round(thumbnail_400px_size_in_bytes / 1024, 2)
    return f'{thumbnail_400px_size_in_kb} KB'
