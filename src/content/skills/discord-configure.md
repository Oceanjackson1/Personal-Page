---
title: "Discord Configure"
description: "设置 Discord 频道——保存机器人令牌并审查访问策略"
category: "other"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Discord"
tags: ["discord", "configuration", "bot", "setup"]
date: 2026-03-20
---

## 概述

设置 Discord 频道，将机器人令牌写入 ~/.claude/channels/discord/.env 并引导用户了解访问策略。服务器在启动时读取两个状态文件。

## 主要功能

- 保存 Discord 机器人令牌
- 检查频道状态和配置
- 引导用户了解访问策略
- 自动配置服务器所需的环境文件
