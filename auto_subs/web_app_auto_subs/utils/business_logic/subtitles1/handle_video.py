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
        name_of_video, 
        path_for_video, 
        path_for_new_video,
        path_of_audio,
        path_with_str: str, 
        translate_var=None,
        
        ):
        
        try:
            mp4filename = name_of_video
            srtfilename = path_with_str + (name_of_video)[0:-4] + '.srt'

            subtitles = pysrt.open(srtfilename)
        
        except Exception as e:
            print('handle_video ', e)
        
        try:

            # MyGoogleTranslator().make_translate(subtitles, srtfilename)
            MyLocalTranslator().make_translate(subtitles, srtfilename)

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
        
            new_audio_filename, audio_clips = MakeAudioRecord().perform_audio_creation(
                subtitles=subtitles, 
                path_of_audio=path_of_audio,
                new_speed_for_audio=1.3, 
                new_volume_for_audio=6.0,
                )

        # try:
        #     PutSubs(mp4filename, srtfilename, path_for_video,
        #             path_for_new_video, new_audio_filename).generate_video_with_subtitles()
        # except Exception as e:
        #     print('PutSubs ', e)

        PutSubs(mp4filename, srtfilename, path_for_video,
                    path_for_new_video, new_audio_filename).generate_video_with_subtitles()
        

        if translate_var == 'True' or translate_var == True:
            for audio_clip in audio_clips:
                        audio_clip.close()
        

        

        
        
        # try:
        #     PutSubs(mp4filename, srtfilename, path_for_video,
        #             path_for_new_video, new_audio_filename).generate_video_with_subtitles()
            
        # except Exception as e:
        #     print('PutSubs ', e)
            

