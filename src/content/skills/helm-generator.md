---
title: "Helm Chart 生成器"
description: "生成 Kubernetes Helm Chart 模板和配置"
category: "devops"
source: "community"
author: "Community"
tags: ["helm", "generator"]
date: 2026-03-20
---

# Helm Chart Generator

## Overview

Generate production-ready Helm charts with deterministic scaffolding, standard helpers, reusable templates, and validation loops.

**Official Documentation:**
- [Helm Docs](https://helm.sh/docs/) - Main documentation
- [Chart Best Practices](https://helm.sh/docs/chart_best_practices/) - Official best practices guide
- [Template Functions](https://helm.sh/docs/chart_template_guide/function_list/) - Built-in functions
- [Sprig Functions](http://masterminds.github.io/sprig/) - Extended function library

## When to Use This Skill

| Use helm-generator | Use OTHER skill |
|-------------------|-----------------|
| Create new Helm charts | **helm-validator**: Validate/lint existing charts |
| Generate Helm templates | **k8s-yaml-generator**: Raw K8s YAML (no Helm) |
| Convert K8s manifests to Helm | **k8s-debug**: Debug deployed resources |
| Implement CRDs in Helm | **k8s-yaml-validator**: Validate K8s manifests |

### Trigger Phrases

Use this skill when prompts include phrases like:
- "create Helm chart"
- "scaffold Helm chart"
- "generate Helm templates"
- "convert manifests to Helm chart"
- "build chart with Deployment/Service/Ingress"

## Execution Flow

Follow these stages in order. Do not skip required stages.

### Stage 1: Gather Requirements (Required)

Collect:
- Scope: full chart, specific templates, or conversion from manifests
- Workload: `deployment`, `statefulset`, or `daemonset`
- Image reference: repository, optional tag, or digest
- Ports: service port and container target port (separate values)
- Runtime settings: resources, probes, autoscaling, ingress, storage
- Security: service account, security contexts, optional RBAC/network policies

Use `request_user_input` when critical fields are missing.

If `request_user_input` is unavailable, ask in normal chat and continue with explicit assumptions.

| Missing Information | Question to Ask |
|---------------------|-----------------|
| Image repository/tag | "What container image should be used? (e.g., nginx:1.25)" |
| Service port | "What service port should be exposed?" |
| Container target port | "What container port should traffic be forwarded to?" |
| Resource limits | "What CPU/memory limits should be set? (e.g., 500m CPU, 512Mi memory)" |
| Probe endpoints | "What health check endpoints does the app expose? (e.g., /health, /ready)" |
| Scaling requirements | "Should autoscaling be enabled? If yes, min/max replicas and target CPU%?" |
| Workload type | "What workload type: Deployment, StatefulSet, or DaemonSet?" |
| Storage requirements | "Does the application need persistent storage? Size and access mode?" |

Do not silently assume critical settings.

### Stage 2: Lookup CRD Documentation (Only if CRDs Are In Scope)

1. Try Context7 first:
   - `mcp__context7__resolve-library-id`
   - `mcp__context7__query-docs`
2. Fallback chain if Context7 is unavailable or incomplete:
   - Operator official docs (preferred)
   - General web search

Also consult `references/crd_patterns.md` for example patterns.

### Stage 3: Scaffold Chart Structure (Required)

Run:
```bash
bash scripts/generate_chart_structure.sh <chart-name> <output-directory> [options]
```

Options:
- `--image <repo>` - Supports repo-only, tagged image, registry ports, and digest refs
- `--port <number>` - Service port (default: 80)
- `--target-port <number>` - Container target port (default: 8080)
- `--type <type>` - Workload type: deployment, statefulset, daemonset (default: deployment)
- `--with-templates` - Generate resource templates (deployment.yaml, service.yaml, etc.)
- `--with-ingress` - Include ingress template
- `--with-hpa` - Include HPA template
- `--force` - Overwrite existing chart without prompting

Image parsing behavior:
- `--image nginx:1.27` -> repository `nginx`, tag `1.27`
- `--image registry.local:5000/team/app` -> repository kept intact
- `--image ghcr.io/org/app@sha256:...` -> digest mode (no tag concatenation)
- `--tag` cannot be combined with digest image references

Idempotency and overwrite behavior:
- `generate_chart_structure.sh`: prompts before overwrite; `--force` overwrites non-interactively.
- `generate_standard_helpers.sh`: prompts before replacing `templates/_helpers.tpl`; `--force` bypasses prompt.

Expected scaffold shape:
```
mychart/
  Chart.yaml
  values.yaml
  templates/
    _helpers.tpl
    NOTES.txt
    serviceaccount.yaml
    service.yaml
    configmap.yaml
    secret.yaml
    deployment.yaml|statefulset.yaml|daemonset.yaml
    ingress.yaml (optional)
    hpa.yaml (optional)
  .helmignore
```

### Stage 4: Generate Standard Helpers

Run:
```bash
bash scripts/generate_standard_helpers.sh <chart-name> <chart-directory>
```

Required helpers: `name`, `fullname`, `chart`, `labels`, `selectorLabels`, `serviceAccountName`.

Fallback:
- If script execution is blocked, copy `assets/_helpers-template.tpl` and replace `CHARTNAME` with the chart name.

### Stage 5: Consult References and Generate Templates (Required)

Consult relevant references once at this stage:
- `references/resource_templates.md` for the resource patterns being generated
- `references/helm_template_functions.md` for templating function usage
- `references/crd_patterns.md` only when CRDs are in scope

Example file-open commands:
```bash
sed -n '1,220p' references/resource_templates.md
sed -n '1,220p' references/helm_template_functions.md
```

Resource coverage from `references/resource_templates.md`:
- Workloads: Deployment, StatefulSet, DaemonSet, Job, CronJob
- Services: Service, Ingress
- Config: ConfigMap, Secret
- RBAC: ServiceAccount, Role, RoleBinding, ClusterRole, ClusterRoleBinding
- Network: NetworkPolicy
- Autoscaling: HPA, PodDisruptionBudget

Required template patterns:
```yaml
metadata:
  name: {{ include "mychart.fullname" . }}
  labels: {{- include "mychart.labels" . | nindent 4 }}

{{- with .Values.nodeSelector }}
nodeSelector: {{- toYaml . | nindent 2 }}
{{- end }}

annotations:
  {{- if and .Values.configMap .Values.configMap.enabled }}
  checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
  {{- end }}
```

Checksum annotations are required for workloads, but must be conditional and only reference generated templates (`configmap.yaml`, `secret.yaml`).

### Stage 6: Create values.yaml

Structure guidelines:
- Group related settings logically
- Document every value with `# --` comments
- Provide sensible defaults
- Include security contexts, resource limits, probes
- Keep `service.port` and `service.targetPort` separate and explicit
- Keep `configMap.enabled` / `secret.enabled` aligned with generated templates

See `assets/values-schema-template.json` for JSON Schema validation.

### Stage 7: Validate

Preferred path: run the `helm-validator` skill.

If skill invocation is unavailable, run local commands directly:
```bash
helm lint <chart-dir>
helm template test <chart-dir>
```

If `helm` is unavailable, report the block clearly and perform partial checks:
- `bash -n scripts/generate_chart_structure.sh`
- `bash -n scripts/generate_standard_helpers.sh`
- Verify generated files and key fields manually

Re-run validation after any fixes.

## Template Functions Quick Reference

See `references/helm_template_functions.md` for complete guide.

| Function | Purpose | Example |
|----------|---------|---------|
| `required` | Enforce required values | `{{ required "msg" .Values.x }}` |
| `default` | Fallback value | `{{ .Values.x \| default 1 }}` |
| `quote` | Quote strings | `{{ .Values.x \| quote }}` |
| `include` | Use helpers | `{{ include "name" . \| nindent 4 }}` |
| `toYaml` | Convert to YAML | `{{ toYaml .Values.x \| nindent 2 }}` |
| `tpl` | Render as template | `{{ tpl .Values.config . }}` |
| `nindent` | Newline + indent | `{{- include "x" . \| nindent 4 }}` |

## Working with CRDs

See `references/crd_patterns.md` for complete examples.

Key points:
- CRDs you ship -> `crds/` directory (not templated, not deleted on uninstall)
- CR instances -> `templates/` directory (fully templated)
- Always look up documentation for CRD spec requirements
- Document operator dependencies in Chart.yaml annotations

## Converting Manifests to Helm

1. **Parameterize:** Names -> helpers, values -> `values.yaml`
2. **Apply patterns:** Labels, conditionals, `toYaml` for complex objects
3. **Add helpers:** Create `_helpers.tpl` with standard helpers
4. **Validate:** Run `helm-validator` (or local lint/template fallback), then test with different values

## Error Handling

| Issue | Solution |
|-------|----------|
| Template syntax errors | `helm template test <chart-dir> --debug --show-only templates/<file>.yaml` |
| Undefined values | `helm lint <chart-dir> --strict` and add `default`/`required` |
| Checksum include errors | Ensure `templates/configmap.yaml` and `templates/secret.yaml` exist and `configMap.enabled` / `secret.enabled` are set correctly |
| Port mismatch (Service vs container) | Set both `service.port` and `service.targetPort`, then re-run `helm template test <chart-dir>` |
| CRD validation fails | Verify apiVersion/spec fields with Context7 or operator docs, then re-render |
| Script argument failures | Run `bash scripts/generate_chart_structure.sh --help` and pass required values for option flags |

## Example Flows

Full scaffold with templates, ingress, HPA, and explicit port mapping:
```bash
bash scripts/generate_chart_structure.sh webapp ./charts \
  --image ghcr.io/acme/webapp:2.3.1 \
  --port 80 \
  --target-port 8080 \
  --type deployment \
  --with-templates \
  --with-ingress \
  --with-hpa
```

Digest-based image scaffold:
```bash
bash scripts/generate_chart_structure.sh api ./charts \
  --image ghcr.io/acme/api@sha256:0123456789abcdef \
  --with-templates
```

Minimal scaffold without templates:
```bash
bash scripts/generate_chart_structure.sh starter ./charts
```

## Scaffold Success Criteria

Mark complete only when all checks pass:
- [ ] `Chart.yaml`, `values.yaml`, `.helmignore`, `templates/NOTES.txt`, and `templates/_helpers.tpl` exist
- [ ] `values.yaml` contains explicit `service.port` and `service.targetPort`
- [ ] If `--with-templates` was used, `serviceaccount.yaml`, `service.yaml`, `configmap.yaml`, `secret.yaml`, and one workload template exist
- [ ] Generated workload template uses conditional checksum annotations for config/secret
- [ ] Image rendering logic supports tag and digest modes
- [ ] Validation completed (`helm-validator` skill or local fallback commands) and outcomes reported

## Resources

### Scripts
| Script | Usage |
|--------|-------|
| `scripts/generate_chart_structure.sh` | `bash scripts/generate_chart_structure.sh <chart-name> <output-dir> [options]` |
| `scripts/generate_standard_helpers.sh` | `bash scripts/generate_standard_helpers.sh <chart-name> <chart-dir> [--force]` |

### References
| File | Content |
|------|---------|
| `references/helm_template_functions.md` | Complete template function guide |
| `references/resource_templates.md` | All K8s resource templates |
| `references/crd_patterns.md` | CRD patterns (cert-manager, Prometheus, Istio, ArgoCD) |

### Assets
| File | Purpose |
|------|---------|
| `assets/_helpers-template.tpl` | Standard helpers template |
| `assets/values-schema-template.json` | JSON Schema for values validation |

## Integration with helm-validator

After generating charts, invoke `helm-validator` and close the loop:
1. Generate chart/templates
2. Run `helm-validator` (or local fallback commands)
3. Fix identified issues
4. Re-validate until passing

---

## Reference: Crd_Patterns

# CRD Patterns and Examples

Common Custom Resource Definition patterns and examples for Helm charts.

## Table of Contents

- [cert-manager](#cert-manager)
- [Prometheus Operator](#prometheus-operator)
- [Istio](#istio)
- [ArgoCD](#argocd)
- [Sealed Secrets](#sealed-secrets)
- [External Secrets Operator](#external-secrets-operator)
- [Gateway API](#gateway-api)
- [KEDA](#keda)
- [VerticalPodAutoscaler (VPA)](#verticalpodautoscaler-vpa)

---

## cert-manager

### Certificate Resource

**File:** `templates/certificate.yaml`

```yaml
{{- if .Values.certificate.enabled }}
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: {{ include "mychart.fullname" . }}-tls
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  secretName: {{ include "mychart.fullname" . }}-tls
  issuerRef:
    name: {{ .Values.certificate.issuer.name }}
    kind: {{ .Values.certificate.issuer.kind | default "ClusterIssuer" }}
    {{- with .Values.certificate.issuer.group }}
    group: {{ . }}
    {{- end }}
  commonName: {{ .Values.certificate.commonName | default (first .Values.certificate.dnsNames) }}
  dnsNames:
    {{- range .Values.certificate.dnsNames }}
    - {{ . | quote }}
    {{- end }}
  {{- with .Values.certificate.ipAddresses }}
  ipAddresses:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.certificate.uris }}
  uris:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.certificate.duration }}
  duration: {{ . }}
  {{- end }}
  {{- with .Values.certificate.renewBefore }}
  renewBefore: {{ . }}
  {{- end }}
  {{- with .Values.certificate.usages }}
  usages:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.certificate.privateKey }}
  privateKey:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.certificate.keystores }}
  keystores:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
certificate:
  enabled: false
  issuer:
    name: letsencrypt-prod
    kind: ClusterIssuer
    group: cert-manager.io
  commonName: ""
  dnsNames:
    - example.com
    - www.example.com
  ipAddresses: []
  uris: []
  duration: 2160h  # 90 days
  renewBefore: 360h  # 15 days
  usages:
    - digital signature
    - key encipherment
  privateKey:
    algorithm: RSA
    encoding: PKCS1
    size: 2048
    rotationPolicy: Never
  keystores: {}
  # keystores:
  #   jks:
  #     create: true
  #     passwordSecretRef:
  #       name: jks-password
  #       key: password
```

### ClusterIssuer Resource

**File:** `templates/clusterissuer.yaml`

```yaml
{{- if .Values.certManager.clusterIssuer.create }}
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: {{ .Values.certManager.clusterIssuer.name }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  {{- if eq .Values.certManager.clusterIssuer.type "acme" }}
  acme:
    server: {{ .Values.certManager.clusterIssuer.acme.server }}
    email: {{ required "certManager.clusterIssuer.acme.email is required!" .Values.certManager.clusterIssuer.acme.email }}
    privateKeySecretRef:
      name: {{ .Values.certManager.clusterIssuer.acme.privateKeySecretName }}
    solvers:
    {{- range .Values.certManager.clusterIssuer.acme.solvers }}
    - {{ toYaml . | nindent 6 }}
    {{- end }}
  {{- else if eq .Values.certManager.clusterIssuer.type "ca" }}
  ca:
    secretName: {{ .Values.certManager.clusterIssuer.ca.secretName }}
  {{- else if eq .Values.certManager.clusterIssuer.type "selfSigned" }}
  selfSigned: {}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
certManager:
  clusterIssuer:
    create: false
    name: letsencrypt-prod
    type: acme  # acme, ca, selfSigned, vault, venafi
    acme:
      server: https://acme-v02.api.letsencrypt.org/directory
      email: admin@example.com
      privateKeySecretName: letsencrypt-prod-account-key
      solvers:
        - http01:
            ingress:
              class: nginx
        # - dns01:
        #     cloudflare:
        #       email: admin@example.com
        #       apiTokenSecretRef:
        #         name: cloudflare-api-token
        #         key: api-token
    ca:
      secretName: ca-key-pair
```

---

## Prometheus Operator

### ServiceMonitor Resource

**File:** `templates/servicemonitor.yaml`

```yaml
{{- if .Values.metrics.serviceMonitor.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
    {{- with .Values.metrics.serviceMonitor.labels }}
    {{- toYaml . | nindent 4 }}
    {{- end }}
  {{- with .Values.metrics.serviceMonitor.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  endpoints:
  - port: {{ .Values.metrics.serviceMonitor.port | default "metrics" }}
    {{- with .Values.metrics.serviceMonitor.interval }}
    interval: {{ . }}
    {{- end }}
    {{- with .Values.metrics.serviceMonitor.scrapeTimeout }}
    scrapeTimeout: {{ . }}
    {{- end }}
    {{- with .Values.metrics.serviceMonitor.path }}
    path: {{ . }}
    {{- end }}
    {{- with .Values.metrics.serviceMonitor.scheme }}
    scheme: {{ . }}
    {{- end }}
    {{- with .Values.metrics.serviceMonitor.tlsConfig }}
    tlsConfig:
      {{- toYaml . | nindent 6 }}
    {{- end }}
    {{- with .Values.metrics.serviceMonitor.relabelings }}
    relabelings:
      {{- toYaml . | nindent 6 }}
    {{- end }}
    {{- with .Values.metrics.serviceMonitor.metricRelabelings }}
    metricRelabelings:
      {{- toYaml . | nindent 6 }}
    {{- end }}
  {{- with .Values.metrics.serviceMonitor.namespaceSelector }}
  namespaceSelector:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
metrics:
  enabled: true
  port: 9090
  serviceMonitor:
    enabled: false
    labels: {}
    annotations: {}
    port: metrics
    interval: 30s
    scrapeTimeout: 10s
    path: /metrics
    scheme: http
    tlsConfig: {}
    relabelings: []
    metricRelabelings: []
    namespaceSelector: {}
```

### PrometheusRule Resource

**File:** `templates/prometheusrule.yaml`

```yaml
{{- if .Values.metrics.prometheusRule.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
    {{- with .Values.metrics.prometheusRule.labels }}
    {{- toYaml . | nindent 4 }}
    {{- end }}
spec:
  groups:
  {{- range .Values.metrics.prometheusRule.groups }}
  - name: {{ .name }}
    {{- with .interval }}
    interval: {{ . }}
    {{- end }}
    rules:
    {{- range .rules }}
    - alert: {{ .alert }}
      expr: {{ .expr }}
      {{- with .for }}
      for: {{ . }}
      {{- end }}
      {{- with .labels }}
      labels:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      annotations:
        {{- range $key, $value := .annotations }}
        {{ $key }}: {{ $value | quote }}
        {{- end }}
    {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
metrics:
  prometheusRule:
    enabled: false
    labels: {}
    groups:
      - name: mychart-alerts
        interval: 30s
        rules:
          - alert: HighErrorRate
            expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
            for: 10m
            labels:
              severity: warning
            annotations:
              summary: "High error rate detected"
              description: "Error rate is {{ $value }} errors per second"
          - alert: PodDown
            expr: up{job="mychart"} == 0
            for: 5m
            labels:
              severity: critical
            annotations:
              summary: "Pod is down"
              description: "Pod {{ $labels.pod }} is down"
```

---

## Istio

### VirtualService Resource

**File:** `templates/virtualservice.yaml`

```yaml
{{- if .Values.istio.virtualService.enabled }}
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  hosts:
  {{- range .Values.istio.virtualService.hosts }}
    - {{ . | quote }}
  {{- end }}
  {{- with .Values.istio.virtualService.gateways }}
  gateways:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.istio.virtualService.http }}
  http:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.istio.virtualService.tcp }}
  tcp:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.istio.virtualService.tls }}
  tls:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
istio:
  virtualService:
    enabled: false
    hosts:
      - example.com
    gateways:
      - istio-system/gateway
    http:
      - match:
          - uri:
              prefix: /api
        route:
          - destination:
              host: mychart-svc
              port:
                number: 80
            weight: 90
          - destination:
              host: mychart-svc-canary
              port:
                number: 80
            weight: 10
        timeout: 30s
        retries:
          attempts: 3
          perTryTimeout: 10s
    tcp: []
    tls: []
```

### Gateway Resource

**File:** `templates/gateway.yaml`

```yaml
{{- if .Values.istio.gateway.enabled }}
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  selector:
    {{- toYaml .Values.istio.gateway.selector | nindent 4 }}
  servers:
  {{- range .Values.istio.gateway.servers }}
  - port:
      number: {{ .port.number }}
      name: {{ .port.name }}
      protocol: {{ .port.protocol }}
    hosts:
    {{- range .hosts }}
      - {{ . | quote }}
    {{- end }}
    {{- with .tls }}
    tls:
      {{- toYaml . | nindent 6 }}
    {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
istio:
  gateway:
    enabled: false
    selector:
      istio: ingressgateway
    servers:
      - port:
          number: 80
          name: http
          protocol: HTTP
        hosts:
          - example.com
      - port:
          number: 443
          name: https
          protocol: HTTPS
        hosts:
          - example.com
        tls:
          mode: SIMPLE
          credentialName: example-com-tls
```

### DestinationRule Resource

**File:** `templates/destinationrule.yaml`

```yaml
{{- if .Values.istio.destinationRule.enabled }}
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  host: {{ .Values.istio.destinationRule.host | default (include "mychart.fullname" .) }}
  {{- with .Values.istio.destinationRule.trafficPolicy }}
  trafficPolicy:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.istio.destinationRule.subsets }}
  subsets:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
istio:
  destinationRule:
    enabled: false
    host: mychart-svc
    trafficPolicy:
      connectionPool:
        tcp:
          maxConnections: 100
        http:
          http1MaxPendingRequests: 50
          http2MaxRequests: 100
      loadBalancer:
        simple: LEAST_REQUEST
      outlierDetection:
        consecutiveErrors: 5
        interval: 30s
        baseEjectionTime: 30s
        maxEjectionPercent: 50
    subsets:
      - name: v1
        labels:
          version: v1
      - name: v2
        labels:
          version: v2
        trafficPolicy:
          loadBalancer:
            simple: ROUND_ROBIN
```

---

## ArgoCD

### Application Resource

**File:** `templates/argocd-application.yaml`

```yaml
{{- if .Values.argocd.application.enabled }}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ include "mychart.fullname" . }}
  namespace: {{ .Values.argocd.application.namespace | default "argocd" }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.argocd.application.finalizers }}
  finalizers:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  project: {{ .Values.argocd.application.project | default "default" }}
  source:
    repoURL: {{ required "argocd.application.source.repoURL is required!" .Values.argocd.application.source.repoURL }}
    targetRevision: {{ .Values.argocd.application.source.targetRevision | default "HEAD" }}
    path: {{ .Values.argocd.application.source.path }}
    {{- with .Values.argocd.application.source.helm }}
    helm:
      {{- toYaml . | nindent 6 }}
    {{- end }}
  destination:
    server: {{ .Values.argocd.application.destination.server | default "https://kubernetes.default.svc" }}
    namespace: {{ .Values.argocd.application.destination.namespace | default .Release.Namespace }}
  syncPolicy:
    {{- with .Values.argocd.application.syncPolicy }}
    {{- toYaml . | nindent 4 }}
    {{- end }}
  {{- with .Values.argocd.application.ignoreDifferences }}
  ignoreDifferences:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
argocd:
  application:
    enabled: false
    namespace: argocd
    project: default
    finalizers:
      - resources-finalizer.argocd.argoproj.io
    source:
      repoURL: https://github.com/example/repo
      targetRevision: main
      path: charts/mychart
      helm:
        releaseName: mychart
        valueFiles:
          - values.yaml
        values: ""
    destination:
      server: https://kubernetes.default.svc
      namespace: default
    syncPolicy:
      automated:
        prune: true
        selfHeal: true
        allowEmpty: false
      syncOptions:
        - CreateNamespace=true
        - PruneLast=true
      retry:
        limit: 5
        backoff:
          duration: 5s
          factor: 2
          maxDuration: 3m
    ignoreDifferences: []
```

### AppProject Resource

**File:** `templates/argocd-appproject.yaml`

```yaml
{{- if .Values.argocd.appProject.enabled }}
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: {{ .Values.argocd.appProject.name }}
  namespace: {{ .Values.argocd.appProject.namespace | default "argocd" }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.argocd.appProject.finalizers }}
  finalizers:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  description: {{ .Values.argocd.appProject.description }}
  sourceRepos:
  {{- range .Values.argocd.appProject.sourceRepos }}
    - {{ . | quote }}
  {{- end }}
  destinations:
  {{- range .Values.argocd.appProject.destinations }}
  - namespace: {{ .namespace }}
    server: {{ .server }}
  {{- end }}
  {{- with .Values.argocd.appProject.clusterResourceWhitelist }}
  clusterResourceWhitelist:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.argocd.appProject.namespaceResourceWhitelist }}
  namespaceResourceWhitelist:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
argocd:
  appProject:
    enabled: false
    name: myproject
    namespace: argocd
    description: "My ArgoCD Project"
    finalizers:
      - resources-finalizer.argocd.argoproj.io
    sourceRepos:
      - '*'
    destinations:
      - namespace: '*'
        server: https://kubernetes.default.svc
    clusterResourceWhitelist:
      - group: '*'
        kind: '*'
    namespaceResourceWhitelist: []
```

---

## Sealed Secrets

### SealedSecret Resource

**File:** `templates/sealedsecret.yaml`

```yaml
{{- if .Values.sealedSecret.enabled }}
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  encryptedData:
    {{- range $key, $value := .Values.sealedSecret.encryptedData }}
    {{ $key }}: {{ $value }}
    {{- end }}
  template:
    metadata:
      name: {{ include "mychart.fullname" . }}
      labels:
        {{- include "mychart.labels" . | nindent 8 }}
    type: {{ .Values.sealedSecret.type | default "Opaque" }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
sealedSecret:
  enabled: false
  type: Opaque
  encryptedData: {}
    # API_KEY: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq...
    # DATABASE_PASSWORD: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq...
```

---

## External Secrets Operator

### ExternalSecret Resource

**File:** `templates/externalsecret.yaml`

```yaml
{{- if .Values.externalSecret.enabled }}
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  secretStoreRef:
    name: {{ .Values.externalSecret.secretStoreRef.name }}
    kind: {{ .Values.externalSecret.secretStoreRef.kind | default "SecretStore" }}
  target:
    name: {{ include "mychart.fullname" . }}
    {{- with .Values.externalSecret.target.creationPolicy }}
    creationPolicy: {{ . }}
    {{- end }}
    {{- with .Values.externalSecret.target.template }}
    template:
      {{- toYaml . | nindent 6 }}
    {{- end }}
  {{- with .Values.externalSecret.refreshInterval }}
  refreshInterval: {{ . }}
  {{- end }}
  {{- if .Values.externalSecret.data }}
  data:
  {{- range .Values.externalSecret.data }}
  - secretKey: {{ .secretKey }}
    remoteRef:
      key: {{ .remoteRef.key }}
      {{- with .remoteRef.property }}
      property: {{ . }}
      {{- end }}
      {{- with .remoteRef.version }}
      version: {{ . }}
      {{- end }}
  {{- end }}
  {{- end }}
  {{- if .Values.externalSecret.dataFrom }}
  dataFrom:
  {{- range .Values.externalSecret.dataFrom }}
  - extract:
      key: {{ .extract.key }}
      {{- with .extract.property }}
      property: {{ . }}
      {{- end }}
  {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
externalSecret:
  enabled: false
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    creationPolicy: Owner
    template:
      type: Opaque
  refreshInterval: 1h
  data:
    - secretKey: API_KEY
      remoteRef:
        key: secret/data/myapp
        property: api_key
    - secretKey: DATABASE_PASSWORD
      remoteRef:
        key: secret/data/myapp
        property: db_password
  dataFrom: []
  # dataFrom:
  #   - extract:
  #       key: secret/data/myapp
```

### SecretStore Resource

**File:** `templates/secretstore.yaml`

```yaml
{{- if .Values.externalSecret.secretStore.create }}
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: {{ .Values.externalSecret.secretStore.name }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  provider:
    {{- if .Values.externalSecret.secretStore.provider.vault }}
    vault:
      server: {{ .Values.externalSecret.secretStore.provider.vault.server }}
      path: {{ .Values.externalSecret.secretStore.provider.vault.path }}
      version: {{ .Values.externalSecret.secretStore.provider.vault.version | default "v2" }}
      auth:
        {{- toYaml .Values.externalSecret.secretStore.provider.vault.auth | nindent 8 }}
    {{- else if .Values.externalSecret.secretStore.provider.aws }}
    aws:
      service: {{ .Values.externalSecret.secretStore.provider.aws.service }}
      region: {{ .Values.externalSecret.secretStore.provider.aws.region }}
      {{- with .Values.externalSecret.secretStore.provider.aws.auth }}
      auth:
        {{- toYaml . | nindent 8 }}
      {{- end }}
    {{- else if .Values.externalSecret.secretStore.provider.gcpsm }}
    gcpsm:
      projectID: {{ .Values.externalSecret.secretStore.provider.gcpsm.projectID }}
      {{- with .Values.externalSecret.secretStore.provider.gcpsm.auth }}
      auth:
        {{- toYaml . | nindent 8 }}
      {{- end }}
    {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
externalSecret:
  secretStore:
    create: false
    name: vault-backend
    provider:
      vault:
        server: https://vault.example.com
        path: secret
        version: v2
        auth:
          kubernetes:
            mountPath: kubernetes
            role: myapp
            serviceAccountRef:
              name: mychart
      # aws:
      #   service: SecretsManager
      #   region: us-east-1
      #   auth:
      #     jwt:
      #       serviceAccountRef:
      #         name: mychart
      # gcpsm:
      #   projectID: my-project
      #   auth:
      #     workloadIdentity:
      #       clusterLocation: us-central1
      #       clusterName: my-cluster
      #       serviceAccountRef:
      #         name: mychart
```

---

## Gateway API

The Gateway API is the evolution of Kubernetes Ingress, providing more expressive and extensible routing capabilities. It's becoming the standard for north-south traffic management in Kubernetes.

### GatewayClass Resource

**File:** `templates/gatewayclass.yaml`

```yaml
{{- if .Values.gatewayAPI.gatewayClass.create }}
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: {{ .Values.gatewayAPI.gatewayClass.name }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.gatewayAPI.gatewayClass.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  controllerName: {{ required "gatewayAPI.gatewayClass.controllerName is required!" .Values.gatewayAPI.gatewayClass.controllerName }}
  {{- with .Values.gatewayAPI.gatewayClass.parametersRef }}
  parametersRef:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.gatewayAPI.gatewayClass.description }}
  description: {{ . | quote }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
gatewayAPI:
  gatewayClass:
    create: false
    name: my-gateway-class
    # Controller implementations:
    # - gateway.nginx.org/nginx-gateway-controller (NGINX Gateway Fabric)
    # - gateway.envoyproxy.io/gatewayclass-controller (Envoy Gateway)
    # - istio.io/gateway-controller (Istio)
    # - projectcontour.io/gateway-controller (Contour)
    # - traefik.io/gateway-controller (Traefik)
    controllerName: gateway.nginx.org/nginx-gateway-controller
    annotations: {}
    description: "Production gateway class"
    parametersRef: {}
    # parametersRef:
    #   group: gateway.nginx.org
    #   kind: NginxProxy
    #   name: nginx-proxy-config
```

### Gateway Resource

**File:** `templates/gateway.yaml`

```yaml
{{- if .Values.gatewayAPI.gateway.enabled }}
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: {{ include "mychart.fullname" . }}
  namespace: {{ .Values.gatewayAPI.gateway.namespace | default .Release.Namespace }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.gatewayAPI.gateway.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  gatewayClassName: {{ required "gatewayAPI.gateway.gatewayClassName is required!" .Values.gatewayAPI.gateway.gatewayClassName }}
  {{- with .Values.gatewayAPI.gateway.addresses }}
  addresses:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  listeners:
  {{- range .Values.gatewayAPI.gateway.listeners }}
  - name: {{ .name }}
    hostname: {{ .hostname | quote }}
    port: {{ .port }}
    protocol: {{ .protocol }}
    {{- with .tls }}
    tls:
      {{- toYaml . | nindent 6 }}
    {{- end }}
    {{- with .allowedRoutes }}
    allowedRoutes:
      {{- toYaml . | nindent 6 }}
    {{- end }}
  {{- end }}
  {{- with .Values.gatewayAPI.gateway.infrastructure }}
  infrastructure:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
gatewayAPI:
  gateway:
    enabled: false
    namespace: ""  # defaults to release namespace
    gatewayClassName: my-gateway-class
    annotations: {}
    addresses: []
    # addresses:
    #   - type: IPAddress
    #     value: 10.0.0.1
    listeners:
      - name: http
        hostname: "*.example.com"
        port: 80
        protocol: HTTP
        allowedRoutes:
          namespaces:
            from: Same
          kinds:
            - kind: HTTPRoute
      - name: https
        hostname: "*.example.com"
        port: 443
        protocol: HTTPS
        tls:
          mode: Terminate
          certificateRefs:
            - name: example-com-tls
              kind: Secret
        allowedRoutes:
          namespaces:
            from: Same
          kinds:
            - kind: HTTPRoute
    infrastructure: {}
    # infrastructure:
    #   labels:
    #     app: my-gateway
    #   annotations:
    #     service.beta.kubernetes.io/aws-load-balancer-type: nlb
```

### HTTPRoute Resource

**File:** `templates/httproute.yaml`

```yaml
{{- if .Values.gatewayAPI.httpRoute.enabled }}
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: {{ include "mychart.fullname" . }}
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.gatewayAPI.httpRoute.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- with .Values.gatewayAPI.httpRoute.parentRefs }}
  parentRefs:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.gatewayAPI.httpRoute.hostnames }}
  hostnames:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  rules:
  {{- range .Values.gatewayAPI.httpRoute.rules }}
  - {{- with .matches }}
    matches:
      {{- toYaml . | nindent 6 }}
    {{- end }}
    {{- with .filters }}
    filters:
      {{- toYaml . | nindent 6 }}
    {{- end }}
    backendRefs:
    {{- range .backendRefs }}
    - name: {{ .name | default (include "mychart.fullname" $) }}
      port: {{ .port | default $.Values.service.port }}
      {{- with .weight }}
      weight: {{ . }}
      {{- end }}
      {{- with .kind }}
      kind: {{ . }}
      {{- end }}
      {{- with .namespace }}
      namespace: {{ . }}
      {{- end }}
    {{- end }}
    {{- with .timeouts }}
    timeouts:
      {{- toYaml . | nindent 6 }}
    {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
gatewayAPI:
  httpRoute:
    enabled: false
    annotations: {}
    parentRefs:
      - name: my-gateway
        namespace: default
        sectionName: https
    hostnames:
      - app.example.com
    rules:
      # Simple routing to backend service
      - matches:
          - path:
              type: PathPrefix
              value: /
        backendRefs:
          - name: ""  # defaults to chart fullname
            port: 0   # defaults to service.port
            weight: 100

      # Path-based routing with multiple backends
      - matches:
          - path:
              type: PathPrefix
              value: /api
          - path:
              type: PathPrefix
              value: /v1
        backendRefs:
          - name: api-service
            port: 8080
            weight: 90
          - name: api-service-canary
            port: 8080
            weight: 10

      # Header-based routing
      - matches:
          - headers:
              - name: X-Version
                value: beta
        backendRefs:
          - name: beta-service
            port: 8080

      # Method-based routing
      - matches:
          - method: POST
            path:
              type: Exact
              value: /webhook
        backendRefs:
          - name: webhook-service
            port: 8080
        timeouts:
          request: 30s
```

### HTTPRoute with Filters

**File:** `templates/httproute-advanced.yaml`

```yaml
{{- if .Values.gatewayAPI.httpRouteAdvanced.enabled }}
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: {{ include "mychart.fullname" . }}-advanced
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  parentRefs:
    - name: {{ .Values.gatewayAPI.httpRouteAdvanced.gatewayRef }}
  hostnames:
    {{- range .Values.gatewayAPI.httpRouteAdvanced.hostnames }}
    - {{ . | quote }}
    {{- end }}
  rules:
  {{- if .Values.gatewayAPI.httpRouteAdvanced.redirectHttpToHttps }}
  # HTTP to HTTPS redirect
  - matches:
      - path:
          type: PathPrefix
          value: /
    filters:
      - type: RequestRedirect
        requestRedirect:
          scheme: https
          statusCode: 301
  {{- end }}
  {{- if .Values.gatewayAPI.httpRouteAdvanced.urlRewrite }}
  # URL rewrite
  - matches:
      - path:
          type: PathPrefix
          value: {{ .Values.gatewayAPI.httpRouteAdvanced.urlRewrite.matchPath }}
    filters:
      - type: URLRewrite
        urlRewrite:
          path:
            type: ReplacePrefixMatch
            replacePrefixMatch: {{ .Values.gatewayAPI.httpRouteAdvanced.urlRewrite.replacePath }}
    backendRefs:
      - name: {{ include "mychart.fullname" . }}
        port: {{ .Values.service.port }}
  {{- end }}
  {{- if .Values.gatewayAPI.httpRouteAdvanced.requestHeaderModifier }}
  # Request header modification
  - matches:
      - path:
          type: PathPrefix
          value: /
    filters:
      - type: RequestHeaderModifier
        requestHeaderModifier:
          {{- with .Values.gatewayAPI.httpRouteAdvanced.requestHeaderModifier.set }}
          set:
            {{- range . }}
            - name: {{ .name }}
              value: {{ .value | quote }}
            {{- end }}
          {{- end }}
          {{- with .Values.gatewayAPI.httpRouteAdvanced.requestHeaderModifier.add }}
          add:
            {{- range . }}
            - name: {{ .name }}
              value: {{ .value | quote }}
            {{- end }}
          {{- end }}
          {{- with .Values.gatewayAPI.httpRouteAdvanced.requestHeaderModifier.remove }}
          remove:
            {{- toYaml . | nindent 12 }}
          {{- end }}
    backendRefs:
      - name: {{ include "mychart.fullname" . }}
        port: {{ .Values.service.port }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
gatewayAPI:
  httpRouteAdvanced:
    enabled: false
    gatewayRef: my-gateway
    hostnames:
      - app.example.com

    # HTTP to HTTPS redirect
    redirectHttpToHttps: false

    # URL rewrite configuration
    urlRewrite:
      matchPath: /old-api
      replacePath: /api/v2

    # Request header modification
    requestHeaderModifier:
      set:
        - name: X-Forwarded-Proto
          value: https
      add:
        - name: X-Request-ID
          value: "{{ .Release.Name }}"
      remove:
        - X-Internal-Header
```

### GRPCRoute Resource

**File:** `templates/grpcroute.yaml`

```yaml
{{- if .Values.gatewayAPI.grpcRoute.enabled }}
apiVersion: gateway.networking.k8s.io/v1
kind: GRPCRoute
metadata:
  name: {{ include "mychart.fullname" . }}-grpc
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  parentRefs:
    {{- range .Values.gatewayAPI.grpcRoute.parentRefs }}
    - name: {{ .name }}
      {{- with .namespace }}
      namespace: {{ . }}
      {{- end }}
      {{- with .sectionName }}
      sectionName: {{ . }}
      {{- end }}
    {{- end }}
  {{- with .Values.gatewayAPI.grpcRoute.hostnames }}
  hostnames:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  rules:
  {{- range .Values.gatewayAPI.grpcRoute.rules }}
  - {{- with .matches }}
    matches:
      {{- toYaml . | nindent 6 }}
    {{- end }}
    backendRefs:
    {{- range .backendRefs }}
    - name: {{ .name }}
      port: {{ .port }}
      {{- with .weight }}
      weight: {{ . }}
      {{- end }}
    {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
gatewayAPI:
  grpcRoute:
    enabled: false
    parentRefs:
      - name: my-gateway
        sectionName: grpc
    hostnames:
      - grpc.example.com
    rules:
      # Route all gRPC traffic
      - backendRefs:
          - name: grpc-service
            port: 50051
            weight: 100

      # Method-specific routing
      - matches:
          - method:
              service: myservice.MyService
              method: MyMethod
        backendRefs:
          - name: grpc-service-v2
            port: 50051
```

### ReferenceGrant Resource

**File:** `templates/referencegrant.yaml`

```yaml
{{- if .Values.gatewayAPI.referenceGrant.enabled }}
apiVersion: gateway.networking.k8s.io/v1
kind: ReferenceGrant
metadata:
  name: {{ include "mychart.fullname" . }}-grant
  namespace: {{ .Values.gatewayAPI.referenceGrant.namespace | default .Release.Namespace }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  from:
  {{- range .Values.gatewayAPI.referenceGrant.from }}
  - group: {{ .group }}
    kind: {{ .kind }}
    namespace: {{ .namespace }}
  {{- end }}
  to:
  {{- range .Values.gatewayAPI.referenceGrant.to }}
  - group: {{ .group | default "" | quote }}
    kind: {{ .kind }}
    {{- with .name }}
    name: {{ . }}
    {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
gatewayAPI:
  referenceGrant:
    enabled: false
    namespace: ""  # defaults to release namespace
    # Allow Gateway in gateway-ns to reference Secrets in this namespace
    from:
      - group: gateway.networking.k8s.io
        kind: Gateway
        namespace: gateway-ns
    to:
      - group: ""
        kind: Secret
        # name: specific-secret  # optional: restrict to specific secret
```

---

## KEDA

KEDA (Kubernetes Event-driven Autoscaling) provides event-driven autoscaling for Kubernetes workloads. It can scale based on events from various sources like message queues, databases, HTTP requests, and more.

### ScaledObject Resource

**File:** `templates/scaledobject.yaml`

```yaml
{{- if .Values.keda.enabled }}
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.keda.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  scaleTargetRef:
    apiVersion: {{ .Values.keda.scaleTargetRef.apiVersion | default "apps/v1" }}
    kind: {{ .Values.keda.scaleTargetRef.kind | default "Deployment" }}
    name: {{ .Values.keda.scaleTargetRef.name | default (include "mychart.fullname" .) }}
    {{- with .Values.keda.scaleTargetRef.envSourceContainerName }}
    envSourceContainerName: {{ . }}
    {{- end }}
  pollingInterval: {{ .Values.keda.pollingInterval | default 30 }}
  cooldownPeriod: {{ .Values.keda.cooldownPeriod | default 300 }}
  {{- with .Values.keda.idleReplicaCount }}
  idleReplicaCount: {{ . }}
  {{- end }}
  minReplicaCount: {{ .Values.keda.minReplicaCount | default 0 }}
  maxReplicaCount: {{ .Values.keda.maxReplicaCount | default 100 }}
  {{- with .Values.keda.fallback }}
  fallback:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.keda.advanced }}
  advanced:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  triggers:
  {{- range .Values.keda.triggers }}
  - type: {{ .type }}
    {{- with .name }}
    name: {{ . }}
    {{- end }}
    metadata:
      {{- range $key, $value := .metadata }}
      {{ $key }}: {{ $value | quote }}
      {{- end }}
    {{- with .authenticationRef }}
    authenticationRef:
      {{- toYaml . | nindent 6 }}
    {{- end }}
    {{- with .metricType }}
    metricType: {{ . }}
    {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
keda:
  enabled: false
  annotations: {}
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ""  # defaults to chart fullname
    envSourceContainerName: ""  # optional: container to source env from
  pollingInterval: 30  # seconds
  cooldownPeriod: 300  # seconds
  idleReplicaCount: 0  # scale to 0 when idle (optional)
  minReplicaCount: 1
  maxReplicaCount: 10
  fallback:
    failureThreshold: 3
    replicas: 2
  advanced:
    restoreToOriginalReplicaCount: true
    horizontalPodAutoscalerConfig:
      name: ""  # custom HPA name
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
            - type: Percent
              value: 100
              periodSeconds: 15
  triggers:
    # CPU-based scaling
    - type: cpu
      metricType: Utilization
      metadata:
        value: "80"

    # Memory-based scaling
    - type: memory
      metricType: Utilization
      metadata:
        value: "80"

    # Prometheus metrics
    - type: prometheus
      metadata:
        serverAddress: http://prometheus:9090
        metricName: http_requests_total
        query: sum(rate(http_requests_total{deployment="mychart"}[2m]))
        threshold: "100"

    # RabbitMQ queue length
    - type: rabbitmq
      metadata:
        host: amqp://rabbitmq:5672
        queueName: myqueue
        queueLength: "50"
      authenticationRef:
        name: rabbitmq-auth

    # Kafka consumer lag
    - type: kafka
      metadata:
        bootstrapServers: kafka:9092
        consumerGroup: my-group
        topic: my-topic
        lagThreshold: "100"

    # Redis list length
    - type: redis
      metadata:
        address: redis:6379
        listName: mylist
        listLength: "10"

    # AWS SQS queue
    - type: aws-sqs-queue
      metadata:
        queueURL: https://sqs.us-east-1.amazonaws.com/123456789/myqueue
        queueLength: "50"
        awsRegion: us-east-1
      authenticationRef:
        name: aws-credentials

    # Cron-based scaling
    - type: cron
      metadata:
        timezone: America/New_York
        start: "0 8 * * 1-5"  # 8 AM weekdays
        end: "0 18 * * 1-5"   # 6 PM weekdays
        desiredReplicas: "10"
```

### ScaledJob Resource

**File:** `templates/scaledjob.yaml`

```yaml
{{- if .Values.keda.scaledJob.enabled }}
apiVersion: keda.sh/v1alpha1
kind: ScaledJob
metadata:
  name: {{ include "mychart.fullname" . }}-job
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  jobTargetRef:
    parallelism: {{ .Values.keda.scaledJob.parallelism | default 1 }}
    completions: {{ .Values.keda.scaledJob.completions | default 1 }}
    activeDeadlineSeconds: {{ .Values.keda.scaledJob.activeDeadlineSeconds | default 600 }}
    backoffLimit: {{ .Values.keda.scaledJob.backoffLimit | default 6 }}
    template:
      spec:
        {{- with .Values.imagePullSecrets }}
        imagePullSecrets:
          {{- toYaml . | nindent 10 }}
        {{- end }}
        restartPolicy: {{ .Values.keda.scaledJob.restartPolicy | default "Never" }}
        containers:
        - name: {{ .Chart.Name }}-job
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          {{- with .Values.keda.scaledJob.command }}
          command:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.keda.scaledJob.args }}
          args:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- with .Values.keda.scaledJob.env }}
          env:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          resources:
            {{- toYaml .Values.keda.scaledJob.resources | nindent 12 }}
  pollingInterval: {{ .Values.keda.scaledJob.pollingInterval | default 30 }}
  successfulJobsHistoryLimit: {{ .Values.keda.scaledJob.successfulJobsHistoryLimit | default 5 }}
  failedJobsHistoryLimit: {{ .Values.keda.scaledJob.failedJobsHistoryLimit | default 5 }}
  maxReplicaCount: {{ .Values.keda.scaledJob.maxReplicaCount | default 100 }}
  scalingStrategy:
    strategy: {{ .Values.keda.scaledJob.scalingStrategy | default "default" }}
  triggers:
  {{- range .Values.keda.scaledJob.triggers }}
  - type: {{ .type }}
    metadata:
      {{- range $key, $value := .metadata }}
      {{ $key }}: {{ $value | quote }}
      {{- end }}
    {{- with .authenticationRef }}
    authenticationRef:
      {{- toYaml . | nindent 6 }}
    {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
keda:
  scaledJob:
    enabled: false
    parallelism: 1
    completions: 1
    activeDeadlineSeconds: 600
    backoffLimit: 6
    restartPolicy: Never
    pollingInterval: 30
    successfulJobsHistoryLimit: 5
    failedJobsHistoryLimit: 5
    maxReplicaCount: 100
    scalingStrategy: default  # default, custom, accurate
    command: []
    args: []
    env: []
    resources:
      limits:
        cpu: 100m
        memory: 128Mi
      requests:
        cpu: 100m
        memory: 128Mi
    triggers:
      - type: aws-sqs-queue
        metadata:
          queueURL: https://sqs.us-east-1.amazonaws.com/123456789/myqueue
          queueLength: "5"
          awsRegion: us-east-1
```

### TriggerAuthentication Resource

**File:** `templates/triggerauthentication.yaml`

```yaml
{{- if .Values.keda.authentication.enabled }}
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: {{ include "mychart.fullname" . }}-auth
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  {{- with .Values.keda.authentication.secretTargetRef }}
  secretTargetRef:
    {{- range . }}
    - parameter: {{ .parameter }}
      name: {{ .name }}
      key: {{ .key }}
    {{- end }}
  {{- end }}
  {{- with .Values.keda.authentication.env }}
  env:
    {{- range . }}
    - parameter: {{ .parameter }}
      name: {{ .name }}
      {{- with .containerName }}
      containerName: {{ . }}
      {{- end }}
    {{- end }}
  {{- end }}
  {{- with .Values.keda.authentication.podIdentity }}
  podIdentity:
    provider: {{ .provider }}
    {{- with .identityId }}
    identityId: {{ . }}
    {{- end }}
  {{- end }}
  {{- with .Values.keda.authentication.hashiCorpVault }}
  hashiCorpVault:
    address: {{ .address }}
    authentication: {{ .authentication }}
    {{- with .role }}
    role: {{ . }}
    {{- end }}
    {{- with .mount }}
    mount: {{ . }}
    {{- end }}
    credential:
      {{- toYaml .credential | nindent 6 }}
    secrets:
      {{- range .secrets }}
      - parameter: {{ .parameter }}
        key: {{ .key }}
        path: {{ .path }}
      {{- end }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
keda:
  authentication:
    enabled: false
    # Secret-based authentication
    secretTargetRef:
      - parameter: connection
        name: rabbitmq-secret
        key: connectionString
      - parameter: password
        name: db-secret
        key: password

    # Environment variable authentication
    env:
      - parameter: awsAccessKeyID
        name: AWS_ACCESS_KEY_ID
      - parameter: awsSecretAccessKey
        name: AWS_SECRET_ACCESS_KEY

    # Pod identity (Azure, AWS IRSA, GCP Workload Identity)
    podIdentity:
      provider: azure  # azure, aws-eks, gcp
      identityId: ""  # optional: specific identity

    # HashiCorp Vault authentication
    hashiCorpVault:
      address: https://vault.example.com
      authentication: token  # token, kubernetes
      role: my-role
      mount: secret
      credential:
        token: vault-token  # or serviceAccount for kubernetes auth
      secrets:
        - parameter: connection
          key: connectionString
          path: secret/data/myapp
```

---

## VerticalPodAutoscaler (VPA)

The VerticalPodAutoscaler automatically adjusts the CPU and memory reservations for pods to help "right-size" your applications.

### VerticalPodAutoscaler Resource

**File:** `templates/vpa.yaml`

```yaml
{{- if .Values.vpa.enabled }}
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.vpa.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  targetRef:
    apiVersion: {{ .Values.vpa.targetRef.apiVersion | default "apps/v1" }}
    kind: {{ .Values.vpa.targetRef.kind | default "Deployment" }}
    name: {{ .Values.vpa.targetRef.name | default (include "mychart.fullname" .) }}
  updatePolicy:
    updateMode: {{ .Values.vpa.updatePolicy.updateMode | default "Auto" }}
    {{- with .Values.vpa.updatePolicy.minReplicas }}
    minReplicas: {{ . }}
    {{- end }}
  {{- with .Values.vpa.resourcePolicy }}
  resourcePolicy:
    containerPolicies:
    {{- range .containerPolicies }}
    - containerName: {{ .containerName | default "*" }}
      {{- with .mode }}
      mode: {{ . }}
      {{- end }}
      {{- with .minAllowed }}
      minAllowed:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .maxAllowed }}
      maxAllowed:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .controlledResources }}
      controlledResources:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .controlledValues }}
      controlledValues: {{ . }}
      {{- end }}
    {{- end }}
  {{- end }}
  {{- with .Values.vpa.recommenders }}
  recommenders:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
vpa:
  enabled: false
  annotations: {}
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ""  # defaults to chart fullname
  updatePolicy:
    # Auto - VPA assigns resource requests on pod creation and updates on existing pods
    # Recreate - VPA assigns resource requests on pod creation and kills existing pods
    # Initial - VPA only assigns requests on pod creation, never updates
    # Off - VPA does not update pods, only provides recommendations
    updateMode: "Auto"
    minReplicas: 1  # minimum replicas for VPA to act on
  resourcePolicy:
    containerPolicies:
      # Apply to all containers
      - containerName: "*"
        minAllowed:
          cpu: 50m
          memory: 64Mi
        maxAllowed:
          cpu: 2
          memory: 4Gi
        controlledResources:
          - cpu
          - memory
        controlledValues: RequestsAndLimits  # RequestsOnly or RequestsAndLimits

      # Specific container policy
      - containerName: my-container
        mode: Auto  # Auto or Off
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 1
          memory: 2Gi

  # Custom recommenders (optional, requires VPA 0.11+)
  recommenders:
    - name: custom-recommender
```

### VPA with Recommendation Only

For applications where you want VPA recommendations without automatic updates:

**File:** `templates/vpa-recommendation.yaml`

```yaml
{{- if .Values.vpa.recommendationOnly.enabled }}
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: {{ include "mychart.fullname" . }}-recommendation
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
    vpa-mode: recommendation-only
spec:
  targetRef:
    apiVersion: apps/v1
    kind: {{ .Values.vpa.recommendationOnly.kind | default "Deployment" }}
    name: {{ include "mychart.fullname" . }}
  updatePolicy:
    updateMode: "Off"
  resourcePolicy:
    containerPolicies:
    - containerName: "*"
      minAllowed:
        cpu: {{ .Values.vpa.recommendationOnly.minCpu | default "25m" }}
        memory: {{ .Values.vpa.recommendationOnly.minMemory | default "32Mi" }}
      maxAllowed:
        cpu: {{ .Values.vpa.recommendationOnly.maxCpu | default "4" }}
        memory: {{ .Values.vpa.recommendationOnly.maxMemory | default "8Gi" }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
vpa:
  recommendationOnly:
    enabled: false
    kind: Deployment
    minCpu: 25m
    minMemory: 32Mi
    maxCpu: 4
    maxMemory: 8Gi
```

---

## General Best Practices

### 1. Conditional Resource Creation

Always wrap CRD resources in conditional blocks:

```yaml
{{- if .Values.certificate.enabled }}
# CRD resource
{{- end }}
```

### 2. Required Values

Use `required` for critical CRD fields:

```yaml
email: {{ required "certManager.clusterIssuer.acme.email is required!" .Values.certManager.clusterIssuer.acme.email }}
```

### 3. Documentation

Document CRD dependencies in Chart.yaml:

```yaml
annotations:
  operatorDependencies: |
    - name: cert-manager
      version: ">=1.12.0"
      url: https://cert-manager.io/docs/installation/
```

### 4. Default Values

Provide sensible defaults for all CRD fields:

```yaml
certificate:
  enabled: false
  duration: 2160h
  renewBefore: 360h
```

### 5. Version Awareness

Be explicit about API versions:

```yaml
apiVersion: cert-manager.io/v1  # Not v1alpha1 or v1beta1
```

### 6. Helper Usage

Use chart helpers for consistent labeling:

```yaml
metadata:
  name: {{ include "mychart.fullname" . }}-tls
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
```

### 7. Testing

Always test CRD resources with:
- `helm template` to verify rendering
- `helm lint` to check syntax
- `kubectl apply --dry-run=server` to validate against cluster

---

## Resources

- [cert-manager Documentation](https://cert-manager.io/docs/)
- [Prometheus Operator](https://prometheus-operator.dev/)
- [Istio Documentation](https://istio.io/latest/docs/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Sealed Secrets](https://sealed-secrets.netlify.app/)
- [External Secrets Operator](https://external-secrets.io/)
- [Gateway API Documentation](https://gateway-api.sigs.k8s.io/)
- [KEDA Documentation](https://keda.sh/docs/)
- [VerticalPodAutoscaler Documentation](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler)

---

## Reference: Helm_Template_Functions

# Helm Template Functions Reference

Comprehensive guide to Helm template functions with practical examples.

## Essential Template Functions

### 1. required - Enforce Required Values

Fails template rendering if a value is not provided.

```yaml
# Syntax
{{ required "error message" .Values.some.value }}

# Example
image: {{ required "image.repository is required!" .Values.image.repository }}
tag: {{ required "image.tag is required!" .Values.image.tag }}
```

**When to use:**
- Critical configuration values that must be set
- Values without sensible defaults
- Production deployments where safety is paramount

### 2. default - Provide Fallback Values

Provides a default value if the value is empty or undefined.

```yaml
# Syntax
{{ .Values.some.value | default "default-value" }}

# Examples
replicas: {{ .Values.replicaCount | default 1 }}
image:
  tag: {{ .Values.image.tag | default .Chart.AppVersion }}
  pullPolicy: {{ .Values.image.pullPolicy | default "IfNotPresent" }}

# Computed defaults
serviceName: {{ .Values.service.name | default (printf "%s-svc" (include "mychart.fullname" .)) }}
```

**When to use:**
- Optional configuration values
- Values with sensible defaults
- Fallback to computed values

### 3. quote - Safely Quote Strings

Wraps a value in double quotes, escaping special characters.

```yaml
# Syntax
{{ .Values.some.value | quote }}

# Examples
env:
  - name: DATABASE_URL
    value: {{ .Values.database.url | quote }}
  - name: API_KEY
    value: {{ .Values.api.key | quote }}

# With pipeline
image: {{ .Values.image.repository | default "nginx" | quote }}
```

**When to use:**
- String values in environment variables
- Configuration values that might contain special characters
- YAML string fields that need guaranteed quoting

### 4. include - Include Templates with Pipeline Support

Includes a named template and allows piping the result to other functions.

```yaml
# Syntax
{{ include "template-name" context }}

# Examples
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}

# With modifications
annotations:
  checksum: {{ include "mychart.config" . | sha256sum }}
```

**When to use:**
- Including helpers or named templates
- When you need to pipe template output to other functions
- Prefer `include` over `template` for better composability

### 5. template - Include Templates (No Pipeline)

Includes a named template (cannot be piped).

```yaml
# Syntax
{{ template "template-name" context }}

# Example
metadata:
  labels:
    {{ template "mychart.labels" . }}
```

**When to use:**
- Simple template inclusion without modification
- Legacy templates (prefer `include` for new code)

### 6. toYaml - Convert to YAML

Converts an object to YAML format.

```yaml
# Syntax
{{ .Values.some.object | toYaml }}

# Examples
{{- with .Values.resources }}
resources:
  {{- toYaml . | nindent 2 }}
{{- end }}

{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

**When to use:**
- Complex nested objects from values.yaml
- Resource specifications (limits, requests)
- Selector, affinity, and toleration definitions

### 7. fromYaml - Parse YAML String

Parses a YAML string into an object.

```yaml
# Syntax
{{ .Values.yamlString | fromYaml }}

# Example
{{- $config := .Values.configYaml | fromYaml }}
{{- if $config.enabled }}
# Use $config values
{{- end }}
```

**When to use:**
- Parsing YAML strings from values
- Dynamic configuration loading

### 8. tpl - Render String as Template

Evaluates a string as a Go template.

```yaml
# Syntax
{{ tpl .Values.templateString . }}

# Example values.yaml
config:
  message: "Release: {{ .Release.Name }}"

# Template
data:
  message: {{ tpl .Values.config.message . }}
```

**When to use:**
- Dynamic template strings in values.yaml
- User-provided template content
- Advanced configuration patterns

### 9. nindent / indent - Control Indentation

Adds newline and indentation, or just indentation.

```yaml
# nindent - newline + indent
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}

# indent - just indent (no newline)
data:
  config: |
    {{ .Values.config | indent 4 }}
```

**When to use:**
- `nindent` for YAML blocks after keys
- `indent` for multi-line string content

### 10. printf - Format Strings

Formats a string using Go's fmt.Sprintf syntax.

```yaml
# Syntax
{{ printf "format" arg1 arg2 }}

# Examples
name: {{ printf "%s-%s" .Release.Name .Chart.Name }}
label: {{ printf "app.kubernetes.io/name: %s" .Chart.Name }}
```

**When to use:**
- Constructing names or identifiers
- String formatting and concatenation

## Logical Functions

### if / else / else if - Conditionals

```yaml
{{- if .Values.ingress.enabled }}
# Ingress resource
{{- end }}

{{- if eq .Values.service.type "LoadBalancer" }}
# LoadBalancer config
{{- else if eq .Values.service.type "NodePort" }}
# NodePort config
{{- else }}
# Default config
{{- end }}
```

### and / or / not - Boolean Logic

```yaml
{{- if and .Values.enabled (not .Values.debug) }}
# Enabled and not debug
{{- end }}

{{- if or .Values.useSSL .Values.production }}
# SSL or production
{{- end }}
```

### with - Scope Context

```yaml
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

**Note:** Inside `with`, `.` refers to the scoped value. Use `$` for root context.

## Comparison Functions

- `eq` - Equal: `{{ if eq .Values.env "prod" }}`
- `ne` - Not equal: `{{ if ne .Values.replicas 1 }}`
- `lt` - Less than: `{{ if lt .Values.replicas 3 }}`
- `le` - Less or equal: `{{ if le .Values.replicas 5 }}`
- `gt` - Greater than: `{{ if gt .Values.replicas 1 }}`
- `ge` - Greater or equal: `{{ if ge .Values.replicas 3 }}`

## String Functions (Sprig)

### Basic String Operations

```yaml
# upper / lower
name: {{ .Values.name | upper }}
label: {{ .Values.env | lower }}

# trim / trimSuffix / trimPrefix
name: {{ .Values.name | trim }}
name: {{ .Values.name | trimSuffix "-" }}

# trunc - truncate to length
name: {{ .Values.longName | trunc 63 | trimSuffix "-" }}

# replace
chart: {{ .Chart.Name | replace "." "-" }}

# contains
{{- if contains "prod" .Values.environment }}
# Production settings
{{- end }}
```

### String Testing

```yaml
# hasPrefix / hasSuffix
{{- if hasPrefix "prod-" .Values.name }}

# empty - test if value is empty
{{- if not (empty .Values.optional) }}
```

## List Functions (Sprig)

### list - Create Lists

```yaml
{{- $myList := list "item1" "item2" "item3" }}
```

### append / prepend

```yaml
{{- $list := list "a" "b" }}
{{- $list = append $list "c" }}
{{- $list = prepend $list "z" }}
```

### first / rest / last / initial

```yaml
first: {{ first .Values.items }}
last: {{ last .Values.items }}
```

### has - Check Membership

```yaml
{{- if has "production" .Values.environments }}
```

## Dict/Map Functions (Sprig)

### dict - Create Dictionary

```yaml
{{- $myDict := dict "key1" "value1" "key2" "value2" }}
{{- include "mychart.helper" $myDict }}
```

### set / unset

```yaml
{{- $_ := set .Values "newKey" "newValue" }}
{{- $_ := unset .Values "oldKey" }}
```

### hasKey

```yaml
{{- if hasKey .Values "optional" }}
```

### merge - Merge Dictionaries

```yaml
{{- $merged := merge .Values.override .Values.defaults }}
```

## Type Functions

### typeOf / kindOf

```yaml
{{- $type := typeOf .Values.someValue }}
```

### int / int64 / float64 / toString

```yaml
port: {{ .Values.port | int }}
cpu: {{ .Values.cpu | toString }}
```

## Crypto Functions

### sha256sum - SHA-256 Hash

```yaml
annotations:
  checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
```

### b64enc / b64dec - Base64

```yaml
data:
  password: {{ .Values.password | b64enc }}
```

## Date Functions

### now - Current Time

```yaml
annotations:
  timestamp: {{ now | date "2006-01-02T15:04:05Z07:00" }}
```

### date - Format Date

```yaml
date: {{ now | date "2006-01-02" }}
```

## Regex Functions

### regexMatch / regexFind / regexReplace

```yaml
{{- if regexMatch "^prod-" .Values.name }}

{{- $version := .Values.image.tag | regexFind "[0-9]+" }}

label: {{ .Values.name | regexReplaceAll "[^a-z0-9-]" "-" }}
```

## Flow Control Functions

### range - Iterate

```yaml
# Range over list
{{- range .Values.items }}
- {{ . }}
{{- end }}

# Range over map
{{- range $key, $value := .Values.config }}
{{ $key }}: {{ $value }}
{{- end }}

# Range with index
{{- range $index, $item := .Values.items }}
{{ $index }}: {{ $item }}
{{- end }}
```

## Lookup Function (Cluster Queries)

Query existing Kubernetes resources (use with caution).

```yaml
{{- $secret := lookup "v1" "Secret" .Release.Namespace "my-secret" }}
{{- if $secret }}
# Secret exists
data:
  password: {{ $secret.data.password }}
{{- else }}
# Create new secret
{{- end }}
```

**⚠️ Warning:** `lookup` queries the cluster, which:
- Breaks the declarative model
- May cause issues with `helm template`
- Can lead to non-reproducible builds
- Should be used sparingly

## Best Practices

### 1. Validation First

```yaml
# Validate required values
name: {{ required "name is required" .Values.name }}
port: {{ required "port is required" .Values.port }}
```

### 2. Provide Defaults

```yaml
# Always provide sensible defaults
replicas: {{ .Values.replicaCount | default 1 }}
image:
  pullPolicy: {{ .Values.image.pullPolicy | default "IfNotPresent" }}
```

### 3. Quote Strings

```yaml
# Quote string values in env vars and annotations
env:
  - name: DATABASE_URL
    value: {{ .Values.database.url | quote }}
```

### 4. Use include Over template

```yaml
# Prefer include for composability
labels:
  {{- include "mychart.labels" . | nindent 2 }}

# Not: {{ template "mychart.labels" . }}
```

### 5. Use toYaml for Complex Objects

```yaml
# Let toYaml handle complex structures
{{- with .Values.resources }}
resources:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

### 6. Proper Indentation

```yaml
# Use nindent for YAML blocks
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}

# Use indent for multi-line strings
data:
  config: |
    {{ .Values.config | indent 4 }}
```

### 7. Whitespace Control

```yaml
# Use {{- and -}} to control whitespace
{{- if .Values.enabled }}
  content
{{- end }}
```

### 8. Fail Fast with required

```yaml
# Fail early if critical values missing
database:
  host: {{ required "database.host is required!" .Values.database.host }}
```

## Common Patterns

### ConfigMap Checksum

Trigger pod restart when ConfigMap changes:

```yaml
annotations:
  checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
```

### Conditional Resource Creation

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
# ...
{{- end }}
```

### Dynamic Names

```yaml
name: {{ include "mychart.fullname" . }}
serviceName: {{ include "mychart.fullname" . }}-svc
```

### Passing Custom Context

```yaml
{{- include "mychart.container" (dict "root" . "container" .Values.mainContainer) }}
```

Then in helper:

```yaml
{{- define "mychart.container" -}}
{{- $root := .root }}
{{- $container := .container }}
name: {{ $container.name }}
image: {{ $container.image }}
namespace: {{ $root.Release.Namespace }}
{{- end }}
```

## Resources

- [Helm Template Functions](https://helm.sh/docs/chart_template_guide/function_list/)
- [Sprig Function Library](https://masterminds.github.io/sprig/)
- [Go Template Documentation](https://pkg.go.dev/text/template)

---

## Reference: Resource_Templates

# Kubernetes Resource Templates for Helm

Reference templates for common Kubernetes resources with Helm templating.

## Table of Contents

- [Workload Resources](#workload-resources)
  - [Deployment](#deployment)
  - [StatefulSet](#statefulset)
  - [DaemonSet](#daemonset)
  - [Job](#job)
  - [CronJob](#cronjob)
- [Service Resources](#service-resources)
  - [Service](#service)
  - [Ingress](#ingress)
- [Configuration Resources](#configuration-resources)
  - [ConfigMap](#configmap)
  - [Secret](#secret)
- [Storage Resources](#storage-resources)
  - [PersistentVolumeClaim](#persistentvolumeclaim)
- [RBAC Resources](#rbac-resources)
  - [ServiceAccount](#serviceaccount)
  - [Role](#role)
  - [RoleBinding](#rolebinding)
  - [ClusterRole](#clusterrole)
  - [ClusterRoleBinding](#clusterrolebinding)
- [Network Resources](#network-resources)
  - [NetworkPolicy](#networkpolicy)
- [Autoscaling Resources](#autoscaling-resources)
  - [HorizontalPodAutoscaler](#horizontalpodautoscaler)
  - [PodDisruptionBudget](#poddisruptionbudget)

---

## Workload Resources

### Deployment

**File:** `templates/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.deployment.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  {{- with .Values.deployment.strategy }}
  strategy:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
        {{- if .Values.configMap }}
        {{- if .Values.configMap.enabled }}
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- end }}
        {{- end }}
        {{- if .Values.secret }}
        {{- if .Values.secret.enabled }}
        checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
        {{- end }}
        {{- end }}
      labels:
        {{- include "mychart.labels" . | nindent 8 }}
        {{- with .Values.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "mychart.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      {{- with .Values.initContainers }}
      initContainers:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 12 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        {{- with .Values.command }}
        command:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        {{- with .Values.args }}
        args:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        {{- range .Values.extraPorts }}
        - name: {{ .name }}
          containerPort: {{ .containerPort }}
          protocol: {{ .protocol | default "TCP" }}
        {{- end }}
        {{- with .Values.livenessProbe }}
        livenessProbe:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        {{- with .Values.readinessProbe }}
        readinessProbe:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        {{- with .Values.startupProbe }}
        startupProbe:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        {{- with .Values.env }}
        env:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        {{- with .Values.envFrom }}
        envFrom:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        {{- with .Values.volumeMounts }}
        volumeMounts:
          {{- toYaml . | nindent 12 }}
        {{- end }}
      {{- with .Values.sidecars }}
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.volumes }}
      volumes:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.priorityClassName }}
      priorityClassName: {{ . }}
      {{- end }}
```

**Corresponding values.yaml:**

```yaml
replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: ""

imagePullSecrets: []

deployment:
  annotations: {}
  strategy: {}
    # type: RollingUpdate
    # rollingUpdate:
    #   maxSurge: 1
    #   maxUnavailable: 0

podAnnotations: {}
podLabels: {}

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true

service:
  targetPort: 8080

extraPorts: []

command: []
args: []

livenessProbe:
  httpGet:
    path: /healthz
    port: http
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5

startupProbe: {}

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi

env: []
envFrom: []

volumeMounts: []
volumes: []

initContainers: []
sidecars: []

nodeSelector: {}
affinity: {}
tolerations: []
priorityClassName: ""
```

---

### StatefulSet

**File:** `templates/statefulset.yaml`

```yaml
{{- if eq .Values.workloadType "StatefulSet" }}
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  serviceName: {{ include "mychart.fullname" . }}-headless
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  {{- with .Values.statefulset.updateStrategy }}
  updateStrategy:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.statefulset.podManagementPolicy }}
  podManagementPolicy: {{ . }}
  {{- end }}
  template:
    metadata:
      annotations:
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
        {{- if .Values.configMap }}
        {{- if .Values.configMap.enabled }}
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- end }}
        {{- end }}
        {{- if .Values.secret }}
        {{- if .Values.secret.enabled }}
        checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
        {{- end }}
        {{- end }}
      labels:
        {{- include "mychart.labels" . | nindent 8 }}
        {{- with .Values.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "mychart.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 12 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        volumeMounts:
        - name: data
          mountPath: {{ .Values.persistence.mountPath }}
        {{- with .Values.volumeMounts }}
          {{- toYaml . | nindent 12 }}
        {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
  {{- if .Values.persistence.enabled }}
  volumeClaimTemplates:
  - metadata:
      name: data
      {{- with .Values.persistence.annotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
    spec:
      accessModes:
        {{- range .Values.persistence.accessModes }}
        - {{ . | quote }}
        {{- end }}
      {{- with .Values.persistence.storageClass }}
      storageClassName: {{ . }}
      {{- end }}
      resources:
        requests:
          storage: {{ .Values.persistence.size }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
workloadType: StatefulSet

statefulset:
  updateStrategy:
    type: RollingUpdate
  podManagementPolicy: OrderedReady

persistence:
  enabled: true
  accessModes:
    - ReadWriteOnce
  size: 10Gi
  storageClass: ""
  mountPath: /data
  annotations: {}
```

---

### DaemonSet

**File:** `templates/daemonset.yaml`

```yaml
{{- if eq .Values.workloadType "DaemonSet" }}
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  {{- with .Values.daemonset.updateStrategy }}
  updateStrategy:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  template:
    metadata:
      annotations:
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
        {{- if .Values.configMap }}
        {{- if .Values.configMap.enabled }}
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- end }}
        {{- end }}
        {{- if .Values.secret }}
        {{- if .Values.secret.enabled }}
        checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
        {{- end }}
        {{- end }}
      labels:
        {{- include "mychart.labels" . | nindent 8 }}
        {{- with .Values.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "mychart.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      hostNetwork: {{ .Values.daemonset.hostNetwork }}
      {{- if .Values.daemonset.hostPID }}
      hostPID: true
      {{- end }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 12 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        volumeMounts:
        - name: host
          mountPath: /host
          readOnly: true
        {{- with .Values.volumeMounts }}
          {{- toYaml . | nindent 12 }}
        {{- end }}
      volumes:
      - name: host
        hostPath:
          path: /
      {{- with .Values.volumes }}
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
workloadType: DaemonSet

daemonset:
  updateStrategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  hostNetwork: false
  hostPID: false
```

---

### Job

**File:** `templates/job.yaml`

```yaml
{{- if eq .Values.workloadType "Job" }}
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.job.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- with .Values.job.backoffLimit }}
  backoffLimit: {{ . }}
  {{- end }}
  {{- with .Values.job.completions }}
  completions: {{ . }}
  {{- end }}
  {{- with .Values.job.parallelism }}
  parallelism: {{ . }}
  {{- end }}
  {{- with .Values.job.activeDeadlineSeconds }}
  activeDeadlineSeconds: {{ . }}
  {{- end }}
  {{- with .Values.job.ttlSecondsAfterFinished }}
  ttlSecondsAfterFinished: {{ . }}
  {{- end }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "mychart.labels" . | nindent 8 }}
        {{- with .Values.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      restartPolicy: {{ .Values.job.restartPolicy }}
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "mychart.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 12 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        {{- with .Values.command }}
        command:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        {{- with .Values.args }}
        args:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        {{- with .Values.env }}
        env:
          {{- toYaml . | nindent 12 }}
        {{- end }}
        {{- with .Values.volumeMounts }}
        volumeMounts:
          {{- toYaml . | nindent 12 }}
        {{- end }}
      {{- with .Values.volumes }}
      volumes:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
workloadType: Job

job:
  annotations: {}
  backoffLimit: 3
  completions: 1
  parallelism: 1
  activeDeadlineSeconds: null
  ttlSecondsAfterFinished: 86400
  restartPolicy: Never

command: []
args: []
```

---

### CronJob

**File:** `templates/cronjob.yaml`

```yaml
{{- if eq .Values.workloadType "CronJob" }}
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  schedule: {{ .Values.cronjob.schedule | quote }}
  {{- with .Values.cronjob.concurrencyPolicy }}
  concurrencyPolicy: {{ . }}
  {{- end }}
  {{- with .Values.cronjob.failedJobsHistoryLimit }}
  failedJobsHistoryLimit: {{ . }}
  {{- end }}
  {{- with .Values.cronjob.successfulJobsHistoryLimit }}
  successfulJobsHistoryLimit: {{ . }}
  {{- end }}
  {{- with .Values.cronjob.startingDeadlineSeconds }}
  startingDeadlineSeconds: {{ . }}
  {{- end }}
  {{- if .Values.cronjob.suspend }}
  suspend: true
  {{- end }}
  jobTemplate:
    metadata:
      labels:
        {{- include "mychart.labels" . | nindent 8 }}
    spec:
      {{- with .Values.cronjob.backoffLimit }}
      backoffLimit: {{ . }}
      {{- end }}
      {{- with .Values.cronjob.ttlSecondsAfterFinished }}
      ttlSecondsAfterFinished: {{ . }}
      {{- end }}
      template:
        metadata:
          {{- with .Values.podAnnotations }}
          annotations:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          labels:
            {{- include "mychart.labels" . | nindent 12 }}
            {{- with .Values.podLabels }}
            {{- toYaml . | nindent 12 }}
            {{- end }}
        spec:
          restartPolicy: {{ .Values.cronjob.restartPolicy }}
          {{- with .Values.imagePullSecrets }}
          imagePullSecrets:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          serviceAccountName: {{ include "mychart.serviceAccountName" . }}
          securityContext:
            {{- toYaml .Values.podSecurityContext | nindent 12 }}
          containers:
          - name: {{ .Chart.Name }}
            securityContext:
              {{- toYaml .Values.securityContext | nindent 16 }}
            image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
            imagePullPolicy: {{ .Values.image.pullPolicy }}
            {{- with .Values.command }}
            command:
              {{- toYaml . | nindent 16 }}
            {{- end }}
            {{- with .Values.args }}
            args:
              {{- toYaml . | nindent 16 }}
            {{- end }}
            resources:
              {{- toYaml .Values.resources | nindent 16 }}
            {{- with .Values.env }}
            env:
              {{- toYaml . | nindent 16 }}
            {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
workloadType: CronJob

cronjob:
  schedule: "0 0 * * *"
  concurrencyPolicy: Forbid
  failedJobsHistoryLimit: 1
  successfulJobsHistoryLimit: 3
  startingDeadlineSeconds: null
  suspend: false
  backoffLimit: 3
  ttlSecondsAfterFinished: 86400
  restartPolicy: Never
```

---

## Service Resources

### Service

**File:** `templates/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.service.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  type: {{ .Values.service.type }}
  {{- if and (eq .Values.service.type "LoadBalancer") .Values.service.loadBalancerIP }}
  loadBalancerIP: {{ .Values.service.loadBalancerIP }}
  {{- end }}
  {{- with .Values.service.loadBalancerSourceRanges }}
  loadBalancerSourceRanges:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.service.externalIPs }}
  externalIPs:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- if .Values.service.sessionAffinity }}
  sessionAffinity: {{ .Values.service.sessionAffinity }}
  {{- if .Values.service.sessionAffinityConfig }}
  sessionAffinityConfig:
    {{- toYaml .Values.service.sessionAffinityConfig | nindent 4 }}
  {{- end }}
  {{- end }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: http
      {{- if and (eq .Values.service.type "NodePort") .Values.service.nodePort }}
      nodePort: {{ .Values.service.nodePort }}
      {{- end }}
    {{- range .Values.service.extraPorts }}
    - port: {{ .port }}
      targetPort: {{ .targetPort }}
      protocol: {{ .protocol | default "TCP" }}
      name: {{ .name }}
      {{- if and (eq $.Values.service.type "NodePort") .nodePort }}
      nodePort: {{ .nodePort }}
      {{- end }}
    {{- end }}
  selector:
    {{- include "mychart.selectorLabels" . | nindent 4 }}
```

**Headless Service (for StatefulSets):**

**File:** `templates/service-headless.yaml`

```yaml
{{- if eq .Values.workloadType "StatefulSet" }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "mychart.fullname" . }}-headless
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  type: ClusterIP
  clusterIP: None
  ports:
    - port: {{ .Values.service.port }}
      targetPort: {{ .Values.service.targetPort }}
      protocol: TCP
      name: http
  selector:
    {{- include "mychart.selectorLabels" . | nindent 4 }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
service:
  type: ClusterIP
  port: 80
  targetPort: 8080
  nodePort: null
  annotations: {}
  loadBalancerIP: ""
  loadBalancerSourceRanges: []
  externalIPs: []
  sessionAffinity: None
  sessionAffinityConfig: {}
  extraPorts: []
  # - name: metrics
  #   port: 9090
  #   targetPort: 9090
  #   protocol: TCP
```

---

### Ingress

**File:** `templates/ingress.yaml`

```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "mychart.fullname" $ }}
                port:
                  {{- if .servicePort }}
                  number: {{ .servicePort }}
                  {{- else }}
                  number: {{ $.Values.service.port }}
                  {{- end }}
          {{- end }}
    {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
ingress:
  enabled: false
  className: "nginx"
  annotations: {}
    # cert-manager.io/cluster-issuer: letsencrypt-prod
    # nginx.ingress.kubernetes.io/ssl-redirect: "true"
    # nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: Prefix
          # servicePort: 80
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local
```

---

## Configuration Resources

### ConfigMap

**File:** `templates/configmap.yaml`

```yaml
{{- if .Values.configMap.enabled }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
data:
  {{- range $key, $value := .Values.configMap.data }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
{{- end }}
```

**With files:**

```yaml
{{- if .Values.configMap.enabled }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
data:
  {{- range $key, $value := .Values.configMap.data }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
{{- with .Values.configMap.files }}
  {{- range $key, $value := . }}
  {{ $key }}: |
    {{- $value | nindent 4 }}
  {{- end }}
{{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
configMap:
  enabled: false
  data: {}
    # KEY: "value"
  files: {}
    # config.yaml: |
    #   server:
    #     port: 8080
```

---

### Secret

**File:** `templates/secret.yaml`

```yaml
{{- if .Values.secret.enabled }}
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
type: {{ .Values.secret.type }}
{{- if .Values.secret.stringData }}
stringData:
  {{- range $key, $value := .Values.secret.stringData }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
{{- end }}
{{- if .Values.secret.data }}
data:
  {{- range $key, $value := .Values.secret.data }}
  {{ $key }}: {{ $value }}
  {{- end }}
{{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
secret:
  enabled: false
  type: Opaque
  stringData: {}
    # API_KEY: "secret-key"
  data: {}
    # PASSWORD: cGFzc3dvcmQ=  # base64 encoded
```

---

## Storage Resources

### PersistentVolumeClaim

**File:** `templates/pvc.yaml`

```yaml
{{- if and .Values.persistence.enabled (not (eq .Values.workloadType "StatefulSet")) }}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.persistence.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  accessModes:
    {{- range .Values.persistence.accessModes }}
    - {{ . | quote }}
    {{- end }}
  resources:
    requests:
      storage: {{ .Values.persistence.size | quote }}
  {{- if .Values.persistence.storageClass }}
  {{- if (eq "-" .Values.persistence.storageClass) }}
  storageClassName: ""
  {{- else }}
  storageClassName: {{ .Values.persistence.storageClass | quote }}
  {{- end }}
  {{- end }}
  {{- with .Values.persistence.selector }}
  selector:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
persistence:
  enabled: false
  accessModes:
    - ReadWriteOnce
  size: 10Gi
  storageClass: ""
  annotations: {}
  selector: {}
```

---

## RBAC Resources

### ServiceAccount

**File:** `templates/serviceaccount.yaml`

```yaml
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "mychart.serviceAccountName" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  {{- with .Values.serviceAccount.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
automountServiceAccountToken: {{ .Values.serviceAccount.automount }}
{{- with .Values.serviceAccount.imagePullSecrets }}
imagePullSecrets:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- end }}
```

---

### Role

**File:** `templates/role.yaml`

```yaml
{{- if .Values.rbac.create }}
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
rules:
{{- range .Values.rbac.rules }}
- apiGroups:
  {{- range .apiGroups }}
    - {{ . | quote }}
  {{- end }}
  resources:
  {{- range .resources }}
    - {{ . | quote }}
  {{- end }}
  verbs:
  {{- range .verbs }}
    - {{ . | quote }}
  {{- end }}
  {{- with .resourceNames }}
  resourceNames:
  {{- range . }}
    - {{ . | quote }}
  {{- end }}
  {{- end }}
{{- end }}
{{- end }}
```

---

### RoleBinding

**File:** `templates/rolebinding.yaml`

```yaml
{{- if .Values.rbac.create }}
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: {{ include "mychart.fullname" . }}
subjects:
- kind: ServiceAccount
  name: {{ include "mychart.serviceAccountName" . }}
  namespace: {{ .Release.Namespace }}
{{- end }}
```

---

### ClusterRole

**File:** `templates/clusterrole.yaml`

```yaml
{{- if .Values.rbac.createClusterRole }}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
rules:
{{- range .Values.rbac.clusterRules }}
- apiGroups:
  {{- range .apiGroups }}
    - {{ . | quote }}
  {{- end }}
  resources:
  {{- range .resources }}
    - {{ . | quote }}
  {{- end }}
  verbs:
  {{- range .verbs }}
    - {{ . | quote }}
  {{- end }}
{{- end }}
{{- end }}
```

---

### ClusterRoleBinding

**File:** `templates/clusterrolebinding.yaml`

```yaml
{{- if .Values.rbac.createClusterRole }}
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: {{ include "mychart.fullname" . }}
subjects:
- kind: ServiceAccount
  name: {{ include "mychart.serviceAccountName" . }}
  namespace: {{ .Release.Namespace }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
rbac:
  create: false
  createClusterRole: false
  rules: []
  # - apiGroups: [""]
  #   resources: ["configmaps", "secrets"]
  #   verbs: ["get", "list", "watch"]
  clusterRules: []
  # - apiGroups: [""]
  #   resources: ["nodes"]
  #   verbs: ["get", "list"]
```

---

## Network Resources

### NetworkPolicy

**File:** `templates/networkpolicy.yaml`

```yaml
{{- if .Values.networkPolicy.enabled }}
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  podSelector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  policyTypes:
  {{- range .Values.networkPolicy.policyTypes }}
    - {{ . }}
  {{- end }}
  {{- with .Values.networkPolicy.ingress }}
  ingress:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  {{- with .Values.networkPolicy.egress }}
  egress:
    {{- toYaml . | nindent 4 }}
  {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
networkPolicy:
  enabled: false
  policyTypes:
    - Ingress
    - Egress
  ingress: []
  # - from:
  #   - namespaceSelector:
  #       matchLabels:
  #         name: allowed-namespace
  #   ports:
  #   - protocol: TCP
  #     port: 8080
  egress: []
  # - to:
  #   - podSelector: {}
  #   ports:
  #   - protocol: TCP
  #     port: 53
```

---

## Autoscaling Resources

### HorizontalPodAutoscaler

**File:** `templates/hpa.yaml`

```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: {{ .Values.workloadType | default "Deployment" }}
    name: {{ include "mychart.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  {{- with .Values.autoscaling.behavior }}
  behavior:
    {{- toYaml . | nindent 4 }}
  {{- end }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
    {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
    {{- end }}
    {{- with .Values.autoscaling.customMetrics }}
    {{- toYaml . | nindent 4 }}
    {{- end }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: null
  behavior: {}
  # behavior:
  #   scaleDown:
  #     stabilizationWindowSeconds: 300
  #     policies:
  #     - type: Percent
  #       value: 50
  #       periodSeconds: 15
  customMetrics: []
  # - type: Pods
  #   pods:
  #     metric:
  #       name: packets-per-second
  #     target:
  #       type: AverageValue
  #       averageValue: 1k
```

---

### PodDisruptionBudget

**File:** `templates/pdb.yaml`

```yaml
{{- if .Values.podDisruptionBudget.enabled }}
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  {{- if .Values.podDisruptionBudget.minAvailable }}
  minAvailable: {{ .Values.podDisruptionBudget.minAvailable }}
  {{- end }}
  {{- if .Values.podDisruptionBudget.maxUnavailable }}
  maxUnavailable: {{ .Values.podDisruptionBudget.maxUnavailable }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
{{- end }}
```

**Corresponding values.yaml:**

```yaml
podDisruptionBudget:
  enabled: false
  minAvailable: 1
  maxUnavailable: null
```

---

## Usage Notes

1. Replace `mychart` with your actual chart name throughout all templates
2. Include standard helpers from `_helpers.tpl`
3. Use `toYaml` for complex nested structures
4. Always provide sensible defaults in values.yaml
5. Use `with` blocks for optional sections
6. Add checksums for ConfigMaps and Secrets to trigger pod restarts
7. Document all values with comments
