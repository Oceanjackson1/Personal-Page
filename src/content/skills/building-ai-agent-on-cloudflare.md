---
title: "Building AI Agent On Cloudflare"
description: "Builds AI agents on Cloudflare using the Agents SDK with state management, real-time WebSockets, scheduled tasks, tool integration, and chat capabilities. Generates production-ready agent code deployed to Workers.  Use when: user wants to 'build a..."
category: "devops"
source: "community"
author: "Community"
tags: ["building", "ai", "agent", "cloudflare"]
date: 2026-03-20
---

# Building Cloudflare Agents

Your knowledge of the Agents SDK may be outdated. **Prefer retrieval over pre-training** for any agent-building task.

## Retrieval Sources

| Source | How to retrieve | Use for |
|--------|----------------|---------|
| Agents SDK docs | `https://github.com/cloudflare/agents/tree/main/docs` | SDK API, state, routing, scheduling |
| Cloudflare Agents docs | `https://developers.cloudflare.com/agents/` | Platform integration, deployment |
| Workers docs | Search tool or `https://developers.cloudflare.com/workers/` | Runtime APIs, bindings, config |

## When to Use

- User wants to build an AI agent or chatbot
- User needs stateful, real-time AI interactions
- User asks about the Cloudflare Agents SDK
- User wants scheduled tasks or background AI work
- User needs WebSocket-based AI communication

## Prerequisites

- Cloudflare account with Workers enabled
- Node.js 18+ and npm/pnpm/yarn
- Wrangler CLI (`npm install -g wrangler`)

## Quick Start

```bash
npm create cloudflare@latest -- my-agent --template=cloudflare/agents-starter
cd my-agent
npm start
```

Agent runs at `http://localhost:8787`

## Core Concepts

### What is an Agent?

An Agent is a stateful, persistent AI service that:
- Maintains state across requests and reconnections
- Communicates via WebSockets or HTTP
- Runs on Cloudflare's edge via Durable Objects
- Can schedule tasks and call tools
- Scales horizontally (each user/session gets own instance)

### Agent Lifecycle

```
Client connects → Agent.onConnect() → Agent processes messages
                                    → Agent.onMessage()
                                    → Agent.setState() (persists + syncs)
Client disconnects → State persists → Client reconnects → State restored
```

## Basic Agent Structure

```typescript
import { Agent, Connection } from "agents";

interface Env {
  AI: Ai;  // Workers AI binding
}

interface State {
  messages: Array<{ role: string; content: string }>;
  preferences: Record<string, string>;
}

export class MyAgent extends Agent<Env, State> {
  // Initial state for new instances
  initialState: State = {
    messages: [],
    preferences: {},
  };

  // Called when agent starts or resumes
  async onStart() {
    console.log("Agent started with state:", this.state);
  }

  // Handle WebSocket connections
  async onConnect(connection: Connection) {
    connection.send(JSON.stringify({
      type: "welcome",
      history: this.state.messages,
    }));
  }

  // Handle incoming messages
  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);

    if (data.type === "chat") {
      await this.handleChat(connection, data.content);
    }
  }

  // Handle disconnections
  async onClose(connection: Connection) {
    console.log("Client disconnected");
  }

  // React to state changes
  onStateUpdate(state: State, source: string) {
    console.log("State updated by:", source);
  }

  private async handleChat(connection: Connection, userMessage: string) {
    // Add user message to history
    const messages = [
      ...this.state.messages,
      { role: "user", content: userMessage },
    ];

    // Call AI
    const response = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
      messages,
    });

    // Update state (persists and syncs to all clients)
    this.setState({
      ...this.state,
      messages: [
        ...messages,
        { role: "assistant", content: response.response },
      ],
    });

    // Send response
    connection.send(JSON.stringify({
      type: "response",
      content: response.response,
    }));
  }
}
```

## Entry Point Configuration

```typescript
// src/index.ts
import { routeAgentRequest } from "agents";
import { MyAgent } from "./agent";

export default {
  async fetch(request: Request, env: Env) {
    // routeAgentRequest handles routing to /agents/:class/:name
    return (
      (await routeAgentRequest(request, env)) ||
      new Response("Not found", { status: 404 })
    );
  },
};

export { MyAgent };
```

Clients connect via: `wss://my-agent.workers.dev/agents/MyAgent/session-id`

## Wrangler Configuration

```toml
name = "my-agent"
main = "src/index.ts"
compatibility_date = "2024-12-01"

[ai]
binding = "AI"

[durable_objects]
bindings = [{ name = "AGENT", class_name = "MyAgent" }]

[[migrations]]
tag = "v1"
new_classes = ["MyAgent"]
```

## State Management

### Reading State

```typescript
// Current state is always available
const currentMessages = this.state.messages;
const userPrefs = this.state.preferences;
```

### Updating State

