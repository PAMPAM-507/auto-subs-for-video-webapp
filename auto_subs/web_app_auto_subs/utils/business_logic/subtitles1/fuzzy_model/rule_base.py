from abc import ABC

class MakeRuleBaseABC(ABC):
    pass


class MakeRuleBase(MakeRuleBaseABC):

    @staticmethod
    def make_rule_base(A1: int, A2: int, A3: int,
             B1: int, B2: int, B3: int):
        
        result = [{"C2": A1 * B1},
            {"C1": A1 * B2},
            {"C1": A1 * B3},
            {"C3": A2 * B1},
            {"C2": A2 * B2},
            {"C1": A2 * B3},
            {"C3": A3 * B1},
            {"C2": A3 * B2},
            {"C2": A3 * B3}]
        
        new_values = list(map(lambda x: round(list(x.values())[0], 2), result))
        
        for i, dictionary in enumerate(result):
            for key in dictionary:
                dictionary[key] = new_values[i]
        
        return result