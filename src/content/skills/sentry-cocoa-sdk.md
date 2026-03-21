---
title: "Sentry Cocoa SDK"
description: "Full Sentry SDK setup for Apple platforms (iOS, macOS, tvOS, watchOS, visionOS). Use when asked to 'add Sentry to iOS', 'add Sentry to Swift', 'install sentry-cocoa', or configure error monitoring, tracing, profiling, session replay, or logging fo..."
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "cocoa", "sdk"]
date: 2026-03-20
---

# Sentry Cocoa SDK

Opinionated wizard that scans your Apple project and guides you through complete Sentry setup.

## Invoke This Skill When

- User asks to "add Sentry to iOS/macOS/tvOS" or "set up Sentry" in an Apple app
- User wants error monitoring, tracing, profiling, session replay, or logging in Swift/ObjC
- User mentions `sentry-cocoa`, `SentrySDK`, or the Apple/iOS Sentry SDK
- User wants to monitor crashes, app hangs, watchdog terminations, or performance

> **Note:** SDK versions and APIs below reflect Sentry docs at time of writing (sentry-cocoa 9.5.1).
> Always verify against [docs.sentry.io/platforms/apple/](https://docs.sentry.io/platforms/apple/) before implementing.

---

## Phase 1: Detect

Run these commands to understand the project before making any recommendations:

```bash
# Check existing Sentry dependency
grep -i sentry Package.swift Podfile Cartfile 2>/dev/null

# Detect UI framework (SwiftUI vs UIKit)
grep -rE "@main|struct.*App.*:.*App" --include="*.swift" . 2>/dev/null | head -5
grep -rE "AppDelegate|UIApplicationMain" --include="*.swift" . 2>/dev/null | head -5

# Detect platform and deployment targets
grep -E "platforms:|\.iOS|\.macOS|\.tvOS|\.watchOS|\.visionOS" Package.swift 2>/dev/null
grep -E "platform :ios|platform :osx|platform :tvos|platform :watchos" Podfile 2>/dev/null

# Detect logging
grep -rE "import OSLog|os\.log|CocoaLumberjack|DDLog" --include="*.swift" . 2>/dev/null | head -5

# Detect companion backend
ls ../backend ../server ../api 2>/dev/null
ls ../go.mod ../requirements.txt ../Gemfile ../package.json 2>/dev/null
```

**What to note:**
- Is `sentry-cocoa` already in `Package.swift` or `Podfile`? If yes, skip to Phase 2 (configure features).
- SwiftUI (`@main App` struct) or UIKit (`AppDelegate`)? Determines init pattern.
- Which Apple platforms? (Affects which features are available — see Platform Support Matrix.)
- Existing logging library? (Enables structured log capture.)
- Companion backend? (Triggers Phase 4 cross-link for distributed tracing.)

---

## Phase 2: Recommend

Based on what you found, present a concrete recommendation. Don't ask open-ended questions — lead with a proposal:

**Recommended (core coverage):**
- ✅ **Error Monitoring** — always; crash reporting, app hangs, watchdog terminations, NSError/Swift errors
- ✅ **Tracing** — always for apps; auto-instruments app launch, network, UIViewController, file I/O, Core Data
- ✅ **Profiling** — production apps; continuous profiling with minimal overhead

**Optional (enhanced observability):**
- ⚡ **Session Replay** — user-facing apps; ⚠️ disabled by default on iOS 26+ (Liquid Glass rendering)
- ⚡ **Logging** — when structured log capture is needed
- ⚡ **User Feedback** — apps that want crash/error feedback forms from users

**Not available for Cocoa:**
- ❌ Metrics — use custom spans instead
- ❌ Crons — backend only
- ❌ AI Monitoring — JS/Python only

**Recommendation logic:**

| Feature | Recommend when... |
|---------|------------------|
| Error Monitoring | **Always** — non-negotiable baseline |
| Tracing | **Always for apps** — rich auto-instrumentation out of the box |
| Profiling | Production apps where performance matters |
| Session Replay | **iOS only** user-facing apps (check iOS 26+ caveat; not tvOS/macOS/watchOS/visionOS) |
| Logging | Existing `os.log` / CocoaLumberjack usage, or structured logs needed |
| User Feedback | Apps wanting in-app bug reports with screenshots |

Propose: *"I recommend Error Monitoring + Tracing + Profiling. Want me to also add Session Replay and Logging?"*

---

## Phase 3: Guide

### Install

**Option 1 — Sentry Wizard (recommended):** Walks you through login, org/project selection, and auth token setup interactively. Then installs the SDK, updates AppDelegate, adds dSYM/debug symbol upload build phases, and configures everything automatically.

```bash
brew install getsentry/tools/sentry-wizard && sentry-wizard -i ios
```

**Option 2 — Swift Package Manager:** File → Add Packages → enter:
```
https://github.com/getsentry/sentry-cocoa.git
```

Or in `Package.swift`:
```swift
.package(url: "https://github.com/getsentry/sentry-cocoa", from: "9.5.1"),
```

**SPM Products** — choose **exactly one** per target:

| Product | Use Case |
|---------|----------|
| `Sentry` | **Recommended** — static framework, fast app start |
| `Sentry-Dynamic` | Dynamic framework alternative |
| `SentrySwiftUI` | SwiftUI view performance tracking (`SentryTracedView`) |
| `Sentry-WithoutUIKitOrAppKit` | watchOS, app extensions, CLI tools |

> ⚠️ Xcode allows selecting multiple products — choose only one.

**Option 3 — CocoaPods:**
```ruby
platform :ios, '11.0'
use_frameworks!

target 'YourApp' do
  pod 'Sentry', :git => 'https://github.com/getsentry/sentry-cocoa.git', :tag => '9.5.1'
end
```

> **Known issue (Xcode 14+):** Sandbox `rsync.samba` error → Target Settings → "Enable User Script Sandbox" → `NO`.

---

### Quick Start — Recommended Init

Full config enabling the most features with sensible defaults. Add before any other code at app startup.

**SwiftUI — App entry point:**
```swift
import SwiftUI
import Sentry

@main
struct MyApp: App {
    init() {
        SentrySDK.start { options in
            options.dsn = ProcessInfo.processInfo.environment["SENTRY_DSN"]
                ?? "https://examplePublicKey@o0.ingest.sentry.io/0"
            options.environment = ProcessInfo.processInfo.environment["SENTRY_ENVIRONMENT"]
            options.releaseName = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String

            // Error monitoring (on by default — explicit for clarity)
            options.enableCrashHandler = true
            options.enableAppHangTrackingV2 = true
            options.enableWatchdogTerminationTracking = true
            options.attachScreenshot = true
            options.attachViewHierarchy = true
            options.sendDefaultPii = true

            // Tracing
            options.tracesSampleRate = 1.0          // lower to 0.2 in high-traffic production

            // Profiling (SDK 9.0.0+ API)
            options.configureProfiling = {
                $0.sessionSampleRate = 1.0
                $0.lifecycle = .trace
            }

            // Session Replay (disabled on iOS 26+ by default — safe to configure)
            options.sessionReplay.sessionSampleRate = 1.0
            options.sessionReplay.onErrorSampleRate = 1.0

            // Logging (SDK 9.0.0+ top-level; use options.experimental.enableLogs in 8.x)
            options.enableLogs = true
        }
    }

    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

**UIKit — AppDelegate:**
```swift
import UIKit
import Sentry

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {
        SentrySDK.start { options in
            options.dsn = ProcessInfo.processInfo.environment["SENTRY_DSN"]
                ?? "https://examplePublicKey@o0.ingest.sentry.io/0"
            options.environment = ProcessInfo.processInfo.environment["SENTRY_ENVIRONMENT"]
            options.releaseName = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String

            options.enableCrashHandler = true
            options.enableAppHangTrackingV2 = true
            options.enableWatchdogTerminationTracking = true
            options.attachScreenshot = true
            options.attachViewHierarchy = true
            options.sendDefaultPii = true

            options.tracesSampleRate = 1.0

            options.configureProfiling = {
                $0.sessionSampleRate = 1.0
                $0.lifecycle = .trace
            }

            options.sessionReplay.sessionSampleRate = 1.0
            options.sessionReplay.onErrorSampleRate = 1.0

            // Logging (SDK 9.0.0+ top-level; use options.experimental.enableLogs in 8.x)
            options.enableLogs = true
        }
        return true
    }
}
```

> ⚠️ SDK initialization must occur on the **main thread**.

---

### For Each Agreed Feature

Walk through features one at a time. Load the reference file for each, follow its steps, and verify before moving to the next:

| Feature | Reference file | Load when... |
|---------|---------------|-------------|
| Error Monitoring | `${SKILL_ROOT}/references/error-monitoring.md` | Always (baseline) |
| Tracing | `${SKILL_ROOT}/references/tracing.md` | App launch, network, UIViewController perf |
| Profiling | `${SKILL_ROOT}/references/profiling.md` | Production perf-sensitive apps |
| Session Replay | `${SKILL_ROOT}/references/session-replay.md` | User-facing iOS/tvOS apps |
| Logging | `${SKILL_ROOT}/references/logging.md` | Structured log capture needed |
| User Feedback | `${SKILL_ROOT}/references/user-feedback.md` | In-app bug reporting wanted |

For each feature: `Read ${SKILL_ROOT}/references/<feature>.md`, follow steps exactly, verify it works.

---

## Configuration Reference

### Key `SentryOptions` Fields

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `dsn` | `String` | `""` | SDK disabled if empty; reads `SENTRY_DSN` env var |
| `environment` | `String` | `""` | e.g., `"production"`; reads `SENTRY_ENVIRONMENT` |
| `releaseName` | `String` | `""` | e.g., `"my-app@1.0.0"`; reads `SENTRY_RELEASE` |
| `debug` | `Bool` | `false` | Verbose SDK output — **disable in production** |
| `sendDefaultPii` | `Bool` | `false` | Include IP, user info from active integrations |
| `enableCrashHandler` | `Bool` | `true` | Master switch for crash reporting |
| `enableAppHangTrackingV2` | `Bool` | `true` (9.0+) | Differentiates fully/non-fully blocked hangs |
| `appHangTimeoutInterval` | `Double` | `2.0` | Seconds before classifying as hang |
| `enableWatchdogTerminationTracking` | `Bool` | `true` | Track watchdog kills (iOS, tvOS, Mac Catalyst) |
| `attachScreenshot` | `Bool` | `false` | Capture screenshot on error |
| `attachViewHierarchy` | `Bool` | `false` | Capture view hierarchy on error |
| `tracesSampleRate` | `NSNumber?` | `nil` | Transaction sample rate (`nil` = tracing disabled); Swift auto-boxes `Double` literals (e.g. `1.0` → `NSNumber`) |
| `tracesSampler` | `Closure` | `nil` | Dynamic per-transaction sampling (overrides rate) |
| `enableAutoPerformanceTracing` | `Bool` | `true` | Master switch for auto-instrumentation |
| `tracePropagationTargets` | `[String]` | `[".*"]` | Hosts/regex that receive distributed trace headers |
| `enableCaptureFailedRequests` | `Bool` | `true` | Auto-capture HTTP 5xx errors as events |
| `enableNetworkBreadcrumbs` | `Bool` | `true` | Breadcrumbs for outgoing HTTP requests |
| `inAppInclude` | `[String]` | `[]` | Module prefixes treated as "in-app" code |
| `maxBreadcrumbs` | `Int` | `100` | Max breadcrumbs per event |
| `sampleRate` | `Float` | `1.0` | Error event sample rate |
| `beforeSend` | `Closure` | `nil` | Hook to mutate/drop error events |
| `onCrashedLastRun` | `Closure` | `nil` | Called on next launch after a crash |

### Environment Variables

| Variable | Maps to | Purpose |
|----------|---------|---------|
| `SENTRY_DSN` | `dsn` | Data Source Name |
| `SENTRY_RELEASE` | `releaseName` | App version (e.g., `my-app@1.0.0`) |
| `SENTRY_ENVIRONMENT` | `environment` | Deployment environment |

### Platform Feature Support Matrix

| Feature | iOS | tvOS | macOS | watchOS | visionOS |
|---------|-----|------|-------|---------|----------|
| Crash Reporting | ✅ | ✅ | ✅ | ✅ | ✅ |
| App Hangs V2 | ✅ | ✅ | ❌ | ❌ | ❌ |
| Watchdog Termination | ✅ | ✅ | ❌ | ❌ | ❌ |
| App Start Tracing | ✅ | ✅ | ❌ | ❌ | ✅ |
| UIViewController Tracing | ✅ | ✅ | ❌ | ❌ | ✅ |
| SwiftUI Tracing | ✅ | ✅ | ✅ | ❌ | ✅ |
| Network Tracking | ✅ | ✅ | ✅ | ❌ | ✅ |
| Profiling | ✅ | ✅ | ✅ | ❌ | ✅ |
| Session Replay | ✅ | ❌ | ❌ | ❌ | ❌ |
| MetricKit | ✅ (15+) | ❌ | ✅ (12+) | ❌ | ❌ |

---

## Verification

Test that Sentry is receiving events:

```swift
// Trigger a test error event:
SentrySDK.capture(message: "Sentry Cocoa SDK test")

