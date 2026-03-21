---
title: "Github Actions Validator"
description: "Validate, lint, audit, fix GitHub Actions workflows (.github/workflows)."
category: "devops"
source: "community"
author: "Community"
tags: ["github", "actions", "validator"]
date: 2026-03-20
---

# GitHub Actions Validator

## Overview

Validate and test GitHub Actions workflows, custom actions, and public actions using industry-standard tools (actionlint and act). This skill provides comprehensive validation including syntax checking, static analysis, local workflow execution testing, and action verification with version-aware documentation lookup.

## Trigger Phrases

Use this skill when the request includes phrases like:
- "validate this GitHub Actions workflow"
- "check my `.github/workflows/*.yml` file"
- "debug actionlint errors"
- "test this workflow locally with act"
- "verify GitHub Action versions or deprecations"

## When to Use This Skill

Use this skill when:
- **Validating workflow files**: Checking `.github/workflows/*.yml` for syntax errors and best practices
- **Testing workflows locally**: Running workflows with `act` before pushing to GitHub
- **Debugging workflow failures**: Identifying issues in workflow configuration
- **Validating custom actions**: Checking composite, Docker, or JavaScript actions
- **Verifying public actions**: Validating usage of actions from GitHub Marketplace
- **Pre-commit validation**: Ensuring workflows are valid before committing

## Required Execution Flow

Every validation run should follow these steps in order.

### Step 1: Set Skill Path and Run Validation

Run commands from the repository root that contains `.github/workflows/`.

```bash
SKILL_DIR="devops-skills-plugin/skills/github-actions-validator"
bash "$SKILL_DIR/scripts/validate_workflow.sh" <workflow-file-or-directory>
```

### Step 2: Map Each Error to a Reference

For each actionlint/act error, consult the mapping table below, then extract the matching fix pattern.

### Step 3: Apply Minimal-Quote Policy

For each issue:
1. Include the exact error line from tool output.
2. Quote only the smallest useful snippet from `references/` (prefer <=8 lines).
3. Paraphrase the rest and cite the source file/section.
4. Show corrected workflow code.

### Step 4: Handle Unmapped Errors Explicitly

If an error does not match any mapping:
1. Label it as `UNMAPPED`.
2. Capture exact tool output, workflow file, and line number (if available).
3. Check `references/common_errors.md` general sections first.
4. If still unresolved, search official docs with the exact error string.
5. Mark the fix as `provisional` until post-fix rerun passes.

### Step 5: Verify Public Action Versions

For each `uses: owner/action@version`:
1. Check `references/action_versions.md`.
2. For unknown actions, verify against official docs.
3. Confirm required inputs and deprecations.

Offline mode behavior:
- If network/doc lookup is unavailable, rely on `references/action_versions.md` only.
- Mark unknown actions as `UNVERIFIED-OFFLINE`.
- Do not claim "latest" version without an online verification pass.

### Step 6: Mandatory Post-Fix Rerun

After applying fixes, rerun validation before finalizing:

```bash
SKILL_DIR="devops-skills-plugin/skills/github-actions-validator"
bash "$SKILL_DIR/scripts/validate_workflow.sh" <workflow-file-or-directory>
```

### Step 7: Provide Final Summary

Final output should include:
- Issues found and fixes applied
- Any `UNMAPPED` or `UNVERIFIED-OFFLINE` items
- Post-fix rerun command and result
- Remaining warnings/risk notes

### Error Type to Reference File Mapping

| Error Pattern in Output | Reference File to Read | Section to Quote |
|------------------------|----------------------|------------------|
| `runs-on:`, `runner`, `ubuntu`, `macos`, `windows` | `references/runners.md` | Runner labels |
| `cron`, `schedule` | `references/common_errors.md` | Schedule Errors |
| `${{`, `expression`, `if:` | `references/common_errors.md` | Expression Errors |
| `needs:`, `job`, `dependency` | `references/common_errors.md` | Job Configuration Errors |
| `uses:`, `action`, `input` | `references/common_errors.md` | Action Errors |
| `untrusted`, `injection`, `security` | `references/common_errors.md` | Script Injection section |
| `syntax`, `yaml`, `unexpected` | `references/common_errors.md` | Syntax Errors |
| `docker`, `container` | `references/act_usage.md` | Troubleshooting |
| `@v3`, `@v4`, `deprecated`, `outdated` | `references/action_versions.md` | Version table |
| `workflow_call`, `reusable`, `oidc` | `references/modern_features.md` | Relevant section |
| `glob`, `path`, `paths:`, `pattern` | `references/common_errors.md` | Path Filter Errors |

### Example: Complete Error Handling Workflow

**User's workflow has this error:**
```
runs-on: ubuntu-lastest
```

**Step 1 - Script output:**
```
label "ubuntu-lastest" is unknown
```

**Step 2 - Read `references/runners.md` or `references/common_errors.md`:**
Find the "Invalid Runner Label" section.

**Step 3 - Quote the fix to user:**

> **Error:** `label "ubuntu-lastest" is unknown`
>
> **Cause:** Typo in runner label (from `references/common_errors.md`):
> ```yaml
> # Bad
> runs-on: ubuntu-lastest  # Typo
> ```
>
> **Fix** (from `references/common_errors.md`):
> ```yaml
> # Good
> runs-on: ubuntu-latest
> ```
>
> **Valid runner labels** (from `references/runners.md`):
> - `ubuntu-latest`, `ubuntu-24.04`, `ubuntu-22.04`
> - `windows-latest`, `windows-2025`, `windows-2022`
> - `macos-latest`, `macos-15`, `macos-14`

**Step 4 - Provide corrected code:**
```yaml
runs-on: ubuntu-latest
```

## Quick Start

Set once per shell session:

```bash
SKILL_DIR="devops-skills-plugin/skills/github-actions-validator"
```

### Initial Setup

```bash
bash "$SKILL_DIR/scripts/install_tools.sh"
```

This installs **act** (local workflow execution) and **actionlint** (static analysis) to `scripts/.tools/`.

### Basic Validation

```bash
# Validate a single workflow
bash "$SKILL_DIR/scripts/validate_workflow.sh" .github/workflows/ci.yml

# Validate all workflows
bash "$SKILL_DIR/scripts/validate_workflow.sh" .github/workflows/

# Lint-only (fastest)
bash "$SKILL_DIR/scripts/validate_workflow.sh" --lint-only .github/workflows/ci.yml

# Test-only with act (requires Docker)
bash "$SKILL_DIR/scripts/validate_workflow.sh" --test-only .github/workflows/
```

## Core Validation Workflow

### 1. Static Analysis with actionlint

Start with static analysis to catch syntax errors and common issues:

```bash
bash "$SKILL_DIR/scripts/validate_workflow.sh" --lint-only .github/workflows/ci.yml
```

**What actionlint checks:** YAML syntax, schema compliance, expression syntax, runner labels, action inputs/outputs, job dependencies, CRON syntax, glob patterns, shell scripts, security vulnerabilities.

### 2. Local Testing with act

After passing static analysis, test workflow execution:

```bash
bash "$SKILL_DIR/scripts/validate_workflow.sh" --test-only .github/workflows/
```

**Note:** act has limitations - see `references/act_usage.md`.

### 3. Full Validation

```bash
bash "$SKILL_DIR/scripts/validate_workflow.sh" .github/workflows/ci.yml
```

Default behavior if tools/runtime are unavailable:
- If `act` is missing, full validation falls back to actionlint-only.
- If Docker is unavailable, full validation skips act and continues with actionlint.
- `--check-versions` works in offline/local mode using `references/action_versions.md`.

## Validating Resource Types

### Workflows

```bash
# Single workflow
bash "$SKILL_DIR/scripts/validate_workflow.sh" .github/workflows/ci.yml

# All workflows
bash "$SKILL_DIR/scripts/validate_workflow.sh" .github/workflows/
```

