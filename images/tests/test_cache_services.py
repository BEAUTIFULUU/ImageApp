import tempfile
from datetime import datetime, timedelta
import pytest
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from images.models import AccountTier, UserImage
from images.services.cache_services import store_temporary_link_in_cache, get_temporary_link_from_cache

User = get_user_model()


@pytest.fixture
def create_basic_acc_tier():
    basic_acc_tier = AccountTier.objects.create(
        name='Basic',
        original_image_link=False,
        expiring_link=False,
        thumbnail_height=200,
        thumbnail_width=1
    )
    return basic_acc_tier


@pytest.fixture
def create_enterprise_acc_tier():
    basic_acc_tier = AccountTier.objects.create(
        name='Enterprise',
        original_image_link=True,
        expiring_link=True,
        thumbnail_height=400,
        thumbnail_width=1
    )
    return basic_acc_tier


@pytest.fixture
def create_authenticated_user_with_basic_tier(create_basic_acc_tier):
    """The built-in Django User model is automatically extended with a UserProfile through signals in models.py."""
    user = User.objects.create_user(username='123', password='123')
    client = APIClient()
    client.login(username='123', password='123')
    return user, client


@pytest.fixture
def create_user_image(create_authenticated_user_with_basic_tier, create_enterprise_acc_tier):
    user, client = create_authenticated_user_with_basic_tier
    enterprise_tier = create_enterprise_acc_tier
    user.userprofile.account_tier = enterprise_tier

    image_path = 'images/tests/test_images/test_img.jpg'
    image = Image.open(image_path)

    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file.name)
    uploaded_file = SimpleUploadedFile("test_image.jpg", tmp_file.read(), content_type="image/jpg")
    user_image = UserImage.objects.create(user=user.userprofile, image=uploaded_file)
    return user_image


@pytest.mark.django_db
def test_store_and_retrieve_temporary_link(create_user_image):
    user_image = create_user_image

    temporary_link = "https://example.com/temporary-link"
    expiration_time = datetime.now() + timedelta(hours=1)

    store_temporary_link_in_cache(user_image.pk, temporary_link, expiration_time)

    retrieved_link = get_temporary_link_from_cache(user_image.pk)

    assert retrieved_link == temporary_link


@pytest.mark.django_db
def test_get_temporary_link_not_found():
    non_existent_image_id = 999999
    retrieved_link = get_temporary_link_from_cache(non_existent_image_id)

    assert retrieved_link == "Image not found."

    cache_key = f'temporary_link_{non_existent_image_id}'
    assert cache.get(cache_key) is None
