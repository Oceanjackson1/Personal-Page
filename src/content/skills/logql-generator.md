---
title: "Logql Generator"
description: "Generate LogQL queries, log stream selectors, metric queries, and alerting rules for Grafana Loki."
category: "devops"
source: "community"
author: "Community"
tags: ["logql", "generator"]
date: 2026-03-20
---

# LogQL Query Generator

## Overview

Interactive workflow for generating production-ready LogQL queries. LogQL is Grafana Loki's query language with indexed label selection, line filtering, parsing, and metric aggregation.

## Trigger Hints

- "Write a LogQL query for error rate by service."
- "Help me build a Loki alert query."
- "Convert this troubleshooting requirement into LogQL."
- "I need step-by-step LogQL query construction."

Use this skill for query generation, dashboard queries, alerting expressions, and troubleshooting with Loki logs.

## Execution Flow (Deterministic)

Always run stages in order. Do not skip required stages.

### Stage 1 (Required): Capture Intent

Use `AskUserQuestion` to collect goal and use case.

Template:
- "What is your primary goal: debugging, alerting, dashboard metric, or investigation?"
- "Do you need a log query (raw lines) or a metric query (numeric output)?"
- "What time window should this cover (example: last 15m, 1h, 24h)?"

Fallback if `AskUserQuestion` is unavailable:
- Ask the same questions in plain text and continue.

### Stage 2 (Required): Capture Log Source Details

Collect:
1. Labels for stream selectors (`job`, `namespace`, `app`, `service_name`, `cluster`)
2. Log format (JSON, logfmt, plain text, mixed)
3. Known fields to filter/aggregate (`status`, `level`, `duration`, `path`, `trace_id`)

Ambiguity and partial-answer handling:
1. If a required field is missing, ask one focused follow-up question.
2. If still missing, proceed with explicit assumptions.
3. Prefix assumptions with `Assumptions:` in the output so the user can correct them quickly.

### Stage 3 (Required): Discover Loki and Grafana Versions

Collect or infer:
- Loki version (example: `2.9.x`, `3.0+`, unknown)
- Grafana version (example: `10.x`, `11.x`, unknown)
- Deployment context (self-hosted Loki, Grafana Cloud, unknown)

Version compatibility policy:
1. If versions are known, use the newest compatible syntax only.
2. If versions are unknown, use compatibility-first syntax and avoid 3.x-only features by default.
3. For unknown versions, provide an optional "3.x optimized variant" separately.

Avoid by default when version is unknown:
- Pattern match operators `|>` and `!>`
- `approx_topk`
- Structured metadata specific behavior (`detected_level`, accelerated metadata filtering assumptions)

### Stage 4 (Required): Plan Confirmation and Output Mode

Present a plain-English plan, then ask the user to choose output mode.

Plan template:
```text
LogQL Query Plan
Goal: <goal>
Query type: <log or metric>
Streams: <selector>
Filters/parsing: <filters + parser>
Aggregation window: <function and [range]>
Compatibility mode: <version-aware or compatibility-first>
```

Mode selection template:
- "Do you want `final query only` (default) or `incremental build` (step-by-step)?"

If user does not choose, default to `final query only`.

### Stage 5 (Conditional, Blocking): Reference Checkpoint for Complex Queries

Complex query triggers:
- Nested aggregations (`topk(sum by(...))`, multiple `sum by`, percentiles)
- Performance-sensitive queries (high volume streams, long ranges)
- Alerting expressions
- Template functions (`line_format`, `label_format`)
- Regex-heavy extraction, IP matching, pattern parsing
- Loki 3.x feature usage

Blocking checkpoint rule:
1. Read relevant files before generation using explicit file-open/read actions.
2. Minimum file set:
   - `examples/common_queries.logql` for syntax and query patterns
   - `references/best_practices.md` for performance and alerting guidance
3. Do not generate the final query until this checkpoint is complete.

Fallback when file-read tools are unavailable:
1. State that reference files could not be read in this environment.
2. Generate a conservative query (compatibility-first, simpler operators).
3. Mark result as `Unverified against local references`.

### Stage 6 (Conditional): External Docs Lookup Policy (Context7 Before WebSearch)

Use external lookup only for version-specific behavior, unclear syntax, or advanced features not covered in local references.

Decision order:
1. Context7 first:
   - `mcp__context7__resolve-library-id` with `libraryName="grafana loki"`
   - `mcp__context7__query-docs` for the exact topic
2. WebSearch second (fallback only) when:
   - Context7 is unavailable
   - Context7 does not provide required version-specific detail
   - You need latest release/deprecation confirmation

WebSearch fallback constraints:
- Prefer official Grafana/Loki docs and release notes.
- Note which statement came from fallback search.

### Stage 7 (Required): Generate Query

#### Stage 7A (Default): Final Query Only

Return one production-ready query plus short explanation.

#### Stage 7B (Optional): Incremental Build Mode

Use this when requested or when debugging complex pipelines.

