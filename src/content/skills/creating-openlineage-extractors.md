---
title: "Creating OpenLineage Extractors"
description: "为不支持的 Airflow 操作符创建自定义 OpenLineage 提取器以捕获数据血缘"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["openlineage", "airflow", "lineage", "extractor"]
date: 2026-03-20
---

## 概述

为没有内置支持的 Airflow 操作符创建自定义 OpenLineage 提取器，以捕获数据血缘信息。适用于需要从不支持的第三方操作符获取血缘、需要列级血缘或需要超出 inlets/outlets 能力的复杂提取逻辑的场景。

## 主要功能

- 为不支持的操作符创建自定义提取器
- 支持列级血缘追踪
- 处理复杂的提取逻辑
- 遵循 OpenLineage 提供者开发指南
