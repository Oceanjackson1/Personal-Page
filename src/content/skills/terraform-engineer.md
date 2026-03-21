---
title: "Terraform Engineer"
description: "Use when implementing infrastructure as code with Terraform across AWS, Azure, or GCP. Invoke for module development (create reusable modules, manage module versioning), state management (migrate backends, import existing resources, resolve state ..."
category: "devops"
source: "community"
author: "Community"
tags: ["terraform", "engineer"]
date: 2026-03-20
---

# Terraform Engineer

Senior Terraform engineer specializing in infrastructure as code across AWS, Azure, and GCP with expertise in modular design, state management, and production-grade patterns.

## Core Workflow

1. **Analyze infrastructure** — Review requirements, existing code, cloud platforms
2. **Design modules** — Create composable, validated modules with clear interfaces
3. **Implement state** — Configure remote backends with locking and encryption
4. **Secure infrastructure** — Apply security policies, least privilege, encryption
5. **Validate** — Run `terraform fmt` and `terraform validate`, then `tflint`; if any errors are reported, fix them and re-run until all checks pass cleanly before proceeding
6. **Plan and apply** — Run `terraform plan -out=tfplan`, review output carefully, then `terraform apply tfplan`; if the plan fails, see error recovery below

### Error Recovery

**Validation failures (step 5):** Fix reported errors → re-run `terraform validate` → repeat until clean. For `tflint` warnings, address rule violations before proceeding.

**Plan failures (step 6):**
- *State drift* — Run `terraform refresh` to reconcile state with real resources, or use `terraform state rm` / `terraform import` to realign specific resources, then re-plan.
- *Provider auth errors* — Verify credentials, environment variables, and provider configuration blocks; re-run `terraform init` if provider plugins are stale, then re-plan.
- *Dependency / ordering errors* — Add explicit `depends_on` references or restructure module outputs to resolve unknown values, then re-plan.

After any fix, return to step 5 to re-validate before re-running the plan.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Modules | `references/module-patterns.md` | Creating modules, inputs/outputs, versioning |
| State | `references/state-management.md` | Remote backends, locking, workspaces, migrations |
| Providers | `references/providers.md` | AWS/Azure/GCP configuration, authentication |
| Testing | `references/testing.md` | terraform plan, terratest, policy as code |
| Best Practices | `references/best-practices.md` | DRY patterns, naming, security, cost tracking |

## Constraints

### MUST DO
- Use semantic versioning and pin provider versions
- Enable remote state with locking and encryption
- Validate inputs with validation blocks
- Use consistent naming conventions and tag all resources
- Document module interfaces
- Run `terraform fmt` and `terraform validate`

### MUST NOT DO
- Store secrets in plain text or hardcode environment-specific values
- Use local state for production or skip state locking
- Mix provider versions without constraints
- Create circular module dependencies or skip input validation
- Commit `.terraform` directories

## Code Examples

### Minimal Module Structure

**`main.tf`**
```hcl
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  tags   = var.tags
}
```

**`variables.tf`**
```hcl
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string

  validation {
    condition     = length(var.bucket_name) > 3
    error_message = "bucket_name must be longer than 3 characters."
  }
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
```

**`outputs.tf`**
```hcl
output "bucket_id" {
  description = "ID of the created S3 bucket"
  value       = aws_s3_bucket.this.id
}
```

### Remote Backend Configuration (S3 + DynamoDB)

```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "env/prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
```

### Provider Version Pinning

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}
```

## Output Format

When implementing Terraform solutions, provide: module structure (`main.tf`, `variables.tf`, `outputs.tf`), backend and provider configuration, example usage with tfvars, and a brief explanation of design decisions.

---

## Reference: Best Practices

# Terraform Best Practices

## DRY Principles

**Use Modules for Reusability**
```hcl
# Bad - Repeated code
resource "aws_vpc" "app1" {
  cidr_block = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "app1-vpc", Environment = "prod" }
}

resource "aws_vpc" "app2" {
  cidr_block = "10.1.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "app2-vpc", Environment = "prod" }
}

# Good - Use module
module "vpc_app1" {
  source = "./modules/vpc"

  name       = "app1"
  cidr_block = "10.0.0.0/16"
  environment = "prod"
}

module "vpc_app2" {
  source = "./modules/vpc"

  name       = "app2"
  cidr_block = "10.1.0.0/16"
  environment = "prod"
}
```

**Use Locals for Repeated Values**
```hcl
locals {
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_name
    CostCenter  = var.cost_center
  }

  name_prefix = "${var.project_name}-${var.environment}"

  # Computed locals
  vpc_cidr = var.environment == "production" ? "10.0.0.0/16" : "10.1.0.0/16"

  # Complex data structures
  availability_zones = slice(data.aws_availability_zones.available.names, 0, var.az_count)
}

resource "aws_vpc" "main" {
  cidr_block = local.vpc_cidr
  tags       = merge(local.common_tags, { Name = "${local.name_prefix}-vpc" })
}
```

**Use Data Sources Instead of Hardcoding**
```hcl
# Bad - Hardcoded AMI
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
}

