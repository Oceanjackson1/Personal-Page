---
title: "Sentry React SDK"
description: "Sentry 错误监控 React SDK 集成，前端异常和性能监控"
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "react", "sdk"]
date: 2026-03-20
---

# Sentry React SDK

Opinionated wizard that scans your React project and guides you through complete Sentry setup.

## Invoke This Skill When

- User asks to "add Sentry to React" or "set up Sentry" in a React app
- User wants error monitoring, tracing, session replay, profiling, or logging in React
- User mentions `@sentry/react`, React Sentry SDK, or Sentry error boundaries
- User wants to monitor React Router navigation, Redux state, or component performance

> **Note:** SDK versions and APIs below reflect current Sentry docs at time of writing (`@sentry/react` ≥8.0.0).
> Always verify against [docs.sentry.io/platforms/javascript/guides/react/](https://docs.sentry.io/platforms/javascript/guides/react/) before implementing.

---

## Phase 1: Detect

Run these commands to understand the project before making any recommendations:

```bash
# Detect React version
cat package.json | grep -E '"react"|"react-dom"'

# Check for existing Sentry
cat package.json | grep '"@sentry/'

# Detect router
cat package.json | grep -E '"react-router-dom"|"@tanstack/react-router"'

# Detect state management
cat package.json | grep -E '"redux"|"@reduxjs/toolkit"'

# Detect build tool
ls vite.config.ts vite.config.js webpack.config.js craco.config.js 2>/dev/null
cat package.json | grep -E '"vite"|"react-scripts"|"webpack"'

# Detect logging libraries
cat package.json | grep -E '"pino"|"winston"|"loglevel"'

# Check for companion backend in adjacent directories
ls ../backend ../server ../api 2>/dev/null
cat ../go.mod ../requirements.txt ../Gemfile ../pom.xml 2>/dev/null | head -3
```

**What to determine:**

| Question | Impact |
|----------|--------|
| React 19+? | Use `reactErrorHandler()` hook pattern |
| React <19? | Use `Sentry.ErrorBoundary` |
| `@sentry/react` already present? | Skip install, go straight to feature config |
| `react-router-dom` v5 / v6 / v7? | Determines which router integration to use |
| `@tanstack/react-router`? | Use `tanstackRouterBrowserTracingIntegration()` |
| Redux in use? | Recommend `createReduxEnhancer()` |
| Vite detected? | Source maps via `sentryVitePlugin` |
| CRA (`react-scripts`)? | Source maps via `@sentry/webpack-plugin` in CRACO |
| Backend directory found? | Trigger Phase 4 cross-link suggestion |

---

## Phase 2: Recommend

Present a concrete recommendation based on what you found. Don't ask open-ended questions — lead with a proposal:

**Recommended (core coverage):**
- ✅ **Error Monitoring** — always; captures unhandled errors, React error boundaries, React 19 hooks
- ✅ **Tracing** — React SPAs benefit from page load, navigation, and API call tracing
- ✅ **Session Replay** — recommended for user-facing apps; records sessions around errors

**Optional (enhanced observability):**
- ⚡ **Logging** — structured logs via `Sentry.logger.*`; recommend when structured log search is needed
- ⚡ **Profiling** — JS Self-Profiling API (⚠️ experimental; requires cross-origin isolation headers)

**Recommendation logic:**

| Feature | Recommend when... |
|---------|------------------|
| Error Monitoring | **Always** — non-negotiable baseline |
| Tracing | **Always for React SPAs** — page load + navigation spans are high-value |
| Session Replay | User-facing app, login flows, or checkout pages |
| Logging | App needs structured log search or log-to-trace correlation |
| Profiling | Performance-critical app; server sends `Document-Policy: js-profiling` header |

**React-specific extras:**
- React 19 detected → set up `reactErrorHandler()` on `createRoot`
- React Router detected → configure matching router integration (see Phase 3)
- Redux detected → add `createReduxEnhancer()` to Redux store
- Vite detected → configure `sentryVitePlugin` for source maps (essential for readable stack traces)

Propose: *"I recommend setting up Error Monitoring + Tracing + Session Replay. Want me to also add Logging or Profiling?"*

---

## Phase 3: Guide

### Install

```bash
npm install @sentry/react --save
```

### Create `src/instrument.ts`

Sentry must initialize **before any other code runs**. Put `Sentry.init()` in a dedicated sidecar file:

```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN, // Adjust per build tool (see table below)
  environment: import.meta.env.MODE,
  release: import.meta.env.VITE_APP_VERSION, // inject at build time

  sendDefaultPii: true,

  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  // Tracing
  tracesSampleRate: 1.0, // lower to 0.1–0.2 in production
  tracePropagationTargets: ["localhost", /^https:\/\/yourapi\.io/],

  // Session Replay
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,

  enableLogs: true,
});
```

**DSN environment variable by build tool:**

| Build Tool | Variable Name | Access in code |
|------------|--------------|----------------|
| Vite | `VITE_SENTRY_DSN` | `import.meta.env.VITE_SENTRY_DSN` |
| Create React App | `REACT_APP_SENTRY_DSN` | `process.env.REACT_APP_SENTRY_DSN` |
| Custom webpack | `SENTRY_DSN` | `process.env.SENTRY_DSN` |

### Entry Point Setup

Import `instrument.ts` as the **very first import** in your entry file:

```tsx
// src/main.tsx (Vite) or src/index.tsx (CRA/webpack)
import "./instrument";              // ← MUST be first

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

### React Version-Specific Error Handling

**React 19+** — use `reactErrorHandler()` on `createRoot`:

```tsx
import { reactErrorHandler } from "@sentry/react";

createRoot(document.getElementById("root")!, {
  onUncaughtError: reactErrorHandler(),
  onCaughtError: reactErrorHandler(),
  onRecoverableError: reactErrorHandler(),
}).render(<App />);
```

**React <19** — wrap your app in `Sentry.ErrorBoundary`:

```tsx
import * as Sentry from "@sentry/react";

createRoot(document.getElementById("root")!).render(
  <Sentry.ErrorBoundary fallback={<p>Something went wrong</p>} showDialog>
    <App />
  </Sentry.ErrorBoundary>
);
```

Use `<Sentry.ErrorBoundary>` for any sub-tree that should catch errors independently (route sections, widgets, etc.).

### Router Integration

Configure the matching integration for your router:

| Router | Integration | Notes |
|--------|------------|-------|
| React Router v7 | `reactRouterV7BrowserTracingIntegration` | `useEffect`, `useLocation`, `useNavigationType`, `createRoutesFromChildren`, `matchRoutes` from `react-router` |
| React Router v6 | `reactRouterV6BrowserTracingIntegration` | `useEffect`, `useLocation`, `useNavigationType`, `createRoutesFromChildren`, `matchRoutes` from `react-router-dom` |
| React Router v5 | `reactRouterV5BrowserTracingIntegration` | Wrap routes in `withSentryRouting(Route)` |
| TanStack Router | `tanstackRouterBrowserTracingIntegration(router)` | Pass router instance — no hooks required |
| No router / custom | `browserTracingIntegration()` | Names transactions by URL path |

**React Router v6/v7 setup:**

```typescript
// in instrument.ts integrations array:
import React from "react";
import {
  createRoutesFromChildren, matchRoutes,
  useLocation, useNavigationType,
} from "react-router-dom"; // or "react-router" for v7
import * as Sentry from "@sentry/react";
import { reactRouterV6BrowserTracingIntegration } from "@sentry/react";
import { createBrowserRouter } from "react-router-dom";

// Option A — createBrowserRouter (recommended for v6.4+):
const sentryCreateBrowserRouter = Sentry.wrapCreateBrowserRouterV6(createBrowserRouter);
const router = sentryCreateBrowserRouter([...routes]);

// Option B — createBrowserRouter for React Router v7:
// const sentryCreateBrowserRouter = Sentry.wrapCreateBrowserRouterV7(createBrowserRouter);

// Option C — integration with hooks (v6 without data APIs):
Sentry.init({
  integrations: [
    reactRouterV6BrowserTracingIntegration({
      useEffect: React.useEffect,
      useLocation,
      useNavigationType,
      matchRoutes,
      createRoutesFromChildren,
    }),
  ],
});
```

**TanStack Router setup:**

```typescript
import { tanstackRouterBrowserTracingIntegration } from "@sentry/react";

// Pass your TanStack router instance:
Sentry.init({
  integrations: [tanstackRouterBrowserTracingIntegration(router)],
});
```

### Redux Integration (when detected)

```typescript
import * as Sentry from "@sentry/react";
import { configureStore } from "@reduxjs/toolkit";

const store = configureStore({
  reducer: rootReducer,
  enhancers: (getDefaultEnhancers) =>
    getDefaultEnhancers().concat(Sentry.createReduxEnhancer()),
});
```

### Source Maps Setup (strongly recommended)

Without source maps, stack traces show minified code. Set up the build plugin to upload source maps automatically:

**Vite (`vite.config.ts`):**

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { sentryVitePlugin } from "@sentry/vite-plugin";

export default defineConfig({
  build: { sourcemap: "hidden" },
  plugins: [
    react(),
    sentryVitePlugin({
      org: process.env.SENTRY_ORG,
      project: process.env.SENTRY_PROJECT,
      authToken: process.env.SENTRY_AUTH_TOKEN,
    }),
  ],
});
```

Add to `.env` (never commit):
```bash
SENTRY_AUTH_TOKEN=sntrys_...
SENTRY_ORG=my-org-slug
SENTRY_PROJECT=my-project-slug
```

**Create React App (via CRACO):**

```bash
npm install @craco/craco @sentry/webpack-plugin --save-dev
```

```javascript
// craco.config.js
const { sentryWebpackPlugin } = require("@sentry/webpack-plugin");

module.exports = {
  webpack: {
    plugins: {
      add: [
        sentryWebpackPlugin({
          org: process.env.SENTRY_ORG,
          project: process.env.SENTRY_PROJECT,
          authToken: process.env.SENTRY_AUTH_TOKEN,
        }),
      ],
    },
  },
};
```

### For Each Agreed Feature

Walk through features one at a time. Load the reference file, follow its steps, verify before moving on:

| Feature | Reference | Load when... |
|---------|-----------|-------------|
| Error Monitoring | `${SKILL_ROOT}/references/error-monitoring.md` | Always (baseline) |
| Tracing | `${SKILL_ROOT}/references/tracing.md` | SPA navigation / API call tracing |
| Session Replay | `${SKILL_ROOT}/references/session-replay.md` | User-facing app |
| Logging | `${SKILL_ROOT}/references/logging.md` | Structured log search / log-to-trace |
| Profiling | `${SKILL_ROOT}/references/profiling.md` | Performance-critical app |
| React Features | `${SKILL_ROOT}/references/react-features.md` | Redux, component tracking, source maps, integrations catalog |

For each feature: `Read ${SKILL_ROOT}/references/<feature>.md`, follow steps exactly, verify it works.

---

## Configuration Reference

### Key `Sentry.init()` Options

| Option | Type | Default | Notes |
|--------|------|---------|-------|
| `dsn` | `string` | — | **Required.** SDK disabled when empty |
| `environment` | `string` | `"production"` | e.g., `"staging"`, `"development"` |
| `release` | `string` | — | e.g., `"my-app@1.0.0"` or git SHA — links errors to releases |
| `sendDefaultPii` | `boolean` | `false` | Includes IP addresses and request headers |
| `tracesSampleRate` | `number` | — | 0–1; `1.0` in dev, `0.1–0.2` in prod |
| `tracesSampler` | `function` | — | Per-transaction sampling; overrides rate |
| `tracePropagationTargets` | `(string\|RegExp)[]` | — | Outgoing URLs that receive distributed tracing headers |
| `replaysSessionSampleRate` | `number` | — | Fraction of all sessions recorded |
| `replaysOnErrorSampleRate` | `number` | — | Fraction of error sessions recorded |
| `enableLogs` | `boolean` | `false` | Enable `Sentry.logger.*` API |
| `attachStacktrace` | `boolean` | `false` | Stack traces on `captureMessage()` calls |
| `maxBreadcrumbs` | `number` | `100` | Breadcrumbs stored per event |
| `debug` | `boolean` | `false` | Verbose SDK output to console |
| `tunnel` | `string` | — | Proxy URL to bypass ad blockers |

### React Compatibility Matrix

| React Version | Error handling approach | SDK minimum |
|---------------|------------------------|-------------|
| React 19+ | `reactErrorHandler()` on `createRoot` | `@sentry/react` ≥8.0.0 |
| React 16–18 | `Sentry.ErrorBoundary` component | `@sentry/react` ≥7.0.0 |
| React 16 | `componentDidCatch` class boundaries | `@sentry/react` ≥6.0.0 |

---

## Verification

Trigger test events to confirm Sentry is receiving data:

```tsx
// Add a temporary test button anywhere in your app
import * as Sentry from "@sentry/react";

function SentryTest() {
  return (
    <>
      <button onClick={() => { throw new Error("Sentry React test error"); }}>
        Test Error
      </button>
      <button onClick={() => Sentry.captureMessage("Sentry test message", "info")}>
        Test Message
      </button>
    </>
  );
}
```

Check the Sentry dashboard:
- **Issues** → error appears within seconds
- **Traces** → page load and navigation transactions visible
- **Replays** → session recording visible after page interaction
- **Logs** → structured log entries if logging enabled

Set `debug: true` in `Sentry.init()` and check the browser console if nothing appears.

---

## Phase 4: Cross-Link

After completing React setup, check for a companion backend missing Sentry coverage:

```bash
ls ../backend ../server ../api ../go ../python 2>/dev/null
cat ../go.mod 2>/dev/null | head -3
cat ../requirements.txt ../pyproject.toml 2>/dev/null | head -3
cat ../Gemfile 2>/dev/null | head -3
cat ../pom.xml 2>/dev/null | grep '<artifactId>' | head -3
```

If a backend exists without Sentry configured, suggest the matching skill:

| Backend detected | Suggest skill |
|-----------------|--------------|
| Go (`go.mod`) | `sentry-go-sdk` |
| Python (`requirements.txt`, `pyproject.toml`) | `sentry-python-sdk` |
| Ruby (`Gemfile`) | `sentry-ruby-sdk` |
| Java (`pom.xml`, `build.gradle`) | Use `@sentry/java` — see [docs.sentry.io/platforms/java/](https://docs.sentry.io/platforms/java/) |
| Node.js (Express, Fastify) | Use `@sentry/node` — see [docs.sentry.io/platforms/javascript/guides/express/](https://docs.sentry.io/platforms/javascript/guides/express/) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Set `debug: true`, check DSN, open browser console for SDK errors |
| Source maps not working | Build in production mode (`npm run build`); verify `SENTRY_AUTH_TOKEN` is set |
| Minified stack traces | Source maps not uploading — check plugin config and auth token |
| `instrument.ts` not running first | Verify it's the first import in entry file before React/app imports |
| React 19 errors not captured | Confirm `reactErrorHandler()` is passed to all three `createRoot` options |
| React <19 errors not captured | Ensure `<Sentry.ErrorBoundary>` wraps the component tree |
| Router transactions named `<unknown>` | Add router integration matching your router version |
| `tracePropagationTargets` not matching | Check regex escaping; default is `localhost` and your DSN origin only |
| Session replay not recording | Confirm `replayIntegration()` is in init; check `replaysSessionSampleRate` |
| Redux actions not in breadcrumbs | Add `Sentry.createReduxEnhancer()` to store enhancers |
| Ad blockers dropping events | Set `tunnel: "/sentry-tunnel"` and add server-side relay endpoint |
| High replay storage costs | Lower `replaysSessionSampleRate`; keep `replaysOnErrorSampleRate: 1.0` |
| Profiling not working | Verify `Document-Policy: js-profiling` header is set on document responses |

---

## Reference: Error Monitoring

# Error Monitoring — Sentry React SDK

> Minimum SDK: `@sentry/react` ≥8.0.0+  
> `captureReactException()` requires `@sentry/react` ≥9.8.0  
> `reactErrorHandler()` requires `@sentry/react` ≥8.6.0

---

## How Automatic Capture Works

The React SDK hooks into the browser environment and captures errors automatically from multiple layers:

| Layer | Mechanism | Integration |
|-------|-----------|-------------|
| Uncaught JS exceptions | `window.onerror` | `GlobalHandlers` (default on) |
| Unhandled promise rejections | `window.onunhandledrejection` | `GlobalHandlers` (default on) |
| Errors in `setTimeout` / `setInterval` / `requestAnimationFrame` | Patched browser APIs | `BrowserApiErrors` (default on) |
| React render errors (React <19) | `componentDidCatch` via `<ErrorBoundary>` | `Sentry.ErrorBoundary` |
| React render errors (React 19+) | `createRoot` hooks | `Sentry.reactErrorHandler()` |
| Console errors (optional) | Patched `console.error` | `CaptureConsole` (opt-in) |

### What Requires Manual Instrumentation

The global handlers only catch errors that **escape** your code. These are silently swallowed without manual calls:

- Errors caught by your own `try/catch` blocks
- Errors swallowed by React Router's default error boundary
- Business-logic failures (validation errors, unexpected states)
- Async errors inside `Promise.then()` chains where `.catch()` is attached
- User-visible conditions that aren't exceptions (use `captureMessage`)

### Disabling or Customizing Automatic Capture

```javascript
Sentry.init({
  integrations: [
    Sentry.globalHandlersIntegration({
      onerror: true,
      onunhandledrejection: false,  // handle rejections manually
    }),
  ],
});

// Manual rejection handler:
window.addEventListener("unhandledrejection", (event) => {
  Sentry.captureException(event.reason);
});
```

---

## React Error Boundaries

### Strategy: React 19+ vs. React ≤18

| | React ≤18 | React 19+ |
|---|---|---|
| **Global error reporting** | `window.onerror` + `Sentry.ErrorBoundary` | `Sentry.reactErrorHandler()` on `createRoot` |
| **Scoped fallback UI** | `<Sentry.ErrorBoundary>` | `<Sentry.ErrorBoundary>` (still required) |
| **Complementary?** | N/A | ✅ Use both together |

---

### React 19+ — `Sentry.reactErrorHandler()` with `createRoot`

React 19 exposes three hooks on `createRoot` and `hydrateRoot`. Pass `Sentry.reactErrorHandler()` to each one. Requires `@sentry/react` ≥8.6.0.

```jsx
// src/main.tsx
import { createRoot } from "react-dom/client";
import * as Sentry from "@sentry/react";

Sentry.init({ dsn: "___PUBLIC_DSN___" });

const container = document.getElementById("app")!;

createRoot(container, {
  // Fires for errors that bubble up WITHOUT any ErrorBoundary catching them.
  // These are fatal — the entire React tree unmounts.
  onUncaughtError: Sentry.reactErrorHandler((error, errorInfo) => {
    // Optional: runs AFTER Sentry has already captured the error
    console.warn("Uncaught React error:", error.message);
    console.warn("Component stack:", errorInfo.componentStack);
  }),

  // Fires for errors caught BY an ErrorBoundary (React 19 re-routes caught errors here).
  // The boundary still renders its fallback UI — this is just the reporting hook.
  onCaughtError: Sentry.reactErrorHandler(),

  // Fires when React recovers from an error automatically (e.g. hydration mismatch).
  onRecoverableError: Sentry.reactErrorHandler(),
}).render(<App />);
```

**SSR / `hydrateRoot`:**

```jsx
import { hydrateRoot } from "react-dom/client";
import * as Sentry from "@sentry/react";

hydrateRoot(document.getElementById("app")!, <App />, {
  onUncaughtError: Sentry.reactErrorHandler(),
  onCaughtError: Sentry.reactErrorHandler(),
  onRecoverableError: Sentry.reactErrorHandler(),
});
```

**Key behavior differences between the three hooks:**

| Hook | Fires when... | Tree state after |
|------|--------------|-----------------|
| `onUncaughtError` | Error escapes all boundaries | Tree unmounts (fatal) |
| `onCaughtError` | ErrorBoundary catches the error | Boundary renders fallback |
| `onRecoverableError` | React auto-recovers (e.g. hydration) | Tree continues rendering |

#### React 19 + ErrorBoundary Together (Recommended Pattern)

`reactErrorHandler()` is the global net. `<Sentry.ErrorBoundary>` provides scoped fallback UIs. Use both:

```jsx
// src/main.tsx — global net via reactErrorHandler
createRoot(document.getElementById("root")!, {
  onUncaughtError: Sentry.reactErrorHandler(),
  onCaughtError: Sentry.reactErrorHandler(),
  onRecoverableError: Sentry.reactErrorHandler(),
}).render(<App />);

// src/App.tsx — scoped fallback UIs via ErrorBoundary
function App() {
  return (
    <Layout>
      <Sentry.ErrorBoundary fallback={<NavError />}>
        <Navigation />
      </Sentry.ErrorBoundary>
      <Sentry.ErrorBoundary fallback={<DashboardError />}>
        <Dashboard />
      </Sentry.ErrorBoundary>
    </Layout>
  );
}
```

---

### `<Sentry.ErrorBoundary>` — Full Props Reference

Works with React 16+. Catches errors in its subtree, reports them to Sentry, and renders a fallback UI.

```typescript
// Full TypeScript signature
interface ErrorBoundaryProps {
  // Fallback UI — static element or render function
  fallback?: React.ReactNode | FallbackRender;
  // FallbackRender receives: { error: Error; componentStack: string; resetError: () => void }

  // Called immediately when a child throws
  onError?: (error: Error, componentStack: string, eventId: string) => void;

  // Called with the Sentry Scope before the error is captured — enrich here
  beforeCapture?: (scope: Scope, error: Error, componentStack: string) => void;

  // Called when resetError() is invoked from the fallback
  onReset?: (error: Error | null, componentStack: string | null, eventId: string | null) => void;

  // Lifecycle hooks
  onMount?: () => void;
  onUnmount?: (error: Error | null) => void;

  // User feedback dialog — shown automatically on error
  showDialog?: boolean;
  dialogOptions?: ReportDialogOptions;
}
```

---

#### `fallback` — Render Fallback UI on Error

```jsx
// 1. Static element
<Sentry.ErrorBoundary fallback={<p>Something went wrong. Please refresh.</p>}>
  <Dashboard />
</Sentry.ErrorBoundary>

// 2. Render function — access error details and reset handler
<Sentry.ErrorBoundary
  fallback={({ error, componentStack, resetError }) => (
    <div className="error-state">
      <h2>Something broke</h2>
      <p><strong>Error:</strong> {error.message}</p>
      <details>
        <summary>Component stack</summary>
        <pre style={{ fontSize: 12 }}>{componentStack}</pre>
      </details>
      <button onClick={resetError}>↺ Try Again</button>
    </div>
  )}
>
  <Dashboard />
</Sentry.ErrorBoundary>
```

**`resetError()`** resets the boundary's internal state and re-attempts rendering children. Use it for retry UIs.

---

#### `onError` — React to a Captured Error

Called immediately when a child throws. Receives the error, component stack, and the Sentry event ID (useful for linking user feedback to the event).

```jsx
<Sentry.ErrorBoundary
  onError={(error, componentStack, eventId) => {
    // Report to your own analytics
    myAnalytics.track("error_boundary_triggered", {
      errorMessage: error.message,
      sentryEventId: eventId,
    });
    // Dispatch to Redux or Zustand
    store.dispatch(setGlobalError({ error, eventId }));
    // Show feedback dialog linked to this event
    Sentry.showReportDialog({ eventId });
  }}
  fallback={<ErrorScreen />}
>
  <App />
</Sentry.ErrorBoundary>
```

---

#### `beforeCapture` — Enrich the Event Before Sending

Called with the Sentry `Scope` before the error is captured. Use it to add tags, context, or level enrichment specific to this boundary's location in the tree.

```jsx
<Sentry.ErrorBoundary
  beforeCapture={(scope, error, componentStack) => {
    scope.setTag("section", "checkout");
    scope.setTag("error_type", error.constructor.name);
    scope.setExtra("componentStack", componentStack);
    scope.setLevel("fatal");
    scope.setContext("payment", { step: "card-entry" });
  }}
  fallback={<CheckoutError />}
>
  <CheckoutFlow />
</Sentry.ErrorBoundary>
```

---

#### `onReset` — Cleanup When the Boundary Resets

Called when `resetError()` is invoked. Clear stale state in stores or invalidate caches here.

```jsx
<Sentry.ErrorBoundary
  onReset={(error, componentStack, eventId) => {
    queryClient.clear();
    store.dispatch(clearCheckoutState());
  }}
  fallback={({ resetError }) => (
    <div>
      <p>Payment failed to load.</p>
      <button onClick={resetError}>Retry</button>
    </div>
  )}
>
  <CheckoutFlow />
</Sentry.ErrorBoundary>
```

---

#### `showDialog` + `dialogOptions` — Crash-Report Modal on Error

```jsx
<Sentry.ErrorBoundary
  showDialog
  dialogOptions={{
    title: "It looks like something went wrong.",
    subtitle: "Our engineering team has been notified.",
    subtitle2: "Want to help us fix it? Tell us what happened.",
    labelName: "Your name",
    labelEmail: "Your email",
    labelComments: "What happened before this error?",
    labelSubmit: "Send Report",
    successMessage: "Thanks! Your report helps us improve.",
    user: { email: "currentuser@example.com", name: "Jane Smith" },
  }}
  fallback={<p>We've logged this issue and are working on a fix.</p>}
>
  <Dashboard />
</Sentry.ErrorBoundary>
```

---

#### `onMount` / `onUnmount` — Lifecycle Hooks

```jsx
<Sentry.ErrorBoundary
  onMount={() => analytics.track("error_boundary_mounted", { section: "dashboard" })}
  onUnmount={(error) => {
    if (error) analytics.track("error_boundary_active_on_unmount");
  }}
  fallback={<DashboardError />}
>
  <Dashboard />
</Sentry.ErrorBoundary>
```

---

### `Sentry.withErrorBoundary(Component, options)` — HOC Pattern

Equivalent to wrapping with `<Sentry.ErrorBoundary>`. Useful when you want to wrap at the import or module level instead of in JSX.

```jsx
import * as Sentry from "@sentry/react";

// Basic
const SafeDashboard = Sentry.withErrorBoundary(Dashboard, {
  fallback: <p>Dashboard failed to load.</p>,
});

// Full options — identical to ErrorBoundary props
const SafeCheckout = Sentry.withErrorBoundary(CheckoutFlow, {
  fallback: ({ error, resetError }) => (
    <div>
      <p>Checkout error: {error.message}</p>
      <button onClick={resetError}>Retry</button>
    </div>
  ),
  onError: (error, componentStack, eventId) => {
    analytics.track("checkout_boundary_triggered", { eventId });
  },
  beforeCapture: (scope) => {
    scope.setTag("section", "checkout");
    scope.setLevel("fatal");
  },
  showDialog: true,
});

// Use exactly like the unwrapped component
function App() {
  return <SafeCheckout />;
}
```

---

### Nested Error Boundaries — Isolation Pattern

Each boundary only catches errors from **its own subtree**. Nesting lets one broken feature fail in isolation without crashing the whole page.

```jsx
function App() {
  return (
    // Outermost — catches anything that escapes inner boundaries
    <Sentry.ErrorBoundary
      fallback={<FullPageError />}
      beforeCapture={(scope) => scope.setTag("level", "app")}
    >
      <Layout>
        <Sentry.ErrorBoundary
          fallback={<NavError />}
          beforeCapture={(scope) => scope.setTag("section", "navigation")}
        >
          <Navigation />
        </Sentry.ErrorBoundary>

        <main>
          <Sentry.ErrorBoundary
            fallback={<SidebarError />}
            beforeCapture={(scope) => scope.setTag("section", "sidebar")}
          >
            <Sidebar />
          </Sentry.ErrorBoundary>

          <Sentry.ErrorBoundary
            fallback={<ContentError />}
            beforeCapture={(scope) => scope.setTag("section", "content")}
          >
            <MainContent />
          </Sentry.ErrorBoundary>
        </main>
      </Layout>
    </Sentry.ErrorBoundary>
  );
}
```

**Recommended placement strategy:**

| Boundary location | Purpose |
|------------------|---------|
| Outermost (around `<App>`) | Last resort — prevents total blank page |
| Route level | Isolate route failures; different fallback per route |
| Widget / panel level | Let other panels stay functional when one fails |
| Data-fetching components | Catch errors from async rendering |

---

### Custom Class-Based Error Boundaries — `captureReactException`

> Requires `@sentry/react` ≥9.8.0

If you need a custom class boundary, use `captureReactException` instead of `captureException`. It correctly attaches the React `componentStack` as a linked cause via the `LinkedErrors` integration, producing readable component traces in Sentry.

```jsx
import * as Sentry from "@sentry/react";

class CustomBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // errorInfo = { componentStack: "\n  at Dashboard\n  at App..." }
    // captureReactException wires up the componentStack correctly
    Sentry.captureReactException(error, errorInfo);
  }

  render() {
    if (this.state.hasError) return <p>Something went wrong.</p>;
    return this.props.children;
  }
}
```

> **Why not plain `captureException`?** Calling `captureException` inside `componentDidCatch` loses the component stack linkage. `captureReactException` correctly wires `error.cause` so the component tree appears as a linked error in Sentry's issue detail view.

**What linked errors look like in Sentry:**

```
Error: Cannot read properties of undefined (reading 'map')
  at Dashboard (Dashboard.tsx:42)
Caused by: React component stack:
  at Dashboard
  at Sentry.ErrorBoundary
  at App
```

> Requires React 17+ and the `LinkedErrors` integration (enabled by default). Set up source maps for readable component file paths.

---

## Manual Error Capture

### `Sentry.captureException(error, captureContext?)`

Captures an error and sends it to Sentry. Prefer `Error` objects (they include stack traces). Non-`Error` values (strings, plain objects) are accepted but may lack stack traces.

```javascript
// Basic usage
try {
  riskyOperation();
} catch (err) {
  Sentry.captureException(err);
}

// With full capture context
try {
  await chargeCard(order);
} catch (err) {
  Sentry.captureException(err, {
    level: "fatal",                          // "fatal"|"error"|"warning"|"log"|"info"|"debug"
    tags: { module: "checkout", retried: "true" },
    extra: { cartItems: 3, coupon: "SAVE20" },
    user: { id: "u_123", email: "user@example.com" },
    fingerprint: ["checkout-payment-fail"],  // custom grouping key
    contexts: {
      payment: { provider: "stripe", amount: 9999, currency: "usd" },
    },
  });
}
```

**React-specific tip:** Avoid calling Sentry in the render path. Wrap Sentry calls in `useEffect` to prevent firing on every render:

```jsx
function UserProfile({ userId }) {
  const { data: profile, error } = useQuery(["user", userId], fetchUser);

  useEffect(() => {
    if (error) {
      Sentry.captureException(error, {
        tags: { component: "UserProfile" },
        extra: { userId },
      });
    }
  }, [error, userId]);

  if (error) return <p>Failed to load profile.</p>;
  return profile ? <Profile data={profile} /> : null;
}
```

---

### `Sentry.captureMessage(message, level?)`

Captures a plain-text message as a Sentry issue. Useful for non-exception events: deprecated API calls, suspicious conditions, rate-limit hits.

```javascript
// With level as second argument
Sentry.captureMessage("Payment gateway timeout — fallback triggered", "warning");

// All valid levels: "fatal" | "error" | "warning" | "log" | "info" | "debug"
// Default when omitted: "info"

// With full capture context as second argument
Sentry.captureMessage("Feature flag evaluation failed", {
  level: "error",
  tags: { flagName: "new-checkout", service: "feature-flags" },
  extra: { userId: "u_42", evaluationContext: { country: "DE" } },
});
```

---

### `Sentry.captureEvent(event)`

Low-level API for sending a fully constructed Sentry event object. Use `captureException` or `captureMessage` in application code. `captureEvent` is for custom integrations or forwarding events from legacy loggers.

```javascript
Sentry.captureEvent({
  message: "Legacy logger forwarded event",
  level: "warning",
  tags: { source: "legacy-logger", module: "billing" },
  extra: { rawLog: "something went wrong at line 42" },
  timestamp: Date.now() / 1000,  // Unix timestamp in seconds
  fingerprint: ["legacy-billing-error"],
});
```

---

### Try/Catch Patterns in React

**Event handlers** — errors here are NOT caught by error boundaries (boundaries only catch render errors):

```jsx
function PaymentForm() {
  const [status, setStatus] = useState("idle");

  async function handleSubmit(event) {
    event.preventDefault();
    setStatus("loading");
    try {
      await processPayment(getFormValues(event.target));
      setStatus("success");
    } catch (err) {
      setStatus("error");
      Sentry.captureException(err, {
        tags: { component: "PaymentForm", action: "submit" },
        extra: { formFields: Object.fromEntries(new FormData(event.target)) },
      });
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <button type="submit" disabled={status === "loading"}>
        {status === "loading" ? "Processing..." : "Pay"}
      </button>
      {status === "error" && <p>Payment failed. Please try again.</p>}
    </form>
  );
}
```

**Async operations in effects:**

```jsx
useEffect(() => {
  async function loadData() {
    try {
      const data = await fetchDashboardData();
      setData(data);
    } catch (err) {
      Sentry.captureException(err, {
        tags: { hook: "useEffect", data: "dashboard" },
      });
      setError(err);
    }
  }
  loadData();
}, []);
```

**Promise chains:**

```javascript
fetchUserData(userId)
  .then(processUser)
  .catch((err) => {
    Sentry.captureException(err, {
      tags: { operation: "fetchUserData" },
      extra: { userId },
    });
    return null; // graceful fallback
  });
```

---

## Context Enrichment

### `Sentry.setUser(user)` — Identify the Current User

Associates a user identity with all subsequent events. Call after login; call `Sentry.setUser(null)` on logout.

```typescript
// Accepted fields (all optional):
interface SentryUser {
  id?: string | number;     // your internal user ID
  email?: string;
  username?: string;
  ip_address?: string;      // "{{ auto }}" to infer from request
  segment?: string;         // e.g. "paid", "trial", "beta", "enterprise"
  // Any additional custom fields are accepted
}
```

```javascript
// On login:
Sentry.setUser({
  id: "usr_abc123",
  email: "jane.smith@example.com",
  username: "janesmith",
  segment: "enterprise",
  // Custom fields:
  plan: "pro",
  team_id: "team_789",
  account_age_days: 365,
});

// On logout — clears user from all subsequent events:
Sentry.setUser(null);

// Auto-infer IP address (requires sendDefaultPii: true):
Sentry.setUser({
  id: "usr_abc123",
  ip_address: "{{ auto }}",
});
```

> **Privacy:** `sendDefaultPii: true` in `Sentry.init` enables automatic IP inference. To prevent IP storage entirely, enable "Prevent Storing of IP Addresses" in your project's Security & Privacy settings in Sentry.

---

### `Sentry.setContext(name, data)` — Attach Structured Custom Data

Attaches arbitrary structured data to all subsequent events. Context is **not indexed or searchable** — use tags for filterable data. Context appears in the issue detail view.

```javascript
// E-commerce checkout context
Sentry.setContext("checkout", {
  step: "payment",
  cart_items: 3,
  total_usd: 99.99,
  coupon_applied: "SAVE20",
  payment_provider: "stripe",
});

// Feature flags in effect
Sentry.setContext("feature_flags", {
  new_checkout: true,
  dark_mode: false,
  experiment_group: "variant_b",
});

// Remove a context:
Sentry.setContext("checkout", null);
```

> **Depth:** Sentry normalizes context to **3 levels deep** by default. Adjust via `normalizeDepth` in `Sentry.init`. The key `type` is reserved — don't use it in context objects.

---

### `Sentry.setTag(key, value)` / `Sentry.setTags(tags)` — Searchable Key-Value Pairs

Tags are **indexed and searchable**. They power Sentry's filter sidebar, tag distribution charts, and issue similarity detection. Use tags for any data you want to filter or aggregate on.

**Constraints:** Key ≤32 chars (`a-z A-Z 0-9 _ . : -`, no spaces). Value ≤200 chars, no newlines.

```javascript
// Single tag
Sentry.setTag("page_locale", "de-at");
Sentry.setTag("user_plan", "enterprise");
Sentry.setTag("app_version", "2.4.1");

// Multiple at once
Sentry.setTags({
  "release.stage": "canary",
  "tenant.id": "tenant_abc",
  "browser.engine": "blink",
});

// Per-event inline (does not persist to subsequent events)
Sentry.captureException(err, {
  tags: { component: "PaymentForm", retry_attempt: "2" },
});

// Scoped — only applies within the callback
Sentry.withScope((scope) => {
  scope.setTag("operation", "bulk-delete");
  Sentry.captureException(deleteError);
});
// "operation" tag does NOT appear on subsequent events
```

> Do not overwrite Sentry's built-in tags (`browser`, `os`, `url`, `environment`, `release`). Use your own namespaced keys.

---

### `Sentry.setExtra(key, value)` / `Sentry.setExtras(extras)` — Arbitrary Data

For loosely-typed supplementary data. Prefer `setContext` for structured data with a meaningful group name.

```javascript
Sentry.setExtra("raw_api_response", responseText);
Sentry.setExtra("debug_state_dump", JSON.stringify(stateSnapshot));

Sentry.setExtras({
  component_version: "3.2.1",
  last_action: "submit_form",
  form_fields: { total: 5, valid: 3, invalid: 2 },
});
```

---

### Inline Context on Capture Calls

All context can be provided per-event using the second argument to `captureException` or `captureMessage`. This is the cleanest approach for one-off enrichment:

```javascript
Sentry.captureException(err, {
  user: { id: "u_42", email: "user@example.com" },
  level: "fatal",
  tags: { module: "checkout", payment_provider: "stripe" },
  extra: { formState: JSON.stringify(formValues) },
  contexts: {
    payment: { provider: "stripe", last4: "4242", amount_cents: 9999 },
  },
  fingerprint: ["{{ default }}", "stripe-card-error"],
});
```

---

## Breadcrumbs

Breadcrumbs are a structured trail of events leading up to an error. They're buffered locally and attached to the next event sent to Sentry.

### Automatic Breadcrumbs (Zero Config)

| Type | What's Captured |
|------|----------------|
| `ui.click` | DOM element clicks (CSS selector or component name if annotation enabled) |
| `ui.input` | Keyboard/input interactions |
| `navigation` | URL changes: `pushState`, `popstate`, hash changes |
| `http` | XHR and `fetch` requests (URL, method, status code) |
| `console` | `console.log`, `warn`, `error`, `info`, `debug` output |
| `sentry` | SDK-internal events |

---

### `Sentry.addBreadcrumb(breadcrumb)` — Manual Breadcrumbs

```typescript
interface Breadcrumb {
  type?:      "default" | "debug" | "error" | "info" | "navigation" | "http" | "query" | "ui" | "user";
  category?:  string;      // dot-namespaced: "auth", "ui.click", "api.request"
  message?:   string;      // human-readable description
  level?:     "fatal" | "error" | "warning" | "log" | "info" | "debug";
  timestamp?: number;      // Unix timestamp in seconds (auto-set if omitted)
  data?:      Record<string, unknown>;
}
```

```javascript
// Auth events
Sentry.addBreadcrumb({
  category: "auth",
  message: "User logged in",
  level: "info",
  data: { userId: "u_42", method: "oauth2", provider: "google" },
});

Sentry.addBreadcrumb({
  category: "auth",
  message: "Token refresh failed",
  level: "warning",
  type: "error",
  data: { reason: "expired", expiredAt: "2024-01-15T10:00:00Z" },
});

// Navigation
Sentry.addBreadcrumb({
  type: "navigation",
  category: "navigation",
  message: "User navigated to checkout",
  data: { from: "/cart", to: "/checkout/payment" },
});

// API call outcome
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

// User actions
Sentry.addBreadcrumb({
  type: "user",
  category: "ui.click",
  message: "Clicked 'Place Order' button",
  data: { orderId: "ord_xyz", itemCount: 3, total: 99.99 },
});

// State machine transitions
Sentry.addBreadcrumb({
  category: "state",
  type: "debug",
  message: "State machine transitioned",
  level: "debug",
  data: { from: "PENDING", to: "PROCESSING", trigger: "user_submit" },
});
```

---

### Filtering Breadcrumbs — `beforeBreadcrumb`

Configured in `Sentry.init`. Return `null` to discard a breadcrumb entirely.

```javascript
Sentry.init({
  beforeBreadcrumb(breadcrumb, hint) {
    // Drop clicks on password fields (privacy)
    if (breadcrumb.category === "ui.click") {
      const target = hint?.event?.target;
      if (target?.type === "password") return null;
    }

    // Enrich XHR breadcrumbs with request body size
    if (breadcrumb.type === "http" && hint?.xhr) {
      breadcrumb.data = {
        ...breadcrumb.data,
        requestBodySize: hint.xhr.requestBody?.length ?? 0,
      };
    }

    // Drop verbose console.debug breadcrumbs in production
    if (breadcrumb.category === "console" && breadcrumb.level === "debug") {
      return null;
    }

    return breadcrumb;
  },
});
```

**`maxBreadcrumbs`** — Controls how many breadcrumbs are stored. Default: 100. Set in `Sentry.init`:

```javascript
Sentry.init({ maxBreadcrumbs: 50 });
```

---

## Scopes

Scopes are how Sentry attaches context (tags, user, breadcrumbs, extras) to events. Three scope types are merged before each event is sent.

### The Three Scope Types

| Scope | API | Lifetime | Written by |
|-------|-----|----------|-----------|
| **Global** | `Sentry.getGlobalScope()` | Entire process | You (set once) |
| **Isolation** | `Sentry.getIsolationScope()` | Current page/request | `Sentry.setTag()` etc. |
| **Current** | `Sentry.getCurrentScope()` | Innermost execution | `Sentry.withScope()` |

**Merge priority (later wins):**
```
Global → Isolation → Current → Event Sent
(lowest priority)              (highest priority)
```

---

### Global Scope — `Sentry.getGlobalScope()`

Applied to **every event** from anywhere in the app. Use for universal data: app version, build ID, deployment region.

```javascript
const globalScope = Sentry.getGlobalScope();
globalScope.setTag("app_version", "2.4.1");
globalScope.setTag("build_id", import.meta.env.VITE_BUILD_ID);
globalScope.setContext("deployment", {
  region: "us-east-1",
  datacenter: "aws",
  env: "production",
});
```

> **Cannot capture events** — only stores data.

---

### Isolation Scope — `Sentry.getIsolationScope()`

In the **browser**, the isolation scope is effectively global — only one ever exists per page load (unlike Node where it's forked per request). All top-level `Sentry.setXxx()` methods write here.

```javascript
// These two are identical in the browser:
Sentry.setTag("user_plan", "pro");
Sentry.getIsolationScope().setTag("user_plan", "pro");

// On login — persists for all subsequent events on this page:
Sentry.setUser({ id: "u_42", email: "user@example.com" });

// On logout — clears user from isolation scope:
Sentry.setUser(null);
```

> **Cannot capture events** — only stores data.

---

### `Sentry.withScope(callback)` — Scoped Modifications

Creates a **fork** of the current scope, active only within the callback. Modifications do not leak to subsequent events. The most important tool for per-event enrichment without polluting global state.

```javascript
// Add context to one specific capture only
Sentry.withScope((scope) => {
  scope.setTag("operation", "bulk-delete");
  scope.setLevel("warning");
  scope.setContext("bulk", { count: items.length, userId: currentUser.id });
  Sentry.captureException(deleteError);
});
// "operation" tag does NOT appear on any subsequent events

// Rich per-operation isolation
async function processPayment(order) {
  try {
    await stripe.charge(order);
  } catch (err) {
    Sentry.withScope((scope) => {
      scope.setTag("module", "payments");
      scope.setTag("payment_provider", "stripe");
      scope.setLevel("fatal");
      scope.setUser({ id: order.userId });
      scope.setContext("order", {
        id: order.id,
        amount: order.amount,
        currency: order.currency,
        items: order.items.length,
      });
      scope.setExtra("stripe_error_code", err.code);
      scope.addBreadcrumb({
        category: "payment",
        message: "Stripe charge attempt failed",
        level: "error",
        data: { stripeCode: err.code, message: err.message },
      });
      Sentry.captureException(err);
    });
  }
}

// addEventProcessor inside a scope — transform the event before it's sent
Sentry.withScope((scope) => {
  scope.addEventProcessor((event) => {
    event.tags = { ...event.tags, processed_by: "payment_handler" };
    return event;
  });
  Sentry.captureException(err);
});
```

---

### Scope Decision Guide

| Goal | API |
|------|-----|
| Data on ALL events (app version, build ID) | `Sentry.getGlobalScope().setTag(...)` |
| Data on current page view / user session | `Sentry.setTag(...)` (isolation scope) |
| Data on ONE specific capture | `Sentry.withScope((scope) => { ... })` |
| Data inline on a single event | Second arg to `captureException(err, { tags: {...} })` |

> **Do NOT use `Sentry.configureScope()`** — deprecated since SDK v8. Use `getIsolationScope()` or `getGlobalScope()` instead.

---

## Event Filtering

### `beforeSend(event, hint)` — Modify or Drop Events

Called before every error event is sent. Return `null` to drop the event. Mutate `event` to scrub or enrich it.

```javascript
Sentry.init({
  beforeSend(event, hint) {
    const originalError = hint.originalException;

    // Drop non-Error rejections (e.g. cancelled requests)
    if (originalError && !(originalError instanceof Error)) {
      return null;
    }

    // Drop browser extension errors
    if (event.exception?.values?.[0]?.stacktrace?.frames?.some(
      frame => frame.filename?.includes("extension://")
    )) {
      return null;
    }

    // Drop 404 errors from event handlers
    if (originalError?.message?.includes("404")) {
      return null;
    }

    // Scrub PII from user context
    if (event.user?.email) {
      event.user = { ...event.user, email: "[filtered]" };
    }

    // Override fingerprint for known error patterns
    if (originalError?.message?.includes("ChunkLoadError")) {
      event.fingerprint = ["chunk-load-error"];
    }

    return event;
  },
});
```

**Accessing the original error from `hint`:**

```javascript
beforeSend(event, hint) {
  const error = hint.originalException;  // The original Error object
  const syntheticEvent = hint.syntheticException;  // SDK-generated error for messages

  if (error instanceof TypeError && error.message === "Failed to fetch") {
    // Enrich with tag instead of dropping
    event.tags = { ...event.tags, network_error: "true" };
  }
  return event;
}
```

---

### `ignoreErrors` — Pattern-Based Filtering

Array of string or RegExp patterns. Events whose error message matches any pattern are silently dropped before `beforeSend`.

```javascript
Sentry.init({
  ignoreErrors: [
    // Exact strings (substring match):
    "ResizeObserver loop limit exceeded",
    "Non-Error exception captured",
    "Object Not Found Matching Id",

    // Regular expressions:
    /^Network Error$/,
    /ChunkLoadError/,
    /Loading chunk \d+ failed/,
    /^Script error\.?$/,       // cross-origin script errors with no details

    // Browser extension noise:
    "from accessing a cross-origin frame",
    /webkit-masked-url/,
  ],
});
```

---

### `allowUrls` / `denyUrls` — URL-Based Filtering

Only capture errors (or skip errors) from scripts at specific URLs.

```javascript
Sentry.init({
  // Only capture errors originating from your own scripts:
  allowUrls: [
    /https:\/\/yourapp\.com/,
    /https:\/\/cdn\.yourapp\.com/,
  ],

  // Skip errors from known third-party noise:
  denyUrls: [
    /extensions\//i,
    /^chrome:\/\//i,
    /^safari-extension:\/\//i,
    /gtm\.js/,
    /analytics\.js/,
  ],
});
```

---

### `sampleRate` — Capture Only a Fraction of Errors

```javascript
Sentry.init({
  sampleRate: 0.25,  // Capture 25% of errors (randomly sampled)
});
```

> Use `beforeSend` for conditional filtering (based on error type, URL, user). Use `sampleRate` for volume reduction when error rates are very high.

---

## Fingerprinting

### Default Grouping Behavior

Sentry groups errors into issues by default using a combination of: exception type, exception message, and stack trace. This works well for most cases but can produce false groupings for dynamic error messages.

### Custom Fingerprinting

Override grouping by providing a `fingerprint` array on the event.

```javascript
// All Stripe card errors grouped together regardless of message:
Sentry.captureException(err, {
  fingerprint: ["stripe-card-error"],
});

// Use {{ default }} to extend (not replace) Sentry's default grouping:
Sentry.captureException(err, {
  fingerprint: ["{{ default }}", "payment-module"],
});

// Dynamic component — group by component name + error type:
Sentry.captureException(err, {
  fingerprint: ["DataGrid", err.constructor.name],
});
```

**Via `beforeSend` for pattern-based fingerprinting:**

```javascript
Sentry.init({
  beforeSend(event, hint) {
    const error = hint.originalException;

    // Group all network timeouts as one issue:
    if (error?.message?.includes("timeout")) {
      event.fingerprint = ["network-timeout"];
    }

    // Group chunk load failures as one issue:
    if (error?.name === "ChunkLoadError") {
      event.fingerprint = ["chunk-load-failure"];
    }

    return event;
  },
});
```

---

## User Feedback

### When to Use Which Mechanism

| | `feedbackIntegration()` Widget | `Sentry.showReportDialog()` |
|---|---|---|
| **Trigger** | Anytime — user-initiated | On error — automatic |
| **UI** | Floating button (bottom-right) | Modal overlay |
| **Requires error?** | No | Yes (`eventId` required) |
| **Screenshots** | Yes (SDK ≥8.0.0) | No |
| **Best for** | General feedback, bug reports | Post-crash reports |

---

### `feedbackIntegration()` — Persistent Feedback Widget

Adds a floating feedback button to the page. Users submit feedback at any time — no error required.

```javascript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "___PUBLIC_DSN___",
  integrations: [
    Sentry.feedbackIntegration({
      colorScheme: "system", // "system" | "light" | "dark"
    }),
  ],
});
```

#### Complete Configuration Reference

```javascript
Sentry.feedbackIntegration({
  // ── Behavior ──────────────────────────────────────────────────────────
  autoInject: true,         // Auto-inject button into DOM. Set false for programmatic control.
  colorScheme: "system",    // "system" | "light" | "dark"
  showBranding: true,       // Show "Powered by Sentry" logo
  id: "sentry-feedback",    // Container div ID
  tags: {                   // Sentry tags on all feedback submissions
    product_area: "checkout",
    version: "2.4.1",
  },

  // ── User Fields ───────────────────────────────────────────────────────
  showName: true,
  showEmail: true,
  isNameRequired: false,
  isEmailRequired: false,
  enableScreenshot: true,   // Allow screenshot attachment (SDK ≥8.0.0, hidden on mobile)
  useSentryUser: {
    email: "email",         // Which Sentry user field maps to the email input
    name: "username",       // Which Sentry user field maps to the name input
  },

  // ── Labels / Text ─────────────────────────────────────────────────────
  triggerLabel: "Report a Bug",
  triggerAriaLabel: "Report a Bug",   // v8.20.0+
  formTitle: "Report a Bug",
  submitButtonLabel: "Send Bug Report",
  cancelButtonLabel: "Cancel",
  confirmButtonLabel: "Confirm",
  addScreenshotButtonLabel: "Add a screenshot",
  removeScreenshotButtonLabel: "Remove screenshot",
  nameLabel: "Name",
  namePlaceholder: "Your Name",
  emailLabel: "Email",
  emailPlaceholder: "your.email@example.org",
  isRequiredLabel: "(required)",
  messageLabel: "Description",
  messagePlaceholder: "What's the bug? What did you expect?",
  successMessageText: "Thank you for your report!",
  // Screenshot annotation labels (v10.10.0+):
  highlightToolText: "Highlight",
  hideToolText: "Hide",
  removeHighlightText: "Remove",

  // ── Theme Overrides ───────────────────────────────────────────────────
  themeLight: {
    foreground: "#2b2233",
    background: "#ffffff",
    accentForeground: "#ffffff",
    accentBackground: "#6a3fc8",
    successColor: "#268d75",
    errorColor: "#df3338",
  },
  themeDark: {
    foreground: "#ebe6ef",
    background: "#29232f",
    accentForeground: "#ffffff",
    accentBackground: "#6a3fc8",
    successColor: "#2da98c",
    errorColor: "#f55459",
  },

  // ── Callbacks ─────────────────────────────────────────────────────────
  onFormOpen: () => analytics.track("feedback_form_opened"),
  onFormClose: () => analytics.track("feedback_form_closed_without_submit"),
  onSubmitSuccess: (data, eventId) => {
    // data: { name, email, message }
    toast.success(`Thanks! Reference: ${eventId}`);
  },
  onSubmitError: (error) => {
    toast.error("Failed to submit feedback. Please try again.");
  },
})
```

**Programmatic control (when `autoInject: false`):**

```javascript
// In Sentry.init
const feedbackIntegration = Sentry.feedbackIntegration({ autoInject: false });
Sentry.init({ integrations: [feedbackIntegration] });

// Elsewhere — open the widget from a button:
document.getElementById("feedback-btn").addEventListener("click", () => {
  feedbackIntegration.openDialog();
});

// Or attach to a DOM element (converts it to a trigger):
feedbackIntegration.attachTo(document.getElementById("help-menu-item"));
```

---

### `Sentry.captureFeedback(feedback, hints?)` — Programmatic Feedback API

Submit feedback without any UI. Ideal for custom feedback forms you build yourself.

```javascript
// Basic
Sentry.captureFeedback({
  name: "John Doe",
  email: "john@example.com",
  message: "The export button does nothing on Firefox.",
});

// With capture context and attachments
Sentry.captureFeedback(
  {
    name: "Jane Smith",
    email: "jane@example.com",
    message: "Chart data looks wrong after filtering by date.",
  },
  {
    captureContext: {
      tags: { page: "analytics-dashboard", browser: navigator.userAgent },
      extra: { chartConfig: JSON.stringify(currentChartConfig) },
    },
    attachments: [
      {
        filename: "screenshot.png",
        data: new Uint8Array(screenshotBuffer),
        contentType: "image/png",
      },
    ],
  }
);
```

---

### `Sentry.showReportDialog(options)` — Crash-Report Modal

Shows a user-facing modal after an error. **Requires** an `eventId` to link the feedback to a Sentry event.

**From `onError` in `ErrorBoundary`:**

```jsx
<Sentry.ErrorBoundary
  onError={(error, componentStack, eventId) => {
    Sentry.showReportDialog({
      eventId,
      user: { name: currentUser.name, email: currentUser.email },
    });
  }}
  fallback={<ErrorScreen />}
>
  <App />
</Sentry.ErrorBoundary>
```

**From `beforeSend`:**

```javascript
Sentry.init({
  beforeSend(event, hint) {
    if (event.exception && event.event_id) {
      Sentry.showReportDialog({ eventId: event.event_id });
    }
    return event;
  },
});
```

**From a manual catch:**

```javascript
function handleCriticalError(err) {
  const eventId = Sentry.captureException(err);
  Sentry.showReportDialog({
    eventId,
    user: { name: auth.user.displayName, email: auth.user.email },
    title: "It looks like we're having issues.",
    subtitle: "Our team has been notified.",
    subtitle2: "If you'd like to help, tell us what happened below.",
    labelComments: "Steps to reproduce:",
    labelSubmit: "Send Report",
    successMessage: "Your feedback has been sent. Thank you!",
  });
}
```

#### Complete `showReportDialog` Options

| Option | Type | Notes |
|--------|------|-------|
| `eventId` | `string` | **Required.** Links feedback to the Sentry event |
| `dsn` | `string` | Override DSN (defaults to `Sentry.init` DSN) |
| `user.name` | `string` | Pre-fill the name field |
| `user.email` | `string` | Pre-fill the email field |
| `lang` | `string` | ISO language code (e.g. `"de"`, `"fr"`, `"ja"`) |
| `title` | `string` | Modal header text |
| `subtitle` | `string` | First subtitle line |
| `subtitle2` | `string` | Second subtitle line |
| `labelName` | `string` | Label for the name field |
| `labelEmail` | `string` | Label for the email field |
| `labelComments` | `string` | Label for the description field |
| `labelSubmit` | `string` | Submit button text |
| `labelClose` | `string` | Close button text |
| `successMessage` | `string` | Shown after successful submission |
| `onLoad` | `() => void` | Called when dialog opens |
| `onClose` | `() => void` | Called when dialog closes (v7.82.0+) |

---

## React Router — Critical Error Boundary Note

React Router's **default error boundary silently discards errors in production**. Always provide a custom `errorElement` that captures to Sentry:

```jsx
import { useRouteError } from "react-router-dom";
import * as Sentry from "@sentry/react";

function RootErrorBoundary() {
  const error = useRouteError();

  React.useEffect(() => {
    if (error instanceof Error) {
      Sentry.captureException(error, {
        tags: { source: "react-router-error-element" },
      });
    }
  }, [error]);

  return (
    <div>
      <h1>Something went wrong</h1>
      <p>{error instanceof Error ? error.message : "An unexpected error occurred."}</p>
      <button onClick={() => window.location.reload()}>Reload page</button>
    </div>
  );
}

const router = Sentry.wrapCreateBrowserRouterV6(createBrowserRouter)([
  {
    path: "/",
    element: <Layout />,
    errorElement: <RootErrorBoundary />,  // ← required
    children: [ /* your routes */ ],
  },
]);
```

---

## Quick Reference

```javascript
// ── Capture APIs ──────────────────────────────────────────────────────
Sentry.captureException(error)
Sentry.captureException(error, { level, tags, extra, contexts, fingerprint, user })
Sentry.captureMessage("text", "warning")
Sentry.captureMessage("text", { level, tags, extra })
Sentry.captureEvent({ message, level, tags, extra, timestamp })
Sentry.captureReactException(error, reactErrorInfo)   // ≥9.8.0 — custom class boundaries

// ── React 19+ Error Hooks ─────────────────────────────────────────────
createRoot(el, {
  onUncaughtError:   Sentry.reactErrorHandler(optionalCallback),
  onCaughtError:     Sentry.reactErrorHandler(),
  onRecoverableError: Sentry.reactErrorHandler(),
})
hydrateRoot(el, <App />, { /* same three hooks */ })

// ── Error Boundaries (React 16+) ──────────────────────────────────────
<Sentry.ErrorBoundary
  fallback={<UI /> | ({ error, componentStack, resetError }) => <UI />}
  onError={(error, stack, eventId) => {}}
  beforeCapture={(scope, error, stack) => {}}
  onReset={(error, stack, eventId) => {}}
  showDialog  dialogOptions={{}}
  onMount={() => {}}  onUnmount={(error) => {}}
>
Sentry.withErrorBoundary(Component, options)   // HOC equivalent

// ── Context ───────────────────────────────────────────────────────────
Sentry.setUser({ id, email, username, ip_address, segment, ...custom })
Sentry.setUser(null)                           // clear on logout
Sentry.setTag("key", "value")
Sentry.setTags({ key1: "v1", key2: "v2" })
Sentry.setContext("name", { key: value })      // structured, not searchable
Sentry.setContext("name", null)                // remove context
Sentry.setExtra("key", value)
Sentry.setExtras({ key1: v1 })

// ── Breadcrumbs ───────────────────────────────────────────────────────
Sentry.addBreadcrumb({ type, category, message, level, data, timestamp })

// ── Scopes ────────────────────────────────────────────────────────────
Sentry.withScope((scope) => { scope.setTag(...); Sentry.captureException(...) })
Sentry.getGlobalScope()          // all events, process lifetime
Sentry.getIsolationScope()       // current page/session (= Sentry.setTag etc.)
// DON'T: Sentry.configureScope() — deprecated since SDK v8

// ── Filtering ─────────────────────────────────────────────────────────
// Sentry.init({ beforeSend, ignoreErrors, allowUrls, denyUrls, sampleRate })

// ── User Feedback ─────────────────────────────────────────────────────
Sentry.feedbackIntegration({ colorScheme, autoInject, showName, isEmailRequired, ... })
Sentry.captureFeedback({ name, email, message }, { captureContext, attachments })
Sentry.showReportDialog({ eventId, user, title, subtitle, ... })
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Errors appearing twice in development | Expected behavior — React Strict Mode re-throws caught errors to the global handler. Validate in production builds only. |
| Missing component stack in issues | Requires React 17+. Ensure `LinkedErrors` integration is enabled (it is by default). |
| React Router errors not captured | React Router's default boundary swallows errors. Add a custom `errorElement` that calls `captureException`. |
| `CaptureConsole` causing duplicates | React logs caught errors via `console.error`. Remove `CaptureConsole` or exclude `console.error` from its config. |
| `captureReactException` not available | Upgrade to `@sentry/react` ≥9.8.0. |
| `reactErrorHandler` not available | Upgrade to `@sentry/react` ≥8.6.0. |
| Errors captured without user context | Call `Sentry.setUser()` after login, not inside `Sentry.init`. It must be called after authentication completes. |
| `configureScope is not a function` | Deprecated in SDK v8. Replace with `getIsolationScope()` or `withScope()`. |
| Tags not appearing on events | Tags set via `Sentry.setTag()` go to the isolation scope; verify you're not clearing it unexpectedly. |
| `showReportDialog` shows but has no event | Pass `eventId` from `Sentry.captureException(err)` return value or from `onError` prop. |
| `feedbackIntegration` button not appearing | Confirm `feedbackIntegration()` is in the `integrations` array in `Sentry.init`. Check for z-index conflicts. |
| `beforeSend` returning `null` but events still sent | Check `beforeSendTransaction` — a separate hook for performance events. Also verify no other SDK instance is active. |
| High event volume from known errors | Add patterns to `ignoreErrors`, or use `sampleRate` to reduce volume. Use `beforeSend` for type-specific filtering. |
| Errors from browser extensions captured | Add `/extensions\//i` and `/^chrome:\/\//i` to `denyUrls`. |

---

## Reference: Logging

# Logging — Sentry React SDK

> Minimum SDK: `@sentry/react` ≥9.41.0+ for `Sentry.logger` API and `enableLogs`  
> `consoleLoggingIntegration()`: requires ≥10.13.0+  
> Scope-based attributes (`getGlobalScope`, `getIsolationScope`): requires ≥10.32.0+

> ⚠️ **Not available via CDN/loader snippet** — NPM install required.

---

## Enabling Logs

`enableLogs` is opt-in and must be explicitly set in `Sentry.init()`:

```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  enableLogs: true, // Required — logging is disabled by default
});
```

Without `enableLogs: true`, all `Sentry.logger.*` calls are silently no-ops and nothing is sent to Sentry.

---

## Logger API — Six Levels

```typescript
import * as Sentry from "@sentry/react";

Sentry.logger.trace("Entering processOrder", { fn: "processOrder", orderId: "ord_1" });
Sentry.logger.debug("Cache lookup", { key: "user:123", hit: false });
Sentry.logger.info("Order created", { orderId: "order_456", total: 99.99 });
Sentry.logger.warn("Rate limit approaching", { current: 95, max: 100 });
Sentry.logger.error("Payment failed", { reason: "card_declined", userId: "u_1" });
Sentry.logger.fatal("Database unavailable", { host: "db-primary" });
```

| Level | Method | Typical Use |
|-------|--------|-------------|
| `trace` | `Sentry.logger.trace()` | Ultra-granular function entry/exit; high-volume — filter aggressively in production |
| `debug` | `Sentry.logger.debug()` | Development diagnostics, cache hits/misses, local state changes |
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

Each parameter is independently searchable in Sentry's log explorer. You can filter by `message.parameter.0 = "user_123"` without matching the full message string.

> ⚠️ `logger.fmt` must be used as a **tagged template literal** — not as a function call. `Sentry.logger.fmt("text")` will not produce structured parameters.

### When to use `fmt` vs plain attributes

| Approach | Use when |
|----------|----------|
| `Sentry.logger.info(msg, { key: val })` | Variables are logically distinct attributes with names |
| `Sentry.logger.info(Sentry.logger.fmt\`...\`)` | Variables are part of a human-readable sentence |

---

## Console Capture — `consoleLoggingIntegration`

Automatically forwards `console.*` calls to Sentry as structured logs. Requires SDK ≥10.13.0.

```typescript
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  enableLogs: true,
  integrations: [
    Sentry.consoleLoggingIntegration({
      levels: ["log", "warn", "error"], // which console methods to forward
    }),
  ],
});

// These calls are now automatically sent to Sentry:
console.log("User action recorded", { userId: 123 });
console.warn("Slow render detected", 240, "ms");
console.error("Fetch failed", new Error("timeout"));
```

Multiple arguments are mapped to positional parameters:
```
console.log("Text", 123, true)
  → message.parameter.0 = 123
  → message.parameter.1 = true
```

### Capturable console levels

| Console method | Sentry log level |
|----------------|-----------------|
| `console.log` | `info` |
| `console.info` | `info` |
| `console.warn` | `warn` |
| `console.error` | `error` |
| `console.debug` | `debug` |
| `console.assert` (failing) | `error` |

Configure `levels` to include only the methods you want forwarded.

---

## Log Filtering — `beforeSendLog`

Use `beforeSendLog` to drop, modify, or scrub logs before they leave the client. Return `null` to discard:

```typescript
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
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

## Structured Attributes

Every `Sentry.logger.*` call accepts an attributes object as its second argument:

```typescript
Sentry.logger.info("Checkout completed", {
  orderId: "ord_789",
  userId: "usr_123",
  cartValue: 149.99,
  itemCount: 3,
  paymentMethod: "stripe",
  userTier: "premium",
  duration: Date.now() - startTime,
});
```

Attributes become **searchable and filterable** in Sentry's log explorer. Prefer one comprehensive log with all relevant context over many small scattered logs ("wide events").

---

## Scope-Based Automatic Attributes (SDK ≥10.32.0)

Attributes set on scopes are automatically added to all logs emitted within that scope.

### Global scope — entire session

```typescript
// Set once at app startup — persists for the lifetime of the page
Sentry.getGlobalScope().setAttributes({
  service: "react-checkout",
  version: "2.1.0",
  region: "us-east-1",
});
```

### Isolation scope — logical user session context

```typescript
// Set after user authenticates
Sentry.getIsolationScope().setAttributes({
  org_id: user.orgId,
  user_tier: user.tier,
  account_type: user.accountType,
});
```

### Current scope — single operation

```typescript
Sentry.withScope((scope) => {
  scope.setAttribute("order_id", "ord_789");
  scope.setAttribute("payment_method", "stripe");
  Sentry.logger.info("Processing payment", { amount: 49.99 });
  // order_id and payment_method are included on this log only
});
```

**Constraint:** Scope attributes accept only `string`, `number`, and `boolean` values — no arrays or objects.

---

## Auto-Generated Attributes

These are added by the SDK to every log without any developer configuration:

| Attribute | Source | Notes |
|-----------|--------|-------|
| `sentry.environment` | `environment` in `Sentry.init()` | — |
| `sentry.release` | `release` in `Sentry.init()` | — |
| `sentry.sdk.name` | SDK internals | e.g., `"sentry.javascript.react"` |
| `sentry.sdk.version` | SDK internals | — |
| `browser.name` | User-Agent parsing | e.g., `"Chrome"` |
| `browser.version` | User-Agent parsing | e.g., `"121.0.0"` |
| `user.id`, `user.name`, `user.email` | `Sentry.setUser()` | Requires `sendDefaultPii: true` |
| `sentry.trace.parent_span_id` | Active tracing span | Enables log ↔ trace correlation |
| `sentry.replay_id` | Active Session Replay session | Enables log ↔ replay correlation |
| `message.template` | `logger.fmt` usage | The template string |
| `message.parameter.N` | `logger.fmt` usage | Each interpolated value |

---

## Log-to-Trace Correlation

When tracing is enabled alongside logging, logs are **automatically linked** to the active span:

```typescript
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  enableLogs: true,
  tracesSampleRate: 1.0,
  integrations: [Sentry.browserTracingIntegration()],
});

// Logs emitted inside a span are linked to it automatically
await Sentry.startSpan({ name: "checkout-flow", op: "ui.action" }, async () => {
  Sentry.logger.info("Validating cart", { cartId: "cart_abc" });
  await validateCart();
  Sentry.logger.info("Initiating payment", { gateway: "stripe" });
  await initiatePayment();
});
// Both logs above have sentry.trace.parent_span_id set to the checkout-flow span ID
```

In the Sentry UI:
- **From a log** → click the trace link to jump to the parent span and full trace
- **From a trace span** → click "Logs" to see all logs emitted during that span
- **From a replay** → logs are shown inline with the user session recording

---

## React-Specific Best Practice: Wide Events

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
  activeFeatureFlags: user.flags.join(","),
  durationMs: Date.now() - startTime,
});

// ❌ Avoid — fragmented logs with poor context
Sentry.logger.info("Order ID set", { orderId: order.id });
Sentry.logger.info("Cart total calculated", { cartValue: cart.total });
Sentry.logger.info("Checkout done");
```

---

## When to Use Each API

| Scenario | Recommended API |
|----------|----------------|
| Business event with structured data | `Sentry.logger.info(msg, { ...attrs })` |
| Message with embedded variables | `Sentry.logger.info(Sentry.logger.fmt\`...\`)` |
| Capture an unexpected exception | `Sentry.captureException(err)` |
| Send an informational string event | `Sentry.captureMessage(msg, "info")` |
| Auto-capture existing `console.*` calls | `consoleLoggingIntegration({ levels: [...] })` |

Use `Sentry.logger.*` for **structured, searchable observability data**. Use `captureException` for actual errors that need issue grouping and stack traces.

---

## Log Level Guide

| Level | When to use | Production volume |
|-------|-------------|-----------------|
| `trace` | Function entry/exit, loop iterations | Filter out in production |
| `debug` | Variable values, code paths taken | Filter out in production |
| `info` | User actions, business milestones, API calls | Keep — low/medium volume |
| `warn` | Degraded paths, retries, near-limits | Keep — low volume |
| `error` | Failures that need investigation | Keep — should be rare |
| `fatal` | System-down, unrecoverable state | Keep — should be very rare |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing in Sentry | Verify `enableLogs: true` is in `Sentry.init()`; requires SDK ≥9.41.0 |
| `logger.fmt` not creating `message.parameter.*` | Use as tagged template: `Sentry.logger.fmt\`text ${var}\`` — not `Sentry.logger.fmt("text", var)` |
| Logs not linked to traces | Ensure `browserTracingIntegration()` is added and `tracesSampleRate` > 0; logs must be emitted inside an active span |
| `consoleLoggingIntegration` not available | Upgrade to `@sentry/react` ≥10.13.0 |
| Scope attributes not appearing on logs | Upgrade to `@sentry/react` ≥10.32.0 for `getGlobalScope`/`getIsolationScope` APIs |
| Too many logs — high volume / costs | Use `beforeSendLog` to drop `trace` and `debug` levels in production |
| Log attributes contain `undefined` | Only `string`, `number`, `boolean` are accepted — filter undefined values before passing |
| `beforeSendLog` not firing | Confirm `enableLogs: true` is set; without it, no logs are sent and no hook is called |
| Sensitive data appearing in logs | Add filtering in `beforeSendLog`; better yet, avoid logging sensitive data at the call site |
| Logs appear but have no user context | Call `Sentry.setUser({ id, email })` after authentication and set `sendDefaultPii: true` |

---

## Reference: Profiling

# Browser Profiling — Sentry React SDK

> Minimum SDK: `@sentry/react` ≥10.27.0+ (Beta)

> ⚠️ **Beta status** — breaking changes may occur. Browser support is limited to Chromium-based browsers only.

---

## What Browser Profiling Captures

Sentry's browser profiler uses the [JS Self-Profiling API](https://wicg.github.io/js-self-profiling/) to capture:

- **JavaScript call stacks** — function names and source file locations (deobfuscated via source maps)
- **CPU time per function** — how much time is spent in each function
- **Flame graphs** — aggregated across real user sessions, not just local dev
- **Linked profiles** — every profile is attached to a trace, enabling navigation from span → flame graph in the Sentry UI

Sampling rate: **100Hz (10ms intervals)** — contrast with Chrome DevTools at 1000Hz (1ms). Less granular, but runs unobtrusively in production.

---

## Browser Compatibility

| Browser | Supported | Notes |
|---------|-----------|-------|
| Chrome / Chromium | ✅ Yes | Primary support target |
| Edge (Chromium) | ✅ Yes | Same engine as Chrome |
| Firefox | ❌ No | Does not implement JS Self-Profiling API |
| Safari / iOS Safari | ❌ No | Does not implement JS Self-Profiling API |

> ⚠️ **Sampling bias:** Profile data is collected **only** from Chromium users. Firefox and Safari sessions are silently not profiled. Consider this when drawing performance conclusions.

In unsupported browsers, `browserProfilingIntegration()` **silently no-ops** — no errors thrown, no overhead.

---

## Required HTTP Header

Every document response serving your React app **must** include this header or profiling silently fails:

```
Document-Policy: js-profiling
```

Without this header, the JS Self-Profiling API is blocked by the browser and no profiles are collected.

### Platform-Specific Header Setup

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

**Netlify (`_headers` file):**
```
/*
  Document-Policy: js-profiling
```

**Express / Node.js:**
```javascript
app.use((req, res, next) => {
  res.set("Document-Policy", "js-profiling");
  next();
});
```

**Nginx (`nginx.conf`):**
```nginx
server {
  location / {
    add_header Document-Policy "js-profiling";
  }
}
```

**Apache (`.htaccess`):**
```apache
<IfModule mod_headers.c>
  Header set Document-Policy "js-profiling"
</IfModule>
```

**AWS CloudFront (Viewer Response function):**
```javascript
function handler(event) {
  var response = event.response;
  response.headers["document-policy"] = { value: "js-profiling" };
  return response;
}
```

**ASP.NET Core (`Program.cs`):**
```csharp
app.Use(async (context, next) => {
  context.Response.OnStarting(() => {
    context.Response.Headers.Append("Document-Policy", "js-profiling");
    return Task.CompletedTask;
  });
  await next();
});
```

> ⚠️ **Static hosting that disallows custom headers** (some CDNs, GitHub Pages) will prevent profiling entirely.

---

## Setup

### Install

```bash
npm install @sentry/react --save
```

### SDK Initialization — Trace Mode (recommended)

Trace mode automatically attaches profiles to all sampled spans. Use this for general production coverage:

```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,

  integrations: [
    Sentry.browserTracingIntegration(), // Must come BEFORE browserProfilingIntegration
    Sentry.browserProfilingIntegration(),
  ],

  // Tracing — profiles are only collected when a transaction is also sampled
  tracesSampleRate: 1.0,

  // Profiling — fraction of sessions to profile
  profileSessionSampleRate: 1.0,

  // "trace" = automatically attach profiles to all active spans
  profileLifecycle: "trace",
});
```

### SDK Initialization — Manual Mode

Manual mode lets you profile specific user flows or code paths explicitly:

```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,

  integrations: [
    Sentry.browserTracingIntegration(),
    Sentry.browserProfilingIntegration(),
  ],

  tracesSampleRate: 1.0,
  profileSessionSampleRate: 1.0,
  // Omit profileLifecycle for manual mode (default)
});

// Later, wrap specific operations:
Sentry.uiProfiler.startProfiler();
// ... user flow or expensive computation ...
Sentry.uiProfiler.stopProfiler();
```

---

## Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tracesSampleRate` | `number` | — | 0.0–1.0 — fraction of transactions traced; profiles only attach to traced transactions |
| `profileSessionSampleRate` | `number` | — | 0.0–1.0 — session-level sampling decision for profiling |
| `profileLifecycle` | `"trace"` | — | Set to `"trace"` for Trace mode; omit for Manual mode |
| `tracePropagationTargets` | `(string\|RegExp)[]` | — | URLs where distributed trace headers are injected |

---

## How Profiles Attach to Traces

Profiles are **not independent** from tracing — they attach to transactions:

1. `tracesSampleRate` determines whether a transaction is traced at all
2. `profileSessionSampleRate` determines whether the **session** opts into profiling
3. A profile is only collected when **both** sampling decisions are yes

**Compound sampling example:**
- `tracesSampleRate: 0.5` + `profileSessionSampleRate: 0.5` → ~25% of sessions produce profiles
- `tracesSampleRate: 1.0` + `profileSessionSampleRate: 1.0` → 100% (development/testing only)

In the Sentry UI, open a trace and click **"Profile"** to view the flame graph for that transaction.

---

## Profiling Modes Comparison

| Mode | How to trigger | Best for |
|------|---------------|----------|
| **Trace** (`profileLifecycle: "trace"`) | Auto-attached to every sampled span | Broad production coverage |
| **Manual** (default) | `uiProfiler.startProfiler()` / `stopProfiler()` | Specific high-value flows (checkout, render) |

---

## Sentry Profiling vs Chrome DevTools

| Aspect | Sentry Browser Profiling | Chrome DevTools |
|--------|--------------------------|-----------------|
| Environment | Production (real users) | Local development only |
| Sampling rate | 100Hz (10ms) | 1000Hz (1ms) |
| Stack traces | Deobfuscated via source maps | Minified names unless local |
| Data scope | Aggregated across all sessions | Single local session |
| Browser coverage | Chromium only | Any browser with DevTools |
| Overhead | Low (production-safe) | Higher — not production-safe |

> ⚠️ **Chrome DevTools conflict:** When `browserProfilingIntegration` is active, Chrome DevTools profiles incorrectly show profiling overhead mixed into rendering work. Disable the integration when doing local DevTools profiling sessions.

---

## Source Maps — Critical for Useful Profiles

Without source maps, flame graphs show **minified function names** like `e`, `t`, `r` — effectively unreadable.

With source maps uploaded to Sentry, flame graphs show **original function names** and file paths from your source code.

**Setup source maps with the Vite plugin** (handles both source map upload and component annotation):

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { sentryVitePlugin } from "@sentry/vite-plugin";

export default defineConfig({
  build: {
    sourcemap: "hidden", // Generate maps but don't serve them publicly
  },
  plugins: [
    react(),
    sentryVitePlugin({
      org: process.env.SENTRY_ORG,
      project: process.env.SENTRY_PROJECT,
      authToken: process.env.SENTRY_AUTH_TOKEN,
      sourcemaps: {
        filesToDeleteAfterUpload: ["./**/*.map"],
      },
    }),
  ],
});
```

See the main SKILL.md **Source Maps Setup** section for Webpack/CRA configuration.

---

## Limitations

| Limitation | Detail |
|-----------|--------|
| **Beta status** | API is experimental; breaking changes possible between releases |
| **Chromium only** | No Firefox, no Safari, no iOS — data is biased |
| **Requires header** | `Document-Policy: js-profiling` must be served; some hosts don't allow custom headers |
| **Compound sampling** | Profiles only captured when transaction is also sampled |
| **10ms granularity** | Very short functions (<10ms) may not appear in profiles |
| **Chrome DevTools conflict** | Must disable integration when doing local DevTools profiling |
| **Not on CDN** | `browserProfilingIntegration` is not available via the CDN loader bundle |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No profiles appearing in Sentry | Verify `Document-Policy: js-profiling` header is present on document responses |
| Profiles exist but show minified names | Source maps not uploaded — configure `sentryVitePlugin` or `sentryWebpackPlugin` |
| Profiling data only from some users | Expected — only Chromium users are profiled; Firefox/Safari silently no-op |
| Chrome DevTools shows inflated rendering times | Disable `browserProfilingIntegration` during local DevTools sessions |
| `profileSessionSampleRate` has no effect | Ensure `browserProfilingIntegration()` is listed after `browserTracingIntegration()` in the integrations array |
| Profiling on static host not working | Verify your host supports custom response headers; GitHub Pages and some CDNs do not |
| Profiles not linked to spans in Trace mode | Confirm `profileLifecycle: "trace"` is set and `tracesSampleRate` > 0 |

---

## Reference: React Features

# React-Specific Features — Sentry React SDK

> Minimum SDK: `@sentry/react` v8.0.0+

This is the catch-all deep dive for React-specific Sentry features: Redux integration, component tracking, source maps, and the full integrations catalog.

---

## Table of Contents

1. [Redux Integration](#1-redux-integration)
2. [Component Tracking & Performance](#2-component-tracking--performance)
3. [Source Maps](#3-source-maps)
4. [Default Integrations](#4-default-integrations)
5. [Optional Integrations](#5-optional-integrations)
6. [Build Tool Detection & Environment Variables](#6-build-tool-detection--environment-variables)

---

## 1. Redux Integration

`Sentry.createReduxEnhancer()` hooks into your Redux store to automatically:

- Capture **Redux actions as breadcrumbs** on every Sentry error event
- Attach the **Redux state as a `redux_state.json` file** to error events
- Keep **Sentry scope tags in sync** with your Redux state

### Setup — Redux Toolkit (`configureStore`)

```typescript
import * as Sentry from "@sentry/react";
import { configureStore } from "@reduxjs/toolkit";
import rootReducer from "./reducers";

const sentryReduxEnhancer = Sentry.createReduxEnhancer({
  // options — see below
});

const store = configureStore({
  reducer: rootReducer,
  enhancers: (getDefaultEnhancers) => {
    return getDefaultEnhancers().concat(sentryReduxEnhancer);
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;
```

> ⚠️ **Critical:** `sentryReduxEnhancer` is a **store enhancer**, not Redux middleware. Do **NOT** pass it inside `applyMiddleware()`.

### Setup — Legacy `createStore` with Middleware

```javascript
import { createStore, applyMiddleware, compose } from "redux";
import thunk from "redux-thunk";
import * as Sentry from "@sentry/react";

const sentryReduxEnhancer = Sentry.createReduxEnhancer();

const store = createStore(
  rootReducer,
  compose(applyMiddleware(thunk), sentryReduxEnhancer),
);
```

---

### Options: `actionTransformer` — Filter/Scrub Actions Before Breadcrumbs

Called for every dispatched action. Return the action to include it as a breadcrumb, a modified copy to scrub sensitive fields, or `null` to drop it entirely.

```typescript
const sentryReduxEnhancer = Sentry.createReduxEnhancer({
  actionTransformer: (action) => {
    // Drop high-volume or sensitive actions entirely
    if (action.type === "WEBSOCKET_PING") return null;
    if (action.type === "FETCH_SECRETS") return null;

    // Scrub sensitive fields from certain actions
    if (action.type === "USER_LOGIN") {
      return {
        ...action,
        password: "[REDACTED]",
        token: "[REDACTED]",
      };
    }

    if (action.type === "UPDATE_PAYMENT") {
      return {
        ...action,
        payload: {
          ...action.payload,
          cardNumber: null,
          cvv: null,
        },
      };
    }

    // Include all other actions as-is
    return action;
  },
});
```

---

### Options: `stateTransformer` — Filter/Scrub State Snapshots

Called on every state update. Return the state to attach it to error events, a modified copy with sensitive fields redacted, or `null` to exclude state entirely.

```typescript
const sentryReduxEnhancer = Sentry.createReduxEnhancer({
  stateTransformer: (state: RootState) => {
    // Return null to send NO state with errors (reduces context but protects PII)
    // if (state.topSecret.active) return null;

    // Return a scrubbed copy
    return {
      ...state,
      auth: {
        ...state.auth,
        token: null,        // remove auth token
        refreshToken: null,
        password: null,
      },
      user: {
        ...state.user,
        ssn: "[REDACTED]",
        creditCard: null,
        dateOfBirth: null,
      },
      // Remove entire subtrees you don't need
      cache: null,
      rawApiResponses: null,
    };
  },
});
```

> ⚠️ **Warning:** If `stateTransformer` returns `null`, error events will lack Redux state context. Debugging large state-dependent bugs becomes much harder. Prefer returning a filtered copy over returning `null`.

---

### Options: `configureScopeWithState` — Derive Sentry Tags from Redux State

Called after every state update. Use it to keep Sentry scope tags/context in sync with your application's Redux state — these tags then appear on every error captured after the update.

```typescript
const sentryReduxEnhancer = Sentry.createReduxEnhancer({
  configureScopeWithState: (scope: Sentry.Scope, state: RootState) => {
    // Tag events with current user plan (great for filtering errors by customer tier)
    scope.setTag("user.plan", state.user.plan);
    scope.setTag("user.id", state.user.id);

    // Tag with feature flag state
    scope.setTag("feature.newCheckout", String(state.features.newCheckout));
    scope.setTag("feature.darkMode", String(state.settings.darkMode));

    // Tag with routing/navigation state
    scope.setTag("app.currentFlow", state.navigation.currentFlow);

    // Conditional tags based on state shape
    if (state.settings.useImperialUnits) {
      scope.setTag("user.usesImperialUnits", "true");
    }

    // Set structured context (not searchable but visible in issue detail)
    scope.setContext("cart", {
      itemCount: state.cart.items.length,
      total: state.cart.total,
      coupon: state.cart.couponCode ?? null,
    });
  },
});
```

---

### Options: `attachReduxState` — Control State File Attachment

Controls whether the Redux state (post-`stateTransformer`) is attached as a `redux_state.json` file on error events.

- **Type:** `boolean`
- **Default:** `true`
- **Min SDK:** `7.69.0`

```typescript
const sentryReduxEnhancer = Sentry.createReduxEnhancer({
  attachReduxState: false, // Don't attach state file — reduces payload size
});
```

---

### Options: `normalizeDepth` — Control State Serialization Depth

Set in `Sentry.init()`, not in `createReduxEnhancer()`. Increases the depth at which Redux state trees are serialized. The default of `3` is too shallow for most Redux state shapes.

```typescript
Sentry.init({
  dsn: "___PUBLIC_DSN___",
  normalizeDepth: 10, // Default is 3 — increase for deeply nested Redux state
});
```

---

### All Options Summary

| Option | Type | Default | Location | Description |
|--------|------|---------|----------|-------------|
| `actionTransformer` | `(action: Action) => Action \| null` | — | `createReduxEnhancer()` | Modify or drop action breadcrumbs |
| `stateTransformer` | `(state: State) => State \| null` | — | `createReduxEnhancer()` | Modify or drop state attached to events |
| `configureScopeWithState` | `(scope: Scope, state: State) => void` | — | `createReduxEnhancer()` | Sync Sentry scope tags/context with Redux state |
| `attachReduxState` | `boolean` | `true` | `createReduxEnhancer()` | Attach state as `redux_state.json` file on errors |
| `normalizeDepth` | `number` | `3` | `Sentry.init()` | Max depth when serializing nested state |

---

### Complete Working Example with `@reduxjs/toolkit`

```typescript
// store/sentry.ts
import * as Sentry from "@sentry/react";
import type { RootState } from "./types";

export const sentryReduxEnhancer = Sentry.createReduxEnhancer({
  actionTransformer: (action) => {
    // Drop noisy/sensitive action types
    const DROP_TYPES = new Set([
      "SET_AUTH_TOKEN",
      "REFRESH_TOKEN",
      "WEBSOCKET_HEARTBEAT",
      "UPDATE_CURSOR_POSITION",
    ]);
    if (DROP_TYPES.has(action.type)) return null;

    // Scrub passwords from login actions
    if (action.type === "auth/login/pending") {
      return { ...action, meta: { ...action.meta, arg: { email: action.meta?.arg?.email, password: "[REDACTED]" } } };
    }

    return action;
  },

  stateTransformer: (state: RootState) => ({
    ...state,
    auth: { isAuthenticated: state.auth.isAuthenticated, userId: state.auth.userId },
    // Strip large or sensitive subtrees
    rawData: null,
  }),

  configureScopeWithState: (scope, state: RootState) => {
    scope.setTag("user.plan", state.user.plan ?? "unknown");
    scope.setTag("user.id", state.auth.userId ?? "anonymous");
    scope.setTag("org.id", state.org.id ?? "none");
  },
});

// store/index.ts
import { configureStore } from "@reduxjs/toolkit";
import { sentryReduxEnhancer } from "./sentry";
import rootReducer from "./reducers";

export const store = configureStore({
  reducer: rootReducer,
  enhancers: (getDefaultEnhancers) =>
    getDefaultEnhancers().concat(sentryReduxEnhancer),
});
```

```typescript
// instrument.ts — init with normalizeDepth
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  normalizeDepth: 10, // Required for deeply nested Redux state
  integrations: [Sentry.browserTracingIntegration()],
  tracesSampleRate: 1.0,
});
```

### Performance Considerations

Redux state can be very large. Keep in mind:

1. **State size:** Large state trees (thousands of items) will slow serialization and increase payload size. Use `stateTransformer` to return only the relevant slices.
2. **`normalizeDepth`:** Keep it as low as practical. `10` is usually sufficient for deeply nested state; avoid setting it to `Infinity`.
3. **`attachReduxState: false`:** For high-traffic production apps where payload size is a concern, disabling state attachment reduces each error event's size.
4. **`configureScopeWithState` cost:** This runs on every Redux dispatch. Keep the function fast — avoid heavy computations or deep object traversals.

---

## 2. Component Tracking & Performance

### A. React Component Name Annotation (Build-Time)

Replaces opaque CSS selectors in breadcrumbs, Session Replay, and performance spans with readable React component names.

**Before:** `button.en302zp1.app-191aavw.e16hd6vm2[role="button"]`  
**After:** `CheckoutButton`

**Requirements:**
- SDK v7.91.0+
- Components must be in `.jsx` or `.tsx` files (`.js` and `.ts` are **not** annotated)
- esbuild is **not** supported

The bundler plugins inject `data-sentry-component` and `data-sentry-source-file` attributes at build time:

```html
<!-- Resulting DOM -->
<button
  data-sentry-component="CheckoutButton"
  data-sentry-source-file="CheckoutButton.tsx"
>
  Checkout
</button>
```

**Enable via Vite (recommended):**

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { sentryVitePlugin } from "@sentry/vite-plugin";

export default defineConfig({
  plugins: [
    react(),
    sentryVitePlugin({
      org: process.env.SENTRY_ORG,
      project: process.env.SENTRY_PROJECT,
      authToken: process.env.SENTRY_AUTH_TOKEN,
      reactComponentAnnotation: {
        enabled: true,
        // Exclude components that cause "Passing unknown props on Fragment" errors
        ignoredComponents: ["AnimationWrapper", "LayoutFragment"],
      },
    }),
  ],
  build: {
    sourcemap: "hidden",
  },
});
```

**Enable via Babel plugin directly (without bundler plugin):**

```bash
npm install @sentry/babel-plugin-component-annotate --save-dev
```

```javascript
// babel.config.js
module.exports = {
  plugins: ["@sentry/babel-plugin-component-annotate"],
};
```

**Bundler support:**

| Bundler | Component Annotation |
|---------|---------------------|
| Vite | ✅ Supported |
| Webpack | ✅ Supported |
| Rollup | ✅ Supported |
| esbuild | ❌ Not supported |

**What you gain:**

| Where | Before | After |
|-------|--------|-------|
| Breadcrumbs | `div.sc-abc123` | `ProductCard` |
| Session Replay | Unreadable selector | Search by `ProductCard` |
| Performance spans | Generic element | `CheckoutButton` render |

---

### B. `Sentry.withProfiler()` — React Profiler HOC

`withProfiler` wraps a component with the [React Profiler API](https://react.dev/reference/react/Profiler) to capture render timing as Sentry performance spans.

```typescript
import * as Sentry from "@sentry/react";

// Basic — display name inferred from component.displayName or .name
const ProfiledDashboard = Sentry.withProfiler(Dashboard);

// With explicit name (required for anonymous or arrow-function components)
const ProfiledWidget = Sentry.withProfiler(
  ({ data }) => <div>{data.title}</div>,
  { name: "DataWidget" }
);

// Class component decorator syntax
@Sentry.withProfiler
class ExpensiveList extends React.Component {
  render() {
    return <ul>{this.props.items.map(renderItem)}</ul>;
  }
}
```

**Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `name` | `string` | Component `displayName` or `name` | Display name shown in Sentry traces |
| `includeRender` | `boolean` | `true` | Track initial render phase |
| `includeUpdates` | `boolean` | `true` | Track re-render / update phases |

**What it captures:**
- Mount time (initial render duration)
- Update/re-render time per update
- Number of re-renders
- Component name in the Sentry performance trace waterfall

**Data appears in:** Sentry → Performance → Trace View, as child spans of the current transaction.

> **Requires tracing:** `browserTracingIntegration` must be in your `Sentry.init` integrations.

**When to use (and when not to):**

✅ Use on:
- Root-level route components (Dashboard, CheckoutFlow, UserProfile)
- Components with expensive render logic (large lists, complex calculations)
- Components that re-render frequently and may cause jank

❌ Do **not** use on:
- Every component in the tree — the overhead compounds
- Simple presentational/leaf components
- Components that render hundreds of times per second (e.g., animation frames)

**Performance overhead:** Each profiled component adds a small constant overhead per render cycle. Profile the 5–10 most performance-critical components, not the entire tree.

---

## 3. Source Maps

Source maps translate minified production stack traces back to your original source code. Without them, stack traces show obfuscated variable names and collapsed line numbers.

### Recommended: Sentry Wizard

The fastest path — automatically detects your bundler, installs the plugin, and configures auth:

```bash
npx @sentry/wizard@latest -i sourcemaps
```

The wizard:
1. Detects Vite, webpack, or CRA
2. Installs the appropriate Sentry bundler plugin
3. Adds `SENTRY_AUTH_TOKEN` to your `.env.sentry-build-plugin`
4. Configures `sourcemap: "hidden"` and `filesToDeleteAfterUpload`

---

### How Debug IDs Work

Modern Sentry source map matching uses **Debug IDs** — unique identifiers injected by the bundler plugin into both the compiled `.js` bundle and the corresponding `.js.map` file. This makes source map matching reliable without needing to manage file names or release artifacts manually.

**Flow:**
1. Production build runs → bundler plugin injects a Debug ID into each `.js` and `.js.map` file
2. Plugin uploads `.js.map` files to Sentry with their Debug IDs
3. Error occurs in production → stack frame contains the Debug ID
4. Sentry uses the Debug ID to locate the exact source map → deobfuscates the trace

Debug IDs are more reliable than release-based matching (older approach) because they don't depend on consistent release naming or artifact upload timing.

---

### Vite Plugin

**Minimum SDK:** `@sentry/vite-plugin` `2.0.0` / `@sentry/react` `7.47.0`

```bash
npm install @sentry/vite-plugin --save-dev
```

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { sentryVitePlugin } from "@sentry/vite-plugin";

export default defineConfig({
  build: {
    // "hidden" generates source maps but strips the `//# sourceMappingURL=` comment
    // from bundles, so browsers won't load them — they're only for Sentry.
    sourcemap: "hidden",
  },
  plugins: [
    react(),
    // sentryVitePlugin MUST come after all other plugins
    sentryVitePlugin({
      org: process.env.SENTRY_ORG,
      project: process.env.SENTRY_PROJECT,
      authToken: process.env.SENTRY_AUTH_TOKEN,

      // Enable React component name annotation at the same time
      reactComponentAnnotation: {
        enabled: true,
      },

      sourcemaps: {
        // Delete .map files from dist/ after uploading to Sentry
        // so they're not deployed to your CDN/server
        filesToDeleteAfterUpload: [
          "./**/*.map",
          ".*/**/public/**/*.map",
          "./dist/**/client/**/*.map",
        ],
      },
    }),
  ],
});
```

> ⚠️ Place `sentryVitePlugin` **after** all other plugins (especially `@vitejs/plugin-react`) to ensure correct source map generation.

---

### Webpack Plugin

**Minimum SDK:** `@sentry/webpack-plugin` `2.0.0` / `@sentry/react` `7.47.0`

```bash
npm install @sentry/webpack-plugin --save-dev
```

```javascript
// webpack.config.js
const { sentryWebpackPlugin } = require("@sentry/webpack-plugin");

module.exports = {
  // "hidden-source-map" generates source maps without the `//# sourceMappingURL=`
  // reference comment, so they won't be served publicly.
  devtool: "hidden-source-map",

  plugins: [
    sentryWebpackPlugin({
      org: process.env.SENTRY_ORG,
      project: process.env.SENTRY_PROJECT,
      authToken: process.env.SENTRY_AUTH_TOKEN,
      sourcemaps: {
        filesToDeleteAfterUpload: [
          "./**/*.map",
          "./build/static/**/*.map",
        ],
      },
    }),
  ],
};
```

---

### Create React App

CRA has limited configuration access. Two approaches:

**Option A: CRACO (recommended — no ejection)**

```bash
npm install @craco/craco @sentry/webpack-plugin --save-dev
```

```javascript
// craco.config.js
const { sentryWebpackPlugin } = require("@sentry/webpack-plugin");

module.exports = {
  webpack: {
    configure: (webpackConfig) => {
      webpackConfig.devtool = "hidden-source-map";
      webpackConfig.plugins.push(
        sentryWebpackPlugin({
          org: process.env.SENTRY_ORG,
          project: process.env.SENTRY_PROJECT,
          authToken: process.env.SENTRY_AUTH_TOKEN,
          sourcemaps: {
            filesToDeleteAfterUpload: ["./build/static/**/*.map"],
          },
        })
      );
      return webpackConfig;
    },
  },
};
```

Update `package.json` scripts:
```json
{
  "scripts": {
    "start": "craco start",
    "build": "craco build"
  }
}
```

**Option B: Eject (`npm run eject`)**

After ejecting, edit `config/webpack.config.js` directly — same as the regular webpack setup above. Ejection is irreversible; prefer CRACO.

---

### Manual Upload with `sentry-cli`

Use when you can't use a bundler plugin (e.g., legacy toolchain, pre-built artifacts):

```bash
npm install @sentry/cli --save-dev
```

```bash
# Upload source maps after a production build
npx sentry-cli sourcemaps upload \
  --org $SENTRY_ORG \
  --project $SENTRY_PROJECT \
  --auth-token $SENTRY_AUTH_TOKEN \
  ./build
```

**`.sentryclirc` configuration file (alternative to env vars):**

```ini
[defaults]
org = my-org-slug
project = my-project-slug
url = https://sentry.io/
```

```bash
# With .sentryclirc, no --org/--project flags needed:
npx sentry-cli sourcemaps upload --auth-token $SENTRY_AUTH_TOKEN ./build
```

> ⚠️ Never commit `SENTRY_AUTH_TOKEN` to source control. Always read it from environment variables.

**CI/CD pattern (GitHub Actions):**

```yaml
- name: Build
  run: npm run build

- name: Upload source maps to Sentry
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
    SENTRY_ORG: my-org-slug
    SENTRY_PROJECT: my-react-app
  run: |
    npx sentry-cli sourcemaps upload \
      --org $SENTRY_ORG \
      --project $SENTRY_PROJECT \
      --auth-token $SENTRY_AUTH_TOKEN \
      ./build

- name: Delete source maps from build artifacts
  run: find ./build -name "*.map" -delete

- name: Deploy
  run: # your deploy step
```

---

### Environment Variables for Source Maps

Store credentials in `.env.sentry-build-plugin` (auto-loaded by Sentry bundler plugins) or pass as CI/CD secrets:

```bash
# .env.sentry-build-plugin  ← auto-loaded by @sentry/vite-plugin and @sentry/webpack-plugin
# ADD THIS FILE TO .gitignore — never commit it
SENTRY_AUTH_TOKEN=sntrys_eyJ...
SENTRY_ORG=my-org-slug
SENTRY_PROJECT=my-project-slug
```

**Required token permissions:**

The `SENTRY_AUTH_TOKEN` must have:
- **Project:** Read & Write
- **Release:** Admin

---

### Source Map Security

| Strategy | How |
|----------|-----|
| Don't expose maps to browsers | Use `sourcemap: "hidden"` (Vite) or `devtool: "hidden-source-map"` (webpack) |
| Delete maps after upload | Use `filesToDeleteAfterUpload` in the plugin config |
| Block map access at CDN/server | Configure your server to return 403 for `.js.map` requests |

All three should be used together for maximum security.

---

### Troubleshooting Source Maps

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Stack traces still minified | Source maps not uploaded, or Debug IDs missing | Rebuild with production config, re-run wizard or plugin |
| Maps not applied to old errors | Maps uploaded after errors occurred | Always upload maps **before** deploying — ideally in the same CI step |
| "SourceMapDevToolPlugin" stripping sources | `noSources: true` in your webpack SourceMapDevToolPlugin | Remove `noSources: true` option |
| Plugin only uploads once | Running in `--watch` or dev mode | Plugin only uploads during production builds (`NODE_ENV=production`) |
| SENTRY_AUTH_TOKEN not found | Missing env variable | Check `.env.sentry-build-plugin` exists and is not gitignored incorrectly |
| Component names still not showing | `.js`/`.ts` files instead of `.jsx`/`.tsx` | Rename files or use the Babel plugin directly on all JSX transform targets |

---

## 4. Default Integrations

These integrations are **automatically enabled** for every `@sentry/react` installation. No configuration required.

| Integration | Name Constant | What It Does |
|-------------|--------------|--------------|
| Breadcrumbs | `breadcrumbsIntegration` | Captures breadcrumbs from DOM events (clicks, inputs), XHR, fetch, console calls, history navigation |
| Browser API Errors | `browserApiErrorsIntegration` | Wraps `setTimeout`, `setInterval`, `requestAnimationFrame`, `addEventListener`, `removeEventListener` in try/catch so errors inside them are captured |
| Browser Session | `browserSessionIntegration` | Tracks session health (healthy vs. crashed) for Release Health metrics |
| Dedupe | `dedupeIntegration` | Prevents duplicate error events from being sent — deduplicates based on error type, message, and stack trace |
| Function to String | `functionToStringIntegration` | Preserves original function `.toString()` output after SDK instrumentation, so stack traces show readable names |
| Global Handlers | `globalHandlersIntegration` | Listens to `window.onerror` (uncaught exceptions) and `window.onunhandledrejection` (unhandled promise rejections) |
| HTTP Context | `httpContextIntegration` | Attaches current URL, referrer, and user-agent to every event |
| Inbound Filters | `inboundFiltersIntegration` | Filters known-noisy events by error type, message, or URL (e.g., browser extension errors, localhost-only errors) |
| Linked Errors | `linkedErrorsIntegration` | Follows JavaScript `error.cause` chains and attaches nested errors as linked issues — also used for React component stack linkage |

### Customizing a Default Integration's Options

Pass the integration explicitly in `integrations` — it overrides the default instance:

```typescript
Sentry.init({
  dsn: "___PUBLIC_DSN___",
  integrations: [
    // Override breadcrumbs to disable console capturing but keep DOM/fetch/XHR
    Sentry.breadcrumbsIntegration({
      console: false,   // don't capture console.log as breadcrumbs
      dom: true,
      fetch: true,
      history: true,
      xhr: true,
    }),

    // Only capture unhandled exceptions; handle rejections manually
    Sentry.globalHandlersIntegration({
      onerror: true,
      onunhandledrejection: false,
    }),
  ],
});
```

### Removing a Default Integration

Use the function form of `integrations` to filter out what you don't want:

```typescript
Sentry.init({
  dsn: "___PUBLIC_DSN___",
  integrations: (integrations) => {
    // Remove deduplication (e.g., if you want every occurrence recorded separately)
    return integrations.filter(
      (integration) => integration.name !== "Dedupe"
    );
  },
});
```

Common integration names to filter:
- `"Dedupe"` — deduplication
- `"Breadcrumbs"` — all automatic breadcrumbs
- `"GlobalHandlers"` — window.onerror / unhandledrejection
- `"LinkedErrors"` — error cause chain following
- `"HttpContext"` — URL/referrer attachment
- `"InboundFilters"` — built-in noise filtering

### Disabling ALL Default Integrations

```typescript
Sentry.init({
  dsn: "___PUBLIC_DSN___",
  defaultIntegrations: false,
  // Build your own set from scratch:
  integrations: [
    Sentry.globalHandlersIntegration(),
    Sentry.browserTracingIntegration(),
    Sentry.dedupeIntegration(),
  ],
});
```

---

## 5. Optional Integrations

These are available but **must be explicitly added** to your `integrations` array.

### Performance & Tracing

| Integration | Min SDK | Description |
|-------------|---------|-------------|
| `browserTracingIntegration()` | 8.0.0 | Page load tracing, navigation tracing, automatic span creation for fetch/XHR, Core Web Vitals (LCP, FID, CLS), distributed tracing headers |
| `browserProfilingIntegration()` | 10.27.0 (Beta) | JS Self-Profiling API — captures call stacks at 100Hz in Chromium browsers. **Requires** `Document-Policy: js-profiling` HTTP header |

### Session Replay

| Integration | Min SDK | Description |
|-------------|---------|-------------|
| `replayIntegration()` | 7.27.0 | Session Replay — records DOM mutations, network requests, console output. Configured with `replaysSessionSampleRate` and `replaysOnErrorSampleRate` |
| `replayCanvasIntegration()` | 7.98.0 | Extends `replayIntegration` to record `<canvas>` elements in replays |

### Logging

| Integration | Min SDK | Description |
|-------------|---------|-------------|
| `consoleLoggingIntegration()` | 9.41.0 | Automatically forwards `console.log/warn/error/info/debug` calls as structured Sentry logs. Requires `enableLogs: true` |

```typescript
Sentry.init({
  enableLogs: true,
  integrations: [
    Sentry.consoleLoggingIntegration({
      levels: ["warn", "error"], // Only capture warnings and errors
    }),
  ],
});
```

### User Feedback

| Integration | Min SDK | Description |
|-------------|---------|-------------|
| `feedbackIntegration()` | 7.85.0 | Floating feedback button + form (bottom-right). Supports screenshots, custom theming, programmatic control |
| `feedbackModalIntegration()` | 7.85.0 | Modal dialog variant of the feedback form |
| `feedbackScreenshotIntegration()` | 8.0.0 | Adds screenshot capture capability to the feedback widget |

### Error Enhancement

| Integration | Min SDK | Description |
|-------------|---------|-------------|
| `extraErrorDataIntegration()` | 5.16.0 | Attaches non-standard properties on `Error` objects (e.g., `error.code`, `error.statusCode`, custom fields) as extra context |
| `contextLinesIntegration()` | 7.47.0 | Shows source code lines above and below the erroring line in the stack trace (requires source maps) |
| `httpClientIntegration()` | 7.50.0 | Captures failed HTTP requests (4xx/5xx responses) as Sentry error events, with request/response bodies. Opt-in because it may capture PII |
| `reportingObserverIntegration()` | 5.9.0 | Captures [Reporting Observer API](https://developer.mozilla.org/en-US/docs/Web/API/ReportingObserver) events (deprecation warnings, browser interventions, CSP violations) |
| `captureConsoleIntegration()` | 3.3.0 | Captures `console.error`/`console.warn` calls as Sentry issues (not logs). Legacy alternative to `consoleLoggingIntegration` |

### Stack Frame Rewriting

| Integration | Min SDK | Description |
|-------------|---------|-------------|
| `rewriteFramesIntegration()` | 5.7.0 | Rewrites stack frame file paths — useful for normalizing paths in monorepos, Docker containers, or when paths differ between build and deploy environments |

---

### `httpClientIntegration` — Full Setup

Captures HTTP requests that fail (4xx/5xx) as error events, with the request URL, method, status code, and optionally request/response bodies.

```typescript
Sentry.init({
  dsn: "___PUBLIC_DSN___",
  integrations: [
    Sentry.httpClientIntegration({
      // Capture errors for these HTTP status code ranges
      failedRequestStatusCodes: [[400, 499], [500, 599]],

      // Only capture errors for these URL patterns
      failedRequestTargets: [
        "https://api.myapp.com",
        /^https:\/\/internal\.service\//,
      ],
    }),
  ],
  // Required to capture request/response bodies (PII risk — use cautiously)
  sendDefaultPii: true,
});
```

### Adding Integrations After Init

If you need to add an integration after `Sentry.init()` has been called (e.g., after user consent):

```typescript
// After the user accepts analytics cookies:
Sentry.addIntegration(Sentry.replayIntegration({
  maskAllText: true,
  blockAllMedia: true,
}));
```

### Lazy Loading Integrations (Code Splitting)

```typescript
// Dynamic import (works with any bundler)
import("@sentry/browser").then((lazySentry) => {
  Sentry.addIntegration(lazySentry.replayIntegration());
});

// CDN lazyLoadIntegration() — for Sentry loader script environments
async function enableFeedback() {
  try {
    const feedbackIntegration =
      await Sentry.lazyLoadIntegration("feedbackIntegration");
    Sentry.addIntegration(feedbackIntegration({ colorScheme: "system" }));
  } catch (e) {
    // Ad-blockers or network failures — fail gracefully
    console.warn("Could not load Sentry feedback integration", e);
  }
}
```

Lazy-loadable integrations: `replayIntegration`, `replayCanvasIntegration`, `feedbackIntegration`, `feedbackModalIntegration`, `feedbackScreenshotIntegration`, `captureConsoleIntegration`, `contextLinesIntegration`, `linkedErrorsIntegration`, `dedupeIntegration`, `extraErrorDataIntegration`, `httpClientIntegration`, `reportingObserverIntegration`, `rewriteFramesIntegration`, `browserProfilingIntegration`

---

## 6. Build Tool Detection & Environment Variables

### Detecting the Build Tool

```bash
# Run from project root
ls vite.config.ts vite.config.js webpack.config.js webpack.config.ts \
   craco.config.js next.config.js next.config.ts 2>/dev/null

cat package.json | grep -E '"vite"|"react-scripts"|"webpack"|"@craco"'
```

| File/Package Found | Build Tool |
|-------------------|------------|
| `vite.config.*` or `"vite"` in deps | Vite |
| `"react-scripts"` in deps | Create React App |
| `craco.config.js` or `"@craco/craco"` | CRA + CRACO |
| `webpack.config.*` or `"webpack"` in deps | Custom Webpack |
| `next.config.*` or `"next"` in deps | Next.js (use `@sentry/nextjs` instead) |

---

### DSN Environment Variable Patterns

| Build Tool | Variable Name | How to Access in Code |
|------------|--------------|----------------------|
| Vite | `VITE_SENTRY_DSN` | `import.meta.env.VITE_SENTRY_DSN` |
| Create React App | `REACT_APP_SENTRY_DSN` | `process.env.REACT_APP_SENTRY_DSN` |
| Custom Webpack | `SENTRY_DSN` | `process.env.SENTRY_DSN` (requires `DefinePlugin`) |
| Any | `SENTRY_DSN` | Build-time injection (not available at runtime in browser) |

**Vite — `.env` file:**
```bash
# .env.production
VITE_SENTRY_DSN=https://<key>@<org>.ingest.sentry.io/<id>
VITE_SENTRY_ENVIRONMENT=production
```

```typescript
// instrument.ts
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.VITE_SENTRY_ENVIRONMENT ?? "development",
});
```

**Create React App — `.env.production` file:**
```bash
# .env.production  (committed — DSN is public)
REACT_APP_SENTRY_DSN=https://<key>@<org>.ingest.sentry.io/<id>
REACT_APP_SENTRY_ENVIRONMENT=production
```

```typescript
// instrument.ts
Sentry.init({
  dsn: process.env.REACT_APP_SENTRY_DSN,
  environment: process.env.REACT_APP_SENTRY_ENVIRONMENT ?? "development",
});
```

**Custom Webpack — `webpack.config.js` with `DefinePlugin`:**
```javascript
const webpack = require("webpack");

module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      "process.env.SENTRY_DSN": JSON.stringify(process.env.SENTRY_DSN),
      "process.env.SENTRY_ENVIRONMENT": JSON.stringify(
        process.env.NODE_ENV ?? "development"
      ),
    }),
  ],
};
```

```typescript
// instrument.ts
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.SENTRY_ENVIRONMENT,
});
```

---

### Conditional Initialization (Development vs Production)

Prevent Sentry from running in local development to avoid polluting your issue inbox with dev noise:

```typescript
// instrument.ts
import * as Sentry from "@sentry/react";

