---
title: "K8s Debug"
description: "Diagnose and fix Kubernetes pods, CrashLoopBackOff, Pending, DNS, networking, storage, and rollout failures with kubectl."
category: "devops"
source: "community"
author: "Community"
tags: ["k8s", "debug"]
date: 2026-03-20
---

# Kubernetes Debugging Skill

## Overview

Systematic toolkit for debugging Kubernetes clusters, workloads, networking, and storage with a deterministic, safety-first workflow.

## Trigger Phrases

Use this skill when requests resemble:
- "My pod is in `CrashLoopBackOff`; help me find the root cause."
- "Service DNS works in one pod but not another."
- "Deployment rollout is stuck."
- "Pods are `Pending` and not scheduling."
- "Cluster health looks degraded after a change."
- "PVC is pending and pods cannot mount storage."

## Prerequisites

Run from the skill directory (`devops-skills-plugin/skills/k8s-debug`) so relative script paths work as written.

### Required
- `kubectl` installed and configured.
- An active cluster context.
- Read access to namespaces, pods, events, services, and nodes.

Quick preflight:

```bash
kubectl config current-context
kubectl auth can-i get pods -A
kubectl auth can-i get events -A
kubectl get ns
```

### Optional but Recommended
- `jq` for more precise filtering in `./scripts/cluster_health.sh`.
- Metrics API (`metrics-server`) for `kubectl top`.
- In-container debug tools (`nslookup`, `getent`, `curl`, `wget`, `ip`) for deep network tests.

Fallback behavior:
- If optional tools are missing, scripts continue and print warnings with reduced output.
- If `kubectl top` is unavailable, continue with `kubectl describe` and events.

## When to Use This Skill

Use this skill for:
- Pod failures (CrashLoopBackOff, ImagePullBackOff, Pending, OOMKilled)
- Service connectivity or DNS resolution issues
- Network policy or ingress problems
- Volume and storage mount failures
- Deployment rollout issues
- Cluster health or performance degradation
- Resource exhaustion (CPU/memory)
- Configuration problems (ConfigMaps, Secrets, RBAC)

## Safety Rules for Disruptive Commands

Default mode is read-only diagnosis first. Only execute disruptive commands after confirming blast radius and rollback.

Commands requiring explicit confirmation:
- `kubectl delete pod ... --force --grace-period=0`
- `kubectl drain ...`
- `kubectl rollout restart ...`
- `kubectl rollout undo ...`
- `kubectl debug ... --copy-to=...`

Before disruptive actions:
```bash
# Snapshot current state for rollback and incident notes
kubectl get deploy,rs,pod,svc -n <namespace> -o wide
kubectl get pod <pod-name> -n <namespace> -o yaml > before-<pod-name>.yaml
kubectl get events -n <namespace> --sort-by='.lastTimestamp' > before-events.txt
```

## Reference Navigation Map

Load only the section needed for the observed symptom.

| Symptom / Need | Open | Start section |
| --- | --- | --- |
| You need an end-to-end diagnosis path | `./references/troubleshooting_workflow.md` | `General Debugging Workflow` |
| Pod state is `Pending`, `CrashLoopBackOff`, or `ImagePullBackOff` | `./references/troubleshooting_workflow.md` | `Pod Lifecycle Troubleshooting` |
| Service reachability or DNS failure | `./references/troubleshooting_workflow.md` | `Network Troubleshooting Workflow` |
| Node pressure or performance regression | `./references/troubleshooting_workflow.md` | `Resource and Performance Workflow` |
| PVC / PV / storage class issues | `./references/troubleshooting_workflow.md` | `Storage Troubleshooting Workflow` |
| Quick symptom-to-fix lookup | `./references/common_issues.md` | matching issue heading |
| Post-mortem fix options for known issues | `./references/common_issues.md` | `Solutions` sections |

## Scripts Overview

