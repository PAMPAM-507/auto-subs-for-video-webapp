import os
import sys
import traceback
from typing import NoReturn

import redis
import whisper.transcribe
from celery import shared_task
from auto_subs.celery import app

from auto_subs.settings import BASE_DIR, BASE_PATH_OF_VIDEO, \
    REDIS_HOST, REDIS_PORT, logger, PATH_FOR_SUBTITLES, \
    PATH_FOR_VIDEO_WITH_SUBS, EMAIL_HOST_PASSWORD, EMAIL_HOST, \
    EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER, PATH_FOR_AUDIO

from django.core.mail import send_mail, send_mass_mail
from django.db.models import F


from .models import UserVideos

from web_app_auto_subs.utils.services.subtitles1.progress_bar import DjangoORMProgressValue, RedisProgressValue
from web_app_auto_subs.utils.services.subtitles1.start_whisper import StartWhisper
from web_app_auto_subs.utils.services.subtitles1.remove_all_helping_files import RemoveAllHelpingFiles
from web_app_auto_subs.utils.services.subtitles1.handle_video import HandleVideo
from web_app_auto_subs.utils.services.make_srt import MakingSrt
from .utils.services.email.send_email import SendEmail


@app.task
def send_email(subject: str, message: str, to_email: list) -> NoReturn:
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        to_email,
    )

from django.db import transaction

# @transaction.on_commit
@app.task
def test_task():
    print(UserVideos.objects.all())
    print(round(UserVideos.objects.get(\
                pk=70).videos_with_subs.file.size / (1024 * 1024)))
    
    

    
    UserVideos.objects.filter(pk=70).update(
            rendering_progress=100,
            whisper_progress=100,
            translate_progress=100,
            voiceover_progress=100,
            # video_size=round(UserVideos.objects.get(
            #     pk=video_pk).videos_with_subs.file.size / (1024 * 1024))
        )


@app.task
def make_subs(video_pk: int,
              path_of_video: str,
              subs_language: str,
              make_audio_record: bool,
              user_email: str,
              page_number: int,
              size_of_model: str = 'tiny',
              language_for_model: str = 'en',) -> NoReturn:

    import torch

    print(torch.cuda.is_available())
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("CUDA is not available. No GPU found.")

    try:

        StartWhisper(progress_value=RedisProgressValue(redis_client=redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)),
                     saver_progress_results=DjangoORMProgressValue(
                         model=UserVideos,
                         attribute='whisper_progress')).run(
            video_pk=video_pk,
            path_of_video=path_of_video,
            size_of_model=size_of_model,
            language_for_model=language_for_model,
        )

    except Exception as e:
        tb_message = traceback.format_exc()
        logger.error(f'Whisper error occurred: {tb_message}')

    else:
        # try:
        # srt_filepath = PATH_FOR_SUBTITLES + path_of_video.split('/')[-1][:-3] + 'srt'
        # MakingSrt.write_srt(result, srt_filepath)

        name_of_video = path_of_video.split("/")[-1]

        HandleVideo.handle_video(
            video_pk=video_pk,
            name_of_video=name_of_video,
            path_for_video=path_of_video,
            path_for_new_video=PATH_FOR_VIDEO_WITH_SUBS,
            path_of_audio=PATH_FOR_AUDIO,
            path_with_str=PATH_FOR_SUBTITLES,
            translate_var=make_audio_record,
            src_language=language_for_model,
            dest_language=subs_language,
        )

        # except Exception as e:
        #     logger.error(f'Error occurred: {e}')

        # else:
        # , BASE_PATH_OF_VIDEO+'videos']:

        for path in [PATH_FOR_AUDIO, PATH_FOR_SUBTITLES]:
            RemoveAllHelpingFiles.remove(
                path=path,
                base_filename=name_of_video.split(".")[0]
            )

        UserVideos.objects.filter(pk=video_pk).update(
            rendering_progress=100,
            whisper_progress=100,
            translate_progress=100,
            voiceover_progress=100,
            video_size=round(UserVideos.objects.get(
                pk=video_pk).videos_with_subs.file.size / (1024 * 1024))
        )

        # if user_email:
        #     message = f'Здравствуйте, {user_email}, видео обработано!  Перейдите по ссылке, чтобы посмотреть: http://127.0.0.1:8000/personal_account/?page={page_number}'
        #     send_email(subject='PAMPAM-auto-subs.ru. Ссылка на обработанное видео',
        #                message=message, to_email=[user_email,])