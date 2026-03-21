---
title: "Sentry .NET SDK"
description: "Sentry 错误监控 .NET SDK 集成，异常追踪和性能监控"
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "dotnet", "sdk"]
date: 2026-03-20
---

# Sentry .NET SDK

Opinionated wizard that scans your .NET project and guides you through complete Sentry setup: error monitoring, distributed tracing, profiling, structured logging, and cron monitoring across all major .NET frameworks.

## Invoke This Skill When

- User asks to "add Sentry to .NET", "set up Sentry in C#", or "install Sentry for ASP.NET Core"
- User wants error monitoring, tracing, profiling, logging, or crons for a .NET app
- User mentions `SentrySdk.Init`, `UseSentry`, `Sentry.AspNetCore`, or `Sentry.Maui`
- User wants to capture unhandled exceptions in WPF, WinForms, MAUI, or Azure Functions
- User asks about `SentryOptions`, `BeforeSend`, `TracesSampleRate`, or symbol upload

> **Note:** SDK version and APIs below reflect `Sentry` NuGet packages ≥6.1.0.
> Always verify against [docs.sentry.io/platforms/dotnet/](https://docs.sentry.io/platforms/dotnet/) before implementing.

---

## Phase 1: Detect

Run these commands to understand the project before making any recommendations:

```bash
# Detect framework type — find all .csproj files
find . -name "*.csproj" | head -20

# Detect framework targets
grep -r "TargetFramework\|Project Sdk" --include="*.csproj" .

# Check for existing Sentry packages
grep -r "Sentry" --include="*.csproj" . | grep "PackageReference"

# Check startup files
ls Program.cs src/Program.cs App.xaml.cs MauiProgram.cs 2>/dev/null

# Check for appsettings
ls appsettings.json src/appsettings.json 2>/dev/null

# Check for logging libraries
grep -r "Serilog\|NLog\|log4net" --include="*.csproj" .

# Check for companion frontend
ls ../frontend ../client ../web 2>/dev/null
cat ../package.json 2>/dev/null | grep -E '"next"|"react"|"vue"' | head -3
```

**What to determine:**

| Question | Impact |
|----------|--------|
| Framework type? | Determines correct package and init pattern |
| .NET version? | .NET 8+ recommended; .NET Framework 4.6.2+ supported |
| Sentry already installed? | Skip install, go to feature config |
| Logging library (Serilog, NLog)? | Recommend matching Sentry sink/target |
| Async/hosted app (ASP.NET Core)? | `UseSentry()` on `WebHost`; no `IsGlobalModeEnabled` needed |
| Desktop app (WPF, WinForms, WinUI)? | Must set `IsGlobalModeEnabled = true` |
| Serverless (Azure Functions, Lambda)? | Must set `FlushOnCompletedRequest = true` |
| Frontend directory found? | Trigger Phase 4 cross-link |

**Framework → Package mapping:**

| Detected | Package to install |
|----------|--------------------|
| `Sdk="Microsoft.NET.Sdk.Web"` (ASP.NET Core) | `Sentry.AspNetCore` |
| `App.xaml.cs` with `Application` base | `Sentry` (WPF) |
| `[STAThread]` in `Program.cs` | `Sentry` (WinForms) |
| `MauiProgram.cs` | `Sentry.Maui` |
| `WebAssemblyHostBuilder` | `Sentry.AspNetCore.Blazor.WebAssembly` |
| `FunctionsStartup` | `Sentry.Extensions.Logging` + `Sentry.OpenTelemetry` |
| `HttpApplication` / `Global.asax` | `Sentry.AspNet` |
| Generic host / Worker Service | `Sentry.Extensions.Logging` |

---

## Phase 2: Recommend

Present a concrete recommendation based on what you found. Lead with a proposal — don't ask open-ended questions.

**Recommended (core coverage):**
- ✅ **Error Monitoring** — always; captures unhandled exceptions, structured captures, scope enrichment
- ✅ **Tracing** — always for ASP.NET Core and hosted apps; auto-instruments HTTP requests and EF Core queries
- ✅ **Logging** — recommended for all apps; routes ILogger / Serilog / NLog entries to Sentry as breadcrumbs and events

**Optional (enhanced observability):**
- ⚡ **Profiling** — CPU profiling; recommend for performance-critical services running on .NET 6+
- ⚡ **Crons** — detect missed/failed scheduled jobs; recommend when Hangfire, Quartz.NET, or scheduled endpoints detected

**Recommendation logic:**

| Feature | Recommend when... |
|---------|------------------|
| Error Monitoring | **Always** — non-negotiable baseline |
| Tracing | **Always for ASP.NET Core** — request traces, EF Core spans, HttpClient spans are high-value |
| Logging | App uses `ILogger<T>`, Serilog, NLog, or log4net |
| Profiling | Performance-critical service on .NET 6+ |
| Crons | App uses Hangfire, Quartz.NET, or scheduled Azure Functions |

Propose: *"I recommend setting up Error Monitoring + Tracing + Logging. Want me to also add Profiling or Crons?"*

---

## Phase 3: Guide

### Option 1: Wizard (Recommended)

```bash
npx @sentry/wizard@latest -i dotnet
```

The wizard logs you into Sentry, selects your org and project, configures your DSN, and sets up MSBuild symbol upload for readable stack traces in production.

**Skip to [Verification](#verification) after running the wizard.**

---

### Option 2: Manual Setup

#### Install the right package

```bash
# ASP.NET Core
dotnet add package Sentry.AspNetCore -v 6.1.0

# WPF or WinForms or Console
dotnet add package Sentry -v 6.1.0

# .NET MAUI
dotnet add package Sentry.Maui -v 6.1.0

# Blazor WebAssembly
dotnet add package Sentry.AspNetCore.Blazor.WebAssembly -v 6.1.0

# Azure Functions (Isolated Worker)
dotnet add package Sentry.Extensions.Logging -v 6.1.0
dotnet add package Sentry.OpenTelemetry -v 6.1.0

# Classic ASP.NET (System.Web / .NET Framework)
dotnet add package Sentry.AspNet -v 6.1.0
```

---

#### ASP.NET Core — `Program.cs`

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.WebHost.UseSentry(options =>
{
    options.Dsn = Environment.GetEnvironmentVariable("SENTRY_DSN")
                  ?? "___YOUR_DSN___";
    options.Debug = true;                         // disable in production
    options.SendDefaultPii = true;                // captures user IP, name, email
    options.MaxRequestBodySize = RequestSize.Always;
    options.MinimumBreadcrumbLevel = LogLevel.Debug;
    options.MinimumEventLevel = LogLevel.Warning;
    options.TracesSampleRate = 1.0;               // tune to 0.1–0.2 in production
    options.SetBeforeSend((@event, hint) =>
    {
        @event.ServerName = null;                 // scrub hostname from events
        return @event;
    });
});

var app = builder.Build();
app.Run();
```

**`appsettings.json` (alternative configuration):**

```json
{
  "Sentry": {
    "Dsn": "___YOUR_DSN___",
    "SendDefaultPii": true,
    "MaxRequestBodySize": "Always",
    "MinimumBreadcrumbLevel": "Debug",
    "MinimumEventLevel": "Warning",
    "AttachStacktrace": true,
    "Debug": true,
    "TracesSampleRate": 1.0,
    "Environment": "production",
    "Release": "my-app@1.0.0"
  }
}
```

**Environment variables (double underscore as separator):**

```bash
export Sentry__Dsn="https://examplePublicKey@o0.ingest.sentry.io/0"
export Sentry__TracesSampleRate="0.1"
export Sentry__Environment="staging"
```

---

#### WPF — `App.xaml.cs`

> ⚠️ **Critical:** Initialize in the **constructor**, NOT in `OnStartup()`. The constructor fires earlier, catching more failure modes.

```csharp
using System.Windows;
using Sentry;

public partial class App : Application
{
    public App()
    {
        SentrySdk.Init(options =>
        {
            options.Dsn = "___YOUR_DSN___";
            options.Debug = true;
            options.SendDefaultPii = true;
            options.TracesSampleRate = 1.0;
            options.IsGlobalModeEnabled = true;   // required for all desktop apps
        });

        // Capture WPF UI-thread exceptions before WPF's crash dialog appears
        DispatcherUnhandledException += App_DispatcherUnhandledException;
    }

    private void App_DispatcherUnhandledException(
        object sender,
        System.Windows.Threading.DispatcherUnhandledExceptionEventArgs e)
    {
        SentrySdk.CaptureException(e.Exception);
        // Set e.Handled = true to prevent crash dialog and keep app running
    }
}
```

---

#### WinForms — `Program.cs`

```csharp
using System;
using System.Windows.Forms;
using Sentry;

static class Program
{
    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);

        // Required: allows Sentry to see unhandled WinForms exceptions
        Application.SetUnhandledExceptionMode(UnhandledExceptionMode.ThrowException);

        using (SentrySdk.Init(new SentryOptions
        {
            Dsn = "___YOUR_DSN___",
            Debug = true,
            TracesSampleRate = 1.0,
            IsGlobalModeEnabled = true,           // required for desktop apps
        }))
        {
            Application.Run(new MainForm());
        } // Disposing flushes all pending events
    }
}
```

---

#### .NET MAUI — `MauiProgram.cs`

```csharp
public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();
        builder
            .UseMauiApp<App>()
            .UseSentry(options =>
            {
                options.Dsn = "___YOUR_DSN___";
                options.Debug = true;
                options.SendDefaultPii = true;
                options.TracesSampleRate = 1.0;
                // MAUI-specific: opt-in breadcrumbs (off by default — PII risk)
                options.IncludeTextInBreadcrumbs = false;
                options.IncludeTitleInBreadcrumbs = false;
                options.IncludeBackgroundingStateInBreadcrumbs = false;
            });

        return builder.Build();
    }
}
```

---

#### Blazor WebAssembly — `Program.cs`

```csharp
var builder = WebAssemblyHostBuilder.CreateDefault(args);

builder.UseSentry(options =>
{
    options.Dsn = "___YOUR_DSN___";
    options.Debug = true;
    options.SendDefaultPii = true;
    options.TracesSampleRate = 0.1;
});

// Hook logging pipeline without re-initializing the SDK
builder.Logging.AddSentry(o => o.InitializeSdk = false);

await builder.Build().RunAsync();
```

---

#### Azure Functions (Isolated Worker) — `Program.cs`

```csharp
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using OpenTelemetry.Trace;
using Sentry.OpenTelemetry;

var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .ConfigureServices(services =>
    {
        services.AddOpenTelemetry().WithTracing(builder =>
        {
            builder
                .AddSentry()                        // route OTel spans to Sentry
                .AddHttpClientInstrumentation();    // capture outgoing HTTP
        });
    })
    .ConfigureLogging(logging =>
    {
        logging.AddSentry(options =>
        {
            options.Dsn = "___YOUR_DSN___";
            options.Debug = true;
            options.TracesSampleRate = 1.0;
            options.UseOpenTelemetry();                     // let OTel drive tracing
            options.DisableSentryHttpMessageHandler = true; // prevent duplicate HTTP spans
        });
    })
    .Build();

await host.RunAsync();
```

---

#### AWS Lambda — `LambdaEntryPoint.cs`

```csharp
public class LambdaEntryPoint : APIGatewayProxyFunction
{
    protected override void Init(IWebHostBuilder builder)
    {
        builder
            .UseSentry(options =>
            {
                options.Dsn = "___YOUR_DSN___";
                options.TracesSampleRate = 1.0;
                options.FlushOnCompletedRequest = true; // REQUIRED for Lambda
            })
            .UseStartup<Startup>();
    }
}
```

---

#### Classic ASP.NET — `Global.asax.cs`

```csharp
public class MvcApplication : HttpApplication
{
    private IDisposable _sentry;

    protected void Application_Start()
    {
        _sentry = SentrySdk.Init(options =>
        {
            options.Dsn = "___YOUR_DSN___";
            options.TracesSampleRate = 1.0;
            options.AddEntityFramework(); // EF6 query breadcrumbs
            options.AddAspNet();          // Classic ASP.NET integration
        });
    }

    protected void Application_Error() => Server.CaptureLastError();

    protected void Application_BeginRequest() => Context.StartSentryTransaction();
    protected void Application_EndRequest() => Context.FinishSentryTransaction();

    protected void Application_End() => _sentry?.Dispose();
}
```

---

### Symbol Upload (Readable Stack Traces)

Without debug symbols, stack traces show only method names — no file names or line numbers. Upload PDB files to unlock full source context.

**Step 1: Create a Sentry auth token**

Go to [sentry.io/settings/auth-tokens/](https://sentry.io/settings/auth-tokens/) and create a token with `project:releases` and `org:read` scopes.

**Step 2: Add MSBuild properties to `.csproj` or `Directory.Build.props`:**

```xml
<PropertyGroup Condition="'$(Configuration)' == 'Release'">
  <SentryOrg>___ORG_SLUG___</SentryOrg>
  <SentryProject>___PROJECT_SLUG___</SentryProject>
  <SentryUploadSymbols>true</SentryUploadSymbols>
  <SentryUploadSources>true</SentryUploadSources>
  <SentryCreateRelease>true</SentryCreateRelease>
  <SentrySetCommits>true</SentrySetCommits>
</PropertyGroup>
```

**Step 3: Set `SENTRY_AUTH_TOKEN` in CI:**

```yaml
# GitHub Actions
- name: Build & upload symbols
  run: dotnet build -c Release
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
```

---

### For Each Agreed Feature

Load the corresponding reference file and follow its steps:

| Feature | Reference file | Load when... |
|---------|---------------|-------------|
| Error Monitoring | `references/error-monitoring.md` | Always — `CaptureException`, scopes, enrichment, filtering |
| Tracing | `references/tracing.md` | Server apps, distributed tracing, EF Core spans, custom instrumentation |
| Profiling | `references/profiling.md` | Performance-critical apps on .NET 6+ |
| Logging | `references/logging.md` | `ILogger<T>`, Serilog, NLog, log4net integration |
| Crons | `references/crons.md` | Hangfire, Quartz.NET, or scheduled function monitoring |

For each feature: read the reference file, follow its steps exactly, and verify before moving on.

---

## Verification

After wizard or manual setup, add a test throw and remove it after verifying:

```csharp
// ASP.NET Core: add a temporary endpoint
app.MapGet("/sentry-test", () =>
{
    throw new Exception("Sentry test error — delete me");
});

