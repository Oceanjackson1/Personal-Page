---
title: "Helm Validator"
description: "Validate, lint, audit, check Helm charts — Chart.yaml, templates, values.yaml, CRDs, schemas."
category: "devops"
source: "community"
author: "Community"
tags: ["helm", "validator"]
date: 2026-03-20
---

# Helm Chart Validator & Analysis Toolkit

## Overview

This skill provides a comprehensive validation and analysis workflow for Helm charts, combining Helm-native linting, template rendering, YAML validation, schema validation, CRD documentation lookup, and security best practices checking.

**IMPORTANT: This validator is read-only by default.** It analyzes charts and proposes improvements. Only modify files when the user explicitly asks to apply fixes.

## Trigger Cases

Use this skill when one or more of these top cases apply:
- The user asks to validate, lint, check, test, or troubleshoot a Helm chart
- Helm templates fail to render, lint, or produce valid Kubernetes YAML
- A pre-deployment quality gate is needed (schema, dry-run, security checks)
- CRD resources are present and their spec fields must be verified against docs
- The user wants a severity-based validation report with proposed remediations

Trigger phrase examples:
- "Validate this Helm chart before release"
- "Why does `helm template` fail?"
- "Check this chart for Kubernetes and security issues"

Out of scope by default:
- New chart scaffolding or broad chart generation (use `helm-generator`)

## Role Boundaries

- This skill validates and reports; it does not silently rewrite user files.
- It can propose concrete patches and apply them only when the user explicitly requests fixes.
- If execution constraints block a stage, it must continue with reachable stages and document the skip reason.

## Execution Model

1. Run stages in order (1 through 10).
2. Keep going after stage-level failures to collect complete findings, unless rendering fails and no manifests exist.
3. If Stage 4 produces no manifests, mark Stages 5 to 9 as blocked and continue to Stage 10 reporting.
4. Treat Stage 8 as environment-dependent optional; treat Stage 9 and Stage 10 as mandatory when manifests exist.
5. For every skipped stage, record the exact tool/environment reason in the final summary table.

## Quick Execution Modes

### Mode A: Local Validation (no cluster required)
```bash
bash scripts/setup_tools.sh
bash scripts/validate_chart_structure.sh <chart-directory>
helm lint <chart-directory> --strict
helm template <release-name> <chart-directory> --values <values-file> --debug --output-dir ./rendered
find ./rendered -type f \( -name "*.yaml" -o -name "*.yml" \) -exec yamllint -c assets/.yamllint {} +
find ./rendered -type f \( -name "*.yaml" -o -name "*.yml" \) -exec kubeconform -summary -verbose {} +
```

### Mode B: Full Validation (cluster available)
Run Mode A plus Stage 8 dry-run commands in this document.

## Validation & Testing Workflow

Follow this sequential validation workflow. Each stage catches different types of issues:

### Stage 1: Tool Check

Before starting validation, verify required tools are installed:

```bash
bash scripts/setup_tools.sh
```

Required tools:
- **helm**: Helm package manager for Kubernetes (v3+)
- **yamllint**: YAML syntax and style linting
- **kubeconform**: Kubernetes schema validation with CRD support
- **kubectl**: Cluster dry-run testing (optional but recommended)

Fallback policy for unavailable tools or environment constraints:

| Condition | Action | Stage status |
|-----------|--------|--------------|
| `helm` missing | Run Stage 2 only, then report Stages 3 to 9 as skipped/blocked | ⚠️ Warning |
| `yamllint` missing | Use `yq` syntax checks if available; otherwise skip Stage 5 | ⚠️ Warning |
| `kubeconform` missing | Skip Stage 7 and rely on Stage 6 CRD/manual checks | ⚠️ Warning |
| `kubectl` missing or no kube-context | Skip Stage 8, continue with remaining stages | ⚠️ Warning |
| No internet access for CRD docs | Use local CRD manifests and kubeconform output, mark doc lookup incomplete | ⚠️ Warning |

If tools are missing, provide installation instructions from `scripts/setup_tools.sh` output and continue with the fallback path above.

### Stage 2: Helm Chart Structure Validation

Verify the chart follows the standard Helm directory structure:

```bash
bash scripts/validate_chart_structure.sh <chart-directory>
```

**Expected structure:**
```
mychart/
  Chart.yaml          # Chart metadata (required)
  values.yaml         # Default values (required)
  values.schema.json  # JSON Schema for values validation (optional)
  templates/          # Template directory (required)
    _helpers.tpl      # Template helpers (recommended)
    NOTES.txt         # Post-install notes (recommended)
    *.yaml            # Kubernetes manifest templates
  charts/             # Chart dependencies (optional)
  crds/               # Custom Resource Definitions (optional)
  .helmignore         # Files to ignore during packaging (optional)
```

**Common issues caught:**
- Missing required files (Chart.yaml, values.yaml, templates/)
- Invalid Chart.yaml syntax or missing required fields
- Malformed values.schema.json
- Incorrect file permissions

### Stage 3: Helm Lint

Run Helm's built-in linter to catch chart-specific issues:

```bash
helm lint <chart-directory> --strict
```

**Optional flags:**
- `--values <values-file>`: Test with specific values
- `--set key=value`: Override specific values
- `--debug`: Show detailed error information

**Common issues caught:**
- Invalid Chart.yaml metadata
- Template syntax errors
- Missing or undefined values
- Deprecated Kubernetes API versions
- Chart best practice violations

**Auto-fix approach:**
- For template errors, identify the problematic template file
- Show the user the specific line causing issues
- Propose a patch/diff for the fix
- Apply fixes only if the user explicitly asks
- Re-run `helm lint` after fixes are applied

### Stage 4: Template Rendering

Render templates locally to verify they produce valid YAML:

```bash
helm template <release-name> <chart-directory> \
  --values <values-file> \
  --debug \
  --output-dir ./rendered
```

**Options to consider:**
- `--values values.yaml`: Use specific values file
- `--set key=value`: Override individual values
- `--show-only templates/deployment.yaml`: Render specific template
- `--validate`: Validate against Kubernetes OpenAPI schema
- `--include-crds`: Include CRDs in rendered output
- `--is-upgrade`: Simulate upgrade scenario
- `--kube-version 1.28.0`: Target specific Kubernetes version

**Common issues caught:**
- Template syntax errors (Go template issues)
- Undefined variables or values
- Type mismatches (string vs. integer)
- Missing required values
- Logic errors in conditionals or loops
- Incorrect indentation in nested templates

**For template errors:**
- Identify the template file and line number
- Check if values are properly defined in values.yaml
- Verify template function usage (quote, required, default, include, etc.)
- Test with different value combinations

### Stage 5: YAML Syntax Validation

Validate YAML syntax and formatting of rendered templates:

```bash
find ./rendered -type f \( -name "*.yaml" -o -name "*.yml" \) \
  -exec yamllint -c assets/.yamllint {} +
```

**Common issues caught:**
- Indentation errors (tabs vs spaces)
- Trailing whitespace
- Line length violations
- Syntax errors
- Duplicate keys
- Document start/end markers

**Auto-fix approach:**
- For simple issues (indentation, trailing spaces), propose fixes using the Edit tool
- For template-generated issues, fix the source template, not rendered output
- Always show the user what will be changed before applying fixes

### Stage 6: CRD Detection and Documentation Lookup

Before schema validation, detect if the chart contains or renders Custom Resource Definitions:

```bash
# Check crds/ directory
if [ -d <chart-directory>/crds ]; then
  find <chart-directory>/crds -type f \( -name "*.yaml" -o -name "*.yml" \) \
    -exec bash scripts/detect_crd_wrapper.sh {} +
fi

# Check rendered templates
find ./rendered -type f \( -name "*.yaml" -o -name "*.yml" \) \
  -exec bash scripts/detect_crd_wrapper.sh {} +
```

The script outputs JSON with resource information:
```json
[
  {
    "kind": "Certificate",
    "apiVersion": "cert-manager.io/v1",
    "group": "cert-manager.io",
    "version": "v1",
    "isCRD": true,
    "name": "example-cert"
  }
]
```

**For each detected CRD:**

1. **Try context7 MCP first (preferred):**
   ```
   Use mcp__context7__resolve-library-id with the CRD project name
   Example: "cert-manager" for cert-manager.io CRDs
            "prometheus-operator" for monitoring.coreos.com CRDs
            "istio" for networking.istio.io CRDs

   Then use mcp__context7__query-docs with:
   - libraryId from resolve step
   - query: The CRD kind and relevant features (e.g., "Certificate spec required fields")
   ```

2. **Fallback to `web.search_query` (web search) if Context7 fails:**
   ```
   Search query pattern:
   "<kind>" "<group>" kubernetes CRD "<version>" documentation spec

   Example:
   "Certificate" "cert-manager.io" kubernetes CRD "v1" documentation spec
   "Prometheus" "monitoring.coreos.com" kubernetes CRD "v1" documentation spec
   ```

3. **Extract key information:**
   - Required fields in `spec`
   - Field types and validation rules
   - Examples from documentation
   - Version-specific changes or deprecations
   - Common configuration patterns

**Why this matters:** CRDs have custom schemas not available in standard Kubernetes validation tools. Understanding the CRD's spec requirements prevents validation errors and ensures correct resource configuration.

### Stage 7: Schema Validation

Validate rendered templates against Kubernetes schemas:

```bash
find ./rendered -type f \( -name "*.yaml" -o -name "*.yml" \) -exec \
  kubeconform \
    -schema-location default \
    -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
    -summary \
    -verbose \
    {} +
```

**Options to consider:**
- Add `-strict` to reject unknown fields (recommended for production)
- Add `-ignore-missing-schemas` if working with custom/internal CRDs
- Add `-kubernetes-version 1.28.0` to validate against specific K8s version
- Add `-output json` for programmatic processing

**Common issues caught:**
- Invalid apiVersion or kind
- Missing required fields
- Wrong field types
- Invalid enum values
- Unknown fields (with -strict)

**For CRDs:** If kubeconform reports "no schema found", this is expected. Use the documentation from Stage 6 to manually validate the spec fields.

**Stage 7 success criteria (explicit):**
- ✅ Passed: `kubeconform` exits `0`, and no invalid resources are reported.
- ⚠️ Warning: only CRD schema-missing findings remain and Stage 6 documentation/manual verification is completed.
- ❌ Failed: any non-CRD schema violation, parse error, or unresolved required-field/type error.

