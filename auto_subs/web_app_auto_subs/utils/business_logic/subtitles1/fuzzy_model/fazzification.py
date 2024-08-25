from abc import ABC
from typing import Dict, List, NoReturn, Tuple, Union
from .descriptor import FuzzyModelABC

class SolveInputValueABC(ABC):
    pass

class SolveInputValueForModelWithTwoParameters(SolveInputValueABC):

    @classmethod
    def solve_input_value(cls, model: FuzzyModelABC, x1: int, x2: int) -> Tuple[List[float]]:
        list_of_degrees_of_owned_for_first_parameter = cls.calculate_list_of_degrees_of_owned(x1, model.border_for_first_term)
        list_of_degrees_of_owned_for_second_parameter = cls.calculate_list_of_degrees_of_owned(x2, model.border_for_second_term)

        return list_of_degrees_of_owned_for_first_parameter, list_of_degrees_of_owned_for_second_parameter

    @staticmethod
    def calculate_degree_of_owned(x: int, border1: int, border2: int) -> float:
        return round((border2 - abs(x - border1)) / border2, 2)
    
    @classmethod
    def calculate_list_of_degrees_of_owned(cls, x: int, border: List[int]) -> List:
        list_of_degrees_of_owned = [0, 0, 0]

        if border[0] <= x <= border[1]:
            list_of_degrees_of_owned[0] = (cls.calculate_degree_of_owned(x, border[0], border[1]))
        if border[0] <= x <= border[2]:
            list_of_degrees_of_owned[1] = cls.calculate_degree_of_owned(x, border[1], border[1])
        if border[1] <= x <= border[2]:
            list_of_degrees_of_owned[2] = cls.calculate_degree_of_owned(x, border[2], border[1])
        if x > border[2]:
            list_of_degrees_of_owned = [0, 0, 1]

        return list_of_degrees_of_owned