// Or test crash reporting (without debugger — crashes are intercepted by debugger):
// SentrySDK.crash()  // uncomment, run without debugger, relaunch to see crash report
```

Check the Sentry dashboard within a few seconds. If nothing appears:
1. Set `options.debug = true` — prints SDK internals to Xcode console
2. Verify the DSN is correct and the project exists
3. Ensure initialization is on the **main thread**

---

## Production Settings

Lower sample rates for production to control volume and cost:

```swift
options.tracesSampleRate = 0.2          // 20% of transactions

options.configureProfiling = {
    $0.sessionSampleRate = 0.1          // 10% of sessions
    $0.lifecycle = .trace
}

options.sessionReplay.sessionSampleRate = 0.1   // 10% continuous
options.sessionReplay.onErrorSampleRate = 1.0   // 100% on error (keep high)

options.debug = false                   // never in production
```

---

## Phase 4: Cross-Link

After completing Apple setup, check for a companion backend missing Sentry coverage:

```bash
# Detect companion backend
ls ../backend ../server ../api 2>/dev/null
cat ../go.mod 2>/dev/null | head -5
cat ../requirements.txt ../Pipfile 2>/dev/null | head -5
cat ../Gemfile 2>/dev/null | head -5
cat ../package.json 2>/dev/null | grep -E '"name"|"dependencies"' | head -5
```

If a backend is found, configure `tracePropagationTargets` to enable distributed tracing end-to-end, and suggest the matching skill:

| Backend detected | Suggest skill | Trace header support |
|-----------------|--------------|---------------------|
| Go (`go.mod`) | `sentry-go-sdk` | ✅ automatic |
| Python (`requirements.txt`) | `sentry-python-sdk` | ✅ automatic |
| Ruby (`Gemfile`) | `sentry-ruby-sdk` | ✅ automatic |
| Node.js backend (`package.json`) | `sentry-node-sdk` (or `sentry-express-sdk`) | ✅ automatic |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Set `debug: true`, verify DSN format, ensure init is on main thread |
| Crashes not captured | **Run without debugger attached** — debugger intercepts signals |
| App hangs not reported | Auto-disabled when debugger attached; check `appHangTimeoutInterval` |
| Session Replay not recording | Check iOS version — disabled by default on iOS 26+ (Liquid Glass); verify `sessionSampleRate > 0` |
| Tracing data missing | Confirm `tracesSampleRate > 0`; check `enableAutoPerformanceTracing = true` |
| Profiling data missing | Verify `sessionSampleRate > 0` in `configureProfiling`; for `.trace` lifecycle, tracing must be enabled |
| `rsync.samba` build error (CocoaPods) | Target Settings → "Enable User Script Sandbox" → `NO` |
| Multiple SPM products selected | Choose **only one** of `Sentry`, `Sentry-Dynamic`, `SentrySwiftUI`, `Sentry-WithoutUIKitOrAppKit` |
| `inAppExclude` compile error | Removed in SDK 9.0.0 — use `inAppInclude` only |
| Watchdog termination not tracked | Requires `enableCrashHandler = true` (it is by default) |
| Network breadcrumbs missing | Requires `enableSwizzling = true` (it is by default) |
| `profilesSampleRate` compile error | Removed in SDK 9.0.0 — use `configureProfiling` closure instead |

---

## Reference: Error Monitoring

# Error Monitoring — Sentry Cocoa SDK

> Minimum SDK: `sentry-cocoa` v7.0.0+  
> Swift Error improvements: v8.7.0+  
> HTTP client error capture: v8.0.0+

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enableCrashHandler` | `Bool` | `true` | Master switch for crash reporting (signal handlers, Mach exceptions, C++) |
| `sampleRate` | `Float` (0.0–1.0) | `1.0` | Percentage of error events sent |
| `attachStacktrace` | `Bool` | `true` | Attach stack traces to all captured messages |
| `maxBreadcrumbs` | `Int` | `100` | Max breadcrumbs per event |
| `enableAppHangTracking` | `Bool` | `true` | Detect main thread unresponsiveness |
| `appHangTimeoutInterval` | `Double` | `2.0` | Seconds before a hang is reported |
| `enableAppHangTrackingV2` | `Bool` | `true` (v9+) | Differentiates fully/non-fully-blocking hangs |
| `enableWatchdogTerminationTracking` | `Bool` | `true` | Track OS watchdog kills via heuristics |
| `enableCaptureFailedRequests` | `Bool` | `true` | Auto-capture HTTP client errors as Sentry events |
| `failedRequestStatusCodes` | `[HttpStatusCodeRange]` | `[500–599]` | Status code ranges that trigger error capture |
| `failedRequestTargets` | `[String]` | `[".*"]` | Hosts/regex patterns to monitor for HTTP errors |
| `attachScreenshot` | `Bool` | `false` | Capture screenshot when an error event fires |
| `attachViewHierarchy` | `Bool` | `false` | Capture view hierarchy when an error event fires |
| `sendDefaultPii` | `Bool` | `false` | Include PII (IP address, username) in events |

## Code Examples

