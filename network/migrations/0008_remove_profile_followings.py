# Generated by Django 5.0.6 on 2024-07-07 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_remove_profile_net_followers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followings',
        ),
    ]