Step-by-step template:
1. Stream selector
2. Line filter
3. Parser
4. Parsed-field filter
5. Aggregation/window

### Stage 8 (Required): Deliver Usage and Checks

Always include:
1. Final query or incremental sequence
2. How to run it (Grafana Explore/panel or `logcli`)
3. Tunables (labels, thresholds, range)
4. Any assumptions and compatibility notes

## AskUserQuestion Templates

### Intake Template
- "What system/service should this query target?"
- "Which labels are reliable for stream selection?"
- "What defines a match (error text, status code, latency threshold, user path)?"
- "Should output be raw logs or a metric for alert/dashboard?"

### Version Template
- "What Loki version are you running?"
- "What Grafana version are you using?"
- "If unknown, should I generate a compatibility-first query and add an optional 3.x variant?"

### Ambiguity Follow-up Template
- "I am missing `<field>`. Should I assume `<default>` so I can continue?"

## Core Patterns

### Stream Selection and Filtering
```logql
{job="app"} |= "error" |= "timeout"
{job="app"} |~ "error|fatal|critical"
{job="app"} != "debug"
```

### Parsing
```logql
{app="api"} | json | level="error" | status_code >= 500
{app="api"} | logfmt | caller="database.go"
{job="nginx"} | pattern "<ip> - - [<_>] \"<method> <path>\" <status> <size>"
```

### Metric Aggregation
```logql
rate({job="app"} | json | level="error" [5m])
sum by (app) (count_over_time({namespace="prod"} | json [5m]))
sum(rate({app="api"} | json | level="error" [5m])) / sum(rate({app="api"}[5m])) * 100
quantile_over_time(0.95, {app="api"} | json | unwrap duration [5m])
topk(10, sum by (error_type) (count_over_time({job="app"} | json | level="error" [1h])))
```

### Formatting and IP Matching
```logql
{job="app"} | json | line_format "{{.level}}: {{.message}}"
{job="app"} | json | label_format env=`{{.environment}}`
{job="nginx"} | logfmt | remote_addr = ip("192.168.4.0/24")
```

## Query Construction Rules

1. Use specific stream selectors (indexed labels first).
2. Prefer filter order: line filter -> parse -> parsed-field filter.
3. Prefer parser cost order: `pattern` > `logfmt` > `json` > `regexp`.
4. For unknown Loki version, stay on compatibility-first syntax.
5. For complex/critical queries, complete Stage 5 checkpoint before final output.

## Advanced Techniques

### Multiple Parsers
```logql
{app="api"} | json | regexp "user_(?P<user_id>\\d+)"
```

### Unwrap for Numeric Metrics
```logql
sum(sum_over_time({app="api"} | json | unwrap duration [5m]))
```

### Pattern Match Operators (Loki 3.0+, 10x faster than regex)
```logql
{service_name=`app`} |> "<_> level=debug <_>"
```

### Logical Operators
```logql
{app="api"} | json | (status_code >= 400 and status_code < 500) or level="error"
```

### Offset Modifier
```logql
sum(rate({app="api"} | json | level="error" [5m])) - sum(rate({app="api"} | json | level="error" [5m] offset 1d))
```

### Label Operations
```logql
{app="api"} | json | keep namespace, pod, level
{app="api"} | json | drop pod, instance
```

> **Note**: LogQL has no `dedup` or `distinct` operators. Use metric aggregations like `sum by (field)` for programmatic deduplication.

## Loki 3.x Key Features

### Structured Metadata
High-cardinality data without indexing (trace_id, user_id, request_id):
```logql
# Filter AFTER stream selector, NOT in it
{app="api"} | trace_id="abc123" | json | level="error"
```

### Query Acceleration (Bloom Filters)
Place structured metadata filters BEFORE parsers:
```logql
# ACCELERATED
{cluster="prod"} | detected_level="error" | logfmt | json
# NOT ACCELERATED
{cluster="prod"} | logfmt | json | detected_level="error"
```

### approx_topk (Probabilistic)
```logql
approx_topk(10, sum by (endpoint) (rate({app="api"}[5m])))
```

### vector() for Alerting
```logql
sum(count_over_time({app="api"} | json | level="error" [5m])) or vector(0)
```

### Automatic Labels
- **service_name**: Auto-populated from container name
- **detected_level**: Auto-detected when `discover_log_levels: true` (stored as structured metadata)

## Function Reference

### Log Range Aggregations
| Function | Description |
|----------|-------------|
| `rate(log-range)` | Entries per second |
| `count_over_time(log-range)` | Count entries |
| `bytes_rate(log-range)` | Bytes per second |
| `bytes_over_time(log-range)` | Total bytes in time range |
| `absent_over_time(log-range)` | Returns 1 if no logs |

Rule:
- Use `bytes_over_time(<log-range>)` for raw log-byte volume.
- Use `| unwrap bytes(field)` with unwrapped range aggregations for numeric byte fields extracted from log content.

