# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:30:57 2025

@author: Porco Rosso
"""
from typing import Any, Callable, Dict, List, Optional, Type

from libs.utils.functions import filter_class_attrs, merge_dicts, timing_decorator


class main:
    @classmethod
    def __timing_decorator__(
        cls,
        schema: Optional[str] = None,
        table: Optional[str] = None,
        show_time: bool = False
    ) -> Callable[..., Any]:
        return timing_decorator(schema, table, show_time)

    @classmethod
    def __get_all_parents_dict__(cls) -> List[Type[Any]]:
        return [parent for parent in cls.mro() if (parent is not object and hasattr(cls, 'mro'))][::-1]

    def __parameters__(self, *args: Dict[str, Any]) -> Dict[str, Any]:
        all_sources = [
            *[filter_class_attrs(i) for i in self.__get_all_parents_dict__()],
            filter_class_attrs(self),
            *args
        ]
        return merge_dicts(*all_sources)

    def __call__(self, replace: bool = False, **kwargs: Any) -> Optional['main']:
        parameters = self.__parameters__(kwargs)
        if replace:
            return self.__class__(**parameters)
        else:
            [setattr(self, i, j) for i, j in parameters.items()]
            
    @property
    def __login_info__(self) -> Dict[str, Any]:
        return self.__parameters__()

    def __schema_info__(self, **kwargs: Any) -> None:
        pass

    def __read__(self, **kwargs: Any) -> None:
        pass

    def __command__(self, **kwargs: Any) -> None:
        pass

    def __create_table__(self, **kwargs: Any) -> None:
        pass

    def __drop_table__(self, **kwargs: Any) -> None:
        pass

    def __table_exist__(self, **kwargs: Any) -> None:
        pass

    def __write__(self, **kwargs: Any) -> None:
        pass