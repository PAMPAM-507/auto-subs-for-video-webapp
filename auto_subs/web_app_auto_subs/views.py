from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Any

from django.db.models.base import Model as Model
from django.forms import Form as Form
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpRequest, FileResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import connection
from django.core.cache import cache


from auto_subs.settings import BASE_PATH_OF_VIDEO, PATH_FOR_VIDEO_WITH_SUBS, PATH_FOR_VIDEOS
from web_app_auto_subs.utils.services.mixins.progress_bar_api_mixin import ProgressBarAPIMixin
from web_app_auto_subs.utils.services.mixins.change_email_mixin import ChangeEmailMixin
from web_app_auto_subs.utils.services.mixins.register_mixin import RegisterMixin
from web_app_auto_subs.utils.services.mixins.context_mixin import ContextMixin
from web_app_auto_subs.utils.services.mixins.upload_video_mixin import UploadVideoMixin

from .forms import *
from .tasks import *
from .models import *
from .utils.services.email.render_message import RenderMessage
from .utils.services.email.token import account_activation_token
from .utils.services.sending_video_stream.video_stream import VideoStream
from .utils.services.email.abstractapi import validate_email

menu = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'Загрузить видео', 'url_name': 'upload_video'},
    # {'title': 'Профиль', 'url_name': 'personal_account'}

]


class UploadVideo(LoginRequiredMixin, UploadVideoMixin, ContextMixin, FormView):
    template_name: str = 'web_app_auto_subs/upload_video.html'
    form_class: Form = DocumentForm
    success_url: str = reverse_lazy('main')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context, cur_menu='Загрузить видео')
        return context

    def form_valid(self, form: Form) -> HttpResponse:
        
        user = self.request.user

        form = form.save(commit=False)

        subs_language_pk = self.request.POST.get('subs_language')
        video_language_pk = self.request.POST.get('video_language')

        form.user = user

        form.save()

        user_video = UserVideos.objects.filter(
            user=self.request.user).latest('uploaded_at')
        user_video.name_of_video = self.get_name_of_video(user_video.video)
        user_video.videos_with_subs = self.get_name_of_video_with_subs(
            user_video.name_of_video)
        user_video.save()

        subs_language = LanguagesForTranslateVideo.objects.get(
            pk=subs_language_pk)
        video_language = LanguagesForTranslateVideo.objects.get(
            pk=video_language_pk)
        
        user_videos = UserVideos.objects.filter(user=self.request.user)
        count_videos = user_videos.count()
        
        make_subs.delay(user_video.pk,
                        BASE_PATH_OF_VIDEO +
                        str(user_video.video),
                        str(subs_language.language),
                        bool(user_video.make_audio_record),
                        user_email=user.email,
                        page_number=count_videos,
                        language_for_model=video_language.language,
                        )

        return super().form_valid(form)

from django.conf import settings

from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import (
    NotTelegramDataError, 
    TelegramDataIsOutdatedError,
)

bot_name = settings.TELEGRAM_BOT_NAME
bot_token = settings.TELEGRAM_BOT_TOKEN
redirect_url = settings.TELEGRAM_LOGIN_REDIRECT_URL

class MainMenu(ContextMixin, TemplateView):
    template_name: str = 'web_app_auto_subs/base.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        message = cache.get('Description')
        if not message:
            message = Title.objects.get(name='Описание').title
            cache.set('Description', message, 1000)
            
        context = self.get_mixin_context(
            context, message=message, cur_menu='Главная')
        
        if self.request.GET.get('hash'):
            result = verify_telegram_authentication(
            bot_token=bot_token, request_data=self.request.GET
        )
            return HttpResponse('Hello, ' + result['first_name'] + '!')

            
            
        return context

from django_telegram_login.widgets.generator import (
    create_callback_login_widget,
    create_redirect_login_widget,
)
from django_telegram_login.widgets.constants import (
    SMALL, 
    MEDIUM, 
    LARGE,
    DISABLE_USER_PHOTO,
)
def callback(request):
    telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)

    context = {'telegram_login_widget': telegram_login_widget}
    return render(request, 'test.html', context)



