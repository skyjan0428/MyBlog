# Generated by Django 2.2.3 on 2019-07-26 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190726_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='user_id',
            new_name='user',
        ),
    ]
