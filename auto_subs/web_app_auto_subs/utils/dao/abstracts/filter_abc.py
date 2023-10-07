from dataclasses import make_dataclass, dataclass
from abc import ABC, abstractmethod
from typing import Iterable


class FilterQueryAbstract(ABC):

    @abstractmethod
    def filter_query(self, *args, **kwargs) -> Iterable[dataclass]:
        pass
