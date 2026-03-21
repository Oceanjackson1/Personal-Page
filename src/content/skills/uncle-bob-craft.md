---
title: "Uncle Bob Craft"
description: "Use when performing code review, writing or refactoring code, or discussing architecture; complements clean-code and does not replace project linter/formatter."
category: "writing"
source: "community"
author: "Community"
tags: ["uncle", "bob", "craft"]
date: 2026-03-20
---

# Uncle Bob Craft

Apply Robert C. Martin (Uncle Bob) criteria for **code review and production**: Clean Code, Clean Architecture, The Clean Coder, Clean Agile, and design-pattern discipline. This skill is **complementary** to the existing `@clean-code` skill (which focuses on the Clean Code book) and to your project's linter/formatter—it does not replace them.

## Overview

This skill aggregates principles from Uncle Bob's body of work for **reviewing** and **writing** code: naming and functions (via `@clean-code`), architecture and boundaries (Clean Architecture), professionalism and estimation (The Clean Coder), agile values and practices (Clean Agile), and design-pattern use vs misuse. Use it to evaluate structure, dependencies, SOLID in context, code smells, and professional practices. It provides craft and design criteria only—not syntax or style enforcement, which remain the responsibility of your linter and formatter.

## When to Use This Skill

- **Code review**: Apply Dependency Rule, boundaries, SOLID, and smell heuristics; suggest concrete refactors.
- **Refactoring**: Decide what to extract, where to draw boundaries, and whether a design pattern is justified.
- **Architecture discussion**: Check layer boundaries, dependency direction, and separation of concerns.
- **Design patterns**: Assess correct use vs cargo-cult or overuse before introducing a pattern.
- **Estimation and professionalism**: Apply Clean Coder ideas (saying no, sustainable pace, three-point estimates).
- **Agile practices**: Reference Clean Agile (Iron Cross, TDD, refactoring, pair programming) when discussing process.
- **Do not use** to replace or override the project's linter, formatter, or automated tests.

## Aggregators by Source

| Source | Focus | Where to go |
|--------|--------|-------------|
| **Clean Code** | Names, functions, comments, formatting, tests, classes, smells | Use `@clean-code` for detail; this skill references it for review/production. |
| **Clean Architecture** | Dependency Rule, layers, boundaries, SOLID in architecture | See [reference.md](./reference.md) and [references/clean-architecture.md](./references/clean-architecture.md). |
| **The Clean Coder** | Professionalism, estimation, saying no, sustainable pace | See [reference.md](./reference.md) and [references/clean-coder.md](./references/clean-coder.md). |
| **Clean Agile** | Values, Iron Cross, TDD, refactoring, pair programming | See [reference.md](./reference.md) and [references/clean-agile.md](./references/clean-agile.md). |
| **Design patterns** | When to use, misuse, cargo cult | See [reference.md](./reference.md) and [references/design-patterns.md](./references/design-patterns.md). |

## Design Patterns: Use vs Misuse

- **Use patterns** when they solve a real design problem (e.g., variation in behavior, lifecycle, or cross-cutting concern), not to look "enterprise."
- **Avoid cargo cult**: Do not add Factory/Strategy/Repository just because the codebase "should" have them; add them when duplication or rigidity justifies the abstraction.
- **Signs of misuse**: Pattern name in every class name, layers that only delegate without logic, patterns that make simple code harder to follow.
- **Rule of thumb**: Introduce a pattern when you feel the third duplication or the second reason to change; name the pattern in code or docs so intent is clear.

## Smells and Heuristics (Summary)

| Smell / Heuristic | Meaning |
|-------------------|--------|
| **Rigidity** | Small change forces many edits. |
| **Fragility** | Changes break unrelated areas. |
| **Immobility** | Hard to reuse in another context. |
| **Viscosity** | Easy to hack, hard to do the right thing. |
| **Needless complexity** | Speculative or unused abstraction. |
| **Needless repetition** | DRY violated; same idea in multiple places. |
| **Opacity** | Code is hard to understand. |

Full lists (including heuristics C1–T9-style) are in [reference.md](./reference.md). Use these in review to name issues and suggest refactors (extract, move dependency, introduce boundary).

## Review vs Production

