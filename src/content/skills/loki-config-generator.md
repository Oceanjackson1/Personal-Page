---
title: "Loki Config Generator"
description: "Generate/create Loki configs — ingester, querier, compactor, ruler, S3/GCS/Azure backends."
category: "devops"
source: "community"
author: "Community"
tags: ["loki", "config", "generator"]
date: 2026-03-20
---

# Loki Configuration Generator

## Overview

Generate production-ready Grafana Loki server configurations with best practices. Supports monolithic, simple scalable, and microservices deployment modes with S3, GCS, Azure, or filesystem storage.

> **Current Stable:** Loki 3.6.2 (November 2025)
> **Important:** Promtail deprecated in 3.4 - use [Grafana Alloy](https://grafana.com/docs/alloy/latest/) instead. See `examples/grafana-alloy.yaml` for log collection configuration.

## When to Use

Invoke when: deploying Loki, creating configs from scratch, migrating to Loki, implementing multi-tenant logging, configuring storage backends, or optimizing existing deployments.

---

## Generation Methods

### Method 1: Script Generation (Recommended)

**Use `scripts/generate_config.py` for consistent, validated configurations:**

```bash
# Simple Scalable with S3 (production)
python3 scripts/generate_config.py \
  --mode simple-scalable \
  --storage s3 \
  --bucket my-loki-bucket \
  --region us-east-1 \
  --retention-days 30 \
  --otlp-enabled \
  --output loki-config.yaml

# Monolithic with filesystem (development)
python3 scripts/generate_config.py \
  --mode monolithic \
  --storage filesystem \
  --no-auth-enabled \
  --output loki-dev.yaml

# Production with Thanos storage (Loki 3.4+)
python3 scripts/generate_config.py \
  --mode simple-scalable \
  --storage s3 \
  --thanos-storage \
  --otlp-enabled \
  --time-sharding \
  --output loki-thanos.yaml
```

**Script Options:**
| Option | Description |
|--------|-------------|
| `--mode` | monolithic, simple-scalable, microservices |
| `--storage` | filesystem, s3, gcs, azure |
| `--auth-enabled` / `--no-auth-enabled` | Explicitly enable/disable auth |
| `--otlp-enabled` | Enable OTLP ingestion configuration |
| `--thanos-storage` | Use Thanos object storage client (3.4+, cloud backends) |
| `--time-sharding` | Enable out-of-order ingestion (simple-scalable) |
| `--ruler` | Enable alerting/recording rules (not monolithic) |
| `--horizontal-compactor` | main/worker mode (simple-scalable, 3.6+) |
| `--zone-awareness` | Enable multi-AZ placement safeguards |
| `--limits-dry-run` | Log limit rejections without enforcing |

### Method 2: Manual Configuration

Follow the staged workflow below when script generation doesn't meet specific requirements or when learning the configuration structure.

### Output Formats

For Kubernetes deployments, generate BOTH formats:
1. **Native Loki config** (`loki-config.yaml`) - For ConfigMap or direct use
2. **Helm values** (`values.yaml`) - For Helm chart deployments

See `examples/kubernetes-helm-values.yaml` for Helm format.

---

## Documentation Lookup

### When to Use Context7/Web Search

**REQUIRED - Use Context7 MCP for:**
- Configuring features from Loki 3.4+ (Thanos storage, time sharding)
- Configuring features from Loki 3.6+ (horizontal compactor, enforced labels)
- Bloom filter configuration (complex, experimental)
- Custom OTLP attribute mappings beyond standard patterns
- Troubleshooting configuration errors

**OPTIONAL - Skip documentation lookup for:**
- Standard deployment modes (monolithic, simple-scalable)
- Basic storage configuration (S3, GCS, Azure, filesystem)
- Default limits and component settings
- Configurations covered in `references/` directory

### Context7 MCP (preferred)

```
resolve-library-id: "grafana loki"
get-library-docs: /websites/grafana_loki, topic: [component]
```

**Example topics:** `storage_config`, `limits_config`, `otlp`, `compactor`, `ruler`, `bloom`

### Web Search Fallback

Use when Context7 unavailable: `"Grafana Loki 3.6 [component] configuration documentation site:grafana.com"`

---

## Configuration Workflow

### Stage 1: Gather Requirements

**Deployment Mode:**
| Mode | Scale | Use Case |
|------|-------|----------|
| Monolithic | <100GB/day | Testing, development |
| Simple Scalable | 100GB-1TB/day | Production |
| Microservices | >1TB/day | Large-scale, multi-tenant |

**Storage Backend:** S3, GCS, Azure Blob, Filesystem, MinIO

**Key Questions:** Expected log volume? Retention period? Multi-tenancy needed? High availability requirements? Kubernetes deployment?

Ask the user directly if required information is missing.

### Stage 2: Schema Configuration (CRITICAL)

For all new deployments (Loki 2.9+), use TSDB with v13 schema:

```yaml
schema_config:
  configs:
    - from: "2025-01-01"  # Use deployment date
      store: tsdb
      object_store: s3     # s3, gcs, azure, filesystem
      schema: v13
      index:
        prefix: loki_index_
        period: 24h
```

**Key:** Schema cannot change after deployment without migration.

### Stage 3: Storage Configuration

**S3:**
```yaml
common:
  storage:
    s3:
      s3: s3://us-east-1/loki-bucket
      s3forcepathstyle: false
```

**GCS:** `gcs: { bucket_name: loki-bucket }`
**Azure:** `azure: { container_name: loki-container, account_name: ${AZURE_ACCOUNT_NAME} }`
**Filesystem:** `filesystem: { chunks_directory: /loki/chunks, rules_directory: /loki/rules }`

### Stage 4: Component Configuration

**Ingester:**
```yaml
ingester:
  chunk_encoding: snappy
  chunk_idle_period: 30m
  max_chunk_age: 2h
  chunk_target_size: 1572864  # 1.5MB
  lifecycler:
    ring:
      replication_factor: 3  # 3 for production
```

**Querier:**
```yaml
querier:
  max_concurrent: 4
  query_timeout: 1m
```

**Compactor:**
```yaml
compactor:
  working_directory: /loki/compactor
  compaction_interval: 10m
  retention_enabled: true
  retention_delete_delay: 2h
```

### Stage 5: Limits Configuration

```yaml
limits_config:
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
  max_streams_per_user: 10000
  max_entries_limit_per_query: 5000
  max_query_length: 721h
  retention_period: 30d
  allow_structured_metadata: true
  volume_enabled: true
```

### Stage 6: Server & Auth

```yaml
server:
  http_listen_port: 3100
  grpc_listen_port: 9096
  log_level: info

auth_enabled: true  # false for single-tenant
```

### Stage 7: OTLP Ingestion (Loki 3.0+)

Native OpenTelemetry ingestion - use `otlphttp` exporter (NOT deprecated `lokiexporter`):

```yaml
limits_config:
  allow_structured_metadata: true
  otlp_config:
    resource_attributes:
      attributes_config:
        - action: index_label  # Low-cardinality only!
          attributes: [service.name, service.namespace, deployment.environment]
        - action: structured_metadata  # High-cardinality
          attributes: [k8s.pod.name, service.instance.id]
```

**Actions:** `index_label` (searchable, low-cardinality), `structured_metadata` (queryable), `drop`

> **⚠️ NEVER use `k8s.pod.name` as index_label** - use structured_metadata instead.

**OTel Collector:**
```yaml
exporters:
  otlphttp:
    endpoint: http://loki:3100/otlp
```

### Stage 8: Caching

```yaml
chunk_store_config:
  chunk_cache_config:
    memcached_client:
      host: memcached-chunks
      timeout: 500ms

query_range:
  cache_results: true
  results_cache:
    cache:
      memcached_client:
        host: memcached-results
```

### Stage 9: Advanced Features

**Pattern Ingester (3.0+):**
```yaml
pattern_ingester:
  enabled: true
```

**Bloom Filters (Experimental, 3.3+):** Only for >75TB/month deployments. Works on structured metadata only. See examples/ for config.

**Time Sharding (3.4+):** For out-of-order ingestion:
```yaml
limits_config:
  shard_streams:
    time_sharding_enabled: true
```

**Thanos Storage (3.4+):** New storage client, opt-in now, default later:
```yaml
storage_config:
  use_thanos_objstore: true
  object_store:
    s3:
      bucket_name: my-bucket
      endpoint: s3.us-west-2.amazonaws.com
```

### Stage 10: Ruler (Alerting)

```yaml
ruler:
  storage:
    type: s3
    s3: { bucket_name: loki-ruler }
  alertmanager_url: http://alertmanager:9093
  enable_api: true
  enable_sharding: true
```

### Stage 11: Loki 3.6 Features

- **Horizontally Scalable Compactor:** `horizontal_scaling_mode: main|worker`
- **Policy-Based Enforced Labels:** `enforced_labels: [service.name]`
- **FluentBit v4:** `structured_metadata` parameter support

### Stage 12: Validate Configuration (REQUIRED)

**Always validate before deployment:**

```bash
# Syntax and parameter validation
loki -config.file=loki-config.yaml -verify-config

# Print resolved configuration (shows defaults)
loki -config.file=loki-config.yaml -print-config-stderr 2>&1 | head -100

# Dry-run with Docker (if Loki not installed locally)
docker run --rm -v $(pwd)/loki-config.yaml:/etc/loki/config.yaml \
  grafana/loki:3.6.2 -config.file=/etc/loki/config.yaml -verify-config
```

**Validation Checklist:**
- [ ] No syntax errors from `-verify-config`
- [ ] Schema uses `tsdb` and `v13`
- [ ] `replication_factor: 3` for production
- [ ] `auth_enabled: true` if multi-tenant
- [ ] Storage credentials/IAM configured
- [ ] Retention period matches requirements

---

## Production Checklist

### High Availability Requirements

**Zone-Aware Replication (CRITICAL for production multi-AZ deployments):**

When using `replication_factor: 3`, ALWAYS enable zone-awareness for multi-AZ deployments:

```yaml
ingester:
  lifecycler:
    ring:
      replication_factor: 3
      zone_awareness_enabled: true  # CRITICAL for multi-AZ

# Set zone via environment variable or config
# Each pod should set its zone based on node topology
common:
  instance_availability_zone: ${AVAILABILITY_ZONE}
```

**Why:** Without zone-awareness, all 3 replicas may land in the same AZ. If that AZ fails, you lose data.

**Kubernetes Implementation:**
```yaml
# In Helm values or pod spec
env:
  - name: AVAILABILITY_ZONE
    valueFrom:
      fieldRef:
        fieldPath: metadata.labels['topology.kubernetes.io/zone']
```

### TLS Configuration (Production Required)

Enable TLS for all inter-component and client communication:

```yaml
server:
  http_tls_config:
    cert_file: /etc/loki/tls/tls.crt
    key_file: /etc/loki/tls/tls.key
    client_ca_file: /etc/loki/tls/ca.crt  # For mTLS
  grpc_tls_config:
    cert_file: /etc/loki/tls/tls.crt
    key_file: /etc/loki/tls/tls.key
    client_ca_file: /etc/loki/tls/ca.crt
```

See `examples/production-tls.yaml` for complete TLS configuration.

### Production Checklist Summary

| Requirement | Setting | Required For |
|-------------|---------|--------------|
| `replication_factor: 3` | common block | All production |
| `zone_awareness_enabled: true` | ingester.lifecycler.ring | Multi-AZ |
| `auth_enabled: true` | root level | Multi-tenant |
| TLS enabled | server block | All production |
| IAM roles (not keys) | storage config | Cloud storage |
| Caching enabled | chunk_store_config, query_range | Performance |
| Pattern ingester | pattern_ingester.enabled | Observability |
| Retention configured | compactor + limits_config | Cost control |

---

## Monitoring Recommendations

### Key Metrics to Monitor

Configure Prometheus to scrape Loki metrics and alert on these critical indicators:

```yaml
# Prometheus scrape config
- job_name: 'loki'
  static_configs:
    - targets: ['loki:3100']
```

### Critical Alerts

```yaml
groups:
  - name: loki-critical
    rules:
      # Ingestion failures
      - alert: LokiIngestionFailures
        expr: sum(rate(loki_distributor_ingester_append_failures_total[5m])) > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Loki ingestion failures detected"

      # High stream cardinality (performance killer)
      - alert: LokiHighStreamCardinality
        expr: loki_ingester_memory_streams > 100000
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High stream cardinality - review labels"

      # Compaction not running (retention broken)
      - alert: LokiCompactionStalled
        expr: time() - loki_compactor_last_successful_run_timestamp_seconds > 7200
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Loki compaction stalled - retention not enforced"

      # Query latency
      - alert: LokiSlowQueries
        expr: histogram_quantile(0.99, sum(rate(loki_request_duration_seconds_bucket{route=~"loki_api_v1_query.*"}[5m])) by (le)) > 30
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Loki query P99 latency > 30s"

      # Ingester memory pressure
      - alert: LokiIngesterMemoryHigh
        expr: container_memory_usage_bytes{container="ingester"} / container_spec_memory_limit_bytes{container="ingester"} > 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Loki ingester memory usage > 80%"
```

### Key Metrics Reference

| Metric | Description | Action Threshold |
|--------|-------------|------------------|
| `loki_ingester_memory_streams` | Active streams in memory | >100k: review cardinality |
| `loki_distributor_ingester_append_failures_total` | Ingestion failures | >0: investigate immediately |
| `loki_request_duration_seconds` | Query latency | P99 >30s: add caching/queriers |
| `loki_ingester_chunks_flushed_total` | Chunk flush rate | Low rate: check ingester health |
| `loki_compactor_last_successful_run_timestamp_seconds` | Last compaction | >2h ago: compaction broken |

### Grafana Dashboard

Import official Loki dashboards:
- Dashboard ID: `13407` - Loki Logs
- Dashboard ID: `14055` - Loki Operational

---

## Log Collection with Grafana Alloy

> **Promtail is deprecated** (support ends Feb 2026). Use Grafana Alloy for new deployments.

### Basic Alloy Configuration

See `examples/grafana-alloy.yaml` for complete configuration.

```alloy
// Kubernetes log discovery
discovery.kubernetes "pods" {
  role = "pod"
}

// Relabeling for Kubernetes metadata
discovery.relabel "pods" {
  targets = discovery.kubernetes.pods.targets

  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    target_label  = "namespace"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_name"]
    target_label  = "pod"
  }
  rule {
    source_labels = ["__meta_kubernetes_pod_container_name"]
    target_label  = "container"
  }
}

// Log collection
loki.source.kubernetes "pods" {
  targets    = discovery.relabel.pods.output
  forward_to = [loki.write.default.receiver]
}

// Send to Loki
loki.write "default" {
  endpoint {
    url = "http://loki-gateway.loki.svc.cluster.local/loki/api/v1/push"

    // For multi-tenant
    tenant_id = "default"
  }
}
```

### Migration from Promtail

```bash
# Convert Promtail config to Alloy
alloy convert --source-format=promtail --output=alloy-config.alloy promtail.yaml
```

---

## Complete Examples

See `examples/` directory for full configurations:
- `monolithic-filesystem.yaml` - Development/testing
- `simple-scalable-s3.yaml` - Production with S3
- `microservices-s3.yaml` - Large-scale distributed
- `multi-tenant.yaml` - Multi-tenant with per-tenant limits
- `production-tls.yaml` - TLS-enabled production config
- `grafana-alloy.yaml` - Log collection with Alloy
- `kubernetes-helm-values.yaml` - Helm chart values

**Minimal Monolithic:**
```yaml
auth_enabled: false
server:
  http_listen_port: 3100

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2025-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: loki_index_
        period: 24h

limits_config:
  retention_period: 30d
  allow_structured_metadata: true

compactor:
  working_directory: /loki/compactor
  retention_enabled: true
```

---

## Helm Deployment

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki -f values.yaml
```

**Generate both native config and Helm values for Kubernetes deployments.**

```yaml
# values.yaml
deploymentMode: SimpleScalable

loki:
  schemaConfig:
    configs:
      - from: "2025-01-01"
        store: tsdb
        object_store: s3
        schema: v13
        index:
          prefix: loki_index_
          period: 24h
  limits_config:
    retention_period: 30d
    allow_structured_metadata: true
  # Zone awareness for HA
  ingester:
    lifecycler:
      ring:
        zone_awareness_enabled: true

backend:
  replicas: 3
  # Spread across zones
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: DoNotSchedule
read:
  replicas: 3
write:
  replicas: 3
```

---

## Best Practices

**Performance:**
- `chunk_encoding: snappy`, `chunk_target_size: 1572864`
- Enable caching (chunks, results)
- `parallelise_shardable_queries: true`

**Security:**
- `auth_enabled: true` with reverse proxy auth
- IAM roles for cloud storage (never hardcode keys)
- TLS for all communications (see Production Checklist)

**Reliability:**
- `replication_factor: 3` for production
- `zone_awareness_enabled: true` for multi-AZ (see Production Checklist)
- Persistent volumes for ingesters
- Monitor ingestion rate and query latency (see Monitoring section)

**Limits:** Set `ingestion_rate_mb`, `max_streams_per_user` to prevent overload

---

## Common Issues

| Issue | Solution |
|-------|----------|
| High ingester memory | Reduce `max_streams_per_user`, lower `chunk_idle_period` |
| Slow queries | Increase `max_concurrent`, enable parallelization, add caching |
| Ingestion failures | Check `ingestion_rate_mb`, verify storage connectivity |
| Storage growing fast | Enable retention, check compression, review cardinality |
| Data loss in AZ failure | Enable `zone_awareness_enabled: true` |
| Config validation fails | Run `loki -verify-config`, check YAML syntax |

---

## Deprecated (Migrate Away)

- `boltdb-shipper` → `tsdb`
- `lokiexporter` → `otlphttp`
- Promtail → Grafana Alloy (support ends Feb 2026)

---

## Resources

**scripts/generate_config.py** - Generate configs programmatically (RECOMMENDED)
**examples/** - Complete configuration examples for all modes
**references/** - Full parameter reference and best practices

## Related Skills

- **logql-generator** - LogQL query generation
- **fluentbit-generator** - Log collection to Loki

---

## Reference: Best_Practices

# Loki Configuration Best Practices

This document outlines best practices for configuring and deploying Grafana Loki in production environments.

> **Important Notice (Loki 3.4+):** Promtail has been deprecated and its code merged into Grafana Alloy. For new log collection deployments, use [Grafana Alloy](https://grafana.com/docs/alloy/latest/) instead of Promtail.

## Schema Configuration

### Use TSDB with v13 Schema (CRITICAL)

**Always use the latest schema** for new deployments:

```yaml
schema_config:
  configs:
    - from: "2025-01-01"  # Use deployment date
      store: tsdb
      object_store: s3
      schema: v13
      index:
        prefix: loki_index_
        period: 24h
```

**Why:**
- TSDB is the modern, performant index store
- v13 schema provides best performance and features
- Cannot be changed after deployment without migration
- Daily period (`24h`) is recommended for most use cases

**Important:** Set `from` date to your deployment date, not a past date.

## Deployment Modes

### Choose the Right Deployment Mode

| Mode | Use Case | Ingestion | Complexity |
|------|----------|-----------|------------|
| **Monolithic** | Development, testing, small deployments | <100GB/day | Low |
| **Simple Scalable** | Production, moderate scale | 100GB-1TB/day | Medium |
| **Microservices** | Large scale, multi-tenancy | >1TB/day | High |

**Monolithic:**
- Single binary with all components
- Easy to operate
- Limited scalability
- Good for getting started

**Simple Scalable:**
- Separates read, write, and backend
- Horizontal scaling
- Production-ready
- Recommended for most use cases

**Microservices:**
- Full component separation
- Maximum scalability
- Independent scaling per component
- Requires more operational overhead

## Storage Configuration

### Storage Backend Selection

**Filesystem:**
- Development and testing only
- Requires persistent volumes
- Not recommended for production at scale

**Object Storage (S3, GCS, Azure):**
- Recommended for production
- Cost-effective at scale
- Durable and highly available
- Use IAM roles/service accounts for authentication

**Best practices:**
```yaml
common:
  storage:
    s3:
      s3: s3://region/bucket-name
      s3forcepathstyle: false
      # Use IAM roles instead of access keys
  replication_factor: 3  # Always use 3 for production
```

## Replication and High Availability

### Always Use Replication Factor 3

```yaml
common:
  replication_factor: 3
```

**Why:**
- Data durability: tolerates 2 node failures
- Query reliability: ensures data availability
- Industry standard for distributed systems

### Enable Zone-Aware Replication

For multi-AZ deployments:

```yaml
ingester:
  lifecycler:
    ring:
      zone_awareness_enabled: true
```

**Why:**
- Distributes replicas across availability zones
- Survives entire AZ failures
- Better fault tolerance

## Native OTLP Ingestion (Loki 3.0+)

### Configure OTLP Attributes

If using OpenTelemetry, configure how OTLP attributes are mapped:

```yaml
limits_config:
  allow_structured_metadata: true

  otlp_config:
    resource_attributes:
      ignore_defaults: false  # Set true to completely override defaults
      attributes_config:
        - action: index_label
          attributes:
            - service.name
            - service.namespace
            - deployment.environment
            # NOTE: Do NOT include high-cardinality attributes as index labels!
        - action: structured_metadata
          attributes:
            - k8s.pod.name           # High cardinality - use structured_metadata
            - service.instance.id    # High cardinality - use structured_metadata
    log_attributes:
      - action: structured_metadata
        attributes:
          - trace_id
          - span_id
```

> **⚠️ CRITICAL: Label Cardinality Best Practices (Updated 2025)**
>
> **DO NOT** use these high-cardinality attributes as index labels:
> - `k8s.pod.name` - Changes frequently, creates too many streams
> - `service.instance.id` - High cardinality
>
> Instead, store them as `structured_metadata`. This is now the recommended approach.
> See: https://grafana.com/docs/loki/latest/get-started/labels/remove-default-labels/

**Recommended index labels** (low-cardinality):
- `service.name`, `service.namespace`, `deployment.environment`
- `cloud.region`, `cloud.availability_zone`
- `k8s.cluster.name`, `k8s.namespace.name`, `k8s.container.name`
- `k8s.deployment.name`, `k8s.statefulset.name`, `k8s.daemonset.name`

**Configuring Default Resource Attributes:**

For more control over which OTLP resource attributes become labels:

```yaml
distributor:
  otlp_config:
    default_resource_attributes_as_index_labels:
      - service.name
      - service.namespace
      - deployment.environment
      - k8s.cluster.name
      - k8s.namespace.name
      # EXCLUDES: k8s.pod.name, service.instance.id
```

**Why:**
- Native OTLP support eliminates the need for Loki Exporter (deprecated)
- Control which attributes become labels vs structured metadata
- **Low-cardinality** attributes should be `index_label`
- **High-cardinality** attributes should be `structured_metadata`
- Use `ignore_defaults: true` for complete control over attribute mapping

**OTLP Endpoint:** `POST /otlp/v1/logs`

**OpenTelemetry Collector Configuration:**
```yaml
exporters:
  otlphttp:
    endpoint: http://loki:3100/otlp
    # Note: lokiexporter is DEPRECATED - use otlphttp instead

service:
  pipelines:
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp]
```

## Pattern Ingester (Loki 3.0+)

### Enable Pattern Detection

```yaml
pattern_ingester:
  enabled: true
