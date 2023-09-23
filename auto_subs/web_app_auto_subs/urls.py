from django.urls import path
from .views import *

urlpatterns = [
    path('', MainMenu.as_view(), name='main'),
    path('upload_video/', UploadVideo.as_view(), name='upload_video'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate,
         name='activate'),

]
