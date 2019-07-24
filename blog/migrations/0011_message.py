# Generated by Django 2.2.3 on 2019-07-18 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_token_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Datetime')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reciever', to='blog.User')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender', to='blog.User')),
            ],
        ),
    ]