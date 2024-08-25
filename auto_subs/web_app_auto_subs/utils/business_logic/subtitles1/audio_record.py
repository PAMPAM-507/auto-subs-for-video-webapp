from typing import NoReturn
import pysrt
import os

from gtts import gTTS
from abc import ABC, abstractmethod
from moviepy.editor import VideoFileClip, CompositeAudioClip, AudioFileClip
import moviepy.audio.fx.all as afx
from pydub import AudioSegment
import soundfile as sf


class MakeAudioRecordABC(ABC):

    @staticmethod
    def check_directory(directory: str):
        # os.makedirs(directory, exist_ok=True)
        pass

    @staticmethod
    def check_audio_clip_is_shorter_than_subtitle(audio_clip, duration, audio_file):
        if audio_clip.duration < duration:
            # print(f"Warning: Duration of audio file {audio_file} is shorter than the subtitle duration.")
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


    # @staticmethod
    # def change_audio_speed_without_distortion(
    #     audio_file, path_for_output_file: str, speed_factor: float=1.0,
    #     ) -> NoReturn:
    #     y, sr = librosa.load(audio_file)
    #     y_fast = librosa.effects.time_stretch(y, rate=speed_factor)
    #     sf.write(path_for_output_file, y_fast, sr)

    @staticmethod
    def change_audio_speed_without_distortion(
            audio_file: str,  
            path_for_output_file: str,
            speed_factor: float=1.0,
            ) -> NoReturn:
        
        sound = AudioSegment.from_file(audio_file)
        so = sound.speedup(speed_factor, 150, 25)
        so.export(path_for_output_file, format = 'mp3')


class MakeAudioRecord(MakeAudioRecordABC):

    def make_audio_for_each_subtitles(
            cls, subtitles: pysrt, path_of_audio: str, new_speed_for_audio: float=1.0, new_volume_for_audio: float=1.0
            ) -> CompositeAudioClip:

        # cls.check_directory(f'./{path_of_audio}/records')

        audio_clips = []

        for i, subtitle in enumerate(subtitles):
            start_time = cls.time_to_seconds(subtitle.start)
            end_time = cls.time_to_seconds(subtitle.end)
            duration = end_time - start_time
            text = subtitle.text

            # audio_file = f"./{path_of_audio}/records/audio_{i}.mp3"
            audio_file = f"{path_of_audio}records/audio_{i}.mp3"
            if cls.text_to_speech(text, audio_file):

                # modified_audio_file = f"./{path_of_audio}/records/modified_audio_{i}.mp3"
                modified_audio_file = f"{path_of_audio}records/modified_audio_{i}.mp3"
                
                cls.change_audio_speed_without_distortion(audio_file=audio_file, path_for_output_file=modified_audio_file, speed_factor=new_speed_for_audio,
                    )

                audio_clip = AudioFileClip(modified_audio_file)

                duration = cls.check_audio_clip_is_shorter_than_subtitle(audio_clip, duration, audio_file)
                
                audio_clip = audio_clip.set_start(start_time).set_duration(duration).volumex(new_volume_for_audio)


                audio_clips.append(audio_clip)

        return CompositeAudioClip(audio_clips), audio_clips

    def perform_audio_creation(
            cls, subtitles, path_of_audio: str, new_speed_for_audio: float=1, new_volume_for_audio: float=1
                               ) -> CompositeAudioClip:

        new_audio, audio_clips = cls.make_audio_for_each_subtitles(
            subtitles=subtitles, 
            path_of_audio=path_of_audio, 
            new_speed_for_audio=new_speed_for_audio, 
            new_volume_for_audio=new_volume_for_audio
            )

        return new_audio, audio_clips