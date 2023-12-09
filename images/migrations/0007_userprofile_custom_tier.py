# Generated by Django 4.2.4 on 2023-10-31 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0006_rename_image_imagethumbnail_image_thumb"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="custom_tier",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="images.tier",
            ),
        ),
    ]
