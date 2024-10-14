
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from web_app_auto_subs import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web_app_auto_subs.urls')),
    path('social_auth/', include('social_django.urls', namespace='social')),
    # path('accounts/', include('allauth.urls')),
]

handler404 = views.page_not_found

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

