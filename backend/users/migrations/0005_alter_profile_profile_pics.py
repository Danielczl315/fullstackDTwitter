# Generated by Django 4.1.3 on 2022-12-12 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_remove_profile_profile_url_profile_profile_pics_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_pics",
            field=models.ImageField(default="default.png", upload_to="profile_pics"),
        ),
    ]