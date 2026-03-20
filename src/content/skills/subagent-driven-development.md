---
title: "Subagent-Driven Development"
description: "通过为每个任务分派独立子代理并进行双阶段审查来执行实现计划"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Superpowers"
tags: ["subagent", "development", "parallel", "code-review"]
date: 2026-03-20
---

## 概述

通过为每个任务分派全新的子代理来执行计划，每个任务完成后进行两阶段审查：先检查规格合规性，再检查代码质量。子代理拥有隔离的上下文和精心构建的指令，确保高质量和快速迭代。

## 主要功能

- 每个任务使用全新的子代理，避免上下文污染
- 双阶段审查机制：规格合规性 + 代码质量
- 支持并行处理独立任务
- 保留主会话上下文用于协调工作
