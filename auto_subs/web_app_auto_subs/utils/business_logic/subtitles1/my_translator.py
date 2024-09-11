from abc import ABC, abstractmethod
import os
import re
from typing import NoReturn, IO

import pysrt
from googletrans import Translator, constants
from pprint import pprint
from pathlib import Path
from colorama import Fore, init
import redis
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from web_app_auto_subs.models import UserVideos


class MYTranslatorABC(ABC):

    @abstractmethod
    def make_translate(self, subtitles):
        pass


class MyGoogleTranslator(MYTranslatorABC):

    translator = Translator()

    def make_translate(self, subtitles: pysrt.SubRipFile, 
                       path_for_subs: str, 
                       video_pk: int, 
                       src_language: str='en', 
                       dest_language: str='ru') -> NoReturn:
        
        redis_client = redis.Redis(host='localhost', port=6380, db=0)
        
        lst = []
        for s in subtitles:
            lst.append(s)

        subs_len = len(lst)
        sentences = lst
        lst = []
        
        checking_counter = 0
        k = 0

        for j in range(len(sentences)):
            try:
                translation = self.translator.translate(
                    text=sentences[j].text, src=src_language, dest=dest_language)
                lst.append(translation.text)
                k += 1
                checking_counter += 1
                
                percentages = int((k * 100 / subs_len) / 2)
                
                if checking_counter > 15:

                    redis_client.set(f'translate_progress{video_pk}', percentages)
                    print('Translate progress: ', int(redis_client.get(f'translate_progress{video_pk}')))
                    checking_counter = 0
                    
            except Exception as e:
                lst.append(f'translation error! Original text: {sentences[j].text}')


        checking_counter = 0
        k = 0
        
        for i in range(len(subtitles)):
            if sentences[i].start == subtitles[i].start and sentences[i].end == subtitles[i].end:
                subtitles[i].text = lst[i]
                
            k += 1
            checking_counter += 1
            
            percentages2 = percentages + int((k * 100 / subs_len) / 2)
            
            if checking_counter > 15:
                
                redis_client.set(f'translate_progress{video_pk}', percentages2)
                print('Translate progress: ', int(redis_client.get(f'translate_progress{video_pk}')))
                checking_counter = 0
        
            redis_client.delete(f'translate_progress{video_pk}')
            UserVideos.objects.filter(pk=video_pk).update(translate_progress=100)
        
        redis_client.close()

        subtitles.save(path_for_subs)


class MyLocalTranslator(MYTranslatorABC):

    init()

    tokenizer = AutoTokenizer.from_pretrained(
        Path.cwd() / 'web_app_auto_subs' / 'utils' / 'business_logic' / 'subtitles1' / 'model' / 'en-ru-local')
    model = AutoModelForSeq2SeqLM.from_pretrained(
        Path.cwd() / 'web_app_auto_subs' / 'utils' / 'business_logic' / 'subtitles1' / 'model' / 'en-ru-local')

    def translate_phrase(self, phrase: str) -> str:
        inputs = self.tokenizer(phrase, return_tensors="pt")
        output = self.model.generate(**inputs, max_new_tokens=100)
        out_text = self.tokenizer.batch_decode(
            output, skip_special_tokens=True)
        return out_text[0]

    def make_translate(self, subtitles: pysrt, path_for_subs: str) -> NoReturn:
        
        lst = []
        for s in subtitles:
            lst.append(s)

        sentences = lst
        lst = []

        for j in range(len(sentences)):
            translation = self.translate_phrase(str(sentences[j].text))
            # print(str(translation))
            if str(translation).casefold() in ('хм...', 'тсс!', 'тсс.','тсс','э-э', 'ух.', 'ммм.', 'мм.', 'ааа!', 'ох!', 'ммм', 'м.', 'хмм', 'ааа', 'ох.', 'ммм...', 'ааа...', 'ааа.', 'хм.'):
                lst.append('...')
            else: lst.append(str(translation))
        

        for i in range(len(subtitles)):
            if sentences[i].start == subtitles[i].start and sentences[i].end == subtitles[i].end:
                # print(lst[i], '\n')
                subtitles[i].text = lst[i]

        subtitles.save(path_for_subs)


if __name__ == '__main__':
    print(MyLocalTranslator().translate_phrase('''I think listening to a lecture is a bit boring
I think taking exams is incredibly stressful
I think watching TV series is really interesting
I think that computer game is very expensive
I think solving that equation is quite difficult
'''))