# Good - Dynamic AMI lookup
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro"
}
```

**Use for_each for Multiple Similar Resources**
```hcl
# Bad - Duplicated resources
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"
}

# Good - Use for_each
variable "private_subnets" {
  type = map(object({
    cidr_block = string
    az         = string
  }))
  default = {
    subnet1 = { cidr_block = "10.0.1.0/24", az = "us-east-1a" }
    subnet2 = { cidr_block = "10.0.2.0/24", az = "us-east-1b" }
  }
}

resource "aws_subnet" "private" {
  for_each = var.private_subnets

  vpc_id            = aws_vpc.main.id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.az

  tags = {
    Name = "${var.name}-private-${each.key}"
  }
}
```

## Naming Conventions

**Resource Naming**
```hcl
# Pattern: {resource_type}_{descriptive_name}

# Good examples
resource "aws_vpc" "main" {}
resource "aws_subnet" "private" {}
resource "aws_security_group" "web" {}
resource "aws_instance" "app" {}

# Avoid generic names
resource "aws_vpc" "vpc" {}          # Bad
resource "aws_subnet" "subnet" {}    # Bad
resource "aws_vpc" "this" {}         # Use in modules only
```

**AWS Resource Name Tags**
```hcl
locals {
  # Pattern: {project}-{environment}-{resource}-{identifier}
  name_prefix = "${var.project_name}-${var.environment}"
}

resource "aws_vpc" "main" {
  cidr_block = var.cidr_block

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-vpc"
  })
}

resource "aws_subnet" "private" {
  for_each = var.private_subnets

  vpc_id     = aws_vpc.main.id
  cidr_block = each.value.cidr_block

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-private-${each.key}"
    Type = "private"
  })
}

resource "aws_security_group" "web" {
  name   = "${local.name_prefix}-web-sg"
  vpc_id = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-web-sg"
  })
}
```

**Variable Naming**
```hcl
# Use snake_case for all names
variable "instance_type" {}      # Good
variable "instanceType" {}       # Bad
variable "InstanceType" {}       # Bad

# Be descriptive
variable "vpc_cidr_block" {}     # Good
variable "cidr" {}               # Too vague

# Boolean variables should be questions
variable "enable_nat_gateway" {} # Good
variable "nat_gateway" {}        # Ambiguous

# Plural for lists/maps
variable "availability_zones" {} # Good
variable "private_subnets" {}    # Good
```

**File Naming**
```
# Standard structure
main.tf           # Primary resource definitions
variables.tf      # Input variables
outputs.tf        # Output values
versions.tf       # Terraform and provider versions
backend.tf        # Backend configuration (optional)
locals.tf         # Local values (optional)
data.tf           # Data sources (optional)

# Resource-specific files for complex modules
vpc.tf
subnets.tf
security_groups.tf
route_tables.tf
```

## Security Best Practices

**Secret Management**
```hcl
# Bad - Secrets in plain text
variable "db_password" {
  default = "SuperSecret123!"  # NEVER DO THIS
}

# Good - Use sensitive variables
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
  # No default - must be provided
}

# Better - Use secrets manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

**Encryption at Rest**
```hcl
# S3 bucket with encryption
resource "aws_s3_bucket" "data" {
  bucket = "my-data-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }
    bucket_key_enabled = true
  }
}

# EBS volume encryption
resource "aws_ebs_volume" "data" {
  availability_zone = "us-east-1a"
  size              = 100
  encrypted         = true
  kms_key_id        = aws_kms_key.ebs.arn
}

# RDS encryption
resource "aws_db_instance" "main" {
  storage_encrypted   = true
  kms_key_id          = aws_kms_key.rds.arn
}
```

**Least Privilege IAM**
```hcl
# Bad - Overly permissive
data "aws_iam_policy_document" "bad" {
  statement {
    effect    = "Allow"
    actions   = ["*"]
    resources = ["*"]
  }
}

# Good - Specific permissions
data "aws_iam_policy_document" "good" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject"
    ]
    resources = [
      "${aws_s3_bucket.data.arn}/*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.data.arn
    ]
  }
}
```

**Network Security**
```hcl
# Security group with restricted access
resource "aws_security_group" "web" {
  name        = "${var.name}-web-sg"
  description = "Security group for web servers"
  vpc_id      = aws_vpc.main.id

  # Bad - Too permissive
  # ingress {
  #   from_port   = 0
  #   to_port     = 65535
  #   protocol    = "tcp"
  #   cidr_blocks = ["0.0.0.0/0"]
  # }

  # Good - Specific rules
  ingress {
    description = "HTTPS from internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "All outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## Resource Tagging

**Consistent Tagging Strategy**
```hcl
locals {
  # Required tags for all resources
  required_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
    Project     = var.project_name
    CostCenter  = var.cost_center
    Owner       = var.owner_email
  }

  # Optional tags
  optional_tags = {
    Repository = "github.com/org/repo"
    Terraform  = "true"
  }

  # Merge all tags
  common_tags = merge(local.required_tags, local.optional_tags, var.additional_tags)
}

