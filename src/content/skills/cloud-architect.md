---
title: "Cloud Architect"
description: "Designs cloud architectures, creates migration plans, generates cost optimization recommendations, and produces disaster recovery strategies across AWS, Azure, and GCP. Use when designing cloud architectures, planning migrations, or optimizing mul..."
category: "devops"
source: "community"
author: "Community"
tags: ["cloud", "architect"]
date: 2026-03-20
---

# Cloud Architect

## Core Workflow

1. **Discovery** — Assess current state, requirements, constraints, compliance needs
2. **Design** — Select services, design topology, plan data architecture
3. **Security** — Implement zero-trust, identity federation, encryption
4. **Cost Model** — Right-size resources, reserved capacity, auto-scaling
5. **Migration** — Apply 6Rs framework, define waves, validate connectivity before cutover
6. **Operate** — Set up monitoring, automation, continuous optimization

### Workflow Validation Checkpoints

**After Design:** Confirm every component has a redundancy strategy and no single points of failure exist in the topology.

**Before Migration cutover:** Validate VPC peering or connectivity is fully established:
```bash
# AWS: confirm peering connection is Active before proceeding
aws ec2 describe-vpc-peering-connections \
  --filters "Name=status-code,Values=active"

# Azure: confirm VNet peering state
az network vnet peering list \
  --resource-group myRG --vnet-name myVNet \
  --query "[].{Name:name,State:peeringState}"
```

**After Migration:** Verify application health and routing:
```bash
# AWS: check target group health in ALB
aws elbv2 describe-target-health \
  --target-group-arn arn:aws:elasticloadbalancing:...
```

**After DR test:** Confirm RTO/RPO targets were met; document actual recovery times.

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| AWS Services | `references/aws.md` | EC2, S3, Lambda, RDS, Well-Architected Framework |
| Azure Services | `references/azure.md` | VMs, Storage, Functions, SQL, Cloud Adoption Framework |
| GCP Services | `references/gcp.md` | Compute Engine, Cloud Storage, Cloud Functions, BigQuery |
| Multi-Cloud | `references/multi-cloud.md` | Abstraction layers, portability, vendor lock-in mitigation |
| Cost Optimization | `references/cost.md` | Reserved instances, spot, right-sizing, FinOps practices |

## Constraints

### MUST DO
- Design for high availability (99.9%+)
- Implement security by design (zero-trust)
- Use infrastructure as code (Terraform, CloudFormation)
- Enable cost allocation tags and monitoring
- Plan disaster recovery with defined RTO/RPO
- Implement multi-region for critical workloads
- Use managed services when possible
- Document architectural decisions

### MUST NOT DO
- Store credentials in code or public repos
- Skip encryption (at rest and in transit)
- Create single points of failure
- Ignore cost optimization opportunities
- Deploy without proper monitoring
- Use overly complex architectures
- Ignore compliance requirements
- Skip disaster recovery testing

## Common Patterns with Examples

### Least-Privilege IAM (Zero-Trust)

Rather than broad policies, scope permissions to specific resources and actions:

```bash
# AWS: create a scoped role for an application
aws iam create-role \
  --role-name AppRole \
  --assume-role-policy-document file://trust-policy.json

aws iam put-role-policy \
  --role-name AppRole \
  --policy-name AppInlinePolicy \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-app-bucket/*"
    }]
  }'
```

```hcl
# Terraform equivalent
resource "aws_iam_role" "app_role" {
  name               = "AppRole"
  assume_role_policy = data.aws_iam_policy_document.trust.json
}

resource "aws_iam_role_policy" "app_policy" {
  role = aws_iam_role.app_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject", "s3:PutObject"]
      Resource = "${aws_s3_bucket.app.arn}/*"
    }]
  })
}
```

### VPC with Public/Private Subnets (Terraform)

```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "main", CostCenter = var.cost_center }
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet("10.0.0.0/16", 8, count.index)
  availability_zone = data.aws_availability_zones.available.names[count.index]
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet("10.0.0.0/16", 8, count.index + 10)
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
}
```

### Auto-Scaling Group (Terraform)

```hcl
resource "aws_autoscaling_group" "app" {
  desired_capacity    = 2
  min_size            = 1
  max_size            = 10
  vpc_zone_identifier = aws_subnet.private[*].id

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "CostCenter"
    value               = var.cost_center
    propagate_at_launch = true
  }
}

resource "aws_autoscaling_policy" "cpu_target" {
  autoscaling_group_name = aws_autoscaling_group.app.name
  policy_type            = "TargetTrackingScaling"
  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 60.0
  }
}
```

### Cost Analysis CLI

```bash
# AWS: identify top cost drivers for the last 30 days
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '30 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --query 'ResultsByTime[0].Groups[*].{Service:Keys[0],Cost:Metrics.UnblendedCost.Amount}' \
  --output table

# Azure: review spend by resource group
az consumption usage list \
  --start-date $(date -d '30 days ago' +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d) \
  --query "[].{ResourceGroup:resourceGroup,Cost:pretaxCost,Currency:currency}" \
  --output table
```

## Output Templates

When designing cloud architecture, provide:
1. Architecture diagram with services and data flow
2. Service selection rationale (compute, storage, database, networking)
3. Security architecture (IAM, network segmentation, encryption)
4. Cost estimation and optimization strategy
5. Deployment approach and rollback plan

---

## Reference: Aws

# AWS Architecture Reference

Comprehensive guide for AWS services, patterns, and Well-Architected Framework implementation.

## Well-Architected Framework

### Six Pillars

1. **Operational Excellence**
   - Infrastructure as Code (CloudFormation, CDK, Terraform)
   - Continuous integration/deployment
   - Observability (CloudWatch, X-Ray)
   - Runbooks and playbooks
   - Game days and failure injection

2. **Security**
   - Identity and Access Management (IAM)
   - Detective controls (GuardDuty, Security Hub)
   - Infrastructure protection (VPC, security groups, NACLs)
   - Data protection (KMS, encryption at rest/transit)
   - Incident response automation

3. **Reliability**
   - Multi-AZ deployments
   - Auto Scaling groups
   - Route 53 health checks and failover
   - Backup and restore (AWS Backup)
   - Chaos engineering (AWS FIS)

4. **Performance Efficiency**
   - Right-sizing with Compute Optimizer
   - Caching strategies (CloudFront, ElastiCache)
   - Database optimization (RDS Performance Insights)
   - Serverless architectures
   - Global content delivery

5. **Cost Optimization**
   - Reserved Instances and Savings Plans
   - Spot Instances for fault-tolerant workloads
   - S3 Intelligent-Tiering and lifecycle policies
   - Right-sizing recommendations
   - Cost allocation tags and budgets

6. **Sustainability**
   - Region selection for renewable energy
   - Serverless to minimize idle resources
   - Efficient data storage patterns
   - Resource utilization optimization

## Core Services Architecture

### Compute

**EC2 (Elastic Compute Cloud)**
- Instance families: General (t3, m5), Compute (c5), Memory (r5), GPU (p3, g4)
- Auto Scaling: Target tracking, step scaling, scheduled scaling
- Placement groups: Cluster, partition, spread
- Best practices: Use latest generation, right-size, enable detailed monitoring

**Lambda**
- Invocation models: Synchronous, asynchronous, event source mapping
- Concurrency: Reserved, provisioned, burst limits
- Layers for shared dependencies
- Best practices: Keep functions small, use environment variables, set timeouts

**ECS/EKS (Container Services)**
- ECS: Fargate for serverless, EC2 for control
- EKS: Managed Kubernetes with AWS integration
- Service mesh: App Mesh for observability
- Best practices: Use Fargate for simplicity, EKS for portability

**Elastic Beanstalk**
- Managed platform for web apps
- Auto-scaling and load balancing included
- Support for multiple languages and Docker

### Storage

**S3 (Simple Storage Service)**
- Storage classes: Standard, IA, One Zone-IA, Glacier, Deep Archive
- Lifecycle policies for automatic tiering
- Versioning and MFA delete for protection
- Cross-region replication for DR
- Best practices: Enable versioning, use lifecycle policies, block public access

**EBS (Elastic Block Store)**
- Volume types: gp3 (general), io2 (IOPS), st1 (throughput), sc1 (cold)
- Snapshots to S3 for backup
- Encryption by default
- Best practices: Use gp3 for most workloads, enable encryption

**EFS (Elastic File System)**
- NFSv4 file system for shared access
- Performance modes: General purpose, Max I/O
- Throughput modes: Bursting, provisioned
- Best practices: Use lifecycle management, enable encryption

**FSx**
- FSx for Windows File Server (SMB)
- FSx for Lustre (HPC workloads)
- FSx for NetApp ONTAP
- FSx for OpenZFS

### Database

**RDS (Relational Database Service)**
- Engines: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora
- Multi-AZ for high availability
- Read replicas for scalability
- Automated backups and point-in-time recovery
- Best practices: Use Aurora for performance, enable Multi-AZ, use read replicas

**Aurora**
- MySQL and PostgreSQL compatible
- 5x MySQL, 3x PostgreSQL performance
- Global databases for cross-region DR
- Serverless v2 for variable workloads
- Best practices: Use Aurora Serverless for unpredictable workloads

**DynamoDB**
- NoSQL key-value and document database
- On-demand or provisioned capacity
- Global tables for multi-region replication
- DynamoDB Streams for change data capture
- Best practices: Use on-demand for unpredictable traffic, implement GSI carefully

