from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class UserVideos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')

    video = models.FileField(upload_to='videos/%Y/%m/%d/',
                             verbose_name='Видео',
                             validators=[FileExtensionValidator(
                                 allowed_extensions=['mp4'])])

    uploaded_at = models.DateTimeField(auto_now_add=True)

    videos_with_subs = models.FileField(upload_to='videos_with_subs/%Y/%m/%d/',
                                        null=True, verbose_name='Видео с субтитрами')

    name_of_video = models.CharField(max_length=50,
                                     verbose_name='Название видео', null=True)

    def get_absolute_url(self):
        return reverse('watch_video', kwargs={'pk': self.pk})