### SDK initialization

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "https://examplePublicKey@o0.ingest.sentry.io/0"
    options.environment = "production"
    options.releaseName = "my-app@2.0.0+123"
    options.enableCrashHandler = true   // default; explicit for clarity
    options.attachScreenshot = true
    options.attachViewHierarchy = true
}
```

### Capture a message

```swift
SentrySDK.capture(message: "Something noteworthy happened")
```

### Capture a Swift Error / NSError

```swift
do {
    try riskyOperation()
} catch {
    SentrySDK.capture(error: error)
}
```

### Capture a custom SentryEvent

```swift
let event = Event(level: .warning)
event.message = SentryMessage(formatted: "Checkout flow aborted")
event.tags = ["feature": "checkout"]
event.extra = ["cart_items": 3]
SentrySDK.capture(event: event)
```

### Swift Error enum — human-readable titles (v8.7.0+)

By default, Swift error enum cases appear as `LoginError - Code: 1`. To get readable titles, conform to `CustomNSError`:

```swift
enum LoginError: Error {
    case wrongUser(id: String)
    case wrongPassword
}

extension LoginError: CustomNSError {
    var errorUserInfo: [String: Any] {
        [NSDebugDescriptionErrorKey: debugDescription]
    }

    private var debugDescription: String {
        switch self {
        case .wrongUser(let id): return "Wrong user (id: \(id))"
        case .wrongPassword:     return "Wrong password"
        }
    }
}

// Captures "LoginError - Wrong user (id: 12345)" as the issue title
SentrySDK.capture(error: LoginError.wrongUser(id: "12345"))
```

> Use `NSDebugDescriptionErrorKey`, NOT `NSLocalizedDescriptionKey`. Localized strings vary by device locale and create duplicate issues.

### Capture with per-event scope

The scope callback receives an isolated copy — changes don't affect global state:

```swift
SentrySDK.capture(error: error) { scope in
    scope.setTag(value: "checkout", key: "feature")
    scope.setContext(value: ["amount": 99.99, "currency": "USD"], key: "payment")
}

SentrySDK.capture(message: "Payment declined") { scope in
    scope.setLevel(.fatal)
    scope.setTag(value: "stripe", key: "payment_provider")
}
```

### App hang detection

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.enableAppHangTracking = true
    options.appHangTimeoutInterval = 2.0    // default; avoid values < 0.1

    // V2: differentiates fully vs non-fully blocking hangs (default in v9+)
    options.enableAppHangTrackingV2 = true
    options.enableReportNonFullyBlockingAppHangs = true
}

// Pause tracking during expected blocking operations (e.g., permission dialogs)
SentrySDK.pauseAppHangTracking()
// ... system dialog ...
SentrySDK.resumeAppHangTracking()
```

V2 exception types:

| Type | Meaning |
|------|---------|
| `App Hang Fully Blocked` | Main thread completely frozen |
| `App Hang Non Fully Blocked` | App stuck but still renders some frames |
| `Fatal App Hang Fully Blocked` | Force-quit / watchdog kill during full block |
| `Fatal App Hang Non Fully Blocked` | Force-quit / watchdog kill during partial block |

### HTTP client error capture

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.enableCaptureFailedRequests = true

    // Capture 4xx and 5xx
    options.failedRequestStatusCodes = [
        HttpStatusCodeRange(min: 400, max: 599)
    ]

    // Only monitor your own backend
    options.failedRequestTargets = [
        "api.myapp.com",
        ".*\\.myapp\\.com"   // regex supported
    ]
}
```

### Scope management

```swift
// Global scope — persists across all events
SentrySDK.configureScope { scope in
    scope.setTag(value: "premium", key: "subscription")
    scope.setExtra(value: 42, key: "retry_count")

    let user = User()
    user.email = "user@example.com"
    user.userId = "abc123"
    scope.setUser(user)

    scope.setContext(value: [
        "version": "2.1",
        "platform": "ios"
    ], key: "app_info")
}

// Clear a specific value
SentrySDK.configureScope { scope in
    scope.removeTag(key: "subscription")
    scope.setUser(nil)   // clear user on logout
}

// Clear everything
SentrySDK.configureScope { $0.clear() }
```

### Set user identity

```swift
let user = User()
user.userId = "user-abc-123"
user.email = "john.doe@example.com"
user.username = "johndoe"
user.data = ["plan": "premium"]
SentrySDK.setUser(user)

// On logout
SentrySDK.setUser(nil)
```

### Breadcrumbs

```swift
let crumb = Breadcrumb()
crumb.level = .info
crumb.category = "auth"
crumb.type = "user"
crumb.message = "User logged in"
crumb.data = ["method": "oauth", "provider": "google"]
SentrySDK.addBreadcrumb(crumb)
```

Filter breadcrumbs via `beforeBreadcrumb`:

```swift
SentrySDK.start { options in
    options.beforeBreadcrumb = { crumb in
        if crumb.message?.contains("password") == true { return nil }
        return crumb
    }
}
```

### beforeSend hook — filter and modify events

```swift
SentrySDK.start { options in
    options.beforeSend = { event in
        // Drop events from internal testers
        if event.user?.email?.hasSuffix("@mycompany.com") == true {
            return nil
        }
        // Suppress app hang events
        // Note: V1 (enableAppHangTracking) uses exception type "App Hanging"
        //       V2 (enableAppHangTrackingV2, default in 9.0+) may use a different
        //       type — inspect event.exceptions?.first?.type in beforeSend to confirm
        if event.exceptions?.first?.type == "App Hanging" {
            return nil
        }
        // Scrub sensitive data
        event.request?.cookies = nil
        // Add global tag
        event.tags?["processed_by"] = "beforeSend"
        return event
    }
}
```

### Screenshot and view hierarchy attachments

```swift
SentrySDK.start { options in
    options.attachScreenshot = true
    options.screenshot.maskAllText = true        // default: true
    options.screenshot.maskAllImages = true      // default: true
    options.screenshot.maskedViewClasses = [MySecretView.self]
    options.screenshot.unmaskedViewClasses = [MyLogoView.self]

    options.attachViewHierarchy = true
    options.reportAccessibilityIdentifier = true // disable if identifiers contain PII

    // Conditional capture
    options.beforeCaptureScreenshot = { event in event.level == .fatal }
    options.beforeCaptureViewHierarchy = { _ in true }
}
```

### Fingerprinting and custom grouping

```swift
// Per-event fingerprint via scope
SentrySDK.capture(error: error) { scope in
    scope.fingerprint = ["payment-service-timeout", "stripe"]
}

// Pattern-based in beforeSend — extend default grouping
SentrySDK.start { options in
    options.beforeSend = { event in
        if let error = event.error as NSError?,
           error.domain == NSURLErrorDomain,
           let url = error.userInfo[NSURLErrorFailingURLErrorKey] as? String {
            event.fingerprint = ["{{ default }}", url, String(error.code)]
        }
        return event
    }
}

// Aggressive grouping — all SQLite errors → one issue
SentrySDK.start { options in
    options.beforeSend = { event in
        if let error = event.error as NSError?,
           error.domain == NSSQLiteErrorDomain {
            event.fingerprint = ["database-connection-error"]
        }
        return event
    }
}
```

`"{{ default }}"` substitutes Sentry's standard hash, allowing you to *extend* rather than fully replace default grouping.

### onCrashedLastRun callback

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.onCrashedLastRun = { event in
        // Called once after init when the previous run crashed.
        // Keep this minimal — complex logic can cascade into another crash.
        UserDefaults.standard.set(true, forKey: "didCrashLastRun")
    }
}
```

## Automatic Crash Reporting

When `enableCrashHandler = true` (default), the SDK installs:

- **Signal handlers** — SIGABRT, SIGBUS, SIGFPE, SIGILL, SIGSEGV, SIGTRAP
- **Mach exception handlers** — low-level kernel exceptions
- **C++ exception handlers** — `std::terminate` interception
- **Objective-C uncaught exception handler** — `NSSetUncaughtExceptionHandler`

> ⚠️ Always test crash reporting **without a debugger attached**. The debugger intercepts signals and prevents the SDK from capturing crashes.

### macOS — uncaught NSException reporting

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.enableUncaughtNSExceptionReporting = true
}
```

### SIGTERM reporting (v8.27.0+)

```swift
options.enableSigtermReporting = true   // report background task timeouts
```

## Scope API Quick Reference

```swift
SentrySDK.configureScope { scope in
    scope.setTag(value: "v2", key: "api_version")
    scope.removeTag(key: "api_version")
    scope.setExtra(value: someObject, key: "debug_info")
    scope.removeExtra(key: "debug_info")
    scope.setContext(value: ["key": "value"], key: "my_context")
    scope.removeContext(key: "my_context")
    scope.setUser(User(userId: "12345"))
    scope.setUser(nil)
    scope.setLevel(.error)
    scope.fingerprint = ["my-group-key"]
    scope.addBreadcrumb(crumb)
    scope.clear()
}
```

## Best Practices

- Set `releaseName` to a consistent value (e.g., `CFBundleShortVersionString + "+" + CFBundleVersion`) for regression tracking between deployments
- Use `NSDebugDescriptionErrorKey` — not `NSLocalizedDescriptionKey` — for error user info to avoid locale-based duplicate issues
- Use `beforeSend` to strip PII (`event.request?.cookies = nil`) when `sendDefaultPii = false`
- Use `onCrashedLastRun` only for lightweight operations (flag writes); heavy logic risks a cascading crash
- Disable app hang tracking for **Widgets and Live Activities** to avoid false positives
- Use `initialScope` to set global context before the first event fires

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Crashes not appearing in Sentry | Test without debugger attached; debugger intercepts signals |
| Swift errors show "Code: 1" | Conform to `CustomNSError` and provide `NSDebugDescriptionErrorKey` in `errorUserInfo` |
| Duplicate issues from localization | Use `NSDebugDescriptionErrorKey`, not `NSLocalizedDescriptionKey` |
| App hang events too noisy | Raise `appHangTimeoutInterval`; or filter in `beforeSend` by exception type |
| HTTP errors not captured | Verify `enableCaptureFailedRequests = true` and `failedRequestStatusCodes` covers the status code |
| Screenshots contain PII | Enable `screenshot.maskAllText = true` and `screenshot.maskAllImages = true` (both default) |
| Events missing from `beforeSend` for transactions | `beforeSend` is for error/message events only; use `beforeSendSpan` for spans |
| `onCrashedLastRun` not firing | SDK must be initialized on main thread; check `enableCrashHandler = true` |

---

## Reference: Logging

# Logging — Sentry Cocoa SDK

> Minimum SDK (experimental): `sentry-cocoa` v8.55.0+  
> Minimum SDK (stable): `sentry-cocoa` v9.0.0+

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enableLogs` | `Bool` | `false` | Enable structured logging (v9.0.0+, stable) |
| `experimental.enableLogs` | `Bool` | `false` | Enable structured logging (v8.55.0–8.x, experimental) |
| `beforeSendLog` | `((SentryLog) -> SentryLog?)?` | `nil` | Filter or modify logs before sending; return `nil` to drop |

