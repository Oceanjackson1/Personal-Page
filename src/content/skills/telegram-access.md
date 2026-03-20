---
title: "Telegram Access Management"
description: "管理 Telegram 频道访问权限——审批配对、编辑允许列表和设置策略"
category: "other"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Telegram"
tags: ["telegram", "access", "security", "channel"]
date: 2026-03-20
---

## 概述

管理 Telegram 频道的访问控制。所有状态存储在 ~/.claude/channels/telegram/access.json 中。该技能仅处理用户在终端会话中直接输入的请求，拒绝通过频道通知传来的访问变更请求以防止提示注入。

## 主要功能

- 审批和管理频道配对
- 编辑允许列表
- 设置 DM 和群组策略
- 安全防护防止提示注入攻击