```

**Why:**
- Automatic log pattern detection
- Powers Explore Logs / Grafana Drilldown features
- Identifies recurring patterns for anomaly detection
- Minimal resource overhead

## Caching Configuration

### Configure Memcached for Production

```yaml
# Chunk cache
chunk_store_config:
  chunk_cache_config:
    memcached:
      batch_size: 256
      parallelism: 10
    memcached_client:
      host: memcached-chunks.loki.svc.cluster.local
      service: memcached-client
      timeout: 500ms

# Results cache
query_range:
  cache_results: true
  results_cache:
    cache:
      memcached_client:
        host: memcached-results.loki.svc.cluster.local
        timeout: 500ms
```

**Important Notes:**
- **TSDB does NOT need index cache** - only chunks and results cache
- Use separate Memcached instances for chunks and results
- Size chunk cache based on query hot data volume
- Size results cache based on repeated query patterns

**Helm Chart Caching:**
```yaml
memcached:
  chunk_cache:
    enabled: true
  results_cache:
    enabled: true

memcachedChunks:
  enabled: true
  replicas: 2
  resources:
    requests:
      memory: 1Gi
    limits:
      memory: 2Gi
```

## Limits Configuration

### Set Appropriate Ingestion Limits

```yaml
limits_config:
  ingestion_rate_mb: 50  # Adjust based on expected load
  ingestion_burst_size_mb: 100  # 2x rate for bursts
  max_line_size: 256KB
  max_line_size_truncate: true
