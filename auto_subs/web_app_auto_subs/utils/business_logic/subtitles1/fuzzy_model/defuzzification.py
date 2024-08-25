from abc import ABC
from typing import Dict, List, NoReturn, Tuple, Union


class DefuzzificationABC(ABC):
    pass

class DefuzzificationByHeightMethod(DefuzzificationABC):

    @staticmethod
    def execute_defuzzification(rule_base: List[Dict[str, float],], border_for_output_term: List[float]) -> float:
        result = []
        values_of_C1 = []
        values_of_C2 = []
        values_of_C3 = []
        
        for i in rule_base:
            if i.get("C1") != 0.0 and i.get("C2") != 0.0 and i.get("C3") != 0.0:
                result.append(i)
        for i in result:
            if i.get("C1", False):
                values_of_C1.append(i.get("C1"))
            elif i.get("C2", False):
                values_of_C2.append(i.get("C2"))
            elif i.get("C3", False):
                values_of_C3.append(i.get("C3"))      

        denominator = sum(values_of_C1) + sum(values_of_C2) + sum(values_of_C3)
        
        values_of_C1, values_of_C2, values_of_C3 = list(map(lambda x: x*border_for_output_term[0], values_of_C1)), list(map(lambda x: x*border_for_output_term[1], values_of_C2)), list(map(lambda x: x*border_for_output_term[2], values_of_C3))
        
        numerator = sum(values_of_C1) + sum(values_of_C2) + sum(values_of_C3)

        return round(numerator/denominator, 2)
    
    @staticmethod
    def calculate_degree_of_owned(x: int, border1: int, border2: int) -> float:
        return round((border2 - abs(x - border1)) / border2, 2)
    
    @classmethod
    def calculate_list_of_degrees_of_owned_for_output_parameter(cls, y: float, border_for_output_term: List[float]) -> List[float]:
        list_of_degrees_of_owned_for_output_parameter = [0, 0, 0]

        if border_for_output_term[0] <= y <= border_for_output_term[1]:
            list_of_degrees_of_owned_for_output_parameter[0] = (cls.calculate_degree_of_owned(y, border_for_output_term[0], border_for_output_term[1]))
        if border_for_output_term[0] <= y <= border_for_output_term[2]:
            list_of_degrees_of_owned_for_output_parameter[1] = cls.calculate_degree_of_owned(y, border_for_output_term[1], border_for_output_term[1])
        if border_for_output_term[1] <= y <= border_for_output_term[2]:
            list_of_degrees_of_owned_for_output_parameter[2] = cls.calculate_degree_of_owned(y, border_for_output_term[2], border_for_output_term[1])

        # print("Степень принадлежности к терму 'Низкая загрузка': ", list_of_degrees_of_owned_for_output_parameter[0])
        # print("Степень принадлежности к терму 'Средняя загрузка': ", list_of_degrees_of_owned_for_output_parameter[1])
        # print("Степень принадлежности к терму 'Высокая загрузка': ", list_of_degrees_of_owned_for_output_parameter[2])

        return list_of_degrees_of_owned_for_output_parameter

    @classmethod
    def find_result_of_max_term(cls, y: float, border_for_output_term: List[float]) -> Tuple[Union[str, float]]:
        list_of_degrees_of_owned_for_output_parameter = cls.calculate_list_of_degrees_of_owned_for_output_parameter(y, border_for_output_term)
        result = {
                'C1': list_of_degrees_of_owned_for_output_parameter[0], 
                  'C2': list_of_degrees_of_owned_for_output_parameter[1], 
                  'C3': list_of_degrees_of_owned_for_output_parameter[2],
                  }

        values = list(result.values())
        keys = list(result.keys())
        maxi = max(result.values())

        for i in range(len(values)):
            if values[i] == maxi:
                index = i
                break

        key = keys[index]

        return key, y

    @classmethod
    def get_resulting_value(cls, rule_base: List[Dict[str, float],], border_for_output_term: List[float]) -> Tuple[Union[str, float]]:
        y = cls.execute_defuzzification(rule_base, border_for_output_term)

        return cls.find_result_of_max_term(y, border_for_output_term)