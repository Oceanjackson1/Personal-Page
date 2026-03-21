---
title: "Sentry Next.js SDK"
description: "Sentry 错误监控 Next.js SDK 集成，服务端和客户端错误追踪"
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "nextjs", "sdk"]
date: 2026-03-20
---

# Sentry Next.js SDK

Opinionated wizard that scans your Next.js project and guides you through complete Sentry setup across all three runtimes: browser, Node.js server, and Edge.

## Invoke This Skill When

- User asks to "add Sentry to Next.js" or "set up Sentry" in a Next.js app
- User wants to install or configure `@sentry/nextjs`
- User wants error monitoring, tracing, session replay, logging, or profiling for Next.js
- User asks about `instrumentation.ts`, `withSentryConfig()`, or `global-error.tsx`
- User wants to capture server actions, server component errors, or edge runtime errors

> **Note:** SDK versions and APIs below reflect current Sentry docs at time of writing (`@sentry/nextjs` ≥8.28.0).
> Always verify against [docs.sentry.io/platforms/javascript/guides/nextjs/](https://docs.sentry.io/platforms/javascript/guides/nextjs/) before implementing.

---

## Phase 1: Detect

Run these commands to understand the project before making any recommendations:

```bash
# Detect Next.js version and existing Sentry
cat package.json | grep -E '"next"|"@sentry/'

# Detect router type (App Router vs Pages Router)
ls src/app app src/pages pages 2>/dev/null

# Check for existing Sentry config files
ls instrumentation.ts instrumentation-client.ts sentry.server.config.ts sentry.edge.config.ts 2>/dev/null
ls src/instrumentation.ts src/instrumentation-client.ts 2>/dev/null

# Check next.config
ls next.config.ts next.config.js next.config.mjs 2>/dev/null

# Check for existing error boundaries
find . -name "global-error.tsx" -o -name "_error.tsx" 2>/dev/null | grep -v node_modules

# Check build tool
cat package.json | grep -E '"turbopack"|"webpack"'

# Check for logging libraries
cat package.json | grep -E '"pino"|"winston"|"bunyan"'

# Check for companion backend
ls ../backend ../server ../api 2>/dev/null
cat ../go.mod ../requirements.txt ../Gemfile 2>/dev/null | head -3
```

**What to determine:**

| Question | Impact |
|----------|--------|
| Next.js version? | 13+ required; 15+ needed for Turbopack support |
| App Router or Pages Router? | Determines error boundary files needed (`global-error.tsx` vs `_error.tsx`) |
| `@sentry/nextjs` already present? | Skip install, go to feature config |
| Existing `instrumentation.ts`? | Merge Sentry into it rather than replace |
| Turbopack in use? | Tree-shaking in `withSentryConfig` is webpack-only |
| Logging library detected? | Recommend Sentry Logs integration |
| Backend directory found? | Trigger Phase 4 cross-link suggestion |

---

## Phase 2: Recommend

Present a concrete recommendation based on what you found. Don't ask open-ended questions — lead with a proposal:

**Recommended (core coverage):**
- ✅ **Error Monitoring** — always; captures server errors, client errors, server actions, and unhandled promise rejections
- ✅ **Tracing** — server-side request tracing + client-side navigation spans across all runtimes
- ✅ **Session Replay** — recommended for user-facing apps; records sessions around errors

**Optional (enhanced observability):**
- ⚡ **Logging** — structured logs via `Sentry.logger.*`; recommend when `pino`/`winston` or log search is needed
- ⚡ **Profiling** — continuous profiling; requires `Document-Policy: js-profiling` header
- ⚡ **AI Monitoring** — OpenAI, Vercel AI SDK, Anthropic; recommend when AI/LLM calls detected
- ⚡ **Crons** — detect missed/failed scheduled jobs; recommend when cron patterns detected
- ⚡ **Metrics** — custom metrics via `Sentry.metrics.*`; recommend when custom KPIs or business metrics needed

**Recommendation logic:**

| Feature | Recommend when... |
|---------|------------------|
| Error Monitoring | **Always** — non-negotiable baseline |
| Tracing | **Always for Next.js** — server route tracing + client navigation are high-value |
| Session Replay | User-facing app, login flows, or checkout pages |
| Logging | App uses structured logging or needs log-to-trace correlation |
| Profiling | Performance-critical app; client sets `Document-Policy: js-profiling` |
| AI Monitoring | App makes OpenAI, Vercel AI SDK, or Anthropic calls |
| Crons | App has Vercel Cron jobs, scheduled API routes, or `node-cron` usage |
| Metrics | App needs custom counters, gauges, or histograms via `Sentry.metrics.*` |

Propose: *"I recommend setting up Error Monitoring + Tracing + Session Replay. Want me to also add Logging or Profiling?"*

---

## Phase 3: Guide

### Option 1: Wizard (Recommended)

```bash
npx @sentry/wizard@latest -i nextjs
```

The wizard walks you through login, org/project selection, and auth token setup interactively — no manual token creation needed. It then installs the SDK, creates all necessary config files (`instrumentation-client.ts`, `sentry.server.config.ts`, `sentry.edge.config.ts`, `instrumentation.ts`), wraps `next.config.ts` with `withSentryConfig()`, configures source map upload, and adds a `/sentry-example-page` for verification.

**Skip to [Verification](#verification) after running the wizard.**

---

### Option 2: Manual Setup

#### Install

```bash
npm install @sentry/nextjs --save
```

#### Create `instrumentation-client.ts` — Browser / Client Runtime

> Older docs used `sentry.client.config.ts` — the current pattern is `instrumentation-client.ts`.

```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN ?? "___PUBLIC_DSN___",

  sendDefaultPii: true,

  // 100% in dev, 10% in production
  tracesSampleRate: process.env.NODE_ENV === "development" ? 1.0 : 0.1,

  // Session Replay: 10% of all sessions, 100% of sessions with errors
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,

  enableLogs: true,

  integrations: [
    Sentry.replayIntegration(),
    // Optional: user feedback widget
    // Sentry.feedbackIntegration({ colorScheme: "system" }),
  ],
});

// Hook into App Router navigation transitions (App Router only)
export const onRouterTransitionStart = Sentry.captureRouterTransitionStart;
```

#### Create `sentry.server.config.ts` — Node.js Server Runtime

```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN ?? "___DSN___",

  sendDefaultPii: true,
  tracesSampleRate: process.env.NODE_ENV === "development" ? 1.0 : 0.1,

  // Attach local variable values to stack frames
  includeLocalVariables: true,

  enableLogs: true,
});
```

#### Create `sentry.edge.config.ts` — Edge Runtime

```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN ?? "___DSN___",

  sendDefaultPii: true,
  tracesSampleRate: process.env.NODE_ENV === "development" ? 1.0 : 0.1,

  enableLogs: true,
});
```

#### Create `instrumentation.ts` — Server-Side Registration Hook

> Requires `experimental.instrumentationHook: true` in `next.config` for Next.js < 14.0.4. It's stable in 14.0.4+.

```typescript
import * as Sentry from "@sentry/nextjs";

export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    await import("./sentry.server.config");
  }

  if (process.env.NEXT_RUNTIME === "edge") {
    await import("./sentry.edge.config");
  }
}

// Automatically captures all unhandled server-side request errors
// Requires @sentry/nextjs >= 8.28.0
export const onRequestError = Sentry.captureRequestError;
```

**Runtime dispatch:**

| `NEXT_RUNTIME` | Config file loaded |
|---|---|
| `"nodejs"` | `sentry.server.config.ts` |
| `"edge"` | `sentry.edge.config.ts` |
| *(client bundle)* | `instrumentation-client.ts` (Next.js handles this directly) |

#### App Router: Create `app/global-error.tsx`

This catches errors in the root layout and React render errors:

```tsx
"use client";

import * as Sentry from "@sentry/nextjs";
import NextError from "next/error";
import { useEffect } from "react";

export default function GlobalError({
  error,
}: {
  error: Error & { digest?: string };
}) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <html>
      <body>
        <NextError statusCode={0} />
      </body>
    </html>
  );
}
```

#### Pages Router: Update `pages/_error.tsx`

```tsx
import * as Sentry from "@sentry/nextjs";
import type { NextPageContext } from "next";
import NextErrorComponent from "next/error";

type ErrorProps = { statusCode: number };

export default function CustomError({ statusCode }: ErrorProps) {
  return <NextErrorComponent statusCode={statusCode} />;
}

CustomError.getInitialProps = async (ctx: NextPageContext) => {
  await Sentry.captureUnderscoreErrorException(ctx);
  return NextErrorComponent.getInitialProps(ctx);
};
```

#### Wrap `next.config.ts` with `withSentryConfig()`

```typescript
import type { NextConfig } from "next";
import { withSentryConfig } from "@sentry/nextjs";

const nextConfig: NextConfig = {
  // your existing Next.js config
};

export default withSentryConfig(nextConfig, {
  org: "___ORG_SLUG___",
  project: "___PROJECT_SLUG___",

  // Source map upload auth token (see Source Maps section below)
  authToken: process.env.SENTRY_AUTH_TOKEN,

  // Upload wider set of client source files for better stack trace resolution
  widenClientFileUpload: true,

  // Create a proxy API route to bypass ad-blockers
  tunnelRoute: "/monitoring",

  // Suppress non-CI output
  silent: !process.env.CI,
});
```

#### Exclude Tunnel Route from Middleware

If you have `middleware.ts`, exclude the tunnel path from auth or redirect logic:

```typescript
// middleware.ts
export const config = {
  matcher: [
    // Exclude monitoring route, Next.js internals, and static files
    "/((?!monitoring|_next/static|_next/image|favicon.ico).*)",
  ],
};
```

---

### Source Maps Setup

Source maps make production stack traces readable — without them, you see minified code. This is non-negotiable for production apps.

**Step 1: Generate a Sentry auth token**

Go to [sentry.io/settings/auth-tokens/](https://sentry.io/settings/auth-tokens/) and create a token with `project:releases` and `org:read` scopes.

**Step 2: Set environment variables**

```bash
# .env.sentry-build-plugin  (gitignore this file)
SENTRY_AUTH_TOKEN=sntrys_eyJ...
```

Or set in CI secrets:

```bash
SENTRY_AUTH_TOKEN=sntrys_eyJ...
SENTRY_ORG=my-org        # optional if set in next.config
SENTRY_PROJECT=my-project # optional if set in next.config
```

**Step 3: Add to `.gitignore`**

```
.env.sentry-build-plugin
```

**Step 4: Verify `authToken` is wired in `next.config.ts`**

```typescript
withSentryConfig(nextConfig, {
  org: "my-org",
  project: "my-project",
  authToken: process.env.SENTRY_AUTH_TOKEN, // reads from .env.sentry-build-plugin or CI env
  widenClientFileUpload: true,
});
```

Source maps are uploaded automatically on every `next build`.

---

### For Each Agreed Feature

Load the corresponding reference file and follow its steps:

| Feature | Reference file | Load when... |
|---------|---------------|-------------|
| Error Monitoring | `references/error-monitoring.md` | Always (baseline) — App Router error boundaries, Pages Router `_error.tsx`, server action wrapping |
| Tracing | `references/tracing.md` | Server-side request tracing, client navigation, distributed tracing, `tracePropagationTargets` |
| Session Replay | `references/session-replay.md` | User-facing app; privacy masking, canvas recording, network capture |
| Logging | `references/logging.md` | Structured logs, `Sentry.logger.*`, log-to-trace correlation |
| Profiling | `references/profiling.md` | Continuous profiling, `Document-Policy` header, `nodeProfilingIntegration` |
| AI Monitoring | `references/ai-monitoring.md` | App uses OpenAI, Vercel AI SDK, or Anthropic |
| Crons | `references/crons.md` | Vercel Cron, scheduled API routes, `node-cron` |

For each feature: read the reference file, follow its steps exactly, and verify before moving on.

---

## Verification

After wizard or manual setup, verify Sentry is working:

```typescript
// Add temporarily to a server action or API route, then remove
import * as Sentry from "@sentry/nextjs";

throw new Error("Sentry test error — delete me");
// or
Sentry.captureException(new Error("Sentry test error — delete me"));
```

Then check your [Sentry Issues dashboard](https://sentry.io/issues/) — the error should appear within ~30 seconds.

**Verification checklist:**

| Check | How |
|-------|-----|
| Client errors captured | Throw in a client component, verify in Sentry |
| Server errors captured | Throw in a server action or API route |
| Edge errors captured | Throw in middleware or edge route handler |
| Source maps working | Check stack trace shows readable file names |
| Session Replay working | Check Replays tab in Sentry dashboard |

---

## Config Reference

### `Sentry.init()` Options

| Option | Type | Default | Notes |
|--------|------|---------|-------|
| `dsn` | `string` | — | Required. Use `NEXT_PUBLIC_SENTRY_DSN` for client, `SENTRY_DSN` for server |
| `tracesSampleRate` | `number` | — | 0–1; 1.0 in dev, 0.1 in prod recommended |
| `replaysSessionSampleRate` | `number` | `0.1` | Fraction of all sessions recorded |
| `replaysOnErrorSampleRate` | `number` | `1.0` | Fraction of error sessions recorded |
| `sendDefaultPii` | `boolean` | `false` | Include IP, request headers in events |
| `includeLocalVariables` | `boolean` | `false` | Attach local variable values to stack frames (server only) |
| `enableLogs` | `boolean` | `false` | Enable Sentry Logs product |
| `environment` | `string` | auto | `"production"`, `"staging"`, etc. |
| `release` | `string` | auto | Set to commit SHA or version tag |
| `debug` | `boolean` | `false` | Log SDK activity to console |

### `withSentryConfig()` Options

| Option | Type | Notes |
|--------|------|-------|
| `org` | `string` | Sentry organization slug |
| `project` | `string` | Sentry project slug |
| `authToken` | `string` | Source map upload token (`SENTRY_AUTH_TOKEN`) |
| `widenClientFileUpload` | `boolean` | Upload more client files for better stack traces |
| `tunnelRoute` | `string` | API route path for ad-blocker bypass (e.g. `"/monitoring"`) |
| `silent` | `boolean` | Suppress build output (`!process.env.CI` recommended) |
| `webpack.treeshake.*` | `object` | Tree-shake SDK features (webpack only, not Turbopack) |

### Environment Variables

| Variable | Runtime | Purpose |
|----------|---------|---------|
| `NEXT_PUBLIC_SENTRY_DSN` | Client | DSN for browser Sentry init (public) |
| `SENTRY_DSN` | Server / Edge | DSN for server/edge Sentry init |
| `SENTRY_AUTH_TOKEN` | Build | Source map upload auth token (secret) |
| `SENTRY_ORG` | Build | Org slug (alternative to `org` in config) |
| `SENTRY_PROJECT` | Build | Project slug (alternative to `project` in config) |
| `SENTRY_RELEASE` | Server | Release version string (auto-detected from git) |
| `NEXT_RUNTIME` | Server / Edge | `"nodejs"` or `"edge"` (set by Next.js internally) |

---

## Phase 4: Cross-Link

After completing Next.js setup, check for companion services:

```bash
# Check for backend services in adjacent directories
ls ../backend ../server ../api ../services 2>/dev/null

# Check for backend language indicators
cat ../go.mod 2>/dev/null | head -3
cat ../requirements.txt ../pyproject.toml 2>/dev/null | head -3
cat ../Gemfile 2>/dev/null | head -3
cat ../pom.xml ../build.gradle 2>/dev/null | head -3
```

If a backend is found, suggest the matching SDK skill:

| Backend detected | Suggest skill |
|-----------------|--------------|
| Go (`go.mod`) | `sentry-go-sdk` |
| Python (`requirements.txt`, `pyproject.toml`) | `sentry-python-sdk` |
| Ruby (`Gemfile`) | `sentry-ruby-sdk` |
| Java/Kotlin (`pom.xml`, `build.gradle`) | See [docs.sentry.io/platforms/java/](https://docs.sentry.io/platforms/java/) |
| Node.js (Express, Fastify, Hapi) | `@sentry/node` — see [docs.sentry.io/platforms/javascript/guides/express/](https://docs.sentry.io/platforms/javascript/guides/express/) |

Connecting frontend and backend with the same DSN or linked projects enables **distributed tracing** — stack traces that span your browser, Next.js server, and backend API in a single trace view.

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Events not appearing | DSN misconfigured or `debug: false` hiding errors | Set `debug: true` temporarily; check browser network tab for requests to `sentry.io` |
| Stack traces show minified code | Source maps not uploading | Check `SENTRY_AUTH_TOKEN` is set; run `next build` and look for "Source Maps" in build output |
| `onRequestError` not firing | SDK version < 8.28.0 | Upgrade: `npm install @sentry/nextjs@latest` |
| Edge runtime errors missing | `sentry.edge.config.ts` not loaded | Verify `instrumentation.ts` imports it when `NEXT_RUNTIME === "edge"` |
| Tunnel route returns 404 | `tunnelRoute` set but Next.js route missing | The plugin creates it automatically; check you ran `next build` after adding `tunnelRoute` |
| `withSentryConfig` tree-shaking breaks build | Turbopack in use | Tree-shaking options only work with webpack; remove `webpack.treeshake` options when using Turbopack |
| `global-error.tsx` not catching errors | Missing `"use client"` directive | Add `"use client"` as the very first line of `global-error.tsx` |
| Session Replay not recording | `replayIntegration()` missing from client init | Add `Sentry.replayIntegration()` to `integrations` in `instrumentation-client.ts` |

---

## Reference: Ai Monitoring

# AI Monitoring — Sentry Next.js SDK

> OpenAI integration: `@sentry/nextjs` ≥10.28.0+  
> Vercel AI SDK integration: ≥10.6.0+ (Node/Edge/Bun), ≥10.12.0+ (Deno)  
> Anthropic integration: see platform docs

> ⚠️ **Tracing must be enabled.** AI monitoring piggybacks on tracing infrastructure. `tracesSampleRate` must be > 0.

---

## Overview

Sentry AI Agents Monitoring automatically tracks:
- Agent runs and error rates
- LLM calls (model, token counts, estimated cost)
- Tool calls and outputs
- Agent handoffs
- Full prompt/completion data (opt-in)
- Performance bottlenecks across the AI pipeline

---

## Supported AI Libraries

| Library | Integration API | Auto-enabled (Node server)? | Min SDK Version |
|---------|----------------|----------------------------|----------------|
| **OpenAI** (`openai`) | `openAIIntegration` / `instrumentOpenAiClient` | ✅ Yes | **10.28.0** |
| **Vercel AI SDK** (`ai`) | `vercelAIIntegration` | ✅ Yes (Node), ❌ Edge manual | **10.6.0** |
| **Anthropic** (`@anthropic-ai/sdk`) | `anthropicAIIntegration` / `instrumentAnthropicAiClient` | ✅ Yes | See platform docs |

---

## OpenAI Integration

### Which API to Use?

| Context | API |
|---------|-----|
| **Next.js server-side** (API routes, Server Components, Route Handlers) | `Sentry.openAIIntegration()` in `sentry.server.config.ts` |
| **Browser / client-side** | `Sentry.instrumentOpenAiClient(openaiInstance)` — manual wrapper |

### Server-Side Setup (`sentry.server.config.ts`)

`openAIIntegration` is **enabled by default** on the server. Pass it explicitly to customize options:

```typescript
// sentry.server.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,

  // Tracing MUST be enabled for AI monitoring
  tracesSampleRate: 1.0,

  integrations: [
    Sentry.openAIIntegration({
      recordInputs: true,   // capture prompts sent to OpenAI
      recordOutputs: true,  // capture completions from OpenAI
    }),
  ],
});
```

### Client-Side / Manual Wrapping

```typescript
import OpenAI from "openai";
import * as Sentry from "@sentry/nextjs";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY, // ⚠️ Never expose this in the browser!
});

// Wrap once at module level — reuse this client everywhere
const client = Sentry.instrumentOpenAiClient(openai, {
  recordInputs: true,
  recordOutputs: true,
});

const response = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello!" }],
});
```

### Streaming — Important

For streamed responses, you **must** pass `stream_options: { include_usage: true }`. Without this, OpenAI does not include token counts in streamed responses, so Sentry cannot capture usage metrics:

```typescript
const stream = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello!" }],
  stream: true,
  stream_options: { include_usage: true }, // ← REQUIRED for token tracking
});
```

### OpenAI Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `recordInputs` | `boolean` | `true` if `sendDefaultPii: true` | Capture prompts/messages sent to OpenAI |
| `recordOutputs` | `boolean` | `true` if `sendDefaultPii: true` | Capture generated text/responses |

**Supported versions:** `openai` ≥4.0.0 <7

---

## Vercel AI SDK Integration

### Setup

The integration is **auto-enabled** in the Node runtime. For the Edge runtime, add it explicitly:

```typescript
// sentry.server.config.ts — Node runtime (auto-enabled, customize here)
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  integrations: [
    Sentry.vercelAIIntegration({
      force: true, // ← Required for Vercel production deployments (see note below)
      recordInputs: true,
      recordOutputs: true,
    }),
  ],
});
```

```typescript
// sentry.edge.config.ts — Edge runtime requires manual opt-in
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  integrations: [
    Sentry.vercelAIIntegration(),
  ],
});
```

### Per-Call Telemetry (Required)

You **must** pass `experimental_telemetry: { isEnabled: true }` to every AI SDK function call you want traced:

```typescript
import { generateText, generateObject, streamText } from "ai";
import { openai } from "@ai-sdk/openai";

// generateText
const result = await generateText({
  model: openai("gpt-4o"),
  prompt: "What is the capital of France?",
  experimental_telemetry: {
    isEnabled: true,
    functionId: "my-text-generation",  // helps identify this function in traces
    recordInputs: true,
    recordOutputs: true,
  },
});

// generateObject
const { object } = await generateObject({
  model: openai("gpt-4o"),
  schema: z.object({ answer: z.string() }),
  prompt: "...",
  experimental_telemetry: { isEnabled: true, functionId: "my-object-gen" },
});

// streamText
const { textStream } = await streamText({
  model: openai("gpt-4o"),
  prompt: "...",
  experimental_telemetry: { isEnabled: true, functionId: "my-stream" },
});
```

### Vercel Production: `force: true`

When deployed to Vercel, the `ai` package gets bundled in Next.js production builds. This prevents automatic module detection, causing spans to use raw names (`ai.toolCall`, `ai.streamText`) instead of semantic names (`gen_ai.execute_tool`, `gen_ai.stream_text`).

**Fix — always use `force: true` in `sentry.server.config.ts` when deploying to Vercel:**
```typescript
Sentry.vercelAIIntegration({ force: true })
```

### Vercel AI SDK Configuration Options

| Option | Type | Default | Min SDK | Description |
|--------|------|---------|---------|-------------|
| `force` | `boolean` | `false` | 9.29.0 | Force-enable regardless of module detection. Use on Vercel. |
| `recordInputs` | `boolean` | `true`* | 9.27.0 | Capture inputs. *Defaults to `true` when `sendDefaultPii: true`. |
| `recordOutputs` | `boolean` | `true`* | 9.27.0 | Capture outputs. *Defaults to `true` when `sendDefaultPii: true`. |

**Supported versions:** `ai` ≥3.0.0 ≤6

---

## Anthropic Integration

### Server-Side Setup

```typescript
// sentry.server.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  integrations: [
    Sentry.anthropicAIIntegration({
      recordInputs: true,
      recordOutputs: true,
    }),
  ],
});
```

### Manual Wrapping

```typescript
import Anthropic from "@anthropic-ai/sdk";
import * as Sentry from "@sentry/nextjs";

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY, // ⚠️ Never expose in the browser!
});

const client = Sentry.instrumentAnthropicAiClient(anthropic, {
  recordInputs: true,
  recordOutputs: true,
});

const response = await client.messages.create({
  model: "claude-3-5-sonnet-20241022",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello, Claude!" }],
});
```

### Supported Anthropic Operations

| Operation | Method |
|-----------|--------|
| Create messages | `client.messages.create()` |
| Stream messages | `client.messages.stream()` |
| Count tokens | `client.messages.countTokens()` |
| Legacy completions | `client.completions.create()` |
| Beta messages | `client.beta.messages.create()` |

**Supported versions:** `@anthropic-ai/sdk` ≥0.19.2 <1.0.0

---

## Token Usage Tracking

Sentry automatically captures token usage following OpenTelemetry GenAI semantic conventions:

| Span Attribute | Description |
|----------------|-------------|
| `gen_ai.request.model` | Model name |
| `gen_ai.usage.input_tokens` | Prompt/input token count |
| `gen_ai.usage.output_tokens` | Completion/output token count |
| `gen_ai.usage.input_tokens.cached` | Cached input tokens |
| `gen_ai.usage.input_tokens.cache_write` | Cache write tokens |
| `gen_ai.usage.output_tokens.reasoning` | Reasoning tokens (e.g., o1 models) |

**Cost estimates** are sourced from models.dev and OpenRouter. Limitations: no volume discounts, no non-token charges, unrecognized models show no estimate.

---

## Prompt/Completion Capture & PII

`recordInputs` captures prompts sent to the AI API.  
`recordOutputs` captures the generated text/completions returned.

Both default to `true` only when `sendDefaultPii: true` is set:

```typescript
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  sendDefaultPii: true, // ← enables input/output recording by default
  tracesSampleRate: 1.0,
});
```

Or enable explicitly without `sendDefaultPii`:

```typescript
integrations: [
  Sentry.openAIIntegration({
    recordInputs: true,   // explicitly opt in
    recordOutputs: true,
  }),
],
```

> ⚠️ **PII warning:** Prompts often contain user-supplied text. If users include personal data in prompts, enabling `recordInputs` will send that data to Sentry. Review your privacy policy before enabling.

---

## Complete Setup Example

```typescript
// sentry.server.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  integrations: [
    Sentry.openAIIntegration({ recordInputs: true, recordOutputs: true }),
    Sentry.vercelAIIntegration({ force: true, recordInputs: true, recordOutputs: true }),
    Sentry.anthropicAIIntegration({ recordInputs: true, recordOutputs: true }),
  ],
});
```

```typescript
// app/api/chat/route.ts — OpenAI with streaming
import OpenAI from "openai";
import * as Sentry from "@sentry/nextjs";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const sentryOpenAI = Sentry.instrumentOpenAiClient(openai);

export async function POST(req: Request) {
  const { messages } = await req.json();

  const completion = await sentryOpenAI.chat.completions.create({
    model: "gpt-4o",
    messages,
    stream: true,
    stream_options: { include_usage: true }, // ← Required for token tracking
  });

  // ... stream response to client
}
```

```typescript
// app/api/generate/route.ts — Vercel AI SDK
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const result = await generateText({
    model: openai("gpt-4o"),
    prompt,
    experimental_telemetry: {
      isEnabled: true,            // ← Required for Sentry to capture spans
      functionId: "chat-handler",
      recordInputs: true,
      recordOutputs: true,
    },
  });

  return Response.json({ text: result.text });
}
```

---

## AI Agents Dashboard

Access at **Sentry → AI → Agents** (or **Insights → AI**).

| Tab | What you see |
|-----|-------------|
| **Overview** | Agent runs, error rates, duration, LLM calls, tokens used, tool calls |
| **Models** | Per-model cost estimates, token breakdown (input/output/cached), duration |
| **Tools** | Per-tool call counts, error rates, input/output for each invocation |
| **Traces** | Full pipeline from user request to final response with all spans |

---

## SDK Version Matrix

| Feature | Min SDK Version |
|---------|----------------|
| Vercel AI SDK integration (Node/CF/Edge/Bun) | **10.6.0** |
| Vercel AI SDK integration (Deno) | **10.12.0** |
| Vercel AI `recordInputs`/`recordOutputs` | 9.27.0 |
| Vercel AI `force` option | 9.29.0 |
| OpenAI integration (`openAIIntegration` / `instrumentOpenAiClient`) | **10.28.0** |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No AI spans appearing | Verify `tracesSampleRate` > 0; AI monitoring requires tracing |
| Token counts missing in streams | Add `stream_options: { include_usage: true }` to all OpenAI streaming calls |
| Vercel AI spans show raw names (`ai.toolCall`) | Add `vercelAIIntegration({ force: true })` in server config |
| `recordInputs`/`recordOutputs` not capturing | Set `sendDefaultPii: true` or explicitly pass `recordInputs: true` to the integration |
| Anthropic spans missing | Check SDK version supports Anthropic integration; add `anthropicAIIntegration()` explicitly |
| Cost estimates not showing | Model name must match models.dev/OpenRouter pricing data; custom/fine-tuned models may show no estimate |
| Edge runtime AI spans missing | Add `vercelAIIntegration()` to `sentry.edge.config.ts` explicitly (not auto-enabled for Edge) |
| OpenAI browser-side spans missing | Use `instrumentOpenAiClient()` wrapper — `openAIIntegration()` only works server-side |
| No data in AI Agents dashboard | Ensure traces are being sent; check DSN and `tracesSampleRate` |

---

## Reference: Crons

# Crons — Sentry Next.js SDK

> Minimum SDK: `@sentry/nextjs` ≥7.51.1+ for `captureCheckIn`  
> `Sentry.withMonitor()`: ≥7.76.0+  
> Cron library auto-instrumentation: ≥7.92.0+

> ⚠️ **Server and Edge runtimes only.** Cron monitoring is not available in the browser runtime.

---

## Overview

Sentry Cron Monitoring detects:
- **Missed check-ins** — job didn't run at the expected time
- **Runtime failures** — job ran but encountered an error
- **Timeouts** — job exceeded `maxRuntime` without completing

---

## Option A: Automatic Vercel Cron Integration

For **Vercel-hosted Next.js** apps using Vercel Cron Jobs:

```javascript
// next.config.js
const { withSentryConfig } = require("@sentry/nextjs");

module.exports = withSentryConfig(nextConfig, {
  automaticVercelMonitors: true,
});
```

> ⚠️ **Critical limitation:** `automaticVercelMonitors` only works with the **Pages Router**. **App Router route handlers are NOT yet supported** for automatic instrumentation. Use `captureCheckIn` or `withMonitor` manually for App Router cron routes.

---

## Option B: Auto-Instrumentation of Cron Libraries (SDK ≥7.92.0)

### `cron` npm package

```typescript
import { CronJob } from "cron";
import * as Sentry from "@sentry/nextjs";

const CronJobWithCheckIn = Sentry.cron.instrumentCron(CronJob, "my-cron-job");

const job = new CronJobWithCheckIn("* * * * *", () => {
  console.log("Runs every minute");
});

// Or via .from() factory:
const job2 = CronJobWithCheckIn.from({
  cronTime: "* * * * *",
  onTick: () => console.log("Runs every minute"),
});
```

### `node-cron` npm package

```typescript
import cron from "node-cron";
import * as Sentry from "@sentry/nextjs";

const cronWithCheckIn = Sentry.cron.instrumentNodeCron(cron);

cronWithCheckIn.schedule(
  "* * * * *",
  () => {
    console.log("Running every minute");
  },
  { name: "my-cron-job" }, // ← name is required for Sentry monitoring
);
```

### `node-schedule` npm package (SDK ≥7.93.0)

```typescript
import * as schedule from "node-schedule";
import * as Sentry from "@sentry/nextjs";

const scheduleWithCheckIn = Sentry.cron.instrumentNodeSchedule(schedule);

scheduleWithCheckIn.scheduleJob(
  "my-cron-job",   // ← first arg is the monitor slug
  "* * * * *",
  () => {
    console.log("Running every minute");
  },
);
```

> ⚠️ `node-schedule` instrumentation only supports **cron string format**. Date objects and RecurrenceRule objects are not supported.

---

## Option C: `Sentry.withMonitor()` Wrapper (SDK ≥7.76.0)

Wraps any callback and automatically sends `in_progress` → `ok`/`error` check-ins:

```typescript
import * as Sentry from "@sentry/nextjs";

// Basic usage — monitor must already exist in Sentry
await Sentry.withMonitor("my-monitor-slug", async () => {
  await processQueue();
});
```

### With Full Monitor Configuration (Upsert)

```typescript
await Sentry.withMonitor(
  "hourly-report-job",
  async () => {
    await generateHourlyReport();
  },
  {
    schedule: {
      type: "crontab",
      value: "0 * * * *",   // runs at top of every hour
    },
    checkinMargin: 2,        // minutes of grace before "missed"
    maxRuntime: 10,          // minutes before marking as failed
    timezone: "America/Los_Angeles",
    failureIssueThreshold: 3,   // consecutive failures before creating issue (SDK ≥8.7.0)
    recoveryThreshold: 2,        // consecutive successes before resolving issue (SDK ≥8.7.0)
  },
);
```

### Interval Schedule

```typescript
await Sentry.withMonitor(
  "data-sync-job",
  async () => {
    await syncData();
  },
  {
    schedule: {
      type: "interval",
      value: 30,         // numeric value
      unit: "minute",    // "minute" | "hour" | "day" | "week" | "month" | "year"
    },
  },
);
```

---

## Option D: Manual `Sentry.captureCheckIn()` (SDK ≥7.51.1)

For full control — send check-ins manually at job start and end:

```typescript
import * as Sentry from "@sentry/nextjs";

// 1. Signal job started — returns a checkInId for correlation
const checkInId = Sentry.captureCheckIn({
  monitorSlug: "my-monitor-slug",
  status: "in_progress",
});

try {
  await doWork();

  // 2a. Signal success
  Sentry.captureCheckIn({
    checkInId,
    monitorSlug: "my-monitor-slug",
    status: "ok",
  });
} catch (err) {
  // 2b. Signal failure
  Sentry.captureCheckIn({
    checkInId,
    monitorSlug: "my-monitor-slug",
    status: "error",
  });
  throw err;
}
```

### With Upsert Config

```typescript
const checkInId = Sentry.captureCheckIn(
  {
    monitorSlug: "my-monitor-slug",
    status: "in_progress",
  },
  {
    schedule: {
      type: "crontab",
      value: "*/5 * * * *",  // every 5 minutes
    },
    checkinMargin: 1,
    maxRuntime: 5,
    timezone: "UTC",
  },
);
```

### Heartbeat Check-In (Detects Missed Jobs Only)

If you only need to know whether the job ran (not runtime failures), send a single check-in at completion:

```typescript
try {
  await doWork();
  Sentry.captureCheckIn({ monitorSlug: "my-monitor-slug", status: "ok" });
} catch (err) {
  Sentry.captureCheckIn({ monitorSlug: "my-monitor-slug", status: "error" });
}
```

---

## Using Crons with Next.js Route Handlers

For App Router cron endpoints called by Vercel Cron or an external scheduler:

```typescript
// app/api/cron/route.ts
import * as Sentry from "@sentry/nextjs";
import { NextResponse } from "next/server";

export async function GET() {
  const checkInId = Sentry.captureCheckIn({
    monitorSlug: "my-api-cron",
    status: "in_progress",
  });

  try {
    await runMyScheduledTask();

    Sentry.captureCheckIn({
      checkInId,
      monitorSlug: "my-api-cron",
      status: "ok",
    });

    return NextResponse.json({ ok: true });
  } catch (err) {
    Sentry.captureCheckIn({
      checkInId,
      monitorSlug: "my-api-cron",
      status: "error",
    });
    throw err;
  }
}
```

### Using `withMonitor` in a Route Handler

```typescript
// app/api/cron/route.ts
import * as Sentry from "@sentry/nextjs";
import { NextResponse } from "next/server";

export async function GET() {
  await Sentry.withMonitor(
    "my-api-cron",
    async () => {
      await runMyScheduledTask();
    },
    {
      schedule: { type: "crontab", value: "0 * * * *" },
      checkinMargin: 2,
      maxRuntime: 5,
      timezone: "UTC",
    },
  );

  return NextResponse.json({ ok: true });
}
```

### Edge Runtime Route Handler

```typescript
// app/api/cron/route.ts
export const runtime = "edge";

import * as Sentry from "@sentry/nextjs";
import { NextResponse } from "next/server";

export async function GET() {
  await Sentry.withMonitor("my-edge-cron", async () => {
    await runEdgeTask();
  });

  return NextResponse.json({ ok: true });
}
```

---

## Monitor Configuration Reference

Full upsert config object shape:

```typescript
interface MonitorConfig {
  schedule: {
    type: "crontab";
    value: string;       // Standard cron expression, e.g. "0 9 * * 1-5"
  } | {
    type: "interval";
    value: number;       // Numeric quantity
    unit: "minute" | "hour" | "day" | "week" | "month" | "year";
  };
  checkinMargin?: number;          // Minutes of grace period before "missed" alert
  maxRuntime?: number;             // Minutes before in-progress job is marked failed
  timezone?: string;               // IANA tz string, e.g. "America/New_York"
  failureIssueThreshold?: number;  // Consecutive failures → create issue (SDK ≥8.7.0)
  recoveryThreshold?: number;      // Consecutive successes → resolve issue (SDK ≥8.7.0)
}
```

---

## Cron Status Values

| Status | When to use |
|--------|------------|
| `in_progress` | Job has started, work is underway |
| `ok` | Job completed successfully |
| `error` | Job failed — an error occurred |

---

## Rate Limits

Cron check-ins are rate-limited to **6 check-ins per minute per monitor environment**. Each environment (production, staging, etc.) is tracked independently.

---

## Alerting

Create issue alerts filtered by the tag **`monitor.slug`** equals `[your-monitor-slug]` in Sentry's Alerts sidebar.

---

## SDK Version Matrix

| Feature | Min SDK Version |
|---------|----------------|
| `Sentry.captureCheckIn()` | **7.51.1** |
| `Sentry.withMonitor()` | **7.76.0** |
| `cron` library auto-instrumentation | **7.92.0** |
| `node-cron` auto-instrumentation | **7.92.0** |
| `node-schedule` auto-instrumentation | **7.93.0** |
| `failureIssueThreshold` / `recoveryThreshold` | **8.7.0** |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Check-ins not appearing in Sentry | Verify `monitorSlug` matches the slug configured in Sentry; check DSN is correct |
| Monitor shows "missed" despite job running | Adjust `checkinMargin` to allow more grace time; check clock skew |
| Monitor shows "timeout" | Increase `maxRuntime`; investigate why the job is taking longer than expected |
| `automaticVercelMonitors` not working | Confirm you're using Pages Router — App Router is NOT supported for automatic instrumentation |
| `withMonitor` not creating the monitor | First check-in with upsert config creates the monitor; ensure config is passed |
| Edge runtime check-ins failing | Ensure `sentry.edge.config.ts` is configured; crons work in Edge runtime |
| Client-side cron calls failing | Move cron monitoring to server/edge code — browser runtime is not supported |
| Rate limit errors on check-ins | Job is sending more than 6 check-ins/minute; reduce polling frequency or combine check-ins |
| `node-schedule` with date/RecurrenceRule | Only cron string format is supported for auto-instrumentation; use `withMonitor` instead |

---

## Reference: Error Monitoring

# Error Monitoring — Sentry Next.js SDK

> Minimum SDK: `@sentry/nextjs` ≥8.0.0  
> `onRequestError` hook requires `@sentry/nextjs` ≥8.28.0 and Next.js 15+  
> `withServerActionInstrumentation` available since `@sentry/nextjs` ≥8.0.0

---

## Three-Runtime Architecture

Next.js runs code in three separate environments. Sentry provides **distinct init files** for each:

| File | Runtime | Captures |
|------|---------|---------|
| `instrumentation-client.ts` | Browser | Client-side errors, unhandled rejections |
| `sentry.server.config.ts` | Node.js | API routes, Server Components, Server Actions |
| `sentry.edge.config.ts` | Edge | Middleware, edge routes |

All three use the same DSN but are configured independently.

---

## Automatic vs Manual Error Capture

### What Is Captured Automatically

| Error Type | Captured? | Mechanism |
|-----------|-----------|-----------|
| Unhandled client JS exceptions | ✅ Yes | `window.onerror` (GlobalHandlers integration) |
| Unhandled promise rejections (client) | ✅ Yes | `window.onunhandledrejection` |
| Server Component render errors (Next.js 15+) | ✅ Yes | `onRequestError` hook in `instrumentation.ts` |
| Unhandled API route crashes (server) | ✅ Yes | Node.js uncaught exception handler |
| Re-thrown errors from `try/catch` | ✅ Yes | Bubbles to global handler |
| `error.tsx` boundary errors | ❌ No | Next.js catches before Sentry |
| `global-error.tsx` boundary errors | ❌ No | Next.js catches before Sentry |
| Caught + swallowed `try/catch` errors | ❌ No | Must call `captureException` manually |
| Server Action graceful error returns | ❌ No | Must call `captureException` or use wrapper |
| Caught edge middleware errors | ❌ No | Must call `captureException` manually |

### The Core Rule

> **"If you catch an error and don't re-throw it, Sentry never sees it."**

```typescript
// ✅ Automatically captured — unhandled, bubbles up
throw new Error("Unhandled");

// ✅ Automatically captured — re-thrown
try {
  await doSomething();
} catch (err) {
  throw err;
}

// ❌ NOT captured — swallowed by graceful return
try {
  await doSomething();
} catch (err) {
  return { error: "Failed" }; // ← must add captureException here
}

// ✅ Manually captured
try {
  await doSomething();
} catch (err) {
  Sentry.captureException(err);
  return { error: "Failed" };
}
```

---

## Client-Side Error Capture

### `Sentry.captureException(error, context?)`

Captures an exception and sends it to Sentry. Prefer `Error` objects — they include stack traces.

```typescript
// Basic
Sentry.captureException(new Error("Something broke"));

// With inline context (one-off enrichment)
Sentry.captureException(error, {
  level: "fatal",
  tags: { section: "checkout" },
  extra: { orderId, userId: user.id },
  user: { id: "user-123", email: "user@example.com" },
  fingerprint: ["checkout-failure", String(error.code)],
  contexts: {
    cart: { items: 3, total: 99.99 },
  },
});
```

### `Sentry.captureMessage(message, levelOrContext?)`

Captures a plain message — useful for notable conditions that aren't exceptions.

```typescript
// With severity level
Sentry.captureMessage("Deprecated API used", "warning");
// Levels: "fatal" | "error" | "warning" | "log" | "info" | "debug"

// With full context
Sentry.captureMessage("Payment method expired", {
  level: "warning",
  tags: { payment_provider: "stripe" },
  user: { id: currentUser.id },
});
```

### Unhandled Rejections

Automatically captured by the `GlobalHandlers` integration. To customize:

```typescript
// instrumentation-client.ts
Sentry.init({
  dsn: "___PUBLIC_DSN___",
  integrations: [
    Sentry.globalHandlersIntegration({
      onerror: true,
      onunhandledrejection: true, // set false to handle manually
    }),
  ],
});

// Manual rejection handling (if onunhandledrejection: false)
window.addEventListener("unhandledrejection", (event) => {
  Sentry.captureException(event.reason);
});
```

---

## Error Boundaries

### App Router: `app/error.tsx` (Segment-level)

Each route segment can have its own `error.tsx`. Next.js catches these before Sentry — you **must** call `captureException` manually inside `useEffect`.

```tsx
// app/error.tsx  (also: app/dashboard/error.tsx, etc.)
"use client";

import { useEffect } from "react";
import * as Sentry from "@sentry/nextjs";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // REQUIRED: Next.js catches this before Sentry can
    Sentry.captureException(error);
  }, [error]);

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

> **`digest`:** Server-side errors include a `digest` hash. Use it to correlate Sentry events with server logs.

### App Router: `app/global-error.tsx` (Root Layout)

Last-resort catch-all for root layout errors. Must render its own `<html>` and `<body>`. Use the `NextError` component for consistency with Next.js default error pages.

```tsx
// app/global-error.tsx
"use client";

import * as Sentry from "@sentry/nextjs";
import NextError from "next/error";
import { useEffect } from "react";

export default function GlobalError({
  error,
}: {
  error: Error & { digest?: string };
}) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <html>
      <body>
        {/*
          App Router doesn't expose HTTP status codes for errors,
          so pass 0 to render a generic error message.
        */}
        <NextError statusCode={0} />
      </body>
    </html>
  );
}
```

### App Router: Error Boundary Directory Structure

```
app/
├── global-error.tsx        # Root layout errors (last resort)
├── error.tsx               # App-wide segment fallback
├── layout.tsx
├── page.tsx
└── dashboard/
    ├── error.tsx           # Dashboard-specific error boundary
    ├── layout.tsx
    └── page.tsx
```

### React 18 and Earlier: `<Sentry.ErrorBoundary>`

For client components using React 18 or earlier, wrap with `<Sentry.ErrorBoundary>` for additional control and fallback UIs:

```tsx
"use client";

import * as Sentry from "@sentry/nextjs";

function CheckoutPage() {
  return (
    <Sentry.ErrorBoundary
      fallback={({ error, resetError }) => (
        <div>
          <p>Checkout failed: {error.message}</p>
          <button onClick={resetError}>Retry</button>
        </div>
      )}
      beforeCapture={(scope, error) => {
        scope.setTag("section", "checkout");
        scope.setLevel("fatal");
      }}
      onError={(error, componentStack, eventId) => {
        analytics.track("error_boundary", { eventId });
      }}
    >
      <CheckoutFlow />
    </Sentry.ErrorBoundary>
  );
}
```

### React 19+: `Sentry.reactErrorHandler()` with `createRoot`

React 19 exposes hooks on `createRoot`. If you're using React 19 client components, pass `Sentry.reactErrorHandler()` to each hook:

```tsx
// In your client entry point or root layout setup
import { createRoot } from "react-dom/client";
import * as Sentry from "@sentry/nextjs";

createRoot(container, {
  onUncaughtError: Sentry.reactErrorHandler(),    // fatal — tree unmounts
  onCaughtError: Sentry.reactErrorHandler(),      // caught by an ErrorBoundary
  onRecoverableError: Sentry.reactErrorHandler(), // auto-recovery (hydration)
}).render(<App />);
```

> **Use both together:** `reactErrorHandler()` is the global net; `<Sentry.ErrorBoundary>` provides scoped fallback UIs.

---

## Pages Router Error Handling

### `pages/_error.tsx`

Use `captureUnderscoreErrorException` — a helper that reads Next.js context and captures the error with correct status code.

```tsx
// pages/_error.tsx
import * as Sentry from "@sentry/nextjs";
import type { NextPage } from "next";
import type { ErrorProps } from "next/error";
import Error from "next/error";

const CustomErrorComponent: NextPage<ErrorProps> = (props) => {
  return <Error statusCode={props.statusCode} />;
};

CustomErrorComponent.getInitialProps = async (contextData) => {
  // CRITICAL: await so Sentry flushes before the serverless function exits
  await Sentry.captureUnderscoreErrorException(contextData);
  return Error.getInitialProps(contextData);
};

export default CustomErrorComponent;
```

### `pages/_app.tsx`

For global error handling at the app level in Pages Router:

```tsx
// pages/_app.tsx
import type { AppProps } from "next/app";
import * as Sentry from "@sentry/nextjs";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Sentry.ErrorBoundary fallback={<p>An error has occurred.</p>}>
      <Component {...pageProps} />
    </Sentry.ErrorBoundary>
  );
}
```

---

## Server-Side Error Capture

### `onRequestError` Hook (Next.js 15+, SDK ≥8.28.0)

Export `onRequestError` from `instrumentation.ts` to automatically capture Server Component errors without adding `captureException` everywhere:

```typescript
// instrumentation.ts
import * as Sentry from "@sentry/nextjs";

export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    await import("./sentry.server.config");
  }
  if (process.env.NEXT_RUNTIME === "edge") {
    await import("./sentry.edge.config");
  }
}

