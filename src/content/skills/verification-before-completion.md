---
title: "Verification Before Completion"
description: "在声称工作完成之前，必须运行验证命令并确认输出"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Superpowers"
tags: ["verification", "testing", "quality-assurance"]
date: 2026-03-20
---

## 概述

在未经验证的情况下声称工作完成是不诚实的。该技能强制要求在提交或创建 PR 之前运行验证命令并确认输出，确保证据先于断言。

## 主要功能

- 强制执行"证据先于声明"的铁律
- 在声称完成前必须运行新的验证命令
- 确认验证输出后才能做出成功声明
- 防止未经测试就提交代码
