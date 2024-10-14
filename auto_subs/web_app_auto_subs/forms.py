import os
import subprocess
from typing import NoReturn
import uuid
from django import forms

from .models import *

from auto_subs.settings import BASE_PATH_OF_VIDEO
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError


class DocumentForm(forms.ModelForm):
    
    video_language = forms.ModelChoiceField(
        queryset=LanguagesForTranslateVideo.objects.all(),
        label='Select the language used in the original video',
        initial =LanguagesForTranslateVideo.objects.get(language='en'),
    )
    
    subs_language = forms.ModelChoiceField(
        queryset=LanguagesForTranslateVideo.objects.all(),
        label='Select the language for subtitles',
        initial =LanguagesForTranslateVideo.objects.get(language='ru'),
    )
    
    video = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        label='Uploading a video'                  
        )
    
    make_audio_record = forms.BooleanField(label='Do I need to make an audio translation', initial=False, required=False)

    class Meta:
        model = UserVideos
        fields = ('video', 'make_audio_record')
        widgets = {'user': forms.HiddenInput(),}
    
    
    def clean_subs_language(self):
        subs_language = self.cleaned_data['subs_language']
        video_language = self.cleaned_data['video_language']
        make_audio_record = self.cleaned_data['make_audio_record']
        
        if subs_language == video_language and make_audio_record:
            raise ValidationError('The languages for subtitles and the language used in the video must not match when audio translation is enabled')

        return subs_language
    
    
    def clean_video(self):
        
        def delete_temp_video(path: str) -> NoReturn:
            try:
                os.remove(path)
                print(f"File {path} successfully deleted")
            except FileNotFoundError:
                print(f"File {path} not found")
            except PermissionError:
                print(f"There are no permissions to delete the file {path}")
            except Exception as e:
                print(f"Error deleting a file: {e}")
        
        
        video = self.cleaned_data['video']
        path = f'{BASE_PATH_OF_VIDEO}/temp_video{uuid.uuid4()}.mp4'
        
        with open(path, 'wb+') as temp_file:
            for chunk in video.chunks():
                temp_file.write(chunk)
    
        try:
            # Запуск ffmpeg для анализа файла
            result = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'null', '-'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                delete_temp_video(path)
                raise ValidationError('This file is not a valid video file')
        
        except subprocess.CalledProcessError:
            delete_temp_video(path)
            raise ValidationError('Error checking the video file')
        
        else:
            delete_temp_video(path)
            return video

class RegisterUserForm(UserCreationForm):
    usable_password = None
    
    username = forms.EmailField(label='Email ')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password ')
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Password repetition ')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserFrom(AuthenticationForm):
    username = forms.EmailField(label='Email ')
    password = forms.CharField(widget=forms.PasswordInput, label='Password ')

    class Meta:
        model = User
        fields = ('username', 'password',)


class ChangeUserInfoForm(forms.Form):
    choose_form = forms.ChoiceField(
        choices=((0, 'Changing the password'), (1, 'Changing the email address')),
        label='Choose what you want to change',

    )
    
# class UpdateUserInfoForm(forms.ModelForm):
    
    
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'password')
        


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Password ', required=True)
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, label='New password', required=True)
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label='Repeat the new password ', required=True)
    
    
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')
        
        if not new_password1:
            raise ValidationError('A new password field is required')
        
        if new_password1 == old_password:
            raise ValidationError('The new password must be different from the old one')
        
        return new_password1


    # class Meta:
    #     model = User
    #     fields = ('old_password', 'new_password1', 'new_password2',)


class ChangeEmailForm(forms.ModelForm):
    username = forms.EmailField(label='New email address ')
    
    class Meta:
        model = User
        fields = ('username',)

# <!--<form method="post" enctype="multipart/form-data">
#         {% scrf_token %}
#         <div>{{ form2.non_field_errors }}</div>
#         {% for f2 in form2 %}
#             <p><label for="f2.id.for_label">{{ label }}</label>{{ f2 }}</p>
#         {% endfor %}
#     </form>-->
