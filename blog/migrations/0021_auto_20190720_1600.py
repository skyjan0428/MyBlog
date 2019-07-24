# Generated by Django 2.2.3 on 2019-07-20 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_post_attach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='attach',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='attach_to_post', to='blog.Post'),
        ),
    ]