// Or capture explicitly anywhere
SentrySdk.CaptureException(new Exception("Sentry test error — delete me"));
```

Then check your [Sentry Issues dashboard](https://sentry.io/issues/) — the error should appear within ~30 seconds.

**Verification checklist:**

| Check | How |
|-------|-----|
| Exceptions captured | Throw a test exception, verify in Sentry Issues |
| Stack traces readable | Check that file names and line numbers appear |
| Tracing active | Check Performance tab for transactions |
| Logging wired | Log an error via `ILogger`, check it appears as Sentry breadcrumb |
| Symbol upload working | Stack trace shows `Controllers/HomeController.cs:42` not `<unknown>` |

---

## Config Reference

### Core `SentryOptions`

| Option | Type | Default | Env Var | Notes |
|--------|------|---------|---------|-------|
| `Dsn` | `string` | — | `SENTRY_DSN` | Required. SDK disabled if unset. |
| `Debug` | `bool` | `false` | — | SDK diagnostic output. Disable in production. |
| `DiagnosticLevel` | `SentryLevel` | `Debug` | — | `Debug`, `Info`, `Warning`, `Error`, `Fatal` |
| `Release` | `string` | auto | `SENTRY_RELEASE` | Auto-detected from assembly version + git SHA |
| `Environment` | `string` | `"production"` | `SENTRY_ENVIRONMENT` | `"debug"` when debugger attached |
| `Dist` | `string` | — | — | Build variant. Max 64 chars. |
| `SampleRate` | `float` | `1.0` | — | Error event sampling rate 0.0–1.0 |
| `TracesSampleRate` | `double` | `0.0` | — | Transaction sampling. Must be `> 0` to enable. |
| `TracesSampler` | `Func<SamplingContext, double>` | — | — | Per-transaction dynamic sampler; overrides `TracesSampleRate` |
| `ProfilesSampleRate` | `double` | `0.0` | — | Fraction of traced transactions to profile. Requires `Sentry.Profiling`. |
| `SendDefaultPii` | `bool` | `false` | — | Include user IP, name, email |
| `AttachStacktrace` | `bool` | `true` | — | Attach stack trace to all messages |
| `MaxBreadcrumbs` | `int` | `100` | — | Max breadcrumbs stored per event |
| `IsGlobalModeEnabled` | `bool` | `false`* | — | *Auto-`true` for MAUI, Blazor WASM. **Must** be `true` for WPF, WinForms, Console. |
| `AutoSessionTracking` | `bool` | `false`* | — | *Auto-`true` for MAUI. Enable for Release Health. |
| `CaptureFailedRequests` | `bool` | `true` | — | Auto-capture HTTP client errors |
| `CacheDirectoryPath` | `string` | — | — | Offline event caching directory |
| `ShutdownTimeout` | `TimeSpan` | — | — | Max wait for event flush on shutdown |
| `HttpProxy` | `string` | — | — | Proxy URL for Sentry requests |
| `EnableBackpressureHandling` | `bool` | `true` | — | Auto-reduce sample rates on delivery failures |

### ASP.NET Core Extended Options (`SentryAspNetCoreOptions`)

| Option | Type | Default | Notes |
|--------|------|---------|-------|
| `MaxRequestBodySize` | `RequestSize` | `None` | `None`, `Small` (~4 KB), `Medium` (~10 KB), `Always` |
| `MinimumBreadcrumbLevel` | `LogLevel` | `Information` | Min log level for breadcrumbs |
| `MinimumEventLevel` | `LogLevel` | `Error` | Min log level to send as Sentry event |
| `CaptureBlockingCalls` | `bool` | `false` | Detect `.Wait()` / `.Result` threadpool starvation |
| `FlushOnCompletedRequest` | `bool` | `false` | **Required for Lambda / serverless** |
| `IncludeActivityData` | `bool` | `false` | Capture `System.Diagnostics.Activity` values |

### MAUI Extended Options (`SentryMauiOptions`)

| Option | Type | Default | Notes |
|--------|------|---------|-------|
| `IncludeTextInBreadcrumbs` | `bool` | `false` | Text from `Button`, `Label`, `Entry` elements. ⚠️ PII risk. |
| `IncludeTitleInBreadcrumbs` | `bool` | `false` | Titles from `Window`, `Page` elements. ⚠️ PII risk. |
| `IncludeBackgroundingStateInBreadcrumbs` | `bool` | `false` | `Window.Backgrounding` event state. ⚠️ PII risk. |

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `SENTRY_DSN` | Project DSN |
| `SENTRY_RELEASE` | App version (e.g. `my-app@1.2.3`) |
| `SENTRY_ENVIRONMENT` | Deployment environment name |
| `SENTRY_AUTH_TOKEN` | MSBuild / `sentry-cli` symbol upload auth token |

**ASP.NET Core:** use double underscore `__` as hierarchy separator:

```bash
export Sentry__Dsn="https://..."
export Sentry__TracesSampleRate="0.1"
```

### MSBuild Symbol Upload Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `SentryOrg` | `string` | — | Sentry organization slug |
| `SentryProject` | `string` | — | Sentry project slug |
| `SentryUploadSymbols` | `bool` | `false` | Upload PDB files for line numbers in stack traces |
| `SentryUploadSources` | `bool` | `false` | Upload source files for source context |
| `SentryCreateRelease` | `bool` | `false` | Auto-create a Sentry release during build |
| `SentrySetCommits` | `bool` | `false` | Associate git commits with the release |
| `SentryUrl` | `string` | — | Self-hosted Sentry URL |

---

## Phase 4: Cross-Link

After completing .NET setup, check for companion frontend projects:

```bash
# Check for frontend in adjacent directories
ls ../frontend ../client ../web ../app 2>/dev/null

# Check for JavaScript framework indicators
cat ../package.json 2>/dev/null | grep -E '"next"|"react"|"vue"|"nuxt"' | head -3
```

If a frontend is found, suggest the matching SDK skill:

| Frontend detected | Suggest skill |
|-------------------|--------------|
| Next.js (`"next"` in `package.json`) | `sentry-nextjs-sdk` |
| React SPA (`"react"` without `"next"`) | `@sentry/react` — see [docs.sentry.io/platforms/javascript/guides/react/](https://docs.sentry.io/platforms/javascript/guides/react/) |
| Vue.js | `@sentry/vue` — see [docs.sentry.io/platforms/javascript/guides/vue/](https://docs.sentry.io/platforms/javascript/guides/vue/) |
| Nuxt | `@sentry/nuxt` — see [docs.sentry.io/platforms/javascript/guides/nuxt/](https://docs.sentry.io/platforms/javascript/guides/nuxt/) |

Connecting frontend and backend with the same Sentry project enables **distributed tracing** — a single trace view spanning browser, .NET server, and any downstream APIs.

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Events not appearing | DSN misconfigured | Set `Debug = true` and check console output for SDK diagnostic messages |
| Stack traces show no file/line | PDB files not uploaded | Add `SentryUploadSymbols=true` to `.csproj`; set `SENTRY_AUTH_TOKEN` in CI |
| WPF/WinForms exceptions missing | `IsGlobalModeEnabled` not set | Set `options.IsGlobalModeEnabled = true` in `SentrySdk.Init()` |
| Lambda/serverless events lost | Container freezes before flush | Set `options.FlushOnCompletedRequest = true` |
| WPF UI-thread exceptions missing | `DispatcherUnhandledException` not wired | Register `App.DispatcherUnhandledException` in constructor (not `OnStartup`) |
| Duplicate HTTP spans in Azure Functions | Both Sentry and OTel instrument HTTP | Set `options.DisableSentryHttpMessageHandler = true` |
| `TracesSampleRate` has no effect | Rate is `0.0` (default) | Set `TracesSampleRate > 0` to enable tracing |
| `appsettings.json` values ignored | Config key format wrong | Use flat key `"Sentry:Dsn"` or env var `Sentry__Dsn` (double underscore) |
| `BeforeSend` drops all events | Hook returns `null` unconditionally | Verify your filter logic; return `null` only for events you want to drop |
| MAUI native crashes not captured | Wrong package | Confirm `Sentry.Maui` is installed (not just `Sentry`) |

---

## Reference: Crons

# Crons — Sentry .NET SDK

> Minimum SDK: `Sentry` ≥ 4.2.0

---

## Overview

Sentry Cron Monitoring detects:
- **Missed check-ins** — job didn't run at the expected time
- **Runtime failures** — job ran but encountered an error
- **Timeouts** — job exceeded `MaxRuntime` without completing

---

## `CaptureCheckIn()` API

```csharp
// Signature
SentryId CaptureCheckIn(
    string monitorSlug,
    CheckInStatus status,
    SentryId? checkInId = null,
    TimeSpan? duration = null,
    Action<SentryMonitorOptions>? configureMonitorOptions = null
)
```

### Check-In Status Values

| Status | When to use |
|--------|-------------|
| `CheckInStatus.InProgress` | Job has started, work is underway |
| `CheckInStatus.Ok` | Job completed successfully |
| `CheckInStatus.Error` | Job failed — an error occurred |

---

## Pattern A: Two-Signal Check-Ins (Recommended)

Sends two signals: `InProgress` at start and `Ok`/`Error` at end.  
Enables detection of both **missed jobs** and **timeout violations**.

```csharp
// Mark job as started — save the checkInId for correlation
var checkInId = SentrySdk.CaptureCheckIn("my-monitor-slug", CheckInStatus.InProgress);

try
{
    DoWork();

    // Mark as successful
    SentrySdk.CaptureCheckIn("my-monitor-slug", CheckInStatus.Ok, checkInId);
}
catch (Exception ex)
{
    // Mark as failed
    SentrySdk.CaptureCheckIn("my-monitor-slug", CheckInStatus.Error, checkInId);
    throw;
}
```

---

## Pattern B: Heartbeat Check-In (Simpler)

Sends a single check-in **after** execution. Detects **missed jobs** only — cannot detect timeouts.

```csharp
try
{
    DoWork();
    SentrySdk.CaptureCheckIn("my-monitor-slug", CheckInStatus.Ok);
}
catch
{
    SentrySdk.CaptureCheckIn("my-monitor-slug", CheckInStatus.Error);
    throw;
}
```

Optionally report the actual runtime duration:

```csharp
var sw = Stopwatch.StartNew();
DoWork();
sw.Stop();

SentrySdk.CaptureCheckIn(
    "my-monitor-slug",
    CheckInStatus.Ok,
    duration: sw.Elapsed
);
```

---

## Programmatic Monitor Configuration (Upsert)

Create or update a monitor directly from code via `configureMonitorOptions`. This is sent with the **first** check-in and is idempotent — safe to call on every run.

### Crontab Schedule

```csharp
var checkInId = SentrySdk.CaptureCheckIn(
    "my-scheduled-job",
    CheckInStatus.InProgress,
    configureMonitorOptions: options =>
    {
        options.Schedule = "0 2 * * *";       // 2 AM daily (crontab expression)
        options.CheckInMargin = 5;             // 5 min grace period before "missed"
        options.MaxRuntime = 30;               // alert if running longer than 30 min
        options.TimeZone = "America/New_York"; // IANA timezone
        options.FailureIssueThreshold = 2;     // create issue after 2 consecutive failures
        options.RecoveryThreshold = 1;         // resolve issue after 1 consecutive success
    }
);
```

### Interval-Based Schedule

```csharp
var checkInId = SentrySdk.CaptureCheckIn(
    "my-interval-job",
    CheckInStatus.InProgress,
    configureMonitorOptions: options =>
    {
        options.Interval(6, SentryMonitorInterval.Hour); // every 6 hours
        options.CheckInMargin = 30;
        options.MaxRuntime = 120;
        options.TimeZone = "UTC";
        options.FailureIssueThreshold = 1;
        options.RecoveryThreshold = 3;
    }
);
```

### `SentryMonitorInterval` Values

| Value | Description |
|-------|-------------|
| `SentryMonitorInterval.Minute` | Per-minute interval |
| `SentryMonitorInterval.Hour` | Per-hour interval |
| `SentryMonitorInterval.Day` | Per-day interval |
| `SentryMonitorInterval.Week` | Per-week interval |
| `SentryMonitorInterval.Month` | Per-month interval |
| `SentryMonitorInterval.Year` | Per-year interval |

---

## Monitor Configuration Reference

| Option | Type | Description |
|--------|------|-------------|
| `Schedule` | `string` | Standard crontab expression (e.g., `"*/15 * * * *"`) |
| `Interval(n, unit)` | method | Interval-based schedule; alternative to `Schedule` |
| `CheckInMargin` | `int` | Minutes of grace period before a missing check-in is flagged |
| `MaxRuntime` | `int` | Maximum allowed runtime in minutes before a timeout alert |
| `TimeZone` | `string` | IANA timezone name (e.g., `"UTC"`, `"America/Chicago"`) |
| `FailureIssueThreshold` | `int` | Consecutive failures before a Sentry issue is opened |
| `RecoveryThreshold` | `int` | Consecutive successes before a Sentry issue is closed |

---

## ASP.NET Core — BackgroundService / IHostedService

The most common .NET pattern for scheduled jobs is a `BackgroundService`. Pair it with `CaptureCheckIn` for full monitoring:

```csharp
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Sentry;

public class NightlyReportJob : BackgroundService
{
    private readonly ILogger<NightlyReportJob> _logger;
    private const string MonitorSlug = "nightly-report";

    public NightlyReportJob(ILogger<NightlyReportJob> logger)
        => _logger = logger;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            // Wait until next scheduled time (e.g., 2 AM)
            await WaitUntilNextRunAsync(stoppingToken);

            var checkInId = SentrySdk.CaptureCheckIn(
                MonitorSlug,
                CheckInStatus.InProgress,
                configureMonitorOptions: o =>
                {
                    o.Schedule = "0 2 * * *"; // 2 AM daily
                    o.CheckInMargin = 15;
                    o.MaxRuntime = 60;
                    o.TimeZone = "UTC";
                    o.FailureIssueThreshold = 1;
                    o.RecoveryThreshold = 1;
                }
            );

            try
            {
                _logger.LogInformation("Starting nightly report generation");
                await GenerateReportAsync(stoppingToken);
                _logger.LogInformation("Nightly report completed successfully");

                SentrySdk.CaptureCheckIn(MonitorSlug, CheckInStatus.Ok, checkInId);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Nightly report failed");
                SentrySdk.CaptureCheckIn(MonitorSlug, CheckInStatus.Error, checkInId);
            }
        }
    }

    private async Task WaitUntilNextRunAsync(CancellationToken ct)
    {
        var now = DateTime.UtcNow;
        var nextRun = now.Date.AddDays(now.Hour >= 2 ? 1 : 0).AddHours(2);
        var delay = nextRun - now;
        if (delay > TimeSpan.Zero)
            await Task.Delay(delay, ct);
    }

    private Task GenerateReportAsync(CancellationToken ct) => Task.CompletedTask; // replace with real logic
}
```

Register the hosted service in `Program.cs`:

```csharp
builder.Services.AddHostedService<NightlyReportJob>();
```

### Minimal IHostedService Implementation

For simpler one-shot or timer-based jobs:

```csharp
public class SyncJob : IHostedService, IDisposable
{
    private Timer? _timer;
    private const string MonitorSlug = "data-sync";

    public Task StartAsync(CancellationToken cancellationToken)
    {
        _timer = new Timer(RunJob, null, TimeSpan.Zero, TimeSpan.FromHours(1));
        return Task.CompletedTask;
    }

    private void RunJob(object? state)
    {
        var checkInId = SentrySdk.CaptureCheckIn(
            MonitorSlug,
            CheckInStatus.InProgress,
            configureMonitorOptions: o =>
            {
                o.Interval(1, SentryMonitorInterval.Hour);
                o.CheckInMargin = 5;
                o.MaxRuntime = 30;
                o.TimeZone = "UTC";
            }
        );

        try
        {
            SyncData();
            SentrySdk.CaptureCheckIn(MonitorSlug, CheckInStatus.Ok, checkInId);
        }
        catch
        {
            SentrySdk.CaptureCheckIn(MonitorSlug, CheckInStatus.Error, checkInId);
            throw;
        }
    }

    private void SyncData() { /* real logic here */ }

    public Task StopAsync(CancellationToken cancellationToken)
    {
        _timer?.Change(Timeout.Infinite, 0);
        return Task.CompletedTask;
    }

    public void Dispose() => _timer?.Dispose();
}
```

---

## Hangfire Integration

A dedicated `Sentry.Hangfire` package wraps check-ins automatically around Hangfire job execution:

```shell
dotnet add package Sentry.Hangfire
```

Register the integration when configuring Hangfire:

```csharp
// Program.cs
builder.Services.AddHangfire(config =>
{
    config.UseSqlServerStorage(connectionString);
    config.UseSentry(); // ← enables automatic check-in wrapping
});
builder.Services.AddHangfireServer();
```

With Hangfire, check-ins are sent automatically for every recurring job — no manual `CaptureCheckIn` calls needed. Set the monitor slug using the job's `RecurringJobId`.

See the [Hangfire integration guide](https://docs.sentry.io/platforms/dotnet/guides/hangfire/) for full details.

---

## Quartz.NET Integration

**No official Quartz.NET package exists.** Use `CaptureCheckIn` manually inside `IJob.Execute()`:

```csharp
using Quartz;
using Sentry;

