---
title: "Stripe Best Practices"
description: "构建 Stripe 集成的最佳实践，涵盖支付处理、结账流程和 Webhooks"
category: "development"
source: "community"
sourceUrl: "https://github.com/anthropics/claude-code"
author: "Stripe"
tags: ["stripe", "payments", "checkout", "integration"]
date: 2026-03-20
---

## 概述

构建 Stripe 集成的最佳实践指南。优先推荐 CheckoutSessions API 和 Stripe 托管/嵌入式结账页面。避免使用已弃用的 Charges API、Sources API 和旧版 Card Element。始终使用最新版本的 API 和 SDK。

## 主要功能

- 优先使用 CheckoutSessions API 进行支付建模
- 推荐 Stripe 托管或嵌入式结账页面
- 指导使用 Payment Element 替代旧版 Card Element
- 建议开启动态支付方式而非手动指定
- 提供上线前检查清单
