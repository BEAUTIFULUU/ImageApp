from unittest import mock
import pytest
import tempfile
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from unittest.mock import patch
from rest_framework.test import APIClient
from ..services.basic_services import (
    get_image_details,
    get_user_images,
    delete_image,
    create_image_obj,
)
from ..models import UserImage, UserProfile, AccountTier
<<<<<<< HEAD
from google.cloud import storage
=======
>>>>>>> ed8e77468c8925a27241943c28dbdddb893bd931

User = get_user_model()


@pytest.fixture
def mock_apply_async():
<<<<<<< HEAD
    with patch('images.services.basic_services.resize_image.apply_async') as mock:
=======
    with patch("images.services.basic_services.resize_image.apply_async") as mock:
>>>>>>> ed8e77468c8925a27241943c28dbdddb893bd931
        yield mock


@pytest.fixture
def create_basic_acc_tier():
    basic_acc_tier = AccountTier.objects.create(
        name="Basic",
        original_image_link=False,
        expiring_link=False,
        thumbnail_height=200,
        thumbnail_width=1,
    )
    return basic_acc_tier


@pytest.fixture
def create_premium_acc_tier():
    basic_acc_tier = AccountTier.objects.create(
        name="Premium",
        original_image_link=True,
        expiring_link=False,
        thumbnail_height=400,
        thumbnail_width=1,
    )
    return basic_acc_tier


@pytest.fixture
def create_enterprise_acc_tier():
    basic_acc_tier = AccountTier.objects.create(
        name="Enterprise",
        original_image_link=True,
        expiring_link=True,
        thumbnail_height=400,
        thumbnail_width=1,
    )
    return basic_acc_tier


@pytest.fixture
def create_custom_acc_tier():
    basic_acc_tier = AccountTier.objects.create(
        name="600x400",
        original_image_link=True,
        expiring_link=False,
        thumbnail_height=600,
        thumbnail_width=500,
    )
    return basic_acc_tier


@pytest.fixture
def create_authenticated_user_with_basic_tier(create_basic_acc_tier):
    """The built-in Django User model is automatically extended with a UserProfile through signals in models.py."""
    user = User.objects.create_user(username="123", password="123")
    client = APIClient()
    client.login(username="123", password="123")
    return user, client


@pytest.fixture
def create_user_image(create_authenticated_user_with_basic_tier):
    user, client = create_authenticated_user_with_basic_tier

    image_path = "images/tests/test_images/test_img.jpg"
    image = Image.open(image_path)

    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file.name)
    uploaded_file = SimpleUploadedFile(
        "test_image.jpg", tmp_file.read(), content_type="image/jpg"
    )
    user_image = UserImage.objects.create(user=user.userprofile, image=uploaded_file)
    return user_image


@pytest.fixture
def mock_create_image_bucket():
    mock_bucket = mock.Mock(spec=storage.Bucket)

    mock_bucket.name = 'test-bucket'
    mock_bucket.client.create_bucket.return_value = mock_bucket

    def mock_create_image_bucket_func():
        return mock_bucket

    return mock_create_image_bucket_func


@pytest.mark.django_db
class TestUserImageLogic:
    def test_get_image_details(self, create_user_image):
        user_image = create_user_image
        result_image = get_image_details(image_id=user_image.id, user=user_image.user)

        assert user_image == result_image
        assert UserImage.objects.count() == 1
        assert UserProfile.objects.count() == 1
        assert AccountTier.objects.count() == 1

    def test_get_image_details_invalid_data(self, create_user_image):
        user_image = create_user_image
        with pytest.raises(Http404):
            get_image_details(image_id=99999999, user=user_image.user)

    def test_get_user_images(self, create_user_image):
        user_image = create_user_image
        result_images = get_user_images(user=user_image.user)

        assert len(result_images) == 1
        assert user_image in result_images

    def test_delete_user_image(self, create_user_image):
        user_image = create_user_image
        delete_image(image_id=user_image.pk, user=user_image.user)

        assert not UserImage.objects.filter(pk=user_image.pk).exists()

<<<<<<< HEAD
    def test_create_image_obj_for_basic_tier_user(self, create_authenticated_user_with_basic_tier, mock_apply_async):
=======
    def test_create_image_obj_for_basic_tier_user(
        self, create_authenticated_user_with_basic_tier, mock_apply_async
    ):
