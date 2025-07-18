# Project Coding Style Guide

This document outlines the preferred coding style and principles for this project. Adhering to these guidelines ensures consistency, readability, and maintainability across the codebase, reflecting the project's unique taste and approach to software development. This guide integrates project-specific conventions with general Python best practices, primarily drawing from PEP 8.

## 1. General Principles

*   **File Header Preservation:** The initial file header, including creation date and author information, must be preserved during any modifications. This metadata is crucial for historical tracking and attribution.
*   **Clarity and Readability:** Code should be easy to understand and follow. Prioritize clear, explicit code over clever or overly concise solutions.
*   **Maintainability:** Code should be structured in a way that facilitates future modifications, debugging, and collaboration.
*   **Modularity:** Components should be self-contained, have clear responsibilities, and minimize interdependencies.
*   **Performance (Quantitative Focus):** For quantitative analysis, prioritize vectorized operations and efficient data handling, typically using `pandas` and `numpy`. Avoid unnecessary loops when vectorized alternatives exist.

## 2. Naming Conventions

Naming conventions are crucial for code readability and consistency. This project adopts a blend of PEP 8 and specific project conventions.

### 2.1 Classes

*   **Main/Core Classes:** For the primary class within a module that serves as the main entry point or proxy, use `main` (lowercase). This is a project-specific convention.
    *   *Example:* `class main:`
*   **Configuration/Constant Classes:** For classes primarily holding static configuration or constant values, use `ALL_CAPS`. This is a project-specific convention.
    *   *Example:* `class DATABASE:`
*   **Other Classes:** For all other general-purpose classes, use `CapWords` (PascalCase), where each word in the name begins with a capital letter. This aligns with PEP 8.
    *   *Example:* `class MyProcessor:`

### 2.2 Functions and Methods

*   Use `snake_case` (lowercase words separated by underscores) for function and method names. This aligns with PEP 8.
    *   *Example:* `process_data`, `calculate_sharpe_ratio`
*   **Internal Methods:** For methods intended for internal use within a class or module, use a `__double_underscore__` prefix (e.g., `__log_activity__`, `__read__`, `__command__`). This is a distinct project convention, differing from standard Python `_single_underscore` for internal methods, and is used to clearly denote methods that are part of the internal API and should not be directly called by external code.
    *   *Example:* `def __log_activity__(self, message: str) -> None:`

### 2.3 Variables

*   Use `snake_case` for variable names. This aligns with PEP 8.
    *   *Example:* `total_count`, `file_path`
*   **Constants (Module-Level):** For constants defined at the module level, use `ALL_CAPS` (all uppercase letters with words separated by underscores). This aligns with PEP 8.
    *   *Example:* `DEFAULT_TIMEOUT`, `MAX_RETRIES`

## 3. Code Formatting

Consistent code formatting improves readability and reduces cognitive load.

### 3.1 Indentation

*   Use 4 spaces per indentation level. Never use tabs. This aligns with PEP 8.

### 3.2 Blank Lines

*   **Two blank lines** between top-level function or class definitions. This aligns with PEP 8.
*   One blank line around logical sections within functions/methods for readability. This aligns with PEP 8.

### 3.3 Imports

*   Imports should be at the top of the file, immediately after any module docstrings and `coding` declarations. This aligns with PEP 8.
*   Group imports in the following order, separated by a blank line:
    1.  Standard library imports (e.g., `os`, `sys`).
    2.  Third-party library imports (e.g., `pandas`, `numpy`).
    3.  Local project-specific imports.
*   Within each group, imports should be sorted alphabetically. This aligns with PEP 8.
*   Avoid wildcard imports (`from module import *`). This aligns with PEP 8.

### 3.4 Line Length

