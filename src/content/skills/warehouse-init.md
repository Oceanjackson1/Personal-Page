---
title: "Warehouse Schema Init"
description: "初始化仓库架构发现，生成包含所有表元数据的参考文件"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["warehouse", "schema", "discovery", "metadata"]
date: 2026-03-20
---

## 概述

生成全面的、用户可编辑的数据仓库架构参考文件。发现所有数据库、架构、表和列，并使用代码库上下文（dbt 模型、SQL 文件、架构文档）进行丰富。

## 主要功能

- 自动发现仓库中的所有数据库、架构和表
- 使用代码库上下文丰富元数据
- 生成可编辑的 .astro/warehouse.md 参考文件
- 支持按需刷新架构变更
