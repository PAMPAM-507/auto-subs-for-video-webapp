from dataclasses import dataclass

from typing import Iterable

from ..abstracts.all_abc import AllQueryAbstract
from web_app_auto_subs.utils.dao.dao import DAOForModels
from django.db import models


class AllQuery(AllQueryAbstract):
    """
    It is class for send request with all() method.
    It is necessary to enter the name of the model
    to which the request will send, and some attribute names.
    If it is necessary you can enter name of fields which may not be in model,
    for example, it can be field of photo.
    """

    def all_query(self, some_model: models.Model, *args, exceptions: str = None, **kwargs) -> Iterable[dataclass]:
        dao = DAOForModels(args, exceptions)
        return list(map(dao.fill_universal_data_class, some_model.objects.all()))
