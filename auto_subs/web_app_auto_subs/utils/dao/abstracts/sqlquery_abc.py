from dataclasses import make_dataclass, dataclass
from abc import ABC, abstractmethod
from typing import Iterable
from django.db import connection


class SQLQueryAbstract(ABC):

    @abstractmethod
    def sql_query(self, *args, **kwargs) -> Iterable[dataclass]:
        pass

    @staticmethod
    def _push_raw_query(sql: str = 'None', *args, **kwargs):
        if sql == None:
            raise ValueError('sql is mandatory variable, this contain str field')

        with connection.cursor() as cursor:
            cursor.execute(sql, [*args])
            return list(cursor.fetchall())


