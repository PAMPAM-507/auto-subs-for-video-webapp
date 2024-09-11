
from typing import NoReturn, Union
import pysrt
import os
import sys


from .put_subs import PutSubs
from .my_translator import MyGoogleTranslator, MyLocalTranslator
from .audio_record import MakeAudioRecord

# class HandleVideo():

#     @staticmethod
#     def handle_video(name_of_video, path_for_video, path_for_new_video):
#         try:
#             mp4filename = name_of_video
#             srtfilename = os.environ.get('PROJECT_ROOT') + \
#                 '/bin/' + (name_of_video)[0:-4] + '.srt'

#             subtitles = pysrt.open(srtfilename)
            
#             # MyGoogleTranslator().make_translate(subtitles, srtfilename)
#             MyLocalTranslator().make_translate(subtitles, srtfilename)
#             PutSubs(mp4filename, srtfilename, path_for_video,
#                     path_for_new_video).generate_video_with_subtitles()
            
#         except Exception as e:
#             print('handle_video ', e)

class HandleVideo():

    @staticmethod
    def handle_video(
        video_pk: int,
        name_of_video: str, 
        path_for_video: str, 
        path_for_new_video: str,
        path_of_audio: str,
        path_with_str: str, 
        translate_var: Union[bool, str] =None,
        src_language='en', 
        dest_language='ru',
        ) -> NoReturn:
        
        
        
        try:
            mp4filename = name_of_video
            srtfilename = path_with_str + (name_of_video)[0:-4] + '.srt'

            subtitles = pysrt.open(srtfilename)
        
        except Exception as e:
            print('handle_video ', e)
        
        try:

            

            MyGoogleTranslator().make_translate(subtitles, 
                                                srtfilename, 
                                                video_pk, 
                                                src_language=src_language, 
                                                dest_language=dest_language,)
            # MyLocalTranslator().make_translate(subtitles, srtfilename)

        except Exception as e:
            print('MyLocalTranslator ', e)

        new_audio_filename = None
        if translate_var == 'True' or translate_var == True:

            # try:
            #     new_audio_filename, audio_clips = MakeAudioRecord().perform_audio_creation(
            #          subtitles=subtitles, path_of_audio='bin', new_speed_for_audio=1.4, new_volume_for_audio=6.0,
            #          )

            # except Exception as e:
            #     print('MakeAudioRecord ', e)
        
            # new_audio_filename, audio_clips = MakeAudioRecord().perform_audio_creation(
            #     subtitles=subtitles,
            #     base_filename=name_of_video.split(".")[0],
            #     path_of_audio=path_of_audio,
            #     new_speed_for_audio=1.5, 
            #     new_volume_for_audio=6.0,
            #     )
            
            new_audio_filename, audio_clips = MakeAudioRecord().make_audio_for_each_subtitles(
                video_pk=video_pk,
                subtitles=subtitles, 
                base_filename=name_of_video.split(".")[0], 
                path_of_audio=path_of_audio, 
                new_volume_for_audio=6.0,)


        # try:
        #     PutSubs(mp4filename, srtfilename, path_for_video,
        #             path_for_new_video, new_audio_filename).generate_video_with_subtitles()
        # except Exception as e:
        #     print('PutSubs ', e)
        
        # import contextlib
        
        # import moviepy
        
        # from web_app_auto_subs.progress_bar import _CustomProgressBar
        
        # @contextlib.contextmanager
        # def temporary_tqdm_replacement():
        #     original_tqdm = moviepy.video.io.ffmpeg_tools.tqdm
        #     moviepy.video.io.ffmpeg_tools.tqdm = _CustomProgressBar
        #     try:
        #         yield
        #     finally:
        #         moviepy.video.io.ffmpeg_tools.tqdm = original_tqdm

        # with temporary_tqdm_replacement():
        PutSubs(mp4filename, srtfilename, video_pk, path_for_video,
                    path_for_new_video, new_audio_filename).generate_video_with_subtitles()
        

        if translate_var == 'True' or translate_var == True:
            for audio_clip in audio_clips:
                        audio_clip.close()
        

        

        
        
        # try:
        #     PutSubs(mp4filename, srtfilename, path_for_video,
        #             path_for_new_video, new_audio_filename).generate_video_with_subtitles()
            
        # except Exception as e:
        #     print('PutSubs ', e)
            

