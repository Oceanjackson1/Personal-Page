---
title: "Cloudflare Durable Objects"
description: "Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing RPC methods, SQLite storage, alarms, WebSockets, or reviewing DO code for best practices. Covers W..."
category: "devops"
source: "community"
author: "Community"
tags: ["cloudflare", "durable", "objects"]
date: 2026-03-20
---

# Durable Objects

Build stateful, coordinated applications on Cloudflare's edge using Durable Objects.

## Retrieval Sources

Your knowledge of Durable Objects APIs and configuration may be outdated. **Prefer retrieval over pre-training** for any Durable Objects task.

| Resource | URL |
|----------|-----|
| Docs | https://developers.cloudflare.com/durable-objects/ |
| API Reference | https://developers.cloudflare.com/durable-objects/api/ |
| Best Practices | https://developers.cloudflare.com/durable-objects/best-practices/ |
| Examples | https://developers.cloudflare.com/durable-objects/examples/ |

Fetch the relevant doc page when implementing features.

## When to Use

- Creating new Durable Object classes for stateful coordination
- Implementing RPC methods, alarms, or WebSocket handlers
- Reviewing existing DO code for best practices
- Configuring wrangler.jsonc/toml for DO bindings and migrations
- Writing tests with `@cloudflare/vitest-pool-workers`
- Designing sharding strategies and parent-child relationships

## Reference Documentation

- `./references/rules.md` - Core rules, storage, concurrency, RPC, alarms
- `./references/testing.md` - Vitest setup, unit/integration tests, alarm testing
- `./references/workers.md` - Workers handlers, types, wrangler config, observability

Search: `blockConcurrencyWhile`, `idFromName`, `getByName`, `setAlarm`, `sql.exec`

## Core Principles

### Use Durable Objects For

| Need | Example |
|------|---------|
| Coordination | Chat rooms, multiplayer games, collaborative docs |
| Strong consistency | Inventory, booking systems, turn-based games |
| Per-entity storage | Multi-tenant SaaS, per-user data |
| Persistent connections | WebSockets, real-time notifications |
| Scheduled work per entity | Subscription renewals, game timeouts |

### Do NOT Use For

- Stateless request handling (use plain Workers)
- Maximum global distribution needs
- High fan-out independent requests

## Quick Reference

### Wrangler Configuration

```jsonc
// wrangler.jsonc
{
  "durable_objects": {
    "bindings": [{ "name": "MY_DO", "class_name": "MyDurableObject" }]
  },
  "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyDurableObject"] }]
}
```

### Basic Durable Object Pattern

```typescript
import { DurableObject } from "cloudflare:workers";

export interface Env {
  MY_DO: DurableObjectNamespace<MyDurableObject>;
}

export class MyDurableObject extends DurableObject<Env> {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    ctx.blockConcurrencyWhile(async () => {
      this.ctx.storage.sql.exec(`
        CREATE TABLE IF NOT EXISTS items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          data TEXT NOT NULL
        )
      `);
    });
  }

  async addItem(data: string): Promise<number> {
    const result = this.ctx.storage.sql.exec<{ id: number }>(
      "INSERT INTO items (data) VALUES (?) RETURNING id",
      data
    );
    return result.one().id;
  }
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const stub = env.MY_DO.getByName("my-instance");
    const id = await stub.addItem("hello");
    return Response.json({ id });
  },
};
```

## Critical Rules

1. **Model around coordination atoms** - One DO per chat room/game/user, not one global DO
2. **Use `getByName()` for deterministic routing** - Same input = same DO instance
3. **Use SQLite storage** - Configure `new_sqlite_classes` in migrations
4. **Initialize in constructor** - Use `blockConcurrencyWhile()` for schema setup only
5. **Use RPC methods** - Not fetch() handler (compatibility date >= 2024-04-03)
6. **Persist first, cache second** - Always write to storage before updating in-memory state
7. **One alarm per DO** - `setAlarm()` replaces any existing alarm

## Anti-Patterns (NEVER)

