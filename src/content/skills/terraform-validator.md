---
title: "Terraform 验证器"
description: "验证和审查 Terraform 配置的安全性、合规性和最佳实践"
category: "devops"
source: "community"
author: "Community"
tags: ["terraform", "validator"]
date: 2026-03-20
---

# Terraform Validator

Comprehensive toolkit for validating, linting, and testing Terraform configurations with automated workflows for syntax validation, security scanning, and intelligent documentation lookup.

## ⚠️ Critical Requirements Checklist

**STOP: You MUST complete these steps in order. Do NOT skip any REQUIRED step.**

| Step | Action | Required |
|------|--------|----------|
| 1 | Run `bash scripts/extract_tf_info_wrapper.sh <path>` | ✅ REQUIRED |
| 2 | Context7 lookup for **ALL** providers (explicit AND implicit); **WebSearch fallback if not found** | ✅ REQUIRED |
| 3 | **READ** `references/security_checklist.md` | ✅ REQUIRED |
| 4 | **READ** `references/best_practices.md` | ✅ REQUIRED |
| 5 | Run `terraform fmt` | ✅ REQUIRED |
| 6 | Run `tflint` (or note as skipped if unavailable) | Recommended |
| 7 | Run `terraform init` (if not initialized) | ✅ REQUIRED |
| 8 | Run `terraform validate` | ✅ REQUIRED |
| 9 | Run `bash scripts/run_checkov.sh <path>` | ✅ REQUIRED |
| 10 | Cross-reference findings with `security_checklist.md` sections | ✅ REQUIRED |
| 11 | Generate report citing reference files | ✅ REQUIRED |
| 12 | Run regression tests (`bash tests/test_regression.sh`) | ✅ REQUIRED |
| 13 | Run lightweight CI checks (`bash -n`, `py_compile`, smoke) | ✅ REQUIRED |

> **IMPORTANT:** Steps 3-4 (reading reference files) must be completed BEFORE running security scans. The reference files contain remediation patterns that MUST be cited in your report.

> **Context7 Fallback:** If Context7 does not have a provider (common for: random, null, local, time, tls), use WebSearch: `"terraform-provider-{name} hashicorp documentation"`

## When to Use This Skill

- Working with Terraform files (`.tf`, `.tfvars`, `.tfstate`)
- Validating Terraform configuration syntax and structure
- Linting and formatting HCL code
- Performing dry-run testing with `terraform plan`
- Debugging Terraform errors or misconfigurations
- Understanding custom Terraform providers or modules
- Security validation of Terraform configurations

## External Documentation

