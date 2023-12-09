from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
from .services.cloud_services import user_image_upload_path, thumbnail_upload_path


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_tier = models.ForeignKey(
        "AccountTier",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
    )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            user_profile = UserProfile.objects.create(user=instance)
            basic_tier = AccountTier.objects.get(name="Basic")
            user_profile.account_tier = basic_tier
            user_profile.save()

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


class UserImage(models.Model):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to=user_image_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])],
    )
    upload_date = models.DateTimeField(auto_now_add=True)


class ImageThumbnail(models.Model):
    user_image = models.ForeignKey(
        UserImage, on_delete=models.CASCADE, related_name="thumbnails"
    )
    image_thumb = models.ImageField(
        upload_to=thumbnail_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])],
    )


class AccountTier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    original_image_link = models.BooleanField(default=True)
    expiring_link = models.BooleanField(default=False)
    thumbnail_height = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5000)]
    )
    thumbnail_width = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5000)], default=1
    )

    def __str__(self):
        return self.name
