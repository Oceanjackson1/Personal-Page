---
title: "GitHub Actions 生成器"
description: "生成 CI/CD 工作流配置的 GitHub Actions YAML 文件"
category: "devops"
source: "community"
author: "Community"
tags: ["github", "actions", "generator"]
date: 2026-03-20
---

# GitHub Actions Generator

Generate production-ready GitHub Actions workflows and custom actions following current best practices, security standards, and naming conventions. All generated resources are automatically validated using the devops-skills:github-actions-validator skill.

## Quick Reference

| Capability | When to Use | Reference |
|------------|-------------|-----------|
| Workflows | CI/CD, automation, testing | `references/best-practices.md` |
| Composite Actions | Reusable step combinations | `references/custom-actions.md` |
| Docker Actions | Custom environments/tools | `references/custom-actions.md` |
| JavaScript Actions | API interactions, complex logic | `references/custom-actions.md` |
| Reusable Workflows | Shared patterns across repos | `references/advanced-triggers.md` |
| Security Scanning | Dependency review, SBOM | `references/best-practices.md` |
| Modern Features | Summaries, environments | `references/modern-features.md` |

---

## Trigger Decision Tree

Route every request through this decision tree before reading references or generating files:

1. If the user asks for `.github/workflows/*.yml` CI/CD automation, choose **Workflow Generation**.
2. If the user asks for `action.yml` or a reusable step package, choose **Custom Action Generation**.
3. If the user asks for `workflow_call` or shared pipelines across repositories, choose **Reusable Workflow Generation**.
4. If the request includes security-only scanning (dependency review, SBOM, CodeQL), stay on **Workflow Generation** with the security pattern.
5. If intent is ambiguous, ask one disambiguation question: "Do you want a workflow, a custom action, or a reusable workflow?"

## Progressive Disclosure Route

Load only what is needed for the selected route, in this order:

| Route | Load First (required) | Load Next (only if needed) | Primary Template |
|-------|------------------------|------------------------------|------------------|
| Workflow Generation | `references/best-practices.md` | `references/common-actions.md`, `references/expressions-and-contexts.md`, `references/modern-features.md` | `assets/templates/workflow/basic_workflow.yml` |
| Custom Action Generation | `references/custom-actions.md` | `references/best-practices.md` | `assets/templates/action/composite/action.yml`, `assets/templates/action/docker/`, `assets/templates/action/javascript/` |
| Reusable Workflow Generation | `references/advanced-triggers.md` | `references/best-practices.md`, `references/common-actions.md` | `assets/templates/workflow/reusable_workflow.yml` |

If a required reference/template is unavailable, continue with the closest available reference and report the fallback explicitly in output.

---

## Core Capabilities

### 1. Generate Workflows

**Triggers:** "Create a workflow for...", "Build a CI/CD pipeline..."

**Process:**
1. Understand requirements (triggers, runners, dependencies)
2. Define trust boundaries (internal branches vs fork PRs vs external triggers)
3. Set default `permissions` to read-only, then elevate only per job when required
4. Reference `references/best-practices.md` for patterns
5. Reference `references/common-actions.md` for action versions
6. Generate workflow with:
   - Semantic names, pinned actions (SHA), explicit permissions
   - Concurrency controls, caching, matrix strategies
   - Fork-safe PR handling (no secrets in untrusted contexts)
7. **Validate** with devops-skills:github-actions-validator skill
8. Fix issues and re-validate if needed

**Minimal Example:**
```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
      - uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 # v6.2.0
        with:
          node-version: '24'
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

**Untrusted PR Guardrail (required for secret-using jobs):**
```yaml
jobs:
  deploy:
    if: github.event_name != 'pull_request' || github.event.pull_request.head.repo.full_name == github.repository
```

### 2. Generate Custom Actions

**Triggers:** "Create a composite action...", "Build a Docker action...", "Create a JavaScript action..."

**Types:**
- **Composite:** Combine multiple steps → Fast startup
- **Docker:** Custom environment/tools → Isolated
- **JavaScript:** API access, complex logic → Fastest

**Process:**
1. Use templates from `assets/templates/action/`
2. Follow structure in `references/custom-actions.md`
3. Include branding, inputs/outputs, documentation
4. **Validate** with devops-skills:github-actions-validator skill

See `references/custom-actions.md` for:
- Action metadata and branding
- Directory structure patterns
- Versioning and release workflows

### 3. Generate Reusable Workflows

**Triggers:** "Create a reusable workflow...", "Make this workflow callable..."

**Key Elements:**
- `workflow_call` trigger with typed inputs
- Explicit secrets (avoid `secrets: inherit`)
- Explicit trusted-caller expectations (document org/repo boundaries)
- Outputs mapped from job outputs
- Minimal permissions

```yaml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy-token:
        required: false
    outputs:
      result:
        value: ${{ jobs.build.outputs.result }}
```

When secrets are required, pass only the exact secret names needed and prefer environment protection rules for deployment stages.

See `references/advanced-triggers.md` for complete patterns.

### 4. Generate Security Workflows

**Triggers:** "Add security scanning...", "Add dependency review...", "Generate SBOM..."

**Components:**
- **Dependency Review:** `actions/dependency-review-action@v4`
- **SBOM Attestations:** `actions/attest-sbom@v2`
- **CodeQL Analysis:** `github/codeql-action`

**Permission Model:**
Use a read-only workflow-level baseline, then elevate only in the security job that requires write scopes.
```yaml
permissions:
  contents: read

jobs:
  security-scan:
    permissions:
      contents: read
      security-events: write  # For CodeQL
      id-token: write         # For attestations
      attestations: write     # For attestations
```

See `references/best-practices.md` section on security.

### 5. Modern Features

**Triggers:** "Add job summaries...", "Use environments...", "Run in container..."

See `references/modern-features.md` for:
- Job summaries (`$GITHUB_STEP_SUMMARY`)
- Deployment environments with approvals
- Container jobs with services
- Workflow annotations

### 6. Third-Party Action Documentation and Citation

When using third-party actions (any `uses:` entry not in the same repository):

1. **Search for documentation:**
   ```
   "[owner/repo] [version] github action documentation"
   ```

2. **Or use Context7 MCP:**
   - `mcp__context7__resolve-library-id` to find action
   - `mcp__context7__query-docs` for documentation

3. **Pin to SHA with version comment:**
   ```yaml
   - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
   ```

4. **Cite source and version in the response:**
   - Action source (repository URL)
   - Version source (release/tag/changelog URL)
   - Selected commit SHA and human-readable version
   - Access date for the source used

See `references/common-actions.md` for pre-verified action versions.

---

## Validation Workflow

**CRITICAL:** Every generated resource MUST be validated.

1. Generate workflow/action file
2. Invoke `devops-skills:github-actions-validator` skill
3. If errors: fix and re-validate
4. If success: present with usage instructions

**Skip validation only for:**
- Partial code snippets
- Documentation examples
- User explicitly requests skip

## Fallback Behavior (Tooling and Environment Constraints)

If required tooling or network access is unavailable, use this deterministic fallback order:

1. If `devops-skills:github-actions-validator` is unavailable, run local fallback checks:
   - `actionlint` (if installed)
   - `yamllint` (if installed)
   - manual YAML/schema review with a clear "not tool-validated" note
2. If Context7 or internet access is unavailable:
   - use `references/common-actions.md` for known action versions
   - state that external version verification could not be completed
3. If a template path is missing:
   - generate from the closest template pattern in `assets/templates/`
   - document which template was substituted

Fallback usage must always be reported in the final output.

---

## Mandatory Standards

All generated resources must follow:

| Standard | Implementation |
|----------|---------------|
| **Security** | Pin to SHA, minimal permissions, mask secrets |
| **Performance** | Caching, concurrency, shallow checkout |
| **Naming** | Descriptive names, lowercase-hyphen files |
| **Error Handling** | Timeouts, cleanup with `if: always()` |

See `references/best-practices.md` for complete guidelines.

---

## Resources

### Reference Documents

| Document | Content | When to Use |
|----------|---------|-------------|
| `references/best-practices.md` | Security, performance, patterns | Every workflow |
| `references/common-actions.md` | Action versions, inputs, outputs | Public action usage |
| `references/expressions-and-contexts.md` | `${{ }}` syntax, contexts, functions | Complex conditionals |
| `references/advanced-triggers.md` | workflow_run, dispatch, ChatOps | Workflow orchestration |
| `references/custom-actions.md` | Metadata, structure, versioning | Custom action creation |
| `references/modern-features.md` | Summaries, environments, containers | Enhanced workflows |

### Templates

| Template | Location |
|----------|----------|
| Basic Workflow | `assets/templates/workflow/basic_workflow.yml` |
| Reusable Workflow | `assets/templates/workflow/reusable_workflow.yml` |
| Composite Action | `assets/templates/action/composite/action.yml` |
| Docker Action | `assets/templates/action/docker/` |
| JavaScript Action | `assets/templates/action/javascript/` |

---

## Common Patterns

### Matrix Testing
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20, 22]
  fail-fast: false
```

### Conditional Deployment
```yaml
deploy:
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
```

### Artifact Sharing
```yaml
# Upload
- uses: actions/upload-artifact@5d5d22a31266ced268874388b861e4b58bb5c2f3 # v4.3.1
  with:
    name: build-${{ github.sha }}
    path: dist/

# Download (in dependent job)
- uses: actions/download-artifact@c850b930e6ba138125429b7e5c93fc707a7f8427 # v4.1.4
  with:
    name: build-${{ github.sha }}
```

### Third-Party Action Citation Block
```text
Third-party action citations:
- actions/checkout: https://github.com/actions/checkout (version: v6.0.2, sha: de0fac2e4500dabe0009e67214ff5f5447ce83dd, accessed: 2026-02-28)
```

---

## Done Criteria

The task is complete only when all checks below pass:

1. The request route was selected using the trigger decision tree.
2. Only the minimum required references/templates were loaded first.
3. Every third-party action is pinned to a commit SHA and has source/version citation.
4. Validation was run, or a skip exception/fallback path was explicitly documented.
5. Output includes assumptions, security-sensitive decisions (permissions/secrets), and generated file paths.

---

## Workflow Summary

1. **Route** the request using the trigger decision tree
2. **Load** the minimum references/templates for that route
3. **Generate** using mandatory security and naming standards
4. **Cite** and pin third-party actions (source, version, SHA)
5. **Validate** with `devops-skills:github-actions-validator` (or documented fallback)
6. **Fix and re-validate** until clean
7. **Present** validated output with citations, assumptions, and file paths

---

## Reference: Advanced Triggers

# Advanced GitHub Actions Triggers

**Last Updated:** November 2025

## Overview

This guide covers advanced trigger patterns for GitHub Actions workflows beyond the basic `push`, `pull_request`, and `schedule` triggers. These patterns enable workflow orchestration, external integrations, ChatOps, and complex automation scenarios.

## Table of Contents

