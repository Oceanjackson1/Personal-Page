---
title: "K8s Yaml Generator"
description: "Generate/create/scaffold Kubernetes YAML — Deployment, Service, ConfigMap, Ingress, RBAC, StatefulSet, CRDs."
category: "devops"
source: "community"
author: "Community"
tags: ["k8s", "yaml", "generator"]
date: 2026-03-20
---

# Kubernetes YAML Generator

Generate Kubernetes manifests with deterministic steps, bounded CRD research, and mandatory validation for full-resource output.

## Trigger Guidance

Use this skill when the user asks to create or update Kubernetes YAML, for example:

- "Generate a Deployment + Service manifest for my app."
- "Create an Argo CD Application CRD."
- "Write a StatefulSet with PVC templates."
- "Produce production-ready Kubernetes YAML with best practices."

Do not use this skill for validation-only requests. For validation-only work, use `k8s-yaml-validator`.

## Execution Model

Normative keywords:

- `MUST`: required
- `SHOULD`: default unless user requests otherwise
- `MAY`: optional

Deterministic sequence:

1. Preflight request and path/rendering sanity.
2. Capture minimum required inputs.
3. Resolve CRD references (bounded workflow only when CRD/custom API is involved).
4. Generate YAML with baseline quality checks.
5. Run mandatory validation (or documented fallback path when tooling is unavailable).
6. Deliver YAML plus explicit validation report and assumptions.

If one step is blocked by environment constraints, execute that step's fallback and continue.

## 1) Preflight

Before generation:

- Confirm whether output is full manifest(s) or snippet-only.
- Confirm target Kubernetes version when provided.
- Verify any referenced local file path exists before using it.
- Normalize resource naming to DNS-1123-compatible names where applicable.

Preflight stop condition:

- If required core inputs are missing (resource type, workload image for Pod-based resources, or CRD kind/apiVersion), ask for those first.

## 2) Capture Required Inputs

Collect:

- Resource types (`Deployment`, `Service`, `ConfigMap`, CRD kind, etc.)
- `apiVersion` + `kind`
- Namespace/scoping requirements
- Ports, replicas, images, probes, storage, and secret/config needs
- Environment assumptions (dev/staging/prod)
- For CRDs: project name and target CRD version if known

Safe defaults (state explicitly in output):

- Namespace: `default` (namespace-scoped resources)
- Deployment replicas: `2`
- Service type: `ClusterIP`
- Image pull policy: `IfNotPresent` (unless user needs forced pulls)

## 3) CRD Lookup Workflow (Bounded)

Run this step only for custom APIs outside Kubernetes built-in groups.

### 3.1 Identify CRD target

Extract:

- API group, version, kind (for example `argoproj.io/v1alpha1`, `Application`)
- Requested product/version (for example Argo CD `v2.9.x`)

### 3.2 Context7 primary path

Use the correct Context7 tools and payloads:

1. `mcp__context7__resolve-library-id`
2. `mcp__context7__query-docs`

Sample payloads:

```text
Tool: mcp__context7__resolve-library-id
libraryName: "argo-cd"
query: "Find Argo CD documentation for Application CRD schema compatibility"
```

```text
Tool: mcp__context7__query-docs
libraryId: "/argoproj/argo-cd/v2.9.0"
query: "Application CRD required spec fields for apiVersion argoproj.io/v1alpha1 with minimal valid example"
```

Selection rules:

- Prefer exact project/library name matches.
- Prefer versioned `libraryId` when user specifies a version.
- Otherwise use unversioned ID and note version uncertainty.

### 3.3 Thresholds and stop conditions

Bound the lookup to prevent unbounded retries:

- `resolve-library-id`: max 2 attempts (primary name + one alternate name).
- `query-docs`: max 3 focused queries total.
- Web fallback: max 2 version-specific searches.

Stop early when all are true:

- Required CRD fields are identified.
- At least one authoritative example is found.
- Version compatibility is known or explicitly marked unknown.