>>>>>>> ed8e77468c8925a27241943c28dbdddb893bd931
        user, _ = create_authenticated_user_with_basic_tier

        image_path = "images/tests/test_images/test_img.jpg"
        image = Image.open(image_path)
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file.name)
<<<<<<< HEAD
        uploaded_file = SimpleUploadedFile("test_image.jpg", tmp_file.read(), content_type="image/jpg")

        image_obj = create_image_obj(user=user, image=uploaded_file)

        assert image_obj.pk is not None
        assert UserImage.objects.filter(user=user.userprofile).count() == 1
        mock_apply_async.assert_any_call(args=(user.userprofile.account_tier.thumbnail_height, None, image_obj.pk))

    def test_create_image_obj_for_premium_tier_user(
            self, create_authenticated_user_with_basic_tier, mock_apply_async, create_premium_acc_tier):
        user, _ = create_authenticated_user_with_basic_tier
        premium_tier = create_premium_acc_tier
        user.userprofile.account_tier = premium_tier

        image_path = 'images/tests/test_images/test_img.jpg'
        image = Image.open(image_path)
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file.name)
        uploaded_file = SimpleUploadedFile("test_image.jpg", tmp_file.read(), content_type="image/jpg")

        image_obj = create_image_obj(user=user, image=uploaded_file)

        assert image_obj.pk is not None
        assert UserImage.objects.filter(user=user.userprofile).count() == 1
        mock_apply_async.assert_any_call(args=(user.userprofile.account_tier.thumbnail_height, None, image_obj.pk))
        mock_apply_async.assert_any_call(args=(400, None, image_obj.pk))

    def test_create_image_obj_for_enterprise_tier_user(
            self, create_authenticated_user_with_basic_tier, mock_apply_async, create_enterprise_acc_tier):
        user, _ = create_authenticated_user_with_basic_tier
        enterprise_tier = create_enterprise_acc_tier
        user.userprofile.account_tier = enterprise_tier

        image_path = 'images/tests/test_images/test_img.jpg'
        image = Image.open(image_path)
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file.name)
        uploaded_file = SimpleUploadedFile("test_image.jpg", tmp_file.read(), content_type="image/jpg")

        image_obj = create_image_obj(user=user, image=uploaded_file)

        assert image_obj.pk is not None
        assert UserImage.objects.filter(user=user.userprofile).count() == 1
        mock_apply_async.assert_any_call(args=(user.userprofile.account_tier.thumbnail_height, None, image_obj.pk))
        mock_apply_async.assert_any_call(args=(400, None, image_obj.pk))

    def test_create_image_obj_for_custom_tier_user(
            self, create_authenticated_user_with_basic_tier, mock_apply_async, create_custom_acc_tier):
        user, _ = create_authenticated_user_with_basic_tier
        custom_tier = create_custom_acc_tier
        user.userprofile.account_tier = custom_tier

        image_path = 'images/tests/test_images/test_img.jpg'
        image = Image.open(image_path)
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file.name)
        uploaded_file = SimpleUploadedFile("test_image.jpg", tmp_file.read(), content_type="image/jpg")
=======
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg", tmp_file.read(), content_type="image/jpg"
        )
>>>>>>> ed8e77468c8925a27241943c28dbdddb893bd931

        image_obj = create_image_obj(user=user, image=uploaded_file)

        assert image_obj.pk is not None
        assert UserImage.objects.filter(user=user.userprofile).count() == 1
        mock_apply_async.assert_any_call(
            args=(user.userprofile.account_tier.thumbnail_height, None, image_obj.pk)
        )

    def test_create_image_obj_for_premium_tier_user(
        self,
        create_authenticated_user_with_basic_tier,
        create_premium_acc_tier,
        mock_apply_async,
    ):
        user, _ = create_authenticated_user_with_basic_tier
        premium_tier = create_premium_acc_tier
        user.userprofile.account_tier = premium_tier

        image_path = "images/tests/test_images/test_img.jpg"
        image = Image.open(image_path)
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file.name)
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg", tmp_file.read(), content_type="image/jpg"
        )

        image_obj = create_image_obj(user=user, image=uploaded_file)

        assert image_obj.pk is not None
        assert UserImage.objects.filter(user=user.userprofile).count() == 1
        mock_apply_async.assert_any_call(
            args=(user.userprofile.account_tier.thumbnail_height, None, image_obj.pk)
        )
        mock_apply_async.assert_any_call(args=(400, None, image_obj.pk))

    def test_create_image_obj_for_enterprise_tier_user(
        self,
        create_authenticated_user_with_basic_tier,
        mock_apply_async,
        create_enterprise_acc_tier,
    ):
        user, _ = create_authenticated_user_with_basic_tier
        enterprise_tier = create_enterprise_acc_tier
        user.userprofile.account_tier = enterprise_tier

        image_path = "images/tests/test_images/test_img.jpg"
        image = Image.open(image_path)
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file.name)
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg", tmp_file.read(), content_type="image/jpg"
        )

        image_obj = create_image_obj(user=user, image=uploaded_file)

        assert image_obj.pk is not None
        assert UserImage.objects.filter(user=user.userprofile).count() == 1
        mock_apply_async.assert_any_call(
            args=(user.userprofile.account_tier.thumbnail_height, None, image_obj.pk)
        )
        mock_apply_async.assert_any_call(args=(400, None, image_obj.pk))

    def test_create_image_obj_for_custom_tier_user(
        self,
        create_authenticated_user_with_basic_tier,
        mock_apply_async,
        create_custom_acc_tier,
    ):
        user, _ = create_authenticated_user_with_basic_tier
        custom_tier = create_custom_acc_tier
        user.userprofile.account_tier = custom_tier

        image_path = "images/tests/test_images/test_img.jpg"
        image = Image.open(image_path)
        tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(tmp_file.name)
        uploaded_file = SimpleUploadedFile(
            "test_image.jpg", tmp_file.read(), content_type="image/jpg"
        )

        image_obj = create_image_obj(user=user, image=uploaded_file)

        assert image_obj.pk is not None
        assert UserImage.objects.filter(user=user.userprofile).count() == 1
        mock_apply_async.assert_any_call(
            args=(
                user.userprofile.account_tier.thumbnail_height,
                user.userprofile.account_tier.thumbnail_width,
                image_obj.pk,
            )
        )