### Unwrapped Range Aggregations
| Function | Description |
|----------|-------------|
| `sum_over_time`, `avg_over_time`, `max_over_time`, `min_over_time` | Aggregate numeric values |
| `quantile_over_time(φ, range)` | φ-quantile (0 ≤ φ ≤ 1) |
| `first_over_time`, `last_over_time` | First/last value in interval |
| `stddev_over_time` | Population standard deviation of unwrapped values |
| `stdvar_over_time` | Population variance of unwrapped values |
| `rate_counter` | Per-second rate treating values as a monotonically increasing counter |

### Aggregation Operators
`sum`, `avg`, `min`, `max`, `count`, `stddev`, `topk`, `bottomk`, `approx_topk`, `sort`, `sort_desc`

With grouping: `sum by (label1, label2)` or `sum without (label1)`

### Conversion Functions
| Function | Description |
|----------|-------------|
| `duration_seconds(label)` | Convert duration string |
| `bytes(label)` | Convert byte string (KB, MB) |

### label_replace()
```logql
label_replace(rate({job="api"} |= "err" [1m]), "foo", "$1", "service", "(.*):.*")
```

## Parser Reference

### logfmt
```logql
| logfmt [--strict] [--keep-empty]
```
- `--strict`: Error on malformed entries
- `--keep-empty`: Keep standalone keys

### JSON
```logql
| json                                           # All fields
| json method="request.method", status="response.status"  # Specific fields
| json servers[0], headers="request.headers[\"User-Agent\"]"  # Nested/array
```

### pattern
```logql
| pattern "<ip> - - [<timestamp>] \"<method> <path> <_>\" <status> <size>"
```
Named placeholders become extracted labels; `<_>` discards a field.

### regexp
```logql
| regexp "(?P<level>\\w+): (?P<message>.+)"
```
Uses named capture groups (`?P<name>`). Slower than `pattern`/`logfmt`/`json`.

### decolorize
```logql
| decolorize
```
Strips ANSI color escape codes. Apply before parsing when logs come from terminal output.

### unpack
```logql
| unpack
```
Unpacks log entries that were packed by Promtail's `pack` pipeline stage. Restores the original log line and any embedded labels.

## Template Functions

Common functions for `line_format` and `label_format`:

**String**: `trim`, `upper`, `lower`, `replace`, `trunc`, `substr`, `printf`, `contains`, `hasPrefix`
**Math**: `add`, `sub`, `mul`, `div`, `addf`, `subf`, `floor`, `ceil`, `round`
**Date**: `date`, `now`, `unixEpoch`, `toDate`, `duration_seconds`
**Regex**: `regexReplaceAll`, `count`
**Other**: `fromJson`, `default`, `int`, `float64`, `__line__`, `__timestamp__`

See `examples/common_queries.logql` for detailed usage.

## Alerting Rules

```logql
# Alert when error rate exceeds 5%
(sum(rate({app="api"} | json | level="error" [5m])) / sum(rate({app="api"}[5m]))) > 0.05

# With vector() to avoid "no data"
sum(rate({app="api"} | json | level="error" [5m])) or vector(0) > 10
```

## Error Handling

| Issue | Solution |
|-------|----------|
| No results | Check labels exist, verify time range, test stream selector alone |
| Query slow | Use specific selectors, filter before parsing, reduce time range |
| Parse errors | Verify log format matches parser, test JSON validity |
| High cardinality | Use line filters not label filters for unique values, aggregate |

## Documentation Lookup

Use Stage 6 policy. Trigger external docs for:

| Trigger | Topic to Search | Tool to Use |
|---------|-----------------|-------------|
| User mentions Loki 3.x features | `structured metadata`, `bloom filters`, `detected_level` | Context7 first |
| `approx_topk` function needed | `approx_topk probabilistic` | Context7 first |
| Pattern match operators (`\|>`, `!>`) | `pattern match operator` | Context7 first |
| `vector()` function for alerting | `vector function alerting` | Context7 first |
| Recording rules configuration | `recording rules loki` | Context7 first |
| Unclear syntax or edge cases | Specific function/operator | Context7 first |
| Version-specific behavior questions | Version + feature | WebSearch fallback |
| Grafana Alloy integration | `grafana alloy loki` | WebSearch fallback |

## Resources

- `examples/common_queries.logql`: Query patterns, template function examples
- `references/best_practices.md`: Optimization, anti-patterns, alerting guidance

## Example Flows

### Example A: Final Query Only (Default)
1. User asks for 5xx rate by service over 15m.
2. Capture labels and format (`json`).
3. Confirm version and mode (`final query only`).
4. Generate one query:
```logql
sum by (service) (rate({namespace="prod", app="api"} | json | status_code >= 500 [15m]))
```

### Example B: Incremental Build (Optional)
1. User asks to debug login failures and requests step-by-step mode.
2. Provide staged build:
```logql
{app="auth"}
{app="auth"} |= "login failed"
{app="auth"} |= "login failed" | json
sum(count_over_time({app="auth"} |= "login failed" | json [5m]))
```
3. Explain where to stop if any step returns zero results.

