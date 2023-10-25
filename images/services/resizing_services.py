import os
from PIL import Image
from ImageApp import settings
from images.models import UserImage


def resize_image_to_200px_height(original_image: UserImage):
    destination_folder = os.path.join(settings.MEDIA_ROOT, 'images')
    image = Image.open(original_image)

    width, height = image.size
    new_height = 200
    new_width = int((new_height / height) * width)

    resized_image = image.resize((new_width, new_height))

    original_filename = os.path.basename(original_image.name)
    resized_image_name = f'200px_{original_filename}'
    resized_image_path = os.path.join(destination_folder, resized_image_name)

    resized_image.save(resized_image_path)
    image.close()
    return resized_image_path


def resize_image_to_400px_height(original_image: UserImage):
    destination_folder = os.path.join(settings.MEDIA_ROOT, 'images')
    image = Image.open(original_image)

    width, height = image.size
    new_height = 400
    new_width = int((new_height / height) * width)

    resized_image = image.resize((new_width, new_height))

    original_filename = os.path.basename(original_image.name)
    resized_image_name = f'400px_{original_filename}'
    resized_image_path = os.path.join(destination_folder, resized_image_name)

    resized_image.save(resized_image_path)
    image.close()
    return resized_image_path