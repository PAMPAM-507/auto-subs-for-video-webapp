# Generated by Django 5.1 on 2024-09-02 06:43

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguagesForTranslateVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50, unique=True, verbose_name='Язык в символах')),
                ('name_of_language', models.CharField(max_length=50, null=True, unique=True, verbose_name='Язык')),
            ],
            options={
                'verbose_name': 'Язык для перевода видео',
                'verbose_name_plural': 'Языки для перевода видео',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Текст')),
                ('name', models.CharField(max_length=100, verbose_name='Название заголовка')),
            ],
            options={
                'verbose_name': 'Заголовок',
                'verbose_name_plural': 'Заголовоки',
            },
        ),
        migrations.CreateModel(
            name='ChangeEmailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Новый email')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='UserVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to='videos', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])], verbose_name='Видео')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('videos_with_subs', models.FileField(blank=True, null=True, upload_to='videos_with_subs/', verbose_name='Видео с субтитрами')),
                ('name_of_video', models.CharField(blank=True, max_length=50, null=True, verbose_name='Название видео')),
                ('make_audio_record', models.BooleanField(default=False, null=True, verbose_name='Нужно ли сделать аудио перевод')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Пользовательское видео',
                'verbose_name_plural': 'Пользовательские видео',
            },
        ),
    ]
