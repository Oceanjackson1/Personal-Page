---
title: "Chrome DevTools Troubleshooting"
description: "排查 Chrome DevTools MCP 的连接和目标问题，修复服务器初始化故障"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Chrome DevTools MCP"
tags: ["troubleshooting", "chrome", "mcp", "configuration"]
date: 2026-03-20
---

## 概述

当 list_pages、new_page 或 navigate_page 失败，或服务器初始化失败时，该技能作为故障排除向导帮助用户配置和修复 Chrome DevTools MCP 服务器设置。

## 主要功能

- 查找并读取 MCP 配置文件进行诊断
- 识别错误的参数、标志或缺失的环境变量
- 提供分步诊断流程
- 支持多种配置文件格式的检查
