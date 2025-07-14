# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 22:11:13 2025

@author: Porco Rosso
"""
import functools
import inspect
from typing import Any, Callable, Dict, List, Type

from libs.DB.__database_struct__.common_metaclass import (
    AutoPropagateMeta, set_main_class_ref
)
from libs.DB.__database_struct__.DuckDB import main as DuckDB
from libs.DB.__database_struct__.MySQL import main as MySQL
from libs.DB.config import DB_RECOMMAND_SOURCE
from libs.utils.functions import flatten_list


DATA_SOURCE_DICT: Dict[str, Any] = {
    'DuckDB': DuckDB(),
    'MySQL': MySQL()
}


def setup_dynamic_properties(cls: Type[Any]) -> Type[Any]:
    """
    ===========================================================================

    Decorator to set up dynamic properties on the main class.

    This decorator scans the classes in DATA_SOURCE_DICT and creates
    property proxies on the decorated class (main) for all public attributes
    found in the source classes.

    Parameters
    ----------
    cls : Type[Any]
        The class to decorate (expected to be the 'main' class).

    Returns
    -------
    Type[Any]
        The decorated class with dynamic properties.

    ---------------------------------------------------------------------------

    用于在主类上设置动态属性的装饰器。

    该装饰器扫描 DATA_SOURCE_DICT 中的类，并为在源类中找到的所有公共属性
    在被装饰的类（main）上创建属性代理。

    参数
    ----------
    cls : Type[Any]
        要装饰的类（应为 'main' 类）。

    返回
    -------
    Type[Any]
        带有动态属性的被装饰类。

    ---------------------------------------------------------------------------
    """
    cls._dynamic_properties_cache = set()

    def _add_single_dynamic_property(inner_cls: Type[Any], attr_name: str) -> None:
        if attr_name in inner_cls._dynamic_properties_cache:
            return

        def _make_getter(name: str) -> Callable[[Type[Any]], Any]:
            def getter(cls_param: Type[Any]) -> Any:
                active_source_name = cls_param.source
                active_source_class = DATA_SOURCE_DICT[active_source_name]
                if hasattr(active_source_class, name):
                    return getattr(active_source_class, name)
                raise AttributeError(
                    f"Attribute '{name}' not found in the current active source "
                    f"'{active_source_name}' ({type(active_source_class).__name__}). "
                    f"Check if it exists or if 'source' is set correctly."
                )
            return getter

        def _make_setter(name: str) -> Callable[[Type[Any], Any], None]:
            def setter(cls_param: Type[Any], value: Any) -> None:
                active_source_name = cls_param.source
                active_source_class = DATA_SOURCE_DICT[active_source_name]
                if hasattr(active_source_class, name):
                    setattr(active_source_class, name, value)
                else:
                    raise AttributeError(
                        f"Cannot set attribute '{name}'. Not found in the current "
                        f"active source '{active_source_name}' "
                        f"({type(active_source_class).__name__})."
                    )
            return setter

        prop = property(_make_getter(attr_name), _make_setter(attr_name))
        setattr(inner_cls, attr_name, prop)
        inner_cls._dynamic_properties_cache.add(attr_name)

    setattr(cls, '_add_single_dynamic_property', _add_single_dynamic_property)

    for source_class_obj in DATA_SOURCE_DICT.values():
        if isinstance(source_class_obj, type):
            for attr_name in dir(source_class_obj):
                if not attr_name.startswith('_') and not callable(
                    getattr(source_class_obj, attr_name)
                ):
                    cls._add_single_dynamic_property(cls, attr_name)

    return cls


@setup_dynamic_properties
class main(type('MainClassBase', (), DATA_SOURCE_DICT)):
    """
    ===========================================================================

    Main class that acts as a dynamic proxy to the underlying database sources.

    It uses a metaclass and a decorator to forward attribute and method calls
    to the currently active database instance specified by the `source` attribute.

    ---------------------------------------------------------------------------

    作为底层数据库源的动态代理的主类。

    它使用元类和装饰器将属性和方法调用转发到由 `source` 属性指定的
    当前活动的数据库实例。

    ---------------------------------------------------------------------------
    """
    source: str = DB_RECOMMAND_SOURCE

    def __init__(self) -> None:
        """
        ===========================================================================

        Initializes the main proxy instance.

        ---------------------------------------------------------------------------

        初始化主代理实例。

        ---------------------------------------------------------------------------
        """
        pass

    def __getattr__(self, name: str) -> Any:
        """
        ===========================================================================

        Forwards attribute access to the active database instance.

        Parameters
        ----------
        name : str
            The name of the attribute to access.

        Returns
        -------
        Any
            The attribute from the active database instance.

        ---------------------------------------------------------------------------

        将属性访问转发到活动的数据库实例。

        参数
        ----------
        name : str
            要访问的属性的名称。

        返回
        -------
        Any
            来自活动数据库实例的属性。

        ---------------------------------------------------------------------------
        """
        if name == 'source':
            return object.__getattribute__(self, name)

        active_db_instance = DATA_SOURCE_DICT[self.source]

        if hasattr(type(self), name) and callable(getattr(type(self), name)):
            return getattr(type(self), name)

        if hasattr(active_db_instance, name):
            attr = getattr(active_db_instance, name)
            if callable(attr):
                return functools.partial(attr)
            return attr

        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}', and it was "
            f"not found in the active source '{self.source}' "
            f"({type(active_db_instance).__name__} instance)."
        )

    def __setattr__(self, name: str, value: Any) -> None:
        """
        ===========================================================================

        Sets an attribute on the main instance or the active database instance.

        Parameters
        ----------
        name : str
            The name of the attribute to set.
        value : Any
            The value to set the attribute to.

        ---------------------------------------------------------------------------

        在主实例或活动的数据库实例上设置属性。

        参数
        ----------
        name : str
            要设置的属性的名称。
        value : Any
            要将属性设置成的值。

        ---------------------------------------------------------------------------
        """
        if name == 'source' or name.startswith('_'):
            object.__setattr__(self, name, value)
            return

        active_db_instance = DATA_SOURCE_DICT[self.source]
        setattr(active_db_instance, name, value)

    @classmethod
    def __internal_attrs__(cls) -> List[str]:
        """
        ===========================================================================

        Returns a sorted list of all internal attributes from all data sources.

        Returns
        -------
        List[str]
            A list of internal attribute names.

        ---------------------------------------------------------------------------

        返回一个包含所有数据源的所有内部属性的排序列表。

        返回
        -------
        List[str]
            内部属性名称的列表。

        ---------------------------------------------------------------------------
        """
        attrs = [DATA_SOURCE_DICT[i].__internal_attrs__ for i in DATA_SOURCE_DICT]
        return sorted(flatten_list(attrs))

    @property
    def login_info(self) -> Dict[str, Any]:
        """
        ===========================================================================

        Returns the login information of the current active source.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing login info.

        ---------------------------------------------------------------------------

        返回当前活动源的登录信息。

        返回
        -------
        Dict[str, Any]
            包含登录信息的字典。

        ---------------------------------------------------------------------------
        """
        return getattr(self, self.source).__login_info__

    def schema_info(self, **kwargs: Any) -> Any:
        return getattr(self, self.source).__schema_info__(**kwargs)

    def read(self, **kwargs: Any) -> Any:
        return getattr(self, self.source).__read__(**kwargs)

    def command(self, **kwargs: Any) -> Any:
        return getattr(self, self.source).__command__(**kwargs)

    def create_table(self, **kwargs: Any) -> Any:
        return getattr(self, self.source).__create_table__(**kwargs)

    def drop_table(self, **kwargs: Any) -> Any:
        return getattr(self, self.source).__drop_table__(**kwargs)

    def table_exist(self, **kwargs: Any) -> Any:
        return getattr(self, self.source).__table_exist__(**kwargs)

    def write(self, df_obj: Any, **kwargs: Any) -> Any:
        return getattr(self, self.source).__write__(df_obj, **kwargs)

    def __repr__(self) -> str:
        """
        ===========================================================================

        Returns a string representation of the DB source and login info.

        Returns
        -------
        str
            The string representation.

        ---------------------------------------------------------------------------

        返回数据库源和登录信息的字符串表示形式。

        返回
        -------
        str
            字符串表示形式。

        ---------------------------------------------------------------------------
        """
        login_info_str = str(self.login_info)[1:-1].replace("'", '')
        sorted_info = ', \n'.join(sorted(login_info_str.split(', ')))
        return f'DB source: {self.source}, \n{sorted_info}'
