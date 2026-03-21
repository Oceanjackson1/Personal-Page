---
title: "Terraform 生成器"
description: "生成 Terraform 基础设施代码，云资源配置和模块化设计"
category: "devops"
source: "community"
author: "Community"
tags: ["terraform", "generator"]
date: 2026-03-20
---

# Terraform Generator

## Overview

This skill enables the generation of production-ready Terraform configurations following best practices and current standards. Automatically integrates validation and documentation lookup for custom providers and modules.

## Critical Requirements Checklist

**STOP: You MUST complete ALL steps in order. Do NOT skip any REQUIRED step.**

| Step | Action | Required |
|------|--------|----------|
| 1 | Understand requirements (providers, resources, modules) | ✅ REQUIRED |
| 2 | Check for custom providers/modules and lookup documentation | ✅ REQUIRED |
| 3 | Consult reference files before generation | ✅ REQUIRED |
| 4 | Generate Terraform files with ALL best practices | ✅ REQUIRED |
| 5 | Include data sources for dynamic values (region, account, AMIs) | ✅ REQUIRED |
| 6 | Add lifecycle rules on critical resources (KMS, databases) | ✅ REQUIRED |
| 7 | Invoke `Skill(devops-skills:terraform-validator)` | ✅ REQUIRED |
| 8 | **FIX all validation/security failures and RE-VALIDATE** | ✅ REQUIRED |
| 9 | Provide usage instructions (files, next steps, security) | ✅ REQUIRED |

> **IMPORTANT:** If validation fails (terraform validate OR security scan), you MUST fix the issues and re-run validation until ALL checks pass. Do NOT proceed to Step 9 with failing checks.

## Core Workflow

When generating Terraform configurations, follow this workflow:

### Step 1: Understand Requirements

Analyze the user's request to determine:
- What infrastructure resources need to be created
- Which Terraform providers are required (AWS, Azure, GCP, custom, etc.)
- Whether any modules are being used (official, community, or custom)
- Version constraints for providers and modules
- Variable inputs and outputs needed
- State backend configuration (local, S3, remote, etc.)

### Step 2: Check for Custom Providers/Modules

Before generating configurations, identify if custom or third-party providers/modules are involved:

**Standard providers** (no lookup needed):
- hashicorp/aws
- hashicorp/azurerm
- hashicorp/google
- hashicorp/kubernetes
- Other official HashiCorp providers

**Custom/third-party providers/modules** (require documentation lookup):
- Third-party providers (e.g., datadog/datadog, mongodb/mongodbatlas)
- Custom modules from Terraform Registry
- Private or company-specific modules
- Community modules

**When custom providers/modules are detected:**

1. Use WebSearch to find version-specific documentation:
   ```
   Search query format: "[provider/module name] terraform [version] documentation [specific resource]"
   Example: "datadog terraform provider v3.30 monitor resource documentation"
   Example: "terraform-aws-modules vpc version 5.0 documentation"
   ```

2. Focus searches on:
   - Official documentation (registry.terraform.io, provider websites)
   - Required and optional arguments
   - Attribute references
   - Example usage
   - Version compatibility notes

3. If Context7 MCP is available and the provider/module is supported, use it as an alternative:
   ```
   mcp__context7__resolve-library-id → mcp__context7__query-docs
   ```

### Step 2.5: Consult Reference Files (REQUIRED)

Before generating configuration, you MUST consult reference files using this matrix:

| Reference | Requirement | Read When |
|-----------|-------------|-----------|
| `terraform_best_practices.md` | REQUIRED | Always - contains baseline required patterns |
| `provider_examples.md` | REQUIRED | Any AWS, Azure, GCP, or Kubernetes resource generation |
| `common_patterns.md` | OPTIONAL by default, REQUIRED for complex requests | Multi-environment, workspace, composition, DR, or conditional patterns |

Open references by path:

```
devops-skills-plugin/skills/terraform-generator/references/terraform_best_practices.md
devops-skills-plugin/skills/terraform-generator/references/provider_examples.md
devops-skills-plugin/skills/terraform-generator/references/common_patterns.md
```

### Step 3: Generate Terraform Configuration

Generate HCL files following best practices:

**File Organization:**
```
terraform-project/
├── main.tf           # Primary resource definitions
├── variables.tf      # Input variable declarations
├── outputs.tf        # Output value declarations
├── versions.tf       # Provider version constraints
├── terraform.tfvars  # Variable values (optional, for examples)
└── backend.tf        # Backend configuration (optional)
```

**Best Practices to Follow:**

1. **Provider Configuration:**
   ```hcl
   terraform {
     required_version = ">= 1.10, < 2.0"

     required_providers {
       aws = {
         source  = "hashicorp/aws"
         version = "~> 6.0"  # Major pin; verify exact current version when needed
       }
     }
   }

   provider "aws" {
     region = var.aws_region
   }
   ```

2. **Resource Naming:**
   - Use descriptive resource names
   - Follow snake_case convention
   - Include resource type in name when helpful
   ```hcl
   resource "aws_instance" "web_server" {
     # ...
   }
   ```

3. **Variable Declarations:**
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
   ```

4. **Output Values:**
   ```hcl
   output "instance_public_ip" {
     description = "Public IP address of the web server"
     value       = aws_instance.web_server.public_ip
   }
   ```

5. **Use Data Sources for References:**
   ```hcl
   data "aws_ami" "ubuntu" {
     most_recent = true
     owners      = ["099720109477"] # Canonical

     filter {
       name   = "name"
       values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
     }
   }
   ```

6. **Module Usage:**
   ```hcl
   module "vpc" {
     source  = "terraform-aws-modules/vpc/aws"
     version = "5.0.0"

     name = "my-vpc"
     cidr = "10.0.0.0/16"

     azs             = ["us-east-1a", "us-east-1b"]
     private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
     public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
   }
   ```

7. **Use locals for Computed Values:**
   ```hcl
   locals {
     common_tags = {
       Environment = var.environment
       ManagedBy   = "Terraform"
       Project     = var.project_name
     }
   }
   ```

8. **Lifecycle Rules When Appropriate:**
   ```hcl
   resource "aws_instance" "example" {
     # ...

     lifecycle {
       create_before_destroy = true
       prevent_destroy       = true
       ignore_changes        = [tags]
     }
   }
   ```

9. **Dynamic Blocks for Repeated Configuration:**
   ```hcl
   resource "aws_security_group" "example" {
     # ...

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

10. **Comments and Documentation:**
    - Add comments explaining complex logic
    - Document why certain values are used
    - Include examples in variable descriptions

**Security Best Practices:**
- Never hardcode sensitive values (use variables)
- Use data sources for AMIs and other dynamic values
- Implement least-privilege IAM policies
- Enable encryption by default
- Use secure backend configurations

### Required: Data Sources for Dynamic Values (Provider-Aware)

You MUST include provider-appropriate data lookups for dynamic infrastructure values. Do NOT hardcode cloud/account/region/image IDs.

| Provider | Required Dynamic Context | Typical Data Sources |
|----------|--------------------------|----------------------|
| AWS | Region/account/AZ/image IDs | `aws_region`, `aws_caller_identity`, `aws_availability_zones`, `aws_ami` |
| Azure | Tenant/subscription/client context | `azurerm_client_config`, `azurerm_subscription` |
| GCP | Project/client context/zone discovery | `google_client_config`, `google_compute_zones`, `google_compute_image` |
| Kubernetes | Cluster endpoint/auth from trusted source | Use module outputs or cloud data sources; avoid hardcoded tokens/endpoints |

```hcl
# AWS dynamic context
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# Azure dynamic context
data "azurerm_client_config" "current" {}
data "azurerm_subscription" "current" {}

# GCP dynamic context
data "google_client_config" "current" {}
```

### Required: Lifecycle and Deletion Safeguards (Provider-Aware)

You MUST protect stateful and critical resources from accidental destruction/deletion using both Terraform lifecycle and provider-native safeguards.

| Provider | Critical Resource Classes | Required Protection Mechanism |
|----------|---------------------------|-------------------------------|
| AWS | KMS, RDS, S3 data buckets, DynamoDB, ElastiCache, secrets | `lifecycle { prevent_destroy = true }` and service-specific deletion protection where supported |
| Azure | Key Vaults, SQL, Storage, stateful compute | `prevent_destroy` where appropriate plus provider feature flags/resource deletion protection |
| GCP | Cloud SQL, GKE, storage, stateful compute | `prevent_destroy` and resource-level `deletion_protection = true` where supported |
| Kubernetes | Stateful workloads and persistent data | Avoid destructive replacement patterns and protect backing cloud resources |

```hcl
resource "aws_db_instance" "main" {
  # ...
  deletion_protection = true
  lifecycle {
    prevent_destroy = true
  }
}

resource "google_sql_database_instance" "main" {
  # ...
  deletion_protection = true
}
```

### Required: Object Storage Lifecycle Safeguards

When using AWS S3 lifecycle configuration, ALWAYS include a rule to abort incomplete multipart uploads:

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  # REQUIRED: Abort incomplete multipart uploads to prevent storage costs
  rule {
    id     = "abort-incomplete-uploads"
    status = "Enabled"

    # Filter applies to all objects (empty filter = all objects)
    filter {}

    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }

  # Other lifecycle rules (e.g., transition to IA)
  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    filter {
      prefix = ""  # Apply to all objects
    }

    transition {
      days          = 90
      storage_class = "STANDARD_IA"
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 365
    }
  }
}
```

> **Why?** Incomplete multipart uploads consume storage and incur costs. Checkov check `CKV_AWS_300` enforces this for AWS.
>
> For Azure/GCP object storage, add equivalent lifecycle/retention rules for stale objects and old versions.

### Step 4: Validate Generated Configuration (REQUIRED)

After generating Terraform files, ALWAYS validate them using the devops-skills:terraform-validator skill:

```
Invoke: Skill(devops-skills:terraform-validator)
```

The devops-skills:terraform-validator skill will:
1. Check HCL syntax with `terraform fmt -check`
2. Initialize the configuration with `terraform init`
3. Validate the configuration with `terraform validate`
4. Run security scan with Checkov
5. Perform dry-run testing (if requested) with `terraform plan`

**CRITICAL: Fix-and-Revalidate Loop**

If ANY validation or security check fails, you MUST:

1. **Review the error** - Understand what failed and why
2. **Fix the issue** - Edit the generated file to resolve the problem
3. **Re-run validation** - Invoke `Skill(devops-skills:terraform-validator)` again
4. **Repeat until ALL checks pass** - Do NOT proceed with failing checks

```
┌─────────────────────────────────────────────────────────┐
│  VALIDATION FAILED?                                      │
│                                                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────────────────┐  │
│  │  Fix    │───▶│ Re-run  │───▶│ All checks pass?    │  │
│  │  Issue  │    │ Skill   │    │ YES → Step 5        │  │
│  └─────────┘    └─────────┘    │ NO  → Loop back     │  │
│       ▲                         └─────────────────────┘  │
│       │                                    │             │
│       └────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────┘
```

**Common validation failures to fix:**
| Check | Issue | Fix |
|-------|-------|-----|
| `CKV_AWS_300` | Missing abort multipart upload | Add `abort_incomplete_multipart_upload` rule |
| `CKV_AWS_24` | SSH open to 0.0.0.0/0 | Restrict to specific CIDR |
| `CKV_AWS_16` | RDS encryption disabled | Add `storage_encrypted = true` |
| `terraform validate` | Invalid resource argument | Check provider documentation |

**If custom providers are detected during validation:**
- The devops-skills:terraform-validator skill will automatically fetch documentation
- Use the fetched documentation to fix any issues

### Step 5: Provide Usage Instructions (REQUIRED)

After successful generation and validation with ALL checks passing, you MUST provide the user with:

**Required Output Format:**

```markdown
## Generated Files

