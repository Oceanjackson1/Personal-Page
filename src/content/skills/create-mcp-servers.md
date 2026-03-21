---
title: "Create MCP Servers"
description: "Create Model Context Protocol (MCP) servers that expose tools, resources, and prompts to Claude. Use when building custom integrations, APIs, data sources, or any server that Claude should interact with via the MCP protocol. Supports both TypeScri..."
category: "development"
source: "community"
author: "Community"
tags: ["create", "mcp", "servers"]
date: 2026-03-20
---

<objective>
MCP servers extend Claude's capabilities by exposing tools, resources, and prompts. This skill guides creation of production-ready MCP servers with API integrations, OAuth authentication, response optimization, and proper installation in Claude Code and Claude Desktop.
</objective>

<essential_principles>

<the_5_rules>
Every MCP server must follow these:

1. **Never Hardcode Secrets** - Use `${VAR}` expansion in configs, environment variables in code
2. **Use `cwd` Property** - Isolates dependencies (not `--cwd` in args)
3. **Always Absolute Paths** - `which uv` to find paths, never relative
4. **One Server Per Directory** - `~/Developer/mcp/{server-name}/`
5. **Use `uv` for Python** - Better than pip, handles venvs automatically
</the_5_rules>

<security_checklist>
- Never ask user to paste secrets into chat
- Always use environment variables for credentials
- Use ${VAR} expansion in configs
- Provide exact commands for user to run in terminal
- Verify environment variable existence without showing values
- Never hardcode API keys in code or configs
</security_checklist>

<architecture_decision>
Operation count determines architecture:

- **1-2 operations** → Traditional pattern (flat tools)
- **3+ operations** → On-demand discovery pattern (meta-tools)

Traditional: Each operation is a separate tool
On-demand: 4 meta-tools (discover, get_schema, execute, continue) + operations.json
</architecture_decision>

<context>
MCP servers expose:
- **Tools**: Functions Claude can call (API requests, file operations, calculations)
- **Resources**: Data Claude can read (files, database records, API responses)
- **Prompts**: Reusable prompt templates with arguments

Standard location: `~/Developer/mcp/{server-name}/`
</context>

</essential_principles>

<routing>
Based on user intent, route to appropriate workflow:

**No context provided** (skill invoked without description):
Use AskUserQuestion:
- header: "Mode"
- question: "What would you like to do?"
- options:
  - "Create a new MCP server" → workflows/create-new-server.md
  - "Update an existing MCP server" → workflows/update-existing-server.md
  - "Troubleshoot a server" → workflows/troubleshoot-server.md

**Context provided** (user described what they want):
Route directly to workflows/create-new-server.md
</routing>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| create-new-server.md | Full 8-step workflow from intake to verification |
| update-existing-server.md | Modify or extend an existing server |
| troubleshoot-server.md | Diagnose and fix connection/runtime issues |
</workflows_index>

<templates_index>
| Template | Purpose |
|----------|---------|
| python-server.py | Traditional pattern starter for Python |
| typescript-server.ts | Traditional pattern starter for TypeScript |
| operations.json | On-demand discovery operations definition |
</templates_index>

<scripts_index>
| Script | Purpose |
|--------|---------|
| setup-python-project.sh | Initialize Python MCP project with uv |
| setup-typescript-project.sh | Initialize TypeScript MCP project with npm |
</scripts_index>

<references_index>
**Core workflow:**
- creation-workflow.md - Complete step-by-step with exact commands

**Architecture patterns:**
- traditional-pattern.md - For 1-2 operations (flat tools)
- large-api-pattern.md - For 3+ operations (on-demand discovery)

**Language-specific:**
- python-implementation.md - Async patterns, type hints
- typescript-implementation.md - Type safety, SDK features

**Advanced topics:**
- oauth-implementation.md - OAuth with stdio isolation
- response-optimization.md - Field truncation, pagination
- tools-and-resources.md - Resources API, prompts, streaming
- testing-and-deployment.md - Unit tests, packaging, publishing
- validation-checkpoints.md - All validation checks
- adaptive-questioning-guide.md - Question templates for intake
- api-research-template.md - API research document format
</references_index>

<quick_reference>
```bash
# List servers
claude mcp list

# Add server (Python)
claude mcp add --transport stdio <name> \
  --env API_KEY='${API_KEY}' \
  -- uv --directory ~/Developer/mcp/<name> run python -m src.server

# Add server (TypeScript)
claude mcp add --transport stdio <name> \
  --env API_KEY='${API_KEY}' \
  -- node ~/Developer/mcp/<name>/build/index.js

# Remove server
claude mcp remove <name>

# Check logs
tail -f ~/Library/Logs/Claude/mcp-server-<name>.log

# Find paths
which uv && which node && which python
```
</quick_reference>

<troubleshooting_quick>
**Server not appearing:** Check `claude mcp list`, verify config in `~/.claude/settings.json`

**"command not found":** Use absolute paths from `which uv` / `which node`

**Environment variable not found:**
```bash
echo $MY_API_KEY  # Check if set
echo 'export MY_API_KEY="value"' >> ~/.zshrc && source ~/.zshrc
```

**Secrets visible in conversation:** STOP. Delete conversation. Rotate credentials. Never paste secrets in chat.

Full troubleshooting: workflows/troubleshoot-server.md
</troubleshooting_quick>

<success_criteria>
A production-ready MCP server has:
- Valid configuration in Claude Code (`claude mcp list` shows ✓ Connected)
- Valid configuration in Claude Desktop config
- Environment variables set securely in ~/.zshrc
- Architecture matches operation count
- OAuth stdio isolation if applicable
- Response optimization for list/search operations
- All validation checkpoints passed
- No errors in logs
</success_criteria>

---

## Reference: Adaptive Questioning Guide

# Adaptive Questioning Guide

## Question Templates by Purpose

When "Ask me 4 more targeted questions" is selected, generate questions based on the purpose(s) selected in Step 0.

### For API Integration

- Which specific endpoints/resources? (e.g., for Stripe: payments, customers, subscriptions)
- Read-only, write access, or both?
- Any specific use cases to prioritize?
- Authentication scope needed?

### For Database Access

- Which database system? (PostgreSQL, MySQL, MongoDB, etc.)
- What operations? (SELECT only, full CRUD, complex queries)
- Specific tables/collections?
- Migration management needed?

### For File Operations

- What file types? (JSON, CSV, images, etc.)
- Read, write, or both?
- Batch processing or single files?
- Directory traversal needed?

### For Custom Tools

- What calculations/transformations?
- Input/output data types?
- Real-time or batch processing?
- Any external dependencies?

## Usage

1. Select relevant template based on purpose from Step 0
2. Generate 4 questions using AskUserQuestion tool
3. After receiving answers, analyze for gaps
4. Present decision gate again
5. Repeat until user selects "Proceed to API research"

---

## Reference: Api Research Template

# API Research Template

Use this template when creating API_RESEARCH.md in Step 1.

```markdown
# API Research: {Service Name}

**Research Date:** {YYYY-MM-DD}
**Documentation Version:** {version if available}

## Sources (with dates)

- Official docs: {URL} (accessed {date})
- SDK repository: {URL} (last updated {date})
- Additional references: {URLs with dates}

**All sources verified as 2024-2025 current.**

## Authentication

**Method:** {API Key / OAuth 2.0 / JWT / etc.}
**How to obtain:** {exact steps or URL}
**How to pass:** {Header: "Authorization: Bearer TOKEN" / Query param / etc.}

## Official SDK

**Exists:** {Yes/No}
**Package name:** {npm package / PyPI package}
**Version:** {latest version number}
**Install command:** {npm install X / pip install X}
**Documentation:** {SDK docs URL}

## Base URL

{https://api.service.com/v1}

## Required Endpoints

### Operation 1: {operation-name}

- **Endpoint:** `{METHOD} /path/to/endpoint`
- **Verified:** ✓ Confirmed in official docs
- **Parameters:**
  - `param1` (required): {type} - {description}
  - `param2` (optional): {type} - {description}
- **Response schema:**
  ```json
  {
    "field": "type",
    "nested": {"field": "type"}
  }
  ```
- **Official example:** {link to example in docs}

### Operation 2: {operation-name}

{Repeat for EVERY planned operation from Step 0}

## Rate Limits

- **Requests per minute:** {number}
- **Requests per hour:** {number}
- **Rate limit headers:** {X-RateLimit-Remaining, etc.}

## Current Implementation Patterns (2024-2025)

**Async/await:** {Yes - modern async/await patterns used}
**Error handling:** {Standard HTTP status codes / Custom error format}
**Pagination:** {Cursor-based / Offset-based / Page-based}
**Webhooks:** {Supported: Yes/No, webhook verification method}

## Notes

{Any important gotchas, deprecations, or special considerations}
```

---

## Reference: Auto Installation

# Auto-Installation for MCP Servers

Complete guide for automatically installing MCP servers in both Claude Code and Claude Desktop with safe credential management.

## Overview

When you build an MCP server, you want it instantly available in both:
- **Claude Code** - For development and coding workflows
- **Claude Desktop** - For conversational usage

This guide provides scripts and patterns for zero-friction installation.

## The Problem

Manual MCP installation requires:
1. Adding to Claude Code via CLI (`claude mcp add`)
2. Editing Claude Desktop config JSON manually
3. Copying credentials to multiple places
4. Restarting both applications
5. Testing that everything works

This is tedious and error-prone.

## The Solution

A manual configuration approach with secure patterns:
1. Store credentials in `~/.mcp_secrets` with `chmod 600`
2. Use variable expansion (`${VAR}`) in all configs
3. Install in Claude Code (user scope)
4. Manually update Claude Desktop config with variable references
5. Never write hardcoded secrets to configuration files

**Why not automated?** Auto-installation scripts that write actual credential values to configs are insecure. The recommended pattern uses variable expansion everywhere.

## Secure Installation Guide

### Step 1: Set Up Secrets

Create `~/.mcp_secrets`:
```bash
# ~/.mcp_secrets
export META_ACCESS_TOKEN="your_token_here"
export META_AD_ACCOUNT_ID="act_123456"
export STRIPE_API_KEY="sk_live_xyz"
```

Secure it:
```bash
chmod 600 ~/.mcp_secrets
```

Load in shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
# Load MCP secrets
if [ -f ~/.mcp_secrets ]; then
  source ~/.mcp_secrets
fi
```

Reload:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### Step 2: Install in Claude Code

```bash
# Source secrets
source ~/.mcp_secrets

# Install with actual values (Claude Code stores them securely)
claude mcp add --transport stdio meta-ads \
  --scope user \
  --env META_ACCESS_TOKEN=${META_ACCESS_TOKEN} \
  --env META_AD_ACCOUNT_ID=${META_AD_ACCOUNT_ID} \
  -- uv --directory ~/Developer/mcp/meta-ads-mcp run python -m src.server
```

**Note:** When using `claude mcp add`, you pass actual values. Claude Code stores them securely in `~/.claude/.claude.json` and references them correctly.

### Step 3: Configure Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "meta-ads": {
      "command": "/Users/username/.local/bin/uv",
      "args": ["--directory", "/Users/username/Developer/mcp/meta-ads-mcp", "run", "python", "-m", "src.server"],
      "cwd": "/Users/username/Developer/mcp/meta-ads-mcp",
      "env": {
        "META_ACCESS_TOKEN": "${META_ACCESS_TOKEN}",
        "META_AD_ACCOUNT_ID": "${META_AD_ACCOUNT_ID}"
      }
    }
  }
}
```

**CRITICAL:** Use variable expansion (`${VAR}`), never hardcode values.

### Step 4: Verify Installation

```bash
# Check Claude Code
claude mcp list

# Test environment variables
echo $META_ACCESS_TOKEN  # Should show value
```

Restart Claude Desktop and test.

## Complete Examples

### Example 1: Stripe MCP Server

**1. Add to `~/.mcp_secrets`:**
```bash
export STRIPE_API_KEY="sk_live_abc123"
```

**2. Install in Claude Code:**
```bash
source ~/.mcp_secrets
claude mcp add --transport stdio stripe \
  --scope user \
  --env STRIPE_API_KEY=${STRIPE_API_KEY} \
  -- uv --directory ~/Developer/mcp/stripe-mcp run python -m src.server
```

**3. Configure Claude Desktop:**
```json
{
  "mcpServers": {
    "stripe": {
      "command": "/Users/username/.local/bin/uv",
      "args": ["--directory", "/Users/username/Developer/mcp/stripe-mcp", "run", "python", "-m", "src.server"],
      "cwd": "/Users/username/Developer/mcp/stripe-mcp",
      "env": {
        "STRIPE_API_KEY": "${STRIPE_API_KEY}"
      }
    }
  }
}
```

### Example 2: Multi-Profile Server (GoHighLevel)

**1. Add to `~/.mcp_secrets`:**
```bash
export GHL_MAIN_API_TOKEN="pit_main_abc"
export GHL_MAIN_LOCATION_ID="loc_main_123"
export GHL_CLIENT_API_TOKEN="pit_client_xyz"
export GHL_CLIENT_LOCATION_ID="loc_client_456"
```

**2. Install in Claude Code:**
```bash
source ~/.mcp_secrets
claude mcp add --transport stdio ghl \
  --scope user \
  --env GHL_MAIN_API_TOKEN=${GHL_MAIN_API_TOKEN} \
  --env GHL_MAIN_LOCATION_ID=${GHL_MAIN_LOCATION_ID} \
  --env GHL_CLIENT_API_TOKEN=${GHL_CLIENT_API_TOKEN} \
  --env GHL_CLIENT_LOCATION_ID=${GHL_CLIENT_LOCATION_ID} \
  -- uv --directory ~/Developer/mcp/ghl-mcp run python -m src.server
```

**3. Configure Claude Desktop:**
```json
{
  "mcpServers": {
    "ghl": {
      "command": "/Users/username/.local/bin/uv",
      "args": ["--directory", "/Users/username/Developer/mcp/ghl-mcp", "run", "python", "-m", "src.server"],
      "cwd": "/Users/username/Developer/mcp/ghl-mcp",
      "env": {
        "GHL_MAIN_API_TOKEN": "${GHL_MAIN_API_TOKEN}",
        "GHL_MAIN_LOCATION_ID": "${GHL_MAIN_LOCATION_ID}",
        "GHL_CLIENT_API_TOKEN": "${GHL_CLIENT_API_TOKEN}",
        "GHL_CLIENT_LOCATION_ID": "${GHL_CLIENT_LOCATION_ID}"
      }
    }
  }
}
```

## Credential Management Best Practices

### Use ~/.mcp_secrets

Store all MCP server credentials in `~/.mcp_secrets`:

```bash
# ~/.mcp_secrets
# Meta Ads
export META_MAIN_ACCESS_TOKEN="EAAJxdR0..."
export META_MAIN_AD_ACCOUNT_ID="act_123456789"

# Stripe
export STRIPE_API_KEY="sk_live_..."

# GoHighLevel
export GHL_MAIN_API_TOKEN="pit-..."
export GHL_MAIN_LOCATION_ID="PpE1PIlJ..."

# Zoom
export ZOOM_ACCOUNT_ID="5ZozWfDX..."
export ZOOM_CLIENT_ID="or2VVA9x..."
export ZOOM_CLIENT_SECRET="oRO3NKXX..."
```

Secure it:
```bash
chmod 600 ~/.mcp_secrets
```

Load in shell profile:
```bash
# Add to ~/.zshrc or ~/.bashrc
if [ -f ~/.mcp_secrets ]; then
  source ~/.mcp_secrets
fi
```

### Security Checklist

- [ ] `~/.mcp_secrets` has `chmod 600` permissions
- [ ] All configs use `${VAR}` variable expansion
- [ ] `.env` files are in `.gitignore`
- [ ] Pre-commit hook installed to catch secrets
- [ ] Never commit actual credential values
- [ ] Rotate credentials if accidentally exposed

## Verification

### Check Claude Code Installation
```bash
# List all installed servers
claude mcp list

# Get specific server details
claude mcp get meta-ads

# Remove if needed
claude mcp remove meta-ads
```

### Check Claude Desktop Configuration

```bash
# View all servers
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq '.mcpServers'

# Check specific server
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq '.mcpServers["meta-ads"]'

# Verify cwd property is set
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq '.mcpServers["meta-ads"].cwd'

# Verify env uses variable expansion
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq '.mcpServers["meta-ads"].env'
```

Ensure configs show `${VAR}` syntax, not actual values.

### Test in Conversation

**Claude Code:**
- Open any project
- Ask: "List available MCP servers"
- Ask: "What Meta Ads operations are available?"

**Claude Desktop:**
- Restart the app
- Ask: "List available MCP servers"
- Ask: "What Meta Ads operations are available?"

## Workflow Integration

When creating MCP servers, include installation in your development process:

### Final Installation Steps

1. **Add credentials to `~/.mcp_secrets`**
2. **Install in Claude Code** using `claude mcp add` with actual values
3. **Configure Claude Desktop** with variable expansion (`${VAR}`)
4. **Verify with security checklist**
5. **Test in both environments**

This ensures secure, consistent installation across all clients.

## Troubleshooting

**"Command not found: claude"**
- Install Claude Code CLI: Open Claude Code → run `/install-cli`

**"jq: command not found"**
```bash
brew install jq  # macOS
```

**"Server not appearing in Claude Code"**
```bash
# Check installation
claude mcp list

# Try removing and reinstalling
claude mcp remove <server-name>
~/.claude/scripts/install-mcp.sh ...
```

**"Server not appearing in Claude Desktop"**
- Verify JSON syntax: `jq '.' ~/Library/Application\ Support/Claude/claude_desktop_config.json`
- Check backup file if config is corrupted
- Restart Claude Desktop

**"Environment variable not found"**
- Check `~/.claude/.env` exists
- Verify variable names match exactly
- Ensure no extra spaces: `KEY=value` not `KEY = value`

## TypeScript/Node Servers

### Installation Pattern

**Claude Code:**
```bash
claude mcp add --transport stdio my-ts-server \
  --scope user \
  --env API_KEY=${API_KEY} \
  -- node ~/Developer/mcp/my-ts-server/dist/index.js
```

**Claude Desktop:**
```json
{
  "mcpServers": {
    "my-ts-server": {
      "command": "/usr/local/bin/node",
      "args": ["/Users/username/Developer/mcp/my-ts-server/dist/index.js"],
      "cwd": "/Users/username/Developer/mcp/my-ts-server",
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

**Note:** TypeScript servers have natural isolation through `node_modules/`.

## Advanced: HTTP/SSE Servers

For remote servers:

```bash
# HTTP server
claude mcp add --transport http my-server https://api.example.com/mcp

# SSE server with headers
claude mcp add --transport sse my-server \
  --header "Authorization: Bearer $API_TOKEN" \
  https://mcp.example.com/sse
```

## Security Best Practices Summary

### Critical Security Rules

1. **Never hardcode credentials** - Always use `${VAR}` variable expansion
2. **Secure credential files** - `chmod 600 ~/.mcp_secrets`
3. **Use `.gitignore`** - Never commit `.env`, `.env.local`, `*.key`, `secrets.json`
4. **Variable expansion everywhere** - Claude Desktop configs must use `${VAR}`
5. **Token rotation** - Update `~/.mcp_secrets`, restart clients
6. **Pre-commit hooks** - Install to catch accidental commits
7. **Always include `cwd`** - Set working directory in all configs
8. **Absolute paths** - Command, args, cwd must all be absolute
9. **User scope for secrets** - Keep credentials out of project configs
10. **Validate before deploy** - Run security checklist

### What Good Looks Like

**✅ Secure Configuration:**
```json
{
  "command": "/Users/username/.local/bin/uv",
  "args": ["--directory", "/Users/username/Developer/mcp/my-server", "run", "python", "-m", "src.server"],
  "cwd": "/Users/username/Developer/mcp/my-server",
  "env": {
    "API_KEY": "${API_KEY}",
    "DB_URL": "${DB_URL:-postgres://localhost/mydb}"
  }
}
```

**❌ Insecure Configuration:**
```json
{
  "command": "uv",
  "args": ["--directory", "./my-server", "run", "python", "-m", "src.server"],
  "env": {
    "API_KEY": "sk_live_abc123"
  }
}
```

Issues: Relative command path, relative directory, hardcoded secret, no `cwd` property.

---

## Reference: Best Practices

# MCP Server Best Practices

<overview>
Production-ready MCP servers require attention to security, reliability, performance, and maintainability. This guide covers essential best practices for building robust servers.
</overview>

## Security

<input_validation>
**Always Validate Inputs**:

```typescript
// TypeScript - Use Zod for strict validation
import { z } from "zod";

const FileReadSchema = z.object({
  path: z.string()
    .min(1, "Path required")
    .max(500, "Path too long")
    .refine(
      (path) => !path.includes(".."),
      "Path traversal not allowed"
    )
    .refine(
      (path) => !path.startsWith("/etc"),
      "System directories not allowed"
    ),
});

async function readFileTool(args: z.infer<typeof FileReadSchema>) {
  // Validation happens automatically via Zod
  const validated = FileReadSchema.parse(args);

  // Additional runtime checks
  const fullPath = path.resolve(ALLOWED_DIR, validated.path);
  if (!fullPath.startsWith(ALLOWED_DIR)) {
    throw new Error("Access denied: Path outside allowed directory");
  }

  // Safe to proceed
  return await fs.readFile(fullPath, "utf-8");
}
```

```python
# Python - Use Pydantic with validators
from pydantic import BaseModel, Field, field_validator
from pathlib import Path

class FileReadArgs(BaseModel):
    path: str = Field(min_length=1, max_length=500)

    @field_validator('path')
    @classmethod
    def validate_path(cls, v: str) -> str:
        # Prevent path traversal
        if ".." in v:
            raise ValueError("Path traversal not allowed")

        # Prevent system directories
        if v.startswith("/etc") or v.startswith("/sys"):
            raise ValueError("System directories not allowed")

        return v

async def read_file_tool(args: FileReadArgs) -> TextContent:
    # Additional runtime checks
    full_path = (Path(ALLOWED_DIR) / args.path).resolve()
    if not str(full_path).startswith(ALLOWED_DIR):
        raise ValueError("Access denied: Path outside allowed directory")

    # Safe to proceed
    async with aiofiles.open(full_path, "r") as f:
        content = await f.read()
        return TextContent(type="text", text=content)
```

**Key principles**:
- Validate all inputs with strict schemas
- Check for path traversal attacks (`..`, absolute paths)
- Whitelist allowed directories/operations
- Validate at schema level AND runtime
- Never trust user input
</input_validation>

<secrets_management>
**Secrets Management**:

```typescript
// TypeScript - Environment variables, never hardcode
import dotenv from "dotenv";
dotenv.config();

interface Config {
  apiKey: string;
  dbPassword: string;
}

function loadConfig(): Config {
  const apiKey = process.env.API_KEY;
  const dbPassword = process.env.DB_PASSWORD;

  if (!apiKey || !dbPassword) {
    throw new Error("Missing required environment variables");
  }

  // NEVER log secrets
  console.error("Config loaded successfully");

  return { apiKey, dbPassword };
}

const config = loadConfig();

