import sys
from abc import ABC, abstractmethod

import tqdm
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip


from web_app_auto_subs.progress_bar import _CustomProgressBar, logger
from .make_subs import MakeSubs






class PutSubsABC(ABC):
    pass


class PutSubs(PutSubsABC):

    def __init__(self, mp4filename: str, srtfilename: str, path_for_video: str, path_for_new_video: str, new_audio_filename: str=None):
        self.__begin, self.__end = mp4filename.split(".mp4")
        self.__video = VideoFileClip(path_for_video)
        self.__subtitles = pysrt.open(srtfilename)
        self.__output_video_file = (self.__begin + '_subtitled' + ".mp4")
        self.path_for_new_video = str(path_for_new_video)
        self.__new_audio = new_audio_filename
        self.__old_audio = self.__video.audio
        

    @staticmethod
    def __create_subtitle_clips(subtitles, video):
        return MakeSubs().create_subtitle_clips(subtitles, video.size)

    @staticmethod
    def __make_final_video(video, subtitle_clips, old_audio, new_audio=None, ):
        if new_audio:
            final_audio = CompositeAudioClip([old_audio, new_audio])
            video = video.set_audio(final_audio)

        return CompositeVideoClip([video] + subtitle_clips)
    
    @staticmethod
    def __save_final_video(final_video, output_video_file, path_for_new_video):
        final_video.write_videofile(f'{path_for_new_video}/{output_video_file}', 
                                    logger=logger)

    def generate_video_with_subtitles(self):
        self.__save_final_video(
            self.__make_final_video(
            video=self.__video, subtitle_clips=self.__create_subtitle_clips(
                self.__subtitles, self.__video,
                ), 
            old_audio=self.__old_audio, new_audio=self.__new_audio
        ), self.__output_video_file, self.path_for_new_video
        )
        
        



# import sys
# from abc import ABC, abstractmethod

# import tqdm
# import pysrt
# from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip

# from web_app_auto_subs.progress_bar import _CustomProgressBar, _CustomProgressBar2
# from .make_subs import MakeSubs


# class PutSubsABC(ABC):
#     pass


# class PutSubs(PutSubsABC):

#     def __init__(self, mp4filename: str, srtfilename: str, path_for_video: str, path_for_new_video: str, new_audio_filename: str = None):
#         self.__begin, self.__end = mp4filename.split(".mp4")
#         self.__video = VideoFileClip(path_for_video)
#         self.__subtitles = pysrt.open(srtfilename)
#         self.__output_video_file = (self.__begin + '_subtitled' + ".mp4")
#         self.path_for_new_video = str(path_for_new_video)
#         self.__new_audio = new_audio_filename
#         self.__old_audio = self.__video.audio

#     @staticmethod
#     def __create_subtitle_clips(subtitles, video):
#         return MakeSubs().create_subtitle_clips(subtitles, video.size)

#     @staticmethod
#     def __make_final_video(video, subtitle_clips, old_audio, new_audio=None):
#         if new_audio:
#             final_audio = CompositeAudioClip([old_audio, new_audio])
#             video = video.set_audio(final_audio)

#         return CompositeVideoClip([video] + subtitle_clips)

#     @staticmethod    
#     def custom_write_videofile(clip, filename, *args, **kwargs):
#         # Заменяем стандартный tqdm на кастомный
#         original_tqdm = tqdm.tqdm
#         progress_bar = _CustomProgressBar2(total=clip.duration)  # Установите total на нужное значение
#         tqdm.tqdm = progress_bar

#         try:
#             # Метод write_videofile теперь должен использовать кастомный tqdm
#             clip.write_videofile(filename, *args, **kwargs)
#         finally:
#             tqdm.tqdm = original_tqdm
#             progress_bar.close()
        
#         return progress_bar


#     def __save_final_video(self, final_video, output_video_file, path_for_new_video):
#         full_output_path = f'{path_for_new_video}/{output_video_file}'
#         # Получите кастомный прогресс-бар
#         progress_bar = PutSubs.custom_write_videofile(final_video, full_output_path, fps=24, codec='libx264', audio_codec='aac', threads=4)
#         # Получите прогресс
#         current, total = progress_bar.get_progress()
#         print(f"Final Progress: {current}/{total}")

#     def generate_video_with_subtitles(self):
#         final_video = self.__make_final_video(
#             video=self.__video,
#             subtitle_clips=self.__create_subtitle_clips(self.__subtitles, self.__video),
#             old_audio=self.__old_audio,
#             new_audio=self.__new_audio
#         )
#         self.__save_final_video(final_video, self.__output_video_file, self.path_for_new_video)