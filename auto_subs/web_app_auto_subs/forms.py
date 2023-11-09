from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class DocumentForm(forms.ModelForm):
    # user = forms.CharField(editable=False)
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
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторение пароля ')

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class LanguageForm(forms.ModelForm):
    video_language = forms.ModelChoiceField(
        queryset=LanguagesForTranslateVideo.objects.all(),
        label='Язык оригинального файла',
    )
    subs_language = forms.ModelChoiceField(
        queryset=LanguagesForTranslateVideo.objects.all(),
        label='Выберите язык для субтитров',
    )

    class Meta:
        model = LanguagesForTranslateVideo
        fields = ('language',)


# <!--<form method="post" enctype="multipart/form-data">
#         {% scrf_token %}
#         <div>{{ form2.non_field_errors }}</div>
#         {% for f2 in form2 %}
#             <p><label for="f2.id.for_label">{{ label }}</label>{{ f2 }}</p>
#         {% endfor %}
#     </form>-->