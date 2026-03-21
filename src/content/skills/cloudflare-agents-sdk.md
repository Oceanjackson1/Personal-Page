---
title: "Cloudflare Agents SDK"
description: "Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks, MCP servers, or chat applications. Covers Agent class, state management, callable RPC, Wo..."
category: "devops"
source: "community"
author: "Community"
tags: ["cloudflare", "agents", "sdk"]
date: 2026-03-20
---

# Cloudflare Agents SDK

Your knowledge of the Agents SDK may be outdated. **Prefer retrieval over pre-training** for any Agents SDK task.

## Retrieval Sources

Fetch current docs from `https://github.com/cloudflare/agents/tree/main/docs` before implementing.

| Topic | Doc | Use for |
|-------|-----|---------|
| Getting started | `docs/getting-started.md` | First agent, project setup |
| State | `docs/state.md` | `setState`, `validateStateChange`, persistence |
| Routing | `docs/routing.md` | URL patterns, `routeAgentRequest`, `basePath` |
| Callable methods | `docs/callable-methods.md` | `@callable`, RPC, streaming, timeouts |
| Scheduling | `docs/scheduling.md` | `schedule()`, `scheduleEvery()`, cron |
| Workflows | `docs/workflows.md` | `AgentWorkflow`, durable multi-step tasks |
| HTTP/WebSockets | `docs/http-websockets.md` | Lifecycle hooks, hibernation |
| Email | `docs/email.md` | Email routing, secure reply resolver |
| MCP client | `docs/mcp-client.md` | Connecting to MCP servers |
| MCP server | `docs/mcp-servers.md` | Building MCP servers with `McpAgent` |
| Client SDK | `docs/client-sdk.md` | `useAgent`, `useAgentChat`, React hooks |
| Human-in-the-loop | `docs/human-in-the-loop.md` | Approval flows, pausing workflows |
| Resumable streaming | `docs/resumable-streaming.md` | Stream recovery on disconnect |

Cloudflare docs: https://developers.cloudflare.com/agents/

## Capabilities

The Agents SDK provides:

- **Persistent state** - SQLite-backed, auto-synced to clients
- **Callable RPC** - `@callable()` methods invoked over WebSocket
- **Scheduling** - One-time, recurring (`scheduleEvery`), and cron tasks
- **Workflows** - Durable multi-step background processing via `AgentWorkflow`
- **MCP integration** - Connect to MCP servers or build your own with `McpAgent`
- **Email handling** - Receive and reply to emails with secure routing
- **Streaming chat** - `AIChatAgent` with resumable streams
- **React hooks** - `useAgent`, `useAgentChat` for client apps

## FIRST: Verify Installation

```bash
npm ls agents  # Should show agents package
```

If not installed:
```bash
npm install agents
```

## Wrangler Configuration

```jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "MyAgent", "class_name": "MyAgent" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyAgent"] }]
}
```

## Agent Class

```typescript
import { Agent, routeAgentRequest, callable } from "agents";

type State = { count: number };

export class Counter extends Agent<Env, State> {
  initialState = { count: 0 };

  // Validation hook - runs before state persists (sync, throwing rejects the update)
  validateStateChange(nextState: State, source: Connection | "server") {
    if (nextState.count < 0) throw new Error("Count cannot be negative");
  }

  // Notification hook - runs after state persists (async, non-blocking)
  onStateUpdate(state: State, source: Connection | "server") {
    console.log("State updated:", state);
  }

  @callable()
  increment() {
    this.setState({ count: this.state.count + 1 });
    return this.state.count;
  }
}

export default {
  fetch: (req, env) => routeAgentRequest(req, env) ?? new Response("Not found", { status: 404 })
};
```

## Routing

Requests route to `/agents/{agent-name}/{instance-name}`:

| Class | URL |
|-------|-----|
| `Counter` | `/agents/counter/user-123` |
| `ChatRoom` | `/agents/chat-room/lobby` |

Client: `useAgent({ agent: "Counter", name: "user-123" })`

## Core APIs

