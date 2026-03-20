---
title: "Cosmos + dbt Core"
description: "使用 Astronomer Cosmos 将 dbt Core 项目转化为 Airflow DAG/TaskGroup"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["cosmos", "dbt", "airflow", "data-pipeline"]
date: 2026-03-20
---

## 概述

将 dbt Core 项目转化为 Airflow DAG 或 TaskGroup，使用 Astronomer Cosmos。覆盖 Cosmos 1.11+ 和 Airflow 3.x 的配置。在实施前需验证 dbt 引擎、数据仓库、Airflow 版本等条件。

## 主要功能

- 将 dbt Core 项目集成到 Airflow 中
- 支持 DbtDag、DbtTaskGroup 和单独操作符
- 配置 ProfileConfig 和 operator_args
- 支持多种执行环境（Airflow 环境/venv/容器）
