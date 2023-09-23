from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class DocumentForm(forms.ModelForm):
    # user = forms.CharField(editable=False)

    class Meta:
        model = UserVideos
        fields = ('video',)
        widgets = {'user': forms.HiddenInput()}


class RegisterUser(UserCreationForm):
    username = forms.EmailField(label='Email ')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль ')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторение пароля ')

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
