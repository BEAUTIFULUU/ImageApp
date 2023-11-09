import magic
from rest_framework.exceptions import ValidationError
from ImageApp import settings
from images.models import UserImage


def validate_image_format(uploaded_image: UserImage):
    image_bytes = uploaded_image.read()
    mime_type = magic.Magic(mime=True)
    content_type = mime_type.from_buffer(image_bytes[:2048])

    if content_type not in settings.WHITELISTED_IMAGE_TYPES.values():
        raise ValidationError('Invalid image content-type')
