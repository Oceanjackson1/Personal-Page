---
title: "Comfyui Gateway"
description: "REST API gateway for ComfyUI servers. Workflow management, job queuing, webhooks, caching, auth, rate limiting, and image delivery (URL + base64)."
category: "workflow"
source: "community"
author: "Community"
tags: ["comfyui", "gateway"]
date: 2026-03-20
---

# ComfyUI Gateway

## Overview

REST API gateway for ComfyUI servers. Workflow management, job queuing, webhooks, caching, auth, rate limiting, and image delivery (URL + base64).

## When to Use This Skill

- When the user mentions "comfyui" or related topics
- When the user mentions "comfy ui" or related topics
- When the user mentions "stable diffusion api gateway" or related topics
- When the user mentions "gateway comfyui" or related topics
- When the user mentions "api gateway imagens" or related topics
- When the user mentions "queue imagens" or related topics

## Do Not Use This Skill When

- The task is unrelated to comfyui gateway
- A simpler, more specific tool can handle the request
- The user needs general-purpose assistance without domain expertise

## How It Works

A production-grade REST API gateway that transforms any ComfyUI server into a universal,
secure, and scalable service. Supports workflow templates with placeholders, job queuing
with priorities, webhook callbacks, result caching, and multiple storage backends.

## Architecture Overview

```
┌─────────────┐     ┌──────────────────────────────────┐     ┌──────────┐
│   Clients    │────▶│        ComfyUI Gateway           │────▶│ ComfyUI  │
│ (curl, n8n,  │     │                                  │     │ Server   │
│  Claude,     │     │  ┌─────────┐  ┌──────────────┐  │     │ (local/  │
│  Lovable,    │     │  │ Fastify │  │ BullMQ Queue │  │     │  remote) │
│  Supabase)   │     │  │ API     │──│ (or in-mem)  │  │     └──────────┘
│              │◀────│  └─────────┘  └──────────────┘  │
│              │     │  ┌─────────┐  ┌──────────────┐  │     ┌──────────┐
│              │     │  │ Auth +  │  │ Storage      │  │────▶│ S3/MinIO │
│              │     │  │ RateL.  │  │ (local/S3)   │  │     │(optional)│
│              │     │  └─────────┘  └──────────────┘  │     └──────────┘
└─────────────┘     └──────────────────────────────────┘
```

## Components

| Component | Purpose | File(s) |
|-----------|---------|---------|
| **API Gateway** | REST endpoints, validation, CORS | `src/api/` |
| **Worker** | Processes jobs, talks to ComfyUI | `src/worker/` |
| **ComfyUI Client** | HTTP + WebSocket to ComfyUI | `src/comfyui/` |
| **Workflow Manager** | Template storage, placeholder rendering | `src/workflows/` |
| **Storage Provider** | Local disk + S3-compatible | `src/storage/` |
| **Cache** | Hash-based deduplication | `src/cache/` |
| **Notifier** | Webhook with HMAC signing | `src/notifications/` |
| **Auth** | API key + JWT + rate limiting | `src/auth/` |
| **DB** | SQLite (better-sqlite3) or Postgres | `src/db/` |
| **CLI** | Init, add-workflow, run, worker | `src/cli/` |

## Quick Start

```bash

## 1. Install

cd comfyui-gateway
npm install

## 2. Configure

cp .env.example .env

## 3. Initialize

npx tsx src/cli/index.ts init

## 4. Add A Workflow

npx tsx src/cli/index.ts add-workflow ./workflows/sdxl_realism_v1.json \
  --id sdxl_realism_v1 --schema ./workflows/sdxl_realism_v1.schema.json

## 5. Start (Api + Worker In One Process)

npm run dev

## Or Separately:

npm run start:api   # API only
npm run start:worker # Worker only
```

## Environment Variables

All configuration is via `.env` — nothing is hardcoded:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `3000` | API server port |
| `HOST` | `0.0.0.0` | API bind address |
| `COMFYUI_URL` | `http://127.0.0.1:8188` | ComfyUI server URL |
| `COMFYUI_TIMEOUT_MS` | `300000` | Max wait for ComfyUI (5min) |
| `API_KEYS` | `""` | Comma-separated API keys (`key:role`) |
| `JWT_SECRET` | `""` | JWT signing secret (empty = JWT disabled) |
| `REDIS_URL` | `""` | Redis URL (empty = in-memory queue) |
| `DATABASE_URL` | `./data/gateway.db` | SQLite path or Postgres URL |
| `STORAGE_PROVIDER` | `local` | `local` or `s3` |
| `STORAGE_LOCAL_PATH` | `./data/outputs` | Local output directory |
| `S3_ENDPOINT` | `""` | S3/MinIO endpoint |
| `S3_BUCKET` | `""` | S3 bucket name |
| `S3_ACCESS_KEY` | `""` | S3 access key |
| `S3_SECRET_KEY` | `""` | S3 secret key |
| `S3_REGION` | `us-east-1` | S3 region |
| `WEBHOOK_SECRET` | `""` | HMAC signing secret for webhooks |
| `WEBHOOK_ALLOWED_DOMAINS` | `*` | Comma-separated allowed callback domains |
| `MAX_CONCURRENCY` | `1` | Parallel jobs per GPU |
| `MAX_IMAGE_SIZE` | `2048` | Maximum dimension (width or height) |
| `MAX_BATCH_SIZE` | `4` | Maximum batch size |
| `CACHE_ENABLED` | `true` | Enable result caching |
| `CACHE_TTL_SECONDS` | `86400` | Cache TTL (24h) |
| `RATE_LIMIT_MAX` | `100` | Requests per window |
| `RATE_LIMIT_WINDOW_MS` | `60000` | Rate limit window (1min) |
| `LOG_LEVEL` | `info` | Pino log level |
| `PRIVACY_MODE` | `false` | Redact prompts from logs |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |
| `NODE_ENV` | `development` | Environment |

## Health & Capabilities

```
GET /health
→ { ok: true, version, comfyui: { reachable, url, models? }, uptime }

GET /capabilities
→ { workflows: [...], maxSize, maxBatch, formats, storageProvider }
```

## Workflows (Crud)

```
GET    /workflows            → list all workflows
POST   /workflows            → register new workflow
GET    /workflows/:id        → workflow details + input schema
PUT    /workflows/:id        → update workflow
DELETE /workflows/:id        → remove workflow
```

## Jobs

```
POST   /jobs                 → create job (returns jobId immediately)
GET    /jobs/:jobId          → status + progress + outputs
GET    /jobs/:jobId/logs     → sanitized execution logs
POST   /jobs/:jobId/cancel   → request cancellation
GET    /jobs                 → list jobs (filters: status, workflowId, after, before, limit)
```

## Outputs

```
GET    /outputs/:jobId       → list output files + metadata
GET    /outputs/:jobId/:file → download/stream file
```

## Job Lifecycle

```
queued → running → succeeded
                 → failed
                 → canceled
```

1. Client POSTs to `/jobs` with workflowId + inputs
2. Gateway validates, checks cache, checks idempotency
3. If cache hit → returns existing outputs immediately (status: `cache_hit`)
4. Otherwise → enqueues job, returns `jobId` + `pollUrl`
5. Worker picks up job, renders workflow template, submits to ComfyUI
6. Worker polls ComfyUI for progress (or listens via WebSocket)
7. On completion → downloads outputs, stores them, updates DB
8. If callbackUrl → sends signed webhook POST
9. Client polls `/jobs/:jobId` or receives webhook

## Workflow Templates

Workflows are ComfyUI JSON with `{{placeholder}}` tokens. The gateway resolves
these at runtime using the job's `inputs` and `params`:

```json
{
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "seed": "{{seed}}",
      "steps": "{{steps}}",
      "cfg": "{{cfg}}",
      "sampler_name": "{{sampler}}",
      "scheduler": "normal",
      "denoise": 1,
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "{{prompt}}",
      "clip": ["4", 1]
    }
  }
}
```

Each workflow has an `inputSchema` (Zod) that validates what the client sends.

## Security Model

- **API Keys**: `X-API-Key` header; keys configured via `API_KEYS` env var as `key1:admin,key2:user`
- **JWT**: Optional; when `JWT_SECRET` is set, accepts `Authorization: Bearer <token>`
- **Roles**: `admin` (full CRUD on workflows + jobs), `user` (create jobs, read own jobs)
- **Rate Limiting**: Per key + per IP, configurable window and max
- **Webhook Security**: HMAC-SHA256 signature in `X-Signature` header
- **Callback Allowlist**: Only approved domains receive webhooks
- **Privacy Mode**: When enabled, prompts are redacted from logs and DB
- **Idempotency**: `metadata.requestId` prevents duplicate processing
- **CORS**: Configurable allowed origins
- **Input Validation**: Zod schemas on every endpoint; max size/batch enforced

## Comfyui Integration

The gateway communicates with ComfyUI via its native HTTP API:

| ComfyUI Endpoint | Gateway Usage |
|------------------|---------------|
| `POST /prompt` | Submit rendered workflow |
| `GET /history/{id}` | Poll job completion |
| `GET /view?filename=...` | Download generated images |
| `GET /object_info` | Discover available nodes/models |
| `WS /ws?clientId=...` | Real-time progress (optional) |

The client auto-detects ComfyUI version and adapts:
- Tries WebSocket first for progress, falls back to polling
- Handles both `/history` response formats
- Detects OOM errors and classifies them with recommendations

## Cache Strategy

Cache key = SHA-256 of `workflowId + sorted(inputs) + sorted(params) + checkpoint`.
On cache hit, the gateway returns a "virtual" job with pre-existing outputs — no GPU
computation needed. Cache is stored alongside job data in the DB with configurable TTL.

## Error Classification

| Error Code | Meaning | Retry? |
|------------|---------|--------|
| `COMFYUI_UNREACHABLE` | Cannot connect to ComfyUI | Yes (with backoff) |
| `COMFYUI_OOM` | Out of memory on GPU | No (reduce dimensions) |
| `COMFYUI_TIMEOUT` | Execution exceeded timeout | Maybe (increase timeout) |
| `COMFYUI_NODE_ERROR` | Node execution failed | No (check workflow) |
| `VALIDATION_ERROR` | Invalid inputs | No (fix request) |
| `WORKFLOW_NOT_FOUND` | Unknown workflowId | No (register workflow) |
| `RATE_LIMITED` | Too many requests | Yes (wait) |
| `AUTH_FAILED` | Invalid/missing credentials | No (fix auth) |
| `CACHE_HIT` | (Not an error) Served from cache | N/A |

## Bundled Workflows

Three production-ready workflow templates are included:

## 1. `Sdxl_Realism_V1` — Photorealistic Generation

- Checkpoint: SDXL base
- Optimized for: Portraits, landscapes, product shots
- Default: 1024x1024, 30 steps, cfg 7.0

## 2. `Sprite_Transparent_Bg` — Game Sprites With Alpha

- Checkpoint: SD 1.5 or SDXL
- Optimized for: 2D game assets, transparent backgrounds
- Default: 512x512, 25 steps, cfg 7.5

## 3. `Icon_512` — App Icons With Optional Upscale

- Checkpoint: SDXL base
- Optimized for: Square icons, clean edges
- Default: 512x512, 20 steps, cfg 6.0, optional 2x upscale

## Observability

- **Structured Logs**: Pino JSON logs with `correlationId` on every request
- **Metrics**: Jobs queued/running/succeeded/failed, avg processing time, cache hit rate
- **Audit Log**: Admin actions (workflow CRUD, key management) logged with timestamp + actor