| Script | Purpose | Required args | Optional args | Output | Fallback behavior |
| --- | --- | --- | --- | --- | --- |
| `./scripts/cluster_health.sh` | Cluster-wide health snapshot (nodes, workloads, events, common failure states) | None | `--strict`, `K8S_REQUEST_TIMEOUT` env var | Sectioned report to stdout | Continues on check failures, tracks them in summary and exit code |
| `./scripts/network_debug.sh` | Pod-centric network and DNS diagnostics | `<pod-name>` (`<namespace>` defaults to `default`) | `--strict`, `--insecure`, `K8S_REQUEST_TIMEOUT` env var | Sectioned report to stdout | Uses secure API probe by default; insecure TLS requires explicit `--insecure` |
| `./scripts/pod_diagnostics.py` | Deep pod diagnostics (status, describe, YAML, events, per-container logs, node context) | `<pod-name>` | `-n/--namespace`, `-o/--output` | Sectioned report to stdout or file | Fails fast on missing access; skips optional metrics/log blocks with clear messages |

### Script Exit Codes

`./scripts/cluster_health.sh` and `./scripts/network_debug.sh` share the same contract:

- `0`: checks completed with no check failures (warnings allowed unless `--strict` is set).
- `1`: one or more checks failed, or warnings occurred in `--strict` mode.
- `2`: blocked preconditions (for example: missing `kubectl`, no active context, inaccessible namespace/pod).

## Deterministic Debugging Workflow

Follow this systematic approach for any Kubernetes issue:

### 1. Preflight and Scope

```bash
kubectl config current-context
kubectl get ns
kubectl auth can-i get pods -n <namespace>
```

If preflight fails, stop and fix access/context first.

### 2. Identify the Problem Layer

Categorize the issue:
- **Application Layer**: Application crashes, errors, bugs
- **Pod Layer**: Pod not starting, restarting, or pending
- **Service Layer**: Network connectivity, DNS issues
- **Node Layer**: Node not ready, resource exhaustion
- **Cluster Layer**: Control plane issues, API problems
- **Storage Layer**: Volume mount failures, PVC issues
- **Configuration Layer**: ConfigMap, Secret, RBAC issues

### 3. Gather Diagnostics with the Right Script

Use the appropriate diagnostic script based on scope:

#### Pod-Level Diagnostics
Use `./scripts/pod_diagnostics.py` for comprehensive pod analysis:

```bash
python3 ./scripts/pod_diagnostics.py <pod-name> -n <namespace>
```

This script gathers:
- Pod status and description
- Pod events
- Container logs (current and previous)
- Resource usage
- Node information
- YAML configuration

Output can be saved for analysis:

```bash
python3 ./scripts/pod_diagnostics.py <pod-name> -n <namespace> -o diagnostics.txt
```

#### Cluster-Level Health Check
Use `./scripts/cluster_health.sh` for overall cluster diagnostics:

```bash
./scripts/cluster_health.sh > cluster-health-$(date +%Y%m%d-%H%M%S).txt
```

This script checks:
- Cluster info and version
- Node status and resources
- Pods across all namespaces
- Failed/pending pods
- Recent events
- Deployments, services, statefulsets, daemonsets
- PVCs and PVs
- Component health
- Common error states (CrashLoopBackOff, ImagePullBackOff)

#### Network Diagnostics
Use `./scripts/network_debug.sh` for connectivity issues:

```bash
./scripts/network_debug.sh <namespace> <pod-name>
# or force warning sensitivity / insecure TLS only when explicitly needed:
./scripts/network_debug.sh --strict <namespace> <pod-name>
./scripts/network_debug.sh --insecure <namespace> <pod-name>
```

This script analyzes:
- Pod network configuration
- DNS setup and resolution
- Service endpoints
- Network policies
- Connectivity tests
- CoreDNS logs

### 4. Follow Issue-Specific Reference Workflow

Based on the identified issue, consult `./references/troubleshooting_workflow.md`:

