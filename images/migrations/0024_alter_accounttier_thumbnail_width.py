# Generated by Django 4.2.4 on 2023-11-04 17:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0023_accounttier_remove_userprofile_custom_tier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttier',
            name='thumbnail_width',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5000)]),
        ),
    ]