const IS_PRODUCTION =
  import.meta.env.PROD ||                           // Vite
  process.env.NODE_ENV === "production";             // webpack / CRA

if (IS_PRODUCTION) {
  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN,           // or your env var pattern
    environment: "production",
    integrations: [
      Sentry.browserTracingIntegration(),
      Sentry.replayIntegration({
        maskAllText: false,
        blockAllMedia: false,
      }),
    ],
    tracesSampleRate: 0.2,              // 20% in production
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
  });
} else {
  // In development: optionally init with verbose debug and full sampling
  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN,
    environment: "development",
    debug: true,                        // Verbose SDK logging
    tracesSampleRate: 1.0,              // 100% in dev so nothing is missed
    integrations: [Sentry.browserTracingIntegration()],
    // No Replay in dev — too noisy
  });
}
```

---

### Complete `instrument.ts` Reference — All Features

A kitchen-sink example combining every feature:

```typescript
// src/instrument.ts
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.VITE_APP_ENV ?? "production",
  release: import.meta.env.VITE_APP_VERSION,

  // ── Integrations ─────────────────────────────────────────────
  integrations: [
    // Tracing (navigation + API + Core Web Vitals)
    Sentry.browserTracingIntegration(),

    // Session Replay
    Sentry.replayIntegration({
      maskAllText: false,
      blockAllMedia: false,
    }),

    // Profiling (Beta — Chromium only, needs Document-Policy header)
    // Sentry.browserProfilingIntegration(),

    // Structured logging (requires enableLogs: true)
    Sentry.consoleLoggingIntegration({
      levels: ["warn", "error"],
    }),

    // Capture HTTP 4xx/5xx as Sentry errors
    Sentry.httpClientIntegration({
      failedRequestStatusCodes: [[400, 499], [500, 599]],
    }),

    // Show source lines in stack traces (requires source maps)
    Sentry.contextLinesIntegration(),

    // Capture non-standard Error properties
    Sentry.extraErrorDataIntegration(),

    // User feedback widget
    Sentry.feedbackIntegration({
      colorScheme: "system",
      showBranding: false,
      triggerLabel: "Report a Bug",
    }),
  ],

  // ── Tracing ───────────────────────────────────────────────────
  tracesSampleRate: 0.2,
  tracePropagationTargets: [
    "localhost",
    /^https:\/\/api\.myapp\.com/,
  ],

  // ── Session Replay ────────────────────────────────────────────
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,

  // ── Profiling ─────────────────────────────────────────────────
  profileSessionSampleRate: 1.0,

  // ── Logging ───────────────────────────────────────────────────
  enableLogs: true,
  beforeSendLog: (log) => {
    if (log.level === "debug") return null; // Drop debug logs
    if (log.attributes?.password) delete log.attributes.password;
    return log;
  },

  // ── Redux ─────────────────────────────────────────────────────
  normalizeDepth: 10,

  // ── Filtering ─────────────────────────────────────────────────
  ignoreErrors: [
    "ResizeObserver loop limit exceeded",
    /^Loading chunk \d+ failed/,
  ],
  denyUrls: [
    /extensions\//i,
    /^chrome:\/\//i,
  ],

  beforeSend(event) {
    // Strip credit card numbers from messages just in case
    if (event.message) {
      event.message = event.message.replace(/\b\d{16}\b/g, "[CARD]");
    }
    return event;
  },
});
```

```typescript
// store/index.ts — wire in Redux enhancer
import { configureStore } from "@reduxjs/toolkit";
import * as Sentry from "@sentry/react";