## Code Examples

### Enable logging

**SDK v9.0.0+ (stable, recommended):**

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.enableLogs = true
}
```

**SDK v8.55.0–8.x (experimental):**

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.experimental.enableLogs = true
}
```

### All log levels

```swift
import Sentry

let logger = SentrySDK.logger

// Without attributes
logger.trace("Starting database connection")
logger.debug("Cache miss for user")
logger.info("Profile updated successfully")
logger.warn("Rate limit nearly reached")
logger.error("Failed to process payment")
logger.fatal("Database connection pool exhausted")

// With structured attributes
logger.trace("Starting DB connection",    attributes: ["database": "users"])
logger.debug("Cache miss for user",       attributes: ["userId": 123])
logger.info("Profile updated",            attributes: ["profileId": 345])
logger.warn("Rate limit reached",         attributes: ["endpoint": "/api/results/"])
logger.error("Payment failed",            attributes: ["amount": 99.99])
logger.fatal("Connection pool exhausted", attributes: ["activeConnections": 100])
```

Supported attribute value types: `String`, `Int`, `Double`, `Bool`.

### Log levels (severity order)

| Level | Method | Typical Use |
|-------|--------|-------------|
| 1 — Trace | `logger.trace(...)` | Very fine-grained diagnostic events |
| 2 — Debug | `logger.debug(...)` | Debugging information |
| 3 — Info | `logger.info(...)` | General informational messages |
| 4 — Warn | `logger.warn(...)` | Potentially harmful situations |
| 5 — Error | `logger.error(...)` | Error events; app may continue |
| 6 — Fatal | `logger.fatal(...)` | Severe errors; likely app abort |

### Swift string interpolation as structured attributes

When you use Swift string interpolation in the message, the SDK automatically extracts the interpolated values as named attributes using the key pattern `sentry.message.parameter.{index}`:

```swift
let userId = "user_123"
let orderCount = 5

logger.info("User \(userId) placed \(orderCount) orders")

// Sentry receives:
//   message template: "User %s placed %d orders"
//   sentry.message.parameter.0 = "user_123"
//   sentry.message.parameter.1 = 5
```

This preserves the ability to search and filter by the template while retaining the individual values as queryable attributes.

### beforeSendLog filter hook

```swift
SentrySDK.start { options in
    options.enableLogs = true
    options.beforeSendLog = { log in
        // Drop trace-level logs
        if log.level == .trace { return nil }

        // Drop debug logs in production
        if log.level == .debug && options.environment == "production" { return nil }

        // Enrich all logs with app version
        var mutableLog = log
        mutableLog.attributes["app.version"] =
            Bundle.main.object(forInfoDictionaryKey: "CFBundleShortVersionString") as? String
        return mutableLog
    }
}
```

Available on `SentryLog`:
- `log.level` — `SentryLevel` (`.trace`, `.debug`, `.info`, `.warning`, `.error`, `.fatal`)
- `log.message` — `String`
- `log.timestamp` — `Date`
- `log.attributes` — `[String: Any]`

### Automatic default attributes

The SDK automatically attaches the following to every log entry:

- `environment` and `release`
- SDK name and version
- User ID, name, email (if set via `SentrySDK.setUser(...)`)
- Message template and `sentry.message.parameter.*` interpolated values
- Integration origin marker

### Using alongside Apple os.log

`SentrySDK.logger` is a standalone Sentry telemetry system — it is **not** a bridge to `os.log` / `Logger`. To write to both:

```swift
import OSLog
import Sentry

private let osLog = Logger(subsystem: "com.myapp", category: "network")

func fetchData() {
    osLog.info("Fetching data")                        // → system log / Console.app
    SentrySDK.logger.info("Fetching data",             // → Sentry Logs
                          attributes: ["subsystem": "network"])
}
```

There is no built-in bridge to automatically forward `OSLog` entries to Sentry.

### Full initialization example with logging

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.environment = "production"
    options.enableLogs = true   // v9.0.0+
    options.beforeSendLog = { log in
        // Drop trace and debug in production
        guard log.level != .trace && log.level != .debug else { return nil }
        return log
    }
}

// Anywhere in your app:
SentrySDK.logger.info("User signed in",
                      attributes: ["userId": currentUser.id, "method": "oauth"])
```

## Known Limitations

- Logs can be **lost in crash scenarios** if the SDK cannot flush the buffer before the app terminates — this is a known limitation of the current implementation
- Logs are a **separate pipeline** from error events — they are not attached to breadcrumbs or spans automatically
- Attribute values are limited to `String`, `Int`, `Double`, and `Bool` — other types must be converted

## Best Practices

- Prefer `logger.error(...)` or `logger.fatal(...)` over `SentrySDK.capture(message:)` for application-level log lines — structured logs are easier to search and filter in Sentry
- Use structured attributes instead of embedding values in the message string directly; attributes are indexed and queryable
- Use Swift string interpolation to let the SDK extract attribute values automatically
- Set `beforeSendLog` to drop `trace` and `debug` in production to reduce noise and volume
- Set the user via `SentrySDK.setUser(...)` before logging to automatically correlate logs with user identities

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing in Sentry | Verify `options.enableLogs = true` (v9+) or `options.experimental.enableLogs = true` (v8.55+) |
| Logs only partially appearing | Logs may be lost during crashes; this is a known SDK limitation |
| `SentrySDK.logger` not found | Requires v8.55.0+; check SPM/CocoaPods version |
| Attributes not queryable | Only `String`, `Int`, `Double`, and `Bool` are supported attribute value types |
| `beforeSendLog` not called | Ensure you set it before `SentrySDK.start` completes and `enableLogs = true` |
| Too many logs overwhelming Sentry | Use `beforeSendLog` to filter by level; set minimum level for production |
| Logs missing user context | Call `SentrySDK.setUser(...)` before logging to attach user identity automatically |

---

## Reference: Profiling

# Profiling — Sentry Cocoa SDK

> Minimum SDK for UI Profiling (`configureProfiling`): `sentry-cocoa` v8.49.0+  
> Minimum SDK for stable `configureProfiling` API: v9.0.0+  
> **All legacy profiling APIs (`profilesSampleRate`, `enableAppLaunchProfiling`, continuous beta) were removed in v9.0.0.**

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `configureProfiling` | `((SentryProfileOptions) -> Void)?` | `nil` | Closure to configure UI Profiling (v8.49.0+) |
| `sessionSampleRate` | `Double` (0.0–1.0) | `0` | Fraction of user sessions to profile; evaluated once per session |
| `lifecycle` | `SentryProfileLifecycle` | `.manual` | `.trace` (auto) or `.manual` (explicit start/stop) |
| `profileAppStarts` | `Bool` | `false` | Profile from the earliest possible lifecycle stage on next launch |

## Code Examples

### Basic setup — trace lifecycle (recommended)

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"

    // Tracing must be enabled for .trace lifecycle
    options.tracesSampleRate = 1.0

    options.configureProfiling = {
        $0.sessionSampleRate = 1.0   // 100% of sessions; lower for production
        $0.lifecycle = .trace        // profiler runs while a root span is active
    }
}
```

### Manual lifecycle — explicit start/stop

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.configureProfiling = {
        $0.sessionSampleRate = 1.0
        $0.lifecycle = .manual   // default if omitted
    }
}

// Profile a specific operation
@IBAction func onSyncTapped() {
    SentrySDK.startProfiler()

    URLSession.shared.dataTask(with: syncRequest) { data, _, _ in
        self.processData(data)
        DispatchQueue.main.async {
            self.tableView.performBatchUpdates({
                // update cells
            }) { _ in
                SentrySDK.stopProfiler()
            }
        }
    }.resume()
}
```

### App launch profiling (trace lifecycle)

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.tracesSampleRate = 1.0
    options.configureProfiling = {
        $0.sessionSampleRate = 1.0
        $0.lifecycle = .trace
        $0.profileAppStarts = true   // profile from earliest lifecycle stage
    }
}
```