## Done Criteria

Mark task done only when all checks pass:
1. Required stages (1, 2, 3, 4, 7, 8) were completed.
2. Stage 5 checkpoint was completed for any complex query.
3. Stage 6 lookup order followed Context7 before WebSearch when external docs were needed.
4. Output mode was explicitly selected or defaulted (`final query only`).
5. Loki/Grafana compatibility assumptions were stated when versions were unknown.
6. Final output includes query text, usage note, tunables, and assumptions.

## Version Notes

- **Loki 3.0+**: Bloom filters, structured metadata, pattern match operators (`|>`, `!>`)
- **Loki 3.3+**: `approx_topk` function
- **Loki 3.5+**: Promtail deprecated (use Grafana Alloy)
- **Loki 3.6+**: Horizontally scalable compactor, Loki UI as Grafana plugin

> **Deprecations**: Promtail (use Alloy), BoltDB store (use TSDB with v13 schema)

---

## Reference: Best_Practices

# LogQL Best Practices

This document outlines best practices for writing efficient, maintainable, and performant LogQL queries in Grafana Loki.

## Query Structure and Performance

### 1. Use Specific Stream Selectors

Always use the most specific label selectors possible to reduce the number of streams Loki needs to search.

**Good:**
```logql
{namespace="production", app="api-server", environment="prod"}
```

**Bad:**
```logql
{namespace="production"}  # Too broad, searches many streams
```

**Why:** Loki indexes logs by label combinations (streams). More specific selectors mean fewer streams to search, resulting in faster queries.

### 2. Order Operations Efficiently

Apply filters in the most efficient order: stream selector → line filters → parser → label filters → aggregations.

**Good:**
```logql
{job="nginx"} |= "error" | json | status_code >= 500 | sum(count_over_time([5m]))
```

**Bad:**
```logql
{job="nginx"} | json | status_code >= 500 |= "error"  # Parse before line filter
```

**Why:** Line filters are fast and work on raw log lines. Parsers are more expensive. Apply cheap operations first to reduce data early.

### 3. Use Line Filters Before Parsing

Filter out irrelevant log lines before parsing to reduce computational overhead.

**Good:**
```logql
{app="api"} |= "error" | json | level="error"
```

**Bad:**
```logql
{app="api"} | json | level="error"  # Parses all logs, not just errors
```

**Why:** Line filters (|=, !=, |~, !~) are extremely fast string operations. Parsing (json, logfmt, regexp) is more expensive.

### 4. Avoid Complex Regex When Simple Matching Works

Use exact string matching when possible instead of regex.

**Good:**
```logql
{job="app"} |= "ERROR:"  # Fast string match
```

**Bad:**
```logql
{job="app"} |~ "ERROR:"  # Slower regex match for simple string
```

**Why:** Regex matching requires compilation and more complex pattern matching. Simple string contains is significantly faster.

### 5. Use Appropriate Time Ranges

Use the shortest time range that satisfies your requirements.

**Good:**
```logql
rate({app="api"}[1m])  # For real-time dashboards
rate({app="api"}[1h])  # For trend analysis
```

**Bad:**
```logql
rate({app="api"}[24h])  # Unnecessarily long for real-time monitoring
```

**Why:** Larger time ranges mean more data to process. Match the range to your use case.

## Label Management

### 6. Understand Label vs Line Filter Trade-offs

Use labels for indexed dimensions, line filters for unique values.

**Good (using line filter for unique ID):**
```logql
{app="api"} |= "trace_id=abc123"
```

**Bad (would create high cardinality if trace_id was a label):**
```logql
{app="api", trace_id="abc123"}  # Don't do this!
```

**Why:** Labels create separate streams and indexes. High cardinality labels (user IDs, trace IDs, session IDs) create too many streams, degrading performance.

### 7. Keep Cardinality Low

Avoid using high-cardinality data as labels in stream selectors.

**High cardinality fields (use line filters instead):**
- user_id
- trace_id
- request_id
- session_id
- ip_address (individual IPs)
- timestamp

**Good cardinality fields (suitable for labels):**
- namespace
- app
- environment
- cluster
- level (error, warn, info)
- pod (in moderation)
- job
- host (in moderation)

**Why:** Each unique combination of labels creates a new stream. Too many streams overwhelm Loki's indexing.

### 8. Use Label Operations Wisely

Drop unnecessary labels to reduce series cardinality in metric queries.

**Good:**
```logql
{app="api"} | json | drop instance, pod | sum by (namespace, app) (rate([5m]))
```

**Why:** Fewer labels in results = fewer time series = better performance and lower memory usage.

## Parsing Best Practices

### 9. Choose the Right Parser

Use the most appropriate parser for your log format.

