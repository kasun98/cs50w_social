# Generated by Django 5.0.6 on 2024-07-07 06:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_post_poster_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('profile_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('followings', models.JSONField(default=list, null=True)),
            ],
        ),
    ]
