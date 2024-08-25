from abc import ABC
from typing import Dict, List, NoReturn, Tuple, Union

class FuzzyModelABC(ABC):
    pass

class Descriptor():

    def __set_name__(self, owner: FuzzyModelABC, name: str) -> NoReturn:
        self.name = '_' + name
    
    def __get__(self, instance: FuzzyModelABC, owner: FuzzyModelABC) -> Union[List, int]:
        # print('__get__')
        return getattr(instance, self.name)

    def __set__(self, instance: FuzzyModelABC, value: Union[int, list, dict]) -> NoReturn:
        setattr(instance, self.name, value)

