# Generated by Django 2.2.3 on 2019-07-17 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_remove_token_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='token',
            field=models.CharField(max_length=500, null=True),
        ),
    ]