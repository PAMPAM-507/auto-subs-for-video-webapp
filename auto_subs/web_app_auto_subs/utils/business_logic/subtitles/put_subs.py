import sys
from abc import ABC, abstractmethod
from .make_subs import MakeSubs

import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os


class PutSubsABC(ABC):
    pass


class PutSubs(PutSubsABC):

    def __init__(self, mp4filename: str, srtfilename: str, path_to_save: str, name_of_video: str):
        self.__video = VideoFileClip(mp4filename)
        self.__subtitles = pysrt.open(srtfilename)
        self.__output_video_file = (name_of_video + '_subtitled' + ".mp4")
        self.__path_to_save = path_to_save
        # self.output_video_file = self.output_video_file[8:]

    # Create subtitle clips
    @staticmethod
    def __create_subtitle_clips(subtitles, video):
        return MakeSubs().create_subtitle_clips(subtitles, video.size)

    # Add subtitles to the video
    @staticmethod
    def __make_final_video(video, subtitle_clips):
        return CompositeVideoClip([video] + subtitle_clips)

    @staticmethod
    def __save_final_video(final_video, output_video_file, path_to_save):
        final_video.write_videofile(f'./media/video_with_subs/{output_video_file}')

    def generate_video_with_subtitles(self):
        self.__save_final_video(
            self.__make_final_video(
                self.__video,
                self.__create_subtitle_clips(self.__subtitles, self.__video)
            ), self.__output_video_file, self.__path_to_save
        )