# Use provider default tags
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}

# Resource-specific tags
resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type

  tags = merge(local.common_tags, {
    Name = "${var.name}-app"
    Role = "application"
    Backup = "daily"
  })
}
```

## Cost Optimization

**Cost-Aware Resource Sizing**
```hcl
variable "environment" {
  type = string
}

locals {
  # Environment-based sizing
  instance_type = {
    production  = "t3.large"
    staging     = "t3.medium"
    development = "t3.micro"
  }

  rds_instance_class = {
    production  = "db.r5.xlarge"
    staging     = "db.t3.medium"
    development = "db.t3.micro"
  }

  enable_multi_az = var.environment == "production" ? true : false
}

resource "aws_instance" "app" {
  instance_type = local.instance_type[var.environment]
}

resource "aws_db_instance" "main" {
  instance_class = local.rds_instance_class[var.environment]
  multi_az       = local.enable_multi_az
}
```

**Lifecycle Management**
```hcl
resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type

  lifecycle {
    create_before_destroy = true
    prevent_destroy       = var.environment == "production"
    ignore_changes        = [ami, user_data]
  }
}

# S3 lifecycle rules for cost savings
resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "transition-to-ia"
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
  }
}
```

**Resource Scheduling**
```hcl
# Auto-scaling schedule for cost savings
resource "aws_autoscaling_schedule" "scale_down_evening" {
  scheduled_action_name  = "scale-down-evening"
  min_size               = 1
  max_size               = 1
  desired_capacity       = 1
  recurrence             = "0 20 * * MON-FRI"
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_schedule" "scale_up_morning" {
  scheduled_action_name  = "scale-up-morning"
  min_size               = 3
  max_size               = 10
  desired_capacity       = 3
  recurrence             = "0 7 * * MON-FRI"
  autoscaling_group_name = aws_autoscaling_group.app.name
}
```

## Code Organization

**Directory Structure**
```
terraform/
├── environments/
│   ├── production/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── development/
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── global/
│   ├── iam/
│   └── route53/
└── README.md
```

**Module Best Practices**
```hcl
# Keep modules small and focused
# modules/vpc/main.tf - Does ONE thing well

# Clear input/output contracts
# modules/vpc/variables.tf
variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
  validation { ... }
}

# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

# Version all modules
# modules/vpc/versions.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

## Best Practices Checklist

- [ ] Use remote state with locking
- [ ] Pin Terraform and provider versions
- [ ] Validate all input variables
- [ ] Use consistent naming conventions
- [ ] Tag all resources for cost tracking
- [ ] Encrypt sensitive data at rest and in transit
- [ ] Implement least privilege IAM policies
- [ ] Use modules for reusable components
- [ ] Document module interfaces
- [ ] Run terraform fmt before commit
- [ ] Run terraform validate in CI/CD
- [ ] Review plan output before apply
- [ ] Use data sources instead of hardcoding
- [ ] Implement automated testing
- [ ] Use for_each instead of count
- [ ] Avoid hardcoded secrets
- [ ] Enable logging and monitoring
- [ ] Implement cost optimization strategies
- [ ] Use lifecycle rules appropriately
- [ ] Keep modules focused and single-purpose

---

## Reference: Module Patterns

# Terraform Module Patterns

## Module Structure

```
terraform-aws-vpc/
├── main.tf           # Primary resource definitions
├── variables.tf      # Input variable declarations
├── outputs.tf        # Output value definitions
├── versions.tf       # Provider version constraints
├── README.md         # Module documentation
├── examples/
│   └── complete/
│       ├── main.tf
│       └── variables.tf
└── tests/
    └── vpc_test.go
```

## Basic Module Pattern

**main.tf**
```hcl
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support

  tags = merge(
    var.tags,
    {
      Name = var.name
    }
  )
}

resource "aws_subnet" "private" {
  for_each = var.private_subnets

  vpc_id            = aws_vpc.this.id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.az

  tags = merge(
    var.tags,
    {
      Name = "${var.name}-private-${each.key}"
      Type = "private"
    }
  )
}
```

**variables.tf**
```hcl
variable "name" {
  description = "Name prefix for all resources"
  type        = string

  validation {
    condition     = length(var.name) > 0 && length(var.name) <= 32
    error_message = "Name must be 1-32 characters"
  }
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string

  validation {
    condition     = can(cidrhost(var.cidr_block, 0))
    error_message = "Must be valid IPv4 CIDR block"
  }
}

variable "private_subnets" {
  description = "Map of private subnet configurations"
  type = map(object({
    cidr_block = string
    az         = string
  }))
  default = {}
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in VPC"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in VPC"
  type        = bool
  default     = true
}
```

**outputs.tf**
```hcl
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.this.cidr_block
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = { for k, v in aws_subnet.private : k => v.id }
}

output "private_subnet_cidrs" {
  description = "CIDR blocks of private subnets"
  value       = { for k, v in aws_subnet.private : k => v.cidr_block }
}
```