## Cli Reference

```bash
npx tsx src/cli/index.ts init                    # Create dirs, .env.example
npx tsx src/cli/index.ts add-workflow <file>      # Register workflow template
  --id <id> --name <name> --schema <schema.json>
npx tsx src/cli/index.ts list-workflows           # Show registered workflows
npx tsx src/cli/index.ts run                      # Start API server
npx tsx src/cli/index.ts worker                   # Start job worker
npx tsx src/cli/index.ts health                   # Check ComfyUI connectivity
```

## Troubleshooting

Read `references/troubleshooting.md` for detailed guidance on:
- ComfyUI not reachable (firewall, wrong port, Docker networking)
- OOM errors (reduce resolution, batch, or steps)
- Slow generation (GPU utilization, queue depth, model loading)
- Webhook failures (DNS, SSL, timeout, domain allowlist)
- Redis connection issues (fallback to in-memory)
- Storage permission errors (local path, S3 credentials)

## Integration Examples

Read `references/integration.md` for ready-to-use examples with:
- curl commands for every endpoint
- n8n webhook workflow
- Supabase Edge Function caller
- Claude Code / Claude.ai integration
- Python requests client
- JavaScript fetch client

## File Structure

```
comfyui-gateway/
├── SKILL.md
├── package.json
├── tsconfig.json
├── .env.example
├── src/
│   ├── api/
│   │   ├── server.ts          # Fastify setup + plugins
│   │   ├── routes/
│   │   │   ├── health.ts      # GET /health, /capabilities
│   │   │   ├── workflows.ts   # CRUD /workflows
│   │   │   ├── jobs.ts        # CRUD /jobs
│   │   │   └── outputs.ts     # GET /outputs
│   │   ├── middleware/
│   │   │   └── error-handler.ts
│   │   └── plugins/
│   │       ├── auth.ts        # API key + JWT
│   │       ├── rate-limit.ts
│   │       └── cors.ts
│   ├── worker/
│   │   └── processor.ts       # Job processor
│   ├── comfyui/
│   │   └── client.ts          # ComfyUI HTTP + WS client
│   ├── storage/
│   │   ├── index.ts           # Provider factory
│   │   ├── local.ts           # Local filesystem
│   │   └── s3.ts              # S3-compatible
│   ├── workflows/
│   │   └── manager.ts         # Template CRUD + rendering
│   ├── cache/
│   │   └── index.ts           # Hash-based cache
│   ├── notifications/
│   │   └── webhook.ts         # HMAC-signed callbacks
│   ├── auth/
│   │   └── index.ts           # Key/JWT validation + roles
│   ├── db/
│   │   ├── index.ts           # DB factory (SQLite/Postgres)
│   │   └── migrations.ts      # Schema creation
│   ├── cli/
│   │   └── index.ts           # CLI commands
│   ├── utils/
│   │   ├── config.ts          # Env loading + validation
│   │   ├── errors.ts          # Error classes
│   │   ├── logger.ts          # Pino setup
│   │   └── hash.ts            # SHA-256 hashing
│   └── index.ts               # Main entrypoint
├── config/
│   └── workflows/             # Bundled workflow templates
│       ├── sdxl_realism_v1.json
│       ├── sdxl_realism_v1.schema.json
│       ├── sprite_transparent_bg.json
│       ├── sprite_transparent_bg.schema.json
│       ├── icon_512.json
│       └── icon_512.schema.json
├── data/
│   ├── outputs/               # Generated images
│   ├── workflows/             # User-added wor

## Best Practices

- Provide clear, specific context about your project and requirements
- Review all suggestions before applying them to production code
- Combine with other complementary skills for comprehensive analysis

## Common Pitfalls

- Using this skill for tasks outside its domain expertise
- Applying recommendations without understanding your specific context
- Not providing enough project context for accurate analysis

## Related Skills

- `ai-studio-image` - Complementary skill for enhanced analysis
- `image-studio` - Complementary skill for enhanced analysis
- `stability-ai` - Complementary skill for enhanced analysis

---

## Reference: Integration

# ComfyUI Gateway -- Integration Guide

Complete integration reference with ready-to-use code examples for every endpoint
and common platforms. All examples assume the gateway is running at
`http://localhost:3000` with API key authentication enabled.

---

## Table of Contents