| File | Description |
|------|-------------|
| `<actual-file-path>` | What was generated in that file |

Only list files that were actually generated for this request. Do not include placeholder paths or files that do not exist.

## Next Steps

1. Review and customize `terraform.tfvars` with your values
2. Initialize Terraform:
   ```bash
   terraform init
   ```
3. Review the execution plan:
   ```bash
   terraform plan
   ```
4. Apply the configuration:
   ```bash
   terraform apply
   ```

## Customization Notes

- [ ] Update `variable_name` in terraform.tfvars
- [ ] Configure backend in backend.tf for remote state
- [ ] Adjust resource names/tags as needed

## Security Reminders

⚠️ Before applying:
- Review IAM policies and permissions
- Ensure sensitive values are NOT committed to version control
- Configure state backend with encryption enabled
- Set up state locking for team collaboration
```

> **IMPORTANT:** Do NOT skip Step 5. The user needs actionable guidance on how to use the generated configuration.

## Common Generation Patterns

### Pattern 1: Simple Resource Creation

User request: "Create an AWS S3 bucket with versioning"

Generated files:
- `main.tf` - S3 bucket resource with versioning enabled
- `variables.tf` - Bucket name, tags variables
- `outputs.tf` - Bucket ARN and name outputs
- `versions.tf` - AWS provider version constraints

### Pattern 2: Module-Based Infrastructure

User request: "Set up a VPC using the official AWS VPC module"

Actions:
1. Identify module: terraform-aws-modules/vpc/aws
2. Web search for latest version and documentation
3. Generate configuration using module with appropriate inputs
4. Validate with devops-skills:terraform-validator

### Pattern 3: Multi-Provider Configuration

User request: "Create infrastructure across AWS and Datadog"

Actions:
1. Identify standard provider (AWS) and custom provider (Datadog)
2. Web search for Datadog provider documentation with version
3. Generate configuration with both providers properly configured
4. Ensure provider aliases if needed
5. Validate with devops-skills:terraform-validator

### Pattern 4: Complex Resource with Dependencies

User request: "Create an ECS cluster with ALB and auto-scaling"

Generated structure:
- Multiple resource blocks with proper dependencies
- Data sources for AMIs, availability zones, etc.
- Local values for computed configurations
- Comprehensive variables and outputs
- Proper dependency management using implicit references

## Error Handling

**Common Issues and Solutions:**

1. **Provider Not Found:**
   - Ensure provider is listed in `required_providers` block
   - Verify source address format: `namespace/name`
   - Check version constraint syntax

2. **Invalid Resource Arguments:**
   - Refer to web search results for custom providers
   - Check for required vs optional arguments
   - Verify attribute value types (string, number, bool, list, map)

3. **Circular Dependencies:**
   - Review resource references
   - Use `depends_on` explicit dependencies if needed
   - Consider breaking into separate modules

4. **Validation Failures:**
   - Run devops-skills:terraform-validator skill to get detailed errors
   - Fix issues one at a time
   - Re-validate after each fix

## Version Awareness

Always consider version compatibility:

1. **Terraform Version:**
   - Use `required_version` constraint with both lower and upper bounds
   - If generated configuration includes write-only arguments (`*_wo`): use `required_version = ">= 1.11, < 2.0"`.
   - Else if it uses ephemeral constructs (`ephemeral` blocks, ephemeral variables/outputs) without write-only arguments: use `required_version = ">= 1.10, < 2.0"`.
   - Else use the project baseline (default `>= 1.8, < 2.0` unless repository policy requires newer).
   - Use `>= 1.14, < 2.0` for latest features (actions, query command)
   - Document any version-specific features used (see below)

2. **Provider Version Policy (canonical):**
   - Pin provider major versions with `~>` constraints (for example `~> 6.0`, `~> 4.0`, `~> 7.0`).
   - Do not claim "latest" version unless verified online during the current run.
   - Keep cross-provider guidance consistent:
     - AWS family: major-pin policy (for example `~> 6.0`)
     - AzureRM: major-pin policy (for example `~> 4.0`)
     - Google: major-pin policy (for example `~> 7.0`)
     - Kubernetes: major/minor pin based on target cluster/provider compatibility
   - Use the same provider/version language in `SKILL.md`, `references/terraform_best_practices.md`, and template `assets/minimal-project/versions.tf`.

3. **Module Versions:**
   - Always pin module versions
   - Review module documentation for version compatibility
   - Test module updates in non-production first

### Required Version Decision Table

| Generated Output Contains | Required Version to Emit |
|---------------------------|--------------------------|
| Any write-only argument (`*_wo`) | `>= 1.11, < 2.0` |
| Ephemeral constructs only (no write-only) | `>= 1.10, < 2.0` |
| Neither write-only nor ephemeral | Project baseline (default `>= 1.8, < 2.0`) |

#### Feature-Gating Examples

```hcl
# Positive: write-only usage requires Terraform 1.11+
terraform {
  required_version = ">= 1.11, < 2.0"
}

ephemeral "random_password" "db_password" {
  length = 16
}

