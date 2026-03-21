---
title: "Promql Generator"
description: "Generate/create/write PromQL queries, metric expressions, alerting rules, recording rules, Prometheus dashboards."
category: "devops"
source: "community"
author: "Community"
tags: ["promql", "generator"]
date: 2026-03-20
---

# PromQL Query Generator

## Overview

This skill provides a comprehensive, interactive workflow for generating production-ready PromQL queries with best practices built-in. Generate queries for monitoring dashboards, alerting rules, and ad-hoc analysis with an emphasis on user collaboration and planning before code generation.

## When to Use This Skill

Invoke this skill when:
- Creating new PromQL queries from scratch
- Building monitoring dashboards (Grafana, Prometheus UI, etc.)
- Implementing alerting rules for Prometheus Alertmanager
- Analyzing metrics for troubleshooting or capacity planning
- Converting monitoring requirements into PromQL expressions
- Learning PromQL or teaching others
- The user asks to "create", "generate", "build", or "write" PromQL queries
- Working with Prometheus metrics (counters, gauges, histograms, summaries)
- Implementing RED (Rate, Errors, Duration) or USE (Utilization, Saturation, Errors) metrics

## Interactive Query Planning Workflow

**CRITICAL**: This skill emphasizes **interactive planning** before query generation. Always engage the user in a collaborative planning process to ensure the generated query matches their exact intentions.

Follow this workflow when generating PromQL queries:

### Stage 1: Understand the Monitoring Goal

Start by understanding what the user wants to monitor or measure. Ask clarifying questions to gather requirements:

1. **Primary Goal**: What are you trying to monitor or measure?
   - Request rate (requests per second)
   - Error rate (percentage of failed requests)
   - Latency/duration (response times, percentiles)
   - Resource usage (CPU, memory, disk, network)
   - Availability/uptime
   - Queue depth, saturation, throughput
   - Custom business metrics

2. **Use Case**: What will this query be used for?
   - Dashboard visualization (Grafana, Prometheus UI)
   - Alerting rule (firing when threshold exceeded)
   - Ad-hoc troubleshooting/analysis
   - Recording rule (pre-computed aggregation)
   - Capacity planning or SLO tracking

3. **Context**: Any additional context?
   - Service/application name
   - Team or project
   - Priority level
   - Existing metrics or naming conventions

Use the **AskUserQuestion** tool to gather this information if not provided.

> **When to Ask vs. Infer**: If the user's initial request already clearly specifies the goal, use case, and context (e.g., "Create an alert for P95 latency > 500ms for payment-service"), you may acknowledge these details in your response instead of re-asking. Only ask clarifying questions for information that is missing or ambiguous.

### Stage 2: Identify Available Metrics

Determine which metrics are available and relevant:

1. **Metric Discovery**: What metrics are available?
   - Ask the user for metric names
   - If uncertain, suggest common naming patterns
   - Check for metric type indicators in the name:
     - `_total` suffix → Counter
     - `_bucket`, `_sum`, `_count` suffix → Histogram
     - No suffix → Likely Gauge
     - `_created` suffix → Counter creation timestamp

2. **Metric Type Identification**: Confirm the metric type(s)
   - **Counter**: Cumulative metric that only increases (or resets to zero)
     - Examples: `http_requests_total`, `errors_total`, `bytes_sent_total`
     - Use with: `rate()`, `irate()`, `increase()`
   - **Gauge**: Point-in-time value that can go up or down
     - Examples: `memory_usage_bytes`, `cpu_temperature_celsius`, `queue_length`
     - Use with: `avg_over_time()`, `min_over_time()`, `max_over_time()`, or directly
   - **Histogram**: Buckets of observations with cumulative counts
     - Examples: `http_request_duration_seconds_bucket`, `response_size_bytes_bucket`
     - Use with: `histogram_quantile()`, `rate()`
   - **Summary**: Pre-calculated quantiles with count and sum
     - Examples: `rpc_duration_seconds{quantile="0.95"}`
     - Use `_sum` and `_count` for averages; don't average quantiles

3. **Label Discovery**: What labels are available on these metrics?
   - Common labels: `job`, `instance`, `environment`, `service`, `endpoint`, `status_code`, `method`
   - Ask which labels are important for filtering or grouping

Use the **AskUserQuestion** tool to confirm metric names, types, and available labels.

### Stage 3: Determine Query Parameters

Gather specific requirements for the query.

#### Pre-confirmation for User-Provided Parameters

**IMPORTANT**: When the user has already specified parameters in their initial request (e.g., "5-minute window", "500ms threshold", "> 5% error rate"), you MUST:

1. **Acknowledge the provided values** explicitly in your response
2. **Present them as pre-filled defaults** in AskUserQuestion with the first option being "Use specified values"
3. **Allow quick confirmation** rather than re-asking for information already given

**Example**: If user says "alert when P95 latency exceeds 500ms", use:
```
AskUserQuestion:
- Question: "Confirm the alert threshold?"
- Options:
  1. "500ms (as specified)" - Use the threshold from your request
  2. "Different threshold" - Let me specify a different value
```

This respects the user's input and speeds up the workflow while still allowing modifications.

1. **Time Range**: What time window should the query cover?
   - Instant value (current)
   - Rate over time (`[5m]`, `[1h]`, `[1d]`)
   - For rate calculations: typically `[1m]` to `[5m]` for real-time, `[1h]` to `[1d]` for trends
   - Rule of thumb: Rate range should be at least 4x the scrape interval

2. **Label Filtering**: Which labels should filter the data?
   - Exact matches: `job="api-server"`, `status_code="200"`
   - Negative matches: `status_code!="200"`
   - Regex matches: `instance=~"prod-.*"`
   - Multiple conditions: `{job="api", environment="production"}`

3. **Aggregation**: Should the data be aggregated?
   - **No aggregation**: Return all time series as-is
   - **Aggregate by labels**: `sum by (job, endpoint)`, `avg by (instance)`
   - **Aggregate without labels**: `sum without (instance, pod)`, `avg without (job)`
   - Common aggregations: `sum`, `avg`, `max`, `min`, `count`, `topk`, `bottomk`

4. **Thresholds or Conditions**: Are there specific conditions?
   - For alerting: threshold values (e.g., error rate > 5%)
   - For filtering: only show series above/below a value
   - For comparison: compare against historical data (offset)

Use the **AskUserQuestion** tool to gather or confirm these parameters. When the user has already provided values (e.g., "5-minute window", "> 5%"), present them as the default option for confirmation.

### Stage 4: Present the Query Plan

**BEFORE GENERATING ANY CODE**, present a plain-English query plan and ask for user confirmation:

```
## PromQL Query Plan

Based on your requirements, here's what the query will do:

**Goal**: [Describe the monitoring goal in plain English]

**Query Structure**:
1. Start with metric: `[metric_name]`
2. Filter by labels: `{label1="value1", label2="value2"}`
3. Apply function: `[function_name]([metric][time_range])`
4. Aggregate: `[aggregation] by ([label_list])`
5. Additional operations: [any calculations, ratios, or transformations]

**Expected Output**:
- Data type: [instant vector/scalar]
- Labels in result: [list of labels]
- Value represents: [what the number means]
- Typical range: [expected value range]

**Example Interpretation**:
If the query returns `0.05`, it means: [plain English explanation]

**Does this match your intentions?**
- If yes, I'll generate the query and validate it
- If no, let me know what needs to change
```

Use the **AskUserQuestion** tool to confirm the plan with options:
- "Yes, generate this query"
- "Modify [specific aspect]"
- "Show me alternative approaches"

When the user chooses:
- **"Modify [specific aspect]"**: ask one focused follow-up question about what to change (metric, labels, function, time range, threshold, or output shape), then present an updated plan before generating.
- **"Show me alternative approaches"**: provide at least two valid query plans with trade-offs (accuracy, cost, cardinality, readability), then ask the user to choose one before generating.

### Stage 5: Generate the PromQL Query

Once the user confirms the plan, generate the actual PromQL query following best practices.

#### IMPORTANT: Consult Reference Files Before Generating

**Before writing any query code**, you MUST:

1. **Identify the query category** first (histogram, RED, USE, function-specific, optimization, etc.).

2. **Read only the relevant reference section(s)** using the Read tool:
   - For histogram queries → Read `references/metric_types.md` (Histogram section)
   - For error/latency patterns → Read `references/promql_patterns.md` (RED method section)
   - For resource monitoring → Read `references/promql_patterns.md` (USE method section)
   - For optimization questions → Read `references/best_practices.md`
   - For specific functions → Read `references/promql_functions.md`
   - Re-read a section only if requirements changed or you have not consulted it yet in the current thread.

3. **If a needed reference cannot be read**, state the issue and continue with best-effort generation using the most applicable documented pattern you already have.

4. **Cite the applicable pattern or best practice** in your response:
   ```
   As documented in references/promql_patterns.md (Pattern 3: Latency Percentile):
   # 95th percentile latency
   histogram_quantile(0.95, sum by (le) (rate(...)))
   ```

5. **Reference example files** when generating similar queries:
   ```
   Based on examples/red_method.promql (lines 64-82):
   # P95 latency with proper histogram_quantile usage
   ```

This keeps generated queries aligned with documented patterns while avoiding unnecessary full-file rereads on iterative follow-ups.

#### Best Practices for Query Generation

1. **Always Use Label Filters**
   ```promql
   # Good: Specific filtering reduces cardinality
   rate(http_requests_total{job="api-server", environment="prod"}[5m])

   # Bad: Matches all time series, high cardinality
   rate(http_requests_total[5m])
   ```

2. **Use Appropriate Functions for Metric Types**
   ```promql
   # Counter: Use rate() or increase()
   rate(http_requests_total[5m])

   # Gauge: Use directly or with *_over_time()
   memory_usage_bytes
   avg_over_time(memory_usage_bytes[5m])

   # Histogram: Use histogram_quantile()
   histogram_quantile(0.95,
     sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
   )
   ```

3. **Apply Aggregations with by() or without()**
   ```promql
   # Aggregate by specific labels (keeps only these labels)
   sum by (job, endpoint) (rate(http_requests_total[5m]))

   # Aggregate without specific labels (removes these labels)
   sum without (instance, pod) (rate(http_requests_total[5m]))
   ```

4. **Use Exact Matches Over Regex When Possible**
   ```promql
   # Good: Faster exact match
   http_requests_total{status_code="200"}

   # Bad: Slower regex match when not needed
   http_requests_total{status_code=~"200"}
   ```

5. **Calculate Ratios Properly**
   ```promql
   # Error rate: errors / total requests
   sum(rate(http_requests_total{status_code=~"5.."}[5m]))
   /
   sum(rate(http_requests_total[5m]))
   ```

6. **Use Recording Rules for Complex Queries**
   - If a query is used frequently or is computationally expensive
   - Pre-aggregate data to reduce query load
   - Follow naming convention: `level:metric:operations`

7. **Format for Readability**
   ```promql
   # Good: Multi-line for complex queries
   histogram_quantile(0.95,
     sum by (le, job) (
       rate(http_request_duration_seconds_bucket{job="api-server"}[5m])
     )
   )
   ```

#### Common Query Patterns

**Pattern 1: Request Rate**
```promql
# Requests per second
rate(http_requests_total{job="api-server"}[5m])

# Total requests per second across all instances
sum(rate(http_requests_total{job="api-server"}[5m]))
```

**Pattern 2: Error Rate**
```promql
# Error ratio (0 to 1)
sum(rate(http_requests_total{job="api-server", status_code=~"5.."}[5m]))
/
sum(rate(http_requests_total{job="api-server"}[5m]))

# Error percentage (0 to 100)
(
  sum(rate(http_requests_total{job="api-server", status_code=~"5.."}[5m]))
  /
  sum(rate(http_requests_total{job="api-server"}[5m]))
) * 100
```

**Pattern 3: Latency Percentile (Histogram)**
```promql
# 95th percentile latency
histogram_quantile(0.95,
  sum by (le) (
    rate(http_request_duration_seconds_bucket{job="api-server"}[5m])
  )
)
```

**Pattern 4: Resource Usage**
```promql
# Current memory usage
process_resident_memory_bytes{job="api-server"}

# Average CPU usage over 5 minutes
avg_over_time(process_cpu_seconds_total{job="api-server"}[5m])
```

**Pattern 5: Availability**
```promql
# Percentage of up instances
(
  count(up{job="api-server"} == 1)
  /
  count(up{job="api-server"})
) * 100
```

**Pattern 6: Saturation/Queue Depth**
```promql
# Average queue length
avg_over_time(queue_depth{job="worker"}[5m])

# Maximum queue depth in the last hour
max_over_time(queue_depth{job="worker"}[1h])
```

### Stage 6: Validate the Generated Query

**ALWAYS attempt to validate the generated query first** using the devops-skills:promql-validator skill:

```
After generating the query, automatically invoke:
Skill(devops-skills:promql-validator)

The devops-skills:promql-validator skill will:
1. Check syntax correctness
2. Validate semantic logic (correct functions for metric types)
3. Identify anti-patterns and inefficiencies
4. Suggest optimizations
5. Explain what the query does
6. Verify it matches user intent
```

**Validation checklist**:
- Syntax is correct (balanced brackets, valid operators)
- Metric type matches function usage
- Label filters are specific enough
- Aggregation is appropriate
- Time ranges are reasonable
- No known anti-patterns
- Query is optimized for performance

If validation fails, fix issues and re-validate until all checks pass.

If the validator skill is unavailable, fails to run, or cannot complete after two fix/re-validate cycles:
- Report the validator failure briefly (tool unavailable, timeout, parsing error, etc.).
- Run a manual fallback check (syntax shape, metric/function compatibility, label filtering, aggregation, time range sanity).
- Mark any unchecked areas as **UNVERIFIED** and ask the user whether to proceed with best-effort output or provide more context for another validation attempt.

**IMPORTANT: Display Validation Results to User**

After running validation, you MUST display the structured results to the user in this format:

```
## PromQL Validation Results

### Syntax Check
- Status: ✅ VALID / ⚠️ WARNING / ❌ ERROR / ⚠️ UNVERIFIED
- Issues: [list any syntax errors]

### Best Practices Check
- Status: ✅ OPTIMIZED / ⚠️ CAN BE IMPROVED / ❌ HAS ISSUES / ⚠️ UNVERIFIED
- Issues: [list any problems found]
- Suggestions: [list optimization opportunities]

### Validation Coverage
- Validator tool run: [successful / failed / unavailable]
- Checks completed: [syntax, semantics, anti-patterns, performance, intent-match]
- Checks skipped: [list any skipped checks, or "None"]

### Query Explanation
- **What it measures**: [plain English description]
- **Output labels**: [list labels in result, or "None (scalar)"]
- **Expected result structure**: [instant vector / scalar / etc.]
```

This transparency helps users understand the validation process and any recommendations.

### Stage 7: Provide Usage Instructions

After generation and validation (or manual fallback validation), provide the user with:

1. **The Final Query**:
   ```promql
   [Generated and validated PromQL query]
   ```

2. **Query Explanation**:
   - What the query measures
   - How to interpret the results
   - Expected value range
   - Labels in the output

