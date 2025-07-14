# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 22:11:13 2025

@author: Porco Rosso
"""

import inspect

from libs.DB.__database_struct__.DuckDB import main as DuckDB
from libs.DB.__database_struct__.MySQL import main as MySQL
from libs.DB.config import DB_RECOMMAND_SOURCE
from libs.utils.functions import flatten_list

DATA_SOURCE_DICT = {
    'DuckDB': DuckDB(),
    'MySQL': MySQL()
}

from libs.DB.__database_struct__.common_metaclass import AutoPropagateMeta, set_main_class_ref

# --- 2. 主类的装饰器 (setup_dynamic_properties) ---
# 这个装饰器应放在此处，因为它需要访问 DATA_SOURCE_DICT 和 main 类自身
def setup_dynamic_properties(cls):
    # 用于跟踪 main 类上已创建的动态属性
    cls._dynamic_properties_cache = set()

    @classmethod # <-- 注意这里，getter/setter 的上下文将是类方法
    def _add_single_dynamic_property(inner_cls, attr_name):
        """
        内部方法：为新发现的属性添加单个 @property 和 @setter。
        确保只添加一次。
        """
        if attr_name in inner_cls._dynamic_properties_cache:
            return # 已存在，跳过

        # 创建 getter 函数
        # 注意：这里的 getter 不再接收 self，而是接收 cls（即 main 类本身）
        def _make_getter(name):
            # 将 getter 定义为接收 cls 参数
            def getter(cls_param): # 改名为 cls_param 以避免与外部 cls 混淆
                active_source_class_name = cls_param.source # 从 main 类获取当前源
                active_source_class = DATA_SOURCE_DICT[active_source_class_name] # 从字典获取实际的类对象
                
                if hasattr(active_source_class, name):
                    return getattr(active_source_class, name)
                else:
                    raise AttributeError(
                        f"在当前活动源 '{active_source_class_name}' (来自 {active_source_class.__name__}) 中未找到属性 '{name}'。 "
                        f"请检查其是否存在或 'source' 是否设置正确。"
                    )
            return getter

        # 创建 setter 函数
        # 注意：这里的 setter 也不再接收 self，而是接收 cls（即 main 类本身）
        def _make_setter(name):
            # 将 setter 定义为接收 cls 参数
            def setter(cls_param, value): # 改名为 cls_param 以避免与外部 cls 混淆
                active_source_class_name = cls_param.source # 从 main 类获取当前源
                active_source_class = DATA_SOURCE_DICT[active_source_class_name] # 从字典获取实际的类对象
                
                if hasattr(active_source_class, name):
                    setattr(active_source_class, name, value)
                else:
                    raise AttributeError(
                        f"无法设置属性 '{name}'。在当前活动源 '{active_source_class_name}' (来自 {active_source_class.__name__}) 中未找到。"
                    )
            return setter

        # 创建并设置属性
        prop = property(_make_getter(attr_name), _make_setter(attr_name))
        setattr(inner_cls, attr_name, prop)
        inner_cls._dynamic_properties_cache.add(attr_name)
        # print(f"-> main 类已动态添加属性代理: '{attr_name}'")

    # 将这个内部方法绑定到 main 类上
    setattr(cls, '_add_single_dynamic_property', _add_single_dynamic_property)

    # 在类定义时执行初始扫描，为所有已知属性创建代理
    for source_class_obj in DATA_SOURCE_DICT.values():
        if isinstance(source_class_obj, type): # 确保是类对象，防止 DATA_SOURCE_DICT 中有其他非类值
            for attr_name in dir(source_class_obj):
                if not attr_name.startswith('_') and not callable(getattr(source_class_obj, attr_name)):
                    cls._add_single_dynamic_property(attr_name)

    return cls
    
# 3. 定义 'main' 类并应用装饰器
@setup_dynamic_properties
class main(type('MainClassBase', (), DATA_SOURCE_DICT)):
    source = DB_RECOMMAND_SOURCE

    def __init__(self):
        # main 实例自己可能需要维护一些状态，但不会直接持有数据库属性
        pass

    def __getattr__(self, name: str):
        """
        当访问 main 实例上不存在的属性时被调用。
        它会将属性访问转发给当前活动的数据库实例。
        """
        if name == 'source': # 避免循环访问 source 属性
            return object.__getattribute__(self, name) # 直接获取 main 实例的 source 属性

        active_db_instance = DATA_SOURCE_DICT[self.source]
        
        # 优先从 main 类本身获取（例如 __internal_attrs__ 这样的类方法）
        if hasattr(type(self), name) and callable(getattr(type(self), name)):
            return getattr(type(self), name) # 如果是类方法，直接返回类方法
        
        # 否则，从当前活跃的数据库实例获取属性
        if hasattr(active_db_instance, name):
            # 如果是可调用的（例如 __command__ 或 __engine__），返回一个绑定到实例的方法
            attr = getattr(active_db_instance, name)
            if callable(attr):
                # 如果是方法，我们希望它在被调用时仍然作用于 active_db_instance
                # return lambda *args, **kwargs: attr(*args, **kwargs) # 这种简单 lambda 可以，但失去了方法签名
                import functools
                return functools.partial(attr) # 更好的方法绑定

            return attr
        
        raise AttributeError(
            f"'{type(self).__name__}' 对象没有属性 '{name}'，且在当前活动源 "
            f"'{self.source}' ({active_db_instance.__class__.__name__} 实例) 中也未找到。"
        )

    def __setattr__(self, name: str, value) -> None:
        """
        当设置 main 实例的属性时被调用。
        它会将属性设置转发给当前活动的数据库实例，或者设置 main 自身的属性。
        """
        # 如果是 main 自身的属性 (例如 'source')，直接设置
        if name == 'source' or name.startswith('_'): # 假定以 '_' 开头的或 'source' 是 main 自身的
            object.__setattr__(self, name, value)
            return

        active_db_instance = DATA_SOURCE_DICT[self.source]
        
        # 尝试设置到活跃的数据库实例上
        # 这里需要判断是设置现有属性还是添加新属性
        # 对于实例化后才有的属性，我们通常希望直接设置到实例上
        setattr(active_db_instance, name, value)
        # print(f"DEBUG: 属性 '{name}' 已设置到 '{active_db_instance.__class__.__name__}' 实例。")


    @classmethod
    def __internal_attrs__(cls):
        return sorted(flatten_list([DATA_SOURCE_DICT[i].__internal_attrs__() for i in DATA_SOURCE_DICT.keys()]))
    
    @property
    def login_info(self):
        return getattr(self, self.source).__login_info__
    
    def schema_info(self, **kwargs):
        return getattr(self, self.source).__schema_info__(**kwargs)

    def read(self, **kwargs):
        return  getattr(self, self.source).__read__(**kwargs)
    
    def command(self, **kwargs):
        return  getattr(self, self.source).__command__(**kwargs)
    
    def create_table(self, **kwargs):
        return  getattr(self, self.source).__create_table__(**kwargs)
    
    def drop_table(self, **kwargs):
        return  getattr(self, self.source).__drop_table__(**kwargs)
    
    def table_exist(self, **kwargs):
        return  getattr(self, self.source).__table_exist__(**kwargs)
    
    def write(self, df_obj, **kwargs):
        return  getattr(self, self.source).__write__(df_obj, **kwargs)
    
    def __repr__(self):
        dic = ', \n'.join(sorted(str(self.__login_info__)[1:-1].replace("'", '').split(', ')))
        dic = f'DB source: {self.source}, \n' + dic
        return dic
    
    
    
    
    
    
    
    
    
    
    
    
    