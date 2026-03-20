---
title: "Airflow Human-in-the-Loop"
description: "在 Airflow 中实现人工审批、表单输入和人工驱动分支的工作流"
category: "devops"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Data"
tags: ["airflow", "hitl", "approval", "workflow"]
date: 2026-03-20
---

## 概述

在 Airflow DAG 中实现人工审批门控、表单输入和人工驱动分支。使用可延迟的 HITL 操作符暂停工作流执行，直到人工通过 UI 或 REST API 响应。需要 Airflow 3.1+。

## 主要功能

- ApprovalOperator 用于审批/拒绝工作流
- HITLOperator 用于表单输入
- HITLBranchOperator 用于人工驱动的分支选择
- 支持通过 Airflow UI 或 REST API 响应