3. **How to Use It**:
   - **For Dashboards**: Copy into Grafana/Prometheus UI panel query
   - **For Alerts**: Integrate into Alertmanager rule with threshold
   - **For Recording Rules**: Add to Prometheus recording rule config
   - **For Ad-hoc**: Run directly in Prometheus expression browser

4. **Customization Notes**:
   - Time ranges that might need adjustment
   - Labels to modify for different environments
   - Threshold values to tune
   - Alternative functions if requirements change

5. **Related Queries**:
   - Suggest complementary queries
   - Mention recording rule opportunities
   - Recommend dashboard panels

## Native Histograms (Prometheus 3.x+)

Native histograms are now **stable** in Prometheus 3.0+ (released November 2024). They offer significant advantages over classic histograms:
- Sparse bucket representation with near-zero cost for empty buckets
- No configuration of bucket boundaries during instrumentation
- Coverage of the full float64 range
- Efficient mergeability across histograms
- Simpler query syntax

> **Important**: Starting with Prometheus v3.8.0, native histograms are fully stable. However, scraping native histograms still requires explicit activation via the `scrape_native_histograms` configuration setting. Starting with v3.9, no feature flag is needed but `scrape_native_histograms` must be set explicitly.

### Native vs Classic Histogram Syntax

```promql
# Classic histogram (requires _bucket suffix and le label)
histogram_quantile(0.95,
  sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
)

# Native histogram (simpler - no _bucket suffix, no le label needed)
histogram_quantile(0.95,
  sum by (job) (rate(http_request_duration_seconds[5m]))
)
```

### Native Histogram Functions

```promql
# Get observation count rate from native histogram
histogram_count(rate(http_request_duration_seconds[5m]))

# Get sum of observations from native histogram
histogram_sum(rate(http_request_duration_seconds[5m]))

# Calculate fraction of observations between two values
histogram_fraction(0, 0.1, rate(http_request_duration_seconds[5m]))

# Average request duration from native histogram
histogram_sum(rate(http_request_duration_seconds[5m]))
/
histogram_count(rate(http_request_duration_seconds[5m]))
```

### Detecting Native vs Classic Histograms

Native histograms are identified by:
- **No `_bucket` suffix** on the metric name
- **No `le` label** in the time series
- The metric stores histogram data directly (not separate bucket counters)

When querying, check if your Prometheus instance has native histograms enabled:
```yaml
# prometheus.yml - Enable native histogram scraping
scrape_configs:
  - job_name: 'my-app'
    scrape_native_histogram: true  # Prometheus 3.x+
```

### Custom Bucket Native Histograms (NHCB)

Prometheus 3.4+ supports custom bucket native histograms (schema -53), allowing classic histogram to native histogram conversion. This is a key migration path for users with existing classic histograms.

**Benefits of NHCB**:
- Keep existing instrumentation (no code changes needed)
- Store classic histograms as native histograms for lower costs
- Query with native histogram syntax
- Improved reliability and compression

**Configuration** (Prometheus 3.4+):
```yaml
# prometheus.yml - Convert classic histograms to NHCB on scrape
global:
  scrape_configs:
    - job_name: 'my-app'
      convert_classic_histograms_to_nhcb: true  # Prometheus 3.4+
```

**Querying NHCB**:
```promql
# Query NHCB metrics the same way as native histograms
histogram_quantile(0.95, sum by (job) (rate(http_request_duration_seconds[5m])))

# histogram_fraction also works with NHCB (Prometheus 3.4+)
histogram_fraction(0, 0.2, rate(http_request_duration_seconds[5m]))
```

**Note**: Schema -53 indicates custom bucket boundaries. These histograms with different custom bucket boundaries are generally not mergeable with each other.

---

## SLO, Error Budget, and Burn Rate Patterns

Service Level Objectives (SLOs) are critical for modern SRE practices. These patterns help implement SLO-based monitoring and alerting.

### Error Budget Calculation

```promql
# Error budget remaining (for 99.9% SLO over 30 days)
# Returns value between 0 and 1 (1 = full budget, 0 = exhausted)
1 - (
  sum(rate(http_requests_total{job="api", status_code=~"5.."}[30d]))
  /
  sum(rate(http_requests_total{job="api"}[30d]))
) / 0.001  # 0.001 = 1 - 0.999 (allowed error rate)

# Simplified: Availability over 30 days
sum(rate(http_requests_total{job="api", status_code!~"5.."}[30d]))
/
sum(rate(http_requests_total{job="api"}[30d]))
```

### Burn Rate Calculation

Burn rate measures how fast you're consuming error budget. A burn rate of 1 means you'll exhaust the budget exactly at the end of the SLO window.

```promql
# Current burn rate (1 hour window, 99.9% SLO)
# Burn rate = (current error rate) / (allowed error rate)
(
  sum(rate(http_requests_total{job="api", status_code=~"5.."}[1h]))
  /
  sum(rate(http_requests_total{job="api"}[1h]))
) / 0.001  # 0.001 = allowed error rate for 99.9% SLO

# Burn rate > 1 means consuming budget faster than allowed
# Burn rate of 14.4 consumes 2% of monthly budget in 1 hour
```

### Multi-Window, Multi-Burn-Rate Alerts (Google SRE Standard)

The recommended approach for SLO alerting uses multiple windows to balance detection speed and precision:

```promql
# Page-level alert: 2% budget in 1 hour (burn rate 14.4)
# Long window (1h) AND short window (5m) must both exceed threshold
(
  (
    sum(rate(http_requests_total{job="api", status_code=~"5.."}[1h]))
    /
    sum(rate(http_requests_total{job="api"}[1h]))
  ) > 14.4 * 0.001
)
and
(
  (
    sum(rate(http_requests_total{job="api", status_code=~"5.."}[5m]))
    /
    sum(rate(http_requests_total{job="api"}[5m]))
  ) > 14.4 * 0.001
)

# Ticket-level alert: 5% budget in 6 hours (burn rate 6)
(
  (
    sum(rate(http_requests_total{job="api", status_code=~"5.."}[6h]))
    /
    sum(rate(http_requests_total{job="api"}[6h]))
  ) > 6 * 0.001
)
and
(
  (
    sum(rate(http_requests_total{job="api", status_code=~"5.."}[30m]))
    /
    sum(rate(http_requests_total{job="api"}[30m]))
  ) > 6 * 0.001
)
```

### SLO Recording Rules

Pre-compute SLO metrics for efficient alerting:

```yaml
# Recording rules for SLO calculations
groups:
  - name: slo_recording_rules
    interval: 30s
    rules:
      # Error ratio over different windows
      - record: job:slo_errors_per_request:ratio_rate1h
        expr: |
          sum by (job) (rate(http_requests_total{status_code=~"5.."}[1h]))
          /
          sum by (job) (rate(http_requests_total[1h]))

      - record: job:slo_errors_per_request:ratio_rate5m
        expr: |
          sum by (job) (rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum by (job) (rate(http_requests_total[5m]))

      # Availability (success ratio)
      - record: job:slo_availability:ratio_rate1h
        expr: |
          1 - job:slo_errors_per_request:ratio_rate1h
```

### Latency SLO Queries

```promql
# Percentage of requests faster than SLO target (200ms)
(
  sum(rate(http_request_duration_seconds_bucket{le="0.2", job="api"}[5m]))
  /
  sum(rate(http_request_duration_seconds_count{job="api"}[5m]))
) * 100

# Requests violating latency SLO (slower than 500ms)
(
  sum(rate(http_request_duration_seconds_count{job="api"}[5m]))
  -
  sum(rate(http_request_duration_seconds_bucket{le="0.5", job="api"}[5m]))
)
/
sum(rate(http_request_duration_seconds_count{job="api"}[5m]))
```

### Burn Rate Reference Table

| Burn Rate | Budget Consumed | Time to Exhaust 30-day Budget | Alert Severity |
|-----------|-----------------|-------------------------------|----------------|
| 1         | 100% over 30d   | 30 days                       | None           |
| 2         | 100% over 15d   | 15 days                       | Low            |
| 6         | 5% in 6h        | 5 days                        | Ticket         |
| 14.4      | 2% in 1h        | ~2 days                       | Page           |
| 36        | 5% in 1h        | ~20 hours                     | Page (urgent)  |

---

## Advanced Query Techniques

### Using Subqueries

Subqueries enable complex time-based calculations:

```promql
# Maximum 5-minute rate over the past 30 minutes
max_over_time(
  rate(http_requests_total[5m])[30m:1m]
)
```

**Syntax**: `<query>[<range>:<resolution>]`
- `<range>`: Time window to evaluate over
- `<resolution>`: Step size between evaluations

### Using Offset Modifier

Compare current data with historical data:

```promql
# Compare current rate with rate from 1 week ago
rate(http_requests_total[5m])
-
rate(http_requests_total[5m] offset 1w)
```

### Using @ Modifier

Query metrics at specific timestamps:

```promql
# Rate at the end of the range query
rate(http_requests_total[5m] @ end())

# Rate at specific Unix timestamp
rate(http_requests_total[5m] @ 1609459200)
```

### Binary Operators and Vector Matching

Combine metrics with operators and control label matching:

```promql
# One-to-one matching (default)
metric_a + metric_b

# Many-to-one with group_left
rate(http_requests_total[5m])
* on (job, instance) group_left (version)
  app_version_info

# Ignoring specific labels
metric_a + ignoring(instance) metric_b
```

### Logical Operators

Filter time series based on conditions:

```promql
# Return series only where value > 100
http_requests_total > 100

# Return series present in both
metric_a and metric_b

# Return series in A but not in B
metric_a unless metric_b
```

## Documentation Lookup

If the user asks about specific Prometheus features, operators, or custom metrics:

1. **Try context7 MCP first (preferred)**:
   ```
   Use mcp__context7__resolve-library-id with "prometheus"
   Then use mcp__context7__get-library-docs with:
   - context7CompatibleLibraryID: /prometheus/docs
   - topic: [specific feature, function, or operator]
   - page: 1 (fetch additional pages if needed)
   ```

2. **Fallback to WebSearch**:
   ```
   Search query pattern:
   "Prometheus PromQL [function/operator/feature] documentation [version] examples"

   Examples:
   "Prometheus PromQL rate function documentation examples"
   "Prometheus PromQL histogram_quantile documentation best practices"
   "Prometheus PromQL aggregation operators documentation"
   ```

## Common Monitoring Scenarios

### RED Method (for Request-Driven Services)

1. **Rate**: Request throughput
   ```promql
   sum(rate(http_requests_total{job="api"}[5m])) by (endpoint)
   ```

2. **Errors**: Error rate
   ```promql
   sum(rate(http_requests_total{job="api", status_code=~"5.."}[5m]))
   /
   sum(rate(http_requests_total{job="api"}[5m]))
   ```

3. **Duration**: Latency percentiles
   ```promql
   histogram_quantile(0.95,
     sum by (le) (rate(http_request_duration_seconds_bucket{job="api"}[5m]))
   )
   ```

### USE Method (for Resources)

1. **Utilization**: Resource usage percentage
   ```promql
   (
     avg(rate(node_cpu_seconds_total{mode!="idle"}[5m]))
     /
     count(node_cpu_seconds_total{mode="idle"})
   ) * 100
   ```

2. **Saturation**: Queue depth or resource contention
   ```promql
   avg_over_time(node_load1[5m])
   ```

3. **Errors**: Error counters
   ```promql
   rate(node_network_receive_errs_total[5m])
   ```

## Alerting Rules

When generating queries for alerting:

1. **Include the Threshold**: Make the condition explicit
   ```promql
   # Alert when error rate exceeds 5%
   (
     sum(rate(http_requests_total{status_code=~"5.."}[5m]))
     /
     sum(rate(http_requests_total[5m]))
   ) > 0.05
   ```

2. **Use Boolean Operators**: Return 1 (fire) or 0 (no alert)
   ```promql
   # Returns 1 when memory usage > 90%
   (process_resident_memory_bytes / node_memory_MemTotal_bytes) > 0.9
   ```

3. **Consider for Duration**: Alerts typically use `for` clause
   ```yaml
   alert: HighErrorRate
   expr: |
     (
       sum(rate(http_requests_total{status_code=~"5.."}[5m]))
       /
       sum(rate(http_requests_total[5m]))
     ) > 0.05
   for: 10m  # Only fire after 10 minutes of continuous violation
   ```

## Recording Rules

When generating queries for recording rules:

1. **Follow Naming Convention**: `level:metric:operations`
   ```yaml
   # level: aggregation level (job, instance, etc.)
   # metric: base metric name
   # operations: functions applied

   - record: job:http_requests:rate5m
     expr: sum by (job) (rate(http_requests_total[5m]))
   ```

2. **Pre-aggregate Expensive Queries**:
   ```yaml
   # Recording rule for frequently-used latency query
   - record: job_endpoint:http_request_duration_seconds:p95
     expr: |
       histogram_quantile(0.95,
         sum by (job, endpoint, le) (
           rate(http_request_duration_seconds_bucket[5m])
         )
       )
   ```

3. **Use Recorded Metrics in Dashboards**:
   ```promql
   # Instead of expensive query, use pre-recorded metric
   job_endpoint:http_request_duration_seconds:p95{job="api-server"}
   ```

## Error Handling

### Common Issues and Solutions

1. **Empty Results**:
   - Check if metrics exist: `up{job="your-job"}`
   - Verify label filters are correct
   - Check time range is appropriate
   - Confirm metric is being scraped

2. **Too Many Series (High Cardinality)**:
   - Add more specific label filters
   - Use aggregation to reduce series count
   - Consider using recording rules
   - Check for label explosion (dynamic labels)

3. **Incorrect Values**:
   - Verify metric type (counter vs gauge)
   - Check function usage (rate on counters, not gauges)
   - Verify time range is appropriate
   - Check for counter resets

4. **Performance Issues**:
   - Reduce time range for range vectors
   - Add label filters to reduce cardinality
   - Use recording rules for complex queries
   - Avoid expensive regex patterns
   - Consider query timeout settings

## Communication Guidelines

When generating queries:

1. **Explain the Plan**: Always present a plain-English plan before generating
2. **Ask Questions**: Use AskUserQuestion tool to gather requirements
3. **Confirm Intent**: Verify the query matches user goals before finalizing
4. **Educate**: Explain why certain functions or patterns are used
5. **Provide Context**: Show how to interpret results
6. **Suggest Improvements**: Offer optimizations or alternative approaches
7. **Validate Proactively**: Always validate and fix issues
8. **Follow Up**: Ask if adjustments are needed

## Fallback When AskUserQuestion Is Unavailable

If a structured question tool is unavailable, continue with an explicit inline questionnaire in plain text:
1. Ask for goal, metric names/types, labels, time range, aggregation, and use case in one compact prompt.
2. If the user provides partial answers, proceed with conservative defaults and clearly mark assumptions.
3. If core inputs are still ambiguous, offer 2-3 concrete query-plan options and ask the user to pick one.
4. Do not block generation indefinitely waiting for perfect context; generate a best-effort query with assumption notes.