**Key validation points:** triggers, job configurations, runner labels, environment variables, secrets, conditionals, matrix strategies.

### Custom Local Actions

Create a test workflow that uses the custom action, then validate:

```bash
bash "$SKILL_DIR/scripts/validate_workflow.sh" .github/workflows/test-custom-action.yml
```

### Public Actions

When workflows use public actions (e.g., `actions/checkout@v6`):

1. Check `references/action_versions.md` first
2. Use official docs (or web search) for unknown actions
3. Verify required inputs and version
4. Check for deprecation warnings
5. Run validation script

If offline:
- Mark unknown versions as `UNVERIFIED-OFFLINE`
- Avoid "latest/current" claims until online verification is possible

**Search format:** `"[action-name] [version] github action documentation"`

## Reference File Consultation Guide

### Mandatory Reference Consultation

| Situation | Reference File | Action |
|-----------|---------------|--------|
| actionlint reports any mapped error | `references/common_errors.md` | Find matching error and apply minimal quote policy |
| actionlint reports unmapped error | `references/common_errors.md` + official docs | Label as `UNMAPPED`, capture exact output and verify by rerun |
| act fails with Docker/runtime error | `references/act_usage.md` | Check Troubleshooting section |
| act fails but workflow works on GitHub | `references/act_usage.md` | Read Limitations section |
| User asks about actionlint config | `references/actionlint_usage.md` | Provide examples |
| User asks about act options | `references/act_usage.md` | Read Advanced Options |
| Security vulnerability detected | `references/common_errors.md` | Quote minimal safe fix snippet |
| Validating action versions | `references/action_versions.md` | Check version table and offline note |
| Using modern features | `references/modern_features.md` | Check syntax examples |
| Runner questions/errors | `references/runners.md` | Check labels and availability |

### Script Output to Reference Mapping

| Output Pattern | Reference File |
|----------------|----------------|
| `[syntax-check]`, parse, YAML errors | `common_errors.md` - Syntax Errors |
| `[expression]`, `${{`, condition parsing | `common_errors.md` - Expression Errors |
| `[action]`, `uses:`, input/output mismatch | `common_errors.md` - Action Errors |
| `[events]` with CRON/schedule text | `common_errors.md` - Schedule Errors |
| `potentially untrusted`, injection warnings | `common_errors.md` - Security section |
| `[runner-label]` or unknown `runs-on` label | `runners.md` |
| `[job-needs]` dependency errors | `common_errors.md` - Job Configuration Errors |
| `[glob]`, `paths`, pattern errors | `common_errors.md` - Path Filter Errors |
| Docker/pull/image errors from act | `act_usage.md` - Troubleshooting |
| No pattern match | `common_errors.md` + official docs (label `UNMAPPED`) |

## Reference Files Summary

| File | Content |
|------|---------|
| `references/act_usage.md` | Act tool usage, commands, options, limitations, troubleshooting |
| `references/actionlint_usage.md` | Actionlint validation categories, configuration, integration |
| `references/common_errors.md` | Common errors catalog with fixes |
| `references/action_versions.md` | Current action versions, deprecation timeline, SHA pinning |
| `references/modern_features.md` | Reusable workflows, SBOM, OIDC, environments, containers |
| `references/runners.md` | GitHub-hosted runners (ARM64, GPU, M2 Pro, deprecations) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Tools not found" | Run `bash "$SKILL_DIR/scripts/install_tools.sh"` |
| "Docker daemon not running" | Start Docker or use `--lint-only` |
| "Permission denied" | Run `chmod +x "$SKILL_DIR"/scripts/*.sh` |
| act fails but GitHub works | See `references/act_usage.md` Limitations |

### Debug Mode

```bash
actionlint -verbose .github/workflows/ci.yml  # Verbose actionlint
act -v                                         # Verbose act
act -n                                         # Dry-run (no execution)
```

## Best Practices

1. **Always validate locally first** - Catch errors before pushing
2. **Use actionlint in CI/CD** - Automate validation in pipelines
3. **Pin action versions** - Use `@v6` not `@main` for stability; SHA pinning for security
4. **Keep tools updated** - Regularly update actionlint and act
5. **Use official docs for unknown actions** - Verify usage and versions
6. **Check version compatibility** - See `references/action_versions.md`
7. **Enable shellcheck** - Catch shell script issues early
8. **Review security warnings** - Address script injection issues

## Limitations

- **act limitations**: Not all GitHub Actions features work locally
- **Docker requirement**: act requires Docker to be running
- **Network actions**: Some GitHub API actions may fail locally
- **Private actions**: Cannot validate without access
- **Runtime behavior**: Static analysis cannot catch all issues
- **File location**: act can only validate workflows in `.github/workflows/` directory; files outside (like `examples/`) can only be validated with actionlint

## Quick Examples

### Example 1: Pre-commit Validation

```bash
SKILL_DIR="devops-skills-plugin/skills/github-actions-validator"
bash "$SKILL_DIR/scripts/validate_workflow.sh" .github/workflows/
git add .github/workflows/ && git commit -m "Update workflows"
```

### Example 2: Debug Failing Workflow

```bash
bash "$SKILL_DIR/scripts/validate_workflow.sh" --lint-only .github/workflows/failing.yml
# Fix issues
bash "$SKILL_DIR/scripts/validate_workflow.sh" .github/workflows/failing.yml
```

## Complete Worked Example: Multi-Error Workflow

This example demonstrates the **full assistant workflow** for handling multiple errors.

### User's Problematic Workflow

```yaml
name: Broken CI
on:
  schedule:
    - cron: '0 0 * * 8'  # ERROR 1
jobs:
  build:
    runs-on: ubuntu-lastest  # ERROR 2
    steps:
      - uses: actions/checkout@v3  # ERROR 3 (outdated)
      - run: echo ${{ github.event.issue.title }}  # ERROR 4 (security)
  deploy:
    needs: biuld  # ERROR 5 (typo)
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying"
```

### Step 1: Run Validation

```bash
bash "$SKILL_DIR/scripts/validate_workflow.sh" --lint-only workflow.yml
```

**Output:**
```
[ERROR] invalid CRON format "0 0 * * 8"
[ERROR] label "ubuntu-lastest" is unknown
[WARN] "github.event.issue.title" is potentially untrusted
[ERROR] job "deploy" needs job "biuld" which does not exist
```

### Step 2-3: Consult References and Quote Fixes

---

**Error 1: Invalid CRON Expression**

*From `references/common_errors.md` - Schedule Errors:*

> **Cause:** Day of week 8 doesn't exist (valid: 0-6, where 0 = Sunday)
>
> ```yaml
> # Bad
> schedule:
>   - cron: '0 0 * * 8'  # Day 8 doesn't exist
>
> # Good
> schedule:
>   - cron: '0 0 * * 0'  # Sunday
> ```
>
> **CRON format:** `minute hour day month weekday`
> - Weekday: 0-6 (0 = Sunday)

**Fix:** Change `8` to `0` (Sunday) or `1-6` for Monday-Saturday.

---

**Error 2: Invalid Runner Label**

*From `references/common_errors.md` - Job Configuration Errors and `references/runners.md`:*

> **Cause:** Typo in runner label
>
> ```yaml
> # Bad
> runs-on: ubuntu-lastest  # Typo
>
> # Good
> runs-on: ubuntu-latest
> ```
>
> **Valid labels (from `references/runners.md`):**
> - `ubuntu-latest` (Ubuntu 24.04)
> - `ubuntu-24.04`, `ubuntu-22.04`
> - `macos-latest` (macOS 15)
> - `windows-latest` (Windows Server 2022)

**Fix:** Change `ubuntu-lastest` to `ubuntu-latest`.

---

**Error 3: Outdated Action Version**

*From `references/action_versions.md`:*