Hard stop when budgets are exhausted:

- Generate only fields verified by sources.
- Mark remaining fields as `Needs confirmation`.
- Report residual risk and request one of:
  - exact CRD docs URL, or
  - cluster introspection output (for example `kubectl explain <kind>.spec` when available).

### 3.4 Fallback order

Use this order:

1. Context7 (`resolve-library-id` -> `query-docs`)
2. Official project docs via web search
3. Cluster-local introspection (`kubectl explain`, if cluster access exists)

If none are available, provide a minimal, clearly marked draft and do not claim full CRD correctness.

## 4) YAML Generation Rules

Apply these checks:

- Use explicit, non-deprecated API versions.
- Include consistent labels (`app.kubernetes.io/*`) across related resources.
- Include namespace for namespace-scoped resources.
- Add resource requests/limits for Pod workloads unless user opts out.
- Add readiness/liveness probes for long-running services where applicable.
- Use `securityContext` to avoid root execution by default.
- Keep multi-resource ordering dependency-safe (for example ConfigMap before Deployment consumers).

Minimal label baseline:

```yaml
labels:
  app.kubernetes.io/name: myapp
  app.kubernetes.io/instance: myapp-prod
  app.kubernetes.io/part-of: myplatform
  app.kubernetes.io/managed-by: codex
```

## 5) Mandatory Validation and Contingencies

For full manifest generation, validation is mandatory.

Primary path:

- Invoke `k8s-yaml-validator`.
- Iterate fix -> revalidate until blocking issues are gone.

Required reporting after each validation pass:

- `Validation mode`: `k8s-yaml-validator` | `script fallback` | `manual fallback`
- `Syntax`: pass/fail
- `Schema`: pass/fail/partial
- `CRD check`: pass/fail/partial
- `Dry-run`: server/client/skipped
- `Blocking issues remaining`: yes/no

Contingency A: validator skill unavailable

Run direct commands:

```bash
bash devops-skills-plugin/skills/k8s-yaml-validator/scripts/setup_tools.sh
yamllint -c devops-skills-plugin/skills/k8s-yaml-validator/assets/.yamllint <file.yaml>
kubeconform -schema-location default -strict -ignore-missing-schemas -summary <file.yaml>
server_out="$(mktemp)"
client_out="$(mktemp)"
trap 'rm -f "$server_out" "$client_out"' EXIT

if kubectl apply --dry-run=server -f <file.yaml> >"$server_out" 2>&1; then
  echo "server_validation=passed"
elif grep -Eqi "connection refused|no such host|i/o timeout|tls handshake timeout|unable to connect to the server|no configuration has been provided|the server doesn't have a resource type" "$server_out"; then
  echo "server_validation=skipped"
  if kubectl apply --dry-run=client -f <file.yaml> >"$client_out" 2>&1; then
    echo "client_validation=passed"
  else
    echo "client_validation=failed"
    cat "$client_out"
    exit 1
  fi
else
  echo "server_validation=failed"
  cat "$server_out"
  exit 1
fi
```

Contingency B: local tools partially unavailable

- Run available checks.
- Record skipped checks explicitly.
- Add residual risk for every skipped check.

Contingency C: repeated validation failure

- Maximum 3 fix/revalidate cycles.
- If still failing, stop and return:
  - current YAML,
  - exact failing errors,
  - smallest required user decision/input to unblock.

Validation exceptions:

- Snippet-only or docs-only requests MAY skip full validation, but the output MUST state `Validation status: Skipped (reason)`.

## 6) Delivery Contract

Final output MUST include:

1. Generated YAML.
2. What was generated (resource list, namespace/scoping).
3. Validation report in the required format.
4. Assumptions and defaults used.
5. References used:
   - Context7 IDs/queries used (for CRDs)
   - external docs/searches used
   - items skipped/missing and impact

Suggested next commands:

```bash
kubectl apply -f <filename>.yaml
kubectl get <resource-type> <name> -n <namespace>
kubectl describe <resource-type> <name> -n <namespace>
```

## 7) Canonical Example Flows

### Example A: Built-in resources (Deployment + Service)

1. Capture app image, ports, replicas, namespace.
2. Generate Deployment and Service with consistent labels/selectors.
3. Validate with `k8s-yaml-validator`.
4. Return YAML + validation report + assumptions.

### Example B: CRD resource (Argo CD Application)

1. Extract `argoproj.io/v1alpha1` + `Application`.
2. Run bounded Context7 lookup (`resolve-library-id` then `query-docs`).
3. If needed, perform bounded web fallback.
4. Generate CRD YAML only with verified fields.
5. Validate, report any partial verification, and return residual risks.

## 8) Definition of Done

Execution is complete only when all applicable checks pass:

- Trigger use case is correct (generation, not validation-only).
- Required inputs are captured or explicit assumptions are documented.
- CRD lookup follows bounded thresholds and stop conditions.
- Tool names and command paths are valid and consistent.
- Full manifests are validated (or fallback path is documented with residual risk).
- Final response includes YAML, validation report, assumptions, and references.

---

## Reference: Resource_Patterns

# Kubernetes Resource Patterns

Canonical YAML patterns for all resources generated by this skill. Each section shows a full pattern with safe defaults, lists required fields, and notes common mistakes.

---

## Deployment

**Required fields:** `apiVersion`, `kind`, `metadata.name`, `spec.selector`, `spec.template`, `spec.template.spec.containers`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: default
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/instance: my-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/part-of: my-app
    app.kubernetes.io/managed-by: kubectl
spec:
  replicas: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: my-app
  template:
    metadata:
      labels:
        app.kubernetes.io/name: my-app   # Must match selector.matchLabels
    spec:
      containers:
      - name: my-app
        image: my-app:1.0.0
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

**Common mistakes:**
- `selector.matchLabels` must be a subset of `template.metadata.labels` — mismatch causes `Invalid value` error
- `selector` is immutable after creation; changing it requires deleting and recreating the Deployment
- Missing `resources.limits` causes pods to be scheduled without constraints

---

## Service

**Required fields:** `apiVersion`, `kind`, `metadata.name`, `spec.ports`, `spec.selector`

```yaml
# ClusterIP (default, internal only)
apiVersion: v1
kind: Service
metadata:
  name: my-app
  namespace: default
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: my-app
  ports:
  - name: http
    port: 80          # Port exposed on the Service
    targetPort: http  # Named port or number on the Pod
    protocol: TCP
---
# NodePort (external via node IP + port)
apiVersion: v1
kind: Service
metadata:
  name: my-app-nodeport
  namespace: default
spec:
  type: NodePort
  selector:
    app.kubernetes.io/name: my-app
  ports:
  - name: http
    port: 80
    targetPort: http
    nodePort: 30080   # 30000–32767; omit to auto-assign
---
# LoadBalancer (external via cloud LB)
apiVersion: v1
kind: Service
metadata:
  name: my-app-lb
  namespace: default
spec:
  type: LoadBalancer
  selector:
    app.kubernetes.io/name: my-app
  ports:
  - name: http
    port: 80
    targetPort: http
```

**Common mistakes:**
- `targetPort` must match a `containerPort` name or number defined in the pod spec
- `selector` must match labels on pods, not on the Deployment itself

---

## StatefulSet

**Required fields:** `spec.serviceName` (must match a headless Service), `spec.selector`, `spec.template`, `volumeClaimTemplates` (if using persistent storage)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: my-db
  namespace: default
spec:
  serviceName: my-db-headless   # Must reference a headless Service (clusterIP: None)
  replicas: 3
  podManagementPolicy: OrderedReady  # Or Parallel for faster scale
  selector:
    matchLabels:
      app.kubernetes.io/name: my-db
  template:
    metadata:
      labels:
        app.kubernetes.io/name: my-db
    spec:
      containers:
      - name: my-db
        image: postgres:15
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes:
      - ReadWriteOnce
      storageClassName: standard
      resources:
        requests:
          storage: 10Gi