| Task | API |
|------|-----|
| Read state | `this.state.count` |
| Write state | `this.setState({ count: 1 })` |
| SQL query | `` this.sql`SELECT * FROM users WHERE id = ${id}` `` |
| Schedule (delay) | `await this.schedule(60, "task", payload)` |
| Schedule (cron) | `await this.schedule("0 * * * *", "task", payload)` |
| Schedule (interval) | `await this.scheduleEvery(30, "poll")` |
| RPC method | `@callable() myMethod() { ... }` |
| Streaming RPC | `@callable({ streaming: true }) stream(res) { ... }` |
| Start workflow | `await this.runWorkflow("ProcessingWorkflow", params)` |

## React Client

```tsx
import { useAgent } from "agents/react";

function App() {
  const [state, setLocalState] = useState({ count: 0 });

  const agent = useAgent({
    agent: "Counter",
    name: "my-instance",
    onStateUpdate: (newState) => setLocalState(newState),
    onIdentity: (name, agentType) => console.log(`Connected to ${name}`)
  });

  return (
    <button onClick={() => agent.setState({ count: state.count + 1 })}>
      Count: {state.count}
    </button>
  );
}
```

## References

- **[references/workflows.md](references/workflows.md)** - Durable Workflows integration
- **[references/callable.md](references/callable.md)** - RPC methods, streaming, timeouts
- **[references/state-scheduling.md](references/state-scheduling.md)** - State persistence, scheduling
- **[references/streaming-chat.md](references/streaming-chat.md)** - AIChatAgent, resumable streams
- **[references/mcp.md](references/mcp.md)** - MCP server integration
- **[references/email.md](references/email.md)** - Email routing and handling
- **[references/codemode.md](references/codemode.md)** - Code Mode (experimental)

---

## Reference: Callable

# Callable Methods

Fetch `docs/callable-methods.md` from `https://github.com/cloudflare/agents/tree/main/docs` for complete documentation.

## Overview

`@callable()` exposes agent methods to clients via WebSocket RPC.

```typescript
import { Agent, callable } from "agents";

export class MyAgent extends Agent<Env, State> {
  @callable()
  async greet(name: string): Promise<string> {
    return `Hello, ${name}!`;
  }

  @callable()
  async processData(data: unknown): Promise<Result> {
    // Long-running work
    return result;
  }
}
```

## Client Usage

```typescript
// Basic call
const greeting = await agent.call("greet", ["World"]);

// With timeout
const result = await agent.call("processData", [data], {
  timeout: 5000  // 5 second timeout
});
```

## Streaming Responses

```typescript
import { Agent, callable, StreamingResponse } from "agents";

export class MyAgent extends Agent<Env, State> {
  @callable({ streaming: true })
  async streamResults(stream: StreamingResponse, query: string) {
    for await (const item of fetchResults(query)) {
      stream.send(JSON.stringify(item));
    }
    stream.close();
  }

  @callable({ streaming: true })
  async streamWithError(stream: StreamingResponse) {
    try {
      // ... work
    } catch (error) {
      stream.error(error.message);  // Signal error to client
      return;
    }
    stream.close();
  }
}
```

Client with streaming:

```typescript
await agent.call("streamResults", ["search term"], {
  stream: {
    onChunk: (data) => console.log("Chunk:", data),
    onDone: () => console.log("Complete"),
    onError: (error) => console.error("Error:", error)
  }
});
```

## Introspection

```typescript
// Get list of callable methods on an agent
const methods = await agent.call("getCallableMethods", []);
// Returns: ["greet", "processData", "streamResults", ...]
```

## When to Use

| Scenario | Use |
|----------|-----|
| Browser/mobile calling agent | `@callable()` |
| External service calling agent | `@callable()` |
| Worker calling agent (same codebase) | DO RPC directly |
| Agent calling another agent | `getAgentByName()` + DO RPC |

---

## Reference: Codemode

# Code Mode (Experimental)

Code Mode generates executable JavaScript instead of making individual tool calls. This significantly reduces token usage and enables complex multi-tool workflows.

## Why Code Mode?

