from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError


class DocumentForm(forms.ModelForm):
    subs_language = forms.ModelChoiceField(
        queryset=LanguagesForTranslateVideo.objects.all(),
        label='Выберите язык для субтитров',
        # initial ='Русский',
    )
    video = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        label='Загрузка видео'                  
        )

    class Meta:
        model = UserVideos
        fields = ('video', 'make_audio_record')
        widgets = {'user': forms.HiddenInput(),}


class RegisterUserForm(UserCreationForm):
    username = forms.EmailField(label='Email ')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль ')
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Повторение пароля ')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserFrom(AuthenticationForm):
    username = forms.EmailField(label='Email ')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль ')

    class Meta:
        model = User
        fields = ('username', 'password',)


class ChangeUserInfoForm(forms.Form):
    choose_form = forms.ChoiceField(
        choices=((0, 'Смена пароля'), (1, 'Смена адреса электронной почты')),
        label='Выберите, что вы хотите изменить',

    )
    
# class UpdateUserInfoForm(forms.ModelForm):
    
    
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'password')
        


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Пароль ', required=True)
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, label='Новый пароль ', required=True)
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label='Повторите новый пароль ', required=True)
    
    
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        old_password = self.cleaned_data.get('old_password')
        
        if not new_password1:
            raise ValidationError('Новое поле пароля обязательно.')
        
        if new_password1 == old_password:
            raise ValidationError('Новый пароль должен отличаться от старого')
        
        return new_password1


    # class Meta:
    #     model = User
    #     fields = ('old_password', 'new_password1', 'new_password2',)


class ChangeEmailForm(forms.ModelForm):
    username = forms.EmailField(label='Новый email ')
    
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
