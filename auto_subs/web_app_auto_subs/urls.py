from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView


from .views import *

urlpatterns = [
    path('', MainMenu.as_view(), name='main'),
    path('upload_video/', UploadVideo.as_view(), name='upload_video'),


    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutViewWithGet.as_view(), name='logout'),
    
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate,
         name='activate'),
    path('personal_account/', PersonalAccount.as_view(), name='personal_account'),
    path('personal_account/<int:pk>/', GetVideo.as_view(), name='watch_video'),
    path('stream/<int:pk>/', get_streaming_video, name='stream'),

    path('edit_profile/', ChangeUserInfo.as_view(), name='edit_profile'),
    
    path('change_password/', ChangePassword.as_view(), name='password_change'),
    path('change_password_done/', PasswordChangeDoneView.as_view(template_name='web_app_auto_subs/password_change_done.html'), name='password_change_done'),
    
    path('change_email/', ChangeEmail.as_view(), name='change_email'),
    path('change_email_done/', ChangeEmailDone.as_view(), name='change_email_done'),



]