[DisallowConcurrentExecution]
public class MyQuartzJob : IJob
{
    public async Task Execute(IJobExecutionContext context)
    {
        var slug = $"quartz-{context.JobDetail.Key.Name}";

        var checkInId = SentrySdk.CaptureCheckIn(slug, CheckInStatus.InProgress,
            configureMonitorOptions: o =>
            {
                o.Schedule = "0 */6 * * *"; // every 6 hours
                o.CheckInMargin = 10;
                o.MaxRuntime = 60;
                o.TimeZone = "UTC";
            }
        );

        try
        {
            await DoWorkAsync(context.CancellationToken);
            SentrySdk.CaptureCheckIn(slug, CheckInStatus.Ok, checkInId);
        }
        catch (Exception ex)
        {
            SentrySdk.CaptureCheckIn(slug, CheckInStatus.Error, checkInId);
            throw new JobExecutionException(ex);
        }
    }
}
```

---

## Long-Running Job Pattern (Heartbeat Loop)

For processes that run continuously and should check in periodically:

```csharp
public class LongRunningProcessor : BackgroundService
{
    private const string MonitorSlug = "queue-processor";

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var checkInId = SentrySdk.CaptureCheckIn(
                MonitorSlug,
                CheckInStatus.InProgress,
                configureMonitorOptions: o =>
                {
                    o.Interval(5, SentryMonitorInterval.Minute);
                    o.CheckInMargin = 2;
                    o.MaxRuntime = 10;
                    o.TimeZone = "UTC";
                }
            );

            try
            {
                await ProcessBatchAsync(stoppingToken);
                SentrySdk.CaptureCheckIn(MonitorSlug, CheckInStatus.Ok, checkInId);
            }
            catch (Exception ex) when (!stoppingToken.IsCancellationRequested)
            {
                SentrySdk.CaptureCheckIn(MonitorSlug, CheckInStatus.Error, checkInId);
                // optionally capture the exception too
                SentrySdk.CaptureException(ex);
            }

            await Task.Delay(TimeSpan.FromMinutes(5), stoppingToken);
        }
    }
}
```

---

## Alerting

Create issue alerts in Sentry:  
**Alerts → Create Alert → Issues → filter** by tag `monitor.slug equals my-monitor-slug`

---

## Rate Limits

Cron check-ins are rate-limited to **6 check-ins per minute per monitor per environment**. Each environment (`production`, `staging`, etc.) tracks independently. Exceeding this limit silently drops events — visible in Usage Stats.

---

## SDK Version Matrix

| Feature | Min SDK Version |
|---------|----------------|
| `SentrySdk.CaptureCheckIn()` | **4.2.0** |
| Heartbeat pattern | **4.2.0** |
| Programmatic monitor upsert (`configureMonitorOptions`) | **4.2.0** |
| Crontab schedule | **4.2.0** |
| Interval schedule (`SentryMonitorInterval`) | **4.2.0** |
| `Sentry.Hangfire` auto-integration | **4.x** |
| Quartz.NET | ❌ Manual API only |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Check-ins not appearing in Sentry | Verify `monitorSlug` matches the slug configured in Sentry; check DSN is correct and SDK is initialized |
| Monitor shows "missed" despite job running | Increase `CheckInMargin` to allow more grace time; check server clock sync (NTP) |
| Monitor shows "timeout" | Increase `MaxRuntime`; investigate why the job exceeds the expected duration |
| Monitor not auto-created | Pass `configureMonitorOptions` on the **first** `CaptureCheckIn` call — the upsert creates the monitor |
| `CheckInStatus.Error` but no Sentry issue | Configure `FailureIssueThreshold = 1` on the monitor options to create issues on first failure |
| Hangfire jobs not sending check-ins | Ensure `config.UseSentry()` is called inside `AddHangfire`; verify Sentry SDK is initialized before Hangfire starts |
| Quartz jobs not monitored | No official integration — add `CaptureCheckIn` manually inside `IJob.Execute()` |
| Duplicate check-ins from multiple instances | Use a distributed lock (e.g., `IDistributedLock`) around the check-in calls, or configure Quartz/Hangfire with single-instance scheduling |

---

## Reference: Error Monitoring

# Error Monitoring — Sentry .NET SDK

> Minimum SDK: `Sentry` ≥ 4.0.0 (NuGet)  
> ASP.NET Core integration: `Sentry.AspNetCore` ≥ 4.0.0  
> MAUI integration: `Sentry.Maui` ≥ 4.0.0  
> User feedback API: `Sentry` ≥ 4.0.0 (`CaptureFeedback`)

---

## Automatic vs Manual Error Capture

### What Is Captured Automatically

| Error Type | Captured? | Mechanism |
|-----------|-----------|-----------|
| Unhandled exceptions (all platforms) | ✅ Yes | `AppDomain.CurrentDomain.UnhandledException` |
| Unobserved Task exceptions | ✅ Yes | `TaskScheduler.UnobservedTaskException` |
| ASP.NET Core request errors | ✅ Yes | Sentry middleware |
| WPF Dispatcher unhandled exceptions | ✅ Yes | `Application.DispatcherUnhandledException` (with hook) |
| MAUI unhandled exceptions | ✅ Yes | Platform-specific native integrations |
| WinForms exceptions | ✅ Yes | Requires `SetUnhandledExceptionMode(ThrowException)` |
| Caught + swallowed `try/catch` | ❌ No | Must call `SentrySdk.CaptureException()` manually |
| Graceful error returns | ❌ No | Must call `SentrySdk.CaptureException()` manually |

### The Core Rule

> **"If you catch an exception and don't re-throw it, Sentry never sees it."**

```csharp
// ✅ Automatically captured — unhandled, bubbles up
throw new Exception("Unhandled");

// ✅ Automatically captured — re-thrown
try
{
    await DoSomethingAsync();
}
catch (Exception ex)
{
    throw; // re-throw preserves stack trace
}

// ❌ NOT captured — swallowed by graceful return
try
{
    await DoSomethingAsync();
}
catch (Exception ex)
{
    return Result.Failure("Operation failed"); // ← Sentry never sees this
}

// ✅ Manually captured
try
{
    await DoSomethingAsync();
}
catch (Exception ex)
{
    SentrySdk.CaptureException(ex);
    return Result.Failure("Operation failed");
}
```

---

## Core Capture API

### `SentrySdk.CaptureException`

```csharp
// Basic — capture a caught exception
SentryId id = SentrySdk.CaptureException(exception);

// With inline scope enrichment — changes are isolated to this ONE event
SentryId id = SentrySdk.CaptureException(exception, scope =>
{
    scope.SetTag("order.id", orderId.ToString());
    scope.Level = SentryLevel.Fatal;
    scope.User = new SentryUser { Id = userId };
});
```

> **Key behavior:** The SDK clones the current scope before invoking the callback. Changes inside the callback apply only to that one event and do not affect subsequent events.

### `SentrySdk.CaptureMessage`

```csharp
// Default level is Info
SentrySdk.CaptureMessage("Something notable happened");

// With explicit severity
SentrySdk.CaptureMessage("Disk space critically low", SentryLevel.Warning);

// With scope enrichment
SentrySdk.CaptureMessage("Payment gateway timeout", scope =>
{
    scope.SetTag("gateway", "stripe");
    scope.Level = SentryLevel.Error;
}, SentryLevel.Error);
```

**SentryLevel values:**
```csharp
SentryLevel.Debug
SentryLevel.Info      // default for CaptureMessage
SentryLevel.Warning
SentryLevel.Error
SentryLevel.Fatal
```

### `SentrySdk.CaptureEvent`

For full manual control over every field on the event:

```csharp
var evt = new SentryEvent
{
    Message = new SentryMessage { Message = "Custom structured event" },
    Level = SentryLevel.Error
};
evt.SetTag("custom-tag", "value");
evt.Fingerprint = new[] { "custom-fingerprint" };
SentrySdk.CaptureEvent(evt);

// Construct from a caught exception
try { ... }
catch (Exception ex)
{
    var evt = new SentryEvent(ex)
    {
        Level = SentryLevel.Fatal
    };
    SentrySdk.CaptureEvent(evt);
}
```

### All capture signatures

```csharp
// CaptureException
SentryId SentrySdk.CaptureException(Exception exception)
SentryId SentrySdk.CaptureException(Exception exception, Action<Scope> configureScope)

// CaptureMessage
SentryId SentrySdk.CaptureMessage(string message, SentryLevel level = SentryLevel.Info)
SentryId SentrySdk.CaptureMessage(string message, Action<Scope> configureScope,
    SentryLevel level = SentryLevel.Info)

// CaptureEvent
SentryId SentrySdk.CaptureEvent(SentryEvent evt, Scope? scope = null, SentryHint? hint = null)
SentryId SentrySdk.CaptureEvent(SentryEvent evt, Action<Scope> configureScope)
SentryId SentrySdk.CaptureEvent(SentryEvent evt, SentryHint? hint, Action<Scope> configureScope)

// Flush
void  SentrySdk.Flush()
void  SentrySdk.Flush(TimeSpan timeout)
Task  SentrySdk.FlushAsync(TimeSpan timeout)

// Utility
bool      SentrySdk.IsEnabled
SentryId  SentrySdk.LastEventId
```

---

## ASP.NET Core — Automatic & Manual Error Capture

### Installation

```shell
dotnet add package Sentry.AspNetCore
```

### Initialization in `Program.cs`

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.WebHost.UseSentry(options =>
{
    options.Dsn = "https://...@sentry.io/...";
    options.SendDefaultPii = true;              // Include user IP, headers, auth
    options.MaxRequestBodySize = RequestSize.Always;
    options.TracesSampleRate = 1.0;
    options.Debug = true;
});

var app = builder.Build();
app.Run();
```

### Via `appsettings.json` (no code required)

```json
{
  "Sentry": {
    "Dsn": "https://...@sentry.io/...",
    "SendDefaultPii": true,
    "MaxRequestBodySize": "Always",
    "MinimumBreadcrumbLevel": "Debug",
    "MinimumEventLevel": "Warning",
    "AttachStacktrace": true,
    "Debug": true,
    "TracesSampleRate": 1.0
  }
}
```

### Via environment variables (double-underscore convention)

```shell
Sentry__Dsn=https://...@sentry.io/...
Sentry__Debug=true
Sentry__TracesSampleRate=0.5
Sentry__SendDefaultPii=true
```

### What ASP.NET Core captures automatically

- All unhandled exceptions thrown from controllers and middleware → captured as Sentry events
- HTTP request data (URL, method, headers, body if configured)
- User info from `IHttpContext` when `SendDefaultPii = true`
- Breadcrumbs from `Microsoft.Extensions.Logging`
- Performance transactions for each HTTP request (when `TracesSampleRate > 0`)

### Manual capture in a controller

```csharp
[ApiController]
[Route("[controller]")]
public class OrderController : ControllerBase
{
    [HttpPost]
    public IActionResult CreateOrder(OrderRequest request)
    {
        try
        {
            _orderService.Create(request);
            return Ok();
        }
        catch (PaymentDeclinedException ex)
        {
            SentrySdk.CaptureException(ex, scope =>
            {
                scope.SetTag("payment.gateway", request.PaymentGateway);
                scope.SetExtra("order_amount", request.Amount);
            });
            return StatusCode(402, "Payment declined");
        }
    }
}
```

### Custom user factory (DI)

```csharp
public class MyUserFactory : ISentryUserFactory
{
    private readonly IHttpContextAccessor _accessor;

    public MyUserFactory(IHttpContextAccessor accessor)
        => _accessor = accessor;

    public SentryUser? Create()
    {
        var user = _accessor.HttpContext?.User;
        if (user?.Identity?.IsAuthenticated != true) return null;

        return new SentryUser
        {
            Id       = user.FindFirst(ClaimTypes.NameIdentifier)?.Value,
            Email    = user.FindFirst(ClaimTypes.Email)?.Value,
            Username = user.Identity.Name
        };
    }
}

// Register in DI
services.AddSingleton<ISentryUserFactory, MyUserFactory>();
```

### ASP.NET Core-specific options

| Option | Type | Description |
|--------|------|-------------|
| `SendDefaultPii` | `bool` | Include request URL, headers, user IP, auth info |
| `MaxRequestBodySize` | `RequestSize` | `None`, `Small` (<4 KB), `Medium` (<10 KB), `Always` |
| `MinimumBreadcrumbLevel` | `LogLevel` | Min log level for breadcrumb capture from ILogger |
| `MinimumEventLevel` | `LogLevel` | Min log level to generate a Sentry error event from ILogger |
| `CaptureBlockingCalls` | `bool` | Detect `Task.Wait()` / `.Result` threadpool starvation |

---

## Scope Management

### How Scopes Work in .NET

The **Hub** holds a stack of scopes. When an event is captured the hub merges the topmost scope's data into the event. Scope storage mode is controlled by `IsGlobalModeEnabled`:

| `IsGlobalModeEnabled` | Storage | Use For |
|---|---|---|
| `false` (default) | `AsyncLocal<T>` | Server apps — per-request isolation |
| `true` | Singleton | Desktop apps — shared scope across threads |

### `ConfigureScope` — Persistent Changes

Modifies the current ambient scope permanently (until changed or scope is popped). Use for session-level data:

```csharp
SentrySdk.ConfigureScope(scope =>
{
    scope.SetTag("tenant.id", tenantId);
    scope.User = new SentryUser
    {
        Id    = user.Id.ToString(),
        Email = user.Email
    };
    scope.Level = SentryLevel.Warning;
    scope.TransactionName = "UserCheckout";
});

// Async variant
await SentrySdk.ConfigureScopeAsync(async scope =>
{
    var user = await _context.Users.FindAsync(userId);
    scope.User = new SentryUser { Id = user.Id.ToString(), Email = user.Email };
});

// Allocation-free overload (avoids closure)
SentrySdk.ConfigureScope(
    static (scope, tenantId) => scope.SetTag("tenant.id", tenantId),
    currentTenantId);
```

### `PushScope` — Temporary Isolated Scope

Inherits parent scope data. All changes inside the `using` block are discarded when disposed:

```csharp
using (SentrySdk.PushScope())
{
    SentrySdk.ConfigureScope(scope =>
    {
        scope.SetTag("operation", "bulk-import");
        scope.User = new SentryUser { Id = userId };
    });

    SentrySdk.CaptureException(new Exception("Scoped error"));
} // scope is popped here — tags/user cleared
```

### Inline scope callback (preferred for single events)

The `configureScope` callback on capture methods is the preferred pattern for one-off enrichment without needing a `using` block:

```csharp
// Only this event carries the tag
SentrySdk.CaptureException(ex, scope =>
{
    scope.SetTag("action", "checkout");
    scope.Level = SentryLevel.Fatal;
});

// The next event is NOT affected
SentrySdk.CaptureException(otherEx);
```

### Clearing scope data

```csharp
SentrySdk.ConfigureScope(scope =>
{
    scope.User = new SentryUser();   // Clear user (e.g., on logout)
    scope.Clear();                   // Clear everything
    scope.ClearBreadcrumbs();
    scope.ClearAttachments();
});
```

### Scope decision guide

