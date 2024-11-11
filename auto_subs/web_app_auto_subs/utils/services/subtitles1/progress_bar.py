from abc import ABC, abstractmethod
import os
import sys
import time
from typing import List, None, Union
import tqdm
import whisper
import datetime
import redis

from django.db.models.base import Model as Model

from web_app_auto_subs.models import UserVideos
from proglog import ProgressBarLogger
from .fuzzy_model.descriptor import Descriptor


class IProgressValue(ABC):
    
    @abstractmethod
    def get_progress_value(self, key: str|int) -> Union[int, float]:
        pass
    
    @abstractmethod
    def delete_progress_value(self, key: str|int) -> None:
        pass
    
    @abstractmethod
    def set_progress_value(self, key: str|int, value: Union[int, float]) -> None:
        pass
    
    @abstractmethod
    def close(self,) -> None:
        pass


from typing import Union, None
from django.db.models import Model

class DjangoORMProgressValue(IProgressValue):
    
    def __init__(self, model: Model, attribute: str):
        self.model = model
        self.attribute = attribute
    
    def get_progress_value(self, key: str | int):
        obj = self.model.objects.get(pk=key)
        return getattr(obj, self.attribute)

    def delete_progress_value(self, key: str | int) -> None:
        pass
    
    def set_progress_value(self, key: str | int, value: Union[int, float]) -> None:
        self.model.objects.filter(pk=key).update(**{self.attribute: value})
    
    def close(self) -> None:
        pass


class RedisProgressValue(IProgressValue):
    
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
    
    def get_progress_value(self, key: str|int) -> Union[int, float]:
        return self.redis_client.get(key)
    
    def delete_progress_value(self, key: str|int) -> None:
        self.redis_client.delete(key)
    
    def set_progress_value(self, key: str|int, value: Union[int, float]) -> None:
        self.redis_client.set(key, value)
    
    def close(self):
        self.redis_client.close()


class MyBarLogger(ProgressBarLogger):

    def __init__(self, video_pk: int, 
                 write_progress_value: IProgressValue,
                 saver_progress_results: IProgressValue,):
        super().__init__()
        self.last_message = ''
        self.previous_percentage = 0
        self.video_pk = video_pk
        self.k = 0
        self.write_progress_value = write_progress_value
        self.saver_progress_results = saver_progress_results
        
    def __del__(self, ):
        self.write_progress_value.delete_progress_value(f'moviepy_progress{self.video_pk}')
        self.write_progress_value.close()
        
        # with redis.Redis(host='localhost', port=6380, db=0) as r:
        #     r.delete(f'moviepy_progress{self.video_pk}')
        # UserVideos.objects.filter(pk=self.video_pk).update(rendering_progress=100)
        self.saver_progress_results.set_progress_value(key=self.video_pk, value=100)

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
                        # with redis.Redis(host='localhost', port=6380, db=0) as r:
                        #     r.set(f'moviepy_progress{self.video_pk}', self.previous_percentage)
                        #     print('Rendering progress: ', int(r.get(f'moviepy_progress{self.video_pk}')))
                        
                        self.write_progress_value.set_progress_value(f'moviepy_progress{self.video_pk}', self.previous_percentage)
                        print('Rendering progress: ', int(self.write_progress_value.get_progress_value(f'moviepy_progress{self.video_pk}')))
                        self.k = 0


# class CustomProgressBar():
    
#     redis_client = Descriptor()
#     variable_for_calculate_degrees = Descriptor()
#     video_pk = Descriptor()
#     redis_variable = Descriptor()
    
#     def __init__(self, redis_client: redis.Redis, 
#                  redis_variable: str, 
#                  variable_for_calculate_degrees: int, 
#                  video_pk: int) -> None:
#         self.redis_client = redis_client
#         self.variable_for_calculate_degrees = variable_for_calculate_degrees
#         self.video_pk = video_pk
#         self.redis_variable = redis_variable
    


    
        
        

        
    # def save_results_of_progress(self, counter: int, checking_counter: int) -> None:
        
    #     if checking_counter >= 10:
        
    #         percentages = self.calculate_percentages(counter, self.__variable_for_calculate_degrees)
            
    #         self.__redis.set(f'{self.self.__redis_variable}{self.__video_pk}', percentages)
    #         print(f'{self.__redis_variable}: ', int(self.redis.get(f'{self.__redis_variable}{self.__video_pk}')))
    #         checking_counter = 0
    
    # @staticmethod
    # def calculate_percentages(counter: int, variable_for_calculate_degrees: int) -> int:
    #     percentages = 0

    #     percentages = int(counter * 100 / variable_for_calculate_degrees)
            
    #     return percentages


# class SaveResultsOfProgress():

    
#     def save_to_redis(self, redis_client: redis.Redis, 
#                       bar: CustomProgressBar, 
#                       counter: int,
#                       checking_counter: int) -> int:
        
#         if checking_counter >= 10:
        
#             percentages = self.calculate_percentages(counter, self.__variable_for_calculate_degrees)
            
#             redis_client.set(f'{bar.redis_variable}{bar.video_pk}', percentages)
#             print(f'{bar.redis_variable}: ', int(redis_client.get(f'{bar.redis_variable}{self.__video_pk}')))
#             checking_counter = 0
            
#             return checking_counter
        
#         return checking_counter
    
#     def save_to_bd_and_delete_from_redis(model: Model, bar: CustomProgressBar, redis_client: redis.Redis, ):
#         redis_client.delete(f'voiceover_progress{bar.video_pk}')
#         var = getattr(model, bar.redis_variable)
#         model.objects.filter(pk=bar.video_pk).update(var=100, )
                    