Traditional tool calling:
- One tool call per LLM request
- Multiple round-trips for chained operations
- High token usage for complex workflows

Code Mode:
- LLM generates code that orchestrates multiple tools
- Single execution for complex workflows
- Self-debugging and error recovery
- Ideal for MCP server orchestration

## Setup

### 1. Wrangler Config

```jsonc
{
  "name": "my-agent-worker",
  "compatibility_flags": ["experimental", "enable_ctx_exports"],
  "durable_objects": {
    // "class_name" must match your Agent class name exactly
    "bindings": [{ "name": "MyAgent", "class_name": "MyAgent" }]
  },
  "migrations": [
    // Required: list all Agent classes for SQLite storage
    { "tag": "v1", "new_sqlite_classes": ["MyAgent"] }
  ],
  "services": [
    {
      "binding": "globalOutbound",
      // "service" must match "name" above
      "service": "my-agent-worker",
      "entrypoint": "globalOutbound"
    },
    {
      "binding": "CodeModeProxy",
      "service": "my-agent-worker",
      "entrypoint": "CodeModeProxy"
    }
  ],
  "worker_loaders": [{ "binding": "LOADER" }]
}
```

### 2. Export Required Classes

```typescript
// Export the proxy for tool execution (required for codemode)
export { CodeModeProxy } from "@cloudflare/codemode/ai";

// Define outbound fetch handler for security filtering
export const globalOutbound = {
  fetch: async (input: string | URL | RequestInfo, init?: RequestInit) => {
    const url = new URL(
      typeof input === "string"
        ? input
        : typeof input === "object" && "url" in input
          ? input.url
          : input.toString()
    );
    // Block certain domains if needed
    if (url.hostname === "blocked.example.com") {
      return new Response("Not allowed", { status: 403 });
    }
    return fetch(input, init);
  }
};
```

### 3. Install Dependencies

```bash
npm install @cloudflare/codemode ai @ai-sdk/openai zod
```

### 4. Use Code Mode in Agent

```typescript
import { Agent } from "agents";
import { experimental_codemode as codemode } from "@cloudflare/codemode/ai";
import { streamText, tool, convertToModelMessages } from "ai";
import { openai } from "@ai-sdk/openai";
import { env } from "cloudflare:workers";
import { z } from "zod";

const tools = {
  getWeather: tool({
    description: "Get weather for a location",
    parameters: z.object({ location: z.string() }),
    execute: async ({ location }) => `Weather: ${location} 72°F`
  }),
  sendEmail: tool({
    description: "Send an email",
    parameters: z.object({ to: z.string(), subject: z.string(), body: z.string() }),
    execute: async ({ to, subject, body }) => `Email sent to ${to}`
  })
};

export class MyAgent extends Agent<Env, State> {
  tools = {};

  // Method called by codemode proxy
  callTool(functionName: string, args: unknown[]) {
    return this.tools[functionName]?.execute?.(args, {
      abortSignal: new AbortController().signal,
      toolCallId: "codemode",
      messages: []
    });
  }

  async onChatMessage() {
    this.tools = { ...tools, ...this.mcp.getAITools() };

    const { prompt, tools: wrappedTools } = await codemode({
      prompt: "You are a helpful assistant...",
      tools: this.tools,
      globalOutbound: env.globalOutbound,
      loader: env.LOADER,
      proxy: this.ctx.exports.CodeModeProxy({
        props: {
          binding: "MyAgent",  // Class name
          name: this.name,     // Instance name
          callback: "callTool" // Method to call
        }
      })
    });

    const result = streamText({
      system: prompt,
      model: openai("gpt-4o"),
      messages: await convertToModelMessages(this.state.messages),
      tools: wrappedTools  // Use wrapped tools, not original
    });

    // ... handle stream
  }
}
```

## Generated Code Example

When user asks "Check the weather in NYC and email me the forecast", codemode generates:

```javascript
async function executeTask() {
  const weather = await codemode.getWeather({ location: "NYC" });
  
  await codemode.sendEmail({
    to: "user@example.com",
    subject: "NYC Weather Forecast",
    body: `Current weather: ${weather}`
  });
  
  return { success: true, weather };
}
```