- Single global DO handling all requests (bottleneck)
- Using `blockConcurrencyWhile()` on every request (kills throughput)
- Storing critical state only in memory (lost on eviction/crash)
- Using `await` between related storage writes (breaks atomicity)
- Holding `blockConcurrencyWhile()` across `fetch()` or external I/O

## Stub Creation

```typescript
// Deterministic - preferred for most cases
const stub = env.MY_DO.getByName("room-123");

// From existing ID string
const id = env.MY_DO.idFromString(storedIdString);
const stub = env.MY_DO.get(id);

// New unique ID - store mapping externally
const id = env.MY_DO.newUniqueId();
const stub = env.MY_DO.get(id);
```

## Storage Operations

```typescript
// SQL (synchronous, recommended)
this.ctx.storage.sql.exec("INSERT INTO t (c) VALUES (?)", value);
const rows = this.ctx.storage.sql.exec<Row>("SELECT * FROM t").toArray();

// KV (async)
await this.ctx.storage.put("key", value);
const val = await this.ctx.storage.get<Type>("key");
```

## Alarms

```typescript
// Schedule (replaces existing)
await this.ctx.storage.setAlarm(Date.now() + 60_000);

// Handler
async alarm(): Promise<void> {
  // Process scheduled work
  // Optionally reschedule: await this.ctx.storage.setAlarm(...)
}

// Cancel
await this.ctx.storage.deleteAlarm();
```

## Testing Quick Start

```typescript
import { env } from "cloudflare:test";
import { describe, it, expect } from "vitest";

describe("MyDO", () => {
  it("should work", async () => {
    const stub = env.MY_DO.getByName("test");
    const result = await stub.addItem("test");
    expect(result).toBe(1);
  });
});
```

---

## Reference: Rules

# Durable Objects Rules & Best Practices

## Design & Sharding

### Model Around Coordination Atoms

Create one DO per logical unit needing coordination: chat room, game session, document, user, tenant.

```typescript
// ✅ Good: One DO per chat room
const stub = env.CHAT_ROOM.getByName(roomId);

// ❌ Bad: Single global DO
const stub = env.CHAT_ROOM.getByName("global"); // Bottleneck!
```

### Parent-Child Relationships

For hierarchical data, create separate child DOs. Parent tracks references, children handle own state.

```typescript
// Parent: GameServer tracks match references
// Children: GameMatch handles individual match state
async createMatch(name: string): Promise<string> {
  const matchId = crypto.randomUUID();
  this.ctx.storage.sql.exec(
    "INSERT INTO matches (id, name) VALUES (?, ?)",
    matchId, name
  );
  const child = this.env.GAME_MATCH.getByName(matchId);
  await child.init(matchId, name);
  return matchId;
}
```

### Location Hints

Influence DO creation location for latency-sensitive apps:

```typescript
const id = env.GAME.idFromName(gameId, { locationHint: "wnam" });
```

Available hints: `wnam`, `enam`, `sam`, `weur`, `eeur`, `apac`, `oc`, `afr`, `me`.

## Storage

### SQLite (Recommended)

Configure in wrangler:
```jsonc
{ "migrations": [{ "tag": "v1", "new_sqlite_classes": ["MyDO"] }] }
```

SQL API is synchronous:
```typescript
// Write
this.ctx.storage.sql.exec(
  "INSERT INTO items (name, value) VALUES (?, ?)",
  name, value
);

// Read
const rows = this.ctx.storage.sql.exec<{ id: number; name: string }>(
  "SELECT * FROM items WHERE name = ?", name
).toArray();

// Single row
const row = this.ctx.storage.sql.exec<{ count: number }>(
  "SELECT COUNT(*) as count FROM items"
).one();
```

### Migrations

**Note:** `PRAGMA user_version` is **not supported** in Durable Objects SQLite storage. Use a `_sql_schema_migrations` table instead:

