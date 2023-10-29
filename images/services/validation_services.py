import filetype
from rest_framework.exceptions import ValidationError


def validate_image_format(uploaded_image):
    kind = filetype.guess(uploaded_image.read())

    if kind is None:
        raise ValidationError('Invalid file format. Only JPEG and PNG images are allowed.')

    elif kind.extension not in ['jpg', 'png']:
        raise ValidationError('Invalid file format. Only JPEG and PNG images are allowed.')
