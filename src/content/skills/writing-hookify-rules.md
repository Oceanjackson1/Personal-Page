---
title: "Writing Hookify Rules"
description: "编写 Hookify 规则的语法和模式指南，定义模式匹配和消息显示"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Hookify"
tags: ["hookify", "rules", "automation", "pattern-matching"]
date: 2026-03-20
---

## 概述

Hookify 规则是带有 YAML 前置信息的 Markdown 文件，定义要监视的模式和匹配时显示的消息。规则存储在 .claude/hookify.{rule-name}.local.md 文件中。

## 主要功能

- YAML 前置信息定义规则标识符和启用状态
- 模式匹配定义监视条件
- 消息定义匹配时的提示内容
- 支持多种匹配模式和规则组合