- **Pod Pending**: Resource/scheduling workflow
- **CrashLoopBackOff**: Application crash workflow
- **ImagePullBackOff**: Image pull workflow
- **Service issues**: Network connectivity workflow
- **DNS failures**: DNS troubleshooting workflow
- **Resource exhaustion**: Performance investigation workflow
- **Storage issues**: PVC binding workflow
- **Deployment stuck**: Rollout workflow

### 5. Apply Targeted Fixes

Refer to `./references/common_issues.md` for symptom-specific fixes.

### 6. Verify and Close

Run final verification:

```bash
kubectl get pods -n <namespace> -o wide
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20
kubectl rollout status deployment/<name> -n <namespace>
```

Issue is done when user-visible behavior is healthy and no new critical warning events appear.

## Example Flows

### Example 1: CrashLoopBackOff in `payments` Namespace

```bash
python3 ./scripts/pod_diagnostics.py payments-api-7c97f95dfb-q9l7k -n payments -o payments-diagnostics.txt
kubectl logs payments-api-7c97f95dfb-q9l7k -n payments --previous --tail=100
kubectl get deploy payments-api -n payments -o yaml | grep -A 8 livenessProbe
```

Then open `./references/common_issues.md` and apply the `CrashLoopBackOff` solutions.

### Example 2: Service DNS/Connectivity Failure

```bash
./scripts/network_debug.sh checkout checkout-api-75f49c9d8f-z6qtm
kubectl get svc checkout-api -n checkout
kubectl get endpoints checkout-api -n checkout
kubectl get networkpolicies -n checkout
```

Then follow `Service Connectivity Workflow` in `./references/troubleshooting_workflow.md`.

## Essential Manual Commands

### Pod Debugging

```bash
# View pod status
kubectl get pods -n <namespace> -o wide

# Detailed pod information
kubectl describe pod <pod-name> -n <namespace>

# View logs
kubectl logs <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --previous  # Previous container
kubectl logs <pod-name> -n <namespace> -c <container>  # Specific container

# Execute commands in pod
kubectl exec <pod-name> -n <namespace> -it -- /bin/sh

# Get pod YAML
kubectl get pod <pod-name> -n <namespace> -o yaml
```

### Service and Network Debugging

```bash
# Check services
kubectl get svc -n <namespace>
kubectl describe svc <service-name> -n <namespace>

# Check endpoints
kubectl get endpoints -n <namespace>

# Test DNS
kubectl exec <pod-name> -n <namespace> -- nslookup kubernetes.default

# View events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

### Resource Monitoring

```bash
# Node resources
kubectl top nodes
kubectl describe nodes

# Pod resources
kubectl top pods -n <namespace>
kubectl top pod <pod-name> -n <namespace> --containers
```

### Emergency Operations

```bash
# Restart deployment
kubectl rollout restart deployment/<name> -n <namespace>

# Rollback deployment
kubectl rollout undo deployment/<name> -n <namespace>

# Force delete stuck pod
kubectl delete pod <pod-name> -n <namespace> --force --grace-period=0

