import re

from moviepy.editor import VideoFileClip


def get_video_duration(file_path: str) -> float:
    try:
        clip = VideoFileClip(file_path)
        duration = clip.duration
        return duration
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def parse_time(time_str: str) -> float:
    """Парсит строку времени в формате '00:00.000' и возвращает время в секундах."""
    minutes, seconds = map(float, time_str.split(':'))
    return minutes * 60 + seconds

def calculate_segment_duration(segment: str) -> float:
    """Вычисляет длительность фрагмента в секундах из строки в формате '[00:00.000 --> 00:04.000]'."""
    pattern = r'\[(\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}\.\d{3})\]'
    match = re.match(pattern, segment)
    
    if match:
        start_time = match.group(1)
        end_time = match.group(2)
        
        end_seconds = parse_time(end_time)
        
        return end_seconds
    else:
        print("Неправильный формат фрагмента")

# # Пример использования
# segment = "[00:00.000 --> 00:04.000]"
# duration = calculate_segment_duration(segment)
# print(f"Длительность фрагмента: {duration} секунд")