```

**Common mistakes:**
- `volumeClaimTemplates` are immutable; to resize, delete the StatefulSet (keep pods), update PVCs, then recreate
- The headless Service (`clusterIP: None`) must exist before the StatefulSet, or pods stay Pending
- Pod DNS: `<pod>.<serviceName>.<namespace>.svc.cluster.local`

---

## DaemonSet

**Required fields:** `spec.selector`, `spec.template`

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: my-agent
  namespace: default
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: my-agent
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  template:
    metadata:
      labels:
        app.kubernetes.io/name: my-agent
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      containers:
      - name: my-agent
        image: my-agent:1.0.0
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

**Common mistakes:**
- DaemonSets run on every node by default; use `tolerations` + `nodeSelector` to restrict to specific nodes
- Without `tolerations` for control-plane taint, the pod won't run on control-plane nodes

---

## Job

**Required fields:** `spec.template.spec.containers`, `spec.template.spec.restartPolicy` (must be `Never` or `OnFailure`)

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: my-batch-job
  namespace: default
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 3
  ttlSecondsAfterFinished: 300   # Auto-delete after 5 minutes
  template:
    spec:
      restartPolicy: Never   # Never or OnFailure; not Always
      containers:
      - name: my-job
        image: my-job:1.0.0
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
```

**Common mistakes:**
- `restartPolicy: Always` is forbidden in Jobs — use `Never` or `OnFailure`
- Without `ttlSecondsAfterFinished`, completed Jobs and their pods accumulate indefinitely

---

## CronJob

**Required fields:** `spec.schedule`, `spec.jobTemplate`

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: my-cron
  namespace: default
spec:
  schedule: "0 2 * * *"           # Daily at 02:00 UTC
  timeZone: "UTC"                  # Explicit timezone (K8s 1.27+ GA)
  concurrencyPolicy: Forbid        # Allow, Forbid, or Replace
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 600
  jobTemplate:
    spec:
      backoffLimit: 2
      ttlSecondsAfterFinished: 600
      template:
        spec:
          restartPolicy: OnFailure
          containers:
          - name: my-cron
            image: my-job:1.0.0
            resources:
              requests:
                memory: "64Mi"
                cpu: "50m"
              limits:
                memory: "128Mi"
                cpu: "200m"
```

**Common mistakes:**
- `schedule` uses UTC by default; use `timeZone` to specify local timezone
- `concurrencyPolicy: Allow` (default) can cause job pile-up if runs take longer than the interval

---

## ConfigMap

**Required fields:** `apiVersion`, `kind`, `metadata.name`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-app-config
  namespace: default
immutable: false   # Set to true to prevent accidental changes
data:
  KEY: value
  config.yaml: |
    server:
      port: 8080
binaryData:
  logo.png: <base64-encoded bytes>   # Use binaryData for non-UTF-8 content
```

**Common mistakes:**
- `data` values must be strings; use `binaryData` for binary content
- `immutable: true` prevents updates; pod must be restarted manually after recreation

---

## Secret

**Required fields:** `apiVersion`, `kind`, `metadata.name`, `type`

```yaml
# Opaque (arbitrary key-value pairs)
apiVersion: v1
kind: Secret
metadata:
  name: my-app-secret
  namespace: default
type: Opaque
immutable: false
data:
  username: bXktdXNlcg==      # base64-encoded; echo -n 'my-user' | base64
  password: c2VjcmV0          # base64-encoded
---
# TLS secret (for Ingress TLS)
apiVersion: v1
kind: Secret
metadata:
  name: my-app-tls
  namespace: default
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded cert>
  tls.key: <base64-encoded key>
```

**Common mistakes:**
- Values in `data` must be base64-encoded; use `stringData` for plain text (Kubernetes handles encoding)
- `stringData` is write-only; it's always read back as base64 in `data`

