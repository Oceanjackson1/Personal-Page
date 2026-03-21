---
title: "Perf Code Paths"
description: "Use when mapping code paths, entrypoints, and likely hot files before profiling."
category: "development"
source: "community"
author: "Community"
tags: ["perf", "code", "paths"]
date: 2026-03-20
---

# perf-code-paths

Identify likely implementation paths for a performance scenario.

Follow `docs/perf-requirements.md` as the canonical contract.

## Required Steps

1. Use repo-map if available; otherwise use grep for entrypoints and handlers.
2. List top candidate files/symbols tied to the scenario.
3. Include imports/exports or call chains when relevant.

## Output Format

```
keywords: <comma-separated list>
paths:
  - file: <path>
    symbols: [<symbol1>, <symbol2>]
    evidence: <short reason>
```

## Constraints

- Focus only on supported languages (Rust, Java, JS/TS, Go, Python).
- Keep to the most relevant 10-15 files.

