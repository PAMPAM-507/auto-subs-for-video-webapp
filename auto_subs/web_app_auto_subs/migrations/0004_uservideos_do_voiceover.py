# Generated by Django 5.1 on 2024-09-10 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_auto_subs', '0003_uservideos_translate_progress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservideos',
            name='do_voiceover',
            field=models.BooleanField(blank=True, null=True, verbose_name='Делать озвучку'),
        ),
    ]