---
title: "Render 部署"
description: "Render 云平台部署配置，Web 服务和数据库托管"
category: "devops"
source: "community"
author: "Community"
tags: ["render", "deploy"]
date: 2026-03-20
---

# Deploy to Render

Render supports **Git-backed** services and **prebuilt Docker image** services.

This skill covers **Git-backed** flows:
1. **Blueprint Method** - Generate render.yaml for Infrastructure-as-Code deployments
2. **Direct Creation** - Create services instantly via MCP tools

Blueprints can also run a **prebuilt Docker image** by using `runtime: image`, but the `render.yaml` still must live in a Git repo.

If there is no Git remote, stop and ask the user to either:
- Create/push a Git remote (can be minimal if only the Blueprint is needed), or
- Use the Render Dashboard/API to deploy a prebuilt Docker image (MCP cannot create image-backed services).

## Prerequisites

- When sandboxing blocks the deployment network calls, rerun with `sandbox_permissions=require_escalated`.
- The deployment might take a few minutes. Use appropriate timeout values.

## When to Use This Skill

Activate this skill when users want to:
- Deploy an application to Render
- Create a render.yaml Blueprint file
- Set up Render deployment for their project
- Host or publish their application on Render's cloud platform
- Create databases, cron jobs, or other Render resources

## Happy Path (New Users)

Use this short prompt sequence before deep analysis to reduce friction:
1. Ask whether they want to deploy from a Git repo or a prebuilt Docker image.
2. Ask whether Render should provision everything the app needs (based on what seems likely from the user's description) or only the app while they bring their own infra. If dependencies are unclear, ask a short follow-up to confirm whether they need a database, workers, cron, or other services.

Then proceed with the appropriate method below.

## Choose Your Source Path

**Git Repo Path:** Required for both Blueprint and Direct Creation. The repo must be pushed to GitHub, GitLab, or Bitbucket.

**Prebuilt Docker Image Path:** Supported by Render via image-backed services. This is **not** supported by MCP; use the Dashboard/API. Ask for:
- Image URL (registry + tag)
- Registry auth (if private)
- Service type (web/worker) and port

If the user chooses a Docker image, guide them to the Render Dashboard image deploy flow or ask them to add a Git remote (so you can use a Blueprint with `runtime: image`).

## Choose Your Deployment Method (Git Repo)

Both methods require a Git repository pushed to GitHub, GitLab, or Bitbucket. (If using `runtime: image`, the repo can be minimal and only contain `render.yaml`.)

| Method | Best For | Pros |
|--------|----------|------|
| **Blueprint** | Multi-service apps, IaC workflows | Version controlled, reproducible, supports complex setups |
| **Direct Creation** | Single services, quick deployments | Instant creation, no render.yaml file needed |

### Method Selection Heuristic

Use this decision rule by default unless the user requests a specific method. Analyze the codebase first; only ask if deployment intent is unclear (e.g., DB, workers, cron).

**Use Direct Creation (MCP) when ALL are true:**
- Single service (one web app or one static site)
- No separate worker/cron services
- No attached databases or Key Value
- Simple env vars only (no shared env groups)
If this path fits and MCP isn't configured yet, stop and guide MCP setup before proceeding.

**Use Blueprint when ANY are true:**
- Multiple services (web + worker, API + frontend, etc.)
- Databases, Redis/Key Value, or other datastores are required
- Cron jobs, background workers, or private services
- You want reproducible IaC or a render.yaml committed to the repo
- Monorepo or multi-env setup that needs consistent configuration

If unsure, ask a quick clarifying question, but default to Blueprint for safety. For a single service, strongly prefer Direct Creation via MCP and guide MCP setup if needed.

## Prerequisites Check

When starting a deployment, verify these requirements in order:

**1. Confirm Source Path (Git vs Docker)**

If using Git-based methods (Blueprint or Direct Creation), the repo must be pushed to GitHub/GitLab/Bitbucket. Blueprints that reference a prebuilt image still require a Git repo with `render.yaml`.

```bash
git remote -v
```

- If no remote exists, stop and ask the user to create/push a remote **or** switch to Docker image deploy.

**2. Check MCP Tools Availability (Preferred for Single-Service)**

MCP tools provide the best experience. Check if available by attempting:
```
list_services()
```

If MCP tools are available, you can skip CLI installation for most operations.

**3. Check Render CLI Installation (for Blueprint validation)**
```bash
render --version
```
If not installed, offer to install:
- macOS: `brew install render`
- Linux/macOS: `curl -fsSL https://raw.githubusercontent.com/render-oss/cli/main/bin/install.sh | sh`

**4. MCP Setup (if MCP isn't configured)**

If `list_services()` fails because MCP isn't configured, ask whether they want to set up MCP (preferred) or continue with the CLI fallback. If they choose MCP, ask which AI tool they're using, then provide the matching instructions below. Always use their API key.

### Cursor

Walk the user through these steps:

1) Get a Render API key:
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) Add this to `~/.cursor/mcp.json` (replace `<YOUR_API_KEY>`):
```json
{
  "mcpServers": {
    "render": {
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_API_KEY>"
      }
    }
  }
}
```

3) Restart Cursor, then retry `list_services()`.

### Claude Code

Walk the user through these steps:

1) Get a Render API key:
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) Add the MCP server with Claude Code (replace `<YOUR_API_KEY>`):
```bash
claude mcp add --transport http render https://mcp.render.com/mcp --header "Authorization: Bearer <YOUR_API_KEY>"
```

3) Restart Claude Code, then retry `list_services()`.

### Codex

Walk the user through these steps:

1) Get a Render API key:
```
https://dashboard.render.com/u/*/settings#api-keys
```

2) Set it in their shell:
```bash
export RENDER_API_KEY="<YOUR_API_KEY>"
```

3) Add the MCP server with the Codex CLI:
```bash
codex mcp add render --url https://mcp.render.com/mcp --bearer-token-env-var RENDER_API_KEY
```

4) Restart Codex, then retry `list_services()`.

### Other Tools

If the user is on another AI app, direct them to the Render MCP docs for that tool's setup steps and install method.

### Workspace Selection

After MCP is configured, have the user set the active Render workspace with a prompt like:

```
Set my Render workspace to [WORKSPACE_NAME]
```

**5. Check Authentication (CLI fallback only)**

If MCP isn't available, use the CLI instead and verify you can access your account:
```bash
# Check if user is logged in (use -o json for non-interactive mode)
render whoami -o json
```

If `render whoami` fails or returns empty data, the CLI is not authenticated. The CLI won't always prompt automatically, so explicitly prompt the user to authenticate:

If neither is configured, ask user which method they prefer:
- **API Key (CLI)**: `export RENDER_API_KEY="rnd_xxxxx"` (Get from https://dashboard.render.com/u/*/settings#api-keys)
- **Login**: `render login` (Opens browser for OAuth)

**6. Check Workspace Context**

Verify the active workspace:
```
get_selected_workspace()
```

Or via CLI:
```bash
render workspace current -o json
```

To list available workspaces:
```
list_workspaces()
```

If user needs to switch workspaces, they must do so via Dashboard or CLI (`render workspace set`).

Once prerequisites are met, proceed with deployment workflow.

---

# Method 1: Blueprint Deployment (Recommended for Complex Apps)

## Blueprint Workflow

### Step 1: Analyze Codebase

Analyze the codebase to determine framework/runtime, build and start commands, required env vars, datastores, and port binding. Use the detailed checklists in [references/codebase-analysis.md](references/codebase-analysis.md).

### Step 2: Generate render.yaml

Create a `render.yaml` Blueprint file following the Blueprint specification.

Complete specification: [references/blueprint-spec.md](references/blueprint-spec.md)

**Key Points:**
- Always use `plan: free` unless user specifies otherwise
- Include ALL environment variables the app needs
- Mark secrets with `sync: false` (user fills these in Dashboard)
- Use appropriate service type: `web`, `worker`, `cron`, `static`, or `pserv`
- Use appropriate runtime: [references/runtimes.md](references/runtimes.md)

**Basic Structure:**
```yaml
services:
  - type: web
    name: my-app
    runtime: node
    plan: free
    buildCommand: npm ci
    startCommand: npm start
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString
      - key: JWT_SECRET
        sync: false  # User fills in Dashboard

databases:
  - name: postgres
    databaseName: myapp_db
    plan: free
```

**Service Types:**
- `web`: HTTP services, APIs, web applications (publicly accessible)
- `worker`: Background job processors (not publicly accessible)
- `cron`: Scheduled tasks that run on a cron schedule
- `static`: Static sites (HTML/CSS/JS served via CDN)
- `pserv`: Private services (internal only, within same account)

Service type details: [references/service-types.md](references/service-types.md)
Runtime options: [references/runtimes.md](references/runtimes.md)
Template examples: [assets/](assets/)

### Step 2.5: Immediate Next Steps (Always Provide)

After creating `render.yaml`, always give the user a short, explicit checklist and run validation immediately when the CLI is available:
1. **Authenticate (CLI)**: run `render whoami -o json` (if not logged in, run `render login` or set `RENDER_API_KEY`)
2. **Validate (recommended)**: run `render blueprints validate`
   - If the CLI isn't installed, offer to install it and provide the command.
3. **Commit + push**: `git add render.yaml && git commit -m "Add Render deployment configuration" && git push origin main`
4. **Open Dashboard**: Use the Blueprint deeplink and complete Git OAuth if prompted
5. **Fill secrets**: Set env vars marked `sync: false`
6. **Deploy**: Click "Apply" and monitor the deploy

### Step 3: Validate Configuration

Validate the render.yaml file to catch errors before deployment. If the CLI is installed, run the commands directly; only prompt the user if the CLI is missing:

```bash
render whoami -o json  # Ensure CLI is authenticated (won't always prompt)
render blueprints validate
```

Fix any validation errors before proceeding. Common issues:
- Missing required fields (`name`, `type`, `runtime`)
- Invalid runtime values
- Incorrect YAML syntax
- Invalid environment variable references

Configuration guide: [references/configuration-guide.md](references/configuration-guide.md)

### Step 4: Commit and Push

**IMPORTANT:** You must merge the `render.yaml` file into your repository before deploying.

Ensure the `render.yaml` file is committed and pushed to your Git remote:

```bash
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main
```

If there is no Git remote yet, stop here and guide the user to create a GitHub/GitLab/Bitbucket repo, add it as `origin`, and push before continuing.

**Why this matters:** The Dashboard deeplink will read the render.yaml from your repository. If the file isn't merged and pushed, Render won't find the configuration and deployment will fail.

Verify the file is in your remote repository before proceeding to the next step.

### Step 5: Generate Deeplink

Get the Git repository URL:

```bash
git remote get-url origin
```

This will return a URL from your Git provider. **If the URL is SSH format, convert it to HTTPS:**

| SSH Format | HTTPS Format |
|------------|--------------|
| `git@github.com:user/repo.git` | `https://github.com/user/repo` |
| `git@gitlab.com:user/repo.git` | `https://gitlab.com/user/repo` |
| `git@bitbucket.org:user/repo.git` | `https://bitbucket.org/user/repo` |

**Conversion pattern:** Replace `git@<host>:` with `https://<host>/` and remove `.git` suffix.

Format the Dashboard deeplink using the HTTPS repository URL:
```
https://dashboard.render.com/blueprint/new?repo=<REPOSITORY_URL>
```

Example:
```
https://dashboard.render.com/blueprint/new?repo=https://github.com/username/repo-name
```

### Step 6: Guide User

**CRITICAL:** Ensure the user has merged and pushed the render.yaml file to their repository before clicking the deeplink. If the file isn't in the repository, Render cannot read the Blueprint configuration and deployment will fail.

Provide the deeplink to the user with these instructions:

1. **Verify render.yaml is merged** - Confirm the file exists in your repository on GitHub/GitLab/Bitbucket
2. Click the deeplink to open Render Dashboard
3. Complete Git provider OAuth if prompted
4. Name the Blueprint (or use default from render.yaml)
5. Fill in secret environment variables (marked with `sync: false`)
6. Review services and databases configuration
7. Click "Apply" to deploy

The deployment will begin automatically. Users can monitor progress in the Render Dashboard.

### Step 7: Verify Deployment

After the user deploys via Dashboard, verify everything is working.

**Check deployment status via MCP:**
```
list_deploys(serviceId: "<service-id>", limit: 1)
```
Look for `status: "live"` to confirm successful deployment.

**Check for runtime errors (wait 2-3 minutes after deploy):**
```
list_logs(resource: ["<service-id>"], level: ["error"], limit: 20)
```

**Check service health metrics:**
```
get_metrics(
  resourceId: "<service-id>",
  metricTypes: ["http_request_count", "cpu_usage", "memory_usage"]
)
```

If errors are found, proceed to the **Post-deploy verification and basic triage** section below.

---

# Method 2: Direct Service Creation (Quick Single-Service Deployments)

For simple deployments without Infrastructure-as-Code, create services directly via MCP tools.

## When to Use Direct Creation

- Single web service or static site
- Quick prototypes or demos
- When you don't need a render.yaml file in your repo
- Adding databases or cron jobs to existing projects

## Prerequisites for Direct Creation

**Repository must be pushed to a Git provider.** Render clones your repository to build and deploy services.

```bash
git remote -v  # Verify remote exists
git push origin main  # Ensure code is pushed
```

Supported providers: GitHub, GitLab, Bitbucket

If no remote exists, stop and ask the user to create/push a remote or switch to Docker image deploy.

**Note:** MCP does not support creating image-backed services. Use the Dashboard/API for prebuilt Docker image deploys.

## Direct Creation Workflow

Use the concise steps below, and refer to [references/direct-creation.md](references/direct-creation.md) for full MCP command examples and follow-on configuration.

### Step 1: Analyze Codebase
Use [references/codebase-analysis.md](references/codebase-analysis.md) to determine runtime, build/start commands, env vars, and datastores.

### Step 2: Create Resources via MCP
Create the service (web or static) and any required databases or key-value stores. See [references/direct-creation.md](references/direct-creation.md).

If MCP returns an error about missing Git credentials or repo access, stop and guide the user to connect their Git provider in the Render Dashboard, then retry.

### Step 3: Configure Environment Variables
Add required env vars via MCP after creation. See [references/direct-creation.md](references/direct-creation.md).

Remind the user that secrets can be set in the Dashboard if they prefer not to pass them via MCP.

### Step 4: Verify Deployment
Check deploy status, logs, and metrics. See [references/direct-creation.md](references/direct-creation.md).

---

For service discovery, configuration details, quick commands, and common issues, see [references/deployment-details.md](references/deployment-details.md).

---

# Post-deploy verification and basic triage (All Methods)

Keep this short and repeatable. If any check fails, fix it before redeploying.

1. Confirm the latest deploy is `live` and serving traffic
2. Hit the health endpoint (or root) and verify a 200 response
3. Scan recent error logs for a clear failure signature
4. Verify required env vars and port binding (`0.0.0.0:$PORT`)

Detailed checklist and commands: [references/post-deploy-checks.md](references/post-deploy-checks.md)

If the service fails to start or health checks time out, use the basic triage guide:
[references/troubleshooting-basics.md](references/troubleshooting-basics.md)

## Troubleshooting

### Escalated Network Access

If deployment fails due to network issues (timeouts, DNS errors, connection resets), rerun the deploy with escalated permissions (use `sandbox_permissions=require_escalated`). The deploy requires escalated network access when sandbox networking blocks outbound requests.

Example guidance to the user:

```
The deploy needs escalated network access to deploy to Render. I can rerun the command with escalated permissions—want me to proceed?
```

Optional: If you need deeper diagnostics (metrics/DB checks/error catalog), suggest installing the
`render-debug` skill. It is not required for the core deploy flow.

---

## Reference: Blueprint Spec

# Render Blueprint Specification

Complete reference for render.yaml Blueprint files. Blueprints define your infrastructure as code for reproducible deployments on Render.

## Overview

A Blueprint is a YAML file (typically `render.yaml`) placed in your repository root that describes:
- Services (web, worker, cron, static, private)
- Databases (PostgreSQL, Redis)
- Environment variables and secrets
- Scaling and resource configuration
- Project organization

## Root-Level Structure

```yaml
# Top-level fields
services: []         # Array of service definitions
databases: []        # Array of PostgreSQL databases
envVarGroups: []     # Reusable environment variable groups (optional)
projects: []         # Project organization (optional)
ungrouped: []        # Resources outside projects (optional)
previews:            # Preview environment configuration (optional)
  generation: auto_preview | manual | none
```

## Service Types

### Web Services (`type: web`)

HTTP services, APIs, and web applications. Publicly accessible via HTTPS.

**Required fields:**
- `name`: Unique service identifier
- `type`: Must be `web`
- `runtime`: Language/environment (see Runtimes section)
- `buildCommand`: Command to build the application
- `startCommand`: Command to start the server

**Common optional fields:**
- `plan`: Instance type (default: `free`)
- `region`: Deployment region (default: `oregon`)
- `branch`: Git branch to deploy (default: `main`)
- `autoDeploy`: Auto-deploy on push (default: `true`)
- `envVars`: Environment variables array
- `healthCheckPath`: Health check endpoint (default: `/`)
- `numInstances`: Number of instances (manual scaling)
- `scaling`: Autoscaling configuration

**Example:**
```yaml
services:
  - type: web
    name: api-server
    runtime: node
    plan: free
    buildCommand: npm ci
    startCommand: npm start
    branch: main
    autoDeploy: true
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 10000
```

### Worker Services (`type: worker`)

Background job processors, queue consumers. Not publicly accessible.

**Required fields:**
- `name`: Unique service identifier
- `type`: Must be `worker`
- `runtime`: Language/environment
- `buildCommand`: Command to build
- `startCommand`: Command to start worker process

**Key differences from web services:**
- No public URL
- No health checks
- No port binding required

**Example:**
```yaml
services:
  - type: worker
    name: job-processor
    runtime: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: celery -A tasks worker --loglevel=info
    envVars:
      - key: REDIS_URL
        fromDatabase:
          name: redis
          property: connectionString
```

### Cron Jobs (`type: cron`)

Scheduled tasks that run on a cron schedule.

**Required fields:**
- `name`: Unique service identifier
- `type`: Must be `cron`
- `runtime`: Language/environment
- `schedule`: Cron expression
- `buildCommand`: Command to build
- `startCommand`: Command to execute on schedule

**Schedule format:** Standard cron syntax (minute hour day month weekday)

**Examples:**
- `0 0 * * *` - Daily at midnight UTC
- `*/15 * * * *` - Every 15 minutes
- `0 9 * * 1` - Every Monday at 9 AM UTC

**Example:**
```yaml
services:
  - type: cron
    name: daily-backup
    runtime: node
    schedule: "0 2 * * *"
    buildCommand: npm ci
    startCommand: node scripts/backup.js
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString
```

### Static Sites (`type: static` or `type: web` with `runtime: static`)

Serve static HTML/CSS/JS files via CDN.

**Required fields:**
- `name`: Unique service identifier
- `type`: `web`
- `runtime`: `static`
- `buildCommand`: Command to build static assets
- `staticPublishPath`: Path to built files (e.g., `./build`, `./dist`)

**Optional configuration:**
- `routes`: Routing rules for SPAs
- `headers`: Custom HTTP headers
- `buildFilter`: Path filters for build triggers

**Example:**
```yaml
services:
  - type: web
    name: react-app
    runtime: static
    buildCommand: npm ci && npm run build
    staticPublishPath: ./dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
    headers:
      - path: /*
        name: Cache-Control
        value: public, max-age=31536000, immutable
```

### Private Services (`type: pserv`)

Internal services accessible only within your Render account.

**Required fields:**
- `name`: Unique service identifier
- `type`: Must be `pserv`
- `runtime`: Language/environment
- `buildCommand`: Command to build
- `startCommand`: Command to start

**Use cases:**
- Internal APIs
- Database proxies
- Microservices not exposed to internet

**Example:**
```yaml
services:
  - type: pserv
    name: internal-api
    runtime: go
    plan: free
    buildCommand: go build -o bin/app
    startCommand: ./bin/app
```

## Runtimes

### Native Runtimes

**Node.js (`runtime: node`):**
- Versions: 14, 16, 18, 20, 21
- Default version: 20
- Specify version in `package.json` engines field

**Python (`runtime: python`):**
- Versions: 3.8, 3.9, 3.10, 3.11, 3.12
- Default version: 3.11
- Specify version in `runtime.txt` or `Pipfile`

**Go (`runtime: go`):**
- Versions: 1.20, 1.21, 1.22, 1.23
- Uses go modules
- Version from `go.mod`

**Ruby (`runtime: ruby`):**
- Versions: 3.0, 3.1, 3.2, 3.3
- Uses Bundler
- Version from `.ruby-version` or `Gemfile`

**Rust (`runtime: rust`):**
- Latest stable version
- Uses Cargo

**Elixir (`runtime: elixir`):**
- Latest stable version
- Uses Mix

### Docker Runtime

**Docker (`runtime: docker`):**
Build from a Dockerfile in your repository.

**Additional fields:**
- `dockerfilePath`: Path to Dockerfile (default: `./Dockerfile`)
- `dockerContext`: Build context directory (default: `.`)

**Example:**
```yaml
services:
  - type: web
    name: docker-app
    runtime: docker
    dockerfilePath: ./docker/Dockerfile
    dockerContext: .
    plan: free
```

**Image (`runtime: image`):**
Deploy pre-built Docker images from a registry.

**Additional fields:**
- `image`: Image URL (e.g., `registry.com/image:tag`)
- `registryCredential`: Credentials for private registries

**Example:**
```yaml
services:
  - type: web
    name: prebuilt-app
    runtime: image
    image: myregistry.com/app:v1.2.3
    plan: free
```

## Service Plans

Available instance types:

| Plan | RAM | CPU | Price |
|------|-----|-----|-------|
| `free` | 512 MB | 0.5 | Free (750 hrs/mo) |
| `starter` | 512 MB | 0.5 | $7/month |
| `standard` | 2 GB | 1 | $25/month |
| `pro` | 4 GB | 2 | $85/month |
| `pro_plus` | 8 GB | 4 | $175/month |

**Always default to `plan: free` unless user specifies otherwise.**

## Regions

Available deployment regions:

- `oregon` (US West) - Default
- `ohio` (US East)
- `virginia` (US East)
- `frankfurt` (EU)
- `singapore` (Asia)

**Example:**
```yaml
services:
  - type: web
    name: my-app
    runtime: node
    region: frankfurt
```

## Environment Variables

Three patterns for defining environment variables:

### 1. Hardcoded Values

For non-sensitive configuration:

```yaml
envVars:
  - key: NODE_ENV
    value: production
  - key: API_URL
    value: https://api.example.com
  - key: LOG_LEVEL
    value: info
```

### 2. Generated Secrets

Render generates a base64-encoded 256-bit random value:

```yaml
envVars:
  - key: SESSION_SECRET
    generateValue: true
  - key: ENCRYPTION_KEY
    generateValue: true
```

### 3. User-Provided Secrets

Prompt user for values during Blueprint creation:

```yaml
envVars:
  - key: STRIPE_SECRET_KEY
    sync: false
  - key: JWT_SECRET
    sync: false
  - key: API_KEY
    sync: false
```

**The `sync: false` flag means "user will fill this in the Dashboard".**

### 4. Database References

Link to database connection strings:

```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: postgres
      property: connectionString
  - key: REDIS_URL
    fromDatabase:
      name: redis
      property: connectionString
```

**Available properties:**
- `connectionString`: Full connection URL
- `host`: Database host
- `port`: Database port
- `user`: Database username
- `password`: Database password
- `database`: Database name
- `hostport`: Combined `host:port`

### 5. Service References

Link to other services:

```yaml
envVars:
  - key: API_URL
    fromService:
      name: api-server
      type: web
      property: host
```

### 6. Environment Variable Groups

Reusable groups shared across services:

```yaml
envVarGroups:
  - name: shared-config
    envVars:
      - key: LOG_LEVEL
        value: info
      - key: ENVIRONMENT
        value: production

services:
  - type: web
    name: web-app
    runtime: node
    envVars:
      - fromGroup: shared-config
      - key: PORT
        value: 10000
```

## Databases

### PostgreSQL

```yaml
databases:
  - name: postgres
    databaseName: myapp_prod
    user: myapp_user
    plan: free
    postgresMajorVersion: "15"
    ipAllowList: []
```

**Plans:**
- `free`: 1 GB storage, 97 MB RAM, 0.1 CPU
- `basic-256mb`, `basic-512mb`, `basic-1gb`, `basic-4gb`
- `pro-4gb`, `pro-8gb`, `pro-16gb`, etc.
- `accelerated-4gb`, `accelerated-8gb`, etc. (SSD-backed)

**Key fields:**
- `name`: Identifier for references
- `databaseName`: Actual PostgreSQL database name
- `user`: Database username
- `postgresMajorVersion`: PostgreSQL version (11-16)
- `ipAllowList`: Array of CIDR blocks (empty = internal only)
- `diskSizeGB`: Storage size (paid plans only)

**High Availability (paid plans):**
```yaml
databases:
  - name: postgres
    databaseName: myapp_prod
    plan: pro-4gb
    highAvailabilityEnabled: true
```

**Read Replicas (paid plans):**
```yaml
databases:
  - name: postgres
    databaseName: myapp_prod
    plan: pro-4gb
    readReplicas:
      - name: read-replica-1
        region: ohio
      - name: read-replica-2
        region: frankfurt
```

### Redis (Key-Value Store)

```yaml
databases:
  - name: redis
    plan: free
    maxmemoryPolicy: allkeys-lru
    ipAllowList: []
```

**Plans:** Same as PostgreSQL

**maxmemoryPolicy options:**
- `allkeys-lru`: Evict least recently used keys
- `volatile-lru`: Evict LRU keys with TTL
- `allkeys-random`: Evict random keys
- `volatile-random`: Evict random keys with TTL
- `volatile-ttl`: Evict keys with soonest TTL
- `noeviction`: Return errors when memory full

## Scaling

### Manual Scaling

Fixed number of instances:

```yaml
services:
  - type: web
    name: my-app
    runtime: node
    plan: standard
    numInstances: 3
```

### Autoscaling

Dynamic scaling based on CPU/memory (Professional workspace required):

```yaml
services:
  - type: web
    name: my-app
    runtime: node
    plan: standard
    scaling:
      minInstances: 1
      maxInstances: 5
      targetCPUPercent: 60
      targetMemoryPercent: 70
```

**Notes:**
- Autoscaling disabled in preview environments
- Preview environments run `minInstances` count
- Requires Professional or higher workspace

## Health Checks

Configure health check endpoints:

```yaml
services:
  - type: web
    name: my-app
    runtime: node
    healthCheckPath: /health
```

**Default:** `/` (root path)

**Recommended:** Add a dedicated `/health` endpoint that returns `200 OK`.

## Build Filters

Control when builds are triggered based on changed files:

```yaml
services:
  - type: web
    name: frontend
    runtime: static
    buildFilter:
      paths:
        - frontend/**
      ignoredPaths:
        - frontend/README.md
        - frontend/**/*.test.js
```

**Behavior:**
- If `paths` specified: Build only when files in those paths change
- If `ignoredPaths` specified: Don't build when only ignored files change

## Projects and Environments

Organize services into projects with multiple environments:

```yaml
projects:
  - name: my-application
    environments:
      - name: production
        services:
          - type: web
            name: prod-api
            runtime: node
            plan: pro
            buildCommand: npm ci
            startCommand: npm start
        databases:
          - name: prod-postgres
            plan: pro-4gb
        networking:
          isolation: enabled
        permissions:
          protection: enabled

      - name: staging
        services:
          - type: web
            name: staging-api
            runtime: node
            plan: starter
            buildCommand: npm ci
            startCommand: npm start
        databases:
          - name: staging-postgres
            plan: free
```

**Environment features:**
- `networking.isolation`: Enable network isolation between environments
- `permissions.protection`: Require approval for environment changes

## Preview Environments

Configure automatic preview environments for pull requests:

```yaml
previews:
  generation: auto_preview  # auto_preview | manual | none
```

**Options:**
- `auto_preview`: Create preview environment for each PR automatically
- `manual`: User manually triggers preview creation
- `none`: Disable preview environments

## Complete Example

Full-featured Blueprint with multiple services and databases:

```yaml
services:
  # Web service
  - type: web
    name: web-app
    runtime: node
    plan: free
    region: oregon
    buildCommand: npm ci && npm run build
    startCommand: npm start
    branch: main
    autoDeploy: true
    healthCheckPath: /health
    envVars:
      - key: NODE_ENV
        value: production
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString
      - key: REDIS_URL
        fromDatabase:
          name: redis
          property: connectionString
      - key: JWT_SECRET
        sync: false

  # Background worker
  - type: worker
    name: queue-worker
    runtime: node
    plan: free
    buildCommand: npm ci
    startCommand: node worker.js
    envVars:
      - key: REDIS_URL
        fromDatabase:
          name: redis
          property: connectionString

  # Cron job
  - type: cron
    name: daily-cleanup
    runtime: node
    schedule: "0 3 * * *"
    buildCommand: npm ci
    startCommand: node scripts/cleanup.js
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: postgres
          property: connectionString

  # Static frontend
  - type: web
    name: frontend
    runtime: static
    buildCommand: npm ci && npm run build
    staticPublishPath: ./dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html

databases:
  - name: postgres
    databaseName: app_production
    user: app_user
    plan: free
    postgresMajorVersion: "15"
    ipAllowList: []

  - name: redis
    plan: free
    maxmemoryPolicy: allkeys-lru
    ipAllowList: []
```

## Validation

Validate your Blueprint before deploying (when CLI command is available):

```bash
render blueprint validate
```

**Common validation errors:**
- Missing required fields
- Invalid runtime values
- Incorrect environment variable references
- Invalid cron expressions
- Invalid YAML syntax

## Best Practices

1. **Always use `plan: free` by default** - Let users upgrade if needed
2. **Mark all secrets with `sync: false`** - Never hardcode sensitive values
3. **Use `fromDatabase` for database URLs** - Automatic internal connection strings
4. **Add health check endpoints** - Faster deployment detection
5. **Use non-interactive build commands** - Prevents build hangs
6. **Bind to `0.0.0.0:$PORT`** - Required for web services
7. **Use environment variable groups** - Share config across services
8. **Enable autoDeploy: true** - Deploy automatically on push
9. **Set appropriate regions** - Choose closest to your users
10. **Use build filters** - Optimize build triggers in monorepos

## Additional Resources

- Official Blueprint Specification: https://render.com/docs/blueprint-spec
- Render CLI Documentation: https://render.com/docs/cli
- Environment Variables Guide: https://render.com/docs/environment-variables

---

## Reference: Codebase Analysis

# Codebase Analysis (Deploy)

Use this reference for framework-specific detection and build/start command selection when preparing a Render deployment.

## Node.js Projects
- Read `package.json` to detect framework (Express, Next.js, Nest.js, Fastify, etc.)
- Check `scripts` section for build/start commands
- Look for `engines` field for Node version, or look in `.node-versions` or `.nvmrc`
- Detect package manager:
  - `bun.lockb` (Bun) -> `bun install --frozen-lockfile` / `bun run start`
  - `pnpm-lock.yaml` (pnpm) -> `pnpm install --frozen-lockfile` / `pnpm start`
  - `yarn.lock` (Yarn) -> `yarn install --frozen-lockfile` / `yarn start`
  - `package-lock.json` (npm) -> `npm ci` / `npm start`
  - `package.json` only (npm fallback) -> `npm install` / `npm start`

## Python Projects
- Check for dependency files and detect package manager:
  - `uv.lock` (uv) -> `uv sync` / `uv run gunicorn app:app`
  - `poetry.lock` (Poetry) -> `poetry install --no-dev` / `poetry run gunicorn app:app`
  - `Pipfile.lock` (pipenv) -> `pipenv install --deploy` / `pipenv run gunicorn app:app`
  - `requirements.txt` (pip) -> `pip install -r requirements.txt` / `gunicorn app:app`
  - `pyproject.toml` only -> check for `[tool.uv]`, `[tool.poetry]`, or use pip
- Detect framework: Django, Flask, FastAPI, Celery, others
- Check for Python version:
  - `.python-version` (uv/pyenv)
  - `runtime.txt` (Render-specific)
  - `pyproject.toml` (requires-python field)

## Go Projects
- Read `go.mod` for dependencies
- Identify web framework (Gin, Echo, Chi, Fiber, net/http)
- Note Go version from `go.mod`

## Static Sites
- Look for build output directories (`build/`, `dist/`, `site/`, `public/`)
- Detect framework: React, Vue, Gatsby, Next.js (static export)
- Check build scripts in `package.json`

## Docker Projects
- Look for `Dockerfile`
- Note exposed ports and build stages
- Check for `docker-compose.yml` patterns

## Key Information to Extract
- Build command (e.g., `npm ci`, `pip install -r requirements.txt`, `go build`)
- Start command (e.g., `npm start`, `gunicorn app:app`, `./bin/app`)
- Environment variables used in code (API keys, database URLs, secrets)
- Database requirements (PostgreSQL, Redis, MongoDB)
- Port binding (check if app uses an environment variable for port to run on)

---

## Reference: Configuration Guide

# Render Configuration Guide

Common configuration patterns, best practices, and troubleshooting for Render deployments.

## Environment Variables

### Required vs Optional Variables

**Always declare ALL environment variables in render.yaml**, even if values are provided by user later.

**Three categories:**

1. **Configuration values** (hardcoded):
```yaml
envVars:
  - key: NODE_ENV
    value: production
  - key: LOG_LEVEL
    value: info
  - key: API_URL
    value: https://api.example.com
```

2. **Secrets** (user provides):
```yaml
envVars:
  - key: JWT_SECRET
    sync: false
  - key: STRIPE_SECRET_KEY
    sync: false
  - key: API_KEY
    sync: false
```

3. **Auto-generated** (Render provides):
```yaml
envVars:
  - key: SESSION_SECRET
    generateValue: true
  - key: ENCRYPTION_KEY
    generateValue: true
```

### Database Connection Patterns

**PostgreSQL:**
```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: postgres
      property: connectionString
```

**Redis:**
```yaml
envVars:
  - key: REDIS_URL
    fromDatabase:
      name: redis
      property: connectionString
```

**Multiple databases:**
```yaml
envVars:
  - key: PRIMARY_DB_URL
    fromDatabase:
      name: postgres-primary
      property: connectionString
  - key: ANALYTICS_DB_URL
    fromDatabase:
      name: postgres-analytics
      property: connectionString
  - key: CACHE_URL
    fromDatabase:
      name: redis
      property: connectionString
```

### Cross-Service References

Reference other services in your account:

```yaml
services:
  - type: web
    name: frontend
    runtime: node
    envVars:
      - key: API_URL
        fromService:
          name: backend-api
          type: web
          property: host  # or hostport, port

  - type: web
    name: backend-api
    runtime: node
```

**Available properties:**
- `host`: Service hostname
- `port`: Service port
- `hostport`: Combined `host:port`

### Environment Variable Groups

Share common configuration across services:

```yaml
envVarGroups:
  - name: common-config
    envVars:
      - key: NODE_ENV
        value: production
      - key: LOG_LEVEL
        value: info
      - key: TZ
        value: UTC

services:
  - type: web
    name: web-app
    runtime: node
    envVars:
      - fromGroup: common-config
      - key: PORT
        value: 10000

  - type: worker
    name: worker
    runtime: node
    envVars:
      - fromGroup: common-config
```

---

## Port Binding

### The Port Binding Requirement

**CRITICAL:** Web services must bind to `0.0.0.0:$PORT`

**Why this matters:**
- Render sets `PORT` environment variable (default: 10000)
- Services must bind to `0.0.0.0` (not `localhost` or `127.0.0.1`)
- Health checks fail if port binding is incorrect
- Deployment will fail or service won't receive traffic

### Code Examples by Language

**Node.js / Express:**
```javascript
const express = require('express');
const app = express();

const PORT = process.env.PORT || 3000;

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
```

**Python / Flask:**
```python
import os
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

**Python / Django:**

In `settings.py`:
```python
# Django runs on port specified by environment
ALLOWED_HOSTS = ['*']
```

Start command in render.yaml:
```yaml
startCommand: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**Python / FastAPI:**
```python
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

Start command:
```yaml
startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Go:**
```go
package main

import (
    "fmt"
    "net/http"
    "os"
)

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "3000"
    }

    http.HandleFunc("/", handler)
    fmt.Printf("Server starting on port %s\n", port)
    http.ListenAndServe(":"+port, nil)
}
```

**Ruby / Rails:**

In `config/puma.rb`:
```ruby
port ENV.fetch("PORT") { 3000 }
bind "tcp://0.0.0.0:#{ENV.fetch('PORT', 3000)}"
```

**Rust / Actix:**
```rust
use actix_web::{App, HttpServer};
use std::env;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let addr = format!("0.0.0.0:{}", port);

    HttpServer::new(|| App::new())
        .bind(&addr)?
        .run()
        .await
}
```

---

## Build Commands

### Non-Interactive Flags

**Always use non-interactive flags** to prevent builds from hanging waiting for input.

**npm (Node.js):**
```yaml
buildCommand: npm ci
# NOT: npm install
```

**pip (Python):**
```yaml
buildCommand: pip install -r requirements.txt
# Already non-interactive
```

**apt (System packages):**
```yaml
buildCommand: apt-get update && apt-get install -y libpq-dev
# Use -y flag to auto-confirm
```

**bundler (Ruby):**
```yaml
buildCommand: bundle install --jobs=4 --retry=3
```

### Build with Additional Steps

**Node.js with build step:**
```yaml
buildCommand: npm ci && npm run build
```

**Python Django with static files:**
```yaml
buildCommand: pip install -r requirements.txt && python manage.py collectstatic --no-input
```

**Ruby Rails with assets:**
```yaml
buildCommand: bundle install && bundle exec rails assets:precompile
```

### Build Timeouts

**Free tier:** 15 minutes
**Paid tiers:** Configurable

**If builds timeout:**
1. Optimize dependencies (remove unused packages)
2. Use build caching
3. Consider pre-building in CI/CD
4. Upgrade to paid tier for longer timeouts

---

## Database Connections

### Internal vs External URLs

**Use internal URLs for better performance:**

When using `fromDatabase`, Render automatically provides internal `.render-internal.com` URLs:

```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: postgres
      property: connectionString
```

This provides: `postgresql://user:pass@postgres.render-internal.com:5432/db`

**Benefits:**
- Lower latency (same data center)
- No external bandwidth charges
- Automatic internal DNS

### Connection Pooling

**Node.js / PostgreSQL:**
```javascript
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

**Python / PostgreSQL:**
```python
import psycopg2.pool

pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=20,
    dsn=os.environ['DATABASE_URL']
)
```

**Django Settings:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'URL': os.environ['DATABASE_URL'],
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Database Migrations

**Run migrations during build:**

**Django:**
```yaml
buildCommand: pip install -r requirements.txt && python manage.py migrate
```

**Rails:**
```yaml
buildCommand: bundle install && bundle exec rails db:migrate
```

**Node.js / Prisma:**
```yaml
buildCommand: npm ci && npx prisma migrate deploy
```

---

## Free Tier Limitations

### What's Included

**Free tier provides:**
- 1 web service
- 1 PostgreSQL database (1 GB storage, 97 MB RAM)
- 750 hours/month compute
- 512 MB RAM per service
- 0.5 CPU per service
- 100 GB bandwidth/month

### Resource Limits

**Memory (512 MB):**
- Monitor memory usage in logs
- Optimize for memory-constrained environments
- Use lightweight dependencies

**CPU (0.5 cores):**
- Suitable for low-traffic applications
- Consider upgrading for higher traffic

**Spin Down (Free services):**
- Services spin down after 15 minutes of inactivity
- First request after spin down takes ~30 seconds (cold start)
- Upgrade to paid tier for always-on services

### When to Upgrade

**Upgrade to paid plan when:**
- Need more than 1 web service
- Need always-on services (no spin down)
- Traffic exceeds free tier limits
- Need more memory/CPU
- Need faster build times
- Need preview environments

---

## Health Checks

### Adding Health Check Endpoints

**Node.js / Express:**
```javascript
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString()
  });
});
```

**Python / Flask:**
```python
@app.route('/health')
def health():
    return {'status': 'ok'}, 200