| Log Format | Parser | Example |
|------------|--------|---------|
| Custom patterns | `pattern` | `{app="nginx"} \| pattern "<ip> <_> <status>"` |
| key=value pairs | `logfmt` | `{app="api"} \| logfmt` |
| key=value (strict) | `logfmt --strict` | `{app="api"} \| logfmt --strict` |
| JSON | `json` | `{app="api"} \| json` |
| JSON (specific fields) | `json` | `{app="api"} \| json status="response.code"` |
| Complex regex | `regexp` | `{app="api"} \| regexp "(?P<level>\\w+)"` |

**Performance order (fastest to slowest):** pattern > logfmt > json > regexp

**Why this order matters:**
- **pattern**: Simple string matching with placeholders, fastest execution
- **logfmt**: Optimized key=value parsing, very efficient
- **json**: Full JSON parsing, moderate overhead
- **regexp**: Regex compilation and matching, slowest but most flexible

**Why:** Simpler parsers are faster. JSON and logfmt are optimized. Pattern is faster than regex for simple cases.

### 9a. Use logfmt Parser Flags When Needed

The logfmt parser supports optional flags for handling edge cases:

**`--strict` flag:**
```logql
# Fail on malformed key=value pairs (stops scanning on error)
{app="api"} | logfmt --strict

# Use when you need to detect malformed log entries
{app="api"} | logfmt --strict | __error__ != ""
```

**`--keep-empty` flag:**
```logql
# Retain standalone keys as labels with empty string value
{app="api"} | logfmt --keep-empty

# Combine flags
{app="api"} | logfmt --strict --keep-empty
```

**When to use:**
- `--strict`: When log quality matters and you want to detect malformed entries
- `--keep-empty`: When logs have standalone keys (no values) that need to be preserved

**Why:** By default, logfmt is non-strict (skips invalid tokens) which is more lenient but may hide log quality issues.

### 9b. Use JSON Parser Parameter Extraction for Performance

Extract only the fields you need instead of parsing entire JSON:

**Good (extract specific fields):**
```logql
{app="api"} | json status="response.code", method="request.method"
```

**Less efficient (parse all fields):**
```logql
{app="api"} | json
```

**Supported access patterns:**
- Dot notation: `| json method="request.method"`
- Bracket notation: `| json ua="headers[\"User-Agent\"]"`
- Array access: `| json first="items[0]"`
- Combined: `| json item="data.items[0].name"`

**Why:** Extracting fewer fields reduces parsing overhead and memory usage.

### 10. Parse Only What You Need

If you only need specific fields, extract just those fields.

**Good:**
```logql
{app="api"} | json level, message, status_code
```

**Better than:**
```logql
{app="api"} | json  # Parses all fields
```

**Why:** Extracting fewer fields reduces parsing overhead and memory usage.

### 11. Use Pattern Parser for Simple Cases

Pattern parser is faster than regex for straightforward field extraction.

**Good:**
```logql
{job="nginx"} | pattern "<ip> - - [<timestamp>] \"<method> <path> <_>\" <status>"
```

**Avoid (unless necessary):**
```logql
{job="nginx"} | regexp "(?P<ip>\\S+) .* (?P<method>\\w+) (?P<path>\\S+).*"
```

**Why:** Pattern parser is simpler and faster for structured formats.

## Aggregation Best Practices

### 12. Use Appropriate Aggregation Functions

Choose the right function for your metric type.

| Metric Type | Function | Use Case |
|-------------|----------|----------|
| Count logs | `count_over_time()` | Number of log lines |
| Event rate | `rate()`, `bytes_rate()` | Events per second |
| Numeric extraction | `unwrap` + `sum_over_time()` | Sum of values |
| Percentiles | `quantile_over_time()` | Latency, duration |
| Statistics | `avg_over_time()`, `max_over_time()`, `min_over_time()` | Averages, extremes |

### 13. Aggregate Early and Often

Reduce data volume as early as possible.

**Good:**
```logql
sum by (namespace) (
  count_over_time({app="api"} | json | level="error" [5m])
)
```

**Why:** Aggregating reduces the number of time series, improving query performance.

### 14. Use `by` Instead of `without` When Possible

Explicitly specify labels to keep rather than labels to remove.

**Good:**
```logql
sum by (namespace, app) (rate({job="kubernetes-pods"}[5m]))
```

**Less efficient:**
```logql
sum without (pod, instance, node) (rate({job="kubernetes-pods"}[5m]))
```

**Why:** `by` is more explicit and often results in fewer output series.

## Query Optimization

### 15. Avoid Expensive Operations in Inner Loops

Don't use regex or complex parsing inside frequently-evaluated contexts.

**Good:**
```logql
sum(rate({app="api"} |= "error" [5m]))  # Filter first
```

**Bad:**
```logql
sum(rate({app="api"} | regexp "complex.*pattern" [5m]))  # Regex on every line
```

### 16. Use Metric Queries for Dashboards

For dashboard panels, use metric queries (aggregations) rather than log queries.

**Good (for time series panel):**
```logql
rate({app="api"}[5m])
```

**Bad (for time series panel):**
```logql
{app="api"}  # Returns log lines, not metrics
```

**Why:** Metric queries return time series data suitable for graphing.