// Automatically captures errors from Server Components, Middleware, and proxies
export const onRequestError = Sentry.captureRequestError;
```

### API Routes (App Router)

Unhandled errors crash the request and are auto-captured. Caught errors must be captured manually:

```typescript
// app/api/users/route.ts
import { NextResponse } from "next/server";
import * as Sentry from "@sentry/nextjs";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const user = await db.users.create(body);
    return NextResponse.json(user, { status: 201 });
  } catch (error) {
    Sentry.captureException(error, {
      tags: { route: "/api/users", method: "POST" },
    });
    return NextResponse.json({ error: "Failed to create user" }, { status: 500 });
  }
}
```

### API Routes (Pages Router)

```typescript
// pages/api/users.ts
import type { NextApiRequest, NextApiResponse } from "next";
import * as Sentry from "@sentry/nextjs";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const data = await fetchData();
    res.status(200).json(data);
  } catch (error) {
    Sentry.captureException(error);
    res.status(500).json({ error: "Internal server error" });
  }
}
```

### Server Actions

#### Manual Pattern

```typescript
// app/actions.ts
"use server";

import * as Sentry from "@sentry/nextjs";

export async function createPost(formData: FormData) {
  try {
    const post = await db.posts.create({
      data: { title: formData.get("title") as string },
    });
    return { success: true, id: post.id };
  } catch (error) {
    // Graceful return swallows — must capture manually
    Sentry.captureException(error);
    return { success: false, error: "Failed to create post" };
  }
}
```

#### `withServerActionInstrumentation` (Recommended)

Automatically instruments server actions with tracing, attaches form data, and connects client/server traces:

```typescript
// app/actions.ts
"use server";