Launch profile attaches to a special `app.launch` transaction (shown as **"launch"** in the Sentry UI). The profiler stops automatically when:
1. `SentrySDK.startWithOptions` is called, OR
2. TTID/TTFD is reached (if TTID/TTFD tracking is enabled)

### Manual lifecycle — app launch profiling

With `.manual` lifecycle, a launch profile starts on the **next app launch** and continues until you explicitly call `SentrySDK.stopProfiler()`.

### Compound sampling example

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.tracesSampleRate = 0.5   // 50% of transactions traced
    options.configureProfiling = {
        $0.sessionSampleRate = 0.5   // 50% of those sessions profiled
        $0.lifecycle = .trace
        // Result: ~25% of root span creations will produce profile data (0.5 × 0.5)
    }
}
```

`sessionSampleRate` is evaluated **once per session**, not per span. The same decision applies to all profiler start attempts for the duration of that session.

## SentryProfileLifecycle Values

| Value | Behaviour |
|-------|-----------|
| `.manual` | Profiler runs only between `SentrySDK.startProfiler()` and `SentrySDK.stopProfiler()` |
| `.trace` | Profiler starts automatically when a new root span is created; stops when no root spans remain |

## Manual Profiler Control

```swift
SentrySDK.startProfiler()   // begin profiling (manual lifecycle)
SentrySDK.stopProfiler()    // end profiling and flush data to Sentry
```

## dSYM Upload Requirement

Profiling data in Sentry shows symbolicated stack frames. Without dSYM files, frames appear as memory addresses.

Upload dSYMs via the Sentry Wizard build phase (added automatically during wizard setup):

```bash
# Verify the build phase exists in Xcode:
# Target → Build Phases → "Upload Debug Symbols to Sentry"
# or manually:
sentry-cli --auth-token YOUR_TOKEN debug-files upload \
    --org YOUR_ORG \
    --project YOUR_PROJECT \
    path/to/dSYMs/
```

For CI/CD, set `SENTRY_AUTH_TOKEN` as an environment variable.

## API History / Migration

| API | Introduced | Removed | Notes |
|-----|-----------|---------|-------|
| `profilesSampleRate` | 8.12.0 | **9.0.0** | Transaction-based profiling |
| `profilesSampler` | 8.12.0 | **9.0.0** | Dynamic transaction-based profiling |
| `enableAppLaunchProfiling` | 8.21.0 | **9.0.0** | Launch profiling (old) |
| Continuous profiling beta | 8.36.0 | **9.0.0** | Standalone `startProfiler`/`stopProfiler` (old) |
| `configureProfiling` (UI Profiling) | **8.49.0** | — | **Current API** |

### Migrating from legacy `profilesSampleRate`

```swift
// BEFORE (removed in v9.0.0)
SentrySDK.start { options in
    options.tracesSampleRate = 1.0
    options.profilesSampleRate = 1.0   // ❌ no longer exists
}

// AFTER (v9.0.0+)
SentrySDK.start { options in
    options.tracesSampleRate = 1.0
    options.configureProfiling = {
        $0.sessionSampleRate = 1.0
        $0.lifecycle = .trace          // ✅ equivalent behaviour
    }
}
```

## Best Practices

- Always set `sessionSampleRate > 0` — it defaults to `0`, so no profiling data is collected unless you explicitly set it
- Use `.trace` lifecycle in production: the profiler only runs during active transactions, minimising overhead
- Use `.manual` lifecycle to profile targeted operations (e.g., a specific button tap, a batch import)
- Lower `sessionSampleRate` in production (e.g., `0.1`) — profiling adds CPU overhead on older devices
- Upload dSYMs for every build; without them, profile data shows raw addresses
- `profileAppStarts = true` is most valuable for identifying slow `+[AppDelegate application:didFinishLaunchingWithOptions:]` work
- Do not combine the old `profilesSampleRate` with `configureProfiling` — the old APIs are removed in v9.0.0

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No profiling data in Sentry | Verify `sessionSampleRate > 0`; it defaults to `0` |
| Profiles missing for `.trace` lifecycle | Verify `tracesSampleRate > 0`; profiles only appear when transactions are sent |
| Stack frames show memory addresses | Upload dSYMs; verify build phase runs in both Debug and Release |
| Profiling not starting on app launch | Use `profileAppStarts = true`; SDK must be initialised with `SentrySDK.startWithOptions` |
| `configureProfiling` not available | Requires v8.49.0+; check your SPM/CocoaPods version |
| Old `profilesSampleRate` not compiling | Removed in v9.0.0; migrate to `configureProfiling` |
| Manual profiler never stops | Ensure `SentrySDK.stopProfiler()` is called on all code paths, including error branches |
| Excessive CPU overhead | Lower `sessionSampleRate`; switch to `.trace` lifecycle; avoid `.manual` with long-running sessions |

---

## Reference: Session Replay

# Session Replay — Sentry Cocoa SDK

> Minimum SDK: `sentry-cocoa` v8.31.1+  
> View Renderer V2 (default): v8.50.0+  
> iOS 26 auto-disable safeguard: v8.57.0+

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `sessionReplay.sessionSampleRate` | `Float` (0.0–1.0) | `0` | Continuous recording sample rate |
| `sessionReplay.onErrorSampleRate` | `Float` (0.0–1.0) | `0` | Buffered recording sample rate (uploads on error) |
| `sessionReplay.maskAllText` | `Bool` | `true` | Mask all text content |
| `sessionReplay.maskAllImages` | `Bool` | `true` | Mask all images |
| `sessionReplay.maskedViewClasses` | `[AnyClass]` | `[]` | Additional view classes to always mask |
| `sessionReplay.unmaskedViewClasses` | `[AnyClass]` | `[]` | View classes to always unmask |
| `sessionReplay.quality` | `SentryReplayQuality` | `.medium` | Video quality (bitrate and resolution) |
| `sessionReplay.enableViewRendererV2` | `Bool` | `true` | Faster renderer (default since v8.50.0) |
| `sessionReplay.enableFastViewRendering` | `Bool` | `false` | Experimental CALayer renderer (faster, less accurate) |
| `sessionReplay.frameRate` | `UInt` | `1` | Frames per second |
| `sessionReplay.errorReplayDuration` | `TimeInterval` | `30` | Seconds of buffer kept before an error |
| `sessionReplay.sessionSegmentDuration` | `TimeInterval` | `5` | Seconds per upload segment |
| `sessionReplay.maximumDuration` | `TimeInterval` | `3600` | Maximum session duration (60 min) |
| `experimental.enableSessionReplayInUnreliableEnvironment` | `Bool` | `false` | Force-enable on iOS 26+ (⚠️ PII risk) |

## Code Examples

### Basic setup

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"

    // Continuously record 10% of sessions
    options.sessionReplay.sessionSampleRate = 0.1

    // Buffer and upload on error for all other sessions
    options.sessionReplay.onErrorSampleRate = 1.0
}
```

**Sampling logic:** `sessionSampleRate` is evaluated first. If not selected for continuous recording, the SDK switches to buffered mode and evaluates `onErrorSampleRate` — keeping a rolling buffer that is uploaded only when an error fires.

### Session lifecycle

- **Starts:** SDK init or app foreground
- **Ends:** 30+ seconds in background, or 60-minute maximum
- **Buffer mode:** Keeps a rolling 30-second window; uploaded on error capture
- **Segments:** Chunked into 5-second segments for upload
- **Resumes:** Within 30 seconds of foreground using the same `replay_id`

### Privacy masking defaults

What is masked by default:

- ✅ All text content (`maskAllText = true`)
- ✅ All images (`maskAllImages = true`)
- ✅ User input fields (always masked, regardless of settings)
- ✅ Video players
- ✅ WebViews
- ❌ Bundled image assets (considered low PII risk — shown in replay)

### SwiftUI view modifiers

```swift
import Sentry

// UNMASK a specific view (show in replay despite global maskAllText/maskAllImages)
Text("Public promotion text")
    .sentryReplayUnmask()

// MASK a specific view (hide in replay even if global masking is off)
Text("\(user.creditCardNumber)")
    .sentryReplayMask()

// Visualize masking overlay in DEBUG builds / Xcode Previews
ContentView()
    .sentryReplayPreviewMask()
```

### UIKit view instance masking

```swift
// Mask a single UIView instance
myView.sentryReplayMask()
// equivalent:
SentrySDK.replay.maskView(view: myView)

// Unmask a single UIView instance
myLabel.sentryReplayUnmask()
// equivalent:
SentrySDK.replay.unmaskView(view: myLabel)
```

> Note: Masking targets `UIView` subclasses only. You **cannot** target `UIViewController` types directly.

### Class-level masking (all instances of a class)

```swift
SentrySDK.start { options in
    options.sessionReplay.maskedViewClasses   = [MySecretView.self, CreditCardField.self]
    options.sessionReplay.unmaskedViewClasses = [MyPublicBanner.self]
}
```

### Debug — visualize the masking overlay live

```swift
#if DEBUG
SentrySDK.replay.showMaskPreview()       // full opacity
SentrySDK.replay.showMaskPreview(0.5)    // 50% opacity
#endif
```

### Exclude views from subtree traversal

For views that cause crashes or performance issues during replay capture:

