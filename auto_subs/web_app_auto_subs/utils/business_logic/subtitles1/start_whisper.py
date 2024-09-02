import subprocess
import contextlib
import sys
import os
from typing import NoReturn

import redis
import whisper.transcribe
from moviepy.editor import VideoFileClip

from auto_subs.settings import PATH_FOR_SUBTITLES
from auto_subs.settings import logger


class StartWhisper():
    
    @staticmethod
    def calculate_percentages(total_seconds: int, duration_in_seconds: int) -> int:
        """Method to calculate percentage by duration in seconds=100% and total_seconds - 
        amount of seconds which were executed
        """
        
        try:
            percentages = total_seconds * 100 / duration_in_seconds
        except ZeroDivisionError as e:
            logger.error(f'Error occurred: {e}')
        except TypeError as e:
            logger.error(f'Error occurred: {e}')
        except Exception as e:
            logger.error(f'Error occurred: {e}')
        
        percentages = int(percentages)
        
        if percentages > 100:
            percentages = 100
        
        return percentages
    
    
    @staticmethod
    def parse_str_time_to_seconds(time_str: str) -> int:
        """Method parse time string to seconds

        Args:
            time_str (str): [00:04]

        Returns:
           int: 4
        """
        
        try: 
            minutes, seconds = time_str.split(':')
        except ValueError:
            logger.error(f'Error occurred: {e}')
        except Exception as e:
            logger.error(f'Error occurred: {e}')
        
        else:
            try:
                result = int(minutes) * 60 + int(seconds)
            except ValueError:
                logger.error(f'Error occurred: {e}')
            except Exception as e:
                logger.error(f'Error occurred: {e}')
            
        return result
        
        
    
    
    def run(self, video_pk: int, path_of_video: str, size_of_model: str, language_for_model: str) -> NoReturn:
        """Method run whisper process

        Args:
            video_pk (int): video pk
            path_of_video (str): full path of video
            size_of_model (str): tiny
            language_for_model (str): en, ru, etc

        """
        
        if not os.path.exists(path_of_video):
            logger.info(f'Error occurred: video file does not exist')
            raise FileExistsError('Video file does not exist')
        
        command = f'cd {PATH_FOR_SUBTITLES} && whisper {path_of_video} --model {size_of_model} --language {language_for_model}'
        
        duration_in_seconds = VideoFileClip(path_of_video).duration
        
        try:
                process = subprocess.Popen(
                    command, 
                    shell=True, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                for line in process.stdout:

                    total_seconds = self.parse_str_time_to_seconds(time_str=line[15:20])
                    
                    percentages = self.calculate_percentages(total_seconds, duration_in_seconds)
                    
                    
                    with redis.Redis(host='localhost', port=6380, db=0) as r:
                        r.set(f'whisper_progress{video_pk}', percentages)
                        print('Progress of transcription process: ', int(r.get(f'whisper_progress{video_pk}')))

                process.wait()

                if process.returncode != 0:
                    raise subprocess.CalledProcessError(process.returncode, command)
                
                with redis.Redis(host='localhost', port=6380, db=0) as r:
                    percentages = int(r.get(f'whisper_progress{video_pk}'))
                    if percentages < 100:
                        percentages = 100
                        r.set(f'whisper_progress{video_pk}', percentages)

        except Exception as e:
            logger.error(f'Error occurred: {e}')