### 17. Limit Log Query Results

When querying for log lines (not metrics), limit the result set.

**Important:** The `limit` is an **API parameter**, not a LogQL pipeline operator. Set it via:
- **API:** `/loki/api/v1/query_range?query={...}&limit=100`
- **Grafana UI:** "Line limit" field in the query editor (default: 1000)
- **logcli:** `--limit=100` flag

**Good:**
```bash
# Using logcli
logcli query '{app="api"} | json | level="error"' --limit=100

# Using API
curl -G "http://localhost:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={app="api"} | json | level="error"' \
  --data-urlencode 'limit=100'
```

**Why:** Returning thousands of log lines is slow and resource-intensive. Always set appropriate limits for log queries.

### 18. Use `__error__=""` to Filter Parse Errors

When parsing, filter out lines that fail to parse to get clean results.

**Good:**
```logql
{app="api"} | json | __error__="" | level="error"
```

**Why:** Parse errors create `__error__` labels. Filtering them out gives you only successfully parsed logs.

## Alerting Best Practices

### 19. Use Metric Queries for Alerts

Alerts require numeric values. Always use metric queries (aggregations).

**Good:**
```logql
sum(rate({app="api"} | json | level="error" [5m])) > 10
```

**Bad:**
```logql
{app="api"} | json | level="error"  # Returns logs, not metrics
```

### 20. Include Meaningful Thresholds

Set explicit, meaningful thresholds for alerting.

**Good:**
```logql
(
  sum(rate({app="api"} | json | level="error" [5m]))
  /
  sum(rate({app="api"}[5m]))
) > 0.05  # Alert if error rate > 5%
```

**Why:** Thresholds should be based on SLOs or historical baselines.

### 21. Use `absent_over_time` for Missing Logs

Detect when logs stop coming (potential service outage).

**Good:**
```logql
absent_over_time({app="critical-service"}[5m])
```

**Why:** This returns 1 when no logs match in the time range, indicating a potential problem.

## Security and Sensitive Data

### 22. Don't Log Sensitive Information

Avoid logging sensitive data that could appear in LogQL query results.

**Avoid in logs:**
- Passwords
- API keys
- Tokens
- Credit card numbers
- PII (personally identifiable information)

**If you must log sensitive data:**
- Use structured metadata (not indexed)
- Redact before ingestion
- Use Loki's data retention policies
- Restrict access with Loki's multi-tenancy

### 23. Use Structured Metadata for High-Cardinality Data

Store high-cardinality data as structured metadata, not labels.

**Good:**
```yaml
# In your log shipper config
structured_metadata:
  trace_id: ${TRACE_ID}
  user_id: ${USER_ID}
```

**Then query:**
```logql
{app="api"} | trace_id="abc123"
```

**Why:** Structured metadata is not indexed, avoiding cardinality issues.

## Maintenance and Debugging

### 24. Test Queries Incrementally

Build complex queries step by step, testing each stage.

**Approach:**
```logql
# Step 1: Test stream selector
{app="api"}

# Step 2: Add line filter
{app="api"} |= "error"

# Step 3: Add parser
{app="api"} |= "error" | json

# Step 4: Add label filter
{app="api"} |= "error" | json | status_code >= 500

# Step 5: Add aggregation
sum(count_over_time({app="api"} |= "error" | json | status_code >= 500 [5m]))
```

**Why:** Incremental testing helps identify issues early and understand query behavior.

### 25. Use `line_format` for Debugging

Format log output to see extracted fields during development.

**Debugging query:**
```logql
{app="api"} | json | line_format "level={{.level}} status={{.status_code}} message={{.message}}"
```

**Why:** Makes it easy to see what fields were extracted and their values.

### 26. Comment Complex Queries

Use LogQL comments to document complex queries.

**Good:**
```logql
# Calculate 5xx error rate as percentage
# Alerts when > 5% for SLO compliance
(
  sum(rate({app="api"} | json | status_code >= 500 [5m]))
  /
  sum(rate({app="api"}[5m]))
) * 100 > 5
```

**Why:** Comments help team members understand query intent and logic.

## Performance Tuning

### 27. Use Query Splitting for Large Time Ranges

For very large time ranges, consider splitting queries or using downsampling.

**Instead of:**
```logql
sum(count_over_time({app="api"}[30d]))  # Very expensive
```

**Consider:**
- Using Loki's query splitting (automatic in recent versions)
- Using recording rules for frequently-queried metrics
- Adjusting retention policies

### 28. Leverage Loki's Query Parallelization

Recent Loki versions automatically parallelize queries. Structure queries to take advantage:

**Good (parallelizable):**
```logql
sum by (namespace) (rate({job="kubernetes-pods"}[5m]))
```

**Why:** Loki can process different namespaces in parallel.

### 29. Use Appropriate Step Sizes

For metric queries over long time ranges, use appropriate step sizes.

**Good:**
```logql
# For 24h dashboard, use 1m step
rate({app="api"}[5m])  # With 1m step in Grafana

# For 7d dashboard, use 5m or 15m step
rate({app="api"}[15m])  # With 5m step
```

