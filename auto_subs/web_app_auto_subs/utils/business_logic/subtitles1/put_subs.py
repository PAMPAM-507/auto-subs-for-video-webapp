import sys
from abc import ABC, abstractmethod
from .make_subs import MakeSubs

import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip


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
        final_video.write_videofile(f'{path_for_new_video}/{output_video_file}')

    def generate_video_with_subtitles(self):
        self.__save_final_video(
            self.__make_final_video(
            video=self.__video, subtitle_clips=self.__create_subtitle_clips(
                self.__subtitles, self.__video,
                ), 
            old_audio=self.__old_audio, new_audio=self.__new_audio
        ), self.__output_video_file, self.path_for_new_video
        )