```

**Why:**
- Prevents resource exhaustion
- Protects against misconfigured clients
- Allows burst traffic while limiting sustained overload

### Control Stream Cardinality

```yaml
limits_config:
  max_streams_per_user: 10000
  max_global_streams_per_user: 100000
```

**Why:**
- High cardinality kills performance
- Each label combination creates a stream
- Limit prevents accidental label explosion

**Best practice:** Use line filters for high-cardinality data (user IDs, trace IDs) instead of labels.

### Configure Retention

```yaml
compactor:
  retention_enabled: true
  retention_delete_delay: 2h

limits_config:
  retention_period: 30d  # Adjust based on requirements
```

**Why:**
- Controls storage costs
- Meets compliance requirements
- Automatic cleanup of old data

## Chunk Management

### Optimize Chunk Settings

```yaml
ingester:
  chunk_encoding: snappy
  chunk_target_size: 1572864  # 1.5MB
  chunk_idle_period: 30m
  max_chunk_age: 2h
```

**Why:**
- `snappy`: Best balance of speed vs compression
- `1.5MB` target: Optimal chunk size (requires 5-10x raw data)
- `30m` idle: Flushes inactive chunks to storage
- `2h` max age: Prevents memory buildup

**Important:** More streams = more chunks in memory. Keep stream cardinality low.

## Query Performance

### Configure Query Concurrency

```yaml
querier:
  max_concurrent: 4  # Per querier instance
  query_timeout: 5m
