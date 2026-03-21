---
title: "Perf Theory Tester"
description: "Use when running controlled perf experiments to validate hypotheses."
category: "development"
source: "community"
author: "Community"
tags: ["perf", "theory", "tester"]
date: 2026-03-20
---

# perf-theory-tester

Test hypotheses using controlled experiments.

Follow `docs/perf-requirements.md` as the canonical contract.

## Required Steps

1. Confirm baseline is clean.
2. Apply a single change tied to the hypothesis.
3. Run 2+ validation passes.
4. Revert to baseline before the next experiment.

## Output Format

```
hypothesis: <id>
change: <summary>
delta: <metrics>
verdict: accept|reject|inconclusive
evidence:
  - command: <benchmark command>
  - files: <changed files>
```

## Constraints

- One change per experiment.
- No parallel benchmarks.
- Record evidence for each run.

