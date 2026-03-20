---
title: "Testing DAGs"
description: "复杂的 DAG 测试工作流，支持测试-调试-修复的迭代循环"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["airflow", "testing", "dag", "debugging"]
date: 2026-03-20
---

## 概述

使用 af 命令进行 DAG 的测试、调试和修复的迭代循环。适用于多步骤测试请求，如"测试这个 DAG 并在失败时修复"。

## 主要功能

- 运行 DAG 测试
- 测试失败时自动进入调试流程
- 支持迭代的测试-调试-修复循环
- 使用 af CLI 命令，无需安装
