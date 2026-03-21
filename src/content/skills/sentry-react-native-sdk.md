---
title: "Sentry React Native SDK"
description: "Full Sentry SDK setup for React Native and Expo. Use when asked to 'add Sentry to React Native', 'install @sentry/react-native', 'setup Sentry in Expo', or configure error monitoring, tracing, profiling, session replay, or logging for React Native..."
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "react", "native", "sdk"]
date: 2026-03-20
---

# Sentry React Native SDK

Opinionated wizard that scans your React Native or Expo project and guides you through complete Sentry setup — error monitoring, tracing, profiling, session replay, logging, and more.

## Invoke This Skill When

- User asks to "add Sentry to React Native" or "set up Sentry" in an RN or Expo app
- User wants error monitoring, tracing, profiling, session replay, or logging in React Native
- User mentions `@sentry/react-native`, mobile error tracking, or Sentry for Expo
- User wants to monitor native crashes, ANRs, or app hangs on iOS/Android

> **Note:** SDK versions and APIs below reflect current Sentry docs at time of writing (`@sentry/react-native` ≥6.0.0, minimum recommended ≥8.0.0).
> Always verify against [docs.sentry.io/platforms/react-native/](https://docs.sentry.io/platforms/react-native/) before implementing.

---

## Phase 1: Detect

Run these commands to understand the project before making any recommendations:

```bash
# Detect project type and existing Sentry
cat package.json | grep -E '"(react-native|expo|@expo|@sentry/react-native|sentry-expo)"'

# Distinguish Expo managed vs bare vs vanilla RN
ls app.json app.config.js app.config.ts 2>/dev/null
cat app.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('Expo managed' if 'expo' in d else 'Bare/Vanilla')" 2>/dev/null

# Check Expo SDK version (important: Expo SDK 50+ required for @sentry/react-native)
cat package.json | grep '"expo"'

# Detect navigation library
grep -E '"(@react-navigation/native|react-native-navigation)"' package.json

# Detect state management (Redux → breadcrumb integration available)
grep -E '"(redux|@reduxjs/toolkit|zustand|mobx)"' package.json

# Check for existing Sentry initialization
grep -r "Sentry.init" src/ app/ App.tsx App.js _layout.tsx 2>/dev/null | head -5

# Detect Hermes (affects source map handling)
cat android/app/build.gradle 2>/dev/null | grep -i hermes
cat ios/Podfile 2>/dev/null | grep -i hermes

# Detect Expo Router
ls app/_layout.tsx app/_layout.js 2>/dev/null

# Detect backend for cross-link
ls backend/ server/ api/ 2>/dev/null
find . -maxdepth 3 \( -name "go.mod" -o -name "requirements.txt" -o -name "Gemfile" -o -name "package.json" \) 2>/dev/null | grep -v node_modules | head -10
```

**What to determine:**

| Question | Impact |
|----------|--------|
| `expo` in `package.json`? | Expo path (config plugin + `getSentryExpoConfig`) vs bare/vanilla RN path |
| Expo SDK ≥50? | `@sentry/react-native` directly; older = `sentry-expo` (legacy, do not use) |
| `app.json` has `"expo"` key? | Managed Expo — wizard is simplest; config plugin handles all native config |
| `app/_layout.tsx` present? | Expo Router project — init goes in `_layout.tsx` |
| `@sentry/react-native` already in `package.json`? | Skip install, jump to feature config |
| `@react-navigation/native` present? | Recommend `reactNavigationIntegration` for screen tracking |
| `react-native-navigation` present? | Recommend `reactNativeNavigationIntegration` (Wix) |
| Backend directory detected? | Trigger Phase 4 cross-link |

---

## Phase 2: Recommend

Present a concrete recommendation based on what you found. Don't ask open-ended questions — lead with a proposal:

**Recommended (core coverage — always set up these):**
- ✅ **Error Monitoring** — captures JS exceptions, native crashes (iOS + Android), ANRs, and app hangs
- ✅ **Tracing** — mobile performance is critical; auto-instruments navigation, app start, network requests
- ✅ **Session Replay** — mobile replay captures screenshots and touch events for debugging user issues

**Optional (enhanced observability):**
- ⚡ **Profiling** — CPU profiling on iOS (JS profiling cross-platform); low overhead in production
- ⚡ **Logging** — structured logs via `Sentry.logger.*`; links to traces for full context
- ⚡ **User Feedback** — collect user-submitted bug reports directly from your app

**Recommendation logic:**

| Feature | Recommend when... |
|---------|------------------|
| Error Monitoring | **Always** — non-negotiable baseline for any mobile app |
| Tracing | **Always for mobile** — app start, navigation, and network latency matter |
| Session Replay | User-facing production app; debug user-reported issues visually |
| Profiling | Performance-sensitive screens, startup time concerns, or production perf investigations |
| Logging | App uses structured logging, or you want log-to-trace correlation in Sentry |
| User Feedback | Beta or customer-facing app where you want user-submitted bug reports |

Propose: *"For your [Expo managed / bare RN] app, I recommend setting up Error Monitoring + Tracing + Session Replay. Want me to also add Profiling and Logging?"*

---

## Phase 3: Guide

### Determine Your Setup Path

| Project type | Recommended setup | Complexity |
|-------------|------------------|------------|
| Expo managed (SDK 50+) | Wizard CLI or manual with config plugin | Low — wizard does everything |
| Expo bare (SDK 50+) | Wizard CLI recommended | Medium — handles iOS/Android config |
| Vanilla React Native (0.69+) | Wizard CLI recommended | Medium — handles Xcode + Gradle |
| Expo SDK <50 | Use `sentry-expo` (legacy) | See [legacy docs](https://docs.sentry.io/platforms/react-native/manual-setup/expo/) |

---

### Path A: Wizard CLI (Recommended for all project types)

Run the wizard — it walks you through login, org/project selection, and auth token setup interactively. It then handles installation, native config, source map upload, and initial `Sentry.init()`:

```bash
npx @sentry/wizard@latest -i reactNative
```

**What the wizard creates/modifies:**

| File | Action | Purpose |
|------|--------|---------|
| `package.json` | Installs `@sentry/react-native` | Core SDK |
| `metro.config.js` | Adds `@sentry/react-native/metro` serializer | Source map generation |
| `app.json` | Adds `@sentry/react-native/expo` plugin (Expo only) | Config plugin for native builds |
| `App.tsx` / `_layout.tsx` | Adds `Sentry.init()` and `Sentry.wrap()` | SDK initialization |
| `ios/sentry.properties` | Stores org/project/token | iOS source map + dSYM upload |
| `android/sentry.properties` | Stores org/project/token | Android source map upload |
| `android/app/build.gradle` | Adds Sentry Gradle plugin | Android source maps + proguard |
| `ios/[AppName].xcodeproj` | Wraps "Bundle RN" build phase + adds dSYM upload | iOS symbol upload |
| `.env.local` | `SENTRY_AUTH_TOKEN` | Auth token (add to `.gitignore`) |

After the wizard runs, skip to [Verification](#verification).

---

### Path B: Manual — Expo Managed (SDK 50+)

**Step 1 — Install**

```bash
npx expo install @sentry/react-native
```

**Step 2 — `metro.config.js`**

```javascript
const { getSentryExpoConfig } = require("@sentry/react-native/metro");
const config = getSentryExpoConfig(__dirname);
module.exports = config;
```

If `metro.config.js` doesn't exist yet:
```bash
npx expo customize metro.config.js
# Then replace contents with the above
```

**Step 3 — `app.json` — Add Expo config plugin**

```json
{
  "expo": {
    "plugins": [
      [
        "@sentry/react-native/expo",
        {
          "url": "https://sentry.io/",
          "project": "YOUR_PROJECT_SLUG",
          "organization": "YOUR_ORG_SLUG"
        }
      ]
    ]
  }
}
```

> **Note:** Set `SENTRY_AUTH_TOKEN` as an environment variable for native builds — never commit it to version control.

**Step 4 — Initialize Sentry**

For **Expo Router** (`app/_layout.tsx`):

```typescript
import { Stack, useNavigationContainerRef } from "expo-router";
import { isRunningInExpoGo } from "expo";
import * as Sentry from "@sentry/react-native";
import React from "react";

const navigationIntegration = Sentry.reactNavigationIntegration({
  enableTimeToInitialDisplay: !isRunningInExpoGo(), // disabled in Expo Go
});

Sentry.init({
  dsn: process.env.EXPO_PUBLIC_SENTRY_DSN ?? "YOUR_SENTRY_DSN",
  sendDefaultPii: true,

  // Tracing
  tracesSampleRate: 1.0, // lower to 0.1–0.2 in production

  // Profiling
  profilesSampleRate: 1.0,

  // Session Replay
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,

  // Logging (SDK ≥7.0.0)
  enableLogs: true,

  // Navigation
  integrations: [
    navigationIntegration,
    Sentry.mobileReplayIntegration(),
  ],

  enableNativeFramesTracking: !isRunningInExpoGo(), // slow/frozen frames

  environment: __DEV__ ? "development" : "production",
});

function RootLayout() {
  const ref = useNavigationContainerRef();

  React.useEffect(() => {
    if (ref) {
      navigationIntegration.registerNavigationContainer(ref);
    }
  }, [ref]);

  return <Stack />;
}

export default Sentry.wrap(RootLayout);
```

For **standard Expo** (`App.tsx`):

```typescript
import { NavigationContainer, createNavigationContainerRef } from "@react-navigation/native";
import { isRunningInExpoGo } from "expo";
import * as Sentry from "@sentry/react-native";

const navigationIntegration = Sentry.reactNavigationIntegration({
  enableTimeToInitialDisplay: !isRunningInExpoGo(),
});

Sentry.init({
  dsn: process.env.EXPO_PUBLIC_SENTRY_DSN ?? "YOUR_SENTRY_DSN",
  sendDefaultPii: true,
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  enableLogs: true,
  integrations: [
    navigationIntegration,
    Sentry.mobileReplayIntegration(),
  ],
  enableNativeFramesTracking: !isRunningInExpoGo(),
  environment: __DEV__ ? "development" : "production",
});

const navigationRef = createNavigationContainerRef();

function App() {
  return (
    <NavigationContainer
      ref={navigationRef}
      onReady={() => {
        navigationIntegration.registerNavigationContainer(navigationRef);
      }}
    >
      {/* your navigation here */}
    </NavigationContainer>
  );
}

export default Sentry.wrap(App);
```

---

### Path C: Manual — Bare React Native (0.69+)

**Step 1 — Install**

```bash
npm install @sentry/react-native --save
cd ios && pod install
```

**Step 2 — `metro.config.js`**

```javascript
const { getDefaultConfig } = require("@react-native/metro-config");
const { withSentryConfig } = require("@sentry/react-native/metro");

const config = getDefaultConfig(__dirname);
module.exports = withSentryConfig(config);
```

**Step 3 — iOS: Modify Xcode build phase**

Open `ios/[AppName].xcodeproj` in Xcode. Find the **"Bundle React Native code and images"** build phase and replace the script content with:

```bash
# RN 0.81.1+
set -e
WITH_ENVIRONMENT="../node_modules/react-native/scripts/xcode/with-environment.sh"
SENTRY_XCODE="../node_modules/@sentry/react-native/scripts/sentry-xcode.sh"
/bin/sh -c "$WITH_ENVIRONMENT $SENTRY_XCODE"
```

**Step 4 — iOS: Add "Upload Debug Symbols to Sentry" build phase**

Add a new **Run Script** build phase in Xcode (after the bundle phase):

```bash
/bin/sh ../node_modules/@sentry/react-native/scripts/sentry-xcode-debug-files.sh
```

**Step 5 — iOS: `ios/sentry.properties`**

```properties
defaults.url=https://sentry.io/
defaults.org=YOUR_ORG_SLUG
defaults.project=YOUR_PROJECT_SLUG
auth.token=YOUR_ORG_AUTH_TOKEN
```

**Step 6 — Android: `android/app/build.gradle`**

Add before the `android {}` block:

```groovy
apply from: "../../node_modules/@sentry/react-native/sentry.gradle"
```

**Step 7 — Android: `android/sentry.properties`**

```properties
defaults.url=https://sentry.io/
defaults.org=YOUR_ORG_SLUG
defaults.project=YOUR_PROJECT_SLUG
auth.token=YOUR_ORG_AUTH_TOKEN
```

**Step 8 — Initialize Sentry (`App.tsx` or entry point)**

```typescript
import { NavigationContainer, createNavigationContainerRef } from "@react-navigation/native";
import * as Sentry from "@sentry/react-native";

const navigationIntegration = Sentry.reactNavigationIntegration({
  enableTimeToInitialDisplay: true,
});

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  sendDefaultPii: true,
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  enableLogs: true,
  integrations: [
    navigationIntegration,
    Sentry.mobileReplayIntegration(),
  ],
  enableNativeFramesTracking: true,
  environment: __DEV__ ? "development" : "production",
});

const navigationRef = createNavigationContainerRef();

function App() {
  return (
    <NavigationContainer
      ref={navigationRef}
      onReady={() => {
        navigationIntegration.registerNavigationContainer(navigationRef);
      }}
    >
      {/* your navigation here */}
    </NavigationContainer>
  );
}

export default Sentry.wrap(App);
```

---

### Quick Reference: Full-Featured `Sentry.init()`

This is the recommended starting configuration with all features enabled:

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_SENTRY_DSN",
  sendDefaultPii: true,

  // Tracing — lower to 0.1–0.2 in high-traffic production
  tracesSampleRate: 1.0,

  // Profiling — runs on a subset of traced transactions
  profilesSampleRate: 1.0,

  // Session Replay — always capture on error, sample 10% of all sessions
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,

  // Logging — enable Sentry.logger.* API
  enableLogs: true,

  // Integrations — mobile replay is opt-in
  integrations: [
    Sentry.mobileReplayIntegration({
      maskAllText: true,   // masks text by default for privacy
      maskAllImages: true,
    }),
  ],

  // Native frames tracking (disable in Expo Go)
  enableNativeFramesTracking: true,

  // Environment
  environment: __DEV__ ? "development" : "production",

  // Release — set from CI or build system
  // release: "my-app@1.0.0+1",
  // dist: "1",
});

// REQUIRED: Wrap root component to capture React render errors
export default Sentry.wrap(App);
```

---

### Navigation Setup — React Navigation (v5+)

```typescript
import { reactNavigationIntegration } from "@sentry/react-native";
import { NavigationContainer, createNavigationContainerRef } from "@react-navigation/native";

const navigationIntegration = reactNavigationIntegration({
  enableTimeToInitialDisplay: true,   // track TTID per screen
  routeChangeTimeoutMs: 1_000,        // max wait for route change to settle
  ignoreEmptyBackNavigationTransactions: true,
});

// Add to Sentry.init integrations array
Sentry.init({
  integrations: [navigationIntegration],
  // ...
});

// In your component:
const navigationRef = createNavigationContainerRef();

<NavigationContainer
  ref={navigationRef}
  onReady={() => {
    navigationIntegration.registerNavigationContainer(navigationRef);
  }}
>
```

### Navigation Setup — Wix React Native Navigation

```typescript
import * as Sentry from "@sentry/react-native";
import { Navigation } from "react-native-navigation";

Sentry.init({
  integrations: [Sentry.reactNativeNavigationIntegration({ navigation: Navigation })],
  // ...
});
```

---

### Wrap Your Root Component

Always wrap your root component — this enables React error boundaries and ensures crashes at the component tree level are captured:

```typescript
export default Sentry.wrap(App);
```

---

### For Each Agreed Feature

Walk through features one at a time. Load the reference file for each, follow its steps, then verify before moving on:

| Feature | Reference | Load when... |
|---------|-----------|-------------|
| Error Monitoring | `${SKILL_ROOT}/references/error-monitoring.md` | Always (baseline) |
| Tracing & Performance | `${SKILL_ROOT}/references/tracing.md` | Always for mobile (app start, navigation, network) |
| Profiling | `${SKILL_ROOT}/references/profiling.md` | Performance-sensitive production apps |
| Session Replay | `${SKILL_ROOT}/references/session-replay.md` | User-facing apps |
| Logging | `${SKILL_ROOT}/references/logging.md` | Structured logging / log-to-trace correlation |
| User Feedback | `${SKILL_ROOT}/references/user-feedback.md` | Collecting user-submitted reports |

For each feature: `Read ${SKILL_ROOT}/references/<feature>.md`, follow steps exactly, verify it works.

---

## Configuration Reference

### Core `Sentry.init()` Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `dsn` | `string` | — | **Required.** Project DSN; SDK disabled if empty. Env: `SENTRY_DSN` |
| `environment` | `string` | — | e.g., `"production"`, `"staging"`. Env: `SENTRY_ENVIRONMENT` |
| `release` | `string` | — | App version, e.g., `"my-app@1.0.0+42"`. Env: `SENTRY_RELEASE` |
| `dist` | `string` | — | Build number / variant identifier (max 64 chars) |
| `sendDefaultPii` | `boolean` | `false` | Include PII: IP address, cookies, user data |
| `sampleRate` | `number` | `1.0` | Error event sampling (0.0–1.0) |
| `maxBreadcrumbs` | `number` | `100` | Max breadcrumbs per event |
| `attachStacktrace` | `boolean` | `true` | Auto-attach stack traces to messages |
| `attachScreenshot` | `boolean` | `false` | Capture screenshot on error (SDK ≥4.11.0) |
| `attachViewHierarchy` | `boolean` | `false` | Attach JSON view hierarchy as attachment |
| `debug` | `boolean` | `false` | Verbose SDK output. **Never use in production** |
| `enabled` | `boolean` | `true` | Disable SDK entirely (e.g., for testing) |
| `ignoreErrors` | `string[] \| RegExp[]` | — | Drop errors matching these patterns |
| `ignoreTransactions` | `string[] \| RegExp[]` | — | Drop transactions matching these patterns |
| `maxCacheItems` | `number` | `30` | Max offline-cached envelopes |
| `defaultIntegrations` | `boolean` | `true` | Set `false` to disable all default integrations |
| `integrations` | `array \| function` | — | Add or filter integrations |

### Tracing Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `tracesSampleRate` | `number` | `0` | Transaction sample rate (0–1). Use `1.0` in dev |
| `tracesSampler` | `function` | — | Per-transaction sampling; overrides `tracesSampleRate` |
| `tracePropagationTargets` | `(string \| RegExp)[]` | `[/.*/]` | Which API URLs receive distributed tracing headers |
| `profilesSampleRate` | `number` | `0` | Profiling sample rate (applied to traced transactions) |

### Native / Mobile Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `enableNative` | `boolean` | `true` | Set `false` for JS-only (no native SDK) |
| `enableNativeCrashHandling` | `boolean` | `true` | Capture native hard crashes (iOS/Android) |
| `enableNativeFramesTracking` | `boolean` | — | Slow/frozen frames tracking. **Disable in Expo Go** |
| `enableWatchdogTerminationTracking` | `boolean` | `true` | OOM kill detection (iOS) |
| `enableAppHangTracking` | `boolean` | `true` | App hang detection (iOS, tvOS, macOS) |
| `appHangTimeoutInterval` | `number` | `2` | Seconds before classifying as app hang (iOS) |
| `enableAutoPerformanceTracing` | `boolean` | `true` | Auto performance instrumentation |
| `enableNdkScopeSync` | `boolean` | `true` | Java→NDK scope sync (Android) |
| `attachThreads` | `boolean` | `false` | Auto-attach all threads on crash (Android) |
| `autoInitializeNativeSdk` | `boolean` | `true` | Set `false` for manual native init |
| `onReady` | `function` | — | Callback after native SDKs initialize |

### Session & Release Health Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `autoSessionTracking` | `boolean` | `true` | Session tracking (crash-free users/sessions) |
| `sessionTrackingIntervalMillis` | `number` | `30000` | ms of background before session ends |

### Replay Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `replaysSessionSampleRate` | `number` | `0` | Fraction of all sessions recorded |
| `replaysOnErrorSampleRate` | `number` | `0` | Fraction of error sessions recorded |

### Logging Options (SDK ≥7.0.0)

| Option | Type | Purpose |
|--------|------|---------|
| `enableLogs` | `boolean` | Enable `Sentry.logger.*` API |
| `beforeSendLog` | `function` | Filter/modify logs before sending |
| `logsOrigin` | `'native' \| 'js' \| 'all'` | Filter log source (SDK ≥7.7.0) |

### Hook Options

| Option | Type | Purpose |
|--------|------|---------|
| `beforeSend` | `(event, hint) => event \| null` | Modify/drop JS error events. ⚠️ Does NOT apply to native crashes |
| `beforeSendTransaction` | `(event) => event \| null` | Modify/drop transaction events |
| `beforeBreadcrumb` | `(breadcrumb, hint) => breadcrumb \| null` | Process breadcrumbs before storage |

---

## Environment Variables

| Variable | Purpose | Notes |
|----------|---------|-------|
| `SENTRY_DSN` | Data Source Name | Falls back from `dsn` option |
| `SENTRY_AUTH_TOKEN` | Upload source maps and dSYMs | **Never commit — use CI secrets** |
| `SENTRY_ORG` | Organization slug | Used by wizard and build plugins |
| `SENTRY_PROJECT` | Project slug | Used by wizard and build plugins |
| `SENTRY_RELEASE` | Release identifier | Falls back from `release` option |
| `SENTRY_ENVIRONMENT` | Environment name | Falls back from `environment` option |
| `SENTRY_DISABLE_AUTO_UPLOAD` | Skip source map upload | Set `true` during local builds |
| `EXPO_PUBLIC_SENTRY_DSN` | Expo public env var for DSN | Safe to embed in client bundle |

---

## Source Maps & Debug Symbols

Source maps and debug symbols are what transform minified stack traces into readable ones. When set up correctly, Sentry shows you the exact line of your source code that threw.

### How Uploads Work

| Platform | What's uploaded | When |
|----------|----------------|------|
| **iOS** (JS) | Source maps (`.map` files) | During Xcode build |
| **iOS** (Native) | dSYM bundles | During Xcode archive / Xcode Cloud |
| **Android** (JS) | Source maps + Hermes `.hbc.map` | During Gradle build |
| **Android** (Native) | Proguard mapping + NDK `.so` files | During Gradle build |

### Expo: Automatic Upload

The `@sentry/react-native/expo` config plugin automatically sets up upload hooks for native builds. Source maps are uploaded during `eas build` and `expo run:ios/android` (release).

```bash
SENTRY_AUTH_TOKEN=sntrys_... npx expo run:ios --configuration Release
```

### Manual Upload (bare RN)

If you need to manually upload source maps:

```bash
npx sentry-cli sourcemaps upload \
  --org YOUR_ORG \
  --project YOUR_PROJECT \
  --release "my-app@1.0.0+1" \
  ./dist
```

---

## Default Integrations (Auto-Enabled)

These integrations are enabled automatically — no config needed:

| Integration | What it does |
|-------------|-------------|
| `ReactNativeErrorHandlers` | Catches unhandled JS exceptions and promise rejections |
| `Release` | Attaches release/dist to all events |
| `Breadcrumbs` | Records console logs, HTTP requests, user gestures as breadcrumbs |
| `HttpClient` | Adds HTTP request/response breadcrumbs |
| `DeviceContext` | Attaches device/OS/battery info to events |
| `AppContext` | Attaches app version, bundle ID, and memory info |
| `CultureContext` | Attaches locale and timezone |
| `Screenshot` | Captures screenshot on error (when `attachScreenshot: true`) |
| `ViewHierarchy` | Attaches view hierarchy (when `attachViewHierarchy: true`) |
| `NativeLinkedErrors` | Links JS errors to their native crash counterparts |

### Opt-In Integrations

| Integration | How to enable |
|-------------|--------------|
| `mobileReplayIntegration()` | Add to `integrations` array |
| `reactNavigationIntegration()` | Add to `integrations` array |
| `reactNativeNavigationIntegration()` | Add to `integrations` array (Wix only) |
| `feedbackIntegration()` | Add to `integrations` array (user feedback widget) |

---

## Expo Config Plugin Reference

Configure the plugin in `app.json` or `app.config.js`:

```json
{
  "expo": {
    "plugins": [
      [
        "@sentry/react-native/expo",
        {
          "url": "https://sentry.io/",
          "project": "my-project",
          "organization": "my-org",
          "note": "Set SENTRY_AUTH_TOKEN env var for native builds"
        }
      ]
    ]
  }
}
```

Or in `app.config.js` (allows env var interpolation):

```javascript
export default {
  expo: {
    plugins: [
      [
        "@sentry/react-native/expo",
        {
          url: "https://sentry.io/",
          project: process.env.SENTRY_PROJECT,
          organization: process.env.SENTRY_ORG,
        },
      ],
    ],
  },
};
```

---

## Production Settings

Lower sample rates and harden config before shipping to production:

```typescript
Sentry.init({
  dsn: process.env.EXPO_PUBLIC_SENTRY_DSN,
  environment: __DEV__ ? "development" : "production",

  // Trace 10–20% of transactions in high-traffic production
  tracesSampleRate: __DEV__ ? 1.0 : 0.1,

  // Profile 100% of traced transactions (profiling is always a subset of tracing)
  profilesSampleRate: 1.0,

  // Replay all error sessions, sample 5% of normal sessions
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: __DEV__ ? 1.0 : 0.05,

  // Set release and dist for accurate source map lookup
  release: "my-app@" + Application.nativeApplicationVersion,
  dist: String(Application.nativeBuildVersion),

  // Disable debug logging in production
  debug: __DEV__,
});
```

---

## Verification

After setup, test that Sentry is receiving events:

```typescript
// Quick test — throws and Sentry.wrap(App) catches it
<Button
  title="Test Sentry Error"
  onPress={() => {
    throw new Error("My first Sentry error!");
  }}
/>

// Or capture manually
<Button
  title="Test Sentry Message"
  onPress={() => {
    Sentry.captureMessage("Sentry test message", "info");
  }}
/>
```

**Check the Sentry dashboard:**
- **Issues** → your test error should appear within seconds
- **Traces** → look for a "main" transaction with child spans
- **Replays** → session recording visible after app interaction (native build only — not Expo Go)
- **Logs** → structured log entries if `enableLogs: true`

> ⚠️ **Expo Go limitation:** Native crashes, session replay, slow/frozen frames, TTID, and TTFD only work in native builds (`eas build` or `expo run`). Expo Go runs in a JS-only mode. Set `enableNativeFramesTracking: !isRunningInExpoGo()` to avoid warnings.

If nothing appears:
1. Set `debug: true` — SDK logs to Metro console
2. Verify DSN is correct and the Sentry project exists
3. Ensure `Sentry.wrap(App)` is applied to the root component
4. For native crashes, build a release build (crashes in debug mode may not forward)

---

## Phase 4: Cross-Link

After completing React Native setup, check for a backend or web frontend missing Sentry coverage:

```bash
# Adjacent backend directories
ls ../backend ../server ../api 2>/dev/null
cat ../go.mod 2>/dev/null | head -3
cat ../requirements.txt ../pyproject.toml 2>/dev/null | head -3
cat ../Gemfile 2>/dev/null | head -3
ls ../backend/package.json ../server/package.json 2>/dev/null

# Web frontend in same or sibling repo
ls ../web ../frontend ../dashboard 2>/dev/null
cat ../web/package.json ../frontend/package.json 2>/dev/null | grep -E '"react"|"svelte"|"next"'

# Check for OpenTelemetry (for distributed tracing interop)
grep -r "opentelemetry" ../backend/go.mod ../server/requirements.txt 2>/dev/null
```

If a backend or web frontend exists without Sentry, suggest the matching skill:

| Detected | Suggest skill |
|----------|--------------|
| Go backend (`go.mod`) | `sentry-go-sdk` |
| Python backend (`requirements.txt`, `pyproject.toml`) | `sentry-python-sdk` |
| Ruby backend (`Gemfile`) | `sentry-ruby-sdk` |
| Node.js backend (Express, Fastify, etc.) | `@sentry/node` — see [docs.sentry.io/platforms/javascript/guides/express/](https://docs.sentry.io/platforms/javascript/guides/express/) |
| React / Next.js web | `sentry-react-sdk` |
| Svelte / SvelteKit web | `sentry-svelte-sdk` |

**Distributed tracing setup** — if the backend skill is added, configure `tracePropagationTargets` in React Native to propagate trace context to your API:

```typescript
Sentry.init({
  tracePropagationTargets: [
    "localhost",
    /^https:\/\/api\.yourapp\.com/,
  ],
  // ...
});
```

This links mobile transactions to backend traces in the Sentry waterfall view.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing in Sentry | Set `debug: true`, check Metro/Xcode console for SDK errors; verify DSN is correct |
| `pod install` fails | Run `cd ios && pod install --repo-update`; check CocoaPods version |
| iOS build fails with Sentry script | Verify the "Bundle React Native code and images" script was replaced (not appended to) |
| Android build fails after adding `sentry.gradle` | Ensure `apply from` line is before the `android {}` block in `build.gradle` |
| Android Gradle 8+ compatibility issue | Use `sentry-android-gradle-plugin` ≥4.0.0; check `sentry.gradle` version in your SDK |
| Source maps not uploading | Verify `sentry.properties` has a valid `auth.token`; check build logs for `sentry-cli` output |
| Source maps not resolving in Sentry | Confirm `release` and `dist` in `Sentry.init()` match the uploaded bundle metadata |
| Hermes source maps not working | Hermes emits `.hbc.map` — the Gradle plugin handles this automatically; verify `sentry.gradle` is applied |
| Session replay not recording | Must use a native build (not Expo Go); confirm `mobileReplayIntegration()` is in `integrations` |
| Replay shows blank/black screens | Check that `maskAllText`/`maskAllImages` settings match your privacy requirements |
| Slow/frozen frames not tracked | Set `enableNativeFramesTracking: true` and confirm you're on a native build (not Expo Go) |
| TTID / TTFD not appearing | Requires `enableTimeToInitialDisplay: true` in `reactNavigationIntegration()` on a native build |
| App crashes on startup after adding Sentry | Likely a native initialization error — check Xcode/Logcat logs; try `enableNative: false` to isolate |
| Expo SDK 49 or older | Use `sentry-expo` (legacy package); `@sentry/react-native` requires Expo SDK 50+ |
| `isRunningInExpoGo` import error | Import from `expo` package: `import { isRunningInExpoGo } from "expo"` |
| Node not found during Xcode build | Add `export NODE_BINARY=$(which node)` to the Xcode build phase, or symlink: `ln -s $(which node) /usr/local/bin/node` |
| Expo Go warning about native features | Use `isRunningInExpoGo()` guard: `enableNativeFramesTracking: !isRunningInExpoGo()` |
| `beforeSend` not firing for native crashes | Expected — `beforeSend` only intercepts JS-layer errors; native crashes bypass it |
| Android 15+ (16KB page size) crash | Upgrade to `@sentry/react-native` ≥6.3.0 |
| Too many transactions in dashboard | Lower `tracesSampleRate` to `0.1` or use `tracesSampler` to drop health checks |
| `SENTRY_AUTH_TOKEN` exposed in app bundle | `SENTRY_AUTH_TOKEN` is for build-time upload only — never pass it to `Sentry.init()` |
| EAS Build: Sentry auth token missing | Set `SENTRY_AUTH_TOKEN` as an EAS secret: `eas secret:create --name SENTRY_AUTH_TOKEN` |

---

## Reference: Error Monitoring

# Error Monitoring & Crash Reporting — Sentry React Native SDK

> **Minimum SDK:** `@sentry/react-native` ≥ 6.0.0 (≥ 8.0.0 recommended)
> **Native SDKs:** `sentry-cocoa` (iOS/tvOS/macOS) · `sentry-android` (Java + NDK)
> **React Native:** 0.71+ required for Fabric renderer support

React Native is unique: errors can originate from three different layers — the **JavaScript runtime**, **native iOS** (ObjC/Swift, Mach exceptions), or **native Android** (Java, JNI/C++ via NDK). The Sentry RN SDK bridges all three.

---

## Table of Contents

1. [Core Capture APIs](#1-core-capture-apis)
2. [Native Crash Handling — iOS & Android](#2-native-crash-handling--ios--android)
3. [ANR / App Hang Detection](#3-anr--app-hang-detection)
4. [Unhandled Promise Rejections](#4-unhandled-promise-rejections)
5. [Sentry.wrap(App) — Top-Level Error Boundary](#5-sentrywrapapp--top-level-error-boundary)
6. [ErrorBoundary Component](#6-errorboundary-component)
7. [Scope Management](#7-scope-management)
8. [Context Enrichment — Tags, User, Extra, Contexts](#8-context-enrichment--tags-user-extra-contexts)
9. [Breadcrumbs — Automatic & Manual](#9-breadcrumbs--automatic--manual)
10. [beforeSend / beforeSendTransaction Hooks](#10-beforesend--beforesendtransaction-hooks)
11. [Fingerprinting & Grouping](#11-fingerprinting--grouping)
12. [Event Processors](#12-event-processors)
13. [Attachments — Screenshots & View Hierarchy](#13-attachments--screenshots--view-hierarchy)
14. [Redux Integration](#14-redux-integration)
15. [Device & App Context](#15-device--app-context)
16. [Release Health & Sessions](#16-release-health--sessions)
17. [Offline Event Caching](#17-offline-event-caching)
18. [Default Integrations](#18-default-integrations)
19. [Full init() Options Reference](#19-full-init-options-reference)
20. [Quick Reference Cheatsheet](#20-quick-reference-cheatsheet)
21. [Troubleshooting](#21-troubleshooting)

---

## 1. Core Capture APIs

Three fundamental data concepts:
- **Event** — a single submission to Sentry (exception, message, or raw event)
- **Issue** — a group of similar events clustered by Sentry
- **Capturing** — the act of reporting an event

### `Sentry.captureException(error, context?)`

Captures any thrown `Error` (or non-Error value) and sends it to Sentry.

```typescript
import * as Sentry from "@sentry/react-native";

// Basic usage
try {
  aFunctionThatMightFail();
} catch (err) {
  Sentry.captureException(err);
}

// With inline context (plain object)
Sentry.captureException(new Error("something went wrong"), {
  tags: { section: "checkout" },
  user: { email: "user@example.com" },
  extra: { orderId: "abc-123" },
  level: "warning",
  fingerprint: ["{{ default }}", "checkout-error"],
});

// With a scope callback — clones scope for this capture only
Sentry.captureException(new Error("something went wrong"), (scope) => {
  scope.setTag("section", "articles");
  scope.setLevel("warning");
  return scope;
});

// New Scope instance — merges with global scope
const scope = new Sentry.Scope();
scope.setTag("section", "articles");
Sentry.captureException(new Error("something went wrong"), scope);

// Isolate entirely — return the scope from a function to ignore global attrs
Sentry.captureException(new Error("clean slate"), () => scope);
```

### `Sentry.captureMessage(message, level?)`

Sends a textual message. Useful for non-exception events or informational milestones.

```typescript
// Default level is "info"
Sentry.captureMessage("Something noteworthy happened");

// Explicit severity level
// "fatal" | "error" | "warning" | "log" | "info" | "debug"
Sentry.captureMessage("Payment declined", "warning");
Sentry.captureMessage("Critical system failure", "fatal");
Sentry.captureMessage("Debug checkpoint reached", "debug");
```

### `Sentry.captureEvent(event)`

Low-level method to send a fully constructed Sentry event object. Used for advanced cases where you build the event manually.

```typescript
Sentry.captureEvent({
  message: "Manual event",
  level: "error",
  tags: { custom_tag: "value" },
  extra: { arbitrary_data: true },
  fingerprint: ["my-custom-fingerprint"],
  timestamp: Date.now() / 1000,
});
```

### Error Levels

| Level | Use Case |
|-------|----------|
| `fatal` | App crash, total loss of functionality |
| `error` | Feature broken, user action failed |
| `warning` | Degraded state, non-critical failure |
| `info` | Informational, noteworthy events |
| `log` | Low-priority operational logs |
| `debug` | Development diagnostics |

---

## 2. Native Crash Handling — iOS & Android

The React Native SDK delegates to two native SDKs for platform-level crash capture:
- **iOS/tvOS/macOS** — `sentry-cocoa`
- **Android** — `sentry-android` (Java/Kotlin + NDK for C/C++)

### How Native Crash Capture Works

Native crashes (segfaults, SIGSEGV, unhandled C++ exceptions, OOM kills) are captured **entirely at the OS level** — not in JavaScript. The crash handler is registered during native SDK initialization. Crash reports are:

1. Persisted to disk in binary envelope format at crash time
2. **Not sent at crash time** — queued and sent on the **next app launch**

```
iOS:     [crash] → written to disk by sentry-cocoa
                 → [next launch] → sentry-cocoa reads and transmits

Android: [crash] → written to disk by sentry-android
                 → [next app restart] → sentry-android reads and transmits
```

### Native Configuration Options

```typescript
Sentry.init({
  dsn: "https://examplePublicKey@o0.ingest.sentry.io/0",

  // Disable all native SDK functionality (JS layer only)
  enableNative: false,

  // Prevent native layer from capturing hard crashes
  enableNativeCrashHandling: false,

  // Manually initialize native SDKs yourself (advanced)
  autoInitializeNativeSdk: false,

  // Sync Android Java scope data to NDK layer (for C/C++ crash context)
  enableNdkScopeSync: true,

  // Android 12+: use ApplicationExitInfo for enhanced tombstone reports
  enableTombstone: true,

  // Attach all thread states to Android events (has a performance impact)
  attachThreads: false,

  // Called after native SDKs have finished initializing
  onReady: () => {
    console.log("Sentry native SDKs initialized");
  },
});
```

### Offline Caching Behavior

| Platform | Offline Behavior |
|----------|-----------------|
| **Android** | Events cached on device; transmitted on **app restart** |
| **iOS** | Events cached on device; transmitted when the **next event fires** |

### Linked Errors (Chained `.cause`)

The `NativeLinkedErrors` integration (enabled by default) reads the `.cause` property on errors recursively, linking the error chain up to **5 levels deep**:

```typescript
try {
  await fetchMovieReviews(movie);
} catch (originalError) {
  const wrapperError = new Error(`Failed to fetch reviews for: ${movie}`);
  wrapperError.cause = originalError; // SDK reads this chain
  Sentry.captureException(wrapperError);
}
```

---

## 3. ANR / App Hang Detection

### Android — Application Not Responding (ANR)

ANR detection is handled by the native `sentry-android` SDK. Android's OS flags an ANR when:
- An **activity doesn't respond to user input within 5 seconds**
- A **broadcast receiver doesn't complete within 10 seconds**

The SDK detects this via a watchdog thread monitoring the main thread. When the UI thread is blocked, an ANR event is created and sent to Sentry. ANR detection on Android is **always enabled** via the native SDK and is not configurable from JavaScript.

### iOS / tvOS / macOS — App Hangs

On Apple platforms, `sentry-cocoa` monitors the main thread with a watchdog. Any block exceeding the configured threshold triggers an error event.

```typescript
Sentry.init({
  dsn: "___PUBLIC_DSN___",

  // Disable app hang tracking (Apple platforms only)
  enableAppHangTracking: false,

  // Detection threshold in seconds (default: 2)
  // Main thread must be blocked longer than this value to trigger
  appHangTimeoutInterval: 1,
});
```

> **Note:** `enableAppHangTracking` and `appHangTimeoutInterval` apply to **iOS, tvOS, and macOS** only.

### iOS Watchdog Terminations & OOM

```typescript
Sentry.init({
  // Track out-of-memory kills and watchdog terminations on iOS (default: true)
  enableWatchdogTerminationTracking: true,
});
```

---

## 4. Unhandled Promise Rejections

The SDK automatically captures unhandled promise rejections via the built-in `UnhandledRejection` integration. Any promise that rejects without a `.catch()` or `try/catch` is captured as a Sentry error event with no configuration needed.

```typescript
// This is automatically captured by Sentry:
async function doSomething() {
  throw new Error("Unhandled rejection");
}
doSomething(); // No await, no .catch()

// To disable (if you handle these yourself elsewhere):
Sentry.init({
  integrations: (integrations) =>
    integrations.filter((i) => i.name !== "UnhandledRejection"),
});
```

---

## 5. `Sentry.wrap(App)` — Top-Level Error Boundary

`Sentry.wrap` wraps your **root component** and should be used in every React Native app using Sentry.

```typescript
// index.js / app entry point
import { AppRegistry } from "react-native";
import * as Sentry from "@sentry/react-native";
import App from "./src/App";
import { name as appName } from "./app.json";

Sentry.init({
  dsn: "https://examplePublicKey@o0.ingest.sentry.io/0",
});

AppRegistry.registerComponent(appName, () => Sentry.wrap(App));
```

**What `Sentry.wrap` does:**

| Capability | Description |
|------------|-------------|
| **React render error boundary** | Catches errors thrown during component rendering |
| **UI interaction tracking** | Records touch events as `ui.click` breadcrumbs automatically |
| **User Feedback Widget** | `Sentry.showFeedbackWidget()` requires this wrapper |
| **Session Replay buffering** | Buffers pre-error session data for the feedback widget |

---

## 6. `ErrorBoundary` Component

`Sentry.ErrorBoundary` is a React error boundary that catches render-time errors, reports them to Sentry with full React component stack context, and renders a fallback UI.

### Basic Usage

```typescript
import * as Sentry from "@sentry/react-native";

function App() {
  return (
    <Sentry.ErrorBoundary fallback={<Text>An error has occurred</Text>}>
      <Dashboard />
    </Sentry.ErrorBoundary>
  );
}
```

### Fallback as a Function

```typescript
import * as Sentry from "@sentry/react-native";

function App() {
  return (
    <Sentry.ErrorBoundary
      fallback={({ error, componentStack, resetError }) => (
        <View style={styles.errorContainer}>
          <Text style={styles.title}>Something went wrong</Text>
          <Text style={styles.message}>{error.toString()}</Text>
          <Text style={styles.stack}>{componentStack}</Text>
          <Button title="Try again" onPress={resetError} />
        </View>
      )}
    >
      <MainContent />
    </Sentry.ErrorBoundary>
  );
}
```

The fallback function receives:
- `error` — the thrown error object
- `componentStack` — React's component stack trace string
- `resetError` — function to clear error state and re-render children

### Higher-Order Component (HOC) Pattern

```typescript
import * as Sentry from "@sentry/react-native";

const SafeDashboard = Sentry.withErrorBoundary(Dashboard, {
  fallback: <View><Text>Dashboard unavailable</Text></View>,
});
```

### Multiple Boundaries with Contextual Tags

```typescript
function App() {
  return (
    <View>
      <Sentry.ErrorBoundary
        fallback={<SidebarFallback />}
        beforeCapture={(scope) => scope.setTag("section", "sidebar")}
      >
        <Sidebar />
      </Sentry.ErrorBoundary>

      <Sentry.ErrorBoundary
        fallback={<ContentFallback />}
        beforeCapture={(scope) => scope.setTag("section", "content")}
      >
        <MainContent />
      </Sentry.ErrorBoundary>
    </View>
  );
}
```

Nesting error boundaries allows granular isolation: an error in `Sidebar` won't crash `MainContent`, and each boundary tags its errors with a `section` for easy filtering in Sentry.

### Show User Feedback Dialog on Error

```typescript
<Sentry.ErrorBoundary
  showDialog       // auto-opens user feedback dialog when error is caught
  fallback={<ErrorScreen />}
>
  <App />
</Sentry.ErrorBoundary>
```

### Full Props Reference

| Prop | Type | Description |
|------|------|-------------|
| `fallback` | `ReactNode \| ({ error, componentStack, resetError }) => ReactNode` | UI rendered when an error is caught |
| `showDialog` | `boolean` | Open User Feedback widget on error |
| `dialogOptions` | `object` | Options passed to the feedback dialog |
| `onError` | `(error, componentStack, eventId) => void` | Called when an error is caught; useful for state propagation |
| `beforeCapture` | `(scope, error, componentStack) => void` | Called before sending to Sentry; add tags/context here |
| `onMount` | `() => void` | Called on `componentDidMount` |
| `onUnmount` | `() => void` | Called on `componentWillUnmount` |

### Manual Error Boundary (Class Component)

```typescript
import React from "react";
import * as Sentry from "@sentry/react-native";

class CustomErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    Sentry.captureException(error, {
      extra: { componentStack: info.componentStack },
    });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? null;
    }
    return this.props.children;
  }
}
```

> **Important:** Custom error boundaries **must be class components** — this is a React requirement, not a Sentry limitation.

---

## 7. Scope Management

Scopes hold contextual data (tags, user, breadcrumbs, contexts) that is merged into captured events. There are three scope layers with different lifetimes.

### Three Scope Types

#### Global Scope
Applied to **every event** regardless of origin. Used for low-level environmental data.

```typescript
const globalScope = Sentry.getGlobalScope();
globalScope.setTag("app_type", "mobile");
globalScope.setContext("runtime", { name: "Hermes", version: "0.11.0" });
```

#### Isolation Scope
Separates events from each other (per-session in mobile). All `Sentry.setXXX()` convenience methods write here.

```typescript
// These are equivalent:
Sentry.setTag("my-tag", "my value");
Sentry.getIsolationScope().setTag("my-tag", "my value");