**versions.tf**
```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
```

## Module Composition

```hcl
# Composite module using child modules
module "networking" {
  source = "./modules/vpc"

  name       = "production"
  cidr_block = "10.0.0.0/16"

  private_subnets = {
    app1 = { cidr_block = "10.0.1.0/24", az = "us-east-1a" }
    app2 = { cidr_block = "10.0.2.0/24", az = "us-east-1b" }
  }

  tags = local.common_tags
}

module "security" {
  source = "./modules/security-groups"

  vpc_id = module.networking.vpc_id

  security_groups = {
    web = {
      ingress = [
        { from_port = 443, to_port = 443, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
      ]
    }
  }
}
```

## Dynamic Blocks

```hcl
resource "aws_security_group" "this" {
  name   = var.name
  vpc_id = var.vpc_id

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }

  dynamic "egress" {
    for_each = var.egress_rules
    content {
      from_port   = egress.value.from_port
      to_port     = egress.value.to_port
      protocol    = egress.value.protocol
      cidr_blocks = egress.value.cidr_blocks
      description = egress.value.description
    }
  }
}
```

## Conditional Resources

```hcl
# Create NAT gateway only if enabled
resource "aws_nat_gateway" "this" {
  count = var.enable_nat_gateway ? 1 : 0

  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.name}-nat"
  }

  depends_on = [aws_internet_gateway.this]
}

# Use for_each for multiple optional resources
resource "aws_route53_zone" "private" {
  for_each = var.create_private_zone ? { main = var.domain_name } : {}

  name = each.value

  vpc {
    vpc_id = aws_vpc.this.id
  }
}
```

## Module Versioning

```hcl
# Pin to specific version
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  # ... configuration
}

# Use version constraints
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"  # >= 19.0, < 20.0

  # ... configuration
}

# Reference Git tags
module "custom" {
  source = "git::https://github.com/org/terraform-modules.git//vpc?ref=v1.2.3"

  # ... configuration
}
```

## Module Testing Example

```hcl
# examples/complete/main.tf
module "vpc_test" {
  source = "../.."

  name       = "test-vpc"
  cidr_block = "10.100.0.0/16"

  private_subnets = {
    app = { cidr_block = "10.100.1.0/24", az = "us-east-1a" }
  }

  tags = {
    Environment = "test"
    ManagedBy   = "terraform"
  }
}

output "vpc_id" {
  value = module.vpc_test.vpc_id
}
```

## Best Practices

- Keep modules focused and single-purpose
- Use `for_each` over `count` for resources
- Validate all inputs with validation blocks
- Document all variables and outputs
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Provide complete examples
- Test modules before publishing
- Use consistent naming conventions
- Tag all taggable resources
- Avoid hardcoded values

---

## Reference: Providers

# Terraform Provider Configuration

## AWS Provider

**Basic Configuration**
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
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
```

**Multiple AWS Accounts/Regions**
```hcl
provider "aws" {
  alias  = "primary"
  region = "us-east-1"

  assume_role {
    role_arn     = "arn:aws:iam::123456789012:role/TerraformRole"
    session_name = "terraform-session"
  }
}

provider "aws" {
  alias  = "secondary"
  region = "us-west-2"

  assume_role {
    role_arn = "arn:aws:iam::987654321098:role/TerraformRole"
  }
}

# Use aliased provider
resource "aws_vpc" "primary" {
  provider   = aws.primary
  cidr_block = "10.0.0.0/16"
}

resource "aws_vpc" "secondary" {
  provider   = aws.secondary
  cidr_block = "10.1.0.0/16"
}
```

**AWS Authentication Methods**
```hcl
# Method 1: Environment variables (recommended for CI/CD)
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN

# Method 2: Shared credentials file
provider "aws" {
  region                   = "us-east-1"
  shared_credentials_files = ["~/.aws/credentials"]
  profile                  = "production"
}

# Method 3: IAM role (recommended for EC2/ECS)
provider "aws" {
  region = "us-east-1"
  # Automatically uses instance profile
}

# Method 4: Assume role
provider "aws" {
  region = "us-east-1"

  assume_role {
    role_arn     = var.terraform_role_arn
    session_name = "terraform-${var.environment}"
    external_id  = var.external_id
  }
}
```

**AWS Provider Features**
```hcl
provider "aws" {
  region = "us-east-1"

  # Default tags applied to all resources
  default_tags {
    tags = {
      Environment = "production"
      ManagedBy   = "Terraform"
      CostCenter  = "engineering"
    }
  }

  # Ignore specific tags (useful for auto-scaling)
  ignore_tags {
    keys = ["aws:autoscaling:groupName"]
  }

  # Custom endpoint for localstack/testing
  endpoints {
    s3  = "http://localhost:4566"
    ec2 = "http://localhost:4566"
  }

  # Rate limiting
  max_retries = 3

  # HTTP proxy
  http_proxy = "http://proxy.example.com:8080"
}
```

## Azure Provider (azurerm)

**Basic Configuration**
```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = true
    }

    key_vault {
      purge_soft_delete_on_destroy    = false
      recover_soft_deleted_key_vaults = true
    }

    virtual_machine {
      delete_os_disk_on_deletion     = true
      graceful_shutdown              = false
      skip_shutdown_and_force_delete = false
    }
  }

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}
```

**Multiple Azure Subscriptions**
```hcl
provider "azurerm" {
  alias           = "production"
  subscription_id = var.prod_subscription_id
  tenant_id       = var.tenant_id

  features {}
}