export const store = configureStore({
  reducer: rootReducer,
  enhancers: (getDefaultEnhancers) =>
    getDefaultEnhancers().concat(
      Sentry.createReduxEnhancer({
        stateTransformer: (state) => ({ ...state, auth: null }),
        configureScopeWithState: (scope, state) => {
          scope.setTag("user.plan", state.user.plan);
        },
      })
    ),
});
```

---

## Quick Reference

```typescript
// ── Redux ─────────────────────────────────────────────────────
Sentry.createReduxEnhancer({
  actionTransformer: (action) => action | null,
  stateTransformer: (state) => state | null,
  configureScopeWithState: (scope, state) => void,
  attachReduxState: true,
})
// normalizeDepth goes in Sentry.init(), not createReduxEnhancer()

// ── Component Tracking ────────────────────────────────────────
Sentry.withProfiler(Component, { name?, includeRender?, includeUpdates? })
sentryVitePlugin({ reactComponentAnnotation: { enabled: true, ignoredComponents: [] } })
// Babel plugin direct: @sentry/babel-plugin-component-annotate

// ── Source Maps ───────────────────────────────────────────────
npx @sentry/wizard@latest -i sourcemaps  // automated setup
// Vite: build.sourcemap = "hidden" + sentryVitePlugin()
// Webpack: devtool: "hidden-source-map" + sentryWebpackPlugin()
// CRA: use CRACO + sentryWebpackPlugin
// Manual: npx sentry-cli sourcemaps upload --auth-token $TOKEN ./dist

