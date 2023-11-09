import os
# from .main import *
from web_app_auto_subs.utils.business_logic.subtitles.main import execute_bs_for_make_subs

from celery import shared_task
from auto_subs.celery import app
from auto_subs.settings import BASE_DIR, path_for_subtitles, path_for_video_with_subs, EMAIL_HOST_PASSWORD, EMAIL_HOST, \
    EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER
from .utils.services.email.send_email import SendEmail


@app.task
def make_subs(path_of_video: str,
              subs_language: str,
              size_of_model: str = 'tiny',
              language_for_model: str = 'en'):
    os.system(
        f'cd {path_for_subtitles} && whisper {path_of_video} --model {size_of_model} --language {language_for_model}'
    )
    execute_bs_for_make_subs(
        path_of_video, path_for_subtitles, path_for_video_with_subs, subs_language
    )


@app.task
def send_email(subject: str, message: str, to_email: list):
    SendEmail(
        EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER,
        EMAIL_HOST_PASSWORD, EMAIL_USE_TLS,
    ).send(
        subject=subject,
        message=message,
        email_from=EMAIL_HOST_USER,
        to_email=to_email
    )