| Tool | Documentation |
|------|---------------|
| **Terraform** | [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform/docs) |
| **TFLint** | [github.com/terraform-linters/tflint](https://github.com/terraform-linters/tflint) |
| **Checkov** | [checkov.io](https://www.checkov.io/1.Welcome/Quick%20Start.html) |
| **Trivy** | [aquasecurity.github.io/trivy](https://aquasecurity.github.io/trivy) |

## Validation Workflow

**IMPORTANT:** Follow this workflow in order. Each step is REQUIRED unless explicitly marked optional.

```
1. Identify Terraform files in scope
   ├─> Single file, directory, or multi-environment

2. Extract Provider/Module Info (REQUIRED)
   ├─> MUST run: bash scripts/extract_tf_info_wrapper.sh <path>
   ├─> Parse output for providers and modules
   └─> Use for Context7 documentation lookup

3. Lookup Provider Documentation (REQUIRED)
   ├─> For EACH provider detected:
   │   ├─> mcp__context7__resolve-library-id with "terraform-provider-{name}"
   │   ├─> mcp__context7__query-docs for version-specific guidance
   │   └─> If NOT found in Context7: WebSearch fallback (see below)
   └─> Note any custom/private providers for WebSearch

4. Read Reference Files (REQUIRED before validation)
   ├─> MUST READ: references/security_checklist.md (before security scan)
   ├─> MUST READ: references/best_practices.md (for structure validation)
   └─> Reference common_errors.md if errors occur

5. Format and Lint (REQUIRED)
   ├─> MUST run: terraform fmt -recursive (auto-fix formatting)
   ├─> MUST run: terraform fmt -check -recursive (verify no drift)
   ├─> RUN: tflint (or note as skipped if unavailable)
   └─> Report formatting issues

6. Syntax Validation (REQUIRED)
   ├─> MUST run: terraform init (if not initialized)
   ├─> MUST run: terraform validate
   └─> Report syntax errors (consult common_errors.md)

7. Security Scanning (REQUIRED)
   ├─> MUST run: bash scripts/run_checkov.sh <path>
   ├─> Analyze policy violations against security_checklist.md
   └─> Suggest remediations from reference

8. Dry-Run Testing (if credentials available)
   ├─> terraform plan
   ├─> Analyze planned changes
   └─> Report potential issues

9. Regression and Wrapper Determinism Checks (REQUIRED)
   ├─> MUST run: bash tests/test_regression.sh
   ├─> Confirms parser error handling returns non-zero
   ├─> Confirms implicit provider detection for docs lookup
   ├─> Confirms wrapper argument handling is deterministic
   └─> Confirms checkov wrapper preserves scanner exit code

10. Lightweight CI Checks (REQUIRED)
   ├─> MUST run: bash -n scripts/*.sh
   ├─> MUST run: python3 -m py_compile scripts/*.py
   ├─> MUST run: smoke check for extract wrapper on sample fixture
   └─> Record command outputs and exit codes

11. Generate Comprehensive Report
   ├─> Include all findings with severity
   ├─> Reference best_practices.md for recommendations
   └─> Offer to fix issues if appropriate
```

## Required Reference File Reading

**You MUST read these reference files during validation:**

| When | Reference File | Action |
|------|----------------|--------|
| **Before security scan** | `references/security_checklist.md` | Read to understand security checks and remediation patterns |
| **During validation** | `references/best_practices.md` | Read to validate project structure, naming, and patterns |
| **If errors occur** | `references/common_errors.md` | Read to find solutions for specific error messages |
| **If using Terraform 1.10+** | `references/advanced_features.md` | Read to understand ephemeral values, actions, list resources |

## Required Script Usage

**You MUST use these wrapper scripts instead of calling tools directly:**

| Task | Script | Command |
|------|--------|---------|
| **Extract provider/module info** | `extract_tf_info_wrapper.sh` | `bash scripts/extract_tf_info_wrapper.sh <path>` |
| **Run security scan** | `run_checkov.sh` | `bash scripts/run_checkov.sh <path>` |
| **Install checkov (if missing)** | `install_checkov.sh` | `bash scripts/install_checkov.sh install` |

> **Note:** `extract_tf_info_wrapper.sh` automatically handles the python-hcl2 dependency. If system Python lacks `python-hcl2`, it creates/reuses a cached virtual environment under `~/.cache/terraform-validator/` by default.

### Script Run Context (REQUIRED)

- Default working directory: `devops-skills-plugin/skills/terraform-validator`
- If running from elsewhere, use absolute script paths:
  - `bash /absolute/path/to/terraform-validator/scripts/extract_tf_info_wrapper.sh <path>`
  - `bash /absolute/path/to/terraform-validator/scripts/run_checkov.sh <path>`
  - `bash /absolute/path/to/terraform-validator/scripts/install_checkov.sh install`

## Context7 Provider Documentation Lookup (REQUIRED)

**For EVERY provider detected, you MUST lookup documentation via Context7:**

```
1. Run extract_tf_info_wrapper.sh to get provider list
2. For each provider (e.g., "aws", "google", "azurerm"):
   a. Call: mcp__context7__resolve-library-id with "terraform-provider-{name}"
   b. Call: mcp__context7__query-docs with the resolved ID
   c. Note version-specific features and constraints
3. Include relevant provider guidance in validation report
```

**Example for AWS provider:**
```
mcp__context7__resolve-library-id("terraform-provider-aws")
mcp__context7__query-docs(context7CompatibleLibraryID, "best practices")
```

### Context7 Fallback to WebSearch (REQUIRED)

**If Context7 does not find a provider, you MUST fall back to WebSearch:**

```
1. If mcp__context7__resolve-library-id returns no results or provider not found:
   a. Use WebSearch with query: "terraform-provider-{name} hashicorp documentation"
   b. For specific version: "terraform-provider-{name} {version} documentation site:registry.terraform.io"
2. Common providers NOT in Context7 (use WebSearch directly):
   - random (hashicorp/random)
   - null (hashicorp/null)
   - local (hashicorp/local)
   - time (hashicorp/time)
   - tls (hashicorp/tls)
3. Document in report: "Provider docs via WebSearch (not in Context7)"
```

**WebSearch Fallback Example:**
```
# If Context7 fails for random provider:
WebSearch("terraform-provider-random hashicorp documentation site:registry.terraform.io")
```

> **Note:** HashiCorp utility providers (random, null, local, time, tls, archive, external, http) may not be indexed in Context7. Always fall back to WebSearch for these.

## Detecting Implicit Providers (REQUIRED)

**IMPORTANT:** Providers can be used without being declared in `required_providers`. You MUST detect ALL providers:

### Detection Methods

1. **Explicit Providers:** Listed in `required_providers` block (from extract_tf_info_wrapper.sh output)
2. **Implicit Providers:** Inferred from resource type prefixes

### Common Implicit Provider Patterns

| Resource Type Prefix | Provider Name | Context7 Lookup |
|---------------------|---------------|-----------------|
| `random_*` | `random` | `terraform-provider-random` |
| `null_*` | `null` | `terraform-provider-null` |
| `local_*` | `local` | `terraform-provider-local` |
| `tls_*` | `tls` | `terraform-provider-tls` |
| `time_*` | `time` | `terraform-provider-time` |
| `archive_*` | `archive` | `terraform-provider-archive` |
| `http` (data source) | `http` | `terraform-provider-http` |
| `external` (data source) | `external` | `terraform-provider-external` |

### Workflow for Complete Provider Detection

```
1. Parse extract_tf_info_wrapper.sh output
2. Get providers from "providers" array (explicit)
3. Get resources from "resources" array
4. For EACH resource type:
   a. Extract prefix (e.g., "random" from "random_id")
   b. Check if already in providers list
   c. If NOT in providers: add as implicit provider
5. Perform Context7 lookup for ALL providers (explicit + implicit)
```

### Example

If `extract_tf_info_wrapper.sh` returns:
```json
{
  "providers": [{"name": "aws", ...}],
  "resources": [
    {"type": "aws_instance", ...},
    {"type": "random_id", ...}
  ]
}
```

You MUST lookup BOTH:
- `terraform-provider-aws` (explicit)
- `terraform-provider-random` (implicit - detected from `random_id` resource)

## Quick Reference Commands

### Format and Lint

```bash
# Check formatting (dry-run)
terraform fmt -check -recursive .

# Apply formatting
terraform fmt -recursive .

# Run tflint (requires .tflint.hcl config)
tflint --init              # Install plugins
tflint --recursive         # Lint all modules
tflint --format compact    # Compact output
```

> **TFLint Configuration:** See [TFLint Ruleset documentation](https://github.com/terraform-linters/tflint/blob/master/docs/user-guide/plugins.md) for plugin setup.

### Validate Configuration

```bash
# Initialize (downloads providers and modules)
terraform init

# Validate syntax
terraform validate

# Validate with JSON output
terraform validate -json
```

### Security Scanning

**MUST use wrapper script:**
```bash
# Use the wrapper script (REQUIRED)
bash scripts/run_checkov.sh ./terraform

# With specific options
bash scripts/run_checkov.sh -f json ./terraform
bash scripts/run_checkov.sh --compact ./terraform
```

> **Detailed Security Scanning:** You MUST read `references/security_checklist.md` before running security scans to understand the checks and remediation patterns.

## Security Finding Cross-Reference (REQUIRED)

**When reporting security findings, you MUST cite specific sections from `security_checklist.md`:**

### Cross-Reference Mapping

| Checkov Check Pattern | security_checklist.md Section |
|-----------------------|------------------------------|
| `CKV_AWS_24` (SSH open) | "Overly Permissive Security Groups" |
| `CKV_AWS_260` (HTTP open) | "Overly Permissive Security Groups" |
| `CKV_AWS_16` (RDS encryption) | "Encryption at Rest" |
| `CKV_AWS_17` (RDS public) | "RDS Databases" |
| `CKV_AWS_130` (public subnet) | "Network Security" |
| `CKV_AWS_53-56` (S3 public access) | "Public S3 Buckets" |
| `CKV_AWS_*` (IAM) | "IAM Security" |
| `CKV_AWS_79` (IMDSv1) | "ECS/EKS" |
| Hardcoded passwords | "Hardcoded Credentials" |
| Sensitive outputs | "Sensitive Output Exposure" |

### Report Template for Security Findings

```markdown
### Security Issue: [Check ID]

**Finding:** [Description from checkov]
**Resource:** [Resource name and file:line]
**Severity:** [HIGH/MEDIUM/LOW]

**Reference:** security_checklist.md - "[Section Name]"

**Remediation Pattern:**
[Copy relevant code example from security_checklist.md]

**Recommended Fix:**
[Specific fix for this configuration]
```

### Example Cross-Referenced Report

````markdown
### Security Issue: CKV_AWS_24

**Finding:** Security group allows SSH from 0.0.0.0/0
**Resource:** aws_security_group.web (main.tf:47-79)
**Severity:** HIGH

**Reference:** security_checklist.md - "Overly Permissive Security Groups"

**Remediation Pattern (from reference):**
```hcl
variable "admin_cidr" {
  description = "CIDR block for admin access"
  type        = string
}

resource "aws_security_group" "app" {
  ingress {
    description = "SSH from admin network only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }
}
```

**Recommended Fix:** Replace `cidr_blocks = ["0.0.0.0/0"]` with a variable or specific CIDR range.
````

### Dry-Run Testing

```bash
# Generate execution plan
terraform plan

# Save plan to file
terraform plan -out=tfplan

# Plan with specific var file
terraform plan -var-file="production.tfvars"

# Plan with target resource
terraform plan -target=aws_instance.example
```

**Plan Output Symbols:**
- `+` Resources to be created
- `-` Resources to be destroyed
- `~` Resources to be modified
- `-/+` Resources to be replaced

## Handling Missing Tools

When validation tools are not installed, follow this recovery workflow:

### Recovery Workflow (REQUIRED)

```
1. Detect missing tool
2. Inform user what is missing and why it's needed
3. Provide installation command
4. ASK user: "Would you like me to install [tool] and continue?"
5. If yes: Run installation and RERUN the validation step
6. If no: Note as skipped in report, continue with available tools
```

### Tool-Specific Recovery

**If checkov is missing:**
```
1. Inform: "Checkov is not installed. It's required for security scanning."
2. Ask: "Would you like me to install it? I'll use: bash scripts/install_checkov.sh install"
3. If yes: Run install script, then rerun security scan
```

**If tflint is missing:**
```
1. Inform: "TFLint is not installed. It provides advanced linting beyond terraform validate."
2. Ask: "Would you like me to install it?"
3. Provide: brew install tflint (macOS) or installation script (Linux)
```

**If python-hcl2 is missing:**
```
The extract_tf_info_wrapper.sh script handles this automatically by creating
or reusing a cached venv. No user action required.
```

**Required tools:** `terraform fmt`, `terraform init`, `terraform validate`
**Required for full security validation:** `checkov`
**Optional but recommended:** `tflint`

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `extract_tf_info_wrapper.sh` | Parse Terraform files for providers/modules (auto-handles dependencies) | `bash scripts/extract_tf_info_wrapper.sh <path>` |
| `extract_tf_info.py` | Core parser (requires python-hcl2) | Use wrapper instead |
| `run_checkov.sh` | Wrapper for Checkov scans with enhanced output | `bash scripts/run_checkov.sh <path>` |
| `install_checkov.sh` | Install Checkov in isolated venv | `bash scripts/install_checkov.sh install` |

## Reference Documentation

**MUST READ during validation workflow:**

| Reference | When to Read | Content |
|-----------|--------------|---------|
| `references/security_checklist.md` | Before security scan | Security validation, Checkov/Trivy usage, common policies, remediation patterns |
| `references/best_practices.md` | During validation | Project structure, naming conventions, module design, state management |
| `references/common_errors.md` | When errors occur | Error database with causes and solutions |
| `references/advanced_features.md` | If Terraform >= 1.10 | Ephemeral values (1.10+), Actions (1.14+), List Resources (1.14+) |

## Workflow Examples

### Example 1: Validate Single File

```
1. MUST: bash scripts/extract_tf_info_wrapper.sh main.tf
2. MUST: Context7 lookup for each provider detected
3. MUST: Read references/security_checklist.md
4. MUST: Read references/best_practices.md
5. RUN: terraform fmt -check main.tf
6. RUN: terraform init (if needed) && terraform validate
7. MUST: bash scripts/run_checkov.sh -f json main.tf
8. Report issues with remediation from references
9. If custom providers: WebSearch for documentation
```

### Example 2: Full Module Validation

```
1. Identify all .tf files in directory
2. MUST: bash scripts/extract_tf_info_wrapper.sh ./modules/vpc/
3. MUST: Context7 lookup for ALL providers
4. MUST: Read references/security_checklist.md
5. MUST: Read references/best_practices.md
6. RUN: terraform fmt -recursive
7. RUN: tflint --recursive (or note as skipped if unavailable)
8. RUN: terraform init && terraform validate
9. MUST: bash scripts/run_checkov.sh ./modules/vpc/
10. Analyze findings against security_checklist.md
11. Validate structure against best_practices.md
12. Provide comprehensive report with references
```

### Example 3: Production Dry-Run

```
1. Verify terraform initialized
2. MUST: Read references/security_checklist.md (production focus)
3. RUN: terraform plan -var-file="production.tfvars"
4. Analyze for unexpected changes
5. Highlight create/modify/destroy operations
6. Flag security concerns (compare with security_checklist.md)
7. Recommend whether safe to apply
```

## Advanced Features

Terraform 1.10+ introduces ephemeral values for secure secrets management. Terraform 1.14+ adds Actions for imperative operations and List Resources for querying infrastructure.

**MUST READ:** `references/advanced_features.md` when:
- Terraform version >= 1.10 is detected
- Configuration uses `ephemeral` blocks
- Configuration uses `action` blocks
- Configuration uses `.tfquery.hcl` files

## Integration with Other Skills

- **k8s-yaml-validator** - For Terraform Kubernetes provider validation
- **helm-validator** - When Terraform manages Helm releases
- **k8s-debug** - For debugging infrastructure provisioned by Terraform

## Notes

- Always run validation in order: extract info → lookup docs → read refs → format → lint → validate → security → plan
- MUST use wrapper scripts for extract_tf_info and checkov
- MUST run `bash tests/test_regression.sh` after script changes
- MUST run lightweight CI checks: `bash -n scripts/*.sh` and `python3 -m py_compile scripts/*.py`
- MUST read reference files before relevant validation steps
- MUST lookup provider docs via Context7 for ALL providers
- MUST offer recovery/rerun when tools are missing
- Never commit without running terraform fmt
- Always review plan output before applying
- Use version constraints for all providers and modules
- Use remote state for team collaboration
- Enable state locking to prevent concurrent modifications

## Done Criteria

- Validation instructions are executable end-to-end with one deterministic command path.
- Wrapper scripts behave predictably in both success and failure paths (including propagated non-zero exits).
- Regression tests cover parser error handling, implicit provider detection, wrapper argument handling, and checkov exit-code behavior.
- Lightweight CI checks (`bash -n`, `py_compile`, smoke checks) pass before final reporting.

---

## Reference: Advanced_Features

# Terraform Advanced Features

Modern Terraform features for enhanced infrastructure management. This reference covers features introduced in Terraform 1.10+.

> **Official Documentation:** [developer.hashicorp.com/terraform](https://developer.hashicorp.com/terraform/docs)

## Ephemeral Values and Write-Only Arguments (1.10+)

**Purpose:** Securely manage sensitive data like passwords and tokens without storing them in Terraform state or plan files.

### Overview

Ephemeral values are temporary values that exist only during a Terraform operation. They are never persisted to state, plan files, or logs. This is a major security improvement for secrets management.

### Ephemeral Resources

Ephemeral resources generate temporary values that don't persist:

```hcl
# Generate a temporary password - NOT stored in state
ephemeral "random_password" "db_password" {
  length           = 16
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Use with AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "db_password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id                = aws_secretsmanager_secret.db_password.id
  secret_string_wo         = ephemeral.random_password.db_password.result
  secret_string_wo_version = 1
}
```

### Write-Only Arguments (1.11+)

Write-only arguments accept values but never persist them:

```hcl
# Use ephemeral password with write-only argument
ephemeral "random_password" "db_password" {
  length = 16
}

resource "aws_db_instance" "example" {
  instance_class       = "db.t3.micro"
  allocated_storage    = "5"
  engine               = "postgres"
  username             = "admin"
  skip_final_snapshot  = true

  # Write-only argument - password is NOT stored in state
  password_wo          = ephemeral.random_password.db_password.result
  password_wo_version  = 1  # Increment to trigger password update
}
```

### Key Concepts

| Concept | Version | Description |
|---------|---------|-------------|
| `ephemeral` block | 1.10+ | Defines resources that are never stored in state |
| Ephemeral variables | 1.10+ | Variables marked `ephemeral = true` |
| Ephemeral outputs | 1.10+ | Outputs marked `ephemeral = true` |
| Write-only arguments | 1.11+ | Resource arguments ending in `_wo` that accept ephemeral values |
| `_wo_version` arguments | 1.11+ | Version tracking to prevent updates on every run |
| `ephemeralasnull` function | 1.10+ | Convert ephemeral to null for conditional logic |

### Ephemeral Input Variables

```hcl
variable "api_token" {
  type      = string
  sensitive = true
  ephemeral = true  # Value is not stored in state
}
```

### Ephemeral Outputs

```hcl
output "generated_password" {
  value     = ephemeral.random_password.main.result
  ephemeral = true  # Value is not stored in state
}
```

### Provider Support

Ephemeral resources are available in:
- AWS Provider (secrets, passwords)
- Azure Provider
- Kubernetes Provider
- Random Provider (`random_password`)
- Google Cloud Provider

### Security Best Practices

1. **Always use ephemeral for secrets** - passwords, API keys, tokens
2. **Use write-only arguments** - for database passwords, secret values
3. **Increment version** - when you need to update write-only values
4. **Combine with Secrets Manager** - store ephemeral values in vault
5. **Never log ephemeral values** - they won't appear in plan output

### Validation Considerations

When validating Terraform configurations with ephemeral values:
- Ephemeral resources don't appear in state
- Write-only arguments show as `(sensitive value)` in plans
- `terraform plan` will show ephemeral resource creation each run
- Checkov may not detect issues in ephemeral resources (no state)

---

## Actions Blocks (1.14+)

**Purpose:** Execute provider-defined imperative operations outside the normal CRUD model.

### Overview

Actions are a concept in Terraform 1.14 (GA - November 2025) that allow providers to define operations that don't fit the standard create/read/update/delete lifecycle. This is useful for one-time operations like invoking Lambda functions or invalidating CDN caches.

### Basic Example

```hcl
# Define an action to invoke a Lambda function
action "aws_lambda_invoke" "process_data" {
  config {
    function_name = aws_lambda_function.processor.function_name
    payload       = jsonencode({ action = "process" })
  }
}

# CloudFront cache invalidation action
action "aws_cloudfront_create_invalidation" "invalidate_cache" {
  config {
    distribution_id = aws_cloudfront_distribution.cdn.id
    paths           = ["/*"]
  }
}
```

### Advanced Example with Dependencies

```hcl
# Resource with action trigger on lifecycle events
resource "aws_s3_object" "data_file" {
  bucket       = aws_s3_bucket.data.id
  key          = "data/input.json"
  source       = "local/input.json"
  content_type = "application/json"

  # Trigger action when S3 object is updated
  lifecycle {
    action_trigger {
      events  = [after_update]
      actions = [action.aws_lambda_invoke.process_data]
    }
  }
}

# Lambda invocation action - triggered by resource lifecycle
action "aws_lambda_invoke" "process_data" {
  config {
    function_name = aws_lambda_function.processor.function_name
    payload = jsonencode({
      bucket = aws_s3_bucket.data.id
      key    = aws_s3_object.data_file.key
      action = "process"
    })
  }
}

# CloudFront cache invalidation - triggered after S3 update
resource "aws_s3_object" "index_html" {
  bucket       = aws_s3_bucket.website.id
  key          = "index.html"
  content_type = "text/html"
  source       = "html/index.html"

  lifecycle {
    action_trigger {
      events  = [after_update]
      actions = [action.aws_cloudfront_create_invalidation.invalidate_cache]
    }
  }
}

action "aws_cloudfront_create_invalidation" "invalidate_cache" {
  config {
    distribution_id = aws_cloudfront_distribution.cdn.id
    paths           = ["/*"]
  }
}
```

### Key Features

1. **Imperative Operations** - Actions perform side effects, not resource management
2. **Lifecycle Integration** - Can trigger on resource create/update/destroy
3. **CLI Invocation** - Run with `terraform apply -invoke` to trigger actions directly
4. **Provider-Defined** - Actions are defined by providers (AWS, Azure, etc.)
5. **Chainable** - Actions can depend on other actions

### CLI Commands

```bash
# Plan with specific action invocation
terraform plan -invoke=action.aws_lambda_invoke.process_data

# Apply with specific action invocation
terraform apply -invoke=action.aws_lambda_invoke.process_data

# Apply with auto-approve and action invocation
terraform apply -auto-approve -invoke=action.aws_cloudfront_create_invalidation.invalidate_cache

# Normal apply (actions triggered by lifecycle events still run)
terraform apply
```

### When to Use Actions

- Invoking Lambda/Cloud Functions
- Cache invalidation (CloudFront, CDN)
- Stopping/starting EC2 instances
- Database migrations
- API calls that don't create resources
- Post-deployment scripts
- Integration testing triggers

### Provider Support (as of November 2025)

| Provider | Available Actions |
|----------|-------------------|
| AWS | `aws_lambda_invoke`, `aws_cloudfront_create_invalidation`, `aws_ec2_stop_instance` |
| Azure | Coming soon |
| GCP | Coming soon |

### Validation Considerations

- Actions don't create resources in state
- `terraform plan` shows action effects separately
- Actions run in dependency order
- Failed actions don't roll back completed actions

---

## List Resources and Query Command (1.14+)

**Purpose:** Query and filter existing infrastructure resources directly from Terraform, with optional configuration generation for importing.

### Overview

Terraform 1.14 introduces List Resources, defined in `*.tfquery.hcl` files, that allow you to query existing infrastructure and optionally generate Terraform configuration for discovered resources.

### Basic Query File

```hcl
# my_query.tfquery.hcl

# List all S3 buckets with specific tags
list "aws_s3_bucket" "production_buckets" {
  filter {
    tags = {
      Environment = "production"
    }
  }
}

# List EC2 instances by type
list "aws_instance" "large_instances" {
  filter {
    instance_type = "t3.large"
  }
}

# List all VPCs
list "aws_vpc" "all_vpcs" {}
```

### CLI Commands

```bash
# Execute query and display results
terraform query

# Execute query with specific query file
terraform query -query=my_query.tfquery.hcl

# Generate configuration for discovered resources
terraform query -generate-config-out=discovered.tf

# Validate query files offline
terraform validate -query
```

### Advanced Query Example

```hcl
# infrastructure_audit.tfquery.hcl

# Find untagged resources
list "aws_s3_bucket" "untagged_buckets" {
  filter {
    tags = null
  }
}

# Find publicly accessible resources
list "aws_security_group" "public_ingress" {
  filter {
    ingress {
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
}

# Find resources by name pattern
list "aws_instance" "web_servers" {
  filter {
    tags = {
      Name = "web-*"
    }
  }
}
```

### Use Cases

1. **Infrastructure Auditing** - Discover resources not managed by Terraform
2. **Compliance Checking** - Find resources missing required tags
3. **Cost Optimization** - Identify oversized or unused resources
4. **Import Generation** - Generate configuration for manual imports
5. **Drift Detection** - Compare query results with state

### Output Example

```
$ terraform query

List: aws_s3_bucket.production_buckets
  Found 3 resources:

  - arn:aws:s3:::prod-logs-bucket
    tags.Environment = "production"
    tags.Team = "ops"

  - arn:aws:s3:::prod-assets-bucket
    tags.Environment = "production"
    tags.Team = "web"

  - arn:aws:s3:::prod-backups-bucket
    tags.Environment = "production"
    tags.Team = "dba"
```

### Validation Considerations

- Query files are validated with `terraform validate -query`
- Queries require valid provider authentication
- Results depend on IAM permissions
- Large queries may be rate-limited by cloud providers

---

## Feature Version Matrix

| Feature | Terraform Version | Status |
|---------|-------------------|--------|
| Ephemeral resources | 1.10+ | GA |
| Ephemeral variables/outputs | 1.10+ | GA |
| Write-only arguments | 1.11+ | GA |
| S3 native state locking | 1.11+ | GA |
| Actions blocks | 1.14+ | GA (Nov 2025) |
| List resources / Query | 1.14+ | GA (Nov 2025) |

## Related Documentation

- [Terraform Ephemeral Values](https://developer.hashicorp.com/terraform/language/values/ephemeral)
- [Terraform State Management](https://developer.hashicorp.com/terraform/language/state)
- [Import Block](https://developer.hashicorp.com/terraform/language/import)
- [Moved Block](https://developer.hashicorp.com/terraform/language/moved)
- [Removed Block](https://developer.hashicorp.com/terraform/language/removed)

---

## Reference: Best_Practices

# Terraform Best Practices

Coding standards and best practices for writing maintainable, scalable, and reliable Terraform configurations.

## Project Structure

### Recommended Directory Layout

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── production/
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── compute/
│   └── database/
├── global/
│   ├── iam/
│   └── route53/
└── README.md
```

### File Organization

**Standard Files:**
- `main.tf` - Primary resource definitions
- `variables.tf` - Input variable declarations
- `outputs.tf` - Output value declarations
- `versions.tf` - Terraform and provider version constraints
- `backend.tf` - Backend configuration
- `locals.tf` - Local value definitions (if many)
- `data.tf` - Data source definitions (if many)
- `terraform.tfvars` - Variable values (not committed for secrets)

**When to Split Files:**
- More than 200 lines in a single file
- Logical grouping of resources (e.g., `networking.tf`, `compute.tf`)
- Complex modules with many resource types

## Naming Conventions

### Resources

**Pattern:** `<resource-type>_<descriptive-name>`

```hcl
# Good
resource "aws_instance" "web_server" {}
resource "aws_s3_bucket" "application_logs" {}
resource "aws_security_group" "database_access" {}

# Avoid
resource "aws_instance" "instance1" {}
resource "aws_s3_bucket" "bucket" {}
```

### Variables

**Pattern:** `snake_case` with descriptive names

```hcl
# Good
variable "vpc_cidr_block" {}
variable "instance_type" {}
variable "environment_name" {}

# Avoid
variable "VPCCIDR" {}
variable "type" {}
variable "env" {}
```

### Modules

**Pattern:** `kebab-case` for directories, `snake_case` for module calls

```hcl
# Directory: modules/vpc-networking/

module "vpc_networking" {
  source = "./modules/vpc-networking"
}
```

### Tags

**Consistent Tagging Strategy:**

```hcl
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_name
    Owner       = var.owner_email
    CostCenter  = var.cost_center
  }
}

resource "aws_instance" "web" {
  # ... other config ...

  tags = merge(local.common_tags, {
    Name = "${var.environment}-web-server"
    Role = "webserver"
  })
}
```

## Variable Management

### Variable Declarations

**Always Include:**
- Type constraints
- Descriptions
- Validation rules (when applicable)
- Default values (for non-sensitive, non-environment-specific values)

```hcl
variable "instance_type" {
  description = "EC2 instance type for web servers"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = contains(["t3.micro", "t3.small", "t3.medium"], var.instance_type)
    error_message = "Instance type must be t3.micro, t3.small, or t3.medium."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "VPC CIDR must be a valid IPv4 CIDR block."
  }
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true  # Prevents display in logs
}
```

### Variable Types

**Use Specific Types:**

```hcl
# Primitive types
variable "instance_count" {
  type = number
}

variable "enable_monitoring" {
  type = bool
}

# Collection types
variable "availability_zones" {
  type = list(string)
}

variable "tags" {
  type = map(string)
}

# Object types
variable "database_config" {
  type = object({
    engine         = string
    engine_version = string
    instance_class = string
    allocated_storage = number
  })
}
```

### Environment-Specific Variables

**Use .tfvars Files:**

```hcl
# environments/dev/terraform.tfvars
environment     = "dev"
instance_type   = "t3.micro"
instance_count  = 1
enable_backup   = false

# environments/production/terraform.tfvars
environment     = "production"
instance_type   = "t3.large"
instance_count  = 3
enable_backup   = true
```

## Module Design

### Module Best Practices

**Single Responsibility:**
Each module should have one clear purpose.

```hcl
# Good: Focused module
module "vpc" {
  source = "./modules/vpc"
  # VPC-specific config
}

# Avoid: Kitchen-sink module
module "infrastructure" {
  source = "./modules/everything"
  # VPC, databases, compute, monitoring, etc.
}
```

**Required vs Optional Variables:**

```hcl
# modules/database/variables.tf

# Required - no default
variable "database_name" {
  description = "Name of the database"
  type        = string
}

# Optional - has sensible default
variable "backup_retention_days" {
  description = "Number of days to retain backups"
  type        = number
  default     = 7
}
```

**Output Everything Useful:**

```hcl
# modules/vpc/outputs.tf

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}
```

### Module Documentation

**README.md Template:**

```markdown
# VPC Module

Creates a VPC with public and private subnets across multiple availability zones.

## Usage

```hcl
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr             = "10.0.0.0/16"
  availability_zones   = ["us-east-1a", "us-east-1b"]
  environment          = "production"
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| aws | >= 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| vpc_cidr | CIDR block for VPC | `string` | n/a | yes |
| availability_zones | List of AZs | `list(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | ID of the VPC |
| private_subnet_ids | List of private subnet IDs |
```

## State Management

### Remote State

**Always Use Remote State for Teams:**

```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "production/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-locks"

    # Workspace-specific state
    workspace_key_prefix = "workspaces"
  }
}
```

### State Locking

**DynamoDB Table for S3 Backend:**

```hcl
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name      = "Terraform State Locks"
    ManagedBy = "Terraform"
  }
}
```

### State Isolation

**Separate State Files by Environment and Component:**

```
s3://terraform-state/
├── production/
│   ├── vpc/terraform.tfstate
│   ├── database/terraform.tfstate
│   └── compute/terraform.tfstate
├── staging/
│   ├── vpc/terraform.tfstate
│   └── compute/terraform.tfstate
└── dev/
    └── all/terraform.tfstate
```

## Resource Management

### Use Data Sources for Existing Resources

```hcl
# Instead of hardcoding
resource "aws_instance" "web" {
  subnet_id = "subnet-12345"  # Avoid
}

# Use data sources
data "aws_subnet" "private" {
  filter {
    name   = "tag:Name"
    values = ["${var.environment}-private-subnet"]
  }
}

resource "aws_instance" "web" {
  subnet_id = data.aws_subnet.private.id
}
```

### Resource Dependencies

**Implicit Dependencies (Preferred):**

```hcl
resource "aws_instance" "web" {
  subnet_id         = aws_subnet.private.id  # Implicit dependency
  security_groups   = [aws_security_group.web.id]
}
```

**Explicit Dependencies (When Needed):**

```hcl
resource "aws_iam_role_policy" "example" {
  # ... config ...

  # Ensure role exists before attaching policy
  depends_on = [aws_iam_role.example]
}
```

### Count vs For_Each

**Use for_each for Map-Like Resources:**

```hcl
# Good: for_each with maps
locals {
  subnets = {
    public_a  = { cidr = "10.0.1.0/24", az = "us-east-1a" }
    public_b  = { cidr = "10.0.2.0/24", az = "us-east-1b" }
    private_a = { cidr = "10.0.3.0/24", az = "us-east-1a" }
    private_b = { cidr = "10.0.4.0/24", az = "us-east-1b" }
  }
}

resource "aws_subnet" "main" {
  for_each = local.subnets

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr
  availability_zone = each.value.az

  tags = {
    Name = each.key
  }
}
```

**Use count for Simple Conditionals:**

```hcl
resource "aws_cloudwatch_log_group" "app" {
  count = var.enable_logging ? 1 : 0

  name = "/aws/app/logs"
}
```

## Version Constraints

### Terraform Version

```hcl
terraform {
  required_version = ">= 1.0, < 2.0"
}
```

### Provider Versions

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Allow patch updates, lock minor version
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

**Version Constraint Operators:**
- `=` - Exact version
- `!=` - Exclude version
- `>`, `>=`, `<`, `<=` - Comparison
- `~>` - Pessimistic constraint (allow rightmost version component to increment)

## State Management Blocks

Terraform 1.1+ introduced declarative blocks for managing state without manual `terraform state` commands.

### Import Block (Terraform 1.5+)

The `import` block allows config-driven import of existing resources into Terraform state.

**Basic Usage:**
```hcl
# Import an existing VPC
import {
  to = aws_vpc.main
  id = "vpc-0123456789abcdef0"
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main-vpc"
  }
}
```

**Dynamic Import (Terraform 1.6+):**
```hcl
# Import with expressions
variable "vpc_id" {
  type = string
}

import {
  to = aws_vpc.main
  id = var.vpc_id
}

# Import with string interpolation
import {
  to = aws_s3_bucket.logs
  id = "${var.environment}-logs-bucket"
}
```

**Generate Configuration:**
```bash
# Generate config for imported resources
terraform plan -generate-config-out=generated.tf
```

**Workflow:**
1. Add `import` block with target resource address and ID
2. Run `terraform plan` to see what will be imported
3. Add or generate the corresponding resource block
4. Run `terraform apply` to import
5. Remove the `import` block after successful import

### Moved Block (Terraform 1.1+)

The `moved` block enables refactoring without manual state manipulation.

**Rename a Resource:**
```hcl
# Old: aws_instance.web
# New: aws_instance.web_server

moved {
  from = aws_instance.web
  to   = aws_instance.web_server
}

resource "aws_instance" "web_server" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
}
```

**Move to a Module:**
```hcl
# Move resource into a module
moved {
  from = aws_vpc.main
  to   = module.networking.aws_vpc.main
}

module "networking" {
  source = "./modules/networking"
}
```

**Move from count to for_each:**
```hcl
# Old: aws_instance.web[0], aws_instance.web[1]
# New: aws_instance.web["web-1"], aws_instance.web["web-2"]

moved {
  from = aws_instance.web[0]
  to   = aws_instance.web["web-1"]
}

moved {
  from = aws_instance.web[1]
  to   = aws_instance.web["web-2"]
}

resource "aws_instance" "web" {
  for_each = toset(["web-1", "web-2"])

  ami           = "ami-12345678"
  instance_type = "t3.micro"

  tags = {
    Name = each.key
  }
}
```

**Rename a Module:**
```hcl
moved {
  from = module.old_name
  to   = module.new_name
}

module "new_name" {
  source = "./modules/compute"
}
```

**Best Practices for moved:**
- Keep `moved` blocks until all team members have applied the changes
- Remove `moved` blocks after state migration is complete across all environments
- Use descriptive commit messages explaining the refactoring

### Removed Block (Terraform 1.7+)

The `removed` block allows declarative removal of resources from Terraform management.

**Remove Without Destroying:**
```hcl
# Stop managing resource but keep it in cloud
removed {
  from = aws_instance.legacy_server

  lifecycle {
    destroy = false
  }
}
```

**Remove and Destroy:**
```hcl
# Remove from state and destroy the resource
removed {
  from = aws_s3_bucket.old_logs

  lifecycle {
    destroy = true
  }
}
```

**Remove Module:**
```hcl
# Remove entire module from management
removed {
  from = module.deprecated_service

  lifecycle {
    destroy = false
  }
}
```

**Use Cases:**
- Migrating resource ownership to another team/state
- Removing resources that should persist but not be managed
- Cleaning up after manual resource creation
- Deprecating modules without destroying infrastructure

### State Block Comparison

| Block | Version | Purpose | Use Case |
|-------|---------|---------|----------|
| `import` | 1.5+ | Bring existing resources into Terraform | Adopting existing infrastructure |
| `moved` | 1.1+ | Refactor without state surgery | Renaming, restructuring modules |
| `removed` | 1.7+ | Stop managing resources declaratively | Ownership transfer, cleanup |

### Migration from CLI Commands

**Old Way (CLI):**
```bash
# Import
terraform import aws_vpc.main vpc-12345

# Move
terraform state mv aws_instance.web aws_instance.web_server

# Remove
terraform state rm aws_instance.legacy
```

**New Way (Config-Driven):**
```hcl
# All operations are declarative and version-controlled
import {
  to = aws_vpc.main
  id = "vpc-12345"
}

moved {
  from = aws_instance.web
  to   = aws_instance.web_server
}

removed {
  from = aws_instance.legacy
  lifecycle {
    destroy = false
  }
}
```

**Benefits of Config-Driven Approach:**
- Changes are code-reviewed and version-controlled
- Operations are repeatable and documented
- Team collaboration without state file conflicts
- Rollback capability through git history

## Code Quality

### Use Locals for Computed Values

```hcl
locals {
  name_prefix = "${var.environment}-${var.project}"

  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  # Computed values
  is_production = var.environment == "production"
  instance_type = local.is_production ? "t3.large" : "t3.micro"
}
```

### Dynamic Blocks

**Use Sparingly and Only When Necessary:**

```hcl
resource "aws_security_group" "example" {
  name = "example"

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}
```

### Conditional Resources

```hcl
# Use count for conditional creation
resource "aws_kms_key" "encryption" {
  count = var.enable_encryption ? 1 : 0

  description = "Encryption key"
}

# Reference with [0] and handle with try()
resource "aws_s3_bucket" "example" {
  # ...

  kms_master_key_id = try(aws_kms_key.encryption[0].arn, null)
}
```

## Testing

### Validation

```bash
# Format check
terraform fmt -check -recursive

# Validation
terraform validate

# Plan review
terraform plan

# Compliance testing
terraform-compliance -p terraform.plan -f compliance/
```

### Pre-Commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.0
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_docs
      - id: terraform_tflint
```

## Performance

### Reduce Plan Time

- Use targeted plans for large infrastructures: `terraform plan -target=module.vpc`
- Split large configurations into smaller state files
- Use `-parallelism` flag: `terraform apply -parallelism=20`

### Optimize Resource Queries

```hcl
# Cache data source results in locals
data "aws_ami" "ubuntu" {
  most_recent = true
  # ... filters ...
}

locals {
  ami_id = data.aws_ami.ubuntu.id
}

# Reuse local value
resource "aws_instance" "web" {
  count         = 10
  ami           = local.ami_id  # Don't repeat data source
  instance_type = var.instance_type
}
```

## Documentation

### Inline Comments

```hcl
# Create VPC with DNS support enabled for private hosted zones
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true  # Required for Route53 private zones
  enable_dns_support   = true

  tags = merge(local.common_tags, {
    Name = "${var.environment}-vpc"
  })
}
```

### Module Documentation

Use [terraform-docs](https://github.com/terraform-docs/terraform-docs) to auto-generate documentation:

```bash
terraform-docs markdown table . > README.md
```

## Security Best Practices

- Never commit `.tfstate` files
- Never commit `.tfvars` files with secrets
- Use `.gitignore`:
  ```
  .terraform/
  *.tfstate
  *.tfstate.backup
  *.tfvars
  .terraform.lock.hcl
  ```
- Use `sensitive = true` for sensitive variables and outputs
- Encrypt remote state
- Use least-privilege IAM policies
- Enable MFA for state bucket access

## Workflow

### Recommended Git Workflow

1. Create feature branch
2. Make changes
3. Run `terraform fmt`
4. Run `terraform validate`
5. Run `terraform plan` and review
6. Commit changes
7. Create pull request
8. Peer review
9. Merge to main
10. Apply in environment

### CI/CD Integration

```yaml
# .github/workflows/terraform.yml
name: Terraform

on: [pull_request]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: hashicorp/setup-terraform@v2

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        run: terraform plan
```

---

## Reference: Common_Errors

# Common Terraform Errors

Database of frequently encountered Terraform errors with detailed solutions and prevention strategies.

## Initialization Errors

### Error: Failed to query available provider packages

```
Error: Failed to query available provider packages

Could not retrieve the list of available versions for provider
hashicorp/aws: no available releases match the given constraints
```

**Causes:**
- Invalid version constraint in `required_providers`
- Network connectivity issues
- Provider source incorrect or doesn't exist

**Solutions:**
```hcl
# Check provider configuration
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"  # Verify source is correct
      version = "~> 5.0"         # Check version exists
    }
  }
}
```

```bash
# Clear cache and reinitialize
rm -rf .terraform .terraform.lock.hcl
terraform init
```

### Error: Module not found

```
Error: Module not installed

This configuration requires module "vpc" but it is not installed.
```

**Causes:**
- Forgot to run `terraform init`
- Module source path incorrect
- Network issues downloading remote modules

**Solutions:**
```bash
# Initialize to download modules
terraform init

# Update modules
terraform init -upgrade

# Check module source
module "vpc" {
  source = "./modules/vpc"  # Verify path exists
  # or
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"
}
```

## Validation Errors

### Error: Unsupported argument

```
Error: Unsupported argument

An argument named "instance_class" is not expected here.
```

**Causes:**
- Typo in argument name
- Argument not supported in this resource type
- Wrong provider version

**Solutions:**
1. Check official documentation for correct argument names
2. Verify provider version supports the argument
3. Use `terraform console` to explore resource schema

```bash
# Check resource schema
terraform console
> provider::aws::schema::aws_instance
```

### Error: Missing required argument

```
Error: Missing required argument

The argument "ami" is required, but no definition was found.
```

**Solutions:**
```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id  # Add missing argument
  instance_type = var.instance_type
}
```

### Error: Incorrect attribute value type

```
Error: Incorrect attribute value type

Inappropriate value for attribute "instance_count": a number is required.
```

**Solutions:**
```hcl
# Ensure variable has correct type
variable "instance_count" {
  type    = number
  default = 1  # Not "1"
}

# Convert if needed
resource "aws_instance" "web" {
  count = tonumber(var.instance_count)
}
```

## Resource Errors

### Error: Error creating resource: already exists

```
Error: Error creating VPC: VpcLimitExceeded: The maximum number of VPCs has been reached.
```

**Causes:**
- Resource already exists in AWS
- Service quota exceeded
- Import needed for existing resource

**Solutions:**
```bash
# Import existing resource
terraform import aws_vpc.main vpc-12345678

# Request quota increase
aws service-quotas request-service-quota-increase \
  --service-code vpc \
  --quota-code L-F678F1CE \
  --desired-value 10
```

### Error: Resource not found

```
Error: Error reading VPC: VPCNotFound: The vpc ID 'vpc-12345' does not exist
```

**Causes:**
- Resource was manually deleted
- Wrong AWS region
- State file out of sync

**Solutions:**
```bash
# Refresh state
terraform refresh

# Remove from state if truly deleted
terraform state rm aws_vpc.main

# Check AWS region configuration
provider "aws" {
  region = "us-east-1"  # Verify correct region
}
```

### Error: Resource dependency violation

```
Error: Error deleting VPC: DependencyViolation: The vpc 'vpc-12345' has dependencies and cannot be deleted.
```

**Causes:**
- Resources still attached to VPC
- Manual deletion required first
- Incorrect destroy order

**Solutions:**
```bash
# Use targeted destroy
terraform destroy -target=aws_subnet.private
terraform destroy -target=aws_vpc.main

# Or recreate dependencies
terraform apply
terraform destroy  # Destroy in correct order
```

## State Management Errors

### Error: State lock acquisition failed

```
Error: Error acquiring the state lock

Lock Info:
  ID:        abc123
  Path:      terraform.tfstate
  Operation: OperationTypeApply
```

**Causes:**
- Another terraform process running
- Previous operation crashed without releasing lock
- DynamoDB table issues (S3 backend)

**Solutions:**
```bash
# Wait for other process to complete, or force unlock (use carefully)
terraform force-unlock abc123

# Verify no other terraform processes
ps aux | grep terraform

# Check DynamoDB lock table
aws dynamodb scan --table-name terraform-state-locks
```

### Error: State file version mismatch

```
Error: state snapshot was created by Terraform v1.5.0, which is newer than current v1.4.0
```

**Solutions:**
```bash
# Upgrade Terraform to required version
brew upgrade terraform

# Or use tfenv for version management
tfenv install 1.5.0
tfenv use 1.5.0
```

### Error: Backend configuration changed

```
Error: Backend configuration changed

A change in the backend configuration has been detected.
```

**Solutions:**
```bash
# Reconfigure backend
terraform init -reconfigure

# Migrate state to new backend
terraform init -migrate-state
```

## Plan/Apply Errors

### Error: Provider authentication failed

```
Error: error configuring Terraform AWS Provider: no valid credential sources for Terraform AWS Provider found.
```

**Causes:**
- AWS credentials not configured
- Expired credentials
- Wrong profile or role

**Solutions:**
```bash
# Set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"

# Or use AWS CLI profile
export AWS_PROFILE="your-profile"

# Or configure in provider
provider "aws" {
  profile = "your-profile"
  region  = "us-east-1"
}

# Verify credentials
aws sts get-caller-identity
```

### Error: Cycle dependency

```
Error: Cycle: aws_security_group.web, aws_security_group.db
```

**Causes:**
- Security groups reference each other
- Circular module dependencies

**Solutions:**
```hcl
# Break cycle with security group rules
resource "aws_security_group" "web" {
  name = "web-sg"
  # Remove inline rules causing cycle
}

resource "aws_security_group" "db" {
  name = "db-sg"
}

# Create rules separately
resource "aws_security_group_rule" "web_to_db" {
  type                     = "egress"
  from_port                = 3306
  to_port                  = 3306
  protocol                 = "tcp"
  security_group_id        = aws_security_group.web.id
  source_security_group_id = aws_security_group.db.id
}
```

### Error: Invalid count argument

```
Error: Invalid count argument

The "count" value depends on resource attributes that cannot be determined until apply.
```

**Solutions:**
```hcl
# Use two-step apply or redesign

# Bad
resource "aws_instance" "web" {
  count = length(aws_subnet.private)  # Unknown until apply
}

# Good - use for_each instead
resource "aws_instance" "web" {
  for_each = toset(var.subnet_ids)  # Known at plan time

  subnet_id = each.value
}
```

### Error: Invalid for_each argument

```
Error: Invalid for_each argument

The "for_each" value depends on resource attributes that cannot be determined until apply.
```

**Solutions:**
```hcl
# Use data sources or variables instead of resource attributes

# Bad
resource "aws_route_table_association" "private" {
  for_each = aws_subnet.private  # Unknown until apply
}

# Good
locals {
  subnets = {
    private_a = { cidr = "10.0.1.0/24" }
    private_b = { cidr = "10.0.2.0/24" }
  }
}

resource "aws_subnet" "private" {
  for_each   = local.subnets
  cidr_block = each.value.cidr
}
```

## Variable Errors

### Error: No value for required variable

```
Error: No value for required variable

The root module input variable "db_password" is not set.
```

**Solutions:**
```bash
# Set via command line
terraform apply -var="db_password=secretpass"

# Set via tfvars file
echo 'db_password = "secretpass"' > terraform.tfvars

# Set via environment variable
export TF_VAR_db_password="secretpass"
```

### Error: Invalid variable type

```
Error: Invalid value for input variable

The given value is not suitable for var.instance_count: number required.
```

**Solutions:**
```hcl
# In terraform.tfvars, use correct type
instance_count = 3  # Not "3"

# Or convert in code
variable "instance_count" {
  type = string
}

resource "aws_instance" "web" {
  count = tonumber(var.instance_count)
}
```

## Module Errors

### Error: Unsuitable value for module variable

```
Error: Unsuitable value for var.vpc_cidr

This value does not have any of the required types: string.
```

**Solutions:**
```hcl
# Check module call
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr = "10.0.0.0/16"  # Ensure string, not object
}
```

### Error: Unsupported attribute in module output

```
Error: Unsupported attribute

This object does not have an attribute named "vpc_id".
```

**Causes:**
- Output not defined in module
- Typo in output name
- Module version mismatch

**Solutions:**
```hcl
# Check module outputs.tf
output "vpc_id" {
  value = aws_vpc.main.id
}

# Reference correctly
resource "aws_instance" "web" {
  subnet_id = module.vpc.vpc_id  # Use exact output name
}
```

## Provider-Specific Errors

### AWS: Error creating Security Group: InvalidGroup.Duplicate

```
Error: Error creating Security Group: InvalidGroup.Duplicate: The security group 'web-sg' already exists
```

**Solutions:**
```bash
# Import existing security group
terraform import aws_security_group.web sg-12345678

# Or use data source
data "aws_security_group" "existing" {
  name = "web-sg"
}
```

### AWS: Error: Timeout while waiting for state

```
Error: timeout while waiting for resource to be created
```

**Causes:**
- Resource taking longer than expected
- Resource creation actually failed
- API throttling

**Solutions:**
```hcl
# Increase timeout
resource "aws_db_instance" "main" {
  # ... config ...

  timeouts {
    create = "60m"
    update = "60m"
    delete = "60m"
  }
}
```

### AWS: Error: UnauthorizedOperation

```
Error: UnauthorizedOperation: You are not authorized to perform this operation.
```

**Solutions:**
```bash
# Check IAM permissions
aws iam get-user-policy --user-name your-user --policy-name your-policy

# Verify required permissions for resource
# Example: EC2 instance requires:
# - ec2:RunInstances
# - ec2:DescribeInstances
# - ec2:DescribeImages
# etc.
```

## Workspace Errors

### Error: Workspace already exists

```
Error: Workspace "production" already exists
```

**Solutions:**
```bash
# Select existing workspace
terraform workspace select production

# List workspaces
terraform workspace list

# Delete workspace (if empty)
terraform workspace delete production
```

## Formatting Errors

### Error: Terraform fmt found issues

```
main.tf
  - Line 5: Incorrect indentation
```

**Solutions:**
```bash
# Auto-fix formatting
terraform fmt

# Check formatting (CI/CD)
terraform fmt -check

# Recursive formatting
terraform fmt -recursive
```

## Import Errors

### Error: Import resource does not exist

```
Error: Cannot import non-existent remote object
```

**Solutions:**
```bash
# Verify resource ID
aws ec2 describe-instances --instance-ids i-12345

# Use correct resource address
terraform import aws_instance.web i-1234567890abcdef0

# Check provider configuration matches resource region
```

## Prevention Strategies

### Pre-Commit Checks

```bash
# Run these before every commit
terraform fmt -check -recursive
terraform validate
terraform plan
```

### Use Validation Rules

```hcl
variable "environment" {
  type = string

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}
```

### Enable Detailed Logging

```bash
# Debug mode
export TF_LOG=DEBUG
terraform apply

# Log to file
export TF_LOG_PATH="./terraform.log"
```

### Version Pinning

```hcl
terraform {
  required_version = "~> 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

---

## Reference: Security_Checklist

# Terraform Security Checklist

Comprehensive security validation checklist for Terraform configurations. Use this reference when performing security reviews or auditing infrastructure-as-code.

## Secrets Management

### Hardcoded Credentials

**Risk:** Secrets committed to version control can be exposed.

**Detection:**
```bash
# Search for common secret patterns
grep -rE "(password|secret|api_key|access_key)\s*=\s*\"[^$]" *.tf
grep -rE "private_key\s*=\s*\"" *.tf
grep -rE "token\s*=\s*\"[^$]" *.tf
```

**Remediation:**
- Use Terraform variables with `sensitive = true`
- Use environment variables (TF_VAR_*)
- Use HashiCorp Vault or AWS Secrets Manager
- Use AWS Systems Manager Parameter Store
- Never commit `.tfvars` files with secrets

**Example - Insecure:**
```hcl
resource "aws_db_instance" "example" {
  username = "admin"
  password = "hardcoded_password123"  # SECURITY ISSUE
}
```

**Example - Secure:**
```hcl
variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_db_instance" "example" {
  username = "admin"
  password = var.db_password
}
```

### Sensitive Output Exposure

**Risk:** Sensitive data exposed in terraform state or plan output.

**Detection:**
- Review output blocks for sensitive data
- Check state files for plaintext secrets

**Remediation:**
```hcl
output "db_password" {
  value     = aws_db_instance.example.password
  sensitive = true  # Prevents display in console
}
```

## Network Security

### Overly Permissive Security Groups

**Risk:** Unrestricted access to resources from the internet.

**Detection Patterns:**
```hcl
# SECURITY ISSUE: SSH open to world
ingress {
  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

# SECURITY ISSUE: All ports open
ingress {
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}
```

**Best Practices:**
- Restrict SSH/RDP to specific IP ranges or VPN
- Use security group references instead of CIDR blocks
- Implement least-privilege access
- Document exceptions with comments

**Example - Secure:**
```hcl
variable "admin_cidr" {
  description = "CIDR block for admin access"
  type        = string
}

resource "aws_security_group" "app" {
  ingress {
    description = "SSH from admin network only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }
}
```

### Public S3 Buckets

**Risk:** Data exposure through public S3 access.

**Detection:**
```hcl
# SECURITY ISSUE: Public bucket
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.example.id

  block_public_acls       = false  # Should be true
  block_public_policy     = false  # Should be true
  ignore_public_acls      = false  # Should be true
  restrict_public_buckets = false  # Should be true
}
```

**Best Practices:**
```hcl
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.example.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

## Encryption

### Encryption at Rest

**Resources to Check:**
- RDS databases
- S3 buckets
- EBS volumes
- DynamoDB tables
- Elasticsearch domains
- Kinesis streams
- SQS queues

**Example - RDS Encryption:**
```hcl
resource "aws_db_instance" "example" {
  storage_encrypted = true  # Required
  kms_key_id       = aws_kms_key.db.arn  # Use customer-managed keys
}
```

**Example - S3 Encryption:**
```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
  }
}
```

### Encryption in Transit

**Risk:** Data intercepted during transmission.

**Best Practices:**
- Enforce HTTPS/TLS for all endpoints
- Use SSL/TLS for database connections
- Enable encryption for load balancers

**Example - ALB HTTPS:**
```hcl
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.example.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS-1-2-2017-01"
  certificate_arn   = aws_acm_certificate.cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.example.arn
  }
}

# Redirect HTTP to HTTPS
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.example.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}
```

## IAM Security

### Overly Permissive Policies

**Risk:** Privilege escalation and unauthorized access.

**Detection Patterns:**
```hcl
# SECURITY ISSUE: Admin access
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}

# SECURITY ISSUE: Too broad
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

**Best Practices:**
- Follow least-privilege principle
- Use specific actions instead of wildcards
- Scope resources narrowly
- Use conditions to restrict access

**Example - Least Privilege:**
```hcl
data "aws_iam_policy_document" "s3_read_only" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.app_data.arn,
      "${aws_s3_bucket.app_data.arn}/*"
    ]
  }
}
```

### Missing MFA Requirements

**Best Practice:**
```hcl
data "aws_iam_policy_document" "require_mfa" {
  statement {
    effect = "Deny"
    actions = ["*"]
    resources = ["*"]

    condition {
      test     = "BoolIfExists"
      variable = "aws:MultiFactorAuthPresent"
      values   = ["false"]
    }
  }
}
```

### Cross-Account Access

**Risk:** Unauthorized access from other AWS accounts.

**Best Practices:**
- Explicitly specify trusted accounts
- Require external ID for third-party access
- Use conditions to restrict access

```hcl
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::123456789012:root"]
    }
    actions = ["sts:AssumeRole"]

    condition {
      test     = "StringEquals"
      variable = "sts:ExternalId"
      values   = [var.external_id]
    }
  }
}
```

## Logging and Monitoring

### Missing CloudTrail

**Risk:** No audit trail for API calls.

**Best Practice:**
```hcl
resource "aws_cloudtrail" "main" {
  name                          = "main-trail"
  s3_bucket_name               = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true
  is_multi_region_trail        = true
  enable_logging               = true

  event_selector {
    read_write_type           = "All"
    include_management_events = true
  }
}
```

### Missing VPC Flow Logs

**Best Practice:**
```hcl
resource "aws_flow_log" "vpc" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.flow_logs.arn
  log_destination = aws_cloudwatch_log_group.flow_logs.arn
}
```

### Unencrypted Logs

**Best Practice:**
```hcl
resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/app/logs"
  retention_in_days = 90
  kms_key_id        = aws_kms_key.logs.arn  # Encrypt logs
}
```

## Resource-Specific Checks

### RDS Databases

- [ ] `storage_encrypted = true`
- [ ] `publicly_accessible = false`
- [ ] Backup retention enabled
- [ ] Multi-AZ for production
- [ ] IAM authentication enabled
- [ ] Enhanced monitoring enabled
- [ ] SSL/TLS required for connections

### ElastiCache

- [ ] `at_rest_encryption_enabled = true`
- [ ] `transit_encryption_enabled = true`
- [ ] Auth token enabled for Redis
- [ ] Subnet group in private subnets

### Lambda Functions

- [ ] Environment variables encrypted with KMS
- [ ] VPC configuration if accessing private resources
- [ ] IAM role with least-privilege
- [ ] Dead letter queue configured
- [ ] Reserved concurrency to prevent cost overruns

### ECS/EKS

- [ ] Secrets managed via Secrets Manager
- [ ] Container images scanned
- [ ] Network policy enforcement
- [ ] Pod security policies
- [ ] RBAC configured

## State File Security

### Remote State

**Risk:** State files contain sensitive data in plaintext.

**Best Practices:**

**Terraform 1.11+ (S3 Native Locking - Recommended):**
```hcl
terraform {
  backend "s3" {
    bucket       = "terraform-state-bucket"
    key          = "prod/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true  # Required
    kms_key_id   = "arn:aws:kms:..."
    use_lockfile = true  # S3 native locking (1.11+)
  }
}
```

> **Note:** Terraform 1.11 introduced S3 native state locking via the `use_lockfile` argument. This uses S3's conditional writes to implement locking without requiring DynamoDB. The DynamoDB-based locking (`dynamodb_table`) is now deprecated but still supported for backward compatibility.

**Legacy (Terraform < 1.11 or backward compatibility):**
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true  # Required
    kms_key_id     = "arn:aws:kms:..."
    dynamodb_table = "terraform-locks"  # State locking (deprecated in 1.11+)
  }
}
```

