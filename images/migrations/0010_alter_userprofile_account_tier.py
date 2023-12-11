# Generated by Django 4.2.4 on 2023-10-31 16:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("images", "0009_remove_tier_built_in_alter_userprofile_account_tier"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="account_tier",
            field=models.CharField(
                blank=True,
                choices=[
                    ("basic", "Basic"),
                    ("premium", "Premium"),
                    ("enterprise", "Enterprise"),
                ],
                max_length=10,
                null=True,
            ),
        ),
    ]