// Set user for the entire session:
Sentry.setUser({ id: "42", email: "user@example.com" });
```

#### Current Scope
The locally active scope. Best accessed via `withScope()`.

### Scope Data Precedence

Scopes merge in order: **global → isolation → current**. A key on the current scope overrides the same key on outer scopes.

```typescript
Sentry.getGlobalScope().setExtras({ shared: "global", global: "data" });
Sentry.getIsolationScope().setExtras({ shared: "isolation", isolation: "data" });
Sentry.getCurrentScope().setExtras({ shared: "current", current: "data" });

// Resulting event extras: { shared: "current", global: "data", isolation: "data", current: "data" }
```

### `withScope()` — Temporary Isolated Scopes

Creates a **cloned scope** valid only inside the callback. Changes do not affect the outer scope.

```typescript
// Error 1 gets the tag; Error 2 does NOT
Sentry.withScope((scope) => {
  scope.setTag("my-tag", "my value");
  scope.setLevel("warning");
  Sentry.captureException(new Error("my error")); // tagged
});
Sentry.captureException(new Error("my other error")); // NOT tagged

// Temporarily override user identity for one capture
Sentry.withScope((scope) => {
  scope.setUser({ id: "service-account" });
  Sentry.captureException(backgroundJobError);
  // original user identity restored after this block
});
```

### Convenience Methods (All Write to Isolation Scope)

```typescript
Sentry.setTag(key, value)
Sentry.setTags({ key: value })
Sentry.setUser({ id, email, username })
Sentry.setContext(name, object)
Sentry.setExtra(key, value)
Sentry.setExtras({ key: value })
Sentry.addBreadcrumb(breadcrumb)
```

---

## 8. Context Enrichment — Tags, User, Extra, Contexts

### Tags — Indexed & Searchable

Tags are **key/value string pairs** indexed in Sentry, enabling full-text search, filter sidebars, and distribution maps in the UI.

```typescript
Sentry.setTag("page_locale", "de-at");
Sentry.setTag("app_version", "3.2.1");
Sentry.setTag("user_plan", "enterprise");
```

**Tag constraints:**

| Property | Constraint |
|----------|-----------|
| Key max length | 32 characters |
| Key allowed characters | `a-zA-Z`, `0-9`, `_`, `.`, `:`, `-` |
| Value max length | 200 characters |
| Value forbidden | Newline `\n` characters |

### User Identity

```typescript
// Set on login
Sentry.setUser({
  id: "42",
  email: "john.doe@example.com",
  username: "johndoe",
  ip_address: "{{auto}}", // Sentry resolves this automatically
  // Any additional key-value pairs
  plan: "enterprise",
  role: "admin",
});

