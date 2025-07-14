# Code Standardization Guidelines (PEP 8 Enhanced)

This document outlines the code standardization rules to be followed. The goal is to ensure consistency, readability, and maintainability across the codebase. This version integrates the official PEP 8 style guide with our project-specific requirements.

## 1. General Principles

*   **Respect Existing Standards:** Always adhere to the original code's conventions, including existing comment styles, coding paradigms, and formatting. When in doubt, observe the surrounding code.
*   **No In-Place Changes:** All modifications must be saved to a new file with a `_new` suffix (e.g., `original.py` becomes `original_new.py`). The original file must remain untouched.
*   **Skipping Files:** `__init__.py` files and files containing only header comments (empty content) should be skipped.

## 2. Code Layout (PEP 8)

*   **Indentation**: Use **4 spaces** per indentation level. Do not use tabs.
*   **Line Length**: Limit all lines to a maximum of **79 characters**.
*   **Line Breaks**: For long lines, break them using Python's implied line continuation inside parentheses, brackets, and braces. If necessary, use a backslash (`\`).
*   **Blank Lines**:
    *   Top-level function and class definitions: **Two** blank lines.
    *   Method definitions inside a class: **One** blank line.
    *   Use blank lines sparingly inside functions to separate logical sections.

## 3. Imports (PEP 8)

*   Imports should always be at the **top of the file**, just after any module comments and docstrings.
*   Imports should be grouped in the following order, with a blank line between each group:
    1.  Standard library imports (e.g., `os`, `sys`).
    2.  Related third-party imports (e.g., `numpy`, `pandas`).
    3.  Local application/library specific imports.
*   Use **absolute imports** whenever possible (e.g., `from myapp.utils import my_function`).
*   Avoid wildcard imports (`from module import *`).

## 4. Whitespace in Expressions and Statements (PEP 8)

*   **Binary Operators**: Always surround these with a single space on either side: `assignment (=)`, `augmented assignment (+=, -= etc.)`, `comparisons (==, <, >, !=, <=, >=, in, not in, is, is not)`, `Booleans (and, or, not)`.
*   **Commas**: A space should follow a comma, but not precede it.
*   **Function Calls**: No whitespace immediately inside parentheses: `my_function(arg1, arg2)`.
*   **Default Parameter Values**: No spaces around the `=` sign when used to indicate a keyword argument or a default parameter value.

## 5. Commenting Standards (Project Specific)

All new comments, especially for functions and classes, must follow our specific bilingual format.

### 5.1 Function Comment Style

This style is mandatory for all functions.

```python
def example_function(
    param1: str,
    param2: int = 0,
    *args: any,
    **kwargs: any
) -> dict:
    """
    ===========================================================================

    English summary of the function's purpose.

    Parameters
    ----------
    param1 : str
        English description of param1.
    param2 : int, optional
        English description of param2. Defaults to 0.
    *args : any
        English description of positional arguments.
    **kwargs : any
        English description of keyword arguments.

    Returns
    -------
    dict
        English description of the return value.

    ---------------------------------------------------------------------------

    中文函数目的概述。

    参数
    ----------
    param1 : str
        param1的中文描述。
    param2 : int, optional
        param2的中文描述。默认为 0。
    *args : any
        位置参数的中文描述。
    **kwargs : any
        关键字参数的中文描述。

    返回
    -------
    dict
        返回值的中文描述。

    ---------------------------------------------------------------------------
    """
    # Function implementation
    pass
```

### 5.2 Class Comment Style

This style is mandatory for all classes.

```python
class ExampleClass:
    """
    ===========================================================================

    English summary of the class's purpose.

    ---------------------------------------------------------------------------

    中文类目的概述。

    ---------------------------------------------------------------------------
    """
    def __init__(self, param1: str, param2: int):
        # Constructor implementation
        pass
```

### 5.3 Inline Comments

*   Use sparingly.
*   Focus on **why** something is done, not **what**.
*   Should be bilingual if explaining complex logic.
*   (PEP 8) An inline comment is a comment on the same line as a statement. They should be separated by at least **two spaces** from the statement.