class RegisterUser(RegisterMixin, ContextMixin, CreateView):
    form_class: Form = RegisterUserForm
    template_name: str = 'web_app_auto_subs/register.html'
    success_url: str = reverse_lazy('login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context, cur_menu=' ')

        return context

    def form_valid(self, form: Form) -> HttpResponse:
        group = Group.objects.get(name='Usual user')

        user = form.save(commit=False)
        user.is_active = False
        user.email = user.username
        user.save()

        if group:
            user.groups.add(group)

        obj = ChangeEmailModel(pk=user.id, email2='xxx', user=user)
        obj.save()

        try:
            self.send_mail_to_confirm_registration(user)

        except:
            form.add_error(None, 'Не удалось отправить сообщение')

            self.handle_errors_related_to_wrong_adding_user(user)

        return super().form_valid(form)


def activate(request, uidb64, token) -> HttpResponse:
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

        obj = ChangeEmailModel.objects.get(user=uid)

        # Обработка изменения email
        if obj.email2 != 'xxx':
            user.username = obj.email2
            update_session_auth_hash(request, user)
            obj.email2 = 'xxx'
            obj.save()

        user.is_active = True
        user.save()

        context[
            'message'] = 'Благодарим вас за подтверждение электронной почты. Теперь вы можете войти в свою учетную запись'

        return render(request, 'web_app_auto_subs/render_to_string/activate_message.html', context)

    else:

        context['message'] = 'Ссылка для активации недействительна'

        return render(request, 'web_app_auto_subs/render_to_string/activate_message.html', context)


class LoginUser(ContextMixin, LoginView):
    form_class: Form = LoginUserFrom
    template_name: str = 'web_app_auto_subs/login.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)

        return context

    def get_success_url(self) -> str:
        return reverse_lazy('main')


class LogoutViewWithGet(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.user.is_authenticated:
            logout(request)
        return redirect('main')


class PersonalAccount(LoginRequiredMixin, ContextMixin, ListView):
    template_name: str = 'web_app_auto_subs/personal_account.html'
    context_object_name: str = 'videos'
    paginate_by: int = 1
    # permission_required: str = 'web_app_auto_subs.social_auth'

    def get_queryset(self) -> QuerySet[UserVideos]:
        return UserVideos.objects.filter(user=self.request.user,)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context, cur_menu='Профиль')

        # Получение списка идентификаторов видео и добавление их в контекст
        video_ids = list(context['videos'].values_list('pk', flat=True))
        context['video_ids'] = video_ids

        return context


class DeleteVideoView(DeleteView):
    model: Model = UserVideos
    success_url: str = reverse_lazy('personal_account')
    pk_url_kwarg: str = 'video_pk'
    
    def form_valid(self, form):
        
        video = UserVideos.objects.get(pk=self.kwargs[self.pk_url_kwarg])
        
        RemoveAllHelpingFiles.remove(
            path=PATH_FOR_VIDEO_WITH_SUBS, 
            base_filename=video.name_of_video + '_subtitled'
            )
        
        RemoveAllHelpingFiles.remove(
            path=PATH_FOR_VIDEOS, 
            base_filename=video.name_of_video
            )
        
        return super().form_valid(form)


class GetVideo(LoginRequiredMixin, ContextMixin, DetailView):
    template_name: str = 'web_app_auto_subs/video.html'
    pk_url_kwarg: str = 'pk'
    context_object_name: str = 'video'

    def get_object(self, get_queryset=None) -> Model:
        return get_object_or_404(UserVideos, user=self.request.user.id, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context, )

        return context


def get_streaming_video(request, pk: int) -> StreamingHttpResponse:
    file, status_code, content_length, content_range = VideoStream().open_file(request, pk)
    response = StreamingHttpResponse(
        file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


def download_video(request, video_pk):
    video = get_object_or_404(UserVideos, pk=video_pk)
    file_path = video.videos_with_subs.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{video.name_of_video}.mp4"'
    return response


class MyPasswordResetView(PasswordResetView,):
    template_name='web_app_auto_subs/password_reset_form.html'
    email_template_name='web_app_auto_subs/password_reset_email.html'
    success_url=reverse_lazy('password_reset_done')
    # PasswordResetMixin, 
    
    def form_valid(self, form: Form) -> HttpResponse:
        
        print(form.cleaned_data.get('email'))
        
        user = get_user_model().objects.get(username=form.cleaned_data.get('email'))
        
        try:
            self.send_mail_to_confirm_registration(user)

        except:
            form.add_error(None, 'Не удалось отправить сообщение')

            self.handle_errors_related_to_wrong_adding_user(user)

        return super().form_valid(form)
        
    


class ChangeUserInfo(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    form_class: Form = ChangeUserInfoForm
    template_name: str = 'web_app_auto_subs/edit_profile.html'
    success_url: str = reverse_lazy('edit_profile')
    permission_required: str = 'auth.usual_user'

    def get_success_url(self) -> str:

        return reverse_lazy('password_change') if self.choose_form == 0 else reverse_lazy('change_email')

    def form_valid(self, form: ChangeUserInfoForm) -> HttpResponse:
        self.choose_form = int(form.cleaned_data.get('choose_form'))

        return super().form_valid(form)


class PasswordChange(PermissionRequiredMixin, LoginRequiredMixin, ContextMixin, PasswordChangeView):
    form_class: Form = ChangePasswordForm
    template_name: str = 'web_app_auto_subs/password_change.html'
    success_url: str = reverse_lazy('password_change_done')
    permission_required: str = 'auth.usual_user'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)

        return context

    def form_valid(self, form: ChangePasswordForm) -> HttpResponse:
        update_session_auth_hash(self.request, self.request.user)

        return super().form_valid(form)


class ChangeEmailDone(PermissionRequiredMixin, LoginRequiredMixin, ContextMixin, TemplateView):
    template_name: str = 'web_app_auto_subs/change_email_done.html'
    permission_required: str = 'auth.usual_user'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)

        return context


class ChangeEmail(PermissionRequiredMixin, LoginRequiredMixin, ChangeEmailMixin, ContextMixin, FormView):
    form_class: Form = ChangeEmailForm
    template_name: str = 'web_app_auto_subs/change_email.html'
    success_url: str = reverse_lazy('change_email_done')
    permission_required: str = 'auth.usual_user'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)

        return context

    def form_valid(self, form) -> HttpResponse:
        valid = validate_email(str(form.cleaned_data.get('username')))
        print('valid', valid)

        if valid:

            user = self.request.user

            self.mark_user_for_changing_password(
                user=user,
                email=form.cleaned_data.get('username'),
            )

            update_session_auth_hash(self.request, user)

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
            )

        else:
            form.add_error(None, 'Почта не прошла процесс валидации')

        return super().form_valid(form)


class test(ProgressBarAPIMixin, APIView):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        video_pk = int(request.GET.get("video_id"))

        rendering_progress, whisper_progress = 0, 0

        with redis.Redis(host='localhost', port=6380, db=0) as r:
            
            whisper_progress = self.get_progress_info(r, video_pk, 'whisper_progress')
            translate_progress = self.get_progress_info(r, video_pk, 'translate_progress')
            rendering_progress = self.get_progress_info(r, video_pk, 'rendering_progress')
            voiceover_progress = self.get_progress_info(r, video_pk, 'voiceover_progress')
        
        return Response({
            "video_id": video_pk,
            'moviepy_progress': rendering_progress,
            'translate_progress': translate_progress,
            'whisper_progress': whisper_progress,
            'voiceover_progress': voiceover_progress,
        })

