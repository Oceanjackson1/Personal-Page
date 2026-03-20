---
title: "MCP Integration"
description: "将 Model Context Protocol 服务器集成到 Claude Code 插件中，连接外部服务和 API"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Plugin Dev"
tags: ["mcp", "integration", "api", "external-services"]
date: 2026-03-20
---

## 概述

Model Context Protocol (MCP) 使 Claude Code 插件能够通过提供结构化的工具访问来集成外部服务和 API。支持 SSE、stdio、HTTP 和 WebSocket 等多种服务器类型，可处理 OAuth 和复杂的认证流程。

## 主要功能

- 连接外部服务（数据库、API、文件系统）
- 从单个服务提供 10+ 相关工具
- 处理 OAuth 和复杂认证流程
- 将 MCP 服务器与插件打包实现自动设置
