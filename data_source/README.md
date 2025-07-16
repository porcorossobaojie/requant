# Data Source Module

This module is responsible for abstracting and managing various data sources used within the project. It provides a unified interface for accessing financial data from different providers, ensuring consistency and ease of integration.

## Directory Structure

```
data_source/
├── __init__.py
├── config.py           # Base configuration for data sources
├── local.py            # Local login information for data sources (e.g., API keys)
├── joinquant/          # Specific implementation for JoinQuant data source
│   ├── __init__.py
│   ├── config.py       # JoinQuant specific configuration, extends base config
│   ├── ann_dt_table/   # Modules for annotation date tables
│   └── trade_dt_table/ # Modules for trade date tables
└── ...
```

## Configuration

The `data_source` module utilizes a hierarchical configuration system to manage data source settings and credentials.

*   `config.py`: Defines base configurations for all data sources, such as default database types and common field names.
*   `local.py`: Stores sensitive login information (e.g., API keys, usernames, passwords) for various data providers. This file is intended for local setup and should typically be excluded from version control (e.g., via `.gitignore`).
*   `joinquant/config.py`: Contains configurations specific to the JoinQuant data source. It extends the `DATABASE` class from the base `config.py` and imports login information from `local.py`.

## Relationship Diagram

The following diagram illustrates the dependencies and inheritance relationships between the configuration files within the `data_source` module:

```
+-----------------------+       +-----------------------+
| data_source/local.py  |       | data_source/config.py |
| - LOGIN_INFO          |       | - class DATABASE      |
+-----------+-----------+       | - class FILTER        |
            ^                     +-----------+-----------+
            | imports             ^                     
            |                     | extends             
            |                     |                     
+---------------------------------+
| data_source/joinquant/config.py |
| - imports LOGIN_INFO            |
| - extends DATABASE from base    |
| - class DATABASE                |
| - class FILTER                  |
| - class ANN_DT_TABLES           |
| - class TRADE_DT_TABLES         |
+---------------------------------+
```

**Explanation:**

*   `data_source/config.py`: Provides the foundational `DATABASE` and `FILTER` classes with common settings.
*   `data_source/local.py`: Supplies the `LOGIN_INFO` dictionary, which holds credentials for external data services.
*   `data_source/joinquant/config.py`:
    *   **Imports `LOGIN_INFO`** from `data_source/local.py` to authenticate with the JoinQuant API.
    *   **Extends `DATABASE`** from `data_source/config.py`, allowing it to inherit and potentially override base database settings while adding JoinQuant-specific configurations (e.g., `schema`, `partition`, `primary_key`).
    *   Defines additional classes like `ANN_DT_TABLES` and `TRADE_DT_TABLES` that specify how various JoinQuant tables are structured and accessed.

---

# 数据源模块

此模块负责抽象和管理项目中使用的各种数据源。它提供了一个统一的接口，用于从不同的提供商访问金融数据，确保一致性和易于集成。

## 目录结构

```
data_source/
├── __init__.py
├── config.py           # 数据源的基础配置
├── local.py            # 数据源的本地登录信息（例如，API 密钥）
├── joinquant/          # 聚宽数据源的特定实现
│   ├── __init__.py
│   ├── config.py       # 聚宽特定配置，继承自基础配置
│   ├── ann_dt_table/   # 注释日期表的模块
│   └── trade_dt_table/ # 交易日期表的模块
└── ...
```

## 配置

`data_source` 模块采用分层配置系统来管理数据源设置和凭据。

*   `config.py`：定义所有数据源的基础配置，例如默认数据库类型和常用字段名称。
*   `local.py`：存储各种数据提供商的敏感登录信息（例如，API 密钥、用户名、密码）。此文件用于本地设置，通常应从版本控制中排除（例如，通过 `.gitignore`）。
*   `joinquant/config.py`：包含聚宽数据源的特定配置。它继承自基础 `config.py` 中的 `DATABASE` 类，并从 `local.py` 导入登录信息。

## 关系图

下图说明了 `data_source` 模块中配置文件之间的依赖关系和继承关系：

```
+-----------------------+       +-----------------------+
| data_source/local.py  |       | data_source/config.py |
| - LOGIN_INFO          |       | - class DATABASE      |
+-----------+-----------+       | - class FILTER        |
            ^                     +-----------+-----------+
            | 导入                ^                     
            |                     | 继承                
            |                     |                     
+---------------------------------+
| data_source/joinquant/config.py |
| - 导入 LOGIN_INFO               |
| - 继承基础 DATABASE             |
| - class DATABASE                |
| - class FILTER                  |
| - class ANN_DT_TABLES           |
| - class TRADE_DT_TABLES         |
+---------------------------------+
```

**解释：**

*   `data_source/config.py`：提供包含通用设置的基础 `DATABASE` 和 `FILTER` 类。
*   `data_source/local.py`：提供 `LOGIN_INFO` 字典，其中包含外部数据服务的凭据。
*   `data_source/joinquant/config.py`：
    *   **从 `data_source/local.py` 导入 `LOGIN_INFO`** 以便与聚宽 API 进行身份验证。
    *   **继承 `data_source/config.py` 中的 `DATABASE`**，使其能够继承并可能覆盖基础数据库设置，同时添加聚宽特定的配置（例如，`schema`、`partition`、`primary_key`）。
    *   定义了额外的类，如 `ANN_DT_TABLES` 和 `TRADE_DT_TABLES`，它们指定了各种聚宽表的结构和访问方式。
