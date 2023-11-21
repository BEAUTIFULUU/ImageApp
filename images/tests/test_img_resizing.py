import os
import tempfile
import pytest
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from images.models import ImageThumbnail, AccountTier, UserImage
from images.tasks import resize_image

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
def create_premium_acc_tier():
    premium_acc_tier = AccountTier.objects.create(
        name='Premium',
        original_image_link=True,
        expiring_link=False,
        thumbnail_height=400,
        thumbnail_width=1
    )
    return premium_acc_tier


@pytest.fixture
def create_enterprise_acc_tier():
    enterprise_acc_tier = AccountTier.objects.create(
        name='Enterprise',
        original_image_link=True,
        expiring_link=True,
        thumbnail_height=400,
        thumbnail_width=1
    )
    return enterprise_acc_tier


@pytest.fixture
def create_custom_acc_tier():
    custom_acc_tier = AccountTier.objects.create(
        name='600x400',
        original_image_link=True,
        expiring_link=False,
        thumbnail_height=600,
        thumbnail_width=500
    )
    return custom_acc_tier


@pytest.fixture
def create_authenticated_user_with_basic_tier(create_basic_acc_tier):
    """The built-in Django User model is automatically extended with a UserProfile through signals in models.py."""
    user = User.objects.create_user(username='123', password='123')
    client = APIClient()
    client.login(username='123', password='123')
    return user, client


@pytest.fixture
def create_user_image(create_authenticated_user_with_basic_tier):
    user, client = create_authenticated_user_with_basic_tier

    image_path = 'images/tests/test_images/test_img.jpg'
    image = Image.open(image_path)

    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file.name)
    uploaded_file = SimpleUploadedFile("test_image.jpg", tmp_file.read(), content_type="image/jpg")
    user_image = UserImage.objects.create(user=user.userprofile, image=uploaded_file)
    return user_image


@pytest.mark.django_db
class TestResizing:
    def test_resize_image_for_basic_tier(self, create_user_image, create_authenticated_user_with_basic_tier):
        user, _ = create_authenticated_user_with_basic_tier
        user_image = create_user_image
        acc_tier_thb_height = user.userprofile.account_tier.thumbnail_height
        acc_tier_thb_width = user.userprofile.account_tier.thumbnail_width

        resize_image(
            height=acc_tier_thb_height, width=acc_tier_thb_width, image_id=user_image.pk)

        thumbnail = ImageThumbnail.objects.get(user_image=user_image)

        assert thumbnail.image_thumb is not None
        assert thumbnail.image_thumb.width == acc_tier_thb_height
        assert thumbnail.image_thumb.height == acc_tier_thb_width

    def test_resize_image_for_premium_tier(
            self, create_user_image, create_authenticated_user_with_basic_tier, create_premium_acc_tier):
        user, _ = create_authenticated_user_with_basic_tier
        user.userprofile.account_tier = create_premium_acc_tier
        user_image = create_user_image
        acc_tier_thb_height = user.userprofile.account_tier.thumbnail_height
        acc_tier_thb_width = user.userprofile.account_tier.thumbnail_width

        resize_image(
            height=acc_tier_thb_height, width=acc_tier_thb_width, image_id=user_image.pk)

        thumbnail = ImageThumbnail.objects.get(user_image=user_image)

        assert thumbnail.image_thumb is not None
        assert thumbnail.image_thumb.width == acc_tier_thb_height
        assert thumbnail.image_thumb.height == acc_tier_thb_width

    def test_resize_image_for_enterprise_tier(
            self, create_user_image, create_authenticated_user_with_basic_tier, create_enterprise_acc_tier):
        user, _ = create_authenticated_user_with_basic_tier
        user.userprofile.account_tier = create_enterprise_acc_tier
        user_image = create_user_image
        acc_tier_thb_height = user.userprofile.account_tier.thumbnail_height
        acc_tier_thb_width = user.userprofile.account_tier.thumbnail_width

        resize_image(
            height=acc_tier_thb_height, width=acc_tier_thb_width, image_id=user_image.pk)

        thumbnail = ImageThumbnail.objects.get(user_image=user_image)

        assert thumbnail.image_thumb is not None
        assert thumbnail.image_thumb.width == acc_tier_thb_height
        assert thumbnail.image_thumb.height == acc_tier_thb_width

    def test_resize_image_for_custom_tier(
            self, create_user_image, create_authenticated_user_with_basic_tier, create_custom_acc_tier):
        user, _ = create_authenticated_user_with_basic_tier
        user.userprofile.account_tier = create_custom_acc_tier
        user_image = create_user_image
        acc_tier_thb_height = user.userprofile.account_tier.thumbnail_height
        acc_tier_thb_width = user.userprofile.account_tier.thumbnail_width

        resize_image(
            height=acc_tier_thb_height, width=acc_tier_thb_width, image_id=user_image.pk)

        thumbnail = ImageThumbnail.objects.get(user_image=user_image)

        assert thumbnail.image_thumb is not None
        assert thumbnail.image_thumb.width == acc_tier_thb_height
        assert thumbnail.image_thumb.height == acc_tier_thb_width
