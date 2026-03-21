---
title: "Security Ownership Map"
description: "Analyze git repositories to build a security ownership topology (people-to-file), compute bus factor and sensitive-code ownership, and export CSV/JSON for graph databases and visualization. Trigger only when the user explicitly wants a security-or..."
category: "research"
source: "community"
author: "Community"
tags: ["security", "ownership", "map"]
date: 2026-03-20
---

# Security Ownership Map

## Overview

Build a bipartite graph of people and files from git history, then compute ownership risk and export graph artifacts for Neo4j/Gephi. Also build a file co-change graph (Jaccard similarity on shared commits) to cluster files by how they move together while ignoring large, noisy commits.

## Requirements

- Python 3
- `networkx` (required; community detection is enabled by default)

Install with:

```bash
pip install networkx
```

## Workflow

1. Scope the repo and time window (optional `--since/--until`).
2. Decide sensitivity rules (use defaults or provide a CSV config).
3. Build the ownership map with `scripts/run_ownership_map.py` (co-change graph is on by default; use `--cochange-max-files` to ignore supernode commits).
4. Communities are computed by default; graphml output is optional (`--graphml`).
5. Query the outputs with `scripts/query_ownership.py` for bounded JSON slices.
6. Persist and visualize (see `references/neo4j-import.md`).

By default, the co-change graph ignores common “glue” files (lockfiles, `.github/*`, editor config) so clusters reflect actual code movement instead of shared infra edits. Override with `--cochange-exclude` or `--no-default-cochange-excludes`. Dependabot commits are excluded by default; override with `--no-default-author-excludes` or add patterns via `--author-exclude-regex`.

If you want to exclude Linux build glue like `Kbuild` from co-change clustering, pass:

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo /path/to/linux \
  --out ownership-map-out \
  --cochange-exclude "**/Kbuild"
```

## Quick start

Run from the repo root:

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --since "12 months ago" \
  --emit-commits
```

Defaults: author identity, author date, and merge commits excluded. Use `--identity committer`, `--date-field committer`, or `--include-merges` if needed.

Example (override co-change excludes):

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --cochange-exclude "**/Cargo.lock" \
  --cochange-exclude "**/.github/**" \
  --no-default-cochange-excludes
```

Communities are computed by default. To disable:

```bash
python skills/skills/security-ownership-map/scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --no-communities
```

## Sensitivity rules

By default, the script flags common auth/crypto/secret paths. Override by providing a CSV file:

```
# pattern,tag,weight
**/auth/**,auth,1.0
**/crypto/**,crypto,1.0
**/*.pem,secrets,1.0
```

Use it with `--sensitive-config path/to/sensitive.csv`.

## Output artifacts

`ownership-map-out/` contains:

- `people.csv` (nodes: people)
- `files.csv` (nodes: files)
- `edges.csv` (edges: touches)
- `cochange_edges.csv` (file-to-file co-change edges with Jaccard weight; omitted with `--no-cochange`)
- `summary.json` (security ownership findings)
- `commits.jsonl` (optional, if `--emit-commits`)
- `communities.json` (computed by default from co-change edges when available; includes `maintainers` per community; disable with `--no-communities`)
- `cochange.graph.json` (NetworkX node-link JSON with `community_id` + `community_maintainers`; falls back to `ownership.graph.json` if no co-change edges)
- `ownership.graphml` / `cochange.graphml` (optional, if `--graphml`)

`people.csv` includes timezone detection based on author commit offsets: `primary_tz_offset`, `primary_tz_minutes`, and `timezone_offsets`.

## LLM query helper

Use `scripts/query_ownership.py` to return small, JSON-bounded slices without loading the full graph into context.

Examples:

```bash
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out people --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag auth --bus-factor-max 1
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out person --person alice@corp --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out file --file crypto/tls
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out cochange --file crypto/tls --limit 10
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section orphaned_sensitive_code
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out community --id 3
```

Use `--community-top-owners 5` (default) to control how many maintainers are stored per community.

## Basic security queries

Run these to answer common security ownership questions with bounded output:

```bash
# Orphaned sensitive code (stale + low bus factor)
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section orphaned_sensitive_code

# Hidden owners for sensitive tags
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section hidden_owners

# Sensitive hotspots with low bus factor
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out summary --section bus_factor_hotspots

# Auth/crypto files with bus factor <= 1
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag auth --bus-factor-max 1
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out files --tag crypto --bus-factor-max 1

# Who is touching sensitive code the most
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out people --sort sensitive_touches --limit 10

# Co-change neighbors (cluster hints for ownership drift)
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out cochange --file path/to/file --min-jaccard 0.05 --limit 20

# Community maintainers (for a cluster)
python skills/skills/security-ownership-map/scripts/query_ownership.py --data-dir ownership-map-out community --id 3

