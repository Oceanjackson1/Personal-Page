---
title: "Using Git Worktrees"
description: "使用 Git Worktrees 创建隔离工作区，支持同时在多个分支上工作"
category: "workflow"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Superpowers"
tags: ["git", "worktree", "isolation", "branching"]
date: 2026-03-20
---

## 概述

Git worktrees 创建共享同一仓库的隔离工作区，允许同时在多个分支上工作而无需切换。该技能提供系统化的目录选择和安全验证流程，确保可靠的工作区隔离。

## 主要功能

- 创建与当前工作区隔离的 Git worktree
- 智能目录选择和优先级排序
- 安全验证机制防止误操作
- 适用于功能开发和执行实现计划
