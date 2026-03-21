---
title: "Terragrunt Generator"
description: "Generate/create/scaffold Terragrunt HCL files — root.hcl, terragrunt.hcl, child modules, stacks, multi-env layouts."
category: "research"
source: "community"
author: "Community"
tags: ["terragrunt", "generator"]
date: 2026-03-20
---

# Terragrunt Generator

## Overview

Generate production-ready Terragrunt configurations following current best practices, naming conventions, and security standards. All generated configurations are automatically validated.

## Trigger Phrases

Use this skill when the user asks for:
- A new `root.hcl`, `terragrunt.hcl`, or `terragrunt.stack.hcl`
- Multi-environment Terragrunt layouts (`dev/staging/prod`)
- Terragrunt dependency wiring (`dependency` or `dependencies` blocks)
- Terragrunt module source setup (local, Git, Terraform Registry via `tfr:///`)
- Stack catalog unit generation under `catalog/units/*`

**Terragrunt 2025 Features Supported:**
- [Stacks](https://terragrunt.gruntwork.io/docs/features/stacks/) - Infrastructure blueprints with `terragrunt.stack.hcl` (GA since v0.78.0)
- [Feature Flags](https://terragrunt.gruntwork.io/docs/features/feature-flags/) - Runtime control via `feature` blocks
- [Exclude Blocks](https://terragrunt.gruntwork.io/docs/reference/config-blocks-and-attributes/#exclude) - Fine-grained execution control (replaces deprecated `skip`)
- [Errors Blocks](https://terragrunt.gruntwork.io/docs/reference/config-blocks-and-attributes/#errors) - Advanced error handling (replaces deprecated `retryable_errors`)
- [OpenTofu Engine](https://terragrunt.gruntwork.io/docs/features/engine/) - Alternative IaC engine support

## Root Configuration Naming

> **RECOMMENDED**: Use `root.hcl` instead of `terragrunt.hcl` for root files per [migration guide](https://terragrunt.gruntwork.io/docs/migrate/migrating-from-root-terragrunt-hcl).

| Approach | Root File | Include Syntax |
|----------|-----------|----------------|
| **Modern** | `root.hcl` | `find_in_parent_folders("root.hcl")` |
| **Legacy** | `terragrunt.hcl` | `find_in_parent_folders()` |

**Include standard:** Default to `find_in_parent_folders("root.hcl")` in all new examples and generated configs. Use `find_in_parent_folders()` only when explicitly targeting a legacy root file named `terragrunt.hcl`.

## Architecture Patterns

> **CRITICAL:** Before generating ANY configuration, you MUST determine the architecture pattern and understand its constraints.

### Pattern A: Multi-Environment with Environment-Agnostic Root

**Use when:** Managing multiple environments (dev/staging/prod) with shared root configuration.

**Key principle:** `root.hcl` is **environment-agnostic** - it does NOT read environment-specific files.

```
infrastructure/
├── root.hcl              # Environment-AGNOSTIC (no env.hcl references)
├── dev/
│   ├── env.hcl           # Environment variables (locals block)
│   ├── vpc/terragrunt.hcl
│   └── rds/terragrunt.hcl
└── prod/
    ├── env.hcl           # Environment variables (locals block)
    ├── vpc/terragrunt.hcl
    └── rds/terragrunt.hcl
```

**Root.hcl constraints:**
- ❌ CANNOT use `read_terragrunt_config(find_in_parent_folders("env.hcl"))` - env.hcl doesn't exist at root level
- ❌ CANNOT reference `local.environment` or `local.aws_region` that come from env.hcl
- ✅ CAN use static values or `get_env()` for runtime configuration
- ✅ CAN use `${path_relative_to_include()}` for state keys (this works dynamically)

**Child modules read env.hcl:**
```hcl
# dev/vpc/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  env = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

inputs = {
  name = "${local.env.locals.environment}-vpc"  # Works: env.hcl exists in dev/
}
```

### Pattern B: Single Environment or Environment-Aware Root

**Use when:** Single environment OR all environments share the same root with environment detection.

```
infrastructure/
├── root.hcl              # Can be environment-aware via get_env() or directory parsing
├── account.hcl           # Account-level config (optional)
├── region.hcl            # Region-level config (optional)
└── vpc/
    └── terragrunt.hcl
```

**Root.hcl can detect environment:**
```hcl
# root.hcl - environment detection via directory path
locals {
  # Parse environment from path (e.g., "prod/vpc" -> "prod")
  path_parts  = split("/", path_relative_to_include())
  environment = local.path_parts[0]

  # OR use environment variable
  environment = get_env("TG_ENVIRONMENT", "dev")
}
```

### Pattern C: Shared Environment Variables (_env directory)

**Use when:** Centralizing environment variables with symlinks or direct references.

```
infrastructure/
├── root.hcl              # Environment-AGNOSTIC
├── _env/                 # Centralized environment definitions
│   ├── prod.hcl
│   ├── staging.hcl
│   └── dev.hcl
├── prod/
│   ├── env.hcl           # Reads from _env/prod.hcl
│   └── vpc/terragrunt.hcl
└── dev/
    ├── env.hcl           # Reads from _env/dev.hcl
    └── vpc/terragrunt.hcl
```

**env.hcl reads from _env:**
```hcl
# prod/env.hcl
locals {
  env_vars = read_terragrunt_config("${get_repo_root()}/_env/prod.hcl")

  # Re-export for child modules
  environment        = local.env_vars.locals.environment
  aws_region         = local.env_vars.locals.aws_region
  vpc_cidr           = local.env_vars.locals.vpc_cidr
  # ... other variables
}
```

### Architecture Pattern Selection Checklist (Canonical)

> **MANDATORY:** Before writing any files, you MUST complete this checklist and OUTPUT it to the user with checkmarks filled in. This is not optional.

**Output this completed checklist before generating any files:**
```
## Architecture Pattern Selection

[x] Identified architecture pattern: Pattern ___ (A/B/C)
[x] Root.hcl scope: [ ] environment-agnostic  OR  [ ] environment-aware
[x] env.hcl location: ___________________
[x] Child modules access env via: ___________________
[x] Verified: No file references a path that doesn't exist from its location
```

**Example completed checklist:**
```
## Architecture Pattern Selection

[x] Identified architecture pattern: Pattern A (Multi-Environment with Environment-Agnostic Root)
[x] Root.hcl scope: [x] environment-agnostic  OR  [ ] environment-aware
[x] env.hcl location: dev/env.hcl, prod/env.hcl (one per environment)
[x] Child modules access env via: read_terragrunt_config(find_in_parent_folders("env.hcl"))
[x] Verified: No file references a path that doesn't exist from its location
```

## Quick Variable Definition Examples

Use these starter files for Pattern B and account/region-aware setups.

**env.hcl**
```hcl
locals {
  environment = "dev"
  aws_region  = "us-east-1"
  project     = "platform"
}
```

**account.hcl**
```hcl
locals {
  account_id   = "123456789012"
  account_name = "shared-services"
}
```

**region.hcl**
```hcl
locals {
  aws_region = "us-east-1"
}
```

## When to Use

- Creating new Terragrunt projects or configurations
- Setting up multi-environment infrastructure (dev/staging/prod)
- Implementing DRY Terraform configurations
- Managing complex infrastructure with dependencies
- Working with custom Terraform providers or modules

## Core Capabilities

### 1. Generate Root Configuration
Create root-level `root.hcl` or `terragrunt.hcl` with remote state, provider config, and common variables.

> **MANDATORY:** Before generating, READ the template file:
> ```
> Read: assets/templates/root/terragrunt.hcl
> ```

**Template:** `assets/templates/root/terragrunt.hcl`
**Patterns:** `references/common-patterns.md` → Root Configuration Patterns

**Key placeholders to replace:**
- `[BUCKET_NAME]`, `[AWS_REGION]`, `[DYNAMODB_TABLE]`
- `[TERRAFORM_VERSION]`, `[PROVIDER_NAME]`, `[PROVIDER_SOURCE]`, `[PROVIDER_VERSION]`
- `[ENVIRONMENT]`, `[PROJECT_NAME]`

**Root.hcl Design Principles:**
1. **Environment-agnostic by default** - Don't assume env.hcl exists at root level
2. **Use static values for provider/backend region** - Or use `get_env()` for runtime config
3. **State key uses `path_relative_to_include()`** - This automatically includes environment path
4. **Provider tags can be static** - Environment-specific tags go in child modules

### 2. Generate Child Module Configuration
Create child modules with dependencies, mock outputs, and proper includes.

> **MANDATORY:** Before generating, READ the template file:
> ```
> Read: assets/templates/child/terragrunt.hcl
> ```

**Template:** `assets/templates/child/terragrunt.hcl`
**Patterns:** `references/common-patterns.md` → Child Module Patterns

**Module source options:**
- Local: `"../../modules/vpc"`
- Git: `"git::https://github.com/org/repo.git//path?ref=v1.0.0"`
- Registry: `"tfr:///terraform-aws-modules/vpc/aws?version=5.1.0"`

### 3. Generate Standalone Module
Self-contained modules without root dependency.

> **MANDATORY:** Before generating, READ the template file:
> ```
> Read: assets/templates/module/terragrunt.hcl
> ```

**Template:** `assets/templates/module/terragrunt.hcl`

### Canonical Placeholder Replacement Map

Use this map for every generated output:

| Placeholder | Meaning | Example Replacement | Notes |
|-------------|---------|---------------------|-------|
| `[AWS_REGION]` | AWS region | `us-east-1` | Canonical region placeholder in all templates |
| `[ENVIRONMENT]` | Environment name | `dev` | Keep lowercase for directory naming |
| `[PROJECT_NAME]` | Project/application name | `payments-platform` | Use the same value in tags and names |
| `[BUCKET_NAME]` | Remote state S3 bucket | `acme-tfstate-prod` | Bucket must exist before first apply |
| `[DYNAMODB_TABLE]` | State lock table | `acme-terraform-locks` | Table must exist before first apply |
| `[PROVIDER_SOURCE]` | Terraform provider source | `hashicorp/aws` | Use fully qualified source |
| `[TERRAFORM_VERSION]` | Required Terraform/OpenTofu version | `1.8.5` | Used in both `terraform_version_constraint` and `required_version`. Keep compatible with module constraints. |

**Legacy alias normalization:** If you see `[REGION]` in older examples, treat it as `[AWS_REGION]` and replace it before validation.

### 4. Generate Multi-Environment Infrastructure
Complete directory structures for dev/staging/prod.

> **MANDATORY:** Before generating:
> 1. Determine architecture pattern (see Architecture Patterns section)
> 2. Read relevant templates for root, env, and child modules
> 3. Verify env.hcl placement and access patterns:
>    ```
>    Read: assets/templates/env/env.hcl
>    ```

**Patterns:** `references/common-patterns.md` → Environment-Specific Patterns

**Typical structure (Pattern A - Environment-Agnostic Root):**
```
infrastructure/
├── root.hcl              # Environment-AGNOSTIC root config
├── dev/
│   ├── env.hcl           # Dev environment variables
│   └── vpc/terragrunt.hcl
└── prod/
    ├── env.hcl           # Prod environment variables
    └── vpc/terragrunt.hcl
```

### 5. Generate Terragrunt Stacks (2025)
Infrastructure blueprints using `terragrunt.stack.hcl`.

> **MANDATORY:** Before generating, READ the template files:
> ```
> Read: assets/templates/stack/terragrunt.stack.hcl
> Read: assets/templates/catalog/terragrunt.hcl
> ```

**Docs:** [Stacks Documentation](https://terragrunt.gruntwork.io/docs/features/stacks/)
**Template:** `assets/templates/stack/terragrunt.stack.hcl`
**Catalog Template:** `assets/templates/catalog/terragrunt.hcl`
**Patterns:** `references/common-patterns.md` → Stacks Patterns

**Stack path rule:** Keep `no_dot_terragrunt_stack` mode consistent across dependent units. Do not mix direct-path and `.terragrunt-stack` generation in the same dependency chain.

**Commands:**
```bash
terragrunt stack generate    # Generate unit configurations
terragrunt stack run plan    # Plan all units
terragrunt stack run apply   # Apply all units
terragrunt stack output      # Get aggregated outputs
terragrunt stack clean       # Clean generated directories
```

### 6. Generate Feature Flags (2025)
Runtime control without code changes.

**Docs:** [Feature Flags Documentation](https://terragrunt.gruntwork.io/docs/features/feature-flags/)
**Patterns:** `references/common-patterns.md` → Feature Flags Patterns

> **CRITICAL:** Feature flag `default` values MUST be static (boolean, string, number).
> They CANNOT reference `local.*` values. Use static defaults and override via CLI/env vars.

**Correct:**
```hcl
feature "enable_monitoring" {
  default = false  # Static value - OK
}
```

**Incorrect:**
```hcl
feature "enable_monitoring" {
  default = local.env.locals.enable_monitoring  # Dynamic reference - FAILS
}
```

**Usage:**
```bash
terragrunt apply --feature enable_monitoring=true
# or
export TG_FEATURE="enable_monitoring=true"
```

**Environment-specific defaults:** Use different static defaults per environment file, not dynamic references.

### 7. Generate Exclude Blocks (2025)
Fine-grained execution control (replaces deprecated `skip`).

**Docs:** [Exclude Block Reference](https://terragrunt.gruntwork.io/docs/reference/config-blocks-and-attributes/#exclude)
**Patterns:** `references/common-patterns.md` → Exclude Block Patterns

**Actions:** `"plan"`, `"apply"`, `"destroy"`, `"all"`, `"all_except_output"`

**Production Recommendation:** For critical production resources, add exclude blocks to prevent accidental destruction:
```hcl
# Protect production databases from accidental destroy
exclude {
  if      = true
  actions = ["destroy"]
  exclude_dependencies = false
}

# Also use prevent_destroy for critical resources
prevent_destroy = true
```

### 8. Generate Errors Blocks (2025)
Advanced error handling (replaces deprecated `retryable_errors`).

**Docs:** [Errors Block Reference](https://terragrunt.gruntwork.io/docs/reference/config-blocks-and-attributes/#errors)
**Patterns:** `references/common-patterns.md` → Errors Block Patterns

### 9. Generate OpenTofu Engine Configuration (2025)
Use OpenTofu as the IaC engine.

**Docs:** [Engine Documentation](https://terragrunt.gruntwork.io/docs/features/engine/)
**Patterns:** `references/common-patterns.md` → OpenTofu Engine Patterns

### 10. Handling Custom Providers/Modules
When generating configs with custom providers:

1. **Identify** the provider name, source, and version
2. **Search** using WebSearch: `"[provider] terraform provider [version] documentation"`
3. **Or use Context7 MCP** if available for structured docs
4. **Generate** with proper `required_providers` block
5. **Document** authentication requirements in comments

## Generation Workflow

> **CRITICAL:** Follow this workflow for EVERY generation task. Skipping steps leads to validation errors.

### Step 1: Understand Requirements
- What type of configuration? (root, child, standalone, stack)
- Single or multi-environment?
- What dependencies exist between modules?
- What providers/modules will be used?

### Step 2: Determine Architecture Pattern
> **MANDATORY:** Select and document the pattern BEFORE writing any files.

| Scenario | Pattern | Root.hcl Scope |
|----------|---------|----------------|
| Multi-env with shared root | Pattern A | Environment-agnostic |
| Single environment | Pattern B | Environment-aware |
| Centralized env vars | Pattern C | Environment-agnostic |

Complete the **Architecture Pattern Selection Checklist (Canonical)** above and include it in output before file generation.

### Step 3: Read Required Templates
> **MANDATORY:** Read the relevant template file(s) BEFORE generating each configuration type.

| Configuration Type | Template to Read | Purpose |
|-------------------|------------------|---------|
| Root configuration | `assets/templates/root/terragrunt.hcl` | Shared state backend, providers, and common inputs |
| Environment variables | `assets/templates/env/env.hcl` | Per-environment locals read by child modules (Pattern A) |
| Child module | `assets/templates/child/terragrunt.hcl` | Environment module wired to root include |
| Standalone module | `assets/templates/module/terragrunt.hcl` | Independent Terragrunt module without root include |
| Stack file | `assets/templates/stack/terragrunt.stack.hcl` | Blueprint that generates multiple units |
| Catalog unit | `assets/templates/catalog/terragrunt.hcl` | Reusable unit template consumed by stacks |

**Also read:**
- `references/common-patterns.md` - Primary source for generation patterns

### Step 4: Generate with Validation

> **Validation Strategy:** Use a combination of inline checks during generation and batch validation at the end.

**Generation order for multi-environment projects:**

1. **Generate root.hcl first**
   - **Inline checks (during generation):**
     - [ ] No `read_terragrunt_config(find_in_parent_folders("env.hcl"))` if environment-agnostic
     - [ ] `remote_state` block has `encrypt = true`
     - [ ] `errors` block used (not deprecated `retryable_errors`)

2. **Generate env.hcl files for each environment**
   - **Inline checks (during generation):**
     - [ ] `locals` block contains environment, aws_region, and module-specific vars
     - [ ] No references to files that don't exist at that directory level

3. **Generate child modules (VPC, etc.) - modules with NO dependencies first**
   - **Inline checks (during generation):**
     - [ ] `include` block uses `find_in_parent_folders("root.hcl")`
     - [ ] `read_terragrunt_config(find_in_parent_folders("env.hcl"))` present
     - [ ] `terraform.source` uses valid syntax (`tfr:///`, `git::`, or relative path)

4. **Generate dependent modules (RDS, EKS, etc.)**
   - **Inline checks (during generation):**
     - [ ] `dependency` blocks have `mock_outputs`
     - [ ] `mock_outputs_allowed_terraform_commands` includes `["validate", "plan", "destroy"]`
     - [ ] Production modules have `prevent_destroy = true` and/or `exclude` block

5. **Run batch validation after ALL files are generated**
   > **Note:** Full CLI validation (`terragrunt hcl fmt`, `terragrunt dag graph`) requires all files to exist, so these are batched at the end.

   ```bash
   # Batch validation commands (run after all files exist):
   terragrunt hcl fmt --check          # Format validation
   terragrunt dag graph                 # Dependency graph validation
   ```

   - Invoke `Skill(devops-skills:terragrunt-validator)` for comprehensive validation

### Step 5: Fix and Re-Validate
If validation fails:
1. Analyze errors (path resolution, missing variables, syntax errors)
2. Fix issues in the specific file(s)
3. Re-validate the fixed file(s)
4. Repeat until ALL errors are resolved

### Step 6: Present Results
Follow "Presentation Requirements" section below.

## Validation Workflow

**CRITICAL:** Every generated configuration MUST be validated.

### Incremental Validation Checks

**After generating root.hcl:**
```bash
cd <infrastructure-directory>
terragrunt hcl fmt --check
```

**After generating each child module:**
```bash
cd <module-directory>
terragrunt hcl fmt --check
# If no dependencies on other modules:
terragrunt hcl validate --inputs
```

### Full Validation

After all files are generated:

1. **Invoke validation skill:**
   ```
   Invoke: Skill(devops-skills:terragrunt-validator)
   ```

2. **If validation fails:**
   - Analyze errors (missing placeholders, invalid syntax, wrong paths)
   - Fix issues
   - **Re-validate** (repeat until ALL errors are resolved)

3. **If validation succeeds:** Present configurations with usage instructions

**Skip validation only for:** Partial snippets, documentation examples, or explicit user request

### Validation Fallbacks (Environment Constraints)

If the normal validation path is unavailable, use this fallback order and report what was skipped:

1. If `terragrunt` is unavailable:
   - Run static checks:
     ```bash
     rg -n "\[[A-Z0-9_]+\]" .
     rg -n "find_in_parent_folders\\(\"env\\.hcl\"\\)" .
     ```
   - Report that runtime Terragrunt validation is pending.
2. If validator skill execution is unavailable:
   - Run direct Terragrunt checks instead:
     ```bash
     terragrunt hcl fmt --check
     terragrunt dag graph
     ```
3. If `tree` is unavailable for presentation:
   - Use:
     ```bash
     find . -maxdepth 4 -type f | sort
     ```

## Presentation Requirements

> **MANDATORY:** After successful validation, you MUST present ALL of the following sections. Incomplete presentation is not acceptable. Copy and fill in the templates below.

### 1. Directory Structure Summary (MANDATORY)
```bash
# Show the generated structure
tree <infrastructure-directory>
```

### 2. Files Generated (MANDATORY)

**Output this table with all generated files:**
```markdown
| File | Purpose |
|------|---------|
| root.hcl | Shared configuration for all child modules (state backend, provider) |
| dev/env.hcl | Development environment variables |
| prod/env.hcl | Production environment variables |
| dev/vpc/terragrunt.hcl | VPC module for development |
| ... | ... |
```

### 3. Usage Instructions (MANDATORY)

> **You MUST include this section.** Copy the template below and fill in the actual values:

```markdown
## Usage Instructions

### Prerequisites
Before running Terragrunt commands, ensure:
1. AWS credentials are configured (`aws configure` or environment variables)
2. S3 bucket `<BUCKET_NAME>` exists for state storage
3. DynamoDB table `<TABLE_NAME>` exists for state locking

### Commands

# Navigate to infrastructure directory
cd <INFRASTRUCTURE_DIR>

# Initialize all modules
terragrunt run --all init

# Preview changes for a specific environment
cd <ENV>/vpc && terragrunt plan

# Preview all changes
terragrunt run --all plan

# Apply changes (requires approval)
terragrunt run --all apply

# Destroy (use with extreme caution)
terragrunt run --all destroy
```

### 4. Placeholder Replacement and Secrets Check (MANDATORY)

> **You MUST include this section.** Copy the template below and fill in the actual values:

```markdown
## Placeholder and Secrets Check

### Placeholder Replacement
- [ ] All placeholders (`[AWS_REGION]`, `[BUCKET_NAME]`, `[DYNAMODB_TABLE]`, etc.) replaced with real values
- [ ] No legacy placeholder aliases left (for example `[REGION]`)
- [ ] `terraform.source` values point to real module sources and pinned versions

### Secrets Safety
- [ ] No plaintext credentials or access keys in `terragrunt.hcl`, `root.hcl`, `env.hcl`, `account.hcl`, or `region.hcl`
- [ ] Sensitive values sourced via environment variables, secret managers, or CI variables
- [ ] Example values kept non-sensitive and clearly marked as placeholders
```

### 5. Environment-Specific Notes (MANDATORY)

> **You MUST include this section.** Copy the template below and fill in the actual values:

```markdown
## Environment Notes

### Required Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| AWS_PROFILE | AWS CLI profile to use | `my-profile` |
| AWS_REGION | AWS region (or set in provider) | `us-east-1` |

### Prerequisites
- [ ] S3 bucket `<BUCKET_NAME>` must exist before first run
- [ ] DynamoDB table `<TABLE_NAME>` must exist for state locking
- [ ] IAM permissions for Terraform state management

### Production-Specific Protections
| Module | Protection | Description |
|--------|------------|-------------|
| prod/rds | `prevent_destroy = true` | Prevents accidental database deletion |
| prod/rds | `exclude { actions = ["destroy"] }` | Blocks destroy commands |
```

### 6. Next Steps (Optional)
Suggest what the user might want to do next (add more modules, customize configurations, etc.)

## Best Practices

Reference `../terragrunt-validator/references/best_practices.md` for comprehensive guidelines.

**Key principles:**
- Use `include` blocks to inherit root configuration (DRY)
- Always provide mock outputs for dependencies
- Enable state encryption (`encrypt = true`)
- Use `generate` blocks for provider configuration
- Specify bounded version constraints (`~> 5.0`, not `>= 5.0`) for local/Git modules
- Never hardcode credentials or secrets
- Configure retry logic for transient errors

> **Note on Version Constraints with Registry Modules:** When using Terraform Registry modules (e.g., `tfr:///terraform-aws-modules/vpc/aws?version=5.1.0`), they typically define their own `required_providers`. In this case, you may omit generating `required_providers` in `root.hcl` to avoid conflicts. The module's pinned version (`?version=X.X.X`) provides the version constraint. See "Common Issues → Provider Conflict with Registry Modules" for details.

**Anti-patterns to avoid:**
- Hardcoded account IDs, regions, or environment names
- Missing mock outputs for dependencies
- Duplicated configuration across modules
- Unencrypted state storage
- Missing or loose version constraints (except when using registry modules that define their own)
- Root.hcl trying to read env.hcl that doesn't exist at root level

## Deprecated Attributes

| Deprecated | Replacement | Reference |
|------------|-------------|-----------|
| `skip` | `exclude` block | [Docs](https://terragrunt.gruntwork.io/docs/reference/config-blocks-and-attributes/#exclude) |
| `retryable_errors` | `errors.retry` block | [Docs](https://terragrunt.gruntwork.io/docs/reference/config-blocks-and-attributes/#errors) |
| `run-all` | `run --all` | [Migration](https://terragrunt.gruntwork.io/docs/migrate/migrating-from-run-all/) |
| `--terragrunt-*` flags | Unprefixed flags | [CLI Reference](https://terragrunt.gruntwork.io/docs/reference/cli-options/) |
| `TERRAGRUNT_*` env vars | `TG_*` env vars | [CLI Reference](https://terragrunt.gruntwork.io/docs/reference/cli-options/) |

## Resources

### Templates - MUST Read Before Generating

| Configuration Type | Template File | Purpose | When to Read |
|-------------------|---------------|---------|--------------|
| Root configuration | `assets/templates/root/terragrunt.hcl` | Shared backend, provider, and common inputs | Before generating any root.hcl |
| Environment variables | `assets/templates/env/env.hcl` | Per-environment locals (environment, region, sizing, feature toggles) | Before generating any env.hcl (Pattern A) |
| Child module | `assets/templates/child/terragrunt.hcl` | Module include, source, and optional dependency scaffolding | Before generating any child module |
| Standalone module | `assets/templates/module/terragrunt.hcl` | Module config without root inheritance | Before generating standalone modules |
| Stack file | `assets/templates/stack/terragrunt.stack.hcl` | Stack blueprint and unit generation | Before generating stacks |
| Catalog unit | `assets/templates/catalog/terragrunt.hcl` | Reusable unit consumed by stack definitions | Before generating catalog units |

### References

| Reference | Content | Purpose | When to Read |
|-----------|---------|---------|--------------|
| `references/common-patterns.md` | All generation patterns with examples | Pick a compatible pattern before writing files | Always, before generating |
| `../terragrunt-validator/references/best_practices.md` | Comprehensive best practices | Final quality and safety checks | Always, before generating |

### Official Documentation
- [Terragrunt Docs](https://terragrunt.gruntwork.io/docs/)
- [Configuration Reference](https://terragrunt.gruntwork.io/docs/reference/config-blocks-and-attributes/)
- [CLI Reference](https://terragrunt.gruntwork.io/docs/reference/cli-options/)
- [Stacks](https://terragrunt.gruntwork.io/docs/features/stacks/)
- [Feature Flags](https://terragrunt.gruntwork.io/docs/features/feature-flags/)
- [Engine](https://terragrunt.gruntwork.io/docs/features/engine/)
- [Migration Guides](https://terragrunt.gruntwork.io/docs/migrate/)

## Common Issues

### Root.hcl Cannot Find env.hcl

**Symptom:**
```
Error: Attempt to get attribute from null value
  on ./root.hcl line X:
  This value is null, so it does not have any attributes.
```

**Cause:** Root.hcl is trying to read `env.hcl` via `find_in_parent_folders("env.hcl")`, but env.hcl doesn't exist at the root level.

**Solution:** Make root.hcl environment-agnostic:
```hcl
# DON'T do this in root.hcl for multi-environment setups:
locals {
  env_vars = read_terragrunt_config(find_in_parent_folders("env.hcl"))  # FAILS
}

# DO use static values or get_env():
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "us-east-1"  # Static value, or use get_env("AWS_REGION", "us-east-1")
}
EOF
}
```

### Provider Conflict with Registry Modules

When using Terraform Registry modules (e.g., `tfr:///terraform-aws-modules/vpc/aws`), they may define their own `required_providers` block. This can conflict with provider configuration generated by `root.hcl`.

**Symptoms:**
```
Error: Duplicate required providers configuration
```

**Solutions:**
1. **Remove conflicting generate block** - If using registry modules that manage their own providers, avoid generating duplicate `required_providers`:
   ```hcl
   # In root.hcl - only generate provider config, not required_providers
   generate "provider" {
     path      = "provider.tf"
     if_exists = "overwrite_terragrunt"
     contents  = <<EOF
   provider "aws" {
     region = "us-east-1"
   }
   EOF
   }
   ```

2. **Use if_exists = "skip"** - Skip generation if file already exists:
   ```hcl
   generate "versions" {
     path      = "versions.tf"
     if_exists = "skip"  # Don't overwrite module's versions.tf
     contents  = "..."
   }
   ```

3. **Clear cache** - If conflicts persist after fixes:
   ```bash
   rm -rf .terragrunt-cache
   terragrunt init
   ```

### Feature Flag Validation Errors

If you see `Unknown variable; There is no variable named "local"` in feature blocks, ensure defaults are static values (see Feature Flags section above).

### Child Module Cannot Find env.hcl

**Symptom:**
```
Error: Attempt to get attribute from null value
  on ./dev/vpc/terragrunt.hcl line X:
```

**Cause:** Child module's `find_in_parent_folders("env.hcl")` cannot find env.hcl.

**Solution:** Ensure env.hcl exists in the environment directory:
```
dev/
├── env.hcl           # This file MUST exist
└── vpc/
    └── terragrunt.hcl  # Calls find_in_parent_folders("env.hcl")
```

## Quick Reference Card

### File Reading Checklist

Before generating, READ these files in order:

1. [ ] `references/common-patterns.md` - Understand available patterns
2. [ ] `../terragrunt-validator/references/best_practices.md` - Know the rules
3. [ ] Relevant template(s) from `assets/templates/` - Structural reference

### Architecture Decision Tree

```
Q: Multiple environments (dev/staging/prod)?
├─ YES → Q: Shared root configuration?
│   ├─ YES → Pattern A: Environment-Agnostic Root
│   └─ NO  → Separate root.hcl per environment
└─ NO  → Q: Environment detection needed?
    ├─ YES → Pattern B: Environment-Aware Root
    └─ NO  → Pattern B: Simple single-environment
```

### Validation Sequence

1. Format check: `terragrunt hcl fmt --check`
2. Input validation: `terragrunt hcl validate --inputs`
3. Full validation: Invoke `Skill(devops-skills:terragrunt-validator)`
4. Fix errors → Re-validate → Repeat until clean

## Done Criteria

This skill execution is complete only when ALL are true:

- One architecture checklist is completed and shown (the canonical checklist in this file)
- Generated files consistently use modern root include syntax unless legacy was explicitly requested
- Registry sources use canonical `tfr:///NAMESPACE/NAME/PROVIDER?version=X.Y.Z` format
- Dependency blocks are added only where actually needed (not left as unresolved placeholders)
- All placeholders are replaced and secrets checks are reported in output
- Validation succeeded, or fallback checks ran with explicit limitations documented

---

## Reference: Common Patterns

# Terragrunt Common Generation Patterns

## Overview

This reference provides common patterns and code examples for generating Terragrunt configurations. Use these patterns as building blocks when creating new Terragrunt resources.

> **Include syntax standard:** Use `find_in_parent_folders("root.hcl")` for new projects. Only use `find_in_parent_folders()` when the repository intentionally keeps a legacy root file named `terragrunt.hcl`.

## Root Configuration Patterns

### Pattern 1: Basic Root with S3 Backend

**Use when:** Starting a new Terragrunt project with AWS S3 backend

```hcl
# root.hcl (modern root file name)
remote_state {
  backend = "s3"
  config = {
    bucket         = "company-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = var.region
}
EOF
}

inputs = {
  region = "us-east-1"
  common_tags = {
    ManagedBy = "Terragrunt"
  }
}
```

### Pattern 2: Multi-Account Root Configuration

**Use when:** Managing multiple AWS accounts with role assumption

```hcl
# root.hcl (modern root file name)
locals {
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  region_vars  = read_terragrunt_config(find_in_parent_folders("region.hcl"))
  env_vars     = read_terragrunt_config(find_in_parent_folders("env.hcl"))

  account_id  = local.account_vars.locals.account_id
  region      = local.region_vars.locals.region
  environment = local.env_vars.locals.environment
}

remote_state {
  backend = "s3"
  config = {
    bucket         = "terraform-state-${local.account_id}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = local.region
    encrypt        = true
    dynamodb_table = "terraform-locks-${local.environment}"

    role_arn = "arn:aws:iam::${local.account_id}:role/TerraformRole"
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "aws" {
  region = "${local.region}"

  assume_role {
    role_arn = "arn:aws:iam::${local.account_id}:role/TerraformRole"
  }

  default_tags {
    tags = {
      Environment = "${local.environment}"
      ManagedBy   = "Terragrunt"
    }
  }
}
EOF
}

inputs = {
  account_id  = local.account_id
  region      = local.region
  environment = local.environment
}
```

### Pattern 3: Multi-Cloud Root Configuration

**Use when:** Managing resources across multiple cloud providers

```hcl
# root.hcl (modern root file name)
generate "providers" {
  path      = "providers.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}
EOF
}
```

## Child Module Patterns

### Pattern 1: Simple Module with No Dependencies

**Use when:** Creating standalone infrastructure component

```hcl
# modules/vpc/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws?version=5.1.0"
}

inputs = {
  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false

  tags = {
    Name = "my-vpc"
  }
}
```

### Pattern 2: Module with Single Dependency

**Use when:** Creating a resource that depends on another module's outputs

```hcl
# modules/rds/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "tfr:///terraform-aws-modules/rds/aws?version=6.1.0"
}

dependency "vpc" {
  config_path = "../vpc"

  mock_outputs = {
    vpc_id             = "vpc-mock123"
    database_subnet_ids = ["subnet-mock1", "subnet-mock2"]
  }

  mock_outputs_allowed_terraform_commands = ["validate", "plan", "destroy"]
}

dependency "security_group" {
  config_path = "../security-groups/database"

  mock_outputs = {
    security_group_id = "sg-mock123"
  }

  mock_outputs_allowed_terraform_commands = ["validate", "plan", "destroy"]
}

inputs = {
  identifier = "mydb"
  engine     = "postgres"

  vpc_security_group_ids = [dependency.security_group.outputs.security_group_id]
  db_subnet_group_name   = dependency.vpc.outputs.database_subnet_group_name

  allocated_storage = 20
  instance_class    = "db.t3.micro"
}
```

### Pattern 3: Module with Multiple Dependencies

**Use when:** Creating complex infrastructure with multiple upstream dependencies

```hcl
# modules/eks/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "tfr:///terraform-aws-modules/eks/aws?version=19.15.0"
}

dependencies {
  paths = ["../vpc", "../security-groups", "../iam-roles"]
}

dependency "vpc" {
  config_path = "../vpc"

  mock_outputs = {
    vpc_id             = "vpc-mock"
    private_subnet_ids = ["subnet-1", "subnet-2"]
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

dependency "security_groups" {
  config_path = "../security-groups"

  mock_outputs = {
    cluster_security_group_id = "sg-mock"
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

dependency "iam" {
  config_path = "../iam-roles"

  mock_outputs = {
    cluster_role_arn = "arn:aws:iam::123456789012:role/mock-role"
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

inputs = {
  cluster_name    = "my-eks-cluster"
  cluster_version = "1.28"

  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.private_subnet_ids

  cluster_security_group_id = dependency.security_groups.outputs.cluster_security_group_id
  iam_role_arn              = dependency.iam.outputs.cluster_role_arn

  enable_irsa = true
}
```

### Pattern 4: Module with Conditional Logic

**Use when:** Generating configurations with environment-specific variations

```hcl
# modules/app/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  env = get_env("ENVIRONMENT", "dev")

  instance_counts = {
    dev  = 1
    staging = 2
    prod = 3
  }

  instance_types = {
    dev  = "t3.micro"
    staging = "t3.small"
    prod = "t3.medium"
  }
}

terraform {
  source = "../../terraform-modules/app"
}

inputs = {
  environment    = local.env
  instance_count = local.instance_counts[local.env]
  instance_type  = local.instance_types[local.env]

  enable_monitoring = local.env == "prod" ? true : false
  enable_backups    = local.env == "prod" ? true : false

  tags = merge(
    {
      Environment = local.env
      ManagedBy   = "Terragrunt"
    },
    local.env == "prod" ? { CriticalResource = "true" } : {}
  )
}
```

## Environment-Specific Patterns

### Pattern 1: Environment Configuration Files

**Use when:** Managing multiple environments with shared structure

```
infrastructure/
├── root.hcl                 # Root config (modern)
├── _env/
│   ├── prod.hcl            # Production variables
│   ├── staging.hcl         # Staging variables
│   └── dev.hcl             # Development variables
├── prod/
│   ├── env.hcl -> ../_env/prod.hcl
│   └── vpc/
│       └── terragrunt.hcl
└── staging/
    ├── env.hcl -> ../_env/staging.hcl
    └── vpc/
        └── terragrunt.hcl
```

**_env/prod.hcl:**
```hcl
locals {
  environment = "prod"
  region      = "us-east-1"

  vpc_cidr = "10.0.0.0/16"

  instance_type = "t3.medium"
  min_size      = 3
  max_size      = 10
}
```

**prod/vpc/terragrunt.hcl:**
```hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  env = read_terragrunt_config(find_in_parent_folders("env.hcl"))
}

terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws?version=5.1.0"
}

inputs = {
  name = "${local.env.locals.environment}-vpc"
  cidr = local.env.locals.vpc_cidr

  azs = ["${local.env.locals.region}a", "${local.env.locals.region}b"]
}
```

## Advanced Patterns

### Pattern 1: Dynamic Provider Configuration

**Use when:** Provider configuration varies by module or environment

```hcl
# modules/cross-account-resource/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  target_account_id = "987654321098"
}

generate "provider_override" {
  path      = "provider_override.tf"
  if_exists = "overwrite"
  contents  = <<EOF
provider "aws" {
  alias  = "target_account"
  region = var.region

  assume_role {
    role_arn = "arn:aws:iam::${local.target_account_id}:role/CrossAccountRole"
  }
}
EOF
}

terraform {
  source = "../../terraform-modules/cross-account-resource"
}
```

### Pattern 2: Module Composition

**Use when:** Combining multiple modules in a single configuration

```hcl
# modules/application-stack/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "../../terraform-modules/application-stack"
}

dependency "vpc" {
  config_path = "../networking/vpc"
  mock_outputs = {
    vpc_id     = "vpc-mock"
    subnet_ids = ["subnet-1", "subnet-2"]
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

dependency "database" {
  config_path = "../data/rds"
  mock_outputs = {
    endpoint = "mock.endpoint.rds.amazonaws.com"
    port     = 5432
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

dependency "cache" {
  config_path = "../data/elasticache"
  mock_outputs = {
    endpoint = "mock.cache.amazonaws.com"
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

inputs = {
  name = "my-application"

  # Networking
  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.private_subnet_ids

  # Database
  database_endpoint = dependency.database.outputs.endpoint
  database_port     = dependency.database.outputs.port

  # Cache
  cache_endpoint = dependency.cache.outputs.endpoint

  # Application configuration
  image_tag      = "latest"
  desired_count  = 2
  cpu            = 256
  memory         = 512
}
```

### Pattern 3: Hooks for Pre/Post Operations

**Use when:** Need to run commands before or after Terraform operations

```hcl
# modules/database/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "tfr:///terraform-aws-modules/rds/aws?version=6.1.0"

  before_hook "backup_check" {
    commands = ["apply"]
    execute  = ["bash", "-c", "echo 'Starting database deployment...'"]
  }

  after_hook "notify_deployment" {
    commands     = ["apply"]
    execute      = ["bash", "-c", "curl -X POST https://slack.webhook.url -d '{\"text\":\"Database deployed\"}'"]
    run_on_error = false
  }

  error_hook "notify_error" {
    commands = ["apply", "plan"]
    execute  = ["bash", "-c", "echo 'Error occurred during Terraform operation'"]
  }
}
```

### Pattern 4: External Data Integration

**Use when:** Need to fetch dynamic values from external sources

```hcl
# modules/app/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

locals {
  # Fetch current git branch (--quiet suppresses Terragrunt banner output)
  git_branch = run_cmd("--quiet", "git", "rev-parse", "--abbrev-ref", "HEAD")

  # Fetch AWS account ID
  account_id = run_cmd("--quiet", "aws", "sts", "get-caller-identity", "--query", "Account", "--output", "text")

  # Read JSON configuration
  config = jsondecode(file("${get_terragrunt_dir()}/config.json"))
}

terraform {
  source = "../../terraform-modules/app"
}

inputs = {
  git_branch = local.git_branch
  account_id = local.account_id

  app_config = local.config

  name = "${local.config.app_name}-${local.git_branch}"
}
```

## Custom Provider Patterns

### Pattern 1: Kubernetes Provider with EKS

**Use when:** Managing Kubernetes resources with Terragrunt

```hcl
# modules/k8s-app/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

dependency "eks" {
  config_path = "../eks-cluster"

  mock_outputs = {
    cluster_endpoint          = "https://mock-endpoint"
    cluster_certificate       = "mock-cert"
    cluster_name              = "mock-cluster"
  }
  mock_outputs_allowed_terraform_commands = ["validate", "plan"]
}

generate "kubernetes_provider" {
  path      = "kubernetes_provider.tf"
  if_exists = "overwrite"
  contents  = <<EOF
provider "kubernetes" {
  host                   = "${dependency.eks.outputs.cluster_endpoint}"
  cluster_ca_certificate = base64decode("${dependency.eks.outputs.cluster_certificate}")

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args = [
      "eks",
      "get-token",
      "--cluster-name",
      "${dependency.eks.outputs.cluster_name}"
    ]
  }
}

provider "helm" {
  kubernetes {
    host                   = "${dependency.eks.outputs.cluster_endpoint}"
    cluster_ca_certificate = base64decode("${dependency.eks.outputs.cluster_certificate}")

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args = [
        "eks",
        "get-token",
        "--cluster-name",
        "${dependency.eks.outputs.cluster_name}"
      ]
    }
  }
}
EOF
}

terraform {
  source = "../../terraform-modules/k8s-app"
}
```

### Pattern 2: Multiple Provider Versions

**Use when:** Different modules require different provider versions

```hcl
# modules/legacy-resource/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

generate "provider_version_override" {
  path      = "versions.tf"
  if_exists = "overwrite"
  contents  = <<EOF
terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"  # Legacy version for compatibility
    }
  }
}
EOF
}

terraform {
  source = "../../terraform-modules/legacy-resource"
}
```

## Stacks Patterns (2025)

Terragrunt Stacks allow you to define infrastructure blueprints that generate unit configurations programmatically. GA since v0.78.0 (May 2025).

### Pattern 1: Basic Stack with Units

**Use when:** Creating a reusable infrastructure blueprint

Catalog units expect `values.name` as the base resource identifier from each stack unit.

```hcl
# terragrunt.stack.hcl
locals {
  environment = "prod"
  aws_region  = "us-east-1"
  units_path  = find_in_parent_folders("catalog/units")

  # Keep this mode consistent across dependent units.
  # Do not mix .terragrunt-stack generation with direct path generation.
  use_direct_paths = true
}

unit "vpc" {
  source = "${local.units_path}/vpc"
  path   = "vpc"
  no_dot_terragrunt_stack = local.use_direct_paths
  values = {
    name        = "${local.environment}-vpc"
    cidr        = "10.0.0.0/16"
    environment = local.environment
  }
}

unit "database" {
  source = "${local.units_path}/database"
  path   = "database"
  no_dot_terragrunt_stack = local.use_direct_paths
  values = {
    name        = "${local.environment}-db"
    engine      = "postgres"
    vpc_path    = "../vpc"
    environment = local.environment
  }
}
```

### Pattern 2: Stack with Git-Based Unit Sources

**Use when:** Using versioned unit definitions from a remote repository

```hcl
# terragrunt.stack.hcl
unit "vpc" {
  source = "git::git@github.com:acme/infrastructure-catalog.git//units/vpc?ref=v1.0.0"
  path   = "vpc"
  values = {
    name = "main"
    cidr = "10.0.0.0/16"
  }
}

unit "database" {
  source = "git::git@github.com:acme/infrastructure-catalog.git//units/database?ref=v1.0.0"
  path   = "database"
  values = {
    name     = "main-db"
    engine   = "postgres"
    version  = "15"
    vpc_path = "../vpc"
  }
}
```

### Pattern 3: Catalog Unit with Values

**Use when:** Creating reusable unit templates for stacks

The `name` key is the standard generic resource name key passed from the stack's unit
`values` block. Unit-specific keys (e.g., `cidr`, `engine`) are passed alongside it.

```hcl
# catalog/units/vpc/terragrunt.hcl
include "root" {
  path = find_in_parent_folders("root.hcl")
}

terraform {
  source = "tfr:///terraform-aws-modules/vpc/aws?version=5.1.0"
}

inputs = {
  # `values.name` is the standard generic resource name key set in the stack definition.
  name = values.name
  cidr = values.cidr

  azs             = ["${values.aws_region}a", "${values.aws_region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = try(values.enable_nat, true)

  tags = {
    Environment = values.environment
    ManagedBy   = "Terragrunt"
  }
}
```

### Pattern 4: Stack Commands

```bash
# Generate unit configurations from stack
terragrunt stack generate

# Plan all units in the stack
terragrunt stack run plan

# Apply all units in the stack
terragrunt stack run apply

# Get aggregated outputs from all units
terragrunt stack output

# Clean generated directories
terragrunt stack clean
```

## Feature Flags Patterns (2025)

Feature flags provide runtime control over Terragrunt behavior.

### Pattern 1: Basic Feature Flag

**Use when:** Enabling/disabling features at runtime

```hcl
# terragrunt.hcl
feature "enable_monitoring" {
  default = false
}

inputs = {
  enable_monitoring = feature.enable_monitoring.value
}
```

**Usage:**
```bash
# Override via CLI
terragrunt apply --feature enable_monitoring=true

# Override via environment variable
export TG_FEATURE="enable_monitoring=true"
terragrunt apply
```

### Pattern 2: Feature Flag for Module Versioning

**Use when:** Controlling module versions at runtime

```hcl
# terragrunt.hcl
feature "module_version" {
  default = "v1.0.0"
}

terraform {
  source = "git::git@github.com:acme/modules.git//vpc?ref=${feature.module_version.value}"
}
```

### Pattern 3: Feature Flag with Conditional Logic

**Use when:** Complex conditional behavior based on flags

```hcl
# terragrunt.hcl
feature "enable_ha" {
  default = false
}

locals {
  instance_count = feature.enable_ha.value ? 3 : 1
  instance_type  = feature.enable_ha.value ? "t3.medium" : "t3.micro"
}

inputs = {
  instance_count = local.instance_count
  instance_type  = local.instance_type
}
```

### Pattern 4: Environment-Based Feature Flags

**Use when:** Controlling deployments per environment

```hcl
# prod/root.hcl
feature "prod" {
  default = false
}

exclude {
  if      = !feature.prod.value
  actions = ["all_except_output"]
}
```

**Usage:**
```bash
# Enable production deployment
terragrunt run --all apply --feature prod=true
```

## Exclude Block Patterns (2025)

The `exclude` block replaces the deprecated `skip` attribute with more fine-grained control.

### Pattern 1: Basic Exclusion

**Use when:** Excluding a unit from all operations

```hcl
# terragrunt.hcl
exclude {
  if                   = true
  actions              = ["all"]
  exclude_dependencies = false
}
```

### Pattern 2: Exclude Specific Actions

**Use when:** Excluding only certain operations

```hcl
# terragrunt.hcl
exclude {
  if      = true
  actions = ["apply", "destroy"]  # Still allows plan and output
}
```

### Pattern 3: Conditional Exclusion with Feature Flags

**Use when:** Dynamic exclusion based on runtime flags

```hcl
# terragrunt.hcl
feature "skip_in_dev" {
  default = false
}

exclude {
  if      = feature.skip_in_dev.value
  actions = ["apply", "destroy"]
  exclude_dependencies = false
}
```

### Pattern 4: Time-Based Exclusion

**Use when:** Preventing deployments during certain periods

```hcl
# terragrunt.hcl
locals {
  day_of_week = formatdate("EEE", timestamp())
  is_weekend  = contains(["Fri", "Sat", "Sun"], local.day_of_week)
}

exclude {
  if      = local.is_weekend
  actions = ["apply", "destroy"]
}
```

### Pattern 5: All Except Output

**Use when:** Allowing only output retrieval

```hcl
# terragrunt.hcl
exclude {
  if      = true
  actions = ["all_except_output"]
}
```

## Errors Block Patterns (2025)

The `errors` block replaces deprecated `retryable_errors`, `retry_max_attempts`, and `retry_sleep_interval_sec`.

### Pattern 1: Basic Retry Configuration

**Use when:** Handling transient errors with retries

```hcl
# terragrunt.hcl
errors {
  retry "transient_errors" {
    retryable_errors = [
      "(?s).*Failed to load state.*tcp.*timeout.*",
      "(?s).*Error installing provider.*TLS handshake timeout.*",
      "(?s).*429 Too Many Requests.*",
    ]
    max_attempts       = 3
    sleep_interval_sec = 5
  }
}
```

### Pattern 2: Ignore Safe Errors

**Use when:** Ignoring known safe-to-ignore errors

```hcl
# terragrunt.hcl
errors {
  ignore "known_warnings" {
    ignorable_errors = [
      ".*Warning: Resource already exists.*",
      "!.*Error: critical.*"  # Negation: don't ignore critical errors
    ]
    message = "Ignoring known safe warnings"
    signals = {
      alert_team = false
    }
  }
}
```

### Pattern 3: Combined Retry and Ignore

**Use when:** Comprehensive error handling

```hcl
# terragrunt.hcl
errors {
  retry "network_errors" {
    retryable_errors = [
      "(?s).*connection reset by peer.*",
      "(?s).*timeout.*",
    ]
    max_attempts       = 3
    sleep_interval_sec = 10
  }

  ignore "deprecation_warnings" {
    ignorable_errors = [
      ".*Deprecation Warning.*",
    ]
    message = "Ignoring deprecation warnings"
  }
}
```

### Pattern 4: Feature Flag Controlled Error Handling

**Use when:** Dynamic error handling based on flags

```hcl
# terragrunt.hcl
feature "enable_flaky_module" {
  default = false
}

errors {
  ignore "flaky_module_errors" {
    ignorable_errors = feature.enable_flaky_module.value ? [
      ".*Error: flaky module error.*"
    ] : []
    message = "Ignoring flaky module error"
    signals = {
      send_notification = true
    }
  }
}
```

## OpenTofu Engine Patterns (2025)

Configure Terragrunt to use OpenTofu as the IaC engine.

### Pattern 1: GitHub-Based Engine

**Use when:** Using the official OpenTofu engine

```hcl
# terragrunt.hcl
engine {
  source  = "github.com/gruntwork-io/terragrunt-engine-opentofu"
  version = "v0.0.15"
}
```

### Pattern 2: Auto-Install OpenTofu Version

**Use when:** Automatically installing a specific OpenTofu version

```hcl
# terragrunt.hcl
engine {
  source = "github.com/gruntwork-io/terragrunt-engine-opentofu"
  meta = {
    tofu_version     = "v1.9.1"      # Or "latest" for stable version
    tofu_install_dir = "/opt/tofu"   # Optional custom install directory
  }
}
```

### Pattern 3: Local Engine Binary

**Use when:** Using a locally built or installed engine

```hcl
# terragrunt.hcl
engine {
  source = "/usr/local/bin/terragrunt-iac-engine-opentofu"
}
```

### Pattern 4: HTTPS Engine Source

**Use when:** Downloading engine from a specific URL

```hcl
# terragrunt.hcl
engine {
  source = "https://github.com/gruntwork-io/terragrunt-engine-opentofu/releases/download/v0.0.15/terragrunt-iac-engine-opentofu_rpc_v0.0.15_linux_amd64.zip"
}
```

## Provider Cache Patterns (2025)

Optimize provider downloads with caching.

### Pattern 1: Enable Provider Cache Server

**Use when:** Running multiple terragrunt operations

```bash
# Enable provider cache for run --all operations
terragrunt run --all plan --provider-cache

# Via environment variable
TG_PROVIDER_CACHE=1 terragrunt run --all apply
```

### Pattern 2: Custom Cache Directory

**Use when:** Specifying a custom cache location

```bash
TG_PROVIDER_CACHE=1 \
TG_PROVIDER_CACHE_DIR=/custom/cache/path \
terragrunt plan
```

### Pattern 3: Auto Provider Cache (OpenTofu 1.10+)

**Use when:** Using OpenTofu's native provider caching

```bash
# Enable auto-provider-cache-dir experiment
terragrunt run --all apply --experiment auto-provider-cache-dir

# Via environment variable
TG_EXPERIMENT='auto-provider-cache-dir' terragrunt run --all apply
```

### Pattern 4: Remote Cache Server

**Use when:** Sharing cache across team/CI

```bash
TG_PROVIDER_CACHE=1 \
TG_PROVIDER_CACHE_HOST=192.168.0.100 \
TG_PROVIDER_CACHE_PORT=5758 \
TG_PROVIDER_CACHE_TOKEN=my-secret \
terragrunt apply
```

## Summary

These patterns cover the most common Terragrunt generation scenarios:

1. **Root configurations** - Project setup with state management
2. **Child modules** - Resource creation with dependency management
3. **Environment handling** - Multi-environment infrastructure
4. **Advanced patterns** - Complex scenarios and integrations
5. **Stacks** - Infrastructure blueprints for maximum reusability (2025)
6. **Feature Flags** - Runtime control over behavior (2025)
7. **Exclude blocks** - Fine-grained execution control (2025)
8. **Errors blocks** - Advanced error handling (2025)
9. **OpenTofu engine** - Alternative IaC engine support (2025)
10. **Provider cache** - Performance optimization (2025)

When generating Terragrunt configurations, select the appropriate pattern based on:
- Project structure (single vs multi-account/environment)
- Module dependencies (none, single, multiple)
- Provider requirements (single vs multi-cloud)
- Operational needs (hooks, external data, etc.)
- Reusability requirements (stacks vs traditional modules)
- Runtime control needs (feature flags, exclusions)

Always validate generated configurations using the terragrunt-validator or terraform-validator skills.