*   While not strictly enforced to 79 characters (as per PEP 8), strive for readability. Break long lines where appropriate to enhance clarity. Docstring separators (`===================`) are an explicit exception and may exceed this limit. The goal is to keep lines manageable and easy to read without excessive horizontal scrolling.
*   **Function Variable Line Breaks:** When a function has more than 3 variables (excluding `self`, `cls`, and other system default variables), consider breaking lines based on the actual length of the function definition line. For 4 or more variables, line breaks should generally be applied unless the function definition line is exceptionally short.

### 3.5 Whitespace in Expressions and Statements

*   Avoid extraneous whitespace in the following situations (aligns with PEP 8):
    *   Immediately inside parentheses, brackets or braces.
    *   Immediately before a comma, semicolon, or colon.
    *   Immediately before the open parenthesis that starts the argument list of a function call.
    *   Immediately before the open bracket that starts a slice or indexing.
*   Always surround binary operators (assignment, comparisons, booleans, arithmetic) with a single space on either side. This aligns with PEP 8.

## 4. Type Hinting

Consistent and clear type hinting is essential for code clarity, maintainability, and enabling static analysis tools.

*   **Consistent Use:** All function arguments, return values, and significant variables should have type hints. This is a strong project requirement.
*   **Clarity:** Use specific types where possible (e.g., `List[str]` instead of `list`, `Dict[str, Any]` instead of `dict`).
*   **`Any` Usage:** Use `Any` sparingly, typically for highly generic functions, when dealing with external libraries that lack precise type information, or when type complexity outweighs the benefit. When `Any` is used, consider adding a comment explaining why.
*   **Inferred Types:** For function variables and outputs, infer types based on context and meaning.

## 5. Object-Oriented Programming (OOP)

This project leverages advanced OOP principles for robust and flexible system design.

*   **Encapsulation:** Use properties and methods to control access to internal state, rather than directly exposing attributes.
*   **Inheritance and Composition:** Prefer composition over inheritance where appropriate, especially for building flexible and reusable components.
*   **Advanced Patterns:** Actively utilize advanced OOP features like metaclasses, `__getattr__`, `__setattr__`, `__call__` for dynamic behavior and proxy patterns. This is particularly relevant for database interactions, data source abstraction, and other areas requiring highly flexible and extensible designs.

## 6. Example Code Illustrating Style

The following snippet encapsulates the key style characteristics described above:

```python
# Example.py

import os
import sys
import pandas as pd
import numpy as np
from typing import Any, Dict, List

# Third-party imports
# from some_library import SomeClass

# Local project-specific imports
# from project.utils import helper_function


class CONFIG:
    """
    ===========================================================================

    Configuration class for example settings.

    This class holds static configuration values for the project.

    ---------------------------------------------------------------------------

    示例配置类。

    此类包含项目的静态配置值。

    ---------------------------------------------------------------------------
    """
    DEFAULT_VALUE: int = 10
    DATA_PATH: str = "/data/example.csv"
    MAX_RETRIES: int = 3


class main:
    """
    ===========================================================================

    Main class demonstrating the project's coding style.

    This class showcases various style elements including bilingual docstrings,
    type hinting, and specific naming conventions. It acts as a primary entry
    point or proxy for certain functionalities.

    ---------------------------------------------------------------------------

    展示项目编码风格的主类。

    此类展示了包括双语文档字符串、类型提示和特定命名约定在内的各种风格元素。
    它作为某些功能的主要入口点或代理。

    ---------------------------------------------------------------------------
    """
    def __init__(self, initial_data: pd.DataFrame) -> None:
        """
        ===========================================================================

        Initializes the ExampleProcessor with some data.

        Parameters
        ----------
        initial_data : pd.DataFrame
            The initial DataFrame to process.

        ---------------------------------------------------------------------------

        使用数据初始化 ExampleProcessor。

        参数
        ----------
        initial_data : pd.DataFrame
            要处理的初始 DataFrame。

        ---------------------------------------------------------------------------
        """
        self._data: pd.DataFrame = initial_data
        self.__log_activity__("ExampleProcessor initialized.")


    def process_data(self) -> pd.DataFrame:
        """
        ===========================================================================

        Processes the internal data.

        This method applies a simple transformation to the DataFrame,
        demonstrating vectorized operations.

        Returns
        -------
        pd.DataFrame
            The processed DataFrame.

        ---------------------------------------------------------------------------

        处理内部数据。

        此方法对 DataFrame 应用简单的转换，展示了向量化操作。

        返回
        -------
        pd.DataFrame
            处理后的 DataFrame。

        ---------------------------------------------------------------------------
        """
        print(f"Using default value: {CONFIG.DEFAULT_VALUE}")
        # Example of vectorized operation
        processed_df: pd.DataFrame = self._data * CONFIG.DEFAULT_VALUE
        return processed_df


    def __log_activity__(self, message: str) -> None:
        """
        ===========================================================================

        Logs an internal activity.

        This is an example of an internal method using double underscores,
        indicating it's part of the internal API.

        Parameters
        ----------
        message : str
            The message to log.

        ---------------------------------------------------------------------------

        记录内部活动。

        这是一个使用双下划线的内部方法示例，表示它是内部 API 的一部分。

        参数
        ----------
        message : str
            要记录的消息。

        ---------------------------------------------------------------------------
        """
        print(f"Internal Log: {message}")


def standalone_function(input_list: List[int]) -> List[int]:
    """
    ===========================================================================

    A standalone function demonstrating top-level function style.

    This function doubles each number in the input list.

    ---------------------------------------------------------------------------

    一个展示顶级函数风格的独立函数。

    此函数将输入列表中的每个数字加倍。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    input_list : List[int]
        A list of integers.

    ---------------------------------------------------------------------------

    参数
    ----------
    input_list : List[int]
        一个整数列表。

    ---------------------------------------------------------------------------

    Returns
    -------
    List[int]
        A new list with each number doubled.

    ---------------------------------------------------------------------------

    返回
    -------
    List[int]
        一个新列表，其中每个数字都加倍。

    ---------------------------------------------------------------------------
    """
    return [x * 2 for x in input_list]
```

# 项目编码风格指南

本文档概述了本项目的首选编码风格和原则。遵循这些指南可确保代码库的一致性、可读性和可维护性，从而反映项目在软件开发方面的独特品味和方法。本指南将项目特定约定与通用 Python 最佳实践（主要来自 PEP 8）相结合。

## 1. 一般原则

*   **清晰性和可读性：** 代码应易于理解和遵循。优先选择清晰、明确的代码，而不是巧妙或过于简洁的解决方案。
*   **可维护性：** 代码结构应便于未来的修改、调试和协作。
*   **模块化：** 组件应自包含，具有明确的职责，并尽量减少相互依赖。
*   **性能（量化重点）：** 对于量化分析，优先考虑向量化操作和高效的数据处理，通常使用 `pandas` 和 `numpy`。在存在向量化替代方案时，避免不必要的循环。

## 2. 命名约定

命名约定对于代码的可读性和一致性至关重要。本项目采用 PEP 8 和特定项目约定的混合方式。

### 2.1 类

*   **主/核心类：** 对于模块中作为主要入口点或代理的主类，使用 `main`（小写）。这是一个项目特定约定。
    *   *示例：* `class main:`
*   **配置/常量类：** 对于主要用于存储静态配置或常量值的类，使用 `ALL_CAPS`。这是一个项目特定约定。
    *   *示例：* `class DATABASE:`
*   **其他类：** 对于所有其他通用类，使用 `CapWords`（帕斯卡命名法），其中名称中的每个单词都以大写字母开头。这与 PEP 8 一致。
    *   *示例：* `class MyProcessor:`

### 2.2 函数和方法

*   函数和方法名称使用 `snake_case`（小写单词以下划线分隔）。这与 PEP 8 一致。
    *   *示例：* `process_data`、`calculate_sharpe_ratio`