# Drain node (maintenance)
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Cordon node (prevent scheduling)
kubectl cordon <node-name>
```

## Completion Criteria

Troubleshooting session is complete when all are true:
- [ ] Cluster context and namespace are confirmed.
- [ ] Relevant diagnostic script output is captured.
- [ ] Root cause is identified and tied to evidence (events/logs/config/state).
- [ ] Any disruptive action was preceded by snapshot and rollback plan.
- [ ] Fix verification commands show healthy state.
- [ ] Reference path used (`./references/troubleshooting_workflow.md` or `./references/common_issues.md`) is documented in notes.

## Related Tools

Useful additional tools for Kubernetes debugging:
- **kubectl-debug**: Advanced debugging plugin
- **stern**: Multi-pod log tailing
- **kubectx/kubens**: Context and namespace switching
- **k9s**: Terminal UI for Kubernetes
- **lens**: Desktop IDE for Kubernetes
- **Prometheus/Grafana**: Monitoring and alerting
- **Jaeger/Zipkin**: Distributed tracing

---

## Reference: Common_Issues

# Common Kubernetes Issues and Troubleshooting

## How to Use This Reference

Use this file as a symptom-to-fix lookup after collecting diagnostics.

Suggested sequence:
1. Match the observed symptom with the closest issue heading.
2. Run the listed `Debugging Steps` commands and confirm you can reproduce the failure.
3. Apply the least disruptive fix from `Solutions`.
4. Re-run verification commands and confirm the symptom is gone.

If you need an end-to-end decision flow instead of a known symptom lookup, use `./references/troubleshooting_workflow.md`.

## Pod Issues

### CrashLoopBackOff

**Symptoms:**
- Pod repeatedly crashes and restarts
- Status shows `CrashLoopBackOff`
- Increasing restart count

**Common Causes:**
1. Application error causing immediate exit
2. Missing environment variables or configuration
3. Insufficient resources (memory/CPU)
4. Failed health checks (liveness probe)
5. Missing dependencies or volumes

**Debugging Steps:**
```bash
# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# View current logs
kubectl logs <pod-name> -n <namespace>

# View previous container logs (from crashed container)
kubectl logs <pod-name> -n <namespace> --previous

# Check resource limits
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 resources

# Check liveness/readiness probes
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 livenessProbe
```

**Solutions:**
- Fix application code causing crashes
- Add missing environment variables via ConfigMap/Secret
- Increase resource limits
- Adjust or remove overly aggressive liveness probes
- Ensure all required volumes are mounted and accessible

---

### ImagePullBackOff / ErrImagePull

**Symptoms:**
- Pod status shows `ImagePullBackOff` or `ErrImagePull`
- Pod fails to start
- Events show image pull errors

**Common Causes:**
1. Image doesn't exist or wrong image name/tag
2. Private registry requires authentication
3. Network issues accessing registry
4. Image pull secrets missing or incorrect
5. Registry rate limiting

**Debugging Steps:**
```bash
# Check exact error message
kubectl describe pod <pod-name> -n <namespace>

# Verify image name and tag
kubectl get pod <pod-name> -n <namespace> -o yaml | grep image:

# Check image pull secrets
kubectl get pod <pod-name> -n <namespace> -o yaml | grep imagePullSecrets -A 2

# List secrets in namespace
kubectl get secrets -n <namespace>

# Test image pull manually on node
docker pull <image-name>
```

**Solutions:**
- Verify image exists in registry: `docker pull <image>`
- Create image pull secret: `kubectl create secret docker-registry <secret-name> --docker-server=<registry> --docker-username=<user> --docker-password=<pass>`
- Add imagePullSecrets to pod spec
- Use correct image tag (avoid `latest` in production)
- Check registry credentials and permissions

---

### Pending Pods

**Symptoms:**
- Pod stuck in `Pending` state
- Pod never gets scheduled

**Common Causes:**
1. Insufficient cluster resources (CPU/memory)
2. No nodes match pod's node selector
3. Taints on nodes prevent scheduling
4. PersistentVolumeClaim not bound
5. Pod affinity/anti-affinity rules cannot be satisfied

**Debugging Steps:**
```bash
# Check scheduling events
kubectl describe pod <pod-name> -n <namespace>

# Check node resources
kubectl top nodes
kubectl describe nodes

# Check PVC status
kubectl get pvc -n <namespace>

# Check node selectors and taints
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 nodeSelector
kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
```

**Solutions:**
- Add more nodes to cluster or free up resources
- Remove/adjust node selectors
- Add tolerations for taints
- Create or fix PersistentVolume for PVC
- Adjust affinity/anti-affinity rules
- Check resource quotas: `kubectl get resourcequota -n <namespace>`

---

### OOMKilled (Out of Memory)

**Symptoms:**
- Pod restarts with exit code 137
- Last state shows `OOMKilled`
- Container was killed due to memory

**Debugging Steps:**
```bash
# Check pod status and last state
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 lastState

