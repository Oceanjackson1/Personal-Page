---
title: "Annotating Task Lineage"
description: "使用 inlets 和 outlets 为 Airflow 任务添加数据血缘注解"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["airflow", "lineage", "openlineage", "metadata"]
date: 2026-03-20
---

## 概述

为 Airflow 任务添加数据血缘注解，使用 inlets 和 outlets 指定输入/输出数据集，为没有内置 OpenLineage 提取器的操作符启用血缘跟踪。

## 主要功能

- 使用 inlets 和 outlets 标注数据输入输出
- 为任务添加血缘元数据
- 在 Astro 的增强血缘视图中可视化
- 提供跨 DAG 和跨部署的血缘视图