```

**Recommendations:**
- Start with 4 concurrent queries
- Increase based on CPU/memory resources
- Monitor query latency and adjust

### Enable Query Parallelization

```yaml
query_range:
  parallelise_shardable_queries: true
  split_queries_by_interval: 15m  # For large time ranges
```

**Why:**
- Distributes query load across queriers
- Faster results for large time ranges
- Better resource utilization

## Security

### Enable Multi-Tenancy

```yaml
auth_enabled: true
```

**Production recommendation:**
- Always use `auth_enabled: true`
- Deploy authenticating reverse proxy (nginx, Envoy)
- Enforce `X-Scope-OrgID` header
- Isolate tenant data

### Use TLS for Inter-Component Communication

```yaml
server:
  http_tls_config:
    cert_file: /path/to/cert.pem
    key_file: /path/to/key.pem
  grpc_tls_config:
    cert_file: /path/to/cert.pem
    key_file: /path/to/key.pem
```

**Why:**
- Encrypts data in transit
- Prevents eavesdropping
- Required for compliance (PCI, HIPAA, etc.)

### Secure Credentials

**Never hardcode credentials:**
```yaml
# BAD
common:
  storage:
    s3:
      access_key_id: AKIAIOSFODNN7EXAMPLE
      secret_access_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# GOOD
common:
  storage:
    s3:
      # Uses IAM role automatically
```

**Best practices:**
- Use IAM roles for AWS
- Use service accounts for GCP
- Use managed identities for Azure
- Store secrets in Kubernetes Secrets or Vault
- Reference secrets via environment variables

## Monitoring and Observability

### Enable Metrics

Loki exports Prometheus metrics automatically. Scrape them:

```yaml
# In Prometheus config
- job_name: 'loki'
  static_configs:
    - targets: ['loki:3100']
```

**Key metrics to monitor:**
- `loki_ingester_chunks_flushed_total`: Chunk flush rate
- `loki_ingester_memory_streams`: Active streams (watch for growth)
- `loki_request_duration_seconds`: Query latency
- `loki_distributor_ingester_append_failures_total`: Ingestion failures
- `loki_boltdb_shipper_request_duration_seconds`: Index query time

### Set Up Alerts

**Critical alerts:**
```yaml
# High ingestion failure rate
- alert: LokiIngestionFailureRate
  expr: sum(rate(loki_distributor_ingester_append_failures_total[5m])) > 10

# Too many streams (cardinality explosion)
- alert: LokiHighStreamCardinality
  expr: loki_ingester_memory_streams > 100000

# Compaction not running
- alert: LokiCompactionNotRunning
  expr: time() - loki_boltdb_shipper_compact_tables_operation_last_successful_run_timestamp_seconds > 3600
```

## Resource Planning

### Ingester Resources

**Memory requirements:**
- Base: ~1GB per ingester
- Add: 1-2KB per active stream
- Add: Chunk buffer (depends on throughput)

**Example:** 10,000 streams = ~1GB + 20MB = ~1.2GB minimum

**Kubernetes recommendations:**
```yaml
resources:
  requests:
    memory: "4Gi"
    cpu: "1"
  limits:
    memory: "8Gi"
    cpu: "2"
```

### Querier Resources

**Memory requirements:**
- Base: ~500MB per querier
- Add: Depends on query complexity and concurrency

**CPU requirements:**
- Varies with query load
- More CPU = faster queries

**Kubernetes recommendations:**
```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1"
  limits:
    memory: "4Gi"
    cpu: "2"
```

### Storage Requirements

**Estimate storage:**
```
Daily storage = (ingestion rate MB/s) × 86400 seconds × compression ratio
```

**Compression ratios:**
- Text logs: 5-10x (snappy)
- JSON logs: 3-7x (snappy)
- Structured logs: 2-5x (snappy)

**Example:** 10 MB/s ingestion with 5x compression:
```
10 MB/s × 86400 × 0.2 = ~170 GB/day
```

## Operational Best Practices

### Use Health Checks

Configure Kubernetes probes:

```yaml
livenessProbe:
  httpGet:
    path: /ready
    port: 3100
  initialDelaySeconds: 45

readinessProbe:
  httpGet:
    path: /ready
    port: 3100
  initialDelaySeconds: 45
```

### Enable Graceful Shutdown

```yaml
server:
  graceful_shutdown_timeout: 30s
```

**Why:**
- Allows in-flight requests to complete
- Prevents data loss during restarts
- Smooth rolling updates

### Use Configuration Management

**Best practices:**
- Store configs in Git
- Use configuration as code (Terraform, Helm)
- Validate configs before applying
- Test in staging before production
- Document all customizations

### Regular Maintenance

**Weekly:**
- Review metrics and alerts
- Check for errors in logs
- Verify compaction is running

**Monthly:**
- Review and adjust limits based on actual usage
- Analyze storage growth trends
- Update Loki to latest stable version

**Quarterly:**
- Review architecture for scale
- Optimize queries and cardinality
- Conduct disaster recovery tests

## Common Anti-Patterns

### Don't Use High-Cardinality Labels

**BAD:**
```yaml
# Don't use user_id, trace_id, request_id as labels
{app="api", user_id="12345"}  # Creates too many streams
```

**GOOD:**
```yaml
# Use structured metadata or line filters instead
{app="api"} | json | user_id="12345"
```

### Don't Ignore Limits

**BAD:**
```yaml
limits_config:
  max_streams_per_user: 0  # Unlimited - dangerous!
```

**GOOD:**
```yaml
limits_config:
  max_streams_per_user: 10000  # Reasonable limit
```

### Don't Skip Replication

**BAD:**
```yaml
common:
  replication_factor: 1  # Single copy - data loss risk
```

**GOOD:**
```yaml
common:
  replication_factor: 3  # Durability and availability
```

### Don't Use Filesystem Storage in Production

**BAD:**
```yaml
common:
  storage:
    filesystem:
      chunks_directory: /loki/chunks  # Not scalable
```

**GOOD:**
```yaml
common:
  storage:
    s3:
      s3: s3://region/bucket  # Scalable and durable