**ElastiCache**
- Redis or Memcached in-memory caching
- Cluster mode for Redis scalability
- Best practices: Use for session storage, API caching

### Networking

**VPC (Virtual Private Cloud)**
- CIDR planning: Avoid overlaps, plan for growth
- Subnets: Public (IGW), private (NAT), isolated (no internet)
- Route tables and routing decisions
- Security groups (stateful) and NACLs (stateless)
- Best practices: Use /16 for VPC, /24 for subnets, plan IP space

**Route 53**
- DNS service with health checks
- Routing policies: Simple, weighted, latency, failover, geolocation
- Best practices: Use alias records, enable DNSSEC

**CloudFront**
- Global CDN with edge locations
- Origin types: S3, ALB, custom origins
- Lambda@Edge for request/response manipulation
- Best practices: Enable compression, use field-level encryption

**VPN and Direct Connect**
- Site-to-Site VPN for encrypted tunnels
- Direct Connect for dedicated bandwidth
- Transit Gateway for hub-and-spoke topology
- Best practices: Use Direct Connect for high bandwidth, Transit Gateway for complex routing

**API Gateway**
- REST APIs, HTTP APIs, WebSocket APIs
- Throttling and quotas
- Integration with Lambda, HTTP endpoints, AWS services
- Best practices: Use HTTP APIs for lower cost, implement caching

### Security

**IAM (Identity and Access Management)**
- Principle of least privilege
- Roles for applications, not access keys
- MFA for privileged users
- Service Control Policies (SCPs) for organization-wide controls
- Best practices: Use roles, enable MFA, rotate credentials

**KMS (Key Management Service)**
- Customer managed keys (CMKs)
- Automatic key rotation
- Envelope encryption pattern
- Best practices: Enable automatic rotation, use grants for temporary access

**Secrets Manager**
- Automatic rotation for RDS credentials
- Versioning and rollback
- Best practices: Rotate secrets regularly, use VPC endpoints

**Security Hub**
- Centralized security findings
- CIS AWS Foundations Benchmark
- Integration with GuardDuty, Inspector, Macie

**GuardDuty**
- Threat detection using ML
- Monitors CloudTrail, VPC Flow Logs, DNS logs

## Architecture Patterns

### High Availability

**Multi-AZ Pattern**
```
- Application Load Balancer across 3 AZs
- Auto Scaling group with instances in each AZ
- RDS Multi-AZ for database
- S3 for static assets (11 9's durability)
```

**Multi-Region Pattern**
```
- Route 53 with health checks and failover
- CloudFront for global distribution
- Aurora Global Database for <1s RPO
- S3 Cross-Region Replication
```

### Serverless Architecture

**API-Driven Pattern**
```
API Gateway -> Lambda -> DynamoDB
              |
              v
          EventBridge -> Lambda (async processing)
```

**Event-Driven Pattern**
```
S3 Event -> Lambda -> Process -> SNS
                                  |
                                  v
                              Multiple subscribers
```

### Microservices on AWS

**Container-Based**
```
ALB -> ECS Fargate (multiple services)
    |
    v
Service Discovery (Cloud Map)
    |
    v
RDS/DynamoDB per service
```

**Service Mesh**
```
App Mesh for traffic management
X-Ray for distributed tracing
CloudWatch Container Insights
```

### Data Lake Architecture

```
Data Sources -> Kinesis Data Streams
                      |
                      v
              Kinesis Firehose
                      |
                      v
                S3 (raw bucket)
                      |
                      v
        Glue ETL or Lambda processing
                      |
                      v
            S3 (processed bucket)
                      |
                      v
          Athena/Redshift Spectrum
                      |
                      v
              QuickSight dashboards
```

## Migration Strategies (6Rs)

1. **Rehost (Lift-and-Shift)**
   - AWS Application Migration Service (MGN)
   - Minimal changes, quick migration
   - Use for legacy apps with compliance constraints

2. **Replatform (Lift-Tinker-and-Shift)**
   - Migrate to RDS instead of self-managed databases
   - Use Elastic Beanstalk instead of custom app servers
   - Small optimizations during migration

3. **Repurchase (Drop-and-Shop)**
   - Move to SaaS (e.g., Salesforce, Workday)
   - Reduce maintenance burden

4. **Refactor/Re-architect**
   - Modernize to serverless or containers
   - Highest effort, highest benefit
   - Use for competitive advantage applications

5. **Retire**
   - Decommission unused applications
   - Reduce attack surface and costs

6. **Retain**
   - Keep on-premises temporarily
   - Migrate later or keep for regulatory reasons

## Landing Zone Design

**AWS Control Tower**
- Multi-account strategy (AWS Organizations)
- Account factory for standardization
- Guardrails for governance (SCPs)
- Centralized logging (CloudTrail, Config)

**Account Structure**
```
Root
├── Security OU
│   ├── Log Archive Account
│   └── Security Tooling Account
├── Infrastructure OU
│   ├── Network Account (Transit Gateway, VPN)
│   └── Shared Services Account
└── Workloads OU
    ├── Production Account
    ├── Staging Account
    └── Development Account
```

**Network Design**
```
Transit Gateway (hub)
    |
    ├── Production VPC
    ├── Staging VPC
    ├── Development VPC
    └── On-premises (Direct Connect/VPN)
```

## Cost Optimization Strategies

**Compute Savings**
- Compute Savings Plans (up to 66% savings)
- EC2 Reserved Instances (1-year or 3-year)
- Spot Instances for batch/fault-tolerant workloads
- Lambda: Reduce memory if possible, use reserved concurrency

**Storage Savings**
- S3 Intelligent-Tiering for unpredictable access
- Lifecycle policies to Glacier/Deep Archive
- EBS gp3 instead of gp2 (20% cheaper, better performance)
- Delete unused snapshots and volumes

**Database Savings**
- Aurora Serverless v2 for variable workloads
- RDS Reserved Instances
- DynamoDB on-demand for unpredictable workloads
- Read replicas in same region to reduce cross-AZ data transfer

**Monitoring and Alerting**
- AWS Cost Explorer for analysis
- AWS Budgets for alerts
- Cost Anomaly Detection
- Trusted Advisor for recommendations

## Disaster Recovery

**RPO and RTO Targets**
- Backup and Restore: Hours RPO/RTO (lowest cost)
- Pilot Light: Minutes RPO, hours RTO
- Warm Standby: Seconds RPO, minutes RTO
- Multi-Site Active/Active: Near-zero RPO/RTO (highest cost)

**Implementation**
- AWS Backup for centralized backup management
- Aurora Global Database for cross-region replication
- S3 Cross-Region Replication
- Route 53 health checks and failover routing
- Regular DR testing with CloudFormation/Terraform

## Monitoring and Observability

**CloudWatch**
- Metrics: Standard (5 min) and detailed (1 min)
- Alarms with SNS notifications
- Logs Insights for log analysis
- Dashboards for visualization

**X-Ray**
- Distributed tracing for microservices
- Service map visualization
- Trace annotations and metadata

**AWS Config**
- Resource inventory and change tracking
- Compliance rules evaluation
- Relationship tracking between resources

---

## Reference: Azure

# Azure Architecture Reference

Comprehensive guide for Azure services, patterns, and Cloud Adoption Framework implementation.

## Cloud Adoption Framework

### Framework Phases

1. **Strategy**
   - Define business justification
   - Expected business outcomes
   - Business case development
   - First project prioritization

2. **Plan**
   - Digital estate assessment
   - Initial organization alignment
   - Skills readiness plan
   - Cloud adoption plan

3. **Ready**
   - Azure landing zone setup
   - Azure setup guide
   - Migration readiness
   - Best practices validation

4. **Adopt (Migrate + Innovate)**
   - Migration: Assess, migrate, optimize
   - Innovate: Build cloud-native solutions
   - Best practices and patterns

5. **Govern**
   - Methodology for governance
   - Governance benchmark
   - Initial governance foundation
   - Mature governance evolution

6. **Manage**
   - Business commitments
   - Operations baseline
   - Platform and workload specialization

## Azure Well-Architected Framework

### Five Pillars

1. **Cost Optimization**
   - Azure Cost Management and Billing
   - Reserved instances and Savings Plans
   - Azure Hybrid Benefit
   - Auto-scaling and right-sizing

2. **Operational Excellence**
   - Infrastructure as Code (ARM, Bicep, Terraform)
   - Azure DevOps and GitHub Actions
   - Azure Monitor and Application Insights
   - Deployment slots and blue-green deployments

3. **Performance Efficiency**
   - Azure CDN and Front Door
   - Auto-scaling (VMSS, App Service)
   - Caching (Redis, CDN)
   - Performance diagnostics

4. **Reliability**
   - Availability Zones and regions
   - Azure Site Recovery
   - Load Balancer and Traffic Manager
   - Backup and disaster recovery

5. **Security**
   - Azure AD (Entra ID)
   - Network Security Groups and Firewalls
   - Azure Key Vault
   - Microsoft Defender for Cloud

## Core Services Architecture

### Compute

**Virtual Machines**
- VM sizes: General (D-series), Compute (F-series), Memory (E-series), GPU (N-series)
- Availability Sets (99.95% SLA)
- Availability Zones (99.99% SLA)
- VM Scale Sets for auto-scaling
- Best practices: Use managed disks, enable accelerated networking, use proximity placement groups