1. [curl Examples (Every Endpoint)](#1-curl-examples)
2. [n8n Webhook Workflow](#2-n8n-webhook-workflow)
3. [Supabase Edge Function](#3-supabase-edge-function)
4. [Claude Code Integration](#4-claude-code-integration)
5. [Python Requests Client](#5-python-requests-client)
6. [JavaScript/TypeScript Fetch Client](#6-javascripttypescript-fetch-client)
7. [Webhook Receiver (Express.js + HMAC)](#7-webhook-receiver-expressjs--hmac)
8. [Docker Compose](#8-docker-compose)
9. [Environment Configuration Examples](#9-environment-configuration-examples)

---

## 1. curl Examples

### Health Check

```bash
curl -s http://localhost:3000/health | jq .
```

Response:

```json
{
  "ok": true,
  "version": null,
  "comfyui": {
    "reachable": true,
    "url": "http://127.0.0.1:8188"
  },
  "uptime": 1234.567
}
```

### Capabilities

```bash
curl -s http://localhost:3000/capabilities \
  -H "X-API-Key: your-api-key" | jq .
```

Response:

```json
{
  "workflows": [
    { "id": "sdxl_realism_v1", "name": "SDXL Realism v1", "description": "..." },
    { "id": "sprite_transparent_bg", "name": "Sprite Transparent BG", "description": "..." }
  ],
  "maxSize": 2048,
  "maxBatch": 4,
  "formats": ["png", "jpg", "webp"],
  "storageProvider": "local"
}
```

### List Workflows

```bash
curl -s http://localhost:3000/workflows \
  -H "X-API-Key: your-api-key" | jq .
```

### Get Workflow Details

```bash
curl -s http://localhost:3000/workflows/sdxl_realism_v1 \
  -H "X-API-Key: your-api-key" | jq .
```

### Create Workflow (Admin)

```bash
curl -X POST http://localhost:3000/workflows \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-admin-key" \
  -d '{
    "id": "my_custom_workflow",
    "name": "My Custom Workflow",
    "description": "A custom txt2img workflow",
    "workflowJson": {
      "3": {
        "class_type": "KSampler",
        "inputs": {
          "seed": "{{seed}}",
          "steps": "{{steps}}",
          "cfg": "{{cfg}}",
          "sampler_name": "euler",
          "scheduler": "normal",
          "denoise": 1,
          "model": ["4", 0],
          "positive": ["6", 0],
          "negative": ["7", 0],
          "latent_image": ["5", 0]
        }
      },
      "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
          "text": "{{prompt}}",
          "clip": ["4", 1]
        }
      }
    },
    "inputSchema": {
      "type": "object",
      "fields": {
        "prompt": { "type": "string", "required": true, "description": "Text prompt" },
        "seed": { "type": "number", "default": -1, "description": "Random seed" },
        "steps": { "type": "number", "default": 30, "min": 1, "max": 100 },
        "cfg": { "type": "number", "default": 7.0, "min": 1, "max": 20 }
      }
    },
    "defaultParams": {
      "seed": -1,
      "steps": 30,
      "cfg": 7.0
    }
  }' | jq .
```

### Update Workflow (Admin)

```bash
curl -X PUT http://localhost:3000/workflows/my_custom_workflow \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-admin-key" \
  -d '{
    "name": "My Custom Workflow v2",
    "description": "Updated description"
  }' | jq .
```

### Delete Workflow (Admin)

```bash
curl -X DELETE http://localhost:3000/workflows/my_custom_workflow \
  -H "X-API-Key: your-admin-key" -v
# Returns HTTP 204 No Content
```

### Create Job

```bash
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": {
      "prompt": "a photorealistic mountain landscape at sunset, 8k, detailed",
      "negative_prompt": "blurry, low quality",
      "width": 1024,
      "height": 1024,
      "steps": 30,
      "cfg": 7.0,
      "seed": 42
    },
    "callbackUrl": "https://your-app.com/webhook/comfyui",
    "metadata": {
      "requestId": "req_abc123",
      "userId": "user_456"
    }
  }' | jq .
```

Response (HTTP 202):

```json
{
  "jobId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "queued",
  "etaSeconds": 0,
  "pollUrl": "/jobs/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Poll Job Status

```bash
curl -s http://localhost:3000/jobs/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  -H "X-API-Key: your-api-key" | jq .
```

Response (completed):

```json
{
  "jobId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "succeeded",
  "workflowId": "sdxl_realism_v1",
  "progress": 100,
  "outputs": [
    {
      "filename": "ComfyUI_00001_.png",
      "storagePath": "/data/outputs/a1b2.../uuid.png",
      "url": "/outputs/a1b2.../uuid.png",
      "size": 1542890,
      "sha256": "abc123..."
    }
  ],
  "error": null,
  "timing": {
    "createdAt": "2025-01-15T10:30:00.000Z",
    "startedAt": "2025-01-15T10:30:01.000Z",
    "completedAt": "2025-01-15T10:30:15.000Z",
    "executionTimeMs": 14000
  },
  "metadata": { "requestId": "req_abc123", "userId": "user_456" }
}
```

### List Jobs (with Filters)

```bash
# All jobs
curl -s "http://localhost:3000/jobs" \
  -H "X-API-Key: your-api-key" | jq .

# Filter by status
curl -s "http://localhost:3000/jobs?status=succeeded&limit=10" \
  -H "X-API-Key: your-api-key" | jq .

# Filter by workflow and date range
curl -s "http://localhost:3000/jobs?workflowId=sdxl_realism_v1&after=2025-01-01T00:00:00Z&limit=50" \
  -H "X-API-Key: your-api-key" | jq .
```

### Get Job Logs

```bash
curl -s http://localhost:3000/jobs/a1b2c3d4-e5f6-7890-abcd-ef1234567890/logs \
  -H "X-API-Key: your-api-key" | jq .
```

### Cancel Job

```bash
curl -X POST http://localhost:3000/jobs/a1b2c3d4-e5f6-7890-abcd-ef1234567890/cancel \
  -H "X-API-Key: your-api-key" | jq .
```

Response:

```json
{
  "jobId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "cancelled",
  "message": "Cancellation requested"
}
```

### List Outputs

```bash
curl -s http://localhost:3000/outputs/a1b2c3d4-e5f6-7890-abcd-ef1234567890 \
  -H "X-API-Key: your-api-key" | jq .
```

### Download Output (Binary)

```bash
# Stream to file
curl -s http://localhost:3000/outputs/a1b2c3d4-e5f6-7890-abcd-ef1234567890/uuid.png \
  -H "X-API-Key: your-api-key" \
  -o output.png

# View content type and size
curl -sI http://localhost:3000/outputs/a1b2c3d4-e5f6-7890-abcd-ef1234567890/uuid.png \
  -H "X-API-Key: your-api-key"
```

### Download Output (Base64)

```bash
curl -s "http://localhost:3000/outputs/a1b2c3d4-e5f6-7890-abcd-ef1234567890/uuid.png?format=base64" \
  -H "X-API-Key: your-api-key" | jq .
```

Response:

```json
{
  "filename": "uuid.png",
  "contentType": "image/png",
  "size": 1542890,
  "data": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

---

## 2. n8n Webhook Workflow

Step-by-step setup for using n8n to trigger image generation and receive results
via webhook.

### Step 1: Create a Webhook Trigger Node

1. Add a **Webhook** node in n8n.
2. Set HTTP Method to `POST`.
3. Set Path to `/comfyui-result`.
4. Under Authentication, select **Header Auth** and configure:
   - Name: `X-Signature`
   - Value: leave blank (we will verify in code).
5. Copy the **Production URL** (e.g., `https://n8n.your-domain.com/webhook/comfyui-result`).

### Step 2: Create an HTTP Request Node to Submit a Job

1. Add an **HTTP Request** node.
2. Configure:
   - Method: `POST`
   - URL: `http://your-gateway:3000/jobs`
   - Authentication: select **Generic Credential Type** > **Header Auth**
     - Name: `X-API-Key`
     - Value: `your-api-key`
   - Body Content Type: JSON
   - Body:

```json
{
  "workflowId": "sdxl_realism_v1",
  "inputs": {
    "prompt": "{{ $json.prompt }}",
    "width": 1024,
    "height": 1024,
    "steps": 30
  },
  "callbackUrl": "https://n8n.your-domain.com/webhook/comfyui-result",
  "metadata": {
    "requestId": "{{ $json.requestId }}"
  }
}
```

### Step 3: Process the Webhook Callback

Back in the Webhook node, add downstream nodes:

1. **IF** node: Check `{{ $json.status }}` equals `succeeded`.
2. On true branch, **HTTP Request** node to download the image:
   - URL: `http://your-gateway:3000{{ $json.result.outputs[0].url }}`
   - Headers: `X-API-Key: your-api-key`
   - Response Format: File
3. Continue with your pipeline (save to disk, upload to S3, send to Slack, etc.).

### Step 4: HMAC Verification (Optional)

Add a **Code** node before the IF to verify the webhook signature:

```javascript
const crypto = require('crypto');
const secret = 'your-webhook-secret';
const body = JSON.stringify($json);
const expected = crypto
  .createHmac('sha256', secret)
  .update(body, 'utf8')
  .digest('hex');
const received = $headers['x-signature']?.replace('sha256=', '');

if (received !== expected) {
  throw new Error('Invalid webhook signature');
}

return $json;
```

### Step 5: Add WEBHOOK_ALLOWED_DOMAINS

In your gateway `.env`:

```
WEBHOOK_ALLOWED_DOMAINS=n8n.your-domain.com
WEBHOOK_SECRET=your-webhook-secret
```

---

## 3. Supabase Edge Function

A Supabase Edge Function that submits a job to the gateway and returns the job
ID for client-side polling.

### File: `supabase/functions/generate-image/index.ts`

```typescript
import { serve } from "https://deno.land/std@0.177.0/http/server.ts";

const GATEWAY_URL = Deno.env.get("COMFYUI_GATEWAY_URL") ?? "http://localhost:3000";
const GATEWAY_KEY = Deno.env.get("COMFYUI_GATEWAY_KEY") ?? "";

interface GenerateRequest {
  prompt: string;
  negative_prompt?: string;
  width?: number;
  height?: number;
  steps?: number;
  workflow_id?: string;
  callback_url?: string;
}

serve(async (req: Request) => {
  // CORS preflight
  if (req.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" },
    });
  }

  try {
    const body: GenerateRequest = await req.json();

    if (!body.prompt || body.prompt.trim().length === 0) {
      return new Response(JSON.stringify({ error: "prompt is required" }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Submit job to ComfyUI Gateway
    const jobResponse = await fetch(`${GATEWAY_URL}/jobs`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": GATEWAY_KEY,
      },
      body: JSON.stringify({
        workflowId: body.workflow_id ?? "sdxl_realism_v1",
        inputs: {
          prompt: body.prompt,
          negative_prompt: body.negative_prompt ?? "",
          width: body.width ?? 1024,
          height: body.height ?? 1024,
          steps: body.steps ?? 30,
        },
        callbackUrl: body.callback_url,
        metadata: {
          requestId: crypto.randomUUID(),
          source: "supabase-edge-function",
        },
      }),
    });

    if (!jobResponse.ok) {
      const errorData = await jobResponse.json();
      return new Response(JSON.stringify(errorData), {
        status: jobResponse.status,
        headers: { "Content-Type": "application/json" },
      });
    }

    const jobData = await jobResponse.json();

    return new Response(
      JSON.stringify({
        job_id: jobData.jobId,
        status: jobData.status,
        poll_url: `${GATEWAY_URL}${jobData.pollUrl}`,
      }),
      {
        status: 202,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      },
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ error: "Internal error", message: String(err) }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      },
    );
  }
});
```

### Deploy

```bash
# Set secrets in Supabase
supabase secrets set COMFYUI_GATEWAY_URL=https://your-gateway.com
supabase secrets set COMFYUI_GATEWAY_KEY=your-api-key

# Deploy the function
supabase functions deploy generate-image

# Test
curl -X POST https://your-project.supabase.co/functions/v1/generate-image \
  -H "Authorization: Bearer YOUR_SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a photorealistic cat"}'
```

---

## 4. Claude Code Integration

How to use the ComfyUI Gateway from within a Claude Code session or any
environment where Claude has access to shell tools.

### Generating an Image from Claude Code

When Claude Code has access to `bash` or `curl`, you can generate images directly:

```bash
# 1. Submit a generation job
JOB_RESPONSE=$(curl -s -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": {
      "prompt": "a professional headshot photo, studio lighting, neutral background",
      "width": 1024,
      "height": 1024,
      "steps": 30
    },
    "metadata": { "requestId": "claude-session-001" }
  }')

JOB_ID=$(echo "$JOB_RESPONSE" | jq -r '.jobId')
echo "Job submitted: $JOB_ID"

# 2. Poll until complete (simple loop)
while true; do
  STATUS=$(curl -s "http://localhost:3000/jobs/$JOB_ID" \
    -H "X-API-Key: your-api-key" | jq -r '.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "succeeded" ] || [ "$STATUS" = "failed" ] || [ "$STATUS" = "cancelled" ]; then
    break
  fi
  sleep 3
done

# 3. Get the output URL
OUTPUT_URL=$(curl -s "http://localhost:3000/jobs/$JOB_ID" \
  -H "X-API-Key: your-api-key" | jq -r '.outputs[0].url')
echo "Output: http://localhost:3000$OUTPUT_URL"

# 4. Download the image
curl -s "http://localhost:3000$OUTPUT_URL" \
  -H "X-API-Key: your-api-key" -o generated_image.png
```

### Using Base64 Output in Claude Code

If you need the image as base64 (for inline display or further processing):

```bash
# Get base64 encoded output
B64_DATA=$(curl -s "http://localhost:3000${OUTPUT_URL}?format=base64" \
  -H "X-API-Key: your-api-key" | jq -r '.data')

# Save the base64 to a file (can be read by Claude's image viewer)
echo "$B64_DATA" | base64 -d > generated_image.png
```

### Helper Script for Repeated Use

Save as `generate.sh` in your project:

```bash
#!/usr/bin/env bash
set -euo pipefail

GATEWAY_URL="${COMFYUI_GATEWAY_URL:-http://localhost:3000}"
API_KEY="${COMFYUI_API_KEY:-}"
WORKFLOW="${1:-sdxl_realism_v1}"
PROMPT="${2:-a test image}"
OUTPUT="${3:-output.png}"

# Submit
JOB=$(curl -sf -X POST "$GATEWAY_URL/jobs" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d "{
    \"workflowId\": \"$WORKFLOW\",
    \"inputs\": { \"prompt\": \"$PROMPT\", \"width\": 1024, \"height\": 1024 }
  }")

JOB_ID=$(echo "$JOB" | jq -r '.jobId')
echo "Job: $JOB_ID"

# Poll
for i in $(seq 1 120); do
  RESULT=$(curl -sf "$GATEWAY_URL/jobs/$JOB_ID" -H "X-API-Key: $API_KEY")
  STATUS=$(echo "$RESULT" | jq -r '.status')
  if [ "$STATUS" = "succeeded" ]; then
    URL=$(echo "$RESULT" | jq -r '.outputs[0].url')
    curl -sf "$GATEWAY_URL$URL" -H "X-API-Key: $API_KEY" -o "$OUTPUT"
    echo "Saved to $OUTPUT"
    exit 0
  elif [ "$STATUS" = "failed" ]; then
    echo "FAILED: $(echo "$RESULT" | jq '.error')"
    exit 1
  fi
  sleep 2
done

echo "TIMEOUT"
exit 1
```

Usage:

```bash
chmod +x generate.sh
export COMFYUI_API_KEY=your-api-key
./generate.sh sdxl_realism_v1 "a sunset over the ocean" sunset.png
```

---

## 5. Python Requests Client

Full-featured Python client with job submission, polling, and download.

### File: `comfyui_client.py`

```python
"""
ComfyUI Gateway Python Client

Usage:
    from comfyui_client import ComfyUIGateway

    gw = ComfyUIGateway("http://localhost:3000", api_key="your-key")
    result = gw.generate("sdxl_realism_v1", prompt="a mountain landscape")
    gw.download(result["outputs"][0]["url"], "output.png")
"""

import time
import uuid
import hashlib
import hmac
import requests
from typing import Any, Optional


class ComfyUIGatewayError(Exception):
    """Base exception for gateway errors."""

    def __init__(self, message: str, status_code: int = 0, details: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details


class ComfyUIGateway:
    """Client for the ComfyUI Gateway REST API."""

    def __init__(self, base_url: str, api_key: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        if api_key:
            self.session.headers["X-API-Key"] = api_key

    # ── Health & Capabilities ──────────────────────────────────────────────

    def health(self) -> dict:
        """Check gateway and ComfyUI health."""
        resp = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def capabilities(self) -> dict:
        """Get available workflows and server capabilities."""
        resp = self.session.get(
            f"{self.base_url}/capabilities", timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # ── Workflows ──────────────────────────────────────────────────────────

    def list_workflows(self) -> list[dict]:
        """List all registered workflows."""
        resp = self.session.get(
            f"{self.base_url}/workflows", timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()["workflows"]

    def get_workflow(self, workflow_id: str) -> dict:
        """Get details of a specific workflow."""
        resp = self.session.get(
            f"{self.base_url}/workflows/{workflow_id}", timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()["workflow"]

    def create_workflow(
        self,
        workflow_id: str,
        name: str,
        workflow_json: dict,
        input_schema: Optional[dict] = None,
        description: str = "",
        default_params: Optional[dict] = None,
    ) -> dict:
        """Register a new workflow (admin only)."""
        body: dict[str, Any] = {
            "id": workflow_id,
            "name": name,
            "workflowJson": workflow_json,
        }
        if description:
            body["description"] = description
        if input_schema:
            body["inputSchema"] = input_schema
        if default_params:
            body["defaultParams"] = default_params

        resp = self.session.post(
            f"{self.base_url}/workflows",
            json=body,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()["workflow"]

    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow (admin only). Returns True on success."""
        resp = self.session.delete(
            f"{self.base_url}/workflows/{workflow_id}", timeout=self.timeout
        )
        return resp.status_code == 204

    # ── Jobs ───────────────────────────────────────────────────────────────

    def submit_job(
        self,
        workflow_id: str,
        inputs: dict,
        params: Optional[dict] = None,
        callback_url: Optional[str] = None,
        request_id: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Submit a new generation job. Returns immediately with jobId."""
        body: dict[str, Any] = {
            "workflowId": workflow_id,
            "inputs": inputs,
        }
        if params:
            body["params"] = params
        if callback_url:
            body["callbackUrl"] = callback_url

        meta = metadata or {}
        if request_id:
            meta["requestId"] = request_id
        if meta:
            body["metadata"] = meta

        resp = self.session.post(
            f"{self.base_url}/jobs", json=body, timeout=self.timeout
        )

        if not resp.ok:
            data = resp.json()
            raise ComfyUIGatewayError(
                data.get("message", "Job submission failed"),
                status_code=resp.status_code,
                details=data,
            )

        return resp.json()

    def get_job(self, job_id: str) -> dict:
        """Get the status and details of a job."""
        resp = self.session.get(
            f"{self.base_url}/jobs/{job_id}", timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def list_jobs(
        self,
        status: Optional[str] = None,
        workflow_id: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        """List jobs with optional filters."""
        params: dict[str, Any] = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        if workflow_id:
            params["workflowId"] = workflow_id

        resp = self.session.get(
            f"{self.base_url}/jobs", params=params, timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def cancel_job(self, job_id: str) -> dict:
        """Cancel a queued or running job."""
        resp = self.session.post(
            f"{self.base_url}/jobs/{job_id}/cancel", timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def get_job_logs(self, job_id: str) -> dict:
        """Get processing logs for a job."""
        resp = self.session.get(
            f"{self.base_url}/jobs/{job_id}/logs", timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # ── Outputs ────────────────────────────────────────────────────────────

    def list_outputs(self, job_id: str) -> list[dict]:
        """List output files for a completed job."""
        resp = self.session.get(
            f"{self.base_url}/outputs/{job_id}", timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()["files"]

    def get_output_base64(self, job_id: str, filename: str) -> dict:
        """Get a single output file as base64."""
        resp = self.session.get(
            f"{self.base_url}/outputs/{job_id}/{filename}",
            params={"format": "base64"},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def download(self, url_path: str, output_path: str) -> str:
        """Download an output file to a local path. Returns the path."""
        full_url = f"{self.base_url}{url_path}" if url_path.startswith("/") else url_path
        resp = self.session.get(full_url, timeout=120)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(resp.content)
        return output_path

    # ── High-Level: Generate & Wait ────────────────────────────────────────

    def generate(
        self,
        workflow_id: str,
        poll_interval: float = 2.0,
        max_wait: float = 300.0,
        **inputs: Any,
    ) -> dict:
        """
        Submit a job, poll until complete, and return the full result.

        Usage:
            result = gw.generate("sdxl_realism_v1", prompt="a sunset", steps=30)
            print(result["outputs"])
        """
        job = self.submit_job(
            workflow_id=workflow_id,
            inputs=inputs,
            request_id=str(uuid.uuid4()),
        )
        job_id = job["jobId"]

        start = time.time()
        while time.time() - start < max_wait:
            result = self.get_job(job_id)
            status = result["status"]

            if status == "succeeded":
                return result
            elif status in ("failed", "cancelled"):
                raise ComfyUIGatewayError(
                    f"Job {status}: {result.get('error')}",
                    details=result,
                )

            time.sleep(poll_interval)

        raise ComfyUIGatewayError(f"Job {job_id} timed out after {max_wait}s")


# ── Usage Example ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    gw = ComfyUIGateway("http://localhost:3000", api_key="your-api-key")

    # Check health
    print("Health:", gw.health())

    # Generate an image (blocking)
    result = gw.generate(
        "sdxl_realism_v1",
        prompt="a photorealistic golden retriever in a park",
        width=1024,
        height=1024,
        steps=30,
    )

    # Download the first output
    if result["outputs"]:
        output_url = result["outputs"][0]["url"]
        gw.download(output_url, "generated.png")
        print(f"Image saved to generated.png ({result['outputs'][0]['size']} bytes)")
    else:
        print("No outputs produced")
```

---

## 6. JavaScript/TypeScript Fetch Client

A full client using native `fetch` (Node.js 18+, Deno, Bun, or browsers).

### File: `comfyui-client.ts`

```typescript
/**
 * ComfyUI Gateway TypeScript Client
 *
 * Works with Node.js 18+ (native fetch), Deno, Bun, and browsers.
 */

export interface GatewayConfig {
  baseUrl: string;
  apiKey?: string;
  timeout?: number;
}

export interface JobSubmission {
  workflowId: string;
  inputs: Record<string, unknown>;
  params?: Record<string, unknown>;
  callbackUrl?: string;
  metadata?: Record<string, unknown>;
}

export interface JobResult {
  jobId: string;
  status: "queued" | "running" | "succeeded" | "failed" | "cancelled";
  workflowId: string;
  progress: number | null;
  outputs: Array<{
    filename: string;
    storagePath: string;
    url: string;
    size: number;
    sha256: string;
  }> | null;
  error: unknown;
  timing: {
    createdAt: string;
    startedAt: string | null;
    completedAt: string | null;
    executionTimeMs: number | null;
  };
  metadata: Record<string, unknown> | null;
}

export class ComfyUIGateway {
  private baseUrl: string;
  private headers: Record<string, string>;
  private timeout: number;

  constructor(config: GatewayConfig) {
    this.baseUrl = config.baseUrl.replace(/\/+$/, "");
    this.timeout = config.timeout ?? 30_000;
    this.headers = {
      "Content-Type": "application/json",
    };
    if (config.apiKey) {
      this.headers["X-API-Key"] = config.apiKey;
    }
  }

  // ── Internal fetch wrapper ──────────────────────────────────────────────

  private async request<T>(
    method: string,
    path: string,
    body?: unknown,
    options: { timeout?: number; params?: Record<string, string> } = {},
  ): Promise<T> {
    let url = `${this.baseUrl}${path}`;

    if (options.params) {
      const searchParams = new URLSearchParams(options.params);
      url += `?${searchParams.toString()}`;
    }

    const controller = new AbortController();
    const timer = setTimeout(
      () => controller.abort(),
      options.timeout ?? this.timeout,
    );

    try {
      const resp = await fetch(url, {
        method,
        headers: this.headers,
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });

      if (!resp.ok) {
        const errorBody = await resp.json().catch(() => ({}));
        throw new Error(
          `Gateway error ${resp.status}: ${(errorBody as { message?: string }).message ?? resp.statusText}`,
        );
      }

      // 204 No Content
      if (resp.status === 204) {
        return undefined as T;
      }

      return (await resp.json()) as T;
    } finally {
      clearTimeout(timer);
    }
  }

  // ── Health ──────────────────────────────────────────────────────────────

  async health(): Promise<{
    ok: boolean;
    version: string | null;
    comfyui: { reachable: boolean; url: string };
    uptime: number;
  }> {
    return this.request("GET", "/health");
  }

  async capabilities(): Promise<{
    workflows: Array<{ id: string; name: string }>;
    maxSize: number;
    maxBatch: number;
    formats: string[];
    storageProvider: string;
  }> {
    return this.request("GET", "/capabilities");
  }

  // ── Workflows ───────────────────────────────────────────────────────────

  async listWorkflows(): Promise<Array<{ id: string; name: string }>> {
    const data = await this.request<{ workflows: Array<{ id: string; name: string }> }>(
      "GET",
      "/workflows",
    );
    return data.workflows;
  }

  async getWorkflow(id: string): Promise<Record<string, unknown>> {
    const data = await this.request<{ workflow: Record<string, unknown> }>(
      "GET",
      `/workflows/${encodeURIComponent(id)}`,
    );
    return data.workflow;
  }

  // ── Jobs ────────────────────────────────────────────────────────────────

  async submitJob(
    submission: JobSubmission,
  ): Promise<{ jobId: string; status: string; pollUrl: string }> {
    return this.request("POST", "/jobs", submission);
  }

  async getJob(jobId: string): Promise<JobResult> {
    return this.request("GET", `/jobs/${encodeURIComponent(jobId)}`);
  }

  async cancelJob(
    jobId: string,
  ): Promise<{ jobId: string; status: string; message: string }> {
    return this.request("POST", `/jobs/${encodeURIComponent(jobId)}/cancel`);
  }

  async listJobs(filters?: {
    status?: string;
    workflowId?: string;
    limit?: number;
    offset?: number;
  }): Promise<{ jobs: JobResult[]; count: number }> {
    const params: Record<string, string> = {};
    if (filters?.status) params.status = filters.status;
    if (filters?.workflowId) params.workflowId = filters.workflowId;
    if (filters?.limit) params.limit = String(filters.limit);
    if (filters?.offset) params.offset = String(filters.offset);

    return this.request("GET", "/jobs", undefined, { params });
  }

  // ── Outputs ─────────────────────────────────────────────────────────────

  async listOutputs(
    jobId: string,
  ): Promise<Array<{ filename: string; size: number; sha256: string; url: string }>> {
    const data = await this.request<{
      files: Array<{ filename: string; size: number; sha256: string; url: string }>;
    }>("GET", `/outputs/${encodeURIComponent(jobId)}`);
    return data.files;
  }

  async getOutputBase64(
    jobId: string,
    filename: string,
  ): Promise<{ filename: string; contentType: string; size: number; data: string }> {
    return this.request(
      "GET",
      `/outputs/${encodeURIComponent(jobId)}/${encodeURIComponent(filename)}`,
      undefined,
      { params: { format: "base64" } },
    );
  }

  async downloadOutput(jobId: string, filename: string): Promise<Blob> {
    const url = `${this.baseUrl}/outputs/${encodeURIComponent(jobId)}/${encodeURIComponent(filename)}`;
    const resp = await fetch(url, { headers: this.headers });
    if (!resp.ok) throw new Error(`Download failed: ${resp.status}`);
    return resp.blob();
  }

  // ── High-Level: Generate & Wait ─────────────────────────────────────────

  async generate(
    workflowId: string,
    inputs: Record<string, unknown>,
    options: {
      pollIntervalMs?: number;
      maxWaitMs?: number;
      onProgress?: (progress: number | null, status: string) => void;
    } = {},
  ): Promise<JobResult> {
    const { pollIntervalMs = 2000, maxWaitMs = 300_000, onProgress } = options;

    const job = await this.submitJob({
      workflowId,
      inputs,
      metadata: { requestId: crypto.randomUUID() },
    });

    const start = Date.now();

    while (Date.now() - start < maxWaitMs) {
      const result = await this.getJob(job.jobId);

      onProgress?.(result.progress, result.status);

      if (result.status === "succeeded") {
        return result;
      }

      if (result.status === "failed" || result.status === "cancelled") {
        throw new Error(
          `Job ${result.status}: ${JSON.stringify(result.error)}`,
        );
      }

      await new Promise((r) => setTimeout(r, pollIntervalMs));
    }

    throw new Error(`Job ${job.jobId} timed out after ${maxWaitMs}ms`);
  }
}

// ── Usage Example ─────────────────────────────────────────────────────────

async function main() {
  const gw = new ComfyUIGateway({
    baseUrl: "http://localhost:3000",
    apiKey: "your-api-key",
  });

  // Health check
  const health = await gw.health();
  console.log("ComfyUI reachable:", health.comfyui.reachable);

  // Generate (blocking)
  const result = await gw.generate(
    "sdxl_realism_v1",
    {
      prompt: "a photorealistic golden retriever in a park",
      width: 1024,
      height: 1024,
      steps: 30,
    },
    {
      onProgress: (progress, status) =>
        console.log(`Status: ${status}, Progress: ${progress ?? "N/A"}%`),
    },
  );

  console.log("Outputs:", result.outputs);

  // Download first output as base64
  if (result.outputs && result.outputs.length > 0) {
    const firstOutput = result.outputs[0];
    const b64 = await gw.getOutputBase64(result.jobId, firstOutput.filename);
    console.log(`Image: ${b64.contentType}, ${b64.size} bytes`);
  }
}

// Uncomment to run:
// main().catch(console.error);
```

---

## 7. Webhook Receiver (Express.js + HMAC)

A standalone Express.js server that receives webhook callbacks from the gateway,
verifies HMAC-SHA256 signatures, and processes results.

### File: `webhook-receiver.js`

```javascript
const express = require("express");
const crypto = require("crypto");

const app = express();
const PORT = process.env.WEBHOOK_PORT || 4000;
const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET || "your-webhook-secret";

// IMPORTANT: Must use raw body for HMAC computation
app.use(
  express.json({
    verify: (req, _res, buf) => {
      // Store raw body buffer for signature verification
      req.rawBody = buf;
    },
  }),
);

/**
 * Verify HMAC-SHA256 signature from the gateway.
 *
 * The gateway sends: X-Signature: sha256=<hex_digest>
 * Computed as: HMAC-SHA256(secret, raw_json_body)
 */
function verifySignature(req) {
  const signatureHeader = req.headers["x-signature"];
  if (!signatureHeader) {
    return { valid: false, reason: "Missing X-Signature header" };
  }

  // Extract hex digest (format: "sha256=abcdef...")
  const receivedSig = signatureHeader.replace("sha256=", "");

  // Compute expected signature using raw body bytes
  const expectedSig = crypto
    .createHmac("sha256", WEBHOOK_SECRET)
    .update(req.rawBody, "utf8")
    .digest("hex");

  // Constant-time comparison to prevent timing attacks
  const valid = crypto.timingSafeEqual(
    Buffer.from(receivedSig, "hex"),
    Buffer.from(expectedSig, "hex"),
  );

  return { valid, reason: valid ? null : "Signature mismatch" };
}

/**
 * POST /webhook/comfyui
 *
 * Receives job completion/failure callbacks from the ComfyUI Gateway.
 */
app.post("/webhook/comfyui", (req, res) => {
  // 1. Verify HMAC signature
  if (WEBHOOK_SECRET) {
    const { valid, reason } = verifySignature(req);
    if (!valid) {
      console.error("Webhook signature verification FAILED:", reason);
      return res.status(401).json({ error: "Invalid signature" });
    }
  }

  // 2. Respond immediately (gateway has a 10s timeout)
  res.status(200).json({ received: true });

  // 3. Process the payload asynchronously
  const payload = req.body;
  console.log("Webhook received:", {
    event: payload.event,
    jobId: payload.jobId,
    status: payload.status,
  });

  if (payload.status === "succeeded") {
    handleSuccess(payload);
  } else if (payload.status === "failed") {
    handleFailure(payload);
  }
});

async function handleSuccess(payload) {
  console.log(`Job ${payload.jobId} succeeded!`);
  console.log(`Outputs: ${payload.result?.outputs?.length ?? 0} files`);

  // Example: Download the first output
  if (payload.result?.outputs?.length > 0) {
    const output = payload.result.outputs[0];
    console.log(`  - ${output.filename}: ${output.size} bytes, URL: ${output.url}`);

    // You could download the file here:
    // const resp = await fetch(`http://gateway:3000${output.url}`,
    //   { headers: { "X-API-Key": "your-key" } });
    // const buffer = await resp.arrayBuffer();
    // fs.writeFileSync(`./downloads/${output.filename}`, Buffer.from(buffer));
  }
}

function handleFailure(payload) {
  console.error(`Job ${payload.jobId} FAILED:`, payload.error);
  // Implement your error handling: retry, notify, log, etc.
}

app.listen(PORT, () => {
  console.log(`Webhook receiver listening on port ${PORT}`);
  console.log(`Endpoint: POST http://localhost:${PORT}/webhook/comfyui`);
  console.log(`HMAC verification: ${WEBHOOK_SECRET ? "ENABLED" : "DISABLED"}`);
});
```

### Run

```bash
npm install express
WEBHOOK_SECRET=your-webhook-secret node webhook-receiver.js
```

---

## 8. Docker Compose

Production-ready Docker Compose configuration with the gateway, ComfyUI, Redis,
and MinIO (S3-compatible storage).

### File: `docker-compose.yml`

```yaml
version: "3.9"

services:
  # ── ComfyUI (GPU) ────────────────────────────────────────────────────────
  comfyui:
    image: ghcr.io/ai-dock/comfyui:latest
    container_name: comfyui
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    ports:
      - "8188:8188"
    volumes:
      - comfyui-data:/workspace/ComfyUI
      - ./models:/workspace/ComfyUI/models
    environment:
      - CLI_ARGS=--listen 0.0.0.0 --port 8188
    networks:
      - comfy-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8188/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # ── ComfyUI Gateway ──────────────────────────────────────────────────────
  gateway:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: comfyui-gateway
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - PORT=3000
      - HOST=0.0.0.0
      - NODE_ENV=production
      - LOG_LEVEL=info
      - PRIVACY_MODE=true

      # ComfyUI connection (use Docker service name)
      - COMFYUI_URL=http://comfyui:8188
      - COMFYUI_TIMEOUT_MS=300000

      # Authentication
      - API_KEYS=sk-admin-key:admin,sk-user-key:user
      - JWT_SECRET=change-this-to-a-random-secret

      # Redis queue
      - REDIS_URL=redis://redis:6379/0

      # Database (SQLite inside the container)
      - DATABASE_URL=./data/gateway.db

      # S3 storage (MinIO)
      - STORAGE_PROVIDER=s3
      - S3_ENDPOINT=http://minio:9000
      - S3_BUCKET=comfyui-outputs
      - S3_ACCESS_KEY=minioadmin
      - S3_SECRET_KEY=minioadmin
      - S3_REGION=us-east-1

      # Rate limiting
      - RATE_LIMIT_MAX=200
      - RATE_LIMIT_WINDOW_MS=60000

      # Job limits
      - MAX_CONCURRENCY=1
      - MAX_IMAGE_SIZE=2048
      - MAX_BATCH_SIZE=4

      # Cache
      - CACHE_ENABLED=true
      - CACHE_TTL_SECONDS=86400

      # Webhooks
      - WEBHOOK_SECRET=your-webhook-hmac-secret
      - WEBHOOK_ALLOWED_DOMAINS=*

      # CORS
      - CORS_ORIGINS=*
    volumes:
      - gateway-data:/app/data
    depends_on:
      redis:
        condition: service_healthy
      comfyui:
        condition: service_healthy
      minio:
        condition: service_healthy
    networks:
      - comfy-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 15s
      timeout: 5s
      retries: 3

  # ── Redis ────────────────────────────────────────────────────────────────
  redis:
    image: redis:7-alpine
    container_name: comfyui-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    networks:
      - comfy-net
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # ── MinIO (S3-compatible storage) ────────────────────────────────────────
  minio:
    image: minio/minio:latest
    container_name: comfyui-minio
    restart: unless-stopped
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin
    volumes:
      - minio-data:/data
    command: server /data --console-address ":9001"
    networks:
      - comfy-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 15s
      timeout: 5s
      retries: 3

  # ── MinIO Bucket Init ────────────────────────────────────────────────────
  minio-init:
    image: minio/mc:latest
    container_name: comfyui-minio-init
    depends_on:
      minio:
        condition: service_healthy
    entrypoint: >
      /bin/sh -c "
      mc alias set local http://minio:9000 minioadmin minioadmin;
      mc mb --ignore-existing local/comfyui-outputs;
      mc anonymous set download local/comfyui-outputs;
      echo 'Bucket created and configured';
      "
    networks:
      - comfy-net

volumes:
  comfyui-data:
  gateway-data:
  redis-data:
  minio-data:

networks:
  comfy-net:
    driver: bridge
```

### Gateway Dockerfile

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --include=optional
COPY tsconfig.json ./
COPY src/ ./src/
RUN npx tsc

FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev --include=optional
COPY --from=builder /app/dist/ ./dist/
COPY config/ ./config/
RUN mkdir -p data/outputs data/workflows data/cache
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Usage

```bash
# Start everything
docker compose up -d

# Watch logs
docker compose logs -f gateway

# Test health
curl http://localhost:3000/health | jq .

# Generate an image
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: sk-admin-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": { "prompt": "a sunset over the ocean" }
  }'

# Stop everything
docker compose down

# Stop and remove volumes (full reset)
docker compose down -v
```

---

## 9. Environment Configuration Examples

### Local Development (Minimal)

```bash
# .env for local development
PORT=3000
HOST=0.0.0.0
NODE_ENV=development
LOG_LEVEL=debug
COMFYUI_URL=http://127.0.0.1:8188
COMFYUI_TIMEOUT_MS=300000

# No auth in development (all requests treated as admin)
API_KEYS=
JWT_SECRET=

# In-memory queue (no Redis needed)
REDIS_URL=

# SQLite database
DATABASE_URL=./data/gateway.db

# Local file storage
STORAGE_PROVIDER=local
STORAGE_LOCAL_PATH=./data/outputs

# Cache enabled
CACHE_ENABLED=true
CACHE_TTL_SECONDS=3600

# Lenient rate limits
RATE_LIMIT_MAX=1000
RATE_LIMIT_WINDOW_MS=60000

# No webhook restrictions
WEBHOOK_SECRET=
WEBHOOK_ALLOWED_DOMAINS=*

# Allow all CORS
CORS_ORIGINS=*
```

### Production (Full Security)

```bash
# .env for production
PORT=3000
HOST=0.0.0.0
NODE_ENV=production
LOG_LEVEL=info
PRIVACY_MODE=true
COMFYUI_URL=http://comfyui-internal:8188
COMFYUI_TIMEOUT_MS=300000

# API keys with roles
API_KEYS=sk-prod-admin-a1b2c3d4:admin,sk-prod-user-e5f6g7h8:user,sk-prod-service-i9j0k1l2:user
JWT_SECRET=a-very-long-random-secret-at-least-32-chars

# Redis for durable job queue
REDIS_URL=redis://:redis-password@redis-host:6379/0

# Postgres for production database
DATABASE_URL=postgresql://gateway_user:strong_password@postgres-host:5432/comfyui_gateway?sslmode=require

# S3 storage
STORAGE_PROVIDER=s3
S3_ENDPOINT=
S3_BUCKET=my-comfyui-outputs
S3_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE
S3_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
S3_REGION=us-east-1

# Cache
CACHE_ENABLED=true
CACHE_TTL_SECONDS=86400

# Strict rate limits
RATE_LIMIT_MAX=100
RATE_LIMIT_WINDOW_MS=60000

# Concurrency
MAX_CONCURRENCY=1
MAX_IMAGE_SIZE=2048
MAX_BATCH_SIZE=4

# Webhook security
WEBHOOK_SECRET=webhook-hmac-secret-at-least-32-chars
WEBHOOK_ALLOWED_DOMAINS=api.your-app.com,n8n.your-app.com

# Restricted CORS
CORS_ORIGINS=https://your-app.com,https://admin.your-app.com
```

### Docker (Internal Network)

```bash
# .env for Docker Compose (services communicate via Docker DNS)
PORT=3000
HOST=0.0.0.0
NODE_ENV=production
LOG_LEVEL=info
PRIVACY_MODE=true

# Docker service name instead of localhost
COMFYUI_URL=http://comfyui:8188
COMFYUI_TIMEOUT_MS=300000

API_KEYS=sk-docker-admin:admin,sk-docker-user:user
JWT_SECRET=docker-jwt-secret-change-me

# Redis via Docker service name
REDIS_URL=redis://redis:6379/0

# SQLite (mounted volume)
DATABASE_URL=./data/gateway.db

# MinIO via Docker service name
STORAGE_PROVIDER=s3
S3_ENDPOINT=http://minio:9000
S3_BUCKET=comfyui-outputs
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_REGION=us-east-1

CACHE_ENABLED=true
CACHE_TTL_SECONDS=86400

RATE_LIMIT_MAX=200
RATE_LIMIT_WINDOW_MS=60000

MAX_CONCURRENCY=1
MAX_IMAGE_SIZE=2048
MAX_BATCH_SIZE=4

WEBHOOK_SECRET=docker-webhook-secret
WEBHOOK_ALLOWED_DOMAINS=*

CORS_ORIGINS=*
```

### WSL2 (Gateway in WSL, ComfyUI on Windows)

```bash
# .env for WSL2 setup
PORT=3000
HOST=0.0.0.0
NODE_ENV=development
LOG_LEVEL=debug

# Use Windows host IP from WSL2 perspective
# Get this with: cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
COMFYUI_URL=http://172.25.192.1:8188
COMFYUI_TIMEOUT_MS=300000

API_KEYS=
JWT_SECRET=

REDIS_URL=
DATABASE_URL=./data/gateway.db

STORAGE_PROVIDER=local
STORAGE_LOCAL_PATH=./data/outputs

CACHE_ENABLED=true
CACHE_TTL_SECONDS=3600

RATE_LIMIT_MAX=500
RATE_LIMIT_WINDOW_MS=60000

WEBHOOK_SECRET=
WEBHOOK_ALLOWED_DOMAINS=*
CORS_ORIGINS=*
```

### Multi-GPU (Separate Workers)

```bash
# .env.shared (common settings)
NODE_ENV=production
LOG_LEVEL=info
COMFYUI_URL=http://comfyui:8188
REDIS_URL=redis://redis:6379/0
DATABASE_URL=postgresql://user:pass@postgres:5432/gateway
STORAGE_PROVIDER=s3
S3_ENDPOINT=http://minio:9000
S3_BUCKET=outputs
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
API_KEYS=sk-admin:admin

# Worker 1 (GPU 0) -- start with: CUDA_VISIBLE_DEVICES=0 npm run start:worker
MAX_CONCURRENCY=1

# Worker 2 (GPU 1) -- start with: CUDA_VISIBLE_DEVICES=1 npm run start:worker
# Uses the same .env, same Redis queue -- BullMQ distributes jobs automatically

# API server (no GPU needed) -- start with: npm run start:api
# Serves the REST API; workers handle ComfyUI execution
```

---

## Reference: Troubleshooting

# ComfyUI Gateway -- Troubleshooting Guide

Comprehensive troubleshooting reference for diagnosing and resolving issues with the
ComfyUI Gateway. Every section follows the **Symptom -> Cause -> Solution** format
with concrete commands you can run immediately.

---

## Table of Contents

1. [ComfyUI Not Reachable](#1-comfyui-not-reachable)
2. [OOM (Out of Memory) Errors](#2-oom-out-of-memory-errors)
3. [Slow Generation](#3-slow-generation)
4. [Webhook Failures](#4-webhook-failures)
5. [Redis Connection Issues](#5-redis-connection-issues)
6. [Storage Errors](#6-storage-errors)
7. [Database Issues](#7-database-issues)
8. [Job Stuck in "running"](#8-job-stuck-in-running)
9. [Rate Limiting Issues](#9-rate-limiting-issues)
10. [Authentication Problems](#10-authentication-problems)

---

## 1. ComfyUI Not Reachable

The gateway returns `COMFYUI_UNREACHABLE` and the `/health` endpoint shows
`comfyui.reachable: false`.

### 1a. Wrong COMFYUI_URL

**Symptom**: Gateway starts fine but every job fails with `COMFYUI_UNREACHABLE`.
The health endpoint returns `{ ok: false, comfyui: { reachable: false } }`.

**Cause**: The `COMFYUI_URL` in `.env` does not point to a running ComfyUI instance.

**Solution**:

```bash
# 1. Verify what you have configured
grep COMFYUI_URL .env

# 2. Test connectivity from the gateway host
curl -s http://127.0.0.1:8188/
# Expected: HTML page or JSON from ComfyUI

# 3. If ComfyUI is on a different port or host, update .env
# Example: COMFYUI_URL=http://192.168.1.50:8188

# 4. Restart the gateway after changing .env
npm run dev
```

### 1b. Firewall Blocking the Port

**Symptom**: `curl` to the ComfyUI URL times out or returns `Connection refused`,
but ComfyUI is confirmed running on that machine.

**Cause**: A host firewall (Windows Defender, iptables, ufw) is blocking the port.

**Solution**:

```bash
# Linux (ufw)
sudo ufw allow 8188/tcp
sudo ufw reload

# Linux (iptables)
sudo iptables -A INPUT -p tcp --dport 8188 -j ACCEPT

# Windows (PowerShell, run as Admin)
New-NetFirewallRule -DisplayName "ComfyUI" -Direction Inbound -Port 8188 -Protocol TCP -Action Allow

# Verify the port is listening
# Linux
ss -tlnp | grep 8188
# Windows
netstat -an | findstr 8188
```

### 1c. Docker Networking

**Symptom**: Gateway running inside Docker cannot reach ComfyUI on `127.0.0.1:8188`.

**Cause**: `127.0.0.1` inside a Docker container refers to the container itself,
not the host machine.

**Solution**:

```bash
# Option A: Use Docker's special host DNS (Linux + Docker Desktop)
COMFYUI_URL=http://host.docker.internal:8188

# Option B: Use the host network mode
docker run --network host comfyui-gateway

# Option C: Put both containers on the same Docker network
docker network create comfy-net
docker run --name comfyui --network comfy-net ...
docker run --name gateway --network comfy-net -e COMFYUI_URL=http://comfyui:8188 ...

# Verify from inside the gateway container
docker exec -it gateway sh -c "wget -qO- http://comfyui:8188/ || echo FAIL"
```

### 1d. WSL2 Networking

**Symptom**: Gateway running on Windows/WSL2 cannot reach ComfyUI running on the
other side (host vs WSL or vice-versa).

**Cause**: WSL2 uses a virtual network adapter. The WSL2 guest and Windows host
have different IP addresses.

**Solution**:

```bash
# From WSL2, get the Windows host IP
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
# Example output: 172.25.192.1

# Set COMFYUI_URL to that IP
COMFYUI_URL=http://172.25.192.1:8188

# Alternatively, if ComfyUI runs inside WSL2 and the gateway is on Windows:
# Find WSL2 IP
wsl hostname -I
# Example output: 172.25.198.5
# Set: COMFYUI_URL=http://172.25.198.5:8188

# Make sure ComfyUI is listening on 0.0.0.0, not just 127.0.0.1
# Launch ComfyUI with: python main.py --listen 0.0.0.0
```

### 1e. ComfyUI Not Started or Crashed

**Symptom**: Port is not listening at all.

**Cause**: ComfyUI process is not running.

**Solution**:

```bash
# Check if the process is running
# Linux
ps aux | grep "main.py"
# Windows
tasklist | findstr python

# Start ComfyUI
cd /path/to/ComfyUI
python main.py --listen 0.0.0.0 --port 8188

# Check logs for startup errors
python main.py --listen 0.0.0.0 --port 8188 2>&1 | tail -50

# Verify it is accepting connections
curl -s http://127.0.0.1:8188/ && echo "OK" || echo "NOT REACHABLE"
```

---

## 2. OOM (Out of Memory) Errors

The gateway classifies these as `COMFYUI_OOM` with `retryable: false`.

### 2a. Resolution or Batch Size Too Large

**Symptom**: Job fails with error containing "CUDA out of memory",
"allocator backend out of memory", or "failed to allocate".

**Cause**: The requested image dimensions or batch size exceeds available VRAM.

**Solution**:

```bash
# 1. Reduce resolution in your job request
# Instead of 2048x2048, try 1024x1024 or 768x768
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": {
      "prompt": "a mountain landscape",
      "width": 1024,
      "height": 1024
    }
  }'

# 2. Reduce batch size to 1
# Set in your job inputs: "batch_size": 1

# 3. Lower the gateway-level limits in .env
MAX_IMAGE_SIZE=1024
MAX_BATCH_SIZE=2
```

### 2b. Too Many Steps

**Symptom**: OOM occurs mid-generation, not immediately at submission.

**Cause**: The sampler accumulates intermediate tensors over many steps.

**Solution**:

```bash
# Reduce steps in the job inputs
# Instead of 50 steps, try 20-30
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": {
      "prompt": "a portrait photo",
      "steps": 20,
      "width": 1024,
      "height": 1024
    }
  }'
```

### 2c. Model Quantization

**Symptom**: Even at low resolution, OOM errors occur because the model is too
large for the GPU (common on 8 GB VRAM cards with SDXL).

**Cause**: Full-precision (fp32) or half-precision (fp16) model weights exceed
available VRAM.

**Solution**:

```bash
# In ComfyUI, use fp8 or quantized checkpoints
# Update your workflow template to use a quantized model:
# e.g., "ckpt_name": "sdxl_base_1.0_fp8.safetensors"

# Or add --fp8_e4m3fn-unet flag when starting ComfyUI
python main.py --listen 0.0.0.0 --fp8_e4m3fn-unet

# Monitor VRAM usage
nvidia-smi -l 2
```

### 2d. VAE Tiling

**Symptom**: OOM happens during the VAE decode step (after sampling completes).

**Cause**: The VAE decoder processes the entire latent at once, which can be very
memory-intensive at high resolutions.

**Solution**:

```
Enable VAE tiling in your ComfyUI workflow by adding a "VAEDecodeTiled" node
instead of "VAEDecode". Tile size of 512 is a good default.

In the workflow JSON template:
{
  "10": {
    "class_type": "VAEDecodeTiled",
    "inputs": {
      "samples": ["3", 0],
      "vae": ["4", 2],
      "tile_size": 512
    }
  }
}
```

---

## 3. Slow Generation

### 3a. GPU Not Being Utilized

**Symptom**: Jobs complete but take much longer than expected. GPU utilization
stays near 0%.

**Cause**: ComfyUI is falling back to CPU inference, or the wrong GPU is selected.

**Solution**:

```bash
# 1. Check GPU utilization during a job
nvidia-smi -l 1
# Look for "GPU-Util" column -- should be 80-100% during sampling

# 2. Verify CUDA is available in ComfyUI
# Check ComfyUI startup logs for "Using device: cuda"

# 3. Force GPU selection (multi-GPU systems)
CUDA_VISIBLE_DEVICES=0 python main.py --listen 0.0.0.0

# 4. Verify PyTorch sees the GPU
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
```

### 3b. Model Loading on Every Job

**Symptom**: First job is slow, subsequent jobs with the same workflow are faster,
but switching workflows causes long delays.

**Cause**: ComfyUI loads the model from disk each time a different checkpoint is
requested. This can take 10-30 seconds per model load.

**Solution**:

```bash
# 1. Increase ComfyUI's model cache
# Start ComfyUI with a larger cache (default is 1 model):
python main.py --listen 0.0.0.0 --cache-size 3

# 2. Use the same checkpoint across workflows when possible
# Standardize on one checkpoint (e.g., sdxl_base_1.0.safetensors)

# 3. Place models on an SSD, not an HDD
# Move ComfyUI/models/ to an NVMe drive for faster load times
```

### 3c. Queue Depth / Concurrency

**Symptom**: Jobs are queued for a long time before starting.
The job stays in `status: "queued"` for minutes.

**Cause**: The worker concurrency is set to 1 (default) and multiple jobs are
queued, or the single slot is occupied by a long-running job.

**Solution**:

```bash
# 1. Check current queue state
curl -s http://localhost:3000/jobs?status=queued | jq '.count'
curl -s http://localhost:3000/jobs?status=running | jq '.count'

# 2. Increase concurrency if your GPU can handle it (multi-batch)
# Edit .env:
MAX_CONCURRENCY=2

# WARNING: Only increase if you have enough VRAM for parallel jobs.
# Two concurrent 1024x1024 SDXL jobs need ~20+ GB VRAM.

# 3. For multi-GPU setups, run multiple worker processes
# Terminal 1: CUDA_VISIBLE_DEVICES=0 npm run start:worker
# Terminal 2: CUDA_VISIBLE_DEVICES=1 npm run start:worker
# Both connect to the same Redis queue
```

### 3d. ComfyUI Startup Time

**Symptom**: The very first job after starting ComfyUI takes 30-60 seconds even
for a simple generation.

**Cause**: ComfyUI performs initialization (loading nodes, compiling, warming up
CUDA) on the first prompt.

**Solution**:

```bash
# 1. Send a warm-up job immediately after starting ComfyUI
# This is a tiny 64x64 generation that forces initialization
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": {
      "prompt": "test",
      "width": 64,
      "height": 64,
      "steps": 1
    }
  }'

# 2. Increase the gateway timeout to account for cold starts
COMFYUI_TIMEOUT_MS=600000
```

---

## 4. Webhook Failures

Webhook errors appear in logs as `WEBHOOK_DELIVERY_FAILED`.

### 4a. DNS Resolution Failure

**Symptom**: Webhook fails with "getaddrinfo ENOTFOUND" or "DNS lookup failed".

**Cause**: The callback URL hostname cannot be resolved.

**Solution**:

```bash
# 1. Test DNS resolution from the gateway host
nslookup your-webhook-domain.com
dig your-webhook-domain.com

# 2. If using a local hostname (e.g., within Docker), make sure it is resolvable
# Add to /etc/hosts if needed:
echo "192.168.1.50 my-webhook-server" | sudo tee -a /etc/hosts

# 3. Verify the callback URL is correct in your job request
curl -X POST http://localhost:3000/jobs \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-key" \
  -d '{
    "workflowId": "sdxl_realism_v1",
    "inputs": { "prompt": "test" },
    "callbackUrl": "https://your-valid-domain.com/webhook"
  }'
