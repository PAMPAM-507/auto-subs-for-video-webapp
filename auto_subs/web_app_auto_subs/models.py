from django.db import models
from django.contrib.auth.models import User


class UserVideos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    video = models.FileField(upload_to='videos/%Y/%m/%d/', verbose_name='Видео')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    videos_with_subs = models.FileField(upload_to='videos_with_subs/%Y/%m/%d/', null=True, verbose_name='Видео с субтитрами')


