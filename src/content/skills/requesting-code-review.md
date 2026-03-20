---
title: "Requesting Code Review"
description: "完成任务或实现主要功能后，发起代码审查以在问题扩散前捕获它们"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Superpowers"
tags: ["code-review", "quality-assurance", "subagent"]
date: 2026-03-20
---

## 概述

通过分派专门的代码审查子代理来在问题扩散前捕获它们。审查者获得精心构建的上下文进行评估，而非你的会话历史，确保审查者专注于工作成果而非思考过程。

## 主要功能

- 在完成主要功能或合并到主分支前自动发起审查
- 使用隔离的子代理进行客观审查
- 支持在开发各阶段灵活触发
- 保留主会话上下文用于后续工作
