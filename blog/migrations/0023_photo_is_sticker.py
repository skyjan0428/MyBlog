# Generated by Django 2.2.3 on 2019-07-24 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_photo_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='is_sticker',
            field=models.BooleanField(default=False),
        ),
    ]
