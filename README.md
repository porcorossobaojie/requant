# `quant` Project Documentation

[![Build Status](https://img.shields.io/travis/user/repo.svg)](https://travis-ci.org/user/repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Introduction

This project is a comprehensive, modular framework for quantitative financial research. It provides an end-to-end solution for data acquisition, factor engineering, strategy development, and performance backtesting, designed to accelerate the quantitative research lifecycle.

## File and Module Structure

```
quant/
├── __data_source__/   # Manages data acquisition and storage.
│   └── joinquant/     # - Implementation for JoinQuant data source.
├── factors/           # Core library for factor creation and management.
│   ├── __factorize__/ # - Handles factor processing and combination.
│   └── equity/        # - Contains equity-specific factor logic.
├── __back_test__/     # The backtesting engine.
│   └── main.py        # - run_backtest(): Primary entry point.
├── strategys/         # Holds the logic for specific trading strategies.
├── flow/              # Orchestrates the end-to-end research workflow.
│   └── main/          # - main.py: Executes a defined workflow.
├── __pandas__/        # Custom extensions and utilities for pandas DataFrames.
└── standard_rules/    # Contains coding and documentation standards.
```

## Module Overview and Architecture

```
+---------------------+      +---------------------+      +---------------------+
|  `__data_source__`  |----->|      `factors`      |----->|     `strategys`     |
| (Get Raw Data)      |      | (Compute Factors)   |      | (Define Logic)      |
+----------+----------+      +----------+----------+      +----------+----------+
           |                          ^                          |
           |                          |                          |
           v                          |                          v
+-------------------------------------+--------------------------+
|                               `flow`                             |
| (Orchestrates the entire process)                                |
+-------------------------------------+--------------------------+
                                      |
                                      v
+----------------------------------------------------------------+
|                            `__back_test__`                       |
| (Simulates strategy performance against historical data)         |
+----------------------------------------------------------------+
```

## Purpose of Each Module

*   **`__data_source__`**: Responsible for all data interactions. It abstracts the data provider (e.g., `JoinQuant`) and provides clean, standardized data to the rest of the framework.
*   **`factors`**: The heart of the analytical process. This module contains the logic for creating a wide range of factors, from simple moving averages to complex Barra-style risk factors. It is designed for performance and extensibility.
*   **`strategys`**: This is where abstract factors are converted into concrete trading rules. Each strategy module defines entry and exit conditions based on one or more factors.
*   **`__back_test__`**: A powerful engine that simulates the performance of strategies against historical data. It handles portfolio construction, transaction costs, and performance metric calculation (e.g., Sharpe Ratio, Max Drawdown).
*   **`flow`**: Acts as the master controller, orchestrating the entire workflow from data loading to backtesting. It ensures that each step is executed in the correct order based on configuration.
*   **`__pandas__`**: A utility module that provides custom, reusable functions and classes to extend the functionality of the `pandas` library, tailored for financial data analysis.

## Other Helpful Information

### Quick Start / Usage Example

```python
# Example: Running a full workflow via the 'flow' module
# (Conceptual - actual implementation may vary)

from flow.main import main as run_flow
from flow import config as flow_config

# 1. Configure the desired workflow
flow_config.set_workflow('factor_analysis_001')

# 2. Execute the end-to-end process
# This will typically handle data loading, factor calculation,
# and backtesting as defined in the configuration.
run_flow.execute()
```

### Core Concepts and Design Philosophy

*   **Modularity**: Every component is designed to be independent and interchangeable.
*   **Configuration-Driven**: Workflows and parameters are controlled via configuration files, not hardcoded. This allows for rapid experimentation.
*   **Vectorized Operations**: Leverages `numpy` and `pandas` for high-performance, vectorized calculations, avoiding slow, iterative loops.

### Contribution Guide

Before contributing, please review the standards defined in the `standard_rules/` directory. All code and documentation must adhere to `code_standards.md` and `readme_standards.md`.

### Known Limitations or Common Pitfalls

*   Ensure your data from `__data_source__` is up-to-date before running backtests to avoid look-ahead bias.

---

# `quant` 项目文档

[![构建状态](https://img.shields.io/travis/user/repo.svg)](https://travis-ci.org/user/repo)
[![许可证: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 简介

本项目是一个全面的、模块化的量化金融研究框架。它为数据获取、因子工程、策略开发和性能回测提供了一套端到端的解决方案，旨在加速量化研究的整个生命周期。

## 文件和模块结构

```
quant/
├── __data_source__/   # 管理数据的获取与存储
│   └── joinquant/     # - JoinQuant 数据源的实现
├── factors/           # 用于因子创建和管理的核心库
│   ├── __factorize__/ # - 处理因子的合成与加工
│   └── equity/        # - 包含权益类因子的具体逻辑
├── __back_test__/     # 回测引擎
│   └── main.py        # - run_backtest(): 主要入口函数
├── strategys/         # 存放具体交易策略的逻辑
├── flow/              # 编排端到端的研究工作流
│   └── main/          # - main.py: 执行一个已定义的工作流
├── __pandas__/        # 针对 Pandas DataFrame 的自定义扩展和工具
└── standard_rules/    # 包含编码和文档规范
```

## 模块概览与架构

```
+---------------------+      +---------------------+      +---------------------+
|  `__data_source__`  |----->|      `factors`      |----->|     `strategys`     |
| (获取原始数据)      |      | (计算因子)          |      | (定义交易逻辑)      |
+----------+----------+      +----------+----------+      +----------+----------+
           |                          ^                          |
           |                          |                          |
           v                          |                          v
+-------------------------------------+--------------------------+
|                               `flow`                             |
| (编排整个流程)                                                   |
+-------------------------------------+--------------------------+
                                      |
                                      v
+----------------------------------------------------------------+
|                            `__back_test__`                       |
| (基于历史数据模拟策略表现)                                       |
+----------------------------------------------------------------+
```

## 各个模块的用途

*   **`__data_source__`**: 负责所有数据交互。它抽象了数据提供方（例如 `JoinQuant`），并为框架的其余部分提供干净、标准化的数据。
*   **`factors`**: 分析流程的核心。该模块包含了创建各类因子的逻辑，从简单的移动平均线到复杂的 Barra 风格风险因子。它的设计旨在实现高性能和高可扩展性。
*   **`strategys`**: 这是将抽象因子转化为具体交易规则的地方。每个策略模块都基于一个或多个因子来定义入场和出场条件。
*   **`__back_test__`**: 一个强大的引擎，用于模拟策略在历史数据上的表现。它处理投资组合构建、交易成本和性能指标计算（如夏普比率、最大回撤）。
*   **`flow`**: 作为主控制器，编排从数据加载到回测的整个工作流程。它确保每一步都根据配置按正确的顺序执行。
*   **`__pandas__`**: 一个实用工具模块，提供可复用的自定义函数和类，以扩展 `pandas` 库的功能，专为金融数据分析而定制。

## 其他有用的信息

### 快速上手 / 用法示例

```python
# 示例：通过 'flow' 模块运行完整的工作流
# (概念性代码，实际实现可能有所不同)

from flow.main import main as run_flow
from flow import config as flow_config

# 1. 配置所需的工作流
flow_config.set_workflow('factor_analysis_001')

# 2. 执行端到端的流程
# 这通常会处理在配置中定义的数据加载、因子计算和回测
run_flow.execute()
```

### 核心概念与设计哲学

*   **模块化**: 每个组件都被设计成独立的、可互换的。
*   **配置驱动**: 工作流和参数通过配置文件控制，而非硬编码。这允许快速进行实验。
*   **向量化运算**: 利用 `numpy` 和 `pandas` 进行高性能的向量化计算，避免缓慢的迭代循环。

### 贡献指南

在贡献代码之前，请查阅 `standard_rules/` 目录中定义的规范。所有代码和文档都必须遵守 `code_standards.md` 和 `readme_standards.md`。

### 已知限制或常见陷阱

*   在运行回测前，请确保 `__data_source__` 中的数据是最新的，以避免前视偏差。
