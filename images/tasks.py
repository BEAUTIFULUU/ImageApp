from io import BytesIO
from PIL import Image
from celery import shared_task
from images.models import ImageThumbnail


@shared_task
def resize_image(user, uploaded_image, height):

    image = Image.open(uploaded_image)

    new_height = height
    new_width = int((float(image.width) / image.height) * new_height)
    image.thumbnail((new_width, new_height))
    resized_image_200 = BytesIO()

    thumbnail_200_px = ImageThumbnail(user_image=uploaded_image, image=resized_image_200)
    thumbnail_200_px.save()

    if user.userprofile.account_tier in ['premium', 'enterprise']:
        image = Image.open(uploaded_image)

        new_height = height
        new_width = int((float(image.width) / image.height) * new_height)
        image.thumbnail((new_width, new_height))
        resized_image_400 = BytesIO()

        thumbnail_400_px = ImageThumbnail(user_image=uploaded_image, image=resized_image_400)
        thumbnail_400_px.save()

    image.close()
