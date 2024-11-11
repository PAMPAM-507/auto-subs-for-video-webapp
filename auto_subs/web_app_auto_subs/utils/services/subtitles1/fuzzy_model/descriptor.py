
from typing import Dict, List, None, Tuple, Union



class Descriptor():

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = '_' + name
    
    def __get__(self, instance: object, owner: object) -> Union[List, int]:
        # print('__get__')
        return getattr(instance, self.name)

    def __set__(self, instance: object, value: Union[int, list, dict]) -> None:
        setattr(instance, self.name, value)

