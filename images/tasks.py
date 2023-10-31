import uuid
from io import BytesIO
from PIL import Image
from celery import shared_task
from django.core.files.base import ContentFile
from images.models import ImageThumbnail, UserImage


@shared_task
def resize_image(height: int, image_id: int) -> None:
    user_image = UserImage.objects.get(pk=image_id)
    img = Image.open(user_image.image)
    img.convert('RGB')

    new_height = height
    new_width = int((float(img.width) / img.height) * new_height)
    img.thumbnail((new_width, new_height))

    output = BytesIO()
    img.save(output, format='JPEG')
    output.seek(0)

    thumbnail = ImageThumbnail(user_image=user_image)
    thumbnail.image_thumb.save(f'thumbnail_{height}_{uuid.uuid4()}.jpg', ContentFile(output.getvalue()), save=True)

    thumbnail.save()
    output.close()