import * as Sentry from "@sentry/nextjs";
import { headers } from "next/headers";

export async function submitForm(formData: FormData) {
  return Sentry.withServerActionInstrumentation(
    "submitForm",
    {
      headers: await headers(), // connects client and server traces
      formData,                 // attaches form data to Sentry events
      recordResponse: true,     // includes response data
    },
    async () => {
      // Errors thrown here are automatically captured
      const result = await processForm(formData);
      return { success: true, data: result };
    },
  );
}
```

---

## Edge Runtime Error Capture

Edge runtime runs in Next.js middleware and edge API routes. Initialize Sentry via `sentry.edge.config.ts`:

```typescript
// sentry.edge.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: "___PUBLIC_DSN___",
  tracesSampleRate: 1.0,
  // Note: Edge runtime has limited Node.js API access
  // Some Node.js-specific integrations are not available
});
```

Errors in middleware are auto-captured via `onRequestError`. Caught errors require manual capture:

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import * as Sentry from "@sentry/nextjs";

export function middleware(request: NextRequest) {
  try {
    // middleware logic
    return NextResponse.next();
  } catch (error) {
    Sentry.captureException(error, {
      tags: { runtime: "edge", path: request.nextUrl.pathname },
    });
    return NextResponse.next();
  }
}

export const config = {
  // Exclude tunnel route from middleware if using tunnelRoute in withSentryConfig
  matcher: ["/((?!monitoring|_next/static|_next/image|favicon.ico).*)"],
};
```