```

### Don't Disable Authentication in Multi-Tenant Environments

**BAD:**
```yaml
auth_enabled: false  # No tenant isolation
```

**GOOD:**
```yaml
auth_enabled: true  # Proper tenant isolation
```

## Configuration Validation

### Before Deployment

1. **Validate syntax:**
   ```bash
   loki -config.file=loki.yaml -verify-config
   ```

2. **Review configuration:**
   ```bash
   loki -config.file=loki.yaml -print-config-stderr
   ```

3. **Test ingestion:**
   Send test logs and verify they appear

4. **Test queries:**
   Run sample LogQL queries

### After Deployment

1. **Check health:**
   ```bash
   curl http://loki:3100/ready
   ```

2. **Monitor metrics:**
   Review Prometheus metrics

3. **Verify data ingestion:**
   Check ingester and distributor logs

4. **Test query performance:**
   Run representative queries

## Troubleshooting Guide

### High Memory Usage

**Symptoms:**
- OOMKilled pods
- Slow queries
- High `loki_ingester_memory_streams`

**Solutions:**
- Reduce `max_streams_per_user`
- Lower `chunk_idle_period`
- Check for cardinality explosion
- Add more ingester replicas

### Slow Queries

**Symptoms:**
- Query timeouts
- High `loki_request_duration_seconds`

**Solutions:**
- Increase `max_concurrent` in querier
- Enable query parallelization
- Add caching
- Optimize LogQL queries (use specific stream selectors)
- Add more querier replicas

### Ingestion Failures

**Symptoms:**
- High `loki_distributor_ingester_append_failures_total`
- Missing logs

**Solutions:**
- Check ingestion rate limits
- Verify storage backend connectivity
- Check authentication headers
- Review distributor logs
- Increase ingester capacity

### Storage Growing Rapidly

**Symptoms:**
- Storage costs increasing
- Running out of disk space

**Solutions:**
- Enable retention
- Review log volume and cardinality
- Implement sampling or filtering at source
- Check chunk compression settings

## Thanos Object Storage Client (Loki 3.4+)

Loki 3.4 introduces new object storage clients based on the **Thanos Object Storage Client**. This is opt-in now but will become the default in future releases.

### Enable Thanos Storage

```yaml
storage_config:
  use_thanos_objstore: true
  object_store:
    s3:
      bucket_name: my-loki-bucket
      endpoint: s3.us-west-2.amazonaws.com
      region: us-west-2
```

**Key Migration Notes:**
- `use_thanos_objstore: true` is **mutually exclusive** with legacy storage config
- `disable_dualstack` → `dualstack_enabled` (inverted)
- `signature_version` removed (always uses V4)
- `http_config` → `http` (nested block)
- Multiple bucket support removed (use single `bucket_name`)
- Storage prefix cannot contain dashes (`-`) - use underscores

**When using Thanos storage, ruler storage must be configured separately:**
```yaml
ruler_storage:
  backend: s3
  s3:
    bucket_name: my-ruler-bucket
```

## Time Sharding for Out-of-Order Ingestion (Loki 3.4+)

For scenarios with delayed log delivery or historical imports:

```yaml
limits_config:
  shard_streams:
    time_sharding_enabled: true
```

**Use cases:**
- Log backfilling
- Delayed log delivery (network issues, batch processing)
- Multi-region log aggregation with varying latencies

## Bloom Filters (Experimental - Loki 3.0+)

> **Warning:** Bloom filters are experimental and intended for deployments ingesting >75TB/month.

> **⚠️ BREAKING CHANGE (Loki 3.3+):** Bloom filters now use **structured metadata** instead of free-text search. The block format (V3) is incompatible with previous versions. **Delete existing bloom blocks before upgrading to 3.3+**.

### When to Use

Bloom filters accelerate "needle in haystack" queries on **structured metadata**:

```yaml
bloom_build:
  enabled: true
  planner:
    planning_interval: 6h

bloom_gateway:
  enabled: true
  worker_concurrency: 4
  block_query_concurrency: 8

limits_config:
  bloom_creation_enabled: true
  bloom_gateway_enable_filtering: true
  tsdb_sharding_strategy: bounded
```

**Use when:**
- Large-scale deployments (>75TB/month)
- Frequent searches for specific values in structured metadata (trace IDs, UUIDs)
- Queries like: `{cluster="prod"} | traceID="3c0e3dcd33e7"`

**Don't use when:**
- Small deployments (overhead > benefit)
- Queries mostly use label selectors
- Budget is a concern (requires additional storage)
- Need free-text search (blooms work on structured metadata only)

**Best Practice for Bloom Queries:**
```logql
# Good - filter structured metadata BEFORE parser
{cluster="prod"} | trace_id="abc123" | json | level="error"

# Bad - parser runs first, blooms can't help
{cluster="prod"} | json | trace_id="abc123" | level="error"
```

## Deprecated Storage and Configuration

> **⚠️ Deprecation Warnings**

### Deprecated Index Stores
- `boltdb` / `boltdb-shipper` - Use `tsdb` instead
- `bigtable` - Migrate to TSDB
- `dynamodb` - Migrate to TSDB
- `cassandra` (for chunks) - Migrate to object storage

### Deprecated Tools
- **Promtail** - Deprecated in Loki 3.4, commercial support ends **February 28, 2026**
  - Use [Grafana Alloy](https://grafana.com/docs/alloy/latest/) instead
  - Migration: `alloy convert --source-format=promtail`
- **Grafana Agent** - Long-term support ended **October 31, 2025**
  - Migrate to [Grafana Alloy](https://grafana.com/docs/alloy/latest/)
- **lokiexporter** (OTel Collector) - Use `otlphttp` instead

### Migration from BoltDB to TSDB
```yaml
schema_config:
  configs:
    - from: 2020-01-01
      store: boltdb-shipper  # Keep for existing data
      schema: v11
    - from: 2025-01-01       # Add new period
      store: tsdb            # Use TSDB for new data
      schema: v13
```

## Additional Resources

- [Grafana Loki Best Practices](https://grafana.com/docs/loki/latest/configure/bp-configure/)
- [Loki Configuration Reference](https://grafana.com/docs/loki/latest/configure/)
- [Loki Operations Guide](https://grafana.com/docs/loki/latest/operations/)
- [Loki Helm Charts](https://grafana.com/docs/loki/latest/setup/install/helm/)
- [OTLP Ingestion](https://grafana.com/docs/loki/latest/send-data/otel/)
- [Grafana Alloy (Promtail replacement)](https://grafana.com/docs/alloy/latest/)

## Related Skills

- **logql-generator**: For generating LogQL queries
- **fluentbit-generator**: For log collection pipelines to Loki
- **promql-generator**: For Prometheus (monitoring Loki)

---

## Reference: Loki_Config_Reference

# Loki Configuration Reference

This document provides a comprehensive reference for Grafana Loki configuration parameters.

> **Current Stable Release:** Loki 3.6.2 (November 2025)

## Table of Contents

- [Server Configuration](#server-configuration)
- [Common Configuration](#common-configuration)
- [Schema Configuration](#schema-configuration)
- [Storage Configuration](#storage-configuration)
- [Ingester Configuration](#ingester-configuration)
- [Distributor Configuration](#distributor-configuration)
- [Querier Configuration](#querier-configuration)
- [Query Frontend Configuration](#query-frontend-configuration)
- [Query Range Configuration](#query-range-configuration)
- [Compactor Configuration](#compactor-configuration)
- [Limits Configuration](#limits-configuration)
- [Ruler Configuration](#ruler-configuration)
- [Pattern Ingester Configuration](#pattern-ingester-configuration)
- [Bloom Configuration](#bloom-configuration)
- [Memberlist Configuration](#memberlist-configuration)
- [Caching Configuration](#caching-configuration)

---

## Server Configuration

The `server` block configures the HTTP and gRPC server settings.

```yaml
server:
  # HTTP server listen address
  # CLI flag: -server.http-listen-address
  [http_listen_address: <string> | default = ""]

  # HTTP server listen port
  # CLI flag: -server.http-listen-port
  [http_listen_port: <int> | default = 3100]

  # gRPC server listen address
  # CLI flag: -server.grpc-listen-address
  [grpc_listen_address: <string> | default = ""]

  # gRPC server listen port
  # CLI flag: -server.grpc-listen-port
  [grpc_listen_port: <int> | default = 9095]

  # Log level: debug, info, warn, error
  # CLI flag: -log.level
  [log_level: <string> | default = "info"]

  # Log format: logfmt, json
  # CLI flag: -log.format
  [log_format: <string> | default = "logfmt"]

  # Timeout for graceful shutdown
  # CLI flag: -server.graceful-shutdown-timeout
  [graceful_shutdown_timeout: <duration> | default = 30s]

  # HTTP server read timeout
  # CLI flag: -server.http-read-timeout
  [http_server_read_timeout: <duration> | default = 30s]

  # HTTP server write timeout
  # CLI flag: -server.http-write-timeout
  [http_server_write_timeout: <duration> | default = 30s]

  # HTTP server idle timeout
  # CLI flag: -server.http-idle-timeout
  [http_server_idle_timeout: <duration> | default = 120s]

  # Maximum number of simultaneous gRPC connections
  # CLI flag: -server.grpc-max-concurrent-streams
  [grpc_server_max_concurrent_streams: <int> | default = 100]

  # TLS configuration for HTTP server
  http_tls_config:
    [cert_file: <string>]
    [key_file: <string>]
    [client_ca_file: <string>]

  # TLS configuration for gRPC server
  grpc_tls_config:
    [cert_file: <string>]
    [key_file: <string>]
    [client_ca_file: <string>]