resource "aws_db_instance" "main" {
  identifier          = "mydb"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  engine              = "postgres"
  username            = "admin"
  skip_final_snapshot = true

  password_wo         = ephemeral.random_password.db_password.result
  password_wo_version = 1
}
```

```hcl
# Negative: reject this pattern (write-only with Terraform 1.10)
terraform {
  required_version = ">= 1.10, < 2.0"
}

resource "aws_db_instance" "invalid" {
  password_wo = "do-not-generate-this"
}
```

### Terraform Version Feature Matrix

| Feature | Minimum Version |
|---------|-----------------|
| `terraform_data` resource | 1.4+ |
| `import {}` blocks | 1.5+ |
| `check {}` blocks | 1.5+ |
| Native testing (`.tftest.hcl`) | 1.6+ |
| Test mocking | 1.7+ |
| `removed {}` blocks | 1.7+ |
| Provider-defined functions | 1.8+ |
| Cross-type refactoring | 1.8+ |
| Enhanced variable validations | 1.9+ |
| `templatestring` function | 1.9+ |
| Ephemeral resources | 1.10+ |
| Write-only arguments | 1.11+ |
| S3 native state locking | 1.11+ |
| Import blocks with `for_each` | 1.12+ |
| Actions block | 1.14+ |
| List resources (`tfquery.hcl`) | 1.14+ |
| `terraform query` command | 1.14+ |

## Modern Terraform Features (1.8+)

### Provider-Defined Functions (Terraform 1.8+)

Provider-defined functions extend Terraform's built-in functions with provider-specific logic.

**Syntax:** `provider::<provider_name>::<function_name>(arguments)`

```hcl
# AWS Provider Functions (v5.40+)
locals {
  # Parse an ARN into components
  parsed_arn = provider::aws::arn_parse(aws_instance.web.arn)
  account_id = local.parsed_arn.account
  region     = local.parsed_arn.region

  # Build an ARN from components
  custom_arn = provider::aws::arn_build({
    partition = "aws"
    service   = "s3"
    region    = ""
    account   = ""
    resource  = "my-bucket/my-key"
  })
}

# Google Cloud Provider Functions (v5.23+)
locals {
  # Extract region from zone
  region = provider::google::region_from_zone(var.zone)  # "us-west1-a" → "us-west1"
}

# Kubernetes Provider Functions (v2.28+)
locals {
  # Encode HCL to Kubernetes manifest YAML
  manifest_yaml = provider::kubernetes::manifest_encode(local.deployment_config)
}
```

### Ephemeral Resources (Terraform 1.10+)

Ephemeral resources provide temporary values that are **never persisted** in state or plan files. Critical for handling secrets securely.

```hcl
# Generate a password that never touches state
ephemeral "random_password" "db_password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# Fetch secrets ephemerally from AWS Secrets Manager
ephemeral "aws_secretsmanager_secret_version" "api_key" {
  secret_id = aws_secretsmanager_secret.api_key.id
}

# Ephemeral variables (declare with ephemeral = true)
variable "temporary_token" {
  type      = string
  ephemeral = true  # Value won't be stored in state
}

# Ephemeral outputs
output "session_token" {
  value     = ephemeral.aws_secretsmanager_secret_version.api_key.secret_string
  ephemeral = true  # Won't be stored in state
}
```

### Write-Only Arguments (Terraform 1.11+)

Write-only arguments accept ephemeral values and are never persisted. They use `_wo` suffix and require a version attribute.

```hcl
terraform {
  required_version = ">= 1.11, < 2.0"
}

# Secure database password handling
ephemeral "random_password" "db_password" {
  length = 16
}

resource "aws_db_instance" "main" {
  identifier        = "mydb"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  engine            = "postgres"
  username          = "admin"

  # Write-only password - never stored in state!
  password_wo         = ephemeral.random_password.db_password.result
  password_wo_version = 1  # Increment to trigger password rotation

  skip_final_snapshot = true
}

# Secrets Manager with write-only
resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id

  # Write-only secret string
  secret_string_wo         = ephemeral.random_password.db_password.result
  secret_string_wo_version = 1
}
```

### Enhanced Variable Validations (Terraform 1.9+)

Validation conditions can now reference other variables, data sources, and local values.

```hcl
# Reference data sources in validation
data "aws_ec2_instance_type_offerings" "available" {
  filter {
    name   = "location"
    values = [var.availability_zone]
  }
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type"

  validation {
    # NEW: Can reference data sources
    condition = contains(
      data.aws_ec2_instance_type_offerings.available.instance_types,
      var.instance_type
    )
    error_message = "Instance type ${var.instance_type} is not available in the selected AZ."
  }
}

# Cross-variable validation
variable "min_instances" {
  type    = number
  default = 1
}

variable "max_instances" {
  type    = number
  default = 10

  validation {
    # NEW: Can reference other variables
    condition     = var.max_instances >= var.min_instances
    error_message = "max_instances must be >= min_instances"
  }
}
```

### S3 Native State Locking (Terraform 1.11+)

S3 now supports native state locking without DynamoDB.

```hcl
terraform {
  backend "s3" {
    bucket       = "my-terraform-state"
    key          = "project/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true

    # NEW: S3-native locking (Terraform 1.11+)
    use_lockfile = true

    # DEPRECATED: DynamoDB locking (still works but no longer required)
    # dynamodb_table = "terraform-locks"
  }
}
```

### Import Blocks (Terraform 1.5+)

Declarative resource imports without command-line operations.

```hcl
# Import existing resources declaratively
import {
  to = aws_instance.web
  id = "i-1234567890abcdef0"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  # ... configuration must match existing resource
}

# Import with for_each
import {
  for_each = var.existing_bucket_names
  to       = aws_s3_bucket.imported[each.key]
  id       = each.value
}
```

### Moved and Removed Blocks

Safely refactor resources without destroying them.

```hcl
# Rename a resource
moved {
  from = aws_instance.old_name
  to   = aws_instance.new_name
}

# Move to a module
moved {
  from = aws_vpc.main
  to   = module.networking.aws_vpc.main
}

# Cross-type refactoring (1.8+)
moved {
  from = null_resource.example
  to   = terraform_data.example
}

# Remove resource from state without destroying (1.7+)
removed {
  from = aws_instance.legacy

  lifecycle {
    destroy = false  # Keep the actual resource, just remove from state
  }
}
```

### Import Blocks with for_each (Terraform 1.12+)

Import multiple resources using `for_each` meta-argument.

```hcl
# Import multiple S3 buckets using a map
locals {
  buckets = {
    "staging" = "bucket1"
    "uat"     = "bucket2"
    "prod"    = "bucket3"
  }
}

import {
  for_each = local.buckets
  to       = aws_s3_bucket.this[each.key]
  id       = each.value
}

resource "aws_s3_bucket" "this" {
  for_each = local.buckets
}

# Import across module instances using list of objects
locals {
  module_buckets = [
    { group = "one", key = "bucket1", id = "one_1" },
    { group = "one", key = "bucket2", id = "one_2" },
    { group = "two", key = "bucket1", id = "two_1" },
  ]
}

import {
  for_each = local.module_buckets
  id       = each.value.id
  to       = module.group[each.value.group].aws_s3_bucket.this[each.value.key]
}
```

### Actions Block (Terraform 1.14+)

Actions enable provider-defined operations outside the standard CRUD model. Use for operations like Lambda invocations, cache invalidations, or database backups.

```hcl
# Invoke a Lambda function (example syntax)
action "aws_lambda_invoke" "process_data" {
  function_name = aws_lambda_function.processor.function_name
  payload       = jsonencode({ action = "process" })
}

# Create CloudFront invalidation
action "aws_cloudfront_create_invalidation" "invalidate_cache" {
  distribution_id = aws_cloudfront_distribution.main.id
  paths           = ["/*"]
}

# Actions support for_each
action "aws_lambda_invoke" "batch_process" {
  for_each = toset(["task1", "task2", "task3"])

  function_name = aws_lambda_function.processor.function_name
  payload       = jsonencode({ task = each.value })
}
```

**Triggering Actions via Lifecycle:**

Use `action_trigger` within a resource's lifecycle block to automatically invoke actions:

```hcl
resource "aws_lambda_function" "example" {
  function_name = "my-function"
  # ... other config ...

  lifecycle {
    action_trigger {
      events  = [after_create, after_update]
      actions = [action.aws_lambda_invoke.process_data]
    }
  }
}