```typescript
constructor(ctx: DurableObjectState, env: Env) {
  super(ctx, env);
  ctx.blockConcurrencyWhile(async () => this.migrate());
}

private migrate() {
  this.ctx.storage.sql.exec(`
    CREATE TABLE IF NOT EXISTS _sql_schema_migrations (
      id INTEGER PRIMARY KEY,
      applied_at TEXT NOT NULL DEFAULT (datetime('now'))
    )
  `);

  const currentVersion = this.ctx.storage.sql
    .exec<{ version: number }>("SELECT COALESCE(MAX(id), 0) as version FROM _sql_schema_migrations")
    .one().version;

  if (currentVersion < 1) {
    this.ctx.storage.sql.exec(`
      CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, data TEXT);
      CREATE INDEX IF NOT EXISTS idx_items_data ON items(data);
      INSERT INTO _sql_schema_migrations (id) VALUES (1);
    `);
  }
  if (currentVersion < 2) {
    this.ctx.storage.sql.exec(`
      ALTER TABLE items ADD COLUMN created_at INTEGER;
      INSERT INTO _sql_schema_migrations (id) VALUES (2);
    `);
  }
}
```

For production apps, consider [`durable-utils`](https://github.com/lambrospetrou/durable-utils#sqlite-schema-migrations) — provides a `SQLSchemaMigrations` class that tracks executed migrations both in memory and in storage. Also see [`@cloudflare/actors` storage utilities](https://github.com/cloudflare/actors/blob/main/packages/storage/src/sql-schema-migrations.ts) — a reference implementation of the same pattern used by the Cloudflare Actors framework.

### State Types

| Type | Speed | Persistence | Use Case |
|------|-------|-------------|----------|
| Class properties | Fastest | Lost on eviction | Caching, active connections |
| SQLite storage | Fast | Durable | Primary data |
| External (R2, D1) | Variable | Durable, cross-DO | Large files, shared data |

**Rule**: Always persist critical state to SQLite first, then update in-memory cache.

## Concurrency

### Input/Output Gates

Storage operations automatically block other requests (input gates). Responses wait for writes (output gates).

```typescript
async increment(): Promise<number> {
  // Safe: input gates block interleaving during storage ops
  const val = (await this.ctx.storage.get<number>("count")) ?? 0;
  await this.ctx.storage.put("count", val + 1);
  return val + 1;
}
```

### Write Coalescing

Multiple writes without `await` between them are batched atomically:

```typescript
// ✅ Good: All three writes commit atomically
this.ctx.storage.sql.exec("UPDATE accounts SET balance = balance - ? WHERE id = ?", amount, fromId);
this.ctx.storage.sql.exec("UPDATE accounts SET balance = balance + ? WHERE id = ?", amount, toId);
this.ctx.storage.sql.exec("INSERT INTO transfers (from_id, to_id, amount) VALUES (?, ?, ?)", fromId, toId, amount);

// ❌ Bad: await breaks coalescing
await this.ctx.storage.put("key1", val1);
await this.ctx.storage.put("key2", val2); // Separate transaction!
```

### Race Conditions with External I/O

`fetch()` and other non-storage I/O allows interleaving:

```typescript
// ⚠️ Race condition possible
async processItem(id: string) {
  const item = await this.ctx.storage.get<Item>(`item:${id}`);
  if (item?.status === "pending") {
    await fetch("https://api.example.com/process"); // Other requests can run here!
    await this.ctx.storage.put(`item:${id}`, { status: "completed" });
  }
}
```

**Solution**: Use optimistic locking (version numbers) or `transaction()`.

### blockConcurrencyWhile()

Blocks ALL concurrency. Use sparingly - only for initialization:

```typescript
// ✅ Good: One-time init
constructor(ctx: DurableObjectState, env: Env) {
  super(ctx, env);
  ctx.blockConcurrencyWhile(async () => this.migrate());
}

// ❌ Bad: On every request (kills throughput)
async handleRequest() {
  await this.ctx.blockConcurrencyWhile(async () => {
    // ~5ms = max 200 req/sec
  });
}
```

**Never** hold across external I/O (fetch, R2, KV).

## RPC Methods

Use RPC (compatibility date >= 2024-04-03) instead of fetch() handler:

```typescript
export class ChatRoom extends DurableObject<Env> {
  async sendMessage(userId: string, content: string): Promise<Message> {
    // Public methods are RPC endpoints
    const result = this.ctx.storage.sql.exec<{ id: number }>(
      "INSERT INTO messages (user_id, content) VALUES (?, ?) RETURNING id",
      userId, content
    );
    return { id: result.one().id, userId, content };
  }
}

// Caller
const stub = env.CHAT_ROOM.getByName(roomId);
const msg = await stub.sendMessage("user-123", "Hello!"); // Typed!
```

### Explicit init() Method

DOs don't know their own ID. Pass identity explicitly:

```typescript
async init(entityId: string, metadata: Metadata): Promise<void> {
  await this.ctx.storage.put("entityId", entityId);
  await this.ctx.storage.put("metadata", metadata);
}
```

## Alarms

One alarm per DO. `setAlarm()` replaces existing.

```typescript
// Schedule
await this.ctx.storage.setAlarm(Date.now() + 60_000);

// Handler
async alarm(): Promise<void> {
  const tasks = this.ctx.storage.sql.exec<Task>(
    "SELECT * FROM tasks WHERE due_at <= ?", Date.now()
  ).toArray();
  
  for (const task of tasks) {
    await this.processTask(task);
  }
  
  // Reschedule if more work
  const next = this.ctx.storage.sql.exec<{ due_at: number }>(
    "SELECT MIN(due_at) as due_at FROM tasks WHERE due_at > ?", Date.now()
  ).one();
  if (next?.due_at) {
    await this.ctx.storage.setAlarm(next.due_at);
  }
}

// Get/Delete
const alarm = await this.ctx.storage.getAlarm();
await this.ctx.storage.deleteAlarm();
```

**Retry**: Alarms auto-retry on failure. Use idempotent handlers.

## WebSockets (Hibernation API)

```typescript
async fetch(request: Request): Promise<Response> {
  const pair = new WebSocketPair();
  this.ctx.acceptWebSocket(pair[1]);
  return new Response(null, { status: 101, webSocket: pair[0] });
}

async webSocketMessage(ws: WebSocket, message: string | ArrayBuffer) {
  const data = JSON.parse(message as string);
  // Handle message
  ws.send(JSON.stringify({ type: "ack" }));
}

async webSocketClose(ws: WebSocket, code: number, reason: string) {
  // Cleanup
}

// Broadcast
getWebSockets().forEach(ws => ws.send(JSON.stringify(payload)));
```

## Error Handling

```typescript
async safeOperation(): Promise<Result> {
  try {
    return await this.riskyOperation();
  } catch (error) {
    console.error("Operation failed:", error);
    // Log to external service if needed
    throw error; // Re-throw to signal failure to caller
  }
}
```

**Note**: Uncaught exceptions may terminate the DO instance. In-memory state is lost, but SQLite storage persists.

---

## Reference: Testing

# Testing Durable Objects

Use `@cloudflare/vitest-pool-workers` to test DOs inside the Workers runtime.

## Setup

### Install Dependencies

```bash
npm i -D vitest@~3.2.0 @cloudflare/vitest-pool-workers
```

### vitest.config.ts

```typescript
import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: "./wrangler.toml" },
      },
    },
  },
});
```

### TypeScript Config (test/tsconfig.json)

```jsonc
{
  "extends": "../tsconfig.json",
  "compilerOptions": {
    "moduleResolution": "bundler",
    "types": ["@cloudflare/vitest-pool-workers"]
  },
  "include": ["./**/*.ts", "../src/worker-configuration.d.ts"]
}
```

### Environment Types (env.d.ts)

```typescript
declare module "cloudflare:test" {
  interface ProvidedEnv extends Env {}
}
```

## Unit Tests (Direct DO Access)

```typescript
import { env } from "cloudflare:test";
import { describe, it, expect } from "vitest";

describe("Counter DO", () => {
  it("should increment", async () => {
    const stub = env.COUNTER.getByName("test-counter");
    
    expect(await stub.increment()).toBe(1);
    expect(await stub.increment()).toBe(2);
    expect(await stub.getCount()).toBe(2);
  });

  it("isolates different instances", async () => {
    const stub1 = env.COUNTER.getByName("counter-1");
    const stub2 = env.COUNTER.getByName("counter-2");
    
    await stub1.increment();
    await stub1.increment();
    await stub2.increment();
    
    expect(await stub1.getCount()).toBe(2);
    expect(await stub2.getCount()).toBe(1);
  });
});
```

## Integration Tests (HTTP via SELF)

```typescript
import { SELF } from "cloudflare:test";
import { describe, it, expect } from "vitest";

describe("Worker HTTP", () => {
  it("should increment via POST", async () => {
    const res = await SELF.fetch("http://example.com?id=test", {
      method: "POST",
    });
    
    expect(res.status).toBe(200);
    const data = await res.json<{ count: number }>();
    expect(data.count).toBe(1);
  });

  it("should get count via GET", async () => {
    await SELF.fetch("http://example.com?id=get-test", { method: "POST" });
    await SELF.fetch("http://example.com?id=get-test", { method: "POST" });
    
    const res = await SELF.fetch("http://example.com?id=get-test");
    const data = await res.json<{ count: number }>();
    expect(data.count).toBe(2);
  });
});
```

## Direct Internal Access

Use `runInDurableObject()` to access instance internals and storage:

```typescript
import { env, runInDurableObject } from "cloudflare:test";
import { describe, it, expect } from "vitest";
import { Counter } from "../src";

describe("DO internals", () => {
  it("can verify storage directly", async () => {
    const stub = env.COUNTER.getByName("direct-test");
    await stub.increment();
    await stub.increment();

    await runInDurableObject(stub, async (instance: Counter, state) => {
      expect(instance).toBeInstanceOf(Counter);
      
      const result = state.storage.sql
        .exec<{ value: number }>(
          "SELECT value FROM counters WHERE name = ?",
          "default"
        )
        .one();
      expect(result.value).toBe(2);
    });
  });
});
```

## List DO IDs

```typescript
import { env, listDurableObjectIds } from "cloudflare:test";
import { describe, it, expect } from "vitest";

describe("DO listing", () => {
  it("can list all IDs in namespace", async () => {
    const id1 = env.COUNTER.idFromName("list-1");
    const id2 = env.COUNTER.idFromName("list-2");
    
    await env.COUNTER.get(id1).increment();
    await env.COUNTER.get(id2).increment();
    
    const ids = await listDurableObjectIds(env.COUNTER);
    expect(ids.length).toBe(2);
    expect(ids.some(id => id.equals(id1))).toBe(true);
    expect(ids.some(id => id.equals(id2))).toBe(true);
  });
});
```

## Testing Alarms

Use `runDurableObjectAlarm()` to trigger alarms immediately:

```typescript
import { env, runInDurableObject, runDurableObjectAlarm } from "cloudflare:test";
import { describe, it, expect } from "vitest";

describe("DO alarms", () => {
  it("can trigger alarms immediately", async () => {
    const stub = env.COUNTER.getByName("alarm-test");
    await stub.increment();
    await stub.increment();
    expect(await stub.getCount()).toBe(2);

    // Schedule alarm
    await runInDurableObject(stub, async (instance, state) => {
      await state.storage.setAlarm(Date.now() + 60_000);
    });

    // Execute immediately without waiting
    const ran = await runDurableObjectAlarm(stub);
    expect(ran).toBe(true);

    // Verify alarm handler ran (if it resets counter)
    expect(await stub.getCount()).toBe(0);

    // No alarm scheduled now
    const ranAgain = await runDurableObjectAlarm(stub);
    expect(ranAgain).toBe(false);
  });
});
```

Example alarm handler:
```typescript
async alarm(): Promise<void> {
  this.ctx.storage.sql.exec("DELETE FROM counters");
}
```

## Test Isolation

Each test gets isolated storage automatically. DOs from one test don't affect others:

```typescript
describe("Isolation", () => {
  it("first test creates DO", async () => {
    const stub = env.COUNTER.getByName("isolated");
    await stub.increment();
    expect(await stub.getCount()).toBe(1);
  });

  it("second test has fresh state", async () => {
    const ids = await listDurableObjectIds(env.COUNTER);
    expect(ids.length).toBe(0); // Previous test's DO is gone
    
    const stub = env.COUNTER.getByName("isolated");
    expect(await stub.getCount()).toBe(0); // Fresh instance
  });
});
```

## SQLite Storage Testing

```typescript
describe("SQLite", () => {
  it("can verify SQL storage", async () => {
    const stub = env.COUNTER.getByName("sqlite-test");
    await stub.increment("page-views");
    await stub.increment("page-views");
    await stub.increment("api-calls");

    await runInDurableObject(stub, async (instance, state) => {
      const rows = state.storage.sql
        .exec<{ name: string; value: number }>(
          "SELECT name, value FROM counters ORDER BY name"
        )
        .toArray();

      expect(rows).toEqual([
        { name: "api-calls", value: 1 },
        { name: "page-views", value: 2 },
      ]);

      expect(state.storage.sql.databaseSize).toBeGreaterThan(0);
    });
  });
});
```

## Running Tests

```bash
npx vitest        # Watch mode
npx vitest run    # Single run
```

package.json:
```json
{
  "scripts": {
    "test": "vitest"
  }
}
```

---

## Reference: Workers

# Cloudflare Workers Best Practices

High-level guidance for Workers that invoke Durable Objects.

## Wrangler Configuration

### wrangler.jsonc (Recommended)

```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-01",
  "compatibility_flags": ["nodejs_compat"],

  "durable_objects": {
    "bindings": [
      { "name": "CHAT_ROOM", "class_name": "ChatRoom" },
      { "name": "USER_SESSION", "class_name": "UserSession" }
    ]
  },

  "migrations": [
    { "tag": "v1", "new_sqlite_classes": ["ChatRoom", "UserSession"] }
  ],

  // Environment variables
  "vars": {
    "ENVIRONMENT": "production"
  },

  // KV namespaces
  "kv_namespaces": [
    { "binding": "CONFIG", "id": "abc123" }
  ],

  // R2 buckets
  "r2_buckets": [
    { "binding": "UPLOADS", "bucket_name": "my-uploads" }
  ],

  // D1 databases
  "d1_databases": [
    { "binding": "DB", "database_id": "xyz789" }
  ]
}
```

### wrangler.toml (Alternative)

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-01"
compatibility_flags = ["nodejs_compat"]

[[durable_objects.bindings]]
name = "CHAT_ROOM"
class_name = "ChatRoom"

[[migrations]]
tag = "v1"
new_sqlite_classes = ["ChatRoom"]

[vars]
ENVIRONMENT = "production"
```

## TypeScript Types

### Environment Interface

```typescript
// src/types.ts
import { ChatRoom } from "./durable-objects/chat-room";
import { UserSession } from "./durable-objects/user-session";

export interface Env {
  // Durable Objects
  CHAT_ROOM: DurableObjectNamespace<ChatRoom>;
  USER_SESSION: DurableObjectNamespace<UserSession>;

  // KV
  CONFIG: KVNamespace;

  // R2
  UPLOADS: R2Bucket;

  // D1
  DB: D1Database;

  // Environment variables
  ENVIRONMENT: string;
  API_KEY: string; // From secrets
}
```

### Export Durable Object Classes

```typescript
// src/index.ts
export { ChatRoom } from "./durable-objects/chat-room";
export { UserSession } from "./durable-objects/user-session";

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    // Worker handler
  },
};
```

## Worker Handler Pattern

```typescript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    try {
      // Route to appropriate handler
      if (url.pathname.startsWith("/api/rooms")) {
        return handleRooms(request, env);
      }
      if (url.pathname.startsWith("/api/users")) {
        return handleUsers(request, env);
      }

      return new Response("Not Found", { status: 404 });
    } catch (error) {
      console.error("Request failed:", error);
      return new Response("Internal Server Error", { status: 500 });
    }
  },
};