```typescript
// setState persists AND syncs to all connected clients
this.setState({
  ...this.state,
  messages: [...this.state.messages, newMessage],
});

// Partial updates work too
this.setState({
  preferences: { ...this.state.preferences, theme: "dark" },
});
```

### SQL Storage

For complex queries, use the embedded SQLite database:

```typescript
// Create tables
await this.sql`
  CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )
`;

// Insert
await this.sql`
  INSERT INTO documents (title, content)
  VALUES (${title}, ${content})
`;

// Query
const docs = await this.sql`
  SELECT * FROM documents WHERE title LIKE ${`%${search}%`}
`;
```

## Scheduled Tasks

Agents can schedule future work:

```typescript
async onMessage(connection: Connection, message: string) {
  const data = JSON.parse(message);

  if (data.type === "schedule_reminder") {
    // Schedule task for 1 hour from now
    const { id } = await this.schedule(3600, "sendReminder", {
      message: data.reminderText,
      userId: data.userId,
    });

    connection.send(JSON.stringify({ type: "scheduled", taskId: id }));
  }
}

// Called when scheduled task fires
async sendReminder(data: { message: string; userId: string }) {
  // Send notification, email, etc.
  console.log(`Reminder for ${data.userId}: ${data.message}`);

  // Can also update state
  this.setState({
    ...this.state,
    lastReminder: new Date().toISOString(),
  });
}
```

### Schedule Options

```typescript
// Delay in seconds
await this.schedule(60, "taskMethod", { data });

// Specific date
await this.schedule(new Date("2025-01-01T00:00:00Z"), "taskMethod", { data });

// Cron expression (recurring)
await this.schedule("0 9 * * *", "dailyTask", {});  // 9 AM daily
await this.schedule("*/5 * * * *", "everyFiveMinutes", {});  // Every 5 min

// Manage schedules
const schedules = await this.getSchedules();
await this.cancelSchedule(taskId);
```

## Chat Agent (AI-Powered)

For chat-focused agents, extend `AIChatAgent`:

```typescript
import { AIChatAgent } from "agents/ai-chat-agent";

export class ChatBot extends AIChatAgent<Env> {
  // Called for each user message
  async onChatMessage(message: string) {
    const response = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        ...this.messages,  // Automatic history management
        { role: "user", content: message },
      ],
      stream: true,
    });

    // Stream response back to client
    return response;
  }
}
```

Features included:
- Automatic message history
- Resumable streaming (survives disconnects)
- Built-in `saveMessages()` for persistence

## Client Integration

### React Hook

```tsx
import { useAgent } from "agents/react";

function Chat() {
  const { state, send, connected } = useAgent({
    agent: "my-agent",
    name: userId,  // Agent instance ID
  });

  const sendMessage = (text: string) => {
    send(JSON.stringify({ type: "chat", content: text }));
  };

  return (
    <div>
      {state.messages.map((msg, i) => (
        <div key={i}>{msg.role}: {msg.content}</div>
      ))}
      <input onKeyDown={(e) => e.key === "Enter" && sendMessage(e.target.value)} />
    </div>
  );
}
```

### Vanilla JavaScript

```javascript
const ws = new WebSocket("wss://my-agent.workers.dev/agents/MyAgent/user123");

ws.onopen = () => {
  console.log("Connected to agent");
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Received:", data);
};

ws.send(JSON.stringify({ type: "chat", content: "Hello!" }));
```

## Common Patterns

See [references/agent-patterns.md](references/agent-patterns.md) for:
- Tool calling and function execution
- Multi-agent orchestration
- RAG (Retrieval Augmented Generation)
- Human-in-the-loop workflows

## Deployment

```bash
# Deploy
npx wrangler deploy

# View logs
wrangler tail

# Test endpoint
curl https://my-agent.workers.dev/agents/MyAgent/test-user
```

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for common issues.

## References

- [references/examples.md](references/examples.md) — Official templates and production examples
- [references/agent-patterns.md](references/agent-patterns.md) — Advanced patterns
- [references/state-patterns.md](references/state-patterns.md) — State management strategies
- [references/troubleshooting.md](references/troubleshooting.md) — Error solutions

---

## Reference: Agent Patterns

# Agent Patterns

Advanced patterns for building sophisticated agents.

## Tool Calling

Agents can expose tools that AI models can call:

```typescript
import { Agent, Connection } from "agents";
import { z } from "zod";

interface Tool {
  name: string;
  description: string;
  parameters: z.ZodSchema;
  handler: (params: any) => Promise<string>;
}

export class ToolAgent extends Agent<Env, State> {
  private tools: Map<string, Tool> = new Map();

  async onStart() {
    // Register tools
    this.registerTool({
      name: "get_weather",
      description: "Get current weather for a city",
      parameters: z.object({ city: z.string() }),
      handler: async ({ city }) => {
        const res = await fetch(`https://api.weather.com/${city}`);
        return JSON.stringify(await res.json());
      },
    });

    this.registerTool({
      name: "search_database",
      description: "Search the document database",
      parameters: z.object({ query: z.string(), limit: z.number().default(10) }),
      handler: async ({ query, limit }) => {
        const results = await this.sql`
          SELECT * FROM documents
          WHERE content LIKE ${`%${query}%`}
          LIMIT ${limit}
        `;
        return JSON.stringify(results);
      },
    });
  }

  private registerTool(tool: Tool) {
    this.tools.set(tool.name, tool);
  }

  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);

    if (data.type === "chat") {
      await this.handleChatWithTools(connection, data.content);
    }
  }

  private async handleChatWithTools(connection: Connection, userMessage: string) {
    // Build tool descriptions for the AI
    const toolDescriptions = Array.from(this.tools.values()).map((t) => ({
      type: "function",
      function: {
        name: t.name,
        description: t.description,
        parameters: JSON.parse(JSON.stringify(t.parameters)),
      },
    }));

    // First AI call - may request tool use
    const response = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
      messages: [
        { role: "system", content: "You are a helpful assistant with access to tools." },
        ...this.state.messages,
        { role: "user", content: userMessage },
      ],
      tools: toolDescriptions,
    });

    // Check if AI wants to use a tool
    if (response.tool_calls) {
      for (const toolCall of response.tool_calls) {
        const tool = this.tools.get(toolCall.function.name);
        if (tool) {
          const params = JSON.parse(toolCall.function.arguments);
          const result = await tool.handler(params);

          // Send tool result back to AI
          const finalResponse = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
            messages: [
              ...this.state.messages,
              { role: "user", content: userMessage },
              { role: "assistant", tool_calls: response.tool_calls },
              { role: "tool", tool_call_id: toolCall.id, content: result },
            ],
          });

          connection.send(JSON.stringify({
            type: "response",
            content: finalResponse.response,
            toolUsed: toolCall.function.name,
          }));
        }
      }
    } else {
      connection.send(JSON.stringify({
        type: "response",
        content: response.response,
      }));
    }
  }
}
```

## RAG (Retrieval Augmented Generation)

Combine Vectorize with Agents for knowledge-grounded responses:

```typescript
interface Env {
  AI: Ai;
  VECTORIZE: VectorizeIndex;
}

export class RAGAgent extends Agent<Env, State> {
  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);

    if (data.type === "chat") {
      // 1. Generate embedding for query
      const embedding = await this.env.AI.run("@cf/baai/bge-base-en-v1.5", {
        text: data.content,
      });

      // 2. Search vector database
      const results = await this.env.VECTORIZE.query(embedding.data[0], {
        topK: 5,
        returnMetadata: true,
      });

      // 3. Build context from results
      const context = results.matches
        .map((m) => m.metadata?.text || "")
        .join("\n\n");

      // 4. Generate response with context
      const response = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
        messages: [
          {
            role: "system",
            content: `Answer based on this context:\n\n${context}\n\nIf the context doesn't contain relevant information, say so.`,
          },
          { role: "user", content: data.content },
        ],
      });

      // 5. Update state and respond
      this.setState({
        messages: [
          ...this.state.messages,
          { role: "user", content: data.content },
          { role: "assistant", content: response.response },
        ],
      });

      connection.send(JSON.stringify({
        type: "response",
        content: response.response,
        sources: results.matches.map((m) => m.metadata?.source),
      }));
    }
  }

  // Ingest documents into vector store
  async ingestDocument(doc: { id: string; text: string; source: string }) {
    const embedding = await this.env.AI.run("@cf/baai/bge-base-en-v1.5", {
      text: doc.text,
    });

    await this.env.VECTORIZE.upsert([{
      id: doc.id,
      values: embedding.data[0],
      metadata: { text: doc.text, source: doc.source },
    }]);
  }
}
```

## Multi-Agent Orchestration

Coordinate multiple specialized agents:

```typescript
interface Env {
  RESEARCHER: DurableObjectNamespace;
  WRITER: DurableObjectNamespace;
  REVIEWER: DurableObjectNamespace;
}

export class OrchestratorAgent extends Agent<Env, State> {
  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);

    if (data.type === "create_article") {
      connection.send(JSON.stringify({ type: "status", step: "researching" }));

      // Step 1: Research agent gathers information
      const researchResult = await this.callAgent(
        this.env.RESEARCHER,
        data.topic,
        { action: "research", topic: data.topic }
      );

      connection.send(JSON.stringify({ type: "status", step: "writing" }));

      // Step 2: Writer agent creates draft
      const draftResult = await this.callAgent(
        this.env.WRITER,
        data.topic,
        { action: "write", research: researchResult, topic: data.topic }
      );

      connection.send(JSON.stringify({ type: "status", step: "reviewing" }));

      // Step 3: Reviewer agent improves draft
      const finalResult = await this.callAgent(
        this.env.REVIEWER,
        data.topic,
        { action: "review", draft: draftResult }
      );

      connection.send(JSON.stringify({
        type: "complete",
        article: finalResult,
      }));
    }
  }

  private async callAgent(
    namespace: DurableObjectNamespace,
    id: string,
    payload: any
  ): Promise<string> {
    const agentId = namespace.idFromName(id);
    const agent = namespace.get(agentId);

    const response = await agent.fetch("http://agent/task", {
      method: "POST",
      body: JSON.stringify(payload),
    });

    return response.text();
  }
}
```

## Human-in-the-Loop

Pause agent execution for human approval:

```typescript
interface State {
  pendingApprovals: Array<{
    id: string;
    action: string;
    data: any;
    requestedAt: string;
  }>;
}

