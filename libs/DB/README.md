# `DB` Module Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction

The `DB` module provides a robust and unified abstraction layer for interacting with various database systems, currently supporting DuckDB and MySQL. Its primary purpose is to offer a consistent interface for common database operations such as reading, writing, executing commands, retrieving schema information, and managing tables, regardless of the underlying database technology. This module simplifies database interactions by handling data type translations and dynamically propagating operations to the active database instance, thereby enhancing code reusability and maintainability across different data sources.

## File and Module Structure

```
DB/
├── config.py               # Database connection configurations (MySQL, DuckDB)
├── __data_type__/
│   └── main.py             # Data type translation logic (e.g., Python types to DB types)
├── __database_struct__/
│   ├── common_metaclass.py # Metaclass for attribute propagation
│   ├── main.py             # Main DB abstraction layer, dynamic proxy to DB instances
│   ├── DuckDB.py           # DuckDB specific implementations of DB operations
│   ├── MySQL.py            # MySQL specific implementations of DB operations
│   └── meta.py             # Base class for DB handlers, parameter management, timing decorators
```

## Module Overview and Architecture

The `DB` module is designed to provide a seamless and unified interface for interacting with different database backends. Its architecture is centered around a dynamic proxy mechanism that abstracts away the specifics of each database system.

Key components and their interactions:
*   `DB.config`: Stores all necessary connection parameters and default settings for each supported database (MySQL, DuckDB).
*   `DB.__data_type__`: Handles the translation of generic data types to the specific data types required by each database dialect.
*   `DB.__database_struct__.meta`: Serves as the foundational base class, providing common functionalities such as parameter merging, instance renewal, and a timing decorator for performance monitoring. It also defines the abstract interface for database operations.
*   `DB.__database_struct__.common_metaclass`: Implements `AutoPropagateMeta`, a metaclass crucial for enabling the dynamic propagation of attributes and methods from the underlying database instances to the main `DB` abstraction class.
*   `DB.__database_struct__.main`: This is the core abstraction layer. It acts as a dynamic proxy, intelligently routing method calls and attribute access to the currently selected active database instance (either DuckDB or MySQL). This dynamic routing is facilitated by the `AutoPropagateMeta` and a setup decorator.
*   `DB.__database_struct__.DuckDB` and `DB.__database_struct__.MySQL`: These modules contain the concrete implementations of all database operations, tailored specifically for DuckDB and MySQL, respectively. They override the placeholder methods defined in `meta.py`.

```
+-------------------+
|  DB.config        |
|  (MySQL, DuckDB)  |
+---------+---------+
          |
          v
+-------------------+
|  DB.__data_type__ |
|  (main.py)        |
+---------+---------+
          |
          v
+-------------------------------------------------------------------+
|  DB.__database_struct__.meta                                      |
|  (Base functionalities: parameter management, timing, abstract ops)|
+---------+---------------------------------------------------------+
          |
          v
+-------------------------------------------------------------------+
|  DB.__database_struct__.common_metaclass                          |
|  (AutoPropagateMeta: enables dynamic attribute propagation)       |
+---------+---------------------------------------------------------+
          |
          v
+-------------------------------------------------------------------+
|  DB.__database_struct__.main                                      |
|  (Dynamic Proxy: routes calls to active DB instance)              |
+---------+---------------------------------------------------------+
          |
          v
+-------------------+   +-------------------+
|  DB.__database_struct__.DuckDB  |   |  DB.__database_struct__.MySQL   |
|  (DuckDB specific impl.)  |   |  (MySQL specific impl.)   |
+-------------------+   +-------------------+
```

## Purpose of Each Module

