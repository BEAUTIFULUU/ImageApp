# Generated by Django 4.2.4 on 2023-11-02 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0013_customtier_alter_userprofile_custom_tier_delete_tier'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagethumbnail',
            name='custom_tier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='images.customtier'),
        ),
    ]