```swift
options.sessionReplay.excludeViewTypeFromSubtreeTraversal("MyProblematicView")
// Force-include a system view normally excluded:
options.sessionReplay.includeViewTypeInSubtreeTraversal("CameraUI.ChromeSwiftUIView")
```

### Reducing performance overhead

```swift
SentrySDK.start { options in
    options.sessionReplay.quality = .low                    // lower bitrate/resolution
    options.sessionReplay.enableFastViewRendering = true    // CALayer renderer (faster, less accurate)
}

// Disable entirely on low-power / low-end devices:
if ProcessInfo.processInfo.isLowPowerModeEnabled {
    options.sessionReplay.sessionSampleRate  = 0.0
    options.sessionReplay.onErrorSampleRate  = 0.0
}
```

### Quality enum values

| Value | Bit Rate | Resolution |
|-------|---------|------------|
| `.low` | ~50 kbps | Reduced |
| `.medium` | Default | Default |
| `.high` | Higher | Full |

---

## ⚠️ iOS 26 / Xcode 26 / Liquid Glass Caveat

Apple's **Liquid Glass** rendering engine in iOS 26 breaks the SDK's view-snapshotting approach, causing unreliable masking and potential PII leaks.

**Starting with v8.57.0**, Session Replay is **automatically and silently disabled** when both:
- App is running on **iOS 26.0 or later**
- App was **compiled with Xcode 26.0 or later**

Replay continues to work if:
- The device runs iOS < 26
- The app was built with Xcode < 26
- `UIDesignRequiresCompatibility = YES` is set in `Info.plist`

**SDKs older than v8.57.0** do **not** include this safeguard and may crash or leak PII on iOS 26. Upgrade immediately.

**Force-enable on iOS 26+ (experimental — will be removed once masking is fixed):**

```swift
SentrySDK.start { options in
    // ⚠️ WARNING: May leak PII. Only use if you understand the risk.
    options.experimental.enableSessionReplayInUnreliableEnvironment = true
}
```

Track the fix at [getsentry/sentry-cocoa#6390](https://github.com/getsentry/sentry-cocoa/issues/6390).

---

## Performance Overhead (iPhone 14 Pro benchmarks)

| Metric | Without Replay | With Replay |
|--------|---------------|-------------|
| FPS | 55 | 53 |
| Memory | 102 MB | 121 MB |
| CPU | 4% | 13% |
| Main thread per capture | — | ~25 ms |
| Network bandwidth | — | ~10 KB/s |

> iPhone 8 and older: The ~25 ms capture time exceeds the 16.7 ms frame budget, causing scrolling jank. View Renderer V2 (default since v8.50.0) improved from ~155 ms to ~25 ms per capture.

---

## Best Practices

- Never enable `enableSessionReplayInUnreliableEnvironment` in production without understanding the PII risk
- Set `maskAllText = true` and `maskAllImages = true` (both default) — only unmasked explicitly what's safe to show
- Use `.sentryReplayUnmask()` sparingly on known-safe content rather than globally disabling masking
- Start with `onErrorSampleRate = 1.0` and `sessionSampleRate = 0` to capture replays only on errors (lowest overhead)
- Test masking on real devices — use `SentrySDK.replay.showMaskPreview()` in DEBUG builds to verify

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No replays appearing | Verify `sessionSampleRate > 0` or `onErrorSampleRate > 0`; both default to `0` |
| Replay disabled on iOS 26 | Expected — SDK 8.57.0+ auto-disables for safety; use the experimental override at your own risk |
| PII visible in replay | Verify `maskAllText = true` and `maskAllImages = true`; check `.sentryReplayUnmask()` isn't applied too broadly |
| Scrolling jank during replay | Enable `enableFastViewRendering = true`; switch to `quality = .low`; consider disabling on low-end devices |
| Replay stops after 60 minutes | Expected — `maximumDuration = 3600` seconds is the default cap |
| Error buffer not uploading | Verify `onErrorSampleRate > 0`; buffer is only uploaded when `SentrySDK.capture(error:)` is called |
| App crash during replay capture | Use `excludeViewTypeFromSubtreeTraversal` for the problematic view type |
| Texture/AsyncDisplayKit views not masked | Access `.view` on the node: `SentrySDK.replay.maskView(view: myNode.view)` |

---

## Reference: Tracing

# Tracing — Sentry Cocoa SDK

> Minimum SDK: `sentry-cocoa` v7.0.0+  
> SwiftUI instrumentation stable: v8.17.0+  
> File I/O manual tracing extensions: v8.48.0+

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `tracesSampleRate` | `Double` (0.0–1.0) | `nil` | Uniform sample rate; mutually exclusive with `tracesSampler` |
| `tracesSampler` | `(SentrySamplingContext) -> NSNumber` | `nil` | Dynamic per-transaction sampling; overrides `tracesSampleRate` |
| `enableAutoPerformanceTracing` | `Bool` | `true` | Master switch for all automatic instrumentation |
| `enableUIViewControllerTracing` | `Bool` | `true` | UIViewController lifecycle spans |
| `enableUserInteractionTracing` | `Bool` | `true` | Transactions for UIControl tap/click events |
| `enableNetworkTracking` | `Bool` | `true` | URLSession HTTP request spans |
| `enableFileIOTracing` | `Bool` | `true` | NSData / FileManager file I/O spans |
| `enableCoreDataTracing` | `Bool` | `true` | Core Data fetch/save spans |
| `enableTimeToFullDisplayTracing` | `Bool` | `false` | TTFD span; requires `SentrySDK.reportFullyDisplayed()` |
| `enablePreWarmedAppStartTracing` | `Bool` | `true` | Prewarmed cold/warm start tracing (iOS 15+) |
| `enableDataSwizzling` | `Bool` | `true` | NSData swizzling for automatic file I/O tracing |
| `enableFileManagerSwizzling` | `Bool` | `false` | NSFileManager swizzling (experimental; needed for iOS 18+) |
| `tracePropagationTargets` | `[String]` | `[".*"]` | Hosts/regex for outgoing distributed trace headers |
| `enableSwizzling` | `Bool` | `true` | Master switch for method swizzling (required by several auto-instrumentation features) |

## Code Examples

### Basic tracing setup

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.tracesSampleRate = 1.0   // 100% in dev; lower for production (e.g., 0.2)
}
```

### Dynamic sampling with tracesSampler

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.tracesSampler = { context in
        // Never sample next-launch transactions
        if context.isForNextAppLaunch { return 0 }
        // Always sample checkout
        if context.customSamplingContext?["flow"] as? String == "checkout" { return 1.0 }
        // Default: 25%
        return 0.25
    }
}
```

### Custom transaction with child spans

```swift
import Sentry

func performCheckout() {
    let transaction = SentrySDK.startTransaction(
        name: "checkout",
        operation: "perform-checkout",
        bindToScope: true   // makes it accessible via SentrySDK.span
    )

    let validationSpan = transaction.startChild(
        operation: "validation",
        description: "validating shopping cart"
    )
    validateShoppingCart()
    validationSpan.finish()

    let processSpan = transaction.startChild(
        operation: "process",
        description: "processing payment"
    )

    do {
        try processPayment()
        processSpan.finish()
        transaction.finish()
    } catch {
        SentrySDK.capture(error: error)
        processSpan.finish(status: .internalError)
        transaction.finish(status: .internalError)
    }
}
```

### Accessing the scope-bound span from a called function

```swift
func processPayment() {
    // Grab the transaction bound to scope (or start a standalone one)
    let span = SentrySDK.span ?? SentrySDK.startTransaction(
        name: "processPayment",
        operation: "task"
    )
    let child = span.startChild(operation: "payment.gateway")
    defer { child.finish() }

    // payment logic...
}
```

### Setting data attributes on transactions and spans

```swift
let transaction = SentrySDK.startTransaction(name: "sync", operation: "task")
transaction.setData(value: "incremental",  key: "sync.type")
transaction.setData(value: 42,             key: "sync.item_count")
transaction.setData(value: true,           key: "sync.force")
transaction.setData(value: ["a", "b"],     key: "sync.queues")

let span = transaction.startChild(operation: "db.fetch")
span.setData(value: "orders",              key: "db.table")
span.finish()
transaction.finish()
```

### Custom performance measurements

```swift
let span = SentrySDK.span

span?.setMeasurement(name: "memory_used",
                     value: 64,
                     unit: MeasurementUnitInformation.megabyte)

span?.setMeasurement(name: "profile_load_time",
                     value: 1.3,
                     unit: MeasurementUnitDuration.second)

span?.setMeasurement(name: "items_processed", value: 128)
```

---

## Automatic Instrumentation

All features are enabled once `tracesSampleRate > 0` (or `tracesSampler` is set). Disable all at once with `enableAutoPerformanceTracing = false`.

### App Start Tracing

**Platforms:** iOS, tvOS, Mac Catalyst

Measures process creation → first rendered frame. Start type classifications:

| Type | Description |
|------|-------------|
| `cold` | First launch, post-reboot, or post-update |
| `warm` | Any other process creation |
| `cold.prewarmed` | Cold start with OS pre-warm (iOS 15+) |
| `warm.prewarmed` | Warm start with OS pre-warm (iOS 15+) |

Child spans produced (sequential):

| Span | Measures |
|------|---------|
| Pre Runtime Init | Process start → runtime init |
| Runtime Init to Pre Main Initializers | Runtime init → pre-main setup |
| UIKit Init | Pre-main → Sentry SDK startup |
| Application Init | SDK startup → `didFinishLaunchingNotification` |
| Initial Frame Render | `didFinishLaunchingNotification` → first CADisplayLink callback (v9+) |