```

**Python / FastAPI:**
```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Go:**
```go
http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    w.Write([]byte(`{"status":"ok"}`))
})
```

### Configure in render.yaml

```yaml
services:
  - type: web
    name: my-app
    runtime: node
    healthCheckPath: /health
```

**Benefits:**
- Faster deployment detection
- Better monitoring
- Automatic restart on health check failures

---

## Common Deployment Issues

### Issue 1: Missing Environment Variables

**Symptom:** Service crashes with "undefined variable" errors

**Solution:** Add all required env vars to render.yaml:
```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: postgres
      property: connectionString
  - key: JWT_SECRET
    sync: false  # User fills in Dashboard
```

### Issue 2: Port Binding Errors

**Symptom:** `EADDRINUSE` or health check timeout errors

**Solution:** Ensure app binds to `0.0.0.0:$PORT`:
```javascript
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0');
```

### Issue 3: Build Hangs

**Symptom:** Build times out after 15 minutes

**Solution:** Use non-interactive build commands:
```yaml
buildCommand: npm ci  # NOT npm install
```

### Issue 4: Database Connection Fails

**Symptom:** `ECONNREFUSED` on port 5432

**Solutions:**
1. Use `fromDatabase` for automatic internal URLs
2. Enable SSL for external connections
3. Check `ipAllowList` settings