// NEVER return secrets to Claude
@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="config://server",
            name="Server Config",
            description="Server configuration (secrets redacted)",
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "config://server":
        return json.dumps({
            "endpoint": config.api_endpoint,
            "timeout": config.timeout,
            # NEVER expose secrets:
            # "apiKey": config.apiKey,  ❌
        })
```

```python
# Python - Use python-dotenv or environment variables
import os
from dataclasses import dataclass

@dataclass
class Config:
    api_key: str
    db_password: str

    @classmethod
    def from_env(cls) -> 'Config':
        api_key = os.getenv("API_KEY")
        db_password = os.getenv("DB_PASSWORD")

        if not api_key or not db_password:
            raise ValueError("Missing required environment variables")

        # NEVER log secrets
        print("Config loaded successfully", file=sys.stderr)

        return cls(api_key=api_key, db_password=db_password)

config = Config.from_env()
```

**Key principles**:
- Use environment variables for secrets
- Never hardcode credentials
- Never log secrets (even in debug mode)
- Never return secrets to Claude
- Use `.env` for development, proper secret management in production
- Rotate secrets regularly
</secrets_management>

<rate_limiting>
**Rate Limiting and Resource Protection**:

```typescript
// TypeScript - Simple rate limiter
class RateLimiter {
  private requests = new Map<string, number[]>();

  check(key: string, limit: number, windowMs: number): boolean {
    const now = Date.now();
    const requests = this.requests.get(key) || [];

    // Remove old requests outside window
    const recent = requests.filter((time) => now - time < windowMs);

    if (recent.length >= limit) {
      return false; // Rate limited
    }

    recent.push(now);
    this.requests.set(key, recent);
    return true;
  }
}

const limiter = new RateLimiter();

async function callTool(name: string, args: any) {
  // Rate limit: 10 requests per minute per tool
  if (!limiter.check(name, 10, 60000)) {
    throw new Error(`Rate limit exceeded for ${name}`);
  }

  // Proceed with tool execution
  return await executeTool(name, args);
}
```

```python
# Python - Rate limiter with asyncio
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[datetime]] = defaultdict(list)

    def check(self, key: str, limit: int, window_seconds: int) -> bool:
        now = datetime.now()
        cutoff = now - timedelta(seconds=window_seconds)

        # Remove old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > cutoff
        ]

        if len(self.requests[key]) >= limit:
            return False  # Rate limited

        self.requests[key].append(now)
        return True

limiter = RateLimiter()

async def call_tool(name: str, args: dict) -> list[TextContent]:
    # Rate limit: 10 requests per minute per tool
    if not limiter.check(name, limit=10, window_seconds=60):
        raise ValueError(f"Rate limit exceeded for {name}")

    # Proceed with tool execution
    return await execute_tool(name, args)
```
</rate_limiting>

<sql_injection>
**SQL Injection Prevention**:

```typescript
// TypeScript - ALWAYS use parameterized queries
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// ✅ CORRECT - Parameterized query
async function getUserById(id: string) {
  const result = await pool.query(
    "SELECT * FROM users WHERE id = $1",
    [id]
  );
  return result.rows[0];
}

// ❌ WRONG - String concatenation (SQL injection!)
async function getUserByIdWrong(id: string) {
  const result = await pool.query(
    `SELECT * FROM users WHERE id = '${id}'`
  );
  return result.rows[0];
}
```

```python
# Python - Use parameterized queries with asyncpg
import asyncpg

async def get_user_by_id(user_id: str) -> dict:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # ✅ CORRECT - Parameterized query
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1",
            user_id
        )
        return dict(row) if row else None
    finally:
        await conn.close()

# ❌ WRONG - String formatting (SQL injection!)
async def get_user_by_id_wrong(user_id: str) -> dict:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        row = await conn.fetchrow(
            f"SELECT * FROM users WHERE id = '{user_id}'"
        )
        return dict(row) if row else None
    finally:
        await conn.close()
```
</sql_injection>

<authentication>
**Authentication & Authorization**:

MCP servers may need to authenticate users or protect sensitive operations. Use OAuth 2.1 for production scenarios.

```typescript
// TypeScript - OAuth Resource Server with FastMCP
import { FastMCP } from "@modelcontextprotocol/server-fastmcp";
import { TokenVerifier, AccessToken } from "@modelcontextprotocol/server-auth";

class JWTTokenVerifier implements TokenVerifier {
  async verifyToken(token: string): Promise<AccessToken | null> {
    try {
      // Verify JWT token (use a library like jose)
      const payload = await verifyJWT(token, process.env.JWT_PUBLIC_KEY);

      return {
        sub: payload.sub,
        scope: payload.scope || "",
        exp: payload.exp,
      };
    } catch (error) {
      return null;
    }
  }
}

const mcp = new FastMCP("Protected API", {
  tokenVerifier: new JWTTokenVerifier(),
  auth: {
    issuerUrl: "https://auth.example.com",
    resourceServerUrl: "http://localhost:3000",
    requiredScopes: ["api:read"],
  },
});

// Tools automatically protected by auth
mcp.tool("get_sensitive_data", async (args, ctx) => {
  // Access token info from context
  const token = ctx.auth?.accessToken;
  if (!token) {
    throw new Error("Unauthorized");
  }

  // Check scopes
  if (!token.scope.includes("data:read")) {
    throw new Error("Insufficient permissions");
  }

  return { data: "sensitive information" };
});
```

```python
# Python - OAuth Resource Server
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.provider import TokenVerifier, AccessToken
from pydantic import AnyHttpUrl
import jwt

class JWTTokenVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        try:
            # Verify JWT (use PyJWT)
            payload = jwt.decode(
                token,
                os.environ["JWT_PUBLIC_KEY"],
                algorithms=["RS256"]
            )

            return AccessToken(
                sub=payload["sub"],
                scope=payload.get("scope", ""),
                exp=payload["exp"],
            )
        except jwt.InvalidTokenError:
            return None

mcp = FastMCP(
    "Protected API",
    token_verifier=JWTTokenVerifier(),
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("https://auth.example.com"),
        resource_server_url=AnyHttpUrl("http://localhost:3000"),
        required_scopes=["api:read"],
    ),
)

@mcp.tool()
async def get_sensitive_data(ctx: Context) -> str:
    """Get sensitive data (requires authentication)."""
    # Access token from context
    token = ctx.request_context.auth.access_token
    if not token:
        raise ValueError("Unauthorized")

    # Check scopes
    if "data:read" not in token.scope:
        raise ValueError("Insufficient permissions")

    return "sensitive information"
```

**API Key Authentication (simpler, less secure)**:

```typescript
// TypeScript - Simple API key auth
const API_KEY = process.env.API_KEY;

server.setRequestHandler("tools/call", async (request) => {
  // Check API key in request metadata
  const apiKey = request.params._meta?.apiKey;

  if (apiKey !== API_KEY) {
    throw new Error("Invalid API key");
  }

  // Proceed with tool execution
  return await handleTool(request.params.name, request.params.arguments);
});
```

```python
# Python - API key in environment variables
API_KEY = os.environ.get("API_KEY")

@mcp.call_tool()
async def call_tool(name: str, arguments: dict, ctx: Context) -> list[TextContent]:
    # Extract API key from request metadata
    api_key = arguments.get("_api_key")

    if api_key != API_KEY:
        raise ValueError("Invalid API key")

    # Proceed with tool execution
    return await execute_tool(name, arguments)
```

**Key principles**:
- Use OAuth 2.1 for production (proper token verification, scope checking)
- API keys only for simple/internal use cases
- Never log tokens or API keys
- Verify authentication on every tool call
- Check authorization (scopes/permissions) per operation
- Return 401 for authentication failures, 403 for authorization failures
- Token verification should be fast (cache public keys)
</authentication>

## Dependency Isolation

<why_it_matters>
**The Problem: Dependency Conflicts Break Everything**

Real story: A pydantic version conflict broke 6 MCP servers simultaneously. One server updated pydantic to 2.10, breaking 5 other servers that required pydantic 2.9. All MCPs failed to start because they shared the same global Python interpreter.

When MCP servers share Python interpreters or global package installations:
- **One server's dependencies can break other servers** (version conflicts cascade)
- **Upgrades become dangerous** (updating one server risks breaking others)
- **Debugging is impossible** (which server caused the conflict?)
- **Rollbacks require reinstalling everything** (no per-server isolation)

**The Solution: Every MCP server needs its own isolated environment**
</why_it_matters>

<uv_tooling>
**Primary Approach: `uv` (Official MCP Recommendation)**

`uv` is the official tool for Python MCP servers. It automatically creates isolated environments per-project and manages dependencies without global installs.

**Development workflow**:
```bash
# Initialize new MCP server with uv
uv init my-mcp-server
cd my-mcp-server

# Add dependencies
uv add mcp aiohttp

# Development/testing
uv run mcp dev server.py

# Install for Claude Desktop
uv run mcp install server.py
```

**Claude Desktop configuration** (automatic isolation):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/username/Developer/mcp/my-server",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

The `--directory` flag tells `uv` to:
1. Use the project's local environment (`.venv/`)
2. Install dependencies from `pyproject.toml` automatically
3. Isolate this server from all others

**Published servers** (for distribution):
```bash
# Users install with uvx (no global pollution)
uvx mcp-server-name
```

**Real examples from working configuration**:

```json
{
  "Workshop": {
    "command": "uv",
    "args": [
      "--directory",
      "/Users/lexchristopherson/Developer/workshops/mcp-server",
      "run",
      "python",
      "server.py"
    ]
  },
  "finance": {
    "command": "uv",
    "args": [
      "--directory",
      "/Users/lexchristopherson/Developer/finance/mcp-server-finance",
      "run",
      "python",
      "server.py"
    ]
  },
  "zoom": {
    "command": "uv",
    "args": [
      "--directory",
      "/Users/lexchristopherson/Developer/mcp/zoom-mcp",
      "run",
      "python",
      "-m",
      "zoom_mcp.server"
    ],
    "env": {
      "ZOOM_ACCOUNT_ID": "...",
      "ZOOM_CLIENT_ID": "...",
      "ZOOM_CLIENT_SECRET": "..."
    }
  }
}
```

Each server runs in complete isolation with its own dependencies.
</uv_tooling>

<anti_patterns>
**What NOT To Do**

**❌ Never use bare `python` or `python3` commands**:
```json
{
  "my-server": {
    "command": "python",
    "args": ["/path/to/server.py"]
  }
}
```
**Why it breaks**: Uses global Python interpreter. Installing dependencies for one server affects all servers. Pydantic conflicts, async library version mismatches, and numpy/pandas incompatibilities will cascade across all MCPs.

**❌ Never use global pip installs**:
```bash
# This breaks isolation
pip install mcp aiohttp pydantic
```
**Why it breaks**: Installs packages globally. When another MCP needs a different version, `pip install --upgrade` breaks the first server. Recovery requires tracking down every affected package.

**❌ Never point to virtual environments directly without `uv`**:
```json
{
  "my-server": {
    "command": "/path/to/.venv/bin/python",
    "args": ["server.py"]
  }
}
```
**Why it breaks**: While this creates isolation, it requires manual venv management. When dependencies change, you must manually reinstall. `uv` handles this automatically via `pyproject.toml`.

**❌ Never share interpreters between servers**:
```bash
# Creating one venv for multiple servers
python -m venv ~/.mcp-shared-env
~/.mcp-shared-env/bin/pip install mcp server1-deps server2-deps
```
**Why it breaks**: Same problem as global installs, just in a different location. Version conflicts still cascade.

**✅ Always use `uv --directory` pattern**:
```json
{
  "my-server": {
    "command": "uv",
    "args": ["--directory", "/full/path/to/project", "run", "python", "server.py"]
  }
}
```
</anti_patterns>

<practical_examples>
**Before: Fragile Configuration** (6 servers broke from one pydantic update)
```json
{
  "mcpServers": {
    "server1": {
      "command": "python",
      "args": ["/path/to/server1.py"]
    },
    "server2": {
      "command": "python",
      "args": ["/path/to/server2.py"]
    },
    "server3": {
      "command": "/path/.venv/bin/python",
      "args": ["server3.py"]
    }
  }
}
```

**After: Isolated Configuration** (each server has own dependencies)
```json
{
  "mcpServers": {
    "server1": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/username/mcp/server1",
        "run",
        "python",
        "server.py"
      ]
    },
    "server2": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/username/mcp/server2",
        "run",
        "python",
        "server.py"
      ]
    },
    "server3": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/username/mcp/server3",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

**Migration guide**:

1. **For each existing MCP server**:
```bash
cd /path/to/mcp-server

# Initialize uv project (creates pyproject.toml)
uv init

# Add your dependencies
uv add mcp aiohttp pydantic
# uv automatically creates isolated .venv/

# Test locally
uv run python server.py
```

2. **Update claude_desktop_config.json**:
```json
{
  "my-server": {
    "command": "uv",
    "args": [
      "--directory",
      "/absolute/path/to/mcp-server",
      "run",
      "python",
      "server.py"
    ]
  }
}
```

3. **Restart Claude Desktop**

Each server now has isolated dependencies. Updating one server's packages never affects others.
</practical_examples>

<typescript_note>
**TypeScript MCP servers** have natural isolation through npm/node_modules:

```json
{
  "my-ts-server": {
    "command": "node",
    "args": ["/path/to/server/dist/index.js"]
  }
}
```

Each TypeScript project has its own `node_modules/` directory, providing automatic isolation. No additional tooling needed.

For published TypeScript servers:
```json
{
  "published-server": {
    "command": "npx",
    "args": ["-y", "@org/mcp-server-name"]
  }
}
```

The `-y` flag installs to npx's cache, isolated from other packages.
</typescript_note>

## Error Handling

<comprehensive_errors>
**Comprehensive Error Handling**:

```typescript
// TypeScript - Error hierarchy
class MCPError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = "MCPError";
  }
}

class ValidationError extends MCPError {
  constructor(message: string) {
    super(message, "VALIDATION_ERROR");
  }
}

class ExternalServiceError extends MCPError {
  constructor(message: string) {
    super(message, "EXTERNAL_SERVICE_ERROR");
  }
}

class NotFoundError extends MCPError {
  constructor(message: string) {
    super(message, "NOT_FOUND");
  }
}

// Tool handler with proper error handling
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const tool = tools.get(request.params.name);

    if (!tool) {
      throw new NotFoundError(`Tool not found: ${request.params.name}`);
    }

    // Validate arguments
    let validatedArgs;
    try {
      validatedArgs = tool.schema.parse(request.params.arguments);
    } catch (error) {
      if (error instanceof z.ZodError) {
        const messages = error.errors.map((e) => `${e.path}: ${e.message}`);
        throw new ValidationError(`Invalid arguments:\n${messages.join("\n")}`);
      }
      throw error;
    }

    // Execute with timeout
    const result = await Promise.race([
      tool.handler(validatedArgs),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Timeout")), 30000)
      ),
    ]);

    return { content: [result] };

  } catch (error) {
    // Log error details to stderr
    console.error("Tool execution error:", {
      tool: request.params.name,
      error: error instanceof Error ? error.message : "Unknown error",
      stack: error instanceof Error ? error.stack : undefined,
    });

    // Return user-friendly error message
    if (error instanceof MCPError) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error.message}`,
          },
        ],
        isError: true,
      };
    }

    // Generic error for unexpected issues
    return {
      content: [
        {
          type: "text",
          text: "An unexpected error occurred. Please contact support.",
        },
      ],
      isError: true,
    };
  }
});
```

```python
# Python - Error hierarchy
class MCPError(Exception):
    """Base MCP error."""
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code

class ValidationError(MCPError):
    """Invalid input validation."""
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")

class ExternalServiceError(MCPError):
    """External service failure."""
    def __init__(self, message: str):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR")

