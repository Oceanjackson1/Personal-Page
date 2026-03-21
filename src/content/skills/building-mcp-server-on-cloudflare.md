---
title: "Building MCP Server On Cloudflare"
description: "Builds remote MCP (Model Context Protocol) servers on Cloudflare Workers with tools, OAuth authentication, and production deployment. Generates server code, configures auth providers, and deploys to Workers.  Use when: user wants to 'build MCP ser..."
category: "devops"
source: "community"
author: "Community"
tags: ["building", "mcp", "server", "cloudflare"]
date: 2026-03-20
---

# Building MCP Servers on Cloudflare

Your knowledge of the MCP SDK and Cloudflare Workers integration may be outdated. **Prefer retrieval over pre-training** for any MCP server task.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| MCP docs | `https://developers.cloudflare.com/agents/mcp/` | Server setup, auth, deployment |
| MCP spec | `https://modelcontextprotocol.io/` | Protocol spec, tool/resource definitions |
| Workers docs | Search tool or `https://developers.cloudflare.com/workers/` | Runtime APIs, bindings, config |

## When to Use

- User wants to build a remote MCP server
- User needs to expose tools via MCP
- User asks about MCP authentication or OAuth
- User wants to deploy MCP to Cloudflare Workers

## Prerequisites

- Cloudflare account with Workers enabled
- Node.js 18+ and npm/pnpm/yarn
- Wrangler CLI (`npm install -g wrangler`)

## Quick Start

### Option 1: Public Server (No Auth)

```bash
npm create cloudflare@latest -- my-mcp-server \
  --template=cloudflare/ai/demos/remote-mcp-authless
cd my-mcp-server
npm start
```

Server runs at `http://localhost:8788/mcp`

### Option 2: Authenticated Server (OAuth)

```bash
npm create cloudflare@latest -- my-mcp-server \
  --template=cloudflare/ai/demos/remote-mcp-github-oauth
cd my-mcp-server
```

Requires OAuth app setup. See [references/oauth-setup.md](references/oauth-setup.md).

## Core Workflow

### Step 1: Define Tools

Tools are functions MCP clients can call. Define them using `server.tool()`:

```typescript
import { McpAgent } from "agents/mcp";
import { z } from "zod";

export class MyMCP extends McpAgent {
  server = new Server({ name: "my-mcp", version: "1.0.0" });

  async init() {
    // Simple tool with parameters
    this.server.tool(
      "add",
      { a: z.number(), b: z.number() },
      async ({ a, b }) => ({
        content: [{ type: "text", text: String(a + b) }],
      })
    );

    // Tool that calls external API
    this.server.tool(
      "get_weather",
      { city: z.string() },
      async ({ city }) => {
        const response = await fetch(`https://api.weather.com/${city}`);
        const data = await response.json();
        return {
          content: [{ type: "text", text: JSON.stringify(data) }],
        };
      }
    );
  }
}
```

### Step 2: Configure Entry Point

**Public server** (`src/index.ts`):

```typescript
import { MyMCP } from "./mcp";

export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const url = new URL(request.url);
    if (url.pathname === "/mcp") {
      return MyMCP.serveSSE("/mcp").fetch(request, env, ctx);
    }
    return new Response("MCP Server", { status: 200 });
  },
};

export { MyMCP };
```

**Authenticated server** — See [references/oauth-setup.md](references/oauth-setup.md).

### Step 3: Test Locally

```bash
# Start server
npm start

# In another terminal, test with MCP Inspector
npx @modelcontextprotocol/inspector@latest
# Open http://localhost:5173, enter http://localhost:8788/mcp
```

### Step 4: Deploy

```bash
npx wrangler deploy
```

Server accessible at `https://[worker-name].[account].workers.dev/mcp`

### Step 5: Connect Clients

**Claude Desktop** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["mcp-remote", "https://my-mcp.workers.dev/mcp"]
    }
  }
}
```

Restart Claude Desktop after updating config.

## Tool Patterns

### Return Types

```typescript
// Text response
return { content: [{ type: "text", text: "result" }] };