# Check memory limits
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 resources

# Check actual memory usage
kubectl top pod <pod-name> -n <namespace> --containers
```

**Solutions:**
- Increase memory limits
- Fix memory leaks in application
- Optimize application memory usage
- Add memory requests/limits if missing

---

## Service and Networking Issues

### Service Not Accessible

**Symptoms:**
- Cannot connect to service from within or outside cluster
- Connection timeout or refused

**Common Causes:**
1. Service selector doesn't match pod labels
2. Target port mismatch
3. Network policies blocking traffic
4. Service type incorrect (ClusterIP vs LoadBalancer)
5. Endpoints not created

**Debugging Steps:**
```bash
# Check service configuration
kubectl get svc <service-name> -n <namespace> -o yaml

# Check endpoints
kubectl get endpoints <service-name> -n <namespace>

# Check pod labels
kubectl get pods -n <namespace> --show-labels

# Test from another pod
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- /bin/bash
# Inside pod: curl <service-name>.<namespace>.svc.cluster.local

# Check network policies
kubectl get networkpolicies -n <namespace>
```

**Solutions:**
- Ensure service selector matches pod labels exactly
- Verify port and targetPort are correct
- Check network policies allow traffic
- Use correct service type for use case
- Ensure pods are running and ready

---

### DNS Resolution Failures

**Symptoms:**
- Pods cannot resolve service names
- `nslookup` or `dig` commands fail
- DNS timeouts

**Common Causes:**
1. CoreDNS not running properly
2. DNS service not accessible
3. Pod DNS config incorrect
4. Network policies blocking DNS

**Debugging Steps:**
```bash
# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Check CoreDNS logs
kubectl logs -n kube-system -l k8s-app=kube-dns

# Test DNS from pod
kubectl exec <pod-name> -n <namespace> -- nslookup kubernetes.default

# Check pod DNS config
kubectl exec <pod-name> -n <namespace> -- cat /etc/resolv.conf

# Check DNS service
kubectl get svc -n kube-system kube-dns
```

**Solutions:**
- Restart CoreDNS: `kubectl rollout restart deployment/coredns -n kube-system`
- Verify DNS service endpoints exist
- Check network policies allow port 53
- Verify kubelet DNS settings

---

## Volume and Storage Issues

### PersistentVolumeClaim Pending

**Symptoms:**
- PVC stuck in `Pending` state
- Pod cannot start due to volume mount

**Debugging Steps:**
```bash
# Check PVC status
kubectl describe pvc <pvc-name> -n <namespace>

# List available PVs
kubectl get pv

# Check storage class
kubectl get storageclass
```

**Solutions:**
- Create matching PersistentVolume
- Verify storage class exists and is correct
- Check volume provisioner is working
- Ensure sufficient storage available

---

## Resource and Configuration Issues

### ConfigMap/Secret Not Found

**Symptoms:**
- Pod fails to start
- Events show volume mount errors
- Missing environment variables

**Debugging Steps:**
```bash
# List ConfigMaps
kubectl get configmaps -n <namespace>

# List Secrets
kubectl get secrets -n <namespace>

# Check pod configuration
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 10 env
```

**Solutions:**
- Create missing ConfigMap/Secret
- Verify names match exactly (case-sensitive)
- Check namespace matches
- Ensure keys referenced exist in ConfigMap/Secret

---

## Performance Issues

### High CPU/Memory Usage

**Debugging Steps:**
```bash
# Check resource usage
kubectl top nodes
kubectl top pods -n <namespace>

# Check resource requests/limits
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 Limits