class NotFoundError(MCPError):
    """Resource not found."""
    def __init__(self, message: str):
        super().__init__(message, "NOT_FOUND")

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls with comprehensive error handling."""
    try:
        # Find tool
        if name not in TOOLS:
            raise NotFoundError(f"Tool not found: {name}")

        tool = TOOLS[name]

        # Validate arguments
        try:
            validated_args = tool.args_model(**arguments)
        except ValidationError as e:
            raise ValidationError(f"Invalid arguments: {e}")

        # Execute with timeout
        result = await asyncio.wait_for(
            tool.handler(validated_args),
            timeout=30.0
        )

        return [result]

    except asyncio.TimeoutError:
        logger.error(f"Tool timeout: {name}")
        return [TextContent(
            type="text",
            text="Error: Tool execution timed out (30s limit)"
        )]

    except MCPError as e:
        logger.error(f"MCP error in {name}: {e.code} - {e}")
        return [TextContent(
            type="text",
            text=f"Error: {e}"
        )]

    except Exception as e:
        logger.exception(f"Unexpected error in {name}")
        return [TextContent(
            type="text",
            text="An unexpected error occurred. Please contact support."
        )]
```

**Key principles**:
- Create error hierarchy for different error types
- Always catch and handle errors gracefully
- Log detailed errors to stderr
- Return user-friendly messages to Claude
- Use timeouts to prevent hanging
- Never expose internal implementation details in errors
</comprehensive_errors>

## Logging

<structured_logging>
**Structured Logging**:

```typescript
// TypeScript - Winston logger
import winston from "winston";

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    // Log to stderr (stdout is for MCP protocol)
    new winston.transports.Console({ stream: process.stderr }),
    // Also log to file
    new winston.transports.File({ filename: "mcp-server.log" }),
  ],
});

// Use throughout application
logger.info("Server starting", { version: SERVER_VERSION });

logger.debug("Tool called", {
  tool: "search",
  args: { query: "test" },
});

logger.error("External API failed", {
  tool: "api_call",
  endpoint: "/users",
  error: error.message,
  stack: error.stack,
});
```

```python
# Python - Structured logging with structlog
import structlog
import sys

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Use throughout application
logger.info("server_starting", version=SERVER_VERSION)

logger.debug("tool_called", tool="search", query="test")

logger.error(
    "external_api_failed",
    tool="api_call",
    endpoint="/users",
    error=str(error),
    exc_info=True,
)
```

**Key principles**:
- Always log to stderr (never stdout - reserved for MCP protocol)
- Use structured logging (JSON format)
- Include context in logs (tool name, arguments, etc.)
- Log errors with stack traces
- Use appropriate log levels (debug, info, warn, error)
- Consider log rotation for production
</structured_logging>

## Performance

<context_optimization>
**Context Window Optimization**:

For servers wrapping large APIs (20+ operations), tool definitions can consume 8,000-15,000 tokens before any actual conversation begins. This is one of the biggest performance bottlenecks for MCP servers.

**Solution:** Use the meta-tools + resources pattern to achieve 90-98% context reduction.

See [Large API Pattern](large-api-pattern.md) for complete guide with real metrics:
- Traditional: 81 tools = 15,000 tokens
- Meta-tools pattern: 4 tools = 300 tokens
- **Savings: 98% context reduction**

This is essential for servers wrapping APIs like GitHub, Stripe, Slack, or any API with 50+ operations.
</context_optimization>

<caching>
**Caching Strategies**:

```typescript
// TypeScript - LRU cache
import { LRUCache } from "lru-cache";

const cache = new LRUCache<string, any>({
  max: 500, // Maximum 500 items
  ttl: 1000 * 60 * 5, // 5 minute TTL
  updateAgeOnGet: true,
});

async function cachedApiCall(url: string) {
  // Check cache first
  const cached = cache.get(url);
  if (cached !== undefined) {
    logger.debug("Cache hit", { url });
    return cached;
  }

  // Fetch if not cached
  logger.debug("Cache miss", { url });
  const response = await fetch(url);
  const data = await response.json();

  // Store in cache
  cache.set(url, data);
  return data;
}
```

```python
# Python - Simple TTL cache
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Any, Dict, Tuple

class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl = timedelta(seconds=ttl_seconds)
        self.cache: Dict[str, Tuple[Any, datetime]] = {}

    def get(self, key: str) -> Any | None:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.ttl:
                return value
            del self.cache[key]
        return None

    def set(self, key: str, value: Any):
        self.cache[key] = (value, datetime.now())

cache = TTLCache(ttl_seconds=300)

async def cached_api_call(url: str) -> dict:
    # Check cache first
    cached = cache.get(url)
    if cached is not None:
        logger.debug("cache_hit", url=url)
        return cached

    # Fetch if not cached
    logger.debug("cache_miss", url=url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    # Store in cache
    cache.set(url, data)
    return data
```
</caching>

<connection_pooling>
**Connection Pooling**:

```typescript
// TypeScript - Database connection pooling
import { Pool } from "pg";

// Create pool once at startup
const pool = new Pool({
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // Maximum 20 connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Reuse connections from pool
async function queryDatabase(sql: string, params: any[]) {
  const client = await pool.connect();
  try {
    const result = await client.query(sql, params);
    return result.rows;
  } finally {
    client.release();
  }
}
```

```python
# Python - asyncpg connection pool
import asyncpg

# Create pool at startup
pool: asyncpg.Pool | None = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        min_size=5,
        max_size=20,
    )

async def query_database(sql: str, *params) -> list[dict]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(sql, *params)
        return [dict(row) for row in rows]

# Initialize in main
async def main():
    await init_db()
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())
    await pool.close()
```
</connection_pooling>

<async_concurrency>
**Async Concurrency**:

```typescript
// TypeScript - Concurrent operations
async function batchProcess(items: string[]) {
  // Process items concurrently (max 5 at a time)
  const results = [];

  for (let i = 0; i < items.length; i += 5) {
    const batch = items.slice(i, i + 5);
    const batchResults = await Promise.all(
      batch.map((item) => processItem(item))
    );
    results.push(...batchResults);
  }

  return results;
}
```

```python
# Python - Concurrent operations with semaphore
async def batch_process(items: list[str]) -> list[dict]:
    # Process items concurrently (max 5 at a time)
    semaphore = asyncio.Semaphore(5)

    async def process_with_semaphore(item: str):
        async with semaphore:
            return await process_item(item)

    tasks = [process_with_semaphore(item) for item in items]
    results = await asyncio.gather(*tasks)
    return results
```
</async_concurrency>

## Reliability

<retry_logic>
**Retry Logic with Exponential Backoff**:

```typescript
// TypeScript - Retry decorator
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }

      const delay = baseDelay * Math.pow(2, attempt);
      logger.warn("Retry attempt", {
        attempt: attempt + 1,
        maxRetries,
        delay,
        error: error instanceof Error ? error.message : "Unknown",
      });

      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw new Error("Unreachable");
}

// Usage
const result = await withRetry(() => fetch(url));
```

```python
# Python - Retry decorator
import asyncio
from functools import wraps
from typing import Callable, TypeVar

T = TypeVar('T')

def with_retry(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise

                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        "retry_attempt",
                        attempt=attempt + 1,
                        max_retries=max_retries,
                        delay=delay,
                        error=str(e),
                    )

                    await asyncio.sleep(delay)

            raise RuntimeError("Unreachable")

        return wrapper
    return decorator

# Usage
@with_retry(max_retries=3, base_delay=1.0)
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```
</retry_logic>

<health_checks>
**Health Checks**:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="health_check",
            description="Check server health and dependencies",
            inputSchema={"type": "object", "properties": {}},
        ),
        # ... other tools
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "health_check":
        health_status = await check_health()
        return [TextContent(
            type="text",
            text=json.dumps(health_status, indent=2)
        )]

async def check_health() -> dict:
    """Check health of server and dependencies."""
    checks = {
        "server": "ok",
        "database": "unknown",
        "external_api": "unknown",
    }

    # Check database
    try:
        await pool.fetchval("SELECT 1")
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"error: {e}"

    # Check external API
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config.api_url}/health", timeout=5) as response:
                if response.status == 200:
                    checks["external_api"] = "ok"
                else:
                    checks["external_api"] = f"error: HTTP {response.status}"
    except Exception as e:
        checks["external_api"] = f"error: {e}"

    return checks
```
</health_checks>

## Tool Design & Usability

<tool_descriptions>
**Writing Effective Tool Descriptions**:

Tool descriptions are critical - they determine whether Claude understands when and how to use your tools.

**Good vs Bad Descriptions**:

```typescript
// ❌ BAD: Vague, unclear when to use
{
  name: "search",
  description: "Search for things",
  // Claude doesn't know: What things? What format? When to use this?
}

// ✅ GOOD: Clear purpose, clear use case
{
  name: "search_github_repos",
  description: "Search GitHub repositories by keyword. Use when the user asks to find, discover, or search for GitHub projects. Returns repository name, description, stars, and URL.",
  // Claude knows: What it does, when to use it, what it returns
}
```

```python
# ❌ BAD: Technical jargon, unclear value
Tool(
    name="execute_query",
    description="Executes a SQL query against the database"
)

# ✅ GOOD: User benefit, clear constraints
Tool(
    name="get_user_orders",
    description="Retrieve all orders for a specific user by email address. Returns order ID, date, total, and status. Use when the user asks about their order history or purchase records."
)
```

**Description Best Practices**:

1. **Start with the action**: "Search GitHub...", "Create a calendar...", "Analyze sentiment..."
2. **Include the use case**: "Use when the user asks to..." or "Use this to..."
3. **Specify what it returns**: "Returns X, Y, Z"
4. **Mention important constraints**: "Maximum 100 results", "Requires API key", "Read-only"
5. **Use user language, not technical jargon**: "orders" not "transactional records"
6. **Be specific about data types**: "email address" not "user identifier"

**Naming Conventions**:

```typescript
// ✅ GOOD: Verb_noun format, clear and specific
"create_calendar_event"
"search_github_repos"
"analyze_sentiment"
"get_user_profile"

// ❌ BAD: Unclear, ambiguous, or too generic
"handle"  // Handle what?
"process"  // Process what?
"data"  // What data operation?
"execute"  // Execute what?
```

**Testing Descriptions with Claude**:

After writing descriptions, test them:
1. Ask Claude "what tools do you have?"
2. Give vague requests: "help me with GitHub"
3. Verify Claude selects the right tool
4. If wrong, improve description specificity

</tool_descriptions>

## Transport Selection

<transport_guide>
**Choosing the Right Transport**:

MCP supports three transport types. Choose based on your use case:

**1. stdio (Standard Input/Output)**

**Best for:**
- Claude Desktop integration
- CLI tools and scripts
- Simple request/response patterns
- Single-user, local execution

**Pros:**
- Simplest to implement
- No network configuration
- Works everywhere
- Built-in session management

**Cons:**
- No network access (local only)
- One client per server process
- No browser support

```json
{
  "command": "uv",
  "args": ["--directory", "/path/to/server", "run", "python", "server.py"]
}
```

**2. SSE (Server-Sent Events)**

**Best for:**
- Web applications
- Multiple concurrent clients
- Real-time updates to browser clients
- Read-heavy workloads

**Pros:**
- Browser-compatible
- Multiple clients per server
- Real-time streaming
- HTTP-based (works through proxies)

**Cons:**
- Requires HTTP server setup
- More complex than stdio
- One-way communication (server → client)

```python
mcp = FastMCP("My Server")

if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)
```

**3. Streamable HTTP**

**Best for:**
- RESTful APIs
- Browser-based clients
- Stateless or stateful sessions
- Enterprise deployments

**Pros:**
- Full HTTP flexibility
- Browser-compatible
- Stateful or stateless modes
- Load balancer friendly

**Cons:**
- Most complex setup
- Requires CORS configuration for browsers
- Session management overhead (stateful mode)

```python
# Stateful (maintains session state)
mcp = FastMCP("Stateful Service")
mcp.run(transport="streamable-http")

# Stateless (no session persistence, simpler)
mcp = FastMCP("Stateless Service", stateless_http=True)
mcp.run(transport="streamable-http")
```

**Decision Matrix**:

| Use Case | Recommended Transport |
|----------|----------------------|
| Claude Desktop only | stdio |
| Browser client | Streamable HTTP or SSE |
| Multiple concurrent users | Streamable HTTP |
| Real-time updates | SSE |
| Simple local tool | stdio |
| Enterprise deployment | Streamable HTTP (stateless) |
| WebSocket alternative | SSE |

</transport_guide>

## Debugging & Development

<mcp_inspector>
**Using MCP Inspector**:

The official MCP Inspector is essential for debugging during development.

```bash
# Install globally
npm install -g @modelcontextprotocol/inspector

# Run your server through the inspector
npx @modelcontextprotocol/inspector uv --directory /path/to/server run python server.py
```

**Inspector Features**:
- **Protocol visualization**: See all MCP messages in real-time
- **Tool testing**: Call tools with custom arguments
- **Resource browsing**: List and read resources
- **Request/response inspection**: Debug message payloads
- **Error tracking**: See exactly where failures occur

**Debugging Workflow**:

1. **Start with Inspector**: Always test new tools/resources through Inspector first
2. **Verify protocol compliance**: Check message formats match MCP spec
3. **Test edge cases**: Try invalid inputs, missing parameters
4. **Check error messages**: Ensure errors are clear and actionable
5. **Validate JSON schemas**: Confirm inputSchema works as expected
6. **Test with Claude Desktop**: Only after Inspector validation passes

</mcp_inspector>

<log_analysis>
**Effective Logging for Debugging**:

```typescript
// TypeScript - Structured logging with context
import winston from "winston";

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({ stream: process.stderr }),
  ],
});

// Log with context
logger.info("Tool called", {
  tool: "search_repos",
  args: { query: "machine learning" },
  user: request.context?.user,
  requestId: generateRequestId(),
});
```

```python
# Python - Debug mode with detailed tracing
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # IMPORTANT: stderr, not stdout
)

logger = logging.getLogger(__name__)

@mcp.tool()
async def search_repos(query: str) -> str:
    logger.debug(f"search_repos called with query: {query}")
    try:
        result = await perform_search(query)
        logger.debug(f"search_repos returned {len(result)} results")
        return result
    except Exception as e:
        logger.error(f"search_repos failed: {e}", exc_info=True)
        raise
```

**Claude Desktop Logs**:

```bash
# macOS
tail -f ~/Library/Logs/Claude/mcp-server-your-server-name.log

# Look for:
# - Server startup errors
# - Tool execution failures
# - Protocol errors
# - Dependency issues
```

**Common Debugging Patterns**:

1. **Tools not appearing**: Check `tools/list` handler and tool descriptions
2. **Tool calls failing**: Check input schema validation and error messages
3. **Server not starting**: Check dependencies, imports, and syntax errors
4. **Slow responses**: Add timing logs around expensive operations
5. **Intermittent failures**: Check for race conditions in async code

</log_analysis>

## Monitoring & Observability

<production_monitoring>
**Metrics Collection**:

Track key metrics for production MCP servers:

```typescript
// TypeScript - Prometheus metrics
import { Counter, Histogram, Registry } from "prom-client";

const registry = new Registry();

const toolCallsTotal = new Counter({
  name: "mcp_tool_calls_total",
  help: "Total number of tool calls",
  labelNames: ["tool_name", "status"],
  registers: [registry],
});

const toolDuration = new Histogram({
  name: "mcp_tool_duration_seconds",
  help: "Tool execution duration",
  labelNames: ["tool_name"],
  registers: [registry],
});

// Instrument tool calls
async function callTool(name: string, args: any) {
  const end = toolDuration.labels(name).startTimer();

  try {
    const result = await executeTool(name, args);
    toolCallsTotal.labels(name, "success").inc();
    return result;
  } catch (error) {
    toolCallsTotal.labels(name, "error").inc();
    throw error;
  } finally {
    end();
  }
}

// Expose metrics endpoint
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", registry.contentType);
  res.end(await registry.metrics());
});
```

```python
# Python - Custom metrics tracking
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict

@dataclass
class ToolMetrics:
    call_count: int = 0
    error_count: int = 0
    total_duration: float = 0.0

metrics = defaultdict(ToolMetrics)

@mcp.tool()
async def tracked_tool(args: str) -> str:
    """Tool with automatic metrics tracking."""
    start = datetime.now()
    tool_name = "tracked_tool"

    try:
        result = await perform_operation(args)
        metrics[tool_name].call_count += 1
        return result
    except Exception as e:
        metrics[tool_name].error_count += 1
        raise
    finally:
        duration = (datetime.now() - start).total_seconds()
        metrics[tool_name].total_duration += duration

# Expose metrics as a tool
@mcp.tool()
async def get_metrics() -> dict:
    """Get server metrics."""
    return {
        tool: {
            "calls": m.call_count,
            "errors": m.error_count,
            "avg_duration": m.total_duration / m.call_count if m.call_count > 0 else 0,
        }
        for tool, m in metrics.items()
    }
```

**Key Metrics to Track**:

- **Tool call count** (by tool name, by status)
- **Tool duration** (p50, p95, p99)
- **Error rate** (by tool, by error type)
- **Resource read count** (by URI pattern)
- **Active sessions** (for stateful servers)
- **Memory usage** (especially for long-running servers)
- **External API latency** (for wrapper MCPs)

**Alerting**:

Set up alerts for:
- Error rate > 5%
- p95 latency > 5 seconds
- Memory usage > 80%
- External API failures
- Server restarts/crashes

</production_monitoring>

## Documentation Standards

<readme_template>
**MCP Server README Template**:

Every MCP server should have a comprehensive README:

```markdown
# MCP Server Name

Brief description (one sentence).

## Features

- Feature 1 with specific benefit
- Feature 2 with specific benefit
- Feature 3 with specific benefit

## Installation

### Prerequisites

- Python 3.10+ / Node.js 18+
- Required API keys or credentials
- Any system dependencies

### Using uv (Recommended)

\```bash
# Development
uv run mcp dev server.py

# Claude Desktop
uv run mcp install server.py --name "Server Name"
\```

### Using pip

\```bash
pip install mcp-server-name

# Or from source
git clone https://github.com/user/mcp-server-name.git
cd mcp-server-name
uv sync
\```

## Configuration

### Claude Desktop

Add to `claude_desktop_config.json`:

\```json
{
  "mcpServers": {
    "server-name": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/server",
        "run",
        "python",
        "server.py"
      ],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
\```

### Environment Variables

- `API_KEY` (required): Your API key from [provider]
- `DEBUG` (optional): Set to `true` for debug logging
- `TIMEOUT` (optional): Request timeout in seconds (default: 30)

## Available Tools

### `tool_name`

Description of what this tool does and when to use it.

**Parameters:**
- `param1` (string, required): Description
- `param2` (number, optional): Description

**Returns:** Description of return value

**Example:**
\```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value",
    "param2": 42
  }
}
\```

## Available Resources

### `resource://uri/pattern/{param}`

Description of this resource and its data.

## Troubleshooting

### Server not starting

- Check that all dependencies are installed
- Verify API keys are set correctly
- Check server logs at `~/Library/Logs/Claude/mcp-server-name.log`

### Tool calls failing

- Verify input parameters match the schema
- Check API rate limits
- See debug logs with `DEBUG=true`

## Development

\```bash
# Run tests
uv run pytest

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/
\```

## License

MIT
```

</readme_template>

## Versioning & Lifecycle

<versioning_strategy>
**Semantic Versioning for MCP Servers**:

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes (removed tools, changed schemas, renamed parameters)
- **MINOR**: New features (new tools, new optional parameters)
- **PATCH**: Bug fixes (no API changes)

**Handling Breaking Changes**:

```typescript
// Version detection
const server = new Server({
  name: "my-server",
  version: "2.0.0",  // Incremented from 1.x
});

// Graceful deprecation
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "search_repos_v2",  // New tool
      description: "Search repositories (v2 with pagination)",
    },
    {
      name: "search_repos",  // Deprecated but still works
      description: "Search repositories (DEPRECATED: Use search_repos_v2)",
      deprecated: true,  // Signal to clients
    },
  ],
}));

// Version-aware handling
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "search_repos") {
    // Log deprecation warning
    logger.warn("Deprecated tool called", { tool: "search_repos" });

    // Still execute for backward compatibility
    return await handleLegacySearch(request.params.arguments);
  }

  if (request.params.name === "search_repos_v2") {
    return await handleNewSearch(request.params.arguments);
  }
});
```

**Migration Guides**:

When releasing breaking changes, provide migration guides:

```markdown
## Migrating from v1 to v2

### Breaking Changes

1. **Tool renamed**: `get_data` → `fetch_data`
   - **Before**: `get_data(id: string)`
   - **After**: `fetch_data(resource_id: string)`
   - **Migration**: Rename tool and parameter

2. **Schema change**: `search` now requires `query` parameter
   - **Before**: `search(terms: string)`
   - **After**: `search(query: string, filters?: object)`
   - **Migration**: Rename `terms` to `query`, add optional `filters`

3. **Removed tool**: `deprecated_tool`
   - **Alternative**: Use `new_tool` instead
   - **Migration**: See examples below

### Migration Examples

\```typescript
// v1
await callTool("get_data", { id: "123" });

// v2
await callTool("fetch_data", { resource_id: "123" });
\```
```

**Deprecation Timeline**:

1. **Version N**: Announce deprecation, keep functionality
2. **Version N+1**: Add warnings to logs
3. **Version N+2**: Remove deprecated features (MAJOR bump)

Maintain backward compatibility for at least 2 minor versions before breaking changes.

</versioning_strategy>

## Advanced Patterns

<multi_tenancy>
**Multi-Tenancy**:

Support multiple organizations/users in a single server:

```typescript
// TypeScript - Tenant isolation
interface TenantContext {
  tenantId: string;
  apiKey: string;
  config: TenantConfig;
}

class MultiTenantMCP {
  private tenants = new Map<string, TenantContext>();

  async loadTenant(tenantId: string): Promise<TenantContext> {
    // Load from database or config
    return {
      tenantId,
      apiKey: await getApiKey(tenantId),
      config: await getTenantConfig(tenantId),
    };
  }

  async handleToolCall(toolName: string, args: any, tenantId: string) {
    // Isolate by tenant
    const tenant = await this.loadTenant(tenantId);

    // Use tenant-specific API key
    const result = await externalAPI.call({
      apiKey: tenant.apiKey,
      config: tenant.config,
      ...args,
    });

    return result;
  }
}
```

```python
# Python - Tenant context per request
from contextvars import ContextVar

current_tenant = ContextVar("current_tenant", default=None)

@dataclass
class TenantContext:
    tenant_id: str
    api_key: str
    rate_limit: int

@mcp.tool()
async def tenant_aware_tool(query: str, ctx: Context) -> str:
    """Tool that respects tenant isolation."""
    # Extract tenant from request context
    tenant_id = ctx.request_context.metadata.get("tenant_id")
    tenant = await load_tenant(tenant_id)

    # Set tenant context for this request
    current_tenant.set(tenant)

    # Use tenant-specific configuration
    result = await external_api.query(
        query,
        api_key=tenant.api_key,
        rate_limit=tenant.rate_limit,
    )

    return result
```

**Key Considerations**:
- Isolate data by tenant ID
- Use tenant-specific API keys/credentials
- Enforce per-tenant rate limits
- Log with tenant context for debugging
- Consider database row-level security
- Test cross-tenant data leakage scenarios

</multi_tenancy>

<stateful_vs_stateless>
**Stateful vs Stateless Design**:

**Stateful Servers** (maintain session state):

```python
# Good for: Multi-step workflows, conversation context
mcp = FastMCP("Stateful Server")

# State persists across tool calls in same session
session_state = {}

@mcp.tool()
async def start_workflow(name: str, ctx: Context) -> str:
    """Start a multi-step workflow."""
    session_id = ctx.request_context.session_id
    session_state[session_id] = {
        "workflow_name": name,
        "step": 1,
        "data": {},
    }
    return f"Workflow '{name}' started"

@mcp.tool()
async def next_step(data: dict, ctx: Context) -> str:
    """Continue workflow with next step."""
    session_id = ctx.request_context.session_id
    state = session_state.get(session_id)

    if not state:
        return "Error: No active workflow"

    state["step"] += 1
    state["data"].update(data)
    return f"Step {state['step']} completed"
```

**Stateless Servers** (no session state):

```python
# Good for: Simple operations, horizontal scaling
mcp = FastMCP("Stateless Server", stateless_http=True)

@mcp.tool()
async def calculate(expression: str) -> float:
    """Pure function - no state needed."""
    return eval(expression)  # (Don't actually use eval!)

@mcp.tool()
async def fetch_data(id: str) -> dict:
    """Fetch from external source - no local state."""
    return await database.get(id)
```

**Decision Matrix**:

| Use Case | Recommendation |
|----------|---------------|
| Simple data fetching | Stateless |
| Multi-step workflows | Stateful |
| Need horizontal scaling | Stateless |
| Conversational context | Stateful |
| High traffic, simple ops | Stateless |
| Complex user sessions | Stateful |

</stateful_vs_stateless>

<idempotency>
**Idempotency for Safe Retries**:

Make operations safe to retry:

```typescript
// TypeScript - Idempotent operations
async function createResource(id: string, data: any) {
  // Check if already exists
  const existing = await database.findById(id);
  if (existing) {
    // Return existing instead of erroring
    return existing;
  }

  // Create only if doesn't exist
  return await database.create({ id, ...data });
}

// Idempotency keys for external APIs
async function chargePayment(amount: number, idempotencyKey: string) {
  return await stripe.charges.create(
    { amount, currency: "usd" },
    { idempotencyKey }  // Stripe handles duplicates
  );
}
```

```python
# Python - Idempotent tool with duplicate detection
@mcp.tool()
async def create_order(order_id: str, items: list[dict]) -> dict:
    """Create order (idempotent - safe to retry)."""
    # Check if already exists
    existing = await db.orders.find_one({"order_id": order_id})
    if existing:
        logger.info(f"Order {order_id} already exists, returning existing")
        return existing

    # Create only if doesn't exist
    order = await db.orders.insert_one({
        "order_id": order_id,
        "items": items,
        "created_at": datetime.now(),
    })

    return order
```

**Idempotency Patterns**:
- Use client-provided IDs (not auto-increment)
- Check-then-create with unique constraints
- Idempotency keys for external API calls
- Status checks before state changes
- Return existing result for duplicate requests

</idempotency>

<graceful_degradation>
**Graceful Degradation**:

Handle dependency failures gracefully:

```typescript
// TypeScript - Fallback strategies
async function searchWithFallback(query: string) {
  try {
    // Try primary search API
    return await primaryAPI.search(query);
  } catch (error) {
    logger.warn("Primary search failed, using fallback", { error });

    try {
      // Fallback to secondary API
      return await secondaryAPI.search(query);
    } catch (fallbackError) {
      // Return cached results if available
      const cached = await cache.get(`search:${query}`);
      if (cached) {
        logger.info("Returning cached results");
        return cached;
      }

      // Ultimate fallback: return partial results
      return {
        results: [],
        error: "Search temporarily unavailable",
        fallback: true,
      };
    }
  }
}
```

```python
# Python - Circuit breaker pattern
from datetime import datetime, timedelta

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure: datetime | None = None
        self.state = "closed"  # closed, open, half-open

    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            # Check if timeout elapsed
            if datetime.now() - self.last_failure > timedelta(seconds=self.timeout):
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func(*args, **kwargs)
            # Success - reset on half-open
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure = datetime.now()

            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                logger.error("Circuit breaker opened")

            raise

# Usage
breaker = CircuitBreaker(failure_threshold=3, timeout=60)

@mcp.tool()
async def fetch_with_protection(url: str) -> str:
    """Fetch with circuit breaker protection."""
    try:
        return await breaker.call(fetch_url, url)
    except Exception as e:
        # Return degraded response
        return f"Service temporarily unavailable: {e}"
```

**Degradation Strategies**:
- Primary → Fallback → Cache → Minimal response
- Circuit breakers for failing dependencies
- Timeouts on all external calls
- Partial results better than errors
- Clear error messages about degraded state

</graceful_degradation>

<cost_optimization>
**Cost Optimization for API Wrappers**:

Reduce costs when wrapping paid APIs:

```typescript
// TypeScript - Intelligent caching
class CostOptimizedAPI {
  private cache = new LRUCache({ max: 1000, ttl: 1000 * 60 * 5 });

  async query(params: QueryParams) {
    const cacheKey = JSON.stringify(params);

    // Check cache first
    const cached = this.cache.get(cacheKey);
    if (cached) {
      logger.info("Cache hit - saved API call", { params });
      return cached;
    }

    // Call expensive API
    const result = await expensiveAPI.call(params);

    // Cache for reuse
    this.cache.set(cacheKey, result);

    // Track cost
    await trackCost(params, estimatedCost(params));

    return result;
  }
}

// Request deduplication
class RequestDeduplicator {
  private pending = new Map();

  async deduplicate(key: string, fn: () => Promise<any>) {
    // Check if request already in flight
    if (this.pending.has(key)) {
      logger.info("Deduplicating request", { key });
      return await this.pending.get(key);
    }

    // Execute and share result
    const promise = fn();
    this.pending.set(key, promise);

    try {
      const result = await promise;
      return result;
    } finally {
      this.pending.delete(key);
    }
  }
}
```

```python
# Python - Batching for bulk operations
class BatchingAPI:
    def __init__(self, batch_size: int = 10, batch_delay: float = 0.1):
        self.batch_size = batch_size
        self.batch_delay = batch_delay
        self.pending_requests: list = []

    async def query(self, item_id: str) -> dict:
        """Query single item - automatically batched."""
        # Add to batch
        future = asyncio.Future()
        self.pending_requests.append((item_id, future))

        # Trigger batch if full
        if len(self.pending_requests) >= self.batch_size:
            await self._process_batch()

        # Wait for result
        return await future

    async def _process_batch(self):
        """Process batch of requests in single API call."""
        if not self.pending_requests:
            return

        batch = self.pending_requests[:]
        self.pending_requests.clear()

        # Single API call for entire batch
        item_ids = [item_id for item_id, _ in batch]
        results = await api.batch_get(item_ids)

        # Distribute results to futures
        for (item_id, future), result in zip(batch, results):
            future.set_result(result)

# Usage
batcher = BatchingAPI(batch_size=10)

@mcp.tool()
async def get_items(ids: list[str]) -> list[dict]:
    """Get multiple items (automatically batched)."""
    return await asyncio.gather(*[batcher.query(id) for id in ids])
```

**Cost Reduction Strategies**:
- Aggressive caching (with appropriate TTLs)
- Request deduplication (multiple requests → one API call)
- Batching (combine N requests → single batch call)
- Rate limiting (prevent runaway costs)
- Cost tracking and alerts
- Cheaper alternatives for non-critical data
- Partial results when possible (don't fetch everything)

</cost_optimization>

---

## Reference: Creation Workflow

# Automated MCP Server Creation Workflow

<overview>
This workflow creates a complete, working MCP server from scratch with zero manual configuration. Use this when Lex wants to build a new MCP server - it handles everything automatically.

**End state**: Server running in both Claude Code and Claude Desktop with all credentials configured.
</overview>

<workflow>

## Task Progress Checklist

Copy this and check off items as you complete them:

```
- [ ] Step 1: Gather requirements
- [ ] Step 2: Create project structure
- [ ] Step 3: Generate server code
- [ ] Step 4: Configure environment variables
- [ ] Step 5: Install in Claude Code
- [ ] Step 6: Install in Claude Desktop
- [ ] Step 7: Test and verify
```

---

## Step 1: Gather Requirements

Use AskUserQuestion to collect all information upfront:

```xml
<questions>
  <question>
    <header>Server Name</header>
    <question>What should this MCP server be called? (lowercase-with-hyphens)</question>
    <options>
      <option>
        <label>Suggest based on purpose</label>
        <description>I'll suggest a name after you describe what it does</description>
      </option>
      <option>
        <label>I have a name</label>
        <description>I know exactly what to call it</description>
      </option>
    </options>
    <multiSelect>false</multiSelect>
  </question>

  <question>
    <header>Language</header>
    <question>Which language should I use?</question>
    <options>
      <option>
        <label>Python</label>
        <description>Recommended for API integrations, data processing, most use cases</description>
      </option>
      <option>
        <label>TypeScript</label>
        <description>Better for Node.js integrations, when you need strict typing</description>
      </option>
    </options>
    <multiSelect>false</multiSelect>
  </question>

  <question>
    <header>Purpose</header>
    <question>What should this server do? What capabilities will it provide?</question>
    <options>
      <option>
        <label>API Integration</label>
        <description>Connect to external APIs (Stripe, Airtable, etc.)</description>
      </option>
      <option>
        <label>File Operations</label>
        <description>Read, write, process files on the filesystem</description>
      </option>
      <option>
        <label>Database Access</label>
        <description>Query and manage database records</description>
      </option>
      <option>
        <label>Custom Tools</label>
        <description>Specialized functions/calculations</description>
      </option>
    </options>
    <multiSelect>true</multiSelect>
  </question>

  <question>
    <header>Credentials</header>
    <question>What environment variables/API keys does this server need?</question>
    <options>
      <option>
        <label>API Keys</label>
        <description>External service API keys</description>
      </option>
      <option>
        <label>Database URL</label>
        <description>Database connection string</description>
      </option>
      <option>
        <label>None</label>
        <description>No credentials needed</description>
      </option>
    </options>
    <multiSelect>true</multiSelect>
  </question>
</questions>
```

**After gathering requirements:**
- If server name wasn't provided, suggest one based on purpose
- Confirm the name: `{purpose}-mcp` (e.g., "stripe-mcp", "notion-mcp")
- List out all environment variables that will be needed
- **Determine architecture based on operation count:**
  - **1-2 operations:** Traditional architecture (flat tools)
  - **3+ operations:** On-demand discovery architecture (meta-tools + resources)
  - Explain: "I'll use on-demand discovery to minimize context usage - this means only loading operation schemas when needed instead of all upfront."

---

## Step 2: Create Project Structure

Execute these commands to set up the project:

**For Python:**
```bash
# Create directory
mkdir -p ~/Developer/mcp/{server-name}/src
cd ~/Developer/mcp/{server-name}

# Initialize project
uv init

# Add dependencies
uv add mcp

# If API integration, add requests
uv add httpx

# Create .gitignore
cat > .gitignore << 'EOF'
.env
.venv/
__pycache__/
*.pyc
.DS_Store
EOF

# Create README template
cat > README.md << 'EOF'
# {Server Name} MCP Server

## Description
{What this server does}

## Setup
1. Install: `uv sync`
2. Configure environment variables in ~/.zshrc
3. Run: `uv run python -m src.server`

## Environment Variables
{List of required env vars}
EOF
```

**For TypeScript:**
```bash
# Create directory
mkdir -p ~/Developer/mcp/{server-name}/src
cd ~/Developer/mcp/{server-name}

# Initialize npm project
npm init -y

# Add dependencies
npm install @modelcontextprotocol/sdk

# If API integration
npm install axios

# Create tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./build",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
.env
node_modules/
build/
.DS_Store
EOF

# Create README
cat > README.md << 'EOF'
# {Server Name} MCP Server

## Description
{What this server does}

## Setup
1. Install: `npm install`
2. Build: `npm run build`
3. Configure environment variables in ~/.zshrc
4. Run: `node build/index.js`

## Environment Variables
{List of required env vars}
EOF
```

**Verify structure created:**
```bash
ls -la ~/Developer/mcp/{server-name}/
```

---

## Step 3: Generate Server Code

Write the server implementation based on requirements and chosen architecture.

### Architecture Decision

**If 1-2 operations:** Use traditional template below
**If 3+ operations:** Use on-demand discovery template (see [references/large-api-pattern.md](large-api-pattern.md) for complete implementation)

---

### Traditional Architecture Template (1-2 Operations)

**Python Template (API Integration):**

```python
# src/server.py
import os
import sys
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration
API_KEY = os.getenv("{ENV_VAR_NAME}")
if not API_KEY:
    print("ERROR: {ENV_VAR_NAME} environment variable not set", file=sys.stderr)
    sys.exit(1)

BASE_URL = "{api_base_url}"

app = Server("{server-name}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="{tool_name}",
            description="{What this tool does}",
            inputSchema={
                "type": "object",
                "properties": {
                    "{param_name}": {
                        "type": "string",
                        "description": "{Parameter description}"
                    }
                },
                "required": ["{param_name}"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool."""
    try:
        if name == "{tool_name}":
            param = arguments["{param_name}"]

            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BASE_URL}/{endpoint}",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    params={"param": param}
                )
                response.raise_for_status()
                data = response.json()

            return [TextContent(
                type="text",
                text=f"Result: {data}"
            )]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        print(f"Error in {name}: {e}", file=sys.stderr)
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

