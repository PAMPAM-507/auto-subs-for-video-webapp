import sys
from abc import ABC, abstractmethod
from typing import List, NoReturn

import tqdm
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip

from .progress_bar import MyBarLogger
from .make_subs import MakeSubs


class PutSubsABC(ABC):
    """Abstract base class for adding subtitles to a video."""
    pass


class PutSubs(PutSubsABC):
    """
    Class for processing a video by adding subtitles, adjusting audio volume, 
    and creating a final video file.

    Attributes:
    - mp4filename (str): Name of the original video file (.mp4).
    - srtfilename (str): Name of the subtitles file (.srt).
    - video_pk (int): Unique identifier for the video, used for logging.
    - path_for_video (str): Path to the input video file.
    - path_for_new_video (str): Path where the new video will be saved.
    - new_audio_filename (str or None): Optional new audio file to mix with the original audio.
    - old_audio_volume_reduction (float): Factor by which to reduce the volume of the original audio (default: 0.5).
    """

    def __init__(self, mp4filename: str,
                 srtfilename: str,
                 video_pk: int,
                 path_for_video: str,
                 path_for_new_video: str,
                 new_audio_filename: str = None,
                 old_audio_volume_reduction: float = 0.5):
        """
        Initializes the PutSubs object with the provided video file, subtitles file, and paths.

        Args:
        - mp4filename: Name of the .mp4 video file.
        - srtfilename: Name of the .srt subtitles file.
        - video_pk: Unique ID for the video, used for logging.
        - path_for_video: Path to the input video file.
        - path_for_new_video: Path where the new video file with subtitles will be saved.
        - new_audio_filename: Optional path to a new audio file to mix into the video.
        - old_audio_volume_reduction: Reduction factor for the original audio volume (default: 0.5).
        """
        self.__begin, self.__end = mp4filename.split(".mp4")
        self.__video = VideoFileClip(path_for_video)
        self.__subtitles = pysrt.open(srtfilename)
        self.__output_video_file = self.__begin + '_subtitled' + ".mp4"
        self.__path_for_new_video = str(path_for_new_video)
        self.__new_audio = new_audio_filename
        self.__old_audio = self.__video.audio
        self.logger = MyBarLogger(video_pk)
        self.__old_audio_volume_reduction = old_audio_volume_reduction

    @staticmethod
    def __create_subtitle_clips(subtitles: pysrt.SubRipFile, video: VideoFileClip) -> List[TextClip]:
        """
        Create subtitle clips for the video based on the provided subtitle file.

        Args:
        - subtitles: SubRipFile object containing the subtitles (.srt).
        - video: The video clip to which subtitles will be added.

        Returns:
        - List of TextClip objects containing the subtitles, timed to the video.
        """
        return MakeSubs().create_subtitle_clips(subtitles, video.size)

    @staticmethod
    def __make_final_video(video: VideoFileClip,
                           subtitle_clips: list,
                           old_audio: CompositeAudioClip,
                           volume_factor: float,
                           new_audio: CompositeAudioClip = None) -> CompositeVideoClip:
        """
        Create the final video by adding subtitle clips and adjusting audio.

        Args:
        - video: The original video clip.
        - subtitle_clips: List of subtitle TextClip objects to overlay on the video.
        - old_audio: The original audio track of the video.
        - volume_factor: The factor by which to reduce the original audio volume.
        - new_audio: Optional new audio clip to mix with the original audio.

        Returns:
        - A CompositeVideoClip object containing the video with subtitles and mixed audio.
        """
        if new_audio:
            final_audio = CompositeAudioClip(
                [old_audio.volumex(volume_factor), new_audio])
            video = video.set_audio(final_audio)

        return CompositeVideoClip([video] + subtitle_clips)

    @staticmethod
    def __save_final_video(final_video: CompositeVideoClip,
                           output_video_file: str,
                           path_for_new_video: str,
                           logger: MyBarLogger) -> NoReturn:
        """
        Save the final video to the specified path.

        Args:
        - final_video: The CompositeVideoClip object representing the final video.
        - output_video_file: Name of the output video file.
        - path_for_new_video: Path to save the new video file.
        - logger: Logger for tracking the progress of the video creation.
        """
        final_video.write_videofile(
            f'{path_for_new_video}/{output_video_file}', logger=logger)

    def generate_video_with_subtitles(self) -> NoReturn:
        """
        Generate a video with subtitles and mixed audio, then save it.

        This method creates subtitle clips, mixes the audio, and calls the save function 
        to write the final video file to the specified path.
        """
        self.__save_final_video(
            self.__make_final_video(
                video=self.__video, subtitle_clips=self.__create_subtitle_clips(
                    self.__subtitles, self.__video,
                ),
                old_audio=self.__old_audio,
                volume_factor=self.__old_audio_volume_reduction,
                new_audio=self.__new_audio
            ), self.__output_video_file, self.__path_for_new_video, logger=self.logger
        )