# Get detailed metrics
kubectl get --raw /apis/metrics.k8s.io/v1beta1/namespaces/<namespace>/pods/<pod-name>
```

**Solutions:**
- Optimize application code
- Adjust resource requests/limits
- Scale horizontally with more replicas
- Implement caching or performance improvements

---

## Deployment Issues

### Deployment Stuck/Not Rolling Out

**Symptoms:**
- New version not deployed
- Old pods still running
- Rollout stuck

**Debugging Steps:**
```bash
# Check rollout status
kubectl rollout status deployment/<deployment-name> -n <namespace>

# Check rollout history
kubectl rollout history deployment/<deployment-name> -n <namespace>

# Check replica sets
kubectl get rs -n <namespace>

# Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

**Solutions:**
- Check if new pods are failing (CrashLoopBackOff, ImagePullBackOff)
- Verify readiness probes are passing
- Check deployment strategy settings
- Rollback if needed: `kubectl rollout undo deployment/<deployment-name> -n <namespace>`

---

## Issue Resolution Done Criteria

Mark troubleshooting complete only when all are true:
- [ ] Symptom was matched to one issue section in this file.
- [ ] At least one command from `Debugging Steps` produced evidence for the diagnosis.
- [ ] Fix was applied and verified with follow-up `kubectl get/describe/logs` checks.
- [ ] No new critical warning events appeared after the fix window.
- [ ] Any disruptive command used (restart/rollback/force delete) was justified in notes.

---

## Reference: Troubleshooting_Workflow

# Kubernetes Troubleshooting Workflows

## How to Use This Reference

Use this file for deterministic, step-by-step diagnosis once you know the rough symptom category.

Routing guide:

| Symptom | Jump to |
| --- | --- |
| Pod is not scheduling | `Pod Pending Workflow` |
| Pod repeatedly restarts | `Pod CrashLoopBackOff Workflow` |
| Image pull fails | `Pod ImagePullBackOff Workflow` |
| Service or DNS is failing | `Network Troubleshooting Workflow` |
| Node or pod resource pressure | `Resource and Performance Workflow` |
| PVC/PV/storage class issue | `Storage Troubleshooting Workflow` |
| Rollout is blocked | `Deployment and Rollout Workflow` |

Safety note:
- Treat `kubectl delete ... --force`, `kubectl drain`, `kubectl rollout restart`, and `kubectl rollout undo` as disruptive commands.
- Capture current state before running disruptive operations.

## General Debugging Workflow

When facing any Kubernetes issue, follow this systematic approach:

### 1. Identify the Problem Layer

Kubernetes issues typically fall into these categories:

```
Application Layer     → Application crashes, errors, bugs
Pod Layer            → Pod not starting, restarting, pending
Service Layer        → Network connectivity, DNS issues
Node Layer           → Node not ready, resource exhaustion
Cluster Layer        → Control plane issues, API problems
Storage Layer        → Volume mount failures, PVC issues
Configuration Layer  → ConfigMap, Secret, RBAC issues
```

### 2. Gather Initial Information

```bash
# What's the current state?
kubectl get pods -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Quick status check
kubectl describe pod <pod-name> -n <namespace>
```

### 3. Drill Down Based on State

Follow the appropriate workflow based on pod state:

- **Pending** → Resource/Scheduling Workflow
- **ImagePullBackOff** → Image Pull Workflow
- **CrashLoopBackOff** → Application Crash Workflow
- **Running but not working** → Service/Network Workflow
- **Error/Unknown** → Node/Cluster Workflow

---

## Pod Lifecycle Troubleshooting

### Pod Pending Workflow

```
1. kubectl describe pod → Check events section
   ↓
2. Check scheduling issues:
   - Insufficient resources? → kubectl top nodes
   - Node selector issues? → Check nodeSelector in pod spec
   - Taints/tolerations? → kubectl get nodes -o custom-columns=NAME:.metadata.name,TAINTS:.spec.taints
   - PVC pending? → kubectl get pvc -n <namespace>
   ↓
3. Take action:
   - Add nodes or free resources
   - Adjust node selector
   - Add tolerations
   - Fix PVC/PV binding
```