**App Service**
- Web Apps, API Apps, Mobile Apps
- Deployment slots for staging
- Auto-scaling based on metrics or schedule
- Supports .NET, Java, Node.js, Python, PHP, Ruby
- Best practices: Use deployment slots, enable auto-scaling, use App Service Plan efficiently

**Azure Functions**
- Consumption Plan (serverless)
- Premium Plan (VNet integration, no cold start)
- Dedicated Plan (App Service Plan)
- Durable Functions for orchestration
- Best practices: Keep functions small, use Premium for production, implement retry policies

**Azure Kubernetes Service (AKS)**
- Managed Kubernetes control plane
- Azure CNI or kubenet networking
- Azure AD integration
- Virtual nodes (Azure Container Instances)
- Best practices: Use system node pools, enable autoscaling, implement network policies

**Container Instances**
- Serverless containers
- Fast startup without infrastructure management
- Best for batch jobs and burstable workloads

**Azure Batch**
- Large-scale parallel and HPC workloads
- Auto-scaling compute nodes
- Task scheduling and dependencies

### Storage

**Blob Storage**
- Storage tiers: Hot, Cool, Archive
- Access tiers: Premium, Standard
- Lifecycle management policies
- Immutable storage for compliance
- Best practices: Use lifecycle policies, enable soft delete, implement versioning

**Azure Files**
- SMB and NFS file shares
- Integration with Azure File Sync
- Premium tier for high performance
- Best practices: Use Premium for databases, implement snapshots

**Disk Storage**
- Managed Disks: Premium SSD, Standard SSD, Standard HDD, Ultra Disk
- Disk encryption with Azure Disk Encryption
- Snapshots and incremental backups
- Best practices: Use Premium SSD for production, enable encryption

**Data Lake Storage Gen2**
- Hierarchical namespace for big data
- Built on Blob Storage
- Integration with Azure Synapse and Databricks
- Best practices: Enable hierarchical namespace, use lifecycle policies

**Azure NetApp Files**
- Enterprise-grade NFS and SMB shares
- High performance and low latency
- Snapshots and data protection

### Database

**Azure SQL Database**
- Serverless and provisioned compute
- Hyperscale for up to 100TB
- Elastic pools for multiple databases
- Auto-tuning and intelligent insights
- Best practices: Use serverless for dev/test, enable geo-replication

**Azure SQL Managed Instance**
- Near 100% compatibility with SQL Server
- VNet integration for isolation
- Native virtual network implementation
- Best practices: Use for lift-and-shift migrations

**Cosmos DB**
- Multi-model NoSQL database
- Global distribution with multi-master
- Consistency levels: Strong, Bounded staleness, Session, Consistent prefix, Eventual
- APIs: SQL, MongoDB, Cassandra, Gremlin, Table
- Best practices: Choose appropriate consistency, partition key design critical

**Azure Database for PostgreSQL/MySQL/MariaDB**
- Flexible Server (newer) vs Single Server (legacy)
- High availability with zone redundancy
- Read replicas for scaling
- Best practices: Use Flexible Server, enable HA, implement connection pooling

**Azure Cache for Redis**
- In-memory caching
- Clustering for scalability
- Geo-replication for disaster recovery
- Best practices: Use Premium tier for production, enable persistence

### Networking

**Virtual Network (VNet)**
- CIDR planning (avoid overlaps)
- Subnets with Network Security Groups
- Service endpoints and Private Link
- VNet peering for connectivity
- Best practices: Plan IP address space, use NSGs, implement Private Link

**Azure Load Balancer**
- Layer 4 load balancing
- Standard SKU (zone-redundant, SLA)
- Health probes and distribution algorithms
- Best practices: Use Standard SKU, configure health probes

**Application Gateway**
- Layer 7 load balancing
- WAF (Web Application Firewall)
- URL-based routing and SSL termination
- Best practices: Enable WAF, use autoscaling

**Azure Front Door**
- Global load balancing and CDN
- WAF at edge
- Anycast for low latency
- Best practices: Use for global applications, enable caching

**VPN Gateway and ExpressRoute**
- Site-to-Site VPN for encrypted connectivity
- ExpressRoute for private, dedicated connection
- Virtual WAN for global transit network
- Best practices: Use ExpressRoute for production, implement redundancy

**Azure Firewall**
- Managed firewall service
- Application and network rules
- Threat intelligence
- Best practices: Use in hub-spoke topology, enable DNS proxy

**Azure Private Link**
- Private connectivity to Azure services
- No public internet exposure
- Available for PaaS services
- Best practices: Use for all PaaS services in production

### Security and Identity

**Azure Active Directory (Microsoft Entra ID)**
- Identity and access management
- Conditional Access policies
- Multi-factor authentication
- B2B and B2C scenarios
- Best practices: Enable MFA, use Conditional Access, implement PIM

**Azure Key Vault**
- Secrets, keys, and certificates management
- Hardware Security Module (HSM) backed
- Soft delete and purge protection
- Best practices: Enable soft delete, use RBAC, implement Private Link

**Microsoft Defender for Cloud**
- Security posture management
- Threat protection for hybrid workloads
- Regulatory compliance dashboard
- Just-in-time VM access
- Best practices: Enable enhanced security, implement recommendations

**Azure Policy**
- Governance and compliance at scale
- Built-in and custom policies
- Deny, audit, append effects
- Best practices: Assign at management group level, test before enforce

**Azure Sentinel**
- Cloud-native SIEM and SOAR
- AI-powered threat detection
- Integration with Microsoft 365, third-party tools
- Best practices: Enable data connectors, create custom analytics rules

## Architecture Patterns

### High Availability

**Zone-Redundant Pattern**
```
Azure Front Door (global)
    |
    v
Application Gateway (zone-redundant)
    |
    v
VM Scale Set (across availability zones)
    |
    v
Azure SQL Database (zone-redundant)
```

**Multi-Region Pattern**
```
Azure Traffic Manager (DNS-based routing)
    |
    ├── Region 1: App Service + SQL Database (primary)
    └── Region 2: App Service + SQL Database (geo-replica)
```

### Hub-Spoke Topology

```
Hub VNet
├── Azure Firewall
├── VPN Gateway
└── Shared Services
    |
    ├── Spoke VNet 1 (Production)
    ├── Spoke VNet 2 (Development)
    └── Spoke VNet 3 (DMZ)
```

### Serverless Architecture

**Event-Driven Pattern**
```
Event Grid -> Azure Functions -> Cosmos DB
                    |
                    v
              Service Bus -> Functions (processing)
```

**API-First Pattern**
```
API Management
    |
    ├── Function App 1 (auth)
    ├── Function App 2 (business logic)
    └── Function App 3 (data access)
```

### Microservices on Azure

**AKS-Based**
```
Azure Front Door
    |
    v
Application Gateway + WAF
    |
    v
AKS (multiple microservices)
    |
    ├── Cosmos DB (microservice A)
    ├── SQL Database (microservice B)
    └── Service Bus (async communication)
```

**Container Apps Pattern**
```
Azure Container Apps
├── Dapr for state management
├── KEDA for event-driven scaling
└── Azure Monitor for observability
```

### Data Platform

```
Data Sources
    |
    v
Event Hubs / IoT Hub
    |
    v
Stream Analytics (real-time processing)
    |
    v
Data Lake Storage Gen2
    |
    v
Azure Synapse Analytics
    |
    v
Power BI (visualization)
```

## Landing Zone Design

### Enterprise-Scale Landing Zone

**Management Group Hierarchy**
```
Tenant Root Group
├── Platform
│   ├── Management (monitoring, automation)
│   ├── Connectivity (hub networks, VPN)
│   └── Identity (domain controllers)
└── Landing Zones
    ├── Corp (internal workloads)
    └── Online (internet-facing workloads)
```

**Network Topology**
```
Hub VNet (Connectivity subscription)
├── Azure Firewall
├── VPN Gateway
├── ExpressRoute Gateway
└── Bastion

Spoke VNets (Workload subscriptions)
├── Production VNet
├── Staging VNet
└── Development VNet
```

**Governance**
- Azure Policy for compliance
- Management groups for hierarchy
- RBAC assignments at appropriate scope
- Resource tags for cost allocation
- Azure Blueprints for repeatable deployments

## Migration Strategies

### Azure Migrate

1. **Assess**
   - Discovery with Azure Migrate appliance
   - Dependency analysis
   - Performance-based sizing
   - Cost estimation

2. **Migrate**
   - Azure Migrate: Server Migration (agentless)
   - Database Migration Service
   - App Service Migration Assistant
   - Data Box for large data transfers

3. **Optimize**
   - Right-sizing recommendations
   - Reserved instances
   - Azure Hybrid Benefit

### Migration Patterns

**Rehost**: Azure Migrate for VMs
**Replatform**: App Service, Azure SQL Database
**Refactor**: Container Apps, AKS, Functions
**Rebuild**: Azure-native services (Cosmos DB, Cognitive Services)

## Cost Optimization

### Compute Savings
- Azure Reserved Instances (1-year or 3-year, up to 72% savings)
- Azure Savings Plans for Compute (up to 65% savings)
- Spot VMs for fault-tolerant workloads (up to 90% savings)
- Azure Hybrid Benefit (use existing Windows Server/SQL licenses)
- Auto-shutdown for dev/test VMs

