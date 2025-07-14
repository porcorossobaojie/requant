# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 09:30:57 2025

@author: Porco Rosso
"""
from libs.utils.functions import filter_class_attrs, merge_dicts, timing_decorator

from typing import Optional, Dict, Any, List, Tuple

class main():
    @classmethod    
    def __timing_decorator__(
        cls,
        schema: Optional[str] = None, 
        table: Optional[str] = None, 
        show_time: bool = False
):
        return timing_decorator(schema, table, show_time)
    
    @classmethod    
    def __get_all_parents_dict__(cls) -> List[type]:
        return [parent for parent in cls.mro() if parent is not object][::-1]
    
    def __parameters__(
        self, 
        *args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        ===========================================================================
    
        Functional function:
            Merge and update parameters as order by class -> self -> kwargs 
    
        Parameters
        ----------
        *args : Dict[str, Any]
            parameters need to update.
    
        Returns
        -------
        parameters : Dict[str, Any]
            updated parameters
    
        ---------------------------------------------------------------------------
    
        功能性函数：
            按 class -> self -> kwargs 的顺序合并和更新参数
    
        参数
        ----------
        *args : Dict[str, Any]
            需要更新的参数。
    
        返回
        -------
        parameters : Dict[str, Any]
            更新后的参数
    
        ---------------------------------------------------------------------------
        """
        parameters = merge_dicts(
            *[filter_class_attrs(i) for i in [*self.__get_all_parents_dict__(), self]],  
            *args
        )
        return parameters
    
    def __call__(
        self, 
        replace: bool = False, 
        **kwargs: Any
    ):
        """
        ===========================================================================
    
        Renew self instance by parameters given
    
        Parameters
        ----------
        replace : bool, optional
            whether new an instance or not. The default is False.
        **kwargs : dict
            parameters need to update.
    
        Returns
        -------
        login.instance or None
            update parameters for self
    
        ---------------------------------------------------------------------------
    
        根据给定的参数更新自身实例
    
        参数
        ----------
        replace : bool, optional
            是否返回一个新的实例。默认为 False。
        **kwargs : dict
            需要更新的参数。
    
        返回
        -------
        login.instance or None
            为self更新参数
    
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
    
    def __schema_info__(self, **kwargs):
        pass
    
    def __read__(self, **kwargs):
        pass
    
    def __comamnd__(self, **kwargs):
        pass
    
    def __create_table__(self, **kwargs):
        pass
    
    def __drop_table__(self, **kwargs):
        pass
    
    def __table_exist__(self, **kwargs):
        pass
    
    def __write__(self, **kwargs):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
