---
title: "Sentry GO SDK"
description: "Full Sentry SDK setup for Go. Use when asked to 'add Sentry to Go', 'install sentry-go', 'setup Sentry in Go', or configure error monitoring, tracing, logging, metrics, or crons for Go applications. Supports net/http, Gin, Echo, Fiber, FastHTTP, I..."
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "go", "sdk"]
date: 2026-03-20
---

# Sentry Go SDK

Opinionated wizard that scans your Go project and guides you through complete Sentry setup.

## Invoke This Skill When

- User asks to "add Sentry to Go" or "setup Sentry" in a Go app
- User wants error monitoring, tracing, logging, metrics, or crons in Go
- User mentions `sentry-go`, `github.com/getsentry/sentry-go`, or Go Sentry SDK
- User wants to monitor panics, HTTP handlers, or scheduled jobs in Go

> **Note:** SDK versions and APIs below reflect Sentry docs at time of writing (sentry-go v0.43.0).
> Always verify against [docs.sentry.io/platforms/go/](https://docs.sentry.io/platforms/go/) before implementing.

---

## Phase 1: Detect

Run these commands to understand the project before making any recommendations:

```bash
# Check existing Sentry dependency
grep -i sentry go.mod 2>/dev/null

# Detect web framework
grep -E "gin-gonic/gin|labstack/echo|gofiber/fiber|valyala/fasthttp|kataras/iris|urfave/negroni" go.mod 2>/dev/null

# Detect logging libraries
grep -E "sirupsen/logrus|go.uber.org/zap|rs/zerolog|log/slog" go.mod go.sum 2>/dev/null

# Detect cron / scheduler patterns
grep -E "robfig/cron|go-co-op/gocron|jasonlvhit/gocron" go.mod 2>/dev/null

# Detect OpenTelemetry usage
grep "go.opentelemetry.io" go.mod 2>/dev/null

# Check for companion frontend
ls frontend/ web/ client/ ui/ 2>/dev/null
```

**What to note:**
- Is `sentry-go` already in `go.mod`? If yes, skip to Phase 2 (configure features).
- Which framework is used? (Determines which sub-package and middleware to install.)
- Which logging library? (Enables automatic log capture.)
- Are cron/scheduler patterns present? (Triggers Crons recommendation.)
- Is there a companion frontend directory? (Triggers Phase 4 cross-link.)

---

## Phase 2: Recommend

Based on what you found, present a concrete recommendation. Don't ask open-ended questions — lead with a proposal:

**Recommended (core coverage):**
- ✅ **Error Monitoring** — always; captures panics and unhandled errors
- ✅ **Tracing** — if HTTP handlers, gRPC, or DB calls are detected
- ✅ **Logging** — if logrus, zap, zerolog, or slog is detected

**Optional (enhanced observability):**
- ⚡ **Metrics** — custom counters and gauges for business KPIs / SLOs
- ⚡ **Crons** — detect silent failures in scheduled jobs
- ⚠️ **Profiling** — removed in sentry-go v0.31.0; see `references/profiling.md` for alternatives

**Recommendation logic:**

| Feature | Recommend when... |
|---------|------------------|
| Error Monitoring | **Always** — non-negotiable baseline |
| Tracing | `net/http`, gin, echo, fiber, or gRPC imports detected |
| Logging | logrus, zap, zerolog, or `log/slog` imports detected |
| Metrics | Business events, SLO tracking, or counters needed |
| Crons | `robfig/cron`, `gocron`, or scheduled job patterns detected |
| Profiling | ⚠️ **Removed in v0.31.0** — do not recommend; see `references/profiling.md` |

Propose: *"I recommend setting up Error Monitoring + Tracing [+ Logging if applicable]. Want me to also add Metrics or Crons?"*

---

## Phase 3: Guide

### Install

```bash
# Core SDK (always required)
go get github.com/getsentry/sentry-go

# Framework sub-package — install only what matches detected framework:
go get github.com/getsentry/sentry-go/http      # net/http
go get github.com/getsentry/sentry-go/gin       # Gin
go get github.com/getsentry/sentry-go/echo      # Echo
go get github.com/getsentry/sentry-go/fiber     # Fiber
go get github.com/getsentry/sentry-go/fasthttp  # FastHTTP

# Logging sub-packages — install only what matches detected logging lib:
go get github.com/getsentry/sentry-go/logrus    # Logrus
go get github.com/getsentry/sentry-go/slog      # slog (stdlib, Go 1.21+)
go get github.com/getsentry/sentry-go/zap       # Zap
go get github.com/getsentry/sentry-go/zerolog   # Zerolog

# OpenTelemetry bridge (only if OTel is already in use):
go get github.com/getsentry/sentry-go/otel
```

### Quick Start — Recommended Init

Add to `main()` before any other code. This config enables the most features with sensible defaults:

```go
import (
    "log"
    "os"
    "time"
    "github.com/getsentry/sentry-go"
)

err := sentry.Init(sentry.ClientOptions{
    Dsn:              os.Getenv("SENTRY_DSN"),
    Environment:      os.Getenv("SENTRY_ENVIRONMENT"), // "production", "staging", etc.
    Release:          release,                          // inject via -ldflags at build time
    SendDefaultPII:   true,
    AttachStacktrace: true,

    // Tracing (adjust sample rate for production)
    EnableTracing:    true,
    TracesSampleRate: 1.0, // lower to 0.1–0.2 in high-traffic production

    // Logs
    EnableLogs: true,
})
if err != nil {
    log.Fatalf("sentry.Init: %s", err)
}
defer sentry.Flush(2 * time.Second)
```

**Injecting `Release` at build time (recommended):**
```go
var release string // set by -ldflags

// go build -ldflags="-X main.release=my-app@$(git describe --tags)"
```

### Framework Middleware

After `sentry.Init`, register the Sentry middleware for your framework:

| Framework | Import path | Middleware call | `Repanic` | `WaitForDelivery` |
|-----------|------------|----------------|-----------|-------------------|
| `net/http` | `.../sentry-go/http` | `sentryhttp.New(opts).Handle(h)` | `true` | `false` |
| Gin | `.../sentry-go/gin` | `router.Use(sentrygin.New(opts))` | `true` | `false` |
| Echo | `.../sentry-go/echo` | `e.Use(sentryecho.New(opts))` | `true` | `false` |
| Fiber | `.../sentry-go/fiber` | `app.Use(sentryfiber.New(opts))` | `false` | `true` |
| FastHTTP | `.../sentry-go/fasthttp` | `sentryfasthttp.New(opts).Handle(h)` | `false` | `true` |
| Iris | `.../sentry-go/iris` | `app.Use(sentryiris.New(opts))` | `true` | `false` |
| Negroni | `.../sentry-go/negroni` | `n.Use(sentrynegroni.New(opts))` | `true` | `false` |

> **Note:** Fiber and FastHTTP are built on `valyala/fasthttp` which has no built-in recovery. Use `Repanic: false, WaitForDelivery: true` for those.

**Hub access in handlers:**
```go
// net/http, Negroni:
hub := sentry.GetHubFromContext(r.Context())

// Gin:
hub := sentrygin.GetHubFromContext(c)

// Echo:
hub := sentryecho.GetHubFromContext(c)

// Fiber:
hub := sentryfiber.GetHubFromContext(c)
```

### For Each Agreed Feature

Walk through features one at a time. Load the reference file for each, follow its steps, and verify before moving to the next:

| Feature | Reference file | Load when... |
|---------|---------------|-------------|
| Error Monitoring | `${SKILL_ROOT}/references/error-monitoring.md` | Always (baseline) |
| Tracing | `${SKILL_ROOT}/references/tracing.md` | HTTP handlers / distributed tracing |
| Profiling | `${SKILL_ROOT}/references/profiling.md` | Performance-sensitive production apps |
| Logging | `${SKILL_ROOT}/references/logging.md` | logrus / zap / zerolog / slog detected |
| Metrics | `${SKILL_ROOT}/references/metrics.md` | Business KPIs / SLO tracking |
| Crons | `${SKILL_ROOT}/references/crons.md` | Scheduler / cron job patterns detected |

For each feature: `Read ${SKILL_ROOT}/references/<feature>.md`, follow steps exactly, verify it works.

---

## Configuration Reference

### Key `ClientOptions` Fields

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `Dsn` | `string` | `""` | SDK disabled if empty; env: `SENTRY_DSN` |
| `Environment` | `string` | `""` | e.g., `"production"`; env: `SENTRY_ENVIRONMENT` |
| `Release` | `string` | `""` | e.g., `"my-app@1.0.0"`; env: `SENTRY_RELEASE` |
| `SendDefaultPII` | `bool` | `false` | Include IP, request headers |
| `AttachStacktrace` | `bool` | `false` | Stack traces on `CaptureMessage` calls |
| `SampleRate` | `float64` | `1.0` | Error event sample rate (0.0 treated as 1.0) |
| `EnableTracing` | `bool` | `false` | Enable performance tracing |
| `TracesSampleRate` | `float64` | `0.0` | Transaction sample rate |
| `TracesSampler` | `TracesSampler` | `nil` | Custom per-transaction sampling (overrides rate) |
| `EnableLogs` | `bool` | `false` | Enable Sentry Logs feature |
| `MaxBreadcrumbs` | `int` | `100` | Max breadcrumbs per event |
| `MaxErrorDepth` | `int` | `100` | Max depth for unwrapping error chains |
| `Debug` | `bool` | `false` | Verbose SDK debug output |
| `BeforeSend` | `func` | `nil` | Hook to mutate/drop error events |
| `BeforeSendTransaction` | `func` | `nil` | Hook to mutate/drop transaction events |
| `IgnoreErrors` | `[]string` | `nil` | Regex patterns for errors to drop |
| `IgnoreTransactions` | `[]string` | `nil` | Regex patterns for transactions to drop |

### Environment Variables

| Variable | Maps to | Purpose |
|----------|---------|---------|
| `SENTRY_DSN` | `Dsn` | Data Source Name |
| `SENTRY_RELEASE` | `Release` | App version (e.g., `my-app@1.0.0`) |
| `SENTRY_ENVIRONMENT` | `Environment` | Deployment environment |
| `HTTP_PROXY` / `HTTPS_PROXY` | `HTTPProxy` / `HTTPSProxy` | Outbound proxy |

Options set in `ClientOptions` **override** environment variables.

---

## Verification

Test that Sentry is receiving events:

```go
// In a handler or test — triggers a real error event:
sentry.CaptureMessage("Sentry Go SDK test")

// Or trigger a captured panic (with recovery middleware in place):
panic("sentry test panic")
```

Check the Sentry dashboard within a few seconds. If nothing appears:
1. Set `Debug: true` in `ClientOptions` — prints SDK internals to stdout
2. Verify the DSN is correct and the project exists
3. Ensure `sentry.Flush(2 * time.Second)` is called (events are async by default)

---

## Phase 4: Cross-Link

After completing Go setup, check for a companion frontend missing Sentry coverage:

```bash
ls frontend/ web/ client/ ui/ 2>/dev/null
cat frontend/package.json web/package.json 2>/dev/null | grep -E '"react"|"svelte"|"vue"|"next"'
```

If a frontend directory exists without Sentry configured, suggest the matching skill:

| Frontend detected | Suggest skill |
|-------------------|--------------|
| React / Next.js | `sentry-react-sdk` |
| Svelte / SvelteKit | `sentry-svelte-sdk` |
| Vue | Use `@sentry/vue` — see [docs.sentry.io/platforms/javascript/guides/vue/](https://docs.sentry.io/platforms/javascript/guides/vue/) |
| Other JS/TS | `sentry-react-sdk` (covers generic browser JS patterns) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Set `Debug: true`, check DSN, verify `sentry.Flush()` is called |
| `sentry.Init` returns error | Malformed DSN — check format: `https://<key>@o<org>.ingest.sentry.io/<project>` |
| Panics not captured | Ensure framework middleware is registered before handlers |
| `defer sentry.Flush` not running | `os.Exit()` skips `defer` — call `sentry.Flush()` explicitly before `os.Exit()` |
| Missing stack traces | Set `AttachStacktrace: true` for `CaptureMessage`; works automatically for `CaptureException` |
| Goroutine events missing context | Clone hub before spawning goroutine: `hub := sentry.CurrentHub().Clone()` |
| Too many transactions | Lower `TracesSampleRate` or use `TracesSampler` to drop health checks / metrics endpoints |
| Fiber/FastHTTP not recovering | Use `Repanic: false, WaitForDelivery: true` for fasthttp-based frameworks |
| `SampleRate: 0.0` sending all events | `0.0` is treated as `1.0`; to drop all, set `Dsn: ""` instead |

---

## Reference: Crons

# Crons — Sentry Go SDK

> Minimum SDK: `github.com/getsentry/sentry-go` v0.18.0+

Sentry Cron Monitoring detects two failure modes:
- **Missed jobs** — the job never ran (schedule was skipped)
- **Timed-out jobs** — the job started but ran too long

## Configuration

No extra `ClientOptions` are required beyond a valid DSN:

```go
sentry.Init(sentry.ClientOptions{
    Dsn: os.Getenv("SENTRY_DSN"),
})
defer sentry.Flush(2 * time.Second)
```

> Check-ins are async by default — always `defer sentry.Flush()` before program exit.

## Core Types

### `CheckIn`

```go
type CheckIn struct {
    ID          EventID       // leave zero on start; use *id from start call on completion
    MonitorSlug string        // slug of the monitor in Sentry
    Status      CheckInStatus // in_progress | ok | error
    Duration    time.Duration // optional; set on final check-in
}
```

### `CheckInStatus` constants

```go
sentry.CheckInStatusInProgress // "in_progress" — job started
sentry.CheckInStatusOK         // "ok"           — job completed successfully
sentry.CheckInStatusError      // "error"         — job failed
```

### `MonitorConfig`

```go
type MonitorConfig struct {
    Schedule              MonitorSchedule     // when the job should run
    CheckInMargin         int64               // minutes of grace period before "missed"
    MaxRuntime            int64               // minutes before in-progress job times out
    Timezone              string              // tz database name, e.g. "America/New_York"
    FailureIssueThreshold int64               // consecutive failures before creating an issue
    RecoveryThreshold     int64               // consecutive successes before auto-resolving
}
```

### Schedule constructors

```go
// Standard 5-field cron expression
sentry.CrontabSchedule("*/10 * * * *")

// Interval-based
sentry.IntervalSchedule(1, sentry.MonitorScheduleUnitHour)
```

`MonitorScheduleUnit` constants: `MonitorScheduleUnitMinute`, `MonitorScheduleUnitHour`, `MonitorScheduleUnitDay`, `MonitorScheduleUnitWeek`, `MonitorScheduleUnitMonth`, `MonitorScheduleUnitYear`.

> `IntervalSchedule` takes `int64`, not `int`.

## Code Examples

### Check-in pattern (recommended)

Sends both a start and a completion check-in. Detects **missed** and **timed-out** jobs.

```go
func runHourlyReport() error {
    monitorConfig := &sentry.MonitorConfig{
        Schedule:              sentry.CrontabSchedule("0 * * * *"),
        MaxRuntime:            5,  // alert if still running after 5 minutes
        CheckInMargin:         2,  // allow 2 minutes late before "missed"
        FailureIssueThreshold: 2,  // create issue after 2 consecutive failures
        RecoveryThreshold:     1,  // auto-resolve after 1 success
        Timezone:              "America/New_York",
    }

    // Send in_progress — pass MonitorConfig here (only needed on first call)
    checkinID := sentry.CaptureCheckIn(
        &sentry.CheckIn{
            MonitorSlug: "hourly-report",
            Status:      sentry.CheckInStatusInProgress,
        },
        monitorConfig,
    )

    err := generateReport()

    // Send ok or error — dereference the *EventID returned by start
    status := sentry.CheckInStatusOK
    if err != nil {
        status = sentry.CheckInStatusError
    }
    sentry.CaptureCheckIn(
        &sentry.CheckIn{
            ID:          *checkinID, // dereference *EventID
            MonitorSlug: "hourly-report",
            Status:      status,
        },
        nil, // no config needed on completion
    )

    return err
}
```

### Heartbeat pattern

Sends only a completion check-in. Detects **missed** jobs only (no timeout detection).

```go
func runDailyCleanup() {
    start := time.Now()

    cleanupOldRecords()

    sentry.CaptureCheckIn(
        &sentry.CheckIn{
            MonitorSlug: "daily-cleanup",
            Status:      sentry.CheckInStatusOK,
            Duration:    time.Since(start),
        },
        &sentry.MonitorConfig{
            Schedule: sentry.CrontabSchedule("0 0 * * *"), // midnight daily
        },
    )
}
```

### Error handling in jobs

```go
func runSyncJob(ctx context.Context) {
    id := sentry.CaptureCheckIn(
        &sentry.CheckIn{MonitorSlug: "data-sync", Status: sentry.CheckInStatusInProgress},
        &sentry.MonitorConfig{
            Schedule:   sentry.IntervalSchedule(10, sentry.MonitorScheduleUnitMinute),
            MaxRuntime: 2,
        },
    )

    err := syncData(ctx)
    if err != nil {
        // Capture the error AND complete the check-in as error
        sentry.CaptureException(err)
        sentry.CaptureCheckIn(
            &sentry.CheckIn{ID: *id, MonitorSlug: "data-sync", Status: sentry.CheckInStatusError},
            nil,
        )
        return
    }

    sentry.CaptureCheckIn(
        &sentry.CheckIn{ID: *id, MonitorSlug: "data-sync", Status: sentry.CheckInStatusOK},
        nil,
    )
}
```

### Integration with robfig/cron

The SDK provides no built-in cron library wrappers — wrap manually:

```go
import "github.com/robfig/cron/v3"

c := cron.New()
c.AddFunc("@every 1h", func() {
    id := sentry.CaptureCheckIn(
        &sentry.CheckIn{
            MonitorSlug: "hourly-job",
            Status:      sentry.CheckInStatusInProgress,
        },
        &sentry.MonitorConfig{
            Schedule:      sentry.CrontabSchedule("0 * * * *"),
            MaxRuntime:    5,
            CheckInMargin: 2,
        },
    )

    err := doWork()

    status := sentry.CheckInStatusOK
    if err != nil {
        status = sentry.CheckInStatusError
    }
    sentry.CaptureCheckIn(
        &sentry.CheckIn{ID: *id, MonitorSlug: "hourly-job", Status: status},
        nil,
    )
})
c.Start()
defer c.Stop()
```

### Linking errors to the monitor

```go
sentry.ConfigureScope(func(scope *sentry.Scope) {
    scope.SetContext("monitor", sentry.Context{"slug": "my-monitor-slug"})
})
// Errors captured in this scope will be linked to the monitor in Sentry
```

## CaptureCheckIn API

```go
// Package-level (uses CurrentHub)
func CaptureCheckIn(checkIn *CheckIn, monitorConfig *MonitorConfig) *EventID

// Hub method
func (hub *Hub) CaptureCheckIn(checkIn *CheckIn, monitorConfig *MonitorConfig) *EventID
```

Both return `*EventID`. Always dereference with `*id` when passing to the completion call. Returns `nil` if no client is bound — guard with `if id != nil`.

## MonitorConfig Guidance

| Field | Recommended value | Notes |
|-------|------------------|-------|
| `Schedule` | Match your actual cron expression | Required |
| `CheckInMargin` | 1–5 min for fast jobs; 10–30 min for slow | Grace period before "missed" alert |
| `MaxRuntime` | 2–3× expected runtime | Triggers timeout alert |
| `Timezone` | e.g., `"America/New_York"` | Defaults to UTC if unset |
| `FailureIssueThreshold` | `2` | Avoid noise from one-off failures |
| `RecoveryThreshold` | `1` | Auto-resolve on first success |

Pass `MonitorConfig` on the **start** check-in only; pass `nil` on the completion call.

## Rate Limits

Sentry limits check-ins to **6 per minute per monitor + environment combination**. For jobs running more frequently than every 10 seconds, consider sampling.

## Best Practices

- Always send both a start (`InProgress`) and a completion (`OK`/`Error`) check-in — this enables timeout detection
- Use `defer sentry.Flush(2 * time.Second)` in `main()` — check-ins are queued async
- Set `MaxRuntime` to roughly 2–3× your expected job duration
- Set `FailureIssueThreshold: 2` to avoid noisy alerts from transient failures
- Create the monitor in the Sentry UI first, then use its slug — or let the SDK auto-create it on first check-in
- Don't reuse the same `MonitorSlug` for different jobs

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Check-ins not appearing | Check DSN; ensure `sentry.Flush()` is called; set `Debug: true` |
| Monitor shows "missed" unexpectedly | Increase `CheckInMargin`; ensure `InProgress` is sent before work starts |
| Monitor shows "timeout" | Increase `MaxRuntime`; check for job hangs |
| Nil pointer on `*checkinID` | `CaptureCheckIn` returns `nil` if no client — check `sentry.Init` was called |
| Duplicate issues for the same failure | Set `FailureIssueThreshold: 2` to batch consecutive failures |
| Check-ins rate limited | Reduce frequency; batch work; check Sentry plan limits |

---

## Reference: Error Monitoring

# Error Monitoring — Sentry Go SDK

> Minimum SDK: `github.com/getsentry/sentry-go` v0.9.0+

## Configuration

Key `ClientOptions` fields for error monitoring:

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `Dsn` | `string` | `""` | SDK disabled if empty |
| `AttachStacktrace` | `bool` | `false` | Stack traces on `CaptureMessage` calls |
| `SendDefaultPII` | `bool` | `false` | Include IP, request headers |
| `SampleRate` | `float64` | `1.0` | Error event sample rate (0.0 treated as 1.0) |
| `MaxBreadcrumbs` | `int` | `100` | Max breadcrumbs per event (negative = disabled) |
| `MaxErrorDepth` | `int` | `100` | Max depth for unwrapping error chains |
| `IgnoreErrors` | `[]string` | `nil` | Regex patterns; matched errors are dropped |
| `BeforeSend` | `func(*Event, *EventHint) *Event` | `nil` | Mutate or drop error events before sending |
| `BeforeBreadcrumb` | `func(*Breadcrumb, *BreadcrumbHint) *Breadcrumb` | `nil` | Mutate or drop breadcrumbs |

## Code Examples

### Basic setup

```go
import (
    "log"
    "os"
    "time"
    "github.com/getsentry/sentry-go"
)

func main() {
    err := sentry.Init(sentry.ClientOptions{
        Dsn:              os.Getenv("SENTRY_DSN"),
        Environment:      os.Getenv("SENTRY_ENVIRONMENT"),
        Release:          release, // inject via -ldflags
        AttachStacktrace: true,
        SendDefaultPII:   true,
    })
    if err != nil {
        log.Fatalf("sentry.Init: %s", err)
    }
    defer sentry.Flush(2 * time.Second)
}
```

### Capturing errors and messages

```go
// Error (any value implementing error interface) — unwraps full chain
sentry.CaptureException(err)

// Plain message (use AttachStacktrace: true for stack traces)
sentry.CaptureMessage("queue depth exceeded threshold")

// Fully manual event
sentry.CaptureEvent(&sentry.Event{
    Message: "payment gateway timeout",
    Level:   sentry.LevelError,
    Tags:    map[string]string{"gateway": "stripe"},
    Fingerprint: []string{"payment-gateway", "timeout"},
})
```

### Panic recovery

```go
// Simplest — defer in any function
func riskyOperation() {
    defer sentry.Recover()
    panic("something catastrophic")
}

// With context — makes context available in BeforeSend via hint.Context
func handleRequest(ctx context.Context) {
    defer sentry.RecoverWithContext(ctx)
    processRequest()
}

// Manual — needed when you must flush before process exit
func main() {
    defer func() {
        if err := recover(); err != nil {
            sentry.CurrentHub().Recover(err)
            sentry.Flush(5 * time.Second)
        }
    }()
}

// HTTP middleware recovery pattern
func SentryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                sentry.CurrentHub().Recover(err)
                sentry.Flush(2 * time.Second)
                http.Error(w, "Internal Server Error", http.StatusInternalServerError)
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

### Hub and scope — context enrichment

```go
// ConfigureScope — persistent modification of the current scope
sentry.ConfigureScope(func(scope *sentry.Scope) {
    scope.SetUser(sentry.User{
        ID:    "user-42",
        Email: "user@example.com",
    })
    scope.SetTag("region", "us-east-1")
    scope.SetContext("request_metadata", map[string]interface{}{
        "trace_id":   traceID,
        "account_id": accountID,
    })
})

// WithScope — isolated temporary scope; changes are discarded after the callback
sentry.WithScope(func(scope *sentry.Scope) {
    scope.SetTag("component", "checkout")
    scope.SetLevel(sentry.LevelWarning)
    sentry.CaptureException(err)
})
// ← scope changes above do NOT affect subsequent events
```

### Hub cloning for goroutines

```go
// ALWAYS clone the hub before spawning goroutines — global hub is not goroutine-safe
go func(hub *sentry.Hub) {
    hub.ConfigureScope(func(scope *sentry.Scope) {
        scope.SetTag("worker_id", "w-1")
    })
    hub.CaptureException(err)
}(sentry.CurrentHub().Clone())
```

### Breadcrumbs

```go
sentry.AddBreadcrumb(&sentry.Breadcrumb{
    Category: "auth",
    Message:  "user authenticated",
    Level:    sentry.LevelInfo,
})

sentry.AddBreadcrumb(&sentry.Breadcrumb{
    Type:     "http",
    Category: "http",
    Data: map[string]interface{}{
        "url":         "https://api.example.com/orders",
        "method":      "POST",
        "status_code": 503,
    },
    Level: sentry.LevelError,
})
```

### Error wrapping and chains

The SDK automatically traverses the full error chain from `CaptureException`. Each error becomes a separate exception entry in Sentry.

```go
// %w wrapping — both errors captured; dbErr shown as root cause
dbErr := errors.New("connection refused")
appErr := fmt.Errorf("failed to load user %d: %w", userID, dbErr)
sentry.CaptureException(appErr)

// errors.Join (Go 1.20+) — captured as Sentry exception group
combined := errors.Join(errors.New("email invalid"), errors.New("token expired"))
sentry.CaptureException(combined)
```

| Wrapping pattern | Interface | Mechanism |
|-----------------|-----------|-----------|
| `fmt.Errorf("%w", err)` | `Unwrap() error` | `"unwrap"` |
| `errors.Join(...)` | `Unwrap() []error` | `"chained"` |
| `pkg/errors` | `Cause() error` | `"cause"` |

Limit chain depth with `MaxErrorDepth` (default 100).

### BeforeSend hook

```go
sentry.Init(sentry.ClientOptions{
    Dsn: os.Getenv("SENTRY_DSN"),
    BeforeSend: func(event *sentry.Event, hint *sentry.EventHint) *sentry.Event {
        // Drop events from health check endpoints
        if event.Request != nil && strings.HasPrefix(event.Request.URL, "/health") {
            return nil // discard
        }
        // Scrub PII
        event.User.Email = ""
        event.User.IPAddress = ""
        // Enrich from original exception type
        if dbErr, ok := hint.OriginalException.(*DatabaseError); ok {
            event.Tags["db.table"] = dbErr.Table
        }
        // Access context set by RecoverWithContext
        if hint.Context != nil {
            if reqID, ok := hint.Context.Value(RequestIDKey).(string); ok {
                event.Tags["request_id"] = reqID
            }
        }
        return event
    },
    // BeforeSend is NOT called for transaction events — use BeforeSendTransaction for those
    BeforeSendTransaction: func(event *sentry.Event, hint *sentry.EventHint) *sentry.Event {
        if event.Transaction == "GET /healthz" {
            return nil
        }
        return event
    },
})
```

### Event processors

```go
// Scope-level (per-request enrichment — preferred)
sentry.ConfigureScope(func(scope *sentry.Scope) {
    scope.AddEventProcessor(func(event *sentry.Event, hint *sentry.EventHint) *sentry.Event {
        event.Tags["request_id"] = r.Header.Get("X-Request-ID")
        event.Tags["tenant_id"]  = r.Header.Get("X-Tenant-ID")
        return event
    })
})

// Client-level (all events from this client)
client, _ := sentry.NewClient(sentry.ClientOptions{Dsn: os.Getenv("SENTRY_DSN")})
client.AddEventProcessor(func(event *sentry.Event, hint *sentry.EventHint) *sentry.Event {
    event.Tags["build_sha"] = os.Getenv("GIT_SHA")
    return event
})
```

Processor execution order: scope processors (LIFO) → client processors → `BeforeSend`.

### Fingerprinting and custom grouping

```go
// One-off — override grouping for a specific error type
sentry.WithScope(func(scope *sentry.Scope) {
    scope.SetFingerprint([]string{"database-connection-error"})
    sentry.CaptureException(err)
})

// Extend default grouping (keeps stack trace + adds discriminators)
BeforeSend: func(event *sentry.Event, hint *sentry.EventHint) *sentry.Event {
    if rpcErr, ok := hint.OriginalException.(MyRPCError); ok {
        event.Fingerprint = []string{
            "{{ default }}",
            rpcErr.FunctionName(),
            strconv.Itoa(rpcErr.ErrorCode()),
        }
    }
    return event
},
```

### Flush patterns

```go
// Recommended: defer in main()
defer sentry.Flush(2 * time.Second)

// os.Exit() bypasses defer — call explicitly
sentry.Flush(2 * time.Second)
os.Exit(1)

// Context-based
ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
defer cancel()
sentry.FlushWithContext(ctx)

// Synchronous transport (no flush needed — every send blocks)
transport := sentry.NewHTTPSyncTransport()
transport.Timeout = 3 * time.Second
sentry.Init(sentry.ClientOptions{Dsn: "...", Transport: transport})
```

## Scope API Reference

```go
scope.SetUser(sentry.User{ID: "42", Email: "user@example.com"})
scope.SetTag("key", "value")
scope.SetTags(map[string]string{"k": "v"})
scope.SetExtra("key", value)           // deprecated — prefer SetContext
scope.SetContext("key", map[string]interface{}{"field": "value"})
scope.SetLevel(sentry.LevelError)      // "debug" | "info" | "warning" | "error" | "fatal"
scope.SetRequest(r *http.Request)
scope.SetFingerprint([]string{"my-group"})
scope.AddBreadcrumb(bc, limit)
scope.ClearBreadcrumbs()
scope.AddEventProcessor(func(*sentry.Event, *sentry.EventHint) *sentry.Event)
scope.Clear()
scope.Clone() *sentry.Scope
```

## Best Practices

- Call `sentry.Init()` once in `main()`, before any goroutines or handlers start
- Always check the error returned by `sentry.Init()`
- Always `defer sentry.Flush(2 * time.Second)` in `main()`; call it explicitly before `os.Exit()`
- Clone the hub before passing it to goroutines: `hub := sentry.CurrentHub().Clone()`
- Use `WithScope` for one-off context; use `ConfigureScope` for persistent session context
- Prefer `SetContext` over `SetExtra` for structured data (Extra is deprecated)
- Use `BeforeSend` to strip PII — never send raw email/IP unless `SendDefaultPII: true` is intentional
- Set `MaxErrorDepth` to a sensible value (5–10) for deeply wrapped error chains

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Set `Debug: true`; verify DSN; ensure `sentry.Flush()` is called |
| Missing stack traces on messages | Set `AttachStacktrace: true` in `ClientOptions` |
| Goroutine events missing scope data | Clone hub before goroutine: `sentry.CurrentHub().Clone()` |
| Panics not captured | Register framework middleware before handlers; or add `defer sentry.Recover()` |
| `defer sentry.Flush` not running | `os.Exit()` skips defers — call `sentry.Flush()` explicitly |
| `SampleRate: 0.0` still sending | `0.0` is treated as `1.0`; to drop all, set `Dsn: ""` |
| Error chain shows only top error | Check `MaxErrorDepth`; ensure errors use `%w` or implement `Unwrap()` |
| BeforeSend not called for transactions | Use `BeforeSendTransaction` for transaction/performance events |

---

## Reference: Logging

# Logging — Sentry Go SDK

> Minimum SDK: `github.com/getsentry/sentry-go` v0.33.0+  
> Minimum SDK for zap integration: v0.43.0+

## Configuration

Enable Sentry Logs in `sentry.Init`:

```go
sentry.Init(sentry.ClientOptions{
    Dsn:        os.Getenv("SENTRY_DSN"),
    EnableLogs: true, // REQUIRED — logs are off by default
})
```

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `EnableLogs` | `bool` | `false` | Enable Sentry Logs feature |
| `BeforeSendLog` | `func(*Log) *Log` | `nil` | Mutate or drop log entries before sending |

> If `EnableLogs` is `false`, `sentry.NewLogger(ctx)` returns a **no-op logger** — all calls are silently discarded.

## Code Examples

### Native Sentry logger

```go
import (
    "context"
    "time"
    "github.com/getsentry/sentry-go"
    "github.com/getsentry/sentry-go/attribute"
)

func main() {
    sentry.Init(sentry.ClientOptions{
        Dsn:        os.Getenv("SENTRY_DSN"),
        EnableLogs: true,
    })
    defer sentry.Flush(2 * time.Second)

    ctx := context.Background()
    logger := sentry.NewLogger(ctx)

    // Basic logging
    logger.Info().Emit("server started")
    logger.Warn().Emitf("queue depth: %d", 42)
    logger.Error().Emit("database connection lost")

    // Per-entry attributes (chained, non-persistent)
    logger.Info().
        String("request.id", "abc-123").
        Int("status.code", 200).
        Bool("cache.hit", true).
        Float64("latency.ms", 12.3).
        Emitf("request completed: %s", r.URL.Path)

    // Permanent logger-level attributes (all subsequent entries include these)
    logger.SetAttributes(
        attribute.String("service", "payment-api"),
        attribute.String("version", "2.1.0"),
    )

    // Switch context on a single entry (for trace correlation)
    logger.Info().WithCtx(requestCtx).Emit("handling request")
}
```

### Log levels

| Method | OTel Severity | Use for |
|--------|--------------|---------|
| `logger.Trace()` | 1 | Very detailed debugging |
| `logger.Debug()` | 5 | Development debugging |
| `logger.Info()` | 9 | Informational events |
| `logger.Warn()` | 13 | Warnings, recoverable issues |
| `logger.Error()` | 17 | Errors requiring attention |
| `logger.Fatal()` | 21 | Fatal — logs then calls `os.Exit(1)` |
| `logger.Panic()` | 21 | Fatal — logs then panics |
| `logger.LFatal()` | 21 | Logs at fatal level without exiting |

### BeforeSendLog — filtering logs

```go
sentry.Init(sentry.ClientOptions{
    Dsn:        os.Getenv("SENTRY_DSN"),
    EnableLogs: true,
    BeforeSendLog: func(log *sentry.Log) *sentry.Log {
        // Drop trace and debug logs
        if log.Severity <= sentry.LogSeverityDebug {
            return nil
        }
        // Drop logs from noisy subsystem
        if v, ok := log.Attributes["service"]; ok && v.String() == "health-checker" {
            return nil
        }
        return log
    },
})
```

`sentry.Log` struct fields: `Timestamp`, `TraceID`, `SpanID`, `Level`, `Severity` (int), `Body`, `Attributes`.

### Auto-attached attributes

The SDK automatically appends these to every log entry:

| Attribute | Source |
|-----------|--------|
| `sentry.release` | `ClientOptions.Release` |
| `sentry.environment` | `ClientOptions.Environment` |
| `sentry.server.address` | `ClientOptions.ServerName` or `os.Hostname()` |
| `sentry.sdk.name` / `.version` | SDK identifier |
| `sentry.message.template` | Set when `Emitf()` is used |
| `sentry.message.parameters.0`, `.1`… | Parameters passed to `Emitf()` |
| `user.id`, `user.name`, `user.email` | Set if user is in scope |

## Logging Integrations

### Logrus

```bash
go get github.com/getsentry/sentry-go/logrus
```

Two hook modes — use them independently or together:

```go
import (
    "github.com/sirupsen/logrus"
    "github.com/getsentry/sentry-go"
    sentrylogrus "github.com/getsentry/sentry-go/logrus"
)

logger := logrus.New()

// Log hook: sends logrus entries as Sentry Log entries (requires EnableLogs: true)
logHook, _ := sentrylogrus.NewLogHook(
    []logrus.Level{logrus.InfoLevel, logrus.WarnLevel},
    sentry.ClientOptions{Dsn: os.Getenv("SENTRY_DSN"), EnableLogs: true},
)
defer logHook.Flush(5 * time.Second)

// Event hook: sends logrus entries as Sentry Events (issues/errors)
eventHook, _ := sentrylogrus.NewEventHook(
    []logrus.Level{logrus.ErrorLevel, logrus.FatalLevel, logrus.PanicLevel},
    sentry.ClientOptions{Dsn: os.Getenv("SENTRY_DSN")},
)
defer eventHook.Flush(5 * time.Second)

logger.AddHook(logHook)
logger.AddHook(eventHook)

// Flush before os.Exit on logger.Fatal()
logrus.RegisterExitHandler(func() {
    logHook.Flush(5 * time.Second)
    eventHook.Flush(5 * time.Second)
})

logger.Info("service started")
logger.WithField("user", sentry.User{ID: "u1"}).Error("payment failed")
```

**Logrus level mapping:**

| Logrus level | Sentry level |
|-------------|--------------|
| Trace, Debug | `debug` |
| Info | `info` |
| Warn | `warning` |
| Error | `error` |
| Fatal, Panic | `fatal` |

**Special field names** (auto-mapped to Sentry metadata):

| Field | Type | Maps to |
|-------|------|---------|
| `"request"` | `*http.Request` | `sentry.Request` |
| `"user"` | `sentry.User` | scope user |
| `"transaction"` | `string` | event transaction ID |
| `"fingerprint"` | `[]string` | event fingerprint |

### slog (Go 1.21+)

```bash
go get github.com/getsentry/sentry-go/slog
```

```go
import (
    "context"
    "log/slog"
    "github.com/getsentry/sentry-go"
    sentryslog "github.com/getsentry/sentry-go/slog"
)

sentry.Init(sentry.ClientOptions{
    Dsn:        os.Getenv("SENTRY_DSN"),
    EnableLogs: true,
})
defer sentry.Flush(5 * time.Second)

ctx := context.Background()
handler := sentryslog.Option{
    // These levels are sent as Sentry Events (issues)
    EventLevel: []slog.Level{slog.LevelError, sentryslog.LevelFatal},
    // These levels are sent as Sentry Log entries
    LogLevel: []slog.Level{slog.LevelInfo, slog.LevelWarn, slog.LevelError},
    AddSource: true, // include file:line in events
}.NewSentryHandler(ctx)

logger := slog.New(handler)
logger.Info("server started", "port", 8080)
logger.Warn("rate limit approaching", "requests", 950)
logger.Error("database connection failed", "host", "db.example.com")
```

**slog level mapping:**

| slog.Level range | Sentry method |
|-----------------|---------------|
| `< -4` | `Trace` |
| `-4` to `-1` | `Debug` |
| `0` to `3` | `Info` |
| `4` to `7` | `Warn` |
| `8` to `11` | `Error` |
| `≥ 12` (`LevelFatal`) | `Fatal` |

`sentryslog.LevelFatal` is defined as `slog.Level(12)`.

### zerolog

```bash
go get github.com/getsentry/sentry-go/zerolog
```

> **Note:** The zerolog integration sends as **Sentry Events** (issues), not Sentry Log entries. It does not support structured logs.

```go
import (
    "github.com/rs/zerolog"
    "github.com/getsentry/sentry-go"
    sentryzerolog "github.com/getsentry/sentry-go/zerolog"
)

writer, _ := sentryzerolog.New(sentryzerolog.Config{
    ClientOptions: sentry.ClientOptions{Dsn: os.Getenv("SENTRY_DSN")},
    Options: sentryzerolog.Options{
        Levels:          []zerolog.Level{zerolog.ErrorLevel, zerolog.FatalLevel},
        WithBreadcrumbs: true,  // non-error logs become breadcrumbs
        FlushTimeout:    3 * time.Second,
    },
})
defer writer.Close()

logger := zerolog.New(writer).With().Timestamp().Logger()
logger.Info().Msg("breadcrumb only")
logger.Error().Str("user", "u1").Msg("captured as Sentry event")
```

**Special field names** (same as logrus, auto-mapped):
`"request"` → `*http.Request`, `"user"` → `sentry.User`, `"transaction"` → string, `"fingerprint"` → `[]string`

### zap (v0.43.0+)

```bash
go get github.com/getsentry/sentry-go/zap
```

```go
import (
    "context"
    "github.com/getsentry/sentry-go"
    sentryzap "github.com/getsentry/sentry-go/zap"
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
    "os"
)

sentry.Init(sentry.ClientOptions{
    Dsn:        os.Getenv("SENTRY_DSN"),
    EnableLogs: true,
})
defer sentry.Flush(2 * time.Second)

ctx := context.Background()
sentryCore := sentryzap.NewSentryCore(ctx, sentryzap.Option{
    Level:     []zapcore.Level{zapcore.InfoLevel, zapcore.WarnLevel, zapcore.ErrorLevel},
    AddCaller: true,
})

// Tee with console output
consoleCore := zapcore.NewCore(
    zapcore.NewConsoleEncoder(zap.NewProductionEncoderConfig()),
    zapcore.AddSync(os.Stdout),
    zapcore.DebugLevel,
)
logger := zap.New(zapcore.NewTee(consoleCore, sentryCore), zap.AddCaller())

// Attach trace context to log entries
span := sentry.StartSpan(ctx, "my-operation")
defer span.Finish()
logger.With(sentryzap.Context(span.Context())).Info("within span",
    zap.String("version", "1.0"),
    zap.Float64("cpu", 0.42),
)
```

**zap level mapping:**

| zap level | Sentry method |
|-----------|---------------|
| Debug | `Debug` |
| Info | `Info` |
| Warn | `Warn` |
| Error, DPanic | `Error` |
| Panic, Fatal | `LFatal` (zap handles the actual exit/panic) |

## Integration Comparison

| Library | Package | Sends as | `EnableLogs` required |
|---------|---------|----------|----------------------|
| Native | `sentry-go` | Sentry Logs | ✅ Yes |
| logrus (log hook) | `sentry-go/logrus` | Sentry Logs | ✅ Yes |
| logrus (event hook) | `sentry-go/logrus` | Sentry Events | ❌ No |
| slog | `sentry-go/slog` | Both (configurable) | ✅ For logs |
| zerolog | `sentry-go/zerolog` | Sentry Events + Breadcrumbs | ❌ No |
| zap | `sentry-go/zap` | Sentry Logs | ✅ Yes |

## Best Practices

- Enable both a log hook and an event hook for logrus — logs for visibility, events for alerting
- For slog, configure `EventLevel` to `[slog.LevelError, LevelFatal]` and `LogLevel` for the rest
- Call `hook.Flush()` (logrus) or `writer.Close()` (zerolog) before program exit
- Use `WithCtx(requestCtx)` on log entries inside HTTP handlers for trace correlation
- Set `sentry.LogSeverityInfo` as the minimum in `BeforeSendLog` to avoid sending noisy debug logs

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing in Sentry | Ensure `EnableLogs: true` in `ClientOptions` |
| `NewLogger` returns no-op | `EnableLogs` is false or no client is bound to the hub |
| Logrus `Fatal` not flushing | Register `logrus.RegisterExitHandler` to flush hooks before exit |
| zerolog entries not appearing | zerolog sends Events, not Logs — check the Issues section, not Logs |
| Logs missing trace context | Use `logger.Info().WithCtx(spanCtx).Emit(...)` to attach span context |
| Too many logs in Sentry | Use `BeforeSendLog` to filter by severity or attribute |

---

## Reference: Metrics

# Metrics — Sentry Go SDK

> Minimum SDK: `github.com/getsentry/sentry-go` v0.42.0+  
> **⚠️ Open Beta** — API may change in future releases.

## Configuration

```go
sentry.Init(sentry.ClientOptions{
    Dsn: os.Getenv("SENTRY_DSN"),
    // Metrics are enabled by default. Disable with:
    DisableMetrics: false,
    // Filter or mutate metrics before sending:
    BeforeSendMetric: func(metric *sentry.Metric) *sentry.Metric {
        return metric // return nil to drop
    },
})
```

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `DisableMetrics` | `bool` | `false` | Set `true` to disable all metrics emission |
| `BeforeSendMetric` | `func(*Metric) *Metric` | `nil` | Mutate or drop individual metrics |

## Meter API

Create a `Meter` from any context:

```go
meter := sentry.NewMeter(ctx)
```

Returns a no-op `Meter` (silently drops all calls) if no client is bound to the hub or `DisableMetrics: true`.

### Meter interface

```go
type Meter interface {
    Count(name string, count int64, opts ...MeterOption)
    Gauge(name string, value float64, opts ...MeterOption)
    Distribution(name string, sample float64, opts ...MeterOption)
    WithCtx(ctx context.Context) Meter       // returns meter linked to new context/span
    SetAttributes(attrs ...attribute.Builder) // permanent attributes on all metrics from this meter
}
```

> **The Go SDK has exactly three metric types: `Count`, `Gauge`, `Distribution`. Sets and timing helpers are not implemented.**

## Code Examples

### Basic metrics

```go
import (
    "context"
    "time"
    "github.com/getsentry/sentry-go"
    "github.com/getsentry/sentry-go/attribute"
)

func main() {
    sentry.Init(sentry.ClientOptions{Dsn: os.Getenv("SENTRY_DSN")})
    defer sentry.Flush(2 * time.Second)

    meter := sentry.NewMeter(context.Background())

    // Counter — integer increments
    meter.Count("emails.sent", 3,
        sentry.WithAttributes(
            attribute.String("provider", "sendgrid"),
            attribute.Bool("transactional", true),
        ),
    )

    // Gauge — current snapshot value
    meter.Gauge("queue.depth", 142.0,
        sentry.WithAttributes(
            attribute.String("queue.name", "orders"),
        ),
    )

    // Distribution — histogram / percentile-friendly samples
    meter.Distribution("api.response_time", 187.5,
        sentry.WithUnit(sentry.UnitMillisecond),
        sentry.WithAttributes(
            attribute.String("endpoint", "/checkout"),
            attribute.String("method", "POST"),
        ),
    )
}
```

### Permanent meter attributes

```go
meter := sentry.NewMeter(context.Background())
meter.SetAttributes(
    attribute.String("service", "payment-api"),
    attribute.String("region", "us-east-1"),
)

// All metrics from this meter include service and region
meter.Count("orders.created", 1)
meter.Gauge("cpu.usage", 0.73, sentry.WithUnit(sentry.UnitRatio))
```

### Trace-linked metrics

Associate metrics with the current request's trace span using `WithCtx`:

```go
http.HandleFunc("/checkout", func(w http.ResponseWriter, r *http.Request) {
    // meter.WithCtx links metrics to the active span in r.Context()
    meter.WithCtx(r.Context()).Count("checkout.attempts", 1,
        sentry.WithAttributes(
            attribute.String("method", r.Method),
        ),
    )
    // ... handler logic
})
```

### Timing a operation with Distribution

There is no built-in timer — measure elapsed time manually:

```go
func processOrder(ctx context.Context, orderID string) error {
    start := time.Now()

    err := doWork(ctx, orderID)

    elapsed := float64(time.Since(start).Milliseconds())
    meter.WithCtx(ctx).Distribution("order.processing_time", elapsed,
        sentry.WithUnit(sentry.UnitMillisecond),
        sentry.WithAttributes(
            attribute.String("order.id", orderID),
            attribute.Bool("success", err == nil),
        ),
    )
    return err
}
```

### Filtering metrics with BeforeSendMetric

```go
sentry.Init(sentry.ClientOptions{
    Dsn: os.Getenv("SENTRY_DSN"),
    BeforeSendMetric: func(m *sentry.Metric) *sentry.Metric {
        // Drop sub-millisecond distributions (noise)
        if m.Type == sentry.MetricTypeDistribution {
            if v, ok := m.Value.Float64(); ok && v < 1.0 {
                return nil
            }
        }
        // Drop metrics from test environment
        if env, ok := m.Attributes["sentry.environment"]; ok && env.String() == "test" {
            return nil
        }
        return m
    },
})
```

### Scope override

Override per-metric user/environment context without changing the global scope:

```go
customScope := sentry.NewScope()
customScope.SetUser(sentry.User{ID: "user-42"})

meter.Gauge("memory.usage", 512.0,
    sentry.WithUnit(sentry.UnitMebibyte),
    sentry.WithScopeOverride(customScope),
)
```

## MeterOption Reference

```go
sentry.WithUnit(unit string)                    // set measurement unit
sentry.WithAttributes(attrs ...attribute.Builder) // per-call attributes
sentry.WithScopeOverride(scope *sentry.Scope)   // override scope for this metric
```

## Unit Constants

**Duration:**

| Constant | Value |
|----------|-------|
| `UnitNanosecond` | `"nanosecond"` |
| `UnitMicrosecond` | `"microsecond"` |
| `UnitMillisecond` | `"millisecond"` |
| `UnitSecond` | `"second"` |
| `UnitMinute` | `"minute"` |
| `UnitHour` | `"hour"` |
| `UnitDay` | `"day"` |
| `UnitWeek` | `"week"` |

**Information:**

| Constant | Value |
|----------|-------|
| `UnitByte` | `"byte"` |
| `UnitKilobyte` | `"kilobyte"` |
| `UnitMegabyte` | `"megabyte"` |
| `UnitGigabyte` | `"gigabyte"` |
| `UnitMebibyte` | `"mebibyte"` |
| `UnitGibibyte` | `"gibibyte"` |

**Fraction:**

| Constant | Value |
|----------|-------|
| `UnitRatio` | `"ratio"` |
| `UnitPercent` | `"percent"` |

## Attribute Package

```go
import "github.com/getsentry/sentry-go/attribute"

attribute.String(key, value string) Builder
attribute.Int(key string, value int) Builder
attribute.Int64(key string, value int64) Builder
attribute.Float64(key string, v float64) Builder
attribute.Bool(key string, v bool) Builder
```

## Auto-Attached Attributes

| Attribute | Source |
|-----------|--------|
| `sentry.release` | `ClientOptions.Release` |
| `sentry.environment` | `ClientOptions.Environment` |
| `sentry.server.address` | `ClientOptions.ServerName` or `os.Hostname()` |
| `sentry.sdk.name` / `.version` | SDK identifier |

## Metric Type Reference

| Method | Value type | Use for |
|--------|-----------|---------|
| `Count` | `int64` | Incrementing counters (events, errors, requests) |
| `Gauge` | `float64` | Current state snapshot (queue depth, memory, connections) |
| `Distribution` | `float64` | Variable measurements supporting percentiles (latency, file sizes) |

Note: `Count` takes `int64`, not `int`. `IntervalSchedule` also takes `int64`.

## Best Practices

- Use `Count` for events that accumulate (requests served, emails sent, errors thrown)
- Use `Gauge` for values that represent current state (queue depth, active connections, cache size)
- Use `Distribution` for latency and sizes — it enables P50/P95/P99 analysis
- Keep metric names lowercase, dot-separated (`api.response_time`, `queue.depth`)
- Avoid high-cardinality tag values (user IDs, request IDs) — prefer categorical values
- Call `meter.SetAttributes()` once with service-level tags rather than repeating them on every call
- Use `meter.WithCtx(ctx)` inside HTTP handlers to link metrics to the active trace span

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Metrics not appearing | Check `DisableMetrics` is not `true`; verify `sentry.Flush()` is called |
| `NewMeter` returns no-op | No client bound to hub; check `sentry.Init` was called |
| `Count` type error | `count` parameter is `int64`, not `int` — use explicit `int64(n)` cast |
| Missing attributes | Use `meter.SetAttributes()` for permanent attributes; they apply to all subsequent calls |
| High-cardinality warnings | Avoid using dynamic values (user IDs, UUIDs) as tag values |

---

## Reference: Profiling

# Profiling — Sentry Go SDK

> **⚠️ Profiling is not available for Go.**
>
> Profiling support was added in v0.22.0 as an alpha feature and **removed in v0.31.0** (breaking change). As of v0.43.0, `ProfilesSampleRate` does not exist in `ClientOptions` and the field will not compile.

## Current Status

The Sentry Go SDK **does not support** transaction-based or continuous profiling. The `/platforms/go/profiling/` documentation page returns 404.

```go
// ❌ This does NOT compile on v0.31.0+
sentry.Init(sentry.ClientOptions{
    EnableTracing:      true,
    TracesSampleRate:   1.0,
    ProfilesSampleRate: 1.0,  // unknown field — compile error
})
```

## Alternatives

For Go application profiling, use these standard approaches independently of Sentry:

**pprof (stdlib):**
```go
import _ "net/http/pprof"

// Exposes /debug/pprof/ on your HTTP server
http.ListenAndServe(":6060", nil)
```

**Continuous profiling services:**
- [Pyroscope](https://pyroscope.io/) — open-source continuous profiling
- [Google Cloud Profiler](https://cloud.google.com/profiler)
- [Datadog Continuous Profiler](https://docs.datadoghq.com/profiler/)

## Check for Future Support

Monitor the [sentry-go releases](https://github.com/getsentry/sentry-go/releases) and [docs.sentry.io/platforms/go/](https://docs.sentry.io/platforms/go/) for profiling to be re-introduced.

---

## Reference: Tracing

# Tracing — Sentry Go SDK

> Minimum SDK: `github.com/getsentry/sentry-go` v0.9.0+

## Configuration

```go
sentry.Init(sentry.ClientOptions{
    Dsn:              os.Getenv("SENTRY_DSN"),
    EnableTracing:    true,      // REQUIRED — tracing is off by default
    TracesSampleRate: 1.0,       // start at 1.0 for dev; lower in production
})
```

Key tracing fields in `ClientOptions`:

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `EnableTracing` | `bool` | `false` | Must be `true` to enable tracing |
| `TracesSampleRate` | `float64` | `0.0` | Uniform sample rate [0.0–1.0] |
| `TracesSampler` | `TracesSampler` | `nil` | Custom per-transaction sampling; overrides `TracesSampleRate` |
| `MaxSpans` | `int` | `1000` | Max child spans per transaction |
| `TracePropagationTargets` | `[]string` | `nil` | URLs to inject trace headers into (nil = all) |
| `PropagateTraceparent` | `bool` | `false` | Also propagate W3C `traceparent` header |
| `TraceIgnoreStatusCodes` | `[][]int` | `[[404]]` | HTTP codes that skip trace creation |
| `BeforeSendTransaction` | `func` | `nil` | Mutate or drop transaction events |

## Code Examples

### Custom sampler

Use `TracesSampler` instead of `TracesSampleRate` for per-transaction control. Setting both — sampler wins.

```go
sentry.Init(sentry.ClientOptions{
    Dsn:          os.Getenv("SENTRY_DSN"),
    EnableTracing: true,
    TracesSampler: sentry.TracesSampler(func(ctx sentry.SamplingContext) float64 {
        switch ctx.Span.Name {
        case "GET /healthz", "GET /metrics":
            return 0.0  // never sample
        case "POST /checkout":
            return 1.0  // always sample
        default:
            return 0.1  // 10% of everything else
        }
    }),
})
```

`SamplingContext` fields:
- `ctx.Span` — current span (always non-nil)
- `ctx.Parent` — parent span (nil for root transactions)

### Manual transactions and spans

```go
// Start a root transaction
tx := sentry.StartTransaction(ctx, "process-order",
    sentry.WithOpName("task"),
    sentry.WithTransactionSource(sentry.SourceCustom),
)
defer tx.Finish()

// Start a child span — pass tx.Context() to nest under the transaction
dbSpan := sentry.StartSpan(tx.Context(), "db.query")
dbSpan.Description = "INSERT INTO orders (user_id, total) VALUES (?, ?)"
dbSpan.SetData("db.system", "postgresql")
dbSpan.SetData("db.rows_affected", 1)
defer dbSpan.Finish()

// Alternative: StartChild on the parent span directly
cacheSpan := tx.StartChild("cache.get",
    sentry.WithDescription("get:user:42"),
)
defer cacheSpan.Finish()
```

### HTTP handler with manual transaction

```go
http.HandleFunc("/users", func(w http.ResponseWriter, r *http.Request) {
    hub := sentry.CurrentHub().Clone()
    ctx := sentry.SetHubOnContext(r.Context(), hub)

    tx := sentry.StartTransaction(ctx,
        fmt.Sprintf("%s %s", r.Method, r.URL.Path),
        sentry.WithOpName("http.server"),
        sentry.ContinueFromRequest(r),           // link to incoming distributed trace
        sentry.WithTransactionSource(sentry.SourceURL),
    )
    defer tx.Finish()

    users, err := fetchUsers(tx.Context())
    if err != nil {
        hub.CaptureException(err)
        http.Error(w, "internal error", 500)
        return
    }
    fmt.Fprintf(w, "%d users", len(users))
})

func fetchUsers(ctx context.Context) ([]string, error) {
    span := sentry.StartSpan(ctx, "db.query")
    span.Description = "SELECT id, name FROM users"
    span.SetData("db.system", "postgresql")
    defer span.Finish()

    time.Sleep(10 * time.Millisecond)
    span.Status = sentry.SpanStatusOK
    return []string{"alice", "bob"}, nil
}
```

### Setting span status and data

```go
span := sentry.StartSpan(ctx, "http.client")
span.Description = "GET https://api.stripe.com/v1/charges"
span.SetData("http.request.method", "GET")
span.SetData("server.address", "api.stripe.com")

req, _ := http.NewRequestWithContext(span.Context(), "GET", "https://api.stripe.com/v1/charges", nil)
resp, err := http.DefaultClient.Do(req)
if err != nil {
    span.Status = sentry.SpanStatusInternalError
} else {
    span.Status = sentry.HTTPtoSpanStatus(resp.StatusCode)
    span.SetData("http.response.status_code", resp.StatusCode)
}
defer span.Finish()
```

> `span.Status` is set **directly** — there is no `SetStatus()` method.

### Retrieving active transaction or span from context

```go
// Root transaction
tx := sentry.TransactionFromContext(ctx)
if tx != nil {
    tx.SetTag("user_id", "42")
    tx.Name = "custom-name"
}

// Innermost span (may be a child)
span := sentry.SpanFromContext(ctx)
span.SetData("result_count", 47)
```

## Framework Middleware

All framework middlewares automatically start a root transaction per request and continue incoming distributed traces.

| Framework | Import | Middleware call | Transaction source |
|-----------|--------|----------------|-------------------|
| `net/http` | `sentry-go/http` | `sentryhttp.New(opts).Handle(mux)` | `SourceURL` |
| Gin | `sentry-go/gin` | `router.Use(sentrygin.New(opts))` | `SourceRoute` |
| Echo | `sentry-go/echo` | `e.Use(sentryecho.New(opts))` | `SourceRoute` |
| Fiber | `sentry-go/fiber` | `app.Use(sentryfiber.New(opts))` | `SourceURL` |
| Iris | `sentry-go/iris` | `app.Use(sentryiris.New(opts))` | `SourceRoute` |

Accessing the current transaction in a framework handler:

```go
// net/http — use the standard context
tx := sentry.TransactionFromContext(r.Context())

// Gin
tx := sentrygin.GetSpanFromContext(c)

// Echo
tx := sentryecho.GetSpanFromContext(c)

// Fiber
tx := sentryfiber.GetSpanFromContext(c)

// Iris
tx := sentryiris.GetSpanFromContext(c)
```

Adding a child span in a Gin handler:

```go
router.GET("/users/:id", func(c *gin.Context) {
    tx := sentrygin.GetSpanFromContext(c)

    dbSpan := sentry.StartSpan(tx.Context(), "db.query")
    dbSpan.Description = "SELECT * FROM users WHERE id = ?"
    defer dbSpan.Finish()

    // handler logic...
})
```

## Distributed Tracing

Sentry propagates two headers:

| Header | Constant | Purpose |
|--------|----------|---------|
| `sentry-trace` | `sentry.SentryTraceHeader` | Links spans across services |
| `baggage` | `sentry.SentryBaggageHeader` | Dynamic Sampling Context |

**Consuming an incoming trace (downstream service):**

```go
// ContinueFromRequest reads both sentry-trace and baggage headers automatically
tx := sentry.StartTransaction(ctx, "GET /api/check",
    sentry.WithOpName("http.server"),
    sentry.ContinueFromRequest(r),
    sentry.WithTransactionSource(sentry.SourceRoute),
)
defer tx.Finish()
```

**Propagating to an outgoing request (upstream service):**

```go
func callDownstream(ctx context.Context, url string) {
    hub := sentry.GetHubFromContext(ctx)

    req, _ := http.NewRequest("GET", url, nil)
    req.Header.Set(sentry.SentryTraceHeader, hub.GetTraceparent())
    req.Header.Set(sentry.SentryBaggageHeader, hub.GetBaggage())

    http.DefaultClient.Do(req)
}
```

**Hub header methods:**

```go
hub.GetTraceparent()    // sentry-trace format: "traceID-spanID-sampled"
hub.GetTraceparentW3C() // W3C format: "00-traceID-spanID-01"
hub.GetBaggage()        // "sentry-trace_id=...,sentry-environment=production,..."
```

Both `sentry-trace` AND `baggage` headers must be propagated for correct Dynamic Sampling Context.

### OpenTelemetry bridge

For projects already using OpenTelemetry, forward OTel spans to Sentry without changing instrumentation:

```go
import (
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    sentryotel "github.com/getsentry/sentry-go/otel"
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/propagation"
)

sentry.Init(sentry.ClientOptions{
    Dsn:              os.Getenv("SENTRY_DSN"),
    EnableTracing:    true,
    TracesSampleRate: 1.0,
})

tp := sdktrace.NewTracerProvider(
    sdktrace.WithSpanProcessor(sentryotel.NewSentrySpanProcessor()),
)
otel.SetTracerProvider(tp)
otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
    propagation.TraceContext{},
    propagation.Baggage{},
    sentryotel.NewSentryPropagator(),
))
```

When using OTel, pass the OTel context explicitly when capturing errors — global `sentry.CaptureException` does not auto-link:

```go
hub := sentry.CurrentHub()
hub.Client().CaptureException(
    err,
    &sentry.EventHint{Context: otelCtx},
    hub.Scope(),
)
```

## SpanOption Reference

```go
sentry.WithOpName("http.server")                 // sets span.Op
sentry.WithDescription("SELECT * FROM users")    // sets span.Description
sentry.WithTransactionName("checkout")           // sets root span name
sentry.WithTransactionSource(sentry.SourceRoute) // transaction naming source
sentry.WithSpanSampled(sentry.SampledTrue)       // force-sample this span
sentry.ContinueFromRequest(r *http.Request)      // read sentry-trace + baggage from request
sentry.ContinueFromHeaders(trace, baggage string)// pass raw header strings
sentry.ContinueTrace(hub, traceparent, baggage)  // hub-aware form
```

## TransactionSource Constants

| Constant | Value | Use when... |
|----------|-------|-------------|
| `SourceURL` | `"url"` | Raw URL path (low-cardinality risk) |
| `SourceRoute` | `"route"` | Parameterised template, e.g. `/users/:id` — **preferred** |
| `SourceView` | `"view"` | View/controller name |
| `SourceCustom` | `"custom"` | Manually set name |
| `SourceTask` | `"task"` | Background task name |

Use `SourceRoute` with parameterised paths to prevent high-cardinality grouping in Sentry's Performance UI.

## SpanStatus Constants

Set directly: `span.Status = sentry.SpanStatusOK`

| Constant | When to use |
|----------|-------------|
| `SpanStatusOK` | Success |
| `SpanStatusInternalError` | Unhandled server error |
| `SpanStatusNotFound` | Resource not found |
| `SpanStatusPermissionDenied` | Auth failure |
| `SpanStatusDeadlineExceeded` | Timeout |
| `SpanStatusInvalidArgument` | Bad input |
| `SpanStatusUnavailable` | Service unavailable |

Or derive from HTTP response: `span.Status = sentry.HTTPtoSpanStatus(resp.StatusCode)`

## Common Span Op Values

| Op | Usage |
|----|-------|
| `http.server` | Incoming HTTP requests |
| `http.client` | Outgoing HTTP calls |
| `db.query` | SQL SELECT/INSERT/UPDATE/DELETE |
| `db` | Generic database operation |
| `cache.get` / `cache.set` | Cache reads/writes |
| `queue.publish` / `queue.process` | Message queues |
| `function` | Generic function call |
| `task` | Background job |
| `grpc.server` / `grpc.client` | gRPC spans |

## Best Practices

- Set `EnableTracing: true` explicitly — it defaults to `false`
- Use `TracesSampler` (not `TracesSampleRate`) for any environment-specific or route-specific sampling logic
- Always `defer span.Finish()` — unfinished spans are silently dropped
- Use `SourceRoute` with parameterised route templates to avoid high-cardinality transaction names
- Use `ContinueFromRequest(r)` in every HTTP handler to preserve distributed traces
- Propagate both `sentry-trace` AND `baggage` headers on outgoing requests
- Don't set `MaxSpans` below the number of expected child spans in your largest transactions

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transactions appearing | Ensure `EnableTracing: true` and `TracesSampleRate > 0` |
| Spans missing from transaction | Ensure `defer span.Finish()` is called on every span |
| High-cardinality transaction names | Use `WithTransactionSource(SourceRoute)` with parameterised route templates |
| Distributed trace not linked | Propagate both `sentry-trace` and `baggage` headers; use `ContinueFromRequest` |
| Health checks polluting data | Use `TracesSampler` to return `0.0` for health endpoints |
| Too many spans | Lower `MaxSpans`; coalesce high-frequency child spans (e.g., N+1 DB calls) |
| OTel errors not linked to trace | Pass OTel `ctx` via `EventHint.Context`; don't use global `sentry.CaptureException` |
