from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', MainMenu.as_view(), name='main'),
    path('upload_video/', UploadVideo.as_view(), name='upload_video'),


    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate,
         name='activate'),
    path('personal_account/<int:user_pk>/', PersonalAccount.as_view(), name='personal_account'),
    path('personal_account/<int:user_pk>/<int:pk>/', GetVideo.as_view(), name='watch_video'),
    path('stream/<int:user_pk>/<int:pk>/', get_streaming_video, name='stream'),

    path('edit_profile/<int:user_pk>/', ChangeUserInfo.as_view(), name='edit_profile'),
    
    path('change_password/<int:user_pk>/', ChangePassword.as_view(), name='change_password'),
    path('change_email/<int:user_pk>/', ChangeEmail.as_view(), name='change_email'),



]
