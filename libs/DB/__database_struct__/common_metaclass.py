# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 23:04:18 2025

@author: Porco Rosso
"""

import inspect

_GLOBAL_MAIN_CLASS_REF = None # 这个引用现在将指向 main 类的一个实例

class AutoPropagateMeta(type):
    """
    这个元类主要用于当你向 DuckDB/MySQL 类**本身**添加新属性时，
    通知主类更新其代理。如果你所有动态属性都在实例上，则这个元类的直接作用会减弱。
    但我们仍保留它，以防有类级别的属性需要代理，或者为了__internal_attrs__的统一性。
    """
    def __setattr__(cls, name, value):
        super().__setattr__(name, value)
        # 如果 _GLOBAL_MAIN_CLASS_REF 是 main 的一个实例，
        # 且我们想让实例代理类上的新属性，需要更复杂的逻辑。
        # 暂时，我们假设它只用于通知主类扫描类属性。
        # 在新的 __getattr__ 方案中，这个元类对于实例属性代理不再那么关键。
        # 但如果你的 __internal_attrs__ 是基于类级别的，它仍然有用。
        pass # 我们不在这里直接通知 main 实例，因为 main 实例会动态转发

def set_main_class_ref(main_instance_ref): # 现在接收的是 main 的一个实例
    global _GLOBAL_MAIN_CLASS_REF
    _GLOBAL_MAIN_CLASS_REF = main_instance_ref