---

## Scope Management

Sentry merges three scope layers before sending each event. Later scopes override earlier ones:

```
Global → Isolation → Current → Event Sent
```

### Global Scope

Applied to every event. Use for universal data (app version, build ID):

```typescript
Sentry.getGlobalScope().setTag("app_version", "2.1.0");
Sentry.getGlobalScope().setContext("build", { sha: process.env.VERCEL_GIT_COMMIT_SHA });
```

### Isolation Scope

- **Server:** Forked per request — safe for per-request user data (no cross-contamination)
- **Browser:** One per page load

All top-level `Sentry.setXxx()` methods write to the isolation scope:

```typescript
// These are identical:
Sentry.setTag("my-tag", "my value");
Sentry.getIsolationScope().setTag("my-tag", "my value");

// Set user on login (persists for the current request/page):
Sentry.setUser({ id: "user-42", email: "user@example.com" });

// Clear user on logout:
Sentry.setUser(null);
```

### `withScope` — Temporary Per-Capture Context

The primary tool for adding context to a single capture without affecting other events:

```typescript
Sentry.withScope((scope) => {
  scope.setTag("operation", "bulk-delete");
  scope.setLevel("warning");
  scope.setUser({ id: order.userId });
  scope.setContext("bulk", { count: items.length });
  scope.addBreadcrumb({
    category: "operation",
    message: "Bulk delete started",
    level: "info",
  });
  Sentry.captureException(deleteError);
});
// Tags/context above do NOT appear on subsequent events
```

### Scope Decision Guide

| Goal | API |
|------|-----|
| Data on ALL events (app version, build ID) | `Sentry.getGlobalScope().setTag(...)` |
| Current request/page-load data | `Sentry.setTag(...)` (isolation scope) |
| One specific capture only | `Sentry.withScope((scope) => { ... })` |
| Inline on a single event | Second arg to `captureException(err, { tags: {...} })` |

---

## Event Enrichment

### `setTag` / `setTags` (Searchable)

Tags are **indexed and searchable** — use them for filtering, grouping, and alerting.

- Key: max 32 chars, `a-zA-Z0-9_.:- ` (no spaces); Value: max 200 chars, no newlines

```typescript
Sentry.setTag("page_locale", "de-at");
Sentry.setTags({
  payment_method: "stripe",
  subscription_tier: "pro",
  region: "eu-west-1",
});
```

### `setContext` (Structured, Non-searchable)

Attaches arbitrary structured data visible in the issue detail view. Not indexed or searchable.

```typescript
Sentry.setContext("checkout", {
  step: "payment",
  cart_items: 3,
  total_usd: 99.99,
  coupon_applied: "SAVE20",
});

// Clear a context:
Sentry.setContext("checkout", null);
```

> **Depth:** Normalized to 3 levels deep by default. The `type` key is reserved — don't use it.

### `setUser` (User Identity)

```typescript
// On login
Sentry.setUser({
  id: "user-42",
  email: "jane@example.com",
  username: "janedoe",
  subscription: "pro",  // arbitrary extra fields accepted
});

// On logout
Sentry.setUser(null);
```

### `setExtra` / `setExtras` (Arbitrary Debug Data)

Non-indexed supplementary data. Prefer `setContext` for structured objects with meaningful names.

```typescript
Sentry.setExtra("raw_api_response", responseText);
Sentry.setExtras({
  formData: { fieldA: "value1" },
  processingStep: "validation",
  retryCount: 3,
});
```

### Tags vs Context vs Extra

| Feature | Searchable? | Indexed? | Best For |
|---------|------------|---------|---------|
| **Tags** | ✅ Yes | ✅ Yes | Filtering, grouping, alerting |
| **Context** | ❌ No | ❌ No | Structured debug info (nested objects) |
| **Extra** | ❌ No | ❌ No | Arbitrary debug values |
| **User** | ✅ Partially | ✅ Yes | User attribution and filtering |

---

## Breadcrumbs

### Automatic Breadcrumbs (Zero Config)

| Type | What's Captured |
|------|----------------|
| `ui.click` | DOM element clicks |
| `navigation` | URL changes, route transitions |
| `http` | XHR/fetch requests (URL, method, status) |
| `console` | `console.log`, `warn`, `error` |

### Manual Breadcrumbs

```typescript
Sentry.addBreadcrumb({
  category: "auth",
  message: "User authenticated",
  level: "info",
  data: { userId: "u_42", method: "oauth2" },
});

Sentry.addBreadcrumb({
  type: "http",
  category: "api.request",
  message: "POST /api/orders",
  level: "info",
  data: {
    url: "/api/orders",
    method: "POST",
    status_code: 422,
    reason: "Validation failed",
  },
});

Sentry.addBreadcrumb({
  type: "navigation",
  category: "navigation",
  message: "User navigated to checkout",
  data: { from: "/cart", to: "/checkout/payment" },
});
```

### Breadcrumb Properties

| Key | Type | Values |
|-----|------|--------|
| `type` | string | `"default"` \| `"debug"` \| `"error"` \| `"info"` \| `"navigation"` \| `"http"` \| `"query"` \| `"ui"` \| `"user"` |
| `category` | string | Dot-notation: `"auth"`, `"ui.click"`, `"api.request"` |
| `message` | string | Human-readable description |
| `level` | string | `"fatal"` \| `"error"` \| `"warning"` \| `"log"` \| `"info"` \| `"debug"` |
| `timestamp` | number | Unix timestamp (auto-set if omitted) |
| `data` | object | Arbitrary key/value data |

### `beforeBreadcrumb` — Filter or Mutate

```typescript
Sentry.init({
  beforeBreadcrumb(breadcrumb, hint) {
    // Drop password field interactions
    if (breadcrumb.category === "ui.click") {
      if (hint?.event?.target?.type === "password") return null;
    }

    // Drop verbose console.debug in production
    if (breadcrumb.category === "console" && breadcrumb.level === "debug") {
      return null;
    }

    // Enrich fetch breadcrumbs
    if (breadcrumb.category === "fetch" && hint?.response) {
      breadcrumb.data = {
        ...breadcrumb.data,
        responseStatus: hint.response.status,
      };
    }

    return breadcrumb;
  },
  maxBreadcrumbs: 50, // default: 100
});
```

---

## `beforeSend` and Filtering Hooks

### `beforeSend` — Modify or Drop Error Events

Last chance to modify or discard events. Runs after all event processors. Return `null` to drop.

```typescript
Sentry.init({
  beforeSend(event, hint) {
    const error = hint.originalException;

    // Drop non-Error rejections (e.g. cancelled requests)
    if (error && !(error instanceof Error)) return null;

    // Drop browser extension errors
    const frames = event.exception?.values?.[0]?.stacktrace?.frames;
    if (frames?.some(f => f.filename?.includes("extension://"))) return null;

    // Scrub PII
    if (event.user?.email) {
      event.user = { ...event.user, email: "[filtered]" };
    }

    // Override fingerprint for known patterns
    if (error?.name === "ChunkLoadError") {
      event.fingerprint = ["chunk-load-failure"];
    }

    return event;
  },
});
```

> **Note:** Only one `beforeSend` is allowed. For multiple processors, use `addEventProcessor()`.

### `beforeSendTransaction` — Modify or Drop Performance Events

```typescript
Sentry.init({
  beforeSendTransaction(event) {
    if (event.transaction === "/api/health") return null;
    return event;
  },
});
```

### `ignoreErrors` — Pattern-Based Filtering

```typescript
Sentry.init({
  ignoreErrors: [
    "ResizeObserver loop limit exceeded",
    "fb_xd_fragment",
    /^Network Error$/i,
    /Loading chunk \d+ failed/,
    /^Script error\.?$/,
  ],
});
```

### `allowUrls` / `denyUrls`

```typescript
Sentry.init({
  // Only capture errors from your own scripts:
  allowUrls: [/https?:\/\/((cdn|www)\.)?yourapp\.com/],

  // Block third-party noise:
  denyUrls: [
    /extensions\//i,
    /^chrome:\/\//i,
    /^moz-extension:\/\//i,
    /gtm\.js/,
  ],
});
```

---

## Fingerprinting and Custom Grouping

All events have a **fingerprint**. Events with the same fingerprint group into the same issue.

### Per-Event Fingerprinting

```typescript
Sentry.captureException(error, {
  fingerprint: ["checkout-failure", "stripe", String(error.code)],
});
```

### `withScope` Fingerprinting

```typescript
Sentry.withScope((scope) => {
  scope.setFingerprint([method, path, String(err.statusCode)]);
  Sentry.captureException(err);
});
```

### `beforeSend` Fingerprinting

```typescript
Sentry.init({
  beforeSend(event, hint) {
    const error = hint.originalException;

    // All DatabaseConnectionErrors → one issue:
    if (error instanceof DatabaseConnectionError) {
      event.fingerprint = ["database-connection-error"];
    }

    // Extend default grouping (keep Sentry's stack-trace hash + add dimension):
    if (error instanceof RPCError) {
      event.fingerprint = [
        "{{ default }}",              // keep Sentry's default
        String(error.functionName),   // + split by RPC function
        String(error.errorCode),
      ];
    }

    return event;
  },
});
```

### Template Variables

| Variable | Description |
|----------|-------------|
| `{{ default }}` | Sentry's normally computed hash (extend rather than replace) |
| `{{ transaction }}` | Current transaction name |
| `{{ function }}` | Top function in stack trace |
| `{{ type }}` | Exception type |

---

## Event Processors

Unlike `beforeSend` (only one allowed), you can register multiple event processors:

```typescript
// Global — runs for all events
Sentry.addEventProcessor((event, hint) => {
  event.extra = {
    ...event.extra,
    buildId: process.env.VERCEL_GIT_COMMIT_SHA,
  };
  return event;
});

// Scoped — runs only inside the withScope callback
Sentry.withScope((scope) => {
  scope.addEventProcessor((event) => {
    event.tags = { ...event.tags, processed_by: "checkout_handler" };
    return event;
  });
  Sentry.captureException(checkoutError);
});
```

**Execution order:** All `addEventProcessor()` processors run first, then `beforeSend` runs last (guaranteed).

---

## Error Capture Quick Reference

### Scenario Coverage Table