### Issue 5: Static Site 404s

**Symptom:** Client-side routes return 404

**Solution:** Add SPA rewrite rules:
```yaml
routes:
  - type: rewrite
    source: /*
    destination: /index.html
```

### Issue 6: Out of Memory (OOM)

**Symptom:** Service crashes with `JavaScript heap out of memory`

**Solutions:**
1. Optimize application memory usage
2. Reduce dependency size
3. Upgrade to higher plan with more RAM

---

## Best Practices Checklist

**Environment Variables:**
- [ ] All env vars declared in render.yaml
- [ ] Secrets marked with `sync: false`
- [ ] Database URLs use `fromDatabase` references

**Port Binding:**
- [ ] App binds to `process.env.PORT`
- [ ] Bind to `0.0.0.0` (not `localhost`)

**Build Commands:**
- [ ] Use non-interactive flags (`npm ci`, `-y`, etc.)
- [ ] Build completes under 15 minutes (free tier)

**Start Commands:**
- [ ] Command starts HTTP server correctly
- [ ] Server binds to correct port

**Health Checks:**
- [ ] `/health` endpoint implemented
- [ ] Returns 200 status code

**Database:**
- [ ] Connection pooling configured
- [ ] Using internal URLs (`.render-internal.com`)
- [ ] SSL enabled if needed