export class ApprovalAgent extends Agent<Env, State> {
  initialState: State = { pendingApprovals: [] };

  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);

    if (data.type === "request_action") {
      // Action requires approval
      if (this.requiresApproval(data.action)) {
        const approvalId = crypto.randomUUID();

        this.setState({
          pendingApprovals: [
            ...this.state.pendingApprovals,
            {
              id: approvalId,
              action: data.action,
              data: data.payload,
              requestedAt: new Date().toISOString(),
            },
          ],
        });

        connection.send(JSON.stringify({
          type: "approval_required",
          approvalId,
          action: data.action,
          description: this.describeAction(data.action, data.payload),
        }));

        return;
      }

      // Execute immediately if no approval needed
      await this.executeAction(connection, data.action, data.payload);
    }

    if (data.type === "approve") {
      const approval = this.state.pendingApprovals.find(
        (a) => a.id === data.approvalId
      );

      if (approval) {
        // Remove from pending
        this.setState({
          pendingApprovals: this.state.pendingApprovals.filter(
            (a) => a.id !== data.approvalId
          ),
        });

        // Execute the approved action
        await this.executeAction(connection, approval.action, approval.data);
      }
    }

    if (data.type === "reject") {
      this.setState({
        pendingApprovals: this.state.pendingApprovals.filter(
          (a) => a.id !== data.approvalId
        ),
      });

      connection.send(JSON.stringify({
        type: "action_rejected",
        approvalId: data.approvalId,
      }));
    }
  }

  private requiresApproval(action: string): boolean {
    const sensitiveActions = ["delete", "send_email", "make_payment", "publish"];
    return sensitiveActions.includes(action);
  }

  private describeAction(action: string, data: any): string {
    // Generate human-readable description
    return `${action}: ${JSON.stringify(data)}`;
  }

  private async executeAction(connection: Connection, action: string, data: any) {
    // Execute the action
    const result = await this.performAction(action, data);

    connection.send(JSON.stringify({
      type: "action_completed",
      action,
      result,
    }));
  }
}
```

## Streaming Responses

Stream AI responses in real-time:

```typescript
export class StreamingAgent extends Agent<Env, State> {
  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);

    if (data.type === "chat") {
      // Start streaming response
      const stream = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
        messages: [
          { role: "system", content: "You are a helpful assistant." },
          ...this.state.messages,
          { role: "user", content: data.content },
        ],
        stream: true,
      });

      let fullResponse = "";

      // Stream chunks to client
      for await (const chunk of stream) {
        if (chunk.response) {
          fullResponse += chunk.response;
          connection.send(JSON.stringify({
            type: "stream",
            content: chunk.response,
            done: false,
          }));
        }
      }

      // Update state with complete response
      this.setState({
        messages: [
          ...this.state.messages,
          { role: "user", content: data.content },
          { role: "assistant", content: fullResponse },
        ],
      });

      // Signal completion
      connection.send(JSON.stringify({
        type: "stream",
        content: "",
        done: true,
      }));
    }
  }
}
```

## Connecting to MCP Servers

Agents can connect to MCP servers as clients:

```typescript
export class MCPClientAgent extends Agent<Env, State> {
  async onStart() {
    // Connect to external MCP server
    await this.addMcpServer(
      "github",
      "https://github-mcp.example.com/sse",
      { headers: { Authorization: `Bearer ${this.env.GITHUB_TOKEN}` } }
    );

    await this.addMcpServer(
      "database",
      "https://db-mcp.example.com/sse"
    );
  }

  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);

    if (data.type === "use_tool") {
      // Call tool on connected MCP server
      const servers = await this.getMcpServers();
      const server = servers.find((s) => s.name === data.server);

      if (server) {
        const result = await server.callTool(data.tool, data.params);
        connection.send(JSON.stringify({ type: "tool_result", result }));
      }
    }
  }

  async onClose() {
    // Cleanup MCP connections
    await this.removeMcpServer("github");
    await this.removeMcpServer("database");
  }
}
```

---

## Reference: Examples

# Project Bootstrapping

Instructions for creating new agent projects.

---

## Create Command

Execute in terminal to generate a new project:

```bash
npm create cloudflare@latest -- my-agent \
  --template=cloudflare/agents-starter
