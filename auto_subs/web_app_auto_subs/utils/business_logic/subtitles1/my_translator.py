from abc import ABC, abstractmethod
import os
import re
from typing import NoReturn

import pysrt
from googletrans import Translator, constants
from pprint import pprint
from pathlib import Path
from colorama import Fore, init
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class MYTranslatorABC(ABC):

    @abstractmethod
    def make_translate(self, subtitles):
        pass


class MyGoogleTranslator(MYTranslatorABC):

    translator = Translator()

    def make_translate(self, subtitles, path_for_subs):
        lst = []
        for s in subtitles:
            lst.append(s)

        sentences = lst
        lst = []

        for j in range(len(sentences)):
            try:
                translation = self.translator.translate(
                    text=sentences[j].text, src='en', dest="ru")
                lst.append(translation.text)
                
            except Exception as e:
                lst.append(f'translation error! Original text: {sentences[j].text}')

        for i in range(len(subtitles)):
            if sentences[i].start == subtitles[i].start and sentences[i].end == subtitles[i].end:
                subtitles[i].text = lst[i]
        
        print('MyGoogleTranslator')

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
