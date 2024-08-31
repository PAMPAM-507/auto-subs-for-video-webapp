import os
import sys
import time
from typing import NoReturn
import tqdm
import whisper
import datetime
import redis

class _CustomProgressBar(tqdm.tqdm):
    def __init__(self, video_pk: int=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = self.n
        self.video_pk = video_pk

    def update(self, n):
        super().update(n)
        self._current += n

        # print("Progress: " + str(self._current) + "/" + str(self.total))
        # print('Progress of transcription process: ', int(((self._current * 100) / self.total)), '%')

        with redis.Redis(host='localhost', port=6380, db=0) as r:
            r.set(f'whisper_progress{self.video_pk}', int(((self._current * 100) / self.total)))
            print('Progress of transcription process: ', int(r.get(f'whisper_progress{self.video_pk}')))


from proglog import ProgressBarLogger

class MyBarLogger(ProgressBarLogger):

    def __init__(self, video_pk: int):
        super().__init__()
        self.last_message = ''
        self.previous_percentage = 0
        self.video_pk = video_pk
        
    def __del__(self, ):
        if self.video_pk < 100 or self.video_pk > 100:
            with redis.Redis(host='localhost', port=6380, db=0) as r:
                r.set(f'moviepy_progress{self.video_pk}', 100)

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
                    with redis.Redis(host='localhost', port=6380, db=0) as r:
                        r.set(f'moviepy_progress{self.video_pk}', self.previous_percentage)
                        print('Progress of transcription process: ', int(r.get(f'moviepy_progress{self.video_pk}')))

# logger = MyBarLogger()