// ── Integrations (opt-in) ─────────────────────────────────────
Sentry.browserTracingIntegration()         // Tracing + Core Web Vitals
Sentry.replayIntegration()                 // Session Replay
Sentry.browserProfilingIntegration()       // JS Profiler (Beta, Chromium only)
Sentry.consoleLoggingIntegration()         // console → Sentry logs
Sentry.feedbackIntegration()               // Feedback widget
Sentry.httpClientIntegration()             // 4xx/5xx as errors
Sentry.contextLinesIntegration()           // Source lines in stack traces
Sentry.extraErrorDataIntegration()         // Non-standard Error properties
Sentry.reportingObserverIntegration()      // Browser deprecation/CSP reports
Sentry.rewriteFramesIntegration()          // Rewrite stack frame paths
Sentry.captureConsoleIntegration()         // console → Sentry issues (legacy)

// ── Remove a Default Integration ─────────────────────────────
Sentry.init({
  integrations: (integrations) =>
    integrations.filter((i) => i.name !== "Dedupe"),
})

// ── Add Integration After Init ────────────────────────────────
Sentry.addIntegration(Sentry.replayIntegration())

// ── Environment Variables ─────────────────────────────────────
// Vite:   import.meta.env.VITE_SENTRY_DSN
// CRA:    process.env.REACT_APP_SENTRY_DSN
// Webpack: process.env.SENTRY_DSN (via DefinePlugin)
```

---

## Reference: Session Replay

# Session Replay — Sentry React SDK

> Minimum SDK: `@sentry/react` ≥7.27.0+  
> `replayCanvasIntegration()`: requires `@sentry/react` ≥7.98.0+

> ⚠️ **Browser-only feature.** Never add `replayIntegration()` to SSR entry points, Node.js server code, or web workers. Only add it where browser APIs are available.

---

## Setup

Session Replay is bundled in `@sentry/react` — no separate package needed.

```typescript
// src/instrument.ts
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,

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