> | Action | Current Version | Minimum Supported |
> |--------|----------------|-------------------|
> | `actions/checkout` | **v6** | v4 |
>
> **SHA Pinning Best Practice:**
> ```yaml
> # Recommended: SHA pinning with version comment
> - uses: actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3  # v6.0.0
> ```

**Fix:** Update from `@v3` to `@v6` (or SHA-pinned version).

---

**Error 4: Security Vulnerability (Script Injection)**

*From `references/common_errors.md` - Expression Errors:*

> **Warning:** Potential script injection via untrusted input
>
> ```yaml
> # Bad - vulnerable to injection
> run: echo ${{ github.event.issue.title }}
>
> # Good - use environment variables
> env:
>   TITLE: ${{ github.event.issue.title }}
> run: echo "$TITLE"
> ```
>
> **Why:** Untrusted input (issue titles, PR bodies, commit messages) can contain malicious commands. Using environment variables sanitizes the input.

**Fix:** Pass untrusted input through environment variable.

---

**Error 5: Undefined Job Dependency**

*From `references/common_errors.md` - Job Configuration Errors:*

> **Error:** Job 'deploy' depends on job 'biuld' which does not exist
>
> ```yaml
> # Bad
> jobs:
>   build:
>     runs-on: ubuntu-latest
>   deploy:
>     needs: biuld  # Typo
>
> # Good
> jobs:
>   build:
>     runs-on: ubuntu-latest
>   deploy:
>     needs: build
> ```

**Fix:** Change `biuld` to `build`.

---

### Step 4: Provide Corrected Workflow

```yaml
name: Fixed CI
on:
  schedule:
    - cron: '0 0 * * 0'  # Fixed: Sunday (0-6 valid)
jobs:
  build:
    runs-on: ubuntu-latest  # Fixed: typo corrected
    steps:
      - uses: actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3  # v6.0.0 - Fixed: updated version
      - name: Process issue
        env:
          TITLE: ${{ github.event.issue.title }}  # Fixed: use env var
        run: echo "$TITLE"
  deploy:
    needs: build  # Fixed: typo corrected
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying"
```

### Step 5: Mandatory Rerun

```bash
bash "$SKILL_DIR/scripts/validate_workflow.sh" --lint-only workflow.yml
```

Expected rerun result:
- No previous errors reproduced
- Remaining warnings, if any, are documented explicitly

### Step 6: Summary

| Error | Type | Fix Applied |
|-------|------|-------------|
| CRON `0 0 * * 8` | Schedule | Changed to `0 0 * * 0` |
| `ubuntu-lastest` | Runner | Changed to `ubuntu-latest` |
| `checkout@v3` | Outdated Action | Updated to `@v6.0.0` (SHA-pinned) |
| Direct `${{ }}` in run | Security | Wrapped in environment variable |
| `needs: biuld` | Job Dependency | Changed to `needs: build` |

**Recommendations:**
- Run `bash "$SKILL_DIR/scripts/validate_workflow.sh" --check-versions` regularly
- Use SHA pinning for all actions in production workflows
- Always pass untrusted input through environment variables

## Done Criteria

Validation work is complete when all are true:
- Trigger matched and correct validation mode selected.
- Each mapped error includes source reference and minimal quote.
- Each unmapped error is labeled `UNMAPPED` with exact output captured.
- Public action versions are verified, or marked `UNVERIFIED-OFFLINE`.
- Post-fix rerun executed and result reported.

## Summary

1. **Setup**: Install tools with `install_tools.sh`
2. **Validate**: Run `validate_workflow.sh` on workflow files
3. **Fix**: Address issues using reference documentation
4. **Rerun**: Verify fixes with a mandatory post-fix validation run
5. **Search**: Use official docs to verify unknown actions
6. **Commit**: Push validated workflows with confidence

For detailed information, consult the appropriate reference file in `references/`.

---

## Reference: Act_Usage

# Act (nektos/act) - Usage Reference

Act is a tool that allows you to run your GitHub Actions locally, providing fast feedback and acting as a local task runner.

## Installation

```bash
# Install act using the official script
curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | bash

# Or use the skill's installation script
bash scripts/install_tools.sh
```

## Core Commands

### List Workflows

List all available workflows in the repository:

```bash
act -l
```

List workflows for a specific event:

```bash
act -l pull_request
act -l push
act -l workflow_dispatch
```

### Dry Run (No Execution)

Validate workflows without executing them, useful for inspection and validation:

```bash
act -n
# or (long form)
act --dryrun
```

This performs a dry run that:
- Parses all workflow files
- Validates syntax
- Shows what would be executed
- Does NOT actually run any jobs
- Returns exit code 0 on success, non-zero on errors

**Important for Validation:** The dry-run mode is perfect for validating workflow syntax before pushing to GitHub.

### Run Workflows

Run the default workflow:

```bash
act
```

Run workflows for a specific event:

```bash
act push
act pull_request
act workflow_dispatch
```

Run a specific job:

```bash
act -j <job-id>
```

Run a specific workflow file:

```bash
act -W .github/workflows/ci.yml
```

## Common Use Cases

### 1. Validate Workflow Syntax

Use dry run to check if workflows parse correctly:

```bash
act -n
```

If there are syntax errors, act will report them immediately.

### 2. Test Workflows Locally

Before pushing to GitHub, test workflows locally:

```bash
# Test push event workflows
act push

# Test pull request workflows
act pull_request
```

### 3. Debug Workflow Issues

Run workflows with verbose output:

```bash
act -v
```

### 4. List Available Events

See which events have workflows configured:

```bash
act -l
```

Output format:
```
Stage  Job ID  Job name  Workflow name  Workflow file  Events
0      build   build     CI             ci.yml         push,pull_request
0      test    test      CI             ci.yml         push,pull_request
```

## Advanced Options

### Container Architecture

Ensure consistent platform behavior across different machines:

```bash
act --container-architecture linux/amd64
```

This is especially important on ARM-based Macs (M1/M2/M3) to ensure workflows run in the same environment as GitHub's x64 runners.

### Using Specific Docker Images

Act uses Docker containers to run jobs. Specify custom images:

```bash
act -P ubuntu-latest=node:16-buster
```

### Configuration File

Create `.actrc` file in your project or home directory to set default options:

```bash
# .actrc
--container-architecture=linux/amd64
--action-offline-mode
```

Options are loaded in this order:
1. XDG spec `.actrc`
2. HOME directory `.actrc`
3. Current directory `.actrc`
4. CLI arguments

### Passing Secrets

Provide secrets for testing:

```bash
act -s GITHUB_TOKEN=ghp_xxx
```

Or use a secrets file:

```bash
act --secret-file .secrets
```

### Environment Variables

Set environment variables:

```bash
act --env MY_VAR=value
```

### Input Variables (for workflow_dispatch)

Pass input variables:

```bash
act workflow_dispatch --input myInput=myValue
```

## Limitations

Be aware of act's limitations:

1. **Not 100% Compatible**: Some GitHub Actions features may not work exactly as on GitHub
2. **Docker Required**: act requires Docker to be installed and running
3. **Network Actions**: Some actions that interact with GitHub's API may fail
4. **Runner Images**: Default runner images may differ from GitHub's hosted runners
5. **Secrets**: Local testing requires manually providing secrets

## Exit Codes

- `0`: Success - all jobs passed
- `1`: Failure - at least one job failed
- `2`: Error - workflow parsing or execution error

## Best Practices for Validation

1. **Always run dry-run first**: `act -n` to catch syntax errors
2. **Test specific events**: Don't run all workflows, target the event you care about
3. **Use verbose mode for debugging**: `act -v` when troubleshooting
4. **Check Docker availability**: Ensure Docker is running before using act
5. **Consider limitations**: Not all features work locally - use for syntax and basic logic validation

## Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution**: Start Docker Desktop or Docker daemon

### Issue: "Workflow file not found"