| Goal | API |
|------|-----|
| Data on ALL events (app version, build ID) | `options.DefaultTags["key"] = "value"` |
| Session/request-level data | `SentrySdk.ConfigureScope(...)` |
| One specific event only | Inline `configureScope` callback on capture |
| Temporary sub-context (batch job, etc.) | `SentrySdk.PushScope()` + `using` |

---

## Context Enrichment

### Tags (Indexed, Searchable)

Tags are **indexed** — use them for filtering, grouping, and alerting rules.

```csharp
SentrySdk.ConfigureScope(scope =>
{
    scope.SetTag("page.locale", "de-at");
    scope.SetTag("user.plan", "enterprise");

    // Set multiple at once
    scope.SetTags(new Dictionary<string, string>
    {
        ["environment"] = "staging",
        ["region"]      = "us-east-1"
    });

    // Unset a tag
    scope.UnsetTag("page.locale");
});

// Default tags for ALL events (set in options)
SentrySdk.Init(options =>
{
    options.DefaultTags["app.version"]     = "2.0.1";
    options.DefaultTags["deployment.region"] = "us-east-1";
});
```

**Tag constraints:** Keys ≤ 32 chars (`a-zA-Z`, `0-9`, `_`, `.`, `:`, `-`); values ≤ 200 chars, no newlines.

### User

```csharp
SentrySdk.ConfigureScope(scope =>
{
    scope.User = new SentryUser
    {
        Id        = "42",
        Username  = "john.doe",
        Email     = "john.doe@example.com",
        IpAddress = "{{auto}}"        // let Sentry infer from the connection
    };

    // Custom fields
    scope.User.Other["account_type"] = "premium";
    scope.User.Other["tenant_id"]    = "acme-corp";
});

// Clear user on logout
SentrySdk.ConfigureScope(scope => scope.User = new SentryUser());
```

**SentryUser fields:**

| Field | Type | Notes |
|-------|------|-------|
| `Id` | `string?` | Internal identifier |
| `Username` | `string?` | Display label |
| `Email` | `string?` | Enables Gravatars and Sentry messaging |
| `IpAddress` | `string?` | `"{{auto}}"` to infer from connection; auto-set when `SendDefaultPii = true` |
| `Other` | `IDictionary<string, string>` | Arbitrary additional user data |

### Breadcrumbs

**Manual:**

```csharp
SentrySdk.AddBreadcrumb(
    message:  "User authenticated",
    category: "auth",
    level:    BreadcrumbLevel.Info);

// With structured data
SentrySdk.AddBreadcrumb(
    message:  "User navigated to checkout",
    category: "navigation",
    type:     "navigation",
    data:     new Dictionary<string, string>
    {
        ["from"] = "/cart",
        ["to"]   = "/checkout"
    },
    level: BreadcrumbLevel.Info);

// Using Breadcrumb object
var crumb = new Breadcrumb(
    message:  "Button clicked",
    type:     "user",
    data:     new Dictionary<string, string> { ["button_id"] = "submit" },
    category: "ui.click",
    level:    BreadcrumbLevel.Info);
SentrySdk.AddBreadcrumb(crumb);
```

**BreadcrumbLevel values:** `Debug`, `Info` (default), `Warning`, `Error`, `Critical`

**Automatically captured breadcrumbs:**

| Source | Requires |
|--------|----------|
| HTTP requests | `SentryHttpMessageHandler` with `HttpClient` |
| Logs (Info+) | `Microsoft.Extensions.Logging`, Serilog, NLog, log4net |
| Database queries | EF6 or EF Core via DiagnosticSource |
| MAUI app events | Navigation, lifecycle, user interactions |

Max breadcrumbs: 100 (default). Override with `options.MaxBreadcrumbs = 50`.

### Custom Contexts (Structured, Non-Searchable)

```csharp
SentrySdk.ConfigureScope(scope =>
{
    scope.Contexts["character"] = new
    {
        Name       = "Mighty Fighter",
        Age        = 19,
        AttackType = "melee"
    };

    scope.Contexts["build"] = new
    {
        Version  = "2.0.1",
        Commit   = "abc123",
        Pipeline = "main-ci"
    };
});
```

> The key `"type"` is **reserved** — do not use it. Contexts are not searchable; use Tags for searchable data.

### Tags vs Contexts vs Extra

| Feature | Searchable? | Indexed? | Best For |
|---------|------------|---------|---------|
| **Tags** | ✅ Yes | ✅ Yes | Filtering, grouping, alerting |
| **Contexts** | ❌ No | ❌ No | Structured debug info (nested objects) |
| **Extra** (deprecated) | ❌ No | ❌ No | Prefer `Contexts` instead |
| **User** | ✅ Partially | ✅ Yes | User attribution and filtering |

---

## `BeforeSend` and Filtering Hooks

### `BeforeSend` — Modify or Drop Error Events

Called immediately before transmission — last in the processing pipeline. Return `null` to drop the event.

```csharp
SentrySdk.Init(options =>
{
    // Simple variant
    options.SetBeforeSend(@event =>
    {
        // Drop noisy exceptions
        if (@event.Exception?.Message.Contains("Noisy Exception") == true)
            return null;

        // Scrub server name for privacy
        @event.ServerName = null;

        return @event;
    });

    // Full variant with SentryHint
    options.SetBeforeSend((@event, hint) =>
    {
        if (@event.Exception is SqlException sqlEx && sqlEx.Number == 1205)
        {
            // Deadlock — enrich rather than drop
            @event.SetTag("sql.error_number", sqlEx.Number.ToString());
        }

        return @event;
    });
});
```

### `BeforeSendTransaction` — Modify or Drop Performance Events

```csharp
options.SetBeforeSendTransaction((transaction, hint) =>
{
    if (transaction.Name == "GET /health")
        return null; // Drop health-check transactions
    return transaction;
});
```

### `BeforeBreadcrumb` — Filter or Modify Breadcrumbs

```csharp
options.SetBeforeBreadcrumb(breadcrumb =>
    breadcrumb.Category == "Spammy.Logger"
        ? null          // null DROPS the breadcrumb
        : breadcrumb);  // returning it KEEPS it (optionally modified)

// Full variant with hint
options.SetBeforeBreadcrumb((breadcrumb, hint) =>
{
    if (breadcrumb.Level == BreadcrumbLevel.Debug)
        return null;
    return breadcrumb;
});
```

### `BeforeSendLog`

```csharp
options.SetBeforeSendLog(log =>
{
    if (log.Level < SentryLevel.Warning)
        return null;
    return log;
});
```

---

## Fingerprinting and Custom Grouping

All events have a fingerprint. Events with the same fingerprint group into the same issue. The default fingerprint is computed from the stack trace. Override it in `BeforeSend` or directly on a scope/event.

### Group more aggressively (collapse all matching into one issue)

```csharp
options.SetBeforeSend(@event =>
{
    if (@event.Exception is SqlConnectionException)
    {
        // All SqlConnectionExceptions → one issue
        @event.SetFingerprint(new[] { "database-connection-error" });
    }
    return @event;
});
```

### Group with greater granularity (split issues using `{{ default }}`)

```csharp
options.SetBeforeSend(@event =>
{
    if (@event.Exception is MyRpcException ex)
    {
        @event.SetFingerprint(new[]
        {
            "{{ default }}",        // keep Sentry's default hash
            ex.Function,            // split by RPC function
            ex.Code.ToString()      // split by status code
        });
    }
    return @event;
});
```

### Set fingerprint directly on scope or event

```csharp
// On scope — applies to all subsequent events in this scope
SentrySdk.ConfigureScope(scope =>
{
    scope.Fingerprint = new[] { "my-custom-fingerprint" };
});

// On a specific event
var evt = new SentryEvent(exception);
evt.Fingerprint = new[] { "{{ default }}", "additional-key" };
SentrySdk.CaptureEvent(evt);
```

### Fingerprint template variables

| Variable | Description |
|----------|-------------|
| `{{ default }}` | Sentry's normally computed hash (extend rather than replace) |
| `{{ transaction }}` | Current transaction name |
| `{{ function }}` | Top function in stack trace |
| `{{ type }}` | Exception type name |

---

## Exception Filters

### Filter by exception type

```csharp
SentrySdk.Init(options =>
{
    // Also suppresses TaskCanceledException (derives from OperationCanceledException)
    options.AddExceptionFilterForType<OperationCanceledException>();
    options.AddExceptionFilterForType<MyBusinessException>();
});
```

### Custom `IExceptionFilter`

```csharp
public class MyExceptionFilter : IExceptionFilter
{
    public bool Filter(Exception ex)
    {
        // Return true to DROP the exception (not sent to Sentry)
        return ex is MyCustomException mce && mce.IsExpected;
    }
}

SentrySdk.Init(options =>
{
    options.AddExceptionFilter(new MyExceptionFilter());
});
```

### Deduplication

```csharp
SentrySdk.Init(options =>
{
    // Default: All ^ InnerException
    options.DeduplicateMode =
        DeduplicateMode.SameEvent |
        DeduplicateMode.SameExceptionInstance;

    // Disable entirely
    options.DisableDuplicateEventDetection();
});
```

**DeduplicateMode flags:** `SameEvent`, `SameExceptionInstance`, `InnerException`, `AggregateException`, `All`

---

## Unhandled Exception Capture

### WPF

```csharp
// App.xaml.cs — must be in constructor, NOT OnStartup()
public partial class App : Application
{
    public App()
    {
        SentrySdk.Init(options =>
        {
            options.Dsn = "https://...@sentry.io/...";
            options.IsGlobalModeEnabled = true; // Required for desktop apps
            options.TracesSampleRate = 1.0;
        });

        // Hook WPF dispatcher-level unhandled exceptions
        DispatcherUnhandledException += App_DispatcherUnhandledException;
    }

    void App_DispatcherUnhandledException(
        object sender, DispatcherUnhandledExceptionEventArgs e)
    {
        SentrySdk.CaptureException(e.Exception);
        e.Handled = true; // Prevent the WPF default crash dialog
    }
}
```

> **`IsGlobalModeEnabled = true`** is required for WPF — ensures background thread exceptions share the same scope as the UI thread.

> **Critical:** Initialize in the `App()` constructor, not `OnStartup()`. The constructor runs before any dispatcher frames, ensuring the unhandled exception hook is registered first.

### MAUI

```csharp
// MauiProgram.cs
public static MauiApp CreateMauiApp()
{
    var builder = MauiApp.CreateBuilder();
    builder
        .UseMauiApp<App>()
        .UseSentry(options =>
        {
            options.Dsn = "https://...@sentry.io/...";
            options.TracesSampleRate = 1.0;

            // Optional — all false by default (PII risk)
            options.IncludeTextInBreadcrumbs               = false;
            options.IncludeTitleInBreadcrumbs              = false;
            options.IncludeBackgroundingStateInBreadcrumbs = false;
        });
    return builder.Build();
}
```

**MAUI platform coverage:**

| Platform | Integration |
|----------|-------------|
| Android | `AppDomainUnhandledExceptionIntegration` + native Android SDK |
| iOS / Mac Catalyst | `RuntimeMarshalManagedExceptionIntegration` + native Cocoa SDK |
| Windows (WinUI) | `AppDomainUnhandledExceptionIntegration` + `WinUIUnhandledExceptionIntegration` |

### Windows Forms

```csharp
// Program.cs
[STAThread]
static void Main()
{
    Application.EnableVisualStyles();
    Application.SetCompatibleTextRenderingDefault(false);

    // REQUIRED: makes WinForms re-throw instead of swallowing exceptions
    Application.SetUnhandledExceptionMode(UnhandledExceptionMode.ThrowException);

    using (SentrySdk.Init(options =>
    {
        options.Dsn = "https://...@sentry.io/...";
        options.IsGlobalModeEnabled = true;
        options.TracesSampleRate = 1.0;
    }))
    {
        Application.Run(new MainForm());
    }
}
```

### Console App

```csharp
// Program.cs
SentrySdk.Init(options =>
{
    options.Dsn = "https://...@sentry.io/...";
    options.TracesSampleRate = 1.0;
});

// SDK 3.31.0+ handles flush on exit automatically
// For older SDKs, wrap in: using var _ = SentrySdk.Init(...);
```

### Disabling Built-in Integrations

```csharp
SentrySdk.Init(options =>
{
    options.DisableAppDomainUnhandledExceptionCapture();
    options.DisableUnobservedTaskExceptionCapture();
    options.DisableAppDomainProcessExitFlush();
    options.DisableRuntimeMarshalManagedExceptionCapture(); // iOS/MacCatalyst
});
```

---

## Event Processors

Unlike `BeforeSend` (only one allowed), multiple event processors can be registered at different scopes:

```csharp
// Global — runs for all events
public class MyEventProcessor : ISentryEventProcessor
{
    public SentryEvent? Process(SentryEvent @event)
    {
        if (@event.Exception is BackgroundJobException)
            return null; // Drop — null discards the event

        @event.SetTag("app.layer", "background-worker");
        @event.ServerName = null; // Scrub hostname

        return @event;
    }
}

// Register globally via options
SentrySdk.Init(options =>
{
    options.AddEventProcessor(new MyEventProcessor());
});

// Register on current + following scopes
SentrySdk.ConfigureScope(scope =>
{
    scope.AddEventProcessor(new MyEventProcessor());
});

// Register for a single event only
SentrySdk.CaptureException(ex, scope =>
{
    scope.AddEventProcessor(new MyEventProcessor());
});
```

### Exception processor (runs before the main chain)

```csharp
public class MyExceptionProcessor : ISentryEventExceptionProcessor
{
    public void Process(Exception exception, SentryEvent sentryEvent)
    {
        if (exception is HttpRequestException httpEx)
        {
            sentryEvent.SetTag("http.status", httpEx.StatusCode?.ToString() ?? "unknown");
        }
    }
}

SentrySdk.Init(options =>
{
    options.AddExceptionProcessor(new MyExceptionProcessor());
});
```

**Processor execution order:**
1. `ISentryEventExceptionProcessor` — exception-specific processors
2. `ISentryEventProcessor` — general event processors
3. `SetBeforeSend` / `SetBeforeSendTransaction` — **always last**

---

## User Feedback

### Programmatic API

```csharp
// Capture an event first to get an ID
var eventId = SentrySdk.CaptureMessage("An event that will receive user feedback.");

// Submit user feedback linked to that event
SentrySdk.CaptureFeedback(
    message:           "It broke when I clicked submit.",
    contactEmail:      "user@example.com",
    name:              "Jane Doe",
    associatedEventId: eventId);
```

**Full signature:**

```csharp
SentryId SentrySdk.CaptureFeedback(
    string message,
    string? contactEmail      = null,
    string? name              = null,
    string? replayId          = null,
    string? url               = null,
    SentryId? associatedEventId = null,
    Scope? scope              = null,
    SentryHint? hint          = null)
```

**Using `SentryFeedback` object:**

```csharp
var feedback = new SentryFeedback(
    message:           "The checkout button is broken.",
    contactEmail:      "user@example.com",
    name:              "John Smith",
    associatedEventId: SentrySdk.LastEventId);

SentrySdk.CaptureFeedback(feedback);
```

> **Validation:** Sentry rejects feedback with invalid email addresses. Pre-validate email format before calling the API.

### Crash-Report Modal (JavaScript widget on error pages)

For ASP.NET Core web apps, show the browser-based report dialog on error response pages:

```html
<!-- Include Sentry JS SDK -->
<script
  src="https://browser.sentry-cdn.com/10.40.0/bundle.min.js"
  crossorigin="anonymous">
</script>

<!-- Show dialog with the server-side event ID -->
<script>
  Sentry.init({ dsn: "https://...@sentry.io/..." });
  Sentry.showReportDialog({ eventId: "@ViewBag.SentryEventId" });
</script>
```

