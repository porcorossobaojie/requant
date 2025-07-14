# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 21:31:13 2025

@author: Porco Rosso

"""

import re
from typing import Dict, List, Any, Type

def __filter_class_attrs__(class_object: Type[Any]) -> Dict[str, Any]:
    """
    ===========================================================================

    Extracts attributes and their values from a class object, excluding dunder methods.

    Parameters
    ----------
    class_object : Type[Any]
        The class object from which to extract attributes.

    Returns
    -------
    Dict[str, Any]
        A dictionary where keys are attribute names and values are their corresponding values.

    ---------------------------------------------------------------------------

    从类对象中提取属性及其值，排除双下划线方法。

    参数
    ----------
    class_object : Type[Any]
        要从中提取属性的类对象。

    返回
    -------
    Dict[str, Any]
        一个字典，其中键是属性名称，值是其对应的值。

    ---------------------------------------------------------------------------
    """
    def check_double_underscore(s: str) -> bool:
        return s.startswith('__') and s.endswith('__') and len(s) > 4
    
    dic = {
        i:j for i, j in class_object.__dict__.items() 
        if not check_double_underscore(i)
    }
    return dic


def __merge_dicts__(*dicts: Dict[str, Any],) -> Dict[str, Any]:
    """
    ===========================================================================

    Merges multiple dictionaries into one, with later dictionaries overriding 
    earlier ones for common keys.

    Parameters
    ----------
    *dicts : Dict[str, Any]
        Variable number of dictionaries to merge.

    Returns
    -------
    Dict[str, Any]
        A new dictionary containing the merged key-value pairs.

    ---------------------------------------------------------------------------

    将多个字典合并为一个，后面字典的键值会覆盖前面字典的键值。

    参数
    ----------
    *dicts : Dict[str, Any]
        要合并的字典的可变数量参数。

    返回
    -------
    Dict[str, Any]
        包含合并后的键值对的新字典。

    ---------------------------------------------------------------------------
    """
    all_keys = set().union(*dicts)
    
    def get_non_none_value(
        key: str
    ) -> Any:
        return next(
            (d[key] for d in reversed(dicts) if key in d and d[key] is not None), 
            None
        )
    
    return {
        key: get_non_none_value(key) for key in all_keys
    }


def __flatten_list__(lst: List[Any],) -> List[Any]:
    """
    ===========================================================================

    Flattens a nested list into a single-level list.

    Parameters
    ----------
    lst : List[Any]
        The nested list to flatten.

    Returns
    -------
    List[Any]
        A new list containing all elements from the nested list in a single level.

    ---------------------------------------------------------------------------

    将嵌套列表展平为单层列表。

    参数
    ----------
    lst : List[Any]
        要展平的嵌套列表。

    返回
    -------
    List[Any]
        一个新列表，包含嵌套列表中所有元素，且为单层。

    ---------------------------------------------------------------------------
    """
    return sum(
        (__flatten_list__(i) if isinstance(i, list) else [i] for i in lst), []
    )