**TypeScript Template (API Integration):**

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";

const API_KEY = process.env.{ENV_VAR_NAME};
if (!API_KEY) {
  console.error("ERROR: {ENV_VAR_NAME} environment variable not set");
  process.exit(1);
}

const BASE_URL = "{api_base_url}";

const server = new Server(
  { name: "{server-name}", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "{tool_name}",
      description: "{What this tool does}",
      inputSchema: {
        type: "object",
        properties: {
          {param_name}: {
            type: "string",
            description: "{Parameter description}"
          }
        },
        required: ["{param_name}"]
      }
    }
  ]
}));

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "{tool_name}") {
      const param = args.{param_name};

      const response = await axios.get(`${BASE_URL}/{endpoint}`, {
        headers: { Authorization: `Bearer ${API_KEY}` },
        params: { param }
      });

      return {
        content: [
          {
            type: "text",
            text: `Result: ${JSON.stringify(response.data)}`
          }
        ]
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    console.error(`Error in ${name}:`, error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`
        }
      ]
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

**Customize the template:**
- Replace `{server-name}`, `{tool_name}`, `{ENV_VAR_NAME}` with actual values
- Add multiple tools if needed
- Implement specific API logic based on requirements
- Add proper error handling for the specific API

---

### On-Demand Discovery Architecture (3+ Operations)

**Why:** Minimizes context usage by loading operation schemas only when needed.

**Implementation:** Follow the complete guide in [references/large-api-pattern.md](large-api-pattern.md) which includes:

1. **4 Meta-Tools Pattern:**
   - `discover` - Browse available operations
   - `get_schema` - Get parameters for one operation
   - `execute` - Run an operation
   - `continue` - Handle pagination

2. **Operations JSON File:** All operation definitions in `operations.json` (not hardcoded in Python)

3. **MCP Resources:** Operations exposed as resources with URIs like `{server}://operations/{category}/{action}`

4. **Smart Dispatch:** Maps operation strings to actual implementations

**Quick reference for on-demand architecture:**
```python
# The 4 meta-tools handle everything
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="discover", ...),
        Tool(name="get_schema", ...),
        Tool(name="execute", ...),
        Tool(name="continue", ...)
    ]

# Operations stored as MCP resources
@app.list_resources()
async def list_resources() -> list[Resource]:
    # Load from operations.json
    # Expose as resources
```

**See large-api-pattern.md for:**
- Complete Python implementation
- TypeScript implementation
- Operations JSON schema
- Dispatch layer implementation
- Testing and debugging

---

### Write the Generated Code

```bash
# For Python
cat > ~/Developer/mcp/{server-name}/src/server.py << 'EOF'
{generated code}
EOF

# For TypeScript (then build)
cat > ~/Developer/mcp/{server-name}/src/index.ts << 'EOF'
{generated code}
EOF
npm run build
```

---

## Step 4: Configure Environment Variables

**SECURITY CRITICAL:** NEVER ask Lex to paste secrets into chat. Secrets must never go through Anthropic's servers or appear in conversation history.

### Provide Exact Commands

For each required environment variable, give Lex the exact commands to run in his terminal.

**Step 4.1: Show required variables and where to get them**

Present to Lex:
```
📋 Required Environment Variables:

{ENV_VAR_NAME_1} - {Description}
  Get it from: {URL or instructions}

{ENV_VAR_NAME_2} - {Description}
  Get it from: {URL or instructions}
```

**Step 4.2: Give exact commands to add to ~/.zshrc**

```
Run these commands in your terminal:

# Add {Server Name} credentials
cat >> ~/.zshrc << 'EOF'

# {Server Name} MCP Server
export {ENV_VAR_NAME_1}="your-value-here"
export {ENV_VAR_NAME_2}="your-value-here"
EOF

# Reload shell
source ~/.zshrc
```

**Step 4.3: Wait for confirmation**

Ask using AskUserQuestion:
```xml
<question>
  <header>Environment Setup</header>
  <question>Have you added the environment variables to ~/.zshrc?</question>
  <options>
    <option>
      <label>Yes, added and sourced</label>
      <description>Variables are ready</description>
    </option>
    <option>
      <label>Skip for now</label>
      <description>I'll add them later</description>
    </option>
  </options>
  <multiSelect>false</multiSelect>
</question>
```

**Step 4.4: Verify variables exist (without showing values)**

```bash
# Check each variable is set (without printing values)
for var in {ENV_VAR_1} {ENV_VAR_2}; do
  if [ -z "${!var}" ]; then
    echo "✗ $var not set - please add to ~/.zshrc and run: source ~/.zshrc"
  else
    echo "✓ $var is set"
  fi
done
```

**Important notes:**
- Variables are checked for existence only (not values)
- Values never appear in conversation or output
- If variables aren't set, stop and wait for Lex to add them

---

## Step 5: Install in Claude Code

```bash
# Get absolute path to uv (for Python) or node (for TypeScript)
UV_PATH=$(which uv)
NODE_PATH=$(which node)

# Build environment flags
ENV_FLAGS=""
for var in {ENV_VAR1} {ENV_VAR2}; do
  ENV_FLAGS+="--env $var=\${$var} "
done

# Install based on language
if [ "{language}" = "Python" ]; then
  claude mcp add --transport stdio {server-name} \
    $ENV_FLAGS \
    -- uv --directory ~/Developer/mcp/{server-name} run python -m src.server
else
  claude mcp add --transport stdio {server-name} \
    $ENV_FLAGS \
    -- node ~/Developer/mcp/{server-name}/build/index.js
fi

# Verify installation
claude mcp list | grep {server-name}
```

**Expected output:**
```
{server-name}: ... - ✓ Connected
```

---

## Step 6: Install in Claude Desktop

```bash
# Get paths
UV_PATH=$(which uv)
NODE_PATH=$(which node)
DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Backup config
cp "$DESKTOP_CONFIG" "$DESKTOP_CONFIG.backup.$(date +%s)"

# Create server config based on language
if [ "{language}" = "Python" ]; then
  SERVER_CONFIG=$(cat <<EOF
{
  "command": "$UV_PATH",
  "args": ["--directory", "$HOME/Developer/mcp/{server-name}", "run", "python", "-m", "src.server"],
  "env": {
    {env_json}
  }
}
EOF
)
else
  SERVER_CONFIG=$(cat <<EOF
{
  "command": "$NODE_PATH",
  "args": ["$HOME/Developer/mcp/{server-name}/build/index.js"],
  "env": {
    {env_json}
  }
}
EOF
)
fi

# Add to config using jq
jq --arg name "{server-name}" \
   --argjson config "$SERVER_CONFIG" \
   '.mcpServers[$name] = $config' \
   "$DESKTOP_CONFIG" > "$DESKTOP_CONFIG.tmp"

mv "$DESKTOP_CONFIG.tmp" "$DESKTOP_CONFIG"

echo "✓ Installed in Claude Desktop"
echo "⚠️  IMPORTANT: Restart Claude Desktop for changes to take effect"
```

**Generate env_json from environment variables:**
```bash
# For each env var, create JSON entry
{
  "ENV_VAR1": "${ENV_VAR1}",
  "ENV_VAR2": "${ENV_VAR2}"
}
```

---

## Step 7: Test and Verify

**Test the server standalone:**
```bash
cd ~/Developer/mcp/{server-name}

# For Python
uv run python -m src.server

# For TypeScript
node build/index.js

# Should wait for input (stdio mode)
# Press Ctrl+C to exit
```

**Verify in Claude Code:**
```bash
# Check server appears
claude mcp list

# Check logs (if there are issues)
tail -50 ~/Library/Logs/Claude/mcp-server-{server-name}.log
```

**Verify in Claude Desktop:**
1. Restart Claude Desktop
2. Open new conversation
3. Try using a tool from the server
4. Check it works

**Final checklist:**
```
- [ ] Server appears in `claude mcp list` with ✓ Connected
- [ ] Environment variables are set in ~/.zshrc
- [ ] Server added to Claude Desktop config
- [ ] Test tool call succeeds
- [ ] No errors in logs
```

</workflow>

<validation>

## Validation After Each Step

**Step 2 validation:**
```bash
# Verify directory exists
test -d ~/Developer/mcp/{server-name} && echo "✓ Directory created" || echo "✗ Directory missing"

# Verify files exist
test -f ~/Developer/mcp/{server-name}/pyproject.toml && echo "✓ Project initialized" || echo "✗ Project not initialized"
```

**Step 3 validation:**
```bash
# Verify server file exists
test -f ~/Developer/mcp/{server-name}/src/server.py && echo "✓ Server code created" || echo "✗ Server code missing"

# For Python: Check syntax
cd ~/Developer/mcp/{server-name}
python -m py_compile src/server.py && echo "✓ Syntax valid" || echo "✗ Syntax error"

# For TypeScript: Check build
npm run build && echo "✓ Build successful" || echo "✗ Build failed"
```

**Step 4 validation:**
```bash
# Verify env vars are set
for var in {ENV_VAR1} {ENV_VAR2}; do
  if [ -z "${!var}" ]; then
    echo "✗ $var not set"
  else
    echo "✓ $var set"
  fi
done
```

**Step 5 validation:**
```bash
# Check Claude Code installation
claude mcp list | grep -q "{server-name}" && echo "✓ Installed in Claude Code" || echo "✗ Not installed"
```

**Step 6 validation:**
```bash
# Check Claude Desktop config
jq '.mcpServers | has("{server-name}")' "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
# Should output: true
```

**Step 7 validation:**
```bash
# Check server health
claude mcp list | grep "{server-name}"
# Should show: ✓ Connected
```

</validation>

<troubleshooting>

## Common Issues During Creation

**"uv: command not found":**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload shell
source ~/.zshrc
```

**"Environment variable not set":**
```bash
# Check if in ~/.zshrc
grep "ENV_VAR_NAME" ~/.zshrc

# If missing, add manually
echo 'export ENV_VAR_NAME="value"' >> ~/.zshrc
source ~/.zshrc
```

**"Server not appearing in Claude Code":**
```bash
# Check installation
claude mcp list

# Check logs
tail -50 ~/Library/Logs/Claude/mcp-server-{server-name}.log

# Reinstall
claude mcp remove {server-name}
# Then repeat Step 5
```

**"jq: command not found":**
```bash
# Install jq
brew install jq
```

**"Syntax error in server code":**
```bash
# For Python
cd ~/Developer/mcp/{server-name}
python -m py_compile src/server.py
# Fix errors shown

# For TypeScript
npm run build
# Fix TypeScript errors shown
```

</troubleshooting>

<notes>

## Important Notes

**Always use absolute paths:**
- Find with: `which uv`, `which node`
- Claude Desktop requires absolute paths

**Environment variable security:**
- Never hardcode secrets in code
- Always use `${VAR}` expansion in configs
- Store in ~/.zshrc for persistence

**Testing first:**
- Always test standalone before installing
- Check logs if server doesn't connect
- Verify env vars are actually set

**Backup before modifying:**
- Claude Desktop config is backed up automatically
- Can restore with: `cp claude_desktop_config.json.backup.<timestamp> claude_desktop_config.json`

</notes>

---

## Reference: Large Api Pattern

# Resources-Based MCP Server Pattern

<overview>
**Achieving 98% Context Reduction Through On-Demand Operation Loading**

When wrapping large APIs (50+ operations) in MCP servers, traditional architecture consumes 15,000-30,000 tokens just loading tool definitions. This pattern reduces that overhead to ~300 tokens while maintaining full functionality.

This guide explains the architectural pattern used in production servers to achieve 90-98% context reduction.
</overview>

## The Problem

<traditional_architecture>
**Traditional MCP Server Architecture**

Most MCP servers expose operations as individual tools:

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="operation_1", description="...", inputSchema={...}),
        Tool(name="operation_2", description="...", inputSchema={...}),
        Tool(name="operation_3", description="...", inputSchema={...}),
        # ... 78 more tools
    ]
```

**Problem:** Every tool definition is sent to Claude on every conversation start, consuming massive context before any actual work begins.

**Real metrics with 81 operations:**
- Tool definitions: ~15,000 tokens
- Context available for conversation: 185,000 tokens (200k - 15k)
- Overhead: 7.5% of available context wasted on metadata

For APIs with 100+ operations, this can consume 20,000-30,000 tokens or more.
</traditional_architecture>

## The Solution

<resources_based_architecture>
**Resources-Based Architecture**

Instead of loading all tools upfront, expose a minimal set of **meta-tools** for discovery and execution, with operation schemas stored as **MCP resources** that are loaded on-demand.

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="discover", description="Browse available operations"),
        Tool(name="get_schema", description="Get operation parameters"),
        Tool(name="execute", description="Execute an operation"),
        Tool(name="continue", description="Paginate large responses")
    ]
```

**Result:** Only 4 tool definitions loaded upfront (~300 tokens), with 81 operation schemas available as resources.
</resources_based_architecture>

## How It Works

<meta_tools_layer>
### Meta-Tools Layer

Four tools handle all interactions:

**`discover` - Operation Discovery**
```python
Tool(
    name="circle_discover",
    description="Browse all available Circle operations organized by category",
    inputSchema={"type": "object", "properties": {}}
)
```
Returns hierarchical tree of all available operations.

**`get_schema` - Schema Retrieval**
```python
Tool(
    name="circle_get_schema",
    description="Get detailed schema for a specific operation",
    inputSchema={
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "Operation identifier (e.g., 'posts.create')"
            }
        }
    }
)
```
Returns full parameter schema for one operation.

**`execute` - Operation Execution**
```python
Tool(
    name="circle_execute",
    description="Execute a Circle operation with parameters",
    inputSchema={
        "type": "object",
        "properties": {
            "operation": {"type": "string"},
            "params": {"type": "object"}
        }
    }
)
```
Routes to actual implementation based on operation string.

**`continue` - Pagination**
```python
Tool(
    name="circle_continue",
    description="Continue retrieving paginated results",
    inputSchema={
        "type": "object",
        "properties": {
            "session_id": {"type": "string"}
        }
    }
)
```
Handles chunked responses for large datasets.
</meta_tools_layer>

<operations_schema>
### Operations Schema File

All operation definitions live in `operations.json`:

```json
{
  "operations": {
    "posts": {
      "list": {
        "name": "circle_list_posts",
        "description": "List posts in Circle",
        "inputSchema": {
          "type": "object",
          "properties": {
            "space_id": {"type": "integer"},
            "page": {"type": "integer"},
            "per_page": {"type": "integer"}
          }
        }
      },
      "create": {
        "name": "circle_create_post",
        "description": "Create a new post",
        "inputSchema": { ... }
      }
    },
    "members": { ... },
    "events": { ... }
  }
}
```
</operations_schema>

<mcp_resources>
### MCP Resources API

Operations are exposed as resources with hierarchical URIs:

```python
@server.list_resources()
async def list_resources() -> list[Resource]:
    resources = []

    # Index resource (full tree)
    resources.append(Resource(
        uri="circle://operations/index",
        name="Operations Index",
        description="Complete tree of all operations"
    ))

    # Category resources
    for category in OPERATIONS.keys():
        resources.append(Resource(
            uri=f"circle://operations/{category}",
            name=f"{category} Operations"
        ))

    # Individual operations
    for category, actions in OPERATIONS.items():
        for action, schema in actions.items():
            resources.append(Resource(
                uri=f"circle://operations/{category}/{action}",
                name=schema["name"],
                description=schema["description"]
            ))

    return resources
```

**Claude can:**
- Browse `circle://operations/index` to see all operations
- Read `circle://operations/posts/create` to get schema
- Never loads operations it doesn't use in a conversation
</mcp_resources>

<operation_dispatch>
### Operation Dispatch

Map operation strings to actual implementations:

```python
def _operation_to_tool_name(operation: str) -> str:
    """Convert 'posts.create' -> 'circle_create_post'"""
    parts = operation.split(".")
    category, action = parts
    return f"circle_{action}_{category.rstrip('s')}"

def _get_tool_handlers(client):
    """Build dispatch dictionary"""
    return {
        "circle_list_posts": client.list_posts,
        "circle_create_post": client.create_post,
        "circle_get_post": client.get_post,
        # ... all other operations
    }

@server.call_tool()
async def call_tool(name: str, arguments: Any):
    if name == "circle_execute":
        operation = arguments["operation"]
        params = arguments["params"]

        # Convert operation string to handler
        tool_name = _operation_to_tool_name(operation)
        handlers = _get_tool_handlers(client)
        handler = handlers[tool_name]

        # Execute
        result = await handler(**params)
        return [TextContent(type="text", text=json.dumps(result))]
```
</operation_dispatch>

## Implementation Guide

<step_1>
### Step 1: Design Your Operation Namespace

Organize operations hierarchically:

```
posts/
  ├── list
  ├── create
  ├── get
  ├── update
  └── delete
members/
  ├── list
  ├── create
  └── search
batch/
  ├── posts/
  │   └── delete
  └── members/
      └── create
```
</step_1>

<step_2>
### Step 2: Extract Tool Definitions to JSON

