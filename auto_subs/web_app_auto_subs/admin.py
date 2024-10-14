from django.contrib import admin
from django.db.models.base import Model as Model
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from .models import *


# Upper header (in the top left corner)
admin.site.site_header = "Admin Panel"
# Page title (browser tabs)
admin.site.site_title = "Site Admin Panel"
# Title on the main admin page
admin.site.index_title = "Welcome to the Admin Panel"


class VideoSizeFilter(admin.SimpleListFilter):
    title = 'Video Size'
    parameter_name = 'video_size'

    def lookups(self, request, model_admin):
        return [
            ('Small', 'Small (up to 20 MB)'),
            ('Medium', 'Medium (from 20 to 50 MB)'),
            ('Large', 'Large (more than 50 MB)')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Small':
            return queryset.filter(video_size__lte=20 * 1024 * 1024)
        elif self.value() == 'Medium':
            return queryset.filter(video_size__gt=20 * 1024 * 1024, video_size__lte=50 * 1024 * 1024)
        elif self.value() == 'Large':
            return queryset.filter(video_size__gt=50 * 1024 * 1024)
        return queryset


@admin.register(UserVideos)
class UserVideosAdmin(admin.ModelAdmin):
    fields = ['id',
              'user',
              'uploaded_at',
              'name_of_video',
              'video',
              'videos_with_subs', 'video_size', 'watch_video',
              'rendering_progress',
              'whisper_progress',
              'translate_progress',
              'voiceover_progress',]

    readonly_fields = ['id', 'uploaded_at', 'watch_video', 'video_size', ]

    list_display = ('id',
                    'user',
                    'name_of_video',
                    'uploaded_at',
                    'video_size',
                    'watch_video',)

    list_display_links = ('id', 'user',)
    search_fields = ('user', 'uploaded_at', 'name_of_video',)
    list_filter = ('uploaded_at', VideoSizeFilter)

    @admin.display(description='Processed Video')
    def watch_video(self, object: Model):
        if object.videos_with_subs:
            html = f"""
            <video
                id="my-video"
                class="video-js"
                controls
                preload="auto"
                width="500"
                height="300"
            >
                <source src="/stream/{object.pk}" type="video/mp4">
                Your browser does not support the video tag.
            </video>

            <script src="https://vjs.zencdn.net/8.5.2/video.min.js"></script>
            """
            return mark_safe(html)
        else:
            return "Video not uploaded"


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_filter = ('name',)


@admin.register(LanguagesForTranslateVideo)
class LanguagesForTranslateVideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'name_of_language',)
    list_display_links = ('id', 'language',)
    search_fields = ('id', 'language',)
    # list_filter = ('language', )
