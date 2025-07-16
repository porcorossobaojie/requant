# README Documentation Standards (Revised)

This document outlines the definitive structure, content, and style for `README.md` files within this project. This revised version strictly adheres to our project's established documentation philosophy, enhancing it with modern best practices for improved clarity and usability.

## 1. General Guidelines

*   **Purpose**: To provide a clear, concise, and comprehensive overview of the module, directory, or component it describes. It serves as the primary entry point for understanding its functionality, structure, and usage.
*   **Audience**: Primarily developers, maintainers, and anyone needing to understand or use the documented code.
*   **Language**: All `README.md` files **must** provide content in both **English and Chinese**. The English version must come first, followed by the Chinese translation, separated by a horizontal rule (`---`).
*   **File Naming**: The documentation file must always be named `README.md`.

## 2. Standard Sections

Each `README.md` file **must** include the following sections in the specified order. This structure is mandatory to ensure consistency.

### 2.1. Module Title and Badges

*   **Heading**: `# `Module Name` Module Documentation` (e.g., `# `__back_test__` Module Documentation`)
*   **Content**: The top-level heading must clearly state the name of the module or directory being documented. Use backticks for the module name.
*   **Badges**: Immediately following the title, a series of badges should be included for at-a-glance status information (e.g., build status, version, license). This is a new requirement to add a modern touch.
    ```markdown
    [![Build Status](https://img.shields.io/travis/user/repo.svg)](https://travis-ci.org/user/repo)
    [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
    ```

### 2.2. Introduction

*   **Heading**: `## Introduction`
*   **Content**: A brief, high-level summary of the module's purpose, its primary function, and what problem it aims to solve. This should be a concise paragraph or two. It is highly recommended to include a screenshot or a GIF here if the module has a visual output, to immediately capture interest.

### 2.3. File and Module Structure

*   **Heading**: `## File and Module Structure`
*   **Content**: A tree-like representation of the directory's key files and sub-directories, adhering strictly to the following rules:
    *   Use a simple ASCII tree structure.
    *   It must include the main/core content modules, ignoring procedural or empty files and directories.
    *   For the main/core content modules, the tree diagram **must** include necessary content such as the names, methods, or meanings of internal main functions.

    ```
    module_name/
    ├── config.py               # Handles all configuration
    └── main.py                 # Main execution logic
        # - run_backtest(): The primary entry point function
    ```

### 2.4. Module Overview and Architecture

*   **Heading**: `## Module Overview and Architecture`
*   **Content**: Explains the overall design principles, key components, and their interactions.
    *   Describe the dependencies and logical flow between different files or sub-modules.
    *   A conceptual flow diagram (using ASCII art) is **mandatory** to visually represent the core logic, key functions, and data flow, not just high-level module interactions.

    ```
    +-----------------+
    |  `config.py`    |
    +--------+--------+
             |
             v
    +--------+--------------------------------+
    |  `main.py` -> run_backtest()           |
    +--------+--------------------------------+
             |
             v
    +--------+--------------------------------+
    |  Data Processing Logic                 |
    +----------------------------------------+
    ```

### 2.5. Purpose of Each Module

*   **Heading**: `## Purpose of Each Module`
*   **Content**: Provide a detailed explanation for each significant file or sub-module. This section must help the reader understand the position and usage of each component.
    *   **Positioning and Role**: Clearly define its specific responsibility and how it fits into the module's overall architecture.
    *   **Key Components and Usage**: Detail the most important classes, functions, or methods. For each key component, explain its purpose, application scenario, and provide a concise code snippet demonstrating how it is called.
    *   **Dependencies**: Briefly mention what other modules it imports or relies on.

### 2.6. Other Helpful Information

*   **Heading**: `## Other Helpful Information`
*   **Content**: This section must provide practical information that helps a developer start using the module quickly and effectively. It should be treated as a mini-guide. The order of subsections here is important.
    *   **Quick Start / Usage Example**: This must be the first part of this section. Provide a clear, end-to-end code snippet demonstrating a primary use case. This should be a practical, runnable example.
    *   **Core Concepts and Design Philosophy**: Explain the key ideas behind the module's design (e.g., "Vectorized backtesting", "Configuration-driven").
    *   **Contribution Guide**: Briefly explain the process for extending or contributing to the module.
    *   **Known Limitations or Common Pitfalls**: List any important warnings, non-obvious behaviors, or things to watch out for.

## 3. Formatting and Style

*   **Markdown**: Use GitHub-flavored Markdown for all formatting.
*   **Headings**: Strictly use the following levels:
    *   Main Title: `#` (one hash)
    *   Major Sections: `##` (two hashes)
    *   Sub-sections: `###` (three hashes)
*   **Code Blocks**: Use triple backticks (``````) for code examples, file structures, and ASCII diagrams.
*   **Inline Code**: Use single backticks (`` `text` ``) for inline code, file names, module names, or key terms.
*   **Bold Text**: Use `**text**` for strong emphasis (e.g., class names, important concepts).
*   **Horizontal Rule**: Use `---` **only** to separate the English and Chinese versions of the document.

## 4. Content Specifics

*   **Clarity and Conciseness**: Write clearly and directly. Avoid jargon where possible, or explain it if necessary.
*   **Accuracy**: Ensure all information is accurate and up-to-date with the current codebase.
*   **Completeness**: Provide enough detail for a new developer to understand the module's purpose and how to use it without needing to dive deep into the code immediately.
*   **Consistency**: Maintain consistent terminology and phrasing throughout the document.

---

# README 文档规范 (修订版)