| Context | Apply |
|---------|--------|
| **Code review** | Dependency Rule and boundaries; SOLID in context; list smells; suggest one or two concrete refactors (e.g., extract function, invert dependency); check tests and professionalism (tests present, no obvious pressure hacks). |
| **Writing new code** | Prefer small functions and single responsibility; depend inward (Clean Architecture); write tests first when doing TDD; avoid patterns until duplication or variation justifies them. |
| **Refactoring** | Identify one smell at a time; refactor in small steps with tests green; improve names and structure before adding behavior. |

## How It Works

### When reviewing code

1. **Boundaries and Dependency Rule**: Check that dependencies point inward (e.g., use cases do not depend on UI or DB details). See [references/clean-architecture.md](./references/clean-architecture.md).
2. **SOLID in context**: Check Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion where they apply to the changed code.
3. **Smells**: Scan for rigidity, fragility, immobility, viscosity, needless complexity/repetition, opacity; list them with file/area.
4. **Concrete suggestions**: Propose one or two refactors (e.g., "Extract this into a function named X," "Introduce an interface so this layer does not depend on the concrete DB client").
5. **Tests and craft**: Note if tests exist and if the change respects sustainable pace (no obvious "we'll fix it later" comments that violate professionalism).

### When writing or refactoring code

1. Prefer **small, single-purpose** functions and classes; use `@clean-code` for naming and structure.
2. Keep **dependencies pointing inward**; put business rules in the center, adapters at the edges.
3. Introduce **design patterns** only when duplication or variation justifies them.
4. Refactor in **small steps** with tests staying green.

## Examples

### Example 1: Code review prompt (copy-pasteable)

Use this to ask for an Uncle Bob–oriented review:

```markdown
Please review this change using Uncle Bob craft criteria (@uncle-bob-craft):
1. Dependency Rule and boundaries — do dependencies point inward?
2. SOLID in context — any violations in the touched code?
3. Smells — list rigidity, fragility, immobility, viscosity, needless complexity/repetition, or opacity.
4. Suggest one or two concrete refactors (e.g., extract function, invert dependency).
Do not duplicate lint/format; focus on structure and design.
```

### Example 2: Before/after (extract and name)

**Before (opacity, does more than one thing):**

```python
def process(d):
    if d.get("t") == 1:
        d["x"] = d["a"] * 1.1
    elif d.get("t") == 2:
        d["x"] = d["a"] * 1.2
    return d
```

**After (clear intent, single level of abstraction):**

```python
def apply_discount(amount: float, discount_type: int) -> float:
    if discount_type == 1:
        return amount * 1.1
    if discount_type == 2:
        return amount * 1.2
    return amount

def process(order: dict) -> dict:
    order["x"] = apply_discount(order["a"], order.get("t", 0))
    return order
```

## Best Practices

- ✅ Use `@clean-code` for naming, functions, comments, and formatting; use this skill for architecture, boundaries, SOLID, smells, and process.
- ✅ In review, name the smell or principle (e.g., "Dependency Rule violation: use case imports from the web framework").
- ✅ Suggest at least one concrete refactor per review (extract, rename, invert dependency).
- ✅ Run the project linter and formatter separately; this skill does not replace them.
- ❌ Do not use this skill to enforce syntax or style; that is the linter's job.
- ❌ Do not add design patterns without a clear duplication or variation reason.

## Common Pitfalls

- **Problem:** Treating every class as needing a Factory or Strategy.  
  **Solution:** Introduce patterns only when you have a real design need (third duplication, second axis of change).

- **Problem:** Review only listing "violates SOLID" without saying where or how.  
  **Solution:** Point to the file/function and which principle (e.g., "SRP: this function parses and persists; split into parse and persist").

- **Problem:** Skipping the project linter because "we applied Uncle Bob."  
  **Solution:** This skill is about craft and design; always run the project's lint and format.

## Related Skills

- **`@clean-code`** — Detailed Clean Code book material (names, functions, comments, formatting, tests, classes, smells). Use for day-to-day code quality; use uncle-bob-craft for architecture and cross-book criteria.
- **`@architecture`** — General architecture decisions and trade-offs. Use when choosing high-level structure; use uncle-bob-craft for Dependency Rule and boundaries.
- **`@code-review-excellence`** — Code review practices. Combine with uncle-bob-craft for principle-based review.
- **`@refactor-clean-code`** — Refactoring toward clean code. Use with uncle-bob-craft when refactoring for boundaries and SOLID.
- **`@test-driven-development`** — TDD workflow. Aligns with Clean Agile and Clean Coder (tests as requirement, sustainable pace).