Move all tool schemas from code to data:

**Before (in Python):**
```python
Tool(
    name="circle_create_post",
    description="Create a new post",
    inputSchema={
        "type": "object",
        "properties": {
            "space_id": {"type": "integer"},
            "name": {"type": "string"},
            "body": {"type": "string"}
        },
        "required": ["space_id", "name", "body"]
    }
)
```

**After (in operations.json):**
```json
{
  "operations": {
    "posts": {
      "create": {
        "name": "circle_create_post",
        "description": "Create a new post",
        "inputSchema": {
          "type": "object",
          "properties": {
            "space_id": {"type": "integer"},
            "name": {"type": "string"},
            "body": {"type": "string"}
          },
          "required": ["space_id", "name", "body"]
        }
      }
    }
  }
}
```
</step_2>

<step_3>
### Step 3: Implement Meta-Tools

Create the 4 core meta-tools (see [Meta-Tools Layer](#meta_tools_layer) above).
</step_3>

<step_4>
### Step 4: Build Operation Dispatcher

```python
def _get_tool_handlers(client):
    """Map operation names to actual implementations"""
    return {
        "your_operation_1": client.method_1,
        "your_operation_2": client.method_2,
        # ... all operations
    }

def _operation_to_tool_name(operation: str) -> str:
    """Convert 'category.action' to 'your_operation_name'"""
    # Your naming convention logic
    pass

@server.call_tool()
async def call_tool(name: str, arguments: Any):
    if name == "your_execute":
        operation = arguments["operation"]
        params = arguments["params"]

        tool_name = _operation_to_tool_name(operation)
        handlers = _get_tool_handlers(client)
        handler = handlers[tool_name]

        return await handler(**params)
```
</step_4>

<step_5>
### Step 5: Expose as MCP Resources

```python
@server.list_resources()
async def list_resources() -> list[Resource]:
    resources = []
    for category, actions in OPERATIONS.items():
        for action, schema in actions.items():
            resources.append(Resource(
                uri=f"yourapp://operations/{category}/{action}",
                name=schema["name"],
                description=schema["description"]
            ))
    return resources

@server.read_resource()
async def read_resource(uri: str) -> str:
    # Parse URI and return operation schema
    category, action = parse_uri(uri)
    schema = OPERATIONS[category][action]
    return json.dumps(schema, indent=2)
```
</step_5>

<step_6>
### Step 6: Add Pagination (Optional)

For large responses (>20k tokens), implement chunking:

```python
def chunk_by_tokens(data: dict, chunk_size: int = 15000) -> list[dict]:
    """Split large responses into chunks"""
    if 'data' not in data:
        return [data]

    items = data['data']
    chunks = []
    current_chunk = []
    current_tokens = 0

    for item in items:
        item_tokens = estimate_tokens(item)
        if current_tokens + item_tokens > chunk_size:
            chunks.append({'data': current_chunk})
            current_chunk = [item]
            current_tokens = item_tokens
        else:
            current_chunk.append(item)
            current_tokens += item_tokens

    if current_chunk:
        chunks.append({'data': current_chunk})

    return chunks
```
</step_6>

## Trade-offs

<advantages>
### Advantages

✅ **Massive context savings** (90-98% reduction)
✅ **Scales to any number of operations** (100, 200, 500+ operations)
✅ **Cleaner code** (schemas in data, not code)
✅ **Easy to maintain** (add operations by editing JSON)
✅ **Better for LLMs** (only loads relevant operations per conversation)
</advantages>

<disadvantages>
### Disadvantages

❌ **Extra discovery step** (Claude must call `discover` or `get_schema` first)
❌ **More complex implementation** (dispatch layer, resources API)
❌ **Slightly slower first call** (needs to fetch schema before executing)
❌ **Not ideal for < 20 operations** (overhead not worth it)
</disadvantages>

<performance_characteristics>
### Performance Characteristics

**First operation in conversation:**
1. Claude calls `discover` to browse operations (~300 tokens response)
2. Claude calls `get_schema` for specific operation (~200 tokens response)
3. Claude calls `execute` with parameters
4. Total: 3 tool calls vs 1 in traditional approach

**Subsequent operations:**
1. Claude already knows operations, just calls `execute`
2. Total: 1 tool call (same as traditional)

**Net result:** Small overhead on first operation, massive context savings overall.
</performance_characteristics>

## When to Use This Pattern

<use_when>
### ✅ Use resources-based architecture when:

- **You have 3+ operations** - Context is precious at every scale, not just large APIs
- **Operations are grouped logically** - Natural hierarchy exists (CRUD, categories)
- **Not all operations used per conversation** - Most conversations only use 2-5 operations
- **Context window is precious** - You need maximum space for actual conversation
- **Operations change frequently** - Easier to maintain in JSON than code

**Updated threshold: Use on-demand discovery for ANY MCP server with 3+ operations.**

Traditional wisdom says "only for 20+ operations," but context efficiency matters at every scale. Even 40% savings (200-500 tokens) compounds across conversations when:
- Conversations span many turns
- Multiple MCP servers are loaded
- Working with large codebases
- Every token counts toward the 200k context window
</use_when>

<dont_use_when>
### ❌ Stick with traditional tools when:

- **You have 1-2 operations only** - Overhead not worth the complexity
- **All operations used in most conversations** - No benefit to on-demand loading
- **Simplicity is priority** - Traditional approach is easier to understand
</dont_use_when>

## Context Savings by Operation Count

| Operations | Traditional | On-Demand | Savings | % Saved |
|------------|-------------|-----------|---------|---------|
| 1-2        | ~200        | ~300      | -100    | -50%    |
| 3          | ~300        | ~300      | 0       | 0%      |
| 5          | ~500        | ~300      | 200     | 40%     |
| 10         | ~1,000      | ~300      | 700     | 70%     |
| 15         | ~1,500      | ~300      | 1,200   | 80%     |
| 50         | ~5,000      | ~300      | 4,700   | 94%     |
| 100        | ~10,000     | ~300      | 9,700   | 97%     |

**Threshold: 3+ operations → use on-demand discovery pattern**

## Real-World Results

<circle_mcp_metrics>
### Circle MCP Server Metrics

**Before (tools-based v1):**
- 81 tool definitions loaded upfront
- ~15,000 tokens consumed
- Context available: 185,000 tokens
- Overhead: 7.5%

**After (resources-based v2):**
- 4 meta-tools loaded upfront
- ~300 tokens consumed
- Context available: 199,700 tokens
- Overhead: 0.15%
- **Savings: 98% context reduction**
</circle_mcp_metrics>

<typical_conversation>
### Typical Conversation Pattern

**Conversation using 3 operations:**

Traditional approach:
- Load 81 tools: 15,000 tokens
- Use 3 operations: 0 tokens (already loaded)
- **Total overhead: 15,000 tokens**

Resources-based approach:
- Load 4 meta-tools: 300 tokens
- Discover operations: 300 tokens (first time only)
- Get 3 schemas: 600 tokens (200 each, first time only)
- Execute 3 operations: 0 tokens (dispatch only)
- **Total overhead: 1,200 tokens**

**Savings: 92% even with discovery overhead**
</typical_conversation>

## Example: Building a GitHub MCP Server

<github_example>
Let's apply this pattern to a hypothetical GitHub API server with 50+ operations:

**1. Design Namespace**

```
repos/
  ├── list
  ├── create
  ├── get
  └── delete
issues/
  ├── list
  ├── create
  ├── update
  └── close
pulls/
  ├── list
  ├── create
  ├── merge
  └── review
actions/
  ├── list_workflows
  ├── trigger_workflow
  └── get_run
```

**2. Create operations.json**

```json
{
  "operations": {
    "repos": {
      "list": {
        "name": "github_list_repos",
        "description": "List repositories for authenticated user",
        "inputSchema": {
          "type": "object",
          "properties": {
            "type": {
              "type": "string",
              "enum": ["all", "owner", "member"]
            },
            "sort": {
              "type": "string",
              "enum": ["created", "updated", "pushed", "full_name"]
            }
          }
        }
      },
      "create": {
        "name": "github_create_repo",
        "description": "Create a new repository",
        "inputSchema": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "private": {"type": "boolean"}
          },
          "required": ["name"]
        }
      }
    },
    "issues": { ... },
    "pulls": { ... }
  }
}
```

**3. Implement Meta-Tools**

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="github_discover",
            description="Browse all GitHub operations",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="github_get_schema",
            description="Get schema for a GitHub operation",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "e.g., 'repos.create', 'issues.list'"
                    }
                },
                "required": ["operation"]
            }
        ),
        Tool(
            name="github_execute",
            description="Execute a GitHub operation",
            inputSchema={
                "type": "object",
                "properties": {
                    "operation": {"type": "string"},
                    "params": {"type": "object"}
                },
                "required": ["operation", "params"]
            }
        )
    ]
```

**4. Build Dispatcher**

```python
def _operation_to_method(operation: str) -> str:
    """Convert 'repos.create' to 'github_create_repo'"""
    category, action = operation.split(".")
    return f"github_{action}_{category.rstrip('s')}"

def _get_handlers(client):
    return {
        "github_list_repos": client.list_repos,
        "github_create_repo": client.create_repo,
        "github_list_issues": client.list_issues,
        # ... all operations
    }

@server.call_tool()
async def call_tool(name: str, arguments: Any):
    if name == "github_execute":
        operation = arguments["operation"]
        params = arguments["params"]

        method = _operation_to_method(operation)
        handlers = _get_handlers(github_client)
        handler = handlers[method]

        result = await handler(**params)
        return [TextContent(type="text", text=json.dumps(result))]
```

**Results**

**50 operations:**
- Traditional: ~8,500 tokens overhead
- Resources-based: ~300 tokens overhead
- **Savings: 96.5%**
</github_example>

## Summary

<conclusion>
The resources-based MCP pattern achieves dramatic context reduction by:

1. **Lazy loading** - Only fetch operation schemas when needed
2. **Meta-tools** - Minimal upfront tool definitions for discovery/execution
3. **MCP resources** - Leverage MCP's resource API for on-demand schema retrieval
4. **Smart dispatch** - Route operation strings to implementations

**When you have 20+ operations, this pattern can save 90-98% of context overhead while maintaining full functionality.**

Use this pattern to build efficient, scalable MCP servers that preserve precious context window for actual conversation.
</conclusion>

---

## Reference: Oauth Implementation

# OAuth Implementation for MCP Servers

<critical_pattern>
**Why this matters:** OAuth libraries write to stdout/stderr, which corrupts MCP's JSON-RPC protocol. MCP servers also run headless (no terminal/browser access) making standard OAuth flows impossible.

**Both patterns below are MANDATORY for any MCP server using OAuth.**
</critical_pattern>

## Pattern 1: stdout/stderr Isolation

<the_problem>
MCP uses JSON-RPC over stdio. OAuth libraries print authorization prompts to stdout/stderr:

```
User authentication requires interaction with your web browser...
Go to the following URL: https://accounts.spotify.com/authorize?...
```

This text corrupts the JSON-RPC protocol, causing errors like:
```
Unexpected token 'G', "Go to the "... is not valid JSON
```
</the_problem>

<the_solution>
Wrap ALL OAuth operations with stdout/stderr redirection:

```python
import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

def get_api_client():
    """Initialize OAuth client with stdio isolation."""
    stderr_capture = StringIO()
    stdout_capture = StringIO()

    with redirect_stderr(stderr_capture), redirect_stdout(stdout_capture):
        # OAuth initialization happens in isolation
        auth_manager = OAuthProvider(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            redirect_uri=os.environ.get("REDIRECT_URI"),
            scope=SCOPE,
            open_browser=False  # Never open browser in MCP server
        )
        client = APIClient(auth_manager=auth_manager)

    # Log captured output to logger (not stdout)
    if stderr_capture.getvalue():
        logger.info(f"OAuth stderr: {stderr_capture.getvalue()}")
    if stdout_capture.getvalue():
        logger.info(f"OAuth stdout: {stdout_capture.getvalue()}")

    return client
```

**Apply to EVERY operation that might trigger token refresh:**

```python
def _execute_operation(operation: str, params: dict) -> Any:
    """Execute API operation with stdio isolation."""
    global client

    stderr_capture = StringIO()
    stdout_capture = StringIO()

    with redirect_stderr(stderr_capture), redirect_stdout(stdout_capture):
        if client is None:
            client = get_api_client()

        # API call may trigger token refresh (which writes to stderr)
        result = client.execute(operation, **params)

    # Log any captured output
    if stderr_capture.getvalue():
        logger.info(f"Execution stderr: {stderr_capture.getvalue()}")

    return result
```
</the_solution>

## Pattern 2: Pre-Authorization Script

<the_problem>
MCP servers run as background processes with NO terminal or browser access:

1. User opens Claude Desktop
2. MCP server starts in background
3. OAuth library needs user to authorize in browser
4. **No way to show URL or open browser**
5. Server hangs waiting for authorization that never comes
</the_problem>

<the_solution>
Create a standalone script users run ONCE to authorize and cache the token:

**`authorize.py` (in server root directory):**

```python
#!/usr/bin/env python3
"""
OAuth authorization helper.
Run this once to authorize the app and cache your token.
"""

import os
from your_oauth_library import OAuthProvider

SCOPE = " ".join([
    "scope1",
    "scope2",
    "scope3"
])

def authorize():
    """Perform OAuth authorization and cache token."""
    print("MCP Server - OAuth Authorization")
    print("=" * 50)

    auth_manager = OAuthProvider(
        client_id=os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET"),
        redirect_uri=os.environ.get("REDIRECT_URI"),
        scope=SCOPE,
        open_browser=True  # ✓ Opens browser ONLY during manual setup
    )

    # Trigger authorization flow
    token_info = auth_manager.get_access_token()

    if token_info:
        print("✓ Authorization successful!")
        print("✓ Token cached for future use")
        print()
        print("You can now use the MCP server.")
    else:
        print("✗ Authorization failed.")

if __name__ == "__main__":
    authorize()
```

**User setup flow (document in README):**

```markdown
## Setup

1. Install dependencies: `uv sync`
2. Set environment variables in ~/.zshrc
3. **Authorize the app (one-time):**
   ```bash
   cd ~/Developer/mcp/{server-name}
   uv run python authorize.py
   ```
4. Restart Claude Desktop
```

**Server uses cached token:**

```python
def get_api_client():
    """Initialize client using CACHED token."""
    stderr_capture = StringIO()
    stdout_capture = StringIO()

    with redirect_stderr(stderr_capture), redirect_stdout(stdout_capture):
        auth_manager = OAuthProvider(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            redirect_uri=os.environ.get("REDIRECT_URI"),
            scope=SCOPE,
            open_browser=False  # ✓ Never open browser in server
        )
        # If .cache file exists, uses cached token
        # If token expired, auto-refreshes silently
        client = APIClient(auth_manager=auth_manager)

    return client
```

**Token storage:**

Most OAuth libraries cache tokens in files like `.cache-{username}`.

**Add to `.gitignore`:**
```gitignore
.cache-*
*.token
.credentials
```
</the_solution>

## When to Apply

<apply_when>
**Use both patterns for:**
- ✓ Any OAuth flow (Spotify, Google, GitHub, Facebook, etc.)
- ✓ Any library that writes to stdout/stderr
- ✓ Background services requiring user authorization
- ✓ Any headless environment with OAuth

**Pattern 1 (stdio isolation) is CRITICAL:**
- Skip it → JSON-RPC protocol breaks → server fails

**Pattern 2 (pre-authorization) is REQUIRED:**
- Skip it → Users can't authorize → server unusable
</apply_when>

<dont_apply_when>
**Don't use for:**
- ✗ API key authentication (no authorization flow needed)
- ✗ Client Credentials OAuth (server-to-server, no user interaction)
- ✗ JWT/Bearer tokens (no interactive flow)
- ✗ Web apps with interactive UI
</dont_apply_when>

## Implementation Checklist

Before declaring OAuth integration complete:

- [ ] **stdio isolation** wraps OAuth client initialization
- [ ] **stdio isolation** wraps every API call (token refresh can write to stderr)
- [ ] **`authorize.py`** script created for one-time setup
- [ ] **README** documents authorization step clearly
- [ ] **`.gitignore`** excludes token cache files
- [ ] **Environment variables** documented (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
- [ ] **Tested** authorization flow manually before MCP installation
- [ ] **Verified** server works with cached token (no browser prompts)

## Code Template

**Minimal OAuth MCP server implementation:**

```python
import os
import logging
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from mcp.server import Server
from your_oauth_library import OAuthProvider, APIClient

logger = logging.getLogger(__name__)

SCOPE = "scope1 scope2 scope3"
client = None

def get_api_client():
    """Initialize OAuth client with stdio isolation."""
    stderr_capture = StringIO()
    stdout_capture = StringIO()

    with redirect_stderr(stderr_capture), redirect_stdout(stdout_capture):
        auth_manager = OAuthProvider(
            client_id=os.environ.get("CLIENT_ID"),
            client_secret=os.environ.get("CLIENT_SECRET"),
            redirect_uri=os.environ.get("REDIRECT_URI"),
            scope=SCOPE,
            open_browser=False
        )
        client = APIClient(auth_manager=auth_manager)

    if stderr_capture.getvalue():
        logger.info(f"OAuth stderr: {stderr_capture.getvalue()}")

    return client

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    global client

    # Isolate ALL API calls
    stderr_capture = StringIO()
    stdout_capture = StringIO()

    with redirect_stderr(stderr_capture), redirect_stdout(stdout_capture):
        if client is None:
            client = get_api_client()

        result = client.execute(name, **arguments)

    return [TextContent(type="text", text=json.dumps(result))]
```

## Common OAuth Libraries

**Python:**
- `spotipy` (Spotify) - writes to stderr, needs both patterns
- `google-auth-oauthlib` (Google) - writes to stdout, needs both patterns
- `requests-oauthlib` (generic) - usually silent, still wrap for safety
- `PyGithub` with OAuth - needs both patterns

**TypeScript/Node:**
- Most Node OAuth libraries write to console.log
- Use similar pattern: capture console output during auth

## Key Takeaways

1. **Any library that writes to stdout/stderr will break MCP's JSON-RPC protocol**
2. **MCP servers run headless - separate authorization from runtime**
3. **Token refresh can write to stderr even if initialization doesn't**
4. **Always isolate, always pre-authorize, always test manually first**

---

## Reference: Python Implementation

# Python MCP Server Implementation

<overview>
Python implementation using the mcp package provides clean async/await patterns, decorator-based APIs, and strong type hints. This guide covers Python-specific features and best practices.
</overview>

## Project Setup

<dependencies>
```toml
# pyproject.toml
[project]
name = "my-mcp-server"
version = "1.0.0"
dependencies = [
    "mcp>=0.1.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.0.0",
]

[project.scripts]
my-mcp-server = "my_mcp_server.server:main"

# Or using setup.py/requirements.txt:
# mcp>=0.1.0
# pydantic>=2.0.0
```
</dependencies>

<directory_structure>
```
my_mcp_server/
├── __init__.py
├── server.py          # Main server implementation
├── tools/             # Tool implementations
│   ├── __init__.py
│   ├── calculator.py
│   └── api_client.py
├── resources/         # Resource handlers
│   ├── __init__.py
│   └── file_system.py
└── config.py          # Configuration
```
</directory_structure>

## Server Structure

<full_example>
```python
"""MCP Server implementation."""
import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Resource,
    Prompt,
    PromptMessage,
    GetPromptResult,
)
from pydantic import BaseModel, Field

# Server instance
app = Server("my-mcp-server")

# Type-safe argument models using Pydantic
class AddNumbersArgs(BaseModel):
    """Arguments for add_numbers tool."""
    a: float = Field(description="First number")
    b: float = Field(description="Second number")

class SearchArgs(BaseModel):
    """Arguments for search tool."""
    query: str = Field(min_length=1, max_length=500, description="Search query")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results")
    filters: list[str] | None = Field(default=None, description="Optional filters")

# Tool handlers
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema=AddNumbersArgs.model_json_schema(),
        ),
        Tool(
            name="search",
            description="Search for items",
            inputSchema=SearchArgs.model_json_schema(),
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    if name == "add_numbers":
        args = AddNumbersArgs(**arguments)
        result = args.a + args.b
        return [TextContent(
            type="text",
            text=f"{args.a} + {args.b} = {result}"
        )]

    elif name == "search":
        args = SearchArgs(**arguments)
        results = await perform_search(args.query, args.limit, args.filters)
        return [TextContent(
            type="text",
            text=f"Found {len(results)} results for '{args.query}'"
        )]

    raise ValueError(f"Unknown tool: {name}")

# Resource handlers
@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="config://settings",
            name="Server Configuration",
            description="Current server settings",
            mimeType="application/json",
        ),
        Resource(
            uri="file:///{path}",
            name="File System",
            description="Read files from filesystem",
            mimeType="text/plain",
        ),
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI."""
    if uri == "config://settings":
        import json
        config = load_config()
        return json.dumps(config.__dict__, indent=2)

    elif uri.startswith("file:///"):
        path = uri[8:]  # Remove "file:///"
        async with aiofiles.open(path, "r") as f:
            return await f.read()

    raise ValueError(f"Unknown resource: {uri}")

# Prompt handlers
@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="code_review",
            description="Review code for best practices",
            arguments=[
                {"name": "language", "description": "Programming language", "required": True},
                {"name": "code", "description": "Code to review", "required": True},
            ],
        ),
    ]

@app.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Get a prompt by name."""
    if name == "code_review":
        language = arguments.get("language", "unknown")
        code = arguments.get("code", "")

        return GetPromptResult(
            description=f"Code review for {language}",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Review this {language} code for best practices:\n\n{code}"
                    ),
                ),
            ],
        )

    raise ValueError(f"Unknown prompt: {name}")

# Helper functions
async def perform_search(query: str, limit: int, filters: list[str] | None) -> list[dict]:
    """Perform search operation."""
    # Implementation here
    return []

def load_config():
    """Load server configuration."""
    from .config import Config
    return Config()

# Main entry point
async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        # Log to stderr (stdout is for MCP protocol)
        print("my-mcp-server starting...", file=sys.stderr)

        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

def run():
    """Synchronous entry point for CLI."""
    asyncio.run(main())

if __name__ == "__main__":
    run()
```
</full_example>

## Type-Safe Patterns

<pydantic_models>
**Using Pydantic for Validation**:

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Annotated

class SearchArgs(BaseModel):
    """Search arguments with validation."""
    query: Annotated[str, Field(min_length=1, max_length=500)]
    limit: Annotated[int, Field(ge=1, le=100)] = 10
    sort_by: str | None = None
    ascending: bool = True

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate search query."""
        if v.strip() != v:
            raise ValueError("Query cannot have leading/trailing whitespace")
        return v

    @model_validator(mode='after')
    def validate_sort(self) -> 'SearchArgs':
        """Validate sort parameters."""
        if self.sort_by and self.sort_by not in ['date', 'relevance', 'title']:
            raise ValueError(f"Invalid sort_by: {self.sort_by}")
        return self

# Use in tool handler
@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "search":
        try:
            args = SearchArgs(**arguments)
            results = await perform_search(args)
            return [TextContent(type="text", text=str(results))]
        except ValidationError as e:
            # Return validation errors to Claude
            return [TextContent(
                type="text",
                text=f"Invalid arguments: {e}"
            )]

    raise ValueError(f"Unknown tool: {name}")
```
</pydantic_models>