**Solution**: Ensure you're in the repository root or use `-W` to specify the workflow file path

### Issue: "Action not found"

**Solution**: Some actions may not be available locally. Use `-P` to specify alternative Docker images or skip the problematic action for validation purposes

### Issue: "Out of disk space"

**Solution**: Clean up Docker images: `docker system prune -a`

---

## Reference: Action_Versions

# Action Version Validation Reference

This reference provides current recommended action versions and validation procedures for GitHub Actions workflows.

## Current Recommended Versions (December 2025)

| Action | Current Version | Minimum Supported | Notes |
|--------|----------------|-------------------|-------|
| `actions/checkout` | **v6** | v4 | v6 stores credentials in $RUNNER_TEMP |
| `actions/setup-node` | **v6** | v4 | v6 adds Node 24 support |
| `actions/setup-python` | **v5** | v4 | v5 adds Python 3.13 support |
| `actions/setup-java` | **v4** | v4 | Current latest |
| `actions/setup-go` | **v5** | v4 | v5 adds Go 1.23 support |
| `actions/cache` | **v4** | v4 | v4.2.0+ required as of Feb 2025 |
| `actions/upload-artifact` | **v4** | v4 | v3 deprecated |
| `actions/download-artifact` | **v4** | v4 | v3 deprecated |
| `docker/setup-buildx-action` | **v3** | v3 | Current latest |
| `docker/login-action` | **v3** | v3 | Current latest |
| `docker/build-push-action` | **v6** | v5 | v6 adds provenance attestation |
| `docker/metadata-action` | **v5** | v5 | Current latest |
| `aws-actions/configure-aws-credentials` | **v4** | v4 | OIDC support improved |

## Version Validation Process

### Step 1: Extract Action References

For each `uses:` statement in the workflow, extract:
- Action name (e.g., `actions/checkout`)
- Version (e.g., `v4`, `v4.1.1`, or SHA like `b4ffde65f46...`)

### Step 2: Compare Against Recommended Versions

For each action found:
1. Look up the action in the table above
2. Compare the workflow version against the **Current Version**
3. Flag if using a version older than **Minimum Supported**

### Step 3: Report Findings

Generate warnings for:
- **OUTDATED**: Action using older major version (e.g., checkout@v4 when v6 is current)
- **DEPRECATED**: Action using version below minimum supported
- **UP-TO-DATE**: Action using current or acceptable version

## Example Version Validation Output

```
=== Action Version Check ===

actions/checkout@v6.0.0 - UP-TO-DATE (current: v6)
actions/setup-java@v4.2.1 - UP-TO-DATE (current: v4)
docker/build-push-action@v5.3.0 - OUTDATED (current: v6, using: v5)
actions/upload-artifact@v3 - DEPRECATED (minimum: v4, using: v3)

Recommendation: Update docker/build-push-action to v6 for provenance attestation support
Recommendation: Update actions/upload-artifact to v4 (v3 is deprecated)
```

## Using the Version Check Flag

```bash
# Check action versions in workflow
bash scripts/validate_workflow.sh --check-versions .github/workflows/ci.yml

# Full validation including version check
bash scripts/validate_workflow.sh .github/workflows/ci.yml
```

## Node.js Runtime Deprecation Timeline

GitHub Actions runtime requirements:
- **Node.js 12**: EOL April 2022 - Actions using this are deprecated
- **Node.js 16**: EOL September 2023 - Actions using this are deprecated
- **Node.js 20**: EOL April 2026 - Current runtime for most actions
- **Node.js 22/24**: Current LTS - Newer actions support these

## SHA Pinning Best Practice

For security, pin actions to specific commit SHAs:

```yaml
# Recommended: SHA pinning with version comment
- uses: actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3  # v6.0.0
- uses: actions/setup-node@2028fbc5c25fe9cf00d9f06a71cc4710d4507903  # v6.0.0

# Acceptable: Major version tag
- uses: actions/checkout@v6

# Not recommended: Branch reference
- uses: actions/checkout@main
```

## Cache Storage Updates (November 2025)

GitHub Actions cache storage expanded beyond the 10 GB limit:

**New Features:**
- **Pay-as-you-go model**: Repositories can store more than 10 GB of cache data
- **Free tier**: All repositories continue to receive 10 GB at no additional cost
- **New management policies**:
  - Cache size eviction limit (GB): Control maximum cache size
  - Cache retention limit (days): Set how long caches are retained

**Pricing:**
- First 10 GB per repository: **FREE**
- Additional storage: Comparable to Git LFS and Codespaces storage
- Requires Pro, Team, or Enterprise account to exceed 10 GB limit

**Cache best practices:**
- Monitor cache usage in repository settings
- Configure eviction limits to control costs
- Use appropriate retention periods for your workflow
- Clean up old caches regularly
- Consider cache key strategies to avoid cache bloat

## Validation Checklist

When validating workflows, ALWAYS:
1. Run the validation script
2. Manually review `uses:` statements against the version table
3. Warn about any outdated or deprecated versions
4. Suggest specific upgrade paths with SHA pinning

---

## Reference: Actionlint_Usage

# Actionlint (rhysd/actionlint) - Usage Reference

Actionlint is a static checker for GitHub Actions workflow files that catches errors before they cause CI failures.

## Installation

```bash
# Download and install using the official script
bash <(curl https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)

# Or use the skill's installation script
bash scripts/install_tools.sh
```

## Core Usage

### Basic Validation

Validate a single workflow file:

```bash
actionlint .github/workflows/ci.yml
```

Validate all workflow files in a directory:

```bash
actionlint .github/workflows/*.yml
```

Validate all workflows in the default location:

```bash
actionlint
```

### Output Formats

#### Default Format (human-readable)

```bash
actionlint
```

Output example:
```
.github/workflows/ci.yml:5:7: unexpected key "job" for "workflow" section [syntax-check]
.github/workflows/ci.yml:10:15: invalid CRON format "0 0 * * 8" in schedule event [events]
```

#### JSON Format

```bash
actionlint -format '{{json .}}'
```

Useful for programmatic processing and integration with other tools.

#### Sarif Format

```bash
actionlint -format sarif
```

For integration with GitHub Code Scanning and other security tools.

## Validation Categories

### 1. Syntax Checking

Validates YAML syntax and GitHub Actions schema:

- Required fields
- Valid keys and values
- Proper nesting
- Type correctness

### 2. Expression Validation

Validates GitHub Actions expressions `${{ }}`:

- Syntax errors
- Type checking (string, number, boolean)
- Function calls
- Context access

Example caught errors:
```yaml
# Error: Boolean expression expected
if: ${{ 'true' }}  # String, not boolean

# Error: Unknown function
run: echo ${{ unknown() }}

# Error: Type mismatch
if: ${{ 42 }}  # Number, not boolean
```

### 3. Runner Label Validation

Validates runner labels against known GitHub-hosted runners:

**Ubuntu:**
- `ubuntu-latest` (currently ubuntu-24.04)
- `ubuntu-24.04`, `ubuntu-22.04`, `ubuntu-20.04`

**Windows:**
- `windows-latest` (currently windows-2022)
- `windows-2025` (NEW - recently added)
- `windows-2022`, `windows-2019`

**macOS:**
- `macos-latest` (currently macos-15)
- `macos-15` (Apple Silicon M1/M2/M3)
- `macos-14` (Apple Silicon M1)
- `macos-26` (preview)
- `macos-13` (Intel - RETIRED November 14, 2025)
- `macos-12` (Intel - RETIRED)

Example:
```yaml
runs-on: ubuntu-lastest  # Error: Did you mean "ubuntu-latest"?
```

### 4. Action Validation

Validates action references:

- Action exists
- Valid version/ref
- Required inputs provided
- No unknown inputs

Example:
```yaml
# Error: Missing required input "path"
- uses: actions/checkout@v5

# Error: Unknown input "invalid_input"
- uses: actions/checkout@v5
  with:
    invalid_input: value
```