本文档概述了本项目中 `README.md` 文件的最终结构、内容和样式。本修订版严格遵循我们项目既定的文档理念，并通过融合现代最佳实践来提升其清晰度和可用性。

## 1. 一般准则

*   **目的**: 提供对其所描述的模块、目录或组件的清晰、简洁和全面的概述。它应作为理解其功能、结构和用法的主要入口点。
*   **受众**: 主要面向开发人员、维护人员以及任何需要理解或使用所记录代码的人员。
*   **语言**: 所有 `README.md` 文件**必须**同时提供**英文和中文**内容。英文版本必须在前，后跟中文翻译，两者之间用水平线 (`---`) 分隔。
*   **文件命名**: 文档文件必须始终命名为 `README.md`。

## 2. 标准章节

每个 `README.md` 文件**必须**按指定顺序包含以下章节。此结构为强制性，以确保一致性。

### 2.1. 模块标题与徽章

*   **标题**: `# `模块名称` 模块文档` (例如, `# `__back_test__` 模块文档`)
*   **内容**: 顶层标题必须清晰地说明所记录模块或目录的名称。模块名称使用反引号。
*   **徽章 (Badges)**: 紧跟标题之后，应包含一系列徽章，用于提供一目了然的状态信息（例如：构建状态、版本、许可证）。这是一项为增加现代感而设的新要求。
    ```markdown
    [![Build Status](https://img.shields.io/travis/user/repo.svg)](https://travis-ci.org/user/repo)
    [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
    ```

### 2.2. 简介

*   **标题**: `## 简介`
*   **内容**: 对模块目的、主要功能以及它旨在解决的问题进行简要、高层次的总结。这应该是一到两个简洁的段落。如果模块有可视化输出，强烈建议在此处包含截图或GIF，以立即吸引读者注意。

### 2.3. 文件和模块结构

*   **标题**: `## 文件和模块结构`
*   **内容**: 目录中关键文件和子目录的树状表示，严格遵守以下规则：
    *   使用简单的 ASCII 树结构。
    *   必须包含主要/核心内容模块，忽略流程性或空的文件及目录。
    *   对于主要/核心内容模块，树状图**必须**包括内部主要函数的名称、方法或含义等必要的内容。

    ```
    module_name/
    ├── config.py               # 处理所有配置
    └── main.py                 # 主要执行逻辑
        # - run_backtest(): 主要入口函数
    ```

### 2.4. 模块概览与架构

*   **标题**: `## 模块概览与架构`
*   **内容**: 解释整体设计原则、关键组件及其交互。
    *   描述不同文件或子模块之间的依赖关系和逻辑流程。
    *   **强制要求**使用概念流程图（ASCII 艺术）来可视化核心逻辑、关键函数和数据流，而不仅仅是高层次的模块交互。

    ```
    +-----------------+
    |  `config.py`    |
    +--------+--------+
             |
             v
    +--------+--------------------------------+
    |  `main.py` -> run_backtest()           |
    +--------+--------------------------------+
             |
             v
    +--------+--------------------------------+
    |  数据处理逻辑                          |
    +----------------------------------------+
    ```

### 2.5. 各个模块的用途

*   **标题**: `## 各个模块的用途`
*   **内容**: 对每个重要文件或子模块提供详细解释。此部分必须帮助读者理解每个组件的定位和用法。
    *   **定位与角色**: 清晰地定义其具体职责以及它在整个模块架构中的位置。
    *   **核心组件与用法**: 详细说明最重要的类、函数或方法。对于每个核心组件，解释其目的、应用场景，并提供一个简洁的代码片段来演示其调用方式。
    *   **依赖关系**: 简要说明它导入或依赖的其他模块。

### 2.6. 其他有用的信息

*   **标题**: `## 其他有用的信息`
*   **内容**: 此部分必须提供实用信息，以帮助开发人员快速有效地开始使用该模块。应将其视为一份迷你指南。此处的子章节顺序非常重要。
    *   **快速上手 / 用法示例**: 此部分必须是本章节的第一部分。提供一个清晰的、端到端的代码片段，演示一个主要用例。这应该是一个实用的、可运行的示例。
    *   **核心概念与设计哲学**: 解释模块设计背后的关键思想（例如，“向量化回测”、“配置驱动”）。
    *   **贡献指南**: 简要说明扩展或贡献模块的流程。
    *   **已知限制或常见陷阱**: 列出使用该模块时需要注意的任何重要警告、不明显的行为或注意事项。

## 3. 格式和样式

*   **Markdown**: 所有格式均使用 GitHub-flavored Markdown。
*   **标题**: 严格使用以下级别：
    *   主标题: `#` (一个井号)
    *   主要章节: `##` (两个井号)
    *   子章节: `###` (三个井号)
*   **代码块**: 使用三个反引号 (``````) 用于代码示例、文件结构和 ASCII 图。
*   **行内代码**: 使用单个反引号 (`` `文本` ``) 用于行内代码、文件名、模块名或关键词。
*   **粗体文本**: 使用 `**文本**` 进行强调（例如，类名、重要概念）。
*   **水平线**: `---` **仅**用于分隔文档的英文和中文版本。

## 4. 内容细节

*   **清晰简洁**: 书写清晰直接。尽可能避免行话，如果需要则进行解释。
*   **准确性**: 确保所有信息准确并与当前代码库保持同步。
*   **完整性**: 提供足够的细节，以便新开发人员无需立即深入代码即可理解模块的目的和使用方法。
*   **一致性**: 在整个文档中保持术语和措辞的一致性。