<async_patterns>
**Async/Await Best Practices**:

```python
import asyncio
from typing import Any

# Concurrent operations
async def fetch_multiple_sources(queries: list[str]) -> list[dict]:
    """Fetch from multiple sources concurrently."""
    tasks = [fetch_source(query) for query in queries]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out errors
    return [r for r in results if not isinstance(r, Exception)]

async def fetch_source(query: str) -> dict:
    """Fetch from a single source."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/search?q={query}") as response:
            return await response.json()

# Timeout handling
async def tool_with_timeout(args: dict) -> TextContent:
    """Tool with timeout protection."""
    try:
        result = await asyncio.wait_for(
            slow_operation(args),
            timeout=30.0  # 30 second timeout
        )
        return TextContent(type="text", text=result)
    except asyncio.TimeoutError:
        return TextContent(
            type="text",
            text="Operation timed out after 30 seconds"
        )

# Background tasks
class ServerState:
    """Maintain server state."""
    def __init__(self):
        self.cache: dict[str, Any] = {}
        self._cleanup_task: asyncio.Task | None = None

    async def start_cleanup(self):
        """Start background cleanup task."""
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _cleanup_loop(self):
        """Periodically clean cache."""
        while True:
            await asyncio.sleep(300)  # Every 5 minutes
            self.cache.clear()
            print("Cache cleaned", file=sys.stderr)

    async def stop(self):
        """Stop background tasks."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

state = ServerState()

async def main():
    """Run server with state management."""
    await state.start_cleanup()

    try:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    finally:
        await state.stop()
```
</async_patterns>

## Error Handling

<error_patterns>
```python
import sys
import traceback
from typing import Any
from mcp.types import TextContent

class ToolError(Exception):
    """Base exception for tool errors."""
    pass

class InvalidArgumentError(ToolError):
    """Invalid tool arguments."""
    pass

class ExternalAPIError(ToolError):
    """External API call failed."""
    pass

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls with comprehensive error handling."""
    try:
        # Validate tool exists
        if name not in AVAILABLE_TOOLS:
            raise ToolError(f"Unknown tool: {name}")

        # Execute tool
        result = await execute_tool(name, arguments)
        return [result]

    except InvalidArgumentError as e:
        # Client error - return helpful message
        print(f"Invalid arguments for {name}: {e}", file=sys.stderr)
        return [TextContent(
            type="text",
            text=f"Invalid arguments: {e}\n\nPlease check the tool's input schema."
        )]

    except ExternalAPIError as e:
        # Upstream error - inform user
        print(f"External API error in {name}: {e}", file=sys.stderr)
        return [TextContent(
            type="text",
            text=f"External service error: {e}\n\nPlease try again later."
        )]

    except Exception as e:
        # Unexpected error - log and return generic message
        print(f"Unexpected error in {name}:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return [TextContent(
            type="text",
            text=f"An unexpected error occurred. Please contact support."
        )]

async def execute_tool(name: str, arguments: dict[str, Any]) -> TextContent:
    """Execute a tool with proper error handling."""
    if name == "api_call":
        try:
            args = APICallArgs(**arguments)
        except Exception as e:
            raise InvalidArgumentError(str(e)) from e

        try:
            response = await make_api_request(args)
            return TextContent(type="text", text=response)
        except aiohttp.ClientError as e:
            raise ExternalAPIError(f"API request failed: {e}") from e

    raise ToolError(f"Unknown tool: {name}")
```
</error_patterns>

## Configuration

<env_config>
```python
# config.py
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    """Server configuration."""
    api_key: str
    api_endpoint: str
    max_retries: int
    debug: bool
    cache_dir: Path

    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables."""
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API_KEY environment variable is required")

        return cls(
            api_key=api_key,
            api_endpoint=os.getenv("API_ENDPOINT", "https://api.example.com"),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            debug=os.getenv("DEBUG", "").lower() == "true",
            cache_dir=Path(os.getenv("CACHE_DIR", "~/.cache/my-mcp-server")).expanduser(),
        )

    def __post_init__(self):
        """Validate and prepare configuration."""
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Log configuration (without secrets)
        if self.debug:
            print(f"Config: endpoint={self.api_endpoint}, retries={self.max_retries}",
                  file=sys.stderr)

# Load config globally
config = Config.from_env()

# Use in tools
@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    if name == "api_call":
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config.api_endpoint}/data",
                headers={"Authorization": f"Bearer {config.api_key}"}
            ) as response:
                data = await response.json()
                return [TextContent(type="text", text=str(data))]

    raise ValueError(f"Unknown tool: {name}")
```

**.env file**:
```
API_KEY=your_api_key_here
API_ENDPOINT=https://api.example.com
MAX_RETRIES=3
DEBUG=true
CACHE_DIR=~/.cache/my-mcp-server
```

**Load .env in development**:
```python
# At top of server.py
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not required in production
```
</env_config>

## Advanced Features

<caching>
**Caching Pattern**:

```python
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Any

class Cache:
    """Simple time-based cache."""
    def __init__(self):
        self._cache: dict[str, tuple[Any, datetime]] = {}

    def get(self, key: str, ttl: int = 300) -> Any | None:
        """Get cached value if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if datetime.now() - timestamp < timedelta(seconds=ttl):
                return value
            del self._cache[key]
        return None

    def set(self, key: str, value: Any):
        """Set cached value."""
        self._cache[key] = (value, datetime.now())

    def clear(self):
        """Clear all cached values."""
        self._cache.clear()

cache = Cache()

async def cached_api_call(url: str) -> dict:
    """API call with caching."""
    cached = cache.get(url, ttl=300)
    if cached is not None:
        print(f"Cache hit: {url}", file=sys.stderr)
        return cached

    print(f"Cache miss: {url}", file=sys.stderr)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            cache.set(url, data)
            return data
```
</caching>

<logging>
**Structured Logging**:

```python
import logging
import sys
from datetime import datetime

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger("my-mcp-server")

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls with logging."""
    logger.info(f"Tool called: {name}", extra={
        "tool_name": name,
        "arg_keys": list(arguments.keys()),
    })

    try:
        result = await execute_tool(name, arguments)
        logger.info(f"Tool completed: {name}")
        return [result]
    except Exception as e:
        logger.error(f"Tool failed: {name}", exc_info=True, extra={
            "tool_name": name,
            "error_type": type(e).__name__,
        })
        raise
```
</logging>

## Build and Distribution

<package_setup>
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-mcp-server"
version = "1.0.0"
description = "MCP server for X"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp>=0.1.0",
    "pydantic>=2.0.0",
    "aiohttp>=3.9.0",
]

[project.scripts]
my-mcp-server = "my_mcp_server.server:run"

[project.urls]
Homepage = "https://github.com/yourusername/my-mcp-server"
Repository = "https://github.com/yourusername/my-mcp-server"
```
</package_setup>

<publishing>
**Build and publish**:

```bash
# Build
python -m pip install build
python -m build

# Publish to PyPI
python -m pip install twine
python -m twine upload dist/*
```

Users install with:
```bash
pip install my-mcp-server
```

Claude Desktop config:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "my-mcp-server"
    }
  }
}
```

Or with uvx (recommended):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uvx",
      "args": ["my-mcp-server"]
    }
  }
}
```
</publishing>

---

## Reference: Response Optimization

# Response Optimization - Truncation & Pagination

<critical_pattern>
**Why this matters:** API responses exhaust Claude's context window after just 5-10 operations. Response optimization achieves 85% token reduction and enables 100+ operations per conversation.

**This pattern is MANDATORY for any MCP server returning lists, search results, or nested objects.**
</critical_pattern>

## The Problem

APIs return verbose responses with nested objects and metadata that Claude doesn't need.

**Example - typical API search response:**

```json
{
  "items": [
    {
      "id": "abc123",
      "name": "Item Name",
      "description": "...",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "owner": {
        "id": "user123",
        "name": "John Doe",
        "email": "john@example.com",
        "avatar_url": "https://...",
        "profile_url": "https://...",
        "created_at": "2023-01-01T00:00:00Z",
        "followers_count": 1234,
        "following_count": 567
      },
      "metadata": {
        "view_count": 5432,
        "like_count": 123,
        "comment_count": 45
      },
      "urls": {
        "self": "https://api.example.com/items/abc123",
        "html": "https://example.com/items/abc123",
        "api": "https://api.example.com/v1/items/abc123"
      },
      "tags": ["tag1", "tag2", "tag3"],
      "is_public": true,
      "is_featured": false,
      "external_ids": {"platform1": "xyz", "platform2": "789"}
    }
    // ... 19 more items with FULL nested objects
  ],
  "pagination": {
    "total": 1247,
    "page": 1,
    "per_page": 20,
    "total_pages": 63
  },
  "links": {
    "next": "https://...",
    "prev": null,
    "first": "https://...",
    "last": "https://..."
  }
}
```

**Token cost:** ~10,000-15,000 tokens for one search

**After 5 searches:** Context exhausted

## The Solution: Two-Part Optimization

### Part 1: Field Truncation (85% token reduction)

**Define essential fields per resource type:**

```python
# What Claude ACTUALLY needs vs what API returns
FIELD_CONFIGS = {
    "items": ["id", "name", "uri", "owner.name", "created_at"],
    # NOT: description, metadata, urls, external_ids, timestamps, etc.

    "users": ["id", "name", "email"],
    # NOT: avatar_url, profile_url, followers_count, created_at, etc.

    "posts": ["id", "title", "author.name", "content_preview"],
    # NOT: full_content, metadata, view_counts, related_posts, etc.
}
```

**Key principle:** Include only what Claude needs to:
1. Uniquely identify the resource (id, uri)
2. Display to user (name, title)
3. Make decisions about next action (status, type, essential relationships)

**Exclude:**
- ✗ Full URLs (API endpoints, profile links)
- ✗ Counters/metrics (views, likes, followers)
- ✗ Timestamps (unless essential for filtering)
- ✗ External IDs and platform-specific metadata
- ✗ Nested objects beyond 1-2 essential fields

**Implementation:**

```python
def _extract_fields(obj: dict, fields: list[str]) -> dict:
    """Extract only specified fields, supporting dot notation for nested fields."""
    result = {}

    for field in fields:
        if "." in field:
            # Handle nested fields like "owner.name"
            parts = field.split(".")
            value = obj
            for part in parts:
                value = value.get(part) if isinstance(value, dict) else None
                if value is None:
                    break

            if value is not None:
                # Flatten nested field
                result[field.replace(".", "_")] = value
        else:
            # Direct field
            if field in obj:
                result[field] = obj[field]

    return result


def _truncate_response(result: dict, operation: str) -> dict:
    """Strip unnecessary fields from API responses."""

    # Handle list responses
    if "items" in result and isinstance(result["items"], list):
        result["items"] = [
            _extract_fields(item, FIELD_CONFIGS["items"])
            for item in result["items"]
        ]

    # Handle single object responses
    elif "data" in result and isinstance(result["data"], dict):
        result["data"] = _extract_fields(result["data"], FIELD_CONFIGS.get(operation, []))

    # Handle nested result types (like Spotify search with tracks/artists/albums)
    elif "tracks" in result and "items" in result["tracks"]:
        result["tracks"]["items"] = [
            _extract_fields(track, FIELD_CONFIGS["tracks"])
            for track in result["tracks"]["items"]
        ]

    return result
```

**Result - optimized response:**

```json
{
  "items": [
    {
      "id": "abc123",
      "name": "Item Name",
      "uri": "app:item:abc123",
      "owner_name": "John Doe",
      "created_at": "2024-01-15"
    }
    // ... 19 more items (minimal data)
  ],
  "total": 1247
}
```

**Token cost:** ~1,500-2,000 tokens (85% reduction)

### Part 2: Adaptive Pagination (20k token threshold)

**For responses that STILL exceed 15-20k tokens after truncation:**

```python
# Constants
CHUNK_SIZE_TOKENS = 15000        # Target chunk size
MAX_TOKENS_BEFORE_CHUNK = 20000  # Threshold to trigger chunking
RESULTS_CACHE = {}               # Session cache

def estimate_tokens(obj: Any) -> int:
    """Estimate token count for an object.

    Rough approximation: 1 token ≈ 4 characters
    """
    try:
        json_str = json.dumps(obj, ensure_ascii=False)
        return len(json_str) // 4
    except:
        return 0


def chunk_by_tokens(data: dict, chunk_size: int = CHUNK_SIZE_TOKENS) -> list[dict]:
    """Split a dict with 'items' or 'data' array into chunks by token count.

    Preserves metadata in first chunk only.
    """
    if not isinstance(data, dict):
        return [data]

    # Try 'items' or 'data' array
    items_key = "items" if "items" in data else "data" if "data" in data else None

    if not items_key or not isinstance(data[items_key], list):
        return [data]

    items = data[items_key]
    if not items:
        return [data]

    chunks = []
    current_chunk_items = []
    current_chunk_tokens = 0

    # Preserve metadata fields in first chunk
    metadata = {k: v for k, v in data.items() if k != items_key}
    metadata_tokens = estimate_tokens(metadata)

    for item in items:
        item_tokens = estimate_tokens(item)

        # Check if adding this item would exceed chunk size
        if current_chunk_items and (current_chunk_tokens + item_tokens > chunk_size):
            # Save current chunk
            chunk_data = {items_key: current_chunk_items}
            if not chunks:
                # Include metadata in first chunk only
                chunk_data.update(metadata)
            chunks.append(chunk_data)

            # Start new chunk
            current_chunk_items = [item]
            current_chunk_tokens = item_tokens
        else:
            current_chunk_items.append(item)
            current_chunk_tokens += item_tokens

    # Add final chunk
    if current_chunk_items:
        chunk_data = {items_key: current_chunk_items}
        if not chunks:
            chunk_data.update(metadata)
        chunks.append(chunk_data)

    return chunks


def format_chunked_response(chunk: dict, chunk_index: int, total_chunks: int, session_id: str = None) -> str:
    """Format a chunk with pagination footer."""
    chunk_json = json.dumps(chunk, indent=2, ensure_ascii=False)

    if total_chunks <= 1:
        return chunk_json

    footer = f"\n\n--- Page {chunk_index + 1}/{total_chunks} ---"
    if chunk_index < total_chunks - 1:
        footer += f"\nCall the 'continue' tool to see more results."
        if session_id:
            footer += f" (session: {session_id})"

    return chunk_json + footer
```

**Apply in execute handler:**

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "yourapp_execute":
        operation = arguments["operation"]
        params = arguments.get("params", {})

        # Execute operation
        result = _execute_operation(operation, params)

        # STEP 1: Apply field truncation (ALWAYS)
        result = _truncate_response(result, operation)

        # STEP 2: Check if pagination needed
        estimated_tokens = estimate_tokens(result)

        if estimated_tokens > MAX_TOKENS_BEFORE_CHUNK:
            # Split into chunks
            chunks = chunk_by_tokens(result, CHUNK_SIZE_TOKENS)

            if len(chunks) > 1:
                # Generate session ID
                import time
                session_id = f"sess_{int(time.time())}_{id(result) % 10000}"

                # Cache remaining chunks
                RESULTS_CACHE[session_id] = {
                    "chunks": chunks,
                    "current_index": 1,  # Next chunk to return
                    "timestamp": time.time()
                }

                # Return only first chunk
                response_text = format_chunked_response(
                    chunks[0],
                    0,
                    len(chunks),
                    session_id
                )
                return [TextContent(type="text", text=response_text)]

        # Normal response (fits in one chunk)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
```

### Part 3: Continue Tool

**Add to meta-tools:**

```python
Tool(
    name="yourapp_continue",
    description="Continue retrieving paginated results from a previous operation. Use when a response shows 'Page X/Y' footer.",
    inputSchema={
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "Session ID from previous paginated response (optional if continuing last session)"
            }
        }
    }
)
```

**Implementation:**

```python
LAST_SESSION_ID = None  # Track most recent session

if name == "yourapp_continue":
    session_id = arguments.get("session_id", LAST_SESSION_ID)

    if not session_id or session_id not in RESULTS_CACHE:
        return [TextContent(
            type="text",
            text="No active pagination session found."
        )]

    # Get cached session
    session = RESULTS_CACHE[session_id]
    chunks = session["chunks"]
    current_index = session["current_index"]

    if current_index >= len(chunks):
        return [TextContent(
            type="text",
            text="No more results available."
        )]

    # Return next chunk
    chunk = chunks[current_index]
    session["current_index"] += 1

    response_text = format_chunked_response(
        chunk,
        current_index,
        len(chunks),
        session_id
    )

    return [TextContent(type="text", text=response_text)]
```

### Part 4: On-Demand Fields (Optional Parameter)

**Pattern:** Allow caller to specify which fields to fetch in GET operations.

**When to use:**
- GET operations where different use cases need different field subsets
- Resources with 10+ available fields but most calls only need 3-4
- Copying/cloning workflows that need configuration fields
- Complementary to field truncation for lists

**Implementation:**

```python
def execute_campaigns_get(
    campaign_id: str,
    fields: list = None,  # Optional field selection
    profile: str = None
) -> dict:
    """Get campaign details with optional field selection."""

    if fields is None:
        # Minimal default for common case
        fields = ["id", "name", "status"]

    # Fetch requested fields from API
    campaign = Campaign(campaign_id)
    result = campaign.api_get(fields=fields)

    return {"data": result.export_all_data()}
```

**Schema definition:**

```json
{
  "name": "yourapp_get_campaign",
  "inputSchema": {
    "type": "object",
    "properties": {
      "campaign_id": {"type": "string"},
      "fields": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Optional fields to fetch. Defaults to [id, name, status]. Available: id, name, status, objective, daily_budget, bid_strategy, created_time, etc."
      }
    },
    "required": ["campaign_id"]
  }
}
```

**Usage examples:**

```
# Minimal fetch (default)
campaigns.get(id="123")
→ {"id": "123", "name": "Test", "status": "ACTIVE"}

# Fetch specific fields for cloning
campaigns.get(id="123", fields=["objective", "daily_budget", "bid_strategy"])
→ {"objective": "SALES", "daily_budget": 5000, "bid_strategy": "LOWEST_COST"}

# Fetch all fields when needed
campaigns.get(id="123", fields=["*"])  # or comprehensive list
```

**Design principle:**

This mirrors the on-demand operations pattern at the response data level:
- On-demand operations: Don't load tool schemas until needed (98% context reduction)
- On-demand fields: Don't load field data until needed (variable context savings)

Both implement: "Pay only for what you use"

**Field discovery:**

Document available fields in operation schema description or point to API docs. Claude can learn which fields exist through:
1. Schema descriptions listing common fields
2. API documentation references
3. Error messages when requesting invalid fields

## When to Apply

<decision_tree>
**ALWAYS apply field truncation if:**
- ✓ Returns lists of items (search, list, browse, query)
- ✓ Returns nested objects (items with embedded related data)
- ✓ API responses regularly > 1,000 tokens
- ✓ Designed for multiple operations per conversation

**ALWAYS apply pagination if:**
- ✓ API can return 100+ items
- ✓ Single responses can exceed 20,000 tokens
- ✓ List operations are common use case

**MAYBE skip if:**
- Single-object CRUD only (get one user, update one record)
- API already returns minimal responses
- Server designed for one-shot operations only
- Responses consistently < 500 tokens
</decision_tree>

## Implementation Checklist

Before declaring optimization complete:

- [ ] **Field configs** defined for each resource type
- [ ] **Token estimation** function implemented
- [ ] **Response truncation** applied in execute handler (BEFORE pagination)
- [ ] **Chunking logic** for responses > 20k tokens
- [ ] **Continue tool** implemented for pagination
- [ ] **Session cache** with cleanup (TTL)
- [ ] **Metadata preservation** in first chunk only
- [ ] **Tested** with large result sets (100+ items)

## Cache Cleanup

**Add TTL to prevent memory leaks:**

```python
import time

def clean_expired_sessions():
    """Remove sessions older than 5 minutes."""
    cutoff = time.time() - 300  # 5 minutes
    expired = [
        sid for sid, session in RESULTS_CACHE.items()
        if session.get("timestamp", 0) < cutoff
    ]
    for sid in expired:
        del RESULTS_CACHE[sid]

# Call before adding new session
clean_expired_sessions()
```

## Real-World Impact

**Without optimization:**
```
Search operation: 10,000 tokens
× 5 searches = 50,000 tokens
Context remaining: 150,000 / 200,000 (25% exhausted)
```

**With optimization:**
```
Search operation: 1,500 tokens (truncated)
× 5 searches = 7,500 tokens
Context remaining: 192,500 / 200,000 (3.75% used)
```

**Result:** 42,500 tokens saved = 28+ more operations possible

## User Experience

**Traditional (unoptimized):**
```
User: "Search for Queen"
Claude: [receives 10,000 token response]
User: "Search for Beatles"
Claude: [receives 10,000 tokens]
... after 5-10 searches, context exhausted
Claude: "I've run out of context"
```

**Optimized:**
```
User: "Search for Queen"
Claude: [receives 1,500 token response]
User: "Search for Beatles"
Claude: [receives 1,500 tokens]
User: "List all my playlists"
Claude: [receives first 15k token chunk]
Claude: "Page 1/3 - call continue for more"
User: "continue"
Claude: [receives second chunk from cache]
... can perform 50+ operations before context issues
```

## Key Takeaways

1. **API responses are designed for breadth, not efficiency**
2. **Field truncation is MANDATORY for production MCP servers**
3. **Pagination is REQUIRED for list operations**
4. **85% token reduction is achievable with minimal code**
5. **Context efficiency enables longer, more productive conversations**
6. **Apply optimization BEFORE declaring server "complete"**

---

## Reference: Testing And Deployment

# Testing and Deployment

<overview>
Production MCP servers require thorough testing and reliable deployment strategies. This guide covers testing approaches, packaging, and distribution for both TypeScript and Python servers.
</overview>

## Testing Strategies

<testing_pyramid>
**Test Pyramid for MCP Servers**:

1. **Unit Tests** (70%): Test individual tool/resource handlers
2. **Integration Tests** (20%): Test server protocol compliance
3. **End-to-End Tests** (10%): Test with actual Claude Desktop

</testing_pyramid>

## TypeScript Testing

<typescript_unit_tests>
**Unit Testing with Vitest**:

```bash
npm install -D vitest @vitest/ui
```

```typescript
// tests/tools/calculator.test.ts
import { describe, it, expect } from "vitest";
import { addNumbersTool } from "../../src/tools/calculator";

describe("Calculator Tools", () => {
  describe("addNumbersTool", () => {
    it("should add two positive numbers", async () => {
      const result = await addNumbersTool({ a: 5, b: 3 });

      expect(result).toEqual({
        type: "text",
        text: "5 + 3 = 8",
      });
    });

    it("should handle negative numbers", async () => {
      const result = await addNumbersTool({ a: -5, b: 3 });

      expect(result).toEqual({
        type: "text",
        text: "-5 + 3 = -2",
      });
    });

    it("should handle decimals", async () => {
      const result = await addNumbersTool({ a: 1.5, b: 2.7 });

      expect(result).toEqual({
        type: "text",
        text: "1.5 + 2.7 = 4.2",
      });
    });
  });
});
```

```json
// package.json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  }
}
```
</typescript_unit_tests>

<typescript_integration_tests>
**Integration Testing**:

```typescript
// tests/integration/server.test.ts
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { createServer } from "../../src/server";

describe("MCP Server Integration", () => {
  let server: Server;
  let transport: InMemoryTransport;

  beforeAll(async () => {
    server = createServer();
    transport = new InMemoryTransport();
    await server.connect(transport);
  });

  afterAll(async () => {
    await server.close();
  });

  it("should list tools", async () => {
    const response = await transport.request({
      method: "tools/list",
    });

    expect(response.tools).toBeArrayOfSize(3);
    expect(response.tools).toContainEqual(
      expect.objectContaining({
        name: "add_numbers",
        description: expect.any(String),
      })
    );
  });

  it("should call tool successfully", async () => {
    const response = await transport.request({
      method: "tools/call",
      params: {
        name: "add_numbers",
        arguments: { a: 5, b: 3 },
      },
    });

    expect(response.content).toEqual([
      {
        type: "text",
        text: "5 + 3 = 8",
      },
    ]);
  });

  it("should return error for unknown tool", async () => {
    await expect(
      transport.request({
        method: "tools/call",
        params: {
          name: "unknown_tool",
          arguments: {},
        },
      })
    ).rejects.toThrow("Unknown tool");
  });

  it("should validate tool arguments", async () => {
    await expect(
      transport.request({
        method: "tools/call",
        params: {
          name: "add_numbers",
          arguments: { a: "not a number", b: 3 },
        },
      })
    ).rejects.toThrow();
  });
});
```
</typescript_integration_tests>

<typescript_mocking>
**Mocking External Dependencies**:

```typescript
// tests/tools/api-client.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { apiClientTool } from "../../src/tools/api-client";

// Mock fetch
global.fetch = vi.fn();

describe("API Client Tool", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should make successful API call", async () => {
    const mockResponse = { data: "test" };

    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await apiClientTool({
      endpoint: "/users/123",
      method: "GET",
    });

    expect(global.fetch).toHaveBeenCalledWith(
      "https://api.example.com/users/123",
      expect.objectContaining({
        method: "GET",
      })
    );

    expect(result).toEqual({
      type: "text",
      text: JSON.stringify(mockResponse, null, 2),
    });
  });

  it("should handle API errors", async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error("Network error"));

    await expect(
      apiClientTool({
        endpoint: "/users/123",
        method: "GET",
      })
    ).rejects.toThrow("Network error");
  });
});
```
</typescript_mocking>

## Python Testing

<python_unit_tests>
**Unit Testing with pytest**:

```bash
pip install pytest pytest-asyncio pytest-cov
```

```python
# tests/tools/test_calculator.py
import pytest
from my_mcp_server.tools.calculator import add_numbers_tool
from my_mcp_server.types import AddNumbersArgs

@pytest.mark.asyncio
async def test_add_positive_numbers():
    """Test adding two positive numbers."""
    args = AddNumbersArgs(a=5, b=3)
    result = await add_numbers_tool(args)

    assert result.type == "text"
    assert result.text == "5 + 3 = 8"

@pytest.mark.asyncio
async def test_add_negative_numbers():
    """Test adding negative numbers."""
    args = AddNumbersArgs(a=-5, b=3)
    result = await add_numbers_tool(args)

    assert result.type == "text"
    assert result.text == "-5 + 3 = -2"

@pytest.mark.asyncio
async def test_add_decimals():
    """Test adding decimal numbers."""
    args = AddNumbersArgs(a=1.5, b=2.7)
    result = await add_numbers_tool(args)

    assert result.type == "text"
    assert result.text == "1.5 + 2.7 = 4.2"

def test_invalid_arguments():
    """Test validation of invalid arguments."""
    with pytest.raises(ValueError):
        AddNumbersArgs(a="not a number", b=3)
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

[tool.coverage.run]
source = ["my_mcp_server"]
omit = ["*/tests/*"]
```

```json
// package.json (for npm scripts)
{
  "scripts": {
    "test": "pytest",
    "test:coverage": "pytest --cov --cov-report=html",
    "test:watch": "pytest-watch"
  }
}
```
</python_unit_tests>

<python_integration_tests>
**Integration Testing**:

```python
# tests/integration/test_server.py
import pytest
from mcp.server import Server
from mcp.types import TextContent
from my_mcp_server.server import app, list_tools, call_tool

@pytest.mark.asyncio
async def test_list_tools():
    """Test listing available tools."""
    tools = await list_tools()

    assert len(tools) == 3
    assert any(tool.name == "add_numbers" for tool in tools)

@pytest.mark.asyncio
async def test_call_tool_success():
    """Test successful tool call."""
    result = await call_tool("add_numbers", {"a": 5, "b": 3})

    assert len(result) == 1
    assert result[0].type == "text"
    assert result[0].text == "5 + 3 = 8"

@pytest.mark.asyncio
async def test_call_unknown_tool():
    """Test calling unknown tool."""
    with pytest.raises(ValueError, match="Unknown tool"):
        await call_tool("unknown_tool", {})

@pytest.mark.asyncio
async def test_call_tool_invalid_args():
    """Test calling tool with invalid arguments."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        await call_tool("add_numbers", {"a": "not a number", "b": 3})

@pytest.mark.asyncio
async def test_resources():
    """Test resource handlers."""
    from my_mcp_server.server import list_resources, read_resource

    resources = await list_resources()
    assert len(resources) > 0

    # Test reading a resource
    content = await read_resource("config://settings")
    assert isinstance(content, str)
```
</python_integration_tests>

<python_mocking>
**Mocking External Dependencies**:

```python
# tests/tools/test_api_client.py
import pytest
from unittest.mock import AsyncMock, patch
from my_mcp_server.tools.api_client import api_client_tool
from my_mcp_server.types import APIClientArgs

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_api_call_success(mock_get):
    """Test successful API call."""
    # Setup mock
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={"data": "test"})
    mock_response.raise_for_status = AsyncMock()
    mock_get.return_value.__aenter__.return_value = mock_response

    # Execute
    args = APIClientArgs(endpoint="/users/123", method="GET")
    result = await api_client_tool(args)

    # Verify
    assert result.type == "text"
    assert '"data": "test"' in result.text
    mock_get.assert_called_once()

@pytest.mark.asyncio
@patch("aiohttp.ClientSession.get")
async def test_api_call_error(mock_get):
    """Test API call error handling."""
    # Setup mock to raise error
    mock_get.side_effect = Exception("Network error")

    # Execute and verify
    args = APIClientArgs(endpoint="/users/123", method="GET")
    with pytest.raises(Exception, match="Network error"):
        await api_client_tool(args)
```
</python_mocking>

## End-to-End Testing

<e2e_manual>
**Manual E2E Testing with Claude Desktop**:

1. **Build your server**:
   ```bash
   # TypeScript
   npm run build

   # Python
   python -m pip install -e .
   ```

2. **Configure Claude Desktop**:
   ```json
   {
     "mcpServers": {
       "test-server": {
         "command": "node",
         "args": ["/absolute/path/to/dist/index.js"]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test in conversation**:
   - "List available tools"
   - "Use the add_numbers tool with 5 and 3"
   - "Read the config://settings resource"

5. **Check logs**:
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Look for your server's stderr output

</e2e_manual>

<e2e_automated>
**Automated E2E Testing** (Advanced):

```typescript
// tests/e2e/claude-integration.test.ts
import { describe, it, expect } from "vitest";
import { spawn } from "child_process";
import { once } from "events";

describe("E2E: Claude Desktop Integration", () => {
  it("should start server and respond to requests", async () => {
    // Start server as subprocess
    const server = spawn("node", ["dist/index.js"], {
      stdio: ["pipe", "pipe", "pipe"],
    });

    // Wait for server to be ready
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // Send MCP protocol message
    const request = {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/list",
    };

    server.stdin.write(JSON.stringify(request) + "\n");

    // Read response
    const [output] = await once(server.stdout, "data");
    const response = JSON.parse(output.toString());

    expect(response.result.tools).toBeDefined();
    expect(response.result.tools.length).toBeGreaterThan(0);

    // Cleanup
    server.kill();
  });
});
```

```python
# tests/e2e/test_claude_integration.py
import pytest
import asyncio
import json
from my_mcp_server.server import main

@pytest.mark.asyncio
async def test_server_protocol():
    """Test server responds to MCP protocol."""
    # This is a simplified example - real implementation would use
    # proper stdio mocking or subprocess communication

    # Start server in background
    server_task = asyncio.create_task(main())

    # Give it time to start
    await asyncio.sleep(1)

    # In practice, you'd send actual MCP protocol messages
    # and verify responses

    # Cleanup
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass
```
</e2e_automated>

## Packaging and Distribution

<typescript_packaging>
**TypeScript: npm Package**:

```json
// package.json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for X",
  "main": "dist/index.js",
  "bin": {
    "my-mcp-server": "./dist/index.js"
  },
  "files": [
    "dist/**/*",
    "README.md",
    "LICENSE"
  ],
  "scripts": {
    "build": "tsc && chmod +x dist/index.js",
    "prepublishOnly": "npm run build && npm test"
  },
  "keywords": ["mcp", "mcp-server", "claude"],
  "author": "Your Name",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/my-mcp-server"
  }
}
```

**Publishing**:
```bash
# Test locally first
npm link
# Test in Claude Desktop with: "command": "my-mcp-server"

