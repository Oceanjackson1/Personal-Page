---
title: "Cosmos + dbt Fusion"
description: "使用 Astronomer Cosmos 运行 dbt Fusion 项目，覆盖 Snowflake/Databricks 的配置"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["cosmos", "dbt-fusion", "airflow", "data-pipeline"]
date: 2026-03-20
---

## 概述

使用 Cosmos 1.11+ 运行 dbt Fusion 项目。覆盖 Snowflake、Databricks、BigQuery 和 Redshift 上使用 ExecutionMode.LOCAL 的 Fusion 特定配置和约束。

## 主要功能

- 配置 dbt Fusion 与 Cosmos 的集成
- 支持 Snowflake、Databricks、BigQuery 和 Redshift
- 使用本地执行模式
- Fusion 特定的约束和配置指导
