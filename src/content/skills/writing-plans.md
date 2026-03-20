---
title: "Writing Plans"
description: "为多步骤任务编写全面的实现计划，确保工程师有足够上下文执行"
category: "workflow"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Superpowers"
tags: ["planning", "documentation", "implementation"]
date: 2026-03-20
---

## 概述

编写全面的实现计划，假设执行的工程师对代码库零了解。文档中记录每个任务需要修改的文件、代码、测试和参考文档，将完整计划拆分为小粒度任务，遵循 DRY、YAGNI 和 TDD 原则。

## 主要功能

- 生成详尽的分步实现计划
- 每个任务都包含具体的文件路径和代码指导
- 假设执行者对代码库和问题域不熟悉
- 支持频繁提交和增量验证
