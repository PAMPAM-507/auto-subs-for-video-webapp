import re


class ParseStrTimeToSeconds:
    
    @staticmethod
    def time_to_seconds(time_str) -> int:
        """Конвертирует строку времени в формате 'hh:mm:ss,ms' в секунды"""
        hours, minutes, seconds_ms = time_str.split(':')
        seconds, milliseconds = seconds_ms.split(',')
        
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        total_seconds += int(milliseconds) / 1000
        
        return int(total_seconds)

    @classmethod
    def calculate_total_seconds(cls, subtitle: str) -> int:
        """Подсчитывает количество секунд из строк с временными метками"""
        total_duration = 0
        
        # Используем регулярное выражение для извлечения двух временных меток
        match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', subtitle)
        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            
            # Конвертируем время в секунды
            start_seconds = cls.time_to_seconds(start_time)
            end_seconds = cls.time_to_seconds(end_time)
            
            # Подсчитываем продолжительность
            total_duration += (end_seconds - start_seconds)
        
        return int(total_duration)

