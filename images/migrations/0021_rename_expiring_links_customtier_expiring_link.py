# Generated by Django 4.2.4 on 2023-11-03 15:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0020_remove_imagethumbnail_custom_tier"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customtier",
            old_name="expiring_links",
            new_name="expiring_link",
        ),
    ]
