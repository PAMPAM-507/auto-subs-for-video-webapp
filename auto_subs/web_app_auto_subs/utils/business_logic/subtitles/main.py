from make_subs import *
from put_subs import PutSubs
from my_translator import MyTranslator


mp4filename = os.getenv('path_for_video')
srtfilename = os.getenv('path_for_video')[9:-4] + '.srt'
srtfilename = os.getenv('path_for_video').split('/')[-1]
subtitles = pysrt.open(srtfilename)

MyTranslator().make_translate(subtitles)
PutSubs(mp4filename, srtfilename).generate_video_with_subtitles()


