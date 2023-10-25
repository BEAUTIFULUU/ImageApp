from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator


class UserProfile(models.Model):
    ACCOUNT_TIER_LEVEL_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    DEFAULT_ACCOUNT_TIER_LEVEL = 'basic'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_tier = models.CharField(
        max_length=10, choices=ACCOUNT_TIER_LEVEL_CHOICES, default=DEFAULT_ACCOUNT_TIER_LEVEL)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


class UserImage(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(
        upload_to='images/', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    upload_date = models.DateTimeField(auto_now_add=True)


class Tier(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.JSONField()
    original_image_link = models.BooleanField(default=True)
    expiring_links = models.BooleanField(default=False)