// Multiple content items
return {
  content: [
    { type: "text", text: "Here's the data:" },
    { type: "text", text: JSON.stringify(data, null, 2) },
  ],
};
```

### Input Validation with Zod

```typescript
this.server.tool(
  "create_user",
  {
    email: z.string().email(),
    name: z.string().min(1).max(100),
    role: z.enum(["admin", "user", "guest"]),
    age: z.number().int().min(0).optional(),
  },
  async (params) => {
    // params are fully typed and validated
  }
);
```

### Accessing Environment/Bindings

```typescript
export class MyMCP extends McpAgent<Env> {
  async init() {
    this.server.tool("query_db", { sql: z.string() }, async ({ sql }) => {
      // Access D1 binding
      const result = await this.env.DB.prepare(sql).all();
      return { content: [{ type: "text", text: JSON.stringify(result) }] };
    });
  }
}
```

## Authentication

For OAuth-protected servers, see [references/oauth-setup.md](references/oauth-setup.md).

Supported providers:
- GitHub
- Google
- Auth0
- Stytch
- WorkOS
- Any OAuth 2.0 compliant provider

## Wrangler Configuration

Minimal `wrangler.toml`:

```toml
name = "my-mcp-server"
main = "src/index.ts"
compatibility_date = "2024-12-01"

[durable_objects]
bindings = [{ name = "MCP", class_name = "MyMCP" }]

[[migrations]]
tag = "v1"
new_classes = ["MyMCP"]
```

With bindings (D1, KV, etc.):

```toml
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxx"

[[kv_namespaces]]
binding = "KV"
id = "xxx"
```

## Common Issues

### "Tool not found" in Client

1. Verify tool name matches exactly (case-sensitive)
2. Ensure `init()` registers tools before connections
3. Check server logs: `wrangler tail`

### Connection Fails

1. Confirm endpoint path is `/mcp`
2. Check CORS if browser-based client
3. Verify Worker is deployed: `wrangler deployments list`

### OAuth Redirect Errors

1. Callback URL must match OAuth app config exactly
2. Check `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` are set
3. For local dev, use `http://localhost:8788/callback`

## References

- [references/examples.md](references/examples.md) — Official templates and production examples
- [references/oauth-setup.md](references/oauth-setup.md) — OAuth provider configuration
- [references/tool-patterns.md](references/tool-patterns.md) — Advanced tool examples
- [references/troubleshooting.md](references/troubleshooting.md) — Error codes and fixes

---

## Reference: Examples

# Project Bootstrapping

Instructions for creating new MCP server projects.

---

## Create Commands

Execute in terminal to generate a new project:

**Without authentication:**

```bash
npm create cloudflare@latest -- my-mcp-server \
  --template=cloudflare/ai/demos/remote-mcp-authless
```

**With GitHub login:**

```bash
npm create cloudflare@latest -- my-mcp-server \
  --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

**With Google login:**

```bash
npm create cloudflare@latest -- my-mcp-server \
  --template=cloudflare/ai/demos/remote-mcp-google-oauth
