# Generated by Django 4.2.4 on 2023-11-04 12:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0021_rename_expiring_links_customtier_expiring_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customtier",
            name="thumbnail_height",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5000),
                ]
            ),
        ),
    ]
