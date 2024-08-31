import os
import sys
from typing import NoReturn

import redis
import whisper.transcribe
from celery import shared_task
from auto_subs.celery import app

from auto_subs.settings import BASE_DIR, BASE_PATH_OF_VIDEO, logger, PATH_FOR_SUBTITLES, PATH_FOR_VIDEO_WITH_SUBS, EMAIL_HOST_PASSWORD, EMAIL_HOST, \
    EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER, PATH_FOR_AUDIO

from django.core.mail import send_mail, send_mass_mail

from web_app_auto_subs.utils.business_logic.subtitles1.start_whisper import StartWhisper
from web_app_auto_subs.progress_bar import _CustomProgressBar
from web_app_auto_subs.utils.business_logic.subtitles1.remove_all_helping_files import RemoveAllHelpingFiles
from web_app_auto_subs.utils.business_logic.subtitles1.handle_video import HandleVideo
from web_app_auto_subs.utils.services.make_srt import MakingSrt
from .utils.services.email.send_email import SendEmail


@app.task
def make_subs(video_pk: int,
              path_of_video: str,
              subs_language: str,
              make_audio_record: bool,
              size_of_model: str = 'tiny',
              language_for_model: str = 'en',) -> NoReturn:
    # try:
    #     command = f'cd {PATH_FOR_SUBTITLES} && whisper {path_of_video} --model {size_of_model} --language {language_for_model}'
    #     logger.info(f'Executing command: {command}')
    #     os.system(command)
    #     logger.info('Command executed successfully')
    # except Exception as e:
    #     logger.error(f'Error occurred: {e}')
    # try:
    #     import whisper.transcribe
    #     transcribe_module = sys.modules['whisper.transcribe']
    #     # model = whisper.load_model(size_of_model)
    #     # result = model.transcribe(path_of_video, language=language_for_model, fp16=False, verbose=None)
    #     import contextlib

        # @contextlib.contextmanager
        # def temporary_tqdm_replacement():
        #     original_tqdm = transcribe_module.tqdm.tqdm
        #     transcribe_module.tqdm.tqdm = _CustomProgressBar
        #     try:
        #         yield
        #     finally:
        #         transcribe_module.tqdm.tqdm = original_tqdm
        
        
    #     @contextlib.contextmanager
    #     def temporary_tqdm_replacement(video_pk):
    #         original_tqdm = transcribe_module.tqdm.tqdm
    #         transcribe_module.tqdm.tqdm = lambda *args, **kwargs: _CustomProgressBar(*args, video_pk=video_pk, **kwargs)
    #         try:
    #             yield
    #         finally:
    #             transcribe_module.tqdm.tqdm = original_tqdm

        
    #     with temporary_tqdm_replacement(video_pk):
    #         model = whisper.load_model(size_of_model)
    #         result = model.transcribe(path_of_video, language=language_for_model, fp16=False, verbose=None)

    #     print('whisper')
        

    # except Exception as e:
    #     logger.error(f'Error occurred: {e}')
    
    try:
        # import subprocess
        # import contextlib
        # import whisper.transcribe
        # import sys
        
        # from moviepy.editor import VideoFileClip


        # def run_whisper_command_with_progress(video_pk, path_of_video, size_of_model, language_for_model):
        #     command = f'cd {PATH_FOR_SUBTITLES} && whisper {path_of_video} --model {size_of_model} --language {language_for_model}'
            
        #     # Создание объекта VideoFileClip
        #     video_clip = VideoFileClip(path_of_video)

        #     # Получение продолжительности видео в секундах
        #     duration_in_seconds = video_clip.duration
        #     percentages = 0.0


        #     try:
        #         process = subprocess.Popen(
        #             command, 
        #             shell=True, 
        #             stdout=subprocess.PIPE, 
        #             stderr=subprocess.PIPE,
        #             text=True
        #         )

        #         # Считываем вывод процесса построчно и обновляем прогресс-бар
        #         for line in process.stdout:
        #             # print(line[0:25], end='')
                    
        #             # line[1:7]
        #             time_str = line[15:20]
        #             minutes, seconds = time_str.split(':')
        #             total_seconds = int(minutes) * 60 + int(seconds)
                    
        #             percentages = total_seconds * 100 / duration_in_seconds
        #             percentages = int(percentages)
                    
        #             if percentages > 100:
        #                 percentages = 100
                        
        #             with redis.Redis(host='localhost', port=6380, db=0) as r:
        #                 r.set(f'whisper_progress{video_pk}', percentages)
        #                 print('Progress of transcription process: ', int(r.get(f'whisper_progress{video_pk}')))
                    
        #             # print(percentages)


        #         process.wait()

        #         if process.returncode != 0:
        #             raise subprocess.CalledProcessError(process.returncode, command)

        #     except Exception as e:
        #         print(f"Error occurred: {e}")

        # # Пример вызова функции
        # run_whisper_command_with_progress(
        #     video_pk=video_pk,
        #     path_of_video=path_of_video,
        #     size_of_model=size_of_model,
        #     language_for_model=language_for_model
        # )
        
        StartWhisper().run(
            video_pk=video_pk, 
            path_of_video=path_of_video, 
            size_of_model=size_of_model, 
            language_for_model=language_for_model
        )
    
    except Exception as e:
        logger.error(f'Whisper error occurred: {e}')

   
    else:
        try:
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
            )
        
        except Exception as e:
            logger.error(f'Error occurred: {e}')
        
        else:
            for path in [PATH_FOR_AUDIO, PATH_FOR_SUBTITLES]: #, BASE_PATH_OF_VIDEO+'videos']:
                RemoveAllHelpingFiles.remove(
                    path=path, 
                    base_filename=name_of_video.split(".")[0]
                    )
    
    # for path in [PATH_FOR_AUDIO, PATH_FOR_SUBTITLES]:
    #             RemoveAllHelpingFiles.remove(
    #                 path=path, 
    #                 base_filename='test_wSZgBpx'
    #                 )
    
    


@app.task
def send_email(subject: str, message: str, to_email: list) -> NoReturn:
    send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        to_email,
    )



   # model = whisper.load_model(size_of_model,)
    # result = model.transcribe(
    #     path_of_video,
    #     language=language_for_model,
    #     fp16=False,
    #     verbose=None,
    #     )