async function handleRooms(request: Request, env: Env): Promise<Response> {
  const url = new URL(request.url);
  const roomId = url.searchParams.get("room");

  if (!roomId) {
    return Response.json({ error: "Missing room parameter" }, { status: 400 });
  }

  const stub = env.CHAT_ROOM.getByName(roomId);

  if (request.method === "POST") {
    const body = await request.json<{ userId: string; message: string }>();
    const result = await stub.sendMessage(body.userId, body.message);
    return Response.json(result);
  }

  const messages = await stub.getMessages();
  return Response.json(messages);
}
```

## Request Validation

```typescript
import { z } from "zod";

const SendMessageSchema = z.object({
  userId: z.string().min(1),
  message: z.string().min(1).max(1000),
});

async function handleSendMessage(request: Request, env: Env): Promise<Response> {
  const body = await request.json();
  const result = SendMessageSchema.safeParse(body);

  if (!result.success) {
    return Response.json(
      { error: "Validation failed", details: result.error.issues },
      { status: 400 }
    );
  }

  const stub = env.CHAT_ROOM.getByName(result.data.userId);
  const message = await stub.sendMessage(result.data.userId, result.data.message);
  return Response.json(message);
}
```

## Observability & Logging

### Structured Logging

```typescript
function log(level: "info" | "warn" | "error", message: string, data?: Record<string, unknown>) {
  console.log(JSON.stringify({
    level,
    message,
    timestamp: new Date().toISOString(),
    ...data,
  }));
}

