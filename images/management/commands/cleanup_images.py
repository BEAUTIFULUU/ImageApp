from django.core.management.base import BaseCommand
from images.models import UserImage
import os


class Command(BaseCommand):
    help = 'Remove images from the database that no longer exist in the media folder'

    def handle(self, *args, **options):
        for image in UserImage.objects.all():
            if not os.path.exists(image.image.path):
                self.stdout.write(self.style.WARNING(f'Removing image with ID {image.id}'))
                image.delete()