### Stage 8: Cluster Dry-Run (if available)

If kubectl is configured and cluster access is available, perform a server-side dry-run:

```bash
# Test installation
helm install <release-name> <chart-directory> \
  --dry-run=server \
  --debug \
  --values <values-file>

# Test upgrade
helm upgrade <release-name> <chart-directory> \
  --dry-run=server \
  --debug \
  --values <values-file>
```

If the Helm version does not support `--dry-run=server`, use `--dry-run` and document that only client-side Helm simulation was executed.

**This catches:**
- Admission controller rejections
- Policy violations (PSP, OPA, Kyverno, etc.)
- Resource quota violations
- Missing namespaces
- Invalid ConfigMap/Secret references
- Webhook validations
- Existing resource conflicts

**If dry-run is not possible:**
- Use kubectl with rendered templates: `kubectl apply --dry-run=server -f ./rendered/`
- Skip if no cluster access
- Document that cluster-specific validation was skipped

**For updates to existing releases:**
```bash
helm diff upgrade <release-name> <chart-directory>
```
This shows what would change, helping catch unintended modifications. (Requires helm-diff plugin)

**Stage 8 success criteria (explicit):**
- ✅ Passed: dry-run install and upgrade commands exit `0` with no admission/policy errors.
- ⚠️ Warning: stage skipped because `kubectl`/cluster context/access is unavailable, or only client-side fallback was possible.
- ❌ Failed: dry-run commands return non-zero due to admission webhooks, policy violations, namespace/quota errors, or reference errors.

### Stage 9: Security Best Practices Check (MANDATORY)

**IMPORTANT:** This stage is MANDATORY. Analyze rendered templates for security best practices compliance.

**Check rendered Deployment/Pod templates for:**

1. **Missing securityContext** - Look for pods/containers without security settings:
   ```yaml
   # Check if pod-level securityContext exists
   spec:
     securityContext:
       runAsNonRoot: true
       runAsUser: 1000
       fsGroup: 2000
   ```

2. **Missing container securityContext** - Each container should have:
   ```yaml
   securityContext:
     allowPrivilegeEscalation: false
     readOnlyRootFilesystem: true
     runAsNonRoot: true
     capabilities:
       drop:
         - ALL
   ```

3. **Missing resource limits/requests** - Check for:
   ```yaml
   resources:
     limits:
       cpu: "100m"
       memory: "128Mi"
     requests:
       cpu: "100m"
       memory: "128Mi"
   ```

4. **Image tag issues** - Flag if using `:latest` or no tag

5. **Missing probes** - Check for liveness/readiness probes

**How to check:** Read the rendered deployment YAML files and grep for these patterns:
```bash
# Check for securityContext
find ./rendered -type f \( -name "*.yaml" -o -name "*.yml" \) \
  -exec grep -l "securityContext" {} +

# Check for resources
find ./rendered -type f \( -name "*.yaml" -o -name "*.yml" \) \
  -exec grep -l "resources:" {} +

# Check for latest tag
find ./rendered -type f \( -name "*.yaml" -o -name "*.yml" \) \
  -exec grep "image:.*:latest" {} +
```

### Stage 10: Final Report (MANDATORY)

**IMPORTANT:** This stage is MANDATORY even if all validations pass. You MUST complete ALL of the following actions.

**Default behavior is read-only.** Do not modify files unless the user explicitly asks you to apply fixes.

#### Step 1: Load Reference Files (MANDATORY when warnings exist)

**If ANY warnings, errors, or security issues were found, you MUST read:**
```
Read references/helm_best_practices.md
Read references/k8s_best_practices.md
```

Use these references to provide context and recommendations for each issue found.

#### Step 2: Present Validation Summary

**Always present a validation summary** formatted as a table showing:
- Each validation stage executed (Stages 1-9)
- Status of each stage (✅ Passed, ⚠️ Warning, ❌ Failed)
- Count of issues found per stage

Example:
```
| Stage | Status | Issues |
|-------|--------|--------|
| 1. Tool Check | ✅ Passed | All tools available |
| 2. Structure | ⚠️ Warning | Missing: .helmignore, NOTES.txt |
| 3. Helm Lint | ✅ Passed | 0 errors |
| 4. Template Render | ✅ Passed | 5 templates rendered |
| 5. YAML Syntax | ✅ Passed | No yamllint errors |
| 6. CRD Detection | ✅ Passed | 1 CRD documented |
| 7. Schema Validation | ✅ Passed | All resources valid |
| 8. Dry-Run | ✅ Passed | No cluster errors |
| 9. Security Check | ⚠️ Warning | Missing securityContext |
```

#### Step 3: Categorize All Issues

Group findings by severity:

**❌ Errors (must fix):**
- Template syntax errors
- Missing required fields
- Schema validation failures
- Dry-run failures

**⚠️ Warnings (should fix):**
- Deprecated Kubernetes APIs
- Missing securityContext
- Missing resource limits/requests
- Using `:latest` image tag
- Missing recommended files (_helpers.tpl, .helmignore, NOTES.txt)

**ℹ️ Info (recommendations):**
- Missing values.schema.json
- Missing README.md
- Optimization opportunities

#### Step 4: List Proposed Changes (DO NOT APPLY)

For each issue, provide a **proposed fix** with:
- File path and line number (if applicable)
- Before/after code blocks
- Explanation of why this change is recommended

Example format:
```
## Proposed Changes

### 1. Add securityContext to Deployment
**File:** templates/deployment.yaml:25
**Severity:** ⚠️ Warning
**Reason:** Running containers as root is a security risk

**Current:**
```yaml
spec:
  containers:
    - name: app
      image: nginx:1.21
```

**Proposed:**
```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
    - name: app
      image: nginx:1.21
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
```

### 2. Add .helmignore file
**File:** .helmignore (new file)
**Severity:** ⚠️ Warning
**Reason:** Excludes unnecessary files from chart packaging

**Proposed:** Copy from `assets/.helmignore`
```

#### Step 5: Automation Opportunities

List all detected automation opportunities:
- If `_helpers.tpl` is missing → Recommend: `bash scripts/generate_helpers.sh <chart>`
- If `.helmignore` is missing → Recommend: Copy from `assets/.helmignore`
- If `values.schema.json` is missing → Recommend: Copy and customize from `assets/values.schema.json`
- If `NOTES.txt` is missing → Recommend: Create post-install notes template
- If `README.md` is missing → Recommend: Create chart documentation

#### Step 6: Final Summary

Provide a final summary:
```
## Validation Summary

**Chart:** <chart-name>
**Status:** ⚠️ Warnings Found (or ✅ Ready for Deployment)

**Issues Found:**
- Errors: X
- Warnings: Y
- Info: Z

**Proposed Changes:** N changes recommended

**Next Steps:**
1. Review proposed changes above
2. Apply changes manually or use helm-generator skill
3. Re-run validation to confirm fixes
```

## Workflow Done Criteria

Validation is complete only when all of the following are true:
- A Stage 1 to Stage 10 status table is present with `✅ Passed`, `⚠️ Warning`, `❌ Failed`, or `⏭️ Skipped` for each stage.
- Every skipped stage includes a concrete tool or environment reason.
- Stage 7 and Stage 8 are evaluated against their explicit success criteria above.
- Severity totals are reported (`Errors`, `Warnings`, `Info`) with proposed remediation actions.
- Role boundary is respected: no file edits unless explicitly requested by the user.

## Helm Templating Automation & Best Practices

This section covers advanced Helm templating techniques, helper functions, and automation strategies.

### Template Helpers (`_helpers.tpl`)

Template helpers are reusable functions defined in `templates/_helpers.tpl`. They promote DRY principles and consistency.

**Standard helper patterns:**