```

### 4b. SSL Certificate Errors

**Symptom**: Webhook fails with "self signed certificate", "CERT_HAS_EXPIRED",
or "unable to verify the first certificate".

**Cause**: The webhook receiver uses an invalid, expired, or self-signed SSL certificate.

**Solution**:

```bash
# 1. Test the certificate manually
openssl s_client -connect your-webhook-domain.com:443 -servername your-webhook-domain.com < /dev/null 2>&1 | head -20

# 2. Check expiration
echo | openssl s_client -connect your-webhook-domain.com:443 2>/dev/null | openssl x509 -noout -dates

# 3. For development with self-signed certs, set NODE_TLS_REJECT_UNAUTHORIZED
# WARNING: Do NOT use this in production
NODE_TLS_REJECT_UNAUTHORIZED=0 npm run dev

# 4. For production, fix the certificate (use Let's Encrypt or a valid CA)
```

### 4c. Webhook Timeout

**Symptom**: Webhook logs show "AbortError" or "Webhook POST timed out".

**Cause**: The webhook receiver takes longer than 10 seconds to respond.
The gateway has a hardcoded 10-second timeout per webhook attempt with
3 retries and exponential backoff.

**Solution**:

```bash
# 1. Ensure your webhook receiver responds quickly
# The receiver should return 200 immediately and process asynchronously
# BAD:  app.post("/webhook", async (req, res) => { await longProcess(); res.send("ok"); })
# GOOD: app.post("/webhook", (req, res) => { res.send("ok"); enqueueWork(req.body); })

