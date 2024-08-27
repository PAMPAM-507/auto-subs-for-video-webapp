import os

import whisper.transcribe
from celery import shared_task
from auto_subs.celery import app

from auto_subs.settings import BASE_DIR, PATH_FOR_SUBTITLES, PATH_FOR_VIDEO_WITH_SUBS, EMAIL_HOST_PASSWORD, EMAIL_HOST, \
    EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER, PATH_FOR_AUDIO
    
from django.core.mail import send_mail, send_mass_mail

from web_app_auto_subs.utils.business_logic.subtitles.main import execute_bs_for_make_subs
from web_app_auto_subs.utils.business_logic.subtitles1.handle_video import HandleVideo
from web_app_auto_subs.utils.services.make_srt import MakingSrt
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
              make_audio_record: bool,
              size_of_model: str = 'tiny',
              language_for_model: str = 'en',):
    try:
        command = f'cd {PATH_FOR_SUBTITLES} && whisper {path_of_video} --model {size_of_model} --language {language_for_model}'
        logger.info(f'Executing command: {command}')
        os.system(command)
        logger.info('Command executed successfully')
    except Exception as e:
        logger.error(f'Error occurred: {e}')
    
    # model = whisper.load_model(size_of_model,)
    # result = model.transcribe(
    #     path_of_video, 
    #     language=language_for_model, 
    #     fp16=False, 
    #     verbose=None,
    #     )
    
    # srt_filepath = PATH_FOR_SUBTITLES + path_of_video.split('/')[-1][:-3] + 'srt'
    # MakingSrt.write_srt(result, srt_filepath)
        
    
    HandleVideo().handle_video(
            name_of_video=path_of_video.split("/")[-1],
            path_for_video=path_of_video, 
            path_for_new_video=PATH_FOR_VIDEO_WITH_SUBS,
            path_of_audio=PATH_FOR_AUDIO,
            path_with_str=PATH_FOR_SUBTITLES,
            translate_var=make_audio_record,
        )


@app.task
def send_email(subject: str, message: str, to_email: list):
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        to_email,
    )
