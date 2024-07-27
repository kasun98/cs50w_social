# Generated by Django 5.0.6 on 2024-07-08 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_alter_post_poster_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='like_count',
        ),
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.JSONField(default=list, null=True),
        ),
    ]
