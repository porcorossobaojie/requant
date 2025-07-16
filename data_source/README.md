# `data_source` Module Documentation

[![Build Status](https://img.shields.io/travis/user/repo.svg)](https://travis-ci.org/user/repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction

The `data_source` module is the cornerstone of the project's data management strategy. It abstracts the complexities of various financial data providers, offering a standardized, unified interface for data retrieval and storage. Its primary goal is to ensure that data access is consistent, reliable, and easily extensible, regardless of the underlying source (e.g., JoinQuant, local files, other APIs).

## File and Module Structure

```
data_source/
├── config.py               # Defines base configurations for all data sources.
├── local.py                # Stores sensitive, local-only login credentials.
└── joinquant/              # Implementation for the JoinQuant data provider.
    ├── config.py           # Contains all configurations specific to JoinQuant.
    │   # - DATABASE: Extends base config, defines schema, keys.
    │   # - ANN_DT_TABLES: Configs for announcement-date-based tables.
    │   # - TRADE_DT_TABLES: Configs for trade-date-based tables.
    ├── meta/
    │   └── main.py         # Core metadata handler for JoinQuant.
    │       # - main(): Fetches, standardizes, and manages market metadata.
    ├── ann_dt_table/
    │   └── main.py         # Handles daily updates for announcement-date tables.
    │       # - daily(): Performs incremental updates based on the last announcement date.
    └── trade_dt_table/
        └── main.py         # Handles daily updates for trade-date tables.
            # - daily(): Performs incremental updates based on the last trade date.
```

## Module Overview and Architecture

The module employs a hierarchical and provider-specific architecture. A central set of base configuration files defines common structures, while provider-specific sub-directories (`joinquant/`) contain tailored logic and configurations. This design promotes modularity and makes it straightforward to add new data sources in the future.

The core logic revolves around a configuration-driven approach. The `config.py` files define not just connection details but also the structure of data tables and the commands needed to fetch them. The `main.py` modules then use these configurations to execute the data retrieval and storage pipelines.

### Configuration Dependency Flow

The relationship between the configuration files is crucial for understanding the data flow and settings inheritance.

```
+--------------------------+        +-------------------------+
|  `data_source/local.py`  |        | `data_source/config.py` |
|--------------------------|        |-------------------------|
| - LOGIN_INFO:            |        | - class DATABASE:       |
|   (User credentials)     |        |   (Base column names)   |
+-----------+--------------+        +------------+------------+
            |                                    ^
            | Imports                            | Inherits
            |                                    |
+-----------+------------------------------------+------------+
|                  `data_source/joinquant/config.py`            |
|-------------------------------------------------------------|
| - Imports LOGIN_INFO for authentication.                    |
| - Extends `DATABASE` to add provider-specific settings.     |
| - Defines `ANN_DT_TABLES` & `TRADE_DT_TABLES` with API cmds.|
+-------------------------------------------------------------+
```

## Purpose of Each Module

### `config.py`
*   **Positioning and Role**: This is the foundational configuration file for the entire `data_source` module. It establishes a common data contract by defining standard field names (e.g., `trade_dt`, `ann_dt`) that all other parts of the project can rely on.
*   **Key Components**:
    *   `DATABASE`: A class that holds non-sensitive, universal configuration values.
    *   `FILTER`: Defines default filter settings, like the global start date for data retrieval.
*   **Dependencies**: None. It is a base configuration file.

### `local.py`
*   **Positioning and Role**: This file is designed to store sensitive user credentials (API keys, passwords) required by data providers. It is explicitly intended for local use and **must** be excluded from version control.
*   **Key Components**:
    *   `LOGIN_INFO`: A dictionary containing the authentication details for a specific service (e.g., JoinQuant).
*   **Dependencies**: None.

### `joinquant/config.py`
*   **Positioning and Role**: This is the central configuration hub for the JoinQuant data source. It aggregates base settings, local credentials, and defines the specific tables and API commands needed to fetch data from JoinQuant.
*   **Key Components**:
    *   `DATABASE`: Inherits from the base `config.py` and extends it with JoinQuant-specific settings like database schema and primary keys.
    *   `ANN_DT_TABLES` & `TRADE_DT_TABLES`: These classes contain dictionaries that map table names to their configurations, including the exact `jqdatasdk` commands to be executed.
*   **Dependencies**: Imports `LOGIN_INFO` from `local.py` and `DATABASE` from the root `config.py`.

### `joinquant/meta/main.py`
*   **Positioning and Role**: This is the core data handling class for the JoinQuant source. It contains the generic pipeline for fetching, cleaning, and standardizing data before it is written to the database.
*   **Key Components**:
    *   `main`: A class that orchestrates the data pipeline. Its `pipeline()` method is the primary entry point for data processing.
*   **Dependencies**: Relies heavily on the configurations defined in `joinquant/config.py`.

## Other Helpful Information

### Quick Start / Usage Example

To run a daily update for a specific table from the JoinQuant source, you would instantiate the appropriate handler and call the `daily()` method.

```python
# Example: Run a daily update for the A-share balance sheet table
from data_source.joinquant.ann_dt_table.main import main as AnnDtMain
from data_source.joinquant.config import ANN_DT_TABLES

# 1. Select the configuration for the desired table
balance_sheet_config = ANN_DT_TABLES.asharebalancesheet

# 2. Instantiate the handler with the configuration
data_handler = AnnDtMain(**balance_sheet_config)

# 3. Execute the daily update
# This will fetch new data since the last update and append it to the table.
data_handler.daily(if_exists='append')
```

### Core Concepts and Design Philosophy

*   **Configuration-Driven**: The module is designed to be highly configurable. By modifying the `config.py` files, you can change table structures, data sources, and retrieval logic without altering the core pipeline code.
*   **Provider-Specific Abstraction**: Each data provider is encapsulated within its own directory (e.g., `joinquant/`). This makes the system modular and easy to extend with new providers in the future.
*   **Hierarchical Configuration**: A base configuration provides common defaults, which can be inherited and overridden by provider-specific configurations. This reduces redundancy and ensures consistency.

---

# `data_source` 模块文档

[![构建状态](https://img.shields.io/travis/user/repo.svg)](https://travis-ci.org/user/repo)
[![许可证: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 简介

`data_source` 模块是项目数据管理策略的基石。它抽象了各种金融数据提供商的复杂性，为数据检索和存储提供了标准化的统一接口。其主要目标是确保数据访问的一致性、可靠性和易扩展性，无论其底层来源如何（例如，聚宽、本地文件、其他API）。

## 文件和模块结构

```
data_source/
├── config.py               # 定义所有数据源的基础配置。
├── local.py                # 存储敏感的、仅限本地使用的登录凭证。
└── joinquant/              # 针对聚宽数据提供商的实现。
    ├── config.py           # 包含所有聚宽特定的配置。
    │   # - DATABASE: 继承基础配置，定义 schema 和键。
    │   # - ANN_DT_TABLES: 基于公告日期表的配置。
    │   # - TRADE_DT_TABLES: 基于交易日期表的配置。
    ├── meta/
    │   └── main.py         # 聚宽的核心元数据处理器。
    │       # - main(): 获取、标准化并管理市场元数据。
    ├── ann_dt_table/
    │   └── main.py         # 处理基于公告日期表的每日更新。
    │       # - daily(): 根据上一个公告日期执行增量更新。
    └── trade_dt_table/
        └── main.py         # 处理基于交易日期表的每日更新。
            # - daily(): 根据上一个交易日期执行增量更新。
```

## 模块概览与架构

该模块采用分层和针对特定提供商的架构。一组中央基础配置文件定义了通用结构，而特定于提供商的子目录（`joinquant/`）则包含定制的逻辑和配置。这种设计促进了模块化，并使得未来添加新的数据源变得简单。

核心逻辑围绕配置驱动的方法展开。`config.py` 文件不仅定义了连接细节，还定义了数据表的结构和获取它们所需的命令。然后，`main.py` 模块使用这些配置来执行数据检索和存储流程。

### 配置依赖流程

理解配置文件之间的关系对于理清数据流和设置继承至关重要。

```
+--------------------------+        +-------------------------+
|  `data_source/local.py`  |        | `data_source/config.py` |
|--------------------------|        |-------------------------|
| - LOGIN_INFO:            |        | - class DATABASE:       |
|   (用户凭证)             |        |   (基础列名)            |
+-----------+--------------+        +------------+------------+
            |                                    ^
            | 导入                               | 继承
            |                                    |
+-----------+------------------------------------+------------+
|                  `data_source/joinquant/config.py`            |
|-------------------------------------------------------------|
| - 导入 LOGIN_INFO 用于认证。                                |
| - 继承 `DATABASE` 以添加提供商特定的设置。                  |
| - 定义 `ANN_DT_TABLES` 和 `TRADE_DT_TABLES` 并包含 API 命令。|
+-------------------------------------------------------------+
```

## 各个模块的用途

### `config.py`
*   **定位与角色**: 这是整个 `data_source` 模块的基础配置文件。它通过定义项目其他部分可以依赖的标准字段名称（例如 `trade_dt`、`ann_dt`）来建立一个通用的数据契约。
*   **核心组件**:
    *   `DATABASE`: 一个持有非敏感、通用配置值的类。
    *   `FILTER`: 定义默认的筛选设置，如全局数据检索的开始日期。
*   **依赖关系**: 无。它是一个基础配置文件。

### `local.py`
*   **定位与角色**: 此文件旨在存储数据提供商所需的敏感用户凭证（API密钥、密码）。它明确用于本地，并且**必须**从版本控制中排除。
*   **核心组件**:
    *   `LOGIN_INFO`: 一个包含特定服务（如聚宽）认证信息的字典。
*   **依赖关系**: 无。

### `joinquant/config.py`
*   **定位与角色**: 这是聚宽数据源的中央配置中心。它聚合了基础设置、本地凭证，并定义了从聚宽获取数据所需的具体表和API命令。
*   **核心组件**:
    *   `DATABASE`: 继承自基础 `config.py` 并通过添加聚宽特定的设置（如数据库 schema 和主键）来扩展它。
    *   `ANN_DT_TABLES` & `TRADE_DT_TABLES`: 这些类包含将表名映射到其配置的字典，包括要执行的确切 `jqdatasdk` 命令。
*   **依赖关系**: 从 `local.py` 导入 `LOGIN_INFO`，并从根 `config.py` 导入 `DATABASE`。

### `joinquant/meta/main.py`
*   **定位与角色**: 这是聚宽数据源的核心数据处理类。它包含了在数据写入数据库之前进行获取、清洗和标准化的通用流程。
*   **核心组件**:
    *   `main`: 一个协调数据流程的类。其 `pipeline()` 方法是数据处理的主要入口点。
*   **依赖关系**: 严重依赖于 `joinquant/config.py` 中定义的配置。

## 其他有用的信息

### 快速上手 / 用法示例

要从聚宽源为特定表运行每日更新，您需要实例化相应的处理器并调用 `daily()` 方法。

```python
# 示例：为A股资产负债表运行每日更新
from data_source.joinquant.ann_dt_table.main import main as AnnDtMain
from data_source.joinquant.config import ANN_DT_TABLES

# 1. 选择所需表的配置
balance_sheet_config = ANN_DT_TABLES.asharebalancesheet

# 2. 使用配置实例化处理器
data_handler = AnnDtMain(**balance_sheet_config)

# 3. 执行每日更新
# 这将获取自上次更新以来的新数据，并将其附加到表中。
data_handler.daily(if_exists='append')
```

### 核心概念与设计哲学

*   **配置驱动**: 该模块被设计为高度可配置。通过修改 `config.py` 文件，您可以更改表结构、数据源和检索逻辑，而无需更改核心流程代码。
*   **提供商特定的抽象**: 每个数据提供商都封装在其自己的目录中（例如 `joinquant/`）。这使得系统模块化，并且易于将来扩展新的提供商。
*   **分层配置**: 基础配置提供了通用的默认值，这些默认值可以被特定于提供商的配置继承和覆盖。这减少了冗余并确保了一致性。