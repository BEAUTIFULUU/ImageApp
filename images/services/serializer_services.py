from ..models import UserImage


def original_image_size(obj: UserImage) -> str:
    size_in_bytes = obj.image.size
    size_in_kb = round(size_in_bytes / 1024, 2)
    return f'{size_in_kb} KB'