**Plans:**
- [ ] Using `plan: free` by default
- [ ] Documented upgrade path for users

**Git Repository:**
- [ ] render.yaml committed to repository
- [ ] Pushed to git remote (GitHub/GitLab/Bitbucket)
- [ ] Branch specified in render.yaml (if not main)

---

## Additional Resources

- Blueprint Specification: [blueprint-spec.md](blueprint-spec.md)
- Service Types: [service-types.md](service-types.md)
- Runtimes: [runtimes.md](runtimes.md)
- Official Render Docs: https://render.com/docs

---

## Reference: Deployment Details

# Deployment Details

Use this reference for service discovery, configuration patterns, quick commands, and common issues.

## Service Discovery

**List all services:**
```
list_services()
```
Returns all services with IDs, names, types, and status.

**Get specific service details:**
```
get_service(serviceId: "<id>")
```
Returns full configuration including environment variables and build/start commands.

**List PostgreSQL databases:**
```
list_postgres_instances()
```

**List Key-Value stores:**
```
list_key_value()
```

## Configuration Details

### Environment Variables

**All environment variables must be declared in render.yaml.**

**Three patterns for environment variables:**

1. **Hardcoded values** (non-sensitive configuration):
```yaml
envVars:
  - key: NODE_ENV
    value: production
  - key: API_URL
    value: https://api.example.com
```

2. **Database connections** (auto-generated):
```yaml
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: postgres
      property: connectionString
  - key: REDIS_URL
    fromDatabase:
      name: redis
      property: connectionString
```

3. **Secrets** (user fills in Dashboard):
```yaml
envVars:
  - key: JWT_SECRET
    sync: false
  - key: API_KEY
    sync: false
  - key: STRIPE_SECRET_KEY
    sync: false
```

Complete environment variable guide: [configuration-guide.md](configuration-guide.md)

### Port Binding

**CRITICAL:** Web services must bind to `0.0.0.0:$PORT` (NOT `localhost`). Render sets the `PORT` environment variable.

**Node.js Example:**
```javascript
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
});
```

**Python Example:**
```python
import os

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

**Go Example:**
```go
port := os.Getenv("PORT")
if port == "" {
    port = "3000"
}
http.ListenAndServe(":"+port, handler)
```

### Plan Defaults

**Use `plan: free` unless the user specifies otherwise.** Refer to Render pricing for current limits and capacity.

### Build Commands

**Use non-interactive flags to prevent build hangs:**
- npm: `npm ci`
- yarn: `yarn install --frozen-lockfile`
- pnpm: `pnpm install --frozen-lockfile`
- bun: `bun install --frozen-lockfile`
- pip: `pip install -r requirements.txt`
- uv: `uv sync`
- apt: `apt-get install -y <package>`
- bundler: `bundle install --jobs=4 --retry=3`

### Database Connections

When services connect to databases in the same Render account, use `fromDatabase` references for internal URLs.

### Health Checks

Optional but recommended: add a `/health` endpoint for faster deployment detection.

## Quick Reference

### MCP Tools (Preferred)
```
# Service Discovery
list_services()
get_service(serviceId: "<id>")
list_postgres_instances()
list_key_value()

# Service Creation
create_web_service(name, runtime, buildCommand, startCommand, ...)
create_static_site(name, buildCommand, publishPath, ...)
create_cron_job(name, runtime, schedule, buildCommand, startCommand, ...)
create_postgres(name, plan, region)
create_key_value(name, plan, region)

# Environment Variables
update_environment_variables(serviceId, envVars: [{key, value}, ...])

# Deployment & Monitoring
list_deploys(serviceId, limit)
list_logs(resource: ["<id>"], level: ["error"])
get_metrics(resourceId, metricTypes: [...])

# Workspace
get_selected_workspace()
list_workspaces()
```

### CLI Commands
```bash
# Validate Blueprint
render blueprints validate

# Check workspace
render workspace current -o json
render workspace set

# List services
render services -o json

# View deployment logs
render logs -r <service-id> -o json