---

## PersistentVolumeClaim

**Required fields:** `spec.accessModes`, `spec.resources.requests.storage`

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-data-pvc
  namespace: default
spec:
  accessModes:
  - ReadWriteOnce    # RWO (single node), RWX (many nodes), ROX (read-only many)
  storageClassName: standard
  resources:
    requests:
      storage: 10Gi
```

**Common mistakes:**
- `accessModes` must match what the StorageClass/PV supports; `ReadWriteMany` requires specific storage backends
- PVC spec (except `resources.requests.storage`) is immutable after binding

---

## Ingress

**Required fields:** `spec.rules`

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: default
spec:
  ingressClassName: nginx    # Required in K8s 1.18+; do not use deprecated annotation
  tls:
  - hosts:
    - my-app.example.com
    secretName: my-app-tls
  rules:
  - host: my-app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix   # Prefix, Exact, or ImplementationSpecific
        backend:
          service:
            name: my-app
            port:
              name: http
```

**Common mistakes:**
- Use `ingressClassName` field, not the deprecated `kubernetes.io/ingress.class` annotation
- `pathType: ImplementationSpecific` behavior varies by controller; prefer `Prefix` or `Exact`

---

## NetworkPolicy

**Required fields:** `spec.podSelector` (empty = select all pods in namespace)

```yaml
# Default deny all ingress and egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
---
# Allow ingress from specific namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-monitoring
  namespace: default
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: my-app
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: monitoring
---
# Allow egress DNS only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-dns
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

**Common mistakes:**
- NetworkPolicy is additive: multiple policies union their rules; a pod not selected by any policy has no restrictions
- Always create a `default-deny-all` before adding allow rules to avoid gaps
- Forgetting to allow egress DNS (port 53) breaks service discovery

---

## ServiceAccount

**Required fields:** `apiVersion`, `kind`, `metadata.name`

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: default
automountServiceAccountToken: false   # Disable for workloads that don't need API access
imagePullSecrets:
- name: my-registry-secret   # Attach pull secrets to the SA instead of each pod
```

---

## Role / ClusterRole

```yaml
# Namespace-scoped
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-app-role
  namespace: default
rules:
- apiGroups: [""]          # "" = core API group
  resources: ["configmaps"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["my-app-secret"]   # Restrict to named resources
  verbs: ["get"]
---
# Cluster-scoped
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: my-app-reader
rules:
- apiGroups: [""]
  resources: ["nodes", "namespaces"]
  verbs: ["get", "list", "watch"]
```

---

## RoleBinding / ClusterRoleBinding

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: my-app-rolebinding
  namespace: default
subjects:
- kind: ServiceAccount
  name: my-app
  namespace: default
roleRef:
  kind: Role           # Role or ClusterRole
  name: my-app-role
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: my-app-clusterrolebinding
subjects:
- kind: ServiceAccount
  name: my-app
  namespace: default
roleRef:
  kind: ClusterRole
  name: my-app-reader
  apiGroup: rbac.authorization.k8s.io
```

**Common mistakes:**
- `roleRef` is immutable; changing it requires deleting and recreating the binding
- Use `Role`+`RoleBinding` for namespace-scoped access; `ClusterRole`+`ClusterRoleBinding` for cluster-wide access
- A `ClusterRole` can be bound with a `RoleBinding` to limit it to one namespace

---

## HorizontalPodAutoscaler (v2)

**Required fields:** `spec.scaleTargetRef`, `spec.minReplicas`, `spec.maxReplicas`, `spec.metrics`

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Common mistakes:**
- Use `autoscaling/v2` (available since Kubernetes v1.23, stable); `autoscaling/v2beta2` is deprecated
- HPA requires `resources.requests` to be set on containers; without requests, CPU/memory utilization cannot be calculated

---

## PodDisruptionBudget

**Required fields:** `spec.selector`, one of `minAvailable` or `maxUnavailable`

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
  namespace: default
spec:
  minAvailable: 1     # Or use maxUnavailable; not both
  selector:
    matchLabels:
      app.kubernetes.io/name: my-app
```

