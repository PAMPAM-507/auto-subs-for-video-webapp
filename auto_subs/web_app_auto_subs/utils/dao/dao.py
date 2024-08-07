from abc import ABC, abstractmethod
from django.db import connection
from dataclasses import make_dataclass, dataclass
from django.db import models


class DAOAbstract(ABC):

    @abstractmethod
    def fill_universal_data_class(self, *args, **kwargs) -> dataclass:
        pass


class DAOMiddleWare(DAOAbstract):
    def fill_universal_data_class(self, *args, **kwargs):
        pass

    def __init__(self, names_of_attrs, exceptions=None):
        self._names_of_attrs = names_of_attrs
        self._exceptions = exceptions

    @property
    def names_of_attrs(self):
        return self._names_of_attrs

    @property
    def exceptions(self):
        return self._exceptions


class DAOForModels(DAOMiddleWare):
    """
    It is universal DAO class which dynamic make dataclass by make_dataclass() and
    return this.
    It is necessary to enter the name of the attributes.
    If it is necessary you can enter name of fields which may not be in model,
    for example, it can be field of photo.
    """

    def __init__(self, names_of_attrs, exceptions=None):
        super().__init__(names_of_attrs, exceptions)

    @staticmethod
    def __verify_attrs(model, names_of_attrs: list, exceptions: str):
        if exceptions:
            try:
                if model.__getattribute__(exceptions):
                    names_of_attrs.append(exceptions)
            except AttributeError as error:
                print(error, 1)
            except Exception as error:
                print(error, 2)

        return names_of_attrs

    def fill_universal_data_class(self, model, *args, **kwargs) -> dataclass:

        lst_of_names_of_fields = self.__verify_attrs(model, self.names_of_attrs, self.exceptions)
        lst_of_types_of_fields = []
        lst_of_attrs = []
        # print(self.__dict__)
        for i in range(len(self.names_of_attrs)):

            try:
                lst_of_types_of_fields.append(type(model.__getattribute__(self.names_of_attrs[i])))

                lst_of_attrs.append(model.__getattribute__(self.names_of_attrs[i]))
            except AttributeError as err:
                print(err)
            except Exception as err:
                print(err)

        lst_of_fields = list(zip(lst_of_names_of_fields, lst_of_types_of_fields))

        some_data_class = make_dataclass('universalDataClass',
                                         lst_of_fields,
                                         namespace={'get': lambda self, attr: getattr(self, f'{attr}')})

        return some_data_class(*lst_of_attrs)


class DAOForSQL(DAOMiddleWare):

    def __init__(self, names_of_attrs, exceptions=None):
        super().__init__(names_of_attrs, exceptions)

    def fill_universal_data_class(self, sql_response: list, *args, **kwargs) -> dataclass:
        lst_of_names_of_fields = self.names_of_attrs
        lst_of_types_of_fields = []
        lst_of_attrs = sql_response

        for i in range(len(sql_response)):
            lst_of_types_of_fields.append(type(sql_response[i]))

        lst_of_fields = list(zip(lst_of_names_of_fields, lst_of_types_of_fields))

        some_data_class = make_dataclass('universalDataClass', lst_of_fields)

        return some_data_class(*lst_of_attrs)