## MCP Server Orchestration

Code Mode excels at orchestrating multiple MCP servers:

```javascript
async function executeTask() {
  // Query file system MCP
  const files = await codemode.listFiles({ path: "/projects" });
  
  // Query database MCP
  const status = await codemode.queryDatabase({
    query: "SELECT * FROM projects WHERE name = ?",
    params: [files[0].name]
  });
  
  // Conditional logic based on results
  if (status.length === 0) {
    await codemode.createTask({
      title: `Review: ${files[0].name}`,
      priority: "high"
    });
  }
  
  return { files, status };
}
```

## When to Use

| Scenario | Use Code Mode? |
|----------|---------------|
| Single tool call | No |
| Chained tool calls | Yes |
| Conditional logic across tools | Yes |
| MCP multi-server workflows | Yes |
| Token budget constrained | Yes |
| Simple Q&A chat | No |

## Limitations

- Experimental - API may change
- Requires Cloudflare Workers
- JavaScript execution only (Python planned)
- Requires additional wrangler config

---

## Reference: Email

# Email Handling

Fetch `docs/email.md` from `https://github.com/cloudflare/agents/tree/main/docs` for complete documentation.

## Overview

Agents receive and reply to emails via Cloudflare Email Routing.

## Wrangler Configuration

```jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "EmailAgent", "class_name": "EmailAgent" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["EmailAgent"] }],
  "send_email": [
    { "name": "SEB", "destination_address": "reply@yourdomain.com" }
  ]
}
```

## Basic Email Handler

```typescript
import { Agent } from "agents";
import { type AgentEmail } from "agents/email";
import PostalMime from "postal-mime";

export class EmailAgent extends Agent<Env, State> {
  async onEmail(email: AgentEmail) {
    const raw = await email.getRaw();
    const parsed = await PostalMime.parse(raw);

    console.log("From:", email.from);
    console.log("Subject:", parsed.subject);

    await this.replyToEmail(email, {
      fromName: "My Agent",
      subject: `Re: ${parsed.subject}`,
      body: "Thanks for your email!"
    });
  }
}
```

## Routing Emails

```typescript
import { routeAgentRequest, routeAgentEmail } from "agents";
import { createAddressBasedEmailResolver } from "agents/email";

export default {
  async email(message, env) {
    await routeAgentEmail(message, env, {
      resolver: createAddressBasedEmailResolver("EmailAgent")
    });
  },

  async fetch(request, env) {
    return routeAgentRequest(request, env) ?? new Response("Not found", { status: 404 });
  }
};
```

## Resolvers

### Address-Based (Inbound Mail)

Routes based on recipient address:

```typescript
import { createAddressBasedEmailResolver } from "agents/email";

const resolver = createAddressBasedEmailResolver("EmailAgent");
// support@example.com → EmailAgent, instance "support"
// NotificationAgent+user123@example.com → NotificationAgent, instance "user123"
```

### Secure Reply (Reply Flows)

Verifies replies are authentic using HMAC-SHA256 signatures:

```typescript
import { createSecureReplyEmailResolver } from "agents/email";

const resolver = createSecureReplyEmailResolver(env.EMAIL_SECRET, {
  maxAge: 7 * 24 * 60 * 60, // 7 days (default: 30 days)
  onInvalidSignature: (email, reason) => {
    console.warn(`Invalid signature from ${email.from}: ${reason}`);
  }
});
```

Sign outbound emails to enable secure reply routing:

```typescript
await this.replyToEmail(email, {
  fromName: "My Agent",
  body: "Thanks!",
  secret: this.env.EMAIL_SECRET  // Signs headers for secure reply routing
});
```

### Catch-All (Single Instance)

Routes all emails to one agent instance:

```typescript
import { createCatchAllEmailResolver } from "agents/email";

const resolver = createCatchAllEmailResolver("EmailAgent", "default");
```

### Combining Resolvers

