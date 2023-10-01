from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import *
from .tasks import *
from .utils.services.email.render_message import RenderMessage
from .utils.services.email.token import account_activation_token
from .services import open_file

from django.http import StreamingHttpResponse
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from auto_subs.settings import BASE_DIR, base_path_of_video, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER, path_for_video_with_subs
from django.contrib.auth.mixins import LoginRequiredMixin

menu = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'Загрузить видео', 'url_name': 'upload_video'},
    {'title': 'Профиль', 'url_name': 'personal_account'}

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
            obj.videos_with_subs = (
                                       (path_for_video_with_subs + f'{obj.video}')[0:-4]
                                   ) + '_subtitled' + ".mp4"
            obj.name_of_video = str(obj.video).split('/')[-1][0:-4]
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


class RegisterUser(View):
    form_class = RegisterUser  # UserCreationForm
    template_name = 'web_app_auto_subs/register.html'
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class(),
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'cur_menu': ' ',

        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            message = RenderMessage().render_message(
                'web_app_auto_subs/render_to_string/acc_activate_email.html',
                {
                    'user': user,
                    'domain': get_current_site(self.request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )

            send_email.delay(
                subject='Ссылка для активации была отправлена на ваш электронный адрес',
                message=message,
                to_email=[form.cleaned_data.get('username'), ]
                # to_email=['andrewselan2001@gmail.com', ]
            )

            context = {
                'message': 'Пожалуйста, подтвердите свой адрес электронной почты, чтобы завершить регистрацию',
                'redirect_url': menu[0].get('url_name'),
                'redirect_title': menu[0].get('title'),
            }

            return render(request, 'web_app_auto_subs/render_to_string/activate_message.html', context)
        else:
            return redirect('register')


def activate(request, uidb64, token):
    context = {
        'redirect_url': menu[0].get('url_name'),
        'redirect_title': menu[0].get('title'),
    }

    User = get_user_model()  # метод вернет текущую активную модель пользователя
    try:
        # расшифровывает/декодирует байтоподобный объект s или строку
        uid = force_str(urlsafe_base64_decode(uidb64))
        # ASCII, закодированный в Base64
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # проверяет соответствует ли токен юзеру
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        context[
            'message'] = 'Благодарим вас за подтверждение по электронной почте. Теперь вы можете войти в свою учетную запись'

        return render(request, 'web_app_auto_subs/render_to_string/activate_message.html', context)

    else:

        context['message'] = 'Ссылка для активации недействительна'

        return render(request, 'web_app_auto_subs/render_to_string/activate_message.html', context)


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


class PersonalAccount(LoginRequiredMixin, View):
    login_url = "/login/"
    template_name = 'web_app_auto_subs/personal_account.html'

    def get(self, request, *args, **kwargs):
        videos = UserVideos.objects.filter(user=request.user.id)

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'cur_menu': 'Профиль',
            'videos': videos,

        }

        return render(request, self.template_name, context)


class GetVideo(LoginRequiredMixin, View):
    login_url = "/login/"
    template_name = 'web_app_auto_subs/video.html'

    def get(self, request, pk, *args, **kwargs):
        video = UserVideos.objects.get(user=request.user.id, pk=pk)

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'video': video,

        }

        return render(request, self.template_name, context)


def get_streaming_video(request, pk: int):
    file, status_code, content_length, content_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response