### Pod CrashLoopBackOff Workflow

```
1. kubectl logs <pod> --previous
   ↓
2. Analyze crash reason:
   - Application error? → Fix code/config
   - Missing dependencies? → Check env vars, volumes, secrets
   - Resource limits? → kubectl describe pod → Check OOMKilled
   - Failed health checks? → Check liveness/readiness probe settings
   ↓
3. Common checks:
   kubectl get pod <pod> -o yaml | grep -A 10 env
   kubectl get pod <pod> -o yaml | grep -A 10 volumeMounts
   kubectl get pod <pod> -o yaml | grep -A 10 livenessProbe
   ↓
4. Fix and verify:
   - Update deployment/pod spec
   - kubectl apply -f updated-config.yaml
   - Watch: kubectl get pods -w
```

### Pod ImagePullBackOff Workflow

```
1. kubectl describe pod → Find exact error
   ↓
2. Verify image:
   - Does image exist? → docker pull <image> (test locally)
   - Correct tag? → Check deployment spec
   - Private registry? → Check imagePullSecrets
   ↓
3. Fix authentication (if needed):
   kubectl create secret docker-registry <secret> \
     --docker-server=<server> \
     --docker-username=<user> \
     --docker-password=<pass>
   ↓
4. Update pod spec with imagePullSecrets
   ↓
5. Verify:
   kubectl get pods -w
```

---

## Network Troubleshooting Workflow

### Service Connectivity Workflow

```
1. Verify service exists:
   kubectl get svc <service-name> -n <namespace>
   ↓
2. Check endpoints:
   kubectl get endpoints <service-name> -n <namespace>
   ↓
   No endpoints? → Check selector matches pod labels
   ↓
3. Test DNS resolution:
   kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- /bin/bash
   nslookup <service-name>.<namespace>.svc.cluster.local
   ↓
   DNS fails? → Check CoreDNS pods and logs
   ↓
4. Test connectivity:
   curl <service-name>.<namespace>.svc.cluster.local:<port>
   ↓
   Connection fails? → Check:
   - Network policies: kubectl get networkpolicies -n <namespace>
   - Target port matches pod port
   - Pod is ready: kubectl get pods -n <namespace>
   ↓
5. Check from outside cluster (if applicable):
   - LoadBalancer service? → Check external IP assigned
   - Ingress? → kubectl get ingress -n <namespace>
   - NodePort? → Access via <node-ip>:<nodePort>
```

### DNS Issues Workflow

```
1. Test DNS from problem pod:
   kubectl exec <pod> -n <namespace> -- nslookup kubernetes.default
   ↓
2. Check CoreDNS health:
   kubectl get pods -n kube-system -l k8s-app=kube-dns
   kubectl logs -n kube-system -l k8s-app=kube-dns
   ↓
3. Verify DNS service:
   kubectl get svc -n kube-system kube-dns
   kubectl get endpoints -n kube-system kube-dns
   ↓
4. Check pod DNS config:
   kubectl exec <pod> -n <namespace> -- cat /etc/resolv.conf
   ↓
5. Fix if needed:
   - Restart CoreDNS: kubectl rollout restart -n kube-system deployment/coredns
   - Check network policies allow DNS (port 53)
   - Verify kubelet configuration
```

---

## Resource and Performance Workflow

### High Resource Usage Investigation

```
1. Identify resource hog:
   kubectl top nodes
   kubectl top pods --all-namespaces
   ↓
2. Check specific pod:
   kubectl top pod <pod-name> -n <namespace> --containers
   kubectl describe pod <pod-name> -n <namespace> | grep -A 10 "Limits"
   ↓
3. Analyze application:
   - Memory leak? → Check logs for errors
   - CPU spike? → Profile application
   - Check resource requests/limits appropriate?
   ↓
4. Take action:
   - Increase limits if legitimate usage
   - Fix application if bug/leak
   - Implement HPA if scaling needed
   - Add resource quotas to prevent overconsumption
```