```csharp
// In your error controller or exception handler middleware
ViewBag.SentryEventId = SentrySdk.LastEventId;
```

---

## Error Capture Quick Reference

### Scenario Coverage Table

| Scenario | Auto Captured? | Solution |
|----------|--------------|---------|
| Unhandled exception (all frameworks) | ✅ Yes | `AppDomain.UnhandledException` integration |
| Unobserved Task exception | ✅ Yes | `TaskScheduler.UnobservedTaskException` integration |
| ASP.NET Core request error | ✅ Yes | Sentry middleware |
| WPF `DispatcherUnhandledException` | ✅ Yes | Hook in `App()` constructor |
| MAUI unhandled exception | ✅ Yes | Platform-specific native integrations |
| WinForms unhandled exception | ✅ Yes | Requires `SetUnhandledExceptionMode(ThrowException)` |
| `try/catch` with graceful return | ❌ No | `SentrySdk.CaptureException(ex)` before return |
| `try/catch` with re-throw | ✅ Yes | Bubbles to unhandled exception handler |
| Background thread exception | ✅ Yes | `IsGlobalModeEnabled = true` for desktop apps |

### API Quick Reference

```csharp
// ── Capture ───────────────────────────────────────────────────────────────
SentrySdk.CaptureException(ex)
SentrySdk.CaptureException(ex, scope => { scope.SetTag("key", "val"); })
SentrySdk.CaptureMessage("text")
SentrySdk.CaptureMessage("text", SentryLevel.Warning)

// ── User ──────────────────────────────────────────────────────────────────
SentrySdk.ConfigureScope(scope => scope.User = new SentryUser { Id = "42", Email = "..." });
SentrySdk.ConfigureScope(scope => scope.User = new SentryUser()); // clear on logout

// ── Tags (searchable) ─────────────────────────────────────────────────────
SentrySdk.ConfigureScope(scope => scope.SetTag("key", "value"));
SentrySdk.ConfigureScope(scope => scope.UnsetTag("key"));

// ── Contexts (structured, non-searchable) ─────────────────────────────────
SentrySdk.ConfigureScope(scope => scope.Contexts["name"] = new { Key = "value" });

// ── Breadcrumbs ───────────────────────────────────────────────────────────
SentrySdk.AddBreadcrumb(message: "...", category: "auth", level: BreadcrumbLevel.Info);

// ── Scope isolation ───────────────────────────────────────────────────────
using (SentrySdk.PushScope())
{
    SentrySdk.ConfigureScope(scope => scope.SetTag("key", "value"));
    SentrySdk.CaptureException(ex);
} // tag is cleared after this block

// ── Fingerprinting ────────────────────────────────────────────────────────
SentrySdk.ConfigureScope(scope => scope.Fingerprint = new[] { "group-key" });
// In BeforeSend: @event.SetFingerprint(new[] { "{{ default }}", "extra-dim" });

// ── Hooks (in SentrySdk.Init) ─────────────────────────────────────────────
options.SetBeforeSend((@event, hint) => @event)         // return null to drop
options.SetBeforeSendTransaction((txn, hint) => txn)
options.SetBeforeBreadcrumb((crumb, hint) => crumb)     // return null to drop
options.AddExceptionFilterForType<OperationCanceledException>()

// ── Flush ─────────────────────────────────────────────────────────────────
SentrySdk.Flush(TimeSpan.FromSeconds(5));
await SentrySdk.FlushAsync(TimeSpan.FromSeconds(5));
```

---

## Configuration Options Reference

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `Dsn` | `string` | — | DSN from Sentry project settings; also reads `SENTRY_DSN` env var |
| `Release` | `string?` | — | App release version; also reads `SENTRY_RELEASE` |
| `Environment` | `string?` | — | Deployment environment; also reads `SENTRY_ENVIRONMENT` |
| `SampleRate` | `float` | `1.0` | Error event sampling rate (0–1) |
| `TracesSampleRate` | `double` | `0` | Transaction sampling rate (0–1) |
| `AttachStacktrace` | `bool` | `true` | Attach stack traces to message events too |
| `SendDefaultPii` | `bool` | `false` | Include IP, username, headers |
| `MaxBreadcrumbs` | `int` | `100` | Max breadcrumbs per event |
| `IsGlobalModeEnabled` | `bool` | `false` | Singleton scope for desktop apps |
| `Debug` | `bool` | `false` | Log SDK diagnostics to console |
| `DiagnosticLevel` | `SentryLevel` | `Debug` | Min level for SDK diagnostic logs |
| `DeduplicateMode` | `DeduplicateMode` | `All ^ InnerException` | Duplicate event detection strategy |
| `MaxAttachmentSize` | `long` | `20 MiB` | Max attachment size in bytes |
| `DefaultTags` | `IDictionary<string, string>` | `{}` | Tags added to every event |
| `CacheDirectoryPath` | `string?` | `null` | Path for offline envelope caching |
| `ShutdownTimeout` | `TimeSpan` | `2s` | Flush timeout on SDK shutdown |
| `CaptureFailedRequests` | `bool` | `true` | Capture HTTP client error responses |
| `EnableLogs` | `bool` | `false` | Enable Sentry structured logging |
| `StackTraceMode` | `StackTraceMode` | `Enhanced` | `Enhanced` or `Original` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Caught exceptions not appearing in Sentry | Any `try/catch` that doesn't re-throw must call `SentrySdk.CaptureException(ex)` before returning |
| WPF exceptions from background threads missing | Set `options.IsGlobalModeEnabled = true`; initialize in `App()` constructor, not `OnStartup()` |
| WinForms exceptions not captured | Call `Application.SetUnhandledExceptionMode(UnhandledExceptionMode.ThrowException)` before `SentrySdk.Init` |
| Events dropped after process exit (console/CLI) | SDK 3.31.0+ handles this automatically; on older versions wrap `Init` result in `using var _ = SentrySdk.Init(...)` |
| Stack traces show minified/optimized frames | Enable symbol upload via MSBuild properties (`SentryOrg`, `SentryProject`, `SentryAuthToken`) |
| Duplicate events in Sentry | Check `DeduplicateMode`; `AggregateException` wrapping can cause same exception to appear multiple times |
| Missing user data on events | For ASP.NET Core, enable `SendDefaultPii = true` or register a custom `ISentryUserFactory`; for desktop apps ensure `IsGlobalModeEnabled = true` |
| `OperationCanceledException` flooding Sentry | Filter with `options.AddExceptionFilterForType<OperationCanceledException>()` |
| Events not sent before Lambda/Azure Functions cold start ends | Call `await SentrySdk.FlushAsync(TimeSpan.FromSeconds(5))` at the end of your handler |
| SDK reports `IsEnabled = false` | DSN not set or set to empty string; check `SENTRY_DSN` env var or options initialization order |

---

## Reference: Logging

# Logging — Sentry .NET SDK

> **Minimum SDK: `Sentry` ≥ 5.14.0** for native `SentrySdk.Logger` + `EnableLogs`  
> Integration packages (`Sentry.Extensions.Logging`, `Sentry.Serilog`, `Sentry.NLog`, `Sentry.Log4Net`) available since SDK ≥ 4.x  
> Native structured logs forwarded through integration packages: requires SDK ≥ 6.1.0

---

## Enabling Native Structured Logs

`EnableLogs` must be set to `true` — logging is **disabled by default**:

```csharp
SentrySdk.Init(options =>
{
    options.Dsn = "https://examplePublicKey@o0.ingest.sentry.io/0";
    options.EnableLogs = true; // Required — logs are silently no-ops without this
});
```

Without `EnableLogs = true`, all `SentrySdk.Logger.*` calls are silently discarded.

---

## Native Logger API — Six Levels

The native logger type is `SentryStructuredLogger`, accessed via `SentrySdk.Logger`:

```csharp
SentrySdk.Logger.LogTrace("Entering method Foo");
SentrySdk.Logger.LogDebug("Loaded {0} items", itemCount);
SentrySdk.Logger.LogInfo("Order created successfully");
SentrySdk.Logger.LogWarning("Cache miss for key {0}", cacheKey);
SentrySdk.Logger.LogError("A {0} error occurred", "critical");
SentrySdk.Logger.LogFatal("Unrecoverable error — shutting down");
```

| Level | Method | Typical Use |
|-------|--------|-------------|
| `Trace` | `LogTrace()` | Ultra-granular method entry/exit; high-volume — filter in production |
| `Debug` | `LogDebug()` | Development diagnostics, cache hits/misses |
| `Info` | `LogInfo()` | Normal business milestones, confirmations |
| `Warning` | `LogWarning()` | Degraded state, approaching limits, recoverable issues |
| `Error` | `LogError()` | Failures requiring attention |
| `Fatal` | `LogFatal()` | Critical failures, system unavailable |

### Attaching Custom Attributes

Use the lambda overload to attach typed key-value attributes to a log entry:

```csharp
SentrySdk.Logger.LogWarning(static log =>
{
    log.SetAttribute("request.id", 12345);
    log.SetAttribute("user.tier", "premium");
    log.SetAttribute("is.retried", true);
}, "Payment declined for order {0}", orderId);
```

### Supported Attribute Value Types

| Category | Types |
|----------|-------|
| Textual | `string`, `char` |
| Logical | `bool` |
| Integral | `sbyte`, `byte`, `short`, `ushort`, `int`, `uint`, `long`, `nint` |
| Floating-point | `float`, `double` |
| Other | Any type via `ToString()` fallback |

---

## Log Filtering — `SetBeforeSendLog`

Use `SetBeforeSendLog` to modify or drop logs before transmission. Return `null` to discard:

```csharp
SentrySdk.Init(options =>
{
    options.Dsn = "https://...@sentry.io/...";
    options.EnableLogs = true;

    options.SetBeforeSendLog(static log =>
    {
        // Drop all Info and Trace logs in production
        if (log.Level is SentryLogLevel.Info or SentryLogLevel.Trace)
            return null;

        // Drop noisy health-check messages
        if (log.Message?.Contains("/health") == true)
            return null;

        // Enrich surviving logs
        log.SetAttribute("app.version", "2.1.0");

        return log;
    });
});
```

### The `SentryLog` Object

| Member | Type | Description |
|--------|------|-------------|
| `Timestamp` | `DateTimeOffset` | When the log was created |
| `TraceId` | `SentryId` | Active trace ID — links log to a trace |
| `SpanId` | `SpanId?` | Active span ID — links log to a span |
| `Level` | `SentryLogLevel` | Trace, Debug, Info, Warning, Error, Fatal |
| `Message` | `string` | Formatted log message |
| `Template` | `string?` | Original message template (if structured) |
| `Parameters` | `ImmutableArray` | Template parameters |
| `TryGetAttribute()` | method | Read an attribute |
| `SetAttribute()` | method | Write/modify an attribute |

---

## Automatically Attached Attributes

These are added by the SDK to every log without any configuration:

| Attribute Key | Source |
|---------------|--------|
| `environment` | SDK config |
| `release` | SDK config |
| `sdk.name`, `sdk.version` | SDK internals |
| `message.template` | Message template |
| `message.parameter.0`, `.1`, … | Template parameters |
| `server.address` | Host info |
| `user.id`, `user.name`, `user.email` | Active scope user (requires `SendDefaultPii = true`) |
| `origin` | Integration that created the log |
| `sentry.trace.parent_span_id` | When inside an active span (enables log ↔ trace correlation) |

---

## Integration: Microsoft.Extensions.Logging (ILogger)

### Install

```shell
dotnet add package Sentry.Extensions.Logging
```

### What it does

The MEL integration provides **three capabilities** simultaneously:
1. Stores log messages as **breadcrumbs** (attached to the next error event as context)
2. Sends logs at or above the event threshold as **Sentry error events**
3. Forwards logs as **native Sentry structured logs** (SDK ≥ 6.1.0)

### ASP.NET Core / Generic Host Setup (Recommended)

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

builder.Logging.AddSentry(o =>
{
    o.Dsn = "https://...@sentry.io/...";
    o.MinimumBreadcrumbLevel = LogLevel.Debug;   // default: Information
    o.MinimumEventLevel = LogLevel.Error;         // default: Error
    o.InitializeSdk = true;                       // set false if using SentrySdk.Init elsewhere
});
```

Or configure via `appsettings.json`:

```json
{
  "Sentry": {
    "Dsn": "https://...@sentry.io/...",
    "MinimumBreadcrumbLevel": "Information",
    "MinimumEventLevel": "Error",
    "SendDefaultPii": true,
    "MaxBreadcrumbs": 100
  }
}
```

```csharp
builder.Logging.AddSentry(); // reads Sentry section from appsettings.json
```

### Direct Setup (no DI)

```csharp
var loggerFactory = LoggerFactory.Create(logging =>
{
    logging.AddSentry(o => o.Dsn = "https://...@sentry.io/...");
});
ILogger logger = loggerFactory.CreateLogger<MyClass>();
```

### Usage

Once configured, use standard `ILogger<T>` — no Sentry-specific code required:

```csharp
public class OrderService
{
    private readonly ILogger<OrderService> _logger;

    public OrderService(ILogger<OrderService> logger) => _logger = logger;

