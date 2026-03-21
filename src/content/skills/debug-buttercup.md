---
title: "Debug Buttercup"
description: "Debugs the Buttercup CRS (Cyber Reasoning System) running on Kubernetes. Use when diagnosing pod crashes, restart loops, Redis failures, resource pressure, disk saturation, DinD issues, or any service misbehavior in the crs namespace. Covers triag..."
category: "devops"
source: "community"
author: "Community"
tags: ["debug", "buttercup"]
date: 2026-03-20
---

# Debug Buttercup

## When to Use

- Pods in the `crs` namespace are in CrashLoopBackOff, OOMKilled, or restarting
- Multiple services restart simultaneously (cascade failure)
- Redis is unresponsive or showing AOF warnings
- Queues are growing but tasks are not progressing
- Nodes show DiskPressure, MemoryPressure, or PID pressure
- Build-bot cannot reach the Docker daemon (DinD failures)
- Scheduler is stuck and not advancing task state
- Health check probes are failing unexpectedly
- Deployed Helm values don't match actual pod configuration

## When NOT to Use

- Deploying or upgrading Buttercup (use Helm and deployment guides)
- Debugging issues outside the `crs` Kubernetes namespace
- Performance tuning that doesn't involve a failure symptom

## Namespace and Services

All pods run in namespace `crs`. Key services:

| Layer | Services |
|-------|----------|
| Infra | redis, dind, litellm, registry-cache |
| Orchestration | scheduler, task-server, task-downloader, scratch-cleaner |
| Fuzzing | build-bot, fuzzer-bot, coverage-bot, tracer-bot, merger-bot |
| Analysis | patcher, seed-gen, program-model, pov-reproducer |
| Interface | competition-api, ui |

## Triage Workflow

Always start with triage. Run these three commands first:

```bash
# 1. Pod status - look for restarts, CrashLoopBackOff, OOMKilled
kubectl get pods -n crs -o wide

# 2. Events - the timeline of what went wrong
kubectl get events -n crs --sort-by='.lastTimestamp'

# 3. Warnings only - filter the noise
kubectl get events -n crs --field-selector type=Warning --sort-by='.lastTimestamp'
```

Then narrow down:

```bash
# Why did a specific pod restart? Check Last State Reason (OOMKilled, Error, Completed)
kubectl describe pod -n crs <pod-name> | grep -A8 'Last State:'

# Check actual resource limits vs intended
kubectl get pod -n crs <pod-name> -o jsonpath='{.spec.containers[0].resources}'

# Crashed container's logs (--previous = the container that died)
kubectl logs -n crs <pod-name> --previous --tail=200

# Current logs
kubectl logs -n crs <pod-name> --tail=200
```

### Historical vs Ongoing Issues

High restart counts don't necessarily mean an issue is ongoing -- restarts accumulate over a pod's lifetime. Always distinguish:
- `--tail` shows the end of the log buffer, which may contain old messages. Use `--since=300s` to confirm issues are actively happening now.
- `--timestamps` on log output helps correlate events across services.
- Check `Last State` timestamps in `describe pod` to see when the most recent crash actually occurred.

### Cascade Detection

When many pods restart around the same time, check for a shared-dependency failure before investigating individual pods. The most common cascade: Redis goes down -> every service gets `ConnectionError`/`ConnectionRefusedError` -> mass restarts. Look for the same error across multiple `--previous` logs -- if they all say `redis.exceptions.ConnectionError`, debug Redis, not the individual services.

## Log Analysis

```bash
# All replicas of a service at once
kubectl logs -n crs -l app=fuzzer-bot --tail=100 --prefix

# Stream live
kubectl logs -n crs -l app.kubernetes.io/name=redis -f

# Collect all logs to disk (existing script)
bash deployment/collect-logs.sh
```

## Resource Pressure

```bash
# Per-pod CPU/memory
kubectl top pods -n crs

# Node-level
kubectl top nodes

# Node conditions (disk pressure, memory pressure, PID pressure)
kubectl describe node <node> | grep -A5 Conditions

# Disk usage inside a pod
kubectl exec -n crs <pod> -- df -h

# What's eating disk
kubectl exec -n crs <pod> -- sh -c 'du -sh /corpus/* 2>/dev/null'
kubectl exec -n crs <pod> -- sh -c 'du -sh /scratch/* 2>/dev/null'
```