// Clear on logout
Sentry.setUser(null);
```

### Custom Structured Contexts

Structured contexts attach arbitrary nested objects to events. They appear on the issue detail page but are **not searchable** (use tags for searchable data).

```typescript
Sentry.setContext("character", {
  name: "Mighty Fighter",
  age: 19,
  attack_type: "melee",
});

Sentry.setContext("order", {
  id: "ORD-9821",
  total: 129.99,
  items: ["item-1", "item-2"],
  shipping: { method: "express", address: "123 Main St" },
});
```

> **Notes:**
> - The key `"type"` is reserved by Sentry — do not use it
> - Context nesting is normalized to **3 levels** by default (configurable via `normalizeDepth`)
> - Avoid sending entire app state blobs; exceeding max payload size triggers HTTP `413`

### Extra Data (Deprecated)

```typescript
// Deprecated — use setContext() instead
Sentry.setExtra("server_name", "web-01");
Sentry.setExtras({ key1: "value1", key2: "value2" });
```

### Inline Context on Capture Calls

```typescript
Sentry.captureException(new Error("something went wrong"), {
  tags: { section: "articles" },
  user: { id: "42", email: "user@example.com" },
  extra: { requestId: "abc-123" },
  contexts: { order: { id: "ORD-9821" } },
  level: "warning",
  fingerprint: ["{{ default }}", "order-error"],
});
```

### Clearing Context

```typescript
// Clear all scope data
Sentry.getCurrentScope().clear();

// Reset user
Sentry.setUser(null);

// Remove a specific tag
Sentry.setTag("key", undefined);
```

---

## 9. Breadcrumbs — Automatic & Manual

Breadcrumbs form a timeline of events leading up to an error. They buffer until the next event is captured — they do not create Sentry issues on their own.

### Manual Breadcrumbs

```typescript
import * as Sentry from "@sentry/react-native";

// Navigation event
Sentry.addBreadcrumb({
  category: "navigation",
  message: "Navigated to screen",
  level: "info",
  data: {
    from: "HomeScreen",
    to: "ProfileScreen",
    params: { userId: "42" },
  },
});

// Authentication event
Sentry.addBreadcrumb({
  category: "auth",
  message: "User logged in: " + user.email,
  level: "info",
});

// API failure before throwing
Sentry.addBreadcrumb({
  category: "api",
  message: "Checkout API call failed",
  level: "error",
  data: {
    url: "/api/checkout",
    status: 500,
    method: "POST",
  },
});
```

**Breadcrumb properties:**

| Property | Description |
|----------|-------------|
| `type` | `"default"`, `"http"`, `"navigation"`, `"user"` |
| `category` | Dot-separated string (e.g., `"ui.click"`, `"http"`, `"auth"`) |
| `message` | Human-readable description |
| `level` | `"fatal"`, `"critical"`, `"error"`, `"warning"`, `"log"`, `"info"`, `"debug"` |
| `timestamp` | Unix timestamp (auto-set if omitted) |
| `data` | Arbitrary `{ key: value }` metadata |

> **Warning:** Unknown keys beyond those above are silently dropped during processing.

### Automatic Breadcrumbs

| Source | Category | How |
|--------|----------|-----|
| Touch interactions | `ui.click` | Via `Sentry.wrap` on root component |
| HTTP requests | `http` | Fetch/XHR patching (default) |
| Console output | `console` | `console.log/warn/error` patching (default) |
| Navigation | `navigation` | Via navigation integrations |
| Redux actions | `redux.action` | Via `Sentry.createReduxEnhancer` |
| Native lifecycle | various | From native SDKs (connectivity changes, lifecycle events) |

### `beforeBreadcrumb` Hook

```typescript
Sentry.init({
  beforeBreadcrumb(breadcrumb, hint) {
    // Drop all UI click breadcrumbs
    if (breadcrumb.category === "ui.click") {
      return null;
    }

    // Scrub auth tokens from HTTP breadcrumbs
    if (breadcrumb.category === "http" && breadcrumb.data?.url) {
      breadcrumb.data.url = breadcrumb.data.url.replace(
        /token=[^&]*/,
        "token=REDACTED"
      );
    }

    // Add extra metadata to console breadcrumbs
    if (breadcrumb.category === "console") {
      breadcrumb.data = { ...breadcrumb.data, deviceTime: Date.now() };
    }

    return breadcrumb; // return null to drop
  },
});
```

### Breadcrumb Capacity

```typescript
Sentry.init({
  // Default is 100; oldest breadcrumbs are discarded when full
  maxBreadcrumbs: 50,
});
```

---

## 10. `beforeSend` / `beforeSendTransaction` Hooks

These hooks fire immediately before an event is transmitted, giving you a final chance to modify or suppress it.

> **Important:** `beforeSend` only runs on **JavaScript-layer events**. It does not affect native Android/iOS crash events captured by the native SDKs.

### `beforeSend` — Error Events

```typescript
Sentry.init({
  beforeSend(event, hint) {
    // hint.originalException — the original thrown Error object
    // hint.syntheticException — auto-generated when non-Error is thrown
    // hint.event_id — the generated event ID

    // Drop events matching a pattern
    if (event.exception?.values?.[0]?.value?.includes("ResizeObserver")) {
      return null;
    }

    // Scrub PII before sending
    if (event.user) {
      delete event.user.email;
      delete event.user.ip_address;
    }

    // Set fingerprint based on error message
    const error = hint.originalException as Error;
    if (error?.message?.match(/database unavailable/i)) {
      event.fingerprint = ["database-unavailable"];
    }

    // Attach extra data
    event.extra = {
      ...event.extra,
      build_number: "42",
    };

    return event; // return null to drop, return event to send
  },
});
```

### `beforeSendTransaction` — Performance Transactions

```typescript
Sentry.init({
  beforeSendTransaction(event) {
    // Drop health check transactions
    if (event.transaction === "/health") return null;

    // Normalize internal transaction names
    if (event.transaction?.startsWith("/internal/")) {
      event.transaction = "/internal/*";
    }

    return event;
  },
});
```

### `ignoreErrors` / `ignoreTransactions`

Pre-filter before `beforeSend` even runs — more efficient for known noise patterns:

```typescript
Sentry.init({
  ignoreErrors: [
    "ResizeObserver loop limit exceeded",
    "Non-Error exception captured",
    /^Script error\.?$/,
  ],
  ignoreTransactions: [
    "/healthcheck",
    /^\/admin\/internal\//,
  ],
});
```

---

## 11. Fingerprinting & Grouping

Fingerprinting controls how Sentry groups events into issues. By default, Sentry groups by stack trace. You can override this to merge or split issues.

### SDK-Level Fingerprinting

```typescript
// Static fingerprint — all matching events become one issue
Sentry.captureException(new Error("DB connection failed"), {
  fingerprint: ["database-connection-error"],
});

// Dynamic — include URL and status for more granular groups
Sentry.captureException(networkErr, {
  fingerprint: ["{{ default }}", networkErr.url, String(networkErr.status)],
});

// Dynamic via beforeSend
Sentry.init({
  beforeSend(event, hint) {
    const error = hint.originalException as Error;
    if (error?.message?.match(/network request failed/i)) {
      event.fingerprint = [
        "network-error",
        event.request?.url ?? "unknown-url",
      ];
    }
    return event;
  },
});
```

### Fingerprint Variables

| Variable | Resolves to |
|----------|-------------|
| `{{ default }}` | Sentry's default grouping hash |
| `{{ error.type }}` | Exception class name |
| `{{ error.value }}` | Exception message text |
| `{{ transaction }}` | Current transaction name |
| `{{ level }}` | Event severity level |
| `{{ message }}` | Captured message |
| `{{ stack.function }}` | Top stack frame function name |
| `{{ stack.module }}` | Top stack frame module |

### Server-Side Fingerprint Rules (Project Settings)

```
# Group all DB errors together regardless of message
error.type:DatabaseUnavailable -> system-down
error.type:ConnectionError -> system-down

# Subdivide connection errors by transaction
error.value:"connection error: *" -> connection-error, {{ transaction }}

# Custom issue title
logger:my.package.* level:error -> error-logger, {{ logger }} title="Error from Logger {{ logger }}"
```

### Fingerprint Priority

1. SDK-set `fingerprint` (in `captureException`, `beforeSend`, or `captureEvent`)
2. Server-side fingerprint rules (Sentry project settings)
3. Sentry's default stack-trace-based grouping

---

## 12. Event Processors

Event processors run on **every event** before transmission. They differ from `beforeSend` in two key ways:
1. `beforeSend` always runs **last**, after all event processors
2. Processors added to a scope only apply to events **within that scope**

### Global Event Processor

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.addEventProcessor((event, hint) => {
  // Enrich all events with app metadata
  event.extra = {
    ...event.extra,
    appBuildTime: BUILD_TIMESTAMP,
    featureFlags: getActiveFeatureFlags(),
  };

  // Drop events from test environments
  if (isTestEnvironment()) return null;

  return event;
});
```

### Scoped Event Processor

```typescript
Sentry.withScope((scope) => {
  scope.addEventProcessor((event, hint) => {
    // Only runs for events captured inside this withScope block
    event.tags = { ...event.tags, flow: "checkout" };
    return event;
  });

  Sentry.captureException(checkoutError); // ✅ processor fires
});

Sentry.captureException(otherError); // ❌ processor does NOT fire
```

### Async Event Processors

```typescript
Sentry.addEventProcessor(async (event, hint) => {
  const deviceInfo = await getDeviceInfo();
  event.contexts = { ...event.contexts, device: deviceInfo };
  return event;
});
```

### Execution Order

```
[All addEventProcessor / scope.addEventProcessor functions]
  ↓ (in registration order)
[beforeSend / beforeSendTransaction]
  ↓ (always last)
[Sentry servers]
```

---

## 13. Attachments — Screenshots & View Hierarchy

### Automatic Screenshot on Error

Captures a PNG screenshot at the moment an error occurs. Attached to the event in Sentry's issue detail view.

```typescript
Sentry.init({
  // Available since @sentry/react-native v4.11.0
  attachScreenshot: true,
});
```

Screenshots appear under **"Attachments"** on the event detail page in Sentry.

> **PII consideration:** Screenshots may capture sensitive data visible on screen (forms, personal information). Review before enabling in production.

### View Hierarchy Capture

Captures a JSON representation of the native component hierarchy at crash time.

```typescript
Sentry.init({
  attachViewHierarchy: true,
});
```

The view hierarchy appears in Sentry's **"View Hierarchy"** tab on the event.

### Manual File Attachments

```typescript
Sentry.captureException(err, {
  attachments: [
    {
      filename: "config.json",
      data: JSON.stringify(appConfig),
      contentType: "application/json",
    },
    {
      filename: "debug.log",
      data: logFileContents,         // string or Uint8Array
      contentType: "text/plain",
    },
    {
      filename: "screenshot.png",
      data: base64PngData,
      contentType: "image/png",
    },
  ],
});
```

### Attachments via Scope

```typescript
Sentry.withScope((scope) => {
  scope.addAttachment({
    filename: "state_snapshot.json",
    data: JSON.stringify(store.getState()),
    contentType: "application/json",
  });
  Sentry.captureException(error);
});
```

> **Size limits:** Attachments must not push the total event payload over Sentry's maximum. Oversized payloads return HTTP `413 Payload Too Large`.

---

## 14. Redux Integration

The `createReduxEnhancer` captures Redux state snapshots and action history as breadcrumbs on error events.

### Setup

```typescript
import { createStore } from "redux";
import * as Sentry from "@sentry/react-native";

const store = createStore(
  rootReducer,
  Sentry.createReduxEnhancer({
    // Transform action before recording — return null to skip
    actionTransformer: (action) => {
      if (action.type === "SENSITIVE_ACTION") return null;
      if (action.type === "SET_PASSWORD") {
        return { ...action, payload: "[REDACTED]" };
      }
      return action;
    },

    // Transform state snapshot — avoid sending large state trees
    stateTransformer: (state) => ({
      selectedTab: state.ui.selectedTab,
      userPlan: state.user.plan,
      cartItemCount: state.cart.items.length,
    }),
  })
);
```

### With Redux Toolkit

```typescript
import { configureStore } from "@reduxjs/toolkit";
import * as Sentry from "@sentry/react-native";

const store = configureStore({
  reducer: rootReducer,
  enhancers: (getDefaultEnhancers) =>
    getDefaultEnhancers().concat(
      Sentry.createReduxEnhancer({
        actionTransformer: (action) => {
          // Drop auth-related actions from breadcrumbs
          if (action.type.startsWith("auth/")) return null;
          return action;
        },
      })
    ),
});
```

Dispatched actions appear in Sentry as `redux.action` breadcrumbs. State at the time of an error is attached to the event under `state.value`.

---

## 15. Device & App Context

The SDK automatically attaches rich device context to every event — no configuration required.

### Automatic Context (No Setup Needed)

| Context Section | Fields | Source |
|-----------------|--------|--------|
| **Device** | Model, manufacturer, brand, screen resolution, orientation, free memory, battery level, charging state | Native SDK |
| **OS** | Name (`iOS`/`Android`), version, build number, kernel version | Native SDK |
| **App** | App ID, version name, version code, build type | Native SDK |
| **React Native** | RN version, JS engine (Hermes/JSC), architecture | JS SDK |

These appear in Sentry under the **"Device"**, **"Operating System"**, and **"App"** sections of any event.

### Overriding or Extending Device Context

```typescript
Sentry.setContext("device", {
  custom_hardware_id: "DEVICE-UUID-123",
});

Sentry.setContext("app", {
  app_version: "3.2.1",
  app_build: "421",
  custom_build_flavor: "staging",
});
```

### Release, Distribution & Environment

```typescript
Sentry.init({
  // Used in Sentry for regression detection and release health
  release: "com.myapp@3.2.1+421",

  // Distinguishes builds within a release (e.g., Xcode build number)
  dist: "421",

  // Shown on every event for filtering
  environment: "production", // "staging" | "development" | "production"
});
```

---

## 16. Release Health & Sessions

Sentry tracks **session-based metrics** to surface crash-free rates and regressions across app versions.

### How Sessions Work

A session begins when the app comes to the foreground and ends when it goes to background for longer than `sessionTrackingIntervalMillis` (default: 30 seconds). Each session maps to a release version, enabling Sentry to compute:

- **Crash-free session rate** — % of sessions without a fatal crash
- **Crash-free user rate** — % of users without a crash in a given release

```typescript
Sentry.init({
  release: "com.myapp@3.2.1+421",
  autoSessionTracking: true,                    // default: true
  sessionTrackingIntervalMillis: 30000,          // default: 30s background threshold
});
```

Sessions are sent automatically. No additional API calls are required.

---

## 17. Offline Event Caching

The SDK caches events locally when the device has no network connectivity. Events are transmitted automatically when connectivity is restored.

```typescript
Sentry.init({
  // Maximum number of envelopes to cache on disk (default: 30)
  maxCacheItems: 30,
});
```

| Platform | Cache Location | Transmission Trigger |
|----------|---------------|----------------------|
| Android | Internal app storage | App restart |
| iOS | App sandbox `Library/Caches/` | Next event fires |

Offline caching works for both JS-layer events and native crash reports.

---

## 18. Default Integrations

The following integrations are enabled automatically:

| Integration | Purpose |
|-------------|---------|
| **InboundFilters** | Drops events matching `ignoreErrors`, `denyUrls`, `allowUrls`. Default-ignores `"Script error"` |
| **FunctionToString** | Preserves original function names even when SDK wraps handlers |
| **Breadcrumbs** | Patches `console`, `fetch`, `XHR` to auto-capture breadcrumbs |
| **NativeLinkedErrors** | Reads `.cause` chains up to 5 levels deep |
| **HttpContext** | Attaches URL, user-agent, referrer to events |
| **Dedupe** | Prevents duplicate consecutive events from being reported |
| **UnhandledRejection** | Auto-captures unhandled promise rejections |

### Customizing Default Integrations

```typescript
// Disable all defaults (rarely needed)
Sentry.init({ defaultIntegrations: false });

// Disable console breadcrumbs only
Sentry.init({
  integrations: [
    Sentry.breadcrumbsIntegration({
      console: false,  // disable console breadcrumbs
      fetch: true,
      xhr: true,
      sentry: true,
      // Note: `dom` and `history` are web-only — not applicable in React Native
    }),
  ],
});

// Remove a specific integration
Sentry.init({
  integrations: (integrations) =>
    integrations.filter((i) => i.name !== "Breadcrumbs"),
});
```

### Opt-In Integrations

```typescript
Sentry.init({
  integrations: [
    // Capture failed HTTP requests (non-2xx) as Sentry errors (v5.3.0+)
    Sentry.httpClientIntegration({
      failedRequestStatusCodes: [[400, 599]],
      failedRequestTargets: ["https://api.myapp.com"],
    }),

    // Rewrite stack frame file paths (useful for custom source map layouts)
    Sentry.rewriteFramesIntegration({ root: "/" }),
  ],
  // Shorthand for httpClientIntegration with default settings:
  enableCaptureFailedRequests: true,
});
```

---