| Scenario | Auto Captured? | Solution |
|----------|---------------|---------|
| Unhandled client JS exception | ✅ Yes | — |
| Unhandled promise rejection | ✅ Yes | — |
| Server Component error (Next.js 15+) | ✅ Yes | `onRequestError` hook |
| Unhandled API route crash | ✅ Yes | — |
| `app/error.tsx` boundary | ❌ No | `captureException` in `useEffect` |
| `app/global-error.tsx` | ❌ No | `captureException` in `useEffect` |
| `try/catch` with graceful return | ❌ No | `captureException` before return |
| `try/catch` with re-throw | ✅ Yes | — |
| Server Action graceful error | ❌ No | `captureException` or `withServerActionInstrumentation` |
| Caught edge middleware error | ❌ No | `captureException` manually |

### API Quick Reference

```typescript
// ── Capture ───────────────────────────────────────────────────────────
Sentry.captureException(error)
Sentry.captureException(error, { level, tags, extra, contexts, fingerprint, user })
Sentry.captureMessage("text", "warning")
Sentry.captureMessage("text", { level, tags, extra })

// ── Next.js Specific ──────────────────────────────────────────────────
export const onRequestError = Sentry.captureRequestError      // instrumentation.ts
await Sentry.captureUnderscoreErrorException(contextData)     // pages/_error.tsx
Sentry.withServerActionInstrumentation("name", opts, fn)      // server actions

// ── User ──────────────────────────────────────────────────────────────
Sentry.setUser({ id, email, username, ...custom })
Sentry.setUser(null)                                          // clear on logout

// ── Tags (searchable) ─────────────────────────────────────────────────
Sentry.setTag("key", "value")
Sentry.setTags({ key1: "v1", key2: "v2" })

// ── Context (structured, non-searchable) ──────────────────────────────
Sentry.setContext("name", { key: value })
Sentry.setContext("name", null)                               // clear

// ── Extra (arbitrary) ─────────────────────────────────────────────────
Sentry.setExtra("key", anyValue)
Sentry.setExtras({ key1: v1 })

// ── Breadcrumbs ───────────────────────────────────────────────────────
Sentry.addBreadcrumb({ type, category, message, level, data })

// ── Scopes ────────────────────────────────────────────────────────────
Sentry.withScope((scope) => { scope.setTag(...); Sentry.captureException(...) })
Sentry.withIsolationScope((scope) => { ... })
Sentry.getGlobalScope().setTag(...)
Sentry.getIsolationScope().setTag(...)                        // same as Sentry.setTag()

// ── Fingerprinting ────────────────────────────────────────────────────
scope.setFingerprint(["group-key"])
event.fingerprint = ["{{ default }}", "extra-dimension"]      // in beforeSend

// ── Hooks ─────────────────────────────────────────────────────────────
Sentry.init({ beforeSend(event, hint) { return event | null } })
Sentry.init({ beforeSendTransaction(event) { return event | null } })
Sentry.init({ beforeBreadcrumb(breadcrumb, hint) { return breadcrumb | null } })
Sentry.init({ ignoreErrors: ["string", /regex/] })
Sentry.init({ allowUrls: [/regex/] })
Sentry.init({ denyUrls: [/regex/] })
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Errors not appearing from `error.tsx` | Add `Sentry.captureException(error)` in a `useEffect` — Next.js catches these before Sentry |
| Server Component errors missing | Ensure `export const onRequestError = Sentry.captureRequestError` is in `instrumentation.ts`; requires SDK ≥8.28.0 + Next.js 15 |
| Minified stack traces | Configure `authToken` in `withSentryConfig` for source map upload; use `digest` to correlate server logs with Sentry events |
| Duplicate errors | Check that only one handler captures the same error; in dev, React Strict Mode may double-fire — validate in production builds |
| Server Action errors missing | Use `withServerActionInstrumentation` wrapper or add `captureException` before any graceful `return` |
| Events blocked by ad-blockers | Set `tunnelRoute: "/monitoring"` in `withSentryConfig`; exclude the route from your middleware matcher |
| Missing edge errors | Verify `sentry.edge.config.ts` is imported via `instrumentation.ts` when `NEXT_RUNTIME === "edge"` |
| Turbopack source map issues | Turbopack source map upload support is experimental; fall back to webpack for production builds if maps are missing |
| Events from wrong DSN in hybrid app | All three runtimes (client, server, edge) use the same DSN; verify each init file has identical DSN value |
| `captureUnderscoreErrorException` not awaited | In Pages Router `_error.tsx`, always `await` it — serverless functions may exit before Sentry flushes otherwise |

---

## Reference: Logging

# Logging — Sentry Next.js SDK

> Minimum SDK: `@sentry/nextjs` ≥9.41.0+ for `Sentry.logger` API and `enableLogs`  
> `consoleLoggingIntegration()` multi-arg parsing: requires ≥10.13.0+  
> Scope-based attributes (`getGlobalScope`, `getIsolationScope`): requires ≥10.32.0+

> ⚠️ **Not available via CDN/loader snippet** — NPM install required.

---

## Enabling Logs

`enableLogs` must be set in **all three** Next.js runtime config files:

```typescript
// instrumentation-client.ts → use NEXT_PUBLIC_SENTRY_DSN
// sentry.server.config.ts   → use SENTRY_DSN
// sentry.edge.config.ts     → use SENTRY_DSN
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN, // use NEXT_PUBLIC_SENTRY_DSN in client config
  enableLogs: true, // Required — logging is disabled by default
});
```

Without `enableLogs: true`, all `Sentry.logger.*` calls are silently no-ops.

---

## Logger API — Six Levels

```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.logger.trace("Entering processOrder", { fn: "processOrder", orderId: "ord_1" });
Sentry.logger.debug("Cache lookup", { key: "user:123", hit: false });
Sentry.logger.info("Order created", { orderId: "order_456", total: 99.99 });
Sentry.logger.warn("Rate limit approaching", { current: 95, max: 100 });
Sentry.logger.error("Payment failed", { reason: "card_declined", userId: "u_1" });
Sentry.logger.fatal("Database unavailable", { host: "db-primary" });
```

| Level | Method | Typical Use |
|-------|--------|-------------|
| `trace` | `Sentry.logger.trace()` | Ultra-granular function entry/exit; high-volume — filter out in production |
| `debug` | `Sentry.logger.debug()` | Development diagnostics, cache hits/misses |
| `info` | `Sentry.logger.info()` | Normal business milestones, confirmations |
| `warn` | `Sentry.logger.warn()` | Degraded state, approaching limits, recoverable issues |
| `error` | `Sentry.logger.error()` | Failures requiring attention |
| `fatal` | `Sentry.logger.fatal()` | Critical failures, system unavailable |

**Attribute value types:** `string`, `number`, `boolean` only — `undefined`, arrays, and objects are not accepted.

---

## Parameterized Messages — `Sentry.logger.fmt`

The `fmt` tagged template literal binds each interpolated variable as a **structured, searchable attribute** in Sentry:

```typescript
const userId = "user_123";
const productName = "Widget Pro";
const amount = 49.99;

Sentry.logger.info(
  Sentry.logger.fmt`User ${userId} purchased ${productName} for $${amount}`
);
```

This produces:
```
message.template:     "User %s purchased %s for $%s"
message.parameter.0:  "user_123"
message.parameter.1:  "Widget Pro"
message.parameter.2:  49.99
```

Each parameter is independently searchable in Sentry's log explorer.

> ⚠️ `logger.fmt` must be used as a **tagged template literal** — not a function call. `Sentry.logger.fmt("text")` will not produce structured parameters.

### When to use `fmt` vs plain attributes

| Approach | Use when |
|----------|----------|
| `Sentry.logger.info(msg, { key: val })` | Variables are logically distinct attributes with names |
| `Sentry.logger.info(Sentry.logger.fmt\`...\`)` | Variables are part of a human-readable sentence |

---

## Console Capture — `consoleLoggingIntegration`

Automatically forwards `console.*` calls to Sentry as structured logs:

```typescript
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enableLogs: true,
  integrations: [
    Sentry.consoleLoggingIntegration({
      levels: ["log", "warn", "error"], // which console methods to forward
    }),
  ],
});
```

Multiple arguments are mapped to positional parameters (requires SDK ≥10.13.0):
```
console.log("User action recorded", userId, success)
  → message.parameter.0 = <userId value>
  → message.parameter.1 = <success value>
```

| Console method | Sentry log level |
|----------------|-----------------|
| `console.log` | `info` |
| `console.info` | `info` |
| `console.warn` | `warn` |
| `console.error` | `error` |
| `console.debug` | `debug` |
| `console.assert` (failing) | `error` |

---

## Log Filtering — `beforeSendLog`

Use `beforeSendLog` to drop, modify, or scrub logs before they are sent. Return `null` to discard:

```typescript
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enableLogs: true,
  beforeSendLog: (log) => {
    // Drop debug and trace logs in production
    if (log.level === "debug" || log.level === "trace") {
      return null;
    }

    // Scrub sensitive attribute keys
    if (log.attributes?.password) {
      delete log.attributes.password;
    }
    if (log.attributes?.["credit_card"]) {
      log.attributes["credit_card"] = "[REDACTED]";
    }

    // Drop noisy health-check logs by message content
    if (log.message?.includes("/health")) {
      return null;
    }

    return log; // send the (possibly modified) log
  },
});
```

### The `log` object shape

| Field | Type | Description |
|-------|------|-------------|
| `level` | `string` | `"trace"` \| `"debug"` \| `"info"` \| `"warn"` \| `"error"` \| `"fatal"` |
| `message` | `string` | The log message text |
| `timestamp` | `number` | Unix timestamp |
| `attributes` | `object` | Key/value pairs attached to this log |

---

## Scope-Based Automatic Attributes (SDK ≥10.32.0)

Attributes set on scopes are automatically added to all logs emitted within that scope.

```typescript
// Global scope — shared across the entire app lifetime
Sentry.getGlobalScope().setAttributes({
  service: "checkout",
  version: "2.1.0",
});

// Isolation scope — unique per request
// ⚠️ CRITICAL for Next.js server-side: use isolation scope (not global)
// to prevent attributes from one request leaking into another
Sentry.getIsolationScope().setAttributes({
  org_id: user.orgId,
  user_tier: user.tier,
});

// Current scope — wraps a single operation
Sentry.withScope((scope) => {
  scope.setAttribute("request_id", req.id);
  Sentry.logger.info("Processing order"); // gets request_id attribute
});
```

> ⚠️ **Next.js server-side isolation:** Always use `getIsolationScope()` for per-request data on the server. The isolation scope is unique per request, preventing attributes from one user's request from bleeding into another's concurrent request.

---

## Third-Party Logger Integrations

### Pino (SDK ≥10.18.0)

```typescript
// sentry.server.config.ts — Pino is a Node.js integration (server-side only)
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  enableLogs: true,
  integrations: [Sentry.pinoIntegration()],
});
// No changes needed to your pino logger — it auto-captures logs
```

### Consola (SDK ≥10.12.0)

```typescript
import { consola } from "consola";

const sentryReporter = Sentry.createConsolaReporter({
  levels: ["error", "warn"], // optional: only forward these levels
});

consola.addReporter(sentryReporter);
```

### Winston (SDK ≥9.13.0)

```typescript
import winston from "winston";
import Transport from "winston-transport";

const SentryTransport = Sentry.createSentryWinstonTransport(Transport, {
  levels: ["error", "warn"],
});

const logger = winston.createLogger({
  transports: [new SentryTransport()],
});
```

---

## Auto-Generated Attributes

These are added by the SDK to every log without any developer configuration:

| Attribute | Notes |
|-----------|-------|
| `sentry.environment` | Always present |
| `sentry.release` | Always present |
| `sentry.sdk.name` | e.g., `"sentry.javascript.nextjs"` |
| `sentry.sdk.version` | Always present |
| `browser.name`, `browser.version` | Client-side only |
| `user.id`, `user.name`, `user.email` | When `Sentry.setUser()` + `sendDefaultPii: true` |
| `sentry.trace.parent_span_id` | When inside an active span (enables log ↔ trace correlation) |
| `sentry.replay_id` | Client-side with Replay enabled |
| `server.address` | Server-side only |
| `message.template` | When using `logger.fmt` |
| `message.parameter.N` | When using `logger.fmt` or `consoleLoggingIntegration` |

---

## Next.js-Specific: Three-Runtime Configuration

For consistency across all runtimes, enable logging in all three config files:

```typescript
// instrumentation-client.ts
import * as Sentry from "@sentry/nextjs";
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enableLogs: true,
  integrations: [Sentry.consoleLoggingIntegration({ levels: ["warn", "error"] })],
});

// sentry.server.config.ts
import * as Sentry from "@sentry/nextjs";
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  enableLogs: true,
  integrations: [Sentry.pinoIntegration()], // or consoleLoggingIntegration
});

// sentry.edge.config.ts
import * as Sentry from "@sentry/nextjs";
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  enableLogs: true,
});
```

### Server Action Logging Example

```typescript
// app/actions/order.ts
"use server";
import * as Sentry from "@sentry/nextjs";

export async function createOrder(formData: FormData) {
  // Use isolation scope for per-request context on the server
  Sentry.getIsolationScope().setAttributes({
    action: "createOrder",
    userId: formData.get("userId") as string,
  });

  Sentry.logger.info("Order creation started", {
    productId: formData.get("productId") as string,
  });

  try {
    const order = await db.orders.create(/* ... */);
    Sentry.logger.info("Order created successfully", { orderId: order.id });
    return order;
  } catch (err) {
    Sentry.logger.error("Order creation failed", {
      reason: (err as Error).message,
    });
    throw err;
  }
}
```

---

## Best Practice: Wide Events

Prefer **one comprehensive log with all context** over many fragmented logs:

```typescript
// ✅ Preferred — one wide log with full context
Sentry.logger.info("Checkout completed", {
  orderId: order.id,
  userId: user.id,
  cartValue: cart.total,
  itemCount: cart.items.length,
  paymentMethod: "stripe",
  userTier: user.tier,
  durationMs: Date.now() - startTime,
});

// ❌ Avoid — fragmented logs that are hard to correlate
Sentry.logger.info("Cart validated");
Sentry.logger.info("Payment processed");
Sentry.logger.info("Checkout done");
```

---

## SDK Version Matrix

| Feature | Min SDK Version |
|---------|----------------|
| `enableLogs` / `Sentry.logger.*` | **9.41.0** |
| Winston transport | 9.13.0 |
| Consola reporter | 10.12.0 |
| Console integration multi-arg parsing | 10.13.0 |
| Pino integration | 10.18.0 |
| Scope attributes (`setAttributes`) | **10.32.0** |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing in Sentry | Verify `enableLogs: true` in `Sentry.init()`; check all three config files (client, server, edge) |
| `logger.fmt` not creating `message.parameter.*` | Use as tagged template: `Sentry.logger.fmt\`text ${var}\`` — not `Sentry.logger.fmt("text", var)` |
| Logs not linked to traces | Ensure `tracesSampleRate` > 0 and the log is emitted inside an active span |
| `consoleLoggingIntegration` not available | Upgrade to ≥10.13.0 |
| Scope attributes not appearing | Upgrade to ≥10.32.0; use `getIsolationScope()` (not `getGlobalScope()`) for server request data |
| Cross-request attribute leakage on server | Replace `getGlobalScope()` with `getIsolationScope()` for per-request data |
| Too many logs / high volume | Use `beforeSendLog` to drop `trace` and `debug` levels in production |
| Log attributes contain `undefined` | Only `string`, `number`, `boolean` are accepted — filter out undefined values |
| `beforeSendLog` not firing | Confirm `enableLogs: true` is set — without it, no logs are processed |
| Sensitive data appearing in logs | Add filtering in `beforeSendLog`; better yet, avoid logging sensitive data at the call site |
| Edge runtime logs missing | Add `enableLogs: true` to `sentry.edge.config.ts` |

---

## Reference: Profiling

# Profiling — Sentry Next.js SDK

> Browser profiling: `@sentry/nextjs` ≥10.27.0 (Beta)  
> Node.js profiling: `@sentry/profiling-node` — must match `@sentry/nextjs` version exactly

---

## Overview

The Sentry Next.js SDK supports profiling in **two independent runtimes**:

| Runtime | Integration | What it captures |
|---|---|---|
| **Browser** | `browserProfilingIntegration()` | JS call stacks in Chrome/Edge (Chromium only) at 100Hz |
| **Node.js server** | `nodeProfilingIntegration()` | V8 CPU call stacks for API routes, RSC, server actions |

Both are **opt-in** and **independent from each other**. Each attaches to spans and requires tracing to be enabled.

---

## How Profiling Relates to Tracing

Profiles attach to **spans** — they are not independent events:

1. `tracesSampleRate` / `tracesSampler` decides whether a request is traced at all
2. `profileSessionSampleRate` decides whether the **session** opts into profiling
3. A profile is only collected when **both** sampling decisions are "yes"

```
tracesSampleRate: 0.1   + profileSessionSampleRate: 0.5
→ ~5% of requests will have both a trace AND a profile attached
```

In `trace` lifecycle mode, you can drill from a slow span in the Performance UI directly into a flame graph:

```
Trace: "POST /api/checkout" (850ms)
  ├── "validateCart" (45ms) → [Profile attached] → shows db driver hot paths
  ├── "processPayment" (620ms)
  └── "updateInventory" (185ms) → [Profile attached] → shows ORM overhead
```

---

## Browser Profiling

### Browser Compatibility

| Browser | Supported | Notes |
|---------|-----------|-------|
| Chrome / Chromium | ✅ | Primary support |
| Edge (Chromium) | ✅ | Same engine as Chrome |
| Firefox | ❌ | Does not implement JS Self-Profiling API |
| Safari / iOS Safari | ❌ | Does not implement JS Self-Profiling API |

> ⚠️ **Sampling bias:** Profile data comes **only** from Chromium users. In unsupported browsers, `browserProfilingIntegration()` silently no-ops with no errors and no overhead.

### Required: `Document-Policy` Header

The JS Self-Profiling API is gated behind a required response header. Without it, profiling silently fails even in Chromium:

```
Document-Policy: js-profiling
```

**Next.js (`next.config.ts`):**
```typescript
const nextConfig = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [{ key: "Document-Policy", value: "js-profiling" }],
      },
    ];
  },
};
```

**Vercel (`vercel.json`):**
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [{ "key": "Document-Policy", "value": "js-profiling" }]
    }
  ]
}
```

**Netlify (`netlify.toml`):**
```toml
[[headers]]
  for = "/*"
  [headers.values]
    Document-Policy = "js-profiling"