### When NOT to Add Replay

| Context | Reason |
|---------|--------|
| Node.js / Express / Next.js server | No DOM — DOM recording APIs don't exist |
| Web Workers / Service Workers | No DOM access |
| Next.js `_document.tsx` or `instrumentation.ts` (server) | Server-side code — use client-only init |
| Electron main process | Only the renderer process is appropriate |
| Browser extensions | Not a supported use case |
| CI/build pipelines | No user sessions to record |

For **Next.js App Router**, add replay only in `instrumentation-client.ts` or `sentry.client.config.ts` — never in server instrumentation.

---

## Sample Rates

`replaysSessionSampleRate` and `replaysOnErrorSampleRate` are set on `Sentry.init()`, not on the integration itself.

| Option | Type | Default | Behavior |
|--------|------|---------|----------|
| `replaysSessionSampleRate` | `number` (0–1) | `0` | Fraction of all sessions recorded continuously from start |
| `replaysOnErrorSampleRate` | `number` (0–1) | `0` | Fraction of sessions captured when an error occurs — flushes ~60s of buffer, then continues recording |

### How Session and Error Sampling Interact

```
Session starts
      │
      ▼
replaysSessionSampleRate > 0?
      │
      ├─ YES → Roll dice against replaysSessionSampleRate
      │           ├─ WIN  → Record continuously (session mode) — streamed in real-time chunks
      │           └─ LOSE → Buffer last 60s in memory
      │
      └─ NO  → Always buffer last 60s in memory
                    │
                    ▼
             Error occurs?
                    │
                    ├─ YES → Roll dice against replaysOnErrorSampleRate
                    │           ├─ WIN  → Upload 60s buffer + continue recording
                    │           └─ LOSE → Discard buffer, nothing sent
                    │
                    └─ NO  → Buffer discarded at session end
```

### Recommended Strategies

| Strategy | `replaysSessionSampleRate` | `replaysOnErrorSampleRate` | Use when |
|----------|--------------------------|--------------------------|----------|
| **Errors-only** | `0` | `1.0` | Privacy-first; capture only on problems |
| **Balanced** | `0.1` | `1.0` | Most production apps |
| **Full** | `1.0` | `1.0` | Development or low-traffic apps |
| **High-traffic** | `0.01` | `1.0` | 100k+ sessions/day |

**Errors-only** (`replaysSessionSampleRate: 0`, `replaysOnErrorSampleRate: 1.0`) is the most common production choice: near-zero overhead during normal operation, full context when something breaks.

```typescript
// Errors-only setup:
Sentry.init({
  dsn: "...",
  replaysSessionSampleRate: 0,
  replaysOnErrorSampleRate: 1.0,
  integrations: [Sentry.replayIntegration()],
});
```

---

## `replayIntegration()` — All Constructor Options

```typescript
Sentry.replayIntegration({
  // ── SESSION MANAGEMENT ─────────────────────────────────────────
  stickySession: true,              // persist session across page refreshes
  minReplayDuration: 5000,          // min ms before sending (max: 15000)
  maxReplayDuration: 3600000,       // max replay length (1 hour hard cap)

  // ── PRIVACY / MASKING ──────────────────────────────────────────
  maskAllText: true,                // replace all text with ***
  maskAllInputs: true,              // replace all input values with ***
  blockAllMedia: true,              // replace media elements with placeholder
  mask: ['.sentry-mask', '[data-sentry-mask]'],
  unmask: [],
  block: ['.sentry-block', '[data-sentry-block]'],
  unblock: [],
  ignore: ['.sentry-ignore', '[data-sentry-ignore]'],
  maskFn: (text) => '*'.repeat(text.length),

  // ── NETWORK CAPTURE ────────────────────────────────────────────
  networkDetailAllowUrls: [],       // (string|RegExp)[] — enable body/header capture
  networkDetailDenyUrls: [],        // (string|RegExp)[] — override allowlist
  networkCaptureBodies: true,       // capture req/res bodies for allowed URLs
  networkRequestHeaders: [],        // extra request headers to capture
  networkResponseHeaders: [],       // extra response headers to capture

  // ── PERFORMANCE / DOM PROTECTION ──────────────────────────────
  mutationLimit: 10000,             // stop recording after N mutations
  mutationBreadcrumbLimit: 750,     // emit warning breadcrumb after N mutations
  slowClickIgnoreSelectors: [],     // suppress dead/rage click detection here

  // ── ADVANCED ───────────────────────────────────────────────────
  beforeAddRecordingEvent: (event) => event,  // filter/modify events
  beforeErrorSampling: (event) => true,       // control which errors trigger replay
  useCompression: true,             // compress data in Web Worker
  workerUrl: undefined,             // self-host worker for strict CSP
})
```

### Session Management Options

| Option | Type | Default | Notes |
|--------|------|---------|-------|
| `stickySession` | `boolean` | `true` | Uses `sessionStorage` to survive page refreshes within the same tab. Tab close ends the session. |
| `minReplayDuration` | `number` ms | `5000` | Discard replays shorter than this. Max allowed: 15000ms. Prevents "bounce" uploads. |
| `maxReplayDuration` | `number` ms | `3600000` | After this, session ends and a new one begins (re-sampled). Server enforces 1-hour ceiling. |

