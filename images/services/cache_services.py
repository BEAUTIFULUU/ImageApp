from datetime import datetime
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404
from images.models import UserImage


def store_temporary_link_in_cache(image_id: int, temporary_link: str, expiration_time: datetime) -> None:
    cache_key = f'temporary_link_{image_id}'
    expiration_time_seconds = int(expiration_time.timestamp())
    cache.set(cache_key, temporary_link, expiration_time_seconds)


def get_temporary_link_from_cache(image_id: int) -> str:
    try:
        get_object_or_404(UserImage, pk=image_id)
    except Http404:
        cache_key = f'temporary_link_{image_id}'
        cache.delete(cache_key)
        return "Image not found."

    cache_key = f'temporary_link_{image_id}'
    return cache.get(cache_key)