```

---

## Additional Boilerplate Locations

**Main repository:** `github.com/cloudflare/ai` (check demos directory)

Other authentication providers:
- Auth0
- WorkOS AuthKit
- Logto
- Descope
- Stytch

**Cloudflare tooling:** `github.com/cloudflare/mcp-server-cloudflare`

---

## Selection Matrix

| Goal | Boilerplate |
|------|-------------|
| Testing/learning | authless |
| GitHub API access | github-oauth |
| Google API access | google-oauth |
| Enterprise auth | auth0 / authkit |
| Slack apps | slack-oauth |
| Zero Trust | cf-access |

---

## Platform Documentation

- developers.cloudflare.com/agents/model-context-protocol/
- developers.cloudflare.com/agents/guides/remote-mcp-server/
- developers.cloudflare.com/agents/guides/test-remote-mcp-server/
- developers.cloudflare.com/agents/model-context-protocol/authorization/

---

## Commands Reference

**Local execution:**

```bash
cd my-mcp-server
npm install
npm start
# Accessible at http://localhost:8788/mcp
```

**Production push:**

```bash
npx wrangler deploy
# Accessible at https://[worker-name].[subdomain].workers.dev/mcp
```

**Claude Desktop setup** (modify `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["mcp-remote", "https://my-mcp-server.my-account.workers.dev/mcp"]
    }
  }
}
```

**Inspector testing:**

```bash
npx @modelcontextprotocol/inspector@latest
# Launch browser at http://localhost:5173
# Input your server URL: http://localhost:8788/mcp
```

---

## Help Channels

- Cloudflare Discord
- GitHub discussions on cloudflare/ai repository

---

## Reference: Oauth Setup

# Securing MCP Servers

MCP servers require authentication to ensure only trusted users can access them. The MCP specification uses OAuth 2.1 for authentication between clients and servers.

Cloudflare's `workers-oauth-provider` handles token management, client registration, and access token validation automatically.

## Basic Setup

```typescript
import { OAuthProvider } from "@cloudflare/workers-oauth-provider";
import { createMcpHandler } from "agents/mcp";

const apiHandler = {
  async fetch(request: Request, env: unknown, ctx: ExecutionContext) {
    return createMcpHandler(server)(request, env, ctx);
  }
};

export default new OAuthProvider({
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/oauth/token",
  clientRegistrationEndpoint: "/oauth/register",
  apiRoute: "/mcp",
  apiHandler: apiHandler,
  defaultHandler: AuthHandler
});
```

## Proxy Server Pattern

MCP servers often act as OAuth clients too. Your server sits between Claude Desktop and a third-party API like GitHub. To Claude, you're a server. To GitHub, you're a client. This lets users authenticate with their GitHub credentials.

Building a secure proxy server requires careful attention to several security concerns.

---

## Security Requirements

### Redirect URI Validation

The `workers-oauth-provider` validates that `redirect_uri` in authorization requests matches registered URIs. This prevents attackers from redirecting authorization codes to malicious endpoints.

### Consent Dialog

When proxying to third-party providers, implement your own consent dialog before forwarding users upstream. This prevents the "confused deputy" problem where attackers exploit cached consent.

Your consent dialog should:
- Identify the requesting MCP client by name
- Display the specific scopes being requested

---

## CSRF Protection

Prevent attackers from tricking users into approving malicious OAuth clients. Use a random token stored in a secure cookie.

```typescript
// Generate token when showing consent form
function generateCSRFProtection(): { token: string; setCookie: string } {
  const token = crypto.randomUUID();
  const setCookie = `__Host-CSRF_TOKEN=${token}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=600`;
  return { token, setCookie };
}