# 2. Test receiver response time
time curl -s -o /dev/null -w "%{time_total}" -X POST https://your-webhook.com/callback \
  -H "Content-Type: application/json" -d '{"test": true}'
# Should be < 2 seconds
```

### 4d. Domain Not in Allowlist

**Symptom**: Job creation fails with `Callback domain "example.com" is not in the
allowed domains list`.

**Cause**: `WEBHOOK_ALLOWED_DOMAINS` is configured and does not include the
callback URL's domain.

**Solution**:

```bash
# 1. Check current setting
grep WEBHOOK_ALLOWED_DOMAINS .env

# 2. Add the domain (comma-separated list)
WEBHOOK_ALLOWED_DOMAINS=your-app.com,n8n.your-domain.com,*.internal.company.com

# 3. Or allow all domains (less secure, suitable for development)
WEBHOOK_ALLOWED_DOMAINS=*

# 4. Restart the gateway
npm run dev
```

### 4e. HMAC Signature Mismatch

**Symptom**: Your webhook receiver receives the POST but HMAC validation fails
on your end.

**Cause**: The `WEBHOOK_SECRET` configured in the gateway does not match the secret
your receiver uses to validate signatures, or the signature computation differs.

**Solution**:

```bash
# 1. Verify the WEBHOOK_SECRET matches on both sides
grep WEBHOOK_SECRET .env

