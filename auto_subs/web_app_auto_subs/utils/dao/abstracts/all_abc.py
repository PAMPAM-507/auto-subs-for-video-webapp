from dataclasses import make_dataclass, dataclass
from abc import ABC, abstractmethod
from typing import Iterable
from django.db import models


class AllQueryAbstract(ABC):

    @abstractmethod
    def all_query(self, model: models.Model) -> Iterable[dataclass]:
        pass