action "aws_lambda_invoke" "process_data" {
  function_name = aws_lambda_function.example.function_name
  payload       = jsonencode({ action = "initialize" })
}
```

**Manual Invocation:**

Actions can also be invoked manually via CLI:

```bash
terraform apply -invoke action.aws_lambda_invoke.process_data
```

### List Resources and Query Command (Terraform 1.14+)

Query and filter existing infrastructure using `.tfquery.hcl` files and the `terraform query` command.

```hcl
# my-resources.tfquery.hcl
# Define list resources to query existing infrastructure

list "aws_instance" "web_servers" {
  filter {
    name   = "tag:Environment"
    values = [var.environment]
  }

  include_resource = true  # Include full resource details
}

list "aws_s3_bucket" "data_buckets" {
  filter {
    name   = "tag:Purpose"
    values = ["data-storage"]
  }
}
```

```bash
# Query infrastructure and output results
terraform query

# Generate import configuration from query results
terraform query -generate-config-out="import_config.tf"

# Output in JSON format
terraform query -json

# Use with variables
terraform query -var 'environment=prod'
```

### Preconditions and Postconditions (Terraform 1.5+)

Add custom validation within resource lifecycle.

```hcl
resource "aws_instance" "example" {
  instance_type = "t3.micro"
  ami           = data.aws_ami.example.id

  lifecycle {
    # Check before creation
    precondition {
      condition     = data.aws_ami.example.architecture == "x86_64"
      error_message = "The selected AMI must be for the x86_64 architecture."
    }

    # Verify after creation
    postcondition {
      condition     = self.public_dns != ""
      error_message = "EC2 instance must be in a VPC that has public DNS hostnames enabled."
    }
  }
}

# Preconditions on outputs
output "web_url" {
  value = "https://${aws_instance.web.public_dns}"

  precondition {
    condition     = aws_instance.web.public_dns != ""
    error_message = "Instance must have a public DNS name."
  }
}
```

## Resources

### references/

The `references/` directory contains detailed documentation for reference:

- `terraform_best_practices.md` - Comprehensive best practices guide
- `common_patterns.md` - Common Terraform patterns and examples
- `provider_examples.md` - Example configurations for popular providers

Open a reference directly by relative path:
```
devops-skills-plugin/skills/terraform-generator/references/[filename].md
```

### assets/

The `assets/` directory contains template files:

- `minimal-project/` - Minimal Terraform project template

Templates can be copied and customized for the user's specific needs.

## Notes

- Always run devops-skills:terraform-validator after generation
- For feature/version drift checks in CI, run `bash scripts/run_ci_checks.sh`
- Web search is essential for custom providers/modules
- Follow the principle of least surprise in configurations
- Make configurations readable and maintainable
- Include helpful comments and documentation
- Generate realistic examples in terraform.tfvars when helpful

---

## Reference: Common_Patterns

# Common Terraform Patterns

## Multi-Environment Pattern

### Directory Structure
```
terraform/
├── modules/
│   └── app/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── environments/
    ├── dev/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── terraform.tfvars
    │   └── backend.tf
    ├── staging/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── terraform.tfvars
    │   └── backend.tf
    └── production/
        ├── main.tf
        ├── variables.tf
        ├── terraform.tfvars
        └── backend.tf
```

### Implementation

```hcl
# environments/dev/main.tf
module "app" {
  source = "../../modules/app"

  environment     = "dev"
  instance_type   = "t3.micro"
  instance_count  = 1
  enable_backups  = false
}

# environments/production/main.tf
module "app" {
  source = "../../modules/app"

  environment     = "production"
  instance_type   = "t3.large"
  instance_count  = 3
  enable_backups  = true
}
```

## Workspace Pattern

### Using Workspaces for Environments

```hcl
# main.tf
locals {
  environment = terraform.workspace

  environment_config = {
    dev = {
      instance_type  = "t3.micro"
      instance_count = 1
      enable_backups = false
    }
    staging = {
      instance_type  = "t3.small"
      instance_count = 2
      enable_backups = true
    }
    prod = {
      instance_type  = "t3.large"
      instance_count = 3
      enable_backups = true
    }
  }

  config = local.environment_config[local.environment]
}

resource "aws_instance" "app" {
  count         = local.config.instance_count
  instance_type = local.config.instance_type
  # ...
}

# Usage:
# terraform workspace new dev
# terraform workspace select dev
# terraform apply
```

## Blue-Green Deployment Pattern

### Infrastructure for Blue-Green Deployments

```hcl
variable "active_environment" {
  description = "Active environment (blue or green)"
  type        = string
  default     = "blue"

  validation {
    condition     = contains(["blue", "green"], var.active_environment)
    error_message = "Active environment must be blue or green."
  }
}

# Blue environment
module "blue_environment" {
  source = "./modules/environment"

  name            = "blue"
  instance_count  = var.active_environment == "blue" ? var.desired_capacity : 1
  min_size        = var.active_environment == "blue" ? var.min_capacity : 0
  max_size        = var.active_environment == "blue" ? var.max_capacity : 1
  ami_id          = var.blue_ami_id
  # ...
}

# Green environment
module "green_environment" {
  source = "./modules/environment"

  name            = "green"
  instance_count  = var.active_environment == "green" ? var.desired_capacity : 1
  min_size        = var.active_environment == "green" ? var.min_capacity : 0
  max_size        = var.active_environment == "green" ? var.max_capacity : 1
  ami_id          = var.green_ami_id
  # ...
}

