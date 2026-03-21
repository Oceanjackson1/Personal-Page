---
title: "DDD Tactical Patterns"
description: "Apply DDD tactical patterns in code using entities, value objects, aggregates, repositories, and domain events with explicit invariants."
category: "development"
source: "community"
author: "Community"
tags: ["ddd", "tactical"]
date: 2026-03-20
---

# DDD Tactical Patterns

## Use this skill when

- Translating domain rules into code structures.
- Designing aggregate boundaries and invariants.
- Refactoring an anemic model into behavior-rich domain objects.
- Defining repository contracts and domain event boundaries.

## Do not use this skill when

- You are still defining strategic boundaries.
- The task is only API documentation or UI layout.
- Full DDD complexity is not justified.

## Instructions

1. Identify invariants first and design aggregates around them.
2. Model immutable value objects for validated concepts.
3. Keep domain behavior in domain objects, not controllers.
4. Emit domain events for meaningful state transitions.
5. Keep repositories at aggregate root boundaries.

If detailed checklists are needed, open `references/tactical-checklist.md`.

## Example

```typescript
class Order {
  private status: "draft" | "submitted" = "draft";

  submit(itemsCount: number): void {
    if (itemsCount === 0) throw new Error("Order cannot be submitted empty");
    if (this.status !== "draft") throw new Error("Order already submitted");
    this.status = "submitted";
  }
}
```

## Limitations

- This skill does not define deployment architecture.
- It does not choose databases or transport protocols.
- It should be paired with testing patterns for invariant coverage.

---

## Reference: Tactical Checklist

# Tactical Pattern Checklist

## Aggregate design

- One aggregate root per transaction boundary
- Invariants enforced inside aggregate methods
- Avoid cross-aggregate synchronous consistency rules

## Value objects

- Immutable by default
- Validation at construction
- Equality by value, not identity

## Repositories

- Persist and load aggregate roots only
- Expose domain-friendly query methods
- Avoid leaking ORM entities into domain layer

## Domain events

- Past-tense event names (for example, `OrderSubmitted`)
- Include minimal, stable event payloads
- Version event schema before breaking changes
