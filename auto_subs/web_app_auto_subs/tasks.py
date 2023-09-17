import os
from .main import *

from celery import shared_task
from auto_subs.celery import app
from auto_subs.settings import BASE_DIR, path_for_subtitles, path_for_video_with_subs


@app.task
def make_subs(path_of_video: str):
    # path_for_subtitles = str(BASE_DIR) + '/media/subtitles/'
    # path_for_video_with_subs = str(BASE_DIR) + '/media/videos_with_subs/'
    os.system(f'cd {path_for_subtitles} && whisper {path_of_video}')
    execute_bs_for_make_subs(path_of_video, path_for_subtitles, path_for_video_with_subs)