```typescript
async email(message, env) {
  const secureReply = createSecureReplyEmailResolver(env.EMAIL_SECRET);
  const addressBased = createAddressBasedEmailResolver("EmailAgent");

  await routeAgentEmail(message, env, {
    resolver: async (email, env) => {
      // Try secure reply first
      const result = await secureReply(email, env);
      if (result) return result;
      // Fall back to address-based
      return addressBased(email, env);
    }
  });
}
```

## Utilities

```typescript
import { isAutoReplyEmail } from "agents/email";

async onEmail(email: AgentEmail) {
  if (isAutoReplyEmail(email.headers)) {
    // Skip auto-replies (vacation, out-of-office, etc.)
    return;
  }
  // Process email...
}
```

---

## Reference: Mcp

# MCP Server Integration

Fetch `docs/mcp-client.md` and `docs/mcp-servers.md` from `https://github.com/cloudflare/agents/tree/main/docs` for complete documentation.

Agents include a multi-server MCP client for connecting to external MCP servers.

## Add an MCP Server

```typescript
import { Agent, callable } from "agents";

export class MyAgent extends Agent<Env, State> {
  @callable()
  async addServer(name: string, url: string) {
    // Options-based API (recommended)
    const result = await this.addMcpServer(name, url, {
      callbackHost: "https://my-worker.workers.dev",
      transport: { headers: { Authorization: "Bearer ..." } }
    });

    if (result.state === "authenticating") {
      // OAuth required - redirect user to result.authUrl
      return { needsAuth: true, authUrl: result.authUrl };
    }

    return { ready: true, id: result.id };
  }
}
```

## Use MCP Tools

```typescript
async onChatMessage() {
  // Get AI-compatible tools from all connected MCP servers
  const mcpTools = this.mcp.getAITools();
  
  const allTools = {
    ...localTools,
    ...mcpTools
  };

  const result = streamText({
    model: openai("gpt-4o"),
    messages: await convertToModelMessages(this.messages),
    tools: allTools
  });
  
  return result.toUIMessageStreamResponse();
}
```

## List MCP Resources

```typescript
// List all registered servers
const servers = this.mcp.listServers();

// List tools from all servers
const tools = this.mcp.listTools();

// List resources
const resources = this.mcp.listResources();

// List prompts
const prompts = this.mcp.listPrompts();
```

## Remove Server

```typescript
await this.removeMcpServer(serverId);
```

## Building an MCP Server

Use `McpAgent` from the SDK to create an MCP server.

**Install dependencies:**
```bash
npm install @modelcontextprotocol/sdk zod
```

**Wrangler config:**
```jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "MyMCP", "class_name": "MyMCP" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyMCP"] }]
}
```

**Server implementation:**
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { McpAgent } from "agents/mcp";
import { z } from "zod";

type State = { counter: number };

export class MyMCP extends McpAgent<Env, State, {}> {
  server = new McpServer({
    name: "MyMCPServer",
    version: "1.0.0"
  });

  initialState = { counter: 0 };

  async init() {
    // Register a resource
    this.server.resource("counter", "mcp://resource/counter", (uri) => ({
      contents: [{ text: String(this.state.counter), uri: uri.href }]
    }));

    // Register a tool
    this.server.registerTool(
      "increment",
      {
        description: "Increment the counter",
        inputSchema: { amount: z.number().default(1) }
      },
      async ({ amount }) => {
        this.setState({ counter: this.state.counter + amount });
        return {
          content: [{ text: `Counter: ${this.state.counter}`, type: "text" }]
        };
      }
    );
  }
}
```

## Serve MCP Server

```typescript
export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const url = new URL(request.url);

    // SSE transport (legacy)
    if (url.pathname.startsWith("/sse")) {
      return MyMCP.serveSSE("/sse", { binding: "MyMCP" }).fetch(request, env, ctx);
    }

    // Streamable HTTP transport (recommended)
    if (url.pathname.startsWith("/mcp")) {
      return MyMCP.serve("/mcp", { binding: "MyMCP" }).fetch(request, env, ctx);
    }

    return new Response("Not found", { status: 404 });
  }
};
```

---

## Reference: State Scheduling

# State & Scheduling

Fetch `docs/state.md` and `docs/scheduling.md` from `https://github.com/cloudflare/agents/tree/main/docs` for complete documentation.

