import pytest
import tempfile
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ..models import UserImage, AccountTier
from ..services.cache_services import get_temporary_link_from_cache


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
def create_custom_acc_tier_without_exp_link():
    custom_acc_tier = AccountTier.objects.create(
        name='600x400',
        original_image_link=True,
        expiring_link=False,
        thumbnail_height=600,
        thumbnail_width=500
    )
    return custom_acc_tier


@pytest.fixture
def create_custom_acc_tier_with_exp_link():
    custom_acc_tier = AccountTier.objects.create(
        name='600x400',
        original_image_link=True,
        expiring_link=True,
        thumbnail_height=600,
        thumbnail_width=500
    )
    return custom_acc_tier


@pytest.fixture
def create_admin_user_with_basic_tier(create_basic_acc_tier):
    admin_user = User.objects.create_superuser(
        username='321', password='321', email='321@gmail.com')
    client = APIClient()
    client.login(username='321', password='321', email='321@gmail.com')
    return admin_user, client


@pytest.fixture
def create_user_image_for_admin_user(create_admin_user_with_basic_tier):
    user, client = create_admin_user_with_basic_tier

    image_path = 'images/tests/test_images/test_img.jpg'
    image = Image.open(image_path)

    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file.name)
    uploaded_file = SimpleUploadedFile('test_img.jpg', tmp_file.read(), content_type='image/jpg')
    user_image = UserImage.objects.create(user=user.userprofile, image=uploaded_file)
    return user_image


@pytest.fixture
def create_authenticated_user_with_basic_tier(create_basic_acc_tier):
    """The built-in Django User model is automatically extended with a UserProfile through signals in models.py."""
    user = User.objects.create_user(username='123', password='123')
    client = APIClient()
    client.login(username='123', password='123')
    return user, client


@pytest.fixture
def create_user_image_for_authenticated_user(create_authenticated_user_with_basic_tier):
    user, client = create_authenticated_user_with_basic_tier

    image_path = 'images/tests/test_images/test_img.jpg'
    image = Image.open(image_path)

    tmp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(tmp_file.name)
    uploaded_file = SimpleUploadedFile('test_img.jpg', tmp_file.read(), content_type='image/jpg')
    user_image = UserImage.objects.create(user=user.userprofile, image=uploaded_file)
    return user_image