    public async Task ProcessOrderAsync(int orderId)
    {
        _logger.LogInformation("Processing order {OrderId}", orderId); // → breadcrumb

        try
        {
            await _paymentService.ChargeAsync(orderId);
            _logger.LogInformation("Order {OrderId} paid successfully", orderId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to process order {OrderId}", orderId); // → Sentry event
            throw;
        }
    }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `MinimumBreadcrumbLevel` | `LogLevel` | `Information` | Threshold for breadcrumb storage |
| `MinimumEventLevel` | `LogLevel` | `Error` | Threshold for sending Sentry error events |
| `InitializeSdk` | `bool` | `true` | Auto-init SDK. Set `false` when using `SentrySdk.Init` |
| `Filters` | `ICollection<ILogEntryFilter>` | — | Custom pre-processing filters |
| `TagFilters` | `ICollection<string>` | — | Prefix-based tag exclusions |

### Important Behavior Notes

- **Breadcrumb cascade**: A `LogError` event includes ALL breadcrumbs accumulated since the last event — so the full Info/Warning/Error history is attached.
- **Self-filtering**: Messages from assemblies starting with `"Sentry"` are excluded to prevent infinite loops.
- **Single init**: Set `InitializeSdk = false` if calling `SentrySdk.Init()` elsewhere in your startup.
- **Empty DSN** disables the SDK entirely.

---

## Integration: Serilog

### Install

```shell
dotnet add package Sentry.Serilog
```

### What it does

Same three capabilities as MEL: breadcrumbs, Sentry error events, and native structured logs.

### Basic Setup (Serilog initializes Sentry)

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Debug()
    .WriteTo.Sentry(o =>
    {
        o.Dsn = "https://...@sentry.io/...";
        o.MinimumBreadcrumbLevel = LogEventLevel.Debug;   // default: Information
        o.MinimumEventLevel = LogEventLevel.Warning;      // default: Error
    })
    .WriteTo.Console()
    .CreateLogger();
```

### Setup (Sentry initialized separately)

```csharp
SentrySdk.Init(o => o.Dsn = "...");

Log.Logger = new LoggerConfiguration()
    .WriteTo.Sentry(o =>
    {
        o.InitializeSdk = false; // ← avoid double-init
        o.MinimumBreadcrumbLevel = LogEventLevel.Information;
        o.MinimumEventLevel = LogEventLevel.Error;
    })
    .CreateLogger();
```

### ASP.NET Core with Serilog

```csharp
builder.Host.UseSerilog((ctx, cfg) =>
{
    cfg.ReadFrom.Configuration(ctx.Configuration)
       .WriteTo.Sentry(o =>
       {
           o.Dsn = ctx.Configuration["Sentry:Dsn"];
           o.MinimumBreadcrumbLevel = LogEventLevel.Debug;
           o.MinimumEventLevel = LogEventLevel.Error;
       });
});
```

### Usage

```csharp
var log = Log.ForContext<OrderService>();

log.Information("Processing order {OrderId} for {CustomerId}", orderId, customerId); // → breadcrumb
log.Error(ex, "Payment failed for order {OrderId}", orderId); // → Sentry event
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `MinimumBreadcrumbLevel` | `Information` | Minimum `LogEventLevel` for breadcrumbs |
| `MinimumEventLevel` | `Error` | Minimum level for Sentry error events |
| `InitializeSdk` | `true` | Whether this sink initializes the SDK |

---

## Integration: NLog

### Install

```shell
dotnet add package Sentry.NLog
```

### Code-Based Configuration

```csharp
LogManager.Configuration = new LoggingConfiguration();

LogManager.Configuration.AddSentry(options =>
{
    options.Dsn = "https://...@sentry.io/...";
    options.Layout = "${message}";
    options.BreadcrumbLayout = "${logger}: ${message}";
    options.MinimumBreadcrumbLevel = LogLevel.Debug;  // default: Info
    options.MinimumEventLevel = LogLevel.Error;        // default: Error
    options.AddTag("logger", "${logger}");
    options.IgnoreEventsWithNoException = false;
    options.SendEventPropertiesAsData = true;
    options.SendEventPropertiesAsTags = false;
});

LogManager.ReconfigExistingLoggers();
```

### XML Configuration (nlog.config)

```xml
<?xml version="1.0" encoding="utf-8" ?>
<nlog xmlns="http://www.nlog-project.org/schemas/NLog.xsd"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <extensions>
    <add assembly="Sentry.NLog"/>
  </extensions>

  <targets>
    <target xsi:type="Sentry"
            name="sentry"
            dsn="https://...@sentry.io/..."
            minimumBreadcrumbLevel="Debug"
            minimumEventLevel="Error"
            layout="${message}"
            breadcrumbLayout="${logger}: ${message}"
            sendEventPropertiesAsData="true"
            ignoreEventsWithNoException="false">
      <tag name="logger" layout="${logger}"/>
    </target>
  </targets>

  <rules>
    <!-- Set minlevel LOWER than breadcrumbLevel so SentryTarget sees all entries -->
    <logger name="*" minlevel="Debug" writeTo="sentry"/>
  </rules>
</nlog>
```

### Usage

```csharp
private static readonly Logger Logger = LogManager.GetCurrentClassLogger();

public void ProcessOrder(int orderId)
{
    Logger.Info("Processing order {orderId}", orderId); // → breadcrumb

    try { /* ... */ }
    catch (Exception ex)
    {
        Logger.Error(ex, "Failed to process order {orderId}", orderId); // → Sentry event
    }
}
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `MinimumBreadcrumbLevel` | `Info` | Threshold for breadcrumb storage |
| `MinimumEventLevel` | `Error` | Threshold for Sentry error events |
| `InitializeSdk` | `true` | Auto-init SDK when DSN provided |
| `IgnoreEventsWithNoException` | `false` | Skip entries with no attached exception |
| `SendEventPropertiesAsData` | `true` | Forward NLog properties as Sentry event data |
| `SendEventPropertiesAsTags` | `false` | Forward NLog properties as Sentry tags |
| `IncludeEventDataOnBreadcrumbs` | `false` | Attach event property data to breadcrumbs |
| `BreadcrumbLayout` | — | NLog layout string for breadcrumb text |
| `Layout` | — | NLog layout string for event message |
| `Tags` | — | Additional static tags attached to all messages |

### ⚠️ Critical NLog Detail

The `SentryTarget` must receive **all** log entries to correctly classify them as breadcrumbs vs events. Configure NLog's `minlevel` **lower** than `MinimumBreadcrumbLevel`:

```xml
<!-- If MinimumBreadcrumbLevel = Info, set minlevel = Debug or Trace -->
<logger name="*" minlevel="Debug" writeTo="sentry"/>
```

---

## Integration: log4net

### Install

```shell
dotnet add package Sentry.Log4Net
```

### XML Configuration (`app.config` / `web.config`)

```xml
<configuration>
  <configSections>
    <section name="log4net"
             type="log4net.Config.Log4NetConfigurationSectionHandler, log4net"/>
  </configSections>

  <log4net>
    <appender name="SentryAppender" type="Sentry.Log4Net.SentryAppender, Sentry.Log4Net">
      <Dsn value="https://...@sentry.io/..."/>
      <SendIdentity value="true"/>  <!-- send log4net Identity as Sentry user.id -->
      <threshold value="INFO"/>     <!-- minimum level for this appender -->
    </appender>

    <root>
      <level value="DEBUG"/>
      <appender-ref ref="SentryAppender"/>
    </root>
  </log4net>
</configuration>
```

### Programmatic Setup (for full SDK control)

The XML appender supports only a subset of Sentry options. For full control, init the SDK separately and omit the `Dsn` element to skip auto-init:

```csharp
// Startup code
SentrySdk.Init(options =>
{
    options.Dsn = "https://...@sentry.io/...";
    options.Release = "my-app@1.0.0";
    options.TracesSampleRate = 0.1;
});
```

```xml
<!-- In app.config — no <Dsn> element means SDK won't be re-initialized -->
<appender name="SentryAppender" type="Sentry.Log4Net.SentryAppender, Sentry.Log4Net">
  <SendIdentity value="true"/>
  <threshold value="INFO"/>
</appender>
```

### Usage

```csharp
private static readonly ILog Logger = LogManager.GetLogger(typeof(MyClass));

Logger.Info("Processing started");       // → breadcrumb
Logger.Warn("Low disk space warning");   // → breadcrumb
Logger.Error("DB connection failed");    // → Sentry event
Logger.Fatal("Application crash", ex);  // → Sentry event
```

### Key Appender Options

| Option | Description |
|--------|-------------|
| `Dsn` | Auto-initializes SDK when provided |
| `SendIdentity` | Reports log4net `Identity` as `user.id` |
| `threshold` | Minimum log4net level for this appender |

---

## Log-to-Trace Correlation

Every log entry from any integration automatically carries the active trace and span IDs:

| Field | Description |
|-------|-------------|
| `TraceId` | Links the log to an active distributed trace |
| `SpanId` | Links the log to the currently active span |

In the Sentry UI you can navigate from an error or trace directly to the logs that occurred during that trace, and vice versa. No extra configuration required — correlation is automatic when `TracesSampleRate > 0`.

---

## Log Level Mapping

| Sentry Level | MEL (`ILogger`) | Serilog | NLog | log4net |
|--------------|-----------------|---------|------|---------|
| `Trace` | `Trace` | `Verbose` | `Trace` | — |
| `Debug` | `Debug` | `Debug` | `Debug` | `DEBUG` |
| `Info` | `Information` | `Information` | `Info` | `INFO` |
| `Warning` | `Warning` | `Warning` | `Warn` | `WARN` |
| `Error` | `Error` | `Error` | `Error` | `ERROR` |
| `Fatal` | `Critical` | `Fatal` | `Fatal` | `FATAL` |

---

## SDK Version Matrix

| Feature | Min SDK Version |
|---------|----------------|
| Native `SentrySdk.Logger` + `EnableLogs` | **5.14.0** |
| `Sentry.Extensions.Logging` | **4.x** |
| `Sentry.Serilog` | **4.x** |
| `Sentry.NLog` | **4.x** |
| `Sentry.Log4Net` | **4.x** |
| Native logs forwarded via integration packages | **6.1.0** |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Native logs not appearing in Sentry | Verify `EnableLogs = true` in `SentrySdk.Init()` — without it, all `SentrySdk.Logger.*` calls are silently discarded |
| MEL/Serilog/NLog logs not triggering Sentry events | Check `MinimumEventLevel` — only logs at or above this threshold are sent as events; lower it if needed |
| NLog: only Error/Fatal seen, no breadcrumbs | NLog `<logger minlevel>` must be set **lower** than `MinimumBreadcrumbLevel` so the SentryTarget receives all entries |
| SDK initialized twice (double events) | Set `InitializeSdk = false` in the logging integration when you also call `SentrySdk.Init()` in startup |
| Logs not linked to traces | Ensure `TracesSampleRate > 0` and the log is emitted inside an active span |
| Sensitive data appearing in logs | Add filtering in `SetBeforeSendLog`; better yet, avoid logging sensitive values at the call site |
| `SetBeforeSendLog` not firing | Confirm `EnableLogs = true` — without it, no logs are processed and the hook never runs |
| log4net: SDK not receiving Identity as user.id | Set `<SendIdentity value="true"/>` in the appender config |
| High log volume / rate limits | Use `SetBeforeSendLog` to drop `Trace` and `Debug` levels in production |

---

## Reference: Profiling

# Profiling — Sentry .NET SDK

> **Alpha feature** — `Sentry.Profiling` NuGet package  
> Minimum SDK: `Sentry.Profiling` ≥ 4.0.0 · .NET 8.0+ required  
> **Not supported:** .NET Framework, Android, Blazor WASM, Native AOT (except iOS/Mac Catalyst)

---

## Overview

The Sentry .NET SDK captures CPU profiles using the .NET EventPipe (`System.Diagnostics.DiagnosticSource`) sampling infrastructure. Profiles attach to **transactions** — they are not standalone events.

| Platform | Mechanism | Package required |
|---|---|---|
| .NET 8+ on Windows | EventPipe CPU sampling | `Sentry.Profiling` |
| .NET 8+ on Linux | EventPipe CPU sampling | `Sentry.Profiling` ⚠️ see Linux note |
| .NET 8+ on macOS | EventPipe CPU sampling | `Sentry.Profiling` |
| iOS / Mac Catalyst | Native Mono AOT profiler | **None** (built into `Sentry.Maui`) |
| .NET Framework | ❌ Not supported | — |
| Android | ❌ Not supported | — |
| Blazor WebAssembly | ❌ Not supported | — |
| Native AOT (non-iOS) | ❌ Not supported | — |

---

## How Profiling Attaches to Traces

Profiles are always tied to a transaction — you must have tracing enabled first:

```
TracesSampleRate × ProfilesSampleRate = net profiling rate

Example:
  TracesSampleRate   = 0.5  →  50% of requests create transactions
  ProfilesSampleRate = 0.4  →  40% of those transactions get profiled
  Net profiling rate        =  20% of all requests
```

When a transaction starts:
1. `ProfilingIntegration` checks whether this transaction should be profiled (per `ProfilesSampleRate`)
2. If yes, an EventPipe session starts collecting CPU samples (~100 Hz)
3. When `transaction.Finish()` is called, the profiler stops and attaches the profile data to the transaction envelope
4. Both the transaction and the profile are sent to Sentry together — you can drill from a slow span directly into a flame graph

> **One profiler at a time:** Only one profile can be active per process. Nested transactions will not each receive their own profile.

---

## Installation

```bash
dotnet add package Sentry.Profiling
```

> **Do NOT install `Sentry.Profiling` for iOS or Mac Catalyst.** Those platforms use the native Mono AOT profiler bundled inside `Sentry.Maui` — installing this package on those targets has no effect.

---

## Basic Setup

Profiling requires three additions to your `SentrySdk.Init` call:

```csharp
SentrySdk.Init(options =>
{
    options.Dsn = "https://examplePublicKey@o0.ingest.sentry.io/0";

    // Step 1: Enable tracing (REQUIRED — profiling won't work without it)
    options.TracesSampleRate = 1.0;

    // Step 2: Set what fraction of sampled transactions get profiled
    options.ProfilesSampleRate = 1.0;  // 1.0 = 100% for development; lower in production

    // Step 3: Register the profiling integration
    options.AddProfilingIntegration();
});
```

### ASP.NET Core

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

builder.WebHost.UseSentry(options =>
{
    options.Dsn = "https://examplePublicKey@o0.ingest.sentry.io/0";
    options.TracesSampleRate = 1.0;
    options.ProfilesSampleRate = 0.1;   // Profile 10% of sampled transactions in production
    options.AddProfilingIntegration();
});

var app = builder.Build();
app.UseSentry();  // Must appear before other middleware
app.MapControllers();
app.Run();
```

---

## Synchronous Startup (Recommended for Most Apps)

`AddProfilingIntegration()` initializes the EventPipe session asynchronously on a background thread. Transactions that start immediately after `SentrySdk.Init()` may not get a profile because the profiler isn't ready yet.

```csharp
// ❌ Problem: profiler may not be ready when first transaction starts
SentrySdk.Init(options => {
    options.AddProfilingIntegration();  // async startup
});
var tx = SentrySdk.StartTransaction("startup", "init");  // profiler might miss this
```

```csharp
// ✅ Fix: provide a timeout to block until profiler is ready
SentrySdk.Init(options => {
    options.AddProfilingIntegration(TimeSpan.FromMilliseconds(500));
});
var tx = SentrySdk.StartTransaction("startup", "init");  // profiler guaranteed ready
```

> **iOS/Mac Catalyst note:** The native Mono profiler always starts synchronously. The `TimeSpan` parameter is accepted but has no effect on those platforms.

---

## Configuration Options

| Option | Type | Default | Description |
|---|---|---|---|
| `TracesSampleRate` | `double?` | `null` | **Required.** Fraction of requests that create transactions (0.0–1.0). Profiling does nothing without this. |
| `TracesSampler` | `Func<TransactionSamplingContext, double?>` | `null` | Alternative to `TracesSampleRate` for dynamic per-request sampling. Takes precedence when set. |
| `ProfilesSampleRate` | `double?` | `null` | Fraction of sampled transactions that get profiled (0.0–1.0). Null = profiling disabled. |
| `AddProfilingIntegration()` | — | — | Registers `SamplingTransactionProfilerFactory`. **Required.** |
| `AddProfilingIntegration(TimeSpan)` | `TimeSpan` | — | Same as above, but blocks synchronously until the EventPipe session starts (or timeout). Recommended for most apps. |

### Recommended Production Settings

```csharp
SentrySdk.Init(options =>
{
    options.Dsn = "...";

    // Sample 20% of transactions
    options.TracesSampleRate = 0.2;

    // Profile 50% of those — net 10% of all requests get profiled
    options.ProfilesSampleRate = 0.5;

    // Block up to 500ms so early-startup transactions are captured
    options.AddProfilingIntegration(TimeSpan.FromMilliseconds(500));
});
```

---

## Platform-Specific Notes

### Linux

⚠️ **Known issue (open as of Feb 2026, [#4815](https://github.com/getsentry/sentry-dotnet/issues/4815)):** `AddProfilingIntegration()` can throw a `ReflectionTypeLoadException` on startup in Linux containers. This is caused by `Dia2Lib.dll` and `TraceReloggerLib.dll` — Windows-only PDB resolver DLLs that are referenced by the profiler's tracing stack.

**Mitigation:** Wrap `AddProfilingIntegration()` in a try/catch and log the failure gracefully:

```csharp
try
{
    options.AddProfilingIntegration();
}
catch (Exception ex)
{
    Console.Error.WriteLine($"[Sentry] Profiling unavailable on this platform: {ex.Message}");
}
```

Test profiling thoroughly on your specific Linux image before enabling in production.

### iOS / Mac Catalyst

Use the native Mono AOT profiler. No installation needed — it's built into `Sentry.Maui`.

```csharp
// iOS: same configuration, but do NOT install Sentry.Profiling
SentrySdk.Init(options =>
{
    options.Dsn = "...";
    options.TracesSampleRate = 1.0;
    options.ProfilesSampleRate = 1.0;
    options.AddProfilingIntegration();  // delegates to native profiler on iOS/Mac Catalyst
});
```

### Windows

Fully supported. `Dia2Lib.dll` is a Windows-native dependency and loads correctly. No extra steps required.

---

## Limitations and Known Issues

| Limitation | Details |
|---|---|
| **Alpha status** | The profiling feature is officially in Alpha as of Feb 2026. APIs may change and it is not recommended for mission-critical production use without testing. |
| **One profile at a time** | Only one transaction profiler can be active per process. If two transactions run concurrently, only the first one gets a profile. |
| **30-second cap** | Profiles are hard-capped at 30 seconds. Transactions longer than 30 seconds have their profile truncated. |
| **.NET 8+ only** | The EventPipe sampling profiler requires the .NET 8 CLR. .NET 6/7 are not supported even though the SDK targets `netstandard2.0`. |
| **Linux crash bug** | `ReflectionTypeLoadException` on startup in Linux containers (issue #4815, open). See Linux section above. |
| **OTel conflict** | When using `UseOpenTelemetry()` + `AddProfilingIntegration()`, profiles may only show `Program.Main` with no application frames (issue #4820, reported closed — verify in your SDK version). |
| **"Unknown frames"** | Some stack frames appear as "unknown" in the Sentry UI. This is expected — they are anonymous JIT helper methods in System assemblies that can't be resolved to named methods. |
| **No Android / WASM** | Android and Blazor WebAssembly are not supported. |

---

## Complete Setup Example

```csharp
// Program.cs — ASP.NET Core with tracing + profiling

using Sentry;

var builder = WebApplication.CreateBuilder(args);

builder.WebHost.UseSentry(options =>
{
    options.Dsn = "https://examplePublicKey@o0.ingest.sentry.io/0";
    options.Environment = builder.Environment.EnvironmentName;
    options.Release = "my-app@1.2.3";

    // Tracing: sample 10% of requests in production
    options.TracesSampleRate = builder.Environment.IsProduction() ? 0.1 : 1.0;

    // Profiling: profile 50% of sampled transactions
    // Net result: 5% of all production requests are profiled
    options.ProfilesSampleRate = 0.5;

    // Block up to 500ms so early-startup transactions aren't missed
    options.AddProfilingIntegration(TimeSpan.FromMilliseconds(500));
});

var app = builder.Build();
app.UseSentry();
app.MapControllers();
app.Run();
```

### Console / Worker Service

```csharp
using Sentry;

SentrySdk.Init(options =>
{
    options.Dsn = "https://examplePublicKey@o0.ingest.sentry.io/0";
    options.TracesSampleRate = 1.0;
    options.ProfilesSampleRate = 1.0;
    options.AddProfilingIntegration(TimeSpan.FromMilliseconds(500));
});

// The profiler is ready — this transaction will be profiled
var transaction = SentrySdk.StartTransaction("data-import", "task");
SentrySdk.ConfigureScope(s => s.Transaction = transaction);

// ... your work here ...

transaction.Finish(SpanStatus.Ok);
// Profile is bundled with the transaction and sent to Sentry
```

---

## Troubleshooting

| Issue | Solution |
|---|---|
| No profiles appearing in Sentry | Verify `ProfilesSampleRate > 0` AND `TracesSampleRate > 0`. Both must be set. Check that `AddProfilingIntegration()` is called. |
| Early-startup transactions not profiled | Use `AddProfilingIntegration(TimeSpan.FromMilliseconds(500))` to block until the EventPipe session is ready before the first transaction starts. |
| `ReflectionTypeLoadException` on startup (Linux) | Known issue #4815. Wrap `AddProfilingIntegration()` in try/catch. Test on your specific Linux image. Consider disabling profiling on Linux until the fix ships. |
| Profiles show only `Program.Main` frame | Possible OTel conflict (issue #4820). If using `UseOpenTelemetry()`, verify your SDK version has the fix. Try disabling one integration to isolate. |
| Concurrent transactions — second one not profiled | Expected behavior. Only one profiler runs at a time. The first concurrent transaction wins the profiler slot. |
| Profile truncated after 30 seconds | Hard cap in the SDK. Split long-running operations into multiple shorter transactions if full profiling coverage is needed. |
| `.NET 6` or `.NET 7` — profiling not working | Not supported. EventPipe profiling requires .NET 8+. |
| "Unknown frames" in flame graph | Expected for JIT internals. Focus on named application frames. |
| iOS profiles not appearing (using `Sentry.Profiling` package) | Remove `Sentry.Profiling` from iOS targets. iOS/Mac Catalyst use the native Mono AOT profiler built into `Sentry.Maui` — the NuGet package is not needed and may conflict. |

---

## Reference: Tracing

# Tracing — Sentry .NET SDK

> Minimum SDK: `Sentry` ≥4.0.0  
> OpenTelemetry integration: `Sentry.OpenTelemetry` ≥6.1.0  
> Custom measurements: `Sentry` ≥3.23.0  
> Profiling (Alpha): `Sentry.Profiling` ≥4.0.0, .NET 8+ only

---

## How Tracing Is Activated

Tracing is **disabled by default**. Enable it by setting `TracesSampleRate` or `TracesSampler` during `SentrySdk.Init()`:

```csharp
SentrySdk.Init(options =>
{
    options.Dsn = "https://examplePublicKey@o0.ingest.sentry.io/0";
    options.TracesSampleRate = 1.0; // capture all transactions (lower in production)
});
```

> **Without one of these set**, no spans or transactions are created regardless of other configuration.

---

## `TracesSampleRate` — Uniform Sampling

A `double?` between `0.0` (capture nothing) and `1.0` (capture everything). Defaults to `null` (disabled).

```csharp
options.TracesSampleRate = 0.2; // sample 20% of transactions
```

---

## `TracesSampler` — Dynamic Per-Transaction Sampling

When set, takes **precedence** over `TracesSampleRate`. Receives a `TransactionSamplingContext` and returns `double?` (0.0–1.0) or `null` (falls back to `TracesSampleRate`).

```csharp
options.TracesSampler = context =>
{
    var name = context.TransactionContext.Name;
    var op   = context.TransactionContext.Operation;

    // Drop health checks entirely
    if (name.Contains("/health") || name.Contains("/ping"))
        return 0.0;

    // Always capture checkout flow
    if (name == "checkout" || op == "perform-checkout")
        return 1.0;

    // Read caller-supplied hint
    if (context.CustomSamplingContext.TryGetValue("isCritical", out var flag) && flag is true)
        return 1.0;

    return 0.1; // default: 10%
};
```

### Passing Custom Sampling Context

```csharp
var transaction = SentrySdk.StartTransaction(
    new TransactionContext("checkout", "http.server"),
    new Dictionary<string, object?> { ["isCritical"] = true }
);
```

`TransactionSamplingContext` shape:

```csharp
public class TransactionSamplingContext
{
    public ITransactionContext TransactionContext { get; }
    public IReadOnlyDictionary<string, object?> CustomSamplingContext { get; }
}
```

---

## ASP.NET Core Middleware Integration

### Setup

```csharp
// Program.cs — .NET 6+ minimal API
var builder = WebApplication.CreateBuilder(args);

builder.WebHost.UseSentry(options =>
{
    options.Dsn = "https://...@o0.ingest.sentry.io/...";
    options.TracesSampleRate = 1.0;
    options.SendDefaultPii = true; // include user info in transactions
});

var app = builder.Build();

// Place UseSentry() BEFORE all other middleware to capture the full request lifecycle
app.UseSentry();

app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

### What Happens Automatically

| Behavior | Detail |
|---|---|
| One transaction per request | `SentryMiddleware` creates an `ITransactionTracer` for every HTTP request |
| Route-based naming | Transaction name = route template (e.g., `GET /api/users/{id}`) with `TransactionNameSource.Route` |
| Error linking | Transaction is set on scope → all errors captured during the request are linked to it |
| Distributed trace continuation | Incoming `sentry-trace` + `baggage` headers are read; `ContinueTrace()` is called automatically |
| Outgoing HTTP spans | `SentryHttpMessageHandler` auto-registered with `IHttpClientFactory` → child spans on every outbound call |
| EF Core / SQLClient spans | `DiagnosticSource` integration adds `db.*` child spans automatically (≥3.9.0) |
| Transaction send | Finished and sent to Sentry when the response is written |

### Dropping or Renaming Transactions

```csharp
options.BeforeSendTransaction = transaction =>
{
    // Drop internal/health routes
    if (transaction.Name.StartsWith("GET /internal/")) return null;

    return transaction;
};
```

---

## Auto-Instrumentation Reference

| Integration | Spans Created | Package | Notes |
|---|---|---|---|
| ASP.NET Core requests | `http.server` transaction per request | `Sentry.AspNetCore` | Enabled automatically by `UseSentry()` |
| Outgoing HTTP (`IHttpClientFactory`) | `http.client` spans | `Sentry.AspNetCore` | Requires active transaction on scope |
| EF Core queries | `db.query_compiler`, `db.connection`, `db.query` | `Sentry.DiagnosticSource` (auto in `Sentry.AspNetCore` ≥3.9.0) | Opt out with `DisableDiagnosticSourceIntegration()` |
| SQLClient | `db.connection`, `db.query` | `Sentry.DiagnosticSource` | Same as EF Core |
| Azure Functions Worker | Transaction per invocation | `Sentry.AzureFunctions.Worker` | Auto-registered |
| Hangfire jobs | Transaction per job | `Sentry.Hangfire` | Auto-registered |
| `Microsoft.Extensions.AI` | `ai.*` spans | `Sentry.Extensions.AI` | — |

### EF Core Span Types

Three spans are created automatically per EF Core query:

```
db.query_compiler  — query compilation / optimization (cached after first run)
db.connection      — database connection lifecycle
db.query           — actual SQL execution
```

### Outgoing HTTP Auto-Instrumentation

Spans are only created when there is an **active transaction on scope**. For manual `HttpClient` construction outside of `IHttpClientFactory`:

```csharp
var sentryHandler = new SentryHttpMessageHandler();
var httpClient = new HttpClient(sentryHandler);

// Must have a transaction active first
var tx = SentrySdk.StartTransaction("my-op", "http.client");
SentrySdk.ConfigureScope(s => s.Transaction = tx);

var response = await httpClient.GetStringAsync("https://api.example.com");
// ^ creates a "GET https://api.example.com" child span

tx.Finish();
```

---

## Custom Instrumentation

### Minimal Example

```csharp
var transaction = SentrySdk.StartTransaction("test-transaction", "test-operation");

var span = transaction.StartChild("test-child-operation");
// ... do work ...
span.Finish();

transaction.Finish(); // sends everything to Sentry
```

### Real-World Example: Checkout Flow

```csharp
public async Task PerformCheckoutAsync()
{
    var transaction = SentrySdk.StartTransaction("checkout", "perform-checkout");

    // Set on scope so that:
    // 1. Errors during this transaction are linked to it
    // 2. Auto-instrumentation (HTTP, EF Core) attaches child spans to it
    SentrySdk.ConfigureScope(scope => scope.Transaction = transaction);

    // Validate cart
    var validationSpan = transaction.StartChild("validation", "validating shopping cart");
    try
    {
        await ValidateShoppingCartAsync();
        validationSpan.Finish(SpanStatus.Ok);
    }
    catch (Exception ex)
    {
        validationSpan.Finish(ex); // auto-maps exception type → SpanStatus
        transaction.Finish(ex);
        throw;
    }

    // Process payment
    var paymentSpan = transaction.StartChild("payment", "processing payment");
    await ProcessPaymentAsync();
    paymentSpan.Finish(SpanStatus.Ok);

    // Send confirmation
    var emailSpan = transaction.StartChild("email", "sending confirmation email");
    await SendConfirmationEmailAsync();
    emailSpan.Finish(SpanStatus.Ok);

    transaction.Finish(SpanStatus.Ok);
}
```

### Attaching to an Active Transaction

```csharp
public async Task DoSomethingAsync()
{
    var activeSpan = SentrySdk.GetSpan();

    if (activeSpan == null)
    {
        // No transaction in scope — start a new root transaction
        activeSpan = SentrySdk.StartTransaction("task", "background-job");
    }
    else
    {
        // Transaction already running — add a child
        activeSpan = activeSpan.StartChild("subtask");
    }

    // ... work ...
    activeSpan.Finish();
}
```

### Nested Spans with Data

```csharp
var transaction = SentrySdk.StartTransaction("data-pipeline", "pipeline");

var fetchSpan = transaction.StartChild("http.client", "fetch raw data");
    var parseSpan = fetchSpan.StartChild("serialize", "parse JSON response");
    parseSpan.Finish();
fetchSpan.Finish();

var processSpan = transaction.StartChild("function", "transform data");
    var dbSpan = processSpan.StartChild("db.query", "INSERT INTO results");
    dbSpan.SetData("db.system", "postgresql");
    dbSpan.SetData("db.statement", "INSERT INTO results (data) VALUES (?)");
    dbSpan.Finish();
processSpan.Finish();

transaction.Finish();
```

### DI-Friendly Pattern (`IHub`)

In ASP.NET Core, inject `IHub` instead of using the static `SentrySdk` API:

```csharp
public class OrderService
{
    private readonly IHub _hub;
    public OrderService(IHub hub) => _hub = hub;

    public async Task ProcessOrderAsync(int orderId)
    {
        var transaction = _hub.StartTransaction("process-order", "task");
        SentrySdk.ConfigureScope(s => s.Transaction = transaction);

        var span = transaction.StartChild("db.query", $"SELECT * FROM orders WHERE id = {orderId}");
        try
        {
            await FetchOrderAsync(orderId);
            span.Finish(SpanStatus.Ok);
            transaction.Finish(SpanStatus.Ok);
        }
        catch (Exception ex)
        {
            span.Finish(ex);
            transaction.Finish(ex);
            throw;
        }
    }
}
```

---

## Distributed Tracing

### Propagation Headers

Sentry uses two HTTP headers to propagate trace context between services:

| Header | Format | Purpose |
|---|---|---|
| `sentry-trace` | `traceId-spanId-samplingDecision` | Links spans across services into one trace |
| `baggage` | W3C Baggage | Carries Dynamic Sampling Context (DSC): `sentry-trace_id`, `sentry-public_key`, `sentry-environment`, `sentry-release`, `sentry-transaction`, etc. |

> **CORS note:** If you have browser frontends, explicitly allowlist `sentry-trace` and `baggage` in your CORS policy — they're blocked by default as non-simple headers.

### Automatic Propagation (ASP.NET Core)

No configuration needed:
- **Incoming:** `SentryMiddleware` reads `sentry-trace` + `baggage` and calls `ContinueTrace()` automatically
- **Outgoing:** `SentryHttpMessageHandler` injects `sentry-trace` + `baggage` into all `IHttpClientFactory` requests

### Restrict Which Hosts Receive Trace Headers

By default, headers are injected into **all** outgoing requests. Restrict with:

```csharp
options.TracePropagationTargets = new List<StringOrRegex>
{
    "api.mycompany.com",
    new StringOrRegex(new Regex(@"^https://.*\.mycompany\.com")),
};
```

### Manual Propagation — Outgoing

```csharp
// Read from active transaction
var sentryTrace = SentrySdk.GetTraceHeader()?.ToString();
var baggage     = SentrySdk.GetBaggage()?.ToString();

// W3C traceparent (alternative format)
var traceparent = SentrySdk.GetTraceparentHeader()?.ToString();

// Inject into your request
request.Headers["sentry-trace"] = sentryTrace;
request.Headers["baggage"]      = baggage;
```

### Manual Propagation — Incoming (`ContinueTrace`)

```csharp
// Service B receives an HTTP request from Service A
var sentryTraceHeader = httpRequest.Headers["sentry-trace"];
var baggageHeader     = httpRequest.Headers["baggage"];

// ContinueTrace parses headers and returns a pre-populated TransactionContext
// with the upstream traceId, parentSpanId, and sampling decision
var ctx = SentrySdk.ContinueTrace(
    sentryTraceHeader,
    baggageHeader,
    name: "process-incoming-request",
    operation: "http.server"
);

var transaction = SentrySdk.StartTransaction(ctx);
// Now this transaction is part of the same distributed trace as Service A
```

### Producer / Consumer Queue Example

**Producer:**

```csharp
var transaction = SentrySdk.StartTransaction("order-submitted", "function");

var publishSpan = transaction.StartChild("queue.publish", "orders");
publishSpan.SetData("messaging.message.id", messageId);
publishSpan.SetData("messaging.destination.name", "orders-queue");
publishSpan.SetData("messaging.message.body.size", Encoding.UTF8.GetByteCount(payload));

// Embed trace context in the message envelope
var envelope = new MessageEnvelope
{
    Payload    = payload,
    SentryTrace = SentrySdk.GetTraceHeader()?.ToString(),
    Baggage     = SentrySdk.GetBaggage()?.ToString(),
};

await queue.PublishAsync("orders-queue", envelope);
publishSpan.Finish();
transaction.Finish();
```

**Consumer:**

```csharp
var envelope = await queue.ConsumeAsync("orders-queue");

// Link consumer to producer's trace
var ctx         = SentrySdk.ContinueTrace(envelope.SentryTrace, envelope.Baggage);
var transaction = SentrySdk.StartTransaction(ctx, "process-order", "function");

var processSpan = transaction.StartChild("queue.process", "orders");
processSpan.SetData("messaging.message.id", envelope.MessageId);
processSpan.SetData("messaging.destination.name", "orders-queue");
processSpan.SetData("messaging.message.receive.latency", latencyMs);
processSpan.SetData("messaging.message.retry.count", retryCount);

try
{
    await ProcessOrderAsync(envelope.Payload);
    processSpan.Finish(SpanStatus.Ok);
    transaction.Finish(SpanStatus.Ok);
}
catch (Exception ex)
{
    processSpan.Finish(ex);
    SentrySdk.CaptureException(ex);
    transaction.Finish(ex);
}
```

---

## OpenTelemetry Integration

### Version Requirements

| Package | Minimum Version |
|---|---|
| `Sentry` | 6.1.0 |
| `Sentry.OpenTelemetry` | 6.1.0 |
| `OpenTelemetry` | 1.5.0 |

```bash
dotnet add package Sentry.OpenTelemetry
```

### How It Works

The `AddSentry()` extension registers a `SentrySpanProcessor` with the OTel `TracerProvider`. Span mapping:

- The **first** OTel `Span` flowing through the processor becomes a Sentry **Transaction**
- **Child** OTel `Span`s with the same parent become Sentry **child Spans** on that transaction
- A new top-level OTel `Span` from a different service creates a new Sentry **Transaction**, linked via the same distributed trace

### Full ASP.NET Core Setup

Two parts are required — both must be configured:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Part 1: Configure Sentry with UseOpenTelemetry()
builder.WebHost.UseSentry(options =>
{
    options.Dsn = "https://...@o0.ingest.sentry.io/...";
    options.TracesSampleRate = 1.0;
    options.UseOpenTelemetry(); // ← tells Sentry to use OTel for trace context propagation
    // Do NOT also configure Sentry's own DiagnosticSource integration —
    // let OTel instrumentation libraries handle it instead
});

// Part 2: Register OTel TracerProvider with AddSentry()
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddEntityFrameworkCoreInstrumentation()
        .AddSentry() // ← routes all OTel spans to Sentry
    );

var app = builder.Build();
app.UseSentry();
app.Run();
```

### ⚠️ Exception Capture in OTel Mode

**Do NOT use OTel's exception APIs** — they strip exception data before Sentry can see it:

```csharp
// ❌ These lose exception details
activity.RecordException(ex);
activity.AddException(ex);

// ✅ Use these instead
_logger.LogError(ex, "Something went wrong"); // ILogger (Sentry captures via logging integration)
SentrySdk.CaptureException(ex);               // or capture directly
```

---

## Dynamic Sampling

Sentry's dynamic sampling uses the **Dynamic Sampling Context (DSC)** carried in `baggage` to make consistent sampling decisions across a distributed trace.

### How It Works

1. The **head service** (first in the trace) makes the sampling decision.
2. The decision is encoded in `baggage` as `sentry-sampled=true|false`.
3. All downstream services receive `baggage` and honor the upstream decision.
4. DSC fields: `sentry-trace_id`, `sentry-public_key`, `sentry-sample_rate`, `sentry-sampled`, `sentry-release`, `sentry-environment`, `sentry-transaction`, `sentry-user_segment`.

### `TransactionNameSource` — Critical for Grouping

High-cardinality names (raw URLs) break dynamic sampling grouping. Use parameterized routes:

```csharp
// ❌ Raw URL — creates unbounded unique groups, defeats sampling
SentrySdk.StartTransaction("/users/12345/orders/9876", "http.server");

// ✅ Parameterized — clean grouping, correct dynamic sampling
SentrySdk.StartTransaction(new TransactionContext(
    "/users/{userId}/orders/{orderId}",
    "http.server",
    nameSource: TransactionNameSource.Route
));
```

| `TransactionNameSource` | Cardinality | Use For |
|---|---|---|
| `Route` | Low ✅ | Parameterized route templates (e.g., `GET /users/{id}`) |
| `Custom` | Low ✅ | User-defined names (background jobs, tasks) |
| `View` | Low ✅ | Controller / view class names |
| `Component` | Medium | Function / component names |
| `Url` | High ❌ | Raw URLs — avoid for dynamic sampling |
| `Task` | Low ✅ | Background task names |

---

## Operation Types and Naming Conventions

The `operation` string categorizes and color-codes spans in the Sentry UI. Follow these conventions:

| Category | Operation | Example Description |
|---|---|---|
| HTTP server | `http.server` | `GET /api/users` |
| HTTP client | `http.client` | `GET https://api.stripe.com/v1/charges` |
| DB query | `db.query` | `SELECT * FROM orders WHERE id = ?` |
| DB connection | `db.connection` | — |
| DB compile | `db.query_compiler` | The LINQ/HQL expression |
| Cache read | `cache.get` | The cache key |
| Cache write | `cache.put` | The cache key |
| Queue publish | `queue.publish` | Queue or topic name |
| Queue consume | `queue.process` | Queue or topic name |
| Function | `function` | Function or method name |
| Background task | `task` | Task name |
| Serialization | `serialize` | — |
| Validation | `validation` | What is being validated |
| AI inference | `ai.*` | Model name |

### `Origin` Field

Indicates whether a span was created by auto-instrumentation or by your code:

| Value | Source |
|---|---|
| `auto.http.aspnetcore` | ASP.NET Core middleware |
| `auto.http.system_net_http` | `SentryHttpMessageHandler` |
| `auto.db.ef_core` | EF Core DiagnosticSource |
| `auto.db.sql_client` | SQLClient DiagnosticSource |
| `manual` | User code |

---

## Custom Measurements

Attach numeric measurements to transactions (requires `Sentry` ≥3.23.0):

```csharp
var span = SentrySdk.GetSpan();
if (span != null)
{
    var transaction = span.GetTransaction();

    transaction.SetMeasurement("memory_used",            64,   MeasurementUnit.Information.Megabyte);
    transaction.SetMeasurement("profile_loading_time",   1.3,  MeasurementUnit.Duration.Second);
    transaction.SetMeasurement("items_processed",        1500);           // unitless
    transaction.SetMeasurement("cache_hit_rate",         0.85, MeasurementUnit.Fraction.Ratio);
}
```

### `MeasurementUnit` Quick Reference

| Category | Values |
|---|---|
| Duration | `Nanosecond`, `Microsecond`, `Millisecond`, `Second`, `Minute`, `Hour`, `Day`, `Week` |
| Information | `Bit`, `Byte`, `Kilobyte`/`Kibibyte`, `Megabyte`/`Mebibyte`, `Gigabyte`/`Gibibyte`, … |
| Fraction | `Ratio`, `Percent` |
| Unitless | Omit unit parameter |

> **⚠️ Unit consistency:** `("latency", 60, Second)` and `("latency", 3, Minute)` are stored as **separate measurements**, not aggregated. Always use the same unit per measurement name.

---

## `SpanStatus` Reference

```csharp
SpanStatus.Ok                // success
SpanStatus.Cancelled         // OperationCanceledException
SpanStatus.InvalidArgument   // ArgumentException, bad input
SpanStatus.DeadlineExceeded  // TimeoutException
SpanStatus.NotFound          // 404
SpanStatus.PermissionDenied  // UnauthorizedAccessException, 403
SpanStatus.ResourceExhausted // 429 / out of resources
SpanStatus.Unimplemented     // NotImplementedException, 501
SpanStatus.Unavailable       // 503
SpanStatus.InternalError     // unhandled exception, 500
SpanStatus.UnknownError      // unknown failure
SpanStatus.FailedPrecondition // InvalidOperationException
SpanStatus.Aborted           // conflicting operation
SpanStatus.DataLoss          // unrecoverable data loss
```

`span.Finish(exception)` auto-maps exception type → `SpanStatus`. HTTP status codes from `SentryHttpMessageHandler` are also mapped automatically (`2xx→Ok`, `401→Unauthenticated`, `403→PermissionDenied`, `404→NotFound`, `429→ResourceExhausted`, `5xx→InternalError`).

---

## Complete Configuration Reference

```csharp
SentrySdk.Init(options =>
{
    // ── Identity ──────────────────────────────────────────────────────────
    options.Dsn         = "https://examplePublicKey@o0.ingest.sentry.io/0";
    options.Environment = "production";
    options.Release     = "my-app@1.2.3";

    // ── Tracing ───────────────────────────────────────────────────────────
    options.TracesSampleRate = 0.2;  // 20% uniform rate

    // OR dynamic sampler (takes precedence when set)
    options.TracesSampler = ctx =>
    {
        if (ctx.TransactionContext.Name.Contains("/health")) return 0.0;
        return 0.1;
    };

    // Restrict which outbound hosts receive trace headers (default: all)
    options.TracePropagationTargets = new List<StringOrRegex>
    {
        "api.mycompany.internal",
        new StringOrRegex(new Regex(@"^https://.*\.mycompany\.com")),
    };

    // ── Auto-instrumentation control ──────────────────────────────────────
    // options.DisableDiagnosticSourceIntegration(); // opt out of EF Core / SQLClient spans

    // ── OpenTelemetry (optional) ──────────────────────────────────────────
    // options.UseOpenTelemetry(); // use when routing spans via OTel TracerProvider

    // ── Profiling (Alpha, .NET 8+ only) ───────────────────────────────────
    // options.ProfilesSampleRate = 0.1;
    // options.AddProfilingIntegration(TimeSpan.FromMilliseconds(500)); // sync startup
});
```

### Key Options Table

| Option | Type | Default | Purpose |
|---|---|---|---|
| `TracesSampleRate` | `double?` | `null` (disabled) | Uniform sampling rate 0.0–1.0 |
| `TracesSampler` | `Func<TransactionSamplingContext, double?>` | `null` | Dynamic sampler; overrides `TracesSampleRate` |
| `TracePropagationTargets` | `IList<StringOrRegex>` | `[".*"]` (all) | Hosts that receive `sentry-trace` + `baggage` headers |
| `SendDefaultPii` | `bool` | `false` | Include user IP and username in transactions |
| `MaxSpans` | `int` | `1000` | Maximum child spans per transaction |
| `ProfilesSampleRate` | `double?` | `null` | Profiling rate relative to traced transactions |
| `UseOpenTelemetry()` | method | — | Enable OTel-based trace context propagation |
| `DisableDiagnosticSourceIntegration()` | method | — | Opt out of EF Core / SQLClient auto-spans |

---

## Quick Reference Cheat Sheet

```csharp
// ── Start a root transaction ──────────────────────────────────────────────
var tx = SentrySdk.StartTransaction("name", "operation");
SentrySdk.ConfigureScope(s => s.Transaction = tx);  // link errors + enable auto-spans

// ── Add child spans ───────────────────────────────────────────────────────
var span = tx.StartChild("operation", "description");
span.SetData("key", "value");
span.Finish(SpanStatus.Ok);

// ── Get the active span from anywhere ────────────────────────────────────
var active = SentrySdk.GetSpan();
var child  = active?.StartChild("nested-op");
child?.Finish();

// ── Access the transaction from a span ───────────────────────────────────
var txFromSpan = active?.GetTransaction();
txFromSpan?.SetMeasurement("count", 42, MeasurementUnit.Duration.Millisecond);

// ── Finish variants ───────────────────────────────────────────────────────
tx.Finish();                          // implicit Ok
tx.Finish(SpanStatus.InternalError);  // explicit status
tx.Finish(exception);                 // auto-maps exception → SpanStatus

// ── Distributed tracing: outgoing headers ─────────────────────────────────
var traceHeader  = SentrySdk.GetTraceHeader()?.ToString();   // "sentry-trace" value
var baggage      = SentrySdk.GetBaggage()?.ToString();        // "baggage" value
var traceparent  = SentrySdk.GetTraceparentHeader()?.ToString(); // W3C format

// ── Distributed tracing: incoming headers ─────────────────────────────────
var ctx    = SentrySdk.ContinueTrace(incomingTraceHeader, incomingBaggageHeader);
var linked = SentrySdk.StartTransaction(ctx, "name", "op");
```

---

## Troubleshooting

| Issue | Likely Cause | Fix |
|---|---|---|
| No transactions appear in Sentry | `TracesSampleRate` and `TracesSampler` are both unset | Set `options.TracesSampleRate = 1.0` (or `>0`) during `SentrySdk.Init()` |
| Transactions appear but have no child spans | Transaction not set on scope | Call `SentrySdk.ConfigureScope(s => s.Transaction = tx)` after starting the transaction |
| Outgoing HTTP spans missing | `HttpClient` created manually without `SentryHttpMessageHandler` | Use `IHttpClientFactory`, or wrap with `new HttpClient(new SentryHttpMessageHandler())` |
| EF Core spans missing | `Sentry.DiagnosticSource` not installed or version < 3.9.0 | Install `Sentry.DiagnosticSource`, or upgrade `Sentry.AspNetCore` to ≥3.9.0 |
| Distributed trace not connected across services | Missing `ContinueTrace()` on receiving end | Call `SentrySdk.ContinueTrace(traceHeader, baggageHeader)` and use the returned context to start the transaction |
| `sentry-trace` header stripped by browser preflight | CORS policy blocks non-simple headers | Add `sentry-trace` and `baggage` to `Access-Control-Allow-Headers` in your CORS config |
| OTel spans not appearing in Sentry | `AddSentry()` missing from `TracerProvider` OR `UseOpenTelemetry()` missing from `SentryOptions` | Both are required: `AddSentry()` in OTel builder AND `options.UseOpenTelemetry()` in Sentry init |
| OTel mode: exceptions captured with no context | Using `activity.RecordException()` or `activity.AddException()` | Use `SentrySdk.CaptureException(ex)` or `_logger.LogError(ex, ...)` instead |
| High-cardinality transaction groups | Transaction names are raw URLs | Use `TransactionNameSource.Route` with parameterized route templates |