> ⚠️ If more than **5 seconds** elapse between transaction start and app-start end, app start spans are **not attached** to avoid misassociation.

### URLSession Network Tracking

**Platforms:** All  
**Note:** `NSURLConnection` is **not** supported — only `NSURLSession`.

Automatically adds HTTP spans to any active scope-bound transaction.

```swift
// Disable
options.enableNetworkTracking = false
```

### UIViewController Lifecycle Tracing

**Platforms:** iOS, tvOS, Mac Catalyst  
**Not available for:** SwiftUI (use `SentryTracedView` instead)

- Transaction operation: `ui.load`
- Transaction name: `Your_App.MainViewController`
- Auto-generated child spans: `loadView`, `viewDidLoad`, `viewWillAppear`, `viewDidAppear`
- Time to Initial Display (TTID) span: `ui.load.initial-display`

```swift
// Include framework view controllers
options.add(inAppInclude: "MyFramework")

// Exclude specific view controllers
options.swizzleClassNameExcludes = ["MyModalViewController"]

// Disable entirely
options.enableUIViewControllerTracing = false
```

### Time to Full Display (TTFD)

```swift
// Enable globally
options.enableTimeToFullDisplayTracing = true

// In your view controller, signal when async content is fully loaded:
SentrySDK.reportFullyDisplayed()
```

TTFD span status:

| Scenario | Status |
|----------|--------|
| `reportFullyDisplayed()` called | `.ok` |
| Not finished within 30 seconds | `.deadlineExceeded`; duration = TTID duration |
| Called before view appears | Reported time = TTID time |

### SwiftUI Instrumentation

**Package:** `SentrySwiftUI` (separate SPM product — do not also add `Sentry`)

```swift
import SentrySwiftUI

// Option 1: wrapper
var body: some View {
    SentryTracedView("My Awesome Screen") {
        List { /* content */ }
    }
}

// Option 2: modifier
var body: some View {
    List { /* content */ }
        .sentryTrace("My Awesome Screen")
}

// With TTFD (v8.44.0+)
SentryTracedView("Content", waitForFullDisplay: true) {
    VStack { /* async content */ }
        .onAppear {
            Task {
                data = await loadData()
                SentrySDK.reportFullyDisplayed()
            }
        }
}
```

### Slow & Frozen Frames

**Platforms:** iOS, tvOS, Mac Catalyst  
Tracked automatically during any active transaction. Appears as Mobile Vitals in the Sentry Performance UI.

| Threshold | Classification |
|-----------|----------------|
| > 16 ms per frame | Slow frame |
| > 700 ms per frame | Frozen frame |

### User Interaction Tracing

**Platforms:** iOS, tvOS, Mac Catalyst  
**Not available for:** SwiftUI

Creates a transaction for every UIControl tap/click.

- Transaction operation: `ui.action` or `ui.action.click`
- Transaction name: `YourApp_LoginViewController.loginButton`
- `idleTimeout`: 3000 ms — transaction finishes if no child spans within 3 seconds
- Transactions with **no child spans** are dropped

```swift
// Create child spans inside a tap handler:
func onLoginTapped() {
    let span = SentrySDK.span
    let child = span?.startChild(operation: "loadUserProfile")
    // ... work ...
    child?.finish()
}

// Disable
options.enableUserInteractionTracing = false
```

### File I/O Tracing (NSData)

**Platforms:** All  
Tracks `NSData` read/write operations as spans.

```swift
options.enableFileIOTracing = true   // default

// iOS 18+ / macOS 15+: NSFileManager no longer backed by NSData
// Enable experimental NSFileManager swizzling:
options.enableFileManagerSwizzling = true   // experimental, v9.0.0+
```

**Manual tracing extensions (v8.48.0+)** — only create spans when an active transaction exists:

```swift
// Data read/write
let data = try Data(contentsOfWithSentryTracing: url)
try data.writeWithSentryTracing(to: url)

// FileManager
let fm = FileManager.default
fm.createFileWithSentryTracing(atPath: path, contents: data)
try fm.moveItemWithSentryTracing(at: src, to: dst)
try fm.copyItemWithSentryTracing(at: src, to: dst)
try fm.removeItemWithSentryTracing(at: url)
```

Span operations created:

| Method | Span Op |
|--------|---------|
| `Data.init(contentsOf:)` | `file.read` |
| `data.write(to:)` / `createFile` | `file.write` |
| `moveItem` | `file.rename` |
| `copyItem` | `file.copy` |
| `removeItem` | `file.delete` |

### Core Data Tracing

**Platforms:** All  
Instruments `NSManagedObjectContext` fetch and save operations.

```swift
options.enableCoreDataTracing = true   // default

// Disable
options.enableCoreDataTracing = false
```

---

## Distributed Tracing

Sentry injects two headers into outgoing `NSURLSession` requests when the host matches `tracePropagationTargets`:

| Header | Purpose |
|--------|---------|
| `sentry-trace` | Carries trace ID, span ID, and sampled flag |
| `baggage` | Carries Dynamic Sampling Context key-value pairs |

```swift
SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.tracesSampleRate = 1.0

    // Only propagate to your own backend (default: all requests)
    options.tracePropagationTargets = [
        "api.myapp.com",
        ".*\\.myapp\\.com"   // regex supported
    ]

    // Also add W3C traceparent header (requires sentry-cocoa 9.0.0+)
    options.enablePropagateTraceparent = true
}
```

> **`enablePropagateTraceparent` requires sentry-cocoa 9.0.0+.** It is not available in 8.x.
>
> ⚠️ Both headers must be included in CORS allowlists and must not be blocked by proxies or firewalls.

---

## Platform Support Matrix

| Feature | iOS | tvOS | macOS | Mac Catalyst |
|---------|-----|------|-------|--------------|
| `tracesSampleRate` | ✅ | ✅ | ✅ | ✅ |
| App Start Tracing | ✅ | ✅ | ❌ | ✅ |
| UIViewController Lifecycle | ✅ | ✅ | ❌ | ✅ |
| TTID / TTFD | ✅ | ✅ | ❌ | ✅ |
| Slow & Frozen Frames | ✅ | ✅ | ❌ | ✅ |
| Network Tracking (URLSession) | ✅ | ✅ | ✅ | ✅ |
| File I/O Tracing | ✅ | ✅ | ✅ | ✅ |
| Core Data Tracing | ✅ | ✅ | ✅ | ✅ |
| User Interaction Tracing | ✅ | ✅ | ❌ | ✅ |
| SwiftUI (`SentryTracedView`) | ✅ (13+) | ✅ | ✅ | ✅ |
| Prewarmed App Start | ✅ (15+) | ❌ | ❌ | ❌ |
| NSFileManager Swizzling | ✅ (18+) | ✅ (18+) | ✅ (15+) | ✅ |

---

## Best Practices

- Start with `tracesSampleRate = 1.0` in development; lower to `0.1`–`0.2` in production
- Use `tracesSampler` (not `tracesSampleRate`) for route-specific or user-tier-based sampling
- Use `bindToScope: true` when starting a transaction so child spans created anywhere in the call stack are automatically linked
- Always `finish()` spans — unfinished spans are silently dropped
- Use `SentryTracedView` from the `SentrySwiftUI` package for SwiftUI screens (UIViewController tracing doesn't apply)
- Call `SentrySDK.reportFullyDisplayed()` only after your async data has been rendered — not just loaded
- Avoid setting `tracePropagationTargets = [".*"]` in production if you make requests to third-party services not using Sentry

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transactions appearing | Ensure `tracesSampleRate > 0` or `tracesSampler` returns `> 0` |
| Spans missing from transactions | Ensure `span.finish()` is called; check `bindToScope: true` for cross-function spans |
| App start spans not attached | Gap between transaction start and app-start end exceeded 5 seconds; check slow initialization |
| UIViewController tracing missing | Verify `enableSwizzling = true`; check class is not in `swizzleClassNameExcludes` |
| Network spans not appearing | Requires active scope-bound transaction; verify `enableNetworkTracking = true` and `enableSwizzling = true` |
| Distributed trace not linking to backend | Propagate both `sentry-trace` AND `baggage` headers; add them to CORS allowlist |
| File I/O spans missing on iOS 18+ | Enable `enableFileManagerSwizzling = true` (experimental) or use manual `WithSentryTracing` extensions |
| `SentryTracedView` not available | Add `SentrySwiftUI` SPM product — it's a separate package from `Sentry` |
| High-cardinality transaction names | UIViewController transactions use class name — expected; custom transactions should use stable names |

---

## Reference: User Feedback

# User Feedback — Sentry Cocoa SDK

> Minimum SDK: `sentry-cocoa` v8.46.0+  
> Self-hosted Sentry server: 24.4.2+

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `configureUserFeedback` | `((SentryUserFeedbackConfiguration) -> Void)?` | `nil` | Configure the feedback widget and form |
| `autoInject` | `Bool` | `true` | Auto-show floating "Report a Bug" button |
| `useShakeGesture` | `Bool` | `false` | Open the form on device shake |
| `showFormForScreenshots` | `Bool` | `false` | Auto-open form when user takes a screenshot |
| `animations` | `Bool` | `true` | Enable present/dismiss animations |
| `useSentryUser` | `Bool` | `true` | Pre-fill name/email from `SentrySDK.setUser(...)` |
| `isNameRequired` | `Bool` | `false` | Require name field before submission |
| `isEmailRequired` | `Bool` | `false` | Require email field before submission |
| `showName` | `Bool` | `true` | Show the name field |
| `showEmail` | `Bool` | `true` | Show the email field |

## Code Examples

### Basic widget setup (auto-inject mode)

By default (`autoInject = true`), the SDK injects a floating "Report a Bug" button:

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"
    options.configureUserFeedback { config in
        config.onSubmitSuccess = { data in
            // data keys: "message", "name", "email", "attachments"
            print("Feedback submitted: \(data["message"] ?? "")")
        }
        config.onSubmitError = { error in
            print("Submission failed: \(error)")
        }
    }
}
```

### Programmatic widget control

```swift
// Show the floating widget button programmatically
SentrySDK.feedback.showWidget()