```

**Nginx:**
```nginx
add_header Document-Policy "js-profiling";
```

> ⚠️ Static hosting that doesn't support custom headers (some CDNs, GitHub Pages) will prevent browser profiling entirely.

### SDK Configuration — Trace Mode (Recommended)

Profiles auto-attach to all sampled spans with no additional code:

```typescript
// instrumentation-client.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,

  integrations: [
    Sentry.browserTracingIntegration(), // Must come BEFORE browserProfilingIntegration
    Sentry.browserProfilingIntegration(),
  ],

  tracesSampleRate: 1.0,

  // Session-level sampling: decision made once at page load
  profileSessionSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,

  // "trace" = profiles auto-attach to every sampled span
  profileLifecycle: "trace",
});
```

### SDK Configuration — Manual Mode

Profile specific flows or code paths explicitly:

```typescript
// instrumentation-client.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.browserProfilingIntegration(),
  ],
  tracesSampleRate: 1.0,
  profileSessionSampleRate: 1.0,
  // No profileLifecycle → defaults to manual mode
});

// Explicit start/stop around critical code:
Sentry.uiProfiler.startProfiler();
await heavyComputation();
Sentry.uiProfiler.stopProfiler();
```

---

## Node.js Profiling

### Installation

```bash
npm install @sentry/profiling-node --save
```

> ⚠️ **Version pinning is required.** `@sentry/profiling-node` must exactly match your `@sentry/nextjs` version. Mismatched versions cause silent failures.

```bash
# Both should be the same version
npm install @sentry/nextjs@latest @sentry/profiling-node@latest
```

### SDK Configuration

```typescript
// sentry.server.config.ts
import * as Sentry from "@sentry/nextjs";
import { nodeProfilingIntegration } from "@sentry/profiling-node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,

  integrations: [
    nodeProfilingIntegration(), // V8 CpuProfiler native add-on
  ],

  tracesSampleRate: 1.0,

  // Session-level: decision made once at process startup
  profileSessionSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,

  profileLifecycle: "trace", // auto-attach profiles to spans
});
```

> ⚠️ **Do NOT add `nodeProfilingIntegration` to `sentry.edge.config.ts`.** The Edge runtime does not support native add-ons.

### Manual Mode (Node.js)

```typescript
// sentry.server.config.ts
Sentry.init({
  integrations: [nodeProfilingIntegration()],
  profileSessionSampleRate: 1.0,
  profileLifecycle: "manual",
});

// Explicit start/stop:
Sentry.profiler.startProfiler();
await processHeavyJob();
Sentry.profiler.stopProfiler();
```

### Supported Platforms

Precompiled native binaries are available for:

| OS | Architecture | Node.js |
|---|---|---|
| macOS | x64 | 18–24 |
| Linux (glibc) | x64 | 18–24 |
| Linux (musl/Alpine) | x64, ARM64 | 18–24 |
| Linux | ARM64 | 18–24 |
| Windows | x64 | 18–24 |

> ⚠️ **Deno and Bun are not supported.** The native add-on only works in Node.js.

### Environment Variables

```bash
# Override binary path (for custom builds)
SENTRY_PROFILER_BINARY_PATH=/custom/path/profiler.node

# Override binary directory
SENTRY_PROFILER_BINARY_DIR=/path/to/dir

# Profiler logging mode:
# "eager" (default) — faster startProfiler calls, slightly more CPU overhead
# "lazy" — lower CPU overhead, slightly slower startProfiler
SENTRY_PROFILER_LOGGING_MODE=lazy node server.js
```

---

## Configuration Parameters Reference

| Parameter | Applies to | Description |
|-----------|-----------|-------------|
| `profileSessionSampleRate` | Browser + Node.js | 0.0–1.0; session-level sampling decision made once (at page load for browser, process start for server) |
| `profileLifecycle` | Browser + Node.js | `"trace"` = auto-attach to spans; omit for manual mode |
| `browserProfilingIntegration()` | Browser only | Enables JS Self-Profiling API (Chromium only); must come after `browserTracingIntegration()` |
| `nodeProfilingIntegration()` | Node.js only | Enables V8 CpuProfiler; must be in `integrations` array in `sentry.server.config.ts` |

### `profileSessionSampleRate` Semantics

The profiling sampling decision is made **once per session**:
- **Browser:** at page load (`instrumentation-client.ts` init)
- **Server:** at process startup (`sentry.server.config.ts` init)

A "profiling session" either opts in or opts out for its entire lifetime. Within a profiling session, every traced span gets a profile attached (in `trace` mode).

### `profileLifecycle` Modes Comparison

| Mode | Trigger | Best for |
|------|---------|----------|
| `"trace"` | Auto-attached to every sampled span | Broad production coverage; no code changes |
| `"manual"` (default) | `startProfiler()` / `stopProfiler()` | Specific high-value flows (checkout, heavy renders) |

---

## Production vs Development Recommendations

```typescript
// Browser (instrumentation-client.ts)
Sentry.init({
  profileSessionSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
  profileLifecycle: "trace",
});

// Server (sentry.server.config.ts)
Sentry.init({
  integrations: [nodeProfilingIntegration()],
  profileSessionSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 1.0,
  profileLifecycle: "trace",
});
```

**Performance impact notes:**

- **Browser (100Hz sampling):** Low overhead; runs unobtrusively in production. Chrome DevTools profiles at 1000Hz — use Sentry profiling for production coverage, DevTools for local deep-dives.
- **Node.js (V8 CpuProfiler):** The native profiler adds CPU overhead. Test with realistic load before deploying `profileSessionSampleRate: 1.0` to high-traffic production.

> "For high-throughput environments, we recommend testing prior to deployment to ensure that your service's performance characteristics maintain expectations." — Sentry docs

### Chrome DevTools Conflict

When `browserProfilingIntegration` is active, Chrome DevTools profiler shows Sentry's overhead mixed into rendering work. Disable the integration when doing local DevTools profiling sessions.

---

## Complete Setup Example

```typescript
// instrumentation-client.ts (Browser)
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.browserProfilingIntegration(),
  ],
  tracesSampleRate: process.env.NODE_ENV === "development" ? 1.0 : 0.1,
  profileSessionSampleRate: process.env.NODE_ENV === "development" ? 1.0 : 0.1,
  profileLifecycle: "trace",
});
```

```typescript
// sentry.server.config.ts (Node.js)
import * as Sentry from "@sentry/nextjs";
import { nodeProfilingIntegration } from "@sentry/profiling-node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  integrations: [nodeProfilingIntegration()],
  tracesSampleRate: process.env.NODE_ENV === "development" ? 1.0 : 0.1,
  profileSessionSampleRate: process.env.NODE_ENV === "development" ? 1.0 : 0.1,
  profileLifecycle: "trace",
});
```

```typescript
// sentry.edge.config.ts (Edge — NO profiling)
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
  // nodeProfilingIntegration NOT added — Edge runtime doesn't support native add-ons
});
```

```typescript
// next.config.ts — required Document-Policy header for browser profiling
import { withSentryConfig } from "@sentry/nextjs";

const nextConfig = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [{ key: "Document-Policy", value: "js-profiling" }],
      },
    ];
  },
};

export default withSentryConfig(nextConfig, {
  org: process.env.SENTRY_ORG,
  project: process.env.SENTRY_PROJECT,
  authToken: process.env.SENTRY_AUTH_TOKEN,
  tunnelRoute: "/monitoring",
});
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No browser profiles appearing in Sentry | Verify `Document-Policy: js-profiling` is present on document responses (check Network tab in DevTools) |
| Browser profiles only from some users | Expected — only Chromium users are profiled; Firefox/Safari silently no-op |
| Chrome DevTools shows inflated rendering times | Disable `browserProfilingIntegration()` during local DevTools profiling sessions |
| `profileSessionSampleRate` has no effect (browser) | Ensure `browserProfilingIntegration()` is listed **after** `browserTracingIntegration()` in `integrations` |
| No server profiles appearing | Verify `@sentry/profiling-node` version exactly matches `@sentry/nextjs` version |
| `nodeProfilingIntegration` import error | Check `@sentry/profiling-node` is installed and versions match; don't import it in `sentry.edge.config.ts` |
| Profiles not linked to spans | Confirm `profileLifecycle: "trace"` is set and `tracesSampleRate` > 0; both must be set |
| High CPU usage on server | Lower `profileSessionSampleRate` to 0.1 or 0.05; use `SENTRY_PROFILER_LOGGING_MODE=lazy` |
| Native add-on fails to load (Alpine/musl Linux) | Ensure the `@sentry/profiling-node` version supports your OS/arch — check the supported platforms table |
| Flame graphs show minified names | Upload source maps via `withSentryConfig` in `next.config.ts` with `authToken` and project credentials |
| Profiles on static host not working | Browser profiling requires the `Document-Policy` header — verify your host supports custom response headers |

---

## Reference: Session Replay

# Session Replay — Sentry Next.js SDK

> Minimum SDK: `@sentry/nextjs` ≥7.27.0+  
> `replayCanvasIntegration()`: requires ≥7.98.0+

> ⚠️ **Browser-only feature.** Add `replayIntegration()` **only** in `instrumentation-client.ts`. Never in `sentry.server.config.ts` or `sentry.edge.config.ts`.

---

## Setup

Session Replay is bundled in `@sentry/nextjs` — no separate package needed.

```typescript
// instrumentation-client.ts  ← client-side only
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,

  // Sample rates live at init level, NOT inside replayIntegration()
  replaysSessionSampleRate: 0.1,   // record 10% of all sessions from start
  replaysOnErrorSampleRate: 1.0,   // record 100% of sessions that hit an error

  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,     // default: true
      blockAllMedia: true,   // default: true
    }),
  ],
});
```

> **Dev tip:** Set `replaysSessionSampleRate: 1.0` during development to capture every session.

### Where NOT to Add Replay

| Config file | Why |
|-------------|-----|
| `sentry.server.config.ts` | Server runtime — no DOM |
| `sentry.edge.config.ts` | Edge runtime — no DOM |
| `instrumentation.ts` (server section) | Server-side code |
| Any Route Handler or Server Action | Server-side code |

---

## Sample Rates

| Option | Type | Default | Behavior |
|--------|------|---------|----------|
| `replaysSessionSampleRate` | `number` (0–1) | `0` | Fraction of all sessions recorded continuously from start |
| `replaysOnErrorSampleRate` | `number` (0–1) | `0` | Fraction of sessions captured when an error occurs — flushes ~60s of buffer, then continues recording |

**Recommended production sample rates by traffic:**

| Daily Sessions | `replaysSessionSampleRate` | `replaysOnErrorSampleRate` |
|----------------|---------------------------|---------------------------|
| 100,000+ | `0.01` (1%) | `1.0` |
| 10,000–100,000 | `0.10` (10%) | `1.0` |
| Under 10,000 | `0.25` (25%) | `1.0` |

Always keep `replaysOnErrorSampleRate: 1.0` — error replays provide the most debugging value.

### How Sampling Works

1. When a session starts, `replaysSessionSampleRate` is checked.
   - **Sampled → Session Mode:** Recording is sent to Sentry in real-time chunks.
   - **Not sampled → Buffer Mode:** Last ~60 seconds are kept in memory only. Nothing is sent unless an error occurs.
2. If an error occurs in a buffered session, `replaysOnErrorSampleRate` is checked.
   - **Sampled:** The 60-second buffer plus all subsequent data is sent to Sentry.
   - **Not sampled:** Buffer is discarded; nothing is sent.

---

## Session Lifecycle

- **Starts:** When the SDK first loads/initializes.
- **Ends:** After **5 minutes of inactivity** OR after a **maximum of 60 minutes** total.
- **Tab close:** Ends the session immediately.
- **Page refreshes/navigations** within the same domain and tab are captured within the same session.

---

## `replayIntegration()` Options Reference

All options go inside `Sentry.replayIntegration({})`:

### General Options

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `stickySession` | `boolean` | `true` | Tracks a user across page refreshes. One tab = one session. |
| `mutationLimit` | `number` | `10000` | Max DOM mutations before recording stops (performance protection). |
| `mutationBreadcrumbLimit` | `number` | `750` | Threshold for sending a warning breadcrumb about large mutations. |
| `minReplayDuration` | `number` | `5000` ms | Min replay length before sending. Max: 15000. Only applies to session sampling. |
| `maxReplayDuration` | `number` | `3600000` ms | Maximum replay length. Capped at 1 hour. |
| `workerUrl` | `string` | `undefined` | URL to a self-hosted compression worker (avoids inline worker in bundle). |
| `beforeAddRecordingEvent` | `(event) => event \| null` | identity fn | Hook to filter/modify recording events before they leave the browser. |
| `beforeErrorSampling` | `(event) => boolean` | `() => true` | Called in buffer mode only. Return `false` to prevent this error from triggering upload. |
| `slowClickIgnoreSelectors` | `string[]` | `[]` | CSS selectors exempt from slow/rage click detection. |

### Network Capture Options

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `networkDetailAllowUrls` | `(string \| RegExp)[]` | `[]` | URLs for which to capture request/response headers and bodies. |
| `networkDetailDenyUrls` | `(string \| RegExp)[]` | `[]` | URLs to never capture details for. Takes precedence over allow list. |
| `networkCaptureBodies` | `boolean` | `true` | Whether to capture request/response bodies for allowed URLs. |
| `networkRequestHeaders` | `string[]` | `[]` | Additional request headers to capture (beyond Content-Type, Content-Length, Accept). |
| `networkResponseHeaders` | `string[]` | `[]` | Additional response headers to capture. |

---

## Privacy Masking

**All masking/blocking happens on the client before any data is sent to Sentry's servers.**

### Default Privacy Behavior

| Setting | Default | Effect |
|---------|---------|--------|
| `maskAllText` | `true` | Every text character replaced with `*` |
| `maskAllInputs` | `true` | All `<input>` values masked |
| `blockAllMedia` | `true` | `img`, `svg`, `video`, `object`, `picture`, `embed`, `map`, `audio` replaced with same-size placeholder |

### Privacy Options in `replayIntegration({})`

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `mask` | `string[]` | `['.sentry-mask', '[data-sentry-mask]']` | Additional selectors to mask. |
| `maskAllText` | `boolean` | `true` | Mask all text via `maskFn`. |
| `maskAllInputs` | `boolean` | `true` | Mask all input values. |
| `maskFn` | `(text: string) => string` | `(s) => '*'.repeat(s.length)` | Custom masking function. |
| `block` | `string[]` | `['.sentry-block', '[data-sentry-block]']` | Additional selectors to block (replaced with a blank same-size box). |
| `blockAllMedia` | `boolean` | `true` | Block all media elements. |
| `ignore` | `string[]` | `['.sentry-ignore', '[data-sentry-ignore]']` | Input events on matching elements are ignored entirely. |
| `unblock` | `string[]` | `[]` | Selectors to un-block from `blockAllMedia`. |
| `unmask` | `string[]` | `[]` | Selectors to un-mask from `maskAllText`. |

### Three Privacy Mechanisms Compared

| Mechanism | What It Does | HTML Attribute | CSS Class |
|-----------|--------------|----------------|-----------|
| **Mask** | Replaces text chars with `*` | `data-sentry-mask` | `sentry-mask` |
| **Block** | Replaces entire element with blank box | `data-sentry-block` | `sentry-block` |
| **Ignore** | Suppresses input events on the element | `data-sentry-ignore` | `sentry-ignore` |

### Code Examples

**Opt-out of all masking (for non-PII sites):**
```typescript
Sentry.replayIntegration({
  // Only use if your site has NO sensitive data
  maskAllText: false,
  blockAllMedia: false,
});
```

**Custom masking selectors:**
```typescript
Sentry.replayIntegration({
  mask: [".sensitive-field", "[data-pii]"],
  unmask: [".safe-to-show"],
  block: [".user-avatar", "#credit-card-form"],
  unblock: [".public-image"],
  ignore: ["#search-input"],
});
```

**HTML-level masking (no JS config needed):**
```html
<!-- Block this form entirely -->
<form data-sentry-block>...</form>

<!-- Mask text in this element -->
<div class="sentry-mask">Sensitive content</div>

<!-- Ignore events on this input -->
<input class="sentry-ignore" type="text" />
```

> ⚠️ **v8 Breaking Change:** In SDK v8+, `unblock` and `unmask` no longer automatically add `sentry-unblock`/`sentry-unmask` class selectors. To restore v7 behavior:
> ```typescript
> Sentry.replayIntegration({
>   unblock: [".sentry-unblock, [data-sentry-unblock]"],
>   unmask: [".sentry-unmask, [data-sentry-unmask]"],
> });
> ```

---

## Network Request/Response Capture

By default, Replay captures only: URL, body size, method, status code. SDK ≥7.50.0 required for headers/bodies.

```typescript
Sentry.replayIntegration({
  // Capture details for all same-origin requests
  networkDetailAllowUrls: [
    window.location.origin,
    "api.example.com",
    /^https:\/\/api\.example\.com/,
  ],

  // Exclude PII-heavy endpoints
  networkDetailDenyUrls: ["/api/auth", /\/users\/\d+\/private/],

  networkCaptureBodies: true,
  networkRequestHeaders: ["Cache-Control", "X-Request-ID"],
  networkResponseHeaders: ["X-RateLimit-Remaining"],
});
```

**Limits:**
- Bodies truncated to **150k characters** max.
- Only text-based bodies captured: JSON, XML, FormData. Binary/media excluded.
- Sentry applies server-side PII scrubbing (credit cards, SSNs, private keys) on ingested data.

---

## Tree-Shaking Replay out of Server Bundles

**Critical for Next.js:** Session Replay is browser-only. Prevent it from being bundled into server-side or edge bundles:

```javascript
// next.config.js
const { withSentryConfig } = require("@sentry/nextjs");

module.exports = withSentryConfig(nextConfig, {
  webpack: {
    treeshake: {
      removeDebugLogging: true,        // Strip SDK internal debug logs
      excludeReplayIframe: false,      // Remove iframe content capture if unused
      excludeReplayShadowDOM: false,   // Remove shadow DOM capture if unused
      excludeReplayCompressionWorker: false, // Remove if using custom workerUrl
    },
  },
});
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `removeDebugLogging` | `boolean` | `false` | Strips SDK internal `console.log` calls. Safe to enable in production. |
| `removeTracing` | `boolean` | `false` | Removes ALL tracing code. Never call `Sentry.startSpan()` etc. if enabled. |
| `excludeReplayIframe` | `boolean` | `false` | Removes iframe content capture from Replay bundle. |
| `excludeReplayShadowDOM` | `boolean` | `false` | Removes shadow DOM capture from Replay bundle. |
| `excludeReplayCompressionWorker` | `boolean` | `false` | Removes built-in compression worker. Requires providing `workerUrl`. |

> ⚠️ Tree-shaking only works with **webpack** builds. **Turbopack is not supported.**

---

## Canvas Recording

> ⚠️ **There is currently NO PII scrubbing in canvas recordings.** Use with caution.

Canvas recording is opt-in and requires SDK ≥7.98.0:

```typescript
// instrumentation-client.ts
Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [
    Sentry.replayIntegration(),
    Sentry.replayCanvasIntegration(), // adds canvas support
  ],
});
```

**For WebGL/3D canvases** (manual snapshot mode):
```typescript
Sentry.replayCanvasIntegration({
  enableManualSnapshot: true,
});

function paint() {
  // ... your rendering commands ...

  const canvasEl = document.querySelector<HTMLCanvasElement>("#my-canvas");
  Sentry.getClient()
    ?.getIntegrationByName("ReplayCanvas")
    // @ts-ignore
    ?.snapshot(canvasEl);
}
```

---

## Lazy Loading Replay

To reduce initial bundle size, add `replayIntegration()` dynamically after the page loads:

```typescript
// instrumentation-client.ts

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [], // Replay NOT included here
});

// Later — after route change, user interaction, or feature flag check
import("@sentry/nextjs").then((lazySentry) => {
  Sentry.addIntegration(lazySentry.replayIntegration());
});
```

---

## Programmatic Replay Control

```typescript
const replay = Sentry.getReplay();

replay.start();           // Start in session mode (sends continuously)
replay.startBuffering();  // Start in buffer mode (only sends on error)
await replay.stop();      // End the current session
await replay.flush();     // Force upload any pending buffered data
```

Use cases:
- **User-based sampling:** Check authentication, then call `flush()` for premium users.
- **Route-based sampling:** Call `start()` only on high-value pages.
- **Error filtering:** Use `beforeErrorSampling` to prevent certain error types from triggering upload:

```typescript
Sentry.replayIntegration({
  beforeErrorSampling: (event) => {
    // Prevent console.error from triggering replay upload
    if (event.logger === "console") return false;
    return true;
  },
});
```

---

## Custom Compression Worker

Host the compression worker yourself to reduce bundle size and comply with strict CSP policies:

```typescript
// Step 1: Download worker.min.js from:
// https://github.com/getsentry/sentry-javascript/blob/develop/packages/replay-worker/examples/worker.min.js
// Host at /public/worker.min.js → served at /worker.min.js

// Step 2: Configure
Sentry.replayIntegration({
  workerUrl: "/assets/worker.min.js",
});
```

```javascript
// next.config.js — remove built-in worker from bundle
module.exports = withSentryConfig(nextConfig, {
  webpack: {
    treeshake: {
      excludeReplayCompressionWorker: true, // since you're hosting your own
    },
  },
});
```

---

## Content Security Policy (CSP)

Session Replay uses a Web Worker for off-thread compression. Required CSP directives:

```
worker-src 'self' blob:
child-src 'self' blob:   ← Required for Safari ≤ 15.4
```

Also add `sentry.io` to your CORS policy so the Sentry replay iframe can fetch CSS, fonts, and images.

**For Next.js, set headers in `next.config.js`:**
```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          {
            key: "Content-Security-Policy",
            value: "default-src 'self'; worker-src 'self' blob:; child-src 'self' blob:;",
          },
        ],
      },
    ];
  },
};
```

---

## Performance Impact

- **Bundle size:** ~**50KB gzipped** added to browser bundle.
- **Compression:** Off-thread in a Web Worker — does not block the main thread.
- **Mutation protection:** Recording auto-stops if DOM mutations exceed `mutationLimit` (default 10,000).
- **Large lists:** Virtualize or paginate long lists to avoid mutation limit triggers.

**Rage/slow click false positives** (Download/Print buttons that don't mutate DOM):
```typescript
Sentry.replayIntegration({
  slowClickIgnoreSelectors: [
    ".download-btn",
    'a[label*="download" i]',
    "#print-button",
  ],
});
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Replay data missing | CSP blocking blob: workers | Add `worker-src 'self' blob:` |
| CSS/fonts missing in replay | CORS blocking Sentry iframe | Add `sentry.io` to CORS policy |
| Replay not recording | Added to wrong config file | Move to `instrumentation-client.ts` only |
| Click positions misaligned | Custom variable-width fonts | Add `Access-Control-Allow-Origin` headers for fonts |
| Too many rage clicks | Non-mutating buttons (Download, Print) | Use `slowClickIgnoreSelectors` |
| Replay stops early | Too many DOM mutations | Virtualize lists; adjust `mutationLimit` |
| `captureConsoleIntegration` triggers replays | `console.error` counted as error | Use `beforeErrorSampling` to return `false` for console events |
| iframe content not masked | `srcdoc` attribute bypasses masking | Add `block: ["iframe"]` to block iframes entirely |
| Canvas not recording | Not using `replayCanvasIntegration()` | Add `Sentry.replayCanvasIntegration()` alongside `replayIntegration()` |
| Build error about browser globals in server | Replay leaking into server bundle | Use tree-shaking options in `withSentryConfig` |
| `replayCanvasIntegration` not available | SDK version too old | Upgrade to ≥7.98.0 |

---

## Reference: Tracing

# Tracing — Sentry Next.js SDK

> Minimum SDK: `@sentry/nextjs` ≥8.0.0  
> `withServerActionInstrumentation`: ≥8.0.0  
> `enableLongAnimationFrame`: ≥8.18.0  
> `ignoreSpans`: ≥10.2.0

---

## How Tracing Is Activated

Tracing is enabled by setting **`tracesSampleRate`** or **`tracesSampler`** in all three runtime config files. Without one of these, no spans are created.

| Config file | Runtime | What it traces |
|---|---|---|
| `instrumentation-client.ts` | Browser | Page loads, navigations, fetch/XHR, Web Vitals, INP |
| `sentry.server.config.ts` | Node.js | API routes, RSC renders, `getServerSideProps`, background work |
| `sentry.edge.config.ts` | Edge | Next.js middleware |

> ⚠️ **All three must have tracing configured.** Missing one means that runtime produces no spans.

---

## `tracesSampleRate` — Uniform Sampling

A number between `0.0` and `1.0`. Set the same option in all three configs:

```typescript
// Recommended: 100% in development, lower in production
tracesSampleRate: process.env.NODE_ENV === "development" ? 1.0 : 0.1,
```

> **To disable tracing entirely:** omit both `tracesSampleRate` and `tracesSampler`. Setting `tracesSampleRate: 0` is not the same — it still activates instrumentation but sends nothing.

---

## `tracesSampler` — Dynamic Per-Request Sampling

When defined, `tracesSampler` takes **precedence** over `tracesSampleRate`. Receives a `SamplingContext` and returns a number (0–1) or boolean.

```typescript
// TypeScript: SamplingContext shape
interface SamplingContext {
  name: string;                                      // e.g. "GET /api/users"
  attributes: SpanAttributes | undefined;
  parentSampled: boolean | undefined;                // parent's sampling decision
  parentSampleRate: number | undefined;
  inheritOrSampleWith: (fallbackRate: number) => number;
}
```

### Route-Based Sampling

```typescript
Sentry.init({
  tracesSampler: ({ name, inheritOrSampleWith }) => {
    // Always drop health checks
    if (name.includes("/health") || name.includes("/ping")) return 0;

    // Always sample critical flows
    if (name.includes("/checkout") || name.includes("/payment")) return 1.0;

    // Sample admin routes at 50%
    if (name.includes("/admin")) return 0.5;

    // For everything else: honor parent's decision, fall back to 10%
    return inheritOrSampleWith(0.1);
  },
});
```

### With Parent Trace Inheritance

```typescript
Sentry.init({
  tracesSampler: ({ name, parentSampled, inheritOrSampleWith }) => {
    if (name.includes("healthcheck")) return 0;
    if (name.includes("auth"))        return 1;
    // inheritOrSampleWith: respects parent decision if present, else uses fallback
    return inheritOrSampleWith(0.5);
  },
});
```

**Why use `inheritOrSampleWith` instead of checking `parentSampled` directly?**  
It ensures consistent rates flow through distributed traces, enables accurate metric extrapolation, and sets the correct `sentry-sampled` value in downstream `baggage`.

### Sampling Precedence

1. `tracesSampler` function (if defined) — evaluated first
2. Parent's sampling decision (propagated via `sentry-trace` header)
3. `tracesSampleRate` (uniform fallback)

---

## Auto-Instrumented Operations

### Client-Side (Browser)