*   **内部方法：** 对于类或模块内部使用的函数，使用 `__double_underscore__` 前缀（例如，`__log_activity__`、`__read__`、`__command__`）。这是一个独特的项目约定，与标准 Python 中用于内部方法的 `_single_underscore` 不同，用于明确表示这些方法是内部 API 的一部分，不应由外部代码直接调用。
    *   *示例：* `def __log_activity__(self, message: str) -> None:`

### 2.3 变量

*   变量名称使用 `snake_case`。这与 PEP 8 一致。
    *   *示例：* `total_count`、`file_path`
*   **常量（模块级别）：** 对于模块级别定义的常量，使用 `ALL_CAPS`（所有大写字母，单词以下划线分隔）。这与 PEP 8 一致。
    *   *示例：* `DEFAULT_TIMEOUT`、`MAX_RETRIES`

## 3. 代码格式

一致的代码格式可提高可读性并减少认知负担。

### 3.1 缩进

*   每个缩进级别使用 4 个空格。切勿使用制表符。这与 PEP 8 一致。

### 3.2 空行

*   顶级函数或类定义之间有**两个空行**。这与 PEP 8 一致。
*   函数/方法内部的逻辑部分周围有一个空行，以提高可读性。这与 PEP 8 一致。

### 3.3 导入

*   导入应位于文件顶部，紧随任何模块文档字符串和 `coding` 声明之后。这与 PEP 8 一致。
*   按以下顺序分组导入，并用一个空行分隔：
    1.  标准库导入（例如，`os`、`sys`）。
    2.  第三方库导入（例如，`pandas`、`numpy`）。
    3.  本地项目特定导入。
*   在每个组内，导入应按字母顺序排序。这与 PEP 8 一致。
*   避免使用通配符导入（`from module import *`）。这与 PEP 8 一致。

### 3.4 行长度

*   虽然不严格限制为 79 个字符（根据 PEP 8），但力求可读性。在适当的地方断开长行以增强清晰度。文档字符串分隔符（`===================`）是一个明确的例外，可能会超出此限制。目标是使行易于管理和阅读，而无需过多的水平滚动。
*   **函数变量断行：** 当函数变量超过 3 个（不包括 `self`、`cls` 等系统默认变量）时，根据函数命名行的实际长度考虑是否需要断行。对于 4 个或更多变量的情况，除非函数命名行特别短，一般都应考虑断行。

### 3.5 表达式和语句中的空格

*   在以下情况下避免多余的空格（与 PEP 8 一致）：
    *   紧邻括号、方括号或花括号内部。
    *   紧邻逗号、分号或冒号之前。
    *   紧邻函数调用参数列表开头的左括号之前。
    *   紧邻切片或索引开头的左方括号之前。
*   二元运算符（赋值、比较、布尔、算术）两侧始终用一个空格分隔。这与 PEP 8 一致。

## 4. 类型提示

一致且清晰的类型提示对于代码清晰度、可维护性、和启用静态分析工具至关重要。

*   **一致使用：** 所有函数参数、返回值和重要变量都应具有类型提示。这是一个强烈的项目要求。
*   **清晰性：** 尽可能使用特定类型（例如，`List[str]` 而不是 `list`，`Dict[str, Any]` 而不是 `dict`）。
*   **`Any` 的使用：** 谨慎使用 `Any`，通常用于高度通用的函数、处理缺乏精确类型信息的外部库，或者当类型复杂性超过收益时。使用 `Any` 时，考虑添加注释解释原因。
*   **推断类型：** 对于函数变量和输出，根据上下文和含义推断类型。

## 5. 面向对象编程（OOP）

本项目利用高级 OOP 原则来实现健壮和灵活的系统设计。

*   **封装：** 使用属性和方法控制对内部状态的访问，而不是直接暴露属性。
*   **继承和组合：** 在适当的情况下，优先选择组合而不是继承，特别是对于构建灵活和可重用的组件。
*   **高级模式：** 积极利用元类、`__getattr__`、`__setattr__`、`__call__` 等高级 OOP 特性来实现动态行为和代理模式。这对于数据库交互、数据源抽象以及其他需要高度灵活和可扩展设计的领域尤其重要。

