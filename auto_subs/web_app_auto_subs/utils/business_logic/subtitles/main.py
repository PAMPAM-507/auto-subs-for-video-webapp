import os
import pysrt
from .make_subs import *
from .put_subs import PutSubs
from .my_translator import MyTranslator
from auto_subs.settings import BASE_DIR


def execute_bs_for_make_subs(path_of_video: str,
                             path_for_subtitles: str,
                             path_for_video_with_subs: str,
                             subs_language: str
                             ):

    mp4filename = path_of_video
    srtfilename = path_for_subtitles + str(path_of_video).split('/')[-1][0:-4] + '.srt'
    subtitles = pysrt.open(srtfilename)
    name_of_video = path_of_video.split('/')[-1][0:-4]

    MyTranslator().make_translate(subtitles, name_of_video, subs_language)

    PutSubs(mp4filename, srtfilename,
            path_for_video_with_subs, name_of_video
            ).generate_video_with_subtitles()


