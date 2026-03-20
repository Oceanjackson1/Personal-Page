---
title: "Plugin Settings"
description: "使用 .local.md 文件存储插件配置和状态的模式指南"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["plugin", "settings", "configuration", "state"]
date: 2026-03-20
---

## 概述

插件可以在项目目录中的 .claude/plugin-name.local.md 文件中存储用户可配置的设置和状态。该模式使用 YAML 前置信息作为结构化配置，Markdown 内容作为提示或附加上下文。

## 主要功能

- 使用 YAML 前置信息存储结构化配置
- Markdown 正文存储提示或上下文
- 按项目独立配置
- 可从 hooks、commands 和 agents 中读取
