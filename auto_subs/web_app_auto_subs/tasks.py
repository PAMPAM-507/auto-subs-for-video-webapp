import os
from .main import *

from celery import shared_task
from auto_subs.celery import app
from auto_subs.settings import BASE_DIR, path_for_subtitles, path_for_video_with_subs, EMAIL_HOST_PASSWORD, EMAIL_HOST, \
    EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER
from .utils.services.email.send_email import SendEmail


@app.task
def make_subs(path_of_video: str):
    # path_for_subtitles = str(BASE_DIR) + '/media/subtitles/'
    # path_for_video_with_subs = str(BASE_DIR) + '/media/videos_with_subs/'
    os.system(f'cd {path_for_subtitles} && whisper {path_of_video}')
    execute_bs_for_make_subs(path_of_video, path_for_subtitles, path_for_video_with_subs)


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