**Checklist:**
- [ ] Encryption enabled for state storage
- [ ] State locking configured (`use_lockfile = true` for 1.11+ or DynamoDB for older versions)
- [ ] Versioning enabled on state bucket
- [ ] Access restricted via IAM policies
- [ ] MFA delete enabled on state bucket
- [ ] State files never committed to version control

## Compliance Checks

### Tagging

**Best Practice:**
```hcl
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Owner       = var.owner
    CostCenter  = var.cost_center
    Compliance  = "HIPAA"  # If applicable
  }
}

resource "aws_instance" "example" {
  # ... other config ...
  tags = merge(local.common_tags, {
    Name = "app-server"
  })
}
```

### Data Residency

- Ensure resources in correct regions
- Check for cross-region replication
- Verify data sovereignty requirements

## Terraform-Specific Security

### Provider Version Pinning

**Risk:** Unexpected behavior from provider updates.

**Best Practice:**
```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # Pin major version
    }
  }
}
```

### Module Sources

**Risk:** Malicious code from untrusted modules.

**Best Practices:**
- Use verified modules from Terraform Registry
- Pin module versions
- Review module code before use
- Use private module registry for internal modules

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"  # Pin specific version
}
```

## Automated Security Scanning

Tools to integrate:
- **trivy** - Unified security scanner (successor to tfsec, includes IaC scanning)
- **checkov** - Policy-as-code security scanner (3000+ built-in policies)
- **terraform-compliance** - BDD-style testing

> **Note:** Terrascan was archived by Tenable on November 20, 2025 and is no longer maintained. Use Checkov or Trivy instead for OPA/Rego-style policy enforcement.

### Trivy (Recommended)

Trivy is Aqua Security's unified scanner that absorbed tfsec. It scans Terraform, CloudFormation, Kubernetes, Helm, and more.

**Version Note:**
> **Warning:** Trivy v0.60.0 has known regression issues that can cause panics when scanning Terraform configurations. If you experience crashes or unexpected behavior, downgrade to v0.59.x until v0.61.0+ is released with fixes.
>
> To install a specific version:
> ```bash
> # macOS
> brew install trivy@0.59.1
>
> # Linux - specify version in install script
> curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin v0.59.1
> ```

**Installation:**
```bash
# macOS
brew install trivy