## Limitations

- **Does not replace the project linter or formatter.** Run lint and format separately; this skill gives design and craft criteria only.
- **Does not replace automated tests.** It can remind you to write tests (Clean Coder, Clean Agile) but does not run or generate them.
- **Complementary to tooling.** Use it alongside existing CI, lint, and test suites.
- **No syntax or style enforcement.** It focuses on structure, dependencies, smells, and professional practice, not on brace style or line length.
- **Summaries, not the books.** Full Clean Code heuristics, component principles (REP/CCP/CRP, ADP/SDP/SAP), and detailed stories are in the books; we reference the most used parts. See [reference.md](./reference.md) "Scope and attribution."

---

## Reference: Clean Agile

# Clean Agile — Deep Reference

Based on Robert C. Martin, *Clean Agile* (2019). Use this when discussing agile values, practices, and the "Iron Cross."

## Agile values (manifesto)

- Individuals and interactions over processes and tools.
- Working software over comprehensive documentation.
- Customer collaboration over contract negotiation.
- Responding to change over following a plan.

Uncle Bob stresses that the right-hand side still has value; the left-hand side is preferred when there is a trade-off.

## Iron Cross (four supporting values)

| Value | What it means in practice |
|-------|---------------------------|
| **Communication** | Prefer face-to-face (or high-bandwidth) communication; reduce information loss; keep the team aligned. |
| **Courage** | Courage to refactor, to say no to unreasonable requests, to change the design when the code tells you to. |
| **Feedback** | Short feedback loops—unit tests, integration tests, demos, small iterations. Learn fast what works and what doesn’t. |
| **Simplicity** | Do the simplest thing that could possibly work. Avoid speculative design and unnecessary abstraction. |

## Practices

- **TDD (Test-Driven Development)** — Red, green, refactor. Write a failing test first, then minimal code to pass, then refactor. Tests act as specification and safety net.
- **Refactoring** — Continuous small improvements. Keep tests green; improve structure, names, and design in small steps.
- **Pair programming** — Two people at one machine. Improves design and quality; spreads knowledge. Not mandatory every hour, but a recognized practice for hard or critical work.
- **Simple design** — No duplication; express intent; minimal elements (classes, methods); small, focused abstractions. Add complexity only when the code asks for it (e.g., third duplication).

## Relationship to craft

Clean Agile ties agile values to craft: sustainable pace, tests as requirement, refactoring as part of the loop, and simplicity over speculation. Use this reference when discussing how TDD, refactoring, or pairing support agility and quality.

---

## Reference: Clean Architecture

# Clean Architecture — Deep Reference

Based on Robert C. Martin, *Clean Architecture* (2017). Use this when you need detailed criteria for dependency direction, layers, and boundaries.

## Dependency Rule

**Dependencies point inward only.** Code in the center (entities, use cases) must not depend on code in outer circles (UI, DB, frameworks). Outer circles depend on inner circles; inner circles define interfaces, outer circles implement them.

- **Violation**: A use case that imports from Express, Django, or a concrete repository implementation.
- **Correct**: Use case depends on an interface (e.g., `OrderRepository`); the adapter in the outer layer implements it and uses Express/DB.

## Layers (from inside out)

1. **Entities** — Enterprise business rules. Plain structures and rules that apply across the application. No dependencies on frameworks or UI.
2. **Use cases** — Application business rules. Orchestrate entities and define application-specific workflows. Depend only on entities and on interfaces for I/O (repositories, presenters).
3. **Interface adapters** — Convert data between use cases and the outside world. Presenters, gateways, controllers that translate external format to/from use-case format. Depend on use cases (and entities only via use cases).
4. **Frameworks and drivers** — Web framework, DB driver, messaging, file I/O. Implement interfaces defined by use cases or interface adapters. Depend inward.

## Boundaries

- **Boundary** = interface or abstract type that inner code depends on; outer code implements.
- Good boundaries make it easy to swap implementations (e.g., in-memory repo for tests, SQL repo for production).
- Draw boundaries where there is a reason to vary or replace (different persistence, different UI, different transport).

## SOLID in this context

