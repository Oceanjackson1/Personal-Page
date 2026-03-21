---
title: "K8s Yaml Validator"
description: "Validate, lint, audit, or dry-run Kubernetes manifests (Deployment, Service, ConfigMap, CRD)."
category: "devops"
source: "community"
author: "Community"
tags: ["k8s", "yaml", "validator"]
date: 2026-03-20
---

# Kubernetes YAML Validator

## Overview

This skill provides a comprehensive validation workflow for Kubernetes YAML resources, combining syntax linting, schema validation, cluster dry-run testing, and intelligent CRD documentation lookup. Validate any Kubernetes manifest with confidence before applying it to the cluster.

**IMPORTANT: This is a REPORT-ONLY validation tool.** Do NOT modify files, do NOT use Edit tool, do NOT use AskUserQuestion to offer fixes. Generate a comprehensive validation report with suggested fixes shown as before/after code blocks, then let the user decide what to do next.

## Trigger Phrases

Use this skill when prompts look like:
- "Validate this Kubernetes YAML before deploy."
- "Lint these manifests and report what is broken."
- "Check this CRD manifest and explain schema issues."
- "Run dry-run checks on this manifest."
- "Find line-level errors in this multi-document YAML."

## When to Use This Skill

Invoke this skill when:
- Validating Kubernetes YAML files before applying to a cluster
- Debugging YAML syntax or formatting errors
- Working with Custom Resource Definitions (CRDs) and need documentation
- Performing dry-run tests to catch admission controller errors
- Ensuring YAML follows Kubernetes best practices
- Understanding what validation errors exist in manifests (report-only, user fixes manually)
- The user asks to "validate", "lint", "check", or "test" Kubernetes YAML files

## Read-Only Boundary (Mandatory)

This skill is strictly report-only:
- Do NOT modify any user files.
- Do NOT run Edit for fixes.
- Do NOT ask for permission to apply fixes.
- Do provide before/after snippets as suggestions in the report.

## Deterministic Path Setup

Run with explicit paths so commands are repeatable:

```bash
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
SKILL_DIR="$REPO_ROOT/devops-skills-plugin/skills/k8s-yaml-validator"
TARGET_FILE="$REPO_ROOT/<relative/path/to/file.yaml>"
```

Path checks:
- If `REPO_ROOT` is empty, stop and ask for repository root.
- If `SKILL_DIR` does not exist, stop and report path mismatch.
- If `TARGET_FILE` does not exist, stop and ask for the correct file.

## Validation Workflow

Follow this sequential validation workflow. Each stage catches different types of issues:

### Stage 0: Pre-Validation Setup (Deterministic Resource Count)

Before running validators, count documents using the bundled script:

```bash
python3 "$SKILL_DIR/scripts/count_yaml_documents.py" "$TARGET_FILE"
```

Expected output (example):
```json
{
  "file": ".../manifests.yaml",
  "documents": 3,
  "separators": 2
}
```

Gate rules:
- If `documents >= 3`, load `references/validation_workflow.md` before Stage 1.
- Always include the document count in the final report summary.
- If `python3` is unavailable, use fallback:
```bash
awk 'BEGIN{d=0;seen=0} /^[[:space:]]*---[[:space:]]*$/ {if(seen){d++;seen=0}; next} /^[[:space:]]*#/ {next} NF{seen=1} END{if(seen)d++; print d}' "$TARGET_FILE"
```
and mark the count as `estimated` in the report.

### Stage 1: Tool Check

Before starting validation, verify required tools are installed:

```bash
bash "$SKILL_DIR/scripts/setup_tools.sh"
```

Required tools:
- **yamllint**: YAML syntax and style linting
- **kubeconform**: Kubernetes schema validation with CRD support
- **kubectl**: Cluster dry-run testing (optional but recommended)

If tools are missing, display installation guidance from script output and continue with available tools. Document missing tools and skipped stages in the report.

### Stage 2: YAML Syntax Validation

Validate YAML syntax and formatting using yamllint:

```bash
yamllint -c "$SKILL_DIR/assets/.yamllint" "$TARGET_FILE"
```

**Common issues caught:**
- Indentation errors (tabs vs spaces)
- Trailing whitespace
- Line length violations
- Syntax errors
- Duplicate keys

**Reporting approach:**
- Report all syntax issues with file:line references
- For fixable issues, show suggested before/after code blocks
- Continue to next validation stage to collect all issues before reporting

### Stage 3: CRD Detection and Documentation Lookup

Before schema validation, detect if the YAML contains Custom Resource Definitions:

```bash
bash "$SKILL_DIR/scripts/detect_crd_wrapper.sh" "$TARGET_FILE"
```

The wrapper script automatically handles Python dependencies by creating a temporary virtual environment if PyYAML is not available.

**Resilient Parsing:** The script is resilient to syntax errors in individual documents. If a multi-document YAML file has some valid and some invalid documents, the script will:
- Parse valid documents and detect their CRDs
- Report errors for invalid documents but continue processing
- This matches kubeconform's behavior of validating 2/3 resources even when 1/3 has syntax errors

The script outputs JSON with resource information and parse status:
```json
{
  "resources": [
    {
      "kind": "Certificate",
      "apiVersion": "cert-manager.io/v1",
      "group": "cert-manager.io",
      "version": "v1",
      "isCRD": true,
      "name": "example-cert"
    }
  ],
  "parseErrors": [
    {
      "document": 1,
      "start_line": 2,
      "error_line": 6,
      "error": "mapping values are not allowed in this context"
    }
  ],
  "summary": {
    "totalDocuments": 3,
    "parsedSuccessfully": 2,
    "parseErrors": 1,
    "crdsDetected": 1
  }
}
```