## Redis Debugging

Redis is the backbone. When it goes down, everything cascades.

```bash
# Redis pod status
kubectl get pods -n crs -l app.kubernetes.io/name=redis

# Redis logs (AOF warnings, OOM, connection issues)
kubectl logs -n crs -l app.kubernetes.io/name=redis --tail=200

# Connect to Redis CLI
kubectl exec -n crs <redis-pod> -- redis-cli

# Inside redis-cli: key diagnostics
INFO memory          # used_memory_human, maxmemory
INFO persistence     # aof_enabled, aof_last_bgrewrite_status, aof_delayed_fsync
INFO clients         # connected_clients, blocked_clients
INFO stats           # total_connections_received, rejected_connections
CLIENT LIST          # see who's connected
DBSIZE               # total keys

# AOF configuration
CONFIG GET appendonly     # is AOF enabled?
CONFIG GET appendfsync   # fsync policy: everysec, always, or no

# What is /data mounted on? (disk vs tmpfs matters for AOF performance)
```

```bash
kubectl exec -n crs <redis-pod> -- mount | grep /data
kubectl exec -n crs <redis-pod> -- du -sh /data/
```

### Queue Inspection

Buttercup uses Redis streams with consumer groups. Queue names:

| Queue | Stream Key |
|-------|-----------|
| Build | fuzzer_build_queue |
| Build Output | fuzzer_build_output_queue |
| Crash | fuzzer_crash_queue |
| Confirmed Vulns | confirmed_vulnerabilities_queue |
| Download Tasks | orchestrator_download_tasks_queue |
| Ready Tasks | tasks_ready_queue |
| Patches | patches_queue |
| Index | index_queue |
| Index Output | index_output_queue |
| Traced Vulns | traced_vulnerabilities_queue |
| POV Requests | pov_reproducer_requests_queue |
| POV Responses | pov_reproducer_responses_queue |
| Delete Task | orchestrator_delete_task_queue |

```bash
# Check stream length (pending messages)
kubectl exec -n crs <redis-pod> -- redis-cli XLEN fuzzer_build_queue

# Check consumer group lag
kubectl exec -n crs <redis-pod> -- redis-cli XINFO GROUPS fuzzer_build_queue

# Check pending messages per consumer
kubectl exec -n crs <redis-pod> -- redis-cli XPENDING fuzzer_build_queue build_bot_consumers - + 10

# Task registry size
kubectl exec -n crs <redis-pod> -- redis-cli HLEN tasks_registry

# Task state counts
kubectl exec -n crs <redis-pod> -- redis-cli SCARD cancelled_tasks
kubectl exec -n crs <redis-pod> -- redis-cli SCARD succeeded_tasks
kubectl exec -n crs <redis-pod> -- redis-cli SCARD errored_tasks
```

Consumer groups: `build_bot_consumers`, `orchestrator_group`, `patcher_group`, `index_group`, `tracer_bot_group`.

## Health Checks

Pods write timestamps to `/tmp/health_check_alive`. The liveness probe checks file freshness.

```bash
# Check health file freshness
kubectl exec -n crs <pod> -- stat /tmp/health_check_alive
kubectl exec -n crs <pod> -- cat /tmp/health_check_alive
```

If a pod is restart-looping, the health check file is likely going stale because the main process is blocked (e.g. waiting on Redis, stuck on I/O).

## Telemetry (OpenTelemetry / Signoz)

All services export traces and metrics via OpenTelemetry. If Signoz is deployed (`global.signoz.deployed: true`), use its UI for distributed tracing across services.

```bash
# Check if OTEL is configured
kubectl exec -n crs <pod> -- env | grep OTEL

# Verify Signoz pods are running (if deployed)
kubectl get pods -n platform -l app.kubernetes.io/name=signoz
```

Traces are especially useful for diagnosing slow task processing, identifying which service in a pipeline is the bottleneck, and correlating events across the scheduler -> build-bot -> fuzzer-bot chain.

## Volume and Storage

