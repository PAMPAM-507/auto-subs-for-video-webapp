from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model

from web_app_auto_subs.tasks import send_email
from web_app_auto_subs.utils.services.email.render_message import RenderMessage
from web_app_auto_subs.utils.services.email.token import account_activation_token


class RegisterMixin:

    def send_mail_to_confirm_registration(self, user):
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
            to_email=[user.username, ]
            # to_email=['andrewselan2001@gmail.com', ]
        )
    
    def handle_errors_related_to_wrong_adding_user(self, user):
            
            wrong_user = get_user_model.objects.get(username=user.username)

            if wrong_user:
                wrong_user.delete()