## State Management

State persists to SQLite and broadcasts to connected clients automatically.

### Define Typed State

```typescript
type State = { 
  count: number;
  items: string[];
};

export class MyAgent extends Agent<Env, State> {
  initialState: State = { count: 0, items: [] };
}
```

### Read and Update

```typescript
// Read (lazy-loaded from SQLite)
const count = this.state.count;

// Write (sync, persists, broadcasts)
this.setState({ count: this.state.count + 1 });
```

### Validation Hook

`validateStateChange()` runs synchronously before state persists. Throw to reject the update.

```typescript
validateStateChange(nextState: State, source: Connection | "server") {
  if (nextState.count < 0) {
    throw new Error("Count cannot be negative");
  }
}
```

### Execution Order

1. `validateStateChange(nextState, source)` - sync, gating
2. State persisted to SQLite
3. State broadcast to connected clients
4. `onStateUpdate(nextState, source)` - async via `ctx.waitUntil`, non-gating

### Client-Side Sync (React)

```tsx
import { useAgent } from "agents/react";

function App() {
  const [state, setLocalState] = useState<State>({ count: 0 });
  
  const agent = useAgent<State>({
    agent: "MyAgent",
    name: "instance-1",
    onStateUpdate: (newState) => setLocalState(newState)
  });

  return <button onClick={() => agent.setState({ count: state.count + 1 })}>
    Count: {state.count}
  </button>;
}
```

## SQL API

Direct SQLite access for custom queries:

```typescript
// Create table
this.sql`
  CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    name TEXT,
    created_at INTEGER DEFAULT (unixepoch())
  )
`;

// Insert
this.sql`INSERT INTO items (id, name) VALUES (${id}, ${name})`;

// Query with types
const items = this.sql<{ id: string; name: string }>`
  SELECT * FROM items WHERE name LIKE ${`%${search}%`}
`;
```

## Scheduling

### Schedule Types

| Mode | Syntax | Use Case |
|------|--------|----------|
| Delay | `this.schedule(60, ...)` | Run in 60 seconds |
| Date | `this.schedule(new Date(...), ...)` | Run at specific time |
| Cron | `this.schedule("0 8 * * *", ...)` | Recurring schedule |
| Interval | `this.scheduleEvery(30, ...)` | Fixed interval (every 30s) |

### Examples

```typescript
// Delay (seconds)
await this.schedule(60, "checkStatus", { id: "abc123" });

// Specific date
await this.schedule(new Date("2025-12-25T00:00:00Z"), "sendGreeting", { to: "user" });

// Cron (recurring)
await this.schedule("0 9 * * 1-5", "weekdayReport", {});

// Fixed interval (every 30 seconds, overlap prevention built-in)
await this.scheduleEvery(30, "pollUpdates");
await this.scheduleEvery(300, "syncData", { source: "api" });
```

### Handler

```typescript
async sendGreeting(payload: { to: string }, schedule: Schedule) {
  console.log(`Sending greeting to ${payload.to}`);
  // Cron schedules auto-reschedule; one-time schedules are deleted
}
```

### Manage Schedules

```typescript
const schedules = this.getSchedules();
const crons = this.getSchedules({ type: "cron" });
await this.cancelSchedule(schedule.id);
```

## Lifecycle Callbacks

```typescript
export class MyAgent extends Agent<Env, State> {
  async onStart() {
    // Agent started or woke from hibernation
  }

  onConnect(conn: Connection, ctx: ConnectionContext) {
    // WebSocket connected
  }

  onMessage(conn: Connection, message: WSMessage) {
    // WebSocket message (non-RPC)
  }

  onStateUpdate(state: State, source: Connection | "server") {
    // State changed (async, non-blocking)
  }

  onError(error: unknown) {
    // Error handler
    throw error; // Re-throw to propagate
  }
}
```

