# Generated by Django 2.2.3 on 2019-08-09 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_notification_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
    ]