@pytest.mark.django_db
class TestImagesViewPermissions:
    def test_images_view_return_403_for_anonymous_user(self):
        client = APIClient()
        url = 'list_upload_images'
        response = client.get(reverse(url))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_post_image_return_403(self):
        client = APIClient()
        url = 'list_upload_images'

        image_path = 'images/tests/test_images/test_img.jpg'
        with open(image_path, 'rb') as file:
            image_data = file.read()
            image_file = SimpleUploadedFile('test_img.jpg', image_data, content_type='image/jpeg')

        data = {
            'image': image_file,
        }

        response = client.post(reverse(url), data=data, format='multipart')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert UserImage.objects.count() == 0

    def test_images_view_return_images_and_200_for_authenticated_user(self, create_authenticated_user_with_basic_tier):
        user, client = create_authenticated_user_with_basic_tier
        url = 'list_upload_images'
        response = client.get(reverse(url))
        assert response.status_code == status.HTTP_200_OK

    def test_if_authenticated_user_post_image_return_201(self, create_authenticated_user_with_basic_tier):
        user, client = create_authenticated_user_with_basic_tier
        url = 'list_upload_images'

        image_path = 'images/tests/test_images/test_img.jpg'
        with open(image_path, 'rb') as file:
            image_data = file.read()
            image_file = SimpleUploadedFile('test_img.jpg', image_data, content_type='image/jpeg')

        data = {
            'image': image_file,
        }

        assert UserImage.objects.filter(user=user.pk).count() == 0
        response = client.post(reverse(url), data=data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert UserImage.objects.filter(user=user.pk).count() == 1

    def test_images_view_return_images_for_admin_user(self, create_admin_user_with_basic_tier):
        user, client = create_admin_user_with_basic_tier
        url = 'list_upload_images'
        response = client.get(reverse(url))
        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_user_post_image_return_201(self, create_admin_user_with_basic_tier):
        user, client = create_admin_user_with_basic_tier
        url = 'list_upload_images'

        image_path = 'images/tests/test_images/test_img.jpg'
        with open(image_path, 'rb') as file:
            image_data = file.read()
            image_file = SimpleUploadedFile('test_img.jpg', image_data, content_type='image/jpeg')

        data = {
            'image': image_file,
        }

        assert UserImage.objects.filter(user=user.pk).count() == 0
        response = client.post(reverse(url), data=data, format='multipart')
        assert response.status_code == status.HTTP_201_CREATED
        assert UserImage.objects.filter(user=user.pk).count() == 1


@pytest.mark.django_db
class TestImageDetailsViewPermissions:
    def test_image_detail_view_return_403_for_anonymous_user(self, create_user_image_for_authenticated_user):
        image_obj = create_user_image_for_authenticated_user
        client = APIClient()
        url = 'image_details'

        response = client.get(reverse(url, kwargs={'image_id': image_obj.pk}))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_anonymous_user_delete_image_return_403(self, create_user_image_for_authenticated_user):
        image_obj = create_user_image_for_authenticated_user
        client = APIClient()
        url = 'image_details'

        assert UserImage.objects.get(id=image_obj.pk) is not None
        response = client.delete(reverse(url, kwargs={'image_id': image_obj.pk}))
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert UserImage.objects.get(id=image_obj.pk) is not None

    def test_image_details_view_return_image_details_and_200_for_authenticated_user(
            self, create_user_image_for_authenticated_user, create_authenticated_user_with_basic_tier):
        user, client = create_authenticated_user_with_basic_tier
        image_obj = create_user_image_for_authenticated_user
        url = 'image_details'

        response = client.get(reverse(url, kwargs={'image_id': image_obj.pk}))
        assert response.status_code == status.HTTP_200_OK

    def test_if_authenticated_user_delete_image_return_204(
            self, create_user_image_for_authenticated_user, create_authenticated_user_with_basic_tier):
        user, client = create_authenticated_user_with_basic_tier
        image_obj = create_user_image_for_authenticated_user
        url = 'image_details'

        response = client.delete(reverse(url, kwargs={'image_id': image_obj.pk}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert UserImage.objects.filter(user=user.pk).count() == 0

    def test_image_details_view_return_image_details_and_200_for_admin_user(
            self, create_user_image_for_admin_user, create_admin_user_with_basic_tier):
        user, client = create_admin_user_with_basic_tier
        image_obj = create_user_image_for_admin_user
        url = 'image_details'

        response = client.get(reverse(url, kwargs={'image_id': image_obj.pk}))
        assert response.status_code == status.HTTP_200_OK

    def test_if_admin_user_delete_image_return_204(
            self, create_user_image_for_admin_user, create_admin_user_with_basic_tier):
        user, client = create_admin_user_with_basic_tier
        image_obj = create_user_image_for_admin_user
        url = 'image_details'

        response = client.delete(reverse(url, kwargs={'image_id': image_obj.pk}))
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert UserImage.objects.filter(user=user.pk).count() == 0


@pytest.mark.django_db
class TestImageDetailsViewExpiringLinkPermissions:
    def test_if_anonymous_user_post_expiring_link_time_return_403(self, create_user_image_for_authenticated_user):
        image_obj = create_user_image_for_authenticated_user
        client = APIClient()
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is None

    def test_if_authenticated_user_with_basic_acc_tier_post_image_link_time_return_403(
            self, create_authenticated_user_with_basic_tier, create_user_image_for_authenticated_user,
            create_basic_acc_tier):
        image_obj = create_user_image_for_authenticated_user
        user, client = create_authenticated_user_with_basic_tier
        basic_tier = create_basic_acc_tier
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == basic_tier
        assert response.status_code == status.HTTP_403_FORBIDDEN
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is None

    def test_if_authenticated_user_with_premium_acc_tier_post_image_link_time_return_403(
            self, create_authenticated_user_with_basic_tier, create_user_image_for_authenticated_user,
            create_premium_acc_tier):
        image_obj = create_user_image_for_authenticated_user
        user, client = create_authenticated_user_with_basic_tier
        premium_tier = create_premium_acc_tier
        user.userprofile.account_tier = premium_tier
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == premium_tier
        assert response.status_code == status.HTTP_403_FORBIDDEN
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is None

    def test_if_authenticated_user_with_enterprise_acc_tier_post_image_link_time_return_201(
            self, create_authenticated_user_with_basic_tier, create_user_image_for_authenticated_user,
            create_enterprise_acc_tier):
        image_obj = create_user_image_for_authenticated_user
        user, client = create_authenticated_user_with_basic_tier
        enterprise_tier = create_enterprise_acc_tier
        user.userprofile.account_tier = enterprise_tier
        client.force_authenticate(user)
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == enterprise_tier
        assert response.status_code == status.HTTP_201_CREATED
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is not None

    def test_if_authenticated_user_with_custom_tier_with_no_exp_link_post_image_link_time_return_403(
            self, create_authenticated_user_with_basic_tier, create_custom_acc_tier_without_exp_link,
            create_user_image_for_authenticated_user):
        image_obj = create_user_image_for_authenticated_user
        user, client = create_authenticated_user_with_basic_tier
        custom_tier = create_custom_acc_tier_without_exp_link
        user.userprofile.account_tier = custom_tier
        client.force_authenticate(user=user)
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == custom_tier
        assert response.status_code == status.HTTP_403_FORBIDDEN
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is None

    def test_if_authenticated_user_with_custom_tier_with_exp_link_post_image_link_time_return_403(
            self, create_authenticated_user_with_basic_tier, create_custom_acc_tier_with_exp_link,
            create_user_image_for_authenticated_user):
        image_obj = create_user_image_for_authenticated_user
        user, client = create_authenticated_user_with_basic_tier
        custom_tier = create_custom_acc_tier_with_exp_link
        user.userprofile.account_tier = custom_tier
        client.force_authenticate(user=user)
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == custom_tier
        assert response.status_code == status.HTTP_201_CREATED
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is not None

    def test_if_admin_user_with_basic_acc_tier_post_image_link_time_return_403(
            self, create_admin_user_with_basic_tier, create_user_image_for_admin_user, create_basic_acc_tier):
        image_obj = create_user_image_for_admin_user
        user, client = create_admin_user_with_basic_tier
        basic_tier = create_basic_acc_tier
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == basic_tier
        assert response.status_code == status.HTTP_403_FORBIDDEN
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is None

    def test_if_admin_user_with_premium_acc_tier_post_image_link_time_return_403(
            self, create_admin_user_with_basic_tier, create_user_image_for_admin_user, create_premium_acc_tier):
        image_obj = create_user_image_for_admin_user
        user, client = create_admin_user_with_basic_tier
        premium_tier = create_premium_acc_tier
        user.userprofile.account_tier = premium_tier
        client.force_authenticate(user=user)
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == premium_tier
        assert response.status_code == status.HTTP_403_FORBIDDEN
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is None

    def test_if_admin_user_with_enterprise_acc_tier_post_image_link_time_return_201(
            self, create_admin_user_with_basic_tier, create_user_image_for_admin_user, create_enterprise_acc_tier):
        image_obj = create_user_image_for_admin_user
        user, client = create_admin_user_with_basic_tier
        enterprise_tier = create_enterprise_acc_tier
        user.userprofile.account_tier = enterprise_tier
        client.force_authenticate(user=user)
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == enterprise_tier
        assert response.status_code == status.HTTP_201_CREATED
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is not None

    def test_if_admin_user_with_custom_tier_with_no_exp_link_post_image_link_time_return_403(
            self, create_admin_user_with_basic_tier, create_custom_acc_tier_without_exp_link,
            create_user_image_for_admin_user):
        image_obj = create_user_image_for_admin_user
        user, client = create_admin_user_with_basic_tier
        custom_tier = create_custom_acc_tier_without_exp_link
        user.userprofile.account_tier = custom_tier
        client.force_authenticate(user=user)
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == custom_tier
        assert response.status_code == status.HTTP_403_FORBIDDEN
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is None

    def test_if_admin_user_with_custom_tier_with_exp_link_post_image_link_time_return_201(
            self, create_admin_user_with_basic_tier, create_custom_acc_tier_with_exp_link,
            create_user_image_for_admin_user):
        image_obj = create_user_image_for_admin_user
        user, client = create_admin_user_with_basic_tier
        custom_tier = create_custom_acc_tier_with_exp_link
        user.userprofile.account_tier = custom_tier
        client.force_authenticate(user=user)
        url = 'image_details'
        data = {
            'image_link_time': 300
        }

        response = client.post(reverse(url, kwargs={'image_id': image_obj.pk}), data=data, format='json')
        assert user.userprofile.account_tier == custom_tier
        assert response.status_code == status.HTTP_201_CREATED
        temporary_link = get_temporary_link_from_cache(image_id=image_obj.pk)
        assert temporary_link is not None
