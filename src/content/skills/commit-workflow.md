---
title: "Commit Workflow"
description: "自动化 Git 提交工作流，智能生成 commit message 并遵循 Conventional Commits 规范。"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Claude Code Community"
tags: ["git", "commit", "automation"]
date: 2026-03-15
---

## 功能概述

Commit Workflow Skill 帮助开发者自动化 Git 提交流程。它能分析代码变更，智能生成符合 Conventional Commits 规范的 commit message。

## 使用方式

在 Claude Code 中使用 `/commit` 命令即可触发此 Skill。

## 主要特性

- 自动分析 staged changes
- 生成语义化的 commit message
- 支持 Conventional Commits 规范
- 自动判断 feat / fix / refactor 等类型
