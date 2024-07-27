# Generated by Django 5.0.6 on 2024-07-06 18:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_post_poster_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='poster_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