### 5. Job Dependencies

Validates `needs:` dependencies:

- Referenced jobs exist
- No circular dependencies
- Valid job IDs

### 6. CRON Syntax

Validates schedule event CRON expressions:

```yaml
# Error: Day of week must be 0-6
schedule:
  - cron: '0 0 * * 8'
```

### 7. Shell Script Validation

Integrates with shellcheck to validate shell scripts in `run:` steps:

```yaml
# Warning: Quote to prevent word splitting
run: echo $VARIABLE
```

### 8. Glob Pattern Validation

Validates glob patterns in `paths:` and `paths-ignore:` filters for structural errors (e.g., empty patterns or malformed syntax).

**Note:** The pattern `**.js` (double-star without a slash) is **not flagged** by actionlint as of v1.7.x. It is functionally equivalent to `**/*.js` in GitHub's glob engine but `**/*.js` is more explicit and widely understood. Use `**/*.js` as a best practice, not because actionlint will warn about the alternative.

```yaml
# Best practice (clear intent)
on:
  push:
    paths:
      - '**/*.js'   # Matches any .js file in any subdirectory
      - 'src/**'    # Matches everything under src/
```

### 9. Security Checks

Detects potential security issues:

- Injection vulnerabilities
- Insecure credential handling
- Dangerous patterns

Example:
```yaml
# Warning: Potential script injection
run: echo ${{ github.event.issue.title }}
```

## Configuration

Create `.github/actionlint.yaml` or `.github/actionlint.yml`:

```yaml
# Configure shellcheck
shellcheck:
  enable: true
  shell: bash

# Configure pyflakes for Python
pyflakes:
  enable: true
  executable: pyflakes

# Ignore specific rules
ignore:
  - 'SC2086'  # Ignore shellcheck rule
  - 'action-validation'  # Ignore action validation

# Custom runner labels
self-hosted-runner:
  labels:
    - my-custom-runner
    - gpu-runner
```

## Exit Codes

- `0`: Success - no errors found
- `1`: Validation errors found
- `2`: Fatal error (invalid file, config error, etc.)

## Integration

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/rhysd/actionlint
    rev: v1.7.9  # Check https://github.com/rhysd/actionlint/releases for latest version
    hooks:
      - id: actionlint