*   `config.py`: This module centralizes all configuration parameters required for connecting to and interacting with different database systems (MySQL, DuckDB). It defines connection strings, default ports, credentials, and other database-specific settings, ensuring easy management and modification of database access details.
*   `__data_type__/main.py`: Responsible for the crucial task of data type translation. It maps generic data types used within the application to the specific, compatible data types of the chosen database dialect (e.g., converting a Python `int` to an appropriate `INT` type for MySQL or DuckDB). This ensures data integrity and compatibility across various database backends.
*   `__database_struct__/common_metaclass.py`: Defines `AutoPropagateMeta`, a custom metaclass. Its primary role is to facilitate dynamic attribute propagation, allowing the main `DB` abstraction class to seamlessly expose and forward calls to methods and attributes of the underlying active database instance. This enables a flexible and extensible design.
*   `__database_struct__/main.py`: This is the core of the `DB` module's abstraction. It acts as a dynamic proxy, intelligently intercepting method calls and attribute accesses and then routing them to the currently selected database backend (either DuckDB or MySQL). It leverages `AutoPropagateMeta` and a setup decorator to achieve this dynamic dispatch, providing a unified API to the user.
*   `__database_struct__/DuckDB.py`: Contains the concrete implementations of all standard database operations specifically for DuckDB. This includes methods for creating database engines, executing raw SQL commands, reading data into Pandas DataFrames, writing DataFrames to tables, retrieving schema information, checking table existence, and creating/dropping tables.
*   `__database_struct__/MySQL.py`: Similar to `DuckDB.py`, this module provides the concrete implementations of all standard database operations, but tailored for MySQL. It handles MySQL-specific connection details, SQL syntax variations, and data handling, ensuring seamless interaction with MySQL databases through the unified `DB` interface.
*   `__database_struct__/meta.py`: Defines the `meta` base class, which serves as a foundational blueprint for all database handler implementations. It provides common utilities such as `__parameters__` for merging configuration parameters, `__call__` for instance renewal, and a `__timing_decorator__` for performance measurement. It also declares abstract placeholder methods for database operations that must be implemented by concrete database-specific classes (like `DuckDB.py` and `MySQL.py`).

## Other Helpful Information

### Quick Start / Usage Example

To use the `DB` module, you can instantiate the main class and then interact with it as if it were a direct database connection. You can switch between different database sources dynamically.

```python
from libs.DB.__database_struct__.main import main as DB

# Initialize with the default recommended source (e.g., 'DuckDB' from config)
db_instance = DB()

# You can explicitly set the source
# db_instance.source = 'MySQL'

# Example: Execute a command (e.g., create a table)
# For DuckDB, this might create a table in the specified schema
db_instance.command("CREATE TABLE my_schema.my_table (id INTEGER, name VARCHAR);")

# Example: Write a Pandas DataFrame to a table
import pandas as pd
data = {'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie']}
df = pd.DataFrame(data)
db_instance.write(df, table='my_table', schema='my_schema', if_exists='replace')

# Example: Read data from a table
read_df = db_instance.read(table='my_table', schema='my_schema')
print("Read DataFrame:")
print(read_df)

# Example: Get schema information
schema_info_df = db_instance.schema_info()
print("\nSchema Information:")
print(schema_info_df)

# Example: Check if a table exists
table_exists = db_instance.table_exist(table='my_table', schema='my_schema')
print(f"\nDoes 'my_table' exist in 'my_schema'? {table_exists}")

# Example: Drop a table
db_instance.drop_table(table='my_table', schema='my_schema')
table_exists_after_drop = db_instance.table_exist(table='my_table', schema='my_schema')
print(f"Does 'my_table' exist after drop? {table_exists_after_drop}")
```

### Core Concepts and Design Philosophy

The `DB` module is built upon the principles of:
*   **Database Abstraction**: Providing a high-level, unified API that hides the complexities and differences of various underlying database systems.
*   **Dynamic Proxying**: Utilizing Python's dynamic features (metaclasses, `__getattr__`, `__setattr__`) to route operations to the appropriate database backend at runtime, based on the active source.
*   **Configuration-Driven**: Database connection details and default behaviors are managed through a centralized configuration module (`config.py`), allowing for easy modification and environment-specific setups.
*   **Bilingual Documentation**: All key documentation, including this README, is provided in both English and Chinese to support a diverse development team.

### Contribution Guide

Contributions are welcome! To extend or contribute to the `DB` module:
1.  Familiarize yourself with the existing database implementations (e.g., `DuckDB.py`, `MySQL.py`).
2.  For new database support, create a new module within `__database_struct__` that inherits from `meta.py` and implements all abstract database operations.
3.  Update `DB.__database_struct__.main.py` and `DB.config.py` to integrate the new database.
4.  Ensure all new code adheres to the `code_standards_new.md` and all documentation follows `readme_standards.md`.

### Known Limitations or Common Pitfalls

*   **Performance for Extremely Large DataFrames**: While `to_sql` with `chunksize` is used for writing, for extremely large DataFrames (e.g., billions of rows), direct bulk loading utilities specific to each database might offer better performance than the current SQLAlchemy-based approach.
*   **Complex SQL Queries**: While `command` allows raw SQL, for very complex or highly optimized queries, direct interaction with the underlying database's native client might be necessary to leverage all its features. The abstraction aims for common use cases.

---

# `DB` 模块文档

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 简介