```

Or use npx directly:

```bash
npx create-cloudflare@latest --template cloudflare/agents-starter
```

Includes:
- Persistent data via `this.setState` and `this.sql`
- WebSocket real-time connections
- Workers AI bindings ready
- React chat interface example

---

## Project Layout

Generated structure:

```
my-agent/
├── src/
│   ├── app.tsx       # React chat interface
│   ├── server.ts     # Agent implementation
│   ├── tools.ts      # Tool definitions
│   └── utils.ts      # Helpers
├── wrangler.toml     # Platform configuration
└── package.json
```

---

## Agent Variations

**Chat-focused:**

Inherit from base `Agent` class, implement `onMessage` handler:
- Manual conversation tracking
- Full control over responses
- Integrates with any AI provider

**Persistent data:**

Use `this.setState()` for automatic persistence:
- JSON-serializable data
- Auto-syncs to connected clients
- Survives instance eviction

**Per-session isolation:**

Route by unique identifier in URL path:
- Each identifier gets dedicated instance
- Isolated data storage
- Horizontal scaling automatic

---

## Platform Documentation

- developers.cloudflare.com/agents/
- developers.cloudflare.com/agents/getting-started/
- developers.cloudflare.com/agents/api-reference/

**Source repositories:**
- `github.com/cloudflare/agents-starter` (starter template)
- `github.com/cloudflare/agents/tree/main/examples` (reference implementations)

**Related services:**

- developers.cloudflare.com/workers-ai/ (AI models)
- developers.cloudflare.com/vectorize/ (vector search)
- developers.cloudflare.com/d1/ (SQL database)

---

## Reference Implementations

Located at `github.com/cloudflare/agents/tree/main/examples`:

| Example | Description |
|---------|-------------|
| `resumable-stream-chat` | Chat with reconnection-safe streaming |
| `email-agent` | Handle incoming emails via Email Routing |
| `mcp-client` | Connect agents to external MCP servers |
| `mcp-worker` | Expose agent capabilities via MCP protocol |
| `cross-domain` | Multi-domain authentication patterns |
| `tictactoe` | Multiplayer game with shared state |
| `a2a` | Agent-to-agent communication |
| `codemode` | Code transformation workflows |
| `playground` | Interactive testing sandbox |

Browse each folder for complete implementation code and wrangler configuration.

---

## Selection Matrix

| Goal | Approach |
|------|----------|
| Conversational bot | Agent + onMessage handler |
| Custom data schema | Agent + setState() |
| Knowledge retrieval | Agent + Vectorize |
| Background jobs | Agent + schedule() |
| External integrations | Agent + tool definitions |

---

## Commands Reference

**Local execution:**

```bash
cd my-agent
npm install
npm start
# Accessible at http://localhost:8787
```

**Production push:**

```bash
npx wrangler deploy
# Accessible at https://[name].[subdomain].workers.dev
```

**WebSocket connection:**

```javascript
// URL pattern: /agents/:className/:instanceName
const socket = new WebSocket("wss://my-agent.workers.dev/agents/MyAgent/session-123");

socket.onmessage = (e) => {
  console.log("Received:", JSON.parse(e.data));
};

socket.send(JSON.stringify({ type: "chat", content: "Hello" }));
```

**React integration:**

```tsx
import { useAgent } from "agents/react";

function Chat() {
  const { state, send } = useAgent({
    agent: "my-agent",
    name: "session-123",
  });

  // state auto-updates, send() dispatches messages
}
```

---

## Key Methods (from Agent class)

| Method | Purpose |
|--------|---------|
| `onStart()` | Runs on instance startup |
| `onConnect()` | Handles new WebSocket connections |
| `onMessage()` | Processes incoming messages |
| `onClose()` | Cleanup on disconnect |
| `setState()` | Persist and broadcast data |
| `this.sql` | Query embedded SQLite |
| `schedule()` | Delayed/recurring tasks |
| `broadcast()` | Message all connections |

---

## Help Channels

- Cloudflare Discord
- GitHub discussions on cloudflare/agents repository

---

## Reference: State Patterns

# State Management Patterns

Strategies for managing state in Cloudflare Agents.

## How State Works

State is automatically persisted to the `cf_agents_state` SQL table. The `this.state` getter lazily loads from storage, while `this.setState()` serializes and persists changes. State survives Durable Object evictions.

```typescript
class MyAgent extends Agent<Env, { count: number }> {
  initialState = { count: 0 };

  increment() {
    this.setState({ count: this.state.count + 1 });
  }