---

## Privacy & Masking

This is the most critical part of session replay. Misconfiguration can expose PII.

### Default Behavior (Out of the Box)

With zero configuration, Replay ships in **maximum privacy mode**:

| Data type | Default behavior |
|-----------|-----------------|
| All text content | ✅ Masked — replaced with `*` characters (length-preserving) |
| All `<input>` values | ✅ Masked |
| `<img>`, `<video>`, `<audio>`, `<svg>`, `<picture>`, `<embed>`, `<map>`, `<object>` | ✅ Blocked — replaced with same-size placeholder rectangle |
| Network request/response bodies | ❌ Not captured — opt-in required |
| Network headers beyond Content-Type/Length/Accept | ❌ Not captured — opt-in required |

### The Three Privacy Primitives

| Primitive | Effect | Visual result in replay |
|-----------|--------|------------------------|
| **Mask** | Replaces text content character-by-character with `*` | Element shape preserved; text unreadable |
| **Block** | Replaces entire element with opaque placeholder box | Solid grey/black rectangle same size as element |
| **Ignore** | Suppresses interaction events (clicks, keystrokes) on the element | Element visible; no input captured |

**Mask vs Block distinction:** Masked elements show their layout (you see the form structure, field labels, button positions) but no readable text. Blocked elements are completely opaque — you can't see anything inside. Use mask for forms where structure matters; use block for images, payment widgets, or entire sensitive sections.

### `maskAllText` and `maskAllInputs`

```typescript
// Defaults (most secure):
Sentry.replayIntegration({
  maskAllText: true,    // every text node → ***
  maskAllInputs: true,  // every <input> value → ***
});

// Unmask everything (e.g., non-sensitive marketing site):
Sentry.replayIntegration({
  maskAllText: false,
  maskAllInputs: false,
  blockAllMedia: false,
});
```

### `mask` and `unmask` — Selector-Based Text Masking

`mask`: Additional CSS selectors whose text is masked **in addition to** `maskAllText`.

`unmask`: CSS selectors **exempt** from masking, even when `maskAllText: true`.

```typescript
Sentry.replayIntegration({
  maskAllText: true,
  // Reveal specific safe elements:
  unmask: ['.app-title', 'nav a', '.breadcrumb', '[data-public]'],
  // Explicitly mask additional elements even with maskAllText: false:
  mask: ['.user-email', '#account-number', '.billing-address'],
});
```

> **v7 → v8 migration:** In v7, `unmask` defaulted to `['.sentry-unmask', '[data-sentry-unmask]']`. In v8, the default is `[]`. To restore v7 behavior:
> ```typescript
> Sentry.replayIntegration({
>   unmask: ['.sentry-unmask', '[data-sentry-unmask]'],
> });
> ```

### `block` and `unblock` — Selector-Based Element Blocking

`block`: Additional CSS selectors to replace with a placeholder, on top of `blockAllMedia`.

`unblock`: CSS selectors **exempt** from blocking, even when `blockAllMedia: true`.

```typescript
Sentry.replayIntegration({
  blockAllMedia: true,
  // Show specific images even though blockAllMedia is on:
  unblock: ['.product-thumbnail', 'img.company-logo', '.hero-banner'],
  // Block additional sensitive elements:
  block: ['#payment-iframe', '.ssn-display', '.confidential-report'],
});
```

> **v7 → v8 migration:** Same as unmask — in v8, `unblock` defaults to `[]`. To restore:
> ```typescript
> Sentry.replayIntegration({
>   unblock: ['.sentry-unblock', '[data-sentry-unblock]'],
> });
> ```

### `ignore` — Input Event Suppression

Suppresses keypress and input value events on specific fields. The element remains visible in the replay; the SDK just doesn't record what the user types.

```typescript
Sentry.replayIntegration({
  ignore: ['#otp-code', '.credit-card-number', '#ssn-input'],
});
```

### HTML Attribute API — Inline Privacy Control in JSX

Apply privacy controls directly in your React components without touching SDK config:

| Attribute | Class equivalent | Effect |
|-----------|-----------------|--------|
| `data-sentry-mask` | `sentry-mask` | Masks this element's text content |
| `data-sentry-unmask` | `sentry-unmask` | Unmasks this element (overrides `maskAllText`) |
| `data-sentry-block` | `sentry-block` | Replaces entire element with placeholder |
| `data-sentry-unblock` | `sentry-unblock` | Shows this element (overrides `blockAllMedia`) |
| `data-sentry-ignore` | `sentry-ignore` | Suppresses input events |

```tsx
// Mask a specific field even if maskAllText is false:
<p data-sentry-mask>{user.fullName}</p>

// Safe to display even with maskAllText: true:
<h1 data-sentry-unmask>Welcome to Our App</h1>

// Block entire subtree — shows as grey box in replay:
<div data-sentry-block>
  <CreditCardForm />
</div>

// Show this image even with blockAllMedia: true:
<img data-sentry-unblock src="/company-logo.png" alt="Logo" />

// Record the field but not what the user types:
<input data-sentry-ignore type="password" placeholder="Password" />
```

> **SDK v8 note:** For the `data-sentry-*` attributes to be recognized automatically, they are built into the SDK's default selector lists. The class-based equivalents (`.sentry-mask`, etc.) require explicit listing in `mask`/`unmask`/`block`/`unblock` options in v8.

### `maskFn` — Custom Text Replacement Function

Controls how masked text is transformed. Receives the original string, returns the replacement:

```typescript
Sentry.replayIntegration({
  maskFn: (text) => {
    // Default behavior — asterisks preserving length:
    return '*'.repeat(text.length);

    // Fixed placeholder:
    return '[REDACTED]';

    // Preserve structure, mask content:
    return text[0] + '*'.repeat(Math.max(0, text.length - 1));

    // Mask only digits (preserve non-sensitive structure):
    return text.replace(/\d/g, '*');
  },
});
```

### Three Privacy Configuration Modes

**Mode 1 — Maximum Privacy (default):** Mask everything, reveal nothing

```typescript
Sentry.replayIntegration({
  maskAllText: true,
  maskAllInputs: true,
  blockAllMedia: true,
});
```

**Mode 2 — Selective Masking (balanced):** Show most UI, hide sensitive fields

```typescript
Sentry.replayIntegration({
  maskAllText: false,
  blockAllMedia: false,
  maskAllInputs: true,              // still hide input values
  mask: ['#ssn', '#dob', '.pii'],   // mask these explicitly
  block: ['#payment-form', '.private-avatar'],
});
```

**Mode 3 — Whitelist (mask-all, unmask-approved):** Start fully masked, allow-list safe UI

```typescript
Sentry.replayIntegration({
  maskAllText: true,
  blockAllMedia: true,
  unmask: ['nav', 'header', '.app-chrome', '.breadcrumb', '[data-public]'],
  unblock: ['img.product-image', '.marketing-hero', '.public-icon'],
});
```

### How React Component Trees Interact with Masking

Masking operates on the **rendered DOM**, not React component hierarchy. Key behaviors:

- Masking **cascades** through the DOM tree — a `data-sentry-mask` on a parent masks all child text nodes
- Blocking a parent **hides everything inside** — the entire subtree is replaced with a placeholder box
- `unmask`/`unblock` on a child **overrides** the parent's mask/block for that specific subtree
- React's virtual DOM is invisible to Replay — it observes via `MutationObserver` on the real DOM
- Conditionally rendered elements (e.g., toggled modals) are captured when they appear in the DOM

```tsx
// Masking cascades to all children:
<div data-sentry-mask>
  <UserProfile />      {/* All text inside UserProfile is masked */}
  <ContactInfo />      {/* This too */}
</div>

// Child can opt out of parent masking:
<div data-sentry-mask>
  <AccountNumber />                           {/* masked */}
  <span data-sentry-unmask>Account Type</span> {/* visible */}
</div>

// Block a payment widget; unblock the logo inside:
<div data-sentry-block>
  <PaymentProcessor />
  <img data-sentry-unblock src="/payment-logo.svg" />  {/* shows in replay */}
</div>
```

### `beforeAddRecordingEvent` — Custom Event Scrubbing

Available since v7.53.0. Intercepts every recording event before it is buffered. Return `null` to drop, return the event (mutated or not) to keep:

```typescript
Sentry.replayIntegration({
  beforeAddRecordingEvent: (event) => {
    // Drop noisy console breadcrumbs
    if (event.data.tag === 'breadcrumb' && event.data.payload?.category === 'console') {
      return null;
    }

    // Only capture network events for 4xx/5xx responses
    if (
      event.data.tag === 'performanceSpan' &&
      (event.data.payload.op === 'resource.fetch' ||
        event.data.payload.op === 'resource.xhr')
    ) {
      const status = event.data.payload.data?.statusCode;
      if (status && status < 400) return null;
    }

    return event;
  },
});
```

### Scrubbing URLs via `addEventProcessor`

To redact sensitive data from URLs in the replay event metadata (not the recording stream):

```typescript
Sentry.addEventProcessor((event) => {
  if (event.type !== 'replay_event') return event;

  const scrub = (url: string) =>
    url.replace(/\/users\/[a-z0-9-]+\//gi, '/users/[id]/');

  event.urls = event.urls?.map(scrub);
  return event;
});
```

### `srcdoc` Iframe Warning

Elements using the `srcdoc` attribute bypass masking logic. Always block them explicitly:

```typescript
Sentry.replayIntegration({
  block: ['iframe[srcdoc]'],
});
```

---

## Network Request Recording

### What Is Captured by Default

For every `fetch` and `XHR` request, without any configuration:

| Field | Captured? |
|-------|-----------|
| URL | ✅ Yes |
| HTTP method | ✅ Yes |
| HTTP status code | ✅ Yes |
| Request body size (bytes) | ✅ Yes |
| Response body size (bytes) | ✅ Yes |
| Request/response body content | ❌ No |
| Custom headers | ❌ No |

### `networkDetailAllowUrls` — Enable Body and Header Capture

Body and header capture is **opt-in** and only activates for URLs that match this list:

```typescript
Sentry.replayIntegration({
  networkDetailAllowUrls: [
    window.location.origin,              // same-origin (recommended minimum)
    'https://api.myapp.com',             // specific domain
    /^https:\/\/api\.myapp\.com\//,      // regex pattern
    '/api/',                             // substring match
    'graphql',                           // matches any URL containing "graphql"
  ],
});
```

> **Security:** Only allowlist your own APIs. Never include third-party payment processors, auth providers, or analytics endpoints.

### `networkDetailDenyUrls` — Exclude Sensitive Endpoints

Takes precedence over `networkDetailAllowUrls`. Matching URLs never have bodies/headers captured:

```typescript
Sentry.replayIntegration({
  networkDetailAllowUrls: [window.location.origin],
  networkDetailDenyUrls: [
    '/api/auth',
    '/api/login',
    '/api/payment',
    '/api/users/me',
    /\/sensitive\//,
    /\/admin\//,
  ],
});
```

### `networkCaptureBodies` (boolean, default: `true`)

Controls whether request/response bodies are captured for allowlisted URLs. Set `false` to capture only headers and metadata without body content:

```typescript
Sentry.replayIntegration({
  networkDetailAllowUrls: ['https://api.myapp.com'],
  networkCaptureBodies: false,   // headers yes, bodies no
});
```

**Body format support:**

| Format | Captured |
|--------|----------|
| `application/json` | ✅ Yes |
| XML | ✅ Yes |
| `text/plain` | ✅ Yes |
| `multipart/form-data` (text fields) | ✅ Yes |
| Binary / byte arrays | ❌ No |
| File uploads | ❌ No |
| Blobs / media streams | ❌ No |

Bodies are truncated at **150,000 characters** (150 KB). This limit is not configurable.

### `networkRequestHeaders` and `networkResponseHeaders`

By default, only `Content-Type`, `Content-Length`, and `Accept` are captured. Add more:

```typescript
Sentry.replayIntegration({
  networkDetailAllowUrls: [window.location.origin],
  networkRequestHeaders: [
    'Cache-Control',
    'X-Request-ID',
    'X-Correlation-ID',
    // ⚠️ Avoid: 'Authorization', 'Cookie' — contain credentials
  ],
  networkResponseHeaders: [
    'Referrer-Policy',
    'X-Request-ID',
    'X-Response-Time',
    'CF-Ray',
    'X-Cache',
  ],
});
```

> ⚠️ Never capture `Authorization`, `Cookie`, or `Set-Cookie` headers in production. They contain bearer tokens and session credentials.

### Capturing GraphQL Operation Names

GraphQL requests all go to the same endpoint. To distinguish operations, capture the request body and filter by operation name in `beforeAddRecordingEvent`:

```typescript
Sentry.replayIntegration({
  networkDetailAllowUrls: ['https://api.myapp.com/graphql'],
  networkCaptureBodies: true,
  beforeAddRecordingEvent: (event) => {
    // Optionally: drop mutations from replay to reduce noise
    if (
      event.data.tag === 'performanceSpan' &&
      event.data.payload.op === 'resource.fetch'
    ) {
      const body = event.data.payload.data?.request?.body;
      if (body?.operationName === 'InternalAdminMutation') return null;
    }
    return event;
  },
});
```

### Apollo Client Body Capture Issue

Apollo uses an `AbortController` to cancel in-flight queries on component unmount. This abort fires before Replay can read the response body, resulting in empty response bodies.

**Workaround:** Supply a custom signal that doesn't abort the Replay read:

```typescript
import { HttpLink } from '@apollo/client';

const httpLink = new HttpLink({
  uri: '/graphql',
  // Don't pass an AbortController signal here, or use your own
  // that only cancels at route-change boundaries rather than component unmount
});
```

---

## Canvas Recording

### Setup — `replayCanvasIntegration()`

Canvas elements are **not** recorded by default. Add a second integration:

```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "...",
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
  integrations: [
    Sentry.replayIntegration(),
    Sentry.replayCanvasIntegration(),   // requires @sentry/react ≥7.98.0
  ],
});
```

> ⚠️ **No PII scrubbing in canvas recordings.** If your canvas renders sensitive data (user documents, medical images, profile photos), either avoid canvas recording or sanitize the canvas content before each snapshot.

### Standard 2D Canvas

For standard 2D canvas, the default configuration records automatically — no extra code needed. The integration periodically snapshots the canvas content.

### 3D / WebGL Canvas — Manual Snapshotting

WebGL requires `enableManualSnapshot: true` because:

1. The integration must enable `preserveDrawingBuffer` on the WebGL context to read pixel data
2. `preserveDrawingBuffer` prevents the GPU from discarding draw buffers after compositing — this can degrade performance on complex scenes
3. Manual mode lets you control exactly when snapshots are taken

```typescript
Sentry.init({
  integrations: [
    Sentry.replayIntegration(),
    Sentry.replayCanvasIntegration({ enableManualSnapshot: true }),
  ],
});

// React ref + render loop:
import { useRef, useEffect } from 'react';

function WebGLScene() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current!;
    const gl = canvas.getContext('webgl');

    function render() {
      // ... your WebGL rendering ...

      // After rendering, snapshot for Replay:
      const canvasIntegration = Sentry.getClient()?.getIntegrationByName('ReplayCanvas');
      canvasIntegration?.snapshot(canvas);

      requestAnimationFrame(render);
    }

    requestAnimationFrame(render);
  }, []);

  return <canvas ref={canvasRef} id="scene" />;
}
```

### WebGPU Canvas

WebGPU requires an additional flag since it doesn't use `requestAnimationFrame` in the same way:

```typescript
Sentry.replayCanvasIntegration({ enableManualSnapshot: true });

// In your render loop:
const canvasIntegration = Sentry.getClient()?.getIntegrationByName('ReplayCanvas');
canvasIntegration?.snapshot(canvasRef, { skipRequestAnimationFrame: true });
```

### Cross-Origin Canvas Content

If your canvas draws images/videos from a different origin, the browser throws a `SecurityError` when Replay calls `canvas.toDataURL()` (tainted canvas).

**Fix:** Add `crossorigin="anonymous"` to media elements and configure CORS on your CDN:

```tsx
<img crossOrigin="anonymous" src="https://cdn.example.com/texture.png" />
<video crossOrigin="anonymous" src="https://cdn.example.com/clip.mp4" />
```

Your CDN must respond with `Access-Control-Allow-Origin: *` (or your specific origin).

---

## Lazy Loading Replay

Replay adds ~50 KB (gzipped) to your initial bundle. If initial page load performance is critical, defer loading until after the first render:

```typescript
// src/instrument.ts — initialize without replay
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  integrations: [],   // no replay at startup
});

// Load replay after initial render (e.g., in a useEffect or after login):
async function enableReplay() {
  const replayIntegration = await Sentry.lazyLoadIntegration('replayIntegration');
  Sentry.addIntegration(
    replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    })
  );
}
```

**Or with dynamic import:**

```typescript
async function enableReplay() {
  const { replayIntegration } = await import('@sentry/react');
  Sentry.addIntegration(replayIntegration({ maskAllText: true }));
}
```

**Trade-off:** Any errors or sessions that occur before the integration loads are not captured. Prefer lazy loading when:
- The app has a significant unauthenticated surface (home page, landing page)
- You only want replay for authenticated users (load after login)
- Initial page load performance is actively measured

---

## Advanced Configuration

### `beforeErrorSampling` — Control Which Errors Trigger Replay

Only relevant in buffer mode (`replaysOnErrorSampleRate > 0`). Called before the dice roll for error-based sampling. Return `false` to prevent the error from triggering a replay capture:

```typescript
Sentry.replayIntegration({
  beforeErrorSampling: (event) => {
    // Don't capture replay for known benign errors
    if (event.exception?.values?.[0]?.value?.includes('ResizeObserver loop')) {
      return false;
    }
    // Skip console-captured errors (from captureConsoleIntegration)
    if (event.logger === 'console') {
      return false;
    }
    // Skip test environments
    if (event.tags?.environment === 'test') {
      return false;
    }
    // Skip low-severity user-land errors
    if (event.level === 'warning') {
      return false;
    }
    return true;
  },
});
```

> **`captureConsoleIntegration` warning:** If you use this integration, every `console.error()` call captures a Sentry event, which can trigger replay sampling for every console error. Use `beforeErrorSampling` to filter these out.

### `mutationBreadcrumbLimit` and `mutationLimit`

Protect against pages that cause excessive DOM mutations (real-time dashboards, animated charts, chat feeds):

| Option | Default | Behavior |
|--------|---------|----------|
| `mutationBreadcrumbLimit` | `750` | Adds a warning breadcrumb to the replay timeline when exceeded |
| `mutationLimit` | `10000` | Stops recording entirely to protect page performance |

```typescript
Sentry.replayIntegration({
  mutationBreadcrumbLimit: 500,   // warn earlier for noisy pages
  mutationLimit: 5000,            // stop recording earlier
});
```

**When you hit `mutationLimit`, fix the root cause:**
- Virtualize long lists with `react-virtual`, `react-window`, or TanStack Virtual
- Paginate large data tables instead of rendering all rows
- Use CSS animations instead of JS-driven DOM mutations
- Batch React state updates (`unstable_batchedUpdates` or React 18 automatic batching)

### `slowClickIgnoreSelectors`

Sentry automatically detects **dead clicks** (click with no DOM response) and **rage clicks** (3+ clicks within 7 seconds). Suppress this detection for elements that intentionally don't mutate the DOM:

```typescript
Sentry.replayIntegration({
  slowClickIgnoreSelectors: [
    'a[download]',           // download links
    '.copy-to-clipboard',    // clipboard buttons
    '[aria-label*="print" i]',
    '.pdf-export-btn',
    '#video-player',         // video controls
    '.toast-close',          // dismissal buttons that animate out
  ],
});
```

### `workerUrl` — Self-Host the Compression Worker

By default, Sentry creates the compression worker via a `blob:` URL. If your CSP blocks `blob:`, self-host the worker:

1. Copy the worker file from `node_modules/@sentry/replay/build/npm/esm/worker/` after install
2. Serve it from your own origin (e.g., `/assets/sentry-replay-worker.min.js`)
3. Configure the path:

```typescript
Sentry.replayIntegration({
  workerUrl: '/assets/sentry-replay-worker.min.js',
});
```

**With Sentry Vite Plugin (v2.10.0+):**

```typescript
// vite.config.ts
sentryVitePlugin({
  bundleSizeOptimizations: {
    excludeReplayWorker: true,  // extract worker as separate asset
  },
})
```

> The worker is forward/backward compatible within the same major SDK version. Update it when upgrading major versions.

### Manual Session Control

When both sample rates are `0`, control recording programmatically:

```typescript
Sentry.init({
  dsn: "...",
  replaysSessionSampleRate: 0,
  replaysOnErrorSampleRate: 0,
  integrations: [Sentry.replayIntegration()],
});

const replay = Sentry.getReplay();

// Start continuous recording:
replay.start();

// Start in buffer mode (hold in memory, send on flush):
replay.startBuffering();

// Stop recording and flush all pending data:
await replay.stop();

// Upload buffered data without stopping:
await replay.flush();

// Get current replay ID (for linking to support tickets, etc.):
const replayId = replay.getReplayId();
const replayUrl = `https://YOUR-ORG.sentry.io/replays/${replayId}/`;
```

**React Hook pattern for support widget integration:**

```tsx
import { useEffect } from 'react';
import * as Sentry from '@sentry/react';

function SupportButton() {
  const handleOpen = async () => {
    const replay = Sentry.getReplay();
    await replay.flush();
    const replayId = replay.getReplayId();

    openSupportWidget({
      metadata: {
        sentryReplayUrl: replayId
          ? `https://myorg.sentry.io/replays/${replayId}/`
          : undefined,
      },
    });
  };

  return <button onClick={handleOpen}>Contact Support</button>;
}
```

### Deferred Initialization (Feature Flags / A/B Testing)

If your sampling rates come from an external feature flag service:

```typescript
// Start Sentry without replay
Sentry.init({
  dsn: "...",
  integrations: [],
});

// After feature flags resolve:
async function initReplayFromFlags() {
  const flags = await featureFlagService.getFlags();

  const client = Sentry.getClient();
  if (!client) return;

  const options = client.getOptions();
  options.replaysSessionSampleRate = flags.replaySessionRate;
  options.replaysOnErrorSampleRate = flags.replayErrorRate;

  const replay = Sentry.replayIntegration({ maskAllText: true });
  client.addIntegration(replay);
}
```

### Route-Based Recording (Selective Pages)

```typescript
Sentry.init({
  dsn: "...",
  replaysSessionSampleRate: 0,
  replaysOnErrorSampleRate: 0,
  integrations: [Sentry.replayIntegration()],
});

// React Router example: only record checkout flow
import { useLocation } from 'react-router-dom';
import { useEffect } from 'react';

function ReplayController() {
  const location = useLocation();

  useEffect(() => {
    const replay = Sentry.getReplay();
    const isCheckout = location.pathname.startsWith('/checkout');

    if (isCheckout && !replay.getReplayId()) {
      replay.start();
    } else if (!isCheckout && replay.getReplayId()) {
      replay.stop();
    }
  }, [location.pathname]);

  return null;
}
```

---

## Understanding Sessions

### What Is a Session vs a Segment

- **Replay Session:** The full recording from start to end — one replay visible in the Sentry UI. Has a unique `replayId`.
- **Segment:** A chunk of recording data transmitted to the server. Large recordings are split into segments sent in sequence and reassembled server-side.

One session = multiple segments streamed over time.

### Session Lifecycle

| Event | Session behavior |
|-------|-----------------|
| SDK initializes | Sampling evaluated; session or buffer mode begins |
| User is inactive 15+ minutes | Session ends; new session starts on next interaction |
| Total duration exceeds `maxReplayDuration` | Session ends; new session starts (re-sampled) |
| User closes the tab | Session ends; `sessionStorage` is cleared |
| `replay.stop()` called | Session ends; pending data flushed |

An "interaction" that resets the idle timer = mouse click OR browser navigation event.

### Session Mode vs Buffer Mode

| Aspect | Session Mode | Buffer Mode |
|--------|-------------|-------------|
| Activated when | `replaysSessionSampleRate > 0` AND session is sampled | Only `replaysOnErrorSampleRate > 0` |
| Data transmission | Continuous real-time chunks to Sentry | Held in memory; sent only on error |
| Memory usage | Low (continuously streamed out) | ~2–5 MB in RAM (last ~60 seconds) |
| What appears in Sentry | Full session from start | 60s before error + rest of session |
| Idle timeout | 15 minutes | 15 minutes |
| Max duration | `maxReplayDuration` | `maxReplayDuration` |

### How Buffer Mode Flushes on Error

1. Error occurs in the browser
2. Sentry SDK captures the error event
3. `beforeErrorSampling(event)` is called — `return false` to abort
4. Dice roll against `replaysOnErrorSampleRate` — fail → buffer discarded
5. Pass → buffered ~60 seconds of DOM events sent to Sentry
6. Recording continues in session mode for the remainder of the session
7. Error event is linked to the replay via `replayId` tag

---

## Performance Considerations

### Bundle Size

| Component | Size (gzipped) |
|-----------|---------------|
| `replayIntegration()` | ~50 KB |
| `replayCanvasIntegration()` | Additional (small) |
| Compression Web Worker | Extracted as separate chunk |

**Reduction strategies:**
- Use `lazyLoadIntegration('replayIntegration')` to keep it out of the critical bundle
- Set `excludeReplayWorker: true` in the Sentry bundler plugin

### Runtime Overhead

| Operation | Performance impact |
|-----------|------------------|
| DOM observation (MutationObserver) | Low — reads, doesn't write |
| Compression | Off main thread via Web Worker |
| Network interception (fetch/XHR) | Low — thin wrappers |
| Canvas recording (2D) | Moderate — pixel buffer reads |
| Canvas recording (WebGL with `preserveDrawingBuffer`) | High — prevents GPU buffer discard |
| High DOM mutation rate | High — can trigger `mutationLimit` stop |

**Errors-only mode has near-zero overhead** when no error occurs — the in-memory buffer (~2–5 MB) is the only cost.

---

## CSP Requirements

Without correct CSP headers, Replay **fails silently** — no error in the console, no replay recorded.

### Required Directives

```
worker-src 'self' blob:;
child-src 'self' blob:;    ← required for Safari ≤15.4
```

**As an HTTP response header:**
```http
Content-Security-Policy: default-src 'self'; worker-src 'self' blob:; child-src 'self' blob:;
```

**As a meta tag:**
```html
<meta
  http-equiv="Content-Security-Policy"
  content="default-src 'self'; worker-src 'self' blob:; child-src 'self' blob:;"
