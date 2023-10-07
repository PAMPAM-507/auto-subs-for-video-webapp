from dataclasses import make_dataclass, dataclass
from abc import ABC, abstractmethod
from typing import Iterable


class GetQueryAbstract(ABC):

    @abstractmethod
    def get_query(self, *args, **kwargs) -> dataclass:
        pass