provider "azurerm" {
  alias           = "development"
  subscription_id = var.dev_subscription_id
  tenant_id       = var.tenant_id

  features {}
}

resource "azurerm_resource_group" "prod" {
  provider = azurerm.production
  name     = "prod-rg"
  location = "East US"
}
```

**Azure Authentication Methods**
```hcl
# Method 1: Service Principal with Client Secret
provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
  client_id       = var.client_id
  client_secret   = var.client_secret
}

# Method 2: Service Principal with Certificate
provider "azurerm" {
  features {}

  subscription_id             = var.subscription_id
  tenant_id                   = var.tenant_id
  client_id                   = var.client_id
  client_certificate_path     = var.client_certificate_path
  client_certificate_password = var.client_certificate_password
}

# Method 3: Managed Identity (for Azure VMs)
provider "azurerm" {
  features {}

  use_msi         = true
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id
}

# Method 4: Azure CLI (local development)
provider "azurerm" {
  features {}

  use_cli = true
}
```

## GCP Provider

**Basic Configuration**
```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone

  default_labels = {
    environment = var.environment
    managed_by  = "terraform"
  }
}
```

**Multiple GCP Projects**
```hcl
provider "google" {
  alias   = "production"
  project = var.prod_project_id
  region  = "us-central1"
}

provider "google" {
  alias   = "development"
  project = var.dev_project_id
  region  = "us-central1"
}

resource "google_compute_network" "prod" {
  provider = google.production
  name     = "prod-vpc"
}
```

**GCP Authentication Methods**
```hcl
# Method 1: Service Account Key (not recommended for production)
provider "google" {
  credentials = file("service-account-key.json")
  project     = var.project_id
  region      = var.region
}

# Method 2: Application Default Credentials (recommended)
provider "google" {
  # Uses GOOGLE_APPLICATION_CREDENTIALS env var
  project = var.project_id
  region  = var.region
}

# Method 3: Impersonate Service Account
provider "google" {
  project = var.project_id
  region  = var.region

  impersonate_service_account = "terraform@project-id.iam.gserviceaccount.com"
  scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email"
  ]
}

# Method 4: Workload Identity (for GKE)
provider "google" {
  project = var.project_id
  region  = var.region
  # Automatically uses workload identity
}
```

**GCP Beta Resources**
```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# Use beta provider for features not in stable
resource "google_compute_security_policy" "policy" {
  provider = google-beta
  name     = "my-policy"

  # Beta-only features here
}
```

## Kubernetes Provider

**With AWS EKS**
```hcl
data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_name
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}
```

**With GKE**
```hcl
data "google_client_config" "default" {}

data "google_container_cluster" "cluster" {
  name     = var.cluster_name
  location = var.region
}

provider "kubernetes" {
  host  = "https://${data.google_container_cluster.cluster.endpoint}"
  token = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(
    data.google_container_cluster.cluster.master_auth[0].cluster_ca_certificate
  )
}
```

## Helm Provider

```hcl
provider "helm" {
  kubernetes {
    host                   = data.aws_eks_cluster.cluster.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
    token                  = data.aws_eks_cluster_auth.cluster.token
  }
}

resource "helm_release" "nginx" {
  name       = "nginx-ingress"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  version    = "4.8.0"

  values = [
    file("${path.module}/values.yaml")
  ]

  set {
    name  = "controller.service.type"
    value = "LoadBalancer"
  }
}
```

## Provider Version Constraints

```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # >= 5.0.0, < 6.0.0
    }

    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0, < 4.0.0"
    }

    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }

    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

## Best Practices

- Always pin provider versions with constraints
- Use provider aliases for multi-region/account setups
- Leverage default tags for consistent resource tagging
- Use environment variables for credentials (CI/CD)
- Use IAM roles/managed identities when possible
- Never hardcode credentials in code
- Use separate providers for different environments
- Document provider requirements in README
- Test provider upgrades in non-production first
- Use official providers from HashiCorp registry

---

## Reference: State Management

# Terraform State Management

## Remote Backend - S3 (AWS)

**Backend Configuration**
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"

    # Optional: Enable versioning for state file history
    versioning = true
  }
}
```

**S3 Bucket Setup**
```hcl
# State bucket with versioning and encryption
resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-terraform-state"

  lifecycle {
    prevent_destroy = true
  }

  tags = {
    Name        = "Terraform State"
    Environment = "global"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_lock" {
  name           = "terraform-state-lock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform State Lock"
    Environment = "global"
  }
}
```

## Remote Backend - Azure Blob

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstatestorage"
    container_name       = "tfstate"
    key                  = "production.terraform.tfstate"

    # State locking is automatic with Azure Blob
    use_azuread_auth = true
  }
}
```

