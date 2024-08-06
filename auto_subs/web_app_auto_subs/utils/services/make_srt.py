import datetime

class MakingSrt():

    @staticmethod
    def convert_seconds(seconds):
        """Convert seconds to SRT time format."""
        delta = datetime.timedelta(seconds=seconds)
        hours, remainder = divmod(delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = delta.microseconds // 1000
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"

    @classmethod
    def write_srt(cls, transcription_result, srt_filepath):
        segments = transcription_result['segments']
        with open(srt_filepath, 'w', encoding='utf-8') as srt_file:
            for i, segment in enumerate(segments):
                start_time = cls.convert_seconds(segment['start'])
                end_time = cls.convert_seconds(segment['end'])
                text = segment['text'].strip()
                srt_file.write(f"{i + 1}\n")
                srt_file.write(f"{start_time} --> {end_time}\n")
                srt_file.write(f"{text}\n\n")