  onStateUpdate(state: State, source: string) {
    console.log("State updated by:", source);
  }
}
```

## State vs SQL: When to Use Which

### Use `this.state` + `setState()` When:

- Data is small (< 1MB recommended)
- Needs real-time sync to all connected clients
- Simple key-value or object structure
- Frequently read, occasionally updated

```typescript
interface State {
  currentUser: { id: string; name: string };
  preferences: Record<string, string>;
  recentMessages: Message[];  // Keep limited, e.g., last 50
  isTyping: boolean;
}
```

### Use `this.sql` When:

- Large datasets (many records)
- Complex queries (JOINs, aggregations, filtering)
- Historical data / audit logs
- Data that doesn't need real-time sync

```typescript
// Good for SQL
// - Full message history
// - User documents
// - Analytics events
// - Search indexes
```

## Hybrid Pattern

Combine both for optimal performance:

```typescript
interface State {
  recentMessages: Message[];
  onlineUsers: string[];
  currentDocument: Document | null;
}

export class HybridAgent extends Agent<Env, State> {
  initialState: State = {
    recentMessages: [],
    onlineUsers: [],
    currentDocument: null,
  };

  async onStart() {
    await this.sql`
      CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `;

    const recent = await this.sql`
      SELECT * FROM messages
      ORDER BY created_at DESC
      LIMIT 50
    `;

    this.setState({
      ...this.state,
      recentMessages: recent.reverse(),
    });
  }

  async addMessage(message: Message) {
    await this.sql`
      INSERT INTO messages (id, user_id, content)
      VALUES (${message.id}, ${message.userId}, ${message.content})
    `;

    const recentMessages = [...this.state.recentMessages, message].slice(-50);
    this.setState({ ...this.state, recentMessages });
  }
}
```

---

## Queue System

The SDK includes a built-in queue for background task processing. Tasks are stored in SQLite and processed in FIFO order.

### Queue Methods

| Method | Purpose |
|--------|---------|
| `queue(callback, payload)` | Add task, returns task ID |
| `dequeue(id)` | Remove specific task |
| `dequeueAll()` | Clear entire queue |
| `dequeueAllByCallback(name)` | Remove tasks by callback name |
| `getQueue(id)` | Get single task |
| `getQueues(key, value)` | Find tasks by payload field |

### Queue Example

```typescript
export class TaskAgent extends Agent<Env, State> {
  async onMessage(connection: Connection, message: string) {
    const data = JSON.parse(message);

    if (data.type === "process_later") {
      const taskId = await this.queue("processItem", {
        itemId: data.itemId,
        priority: data.priority,
      });

      connection.send(JSON.stringify({ queued: true, taskId }));
    }
  }

  // Callback receives payload and QueueItem metadata
  async processItem(payload: { itemId: string }, item: QueueItem) {
    console.log(`Processing ${payload.itemId}, queued at ${item.createdAt}`);
    // Successfully executed tasks are auto-removed
  }
}
```

**Queue characteristics:**
- Sequential processing (no parallelization)
- Persists across agent restarts
- No built-in retry mechanism
- Payloads must be JSON-serializable

---

## Context Management

Custom methods automatically have full agent context. Use `getCurrentAgent()` to access context from external functions.

```typescript
import { getCurrentAgent } from "agents";

// External utility function
async function logActivity(action: string) {
  const { agent } = getCurrentAgent<MyAgent>();
  await agent.sql`
    INSERT INTO activity_log (action, timestamp)
    VALUES (${action}, ${Date.now()})
  `;
}

export class MyAgent extends Agent<Env, State> {
  async performAction() {
    // Context automatically available
    await logActivity("action_performed");
  }
}
```

`getCurrentAgent<T>()` returns:
- `agent` - The current agent instance
- `connection` - Connection object (if applicable)
- `request` - Request object (if applicable)

---

## State Synchronization

### Optimistic Updates

Update UI immediately, then persist:

```typescript
async onMessage(connection: Connection, message: string) {
  const data = JSON.parse(message);

  if (data.type === "update_preference") {
    this.setState({
      ...this.state,
      preferences: {
        ...this.state.preferences,
        [data.key]: data.value,
      },
    });

    await this.sql`
      INSERT OR REPLACE INTO preferences (key, value)
      VALUES (${data.key}, ${data.value})
    `;
  }
}
```

### Conflict Resolution

Handle concurrent updates with versioning:

```typescript
interface State {
  document: {
    content: string;
    version: number;
    lastModifiedBy: string;
  };
}

async updateDocument(userId: string, newContent: string, expectedVersion: number) {
  if (this.state.document.version !== expectedVersion) {
    throw new Error("Conflict: document was modified by another user");
  }

  this.setState({
    ...this.state,
    document: {
      content: newContent,
      version: expectedVersion + 1,
      lastModifiedBy: userId,
    },
  });
}
```

### Per-Connection State

Track ephemeral state for each connected client:

```typescript
export class MultiUserAgent extends Agent<Env, State> {
  private connectionState = new Map<string, {
    userId: string;
    cursor: { x: number; y: number };
    lastActivity: number;
  }>();

  async onConnect(connection: Connection) {
    this.connectionState.set(connection.id, {
      userId: "",
      cursor: { x: 0, y: 0 },
      lastActivity: Date.now(),
    });
  }