# 2. The gateway sends: X-Signature: sha256=<hex>
# Computed as: HMAC-SHA256(secret, raw_body_string)
# Verify in Node.js:
node -e "
const crypto = require('crypto');
const secret = 'your-webhook-secret';
const body = '{\"jobId\":\"test\",\"status\":\"succeeded\"}';
const sig = crypto.createHmac('sha256', secret).update(body, 'utf8').digest('hex');
console.log('Expected header: sha256=' + sig);
"

# 3. Common mistakes:
# - Parsing the body before computing HMAC (must use raw string)
# - Using different encodings (gateway uses utf8)
# - Comparing strings case-sensitively (hex is lowercase)
```

---

## 5. Redis Connection Issues

### 5a. Cannot Connect to Redis

**Symptom**: Gateway crashes at startup with "Redis connection error" or
"ECONNREFUSED" targeting the Redis port.

**Cause**: Redis server is not running, or the `REDIS_URL` is wrong.

**Solution**:

```bash
# 1. Check if Redis is running
redis-cli ping
# Expected: PONG

# 2. Verify the URL format
# Correct formats:
#   redis://localhost:6379
#   redis://:yourpassword@redis-host:6379/0
#   rediss://user:password@host:6380/0  (TLS)

# 3. Test connectivity
redis-cli -u "redis://localhost:6379" ping