## 19. Full `init()` Options Reference

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  // ── Core ──────────────────────────────────────────────────────────
  dsn: "https://examplePublicKey@o0.ingest.sentry.io/0",
  enabled: true,              // false disables all SDK transmission
  debug: false,               // log SDK internals to console
  release: "com.myapp@3.2.1+421",
  dist: "421",                // distinguishes builds within a release
  environment: "production",
  sampleRate: 1.0,            // 0.0–1.0; fraction of error events to send

  // ── Filtering ─────────────────────────────────────────────────────
  ignoreErrors: ["Script error", /^Non-Error/],
  ignoreTransactions: ["/healthcheck"],
  // denyUrls / allowUrls match stack frame URLs — primarily useful for web;
  // in React Native these can filter native frames but are rarely needed.
  // denyUrls: ["chrome-extension://", /extensions\//i],
  // allowUrls: ["https://myapp.com"],
  maxBreadcrumbs: 100,
  maxValueLength: 250,        // max length of string values in events

  // ── Normalization ─────────────────────────────────────────────────
  normalizeDepth: 3,          // depth to normalize context objects
  normalizeMaxBreadth: 1000,  // max number of object properties

  // ── Hooks ─────────────────────────────────────────────────────────
  beforeSend(event, hint) {
    // JS-layer events only. Return null to drop.
    return event;
  },
  beforeSendTransaction(event) {
    return event;
  },
  beforeBreadcrumb(breadcrumb, hint) {
    return breadcrumb; // return null to drop
  },

  // ── Attachments ───────────────────────────────────────────────────
  attachStacktrace: true,          // stack traces on captureMessage calls
  attachScreenshot: false,         // auto-screenshot on error (v4.11.0+)
  attachViewHierarchy: false,      // native view hierarchy JSON on error
  sendDefaultPii: false,           // allow integrations to send PII

  // ── Transport ─────────────────────────────────────────────────────
  maxCacheItems: 30,               // max envelopes cached offline
  shutdownTimeout: 2000,           // ms to wait for queue drain on shutdown

  // ── Sessions ──────────────────────────────────────────────────────
  autoSessionTracking: true,
  sessionTrackingIntervalMillis: 30000,

  // ── Performance / Tracing ─────────────────────────────────────────
  tracesSampleRate: 0.2,
  tracesSampler: ({ name, attributes, parentSampled }) => {
    if (name.includes("healthcheck")) return 0;
    if (typeof parentSampled === "boolean") return parentSampled;
    return 0.2;
  },
  tracePropagationTargets: ["localhost", /^https:\/\/api\.myapp\.com/],
  enableAutoPerformanceTracing: true,

  // ── Native / Hybrid ───────────────────────────────────────────────
  enableNative: true,
  enableNativeCrashHandling: true,
  autoInitializeNativeSdk: true,
  enableNdkScopeSync: true,            // sync Java scope to NDK (Android)
  enableTombstone: true,               // Android 12+ ApplicationExitInfo (default: false)
  attachThreads: false,                // all threads on Android events
  enableNativeNagger: true,            // warn if native init fails
  enableWatchdogTerminationTracking: true, // iOS OOM tracking

  // ── ANR / App Hang ────────────────────────────────────────────────
  enableAppHangTracking: true,         // Apple platforms only
  appHangTimeoutInterval: 2,           // Apple platforms only, seconds

  // ── HTTP Client ───────────────────────────────────────────────────
  enableCaptureFailedRequests: false,  // auto-capture HTTP errors (v5.3.0+)

  // ── Callbacks ─────────────────────────────────────────────────────
  onReady: () => console.log("Sentry native SDKs initialized"),

  // ── Integrations ──────────────────────────────────────────────────
  integrations: [
    Sentry.feedbackIntegration({
      styles: { submitButton: { backgroundColor: "#6a1b9a" } },
    }),
    Sentry.httpClientIntegration(),
  ],
  defaultIntegrations: true,  // false disables all built-in integrations
});
```

---

## 20. Quick Reference Cheatsheet

```typescript
import * as Sentry from "@sentry/react-native";

// ── Init & Wrap ────────────────────────────────────────────────────
Sentry.init({ dsn: "...", release: "...", environment: "production" });
export default Sentry.wrap(App);  // required for touch breadcrumbs + feedback widget

// ── Capture ───────────────────────────────────────────────────────
Sentry.captureException(new Error("oh no"));
Sentry.captureMessage("Something happened", "warning");
Sentry.captureEvent({ message: "raw event", level: "info" });

// ── Identity & Context ────────────────────────────────────────────
Sentry.setUser({ id: "42", email: "user@example.com" });
Sentry.setTag("version", "3.2.1");
Sentry.setContext("order", { id: "ORD-99", total: 59.99 });

// ── Scopes ────────────────────────────────────────────────────────
Sentry.withScope((scope) => {
  scope.setTag("temp", "value");
  Sentry.captureException(err);
});
Sentry.getGlobalScope().setTag("app", "mobile");
Sentry.getCurrentScope().clear();

// ── Breadcrumbs ───────────────────────────────────────────────────
Sentry.addBreadcrumb({ category: "auth", message: "Login", level: "info" });

// ── Error Boundaries ──────────────────────────────────────────────
<Sentry.ErrorBoundary
  fallback={({ error, resetError }) => (
    <View><Text>{error.toString()}</Text><Button onPress={resetError} title="Retry" /></View>
  )}
  beforeCapture={(scope) => scope.setTag("section", "main")}
>
  <App />
</Sentry.ErrorBoundary>

// ── Event Processor ───────────────────────────────────────────────
Sentry.addEventProcessor((event) => { event.extra = { foo: "bar" }; return event; });
```

---

## 21. Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing in Sentry | Check DSN is correct; set `debug: true` to see SDK logs; verify `enabled: true`; check for `beforeSend` returning `null` |
| Native crashes not reported | Ensure `enableNative: true` and `enableNativeCrashHandling: true`; check that native SDKs initialized (look for `onReady` callback firing) |
| ANR/hang events not appearing | Android ANR is always on; for iOS, verify `enableAppHangTracking: true` and try lowering `appHangTimeoutInterval` |
| `Sentry.wrap` not working | Confirm it wraps the **root component** registered with `AppRegistry` (not an inner component) |
| `showFeedbackWidget()` crashes | App must be wrapped with `Sentry.wrap(App)`; ensure Fabric (new arch) requires RN ≥ 0.71 |
| Screenshots are blank | Screenshot capture may be blocked on certain Android versions; ensure `attachScreenshot: true` |
| `beforeSend` not filtering native crashes | `beforeSend` only filters JS-layer events; native crashes bypass it — use `enableNativeCrashHandling: false` to disable native crash capture entirely |
| Duplicate events appearing | Check for multiple `Sentry.init()` calls; `Dedupe` integration handles sequential duplicates but not concurrent ones |
| Too many breadcrumbs / events | Reduce `maxBreadcrumbs`; use `beforeBreadcrumb` to filter; use `sampleRate` to reduce event volume |
| HTTP errors not captured | Add `enableCaptureFailedRequests: true` (v5.3.0+) or configure `httpClientIntegration()` |
| Missing stack frames (minified) | Upload source maps via Sentry CLI or the Metro plugin; check `dist` and `release` match the build |
| `setContext` data not appearing | Verify key `"type"` is not used (reserved); check `normalizeDepth` isn't truncating nested data |
| Event payload rejected with 413 | Attachment or context too large; use `stateTransformer` in Redux enhancer; limit attachment sizes |
| Offline events not sent | Events are sent on next app launch (Android) or next event fire (iOS); check `maxCacheItems` isn't set too low |

---

## Reference: Logging

# Logging — Sentry React Native SDK

> **Minimum SDK:** `@sentry/react-native` ≥7.0.0 for `Sentry.logger` API  
> **Scope-based attribute setters** (`getGlobalScope`, `withScope`): requires ≥7.8.0  
> **`consoleLoggingIntegration()`**: requires ≥7.0.0

---

## Enabling Logs

`enableLogs` is **off by default** — opt in explicitly:

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN",
  enableLogs: true,
});
```

Place this in your app entry point — `index.js`, `App.tsx`, or `app/_layout.tsx` (Expo Router), depending on your project structure.

---

## Logger API — Six Levels

```typescript
import * as Sentry from "@sentry/react-native";

// Fine-grained debugging — high volume, filter in production
Sentry.logger.trace("Starting authentication flow", { provider: "oauth" });

// Development diagnostics
Sentry.logger.debug("Cache lookup", { key: "user:123", hit: false });

// Normal operations and business milestones
Sentry.logger.info("Order created", { orderId: "order_456", total: 99.99 });

// Degraded state, approaching limits
Sentry.logger.warn("Rate limit approaching", {
  endpoint: "/api/results/",
  current: 95,
  max: 100,
});

// Failures requiring attention
Sentry.logger.error("Payment failed", {
  reason: "card_declined",
  userId: "u_1",
});

// Critical failures — app is down
Sentry.logger.fatal("Database unavailable", { host: "db-primary" });
```

### Level Selection Guide

| Level | When to Use |
|-------|-------------|
| `trace` | Step-by-step internals, loop iterations, low-level flow tracking |
| `debug` | Diagnostic information useful during development |
| `info` | Business events, user actions, meaningful state transitions |
| `warn` | Recoverable errors, degraded performance, approaching limits |
| `error` | Failures that need investigation but don't crash the app |
| `fatal` | Unrecoverable failures — app or critical subsystem is down |

**Attribute value types:** `string`, `number`, and `boolean` only. Other types will be dropped or coerced.

---

## Parameterized Messages with `logger.fmt`

Use `Sentry.logger.fmt` as a tagged template literal to make message variables **individually searchable** in Sentry. Each interpolated value becomes a `message.parameter.N` attribute:

```typescript
const userId = "user_123";
const productName = "Widget Pro";
const amount = 49.99;

Sentry.logger.info(
  Sentry.logger.fmt`User ${userId} purchased ${productName} for $${amount}`
);
// → message.template:    "User %s purchased %s for $%s"
// → message.parameter.0: "user_123"
// → message.parameter.1: "Widget Pro"
// → message.parameter.2: 49.99

Sentry.logger.error(
  Sentry.logger.fmt`Failed to load screen ${screenName}: ${error.message}`
);
```

You can now filter and search for logs by individual parameter values in the Sentry Logs UI — not just by the full message string.

---

## Structured Attributes

Pass attributes as the second argument. They become **queryable columns** in Sentry Logs:

```typescript
Sentry.logger.info("Checkout completed", {
  orderId: order.id,
  userId: user.id,
  cartValue: cart.total,
  itemCount: cart.items.length,
  paymentMethod: "stripe",
  durationMs: Date.now() - startTime,
});

Sentry.logger.error("Navigation failed", {
  fromScreen: "Home",
  toScreen: "Profile",
  errorCode: err.code,
  retryable: true,
});
```

---

## Scope-Based Automatic Attributes (SDK ≥7.8.0)

Set attributes once on a scope and they are **automatically attached to all logs** emitted within that scope.

### Global scope — entire app lifetime

```typescript
// In your Sentry.init block or app startup
Sentry.getGlobalScope().setAttributes({
  app_version: "2.1.0",
  build_number: "42",
  platform: Platform.OS,       // "ios" or "android"
  environment: __DEV__ ? "development" : "production",
});
```

### Scoped attributes — single operation or code block

```typescript
Sentry.withScope(async (scope) => {
  scope.setAttribute("order_id", "ord_789");
  scope.setAttribute("payment_method", "stripe");

  Sentry.logger.info("Validating cart", { cartId: cart.id });
  // order_id and payment_method included in this log
  await processPayment();
  Sentry.logger.info("Payment complete");
  // order_id and payment_method included here too
});
```

---

## Console Logging Integration

Automatically forwards `console.log`, `console.warn`, and `console.error` calls to Sentry as structured logs. Requires SDK ≥7.0.0.

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  enableLogs: true,
  integrations: [
    Sentry.consoleLoggingIntegration({
      levels: ["log", "warn", "error"],  // default — adjust as needed
    }),
  ],
});

// These are now automatically forwarded to Sentry:
console.log("User action:", userId, success);
// → message.parameter.0: userId
// → message.parameter.1: success

console.warn("Memory pressure detected", memoryUsage);
console.error("Fetch failed:", error.message);
```

> **React Native note:** All `console.*` calls in React Native go through the JS bridge. In development, the `consoleLoggingIntegration` will forward them all — use `beforeSendLog` to filter out noise before it reaches Sentry.

---

## Filtering with `beforeSendLog`

Filter or mutate every log before it is transmitted. Return `null` to drop the log entirely:

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  enableLogs: true,
  beforeSendLog: (log) => {
    // Drop low-level logs in production to reduce volume
    if (!__DEV__ && (log.level === "trace" || log.level === "debug")) {
      return null;
    }

    // Scrub sensitive attribute values
    if (log.attributes?.password) {
      delete log.attributes.password;
    }
    if (log.attributes?.credit_card) {
      log.attributes.credit_card = "[REDACTED]";
    }

    // Drop health check noise from console capture
    if (log.message?.includes("heartbeat")) return null;

    return log;
  },
});
```

The `log` object has the following shape:

| Field | Type | Description |
|-------|------|-------------|
| `level` | `string` | `"trace"`, `"debug"`, `"info"`, `"warn"`, `"error"`, `"fatal"` |
| `message` | `string` | The log message (template-expanded) |
| `timestamp` | `number` | Unix timestamp |
| `attributes` | `object` | All structured attributes |

---

## Auto-Generated Attributes

The SDK automatically attaches these attributes to every log:

| Attribute | Source |
|-----------|--------|
| `sentry.environment` | `Sentry.init({ environment })` |
| `sentry.release` | `Sentry.init({ release })` |
| `sentry.sdk.name` | SDK internals |
| `sentry.sdk.version` | SDK internals |
| `user.id`, `user.name`, `user.email` | `Sentry.setUser()` when set |
| `sentry.message.template` | `logger.fmt` usage |
| `sentry.message.parameter.X` | `logger.fmt` interpolated values |
| `origin` | Identifies which integration emitted the log |

### React Native vs Web — Attribute Differences

React Native **does not** emit the following attributes that web SDKs include:

- `browser.name` / `browser.version` — not applicable on native
- `sentry.trace.parent_span_id` — not linked unless using the web tracing stack
- `sentry.replay_id` — not automatically attached to log events in React Native (mobile replay uses a different linking mechanism)
- `server.address` — server-side only
- `payload_size` — web-only

---

## Log Correlation with Traces

When tracing is enabled, logs emitted inside an active span are **automatically correlated** in the Sentry UI. Navigate from a log to its parent span or from a trace to all logs emitted during it.

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  enableLogs: true,
  tracesSampleRate: 1.0,
  integrations: [
    Sentry.reactNavigationIntegration(), // auto-instruments screen transitions
  ],
});

// Inside a Sentry span, logs get linked automatically
await Sentry.startSpan({ name: "checkout", op: "ui.action" }, async () => {
  Sentry.logger.info("Validating cart", { cartId: cart.id });
  await validateCart();

  Sentry.logger.info("Initiating payment", { gateway: "stripe" });
  await processPayment();

  Sentry.logger.info("Checkout complete", { orderId: newOrder.id });
});
// All three logs are linked to the "checkout" span in the Sentry trace view
```

---

## Practical Patterns

### Screen lifecycle logging

```typescript
function ProductScreen({ route }) {
  const { productId } = route.params;

  useEffect(() => {
    Sentry.logger.info("Screen mounted", {
      screen: "ProductScreen",
      productId,
    });

    return () => {
      Sentry.logger.debug("Screen unmounted", { screen: "ProductScreen" });
    };
  }, []);

  const handlePurchase = async () => {
    Sentry.logger.info(
      Sentry.logger.fmt`User initiated purchase for product ${productId}`
    );
    try {
      const result = await purchaseProduct(productId);
      Sentry.logger.info("Purchase succeeded", {
        productId,
        orderId: result.orderId,
      });
    } catch (err) {
      Sentry.logger.error("Purchase failed", {
        productId,
        reason: err.message,
        code: err.code,
      });
    }
  };
}
```

### API call logging

```typescript
async function fetchUserData(userId: string) {
  Sentry.logger.debug(
    Sentry.logger.fmt`Fetching user data for ${userId}`
  );

  const startTime = Date.now();

  try {
    const response = await api.get(`/users/${userId}`);
    Sentry.logger.info("User data fetched", {
      userId,
      durationMs: Date.now() - startTime,
      status: response.status,
    });
    return response.data;
  } catch (err) {
    Sentry.logger.error("User data fetch failed", {
      userId,
      durationMs: Date.now() - startTime,
      status: err.response?.status,
      message: err.message,
    });
    throw err;
  }
}
```

### Redux action logging

```typescript
// Log significant state transitions alongside Redux breadcrumbs
const sentryReduxEnhancer = Sentry.createReduxEnhancer({
  configureScopeWithState: (scope, state) => {
    scope.setTag("user.plan", state.user.subscription);
  },
});

// In your reducers or middleware
function checkoutMiddleware(store) {
  return (next) => (action) => {
    if (action.type === "checkout/completed") {
      Sentry.logger.info("Checkout completed via Redux", {
        orderId: action.payload.orderId,
        total: action.payload.total,
      });
    }
    return next(action);
  };
}
```

---

## Configuration Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enableLogs` | `boolean` | `false` | Master switch — must be `true` for all logging features |
| `beforeSendLog` | `(log) => log \| null` | `undefined` | Filter/mutate logs before transmission |
| `consoleLoggingIntegration` | integration | not added | Capture `console.*` calls as structured logs |

---

## Performance Considerations

- **Log volume:** Every `Sentry.logger.*` call is batched and sent asynchronously — there is no synchronous network overhead per call.
- **Sampling:** Unlike errors and transactions, logs do not currently support sampling rates. Use `beforeSendLog` to drop entire log levels in production (e.g., drop `trace` and `debug`).
- **Size limit:** Log payloads over **1 MB** are dropped server-side. If logs are silently disappearing, check your Sentry org stats.
- **Missing logs on crash:** If the app terminates before the SDK flushes its buffer, the most recent logs may not reach Sentry. This is a known limitation under active improvement.
- **`console.*` forwarding overhead:** `consoleLoggingIntegration` wraps native console methods. In development this is fine; in production, scope it tightly using the `levels` option.

---

## Known Limitations

| Limitation | Details |
|------------|---------|
| Crash buffer loss | Logs buffered since last flush are lost on unexpected termination |
| No per-log sampling | Use `beforeSendLog` to reduce volume; sampling is all-or-nothing |
| 1 MB size cap | Logs larger than 1 MB are dropped server-side |
| No `browser.*` attributes | React Native emits no browser context — these columns are empty in the Logs UI |
| Session Replay not on logs | Expected — mobile replay doesn't populate this attribute on log events; replay is still linked via trace context |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing in Sentry | Check `enableLogs: true` is set in `Sentry.init()` |
| SDK version too old | Upgrade to `@sentry/react-native` ≥7.0.0 for `Sentry.logger`; ≥7.0.0 for `consoleLoggingIntegration`; ≥7.8.0 for scope attribute setters |
| `logger.fmt` not creating `parameter.*` attributes | Ensure it is called as a tagged template literal: `Sentry.logger.fmt\`...\`` — not as a function `Sentry.logger.fmt(...)` |
| Logs disappearing silently | Check Sentry org stats for rate limiting or logs exceeding 1 MB |
| Attribute values showing `[Filtered]` | Server-side PII scrubbing rule matched — adjust **Data Scrubbing** settings in your Sentry project |
| `console.log` calls not forwarded | Add `consoleLoggingIntegration()` to `integrations` and ensure the `levels` array includes `"log"` |
| Too many logs in production | Use `beforeSendLog` to drop `trace`/`debug` levels when `!__DEV__` |
| Logs not linked to traces | Enable tracing (`tracesSampleRate > 0`) and emit logs inside a `Sentry.startSpan()` callback |
| Scope attributes not attaching | Upgrade to ≥7.8.0 for `getGlobalScope().setAttributes()` support |

---

## Reference: Profiling

# Profiling — Sentry React Native SDK

> **Minimum SDK:** `@sentry/react-native` ≥ 5.32.0 for basic profiling · ≥ 5.33.0 for JS-only mode · ≥ 7.9.0 (Android) / ≥ 7.12.0 (iOS) for UI Profiling

Profiling samples the call stack at regular intervals to surface hot code paths and slow functions. The React Native SDK profiles both layers of the stack simultaneously: **JavaScript via Hermes** and **native code via platform profilers** (iOS Instruments-style on iOS, Android profiling on Android).

> Profiling requires tracing to be enabled. Only transactions that are sampled for tracing can be profiled.

---

## Table of Contents