```

---

## Common Configuration

The `common` block configures shared settings across components.

```yaml
common:
  # Path prefix for data storage
  [path_prefix: <string> | default = ""]

  # Instance address for ring registration
  [instance_addr: <string>]

  # Replication factor for data durability
  # CLI flag: -common.replication-factor
  [replication_factor: <int> | default = 3]

  # Storage configuration
  storage:
    # S3 storage configuration
    s3:
      [s3: <string>]  # s3://region/bucket format
      [s3forcepathstyle: <boolean> | default = false]
      [access_key_id: <string>]
      [secret_access_key: <string>]
      [endpoint: <string>]
      [region: <string>]
      [insecure: <boolean> | default = false]

    # GCS storage configuration
    gcs:
      [bucket_name: <string>]
      [service_account: <string>]
      [chunk_buffer_size: <int>]

    # Azure storage configuration
    azure:
      [container_name: <string>]
      [account_name: <string>]
      [account_key: <string>]
      [use_managed_identity: <boolean> | default = false]
      [user_assigned_id: <string>]

    # Filesystem storage configuration
    filesystem:
      [chunks_directory: <string>]
      [rules_directory: <string>]

  # Ring configuration for service discovery
  ring:
    kvstore:
      # Store type: consul, etcd, memberlist, inmemory
      [store: <string> | default = "memberlist"]
      [prefix: <string> | default = "collectors/"]

      # Consul configuration
      consul:
        [host: <string> | default = "localhost:8500"]
        [acl_token: <string>]

      # Etcd configuration
      etcd:
        [endpoints: <list of strings>]
        [username: <string>]
        [password: <string>]
```

---

## Schema Configuration

The `schema_config` block defines how Loki stores and indexes data. **This is critical and cannot be changed after deployment without migration.**

```yaml
schema_config:
  configs:
    # Date when this schema takes effect (YYYY-MM-DD format)
    - from: <daytime>

      # Index store type: tsdb, boltdb-shipper (deprecated)
      # TSDB is recommended for all new deployments
      [store: <string> | default = "tsdb"]

      # Object store type: s3, gcs, azure, filesystem
      [object_store: <string>]

      # Schema version: v13 is latest and recommended
      [schema: <string> | default = "v13"]

      # Index configuration
      index:
        # Table name prefix
        [prefix: <string> | default = "index_"]
        # Table period (24h recommended)
        [period: <duration> | default = 24h]
```

**Best Practice:** Always use `store: tsdb` and `schema: v13` for new deployments.

---

## Storage Configuration

### Legacy Storage Configuration

```yaml
storage_config:
  # TSDB shipper configuration
  tsdb_shipper:
    [active_index_directory: <string>]
    [cache_location: <string>]
    [cache_ttl: <duration> | default = 24h]
    index_gateway_client:
      [server_address: <string>]

  # AWS/S3 configuration
  aws:
    [s3: <string>]
    [s3forcepathstyle: <boolean>]
    [access_key_id: <string>]
    [secret_access_key: <string>]

  # GCS configuration
  gcs:
    [bucket_name: <string>]

  # Azure configuration
  azure:
    [container_name: <string>]
    [account_name: <string>]
    [account_key: <string>]

  # Filesystem configuration
  filesystem:
    [directory: <string>]
```

### Thanos Object Storage Client (Loki 3.4+)

The Thanos-based storage client provides consistent configuration across Grafana's databases.

```yaml
storage_config:
  # Enable Thanos object storage client
  # MUTUALLY EXCLUSIVE with legacy storage config
  use_thanos_objstore: true

  object_store:
    # Storage prefix for all objects (cannot contain dashes)
    [storage_prefix: <string>]

    # S3 configuration
    s3:
      [bucket_name: <string>]
      [endpoint: <string>]
      [region: <string>]
      [access_key_id: <string>]
      [secret_access_key: <string>]
      [native_aws_auth_enabled: <boolean> | default = false]
      [dualstack_enabled: <boolean> | default = false]
      [storage_class: <string> | default = "STANDARD"]
      [max_retries: <int> | default = 10]

      # HTTP client settings
      http:
        [idle_conn_timeout: <duration> | default = 1m30s]
        [response_header_timeout: <duration> | default = 2m]
        [insecure_skip_verify: <boolean> | default = false]

      # Server-side encryption
      sse:
        [type: <string>]  # SSE-KMS or SSE-S3
        [kms_key_id: <string>]
        [kms_encryption_context: <string>]

    # GCS configuration
    gcs:
      [bucket_name: <string>]
      [service_account: <string>]
      [chunk_buffer_size: <int>]
      [max_retries: <int> | default = 5]

    # Azure configuration
    azure:
      [account_name: <string>]
      [account_key: <string>]
      [container_name: <string>]
      [use_managed_identity: <boolean> | default = false]

    # Filesystem configuration
    filesystem:
      [dir: <string>]  # Note: 'dir' not 'directory'
```

**Migration Notes:**
- `use_thanos_objstore: true` is mutually exclusive with legacy storage config
- `disable_dualstack` → `dualstack_enabled` (inverted logic)
- `signature_version` removed (always uses V4)
- `http_config` → `http` (nested block)
- Storage prefix cannot contain dashes (`-`) - use underscores

---

## Ingester Configuration

The `ingester` block configures log ingestion and chunk management.

```yaml
ingester:
  # Chunk compression algorithm: snappy, gzip, lz4, none
  # CLI flag: -ingester.chunk-encoding
  [chunk_encoding: <string> | default = "snappy"]

  # Flush inactive chunks after this period
  # CLI flag: -ingester.chunk-idle-period
  [chunk_idle_period: <duration> | default = 30m]

  # Keep flushed chunks in memory for this duration
  # CLI flag: -ingester.chunk-retain-period
  [chunk_retain_period: <duration> | default = 15m]

  # Maximum age of a chunk before flushing
  # CLI flag: -ingester.max-chunk-age
  [max_chunk_age: <duration> | default = 2h]

  # Target compressed chunk size (bytes)
  # CLI flag: -ingester.chunk-target-size
  [chunk_target_size: <int> | default = 1572864]  # 1.5MB

  # Number of concurrent chunk flushes
  # CLI flag: -ingester.concurrent-flushes
  [concurrent_flushes: <int> | default = 16]

  # Flush check interval
  # CLI flag: -ingester.flush-check-period
  [flush_check_period: <duration> | default = 30s]

  # WAL (Write-Ahead Log) configuration
  wal:
    [enabled: <boolean> | default = true]
    [dir: <string> | default = "wal"]
    [flush_on_shutdown: <boolean> | default = true]
    [replay_memory_ceiling: <int>]

  # Lifecycler configuration for ring registration
  lifecycler:
    ring:
      kvstore:
        [store: <string>]
      [replication_factor: <int> | default = 3]
    [num_tokens: <int> | default = 128]
    [heartbeat_period: <duration> | default = 5s]
    [join_after: <duration> | default = 0s]
    [observe_period: <duration> | default = 0s]
    [interface_names: <list of strings>]
    [final_sleep: <duration> | default = 30s]
```

**Best Practices:**
- Use `chunk_encoding: snappy` for best speed/compression balance
- Target 1.5MB chunks requires 5-10x raw log data
- Set `replication_factor: 3` for production

---

## Distributor Configuration

The `distributor` block configures log distribution to ingesters.

```yaml
distributor:
  ring:
    kvstore:
      [store: <string>]
    [heartbeat_timeout: <duration> | default = 1m]

  # OTLP configuration for default resource attributes
  otlp_config:
    # Override default list of resource attributes promoted to index labels
    # Excludes high-cardinality attributes like k8s.pod.name, service.instance.id
    default_resource_attributes_as_index_labels:
      - service.name
      - service.namespace
      - deployment.environment
      - cloud.region
      - cloud.availability_zone
      - k8s.cluster.name
      - k8s.namespace.name
      - k8s.container.name
      - container.name
      - k8s.deployment.name
      - k8s.statefulset.name
      - k8s.daemonset.name
      - k8s.cronjob.name
      - k8s.job.name

  # Ingest limits (Loki 3.5+)
  [ingest_limits_enabled: <boolean> | default = false]
  [ingest_limits_dry_run_enabled: <boolean> | default = false]