```

**Note:** Always use the latest version of actionlint. Check the [releases page](https://github.com/rhysd/actionlint/releases) for the most recent version.

### GitHub Actions Workflow

```yaml
name: Lint GitHub Actions workflows
on: [push, pull_request]
jobs:
  actionlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3 # v6.0.0
      - name: Download actionlint
        run: bash <(curl https://raw.githubusercontent.com/rhysd/actionlint/main/scripts/download-actionlint.bash)
      - name: Run actionlint
        run: ./actionlint
```

### VS Code Integration

Install the "actionlint" extension for real-time validation in VS Code.

## Common Error Examples

### 1. Typo in Runner Label

```yaml
# Error
runs-on: ubuntu-lastest

# Fix
runs-on: ubuntu-latest
```

### 2. Invalid CRON Expression

```yaml
# Error
schedule:
  - cron: '0 0 * * 8'  # Day of week 8 doesn't exist

# Fix
schedule:
  - cron: '0 0 * * 0'  # Sunday = 0
```

### 3. Missing Required Input

```yaml
# Error
- uses: actions/checkout@v4

# Fix (if repository input is required)
- uses: actions/checkout@v4
  with:
    repository: owner/repo
```

### 4. Invalid Expression

```yaml
# Error
if: ${{ success() && 'true' }}  # Mixing boolean and string

# Fix
if: ${{ success() && true }}
```

### 5. Undefined Job in needs

```yaml
# Error
jobs:
  deploy:
    needs: biuld  # Typo

# Fix
jobs:
  deploy:
    needs: build
```

## Best Practices

1. **Run locally before pushing**: Catch errors early
2. **Use in CI/CD**: Add actionlint to your workflow
3. **Configure for custom runners**: Update config for self-hosted runners
4. **Enable shellcheck**: Catch shell script issues
5. **Review all warnings**: Even non-fatal warnings can indicate issues
6. **Keep actionlint updated**: New rules and features are added regularly

## Limitations

- Cannot validate runtime behavior (only static analysis)
- Cannot access private actions (must be public to validate)
- May not catch all possible issues (e.g., environment-specific problems)
- Custom actions may require manual verification

---

## Reference: Common_Errors

# Common GitHub Actions Errors and Solutions

This reference lists common errors encountered when working with GitHub Actions and how to fix them.

## Syntax Errors

### 1. Invalid YAML Syntax

**Error:**
```
Error: Unable to process file command 'workflow' successfully.
```

**Common Causes:**
- Incorrect indentation (YAML is whitespace-sensitive)
- Missing colons
- Unquoted strings containing special characters
- Tabs instead of spaces

**Fix:**
```yaml
# Bad
name:My Workflow
jobs:
build:
  runs-on: ubuntu-latest

# Good
name: My Workflow
jobs:
  build:
    runs-on: ubuntu-latest
```

### 2. Missing Required Fields

**Error:**
```
Required property is missing: name
```

**Fix:**
```yaml
# Every workflow needs a name
name: CI Pipeline

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3  # v6.0.0
```

### 3. Invalid Workflow Triggers

**Error:**
```
The workflow is not valid. Unexpected value 'on'
```

**Fix:**
```yaml
# Bad - wrong event name
on:
  pull-request:  # Should be pull_request

# Good
on:
  pull_request:
  push:
```

## Expression Errors

### 1. Incorrect Expression Syntax

**Error:**
```
Unrecognized named-value: 'github'. Located at position 1 within expression: github.ref
```

**Fix:**
```yaml
# Bad - missing ${{ }}
if: github.ref == 'refs/heads/main'

# Good
if: ${{ github.ref == 'refs/heads/main' }}

# Even better (GitHub Actions auto-evaluates if conditions)
if: github.ref == 'refs/heads/main'
```

### 2. Type Mismatches

**Error:**
```
Expected boolean value, got string
```

**Fix:**
```yaml
# Bad
if: ${{ 'true' }}  # String, not boolean

# Good
if: ${{ true }}
if: ${{ success() }}
if: ${{ github.event_name == 'push' }}
```

### 3. Script Injection Vulnerabilities

**Warning:**
```
Potential script injection via untrusted input
```

**Fix:**
```yaml
# Bad - vulnerable to injection
run: echo ${{ github.event.issue.title }}

# Good - use environment variables
env:
  TITLE: ${{ github.event.issue.title }}
run: echo "$TITLE"
```

## Action Errors

### 1. Action Not Found

**Error:**
```
Can't find 'action.yml', 'action.yaml' or 'Dockerfile' under '/home/runner/work/_actions/actions/chekout/v4'
```

**Common Causes:**
- Typo in action name
- Invalid action reference
- Action doesn't exist or was removed

**Fix:**
```yaml
# Bad
- uses: actions/chekout@v4  # Typo

# Good
- uses: actions/checkout@v4
```

### 2. Missing Required Inputs

**Error:**
```
Input required and not supplied: path
```

**Fix:**
```yaml
# Bad
- uses: some-action@v1

# Good
- uses: some-action@v1
  with:
    path: ./my-path
```

### 3. Unknown Action Inputs

**Error:**
```
Unexpected input 'invalid_input'
```

**Fix:**
```yaml
# Check the action's documentation for valid inputs
- uses: actions/checkout@v4
  with:
    # Only use documented inputs
    ref: main
    # Remove undocumented inputs
```

### 4. Deprecated Action Versions

**Warning:**
```
Node.js 12/16 actions are deprecated
```

**Fix:**
```yaml
# Deprecated - Node.js 12 (EOL April 2022)
- uses: actions/checkout@v2

# Deprecated - Node.js 16 (EOL September 2023)
- uses: actions/checkout@v3

# Older - Node.js 20 (EOL April 2026)
- uses: actions/checkout@v4
- uses: actions/checkout@v5

# Current - Node.js 20+/24 (v6)
- uses: actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3  # v6.0.0
- uses: actions/setup-node@2028fbc5c25fe9cf00d9f06a71cc4710d4507903  # v6.0.0

# Note: Node.js 20 EOL is April 2026, Node.js 22 and 24 are current
```

## Job Configuration Errors

### 1. Invalid Runner Label

**Error:**
```
Unable to locate executable file: ubuntu-lastest
```

**Fix:**
```yaml
# Bad
runs-on: ubuntu-lastest  # Typo

# Good
runs-on: ubuntu-latest
```

Valid runner labels:
- `ubuntu-latest`, `ubuntu-22.04`, `ubuntu-20.04`
- `windows-latest`, `windows-2025`, `windows-2022`, `windows-2019`
- `macos-latest` (now macOS 15), `macos-15`, `macos-14`, `macos-26` (preview)
- `macos-13` (RETIRED November 14, 2025 - no longer available)
- `macos-15-intel`, `macos-15-large` (Intel x86_64, long-term deprecated)
- `macos-15-xlarge`, `macos-14-xlarge` (M2 Pro with GPU)
- `gpu-t4-4-core` (GPU runners for ML/AI)
- ARM64 runners (free for public repos)

### 2. Undefined Job Dependency

**Error:**
```
Job 'deploy' depends on job 'biuld' which does not exist
```

**Fix:**
```yaml
# Bad
jobs:
  build:
    runs-on: ubuntu-latest
  deploy:
    needs: biuld  # Typo

# Good
jobs:
  build:
    runs-on: ubuntu-latest
  deploy:
    needs: build
```

### 3. Circular Job Dependencies

**Error:**
```
Circular dependency detected
```

**Fix:**
```yaml
# Bad
jobs:
  job1:
    needs: job2
  job2:
    needs: job1  # Circular!

# Good
jobs:
  job1:
    runs-on: ubuntu-latest
  job2:
    needs: job1
```

## Schedule Errors

### 1. Invalid CRON Syntax

**Error:**
```
Invalid CRON expression: '0 0 * * 8'
```

**Fix:**
```yaml
# Bad
schedule:
  - cron: '0 0 * * 8'  # Day 8 doesn't exist

# Good
schedule:
  - cron: '0 0 * * 0'  # Sunday

# CRON format: minute hour day month weekday
# Minute: 0-59
# Hour: 0-23
# Day: 1-31
# Month: 1-12
# Weekday: 0-6 (0 = Sunday)
```

### 2. Multiple Schedule Entries

```yaml
# Correct way to define multiple schedules
on:
  schedule:
    - cron: '0 0 * * 1'  # Monday at midnight
    - cron: '0 12 * * 5'  # Friday at noon
```

## Path Filter Errors

### 1. Glob Pattern Best Practices

**Note:** `**.js` (double-star without a slash) is **not flagged by actionlint** as an error. GitHub's glob engine treats it similarly to `**/*.js`, but `**/*.js` is the conventional and explicit form. Prefer it for clarity.

```yaml
# Not recommended (ambiguous intent, but accepted by actionlint and GitHub)
on:
  push:
    paths:
      - '**.js'

# Recommended (explicit and conventional)
on:
  push:
    paths:
      - '**/*.js'
      - 'src/**'
```

## Environment and Secrets

### 1. Secret Not Found

**Error:**
```
Secret MY_SECRET not found
```

**Fix:**
- Ensure the secret is defined in repository settings
- Check secret name spelling (case-sensitive)
- Verify secret scope (repository vs organization vs environment)

```yaml
# Use secrets correctly
env:
  API_KEY: ${{ secrets.MY_SECRET }}  # Must match name in settings
```

### 2. Environment Variables in run

**Common Issue:**
```yaml
# Bad - environment variable not accessible
steps:
  - run: echo $MY_VAR  # May not work on Windows

# Good - use env
steps:
  - name: Print variable
    env:
      MY_VAR: ${{ secrets.MY_SECRET }}
    run: echo "$MY_VAR"  # Unix
    # or
    run: echo $env:MY_VAR  # Windows PowerShell
```

## Matrix Strategy Errors

### 1. Invalid Matrix Configuration

**Error:**
```
Matrix configuration is invalid
```

**Fix:**
```yaml
# Bad
strategy:
  matrix:
    os: ubuntu-latest  # Should be an array

# Good
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [20, 22, 24]  # Node 16 EOL Sep 2023, Node 20 EOL Apr 2026
```

### 2. Matrix Variable Reference

```yaml
# Correct way to reference matrix variables
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
jobs:
  test:
    runs-on: ${{ matrix.os }}
```

## Conditional Execution Errors

### 1. Always/Cancelled/Failure Conditions

```yaml
# Understanding conditions
steps:
  - name: Run on success (default)
    run: echo "Runs only if previous steps succeeded"

  - name: Run always
    if: always()
    run: echo "Runs whether previous steps succeeded or failed"

  - name: Run on failure
    if: failure()
    run: echo "Runs only if a previous step failed"

  - name: Run on success
    if: success()
    run: echo "Runs only if all previous steps succeeded"
```

## Debugging Tips

### 1. Enable Debug Logging

Set secrets in repository settings:
- `ACTIONS_STEP_DEBUG` = `true` (detailed step logs)
- `ACTIONS_RUNNER_DEBUG` = `true` (runner diagnostic logs)

### 2. Use tmate for Interactive Debugging

```yaml
steps:
  - name: Setup tmate session
    if: failure()
    uses: mxschmitt/action-tmate@v3
```

### 3. Print Context Information

```yaml
steps:
  - name: Dump GitHub context
    run: echo '${{ toJSON(github) }}'

  - name: Dump job context
    run: echo '${{ toJSON(job) }}'

  - name: Dump runner context
    run: echo '${{ toJSON(runner) }}'
```

## Best Practices

1. **Always use specific action versions**: `actions/checkout@v6` not `actions/checkout@main`
2. **Quote strings with special characters**: `name: "My: Workflow"`
3. **Use shellcheck**: Enable shell script linting
4. **Validate locally**: Use act and actionlint before pushing
5. **Use env for secrets**: Never put secrets directly in run commands
6. **Keep workflows DRY**: Use reusable workflows and composite actions
7. **Set timeouts**: Prevent runaway jobs with `timeout-minutes`
8. **Use concurrency**: Cancel redundant runs with concurrency groups

```yaml
# Example of good practices
name: Production Deployment

on:
  push:
    branches: [main]

concurrency:
  group: production
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@1af3b93b6815bc44a9784bd300feb67ff0d1eeb3  # v6.0.0

      - name: Deploy
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          ./deploy.sh
```

---

## Reference: Modern_Features

# Modern GitHub Actions Features Reference

This reference covers validation of modern GitHub Actions features including reusable workflows, attestations, OIDC authentication, and more.

## Reusable Workflows

### Validation Points
- `workflow_call` trigger configuration
- Required and optional inputs with correct types
- Secrets declaration and usage
- Outputs definition

### Example

```yaml
# Reusable workflow (.github/workflows/reusable-deploy.yml)
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      deploy-version:
        required: false
        type: string
        default: 'latest'
    secrets:
      deploy-token:
        required: true
    outputs:
      deployment-url:
        description: "The URL of the deployment"
        value: ${{ jobs.deploy.outputs.url }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    outputs:
      url: ${{ steps.deploy.outputs.url }}
    steps:
      - name: Deploy
        id: deploy
        run: echo "url=https://example.com" >> $GITHUB_OUTPUT
```

### Common Errors
- Incorrect input types (string, number, boolean)
- Missing required secrets
- Invalid output references

### Workflow Limits (November 2025)

GitHub Actions increased reusable workflow limits:
- **Nested workflows**: Up to 10 levels (previously 4)
- **Total workflows per run**: Up to 50 workflows (previously 20)

This enables complex workflow compositions and better code reuse.

---

## SBOM and Build Provenance Attestations

### Validation Points
- Correct permissions (`id-token: write`, `attestations: write`)
- Valid artifact paths
- Proper attestation action usage

### Example

```yaml
permissions:
  id-token: write
  contents: read
  attestations: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Build artifact
        run: |
          mkdir -p dist
          tar -czvf dist/app.tar.gz ./src

      - name: Generate SBOM
        run: |
          # Generate SPDX SBOM
          syft ./src -o spdx-json > sbom.spdx.json

      - uses: actions/attest-sbom@v3
        with:
          subject-path: '${{ github.workspace }}/dist/*.tar.gz'
          sbom-path: '${{ github.workspace }}/sbom.spdx.json'

      - uses: actions/attest-build-provenance@v3
        with:
          subject-path: '${{ github.workspace }}/dist/*.tar.gz'
```

### Common Errors
- Missing required permissions
- Invalid subject-path glob patterns
- Incorrect SBOM format

---

## OIDC Authentication

### Validation Points
- Correct permissions (`id-token: write`)
- Valid audience claims
- Proper OIDC provider configuration
- Token claim validation in receiving systems

### Available Token Claims (November 2025)

| Claim | Description |
|-------|-------------|
| `repository` | Repository name |
| `ref` | Git ref (branch/tag) |
| `sha` | Commit SHA |
| `workflow` | Workflow name |
| `run_id` | Workflow run ID |
| `run_attempt` | Attempt number |
| `check_run_id` | **NEW** - Specific check run ID for the job |
| `actor` | User who triggered the workflow |
| `environment` | Deployment environment (if applicable) |

### Example: AWS OIDC

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
          aws-region: us-east-1
          # Token now includes check_run_id for granular tracking

      - name: Deploy to AWS
        run: aws s3 sync ./build s3://my-bucket/
```

### AWS IAM Policy with check_run_id

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:sub": "repo:org/repo:ref:refs/heads/main",
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
      },
      "StringLike": {
        "token.actions.githubusercontent.com:check_run_id": "*"
      }
    }
  }]
}
```

### Benefits of check_run_id
- **Fine-grained access control**: Trace tokens to exact job and compute
- **Improved auditability**: Track which specific check run made API calls
- **Least-privilege policies**: Attribute-based access control without enumerating repositories
- **Faster revocation**: Reduce secret exposure risk

---

## Deployment Environments

### Validation Points
- Environment name configuration
- Protection rules compatibility
- Required reviewers setup
- Environment variables and secrets scope

### Example

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v6
      - run: ./deploy.sh staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment:
      name: production
      url: https://prod.example.com
    steps:
      - uses: actions/checkout@v6
      - run: ./deploy.sh production
```