## Relevant Reference Criteria and Trivial-Case Skip Rules

Use references deterministically, but avoid unnecessary reads for trivial requests.

Read references when ANY of the following is true:
- Histogram or summary quantiles are requested
- Query uses joins/vector matching, subqueries, offsets, or recording/alerting rules
- Query is for SLO/burn-rate/error-budget workflows
- Query includes optimization or cardinality concerns
- Metric type is unknown or contested

Skip reference reads only when ALL of the following are true:
- Single-metric, single-function query (`rate`, `increase`, `sum`, `avg`, `max`, `min`)
- No joins, no recording/alert rules, no advanced functions
- Metric type and labels are clearly provided by the user

When skipping, explicitly state: `Reference read skipped (trivial case)` and keep validation mandatory.

## Integration with devops-skills:promql-validator

After generating any PromQL query, **automatically invoke the devops-skills:promql-validator skill** to ensure quality:

```
Steps:
1. Generate the PromQL query based on user requirements
2. Invoke devops-skills:promql-validator skill with the generated query
3. Review validation results (syntax, semantics, performance)
4. Fix any issues identified by the validator
5. Re-validate until all checks pass
6. Provide the final validated query with usage instructions
7. Ask user if further refinements are needed
```

This ensures all generated queries follow best practices and are production-ready.

## Resources

> **IMPORTANT: Explicit Reference Consultation**
>
> When generating queries, you SHOULD explicitly read the relevant reference files using the Read tool and cite applicable best practices. This ensures generated queries follow documented patterns and helps users understand why certain approaches are recommended.

### references/

**promql_functions.md**
- Comprehensive reference of all PromQL functions
- Grouped by category (aggregation, math, time, histogram, etc.)
- Usage examples for each function
- **Read this file when**: implementing specific function requirements or when user asks about function behavior

**promql_patterns.md**
- Common query patterns for typical monitoring scenarios
- RED method patterns (Rate, Errors, Duration)
- USE method patterns (Utilization, Saturation, Errors)
- Alerting and recording rule patterns
- **Read this file when**: implementing standard monitoring patterns like error rates, latency, or resource usage

**best_practices.md**
- PromQL best practices and anti-patterns
- Performance optimization guidelines
- Cardinality management
- Query structure recommendations
- **Read this file when**: optimizing queries, reviewing for anti-patterns, or when cardinality concerns arise

**metric_types.md**
- Detailed guide to Prometheus metric types
- Counter, Gauge, Histogram, Summary
- When to use each type
- Appropriate functions for each type
- **Read this file when**: clarifying metric type questions or determining appropriate functions for a metric

### examples/

**common_queries.promql**
- Collection of commonly-used PromQL queries
- Request rate, error rate, latency queries
- Resource usage queries
- Availability and uptime queries
- Can be copied and customized

**red_method.promql**
- Complete RED method implementation
- Request rate queries
- Error rate queries
- Duration/latency queries

**use_method.promql**
- Complete USE method implementation
- Utilization queries
- Saturation queries
- Error queries

**alerting_rules.yaml**
- Example Prometheus alerting rules
- Various threshold-based alerts
- Best practices for alert expressions

**recording_rules.yaml**
- Example Prometheus recording rules
- Pre-aggregated metrics
- Naming conventions

**slo_patterns.promql**
- SLO, error budget, and burn rate queries
- Multi-window, multi-burn-rate alerting patterns
- Latency SLO compliance queries

**kubernetes_patterns.promql**
- Kubernetes monitoring patterns
- kube-state-metrics queries (pods, deployments, nodes)
- cAdvisor container metrics (CPU, memory)
- Vector matching and joins for Kubernetes

## Important Notes

1. **Always Plan Interactively**: Never generate a query without confirming the plan with the user
2. **Use AskUserQuestion**: Leverage the tool to gather requirements and confirm plans
3. **Validate Everything**: Always invoke devops-skills:promql-validator after generation
4. **Educate Users**: Explain what the query does and why it's structured that way
5. **Consider Use Case**: Tailor the query based on whether it's for dashboards, alerts, or analysis
6. **Think About Performance**: Always include label filters and consider cardinality
7. **Follow Metric Types**: Use appropriate functions for counters, gauges, and histograms
8. **Format for Readability**: Use multi-line formatting for complex queries

## Success Criteria

A successful query generation session should meet these measurable checkpoints:
1. Requirement capture completed: goal/use-case/metric/time-range/aggregation recorded.
2. Plan confirmation completed: user approved plan OR explicit assumption set documented.
3. Reference decision recorded: `consulted` with file names OR `skipped (trivial case)` with reason.
4. Query validity completed: syntax passes validator or manual fallback check.
5. Semantic sanity completed: function choice matches metric type (counter/gauge/histogram/summary).
6. Cardinality guard completed: query includes explicit filters or aggregation rationale.
7. Delivery completed: final query + interpretation + next-step customization guidance provided.

## Remember

The goal is to **collaboratively plan** and generate PromQL queries that exactly match user intentions. Always prioritize clarity, correctness, and performance. The interactive planning phase is the most important part of this skill—never skip it!

---

## Reference: Best_Practices

# PromQL Best Practices

Comprehensive guide to writing efficient, maintainable, and correct PromQL queries.

## Table of Contents