```

---

## Querier Configuration

The `querier` block configures log query processing.

```yaml
querier:
  # Maximum concurrent queries per querier
  # CLI flag: -querier.max-concurrent
  [max_concurrent: <int> | default = 4]

  # Query timeout
  # CLI flag: -querier.query-timeout
  [query_timeout: <duration> | default = 1m]

  # Maximum duration for live tailing
  # CLI flag: -querier.tail-max-duration
  [tail_max_duration: <duration> | default = 1h]

  # Extra delay before sending queries to storage
  # CLI flag: -querier.extra-query-delay
  [extra_query_delay: <duration> | default = 0s]

  # Multi-tenant queries (requires auth_enabled: false)
  [multi_tenant_queries_enabled: <boolean> | default = false]

  # Engine configuration
  engine:
    [timeout: <duration> | default = 5m]
    [max_look_back_period: <duration> | default = 30s]
```

---

## Query Frontend Configuration

The `frontend` block configures the query frontend.

```yaml
frontend:
  # Maximum outstanding requests per tenant
  # CLI flag: -querier.max-outstanding-requests-per-tenant
  [max_outstanding_per_tenant: <int> | default = 2048]

  # Compress HTTP responses
  # CLI flag: -querier.compress-http-responses
  [compress_responses: <boolean> | default = true]

  # Response encoding: protobuf (recommended) or json
  [encoding: <string> | default = "protobuf"]

  # Log queries longer than this duration
  # CLI flag: -frontend.log-queries-longer-than
  [log_queries_longer_than: <duration> | default = 0s]

  # Downstream URL for query processing
  [downstream_url: <string>]
```

---

## Query Range Configuration

The `query_range` block configures query splitting and caching.

```yaml
query_range:
  # Align queries with step intervals
  # CLI flag: -querier.align-queries-with-step
  [align_queries_with_step: <boolean> | default = false]

  # Maximum retries for failed queries
  # CLI flag: -querier.max-retries
  [max_retries: <int> | default = 5]

  # Enable parallel execution of shardable queries
  # CLI flag: -querier.parallelise-shardable-queries
  [parallelise_shardable_queries: <boolean> | default = true]

  # Cache query results
  [cache_results: <boolean> | default = false]

  # Results cache configuration
  results_cache:
    cache:
      # Embedded cache
      embedded_cache:
        [enabled: <boolean> | default = false]
        [max_size_mb: <int> | default = 100]
        [ttl: <duration> | default = 1h]

      # Memcached client
      memcached_client:
        [host: <string>]
        [service: <string>]
        [timeout: <duration> | default = 500ms]
        [max_idle_conns: <int> | default = 16]
        [update_interval: <duration> | default = 1m]
        [consistent_hash: <boolean> | default = true]

      # Redis client
      redis:
        [endpoint: <string>]
        [timeout: <duration>]
        [expiration: <duration>]
```

---

## Compactor Configuration

The `compactor` block configures index compaction and retention.

```yaml
compactor:
  # Directory for compaction work
  # CLI flag: -boltdb.shipper.compactor.working-directory
  [working_directory: <string>]

  # How often to run compaction
  # CLI flag: -boltdb.shipper.compactor.compaction-interval
  [compaction_interval: <duration> | default = 10m]

  # Enable retention enforcement
  # CLI flag: -compactor.retention-enabled
  [retention_enabled: <boolean> | default = false]

  # Delay before deleting expired data
  # CLI flag: -compactor.retention-delete-delay
  [retention_delete_delay: <duration> | default = 2h]

  # Number of parallel deletion workers
  # CLI flag: -compactor.retention-delete-worker-count
  [retention_delete_worker_count: <int> | default = 150]

  # Delete request store backend (Loki 3.5+)
  # Options: boltdb, sqlite, s3, gcs, azure
  # SQLite recommended over BoltDB for better query optimization
  [delete_request_store: <string>]

  # Horizontally Scalable Compactor (Loki 3.6+)
  # Modes: disabled (default), main, worker
  [horizontal_scaling_mode: <string> | default = "disabled"]

  # Jobs configuration (for horizontal scaling)
  jobs_config:
    deletion:
      [deletion_manifest_store_prefix: <string> | default = "__deletion_manifest__/"]
      [timeout: <duration> | default = 15m]
      [max_retries: <int> | default = 3]
      [chunk_processing_concurrency: <int> | default = 3]

  # Worker configuration (for horizontal scaling worker mode)
  worker_config:
    [num_sub_workers: <int> | default = 0]  # 0 = use CPU core count
```

**Horizontal Compactor Modes (Loki 3.6+):**
- `disabled`: Traditional single compactor behavior
- `main`: Distributes deletion work to workers; requires disk access
- `worker`: Processes deletion jobs from main compactor via gRPC

---

## Limits Configuration

The `limits_config` block sets rate limits and resource constraints.

```yaml
limits_config:
  # --- Ingestion Limits ---

  # Maximum ingestion rate (MB/s) per tenant
  # CLI flag: -distributor.ingestion-rate-limit-mb
  [ingestion_rate_mb: <float> | default = 4]

  # Maximum burst size (MB) per tenant
  # CLI flag: -distributor.ingestion-burst-size-mb
  [ingestion_burst_size_mb: <float> | default = 6]

  # Maximum log line size
  # CLI flag: -distributor.max-line-size
  [max_line_size: <int> | default = 256KB]

  # Truncate oversized lines instead of rejecting
  # CLI flag: -distributor.max-line-size-truncate
  [max_line_size_truncate: <boolean> | default = false]

  # --- Stream Limits ---

  # Maximum streams per tenant
  # CLI flag: -ingester.max-streams-per-user
  [max_streams_per_user: <int> | default = 10000]

  # Maximum global streams per tenant (across all ingesters)
  # CLI flag: -ingester.max-global-streams-per-user
  [max_global_streams_per_user: <int> | default = 5000]

  # Maximum label name length
  # CLI flag: -validation.max-length-label-name
  [max_label_name_length: <int> | default = 1024]

  # Maximum label value length
  # CLI flag: -validation.max-length-label-value
  [max_label_value_length: <int> | default = 2048]

  # Maximum labels per stream (reduced to 15 in Loki 3.0)
  # CLI flag: -validation.max-label-names-per-series
  [max_label_names_per_series: <int> | default = 15]

  # --- Query Limits ---

  # Maximum entries returned per query
  # CLI flag: -querier.max-entries-limit-per-query
  [max_entries_limit_per_query: <int> | default = 5000]

  # Maximum query time range
  # CLI flag: -querier.max-query-length
  [max_query_length: <duration> | default = 721h]

  # Maximum parallel sub-queries
  # CLI flag: -querier.max-query-parallelism
  [max_query_parallelism: <int> | default = 32]

  # Maximum series per query
  [max_query_series: <int> | default = 500]

  # Maximum chunks per query
  [max_chunks_per_query: <int> | default = 2000000]

  # Query splitting interval (moved from query_range in 2.5.0)
  # CLI flag: -querier.split-queries-by-interval
  [split_queries_by_interval: <duration> | default = 30m]

  # --- Retention ---

  # Global retention period (requires compactor.retention_enabled)
  # CLI flag: -limits.retention-period
  [retention_period: <duration> | default = 0]

  # Per-stream retention (optional)
  retention_stream:
    - selector: '{namespace="prod"}'
      priority: 1
      period: 720h  # 30 days

  # --- Structured Metadata (Loki 2.9+) ---

  # Enable structured metadata
  # CLI flag: -validation.allow-structured-metadata
  [allow_structured_metadata: <boolean> | default = true]

  # Maximum size per log line
  # CLI flag: -limits.max-structured-metadata-size
  [max_structured_metadata_size: <int> | default = 64KB]

  # Maximum entries per log line
  # CLI flag: -limits.max-structured-metadata-entries-count
  [max_structured_metadata_entries_count: <int> | default = 128]

  # --- Volume API ---

  # Enable volume endpoints for Explore Logs / Grafana Drilldown
  [volume_enabled: <boolean> | default = true]

  # --- OTLP Configuration (Loki 3.0+) ---

  otlp_config:
    resource_attributes:
      # Override default resource attributes list
      [ignore_defaults: <boolean> | default = false]

      # Attribute configuration
      attributes_config:
        - action: index_label  # or structured_metadata, drop
          attributes:
            - service.name
            - service.namespace
        - action: structured_metadata
          attributes:
            - k8s.pod.name
            - service.instance.id
        - action: structured_metadata
          regex: "cloud.*"

    # Scope attributes configuration
    scope_attributes:
      - action: drop
        attributes:
          - otel.library.name

    # Log attributes configuration
    log_attributes:
      - action: structured_metadata
        attributes:
          - trace_id
          - span_id
      - action: drop
        regex: "internal.*"

    # Store severity_text as index label (NOT recommended)
    # CLI flag: -limits.otlp-config.severity-text-as-label
    [severity_text_as_label: <boolean> | default = false]

  # --- Time Sharding for Out-of-Order Ingestion (Loki 3.4+) ---

  shard_streams:
    [enabled: <boolean> | default = false]
    [time_sharding_enabled: <boolean> | default = false]

  # --- Enforced Labels (Experimental) ---

  # Labels that must be present in every stream
  # CLI flag: -validation.enforced-labels
  [enforced_labels: <list of strings> | default = []]

  # Policy-based enforced labels
  # The '*' policy applies to all streams
  policy_enforced_labels:
    finance:
      - cost_center
    ops:
      - team
    '*':
      - service.name

  # Policy to stream selector mapping
  policy_stream_mapping:
    finance:
      - selector: '{namespace="prod", container="billing"}'
        priority: 2
    ops:
      - selector: '{namespace="prod", container="ops"}'
        priority: 1

  # --- Block Ingestion ---

  # Block ingestion until date (RFC3339 format)
  # CLI flag: -limits.block-ingestion-until
  [block_ingestion_until: <time> | default = 0]

  # Block ingestion per policy until date
  [block_ingestion_policy_until: <map of string to Time>]

  # HTTP status code when blocked (260 default, 200 for silent)
  # CLI flag: -limits.block-ingestion-status-code
  [block_ingestion_status_code: <int> | default = 260]

  # --- Bloom Filters (Experimental, Loki 3.0+) ---

  [bloom_creation_enabled: <boolean> | default = false]
  [bloom_split_series_keyspace_by: <int> | default = 1024]
  [bloom_gateway_enable_filtering: <boolean> | default = false]
  [tsdb_sharding_strategy: <string>]  # Use "bounded" for blooms

  # --- Metric Aggregation ---

  # Enable metric aggregation for faster histogram queries
  # CLI flag: -limits.metric-aggregation-enabled
  [metric_aggregation_enabled: <boolean> | default = false]

  # --- Ruler Limits ---

  [ruler_max_rules_per_rule_group: <int> | default = 100]
  [ruler_max_rule_groups_per_tenant: <int> | default = 50]
