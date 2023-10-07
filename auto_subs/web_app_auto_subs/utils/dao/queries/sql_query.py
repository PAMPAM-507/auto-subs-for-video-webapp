from dataclasses import dataclass
from typing import Iterable
from django.db import connection

from ..abstracts.sqlquery_abc import SQLQueryAbstract
from django.db import models
from web_app_auto_subs.utils.dao.dao import DAOForModels


class SqlQuery(SQLQueryAbstract):

    def sql_query(self, *args, **kwargs) -> Iterable[dataclass]:
        pass


# с помощью split обрезать разделаить по пробелам sql запрос,
# найти там ключевые слова select и from, по этим границам обрезать список и
# передать этот список аргументов в dao



