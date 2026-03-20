---
title: "Dispatching Parallel Agents"
description: "面对多个独立任务时，将任务分派给专门的并行代理以提高效率"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Superpowers"
tags: ["parallel", "agents", "concurrency", "subagent"]
date: 2026-03-20
---

## 概述

当面临两个或更多独立任务时，通过将任务委派给具有隔离上下文的专门代理来并行执行。每个代理获得精心构建的指令和上下文，确保它们专注于各自的任务，同时保留主会话的上下文用于协调工作。

## 主要功能

- 每个独立问题域分派一个代理，支持并发工作
- 代理拥有隔离的上下文，不会继承主会话的历史
- 精确构建每个代理所需的指令和上下文
- 适用于多个不相关的故障调查、不同子系统的独立修复等场景
