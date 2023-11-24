from django.core.management.base import BaseCommand
from images.models import AccountTier
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Check and load built-in tiers'

    def handle(self, *args, **options):
        tiers_exist = AccountTier.objects.filter(name__in=['Basic', 'Premium', 'Enterprise']).exists()

        if not tiers_exist:
            self.stdout.write(self.style.SUCCESS('Built-in tiers do not exist. Loading data...'))
            call_command('loaddata', 'images/fixtures/initial_acc_tiers_data.json')
        else:
            self.stdout.write(self.style.SUCCESS('Built-in tiers already exist. No need to load data.'))
