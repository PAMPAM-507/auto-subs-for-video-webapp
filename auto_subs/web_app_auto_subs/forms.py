from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class DocumentForm(forms.ModelForm):
    subs_language = forms.ModelChoiceField(
        queryset=LanguagesForTranslateVideo.objects.all(),
        label='Выберите язык для субтитров',
        empty_label=None,
    )

    class Meta:
        model = UserVideos
        fields = ('video',)
        widgets = {'user': forms.HiddenInput()}


class RegisterUser(UserCreationForm):
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
        choices=((1, 'Смена пароля'), (2, 'Смена адреса электронной почты')),
        label='Выберите, что вы хотите изменить',

    )


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Пароль ')
    new_password1 = forms.CharField(
        widget=forms.PasswordInput, label='Новый пароль ')
    new_password2 = forms.CharField(
        widget=forms.PasswordInput, label='Повторите новый пароль ')

    # class Meta:
    #     model = User
    #     fields = ('old_password', 'new_password1', 'new_password2',)






# <!--<form method="post" enctype="multipart/form-data">
#         {% scrf_token %}
#         <div>{{ form2.non_field_errors }}</div>
#         {% for f2 in form2 %}
#             <p><label for="f2.id.for_label">{{ label }}</label>{{ f2 }}</p>
#         {% endfor %}
#     </form>-->