# Load balancer with weighted routing
resource "aws_lb_target_group" "blue" {
  name     = "blue-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_target_group" "green" {
  name     = "green-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_lb_listener_rule" "weighted" {
  listener_arn = aws_lb_listener.main.arn

  action {
    type = "forward"

    forward {
      target_group {
        arn    = aws_lb_target_group.blue.arn
        weight = var.active_environment == "blue" ? 100 : 0
      }

      target_group {
        arn    = aws_lb_target_group.green.arn
        weight = var.active_environment == "green" ? 100 : 0
      }
    }
  }

  condition {
    path_pattern {
      values = ["/*"]
    }
  }
}
```

## Data Layer Separation Pattern

### Separating Stateful and Stateless Infrastructure

```
terraform/
├── data-layer/          # Stateful resources (databases, storage)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── backend.tf
└── app-layer/           # Stateless resources (compute, networking)
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── backend.tf
```

```hcl
# data-layer/main.tf
resource "aws_db_instance" "main" {
  allocated_storage    = 100
  engine              = "postgres"
  engine_version      = "14.7"
  instance_class      = "db.t3.large"
  name                = "appdb"
  username            = var.db_username
  password            = var.db_password

  # Prevent accidental deletion
  deletion_protection = true
  skip_final_snapshot = false

  lifecycle {
    prevent_destroy = true
  }
}

# data-layer/outputs.tf
output "database_endpoint" {
  value = aws_db_instance.main.endpoint
}

# app-layer/main.tf
data "terraform_remote_state" "data_layer" {
  backend = "s3"

  config = {
    bucket = "terraform-state"
    key    = "data-layer/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_instance" "app" {
  # ...

  user_data = templatefile("${path.module}/user_data.sh", {
    database_endpoint = data.terraform_remote_state.data_layer.outputs.database_endpoint
  })
}
```

## Module Composition Pattern

### Building Complex Infrastructure from Simple Modules

```hcl
# Root configuration
module "network" {
  source = "./modules/network"

  vpc_cidr            = var.vpc_cidr
  availability_zones  = var.availability_zones
  public_subnet_cidrs = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs

  tags = local.common_tags
}

module "security" {
  source = "./modules/security"

  vpc_id = module.network.vpc_id

  allowed_cidr_blocks = var.allowed_cidr_blocks

  tags = local.common_tags
}

module "compute" {
  source = "./modules/compute"

  vpc_id         = module.network.vpc_id
  subnet_ids     = module.network.private_subnet_ids
  security_group_ids = [module.security.app_security_group_id]

  instance_type  = var.instance_type
  instance_count = var.instance_count

  tags = local.common_tags
}

module "load_balancer" {
  source = "./modules/load_balancer"

  vpc_id         = module.network.vpc_id
  subnet_ids     = module.network.public_subnet_ids
  security_group_ids = [module.security.lb_security_group_id]

  target_instances = module.compute.instance_ids

  tags = local.common_tags
}

module "database" {
  source = "./modules/database"

  vpc_id         = module.network.vpc_id
  subnet_ids     = module.network.database_subnet_ids
  security_group_ids = [module.security.db_security_group_id]

  database_name = var.database_name
  master_username = var.db_username
  master_password = var.db_password

  tags = local.common_tags
}
```

## Conditional Resource Creation Pattern

### Creating Resources Based on Conditions

```hcl
# Using count for conditional creation
resource "aws_instance" "bastion" {
  count = var.create_bastion ? 1 : 0

  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "bastion-host"
  }
}

# Using for_each with conditional map
resource "aws_cloudwatch_log_group" "optional" {
  for_each = var.enable_logging ? toset(var.log_group_names) : toset([])

  name              = each.value
  retention_in_days = var.log_retention_days
}

# Conditional module inclusion
module "cdn" {
  count  = var.enable_cdn ? 1 : 0
  source = "./modules/cdn"

  origin_domain_name = aws_lb.main.dns_name
  # ...
}

# Accessing conditionally created resources
output "bastion_public_ip" {
  value = var.create_bastion ? aws_instance.bastion[0].public_ip : null
}
```

## Service Mesh Pattern

### Implementing Service Discovery and Mesh

```hcl
# Service registry
resource "aws_service_discovery_private_dns_namespace" "main" {
  name = "internal.example.com"
  vpc  = aws_vpc.main.id
}

# Service definitions
resource "aws_service_discovery_service" "backend" {
  name = "backend"

  dns_config {
    namespace_id = aws_service_discovery_private_dns_namespace.main.id

    dns_records {
      ttl  = 10
      type = "A"
    }

    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

# ECS service with service discovery
resource "aws_ecs_service" "backend" {
  name            = "backend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = 3

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.backend.id]
  }

  service_registries {
    registry_arn = aws_service_discovery_service.backend.arn
  }
}
```

## Tagging Strategy Pattern

### Comprehensive Tagging Implementation

```hcl
locals {
  # Mandatory tags
  mandatory_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    Owner       = var.owner_email
    CostCenter  = var.cost_center
  }

  # Optional tags
  optional_tags = var.additional_tags

  # Combined tags
  common_tags = merge(local.mandatory_tags, local.optional_tags)

  # Resource-specific tags
  database_tags = merge(
    local.common_tags,
    {
      Type      = "Database"
      Backup    = "Required"
      Retention = "30days"
    }
  )

  compute_tags = merge(
    local.common_tags,
    {
      Type           = "Compute"
      AutoScaling    = var.enable_autoscaling
      PatchSchedule  = "Sundays-2AM"
    }
  )
}

# Apply tags to resources
resource "aws_instance" "web" {
  # ...
  tags = merge(
    local.compute_tags,
    {
      Name = "${var.project_name}-web-${count.index + 1}"
      Role = "WebServer"
    }
  )
}

resource "aws_db_instance" "main" {
  # ...
  tags = merge(
    local.database_tags,
    {
      Name = "${var.project_name}-db"
    }
  )
}
```

## Secret Injection Pattern

### Securely Managing Secrets

```hcl
# Using AWS Secrets Manager
data "aws_secretsmanager_secret" "app_secrets" {
  name = "${var.environment}/app/secrets"
}

data "aws_secretsmanager_secret_version" "app_secrets" {
  secret_id = data.aws_secretsmanager_secret.app_secrets.id
}

locals {
  app_secrets = jsondecode(data.aws_secretsmanager_secret_version.app_secrets.secret_string)
}

# ECS task definition with secrets
resource "aws_ecs_task_definition" "app" {
  family = "app"

  container_definitions = jsonencode([
    {
      name  = "app"
      image = var.app_image

      secrets = [
        {
          name      = "DB_PASSWORD"
          valueFrom = "${data.aws_secretsmanager_secret.app_secrets.arn}:password::"
        },
        {
          name      = "API_KEY"
          valueFrom = "${data.aws_secretsmanager_secret.app_secrets.arn}:api_key::"
        }
      ]

      environment = [
        {
          name  = "DB_HOST"
          value = aws_db_instance.main.endpoint
        }
      ]
    }
  ])
}

# Lambda function with secrets
resource "aws_lambda_function" "processor" {
  # ...

  environment {
    variables = {
      DB_HOST        = aws_db_instance.main.endpoint
      SECRETS_ARN    = data.aws_secretsmanager_secret.app_secrets.arn
    }
  }
}
```

## Auto-Scaling Pattern

### Comprehensive Auto-Scaling Configuration

```hcl
# Launch template
resource "aws_launch_template" "app" {
  name_prefix   = "${var.project_name}-"
  image_id      = data.aws_ami.app.id
  instance_type = var.instance_type

  iam_instance_profile {
    name = aws_iam_instance_profile.app.name
  }

  network_interfaces {
    associate_public_ip_address = false
    security_groups            = [aws_security_group.app.id]
    delete_on_termination      = true
  }

  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    environment = var.environment
  }))

  tag_specifications {
    resource_type = "instance"
    tags = local.compute_tags
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name                = "${var.project_name}-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300

  min_size         = var.min_capacity
  max_size         = var.max_capacity
  desired_capacity = var.desired_capacity

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  enabled_metrics = [
    "GroupDesiredCapacity",
    "GroupInServiceInstances",
    "GroupMaxSize",
    "GroupMinSize",
    "GroupPendingInstances",
    "GroupStandbyInstances",
    "GroupTerminatingInstances",
    "GroupTotalInstances"
  ]

  dynamic "tag" {
    for_each = local.compute_tags

    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

# Target tracking scaling policy - CPU
resource "aws_autoscaling_policy" "cpu_target" {
  name                   = "${var.project_name}-cpu-target"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 70.0
  }
}

# Target tracking scaling policy - Request count
resource "aws_autoscaling_policy" "request_count_target" {
  name                   = "${var.project_name}-request-count-target"
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label        = "${aws_lb.main.arn_suffix}/${aws_lb_target_group.app.arn_suffix}"
    }
    target_value = 1000.0
  }
}

# Scheduled scaling
resource "aws_autoscaling_schedule" "scale_up_morning" {
  scheduled_action_name  = "scale-up-morning"
  min_size               = var.min_capacity
  max_size               = var.max_capacity
  desired_capacity       = var.desired_capacity * 2
  recurrence             = "0 8 * * MON-FRI"
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_schedule" "scale_down_evening" {
  scheduled_action_name  = "scale-down-evening"
  min_size               = var.min_capacity
  max_size               = var.max_capacity
  desired_capacity       = var.desired_capacity
  recurrence             = "0 18 * * MON-FRI"
  autoscaling_group_name = aws_autoscaling_group.app.name
}
```

## Disaster Recovery Pattern

### Multi-Region DR Setup

```hcl
# Primary region provider
provider "aws" {
  alias  = "primary"
  region = var.primary_region
}

# DR region provider
provider "aws" {
  alias  = "dr"
  region = var.dr_region
}

# Primary region resources
module "primary_infrastructure" {
  source = "./modules/infrastructure"

  providers = {
    aws = aws.primary
  }

  environment = var.environment
  is_primary  = true
  # ...
}

# DR region resources
module "dr_infrastructure" {
  source = "./modules/infrastructure"

  providers = {
    aws = aws.dr
  }

  environment = var.environment
  is_primary  = false
  # ...
}

# Route53 health check and failover
resource "aws_route53_health_check" "primary" {
  fqdn              = module.primary_infrastructure.load_balancer_dns
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}

resource "aws_route53_record" "primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  set_identifier = "primary"
  failover_routing_policy {
    type = "PRIMARY"
  }

  alias {
    name                   = module.primary_infrastructure.load_balancer_dns
    zone_id               = module.primary_infrastructure.load_balancer_zone_id
    evaluate_target_health = true
  }

  health_check_id = aws_route53_health_check.primary.id
}

resource "aws_route53_record" "dr" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  set_identifier = "dr"
  failover_routing_policy {
    type = "SECONDARY"
  }

  alias {
    name                   = module.dr_infrastructure.load_balancer_dns
    zone_id               = module.dr_infrastructure.load_balancer_zone_id
    evaluate_target_health = true
  }
}

# Cross-region replication for S3
resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.primary

  bucket = module.primary_infrastructure.data_bucket_id
  role   = aws_iam_role.replication.arn

  rule {
    id     = "replicate-all"
    status = "Enabled"

    destination {
      bucket        = module.dr_infrastructure.data_bucket_arn
      storage_class = "STANDARD_IA"

      replication_time {
        status = "Enabled"
        time {
          minutes = 15
        }
      }

      metrics {
        status = "Enabled"
        event_threshold {
          minutes = 15
        }
      }
    }
  }
}

