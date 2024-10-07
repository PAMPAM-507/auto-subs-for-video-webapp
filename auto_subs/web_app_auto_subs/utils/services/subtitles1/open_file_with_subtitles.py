from abc import ABC, abstractmethod
from typing import IO, NoReturn, Iterable

import pysrt


class IFileParser(ABC):

    @abstractmethod
    def get_start_time(self):
        pass

    @abstractmethod
    def get_end_time(self):
        pass

    @abstractmethod
    def get_text(self):
        pass


class PysrtFileParser(IFileParser):
    def __init__(self, file: str) -> NoReturn:
        self.file: Iterable = pysrt.open(file)
        self.file_len = len(self.file)
        self.range = 0

    def get_start_time(self, subtitle: pysrt.srtitem.SubRipItem) -> str:
        return getattr(subtitle, 'start', None)

    def get_end_time(self, subtitle: pysrt.srtitem.SubRipItem) -> str:
        return getattr(subtitle, 'end', None)

    def get_text(self, subtitle: pysrt.srtitem.SubRipItem) -> str:
        return getattr(subtitle, 'text', None)

    def set_text(self, subtitle: pysrt.srtitem.SubRipItem, value: str) -> NoReturn:
        setattr(subtitle, 'text', value)

    def __len__(self) -> int:
        return self.file_len

    def __iter__(self):
        self.range = 0
        return self

    def __next__(self) -> pysrt.srtitem.SubRipItem:
        if self.range < self.file_len:
            result = self.file[self.range]
            self.range += 1
            return result
        else:
            raise StopIteration

    def __getitem__(self, key):
        return self.file[key]
    
    def save(self, path):
        self.file.save(path)