### Common Errors
- Undefined environment names
- Missing URL for environment tracking
- Incorrect environment variable scope

---

## Job Summaries

### Validation Points
- Correct usage of `$GITHUB_STEP_SUMMARY`
- Valid Markdown formatting
- Proper escaping of dynamic content

### Example

```yaml
steps:
  - name: Run tests
    id: tests
    run: |
      # Run tests and capture results
      npm test 2>&1 | tee test-output.txt
      PASSED=$(grep -c "PASS" test-output.txt || echo 0)
      FAILED=$(grep -c "FAIL" test-output.txt || echo 0)
      echo "passed=$PASSED" >> $GITHUB_OUTPUT
      echo "failed=$FAILED" >> $GITHUB_OUTPUT

  - name: Generate summary
    run: |
      echo "## Test Results" >> $GITHUB_STEP_SUMMARY
      echo "" >> $GITHUB_STEP_SUMMARY
      echo "| Status | Count |" >> $GITHUB_STEP_SUMMARY
      echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
      echo "| Passed | ${{ steps.tests.outputs.passed }} |" >> $GITHUB_STEP_SUMMARY
      echo "| Failed | ${{ steps.tests.outputs.failed }} |" >> $GITHUB_STEP_SUMMARY
```

**Note:** Job summaries are runtime features - actionlint validates script syntax but not summary content.

---

## Container Jobs

### Validation Points
- Valid container image references
- Correct volume mounts
- Environment variable configuration
- Service container networking

### Example

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: node:24
      env:
        NODE_ENV: test
      volumes:
        - /data:/data

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v6

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:postgres@postgres:5432/testdb
          REDIS_URL: redis://redis:6379
        run: npm test
```

### Common Errors
- Invalid image tags
- Incorrect volume mount syntax
- Service container networking issues
- Missing health checks for services

---

## Matrix Strategies

### Validation Points
- Matrix values must be arrays
- Valid matrix variable references
- Proper include/exclude syntax

### Example

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [20, 22, 24]
        exclude:
          - os: macos-latest
            node: 20
        include:
          - os: ubuntu-latest
            node: 24
            experimental: true

    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: ${{ matrix.node }}
      - run: npm test
```

---

## Concurrency Control

### Validation Points
- Valid concurrency group names
- Proper cancel-in-progress usage

### Example

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.ref != 'refs/heads/main' }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - run: npm ci && npm run build
```

This prevents redundant runs while protecting main branch runs from cancellation.

---

## Reference: Runners

# GitHub-Hosted Runners Reference (2025)

This reference covers all GitHub-hosted runner types, including recent additions and deprecations.

## Standard Runner Labels

### Ubuntu

```yaml
runs-on: ubuntu-latest      # Ubuntu 24.04 (default)
runs-on: ubuntu-24.04       # Ubuntu 24.04
runs-on: ubuntu-22.04       # Ubuntu 22.04
runs-on: ubuntu-20.04       # Ubuntu 20.04
```

### Windows

```yaml
runs-on: windows-latest     # Windows Server 2022 (default)
runs-on: windows-2025       # Windows Server 2025 (NEW)
runs-on: windows-2022       # Windows Server 2022
runs-on: windows-2019       # Windows Server 2019
```

### macOS

```yaml
runs-on: macos-latest       # macOS 15 (as of Aug 2025)
runs-on: macos-15           # macOS 15 Sequoia (Apple Silicon)
runs-on: macos-14           # macOS 14 Sonoma (Apple Silicon)
runs-on: macos-26           # macOS 26 (PREVIEW)
```

---

## macOS Runner Updates and Deprecations

### Current Status

| Label | Status | Architecture | Notes |
|-------|--------|--------------|-------|
| `macos-latest` | **Active** | ARM64 (Apple Silicon) | Points to macOS 15 |
| `macos-15` | **Active** | ARM64 (Apple Silicon) | M1/M2/M3 |
| `macos-14` | **Active** | ARM64 (Apple Silicon) | M1/M2 |
| `macos-26` | **Preview** | ARM64 (Apple Silicon) | Beta |
| `macos-13` | **RETIRED** | Intel x86_64 | Retired November 14, 2025 |
| `macos-12` | **RETIRED** | Intel x86_64 | Retired |

### Intel-Specific Labels (Long-term Deprecated)

```yaml
runs-on: macos-15-intel     # Intel x86_64 (NEW but deprecated long-term)
runs-on: macos-14-large     # Intel x86_64
runs-on: macos-15-large     # Intel x86_64
```

**Important:** Apple Silicon (ARM64) will be required after Fall 2027. Plan migration now.

### Migration Example

```yaml
jobs:
  build:
    # BAD - macos-13 retired Nov 14, 2025 (WILL FAIL)
    # runs-on: macos-13

    # GOOD - Use macos-15 or macos-latest
    runs-on: macos-15

    steps:
      - uses: actions/checkout@v6
      - run: ./build.sh
