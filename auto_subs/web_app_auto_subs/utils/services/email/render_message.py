from abc import ABC, abstractmethod
from django.template.loader import render_to_string


class RenderMessageABC(ABC):

    @abstractmethod
    def render_message(self, template: str, dictionary: dict, **kwargs):
        pass


class RenderMessage(RenderMessageABC):

    def render_message(self, template: str, dictionary: dict, **kwargs):
        return render_to_string(template, dictionary)