  async onClose(connection: Connection) {
    this.connectionState.delete(connection.id);
  }
}
```

---

## State Migration

When state schema changes:

```typescript
interface StateV2 {
  messages: Array<{ id: string; content: string; timestamp: string }>;
  version: 2;
}

export class MigratingAgent extends Agent<Env, StateV2> {
  initialState: StateV2 = {
    messages: [],
    version: 2,
  };

  async onStart() {
    const rawState = this.state as any;

    if (!rawState.version || rawState.version < 2) {
      const migratedMessages = (rawState.messages || []).map(
        (content: string, i: number) => ({
          id: `migrated-${i}`,
          content,
          timestamp: new Date().toISOString(),
        })
      );

      this.setState({
        messages: migratedMessages,
        version: 2,
      });
    }
  }
}
```

---

## State Size Management

Keep state lean for performance:

```typescript
export class LeanStateAgent extends Agent<Env, State> {
  private readonly MAX_RECENT_MESSAGES = 100;

  async addMessage(message: Message) {
    await this.sql`INSERT INTO messages (id, content) VALUES (${message.id}, ${message.content})`;

    let recentMessages = [...this.state.recentMessages, message];
    if (recentMessages.length > this.MAX_RECENT_MESSAGES) {
      recentMessages = recentMessages.slice(-this.MAX_RECENT_MESSAGES);
    }

    this.setState({
      ...this.state,
      recentMessages,
      stats: {
        ...this.state.stats,
        totalMessages: this.state.stats.totalMessages + 1,
        lastActivity: new Date().toISOString(),
      },
    });
  }
}
```

---

## Debugging State

```typescript
async onMessage(connection: Connection, message: string) {
  const data = JSON.parse(message);

  if (data.type === "debug_state") {
    connection.send(JSON.stringify({
      type: "debug_response",
      state: this.state,
      stateSize: JSON.stringify(this.state).length,
      sqlTables: await this.sql`
        SELECT name FROM sqlite_master WHERE type='table'
      `,
    }));
  }
}
```

---

## Reference: Troubleshooting

# Agent Troubleshooting

Common issues and solutions for Cloudflare Agents.

## Connection Issues

### "WebSocket connection failed"

**Symptoms:** Client cannot connect to agent.

**Causes & Solutions:**

1. **Worker not deployed**
   ```bash
   wrangler deployments list
   wrangler deploy  # If not deployed
   ```

2. **Wrong URL path**
   ```javascript
   // Ensure your routing handles the agent path
   // Client:
   new WebSocket("wss://my-worker.workers.dev/agent/user123");

   // Worker must route to agent:
   if (url.pathname.startsWith("/agent/")) {
     const id = url.pathname.split("/")[2];
     return env.AGENT.get(env.AGENT.idFromName(id)).fetch(request);
   }
   ```

3. **CORS issues (browser clients)**
   Agents handle WebSocket upgrades automatically, but ensure your entry worker doesn't block the request.

### "Connection closed unexpectedly"

1. **Agent threw an error**
   ```bash
   wrangler tail  # Check for exceptions
   ```

2. **Message handler crashed**
   ```typescript
   async onMessage(connection: Connection, message: string) {
     try {
       // Your logic
     } catch (error) {
       console.error("Message handling error:", error);
       connection.send(JSON.stringify({ type: "error", message: error.message }));
     }
   }
   ```

3. **Hibernation woke agent with stale connection**
   Ensure you handle reconnection gracefully in client code.

## State Issues

### "State not persisting"

**Causes:**

1. **Didn't call `setState()`**
   ```typescript
   // Wrong - direct mutation doesn't persist
   this.state.messages.push(newMessage);

   // Correct - use setState
   this.setState({
     ...this.state,
     messages: [...this.state.messages, newMessage],
   });
   ```

2. **Agent crashed before state saved**
   `setState()` is durable, but if agent crashes during processing before `setState()`, changes are lost.

3. **Wrong agent instance**
   Each unique ID gets a separate agent. Ensure clients connect to the same ID.

### "State out of sync between clients"

`setState()` automatically syncs to all connected clients via `onStateUpdate()`. If sync isn't working:

1. **Check `onStateUpdate` is implemented**
   ```typescript
   onStateUpdate(state: State, source: string) {
     // This fires when state changes from any source
     console.log("State updated:", state, "from:", source);
   }
   ```

2. **Client not listening for state updates**
   ```typescript
   // React hook handles this automatically
   const { state } = useAgent({ agent: "my-agent", name: id });

   // Manual WebSocket - listen for state messages
   ws.onmessage = (event) => {
     const data = JSON.parse(event.data);
     if (data.type === "state_update") {
       updateLocalState(data.state);
     }
   };
   ```

### "State too large" / Performance issues

State is serialized as JSON. Keep it small:

```typescript
// Bad - storing everything in state
interface State {
  allMessages: Message[];  // Could be thousands
  allDocuments: Document[];
}

