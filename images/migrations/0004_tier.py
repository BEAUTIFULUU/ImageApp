# Generated by Django 4.2.4 on 2023-10-25 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_alter_userimage_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('thumbnail_sizes', models.JSONField()),
                ('original_image_link', models.BooleanField(default=True)),
                ('expiring_links', models.BooleanField(default=False)),
            ],
        ),
    ]
