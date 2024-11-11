from abc import ABC, abstractmethod
import os
import re
from typing import Iterable, None, IO

import pysrt
from googletrans import Translator, constants
from pprint import pprint
from pathlib import Path
import redis
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from .open_file_with_subtitles import IFileParser

from .progress_bar import IProgressValue



class TranslatorABC(ABC):
    pass

class GoogleTranslator(TranslatorABC):
    translator = Translator()
    
    def translate(cls, text: str, src: str='en', dest: str='ru') -> str:
        translation = cls.translator.translate(
                    text=text, src=src, dest=dest)
        return translation


class IMakeTranslating(ABC):

    @abstractmethod
    def execute(self, subtitles):
        pass


class MakeTranslating(IMakeTranslating):

    def __init__(self, translator: TranslatorABC, saver_progress_results: IProgressValue):
        self.translator = translator
        self.saver_progress_results = saver_progress_results
    
    def __save_progress_results(self, key: int, value: int) -> None:
        self.saver_progress_results.set_progress_value(key=key, value=value)
    

    def execute(self, subtitles: IFileParser,
                       path_for_subs: str, 
                       video_pk: int, 
                       progress_value: IProgressValue,
                       src_language: str='en', 
                       dest_language: str='ru') -> None:
                
        lst = []
        for s in subtitles:
            lst.append(s)

        subs_len = len(lst)
        sentences = lst
        lst = []
        
        checking_counter = 0
        k = 0

        for j in sentences:
            try:
                translation = self.translator.translate(
                    text=subtitles.get_text(j), src=src_language, dest=dest_language)
                lst.append(subtitles.get_text(translation))
                k += 1
                checking_counter += 1
                
                percentages = int((k * 100 / subs_len) / 2)
                
                if checking_counter > 15:
                    
                    progress_value.set_progress_value(f'translate_progress{video_pk}', percentages)
                    print('Translate progress: ', int(progress_value.get_progress_value(f'translate_progress{video_pk}')))
                    
                    # redis_client.set(f'translate_progress{video_pk}', percentages)
                    # print('Translate progress: ', int(redis_client.get(f'translate_progress{video_pk}')))
                    checking_counter = 0
                    
            except Exception as e:
                lst.append(subtitles.get_text(j))


        checking_counter = 0
        k = 0
        
        for i in range(len(subtitles)):
            if subtitles.get_start_time(sentences[i]) == subtitles.get_start_time(subtitles[i]) and subtitles.get_end_time(sentences[i]) == subtitles.get_end_time(subtitles[i]):
                subtitles.set_text(subtitles[i], value=lst[i])
                
            k += 1
            checking_counter += 1
            
            percentages2 = percentages + int((k * 100 / subs_len) / 2)
            
            if checking_counter > 15:
                
                progress_value.set_progress_value(f'translate_progress{video_pk}', percentages2)
                print('Translate progress: ', int(progress_value.get_progress_value(f'translate_progress{video_pk}')))
                
                # redis_client.set(f'translate_progress{video_pk}', percentages2)
                # print('Translate progress: ', int(redis_client.get(f'translate_progress{video_pk}')))
                checking_counter = 0

            progress_value.delete_progress_value(f'translate_progress{video_pk}')
            
            # redis_client.delete(f'translate_progress{video_pk}')
            # UserVideos.objects.filter(pk=video_pk).update(translate_progress=100)
            self.__save_progress_results(key=video_pk, value=100)
            
        progress_value.close()
        # redis_client.close()

        subtitles.save(path_for_subs)


# class MyLocalTranslator(IMakeTranslating):

#     init()

#     tokenizer = AutoTokenizer.from_pretrained(
#         Path.cwd() / 'web_app_auto_subs' / 'utils' / 'services' / 'subtitles1' / 'model' / 'en-ru-local')
#     model = AutoModelForSeq2SeqLM.from_pretrained(
#         Path.cwd() / 'web_app_auto_subs' / 'utils' / 'services' / 'subtitles1' / 'model' / 'en-ru-local')

#     def translate_phrase(self, phrase: str) -> str:
#         inputs = self.tokenizer(phrase, return_tensors="pt")
#         output = self.model.generate(**inputs, max_new_tokens=100)
#         out_text = self.tokenizer.batch_decode(
#             output, skip_special_tokens=True)
#         return out_text[0]

#     def make_translate(self, subtitles: pysrt, path_for_subs: str) -> None:
        
#         lst = []
#         for s in subtitles:
#             lst.append(s)

#         sentences = lst
#         lst = []

#         for j in range(len(sentences)):
#             translation = self.translate_phrase(str(sentences[j].text))
#             # print(str(translation))
#             if str(translation).casefold() in ('хм...', 'тсс!', 'тсс.','тсс','э-э', 'ух.', 'ммм.', 'мм.', 'ааа!', 'ох!', 'ммм', 'м.', 'хмм', 'ааа', 'ох.', 'ммм...', 'ааа...', 'ааа.', 'хм.'):
#                 lst.append('...')
#             else: lst.append(str(translation))
        

#         for i in range(len(subtitles)):
#             if sentences[i].start == subtitles[i].start and sentences[i].end == subtitles[i].end:
#                 # print(lst[i], '\n')
#                 subtitles[i].text = lst[i]

#         subtitles.save(path_for_subs)


# if __name__ == '__main__':
#     print(MyLocalTranslator().translate_phrase('''I think listening to a lecture is a bit boring
# I think taking exams is incredibly stressful
# I think watching TV series is really interesting
# I think that computer game is very expensive
# I think solving that equation is quite difficult
# '''))
