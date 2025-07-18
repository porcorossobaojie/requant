# `DB` Module Documentation

[![Build Status](https://img.shields.io/travis/user/repo.svg)](https://travis-ci.org/user/repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction

The `DB` module provides a robust and extensible framework for interacting with various database systems, primarily focusing on MySQL and DuckDB. It encapsulates database connection logic, data type translation, and common database operations, ensuring a consistent and efficient approach to data management within the project.

## File and Module Structure

```
DB/
├── __init__.py
├── config.py               # Database connection configurations
├── README.md               # This documentation
├── __data_type__/
│   ├── __init__.py
│   └── main.py             # Data type translation (e.g., generic to MySQL/DuckDB types)
│       # - MySQL: Defines MySQL specific data types
│       # - DuckDB: Defines DuckDB specific data types
│       # - main: Translates data types based on database
└── __database_struct__/
    ├── __init__.py
    ├── DuckDB.py           # DuckDB database operations (inherits from meta.main)
    │   # - main: Handles DuckDB specific operations (read, write, create table, etc.)
    ├── main.py             # (Placeholder/Entry point if needed)
    ├── meta.py             # Base class for database operations (provides common methods)
    │   # - main: Base class for MySQL.main and DuckDB.main
    └── MySQL.py            # MySQL database operations (inherits from meta.main)
        # - main: Handles MySQL specific operations (read, write, create table, etc.)
```

## Module Overview and Architecture

The `DB` module is structured to provide a clear separation of concerns, with dedicated sub-modules for configuration, data type handling, and database-specific operations.

### Configuration Relationships

The `config.py` file centralizes database connection parameters. It leverages external login information defined in `local.login_info` to securely manage credentials.

```
+-----------------------+
| local.login_info      |
| (e.g., DB_LOGIN_INFO) |
+-----------+-----------+
            |
            v
+-----------------------+
| DB/config.py          |
| - class MySQL         |
| - class DuckDB        |
+-----------------------+
```

### Class Inheritance Hierarchy

The core database operation classes (`MySQL.main` and `DuckDB.main`) inherit from a common base class (`meta.main`), which provides shared functionalities like parameter handling and timing decorators. This promotes code reusability and consistency across different database implementations.

```
+-----------------------------------+
| DB/__database_struct__/meta.py    |
| - class main                      |
|   (Base class for DB operations)  |
+-----------------+-----------------+
                  |
      +-----------+-----------+
      |                       |
      v                       v
+-------------------+   +-------------------+
| DB/__database_struct__/MySQL.py | DB/__database_struct__/DuckDB.py |
| - class main      |   | - class main      |
|   (MySQL operations)  |   |   (DuckDB operations) |
+-------------------+   +-------------------+
```

### Data Type Translation Integration

The `__data_type__/main.py` module provides a mechanism for translating generic data types into database-specific types. This `data_trans` utility is then utilized by both `MySQL.main` and `DuckDB.main` to ensure proper type mapping during database interactions.

```
+-----------------------------------+
| DB/__data_type__/main.py          |
| - class main (data_trans)         |
|   (Translates data types)         |
+-----------------+-----------------+
                  |
      +-----------+-----------+
      |                       |
      v                       v
+-------------------+   +-------------------+
| DB/__database_struct__/MySQL.py | DB/__database_struct__/DuckDB.py |
| - class main      |   | - class main      |
|   (Uses data_trans)   |   |   (Uses data_trans)   |
+-------------------+   +-------------------+
```

## Purpose of Each Module

*   **`config.py`**: Defines the configuration settings for connecting to different database types (MySQL, DuckDB), inheriting from `local.login_info` for sensitive credentials.
*   **`__data_type__/main.py`**: Manages the translation of generic data types to specific database data types (e.g., `INT` to `TINYINT` for MySQL). It provides `MySQL` and `DuckDB` classes that hold the specific type mappings.
*   **`__database_struct__/meta.py`**: Serves as the abstract base class for all database interaction modules. It provides common functionalities such as parameter handling, timing decorators, and a framework for database operations.
*   **`__database_struct__/MySQL.py`**: Implements the concrete operations for MySQL databases, including environment initialization, command execution, data reading, and table management. It extends `meta.main` and utilizes `__data_type__.main` for type conversions.
*   **`__database_struct__/DuckDB.py`**: Implements the concrete operations for DuckDB databases, mirroring the functionalities of `MySQL.py` but adapted for DuckDB. It also extends `meta.main` and utilizes `__data_type__.main`.

## Other Helpful Information

### Quick Start / Usage Example (Conceptual)

While a runnable example requires specific database setup, here's a conceptual outline of how you might use the `DB` module:

```python
from libs.DB.config import MySQL, DuckDB
from libs.DB.__database_struct__.MySQL import main as MySQLDB
from libs.DB.__database_struct__.DuckDB import main as DuckDB

# Example: Using MySQL
mysql_config = MySQL() # Inherits from local.login_info.DB_LOGIN_INFO.MySQL
mysql_db = MySQLDB(
    host=mysql_config.host,
    port=mysql_config.port,
    user=mysql_config.user,
    password=mysql_config.password,
    schema="my_database"
)

# Initialize environment (create schema if not exists)
mysql_db.__env_init__()

# Create a table
columns_definition = {
    "id": ["INT", "Primary key"],
    "name": ["VARCHAR(255)", "User name"],
    "age": ["INT", "User age"]
}
mysql_db.__create_table__(table="users", columns=columns_definition, primary_key="id")

# Write data
import pandas as pd
data = {"id": [1, 2], "name": ["Alice", "Bob"], "age": [30, 24]}
df = pd.DataFrame(data)
mysql_db.__write__(df_obj=df, table="users", if_exists="append")

# Read data
read_df = mysql_db.__read__(table="users", columns="*")
print(read_df)

# Example: Using DuckDB (similar pattern)
duckdb_config = DuckDB() # Inherits from local.login_info.DB_LOGIN_INFO.DuckDB
duck_db = DuckDB(
    path=duckdb_config.path,
    database=duckdb_config.database,
    schema="my_duckdb_database"
)

# ... similar operations for DuckDB ...
```

### Core Concepts and Design Philosophy

*   **Abstraction**: The module abstracts away the complexities of direct database interactions, providing a consistent API for different database systems.
*   **Configuration-Driven**: Database connection details and other configurations are managed centrally in `config.py`, allowing for easy modification and environment-specific settings.
*   **Inheritance for Reusability**: A clear inheritance hierarchy (`meta.main` as base) ensures that common database operations are defined once and reused across specific database implementations.
*   **Type Safety and Translation**: The `__data_type__` module ensures that data types are correctly mapped between generic Python types and database-specific types, reducing potential errors.
*   **Modularity**: The module is broken down into logical sub-modules, making it easier to understand, maintain, and extend.

---

# `DB` 模块文档

## 简介

`DB` 模块提供了一个健壮且可扩展的框架，用于与各种数据库系统进行交互，主要关注 MySQL 和 DuckDB。它封装了数据库连接逻辑、数据类型转换和常见的数据库操作，确保了项目内部数据管理的一致性和高效性。

## 文件和模块结构

```
DB/
├── __init__.py
├── config.py               # 数据库连接配置
├── README.md               # 本文档
├── __data_type__/
│   ├── __init__.py
│   └── main.py             # 数据类型转换（例如，通用类型到 MySQL/DuckDB 类型）
│       # - MySQL: 定义 MySQL 特定的数据类型
│       # - DuckDB: 定义 DuckDB 特定的数据类型
│       # - main: 根据数据库类型转换数据类型
└── __database_struct__/
    ├── __init__.py
    ├── DuckDB.py           # DuckDB 数据库操作（继承自 meta.main）
    │   # - main: 处理 DuckDB 特定的操作（读取、写入、创建表等）
    ├── main.py             # （如果需要，作为占位符/入口点）
    ├── meta.py             # 数据库操作的基类（提供通用方法）
    │   # - main: MySQL.main 和 DuckDB.main 的基类
    └── MySQL.py            # MySQL 数据库操作（继承自 meta.main）
        # - main: 处理 MySQL 特定的操作（读取、写入、创建表等）
```

## 模块概览与架构

`DB` 模块的结构旨在提供清晰的职责分离，为配置、数据类型处理和特定数据库操作提供了专门的子模块。

### 配置关系

`config.py` 文件集中管理数据库连接参数。它利用 `local.login_info` 中定义的外部登录信息来安全地管理凭据。

```
+-----------------------+
| local.login_info      |
| （例如，DB_LOGIN_INFO） |
+-----------+-----------+
            |
            v
+-----------------------+
| DB/config.py          |
| - class MySQL         |
| - class DuckDB        |
+-----------------------+
```

### 类继承层次结构

核心数据库操作类（`MySQL.main` 和 `DuckDB.main`）继承自一个共同的基类（`meta.main`），该基类提供了参数处理和计时装饰器等共享功能。这促进了不同数据库实现之间的代码重用和一致性。

```
+-----------------------------------+
| DB/__database_struct__/meta.py    |
| - class main                      |
|   （数据库操作的基类）             |
+-----------------+-----------------+
                  |
      +-----------+-----------+
      |                       |
      v                       v
+-------------------+   +-------------------+
| DB/__database_struct__/MySQL.py | DB/__database_struct__/DuckDB.py |
| - class main      |   | - class main      |
|   （MySQL 操作）      |   |   （DuckDB 操作）     |
+-------------------+   +-------------------+
```

### 数据类型转换集成

`__data_type__/main.py` 模块提供了一种将通用数据类型转换为特定数据库类型（`data_trans`）的机制。`MySQL.main` 和 `DuckDB.main` 都使用了这个 `data_trans` 工具，以确保在数据库交互过程中进行正确的类型映射。

```
+-----------------------------------+
| DB/__data_type__/main.py          |
| - class main (data_trans)         |
|   （转换数据类型）                 |
+-----------------+-----------------+
                  |
      +-----------+-----------+
      |                       |
      v                       v
+-------------------+   +-------------------+
| DB/__database_struct__/MySQL.py | DB/__database_struct__/DuckDB.py |
| - class main      |   | - class main      |
|   （使用 data_trans） |   |   （使用 data_trans） |
+-------------------+   +-------------------+
```

## 各个模块的用途

*   **`config.py`**: 定义连接不同数据库类型（MySQL、DuckDB）的配置设置，从 `local.login_info` 继承敏感凭据。
*   **`__data_type__/main.py`**: 管理通用数据类型到特定数据库数据类型（例如，`INT` 到 MySQL 的 `TINYINT`）的转换。它提供了包含特定类型映射的 `MySQL` 和 `DuckDB` 类。
*   **`__database_struct__/meta.py`**: 作为所有数据库交互模块的抽象基类。它提供通用功能，如参数处理、计时装饰器和数据库操作框架。
*   **`__database_struct__/MySQL.py`**: 实现 MySQL 数据库的具体操作，包括环境初始化、命令执行、数据读取和表管理。它扩展了 `meta.main` 并利用 `__data_type__.main` 进行类型转换。
*   **`__database_struct__/DuckDB.py`**: 实现 DuckDB 数据库的具体操作，与 `MySQL.py` 的功能类似，但适用于 DuckDB。它也扩展了 `meta.main` 并利用 `__data_type__.main`。

## 其他有用的信息

### 快速上手 / 用法示例（概念性）

虽然可运行的示例需要特定的数据库设置，但这里是您可能如何使用 `DB` 模块的概念性概述：

```python
from libs.DB.config import MySQL, DuckDB
from libs.DB.__database_struct__.MySQL import main as MySQLDB
from libs.DB.__database_struct__.DuckDB import main as DuckDB

# 示例：使用 MySQL
mysql_config = MySQL() # 继承自 local.login_info.DB_LOGIN_INFO.MySQL
mysql_db = MySQLDB(
    host=mysql_config.host,
    port=mysql_config.port,
    user=mysql_config.user,
    password=mysql_config.password,
    schema="my_database"
)

# 初始化环境（如果模式不存在则创建）
mysql_db.__env_init__()

# 创建表
columns_definition = {
    "id": ["INT", "Primary key"],
    "name": ["VARCHAR(255)", "User name"],
    "age": ["INT", "User age"]
}
mysql_db.__create_table__(table="users", columns=columns_definition, primary_key="id")

# 写入数据
import pandas as pd
data = {"id": [1, 2], "name": ["Alice", "Bob"], "age": [30, 24]}
df = pd.DataFrame(data)
mysql_db.__write__(df_obj=df, table="users", if_exists="append")

# 读取数据
read_df = mysql_db.__read__(table="users", columns="*")
print(read_df)

# 示例：使用 DuckDB（类似模式）
duckdb_config = DuckDB() # 继承自 local.login_info.DB_LOGIN_INFO.DuckDB
duck_db = DuckDB(
    path=duckdb_config.path,
    database=duckdb_config.database,
    schema="my_duckdb_database"
)

# ... DuckDB 的类似操作 ...
```

### 核心概念与设计哲学

*   **抽象**: 该模块抽象了直接数据库交互的复杂性，为不同的数据库系统提供了统一的 API。
*   **配置驱动**: 数据库连接详细信息和其他配置集中在 `config.py` 中管理，允许轻松修改和针对特定环境的设置。
*   **继承实现重用**: 清晰的继承层次结构（`meta.main` 作为基类）确保通用数据库操作只定义一次，并在特定的数据库实现中重用。
*   **类型安全与转换**: `__data_type__` 模块确保数据类型在通用 Python 类型和特定数据库类型之间正确映射，减少潜在错误。
*   **模块化**: 该模块被分解为逻辑子模块，使其更易于理解、维护和扩展。