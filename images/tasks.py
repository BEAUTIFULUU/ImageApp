import uuid
from io import BytesIO
from PIL import Image
from celery import shared_task
from django.core.files.base import ContentFile, File
from images.models import ImageThumbnail, UserImage


@shared_task
def resize_image(height: int, width: int, image_id: int) -> None:
    user_image = UserImage.objects.get(pk=image_id)
    img = Image.open(user_image.image)
    img.convert('RGB')

    new_height = height
    if width is not None:
        new_width = width
    else:
        new_width = int((float(img.width) / img.height) * new_height)

    resized_img = img.resize((new_height, new_width))
    output = BytesIO()
    resized_img.save(output, format='JPEG')
    output.seek(0)

    thumbnail = ImageThumbnail.objects.create(user_image=user_image)
    thumbnail.image_thumb.save(
        f'thumbnail_{new_height}x{new_width}_{uuid.uuid4()}.jpg', File(ContentFile(output.read())), save=True)

    output.close()