**Common mistakes:**
- Use `policy/v1` (GA since K8s 1.21); `policy/v1beta1` is removed
- Setting `minAvailable` equal to `replicas` blocks all voluntary disruptions (node drain fails)

---

## Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace
  labels:
    kubernetes.io/metadata.name: my-namespace   # Automatically set by K8s 1.21+
```

---

## ResourceQuota

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: my-namespace-quota
  namespace: my-namespace
spec:
  hard:
    requests.cpu: "4"
    requests.memory: 8Gi
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"
    services: "10"
    persistentvolumeclaims: "10"
```

---

## LimitRange

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: my-namespace-limits
  namespace: my-namespace
spec:
  limits:
  - type: Container
    default:          # Applied when container has no limits set
      cpu: "500m"
      memory: "256Mi"
    defaultRequest:   # Applied when container has no requests set
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "2"
      memory: "2Gi"
    min:
      cpu: "50m"
      memory: "64Mi"
  - type: PersistentVolumeClaim
    max:
      storage: 50Gi
    min:
      storage: 1Gi
```

---

## Reference: Security_Patterns

# Kubernetes Security Patterns

Security hardening reference for all resources generated by this skill.

---

## Pod-level securityContext

Applied at `spec.template.spec.securityContext` in Deployments/StatefulSets/DaemonSets.

```yaml
securityContext:
  runAsNonRoot: true           # Reject containers running as root (UID 0)
  runAsUser: 1000              # Specific UID; must be non-zero when runAsNonRoot: true
  runAsGroup: 3000             # GID for the primary process
  fsGroup: 2000                # GID for volume mounts; files will be group-owned by this GID
  fsGroupChangePolicy: OnRootMismatch   # Only chown if owner/mode mismatch (faster)
  supplementalGroups: [4000]   # Additional GIDs for the process
  seccompProfile:
    type: RuntimeDefault       # Use the node's default seccomp profile (recommended)
    # type: Localhost          # Load a custom profile from the node
    # localhostProfile: profiles/my-profile.json
    # type: Unconfined         # No seccomp filtering (avoid in production)
  sysctls: []                  # Allow only safe sysctls; empty is safest
```

**Key points:**
- `runAsNonRoot: true` is enforced at admission; the image's USER must be non-zero
- `fsGroup` is required for writable volume mounts; without it, mounted volumes may not be writable by the process
- `seccompProfile: RuntimeDefault` adds significant syscall filtering with minimal application impact

---

## Container-level securityContext

Applied at `spec.template.spec.containers[*].securityContext`.

```yaml
securityContext:
  allowPrivilegeEscalation: false   # Prevent gaining more privileges than parent (always set false)
  readOnlyRootFilesystem: true       # Mount container root FS as read-only
  runAsNonRoot: true                 # Container-level override of pod-level
  runAsUser: 1000                    # Container-level override of pod-level
  capabilities:
    drop:
    - ALL                            # Drop all Linux capabilities
    add:
    - NET_BIND_SERVICE               # Re-add only what's required (binding port <1024)
  privileged: false                  # Never set true in production
  procMount: Default                 # Default; Unmasked only for container-in-container
  seccompProfile:
    type: RuntimeDefault             # Container-level override of pod-level
```

**Minimum recommended set (add to every container):**
```yaml
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
    - ALL
```

**When `readOnlyRootFilesystem: true` requires temp space**, add an `emptyDir` volume:
```yaml
volumeMounts:
- name: tmp
  mountPath: /tmp
volumes:
- name: tmp
  emptyDir: {}
```

---

## NetworkPolicy Patterns

### Default deny all (apply first in every namespace)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: my-namespace
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow ingress from same namespace only

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-same-namespace
  namespace: my-namespace
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector: {}   # Any pod in the same namespace
```