### Storage Savings
- Blob Storage lifecycle policies (Hot -> Cool -> Archive)
- Azure Files: Standard tier for general use
- Managed Disks: Standard SSD instead of Premium if possible
- Delete unused snapshots and disks

### Database Savings
- Serverless tier for Azure SQL Database
- Reserved capacity for Cosmos DB
- DTU model vs vCore (choose based on workload)
- Pause Azure Synapse when not in use

### Monitoring
- Azure Cost Management + Billing
- Cost alerts and budgets
- Azure Advisor recommendations
- Resource tagging for cost allocation

## Disaster Recovery

### Azure Site Recovery

**VM Replication**
- Azure to Azure replication
- On-premises to Azure (VMware, Hyper-V, physical)
- RPO: 30 seconds to a few minutes
- Automated failover and failback

**Recovery Plans**
- Multi-tier application recovery
- Customizable scripts and manual actions
- Integration with Azure Automation

### Backup Strategies

**Azure Backup**
- VM backups (application-consistent)
- SQL Server and SAP HANA in Azure VMs
- Azure Files backup
- Cross-region restore

**Database Backup**
- SQL Database: Automated backups (7-35 days)
- Cosmos DB: Continuous backup (30 days)
- Long-term retention policies

### High Availability

**RTO/RPO Targets**
- Active-Active: Multi-region with Traffic Manager (near-zero)
- Active-Passive: Geo-replication with failover (minutes)
- Backup and Restore: Azure Backup (hours)

## Monitoring and Observability

### Azure Monitor

**Components**
- Metrics: Time-series data (1-minute resolution)
- Logs: Log Analytics workspace for queries (KQL)
- Alerts: Metric, log, and activity log alerts
- Dashboards: Custom visualizations

**Application Insights**
- APM for web applications
- Distributed tracing
- Live Metrics Stream
- Smart detection and anomaly detection
- Best practices: Instrument all applications, set up availability tests

### Log Analytics

**KQL Queries**
```kusto
// Performance analysis
Perf
| where CounterName == "% Processor Time"
| summarize avg(CounterValue) by bin(TimeGenerated, 5m), Computer
| render timechart

// Failed requests
requests
| where success == false
| summarize count() by resultCode, bin(timestamp, 1h)
```

**Workbooks**
- Interactive reports
- Parameterized queries
- Combining metrics and logs

## Identity and Access

### Azure AD Best Practices

- Enable MFA for all users
- Use Conditional Access policies
- Implement Privileged Identity Management (PIM)
- Regular access reviews
- Break-glass accounts

### RBAC Design

**Built-in Roles**
- Owner: Full access including RBAC
- Contributor: Full access except RBAC
- Reader: Read-only access
- Custom roles for specific needs

**Scope Hierarchy**
```
Management Group (highest)
    |
Subscription
    |
Resource Group
    |
Resource (lowest)
```

Best practices: Assign at highest appropriate scope, use groups not individual users, apply least privilege

---

## Reference: Cost

# Cloud Cost Optimization Reference

Comprehensive guide for cloud cost optimization including reserved instances, spot/preemptible, right-sizing, and FinOps practices.

## FinOps Framework

### FinOps Principles

1. **Teams need to collaborate** - Finance, engineering, and business work together
2. **Everyone takes ownership** - Decentralized cost responsibility
3. **A centralized team drives FinOps** - Center of excellence for best practices
4. **Reports should be accessible and timely** - Real-time visibility
5. **Decisions are driven by business value** - Cost per business outcome
6. **Take advantage of variable cost model** - Scale up and down as needed

### FinOps Lifecycle

```
      Inform
         |
    +---------+
    |         |
    v         v
 Optimize --> Operate
    ^         |
    |         |
    +---------+
```

**Inform Phase**
- Visibility into cloud spend
- Allocation and showback
- Benchmarking and forecasting

**Optimize Phase**
- Rate optimization (RIs, savings plans)
- Usage optimization (right-sizing)
- Architectural optimization

**Operate Phase**
- Continuous improvement
- Automation and governance
- Anomaly detection

## Compute Cost Optimization

### Reserved Instances / Savings Plans

**AWS Savings Plans**

| Type | Flexibility | Savings |
|------|-------------|---------|
| Compute Savings Plans | Any EC2, Fargate, Lambda | Up to 66% |
| EC2 Instance Savings Plans | Specific instance family, region | Up to 72% |
| Reserved Instances | Specific instance type, AZ | Up to 72% |

**Commitment Strategy**
```
Baseline (always-on): 1-year or 3-year Savings Plans
Variable (predictable): Scheduled Reserved Instances
Spiky (unpredictable): On-Demand + Spot
```

**Azure Reservations**
```
# Azure CLI - Purchase reservation
az reservations reservation-order purchase \
  --sku Standard_D2s_v3 \
  --term P1Y \
  --billing-scope /subscriptions/{subscription-id} \
  --quantity 10 \
  --applied-scope-type Shared
```

**GCP Committed Use Discounts**
- Resource-based: Specific vCPUs and memory
- Spend-based: Dollar commitment for flexibility
- 1-year (37% discount) or 3-year (55% discount)

### Spot/Preemptible Instances

**When to Use Spot**
- Batch processing and analytics
- CI/CD build agents
- Stateless web servers (with auto-scaling)
- Machine learning training
- Development and testing environments

**AWS Spot Best Practices**
```yaml
# EC2 Auto Scaling with Spot
MixedInstancesPolicy:
  InstancesDistribution:
    OnDemandBaseCapacity: 2
    OnDemandPercentageAboveBaseCapacity: 20
    SpotAllocationStrategy: capacity-optimized
  LaunchTemplate:
    Overrides:
      - InstanceType: m5.large
      - InstanceType: m5a.large
      - InstanceType: m4.large
      - InstanceType: r5.large
```

**Spot Interruption Handling**
```python
# Check for spot termination notice (AWS)
import requests

def check_spot_termination():
    try:
        response = requests.get(
            "http://169.254.169.254/latest/meta-data/spot/termination-time",
            timeout=2
        )
        if response.status_code == 200:
            # 2-minute warning - gracefully shutdown
            graceful_shutdown()
    except requests.exceptions.RequestException:
        pass  # Not being terminated
```

**GCP Preemptible/Spot VMs**
```hcl
# Terraform - GCP Spot VM
resource "google_compute_instance" "spot" {
  name         = "spot-instance"
  machine_type = "n2-standard-4"

  scheduling {
    preemptible                 = true
    automatic_restart           = false
    provisioning_model          = "SPOT"
    instance_termination_action = "STOP"
  }
}
```

### Right-Sizing

**Analysis Process**
1. Collect metrics (CPU, memory, network, disk I/O)
2. Identify idle or underutilized resources
3. Recommend appropriate instance size
4. Implement changes during maintenance windows
5. Monitor and iterate

**AWS Compute Optimizer**
```bash
# Enable Compute Optimizer
aws compute-optimizer update-enrollment-status \
  --status Active \
  --include-member-accounts

# Get recommendations
aws compute-optimizer get-ec2-instance-recommendations \
  --filters name=Finding,values=OVER_PROVISIONED
```

**Right-Sizing Thresholds**
| Metric | Underutilized | Optimal | Overutilized |
|--------|---------------|---------|--------------|
| CPU | <20% avg | 40-60% avg | >80% avg |
| Memory | <30% avg | 50-70% avg | >85% avg |
| Network | <10% capacity | Variable | >80% capacity |

**Azure Advisor Recommendations**
```bash
# Get cost recommendations
az advisor recommendation list \
  --category Cost \
  --query "[?impact=='High']"
```

## Storage Cost Optimization

### Object Storage Tiering

**AWS S3 Storage Classes**
```
S3 Standard
    |
    | (30 days)
    v
S3 Standard-IA
    |
    | (90 days)
    v
S3 Glacier Instant Retrieval
    |
    | (180 days)
    v
S3 Glacier Deep Archive
```

**Lifecycle Policy Example**
```json
{
  "Rules": [
    {
      "ID": "OptimizeCosts",
      "Status": "Enabled",
      "Filter": { "Prefix": "logs/" },
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" },
        { "Days": 365, "StorageClass": "DEEP_ARCHIVE" }
      ],
      "Expiration": { "Days": 730 }
    }
  ]
}
```

**S3 Intelligent-Tiering**
- Automatic tiering based on access patterns
- No retrieval fees
- Small monitoring fee per object
- Best for unpredictable access patterns

### Block Storage Optimization

**EBS Volume Selection**
| Type | Use Case | $/GB/month |
|------|----------|------------|
| gp3 | General purpose | $0.08 |
| gp2 | Legacy (migrate to gp3) | $0.10 |
| io2 | High IOPS databases | $0.125+ |
| st1 | Throughput (big data) | $0.045 |
| sc1 | Cold archives | $0.015 |

**gp3 Migration (20% savings)**
```bash
# Modify EBS volume from gp2 to gp3
aws ec2 modify-volume \
  --volume-id vol-12345678 \
  --volume-type gp3 \
  --iops 3000 \
  --throughput 125
```

### Database Storage

**Aurora Storage Optimization**
- Pay only for storage used (auto-scaling)
- No pre-provisioning required
- 10GB increments up to 128TB

