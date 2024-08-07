from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from web_app_auto_subs.utils.business_logic.mixins.register_mixin import RegisterMixin
from web_app_auto_subs.utils.business_logic.mixins.context_mixin import ContextMixin
from web_app_auto_subs.utils.business_logic.mixins.upload_video_mixin import UploadVideoMixin

from .utils.business_logic.reduction_for_views.reductions import handle_redirect_for_ChangeUserInfo_view_with_get_method, handle_errors_for_ChangePassword_view_with_post_method
from .forms import *
from .tasks import *
from .models import *
from .utils.services.email.render_message import RenderMessage
from .utils.services.email.token import account_activation_token
from .utils.services.sending_video_stream.video_stream import VideoStream
from .utils.dao.queries.all_query import AllQuery
from .utils.dao.queries.filter_query import FilterQuery
from .utils.dao.queries.get_query import GetQuery
from .utils.dao.queries.update_query import GetLatestModel
from .utils.services.email.abstractapi import validate_email


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import StreamingHttpResponse
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic.edit import CreateView, FormView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from auto_subs.settings import BASE_DIR, BASE_PATH_OF_VIDEO, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER, PATH_FOR_VIDEO_WITH_SUBS
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.core.paginator import Paginator

menu = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'Загрузить видео', 'url_name': 'upload_video'},
    # {'title': 'Профиль', 'url_name': 'personal_account'}

]


class UploadVideo(LoginRequiredMixin, UploadVideoMixin, ContextMixin, FormView):
    template_name = 'web_app_auto_subs/upload_video.html'
    form_class = DocumentForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context,)
        return context

    def form_valid(self, form):

        form = form.save(commit=False)

        subs_language_pk = self.request.POST.get('subs_language')

        form.user = self.request.user

        form.save()

        user_video = UserVideos.objects.filter(
            user=self.request.user).latest('uploaded_at')
        user_video.name_of_video = self.get_name_of_video(user_video.video)
        user_video.videos_with_subs = self.get_name_of_video_with_subs(
            user_video.name_of_video)
        user_video.save()

        user_video = UserVideos.objects.filter(
            user=self.request.user).latest('uploaded_at')

        subs_language = LanguagesForTranslateVideo.objects.get(
            pk=subs_language_pk)

        make_subs.delay(BASE_PATH_OF_VIDEO +
                        str(user_video.video), str(subs_language.language))

        return super().form_valid(form)


class MainMenu(ContextMixin, TemplateView):
    template_name = 'web_app_auto_subs/base.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        self.get_mixin_context(
            context, message=Title.objects.get(name='Описание').title)
        return context


class RegisterUser(RegisterMixin, ContextMixin, CreateView):
    form_class = RegisterUserForm  # UserCreationForm
    template_name = 'web_app_auto_subs/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context= super().get_context_data(**kwargs)
        self.get_mixin_context(context, cur_menu=' ')

        return context

    def form_valid(self, form):

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        obj = ExpansionForUser(pk=user.id, email2='xxx', user=user)
        obj.save()

        try:
            self.send_mail_to_confirm_registration(user)

        except:
            form.add_error(None, 'Не удалось отправить сообщение')

            self.handle_errors_related_to_wrong_adding_user(user)


        return super().form_valid(form)
    


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

        obj = ExpansionForUser.objects.get(user=uid)

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
    form_class = LoginUserFrom
    template_name = 'web_app_auto_subs/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context)

        return context

    def get_success_url(self):
        return reverse_lazy('main')


class PersonalAccount(LoginRequiredMixin, View):
    login_url = "/login/"
    template_name = 'web_app_auto_subs/personal_account.html'

    def get(self, request, user_pk, *args, **kwargs):
        # videos = UserVideos.objects.filter(user=request.user.id)

        videos = FilterQuery().filter_query(UserVideos, 'name_of_video', 'get_absolute_url', 'pk',
                                            user=user_pk,
                                            )

        paginator = Paginator(videos, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'cur_menu': 'Профиль',
            # 'videos': videos,
            'page_obj': page_obj,
            'user_pk': user_pk,
        }

        return render(request, self.template_name, context)


class GetVideo(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'web_app_auto_subs/video.html'

    def get(self, request, user_pk, pk, *args, **kwargs):
        # video = UserVideos.objects.get(user=request.user.id, pk=pk)
        video = GetQuery().get_query(UserVideos, 'name_of_video', 'get_absolute_url', 'pk',
                                     user=request.user.id, pk=pk,
                                     )

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'video': video,

        }

        return render(request, self.template_name, context)


def get_streaming_video(request, user_pk, pk: int):
    file, status_code, content_length, content_range = VideoStream().open_file(request, pk)
    response = StreamingHttpResponse(
        file, status=status_code, content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response


class ChangeUserInfo(LoginRequiredMixin, View):
    form_class = ChangeUserInfoForm
    template_name = 'web_app_auto_subs/edit_profile.html'

    def get(self, request, user_pk, *args, **kwargs):

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'form': self.form_class,

        }

        return render(request, self.template_name, context)

    def post(self, request, user_pk, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            addr = handle_redirect_for_ChangeUserInfo_view_with_get_method(
                choose_form=form.cleaned_data.get('choose_form')
            )

            return redirect(addr, user_pk=user_pk)

        return redirect('main')


class ChangePassword(LoginRequiredMixin, View):
    form_class = ChangePasswordForm
    template_name = 'web_app_auto_subs/change_password.html'

    def get(self, request, user_pk, *args, **kwargs):

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'form': self.form_class(request.user),
        }

        return render(request, self.template_name, context)

    def post(self, request, user_pk, *args, **kwargs):

        form = self.form_class(request.user, request.POST)

        old_password = 'old_password'
        new_password1 = 'new_password1'
        new_password2 = 'new_password2'

        if form.is_valid():

            user = form.save()

            user.set_password(form.cleaned_data.get('password1'))
            update_session_auth_hash(request, user)

            return redirect('login')

        else:
            message = handle_errors_for_ChangePassword_view_with_post_method(
                new_password1=form.data.get(new_password1),
                new_password2=form.data.get(new_password2),
            )

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'form': self.form_class(request.user),
            'message': message

        }

        return render(request, self.template_name, context)


class ChangeEmail(LoginRequiredMixin, View):
    form_class = ChangeEmailForm
    template_name = 'web_app_auto_subs/change_email.html'

    def get(self, request, *args, **kwargs):

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'form': self.form_class,
        }

        return render(request, self.template_name, context)

    def post(self, request, user_pk, *args, **kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            user = User.objects.get(pk=request.user.id)
            update_session_auth_hash(request, user)

            obj = ExpansionForUser.objects.get(user=request.user.id)
            obj.email2 = form.cleaned_data.get('username')
            obj.save()

            valid = validate_email(str(form.cleaned_data.get('username')))
            print('valid', valid)

            if valid:

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

        context = {
            'menu': menu,
            'title': 'ПАМ ПАМ',
            'form': self.form_class,
            'message': 'Пожалуйста, подтвердите свой адрес электронной почты',
        }

        return render(request, self.template_name, context)
