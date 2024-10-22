from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


class UserVideos(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name='User')

    video = models.FileField(upload_to='videos',
                             verbose_name='Video',
                             validators=[FileExtensionValidator(
                                 allowed_extensions=['mp4'])])

    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Upload date')

    videos_with_subs = models.FileField(
        # upload_to='videos_with_subs/%Y/%m/%d/',
        upload_to='video_with_subs/',
        null=True, verbose_name='Video with subtitles',
        blank=True
    )

    name_of_video = models.CharField(max_length=50,
                                     verbose_name='Video title', null=True, blank=True)
    
    video_size = models.FloatField(null=True, blank=True, verbose_name='Video size in MB')
    
    make_audio_record = models.BooleanField(null=True, default=False, verbose_name='Is audio translation needed?')
    
    rendering_progress = models.IntegerField(null=True, blank=True, verbose_name='Rendering progress')
    whisper_progress = models.IntegerField(null=True, blank=True, verbose_name='Transcription progress')
    translate_progress = models.IntegerField(null=True, blank=True, verbose_name='Translation progress')
    voiceover_progress = models.IntegerField(null=True, blank=True, verbose_name='Voiceover progress')
    
    def get_absolute_url(self):
        return reverse('watch_video', kwargs={'pk': self.pk})
    
    def __str__(self):
        return 'User video, Id: ' + str(self.pk) + ', Title: ' + str(self.name_of_video)

    class Meta:
        verbose_name = 'User video'
        verbose_name_plural = 'User videos'


class Title(models.Model):
    title = models.TextField(verbose_name='Text')
    name = models.CharField(max_length=100, verbose_name='Title name')

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'


class LanguagesForTranslateVideo(models.Model):
    language = models.CharField(max_length=50, unique=True, verbose_name='Language code')
    name_of_language = models.CharField(max_length=50, unique=True, verbose_name='Language', null=True)

    class Meta:
        verbose_name = 'Language for video translation'
        verbose_name_plural = 'Languages for video translation'

    def __str__(self):
        return self.name_of_language


class ChangeEmailModel(models.Model):
    email2 = models.CharField(max_length=100, verbose_name='New email', null=True, blank=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name='User', unique=True)

    # def get_absolute_url(self):
    #     return reverse('', kwargs={'language': self.language})
