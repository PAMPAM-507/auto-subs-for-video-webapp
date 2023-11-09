from abc import ABC, abstractmethod
from typing import Dict, Callable


class GetLatestModelBC(ABC):

    @abstractmethod
    def get_latest(self, *args, **kwargs):
        pass


class GetLatestModel(GetLatestModelBC):

    def __init__(
            self,
            model,
    ):
        self.model = model

    def get_latest(self, attrs_for_search: Dict[str, str],
                   attrs_for_update: Dict[str, str],
                   args_for_additional_method: str = None,
                   ):
        model = self.model.objects.filter(
            **attrs_for_search
        ).latest(args_for_additional_method)

        return model

        # print(model)
        #
        # for key, value in attrs_for_update.items():
        #     print(key, value)
        #     if attrs_for_update[key]:
        #         model.key = value
        # model.save()