```bash
# PVC status
kubectl get pvc -n crs

# Check if corpus tmpfs is mounted, its size, and backing type
kubectl exec -n crs <pod> -- mount | grep corpus_tmpfs
kubectl exec -n crs <pod> -- df -h /corpus_tmpfs 2>/dev/null

# Check if CORPUS_TMPFS_PATH is set
kubectl exec -n crs <pod> -- env | grep CORPUS

# Full disk layout - what's on real disk vs tmpfs
kubectl exec -n crs <pod> -- df -h
```

`CORPUS_TMPFS_PATH` is set when `global.volumes.corpusTmpfs.enabled: true`. This affects fuzzer-bot, coverage-bot, seed-gen, and merger-bot.

### Deployment Config Verification

When behavior doesn't match expectations, verify Helm values actually took effect:

```bash
# Check a pod's actual resource limits
kubectl get pod -n crs <pod-name> -o jsonpath='{.spec.containers[0].resources}'

# Check a pod's actual volume definitions
kubectl get pod -n crs <pod-name> -o jsonpath='{.spec.volumes}'
```

Helm values template typos (e.g. wrong key names) silently fall back to chart defaults. If deployed resources don't match the values template, check for key name mismatches.

## Service-Specific Debugging

For detailed per-service symptoms, root causes, and fixes, see [references/failure-patterns.md](references/failure-patterns.md).

Quick reference:

- **DinD**: `kubectl logs -n crs -l app=dind --tail=100` -- look for docker daemon crashes, storage driver errors
- **Build-bot**: check build queue depth, DinD connectivity, OOM during compilation
- **Fuzzer-bot**: corpus disk usage, CPU throttling, crash queue backlog
- **Patcher**: LiteLLM connectivity, LLM timeout, patch queue depth
- **Scheduler**: the central brain -- `kubectl logs -n crs -l app=scheduler --tail=-1 --prefix | grep "WAIT_PATCH_PASS\|ERROR\|SUBMIT"`

## Diagnostic Script

Run the automated triage snapshot:

```bash
bash {baseDir}/scripts/diagnose.sh
```

Pass `--full` to also dump recent logs from all pods:

```bash
bash {baseDir}/scripts/diagnose.sh --full
```

This collects pod status, events, resource usage, Redis health, and queue depths in one pass.

---

## Reference: Failure Patterns

# Buttercup Failure Patterns

## Table of Contents