| Operation | Op | What's captured |
|---|---|---|
| Initial page load | `pageload` | LCP, CLS, FCP, TTFB Web Vitals; resource load child spans |
| Client-side navigation | `navigation` | Route change duration; child fetch/XHR spans |
| `fetch()` requests | `http.client` | URL, method, status code, duration, HTTP timings |
| `XMLHttpRequest` | `http.client` | Same as fetch |
| User interactions | `ui.interaction` | INP (Interaction to Next Paint) — emitted on page hide |
| Long Tasks (> 50ms) | `ui.long-task` | Main-thread blocking events |
| Long Animation Frames | `ui.long-animation-frame` | LoAF rendering work — SDK ≥8.18.0 |

### Server-Side (Node.js)

| Operation | Op | Notes |
|---|---|---|
| API route handlers (App Router) | `http.server` | `app/api/*/route.ts` — auto-instrumented |
| API route handlers (Pages Router) | `http.server` | `pages/api/*.ts` — auto-instrumented |
| React Server Components | `http.server` | RSC render times |
| `getServerSideProps` | `http.server` | Pages Router SSR data fetching |
| Edge Middleware | `http.server` | Via `sentry.edge.config.ts` |

> ⚠️ **Server Actions are NOT auto-instrumented.** Wrap each with `withServerActionInstrumentation()` — see below.

---

## `browserTracingIntegration` Options

```typescript
// instrumentation-client.ts
Sentry.init({
  integrations: [
    Sentry.browserTracingIntegration({
      // Page Load & Navigation
      instrumentPageLoad: true,        // default: true
      instrumentNavigation: true,      // default: true

      // HTTP spans
      traceFetch: true,                // default: true
      traceXHR: true,                  // default: true
      enableHTTPTimings: true,         // default: true
      shouldCreateSpanForRequest: (url) => !url.includes("/health"),

      // Performance observations
      enableLongTask: true,            // default: true
      enableLongAnimationFrame: true,  // default: true (SDK ≥8.18.0)
      enableInp: true,                 // INP spans

      // Span lifecycle
      idleTimeout: 1000,               // ms: wait after last child before ending
      finalTimeout: 30000,             // ms: hard cap on span duration
      childSpanTimeout: 15000,         // ms: max time for child spans

      // Span naming — parameterize URLs
      beforeStartSpan: (context) => ({
        ...context,
        name: context.name.replace(/\/\d+/g, "/<id>"),
      }),

      // Span filtering
      ignoreResourceSpans: ["resource.css", "resource.script", "resource.img"],
    }),
  ],
});
```

---

## Custom Spans

### `Sentry.startSpan()` — Active, Auto-Ending (Recommended)

Wraps a block of work. The span becomes active (children nest under it) and ends automatically when the callback returns or resolves:

```typescript
// Async
const data = await Sentry.startSpan(
  {
    name: "fetchUserProfile",
    op: "http.client",
    attributes: { "user.id": userId, "cache.hit": false },
  },
  async () => {
    const res = await fetch(`/api/users/${userId}`);
    return res.json();
  },
);

// Sync
const result = Sentry.startSpan(
  { name: "computeRecommendations", op: "function" },
  () => expensiveComputation(),
);
```

### Nested Spans (Parent–Child Hierarchy)

```typescript
await Sentry.startSpan({ name: "checkout-flow", op: "function" }, async () => {
  // These are automatically children of "checkout-flow"
  const cart = await Sentry.startSpan(
    { name: "fetchCart", op: "db.query" },
    () => db.cart.findUnique({ where: { userId } }),
  );

  const payment = await Sentry.startSpan(
    { name: "processPayment", op: "http.client" },
    () => stripe.paymentIntents.create({ amount: cart.total }),
  );

  return { cart, payment };
});
```

### `Sentry.startSpanManual()` — Active, Manual End

Use when the span lifetime cannot be enclosed in a callback:

```typescript
function authMiddleware(req: Request, res: Response, next: NextFunction) {
  return Sentry.startSpanManual({ name: "auth.verify", op: "middleware" }, (span) => {
    res.once("finish", () => {
      span.setStatus({ code: res.statusCode < 400 ? 1 : 2 });
      span.end(); // ← required
    });
    return next();
  });
}
```

### `Sentry.startInactiveSpan()` — Not Active, Manual End

Creates a span that is **never** automatically made active. Use for parallel work or event-based tracking:

```typescript
// Parallel independent operations
const spanA = Sentry.startInactiveSpan({ name: "operation-a" });
const spanB = Sentry.startInactiveSpan({ name: "operation-b" });

await Promise.all([doA(), doB()]);

spanA.end();
spanB.end();

// Explicit parent assignment
const parent = Sentry.startInactiveSpan({ name: "parent" });
const child = Sentry.startInactiveSpan({ name: "child", parentSpan: parent });
child.end();
parent.end();
```

### Browser: `setActiveSpanInBrowser()` — Persistent Active Span

When a callback-based API isn't practical (e.g., UI event handlers), keep a span active across event calls. Available since SDK v10.15.0:

```typescript
let checkoutSpan: Sentry.Span | undefined;

onCheckoutStart(() => {
  checkoutSpan = Sentry.startInactiveSpan({ name: "checkout-flow" });
  Sentry.setActiveSpanInBrowser(checkoutSpan);
});

onCheckoutComplete(() => {
  checkoutSpan?.end();
});
```

> ⚠️ `setActiveSpanInBrowser` is **browser-only**.

---

## Span Options Reference

```typescript
interface StartSpanOptions {
  name: string;              // Required: label shown in the UI
  op?: string;               // Operation category (see table below)
  attributes?: Record<string, string | number | boolean>;
  parentSpan?: Span;         // Override automatic parent
  onlyIfParent?: boolean;    // Skip span if no active parent exists
  forceTransaction?: boolean; // Force display as root transaction in UI
  startTime?: number;        // Unix timestamp in seconds
}
```

**Common `op` values:**

| `op` | Use for |
|------|---------|
| `http.client` | Outgoing HTTP requests (fetch, XHR) |
| `http.server` | Incoming HTTP requests (API routes, SSR) |
| `db` / `db.query` | Database queries |
| `db.redis` | Redis operations |
| `function` | General function calls |
| `ui.render` | Component render time |
| `ui.action.click` | Click event handling |
| `cache.get` / `cache.put` | Cache reads/writes |
| `queue.publish` / `queue.process` | Message queue operations |
| `task` | Background / scheduled work |

---

## Span Enrichment

```typescript
// Set attributes on the currently active span
const span = Sentry.getActiveSpan();
if (span) {
  span.setAttribute("db.table", "users");
  span.setAttributes({
    "http.method": "POST",
    "order.total": 99.99,
    "user.tier": "premium",
  });

  // Status: 0=unset, 1=ok, 2=error
  span.setStatus({ code: 1 });
  span.setStatus({ code: 2, message: "Payment declined" });
}

// Rename a span at runtime
const span = Sentry.getActiveSpan();
if (span) Sentry.updateSpanName(span, "GET /users/:id");

// Modify all spans globally before sending
Sentry.init({
  beforeSendSpan(span) {
    span.data = {
      ...span.data,
      "deployment.region": process.env.AWS_REGION ?? "unknown",
    };
    return span; // return null to drop (but prefer ignoreSpans for that)
  },
});
```

---

## Server Actions — `withServerActionInstrumentation()`

Server Actions are not auto-instrumented. Wrap each with `withServerActionInstrumentation()`:

```typescript
// app/actions/order.ts
"use server";
import * as Sentry from "@sentry/nextjs";
import { headers } from "next/headers";

export async function createOrder(formData: FormData) {
  return Sentry.withServerActionInstrumentation(
    "createOrder",                       // Action name (becomes span name)
    {
      headers: await headers(),          // Enables distributed trace continuation
      formData,                          // Logged as span data
      recordResponse: true,              // Capture the return value
    },
    async () => {
      const order = await db.orders.create({
        data: { items: formData.get("items"), userId: getCurrentUser() },
      });
      return { success: true, orderId: order.id };
    },
  );
}
```

**Options:**

| Option | Type | Description |
|--------|------|-------------|
| `formData` | `FormData` | Logged with the span |
| `headers` | `Headers` | Required for distributed trace continuation — always pass `await headers()` |
| `recordResponse` | `boolean` | Whether to capture the return value as span data |

---

## Distributed Tracing

### How It Works

Sentry injects two HTTP headers into outgoing requests:

| Header | Format | Purpose |
|--------|--------|---------|
| `sentry-trace` | `{traceId}-{spanId}-{sampled}` | Carries trace context |
| `baggage` | W3C Baggage with `sentry-*` keys | Carries sampling decision + metadata |

Backends must allowlist these headers for CORS:
```
Access-Control-Allow-Headers: sentry-trace, baggage
```

### `tracePropagationTargets`

Controls which outgoing requests get trace headers. Accepts strings (substring match) and/or RegExp:

```typescript
// instrumentation-client.ts
Sentry.init({
  tracePropagationTargets: [
    "localhost",                            // any URL containing "localhost"
    /^https:\/\/api\.yourapp\.com/,         // your API
    /^https:\/\/auth\.yourapp\.com/,        // auth service
    /^\//,                                  // all same-origin relative paths
  ],
});
```

**Default:** `['localhost', /^\//]` — only localhost and same-origin requests.  
**Disable entirely:** `tracePropagationTargets: []`

> ⚠️ If your API is at `http://localhost:3001`, use `"localhost:3001"` or a regex matching the port — `"localhost"` alone won't match.

### Automatic SSR → Client Trace Continuation

When Next.js server-renders a page, Sentry emits trace context as `<meta>` tags in `<head>`. The browser SDK reads them automatically to continue the same trace:

```html
<!-- Auto-injected by Next.js SDK — no configuration needed -->
<meta name="sentry-trace" content="12345678...-1234567890123456-1" />
<meta name="baggage" content="sentry-trace_id=12345678...,sentry-sample_rate=0.1,..." />
```

This means a single distributed trace spans the server render **and** subsequent client-side activity.

### Manual Trace Propagation (Non-HTTP Channels)

For WebSockets, message queues, or other protocols:

```typescript
// Sender — extract current trace context
const traceData = Sentry.getTraceData();
// Returns: { "sentry-trace": "...", "baggage": "..." }

webSocket.send(JSON.stringify({
  payload: myData,
  _sentryMeta: {
    sentryTrace: traceData["sentry-trace"],
    baggage: traceData["baggage"],
  },
}));

// Receiver — continue the trace
const { sentryTrace, baggage } = message._sentryMeta;

Sentry.continueTrace({ sentryTrace, baggage }, () => {
  return Sentry.startSpan({ name: "handleWebSocketMessage" }, () => {
    processMessage(message);
  });
});
```

### Head-Based Sampling

The originating (head) service makes the sampling decision. That decision propagates to all downstream services via `sentry-trace`. All services either all sample or all drop the trace — ensuring complete traces, never partial ones.

---

## Advanced Span APIs

### `continueTrace()` — Continue Incoming Trace

```typescript
// When receiving trace headers from a message queue, cron trigger, etc.
Sentry.continueTrace(
  {
    sentryTrace: incomingHeaders["sentry-trace"],
    baggage: incomingHeaders["baggage"],
  },
  () => {
    return Sentry.startSpan({ name: "processJob", op: "function" }, () =>
      doWork(),
    );
  },
);
```

### `startNewTrace()` — Force a New Trace

```typescript
// Break the distributed chain — start a completely independent trace
Sentry.startNewTrace(() => {
  return Sentry.startSpan({ name: "isolated-operation" }, () => doWork());
});
```

### `suppressTracing()` — Prevent Span Capture

```typescript
// Prevent spans inside this callback from being sent to Sentry
const result = Sentry.suppressTracing(() => {
  return fetch("/internal/health"); // No span created
});
```

### `getActiveSpan()`, `getRootSpan()`

```typescript
const span = Sentry.getActiveSpan();
if (span) {
  span.setAttribute("custom.key", "value");
  const root = Sentry.getRootSpan(span);
  console.log(Sentry.spanToJSON(root).name);
}
```

### `withActiveSpan()` — Run Code with a Specific Active Span

```typescript
const mySpan = Sentry.startInactiveSpan({ name: "background-task" });

await Sentry.withActiveSpan(mySpan, async (scope) => {
  scope.setTag("task.type", "email");
  await sendEmails(); // Errors associate with mySpan
});

mySpan.end();
```

### `forceTransaction` and `onlyIfParent`

```typescript
// Forces span to appear as root transaction in Sentry UI
Sentry.startSpan(
  { name: "background-job", op: "function", forceTransaction: true },
  () => runBackgroundJob(),
);

// Only creates span when an active parent exists (drops orphan spans)
Sentry.startSpan(
  { name: "optional-metric", onlyIfParent: true },
  () => measureSomething(),
);
```

### Browser Flat Span Hierarchy

In browsers, all child spans are attached flat to the root span by default. To opt into true nesting (use with care — can produce incorrect data with concurrent async operations):

```typescript
Sentry.init({
  parentSpanIsAlwaysRootSpan: false,
});
```

---

## Complete Config Example (All Three Runtimes)

```typescript
// instrumentation-client.ts (Browser)
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,

  integrations: [
    Sentry.browserTracingIntegration({
      shouldCreateSpanForRequest: (url) => !url.match(/\/health$/),
    }),
  ],

  tracesSampler: ({ name, inheritOrSampleWith }) => {
    if (name.includes("health")) return 0;
    if (name.includes("/checkout")) return 1.0;
    return inheritOrSampleWith(0.1);
  },

  tracePropagationTargets: [
    "localhost",
    /^https:\/\/api\.myapp\.com/,
  ],
});
```

```typescript
// sentry.server.config.ts (Node.js)
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,

  tracesSampler: ({ name, inheritOrSampleWith }) => {
    if (name.includes("healthcheck")) return 0;
    return inheritOrSampleWith(0.1);
  },
});
```

```typescript
// sentry.edge.config.ts (Edge)
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 0.1,
});
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transactions in Performance dashboard | Verify `tracesSampleRate` or `tracesSampler` is set; confirm it's set in all three runtime configs |
| Server Actions not traced | Wrap each with `withServerActionInstrumentation()`; it's not auto-instrumented |
| Distributed trace not linking frontend → backend | Add backend URL to `tracePropagationTargets`; verify `Access-Control-Allow-Headers: sentry-trace, baggage` on the backend |
| SSR page load not linked to server trace | This is automatic — verify both client and server use the same DSN |
| API requests missing `sentry-trace` header | Check CORS preflight — backend must allow `sentry-trace` and `baggage` |
| Transaction names show raw URLs (`/users/42`) | Use `beforeStartSpan` to parameterize: replace `/\d+/g` with `/<id>` |
| `tracesSampler` not working | When both `tracesSampler` and `tracesSampleRate` are set, `tracesSampler` wins — expected behavior |
| Spans missing after async gap (browser) | Browser uses flat hierarchy; use `startInactiveSpan` with explicit `parentSpan` across async boundaries |
| `tracePropagationTargets` port not matching | `"localhost"` won't match `localhost:3001` — use `"localhost:3001"` or a regex |
| High transaction volume | Use `tracesSampler` to return `0` for health checks; lower default rate with `inheritOrSampleWith(0.02)` |
| Server-only spans not appearing | Verify `instrumentation.ts` exports `onRequestError = Sentry.captureRequestError` and loads the server config |