1. **Chart name helper:**
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "mychart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
```

2. **Fullname helper:**
```yaml
{{/*
Create a default fully qualified app name.
*/}}
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}
```

3. **Chart reference helper:**
```yaml
{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "mychart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}
```

4. **Standard labels helper:**
```yaml
{{/*
Common labels
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
{{ include "mychart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

5. **Selector labels helper:**
```yaml
{{/*
Selector labels
*/}}
{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

6. **ServiceAccount name helper:**
```yaml
{{/*
Create the name of the service account to use
*/}}
{{- define "mychart.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "mychart.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

**When to create helpers:**
- Values used in multiple templates
- Complex logic that's repeated
- Label sets that should be consistent
- Name generation patterns
- Conditional resource inclusion

### Essential Template Functions

Reference and use these Helm template functions for robust charts:

1. **`required` - Enforce required values:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ required "A valid service name is required!" .Values.service.name }}
```

2. **`default` - Provide fallback values:**
```yaml
replicas: {{ .Values.replicaCount | default 1 }}
```

3. **`quote` - Safely quote string values:**
```yaml
env:
  - name: DATABASE_HOST
    value: {{ .Values.database.host | quote }}
```

4. **`include` - Use helpers with pipeline:**
```yaml
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
```

5. **`tpl` - Render strings as templates:**
```yaml
{{- tpl .Values.customConfig . }}
```

6. **`toYaml` - Convert objects to YAML:**
```yaml
{{- with .Values.resources }}
resources:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

7. **`fromYaml` - Parse YAML strings:**
```yaml
{{- $config := .Values.configYaml | fromYaml }}
```

8. **`merge` - Merge maps:**
```yaml
{{- $merged := merge .Values.override .Values.defaults }}
```

9. **`lookup` - Query cluster resources (use carefully):**
```yaml
{{- $secret := lookup "v1" "Secret" .Release.Namespace "my-secret" }}
{{- if $secret }}
  # Secret exists, use it
{{- else }}
  # Create new secret
{{- end }}
```

### Advanced Template Patterns

1. **Conditional resource creation:**
```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
# ... ingress definition
{{- end }}
```

2. **Range over lists:**
```yaml
{{- range .Values.extraEnvVars }}
- name: {{ .name }}
  value: {{ .value | quote }}
{{- end }}
```

3. **Range over maps:**
```yaml
{{- range $key, $value := .Values.configMap }}
{{ $key }}: {{ $value | quote }}
{{- end }}
```

4. **With blocks for scoping:**
```yaml
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

5. **Named templates with custom context:**
```yaml
{{- include "mychart.container" (dict "root" . "container" .Values.mainContainer) }}
```

### Values Structure Best Practices

**Prefer flat structures when possible:**

```yaml
# Good - Flat structure
serverName: nginx
serverPort: 80

# Acceptable - Nested structure for related settings
server:
  name: nginx
  port: 80
  replicas: 3
```

**Always provide defaults in values.yaml:**
```yaml
replicaCount: 1

image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.21.0"

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

**Document all values:**
```yaml
# replicaCount is the number of pod replicas for the deployment
replicaCount: 1

# image configures the container image
image:
  # image.repository is the container image registry and name
  repository: nginx
  # image.tag overrides the image tag (default is chart appVersion)
  tag: "1.21.0"
```

### Template Comments and Documentation

Use Helm template comments for documentation:

```yaml
{{- /*
mychart.fullname generates the fullname for resources.
It supports nameOverride and fullnameOverride values.
Usage: {{ include "mychart.fullname" . }}
*/ -}}
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
```

Use YAML comments for user-facing notes:

```yaml
# WARNING: Changing the storage class will not migrate existing data
storageClass: "standard"
```

### Whitespace Management

Use `-` to chomp whitespace in template directives:

```yaml
{{- if .Values.enabled }}
  # Remove leading whitespace
{{- end }}

{{ .Values.name -}}
  # Remove trailing whitespace
```

Good formatting:
```yaml
{{- if .Values.enabled }}
  key: value
{{- end }}
```

Bad formatting:
```yaml
{{if .Values.enabled}}
key: value
{{end}}
```

## Helper Patterns Reference

When analyzing charts, identify opportunities for helper functions:

1. **Identify repetition:**
   - Same label sets across resources
   - Repeated name generation logic
   - Common conditional patterns

2. **Common helper patterns to recommend:**
   - Chart name helper (`.name`)
   - Fullname helper (`.fullname`)
   - Chart version label (`.chart`)
   - Common labels (`.labels`)
   - Selector labels (`.selectorLabels`)
   - ServiceAccount name (`.serviceAccountName`)

3. **When to recommend helpers:**
   - Missing `_helpers.tpl` file
   - Repeated code patterns across templates
   - Inconsistent label usage
   - Long resource names that need truncation

## Best Practices Reference

For detailed Helm and Kubernetes best practices, load the references:

```
Read references/helm_best_practices.md
Read references/k8s_best_practices.md
```

These references include:
- Chart structure and metadata
- Template conventions and patterns
- Values file organization
- Security best practices
- Resource limits and requests
- Common validation issues and fixes

**When to load:** When validation reveals issues that need context, when implementing new features, or when the user asks about best practices.

## Working with Chart Dependencies

When a chart has dependencies (in `Chart.yaml` or `charts/` directory):

1. **Update dependencies:**
```bash
helm dependency update <chart-directory>
```

2. **List dependencies:**
```bash
helm dependency list <chart-directory>
```

3. **Validate dependencies:**
   - Check that dependency versions are available
   - Verify dependency values are properly scoped
   - Test templates with dependency resources

4. **Override dependency values:**
```yaml
# values.yaml
postgresql:
  enabled: true
  postgresqlPassword: "secret"
  persistence:
    size: 10Gi
```

## Error Handling Strategies

### Tool Not Available
- Run `scripts/setup_tools.sh` to check availability
- Provide installation instructions
- Skip optional stages but document what was skipped
- Continue with available tools

### Template Rendering Errors
- Show the specific template file and line number
- Check if values are defined in values.yaml
- Verify template function syntax
- Test with simpler value combinations
- Use `--debug` flag for detailed error messages

### Cluster Access Issues
- Fall back to client-side validation
- Use rendered templates with kubectl
- Skip cluster validation if no kubectl config
- Document limitations in validation report

### CRD Documentation Not Found
- Document that documentation lookup failed
- Attempt validation with kubeconform CRD schemas
- Suggest manual CRD inspection:
  ```bash
  kubectl get crd <crd-name>.group -o yaml
  kubectl explain <kind>
  ```

### Validation Stage Failures
- Continue to next stage even if one fails
- Collect all errors before presenting to user
- Prioritize fixing Helm lint errors first
- Then fix template errors
- Finally fix schema/validation errors

### macOS Extended Attributes Issue

**Symptom:** Helm reports "Chart.yaml file is missing" even though the file exists and is readable.

**Cause:** On macOS, files created programmatically (via Write tool, scripts, or certain editors) may have extended attributes (e.g., `com.apple.provenance`, `com.apple.quarantine`) that interfere with Helm's file detection.

**Diagnosis:**
```bash
# Check for extended attributes
xattr /path/to/chart/Chart.yaml

# If attributes are present, you'll see output like:
# com.apple.provenance
# com.apple.quarantine
```

**Solutions:**

1. **Remove extended attributes:**
   ```bash
   # Remove all extended attributes from a file
   xattr -c /path/to/chart/Chart.yaml

   # Remove all extended attributes recursively from chart directory
   xattr -cr /path/to/chart/
   ```

2. **Create files using shell commands instead:**
   ```bash
   # Use cat with heredoc instead of direct file writes
   cat > Chart.yaml << 'EOF'
   apiVersion: v2
   name: mychart
   version: 0.1.0
   EOF
   ```

3. **Copy from helm-created chart:**
   ```bash
   # Create a fresh chart and copy structure
   helm create temp-chart
   cp -r temp-chart/* /path/to/your/chart/
   rm -rf temp-chart
   ```

**Prevention:** When creating new chart files on macOS, prefer using `helm create` as a base or use shell heredocs (`cat > file << 'EOF'`) rather than direct file creation tools.

## Communication Guidelines

When presenting validation results and fixes:

1. **Be clear and concise** about what was found
2. **Explain why issues matter** (e.g., "This will cause pod creation to fail")
3. **Provide context** from Helm best practices when relevant
4. **Group related issues** (e.g., all missing helper issues together)
5. **Use file:line references** when available
6. **Show confidence level** for auto-fixes (high confidence = syntax, low = logic changes)
7. **Always provide a summary after proposing fixes** (and after applying fixes when explicitly requested) including:
   - What was changed and why
   - File and line references for each fix
   - Total count of issues resolved
   - Final validation status
   - Any remaining warnings or recommendations

## Version Awareness

Always consider Kubernetes and Helm version compatibility:
- Check for deprecated Kubernetes APIs
- Ensure Helm chart apiVersion is v2 (for Helm 3+)
- For CRDs, ensure the apiVersion matches what's in the cluster
- Use `kubectl api-versions` to list available API versions
- Reference version-specific documentation when available
- Set `kubeVersion` constraint in Chart.yaml if needed

## Chart Testing

For comprehensive testing, use Helm test resources:

1. **Create test resources:**
```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "mychart.fullname" . }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "mychart.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

2. **Run tests:**
```bash
helm test <release-name>
```

## Automation Opportunities Reference

**During Stage 10 (Final Report), list all detected automation opportunities in the summary.**

**Do NOT ask user questions or modify files. Simply list recommendations.**

**Automation opportunities to detect and list:**

| Missing Item | Recommendation |
|--------------|----------------|
| `_helpers.tpl` | Run: `bash scripts/generate_helpers.sh <chart>` |
| `.helmignore` | Copy from: `assets/.helmignore` |
| `values.schema.json` | Copy and customize from: `assets/values.schema.json` |
| `NOTES.txt` | Create post-install notes template |
| `README.md` | Create chart documentation |
| Repeated patterns | Extract to helper functions |

**Security recommendations to include when issues found:**

| Issue | Recommendation |
|-------|----------------|
| Missing pod securityContext | Add `runAsNonRoot: true`, `runAsUser: 1000`, `fsGroup: 2000` |
| Missing container securityContext | Add `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: [ALL]` |
| Missing resource limits | Add CPU/memory limits and requests |
| Using `:latest` tag | Pin to specific image version |
| Missing probes | Add liveness and readiness probes |

**Template improvement recommendations:**

| Issue | Recommendation |
|-------|----------------|
| Using `template` instead of `include` | Replace with `include` for pipeline support |
| Missing `nindent` | Add `nindent` for proper YAML indentation |
| No default values | Add `default` function for optional values |
| Missing `required` function | Add `required` for critical values |

## Resources

### scripts/

**setup_tools.sh**
- Checks for required validation tools (helm, yamllint, kubeconform, kubectl)
- Provides installation instructions for missing tools
- Verifies versions of installed tools
- Usage: `bash scripts/setup_tools.sh`

**validate_chart_structure.sh**
- Validates Helm chart directory structure
- Checks for required files (Chart.yaml, values.yaml, templates/)
- Verifies file formats and syntax
- Usage: `bash scripts/validate_chart_structure.sh <chart-directory>`

**detect_crd_wrapper.sh**
- Wrapper script that handles Python dependency management
- Automatically creates temporary venv if PyYAML is not available
- Calls detect_crd.py to parse YAML files
- Usage: `bash scripts/detect_crd_wrapper.sh <file.yaml> [file2.yaml ...]`

**detect_crd.py**
- Parses YAML files to identify Custom Resource Definitions
- Extracts kind, apiVersion, group, and version information
- Outputs JSON for programmatic processing
- Requires PyYAML (handled automatically by wrapper script)
- Can be called directly: `python3 scripts/detect_crd.py <file.yaml> [file2.yaml ...]`

**generate_helpers.sh**
- Generates standard Helm helpers (_helpers.tpl) for a chart
- Creates fullname, labels, and selector helpers
- Usage: `bash scripts/generate_helpers.sh <chart-directory>`

### references/

**helm_best_practices.md**
- Comprehensive guide to Helm chart best practices
- Covers template patterns, helper functions, values structure
- Common validation issues and how to fix them
- Security and performance recommendations
- Load when providing context for Helm-specific issues

**k8s_best_practices.md**
- Comprehensive guide to Kubernetes YAML best practices
- Covers metadata, labels, resource limits, security context
- Common validation issues and how to fix them
- Load when providing context for Kubernetes-specific issues

**template_functions.md**
- Reference guide for Helm template functions
- Examples of all built-in functions
- Sprig function library reference
- Custom function patterns
- Load when implementing complex templates

### assets/

**.helmignore**
- Standard .helmignore file for excluding files from packaging
- Pre-configured with common patterns

**.yamllint**
- Pre-configured yamllint rules for Kubernetes YAML
- Follows Kubernetes conventions (2-space indentation, line length, etc.)
- Can be customized per project
- Usage: `yamllint -c assets/.yamllint <file.yaml>`

**values.schema.json**
- Example JSON Schema for values validation
- Can be copied and customized for specific charts
- Provides type safety and validation

---

## Reference: Helm_Best_Practices

# Helm Chart Best Practices

This reference provides comprehensive best practices for creating, maintaining, and validating Helm charts.

## Chart Structure

### Required Files

Every Helm chart must have:

```
mychart/
  Chart.yaml     # Chart metadata
  values.yaml    # Default configuration values
  templates/     # Template directory
```

### Chart.yaml Structure

Use apiVersion v2 for Helm 3+ charts:

```yaml
apiVersion: v2
name: mychart
description: A Helm chart for Kubernetes
type: application  # or 'library' for helper charts
version: 0.1.0     # Chart version (SemVer)
appVersion: "1.16.0"  # Version of the app

# Optional but recommended
keywords:
  - web
  - application
home: https://github.com/example/mychart
sources:
  - https://github.com/example/mychart
maintainers:
  - name: Your Name
    email: your.email@example.com

# Dependencies
dependencies:
  - name: postgresql
    version: "~11.6.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled

# Kubernetes version constraint
kubeVersion: ">=1.21.0-0"
```

## Template Best Practices

### 1. Use Named Templates (Helpers)

Define reusable templates in `templates/_helpers.tpl`:

**Good:**
```yaml
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
```

**Usage:**
```yaml
metadata:
  name: {{ include "mychart.fullname" . }}
```

### 2. Use `include` Instead of `template`

**Good:**
```yaml
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
```

**Bad:**
```yaml
metadata:
  labels:
    {{- template "mychart.labels" . }}
```

**Why:** `include` allows piping the output to other functions like `nindent`, `indent`, `quote`, etc.

### 3. Always Quote String Values

**Good:**
```yaml
env:
  - name: DATABASE_HOST
    value: {{ .Values.database.host | quote }}
```

**Bad:**
```yaml
env:
  - name: DATABASE_HOST
    value: {{ .Values.database.host }}
```

**Why:** Prevents YAML parsing issues with special characters and ensures strings are treated as strings.

### 4. Use `required` for Critical Values

**Good:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "mychart.fullname" . }}
data:
  password: {{ required "A valid .Values.password is required!" .Values.password | b64enc }}
```

**Why:** Fails early with a helpful error message if required values are missing.

### 5. Provide Defaults with `default` Function

**Good:**
```yaml
replicas: {{ .Values.replicaCount | default 1 }}
```

**Why:** Makes charts more resilient and easier to use with minimal configuration.

### 6. Use `nindent` for Proper Indentation

**Good:**
```yaml
spec:
  template:
    metadata:
      labels:
        {{- include "mychart.labels" . | nindent 8 }}
```

**Bad:**
```yaml
spec:
  template:
    metadata:
      labels:
{{ include "mychart.labels" . | indent 8 }}
```

**Why:** `nindent` adds a newline before indenting, which is usually what you want in YAML.

### 7. Use `toYaml` for Complex Structures

**Good:**
```yaml
{{- with .Values.resources }}
resources:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

**Why:** Allows users to specify complex YAML structures in values without template complexity.

### 8. Conditional Resource Creation

**Good:**
```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "mychart.fullname" . }}
# ... ingress definition
{{- end }}
```

**Why:** Allows users to optionally enable/disable resources.

### 9. Use `with` for Scoping

**Good:**
```yaml
{{- with .Values.nodeSelector }}
nodeSelector:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

**Why:** Changes the scope of `.` to the specified value, making templates cleaner.

### 10. Template Comments

**Good:**
```yaml
{{- /*
This helper creates the fullname for resources.
It supports nameOverride and fullnameOverride values.
*/ -}}
{{- define "mychart.fullname" -}}
{{- end }}
```

**Bad:**
```yaml
# This creates the fullname
{{- define "mychart.fullname" -}}
{{- end }}
```

**Why:** Template comments (`{{- /* */ -}}`) are removed during rendering, while YAML comments (`#`) remain in output.