# Publish to npm
npm login
npm publish

# Users install with:
# npm install -g my-mcp-server
```
</typescript_packaging>

<python_packaging>
**Python: PyPI Package**:

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-mcp-server"
version = "1.0.0"
description = "MCP server for X"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
keywords = ["mcp", "mcp-server", "claude"]
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "mcp>=0.1.0",
    "pydantic>=2.0.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/my-mcp-server"
Repository = "https://github.com/yourusername/my-mcp-server"
Issues = "https://github.com/yourusername/my-mcp-server/issues"

[project.scripts]
my-mcp-server = "my_mcp_server.server:run"
```

**Publishing**:
```bash
# Build
python -m build

# Test locally first
pip install -e .
# Test in Claude Desktop

# Publish to PyPI
python -m twine upload dist/*

# Users install with:
# pip install my-mcp-server
# OR uvx my-mcp-server (recommended)
```
</python_packaging>

<docker_deployment>
**Docker Deployment** (for server-based MCP):

```dockerfile
# Dockerfile
FROM node:20-slim

WORKDIR /app

COPY package*.json ./
RUN npm ci --production

COPY dist ./dist

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  mcp-server:
    build: .
    ports:
      - "3000:3000"
    environment:
      - API_KEY=${API_KEY}
      - DEBUG=false
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```
</docker_deployment>

## CI/CD

<github_actions>
**GitHub Actions Workflow**:

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test-typescript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run build
      - run: npm test
      - run: npm run test:coverage

  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: pytest --cov

  publish-npm:
    needs: test-typescript
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm run build
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}

  publish-pypi:
    needs: test-python
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install build twine
      - run: python -m build
      - run: python -m twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```
</github_actions>

---

## Reference: Tools And Resources

# MCP Tools and Resources - Advanced Patterns

<overview>
Tools and Resources are the primary ways MCP servers expose functionality. This guide covers advanced patterns, best practices, and real-world examples for both primitives.
</overview>

## Tools: Deep Dive

<tool_design_principles>

**What makes a good tool?**

1. **Single responsibility**: Each tool does one thing well
2. **Clear description**: Claude knows when to use it
3. **Strict schema**: Input validation prevents errors
4. **Predictable output**: Consistent response format
5. **Error messages**: Help Claude understand what went wrong

**Examples**:

✅ **Good**: `search_emails(query: string, limit: number) -> SearchResults`
- Clear purpose, predictable output

❌ **Bad**: `do_stuff(action: string, params: any) -> any`
- Vague purpose, unpredictable output

</tool_design_principles>

<input_schemas>

## Input Schema Best Practices

**TypeScript (Zod)**:
```typescript
import { z } from "zod";

// Strict validation with helpful descriptions
const EmailSearchSchema = z.object({
  query: z.string()
    .min(1, "Query cannot be empty")
    .max(500, "Query too long")
    .describe("Search query for email content"),

  from: z.string()
    .email("Must be valid email address")
    .optional()
    .describe("Filter by sender email"),

  date_range: z.object({
    start: z.string().datetime().describe("Start date (ISO 8601)"),
    end: z.string().datetime().describe("End date (ISO 8601)"),
  }).optional().describe("Filter by date range"),

  limit: z.number()
    .int("Must be integer")
    .min(1, "Minimum 1 result")
    .max(100, "Maximum 100 results")
    .default(10)
    .describe("Maximum number of results"),

  include_attachments: z.boolean()
    .default(false)
    .describe("Include emails with attachments only"),
});
```

**Python (Pydantic)**:
```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime

class DateRange(BaseModel):
    """Date range filter."""
    start: datetime = Field(description="Start date")
    end: datetime = Field(description="End date")

    @field_validator('end')
    @classmethod
    def validate_range(cls, v: datetime, info) -> datetime:
        if 'start' in info.data and v < info.data['start']:
            raise ValueError("End date must be after start date")
        return v

class EmailSearchArgs(BaseModel):
    """Email search arguments."""
    query: str = Field(
        min_length=1,
        max_length=500,
        description="Search query for email content"
    )
    from_: EmailStr | None = Field(
        default=None,
        alias="from",
        description="Filter by sender email"
    )
    date_range: DateRange | None = Field(
        default=None,
        description="Filter by date range"
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of results"
    )
    include_attachments: bool = Field(
        default=False,
        description="Include emails with attachments only"
    )
```

**Key takeaways**:
- Use `.describe()` / `description=` on every field
- Set sensible limits (min/max length, ranges)
- Provide defaults for optional parameters
- Validate relationships between fields
- Use domain-specific types (email, URL, datetime)

</input_schemas>

<output_formats>

## Output Formats

<text_content>
**Text Content** (most common):

```typescript
// TypeScript
return {
  content: [
    {
      type: "text",
      text: "Search results:\n\n1. Email from john@example.com...",
    },
  ],
};
```

```python
# Python
return [TextContent(
    type="text",
    text="Search results:\n\n1. Email from john@example.com..."
)]
```

**When to use**: General purpose results, formatted text, JSON data
</text_content>

<image_content>
**Image Content**:

```typescript
// TypeScript
return {
  content: [
    {
      type: "image",
      data: base64ImageData,
      mimeType: "image/png",
    },
  ],
};
```

```python
# Python
return [ImageContent(
    type="image",
    data=base64_image_data,
    mimeType="image/png"
)]
```

**When to use**: Charts, screenshots, diagrams, generated images
</image_content>

<embedded_resource>
**Embedded Resource**:

```typescript
// TypeScript
return {
  content: [
    {
      type: "resource",
      resource: {
        uri: "email://inbox/12345",
        name: "Email from john@example.com",
        mimeType: "message/rfc822",
        text: emailContent,
      },
    },
  ],
};
```

```python
# Python
return [EmbeddedResource(
    type="resource",
    resource={
        "uri": "email://inbox/12345",
        "name": "Email from john@example.com",
        "mimeType": "message/rfc822",
        "text": email_content,
    }
)]
```

**When to use**: Returning data that could be read as a resource later
</embedded_resource>

<multiple_content>
**Multiple Content Items**:

```typescript
// TypeScript - return multiple pieces of content
return {
  content: [
    {
      type: "text",
      text: "Analysis complete. Here are the results:",
    },
    {
      type: "image",
      data: chartImageBase64,
      mimeType: "image/png",
    },
    {
      type: "text",
      text: "Detailed findings:\n\n...",
    },
  ],
};
```

**When to use**: Complex results with mixed content types
</multiple_content>

</output_formats>

<tool_patterns>

## Common Tool Patterns

<api_client_tool>
**API Client Tool**:

```python
import aiohttp
from typing import Any

class APIClientArgs(BaseModel):
    endpoint: str = Field(description="API endpoint path")
    method: str = Field(default="GET", pattern="^(GET|POST|PUT|DELETE)$")
    body: dict[str, Any] | None = Field(default=None, description="Request body")
    headers: dict[str, str] | None = Field(default=None, description="Custom headers")

async def api_client_tool(args: APIClientArgs) -> TextContent:
    """Generic API client tool."""
    url = f"{config.api_base_url}{args.endpoint}"

    headers = {
        "Authorization": f"Bearer {config.api_key}",
        **(args.headers or {}),
    }

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=args.method,
            url=url,
            json=args.body,
            headers=headers,
        ) as response:
            response.raise_for_status()
            data = await response.json()

            return TextContent(
                type="text",
                text=json.dumps(data, indent=2)
            )
```
</api_client_tool>

<file_operation_tool>
**File Operation Tool**:

```typescript
import { z } from "zod";
import fs from "fs/promises";
import path from "path";

const WriteFileSchema = z.object({
  path: z.string().describe("File path to write"),
  content: z.string().describe("Content to write"),
  mode: z.enum(["overwrite", "append"]).default("overwrite"),
});

async function writeFileTool(args: z.infer<typeof WriteFileSchema>) {
  // Security: Restrict to allowed directories
  const allowedDir = "/Users/user/documents";
  const fullPath = path.resolve(allowedDir, args.path);

  if (!fullPath.startsWith(allowedDir)) {
    throw new Error("Access denied: Path outside allowed directory");
  }

  // Ensure directory exists
  await fs.mkdir(path.dirname(fullPath), { recursive: true });

  // Write file
  if (args.mode === "append") {
    await fs.appendFile(fullPath, args.content);
  } else {
    await fs.writeFile(fullPath, args.content);
  }

  return {
    content: [
      {
        type: "text",
        text: `File written: ${args.path} (${args.content.length} bytes)`,
      },
    ],
  };
}
```
</file_operation_tool>

<database_query_tool>
**Database Query Tool**:

```python
import asyncpg
from typing import Any

class QueryArgs(BaseModel):
    query: str = Field(description="SQL query to execute")
    params: list[Any] | None = Field(default=None, description="Query parameters")
    limit: int = Field(default=100, ge=1, le=1000, description="Row limit")

async def database_query_tool(args: QueryArgs) -> TextContent:
    """Execute database query."""
    # Connect to database
    conn = await asyncpg.connect(
        host=config.db_host,
        database=config.db_name,
        user=config.db_user,
        password=config.db_password,
    )

    try:
        # Security: Use parameterized queries
        query = f"{args.query} LIMIT {args.limit}"
        rows = await conn.fetch(query, *(args.params or []))

        # Format results
        results = [dict(row) for row in rows]

        return TextContent(
            type="text",
            text=json.dumps(results, indent=2, default=str)
        )
    finally:
        await conn.close()
```
</database_query_tool>

<batch_processing_tool>
**Batch Processing Tool**:

```typescript
const BatchProcessSchema = z.object({
  items: z.array(z.string()).min(1).max(100),
  operation: z.enum(["validate", "transform", "analyze"]),
});

async function batchProcessTool(args: z.infer<typeof BatchProcessSchema>) {
  const results = [];

  for (const item of args.items) {
    try {
      const result = await processItem(item, args.operation);
      results.push({ item, status: "success", result });
    } catch (error) {
      results.push({
        item,
        status: "error",
        error: error instanceof Error ? error.message : "Unknown error",
      });
    }
  }

  const successCount = results.filter((r) => r.status === "success").length;

  return {
    content: [
      {
        type: "text",
        text: `Processed ${args.items.length} items: ${successCount} succeeded, ${
          args.items.length - successCount
        } failed\n\n${JSON.stringify(results, null, 2)}`,
      },
    ],
  };
}
```
</batch_processing_tool>

</tool_patterns>

## Resources: Deep Dive

<resource_design_principles>

**What makes a good resource?**

1. **Logical URI scheme**: Consistent, hierarchical addressing
2. **Clear naming**: Resource purpose is obvious
3. **Appropriate mime types**: Helps Claude understand content
4. **Template support**: Use URI templates for dynamic resources
5. **Efficient reading**: Don't load everything at once

**URI Scheme Examples**:

```
file:///{path}                    - File system
db:///{table}/{id}                - Database records
api:///{service}/{endpoint}       - API endpoints
config:///{section}               - Configuration
email:///{folder}/{id}            - Email messages
doc:///{category}/{id}            - Documentation
```

</resource_design_principles>

<resource_patterns>

## Common Resource Patterns

<file_system_resource>
**File System Resource**:

```python
import aiofiles
import os
from pathlib import Path

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List file system resources."""
    base_dir = Path("/Users/user/documents")

    resources = [
        Resource(
            uri="file:///{path}",
            name="File System",
            description="Read files from documents directory",
            mimeType="text/plain",
        )
    ]

    # Also list recent files
    for file_path in base_dir.glob("**/*.txt"):
        rel_path = file_path.relative_to(base_dir)
        resources.append(Resource(
            uri=f"file:///{rel_path}",
            name=file_path.name,
            description=f"Text file: {rel_path}",
            mimeType="text/plain",
        ))

    return resources

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read file system resource."""
    if uri.startswith("file:///"):
        path = uri[8:]  # Remove "file:///"
        full_path = Path("/Users/user/documents") / path

        # Security check
        if not str(full_path).startswith("/Users/user/documents"):
            raise ValueError("Access denied")

        if not full_path.exists():
            raise ValueError(f"File not found: {path}")

        async with aiofiles.open(full_path, "r") as f:
            return await f.read()

    raise ValueError(f"Unknown resource: {uri}")
```
</file_system_resource>

<database_resource>
**Database Resource**:

```typescript
// List database resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const tables = await db.query("SELECT table_name FROM information_schema.tables");

  const resources: Resource[] = tables.rows.map((row) => ({
    uri: `db:///${row.table_name}/{id}`,
    name: `${row.table_name} table`,
    description: `Database table: ${row.table_name}`,
    mimeType: "application/json",
  }));

  return { resources };
});