**DynamoDB Capacity Modes**
| Mode | Best For | Pricing |
|------|----------|---------|
| On-Demand | Unpredictable traffic | Pay per request |
| Provisioned | Steady traffic | Pay per capacity unit |
| Provisioned + Auto Scaling | Variable but predictable | Lower cost than on-demand |

## Network Cost Optimization

### Data Transfer Costs

**AWS Data Transfer Pricing**
```
Inbound: Free
Same AZ: Free
Cross-AZ: $0.01/GB each direction
Same Region (via public IP): $0.01/GB
Cross-Region: $0.02/GB
Internet Egress: $0.09/GB (first 10TB)
```

**Optimization Strategies**
1. Keep traffic within same AZ when possible
2. Use VPC endpoints for AWS services
3. Use CloudFront for cacheable content
4. Compress data before transfer
5. Use regional rather than global services

**VPC Endpoints (Avoid NAT Gateway)**
```hcl
# Gateway endpoint (free for S3, DynamoDB)
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.us-east-1.s3"
}

# Interface endpoint (cheaper than NAT for specific services)
resource "aws_vpc_endpoint" "ecr" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.us-east-1.ecr.api"
  vpc_endpoint_type = "Interface"
}
```

### CDN Optimization

**CloudFront Cost Savings**
- Lower data transfer rates than direct from origin
- Cache hit ratio optimization (target >90%)
- Use Origin Shield to reduce origin load
- Compress objects (Gzip/Brotli)

```yaml
# CloudFront cache optimization
CacheBehaviors:
  - PathPattern: "/static/*"
    CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6  # CachingOptimized
    Compress: true
    TTL:
      DefaultTTL: 86400
      MaxTTL: 31536000
```

## Serverless Cost Optimization

### Lambda Optimization

**Memory/CPU Tuning**
```python
# Use AWS Lambda Power Tuning
# Finds optimal memory for cost vs performance

# Results example:
# 128MB:  $0.000021 per invocation, 3200ms duration
# 256MB:  $0.000025 per invocation, 1600ms duration
# 512MB:  $0.000031 per invocation, 800ms duration
# 1024MB: $0.000042 per invocation, 450ms duration
# Optimal: 512MB (best cost-performance balance)
```

**Cost Reduction Strategies**
1. Right-size memory allocation
2. Minimize cold starts (provisioned concurrency for critical paths)
3. Use ARM64 (Graviton2) - 20% cheaper
4. Optimize package size for faster cold starts
5. Use Lambda Layers for shared dependencies

**Graviton2 Migration**
```yaml
# SAM template with ARM64
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Runtime: python3.11
      Architectures:
        - arm64  # 20% cost savings
```

### Container Optimization

**Fargate Pricing Optimization**
```
# Fargate Spot: Up to 70% discount
# Use for fault-tolerant workloads

ECS Service:
  CapacityProviderStrategy:
    - CapacityProvider: FARGATE_SPOT
      Weight: 4
    - CapacityProvider: FARGATE
      Weight: 1
      Base: 2  # Minimum on-demand tasks
```

**Right-Size Container Resources**
```yaml
# Analyze actual usage with Container Insights
resources:
  requests:
    memory: "256Mi"  # Based on p95 usage + 20% buffer
    cpu: "100m"      # Based on p95 usage + 20% buffer
  limits:
    memory: "512Mi"  # 2x requests for burst
    cpu: "500m"
```

## Cost Allocation and Tagging

### Tagging Strategy

**Required Tags**
```yaml
# Terraform - enforce tags
variable "required_tags" {
  default = {
    environment  = "prod"
    cost-center  = "engineering"
    owner        = "platform-team"
    project      = "api-gateway"
    managed-by   = "terraform"
  }
}

resource "aws_instance" "example" {
  ami           = data.aws_ami.latest.id
  instance_type = "t3.medium"
  tags          = var.required_tags
}
```

**Tag Enforcement**
```json
// AWS SCP - Deny untagged resources
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUntaggedEC2",
      "Effect": "Deny",
      "Action": "ec2:RunInstances",
      "Resource": "arn:aws:ec2:*:*:instance/*",
      "Condition": {
        "Null": {
          "aws:RequestTag/cost-center": "true"
        }
      }
    }
  ]
}
```

### Cost Allocation Reports

**AWS Cost and Usage Report**
```bash
# Enable detailed billing reports
aws cur put-report-definition \
  --report-definition '{
    "ReportName": "detailed-cost-report",
    "TimeUnit": "HOURLY",
    "Format": "Parquet",
    "Compression": "Parquet",
    "S3Bucket": "my-billing-bucket",
    "S3Region": "us-east-1",
    "AdditionalArtifacts": ["ATHENA"]
  }'
```

**Athena Queries for Analysis**
```sql
-- Cost by service and tag
SELECT
  line_item_product_code as service,
  resource_tags_user_cost_center as cost_center,
  SUM(line_item_unblended_cost) as cost
FROM cost_report
WHERE month = '2024-01'
GROUP BY 1, 2
ORDER BY 3 DESC;

-- Unused Reserved Instances
SELECT
  reservation_reservation_a_r_n,
  reservation_unused_quantity,
  reservation_unused_normalized_unit_quantity
FROM cost_report
WHERE reservation_unused_quantity > 0;
```

## Automation and Governance

### Automated Cost Controls

**AWS Budgets with Actions**
```yaml
# CloudFormation - Budget with auto-stop
Resources:
  MonthlyCostBudget:
    Type: AWS::Budgets::Budget
    Properties:
      Budget:
        BudgetName: monthly-cost-limit
        BudgetLimit:
          Amount: 10000
          Unit: USD
        TimeUnit: MONTHLY
        BudgetType: COST
      NotificationsWithSubscribers:
        - Notification:
            NotificationType: ACTUAL
            ComparisonOperator: GREATER_THAN
            Threshold: 80
          Subscribers:
            - SubscriptionType: EMAIL
              Address: finance@company.com
```

**Scheduled Scaling (Dev/Test)**
```yaml
# Stop non-prod resources nights/weekends
Resources:
  ScaleDownSchedule:
    Type: AWS::AutoScaling::ScheduledAction
    Properties:
      AutoScalingGroupName: !Ref DevASG
      DesiredCapacity: 0
      Recurrence: "0 20 * * MON-FRI"  # 8 PM weekdays

  ScaleUpSchedule:
    Type: AWS::AutoScaling::ScheduledAction
    Properties:
      AutoScalingGroupName: !Ref DevASG
      DesiredCapacity: 3
      Recurrence: "0 8 * * MON-FRI"   # 8 AM weekdays
```

### Cost Anomaly Detection

**AWS Cost Anomaly Detection**
```bash
# Create anomaly monitor
aws ce create-anomaly-monitor \
  --anomaly-monitor '{
    "MonitorName": "ServiceMonitor",
    "MonitorType": "DIMENSIONAL",
    "MonitorDimension": "SERVICE"
  }'

# Create anomaly subscription
aws ce create-anomaly-subscription \
  --anomaly-subscription '{
    "SubscriptionName": "CostAlerts",
    "MonitorArnList": ["arn:aws:ce::123456789:anomalymonitor/abc123"],
    "Subscribers": [{"Type": "EMAIL", "Address": "alerts@company.com"}],
    "Threshold": 100
  }'
```

## Cost Metrics and KPIs

### Key Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Unit Cost | Total Cost / Business Metric | Decreasing |
| Coverage | Reserved Hours / Total Hours | >70% |
| Utilization | Used Reserved Hours / Purchased | >80% |
| Waste | Idle Resource Cost / Total Cost | <10% |
| Forecast Accuracy | Actual / Forecasted | 90-110% |

### Dashboard Example

```sql
-- Cost efficiency dashboard metrics
WITH metrics AS (
  SELECT
    date_trunc('month', usage_date) as month,
    SUM(cost) as total_cost,
    SUM(CASE WHEN reservation_arn IS NOT NULL THEN cost END) as reserved_cost,
    COUNT(DISTINCT user_id) as active_users
  FROM cloud_costs
  GROUP BY 1
)
SELECT
  month,
  total_cost,
  reserved_cost / total_cost as reservation_coverage,
  total_cost / active_users as cost_per_user
FROM metrics;
```

## Quick Wins Checklist

**Immediate Savings (This Week)**
- [ ] Delete unused EBS volumes and snapshots
- [ ] Terminate stopped EC2 instances not needed
- [ ] Remove unused Elastic IPs
- [ ] Delete unused load balancers
- [ ] Review and delete old AMIs

**Short-Term (This Month)**
- [ ] Right-size underutilized instances
- [ ] Migrate gp2 volumes to gp3
- [ ] Implement S3 lifecycle policies
- [ ] Enable S3 Intelligent-Tiering
- [ ] Schedule dev/test environments

**Medium-Term (This Quarter)**
- [ ] Purchase Savings Plans for baseline
- [ ] Implement Spot for fault-tolerant workloads
- [ ] Set up cost allocation tags
- [ ] Enable Cost Anomaly Detection
- [ ] Establish FinOps practices

---

## Reference: Gcp

# GCP Architecture Reference

Comprehensive guide for Google Cloud Platform services, patterns, and architecture framework.

## Google Cloud Architecture Framework

### Five Pillars

1. **Operational Excellence**
   - Infrastructure as Code (Deployment Manager, Terraform)
   - CI/CD with Cloud Build
   - Monitoring with Cloud Monitoring (Stackdriver)
   - SRE principles and SLOs
   - Incident management

