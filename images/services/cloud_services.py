import os
import uuid
from urllib.parse import urljoin
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.deconstruct import deconstructible
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import clean_name, setting
from google.cloud import storage
from ImageApp import settings


@deconstructible
class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    bucket_name = setting(os.environ['GS_BUCKET_NAME'])

    def url(self, name):
        return urljoin(settings.MEDIA_URL, name)

    def get_available_name(self, name, max_length=None):
        return clean_name(name)


def generate_image_uuid() -> uuid:
    return str(uuid.uuid4())


def user_image_upload_path(instance, filename: str) -> str:
    image_uuid = generate_image_uuid()
    extension = filename.split('.')[-1]
    cloud_storage_path = f'user_images/{image_uuid}.{extension}'
    return cloud_storage_path


def thumbnail_upload_path(instance, filename: str) -> str:
    image_uuid = generate_image_uuid()
    extension = filename.split('.')[-1]
    cloud_storage_path = f'user_thumbnails/{image_uuid}.{extension}'
    return cloud_storage_path


def get_public_url_for_image(image_id: int, is_thumbnail: bool = False) -> str:
    directory = 'user_thumbnails' if is_thumbnail else 'images'
    storage_client = storage.Client()
    bucket = settings.GS_BUCKET_NAME
    bucket = storage_client.get_bucket(bucket)
    blob_name = f'{directory}/{image_id}.jpg'
    public_url = f'https://storage.googleapis.com/{bucket}/{blob_name}'

    blob = bucket.get_blob(blob_name)

    if blob:
        return public_url
    else:
        return "Image not found"