1. [Workflow Orchestration](#workflow-orchestration)
2. [External Integration](#external-integration)
3. [ChatOps Patterns](#chatops-patterns)
4. [Deployment Triggers](#deployment-triggers)
5. [Advanced Path Filtering](#advanced-path-filtering)
6. [Security Patterns](#security-patterns)
7. [GitHub Services Integration](#github-services-integration)
8. [Best Practices](#best-practices)

---

## Workflow Orchestration

### workflow_run Trigger

The `workflow_run` trigger allows you to chain workflows together, running one workflow after another completes. This is the **recommended pattern** for handling external pull requests securely.

#### Basic Syntax

```yaml
name: Deploy Application

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]
    branches: [main, staging]
```

#### Trigger Types

- `requested` - Workflow run was requested
- `in_progress` - Workflow run is currently running
- `completed` - Workflow run has finished (success, failure, or cancelled)

#### Use Cases

**1. Deployment After CI Success**

```yaml
# deploy.yml - Separate deployment workflow
name: Deploy to Production

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    # Only deploy if CI passed
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest

    environment:
      name: production
      url: https://example.com

    steps:
      - name: Checkout code
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2

      - name: Download build artifacts from CI
        uses: actions/download-artifact@c850b930e6ba138125429b7e5c93fc707a7f8427 # v4.1.4
        with:
          name: build-artifacts
          run-id: ${{ github.event.workflow_run.id }}
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Deploy application
        run: |
          echo "Deploying commit ${{ github.event.workflow_run.head_sha }}"
          # Deployment commands here
```

**2. Security Scanning for External PRs**

```yaml
# security-scan.yml - Runs after CI for external PRs
name: Security Scan

on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

permissions:
  security-events: write
  contents: read

jobs:
  scan:
    # Only scan if CI passed and it was a PR
    if: |
      github.event.workflow_run.conclusion == 'success' &&
      github.event.workflow_run.event == 'pull_request'
    runs-on: ubuntu-latest

    steps:
      - name: Checkout PR code
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          ref: ${{ github.event.workflow_run.head_sha }}

      - name: Run security scan
        run: |
          # Security scanning without exposing secrets to PR
          npm audit --audit-level=high
```

#### Accessing Workflow Run Information

```yaml
steps:
  - name: Get workflow run details
    run: |
      echo "Workflow: ${{ github.event.workflow_run.name }}"
      echo "Conclusion: ${{ github.event.workflow_run.conclusion }}"
      echo "Head SHA: ${{ github.event.workflow_run.head_sha }}"
      echo "Head Branch: ${{ github.event.workflow_run.head_branch }}"
      echo "Run ID: ${{ github.event.workflow_run.id }}"
      echo "Event: ${{ github.event.workflow_run.event }}"
```

#### Security Benefits

✅ **Safer than `pull_request_target`** for external PRs:
- Runs with workflow file from target branch (not PR)
- No access to PR code by default
- Secrets are safe from malicious PRs
- Must explicitly checkout PR code if needed

---

## External Integration

### repository_dispatch Trigger

The `repository_dispatch` trigger allows external systems to trigger workflows via the GitHub API. This enables integration with webhooks, custom dashboards, monitoring systems, and other external tools.

#### Basic Syntax

```yaml
name: Handle External Event

on:
  repository_dispatch:
    types: [deploy-prod, deploy-staging, run-migration, rebuild-cache]
```

#### Event Types

Event types are custom strings you define. Common patterns:
- `deploy-<environment>` - Deployment triggers
- `run-<task>` - Task execution
- `notify-<event>` - Notification handling

#### Triggering via API

**Using curl:**

```bash
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{
    "event_type": "deploy-prod",
    "client_payload": {
      "version": "v1.2.3",
      "requestor": "monitoring-system",
      "environment": "production",
      "rollback": false
    }
  }'
```

**Using Python:**

```python
import requests

def trigger_deployment(repo, token, version, environment):
    url = f"https://api.github.com/repos/{repo}/dispatches"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {
        "event_type": f"deploy-{environment}",
        "client_payload": {
            "version": version,
            "requestor": "api",
            "environment": environment
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.status_code == 204
```

**Using Node.js (Octokit):**

```javascript
const { Octokit } = require("@octokit/rest");

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

await octokit.repos.createDispatchEvent({
  owner: "OWNER",
  repo: "REPO",
  event_type: "deploy-prod",
  client_payload: {
    version: "v1.2.3",
    requestor: "api",
    environment: "production"
  }
});
```

#### Handling Dispatch Events

```yaml
name: External Deployment Trigger

on:
  repository_dispatch:
    types: [deploy-prod, deploy-staging, deploy-dev]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Parse dispatch payload
        id: payload
        run: |
          echo "Event Type: ${{ github.event.action }}"
          echo "Version: ${{ github.event.client_payload.version }}"
          echo "Environment: ${{ github.event.client_payload.environment }}"
          echo "Requestor: ${{ github.event.client_payload.requestor }}"

          # Set outputs for later steps
          echo "version=${{ github.event.client_payload.version }}" >> $GITHUB_OUTPUT
          echo "environment=${{ github.event.client_payload.environment }}" >> $GITHUB_OUTPUT

      - name: Checkout specific version
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          ref: ${{ steps.payload.outputs.version }}

      - name: Deploy to environment
        env:
          ENVIRONMENT: ${{ steps.payload.outputs.environment }}
          VERSION: ${{ steps.payload.outputs.version }}
        run: |
          echo "Deploying $VERSION to $ENVIRONMENT"
          # Deployment logic here
```

#### Use Cases

**1. Webhook Integration**

Trigger workflows from external monitoring/alerting systems:

```yaml
on:
  repository_dispatch:
    types: [incident-detected, performance-degradation]

jobs:
  handle-alert:
    runs-on: ubuntu-latest
    steps:
      - name: Process alert
        run: |
          SEVERITY="${{ github.event.client_payload.severity }}"
          MESSAGE="${{ github.event.client_payload.message }}"

          echo "Alert received: $MESSAGE (Severity: $SEVERITY)"

          if [[ "$SEVERITY" == "critical" ]]; then
            # Trigger emergency procedures
            echo "Initiating critical incident response"
          fi
```

**2. Manual Trigger from Dashboard**

Custom deployment dashboard that triggers GitHub Actions:

```yaml
on:
  repository_dispatch:
    types: [dashboard-deploy]

jobs:
  deploy:
    runs-on: ubuntu-latest

    environment:
      name: ${{ github.event.client_payload.environment }}

    steps:
      - name: Validate payload
        run: |
          # Validate required fields
          if [[ -z "${{ github.event.client_payload.version }}" ]]; then
            echo "Error: version is required"
            exit 1
          fi

          if [[ -z "${{ github.event.client_payload.approver }}" ]]; then
            echo "Error: approver is required"
            exit 1
          fi

      - name: Deploy
        run: |
          echo "Deploying version ${{ github.event.client_payload.version }}"
          echo "Approved by: ${{ github.event.client_payload.approver }}"
```

**3. Cross-Repository Triggers**

Trigger workflow in repo A from repo B:

```yaml
# In Repository A
on:
  repository_dispatch:
    types: [dependency-updated]

jobs:
  rebuild:
    runs-on: ubuntu-latest
    steps:
      - name: Rebuild with new dependency
        run: |
          echo "Dependency ${{ github.event.client_payload.dependency }} updated to ${{ github.event.client_payload.version }}"
          # Rebuild logic
```

#### Security Considerations

🔒 **Token Security:**
- Use a Personal Access Token (PAT) or GitHub App token
- Minimum required scope: `repo` (for private repos) or `public_repo` (for public repos)
- Store token in secrets, never in code
- Rotate tokens regularly

🔒 **Payload Validation:**
- Always validate `client_payload` fields
- Sanitize user input to prevent injection
- Use allowlists for critical fields

```yaml
- name: Validate environment
  run: |
    ENV="${{ github.event.client_payload.environment }}"

    # Only allow specific environments
    if [[ ! "$ENV" =~ ^(dev|staging|production)$ ]]; then
      echo "Error: Invalid environment: $ENV"
      exit 1
    fi
```

---

## ChatOps Patterns

### issue_comment Trigger

The `issue_comment` trigger allows you to implement ChatOps - executing workflows via commands in issue or PR comments.

#### Basic Syntax

```yaml
name: ChatOps Commands

on:
  issue_comment:
    types: [created, edited]
```

#### Comment Types

- `created` - New comment posted
- `edited` - Comment was edited
- `deleted` - Comment was deleted (rarely used)

#### Implementing ChatOps Commands

**Full ChatOps Example:**

```yaml
name: ChatOps - Deploy Command

on:
  issue_comment:
    types: [created]

jobs:
  deploy:
    # Security checks (CRITICAL!)
    if: |
      github.event.issue.pull_request &&
      startsWith(github.event.comment.body, '/deploy') &&
      contains(fromJSON('["OWNER", "MEMBER", "COLLABORATOR"]'), github.event.comment.author_association)

    runs-on: ubuntu-latest

    permissions:
      contents: read
      pull-requests: write
      deployments: write

    steps:
      # Step 1: React to comment to show command received
      - name: Add reaction to comment
        uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
        with:
          script: |
            await github.rest.reactions.createForIssueComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              comment_id: context.payload.comment.id,
              content: 'rocket'
            });

      # Step 2: Parse command and arguments
      - name: Parse deploy command
        id: parse
        run: |
          COMMAND="${{ github.event.comment.body }}"

          # Extract environment (default: staging)
          ENV=$(echo "$COMMAND" | grep -oP '/deploy\s+\K\w+' || echo 'staging')

          # Validate environment
          if [[ ! "$ENV" =~ ^(dev|staging|production)$ ]]; then
            echo "error=Invalid environment: $ENV" >> $GITHUB_OUTPUT
            exit 1
          fi

          echo "environment=$ENV" >> $GITHUB_OUTPUT
          echo "pr_number=${{ github.event.issue.number }}" >> $GITHUB_OUTPUT

      # Step 3: Get PR details
      - name: Get PR branch
        id: pr
        uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
        with:
          script: |
            const pr = await github.rest.pulls.get({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: ${{ steps.parse.outputs.pr_number }}
            });

            core.setOutput('ref', pr.data.head.ref);
            core.setOutput('sha', pr.data.head.sha);
            core.setOutput('repo', pr.data.head.repo.full_name);

      # Step 4: Checkout PR code
      - name: Checkout PR code
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          ref: ${{ steps.pr.outputs.ref }}
          repository: ${{ steps.pr.outputs.repo }}

      # Step 5: Deploy
      - name: Deploy to environment
        id: deploy
        env:
          ENVIRONMENT: ${{ steps.parse.outputs.environment }}
          PR_SHA: ${{ steps.pr.outputs.sha }}
        run: |
          echo "Deploying PR #${{ steps.parse.outputs.pr_number }} to $ENVIRONMENT"
          echo "SHA: $PR_SHA"

          # Deployment logic here
          DEPLOY_URL="https://$ENVIRONMENT.example.com"
          echo "url=$DEPLOY_URL" >> $GITHUB_OUTPUT

      # Step 6: Comment with results
      - name: Comment deployment result
        uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
        with:
          script: |
            const environment = '${{ steps.parse.outputs.environment }}';
            const url = '${{ steps.deploy.outputs.url }}';

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: ${{ steps.parse.outputs.pr_number }},
              body: `✅ Deployed to **${environment}**\n\n🔗 ${url}\n\nTriggered by: @${{ github.event.comment.user.login }}`
            });

      # Step 7: Handle failures
      - name: Comment on failure
        if: failure()
        uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
        with:
          script: |
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: ${{ github.event.issue.number }},
              body: `❌ Deployment failed\n\nCheck the [workflow run](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}) for details.`
            });
```

#### Common ChatOps Commands

**1. /deploy [environment]**
```yaml
startsWith(github.event.comment.body, '/deploy')
```

**2. /run-tests [suite]**
```yaml
startsWith(github.event.comment.body, '/run-tests')
```

**3. /benchmark**
```yaml
contains(github.event.comment.body, '/benchmark')
```

**4. /approve**
```yaml
github.event.comment.body == '/approve'
```

#### Permission Checking

**Author Association Levels:**

- `OWNER` - Repository owner
- `MEMBER` - Organization member
- `COLLABORATOR` - Repository collaborator
- `CONTRIBUTOR` - Has contributed to repo
- `FIRST_TIME_CONTRIBUTOR` - First contribution
- `FIRST_TIMER` - First time interacting
- `NONE` - No association

**Check permissions:**

```yaml
# Only owners and members
if: contains(fromJSON('["OWNER", "MEMBER"]'), github.event.comment.author_association)

# More permissive
if: contains(fromJSON('["OWNER", "MEMBER", "COLLABORATOR", "CONTRIBUTOR"]'), github.event.comment.author_association)
```

**Advanced permission check with team membership:**

```yaml
steps:
  - name: Check team membership
    uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
    with:
      script: |
        const teams = ['deployment-team', 'admin-team'];
        const user = context.payload.comment.user.login;

        let authorized = false;
        for (const team of teams) {
          try {
            await github.rest.teams.getMembershipForUserInOrg({
              org: context.repo.owner,
              team_slug: team,
              username: user
            });
            authorized = true;
            break;
          } catch (error) {
            // User not in this team
          }
        }

        if (!authorized) {
          core.setFailed(`User ${user} not authorized`);
        }
```

#### Security Best Practices for ChatOps

🔒 **Always validate:**
1. Command is from a PR: `github.event.issue.pull_request`
2. User has permissions: `github.event.comment.author_association`
3. Command format is valid
4. Arguments are sanitized

🔒 **Never:**
- Execute arbitrary code from comments
- Use comment content in shell commands without validation
- Trust external PR authors for sensitive operations

🔒 **Use environment variables:**

```yaml
# BAD - Command injection risk
- run: echo ${{ github.event.comment.body }}

# GOOD - Safe
- env:
    COMMENT: ${{ github.event.comment.body }}
  run: echo "$COMMENT"
```

---

## Deployment Triggers

### deployment and deployment_status

These triggers integrate with GitHub's deployment API.

#### deployment Trigger

```yaml
name: Handle Deployment

on:
  deployment:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Get deployment info
        run: |
          echo "Environment: ${{ github.event.deployment.environment }}"
          echo "Ref: ${{ github.event.deployment.ref }}"
          echo "Task: ${{ github.event.deployment.task }}"
          echo "Payload: ${{ toJSON(github.event.deployment.payload) }}"
```

#### deployment_status Trigger

```yaml
name: Post-Deployment Actions

on:
  deployment_status:

jobs:
  notify:
    if: github.event.deployment_status.state == 'success'
    runs-on: ubuntu-latest

    steps:
      - name: Send notification
        run: |
          echo "Deployment to ${{ github.event.deployment.environment }} succeeded"
          # Send Slack/email notification
```

---

## Advanced Path Filtering

### Complex Path Patterns

```yaml
on:
  push:
    paths:
      # Include specific paths
      - 'src/**'
      - 'lib/**/*.js'

      # Exclude paths (ignore)
      - '!src/**/*.md'
      - '!src/**/*.test.js'
      - '!**/__tests__/**'

      # Only specific file types
      - '**.py'
      - '**.yaml'
      - '**.yml'
```

### Path Filters with Multiple Triggers

```yaml
on:
  pull_request:
    paths:
      - 'backend/**'
  push:
    branches: [main]
    paths:
      - 'backend/**'
```

### Monorepo Path Filtering

```yaml
on:
  pull_request:
    paths:
      - 'packages/frontend/**'
      - 'packages/shared/**'
      - '!packages/**/README.md'
      - '!packages/**/*.test.*'
```

---

## Security Patterns

### pull_request vs pull_request_target

| Trigger | Context | Secrets | Use Case | Risk Level |
|---------|---------|---------|----------|------------|
| `pull_request` | PR branch | ❌ No access | Standard PR validation | ✅ Safe |
| `pull_request_target` | Target branch | ✅ Full access | Write to PR from fork | ⚠️ High risk |
| `workflow_run` | Target branch | ✅ Full access | Post-CI for external PRs | ✅ Safe (if used correctly) |

### Safe Patterns

**✅ Standard PR validation:**

```yaml
on:
  pull_request:
    branches: [main]

# Safe: No secrets exposed, runs PR code in isolation
```

**✅ Post-CI processing with workflow_run:**

```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

# Safe: Runs after CI, has secrets, but uses target branch code
```

**⚠️ Dangerous: pull_request_target**

```yaml
on:
  pull_request_target:
    branches: [main]

# DANGEROUS: External PRs can access secrets!
# Only use if you explicitly checkout target branch code
```

### Securing pull_request_target

If you must use `pull_request_target`:

```yaml
on:
  pull_request_target:

jobs:
  comment:
    runs-on: ubuntu-latest

    steps:
      # SAFE: Don't checkout PR code
      - name: Comment on PR
        uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
        with:
          script: |
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'Thanks for your contribution!'
            });

      # UNSAFE: Never do this!
      # - uses: actions/checkout@v4
      #   with:
      #     ref: ${{ github.event.pull_request.head.sha }}
```

---

## GitHub Services Integration

### check_run and check_suite

```yaml
on:
  check_run:
    types: [created, rerequested, completed]

on:
  check_suite:
    types: [completed, requested]
```

### status

```yaml
on:
  status:

jobs:
  handle-status:
    runs-on: ubuntu-latest
    steps:
      - name: Check status
        run: |
          echo "State: ${{ github.event.state }}"
          echo "Context: ${{ github.event.context }}"
```

### package

```yaml
on:
  package:
    types: [published, updated]
```

---

## Best Practices

### 1. Choose the Right Trigger

| Scenario | Recommended Trigger |
|----------|-------------------|
| Standard PR validation | `pull_request` |
| External PR with secrets | `workflow_run` after `pull_request` |
| Deploy after CI | `workflow_run` |
| Manual dashboard trigger | `repository_dispatch` |
| ChatOps commands | `issue_comment` |
| Scheduled cleanup | `schedule` |
| External webhook | `repository_dispatch` |

### 2. Security Checklist

- [ ] Validate user permissions
- [ ] Sanitize all inputs
- [ ] Use environment variables, not direct interpolation
- [ ] Never trust external PR code with secrets
- [ ] Use `workflow_run` instead of `pull_request_target` when possible
- [ ] Implement allowlists for critical operations
- [ ] Log all security-sensitive actions

### 3. Performance Optimization

- Use `workflow_run` to separate slow jobs from fast CI
- Filter triggers with `paths` to avoid unnecessary runs
- Use `concurrency` to cancel outdated runs
- Implement conditional job execution

### 4. Debugging

**Check trigger details:**

```yaml
- name: Debug trigger info
  run: |
    echo "Event name: ${{ github.event_name }}"
    echo "Event: ${{ toJSON(github.event) }}"
```

**Test repository_dispatch locally:**

```bash
# Set token
export GITHUB_TOKEN="your_token"

# Trigger workflow
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type":"test","client_payload":{"debug":true}}'
```

---

## Example Workflows

See the `examples/triggers/` directory for complete working examples:

- `workflow-orchestration.yml` - CI → Deploy workflow chaining
- `repository-dispatch.yml` - External API triggers
- `chatops-commands.yml` - Full ChatOps implementation

---

## Resources

- [GitHub Actions Events Documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [Security Hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
- [GitHub API - Repository Dispatch](https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event)

---

## Reference: Best Practices

# GitHub Actions Best Practices

**Last Updated:** November 2025
**Based on:** Official GitHub Actions documentation and Context7 verified sources

## Table of Contents
1. [Security Best Practices](#security-best-practices)
2. [Performance Optimization](#performance-optimization)
3. [Workflow Design](#workflow-design)
4. [Action Selection and Versioning](#action-selection-and-versioning)
5. [Error Handling](#error-handling)
6. [Maintainability](#maintainability)
7. [Common Patterns](#common-patterns)
8. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

## Security Best Practices

### 1. Pin Actions to Full SHA (Critical Security Practice)

**Best Practice:**
```yaml
# ✅ BEST: Pinned to specific full SHA (40 characters) with version comment
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
```

**Why:**
- Immutable: SHA cannot be changed, preventing supply chain attacks
- Reproducible: Same code runs every time
- Verifiable: Can audit exact code being executed

**Acceptable Alternative:**
```yaml
# ✅ ACCEPTABLE: Major version tag (for official GitHub actions)
- uses: actions/checkout@v4
```

**Avoid:**
```yaml
# ❌ BAD: Mutable references
- uses: actions/checkout@main
- uses: actions/checkout@master
- uses: actions/checkout@latest
```

### 2. Minimal Permissions

**Best Practice:**
```yaml
# Top-level: Set default to read-only
permissions:
  contents: read

jobs:
  build:
    # Job-level: Grant only necessary permissions
    permissions:
      contents: read
      packages: write
      pull-requests: write
```

**Common Permission Scopes:**
- `contents`: Repository contents (read/write)
- `packages`: GitHub Packages (read/write)
- `pull-requests`: PR comments and labels (read/write)
- `issues`: Issue management (read/write)
- `statuses`: Commit statuses (write)
- `checks`: Check runs (write)
- `deployments`: Deployment status (write)

### 3. Secrets Management

**Best Practice:**
```yaml
# ✅ GOOD: Use secrets properly
- name: Deploy to production
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    echo "::add-mask::$API_KEY"
    ./deploy.sh

# ✅ GOOD: Pass secrets to actions
- uses: aws-actions/configure-aws-credentials@v4
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**Avoid:**
```yaml
# ❌ BAD: Exposing secrets
- run: echo "API_KEY=${{ secrets.API_KEY }}"

# ❌ BAD: Using secrets in URLs
- run: git clone https://${{ secrets.GITHUB_TOKEN }}@github.com/user/repo.git
```

### 4. Input Validation and Injection Prevention

**Critical Security Issue:** Script injection through untrusted input is one of the most common security vulnerabilities in GitHub Actions.

**Best Practice - Use Environment Variables:**
```yaml
# ✅ BEST: Always use environment variables for untrusted input (Bash)
- name: Check PR title
  env:
    TITLE: ${{ github.event.pull_request.title }}
  run: |
    if [[ "$TITLE" =~ ^octocat ]]; then
      echo "PR title starts with 'octocat'"
      exit 0
    else
      echo "PR title did not start with 'octocat'"
      exit 1
    fi

# ✅ BEST: Validate inputs with strict patterns
- name: Build image
  env:
    IMAGE_NAME: ${{ github.event.inputs.image-name }}
  run: |
    if [[ ! "$IMAGE_NAME" =~ ^[a-z0-9-]+$ ]]; then
      echo "::error::Invalid image name"
      exit 1
    fi
    docker build -t "$IMAGE_NAME" .
```

**Alternative - Use JavaScript Action:**
```yaml
# ✅ GOOD: Create a JavaScript action to process context values
- uses: fakeaction/checktitle@v3
  with:
    title: ${{ github.event.pull_request.title }}
```

**Avoid:**
```yaml
# ❌ BAD: Direct interpolation of user input (vulnerable to injection)
- run: echo "PR: ${{ github.event.pull_request.title }}"
- run: docker build -t ${{ github.event.inputs.tag }} .
- run: echo "${{ github.event.pull_request.title }}" | grep "fix"
```

### 5. Dependency Review and SBOM Attestations (New in 2025)

**Dependency Review Action:**
```yaml
name: Dependency Review
on:
  pull_request:
    paths-ignore:
      - "README.md"

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2

      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          # Fail on critical vulnerabilities
          fail-on-severity: critical
          # Allow specific dependencies
          allow-licenses: MIT, Apache-2.0, BSD-3-Clause
```

**SBOM Attestations for Container Images:**
```yaml
permissions:
  id-token: write
  contents: read
  attestations: write
  packages: write

steps:
  - name: Build container image
    run: docker build -t ${{ env.REGISTRY }}/myapp:${{ github.sha }} .

  - name: Generate SBOM
    uses: anchore/sbom-action@v0
    with:
      image: ${{ env.REGISTRY }}/myapp:${{ github.sha }}
      format: spdx-json
      output-file: sbom.json

  - name: Generate SBOM attestation
    uses: actions/attest-sbom@v2
    with:
      subject-name: ${{ env.REGISTRY }}/myapp
      subject-digest: sha256:${{ steps.build.outputs.digest }}
      sbom-path: sbom.json
      push-to-registry: true
```

## Performance Optimization

### 1. Dependency Caching (Updated November 2025)

**Important:** actions/cache v5.0.3 is recommended (Node 24 runtime). The cache service was rewritten for improved performance in 2025. Legacy cache service was sunset on February 1, 2025.

**Cache Size Limits (New):** As of November 2025, repositories can exceed the previous 10 GB cache limit using a pay-as-you-go model. All repositories receive 10 GB free, with additional storage available.

**NPM/Node.js with Built-in Caching:**
```yaml
- uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 # v6.2.0
  with:
    node-version: '24'
    cache: 'npm'
    cache-dependency-path: '**/package-lock.json'
```

**Manual Caching with actions/cache@v5:**
```yaml
- name: Cache node modules
  id: cache-npm
  uses: actions/cache@cdf6c1fa76f9f475f3d7449005a359c84ca0f306 # v5.0.3
  env:
    cache-name: cache-node-modules
  with:
    path: ~/.npm
    key: ${{ runner.os }}-build-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-build-${{ env.cache-name }}-
      ${{ runner.os }}-build-
      ${{ runner.os }}-

- name: Check cache hit
  if: ${{ steps.cache-npm.outputs.cache-hit != 'true' }}
  run: echo "Cache miss - installing dependencies"

- name: Install dependencies
  run: npm ci
```

**Maven with Built-in Caching:**
```yaml
- uses: actions/setup-java@387ac29b308b003ca37ba93a6cab5eb57c8f5f93 # v4.0.0
  with:
    java-version: '17'
    distribution: 'temurin'
    cache: 'maven'
```

**Ruby Gems with Matrix Strategy:**
```yaml
- uses: actions/cache@cdf6c1fa76f9f475f3d7449005a359c84ca0f306 # v5.0.3
  with:
    path: vendor/bundle
    key: bundle-${{ matrix.os }}-${{ matrix.ruby-version }}-${{ hashFiles('**/Gemfile.lock') }}
    restore-keys: |
      bundle-${{ matrix.os }}-${{ matrix.ruby-version }}-
```

**.NET Dependencies:**
```yaml
- uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '8.x'
    cache: true  # Caches NuGet global-packages folder
```

### 2. Concurrency Control

**Best Practice:**
```yaml
# Cancel in-progress runs when new commit pushed
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Per-PR Concurrency:**
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

### 3. Shallow Checkout

**Best Practice:**
```yaml
# ✅ GOOD: Shallow clone when full history not needed
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
  with:
    fetch-depth: 1

# ✅ GOOD: Fetch specific depth for changelog generation
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
  with:
    fetch-depth: 50
```

### 4. Matrix Strategy Optimization

**Best Practice:**
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    node: [18, 20, 22]
    exclude:
      # Exclude expensive combinations
      - os: macos-latest
        node: 18
  fail-fast: false  # Continue other jobs even if one fails
  max-parallel: 3   # Limit concurrent jobs
```

## Workflow Design

### 1. Job Dependencies

**Best Practice:**
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    needs: [lint, test]  # Wait for both
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh
```

### 2. Conditional Execution

**Best Practice:**
```yaml
# Job-level condition
jobs:
  deploy:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

# Step-level condition
steps:
  - name: Deploy to staging
    if: github.ref == 'refs/heads/develop'
    run: ./deploy-staging.sh

  - name: Notify on failure
    if: failure()
    run: ./notify.sh
```

**Common Conditions:**
- `success()`: Previous steps succeeded
- `failure()`: Any previous step failed
- `always()`: Run regardless of status
- `cancelled()`: Workflow was cancelled

### 3. Reusable Workflows

**Caller Workflow:**
```yaml
# .github/workflows/ci.yml
jobs:
  call-workflow:
    uses: ./.github/workflows/reusable-build.yml
    with:
      environment: production
    secrets:
      token: ${{ secrets.DEPLOY_TOKEN }}
```

**Reusable Workflow:**
```yaml
# .github/workflows/reusable-build.yml
name: Reusable Build

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      node-version:
        required: false
        type: string
        default: '20'
    secrets:
      token:
        required: true
    outputs:
      build-id:
        description: "Build identifier"
        value: ${{ jobs.build.outputs.id }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      id: ${{ steps.build.outputs.id }}
    steps:
      - name: Build
        id: build
        run: echo "id=build-${{ github.sha }}" >> $GITHUB_OUTPUT
```

## Action Selection and Versioning

### 1. Prefer Official GitHub Actions

**Priority Order:**
1. Official GitHub actions (`actions/*`)
2. Official organization actions (`docker/*`, `aws-actions/*`)
3. Verified creators
4. Community actions (with careful review)

### 2. Version Pinning Strategy

**Recommended Approach:**
```yaml
# Format: @<SHA> # <version-tag>
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
```

**Finding SHAs:**
```bash
# Get SHA for specific tag
git ls-remote https://github.com/actions/checkout v4.1.1
```

### 3. Regular Updates

**Process:**
1. Monitor action releases and security advisories
2. Update SHAs with new versions
3. Test in PR before merging
4. Document version changes in commit message

**Automated Updates:**
Use Dependabot for automatic action updates:
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Error Handling

### 1. Timeouts

**Best Practice:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30  # Prevent hung jobs
    steps:
      - name: Run tests
        timeout-minutes: 15  # Step-level timeout
        run: npm test
```

### 2. Failure Handling

**Best Practice:**
```yaml
jobs:
  test:
    steps:
      - name: Run tests
        id: tests
        continue-on-error: true
        run: npm test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@5d5d22a31266ced268874388b861e4b58bb5c2f3 # v4.3.1
        with:
          name: test-results
          path: test-results/

      - name: Check test results
        if: steps.tests.outcome == 'failure'
        run: exit 1
```

### 3. Cleanup Steps

**Best Practice:**
```yaml
steps:
  - name: Start test environment
    run: docker-compose up -d

  - name: Run tests
    run: npm test

  - name: Cleanup
    if: always()
    run: docker-compose down
```

## Maintainability

### 1. Naming Conventions

**Best Practice:**
```yaml
# Workflow file: lowercase with hyphens
# File: .github/workflows/ci-pipeline.yml

name: CI Pipeline  # Descriptive workflow name

jobs:
  test-node:  # Descriptive job ID
    name: Test on Node ${{ matrix.version }}  # Human-readable job name
    steps:
      - name: Install dependencies  # Action-oriented step name
        run: npm ci
```

### 2. Documentation

**Best Practice:**
```yaml
# CI Pipeline
#
# This workflow runs on every push and pull request to validate code quality.
# It performs linting, testing, and builds the application.
#
# Required secrets:
#   - CODECOV_TOKEN: For uploading coverage reports
#
# Required permissions:
#   - contents: read
#   - checks: write

name: CI Pipeline
```

### 3. Environment Variables

**Best Practice:**
```yaml
# Top-level environment variables
env:
  NODE_VERSION: '20'
  CACHE_VERSION: 'v1'

jobs:
  build:
    env:
      BUILD_ENV: production
    steps:
      - name: Build
        env:
          API_URL: ${{ secrets.API_URL }}
        run: npm run build
```

## Common Patterns

### 1. Multi-Environment Deployment

```yaml
jobs:
  deploy-staging:
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Deploy to staging
        run: ./deploy.sh staging

  deploy-production:
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Deploy to production
        run: ./deploy.sh production
```

### 2. Manual Approval

```yaml
jobs:
  deploy:
    environment:
      name: production
      # Requires manual approval from configured reviewers
    steps:
      - name: Deploy
        run: ./deploy.sh
```

### 3. Artifact Sharing Between Jobs

```yaml
jobs:
  build:
    steps:
      - name: Build application
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@5d5d22a31266ced268874388b861e4b58bb5c2f3 # v4.3.1
        with:
          name: build-${{ github.sha }}
          path: dist/
          retention-days: 7

  test:
    needs: build
    steps:
      - name: Download build artifacts
        uses: actions/download-artifact@c850b930e6ba138125429b7e5c93fc707a7f8427 # v4.1.4
        with:
          name: build-${{ github.sha }}
          path: dist/

      - name: Test build
        run: npm run test:integration
```

### 4. Dynamic Matrix from JSON

```yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - name: Set matrix
        id: set-matrix
        run: |
          echo 'matrix={"version":["18","20","22"]}' >> $GITHUB_OUTPUT

  test:
    needs: setup
    strategy:
      matrix: ${{ fromJSON(needs.setup.outputs.matrix) }}
```

## Anti-Patterns to Avoid

### 1. Storing Secrets in Code

```yaml
# ❌ NEVER DO THIS
env:
  API_KEY: "hardcoded-secret-123"
  PASSWORD: ${{ github.event.inputs.password }}
```

### 2. Using Deprecated Actions

```yaml
# ❌ BAD: Deprecated actions
- uses: actions/setup-node@v1  # Use v6 instead (Node 24 runtime)
- uses: actions/cache@v1       # Use v5.0.3+ instead (Node 24 runtime, required as of Feb 2025)
```

### 3. Overly Broad Permissions

```yaml
# ❌ BAD: Unnecessary permissions
permissions: write-all

# ✅ GOOD: Minimal permissions
permissions:
  contents: read
  pull-requests: write
```

### 4. Long-Running Jobs Without Timeout

```yaml
# ❌ BAD: No timeout
jobs:
  build:
    runs-on: ubuntu-latest
    # Could run forever, consuming minutes

# ✅ GOOD: With timeout
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30
```

### 5. Hardcoded Values

```yaml
# ❌ BAD: Hardcoded
- name: Deploy
  run: kubectl set image deployment/myapp myapp=myapp:1.0.0

# ✅ GOOD: Using variables
- name: Deploy
  env:
    IMAGE_TAG: ${{ github.sha }}
  run: kubectl set image deployment/myapp myapp=myapp:$IMAGE_TAG
```

### 6. Unnecessary Checkouts

```yaml
# ❌ BAD: Checkout when not needed
jobs:
  notify:
    steps:
      - uses: actions/checkout@v4  # Not needed for notification
      - run: ./notify.sh

# ✅ GOOD: Only checkout when needed
jobs:
  notify:
    steps:
      - run: curl -X POST ${{ secrets.WEBHOOK_URL }}
```

## Summary

**Key Takeaways:**
1. Security first: Pin actions, use minimal permissions, protect secrets
2. Optimize performance: Cache dependencies, use concurrency controls
3. Design for maintainability: Clear naming, documentation, reusable components
4. Handle errors gracefully: Timeouts, cleanup, notifications
5. Follow conventions: Standard naming, proper versioning, community practices

Always validate workflows with the github-actions-validator skill before deploying.

---

## Reference: Common Actions

# Common GitHub Actions Reference

**Last Updated:** February 2026
**Source:** Official GitHub Actions repositories and Context7 verified documentation

This document catalogs frequently used GitHub Actions with current versions, inputs, outputs, and usage examples.

**Important Notes for 2026:**
- All actions should be pinned to full 40-character SHA for security
- Node 24 runtime is now supported (Node 20 EOL: April 2026, default switch: March 4, 2026)
- actions/cache v5.0.3 recommended (Node 24 runtime, runner v2.327.1+)
- Cache size limits: 10 GB free per repository, additional storage available (as of February 2026)

## Table of Contents
1. [Repository and Checkout](#repository-and-checkout)
2. [Language and Tool Setup](#language-and-tool-setup)
3. [Caching](#caching)
4. [Artifacts](#artifacts)
5. [Docker](#docker)
6. [Cloud Providers](#cloud-providers)
7. [Testing and Code Quality](#testing-and-code-quality)
8. [Notifications](#notifications)
9. [Release and Publishing](#release-and-publishing)
10. [Security](#security)

## Repository and Checkout

### actions/checkout

**Latest Version:** v6 (v6.0.2)
**SHA:** `de0fac2e4500dabe0009e67214ff5f5447ce83dd`
**Minimum Runner:** v2.327.1+

**Description:** Checkout repository code with improved performance, tag handling, and security

**Common Inputs:**
- `fetch-depth`: Number of commits to fetch (default: 1, use 0 for full history)
- `ref`: Branch, tag, or SHA to checkout
- `token`: PAT for private repos (default: `${{ github.token }}`)
- `submodules`: Whether to checkout submodules (`false`, `true`, `recursive`)
- `lfs`: Whether to download Git LFS files (default: `false`)
- `sparse-checkout`: Paths to checkout (cone mode or individual files) - **Available in v5+**
- `sparse-checkout-cone-mode`: Use cone mode for sparse checkout (default: `true`)

**Required Permissions:**
```yaml
permissions:
  contents: read
```

**Examples:**

**Basic checkout:**
```yaml
- name: Checkout code
  uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
  with:
    fetch-depth: 1
```

**Full history (for changelog/tags):**
```yaml
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
  with:
    fetch-depth: 0
```

**Sparse checkout (specific directories):**
```yaml
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
  with:
    sparse-checkout: |
      .github
      src
      tests
```

**Checkout PR HEAD commit:**
```yaml
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
  with:
    ref: ${{ github.event.pull_request.head.sha }}
```

**Checkout private repository:**
```yaml
- uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
  with:
    repository: my-org/my-private-repo
    token: ${{ secrets.GH_PAT }}
    path: my-repo
```

## Language and Tool Setup

### actions/setup-node

**Latest Version:** v6 (v6.2.0)
**SHA:** `6044e13b5dc448c55e2357c09f80417699197238`
**Minimum Runner:** v2.328.0+ (for Node 24 support)

**Description:** Setup Node.js environment with Node 24 support

**Important:** Node 24 runtime is now supported. Node 20 deprecation timeline: Default switch March 4, 2026 → EOL April 2026 → Complete removal Summer 2026.

**Common Inputs:**
- `node-version`: Version to use (e.g., `'24'`, `'20'`, `'18.x'`, `'lts/*'`)
- `cache`: Package manager to cache (`'npm'`, `'yarn'`, `'pnpm'`)
- `cache-dependency-path`: Path to lock file(s)
- `registry-url`: NPM registry URL for publishing
- `always-auth`: Set always-auth in npmrc (default: `false`)

**Examples:**

**Basic setup with caching:**
```yaml
- name: Setup Node.js 24
  uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 # v6.2.0
  with:
    node-version: '24'
    cache: 'npm'
```

**Multi-lock-file caching:**
```yaml
- uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 # v6.2.0
  with:
    node-version: '24'
    cache: 'npm'
    cache-dependency-path: |
      package-lock.json
      packages/*/package-lock.json
```

**Setup for package publishing:**
```yaml
- uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 # v6.2.0
  with:
    node-version: '20'
    registry-url: 'https://registry.npmjs.org'

- run: npm publish
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### actions/setup-python

**Latest Version:** v6 (v6.2.0)
**SHA:** `a309ff8b426b58ec0e2a45f0f869d46889d02405`

**Description:** Setup Python environment

**Common Inputs:**
- `python-version`: Version to use (e.g., `'3.11'`, `'3.x'`)
- `cache`: Package manager to cache (`'pip'`, `'pipenv'`, `'poetry'`)
- `cache-dependency-path`: Path to requirements file

**Example:**
```yaml
- name: Setup Python
  uses: actions/setup-python@a309ff8b426b58ec0e2a45f0f869d46889d02405 # v6.2.0
  with:
    python-version: '3.11'
    cache: 'pip'
    cache-dependency-path: 'requirements*.txt'
```

### actions/setup-java

**Latest Version:** v4 (v4.0.0)
**SHA:** `387ac29b308b003ca37ba93a6cab5eb57c8f5f93`

**Description:** Setup Java environment

**Common Inputs:**
- `distribution`: Java distribution (`'temurin'`, `'zulu'`, `'adopt'`, etc.)
- `java-version`: Version to use (e.g., `'17'`, `'11'`)
- `cache`: Build tool to cache (`'maven'`, `'gradle'`, `'sbt'`)

**Example:**
```yaml
- name: Setup Java
  uses: actions/setup-java@387ac29b308b003ca37ba93a6cab5eb57c8f5f93 # v4.0.0
  with:
    distribution: 'temurin'
    java-version: '17'
    cache: 'maven'
```

### actions/setup-go

**Latest Version:** v5 (v5.0.0)
**SHA:** `0c52d547c9bc32b1aa3301fd7a9cb496313a4491`

**Description:** Setup Go environment

**Common Inputs:**
- `go-version`: Version to use (e.g., `'1.21'`, `'stable'`)
- `cache`: Whether to cache dependencies (default: `true`)
- `cache-dependency-path`: Path to go.sum

**Example:**
```yaml
- name: Setup Go
  uses: actions/setup-go@0c52d547c9bc32b1aa3301fd7a9cb496313a4491 # v5.0.0
  with:
    go-version: '1.21'
    cache-dependency-path: go.sum
```

## Caching

### actions/cache

**Latest Version:** v5 (v5.0.3)
**SHA:** `cdf6c1fa76f9f475f3d7449005a359c84ca0f306`

**Description:** Cache dependencies and build outputs with Node 24 runtime support

**Important:** actions/cache v5 requires GitHub Actions runner v2.327.1 or later. Repositories get 10 GB free cache storage, with additional storage available.

**Required Inputs:**
- `path`: Directories to cache
- `key`: Cache key (must be unique)

**Optional Inputs:**
- `restore-keys`: Fallback keys if exact key not found

**Example:**
```yaml
- name: Cache dependencies
  uses: actions/cache@cdf6c1fa76f9f475f3d7449005a359c84ca0f306 # v5.0.3
  with:
    path: |
      ~/.npm
      ~/.cache
      node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

## Artifacts

### actions/upload-artifact

**Latest Version:** v4 (v4.3.1)
**SHA:** `5d5d22a31266ced268874388b861e4b58bb5c2f3`

**Description:** Upload build artifacts

**Required Inputs:**
- `name`: Artifact name
- `path`: Files to upload

**Optional Inputs:**
- `retention-days`: How long to keep artifact (1-90, default: 90)
- `if-no-files-found`: What to do if no files found (`warn`, `error`, `ignore`)

**Example:**
```yaml
- name: Upload build artifacts
  uses: actions/upload-artifact@5d5d22a31266ced268874388b861e4b58bb5c2f3 # v4.3.1
  with:
    name: build-${{ github.sha }}
    path: dist/
    retention-days: 7
    if-no-files-found: error
```

### actions/download-artifact

**Latest Version:** v4 (v4.1.4)
**SHA:** `c850b930e6ba138125429b7e5c93fc707a7f8427`

**Description:** Download artifacts from previous jobs

**Optional Inputs:**
- `name`: Artifact name (downloads all if not specified)
- `path`: Destination path

**Example:**
```yaml
- name: Download build artifacts
  uses: actions/download-artifact@c850b930e6ba138125429b7e5c93fc707a7f8427 # v4.1.4
  with:
    name: build-${{ github.sha }}
    path: dist/
```

## Docker

### docker/setup-buildx-action

**Latest Version:** v3 (v3.3.0)
**SHA:** `d70bba72b1f3fd22344832f00baa16ece964efeb`

**Description:** Setup Docker Buildx for advanced builds

**Example:**
```yaml
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@d70bba72b1f3fd22344832f00baa16ece964efeb # v3.3.0
```

### docker/login-action

**Latest Version:** v3 (v3.1.0)
**SHA:** `e92390c5fb421da1463c202d546fed0ec5c39f20`

**Description:** Login to Docker registry

**Common Inputs:**
- `registry`: Registry to login to (default: Docker Hub)
- `username`: Username
- `password`: Password or token

**Example:**
```yaml
# Docker Hub
- name: Login to Docker Hub
  uses: docker/login-action@e92390c5fb421da1463c202d546fed0ec5c39f20 # v3.1.0
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

# GitHub Container Registry
- name: Login to GHCR
  uses: docker/login-action@e92390c5fb421da1463c202d546fed0ec5c39f20 # v3.1.0
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

### docker/build-push-action

**Latest Version:** v5 (v5.3.0)
**SHA:** `2cdde995de11925a030ce8070c3d77a52ffcf1c0`

**Description:** Build and push Docker images

**Common Inputs:**
- `context`: Build context path
- `file`: Dockerfile path
- `push`: Whether to push image (default: `false`)
- `tags`: Image tags
- `platforms`: Target platforms (e.g., `linux/amd64,linux/arm64`)
- `cache-from`: Cache sources
- `cache-to`: Cache destinations
- `build-args`: Build arguments
- `secrets`: Build secrets

**Example:**
```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@2cdde995de11925a030ce8070c3d77a52ffcf1c0 # v5.3.0
  with:
    context: .
    platforms: linux/amd64,linux/arm64
    push: true
    tags: |
      user/app:latest
      user/app:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
    build-args: |
      VERSION=${{ github.sha }}
      BUILD_DATE=${{ github.event.head_commit.timestamp }}
```

## Cloud Providers

### aws-actions/configure-aws-credentials

**Latest Version:** v4 (v4.0.2)
**SHA:** `e3dd6a429d7300a6a4c196c26e071d42e0343502`

**Description:** Configure AWS credentials for GitHub Actions

**Common Inputs:**
- `aws-access-key-id`: AWS access key ID
- `aws-secret-access-key`: AWS secret access key
- `aws-region`: AWS region
- `role-to-assume`: IAM role ARN for OIDC
- `role-session-name`: Session name

**Example (with secrets):**
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502 # v4.0.2
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: us-east-1
```

**Example (with OIDC - preferred):**
```yaml
- name: Configure AWS credentials
  uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502 # v4.0.2
  with:
    role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsRole
    role-session-name: GitHubActions-${{ github.run_id }}
    aws-region: us-east-1
```

### azure/login

**Latest Version:** v2 (v2.0.0)
**SHA:** `6c251865b4e6290e7b78be643ea2d005a6c79ee5`

**Description:** Login to Azure

**Common Inputs:**
- `creds`: Azure credentials JSON
- `client-id`: Service principal client ID (for OIDC)
- `tenant-id`: Azure tenant ID (for OIDC)
- `subscription-id`: Azure subscription ID (for OIDC)

**Example:**
```yaml
- name: Azure Login
  uses: azure/login@6c251865b4e6290e7b78be643ea2d005a6c79ee5 # v2.0.0
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}
```

## Testing and Code Quality

### codecov/codecov-action

**Latest Version:** v4 (v4.0.1)
**SHA:** `e0b68c6749509c5f83f984dd99a76a1c1a231044`

**Description:** Upload code coverage to Codecov

**Common Inputs:**
- `token`: Codecov token
- `files`: Coverage files to upload
- `fail_ci_if_error`: Fail CI if upload fails

**Example:**
```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@e0b68c6749509c5f83f984dd99a76a1c1a231044 # v4.0.1
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    files: ./coverage/lcov.info
    fail_ci_if_error: true
```

### github/super-linter

**Latest Version:** v5 (v5.7.2)
**SHA:** `45fc0d88288beee4701c62761281edfee85655d7`

**Description:** Run multiple linters in one action

**Common Inputs:**
- `validate_all_codebase`: Lint entire codebase or just changes
- `default_branch`: Default branch name
- `disable_errors`: Don't fail on errors

**Example:**
```yaml
- name: Lint code
  uses: github/super-linter@45fc0d88288beee4701c62761281edfee85655d7 # v5.7.2
  env:
    VALIDATE_ALL_CODEBASE: false
    DEFAULT_BRANCH: main
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Notifications

### slackapi/slack-github-action

**Latest Version:** v1 (v1.25.0)
**SHA:** `6c661ce58804a1a20f6dc5fbee7f0381b469e001`

**Description:** Send Slack notifications

**Common Inputs:**
- `webhook-url`: Slack webhook URL
- `payload`: JSON payload to send

**Example:**
```yaml
- name: Notify Slack
  uses: slackapi/slack-github-action@6c661ce58804a1a20f6dc5fbee7f0381b469e001 # v1.25.0
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
    payload: |
      {
        "text": "Build completed: ${{ job.status }}",
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Status:* ${{ job.status }}\n*Branch:* ${{ github.ref }}"
            }
          }
        ]
      }
```

## Release and Publishing

### actions/create-release

**Note:** Deprecated. Use `gh release create` or `softprops/action-gh-release` instead.

### softprops/action-gh-release

**Latest Version:** v2 (v2.0.2)
**SHA:** `9d7c94cfd0a1f3ed45544c887983e9fa900f0564`

**Description:** Create GitHub releases

**Common Inputs:**
- `tag_name`: Release tag (default: from tag trigger)
- `name`: Release name
- `body`: Release description
- `draft`: Create as draft
- `prerelease`: Mark as prerelease
- `files`: Files to upload

**Example:**
```yaml
- name: Create Release
  uses: softprops/action-gh-release@9d7c94cfd0a1f3ed45544c887983e9fa900f0564 # v2.0.2
  with:
    tag_name: ${{ github.ref }}
    name: Release ${{ github.ref_name }}
    body_path: CHANGELOG.md
    draft: false
    prerelease: false
    files: |
      dist/*.zip
      dist/*.tar.gz
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### actions/github-script

**Latest Version:** v7 (v7.0.1)
**SHA:** `60a0d83039c74a4aee543508d2ffcb1c3799cdea`

**Description:** Run JavaScript with GitHub API access

**Common Inputs:**
- `script`: JavaScript code to execute
- `github-token`: GitHub token (default: `${{ github.token }}`)

**Example:**
```yaml
- name: Create comment
  uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '👋 Thanks for reporting!'
      })
```

## Security

### actions/dependency-review-action

**Latest Version:** v4 (v4.8.3)
**SHA:** `05fe4576374b728f0c523d6a13d64c25081e0803`
**Description:** Scans pull requests for vulnerable dependency versions

**Required Permissions:**
```yaml
permissions:
  contents: read
```

**Common Inputs:**
- `fail-on-severity`: Severity level to fail on (`low`, `moderate`, `high`, `critical`)
- `allow-licenses`: Comma-separated list of allowed licenses
- `deny-licenses`: Comma-separated list of denied licenses

**Example:**
```yaml
- name: Dependency Review
  uses: actions/dependency-review-action@05fe4576374b728f0c523d6a13d64c25081e0803 # v4.8.3
  with:
    fail-on-severity: critical
    allow-licenses: MIT, Apache-2.0, BSD-3-Clause
```

### actions/attest-sbom

**Latest Version:** v2 (v2.4.0)
**SHA:** `bd218ad0dbcb3e146bd073d1d9c6d78e08aa8a0b`
**Description:** Generate SBOM attestations for artifacts

**Required Permissions:**
```yaml
permissions:
  id-token: write
  contents: read
  attestations: write
  packages: write  # For container registry
```

**Example:**
```yaml
- name: Generate SBOM attestation
  uses: actions/attest-sbom@bd218ad0dbcb3e146bd073d1d9c6d78e08aa8a0b # v2.4.0
  with:
    subject-name: ${{ env.REGISTRY }}/myapp
    subject-digest: sha256:${{ steps.build.outputs.digest }}
    sbom-path: sbom.json
    push-to-registry: true
```

### actions/attest-build-provenance

**Latest Version:** v2 (v2.4.0)
**SHA:** `e8998f949152b193b063cb0ec769d69d929409be`
**Description:** Generate build provenance attestations for build artifacts

**Required Permissions:**
```yaml
permissions:
  id-token: write
  contents: read
  attestations: write
  packages: write  # For container registry
```

**Example:**
```yaml
- name: Generate provenance attestation
  uses: actions/attest-build-provenance@e8998f949152b193b063cb0ec769d69d929409be # v2.4.0
  with:
    subject-name: ${{ env.REGISTRY }}/myapp
    subject-digest: sha256:${{ steps.build.outputs.digest }}
    push-to-registry: true
```

### github/codeql-action

**Latest Version:** v3 (v3.32.5)
**SHA:** `ae9ef3a1d2e3413523c3741725c30064970cc0d4`
**Description:** GitHub CodeQL scanning actions (`init`, `analyze`, `upload-sarif`)

**Required Permissions:**
```yaml
permissions:
  contents: read
  security-events: write
```

**Example:**
```yaml
- name: Initialize CodeQL
  uses: github/codeql-action/init@ae9ef3a1d2e3413523c3741725c30064970cc0d4 # v3.32.5
  with:
    languages: javascript

- name: Upload SARIF
  if: always()
  uses: github/codeql-action/upload-sarif@ae9ef3a1d2e3413523c3741725c30064970cc0d4 # v3.32.5
  with:
    sarif_file: trivy-results.sarif
```

## Best Practices Summary (Updated November 2025)

1. **Always pin to full SHA**: Use 40-character SHA with version comment
2. **Node 24 migration**: Migrate to Node 24 before March 2026 (Node 20 EOL April 2026)
3. **Cache v4.3.0**: Use latest cache version (v4.2.0+ required, legacy service retired Feb 2025)
4. **Use official actions**: Prefer verified `actions/*`, `docker/*`, etc.
5. **Security scanning**: Implement dependency review and SBOM attestations
6. **Minimal permissions**: Use explicit `permissions:` blocks
7. **Keep up to date**: Monitor releases and security advisories
8. **Document versions**: Add comments explaining version choices

## Finding Action Documentation

**Search Pattern:**
```
"[owner/repo] [version] github action documentation"
```

**Example:**
```
"docker/build-push-action v5 github documentation"
"actions/checkout v5 sparse-checkout"
```

**Official Sources:**
- GitHub Marketplace: https://github.com/marketplace
- Action repository: https://github.com/[owner]/[repo]
- Release notes: https://github.com/[owner]/[repo]/releases
- Context7: Use for structured documentation lookup

**Version Verification:**
- Check releases page for latest version
- Find SHA from tags: `git ls-remote https://github.com/[owner]/[repo] [tag]`
- Verify minimum runner requirements

Always verify action inputs and outputs from official documentation before use.

---

## Reference: Custom Actions

# Custom GitHub Actions Guide

**Last Updated:** December 2025

This guide covers creating custom GitHub Actions: composite, Docker, and JavaScript actions with proper metadata, directory structure, and versioning.

## Table of Contents
1. [Action Types](#action-types)
2. [Action Metadata](#action-metadata)
3. [Directory Structure](#directory-structure)
4. [Versioning](#versioning)
5. [Publishing to Marketplace](#publishing-to-marketplace)

---

## Action Types

| Type | Runtime | Use Case | Performance |
|------|---------|----------|-------------|
| Composite | Shell/Actions | Combine multiple steps | Fast startup |
| Docker | Container | Custom environment/tools | Slower startup |
| JavaScript | Node.js | API interactions, complex logic | Fastest |

---

## Action Metadata

### Branding

Add branding to make your action visually distinctive in GitHub Marketplace:

```yaml
name: 'Setup Node.js with Cache'
description: 'Setup Node.js with automatic dependency caching'
author: 'Your Name or Organization'

branding:
  icon: 'package'  # Feather icon name
  color: 'blue'    # Available: white, yellow, blue, green, orange, red, purple, gray-dark

inputs:
  node-version:
    description: 'Node.js version to use'
    required: true
```

**Available Icons:** See [Feather Icons](https://feathericons.com/) - e.g., `package`, `box`, `server`, `code`, `git-branch`, `shield`, `check-circle`

**Best Practices:**
- Choose icons that represent the action's purpose
- Use consistent branding across related actions
- Branding is required for GitHub Marketplace publishing

---

## Directory Structure

### Local Repository Actions

Use `.github/actions/` for actions within the same repository:

```
repository-root/
├── .github/
│   ├── actions/                    # Local custom actions
│   │   ├── setup-node-cached/      # Composite action
│   │   │   ├── action.yml
│   │   │   └── README.md
│   │   ├── terraform-validator/    # Docker action
│   │   │   ├── action.yml
│   │   │   ├── Dockerfile
│   │   │   ├── entrypoint.sh
│   │   │   └── README.md
│   │   └── label-pr/               # JavaScript action
│   │       ├── action.yml
│   │       ├── dist/
│   │       │   └── index.js        # Compiled/bundled JS
│   │       ├── src/
│   │       │   └── index.ts        # Source TypeScript
│   │       ├── package.json
│   │       └── README.md
│   └── workflows/
│       └── ci.yml
```

**Usage in Workflows:**
```yaml
steps:
  # Local action (same repository)
  - uses: ./.github/actions/setup-node-cached
    with:
      node-version: '20'

  # Action from another repository
  - uses: owner/repo/.github/actions/action-name@v1
```

### Standalone Action Repositories

For actions intended for GitHub Marketplace or cross-repo reuse:

```
action-repository-root/
├── action.yml          # Action definition (MUST be in root)
├── README.md           # Usage documentation
├── LICENSE             # License file
├── CHANGELOG.md        # Version history
├── dist/               # Compiled code (JS actions)
│   └── index.js
├── src/                # Source code (JS actions)
│   └── index.ts
└── Dockerfile          # For Docker actions
```

**Best Practices:**
- Use `.github/actions/` for repository-local actions
- Create separate repos for reusable/Marketplace actions
- Always include README.md with usage examples
- For JS actions, commit compiled `dist/` (don't gitignore)

---

## Versioning

### Semantic Versioning

Use MAJOR.MINOR.PATCH format:
- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

### Git Tags

```bash
# Create version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Update major version tag (v1 → latest v1.x.x)
git tag -fa v1 -m "Update v1 to v1.0.0"
git push origin v1 --force
```

### Tag Strategy

Maintain multiple tag levels:
- **Specific:** `v1.0.0`, `v1.0.1`, `v1.1.0`
- **Major:** `v1`, `v2` (points to latest minor/patch)

**User options:**
```yaml
- uses: owner/action@v1.0.0    # Pinned to exact version
- uses: owner/action@v1        # Latest v1.x.x
- uses: owner/action@abc123    # Pinned to SHA (most secure)
```

### Release Workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags: ['v*']

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2

      - name: Create GitHub Release
        run: gh release create ${{ github.ref_name }} --generate-notes
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Update major version tag
        run: |
          MAJOR=$(echo ${{ github.ref_name }} | cut -d. -f1)
          git tag -fa $MAJOR -m "Update $MAJOR tag"
          git push origin $MAJOR --force
```

### Breaking Changes

When introducing breaking changes:
1. Document in CHANGELOG.md and release notes
2. Increment MAJOR version
3. Provide migration guide
4. Consider maintaining previous major version branch

---

## Publishing to Marketplace

### Requirements

1. **Repository must be public**
2. **action.yml in repository root**
3. **Branding metadata** (icon and color)
4. **README.md** with usage examples
5. **Semantic version tags**

### Marketplace Listing

1. Go to repository Settings → Actions → "Create Action"
2. Or visit: `https://github.com/marketplace/actions/your-action`
3. Fill in marketplace details
4. Submit for review

### Pre-release Testing

Use pre-release versions for testing:
```bash
git tag -a v1.0.0-beta.1 -m "Beta release"
git push origin v1.0.0-beta.1
```

---

## Action Templates

### Composite Action Template

```yaml
name: '[Action Name]'
description: '[Brief description]'
author: '[Author]'

branding:
  icon: 'check-circle'
  color: 'green'

inputs:
  input-name:
    description: '[Description]'
    required: true
    default: '[default value]'

outputs:
  output-name:
    description: '[Description]'
    value: ${{ steps.step-id.outputs.value }}

runs:
  using: 'composite'
  steps:
    - name: Step name
      id: step-id
      shell: bash
      run: echo "value=result" >> $GITHUB_OUTPUT
```

### Docker Action Template

```yaml
name: '[Action Name]'
description: '[Brief description]'
author: '[Author]'

branding:
  icon: 'box'
  color: 'blue'

inputs:
  input-name:
    description: '[Description]'
    required: true

outputs:
  output-name:
    description: '[Description]'

runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.input-name }}
```

### JavaScript Action Template

```yaml
name: '[Action Name]'
description: '[Brief description]'
author: '[Author]'

branding:
  icon: 'code'
  color: 'purple'

inputs:
  github-token:
    description: 'GitHub token for API access'
    required: true

outputs:
  result:
    description: 'Action result'

runs:
  using: 'node20'
  main: 'dist/index.js'
```

---

## Summary

| Aspect | Recommendation |
|--------|---------------|
| Location | `.github/actions/` for local, separate repo for shared |
| Branding | Required for Marketplace, recommended for all |
| Versioning | Semantic versions with major tag updates |
| Documentation | README.md with examples, CHANGELOG.md |
| Security | Pin to SHA, minimal permissions |

---

## Reference: Expressions And Contexts

# GitHub Actions Expressions and Contexts

**Last Updated:** November 2025
**Source:** Official GitHub Actions documentation and Context7 verified examples

## Table of Contents
1. [Expression Syntax](#expression-syntax)
2. [Contexts](#contexts)
3. [Functions](#functions)
4. [Operators](#operators)
5. [Common Patterns](#common-patterns)
6. [Debugging and Troubleshooting](#debugging-and-troubleshooting)

## Expression Syntax

GitHub Actions expressions use `${{ }}` syntax to evaluate values dynamically.

**Basic Usage:**
```yaml
- name: Print environment
  run: echo "Running on ${{ runner.os }}"

- name: Conditional step
  if: ${{ github.ref == 'refs/heads/main' }}
  run: echo "On main branch"

# Note: 'if' doesn't require ${{ }}, it's implicit
- name: Conditional step (preferred)
  if: github.ref == 'refs/heads/main'
  run: echo "On main branch"
```

**Where Expressions Can Be Used:**
- `if` conditionals (implicit `${{ }}`, can omit)
- `env` values (must use `${{ }}`)
- `with` inputs (must use `${{ }}`)
- Step `name` values (must use `${{ }}`)
- Job `outputs` (must use `${{ }}`)
- `environment.name` (can use expressions for dynamic environments)

**Important Notes:**
- Expressions are interpolated **before** the job is sent to the runner
- Use environment variables via `env` context for safer variable handling
- Avoid direct interpolation of untrusted input (use `env` context instead)

## Contexts

Contexts are objects containing information about workflow runs, variables, environments, and more.

### github context

Contains information about the workflow run and triggering event.

**Common Properties:**
```yaml
# Event information
${{ github.event_name }}          # Event that triggered workflow (push, pull_request, etc.)
${{ github.event.action }}        # Action that triggered event (opened, synchronize, etc.)

# Repository information
${{ github.repository }}          # owner/repo
${{ github.repository_owner }}    # Repository owner
${{ github.ref }}                 # Full ref (refs/heads/main, refs/tags/v1.0.0)
${{ github.ref_name }}            # Short ref (main, v1.0.0)
${{ github.sha }}                 # Commit SHA that triggered workflow

# Actor information
${{ github.actor }}               # Username that triggered workflow
${{ github.triggering_actor }}    # User that initiated the workflow run

# Workflow information
${{ github.workflow }}            # Workflow name
${{ github.run_id }}              # Unique workflow run ID
${{ github.run_number }}          # Workflow run number
${{ github.job }}                 # Current job ID

# Pull request information (when event is pull_request)
${{ github.event.pull_request.number }}
${{ github.event.pull_request.title }}
${{ github.event.pull_request.head.ref }}    # Source branch
${{ github.event.pull_request.base.ref }}    # Target branch
${{ github.event.pull_request.head.sha }}

# Push information (when event is push)
${{ github.event.head_commit.message }}
${{ github.event.head_commit.author.name }}
```

**Examples:**
```yaml
# Build image tagged with commit SHA
- name: Build Docker image
  run: docker build -t myapp:${{ github.sha }} .

# Deploy only on main branch
- name: Deploy
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh

# Different behavior for PR vs push
- name: Set environment
  run: |
    if [ "${{ github.event_name }}" == "pull_request" ]; then
      echo "ENV=preview" >> $GITHUB_ENV
    else
      echo "ENV=production" >> $GITHUB_ENV
    fi
```

### env context

Access environment variables defined in workflow, job, or step.

```yaml
env:
  NODE_VERSION: '20'
  BUILD_TYPE: 'production'

jobs:
  build:
    env:
      API_URL: 'https://api.example.com'
    steps:
      - name: Print variables
        run: |
          echo "Node: ${{ env.NODE_VERSION }}"
          echo "API: ${{ env.API_URL }}"
```

### runner context

Information about the runner executing the job.

**Common Properties:**
```yaml
${{ runner.os }}              # OS (Linux, Windows, macOS)
${{ runner.arch }}            # Architecture (X64, ARM64)
${{ runner.name }}            # Runner name
${{ runner.temp }}            # Temp directory path
${{ runner.tool_cache }}      # Tool cache directory path
```

**Examples:**
```yaml
# OS-specific commands
- name: Install dependencies
  run: |
    if [ "${{ runner.os }}" == "Linux" ]; then
      sudo apt-get update
    elif [ "${{ runner.os }}" == "macOS" ]; then
      brew update
    fi

# Cache key with OS
- uses: actions/cache@cdf6c1fa76f9f475f3d7449005a359c84ca0f306 # v5.0.3
  with:
    path: ~/.cache
    key: ${{ runner.os }}-cache-${{ hashFiles('**/lock.file') }}
```

### secrets context

Access encrypted secrets defined in repository or organization settings.

```yaml
- name: Deploy to production
  env:
    API_KEY: ${{ secrets.API_KEY }}
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: ./deploy.sh
```

**Security Notes:**
- Secrets are automatically masked in logs
- Use `echo "::add-mask::$VALUE"` to mask additional values
- Pass secrets via environment variables, not command arguments

### matrix context

Access matrix configuration values when using matrix strategy.

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node: [18, 20, 22]
    include:
      - os: ubuntu-latest
        node: 20
        experimental: true

steps:
  - name: Setup Node.js ${{ matrix.node }}
    uses: actions/setup-node@6044e13b5dc448c55e2357c09f80417699197238 # v6.2.0
    with:
      node-version: ${{ matrix.node }}

  - name: Mark experimental
    if: matrix.experimental
    run: echo "Experimental build"
```

### steps context

Access information about steps that have already run.

```yaml
steps:
  - name: Run tests
    id: tests
    run: npm test

  - name: Upload results
    if: steps.tests.outcome == 'success'
    run: ./upload-results.sh

  - name: Use step output
    run: echo "Test result: ${{ steps.tests.outputs.result }}"
```

**Step Properties:**
- `steps.<step_id>.outputs.<output_name>`: Output value
- `steps.<step_id>.outcome`: Result before `continue-on-error` (`success`, `failure`, `cancelled`, `skipped`)
- `steps.<step_id>.conclusion`: Final result after `continue-on-error`

### job context

Access information about currently running job.

```yaml
jobs:
  build:
    outputs:
      build-id: ${{ steps.build.outputs.id }}
    steps:
      - name: Build
        id: build
        run: echo "id=build-123" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    steps:
      - name: Deploy build
        run: ./deploy.sh ${{ needs.build.outputs.build-id }}
```

### inputs context

Access workflow or reusable workflow inputs.

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options: [dev, staging, production]
      debug:
        description: 'Enable debug mode'
        required: false
        type: boolean
        default: false

jobs:
  deploy:
    steps:
      - name: Deploy to ${{ inputs.environment }}
        run: ./deploy.sh ${{ inputs.environment }}

      - name: Enable debug
        if: inputs.debug
        run: echo "Debug mode enabled"
```

## Functions

### String Functions

**contains()**
```yaml
# Check if string contains substring
if: contains(github.ref, 'refs/tags/')
if: contains(github.event.head_commit.message, '[skip ci]')
if: contains(fromJSON('["main", "develop"]'), github.ref_name)
```

**startsWith()**
```yaml
# Check if string starts with prefix
if: startsWith(github.ref, 'refs/tags/v')
if: startsWith(github.event.pull_request.title, 'feat:')
```

**endsWith()**
```yaml
# Check if string ends with suffix
if: endsWith(github.ref, '/main')
if: endsWith(github.event.pull_request.head.ref, '-hotfix')
```

**format()**
```yaml
# Format string with placeholders
- name: Print message
  run: echo "${{ format('Building {0} on {1}', github.ref_name, runner.os) }}"
```

### Type Conversion Functions

**toJSON()**
```yaml
# Convert object to JSON string
- name: Print context
  run: echo '${{ toJSON(github) }}'

- name: Print matrix
  run: echo '${{ toJSON(matrix) }}'
```

**fromJSON()**
```yaml
# Parse JSON string to object
strategy:
  matrix:
    config: ${{ fromJSON('{"versions":[18,20,22]}') }}

# Use with dynamic matrix
jobs:
  setup:
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: echo 'matrix={"version":["18","20"]}' >> $GITHUB_OUTPUT

  build:
    needs: setup
    strategy:
      matrix: ${{ fromJSON(needs.setup.outputs.matrix) }}
```

### Hash Functions

**hashFiles()**
```yaml
# Generate hash of file contents (for cache keys)
- uses: actions/cache@cdf6c1fa76f9f475f3d7449005a359c84ca0f306 # v5.0.3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}

# Multiple patterns
key: ${{ hashFiles('**/*.go', '**/go.sum') }}
```

### Status Check Functions

**success()**
```yaml
# Run only if all previous steps succeeded
- name: Deploy
  if: success()
  run: ./deploy.sh
```

**failure()**
```yaml
# Run only if any previous step failed
- name: Notify on failure
  if: failure()
  run: ./notify-failure.sh
```

**always()**
```yaml
# Run regardless of previous step status
- name: Cleanup
  if: always()
  run: ./cleanup.sh
```

**cancelled()**
```yaml
# Run if workflow was cancelled
- name: Cleanup on cancel
  if: cancelled()
  run: ./cancel-cleanup.sh
```

## Operators

### Comparison Operators

```yaml
# Equality
if: github.ref == 'refs/heads/main'
if: runner.os != 'Windows'

# Logical
if: github.event_name == 'push' && github.ref == 'refs/heads/main'
if: github.event_name == 'pull_request' || github.event_name == 'push'
if: "!(github.event_name == 'pull_request')"

# Comparison
if: github.event.pull_request.changed_files < 10
if: matrix.node-version >= 20
```

### Operator Precedence

1. `()`
2. `!`
3. `<`, `<=`, `>`, `>=`
4. `==`, `!=`
5. `&&`
6. `||`

## Common Patterns

### Branch-Based Conditions

```yaml
# Main branch only
if: github.ref == 'refs/heads/main'

# Any branch except main
if: github.ref != 'refs/heads/main'

# Specific branches
if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'

# Tag pushes only
if: startsWith(github.ref, 'refs/tags/')

# Version tags only (v1.0.0 format)
if: startsWith(github.ref, 'refs/tags/v')
```

### Event-Based Conditions

```yaml
# Push event only
if: github.event_name == 'push'

# PR opened or synchronized
if: |
  github.event_name == 'pull_request' &&
  (github.event.action == 'opened' || github.event.action == 'synchronize')

# Manual dispatch only
if: github.event_name == 'workflow_dispatch'

# Scheduled run only
if: github.event_name == 'schedule'
```

### Step Status Patterns

```yaml
# Run if specific step succeeded
if: steps.tests.outcome == 'success'

# Run if step failed but continue
if: steps.tests.outcome == 'failure'

# Run cleanup always
if: always()

# Run only on failure
if: failure()
```

### Matrix Patterns

```yaml
# Specific matrix combination
if: matrix.os == 'ubuntu-latest' && matrix.node == 20

# Exclude certain combinations
strategy:
  matrix:
    os: [ubuntu, windows, macos]
    node: [18, 20, 22]
    exclude:
      - os: windows
        node: 18
```

### Dynamic Values

```yaml
# Build tags with multiple values
tags: |
  myapp:latest
  myapp:${{ github.sha }}
  myapp:${{ github.ref_name }}

# Conditional environment
environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'staging' }}

# Dynamic timeout
timeout-minutes: ${{ github.event_name == 'schedule' && 120 || 30 }}
```

### Combining Contexts

```yaml
# Artifact name with context values
- uses: actions/upload-artifact@5d5d22a31266ced268874388b861e4b58bb5c2f3 # v4.3.1
  with:
    name: build-${{ runner.os }}-${{ github.sha }}
    path: dist/

# Cache key with multiple factors
- uses: actions/cache@cdf6c1fa76f9f475f3d7449005a359c84ca0f306 # v5.0.3
  with:
    path: ~/.cache
    key: ${{ runner.os }}-${{ hashFiles('**/*.lock') }}-${{ github.ref_name }}
```

### Safe String Interpolation

```yaml
# ❌ UNSAFE: Direct interpolation of user input
- run: echo "Title: ${{ github.event.pull_request.title }}"

# ✅ SAFE: Use environment variables
- name: Print PR title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "Title: $PR_TITLE"
```

### JSON Manipulation

```yaml
# Create dynamic matrix
- id: set-matrix
  run: |
    if [ "${{ github.event_name }}" == "push" ]; then
      echo 'matrix={"os":["ubuntu","windows","macos"]}' >> $GITHUB_OUTPUT
    else
      echo 'matrix={"os":["ubuntu"]}' >> $GITHUB_OUTPUT
    fi

# Use matrix
strategy:
  matrix: ${{ fromJSON(steps.set-matrix.outputs.matrix) }}
```

## Debugging and Troubleshooting

### Dumping Contexts to Logs

The most effective way to debug workflow issues is to dump context information to logs:

**Dump All Contexts:**
```yaml
name: Context Debugging
on: push

jobs:
  dump_contexts:
    runs-on: ubuntu-latest
    steps:
      - name: Dump GitHub context
        env:
          GITHUB_CONTEXT: ${{ toJson(github) }}
        run: echo "$GITHUB_CONTEXT"

      - name: Dump job context
        env:
          JOB_CONTEXT: ${{ toJson(job) }}
        run: echo "$JOB_CONTEXT"

      - name: Dump steps context
        env:
          STEPS_CONTEXT: ${{ toJson(steps) }}
        run: echo "$STEPS_CONTEXT"

      - name: Dump runner context
        env:
          RUNNER_CONTEXT: ${{ toJson(runner) }}
        run: echo "$RUNNER_CONTEXT"

      - name: Dump strategy context
        env:
          STRATEGY_CONTEXT: ${{ toJson(strategy) }}
        run: echo "$STRATEGY_CONTEXT"

      - name: Dump matrix context
        env:
          MATRIX_CONTEXT: ${{ toJson(matrix) }}
        run: echo "$MATRIX_CONTEXT"
```

**Example Runner Context Output:**
```json
{
  "os": "Linux",
  "arch": "X64",
  "name": "GitHub Actions 2",
  "tool_cache": "/opt/hostedtoolcache",
  "temp": "/home/runner/work/_temp"
}
```

### Safe Variable Interpolation

**Best Practice - Use env context:**
```yaml
# ✅ SAFE: Interpolate before runner execution
- name: Greet user
  env:
    GREETING: ${{ env.Greeting }}
    FIRST_NAME: ${{ env.First_Name }}
    DAY: ${{ env.DAY_OF_WEEK }}
  run: echo "$GREETING $FIRST_NAME. Today is $DAY!"
```

This approach ensures variables are resolved by GitHub Actions before execution, providing consistent behavior.

## Tips and Best Practices

1. **Implicit vs Explicit `${{ }}`:**
   - `if` conditions don't need `${{ }}` (implicit)
   - Other contexts require explicit `${{ }}`

2. **String Comparisons:**
   - Always use quotes for string literals
   - Case-sensitive by default

3. **Boolean Values:**
   - Use `true` and `false` without quotes
   - Empty strings evaluate to `false`

4. **Default Values:**
   ```yaml
   # Use || for default values
   environment: ${{ inputs.environment || 'dev' }}
   ```

5. **Multi-line Expressions:**
   ```yaml
   if: |
     github.event_name == 'push' &&
     github.ref == 'refs/heads/main' &&
     !contains(github.event.head_commit.message, '[skip ci]')
   ```

6. **Security Best Practices:**
   - Always use `env` context for untrusted input
   - Never directly interpolate user-controlled values
   - Use `::add-mask::` for sensitive values

7. **Dynamic Environment Names:**
   ```yaml
   environment:
     name: ${{ github.ref_name }}  # Dynamic based on branch
   ```

8. **Debugging Expressions:**
   ```yaml
   # Print entire context with pretty formatting
   - run: echo '${{ toJson(github) }}'

   # Print specific values
   - run: |
       echo "Event: ${{ github.event_name }}"
       echo "Ref: ${{ github.ref }}"
       echo "SHA: ${{ github.sha }}"
       echo "Actor: ${{ github.actor }}"
   ```

## Summary

- Use `${{ }}` for dynamic values
- Access contexts like `github`, `env`, `secrets`, `matrix`, `runner`, etc.
- Use functions for string manipulation, hashing, and type conversion (`toJSON`, `hashFiles`, `contains`, etc.)
- Combine operators for complex conditions
- **Always validate and sanitize user inputs for security**
- Use `env` context for untrusted input instead of direct interpolation
- Debug with `toJSON()` to dump context information
- Expressions are evaluated before job execution on the runner

**Security Warning:** Never directly interpolate untrusted input (PR titles, issue bodies, user input) in `run` commands. Always use environment variables via the `env` context.

---

## Reference: Modern Features

# Modern GitHub Actions Features

**Last Updated:** December 2025

This guide covers modern GitHub Actions capabilities for enhanced workflow output, deployment control, and containerized builds.

## Table of Contents
1. [Job Summaries](#job-summaries)
2. [Deployment Environments](#deployment-environments)
3. [Container Jobs](#container-jobs)
4. [Workflow Annotations](#workflow-annotations)
5. [Integration Examples](#integration-examples)

---

## Job Summaries

Create rich markdown summaries in the Actions UI using `$GITHUB_STEP_SUMMARY`.

### When to Use
- Display test results, coverage reports, benchmarks
- Show deployment status and URLs
- Present security scan findings
- Summarize workflow execution

### Basic Usage

```yaml
- name: Generate summary
  run: |
    echo "## Build Results :rocket:" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "| Metric | Value |" >> $GITHUB_STEP_SUMMARY
    echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
    echo "| Tests | ${{ steps.test.outputs.passed }} passed |" >> $GITHUB_STEP_SUMMARY
    echo "| Coverage | ${{ steps.test.outputs.coverage }}% |" >> $GITHUB_STEP_SUMMARY
```

### Advanced Patterns

**Test Results Table:**
```yaml
- name: Test summary
  if: always()
  run: |
    echo "## Test Results :test_tube:" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "| Suite | Status | Duration |" >> $GITHUB_STEP_SUMMARY
    echo "|-------|--------|----------|" >> $GITHUB_STEP_SUMMARY
    echo "| Unit Tests | :white_check_mark: | 45s |" >> $GITHUB_STEP_SUMMARY
    echo "| Integration | :white_check_mark: | 2m 30s |" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "### Deployment URLs" >> $GITHUB_STEP_SUMMARY
    echo "- [Staging](https://staging.example.com)" >> $GITHUB_STEP_SUMMARY
    echo "- [Production](https://example.com)" >> $GITHUB_STEP_SUMMARY
```

**Collapsible Details:**
```yaml
- name: Detailed summary
  run: |
    echo "## Summary" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo "<details>" >> $GITHUB_STEP_SUMMARY
    echo "<summary>Click to expand test details</summary>" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY
    echo '```' >> $GITHUB_STEP_SUMMARY
    cat test-output.txt >> $GITHUB_STEP_SUMMARY
    echo '```' >> $GITHUB_STEP_SUMMARY
    echo "</details>" >> $GITHUB_STEP_SUMMARY
```

### Best Practices
- Use `if: always()` to show summaries even on failure
- Include emojis for visual scanning
- Use markdown tables for structured data
- Add links to deployed environments
- Clear summary at start if needed: `> $GITHUB_STEP_SUMMARY`

---

## Deployment Environments

Use GitHub environments with protection rules, approval gates, and environment-specific secrets.

### When to Use
- Multi-stage deployments (dev, staging, production)
- Deployments requiring manual approval
- Environment-specific configuration
- Deployment tracking and rollback

### Basic Usage

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Deploy
        run: ./deploy.sh staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Deploy
        run: ./deploy.sh production
```

### Protection Rules

Configure in repository Settings → Environments:

| Rule | Description |
|------|-------------|
| Required reviewers | Manual approval before deployment |
| Wait timer | Delay deployment by N minutes |
| Deployment branches | Restrict which branches can deploy |
| Environment secrets | Secrets available only in this environment |

### Multi-Environment Pattern

```yaml
name: Deploy

on:
  push:
    branches: [main, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: ${{ github.ref_name == 'main' && 'production' || 'staging' }}
      url: ${{ github.ref_name == 'main' && 'https://example.com' || 'https://staging.example.com' }}
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
      - name: Deploy to ${{ github.ref_name == 'main' && 'production' || 'staging' }}
        env:
          API_KEY: ${{ secrets.API_KEY }}  # Environment-specific secret
        run: ./deploy.sh
```

### Best Practices
- Set environment URLs for easy access
- Use required reviewers for production
- Configure branch policies
- Leverage environment-specific secrets
- Use `needs` to enforce deployment order

---

## Container Jobs

Run jobs inside Docker containers for consistent, isolated build environments.

### When to Use
- Require specific OS/tool versions
- Need isolated build environment
- Want to match local dev environment
- Building for specific Linux distributions

### Basic Container Job

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: node:20-alpine
      env:
        NODE_ENV: production
      options: --cpus 2 --memory 4g
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
      - run: npm ci
      - run: npm run build
```

### With Service Containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: node:20

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
      - name: Run tests
        env:
          DATABASE_URL: postgres://postgres:postgres@postgres:5432/test
          REDIS_URL: redis://redis:6379
        run: npm test
```

### Best Practices
- Use specific image tags (avoid `latest`)
- Configure health checks for services
- Set resource limits with `options`
- Use volumes for persistent data
- Prefer official images

---

## Workflow Annotations

Create annotations (notices, warnings, errors) in the Actions UI and PR files.

### Annotation Commands

| Command | Level | Appearance |
|---------|-------|------------|
| `::notice::` | Info | Blue |
| `::warning::` | Warning | Yellow |
| `::error::` | Error | Red (doesn't fail step) |

### Basic Usage

```yaml
- name: Validate
  run: |
    # Simple annotations
    echo "::notice::Build completed successfully"
    echo "::warning::Deprecated API usage detected"
    echo "::error::Configuration issue found"
```

### File/Line Annotations

Annotations with file location appear in PR Files tab:

```yaml
- name: Lint results
  run: |
    # With file and line info
    echo "::error file=src/app.js,line=10,col=5::Type mismatch detected"
    echo "::warning file=config.js,line=23::Deprecated option used"
    echo "::notice file=utils.js,line=100,endLine=105::Consider refactoring"
```

### Log Groups

Collapse verbose output:

```yaml
- name: Build with groups
  run: |
    echo "::group::Installing dependencies"
    npm ci
    echo "::endgroup::"

    echo "::group::Running tests"
    npm test
    echo "::endgroup::"
```

### Masking Secrets

```yaml
- name: Process secret
  run: |
    SENSITIVE="$(./get-secret.sh)"
    echo "::add-mask::$SENSITIVE"
    echo "Using secret safely"
```

### All Workflow Commands

| Command | Purpose |
|---------|---------|
| `::notice::` | Info annotation |
| `::warning::` | Warning annotation |
| `::error::` | Error annotation |
| `::group::` | Start collapsed section |
| `::endgroup::` | End collapsed section |
| `::add-mask::` | Mask value in logs |
| `::stop-commands::TOKEN` | Disable command processing |
| `::TOKEN::` | Re-enable commands |
| `::debug::` | Debug message (requires debug logging) |

---

## Integration Examples

### Complete CI/CD with Modern Features

```yaml
name: Full-Featured CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:

permissions:
  contents: read
  deployments: write

jobs:
  test:
    runs-on: ubuntu-latest
    container:
      image: node:20-alpine

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres

    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2

      - name: Run tests
        id: test
        env:
          DATABASE_URL: postgres://postgres:postgres@postgres:5432/test
        run: |
          npm ci
          npm test -- --coverage
          echo "coverage=85" >> $GITHUB_OUTPUT

      - name: Coverage check
        run: |
          COVERAGE=${{ steps.test.outputs.coverage }}
          if [ $COVERAGE -lt 80 ]; then
            echo "::warning::Coverage $COVERAGE% below 80% threshold"
          else
            echo "::notice::Coverage $COVERAGE% meets threshold"
          fi

      - name: Test summary
        if: always()
        run: |
          echo "## Test Results :test_tube:" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Metric | Value |" >> $GITHUB_STEP_SUMMARY
          echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
          echo "| Coverage | ${{ steps.test.outputs.coverage }}% |" >> $GITHUB_STEP_SUMMARY
          echo "| Status | :white_check_mark: Passed |" >> $GITHUB_STEP_SUMMARY

  deploy-staging:
    needs: test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com

    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2

      - name: Deploy
        run: ./deploy.sh staging

      - name: Deployment summary
        run: |
          echo "## Deployment :rocket:" >> $GITHUB_STEP_SUMMARY
          echo "- **Environment**: Staging" >> $GITHUB_STEP_SUMMARY
          echo "- **URL**: https://staging.example.com" >> $GITHUB_STEP_SUMMARY
          echo "- **Commit**: ${{ github.sha }}" >> $GITHUB_STEP_SUMMARY

  deploy-production:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com

    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2

      - name: Deploy
        run: ./deploy.sh production

      - name: Deployment summary
        run: |
          echo "## Production Deployment :rocket:" >> $GITHUB_STEP_SUMMARY
          echo "- **Environment**: Production" >> $GITHUB_STEP_SUMMARY
          echo "- **URL**: https://example.com" >> $GITHUB_STEP_SUMMARY
          echo "- **Note**: Required manual approval" >> $GITHUB_STEP_SUMMARY
```

---

## Summary

| Feature | Use Case | Key Benefits |
|---------|----------|--------------|
| Job Summaries | Rich output display | Markdown support, persists in UI |
| Environments | Deployment control | Approvals, secrets, tracking |
| Container Jobs | Consistent builds | Isolation, reproducibility |
| Annotations | Inline feedback | PR integration, visual alerts |

---

## Example: Readme

# GitHub Actions Generator Examples

This directory contains example workflows and actions generated using the github-actions-generator skill.

## Workflows

### Language-Specific CI Pipelines

#### nodejs-ci.yml
Complete CI pipeline for Node.js applications demonstrating:
- Matrix testing across multiple Node.js versions and operating systems
- Dependency caching with `actions/setup-node`
- Parallel linting and testing
- Artifact uploading for test results
- Code coverage reporting with Codecov
- Concurrency controls

**Use case:** Standard CI/CD for Node.js projects

#### python-ci.yml
Python CI pipeline demonstrating:
- Matrix testing across Python versions
- Virtual environment management
- Dependency caching with pip
- Testing with pytest
- Code quality checks

**Use case:** Python application CI/CD

#### go-ci.yml
Go CI pipeline demonstrating:
- Go module caching
- Cross-platform builds
- Go testing and benchmarking
- Static code analysis

**Use case:** Go application CI/CD

### Container & Deployment Workflows

#### docker-build-push.yml
Docker image build and push workflow demonstrating:
- Multi-platform builds (amd64, arm64)
- GitHub Container Registry integration
- Docker layer caching with GitHub Actions cache
- Automatic tagging based on git events
- Secure authentication with `GITHUB_TOKEN`

**Use case:** Containerized application deployment

#### multi-environment-deploy.yml
Multi-environment deployment workflow demonstrating:
- Environment protection rules and approval gates
- Dynamic environment selection (dev, staging, production)
- AWS deployment with OIDC authentication
- Blue-green deployment strategy
- Automatic rollback on failure
- Smoke tests and health checks
- Deployment verification

**Use case:** Production-grade multi-stage deployments

### Advanced Workflow Patterns

#### monorepo-ci.yml
Monorepo CI pipeline demonstrating:
- Path-based change detection
- Conditional job execution based on affected packages
- Cross-package dependency management
- Parallel builds for independent packages
- Artifact sharing between jobs
- Package-specific test strategies

**Use case:** Monorepo projects with multiple packages

#### scheduled-tasks.yml
Scheduled maintenance workflow demonstrating:
- Cron schedule configuration
- Dependency security audits
- Stale branch cleanup
- Cache management
- External service health checks
- Automated issue creation
- Weekly metrics reporting

**Use case:** Repository maintenance and monitoring

### Security Workflows

#### security/dependency-review.yml
Dependency review workflow demonstrating:
- Pull request dependency scanning
- Vulnerability severity thresholds
- License policy enforcement
- Automatic build failure on policy violations

**Use case:** Supply chain security for PRs

#### security/sbom-attestation.yml
SBOM and attestation workflow demonstrating:
- Software Bill of Materials generation
- SBOM attestation with GitHub's signing infrastructure
- Build provenance attestation
- Container vulnerability scanning with Trivy
- Multi-platform container builds
- Security scan results upload to GitHub Security tab

**Use case:** Supply chain security compliance

## Actions

### setup-node-cached/action.yml
Composite action for Node.js setup demonstrating:
- Smart dependency caching for npm, yarn, and pnpm
- Input validation
- Multiple package manager support
- Cache hit detection
- Grouped output for better logging

**Use case:** Reusable Node.js setup across multiple workflows

## Usage

These examples can be used as:
1. **Templates** - Copy and modify for your own projects
2. **Learning Resources** - Study best practices and patterns
3. **Testing** - Validate with github-actions-validator skill

## Testing Examples

To validate any of these examples:

```bash
cd devops-skills-plugin/skills/github-actions-validator
bash scripts/validate_workflow.sh ../../github-actions-generator/examples/workflows/nodejs-ci.yml
```

## Best Practices Demonstrated

All examples follow these best practices:
- ✅ Actions pinned to SHAs with version comments
- ✅ Minimal permissions with explicit `permissions:` blocks
- ✅ Concurrency controls to prevent duplicate runs
- ✅ Proper timeout settings
- ✅ Semantic naming conventions
- ✅ Comprehensive error handling
- ✅ Security-first approach
