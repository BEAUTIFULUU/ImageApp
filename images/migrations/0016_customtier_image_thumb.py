# Generated by Django 4.2.4 on 2023-11-02 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0015_remove_imagethumbnail_custom_tier'),
    ]

    operations = [
        migrations.AddField(
            model_name='customtier',
            name='image_thumb',
            field=models.ManyToManyField(to='images.imagethumbnail'),
        ),
    ]
