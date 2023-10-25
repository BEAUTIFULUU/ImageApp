from datetime import datetime, timedelta
import uuid

from rest_framework.request import Request

from images.models import UserImage
from images.services.cache_services import store_temporary_link_in_cache, get_temporary_link_from_cache


def generate_image_temporary_link(image_id: int, time, request: Request):
    existing_link = get_temporary_link_from_cache(image_id=image_id)
    if existing_link:
        return existing_link
    else:
        token = str(uuid.uuid4())
        user_image = UserImage.objects.get(id=image_id)
        image_url = request.build_absolute_uri(user_image.image.url)

        current_time = datetime.now()
        expiration_time = current_time + timedelta(seconds=int(time))
        expiration_time_str = expiration_time.strftime("%H:%M:%S")

        temporary_link = f'{image_url}?token={token}&expires={expiration_time_str}'

        store_temporary_link_in_cache(image_id, temporary_link, expiration_time)

        temporary_link_from_cache = get_temporary_link_from_cache(image_id)

        return temporary_link_from_cache
