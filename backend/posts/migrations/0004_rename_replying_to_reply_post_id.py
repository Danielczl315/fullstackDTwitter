# Generated by Django 4.1.3 on 2022-12-20 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_reply_like_post_likes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="reply", old_name="replying_to", new_name="post_id",
        ),
    ]
