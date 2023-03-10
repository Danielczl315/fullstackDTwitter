# Generated by Django 4.1.3 on 2022-12-12 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_nonce_alter_user_wallet_address_profile"),
    ]

    operations = [
        migrations.RemoveField(model_name="profile", name="profile_url",),
        migrations.AddField(
            model_name="profile",
            name="profile_pics",
            field=models.ImageField(default="default.jpg", upload_to="profile_pics"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.CharField(default="", max_length=160),
        ),
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.CharField(default="", max_length=50),
        ),
    ]