# Create deployment
render deploys create <service-id> --wait
```

### Templates by Framework
- Node.js Express: [../assets/node-express.yaml](../assets/node-express.yaml)
- Next.js + Postgres: [../assets/nextjs-postgres.yaml](../assets/nextjs-postgres.yaml)
- Django + Worker: [../assets/python-django.yaml](../assets/python-django.yaml)
- Static Site: [../assets/static-site.yaml](../assets/static-site.yaml)
- Go API: [../assets/go-api.yaml](../assets/go-api.yaml)
- Docker: [../assets/docker.yaml](../assets/docker.yaml)

### Documentation
- Full Blueprint specification: [blueprint-spec.md](blueprint-spec.md)
- Service types explained: [service-types.md](service-types.md)
- Runtime options: [runtimes.md](runtimes.md)
- Configuration guide: [configuration-guide.md](configuration-guide.md)

## Common Issues

**Issue:** Deployment fails with port binding error

**Solution:** Ensure app binds to `0.0.0.0:$PORT` (see Port Binding section above)

---

**Issue:** Build hangs or times out

**Solution:** Use non-interactive build commands (see Build Commands section above)

---

**Issue:** Missing environment variables in Dashboard

**Solution:** All env vars must be declared in render.yaml. Add missing vars with `sync: false` for secrets.

---

**Issue:** Database connection fails

**Solution:** Use `fromDatabase` references for internal connection strings.

---

**Issue:** Static site shows 404 for routes

**Solution:** Add rewrite rules to render.yaml for SPA routing:
```yaml
routes:
  - type: rewrite
    source: /*
    destination: /index.html
```

For more detailed troubleshooting, see the debug skill or [configuration-guide.md](configuration-guide.md).

---

## Reference: Direct Creation

# Direct Creation (MCP) Details

Use this reference for MCP direct-creation examples and follow-on configuration.

## Direct Creation Workflow

### Step 1: Analyze Codebase

Use [codebase-analysis.md](codebase-analysis.md) to determine runtime, build/start commands, env vars, and datastores.

### Step 2: Create Resources via MCP

**Create a Web Service:**
```
create_web_service(
  name: "my-api",
  runtime: "node",  # or python, go, rust, ruby, elixir, docker
  repo: "https://github.com/username/repo",
  branch: "main",  # optional, defaults to repo default branch
  buildCommand: "npm ci",
  startCommand: "npm start",
  plan: "free",  # free, starter, standard, pro, pro_max, pro_plus, pro_ultra
  region: "oregon",  # oregon, frankfurt, singapore, ohio, virginia
  envVars: [
    {"key": "NODE_ENV", "value": "production"}
  ]
)
```

**Create a Static Site:**
```
create_static_site(
  name: "my-frontend",
  repo: "https://github.com/username/repo",
  branch: "main",
  buildCommand: "npm run build",
  publishPath: "dist",  # or build, public, out
  envVars: [
    {"key": "VITE_API_URL", "value": "https://api.example.com"}
  ]
)
```

**Create a Cron Job:**
```
create_cron_job(
  name: "daily-cleanup",
  runtime: "node",
  repo: "https://github.com/username/repo",
  schedule: "0 0 * * *",  # Daily at midnight (cron syntax)
  buildCommand: "npm ci",
  startCommand: "node scripts/cleanup.js",
  plan: "free"
)
```

**Create a PostgreSQL Database:**
```
create_postgres(
  name: "myapp-db",
  plan: "free",  # free, basic_256mb, basic_1gb, basic_4gb, pro_4gb, etc.
  region: "oregon"
)
```

**Create a Key-Value Store (Redis):**
```
create_key_value(
  name: "myapp-cache",
  plan: "free",  # free, starter, standard, pro, pro_plus
  region: "oregon",
  maxmemoryPolicy: "allkeys_lru"  # eviction policy
)
```

### Step 3: Configure Environment Variables

After creating services, add environment variables:

```
update_environment_variables(
  serviceId: "<service-id-from-creation>",
  envVars: [
    {"key": "DATABASE_URL", "value": "<connection-string>"},
    {"key": "JWT_SECRET", "value": "<secret-value>"},
    {"key": "API_KEY", "value": "<api-key>"}
  ]
)
```

**Note:** For database connection strings, get the internal URL from the database details in Dashboard or via `get_postgres(postgresId: "<id>")`.

### Step 4: Verify Deployment

Services with `autoDeploy: "yes"` (default) will deploy automatically when created.

**Check deployment status:**
```
list_deploys(serviceId: "<service-id>", limit: 1)
```

**Monitor logs for errors:**
```
list_logs(resource: ["<service-id>"], level: ["error"], limit: 50)
```

**Check health metrics:**
```
get_metrics(
  resourceId: "<service-id>",
  metricTypes: ["http_request_count", "cpu_usage", "memory_usage"]
)
```

---

## Reference: Error Patterns

# Error patterns (compact)

Use this to quickly map log signatures to likely causes and fixes.

| Log pattern | Likely cause | Quick fix |
| --- | --- | --- |
| `KeyError`, `not defined`, `missing environment` | Missing env var | Add env var in render.yaml or via MCP, then redeploy |
| `EADDRINUSE`, `listen EADDRINUSE` | Port binding conflict | Bind to `0.0.0.0:$PORT` |
| `Cannot find module`, `ModuleNotFoundError` | Missing dependency | Add dependency to manifest and rebuild |
| `ECONNREFUSED`, `connection refused` | DB not reachable | Verify DATABASE_URL and DB status |
| `Health check timeout` | No healthy response | Add/verify health endpoint and port |
| `exit 137`, `out of memory` | OOM | Reduce memory use or upgrade plan |
| `Command failed`, `build failed` | Bad build command | Fix build command or dependencies |

---

## Reference: Post Deploy Checks

# Post-deploy checks

Use this after any deploy or service creation. Keep it short; stop when a check fails.

## 1) Confirm deploy status

```
list_deploys(serviceId: "<service-id>", limit: 1)
```

- Expect `status: "live"`.
- If status is failed, inspect build/runtime logs immediately.

## 2) Verify service health

- Hit the health endpoint (preferred) or `/` and confirm a 200 response.
- If there is no health endpoint, add one and redeploy.

## 3) Scan recent error logs

```
list_logs(resource: ["<service-id>"], level: ["error"], limit: 50)
```

- If you see a clear error signature, jump to the matching fix in
  [troubleshooting-basics.md](troubleshooting-basics.md) or
  [error-patterns.md](error-patterns.md).

## 4) Verify env vars and port binding

- Confirm all required env vars are set (especially secrets marked `sync: false`).
- Ensure the app binds to `0.0.0.0:$PORT` (not localhost).

## 5) Redeploy only after fixing the first failure

- Avoid repeated deploys without changes; fix one issue at a time.

---

## Reference: Runtimes

# Render Runtime Options

Complete guide to available runtimes on Render, including versions, configuration, and best practices for each language.

## Native Language Runtimes

### Node.js (`runtime: node`)

**Supported Versions:** 14, 16, 18, 20, 21
**Default Version:** 20

**Version Specification:**

Specify Node version in `package.json`:
```json
{
  "engines": {
    "node": "20.x"
  }
}
```

**Package Managers:**
- **npm**: Default, uses `package-lock.json`
- **Yarn**: Auto-detected if `yarn.lock` exists
- **pnpm**: Auto-detected if `pnpm-lock.yaml` exists

**Common Build Commands:**
```bash
npm ci                          # Recommended (faster, reproducible)
npm ci && npm run build         # Build step included
yarn install --frozen-lockfile  # Yarn equivalent
pnpm install --frozen-lockfile  # pnpm equivalent
```

**Common Start Commands:**
```bash
npm start                       # Uses "start" script in package.json
node server.js                  # Direct file execution
node dist/main.js               # Built output
```

**Popular Frameworks:**
- Express.js, Fastify, Koa (APIs)
- Next.js (full-stack React)
- Nest.js (enterprise TypeScript)
- Remix (full-stack React)
- Nuxt.js (full-stack Vue)

**Example Configuration:**
```yaml
type: web
name: node-app
runtime: node
buildCommand: npm ci && npm run build
startCommand: npm start
```

---

### Python (`runtime: python`)

**Supported Versions:** 3.8, 3.9, 3.10, 3.11, 3.12
**Default Version:** 3.11

**Version Specification:**

Option 1 - `runtime.txt`:
```
python-3.11.5
```

Option 2 - `Pipfile`:
```toml
[requires]
python_version = "3.11"
```

**Package Managers:**
- **pip**: Default, uses `requirements.txt`
- **Poetry**: Auto-detected if `pyproject.toml` exists
- **Pipenv**: Auto-detected if `Pipfile` exists

**Common Build Commands:**
```bash
pip install -r requirements.txt
pip install -r requirements.txt && python manage.py collectstatic --no-input
poetry install --no-dev
pipenv install --deploy
```

**Common Start Commands:**
```bash
gunicorn app:app                                    # Flask
gunicorn config.wsgi:application                    # Django
uvicorn main:app --host 0.0.0.0 --port $PORT       # FastAPI
celery -A tasks worker                              # Celery worker
```

**Popular Frameworks:**
- Django (full-stack web framework)
- Flask (microframework)
- FastAPI (modern async API framework)
- Celery (task queue)

**Example Configuration:**
```yaml
type: web
name: python-app
runtime: python
buildCommand: pip install -r requirements.txt
startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
```

---

### Go (`runtime: go`)

**Supported Versions:** 1.20, 1.21, 1.22, 1.23
**Default Version:** Latest stable

**Version Specification:**

Specify in `go.mod`:
```go
module myapp

go 1.22
```

**Build System:** Uses Go modules

**Common Build Commands:**
```bash
go build -o bin/app .
go build -o bin/app cmd/server/main.go
go build -tags netgo -ldflags '-s -w' -o bin/app
```

**Common Start Commands:**
```bash
./bin/app
./bin/server
```

**Popular Frameworks:**
- net/http (standard library)
- Gin (fast web framework)
- Echo (high performance framework)
- Chi (lightweight router)
- Fiber (Express-inspired framework)
- Gorilla Mux (powerful router)

**Example Configuration:**
```yaml
type: web
name: go-app
runtime: go
buildCommand: go build -o bin/app .
startCommand: ./bin/app
```

---

### Ruby (`runtime: ruby`)

**Supported Versions:** 3.0, 3.1, 3.2, 3.3
**Default Version:** 3.3

**Version Specification:**

Option 1 - `.ruby-version`:
```
3.3.0
```

Option 2 - `Gemfile`:
```ruby
ruby '3.3.0'
```

**Package Manager:** Bundler (uses `Gemfile` and `Gemfile.lock`)

**Common Build Commands:**
```bash
bundle install --jobs=4 --retry=3
bundle install && bundle exec rails assets:precompile
```

**Common Start Commands:**
```bash
bundle exec rails server -b 0.0.0.0 -p $PORT
bundle exec puma -C config/puma.rb
bundle exec rackup -o 0.0.0.0 -p $PORT
bundle exec sidekiq                                  # Worker
```

**Popular Frameworks:**
- Ruby on Rails (full-stack framework)
- Sinatra (microframework)
- Sidekiq (background jobs)

**Example Configuration:**
```yaml
type: web
name: rails-app
runtime: ruby
buildCommand: bundle install && bundle exec rails assets:precompile
startCommand: bundle exec puma -C config/puma.rb
```

---

### Rust (`runtime: rust`)

**Supported Versions:** Latest stable
**Default Version:** Latest stable

**Build System:** Cargo

**Common Build Commands:**
```bash
cargo build --release
cargo build --release --locked
```

**Common Start Commands:**
```bash
./target/release/myapp
```

**Popular Frameworks:**
- Actix Web (powerful, performant)
- Rocket (web framework with focus on usability)
- Axum (modern, ergonomic framework)
- Warp (composable web framework)

**Example Configuration:**
```yaml
type: web
name: rust-app
runtime: rust
buildCommand: cargo build --release
startCommand: ./target/release/myapp
```

---

### Elixir (`runtime: elixir`)

**Supported Versions:** Latest stable
**Default Version:** Latest stable

**Build System:** Mix

**Common Build Commands:**
```bash
mix deps.get --only prod
mix deps.get && mix compile
mix do deps.get, compile, assets.deploy
```

**Common Start Commands:**
```bash
mix phx.server
elixir --name myapp -S mix phx.server
```

**Popular Frameworks:**
- Phoenix (full-stack web framework)
- Phoenix LiveView (real-time applications)

**Example Configuration:**
```yaml
type: web
name: elixir-app
runtime: elixir
buildCommand: mix deps.get --only prod && mix compile
startCommand: mix phx.server
```

---

## Container Runtimes

### Docker (`runtime: docker`)

Build your application from a Dockerfile in your repository.

**Additional Configuration:**
- `dockerfilePath`: Path to Dockerfile (default: `./Dockerfile`)
- `dockerContext`: Build context directory (default: `.`)

**Example Configuration:**
```yaml
type: web
name: docker-app
runtime: docker
dockerfilePath: ./Dockerfile
dockerContext: .
```

**Multi-stage Dockerfile Example:**
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --only=production
EXPOSE 10000
CMD ["node", "dist/main.js"]
```

**Best Practices:**
- Use multi-stage builds to reduce image size
- Copy `package.json` before source code (better caching)
- Use `.dockerignore` to exclude unnecessary files
- Expose port dynamically via `$PORT` environment variable
- Run as non-root user for security

---

### Pre-built Image (`runtime: image`)

Deploy pre-built Docker images from a container registry.

**Additional Configuration:**
- `image`: Full image URL with tag or digest
- `registryCredential`: Credentials for private registries

**Example with Public Image:**
```yaml
type: web
name: prebuilt-app
runtime: image
image: ghcr.io/myorg/myapp:v1.2.3
```

**Example with Private Registry:**
```yaml
type: web
name: private-app
runtime: image
image: myregistry.com/myapp:latest
registryCredential:
  username: my-username
  password:
    sync: false  # User provides in Dashboard
```

**Use Cases:**
- Deploy images built in CI/CD pipeline
- Use images from container registries
- Deploy Docker Hub images
- Use private registry images

---

## Static Runtime (`runtime: static`)

Serve pre-built static files without a backend runtime. Files are served via CDN.

**Additional Configuration:**
- `staticPublishPath`: Directory containing built files (e.g., `./dist`, `./build`)

**Common Build Commands by Framework:**

**React (Create React App):**
```bash
npm ci && npm run build
# Outputs to: ./build
```

**Vue:**
```bash
npm ci && npm run build
# Outputs to: ./dist
```

**Next.js (Static Export):**
```bash
npm ci && npm run build && npm run export
# Outputs to: ./out
```

**Gatsby:**
```bash
npm ci && npm run build
# Outputs to: ./public
```

**Vite:**
```bash
npm ci && npm run build
# Outputs to: ./dist
```

**Example Configuration:**
```yaml
type: web
name: react-app
runtime: static
buildCommand: npm ci && npm run build
staticPublishPath: ./build
```

---

## Runtime Comparison

| Runtime | Build Speed | Cold Start | Best For |
|---------|-------------|------------|----------|
| Node.js | Fast | Fast | APIs, full-stack apps |
| Python | Medium | Medium | Data apps, APIs, web |
| Go | Fast | Very Fast | High performance APIs |
| Ruby | Slow | Medium | Rails apps, traditional web |
| Rust | Very Slow | Very Fast | Performance-critical services |
| Elixir | Medium | Fast | Real-time, concurrent apps |
| Docker | Varies | Medium | Any language, custom setup |
| Static | Very Fast | N/A | SPAs, documentation, marketing |

---

## Choosing the Right Runtime

**Choose Node.js when:**
- Building JavaScript-based applications
- Need rich npm ecosystem
- Want fast iteration and deployment
- Building full-stack applications (Next.js, Remix)

**Choose Python when:**
- Building data-heavy applications
- Need machine learning libraries
- Django or Flask expertise
- Data processing pipelines

**Choose Go when:**
- Need high performance and low resource usage
- Building microservices
- Want simple deployment (single binary)
- Handling high concurrency

**Choose Ruby when:**
- Building traditional web applications
- Ruby on Rails expertise
- Rapid development priority

**Choose Rust when:**
- Maximum performance required
- Systems programming
- Resource-constrained environments

**Choose Docker when:**
- Need custom system dependencies
- Multi-language application
- Existing Dockerfile
- Need full control over environment

**Choose Static when:**
- Building SPAs or static sites
- No backend processing needed
- Want CDN caching and fast delivery
- Documentation or marketing sites

---

## Reference: Service Types

# Render Service Types

Detailed explanation of each service type available on Render. Choose the right service type based on your application's needs.

## Web Services (`type: web`)

### Purpose

Web services are HTTP servers that handle incoming requests from the internet. They're publicly accessible via HTTPS URLs.

### Use Cases

- **REST APIs**: JSON APIs for mobile apps or frontend applications
- **GraphQL servers**: GraphQL endpoints for client queries
- **Web applications**: Server-rendered websites (Django, Rails, Express)
- **Full-stack frameworks**: Next.js, Nuxt.js, Remix, SvelteKit
- **WebSocket servers**: Real-time communication servers
- **SSR applications**: Server-side rendered React, Vue, or Angular apps

### Key Characteristics

- **Public URL**: Automatically assigned `https://[service-name].onrender.com`
- **Port binding required**: Must bind to `0.0.0.0:$PORT`
- **Health checks**: Render pings your service to verify it's running
- **HTTPS**: Automatic SSL/TLS certificates
- **Load balancing**: Traffic distributed across multiple instances
- **Custom domains**: Support for your own domain names

### Required Configuration

```yaml
type: web
name: my-api
runtime: node
buildCommand: npm ci
startCommand: npm start
```

### Best Practices

1. **Bind to environment PORT**:
```javascript
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0');
```

2. **Add health check endpoint**:
```javascript
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});
```

3. **Use appropriate timeouts**: Web requests should complete within 30 seconds

4. **Implement graceful shutdown**: Handle SIGTERM signals properly

---

## Worker Services (`type: worker`)

### Purpose

Worker services run background tasks without handling HTTP requests. They're not publicly accessible.

### Use Cases

- **Queue processors**: Redis queue, BullMQ, Celery, Sidekiq
- **Background jobs**: Email sending, image processing, data exports
- **Event consumers**: Message queue consumers (Kafka, RabbitMQ, etc.)
- **Data pipeline workers**: ETL processes, data transformation
- **Scheduled background tasks**: Continuous processes (not cron)
- **WebSocket backend**: Dedicated WebSocket handler services

### Key Characteristics

- **No public URL**: Not accessible from internet
- **No port binding**: Doesn't need to listen on a port
- **No health checks**: Render monitors process health differently
- **Long-running**: Can run indefinitely
- **Private communication**: Access via internal networking
- **Restart on crash**: Automatically restarted if process dies

### Required Configuration

```yaml
type: worker
name: queue-processor
runtime: python
buildCommand: pip install -r requirements.txt
startCommand: celery -A tasks worker --loglevel=info
```

### Best Practices

1. **Connect to message queue**:
```python
import redis
r = redis.from_url(os.environ['REDIS_URL'])
```

2. **Implement retry logic**: Handle failures gracefully

3. **Monitor queue depth**: Track pending jobs

4. **Log processing status**: Make debugging easier

5. **Graceful shutdown**: Finish current jobs before exiting

### Common Patterns

**Node.js with BullMQ:**
```yaml
type: worker
name: job-processor
runtime: node
buildCommand: npm ci
startCommand: node worker.js
envVars:
  - key: REDIS_URL
    fromDatabase:
      name: redis
      property: connectionString
```

**Python with Celery:**
```yaml
type: worker
name: celery-worker
runtime: python
buildCommand: pip install -r requirements.txt
startCommand: celery -A app.celery worker
envVars:
  - key: REDIS_URL
    fromDatabase:
      name: redis
      property: connectionString
```

---

## Cron Jobs (`type: cron`)

### Purpose

Cron jobs run scheduled tasks on a repeating schedule. They execute, complete, and shut down.

### Use Cases

- **Database backups**: Regular automated backups
- **Report generation**: Daily/weekly reports
- **Data cleanup**: Delete old records periodically
- **Cache warming**: Pre-populate caches
- **Email digests**: Send scheduled email summaries
- **Data synchronization**: Sync between systems
- **Batch processing**: Process accumulated data

### Key Characteristics

- **Scheduled execution**: Runs on cron schedule
- **Automatic shutdown**: Shuts down after completing
- **No persistent port**: Doesn't maintain listening port
- **No health checks**: Task either completes or fails
- **UTC timezone**: All schedules in UTC
- **Maximum runtime**: Jobs timeout after configured limit

### Required Configuration

```yaml
type: cron
name: daily-backup
runtime: node
schedule: "0 2 * * *"  # Daily at 2 AM UTC
buildCommand: npm ci
startCommand: node scripts/backup.js
```

### Schedule Format

Standard cron syntax: `minute hour day month weekday`

**Common schedules:**

| Schedule | Description |
|----------|-------------|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour |
| `0 0 * * *` | Daily at midnight UTC |
| `0 9 * * 1-5` | Weekdays at 9 AM UTC |
| `0 0 1 * *` | First day of each month |
| `0 9 * * 1` | Every Monday at 9 AM UTC |

### Best Practices

1. **Handle failures gracefully**: Jobs should be idempotent

2. **Log completion status**: Track success/failure

3. **Set appropriate timeouts**: Match expected job duration

4. **Use UTC times**: All schedules are UTC-based

5. **Test thoroughly**: Test with different data scenarios

### Example Use Cases

**Daily Database Backup:**
```yaml
type: cron
name: db-backup
runtime: python
schedule: "0 1 * * *"  # 1 AM UTC daily
buildCommand: pip install -r requirements.txt
startCommand: python scripts/backup.py
envVars:
  - key: DATABASE_URL
    fromDatabase:
      name: postgres
      property: connectionString
  - key: S3_BUCKET
    value: my-backups
```

**Hourly Cache Refresh:**
```yaml
type: cron
name: cache-refresh
runtime: node
schedule: "0 * * * *"  # Top of every hour
buildCommand: npm ci
startCommand: node scripts/refresh-cache.js
```

---

## Static Sites (`type: web` + `runtime: static`)

### Purpose

Serve static HTML, CSS, and JavaScript files via CDN. No backend runtime.

### Use Cases

- **Single Page Applications (SPAs)**: React, Vue, Angular apps
- **Static site generators**: Gatsby, Next.js (static export), Hugo
- **Documentation sites**: MkDocs, Docusaurus, VitePress
- **Landing pages**: Marketing sites
- **Portfolio sites**: Personal websites
- **JAMstack sites**: Static sites with API integration

### Key Characteristics

- **CDN delivery**: Global edge caching
- **No backend runtime**: Only serves built files
- **Build output only**: Serves contents of build directory
- **Routing support**: Rewrite rules for SPA routing
- **Custom headers**: Cache control, security headers
- **Fast deployment**: Quick to build and deploy

### Required Configuration

```yaml
type: web
name: frontend
runtime: static
buildCommand: npm ci && npm run build
staticPublishPath: ./dist  # or ./build, ./out, ./public
```

### Routing for SPAs

Single Page Applications need rewrite rules to handle client-side routing:

```yaml
type: web
name: react-app
runtime: static
buildCommand: npm ci && npm run build
staticPublishPath: ./build
routes:
  - type: rewrite
    source: /*
    destination: /index.html
```

### Custom Headers

Add cache control and security headers:

```yaml
type: web
name: static-site
runtime: static
buildCommand: npm ci && npm run build
staticPublishPath: ./dist
headers:
  # Cache static assets
  - path: /static/*
    name: Cache-Control
    value: public, max-age=31536000, immutable

  # Security headers
  - path: /*
    name: X-Frame-Options
    value: DENY
  - path: /*
    name: X-Content-Type-Options
    value: nosniff
```

### Build Filters

For monorepos, only build when frontend files change:

```yaml
type: web
name: frontend
runtime: static
buildCommand: npm ci && npm run build
staticPublishPath: ./dist
buildFilter:
  paths:
    - frontend/**
  ignoredPaths:
    - frontend/**/*.test.js
    - frontend/README.md