2. **Security, Privacy, and Compliance**
   - Identity and Access Management (Cloud IAM)
   - VPC Service Controls for data perimeter
   - Binary Authorization for containers
   - Data encryption (default at rest and in transit)
   - Security Command Center

3. **Reliability**
   - Multi-zone and multi-region deployments
   - Load balancing and autoscaling
   - Disaster recovery planning
   - Chaos engineering practices
   - SLIs, SLOs, and error budgets

4. **Cost Optimization**
   - Committed Use Discounts
   - Sustained Use Discounts (automatic)
   - Preemptible VMs and Spot VMs
   - Recommender for right-sizing
   - Active Assist for optimization

5. **Performance Optimization**
   - Cloud CDN and Media CDN
   - Caching strategies (Memorystore)
   - Database performance tuning
   - Network optimization (Premium vs Standard tier)
   - Regional and zonal resource placement

## Core Services Architecture

### Compute

**Compute Engine**
- Machine types: E2 (cost-optimized), N2 (balanced), C2 (compute-optimized), M2 (memory-optimized)
- Custom machine types for specific needs
- Preemptible VMs (up to 80% discount, max 24 hours)
- Spot VMs (similar to preemptible, better availability)
- Instance groups: Managed (with autoscaling), unmanaged
- Best practices: Use latest generation, committed use discounts, Spot for batch jobs

**Cloud Run**
- Fully managed serverless container platform
- Auto-scaling to zero
- Pay per request
- CPU allocated only during request handling
- Best practices: Stateless containers, optimize cold starts, use Cloud Run jobs for batch

**Cloud Functions**
- Event-driven serverless functions
- 1st gen: HTTP and background functions
- 2nd gen: Built on Cloud Run, better performance
- Event sources: Pub/Sub, Cloud Storage, Firestore, HTTP
- Best practices: Use 2nd gen, minimize cold starts, implement retry logic

**Google Kubernetes Engine (GKE)**
- Managed Kubernetes with GCP integration
- Autopilot mode: Fully managed, per-pod pricing
- Standard mode: More control, node management
- Workload Identity for secure service access
- Binary Authorization for deployment policies
- Best practices: Use Autopilot for simplicity, enable Workload Identity, implement network policies

**App Engine**
- Fully managed platform (PaaS)
- Standard environment (sandboxed, auto-scaling)
- Flexible environment (Docker containers, custom runtimes)
- Traffic splitting for canary deployments
- Best practices: Use Standard for web apps, Flexible for custom dependencies

### Storage

**Cloud Storage**
- Storage classes: Standard, Nearline (30-day), Coldline (90-day), Archive (365-day)
- Object lifecycle management
- Object versioning and retention policies
- Autoclass for automatic tier transitions
- Requester pays for data transfer
- Best practices: Use Autoclass, enable versioning, implement lifecycle policies

**Persistent Disk**
- Types: Standard (HDD), Balanced SSD, SSD, Extreme
- Zonal and regional persistent disks
- Snapshots for backup (incremental)
- Disk resize without downtime
- Best practices: Use Balanced SSD for most workloads, enable snapshots

**Filestore**
- Managed NFS file storage
- Tiers: Basic (1-63.9 TB), Enterprise (1-10 TB, better performance)
- Backup to Cloud Storage
- Best practices: Use Enterprise for production, implement backups

**Cloud Storage for Firebase**
- Object storage for mobile and web apps
- Client SDKs for direct upload/download
- Security rules for access control

### Database

**Cloud SQL**
- Managed MySQL, PostgreSQL, SQL Server
- High availability configuration (regional)
- Read replicas for scaling
- Automated backups and point-in-time recovery
- Best practices: Enable HA, use read replicas, implement connection pooling with Cloud SQL Proxy

**Cloud Spanner**
- Globally distributed relational database
- Horizontal scalability with strong consistency
- Multi-region for 99.999% availability
- TrueTime for global consistency
- Best practices: Design proper schema splits, use commit timestamps, optimize hotspots

**Firestore (Native mode)**
- NoSQL document database
- Real-time synchronization
- Offline support for mobile
- ACID transactions
- Best practices: Design document structure carefully, use collection group queries wisely

**Bigtable**
- NoSQL wide-column database
- Petabyte-scale with single-digit millisecond latency
- HBase API compatible
- Linear scalability by adding nodes
- Best practices: Design row keys to avoid hotspots, use replication for HA

**Memorystore**
- Managed Redis and Memcached
- Standard tier (HA with replica) and Basic tier
- Best practices: Use Standard tier for production, implement connection pooling

**BigQuery**
- Serverless data warehouse
- SQL analytics on petabyte-scale data
- Column-oriented storage
- Automatic caching and optimization
- Best practices: Partition and cluster tables, use approximate functions, control costs with quotas

### Networking

**VPC (Virtual Private Cloud)**
- Global resource (subnets are regional)
- Custom or auto mode networks
- Firewall rules (stateful)
- VPC peering and Shared VPC
- Private Google Access for GCP services
- Best practices: Use custom mode VPC, plan IP ranges, implement firewall rules

**Cloud Load Balancing**
- Global load balancing (HTTP(S), TCP/SSL Proxy, external TCP/UDP)
- Regional load balancing (internal HTTP(S), internal TCP/UDP)
- Anycast IP for global distribution
- Backend services with health checks
- Best practices: Use global for multi-region, enable CDN, configure health checks

**Cloud CDN**
- Global content delivery network
- Cache invalidation and signed URLs
- Integration with Cloud Storage and compute
- Best practices: Enable compression, use cache-control headers

**Cloud Interconnect and VPN**
- Dedicated Interconnect (10 Gbps or 100 Gbps)
- Partner Interconnect (50 Mbps to 50 Gbps)
- Cloud VPN (HA VPN for 99.99% SLA)
- Best practices: Use HA VPN for redundancy, Dedicated Interconnect for high bandwidth

**Cloud Armor**
- DDoS protection and WAF
- Preconfigured and custom rules
- Adaptive protection (ML-based)
- Best practices: Enable for internet-facing services, use preconfigured rules

**Private Service Connect**
- Private connectivity to Google APIs and services
- Service Directory for service discovery
- Best practices: Use for all managed services in production

### Serverless and Event-Driven

**Pub/Sub**
- Global message queue
- At-least-once delivery
- Push and pull subscriptions
- Message ordering and filtering
- Dead-letter topics
- Best practices: Use message attributes for filtering, implement idempotent processing

**Eventarc**
- Event-driven architecture
- Triggers for Cloud Run, Workflows, GKE
- Sources: Audit Logs, Pub/Sub, custom events
- Best practices: Use for decoupled architectures, implement event filtering

**Cloud Scheduler**
- Fully managed cron service
- HTTP, Pub/Sub, and App Engine targets
- Best practices: Use for periodic tasks, implement retry logic

**Workflows**
- Orchestrate and automate GCP and HTTP services
- YAML-based workflow definition
- Built-in error handling and retry
- Best practices: Use for complex multi-step processes, implement compensating transactions

### Security and Identity

**Cloud IAM**
- Resource hierarchy: Organization -> Folders -> Projects -> Resources
- Roles: Primitive (Owner, Editor, Viewer), Predefined, Custom
- Service accounts for applications
- Workload Identity for GKE
- Best practices: Use predefined roles, least privilege, service accounts for apps

**Cloud Key Management (KMS)**
- Encryption key management
- Customer-managed encryption keys (CMEK)
- Hardware Security Module (HSM) backed
- Automatic key rotation
- Best practices: Enable automatic rotation, use separate keys per environment

**Secret Manager**
- Store API keys, passwords, certificates
- Versioning and access control
- Automatic rotation integration
- Best practices: Rotate secrets regularly, use IAM for access control

**Security Command Center**
- Centralized security and risk management
- Asset discovery and vulnerability scanning
- Threat detection and compliance monitoring
- Best practices: Enable all detectors, review findings regularly

**VPC Service Controls**
- Create security perimeters around GCP resources
- Prevent data exfiltration
- Best practices: Use for sensitive data, implement access levels

### AI and Machine Learning

**Vertex AI**
- Unified ML platform
- AutoML for custom models
- Pre-trained models (Vision, Natural Language, etc.)
- MLOps with pipelines
- Best practices: Use AutoML for quick start, implement feature store

**BigQuery ML**
- Create and execute ML models using SQL
- Model types: Linear regression, logistic regression, clustering, etc.
- Integration with Vertex AI
- Best practices: Use for simple models, leverage BigQuery's scale

## Architecture Patterns

### High Availability

**Multi-Zone Pattern**
```
Global HTTP(S) Load Balancer
    |
    v
Managed Instance Group (multi-zone)
    |
    v
Cloud SQL (regional, HA configuration)
    |
    v
Cloud Storage (multi-region)
```

**Multi-Region Pattern**
```
Global HTTP(S) Load Balancer
    |
    ├── Backend Service Region 1 (Cloud Run)
    └── Backend Service Region 2 (Cloud Run)
         |
         v
    Cloud Spanner (multi-region)
```

### Serverless Architecture

**Event-Driven Pattern**
```
Cloud Storage upload event
    |
    v
Pub/Sub topic
    |
    v
Cloud Functions (image processing)
    |
    v
Firestore (metadata storage)
```

