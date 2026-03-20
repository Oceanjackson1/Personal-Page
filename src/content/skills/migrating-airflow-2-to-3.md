---
title: "Migrating Airflow 2 to 3"
description: "指导将 Apache Airflow 2.x 项目迁移到 Airflow 3.x，处理代码变更和兼容性问题"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["airflow", "migration", "upgrade", "compatibility"]
date: 2026-03-20
---

## 概述

帮助将 Airflow 2.x DAG 代码迁移到 Airflow 3.x，聚焦于代码变更（导入、操作符、hooks、上下文、API 用法）。自动检测 Airflow 2.x 代码并提示用户进行迁移。

## 主要功能

- 处理导入路径和操作符变更
- 修复上下文和 API 用法的兼容性问题
- 使用 ruff 检查迁移规则
- 检测并提示 Airflow 2.x 代码