```

### Best Practices

1. **Optimize build output**: Minify, compress, tree-shake

2. **Use proper cache headers**: Long cache for hashed assets

3. **Add security headers**: Protect against common attacks

4. **Configure SPA routing**: Add rewrite rules for client routing

5. **Handle 404s**: Create custom 404.html page

---

## Private Services (`type: pserv`)

### Purpose

Internal services accessible only within your Render account. Not exposed to the internet.

### Use Cases

- **Internal APIs**: Services accessed only by other services
- **Database proxies**: Connection pools, read replicas
- **Microservices**: Service mesh architectures
- **Admin tools**: Internal dashboards
- **Cache layers**: Internal caching services
- **Message brokers**: Internal message queues

### Key Characteristics

- **No public URL**: Only accessible via internal DNS
- **Internal networking**: Fast, low-latency connections
- **Port binding required**: Must bind to `0.0.0.0:$PORT`
- **Private DNS**: `[service-name].render-internal.com`
- **Same-account only**: Only accessible from same account
- **No internet access**: Traffic stays within Render network

### Required Configuration

```yaml
type: pserv
name: internal-api
runtime: node
buildCommand: npm ci
startCommand: npm start
```

### Accessing Private Services

From other services in the same account:

```javascript
// Use .render-internal.com domain
const API_URL = 'http://internal-api.render-internal.com:10000';
```

Or use service references:

```yaml
services:
  - type: web
    name: frontend
    runtime: node
    envVars:
      - key: INTERNAL_API_URL
        fromService:
          name: internal-api
          type: pserv
          property: hostport
