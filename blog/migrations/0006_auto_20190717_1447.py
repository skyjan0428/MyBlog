# Generated by Django 2.2.3 on 2019-07-17 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='token',
        ),
        migrations.AddField(
            model_name='token',
            name='token',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