# 4. If Redis is not needed, remove REDIS_URL to use in-memory queue
# Edit .env:
REDIS_URL=
# The gateway falls back to an in-memory queue automatically
```

### 5b. Redis Authentication Failure

**Symptom**: Error message contains "NOAUTH Authentication required" or
"ERR invalid password".

**Cause**: Redis requires a password but `REDIS_URL` does not include one,
or the password is wrong.

**Solution**:

```bash
# 1. Include the password in the URL
REDIS_URL=redis://:your_redis_password@localhost:6379/0

# 2. Test with redis-cli
redis-cli -a "your_redis_password" ping

# 3. Check Redis config for requirepass
redis-cli CONFIG GET requirepass
```

### 5c. Fallback to In-Memory Queue

**Symptom**: Logs show "No Redis URL configured, using in-memory queue" and
you expected BullMQ.

**Cause**: `REDIS_URL` is empty or not set in `.env`.

**Solution**:

```bash
# 1. Set REDIS_URL in .env
REDIS_URL=redis://localhost:6379

# 2. Verify Redis is running
redis-cli ping

# 3. Restart the gateway
npm run dev

# 4. Confirm in logs: should show "Redis URL configured, using BullMQ worker"
```

> **Note**: The in-memory queue is fine for single-instance development deployments.
> For production with multiple workers or durability requirements, use Redis + BullMQ.

---

## 6. Storage Errors

### 6a. Local Disk Permission Denied

**Symptom**: Job fails at the output storage step with "EACCES: permission denied"
or `STORAGE_READ_ERROR`.

**Cause**: The gateway process does not have write permissions to `STORAGE_LOCAL_PATH`.

**Solution**:

```bash
# 1. Check the configured path
grep STORAGE_LOCAL_PATH .env
# Default: ./data/outputs

# 2. Ensure the directory exists and is writable
mkdir -p ./data/outputs
chmod 755 ./data/outputs

# 3. Check ownership
ls -la ./data/

# 4. If running as a different user (e.g., in Docker)
chown -R node:node ./data/outputs

# 5. For Docker, mount a volume with correct permissions
# docker run -v /host/path/outputs:/app/data/outputs ...
```

### 6b. S3 Credentials Invalid

**Symptom**: Job fails with `STORAGE_S3_PUT_ERROR` and the underlying error
mentions "InvalidAccessKeyId", "SignatureDoesNotMatch", or "AccessDenied".

**Cause**: The `S3_ACCESS_KEY` / `S3_SECRET_KEY` are wrong, expired, or the
IAM policy does not grant `s3:PutObject` permission.

**Solution**:

```bash
# 1. Verify credentials are set
grep S3_ACCESS_KEY .env
grep S3_SECRET_KEY .env
grep S3_BUCKET .env

# 2. Test with AWS CLI
aws s3 ls s3://your-bucket/ \
  --endpoint-url http://your-minio:9000 \
  --region us-east-1

# 3. Test a put operation
echo "test" > /tmp/test.txt
aws s3 cp /tmp/test.txt s3://your-bucket/test.txt \
  --endpoint-url http://your-minio:9000

# 4. Minimum IAM policy for the gateway:
# {
#   "Version": "2012-10-17",
#   "Statement": [{
#     "Effect": "Allow",
#     "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject", "s3:ListBucket"],
#     "Resource": ["arn:aws:s3:::your-bucket", "arn:aws:s3:::your-bucket/*"]
#   }]
# }
```

### 6c. MinIO Configuration

**Symptom**: S3 storage fails with "socket hang up", "ECONNREFUSED", or
"Bucket does not exist".

**Cause**: MinIO endpoint is wrong, the bucket has not been created, or
`forcePathStyle` is not enabled (handled automatically by the gateway).

**Solution**:

```bash
# 1. Verify MinIO is running
curl http://localhost:9000/minio/health/live
# Expected: HTTP 200

# 2. Set the correct endpoint in .env
S3_ENDPOINT=http://localhost:9000
S3_BUCKET=comfyui-outputs
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_REGION=us-east-1

# 3. Create the bucket if it does not exist
# Using mc (MinIO Client)
mc alias set local http://localhost:9000 minioadmin minioadmin
mc mb local/comfyui-outputs

# Or using AWS CLI
aws s3 mb s3://comfyui-outputs --endpoint-url http://localhost:9000
```

---

## 7. Database Issues

### 7a. SQLite WAL Lock Errors

**Symptom**: Intermittent "SQLITE_BUSY" or "database is locked" errors under
concurrent load.

**Cause**: Multiple processes or threads are writing to the SQLite database
simultaneously. SQLite WAL mode supports concurrent readers but only one writer.

**Solution**:

```bash
# 1. The gateway already sets optimal pragmas:
#    journal_mode = WAL
#    synchronous = NORMAL
#    busy_timeout = 5000 (5 seconds)