**Why:** Smaller steps = more data points = slower queries. Match resolution to your needs.

## Structured Metadata (Loki 3.x)

### 35. Use Structured Metadata for High-Cardinality Data

Structured metadata is metadata attached to logs without indexing. Introduced in Loki 3.0.

**What it is:**
- Metadata attached to logs that is NOT indexed
- Ideal for high-cardinality data (trace_id, user_id, request_id, pod names)
- Avoids index bloat and cardinality explosion
- Automatically extracted as labels in query results

**Key differences from labels:**
- Labels are indexed → fast stream selection, but high cardinality is expensive
- Structured metadata is NOT indexed → no cardinality impact, but requires scanning

**Query syntax:**
```logql
# Filter by structured metadata (AFTER stream selector, not inside it!)
{app="api"} | trace_id="abc123"

# Combine multiple structured metadata filters
{app="api"} | trace_id="abc123" | user_id="user456"

# Use with other filters
{app="api"} | trace_id="abc123" | json | level="error"
```

**WRONG (structured metadata is not a label):**
```logql
{app="api", trace_id="abc123"}  # This won't work!
```

**When to use:**
- OpenTelemetry data (trace IDs, span IDs)
- High-cardinality identifiers (user IDs, request IDs, session IDs)
- Kubernetes metadata (pod UIDs, container IDs)
- Any data that would create too many unique label combinations

**Configuration (requires Loki 3.0+ with schema v13+):**
```yaml
limits_config:
  allow_structured_metadata: true
```

### 36. Query Acceleration with Structured Metadata

Loki 3.x can accelerate queries using bloom filters when structured metadata filters are placed correctly.

**CRITICAL: Filter Order Matters for Acceleration**

**Accelerated (bloom filters used):**
```logql
{cluster="prod"} | detected_level="error" | logfmt | json
```
The structured metadata filter comes BEFORE parsers.

**NOT Accelerated (bloom filters NOT used):**
```logql
{cluster="prod"} | logfmt | json | detected_level="error"
```
The filter comes AFTER parsers, preventing acceleration.

**Rules for query acceleration:**
1. Use string equality filters: `| key="value"`
2. Place structured metadata filters BEFORE any parser expressions
3. Filters BEFORE `logfmt`, `json`, `pattern`, `regexp`, `label_format`, `label_replace`

**Supported filter patterns:**
```logql
# Simple equality (accelerated)
{app="api"} | trace_id="abc123" | json

# Multiple filters with OR (accelerated)
{app="api"} | detected_level="error" or detected_level="warn" | json

# Multiple filters with AND (accelerated)
{app="api"} | service="api" and environment="prod" | json
```

**Why this matters:**
- Bloom filters can skip chunks that definitely don't contain the data
- Significant performance improvement for "needle in haystack" queries
- Essential for large-scale deployments (75TB+ monthly logs)

## __error__ Label Debugging

### 37. Debug Parse Errors with __error__ Label

When parsing fails, Loki creates an `__error__` label with the error type.

**Show only lines that failed to parse:**
```logql
{app="api"} | json | __error__ != ""
```

**Show only successfully parsed lines (filter OUT errors):**
```logql
{app="api"} | json | __error__=""
```

**Common error values:**
- `JSONParserErr` - Invalid JSON
- `LogfmtParserErr` - Invalid logfmt
- `PatternParserErr` - Pattern didn't match
- `RegexpParserErr` - Regex didn't match

**Debugging workflow:**
```logql
# Step 1: See which lines are failing
{app="api"} | json | __error__ != "" | line_format "ERROR: {{.__error__}} LINE: {{.__line__}}"

# Step 2: Count errors by type
sum by (__error__) (count_over_time({app="api"} | json | __error__ != "" [5m]))

# Step 3: Production query (exclude errors)
{app="api"} | json | __error__="" | level="error"
```

**Why this matters:**
- Silent parse failures can cause missing data
- Always filter `__error__=""` in production dashboards
- Use error queries to debug log format issues

## Recording Rules

### 38. Use Recording Rules for Expensive Queries

Recording rules precompute expensive queries and store results as metrics.

**When to use recording rules:**
- Dashboard queries that run frequently
- Complex aggregations over large datasets
- Queries that would otherwise time out
- Per-tenant alerting in multi-tenant systems

**Example recording rule configuration:**
```yaml
# /tmp/loki/rules/<tenant-id>/rules.yaml
groups:
  - name: error_rates
    interval: 1m
    rules:
      # Record error rate per app
      - record: app:error_rate:1m
        expr: |
          sum by (app) (
            rate({job="kubernetes-pods"} | json | level="error" [1m])
          )
        labels:
          source: loki_recording_rule

      # Record request rate per namespace
      - record: namespace:request_rate:5m
        expr: |
          sum by (namespace) (
            rate({job="kubernetes-pods"}[5m])
          )

  - name: alerting_rules
    interval: 1m
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum by (app) (rate({job="app"} | json | level="error" [5m]))
            /
            sum by (app) (rate({job="app"}[5m]))
          ) > 0.05
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High error rate for {{ $labels.app }}"
          description: "Error rate is {{ $value | printf \"%.2f\" }}%"
```