// Read database resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;
  const match = uri.match(/^db:\/\/\/([^/]+)\/(.+)$/);

  if (match) {
    const [, table, id] = match;

    // Security: Validate table name against whitelist
    const allowedTables = ["users", "posts", "comments"];
    if (!allowedTables.includes(table)) {
      throw new Error(`Access denied: ${table}`);
    }

    const result = await db.query(
      `SELECT * FROM ${table} WHERE id = $1`,
      [id]
    );

    if (result.rows.length === 0) {
      throw new Error(`Record not found: ${table}/${id}`);
    }

    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(result.rows[0], null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```
</database_resource>

<api_resource>
**API Resource**:

```python
@app.list_resources()
async def list_resources() -> list[Resource]:
    """List API endpoint resources."""
    return [
        Resource(
            uri="api:///users/{user_id}",
            name="User Profile",
            description="Get user profile by ID",
            mimeType="application/json",
        ),
        Resource(
            uri="api:///posts/{post_id}",
            name="Blog Post",
            description="Get blog post by ID",
            mimeType="application/json",
        ),
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read API resource."""
    if uri.startswith("api:///users/"):
        user_id = uri.split("/")[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config.api_url}/users/{user_id}",
                headers={"Authorization": f"Bearer {config.api_key}"}
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return json.dumps(data, indent=2)

    elif uri.startswith("api:///posts/"):
        post_id = uri.split("/")[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config.api_url}/posts/{post_id}",
                headers={"Authorization": f"Bearer {config.api_key}"}
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return json.dumps(data, indent=2)

    raise ValueError(f"Unknown resource: {uri}")
```
</api_resource>

<configuration_resource>
**Configuration Resource**:

```typescript
// List configuration resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "config:///server",
        name: "Server Configuration",
        description: "Server settings and metadata",
        mimeType: "application/json",
      },
      {
        uri: "config:///api",
        name: "API Configuration",
        description: "API endpoints and credentials",
        mimeType: "application/json",
      },
    ],
  };
});

// Read configuration resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri === "config:///server") {
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(
            {
              name: SERVER_NAME,
              version: SERVER_VERSION,
              capabilities: ["tools", "resources"],
            },
            null,
            2
          ),
        },
      ],
    };
  }

  if (uri === "config:///api") {
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(
            {
              endpoint: config.apiEndpoint,
              timeout: config.timeout,
              // Don't expose secrets!
            },
            null,
            2
          ),
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```
</configuration_resource>

</resource_patterns>

<pagination>

## Pagination for Large Resources

**Paginated Resource Pattern**:

```python
class PaginatedReadArgs(BaseModel):
    """Arguments for paginated resource reading."""
    uri: str
    offset: int = Field(default=0, ge=0, description="Starting offset")
    limit: int = Field(default=100, ge=1, le=1000, description="Items per page")

async def read_large_resource(uri: str, offset: int = 0, limit: int = 100) -> str:
    """Read resource with pagination."""
    if uri == "db:///logs":
        conn = await asyncpg.connect(config.db_url)
        try:
            rows = await conn.fetch(
                "SELECT * FROM logs ORDER BY timestamp DESC OFFSET $1 LIMIT $2",
                offset,
                limit
            )
            total = await conn.fetchval("SELECT COUNT(*) FROM logs")

            return json.dumps({
                "data": [dict(row) for row in rows],
                "pagination": {
                    "offset": offset,
                    "limit": limit,
                    "total": total,
                    "has_more": offset + limit < total,
                },
            }, indent=2, default=str)
        finally:
            await conn.close()

    raise ValueError(f"Unknown resource: {uri}")
```

</pagination>

## Scaling to Large APIs

<large_api_note>
**Building a server that wraps APIs with 20+ operations?**

The patterns above work well for small to medium servers (< 20 tools). However, if you're wrapping a large API (GitHub, Stripe, Slack, etc.), each tool definition consumes tokens in Claude's context window.

**Problem:** 50+ tools can consume 8,000-15,000 tokens just in tool definitions, before any actual conversation begins.

**Solution:** Use the **meta-tools + resources pattern** to achieve 90-98% context reduction by loading operation schemas on-demand instead of upfront.

See [Large API Pattern](large-api-pattern.md) for:
- Complete architecture guide
- Real metrics (15,000 → 300 tokens)
- When to use (and when not to use)
- Implementation examples
- Production results

This pattern is essential for servers wrapping APIs with 50+ operations.
</large_api_note>

---

## Reference: Traditional Pattern

# Traditional MCP Server Pattern (1-2 Operations)

<overview>
For simple MCP servers with 1-2 operations, use the traditional flat tools pattern. This is simpler than on-demand discovery and has negligible context overhead.

**Use when:**
- 1-2 distinct operations total
- All operations will be used in most conversations
- Simplicity is more important than context optimization
</overview>

## Architecture

<structure>
Traditional MCP servers expose each operation as a distinct tool:

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="operation_1", description="...", inputSchema={...}),
        Tool(name="operation_2", description="...", inputSchema={...})
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "operation_1":
        # Implementation
    elif name == "operation_2":
        # Implementation
```

**Context overhead:** ~150-300 tokens per operation (negligible for 1-2 operations)
</structure>

## Python Template

<python_api_integration>
### API Integration Server

```python
# src/server.py
import os
import sys
from typing import Any
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration
API_KEY = os.getenv("YOUR_API_KEY")
if not API_KEY:
    print("ERROR: YOUR_API_KEY environment variable not set", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://api.example.com"

app = Server("your-server-name")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="your_operation_name",
            description="What this operation does",
            inputSchema={
                "type": "object",
                "properties": {
                    "param_name": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param_name"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool."""
    try:
        if name == "your_operation_name":
            param = arguments["param_name"]

            # Make API request
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{BASE_URL}/endpoint",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    params={"param": param}
                )
                response.raise_for_status()
                data = response.json()

            return [TextContent(
                type="text",
                text=f"Result: {data}"
            )]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        print(f"Error in {name}: {e}", file=sys.stderr)
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
</python_api_integration>

<python_file_operations>
### File Operations Server

```python
# src/server.py
import os
from pathlib import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("file-processor")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="read_json",
            description="Read and parse a JSON file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to JSON file"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="write_json",
            description="Write data to a JSON file",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "data": {"type": "object"}
                },
                "required": ["path", "data"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "read_json":
            import json
            path = Path(arguments["path"]).expanduser()
            with open(path) as f:
                data = json.load(f)
            return [TextContent(
                type="text",
                text=json.dumps(data, indent=2)
            )]

        elif name == "write_json":
            import json
            path = Path(arguments["path"]).expanduser()
            with open(path, "w") as f:
                json.dump(arguments["data"], f, indent=2)
            return [TextContent(
                type="text",
                text=f"Wrote data to {path}"
            )]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
</python_file_operations>

<python_custom_tools>
### Custom Tools Server

```python
# src/server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("calculator")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="calculate",
            description="Perform mathematical calculation",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "calculate":
            # Safe evaluation (limited to math operations)
            import ast
            import operator

            operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow
            }

            def eval_expr(node):
                if isinstance(node, ast.Num):
                    return node.n
                elif isinstance(node, ast.BinOp):
                    return operators[type(node.op)](
                        eval_expr(node.left),
                        eval_expr(node.right)
                    )
                raise ValueError("Unsupported operation")

            expr = arguments["expression"]
            tree = ast.parse(expr, mode='eval')
            result = eval_expr(tree.body)

            return [TextContent(
                type="text",
                text=f"{expr} = {result}"
            )]

        raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
</python_custom_tools>

## TypeScript Template

<typescript_api_integration>
### API Integration Server

```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";

const API_KEY = process.env.YOUR_API_KEY;
if (!API_KEY) {
  console.error("ERROR: YOUR_API_KEY environment variable not set");
  process.exit(1);
}

const BASE_URL = "https://api.example.com";

const server = new Server(
  { name: "your-server-name", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "your_operation_name",
      description: "What this operation does",
      inputSchema: {
        type: "object",
        properties: {
          param_name: {
            type: "string",
            description: "Parameter description"
          }
        },
        required: ["param_name"]
      }
    }
  ]
}));

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "your_operation_name") {
      const param = args.param_name;

      const response = await axios.get(`${BASE_URL}/endpoint`, {
        headers: { Authorization: `Bearer ${API_KEY}` },
        params: { param }
      });

      return {
        content: [
          {
            type: "text",
            text: `Result: ${JSON.stringify(response.data)}`
          }
        ]
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    console.error(`Error in ${name}:`, error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`
        }
      ]
    };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```
</typescript_api_integration>

## Adding Multiple Operations

<multiple_operations>
For 2 operations, simply add more tools:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="operation_1", ...),
        Tool(name="operation_2", ...)
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "operation_1":
        # Implementation 1
    elif name == "operation_2":
        # Implementation 2
```

**Threshold:** If you find yourself adding a 3rd operation, consider switching to on-demand discovery pattern (see [large-api-pattern.md](large-api-pattern.md)).
</multiple_operations>

## Error Handling

<error_handling_pattern>
Always return errors as TextContent, never raise exceptions to Claude:

```python
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        # Your implementation
        return [TextContent(type="text", text=result)]
    except Exception as e:
        # Log to stderr for debugging
        print(f"Error in {name}: {e}", file=sys.stderr)

        # Return error to Claude
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
```
</error_handling_pattern>

## Testing

<testing_pattern>
Test standalone before installing:

```bash
cd ~/Developer/mcp/your-server

# Python
uv run python -m src.server
# Should wait for stdin (stdio mode), press Ctrl+C to exit

# TypeScript
node build/index.js
# Should wait for stdin (stdio mode), press Ctrl+C to exit
```

If the server waits for input, it's working correctly.
</testing_pattern>

## When to Migrate

<migration_threshold>
If your server grows to 3+ operations:

1. Read [large-api-pattern.md](large-api-pattern.md)
2. Refactor to on-demand discovery architecture
3. Context savings become significant at this scale (90-98% reduction)

**Signs you need on-demand discovery:**
- Adding 3rd+ operation
- Context overhead > 500 tokens
- Not all operations used per conversation
- Operations group into logical categories
</migration_threshold>

---

## Reference: Typescript Implementation

# TypeScript MCP Server Implementation

<overview>
TypeScript implementation using @modelcontextprotocol/sdk provides full type safety, excellent IDE support, and robust async patterns. This guide covers TypeScript-specific features and best practices.
</overview>

## Project Setup

<package_json>
```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0"
  }
}
```
</package_json>

<tsconfig>
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```
</tsconfig>

## Server Structure

<full_example>
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
  TextContent,
  ImageContent,
  EmbeddedResource,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// Define server metadata
const SERVER_NAME = "my-mcp-server";
const SERVER_VERSION = "1.0.0";

// Type-safe tool definitions
interface ToolHandler {
  name: string;
  description: string;
  schema: z.ZodSchema;
  handler: (args: any) => Promise<TextContent | ImageContent | EmbeddedResource>;
}

// Create server instance
const server = new Server(
  {
    name: SERVER_NAME,
    version: SERVER_VERSION,
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// Tool registry
const tools: Map<string, ToolHandler> = new Map();

// Register a tool
function registerTool(tool: ToolHandler) {
  tools.set(tool.name, tool);
}

// Example: Register a calculation tool
registerTool({
  name: "add_numbers",
  description: "Add two numbers together",
  schema: z.object({
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
  }),
  handler: async (args) => {
    const { a, b } = args;
    return {
      type: "text",
      text: `${a} + ${b} = ${a + b}`,
    };
  },
});

// List tools handler
server.setRequestHandler(ListToolsRequestSchema, async () => {
  const toolsList: Tool[] = Array.from(tools.values()).map((tool) => ({
    name: tool.name,
    description: tool.description,
    inputSchema: zodToJsonSchema(tool.schema),
  }));

  return { tools: toolsList };
});

// Call tool handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const toolName = request.params.name;
  const tool = tools.get(toolName);

  if (!tool) {
    throw new Error(`Unknown tool: ${toolName}`);
  }

  // Validate input with Zod
  const validatedArgs = tool.schema.parse(request.params.arguments);

  // Execute tool handler
  const result = await tool.handler(validatedArgs);

  return {
    content: [result],
  };
});

// Helper: Convert Zod schema to JSON Schema
function zodToJsonSchema(schema: z.ZodSchema): any {
  // Simplified conversion - use zod-to-json-schema package for production
  if (schema instanceof z.ZodObject) {
    const shape = schema.shape;
    const properties: any = {};
    const required: string[] = [];

    for (const [key, value] of Object.entries(shape)) {
      properties[key] = { type: getZodType(value as z.ZodTypeAny) };

      // Add description if available
      const description = (value as any)._def?.description;
      if (description) {
        properties[key].description = description;
      }

      // Track required fields
      if (!(value as z.ZodTypeAny).isOptional()) {
        required.push(key);
      }
    }

    return {
      type: "object",
      properties,
      required,
    };
  }

  return { type: "object" };
}

function getZodType(schema: z.ZodTypeAny): string {
  if (schema instanceof z.ZodString) return "string";
  if (schema instanceof z.ZodNumber) return "number";
  if (schema instanceof z.ZodBoolean) return "boolean";
  if (schema instanceof z.ZodArray) return "array";
  if (schema instanceof z.ZodObject) return "object";
  return "string";
}

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Log to stderr (stdout is reserved for MCP protocol)
  console.error(`${SERVER_NAME} v${SERVER_VERSION} running on stdio`);
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
```
</full_example>

## Type-Safe Patterns

<zod_validation>
**Input Validation with Zod**:

```typescript
import { z } from "zod";

// Define schema with validation rules
const SearchSchema = z.object({
  query: z.string().min(1).max(500),
  limit: z.number().int().min(1).max(100).optional().default(10),
  filters: z.array(z.string()).optional(),
});

type SearchArgs = z.infer<typeof SearchSchema>;

// Use in handler
registerTool({
  name: "search",
  description: "Search for items",
  schema: SearchSchema,
  handler: async (args: SearchArgs) => {
    // args is fully typed: { query: string, limit: number, filters?: string[] }
    const results = await performSearch(args.query, args.limit);
    return {
      type: "text",
      text: JSON.stringify(results, null, 2),
    };
  },
});
```
</zod_validation>

<resource_handlers>
**Resource Handlers**:

```typescript
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  Resource,
} from "@modelcontextprotocol/sdk/types.js";

// List resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const resources: Resource[] = [
    {
      uri: "file:///config.json",
      name: "Configuration",
      description: "Server configuration file",
      mimeType: "application/json",
    },
    {
      uri: "file:///{path}",
      name: "File system",
      description: "Read files from the filesystem",
      mimeType: "text/plain",
    },
  ];

  return { resources };
});

// Read resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const uri = request.params.uri;

  if (uri === "file:///config.json") {
    const config = await readConfig();
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(config, null, 2),
        },
      ],
    };
  }

  if (uri.startsWith("file:///")) {
    const path = uri.slice(8); // Remove "file:///"
    const content = await fs.readFile(path, "utf-8");
    return {
      contents: [
        {
          uri,
          mimeType: "text/plain",
          text: content,
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});
```
</resource_handlers>

<prompt_handlers>
**Prompt Templates**:

```typescript
import {
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
  Prompt,
  PromptMessage,
} from "@modelcontextprotocol/sdk/types.js";

// List prompts
server.setRequestHandler(ListPromptsRequestSchema, async () => {
  const prompts: Prompt[] = [
    {
      name: "code_review",
      description: "Review code for best practices",
      arguments: [
        {
          name: "language",
          description: "Programming language",
          required: true,
        },
        {
          name: "code",
          description: "Code to review",
          required: true,
        },
      ],
    },
  ];

  return { prompts };
});

// Get prompt
server.setRequestHandler(GetPromptRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "code_review") {
    const language = args?.language;
    const code = args?.code;

    const messages: PromptMessage[] = [
      {
        role: "user",
        content: {
          type: "text",
          text: `Review this ${language} code for best practices:\n\n${code}`,
        },
      },
    ];

    return {
      description: `Code review for ${language}`,
      messages,
    };
  }

  throw new Error(`Unknown prompt: ${name}`);
});
```
</prompt_handlers>

## Error Handling

<error_patterns>
```typescript
import { McpError, ErrorCode } from "@modelcontextprotocol/sdk/types.js";

// Custom error handling
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const tool = tools.get(request.params.name);

    if (!tool) {
      throw new McpError(
        ErrorCode.MethodNotFound,
        `Tool not found: ${request.params.name}`
      );
    }

    // Validate arguments
    let validatedArgs;
    try {
      validatedArgs = tool.schema.parse(request.params.arguments);
    } catch (error) {
      if (error instanceof z.ZodError) {
        throw new McpError(
          ErrorCode.InvalidParams,
          `Invalid arguments: ${error.message}`
        );
      }
      throw error;
    }

    // Execute handler with timeout
    const result = await Promise.race([
      tool.handler(validatedArgs),
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error("Tool execution timeout")), 30000)
      ),
    ]);

    return { content: [result] };
  } catch (error) {
    // Log to stderr
    console.error(`Tool execution error:`, error);

    // Re-throw MCP errors
    if (error instanceof McpError) {
      throw error;
    }

    // Wrap other errors
    throw new McpError(
      ErrorCode.InternalError,
      error instanceof Error ? error.message : "Unknown error"
    );
  }
});
```
</error_patterns>

## Advanced Features

<streaming>
**Streaming Responses** (for long-running operations):

```typescript
// Note: Basic MCP doesn't support streaming yet, but you can chunk responses
async function handleLargeDataTool(args: any): Promise<TextContent> {
  const data = await fetchLargeDataset(args.query);

  // Split into manageable chunks
  const chunks = chunkData(data, 1000);

  return {
    type: "text",
    text: chunks.map((chunk, i) =>
      `Chunk ${i + 1}/${chunks.length}:\n${chunk}`
    ).join("\n\n"),
  };
}
```
</streaming>

<state_management>
**State Management**:

```typescript
// Maintain server state
class ServerState {
  private cache: Map<string, any> = new Map();
  private connections: Set<string> = new Set();

  setCache(key: string, value: any, ttl: number = 60000) {
    this.cache.set(key, value);
    setTimeout(() => this.cache.delete(key), ttl);
  }

  getCache(key: string): any | undefined {
    return this.cache.get(key);
  }

  addConnection(id: string) {
    this.connections.add(id);
    console.error(`Connection added: ${id} (total: ${this.connections.size})`);
  }

  removeConnection(id: string) {
    this.connections.delete(id);
    console.error(`Connection removed: ${id} (total: ${this.connections.size})`);
  }
}

const state = new ServerState();

// Use state in tools
registerTool({
  name: "cached_fetch",
  description: "Fetch with caching",
  schema: z.object({ url: z.string().url() }),
  handler: async (args) => {
    const cached = state.getCache(args.url);
    if (cached) {
      return { type: "text", text: cached };
    }

    const response = await fetch(args.url);
    const data = await response.text();
    state.setCache(args.url, data);

    return { type: "text", text: data };
  },
});
```
</state_management>

## Environment Configuration

<env_config>
```typescript
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

interface Config {
  apiKey: string;
  apiEndpoint: string;
  maxRetries: number;
  debug: boolean;
}

function loadConfig(): Config {
  const apiKey = process.env.API_KEY;
  if (!apiKey) {
    throw new Error("API_KEY environment variable is required");
  }

  return {
    apiKey,
    apiEndpoint: process.env.API_ENDPOINT || "https://api.example.com",
    maxRetries: parseInt(process.env.MAX_RETRIES || "3"),
    debug: process.env.DEBUG === "true",
  };
}

const config = loadConfig();

// Use in tools
registerTool({
  name: "api_call",
  description: "Call external API",
  schema: z.object({ endpoint: z.string() }),
  handler: async (args) => {
    const response = await fetch(`${config.apiEndpoint}${args.endpoint}`, {
      headers: {
        Authorization: `Bearer ${config.apiKey}`,
      },
    });

    const data = await response.json();
    return { type: "text", text: JSON.stringify(data, null, 2) };
  },
});
```

**.env file**:
```
API_KEY=your_api_key_here
API_ENDPOINT=https://api.example.com
MAX_RETRIES=3
DEBUG=false
```
</env_config>

## Build and Distribution

<build_script>
```json
{
  "scripts": {
    "build": "tsc && chmod +x dist/index.js",
    "prepublishOnly": "npm run build",
    "start": "node dist/index.js"
  },
  "bin": {
    "my-mcp-server": "./dist/index.js"
  }
}
```

Add shebang to src/index.ts:
```typescript
#!/usr/bin/env node

// ... rest of server code
```
</build_script>

<publishing>
**Publish to npm**:

```bash
npm login
npm publish
```

Users install with:
```bash
npm install -g my-mcp-server
```

Claude Desktop config:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "my-mcp-server"
    }
  }
}
```
</publishing>

---

## Reference: Validation Checkpoints

# Validation Checkpoints

Reusable validation commands for each step.

## api-research

```bash
# Check document exists
test -f ~/Developer/mcp/{server-name}/API_RESEARCH.md && echo "✓ Research doc exists" || echo "✗ Missing API_RESEARCH.md"

# Verify required sections present
grep -q "## Authentication" ~/Developer/mcp/{server-name}/API_RESEARCH.md && echo "✓ Authentication documented" || echo "✗ Missing authentication"
grep -q "## Official SDK" ~/Developer/mcp/{server-name}/API_RESEARCH.md && echo "✓ SDK documented" || echo "✗ Missing SDK info"
grep -q "## Required Endpoints" ~/Developer/mcp/{server-name}/API_RESEARCH.md && echo "✓ Endpoints documented" || echo "✗ Missing endpoints"
grep -q "## Rate Limits" ~/Developer/mcp/{server-name}/API_RESEARCH.md && echo "✓ Rate limits documented" || echo "✗ Missing rate limits"

# Verify recency (2024-2025 sources only)
grep -E "(2024|2025)" ~/Developer/mcp/{server-name}/API_RESEARCH.md && echo "✓ Sources are current" || echo "✗ No 2024-2025 sources found"

# Count verified endpoints
VERIFIED_COUNT=$(grep -c "Verified: ✓" ~/Developer/mcp/{server-name}/API_RESEARCH.md)
echo "Verified endpoints: $VERIFIED_COUNT (expected: {count from Step 0})"
```

**Required before Step 2:**
- [ ] API_RESEARCH.md exists
- [ ] All required sections present
- [ ] Every planned operation has verified endpoint
- [ ] All sources dated 2024-2025
- [ ] Endpoint count matches Step 0

## project-structure

```bash
# Verify structure
test -d ~/Developer/mcp/{server-name} && echo "✓ Directory exists" || echo "✗ Missing"
test -f ~/Developer/mcp/{server-name}/pyproject.toml && echo "✓ Project initialized" || echo "✗ Not initialized"
```

**Required before Step 4:**
- [ ] Directory exists
- [ ] Project initialized

## code-syntax

```bash
# Verify code exists
test -f ~/Developer/mcp/{server-name}/src/server.py && echo "✓ Code created" || echo "✗ Missing"

# Check syntax (Python)
cd ~/Developer/mcp/{server-name}
python -m py_compile src/server.py && echo "✓ Valid syntax" || echo "✗ Syntax error"

# OR build (TypeScript)
npm run build && echo "✓ Build successful" || echo "✗ Build failed"
```

**Required before Step 5:**
- [ ] Code file exists
- [ ] Syntax valid / build successful

## env-vars

```bash
# Check variables set (without showing values)
for var in {ENV_VAR1} {ENV_VAR2}; do
  [ -z "${!var}" ] && echo "✗ $var not set" || echo "✓ $var set"
done
```

**Required before Step 6:**
- [ ] All environment variables set

## claude-code-install

```bash
# Verify installation
claude mcp list | grep {server-name}
# Expected: "{server-name}: ... - ✓ Connected"
```

**If not connected, check logs:**
```bash
tail -50 ~/Library/Logs/Claude/mcp-server-{server-name}.log
```

**Required before Step 7:**
- [ ] Server shows "✓ Connected" status

## claude-desktop-config

```bash
# Verify config entry exists
jq '.mcpServers | has("{server-name}")' "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
# Expected: true
```

**Required before Step 8:**
- [ ] Config entry exists for server