`DB` 模块提供了一个健壮且统一的抽象层，用于与各种数据库系统进行交互，目前支持 DuckDB 和 MySQL。其主要目的是为常见的数据库操作（如读取、写入、执行命令、检索模式信息以及管理表）提供一致的接口，而无需关心底层数据库技术。该模块通过处理数据类型转换和将操作动态传播到活动数据库实例，从而简化了数据库交互，提高了不同数据源之间的代码重用性和可维护性。

## 文件和模块结构

```
DB/
├── config.py               # 数据库连接配置 (MySQL, DuckDB)
├── __data_type__/
│   └── main.py             # 数据类型转换逻辑 (例如，Python 类型到数据库类型)
├── __database_struct__/
│   ├── common_metaclass.py # 属性传播的元类
│   ├── main.py             # 主要数据库抽象层，数据库实例的动态代理
│   ├── DuckDB.py           # DuckDB 数据库操作的具体实现
│   ├── MySQL.py            # MySQL 数据库操作的具体实现
│   └── meta.py             # 数据库处理器的基类，参数管理，计时装饰器
```

## 模块概览与架构

`DB` 模块旨在为与不同数据库后端交互提供无缝且统一的接口。其架构围绕一个动态代理机制构建，该机制抽象了每个数据库系统的具体细节。

关键组件及其交互：
*   `DB.config`：存储每个受支持数据库（MySQL、DuckDB）所需的所有连接参数和默认设置。 
*   `DB.__data_type__`：负责将应用程序中使用的通用数据类型转换为每个数据库方言所需的特定数据类型。
*   `DB.__database_struct__.meta`：作为基础基类，提供通用功能，如参数合并、实例更新以及用于性能监控的计时装饰器。它还定义了数据库操作的抽象接口。
*   `DB.__database_struct__.common_metaclass`：实现了 `AutoPropagateMeta`，这是一个关键的元类，用于将底层数据库实例的属性和方法动态传播到主要的 `DB` 抽象类。 
*   `DB.__database_struct__.main`：这是 `DB` 模块抽象的核心。它充当动态代理，智能地拦截方法调用和属性访问，然后将它们路由到当前选定的活动数据库实例（DuckDB 或 MySQL）。这种动态路由由 `AutoPropagateMeta` 和一个设置装饰器促进。
*   `DB.__database_struct__.DuckDB` 和 `DB.__database_struct__.MySQL`：这些模块包含所有数据库操作的具体实现，分别针对 DuckDB 和 MySQL 进行定制。它们覆盖了 `meta.py` 中定义的占位符方法。

```
+-------------------+
|  DB.config        |
|  (MySQL, DuckDB)  |
+---------+---------+
          |
          v
+-------------------+
|  DB.__data_type__ |
|  (main.py)        |
+---------+---------+
          |
          v
+-------------------------------------------------------------------+
|  DB.__database_struct__.meta                                      |
|  (基础功能：参数管理、计时、抽象操作)                               |
+---------+---------------------------------------------------------+
          |
          v
+-------------------------------------------------------------------+
|  DB.__database_struct__.common_metaclass                          |
|  (AutoPropagateMeta：启用动态属性传播)                            |
+---------+---------------------------------------------------------+
          |
          v
+-------------------------------------------------------------------+
|  DB.__database_struct__.main                                      |
|  (动态代理：将调用路由到活动数据库实例)                           |
+---------+---------------------------------------------------------+
          |
          v
+-------------------+   +-------------------+
|  DB.__database_struct__.DuckDB  |   |  DB.__database_struct__.MySQL   |
|  (DuckDB 具体实现)  |   |  (MySQL 具体实现)   |
+-------------------+   +-------------------+
```

## 各个模块的用途