- **SRP** — Each module (class/package) has one reason to change (one actor). E.g., separate "report formatting" from "report calculation" if they change for different reasons.
- **OCP** — Extend behavior via new implementations of interfaces (new adapters), not by editing existing use-case or entity code.
- **LSP** — Any implementation of a repository or gateway interface must be substitutable without breaking the use case.
- **ISP** — Small, focused interfaces (e.g., `ReadOrderRepository` and `WriteOrderRepository` if read and write evolve differently) instead of one fat `OrderRepository`.
- **DIP** — Use cases depend on `OrderRepository` (interface); the composition root wires in `SqlOrderRepository`. High-level policy does not depend on low-level details.

## Inversion of dependencies

- **Without inversion**: Use case imports and calls `SqlOrderRepository` directly → use case depends on DB.
- **With inversion**: Use case depends on `OrderRepository` (interface); `SqlOrderRepository` implements it and is injected at the edge. Use case stays independent of SQL.

## Component cohesion and coupling (for larger systems)

When grouping classes into **components** (modules, packages), Uncle Bob defines:

**Cohesion:**  
- **REP (Reuse/Release Equivalence)** — The unit of reuse is the unit of release; group classes that are reused and released together.  
- **CCP (Common Closure)** — Classes that change for the same reasons belong in the same component; reduces impact of change.  
- **CRP (Common Reuse)** — Classes reused together should be packaged together; avoid forcing dependents to pull in more than they need.

**Coupling:**  
- **ADP (Acyclic Dependencies)** — Component dependency graph must have no cycles.  
- **SDP (Stable Dependencies)** — Depend in the direction of stability; less stable components depend on more stable ones.  
- **SAP (Stable Abstractions)** — Stable components should be abstract; unstable components can be concrete.

Use this when discussing module/package boundaries beyond single layers. For full treatment see *Clean Architecture* (Martin, 2017).

---

Use this reference when reviewing for "dependency direction," "layer violations," or "missing boundaries."

---

## Reference: Clean Coder

# The Clean Coder — Deep Reference

Based on Robert C. Martin, *The Clean Coder* (2011). Use this when discussing professionalism, estimation, and sustainable pace.

## Professionalism

- **Do no harm** — Do not leave the codebase in a worse state. If you must leave a mess, leave a clear TODO and track it. Prefer leaving code better than you found it (boy scout rule).
- **Know your craft** — Practice (e.g., katas), read, stay current. Estimate only what you understand enough to estimate.
- **Saying no** — When a request would compromise quality or is unreasonable, say no. Offer alternatives (e.g., "We can do X by date Y if we drop Z" or "We need two more weeks for tests").
- **Saying yes** — When you commit, mean it. Do not say yes to please and then miss; communicate early if you cannot meet a commitment.

## Estimation

- **Three-point estimate** — Best / nominal / worst case. Use for planning and risk, not as a single "promise" number.
- **Velocity** — Use historical velocity for iteration planning. Do not inflate; if the team goes fast once, use that as data for the next time, not as the new permanent commitment.
- **Uncertainty** — Make uncertainty visible. Prefer ranges and confidence levels over false precision.
- **Refusal to estimate** — It is professional to refuse to give a date when the request is vague or the work is unknown; offer to break it down first or to give a range after discovery.

## Sustainable pace

- Sustained overtime reduces quality and long-term output. Occasional crunch may happen; make it rare and recover afterward.
- Tests, refactoring, and learning are part of the job. Skipping them to "hit the date" creates technical debt and is unprofessional in the long run.

## Tests as a requirement

- Code without tests is legacy. Writing and maintaining tests is part of professional delivery, not optional.
- When under pressure, the first thing to protect is the test suite and the ability to refactor safely.

## Mentoring and collaboration

- **Helping others** — Part of professionalism is mentoring, pairing, and leaving the codebase (and the team) better than you found it.
- **Collaboration** — Communicate clearly with stakeholders and peers; say no when needed, and offer alternatives when saying yes is not possible.

Use this reference when the discussion involves commitment, estimates, saying no, sustainable development practices, or teamwork.

---

## Reference: Design Patterns

# Design Patterns — Use vs Misuse

Use this when evaluating whether a design pattern is justified or is cargo cult / overuse.

## When to use a pattern

- **Repeated variation** — Same algorithm or structure with different behavior (e.g., different discount rules) → Strategy or similar.
- **Lifecycle or creation complexity** — Object creation has many variants or steps → Factory, Builder when the duplication or complexity is real.
- **Cross-cutting concern** — Logging, validation, auth at a boundary → Decorator, middleware, or adapter at the edge.
- **Stable abstraction, varying implementation** — You expect to swap implementations (e.g., repository, gateway) → Interface + implementations; dependency injection.