/>
```

**When using `workerUrl` (self-hosted worker):**
```
worker-src 'self';    ← blob: not required
child-src 'self';
```

**If using a `tunnel` to relay events through your own server:**
```
connect-src 'self' https://o<ORG_ID>.ingest.sentry.io;
```
Or with `tunnel: "/sentry-tunnel"`:
```
connect-src 'self';    ← all requests go to your own origin
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| No replays appearing at all | CSP blocks Web Worker blob URL | Add `worker-src 'self' blob:` and `child-src 'self' blob:` to CSP |
| No replays appearing | `replayIntegration()` not in init | Confirm it's in the `integrations` array in `Sentry.init()` |
| No replays appearing | Both sample rates are `0` | Set `replaysSessionSampleRate: 0.1` or `replaysOnErrorSampleRate: 1.0` |
| No replays appearing | SDK version too old | Upgrade to `@sentry/react` ≥7.27.0 |
| No replays appearing | Running in SSR/Node context | Ensure `replayIntegration()` is only in browser-side init code |
| No replays appearing | `minReplayDuration` too high | Lower it or set to `0` for debugging |
| All text shows as `***` | `maskAllText: true` (default) | Expected. Use `unmask` or `data-sentry-unmask` to reveal safe content |
| Replay cuts off early | `mutationLimit` exceeded | Increase limit or virtualize your lists; check for DOM thrash |
| Replay shows broken layout | External CSS/fonts blocked by CORS | Add `sentry.io` to `Access-Control-Allow-Origin` on your CDN |
| Images missing in replay | External images blocked by CORS | Add `sentry.io` to CDN CORS policy for image assets |
| Network bodies always empty | URL not in `networkDetailAllowUrls` | Add your API domain to the allowlist |
| Network bodies empty (Apollo) | AbortController cancels before Replay reads | Don't abort on component unmount; use route-level cancellation |
| Network body truncated | > 150,000 characters | Expected behavior — limit is not configurable |
| Canvas not recording | Not added by default | Add `replayCanvasIntegration()` to `integrations` array |
| Canvas SecurityError | Cross-origin media taints canvas | Add `crossOrigin="anonymous"` to `<img>`/`<video>` and enable CORS on CDN |
| WebGL canvas blank in replay | `preserveDrawingBuffer` not enabled | Use `enableManualSnapshot: true` on `replayCanvasIntegration()` |
| Rage/dead clicks on download buttons | SDK detects non-DOM-mutating clicks | Add selector to `slowClickIgnoreSelectors` |
| Replays triggered by `console.error` | `captureConsoleIntegration` sends events | Use `beforeErrorSampling` to return `false` when `event.logger === 'console'` |
| Worker CSP error in console | CSP missing `blob:` in `worker-src` | Add `worker-src 'self' blob:` or use `workerUrl` with self-hosted worker |
| High replay volume / storage costs | `replaysSessionSampleRate` too high | Lower it; keep `replaysOnErrorSampleRate: 1.0` for error coverage |
| Replay blocked by ad-blockers | Direct requests to Sentry ingest | Set `tunnel: "/sentry-tunnel"` and implement a server-side relay |

---

## Complete Configuration Reference

```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,

  // ── SAMPLING (init-level, not in replayIntegration) ────────────
  replaysSessionSampleRate: 0.1,      // 10% full session recording
  replaysOnErrorSampleRate: 1.0,      // 100% error-triggered recording

  integrations: [
    Sentry.replayIntegration({

      // ── SESSION ──────────────────────────────────────────────
      stickySession: true,             // survive page refreshes
      minReplayDuration: 5000,         // discard replays < 5s (max: 15000)
      maxReplayDuration: 3600000,      // cap at 1 hour (server limit)

      // ── PRIVACY ──────────────────────────────────────────────
      maskAllText: true,               // mask all text (default: true)
      maskAllInputs: true,             // mask all inputs (default: true)
      blockAllMedia: true,             // block all media (default: true)
      mask: ['.pii', '[data-sensitive]'],
      unmask: ['.app-chrome', 'nav', '.public-label'],
      block: ['#payment-form', '.ssn-widget'],
      unblock: ['.company-logo', '.product-thumbnail'],
      ignore: ['#otp-field'],
      maskFn: (text) => '*'.repeat(text.length),

      // ── NETWORK ──────────────────────────────────────────────
      networkDetailAllowUrls: [window.location.origin, 'https://api.myapp.com'],
      networkDetailDenyUrls: ['/api/auth', '/api/payment', /\/admin\//],
      networkCaptureBodies: true,
      networkRequestHeaders: ['X-Request-ID', 'Cache-Control'],
      networkResponseHeaders: ['X-Request-ID', 'X-Response-Time'],

      // ── DOM PROTECTION ────────────────────────────────────────
      mutationLimit: 10000,
      mutationBreadcrumbLimit: 750,
      slowClickIgnoreSelectors: ['a[download]', '.copy-btn', '.print-btn'],

      // ── ADVANCED ─────────────────────────────────────────────
      workerUrl: '/assets/sentry-replay-worker.min.js',  // if strict CSP
      beforeAddRecordingEvent: (event) => {
        if (event.data.tag === 'breadcrumb' &&
            event.data.payload?.category === 'console') return null;
        return event;
      },
      beforeErrorSampling: (event) => {
        if (event.logger === 'console') return false;
        return true;
      },
    }),

    // Canvas recording (optional):
    Sentry.replayCanvasIntegration({
      enableManualSnapshot: false,   // set true for WebGL/WebGPU
    }),
  ],
});
```

---

## Reference: Tracing

# Tracing — Sentry React SDK

> Minimum SDK: `@sentry/react` ≥8.0.0+  
> `reactRouterV7BrowserTracingIntegration`: requires `@sentry/react` ≥8.0.0  
> `ignoreSpans`: requires `@sentry/react` ≥10.2.0  
> `enableAsyncRouteHandlers` + `lazyRouteManifest`: requires `@sentry/react` ≥10.39.0  
> `enableLongAnimationFrame`: requires `@sentry/react` ≥8.18.0

---

## How Automatic Tracing Works

| What's traced | Op | How |
|---------------|----|-----|
| Initial page load | `pageload` | `browserTracingIntegration()` reads `window.performance` timing |
| Client-side navigations | `navigation` | History API (pushState / replaceState) |
| `fetch()` requests | `http.client` | Patched automatically |
| `XMLHttpRequest` requests | `http.client` | Patched automatically |
| Long Tasks (main-thread blocks > 50ms) | `ui.long-task` | `PerformanceLongTaskTiming` observer |
| Long Animation Frames (≥8.18.0) | `ui.long-animation-frame` | `PerformanceLongAnimationFrameTiming` observer |
| INP interactions | `ui.interaction` | `PerformanceEventTiming` observer, emitted on page hide |

---

## Core Setup

```typescript
// src/instrument.ts (imported FIRST in main.tsx / index.tsx)
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,

  integrations: [
    Sentry.browserTracingIntegration(),
  ],

  // Tracing sample rates
  tracesSampleRate: 1.0,   // 100% in dev; lower to 0.1–0.2 in production

  // Which outgoing requests get sentry-trace + baggage headers
  tracePropagationTargets: [
    "localhost",
    /^https:\/\/api\.yourapp\.com/,
  ],
});
```

> **To disable tracing entirely:** omit both `tracesSampleRate` and `tracesSampler`. Setting `tracesSampleRate: 0` is **not** the same — the integration still runs, it just doesn't send data.

---

## `browserTracingIntegration` — All Options

```typescript
Sentry.browserTracingIntegration({
  /* option: default */
})
```

### Page Load & Navigation

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `instrumentPageLoad` | `boolean` | `true` | Create a `pageload` span on initial load. Disable when you want to name the span yourself via `startBrowserTracingPageLoadSpan`. |
| `instrumentNavigation` | `boolean` | `true` | Create `navigation` spans on History API changes. |

### Span Lifecycle / Timing

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `idleTimeout` | `number` (ms) | `1000` | How long to wait after the last child span finishes before closing the root span. The root takes the last child's end time as its own end time. |
| `finalTimeout` | `number` (ms) | `30000` | Hard cap on how long a pageload/navigation span can live. Prevents runaway open spans. |
| `childSpanTimeout` | `number` (ms) | `15000` | If a child span hasn't finished within this time, the root span finishes anyway. |
| `markBackgroundSpan` | `boolean` | `true` | When the tab goes to the background, mark the active span as `cancelled` and close it. |

### HTTP Request Spans

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `traceFetch` | `boolean` | `true` | Auto-create child spans for `fetch()` calls. |
| `traceXHR` | `boolean` | `true` | Auto-create child spans for `XMLHttpRequest` calls. |
| `enableHTTPTimings` | `boolean` | `true` | Enrich HTTP spans with Resource Timing API data: DNS lookup, TLS handshake, connection, TTFB, download time. |
| `shouldCreateSpanForRequest` | `(url: string) => boolean` | — | Return `false` to skip creating a span for a specific URL. |
| `onRequestSpanStart` | `(span, requestInfo) => void` | — | Fires when a fetch/XHR span starts. Add custom attributes based on headers or URL. |

### Performance Observations

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enableLongTask` | `boolean` | `true` | Capture spans for Long Tasks — main-thread blocks > 50ms. |
| `enableLongAnimationFrame` | `boolean` | `true` | Capture Long Animation Frames (LoAF). Supersedes Long Tasks for most use cases. SDK ≥8.18.0. |
| `enableInp` | `boolean` | `true` (SDK 8.x+) | Auto-capture INP events as standalone spans. In SDK 7.x, defaults to `false` and must be opted in. |
| `interactionsSampleRate` | `number` | `1.0` | Applied **on top of** `tracesSampleRate` for INP spans. `interactionsSampleRate: 0.5` + `tracesSampleRate: 0.1` = **5%** of interactions captured. |

### Span Naming

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `beforeStartSpan` | `(context: StartSpanOptions) => StartSpanOptions` | — | Called just before every pageload or navigation span is created. Mutate and return `context` to rename the span, change `op`, or add attributes. Primary use: parameterize URLs (`/users/123` → `/users/<id>`). |

```typescript
browserTracingIntegration({
  beforeStartSpan: (context) => ({
    ...context,
    name: location.pathname
      .replace(/\/[a-f0-9]{8,}/g, "/<hash>")  // strip hashes/UUIDs
      .replace(/\/\d+/g, "/<id>"),              // strip numeric IDs
  }),
})
```

### Trace Linking

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `linkPreviousTrace` | `'in-memory' \| 'session-storage' \| false` | `'in-memory'` | How a new pageload links back to the previous trace. `'session-storage'` persists across hard reloads. `false` disables linking. |
| `enableReportPageLoaded` | `boolean` | `false` | Enables `Sentry.reportPageLoaded()` for manually signalling page load completion in complex hydration scenarios. |

### Span Filtering

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ignoreResourceSpans` | `string[]` | `[]` | Skip resource spans by `op` prefix. Example: `["resource.css", "resource.script", "resource.img"]`. |
| `ignorePerformanceApiSpans` | `Array<string \| RegExp>` | `[]` | Skip spans created from `performance.mark()`/`performance.measure()` matching these names. |

### Full Example With All Common Options

```typescript
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,

  integrations: [
    Sentry.browserTracingIntegration({
      // Lifecycle
      idleTimeout: 1000,
      finalTimeout: 30_000,
      childSpanTimeout: 15_000,
      markBackgroundSpan: true,

      // HTTP spans
      traceFetch: true,
      traceXHR: true,
      enableHTTPTimings: true,
      shouldCreateSpanForRequest: (url) =>
        !url.includes("/health") && !url.includes("/__webpack_hmr"),
      onRequestSpanStart: (span, { headers }) => {
        const rid = headers?.["x-request-id"];
        if (rid) span.setAttribute("request.id", rid);
      },

      // Performance observations
      enableLongTask: true,
      enableLongAnimationFrame: true,  // SDK ≥8.18.0
      enableInp: true,
      interactionsSampleRate: 1.0,

      // Span naming
      beforeStartSpan: (context) => ({
        ...context,
        name: context.name.replace(/\/\d+/g, "/<id>"),
      }),

      // Filtering
      ignoreResourceSpans: ["resource.css"],

      // Trace linking
      linkPreviousTrace: "in-memory",
    }),
  ],

  tracesSampleRate: 1.0,
  tracePropagationTargets: ["localhost", /^https:\/\/api\.myapp\.com/],
});
```

---

## What's Auto-Instrumented

### Page Load (`op: "pageload"`)
- Created on initial page render using `window.performance` timing API
- Contains Web Vitals: **LCP**, **CLS**, **FCP**, **TTFB**
- HTTP requests made during page load appear as child spans
- Long Tasks and Long Animation Frames appear as child spans

### Navigation (`op: "navigation"`)
- Created on every client-side navigation via the History API
- Does **not** include Web Vitals (those are page-load only)
- HTTP requests during navigation appear as child spans

### HTTP Spans (`op: "http.client"`)
- Automatic for both `fetch()` and `XMLHttpRequest`
- Captures: method, URL, HTTP status code, response size
- With `enableHTTPTimings`: DNS lookup time, TLS handshake, connection time, TTFB, download time

### Long Task Spans (`op: "ui.long-task"`)
- Created for any main-thread block > 50ms
- Helps identify JavaScript that blocks interactivity

### Long Animation Frame Spans (`op: "ui.long-animation-frame"`)
- SDK 8.18.0+; based on the LoAF API
- Captures render-blocking work including style/layout recalculations
- More accurate than Long Tasks for measuring rendering bottlenecks

### INP / Interaction Spans (`op: "ui.interaction"`)
- Standalone spans capturing Interaction to Next Paint
- Emitted on page hide (tab switch, navigation away)
- Attributes: `component`, `element`, `interaction_type`
- On by default in SDK 8.x+; opt-in (`enableInp: true`) in SDK 7.x

---

## Web Vitals

`browserTracingIntegration()` captures Core Web Vitals automatically and surfaces them in the **Sentry Web Vitals** product module:

| Vital | What it measures | Good | Needs Improvement | Poor |
|-------|-----------------|------|-------------------|------|
| **LCP** — Largest Contentful Paint | Time for largest viewport element to render | ≤ 2.5s | ≤ 4s | > 4s |
| **INP** — Interaction to Next Paint | Time from user interaction to next paint (replaced FID March 2024) | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS** — Cumulative Layout Shift | Sum of unexpected layout shift scores | ≤ 0.1 | ≤ 0.25 | > 0.25 |
| **FCP** — First Contentful Paint | Time for first content to render | ≤ 1s | ≤ 3s | > 3s |
| **TTFB** — Time to First Byte | Time until browser receives first byte | ≤ 100ms | ≤ 200ms | > 200ms |
| **FID** — First Input Delay | *(Legacy — collected but replaced by INP)* | ≤ 100ms | ≤ 300ms | > 300ms |

> **LCP and CLS timing note:** These keep changing after the pageload span ends. Sentry captures their final values via `visibilitychange` and page hide events. INP is similarly emitted as a standalone span on page hide.

**INP in SDK 7.x** (must opt in):
```typescript
browserTracingIntegration({ enableInp: true })
```

---

## React Router Integrations

All React Router integrations live in `@sentry/react`. The core mechanism: **replace** `browserTracingIntegration()` with the router-specific variant. Both cannot be used simultaneously.

---

### React Router v7 (Library Mode)

**Package:** `react-router` (v7)  
**Import source for hooks:** `"react-router"`

#### Method 1 — `createBrowserRouter` (Recommended)

```typescript
// src/instrument.ts
import React from "react";
import {
  createBrowserRouter,
  createRoutesFromChildren,
  matchRoutes,
  useLocation,
  useNavigationType,
} from "react-router";
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  integrations: [
    Sentry.reactRouterV7BrowserTracingIntegration({
      useEffect: React.useEffect,
      useLocation,
      useNavigationType,
      createRoutesFromChildren,
      matchRoutes,
    }),
  ],
  tracesSampleRate: 1.0,
  tracePropagationTargets: ["localhost", /^https:\/\/api\.myapp\.com/],
});
```

```typescript
// src/router.ts
import { createBrowserRouter } from "react-router";
import * as Sentry from "@sentry/react";
import { RootLayout, RootErrorBoundary } from "./layouts";
import { HomePage, UsersPage, UserDetailPage, DashboardPage } from "./pages";

// Wrap createBrowserRouter with Sentry instrumentation
const sentryCreateBrowserRouter = Sentry.wrapCreateBrowserRouterV7(createBrowserRouter);

export const router = sentryCreateBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <RootErrorBoundary />,  // see Error Boundary section below
    children: [
      { index: true,                      element: <HomePage /> },
      { path: "users",                    element: <UsersPage /> },
      { path: "users/:userId",            element: <UserDetailPage /> },
      { path: "dashboard",                element: <DashboardPage />,
        children: [
          { path: "analytics",            element: <AnalyticsPage /> },
        ],
      },
    ],
  },
]);
```

```typescript
// src/main.tsx
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router";
import "./instrument";   // ← MUST be first
import { router } from "./router";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <RouterProvider router={router} />
);
```

**Lazy routes (SDK ≥10.39.0):** add `enableAsyncRouteHandlers` and declare all route paths:

```typescript
Sentry.reactRouterV7BrowserTracingIntegration({
  useEffect: React.useEffect,
  useLocation,
  useNavigationType,
  createRoutesFromChildren,
  matchRoutes,
  enableAsyncRouteHandlers: true,
  lazyRouteManifest: [
    "/",
    "/users",
    "/users/:userId",
    "/users/:userId/settings",
    "/dashboard",
    "/dashboard/analytics",
  ],
})
```

**Other router factories:**

| Factory | Sentry wrapper |
|---------|---------------|
| `createBrowserRouter` | `Sentry.wrapCreateBrowserRouterV7` |
| `createMemoryRouter` | `Sentry.wrapCreateMemoryRouterV7` |
| `createHashRouter` | `Sentry.wrapCreateBrowserRouterV7` (works for both) |

#### Method 2 — `<Routes>` Component

```typescript
import React from "react";
import ReactDOM from "react-dom/client";
import {
  BrowserRouter, Routes, Route,
  createRoutesFromChildren, matchRoutes,
  useLocation, useNavigationType,
} from "react-router";
import * as Sentry from "@sentry/react";

Sentry.init({
  // ... same init as Method 1
});

// Wrap Routes ONCE at the top level — do NOT wrap nested <Routes>
const SentryRoutes = Sentry.withSentryReactRouterV7Routing(Routes);

function App() {
  return (
    <BrowserRouter>
      <SentryRoutes>
        <Route path="/"               element={<HomePage />} />
        <Route path="/about"          element={<AboutPage />} />
        <Route path="/users/:userId"  element={<UserDetailPage />} />
        <Route path="*"               element={<NotFoundPage />} />
      </SentryRoutes>
    </BrowserRouter>
  );
}
```

Also works with `MemoryRouter` and `HashRouter`.

#### Method 3 — `useRoutes` Hook

```typescript
import { useRoutes, BrowserRouter } from "react-router";
import * as Sentry from "@sentry/react";

// MUST call wrapUseRoutesV7 OUTSIDE any React component
const useSentryRoutes = Sentry.wrapUseRoutesV7(useRoutes);

function App() {
  return useSentryRoutes([
    { path: "/",               element: <HomePage /> },
    { path: "/users/:userId",  element: <UserDetailPage /> },
    { path: "/dashboard",      element: <DashboardPage />,
      children: [
        { path: "analytics",   element: <AnalyticsPage /> },
      ],
    },
  ]);
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <BrowserRouter><App /></BrowserRouter>
);
```

#### Error Boundary (Required for Production Error Capture)

React Router v7's default `errorElement` swallows errors silently. You must capture them manually:

```typescript
import { useRouteError } from "react-router";
import * as Sentry from "@sentry/react";

export function SentryRouteErrorBoundary() {
  const error = useRouteError() as Error;

  React.useEffect(() => {
    if (error) Sentry.captureException(error);
  }, [error]);

  return (
    <div role="alert">
      <h1>Something went wrong</h1>
      <p>{error?.message ?? "An unexpected error occurred."}</p>
    </div>
  );
}

// Apply as errorElement on your root route and any nested boundaries:
const router = sentryCreateBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <SentryRouteErrorBoundary />,
    children: [
      {
        path: "checkout",
        element: <CheckoutPage />,
        errorElement: <SentryRouteErrorBoundary />,  // nested boundary
      },
    ],
  },
]);
```

---

### React Router v6

**Package:** `react-router-dom` (v6)  
**Import source for hooks:** `"react-router-dom"`

#### Method 1 — `createBrowserRouter` (Recommended for v6.4+)

```typescript
import React from "react";
import {
  createBrowserRouter,
  createRoutesFromChildren,
  matchRoutes,
  useLocation,
  useNavigationType,
} from "react-router-dom";
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  integrations: [
    Sentry.reactRouterV6BrowserTracingIntegration({
      useEffect: React.useEffect,
      useLocation,
      useNavigationType,
      createRoutesFromChildren,
      matchRoutes,
    }),
  ],
  tracesSampleRate: 1.0,
});

// Wrap createBrowserRouter
const sentryCreateBrowserRouter =
  Sentry.wrapCreateBrowserRouterV6(createBrowserRouter);

export const router = sentryCreateBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      { index: true,           element: <HomePage /> },
      { path: "users/:userId", element: <UserDetailPage /> },
      { path: "settings",      element: <SettingsPage /> },
    ],
  },
]);
```

**Other router factories (SDK ≥8.50.0):**

| Factory | Sentry wrapper |
|---------|---------------|
| `createBrowserRouter` | `Sentry.wrapCreateBrowserRouterV6` |
| `createMemoryRouter` | `Sentry.wrapCreateMemoryRouterV6` |

#### Method 2 — `<Routes>` Component

```typescript
import {
  BrowserRouter, Routes, Route,
  createRoutesFromChildren, matchRoutes,
  useLocation, useNavigationType,
} from "react-router-dom";
import * as Sentry from "@sentry/react";

Sentry.init({ /* ... same as above */ });

const SentryRoutes = Sentry.withSentryReactRouterV6Routing(Routes);

function App() {
  return (
    <BrowserRouter>
      <SentryRoutes>
        <Route path="/"               element={<HomePage />} />
        <Route path="/users/:userId"  element={<UserPage />} />
        <Route path="*"               element={<NotFoundPage />} />
      </SentryRoutes>
    </BrowserRouter>
  );
}
```

#### Method 3 — `useRoutes` Hook

```typescript
import { useRoutes, BrowserRouter } from "react-router-dom";
import * as Sentry from "@sentry/react";

// Call OUTSIDE components
const useSentryRoutes = Sentry.wrapUseRoutesV6(useRoutes);

function App() {
  return useSentryRoutes([
    { path: "/",              element: <Home /> },
    { path: "/users/:userId", element: <User /> },
  ]);
}
```

---

### React Router v4 / v5

**Package:** `react-router-dom` (v4 or v5) + `history`

#### Method 1 — `withSentryRouting` HOC (Recommended)

