# Generated by Django 5.1 on 2024-10-08 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_auto_subs', '0006_uservideos_video_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservideos',
            name='video_size',
            field=models.FloatField(blank=True, null=True, verbose_name='Размер видео в мб'),
        ),
    ]