```

---

## ARM64 Runners

### Availability
- **Generally available** as of August 2025
- **Free** for public repositories
- **Private repositories** require GitHub Enterprise Cloud plan

### Labels

```yaml
runs-on: ubuntu-latest-arm64    # Free for public repos
runs-on: ubuntu-24.04-arm64
runs-on: windows-latest-arm64   # ARM Windows
```

### Example

```yaml
jobs:
  build:
    runs-on: ubuntu-latest-arm64  # Free for public repos
    steps:
      - uses: actions/checkout@v6
      - name: Build on ARM64
        run: |
          uname -m  # Should output: aarch64
          ./build.sh
```

### Specifications
- 4 vCPU ARM64 processors
- Available for Linux and Windows
- Native ARM execution (no virtualization needed)
- Ideal for multi-architecture builds

### Common Validation Issues
- Using ARM64 runners in private repos without Enterprise Cloud
- Assuming all community actions work on ARM64
- Not testing ARM-specific compilation issues

---

## GPU Runners

### Availability
- **Generally available** for Windows and Linux
- Requires **Team** or **Enterprise Cloud** plan

### Labels

```yaml
runs-on: gpu-t4-4-core      # NVIDIA Tesla T4
```

### Specifications
- **GPU:** NVIDIA Tesla T4 with 16GB VRAM
- **CPU:** 4 vCPUs
- **RAM:** 28GB
- **Pricing:** $0.07/minute

### Example

```yaml
jobs:
  ml-training:
    runs-on: gpu-t4-4-core
    steps:
      - uses: actions/checkout@v6

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install ML dependencies
        run: |
          pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
          pip install -r requirements.txt

      - name: Train model
        run: python train.py --use-gpu

      - name: Run inference
        run: python inference.py
```

### Use Cases
- ML model training
- GPU-accelerated testing
- CUDA development
- Image/video processing

### Common Validation Issues
- Missing CUDA setup
- Incorrect GPU driver versions
- Not utilizing GPU in workloads (CPU fallback)
- Missing GPU-specific dependencies

---

## M2 Pro macOS Runners (Larger Runners)

### Availability
- **Generally available** with M2 Pro powered runners

### Labels

```yaml
runs-on: macos-latest-xlarge  # macOS 15, M2 Pro
runs-on: macos-15-xlarge      # macOS 15, M2 Pro
runs-on: macos-14-xlarge      # macOS 14, M2 Pro
```

### Specifications
- **CPU:** 5-core (vs 3-core standard)
- **GPU:** 8-core with hardware acceleration (enabled by default)
- **RAM:** 14GB
- **Storage:** 14GB
- **Performance:** Up to 15% faster than M1 runners
- **Pricing:** $0.16/minute

### Example

```yaml
jobs:
  ios-build:
    runs-on: macos-15-xlarge  # M2 Pro with GPU acceleration
    steps:
      - uses: actions/checkout@v6

      - name: Setup Xcode
        uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: latest-stable

      - name: Build iOS app
        run: |
          xcodebuild -workspace App.xcworkspace \
            -scheme Production \
            -configuration Release \
            -archivePath build/App.xcarchive \
            archive

      - name: Run GPU-accelerated tests
        run: |
          # GPU acceleration automatically available
          xcodebuild test -scheme AppTests
```

### Benefits
- GPU hardware acceleration for Metal-based workloads
- Improved build times for iOS/macOS apps
- Better performance for Xcode builds
- Native Apple Silicon performance

---

## Runner Selection Best Practices

### Decision Criteria

1. **Architecture compatibility:** ARM64 vs Intel x86_64
2. **Cost optimization:** Standard vs larger runners
3. **GPU requirements:** ML/AI workloads need GPU runners
4. **Operating system:** Latest versions recommended
5. **Deprecation timelines:** Avoid retired runners
6. **Public vs private repos:** ARM64 free only for public repos

### Validation Checklist

```yaml
# Check these in your workflows:
- [ ] Using latest runner versions (macos-15, windows-2025, ubuntu-latest)
- [ ] Not using deprecated runners (macos-13)
- [ ] Architecture-appropriate runners (ARM64 vs Intel)
- [ ] GPU runners for ML workloads
- [ ] Cost-effective runner selection
- [ ] ARM64 compatibility tested (if using ARM64 runners)
```

### Cost Comparison

| Runner Type | Pricing | Best For |
|-------------|---------|----------|
| Standard (Linux/Windows) | Included | Most workloads |
| Standard (macOS) | Included | iOS/macOS builds |
| ARM64 (public repos) | **Free** | Multi-arch builds |
| ARM64 (private repos) | Enterprise | ARM-native builds |
| GPU (T4) | $0.07/min | ML/AI workloads |
| M2 Pro (xlarge) | $0.16/min | Heavy iOS builds |

---

## Multi-Architecture Builds

### Example: Building for Multiple Architectures

```yaml
jobs:
  build:
    strategy:
      matrix:
        include:
          - runner: ubuntu-latest
            arch: x64
          - runner: ubuntu-latest-arm64
            arch: arm64

    runs-on: ${{ matrix.runner }}
    steps:
      - uses: actions/checkout@v6

      - name: Build
        run: |
          echo "Building for ${{ matrix.arch }}"
          ./build.sh --arch ${{ matrix.arch }}

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.arch }}
          path: dist/
```

---

## Self-Hosted Runner Configuration

When using self-hosted runners, configure actionlint to recognize custom labels:

```yaml
# .github/actionlint.yaml
self-hosted-runner:
  labels:
    - my-custom-runner
    - gpu-runner
    - arm-runner
    - on-premises
```

This prevents actionlint from reporting unknown runner label errors.

---

## Example: Readme

# GitHub Actions Validator - Example Workflows

This directory contains example workflow files for testing the GitHub Actions Validator skill.

## Files

### valid-ci.yml

A complete, valid CI pipeline that passes all validation checks.

**Purpose:** Test successful validation flow

**Usage:**
```bash
bash scripts/validate_workflow.sh examples/valid-ci.yml
```

**Expected Result:** All validations pass

---

### with-errors.yml

A workflow containing common intentional errors for testing error detection.

**Purpose:** Test error detection and reference file consultation

**Errors included (4 total, all caught by actionlint):**
1. Invalid CRON expression (day 8 doesn't exist) — `[events]`
2. Typo in runner label (`ubuntu-lastest` instead of `ubuntu-latest`) — `[runner-label]`
3. Script injection vulnerability (untrusted input in script) — `[expression]`
4. Undefined job dependency (`biuld` instead of `build`) — `[job-needs]`

**Usage:**
```bash
bash scripts/validate_workflow.sh examples/with-errors.yml
```

**Expected Result:** Multiple errors reported by actionlint

---

### outdated-versions.yml

A workflow using older action versions to test version validation.

**Purpose:** Test action version checking

**Version issues included:**
1. `actions/checkout@v4` - OUTDATED (current: v6)
2. `actions/setup-node@v4` - OUTDATED (current: v6)
3. `actions/upload-artifact@v3` - DEPRECATED (minimum: v4)
4. `docker/build-push-action@v5` - OUTDATED (current: v6)

**Usage:**
```bash
bash scripts/validate_workflow.sh --check-versions examples/outdated-versions.yml
```

**Expected Result:** Version warnings for outdated actions

---

## Testing Workflow

1. **Test successful validation:**
   ```bash
   bash scripts/validate_workflow.sh examples/valid-ci.yml
   ```

2. **Test error detection:**
   ```bash
   bash scripts/validate_workflow.sh examples/with-errors.yml
   ```

3. **Test version checking:**
   ```bash
   bash scripts/validate_workflow.sh --check-versions examples/outdated-versions.yml
   ```

4. **Test all examples:**
   ```bash
   for file in examples/*.yml; do
     echo "=== Testing: $file ==="
     bash scripts/validate_workflow.sh --lint-only "$file"
     echo ""
   done
   ```
