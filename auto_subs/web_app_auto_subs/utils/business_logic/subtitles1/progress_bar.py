import os
import sys
import time
from typing import List, NoReturn, Union
import tqdm
import whisper
import datetime
import redis

from django.db.models.base import Model as Model

from web_app_auto_subs.models import UserVideos
from proglog import ProgressBarLogger
from .fuzzy_model.descriptor import Descriptor

class MyBarLogger(ProgressBarLogger):

    def __init__(self, video_pk: int):
        super().__init__()
        self.last_message = ''
        self.previous_percentage = 0
        self.video_pk = video_pk
        self.k = 0
        
    def __del__(self, ):
        with redis.Redis(host='localhost', port=6380, db=0) as r:
            r.delete(f'moviepy_progress{self.video_pk}')
        UserVideos.objects.filter(pk=self.video_pk).update(rendering_progress=100)

    def callback(self, **changes):
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            # print ('Parameter %s is now %s' % (parameter, value))
            self.last_message = value

    def bars_callback(self, bar, attr, value,old_value=None):
        # Every time the logger progress is updated, this function is called
        if 'Writing video' in self.last_message:
            percentage = (value / self.bars[bar]['total']) * 100
            if percentage > 0 and percentage < 100:
                if int(percentage) != self.previous_percentage:
                    self.previous_percentage = int(percentage)
                    self.k += 1
                    if self.k > 20:
                        with redis.Redis(host='localhost', port=6380, db=0) as r:
                            r.set(f'moviepy_progress{self.video_pk}', self.previous_percentage)
                            print('Rendering progress: ', int(r.get(f'moviepy_progress{self.video_pk}')))
                        self.k = 0


class CustomProgressBar():
    
    redis_client = Descriptor()
    variable_for_calculate_degrees = Descriptor()
    video_pk = Descriptor()
    redis_variable = Descriptor()
    
    def __init__(self, redis_client: redis.Redis, 
                 redis_variable: str, 
                 variable_for_calculate_degrees: int, 
                 video_pk: int) -> NoReturn:
        self.redis_client = redis_client
        self.variable_for_calculate_degrees = variable_for_calculate_degrees
        self.video_pk = video_pk
        self.redis_variable = redis_variable
    


    
        
        

        
    # def save_results_of_progress(self, counter: int, checking_counter: int) -> NoReturn:
        
    #     if checking_counter >= 10:
        
    #         percentages = self.calculate_percentages(counter, self.__variable_for_calculate_degrees)
            
    #         self.__redis.set(f'{self.self.__redis_variable}{self.__video_pk}', percentages)
    #         print(f'{self.__redis_variable}: ', int(self.redis.get(f'{self.__redis_variable}{self.__video_pk}')))
    #         checking_counter = 0
    
    @staticmethod
    def calculate_percentages(counter: int, variable_for_calculate_degrees: int) -> int:
        percentages = 0

        percentages = int(counter * 100 / variable_for_calculate_degrees)
            
        return percentages


class SaveResultsOfProgress():

    
    def save_to_redis(self, redis_client: redis.Redis, 
                      bar: CustomProgressBar, 
                      counter: int,
                      checking_counter: int) -> int:
        
        if checking_counter >= 10:
        
            percentages = self.calculate_percentages(counter, self.__variable_for_calculate_degrees)
            
            redis_client.set(f'{bar.redis_variable}{bar.video_pk}', percentages)
            print(f'{bar.redis_variable}: ', int(redis_client.get(f'{bar.redis_variable}{self.__video_pk}')))
            checking_counter = 0
            
            return checking_counter
        
        return checking_counter
    
    def save_to_bd_and_delete_from_redis(model: Model, bar: CustomProgressBar, redis_client: redis.Redis, ):
        redis_client.delete(f'voiceover_progress{bar.video_pk}')
        var = getattr(model, bar.redis_variable)
        model.objects.filter(pk=bar.video_pk).update(var=100, )
                    