// Usage
log("info", "Request received", { path: url.pathname, method: request.method });
log("error", "DO call failed", { roomId, error: String(error) });
```

### Request Tracing

```typescript
async function handleRequest(request: Request, env: Env): Promise<Response> {
  const requestId = crypto.randomUUID();
  const startTime = Date.now();

  try {
    const response = await processRequest(request, env);

    log("info", "Request completed", {
      requestId,
      duration: Date.now() - startTime,
      status: response.status,
    });

    return response;
  } catch (error) {
    log("error", "Request failed", {
      requestId,
      duration: Date.now() - startTime,
      error: String(error),
    });
    throw error;
  }
}
```

### Tail Workers (Production)

For production logging, use Tail Workers to forward logs:

```jsonc
// wrangler.jsonc
{
  "tail_consumers": [
    { "service": "log-collector" }
  ]
}
```

## Error Handling

### Graceful DO Errors

```typescript
async function callDO(stub: DurableObjectStub<ChatRoom>, method: string): Promise<Response> {
  try {
    const result = await stub.getMessages();
    return Response.json(result);
  } catch (error) {
    if (error instanceof Error) {
      // DO threw an error
      log("error", "DO operation failed", { error: error.message });
      return Response.json(
        { error: "Service temporarily unavailable" },
        { status: 503 }
      );
    }
    throw error;
  }
}
```

### Timeout Handling

```typescript
async function withTimeout<T>(promise: Promise<T>, ms: number): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), ms)
  );
  return Promise.race([promise, timeout]);
}

// Usage
const result = await withTimeout(stub.processData(data), 5000);
```

## CORS Handling

```typescript
function corsHeaders(): HeadersInit {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders() });
    }

    const response = await handleRequest(request, env);
    
    // Add CORS headers to response
    const newHeaders = new Headers(response.headers);
    Object.entries(corsHeaders()).forEach(([k, v]) => newHeaders.set(k, v));
    
    return new Response(response.body, {
      status: response.status,
      headers: newHeaders,
    });
  },
};
```

## Secrets Management

Set secrets via wrangler CLI (not in config files):

```bash
wrangler secret put API_KEY
wrangler secret put DATABASE_URL
```

Access in code:
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const apiKey = env.API_KEY; // From secret
    // ...
  },
};
```

## Development Commands

```bash
# Local development
wrangler dev

# Deploy
wrangler deploy

# Tail logs
wrangler tail

# List DOs
wrangler d1 execute DB --command "SELECT * FROM _cf_DO"
```