## Values File Best Practices

### 1. Use Flat Structures When Possible

**Good (Simple):**
```yaml
replicaCount: 1
imagePullPolicy: IfNotPresent
```

**Good (Related Settings):**
```yaml
image:
  repository: nginx
  pullPolicy: IfNotPresent
  tag: "1.21.0"
```

**Bad (Overly Nested):**
```yaml
app:
  deployment:
    pod:
      container:
        image:
          repository: nginx
```

### 2. Document All Values

**Good:**
```yaml
# replicaCount is the number of pod replicas for the deployment
replicaCount: 1

# image configures the container image
image:
  # image.repository is the container image registry and name
  repository: nginx
  # image.pullPolicy is the image pull policy
  pullPolicy: IfNotPresent
  # image.tag overrides the image tag (default is chart appVersion)
  tag: "1.21.0"
```

**Why:** Makes charts self-documenting and easier to use.

### 3. Provide Sensible Defaults

**Good:**
```yaml
replicaCount: 1

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

**Why:** Charts should work out of the box with minimal configuration.

### 4. Use Boolean Flags for Feature Toggles

**Good:**
```yaml
ingress:
  enabled: false
  className: ""
  annotations: {}
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []
```

**Why:** Makes it clear when features are optional and how to enable them.

### 5. Group Related Configuration

**Good:**
```yaml
autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80
```

### 6. Provide Empty Structures for Optional Config

**Good:**
```yaml
nodeSelector: {}
tolerations: []
affinity: {}
```

**Why:** Shows users what optional configurations are available.

## Kubernetes Resource Best Practices

### 1. Always Set Resource Limits and Requests

**Good:**
```yaml
resources:
  limits:
    cpu: 100m
    memory: 128Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

**Why:** Ensures proper scheduling and prevents resource exhaustion.

### 2. Use Proper Label Conventions

**Good:**
```yaml
metadata:
  labels:
    app.kubernetes.io/name: {{ include "mychart.name" . }}
    app.kubernetes.io/instance: {{ .Release.Name }}
    app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
    app.kubernetes.io/managed-by: {{ .Release.Service }}
    helm.sh/chart: {{ include "mychart.chart" . }}
```

**Why:** Follows Kubernetes recommended labels for better tooling integration.

### 3. Use SecurityContext

**Good:**
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 2000
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: true
```

**Why:** Improves security posture.

### 4. Define Probes

**Good:**
```yaml
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
```

**Why:** Ensures Kubernetes can properly manage application health.

### 5. Use ConfigMaps and Secrets Appropriately

**Good:**
```yaml
# ConfigMap for non-sensitive config
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}
data:
  app.conf: |
    {{- .Values.config | nindent 4 }}
```

```yaml
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "mychart.fullname" . }}
type: Opaque
data:
  password: {{ .Values.password | b64enc }}
```

## Template Function Reference

### String Functions

- `quote` - Quote a string
- `squote` - Single quote a string
- `trim` - Remove whitespace
- `trimSuffix` - Remove suffix
- `trimPrefix` - Remove prefix
- `upper` - Convert to uppercase
- `lower` - Convert to lowercase
- `title` - Title case
- `trunc` - Truncate string
- `repeat` - Repeat string
- `substr` - Substring
- `nospace` - Remove all whitespace

### Type Conversion

- `toYaml` - Convert to YAML
- `fromYaml` - Parse YAML
- `toJson` - Convert to JSON
- `fromJson` - Parse JSON
- `toString` - Convert to string
- `toStrings` - Convert list to strings

### Flow Control

- `default` - Provide default value
- `required` - Require a value
- `fail` - Fail with error message
- `coalesce` - Return first non-empty value

### Collections

- `list` - Create a list
- `dict` - Create a dictionary
- `merge` - Merge dictionaries
- `pick` - Pick keys from dictionary
- `omit` - Omit keys from dictionary
- `keys` - Get dictionary keys
- `values` - Get dictionary values

### Encoding

- `b64enc` - Base64 encode
- `b64dec` - Base64 decode
- `sha256sum` - SHA256 hash

## Testing Best Practices

### 1. Create Test Resources

**Good:**
```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "mychart.fullname" . }}-test-connection"
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "mychart.fullname" . }}:{{ .Values.service.port }}']
  restartPolicy: Never
```

**Run tests:**
```bash
helm test <release-name>
```

### 2. Test with Multiple Values

```bash
# Test with production values
helm template my-release ./mychart -f values-prod.yaml

# Test with development values
helm template my-release ./mychart -f values-dev.yaml

# Test with overrides
helm template my-release ./mychart --set replicaCount=3
```

### 3. Validate Before Installing

```bash
# Lint the chart
helm lint ./mychart

# Dry-run install
helm install my-release ./mychart --dry-run --debug

# Validate against cluster
helm install my-release ./mychart --dry-run
```

## Security Best Practices

### 1. Don't Hardcode Secrets

**Bad:**
```yaml
data:
  password: cGFzc3dvcmQ=  # Don't do this!
```

**Good:**
```yaml
data:
  password: {{ .Values.password | b64enc }}
```

### 2. Use RBAC

**Good:**
```yaml
{{- if .Values.serviceAccount.create -}}
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{ include "mychart.serviceAccountName" . }}
{{- end }}
```

### 3. Run as Non-Root

**Good:**
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
```

### 4. Drop Capabilities

**Good:**
```yaml
securityContext:
  capabilities:
    drop:
      - ALL
```

## Performance Best Practices

### 1. Use `.helmignore`

Exclude unnecessary files from the chart package:

```
# .helmignore
.git/
.gitignore
*.md
.DS_Store
*.swp
test/
```

### 2. Minimize Template Complexity

**Good:**
```yaml
{{- with .Values.resources }}
resources:
  {{- toYaml . | nindent 2 }}
{{- end }}
```

**Bad:**
```yaml
resources:
  {{- if .Values.resources.limits }}
  limits:
    {{- if .Values.resources.limits.cpu }}
    cpu: {{ .Values.resources.limits.cpu }}
    {{- end }}
    {{- if .Values.resources.limits.memory }}
    memory: {{ .Values.resources.limits.memory }}
    {{- end }}
  {{- end }}
  # ... more nested conditionals
```

### 3. Use Helpers for Repeated Logic

Don't repeat the same template logic in multiple places - extract it to a helper.

## Version Control Best Practices

### 1. Use SemVer for Chart Versions

- `MAJOR.MINOR.PATCH`
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### 2. Maintain a CHANGELOG

Document changes between versions.

### 3. Tag Releases

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

## Common Pitfalls to Avoid