// Hide the widget button
SentrySDK.feedback.hideWidget()
```

> `SentrySDK.feedback` is of type `SentryFeedbackAPI`. There is no `showUserFeedbackForm()` method — always use `showWidget()` to trigger the UI.

### SwiftUI integration

The feedback widget is UIKit-based. In a SwiftUI app, inject it via `.onAppear` on the root view:

```swift
import SwiftUI
import Sentry

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onAppear {
                    SentrySDK.feedback.showWidget()
                }
        }
    }
}
```

Or via a `UISceneDelegate`:

```swift
func sceneDidBecomeActive(_ scene: UIScene) {
    SentrySDK.feedback.showWidget()
}
```

### Bind to a custom UIButton

```swift
SentrySDK.start { options in
    options.configureUserFeedback { config in
        config.configureWidget { widget in
            widget.autoInject = false       // disable the default floating button
            widget.customButton = myButton  // tapping this button opens the form
        }
    }
}
```

### Trigger via shake gesture or screenshot

```swift
options.configureUserFeedback { config in
    config.useShakeGesture = true          // shake to open form
    config.showFormForScreenshots = true   // auto-open after screenshot
}
```

### Programmatic feedback capture (no widget, custom UI)

Use `SentrySDK.capture(feedback:)` to send feedback from your own UI without any Sentry widget:

```swift
import Sentry

SentrySDK.capture(feedback: .init(
    message: "The checkout button doesn't respond after adding a promo code.",
    name: "Jane Doe",
    email: "jane@example.org",
    source: .custom,
    attachments: nil   // pass [Attachment] to include screenshots or files; nil for none
))
```

### Link feedback to an error event

To associate a feedback submission with a specific Sentry issue, capture the error first and use the resulting event ID:

```swift
let eventId = SentrySDK.capture(error: error)

SentrySDK.capture(feedback: .init(
    message: "App crashed on the checkout screen.",
    name: "User",
    email: "user@example.com",
    associatedEventId: eventId
))
```

### Form customisation

```swift
options.configureUserFeedback { config in
    config.configureForm { form in
        form.formTitle           = "Share Your Feedback"
        form.submitButtonLabel   = "Send Feedback"
        form.cancelButtonLabel   = "Never Mind"
        form.messagePlaceholder  = "What went wrong? What did you expect?"
        form.isNameRequired      = true
        form.isEmailRequired     = true
        form.showBranding        = false
        form.useSentryUser       = true   // pre-fill from SentrySDK.setUser(...)
    }
}
```

### Widget placement and labels

```swift
options.configureUserFeedback { config in
    config.configureWidget { widget in
        widget.labelText = "Give Feedback"
        widget.location  = [.bottom, .trailing]   // anchor edges
        widget.showIcon  = true
        widget.layoutUIOffset = UIOffset(horizontal: -16, vertical: -32)
    }
}
```

### Theme customisation

```swift
options.configureUserFeedback { config in
    config.theme { theme in
        theme.submitBackground = .init(color: .systemBlue)
        theme.fontFamily       = "SF Pro Rounded"
    }
    config.darkTheme { theme in
        theme.background       = .init(color: .black)
        theme.submitBackground = .init(color: .systemPurple)
    }
}
```

Theme properties:

| Property | Light Default | Dark Default |
|----------|--------------|--------------|
| `background` | `rgb(255,255,255)` | `rgb(41,35,47)` |
| `foreground` | `rgb(43,34,51)` | `rgb(235,230,239)` |
| `submitBackground` | `rgb(88,74,192)` | `rgb(88,74,192)` |
| `submitForeground` | `rgb(255,255,255)` | `rgb(255,255,255)` |
| `errorColor` | `rgb(223,51,56)` | `rgb(245,84,89)` |
| `font` | `UIFontTextStyleCallout` | — |
| `headerFont` | `UIFontTextStyleTitle1` | — |
| `fontFamily` | `nil` (system font) | — |

### Session Replay integration

When a user opens the feedback form and Session Replay is enabled, the SDK automatically buffers up to **30 seconds** of the session. On submission, that replay clip is sent alongside the feedback event — no extra configuration needed.

### Full configuration example

```swift
import Sentry

SentrySDK.start { options in
    options.dsn = "___PUBLIC_DSN___"

    options.configureUserFeedback { config in
        config.showFormForScreenshots = true
        config.useShakeGesture        = false
        config.animations             = true

        config.configureForm { form in
            form.formTitle           = "Report a Bug"
            form.submitButtonLabel   = "Send Bug Report"
            form.isNameRequired      = true
            form.isEmailRequired     = false
            form.showBranding        = false
            form.useSentryUser       = true
        }

        config.configureWidget { widget in
            widget.labelText  = "Report a Bug"
            widget.location   = [.bottom, .trailing]
            widget.autoInject = true
        }

        config.theme { theme in
            theme.submitBackground = .init(color: .systemBlue)
        }
        config.darkTheme { theme in
            theme.background = .init(color: .black)
        }

        config.onFormOpen  = { print("Feedback form opened") }
        config.onFormClose = { print("Feedback form closed") }
        config.onSubmitSuccess = { data in
            print("✅ Feedback: \(data["message"] ?? "")")
        }
        config.onSubmitError = { error in
            print("❌ Submission failed: \(error)")
        }
    }
}
```

## SentryUserFeedbackWidgetConfiguration Reference

| Property | Type | Default |
|----------|------|---------|
| `autoInject` | `Bool` | `true` |
| `location` | `[NSDirectionalRectEdge]` | `[.bottom, .trailing]` |
| `layoutUIOffset` | `UIOffset` | `.zero` |
| `windowLevel` | `UIWindow.Level` | `normal + 1` |
| `showIcon` | `Bool` | `true` |
| `labelText` | `String?` | `"Report a Bug"` |
| `widgetAccessibilityLabel` | `String` | `labelText` |
| `customButton` | `UIButton?` | `nil` |

## SentryUserFeedbackFormConfiguration Reference

| Property | Type | Default |
|----------|------|---------|
| `formTitle` | `String` | `"Report a Bug"` |
| `showBranding` | `Bool` | `true` |
| `submitButtonLabel` | `String` | `"Send Bug Report"` |
| `cancelButtonLabel` | `String` | `"Cancel"` |
| `messagePlaceholder` | `String` | `"What's the bug? What did you expect?"` |
| `isNameRequired` | `Bool` | `false` |
| `showName` | `Bool` | `true` |
| `nameLabel` | `String` | `"Name"` |
| `namePlaceholder` | `String` | `"Your Name"` |
| `isEmailRequired` | `Bool` | `false` |
| `showEmail` | `Bool` | `true` |
| `emailLabel` | `String` | `"Email"` |
| `emailPlaceholder` | `String` | `"your.email@example.org"` |
| `useSentryUser` | `Bool` | `true` |

## Best Practices

- Set `useSentryUser = true` (default) and call `SentrySDK.setUser(...)` so the form pre-fills name and email — reduces friction
- Enable `showFormForScreenshots = true` — users often take screenshots when something goes wrong; it's a natural trigger
- Disable `autoInject` and use `widget.customButton = myButton` to match your app's design language
- Use `config.onSubmitSuccess` to show a native confirmation (toast/alert) after the Sentry form dismisses
- If collecting feedback from a known event ID, use `associatedEventId` to link the feedback to the specific issue in Sentry
- Add `tags` on the configuration to automatically tag all feedback events with context (e.g., app version, screen name)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Widget not appearing | Verify `autoInject = true`; in SwiftUI apps call `SentrySDK.feedback.showWidget()` in `.onAppear` |
| Form not opening on shake | Set `useShakeGesture = true`; verify the device is not muted (shake may be overridden by system) |
| Name/email fields not pre-filled | Ensure `useSentryUser = true` (default) and `SentrySDK.setUser(...)` was called before the form opens |
| Submission error | Check network connectivity; verify DSN is correct; inspect `onSubmitError` callback for the error |
| Feedback not linked to an issue | Use `associatedEventId` parameter with the event ID from `SentrySDK.capture(error:)` |
| Screenshot not attached | Wrap PNG `Data` in an `Attachment` and pass via `SentryFeedback.init(attachments:)`; ensure the data is non-nil and valid |
| Widget floating behind other UI | Raise `widget.windowLevel` above your custom windows |
| `configureUserFeedback` not available | Requires v8.46.0+; check your SPM/CocoaPods version |
