import sys
from abc import ABC, abstractmethod
from typing import Tuple

import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from .fuzzy_model.model import FuzzyModel
from .fuzzy_model.defuzzification import DefuzzificationByHeightMethod
from .fuzzy_model.fazzification import SolveInputValueForModelWithTwoParameters
from .fuzzy_model.rule_base import MakeRuleBase

class MakeSubsABC(ABC):

    @abstractmethod
    def create_subtitle_clips(self, subtitles, video_size, font_size=24, font='Arial', color='white', debug=False):
        pass

    @abstractmethod
    def calculate_height_for_subtitle(cls, amount_of_words, amount_of_pixels):
        pass

    @staticmethod
    def time_to_seconds(time_obj):
        return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000
    
    @staticmethod
    def choice_height_for_subtitle(model_value):

        if model_value == 'C2':
            return 3.5 / 5
        
        elif model_value == 'C3':
            return 3 / 5
        
        return 4 / 5
    
    @staticmethod
    def choice_font_size(model_value):

        if model_value == 'C2':
            return 18
        
        elif model_value == 'C3':
            return 14
        
        return 24


class MakeSubs(MakeSubsABC):

    model = FuzzyModel(
        border_for_first_term=[0, 22, 44], 
        border_for_second_term=[0, 777600, 2457600],
        border_for_output_term = [0, 0.5, 1] 
        )
    
    @classmethod
    def calculate_height_for_subtitle(cls, amount_of_words, amount_of_pixels) -> Tuple:
        result = SolveInputValueForModelWithTwoParameters.solve_input_value(cls.model, amount_of_words, amount_of_pixels)

        result = MakeRuleBase.make_rule_base(result[0][0], result[0][1], result[0][2], result[1][0], result[1][1], result[1][2],)

        result = DefuzzificationByHeightMethod.get_resulting_value(result, cls.model.border_for_output_term)
        
        return result

    def create_subtitle_clips(self, subtitles, video_size, font_size=24, font='Arial', color='white', debug=False):

        amount_of_pixels = video_size[0] * video_size[1]

        subtitle_clips = []

        model_value = 'C1'

        for subtitle in subtitles:
            start_time = self.time_to_seconds(subtitle.start)
            end_time = self.time_to_seconds(subtitle.end)
            duration = end_time - start_time

            # print(len(str(subtitle).split('\n')[2].split(' ')))
            # print(str(subtitle).split('\n')[2].split(' '))
            # print(video_size)
            # print(len(str(subtitle).split('\n')[2]))
            try:
                model_value = self.calculate_height_for_subtitle(len(str(subtitle).split('\n')[2].split(' ')), amount_of_pixels)[0]
            except Exception as e:
                print('calculate_height_for_subtitle ', e)
            
            # print('model_value: ', model_value, '\nsize_of_text: ', len(str(subtitle).split('\n')[2].split(' ')), '\namount_of_pixels: ', amount_of_pixels, '\n')

            video_width, video_height = video_size

            text_clip = TextClip(subtitle.text, fontsize=self.choice_font_size(model_value), font=font, color=color, bg_color='transparent',
                                 size=(video_width * 3 / 4, None), method='caption').set_start(start_time).set_duration(
                duration)
            
            subtitle_x_position = 'center'
            subtitle_y_position = video_height * self.choice_height_for_subtitle(model_value)

            text_position = (subtitle_x_position, subtitle_y_position)
            subtitle_clips.append(text_clip.set_position(text_position))

        return subtitle_clips
    
    