### 1. Not Using `-` for Whitespace Control

**Bad:**
```yaml
{{ if .Values.enabled }}
  key: value
{{ end }}
```

**Good:**
```yaml
{{- if .Values.enabled }}
  key: value
{{- end }}
```

### 2. Not Truncating Resource Names

Kubernetes resource names must be <= 63 characters:

**Bad:**
```yaml
name: {{ .Release.Name }}-{{ .Chart.Name }}-deployment
```

**Good:**
```yaml
name: {{ include "mychart.fullname" . | trunc 63 | trimSuffix "-" }}
```

### 3. Using `template` Instead of `include`

Use `include` when you need to pipe the output to other functions.

### 4. Not Validating User Input

**Bad:**
```yaml
replicas: {{ .Values.replicaCount }}
```

**Good:**
```yaml
replicas: {{ required "replicaCount is required" .Values.replicaCount }}
```

### 5. Hardcoding Values in Templates

**Bad:**
```yaml
image: nginx:1.21.0
```

**Good:**
```yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
```

## Upgrade and Migration Best Practices

### 1. Use Helm Hooks

```yaml
metadata:
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "1"
    "helm.sh/hook-delete-policy": hook-succeeded
```

Available hooks:
- `pre-install`
- `post-install`
- `pre-upgrade`
- `post-upgrade`
- `pre-delete`
- `post-delete`
- `pre-rollback`
- `post-rollback`
- `test`

### 2. Test Upgrades

```bash
# Show what would change
helm diff upgrade my-release ./mychart

# Dry-run upgrade
helm upgrade my-release ./mychart --dry-run --debug
```

### 3. Support Rolling Back

Ensure your charts support rollback by not using hooks that delete critical resources.

## Documentation Best Practices

### 1. Create a Comprehensive README

Include:
- Chart description
- Prerequisites
- Installation instructions
- Configuration options (values)
- Examples
- Upgrade notes

### 2. Document Template Functions

Add comments to your `_helpers.tpl`:

```yaml
{{- /*
mychart.fullname generates a fully qualified application name.
It supports fullnameOverride and nameOverride values.
Maximum length is 63 characters per DNS naming spec.
Usage: {{ include "mychart.fullname" . }}
*/ -}}
{{- define "mychart.fullname" -}}
{{- end }}
```

### 3. Provide NOTES.txt

Create `templates/NOTES.txt` with post-installation instructions:

```
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}

{{- if .Values.ingress.enabled }}
Application URL:
{{- range .Values.ingress.hosts }}
  http{{ if $.Values.ingress.tls }}s{{ end }}://{{ . }}{{ $.Values.ingress.path }}
{{- end }}
{{- end }}
```

## Packaging and Distribution

### 1. Package the Chart

```bash
helm package ./mychart
```

### 2. Create Chart Repository

```bash
# Create index
helm repo index .

# Serve repository
helm serve
```

### 3. Publish to Artifact Hub

Create `artifacthub-repo.yml` in your repository:

```yaml
repositoryID: <uuid>
owners:
  - name: Your Name
    email: your.email@example.com
```

## Summary Checklist

Before releasing a chart, verify:

- [ ] Chart.yaml has all required fields
- [ ] values.yaml has sensible defaults
- [ ] All values are documented
- [ ] Templates use helpers for repeated logic
- [ ] Resource names are properly truncated
- [ ] Labels follow Kubernetes conventions
- [ ] Resources have limits and requests
- [ ] SecurityContext is defined
- [ ] Probes are configured
- [ ] Secrets are parameterized, not hardcoded
- [ ] `helm lint` passes
- [ ] `helm template` renders successfully
- [ ] Dry-run install succeeds
- [ ] Tests are defined and pass
- [ ] README.md is comprehensive
- [ ] NOTES.txt provides helpful post-install info
- [ ] Chart version follows SemVer
- [ ] .helmignore excludes unnecessary files

---

## Reference: K8S_Best_Practices

# Kubernetes YAML Best Practices

This reference provides comprehensive best practices for creating, maintaining, and validating Kubernetes resources in Helm charts.

## General YAML Best Practices

### Formatting and Style

- Use 2 spaces for indentation (not tabs)
- Keep lines under 120 characters when possible
- Use lowercase for keys
- Quote string values containing special characters
- Always specify apiVersion and kind
- Include metadata.name for all resources
- Use consistent naming conventions (lowercase, hyphens for separators)

### Resource Organization

- One resource per file for clarity (unless logically grouped)
- Use `---` to separate multiple resources in a single file
- Name files descriptively: `<resource-type>-<name>.yaml`
- Group related resources together (e.g., deployment + service + configmap)

## Metadata Best Practices

### Standard Metadata Structure

```yaml
metadata:
  name: my-app
  namespace: production
  labels:
    app.kubernetes.io/name: my-app
    app.kubernetes.io/instance: my-app-prod
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/component: backend
    app.kubernetes.io/part-of: my-system
    app.kubernetes.io/managed-by: helm
    helm.sh/chart: my-app-1.0.0
  annotations:
    description: "Backend service for my-app"
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
```

### Kubernetes Recommended Labels

Always include these standard labels for better tooling integration:

| Label | Description | Example |
|-------|-------------|---------|
| `app.kubernetes.io/name` | Application name | `nginx` |
| `app.kubernetes.io/instance` | Unique instance identifier | `nginx-prod` |
| `app.kubernetes.io/version` | Application version | `1.21.0` |
| `app.kubernetes.io/component` | Component within architecture | `frontend` |
| `app.kubernetes.io/part-of` | Higher-level application | `wordpress` |
| `app.kubernetes.io/managed-by` | Tool managing the resource | `helm` |

### Helm-Specific Labels

```yaml
labels:
  helm.sh/chart: {{ include "mychart.chart" . }}
  app.kubernetes.io/managed-by: {{ .Release.Service }}
```

## Labels and Selectors

### Selector Best Practices

- Selectors must match pod labels exactly
- Use immutable selectors (they cannot be changed after creation)
- Keep selector labels minimal but unique

**Good:**
```yaml
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: my-app
      app.kubernetes.io/instance: my-app-prod
  template:
    metadata:
      labels:
        app.kubernetes.io/name: my-app
        app.kubernetes.io/instance: my-app-prod
        app.kubernetes.io/version: "1.0.0"  # Additional labels OK
```

**Bad:**
```yaml
spec:
  selector:
    matchLabels:
      app: my-app
      version: "1.0.0"  # Version in selector prevents rolling updates!
```

### Label Key Conventions

- Use DNS subdomain format for prefixed keys: `prefix/key`
- Keys without prefix are private to the user
- Standard prefixes: `app.kubernetes.io/`, `helm.sh/`, `kubernetes.io/`

## Resource Limits and Requests

### Why They Matter

- **Requests**: Minimum resources guaranteed to the container
- **Limits**: Maximum resources the container can use
- Required for proper scheduling, QoS class assignment, and cluster stability

### Recommended Configuration

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "100m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

### Guidelines by Resource Type

| Resource Type | Requests | Limits | Notes |
|---------------|----------|--------|-------|
| CPU | Set always | Optional | Consider burstable workloads |
| Memory | Set always | Set always | Prevents OOM kills |
| Ephemeral Storage | Optional | Recommended | For disk-intensive apps |

### QoS Classes

Kubernetes assigns Quality of Service classes based on resource settings:

1. **Guaranteed**: requests == limits for all containers
2. **Burstable**: At least one container has requests < limits
3. **BestEffort**: No requests or limits set (not recommended)

```yaml
# Guaranteed QoS
resources:
  requests:
    memory: "128Mi"
    cpu: "500m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

### Memory Guidelines

- Set memory limits to prevent OOM kills affecting other pods
- Memory is incompressible - exceeding limits causes termination
- Monitor actual usage before setting production values

### CPU Guidelines

- CPU is compressible - exceeding limits causes throttling, not termination
- Consider not setting CPU limits for burstable workloads
- Use millicores: `100m` = 0.1 CPU core

## Probes Configuration

### Liveness Probe

Determines if the container should be restarted:

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
    httpHeaders:
      - name: X-Health-Check
        value: liveness
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
  successThreshold: 1
```

### Readiness Probe

Determines if the container can receive traffic:

```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
  successThreshold: 1
```

### Startup Probe

For slow-starting containers (Kubernetes 1.18+):

```yaml
startupProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 0
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 30  # 30 * 10 = 300s max startup time
  successThreshold: 1
```

### Probe Types

| Type | Use Case | Example |
|------|----------|---------|
| `httpGet` | HTTP endpoints | REST APIs, web apps |
| `tcpSocket` | TCP connections | Databases, message queues |
| `exec` | Custom scripts | Complex health checks |
| `grpc` | gRPC services | gRPC health protocol |

### Probe Best Practices

- **Liveness**: Check if app is running, not dependencies
- **Readiness**: Check if app can serve traffic (including dependencies)
- **Startup**: Use for slow-starting apps instead of long `initialDelaySeconds`
- Set appropriate timeouts to prevent false positives
- Don't make probes too aggressive (high CPU overhead)

## Security Context

### Pod-Level Security Context

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    fsGroupChangePolicy: "OnRootMismatch"
    seccompProfile:
      type: RuntimeDefault
```

### Container-Level Security Context

```yaml
containers:
  - name: app
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      runAsNonRoot: true
      runAsUser: 1000
      capabilities:
        drop:
          - ALL
        add:
          - NET_BIND_SERVICE  # Only if needed
      seccompProfile:
        type: RuntimeDefault
```

### Security Context Fields Explained

| Field | Level | Description |
|-------|-------|-------------|
| `runAsNonRoot` | Pod/Container | Prevents running as root |
| `runAsUser` | Pod/Container | Specifies UID to run as |
| `runAsGroup` | Pod/Container | Specifies GID to run as |
| `fsGroup` | Pod | Group ownership for volumes |
| `readOnlyRootFilesystem` | Container | Makes root filesystem read-only |
| `allowPrivilegeEscalation` | Container | Prevents privilege escalation |
| `capabilities` | Container | Linux capabilities management |
| `seccompProfile` | Pod/Container | Syscall filtering |

### Recommended Security Baseline

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
```

## Image Management

### Image Specification Best Practices

```yaml
containers:
  - name: app
    image: registry.example.com/my-app:v1.2.3
    imagePullPolicy: IfNotPresent
```

### Image Pull Policy