Rule of thumb: introduce a pattern when you feel the **third duplication** or the **second axis of change** (second reason to open the same module). Name the pattern in code or docs so intent is clear.

## When not to use a pattern

- **Simple, linear code** — No duplication, one reason to change. Adding a Factory or Strategy here adds indirection without benefit.
- **Speculative need** — "We might need to swap implementations later." Prefer YAGNI; add the abstraction when you actually have a second implementation or a second reason to change.
- **Every class is a pattern** — Not every class needs to be behind a Factory or an Interface. Use patterns where they solve a real design problem.

## Cargo cult and misuse

- **Cargo cult** — Using a pattern because "that’s what we do" or "enterprise code has Factories," without a clear design reason. Symptoms: Factory that only calls `new`, Strategy with one implementation and no plan for a second.
- **Overuse** — Pattern names in every class name; layers that only delegate and add no logic; code that is harder to follow than a straightforward version.
- **Misuse** — Wrong pattern for the problem (e.g., Singleton for something that should be testable and replaceable); pattern that hides the real design (e.g., God Object behind a Facade).

## Good signals

- The pattern name appears in design docs or comments where it helps (e.g., "Strategy for discount calculation").
- There are at least two concrete variants or a clear, stated reason for future variation.
- Tests and call sites are simpler because of the abstraction (e.g., tests inject a fake repository).

Use this reference in review when someone proposes or has added a Factory, Strategy, Repository, or other pattern—ask "what duplication or variation does this solve?" and "is there a second implementation or a second reason to change?"

---

## Example: Code Review Checklist

# Uncle Bob Craft — Code Review Checklist

Copy-paste this checklist when performing a principle-based code review with the uncle-bob-craft skill. Run your project linter/formatter separately; this checklist focuses on structure and design.

---

## 1. Dependency Rule and boundaries

- [ ] Dependencies point **inward** (use cases / domain do not depend on UI, DB, or framework details).
- [ ] Outer layers depend on interfaces (e.g., repositories, gateways) defined by inner layers.
- [ ] No direct import of framework or driver in the core/use-case code under review.

## 2. SOLID in context

- [ ] **SRP** — Each class/module has one reason to change (one actor).
- [ ] **OCP** — Extension via new implementations, not by editing existing core logic.
- [ ] **LSP** — Subtypes are substitutable; no hidden assumptions about concrete types.
- [ ] **ISP** — Interfaces are focused; callers do not depend on methods they do not use.
- [ ] **DIP** — High-level code depends on abstractions; concretions are injected at the edge.

## 3. Smells

- [ ] **Rigidity** — Small change does not force edits in many places.
- [ ] **Fragility** — Change does not break unrelated areas.
- [ ] **Immobility** — Reuse is possible where it makes sense.
- [ ] **Viscosity** — Doing the right thing is not harder than hacking.
- [ ] **Needless complexity** — No speculative or unused abstraction.
- [ ] **Needless repetition** — DRY; no obvious duplication.
- [ ] **Opacity** — Names and structure make intent clear.

## 4. Design patterns

- [ ] Any pattern used has a clear **reason** (duplication, variation, or boundary).
- [ ] No cargo-cult pattern (e.g., Factory with a single implementation and no plan for variation).
- [ ] Pattern improves readability or testability, not the opposite.

## 5. Tests and professionalism

- [ ] Touched code has or is covered by tests where appropriate.
- [ ] No "we'll fix it later" or "TODO: refactor" that clearly violates sustainable pace or quality.
- [ ] Commit/PR is coherent and does not leave the codebase worse.

---

## Suggested output format for review

1. **Boundaries**: One or two sentences on dependency direction and any violations.
2. **SOLID**: List any violations with file/function and principle (e.g., "SRP: `OrderService` parses and persists — split.").
3. **Smells**: List smells found with location (e.g., "Rigidity: changing discount rule touches 4 files.").
4. **Concrete refactors**: One or two specific suggestions (e.g., "Extract `applyDiscount` from `process`"; "Introduce `OrderRepository` interface and inject in the use case.").
5. **Tests / professionalism**: Brief note on test coverage and any concerns.

---

*Use with the skill: @uncle-bob-craft. For naming, functions, and formatting detail, also use @clean-code. Always run the project linter and formatter separately.*
