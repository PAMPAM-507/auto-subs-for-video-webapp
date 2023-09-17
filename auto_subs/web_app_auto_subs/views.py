from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from .tasks import *

from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from auto_subs.settings import BASE_DIR, base_path_of_video
from django.contrib.auth.mixins import LoginRequiredMixin

menu = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'Загрузить видео', 'url_name': 'upload_video'},
    # {'title': 'Профиль', 'url_name': 'profile'}

]


class UploadVideo(LoginRequiredMixin, View):
    login_url = "/login/"
    form_class = DocumentForm
    template_name = 'web_app_auto_subs/upload_video.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {
            'form': form,
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'cur_menu': 'Загрузить видео',

        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            path = UserVideos.objects.filter(user=request.user.id).latest('uploaded_at')
            path = path.video
            make_subs.delay(base_path_of_video + str(path))
            return redirect('main')


class MainMenu(View):
    template_name = 'web_app_auto_subs/base.html'

    def get(self, request, *args, **kwargs):
        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'cur_menu': 'Главная'
        }

        return render(request, self.template_name, context)


class RegisterUser(CreateView):
    form_class = RegisterUser  # UserCreationForm
    template_name = 'web_app_auto_subs/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu

        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


def logout_user(request):
    logout(request)
    return redirect('main')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'web_app_auto_subs/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu

        return context

    def get_success_url(self):
        return reverse_lazy('main')