**Azure Storage Setup**
```hcl
resource "azurerm_resource_group" "terraform_state" {
  name     = "terraform-state-rg"
  location = "East US"
}

resource "azurerm_storage_account" "terraform_state" {
  name                     = "tfstatestorage"
  resource_group_name      = azurerm_resource_group.terraform_state.name
  location                 = azurerm_resource_group.terraform_state.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  enable_https_traffic_only = true
  min_tls_version          = "TLS1_2"

  blob_properties {
    versioning_enabled = true
  }

  tags = {
    environment = "global"
    purpose     = "terraform-state"
  }
}

resource "azurerm_storage_container" "terraform_state" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.terraform_state.name
  container_access_type = "private"
}
```

## Remote Backend - GCS (GCP)

```hcl
terraform {
  backend "gcs" {
    bucket = "my-terraform-state"
    prefix = "production/vpc"

    # State locking is automatic with GCS
  }
}
```

## Workspaces

**Using Workspaces**
```bash
# List workspaces
terraform workspace list

# Create new workspace
terraform workspace new staging

# Switch workspace
terraform workspace select production

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete dev
```

**Workspace-Aware Configuration**
```hcl
locals {
  environment = terraform.workspace

  # Environment-specific configuration
  vpc_cidr = {
    production = "10.0.0.0/16"
    staging    = "10.1.0.0/16"
    dev        = "10.2.0.0/16"
  }

  instance_count = {
    production = 5
    staging    = 2
    dev        = 1
  }
}

resource "aws_vpc" "main" {
  cidr_block = local.vpc_cidr[local.environment]

  tags = {
    Name        = "${local.environment}-vpc"
    Environment = local.environment
  }
}

resource "aws_instance" "app" {
  count = local.instance_count[local.environment]

  ami           = var.ami_id
  instance_type = "t3.micro"

  tags = {
    Name        = "${local.environment}-app-${count.index + 1}"
    Environment = local.environment
  }
}
```

## Partial Backend Configuration

**Backend template**
```hcl
# backend.tf
terraform {
  backend "s3" {
    # Configuration provided via backend config file or CLI
  }
}
```

**Environment-specific backend configs**
```hcl
# config/backend-prod.hcl
bucket         = "terraform-state-prod"
key            = "vpc/terraform.tfstate"
region         = "us-east-1"
encrypt        = true
dynamodb_table = "terraform-lock-prod"
```

```bash
# Initialize with backend config
terraform init -backend-config=config/backend-prod.hcl
```

## State Operations

**Import Existing Resources**
```bash
# Import AWS VPC
terraform import aws_vpc.main vpc-12345678

# Import with module
terraform import module.network.aws_vpc.main vpc-12345678
```

**State Manipulation**
```bash
# List resources in state
terraform state list

# Show resource details
terraform state show aws_vpc.main

# Move resource in state
terraform state mv aws_instance.old aws_instance.new

# Remove resource from state (doesn't destroy)
terraform state rm aws_instance.example

# Pull remote state to local file
terraform state pull > terraform.tfstate.backup

# Push local state to remote
terraform state push terraform.tfstate
```

**State Migration**
```bash
# Migrate from local to remote backend
terraform init -migrate-state

# Change backend configuration
terraform init -reconfigure

# Copy state to new backend
terraform init -backend-config=new-backend.hcl -migrate-state
```

## State Locking

**Manual Lock Management**
```bash
# Force unlock if lock is stuck (use carefully!)
terraform force-unlock LOCK_ID

# Example: terraform force-unlock a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Prevent Concurrent Modifications**
```hcl
# State locking happens automatically with supported backends
# DynamoDB for S3, automatic for Azure Blob and GCS

