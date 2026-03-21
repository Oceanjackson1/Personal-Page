---
title: "Sentry Svelte SDK"
description: "Full Sentry SDK setup for Svelte and SvelteKit. Use when asked to 'add Sentry to Svelte', 'add Sentry to SvelteKit', 'install @sentry/sveltekit', or configure error monitoring, tracing, session replay, or logging for Svelte or SvelteKit applications."
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "svelte", "sdk"]
date: 2026-03-20
---

# Sentry Svelte SDK

Opinionated wizard that scans your project and guides you through complete Sentry setup for Svelte and SvelteKit.

## Invoke This Skill When

- User asks to "add Sentry to Svelte" or "set up Sentry" in a Svelte/SvelteKit app
- User wants error monitoring, tracing, session replay, or logging in Svelte or SvelteKit
- User mentions `@sentry/svelte`, `@sentry/sveltekit`, or Sentry SDK for Svelte

> **Note:** SDK versions and APIs below reflect current Sentry docs at time of writing (`@sentry/sveltekit` ≥10.8.0, SvelteKit ≥2.31.0).
> Always verify against [docs.sentry.io/platforms/javascript/guides/sveltekit/](https://docs.sentry.io/platforms/javascript/guides/sveltekit/) before implementing.

---

## Phase 1: Detect

Run these commands to understand the project before making any recommendations:

```bash
# Detect framework type
cat package.json | grep -E '"svelte"|"@sveltejs/kit"|"@sentry/svelte"|"@sentry/sveltekit"'

# Check for SvelteKit indicators
ls svelte.config.js svelte.config.ts vite.config.ts vite.config.js 2>/dev/null

# Check SvelteKit version (determines which setup pattern to use)
cat package.json | grep '"@sveltejs/kit"'

# Check if Sentry is already installed
cat package.json | grep '"@sentry/'

# Check existing hook files
ls src/hooks.client.ts src/hooks.client.js src/hooks.server.ts src/hooks.server.js \
   src/instrumentation.server.ts 2>/dev/null

# Detect logging libraries (Node side)
cat package.json | grep -E '"pino"|"winston"|"consola"'

# Detect if there's a backend (Go, Python, Ruby, etc.) in adjacent directories
ls ../backend ../server ../api 2>/dev/null
cat ../go.mod ../requirements.txt ../Gemfile 2>/dev/null | head -3
```

**What to determine:**

| Question | Impact |
|----------|--------|
| `@sveltejs/kit` in `package.json`? | SvelteKit path vs. plain Svelte path |
| SvelteKit ≥2.31.0? | Modern (`instrumentation.server.ts`) vs. legacy setup |
| `@sentry/sveltekit` already present? | Skip install, go straight to feature config |
| `vite.config.ts` present? | Source map upload via Vite plugin available |
| Backend directory found? | Trigger Phase 4 cross-link suggestion |

---

## Phase 2: Recommend

Present a concrete recommendation based on what you found. Don't ask open-ended questions — lead with a proposal:

**Recommended (core coverage):**
- ✅ **Error Monitoring** — always; auto-captures unhandled errors on client and server
- ✅ **Tracing** — SvelteKit has both client-side navigation spans and server-side request spans; always recommend
- ✅ **Session Replay** — recommended for user-facing SvelteKit apps (client-side only)

**Optional (enhanced observability):**
- ⚡ **Logging** — structured logs via `Sentry.logger.*`; recommend when app uses server-side logging or needs log-to-trace correlation

**Recommendation logic:**

| Feature | Recommend when... |
|---------|------------------|
| Error Monitoring | **Always** — non-negotiable baseline |
| Tracing | **Always for SvelteKit** (client + server); for plain Svelte when calling APIs |
| Session Replay | User-facing app, login flows, or checkout pages present |
| Logging | App already uses server-side logging, or structured log search is needed |

Propose: *"I recommend setting up Error Monitoring + Tracing + Session Replay. Want me to also add structured Logging?"*

---

## Phase 3: Guide

### Determine Setup Path

| Your project | Package | Setup complexity |
|-------------|---------|-----------------|
| SvelteKit (≥2.31.0) | `@sentry/sveltekit` | 5 files to create/modify |
| SvelteKit (<2.31.0) | `@sentry/sveltekit` | 3 files (init in hooks.server.ts) |
| Plain Svelte (no `@sveltejs/kit`) | `@sentry/svelte` | Single entry point |

---

### Path A: SvelteKit (Recommended — Modern, ≥2.31.0)

#### Option 1: Wizard (Recommended)

```bash
npx @sentry/wizard@latest -i sveltekit
```

The wizard walks you through login, org/project selection, and auth token setup interactively — no manual token creation needed. It then installs the SDK, creates all necessary files (client/server hooks, Vite plugin config), configures source map upload, and adds a `/sentry-example-page` for verification. Skip to [Verification](#verification) after running it.

#### Option 2: Manual Setup

**Step 1 — Install**

```bash
npm install @sentry/sveltekit --save
```

**Step 2 — `svelte.config.js`** — Enable instrumentation

```javascript
import adapter from "@sveltejs/adapter-auto";

const config = {
  kit: {
    adapter: adapter(),
    experimental: {
      instrumentation: { server: true },
      tracing: { server: true },
    },
  },
};

export default config;
```

**Step 3 — `src/instrumentation.server.ts`** — Server-side init (runs once at startup)

```typescript
import * as Sentry from "@sentry/sveltekit";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.SENTRY_ENVIRONMENT,
  release: process.env.SENTRY_RELEASE,

  sendDefaultPii: true,
  tracesSampleRate: 1.0,    // lower to 0.1–0.2 in production
  enableLogs: true,
});
```

**Step 4 — `src/hooks.client.ts`** — Client-side init

```typescript
import * as Sentry from "@sentry/sveltekit";

Sentry.init({
  dsn: import.meta.env.PUBLIC_SENTRY_DSN ?? import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,

  sendDefaultPii: true,
  tracesSampleRate: 1.0,

  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  enableLogs: true,
});

export const handleError = Sentry.handleErrorWithSentry();
```

**Step 5 — `src/hooks.server.ts`** — Server hooks (no init here in modern setup)

```typescript
import * as Sentry from "@sentry/sveltekit";
import { sequence } from "@sveltejs/kit/hooks";

export const handleError = Sentry.handleErrorWithSentry();

// sentryHandle() instruments incoming requests and creates root spans
export const handle = Sentry.sentryHandle();

// If you have other handle functions, compose with sequence():
// export const handle = sequence(Sentry.sentryHandle(), myAuthHandle);
```

**Step 6 — `vite.config.ts`** — Source maps (requires `SENTRY_AUTH_TOKEN`)

```typescript
import { sveltekit } from "@sveltejs/kit/vite";
import { sentrySvelteKit } from "@sentry/sveltekit";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    // sentrySvelteKit MUST come before sveltekit()
    sentrySvelteKit({
      org: process.env.SENTRY_ORG,
      project: process.env.SENTRY_PROJECT,
      authToken: process.env.SENTRY_AUTH_TOKEN,
    }),
    sveltekit(),
  ],
});
```

Add to `.env` (never commit):
```bash
SENTRY_AUTH_TOKEN=sntrys_...
SENTRY_ORG=my-org-slug
SENTRY_PROJECT=my-project-slug
```

---

### Path B: SvelteKit Legacy (<2.31.0 or `@sentry/sveltekit` <10.8.0)

Skip `instrumentation.server.ts` and `svelte.config.js` changes. Instead, put `Sentry.init()` directly in `hooks.server.ts`:

```typescript
// src/hooks.server.ts (legacy — init goes here)
import * as Sentry from "@sentry/sveltekit";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  enableLogs: true,
});

export const handleError = Sentry.handleErrorWithSentry();
export const handle = Sentry.sentryHandle();
```

`hooks.client.ts` and `vite.config.ts` are identical to the modern path.

---

### Path C: Plain Svelte (no SvelteKit)

**Install:**

```bash
npm install @sentry/svelte --save
```

**Configure in entry point** (`src/main.ts` or `src/main.js`) **before** mounting the app:

```typescript
import * as Sentry from "@sentry/svelte";
import App from "./App.svelte";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,

  sendDefaultPii: true,

  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  tracesSampleRate: 1.0,
  tracePropagationTargets: ["localhost", /^https:\/\/yourapi\.io/],
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  enableLogs: true,
});

const app = new App({ target: document.getElementById("app")! });
export default app;
```

**Optional: Svelte component tracking** (auto-injects tracking into all components):

```javascript
// svelte.config.js
import { withSentryConfig } from "@sentry/svelte";

export default withSentryConfig(
  { compilerOptions: {} },
  { componentTracking: { trackComponents: true } }
);
```

---

### For Each Agreed Feature

Walk through features one at a time. Load the reference file, follow its steps, then verify before moving on:

| Feature | Reference | Load when... |
|---------|-----------|-------------|
| Error Monitoring | `${SKILL_ROOT}/references/error-monitoring.md` | Always (baseline) |
| Tracing | `${SKILL_ROOT}/references/tracing.md` | API calls / distributed tracing needed |
| Session Replay | `${SKILL_ROOT}/references/session-replay.md` | User-facing app |
| Logging | `${SKILL_ROOT}/references/logging.md` | Structured logs / log-to-trace correlation |

For each feature: `Read ${SKILL_ROOT}/references/<feature>.md`, follow steps exactly, verify it works.

---

## SvelteKit File Summary

| File | Purpose | Modern | Legacy |
|------|---------|--------|--------|
| `src/instrumentation.server.ts` | Server `Sentry.init()` — runs once at startup | ✅ Required | ❌ |
| `src/hooks.client.ts` | Client `Sentry.init()` + `handleError` | ✅ Required | ✅ Required |
| `src/hooks.server.ts` | `handleError` + `sentryHandle()` (no init) | ✅ Required | ✅ Init goes here |
| `svelte.config.js` | Enable `experimental.instrumentation.server` | ✅ Required | ❌ |
| `vite.config.ts` | `sentrySvelteKit()` plugin for source maps | ✅ Recommended | ✅ Recommended |
| `.env` | `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT` | ✅ For source maps | ✅ For source maps |

---

## Configuration Reference

### Key `Sentry.init()` Options

| Option | Type | Default | Notes |
|--------|------|---------|-------|
| `dsn` | `string` | — | **Required.** Use env var; SDK is disabled when empty |
| `environment` | `string` | `"production"` | e.g., `"staging"`, `"development"` |
| `release` | `string` | — | e.g., `"my-app@1.2.3"` or git SHA |
| `sendDefaultPii` | `boolean` | `false` | Includes IP addresses and request headers |
| `tracesSampleRate` | `number` | — | 0–1; use `1.0` in dev, `0.1–0.2` in prod |
| `tracesSampler` | `function` | — | Per-transaction sampling; overrides `tracesSampleRate` |
| `tracePropagationTargets` | `(string\|RegExp)[]` | — | URLs that receive distributed tracing headers |
| `replaysSessionSampleRate` | `number` | — | Fraction of all sessions recorded (client only) |
| `replaysOnErrorSampleRate` | `number` | — | Fraction of error sessions recorded (client only) |
| `enableLogs` | `boolean` | `false` | Enable `Sentry.logger.*` API |
| `beforeSendLog` | `function` | — | Filter/modify logs before send |
| `debug` | `boolean` | `false` | Verbose SDK output to console |

### Server-Only Options (`instrumentation.server.ts` / `hooks.server.ts`)

| Option | Type | Notes |
|--------|------|-------|
| `serverName` | `string` | Hostname tag on server events |
| `includeLocalVariables` | `boolean` | Attach local vars to stack frames |
| `shutdownTimeout` | `number` | ms to flush events before process exit (default: 2000) |

### Adapter Compatibility

| Adapter | Support |
|---------|---------|
| `@sveltejs/adapter-auto` / adapter-vercel (Node) | ✅ Full |
| `@sveltejs/adapter-node` | ✅ Full |
| `@sveltejs/adapter-cloudflare` | ⚠️ Partial — requires extra setup |
| Vercel Edge Runtime | ❌ Not supported |

---

## Verification

After setup, trigger test events to confirm Sentry is receiving data:

```svelte
<!-- src/routes/sentry-test/+page.svelte -->
<script>
  import * as Sentry from "@sentry/sveltekit";
</script>

<button onclick={() => { throw new Error("Sentry client test"); }}>
  Test Client Error
</button>

<button onclick={() => Sentry.captureMessage("Sentry test message", "info")}>
  Test Message
</button>
```

```typescript
// src/routes/sentry-test/+server.ts
export const GET = () => {
  throw new Error("Sentry server test");
};
```

Check the Sentry dashboard:
- **Issues** → both errors should appear within seconds
- **Traces** → look for route-based transactions
- **Replays** → session recording visible after page interaction
- **Logs** → structured log entries (if logging enabled)

If nothing appears, set `debug: true` in `Sentry.init()` and check the browser/server console for SDK output.

---

## Phase 4: Cross-Link

After completing Svelte/SvelteKit setup, check for a companion backend missing Sentry coverage:

```bash
# Look for backend in adjacent directories
ls ../backend ../server ../api ../go ../python 2>/dev/null
cat ../go.mod 2>/dev/null | head -3
cat ../requirements.txt ../pyproject.toml 2>/dev/null | head -3
cat ../Gemfile 2>/dev/null | head -3
```

If a backend exists without Sentry configured, suggest the matching skill:

| Backend detected | Suggest skill |
|-----------------|--------------|
| Go (`go.mod`) | `sentry-go-sdk` |
| Python (`requirements.txt`, `pyproject.toml`) | `sentry-python-sdk` |
| Ruby (`Gemfile`) | `sentry-ruby-sdk` |
| Node.js (Express, Fastify, etc.) | Use `@sentry/node` — see [docs.sentry.io/platforms/javascript/guides/express/](https://docs.sentry.io/platforms/javascript/guides/express/) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Set `debug: true`, check DSN, open browser console for SDK errors |
| Source maps not working | Run `npm run build` (not `dev`), verify `SENTRY_AUTH_TOKEN` is set |
| Server errors not captured | Ensure `handleErrorWithSentry()` is exported from `hooks.server.ts` |
| Client errors not captured | Ensure `handleErrorWithSentry()` is exported from `hooks.client.ts` |
| Session replay not recording | Confirm `replayIntegration()` is in client init only (never server) |
| `sentryHandle()` + other handles not composing | Wrap with `sequence(Sentry.sentryHandle(), myHandle)` |
| Ad-blocker blocking events | Set `tunnel: "/sentry-tunnel"` and add a server-side relay endpoint |
| SvelteKit instrumentation not activating | Confirm `experimental.instrumentation.server: true` in `svelte.config.js` |
| Cloudflare adapter issues | Consult [docs.sentry.io/platforms/javascript/guides/sveltekit/](https://docs.sentry.io/platforms/javascript/guides/sveltekit/) for adapter-specific notes |
| `wrapLoadWithSentry` / `wrapServerLoadWithSentry` errors | These are legacy wrappers — remove them; `sentryHandle()` instruments load functions automatically in ≥10.8.0 |

---

## Reference: Error Monitoring

# Error Monitoring — Sentry Svelte/SvelteKit SDK

> Minimum SDK: `@sentry/sveltekit` ≥7.0.0+ / `@sentry/svelte` ≥7.0.0+

---

## How Automatic Capture Works

| Layer | Mechanism | Fires when... |
|-------|-----------|---------------|
| **Client (both)** | `globalHandlersIntegration` | `window.onerror`, unhandled `Promise` rejections |
| **Client (both)** | `browserApiErrorsIntegration` | Errors thrown in `setTimeout`, `setInterval`, `requestAnimationFrame` |
| **Server (SvelteKit)** | `handleErrorWithSentry()` in `hooks.server.ts` | Any unhandled error in a server hook, load function, or route handler |
| **Server (SvelteKit)** | `sentryHandle()` | Instruments incoming requests; captures errors from the request pipeline |
| **Client (SvelteKit)** | `handleErrorWithSentry()` in `hooks.client.ts` | Any unhandled navigation or client-side error SvelteKit surfaces |

No configuration beyond the `Sentry.init()` call is required for baseline error capture.

---

## SvelteKit Error Hooks

### `hooks.client.ts`

```typescript
import * as Sentry from "@sentry/sveltekit";

Sentry.init({ dsn: import.meta.env.VITE_SENTRY_DSN, sendDefaultPii: true });

// Sentry captures first; your handler runs after
const myErrorHandler = ({ error, event }: { error: unknown; event: unknown }) => {
  console.error("Client error:", error);
};

export const handleError = Sentry.handleErrorWithSentry(myErrorHandler);

// Works with no argument too:
// export const handleError = Sentry.handleErrorWithSentry();
```

### `hooks.server.ts`

```typescript
import * as Sentry from "@sentry/sveltekit";
import { sequence } from "@sveltejs/kit/hooks";

// Sentry.init() is in instrumentation.server.ts (modern) or here (legacy)

const myErrorHandler = ({ error, event }: { error: unknown; event: unknown }) => {
  console.error("Server error:", error);
};

export const handleError = Sentry.handleErrorWithSentry(myErrorHandler);

// sentryHandle() instruments requests and creates root spans
export const handle = Sentry.sentryHandle();

// Composing multiple handles:
// export const handle = sequence(Sentry.sentryHandle(), authHandle, logHandle);
```

### `handleErrorWithSentry()` callback signature

```typescript
export const handleError = Sentry.handleErrorWithSentry(
  (input: {
    error: unknown;
    event: RequestEvent | NavigationEvent;
    status?: number;
    message?: string;
  }) => {
    // Your logic runs AFTER Sentry has already captured the error
  }
);
```

---

## Manual Error Capture

```typescript
import * as Sentry from "@sentry/sveltekit"; // or "@sentry/svelte"

// Capture an Error object
try {
  await riskyOperation();
} catch (err) {
  Sentry.captureException(err);
}

// Capture with extra context
try {
  await riskyOperation();
} catch (err) {
  Sentry.captureException(err, {
    tags: { feature: "checkout", region: "eu" },
    extra: { cartId: "abc-123", itemCount: 3 },
    level: "error",   // "fatal" | "error" | "warning" | "info" | "debug"
  });
}

// Plain message (not tied to an exception)
Sentry.captureMessage("User exceeded rate limit", "warning");

// Isolated scope — doesn't pollute global state
Sentry.withScope((scope) => {
  scope.setTag("component", "PaymentForm");
  scope.setUser({ id: "42", email: "user@example.com" });
  Sentry.captureException(new Error("Payment failed"));
});
```

---

## Context Enrichment

### User Context

```typescript
// Set globally — persists until cleared
Sentry.setUser({
  id: "user-123",
  email: "jane@example.com",
  username: "jdoe",
  ip_address: "{{ auto }}",  // auto-infer from request
  plan: "enterprise",        // custom fields accepted
});

// Clear on logout
Sentry.setUser(null);
```

### Tags (searchable, indexed)

```typescript
Sentry.setTag("release.channel", "beta");
Sentry.setTags({
  "feature.flag": "new-checkout",
  region: "us-east-1",
  version: "2.1.0",
});
```

Key constraints: ≤32 chars, alphanumeric + `_`, `.`, `:`, `-`. Value: ≤200 chars, no newlines.

### Context Objects (structured, non-indexed)

```typescript
Sentry.setContext("cart", {
  itemCount: 3,
  totalAmount: 99.99,
  promoCode: "SAVE20",
});

// Clear context
Sentry.setContext("cart", null);
```

### Extra Data (simple key-value)

```typescript
Sentry.setExtra("requestBody", { amount: 99.99, currency: "USD" });
Sentry.setExtras({ cartItems: 3, promoCode: "SAVE20" });
```

### `initialScope` (set once at init)

```typescript
Sentry.init({
  dsn: "...",
  initialScope: {
    tags: { appVersion: "1.0.0", deploymentId: "abc123" },
    user: { id: "anonymous" },
  },
  // Or as a callback:
  // initialScope: (scope) => { scope.setTag("buildId", BUILD_ID); return scope; },
});
```

---

## Breadcrumbs

```typescript
// Manual breadcrumb
Sentry.addBreadcrumb({
  message: "User submitted checkout form",
  category: "ui.click",
  level: "info",   // "fatal"|"error"|"warning"|"log"|"info"|"debug"
  type: "user",    // "default"|"debug"|"error"|"info"|"navigation"|"http"|"query"|"ui"|"user"
  data: { formId: "checkout-v2", itemCount: 3 },
});

// Auth breadcrumb
Sentry.addBreadcrumb({
  category: "auth",
  message: "Authenticated user " + user.email,
  level: "info",
});
```

**Auto-captured breadcrumbs (browser):** DOM clicks, keyboard events, XHR/fetch requests, console calls, navigation changes.

### Filter breadcrumbs with `beforeBreadcrumb`

```typescript
Sentry.init({
  beforeBreadcrumb(breadcrumb, hint) {
    // Drop verbose console breadcrumbs
    if (breadcrumb.category === "console") return null;
    // Sanitize navigation data
    if (breadcrumb.category === "navigation" && breadcrumb.data?.to) {
      breadcrumb.data.to = breadcrumb.data.to.replace(/\/user\/\d+/, "/user/[id]");
    }
    return breadcrumb;
  },
});
```

---

## `beforeSend` — Filter and Scrub Events

```typescript
Sentry.init({
  // Drop known noise
  ignoreErrors: [
    "ResizeObserver loop limit exceeded",
    /^Network Error$/,
    /ChunkLoadError/,
  ],

  // Only capture errors from your own scripts
  allowUrls: [/https:\/\/myapp\.com/],

  // Scrub PII, drop by condition
  beforeSend(event, hint) {
    // Drop non-Error objects
    if (hint.originalException && !(hint.originalException instanceof Error)) {
      return null;
    }
    // Scrub email from user context
    if (event.user?.email) {
      event.user.email = "[filtered]";
    }
    // Drop 404 errors
    if (event.tags?.statusCode === "404") {
      return null;
    }
    return event;
  },
});
```

---

## Svelte Component Tracking (`@sentry/svelte` only)

Component tracking wraps Svelte's lifecycle hooks and emits spans for each component's `init` and `update` phases.

### Automatic (preprocessor — all components)

```javascript
// svelte.config.js
import { withSentryConfig } from "@sentry/svelte";

export default withSentryConfig(
  { compilerOptions: {} },
  {
    componentTracking: {
      trackComponents: true,   // true = all, or array: ["Navbar", "LoginForm"]
      trackInit: true,         // emit ui.svelte.init spans
      trackUpdates: true,      // emit ui.svelte.update spans
    },
  }
);
```

Spans emitted:
- `ui.svelte.init` — component instantiation → `onMount`
- `ui.svelte.update` — `beforeUpdate` → `afterUpdate`

### Manual (per-component)

```svelte
<script>
  import * as Sentry from "@sentry/svelte";

  Sentry.trackComponent({
    trackInit: true,
    trackUpdates: false,
    componentName: "PaymentForm",  // optional; auto-detected if omitted
  });
</script>
```

---

## SvelteKit `+error.svelte` Integration

SvelteKit renders `+error.svelte` for handled errors. You can surface the Sentry event ID in the error page for user feedback:

```svelte
<!-- src/routes/+error.svelte -->
<script>
  import { page } from "$app/stores";
  import * as Sentry from "@sentry/sveltekit";

  // Show user feedback dialog tied to the last captured event
  function showFeedback() {
    const eventId = Sentry.lastEventId();
    if (eventId) {
      Sentry.showReportDialog({ eventId });
    }
  }
</script>

<h1>{$page.status}: {$page.error?.message}</h1>
<button onclick={showFeedback}>Report this issue</button>
```

---

## Error Boundaries (Svelte 5+)

> Requires Svelte 5 + `@sveltejs/kit` ≥2.x. Catches errors thrown in child components before they propagate to the page.

`<svelte:boundary>` prevents a component subtree from crashing the whole page and lets you report the error to Sentry and optionally display a fallback UI:

```svelte
<script>
  import * as Sentry from "@sentry/sveltekit";
</script>

<svelte:boundary onerror={(error, reset) => {
  Sentry.captureException(error);
}}>
  <RiskyComponent />

  {#snippet failed(error, reset)}
    <p>Something went wrong.</p>
    <button onclick={reset}>Try again</button>
  {/snippet}
</svelte:boundary>
```

**Tips:**
- `onerror` fires synchronously before Svelte tears down the subtree — safe to call `captureException` here
- `reset` re-mounts the boundary subtree; pair it with `Sentry.lastEventId()` + `Sentry.showReportDialog()` for user feedback
- Nest multiple boundaries to isolate independent widgets — a failure in one won't affect others
- Works in both client and server-rendered pages; server-side errors are still captured via `hooks.server.ts`

```svelte
<!-- With user feedback dialog on reset -->
<svelte:boundary onerror={(error) => {
  Sentry.captureException(error);
}}>
  <DataWidget />

  {#snippet failed(error, reset)}
    <button onclick={() => {
      const eventId = Sentry.lastEventId();
      if (eventId) Sentry.showReportDialog({ eventId });
      reset();
    }}>Report &amp; retry</button>
  {/snippet}
</svelte:boundary>
```

---

## Scopes: `withScope` vs Persistent Context

> Minimum SDK: `@sentry/sveltekit` ≥8.0.0 for isolation scopes; ≥10.32.0 for `getGlobalScope`/`getIsolationScope`

| API | Lifetime | Use case |
|-----|----------|----------|
| `Sentry.withScope(fn)` | Isolated to callback | One-off context for a single capture |
| `Sentry.getIsolationScope()` | Per-request (SvelteKit server) | Persistent context scoped to one request |
| `Sentry.getGlobalScope()` | Entire process lifetime | App-wide context (version tags, env) |

> **Note:** `Sentry.configureScope()` is deprecated since SDK v8. Use `getIsolationScope()` or `getGlobalScope()` instead.

```typescript
// withScope — temporary, doesn't affect subsequent events
Sentry.withScope((scope) => {
  scope.setTag("component", "checkout");
  Sentry.captureException(err);  // only this event gets the tag
});

// Set persistent scope data (per-request in SvelteKit server)
const scope = Sentry.getIsolationScope();
scope.setTag("tenant", session.tenantId);
scope.setUser({ id: session.userId });

// App-wide context (set once at startup)
const globalScope = Sentry.getGlobalScope();
globalScope.setTag("app.version", "1.0.0");
```

---

## Svelte vs SvelteKit: Key Differences

| Concern | Standalone Svelte | SvelteKit |
|---------|-------------------|-----------|
| Error hook files | None — errors via `window.onerror` only | `hooks.client.ts` + `hooks.server.ts` |
| Server-side errors | N/A (client-only) | Auto via `handleErrorWithSentry()` |
| Component errors | `window.onerror` catches uncaught ones | Same + SvelteKit route error handling |
| `+error.svelte` | N/A | Add `Sentry.lastEventId()` for feedback |
| Scope per request | N/A | SvelteKit isolation scope per request |

---

## Best Practices

- Export `handleError = Sentry.handleErrorWithSentry()` from **both** hook files in SvelteKit — server errors are missed if only one is set
- Set `sendDefaultPii: true` to capture user IP and request headers automatically
- Use `Sentry.withScope()` for one-off context, `Sentry.getIsolationScope()` / `Sentry.getGlobalScope()` for persistent context
- Scrub PII in `beforeSend` if `sendDefaultPii: true` is set but specific fields must be hidden
- Set `debug: true` during development to verify events are being captured

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server errors not appearing | Confirm `handleErrorWithSentry()` is exported from `hooks.server.ts` |
| Client errors not appearing | Confirm `handleErrorWithSentry()` is exported from `hooks.client.ts` |
| `ignoreErrors` patterns not working | Use `RegExp` for patterns with special chars; string values are treated as regex |
| `beforeSend` returning `null` but events still sent | Check that `beforeSendTransaction` is not what fires (different hook) |
| Component tracking not emitting spans | Ensure `withSentryConfig` wraps the config in `svelte.config.js`; requires tracing enabled |
| `Sentry.lastEventId()` returns undefined | Only populated after `captureException`/`captureMessage` or automatic capture |
| Events appear without user context | Call `Sentry.setUser()` after authentication, not inside `Sentry.init()` |

---

## Reference: Logging

# Logging — Sentry Svelte/SvelteKit SDK

> Minimum SDK: `@sentry/sveltekit` ≥9.41.0+ / `@sentry/svelte` ≥9.41.0+ for `Sentry.logger` API  
> `consoleLoggingIntegration()`: requires ≥10.13.0+  
> Scope-based attribute setters (`getIsolationScope`, `getGlobalScope`): requires ≥10.32.0+

> ⚠️ **Not available via CDN/loader snippet** — NPM install required.

---

## Enabling Logs

`enableLogs` is opt-in. Add it to every `Sentry.init()` call where you want logs captured.

### SvelteKit — both files

```typescript
// src/instrumentation.server.ts (or hooks.server.ts for legacy)
import * as Sentry from "@sentry/sveltekit";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  enableLogs: true,
});
```

```typescript
// src/hooks.client.ts
import * as Sentry from "@sentry/sveltekit";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  enableLogs: true,
});

export const handleError = Sentry.handleErrorWithSentry();
```

### Standalone Svelte — main.ts

```typescript
import * as Sentry from "@sentry/svelte";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  enableLogs: true,
});
```

---

## Logger API — Six Levels

```typescript
import * as Sentry from "@sentry/sveltekit"; // or "@sentry/svelte"

Sentry.logger.trace("Entering processOrder", { fn: "processOrder", orderId: "ord_1" });
Sentry.logger.debug("Cache lookup", { key: "user:123", hit: false });
Sentry.logger.info("Order created", { orderId: "order_456", total: 99.99 });
Sentry.logger.warn("Rate limit approaching", { current: 95, max: 100 });
Sentry.logger.error("Payment failed", { reason: "card_declined", userId: "u_1" });
Sentry.logger.fatal("Database unavailable", { host: "db-primary", port: 5432 });
```

| Level | Intent |
|-------|--------|
| `trace` | Fine-grained debugging, high-volume — filter aggressively in production |
| `debug` | Development diagnostics |
| `info` | Normal operations, business milestones |
| `warn` | Degraded state, near-limit conditions |
| `error` | Failures requiring attention |
| `fatal` | Critical failures, system-down conditions |

**Attribute value types:** `string`, `number`, `boolean` only.

---

## Parameterized Messages (`logger.fmt`)

Use `logger.fmt` tagged template literals to bind variables as **structured, searchable attributes** in Sentry:

```typescript
const userId = "user_123";
const productName = "Widget Pro";
const amount = 49.99;

Sentry.logger.info(
  Sentry.logger.fmt`User ${userId} purchased ${productName} for $${amount}`
);
```

Results in:
```
message.template:     "User %s purchased %s for $%s"
message.parameter.0:  "user_123"
message.parameter.1:  "Widget Pro"
message.parameter.2:  49.99
```

This allows filtering in Sentry by any individual parameter value, not just the full message string.

---

## Console Capture Integration

Automatically forwards `console.*` calls to Sentry as structured logs. Requires SDK ≥10.13.0.

```typescript
Sentry.init({
  dsn: "...",
  enableLogs: true,
  integrations: [
    Sentry.consoleLoggingIntegration({
      levels: ["log", "warn", "error"],  // which console levels to forward
    }),
  ],
});

// These are now automatically sent to Sentry:
console.log("User action", { userId: 123, action: "checkout" });
console.warn("High memory usage", 85, "%");
console.error("Fetch failed", new Error("timeout"));
```

`console.log("Text", 123, true)` → `message.parameter.0 = 123`, `message.parameter.1 = true`

### Consola integration (SvelteKit server-side)

For apps using the `consola` logging library (common in SvelteKit SSR):

```typescript
// SDK >= 10.12.0
import consola from "consola";
import * as Sentry from "@sentry/sveltekit";

const reporter = Sentry.createConsolaReporter();
consola.addReporter(reporter);
```

---

## Scope-Based Automatic Attributes (SDK ≥10.32.0)

Attributes set on scopes are **automatically added to all subsequent logs** within that scope — no need to repeat them on every log call.

### Global scope (process lifetime)

```typescript
// Set once at startup — applies everywhere, client and server
Sentry.getGlobalScope().setAttributes({
  service: "checkout-service",
  version: "2.1.0",
  region: "us-east-1",
});
```

### Isolation scope (per-request in SvelteKit)

SvelteKit creates a new isolation scope per server request. Set per-request context here:

```typescript
// src/hooks.server.ts — enrich every server log with request context
import * as Sentry from "@sentry/sveltekit";

export const handle = sequence(
  Sentry.sentryHandle(),
  async ({ event, resolve }) => {
    Sentry.getIsolationScope().setAttributes({
      org_id: event.locals.user?.orgId,
      user_tier: event.locals.user?.tier,
      request_id: event.request.headers.get("x-request-id") ?? undefined,
    });
    return resolve(event);
  }
);
```

### Current scope (narrowest, single operation)

```typescript
Sentry.withScope((scope) => {
  scope.setAttribute("order_id", "ord_789");
  scope.setAttribute("payment_method", "stripe");
  Sentry.logger.info("Processing payment", { amount: 49.99 });
  // order_id and payment_method are included in this log only
});
```

---

## Log Filtering with `beforeSendLog`

```typescript
Sentry.init({
  dsn: "...",
  enableLogs: true,
  beforeSendLog: (log) => {
    // Drop debug logs in production
    if (log.level === "debug" || log.level === "trace") return null;

    // Scrub sensitive attribute keys
    if (log.attributes?.password) {
      delete log.attributes.password;
    }
    if (log.attributes?.["credit_card"]) {
      log.attributes["credit_card"] = "[REDACTED]";
    }

    // Drop health-check noise
    if (log.attributes?.["http.target"] === "/health") return null;

    return log;
  },
});
```

---

## Auto-Generated Attributes

The SDK adds these to every log without any developer action:

| Attribute | Source | Notes |
|-----------|--------|-------|
| `environment` | `Sentry.init({ environment })` | — |
| `release` | `Sentry.init({ release })` | — |
| `sdk.name`, `sdk.version` | SDK internals | — |
| `browser.name`, `browser.version` | User-Agent | Client-side only |
| `user.id`, `user.name`, `user.email` | `Sentry.setUser()` | When `sendDefaultPii: true` |
| `sentry.trace.parent_span_id` | Active tracing span | If tracing is enabled |
| `sentry.replay_id` | Active replay session | If Session Replay is enabled |
| `message.template`, `message.parameter.X` | `logger.fmt` usage | — |
| `sentry.origin` | Integration-generated logs | — |

---

## Trace + Log Correlation

When tracing is enabled alongside logging, logs are **automatically linked** to the current trace:

```typescript
Sentry.init({
  dsn: "...",
  enableLogs: true,
  tracesSampleRate: 1.0,
  integrations: [Sentry.browserTracingIntegration()],
});

// Inside an active span, logs get sentry.trace.parent_span_id automatically
await Sentry.startSpan({ name: "process-order", op: "task" }, async () => {
  Sentry.logger.info("Validating cart", { cartId: "cart_abc" });
  // ^ this log is linked to the "process-order" span in Sentry UI
  await validateCart();
  Sentry.logger.info("Payment initiated", { gateway: "stripe" });
});
```

Navigate from log → parent span, or from span → correlated logs, in the Sentry UI.

---

## SvelteKit Server-Side Logging

On the server side, `enableLogs: true` in `instrumentation.server.ts` enables `Sentry.logger.*` in:
- `hooks.server.ts` handle functions
- `+page.server.ts` / `+layout.server.ts` load functions
- API routes (`+server.ts`)

```typescript
// src/routes/api/orders/+server.ts
import * as Sentry from "@sentry/sveltekit";
import { json } from "@sveltejs/kit";

export const POST = async ({ request }) => {
  const body = await request.json();

  Sentry.logger.info(
    Sentry.logger.fmt`Creating order for user ${body.userId}`,
  );

  try {
    const order = await createOrder(body);
    Sentry.logger.info("Order created", { orderId: order.id, total: order.total });
    return json(order, { status: 201 });
  } catch (err) {
    Sentry.logger.error("Order creation failed", {
      userId: body.userId,
      reason: (err as Error).message,
    });
    throw err;
  }
};
```

---

## Svelte vs SvelteKit: Key Differences

| Concern | Standalone Svelte | SvelteKit |
|---------|-------------------|-----------|
| `enableLogs` location | Single `main.ts` init | Both `hooks.client.ts` + `instrumentation.server.ts` |
| Server-side logging | ❌ N/A | ✅ Full — `Sentry.logger.*` in any server code |
| Isolation scope per request | ❌ N/A | ✅ Set in `hooks.server.ts` for per-request context |
| `consoleLoggingIntegration` | Single init | Both client and server inits |
| `consola` reporter | N/A (client-only) | Server hooks or load functions |
| Trace correlation | Client spans only | Client + server spans |

---

## Best Practices

- Add `enableLogs: true` to **both** `hooks.client.ts` and `instrumentation.server.ts` in SvelteKit — logging is not shared between the two init calls
- Use `Sentry.logger.fmt` for any log that includes a variable — enables search by value in Sentry
- Set global attributes (`getGlobalScope().setAttributes()`) for service-level metadata (service name, version, region)
- Use `getIsolationScope().setAttributes()` in `hooks.server.ts` to enrich all logs for a given request
- Use `beforeSendLog` to drop `trace`/`debug` logs in production to control volume
- Avoid logging raw sensitive data even with `beforeSendLog` — filter at the call site when possible

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing in Sentry | Check `enableLogs: true` is set; logs require SDK ≥9.41.0 |
| Server logs missing, client logs present | Add `enableLogs: true` to `instrumentation.server.ts` (separate init from client) |
| `logger.fmt` not creating parameters | Ensure you're calling `Sentry.logger.fmt` as a tagged template — not a function call |
| Too many log entries (noise) | Use `beforeSendLog` to filter by level; increase `trace`/`debug` filter in production |
| Logs not linked to traces | Ensure tracing is enabled and active span exists when log is called |
| `consoleLoggingIntegration` requires upgrade | Upgrade to `@sentry/sveltekit` ≥10.13.0 |
| Scope attributes not appearing | Upgrade to ≥10.32.0 for `getGlobalScope`/`getIsolationScope` APIs |
| Log attributes contain `undefined` | Sentry only accepts `string | number | boolean` attribute values — filter undefined before passing |

---

## Reference: Session Replay

# Session Replay — Sentry Svelte/SvelteKit SDK

> Minimum SDK: `@sentry/sveltekit` ≥7.27.0+ / `@sentry/svelte` ≥7.27.0+  
> `replayCanvasIntegration()`: requires `@sentry/sveltekit` ≥7.48.0+

> ⚠️ **Client-only feature.** Never add `replayIntegration()` to `hooks.server.ts` or `instrumentation.server.ts`.

---

## Setup

Session Replay is bundled in `@sentry/sveltekit` and `@sentry/svelte` — no separate package needed.

### SvelteKit — hooks.client.ts

```typescript
import * as Sentry from "@sentry/sveltekit";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,

  // Sample rates live on init, NOT on the integration
  replaysSessionSampleRate: 0.1,   // record 10% of all sessions
  replaysOnErrorSampleRate: 1.0,   // record 100% of sessions that encounter an error

  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,      // default: true
      blockAllMedia: true,    // default: true
    }),
  ],
});

export const handleError = Sentry.handleErrorWithSentry();
```

### Standalone Svelte — main.ts

```typescript
import * as Sentry from "@sentry/svelte";
import App from "./App.svelte";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,

  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,

  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],
});

const app = new App({ target: document.getElementById("app")! });
export default app;
```

---

## Sample Rates

| Option | Location | Behavior |
|--------|----------|----------|
| `replaysSessionSampleRate` | `Sentry.init({})` | Fraction of all sessions recorded from start |
| `replaysOnErrorSampleRate` | `Sentry.init({})` | Fraction of error sessions — includes ~60s of replay before the error |

Recommended values by traffic volume:

| Volume | `replaysSessionSampleRate` | `replaysOnErrorSampleRate` |
|--------|---------------------------|---------------------------|
| High (100k+ sessions/day) | `0.01` | `1.0` |
| Medium (10k–100k/day) | `0.1` | `1.0` |
| Low (<10k/day) | `0.25` | `1.0` |
| Errors-only strategy | `0` | `1.0` |

"Errors-only" (`replaysSessionSampleRate: 0`, `replaysOnErrorSampleRate: 1.0`) minimizes overhead by not recording sessions unless an error occurs.

---

## Core `replayIntegration()` Options

### Recording Control

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `stickySession` | `boolean` | `true` | Persist session across page refreshes |
| `minReplayDuration` | `number` | `5000` | Min ms before a session-based replay is sent |
| `maxReplayDuration` | `number` | `3600000` | Max replay length (1 hour hard cap) |
| `workerUrl` | `string` | — | Self-host the compression Web Worker |

### Mutation Limits (DOM thrash protection)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `mutationLimit` | `number` | `10000` | Stop recording after N DOM mutations |
| `mutationBreadcrumbLimit` | `number` | `750` | Emit a warning breadcrumb after N mutations |

```typescript
Sentry.replayIntegration({
  mutationBreadcrumbLimit: 1000,
  mutationLimit: 1500,
});
```

---

## Privacy and Masking

Replay defaults to **privacy-first**: all text is masked and all media is blocked before a single line of config is written.

### Default behavior

| Element type | Default action |
|-------------|----------------|
| All text content | Replaced with `*` (length-preserving) |
| All inputs | Values replaced with `*` |
| `img`, `svg`, `video`, `audio`, `picture`, `embed`, `map`, `object` | Replaced with same-size placeholder box |

### Global masking overrides

```typescript
Sentry.replayIntegration({
  maskAllText: true,     // default: true — set false to unmask everything
  maskAllInputs: true,   // default: true
  blockAllMedia: true,   // default: true

  // Custom masking function (override default * replacement)
  maskFn: (text) => "█".repeat(text.length),
});
```

### Selector-based fine-grained control

```typescript
Sentry.replayIntegration({
  // Additional selectors to mask/block (additive to defaults)
  mask: [".sensitive-field", "[data-pii]"],
  block: [".payment-widget", "#credit-card-iframe"],
  ignore: ["#search-input"],         // ignore input value changes for this field

  // UNBLOCK specific elements from maskAllText=true
  unmask: [".username-display", ".public-label"],

  // UNBLOCK specific elements from blockAllMedia=true
  unblock: [".product-thumbnail", ".avatar-image"],
});
```

### HTML attribute approach (zero-config)

Apply directly in Svelte markup — no JS config change needed:

```svelte
<!-- Mask text content -->
<p data-sentry-mask>Sensitive content</p>
<p class="sentry-mask">Also masked</p>

<!-- Block entire element (replaced with placeholder) -->
<div data-sentry-block>Payment widget</div>
<div class="sentry-block">Also blocked</div>

<!-- Ignore input value changes -->
<input data-sentry-ignore type="text" />
<input class="sentry-ignore" />
```

Attribute selectors (`data-sentry-*`) are automatically recognized by the SDK. CSS classes require these to be listed in the integration options for SDK v8+:

```typescript
Sentry.replayIntegration({
  unmask: [".sentry-unmask, [data-sentry-unmask]"],
  unblock: [".sentry-unblock, [data-sentry-unblock]"],
});
```

---

## Network Capture

By default, only URL, method, status code, and response size are recorded for network requests. To capture headers and bodies, opt in per URL:

```typescript
Sentry.replayIntegration({
  networkDetailAllowUrls: [
    window.location.origin,          // same-origin requests
    "api.example.com",               // substring match
    /^https:\/\/api\.example\.com/,  // regex match
  ],
  networkDetailDenyUrls: [
    "https://analytics.third-party.com",  // takes precedence over allow
  ],

  networkCaptureBodies: true,                    // capture req/res bodies (default: true when URLs allowed)
  networkRequestHeaders: ["Cache-Control", "X-Request-ID"],
  networkResponseHeaders: ["Referrer-Policy", "X-Response-Time"],
});
```

Constraints:
- Body truncation limit: **150,000 characters** max
- Default captured headers: `Content-Type`, `Content-Length`, `Accept`
- No bodies/extra headers captured unless URLs are in `networkDetailAllowUrls`

---

## Canvas Recording

Requires a second integration:

```typescript
Sentry.init({
  integrations: [
    Sentry.replayIntegration(),
    Sentry.replayCanvasIntegration(),
  ],
});
```

### Manual snapshot mode

Use when canvas content changes outside normal render cycles:

```typescript
Sentry.init({
  integrations: [
    Sentry.replayIntegration(),
    Sentry.replayCanvasIntegration({ enableManualSnapshot: true }),
  ],
});

// Trigger snapshot manually when needed
const canvasIntegration = Sentry.getClient()?.getIntegrationByName("ReplayCanvas");
canvasIntegration?.snapshot(canvasElement);
```

---

## Lazy Loading Replay

Defer loading the replay bundle to improve initial page load performance:

```typescript
// Initialize without replay
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  integrations: [],
});

// Load on demand (e.g., after login, or on idle)
async function enableReplay() {
  const { replayIntegration } = await import("@sentry/sveltekit");
  Sentry.addIntegration(
    replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    })
  );
}
```

---

## Event Filtering

```typescript
Sentry.replayIntegration({
  // Filter/drop individual recording events before they are buffered
  beforeAddRecordingEvent: (event) => {
    // Drop debug console entries from replay
    if (event.data?.payload?.level === "debug") return null;
    return event;
  },

  // Control which errors trigger error-rate sampling
  beforeErrorSampling: (event) => {
    // Don't start replay for NetworkErrors
    return event.exception?.values?.[0]?.type !== "NetworkError";
  },

  // Disable slow/rage-click detection on noisy elements
  slowClickIgnoreSelectors: [".loading-spinner", "#carousel"],
});
```

---

## SvelteKit-Specific Considerations

| Topic | Note |
|-------|-------|
| Server-side rendering | Replay records the **browser DOM** after hydration, not the raw SSR HTML |
| Navigation tracking | SvelteKit client-side navigations are recorded as replay navigation breadcrumbs |
| `+error.svelte` pages | Errors triggering error pages are captured; replay buffers the preceding session |
| Ad-blocker bypass | Set `tunnel: "/sentry-tunnel"` to prevent replay data from being blocked |
| Cloudflare adapter | Replay is client-only; no adapter-specific concerns |

---

## CSP Requirements

If using a strict Content Security Policy, add:

```
worker-src 'self' blob:;
child-src 'self' blob:;
```

The SDK uses a Web Worker (`blob:` URL) for compression.

### Self-hosting the worker

```typescript
Sentry.replayIntegration({
  workerUrl: "/assets/sentry-replay-worker.min.js",
});
```

Download the worker from the `@sentry/replay` package `worker/` directory and serve it from your own origin.

---

## Performance Considerations

- Compression runs in a **Web Worker** — minimal main-thread impact
- `mutationLimit` protects against DOM-heavy frameworks that trigger thousands of mutations
- Network body capture is opt-in per URL — no performance cost without `networkDetailAllowUrls`
- Lazy loading (`Sentry.addIntegration()`) reduces initial bundle size by ~50KB gzipped
- "Errors-only" strategy (`replaysSessionSampleRate: 0`) has near-zero overhead when no error occurs

---

## Best Practices

- Keep `maskAllText: true` and `blockAllMedia: true` as defaults — opt individual elements out via `unmask`/`unblock` or `data-sentry-unmask`/`data-sentry-unblock`
- Use `networkDetailAllowUrls` with your own API domains only — never include third-party analytics or payment processors
- Set `replaysOnErrorSampleRate: 1.0` so you never miss replay for an error session
- Lazy-load replay for unauthenticated pages where user consent or performance is critical
- Add `slowClickIgnoreSelectors` for loading states to avoid false rage-click detection

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Replay not recording | Confirm `replayIntegration()` is in `hooks.client.ts` — never in `hooks.server.ts` |
| All text shown as `*` | Expected with `maskAllText: true`; add `data-sentry-unmask` to elements that are safe to show |
| Replay missing after error | Check `replaysOnErrorSampleRate` is > 0; verify `replaysSessionSampleRate` is not overriding |
| Network requests missing in replay | Add your API domains to `networkDetailAllowUrls` |
| Worker CSP errors in browser console | Add `worker-src 'self' blob:;` to your CSP headers |
| Canvas not recording | Add `replayCanvasIntegration()` alongside `replayIntegration()` |
| High bandwidth usage | Lower `replaysSessionSampleRate`; enable `mutationLimit`; disable network body capture |
| Replay blocked by ad-blocker | Set `tunnel: "/sentry-tunnel"` in `Sentry.init()` and implement server relay |
| `beforeAddRecordingEvent` not filtering | Ensure the function returns `null` (not `undefined`) to drop events |

---

## Reference: Tracing

# Tracing — Sentry Svelte/SvelteKit SDK

> Minimum SDK: `@sentry/sveltekit` ≥7.0.0+ / `@sentry/svelte` ≥7.0.0+  
> `Sentry.updateSpanName()`: requires `@sentry/sveltekit` ≥8.47.0+

---

## How Automatic Tracing Works

### SvelteKit

| What's traced | Where | How |
|---------------|-------|-----|
| Client-side page loads | Browser | `browserTracingIntegration()` in `hooks.client.ts` |
| Client-side navigations | Browser | `browserTracingIntegration()` — SvelteKit router changes |
| Outbound fetch/XHR requests | Browser | `browserTracingIntegration()` with `tracePropagationTargets` |
| Server-side request handling | Node | `sentryHandle()` in `hooks.server.ts` |
| Load functions (`+page.ts`, `+layout.ts`) | Both | Auto via `sentryHandle()` (≥10.8.0) |
| Server → client trace stitching | SSR → browser | SDK injects `<meta>` tags; `browserTracingIntegration()` reads them |

### Standalone Svelte

Only client-side tracing is available. All instrumentation happens in a single init call.

---

## Configuration

### SvelteKit — hooks.client.ts

```typescript
import * as Sentry from "@sentry/sveltekit";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,

  integrations: [
    Sentry.browserTracingIntegration(),
  ],

  tracesSampleRate: 1.0,   // 100% in dev; use 0.1–0.2 in production

  // Which outbound URLs get sentry-trace + baggage headers
  tracePropagationTargets: [
    "localhost",
    /^https:\/\/api\.myapp\.com/,
  ],
});

export const handleError = Sentry.handleErrorWithSentry();
```

### SvelteKit — instrumentation.server.ts (or hooks.server.ts for legacy)

```typescript
import * as Sentry from "@sentry/sveltekit";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
  // No browserTracingIntegration() here — server-side only
});
```

### SvelteKit — hooks.server.ts

```typescript
import * as Sentry from "@sentry/sveltekit";

export const handleError = Sentry.handleErrorWithSentry();
// sentryHandle() creates root spans for all incoming requests
export const handle = Sentry.sentryHandle();
```

### Standalone Svelte — main.ts

```typescript
import * as Sentry from "@sentry/svelte";
import App from "./App.svelte";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,

  integrations: [
    Sentry.browserTracingIntegration(),
  ],

  tracesSampleRate: 1.0,
  tracePropagationTargets: ["localhost", /^https:\/\/yourapi\.io/],
});

const app = new App({ target: document.getElementById("app")! });
export default app;
```

---

## Sampling

| Option | Behavior |
|--------|----------|
| `tracesSampleRate: 1.0` | Capture 100% of traces (dev / low-traffic) |
| `tracesSampleRate: 0.2` | Capture 20% uniformly |
| `tracesSampler: (ctx) => number` | Per-transaction logic; **overrides** `tracesSampleRate` when both set |
| omit both | Tracing fully disabled — no overhead |
| `tracesSampleRate: 0` | Code runs but nothing is sent — not the same as disabled |

### Dynamic sampler

```typescript
Sentry.init({
  tracesSampler: (samplingContext) => {
    const name = samplingContext.transactionContext?.name ?? "";
    if (name === "/health" || name === "/ping") return 0;
    if (name.startsWith("/checkout")) return 1.0;
    return 0.2; // default
  },
});
```

### Disable tracing for production builds (tree-shaking)

Set the build flag `__SENTRY_TRACING__ = false` to strip all tracing code at bundle time:

```typescript
// vite.config.ts
export default defineConfig({
  define: {
    __SENTRY_TRACING__: false,
  },
});
```

---

## `tracePropagationTargets`

Controls which outbound requests receive `sentry-trace` and `baggage` headers. Essential for distributed tracing between the SvelteKit frontend and your APIs.

```typescript
tracePropagationTargets: [
  "localhost",                              // substring match
  /^https:\/\/api\.myapp\.com/,             // regex match
  /^https:\/\/internal-service\.io\/api/,   // second backend
]
```

- Only matching URLs get distributed tracing headers
- Prevents leaking trace IDs to third-party services
- Omit to disable propagation entirely; set to `[""]` to propagate to all URLs

---

## Custom Spans

Three APIs with different lifecycle models:

### `Sentry.startSpan()` — recommended, auto-ends

```typescript
// Async work
const result = await Sentry.startSpan(
  {
    name: "fetch-user-profile",
    op: "http.client",
    attributes: {
      "user.id": userId,
      "cache.hit": false,
    },
  },
  async () => {
    return await fetchUserProfile(userId);
  }
);

// Sync work
const parsed = Sentry.startSpan(
  { name: "parse-payload", op: "deserialize" },
  () => JSON.parse(rawPayload)
);
```

### `Sentry.startSpanManual()` — manual `span.end()`

Use when the span lifetime doesn't match a callback (event-driven flows, middleware):

```typescript
function middleware(_req: Request, res: Response, next: NextFunction) {
  return Sentry.startSpanManual({ name: "express.middleware", op: "middleware" }, (span) => {
    res.once("finish", () => {
      span.setStatus({ code: res.statusCode < 400 ? 1 : 2 }); // 1=ok, 2=error
      span.end();
    });
    return next();
  });
}
```

### `Sentry.startInactiveSpan()` — explicit parent control

```typescript
// Span is not automatically set as the active span
const span = Sentry.startInactiveSpan({ name: "background-job", op: "task" });
await doBackgroundWork();
span.end();

// Explicit parent-child wiring
const parent = Sentry.startInactiveSpan({ name: "checkout-flow" });
const child = Sentry.startInactiveSpan({ name: "validate-cart", parentSpan: parent });
await validateCart();
child.end();
parent.end();
```

---

## Span Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `string` | **Required.** Span label in the UI |
| `op` | `string` | Operation category (e.g., `http.client`, `db.query`, `ui.render`, `task`) |
| `startTime` | `number` | Unix timestamp override |
| `attributes` | `Record<string, string \| number \| boolean>` | Key-value metadata |
| `parentSpan` | `Span` | Explicit parent reference |
| `onlyIfParent` | `boolean` | Drop span if no active parent exists |
| `forceTransaction` | `boolean` | Show as top-level transaction in Sentry UI |

---

## Enriching Active Spans

```typescript
const span = Sentry.getActiveSpan();
if (span) {
  span.setAttribute("db.rows_affected", 42);
  span.setAttributes({ "cache.key": "user:123", "cache.hit": true });
  span.setStatus({ code: 1 }); // 0=unknown, 1=ok, 2=error

  // Rename span (SDK ≥8.47.0)
  Sentry.updateSpanName(span, "Updated Span Name");
}

// Inject attributes into all spans globally
Sentry.init({
  beforeSendSpan(span) {
    span.data = { ...span.data, "app.region": "us-west-2" };
    return span;
  },
});
```

---

## Distributed Tracing: SvelteKit SSR ↔ Client ↔ APIs

SvelteKit's SDK automatically propagates trace context across the full request lifecycle:

```
Browser request
  → SvelteKit server receives request
      → sentryHandle() creates server root span
      → SSR renders HTML with injected <meta name="sentry-trace"> + <meta name="baggage">
  → Browser parses HTML
      → browserTracingIntegration() reads <meta> tags
      → Client span becomes child of SSR span
  → Client makes API call (matching tracePropagationTargets)
      → sentry-trace + baggage headers added to fetch request
      → Backend can continue the trace
```

All of this is automatic when:
1. `sentryHandle()` is exported from `hooks.server.ts`
2. `browserTracingIntegration()` is in client init
3. API URLs are listed in `tracePropagationTargets`

---

## Load Function Tracing (SvelteKit)

With `sentryHandle()` (≥10.8.0), all load functions are automatically instrumented. No wrapper needed.

**Legacy setup only** (if using `@sentry/sveltekit` <10.8.0):

```typescript
// src/routes/+page.ts (client load) — legacy only
import { wrapLoadWithSentry } from "@sentry/sveltekit";

export const load = wrapLoadWithSentry(async ({ fetch, params }) => {
  return { data: await fetch(`/api/${params.id}`).then(r => r.json()) };
});

// src/routes/+page.server.ts (server load) — legacy only
import { wrapServerLoadWithSentry } from "@sentry/sveltekit";

export const load = wrapServerLoadWithSentry(async ({ params }) => {
  return { id: params.id };
});
```

Remove these wrappers when upgrading to `@sentry/sveltekit` ≥10.8.0.

---

## Route-Based Transaction Names

SvelteKit automatically names transactions from SvelteKit's routing system:
- `GET /` → `pageload /`
- `GET /users/[id]` → `pageload /users/[id]`
- `GET /api/users` → server request span name

No manual transaction naming is needed for standard SvelteKit routes.

---

## Performance Data: Web Vitals

`browserTracingIntegration()` captures Core Web Vitals automatically:

| Metric | What it measures |
|--------|-----------------|
| LCP | Largest Contentful Paint |
| FID | First Input Delay |
| CLS | Cumulative Layout Shift |
| TTFB | Time to First Byte |
| FCP | First Contentful Paint |

Visible in the Sentry Performance dashboard under each page transaction.

---

## Flat Span Hierarchy (Browser)

By default, browser spans are **flat** — all spans become direct children of the root span rather than nesting. This avoids incorrect async parent-child associations.

To opt into full nesting (for structured waterfall views, at your own risk):

```typescript
Sentry.init({
  parentSpanIsAlwaysRootSpan: false,
});
```

---

## Filtering Transactions and Spans

```typescript
Sentry.init({
  // Drop entire transactions by name
  ignoreTransactions: ["/health", "/ping", /_next\/static/],

  // Filter/modify transactions before send
  beforeSendTransaction(event) {
    if (event.transaction?.startsWith("/_next/")) return null;
    return event;
  },

  // Filter/modify individual spans (e.g., drop asset spans)
  ignoreSpans: [
    { op: /^browser\.(cache|connect|DNS)$/ },
    { op: "resource.other", name: /.+\.(woff2|ttf|eot)$/ },
    { op: /resource\.(link|script)/, name: /.+\.js.*$/ },
  ],
});
```

---

## Svelte vs SvelteKit: Key Differences

| Concern | Standalone Svelte | SvelteKit |
|---------|-------------------|-----------|
| Server-side tracing | ❌ N/A | ✅ Auto via `sentryHandle()` |
| `browserTracingIntegration()` | In single init call | In `hooks.client.ts` only |
| Distributed tracing | Client-only | Full SSR → client → backend |
| Load function tracing | N/A | Auto (≥10.8.0) |
| Transaction names | URL-based | SvelteKit route patterns |
| Web Vitals | ✅ Both | ✅ Both |

---

## Best Practices

- Use `tracesSampleRate: 1.0` in development; drop to `0.1`–`0.2` in production
- Never add `browserTracingIntegration()` to server-side init
- Use `tracePropagationTargets` to restrict trace header injection to your own backends
- Add `sentryHandle()` before other handles in `sequence()` so it wraps the full request lifecycle
- Use `onlyIfParent: true` on optional spans to avoid orphaned root transactions

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transactions in Performance dashboard | Ensure `tracesSampleRate` > 0; check `browserTracingIntegration()` is in client init |
| Distributed trace not connected (server ↔ client) | Verify `sentryHandle()` is exported from `hooks.server.ts` |
| API calls not connected to frontend trace | Add API URL to `tracePropagationTargets` |
| Load functions not instrumented | Upgrade to `@sentry/sveltekit` ≥10.8.0; remove legacy `wrapLoadWithSentry` |
| `sentryHandle()` breaking other handles | Wrap with `sequence(Sentry.sentryHandle(), myHandle)` from `@sveltejs/kit/hooks` |
| Web Vitals missing | Confirm `browserTracingIntegration()` is included; check browser support |
| Spans missing after async gap | Browser flat hierarchy; use `startInactiveSpan` with explicit `parentSpan` |
| High transaction volume / cost | Lower `tracesSampleRate`; use `tracesSampler` to drop health checks and static assets |