**API-First Pattern**
```
Cloud Endpoints or API Gateway
    |
    v
Cloud Run (multiple services)
    |
    ├── Cloud SQL (transactional data)
    └── Firestore (user data)
```

### Microservices on GKE

**GKE with Service Mesh**
```
Global Load Balancer
    |
    v
GKE Ingress
    |
    v
Anthos Service Mesh (Istio)
    |
    v
Microservices (Cloud Spanner, Firestore, Memorystore)
```

### Data Analytics Platform

```
Data Sources
    |
    v
Pub/Sub (streaming)
    |
    v
Dataflow (Apache Beam)
    |
    v
BigQuery (data warehouse)
    |
    v
Looker or Data Studio (visualization)
```

**Batch Processing**
```
Cloud Storage (raw data)
    |
    v
Dataproc (Apache Spark)
    |
    v
BigQuery (analytics)
```

## Landing Zone Design

### Resource Hierarchy

```
Organization
├── Folders (by environment or team)
│   ├── Production Folder
│   │   ├── Project A
│   │   └── Project B
│   ├── Staging Folder
│   └── Development Folder
└── Shared Services Folder
    ├── Networking Project (Shared VPC host)
    ├── Security Project (KMS, Secret Manager)
    └── Logging Project (centralized logs)
```

### Network Design

**Shared VPC Pattern**
```
Host Project (networking team)
├── Shared VPC
│   ├── Subnet Production (region A)
│   ├── Subnet Staging (region A)
│   └── Subnet Development (region B)

Service Projects (application teams)
├── Production Project (uses Production subnet)
├── Staging Project (uses Staging subnet)
└── Development Project (uses Development subnet)
```

**Hub-and-Spoke with VPN**
```
On-premises Network
    |
    v
Cloud VPN / Interconnect
    |
    v
Hub VPC (shared services)
    |
    ├── Spoke VPC 1 (production workloads)
    ├── Spoke VPC 2 (development workloads)
    └── Spoke VPC 3 (analytics workloads)
```

### Governance

**Organization Policies**
- Restrict public IP assignment
- Enforce uniform bucket-level access
- Restrict VM external IP
- Define allowed resource locations

**IAM Strategy**
- Use Google Groups for role assignments
- Separate duties (network admin, security admin, etc.)
- Service accounts per application
- Workload Identity for GKE workloads

**Logging and Monitoring**
```
All Projects
    |
    v
Log Router
    |
    ├── Cloud Logging (default sink)
    ├── BigQuery (long-term analysis)
    ├── Cloud Storage (archive)
    └── Pub/Sub (real-time processing)
```

## Migration Strategies

### Migrate to Virtual Machines

**Tools**
- Migrate to Virtual Machines (formerly Migrate for Compute Engine)
- Supports VMware, AWS, Azure, physical servers
- Agentless or agent-based migration
- Waves and test clones

**Process**
1. Assess: Fit assessment and TCO analysis
2. Plan: Group VMs, define migration waves
3. Deploy: Set up infrastructure (VPC, firewall rules)
4. Migrate: Test migration, cutover, validation
5. Optimize: Right-sizing, committed use discounts

### Database Migration

**Database Migration Service**
- Minimal downtime migrations
- Supports MySQL, PostgreSQL, SQL Server, Oracle
- Continuous replication for cutover flexibility

**Transfer Appliance**
- Physical device for large data transfers
- Up to 1 PB capacity
- Offline data transfer

## Cost Optimization

### Compute Savings

**Committed Use Discounts**
- 1-year or 3-year commitments
- Up to 57% savings for VMs
- Resource-based or spend-based

**Sustained Use Discounts**
- Automatic discounts for running VMs >25% of month
- Up to 30% savings
- No commitment required

**Preemptible and Spot VMs**
- Up to 80% discount
- Can be terminated by GCP
- Best for batch processing, fault-tolerant workloads

**Recommender**
- VM rightsizing recommendations
- Idle resource identification
- Committed use discount recommendations

### Storage Savings

**Cloud Storage**
- Autoclass for automatic tier transitions
- Lifecycle policies (delete or transition)
- Nearline (30+ days), Coldline (90+ days), Archive (365+ days)
- Requester pays for data transfer

**Persistent Disk**
- Delete orphaned disks
- Use balanced SSD instead of SSD when possible
- Resize disks to match actual usage

### BigQuery Savings

**On-Demand Pricing**
- $5 per TB processed
- Use partitioning and clustering
- Query cache for free repeated queries

**Flat-Rate Pricing**
- Predictable costs for heavy users
- Autoscaling slots available
- Flex slots for short-term commitments

**Best Practices**
- Use approximate aggregation functions (APPROX_COUNT_DISTINCT)
- Avoid SELECT *, specify columns
- Use materialized views for common queries
- Set up cost controls with custom quotas

### Monitoring Costs

**Cloud Billing**
- Budgets and alerts
- Cost breakdown by project, service, SKU
- Export to BigQuery for analysis
- Recommendations from Active Assist

## Disaster Recovery

### Backup Strategies

**VM Backups**
- Persistent disk snapshots (incremental)
- Machine images (include metadata and config)
- Cross-region snapshot copy
- Snapshot schedules for automation

**Database Backups**
- Cloud SQL: Automated backups (7-365 days retention)
- Cloud Spanner: Backups on demand or scheduled
- Firestore: Automated daily exports
- Bigtable: Backups to Cloud Storage

### High Availability

**RTO/RPO Matrix**

| Pattern | RPO | RTO | Cost |
|---------|-----|-----|------|
| Active-Active Multi-Region | Seconds | Seconds | High |
| Active-Passive with Replication | Minutes | Minutes | Medium |
| Warm Standby | Minutes | 10-30 min | Medium |
| Backup and Restore | Hours | Hours | Low |

**Cloud SQL HA**
- Regional configuration with synchronous replication
- Automatic failover
- 99.95% SLA (vs 99.5% for single zone)

**Cloud Spanner**
- Multi-region configuration
- 99.999% availability SLA
- Synchronous replication across regions

### Disaster Recovery Testing

- Regular DR drills (quarterly recommended)
- Document runbooks
- Test restoration procedures
- Measure actual RTO/RPO vs targets

## Monitoring and Observability

### Cloud Monitoring (formerly Stackdriver)

**Metrics**
- System metrics (CPU, memory, disk, network)
- Custom metrics via Cloud Monitoring API
- Metric scopes for multi-project monitoring
- Uptime checks for availability

**Dashboards and Charts**
- Predefined dashboards for GCP services
- Custom dashboards with filters and grouping
- SLO monitoring with error budgets

### Cloud Logging

**Log Types**
- Admin Activity logs (always enabled, no charge)
- Data Access logs (must be enabled)
- System Event logs
- Access Transparency logs (for Google access)

**Log Sinks**
- Route logs to BigQuery, Cloud Storage, Pub/Sub
- Aggregated sinks at organization/folder level
- Exclusion filters to reduce costs

### Cloud Trace

**Distributed Tracing**
- Automatic instrumentation for App Engine, Cloud Run, GKE
- Manual instrumentation with client libraries
- Latency analysis and performance insights
- Integration with Zipkin

### Cloud Profiler

**Continuous Profiling**
- CPU and memory profiling
- Low overhead (< 0.5% CPU)
- Flame graphs for visualization
- Supported languages: Java, Go, Python, Node.js

### Error Reporting

**Aggregated Error Tracking**
- Automatic error grouping
- Stack trace analysis
- Integration with Cloud Logging
- Notifications for new errors

---

## Reference: Multi Cloud

# Multi-Cloud Architecture Reference

Comprehensive guide for multi-cloud strategies, abstraction layers, portability patterns, and vendor lock-in mitigation.

## Multi-Cloud Strategy

### When to Use Multi-Cloud

**Valid Use Cases**
- Regulatory compliance requiring data residency in specific regions
- Best-of-breed service selection (BigQuery for analytics, AWS for ML)
- Acquisition integration (different clouds in merged organizations)
- Disaster recovery with cloud provider as failure domain
- Negotiating leverage with cloud vendors

**Poor Reasons for Multi-Cloud**
- "Avoiding vendor lock-in" without specific exit scenario
- Assuming portability is free (it has significant costs)
- Political decisions without technical justification
- Spreading workloads arbitrarily across providers

### Multi-Cloud Patterns

**Active-Active**
```
Users -> Global Load Balancer
              |
    +---------+---------+
    |                   |
  AWS Region        GCP Region
    |                   |
    +----> Data Sync <--+
```
- Highest complexity and cost
- Best for global latency optimization
- Requires robust data synchronization

**Active-Passive (DR)**
```
Users -> Primary (AWS)
              |
         [Failover]
              |
         Secondary (Azure)
```
- Lower complexity than active-active
- Cloud provider becomes failure domain
- Cold or warm standby in secondary cloud

**Segmented by Workload**
```
Analytics -> GCP (BigQuery)
Core App  -> AWS (ECS, RDS)
Office    -> Azure (M365 integration)
```
- Each workload on best-fit cloud
- No cross-cloud data synchronization
- Simplest multi-cloud pattern

## Abstraction Layers

### Infrastructure Abstraction

