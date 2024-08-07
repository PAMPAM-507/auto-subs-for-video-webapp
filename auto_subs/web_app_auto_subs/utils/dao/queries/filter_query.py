from dataclasses import dataclass
from typing import Iterable

from ..abstracts.filter_abc import FilterQueryAbstract
from django.db import models
from web_app_auto_subs.utils.dao.dao import DAOForModels


class FilterQuery(FilterQueryAbstract):
    """
    It is class for send request with filter() method.
    It is necessary to enter the name of the model
    to which the request will send, and some attribute names.
    If it is necessary you can enter name of fields which may not be in model,
    for example, it can be field of photo.
    """

    def filter_query(self,
                     some_model: models.Model,
                     *args,
                     exceptions: str = None,
                     additional_method: str = None,
                     **kwargs, ) -> Iterable[dataclass]:
        dao = DAOForModels(args, exceptions)
        return list(map(dao.fill_universal_data_class, some_model.objects.filter(**kwargs)))

    def filter_query_latest(self,
                            some_model: models.Model,
                            *args,
                            exceptions: str = None,
                            attr_for_additional_method: str,
                            **kwargs, ) -> dataclass:
        dao = DAOForModels(args, exceptions)
        return dao.fill_universal_data_class(
            some_model.objects.filter(**kwargs).latest(attr_for_additional_method))
