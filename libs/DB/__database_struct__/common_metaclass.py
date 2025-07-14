# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 23:04:18 2025

@author: Porco Rosso
"""

from typing import Any, Optional


_GLOBAL_MAIN_CLASS_REF: Optional[Any] = None


class AutoPropagateMeta(type):
    """
    ===========================================================================

    Metaclass to automatically handle attribute propagation.

    While its direct role is diminished in an instance-based proxy model,
    it is retained for potential class-level attribute proxying and for
    maintaining structural consistency.

    ---------------------------------------------------------------------------

    用于自动处理属性传播的元类。

    虽然在基于实例的代理模型中其直接作用有所减弱，但为了潜在的类级别
    属性代理和保持结构一致性，它仍然被保留。

    ---------------------------------------------------------------------------
    """
    def __setattr__(cls, name: str, value: Any) -> None:
        """
        ===========================================================================

        Sets an attribute on the class.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : Any
            The value of the attribute.

        ---------------------------------------------------------------------------

        在类上设置一个属性。

        参数
        ----------
        name : str
            属性的名称。
        value : Any
            属性的值。

        ---------------------------------------------------------------------------
        """
        super().__setattr__(name, value)
        # In the current design, direct notification to the main instance
        # is not necessary as attribute access is dynamically forwarded.
        pass


def set_main_class_ref(main_instance_ref: Any) -> None:
    """
    ===========================================================================

    Sets a global reference to the main class instance.

    Parameters
    ----------
    main_instance_ref : Any
        The reference to the main class instance.

    ---------------------------------------------------------------------------

    设置一个对主类实例的全局引用。

    参数
    ----------
    main_instance_ref : Any
        对主类实例的引用。

    ---------------------------------------------------------------------------
    """
    global _GLOBAL_MAIN_CLASS_REF
    _GLOBAL_MAIN_CLASS_REF = main_instance_ref
