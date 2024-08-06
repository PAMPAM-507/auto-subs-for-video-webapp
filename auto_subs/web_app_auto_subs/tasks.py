import os
# from .main import *
from web_app_auto_subs.utils.services.make_srt import MakingSrt
import whisper.transcribe

from web_app_auto_subs.utils.business_logic.subtitles.main import execute_bs_for_make_subs

from celery import shared_task
from auto_subs.celery import app
from auto_subs.settings import BASE_DIR, PATH_FOR_SUBTITLES, PATH_FOR_VIDEO_WITH_SUBS, EMAIL_HOST_PASSWORD, EMAIL_HOST, \
    EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER
from .utils.services.email.send_email import SendEmail


# @app.task
# def make_subs(path_of_video: str,
#               subs_language: str,
#               size_of_model: str = 'tiny',
#               language_for_model: str = 'en'):
#     os.system(
#         f'cd {PATH_FOR_SUBTITLES} && whisper {path_of_video} --model {size_of_model} --language {language_for_model}'
#     )

import os
import logging

logger = logging.getLogger('main')

@app.task
def make_subs(path_of_video: str,
              subs_language: str,
              size_of_model: str = 'tiny',
              language_for_model: str = 'en'):
    try:
        command = f'cd {PATH_FOR_SUBTITLES} && whisper {path_of_video} --model {size_of_model} --language {language_for_model}'
        logger.info(f'Executing command: {command}')
        os.system(command)
        logger.info('Command executed successfully')
    except Exception as e:
        logger.error(f'Error occurred: {e}')

    # model = whisper.load_model(size_of_model)
    # result = model.transcribe(path_of_video, language=language_for_model, fp16=False, verbose=None)
    # srt_filepath = PATH_FOR_SUBTITLES + path_of_video.split('/')[-1][:-3] + 'srt'

    # print(srt_filepath)

    # MakingSrt.write_srt(result, srt_filepath)

    execute_bs_for_make_subs(
        path_of_video, PATH_FOR_SUBTITLES, PATH_FOR_VIDEO_WITH_SUBS, subs_language
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
