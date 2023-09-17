import sys
from abc import ABC, abstractmethod

import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os


class MakeSubsABC(ABC):

    @abstractmethod
    def create_subtitle_clips(self, subtitles, video_size, font_size=24, font='Arial', color='white', debug=False):
        pass

    @staticmethod
    def time_to_seconds(time_obj):
        return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000


class MakeSubs(MakeSubsABC):

    def create_subtitle_clips(self, subtitles, video_size, font_size=24, font='Arial', color='white', debug=False):
        subtitle_clips = []

        for subtitle in subtitles:
            start_time = self.time_to_seconds(subtitle.start)
            end_time = self.time_to_seconds(subtitle.end)
            duration = end_time - start_time

            video_width, video_height = video_size

            text_clip = TextClip(subtitle.text, fontsize=font_size, font=font, color=color, bg_color='transparent',
                                 size=(video_width * 3 / 4, None), method='caption').set_start(start_time).set_duration(
                duration)

            subtitle_x_position = 'center'
            subtitle_y_position = video_height * 4 / 5

            text_position = (subtitle_x_position, subtitle_y_position)
            subtitle_clips.append(text_clip.set_position(text_position))

        return subtitle_clips



