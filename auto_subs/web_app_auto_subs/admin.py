from django.contrib import admin
from .models import *


@admin.register(UserVideos)
class UserVideosAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name_of_video', 'uploaded_at',)
    list_display_links = ('id', 'user',)
    search_fields = ('user', 'uploaded_at', 'name_of_video',)
    list_filter = ('user', 'uploaded_at')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_filter = ('id', 'name',)


@admin.register(LanguagesForTranslateVideo)
class LanguagesForTranslateVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'language',)
    list_display_links = ('id', 'language',)
    search_fields = ('id', 'language',)
    list_filter = ('id', 'language',)