## 6. 示例代码展示风格

以下代码片段概括了上述关键风格特征：

```python
# Example.py

import os
import sys
import pandas as pd
import numpy as np
from typing import Any, Dict, List

# Third-party imports
# from some_library import SomeClass

# Local project-specific imports
# from project.utils import helper_function


class CONFIG:
    """
    ===========================================================================

    Configuration class for example settings.

    This class holds static configuration values for the project.

    ---------------------------------------------------------------------------

    示例配置类。

    此类包含项目的静态配置值。

    ---------------------------------------------------------------------------
    """
    DEFAULT_VALUE: int = 10
    DATA_PATH: str = "/data/example.csv"
    MAX_RETRIES: int = 3


class main:
    """
    ===========================================================================

    Main class demonstrating the project's coding style.

    This class showcases various style elements including bilingual docstrings,
    type hinting, and specific naming conventions. It acts as a primary entry
    point or proxy for certain functionalities.

    ---------------------------------------------------------------------------

    展示项目编码风格的主类。

    此类展示了包括双语文档字符串、类型提示和特定命名约定在内的各种风格元素。
    它作为某些功能的主要入口点或代理。

    ---------------------------------------------------------------------------
    """
    def __init__(self, initial_data: pd.DataFrame) -> None:
        """
        ===========================================================================

        Initializes the ExampleProcessor with some data.

        Parameters
        ----------
        initial_data : pd.DataFrame
            The initial DataFrame to process.

        ---------------------------------------------------------------------------

        使用数据初始化 ExampleProcessor。

        参数
        ----------
        initial_data : pd.DataFrame
            要处理的初始 DataFrame。

        ---------------------------------------------------------------------------
        """
        self._data: pd.DataFrame = initial_data
        self.__log_activity__("ExampleProcessor initialized.")


    def process_data(self) -> pd.DataFrame:
        """
        ===========================================================================

        Processes the internal data.

        This method applies a simple transformation to the DataFrame,
        demonstrating vectorized operations.

        Returns
        -------
        pd.DataFrame
            The processed DataFrame.

        ---------------------------------------------------------------------------

        处理内部数据。

        此方法对 DataFrame 应用简单的转换，展示了向量化操作。

        返回
        -------
        pd.DataFrame
            处理后的 DataFrame。

        ---------------------------------------------------------------------------
        """
        print(f"Using default value: {CONFIG.DEFAULT_VALUE}")
        # Example of vectorized operation
        processed_df: pd.DataFrame = self._data * CONFIG.DEFAULT_VALUE
        return processed_df


    def __log_activity__(self, message: str) -> None:
        """
        ===========================================================================

        Logs an internal activity.

        This is an example of an internal method using double underscores,
        indicating it's part of the internal API.

        Parameters
        ----------
        message : str
            The message to log.

        ---------------------------------------------------------------------------

        记录内部活动。

        这是一个使用双下划线的内部方法示例，表示它是内部 API 的一部分。

        参数
        ----------
        message : str
            要记录的消息。

        ---------------------------------------------------------------------------
        """
        print(f"Internal Log: {message}")


def standalone_function(input_list: List[int]) -> List[int]:
    """
    ===========================================================================

    A standalone function demonstrating top-level function style.

    This function doubles each number in the input list.

    ---------------------------------------------------------------------------

    一个展示顶级函数风格的独立函数。

    此函数将输入列表中的每个数字加倍。

    ---------------------------------------------------------------------------

    Parameters
    ----------
    input_list : List[int]
        A list of integers.

    ---------------------------------------------------------------------------

    参数
    ----------
    input_list : List[int]
        一个整数列表。

    ---------------------------------------------------------------------------

    Returns
    -------
    List[int]
        A new list with each number doubled.

    ---------------------------------------------------------------------------

    返回
    -------
    List[int]
        一个新列表，其中每个数字都加倍。

    ---------------------------------------------------------------------------
    """
    return [x * 2 for x in input_list]
