from dataclasses import dataclass

from typing import Iterable

from web_app_auto_subs.utils.dao.dao import DAOForModels
from django.db import models

from ..abstracts.get_abc import GetQueryAbstract


class GetQuery(GetQueryAbstract):
    """
        It is class for send request with get() method.
        It is necessary to enter the name of the model
        to which the request will send, and some attribute names.
        If it is necessary you can enter name of fields which may not be in model,
        for example, it can be field of photo.
    """

    def get_query(self,
                  some_model: models.Model,
                  *args,
                  exceptions: str = None,
                  **kwargs, ) -> dataclass:

        dao = DAOForModels(args, exceptions)

        return dao.fill_universal_data_class(
            model=some_model.objects.get(**kwargs))

