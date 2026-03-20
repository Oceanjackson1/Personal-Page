---
title: "Hook Development"
description: "创建 Claude Code 插件 hooks 的指南，支持事件驱动的自动化脚本"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["plugin", "hooks", "automation", "events"]
date: 2026-03-20
---

## 概述

Hooks 是响应 Claude Code 事件的事件驱动自动化脚本。用于验证操作、执行策略、添加上下文和集成外部工具。支持 PreToolUse、PostToolUse、Stop、SessionStart 等多种事件类型。

## 主要功能

- PreToolUse：在工具调用执行前验证
- PostToolUse：响应工具结果
- Stop/SubagentStop：执行完成标准
- SessionStart：加载项目上下文
- 支持基于提示的高级 hooks API