# Linux
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Docker
docker pull aquasec/trivy
```

**Usage:**
```bash
# Scan Terraform directory
trivy config ./terraform

# Scan with specific severity
trivy config --severity HIGH,CRITICAL ./terraform

# Scan with JSON output
trivy config -f json -o results.json ./terraform

# Scan specific file
trivy config main.tf

# Skip specific checks
trivy config --skip-dirs .terraform ./terraform

# Scan Terraform plan JSON (more accurate)
terraform show -json tfplan > tfplan.json
trivy config tfplan.json

# Use tfvars files for accurate variable resolution
trivy config --tf-vars prod.terraform.tfvars ./terraform

# Exclude downloaded modules from scanning
trivy config --tf-exclude-downloaded-modules ./terraform
```

**Common Trivy Checks for Terraform:**
- `AVD-AWS-0086` - S3 bucket encryption
- `AVD-AWS-0089` - S3 bucket versioning
- `AVD-AWS-0132` - Security group unrestricted ingress
- `AVD-AWS-0107` - RDS encryption at rest
- `AVD-AWS-0078` - EBS encryption

**Output Formats:**
- `table` - Human-readable table (default)
- `json` - JSON format for CI/CD integration
- `sarif` - SARIF format for IDE integration
- `template` - Custom template output

**Ignore Findings:**
```hcl
# trivy:ignore:AVD-AWS-0086
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
}
```

**Advanced Trivy Configuration (trivy.yaml):**
```yaml
# trivy.yaml
exit-code: 1
severity:
  - HIGH
  - CRITICAL
