# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:30:57 2025

@author: Porco Rosso
"""
from typing import Any, Callable, Dict, List, Optional, Type

from libs.utils.functions import filter_class_attrs, merge_dicts, timing_decorator


class main:
    """
    ===========================================================================

    A meta class providing foundational functionalities for database handlers.

    This class offers parameter management, instance renewal, and placeholder
    methods for common database operations.

    ---------------------------------------------------------------------------

    一个为数据库处理器提供基础功能的元类。

    该类提供参数管理、实例更新以及通用数据库操作的占位符方法。

    ---------------------------------------------------------------------------
    """
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
        return [parent for parent in cls.mro() if parent is not object][::-1]

    def __parameters__(
        self,
        *args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        ===========================================================================

        Merge and update parameters in the order: class -> self -> kwargs.

        Parameters
        ----------
        *args : Dict[str, Any]
            Dictionaries of parameters to update.

        Returns
        -------
        Dict[str, Any]
            The updated parameters dictionary.

        ---------------------------------------------------------------------------

        按 class -> self -> kwargs 的顺序合并和更新参数。

        参数
        ----------
        *args : Dict[str, Any]
            需要更新的参数字典。

        返回
        -------
        Dict[str, Any]
            更新后的参数字典。

        ---------------------------------------------------------------------------
        """
        all_sources = [
            *[filter_class_attrs(i) for i in self.__get_all_parents_dict__()],
            filter_class_attrs(self),
            *args
        ]
        return merge_dicts(*all_sources)

    def __call__(self, replace: bool = False, **kwargs: Any) -> Optional['main']:
        """
        ===========================================================================

        Renews the instance with given parameters.

        Parameters
        ----------
        replace : bool, optional
            Whether to return a new instance or modify in-place. Defaults to False.
        **kwargs : Any
            Parameters to update.

        Returns
        -------
        Optional['main']
            A new instance if replace is True, otherwise None.

        ---------------------------------------------------------------------------

        根据给定的参数更新实例。

        参数
        ----------
        replace : bool, optional
            是返回一个新实例还是原地修改。默认为 False。
        **kwargs : Any
            需要更新的参数。

        返回
        -------
        Optional['main']
            如果 replace 为 True，则返回一个新实例，否则返回 None。

        ---------------------------------------------------------------------------
        """
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