**Ruler configuration:**
```yaml
ruler:
  storage:
    type: local
    local:
      directory: /tmp/loki/rules
  rule_path: /tmp/scratch
  alertmanager_url: http://alertmanager:9093
  enable_api: true
  ring:
    kvstore:
      store: inmemory
```

**Benefits:**
- Reduces query load on Loki
- Faster dashboard loading
- Consistent results across queries
- Enables alerting on complex conditions

### 39. Use vector() for Reliable Alerting

The `vector()` function ensures alerting rules always return a value.

**Problem:** When no logs match, the query returns nothing, causing "no data" alert states.

**Solution:**
```logql
# Always returns a value (0 when no matches)
sum(count_over_time({app="api"} | json | level="error" [5m])) or vector(0)

# Use in alerting rule
sum(rate({app="api"} | json | level="error" [5m])) or vector(0) > 10
```

**Why this matters:**
- Prevents flapping alerts due to "no data" states
- Provides consistent behavior for sparse logs
- Essential for reliable alerting on low-volume services

## Anti-Patterns to Avoid

### 30. Don't Use High-Cardinality Labels

**Never do this:**
```logql
{app="api", user_id="12345"}  # user_id is high cardinality!
```

**Do this instead:**
```logql
{app="api"} | json | user_id="12345"
```

### 31. Don't Parse Multiple Times

**Inefficient:**
```logql
{app="api"} | json | json | json  # Multiple parsers
```

**Efficient:**
```logql
{app="api"} | json  # Once is enough
```

### 32. Don't Use Regex for Simple String Matching

**Inefficient:**
```logql
{app="api"} |~ "GET"  # Regex for simple string
```

**Efficient:**
```logql
{app="api"} |= "GET"  # Fast string contains
```

### 33. Don't Aggregate Without Labels

**Inefficient (no grouping):**
```logql
sum(rate({app="api"}[5m]))  # Single time series
```

**Better (grouped by useful dimensions):**
```logql
sum by (namespace, app, environment) (rate({app="api"}[5m]))
```

### 34. Don't Use Very Long Time Ranges in range vectors

**Inefficient:**
```logql
rate({app="api"}[24h])  # 24 hours of data per calculation
```

**Efficient:**
```logql
rate({app="api"}[5m])  # 5 minutes of data per calculation
```

**Why:** Range vectors determine how much historical data each point calculation needs.

## Important Notes About Non-Existent Features

### LogQL Does NOT Have `dedup` or `distinct` Operators

**No `| dedup` syntax:** Deduplication is handled at the UI level in Grafana's Explore panel, not in LogQL itself.

**No `| distinct` syntax:** A `distinct` operator was proposed in [PR #8662](https://github.com/grafana/loki/pull/8662) but was **reverted** before public release due to issues with query splitting, sharding, and metric query compatibility. The proposed syntax `{job="app"} | distinct label` is NOT available in current Loki versions.

**For programmatic deduplication, use metric aggregations:**
```logql
# Count unique messages
sum by (message) (count_over_time({app="api"} | json [5m])) > 0

# Count distinct values of a label
count(count by (user_id) ({app="api"} | json))
```

### LogQL `limit` is an API Parameter, NOT a Pipeline Operator

There is no `| limit 100` syntax in LogQL. The `limit` is set via:
- **API parameter:** `&limit=100`
- **Grafana UI:** "Line limit" field
- **logcli:** `--limit=100` flag

See [Best Practice #17](#17-limit-log-query-results) for details.

## Summary Checklist

When writing LogQL queries, ensure:

- [ ] Stream selectors are as specific as possible
- [ ] Line filters come before parsers
- [ ] Exact string matching is used instead of regex when possible
- [ ] Time ranges are appropriate for the use case
- [ ] High-cardinality data is not used as labels
- [ ] The right parser is chosen for the log format
- [ ] Only necessary fields are extracted
- [ ] Aggregations are used for metric queries
- [ ] Results are limited for log queries
- [ ] Queries are tested incrementally
- [ ] Complex queries are documented with comments
- [ ] `sort` or `sort_desc` used for ordered results
- [ ] `label_replace` used for regex-based label manipulation in metrics
- [ ] `vector(0)` used as fallback in alerting rules

## Additional Resources

- [Grafana Loki Best Practices](https://grafana.com/docs/loki/latest/best-practices/)
- [LogQL Documentation](https://grafana.com/docs/loki/latest/query/)
- [Loki Operations Guide](https://grafana.com/docs/loki/latest/operations/)

## Related Skills

- **loki-config-generator**: For configuring Loki server
- **promql-generator**: For PromQL queries (similar concepts)
- **fluentbit-generator**: For log collection pipelines