## 6. Code Formatting (Project Specific & PEP 8)

*   **Function Parameters:** Each parameter in a function definition **must** be on a new line, following the format `parameter: type = value`. This is a strict project-specific rule.
*   **Type Hinting:** All function parameters and return values **must** have explicit type hints.
*   **Complex Logic:** For complex one-line expressions, break them into multiple lines for clarity. Add a bilingual comment above the statement to explain its function and purpose.

---

# 代码规范指南 (PEP 8 增强版)

本文档概述了需要遵循的代码规范化规则。目标是确保整个代码库的一致性、可读性和可维护性。本版本将官方 PEP 8 风格指南与我们项目的特定要求相结合。

## 1. 通用原则

*   **尊重现有标准:** 始终遵循原始代码的约定，包括现有的注释风格、编码范式和格式。如有疑问，请观察周围的代码。
*   **禁止原地修改:** 所有修改都必须保存到带有 `_new` 后缀的新文件中（例如，`original.py` 变为 `original_new.py`）。必须保持原始文件不变。
*   **跳过文件:** `__init__.py` 文件和仅包含头部注释（内容为空）的文件应被跳过。

## 2. 代码布局 (PEP 8)

*   **缩进**: 每个缩进级别使用 **4个空格**。不要使用制表符 (Tab)。
*   **行长度**: 所有行的最大长度限制为 **79个字符**。
*   **换行**: 对于长行，应使用 Python 在括号、方括号和花括号内的隐式行连续来断行。如果需要，可以使用反斜杠 (`\`)。
*   **空行**:
    *   顶层函数和类的定义: **两**个空行。
    *   类内部的方法定义: **一**个空行。
    *   在函数内部谨慎使用空行来分隔逻辑段落。

## 3. 导入 (PEP 8)

*   导入语句应始终位于**文件顶部**，仅次于任何模块注释和文档字符串。
*   导入应按以下顺序分组，每组之间用一个空行分隔：
    1.  标准库导入 (例如, `os`, `sys`)。
    2.  相关的第三方库导入 (例如, `numpy`, `pandas`)。
    3.  本地应用程序/库的特定导入。
*   尽可能使用**绝对导入** (例如, `from myapp.utils import my_function`)。
*   避免使用通配符导入 (`from module import *`)。

## 4. 表达式和语句中的空格 (PEP 8)

*   **二元运算符**: 两侧始终使用一个空格：`赋值 (=)`, `增强赋值 (+=, -= 等)`, `比较 (==, <, >, !=, <=, >=, in, not in, is, is not)`, `布尔运算 (and, or, not)`。
*   **逗号**: 逗号后应有一个空格，但前面不应有。
*   **函数调用**: 括号内紧邻内容，不加空格: `my_function(arg1, arg2)`。
*   **默认参数值**: 当用于指示关键字参数或默认参数值时，`=` 号周围不加空格。

## 5. 注释标准 (项目特定)

所有新注释，特别是针对函数和类的注释，都必须遵循我们特定的双语格式。

### 5.1 函数注释风格

此风格对所有函数都是强制性的。

```python
# 此处为与英文版相同的Python代码示例
```

### 5.2 类注释风格

此风格对所有类都是强制性的。

```python
# 此处为与英文版相同的Python代码示例
```

### 5.3 行内注释

*   谨慎使用。
*   专注于解释**为什么**这么做，而不是**做什么**。
*   如果解释复杂逻辑，应使用双语。
*   (PEP 8) 行内注释是与语句位于同一行的注释。它们应与语句之间至少隔开**两个空格**。

## 6. 代码格式化 (项目特定 & PEP 8)

*   **函数参数:** 函数定义中的每个参数**必须**位于新的一行，遵循 `参数: 类型 = 值` 的格式。这是严格的项目特定规则。
*   **类型提示:** 所有函数参数和返回值的类型**必须**有明确的类型提示。
*   **复杂逻辑:** 对于复杂的单行表达式，应将其分解为多行以提高清晰度。在语句上方添加双语注释以解释其功能和目的。
