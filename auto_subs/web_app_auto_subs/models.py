from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


class UserVideos(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='Пользователь')

    video = models.FileField(upload_to='videos',
                             verbose_name='Видео',
                             validators=[FileExtensionValidator(
                                 allowed_extensions=['mp4'])])

    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    videos_with_subs = models.FileField(
        # upload_to='videos_with_subs/%Y/%m/%d/',
        upload_to='videos_with_subs/',
        null=True, verbose_name='Видео с субтитрами',
        blank=True
    )

    name_of_video = models.CharField(max_length=50,
                                     verbose_name='Название видео', null=True, blank=True)
    
    make_audio_record = models.BooleanField(null=True, default=False, verbose_name='Нужно ли сделать аудио перевод',)
    
    rendering_progress = models.IntegerField(null=True, blank=True, verbose_name='Прогресс рендеринга')
    whisper_progress = models.IntegerField(null=True, blank=True, verbose_name='Прогресс транскрипции')
    
    def get_absolute_url(self):
        return reverse('watch_video', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Пользовательское видео'
        verbose_name_plural = 'Пользовательские видео'


class Title(models.Model):
    title = models.TextField(verbose_name='Текст')
    name = models.CharField(max_length=100, verbose_name='Название заголовка')

    class Meta:
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовоки'


class LanguagesForTranslateVideo(models.Model):
    language = models.CharField(max_length=50, unique=True, verbose_name='Язык в символах')
    name_of_language = models.CharField(max_length=50, unique=True, verbose_name='Язык', null=True)

    class Meta:
        verbose_name = 'Язык для перевода видео'
        verbose_name_plural = 'Языки для перевода видео'

    def __str__(self):
        return self.name_of_language


class ChangeEmailModel(models.Model):
    email2 = models.CharField(max_length=100, verbose_name='Новый email', null=True, blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь', unique=True)


    # def get_absolute_url(self):
    #     return reverse('', kwargs={'language': self.language})