| Policy | When to Use |
|--------|-------------|
| `Always` | For `:latest` tags or mutable tags |
| `IfNotPresent` | For immutable tags (recommended) |
| `Never` | For pre-loaded images (rare) |

### Image Best Practices

- **Always use specific tags**: Never use `:latest` in production
- **Use digest for immutability**: `image@sha256:abc123...`
- **Use private registries**: For security and reliability
- **Scan images**: Implement vulnerability scanning in CI/CD

```yaml
# Recommended: Specific tag
image: nginx:1.21.6

# Better: Digest for immutability
image: nginx@sha256:2834dc507516af02784808c5f48b7cbe38b8ed5d0f4837f16e78d00deb7e7767

# Avoid: Mutable tags
image: nginx:latest  # Don't do this in production
```

## Pod Disruption Budgets

### Why PDBs Matter

Pod Disruption Budgets ensure high availability during voluntary disruptions like:
- Node drains
- Cluster upgrades
- Deployment rollouts

### PDB Configuration

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
spec:
  # Option 1: Minimum available pods
  minAvailable: 2

  # Option 2: Maximum unavailable pods (use one, not both)
  # maxUnavailable: 1

  selector:
    matchLabels:
      app.kubernetes.io/name: my-app
```

### PDB Best Practices

- Set PDB for all production workloads with multiple replicas
- Use `minAvailable` when you need minimum capacity guarantee
- Use `maxUnavailable` when you want to limit disruption rate
- Don't set `minAvailable` equal to replicas (blocks all disruptions)

```yaml
# Good: Allows 1 pod to be unavailable
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ include "mychart.fullname" . }}-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
```

## Horizontal Pod Autoscaler

### HPA Configuration

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

### HPA Best Practices

- Always set resource requests (required for CPU/memory-based scaling)
- Set appropriate `minReplicas` for base capacity
- Use stabilization windows to prevent flapping
- Consider custom metrics for business-specific scaling
- Don't use HPA with `replicas` field in Deployment (conflicts)

### Helm Template for HPA

```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "mychart.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
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
{{- end }}
```

## Network Policies

### Default Deny All

Start with a default deny policy, then allow specific traffic:

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

### Allow Specific Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8080
```

### Allow Egress to External Services

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-to-database
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 10.0.0.0/8
      ports:
        - protocol: TCP
          port: 5432
    # Allow DNS resolution
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### Network Policy Best Practices

- Start with default deny, then allow specific traffic
- Always allow DNS egress (UDP port 53)
- Use namespace selectors for cross-namespace communication
- Label namespaces for policy targeting
- Test policies in staging before production

## Service Configuration

### Service Types

| Type | Use Case |
|------|----------|
| `ClusterIP` | Internal cluster communication (default) |
| `NodePort` | External access via node ports (30000-32767) |
| `LoadBalancer` | Cloud provider load balancers |
| `ExternalName` | DNS CNAME for external services |

### Service Best Practices

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "mychart.selectorLabels" . | nindent 4 }}
```

### Named Ports

Always use named ports for clarity:

```yaml
# In Deployment
ports:
  - name: http
    containerPort: 8080
    protocol: TCP
  - name: metrics
    containerPort: 9090
    protocol: TCP

# In Service
ports:
  - name: http
    port: 80
    targetPort: http  # References named port
```

## ConfigMaps and Secrets

### ConfigMap Best Practices

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}-config
data:
  # For simple key-value pairs
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"

  # For file content
  app.properties: |
    server.port=8080
    server.host=0.0.0.0
```

### Secret Best Practices

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "mychart.fullname" . }}-secret
type: Opaque
data:
  # Base64 encoded values
  password: {{ .Values.password | b64enc | quote }}
  api-key: {{ .Values.apiKey | b64enc | quote }}
stringData:
  # Plain text (will be encoded)
  config.yaml: |
    database:
      host: {{ .Values.database.host }}
```

### Mounting as Environment Variables

```yaml
env:
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: my-config
        key: LOG_LEVEL
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: my-secret
        key: password
```

### Mounting as Files

```yaml
volumes:
  - name: config
    configMap:
      name: my-config
  - name: secrets
    secret:
      secretName: my-secret
      defaultMode: 0400

volumeMounts:
  - name: config
    mountPath: /etc/config
    readOnly: true
  - name: secrets
    mountPath: /etc/secrets
    readOnly: true
```

## Common Validation Issues

### Missing Required Fields

| Issue | Fix |
|-------|-----|
| Missing `apiVersion` | Add appropriate API version |
| Missing `kind` | Add resource kind |
| Missing `metadata.name` | Add resource name |
| Missing `spec.selector` | Add pod selector for Deployments/Services |
| Empty `containers` | Add at least one container |

### Selector Mismatches

```yaml
# Error: Selector doesn't match pod labels
spec:
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        application: my-app  # Wrong label key!
```

### Invalid Values

| Field | Valid Format | Example |
|-------|--------------|---------|
| CPU | Millicores or decimal | `500m`, `0.5` |
| Memory | Binary units | `512Mi`, `1Gi` |
| Port | 1-65535 | `8080` |
| DNS names | Lowercase alphanumeric with hyphens | `my-app-service` |

### Namespace Issues

- Not all resources are namespaced (e.g., ClusterRole, PersistentVolume)
- Services must be in the same namespace as pods they target
- Default namespace is "default" if not specified

## Deprecation Warnings

### Deprecated APIs

| Old API | New API | K8s Version |
|---------|---------|-------------|
| `extensions/v1beta1` Deployment | `apps/v1` | 1.16+ |
| `extensions/v1beta1` Ingress | `networking.k8s.io/v1` | 1.19+ |
| `networking.k8s.io/v1beta1` Ingress | `networking.k8s.io/v1` | 1.19+ |
| `policy/v1beta1` PodDisruptionBudget | `policy/v1` | 1.21+ |
| `policy/v1beta1` PodSecurityPolicy | Removed (use PSA) | 1.25+ |
| `autoscaling/v2beta1` HPA | `autoscaling/v2` | 1.23+ |
| `batch/v1beta1` CronJob | `batch/v1` | 1.21+ |

### Checking API Versions

```bash
# List available API versions
kubectl api-versions

# Check if resource supports specific version
kubectl api-resources | grep deployments
```

## CRD-Specific Considerations

### API Version Compatibility

- Check the CRD version installed in the cluster
- Use the correct apiVersion for the CRD
- Be aware of deprecations (e.g., v1alpha1 → v1beta1 → v1)

### Required Fields

- CRDs often have custom required fields in spec
- Check the CRD documentation for field requirements
- Use `kubectl explain <kind>` to see field documentation

### Validation

- CRDs may have custom validation rules
- OpenAPI schema validation is stricter in newer K8s versions
- Use dry-run to catch validation errors before applying

```bash
# Explain CRD fields
kubectl explain certificate.spec
kubectl explain certificate.spec.issuerRef
```

## Anti-Patterns to Avoid

### 1. Running as Root

```yaml
# Bad
securityContext:
  runAsUser: 0

# Good
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
```

### 2. Using Latest Tag

```yaml
# Bad
image: nginx:latest

# Good
image: nginx:1.21.6
```

### 3. No Resource Limits

```yaml
# Bad - No limits
containers:
  - name: app
    image: my-app:1.0

# Good - With limits
containers:
  - name: app
    image: my-app:1.0
    resources:
      limits:
        memory: "256Mi"
        cpu: "500m"
```

### 4. Privileged Containers

```yaml
# Bad
securityContext:
  privileged: true

# Good
securityContext:
  privileged: false
  allowPrivilegeEscalation: false
```

### 5. No Probes

```yaml
# Bad - No health checks
containers:
  - name: app

# Good - With probes
containers:
  - name: app
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
```

## Summary Checklist

Before deploying Kubernetes resources, verify:

### Required
- [ ] `apiVersion` and `kind` are correct
- [ ] `metadata.name` follows naming conventions
- [ ] Labels include recommended Kubernetes labels
- [ ] Selectors match pod labels exactly
- [ ] At least one container is defined

### Recommended
- [ ] Resource requests and limits are set
- [ ] Liveness and readiness probes are configured
- [ ] Security context is defined (non-root, read-only fs)
- [ ] Image uses specific tag (not `latest`)
- [ ] Secrets are used for sensitive data (not ConfigMaps)

### Production
- [ ] Pod Disruption Budget is configured
- [ ] Network Policies are in place
- [ ] HPA is configured for scalable workloads
- [ ] Service accounts are properly scoped
- [ ] Pod anti-affinity for high availability

---

## Reference: Template_Functions

# Helm Template Functions Reference

This reference provides a comprehensive guide to Helm template functions, including built-in functions and Sprig library functions.

## Essential Helm Functions

### include

Includes a named template and allows piping the output to other functions.

**Syntax:**
```yaml
{{ include "template.name" . }}
```

**Examples:**
```yaml
# Include and indent
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}

# Include and quote
value: {{ include "mychart.value" . | quote }}

# Include with custom context
{{- include "mychart.container" (dict "root" . "container" .Values.mainContainer) }}
```

**When to use:** Prefer `include` over `template` when you need to manipulate the output with functions.

### tpl

Evaluates a string as a template, allowing dynamic template rendering.

**Syntax:**
```yaml
{{ tpl <string> <context> }}
```

**Examples:**
```yaml
# Render a value as template
{{ tpl .Values.customConfig . }}

# Render external file as template
{{ tpl (.Files.Get "config/app.conf") . }}

# values.yaml
customConfig: |
  server:
    host: {{ .Values.server.host }}
    port: {{ .Values.server.port }}
```

**When to use:** When users need to provide template strings in values or external files.

### required

Enforces that a value must be provided, failing with a custom error message if missing.

**Syntax:**
```yaml
{{ required "error message" .Values.path }}
```

**Examples:**
```yaml
# Require a critical value
apiVersion: v1
kind: Service
metadata:
  name: {{ required "A valid service name is required!" .Values.service.name }}

# Require database password
data:
  password: {{ required "database.password must be set" .Values.database.password | b64enc }}

# Require multiple values
env:
  - name: API_KEY
    value: {{ required "apiKey must be provided" .Values.apiKey | quote }}
