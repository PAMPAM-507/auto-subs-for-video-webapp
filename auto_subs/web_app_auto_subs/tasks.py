import os
import sys
from typing import NoReturn

import whisper.transcribe
from celery import shared_task
from auto_subs.celery import app

from auto_subs.settings import BASE_DIR, BASE_PATH_OF_VIDEO, PATH_FOR_SUBTITLES, PATH_FOR_VIDEO_WITH_SUBS, EMAIL_HOST_PASSWORD, EMAIL_HOST, \
    EMAIL_BACKEND, EMAIL_PORT, \
    EMAIL_USE_TLS, EMAIL_HOST_USER, PATH_FOR_AUDIO

from django.core.mail import send_mail, send_mass_mail

from web_app_auto_subs.progress_bar import _CustomProgressBar
from web_app_auto_subs.utils.business_logic.subtitles1.remove_all_helping_files import RemoveAllHelpingFiles
from web_app_auto_subs.utils.business_logic.subtitles1.handle_video import HandleVideo
from web_app_auto_subs.utils.services.make_srt import MakingSrt
from .utils.services.email.send_email import SendEmail


import os
import logging

logger = logging.getLogger('main')


@app.task
def make_subs(video_id: int,
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
    try:
        import whisper.transcribe
        transcribe_module = sys.modules['whisper.transcribe']
        # model = whisper.load_model(size_of_model)
        # result = model.transcribe(path_of_video, language=language_for_model, fp16=False, verbose=None)
        import contextlib

        # @contextlib.contextmanager
        # def temporary_tqdm_replacement():
        #     original_tqdm = transcribe_module.tqdm.tqdm
        #     transcribe_module.tqdm.tqdm = _CustomProgressBar
        #     try:
        #         yield
        #     finally:
        #         transcribe_module.tqdm.tqdm = original_tqdm
        
        
        @contextlib.contextmanager
        def temporary_tqdm_replacement(video_id):
            original_tqdm = transcribe_module.tqdm.tqdm
            transcribe_module.tqdm.tqdm = lambda *args, **kwargs: _CustomProgressBar(*args, video_id=video_id, **kwargs)
            try:
                yield
            finally:
                transcribe_module.tqdm.tqdm = original_tqdm

        with temporary_tqdm_replacement(video_id):
            model = whisper.load_model(size_of_model)
            result = model.transcribe(path_of_video, language=language_for_model, fp16=False, verbose=None)

        

    except Exception as e:
        logger.error(f'Error occurred: {e}')
 

    
    else:
        try:
            srt_filepath = PATH_FOR_SUBTITLES + path_of_video.split('/')[-1][:-3] + 'srt'
            MakingSrt.write_srt(result, srt_filepath)
            
            name_of_video = path_of_video.split("/")[-1]
            
            HandleVideo.handle_video(
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