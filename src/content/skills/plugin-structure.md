---
title: "Plugin Structure"
description: "Claude Code 插件的标准化目录结构和清单配置指南"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["plugin", "structure", "architecture", "manifest"]
date: 2026-03-20
---

## 概述

Claude Code 插件遵循标准化的目录结构和自动组件发现机制。该技能涵盖常规目录布局、清单驱动配置（plugin.json）和基于组件的组织方式。

## 主要功能

- 标准化目录布局和自动发现
- plugin.json 清单配置
- 组件组织（commands, agents, skills, hooks）
- 使用 ${CLAUDE_PLUGIN_ROOT} 的可移植路径引用