1. [Redis AOF Cascade](#redis-aof-cascade)
2. [Disk Saturation from Corpus Writes](#disk-saturation-from-corpus-writes)
3. [DinD Failures](#dind-failures)
4. [OOM Kills](#oom-kills)
5. [Queue Backlog Stalls](#queue-backlog-stalls)
6. [Health Check Staleness](#health-check-staleness)
7. [Init Container Stuck on Redis](#init-container-stuck-on-redis)

---

## Redis AOF Cascade

**Symptoms**: Multiple pods restart within minutes of each other. Redis logs show:
```
Asynchronous AOF fsync is taking too long (disk is busy?)
```
Services crash with `redis.exceptions.ConnectionError: Connection refused` or `Connection reset by peer`.

**Root cause**: Disk I/O contention blocks Redis `fsync()`. Even tiny AOF writes stall when the underlying disk is busy with other workloads (DinD, fuzzer corpus, etc.). Liveness probe fails. Redis restarts. All services lose connection and cascade-restart.

**Diagnosis**:
```bash
# Check AOF delayed fsync count and config
kubectl exec -n crs <redis-pod> -- redis-cli INFO persistence | grep aof_delayed_fsync
kubectl exec -n crs <redis-pod> -- redis-cli CONFIG GET appendonly
# Check what /data is mounted on - disk vs tmpfs
kubectl exec -n crs <redis-pod> -- mount | grep /data
# Confirm cascade: check if multiple pods crashed with the same Redis error
kubectl logs -n crs <other-pod> --previous --tail=20
```

**Fixes**:
- Use memory-backed volume for Redis: `redis.master.persistence.medium: "Memory"` - AOF writes go to tmpfs, immune to disk contention
- Reduce disk I/O from other sources (corpus tmpfs, DinD storage)
- Note: `persistence.enabled` controls PVC creation, not AOF. AOF is set in Redis server config separately

---

## Disk Saturation from Corpus Writes

**Symptoms**: Pods slow down or hang. `df -h` shows root filesystem nearly full. Node shows `DiskPressure` condition.

**Diagnosis**:
```bash
kubectl describe node <node> | grep DiskPressure
kubectl exec -n crs <fuzzer-pod> -- du -sh /corpus/*
kubectl exec -n crs <fuzzer-pod> -- df -h
```

**Fixes**:
- Enable corpus tmpfs (moves corpus to `/dev/shm`)
- Reduce fuzzer-bot replicas
- Enable scratch-cleaner with shorter retention (`scratchRetentionSeconds`)
- Increase node disk size

---

## DinD Failures

**Symptoms**: Build-bot jobs fail with `Cannot connect to the Docker daemon`. DinD pod restarting or in CrashLoopBackOff.

**Diagnosis**:
```bash
kubectl logs -n crs -l app=dind --tail=100
kubectl describe pod -n crs <dind-pod>
kubectl exec -n crs <dind-pod> -- docker info
```

**Common causes**:
- Storage driver errors (overlay2 on incompatible filesystem)
- DinD running out of disk space (images accumulating)
- Resource limits too low (DinD needs significant CPU/memory for builds)

**Fixes**:
- Increase DinD resource limits (8000m CPU, 16Gi memory for large deployments)
- Prune images periodically: `docker system prune -af`
- Check storage driver compatibility

---

## OOM Kills

**Symptoms**: Pod status shows `OOMKilled`. Describe shows `Last State: Terminated, Reason: OOMKilled`.

**Diagnosis**:
```bash
kubectl describe pod -n crs <pod> | grep -A3 "Last State"
kubectl get events -n crs | grep OOM
kubectl top pods -n crs --sort-by=memory
```

**Common causes**:
- coverage-bot: needs 8Gi+ for large targets
- dind: building large projects

**Fixes**: Increase memory limits in values template for the affected service.

---

## Queue Backlog Stalls

**Symptoms**: Tasks not progressing. Scheduler logs show state stuck (e.g. never reaching `SUBMIT_BUNDLE`). Queue depths growing.

**Diagnosis**:
```bash
# Check all queue depths
for q in fuzzer_build_queue fuzzer_build_output_queue fuzzer_crash_queue \
         confirmed_vulnerabilities_queue orchestrator_download_tasks_queue \
         orchestrator_delete_task_queue tasks_ready_queue patches_queue \
         index_queue index_output_queue traced_vulnerabilities_queue \
         pov_reproducer_requests_queue pov_reproducer_responses_queue; do
  echo "$q: $(kubectl exec -n crs <redis-pod> -- redis-cli XLEN $q)"
done

# Check for stuck consumers
kubectl exec -n crs <redis-pod> -- redis-cli XINFO GROUPS fuzzer_build_queue
```

**Common causes**:
- Consumer pod crashed and didn't ack messages - messages stuck in PEL (pending entries list)
- Downstream service down (e.g. build-bot down -> build queue grows)
- Task timeout too short (`BUILD_TASK_TIMEOUT_MS` default 15min)

**Fixes**:
- Restart the stuck consumer pods
- Claim and ack orphaned pending messages
- Increase task timeouts if builds are legitimately slow

---

## Health Check Staleness

**Symptoms**: Pod keeps restarting despite logs showing it was working. Describe shows `Liveness probe failed`.

**Root cause**: The main process is alive but blocked (e.g. waiting on Redis, slow I/O), so it doesn't update `/tmp/health_check_alive`. After 600s stale + probe timing, Kubernetes kills it.

**Diagnosis**:
```bash
kubectl describe pod -n crs <pod> | grep -A5 "Liveness"
kubectl logs -n crs <pod> --previous --tail=50
```

**Fixes**:
- Fix the underlying block (Redis connection, disk I/O)
- Increase `livenessProbe.periodSeconds` or `failureThreshold`

---

## Init Container Stuck on Redis

**Symptoms**: Pod stuck in `Init:0/1`. Events show init container running but never completing.

**Root cause**: The `wait-for-redis` init container polls `redis-master:6379`. If Redis is down, all pods queue up waiting.

**Diagnosis**:
```bash
kubectl describe pod -n crs <pod> | grep -A10 "Init Containers"
kubectl get pods -n crs -l app.kubernetes.io/name=redis
```

**Fix**: Fix Redis first. Everything else will unblock automatically.