# RDS read replica in DR region
resource "aws_db_instance" "read_replica" {
  provider = aws.dr

  replicate_source_db = module.primary_infrastructure.database_arn

  instance_class      = var.db_instance_class
  publicly_accessible = false
  skip_final_snapshot = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-db-replica"
      Role = "DR"
    }
  )
}
```

## Cost Optimization Pattern

### Implementing Cost Controls

```hcl
# Use Spot Instances for non-critical workloads
resource "aws_autoscaling_group" "batch_processing" {
  # ...

  mixed_instances_policy {
    instances_distribution {
      on_demand_base_capacity                  = 1
      on_demand_percentage_above_base_capacity = 20
      spot_allocation_strategy                 = "capacity-optimized"
    }

    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.batch.id
        version            = "$Latest"
      }

      override {
        instance_type     = "t3.medium"
        weighted_capacity = 1
      }

      override {
        instance_type     = "t3.large"
        weighted_capacity = 2
      }
    }
  }
}

# Schedule shutdown for non-production environments
resource "aws_autoscaling_schedule" "shutdown_evening" {
  count = var.environment != "production" ? 1 : 0

  scheduled_action_name  = "shutdown-evening"
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
  recurrence             = "0 20 * * *"
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_schedule" "startup_morning" {
  count = var.environment != "production" ? 1 : 0

  scheduled_action_name  = "startup-morning"
  min_size               = var.min_capacity
  max_size               = var.max_capacity
  desired_capacity       = var.desired_capacity
  recurrence             = "0 8 * * MON-FRI"
  autoscaling_group_name = aws_autoscaling_group.app.name
}

# Use lifecycle policies for S3
resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "transition-old-data"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "STANDARD_IA"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# Budget alerts
resource "aws_budgets_budget" "monthly" {
  name              = "${var.project_name}-monthly-budget"
  budget_type       = "COST"
  limit_amount      = var.monthly_budget
  limit_unit        = "USD"
  time_period_start = "2024-01-01_00:00"
  time_unit         = "MONTHLY"

  cost_filter {
    name = "TagKeyValue"
    values = [
      "Project$${var.project_name}",
    ]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.budget_alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.budget_alert_email]
  }
}
```

---

## Reference: Provider_Examples

# Terraform Provider Examples

## AWS Provider

### Provider Configuration

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"  # Latest: v6.23.0 (Dec 2025)
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}

# Additional provider for different region
provider "aws" {
  alias  = "us_west"
  region = "us-west-2"
}
```

### Common AWS Resources

```hcl
# EC2 Instance
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.private[0].id

  vpc_security_group_ids = [aws_security_group.web.id]

  root_block_device {
    volume_type = "gp3"
    volume_size = 30
    encrypted   = true
  }

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "${var.project_name}-web"
  }
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Subnet
resource "aws_subnet" "public" {
  count = length(var.availability_zones)

  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone = var.availability_zones[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-${var.availability_zones[count.index]}"
  }
}

# Security Group
resource "aws_security_group" "web" {
  name_prefix = "${var.project_name}-web-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-web-sg"
  }
}

# S3 Bucket
resource "aws_s3_bucket" "data" {
  bucket = "${var.project_name}-data-${random_id.bucket_suffix.hex}"

  tags = {
    Name = "${var.project_name}-data"
  }
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier             = "${var.project_name}-db"
  allocated_storage      = 100
  engine                 = "postgres"
  engine_version         = "14.7"
  instance_class         = var.db_instance_class
  db_name                = var.database_name
  username               = var.db_username
  password               = var.db_password

  vpc_security_group_ids = [aws_security_group.database.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  storage_encrypted      = true
  deletion_protection    = true
  skip_final_snapshot    = false
  final_snapshot_identifier = "${var.project_name}-db-final-snapshot"

  tags = {
    Name = "${var.project_name}-db"
  }
}

# Lambda Function
resource "aws_lambda_function" "processor" {
  filename         = "lambda_function.zip"
  function_name    = "${var.project_name}-processor"
  role            = aws_iam_role.lambda.arn
  handler         = "index.handler"
  source_code_hash = filebase64sha256("lambda_function.zip")
  runtime         = "python3.11"
  timeout         = 300
  memory_size     = 512

  environment {
    variables = {
      ENVIRONMENT = var.environment
      TABLE_NAME  = aws_dynamodb_table.main.name
    }
  }

  vpc_config {
    subnet_ids         = aws_subnet.private[*].id
    security_group_ids = [aws_security_group.lambda.id]
  }

  tags = {
    Name = "${var.project_name}-processor"
  }
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = var.environment == "production"

  tags = {
    Name = "${var.project_name}-alb"
  }
}

resource "aws_lb_target_group" "app" {
  name     = "${var.project_name}-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }

  tags = {
    Name = "${var.project_name}-tg"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
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

## Azure Provider

### Provider Configuration

```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }

    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}
```

### Common Azure Resources

```hcl
# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-rg"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "${var.project_name}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = azurerm_resource_group.main.tags
}

# Subnet
resource "azurerm_subnet" "app" {
  name                 = "app-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]

  service_endpoints = ["Microsoft.Storage", "Microsoft.Sql"]
}

# Network Security Group
resource "azurerm_network_security_group" "app" {
  name                = "${var.project_name}-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  security_rule {
    name                       = "AllowHTTP"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "AllowHTTPS"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = azurerm_resource_group.main.tags
}

# Virtual Machine
resource "azurerm_linux_virtual_machine" "app" {
  name                = "${var.project_name}-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = var.vm_size
  admin_username      = var.admin_username

  network_interface_ids = [
    azurerm_network_interface.app.id,
  ]

  admin_ssh_key {
    username   = var.admin_username
    public_key = file("~/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  tags = azurerm_resource_group.main.tags
}

# Storage Account
resource "azurerm_storage_account" "main" {
  name                     = "${var.project_name}storage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  blob_properties {
    versioning_enabled = true

    delete_retention_policy {
      days = 7
    }
  }

  tags = azurerm_resource_group.main.tags
}

# SQL Database
resource "azurerm_mssql_server" "main" {
  name                         = "${var.project_name}-sqlserver"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = var.sql_admin_username
  administrator_login_password = var.sql_admin_password

  tags = azurerm_resource_group.main.tags
}

resource "azurerm_mssql_database" "main" {
  name      = "${var.project_name}-db"
  server_id = azurerm_mssql_server.main.id
  sku_name  = "S1"

  tags = azurerm_resource_group.main.tags
}

# App Service
resource "azurerm_service_plan" "main" {
  name                = "${var.project_name}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "P1v2"

  tags = azurerm_resource_group.main.tags
}

resource "azurerm_linux_web_app" "main" {
  name                = "${var.project_name}-app"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      node_version = "18-lts"
    }

    always_on = true
  }

  app_settings = {
    "WEBSITE_NODE_DEFAULT_VERSION" = "18-lts"
    "ENVIRONMENT"                  = var.environment
  }

  tags = azurerm_resource_group.main.tags
}
```

## Google Cloud Provider

### Provider Configuration

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"  # Latest: v7.12.0 - includes ephemeral resources & write-only attributes
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
```

### Common GCP Resources

```hcl
# VPC Network
resource "google_compute_network" "main" {
  name                    = "${var.project_name}-vpc"
  auto_create_subnetworks = false
}

# Subnet
resource "google_compute_subnetwork" "app" {
  name          = "${var.project_name}-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.main.id

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.2.0.0/16"
  }
}

# Firewall Rule
resource "google_compute_firewall" "allow_http" {
  name    = "${var.project_name}-allow-http"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web"]
}

# Compute Instance
resource "google_compute_instance" "web" {
  name         = "${var.project_name}-web"
  machine_type = var.machine_type
  zone         = var.zone

  tags = ["web", var.environment]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 20
      type  = "pd-ssd"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.app.id

    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = file("${path.module}/startup.sh")

  service_account {
    email  = google_service_account.app.email
    scopes = ["cloud-platform"]
  }
}

# Cloud Storage Bucket
resource "google_storage_bucket" "data" {
  name          = "${var.project_id}-${var.project_name}-data"
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }

  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }
}

# Cloud SQL Instance
resource "google_sql_database_instance" "main" {
  name             = "${var.project_name}-db"
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier              = var.db_tier
    availability_type = "REGIONAL"
    disk_size         = 100
    disk_type         = "PD_SSD"

    backup_configuration {
      enabled                        = true
      start_time                     = "03:00"
      point_in_time_recovery_enabled = true
      transaction_log_retention_days = 7
      backup_retention_settings {
        retained_backups = 30
      }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.main.id
    }
  }

  deletion_protection = true
}

# GKE Cluster
resource "google_container_cluster" "primary" {
  name     = "${var.project_name}-gke"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.app.name

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "${var.project_name}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = var.node_count

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  node_config {
    machine_type = var.node_machine_type
    disk_size_gb = 100
    disk_type    = "pd-standard"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      environment = var.environment
      project     = var.project_name
    }

    tags = ["gke-node", var.environment]
  }
}

# Cloud Function
resource "google_cloudfunctions_function" "processor" {
  name        = "${var.project_name}-processor"
  description = "Process data from storage"
  runtime     = "python311"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.functions.name
  source_archive_object = google_storage_bucket_object.function_code.name
  trigger_http          = true
  entry_point           = "process"

  environment_variables = {
    ENVIRONMENT = var.environment
    PROJECT_ID  = var.project_id
  }
}
```