---

## Reference: Streaming Chat

# Streaming Chat with AIChatAgent

Fetch `docs/resumable-streaming.md` and `docs/client-sdk.md` from `https://github.com/cloudflare/agents/tree/main/docs` for complete documentation.

`AIChatAgent` provides streaming chat with automatic message persistence and resumable streams.

## Basic Chat Agent

```typescript
import { AIChatAgent } from "@cloudflare/ai-chat";
import { streamText, convertToModelMessages } from "ai";
import { openai } from "@ai-sdk/openai";

export class Chat extends AIChatAgent<Env> {
  async onChatMessage(onFinish) {
    const result = streamText({
      model: openai("gpt-4o"),
      messages: await convertToModelMessages(this.messages),
      onFinish
    });
    return result.toUIMessageStreamResponse();
  }
}
```

## With Custom System Prompt

```typescript
export class Chat extends AIChatAgent<Env> {
  async onChatMessage(onFinish) {
    const result = streamText({
      model: openai("gpt-4o"),
      system: "You are a helpful assistant specializing in...",
      messages: await convertToModelMessages(this.messages),
      onFinish
    });
    return result.toUIMessageStreamResponse();
  }
}
```

## With Tools

```typescript
import { tool } from "ai";
import { z } from "zod";

const tools = {
  getWeather: tool({
    description: "Get weather for a location",
    parameters: z.object({ location: z.string() }),
    execute: async ({ location }) => `Weather in ${location}: 72°F, sunny`
  })
};

export class Chat extends AIChatAgent<Env> {
  async onChatMessage(onFinish) {
    const result = streamText({
      model: openai("gpt-4o"),
      messages: await convertToModelMessages(this.messages),
      tools,
      onFinish
    });
    return result.toUIMessageStreamResponse();
  }
}
```

## Custom UI Message Stream

For more control, use `createUIMessageStream`:

```typescript
import { createUIMessageStream, createUIMessageStreamResponse } from "ai";

export class Chat extends AIChatAgent<Env> {
  async onChatMessage(onFinish) {
    const stream = createUIMessageStream({
      execute: async ({ writer }) => {
        const result = streamText({
          model: openai("gpt-4o"),
          messages: await convertToModelMessages(this.messages),
          onFinish
        });
        writer.merge(result.toUIMessageStream());
      }
    });
    return createUIMessageStreamResponse({ stream });
  }
}
```

## Resumable Streaming

Streams automatically resume if client disconnects and reconnects:

1. Chunks buffered to SQLite during streaming
2. On reconnect, buffered chunks sent immediately
3. Live streaming continues from where it left off

**Enabled by default.** To disable:

```tsx
const { messages } = useAgentChat({ agent, resume: false });
```

## React Client

```tsx
import { useAgent } from "agents/react";
import { useAgentChat } from "@cloudflare/ai-chat/react";

function ChatUI() {
  const agent = useAgent({
    agent: "Chat",
    name: "my-chat-session"
  });

  const { 
    messages, 
    input, 
    handleInputChange, 
    handleSubmit, 
    status 
  } = useAgentChat({ agent });

  return (
    <div>
      {messages.map((m) => (
        <div key={m.id}>
          <strong>{m.role}:</strong> {m.content}
        </div>
      ))}
      
      <form onSubmit={handleSubmit}>
        <input 
          value={input} 
          onChange={handleInputChange}
          disabled={status === "streaming"}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

## Streaming RPC Methods

For non-chat streaming, use `@callable({ streaming: true })`:

```typescript
import { Agent, callable, StreamingResponse } from "agents";

export class MyAgent extends Agent<Env> {
  @callable({ streaming: true })
  async streamData(stream: StreamingResponse, query: string) {
    for (let i = 0; i < 10; i++) {
      stream.send(`Result ${i}: ${query}`);
      await sleep(100);
    }
    stream.close();
  }
}
```

Client receives streamed messages via WebSocket RPC.

## Status Values

`useAgentChat` status:

| Status | Meaning |
|--------|---------|
| `ready` | Idle, ready for input |
| `streaming` | Response streaming |
| `submitted` | Request sent, waiting |
| `error` | Error occurred |

---

## Reference: Workflows

# Workflows Integration

Fetch `docs/workflows.md` from `https://github.com/cloudflare/agents/tree/main/docs` for complete documentation.