# Disable locking for specific operations (not recommended)
terraform apply -lock=false  # DON'T DO THIS IN PRODUCTION
```

## State File Security

**Encryption at Rest**
```hcl
# S3 bucket encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.terraform.arn
    }
    bucket_key_enabled = true
  }
}
```

**Access Control**
```hcl
# S3 bucket policy - restrict access
resource "aws_s3_bucket_policy" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "RequireEncryptedTransport"
        Effect = "Deny"
        Principal = "*"
        Action = "s3:*"
        Resource = [
          aws_s3_bucket.terraform_state.arn,
          "${aws_s3_bucket.terraform_state.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}
```

## State File Organization

```
# Recommended structure for multiple environments
terraform-state-bucket/
├── production/
│   ├── vpc/terraform.tfstate
│   ├── eks/terraform.tfstate
│   └── rds/terraform.tfstate
├── staging/
│   ├── vpc/terraform.tfstate
│   └── eks/terraform.tfstate
└── dev/
    └── vpc/terraform.tfstate
```

## Best Practices

- Always use remote state for teams
- Enable state locking to prevent conflicts
- Encrypt state files at rest and in transit
- Enable versioning for state file history
- Use separate state files per environment
- Restrict access to state buckets
- Back up state files regularly
- Never commit state files to git
- Use workspaces for similar environments only
- Document state migration procedures

---

## Reference: Testing

# Terraform Testing Strategies

## Terraform Plan Validation

**Basic Plan Workflow**
```bash
# Initialize and validate syntax
terraform init
terraform fmt -check
terraform validate

# Plan with output
terraform plan -out=tfplan

# Show plan in JSON for automated review
terraform show -json tfplan | jq .

# Apply specific plan
terraform apply tfplan
```

**Plan with Variable Files**
```bash
# Plan with specific tfvars
terraform plan -var-file="production.tfvars"

# Plan with inline variables
terraform plan -var="instance_count=5"

# Plan with multiple var files
terraform plan \
  -var-file="common.tfvars" \
  -var-file="production.tfvars"
```

**Plan Analysis**
```bash
# Resource targeting for specific resources
terraform plan -target=aws_vpc.main

# Refresh only (check drift)
terraform plan -refresh-only

# Destroy plan
terraform plan -destroy

# Save plan output
terraform plan -out=tfplan 2>&1 | tee plan-output.txt
```

## Terraform Test (1.6+)

**Test File Structure**
```
tests/
├── unit/
│   ├── vpc_test.tftest.hcl
│   └── security_group_test.tftest.hcl
└── integration/
    └── complete_test.tftest.hcl
```

**Basic Test**
```hcl
# tests/vpc_test.tftest.hcl
run "validate_vpc_cidr" {
  command = plan

  variables {
    cidr_block = "10.0.0.0/16"
    name       = "test-vpc"
  }

  assert {
    condition     = aws_vpc.main.cidr_block == "10.0.0.0/16"
    error_message = "VPC CIDR block did not match expected value"
  }

  assert {
    condition     = aws_vpc.main.enable_dns_hostnames == true
    error_message = "DNS hostnames should be enabled"
  }
}

run "validate_tags" {
  command = plan

  variables {
    cidr_block = "10.0.0.0/16"
    name       = "test-vpc"
    tags = {
      Environment = "test"
    }
  }

  assert {
    condition     = aws_vpc.main.tags["Environment"] == "test"
    error_message = "Environment tag not set correctly"
  }
}
```

**Integration Test**
```hcl
# tests/integration/complete_test.tftest.hcl
run "create_full_stack" {
  command = apply

  variables {
    cidr_block = "10.0.0.0/16"
    name       = "integration-test"

    private_subnets = {
      app = { cidr_block = "10.0.1.0/24", az = "us-east-1a" }
    }
  }

  assert {
    condition     = length(aws_subnet.private) == 1
    error_message = "Should create exactly one private subnet"
  }

  assert {
    condition     = output.vpc_id != ""
    error_message = "VPC ID should not be empty"
  }
}
```

**Run Tests**
```bash
# Run all tests
terraform test

# Run specific test file
terraform test tests/vpc_test.tftest.hcl

# Verbose output
terraform test -verbose

# Keep test resources (for debugging)
terraform test -no-cleanup
```

## Terratest (Go-based Testing)

**Test Structure**
```
tests/
├── go.mod
├── go.sum
└── vpc_test.go
```

**go.mod**
```go
module github.com/example/terraform-modules/tests

go 1.21

require (
    github.com/gruntwork-io/terratest v0.45.0
    github.com/stretchr/testify v1.8.4
)
```

**Basic Terratest**
```go
// tests/vpc_test.go
package test

import (
    "testing"

    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestVPCCreation(t *testing.T) {
    t.Parallel()

    terraformOptions := terraform.WithDefaultRetryableErrors(t, &terraform.Options{
        TerraformDir: "../examples/complete",

        Vars: map[string]interface{}{
            "name":       "test-vpc",
            "cidr_block": "10.0.0.0/16",
        },

        EnvVars: map[string]string{
            "AWS_DEFAULT_REGION": "us-east-1",
        },
    })

    defer terraform.Destroy(t, terraformOptions)

    terraform.InitAndApply(t, terraformOptions)

    vpcID := terraform.Output(t, terraformOptions, "vpc_id")
    assert.NotEmpty(t, vpcID)

    vpcCIDR := terraform.Output(t, terraformOptions, "vpc_cidr_block")
    assert.Equal(t, "10.0.0.0/16", vpcCIDR)
}
```

**Advanced Terratest with AWS SDK**
```go
package test

import (
    "testing"

    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/service/ec2"
    "github.com/gruntwork-io/terratest/modules/terraform"
    aws_helper "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/stretchr/testify/assert"
)

func TestVPCConfiguration(t *testing.T) {
    t.Parallel()

    awsRegion := "us-east-1"

    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/complete",
        Vars: map[string]interface{}{
            "name":       "test-vpc",
            "cidr_block": "10.0.0.0/16",
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    vpcID := terraform.Output(t, terraformOptions, "vpc_id")

    // Verify VPC configuration using AWS SDK
    vpc := aws_helper.GetVpcById(t, vpcID, awsRegion)
    assert.Equal(t, "10.0.0.0/16", *vpc.CidrBlock)
    assert.True(t, *vpc.EnableDnsSupport)
    assert.True(t, *vpc.EnableDnsHostnames)

    // Verify tags
    tags := convertEC2TagsToMap(vpc.Tags)
    assert.Equal(t, "test-vpc", tags["Name"])
}

func convertEC2TagsToMap(tags []*ec2.Tag) map[string]string {
    result := make(map[string]string)
    for _, tag := range tags {
        result[*tag.Key] = *tag.Value
    }
    return result
}
```

**Run Terratest**
```bash
cd tests
go mod download
go test -v -timeout 30m
```

## Policy as Code - OPA/Sentinel

**Open Policy Agent (OPA)**

**policy.rego**
```rego
package terraform.analysis

import input as tfplan

# Deny if resources are not tagged
deny[msg] {
    r := tfplan.resource_changes[_]
    r.change.actions[_] == "create"
    not r.change.after.tags.Environment
    msg := sprintf("Resource %s is missing Environment tag", [r.address])
}

# Require encryption for S3 buckets
deny[msg] {
    r := tfplan.resource_changes[_]
    r.type == "aws_s3_bucket"
    r.change.actions[_] == "create"
    not r.change.after.server_side_encryption_configuration
    msg := sprintf("S3 bucket %s must have encryption enabled", [r.address])
}

# Ensure VPC flow logs are enabled
deny[msg] {
    r := tfplan.resource_changes[_]
    r.type == "aws_vpc"
    r.change.actions[_] == "create"
    vpc_id := r.change.after.id
    not has_flow_log(vpc_id)
    msg := sprintf("VPC %s must have flow logs enabled", [r.address])
}

has_flow_log(vpc_id) {
    r := tfplan.resource_changes[_]
    r.type == "aws_flow_log"
    r.change.after.vpc_id == vpc_id
}
```

**Run OPA Policy**
```bash
# Generate plan in JSON
terraform plan -out=tfplan
terraform show -json tfplan > tfplan.json

# Run OPA policy check
opa eval -i tfplan.json -d policy.rego "data.terraform.analysis.deny"
```

**Conftest (OPA wrapper for testing)**
```bash
# Install conftest
brew install conftest

# Test plan against policies
conftest test tfplan.json

# With specific namespace
conftest test tfplan.json --namespace terraform.analysis
```

## TFLint

**Installation and Configuration**
```bash
# Install tflint
brew install tflint

# Initialize tflint plugins
tflint --init
```

**.tflint.hcl**
```hcl
plugin "terraform" {
  enabled = true
  preset  = "recommended"
}

plugin "aws" {
  enabled = true
  version = "0.27.0"
  source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

rule "terraform_naming_convention" {
  enabled = true

  format = "snake_case"
}

rule "terraform_required_version" {
  enabled = true
}

rule "terraform_required_providers" {
  enabled = true
}

rule "aws_instance_invalid_type" {
  enabled = true
}

rule "aws_s3_bucket_encryption" {
  enabled = true
}
```

**Run TFLint**
```bash
# Run linter
tflint

# With specific config
tflint --config=.tflint.hcl

# Recursive (all subdirectories)
tflint --recursive

# Output format
tflint --format=json
```

## Pre-commit Hooks

**.pre-commit-config.yaml**
```yaml
repos:
  - repo: https://github.com/antonbabenko/pre-commit-terraform
    rev: v1.83.6
    hooks:
      - id: terraform_fmt
      - id: terraform_validate
      - id: terraform_tflint
        args:
          - --args=--config=__GIT_WORKING_DIR__/.tflint.hcl
      - id: terraform_docs
        args:
          - --hook-config=--path-to-file=README.md
          - --hook-config=--add-to-existing-file=true
      - id: terraform_checkov
        args:
          - --args=--quiet
          - --args=--skip-check CKV_AWS_*
```

**Setup**
```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run -a
```

## CI/CD Pipeline Testing

**GitHub Actions Example**
```yaml
name: Terraform Test

on: [pull_request]

jobs:
  terraform-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.6.0

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init

      - name: Terraform Validate
        run: terraform validate

      - name: TFLint
        uses: terraform-linters/setup-tflint@v3
        with:
          tflint_version: latest

      - name: Run TFLint
        run: tflint --recursive

      - name: Terraform Test
        run: terraform test

      - name: Checkov
        uses: bridgecrewio/checkov-action@master
        with:
          directory: .
          framework: terraform
```

## Best Practices

- Run `terraform validate` before every commit
- Use `terraform test` for unit and integration tests
- Implement policy as code for security compliance
- Run TFLint in CI/CD pipelines
- Use pre-commit hooks for automated checks
- Test modules with Terratest for critical infrastructure
- Always review plan output before apply
- Test provider upgrades in isolated environments
- Document test scenarios and expected outcomes
- Automate testing in pull request workflows