1. [How Profiling Works](#1-how-profiling-works)
2. [Basic Setup](#2-basic-setup)
3. [Hermes + Platform Profilers](#3-hermes--platform-profilers)
4. [UI Profiling (Experimental)](#4-ui-profiling-experimental)
5. [What Data Is Captured](#5-what-data-is-captured)
6. [Performance Overhead](#6-performance-overhead)
7. [Expo Compatibility](#7-expo-compatibility)
8. [iOS-Specific Notes](#8-ios-specific-notes)
9. [Android-Specific Notes](#9-android-specific-notes)
10. [Configuration Reference](#10-configuration-reference)
11. [Version Requirements](#11-version-requirements)
12. [Known Limitations](#12-known-limitations)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. How Profiling Works

When a transaction is sampled for profiling, the SDK starts sampling the call stack at a fixed interval for the duration of the transaction. Profiles are then attached to the transaction and uploaded to Sentry alongside it.

### Two-layer profiling

```
Transaction starts
│
├── Hermes profiler ─────── JS stack (your React components, business logic, etc.)
│
└── Platform profilers ──── Native stack (Obj-C/Swift on iOS, Kotlin/Java on Android)
                             Bridge calls, native modules, OS calls visible here
```

Both layers run simultaneously. The Sentry UI merges them into a single flame graph so you can trace a slow operation from JS → bridge → native.

### Sampling relationship

`profilesSampleRate` is **relative to `tracesSampleRate`**, not to all transactions:

```
All transactions
    └── × tracesSampleRate → Traced transactions
             └── × profilesSampleRate → Profiled transactions
```

Example: `tracesSampleRate: 0.2` + `profilesSampleRate: 0.5` → 10% of all transactions are profiled.

---

## 2. Basic Setup

### Minimum configuration

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN",

  // Tracing must be enabled — profiling only applies to traced transactions
  tracesSampleRate: 1.0,

  // profilesSampleRate is relative to tracesSampleRate
  // 1.0 = profile every traced transaction (development / testing only)
  profilesSampleRate: 1.0,
});
```

### Recommended production rates

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 0.2,   // trace 20% of transactions
  profilesSampleRate: 0.5, // profile 50% of those → 10% of all transactions profiled
});
```

> **Production guidance:** Profiling adds overhead (see [Performance Overhead](#6-performance-overhead)). Keep `profilesSampleRate` low in production, especially on lower-end Android devices.

---

## 3. Hermes + Platform Profilers

By default, both Hermes (JS) and native platform profilers run simultaneously. Use `hermesProfilingIntegration` to control this behavior:

### Default: both JS and native (recommended)

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
  // hermesProfilingIntegration is added automatically
  // platformProfilers defaults to true
});
```

### Explicit configuration

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
  integrations: [
    Sentry.hermesProfilingIntegration({
      platformProfilers: true,  // default: true — profile native code alongside Hermes JS
      // Set to false to profile ONLY JavaScript (Hermes), skipping native profiling
      // Useful for isolating JS performance issues or reducing overhead
      // Requires SDK ≥ 5.33.0
    }),
  ],
});
```

### When to disable `platformProfilers`

- Isolating a JS-only performance problem (want only the Hermes flame graph)
- Reducing profiling overhead on lower-end devices
- Debugging JS event loop stalls where native noise is distracting

---

## 4. UI Profiling (Experimental)

Standard profiling is transaction-scoped: it starts and stops with each sampled transaction. **UI Profiling** is continuous — it profiles the entire app session (or from app start), independent of transaction boundaries.

Useful for catching performance issues that span multiple transactions or occur outside instrumented code paths.

> **Experimental feature.** The API is under `_experiments` and may change without a major version bump. Available on Android (SDK ≥ 7.9.0) and iOS (SDK ≥ 7.12.0).

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,

  _experiments: {
    profilingOptions: {
      // Fraction of app sessions to profile (0.0–1.0)
      profileSessionSampleRate: 1.0,

      // "trace" = profile only while a transaction is active
      // (still continuous but gated on active traces)
      lifecycle: "trace",

      // Start profiling from the very first frame (captures cold start behavior)
      startOnAppStart: true,
    },
  },
});
```

> **Migration note:** `androidProfilingOptions` (the previous Android-only experimental flag) is **deprecated**. Use `profilingOptions` inside `_experiments` instead — it covers both platforms.

---

## 5. What Data Is Captured

### In a profile

| Data | Description |
|------|-------------|
| **Call stack samples** | Sampled JS + native stack frames at regular intervals |
| **Flame graph** | Aggregated view of time spent in each function |
| **Timeline** | Stack samples over time, correlated with transaction spans |
| **Thread info** | JS thread, main thread, background threads (native) |
| **Function names** | From JS source maps + native debug symbols |

### What profiles are linked to

Each profile is attached to the transaction that triggered it. In the Sentry UI you can:
- View the flame graph alongside the transaction's span waterfall
- Identify which functions were executing during slow spans
- Click through from a slow span to the corresponding stack samples

### What is NOT captured

- Memory allocations (use Instruments / Android Studio for that)
- Network traffic details (captured separately by tracing spans)
- UI rendering frames (slow/frozen frames are a separate tracing metric)

---

## 6. Performance Overhead

Profiling adds CPU and memory overhead. The Hermes profiler uses a sampling approach (not instrumentation), which keeps overhead lower than full instrumentation-based profilers, but it is not zero.

| Factor | Impact |
|--------|--------|
| Hermes profiler (JS only) | Low — sampling-based, not instrumented |
| Platform profilers (native) | Medium — involves OS-level hooks |
| UI Profiling (continuous) | Higher — always running, not transaction-gated |
| Sample rate in Sentry.init | Linear — 10% profiled = ~10× less overhead than 100% |

**Recommendations:**
- Use `profilesSampleRate: 1.0` only in development/testing
- In production, keep `profilesSampleRate ≤ 0.1` for most apps
- On lower-end Android devices (< 4GB RAM), consider even lower rates
- If using UI Profiling experimentally, keep `profileSessionSampleRate` very low in production (0.01–0.05)

---

## 7. Expo Compatibility

| Feature | Expo Go | Expo (Development Build / EAS Build) |
|---------|---------|--------------------------------------|
| Basic profiling (`profilesSampleRate`) | ❌ Not supported | ✅ Supported |
| Platform profilers (`platformProfilers: true`) | ❌ Not supported | ✅ Supported |
| UI Profiling (experimental) | ❌ Not supported | ✅ Supported |

Profiling requires native modules that are not available in Expo Go. You must use a [Development Build](https://docs.expo.dev/develop/development-builds/introduction/) or a production build via EAS Build.

For Expo projects, make sure the Sentry Expo plugin is configured in your `app.config.js` / `app.json`:

```json
{
  "plugins": [
    [
      "@sentry/react-native/expo",
      {
        "organization": "your-org",
        "project": "your-project"
      }
    ]
  ]
}
```

---

## 8. iOS-Specific Notes

- **Simulator:** Profiling works on the iOS Simulator but native platform profiler results may differ from real device behavior. Always validate on a real device before drawing conclusions.
- **Debug builds:** Symbol names are preserved automatically. Profile data is readable without extra configuration.
- **Release builds:** Native frames will show as addresses without symbols unless you upload dSYM files. Configure the Sentry Xcode build phase to upload dSYMs automatically.
- **Bitcode:** If your project uses bitcode (older setups), ensure dSYMs are downloaded from App Store Connect and uploaded to Sentry — these are the re-compiled symbols, not the ones from your local build.
- **Cold start profiling:** To capture profiling during app cold start (before the first transaction begins), use UI Profiling with `startOnAppStart: true`.

---

## 9. Android-Specific Notes

- **Hermes required:** The JS profiler targets the Hermes engine. JSC (JavaScriptCore) is not supported for JS profiling. Hermes is the default engine for React Native ≥ 0.70 and is required.
- **Release builds:** Native frame symbols require ProGuard/R8 mapping files to be uploaded to Sentry. Configure the Sentry Android Gradle plugin to upload them on each build.
- **Android version:** Platform profiling works on Android 5.0 (API 21) and above — the same minimum as React Native itself.
- **Low-end devices:** Profiling adds measurable overhead on devices with limited RAM or slow CPUs. Test on representative low-end devices before enabling in production.
- **Background processes:** Native platform profilers capture all threads, including those from third-party native libraries. Expect some noise from libraries that run background threads.

---

## 10. Configuration Reference

### `Sentry.init` options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `profilesSampleRate` | `number` (0–1) | `undefined` | Fraction of *traced* transactions to also profile. Relative to `tracesSampleRate`. |
| `tracesSampleRate` | `number` (0–1) | `undefined` | Required for profiling. Fraction of transactions to trace. |

### `hermesProfilingIntegration` options

| Option | Type | Default | SDK Version | Description |
|--------|------|---------|-------------|-------------|
| `platformProfilers` | `boolean` | `true` | ≥ 5.32.0 | Profile native code (Swift/ObjC/Kotlin/Java) alongside Hermes JS. Set `false` for JS-only profiling. |

### `_experiments.profilingOptions` (UI Profiling)

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `profileSessionSampleRate` | `number` (0–1) | — | Fraction of app sessions to profile continuously |
| `lifecycle` | `"trace"` | — | When to profile. Currently only `"trace"` is supported. |
| `startOnAppStart` | `boolean` | `false` | Begin profiling at the very first frame, before any transaction starts |

---

## 11. Version Requirements

| Feature | Min SDK | Platforms |
|---------|---------|-----------|
| `profilesSampleRate` (basic profiling) | `5.32.0` | iOS, Android |
| `platformProfilers: false` (JS-only mode) | `5.33.0` | iOS, Android |
| UI Profiling (experimental) | `7.9.0` (Android) · `7.12.0` (iOS) | iOS, Android |

---

## 12. Known Limitations

- **Expo Go:** Not supported. Requires a native build.
- **JSC engine:** JS profiling only supports Hermes. Projects using JavaScriptCore will not get JS profiles.
- **Web/SSR:** The profiling integration is mobile-only. Do not include `hermesProfilingIntegration` in web bundles.
- **Background transactions:** If a transaction completes in the background (app backgrounded mid-transaction), the profile may be truncated.
- **Profile size limits:** Very long transactions with many stack frames can produce large profiles. Sentry may truncate profiles that exceed server-side size limits. Keep `finalTimeoutMs` reasonable (default: 600,000 ms).
- **JS minification in production:** Hermes profile frame names will show minified names unless JS source maps are uploaded to Sentry. Configure the Sentry Metro plugin.
- **Native symbol resolution:** Native frames show as hex addresses unless dSYMs (iOS) or ProGuard mapping files (Android) are uploaded.
- **Simulator accuracy:** iOS Simulator profiling does not reflect real device performance characteristics, especially for native code. Validate on real devices.
- **UI Profiling API stability:** The `_experiments.profilingOptions` API may change. Pin your SDK version if stability matters.

---

## 13. Troubleshooting

| Issue | Likely Cause | Solution |
|-------|-------------|----------|
| No profiles appearing in Sentry | `profilesSampleRate` not set, or `tracesSampleRate` is `0` or unset | Ensure both are set to `> 0`. Check Sentry DSN is correct. |
| JS frames show as minified names (e.g., `t`, `n`, `r`) | Source maps not uploaded | Configure the Sentry Metro plugin to upload source maps on each build |
| Native frames show as hex addresses | dSYM (iOS) or ProGuard mapping (Android) not uploaded | Configure Sentry Xcode / Gradle plugin to upload symbols |
| Profiling causes visible app slowdown | `profilesSampleRate` too high, or `platformProfilers: true` on slow devices | Reduce `profilesSampleRate`; try `platformProfilers: false` |
| `hermesProfilingIntegration is not a function` | SDK version < 5.32.0 | Upgrade to `@sentry/react-native` ≥ 5.32.0 |
| Profiling not working in Expo Go | Expo Go lacks native modules | Switch to a Development Build or EAS Build |
| UI Profiling config has no effect | Using deprecated `androidProfilingOptions` | Migrate to `_experiments.profilingOptions` |
| Profile data appears but flame graph is mostly "unknown" | Missing both source maps AND native symbols | Upload both source maps and dSYMs/ProGuard files |
| Profiles appear only for some transactions | Expected behavior — `profilesSampleRate` controls the fraction | This is correct. Increase the rate if you want broader coverage. |
| App crashes on startup after adding profiling | Hermes not enabled | Verify Hermes is enabled in your React Native config (it's the default for RN ≥ 0.70) |

---

## Reference: Session Replay

# Session Replay — Sentry React Native SDK

> **Minimum SDK:** `@sentry/react-native` ≥ **6.5.0**  
> **Status:** Generally Available on all Sentry plans  
> **Key difference from web:** Screenshot-based capture, NOT DOM recording

---

## How Mobile Replay Differs from Web Replay

Mobile Session Replay is **fundamentally different** from web replay. Understanding this distinction prevents surprises:

| Dimension | Web Session Replay | Mobile Session Replay |
|---|---|---|
| **Recording method** | DOM serialization (HTML/CSS snapshots) | **Screenshot-based** (native view hierarchy snapshots) |
| **Frame rate** | Variable (mutation-driven, often 60fps) | **~1 frame per second** (screenshot on change) |
| **Fidelity** | Pixel-perfect DOM reconstruction | Compressed video segments from screenshots |
| **Text in replay** | ✅ Selectable, searchable text | ❌ Pixel-only — text is in screenshots |
| **CSS inspection** | ✅ Available | ❌ Not available |
| **Privacy mechanism** | CSS-based DOM masking | **Native-layer pixel masking** |
| **Offline support** | ✅ Both session and error modes | ❌ **Error mode only** (`sessionSampleRate` unsupported offline) |
| **Touch recording** | Full pointer/mouse events | Tap breadcrumbs only (no gesture paths) |
| **Rage clicks** | ✅ Detected | ❌ Not supported |
| **Network bodies** | ✅ Optional capture | ❌ Not captured |
| **Scroll positions** | ✅ Precise | ⚠️ Approximate (from screenshots) |

Mobile replay captures **native view hierarchy snapshots + a screenshot** within the same frame, compresses them into video segments, and streams them to Sentry alongside trace IDs, breadcrumbs, and debug info.

---

## Minimum SDK Versions

| Platform / Feature | Minimum Version |
|---|---|
| React Native (basic replay) | **6.5.0** |
| `maskAllVectors` option | 5.36.0 / 6.3.0+ |
| `Sentry.Mask` / `Sentry.Unmask` components | **6.4.0-beta.1** |
| Manually-initialized native SDK masking | **6.15.1** (Cocoa 8.52.1+) |
| `screenshotStrategy` option (Android) | **7.5.0** |
| `includedViewClasses` / `excludedViewClasses` (iOS) | **7.9.0** |
| iOS native SDK | Cocoa 8.43.0+ |
| Android native SDK | 7.20.0+ |

---

## Installation

No separate package needed — `mobileReplayIntegration()` is bundled in `@sentry/react-native`:

```bash
npm install @sentry/react-native
# or
yarn add @sentry/react-native
```

> **Android bundle size note:** The replay module adds ~40 KB compressed / ~80 KB uncompressed. To exclude it entirely if you don't use replay:
> ```gradle
> // android/build.gradle (root level)
> subprojects {
>   configurations.all {
>     exclude group: 'io.sentry', module: 'sentry-android-replay'
>   }
> }
> ```

---

## Basic Setup

```javascript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN_HERE",

  // Session sampling — set both for comprehensive coverage
  replaysSessionSampleRate: 0.1,   // 10% of ALL sessions recorded immediately
  replaysOnErrorSampleRate: 1.0,   // 100% of sessions where an error occurs

  integrations: [
    Sentry.mobileReplayIntegration(),
  ],
});
```

> **During development:** Use `replaysSessionSampleRate: 1.0` so every session is recorded. Lower it in production while keeping `replaysOnErrorSampleRate: 1.0`.

---

## Sample Rates

### `replaysSessionSampleRate`
- Records the **entire user session** starting from SDK initialization / app foreground entry
- Range: `0.0` – `1.0`
- **Not supported in offline mode**

### `replaysOnErrorSampleRate`
- Only activates when an **error occurs**
- SDK maintains a rolling **1-minute pre-error buffer** in memory
- Captures that buffer + everything after the error, giving you full context
- Range: `0.0` – `1.0`
- ✅ Supported in offline mode — segments stored to disk, sent on reconnect

### Recommended Production Values

| Strategy | `replaysSessionSampleRate` | `replaysOnErrorSampleRate` |
|---|---|---|
| Errors-only (minimal overhead) | `0` | `1.0` |
| Balanced | `0.05` | `1.0` |
| High visibility | `0.1` | `1.0` |

### Per-Error Filtering with `beforeErrorSampling`

```javascript
Sentry.mobileReplayIntegration({
  beforeErrorSampling: (event, hint) => {
    // Only capture replays for UNHANDLED errors
    const isHandled = event.exception?.values?.some(
      (exception) => exception.mechanism?.handled === true,
    );
    return !isHandled; // returning false skips replay capture for this error
  },
})
```

---

## All Configuration Options

### `mobileReplayIntegration()` Options

| Option | Type | Default | Min SDK | Description |
|---|---|---|---|---|
| `maskAllText` | `boolean` | `true` | — | Masks all text in screenshots |
| `maskAllImages` | `boolean` | `true` | — | Masks all images |
| `maskAllVectors` | `boolean` | `true` | 5.36.0 / 6.3.0+ | Masks vector graphics |
| `screenshotStrategy` | `'pixelCopy'` \| `'canvas'` | `'pixelCopy'` | 7.5.0 (Android) | Screenshot capture method |
| `includedViewClasses` | `string[]` | — | 7.9.0 (iOS) | Allowlist of native class names to traverse |
| `excludedViewClasses` | `string[]` | — | 7.9.0 (iOS) | Blocklist; takes precedence over `includedViewClasses` |
| `beforeErrorSampling` | `(event, hint) => boolean` | — | — | Return `false` to skip replay for a specific error |

### Top-Level `Sentry.init()` Options

| Option | Type | Default | Description |
|---|---|---|---|
| `replaysSessionSampleRate` | `number` (0–1) | — | Fraction of all sessions to record |
| `replaysOnErrorSampleRate` | `number` (0–1) | — | Fraction of error sessions to record |
| `replaysSessionQuality` | `'low'` \| `'medium'` \| `'high'` | `'medium'` | Screenshot quality — affects CPU, memory, bandwidth |

---

## Privacy & Masking

> ⚠️ **Production warning:** Always verify your masking config before enabling in production. Default settings aggressively mask everything, but any modifications require thorough testing with your actual app UI. If you discover unmasked PII, open a GitHub issue and disable Session Replay until resolved.

### Default Behavior

The SDK masks **all text, images, vectors, webviews, and user input** by default. Masked areas are replaced with a filled block using the most predominant color of the masked element.

### Disable All Masking

Use only if your app contains absolutely no sensitive data:

```javascript
Sentry.mobileReplayIntegration({
  maskAllText: false,
  maskAllImages: false,
  maskAllVectors: false,
})
```

> Requires SDK **5.36.0** / **6.3.0+**. If using manually initialized native SDKs, requires **6.15.1+** (Cocoa **8.52.1+**).

### `Sentry.Mask` and `Sentry.Unmask` Components

Requires SDK **6.4.0-beta.1+**. These are React Native components for fine-grained, per-screen masking control:

```jsx
import * as Sentry from "@sentry/react-native";

const ProfileScreen = () => (
  <View>
    {/* Unmask non-sensitive sections to see them clearly in replay */}
    <Sentry.Unmask>
      <Text>Welcome back!</Text>             {/* ✅ visible in replay */}
      <Text>Public username: johndoe</Text>  {/* ✅ visible in replay */}
    </Sentry.Unmask>

    {/* Mask sensitive sections regardless of global config */}
    <Sentry.Mask>
      <Text>Credit card: 4111-****-****-1111</Text>  {/* 🔒 masked */}
      <TextInput value={ssn} />                       {/* 🔒 masked */}
    </Sentry.Mask>
  </View>
);
```

### Masking Rules & Priority

**`Sentry.Unmask` only unmasks direct children:**

```jsx
<Sentry.Unmask>
  <Text>
    Unmasked line                {/* ✅ direct child — visible */}
    <Text>Nested text</Text>     {/* 🔒 indirect child — still masked */}
  </Text>
  <Text>Also unmasked</Text>    {/* ✅ direct child — visible */}
</Sentry.Unmask>
```

**`Sentry.Mask` masks ALL descendants:**

```jsx
<Sentry.Mask>
  <Text>
    Masked                      {/* 🔒 */}
    <Text>Also masked</Text>    {/* 🔒 */}
  </Text>
</Sentry.Mask>
```

**`Mask` always wins — `Unmask` cannot override it:**

```jsx
{/* Unmask inside Mask — Mask still wins */}
<Sentry.Mask>
  <Sentry.Unmask>
    <Text>Still masked</Text>   {/* 🔒 Unmask has no effect inside Mask */}
  </Sentry.Unmask>
</Sentry.Mask>

{/* Mask inside Unmask — Mask still takes effect */}
<Sentry.Unmask>
  <Sentry.Mask>
    <Text>Masked</Text>         {/* 🔒 */}
  </Sentry.Mask>
</Sentry.Unmask>
```

### Implementation Notes

- `Mask` and `Unmask` are **native components** on both iOS and Android
- Compatible with both **New Architecture** and **Legacy Architecture**
- They behave as standard React Native `View` components (passthrough layout)

---

## React Native View Flattening — Critical Privacy Gotcha

React Native's [View Flattening](https://reactnative.dev/architecture/view-flattening) optimization removes "Layout Only" views from the native hierarchy — and this **includes your `Mask`/`Unmask` wrappers**.

> ⚠️ **View Flattening may cause `Mask`/`Unmask` to not work as expected, accidentally exposing sensitive data.** Always test masking thoroughly on physical devices before shipping.

**Diagnosis:** If `Sentry.Unmask` isn't unmasking content more than one level deep, check whether the wrapper appears in the actual native view hierarchy (use the React Native Inspector or Xcode View Hierarchy Debugger). If the wrapper is absent, it's been flattened away.

**Mitigation:** Add `collapsable={false}` to prevent flattening of critical mask wrappers:

```jsx
<Sentry.Mask collapsable={false}>
  <Text>Sensitive content</Text>
</Sentry.Mask>
```

---

## Android: Screenshot Strategies

Requires SDK **7.5.0+**. Configured via `screenshotStrategy`:

| | `'pixelCopy'` (default) | `'canvas'` (experimental) |
|---|---|---|
| **API** | Android PixelCopy API | Custom Canvas redraw |
| **Performance** | Lower overhead | Higher overhead |
| **Masking accuracy** | Can have pixel misalignments | Reliable, always correct |
| **Mask options respected** | ✅ Yes | ❌ **No — ignores all options; always masks everything** |
| **When to use** | Default; works for most apps | When masking misalignment is a concern |

```javascript
Sentry.mobileReplayIntegration({
  screenshotStrategy: "canvas",   // or "pixelCopy" (default)
})
```

> **Canvas caveat:** When `screenshotStrategy: "canvas"` is set, `maskAllText`, `maskAllImages`, `maskAllVectors`, and `Sentry.Unmask` are all **ignored**. Everything is always fully masked — no selective unmasking is possible.

---

## iOS: View Hierarchy Traversal

On iOS, the SDK traverses the native view hierarchy to capture screenshots. Some custom or third-party view classes can cause crashes or artifacts during traversal. Use these options (SDK **7.9.0+**) to control which classes are included:

```javascript
Sentry.mobileReplayIntegration({
  // Only traverse these specific native classes
  includedViewClasses: ["UILabel", "UIView", "MyCustomView"],

  // Never traverse these (even if listed in includedViewClasses)
  excludedViewClasses: ["WKWebView", "UIWebView", "ThirdPartyVideoView"],
})
```

**Priority:** `excludedViewClasses` always wins over `includedViewClasses`. Use `excludedViewClasses` to exclude problematic classes one at a time rather than rebuilding a full allowlist.

---

## iOS 26.0 / Liquid Glass — Critical Warning

> 🚨 **Potential PII leak on iOS 26.0+**
>
> Apple's **Liquid Glass** rendering in iOS 26.0 introduces masking vulnerabilities — masked areas may be rendered through the glass effect, potentially revealing content that should be hidden. **Thoroughly test Session Replay on iOS 26+ before enabling in production.** Track the fix at [sentry-cocoa #6390](https://github.com/getsentry/sentry-cocoa/issues/6390).

---

## Touch / Gesture Recording

Touch interactions are recorded as **breadcrumb events** (discrete tap events), not raw gesture streams. The replay UI overlays touch indicators at tap locations.

- **What's captured:** Tap position, tapped view, timestamp
- **What's NOT captured:** Swipe paths, gesture velocity, multi-touch sequences, pressure
- **Display:** Touch indicators overlaid on the replay video at breadcrumb timestamps

---

## Network Request Capture

Network requests are **automatically captured** and displayed in the replay Network panel — no extra configuration needed.

| What's captured | What's NOT captured |
|---|---|
| URL, HTTP method | Request bodies |
| Status code | Response bodies |
| Request duration | Response headers |
| Failed requests (highlighted red) | |

Network capture works via existing Sentry network instrumentation, not replay-specific config. Unlike web replay, there is no way to opt in to body capture for mobile.

---

## What the Replay UI Shows

| Panel | Content |
|---|---|
| **Video** | Compressed screenshot sequence at ~1 fps |
| **Breadcrumbs** | User taps, navigation events, foreground/background transitions, battery/orientation/connectivity changes |
| **Timeline** | Scrubbable view with event markers and zoom |
| **Network** | All network requests; failed ones highlighted in red |
| **Console** | Custom logs, Logcat output (Android), Timber logs |
| **Errors** | All errors in the session linked to Sentry issues |
| **Tags** | OS version, device specs, release, user info, custom tags |
| **Trace** | All distributed traces occurring during the replay |

---

## Performance Overhead

Performance benchmarks on real production apps (Pocket Casts, release builds, 10 iterations).

### iOS (iPhone 14 Pro)

| Metric | SDK Only | SDK + Replay | Delta |
|---|---|---|---|
| FPS | 55 | 53 | **-2 fps** |
| Memory | 102 MB | 121 MB | **+19 MB** |
| CPU | 4% | 13% | **+9%** |
| Cold Startup | 1264.80 ms | 1265 ms | Negligible |
| Network Bandwidth | — | ~10 KB/s | — |

### Android (Pixel 2XL)

| Metric | SDK Only | SDK + Replay | Delta |
|---|---|---|---|
| FPS | 55 | 54 | **-1 fps** |
| Memory | 255 MB | 265 MB | **+10 MB** |
| CPU | 36% | 42% | **+6%** |
| Cold Startup | 1533.35 ms | 1539.55 ms | Negligible |
| Network Bandwidth | — | ~7 KB/s | — |

> ⚠️ **Older devices (iPhone 8 and earlier):** Replay can cause **visible scrolling stutter and dropped frames** during UI animations. Test on your minimum supported device before enabling.

### Reducing Performance Impact

```javascript
Sentry.init({
  replaysSessionSampleRate: 0.05,   // Lower session recording rate
  replaysSessionQuality: "low",     // ← Key setting for performance
  replaysOnErrorSampleRate: 1.0,    // Keep error capture at 100%
  integrations: [Sentry.mobileReplayIntegration()],
});
```

`replaysSessionQuality` options:
- `'low'` — Lower CPU, memory, and bandwidth; reduced screenshot fidelity
- `'medium'` (default) — Balanced
- `'high'` — Best fidelity; highest resource usage

---

## Session Lifecycle

| Event | Effect |
|---|---|
| SDK initializes / app enters foreground | New session starts |
| App goes to background | Session pauses |
| App returns to foreground within **30 seconds** | Same session continues (same `replay_id`) |
| App returns to foreground after **30+ seconds** | New session starts |
| Session reaches **60 minutes** | Session terminates |
| App crashes / closes in background | Session terminates abnormally |

---

## Offline Support

| Mode | Offline Support |
|---|---|
| `replaysOnErrorSampleRate` | ✅ Segments stored to disk, sent on reconnect |
| `replaysSessionSampleRate` | ❌ Not supported — session replays require network |

---

## Error Coverage

Session Replay links replays to all error types:
- ✅ Handled exceptions
- ✅ Unhandled exceptions
- ✅ ANRs (App Not Responding) / App Hangs
- ✅ Native (NDK) crashes

---

## Expo Compatibility

`mobileReplayIntegration()` uses native modules for screenshot capture and the `Mask`/`Unmask` components.

| Environment | Replay Support |
|---|---|
| **Expo Go** | ❌ Native modules not supported — replay will not work |
| **Expo with `expo-dev-client`** | ✅ Supported — development builds include native modules |
| **EAS Build** | ✅ Fully supported |
| **Expo bare workflow** | ✅ Fully supported |

For managed Expo workflow, use `expo-dev-client` or EAS Build — not Expo Go.

---

## Metro Config — Component Names in Replay UI

Enable human-readable React component names in the replay UI (shows `<ProfileCard>` instead of `<View>`):

```js
// metro.config.js
const { getDefaultConfig } = require("@react-native/metro-config");
const { withSentryConfig } = require("@sentry/react-native/metro");

module.exports = withSentryConfig(getDefaultConfig(__dirname), {
  annotateReactComponents: true,
});
```

This works with Hermes builds. The annotation happens at the native layer, not the JS thread.

---

## Known Limitations vs. Web Replay

| Capability | Web Replay | Mobile Replay |
|---|---|---|
| Recording fidelity | DOM-exact reproduction | Screenshot video (~1 fps) |
| Text in replay | ✅ Selectable, searchable | ❌ Pixel-only |
| CSS inspection | ✅ | ❌ |
| Rage click detection | ✅ | ❌ (taps only) |
| Scroll positions | ✅ Precise | ⚠️ Approximate |
| Offline session recording | ✅ | ❌ (error mode only) |
| Canvas / WebGL | ✅ | ⚠️ Captured as screenshot |
| Network request bodies | ✅ Optional | ❌ Not available |
| Unmask → nested children | ✅ All descendants | ⚠️ Direct children only |
| View Flattening interference | N/A | ⚠️ Can remove Mask/Unmask wrappers |
| iOS 26.0 Liquid Glass | N/A | ⚠️ Potential PII leak (unfixed) |
| Android canvas strategy | N/A | ⚠️ Forces all-masked (experimental) |
| Lazy loading | ✅ `Sentry.addIntegration()` | ❌ Must be in `Sentry.init()` |
| DOM mutation tracking | ✅ | ❌ Screenshot-based only |

---

## Production-Ready Setup Example

```javascript
// App entry point (App.tsx / _layout.tsx)
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN_HERE",

  // Replay sampling
  replaysSessionSampleRate: 0.05,     // 5% of all sessions
  replaysOnErrorSampleRate: 1.0,      // 100% of error sessions
  replaysSessionQuality: "medium",    // 'low' | 'medium' | 'high'

  integrations: [
    Sentry.mobileReplayIntegration({
      // Privacy — defaults shown explicitly for clarity
      maskAllText: true,
      maskAllImages: true,
      maskAllVectors: true,

      // Android screenshot strategy (SDK 7.5.0+)
      screenshotStrategy: "pixelCopy",  // or 'canvas' (experimental, always masks)

      // iOS view traversal safety (SDK 7.9.0+)
      excludedViewClasses: ["WKWebView", "UIWebView"],

      // Selective replay — only for unhandled errors
      beforeErrorSampling: (event, hint) => {
        const isHandled = event.exception?.values?.some(
          (exc) => exc.mechanism?.handled === true,
        );
        return !isHandled;
      },
    }),
  ],
});
```

```jsx
// Fine-grained masking in screens
import * as Sentry from "@sentry/react-native";

const PaymentScreen = () => (
  <View>
    {/* Unmask non-sensitive summary info */}
    <Sentry.Unmask>
      <Text>Order Summary</Text>
      <Text>Total: $42.00</Text>
    </Sentry.Unmask>

    {/* Always mask payment details */}
    <Sentry.Mask>
      <TextInput placeholder="Card number" />
      <TextInput placeholder="CVV" />
      <Text>Billing address...</Text>
    </Sentry.Mask>
  </View>
);
```

```js
// metro.config.js — human-readable component names in replay UI
const { getDefaultConfig } = require("@react-native/metro-config");
const { withSentryConfig } = require("@sentry/react-native/metro");

module.exports = withSentryConfig(getDefaultConfig(__dirname), {
  annotateReactComponents: true,
});
```

---

## Quick Reference

```
Minimum RN SDK:        6.5.0
Recording method:      Screenshots (~1 fps), NOT DOM recording
Pre-error buffer:      60 seconds
Session timeout:       30s background / 60 min max
Offline support:       Error mode only
Default masking:       ALL text, images, vectors, webviews — fully masked
Unmask scope:          Direct children only (not descendants)
Mask priority:         Always wins — Unmask cannot override
View flattening:       Can silently remove Mask/Unmask — test thoroughly!
Android strategies:    pixelCopy (default) | canvas (experimental, always-masks)
iOS view safety:       excludedViewClasses / includedViewClasses (SDK 7.9.0+)
iOS 26 warning:        Liquid Glass masking bug — test before production!
Component names:       metro.config.js → annotateReactComponents: true
Quality setting:       low | medium (default) | high
Expo Go:               ❌ Not supported — use expo-dev-client or EAS Build
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Replay not recording at all | Verify `mobileReplayIntegration()` is in the `integrations` array in `Sentry.init()` and sample rates are > 0 |
| All content masked even after setting `maskAllText: false` | Check SDK version ≥ 5.36.0 / 6.3.0+. If using manually initialized native SDK, requires 6.15.1+ (Cocoa 8.52.1+) |
| `Sentry.Mask` / `Sentry.Unmask` not working | Requires SDK 6.4.0-beta.1+. Also check for React Native View Flattening — add `collapsable={false}` to wrapper |
| Sensitive data visible despite masking | View Flattening may have removed `Mask` wrappers. Verify wrapper appears in native view hierarchy. Use `collapsable={false}` |
| Replay works in debug but not production | Confirm sample rates in production config; check DSN is correct for environment |
| Expo Go — replay not working | Expected — native modules not supported in Expo Go. Use `expo-dev-client` or EAS Build |
| Android: masking visually misaligned | Try `screenshotStrategy: "canvas"` — more accurate but everything becomes masked |
| iOS: crash during replay capture | A native class is causing traversal issues. Add it to `excludedViewClasses` (SDK 7.9.0+) |
| High CPU / memory on older devices | Set `replaysSessionQuality: "low"` and lower `replaysSessionSampleRate`. Disable on affected device models if needed |
| Pre-error buffer not appearing | Check available memory — the rolling 60-second buffer is held in RAM. Low-memory devices may truncate it |
| iOS 26: masked content visible through UI | Known Liquid Glass bug — disable Session Replay on iOS 26+ until [sentry-cocoa #6390](https://github.com/getsentry/sentry-cocoa/issues/6390) is resolved |
| Error replay count differs from issue count | Expected — rate limiting, manual deletions, or network failures can cause discrepancies |
| `beforeErrorSampling` not being called | Confirm `replaysOnErrorSampleRate` > 0; the callback only fires when error sampling is active |

---

## Reference: Tracing

# Tracing & Performance Monitoring — Sentry React Native SDK

> **Minimum SDK:** `@sentry/react-native` ≥ 5.20.0 for TTID/TTFD · ≥ 5.32.0 for profiling · ≥ 8.0.0 recommended
> **Mobile-first note:** React Native has unique performance capabilities web SDKs don't provide — cold/warm app start tracking, JS event loop stall detection, slow/frozen frame counting, and navigation-based transactions. All are first-class citizens in the Sentry RN SDK.

---

## Table of Contents

1. [Basic Tracing Setup](#1-basic-tracing-setup)
2. [Automatic Instrumentation Setup](#2-automatic-instrumentation-setup)
3. [App Start Tracing](#3-app-start-tracing)
4. [Navigation Instrumentation](#4-navigation-instrumentation)
5. [Screen Rendering: Time to Display](#5-screen-rendering-time-to-display)
6. [Slow & Frozen Frames](#6-slow--frozen-frames)
7. [Stall Tracking](#7-stall-tracking)
8. [Network Request Tracing](#8-network-request-tracing)
9. [Distributed Tracing](#9-distributed-tracing)
10. [User Interaction Tracing](#10-user-interaction-tracing)
11. [Custom Spans](#11-custom-spans)
12. [React Component Profiler](#12-react-component-profiler)
13. [Profiling (Native + Hermes)](#13-profiling-native--hermes)
14. [Dynamic Sampling](#14-dynamic-sampling)
15. [Configuration Reference](#15-configuration-reference)
16. [Mobile vs Web: Feature Matrix](#16-mobile-vs-web-feature-matrix)
17. [Troubleshooting](#17-troubleshooting)

---

## 1. Basic Tracing Setup

Tracing requires **no additional imports** beyond the standard Sentry import — a key difference from the web SDK.

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN",

  // Option A: uniform sample rate (0.0–1.0)
  // 1.0 = 100% of transactions captured — development/testing only
  tracesSampleRate: 1.0,

  // Option B: dynamic sampler — takes precedence over tracesSampleRate when both are set
  // tracesSampler: ({ name, attributes, parentSampled }) => {
  //   if (name === "checkout") return 1.0;
  //   return 0.2;
  // },
});
```

> **Production recommendation:** Use `tracesSampleRate: 0.2` or lower, or switch to `tracesSampler` for context-aware sampling. 100% sampling causes high volume at scale.

---

## 2. Automatic Instrumentation Setup

`reactNativeTracingIntegration` must be explicitly added to enable automatic tracing features. Two required setup steps:

### Step 1 — Add the integration

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,
  integrations: [
    Sentry.reactNativeTracingIntegration(),
  ],
});
```

### Step 2 — Wrap your root component

Required for accurate App Start measurement (records to first component mount instead of JS initialization) and to enable User Interaction tracing:

```typescript
// App.tsx
export default Sentry.wrap(App);
```

### Opt out of automatic instrumentation

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  enableAutoPerformanceTracing: false, // disables all auto instrumentation
});
```

---

## 3. App Start Tracing

**Unique to mobile.** Tracks the duration from the earliest native process initialization to React Native root component mount.

| Metric | Measurement Key | When it fires |
|---|---|---|
| **Cold start** | `measurements.app_start_cold` | Process launched from scratch (not in memory) |
| **Warm start** | `measurements.app_start_warm` | Process was already in memory, activity recreated |

> **Hot starts and resumes are not tracked.** They're considered too fast to be meaningful for monitoring.

### Why `Sentry.wrap(App)` matters for App Start

Without `Sentry.wrap(App)`, the App Start measurement ends at JS initialization rather than at first component mount. Wrapping is essential for accurate data that represents the real user experience.

### How App Start appears in traces

When a routing integration (React Navigation, Expo Router, RNN) is present, App Start data appears as **spans inside the first navigation transaction** — not as a standalone transaction. You'll see it in the trace waterfall as a child span at the root of the first screen.

### Platform accuracy notes

Sentry follows Apple and Google's official App Start guidelines. Reported values may be slightly longer than other tools, as they're designed to most accurately represent real user experience rather than minimize measured time.

### Optimizing App Start time

Common causes of slow cold starts and how to address them:

```typescript
// ❌ Eager import — executes at bundle parse time
import { HeavyModule } from './heavy-module';

// ✅ Lazy import — deferred until actually needed
const loadHeavy = () => import('./heavy-module');

// ❌ Synchronous AsyncStorage read at startup
const theme = await AsyncStorage.getItem('theme'); // blocks JS thread

// ✅ Use a synchronous-safe default, hydrate later
const [theme, setTheme] = useState('light');
useEffect(() => {
  AsyncStorage.getItem('theme').then(setTheme);
}, []);
```

---

## 4. Navigation Instrumentation

The routing integration determines how navigation events create transactions. Each screen transition becomes a transaction, with the screen name as the transaction name.

### 4a. React Navigation (v5+)

The most common setup. Creates a transaction for every route change automatically.

```typescript
import * as Sentry from "@sentry/react-native";
import {
  NavigationContainer,
  createNavigationContainerRef,
} from "@react-navigation/native";

// Step 1 — Create the integration BEFORE Sentry.init
const navigationIntegration = Sentry.reactNavigationIntegration({
  enableTimeToInitialDisplay: true,             // enable TTID measurement per screen
  routeChangeTimeoutMs: 1_000,                  // discard transaction if screen doesn't mount within 1s
  ignoreEmptyBackNavigationTransactions: true,  // drop back-nav transactions with no child spans
  useDispatchedActionData: true,                // attach action data to transaction metadata
});

// Step 2 — Pass to Sentry.init
Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,
  integrations: [navigationIntegration],
});

// Step 3 — Register the container ref in onReady
function App() {
  const containerRef = createNavigationContainerRef();

  return (
    <NavigationContainer
      ref={containerRef}
      onReady={() => {
        // Must be called inside onReady — not before the container is ready
        navigationIntegration.registerNavigationContainer(containerRef);
      }}
    >
      {/* screens */}
    </NavigationContainer>
  );
}

export default Sentry.wrap(App);
```

### 4b. React Native Navigation (Wix/RNN)

Pass the `Navigation` object directly — no ref or container wrapping needed.

```typescript
import * as Sentry from "@sentry/react-native";
import { Navigation } from "react-native-navigation";

Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,
  integrations: [
    Sentry.reactNativeNavigationIntegration({
      navigation: Navigation,                        // required — the RNN Navigation object
      routeChangeTimeoutMs: 1_000,                   // discard stale transactions
      enableTabsInstrumentation: true,               // create transactions on tab changes (default: false)
      ignoreEmptyBackNavigationTransactions: true,   // drop no-span back navigations
    }),
  ],
});
```

### Customizing transaction names

Transaction names default to the route/screen name (e.g., `LoginScreen`, `HomeTab`). Modify via `beforeStartSpan`:

```typescript
Sentry.reactNativeTracingIntegration({
  beforeStartSpan: (context) => ({
    ...context,
    name: context.name.replace("Screen", ""),  // strip "Screen" suffix for cleaner names
    attributes: {
      ...context.attributes,
      "app.version": "2.1.0",
    },
  }),
}),
```

### Tab navigation

Tab navigators preload screens, so auto-instrumentation only creates a transaction for the **initial** tab visit. For subsequent tab switches, use the `TimeToInitialDisplay` and `TimeToFullDisplay` components explicitly (see §5).

---

## 5. Screen Rendering: Time to Display

Two **Mobile Vitals** that have no web equivalent:

| Metric | Abbreviation | What it measures |
|---|---|---|
| **Time to Initial Display** | TTID | From navigation event → first rendered frame visible after Screen mounts |
| **Time to Full Display** | TTFD | From navigation event → all async content loaded and ready for user interaction |

> **Requirements:** SDK ≥ `5.20.0` · Native build required (not available in Expo Go)

### Automatic TTID (React Navigation only)

Enable in the integration config. TTID spans automatically include animation completion time (except JS-driven animations on iOS, which are excluded).

```typescript
const navigationIntegration = Sentry.reactNavigationIntegration({
  enableTimeToInitialDisplay: true, // that's it
});
```

### Manual TTID override

Use when you need to control exactly when "initial display" is considered complete:

```tsx
import * as Sentry from "@sentry/react-native";
import { View } from "react-native";

function ProductListScreen() {
  return (
    <View>
      <Sentry.TimeToInitialDisplay record={true} />
      {/* content */}
    </View>
  );
}
```

### Time to Full Display (TTFD)

Mark full display when all async content is loaded. The `record` prop fires once when it transitions from `false` to `true`:

```tsx
import * as Sentry from "@sentry/react-native";
import { useState, useEffect } from "react";
import { View, Text, ActivityIndicator } from "react-native";

function ProductDetailScreen({ productId }: { productId: string }) {
  const [product, setProduct] = useState<Product | null>(null);

  useEffect(() => {
    fetch(`https://api.example.com/products/${productId}`)
      .then((res) => res.json())
      .then(setProduct);
  }, [productId]);

  return (
    <View>
      {/* Fires once when product transitions from null to loaded */}
      <Sentry.TimeToFullDisplay record={product !== null} />

      {product ? (
        <Text>{product.name}</Text>
      ) : (
        <ActivityIndicator />
      )}
    </View>
  );
}
```

### Tab screens — explicit TTID + TTFD

Because tab screens are preloaded, auto-detection only fires on the first visit. Add both components explicitly for every tab screen:

```tsx
function HomeTabScreen({ isLoading }: { isLoading: boolean }) {
  return (
    <View>
      <Sentry.TimeToInitialDisplay record={true} />
      <Sentry.TimeToFullDisplay record={!isLoading} />
      {/* content */}
    </View>
  );
}
```

> Both `<TimeToInitialDisplay />` and `<TimeToFullDisplay />` render as `<></>` — **zero visual impact.**

---

## 6. Slow & Frozen Frames

**Mobile Vitals** — automatically captured per transaction when tracing is enabled. No configuration required.

| Frame type | Threshold | User experience |
|---|---|---|
| **Slow frame** | Takes longer than expected for the refresh rate | UI hitches, animation jank |
| **Frozen frame** | Completely unresponsive | App appears hung |

> Web Vitals (LCP, FID, CLS) are **not** reported for React Native — slow/frozen frames are the mobile equivalent.

These appear in the **Mobile Vitals** section of every transaction in Sentry's performance UI, alongside App Start time.

### Android: AndroidX dependency

Sentry uses `androidx.core` for accurate slow/frozen frame detection across all Android versions. It's included automatically. If you explicitly remove it:

```groovy
// android/app/build.gradle — removes androidx.core AND disables frame reporting
api('io.sentry:sentry-android:8.33.0') {
    exclude group: 'androidx.core', module: 'core'
}
```

> **Warning:** Removing `androidx.core` disables slow/frozen frame detection entirely.

---

## 7. Stall Tracking

**Unique to React Native.** A "stall" is when the JavaScript event loop takes longer than expected to process a tick — it directly blocks UI rendering and all JS logic.

Three metrics automatically attached to every transaction:

| Metric | Description |
|---|---|
| **Longest Stall Time** | Duration (ms) of the single longest event loop stall |
| **Total Stall Time** | Combined ms of all stalls during the transaction |
| **Stall Count** | Number of individual stalls |

No configuration needed — stall tracking is enabled automatically by `reactNativeTracingIntegration`.

### What causes stalls

```typescript
// ❌ Synchronous heavy computation on the JS thread — causes stalls
const result = items.reduce((acc, item) => {
  return acc + expensiveComputation(item); // blocks JS thread
}, 0);

// ✅ Offload to InteractionManager or requestAnimationFrame
InteractionManager.runAfterInteractions(() => {
  const result = items.reduce((acc, item) => {
    return acc + expensiveComputation(item);
  }, 0);
  setState(result);
});

// ✅ Or better — move to a native module / worklet (Reanimated)
```

---

## 8. Network Request Tracing

Every `fetch` and `XMLHttpRequest` call made while a transaction is active automatically gets a child span. No code changes needed.

Span data includes:
- HTTP method and URL
- Response status code
- Request/response size
- Duration (time-to-first-byte + total)

### Filter which requests get spans

```typescript
Sentry.reactNativeTracingIntegration({
  shouldCreateSpanForRequest: (url) => {
    // Skip analytics pings and health checks
    return !url.match(/\/(analytics|health|metrics)\/?(\?.*)?$/);
  },
}),
```

### Transaction idle and final timeouts

```typescript
Sentry.reactNativeTracingIntegration({
  idleTimeoutMs: 1_000,    // end transaction after 1s of inactivity (default: 1000)
  finalTimeoutMs: 600_000, // hard cap: 10 minutes max transaction duration (default: 600000)
}),
```

---

## 9. Distributed Tracing

Connects mobile traces to backend traces so you can see the full request lifecycle — from the user's tap to database query and back.

### How it works

When a `fetch` request fires inside a transaction, the SDK attaches two headers:

| Header | Purpose |
|---|---|
| `sentry-trace` | Carries the trace ID and span ID |
| `baggage` | Carries sampling decision and trace metadata |

Your backend Sentry SDK reads these headers and links its spans to the same trace, so you see one unified waterfall in Sentry.

### `tracePropagationTargets` — control where headers attach

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,

  // Default on mobile: [/.*/] — attaches to ALL outgoing requests
  // Restrict to your own APIs:
  tracePropagationTargets: [
    "api.myapp.com",             // string — matched against the full URL
    /^https:\/\/api\./,          // regex — matched against the full URL
    "localhost",                 // useful for local development
  ],
});
```

> **Important:** `tracePropagationTargets` matches against the **entire URL string**, not just the domain.

### CORS requirements for web APIs

If your React Native app calls web APIs that run CORS preflight checks, the backend must allow the Sentry headers:

```
Access-Control-Allow-Headers: sentry-trace, baggage
```

Without this, browsers (and React Native on web) will reject the preflight and the request will fail.

### End-to-end example: RN → Node.js API

```typescript
// React Native — starts the trace
await Sentry.startSpan({ name: "addToCart", op: "ui.action" }, async () => {
  // This fetch will carry sentry-trace + baggage headers to api.myapp.com
  const response = await fetch("https://api.myapp.com/cart/items", {
    method: "POST",
    body: JSON.stringify({ productId: "abc-123" }),
  });
  return response.json();
});

// Node.js backend (with @sentry/node) — automatically continues the trace
// The backend span appears as a child in the same trace waterfall
```

```python
# Python backend (with sentry-sdk) — also continues the trace automatically
# No extra code needed beyond standard Sentry initialization
```

---

## 10. User Interaction Tracing

Captures transactions and breadcrumbs for touch events. Transaction names are automatically composed as `ScreenName > element_label`.

### Enable

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  enableUserInteractionTracing: true, // disabled by default
  tracesSampleRate: 1.0,
  integrations: [navigationIntegration],
});

// Wrapping is required for interaction tracing to work
export default Sentry.wrap(App);

// Or with a custom label prop name:
export default Sentry.wrap(App, {
  touchEventBoundaryProps: { labelName: "tracking-id" }, // defaults to "sentry-label"
});
```

### Label interactive elements

```tsx
// Without a label, no transaction is created — the tap is silently ignored
<Pressable
  sentry-label="add_to_cart_button"
  onPress={handleAddToCart}
>
  <Text>Add to Cart</Text>
</Pressable>

// Also works on TouchableOpacity, TouchableHighlight, etc.
<TouchableOpacity sentry-label="checkout_button" onPress={handleCheckout}>
  <Text>Checkout</Text>
</TouchableOpacity>
```

> Transactions with no child spans are automatically dropped — only meaningful interactions are recorded.

### Custom span attributes on interactions (experimental)

```tsx
<Pressable
  sentry-label="checkout"
  sentry-span-attributes={{
    "user.plan": userPlan,         // string
    "cart.item_count": itemCount,  // number
    "cart.has_coupon": hasCoupon,  // boolean
  }}
  onPress={handleCheckout}
>
  <Text>Checkout</Text>
</Pressable>
```

> `sentry-span-attributes` is **experimental** — API may change. The SDK traverses the component tree to find it, so it can be placed on a parent element.

### Gesture Handler (RNGH v2)

```tsx
import { Gesture, GestureDetector } from "react-native-gesture-handler";
import { sentryTraceGesture } from "@sentry/react-native";

function ZoomableImage() {
  const pinch = Gesture.Pinch();
  const longPress = Gesture.LongPress();

  const gesture = Gesture.Race(
    sentryTraceGesture("pinch-to-zoom", pinch),       // label must be unique per screen
    sentryTraceGesture("long-press-cancel", longPress),
  );

  return (
    <GestureDetector gesture={gesture}>
      <Image source={imageSource} />
    </GestureDetector>
  );
}
```

> Only RNGH **API v2** is supported. Both transactions and breadcrumbs are created automatically.

---

## 11. Custom Spans

```typescript
import * as Sentry from "@sentry/react-native";
```

### `startSpan` — Active, auto-ending (recommended)

The span becomes the active parent for any child spans created inside the callback. Ends automatically when the callback resolves (sync or async).

```typescript
// Synchronous
const total = Sentry.startSpan({ name: "computeCartTotal", op: "function" }, () => {
  return items.reduce((sum, item) => sum + item.price, 0);
});

// Async
const data = await Sentry.startSpan(
  { name: "fetchUserProfile", op: "http.client" },
  async () => {
    const res = await fetch("https://api.example.com/profile");
    return res.json();
  }
);

// Nested — child spans automatically attach to their enclosing parent
await Sentry.startSpan({ name: "checkout", op: "function" }, async () => {
  await Sentry.startSpan({ name: "validateCart", op: "function" }, validateCart);
  await Sentry.startSpan({ name: "processPayment", op: "function" }, processPayment);
  await Sentry.startSpan({ name: "sendConfirmation", op: "http.client" }, sendEmail);
});
```

### `startSpanManual` — Active, manually ended

Use when the span lifetime doesn't map cleanly to a function scope (e.g., spans across event callbacks):

```typescript
function trackAnimationPerformance() {
  return Sentry.startSpanManual({ name: "heroAnimation", op: "ui.render" }, (span) => {
    const animation = Animated.timing(translateY, { toValue: 0, duration: 300, useNativeDriver: true });
    animation.start(({ finished }) => {
      span.setAttribute("animation.completed", finished);
      span.end(); // must call end() manually
    });
  });
}
```

### `startInactiveSpan` — Inactive, manually ended

Inactive spans never become automatic parents for child spans. Use for fire-and-forget measurements:

```typescript
// Start a background sync span without it affecting the current active span
const syncSpan = Sentry.startInactiveSpan({ name: "backgroundSync", op: "function" });

await syncLocalDatabase();

syncSpan.end();
```

### Span options

| Option | Type | Description |
|---|---|---|
| `name` | `string` | **Required.** Display name in Sentry UI |
| `op` | `string` | Operation type — use standard values for enhanced UI (see below) |
| `attributes` | `Record<string, string \| number \| boolean \| array>` | Key/value metadata attached to the span |
| `startTime` | `number` | Custom start timestamp (Unix epoch, seconds) |
| `parentSpan` | `Span` | Explicit parent — overrides the active span |
| `onlyIfParent` | `boolean` | Skip this span if there's no active parent |
| `forceTransaction` | `boolean` | Force the span to appear as a top-level transaction in the UI |

### Standard operation types for mobile

Using well-known `op` values unlocks enhanced Sentry UI features (grouping, filtering, icons):

```typescript
Sentry.startSpan({ name: "GET /api/products",     op: "http.client"  }, fetchProducts);
Sentry.startSpan({ name: "SELECT * FROM users",   op: "db"           }, queryDatabase);
Sentry.startSpan({ name: "parseProductData",      op: "function"     }, parseData);
Sentry.startSpan({ name: "HomeScreen render",     op: "ui.render"    }, render);
Sentry.startSpan({ name: "readProductsCache",     op: "file.read"    }, readCache);
Sentry.startSpan({ name: "writeOrdersCache",      op: "file.write"   }, writeCache);
```

Full operation list: [develop.sentry.dev/sdk/performance/span-operations](https://develop.sentry.dev/sdk/performance/span-operations/#list-of-operations)

### Adding attributes

```typescript
// At creation time
await Sentry.startSpan(
  {
    name: "loadFeed",
    op: "http.client",
    attributes: {
      "feed.type": "following",
      "feed.page": 1,
      "feed.has_cache": false,
    },
  },
  loadFeed
);

// On an existing span
const span = Sentry.getActiveSpan();
if (span) {
  span.setAttribute("result.count", 42);
  span.setAttributes({ "filter.applied": true, "filter.type": "category" });
  span.updateName("loadFeed:following"); // rename mid-flight
}
```

### Span utilities

```typescript
// Get the currently active span
const activeSpan = Sentry.getActiveSpan();

// Get the root span (the transaction) from any span
const rootSpan = activeSpan ? Sentry.getRootSpan(activeSpan) : undefined;

// Explicitly set a span as the active parent for a block
const parent = Sentry.startInactiveSpan({ name: "parent" });
Sentry.withActiveSpan(parent, () => {
  Sentry.startSpan({ name: "child" }, () => { /* child attaches to parent */ });
});

// Create a root-level span regardless of current context
Sentry.withActiveSpan(null, () => {
  Sentry.startSpan({ name: "isolated" }, () => { /* no parent */ });
});

// Prevent a specific operation from creating spans
Sentry.suppressTracing(() => {
  fetch("https://analytics.internal/ping"); // no span created for this request
});
```

### Span hierarchy: flat vs. nested

By default (mobile and browser environments), all spans are flat children of the root transaction to avoid async parent misattribution:

```typescript
// Default behavior — both fetches become siblings under the root, not children of their span
await Sentry.startSpan({ name: "span1" }, async () => {
  await fetch("https://api.example.com/a"); // child of root transaction
});
await Sentry.startSpan({ name: "span2" }, async () => {
  await fetch("https://api.example.com/b"); // child of root transaction
});

// Opt into full nesting (may cause incorrect parent attribution with async/await)
Sentry.init({ parentSpanIsAlwaysRootSpan: false });
```

---

## 12. React Component Profiler

Track individual React component lifecycle (mount, update, unmount) as child spans within the current route transaction. Useful for identifying slow renders and unnecessary re-renders.

```typescript
import * as Sentry from "@sentry/react-native";

// Wrap any component with withProfiler
const ProductCard = Sentry.withProfiler(({ product }) => {
  return <View>{/* component content */}</View>;
});

// Or wrap the export
export default Sentry.withProfiler(HeavyListScreen);
```

Profiler spans show up in the transaction waterfall under `ui.react.render` and `ui.react.update` operations.

> **Production builds warning:** React Native minifies class/function names in production. Configure the Sentry Gradle/Xcode plugin + source maps to preserve component names in production profiler data. See the SDK [source maps guide](https://docs.sentry.io/platforms/react-native/sourcemaps/).

---

## 13. Profiling (Native + Hermes)

Profiling samples the call stack at regular intervals to surface hot code paths. Requires tracing to be enabled first — only traced transactions are profiled.

**Minimum SDK version:** `5.32.0`

### Basic setup

`profilesSampleRate` is **relative to `tracesSampleRate`** — a transaction must first be sampled for tracing before profiling applies:

```typescript
Sentry.init({
  dsn: "YOUR_DSN",

  tracesSampleRate: 1.0,    // 100% traced
  profilesSampleRate: 1.0,  // 100% of traced → 100% profiled (dev/testing only)

  // Production example:
  // tracesSampleRate: 0.2,    // 20% traced
  // profilesSampleRate: 0.5,  // 50% of those → 10% of all transactions profiled
});
```

### Hermes + native platform profilers

By default both layers are profiled simultaneously:

1. **Hermes profiler** — JavaScript code executing in the Hermes engine
2. **Platform profilers** — native code (Swift/ObjC on iOS, Kotlin/Java on Android)

Control with `hermesProfilingIntegration`:

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,
  profilesSampleRate: 1.0,
  integrations: [
    Sentry.hermesProfilingIntegration({
      platformProfilers: true,  // default: true — profile native code alongside JS
      // Set false to profile ONLY JS (Hermes) without native code (SDK ≥ 5.33.0)
    }),
  ],
});
```

### UI Profiling (experimental)

Continuous profiling tied to the app lifecycle rather than individual transactions. Useful for catching performance issues that span multiple transactions.

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  tracesSampleRate: 1.0,

  _experiments: {
    profilingOptions: {
      profileSessionSampleRate: 1.0,  // fraction of app sessions to profile
      lifecycle: "trace",             // "trace" = profile only during active transactions
      startOnAppStart: true,          // begin profiling from the very first frame
    },
  },
});
```

> `androidProfilingOptions` is **deprecated** — use `profilingOptions` inside `_experiments` instead.

### Profiling version requirements

| Feature | Min SDK | Platforms |
|---|---|---|
| `profilesSampleRate` (basic) | `5.32.0` | iOS, Android |
| `platformProfilers: false` | `5.33.0` | iOS, Android |
| UI Profiling (experimental) | `7.9.0` (Android) · `7.12.0` (iOS) | iOS, Android |

---

## 14. Dynamic Sampling

`tracesSampler` gives you full control over sampling based on transaction properties at the time the trace starts.

```typescript
Sentry.init({
  dsn: "YOUR_DSN",

  tracesSampler: ({ name, attributes, parentSampled }) => {
    // Always sample critical user flows
    if (name === "checkout" || name === "PaymentScreen") {
      return 1.0;
    }

    // Never sample health checks
    if (name.includes("HealthCheck")) {
      return 0;
    }

    // Respect parent sampling decision for distributed traces
    // (keeps frontend + backend in the same trace or both dropped)
    if (parentSampled !== undefined) {
      return parentSampled ? 1.0 : 0;
    }

    // Default: sample 10%
    return 0.1;
  },
});
```

### Head-based vs. tail-based sampling

| Approach | How | Tradeoff |
|---|---|---|
| **Head-based** (`tracesSampleRate` / `tracesSampler`) | Decision made at trace start | Low overhead, but can't sample based on outcome |
| **Tail-based** (Sentry Dynamic Sampling rules) | Decision made server-side after trace completes | Can prioritize errors/slow traces, requires Sentry Business plan |

For most React Native apps, head-based sampling with a `tracesSampler` is sufficient.

---

## 15. Configuration Reference

### `Sentry.init` options

| Option | Type | Default | Description |
|---|---|---|---|
| `tracesSampleRate` | `number` (0–1) | `undefined` | Uniform transaction sample rate |
| `tracesSampler` | `function` | `undefined` | Dynamic sampler — overrides `tracesSampleRate` when set |
| `profilesSampleRate` | `number` (0–1) | `undefined` | Profile sample rate, relative to traced transactions |
| `tracePropagationTargets` | `(string \| RegExp)[]` | `[/.*/]` on mobile | URLs/patterns that receive `sentry-trace` + `baggage` headers |
| `enableUserInteractionTracing` | `boolean` | `false` | Capture touch interaction transactions |
| `enableAutoPerformanceTracing` | `boolean` | `true` | Master switch for all automatic instrumentation |
| `parentSpanIsAlwaysRootSpan` | `boolean` | `true` | Flat span hierarchy — safe for async/await contexts |

### `reactNativeTracingIntegration` options

| Option | Type | Default | Description |
|---|---|---|---|
| `beforeStartSpan` | `(context) => context` | — | Mutate span context before each navigation/pageload span |
| `shouldCreateSpanForRequest` | `(url) => boolean` | — | Filter which outgoing requests get a span |
| `idleTimeoutMs` | `number` | `1_000` | Ms of inactivity before ending the current transaction |
| `finalTimeoutMs` | `number` | `600_000` | Hard maximum duration for any single transaction |

### `reactNavigationIntegration` options

| Option | Type | Default | Description |
|---|---|---|---|
| `enableTimeToInitialDisplay` | `boolean` | `false` | Auto-measure TTID per screen |
| `routeChangeTimeoutMs` | `number` | `1_000` | Discard transaction if screen doesn't mount within this time |
| `ignoreEmptyBackNavigationTransactions` | `boolean` | `true` | Drop back-nav transactions with no child spans |
| `useDispatchedActionData` | `boolean` | `false` | Include navigation action data in transaction metadata |

### `reactNativeNavigationIntegration` options (Wix RNN)

| Option | Type | Default | Description |
|---|---|---|---|
| `navigation` | `Navigation` | **required** | The RNN Navigation object |
| `routeChangeTimeoutMs` | `number` | `1_000` | Discard stale transactions |
| `enableTabsInstrumentation` | `boolean` | `false` | Create transactions on tab switches |
| `ignoreEmptyBackNavigationTransactions` | `boolean` | `true` | Drop no-span back navigations |

### `hermesProfilingIntegration` options

| Option | Type | Default | Description |
|---|---|---|---|
| `platformProfilers` | `boolean` | `true` | Profile native (Swift/ObjC/Kotlin/Java) alongside Hermes JS |

---

## 16. Mobile vs Web: Feature Matrix

| Capability | Web SDK | React Native SDK |
|---|---|---|
| App cold start tracking | ❌ | ✅ `measurements.app_start_cold` |
| App warm start tracking | ❌ | ✅ `measurements.app_start_warm` |
| Slow frames (Mobile Vital) | ❌ | ✅ Auto (requires `reactNativeTracingIntegration`) |
| Frozen frames (Mobile Vital) | ❌ | ✅ Auto (requires `reactNativeTracingIntegration`) |
| JS event loop stall tracking | ❌ | ✅ Auto (3 metrics: count, longest, total) |
| Time to Initial Display (TTID) | ❌ | ✅ `enableTimeToInitialDisplay: true` |
| Time to Full Display (TTFD) | ❌ | ✅ `<Sentry.TimeToFullDisplay record={...} />` |
| Touch interaction tracing | ❌ | ✅ `enableUserInteractionTracing: true` |
| Gesture tracing (RNGH v2) | ❌ | ✅ `sentryTraceGesture()` |
| Hermes JS profiling | ❌ | ✅ `profilesSampleRate` + `hermesProfilingIntegration` |
| Native platform profiling | ❌ | ✅ `platformProfilers: true` |
| Navigation transactions | ✅ (SPA routers) | ✅ React Navigation · Expo Router · RNN |
| Network span tracing | ✅ | ✅ fetch + XHR auto-instrumented |
| Distributed tracing | ✅ | ✅ `tracePropagationTargets` |
| Web Vitals (LCP, FID, CLS) | ✅ | ❌ (replaced by Mobile Vitals) |

---

## 17. Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| No transactions in Sentry | Tracing not enabled | Add `tracesSampleRate` > 0 and `reactNativeTracingIntegration()` to `integrations` |
| App Start span missing | `Sentry.wrap(App)` not used | Wrap root component: `export default Sentry.wrap(App)` |
| App Start time seems too long | Sentry follows platform vendor guidelines | Expected — Sentry measures the full user-perceptible start time, not internal JS init |
| Navigation transactions not created | Integration not registered | Call `navigationIntegration.registerNavigationContainer(ref)` inside `onReady`, not before |
| TTID/TTFD not appearing | Feature not enabled or wrong SDK version | Requires `enableTimeToInitialDisplay: true` and SDK ≥ 5.20.0, native build required |
| TTID not firing on tab screens | Tab screens are preloaded | Add `<Sentry.TimeToInitialDisplay record={true} />` explicitly to each tab screen |
| No interaction transactions | Missing `sentry-label` prop | Add `sentry-label="my_button"` to every interactive element you want to track |
| `sentry-trace` header missing from requests | `tracePropagationTargets` doesn't match URL | Check the full URL against your patterns — it matches against the entire URL string |
| Backend receives header but trace not linked | Backend SDK not initialized | Ensure your backend uses a Sentry SDK with distributed tracing support |
| Slow/frozen frames missing on Android | Missing `androidx.core` | Don't exclude `androidx.core` from the Sentry Android dependency |
| Profiling data not appearing | Profiling sample rate is 0 or traces not sampled | `profilesSampleRate` is relative to `tracesSampleRate` — both must be > 0 |
| Component names minified in profiler | Production bundle minification | Configure Sentry Gradle/Xcode plugins and upload source maps |
| Gesture spans not appearing | Wrong RNGH version | Only RNGH API v2 is supported — upgrade `react-native-gesture-handler` |
| Stall metrics missing | `reactNativeTracingIntegration` not added | Stall tracking requires the integration — add it to `integrations: []` |
| Transactions never finish | No idle timeout / long background spans | Adjust `idleTimeoutMs` in `reactNativeTracingIntegration` options |

---

## Reference: User Feedback

# User Feedback — Sentry React Native SDK

> **Minimum SDK:** `@sentry/react-native` ≥6.5.0 for `captureFeedback()` API  
> **Feedback widget** (`showFeedbackWidget`, `feedbackIntegration`): ≥6.9.0  
> **Self-hosted Sentry:** ≥24.4.2 required for full user feedback functionality  
> **New Architecture (Fabric):** Feedback widget requires React Native ≥0.71+

---

## Overview

Sentry provides three complementary approaches to collecting user feedback in React Native:

| Approach | When to Use |
|----------|-------------|
| **Feedback Widget** | Built-in modal; minimal code; works out of the box |
| **`FeedbackWidget` component** | Embed feedback form inline within your own screen |
| **`captureFeedback()` API** | Full control; build your own UI and submit programmatically |

All approaches support:
- Linking feedback to specific error events via `associatedEventId`
- Offline caching (stored on-device, sent when connectivity restores)
- Session Replay integration (buffers last 60 seconds of activity with submitted feedback)

---

## Prerequisites

Wrap your root component with `Sentry.wrap` — this is **required** for the feedback widget and error boundary integration:

```typescript
import * as Sentry from "@sentry/react-native";

export default Sentry.wrap(App);
```

Without `Sentry.wrap`, `Sentry.showFeedbackWidget()` and `Sentry.showFeedbackButton()` will not function correctly.

---

## Approach 1: Built-In Feedback Widget

The simplest integration. Call `Sentry.showFeedbackWidget()` from anywhere — a button, menu item, shake gesture handler, or support screen.

### Trigger the Widget

```typescript
import * as Sentry from "@sentry/react-native";
import { Button } from "react-native";

function SupportButton() {
  return (
    <Button
      title="Report a Problem"
      onPress={() => Sentry.showFeedbackWidget()}
    />
  );
}
```

### Persistent Feedback Button

Show or hide the built-in floating feedback button:

```typescript
// Show the floating feedback button (persists on screen)
Sentry.showFeedbackButton();

// Hide it when no longer needed
Sentry.hideFeedbackButton();
```

### Configure the Widget via `feedbackIntegration`

Customize appearance and fields in `Sentry.init`:

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.init({
  dsn: "YOUR_DSN",
  integrations: [
    Sentry.feedbackIntegration({
      // Field placeholder text
      namePlaceholder: "Full Name",
      emailPlaceholder: "your@email.com",
      messagePlaceholder: "What went wrong? What did you expect?",

      // Field labels
      nameLabel: "Name",
      emailLabel: "Email",
      messageLabel: "Description",
      submitButtonLabel: "Send Report",
      cancelButtonLabel: "Cancel",
      formTitle: "Report a Bug",

      // Require fields (all optional by default)
      isNameRequired: false,
      isEmailRequired: false,

      // Styling
      styles: {
        submitButton: {
          backgroundColor: "#6a1b9a",
        },
      },

      // Pre-fill from current user context (reads Sentry user scope)
      useSentryUser: {
        name: "username",   // maps user.username → name field
        email: "email",     // maps user.email → email field
      },
    }),
  ],
});
```

### Architecture Requirements

| Architecture | Support |
|---|---|
| Legacy (Bridge) | ✅ Fully supported |
| New Architecture (Fabric) | ✅ Requires React Native ≥0.71 |

---

## Approach 2: `FeedbackWidget` Component

Embed the feedback form directly into your own screen layout instead of showing it as a modal:

```typescript
import { FeedbackWidget } from "@sentry/react-native";
import { View, Text, StyleSheet } from "react-native";

function SupportScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Having trouble?</Text>
      <Text style={styles.subtext}>
        Describe what happened and we'll look into it.
      </Text>
      <FeedbackWidget />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
  heading: { fontSize: 20, fontWeight: "bold", marginBottom: 8 },
  subtext: { color: "#666", marginBottom: 16 },
});
```

The `FeedbackWidget` component respects the same configuration set in `feedbackIntegration` within `Sentry.init`.

---

## Approach 3: Programmatic API (`captureFeedback`)

Build a completely custom feedback UI and submit via the SDK. Gives full control over form layout, validation, and submission flow.

### Basic Feedback (Standalone)

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.captureFeedback({
  name: "Jane Smith",
  email: "jane@example.com",
  message: "The checkout button doesn't respond after the first tap.",
});
```

### Link Feedback to a Specific Error Event

```typescript
import * as Sentry from "@sentry/react-native";

// Capture an error and get its ID
const eventId = Sentry.captureException(new Error("Payment failed"));

// Associate the user's report with that exact error
Sentry.captureFeedback({
  name: "John Doe",
  email: "john@example.com",
  message: "App crashed when I tapped Pay Now.",
  associatedEventId: eventId,
});
```

### Link Feedback to the Most Recent Event

`Sentry.lastEventId()` retrieves the ID of the last event captured in the current session — useful for post-crash feedback flows:

```typescript
import * as Sentry from "@sentry/react-native";

const lastId = Sentry.lastEventId();

if (lastId) {
  Sentry.captureFeedback({
    name: user.name,
    email: user.email,
    message: feedbackText,
    associatedEventId: lastId,
  });
}
```

### Feedback with Tags and Attachments

```typescript
import * as Sentry from "@sentry/react-native";

Sentry.captureFeedback(
  {
    name: user.displayName,
    email: user.email,
    message: feedbackText,
  },
  {
    captureContext: {
      tags: {
        screen: currentScreen,
        appVersion: appVersion,
        platform: Platform.OS,
      },
    },
    attachments: [
      {
        filename: "device_info.txt",
        data: JSON.stringify(deviceInfo, null, 2),
        contentType: "text/plain",
      },
    ],
  }
);
```

---

## Crash Report Modal (Post-Crash Feedback)

Show a feedback form on the next app launch after a crash. This is the recommended pattern for collecting context around hard crashes that the user survived.

### Pattern: Check for Last Event on Launch

```typescript
import * as Sentry from "@sentry/react-native";
import React from "react";
import { Modal, View, Text, TextInput, Button } from "react-native";

function App() {
  const [showFeedback, setShowFeedback] = React.useState(false);
  const [feedbackText, setFeedbackText] = React.useState("");
  const lastEventId = React.useRef<string | undefined>(undefined);

  React.useEffect(() => {
    // Check if there was a crash in the previous session
    const eventId = Sentry.lastEventId();
    if (eventId) {
      lastEventId.current = eventId;
      setShowFeedback(true);
    }
  }, []);

  function submitCrashFeedback() {
    if (!feedbackText.trim()) return;

    Sentry.captureFeedback({
      message: feedbackText,
      associatedEventId: lastEventId.current,
    });

    setShowFeedback(false);
    setFeedbackText("");
  }

  return (
    <>
      <Modal visible={showFeedback} transparent animationType="slide">
        <View style={{ flex: 1, justifyContent: "center", padding: 24 }}>
          <Text style={{ fontSize: 18, fontWeight: "bold", marginBottom: 8 }}>
            It looks like the app crashed
          </Text>
          <Text style={{ color: "#555", marginBottom: 16 }}>
            What were you doing when it happened?
          </Text>
          <TextInput
            multiline
            value={feedbackText}
            onChangeText={setFeedbackText}
            placeholder="Describe what happened..."
            style={{
              borderWidth: 1,
              borderColor: "#ccc",
              borderRadius: 8,
              padding: 12,
              minHeight: 100,
              marginBottom: 16,
            }}
          />
          <Button title="Send Report" onPress={submitCrashFeedback} />
          <Button title="Skip" onPress={() => setShowFeedback(false)} />
        </View>
      </Modal>
      {/* rest of app */}
    </>
  );
}
```

> **Tip:** `Sentry.lastEventId()` returns the ID of the most recent event captured during the *current* app session. For post-crash context, call it at app start before any other Sentry calls that might create a new event.

---

## Linking Feedback to Errors via `ErrorBoundary`

The `Sentry.ErrorBoundary` component can automatically show a feedback dialog after capturing a React render error, using the `showDialog` prop:

```typescript
import * as Sentry from "@sentry/react-native";
import { Text } from "react-native";

function App() {
  return (
    <Sentry.ErrorBoundary
      fallback={<Text>Something went wrong. Your report has been sent.</Text>}
      showDialog  // Opens Sentry feedback widget after capturing the error
    >
      <MainContent />
    </Sentry.ErrorBoundary>
  );
}
```

### Custom Post-Error Feedback Form

For full control, use `onError` to capture the `eventId` and trigger your own feedback form:

```typescript
import * as Sentry from "@sentry/react-native";
import React from "react";
import { View, Text, TextInput, Button } from "react-native";

function ErrorFallback({ eventId, onReset }: { eventId: string; onReset: () => void }) {
  const [message, setMessage] = React.useState("");

  function submit() {
    Sentry.captureFeedback({
      message,
      associatedEventId: eventId,
    });
    onReset();
  }

  return (
    <View style={{ padding: 24 }}>
      <Text style={{ fontSize: 18, fontWeight: "bold" }}>Oops, something broke</Text>
      <TextInput
        multiline
        value={message}
        onChangeText={setMessage}
        placeholder="What were you trying to do?"
        style={{ borderWidth: 1, borderColor: "#ccc", padding: 12, marginVertical: 16 }}
      />
      <Button title="Send Feedback" onPress={submit} />
    </View>
  );
}

function App() {
  const [errorEventId, setErrorEventId] = React.useState<string | null>(null);

  return (
    <Sentry.ErrorBoundary
      onError={(_error, _componentStack, eventId) => {
        setErrorEventId(eventId);
      }}
      fallback={
        errorEventId
          ? <ErrorFallback eventId={errorEventId} onReset={() => setErrorEventId(null)} />
          : <Text>Something went wrong.</Text>
      }
    >
      <MainContent />
    </Sentry.ErrorBoundary>
  );
}
```

---

## Screenshots in Feedback

Allow users to attach screenshots to feedback reports. Use `attachments` in `captureFeedback` to include screenshots captured from the device:

```typescript
import * as Sentry from "@sentry/react-native";
import { captureScreen } from "react-native-view-shot"; // npm install react-native-view-shot
import RNFS from "react-native-fs"; // npm install react-native-fs

async function submitFeedbackWithScreenshot(feedbackMessage: string) {
  // Capture current screen as PNG
  const screenshotUri = await captureScreen({ format: "png", quality: 0.8 });
  const screenshotBase64 = await RNFS.readFile(screenshotUri, "base64");

  Sentry.captureFeedback(
    {
      message: feedbackMessage,
      associatedEventId: Sentry.lastEventId(),
    },
    {
      attachments: [
        {
          filename: "screenshot.png",
          data: screenshotBase64,
          contentType: "image/png",
        },
      ],
    }
  );
}
```

> **Alternative:** Enable `attachScreenshot: true` in `Sentry.init` to automatically attach a screenshot to every error event — the screenshot then appears alongside any feedback linked to that event via `associatedEventId`.

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  attachScreenshot: true, // Auto-attach screenshot to every error event
});
```

---

## Session Replay Integration with Feedback

When `mobileReplayIntegration()` is enabled and a user submits feedback via the widget, Sentry automatically buffers and attaches **up to 60 seconds of prior session replay** to the feedback submission. This gives you visual context for what the user experienced before they filed the report — no extra code required.

```typescript
Sentry.init({
  dsn: "YOUR_DSN",
  replaysOnErrorSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  integrations: [
    Sentry.mobileReplayIntegration(),
    Sentry.feedbackIntegration(), // replay attaches automatically on feedback submit
  ],
});
```

---

## Offline Feedback

Feedback captured while the device is offline is **automatically cached on-device** by the native SDK layer and replayed to Sentry when connectivity is restored. This applies to all three approaches (`showFeedbackWidget`, `FeedbackWidget`, `captureFeedback`). No additional configuration is needed.

---

## Complete Custom Feedback Form Example

A fully custom feedback flow — your own UI, validation, submission:

```typescript
import React from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
} from "react-native";
import * as Sentry from "@sentry/react-native";

interface FeedbackFormProps {
  onDismiss: () => void;
  associatedEventId?: string;
}

export function CustomFeedbackForm({ onDismiss, associatedEventId }: FeedbackFormProps) {
  const [name, setName] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [message, setMessage] = React.useState("");
  const [submitting, setSubmitting] = React.useState(false);

  async function handleSubmit() {
    if (!message.trim()) {
      Alert.alert("Required", "Please describe what happened.");
      return;
    }

    setSubmitting(true);

    try {
      Sentry.captureFeedback(
        {
          name: name.trim() || undefined,
          email: email.trim() || undefined,
          message: message.trim(),
          associatedEventId,
        },
        {
          captureContext: {
            tags: { feedbackSource: "custom-form" },
          },
        }
      );

      Alert.alert("Thank you", "Your feedback has been submitted.");
      onDismiss();
    } catch (err) {
      Alert.alert("Error", "Failed to submit feedback. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Send Feedback</Text>

      <TextInput
        style={styles.input}
        placeholder="Name (optional)"
        value={name}
        onChangeText={setName}
        autoCapitalize="words"
      />

      <TextInput
        style={styles.input}
        placeholder="Email (optional)"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />

      <TextInput
        style={[styles.input, styles.messageInput]}
        placeholder="Describe what happened *"
        value={message}
        onChangeText={setMessage}
        multiline
        numberOfLines={5}
        textAlignVertical="top"
      />

      <TouchableOpacity
        style={[styles.button, submitting && styles.buttonDisabled]}
        onPress={handleSubmit}
        disabled={submitting}
      >
        <Text style={styles.buttonText}>
          {submitting ? "Sending…" : "Submit"}
        </Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.cancelButton} onPress={onDismiss}>
        <Text style={styles.cancelText}>Cancel</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 24, backgroundColor: "#fff", borderRadius: 12 },
  title: { fontSize: 20, fontWeight: "bold", marginBottom: 16 },
  input: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
    fontSize: 16,
  },
  messageInput: { minHeight: 120 },
  button: {
    backgroundColor: "#6200ee",
    borderRadius: 8,
    padding: 14,
    alignItems: "center",
    marginBottom: 8,
  },
  buttonDisabled: { opacity: 0.6 },
  buttonText: { color: "#fff", fontSize: 16, fontWeight: "600" },
  cancelButton: { alignItems: "center", padding: 10 },
  cancelText: { color: "#666", fontSize: 16 },
});
```

---

## `captureFeedback` API Reference

```typescript
Sentry.captureFeedback(
  feedback: UserFeedback,
  hint?: EventHint
): string | undefined
```

### `feedback` object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | `string` | ✅ | User's feedback text |
| `name` | `string` | ❌ | User's display name |
| `email` | `string` | ❌ | User's email address |
| `associatedEventId` | `string` | ❌ | Links feedback to a specific Sentry event (error or message) |

### `hint` object (optional)

| Field | Type | Description |
|-------|------|-------------|
| `captureContext` | `CaptureContext` | Scope data to attach (tags, extra, user, level, contexts) |
| `attachments` | `Attachment[]` | Files to attach (screenshots, logs, etc.) |

Returns the feedback event ID (or `undefined` if SDK is disabled).

---

## `feedbackIntegration` Configuration Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `formTitle` | `string` | `"Report a Bug"` | Widget modal title |
| `submitButtonLabel` | `string` | `"Send Bug Report"` | Submit button text |
| `cancelButtonLabel` | `string` | `"Cancel"` | Cancel button text |
| `nameLabel` | `string` | `"Name"` | Name field label |
| `namePlaceholder` | `string` | `"Your Name"` | Name field placeholder |
| `emailLabel` | `string` | `"Email"` | Email field label |
| `emailPlaceholder` | `string` | `"your.email@example.org"` | Email field placeholder |
| `messageLabel` | `string` | `"Description"` | Message field label |
| `messagePlaceholder` | `string` | `"What's the bug? What did you expect?"` | Message field placeholder |
| `isNameRequired` | `boolean` | `false` | Make name field required |
| `isEmailRequired` | `boolean` | `false` | Make email field required |
| `useSentryUser` | `object` | — | Maps Sentry user scope fields to pre-fill name/email |
| `styles` | `object` | — | Style overrides for widget UI elements |

---

## API Summary

| Method | Description |
|--------|-------------|
| `Sentry.showFeedbackWidget()` | Open the built-in feedback modal |
| `Sentry.showFeedbackButton()` | Show the persistent floating feedback button |
| `Sentry.hideFeedbackButton()` | Hide the persistent floating feedback button |
| `Sentry.captureFeedback(feedback, hint?)` | Submit feedback programmatically |
| `Sentry.lastEventId()` | Get the ID of the most recent captured event (for linking) |
| `Sentry.feedbackIntegration(options)` | Configure the built-in widget |

---

## Version Requirements

| Feature | Min SDK | Notes |
|---------|---------|-------|
| `captureFeedback()` | ≥6.5.0 | Replaces deprecated `captureUserFeedback()` |
| `showFeedbackWidget()` | ≥6.9.0 | Requires `Sentry.wrap(App)` |
| `feedbackIntegration()` | ≥6.9.0 | Configure widget appearance |
| `FeedbackWidget` component | ≥6.9.0 | Inline embedded widget |
| `showFeedbackButton()` / `hideFeedbackButton()` | ≥6.15.0 | Floating feedback button |
| Offline caching | Built-in | Automatic, no config needed |
| Session Replay attachment | ≥6.9.0 | When `mobileReplayIntegration` enabled |
| New Architecture (Fabric) support | React Native ≥0.71 | Widget works on new arch |

---

## Expo Considerations

- The feedback widget works in **Expo managed and bare** workflows
- `showFeedbackWidget()` requires a **native build** — it does **not** function in Expo Go
- `captureFeedback()` (programmatic API) works in both Expo Go and native builds
- Use `isRunningInExpoGo()` to guard widget calls in dev:

```typescript
import { isRunningInExpoGo } from "expo";
import * as Sentry from "@sentry/react-native";

function ReportButton() {
  if (isRunningInExpoGo()) {
    // Fallback: use captureFeedback directly instead of the widget
    return (
      <Button
        title="Report (dev mode)"
        onPress={() =>
          Sentry.captureFeedback({ message: "Test feedback from Expo Go" })
        }
      />
    );
  }

  return (
    <Button
      title="Report a Problem"
      onPress={() => Sentry.showFeedbackWidget()}
    />
  );
}
```

---

## Migration: `captureUserFeedback` → `captureFeedback`

`captureUserFeedback()` was removed in v7. Replace all usages:

```typescript
// ❌ BEFORE (v6 and earlier) — removed in v7
Sentry.captureUserFeedback({
  event_id: eventId,
  name: "John",
  email: "john@example.com",
  comments: "Something went wrong.",
});

// ✅ AFTER (v7+)
Sentry.captureFeedback({
  associatedEventId: eventId,
  name: "John",
  email: "john@example.com",
  message: "Something went wrong.", // renamed from "comments"
});
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `showFeedbackWidget()` has no effect | Confirm `Sentry.wrap(App)` wraps your root component |
| Widget doesn't open on New Architecture | Requires React Native ≥0.71; check architecture compatibility |
| Feedback not appearing in Sentry dashboard | Verify DSN is correct; check network connectivity; enable `debug: true` for SDK logs |
| `captureFeedback` not sending in Expo Go | Expected — use `captureFeedback()` (works) but not `showFeedbackWidget()` (native only) |
| `lastEventId()` returns `undefined` | No events have been captured in the current session yet; ensure an error or message was captured first |
| Offline feedback not delivered | Offline caching is automatic; check `maxCacheItems` (default: 30); old cache is evicted if full |
| `captureUserFeedback` is not a function | Upgrade to `@sentry/react-native` ≥7.0.0 and replace with `captureFeedback()` |
| Replay not attaching to feedback | Confirm `mobileReplayIntegration()` is in `integrations` and the app is running as a native build |
| `associatedEventId` not linking correctly | Pass the exact event ID string returned by `captureException`, `captureMessage`, or `lastEventId()` |
| Widget styles not applying | Pass `styles` config inside `feedbackIntegration({ styles: { ... } })` in `Sentry.init` |
