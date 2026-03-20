---
title: "Command Development"
description: "创建 Claude Code 斜杠命令的指南，涵盖结构、前置信息和动态功能"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["plugin", "command", "slash-command", "development"]
date: 2026-03-20
---

## 概述

斜杠命令是定义为 Markdown 文件的常用提示，Claude 在交互会话中执行。该技能涵盖命令结构、YAML 前置信息选项、动态参数和 Bash 执行等内容。注意：.claude/commands/ 是旧格式，新技能推荐使用 .claude/skills/ 目录。

## 主要功能

- Markdown 文件格式的命令定义
- YAML 前置信息配置
- 动态参数和文件引用
- Bash 执行和用户交互模式