```

---

## Ruler Configuration

The `ruler` block configures alerting and recording rules.

```yaml
ruler:
  # Rule evaluation interval
  # CLI flag: -ruler.evaluation-interval
  [evaluation_interval: <duration> | default = 1m]

  # Rule polling interval
  # CLI flag: -ruler.poll-interval
  [poll_interval: <duration> | default = 1m]

  # Storage configuration
  storage:
    # Storage type: local, s3, gcs, azure
    [type: <string>]

    local:
      [directory: <string> | default = "/rules"]

    s3:
      [bucket_name: <string>]
      [region: <string>]

    gcs:
      [bucket_name: <string>]

    azure:
      [container_name: <string>]
      [account_name: <string>]

  # Temporary rule file path
  [rule_path: <string> | default = "/rules"]

  # Alertmanager URL
  # CLI flag: -ruler.alertmanager-url
  [alertmanager_url: <string>]

  # Use Alertmanager API v2 (default since Loki 3.2.0)
  # CLI flag: -ruler.enable-alertmanager-v2
  [enable_alertmanager_v2: <boolean> | default = true]

  # Enable ruler API for rule management
  # CLI flag: -ruler.enable-api
  [enable_api: <boolean> | default = false]

  # Enable rule sharding across instances
  # CLI flag: -ruler.enable-sharding
  [enable_sharding: <boolean> | default = false]

  # Ring configuration for sharding
  ring:
    kvstore:
      [store: <string>]

  # Alert timing
  [for_outage_tolerance: <duration> | default = 1h]
  [for_grace_period: <duration> | default = 10m]
  [resend_delay: <duration> | default = 1m]

  # Remote write for recording rules
  remote_write:
    [enabled: <boolean> | default = false]
    client:
      [url: <string>]
      [remote_timeout: <duration> | default = 30s]

  # Alertmanager client configuration
  alertmanager_client:
    tls_config:
      [ca_path: <string>]
      [cert_path: <string>]
      [key_path: <string>]
    [basic_auth_username: <string>]
    [basic_auth_password: <string>]
```

**Rule File Structure:**
```
/rules/<tenant-id>/rules1.yaml
                   /rules2.yaml
```

---

## Pattern Ingester Configuration

The `pattern_ingester` block configures automatic log pattern detection (Loki 3.0+).

```yaml
pattern_ingester:
  # Enable pattern detection
  [enabled: <boolean> | default = false]

  # Metric aggregation configuration
  metric_aggregation:
    [enabled: <boolean> | default = false]
    [loki_address: <string>]
```

---

## Bloom Configuration

Bloom filters accelerate "needle in haystack" queries on structured metadata (Loki 3.0+).

> **Warning:** Experimental feature for deployments ingesting >75TB/month.

> **Breaking Change (Loki 3.3+):** Bloom filters use structured metadata only (not free-text). Delete existing bloom blocks before upgrading.

```yaml
# Bloom build configuration
bloom_build:
  [enabled: <boolean> | default = false]
  planner:
    [planning_interval: <duration> | default = 6h]
    [bloom_split_series_keyspace_by: <int> | default = 1024]
  builder:
    [planner_address: <string>]

# Bloom gateway configuration
bloom_gateway:
  [enabled: <boolean> | default = false]
  client:
    [addresses: <string>]
  [worker_concurrency: <int> | default = 4]
  [block_query_concurrency: <int> | default = 8]
  [max_query_page_size: <int> | default = 64MiB]

# Bloom shipper configuration
bloom_shipper:
  [working_directory: <string>]
```

---

## Memberlist Configuration

The `memberlist` block configures gossip-based cluster coordination.

```yaml
memberlist:
  # Addresses of other nodes to join
  join_members:
    - loki-memberlist

  # Port for gossip messages
  # CLI flag: -memberlist.bind-port
  [bind_port: <int> | default = 7946]

  # Address to advertise to other nodes
  [advertise_addr: <string>]

  # Port to advertise
  [advertise_port: <int>]

  # Timeout for establishing a stream connection
  [stream_timeout: <duration> | default = 2s]

  # Interval between gossip messages
  [gossip_interval: <duration> | default = 200ms]

  # Number of random nodes to gossip to
  [gossip_nodes: <int> | default = 3]
```

---

## Caching Configuration

### Chunk Cache

```yaml
chunk_store_config:
  chunk_cache_config:
    memcached:
      [batch_size: <int> | default = 256]
      [parallelism: <int> | default = 10]
    memcached_client:
      [host: <string>]
      [service: <string>]
      [timeout: <duration> | default = 500ms]
      [max_idle_conns: <int> | default = 100]
```

### Results Cache

```yaml
query_range:
  cache_results: true
  results_cache:
    cache:
      memcached_client:
        [host: <string>]
        [service: <string>]
        [timeout: <duration> | default = 500ms]
        [max_idle_conns: <int> | default = 100]
        [consistent_hash: <boolean> | default = true]
        [update_interval: <duration> | default = 1m]
```

**Note:** TSDB does NOT need index cache - only chunks and results cache.

---

## Additional Resources

- [Grafana Loki Configuration](https://grafana.com/docs/loki/latest/configure/)
- [Grafana Loki Best Practices](https://grafana.com/docs/loki/latest/configure/bp-configure/)
- [Loki HTTP API Reference](https://grafana.com/docs/loki/latest/reference/loki-http-api/)
- [Loki Helm Chart Values](https://grafana.com/docs/loki/latest/setup/install/helm/reference/)