# 2. If running multiple gateway instances, switch to Postgres
DATABASE_URL=postgresql://user:password@localhost:5432/comfyui_gateway

# 3. If you must use SQLite with a single instance, increase busy timeout
# (requires code change or env override):
# The default 5000ms should be sufficient for most single-instance use cases

# 4. Check for stuck WAL files
ls -la ./data/gateway.db*
# You should see: gateway.db, gateway.db-wal, gateway.db-shm

# 5. If the database is corrupted, try recovery
sqlite3 ./data/gateway.db "PRAGMA integrity_check;"
# If it reports errors, back up and recreate:
cp ./data/gateway.db ./data/gateway.db.bak
sqlite3 ./data/gateway.db ".recover" | sqlite3 ./data/gateway_recovered.db
```

### 7b. Postgres Connection Pooling

**Symptom**: Errors like "too many clients already", "remaining connection slots
are reserved", or intermittent "Connection terminated unexpectedly".

**Cause**: The gateway opens too many connections to Postgres, exceeding
`max_connections`, or connections are not being properly returned to the pool.

**Solution**:

```bash
# 1. Check current connections in Postgres
psql -c "SELECT count(*) FROM pg_stat_activity WHERE datname = 'comfyui_gateway';"

# 2. Check max_connections setting
psql -c "SHOW max_connections;"

# 3. Use a connection pooler like PgBouncer
# Install PgBouncer and point DATABASE_URL to it
DATABASE_URL=postgresql://user:password@localhost:6432/comfyui_gateway

# 4. If running multiple gateway instances, ensure the total pool size
# across all instances does not exceed Postgres max_connections
```

### 7c. Database URL Format

**Symptom**: Gateway crashes at startup with "Invalid connection string" or
uses SQLite when you intended Postgres.

**Cause**: The `DATABASE_URL` format is wrong. The gateway checks if the URL
starts with `postgres://` or `postgresql://` to select the Postgres backend.

**Solution**:

```bash
# SQLite formats (all valid):
DATABASE_URL=./data/gateway.db
DATABASE_URL=/absolute/path/to/gateway.db

# Postgres formats (must start with postgres:// or postgresql://):
DATABASE_URL=postgresql://user:password@localhost:5432/comfyui_gateway
DATABASE_URL=postgres://user:password@host:5432/dbname?sslmode=require
```

---

## 8. Job Stuck in "running"

### 8a. ComfyUI Crashed During Execution

**Symptom**: A job shows `status: "running"` indefinitely. No progress updates.
The gateway health endpoint may show `comfyui.reachable: false`.

**Cause**: ComfyUI crashed (segfault, CUDA error, killed by OOM killer) while
processing the job, and the gateway's WebSocket connection was severed.

**Solution**:

```bash
# 1. Check job status
curl -s http://localhost:3000/jobs/<jobId> | jq '.status'

# 2. Check if ComfyUI is still running
curl -s http://localhost:3000/health | jq '.comfyui.reachable'

# 3. If ComfyUI crashed, restart it
cd /path/to/ComfyUI
python main.py --listen 0.0.0.0

# 4. The stuck job will eventually time out (COMFYUI_TIMEOUT_MS, default 5 min)
# and be marked as failed with COMFYUI_TIMEOUT

# 5. To immediately cancel the stuck job
curl -X POST http://localhost:3000/jobs/<jobId>/cancel \
  -H "X-API-Key: your-key"

# 6. To reduce timeout for faster failure detection
COMFYUI_TIMEOUT_MS=120000
```

### 8b. WebSocket Disconnection

**Symptom**: Job stays "running" but ComfyUI is actually done. The output
exists in ComfyUI's history.

**Cause**: The WebSocket connection dropped mid-execution, and the polling
fallback failed to pick up the result.

**Solution**:

```bash
# 1. Check ComfyUI history directly
curl -s http://127.0.0.1:8188/history | jq 'keys | length'

# 2. The gateway automatically falls back to HTTP polling if WebSocket fails.
# If polling also fails, the job times out.

# 3. Restart the gateway to reset connections
npm run dev

# 4. Check network stability between gateway and ComfyUI
ping -c 10 <comfyui-host>
```

### 8c. Restart Recovery

**Symptom**: After restarting the gateway, jobs that were "running" remain
in that state permanently.

**Cause**: The in-memory queue loses track of running jobs when the process
restarts. There is no automatic recovery for in-memory jobs.

**Solution**:

```bash
# 1. For production, use Redis (BullMQ) for durable job queues
REDIS_URL=redis://localhost:6379

# 2. Manually fail stuck jobs via the database
sqlite3 ./data/gateway.db \
  "UPDATE jobs SET status='failed', errorJson='{\"code\":\"GATEWAY_RESTART\",\"message\":\"Job interrupted by gateway restart\"}', completedAt=datetime('now') WHERE status='running';"

# 3. Verify
sqlite3 ./data/gateway.db "SELECT id, status FROM jobs WHERE status='running';"
```

---

## 9. Rate Limiting Issues

### 9a. Identifying You Are Being Rate Limited

**Symptom**: API returns HTTP 429 with body `{ "error": "RATE_LIMITED" }` and
a `Retry-After` header.

**Cause**: You exceeded `RATE_LIMIT_MAX` requests within the `RATE_LIMIT_WINDOW_MS`
window. Limits are applied per API key or per IP.

**Solution**:

```bash
# 1. Check the response headers
curl -v http://localhost:3000/health -H "X-API-Key: your-key" 2>&1 | grep -i "x-ratelimit"
# X-RateLimit-Limit: 100
# X-RateLimit-Remaining: 0
# Retry-After: 42

# 2. Wait for the Retry-After period, then retry

# 3. Implement exponential backoff in your client
```

### 9b. Adjusting Rate Limits

**Symptom**: Legitimate usage is being throttled.

**Cause**: Default limits (100 requests/minute) are too low for your workload.

**Solution**:

```bash
# 1. Increase the limit in .env
RATE_LIMIT_MAX=500
RATE_LIMIT_WINDOW_MS=60000

# 2. For burst workloads, widen the window
RATE_LIMIT_MAX=1000
RATE_LIMIT_WINDOW_MS=300000

# 3. Restart the gateway
npm run dev

# 4. Note: Rate limits are per API key (if authenticated) or per IP.
# Different API keys have independent counters.
```

### 9c. Rate Limit Per API Key vs Per IP

**Symptom**: Different clients sharing the same IP are interfering with each
other's rate limits.

**Cause**: Without API keys, all requests from the same IP share a single
rate-limit bucket.

**Solution**:

```bash
# 1. Assign unique API keys to each client
API_KEYS=client1-key:user,client2-key:user,admin-key:admin

# 2. Each client uses its own X-API-Key header
# Client 1: -H "X-API-Key: client1-key"
# Client 2: -H "X-API-Key: client2-key"

# 3. Each key gets its own independent rate-limit counter
```

---

## 10. Authentication Problems

### 10a. API Key Not Accepted

**Symptom**: Every request returns HTTP 401 with `{ "error": "AUTH_FAILED",
"message": "Invalid API key" }`.

**Cause**: The `X-API-Key` header value does not match any entry in `API_KEYS`.

**Solution**:

```bash
# 1. Check configured keys
grep API_KEYS .env
# Format: key1:admin,key2:user

# 2. Ensure your request uses the exact key (no extra whitespace)
curl -H "X-API-Key: mykey123" http://localhost:3000/health

# 3. Keys are case-sensitive and matched exactly

# 4. If API_KEYS is empty, authentication is DISABLED (development mode)
# All requests are treated as admin. Set keys for production:
API_KEYS=sk-prod-abc123:admin,sk-user-xyz789:user
```

### 10b. JWT Token Expired

**Symptom**: Request returns `{ "error": "AUTH_FAILED", "message": "JWT token
has expired" }`.

**Cause**: The JWT `exp` claim is in the past.

**Solution**:

```bash
# 1. Decode the JWT to check expiration (without verification)
echo "<your-token>" | cut -d'.' -f2 | base64 -d 2>/dev/null | jq '.exp'

# 2. Compare with current time
date +%s

# 3. Generate a new token with a longer TTL
# Example using Node.js:
node -e "
const crypto = require('crypto');
const secret = 'your-jwt-secret';
const header = Buffer.from(JSON.stringify({alg:'HS256',typ:'JWT'})).toString('base64url');
const payload = Buffer.from(JSON.stringify({
  sub: 'user-1',
  role: 'admin',
  iat: Math.floor(Date.now()/1000),
  exp: Math.floor(Date.now()/1000) + 86400  // 24 hours
})).toString('base64url');
const sig = crypto.createHmac('sha256', secret).update(header+'.'+payload).digest('base64url');
console.log(header+'.'+payload+'.'+sig);
"
```

### 10c. JWT Signature Invalid

**Symptom**: Request returns `{ "error": "AUTH_FAILED", "message": "Invalid JWT
signature" }`.

**Cause**: The JWT was signed with a different secret than what is configured in
`JWT_SECRET`.

**Solution**:

```bash
# 1. Verify the secret matches on token-issuer side and gateway side
grep JWT_SECRET .env

# 2. The gateway uses HMAC-SHA256 (HS256) exclusively
# Make sure your token issuer also uses HS256 with the same secret

# 3. Re-generate the token using the correct secret
```

### 10d. No Authentication Header Provided

**Symptom**: Request returns `{ "error": "AUTH_FAILED", "message": "Authentication
required. Provide X-API-Key header or Authorization: Bearer token." }`.

**Cause**: The request has no `X-API-Key` header and no `Authorization: Bearer`
header, and authentication is enabled (API_KEYS or JWT_SECRET is set).

**Solution**:

```bash
# Option A: Use API Key
curl -H "X-API-Key: your-key" http://localhost:3000/health

# Option B: Use JWT Bearer token
curl -H "Authorization: Bearer your.jwt.token" http://localhost:3000/health

# Option C: Disable auth for development (NOT for production)
# Remove all values from API_KEYS and JWT_SECRET in .env:
API_KEYS=
JWT_SECRET=
```

### 10e. Insufficient Permissions (Forbidden)

**Symptom**: Request returns HTTP 403 with `{ "error": "FORBIDDEN", "message":
"Admin role required for this operation" }`.

**Cause**: You are using a `user` role key to perform an admin-only action
(workflow CRUD).

**Solution**:

```bash
# 1. Check which role your key has
grep API_KEYS .env
# Example: sk-user-key:user,sk-admin-key:admin

# 2. Use the admin key for workflow management
curl -H "X-API-Key: sk-admin-key" -X POST http://localhost:3000/workflows ...

# 3. User role can: create jobs, read own jobs, view health/capabilities
# Admin role can: everything the user can + workflow CRUD + view all jobs
```

---

## Quick Diagnostic Commands

```bash
# Gateway health
curl -s http://localhost:3000/health | jq .

# ComfyUI direct connectivity
curl -s http://127.0.0.1:8188/ | head -5

# Queue status
curl -s http://localhost:3000/jobs?status=queued -H "X-API-Key: KEY" | jq '.count'
curl -s http://localhost:3000/jobs?status=running -H "X-API-Key: KEY" | jq '.count'

# GPU memory
nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader

# Redis connectivity
redis-cli -u "$REDIS_URL" ping

# SQLite integrity
sqlite3 ./data/gateway.db "PRAGMA integrity_check;"

# Logs (if using pino-pretty)
npm run dev 2>&1 | npx pino-pretty

# Check all configured environment variables
grep -v '^#' .env | grep -v '^$'
```