**Terraform (Recommended)**
```hcl
# Provider-agnostic module structure
module "compute" {
  source = "./modules/compute"

  provider_type = var.cloud_provider  # aws, azure, gcp
  instance_type = var.instance_size
  region        = var.region
}

# Provider-specific implementations
# modules/compute/aws.tf
resource "aws_instance" "main" {
  count         = var.provider_type == "aws" ? 1 : 0
  ami           = data.aws_ami.latest.id
  instance_type = local.aws_instance_map[var.instance_size]
}

# modules/compute/azure.tf
resource "azurerm_virtual_machine" "main" {
  count    = var.provider_type == "azure" ? 1 : 0
  vm_size  = local.azure_vm_map[var.instance_size]
}
```

**Pulumi (Code-First)**
```typescript
// Abstract cloud resources with TypeScript
interface ComputeConfig {
  size: "small" | "medium" | "large";
  region: string;
}

function createCompute(config: ComputeConfig, provider: "aws" | "gcp") {
  if (provider === "aws") {
    return new aws.ec2.Instance("web", {
      instanceType: sizeMap.aws[config.size],
      // ...
    });
  } else {
    return new gcp.compute.Instance("web", {
      machineType: sizeMap.gcp[config.size],
      // ...
    });
  }
}
```

### Container Orchestration (Kubernetes)

**Portable Kubernetes Deployment**
```yaml
# Same manifests work across EKS, AKS, GKE
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    spec:
      containers:
      - name: web
        image: myregistry/web:v1
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**Cloud-Specific Considerations**
| Feature | EKS | AKS | GKE |
|---------|-----|-----|-----|
| Load Balancer | ALB/NLB annotations | Azure LB | GCP LB |
| Storage Class | gp3, io2 | managed-premium | pd-ssd |
| IAM Integration | IRSA | Workload Identity | Workload Identity |
| Ingress | AWS ALB Controller | AGIC | GKE Ingress |

### Application Abstraction

**Database Abstraction**
```python
# Use standard protocols (SQL, Redis, S3 API)
from sqlalchemy import create_engine

# Same code works with:
# - AWS RDS PostgreSQL
# - Azure Database for PostgreSQL
# - GCP Cloud SQL PostgreSQL
# - Self-managed PostgreSQL

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
```

**Object Storage Abstraction**
```python
import boto3
from botocore.config import Config

# S3-compatible API works with:
# - AWS S3
# - GCP Cloud Storage (interoperability mode)
# - MinIO
# - Cloudflare R2

s3_client = boto3.client(
    's3',
    endpoint_url=os.environ.get("S3_ENDPOINT"),  # Override for non-AWS
    aws_access_key_id=os.environ["ACCESS_KEY"],
    aws_secret_access_key=os.environ["SECRET_KEY"],
)
```

## Data Synchronization

### Database Replication

**Cross-Cloud PostgreSQL**
```
AWS RDS Primary
      |
      | Logical Replication
      v
GCP Cloud SQL Replica (read-only)
```

Configuration:
```sql
-- On primary (AWS RDS)
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- On replica (GCP Cloud SQL)
CREATE SUBSCRIPTION my_subscription
  CONNECTION 'host=aws-rds-endpoint dbname=mydb user=repl'
  PUBLICATION my_publication;
```

**Conflict Resolution Strategies**
- Last-write-wins (timestamp-based)
- Application-level conflict resolution
- CRDT data structures for eventually consistent data
- Avoid multi-master for transactional data

### Object Storage Sync

**Rclone for Cross-Cloud Sync**
```bash
# Sync S3 to GCS
rclone sync s3:my-bucket gcs:my-bucket \
  --transfers 32 \
  --checkers 16 \
  --s3-upload-concurrency 8

# Bidirectional sync with conflict handling
rclone bisync s3:bucket gcs:bucket \
  --conflict-resolve newer
```

**Event-Driven Replication**
```
S3 Bucket -> S3 Event -> Lambda -> GCS Upload
                              |
                              v
                       Consistency Check
```

## Vendor Lock-In Mitigation

### Lock-In Risk Assessment

| Service Type | Lock-In Risk | Mitigation Strategy |
|--------------|--------------|---------------------|
| Compute (VMs) | Low | Standard OS images, IaC |
| Kubernetes | Low | Portable manifests, avoid proprietary add-ons |
| Object Storage | Low | S3-compatible API, standard formats |
| Managed Databases | Medium | Standard SQL, logical backups |
| Serverless Functions | High | Abstraction layers, containers |
| Proprietary AI/ML | High | Open-source alternatives, ONNX models |
| Managed Services | High | Evaluate portability before adoption |

### Mitigation Strategies

**1. Use Open Standards**
- SQL databases over proprietary NoSQL
- Kubernetes over ECS/Cloud Run
- S3 API for object storage
- OpenTelemetry for observability
- OIDC for authentication

**2. Abstract Proprietary Services**
```typescript
// Wrap cloud-specific services
interface QueueService {
  send(message: string): Promise<void>;
  receive(): Promise<string>;
}

class SQSQueue implements QueueService {
  async send(message: string) {
    await this.sqsClient.sendMessage({ QueueUrl: this.url, MessageBody: message });
  }
}

class PubSubQueue implements QueueService {
  async send(message: string) {
    await this.pubsubClient.topic(this.topic).publish(Buffer.from(message));
  }
}

// Factory pattern for cloud selection
function createQueue(provider: string): QueueService {
  switch (provider) {
    case "aws": return new SQSQueue();
    case "gcp": return new PubSubQueue();
  }
}
```

**3. Maintain Exit Capability**
- Regular data export testing
- Document cloud-specific dependencies
- Keep IaC portable across providers
- Estimate migration effort annually

**4. Containerize Everything**
```dockerfile
# Portable container runs anywhere
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

## Network Connectivity

### Cross-Cloud Networking

**VPN Interconnect**
```
AWS VPC                          GCP VPC
   |                                |
   +---> AWS VPN Gateway            |
              |                     |
              | IPsec tunnel        |
              |                     |
              +---> GCP Cloud VPN <-+
```

**Dedicated Interconnect (Enterprise)**
```
On-Premises Data Center
         |
    +----+----+
    |         |
AWS Direct  GCP Cloud
Connect     Interconnect
    |         |
    v         v
AWS VPC    GCP VPC
    |         |
    +----+----+
         |
    Transit Hub (e.g., Megaport, Equinix)
```

### Service Mesh Across Clouds

**Istio Multi-Cluster**
```yaml
# Primary cluster (AWS EKS)
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  values:
    global:
      meshID: multi-cloud-mesh
      multiCluster:
        clusterName: eks-primary
      network: aws-network

# Remote cluster (GCP GKE)
spec:
  values:
    global:
      meshID: multi-cloud-mesh
      multiCluster:
        clusterName: gke-secondary
      network: gcp-network
```

## Cost Management

### Cross-Cloud Cost Visibility

**FinOps Tools**
- CloudHealth by VMware
- Apptio Cloudability
- Spot.io (now part of NetApp)
- Kubecost for Kubernetes

**Unified Tagging Strategy**
```
Required Tags (all clouds):
- environment: prod/staging/dev
- cost-center: engineering/marketing/sales
- owner: team-name
- project: project-code
- managed-by: terraform/manual
```

### Cost Comparison Framework

```
| Workload Type | AWS | Azure | GCP | Decision |
|---------------|-----|-------|-----|----------|
| General Compute | EC2 m5 | D-series | n2-standard | Compare $/vCPU/hour |
| GPU Training | p4d | NC-series | A2 | GCP often cheaper |
| Object Storage | S3 | Blob | GCS | Similar, check egress |
| Analytics | Redshift | Synapse | BigQuery | BigQuery for ad-hoc |
| Kubernetes | EKS | AKS | GKE | GKE Autopilot simplest |
```

## Observability

### Unified Monitoring Stack

**OpenTelemetry Collector**
```yaml
# Collect from all clouds, export to single backend
receivers:
  otlp:
    protocols:
      grpc:
      http:

processors:
  batch:
  attributes:
    actions:
      - key: cloud.provider
        action: upsert
        value: ${CLOUD_PROVIDER}

exporters:
  prometheus:
    endpoint: "0.0.0.0:8889"
  jaeger:
    endpoint: jaeger:14250

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, attributes]
      exporters: [jaeger]
    metrics:
      receivers: [otlp]
      processors: [batch, attributes]
      exporters: [prometheus]
```

**Grafana for Unified Dashboards**
- AWS CloudWatch data source
- Azure Monitor data source
- GCP Cloud Monitoring data source
- Single pane of glass across all clouds

## Security Considerations

### Identity Federation

**Cross-Cloud Identity**
```
Corporate IdP (Okta/Azure AD)
         |
    SAML/OIDC
         |
    +----+----+----+
    |    |    |    |
  AWS  Azure  GCP  K8s
  IAM   AD   IAM  RBAC
```

### Secrets Management

**HashiCorp Vault (Cloud-Agnostic)**
```hcl
# Single secrets management across clouds
resource "vault_aws_secret_backend_role" "aws_role" {
  backend = vault_aws_secret_backend.aws.path
  name    = "app-role"
  credential_type = "iam_user"
}

resource "vault_gcp_secret_roleset" "gcp_role" {
  backend     = vault_gcp_secret_backend.gcp.path
  roleset     = "app-role"
  project     = var.gcp_project
  token_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
}
```

### Network Security

**Zero-Trust Across Clouds**
- mTLS between all services (service mesh)
- No implicit trust based on network location
- Identity-based access control
- Encrypted transit between clouds (VPN/interconnect)