```

**When to use:** For critical values that have no sensible default.

### lookup

Queries existing Kubernetes resources in the cluster during template rendering.

**Syntax:**
```yaml
{{ lookup "apiVersion" "kind" "namespace" "name" }}
```

**Examples:**
```yaml
# Look up existing secret
{{- $secret := lookup "v1" "Secret" .Release.Namespace "my-secret" }}
{{- if $secret }}
  # Secret exists, use existing password
  password: {{ $secret.data.password }}
{{- else }}
  # Create new password
  password: {{ randAlphaNum 16 | b64enc }}
{{- end }}

# List all pods in namespace
{{- $pods := lookup "v1" "Pod" .Release.Namespace "" }}

# Get specific resource
{{- $cm := lookup "v1" "ConfigMap" "default" "my-config" }}
```

**⚠️ Cautions:**
- Only works during `helm install` and `helm upgrade`, not with `helm template`
- Requires cluster access
- Can slow down rendering
- Creates tight coupling between chart and cluster state

**When to use:** When you need to check for existing resources or migrate from existing deployments.

## String Functions

### quote / squote

Wraps a string in double or single quotes.

**Examples:**
```yaml
# Double quotes
env:
  - name: HOST
    value: {{ .Values.host | quote }}  # Output: "localhost"

# Single quotes
value: {{ .Values.name | squote }}  # Output: 'myapp'
```

### default

Provides a fallback value if the input is empty.

**Examples:**
```yaml
# Simple default
replicas: {{ .Values.replicaCount | default 1 }}

# Chain with other functions
image: {{ .Values.image.tag | default .Chart.AppVersion | quote }}

# Default for nested values
{{ .Values.server.port | default 8080 }}
```

### trim / trimSuffix / trimPrefix

Removes whitespace or specific strings.

**Examples:**
```yaml
# Remove whitespace
name: {{ .Values.name | trim }}

# Remove suffix
name: {{ .Release.Name | trimSuffix "-dev" }}

# Remove prefix
name: {{ .Values.fullName | trimPrefix "app-" }}

# Common pattern for resource names
name: {{ include "mychart.fullname" . | trunc 63 | trimSuffix "-" }}
```

### upper / lower / title

Changes string case.

**Examples:**
```yaml
# Uppercase
env: {{ .Values.environment | upper }}  # Output: PRODUCTION

# Lowercase
name: {{ .Values.name | lower }}  # Output: myapp

# Title case
label: {{ .Values.label | title }}  # Output: My Application
```

### trunc

Truncates a string to a specified length.

**Examples:**
```yaml
# Truncate to 63 chars (K8s DNS limit)
name: {{ .Release.Name | trunc 63 | trimSuffix "-" }}

# Truncate to 20 chars
shortName: {{ .Values.name | trunc 20 }}
```

### repeat

Repeats a string N times.

**Examples:**
```yaml
# Repeat string
value: {{ "=" | repeat 10 }}  # Output: ==========

# Create separator
comment: {{ "#" | repeat 20 }}  # Output: ####################
```

### replace

Replaces occurrences of a substring.

**Examples:**
```yaml
# Replace underscores with hyphens
name: {{ .Values.name | replace "_" "-" }}

# Replace spaces
label: {{ .Values.label | replace " " "-" | lower }}

# Chart label (replace + with _)
chart: {{ printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" }}
```

### substr

Extracts a substring.

**Examples:**
```yaml
# Get first 10 characters
short: {{ .Values.name | substr 0 10 }}

# Get characters 5-15
middle: {{ .Values.name | substr 5 15 }}
```

### nospace

Removes all whitespace from a string.

**Examples:**
```yaml
# Remove all spaces
compact: {{ .Values.value | nospace }}  # "hello world" → "helloworld"
```

### contains / hasPrefix / hasSuffix

Checks if a string contains, starts with, or ends with a substring.

**Examples:**
```yaml
# Check if contains
{{- if contains "prod" .Values.environment }}
  # Production configuration
{{- end }}

# Check prefix
{{- if hasPrefix "app-" .Values.name }}
  name: {{ .Values.name }}
{{- else }}
  name: {{ printf "app-%s" .Values.name }}
{{- end }}

# Check suffix
{{- if hasSuffix "-service" .Values.name }}
  # Already has suffix
{{- end }}
```

## Type Conversion Functions

### toYaml / fromYaml

Converts between Go objects and YAML strings.

**Examples:**
```yaml
# Convert to YAML
{{- with .Values.resources }}
resources:
  {{- toYaml . | nindent 2 }}
{{- end }}

# Parse YAML string
{{- $config := .Values.configYaml | fromYaml }}
{{- $config.database.host }}
```

### toJson / fromJson

Converts between Go objects and JSON strings.

**Examples:**
```yaml
# Convert to JSON
data:
  config.json: |
    {{- .Values.config | toJson | nindent 4 }}

# Parse JSON
{{- $data := .Values.jsonString | fromJson }}
{{- $data.key }}
```

### toString

Converts any value to a string.

**Examples:**
```yaml
# Convert number to string
port: {{ .Values.port | toString | quote }}

# Convert boolean to string
enabled: {{ .Values.enabled | toString }}
```

## List/Array Functions

### list

Creates a list.

**Examples:**
```yaml
# Create list
{{- $myList := list "a" "b" "c" }}

# Pass multiple arguments to template
{{- include "mychart.template" (list . "arg1" "arg2") }}
```

### append / prepend

Adds elements to a list.

**Examples:**
```yaml
# Append to list
{{- $list := list "a" "b" }}
{{- $list = append $list "c" }}  # ["a", "b", "c"]

# Prepend to list
{{- $list := list "b" "c" }}
{{- $list = prepend $list "a" }}  # ["a", "b", "c"]
```

### first / rest / last

Gets elements from a list.

**Examples:**
```yaml
# Get first element
{{- $first := first $myList }}

# Get all but first
{{- $rest := rest $myList }}

# Get last element
{{- $last := last $myList }}
```

### has

Checks if a list contains an element.

**Examples:**
```yaml
{{- if has "production" .Values.environments }}
  # Production configuration
{{- end }}
```

### compact

Removes empty/nil elements from a list.

**Examples:**
```yaml
{{- $list := list "a" "" "b" nil "c" }}
{{- $cleaned := compact $list }}  # ["a", "b", "c"]
```

### uniq

Removes duplicate elements.

**Examples:**
```yaml
{{- $list := list "a" "b" "a" "c" "b" }}
{{- $unique := uniq $list }}  # ["a", "b", "c"]
```

### sortAlpha

Sorts list alphabetically.

**Examples:**
```yaml
{{- $sorted := .Values.items | sortAlpha }}
```

## Dictionary/Map Functions

### dict

Creates a dictionary.

**Examples:**
```yaml
# Create dict
{{- $myDict := dict "key1" "value1" "key2" "value2" }}

# Pass custom context to template
{{- include "mychart.template" (dict "root" . "custom" "value") }}

# Complex context
{{- $ctx := dict "top" . "container" .Values.mainContainer "port" .Values.service.port }}
{{- include "mychart.container" $ctx }}
```

### merge / mergeOverwrite

Merges dictionaries.

**Examples:**
```yaml
# Merge dictionaries (dest, src1, src2, ...)
{{- $defaults := dict "replicas" 1 "port" 80 }}
{{- $overrides := dict "replicas" 3 }}
{{- $final := merge $overrides $defaults }}
# Result: {"replicas": 3, "port": 80}

# mergeOverwrite (right-most wins)
{{- $result := mergeOverwrite $dict1 $dict2 }}
```

### keys / values

Gets keys or values from a dictionary.

**Examples:**
```yaml
# Get all keys
{{- $keys := keys .Values.config }}

# Get all values
{{- $vals := values .Values.config }}

# Iterate over keys
{{- range $key := keys .Values.labels | sortAlpha }}
  {{ $key }}: {{ index $.Values.labels $key }}
{{- end }}
```

### pick / omit

Selects or excludes keys from a dictionary.

**Examples:**
```yaml
# Pick specific keys
{{- $subset := pick .Values.config "host" "port" }}

# Omit specific keys
{{- $filtered := omit .Values.config "password" "secret" }}
```

### hasKey

Checks if a dictionary has a key.

**Examples:**
```yaml
{{- if hasKey .Values "database" }}
  {{- if hasKey .Values.database "password" }}
    # Password is configured
  {{- end }}
{{- end }}
```

### pluck

Gets a value by key from multiple dictionaries.

**Examples:**
```yaml
# Get "name" from first dict that has it
{{- $name := pluck "name" .Values.override .Values.defaults | first }}
```

## Encoding Functions

### b64enc / b64dec

Base64 encode/decode.

**Examples:**
```yaml
# Encode secret
apiVersion: v1
kind: Secret
data:
  password: {{ .Values.password | b64enc }}

# Decode existing secret
{{- $secret := lookup "v1" "Secret" .Release.Namespace "my-secret" }}
{{- if $secret }}
  {{- $decoded := $secret.data.password | b64dec }}
{{- end }}
```

### sha256sum

Generates SHA256 hash.

**Examples:**
```yaml
# Create checksum annotation to trigger rolling update
annotations:
  checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}

# Hash password
data:
  passwordHash: {{ .Values.password | sha256sum }}
```

### uuidv4

Generates a random UUID v4.

**Examples:**
```yaml
# Generate unique ID
id: {{ uuidv4 }}
```

## Mathematical Functions

### add / sub / mul / div / mod

Basic arithmetic operations.

**Examples:**
```yaml
# Addition
replicas: {{ add .Values.baseReplicas 2 }}

# Subtraction
port: {{ sub .Values.maxPort 100 }}

# Multiplication
memory: {{ mul .Values.memoryPerPod .Values.replicas }}

# Division
cpuPerPod: {{ div .Values.totalCpu .Values.replicas }}

# Modulo
remainder: {{ mod .Values.value 10 }}
```

### max / min

Gets maximum or minimum value.

**Examples:**
```yaml
# Ensure at least 1 replica
replicas: {{ max 1 .Values.replicaCount }}

# Cap at 10 replicas
replicas: {{ min 10 .Values.replicaCount }}
```

### floor / ceil / round

Rounding functions.

**Examples:**
```yaml
# Round down
value: {{ floor 3.7 }}  # 3

# Round up
value: {{ ceil 3.2 }}  # 4

# Round to nearest
value: {{ round 3.5 }}  # 4
```

## Date Functions

### now

Gets current time.

**Examples:**
```yaml
# Current timestamp
annotations:
  timestamp: {{ now | date "2006-01-02T15:04:05Z" }}
```

### date

Formats a date/time.

**Examples:**
```yaml
# Format date
date: {{ now | date "2006-01-02" }}  # 2024-01-15

# Full timestamp
timestamp: {{ now | date "2006-01-02T15:04:05Z07:00" }}

# Custom format
generated: {{ now | date "Monday, 02-Jan-06 15:04:05 MST" }}
```

### dateModify

Modifies a date.

**Examples:**
```yaml
# Add 24 hours
tomorrow: {{ now | dateModify "24h" }}

# Subtract 7 days
lastWeek: {{ now | dateModify "-168h" }}
```

## Comparison Functions

### eq / ne

Equality and inequality.

**Examples:**
```yaml
{{- if eq .Values.environment "production" }}
  # Production settings
{{- end }}

{{- if ne .Values.replicaCount 1 }}
  # Multiple replicas
{{- end }}
```

### lt / le / gt / ge

Less than, less than or equal, greater than, greater than or equal.

**Examples:**
```yaml
{{- if gt .Values.replicaCount 1 }}
  # Multiple replicas
{{- end }}

{{- if le .Values.maxConnections 100 }}
  # Low connection count
{{- end }}
```

### and / or / not

Logical operations.

**Examples:**
```yaml
{{- if and .Values.ingress.enabled .Values.ingress.tls.enabled }}
  # Ingress with TLS
{{- end }}

{{- if or (eq .Values.env "dev") (eq .Values.env "staging") }}
  # Non-production environment
{{- end }}

{{- if not .Values.production }}
  # Development mode
{{- end }}
```

## Flow Control Functions

### fail

Fails template rendering with an error message.

**Examples:**
```yaml
{{- if not .Values.required }}
  {{- fail "required value is not set" }}
{{- end }}

{{- if lt .Values.replicas 1 }}
  {{- fail "replicas must be at least 1" }}
{{- end }}
```

### coalesce

Returns the first non-empty value.

**Examples:**
```yaml
# Use first non-empty value
name: {{ coalesce .Values.nameOverride .Values.name .Chart.Name }}

# Multiple fallbacks
host: {{ coalesce .Values.database.host .Values.defaultHost "localhost" }}
```

### ternary

Inline if-then-else.

**Examples:**
```yaml
# Ternary operator
type: {{ ternary "LoadBalancer" "ClusterIP" .Values.production }}

# With comparison
replicas: {{ ternary 3 1 (eq .Values.env "production") }}
```

## Indentation Functions

### indent

Indents each line by N spaces.

**Examples:**
```yaml
# Indent by 4 spaces
metadata:
  labels:
{{ include "mychart.labels" . | indent 4 }}
```

### nindent

Adds a newline then indents.

**Examples:**
```yaml
# Newline + indent (preferred)
metadata:
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
```

**Why prefer nindent:** Most YAML structures need a newline before the indented content, making `nindent` the right choice in most cases.

## Random Functions

### randAlphaNum

Generates random alphanumeric string.

**Examples:**
```yaml
# Generate random password
{{- $password := randAlphaNum 16 }}

# Generate unique suffix
name: {{ printf "%s-%s" .Release.Name (randAlphaNum 5) }}
```

### randAlpha / randNumeric

Generates random alphabetic or numeric string.

**Examples:**
```yaml
# Random letters only
code: {{ randAlpha 8 }}

# Random numbers only
id: {{ randNumeric 6 }}
```

### randAscii

Generates random ASCII string.

**Examples:**
```yaml
# Random ASCII characters
token: {{ randAscii 32 }}
```

## File Functions

### Files.Get

Reads a file from the chart.

**Examples:**
```yaml
# Read configuration file
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}
data:
  config.yaml: |
    {{- .Files.Get "config/app.yaml" | nindent 4 }}