## Kubernetes Provider

### Provider Configuration

```hcl
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

provider "kubernetes" {
  host                   = var.cluster_endpoint
  cluster_ca_certificate = base64decode(var.cluster_ca_cert)
  token                  = var.cluster_token
}
```

### Common Kubernetes Resources

```hcl
# Namespace
resource "kubernetes_namespace" "app" {
  metadata {
    name = var.namespace

    labels = {
      name        = var.namespace
      environment = var.environment
    }
  }
}

# Deployment
resource "kubernetes_deployment" "app" {
  metadata {
    name      = "${var.app_name}-deployment"
    namespace = kubernetes_namespace.app.metadata[0].name

    labels = {
      app         = var.app_name
      environment = var.environment
    }
  }

  spec {
    replicas = var.replica_count

    selector {
      match_labels = {
        app = var.app_name
      }
    }

    template {
      metadata {
        labels = {
          app         = var.app_name
          environment = var.environment
        }
      }

      spec {
        container {
          name  = var.app_name
          image = "${var.image_repository}:${var.image_tag}"

          port {
            container_port = var.container_port
          }

          env {
            name  = "ENVIRONMENT"
            value = var.environment
          }

          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }

          liveness_probe {
            http_get {
              path = "/health"
              port = var.container_port
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }

          readiness_probe {
            http_get {
              path = "/ready"
              port = var.container_port
            }
            initial_delay_seconds = 10
            period_seconds        = 5
          }
        }
      }
    }
  }
}

# Service
resource "kubernetes_service" "app" {
  metadata {
    name      = "${var.app_name}-service"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  spec {
    selector = {
      app = var.app_name
    }

    port {
      port        = 80
      target_port = var.container_port
    }

    type = "LoadBalancer"
  }
}

# ConfigMap
resource "kubernetes_config_map" "app" {
  metadata {
    name      = "${var.app_name}-config"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  data = {
    "config.json" = jsonencode({
      environment = var.environment
      log_level   = var.log_level
    })
  }
}

# Secret
resource "kubernetes_secret" "app" {
  metadata {
    name      = "${var.app_name}-secret"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  data = {
    database_password = base64encode(var.database_password)
    api_key          = base64encode(var.api_key)
  }

  type = "Opaque"
}

# Ingress
resource "kubernetes_ingress_v1" "app" {
  metadata {
    name      = "${var.app_name}-ingress"
    namespace = kubernetes_namespace.app.metadata[0].name

    annotations = {
      "kubernetes.io/ingress.class"                = "nginx"
      "cert-manager.io/cluster-issuer"            = "letsencrypt-prod"
      "nginx.ingress.kubernetes.io/ssl-redirect"  = "true"
    }
  }

  spec {
    tls {
      hosts = [var.domain_name]
      secret_name = "${var.app_name}-tls"
    }

    rule {
      host = var.domain_name

      http {
        path {
          path      = "/"
          path_type = "Prefix"

          backend {
            service {
              name = kubernetes_service.app.metadata[0].name
              port {
                number = 80
              }
            }
          }
        }
      }
    }
  }
}

# Horizontal Pod Autoscaler
resource "kubernetes_horizontal_pod_autoscaler_v2" "app" {
  metadata {
    name      = "${var.app_name}-hpa"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind        = "Deployment"
      name        = kubernetes_deployment.app.metadata[0].name
    }

    min_replicas = 2
    max_replicas = 10

    metric {
      type = "Resource"
      resource {
        name = "cpu"
        target {
          type                = "Utilization"
          average_utilization = 70
        }
      }
    }

    metric {
      type = "Resource"
      resource {
        name = "memory"
        target {
          type                = "Utilization"
          average_utilization = 80
        }
      }
    }
  }
}
```

---

## Reference: Terraform_Best_Practices

# Terraform Best Practices

## Project Structure

### Standard Project Layout

```
terraform-project/
├── main.tf              # Primary resource definitions
├── variables.tf         # Input variable declarations
├── outputs.tf           # Output value declarations
├── versions.tf          # Terraform and provider version constraints
├── terraform.tfvars     # Variable values (gitignored if sensitive)
├── backend.tf           # Backend configuration (optional)
├── locals.tf            # Local values (optional)
├── data.tf              # Data source definitions (optional)
└── modules/             # Local modules (optional)
    └── networking/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

### Multi-Environment Structure

```
terraform-project/
├── modules/             # Reusable modules
│   └── vpc/
├── environments/        # Environment-specific configurations
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── production/
└── shared/              # Shared resources
```

## Naming Conventions

### Resource Naming

- Use snake_case for all names
- Be descriptive but concise
- Include resource type when helpful
- Avoid redundant prefixes

```hcl
# Good
resource "aws_instance" "web_server" {}
resource "aws_security_group" "web_server_sg" {}

# Avoid
resource "aws_instance" "aws_instance_web" {}
resource "aws_security_group" "sg" {}
```

### Variable Naming

- Use descriptive names
- Include units in name when applicable
- Use consistent naming across modules

```hcl
# Good
variable "instance_count" {}
variable "backup_retention_days" {}
variable "enable_encryption" {}

# Avoid
variable "count" {}
variable "retention" {}
variable "encrypt" {}
```

## Version Pinning

### Terraform Version

```hcl
terraform {
  required_version = ">= 1.10, < 2.0"  # Baseline when using ephemeral features without write-only arguments
}
```

Version feature gates:
- Use `required_version = ">= 1.11, < 2.0"` when write-only arguments (`*_wo`) are used.
- Use `required_version = ">= 1.10, < 2.0"` for ephemeral-only configurations.
- If neither write-only nor ephemeral features are used, follow the repository baseline (for example `>= 1.8, < 2.0`).

### Provider Versions

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"  # Allow patch versions within major v6
    }
    random = {
      source  = "hashicorp/random"
      version = "3.5.1"   # Pin exact version if needed
    }
  }
}
```

Version policy:
- Prefer major-version pinning with `~>` across AWS/Azure/GCP providers.
- Avoid hardcoding "latest" numbers in static templates; verify current versions during execution when needed.

### Module Versions

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"  # Always pin module versions
  # ...
}
```

## State Management

### Remote Backend Configuration

```hcl
# Modern S3 backend with native locking (Terraform 1.11+)
terraform {
  backend "s3" {
    bucket       = "my-terraform-state"
    key          = "project/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true  # S3-native locking (recommended for 1.11+)
    kms_key_id   = "alias/terraform-state"
  }
}

# Legacy S3 backend with DynamoDB locking (Terraform < 1.11)
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "project/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"  # Deprecated in 1.11+
    kms_key_id     = "alias/terraform-state"
  }
}
```

### State Locking

Always use state locking for remote backends:
- S3: Use `use_lockfile = true` (Terraform 1.11+) or DynamoDB table (legacy)
- Azure Storage: Built-in locking
- GCS: Built-in locking

## Variable Management

### Variable Definitions

```hcl
variable "instance_type" {
  description = "EC2 instance type for web servers"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = can(regex("^t[23]\\.", var.instance_type))
    error_message = "Instance type must be from t2 or t3 family."
  }
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)

  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "At least 2 availability zones required."
  }
}
```

### Sensitive Variables

```hcl
variable "database_password" {
  description = "Password for database admin user"
  type        = string
  sensitive   = true
}

output "connection_string" {
  value     = "postgresql://user:${var.database_password}@${aws_db_instance.main.endpoint}"
  sensitive = true
}
```

### Variable Precedence

1. Environment variables (`TF_VAR_name`)
2. `terraform.tfvars` file
3. `terraform.tfvars.json` file
4. `*.auto.tfvars` files (alphabetical order)
5. `-var` and `-var-file` command-line flags
6. Default values in variable declarations

## Resource Management

### Dependencies

```hcl
# Implicit dependency (preferred)
resource "aws_eip" "example" {
  instance = aws_instance.web.id  # Implicit dependency
}