# Monthly maintainers for the community containing a file
python skills/skills/security-ownership-map/scripts/community_maintainers.py \
  --data-dir ownership-map-out \
  --file network/card.c \
  --since 2025-01-01 \
  --top 5

# Quarterly buckets instead of monthly
python skills/skills/security-ownership-map/scripts/community_maintainers.py \
  --data-dir ownership-map-out \
  --file network/card.c \
  --since 2025-01-01 \
  --bucket quarter \
  --top 5
```

Notes:
- Touches default to one authored commit (not per-file). Use `--touch-mode file` to count per-file touches.
- Use `--window-days 90` or `--weight recency --half-life-days 180` to smooth churn.
- Filter bots with `--ignore-author-regex '(bot|dependabot)'`.
- Use `--min-share 0.1` to show stable maintainers only.
- Use `--bucket quarter` for calendar quarter groupings.
- Use `--identity committer` or `--date-field committer` to switch from author attribution.
- Use `--include-merges` to include merge commits (excluded by default).

### Summary format (default)

Use this structure, add fields if needed:

```json
{
  "orphaned_sensitive_code": [
    {
      "path": "crypto/tls/handshake.rs",
      "last_security_touch": "2023-03-12T18:10:04+00:00",
      "bus_factor": 1
    }
  ],
  "hidden_owners": [
    {
      "person": "alice@corp",
      "controls": "63% of auth code"
    }
  ]
}
```

## Graph persistence

Use `references/neo4j-import.md` when you need to load the CSVs into Neo4j. It includes constraints, import Cypher, and visualization tips.

## Notes

- `bus_factor_hotspots` in `summary.json` lists sensitive files with low bus factor; `orphaned_sensitive_code` is the stale subset.
- If `git log` is too large, narrow with `--since` or `--until`.
- Compare `summary.json` against CODEOWNERS to highlight ownership drift.

---

## Reference: Neo4J Import

# Neo4j Import Notes

Use these steps when persisting the ownership graph to Neo4j.

## Quick import (LOAD CSV)

1. Copy `people.csv`, `files.csv`, and `edges.csv` into the Neo4j import directory.
2. Run the following Cypher from Neo4j Browser or `cypher-shell`:

```cypher
CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT file_id IF NOT EXISTS FOR (f:File) REQUIRE f.id IS UNIQUE;

LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (p:Person {id: row.person_id})
SET p.name = row.name,
    p.email = row.email,
    p.first_seen = row.first_seen,
    p.last_seen = row.last_seen,
    p.commit_count = toInteger(row.commit_count),
    p.touches = toInteger(row.touches),
    p.sensitive_touches = toFloat(row.sensitive_touches),
    p.primary_tz_offset = CASE row.primary_tz_offset WHEN '' THEN null ELSE row.primary_tz_offset END,
    p.primary_tz_minutes = CASE row.primary_tz_minutes WHEN '' THEN null ELSE toInteger(row.primary_tz_minutes) END,
    p.timezone_offsets = CASE row.timezone_offsets WHEN '' THEN null ELSE row.timezone_offsets END;

LOAD CSV WITH HEADERS FROM 'file:///files.csv' AS row
MERGE (f:File {id: row.file_id})
SET f.path = row.path,
    f.first_seen = row.first_seen,
    f.last_seen = row.last_seen,
    f.commit_count = toInteger(row.commit_count),
    f.touches = toInteger(row.touches),
    f.bus_factor = toInteger(row.bus_factor),
    f.sensitivity_score = toFloat(row.sensitivity_score),
    f.sensitivity_tags = row.sensitivity_tags;

LOAD CSV WITH HEADERS FROM 'file:///edges.csv' AS row
MATCH (p:Person {id: row.person_id})
MATCH (f:File {id: row.file_id})
MERGE (p)-[r:TOUCHES]->(f)
SET r.touches = toInteger(row.touches),
    r.recency_weight = toFloat(row.recency_weight),
    r.first_seen = row.first_seen,
    r.last_seen = row.last_seen,
    r.sensitive_weight = toFloat(row.sensitive_weight);

LOAD CSV WITH HEADERS FROM 'file:///cochange_edges.csv' AS row
MATCH (f1:File {id: row.file_a})
MATCH (f2:File {id: row.file_b})
MERGE (f1)-[r:COCHANGES]->(f2)
SET r.cochange_count = toInteger(row.cochange_count),
    r.jaccard = toFloat(row.jaccard);
```

## Visualization tips

- Use Neo4j Bloom or Browser with `MATCH (p:Person)-[r:TOUCHES]->(f:File) RETURN p,r,f`.
- Filter by `f.sensitivity_score > 0` to highlight security-relevant clusters.
- For Gephi, import `edges.csv` as edges and `files.csv` / `people.csv` as nodes.