## Overview

Agents handle real-time communication; Workflows handle durable execution. Together they enable:

- Long-running background tasks with automatic retries
- Human-in-the-loop approval flows
- Multi-step pipelines that survive failures

| Use Case | Recommendation |
|----------|----------------|
| Chat/messaging | Agent only |
| Quick API calls (<30s) | Agent only |
| Background processing (<30s) | Agent `queue()` |
| Long-running tasks (>30s) | Agent + Workflow |
| Human approval flows | Agent + Workflow |

## AgentWorkflow Base Class

```typescript
import { AgentWorkflow } from "agents/workflows";
import type { AgentWorkflowEvent, AgentWorkflowStep } from "agents/workflows";

type TaskParams = { taskId: string; data: string };

export class ProcessingWorkflow extends AgentWorkflow<MyAgent, TaskParams> {
  async run(event: AgentWorkflowEvent<TaskParams>, step: AgentWorkflowStep) {
    const params = event.payload;

    // Durable step - retries on failure
    const result = await step.do("process", async () => {
      return processData(params.data);
    });

    // Non-durable: progress reporting
    await this.reportProgress({ step: "process", percent: 0.5 });

    // Non-durable: broadcast to connected clients
    this.broadcastToClients({ type: "update", taskId: params.taskId });

    // Durable: merge state via step
    await step.mergeAgentState({ lastProcessed: params.taskId });

    // Durable: report completion
    await step.reportComplete(result);

    return result;
  }
}
```

## Wrangler Configuration

```jsonc
{
  "workflows": [
    { "name": "processing-workflow", "binding": "PROCESSING_WORKFLOW", "class_name": "ProcessingWorkflow" }
  ],
  "durable_objects": {
    "bindings": [{ "name": "MyAgent", "class_name": "MyAgent" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyAgent"] }]
}
```

## Agent Methods for Workflows

```typescript
// Start a workflow
const instance = await this.runWorkflow("ProcessingWorkflow", { taskId: "123", data: "..." });

// Send event to waiting workflow
await this.sendWorkflowEvent("ProcessingWorkflow", workflowId, { type: "approve" });

// Query workflows
const workflow = await this.getWorkflow(workflowId);
const workflows = await this.getWorkflows({ status: "running" });

// Control workflows
await this.approveWorkflow(workflowId);
await this.rejectWorkflow(workflowId);
await this.terminateWorkflow(workflowId);
await this.pauseWorkflow(workflowId);
await this.resumeWorkflow(workflowId);

// Delete workflows
await this.deleteWorkflow(workflowId);
await this.deleteWorkflows({ status: "complete", before: new Date(...) });
```

## Lifecycle Callbacks

```typescript
export class MyAgent extends Agent<Env, State> {
  async onWorkflowProgress(workflowName: string, workflowId: string, progress: unknown) {
    // Workflow reported progress via this.reportProgress()
    this.broadcast({ type: "progress", workflowId, progress });
  }

  async onWorkflowComplete(workflowName: string, workflowId: string, result?: unknown) {
    // Workflow finished successfully
  }

  async onWorkflowError(workflowName: string, workflowId: string, error: Error) {
    // Workflow failed
  }

  async onWorkflowEvent(workflowName: string, workflowId: string, event: unknown) {
    // Workflow received an event via sendWorkflowEvent()
  }
}
```

## Human-in-the-Loop

```typescript
// In workflow: wait for approval
const approved = await step.waitForEvent<{ approved: boolean }>("approval", {
  timeout: "7d"
});

if (!approved.approved) {
  throw new Error("Rejected");
}

// From agent: approve or reject
await this.approveWorkflow(workflowId);  // Sends { approved: true }
await this.rejectWorkflow(workflowId);   // Sends { approved: false }
```
