
from typing import NoReturn, Union
import pysrt
import os
import sys

import redis
from moviepy.editor import CompositeAudioClip

from auto_subs.settings import logger, REDIS_HOST, REDIS_PORT
from .open_file_with_subtitles import PysrtFileParser
from .put_subs import PutSubs
from .my_translator import MakeTranslating, GoogleTranslator
from .audio_record import MakeAudioRecord
from .progress_bar import MyBarLogger, RedisProgressValue, DjangoORMProgressValue
from web_app_auto_subs.models import UserVideos



class HandleVideo():

    @staticmethod
    def handle_video(
        video_pk: int,
        name_of_video: str,
        path_for_video: str,
        path_for_new_video: str,
        path_of_audio: str,
        path_with_str: str,
        translate_var: Union[bool, str] = None,
        src_language='en',
        dest_language='ru',
    ) -> NoReturn:

        try:
            mp4filename = name_of_video
            srtfilename = path_with_str + (name_of_video)[0:-4] + '.srt'
            
            subtitles = PysrtFileParser(srtfilename)

            # subtitles = pysrt.open(srtfilename)

        except Exception as e:
            logger.error(f'try to pysrt.open(srtfilename) in handle_video, error occurred: {e}')


        try:

            MakeTranslating(
                translator=GoogleTranslator(),
                saver_progress_results=DjangoORMProgressValue(
                    model=UserVideos,
                    attribute='translate_progress')
            ).execute(subtitles,
                        srtfilename,
                        video_pk,
                        progress_value=RedisProgressValue(
                            redis_client=redis.Redis(host=REDIS_HOST, 
                                                     port=REDIS_PORT, 
                                                     db=0)),
                        src_language=src_language,
                        dest_language=dest_language,)


        except Exception as e:
            logger.error(f'try to MakeTranslating(...).execute(...) in handle_video, error occurred: {e}')

        new_audio_filename = None
        if translate_var == 'True' or translate_var == True:
            
            try:
                audio_clips = MakeAudioRecord().make_audio_for_each_subtitles(
                    video_pk=video_pk,
                    subtitles=subtitles,
                    base_filename=name_of_video.split(".")[0],
                    path_of_audio=path_of_audio,
                    progress_value=RedisProgressValue(
                        redis_client=redis.Redis(host=REDIS_HOST, 
                                                 port=REDIS_PORT, 
                                                 db=0)),

                    saver_progress_results=DjangoORMProgressValue(
                        model=UserVideos,
                        attribute='voiceover_progress'),

                    new_volume_for_audio=6.0,)
                
                new_audio_filename = CompositeAudioClip(audio_clips)
                
            except Exception as e:
                logger.error(f'try to MakeAudioRecord().make_audio_for_each_subtitles(...) in handle_video, error occurred: {e}')
        
        try:
            PutSubs(mp4filename,
                    srtfilename,
                    video_pk,
                    path_for_video,
                    path_for_new_video,
                    MyBarLogger(video_pk=video_pk,
                                write_progress_value=RedisProgressValue(
                                    redis_client=redis.Redis(host=REDIS_HOST, 
                                                             port=REDIS_PORT, 
                                                             db=0)),
                                saver_progress_results=DjangoORMProgressValue(
                                    model=UserVideos,
                                    attribute='rendering_progress'),),
                    new_audio_filename=new_audio_filename).generate_video_with_subtitles()
        except Exception as e:
            logger.error(f'try to PutSubs(...).generate_video_with_subtitles() in handle_video, error occurred: {e}')
                
        if translate_var == 'True' or translate_var == True:
            for audio_clip in audio_clips:
                audio_clip.close()
                
                