**For each detected CRD:**

1. **Try Context7 MCP first (preferred):**
   - Resolve library:
     - Tool: `mcp__context7__resolve-library-id`
     - `libraryName`: CRD project name (example: `cert-manager` for `cert-manager.io`)
   - Query docs:
     - Tool: `mcp__context7__query-docs`
     - `libraryId`: resolved library ID from previous step
     - `query`: include CRD kind, group, and version (example: `Certificate cert-manager.io v1 required fields in spec`)

2. **Fallback to `web.search_query` if Context7 fails or returns insufficient details:**
   ```
   Search query pattern:
   "<kind>" "<group>" kubernetes CRD "<version>" documentation spec

   Example:
   "Certificate" "cert-manager.io" kubernetes CRD "v1" documentation spec
   ```

3. **Extract key information:**
   - Required fields in `spec`
   - Field types and validation rules
   - Examples from documentation
   - Version-specific changes or deprecations

**Secondary CRD Detection via kubeconform:** If `detect_crd_wrapper.sh` cannot identify CRDs (for example, syntax errors in all documents), but kubeconform still validates a CRD resource, look up docs for that CRD anyway. Parse kubeconform output to identify validated CRDs and perform Context7/`web.search_query` lookups.

**Why this matters:** CRDs have custom schemas not available in standard Kubernetes validation tools. Understanding the CRD's spec requirements prevents validation errors and ensures correct resource configuration.

### Stage 4: Schema Validation

Validate against Kubernetes schemas using kubeconform:

```bash
kubeconform \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  -strict \
  -ignore-missing-schemas \
  -summary \
  -verbose \
  "$TARGET_FILE"
```

**Options explained:**
- `-strict`: Reject unknown fields (recommended for production - catches typos)
- `-ignore-missing-schemas`: Skip validation for CRDs without available schemas
- `-kubernetes-version 1.30.0`: Validate against specific K8s version

**Common issues caught:**
- Invalid apiVersion or kind
- Missing required fields
- Wrong field types
- Invalid enum values
- Unknown fields (with -strict)

**For CRDs:** If kubeconform reports "no schema found", this is expected. Use the documentation from Stage 3 to manually validate the spec fields.

**kubeconform line number behavior — two distinct cases:**

kubeconform does NOT report file-absolute line numbers. You must translate:

1. **Parse errors** (e.g. `error converting YAML to JSON: yaml: line N`):
   - `N` is **document-relative** (line N within that document's content).
   - Convert to file-absolute: `file_line = doc_start_line + N - 1`
   - `doc_start_line` comes from the `start_line` field in `detect_crd_wrapper.sh` output.
   - Example: document starts at file line 4, kubeconform says `yaml: line 5` →
     file-absolute line = 4 + 5 − 1 = **line 8** (matches yamllint output).

2. **Schema validation errors** (e.g. `got string, want integer`):
   - kubeconform reports **JSON path only**, no line number.
   - Example: `at '/spec/template/spec/containers/0/ports/0/containerPort': got string, want integer`
   - To find the line: search the YAML file for the field name (e.g. `containerPort`) within
     the relevant document section, using file-absolute line numbers from the surrounding context.

Always present line numbers as file-absolute in the validation report even when translating
from kubeconform's document-relative output.

### Stage 5: Cluster Dry-Run (if available)

**IMPORTANT: Always try server-side dry-run first.** Server-side validation catches more issues than client-side because it runs through admission controllers and webhooks.

**Decision Tree:**

```
1. Try server-side dry-run first:
   kubectl apply --dry-run=server -f "$TARGET_FILE"

   └─ If SUCCESS → Use results, continue to Stage 6

   └─ If FAILS with connection error (e.g., "connection refused",
      "unable to connect", "no configuration"):
      │
      ├─ 2. Attempt client-side dry-run (parse-only fallback):
      │     kubectl apply --dry-run=client --validate=false -f "$TARGET_FILE"
      │
      │     ├─ If SUCCESS:
      │     │    Document in report: "Server-side validation skipped (no cluster access); client fallback ran in parse-only mode"
      │     │
      │     └─ If FAILS with discovery/openapi error (e.g., "unable to recognize",
      │        "failed to download openapi", "couldn't get current server API group list"):
      │        Document in report: "Dry-run skipped (cluster discovery unavailable)"
      │        Continue to Stage 6
      │
      └─ If FAILS with validation error (e.g., "admission webhook denied",
         "resource quota exceeded", "invalid value"):
         └─ Record the error, continue to Stage 6

   └─ If FAILS with parse error (e.g., "error converting YAML to JSON",
      "yaml: line X: mapping values are not allowed"):
      └─ Record the error, skip client-side dry-run (same error will occur)
         Document in report: "Dry-run blocked by YAML syntax errors - fix syntax first"
         Continue to Stage 6
```

**Note:** Parse errors from earlier stages (yamllint, kubeconform) will also cause dry-run to fail. Do NOT attempt client-side dry-run as a fallback for parse errors - it will produce the same error. Parse errors must be fixed before dry-run validation can proceed.

**Server-side dry-run catches:**
- Admission controller rejections
- Policy violations (PSP, OPA, Kyverno, etc.)
- Resource quota violations
- Missing namespaces
- Invalid ConfigMap/Secret references
- Webhook validations

**Client-side dry-run with `--validate=false` catches (fallback, when command succeeds):**
- YAML/JSON conversion and request-construction issues
- Whether `kubectl` can process and submit the manifest shape in client mode
- **Note:** `--validate=false` disables schema/type/required-field validation and still does NOT catch admission controller or policy issues.

**Document in your report which mode was used:**
- If server-side: "Full cluster validation performed"
- If client-side with `--validate=false`: "Limited parse-only validation (no cluster access) - schema and admission policies not checked"
- If skipped: "Dry-run skipped - kubectl not available"
- If skipped after client fallback attempt: "Dry-run skipped (cluster discovery unavailable)"

**For updates to existing resources:**
```bash
kubectl diff -f "$TARGET_FILE"
```
This shows what would change, helping catch unintended modifications.

### Stage 6: Generate Detailed Validation Report (REPORT ONLY)

After completing all validation stages, generate a comprehensive report. **This is a REPORT-ONLY stage.**

**NEVER do any of the following:**
- Do NOT use the Edit tool to modify files
- Do NOT use AskUserQuestion to offer to fix issues
- Do NOT prompt the user asking if they want fixes applied
- Do NOT modify any YAML files

**ALWAYS do the following:**
- Generate a comprehensive validation report
- Show before/after code blocks as SUGGESTIONS only
- Let the user decide what to do after reviewing the report
- End with "Next Steps" for the user to take manually

1. **Summarize all issues found** across all stages in a table format:

   ```
   | Severity | Stage | Location | Issue | Suggested Fix |
   |----------|-------|----------|-------|---------------|
   | Error | Syntax | file.yaml:5 | Indentation error | Use 2 spaces |
   | Error | Schema | file.yaml:21 | Wrong type | Change to integer |
   | Warning | Best Practice | file.yaml:30 | Missing labels | Add app label |
   ```

2. **Categorize by severity:**
   - **Errors** (must fix): Syntax errors, missing required fields, dry-run failures
   - **Warnings** (should fix): Style issues, best practice violations
   - **Info** (optional): Suggestions for improvement

3. **Show before/after code blocks for each issue:**

   For every issue, display explicit before/after YAML snippets showing the suggested fix:

   ```
   **Issue 1: deployment.yaml:21 - Wrong field type (Error)**

   Current:
   ```yaml
           - containerPort: "80"
   ```

   Suggested Fix:
   ```yaml
           - containerPort: 80
   ```

   **Why:** containerPort must be an integer, not a string. Kubernetes will reject string values.
   Reference: See k8s_best_practices.md "Invalid Values" section.
   ```

4. **Provide validation summary:**

   ```
   ## Validation Report Summary

   File: deployment.yaml
   Resources Analyzed: 3 (Deployment, Service, Certificate)

   | Stage | Status | Issues Found |
   |-------|--------|--------------|
   | YAML Syntax | ❌ Failed | 2 errors |
   | CRD Detection | ✅ Passed | 1 CRD detected (Certificate) |
   | Schema Validation | ❌ Failed | 1 error |
   | Dry-Run | ❌ Failed | 1 error |

   Total Issues: 4 errors, 2 warnings

   ## Detailed Findings

   [List each issue with before/after code blocks as shown above]

   ## Next Steps

   1. Fix the 4 errors listed above (deployment will fail without these)
   2. Consider addressing the 2 warnings for best practices
   3. Re-run validation after fixes to confirm resolution
   ```

5. **Do NOT modify files** - this is a reporting tool only
   - Present all findings clearly
   - Let the user decide which fixes to apply
   - User can request fixes after reviewing the report

## Objective Stage Gates (Repeatable)

Use this table to keep stage decisions deterministic:

| Stage | Required | Command | Pass/Fail Criteria | Fallback |
|------|----------|---------|--------------------|----------|
| 0 Resource Count | Yes | `python3 "$SKILL_DIR/scripts/count_yaml_documents.py" "$TARGET_FILE"` | Pass when count output is produced and `documents` is recorded. | Use AWK estimator and mark `estimated`. |
| 1 Tool Check | Yes | `bash "$SKILL_DIR/scripts/setup_tools.sh"` | Pass when command runs and tool availability is known. | Continue with available tools and log skips. |
| 2 YAML Syntax | If `yamllint` available | `yamllint -c "$SKILL_DIR/assets/.yamllint" "$TARGET_FILE"` | Pass on exit code `0`; fail on lint errors. | Skip with explicit reason if missing binary. |
| 3 CRD Detection | If `python3` available | `bash "$SKILL_DIR/scripts/detect_crd_wrapper.sh" "$TARGET_FILE"` | Pass when JSON output includes `summary`. | Skip CRD extraction and rely on kubeconform clues. |
| 4 Schema | If `kubeconform` available | kubeconform command from Stage 4 | Pass when kubeconform reports valid resources. | Skip and record as coverage gap if missing binary. |
| 5 Dry-Run | If `kubectl` available | `kubectl apply --dry-run=server -f "$TARGET_FILE"` | Pass on successful server dry-run. | Attempt parse-only client fallback with `--dry-run=client --validate=false`; if discovery still fails, mark stage skipped. |
| 6 Report | Yes | Report generation | Pass when summary + per-issue snippets + next steps are provided. | No fallback; this stage is mandatory. |

## Fallback Matrix

| Constraint | Action | Report Language |
|-----------|--------|-----------------|
| `python3` unavailable | Skip `count_yaml_documents.py` and CRD parser scripts. Use AWK count only. | `Python runtime unavailable; CRD parser skipped, resource count is estimated.` |
| `yamllint` unavailable | Skip Stage 2; continue with schema/dry-run stages if available. | `YAML lint skipped because yamllint is not installed.` |
| `kubeconform` unavailable | Skip Stage 4; run lint and dry-run only. | `Schema validation skipped because kubeconform is not installed.` |
| `kubectl` unavailable | Skip Stage 5 entirely. | `Dry-run skipped because kubectl is not installed.` |
| No cluster connectivity | Run server-side first, then attempt parse-only client fallback with `--dry-run=client --validate=false`; if it still fails, skip dry-run and continue. | `Server-side dry-run unavailable due cluster access; parse-only client-side dry-run attempted (schema checks disabled).` |
| Client dry-run still requires discovery | Treat dry-run as unavailable and rely on lint + schema stages. | `Dry-run skipped (cluster discovery unavailable); lint and schema results used.` |
| External docs unavailable | Continue local validation and state documentation gap. | `CRD documentation lookup deferred due tooling/network limitation.` |

## Best Practices Reference

For detailed Kubernetes YAML best practices, load the reference:
```
Read "$SKILL_DIR/references/k8s_best_practices.md"
```

This reference includes:
- Metadata and label conventions
- Resource limits and requests
- Security context guidelines
- Probe configurations
- Common validation issues and fixes

**When to load (ALWAYS load in these cases):**
- Schema validation fails with type errors (e.g., string vs integer, invalid values)
- Schema validation reports missing required fields
- kubeconform reports invalid field values or unknown fields
- Dry-run fails with validation errors related to resources, probes, or security
- When explaining why a fix is needed (to provide context from best practices)

## Detailed Validation Workflow Reference

For in-depth workflow details and error handling strategies, load the reference:
```
Read "$SKILL_DIR/references/validation_workflow.md"
```

This reference includes:
- Detailed command options for each tool
- Error handling strategies
- Multi-resource file handling
- Complete workflow diagram
- Troubleshooting guide

**When to load (ALWAYS load in these cases):**
- File contains 3 or more resources (multi-document YAML)
- Validation produces errors you haven't seen before or can't immediately diagnose
- Need to understand the complete workflow for debugging
- Errors span multiple validation stages

## Working with Multiple Resources

When a YAML file contains multiple resources (separated by `---`):

1. **Validate the entire file first** with yamllint and kubeconform
2. **If errors occur, identify which resource** has issues by checking line numbers
3. **For dry-run**, the file is tested as a unit (Kubernetes processes in order)
4. **Track issues per-resource** when presenting findings to the user

### Partial Parsing Behavior

When a multi-document YAML file has some valid and some invalid documents:

**Expected behavior:**
- The CRD detection script (`detect_crd.py`) will parse valid documents and skip invalid ones
- kubeconform will validate resources it can parse and report errors for unparseable ones
- The validation report should clearly show which documents parsed and which failed

**Example scenario:**
A file with 3 documents where document 1 has a syntax error:
- Document 1 (Deployment): Syntax error at line 8
- Document 2 (Service): Valid
- Document 3 (Certificate CRD): Valid

**Expected output:**
- CRD detection: Finds Certificate CRD from document 3
- kubeconform: Reports error for document 1, validates documents 2 and 3
- Report: Shows syntax error for document 1, validation results for documents 2 and 3

**In your report:**
```
| Document | Resource | Parsing | Validation |
|----------|----------|---------|------------|
| 1 | Deployment | ❌ Syntax error (line 8) | Skipped |
| 2 | Service | ✅ Parsed | ✅ Valid |
| 3 | Certificate | ✅ Parsed | ✅ Valid |
```

**Line Number Reference Style:**
- **Always use file-absolute line numbers** (line numbers relative to the start of the entire file)
- This matches what yamllint, kubeconform, and kubectl report
- Example: If a file has 3 documents and the error is in document 2 which starts at line 35, report as "line 42" (the absolute line in the file), not "line 7" (relative to document start)
- This consistency makes it easy for users to navigate directly to the error in their editor

This ensures users get maximum validation feedback even when some documents have issues.

## Error Handling Strategies

### Tool Not Available
- Run `bash "$SKILL_DIR/scripts/setup_tools.sh"` to check availability
- Provide installation instructions
- Skip optional stages but document what was skipped
- Continue with available tools

### Cluster Access Issues
- Attempt parse-only client-side dry-run with `--dry-run=client --validate=false`
- Treat this fallback as transport/parsing signal only (`--validate=false` disables schema/type/required-field checks)
- If client dry-run still fails with API discovery/openapi errors, skip dry-run and rely on lint/schema stages
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
- Prioritize fixing earlier stage errors first

## Communication Guidelines

When presenting validation results:

1. **Be clear and concise** about what was found
2. **Explain why issues matter** (e.g., "This will cause pod creation to fail")
3. **Provide context** from best practices when relevant
4. **Group related issues** (e.g., all missing label issues together)
5. **Use file:line references** for all issues
6. **Show fix complexity** - Include a complexity indicator in the issue header:
   - **[Simple]**: Single-line fixes like indentation, typos, or value changes
   - **[Medium]**: Multi-line changes or adding missing fields/sections
   - **[Complex]**: Logic changes, restructuring, or changes affecting multiple resources

   Example format in issue header:
   ```
   **Issue 1: deployment.yaml:8 - Wrong indentation (Error) [Simple]**
   **Issue 2: deployment.yaml:15-25 - Missing security context (Warning) [Medium]**
   **Issue 3: deployment.yaml - Selector mismatch with Service (Error) [Complex]**
   ```
7. **Always provide a comprehensive report** including:
   - Summary table of all issues by stage
   - Before/after code blocks for each issue
   - Total count of errors and warnings
   - Clear next steps for the user
8. **NEVER offer to apply fixes** - this is strictly a reporting tool
   - Do not ask "Would you like me to fix this?"
   - Do not use AskUserQuestion for fix confirmations
   - Present the report and let the user take action

## Performance Optimization

### Parallel Tool Execution

For improved validation speed, some stages can be executed in parallel:

**Can run in parallel (no dependencies):**
- `yamllint` (Stage 2) and `detect_crd_wrapper.sh` (Stage 3) can run simultaneously
- Both tools operate independently on the input file
- Results from both are needed before proceeding to schema validation

**Example parallel execution:**
```
# Run these in parallel (using & and wait, or parallel tool calls):
yamllint -c "$SKILL_DIR/assets/.yamllint" "$TARGET_FILE"
bash "$SKILL_DIR/scripts/detect_crd_wrapper.sh" "$TARGET_FILE"
```

**Must run sequentially:**
- Stage 0 (Resource Count Check) → Before all other stages
- Stage 1 (Tool Check) → Before using any tools
- Stage 4 (Schema Validation) → After CRD detection (needs CRD info for context)
- Stage 5 (Dry-Run) → After schema validation
- Stage 6 (Report) → After all validation stages complete

**When to parallelize:**
- Files with more than 5 resources benefit most from parallel execution
- For small files (1-2 resources), sequential execution is fine

## Version Awareness

Always consider Kubernetes version compatibility:
- Check for deprecated APIs (e.g., `extensions/v1beta1` → `apps/v1`)
- For CRDs, ensure the apiVersion matches what's in the cluster
- Use `kubectl api-versions` to list available API versions in the cluster
- Reference version-specific documentation when available

## Test Coverage Guidance

The `test/` directory contains example files to exercise all validation paths. Use these to verify skill behavior.

### Test Files

| Test File | Purpose | Expected Behavior |
|-----------|---------|-------------------|
| `deployment-test.yaml` | Valid standard K8s resource | All stages pass, no errors |
| `certificate-crd-test.yaml` | Valid CRD resource | CRD detected, Context7 lookup performed, no errors |
| `comprehensive-test.yaml` | Multi-resource with intentional YAML syntax error | Syntax error detected, partial parsing works, CRD found |
| `schema-errors-test.yaml` | Valid YAML with intentional schema type errors | yamllint passes; kubeconform fails with 2 JSON-path errors (replicas, containerPort) |

### Validation Paths to Test

1. **Happy Path (All Valid)**
   - File: `deployment-test.yaml`
   - Expected: All stages pass, report shows "0 errors, 0 warnings"
   - Commands:
```bash
cd "$SKILL_DIR"
python3 scripts/count_yaml_documents.py test/deployment-test.yaml
yamllint -c assets/.yamllint test/deployment-test.yaml
bash scripts/detect_crd_wrapper.sh test/deployment-test.yaml
kubeconform \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  -strict -ignore-missing-schemas -summary -verbose \
  test/deployment-test.yaml
kubectl apply --dry-run=server -f test/deployment-test.yaml
```

2. **CRD Detection Path**
   - File: `certificate-crd-test.yaml`
   - Expected: CRD detected, `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` used
   - Commands:
```bash
cd "$SKILL_DIR"
python3 scripts/count_yaml_documents.py test/certificate-crd-test.yaml
bash scripts/detect_crd_wrapper.sh test/certificate-crd-test.yaml
kubeconform \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  -strict -ignore-missing-schemas -summary -verbose \
  test/certificate-crd-test.yaml
```

3. **Syntax Error Path**
   - File: `comprehensive-test.yaml`
   - Expected: yamllint catches error, kubeconform reports partial validation, dry-run blocked
   - Commands:
```bash
cd "$SKILL_DIR"
python3 scripts/count_yaml_documents.py test/comprehensive-test.yaml
yamllint -c assets/.yamllint test/comprehensive-test.yaml
bash scripts/detect_crd_wrapper.sh test/comprehensive-test.yaml
kubeconform \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  -strict -ignore-missing-schemas -summary -verbose \
  test/comprehensive-test.yaml
kubectl apply --dry-run=server -f test/comprehensive-test.yaml
```

4. **Multi-Resource Partial Parsing**
   - File: `comprehensive-test.yaml` (has 3 resources, 1 with syntax error)
   - Expected: 2/3 resources validated, parse error reported for document 1
   - Commands:
```bash
cd "$SKILL_DIR"
python3 scripts/count_yaml_documents.py test/comprehensive-test.yaml
bash scripts/detect_crd_wrapper.sh test/comprehensive-test.yaml
```

5. **Schema Validation Error Path (type mismatches)**
   - File: `schema-errors-test.yaml`
   - Expected: yamllint passes (valid YAML), kubeconform fails with 2 JSON-path schema errors
   - Note: kubeconform reports JSON paths, not line numbers — locate fields manually in the YAML
   - Commands:
```bash
cd "$SKILL_DIR"
python3 scripts/count_yaml_documents.py test/schema-errors-test.yaml
yamllint -c assets/.yamllint test/schema-errors-test.yaml
bash scripts/detect_crd_wrapper.sh test/schema-errors-test.yaml
kubeconform \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  -strict -ignore-missing-schemas -summary -verbose \
  test/schema-errors-test.yaml
```

6. **No Cluster Access Path**
   - Any valid file with no kubectl cluster configured
   - Expected: Server-side dry-run fails; parse-only client-side fallback is attempted (no schema guarantees) and may still fail if API discovery is unavailable
   - Commands:
```bash
cd "$SKILL_DIR"
KUBECONFIG=/tmp/nonexistent-kubeconfig kubectl apply --dry-run=server -f test/deployment-test.yaml
KUBECONFIG=/tmp/nonexistent-kubeconfig kubectl apply --dry-run=client --validate=false -f test/deployment-test.yaml
```

7. **Missing Tools Path**
   - Test by temporarily removing a tool from PATH
   - Expected: setup_tools.sh reports missing tools and prints install instructions, validation continues with available tools
   - Commands:
```bash
cd "$SKILL_DIR"
PATH="/usr/bin:/bin" bash scripts/setup_tools.sh
```

### Creating New Test Files

When adding test files:
1. Name files descriptively: `<scenario>-test.yaml`
2. Document expected behavior in comments at top of file
3. Include intentional errors for error-path tests
4. Test both standard K8s resources and CRDs

### Expected Report Structure

For any validation, the report should include:
- [ ] Summary table with issue counts by severity
- [ ] Stage-by-stage status table (passed/failed/skipped)
- [ ] Document parsing table (for multi-resource files)
- [ ] Before/after code blocks for each issue
- [ ] Fix complexity indicators ([Simple], [Medium], [Complex])
- [ ] File-absolute line numbers
- [ ] "Next Steps" section

## Done Criteria

Validation is complete only when all conditions are true:
- Stage gates were evaluated in order and every skipped stage includes a reason.
- Resource count came from `count_yaml_documents.py` (or documented AWK fallback).
- CRD lookups used `mcp__context7__resolve-library-id` + `mcp__context7__query-docs`, with `web.search_query` fallback only when needed.
- Report-only boundary was preserved (no edits, no fix-application prompts).
- Output includes exact commands run, findings by severity, and manual next steps.

## Resources

### scripts/

**detect_crd_wrapper.sh**
- Wrapper script that handles Python dependency management
- Automatically creates temporary venv if PyYAML is not available
- Calls detect_crd.py to parse YAML files
- Usage: `bash "$SKILL_DIR/scripts/detect_crd_wrapper.sh" "$TARGET_FILE"`

**detect_crd.py**
- Parses YAML files to identify Custom Resource Definitions
- Extracts kind, apiVersion, group, and version information
- Outputs JSON for programmatic processing
- Requires PyYAML (handled automatically by wrapper script)
- Can be called directly: `python3 "$SKILL_DIR/scripts/detect_crd.py" "$TARGET_FILE"`

**count_yaml_documents.py**
- Deterministically counts non-empty YAML documents in a multi-doc file
- Returns JSON with document count and separators
- Use before Stage 1 to decide whether to load deep workflow reference
- Usage: `python3 "$SKILL_DIR/scripts/count_yaml_documents.py" "$TARGET_FILE"`

**setup_tools.sh**
- Checks for required validation tools
- Provides installation instructions for missing tools
- Verifies versions of installed tools
- Usage: `bash "$SKILL_DIR/scripts/setup_tools.sh"`

### references/

**k8s_best_practices.md**
- Comprehensive guide to Kubernetes YAML best practices
- Covers metadata, labels, resource limits, security context
- Common validation issues and how to fix them
- Load when providing context for validation errors

**validation_workflow.md**
- Detailed validation workflow with all stages
- Command options and configurations
- Error handling strategies
- Complete workflow diagram
- Load for complex validation scenarios

### assets/

**.yamllint**
- Pre-configured yamllint rules for Kubernetes YAML
- Follows Kubernetes conventions (2-space indentation, line length, etc.)
- Can be customized per project
- Usage: `yamllint -c "$SKILL_DIR/assets/.yamllint" "$TARGET_FILE"`

---

## Reference: K8S_Best_Practices

# Kubernetes YAML Best Practices

## General YAML Best Practices

### Formatting and Style
- Use 2 spaces for indentation (not tabs)
- Keep lines under 80 characters when possible
- Use lowercase for keys
- Quote string values containing special characters
- Always specify apiVersion and kind
- Include metadata.name for all resources

### Resource Organization
- One resource per file for clarity (unless logically grouped)
- Use `---` to separate multiple resources in a single file
- Name files descriptively: `<resource-type>-<name>.yaml`

## Kubernetes-Specific Best Practices

### Metadata
```yaml
metadata:
  name: my-app
  namespace: production
  labels:
    app: my-app
    version: v1.0.0
    component: backend
    managed-by: kubectl
  annotations:
    description: "Backend service for my-app"
```

### Labels and Selectors
- Always include `app` label
- Use consistent label keys across resources
- Include version labels for rollout tracking
- Selectors must match pod labels exactly

### Resource Limits and Requests
Always specify both requests and limits:
```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "250m"
  limits:
    memory: "128Mi"
    cpu: "500m"
```

### Probes
Always define liveness and readiness probes:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Security
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
```

### Image Management
```yaml
image: registry.example.com/my-app:v1.2.3  # Always use specific tags
imagePullPolicy: IfNotPresent  # Or Always for :latest
```

## Common Validation Issues

### Missing Required Fields
- `apiVersion` and `kind` are always required
- `metadata.name` is required for all resources
- `spec.selector` must be specified for Deployments/Services
- `spec.template.spec.containers` must have at least one container

### Selector Mismatches
Deployment selector must match pod template labels:
```yaml
# Deployment
spec:
  selector:
    matchLabels:
      app: my-app  # Must match pod labels below
  template:
    metadata:
      labels:
        app: my-app  # Must match selector above
```

### Invalid Values
- CPU: Use millicore notation (e.g., "500m") or fractional (e.g., "0.5")
- Memory: Use Mi, Gi notation (e.g., "512Mi")
- Port numbers: Must be 1-65535
- DNS names: Must be lowercase alphanumeric with hyphens

### Namespace Issues
- Not all resources are namespaced (e.g., ClusterRole, PersistentVolume)
- Services must be in the same namespace as the pods they target
- Default namespace is "default" if not specified

## CRD-Specific Considerations

### API Version Compatibility
- Check the CRD version installed in the cluster
- Use the correct apiVersion for the CRD
- Be aware of deprecations (e.g., v1alpha1 → v1beta1 → v1)

### Required Fields
- CRDs often have custom required fields in spec
- Check the CRD documentation for field requirements
- Use kubectl explain <kind> to see field documentation

### Validation
- CRDs may have custom validation rules
- OpenAPI schema validation is stricter in newer K8s versions
- Use dry-run to catch validation errors before applying

## Deprecation Warnings

### Common Deprecated APIs
- `extensions/v1beta1` → `apps/v1` (Deployments, DaemonSets)
- `networking.k8s.io/v1beta1` → `networking.k8s.io/v1` (Ingress)
- `policy/v1beta1` → `policy/v1` (PodDisruptionBudget)

Always use the latest stable API version.

---

## Reference: Validation_Workflow

# Kubernetes YAML Validation Workflow

This document outlines the comprehensive validation workflow for Kubernetes YAML resources.

## Validation Stages

### Stage 0: Resource Count (Deterministic)

**Purpose:** Count non-empty YAML documents before running validators.

**Command:**
```bash
python3 scripts/count_yaml_documents.py <file.yaml>
```

**Fallback when Python is unavailable (estimated count):**
```bash
awk 'BEGIN{d=0;seen=0} /^[[:space:]]*---[[:space:]]*$/ {if(seen){d++;seen=0}; next} /^[[:space:]]*#/ {next} NF{seen=1} END{if(seen)d++; print d}' <file.yaml>
```

### Stage 1: Tool Check

**Purpose:** Determine which validation stages are runnable in the current environment.

**Command:**
```bash
bash scripts/setup_tools.sh
```

If required tools are missing, continue with available tools and report skipped stages.

### Stage 2: YAML Syntax Validation (yamllint)

**Purpose:** Catch YAML syntax errors and style issues before Kubernetes-specific validation.

**Command:**
```bash
yamllint -c assets/.yamllint <file.yaml>
```

**Common Issues Detected:**
- Indentation errors (tabs vs spaces)
- Line length violations
- Trailing spaces
- Missing document start markers
- Duplicate keys
- Syntax errors

Stage 3 (CRD detection and docs lookup) is covered in the dedicated section below.

### Stage 4: Kubernetes Schema Validation (kubeconform)

**Purpose:** Validate against Kubernetes schemas and detect structural issues.

**Basic Command:**
```bash
kubeconform -summary <file.yaml>
```

**With CRD Support (recommended):**
```bash
kubeconform \
  -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  -strict \
  -ignore-missing-schemas \
  -summary \
  -verbose \
  <file.yaml>
```

**Options:**
- `-strict`: Reject resources with unknown fields (catches typos - recommended for production)
- `-ignore-missing-schemas`: Skip validation for CRDs without available schemas
- `-kubernetes-version <version>`: Validate against specific K8s version (e.g., 1.30.0)
- `-output json`: Output results as JSON

**Common Issues Detected:**
- Invalid apiVersion
- Missing required fields
- Invalid field types
- Unknown fields (in strict mode)
- Invalid enum values

### Stage 5: Cluster Dry-Run (kubectl)

**Purpose:** Validate against the actual cluster configuration, admission controllers, and policies.

**Client-Side Dry Run:**
```bash
kubectl apply --dry-run=client --validate=false -f <file.yaml>
```
- Best-effort fallback when server-side dry-run is unavailable
- May still fail if API discovery is unavailable (for example, no reachable cluster)
- Does not catch admission controller or policy issues

**Server-Side Dry Run:**
```bash
kubectl apply --dry-run=server -f <file.yaml>
```
- Full validation including admission controllers
- Validates against cluster-specific constraints
- Requires cluster access
- Catches issues like:
  - Resource quota violations
  - Policy violations (PSP, OPA, Kyverno)
  - Admission webhook rejections
  - Namespace existence
  - ConfigMap/Secret references

**Diff Mode (for updates):**
```bash
kubectl diff -f <file.yaml>
```
Shows what would change if applied to the cluster.

## CRD Detection and Documentation Lookup (Stage 3)

### Step 1: Detect CRDs

Use the wrapper script (handles missing PyYAML automatically):
```bash
bash scripts/detect_crd_wrapper.sh <file.yaml>
```

Output example:
```json
{
  "resources": [
    {
      "kind": "Certificate",
      "apiVersion": "cert-manager.io/v1",
      "group": "cert-manager.io",
      "version": "v1",
      "isCRD": true,
      "name": "example-cert"
    }
  ],
  "parseErrors": [],
  "summary": {
    "totalDocuments": 1,
    "parsedSuccessfully": 1,
    "parseErrors": 0,
    "crdsDetected": 1
  }
}
```

### Step 2: Lookup CRD Documentation

For each detected CRD:

1. **Use context7 MCP (preferred):**
   - Resolve library ID: `mcp__context7__resolve-library-id` with the CRD group/project name
   - Fetch documentation: `mcp__context7__query-docs` with the library ID
   - Focus on the specific version if available

2. **Fallback to Web Search:**
   - Search query: `"<kind>" "<group>" kubernetes CRD "<version>" documentation`
   - Example: `"Certificate" "cert-manager.io" kubernetes CRD "v1" documentation`
   - Look for official documentation sites
   - Check for API references and examples

### Step 3: Validate Against CRD Schema

Once documentation is found:
- Check required fields in spec
- Verify field types and formats
- Validate enum values
- Check for version-specific changes

## Complete Validation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 0. Count Documents                                          │
│    Run: python3 scripts/count_yaml_documents.py <file.yaml> │
│    Record: documents + separators                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. Check Tools                                              │
│    Run: bash scripts/setup_tools.sh                         │
│    Continue with available tools                            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. YAML Syntax Check                                        │
│    Run: yamllint -c assets/.yamllint <file.yaml>            │
│    Fix: Indentation, trailing spaces, syntax errors         │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Detect CRDs                                              │
│    Run: bash scripts/detect_crd_wrapper.sh <file.yaml>      │
│    Parse: Extract kind, apiVersion, group                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
                    ┌──────┴──────┐
                    │             │
                [CRD?]          [Standard Resource]
                    │             │
                    ↓             ↓
     ┌──────────────────────┐    │
     │ 4a. Lookup CRD Docs   │    │
     │    - context7 MCP     │    │
     │    - Web search       │    │
     │    - Version-aware    │    │
     └──────────────────────┘    │
                    │             │
                    └──────┬──────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Schema Validation                                        │
│    Run: kubeconform -summary <file.yaml>                    │
│    Fix: Required fields, types, unknown fields              │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Dry-Run (if cluster available)                           │
│    Run: kubectl apply --dry-run=server -f <file.yaml>       │
│    Fix: Admission issues, quotas, policies                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Generate Validation Report                               │
│    - Summarize all issues in table format                   │
│    - Show before/after code blocks for each issue           │
│    - Do NOT modify files - report only                      │
└─────────────────────────────────────────────────────────────┘
```

## Error Handling

### Tool Not Found
- Run `scripts/setup_tools.sh` to check tool availability
- Provide installation instructions
- Skip optional validation stages if tools missing

### Cluster Not Available
- Skip server-side dry-run
- Attempt client-side dry-run with `--dry-run=client --validate=false`
- If client-side still fails due discovery/openapi errors, skip dry-run and rely on kubeconform
- Warn user that dry-run coverage is limited or unavailable

### CRD Documentation Not Found
- Document that CRD docs couldn't be found
- Attempt validation with kubeconform CRD schemas
- Suggest checking cluster for CRD definition:
  ```bash
  kubectl get crd <crd-name> -o yaml
  ```

### Multiple Resources in One File
- Validate each resource separately
- Track which resource has issues
- Provide line numbers for error locations

## Best Practices for Validation

1. **Always validate in order:** count → tool check → syntax → CRD detection → schema → dry-run
2. **Collect all issues:** Don't stop at first error - gather everything before reporting
3. **For CRDs:** Always look up documentation first
4. **Version awareness:** Check K8s version compatibility
5. **Test with cluster:** Server-side dry-run is the most reliable
6. **Show before/after:** Display code blocks showing suggested fixes
7. **Provide context:** Explain what each issue means and why the fix is needed
8. **Report only:** Do NOT modify files - let user decide which fixes to apply
9. **Load best practices reference:** When schema errors occur, load k8s_best_practices.md for context

## Creating Validation Reports

Generate a comprehensive validation report with all findings. Do NOT modify files.

### Report Components

1. **Header with issue count**
   ```
   ## Validation Report - 7 issues found (4 errors, 3 warnings)
   ```

2. **Issues Summary Table**
   ```
   | Severity | Stage | Location | Issue | Suggested Fix |
   |----------|-------|----------|-------|---------------|
   | Error | Syntax | file.yaml:8 | Wrong indentation | Use 2 spaces |
   | Error | Schema | file.yaml:21 | Wrong type | Change to integer |
   | Warning | Best Practice | file.yaml:30 | Missing labels | Add app label |
   ```

3. **Detailed Findings** (for each issue)
   - File:line reference
   - Current code block
   - Suggested fix code block
   - Explanation of why it matters

4. **Validation status by stage**
   - Show which stages passed/failed
   - Note if any stages were skipped (e.g., no cluster access)

5. **Next Steps**
   - List errors that must be fixed before deployment
   - List warnings for best practices consideration
   - Suggest re-running validation after fixes

### Example Report Format

```
## Validation Report - 7 issues found

File: deployment.yaml
Resources Analyzed: 3 (Deployment, Service, Certificate)

| Stage | Status | Issues |
|-------|--------|--------|
| YAML Syntax | ❌ Failed | 2 errors |
| CRD Detection | ✅ Passed | 1 CRD found |
| Schema Validation | ❌ Failed | 2 errors |
| Dry-Run | ❌ Failed | 1 error |

### Issue 1: deployment.yaml:8 - Wrong indentation (Error)

Current:
```yaml
    labels:
```

Suggested Fix:
```yaml
  labels:
```

**Why:** Kubernetes YAML requires 2-space indentation.

### Issue 2: deployment.yaml:21 - Wrong field type (Error)

Current:
```yaml
        - containerPort: "80"
```

Suggested Fix:
```yaml
        - containerPort: 80
```

**Why:** containerPort must be an integer, not a string.

[... more issues ...]

## Next Steps

1. Fix the 4 errors listed above (deployment will fail without these)
2. Consider addressing the 3 warnings for best practices
3. Re-run validation to confirm all issues resolved
```

### Report Best Practices

- **Be specific:** List every issue with exact location
- **Show both current and suggested:** Always show before/after code blocks
- **Explain impact:** Help user understand why each issue matters
- **Group by file:** When multiple files are involved
- **Prioritize by severity:** Errors first, then warnings, then info
- **Provide file references:** Always include file:line for traceability
- **Clear next steps:** Tell user exactly what to do