scan:
  scanners:
    - vuln
    - secret
    - misconfig
misconfiguration:
  terraform:
    tfvars-files:
      - prod.tfvars
```

### Checkov 3.0

Checkov 3.0 introduces major improvements for Terraform scanning with enhanced graph policies and deeper analysis.

**Key 3.0 Features:**

1. **Deep Analysis Mode:**
   Fully resolve for_each, dynamic blocks, and complex configurations:
   ```bash
   # Enable deep analysis with plan file
   checkov -f tfplan.json --deep-analysis --repo-root-for-plan-enrichment .
   ```

2. **Baseline Feature:**
   Track only new misconfigurations (ignore existing):
   ```bash
   # Create baseline from current state
   checkov -d . --create-baseline

   # Run subsequent scans against baseline
   checkov -d . --baseline .checkov.baseline
   ```

3. **Enhanced Policy Language:**
   36 new operators including:
   - `SUBSET` - Check if values are subset of allowed values
   - `jsonpath_*` operators - Deep JSON path queries
   - Enhanced graph traversal for complex dependencies

4. **Improved Dynamic Block Support:**
   ```bash
   # Scan with full dynamic block resolution
   checkov -d . --download-external-modules true
   ```

**Checkov 3.0 Commands:**
```bash
# Basic scan
checkov -d .

