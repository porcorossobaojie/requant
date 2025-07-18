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

    Base class for database metadata operations.

    This class provides common methods for database interactions, including
    timing decorators, parameter handling, and schema information retrieval.

    ---------------------------------------------------------------------------

    数据库元数据操作的基类。

    此类提供数据库交互的常用方法，包括计时装饰器、参数处理和模式信息检索。

    ---------------------------------------------------------------------------
    """
    @classmethod
    def __timing_decorator__(
        cls,
        schema: Optional[str] = None,
        table: Optional[str] = None,
        show_time: bool = False
    ) -> Callable[..., Any]:
        """
        ===========================================================================

        Decorator for timing database operations.

        Parameters
        ----------
        cls : type
            The class itself.
        schema : Optional[str], optional
            The database schema name, by default None.
        table : Optional[str], optional
            The table name, by default None.
        show_time : bool, optional
            Whether to show the execution time, by default False.

        Returns
        -------
        Callable[..., Any]
            A timing decorator.

        ---------------------------------------------------------------------------

        用于计时数据库操作的装饰器。

        参数
        ----------
        cls : type
            类本身。
        schema : Optional[str], optional
            数据库模式名称，默认为 None。
        table : Optional[str], optional
            表名称，默认为 None。
        show_time : bool, optional
            是否显示执行时间，默认为 False。

        返回
        -------
        Callable[..., Any]
            一个计时装饰器。

        ---------------------------------------------------------------------------
        """
        return timing_decorator(schema, table, show_time)

    @classmethod
    def __get_all_parents_dict__(cls) -> List[Type[Any]]:
        """
        ===========================================================================

        Retrieves all parent classes in the Method Resolution Order (MRO).

        Parameters
        ----------
        cls : type
            The class itself.

        Returns
        -------
        List[Type[Any]]
            A list of parent classes.

        ---------------------------------------------------------------------------

        检索方法解析顺序 (MRO) 中的所有父类。

        参数
        ----------
        cls : type
            类本身。

        返回
        -------
        List[Type[Any]]
            父类列表。

        ---------------------------------------------------------------------------
        """
        return [
            parent for parent in cls.mro()
            if (parent is not object and hasattr(cls, 'mro'))
        ][::-1]

    def __parameters__(self, *args: Dict[str, Any]) -> Dict[str, Any]:
        """
        ===========================================================================

        Combines parameters from class attributes and arguments.

        Parameters
        ----------
        self : object
            The instance of the class.
        *args : Dict[str, Any]
            Additional dictionaries of parameters.

        Returns
        -------
        Dict[str, Any]
            A combined dictionary of parameters.

        ---------------------------------------------------------------------------

        合并类属性和参数中的参数。

        参数
        ----------
        self : object
            类的实例。
        *args : Dict[str, Any]
            额外的参数字典。

        返回
        -------
        Dict[str, Any]
            合并后的参数字典。

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

        Allows the class instance to be called like a function.

        If `replace` is True, a new instance with updated parameters is returned.
        Otherwise, the current instance's attributes are updated.

        Parameters
        ----------
        self : object
            The instance of the class.
        replace : bool, optional
            If True, return a new instance with updated parameters; otherwise, update current instance, by default False.
        **kwargs : Any
            Keyword arguments to update the instance parameters.

        Returns
        -------
        Optional['main']
            A new instance if `replace` is True, otherwise None.

        ---------------------------------------------------------------------------

        允许像函数一样调用类实例。

        如果 `replace` 为 True，则返回一个带有更新参数的新实例。
        否则，更新当前实例的属性。

        参数
        ----------
        self : object
            类的实例。
        replace : bool, optional
            如果为 True，则返回一个带有更新参数的新实例；否则，更新当前实例，默认为 False。
        **kwargs : Any
            用于更新实例参数的关键字参数。

        返回
        -------
        Optional['main']
            如果 `replace` 为 True，则为新实例，否则为 None。

        ---------------------------------------------------------------------------
        """
        parameters = self.__parameters__(kwargs)
        if replace:
            return self.__class__(**parameters)
        else:
            [setattr(self, i, j) for i, j in parameters.items()]

    @property
    def __login_info__(self) -> Dict[str, Any]:
        """
        ===========================================================================

        Retrieves the login information.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing login information.

        ---------------------------------------------------------------------------

        检索登录信息。

        返回
        -------
        Dict[str, Any]
            包含登录信息的字典。

        ---------------------------------------------------------------------------
        """
        return self.__parameters__()

    def __schema_info__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Placeholder for schema information retrieval.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        模式信息检索的占位符。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            额外的关键字参数。

        ---------------------------------------------------------------------------
        """
        pass

    def __read__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Placeholder for data reading operation.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        数据读取操作的占位符。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            额外的关键字参数。

        ---------------------------------------------------------------------------
        """
        pass

    def __command__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Placeholder for executing database commands.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        执行数据库命令的占位符。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            额外的关键字参数。

        ---------------------------------------------------------------------------
        """
        pass

    def __create_table__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Placeholder for table creation operation.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        表创建操作的占位符。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            额外的关键字参数。

        ---------------------------------------------------------------------------
        """
        pass

    def __drop_table__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Placeholder for table dropping operation.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        表删除操作的占位符。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            额外的关键字参数。

        ---------------------------------------------------------------------------
        """
        pass

    def __table_exist__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Placeholder for checking table existence.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        检查表是否存在的占位符。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            额外的关键字参数。

        ---------------------------------------------------------------------------
        """
        pass

    def __write__(self, **kwargs: Any) -> None:
        """
        ===========================================================================

        Placeholder for data writing operation.

        Parameters
        ----------
        self : object
            The instance of the class.
        **kwargs : Any
            Additional keyword arguments.

        ---------------------------------------------------------------------------

        数据写入操作的占位符。

        参数
        ----------
        self : object
            类的实例。
        **kwargs : Any
            额外的关键字参数。

        ---------------------------------------------------------------------------
        """
        pass