1. [Label Selection and Filtering](#label-selection-and-filtering)
2. [Metric Type Usage](#metric-type-usage)
3. [Aggregation Best Practices](#aggregation-best-practices)
4. [Performance Optimization](#performance-optimization)
5. [Time Range Selection](#time-range-selection)
6. [Recording Rules](#recording-rules)
7. [Alerting Best Practices](#alerting-best-practices)
8. [Query Readability](#query-readability)
9. [Common Anti-Patterns](#common-anti-patterns)
10. [Testing and Validation](#testing-and-validation)

---

## Label Selection and Filtering

### Always Use Label Filters

**Problem**: Querying metrics without label filters can match thousands or millions of time series, causing performance issues and timeouts.

```promql
# ❌ Bad: No filtering, matches all time series
rate(http_requests_total[5m])

# ✅ Good: Specific filtering
rate(http_requests_total{job="api-server", environment="production"}[5m])
```

**Best practices**:
- Always include at least `job` label filter
- Add `environment` or `cluster` for multi-environment setups
- Use `instance` for single-instance queries
- Add functional labels like `endpoint`, `method`, `status_code` as needed

### Use Exact Matches Over Regex

**Problem**: Regex matching (`=~`) is significantly slower than exact matching (`=`).

```promql
# ❌ Bad: Unnecessary regex for exact match
http_requests_total{status_code=~"200"}

# ✅ Good: Exact match is faster
http_requests_total{status_code="200"}

# ✅ Good: Regex when truly needed
http_requests_total{status_code=~"2.."}  # All 2xx codes
http_requests_total{instance=~"prod-.*"}  # Pattern matching
```

**When regex is appropriate**:
- Matching patterns: `instance=~"prod-.*"`
- Multiple values: `status_code=~"200|201|202"`
- Character classes: `status_code=~"5.."`

**Optimization tips**:
- Anchor regex patterns when possible: `=~"^prod-.*"`
- Keep patterns simple and specific
- Use multiple exact matchers instead of single regex when possible

### Avoid High-Cardinality Labels

**Problem**: Labels with many unique values create massive number of time series.

```promql
# ❌ Bad: user_id creates one series per user (high cardinality)
sum by (user_id) (rate(requests_total[5m]))

# ✅ Good: Aggregate without high-cardinality labels
sum(rate(requests_total[5m]))

# ✅ Good: Use low-cardinality labels
sum by (service, environment) (rate(requests_total[5m]))
```

**High-cardinality labels to avoid in aggregations**:
- User IDs, session IDs, request IDs
- IP addresses (unless specifically needed)
- Timestamps
- Full URLs or paths (use path patterns instead)
- UUIDs

**Solutions**:
- Aggregate out high-cardinality labels with `without()`
- Use lower-cardinality alternatives (e.g., `path_pattern` instead of `full_url`)
- Implement recording rules to pre-aggregate

---

## Metric Type Usage

### Use rate() with Counters

**Problem**: Counter metrics always increase; raw values are not useful for analysis.

```promql
# ❌ Bad: Raw counter value is not meaningful
http_requests_total

# ✅ Good: Calculate rate (requests per second)
rate(http_requests_total[5m])

# ✅ Good: Calculate total increase over period
increase(http_requests_total[1h])
```

**Counter identification**:
- Metrics ending in `_total` (e.g., `requests_total`, `errors_total`)
- Metrics ending in `_count` (e.g., `http_requests_count`)
- Metrics ending in `_sum` (e.g., `request_duration_seconds_sum`)
- Metrics ending in `_bucket` (e.g., `request_duration_seconds_bucket`)

### Don't Use rate() with Gauges

**Problem**: Gauge metrics represent current state, not cumulative values.

```promql
# ❌ Bad: rate() on gauge doesn't make sense
rate(memory_usage_bytes[5m])

# ✅ Good: Use gauge value directly
memory_usage_bytes

# ✅ Good: Use *_over_time functions for analysis
avg_over_time(memory_usage_bytes[5m])
max_over_time(memory_usage_bytes[1h])
```

**Gauge examples**:
- `memory_usage_bytes`
- `cpu_temperature_celsius`
- `queue_length`
- `active_connections`

### Histogram Quantiles Require Aggregation

**Problem**: `histogram_quantile()` requires proper aggregation and the `le` label.

```promql
# ❌ Bad: Missing aggregation
histogram_quantile(0.95, rate(request_duration_seconds_bucket[5m]))

# ❌ Bad: Missing le label in aggregation
histogram_quantile(0.95, sum(rate(request_duration_seconds_bucket[5m])))

# ❌ Bad: Missing rate() on buckets
histogram_quantile(0.95, sum by (le) (request_duration_seconds_bucket))

# ✅ Good: Correct usage
histogram_quantile(0.95,
  sum by (le) (rate(request_duration_seconds_bucket[5m]))
)

# ✅ Good: Preserving additional labels
histogram_quantile(0.95,
  sum by (service, le) (rate(request_duration_seconds_bucket[5m]))
)
```

**Requirements for histogram_quantile()**:
1. Must apply `rate()` or `irate()` to bucket counters
2. Must aggregate with `sum`
3. Must include `le` label in aggregation
4. Can include other labels for grouping

### Never Average Pre-Calculated Quantiles

**Problem**: Averaging quantiles is mathematically invalid and produces incorrect results.

```promql
# ❌ Bad: Averaging quantiles is wrong
avg(request_duration_seconds{quantile="0.95"})

# ✅ Good: Use _sum and _count to calculate average
sum(rate(request_duration_seconds_sum[5m]))
/
sum(rate(request_duration_seconds_count[5m]))

# ✅ Good: If you need quantiles, use histogram
histogram_quantile(0.95,
  sum by (le) (rate(request_duration_seconds_bucket[5m]))
)
```

---

## Aggregation Best Practices

### Choose Between by() and without()

**by()**: Keeps only specified labels, removes all others
**without()**: Removes specified labels, keeps all others

```promql
# Use by() when you know exactly what labels you want to keep
sum by (service, environment) (rate(requests_total[5m]))

# Use without() when you want to remove specific labels
sum without (instance, pod) (rate(requests_total[5m]))
```

**When to use each**:
- **by()**: When aggregating to specific dimensions (service-level metrics)
- **without()**: When removing noise (instance-level details)

### Aggregate Before histogram_quantile()

**Always aggregate before calling histogram_quantile()**:

```promql
# ❌ Bad: Trying to aggregate after quantile calculation
sum(
  histogram_quantile(0.95, rate(request_duration_seconds_bucket[5m]))
)

# ✅ Good: Aggregate first, then calculate quantile
histogram_quantile(0.95,
  sum by (le) (rate(request_duration_seconds_bucket[5m]))
)

# ✅ Good: Aggregate with grouping
histogram_quantile(0.95,
  sum by (service, le) (rate(request_duration_seconds_bucket[5m]))
)
```

### Use Appropriate Aggregation Operators

Choose the right aggregation for your use case:

```promql
# sum: For counting, totaling
sum(up{job="api"})  # Total number of instances

# avg: For average values
avg(cpu_usage_percent)  # Average CPU across instances

# max/min: For identifying extremes
max(memory_usage_bytes)  # Instance with highest memory use

# count: For counting series
count(up{job="api"} == 1)  # Number of healthy instances

# topk/bottomk: For top/bottom N
topk(10, rate(requests_total[5m]))  # Top 10 by request rate

# quantile: For percentiles across simple metrics
quantile(0.95, response_time_seconds)  # 95th percentile
```

---

## Performance Optimization

### Limit Cardinality

**The number of time series matters most for query performance.**

```promql
# Check cardinality of a metric
count(metric_name)

# Check cardinality by label
count by (label_name) (metric_name)

# Identify high-cardinality metrics
topk(10, count by (__name__) ({__name__=~".+"}))
```

**Strategies to reduce cardinality**:
1. Add more specific label filters
2. Use aggregation to reduce dimensions
3. Remove high-cardinality labels from queries
4. Use recording rules for frequently-queried aggregations

### Optimize Time Ranges

**Larger time ranges process more data and run slower.**

```promql
# ❌ Slow: Very large range for rate
rate(requests_total[1h])

# ✅ Fast: Appropriate range for rate
rate(requests_total[5m])

# For recording rules: Pre-compute common ranges
# Then use the recorded metric instead
job:requests:rate5m  # Recorded metric
```

**Time range guidelines**:
- **Rate functions**: `[1m]` to `[5m]` for real-time monitoring
- **Trend analysis**: `[1h]` to `[1d]` when needed
- **Rule of thumb**: Range should be 4× scrape interval minimum
- **Recording rules**: Use for ranges longer than `[5m]` if queried frequently

### Avoid Expensive Subqueries

**Subqueries can exponentially increase query cost.**

```promql
# ❌ Expensive: Subquery over long range
max_over_time(rate(metric[5m])[7d:1h])

# ✅ Better: Use recording rule
max_over_time(job:metric:rate5m[7d])

# ✅ Better: Reduce range if possible
max_over_time(rate(metric[5m])[1d:1h])
```

**Subquery cost = range_duration / resolution × base_query_cost**

### Use Recording Rules for Complex Queries

**Recording rules pre-compute expensive queries.**

```yaml
# Recording rule configuration
groups:
  - name: request_rates
    interval: 30s
    rules:
      # Pre-compute expensive aggregation
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))

      # Pre-compute complex quantile
      - record: job:http_latency:p95
        expr: |
          histogram_quantile(0.95,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )
```

**Use recording rules when**:
- Query is used in multiple dashboards
- Query is computationally expensive
- Query is accessed frequently (every dashboard refresh)
- You need faster dashboard/alert evaluation

---

## Time Range Selection

### Choose Appropriate Ranges for rate()

**Too short**: Noisy, sensitive to scraping jitter
**Too long**: Hides important spikes, slow to react

```promql
# Real-time monitoring: 1-5 minutes
rate(requests_total[2m])
rate(requests_total[5m])

# Trend analysis: 15 minutes to 1 hour
rate(requests_total[15m])
rate(requests_total[1h])

# Historical analysis: Hours to days
rate(requests_total[6h])
rate(requests_total[1d])
```

**Guidelines**:
- Minimum range: 4× scrape interval
- For 15s scrape interval: minimum `[1m]`
- For 30s scrape interval: minimum `[2m]`
- Default choice: `[5m]` works well for most cases

### Use irate() for Volatile Metrics

```promql
# rate(): Average over time range, smooth
rate(requests_total[5m])

# irate(): Instant based on last 2 points, volatile
irate(requests_total[5m])
```

**When to use irate()**:
- Detecting sudden spikes
- Alerting on rapid changes
- Short-term analysis
- Metrics that change dramatically

**When to use rate()**:
- Dashboard visualizations
- Trend analysis
- Smooth charts
- Most monitoring use cases

---

## Recording Rules

### Follow Naming Convention

**Format**: `level:metric:operations`

```yaml
# level: Aggregation level (job, service, cluster)
# metric: Base metric name
# operations: Functions applied (rate5m, p95, sum)

rules:
  # Good examples
  - record: job:http_requests:rate5m
    expr: sum by (job) (rate(http_requests_total[5m]))

  - record: job_endpoint:http_latency:p95
    expr: |
      histogram_quantile(0.95,
        sum by (job, endpoint, le) (rate(http_request_duration_seconds_bucket[5m]))
      )

  - record: cluster:cpu_usage:ratio
    expr: |
      sum(rate(node_cpu_seconds_total{mode!="idle"}[5m]))
      /
      sum(rate(node_cpu_seconds_total[5m]))
```

### Pre-Aggregate Expensive Queries

```yaml
# Instead of running this expensive query repeatedly:
# histogram_quantile(0.95, sum by (le) (rate(latency_bucket[5m])))

# Create a recording rule:
- record: :http_request_duration:p95
  expr: |
    histogram_quantile(0.95,
      sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
    )

# Then use the recorded metric:
# :http_request_duration:p95
```

### Layer Recording Rules

**Build complex metrics in stages:**

```yaml
# Layer 1: Basic rates
- record: instance:requests:rate5m
  expr: rate(http_requests_total[5m])

# Layer 2: Job-level aggregation
- record: job:requests:rate5m
  expr: sum by (job) (instance:requests:rate5m)

# Layer 3: Derived metrics
- record: job:error_ratio:rate5m
  expr: |
    sum by (job) (instance:requests:rate5m{status_code=~"5.."})
    /
    job:requests:rate5m
```

---

## Alerting Best Practices

### Make Alert Expressions Boolean

**Alert expressions should return 1 (firing) or 0 (not firing).**

```promql
# ✅ Good: Boolean expression
(
  sum(rate(errors_total[5m]))
  /
  sum(rate(requests_total[5m]))
) > 0.05

# ✅ Good: Explicit comparison
http_requests_rate < 10

# ✅ Good: Complex boolean
(cpu_usage > 80) and (memory_usage > 90)
```

### Use `for` Duration for Stability

**Avoid alerting on transient spikes.**

```yaml
# Alert only after condition persists for 10 minutes
- alert: HighErrorRate
  expr: |
    (
      sum(rate(errors_total[5m]))
      /
      sum(rate(requests_total[5m]))
    ) > 0.05
  for: 10m
  annotations:
    summary: "Error rate above 5% for 10+ minutes"
```

**`for` duration guidelines**:
- Short-lived issues: `5m`
- Sustained problems: `10m` to `15m`
- Avoid false positives: `30m`+
- Critical immediate alerts: `0m` (no `for`)

### Include Context in Alert Queries

```promql
# ✅ Good: Include labels that identify the problem
sum by (service, environment) (
  rate(errors_total[5m])
) > 100

# Alerts will show which service and environment
```

### Avoid Alerting on Absence Without Context

```promql
# ❌ Bad: Too generic
absent(up)

# ✅ Good: Specific service
absent(up{job="critical-service"})

# ✅ Good: With timeout
absent_over_time(up{job="critical-service"}[10m])
```

---

## Query Readability

### Format Complex Queries

**Use multi-line formatting for readability:**

```promql
# ✅ Good: Multi-line with indentation
histogram_quantile(0.95,
  sum by (service, le) (
    rate(http_request_duration_seconds_bucket{
      environment="production",
      job="api-server"
    }[5m])
  )
)

# ❌ Bad: Single line, hard to read
histogram_quantile(0.95, sum by (service, le) (rate(http_request_duration_seconds_bucket{environment="production", job="api-server"}[5m])))
```

### Use Comments in Recording Rules

```yaml
rules:
  # Calculate p95 latency for all API endpoints
  # Used by: API dashboard, SLO calculations, latency alerts
  - record: api:http_latency:p95
    expr: |
      histogram_quantile(0.95,
        sum by (endpoint, le) (
          rate(http_request_duration_seconds_bucket{job="api"}[5m])
        )
      )
```

### Name Recording Rules Descriptively

```yaml
# ✅ Good: Clear purpose from name
- record: api:error_rate:ratio5m
- record: db:query_duration:p99
- record: cluster:memory_usage:bytes

# ❌ Bad: Unclear names
- record: metric1
- record: temp_calc
- record: x
```

---

## Common Anti-Patterns

### Anti-Pattern 1: No Label Filters

```promql
# ❌ Anti-pattern
rate(http_requests_total[5m])

# ✅ Fix
rate(http_requests_total{job="api-server", environment="prod"}[5m])
```

### Anti-Pattern 2: Regex for Exact Match

```promql
# ❌ Anti-pattern
metric{label=~"value"}

# ✅ Fix
metric{label="value"}
```

### Anti-Pattern 3: rate() on Gauges

```promql
# ❌ Anti-pattern
rate(memory_usage_bytes[5m])

# ✅ Fix
avg_over_time(memory_usage_bytes[5m])
```

### Anti-Pattern 4: Missing rate() on Counters

```promql
# ❌ Anti-pattern
http_requests_total

# ✅ Fix
rate(http_requests_total[5m])
```

### Anti-Pattern 5: Averaging Quantiles

```promql
# ❌ Anti-pattern
avg(http_duration{quantile="0.95"})

# ✅ Fix
histogram_quantile(0.95,
  sum by (le) (rate(http_duration_bucket[5m]))
)
```

### Anti-Pattern 6: Missing Aggregation in histogram_quantile

```promql
# ❌ Anti-pattern
histogram_quantile(0.95, rate(latency_bucket[5m]))

# ✅ Fix
histogram_quantile(0.95,
  sum by (le) (rate(latency_bucket[5m]))
)
```

### Anti-Pattern 7: High-Cardinality Aggregation

```promql
# ❌ Anti-pattern
sum by (user_id) (requests)  # millions of series

# ✅ Fix
sum(requests)  # single series
# Or use low-cardinality labels
sum by (service) (requests)
```

---

## Testing and Validation

### Test Queries Before Production

1. **Check cardinality**:
   ```promql
   count(your_query)
   ```

2. **Verify result makes sense**:
   - Check value range
   - Verify labels in output
   - Compare with expected results

3. **Test edge cases**:
   - What if metric doesn't exist?
   - What if all instances are down?
   - What during counter resets?

### Validate Time Ranges

```promql
# Test with different ranges
rate(metric[1m])
rate(metric[5m])
rate(metric[1h])

# Verify results are reasonable
```

### Check for Missing Data

```promql
# Verify metric exists
count(metric_name) > 0

# Check for gaps
absent_over_time(metric_name[10m])
```

---

## Summary Checklist

Before deploying a PromQL query, verify:

- [ ] Uses specific label filters (at least `job`)
- [ ] Uses exact match (`=`) instead of regex when possible
- [ ] Uses appropriate function for metric type
  - [ ] `rate()` for counters
  - [ ] Direct value or `*_over_time()` for gauges
  - [ ] `histogram_quantile()` with `sum by (le)` for histograms
- [ ] Includes proper aggregation
- [ ] Uses reasonable time range (typically `[5m]`)
- [ ] Avoids high-cardinality labels
- [ ] Formatted for readability
- [ ] Tested and returns expected results
- [ ] Considers using recording rule if expensive and frequently accessed
- [ ] Includes descriptive naming (for recording rules/alerts)
- [ ] Documented with comments (for complex queries)

---

## Resources

- [Official Prometheus Querying Documentation](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [PromQL Functions Reference](promql_functions.md)
- [Common Query Patterns](promql_patterns.md)

---

## Reference: Metric_Types

# Prometheus Metric Types

Comprehensive guide to the four Prometheus metric types: Counter, Gauge, Histogram, and Summary.

## Table of Contents

1. [Overview](#overview)
2. [Counter](#counter)
3. [Gauge](#gauge)
4. [Histogram](#histogram)
5. [Summary](#summary)
6. [Choosing the Right Type](#choosing-the-right-type)
7. [Metric Naming Conventions](#metric-naming-conventions)

---

## Overview

Prometheus has four core metric types, each designed for specific use cases:

| Type | Description | Use Case | Example |
|------|-------------|----------|---------|
| **Counter** | Cumulative value that only increases | Counting events | Requests, errors, bytes sent |
| **Gauge** | Value that can go up or down | Current state | Memory usage, temperature, queue size |
| **Histogram** | Observations bucketed by value | Latency, sizes | Request duration, response size |
| **Summary** | Observations with quantiles | Latency, sizes | Request duration percentiles |

---

## Counter

### Definition

A **counter** is a cumulative metric that only increases over time (or resets to zero on restart). Counters are used for counting events.

### Characteristics

- **Only increases** (or resets to 0)
- **Cumulative** - represents total count since start
- **Not meaningful as raw value** - always use with `rate()` or `increase()`
- **Handles restarts** - rate functions automatically detect and handle counter resets

### Examples

```promql
# Total HTTP requests since process started
http_requests_total

# Total errors since process started
http_errors_total

# Total bytes sent since process started
bytes_sent_total

# Total database queries executed
db_queries_total{operation="select"}
```

### Naming Convention

Counters should end with `_total`:
- `http_requests_total`
- `errors_total`
- `bytes_processed_total`
- `cache_hits_total`

### Common PromQL Functions

#### rate() - Per-Second Average Rate

```promql
# Requests per second over last 5 minutes
rate(http_requests_total[5m])

# Errors per second
rate(errors_total[2m])

# Bytes sent per second
rate(bytes_sent_total[1m])
```

**When to use**: Graphing trends, calculating throughput, most monitoring use cases

#### irate() - Instant Rate

```promql
# Instant requests per second
irate(http_requests_total[5m])
```

**When to use**: Detecting spikes, alerting on sudden changes, real-time dashboards

#### increase() - Total Increase

```promql
# Total requests in the last hour
increase(http_requests_total[1h])

# Total errors in the last day
increase(errors_total[24h])
```

**When to use**: Calculating totals over periods, capacity planning, billing

### Best Practices

```promql
# ✅ Good: Use rate() for per-second values
rate(http_requests_total{job="api"}[5m])

# ✅ Good: Use increase() for totals
increase(http_requests_total{job="api"}[1h])

# ❌ Bad: Don't use raw counter values
http_requests_total

# ❌ Bad: Don't use rate() without time range
rate(http_requests_total)
```

### Use Cases

- **Request counting**: `http_requests_total`, `grpc_requests_total`
- **Error tracking**: `errors_total`, `failed_requests_total`
- **Throughput**: `bytes_sent_total`, `messages_processed_total`
- **Cache hits/misses**: `cache_hits_total`, `cache_misses_total`
- **Database operations**: `db_queries_total`, `db_transactions_total`

---

## Gauge

### Definition

A **gauge** is a metric that represents a single numerical value that can go up or down. Gauges represent current state or level.

### Characteristics

- **Can increase or decrease**
- **Represents current value** - meaningful as-is
- **Snapshot** - shows state at time of measurement
- **No cumulative behavior**

### Examples

```promql
# Current memory usage in bytes
memory_usage_bytes

# Current CPU temperature
cpu_temperature_celsius

# Current number of items in queue
queue_length

# Current number of active connections
active_connections

# Current disk space available
disk_available_bytes
```

### Naming Convention

Gauges should describe the measured value and include units:
- `memory_usage_bytes`
- `temperature_celsius`
- `queue_depth`
- `active_threads`
- `cpu_usage_ratio` (for percentages expressed as 0-1)

### Common PromQL Functions

#### Direct Usage

```promql
# Current memory usage
memory_usage_bytes

# Current queue length
queue_depth{service="worker"}
```

#### *_over_time Functions

```promql
# Average memory usage over 5 minutes
avg_over_time(memory_usage_bytes[5m])

# Maximum queue depth in last hour
max_over_time(queue_depth[1h])

# Minimum available disk space in last day
min_over_time(disk_available_bytes[24h])

# Count of samples (how many times scraped)
count_over_time(metric[5m])
```

#### Statistical Analysis

```promql
# Standard deviation of response time
stddev_over_time(response_time_seconds[5m])

# Quantile of gauge values over time
quantile_over_time(0.95, metric[5m])

# Rate of change (derivative)
deriv(queue_length[10m])
```

### Best Practices

```promql
# ✅ Good: Use gauge directly for current value
memory_usage_bytes

# ✅ Good: Use *_over_time for analysis
avg_over_time(memory_usage_bytes[5m])

# ❌ Bad: Don't use rate() on gauges
rate(memory_usage_bytes[5m])

# ❌ Bad: Don't use increase() on gauges
increase(memory_usage_bytes[1h])

# ✅ Good: Use deriv() for rate of change
deriv(disk_usage_bytes[1h])
```

### Use Cases

- **Resource usage**: `memory_usage_bytes`, `cpu_usage_percent`, `disk_usage_bytes`
- **Temperatures**: `cpu_temperature_celsius`, `disk_temperature_celsius`
- **Queue metrics**: `queue_length`, `pending_jobs`
- **Connection counts**: `active_connections`, `idle_connections`
- **Thread counts**: `active_threads`, `blocked_threads`
- **Current state**: `replica_count`, `node_count`, `pod_count`

---

## Histogram

### Definition

A **histogram** samples observations (like request durations or response sizes) and counts them in configurable buckets. It also provides a sum of all observed values.

### Characteristics

- **Buckets** - predefined upper bounds (le = "less than or equal")
- **Cumulative** - each bucket includes all observations ≤ its upper bound
- **Three metrics**:
  - `_bucket` - counter for each bucket
  - `_sum` - sum of all observed values
  - `_count` - total number of observations
- **Calculate quantiles** - use `histogram_quantile()`
- **Flexible** - can calculate any quantile from the same data

### Structure

For metric `http_request_duration_seconds`, you get:

```
http_request_duration_seconds_bucket{le="0.1"}   # ≤ 0.1s
http_request_duration_seconds_bucket{le="0.5"}   # ≤ 0.5s
http_request_duration_seconds_bucket{le="1"}     # ≤ 1s
http_request_duration_seconds_bucket{le="5"}     # ≤ 5s
http_request_duration_seconds_bucket{le="+Inf"}  # All observations
http_request_duration_seconds_sum                # Sum of all durations
http_request_duration_seconds_count              # Total count
```

### Examples

```promql
# Request duration histogram
http_request_duration_seconds_bucket

# Response size histogram
http_response_size_bytes_bucket

# Database query duration histogram
db_query_duration_seconds_bucket
```

### Naming Convention

Histograms should describe what is being measured and include units:
- `http_request_duration_seconds`
- `response_size_bytes`
- `db_query_duration_seconds`
- `batch_processing_time_seconds`

The instrumentation library automatically adds `_bucket`, `_sum`, and `_count` suffixes.

### Common PromQL Functions

#### histogram_quantile() - Calculate Percentiles

```promql
# 95th percentile request duration
histogram_quantile(0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)

# Multiple percentiles
histogram_quantile(0.50, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))  # P50
histogram_quantile(0.90, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))  # P90
histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))  # P99

# Percentile by service
histogram_quantile(0.95,
  sum by (service, le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

#### Average from Histogram

```promql
# Average request duration
sum(rate(http_request_duration_seconds_sum[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))

# Average by endpoint
sum by (endpoint) (rate(http_request_duration_seconds_sum[5m]))
/
sum by (endpoint) (rate(http_request_duration_seconds_count[5m]))
```

#### Request Rate from Histogram

```promql
# Requests per second (from histogram)
sum(rate(http_request_duration_seconds_count[5m]))

# Same as using counter
sum(rate(http_requests_total[5m]))
```

#### Fraction of Observations

```promql
# Percentage of requests under 100ms
(
  sum(rate(http_request_duration_seconds_bucket{le="0.1"}[5m]))
  /
  sum(rate(http_request_duration_seconds_count[5m]))
) * 100

# SLO: 95% of requests must be under 500ms
(
  sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
  /
  sum(rate(http_request_duration_seconds_count[5m]))
) >= 0.95
```

### Best Practices

```promql
# ✅ Good: Always use rate() on buckets
histogram_quantile(0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)

# ✅ Good: Always include sum by (le)
histogram_quantile(0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)

# ✅ Good: Can include other labels for grouping
histogram_quantile(0.95,
  sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
)

# ❌ Bad: Missing aggregation
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# ❌ Bad: Missing le in aggregation
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket[5m]))
)

# ❌ Bad: Missing rate()
histogram_quantile(0.95,
  sum by (le) (http_request_duration_seconds_bucket)
)
```

### Use Cases

- **Request latency**: `http_request_duration_seconds`, `grpc_request_duration_seconds`
- **Response sizes**: `http_response_size_bytes`, `message_size_bytes`
- **Database query times**: `db_query_duration_seconds`
- **Batch processing times**: `batch_processing_duration_seconds`
- **Any measurement where you need percentiles**: response times, processing durations, sizes

### Advantages

- **Flexible**: Calculate any quantile from same data
- **Aggregatable**: Can aggregate across dimensions
- **Resource efficient**: Client-side bucketing, not all observations
- **Suitable for alerting**: Consistent with `rate()` calculations

### Bucket Configuration

Choose buckets that cover your expected range:

```go
// Example: HTTP request duration (Go client)
[]float64{.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10}
// 5ms, 10ms, 25ms, 50ms, 100ms, 250ms, 500ms, 1s, 2.5s, 5s, 10s

// Example: Response size in bytes
[]float64{100, 1000, 10000, 100000, 1000000, 10000000}
// 100B, 1KB, 10KB, 100KB, 1MB, 10MB
```

---

## Summary

### Definition

A **summary** is similar to a histogram but calculates quantiles on the client side and streams pre-calculated percentiles to Prometheus.

### Characteristics

- **Pre-calculated quantiles** - computed by client
- **Three metrics**:
  - `{quantile="0.5"}` - 50th percentile
  - `{quantile="0.9"}` - 90th percentile
  - `{quantile="0.99"}` - 99th percentile
  - `_sum` - sum of all observed values
  - `_count` - total number of observations
- **Not aggregatable** - quantiles can't be averaged or summed
- **Less flexible** - can only view pre-configured quantiles

### Structure

For metric `http_request_duration_seconds`, you get:

```
http_request_duration_seconds{quantile="0.5"}   # 50th percentile (median)
http_request_duration_seconds{quantile="0.9"}   # 90th percentile
http_request_duration_seconds{quantile="0.99"}  # 99th percentile
http_request_duration_seconds_sum               # Sum of all durations
http_request_duration_seconds_count             # Total count
```

### Examples

```promql
# Pre-calculated 95th percentile
http_request_duration_seconds{quantile="0.95"}

# Pre-calculated 50th percentile (median)
rpc_duration_seconds{quantile="0.5"}
```

### Common PromQL Functions

#### Using Pre-Calculated Quantiles

```promql
# Use quantile directly (no calculation needed)
http_request_duration_seconds{quantile="0.95"}

# By service
http_request_duration_seconds{service="api", quantile="0.95"}
```

#### Calculate Average

```promql
# Average from summary
sum(rate(http_request_duration_seconds_sum[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))
```

### Best Practices

```promql
# ✅ Good: Use quantile directly
http_request_duration_seconds{quantile="0.95"}

# ✅ Good: Calculate average from _sum and _count
sum(rate(http_request_duration_seconds_sum[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))

# ❌ Bad: Don't average quantiles across instances
avg(http_request_duration_seconds{quantile="0.95"})

# ❌ Bad: Don't sum quantiles
sum(http_request_duration_seconds{quantile="0.95"})

# ❌ Bad: Don't use histogram_quantile() on summaries
histogram_quantile(0.95, http_request_duration_seconds)
```

### Use Cases

- **When client-side quantiles are acceptable**
- **Single instance metrics** (not aggregated across multiple instances)
- **Legacy systems** (histograms are generally preferred now)
- **Specific quantile requirements** that won't change

### Limitations

1. **Cannot aggregate across instances/labels** - quantiles can't be averaged
2. **Fixed quantiles** - can't calculate new percentiles from existing data
3. **More client resources** - quantile calculation happens on client
4. **Not suitable for alerting** - quantiles calculated differently than rates

### Histogram vs Summary

| Feature | Histogram | Summary |
|---------|-----------|---------|
| **Quantile calculation** | Server-side | Client-side |
| **Aggregatable** | ✅ Yes | ❌ No |
| **Flexible quantiles** | ✅ Calculate any | ❌ Only pre-configured |
| **Client resources** | Low | Higher |
| **Server resources** | Higher | Low |
| **Alerting friendly** | ✅ Yes | ⚠️ Limited |
| **Recommended** | ✅ Preferred | ⚠️ Legacy |

**Recommendation**: Use **histograms** for new instrumentation. Summaries are mainly for legacy compatibility.

---

## Choosing the Right Type

### Decision Tree

```
Are you counting events that only increase?
├─ Yes → Counter (e.g., requests_total, errors_total)
└─ No → Is it a current state that can go up or down?
    ├─ Yes → Gauge (e.g., memory_bytes, queue_length)
    └─ No → Do you need percentiles/distributions?
        ├─ Yes → Histogram (e.g., duration_seconds, size_bytes)
        └─ No → Consider if you really need metrics for this
```

### Use Case Matrix

| What You're Measuring | Metric Type | Example |
|----------------------|-------------|---------|
| Total requests | Counter | `http_requests_total` |
| Failed requests | Counter | `http_errors_total` |
| Bytes transferred | Counter | `bytes_sent_total` |
| Current memory usage | Gauge | `memory_usage_bytes` |
| Queue depth | Gauge | `queue_length` |
| Active connections | Gauge | `active_connections` |
| Request duration | Histogram | `http_request_duration_seconds` |
| Response size | Histogram | `http_response_size_bytes` |
| Latency percentiles | Histogram | `request_latency_seconds` |
| Pre-calculated quantiles | Summary | `rpc_duration_seconds` |

---

## Metric Naming Conventions

### General Rules

1. **Use base units**: seconds (not milliseconds), bytes (not kilobytes)
2. **Include units in name**: `_seconds`, `_bytes`, `_ratio`, `_percent`
3. **Use descriptive names**: `http_request_duration_seconds` not `http_req_dur_s`
4. **Counters end in `_total`**: `requests_total`, `errors_total`
5. **Ratios use `_ratio` suffix**: `cpu_usage_ratio` (0-1 range)
6. **Avoid stuttering**: `http_requests_total` not `http_http_requests_total`

### Unit Suffixes

| Unit | Suffix | Example |
|------|--------|---------|
| Seconds | `_seconds` | `http_request_duration_seconds` |
| Bytes | `_bytes` | `memory_usage_bytes` |
| Ratio (0-1) | `_ratio` | `cpu_usage_ratio` |
| Percentage (0-100) | `_percent` | `cpu_usage_percent` |
| Total count | `_total` | `http_requests_total` |
| Celsius | `_celsius` | `cpu_temperature_celsius` |
| Joules | `_joules` | `energy_consumption_joules` |
| Volts | `_volts` | `voltage_volts` |

### Namespace Structure

`<namespace>_<subsystem>_<metric_name>_<unit>`

```
# Good examples
http_request_duration_seconds
http_response_size_bytes
db_query_duration_seconds
process_resident_memory_bytes
node_cpu_seconds_total

# Component structure
prometheus_http_requests_total     # namespace: prometheus, subsystem: http
node_network_receive_bytes_total   # namespace: node, subsystem: network
```

---

## Summary Comparison

| Metric Type | Increases | Decreases | Aggregatable | Use Rate | Use Case |
|-------------|-----------|-----------|--------------|----------|----------|
| **Counter** | ✅ | ❌ | ✅ | ✅ | Event counting |
| **Gauge** | ✅ | ✅ | ✅ | ❌ | Current state |
| **Histogram** | ✅ (_bucket) | ❌ | ✅ | ✅ | Distributions |
| **Summary** | ✅ (_sum) | ❌ | ⚠️ (limited) | ⚠️ | Pre-calc quantiles |

**Most common**: Counter and Histogram cover 90% of use cases.

---

## References

- [Prometheus Metric Types](https://prometheus.io/docs/concepts/metric_types/)
- [Prometheus Best Practices - Naming](https://prometheus.io/docs/practices/naming/)
- [Histograms and Summaries](https://prometheus.io/docs/practices/histograms/)

---

## Reference: Promql_Functions

# PromQL Functions Reference

Complete reference of Prometheus Query Language functions organized by category.

## Aggregation Operators

Aggregation operators combine multiple time series into fewer time series.

**Syntax**: `<operator> [without|by (<label_list>)] (<instant_vector>)`

### sum

Calculates sum of values across time series.

```promql
# Sum all HTTP requests
sum(http_requests_total)

# Sum by job and endpoint
sum by (job, endpoint) (http_requests_total)

# Sum without instance label
sum without (instance) (http_requests_total)
```

**Use for**: Totaling metrics across instances, calculating aggregate throughput.

### avg

Calculates average of values across time series.

```promql
# Average CPU usage across all instances
avg(cpu_usage_percent)

# Average by environment
avg by (environment) (cpu_usage_percent)
```

**Use for**: Average resource usage, typical response times.

### max / min

Returns maximum or minimum value across time series.

```promql
# Maximum memory usage across instances
max(memory_usage_bytes)

# Minimum available disk space by node
min by (node) (disk_available_bytes)
```

**Use for**: Peak resource usage, bottleneck identification.

### count

Counts the number of time series.

```promql
# Count of running instances
count(up == 1)

# Count of instances by version
count by (version) (app_version_info)
```

**Use for**: Counting instances, availability calculations.

### count_values

Counts time series with the same value.

```promql
# Count how many instances have each version
count_values("version", app_version)
```

**Use for**: Distribution analysis, version tracking.

### topk / bottomk

Returns k largest or smallest time series by value.

```promql
# Top 5 endpoints by request count
topk(5, rate(http_requests_total[5m]))

# Bottom 3 instances by available memory
bottomk(3, node_memory_available_bytes)
```

**Use for**: Identifying highest/lowest consumers, troubleshooting hotspots.

### quantile

Calculates φ-quantile (0 ≤ φ ≤ 1) across dimensions.

```promql
# 95th percentile of response times
quantile(0.95, response_time_seconds)

# 50th percentile (median) by service
quantile(0.5, response_time_seconds) by (service)
```

**Use for**: Percentile calculations across simple metrics (not histograms).

### stddev / stdvar

Calculates standard deviation or variance.

```promql
# Standard deviation of response times
stddev(response_time_seconds)
```

**Use for**: Measuring variability, detecting anomalies.

## Rate and Increase Functions

Functions for working with counter metrics (cumulative values that only increase).

### rate

Calculates per-second average rate of increase over a time range.

```promql
# Requests per second over last 5 minutes
rate(http_requests_total[5m])

# Bytes sent per second
rate(bytes_sent_total[1m])
```

**How it works**:
- Calculates increase between first and last samples in range
- Divides by time elapsed to get per-second rate
- Automatically handles counter resets
- Extrapolates to range boundaries

**Best practices**:
- Use with counter metrics only (metrics with `_total`, `_count`, `_sum`, or `_bucket` suffix)
- Range should be at least 4x the scrape interval
- Minimum range typically `[1m]` to `[5m]`
- Returns average rate, smoothing out spikes

**When to use**: For graphing trends, alerting on sustained rates, calculating throughput.

### irate

Calculates instant rate based on the last two data points.

```promql
# Instant rate of HTTP requests
irate(http_requests_total[5m])

# Real-time throughput (sensitive to spikes)
irate(bytes_processed_total[2m])
```

**How it works**:
- Uses only the last two samples in the range
- Range determines maximum lookback window
- More sensitive to short-term changes than `rate()`

**Best practices**:
- Use with counter metrics only
- Best for ranges of `[2m]` to `[5m]`
- More volatile than `rate()`, shows spikes
- Good for alerting on sudden changes

**When to use**: For alerting on spike detection, real-time dashboards showing immediate changes.

**Rate vs irate**:
- `rate()`: Average over time range, smooth
- `irate()`: Instant based on last 2 points, volatile
- For graphing: use `rate()`
- For spike alerts: use `irate()`

**Native Histogram Support (Prometheus 3.3+)**: `irate()` and `idelta()` now work with native histograms, enabling instant rate calculations on histogram data.

```promql
# Instant rate on native histogram (Prometheus 3.3+)
irate(http_request_duration_seconds[5m])
```

### increase

Calculates total increase over a time range.

```promql
# Total requests in the last hour
increase(http_requests_total[1h])

# Total bytes sent in the last day
increase(bytes_sent_total[24h])
```

**How it works**:
- Syntactic sugar for `rate(v) * range_in_seconds`
- Returns total increase (not per-second)
- Automatically handles counter resets
- Extrapolates to range boundaries

**Best practices**:
- Use with counter metrics only
- Useful for calculating totals over periods
- Result can be fractional due to extrapolation

**When to use**: Calculating totals for billing, capacity planning, SLO calculations.

### resets

Counts the number of counter resets within a time range.

```promql
# Number of times counter reset in last hour
resets(http_requests_total[1h])
```

**When to use**: Detecting application restarts, investigating metric inconsistencies.

## Time Functions

Functions for extracting time components and working with timestamps.

### time

Returns current evaluation timestamp as seconds since Unix epoch.

```promql
# Current timestamp
time()

# Time since metric was last seen (in seconds)
time() - max(metric_timestamp)
```

**Use for**: Calculating age of data, time-based math.

### timestamp

Returns timestamp of each sample in the instant vector.

```promql
# Get timestamp of last scrape
timestamp(up)

# Time since last successful backup
time() - timestamp(last_backup_success)
```

**Use for**: Checking staleness, calculating time since event.

### year / month / day_of_month / day_of_week

Extract time components from Unix timestamp.

```promql
# Current year
year()

# Current month (1-12)
month()

# Current day of month (1-31)
day_of_month()

# Current day of week (0=Sunday, 6=Saturday)
day_of_week()

# Extract from specific timestamp
year(timestamp(last_backup))
```

**Use for**: Time-based filtering, business hour alerting.

### hour / minute

Extract hour (0-23) or minute (0-59) from timestamp.

```promql
# Current hour
hour()

# Current minute
minute()

# Check if within business hours (9 AM - 5 PM)
hour() >= 9 and hour() < 17
```

**Use for**: Time-of-day alerting, business hour filtering.

### days_in_month

Returns number of days in the month of the timestamp.

```promql
# Days in current month
days_in_month()

# Days in month of specific timestamp
days_in_month(timestamp(metric))
```

**Use for**: Calendar calculations, month-end processing.

## Prometheus 3.x Time Functions (Experimental)

These functions are available in Prometheus 3.5+ behind the `--enable-feature=promql-experimental-functions` flag.

### ts_of_max_over_time

Returns the timestamp when the maximum value occurred in the range.

```promql
# When did CPU usage peak in the last hour?
ts_of_max_over_time(cpu_usage_percent[1h])

# Find when error spike happened
ts_of_max_over_time(rate(errors_total[5m])[1h:1m])
```

**Use for**: Incident investigation, finding when peaks occurred.

### ts_of_min_over_time

Returns the timestamp when the minimum value occurred in the range.

```promql
# When was memory usage lowest?
ts_of_min_over_time(memory_available_bytes[1h])

# Find when throughput dropped
ts_of_min_over_time(rate(requests_total[5m])[1h:1m])
```

**Use for**: Finding performance troughs, capacity planning.

### ts_of_last_over_time

Returns the timestamp of the last sample in the range.

```promql
# When was this metric last scraped?
ts_of_last_over_time(up[10m])

# Check data freshness
time() - ts_of_last_over_time(metric[1h])
```

**Use for**: Detecting stale data, monitoring scrape health.

### first_over_time (Prometheus 3.7+)

Returns the first (oldest) value in the time range.

> **Requires Feature Flag**: Must enable with `--enable-feature=promql-experimental-functions`

```promql
# Get the first value in a range
first_over_time(metric[1h])

# Compare current vs initial value
metric - first_over_time(metric[1h])

# Calculate change over time window
last_over_time(metric[1h]) - first_over_time(metric[1h])
```

**Use for**: Baseline comparisons, detecting drift, calculating change over time.

### ts_of_first_over_time (Prometheus 3.7+)

Returns the timestamp of the first sample in the range.

> **Requires Feature Flag**: Must enable with `--enable-feature=promql-experimental-functions`

```promql
# When did this time series start?
ts_of_first_over_time(metric[24h])

# How long has this metric existed?
time() - ts_of_first_over_time(metric[7d])
```

**Use for**: Tracking when metrics first appeared, calculating metric age.

### mad_over_time (Experimental)

Calculates the median absolute deviation of all float samples in the specified interval.

> **Requires Feature Flag**: Must enable with `--enable-feature=promql-experimental-functions`

```promql
# Median absolute deviation of CPU usage over 1 hour
mad_over_time(cpu_usage_percent[1h])

# Detect anomalies: values far from median
metric > avg_over_time(metric[1h]) + 3 * mad_over_time(metric[1h])
```

**Use for**: Anomaly detection, measuring variability robustly (less sensitive to outliers than stddev).

### sort_by_label (Experimental)

Returns vector elements sorted by the values of the given labels in ascending order.

> **Requires Feature Flag**: Must enable with `--enable-feature=promql-experimental-functions`

```promql
# Sort by service name
sort_by_label(up, "service")

# Sort by multiple labels
sort_by_label(http_requests_total, "job", "instance")
```

**How it works**:
- Sorts by the specified label values alphabetically
- If label values are equal, elements are sorted by their full label sets
- Acts on both float and histogram samples
- Only affects instant queries (range queries have fixed ordering)

**Use for**: Organizing query results for display, dashboard ordering.

### sort_by_label_desc (Experimental)

Same as `sort_by_label`, but sorts in descending order.

> **Requires Feature Flag**: Must enable with `--enable-feature=promql-experimental-functions`

```promql
# Sort by service name (descending)
sort_by_label_desc(up, "service")
```

**Use for**: Reverse alphabetical ordering of results.

## Math Functions

Mathematical operations on metric values.

### abs

Returns absolute value.

```promql
# Absolute value of temperature difference
abs(current_temp - target_temp)
```

### ceil / floor

Rounds up or down to nearest integer.

```promql
# Round up CPU count
ceil(cpu_count_fractional)

# Round down memory in GB
floor(memory_bytes / 1024 / 1024 / 1024)
```

### round

Rounds to nearest integer or specified precision.

```promql
# Round to nearest integer
round(cpu_usage_percent)

# Round to nearest 0.1
round(response_time_seconds, 0.1)

# Round to nearest 10
round(request_count, 10)
```

### sqrt

Calculates square root.

```promql
# Standard deviation calculation
sqrt(avg(metric^2) - avg(metric)^2)
```

### exp / ln / log2 / log10

Exponential and logarithmic functions.

```promql
# Natural exponential
exp(log_scale_metric)

# Natural logarithm
ln(exponential_metric)

# Base-2 logarithm
log2(power_of_two_metric)

# Base-10 logarithm
log10(large_number_metric)
```

### clamp / clamp_max / clamp_min

Limits values to a range.

```promql
# Clamp between 0 and 100
clamp(metric, 0, 100)

# Cap at maximum
clamp_max(metric, 100)

# Ensure minimum
clamp_min(metric, 0)
```

**Use for**: Normalizing values, preventing display overflow.

### sgn

Returns sign of value: 1 for positive, 0 for zero, -1 for negative.

```promql
# Get sign of temperature delta
sgn(current_temp - target_temp)
```

## Native Histogram Functions (Prometheus 3.x+)

Native histograms are now **stable** in Prometheus 3.x. These functions work with native histogram data.

### histogram_quantile (Native Histograms)

For native histograms, the syntax is simpler - no `_bucket` suffix or `le` label needed:

```promql
# Native histogram quantile (simpler syntax)
histogram_quantile(0.95,
  sum by (job) (rate(http_request_duration_seconds[5m]))
)

# Compare with classic histogram (requires _bucket and le)
histogram_quantile(0.95,
  sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

### histogram_count

Extracts the count of observations from a native histogram.

```promql
# Rate of observations per second
histogram_count(rate(http_request_duration_seconds[5m]))

# Total observations in time window
histogram_count(increase(http_request_duration_seconds[1h]))
```

**Use for**: Getting request counts from native histogram metrics.

### histogram_sum

Extracts the sum of observations from a native histogram.

```promql
# Sum of all observation values
histogram_sum(rate(http_request_duration_seconds[5m]))

# Average value from native histogram
histogram_sum(rate(http_request_duration_seconds[5m]))
/
histogram_count(rate(http_request_duration_seconds[5m]))
```

**Use for**: Calculating averages, total latency.

### histogram_fraction

Calculates the fraction of observations between two values in a native histogram.

```promql
# Fraction of requests under 100ms
histogram_fraction(0, 0.1, rate(http_request_duration_seconds[5m]))

# Percentage of requests between 100ms and 500ms
histogram_fraction(0.1, 0.5, rate(http_request_duration_seconds[5m])) * 100

# SLO compliance: percentage under threshold
histogram_fraction(0, 0.2, rate(http_request_duration_seconds[5m])) >= 0.95
```

**Use for**: SLO compliance calculations, distribution analysis.

### histogram_stddev

Calculates the estimated standard deviation of observations in a native histogram.

```promql
# Standard deviation of request durations
histogram_stddev(rate(http_request_duration_seconds[5m]))
```

**How it works**:
- Assumes observations within a bucket are at the mean of bucket boundaries
- For zero buckets and custom-boundary buckets: uses arithmetic mean
- For exponential buckets: uses geometric mean
- Float samples are ignored and do not appear in the returned vector

**Use for**: Understanding variability in metrics, anomaly detection.

### histogram_stdvar

Calculates the estimated standard variance of observations in a native histogram.

```promql
# Standard variance of request durations
histogram_stdvar(rate(http_request_duration_seconds[5m]))

# Compare variance across services
histogram_stdvar(sum by (service) (rate(http_request_duration_seconds[5m])))
```

**How it works**:
- Same estimation method as `histogram_stddev` (variance = stddev²)
- Assumes observations within a bucket are at the mean of bucket boundaries
- For zero buckets and custom-boundary buckets: uses arithmetic mean
- For exponential buckets: uses geometric mean
- Float samples are ignored and do not appear in the returned vector

**Use for**: Statistical analysis, comparing variability across dimensions.

### histogram_avg

Calculates average from a native histogram (shorthand for sum/count).

```promql
# Average request duration
histogram_avg(rate(http_request_duration_seconds[5m]))
```

**Use for**: Quick average calculations.

---

## Prometheus 3.0 Breaking Changes and New Features

This section documents important changes in Prometheus 3.0 (released November 2024) that affect PromQL queries.

### Breaking Changes

1. **Range Selectors Now Left-Open**
   - In Prometheus 3.0, range selectors exclude samples at the lower time boundary
   - A sample coinciding with the lower time limit is now excluded (previously included)
   - This affects queries like `rate(metric[5m])` where the 5-minute-ago sample may behave differently

2. **`holt_winters` Renamed to `double_exponential_smoothing`**
   - The function is now behind `--enable-feature=promql-experimental-functions`
   - See the [double_exponential_smoothing](#double_exponential_smoothing-formerly-holt_winters) section

3. **Regex `.` Now Matches All Characters**
   - The `.` regex pattern now matches all characters including newlines
   - This is a performance improvement but may affect regex-based label matching

### New Features

1. **UTF-8 Metric and Label Names**
   - Prometheus 3.0 allows UTF-8 characters in metric and label names by default
   - Use the quoting syntax for UTF-8 metrics: `{"metric.name.with" = "value"}`

2. **Native Histograms Stable**
   - Native histograms are now stable (no longer experimental)
   - See the [Native Histogram Functions](#native-histogram-functions-prometheus-3x) section

3. **New Experimental Time Functions** (require `--enable-feature=promql-experimental-functions`)
   - `first_over_time()` - Returns the first value in a range (Prometheus 3.7+)
   - `ts_of_first_over_time()` - Timestamp of first sample (Prometheus 3.7+)
   - `ts_of_max_over_time()` - When maximum occurred (Prometheus 3.5+)
   - `ts_of_min_over_time()` - When minimum occurred (Prometheus 3.5+)
   - `ts_of_last_over_time()` - Timestamp of last sample (Prometheus 3.5+)

---

## Classic Histogram and Summary Functions

Functions for working with classic histogram and summary metrics.

### histogram_quantile

Calculates φ-quantile (0 ≤ φ ≤ 1) from histogram buckets.

```promql
# 95th percentile of request duration
histogram_quantile(0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)

# 50th percentile (median) by service
histogram_quantile(0.5,
  sum by (service, le) (rate(http_request_duration_seconds_bucket[5m]))
)

# 99th percentile with job label preserved
histogram_quantile(0.99,
  sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

**Critical requirements**:
- Must have `le` label (bucket upper bound)
- Must use `rate()` or `irate()` on bucket counters
- Result is interpolated, not exact
- Requires buckets on both sides of the quantile

**Best practices**:
- Always aggregate with `sum` before calling `histogram_quantile()`
- Keep `le` label in aggregation: `sum by (le)` or `sum by (job, le)`
- Apply `rate()` inside the aggregation
- Use appropriate time range for `rate()` (typically `[5m]`)

**Common mistakes**:
- ❌ `histogram_quantile(0.95, rate(metric_bucket[5m]))` - Missing aggregation
- ❌ `histogram_quantile(0.95, sum(metric_bucket))` - Missing rate() and le label
- ✅ `histogram_quantile(0.95, sum by (le) (rate(metric_bucket[5m])))` - Correct

**When to use**: Calculating latency percentiles, response time SLOs.

### histogram_count / histogram_sum

Extracts total count or sum of observations from histogram.

```promql
# Total number of requests (from histogram)
histogram_count(http_request_duration_seconds)

# Total duration of all requests
histogram_sum(http_request_duration_seconds)

# Average request duration
histogram_sum(http_request_duration_seconds)
/
histogram_count(http_request_duration_seconds)
```

**Note**: For classic histograms, use `_count` and `_sum` suffixes instead:
```promql
http_request_duration_seconds_count
http_request_duration_seconds_sum
```

### histogram_fraction

Calculates fraction of observations between two values.

```promql
# Fraction of requests faster than 100ms
histogram_fraction(0, 0.1, http_request_duration_seconds)

# Percentage of requests between 100ms and 500ms
histogram_fraction(0.1, 0.5, http_request_duration_seconds) * 100
```

**Use for**: Calculating SLO compliance, analyzing distribution.

## Range Vector Functions

Functions that operate on range vectors (time series over a duration).

### *_over_time Functions

Calculate statistics over a time range.

```promql
# Average value over last 5 minutes
avg_over_time(cpu_usage_percent[5m])

# Maximum value over last hour
max_over_time(memory_usage_bytes[1h])

# Minimum value over last 10 minutes
min_over_time(disk_available_bytes[10m])

# Sum of values over time range
sum_over_time(event_counter[1h])

# Count of samples in time range
count_over_time(metric[5m])

# Standard deviation over time
stddev_over_time(response_time[5m])

# Variance over time
stdvar_over_time(response_time[5m])

# Quantile over time
quantile_over_time(0.95, response_time[5m])

# First value in range (oldest)
present_over_time(metric[5m])

# Changes (count of value changes)
changes(metric[5m])
```

**Best practices**:
- Use with gauge metrics for analysis
- Don't use with counter metrics (use `rate()` instead)
- Common ranges: `[5m]`, `[1h]`, `[1d]`

**Use cases**:
- `avg_over_time()`: Smoothing noisy gauges
- `max_over_time()` / `min_over_time()`: Peak/trough detection
- `changes()`: Detecting flapping or instability

### deriv

Calculates per-second derivative using linear regression.

```promql
# Rate of change of queue length
deriv(queue_length[5m])
```

**Use for**: Predicting trends, detecting gradual changes.

### predict_linear

Predicts value at future time using linear regression.

```promql
# Predict disk usage in 4 hours
predict_linear(disk_usage_bytes[1h], 4*3600)

# Predict when disk will be full
(disk_capacity_bytes - disk_usage_bytes)
/
deriv(disk_usage_bytes[1h])
```

**Use for**: Capacity forecasting, preemptive alerting.

### double_exponential_smoothing (formerly holt_winters)

Calculates smoothed value using double exponential smoothing (Holt Linear method).

> **Prometheus 3.0 Breaking Change**: This function was renamed from `holt_winters` to `double_exponential_smoothing` in Prometheus 3.0. The old name `holt_winters` no longer works.
>
> **Requires Feature Flag**: Must enable with `--enable-feature=promql-experimental-functions`

```promql
# Smooth and forecast metric (Prometheus 3.0+)
double_exponential_smoothing(metric[1h], 0.5, 0.5)

# For Prometheus 2.x, use the old name:
# holt_winters(metric[1h], 0.5, 0.5)
```

**Parameters**:
- First number (sf): smoothing factor (0-1) - lower values give more weight to old data
- Second number (tf): trend factor (0-1) - higher values consider more trends

**Important Notes**:
- Should only be used with gauge metrics
- Only works with float samples (histogram samples are ignored)
- The rename was done because "Holt-Winters" usually refers to triple exponential smoothing, while this implementation is double exponential smoothing (also called "Holt Linear")

**Use for**: Seasonal pattern detection, anomaly detection, trend forecasting.

## Label Manipulation Functions

Functions for modifying labels on time series.

### label_replace

Replaces label value using regex. Syntax:
`label_replace(v, dst_label, replacement, src_label, regex)`

```promql
# Extract hostname from instance (remove port)
# Input: instance="server-1:9090" → Output: hostname="server-1"
label_replace(
  up,
  "hostname",        # destination label name
  "$1",              # replacement ($1 = first capture group)
  "instance",        # source label
  "(.+):\\d+"        # regex (capture everything before :port)
)

# Extract region from instance FQDN
# Input: instance="web-1.us-east-1.example.com:9090"
# Output: region="us-east-1"
label_replace(
  metric,
  "region",
  "$1",
  "instance",
  "[^.]+\\.([^.]+)\\..*"
)

# Create environment label from job name
# Input: job="api-production" → Output: env="production"
label_replace(
  metric,
  "env",
  "$1",
  "job",
  ".*-(.*)"
)

# Copy label to new name (rename)
label_replace(
  metric,
  "service",         # new label name
  "$1",
  "job",             # original label
  "(.*)"             # match everything
)

# Add static prefix/suffix to label
label_replace(
  metric,
  "full_name",
  "prefix-$1-suffix",
  "name",
  "(.*)"
)

# Handle missing labels (empty replacement if no match)
label_replace(
  metric,
  "extracted",
  "$1",
  "optional_label",
  "pattern-(.*)"     # Returns empty string if no match
)
```

**Syntax notes**:
- `$1`, `$2`, etc. refer to regex capture groups
- If regex doesn't match, the destination label gets an empty string
- If destination label already exists, it gets overwritten

**Use for**: Creating new labels, extracting parts of label values, renaming labels.

### label_join

Joins multiple label values with a separator. Syntax:
`label_join(v, dst_label, separator, src_label1, src_label2, ...)`

```promql
# Combine job and instance into single label
# Input: job="api", instance="server-1" → Output: job_instance="api:server-1"
label_join(
  metric,
  "job_instance",    # destination label name
  ":",               # separator
  "job",             # first source label
  "instance"         # second source label
)

# Create full path from multiple labels
# Input: namespace="prod", service="api", pod="api-xyz"
# Output: full_path="prod/api/api-xyz"
label_join(
  metric,
  "full_path",
  "/",
  "namespace",
  "service",
  "pod"
)

# Create unique identifier
label_join(
  metric,
  "uid",
  "-",
  "cluster",
  "namespace",
  "pod"
)

# Join with empty separator (concatenate)
label_join(
  metric,
  "combined",
  "",
  "prefix",
  "name"
)
```

**Use for**: Combining labels for grouping, creating unique identifiers, display purposes.

### info() Function (Experimental)

The `info()` function (experimental in Prometheus 3.x) enriches metrics with labels from info metrics like `target_info`.

> **Requires Feature Flag**: Must enable with `--enable-feature=promql-experimental-functions`

**Syntax**: `info(v instant-vector, [data-label-selector instant-vector])`

```promql
# Enrich metrics with target_info labels
info(
  rate(http_requests_total[5m]),
  {k8s_cluster_name=~".+"}
)

# Without data-label-selector (adds all data labels from matching info metrics)
info(rate(http_requests_total[5m]))

# Equivalent using raw join (works in all Prometheus versions)
rate(http_requests_total[5m])
* on (job, instance) group_left (k8s_cluster_name, k8s_namespace_name)
  target_info
```

**How it works**:
- Finds, for each time series in `v`, all info series with matching identifying labels
- Adds the union of their data (non-identifying) labels to the time series
- The optional second argument constrains which info series to consider and which data labels to add
- Identifying labels are the subset of labels that uniquely identify the info series

**Current Limitations**:
- This is an experimental function and behavior may change
- Designed to improve UX around including labels from info metrics
- Works best with OpenTelemetry's `target_info` metric

**Use for**: Adding resource attributes from OpenTelemetry, enriching metrics with metadata, simplifying group_left joins with info metrics.

## Utility Functions

Miscellaneous utility functions.

### absent

Returns 1-element vector if input is empty, otherwise returns empty.

```promql
# Alert if metric is missing
absent(up{job="critical-service"})

# Alert if no instances are up
absent(up{job="api"} == 1)
```

**Use for**: Alerting on missing metrics or time series.

### absent_over_time

Returns 1 if no samples exist in the time range.

```promql
# Alert if no data for 10 minutes
absent_over_time(metric[10m])
```

**Use for**: Detecting data gaps, scrape failures.

### scalar

Converts single-element instant vector to scalar.

```promql
# Convert vector to scalar for math
scalar(sum(up{job="api"}))

# Use in calculations
metric * scalar(sum(scaling_factor))
```

**Warning**: Returns NaN if input has 0 or >1 elements.

### vector

Converts scalar to single-element instant vector.

```promql
# Convert number to vector
vector(123)

# Current timestamp as vector
vector(time())
```

**Use for**: Combining scalars with vector operations.

### sort / sort_desc

Sorts instant vector by value.

```promql
# Sort ascending
sort(http_requests_total)

# Sort descending
sort_desc(http_requests_total)
```

**Use for**: Display ordering (topk/bottomk are usually better).

## Advanced Functions

### group

Returns constant 1 for each time series, removing all values.

```promql
# Get all time series without values
group(metric)
```

**Use for**: Existence checks, label discovery.

## Function Chaining

Functions can be chained to build complex queries:

```promql
# Multi-stage aggregation
topk(10,
  sum by (endpoint) (
    rate(http_requests_total{job="api"}[5m])
  )
)

# Nested time-based calculations
max_over_time(
  rate(metric[5m])[1h:1m]
)

# Complex ratio with aggregations
(
  sum by (job) (rate(http_errors_total[5m]))
  /
  sum by (job) (rate(http_requests_total[5m]))
) * 100
```

## Performance Considerations

1. **Range Vector Size**: Larger ranges process more data
   - `[5m]` is fast and usually sufficient
   - `[1h]` or larger can be expensive
   - Use recording rules for large ranges used frequently

2. **Cardinality**: Functions on high-cardinality metrics are expensive
   - Add label filters to reduce series count
   - Use aggregation to reduce dimensions
   - Avoid operations on bare metric names

3. **Subqueries**: Can be very expensive
   - Limit subquery ranges
   - Consider recording rules for complex subqueries
   - Test query performance before production use

4. **Regex**: Slower than exact matches
   - Use `=` instead of `=~` when possible
   - Keep regex patterns simple
   - Anchor patterns when possible

## Function Decision Tree

**For Counters** (metrics with `_total`, `_count`, `_sum`, `_bucket`):
- Graphing trends → `rate()`
- Detecting spikes → `irate()`
- Calculating totals → `increase()`
- Checking for resets → `resets()`

**For Gauges** (memory, temperature, queue depth):
- Current value → use directly
- Average over time → `avg_over_time()`
- Peak detection → `max_over_time()` / `min_over_time()`
- Smoothing noisy data → `avg_over_time()`

**For Histograms** (`_bucket` suffix with `le` label):
- Percentiles → `histogram_quantile()`
- Average → use `_sum` / `_count`
- Request count → use `_count`

**For Summaries** (pre-calculated quantiles):
- Use quantile labels directly
- Don't average quantiles
- Calculate average from `_sum` / `_count`

---

## Reference: Promql_Patterns

# PromQL Query Patterns

Common query patterns for typical monitoring scenarios, organized by use case.

## Table of Contents

1. [RED Method (Request-Driven Services)](#red-method)
2. [USE Method (Resources)](#use-method)
3. [Request Patterns](#request-patterns)
4. [Error Patterns](#error-patterns)
5. [Latency Patterns](#latency-patterns)
6. [Resource Usage Patterns](#resource-usage-patterns)
7. [Availability Patterns](#availability-patterns)
8. [Saturation Patterns](#saturation-patterns)
9. [Ratio Calculations](#ratio-calculations)
10. [Time-Based Patterns](#time-based-patterns)
11. [Alerting Patterns](#alerting-patterns)

---

## RED Method

The RED method focuses on three key metrics for request-driven services:
- **Rate**: Throughput (requests per second)
- **Errors**: Error rate (failed requests)
- **Duration**: Latency (response time)

### Rate: Request Throughput

```promql
# Total requests per second across all instances
sum(rate(http_requests_total{job="api-server"}[5m]))

# Requests per second by endpoint
sum by (endpoint) (rate(http_requests_total{job="api-server"}[5m]))

# Requests per second by status code
sum by (status_code) (rate(http_requests_total{job="api-server"}[5m]))

# Requests per second by method and endpoint
sum by (method, endpoint) (rate(http_requests_total{job="api-server"}[5m]))

# Total requests per minute (instead of per second)
sum(rate(http_requests_total{job="api-server"}[5m])) * 60
```

### Errors: Error Rate

```promql
# Error ratio (0 to 1)
sum(rate(http_requests_total{job="api-server", status_code=~"5.."}[5m]))
/
sum(rate(http_requests_total{job="api-server"}[5m]))

# Error percentage (0 to 100)
(
  sum(rate(http_requests_total{job="api-server", status_code=~"5.."}[5m]))
  /
  sum(rate(http_requests_total{job="api-server"}[5m]))
) * 100

# Error rate by endpoint
sum by (endpoint) (rate(http_requests_total{status_code=~"5.."}[5m]))
/
sum by (endpoint) (rate(http_requests_total[5m]))

# 4xx client errors separately
sum(rate(http_requests_total{status_code=~"4.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

### Duration: Latency

```promql
# 95th percentile latency
histogram_quantile(0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket{job="api-server"}[5m]))
)

# Multiple percentiles
histogram_quantile(0.50, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))  # P50 (median)
histogram_quantile(0.90, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))  # P90
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))  # P95
histogram_quantile(0.99, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))  # P99

# Average latency
sum(rate(http_request_duration_seconds_sum[5m]))
/
sum(rate(http_request_duration_seconds_count[5m]))

# Latency by endpoint
histogram_quantile(0.95,
  sum by (endpoint, le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

---

## USE Method

The USE method focuses on resources:
- **Utilization**: Percentage of resource in use
- **Saturation**: Queue depth or resource contention
- **Errors**: Error counters

### Utilization: Resource Usage

```promql
# CPU utilization percentage
(
  1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))
) * 100

# Memory utilization percentage
(
  (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
  /
  node_memory_MemTotal_bytes
) * 100

# Disk utilization percentage
(
  (node_filesystem_size_bytes - node_filesystem_avail_bytes)
  /
  node_filesystem_size_bytes
) * 100

# Network utilization (as percentage of capacity)
(
  rate(node_network_transmit_bytes_total[5m])
  /
  node_network_speed_bytes
) * 100
```

### Saturation: Queue Depth

```promql
# Load average (normalized by CPU count)
node_load1
/
count without (cpu, mode) (node_cpu_seconds_total{mode="idle"})

# Average queue length
avg_over_time(queue_depth{job="worker"}[5m])

# Maximum queue depth in last hour
max_over_time(queue_depth{job="worker"}[1h])

# Thread pool saturation
active_threads / max_threads
```

### Errors: Resource Errors

```promql
# Network receive errors per second
rate(node_network_receive_errs_total[5m])

# Disk I/O errors
rate(node_disk_io_errors_total[5m])

# Out of memory kills
rate(node_vmstat_oom_kill[5m])
```

---

## Request Patterns

### Total Requests

```promql
# Total requests (instant count)
sum(http_requests_total)

# Total requests in last hour
sum(increase(http_requests_total[1h]))

# Total requests by service
sum by (service) (http_requests_total)
```

### Request Rate Over Time

```promql
# Current request rate
rate(http_requests_total[5m])

# Request rate comparison: current vs 1 hour ago
rate(http_requests_total[5m])
-
rate(http_requests_total[5m] offset 1h)

# Request rate comparison: current vs 1 week ago
rate(http_requests_total[5m])
/
rate(http_requests_total[5m] offset 1w)
```

### Top Endpoints

```promql
# Top 10 endpoints by request count
topk(10, sum by (endpoint) (rate(http_requests_total[5m])))

# Bottom 5 endpoints (least used)
bottomk(5, sum by (endpoint) (rate(http_requests_total[5m])))
```

---

## Error Patterns

### Error Count and Rate

```promql
# Total errors per second
sum(rate(http_errors_total[5m]))

# Errors by type
sum by (error_type) (rate(errors_total[5m]))

# Specific error rate
rate(http_requests_total{status_code="503"}[5m])
```

### Error Ratios

```promql
# Overall error rate
sum(rate(errors_total[5m]))
/
sum(rate(requests_total[5m]))

# Error rate by service
sum by (service) (rate(errors_total[5m]))
/
sum by (service) (rate(requests_total[5m]))

# Success rate (inverse of error rate)
1 - (
  sum(rate(errors_total[5m]))
  /
  sum(rate(requests_total[5m]))
)
```

### Error Trending

```promql
# Rate of change in errors
deriv(sum(errors_total)[10m])

# Predicted error count in 1 hour
predict_linear(errors_total[30m], 3600)
```

---

## Latency Patterns

### Percentile Calculations

```promql
# Standard percentiles from histogram
histogram_quantile(0.50, sum by (le) (rate(latency_bucket[5m])))  # Median
histogram_quantile(0.90, sum by (le) (rate(latency_bucket[5m])))  # P90
histogram_quantile(0.95, sum by (le) (rate(latency_bucket[5m])))  # P95
histogram_quantile(0.99, sum by (le) (rate(latency_bucket[5m])))  # P99
histogram_quantile(0.999, sum by (le) (rate(latency_bucket[5m]))) # P99.9

# Percentiles by service
histogram_quantile(0.95,
  sum by (service, le) (rate(request_duration_seconds_bucket[5m]))
)
```

### Average and Aggregate Latency

```promql
# Average latency
sum(rate(request_duration_seconds_sum[5m]))
/
sum(rate(request_duration_seconds_count[5m]))

# Maximum latency across all instances
max(max_over_time(request_duration_seconds[5m]))

# Minimum latency
min(min_over_time(request_duration_seconds[5m]))
```

### Latency SLO Compliance

```promql
# Percentage of requests under 200ms
(
  sum(rate(request_duration_seconds_bucket{le="0.2"}[5m]))
  /
  sum(rate(request_duration_seconds_count[5m]))
) * 100

# Percentage of requests violating SLO (over 1s)
(
  sum(rate(request_duration_seconds_count[5m]))
  -
  sum(rate(request_duration_seconds_bucket{le="1"}[5m]))
) / sum(rate(request_duration_seconds_count[5m])) * 100
```

---

## Resource Usage Patterns

### CPU

```promql
# CPU usage percentage by mode
sum by (mode) (rate(node_cpu_seconds_total[5m])) * 100

# Total CPU usage (excluding idle)
(
  sum(rate(node_cpu_seconds_total{mode!="idle"}[5m]))
  /
  sum(rate(node_cpu_seconds_total[5m]))
) * 100

# CPU usage by instance
100 - (
  avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100
)

# Container CPU usage (percentage of limit)
(
  rate(container_cpu_usage_seconds_total[5m])
  /
  container_spec_cpu_quota * container_spec_cpu_period
) * 100
```

### Memory

```promql
# Available memory in GB
node_memory_MemAvailable_bytes / 1024 / 1024 / 1024

# Memory usage percentage
(
  (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
  /
  node_memory_MemTotal_bytes
) * 100

# Container memory usage (percentage of limit)
(
  container_memory_usage_bytes
  /
  container_spec_memory_limit_bytes
) * 100

# Memory usage by namespace (Kubernetes)
sum by (namespace) (container_memory_usage_bytes)
```

### Disk

```promql
# Disk space available in GB
node_filesystem_avail_bytes / 1024 / 1024 / 1024

# Disk usage percentage
(
  (node_filesystem_size_bytes - node_filesystem_avail_bytes)
  /
  node_filesystem_size_bytes
) * 100

# Disk I/O rate (reads + writes per second)
rate(node_disk_reads_completed_total[5m]) + rate(node_disk_writes_completed_total[5m])

# Time until disk full (prediction in hours)
(
  node_filesystem_avail_bytes
  /
  deriv(node_filesystem_avail_bytes[1h])
) / 3600
```

### Network

```promql
# Network receive rate in MB/s
rate(node_network_receive_bytes_total[5m]) / 1024 / 1024

# Network transmit rate in MB/s
rate(node_network_transmit_bytes_total[5m]) / 1024 / 1024

# Total network throughput
(
  rate(node_network_receive_bytes_total[5m])
  +
  rate(node_network_transmit_bytes_total[5m])
) / 1024 / 1024

# Network error rate
rate(node_network_receive_errs_total[5m]) + rate(node_network_transmit_errs_total[5m])
```

---

## Availability Patterns

### Service Uptime

```promql
# Percentage of instances that are up
(count(up{job="api-server"} == 1) / count(up{job="api-server"})) * 100

# Number of instances up
count(up{job="api-server"} == 1)

# Number of instances down
count(up{job="api-server"} == 0)

# Uptime by service
sum by (job) (up == 1) / count by (job) (up) * 100
```

### Uptime Duration

```promql
# Time since last restart (in hours)
(time() - process_start_time_seconds) / 3600

# Minimum uptime across instances (in days)
min((time() - process_start_time_seconds) / 86400)
```

### Success Rate

```promql
# HTTP success rate (2xx + 3xx)
sum(rate(http_requests_total{status_code=~"[23].."}[5m]))
/
sum(rate(http_requests_total[5m]))

# Health check success rate
sum(rate(health_check_total{result="success"}[5m]))
/
sum(rate(health_check_total[5m]))
```

---

## Saturation Patterns

### Queue Metrics

```promql
# Current queue size
queue_size

# Average queue size over time
avg_over_time(queue_size[10m])

# Queue processing rate
rate(queue_processed_total[5m])

# Queue fill rate
rate(queue_added_total[5m]) - rate(queue_processed_total[5m])

# Time to drain queue (in seconds)
queue_size / rate(queue_processed_total[5m])
```

### Thread Pool Saturation

```promql
# Active threads ratio
active_threads / max_threads

# Thread pool utilization percentage
(active_threads / max_threads) * 100

# Rejected tasks rate
rate(thread_pool_rejected_total[5m])
```

### Connection Pool

```promql
# Active connections ratio
active_connections / max_connections

# Connection pool utilization
(active_connections / max_connections) * 100

# Connection wait time
connection_wait_duration_seconds
```

---

## Ratio Calculations

### Basic Ratios

```promql
# Success/failure ratio
rate(success_total[5m]) / rate(failure_total[5m])

# Cache hit ratio
rate(cache_hits_total[5m])
/
(rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))

# Write/read ratio
rate(writes_total[5m]) / rate(reads_total[5m])
```

### Efficiency Metrics

```promql
# Requests per CPU core
sum(rate(http_requests_total[5m]))
/
count(node_cpu_seconds_total{mode="idle"})

# Throughput per GB of memory
sum(rate(bytes_processed_total[5m]))
/
sum(node_memory_MemTotal_bytes / 1024 / 1024 / 1024)

# Cost per request (if cost metric exists)
sum(cost_dollars_total) / sum(http_requests_total)
```

---

## Time-Based Patterns

### Comparing with Historical Data

```promql
# Current vs 1 hour ago
metric - metric offset 1h

# Current vs yesterday
metric - metric offset 1d

# Current vs last week
metric - metric offset 1w

# Percentage change from yesterday
((metric - metric offset 1d) / metric offset 1d) * 100
```

### Time-of-Day Analysis

```promql
# Note: hour() and day_of_week() evaluate in UTC.

# Only show data during business hours (9 AM - 5 PM UTC)
metric and on() (hour() >= 9 and hour() < 17)

# Only show data on weekdays (Monday-Friday UTC)
metric and on() (day_of_week() >= 1 and day_of_week() <= 5)

# Weekend metrics (Saturday-Sunday UTC)
metric and on() (day_of_week() == 0 or day_of_week() == 6)
```

### Trend Analysis

```promql
# Rate of change over time
deriv(metric[10m])

# Predict value in 1 hour
predict_linear(metric[30m], 3600)

# Smoothed trend (Double Exponential Smoothing)
# Note: holt_winters was renamed to double_exponential_smoothing in Prometheus 3.0
# Requires --enable-feature=promql-experimental-functions
double_exponential_smoothing(metric[1h], 0.5, 0.5)
```

---

## Alerting Patterns

### Threshold Alerts

```promql
# CPU usage above 80%
(1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m]))) * 100 > 80

# Error rate above 5%
(
  sum(rate(errors_total[5m]))
  /
  sum(rate(requests_total[5m]))
) > 0.05

# Disk space below 10%
(node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100 < 10

# Latency above 1 second
histogram_quantile(0.95, sum by (le) (rate(latency_bucket[5m]))) > 1
```

### Rate of Change Alerts

```promql
# Error rate increasing rapidly
deriv(sum(errors_total)[10m]) > 10

# Sudden traffic spike (>50% increase in 5 minutes)
(
  (rate(requests_total[5m]) - rate(requests_total[5m] offset 5m))
  /
  rate(requests_total[5m] offset 5m)
) > 0.5
```

### Absence Alerts

```promql
# Alert if metric is missing
absent(up{job="critical-service"})

# Alert if no data for 10 minutes
absent_over_time(metric[10m])

# Alert if no successful health checks
absent(health_check{result="success"})
```

### Multi-Condition Alerts

```promql
# High error rate AND high latency
(
  (sum(rate(errors_total[5m])) / sum(rate(requests_total[5m]))) > 0.05
)
and
(
  histogram_quantile(0.95, sum by (le) (rate(latency_bucket[5m]))) > 1
)

# Low availability AND high error rate
(
  (count(up{job="api"} == 1) / count(up{job="api"})) < 0.9
)
and
(
  sum(rate(errors_total[5m])) > 10
)
```

---

## Vector Matching and Joins

Vector matching enables combining data from different metrics. Essential for enriching metrics with metadata and correlating related time series.

### Basic One-to-One Matching

```promql
# Default: match on all common labels
metric_a + metric_b

# Result includes only series where both metrics have matching labels
# Output has labels present in both sides
```

### Using `on()` for Explicit Label Matching

```promql
# Match only on specific labels
metric_a + on (job, instance) metric_b

# Match ignoring specific labels
metric_a + ignoring (version, pod) metric_b
```

### Many-to-One Joins with `group_left`

Use `group_left` when the left side has more time series than the right side. The result includes labels from both sides.

```promql
# Enrich metrics with version info from info metric
rate(http_requests_total[5m])
* on (job, instance) group_left (version, environment)
  app_version_info

# Join container metrics with kube_pod_info
sum by (namespace, pod) (
  rate(container_cpu_usage_seconds_total{container!=""}[5m])
)
* on (namespace, pod) group_left (node, created_by_name)
  kube_pod_info

# Add target_info labels to metrics (OpenTelemetry pattern)
rate(http_requests_total[5m])
* on (job, instance) group_left (k8s_cluster_name, k8s_namespace_name)
  target_info
```

### One-to-Many Joins with `group_right`

Use `group_right` when the right side has more time series.

```promql
# Service info on the right, metrics on the left
service_info
* on (service) group_right (version, owner)
  sum by (service) (rate(requests_total[5m]))
```

### Joining Metrics with Different Label Names

Use `label_replace` to create matching labels when metrics use different label names.

```promql
# Metric A uses "server", Metric B uses "host"
# First, rename "server" to "host" in metric_a
label_replace(metric_a, "host", "$1", "server", "(.*)")
* on (host) group_left ()
  metric_b

# Alternative: rename in both metrics to a common name
label_replace(metric_a, "machine", "$1", "server", "(.*)")
* on (machine)
  label_replace(metric_b, "machine", "$1", "host", "(.*)")
```

### Enriching with Info Metrics

Info metrics are gauges with constant value 1 that carry metadata labels.

```promql
# Common info metric pattern
# info_metric{label1="value1", label2="value2", ...} = 1

# Join to add metadata labels to metrics
up
* on (job, instance) group_left (version, commit)
  build_info

# Kubernetes: Add node info to pod metrics
sum by (namespace, pod, node) (
  kube_pod_info
  * on (pod, namespace) group_right (node)
    sum by (namespace, pod) (
      rate(container_cpu_usage_seconds_total[5m])
    )
)
```

### Extracting Deployment Name from ReplicaSet

```promql
# ReplicaSet names are deployment_name + "-" + random_suffix
# Extract deployment name from owner reference
sum by (namespace, deployment) (
  label_replace(
    kube_pod_container_resource_requests{resource="cpu"},
    "deployment",
    "$1",
    "pod",
    "(.+)-[^-]+-[^-]+"  # Match deployment-replicaset-pod pattern
  )
)
```

### Conditional Joins

```promql
# Only include series where both conditions are met
metric_a > 100
and on (job, instance)
metric_b > 50

# Include all from left, filter by right
metric_a
and on (job)
(metric_b > 100)

# Exclude series present in right side
metric_a
unless on (job)
metric_b
```

### Aggregating Before Joining

```promql
# Wrong: joining before aggregating can cause mismatches
rate(http_requests_total[5m])
* on (instance) group_left (version)
  app_info

# Better: aggregate first, then join
sum by (job, instance) (rate(http_requests_total[5m]))
* on (job, instance) group_left (version)
  app_info
```

### Kubernetes Join Patterns

```promql
# CPU usage with pod owner (deployment, statefulset, etc.)
sum by (namespace, pod) (
  rate(container_cpu_usage_seconds_total{container!="", container!="POD"}[5m])
)
* on (namespace, pod) group_left (owner_name, owner_kind)
  kube_pod_owner

# Memory usage with node zone label
sum by (namespace, pod, node) (
  container_memory_working_set_bytes{container!="", container!="POD"}
)
* on (node) group_left (label_topology_kubernetes_io_zone)
  kube_node_labels

# Requests with service selector labels
sum by (namespace, service) (
  rate(http_requests_total[5m])
)
* on (namespace, service) group_left (label_app, label_version)
  kube_service_labels
```

### Vector Matching Operators Summary

| Operator | Purpose | Example |
|----------|---------|---------|
| `on (labels)` | Match only on specified labels | `a + on (job) b` |
| `ignoring (labels)` | Match ignoring specified labels | `a + ignoring (pod) b` |
| `group_left (labels)` | Many-to-one, copy labels from right | `a * on (job) group_left (version) b` |
| `group_right (labels)` | One-to-many, copy labels from left | `a * on (job) group_right (version) b` |
| `and on ()` | Intersection (both sides match) | `a and on (job) b` |
| `or on ()` | Union (either side) | `a or on (job) b` |
| `unless on ()` | Exclusion (left minus right) | `a unless on (job) b` |

### Common Pitfalls

```promql
# ❌ Wrong: Missing group_left for many-to-one join
rate(http_requests_total[5m]) * on (instance) app_info

# ✅ Correct: Use group_left
rate(http_requests_total[5m]) * on (instance) group_left () app_info

# ❌ Wrong: group_left without on()
rate(http_requests_total[5m]) * group_left (version) app_info

# ✅ Correct: Always pair group_left with on()
rate(http_requests_total[5m]) * on (job, instance) group_left (version) app_info

# ❌ Wrong: Joining on high-cardinality labels causes explosion
metric_a * on (request_id) metric_b

# ✅ Correct: Aggregate first or use lower-cardinality labels
sum by (job) (metric_a) * on (job) sum by (job) (metric_b)
```

---

## Best Practices Summary

1. **Always use label filters** to reduce cardinality
2. **Use appropriate time ranges** - typically `[5m]` for real-time, `[1h]` for trends
3. **Aggregate before histogram_quantile()** - always include `sum by (le)`
4. **Use rate() for counters** - don't query counter values directly
5. **Format for readability** - use multi-line for complex queries
6. **Test queries** - verify they return expected results before productionizing
7. **Use recording rules** - pre-compute expensive queries used frequently
8. **Consider cardinality** - avoid high-cardinality labels in aggregations
9. **Apply exact matches** - use `=` instead of `=~` when possible
10. **Document queries** - add comments explaining complex logic

---

## Pattern Selection Guide

**For monitoring request-driven services**:
- Use RED method (Rate, Errors, Duration)
- Focus on request rate, error rate, and latency percentiles

**For monitoring resources** (CPU, memory, disk):
- Use USE method (Utilization, Saturation, Errors)
- Track usage percentage, queue depth, and error counters

**For alerting**:
- Use threshold-based alerts for known limits
- Use rate-of-change alerts for anomaly detection
- Combine conditions for more accurate alerts

**For dashboards**:
- Use smooth metrics (rate, avg_over_time)
- Show multiple percentiles for latency
- Include comparison with historical data

**For capacity planning**:
- Use predict_linear() for forecasting
- Track trends over longer periods
- Monitor saturation metrics