```

### Best Practices

1. **Use internal DNS**: Always use `.render-internal.com` domains

2. **No authentication needed**: Already isolated to account

3. **Fast communication**: Low latency between services

4. **Simplify architecture**: No need for external load balancers

---

## Comparison Table

| Feature | Web | Worker | Cron | Static | Private |
|---------|-----|--------|------|--------|---------|
| Public URL | ✅ Yes | ❌ No | ❌ No | ✅ Yes | ❌ No |
| Port Binding | ✅ Required | ❌ Not needed | ❌ Not needed | ❌ N/A | ✅ Required |
| Health Checks | ✅ Yes | ❌ No | ❌ No | ❌ N/A | ✅ Yes |
| Runtime | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes |
| Persistent | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Scaling | ✅ Yes | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| Use Case | HTTP servers | Background jobs | Scheduled tasks | Static files | Internal services |

## Choosing the Right Service Type

**Use Web Service when:**
- Your app handles HTTP requests
- Users need to access it via URL
- You need load balancing and scaling

**Use Worker Service when:**
- Processing background jobs
- Consuming from message queues
- Running long-lived processes without HTTP

**Use Cron Job when:**
- Running scheduled tasks
- Processing doesn't need to be always-on
- Tasks run periodically (hourly, daily, weekly)

**Use Static Site when:**
- Serving pre-built HTML/CSS/JS
- No backend processing needed
- Want CDN caching and fast delivery

**Use Private Service when:**
- Service only accessed by other services
- Want internal-only communication
- Building microservice architectures

---

## Reference: Troubleshooting Basics

# Basic troubleshooting (deploy-time and startup)

Use this when a deploy fails, the service crashes on start, or health checks time out.
Keep fixes minimal and redeploy after each change.

## 1) Classify the failure

- **Build failure**: errors in build logs, missing dependencies, build command issues.
- **Startup failure**: app exits quickly, crashes, or cannot bind to `$PORT`.
- **Runtime/health failure**: service is live but health checks fail or 5xx errors.

## 2) Quick checks by class

**Build failure**
- Confirm the build command is correct for the runtime.
- Ensure required dependencies are present in `package.json`, `requirements.txt`, etc.
- Check for missing build-time env vars.

**Startup failure**
- Confirm the start command and working directory.
- Ensure port binding is `0.0.0.0:$PORT`.
- Check for missing runtime env vars (secrets, DB URLs).

**Runtime/health failure**
- Verify the health endpoint path and response.
- Confirm the app is actually listening on `$PORT`.
- Check database connectivity and migrations.

## 3) Map error signatures to fixes

Use [error-patterns.md](error-patterns.md) for a compact catalog of common log messages.

## 4) If still blocked

Gather the latest build logs and runtime error logs, then consider the optional
`render-debug` skill for deeper diagnostics (metrics, DB checks, expanded patterns).