### Allow ingress from specific namespace (e.g., monitoring)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-monitoring
  namespace: my-namespace
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: my-app
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: monitoring
      podSelector:
        matchLabels:
          app.kubernetes.io/name: prometheus   # Both conditions must be true (AND)
```

### Allow egress DNS + specific services only

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-selective
  namespace: my-namespace
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: my-app
  policyTypes:
  - Egress
  egress:
  - ports:   # DNS — always required for service discovery
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  - to:
    - podSelector:
        matchLabels:
          app.kubernetes.io/name: my-db
    ports:
    - protocol: TCP
      port: 5432
```

**Key points:**
- In `from`/`to`, multiple items are ORed; within an item, `namespaceSelector` + `podSelector` are ANDed
- Always allow DNS egress (port 53 UDP+TCP) or pod DNS lookups will fail
- Apply `default-deny-all` before adding allow rules

---

## Minimal RBAC

### When to use Role vs ClusterRole

| Scenario | Use |
|---|---|
| Access resources in one namespace | `Role` + `RoleBinding` |
| Access resources across all namespaces | `ClusterRole` + `ClusterRoleBinding` |
| Reuse the same permissions in multiple namespaces | `ClusterRole` + `RoleBinding` (per namespace) |
| Node-level or non-namespaced resources | `ClusterRole` + `ClusterRoleBinding` |

### Aggregated ClusterRoles

Use aggregation to extend built-in roles without modifying them:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: my-custom-viewer
  labels:
    rbac.authorization.k8s.io/aggregate-to-view: "true"   # Extends 'view' ClusterRole
rules:
- apiGroups: ["my.custom.io"]
  resources: ["myresources"]
  verbs: ["get", "list", "watch"]
```

### Principle of least privilege

```yaml
rules:
# Good: specific resources, specific verbs, specific names
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["only-this-secret"]
  verbs: ["get"]

# Avoid: wildcard verbs or resources
- apiGroups: ["*"]
  resources: ["*"]
  verbs: ["*"]
```

---

## ImagePullSecrets and Private Registries

### Attach to ServiceAccount (recommended — applies to all pods using the SA)

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: default
imagePullSecrets:
- name: my-registry-secret
```

### Attach directly to Pod (use when SA approach is not applicable)

```yaml
spec:
  imagePullSecrets:
  - name: my-registry-secret
```

### Create the pull secret

```bash
kubectl create secret docker-registry my-registry-secret \
  --docker-server=registry.example.com \
  --docker-username=my-user \
  --docker-password=my-password \
  --namespace=default
```

---

## ServiceAccount Token Auto-mounting

By default, Kubernetes mounts a ServiceAccount token into every pod at `/var/run/secrets/kubernetes.io/serviceaccount/`. Disable this for workloads that don't need API server access:

```yaml
# Disable on the ServiceAccount (applies to all pods using it)
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
  namespace: default
automountServiceAccountToken: false
```

```yaml
# Override on the Pod/Deployment (takes precedence over ServiceAccount setting)
spec:
  template:
    spec:
      automountServiceAccountToken: false
```

**When to keep it enabled:**
- Operators and controllers that watch/modify Kubernetes resources
- Applications using in-cluster config (`rest.InClusterConfig()`)
- Service meshes that inject sidecars needing API access

**When to disable it:**
- Web applications, APIs, and stateless services
- Batch jobs without cluster API interaction
- Any workload where the token is not used

---

## Complete Hardened Pod Template

Combine all patterns for a production-ready pod template:

```yaml
spec:
  serviceAccountName: my-app
  automountServiceAccountToken: false
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: my-app
    image: my-app:1.0.0
    imagePullPolicy: IfNotPresent
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "256Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /healthz
        port: http
      initialDelaySeconds: 10
      periodSeconds: 15
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /readyz
        port: http
      initialDelaySeconds: 5
      periodSeconds: 10
      failureThreshold: 3
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
```
