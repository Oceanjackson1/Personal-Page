---
title: "Agent Development"
description: "创建 Claude Code 插件代理的指南，处理复杂的多步骤自主任务"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["plugin", "agent", "subagent", "autonomous"]
date: 2026-03-20
---

## 概述

代理是独立处理复杂多步骤任务的自主子进程。该技能涵盖代理结构、触发条件和系统提示设计，使创建强大的自主能力成为可能。

## 主要功能

- 代理用于自主工作，命令用于用户发起的操作
- Markdown 文件格式配合 YAML 前置信息
- 通过描述字段和示例触发
- 支持模型和颜色自定义
