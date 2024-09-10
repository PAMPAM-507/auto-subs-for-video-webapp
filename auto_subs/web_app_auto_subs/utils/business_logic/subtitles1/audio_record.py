from typing import IO, List, NoReturn, Tuple, Union
import pysrt
import os

from gtts import gTTS
from abc import ABC, abstractmethod
from moviepy.editor import VideoFileClip, CompositeAudioClip, AudioFileClip
from pydub import AudioSegment
import redis


from web_app_auto_subs.utils.business_logic.subtitles1.progress_bar import CustomProgressBar
from web_app_auto_subs.models import UserVideos
from web_app_auto_subs.utils.business_logic.subtitles1.parse_str_time_to_soconds import ParseStrTimeToSeconds
from .fuzzy_model.model import FuzzyModel
from .fuzzy_model.defuzzification import DefuzzificationByHeightMethod
from .fuzzy_model.fazzification import SolveInputValueForModelWithTwoParameters
from .fuzzy_model.rule_base import MakeRuleBaseForAudioRecords


class MakeAudioRecordABC(ABC):

    @staticmethod
    def check_audio_clip_is_shorter_than_subtitle(audio_clip, duration, audio_file):
        if audio_clip.duration < duration:
            duration = audio_clip.duration

        return duration

    @staticmethod
    def text_to_speech(text, output_file, lang:str ='ru'):
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(output_file)
            return True
        
        except AssertionError:
            return None

    @staticmethod
    def time_to_seconds(t):
        return t.hours * 3600 + t.minutes * 60 + t.seconds + t.milliseconds / 1000
    
    @staticmethod
    def close_audio_files(audio_clips):
        for audio_clip in audio_clips:
            audio_clip.close()

    @staticmethod
    def change_audio_speed(audio_file, speed=1.0):
        sound = AudioSegment.from_file(audio_file)
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

    @staticmethod
    def change_audio_speed_without_distortion(
            audio_file: str,  
            path_for_output_file: str,
            speed_factor: float=1.0,
            ) -> NoReturn:
        
        sound = AudioSegment.from_file(audio_file)
        so = sound.speedup(speed_factor, 150, 25)
        so.export(path_for_output_file, format = 'mp3')
    
    
    @classmethod
    def calculate_height_for_audio_record(self, amount_of_words: int, time_range: float) -> Tuple[str, Union[int, float]]:
        result = SolveInputValueForModelWithTwoParameters.solve_input_value(self.model, amount_of_words, time_range)

        result = MakeRuleBaseForAudioRecords.make_rule_base(result[0][0], result[0][1], result[0][2], result[1][0], result[1][1], result[1][2],)

        result = DefuzzificationByHeightMethod.get_resulting_value(result, self.model.border_for_output_term)
        
        return result
    
    
    def reduce_audio_volume(input_video_path, volume_factor):
        """
        Уменьшает громкость аудио в видео и возвращает аудиоклип.

        :param input_video_path: Путь к исходному видеофайлу
        :param volume_factor: Коэффициент уменьшения громкости (0.0 - 1.0)
        :return: Аудиоклип с изменённой громкостью
        """
        # Загрузка видео
        clip = VideoFileClip(input_video_path)

        # Изменение громкости аудио
        audio_with_reduced_volume = clip.audio.volumex(volume_factor)

        return audio_with_reduced_volume


from moviepy.editor import AudioFileClip, CompositeAudioClip

class MakeAudioRecord(MakeAudioRecordABC):
    
    model = FuzzyModel(
        border_for_first_term=[0, 8, 16], 
        border_for_second_term=[1, 4, 7],
        border_for_output_term = [1.4, 1.6, 1.8],
    )
    
    

    def make_audio_for_each_subtitles(
            self, video_pk: int, subtitles: pysrt.SubRipFile, base_filename: str, path_of_audio: str, 
            new_volume_for_audio: float=1.0, 
            ) -> Tuple[CompositeAudioClip, List[IO]]:
        
        redis_client = redis.Redis(host='localhost', port=6380, db=0)
        
        audio_clips = []
        
        subtitles_len = len(subtitles)
        k = 0
        checking_counter = 0

        for i, subtitle in enumerate(subtitles):
            start_time = self.time_to_seconds(subtitle.start)
            end_time = self.time_to_seconds(subtitle.end)
            duration = end_time - start_time
            text = subtitle.text

            audio_file = f"{path_of_audio}/{base_filename}.{i}.mp3"
            if self.text_to_speech(text, audio_file):
                
                k += 1
                checking_counter += 1
                if checking_counter >= 10:
                    
                    percentages = int(k * 100 / subtitles_len)
                    
                    redis_client.set(f'voiceover_progress{video_pk}', percentages)
                    print('voiceover progress: ', int(redis_client.get(f'voiceover_progress{video_pk}')))
                    checking_counter = 0
                

                modified_audio_file = f"{path_of_audio}/{base_filename}.modified.{i}.mp3"
                
                model_value = 1.2

                try:
                    model_value = self.calculate_height_for_audio_record(
                        len(str(subtitle).split('\n')[2].split(' ')),
                        ParseStrTimeToSeconds.calculate_total_seconds(str(subtitle).split('\n')[1]), 
                    )[1]
                
                except Exception as e:
                    print('calculate_height_for_audio_record ', e)
                
                self.change_audio_speed_without_distortion(
                    audio_file=audio_file, 
                    path_for_output_file=modified_audio_file, 
                    speed_factor=model_value,
                )

                audio_clip = AudioFileClip(modified_audio_file)

                duration = self.check_audio_clip_is_shorter_than_subtitle(audio_clip, duration, audio_file)
                
                audio_clip = audio_clip.set_start(start_time).set_duration(duration).volumex(new_volume_for_audio)

                audio_clips.append(audio_clip)
        
        redis_client.delete(f'voiceover_progress{video_pk}')
        UserVideos.objects.filter(pk=video_pk).update(voiceover_progress=100)

        redis_client.close()
            
        return CompositeAudioClip(audio_clips), audio_clips

    # def perform_audio_creation(
    #         self, subtitles, base_filename, path_of_audio: str, new_speed_for_audio: float=1, new_volume_for_audio: float=1
    #                            ) -> tuple[CompositeAudioClip, List[IO]]:

    #     new_audio, audio_clips = self.make_audio_for_each_subtitles(
    #         subtitles=subtitles,
    #         base_filename=base_filename,
    #         path_of_audio=path_of_audio, 
    #         new_speed_for_audio=new_speed_for_audio, 
    #         new_volume_for_audio=new_volume_for_audio
    #         )

    #     return new_audio, audio_clips