### Node Resource Exhaustion Workflow

```
1. Check node status:
   kubectl get nodes
   kubectl describe node <node-name>
   ↓
2. Look for pressure conditions:
   - MemoryPressure
   - DiskPressure
   - PIDPressure
   ↓
3. Check node resources:
   kubectl top node <node-name>
   ↓
4. Find resource consumers:
   kubectl describe node <node-name> | grep -A 20 "Allocated resources"
   ↓
5. Actions:
   - Evict non-critical pods
   - Add more nodes
   - Adjust resource requests/limits
   - Clean up disk space if DiskPressure
```

---

## Storage Troubleshooting Workflow

### PVC Binding Issues Workflow

```
1. Check PVC status:
   kubectl get pvc -n <namespace>
   kubectl describe pvc <pvc-name> -n <namespace>
   ↓
2. Check for matching PV:
   kubectl get pv
   ↓
   No matching PV? → Check:
   - Storage class exists: kubectl get storageclass
   - Dynamic provisioner working
   - Manual PV needed?
   ↓
3. Verify storage class:
   kubectl describe storageclass <class-name>
   ↓
4. Check provisioner logs (if dynamic):
   kubectl logs -n kube-system <provisioner-pod>
   ↓
5. Fix:
   - Create matching PV (static)
   - Fix storage class configuration (dynamic)
   - Verify provisioner is running
```

---

## Deployment and Rollout Workflow

### Stuck Deployment Workflow

```
1. Check rollout status:
   kubectl rollout status deployment/<name> -n <namespace>
   ↓
2. Check replica sets:
   kubectl get rs -n <namespace>
   kubectl describe rs <new-replicaset> -n <namespace>
   ↓
3. Check new pod status:
   kubectl get pods -n <namespace> -l app=<app-label>
   ↓
   Pods failing? → Follow pod troubleshooting workflow
   ↓
4. Check rollout strategy:
   kubectl get deployment <name> -n <namespace> -o yaml | grep -A 10 strategy
   ↓
5. Options:
   - Fix pod issues and rollout will continue
   - Pause rollout: kubectl rollout pause deployment/<name>
   - Rollback: kubectl rollout undo deployment/<name>
   - Check revision history: kubectl rollout history deployment/<name>
```

---

## Quick Reference Commands

### Essential Debug Commands

```bash
# Pod debugging
kubectl get pods -n <namespace> -o wide
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> [-c container]
kubectl logs <pod> -n <namespace> --previous
kubectl exec <pod> -n <namespace> -it -- /bin/sh

# Service debugging
kubectl get svc -n <namespace>
kubectl get endpoints -n <namespace>
kubectl describe svc <service> -n <namespace>

# Events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Resource usage
kubectl top nodes
kubectl top pods -n <namespace>

# Network debugging
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- /bin/bash

# Cluster health
kubectl get nodes
kubectl cluster-info
kubectl get componentstatuses
```

### Emergency Commands

```bash
# Delete stuck pod
kubectl delete pod <pod> -n <namespace> --force --grace-period=0

# Restart deployment
kubectl rollout restart deployment/<name> -n <namespace>

# Rollback deployment
kubectl rollout undo deployment/<name> -n <namespace>

# Cordon node (prevent new pods)
kubectl cordon <node-name>

# Drain node (evict pods)
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
```

## Workflow Done Criteria

A troubleshooting run is complete when all checks pass:
- [ ] Issue category was mapped to one workflow above.
- [ ] Evidence was captured (events, logs, describe output, and at least one config/state snapshot).
- [ ] Root cause and fix are connected by observable data.
- [ ] Post-fix verification succeeded (`kubectl get`, `kubectl rollout status`, or service connectivity checks).
- [ ] Any disruptive action was documented with reason and rollback option.