*   `config.py`：该模块集中管理连接和与不同数据库系统（MySQL、DuckDB）交互所需的所有配置参数。它定义了连接字符串、默认端口、凭据以及其他特定于数据库的设置，确保数据库访问详细信息的轻松管理和修改。
*   `__data_type__/main.py`：负责数据类型转换的关键任务。它将应用程序中使用的通用数据类型映射到所选数据库方言的特定兼容数据类型（例如，将 Python 的 `int` 转换为 MySQL 或 DuckDB 适当的 `INT` 类型）。这确保了跨各种数据库后端的数据完整性和兼容性。
*   `__database_struct__/common_metaclass.py`：定义了 `AutoPropagateMeta`，一个自定义元类。其主要作用是促进动态属性传播，允许主要的 `DB` 抽象类无缝地公开和转发对底层活动数据库实例的方法和属性的调用。这实现了灵活和可扩展的设计。
*   `__database_struct__/main.py`：这是 `DB` 模块抽象的核心。它充当动态代理，智能地拦截方法调用和属性访问，然后将它们路由到当前选定的数据库后端（DuckDB 或 MySQL）。它利用 `AutoPropagateMeta` 和一个设置装饰器来实现这种动态分派，为用户提供统一的 API。
*   `__database_struct__/DuckDB.py`：包含专门针对 DuckDB 的所有标准数据库操作的具体实现。这包括用于创建数据库引擎、执行原始 SQL 命令、将数据读取到 Pandas DataFrame、将 DataFrame 写入表、检索模式信息、检查表是否存在以及创建/删除表的方法。
*   `__database_struct__/MySQL.py`：与 `DuckDB.py` 类似，该模块提供了所有标准数据库操作的具体实现，但针对 MySQL 进行了定制。它处理 MySQL 特定的连接详细信息、SQL 语法变体和数据处理，确保通过统一的 `DB` 接口与 MySQL 数据库无缝交互。
*   `__database_struct__/meta.py`：定义了 `meta` 基类，作为所有数据库处理程序实现的基础蓝图。它提供了通用实用程序，例如用于合并配置参数的 `__parameters__`、用于实例更新的 `__call__` 以及用于性能测量的 `__timing_decorator__`。它还声明了必须由具体数据库特定类（如 `DuckDB.py` 和 `MySQL.py`）实现的数据库操作的抽象占位符方法。

## 其他有用的信息

### 快速上手 / 用法示例

要使用 `DB` 模块，您可以实例化主类，然后像直接数据库连接一样与其交互。您可以在不同的数据库源之间动态切换。

```python
from libs.DB.__database_struct__.main import main as DB

# 使用默认推荐源（例如，来自配置的 'DuckDB'）进行初始化
db_instance = DB()

# 您可以显式设置源
# db_instance.source = 'MySQL'

# 示例：执行命令（例如，创建表）
# 对于 DuckDB，这可能会在指定的模式中创建表
db_instance.command("CREATE TABLE my_schema.my_table (id INTEGER, name VARCHAR);")

# 示例：将 Pandas DataFrame 写入表
import pandas as pd
data = {'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie']}
df = pd.DataFrame(data)
db_instance.write(df, table='my_table', schema='my_schema', if_exists='replace')

# 示例：从表中读取数据
read_df = db_instance.read(table='my_table', schema='my_schema')
print("Read DataFrame:")
print(read_df)

# 示例：获取模式信息
schema_info_df = db_instance.schema_info()
print("\nSchema Information:")
print(schema_info_df)

# 示例：检查表是否存在
table_exists = db_instance.table_exist(table='my_table', schema='my_schema')
print(f"\nDoes 'my_table' exist in 'my_schema'? {table_exists}")

# 示例：删除表
db_instance.drop_table(table='my_table', schema='my_schema')
table_exists_after_drop = db_instance.table_exist(table='my_table', schema='my_schema')
print(f"Does 'my_table' exist after drop? {table_exists_after_drop}")
```

### 核心概念与设计哲学

`DB` 模块建立在以下原则之上：
*   **数据库抽象**：提供一个高级的、统一的 API，隐藏各种底层数据库系统的复杂性和差异。
*   **动态代理**：利用 Python 的动态特性（元类、`__getattr__`、`__setattr__`）在运行时将操作路由到适当的数据库后端，基于活动源。
*   **配置驱动**：数据库连接详细信息和默认行为通过集中的配置模块（`config.py`）进行管理，便于轻松修改和针对特定环境的设置。
*   **双语文档**：所有关键文档，包括本 README，均提供英文和中文版本，以支持多元化的开发团队。

### 贡献指南

欢迎贡献！要扩展或贡献 `DB` 模块：
1.  熟悉现有的数据库实现（例如，`DuckDB.py`、`MySQL.py`）。
2.  对于新的数据库支持，在 `__database_struct__` 中创建一个新模块，该模块继承自 `meta.py` 并实现所有抽象数据库操作。
3.  更新 `DB.__database_struct__.main.py` 和 `DB.config.py` 以集成新的数据库。
4.  确保所有新代码符合 `code_standards.md`，并且所有文档遵循 `readme_standards.md`。

### 已知限制或常见陷阱

*   **极大数据帧的性能**：虽然使用 `to_sql` 和 `chunksize` 进行写入，但对于极大的数据帧（例如，数十亿行），特定于每个数据库的直接批量加载工具可能比当前基于 SQLAlchemy 的方法提供更好的性能。
*   **复杂 SQL 查询**：虽然 `command` 允许原始 SQL，但对于非常复杂或高度优化的查询，可能需要直接与底层数据库的本机客户端交互，以利用其所有功能。抽象旨在满足常见用例。