```typescript
import React from "react";
import ReactDOM from "react-dom";
import { Route, Router, Switch } from "react-router-dom";
import { createBrowserHistory } from "history";
import * as Sentry from "@sentry/react";

// 1. Create a history instance
const history = createBrowserHistory();

// 2. Init with reactRouterV5BrowserTracingIntegration
Sentry.init({
  dsn: "...",
  integrations: [
    Sentry.reactRouterV5BrowserTracingIntegration({ history }),
  ],
  tracesSampleRate: 1.0,
});

// 3. Wrap Route with HOC — enables parameterized transaction names
const SentryRoute = Sentry.withSentryRouting(Route);

// 4. Use SentryRoute everywhere instead of Route
//    ORDER MATTERS — most specific paths first (decreasing specificity)
function App() {
  return (
    <Router history={history}>
      <Switch>
        <SentryRoute path="/users/:userId/settings" component={UserSettingsPage} />
        <SentryRoute path="/users/:userId"          component={UserPage} />
        <SentryRoute path="/users"                  component={UsersPage} />
        <SentryRoute path="/"                       component={HomePage} />
      </Switch>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
```

#### Method 2 — Static Route Config (no HOC)

```typescript
import { matchPath } from "react-router-dom";
import { createBrowserHistory } from "history";
import * as Sentry from "@sentry/react";

const history = createBrowserHistory();

// Define all routes; most specific first
const routes = [
  { path: "/users/:userId/settings" },
  { path: "/users/:userId" },
  { path: "/users" },
  { path: "/dashboard/analytics" },
  { path: "/dashboard" },
  { path: "/" },
];

Sentry.init({
  dsn: "...",
  integrations: [
    Sentry.reactRouterV5BrowserTracingIntegration({
      history,
      routes,
      matchPath,   // from react-router-dom
    }),
  ],
  tracesSampleRate: 1.0,
});
```

**React Router v4:** use `Sentry.reactRouterV4BrowserTracingIntegration` — the API is identical to v5.

---

### TanStack Router

**Requires:** `@tanstack/react-router` ≥1.64.0

```typescript
// src/main.tsx
import * as Sentry from "@sentry/react";
import { createRouter, RouterProvider } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";   // generated by TanStack Router

// 1. Create the router first
const router = createRouter({
  routeTree,
  defaultPreload: "intent",
});

// 2. Init Sentry, passing the router instance
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  integrations: [
    Sentry.tanstackRouterBrowserTracingIntegration(router),
  ],
  tracesSampleRate: 1.0,
  tracePropagationTargets: ["localhost", /^https:\/\/api\.myapp\.com/],
});

// 3. Render
ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Sentry.ErrorBoundary fallback={<p>An error has occurred</p>}>
      <RouterProvider router={router} />
    </Sentry.ErrorBoundary>
  </StrictMode>
);
```

**Key difference vs React Router:** `tanstackRouterBrowserTracingIntegration` takes the router instance directly — no hooks (`useLocation`, `useNavigationType`) or helpers (`createRoutesFromChildren`, `matchRoutes`) are needed. TanStack Router exposes its route definitions directly to the SDK.

---

### How Route Names Are Parameterized

All router integrations extract parameterized route patterns instead of literal URLs:

| Actual URL | Transaction Name |
|-----------|-----------------|
| `/users/42` | `/users/:userId` |
| `/orders/abc-123/items` | `/orders/:orderId/items` |
| `/posts/2024/my-first-post` | `/posts/:year/:slug` |

This grouping is essential for meaningful performance data — without it, every user generates a unique transaction name and nothing can be aggregated.

---

### Router Integration Quick-Reference

```
Are you using React Router?
├─ v7 (react-router package) ──────► reactRouterV7BrowserTracingIntegration
│    ├─ createBrowserRouter? ──────► wrapCreateBrowserRouterV7(createBrowserRouter)
│    ├─ createMemoryRouter? ───────► wrapCreateMemoryRouterV7(createMemoryRouter)
│    ├─ <Routes> component? ───────► withSentryReactRouterV7Routing(Routes)
│    └─ useRoutes hook? ────────────► wrapUseRoutesV7(useRoutes)
│
├─ v6 (react-router-dom) ──────────► reactRouterV6BrowserTracingIntegration
│    ├─ createBrowserRouter? ──────► wrapCreateBrowserRouterV6(createBrowserRouter)
│    ├─ createMemoryRouter? ───────► wrapCreateMemoryRouterV6(createMemoryRouter) [≥8.50.0]
│    ├─ <Routes> component? ───────► withSentryReactRouterV6Routing(Routes)
│    └─ useRoutes hook? ────────────► wrapUseRoutesV6(useRoutes)
│
├─ v4/v5 ───────────────────────────► reactRouterV5BrowserTracingIntegration({ history })
│    ├─ with static routes array ──► add { routes, matchPath }
│    └─ without static routes ─────► withSentryRouting(Route) HOC
│
└─ No router / unsupported router ──► browserTracingIntegration()
     └─ custom router ──────────────► { instrumentPageLoad: false, instrumentNavigation: false }
                                       + startBrowserTracingPageLoadSpan
                                       + startBrowserTracingNavigationSpan

Are you using TanStack Router?
└─ Any version ≥1.64.0 ─────────────► tanstackRouterBrowserTracingIntegration(router)
```

---

## Custom Spans

### The Three Span APIs

#### `Sentry.startSpan()` — Active, Auto-Ending (Recommended)

Wraps a block of work. The span is active (collects children) and automatically ends when the callback returns or resolves:

```typescript
// Asynchronous
const data = await Sentry.startSpan(
  {
    name: "fetchUserProfile",
    op: "http.client",
    attributes: {
      "user.id": userId,
      "cache.hit": false,
    },
  },
  async () => {
    const res = await fetch(`/api/users/${userId}`);
    return res.json();
  }
);

// Synchronous
const result = Sentry.startSpan(
  { name: "computeRecommendations", op: "function" },
  () => expensiveComputation()
);

// Thrown errors are captured and the span is marked as error automatically
```

#### `Sentry.startSpanManual()` — Active, Manual End

Use when the span lifetime cannot be enclosed in a single callback — e.g., middleware that calls `next()`:

```typescript
function authMiddleware(req: Request, res: Response, next: NextFunction) {
  return Sentry.startSpanManual(
    { name: "auth.verify", op: "middleware" },
    (span) => {
      // span is active inside this callback only
      res.once("finish", () => {
        span.setStatus({ code: res.statusCode < 400 ? 1 : 2 });
        span.end();  // ← REQUIRED — will not end automatically
      });
      return next();
    }
  );
}
```

#### `Sentry.startInactiveSpan()` — Not Active, Manual End

For spans that cross event boundaries and should **not** automatically collect children as parent:

```typescript
let checkoutSpan: Sentry.Span | undefined;

// On flow start
document.getElementById("checkout-btn")!.addEventListener("click", () => {
  checkoutSpan = Sentry.startInactiveSpan({
    name: "checkout-flow",
    op: "ui.flow",
  });
});

// On flow end (later, in a different event handler)
document.getElementById("confirm-btn")!.addEventListener("click", () => {
  checkoutSpan?.setAttribute("payment.method", "stripe");
  checkoutSpan?.setStatus({ code: 1 });
  checkoutSpan?.end();  // ← REQUIRED
});
```

Explicit parent-child wiring with inactive spans:

```typescript
const parentSpan = Sentry.startInactiveSpan({ name: "checkout-flow" });

const childA = Sentry.startInactiveSpan({
  name: "validate-cart",
  op: "function",
  parentSpan,           // ← explicit parent reference
});
await validateCart();
childA.end();

const childB = Sentry.startInactiveSpan({
  name: "process-payment",
  op: "function",
  parentSpan,
});
await processPayment();
childB.end();

parentSpan.end();
```

---

### Span Options Reference

```typescript
interface StartSpanOptions {
  name: string;             // Required — label shown in the UI
  op?: string;              // Operation category (see table below)
  startTime?: number;       // Unix timestamp in seconds (can be float)
  attributes?: Record<string, string | number | boolean | string[] | number[] | boolean[]>;
  parentSpan?: Span;        // Override default parent (mainly for startInactiveSpan)
  onlyIfParent?: boolean;   // Drop this span if there is no currently active parent
  forceTransaction?: boolean; // Force span to appear as a root transaction in the UI
}
```

**Common `op` values:**

| `op` | When to use |
|------|-------------|
| `http.client` | Outgoing HTTP requests |
| `db.query` | Database queries |
| `ui.render` | React component render work |
| `ui.load` | Async data loading for a page/view |
| `ui.click` | User click event handling |
| `ui.flow` | Multi-step UI flow (checkout, wizard) |
| `function` | General JS function calls |
| `task` | Background/scheduled work |
| `cache.get` / `cache.set` | Cache reads/writes |
| `middleware` | Express/Koa/Fastify middleware |

---

### Enriching Spans

```typescript
const span = Sentry.getActiveSpan();

if (span) {
  // Single attribute
  span.setAttribute("db.table", "users");
  span.setAttribute("db.rows_affected", 5);

  // Multiple attributes at once
  span.setAttributes({
    "http.method": "POST",
    "http.status_code": 201,
    "user.tier": "premium",
  });

  // Status codes: 0=unset, 1=ok, 2=error
  span.setStatus({ code: 1 });
  span.setStatus({ code: 2, message: "Upstream timeout" });

  // HTTP-specific shorthand
  span.setHttpStatus(404);  // sets code=2, message="Not Found"
  span.setHttpStatus(200);  // sets code=1

  // Rename at runtime
  span.updateName("GET /users/:id");

  // End with explicit timestamp (seconds since epoch)
  span.end(Date.now() / 1000);
}
```

---

### Nesting Spans

Children nest automatically under the currently active span:

```typescript
await Sentry.startSpan({ name: "loadDashboard", op: "ui.load" }, async () => {
  // These are children of "loadDashboard"
  const [user, posts] = await Promise.all([
    Sentry.startSpan({ name: "fetchUser", op: "http.client" }, () =>
      fetch("/api/user").then(r => r.json())
    ),
    Sentry.startSpan({ name: "fetchPosts", op: "http.client" }, () =>
      fetch("/api/posts").then(r => r.json())
    ),
  ]);

  // Sequential child — still nested under "loadDashboard"
  await Sentry.startSpan({ name: "renderDashboard", op: "ui.render" }, async () => {
    await renderContent(user, posts);
  });
});
```

### `forceTransaction` — Standalone Root Span

Forces a span to appear as its own root transaction in the Sentry UI, independent of any active parent. Useful for background workers, Web Workers, or queue processors:

```typescript
Sentry.startSpan(
  { name: "processEmailQueue", op: "task", forceTransaction: true },
  async () => {
    const batch = await queue.take(50);
    await processBatch(batch);
  }
);
```

### Browser Flat Span Hierarchy

In browsers, all child spans are attached **flat** to the root span (not nested under intermediate parents). This prevents incorrect parent-child attribution in parallel async flows.

To opt into true nesting (use with care):

```typescript
Sentry.init({
  // ...
  parentSpanIsAlwaysRootSpan: false,
});
```

---

## Distributed Tracing

Distributed tracing connects a browser page load to all backend API calls it triggers, creating a single end-to-end waterfall.

### The Two Headers

| Header | Format | Purpose |
|--------|--------|---------|
| `sentry-trace` | `{traceId}-{spanId}-{sampled}` | Carries trace context |
| `baggage` | W3C Baggage format with `sentry-*` entries | Carries sampling decision + metadata |

Both headers are automatically injected into `fetch()` and `XMLHttpRequest` for URLs matching `tracePropagationTargets`.

### `tracePropagationTargets`

```typescript
Sentry.init({
  tracePropagationTargets: [
    // String = substring match against full URL
    "localhost",
    "api.myapp.com",

    // RegExp = tested against full URL
    /^https:\/\/api\.myapp\.com\//,
    /^\/api\//,  // same-origin relative paths

    // Multiple backends
    "https://auth.myapp.com",
    "https://payments.myapp.com",
  ],
});
```

**Defaults:** Same-origin requests get headers automatically. Cross-origin requests need explicit entries.

**Disable completely:**
```typescript
tracePropagationTargets: []  // no distributed tracing headers on any requests
```

### CORS Requirements

Your backend APIs **must** allowlist these headers:

```
Access-Control-Allow-Headers: sentry-trace, baggage
```

Express example:
```javascript
app.use((_req, res, next) => {
  res.setHeader(
    "Access-Control-Allow-Headers",
    "Content-Type, Authorization, sentry-trace, baggage"
  );
  next();
});
```

Without this, preflight requests fail and browsers suppress the headers.

### SSR / Meta Tag Approach

When your HTML is server-rendered, emit Sentry trace context into `<meta>` tags. `browserTracingIntegration` reads them on init and attaches the pageload span to the server's trace — the full request becomes one continuous trace.

Server (Node.js/Express):

```typescript
import * as Sentry from "@sentry/node";

app.get("/", (_req, res) => {
  const traceData = Sentry.getTraceData();
  // { "sentry-trace": "...", baggage: "..." }
  res.render("index", {
    sentryTrace: traceData["sentry-trace"],
    sentryBaggage: traceData["baggage"],
  });
});
```

HTML template (EJS/Handlebars/Jinja/etc.):

```html
<head>
  <meta name="sentry-trace" content="<%= sentryTrace %>" />
  <meta name="baggage"      content="<%= sentryBaggage %>" />
</head>
```

The browser SDK reads these tags automatically — no extra client config needed.

### Manual Propagation (WebSockets, Custom Channels)

For protocols that don't support HTTP headers:

```typescript
// Browser (sender)
const traceData = Sentry.getTraceData();

socket.send(JSON.stringify({
  type: "rpc.updateProfile",
  payload: { name: "Alice" },
  _sentry: {
    trace: traceData["sentry-trace"],
    baggage: traceData["baggage"],
  },
}));
```

```typescript
// Node.js server (receiver)
import * as Sentry from "@sentry/node";
import { propagation, context } from "@opentelemetry/api";

socket.on("message", (raw) => {
  const msg = JSON.parse(raw);
  const ctx = propagation.extract(context.active(), {
    "sentry-trace": msg._sentry.trace,
    "baggage": msg._sentry.baggage,
  });
  context.with(ctx, () => {
    Sentry.startSpan({ name: "ws.updateProfile" }, () => handleMessage(msg));
  });
});
```

### W3C `traceparent` Compatibility (SDK ≥10.10.0)

Add the W3C `traceparent` header alongside `sentry-trace` for OpenTelemetry-native backends:

```typescript
Sentry.init({
  propagateTraceparent: true,
});
```

---

## Sampling

### `tracesSampleRate` — Uniform Rate

```typescript
Sentry.init({
  tracesSampleRate: 1.0,   // 100% — dev / staging / low-traffic
  // tracesSampleRate: 0.2,  // 20% — light production
  // tracesSampleRate: 0.05, // 5%  — high-traffic production
  // tracesSampleRate: 0.01, // 1%  — very high-traffic production
});
```

### `tracesSampler` — Dynamic Per-Transaction

`tracesSampler` replaces `tracesSampleRate` (when both are set, `tracesSampler` wins):

```typescript
Sentry.init({
  tracesSampler: ({ name, attributes, inheritOrSampleWith }) => {
    // Drop health checks and internal routes
    if (["/health", "/ping", "/readyz"].some(p => name.includes(p))) return 0;

    // Always capture critical flows
    if (name.startsWith("/checkout") || name.startsWith("/payment")) return 1.0;

    // Sample admin routes at 50%
    if (name.startsWith("/admin")) return 0.5;

    // High-volume search at 5%
    if (name.includes("/search")) return 0.05;

    // For everything else: honor parent's decision, fall back to 10%
    return inheritOrSampleWith(0.1);
  },
});
```

### Full `samplingContext` Object

```typescript
interface SamplingContext {
  name: string;                     // Span/transaction name (e.g. "GET /users/:id")
  attributes?: SpanAttributes;      // Initial span attributes: op, url, http.method, etc.
  parentSampled?: boolean;          // Was the parent trace sampled? undefined = no parent
  parentSampleRate?: number;        // What rate was used upstream?
  inheritOrSampleWith: (fallbackRate: number) => number;
}
```

### `inheritOrSampleWith` — Why It Matters

Use `inheritOrSampleWith(fallback)` instead of checking `parentSampled` directly. It enables:
- **Deterministic sampling:** the same rate decision is applied throughout the trace chain
- **Accurate metric extrapolation:** Sentry's performance metrics scale correctly only when consistent sample rates flow through all services
- **Correct Sampled flag:** ensures the `sentry-sampled` value in downstream `baggage` matches the actual decision

### Returning Boolean vs Number

```typescript
tracesSampler: ({ name }) => {
  if (name === "/critical")  return true;   // equivalent to 1.0
  if (name === "/noisy")     return false;  // equivalent to 0
  return 0.2;
}
```

### Sampling Guidelines by Traffic Level

| Daily transactions | Recommended `tracesSampleRate` |
|--------------------|-------------------------------|
| < 10K | `1.0` — capture everything |
| 10K–100K | `0.2` — 20% |
| 100K–1M | `0.05` – `0.1` |
| > 1M | `0.01` – `0.02` with `tracesSampler` for priority routes at higher rates |

---

## Span Filtering

### `beforeSendTransaction` — Modify or Drop Whole Transactions

```typescript
Sentry.init({
  beforeSendTransaction(event) {
    // Drop internal/dev routes
    if (event.transaction?.startsWith("/__internal")) return null;

    // Scrub PII from transaction names
    if (event.transaction) {
      event.transaction = event.transaction
        .replace(/\/users\/[^/]+/, "/users/<redacted>");
    }

    // Add custom tags to every transaction
    event.tags = { ...event.tags, "app.build": BUILD_ID };

    return event;
  },
});
```

### `ignoreTransactions` — Declarative Transaction Filtering

```typescript
Sentry.init({
  ignoreTransactions: [
    "/health",            // string = substring match
    /^\/api\/internal/,   // regex = full URL test
    "/__webpack_hmr",
    /\.(png|jpg|svg|ico|woff2)$/,  // static assets
  ],
});
```

### `beforeSendSpan` — Modify Individual Spans

> `beforeSendSpan` **cannot drop spans** — it can only modify them. To suppress spans, use `ignoreSpans` (SDK ≥10.2.0).

```typescript
Sentry.init({
  beforeSendSpan(span) {
    // Redact token from span descriptions
    if (span.op === "http.client" && span.description?.includes("/token")) {
      span.description = span.description.replace(/token=[^&]+/, "token=REDACTED");
    }

    // Enrich all spans with deployment info
    span.data = {
      ...span.data,
      "deployment.region": import.meta.env.VITE_AWS_REGION ?? "unknown",
    };

    return span;  // must return span — never return null
  },
});
```

### `ignoreSpans` — Declarative Span Filtering (SDK ≥10.2.0)

```typescript
Sentry.init({
  ignoreSpans: [
    // String — matches against span name/description
    "font-load",

    // Regex against span name
    /^performance\.mark\./,

    // Object — filter by op only
    { op: "resource.script" },
    { op: "resource.img" },
    { op: "resource.css" },

    // Object — filter by name and op together
    { name: "beacon", op: "http.client" },

    // Object — name regex
    { name: /^(hotjar|analytics|gtag)/ },
  ],
});
```

> **Warning:** If the root span (the transaction itself) matches an `ignoreSpans` rule, the **entire local trace is dropped**.

---

## Custom Routing (Manual Spans)

For unsupported or custom routers, disable auto page spans and drive them yourself:

```typescript
import * as Sentry from "@sentry/react";
import { SEMANTIC_ATTRIBUTE_SENTRY_SOURCE } from "@sentry/react";

const client = Sentry.init({
  dsn: "...",
  integrations: [
    Sentry.browserTracingIntegration({
      instrumentPageLoad: false,   // handled manually
      instrumentNavigation: false, // handled manually
    }),
  ],
  tracesSampleRate: 1.0,
})!;

// Initial page load — name with URL until route is matched
let pageLoadSpan = Sentry.startBrowserTracingPageLoadSpan(client, {
  name: window.location.pathname,
  attributes: {
    [SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: "url",  // start with "url" source
  },
});

// Once the router resolves the matched route
myCustomRouter.on("routeResolved", (route) => {
  if (pageLoadSpan) {
    // Upgrade the pageload span's name to the parameterized pattern
    pageLoadSpan.updateName(route.pattern);          // e.g. "/users/:id"
    pageLoadSpan.setAttribute(
      SEMANTIC_ATTRIBUTE_SENTRY_SOURCE, "route"      // upgrade to "route" source
    );
    pageLoadSpan = undefined;
  } else {
    // Subsequent navigations
    Sentry.startBrowserTracingNavigationSpan(client, {
      op: "navigation",
      name: route.pattern,
      attributes: {
        [SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: "route",
      },
    });
  }
});
```

Both functions create **idle spans** — they close automatically after `idleTimeout`ms of no new child activity, matching the behavior of automatic pageload/navigation spans.

---

## Full Import Reference

```typescript
import * as Sentry from "@sentry/react";

// ── Integrations ──────────────────────────────────────────────────────────
Sentry.browserTracingIntegration(options)
Sentry.reactRouterV7BrowserTracingIntegration(options)
Sentry.reactRouterV6BrowserTracingIntegration(options)
Sentry.reactRouterV5BrowserTracingIntegration(options)
Sentry.reactRouterV4BrowserTracingIntegration(options)
Sentry.tanstackRouterBrowserTracingIntegration(router)

// ── Router Wrappers — v7 ─────────────────────────────────────────────────
Sentry.wrapCreateBrowserRouterV7(createBrowserRouter)
Sentry.wrapCreateMemoryRouterV7(createMemoryRouter)
Sentry.withSentryReactRouterV7Routing(Routes)
Sentry.wrapUseRoutesV7(useRoutes)

// ── Router Wrappers — v6 ─────────────────────────────────────────────────
Sentry.wrapCreateBrowserRouterV6(createBrowserRouter)
Sentry.wrapCreateMemoryRouterV6(createMemoryRouter)    // SDK ≥8.50.0
Sentry.withSentryReactRouterV6Routing(Routes)
Sentry.wrapUseRoutesV6(useRoutes)

// ── Router Wrappers — v5/v4 ──────────────────────────────────────────────
Sentry.withSentryRouting(Route)

// ── Spans ────────────────────────────────────────────────────────────────
Sentry.startSpan(options, callback)
Sentry.startSpanManual(options, callback)
Sentry.startInactiveSpan(options)
Sentry.getActiveSpan()

// ── Custom Browser Tracing ───────────────────────────────────────────────
Sentry.startBrowserTracingPageLoadSpan(client, options)
Sentry.startBrowserTracingNavigationSpan(client, options)

// ── Distributed Tracing ──────────────────────────────────────────────────
Sentry.getTraceData()
// Returns: { "sentry-trace": string, baggage: string }

// ── Constants ────────────────────────────────────────────────────────────
Sentry.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE  // "sentry.source"
Sentry.SEMANTIC_ATTRIBUTE_SENTRY_OP      // "sentry.op"
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transactions in Performance dashboard | Verify `tracesSampleRate` > 0; confirm `browserTracingIntegration()` (or router variant) is in `integrations` array |
| Transaction names show raw URLs (`/users/42`) instead of patterns | Add router integration matching your router version; ensure it's replacing, not supplementing, `browserTracingIntegration()` |
| Transaction named `<unknown>` | Router integration is missing or misconfigured; check `useEffect`, `useLocation`, `useNavigationType` are all passed correctly |
| Distributed trace not linking frontend → backend | Add backend URL to `tracePropagationTargets`; verify `Access-Control-Allow-Headers` includes `sentry-trace, baggage` |
| SSR page load not linked to server trace | Inject `<meta name="sentry-trace">` and `<meta name="baggage">` tags from `Sentry.getTraceData()` in server-rendered HTML |
| API requests missing `sentry-trace` header | Check CORS preflight — backend must allow `sentry-trace` and `baggage` headers |
| INP spans not appearing | In SDK 7.x, enable explicitly: `browserTracingIntegration({ enableInp: true })` |
| Web Vitals missing | Confirm `browserTracingIntegration()` is in client init; check browser support (INP requires Chromium 96+) |
| Spans missing after async gap | Browser uses flat hierarchy; use `startInactiveSpan` with explicit `parentSpan` to enforce parent-child across async boundaries |
| High transaction volume / cost | Use `tracesSampler` to return `0` for health checks and asset routes; lower default rate with `inheritOrSampleWith(0.05)` |
| `beforeSendSpan` returning `null` breaks the SDK | `beforeSendSpan` must always return the span — use `ignoreSpans` to drop spans declaratively |
| Lazy routes not tracked | Upgrade to SDK ≥10.39.0; add `enableAsyncRouteHandlers: true` and `lazyRouteManifest` with all route paths |
| TanStack Router transactions missing | Ensure router is created **before** `Sentry.init()` is called and the router instance is passed to the integration |
