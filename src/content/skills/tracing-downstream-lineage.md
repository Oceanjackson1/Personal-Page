---
title: "Tracing Downstream Lineage"
description: "追踪下游数据血缘和影响分析，评估变更前的影响范围"
category: "research"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["lineage", "impact-analysis", "downstream", "data"]
date: 2026-03-20
---

## 概述

回答关键问题："如果我修改这个会影响什么？"在进行变更之前追踪下游数据血缘以理解影响范围（blast radius）。

## 主要功能

- 识别直接消费者
- 评估变更对下游的影响
- 在修改表或 DAG 前进行风险评估
- 追踪完整的下游依赖链