// Validate token when user approves
function validateCSRFToken(formData: FormData, request: Request): { clearCookie: string } {
  const tokenFromForm = formData.get("csrf_token");
  const cookieHeader = request.headers.get("Cookie") || "";
  const tokenFromCookie = cookieHeader
    .split(";")
    .find((c) => c.trim().startsWith("__Host-CSRF_TOKEN="))
    ?.split("=")[1];

  if (!tokenFromForm || !tokenFromCookie || tokenFromForm !== tokenFromCookie) {
    throw new Error("CSRF token mismatch");
  }

  return {
    clearCookie: `__Host-CSRF_TOKEN=; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=0`
  };
}
```

Include the token as a hidden form field:

```html
<input type="hidden" name="csrf_token" value="${csrfToken}" />
```

---

## Input Sanitization

Client-controlled content (names, logos, URIs) can execute malicious scripts if not sanitized. Treat all client metadata as untrusted.

```typescript
function sanitizeText(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function sanitizeUrl(url: string): string {
  if (!url) return "";
  try {
    const parsed = new URL(url);
    if (!["http:", "https:"].includes(parsed.protocol)) {
      return "";
    }
    return url;
  } catch {
    return "";
  }
}
```

**Required protections:**
- Client names/descriptions: HTML-escape before rendering
- Logo URLs: Allow only `http:` and `https:` schemes
- Client URIs: Same as logo URLs
- Scopes: Treat as text, HTML-escape

---

## Content Security Policy

CSP headers block dangerous content and provide defense in depth.

```typescript
function buildSecurityHeaders(setCookie: string, nonce?: string): HeadersInit {
  const cspDirectives = [
    "default-src 'none'",
    "script-src 'self'" + (nonce ? ` 'nonce-${nonce}'` : ""),
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' https:",
    "font-src 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "connect-src 'self'"
  ].join("; ");

  return {
    "Content-Security-Policy": cspDirectives,
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Content-Type": "text/html; charset=utf-8",
    "Set-Cookie": setCookie
  };
}
```

---

## State Management

Ensure the same user that hits authorize reaches the callback. Use a random state token stored in KV with short expiration.

```typescript
// Create state before redirecting to upstream provider
async function createOAuthState(
  oauthReqInfo: AuthRequest,
  kv: KVNamespace
): Promise<{ stateToken: string }> {
  const stateToken = crypto.randomUUID();
  await kv.put(`oauth:state:${stateToken}`, JSON.stringify(oauthReqInfo), {
    expirationTtl: 600
  });
  return { stateToken };
}

// Bind state to browser session via hashed cookie
async function bindStateToSession(stateToken: string): Promise<{ setCookie: string }> {
  const encoder = new TextEncoder();
  const data = encoder.encode(stateToken);
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");

  return {
    setCookie: `__Host-CONSENTED_STATE=${hashHex}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=600`
  };
}

// Validate in callback - check both KV and session cookie
async function validateOAuthState(
  request: Request,
  kv: KVNamespace
): Promise<{ oauthReqInfo: AuthRequest; clearCookie: string }> {
  const url = new URL(request.url);
  const stateFromQuery = url.searchParams.get("state");

  if (!stateFromQuery) {
    throw new Error("Missing state parameter");
  }

  // Check KV
  const storedDataJson = await kv.get(`oauth:state:${stateFromQuery}`);
  if (!storedDataJson) {
    throw new Error("Invalid or expired state");
  }

  // Check session cookie matches
  const cookieHeader = request.headers.get("Cookie") || "";
  const consentedStateHash = cookieHeader
    .split(";")
    .find((c) => c.trim().startsWith("__Host-CONSENTED_STATE="))
    ?.split("=")[1];

  if (!consentedStateHash) {
    throw new Error("Missing session binding cookie");
  }

  // Hash state and compare
  const encoder = new TextEncoder();
  const hashBuffer = await crypto.subtle.digest("SHA-256", encoder.encode(stateFromQuery));
  const stateHash = Array.from(new Uint8Array(hashBuffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");

  if (stateHash !== consentedStateHash) {
    throw new Error("State token does not match session");
  }

  await kv.delete(`oauth:state:${stateFromQuery}`);

  return {
    oauthReqInfo: JSON.parse(storedDataJson),
    clearCookie: `__Host-CONSENTED_STATE=; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=0`
  };
}
```

---

## Approved Clients Registry

Maintain a registry of approved client IDs per user. Store in a cryptographically signed cookie with HMAC-SHA256.

```typescript
export async function addApprovedClient(
  request: Request,
  clientId: string,
  cookieSecret: string
): Promise<string> {
  const existingClients = await getApprovedClientsFromCookie(request, cookieSecret) || [];
  const updatedClients = Array.from(new Set([...existingClients, clientId]));

  const payload = JSON.stringify(updatedClients);
  const signature = await signData(payload, cookieSecret);
  const cookieValue = `${signature}.${btoa(payload)}`;

  return `__Host-APPROVED_CLIENTS=${cookieValue}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=2592000`;
}
```

When reading the cookie, verify the signature before trusting data. If client isn't approved, show consent dialog.

---

## Cookie Security

### Why `__Host-` prefix?

The `__Host-` prefix prevents subdomain attacks on `*.workers.dev` domains. Requirements:
- Must have `Secure` flag (HTTPS only)
- Must have `Path=/`
- Must not have `Domain` attribute

Without this prefix, an attacker on `evil.workers.dev` could set cookies for your `mcp-server.workers.dev` domain.

### Multiple OAuth Providers

If running multiple OAuth flows on the same domain, namespace your cookies:
- `__Host-CSRF_TOKEN_GITHUB` vs `__Host-CSRF_TOKEN_GOOGLE`
- `__Host-APPROVED_CLIENTS_GITHUB` vs `__Host-APPROVED_CLIENTS_GOOGLE`

---

## Inline JavaScript

If your consent dialog needs inline JavaScript, use data attributes and nonces:

```typescript
const nonce = crypto.randomUUID();

const html = `
  <script nonce="${nonce}" data-redirect-url="${sanitizeUrl(redirectUrl)}">
    setTimeout(() => {
      const script = document.querySelector('script[data-redirect-url]');
      window.location.href = script.dataset.redirectUrl;
    }, 2000);
  </script>
`;

return new Response(html, {
  headers: buildSecurityHeaders(setCookie, nonce)
});
```

Data attributes store user-controlled data separately from executable code. Nonces with CSP allow your specific script while blocking injected scripts.

---

## Provider-Specific Setup

### GitHub

1. Create OAuth App at github.com/settings/developers
2. Set callback URL: `https://[worker].workers.dev/callback`
3. Store secrets:
   ```bash
   wrangler secret put GITHUB_CLIENT_ID
   wrangler secret put GITHUB_CLIENT_SECRET
   ```

### Google

1. Create OAuth Client at console.cloud.google.com/apis/credentials
2. Set authorized redirect URI
3. Scopes: `openid email profile`

### Auth0

1. Create Regular Web Application in Auth0 Dashboard
2. Set allowed callback URLs
3. Endpoints: `https://${AUTH0_DOMAIN}/authorize`, `/oauth/token`, `/userinfo`

---

## References

- [MCP Authorization Spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [RFC 9700 - OAuth Security](https://www.rfc-editor.org/rfc/rfc9700)

---

## Reference: Troubleshooting

# MCP Server Troubleshooting

Common errors and solutions for MCP servers on Cloudflare.

## Connection Issues

### "Failed to connect to MCP server"

**Symptoms:** Client cannot establish connection to deployed server.

**Causes & Solutions:**

1. **Wrong URL path**
   ```
   # Wrong
   https://my-server.workers.dev/

   # Correct
   https://my-server.workers.dev/mcp
   ```

2. **Worker not deployed**
   ```bash
   wrangler deployments list
   # If empty, deploy first:
   wrangler deploy
   ```

3. **Worker crashed on startup**
   ```bash
   wrangler tail
   # Check for initialization errors
   ```

### "WebSocket connection failed"

MCP uses SSE (Server-Sent Events), not WebSockets. Ensure your client is configured for SSE transport:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["mcp-remote", "https://my-server.workers.dev/mcp"]
    }
  }
}
```

### CORS Errors in Browser

If calling from browser-based client:

```typescript
// Add CORS headers to your worker
export default {
  async fetch(request: Request, env: Env) {
    // Handle preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    const response = await handleRequest(request, env);

    // Add CORS headers to response
    const headers = new Headers(response.headers);
    headers.set("Access-Control-Allow-Origin", "*");

    return new Response(response.body, {
      status: response.status,
      headers,
    });
  },
};
```

## Tool Errors

### "Tool not found: [tool_name]"

**Causes:**

1. Tool not registered in `init()`
2. Tool name mismatch (case-sensitive)
3. `init()` threw an error before registering tool

**Debug:**

```typescript
async init() {
  console.log("Registering tools...");

  this.server.tool("my_tool", { ... }, async () => { ... });

  console.log("Tools registered:", this.server.listTools());
}
```

Check logs: `wrangler tail`

### "Invalid parameters for tool"

Zod validation failed. Check parameter schema:

```typescript
// Schema expects number, client sent string
this.server.tool(
  "calculate",
  { value: z.number() },  // Client must send number, not "123"
  async ({ value }) => { ... }
);

// Fix: Coerce string to number
this.server.tool(
  "calculate",
  { value: z.coerce.number() },  // "123" → 123
  async ({ value }) => { ... }
);
```

### Tool Timeout

Workers have CPU time limits (10-30ms for free, longer for paid). For long operations:

```typescript
this.server.tool(
  "long_operation",
  { ... },
  async (params) => {
    // Break into smaller chunks
    // Or use Queues/Durable Objects for background work

    // Don't do this:
    // await sleep(5000);  // Will timeout

    return { content: [{ type: "text", text: "Queued for processing" }] };
  }
);
```

## Authentication Errors

### "401 Unauthorized"

OAuth token missing or expired.

1. **Check client is handling OAuth flow**
2. **Verify secrets are set:**
   ```bash
   wrangler secret list
   # Should show GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
   ```

3. **Check KV namespace exists:**
   ```bash
   wrangler kv namespace list
   # Should show OAUTH_KV
   ```

### "Invalid redirect_uri"

OAuth callback URL doesn't match app configuration.

**Local development:**
- OAuth app callback: `http://localhost:8788/callback`

**Production:**
- OAuth app callback: `https://[worker-name].[account].workers.dev/callback`

Must match EXACTLY (including trailing slash or lack thereof).

### "State mismatch" / CSRF Error

State parameter validation failed.

1. **Clear browser cookies and retry**
2. **Check KV is storing state:**
   ```typescript
   // In your auth handler
   console.log("Storing state:", state);
   await env.OAUTH_KV.put(`state:${state}`, "1", { expirationTtl: 600 });
   ```

3. **Verify same domain for all requests**

## Binding Errors

### "Binding not found: [BINDING_NAME]"

Binding not in `wrangler.toml` or not deployed.

```toml
# wrangler.toml
[[d1_databases]]
binding = "DB"           # Must match env.DB in code
database_name = "mydb"
database_id = "xxx-xxx"
```

After adding bindings: `wrangler deploy`

### "D1_ERROR: no such table"

Migrations not applied.

```bash
# Local
wrangler d1 migrations apply DB_NAME --local

# Production
wrangler d1 migrations apply DB_NAME
```

### Durable Object Not Found

```toml
# wrangler.toml must have:
[durable_objects]
bindings = [{ name = "MCP", class_name = "MyMCP" }]

[[migrations]]
tag = "v1"
new_classes = ["MyMCP"]
```

And class must be exported:

```typescript
export { MyMCP };  // Don't forget this!
```

## Deployment Errors

### "Class MyMCP is not exported"

```typescript
// src/index.ts - Must export the class
export { MyMCP } from "./mcp";

// OR in same file
export class MyMCP extends McpAgent { ... }
```

### "Migration required"

New Durable Object class needs migration:

```toml
# Add to wrangler.toml
[[migrations]]
tag = "v2"  # Increment version
new_classes = ["NewClassName"]
# Or for renames:
# renamed_classes = [{ from = "OldName", to = "NewName" }]
```

### Build Errors

```bash
# Clear cache and rebuild
rm -rf node_modules .wrangler
npm install
wrangler deploy
```

## Debugging Tips

### Enable Verbose Logging

```typescript
export class MyMCP extends McpAgent {
  async init() {
    console.log("MCP Server initializing...");
    console.log("Environment:", Object.keys(this.env));

    this.server.tool("test", {}, async () => {
      console.log("Test tool called");
      return { content: [{ type: "text", text: "OK" }] };
    });

    console.log("Tools registered");
  }
}
```

View logs:
```bash
wrangler tail --format pretty
```

### Test Locally First

```bash
npm start
npx @modelcontextprotocol/inspector@latest
```

Always verify tools work locally before deploying.

### Check Worker Health

```bash
# List deployments
wrangler deployments list

# View recent logs
wrangler tail

# Check worker status
curl -I https://your-worker.workers.dev/mcp
```
