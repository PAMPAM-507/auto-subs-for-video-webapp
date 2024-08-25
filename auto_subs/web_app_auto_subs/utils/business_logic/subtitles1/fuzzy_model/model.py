from typing import List
from .descriptor import Descriptor, FuzzyModelABC


class FuzzyModel(FuzzyModelABC):

    border_for_first_term = Descriptor()
    border_for_second_term = Descriptor()
    border_for_output_term = Descriptor()

    __slots__ = [
        '_border_for_first_term', 
        '_border_for_second_term', 
        '_border_for_output_term'
        ]

    def __init__(
            self, 
            border_for_first_term: List[int], 
            border_for_second_term: List[int], 
            border_for_output_term: List[float],
            ):
        
        self.border_for_first_term = border_for_first_term
        self.border_for_second_term = border_for_second_term
        self.border_for_output_term = border_for_output_term
    
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)