// Good - state for hot data, SQL for cold
interface State {
  recentMessages: Message[];  // Last 50 only
  currentDocument: Document | null;
}

// Store full history in SQL
await this.sql`INSERT INTO messages ...`;
```

## SQL Issues

### "no such table"

Table not created. Create in `onStart()`:

```typescript
async onStart() {
  await this.sql`
    CREATE TABLE IF NOT EXISTS messages (
      id TEXT PRIMARY KEY,
      content TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `;
}
```

### "SQL logic error"

Check your query syntax. Use tagged templates correctly:

```typescript
// Wrong - string interpolation (SQL injection risk!)
await this.sql`SELECT * FROM users WHERE id = '${userId}'`;

// Correct - parameterized query
await this.sql`SELECT * FROM users WHERE id = ${userId}`;
```

### SQL query returns empty

1. **Wrong table name**
2. **Data in different agent instance** (each agent ID has isolated storage)
3. **Query conditions don't match**

Debug:
```typescript
const tables = await this.sql`
  SELECT name FROM sqlite_master WHERE type='table'
`;
console.log("Tables:", tables);

const count = await this.sql`SELECT COUNT(*) as count FROM messages`;
console.log("Message count:", count);
```

## Scheduled Task Issues

### "Task never fires"

1. **Method name mismatch**
   ```typescript
   // Schedule references method that must exist
   await this.schedule(60, "sendReminder", { ... });

   // Method must be defined on the class
   async sendReminder(data: any) {
     // This method MUST exist
   }
   ```

2. **Cron syntax error**
   ```typescript
   // Invalid cron
   await this.schedule("every 5 minutes", "task", {});  // Wrong

   // Valid cron
   await this.schedule("*/5 * * * *", "task", {});  // Every 5 minutes
   ```

3. **Task was cancelled**
   ```typescript
   const schedules = await this.getSchedules();
   console.log("Active schedules:", schedules);
   ```

### "Task fires multiple times"

If you schedule in `onStart()` without checking:

```typescript
async onStart() {
  // Bad - schedules new task every time agent wakes
  await this.schedule("0 9 * * *", "dailyTask", {});

  // Good - check first
  const schedules = await this.getSchedules();
  const hasDaily = schedules.some(s => s.callback === "dailyTask");
  if (!hasDaily) {
    await this.schedule("0 9 * * *", "dailyTask", {});
  }
}
```

## Deployment Issues

### "Class MyAgent is not exported"

```typescript
// src/index.ts - Must export the class
export { MyAgent } from "./agent";

// Or if defined in same file
export class MyAgent extends Agent { ... }
```

### "Durable Object not found"

Check `wrangler.toml`:

```toml
[durable_objects]
bindings = [{ name = "AGENT", class_name = "MyAgent" }]

[[migrations]]
tag = "v1"
new_classes = ["MyAgent"]
```

### "Migration required"

When adding new Durable Object classes:

```toml
[[migrations]]
tag = "v2"  # Increment from previous
new_classes = ["NewAgentClass"]

# Or for renames
# renamed_classes = [{ from = "OldName", to = "NewName" }]
```

## AI Integration Issues

### "AI binding not found"

Add to `wrangler.toml`:

```toml
[ai]
binding = "AI"
```

### "Model not found" / "Rate limited"

```typescript
// Check model name is correct
const response = await this.env.AI.run(
  "@cf/meta/llama-3-8b-instruct",  // Exact model name
  { messages: [...] }
);

// Handle rate limits
try {
  const response = await this.env.AI.run(...);
} catch (error) {
  if (error.message.includes("rate limit")) {
    // Retry with backoff or use queue
  }
}
```

### "Streaming not working"

```typescript
// Enable streaming
const stream = await this.env.AI.run("@cf/meta/llama-3-8b-instruct", {
  messages: [...],
  stream: true,  // Must be true
});

// Iterate over stream
for await (const chunk of stream) {
  connection.send(JSON.stringify({ type: "chunk", content: chunk.response }));
}
```

## Debugging Tips

### Enable Verbose Logging

```typescript
export class MyAgent extends Agent<Env, State> {
  async onStart() {
    console.log("Agent starting, state:", JSON.stringify(this.state));
  }

  async onConnect(connection: Connection) {
    console.log("Client connected:", connection.id);
  }

  async onMessage(connection: Connection, message: string) {
    console.log("Received message:", message);
    // ... handle
    console.log("State after:", JSON.stringify(this.state));
  }

  async onClose(connection: Connection) {
    console.log("Client disconnected:", connection.id);
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
# Connect with test client or use browser console:
# new WebSocket("ws://localhost:8787/agent/test")
```

### Inspect State

Add a debug endpoint:

```typescript
async onRequest(request: Request) {
  const url = new URL(request.url);

  if (url.pathname === "/debug") {
    return Response.json({
      state: this.state,
      schedules: await this.getSchedules(),
    });
  }

  return new Response("Not found", { status: 404 });
}
```