```

### Files.GetBytes

Reads a file as bytes (for binary files).

**Examples:**
```yaml
# Include binary file
data:
  image.png: {{ .Files.GetBytes "files/image.png" | b64enc }}
```

### Files.Glob

Reads multiple files matching a pattern.

**Examples:**
```yaml
# Include all YAML files
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}
data:
  {{- range $path, $content := .Files.Glob "config/*.yaml" }}
  {{ base $path }}: |
    {{- $content | nindent 4 }}
  {{- end }}
```

### Files.Lines

Reads a file line by line.

**Examples:**
```yaml
# Process file line by line
{{- range .Files.Lines "config/servers.txt" }}
  - {{ . }}
{{- end }}
```

### Files.AsConfig / Files.AsSecrets

Creates ConfigMap or Secret data from files.

**Examples:**
```yaml
# ConfigMap from files
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "mychart.fullname" . }}
data:
  {{- (.Files.Glob "config/*").AsConfig | nindent 2 }}

# Secret from files
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "mychart.fullname" . }}
data:
  {{- (.Files.Glob "secrets/*").AsSecrets | nindent 2 }}
```

## Path Functions

### base / dir / ext / clean

Path manipulation functions.

**Examples:**
```yaml
# Get filename
{{- $filename := base "/path/to/file.yaml" }}  # file.yaml

# Get directory
{{- $dir := dir "/path/to/file.yaml" }}  # /path/to

# Get extension
{{- $ext := ext "file.yaml" }}  # .yaml

# Clean path
{{- $clean := clean "/path//to/../file" }}  # /path/file
```

## Regex Functions

### regexMatch

Tests if a string matches a regex.

**Examples:**
```yaml
{{- if regexMatch "^[0-9]+$" .Values.port }}
  # Port is numeric
{{- end }}
```

### regexFind / regexFindAll

Finds regex matches.

**Examples:**
```yaml
# Find first match
{{- $match := regexFind "[0-9]+" .Values.version }}

# Find all matches
{{- $matches := regexFindAll "[A-Z]+" .Values.name -1 }}
```

### regexReplaceAll

Replaces regex matches.

**Examples:**
```yaml
# Replace all digits
name: {{ regexReplaceAll "[0-9]" .Values.name "" }}

# Replace pattern
clean: {{ regexReplaceAll "[^a-z0-9-]" .Values.name "" }}
```

### regexSplit

Splits string by regex.

**Examples:**
```yaml
# Split by delimiter
{{- $parts := regexSplit ":" .Values.imageTag -1 }}
```

## Semantic Version Functions

### semver / semverCompare

Work with semantic versions.

**Examples:**
```yaml
# Parse semantic version
{{- $version := semver "1.2.3" }}
{{- $version.Major }}  # 1
{{- $version.Minor }}  # 2
{{- $version.Patch }}  # 3

# Compare versions
{{- if semverCompare ">=1.20.0" .Capabilities.KubeVersion.Version }}
  # Kubernetes 1.20 or higher
{{- end }}
```

## Advanced Patterns

### Custom Context Passing

```yaml
{{- define "mychart.container" -}}
{{- $root := .root }}
{{- $container := .container }}
{{- $port := .port }}
name: {{ $container.name }}
image: {{ $container.image }}
ports:
  - containerPort: {{ $port }}
{{- end }}

# Usage
{{- include "mychart.container" (dict "root" . "container" .Values.mainContainer "port" 8080) }}
```

### Multi-Stage Processing

```yaml
{{- $config := .Values.configYaml | fromYaml }}
{{- $merged := merge .Values.overrides $config }}
{{- $filtered := omit $merged "internalKey" }}
{{- toYaml $filtered | nindent 2 }}
```

### Conditional Value Selection

```yaml
{{- $value := "" }}
{{- if .Values.custom }}
{{- $value = .Values.custom }}
{{- else if .Values.default }}
{{- $value = .Values.default }}
{{- else }}
{{- $value = "fallback" }}
{{- end }}
```

### Pipeline Composition

```yaml
# Chain multiple functions
value: {{ .Values.name | trim | lower | replace " " "-" | trunc 63 | trimSuffix "-" | quote }}

# Multi-line pipeline
{{- .Values.config
  | toYaml
  | indent 2
  | trim }}
```

## Function Combination Examples

### Resource Name Generation

```yaml
{{- define "mychart.resourceName" -}}
{{- $name := include "mychart.fullname" . -}}
{{- $suffix := .suffix | default "" -}}
{{- if $suffix }}
{{- printf "%s-%s" $name $suffix | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
```

### Safe Value Extraction

```yaml
{{- $password := "" }}
{{- if and .Values.database (hasKey .Values.database "password") }}
{{- $password = .Values.database.password }}
{{- else }}
{{- $password = randAlphaNum 16 }}
{{- end }}
```

### Configuration Merging

```yaml
{{- $defaults := .Files.Get "config/defaults.yaml" | fromYaml }}
{{- $overrides := .Values.config | default (dict) }}
{{- $final := merge $overrides $defaults }}
config: |
  {{- $final | toYaml | nindent 2 }}
```

## Performance Tips

1. **Cache template results** - Use variables to avoid recalculating:
```yaml
{{- $fullname := include "mychart.fullname" . }}
name: {{ $fullname }}
matchLabels:
  app: {{ $fullname }}
```

2. **Minimize lookups** - `lookup` queries are expensive:
```yaml
{{- $secret := lookup "v1" "Secret" .Release.Namespace "my-secret" }}
{{- if $secret }}
  # Use $secret multiple times
{{- end }}
```

3. **Use with for scoping** - Reduces template complexity:
```yaml
{{- with .Values.ingress }}
  {{- if .enabled }}
    host: {{ .host }}
  {{- end }}
{{- end }}
```

## Debugging Functions

### printf

Formatted string output for debugging.

**Examples:**
```yaml
# Debug values
{{- printf "Debug: name=%s, replicas=%d" .Values.name .Values.replicas | fail }}
```

### toYaml for inspection

```yaml
# Inspect values
{{- toYaml .Values | fail }}
```

## Common Gotchas

1. **Nil vs Empty String**
```yaml
# This fails if value is nil
{{- if .Values.optional }}  # Error if nil!

# This works
{{- if .Values.optional | default "" }}  # Safe
```

2. **Type Conversion**
```yaml
# Port is integer in values but needs string comparison
{{- if eq (.Values.port | toString) "80" }}
```

3. **Pipeline Precedence**
```yaml
# Wrong - quote applies to "true", not the result
{{- if .Values.enabled | quote }}

# Right - use parentheses
{{- if (.Values.enabled | quote) }}
```

4. **Whitespace in Conditionals**
```yaml
# Creates extra whitespace
{{ if .Values.enabled }}
  value: true
{{ end }}

# Better - chomp whitespace
{{- if .Values.enabled }}
  value: true
{{- end }}
```