# Deep analysis with Terraform plan
terraform plan -out=tf.plan
terraform show -json tf.plan > tfplan.json
checkov -f tfplan.json --deep-analysis

# Create and use baseline
checkov -d . --create-baseline
checkov -d . --baseline .checkov.baseline

# Compact output (failures only)
checkov -d . --compact

# Skip specific checks
checkov -d . --skip-check CKV_AWS_20,CKV_AWS_21

# Run only specific frameworks
checkov -d . --framework terraform
```

### Tool Comparison

| Tool | Focus | Policy Language | Built-in Policies | Best For |
|------|-------|-----------------|-------------------|----------|
| **trivy** | Security | Rego | 1000+ | All-in-one scanning, container + IaC |
| **checkov** | Security/Compliance | Python/YAML | 3000+ | Multi-framework, compliance, deep analysis |

**Note:** tfsec has been deprecated and merged into Trivy. Terrascan was archived in November 2025. New users should use Trivy or Checkov.

## Quick Security Audit Commands

```bash
# Check for hardcoded secrets
grep -r "password\s*=\s*\"" . --include="*.tf"
grep -r "secret\s*=\s*\"" . --include="*.tf"

# Find public security groups
grep -r "0.0.0.0/0" . --include="*.tf"

# Find unencrypted resources
grep -r "encrypted\s*=\s*false" . --include="*.tf"

# Check for missing backup configurations
grep -r "backup_retention_period\s*=\s*0" . --include="*.tf"
```
