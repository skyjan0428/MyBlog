# Generated by Django 2.2.3 on 2019-07-29 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20190727_1106'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='likepost',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='photo',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='post',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(default='新增個人簡介，讓大家更瞭解你。'),
        ),
    ]