# Explicit dependency (when needed)
resource "aws_instance" "web" {
  # ...

  depends_on = [
    aws_iam_role_policy.example
  ]
}
```

### Lifecycle Rules

```hcl
resource "aws_instance" "web" {
  # ...

  lifecycle {
    create_before_destroy = true  # Create replacement before destroying
    prevent_destroy       = true  # Prevent accidental deletion
    ignore_changes = [            # Ignore external changes
      tags["LastModified"],
      user_data,
    ]
  }
}
```

### Provisioners (Use Sparingly)

```hcl
resource "aws_instance" "web" {
  # ...

  provisioner "local-exec" {
    command = "echo ${self.private_ip} >> private_ips.txt"

    on_failure = continue  # Continue if provisioner fails
  }

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }

    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
    ]
  }
}
```

## Data Sources

### Using Data Sources

```hcl
# Fetch latest AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]  # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Reference in resource
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
}

# Fetch availability zones
data "aws_availability_zones" "available" {
  state = "available"
}

# Use in resources
resource "aws_subnet" "private" {
  count             = length(data.aws_availability_zones.available.names)
  availability_zone = data.aws_availability_zones.available.names[count.index]
  # ...
}
```

## Local Values

### Using Locals

```hcl
locals {
  # Common tags
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
    CostCenter  = var.cost_center
  }

  # Computed values
  az_count        = length(data.aws_availability_zones.available.names)
  subnet_count    = var.subnet_count != null ? var.subnet_count : local.az_count

  # Complex expressions
  instance_name   = "${var.project_name}-${var.environment}-web"

  # Conditional values
  instance_type = var.environment == "production" ? "t3.large" : "t3.micro"

  # Map transformations
  subnet_cidrs = {
    for idx, az in data.aws_availability_zones.available.names :
    az => cidrsubnet(var.vpc_cidr, 8, idx)
  }
}
```

## Dynamic Blocks

### Dynamic Block Patterns

```hcl
# Dynamic ingress rules
resource "aws_security_group" "web" {
  name_prefix = "web-"
  vpc_id      = aws_vpc.main.id

  dynamic "ingress" {
    for_each = var.ingress_rules

    content {
      description = ingress.value.description
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }

  tags = local.common_tags
}

# Variable definition
variable "ingress_rules" {
  type = list(object({
    description = string
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))

  default = [
    {
      description = "HTTP"
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      description = "HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
}
```

## Count and For_Each

### Using Count

```hcl
# Create multiple similar resources
resource "aws_instance" "web" {
  count = var.instance_count

  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  subnet_id     = element(aws_subnet.private[*].id, count.index)

  tags = merge(
    local.common_tags,
    {
      Name = "${local.instance_name}-${count.index + 1}"
    }
  )
}
```

### Using For_Each

```hcl
# Create resources from map
resource "aws_iam_user" "users" {
  for_each = toset(var.user_names)

  name = each.value

  tags = {
    Team = lookup(var.user_teams, each.value, "default")
  }
}

# Create resources with different configurations
variable "environments" {
  type = map(object({
    instance_type = string
    instance_count = number
  }))

  default = {
    dev = {
      instance_type  = "t3.micro"
      instance_count = 1
    }
    prod = {
      instance_type  = "t3.large"
      instance_count = 3
    }
  }
}

resource "aws_instance" "env_servers" {
  # Build one instance object per environment and index
  for_each = merge([
    for env_name, env_cfg in var.environments : {
      for idx in range(env_cfg.instance_count) :
      "${env_name}-${idx + 1}" => {
        environment   = env_name
        instance_type = env_cfg.instance_type
        ordinal       = idx + 1
      }
    }
  ]...)

  ami           = data.aws_ami.ubuntu.id
  instance_type = each.value.instance_type

  tags = {
    Name        = "${each.value.environment}-server-${each.value.ordinal}"
    Environment = each.value.environment
  }
}
```

## Module Best Practices

### Module Structure

```
module/
├── main.tf              # Main resources
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── versions.tf          # Version constraints
├── README.md            # Documentation
└── examples/            # Usage examples
    └── complete/
        ├── main.tf
        └── variables.tf
```

### Module Input Variables

```hcl
# modules/vpc/variables.tf
variable "name" {
  description = "Name to be used on all resources"
  type        = string
}

variable "cidr" {
  description = "CIDR block for VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.cidr, 0))
    error_message = "Must be valid IPv4 CIDR."
  }
}

variable "enable_nat_gateway" {
  description = "Should be true to provision NAT Gateways"
  type        = bool
  default     = true
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}
```

### Module Outputs

```hcl
# modules/vpc/outputs.tf
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.this.id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.this.cidr_block
}

output "private_subnet_ids" {
  description = "List of IDs of private subnets"
  value       = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  description = "List of IDs of public subnets"
  value       = aws_subnet.public[*].id
}
```

### Using Modules

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "${var.project_name}-vpc"
  cidr = "10.0.0.0/16"

  azs             = data.aws_availability_zones.available.names
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = false

  tags = local.common_tags
}

# Reference module outputs
resource "aws_instance" "web" {
  subnet_id = module.vpc.private_subnet_ids[0]
  # ...
}
```

## Security Best Practices

### Secrets Management

```hcl
# NEVER hardcode secrets
# BAD
resource "aws_db_instance" "database" {
  password = "supersecretpassword"  # NEVER DO THIS
}

# GOOD - Use variables
variable "db_password" {
  type      = string
  sensitive = true
}

resource "aws_db_instance" "database" {
  password = var.db_password
}

# BETTER - Use secrets management service
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/password"
}

resource "aws_db_instance" "database" {
  password = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)["password"]
}
```

### Encryption

```hcl
# Enable encryption by default
resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.data.arn
    }
  }
}

# Encrypt EBS volumes
resource "aws_instance" "web" {
  # ...

  root_block_device {
    encrypted   = true
    kms_key_id  = aws_kms_key.data.arn
    volume_type = "gp3"
  }
}
```

### IAM Policies

```hcl
# Use least privilege principle
data "aws_iam_policy_document" "lambda_execution" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${var.function_name}:*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject"
    ]
    resources = [
      "${aws_s3_bucket.data.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "lambda_execution" {
  name   = "${var.function_name}-execution"
  policy = data.aws_iam_policy_document.lambda_execution.json
}
```

## Testing and Validation

### Input Validation

```hcl
variable "environment" {
  type = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_count" {
  type = number

  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

### Pre-commit Hooks

Use terraform fmt and terraform validate in pre-commit hooks:

```bash
#!/bin/bash
# .git/hooks/pre-commit

terraform fmt -check -recursive || exit 1
terraform validate || exit 1
```

## Documentation

### Code Comments

```hcl
# Create VPC for application infrastructure
# This VPC uses a /16 CIDR block to accommodate multiple subnets
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true  # Required for ECS task networking
  enable_dns_support   = true

  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-vpc"
    }
  )
}
```

### README Documentation

Include in project README:
- Purpose of the infrastructure
- Prerequisites
- Required variables
- Usage examples
- Output descriptions
- How to run terraform commands
- Maintenance notes

## Performance Optimization

### Parallel Resource Creation

Terraform automatically parallelizes resource creation when possible. Help it by:
- Avoiding unnecessary dependencies
- Using data sources efficiently
- Structuring modules properly

### State File Optimization

- Use targeted operations when possible: `terraform apply -target=resource`
- Split large configurations into multiple state files
- Use workspaces for similar environments
- Consider using `-refresh=false` when appropriate

### Provider Plugin Caching

```bash
# ~/.terraformrc or terraform.rc
plugin_cache_dir = "$HOME/.terraform.d/plugin-cache"
```

## Common Pitfalls to Avoid

1. **Hardcoding values** - Use variables and data sources
2. **Not pinning versions** - Always pin provider and module versions
3. **Ignoring state** - Never edit state files manually
4. **Circular dependencies** - Structure resources properly
5. **Overly complex modules** - Keep modules focused and simple
6. **Not using remote state** - Always use remote state for team collaboration
7. **Forgetting state locking** - Always use state locking mechanism
8. **Mixing concerns** - Separate infrastructure layers (network, compute, data)
9. **Not validating inputs** - Use validation blocks for variables
10. **Ignoring costs** - Tag resources appropriately for cost tracking
