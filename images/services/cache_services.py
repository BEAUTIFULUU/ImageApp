from django.core.cache import cache


def store_temporary_link_in_cache(image_id: int, temporary_link, expiration_time):
    cache_key = f'temporary_link_{image_id}'
    expiration_time_seconds = int(expiration_time.timestamp())
    cache.set(cache_key, temporary_link, expiration_time_seconds)


def get_temporary_link_from_cache(image_id: int):
    cache_key = f'temporary_link_{image_id}'
    return cache.get(cache_key)
