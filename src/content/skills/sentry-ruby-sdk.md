---
title: "Sentry Ruby SDK"
description: "Full Sentry SDK setup for Ruby. Use when asked to add Sentry to Ruby, install sentry-ruby, setup Sentry in Rails/Sinatra/Rack, or configure error monitoring, tracing, logging, metrics, profiling, or crons for Ruby applications. Also handles migrat..."
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "ruby", "sdk"]
date: 2026-03-20
---

# Sentry Ruby SDK

Opinionated wizard that scans the project and guides through complete Sentry setup.

## Invoke This Skill When

- User asks to "add Sentry to Ruby" or "set up Sentry" in a Ruby app
- User wants error monitoring, tracing, logging, metrics, profiling, or crons in Ruby
- User mentions `sentry-ruby`, `sentry-rails`, or the Ruby Sentry SDK
- User is migrating from AppSignal, Honeybadger, Bugsnag, Rollbar, or Airbrake to Sentry
- User wants to monitor exceptions, HTTP requests, or background jobs in Rails/Sinatra

> **Note:** SDK APIs below reflect sentry-ruby v6.4.0.
> Always verify against [docs.sentry.io/platforms/ruby/](https://docs.sentry.io/platforms/ruby/) before implementing.

---

## Phase 1: Detect

```bash
# Existing Sentry gems
grep -i sentry Gemfile 2>/dev/null

# Framework
grep -iE '\brails\b|\bsinatra\b' Gemfile 2>/dev/null

# Web server — Puma triggers queue time guidance
grep -iE '\bpuma\b' Gemfile 2>/dev/null

# Background jobs
grep -iE '\bsidekiq\b|\bresque\b|\bdelayed_job\b' Gemfile 2>/dev/null

# Competitor monitoring tools — triggers migration path if found
grep -iE '\bappsignal\b|\bhoneybadger\b|\bbugsnag\b|\brollbar\b|\bairbrake\b' Gemfile 2>/dev/null

# Scheduled jobs — triggers Crons recommendation
grep -iE '\bsidekiq-cron\b|\bclockwork\b|\bwhenever\b|\brufus-scheduler\b' Gemfile 2>/dev/null
grep -rn "Sidekiq::Cron\|Clockwork\|every.*do" config/ lib/ --include="*.rb" 2>/dev/null | head -10

# OpenTelemetry tracing — check for SDK + instrumentations
grep -iE '\bopentelemetry-sdk\b|\bopentelemetry-instrumentation\b' Gemfile 2>/dev/null
grep -rn "OpenTelemetry::SDK\.configure\|\.use_all\|\.in_span" config/ lib/ app/ --include="*.rb" 2>/dev/null | head -5

# OpenTelemetry logging — check for logs SDK (much less common in Ruby)
grep -iE '\bopentelemetry-logs-sdk\b|\bopentelemetry-logs-api\b' Gemfile 2>/dev/null
grep -rn "OpenTelemetry::Logs" config/ lib/ app/ --include="*.rb" 2>/dev/null | head -5

# Existing metric patterns (StatsD, Datadog, Prometheus)
grep -rE "(statsd|dogstatsd|prometheus|\.gauge|\.histogram|\.increment|\.timing)" \
  app/ lib/ --include="*.rb" 2>/dev/null | grep -v "_spec\|_test" | head -20

# Companion frontend
cat package.json frontend/package.json web/package.json 2>/dev/null | grep -E '"@sentry|"sentry-'
```

**Route from what you find:**
- **Competitor detected** (`appsignal`, `honeybadger`, `bugsnag`, `rollbar`, `airbrake`) → load `${SKILL_ROOT}/references/migration.md` first; **delete the competitor initializer** as part of migration
- **Sentry already present** → skip to Phase 2 to configure features
- **Rails** → use `sentry-rails` + `config/initializers/sentry.rb`
- **Rack/Sinatra** → `sentry-ruby` + `Sentry::Rack::CaptureExceptions` middleware
- **Sidekiq** → add `sentry-sidekiq`; recommend Metrics if existing metric patterns found
- **Puma detected** → queue time capture is automatic (v6.4.0+), but the reverse proxy must set `X-Request-Start` header; see `${SKILL_ROOT}/references/tracing.md` → "Request Queue Time"
- **OTel tracing detected** (`opentelemetry-sdk` + instrumentations in Gemfile, or `OpenTelemetry::SDK.configure` in source) → use OTLP path: `config.otlp.enabled = true`; do **not** set `traces_sample_rate`; Sentry links errors to OTel traces automatically
- **OTel logging detected** (`opentelemetry-logs-sdk` in Gemfile, or `OpenTelemetry::Logs` in source) → skip `enable_logs`; OTel handles log export
- **OTel tracing present but NOT logging** (the common case) → use OTLP for tracing **and** Sentry native `enable_logs: true` for logging

---

## Phase 2: Recommend

Lead with a concrete proposal — don't ask open-ended questions:

| Feature | Recommend when... |
|---------|------------------|
| Error Monitoring | **Always** |
| OTLP Integration | OTel tracing detected — **replaces** native Tracing |
| Tracing | Rails / Sinatra / Rack / any HTTP framework; **skip if OTel tracing detected** |
| Logging | **Always** — `enable_logs: true` costs nothing; **skip only if OTel logging detected** |
| Metrics | Sidekiq present; existing metric lib (StatsD, Prometheus) detected |
| Profiling | ⚠️ Beta — performance profiling requested; requires `stackprof` or `vernier` gem |
| Crons | Scheduled jobs detected (ActiveJob, Sidekiq-Cron, Clockwork, Whenever) |

**OTel tracing + no OTel logging** (the common case): *"I see OpenTelemetry tracing in the project. I recommend Sentry's OTLP integration for tracing (via your existing OTel setup) + Error Monitoring + Sentry Logging [+ Metrics/Crons if applicable]. Shall I proceed?"*

**OTel tracing + OTel logging:** *"I see OpenTelemetry handling both tracing and logging. I recommend Sentry's OTLP integration + Error Monitoring [+ Metrics/Crons if applicable]. Shall I proceed?"*

**No OTel:** *"I recommend Error Monitoring + Tracing + Logging [+ Metrics if applicable]. Shall I proceed?"*

---

## Phase 3: Guide

### Install

**Rails:**
```ruby
# Gemfile
gem "sentry-ruby"
gem "sentry-rails"
gem "sentry-sidekiq"      # if using Sidekiq
gem "sentry-resque"       # if using Resque
gem "sentry-delayed_job"  # if using DelayedJob
```

**Rack / Sinatra / plain Ruby:**
```ruby
gem "sentry-ruby"
```

Run `bundle install`.

### Framework Integration

| Framework / Runtime | Gem | Init location | Auto-instruments |
|---------------------|-----|---------------|-----------------|
| Rails | `sentry-rails` | `config/initializers/sentry.rb` | Controllers, ActiveRecord, ActiveJob, ActionMailer |
| Rack / Sinatra | `sentry-ruby` | Top of `config.ru` | Requests (via `Sentry::Rack::CaptureExceptions` middleware) |
| Sidekiq | `sentry-sidekiq` | Sentry initializer or Sidekiq config | Worker execution → transactions |
| Resque | `sentry-resque` | Sentry initializer | Worker execution → transactions |
| DelayedJob | `sentry-delayed_job` | Sentry initializer | Job execution → transactions |

### Init — Rails (`config/initializers/sentry.rb`)

```ruby
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.spotlight = Rails.env.development?  # local Spotlight UI; no DSN needed in dev
  config.breadcrumbs_logger = [:active_support_logger, :http_logger]
  config.send_default_pii = true
  config.traces_sample_rate = 1.0  # lower to 0.05–0.2 in production
  config.enable_logs = true
  # Metrics on by default; disable with: config.enable_metrics = false
end
```

`sentry-rails` auto-instruments ActionController, ActiveRecord, ActiveJob, ActionMailer.

### Init — Rack / Sinatra

```ruby
require "sentry-ruby"

Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.spotlight = ENV["RACK_ENV"] == "development"
  config.breadcrumbs_logger = [:sentry_logger, :http_logger]
  config.send_default_pii = true
  config.traces_sample_rate = 1.0
  config.enable_logs = true
end

use Sentry::Rack::CaptureExceptions  # in config.ru, before app middleware
```

### Init — Sidekiq standalone

```ruby
require "sentry-ruby"
require "sentry-sidekiq"

Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.spotlight = ENV.fetch("RAILS_ENV", "development") == "development"
  config.breadcrumbs_logger = [:sentry_logger]
  config.traces_sample_rate = 1.0
  config.enable_logs = true
end
```

### Environment variables

```bash
SENTRY_DSN=https://xxx@oYYY.ingest.sentry.io/ZZZ
SENTRY_ENVIRONMENT=production   # overrides RAILS_ENV / RACK_ENV
SENTRY_RELEASE=my-app@1.0.0
```

### Feature reference files

Walk through features one at a time. Load the reference file for each, follow its steps, and verify before moving to the next:

| Feature | Reference file | Load when... |
|---------|---------------|-------------|
| Migration | `${SKILL_ROOT}/references/migration.md` | Competitor gem found — load **before** installing Sentry |
| Error Monitoring | `${SKILL_ROOT}/references/error-monitoring.md` | Always |
| Tracing | `${SKILL_ROOT}/references/tracing.md` | HTTP handlers / distributed tracing |
| Logging | `${SKILL_ROOT}/references/logging.md` | Structured log capture |
| Metrics | `${SKILL_ROOT}/references/metrics.md` | Sidekiq present; existing metric patterns |
| Profiling | `${SKILL_ROOT}/references/profiling.md` | Performance profiling requested (beta) |
| Crons | `${SKILL_ROOT}/references/crons.md` | Scheduled jobs detected or requested |

For each feature: `Read ${SKILL_ROOT}/references/<feature>.md`, follow steps exactly, verify it works.

---

## Configuration Reference

### Key `Sentry.init` Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `dsn` | String | `nil` | SDK disabled if empty; env: `SENTRY_DSN` |
| `environment` | String | `nil` | e.g., `"production"`; env: `SENTRY_ENVIRONMENT` |
| `release` | String | `nil` | e.g., `"myapp@1.0.0"`; env: `SENTRY_RELEASE` |
| `spotlight` | Boolean | `false` | Send events to Spotlight sidecar (local dev, no DSN needed) |
| `send_default_pii` | Boolean | `false` | Include IP addresses and request headers |
| `sample_rate` | Float | `1.0` | Error event sample rate (0.0–1.0) |
| `traces_sample_rate` | Float | `nil` | Transaction sample rate; `nil` disables tracing |
| `profiles_sample_rate` | Float | `nil` | Profiling rate relative to `traces_sample_rate`; requires `stackprof` or `vernier` |
| `enable_logs` | Boolean | `false` | Enable Sentry structured Logs |
| `enable_metrics` | Boolean | `true` | Enable custom metrics (on by default) |
| `breadcrumbs_logger` | Array | `[]` | Loggers for automatic breadcrumbs (see logging reference) |
| `max_breadcrumbs` | Integer | `100` | Max breadcrumbs per event |
| `debug` | Boolean | `false` | Verbose SDK output to stdout |
| `capture_queue_time` | Boolean | `true` | Record request queue time from `X-Request-Start` header (v6.4.0+) |
| `otlp.enabled` | Boolean | `false` | Route OTel spans to Sentry via OTLP; **do not combine with** `traces_sample_rate` |
| `before_send` | Lambda | `nil` | Mutate or drop error events before sending |
| `before_send_transaction` | Lambda | `nil` | Mutate or drop transaction events before sending |
| `before_send_log` | Lambda | `nil` | Mutate or drop log events before sending |

### Environment Variables

| Variable | Maps to | Purpose |
|----------|---------|---------|
| `SENTRY_DSN` | `dsn` | Data Source Name |
| `SENTRY_RELEASE` | `release` | App version (e.g., `my-app@1.0.0`) |
| `SENTRY_ENVIRONMENT` | `environment` | Deployment environment |

Options set in `Sentry.init` override environment variables.

---

## Verification

**Local dev (no DSN needed) — Spotlight:**
```bash
npx @spotlightjs/spotlight          # browser UI at http://localhost:8969
# or stream events to terminal:
npx @spotlightjs/spotlight tail traces --format json
```
`config.spotlight = Rails.env.development?` (already in the init block above) routes events to the local sidecar automatically.

**With a real DSN:**
```ruby
Sentry.capture_message("Sentry Ruby SDK test")
```

Nothing appears? Set `config.debug = true` and check stdout. Verify DSN format: `https://<key>@o<org>.ingest.sentry.io/<project>`.

---

## Phase 4: Cross-Link

```bash
cat package.json frontend/package.json web/package.json 2>/dev/null | grep -E '"@sentry|"sentry-'
```

| Frontend detected | Suggest |
|-------------------|---------|
| React / Next.js | `sentry-react-sdk` |
| Svelte / SvelteKit | `sentry-svelte-sdk` |
| Vue | `@sentry/vue` — [docs.sentry.io/platforms/javascript/guides/vue/](https://docs.sentry.io/platforms/javascript/guides/vue/) |

For trace stitching between Ruby backend and JS frontend, see `references/tracing.md` → "Frontend trace stitching".

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | `config.debug = true`; verify DSN; ensure `Sentry.init` before first request |
| Rails exceptions missing | Must use `sentry-rails` — `sentry-ruby` alone doesn't hook Rails error handlers |
| No traces (native) | Set `traces_sample_rate > 0`; ensure `sentry-rails` or `Sentry::Rack::CaptureExceptions` |
| No traces (OTLP) | Verify `opentelemetry-exporter-otlp` gem is installed; do **not** set `traces_sample_rate` when using `otlp.enabled = true` |
| Sidekiq jobs not traced | Add `sentry-sidekiq` gem |
| Missing request context | Set `config.send_default_pii = true` |
| Logs not appearing | Set `config.enable_logs = true`; sentry-ruby ≥ 5.27.0 required |
| Metrics not appearing | Check `enable_metrics` is not `false`; verify DSN |
| Events lost on shutdown | `Process.exit!` skips `at_exit` hooks — call `Sentry.flush` explicitly before forced exits |
| Forking server loses events | Puma/Unicorn fork workers — re-initialize in `on_worker_boot` or `after_fork`; without this, the background worker thread dies in child processes |
| DSN rejected / events not delivered | Verify DSN format: `https://<key>@o<org>.ingest.sentry.io/<project>`; set `config.debug = true` to see transport errors |

---

## Reference: Crons

# Crons — Sentry Ruby SDK

> Minimum SDK: `sentry-ruby` v5.14.0+

Cron monitoring detects missed, failed, or slow scheduled jobs by capturing check-in events at job start and completion. Each check-in pair creates a monitor timeline in Sentry — if the `:ok` check-in doesn't arrive on time, Sentry raises an alert.

## Contents

- [Manual check-ins](#manual-check-ins)
- [ActiveJob integration](#activejob-integration)
- [Sidekiq-Cron integration](#sidekiq-cron-integration)
- [Upserting monitor configuration](#upserting-monitor-configuration)
- [Completion-only check-in](#completion-only-check-in)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Manual Check-Ins

Use when the scheduler is Clockwork, Whenever, a plain Ruby loop, or any framework without a built-in integration:

```ruby
# Start check-in — save the returned ID
check_in_id = Sentry.capture_check_in("daily-report", :in_progress)

begin
  GenerateDailyReport.run
  Sentry.capture_check_in("daily-report", :ok, check_in_id: check_in_id)
rescue => e
  Sentry.capture_check_in("daily-report", :error, check_in_id: check_in_id)
  Sentry.capture_exception(e)
  raise
end
```

**Monitor slug** must match the slug configured in Sentry. Slugs are unique per project and environment.

**Status values:**

| Status | When to use |
|--------|-------------|
| `:in_progress` | Job has started |
| `:ok` | Job completed successfully |
| `:error` | Job failed |

## ActiveJob Integration

Include `Sentry::Cron::MonitorCheckIns` to auto-capture check-ins for any ActiveJob:

```ruby
class NightlyCleanupJob < ApplicationJob
  include Sentry::Cron::MonitorCheckIns
  sentry_monitor_check_ins

  def perform
    User.inactive.delete_old_accounts
  end
end
```

Customize the slug and schedule:

```ruby
class NightlyCleanupJob < ApplicationJob
  include Sentry::Cron::MonitorCheckIns
  sentry_monitor_check_ins(
    slug: "nightly-cleanup",
    monitor_config: Sentry::Cron::MonitorConfig.from_crontab(
      "0 2 * * *",
      checkin_margin: 5,   # minutes before marking missed
      max_runtime: 30,     # minutes before marking timed out
      timezone: "UTC"
    )
  )

  def perform
    User.inactive.delete_old_accounts
  end
end
```

## Sidekiq-Cron Integration

Enable automatic check-ins for all Sidekiq-Cron periodic jobs with a single patch:

```ruby
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.enabled_patches += [:sidekiq_cron]
end
```

Sentry captures check-ins for every job defined in your Sidekiq-Cron schedule automatically — no per-job changes needed.

## Upserting Monitor Configuration

Pass `monitor_config` in the initial check-in to create or update the monitor definition programmatically (no manual setup in Sentry UI required):

```ruby
monitor_config = Sentry::Cron::MonitorConfig.from_crontab(
  "5 * * * *",       # runs at :05 every hour
  checkin_margin: 5,
  max_runtime: 15,
  timezone: "Europe/Berlin"
)

check_in_id = Sentry.capture_check_in(
  "hourly-sync",
  :in_progress,
  monitor_config: monitor_config
)
# ... do work ...
Sentry.capture_check_in("hourly-sync", :ok, check_in_id: check_in_id)
```

### Schedule Types

**Crontab:**
```ruby
Sentry::Cron::MonitorConfig.from_crontab(
  "0 9 * * 1-5",   # 9am weekdays
  checkin_margin: 10,
  max_runtime: 60,
  timezone: "America/New_York"
)
```

**Interval:**
```ruby
Sentry::Cron::MonitorConfig.from_interval(
  30, :minute,     # every 30 minutes
  checkin_margin: 5,
  max_runtime: 25
)
```

Supported interval units: `:minute`, `:hour`, `:day`, `:week`, `:month`, `:year`

## Completion-Only Check-In

For jobs where only missed-schedule detection matters (not duration), send a single `:ok` check-in at job completion instead of the two-step `:in_progress` / `:ok` pair:

```ruby
def run_health_ping
  ping_all_services
  Sentry.capture_check_in("health-ping", :ok)
end
```

This detects when a job doesn't run at all but cannot detect stuck or long-running jobs — there is no `:in_progress` marker, so Sentry has no start time to measure against `max_runtime`. Use the full two-step pattern for jobs where duration matters.

## Best Practices

- Use the two-step `:in_progress` / `:ok` pattern for all long-running jobs — it catches both missed runs and jobs that started but never finished
- Set `checkin_margin` a few minutes above the expected cron interval jitter
- Set `max_runtime` conservatively — it's better to alert early on a runaway job than to miss it
- Use `monitor_config` upsert in the job itself rather than configuring monitors manually in the Sentry UI — this keeps schedule definitions in code
- Ensure `SENTRY_DSN` is set in the environment where cron jobs run (often different from the web process)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Check-ins not appearing | Verify `SENTRY_DSN` is set in the cron job's environment (separate from web server) |
| Monitor shows "missed" immediately | `checkin_margin` too low; increase it to account for scheduler jitter |
| `capture_check_in` returns `nil` | SDK not initialized — ensure `Sentry.init` runs before the job |
| ActiveJob mixin not capturing | Confirm `include Sentry::Cron::MonitorCheckIns` and `sentry_monitor_check_ins` are both present |
| Sidekiq-Cron not auto-capturing | Ensure `config.enabled_patches += [:sidekiq_cron]` is in `Sentry.init`; requires `sidekiq-cron` gem |
| Duplicate check-in pairs | Check that `capture_check_in` is not called in both the mixin and manual code for the same job |

---

## Reference: Error Monitoring

# Error Monitoring — Sentry Ruby SDK

> Minimum SDK: `sentry-ruby` gem 5.0.0+

## Contents

- [Configuration](#configuration)
- [Code Examples](#code-examples)
- [Scope API Reference](#scope-api-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Configuration

Key `Sentry.init` options for error monitoring:

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `send_default_pii` | `Boolean` | `false` | Include request headers, IP addresses |
| `sample_rate` | `Float` | `1.0` | Error event sample rate (0.0–1.0) |
| `excluded_exceptions` | `Array` | common 4xx | Exception classes to ignore |
| `include_local_variables` | `Boolean` | `false` | Capture local variables from exception frames |
| `max_breadcrumbs` | `Integer` | `100` | Max breadcrumbs per event |
| `before_send` | `Lambda` | `nil` | Mutate or drop error events before sending |
| `before_breadcrumb` | `Lambda` | `nil` | Mutate or drop breadcrumbs |

## Code Examples

### Automatic capture

**Rails** (`sentry-rails`): exceptions in controllers, background jobs, and mailers are captured automatically — no extra code needed.

**Rack / Sinatra**: register the middleware once and all unhandled exceptions are captured:

```ruby
use Sentry::Rack::CaptureExceptions
```

### Manual capture

```ruby
# Capture any exception
begin
  risky_operation
rescue => e
  Sentry.capture_exception(e)
  raise  # re-raise if you want normal error handling to continue
end

# Capture a plain message (no exception)
Sentry.capture_message("payment gateway unreachable", level: :warning)
```

### User identification

```ruby
# Set user context — call in a Rails before_action or Rack middleware
Sentry.set_user(
  id: current_user.id,
  email: current_user.email,
  username: current_user.username
)

# Clear the user (e.g., on sign-out)
Sentry.set_user({})
```

### Tags, context, and extras

```ruby
# Tags — indexed, filterable in Sentry search
Sentry.set_tags(region: "us-east-1", plan: "enterprise")

# Context — structured data attached to events (not indexed)
Sentry.set_context("order", { id: order.id, total: order.total, currency: "USD" })

# Extras — deprecated; prefer set_context for structured data
Sentry.set_extras(raw_payload: payload.inspect)
```

### Isolated scope with `with_scope`

Changes inside `with_scope` are discarded after the block — ideal for one-off enrichment without polluting subsequent events:

```ruby
Sentry.with_scope do |scope|
  scope.set_tags(component: "checkout", payment_provider: "stripe")
  scope.set_user(id: order.user_id)
  Sentry.capture_exception(e)
end
# ← scope changes above do NOT affect subsequent events
```

### Persistent scope with `configure_scope`

```ruby
Sentry.configure_scope do |scope|
  scope.set_tags(app_version: APP_VERSION)
  scope.set_user(id: current_user.id)
end
# These values apply to all subsequent events in this request/fiber
```

### Rails: per-request context via `before_action`

```ruby
class ApplicationController < ActionController::Base
  before_action :set_sentry_context

  private

  def set_sentry_context
    return unless current_user
    Sentry.set_user(id: current_user.id, email: current_user.email)
    Sentry.set_tags(tenant: current_user.account.slug)
  end
end
```

### Breadcrumbs

```ruby
crumb = Sentry::Breadcrumb.new(
  category: "auth",
  message: "User #{user.email} authenticated",
  level: "info"
)
Sentry.add_breadcrumb(crumb)
```

Automatic breadcrumbs are recorded when `breadcrumbs_logger` is configured:

```ruby
config.breadcrumbs_logger = [:active_support_logger, :http_logger, :redis_logger]
```

| Logger | Captures |
|--------|----------|
| `:active_support_logger` | Rails controller actions, SQL queries, mailer events |
| `:http_logger` | Outbound Net::HTTP requests |
| `:redis_logger` | Redis commands |
| `:sentry_logger` | Ruby `Logger` writes |

### `before_send` hook

```ruby
Sentry.init do |config|
  config.before_send = lambda do |event, hint|
    # Drop ZeroDivisionError
    if hint[:exception].is_a?(ZeroDivisionError)
      next nil  # return nil to discard the event
    end

    # Custom fingerprint for database errors
    if hint[:exception].is_a?(ActiveRecord::StatementInvalid)
      event.fingerprint = ["database-error", hint[:exception].message.split("\n").first]
    end

    # Scrub sensitive fields from the request body
    event.request&.data&.delete("credit_card_number")

    event
  end
end
```

### Exception filters

```ruby
config.excluded_exceptions += [
  "ActionController::RoutingError",
  "ActiveRecord::RecordNotFound",
  "Rack::QueryParser::InvalidParameterError"
]
```

### Local variable capture

```ruby
config.include_local_variables = true
```

Captures local variables from the frames in the exception backtrace. Useful for debugging hard-to-reproduce errors. Evaluate privacy implications before enabling in production.

### Custom fingerprinting

```ruby
# One-off — override grouping for a specific capture
Sentry.with_scope do |scope|
  scope.set_fingerprint(["database-connection-error"])
  Sentry.capture_exception(e)
end

# Extend default grouping in before_send
config.before_send = lambda do |event, hint|
  if hint[:exception].is_a?(MyWorker::JobError)
    event.fingerprint = ["{{ default }}", hint[:exception].job_class]
  end
  event
end
```

## Scope API Reference

```ruby
# Shorthand module methods (operate on current scope)
Sentry.set_user(id:, email:, username:, ip_address:)
Sentry.set_tags(key: "value")
Sentry.set_context("key", { field: "value" })
Sentry.set_extras(key: "value")  # deprecated — prefer set_context

# Scope instance methods (inside with_scope / configure_scope blocks)
scope.set_tags(key: "value")
scope.set_user(id: "42", email: "user@example.com")
scope.set_context("key", { field: "value" })
scope.set_level(:error)            # :debug | :info | :warning | :error | :fatal
scope.set_fingerprint(["my-group"])
scope.clear
```

## Best Practices

- Call `Sentry.init` in `config/initializers/sentry.rb` (Rails) or at the top of `config.ru` before any middleware
- Use `Sentry.with_scope` for one-off context; use `configure_scope` for persistent request context
- Set user in a Rails `before_action` so every exception in that request includes user info
- Use `excluded_exceptions` to filter out expected 4xx errors and keep signal-to-noise high
- Enable `include_local_variables` in development/staging; evaluate privacy implications for production

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Set `config.debug = true`; check DSN; ensure `Sentry.init` is called before exceptions occur |
| Rails exceptions missing | Use `sentry-rails` gem — `sentry-ruby` alone does not hook Rails error handlers |
| Missing request context | Set `config.send_default_pii = true` |
| `before_send` not called for transactions | Use `before_send_transaction` for performance events |
| Error captured but wrong user | Ensure `set_user` runs in a `before_action` before the exception is raised |
| Noise from routing errors | Add `"ActionController::RoutingError"` to `excluded_exceptions` |

---

## Reference: Logging

# Logging — Sentry Ruby SDK

> Minimum SDK: `sentry-ruby` v5.27.0+
> Logs are sent as independent events to Sentry Logs — separate from breadcrumbs and error events.

## Contents

- [Configuration](#configuration)
- [Logging Methods](#logging-methods)
- [Filtering Logs](#filtering-logs)
- [Breadcrumb Loggers](#breadcrumb-loggers)
- [Ruby stdlib Logger integration](#ruby-stdlib-logger-integration)
- [Rails Logger](#rails-logger)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Configuration

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `enable_logs` | Boolean | `false` | Enable Sentry structured Logs — must be `true` |
| `before_send_log` | Lambda | `nil` | Mutate or drop log events before sending |
| `breadcrumbs_logger` | Array | `[]` | Loggers for automatic breadcrumbs (separate from Sentry Logs) |

```ruby
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.enable_logs = true  # required — disabled by default
end
```

## Logging Methods

`Sentry.logger` provides six levels:

```ruby
Sentry.logger.trace("entering payment flow")
Sentry.logger.debug("cache miss for key: %{key}", key: cache_key)
Sentry.logger.info("User %{name} logged in", name: user.email)
Sentry.logger.warn("Retry %{attempt} of %{max}", attempt: 3, max: 5)
Sentry.logger.error("Payment failed: %{message}", message: e.message)
Sentry.logger.fatal("Database unreachable — shutting down")
```

### Parameterized messages

Use `%{key}` named parameters. Parameters are sent as structured attributes, enabling filtering and aggregation in Sentry:

```ruby
# Named parameters (preferred)
Sentry.logger.info(
  "Order %{order_id} placed for %{amount}",
  order_id: order.id,
  amount: order.total
)

# Positional parameters
Sentry.logger.info("Order %s placed", [order.id])
```

### Extra attributes

Pass keyword arguments beyond the message to attach searchable data:

```ruby
Sentry.logger.error(
  "Failed to process payment for order %{order_id}",
  order_id: order.id,
  amount: order.total,
  payment_provider: "stripe",
  error_code: stripe_error.code
)
```

## Filtering Logs

```ruby
config.before_send_log = lambda do |log|
  # Drop debug-level logs in production
  return nil if log.level == :debug

  # Scrub sensitive content
  log.message = log.message.gsub(/token=\S+/, "token=[FILTERED]")

  log
end
```

### `before_send_log` parameter

The `log` argument passed to the callback exposes:

| Property | Type | Description |
|----------|------|-------------|
| `level` | Symbol | `:trace`, `:debug`, `:info`, `:warn`, `:error`, `:fatal` |
| `message` | String | The formatted log message |
| `body` | String | Raw template string (e.g., `"Order %{order_id} placed"`) |
| `attributes` | Hash | Structured parameters passed as keyword arguments |

## Breadcrumb Loggers

Breadcrumbs are different from Sentry Logs — they are attached to the next error event, not sent independently. See `error-monitoring.md` for the full logger table and configuration options.

```ruby
config.breadcrumbs_logger = [:active_support_logger, :http_logger, :redis_logger, :sentry_logger]
```

### Filtering breadcrumbs

```ruby
config.before_breadcrumb = lambda do |breadcrumb, hint|
  # Drop Redis noise in high-traffic environments
  return nil if breadcrumb.category == "redis"
  breadcrumb
end
```

## Ruby stdlib Logger integration

Capture writes from existing Ruby `Logger` instances as Sentry breadcrumbs. This requires enabling the `:logger` patch first — without it `std_lib_logger_filter` is never called:

```ruby
config.breadcrumbs_logger = [:sentry_logger]
config.enabled_patches << :logger   # required — activates the Logger patch

# Optional: filter by severity
config.std_lib_logger_filter = proc do |logger, message, severity|
  [:error, :fatal].include?(severity)
end
```

## Rails Logger

In Rails, `Rails.logger` writes automatically appear as breadcrumbs when `:active_support_logger` is enabled — no extra configuration needed.

To also send key Rails log lines as Sentry Logs (not just breadcrumbs), call `Sentry.logger` explicitly alongside your existing logging:

```ruby
Rails.logger.error("Payment failed: #{e.message}")
Sentry.logger.error("Payment failed: %{message}", message: e.message)
```

## Best Practices

- Always use parameterized messages (`%{key}` syntax) rather than string interpolation — this enables structured log aggregation and search in Sentry
- Use `Sentry.logger` for observability-grade messages (errors, key business events); let high-volume debug logging stay local
- Set `before_send_log` to drop `:trace` and `:debug` levels in production
- Combine `Sentry.logger.error(...)` with `Sentry.capture_exception(e)` for errors — the log provides context, the exception provides the stack trace

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Logs not appearing in Sentry | Set `config.enable_logs = true`; verify `sentry-ruby` ≥ 5.27.0 |
| Breadcrumbs not attached to events | Check `breadcrumbs_logger` includes the right symbol for your stack |
| `Sentry.logger` call crashes | Ensure `Sentry.init` was called before `Sentry.logger` is accessed |
| High log volume | Use `before_send_log` to filter by level; set `:debug` and `:trace` to drop in production |

---

## Reference: Metrics

# Metrics — Sentry Ruby SDK

> Minimum SDK: `sentry-ruby` v6.3.0+
> Metrics are enabled by default (`config.enable_metrics = true`). The v6.3.0 release replaced the beta `increment` API with `count`.

## Contents

- [Configuration](#configuration)
- [Metric Types](#metric-types)
- [Unit Reference](#unit-reference)
- [Sidekiq Metrics](#sidekiq-metrics)
- [Detecting Existing Metric Patterns](#detecting-existing-metric-patterns)
- [`before_send_metric` Hook](#before_send_metric-hook)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Configuration

```ruby
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  # Metrics on by default. To filter or enrich before sending:
  config.before_send_metric = lambda do |metric|
    return nil if metric.name.start_with?("internal.")
    metric.attributes[:environment] ||= Rails.env
    metric
  end
end
```

## Metric Types

### Counter — occurrence counts

```ruby
Sentry.metrics.count("api.requests", attributes: { endpoint: "/orders", status: "200" })
Sentry.metrics.count("user.signup", attributes: { plan: "pro" })
```

### Gauge — current value (can go up or down)

```ruby
Sentry.metrics.gauge("sidekiq.queue.depth", Sidekiq::Stats.new.enqueued)
Sentry.metrics.gauge("cache.size", Rails.cache.stats[:curr_items])
```

### Distribution — statistical spread of a value

```ruby
Sentry.metrics.distribution("http.response_time", duration_ms, unit: "millisecond",
  attributes: { route: "/api/orders" })
Sentry.metrics.distribution("db.query_time", query_ms, unit: "millisecond",
  attributes: { table: "orders" })
```

## Unit Reference

| Category | Values |
|----------|--------|
| Duration | `"nanosecond"`, `"microsecond"`, `"millisecond"`, `"second"`, `"minute"`, `"hour"` |
| Data | `"byte"`, `"kilobyte"`, `"megabyte"`, `"gigabyte"` |
| Fractions | `"ratio"`, `"percent"` |
| None | `"none"` (default) |

## Sidekiq Metrics

Two complementary approaches cover different aspects of Sidekiq observability:

### Option A — Server middleware (per-job metrics)

A Sidekiq server middleware fires for every job execution — the right tool for job duration, throughput, and error rate broken down by queue and worker class.

```ruby
# lib/sentry_job_metrics.rb
class SentryJobMetrics
  def call(worker, job, queue)
    start = Time.now
    yield
    attrs = { queue: queue, worker: worker.class.name }
    Sentry.metrics.distribution("sidekiq.job.duration",
      (Time.now - start) * 1000, unit: "millisecond", attributes: attrs)
    Sentry.metrics.count("sidekiq.job.success", attributes: attrs)
  rescue => e
    Sentry.metrics.count("sidekiq.job.failure",
      attributes: { queue: queue, worker: worker.class.name })
    raise
  end
end

# config/initializers/sidekiq.rb
Sidekiq.configure_server do |config|
  config.server_middleware do |chain|
    chain.add SentryJobMetrics
  end
end
```

**What this gives you:** `sidekiq.job.duration` (p50/p95/p99 per queue + worker), `sidekiq.job.success` and `sidekiq.job.failure` counters.

**What it cannot give you:** queue depth, queue latency (oldest job age), retry/dead queue sizes — these are aggregate stats that require polling `Sidekiq::Stats`.

### Option B — Aggregate queue stats (periodic sampling)

For queue depth and latency, poll `Sidekiq::Stats` on a schedule. A lightweight background thread or a recurring Sidekiq job both work:

```ruby
# config/initializers/sentry_sidekiq_stats.rb
Thread.new do
  loop do
    begin
      stats = Sidekiq::Stats.new
      Sentry.metrics.gauge("sidekiq.enqueued",  stats.enqueued)
      Sentry.metrics.gauge("sidekiq.retries",   stats.retry_size)
      Sentry.metrics.gauge("sidekiq.dead",      stats.dead_size)

      Sidekiq::Queue.all.first(10).each do |q|
        attrs = { queue: q.name }
        Sentry.metrics.gauge("sidekiq.queue.depth",   q.size,    attributes: attrs)
        Sentry.metrics.gauge("sidekiq.queue.latency", q.latency,
          unit: "second", attributes: attrs)
      end
    rescue => e
      # don't crash the thread on transient Redis errors
    end
    sleep 30
  end
end
```

> **Production note:** In forking servers (Puma, Unicorn), start the polling thread in `on_worker_boot` / `after_fork` — threads don't survive `fork()`. Consider using a Sidekiq periodic job instead of a bare thread for better reliability and error visibility.

**Use both together** for complete Sidekiq visibility: the middleware captures per-job detail, the poller captures queue health over time.

## Detecting Existing Metric Patterns

Before adding Sentry metrics, scan for existing instrumentation to migrate or complement:

```bash
# StatsD / Datadog / Prometheus calls
grep -rE "(statsd|dogstatsd|prometheus|\.gauge|\.distribution|\.histogram|\.increment|\.timing)" \
  app/ lib/ --include="*.rb" | grep -v "_spec\|_test"

# Sidekiq::Stats usage (shows what's already being tracked)
grep -rn "Sidekiq::Stats\|Sidekiq::Queue" app/ lib/ --include="*.rb"
```

## `before_send_metric` Hook

```ruby
config.before_send_metric = lambda do |metric|
  return nil if metric.name.start_with?("internal.")
  metric.attributes.delete(:user_id)  # strip PII
  metric
end
```

`MetricEvent` properties:

| Property | Type | Description |
|----------|------|-------------|
| `name` | `String` | Metric identifier |
| `type` | `Symbol` | `:counter`, `:gauge`, or `:distribution` |
| `value` | `Numeric` | Measurement value |
| `unit` | `String?` | Measurement unit |
| `attributes` | `Hash` | Custom key-value pairs |
| `trace_id` | `String?` | Auto-linked when inside a transaction |

## Best Practices

- Use `count` for events, `gauge` for current state, `distribution` for latency/sizes
- Always set `unit:` on distributions — enables proper chart rendering
- Use `attributes:` to slice by queue name, route, status code — these become filter dimensions
- Use `before_send_metric` to strip PII (user IDs, email addresses) from attribute values
- Metrics emitted inside a Sentry transaction are trace-linked automatically

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Metrics not in Sentry | Verify `enable_metrics` is not `false`; check DSN |
| `count` values look wrong | Sentry diffs lifetime counters — reporting deltas directly avoids confusion |
| `before_send_metric` not filtering | Return `nil`, not `false`, to drop a metric |
| Per-job breakdown missing | Ensure `SentryJobMetrics` middleware is added to `server_middleware`, not `client_middleware` |
| Queue depth always zero | Verify the stats polling thread is running; check Redis connectivity |

---

## Reference: Migration

# Migrating to Sentry — Ruby SDK

> Minimum SDK: `sentry-ruby` v5.0.0+ (Rails: also add `sentry-rails`)
> Covers migrations from: AppSignal, Honeybadger, Bugsnag, Rollbar, Airbrake

## Contents

- [Step 1: Detect What's in the Codebase](#step-1-detect-whats-in-the-codebase)
- [AppSignal → Sentry](#appsignal--sentry)
- [Honeybadger → Sentry](#honeybadger--sentry)
- [Bugsnag → Sentry](#bugsnag--sentry)
- [Rollbar → Sentry](#rollbar--sentry)
- [Airbrake → Sentry](#airbrake--sentry)
- [Universal Migration Checklist](#universal-migration-checklist)
- [Troubleshooting](#troubleshooting)

## Step 1: Detect What's in the Codebase

```bash
# Find competitor gems
grep -iE '\bappsignal\b|\bhoneybadger\b|\bbugsnag\b|\brollbar\b|\bairbrake\b' Gemfile Gemfile.lock 2>/dev/null

# Find call sites across the app
grep -rn "Appsignal\.\|Honeybadger\.\|Bugsnag\.\|Rollbar\.\|Airbrake\." \
  app/ lib/ config/ --include="*.rb" | grep -v "_spec\|_test"

# Find config files to remove after migration
ls config/appsignal.yml \
   config/honeybadger.yml .honeybadger.yml \
   config/initializers/bugsnag.rb \
   config/initializers/rollbar.rb \
   config/initializers/airbrake.rb 2>/dev/null
```

---

## AppSignal → Sentry

**Gemfile:**
```ruby
# Remove:
gem "appsignal"

# Add:
gem "sentry-ruby"
gem "sentry-rails"     # if Rails
gem "sentry-sidekiq"   # if Sidekiq
```

**Delete:** `config/appsignal.yml`, `config/initializers/appsignal.rb`

### API mapping

| AppSignal | Sentry |
|-----------|--------|
| `Appsignal.report_error(e)` | `Sentry.capture_exception(e)` |
| `Appsignal.send_error(e)` | `Sentry.capture_exception(e)` |
| `Appsignal.set_error(e)` | `Sentry.capture_exception(e)` |
| `Appsignal.listen_for_error { }` | `begin … rescue => e; Sentry.capture_exception(e); raise; end` |
| `Appsignal.tag_request(key: val)` | `Sentry.set_tags(key: val)` |
| `Appsignal.add_tags(key: val)` | `Sentry.set_tags(key: val)` |
| `Appsignal.add_custom_data(hash)` | `Sentry.set_context("custom", hash)` |
| `Appsignal.set_action("name")` | `Sentry.get_current_scope.set_transaction_name("name")` |
| `Appsignal.add_breadcrumb(cat, action, msg)` | `Sentry.add_breadcrumb(Sentry::Breadcrumb.new(category: cat, message: msg))` |
| `Appsignal.instrument("name") { }` | `Sentry.with_child_span(op: "name") { }` |
| `Appsignal.set_gauge("m", val, tags)` | `Sentry.metrics.gauge("m", val, attributes: tags)` |
| `Appsignal.increment_counter("m", val, tags)` | `Sentry.metrics.count("m", value: val, attributes: tags)` |

### Find call sites

```bash
grep -rn "Appsignal\.\(report_error\|send_error\|set_error\|listen_for_error\|tag_request\|add_tags\|add_custom_data\|instrument\|set_gauge\|increment_counter\)" \
  app/ lib/ --include="*.rb"
```

### Initializer

```ruby
# config/initializers/sentry.rb
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.breadcrumbs_logger = [:active_support_logger, :http_logger]
  config.send_default_pii = true
  config.traces_sample_rate = 1.0
  config.enable_logs = true
end
```

---

## Honeybadger → Sentry

**Gemfile:**
```ruby
# Remove:
gem "honeybadger"

# Add:
gem "sentry-ruby"
gem "sentry-rails"
```

**Delete:** `config/honeybadger.yml`, `.honeybadger.yml`, `config/initializers/honeybadger.rb`

### API mapping

| Honeybadger | Sentry |
|-------------|--------|
| `Honeybadger.notify(e)` | `Sentry.capture_exception(e)` |
| `Honeybadger.notify("message")` | `Sentry.capture_message("message")` |
| `Honeybadger.notify(e, context: hash)` | `Sentry.with_scope { \|s\| s.set_context("ctx", hash); Sentry.capture_exception(e) }` |
| `Honeybadger.context(key: val)` | `Sentry.set_tags(key: val)` |
| `Honeybadger.context { \|c\| c[:key] = val }` | `Sentry.configure_scope { \|s\| s.set_context("app", {key: val}) }` |
| `Honeybadger.context.clear!` | `Sentry.get_current_scope.clear` |
| `Honeybadger.add_breadcrumb(msg, metadata: h)` | `Sentry.add_breadcrumb(Sentry::Breadcrumb.new(message: msg, data: h))` |
| `Honeybadger.exception_filter { \|n\| n.halt! if … }` | `config.before_send = lambda { \|e, _h\| nil if … }` |

### Find call sites

```bash
grep -rn "Honeybadger\.\(notify\|context\|add_breadcrumb\|exception_filter\)" \
  app/ lib/ --include="*.rb"
```

---

## Bugsnag → Sentry

**Gemfile:**
```ruby
# Remove:
gem "bugsnag"

# Add:
gem "sentry-ruby"
gem "sentry-rails"     # if Rails
gem "sentry-sidekiq"   # if Sidekiq
```

**Delete:** `config/initializers/bugsnag.rb`

### API mapping

| Bugsnag | Sentry |
|---------|--------|
| `Bugsnag.notify(e)` | `Sentry.capture_exception(e)` |
| `Bugsnag.notify(e) { \|event\| event.severity = "warning" }` | `Sentry.capture_exception(e, level: :warning)` |
| `Bugsnag.notify(e) { \|event\| event.add_metadata(:ctx, hash) }` | `Sentry.with_scope { \|s\| s.set_context("ctx", hash); Sentry.capture_exception(e) }` |
| `Bugsnag.notify(e) { \|event\| event.set_user(id, email, name) }` | `Sentry.set_user(id: id, email: email, username: name)` |
| `Bugsnag.leave_breadcrumb(name, meta, type)` | `Sentry.add_breadcrumb(Sentry::Breadcrumb.new(message: name, data: meta, category: type))` |
| `Bugsnag.add_metadata(:section, hash)` | `Sentry.set_context("section", hash)` |
| `Bugsnag.configure { \|c\| c.discard_classes << "MyError" }` | `config.before_send = lambda { \|e, h\| h[:exception].is_a?(MyError) ? nil : e }` |
| `event.ignore!` (in on_error callback) | Return `nil` from `config.before_send` |

### Find call sites

```bash
grep -rn "Bugsnag\.\(notify\|leave_breadcrumb\|add_metadata\|clear_metadata\|start_session\)" \
  app/ lib/ --include="*.rb"
```

---

## Rollbar → Sentry

**Gemfile:**
```ruby
# Remove:
gem "rollbar"

# Add:
gem "sentry-ruby"
gem "sentry-rails"     # if Rails
gem "sentry-sidekiq"   # if Sidekiq
```

**Delete:** `config/initializers/rollbar.rb`

### API mapping

| Rollbar | Sentry |
|---------|--------|
| `Rollbar.error(e)` | `Sentry.capture_exception(e)` |
| `Rollbar.warning(msg)` | `Sentry.capture_message(msg, level: :warning)` |
| `Rollbar.info(msg, extra)` | `Sentry.with_scope { \|s\| s.set_context("extra", extra); Sentry.capture_message(msg, level: :info) }` |
| `Rollbar.critical(e)` | `Sentry.capture_exception(e, level: :fatal)` |
| `Rollbar.debug(msg)` | `Sentry.capture_message(msg, level: :debug)` |
| `Rollbar.log(level, e)` | `Sentry.capture_exception(e, level: { "critical" => :fatal }.fetch(level, level.to_sym))` |
| `Rollbar.scoped(person: p) { }` | `Sentry.with_scope { \|s\| s.set_user(p); ... }` |
| `Rollbar.scope!(person: p)` | `Sentry.set_user(p)` |
| `Rollbar.silenced { }` | `# remove — no Sentry equivalent needed` |

Rollbar uses `'warning'` level; Sentry uses `:warning`. Rollbar uses `'critical'`; map to Sentry's `:fatal`.

### Find call sites

```bash
grep -rn "Rollbar\.\(error\|warning\|warn\|info\|debug\|critical\|log\|scoped\|scope\)" \
  app/ lib/ --include="*.rb"
```

---

## Airbrake → Sentry

**Gemfile:**
```ruby
# Remove:
gem "airbrake"
gem "airbrake-ruby"    # if present separately

# Add:
gem "sentry-ruby"
gem "sentry-rails"     # if Rails
gem "sentry-sidekiq"   # if Sidekiq
```

**Delete:** `config/initializers/airbrake.rb`

Also check for and remove: `require 'airbrake/capistrano'` in `Capfile`, `require 'airbrake/rake'` in `Rakefile`, and any Sidekiq/DelayedJob/Resque middleware references.

### API mapping

| Airbrake | Sentry |
|----------|--------|
| `Airbrake.notify(e)` | `Sentry.capture_exception(e)` |
| `Airbrake.notify(e, params)` | `Sentry.with_scope { \|s\| s.set_context("params", params); Sentry.capture_exception(e) }` |
| `Airbrake.notify_sync(e)` | `Sentry.capture_exception(e)` (Sentry handles delivery asynchronously) |
| `Airbrake.notify("message")` | `Sentry.capture_message("message")` |
| `Airbrake.merge_context(hash)` | `Sentry.set_context("app", hash)` |
| `Airbrake.add_filter { \|n\| n.ignore! if ... }` | `config.before_send = lambda { \|e, _h\| ... ? nil : e }` |
| `Airbrake.add_filter(MyFilter)` | `config.before_send = lambda { \|e, _h\| ... }` |
| `notice[:context][:user_id] = id` | `Sentry.set_user(id: id)` |
| `Airbrake.notify_deploy(info)` | Use Sentry release tracking via `SENTRY_RELEASE` env var |
| `Airbrake.notify_request(...)` | Automatic via `sentry-rails` tracing |
| `Airbrake.notify_query(...)` | Automatic via `sentry-rails` ActiveRecord spans |

### Find call sites

```bash
grep -rn "Airbrake\.\(notify\|notify_sync\|merge_context\|add_filter\|notify_request\|notify_query\)" \
  app/ lib/ --include="*.rb"
```

---

## Universal Migration Checklist

Works for any tool not covered above:

```bash
# Error capture
grep -rn "\.\(notify\|report_error\|send_error\|notice_error\)" \
  app/ lib/ --include="*.rb" | grep -v "_spec\|_test"

# Context / tagging
grep -rn "\.\(context\|tag_request\|add_tags\|add_custom_attributes\)" \
  app/ lib/ --include="*.rb" | grep -v "_spec\|_test"

# Custom spans / instrumentation
grep -rn "\.\(instrument\|monitor\|in_transaction\)" \
  app/ lib/ --include="*.rb" | grep -v "_spec\|_test"

# Metric calls
grep -rn "\.\(set_gauge\|increment_counter\|record_metric\|gauge\|histogram\|timing\)" \
  app/ lib/ --include="*.rb" | grep -v "_spec\|_test"

# Environment variables to update
grep -rn "APPSIGNAL\|HONEYBADGER\|BUGSNAG\|ROLLBAR\|AIRBRAKE" \
  .env .env.* config/ --include="*.rb" --include="*.yml" 2>/dev/null
```

### Environment variable mapping

| Tool | Old env var | Sentry |
|------|-------------|--------|
| AppSignal | `APPSIGNAL_PUSH_API_KEY` | `SENTRY_DSN` |
| Honeybadger | `HONEYBADGER_API_KEY` | `SENTRY_DSN` |
| Bugsnag | `BUGSNAG_API_KEY` | `SENTRY_DSN` |
| Rollbar | `ROLLBAR_ACCESS_TOKEN` | `SENTRY_DSN` |
| Airbrake | `AIRBRAKE_PROJECT_ID` + `AIRBRAKE_PROJECT_KEY` | `SENTRY_DSN` |

### Rollout strategy

Run both tools in parallel for one release cycle, then remove the old gem once Sentry is receiving events in production.

```ruby
# Temporary dual-capture shim — remove after rollout validation:
module ErrorCapture
  def self.capture(exception, context: {})
    Sentry.with_scope do |scope|
      scope.set_context("extra", context) unless context.empty?
      Sentry.capture_exception(exception)
    end
    begin
      OldTool.notify(exception)  # replace OldTool with actual constant
    rescue => e
      Sentry.logger.warn("OldTool capture failed: %{message}", message: e.message)
    end
  end
end
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing errors after migration | Ensure `sentry-rails` is present — `sentry-ruby` alone doesn't hook Rails error handlers |
| Context missing from events | Old tools often set context via middleware; replicate with a `before_action` calling `Sentry.set_user` / `Sentry.set_tags` |
| Old gem still loading | Check `Gemfile.lock` — it may be a transitive dependency |
| Distributed traces broken | Ensure all services have migrated and propagate `sentry-trace` + `baggage` headers |

---

## Reference: Profiling

# Profiling — Sentry Ruby SDK

> ⚠️ **Beta** — profiling is in beta and may have bugs.
> Minimum SDK: `sentry-ruby` v5.9.0+ (StackProf), v5.21.0+ (Vernier)

Profiling attaches CPU/memory samples to Sentry transactions. It requires tracing to be enabled first — `profiles_sample_rate` is relative to `traces_sample_rate`.

## Contents

- [Choosing a profiler](#choosing-a-profiler)
- [StackProf setup](#stackprof-setup)
- [Vernier setup](#vernier-setup)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Choosing a Profiler

| Profiler | Gem | Min sentry-ruby | Min Ruby | Notes |
|----------|-----|-----------------|----------|-------|
| StackProf | `stackprof` | v5.9.0 | Any | Wall-clock or CPU sampling |
| Vernier | `vernier` | v5.21.0 | 3.2.1+ | Lower overhead; GVL-aware |

Vernier is preferred for Ruby 3.2.1+ applications. Use StackProf for older Ruby versions.

### GVL-aware profiling (Vernier)

Ruby's Global VM Lock (GVL) means only one thread executes Ruby code at a time. StackProf only samples the thread holding the GVL, so multi-threaded apps (Puma, Sidekiq) show incomplete profiles. Vernier is GVL-aware — it tracks all threads including those waiting on I/O or the GVL, giving a complete picture of where time is spent across the entire process.

### Production overhead

Both profilers use sampling (not tracing), so overhead is low. Expect ~2-5% CPU overhead per profiled transaction. Use `profiles_sample_rate` to control how many transactions are profiled — start with `0.1` in production and adjust based on your performance budget.

## StackProf Setup

```ruby
# Gemfile
gem "sentry-ruby"
gem "sentry-rails"   # if Rails
gem "stackprof"
```

```ruby
# config/initializers/sentry.rb (Rails) or Sentry.init block
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.traces_sample_rate = 1.0    # tracing must be enabled
  config.profiles_sample_rate = 1.0  # relative to traces_sample_rate
end
```

## Vernier Setup

```ruby
# Gemfile
gem "sentry-ruby"
gem "sentry-rails"   # if Rails
gem "vernier"
```

```ruby
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.traces_sample_rate = 1.0
  config.profiles_sample_rate = 1.0
  config.profiler_class = Sentry::Vernier::Profiler  # opt into Vernier
end
```

## Configuration

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `profiles_sample_rate` | Float | `nil` | Fraction of sampled transactions that include a profile [0.0–1.0] |
| `profiler_class` | Class | StackProf profiler | Set to `Sentry::Vernier::Profiler` to use Vernier |

`profiles_sample_rate` is **relative** to `traces_sample_rate`. With `traces_sample_rate = 0.1` and `profiles_sample_rate = 0.5`, 5% of total transactions include a profile.

## Best Practices

- Start with `profiles_sample_rate = 1.0` in development to verify profiles appear in Sentry
- Lower to `0.1`–`0.5` in production — profiling adds overhead per sampled transaction
- Prefer Vernier on Ruby 3.2.1+ for lower overhead and GVL visibility
- Profiling without tracing is not supported — ensure `traces_sample_rate > 0`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No profiles in Sentry | Verify `traces_sample_rate > 0` — profiling requires tracing to be active |
| `Sentry::Vernier::Profiler` not found | Ensure `vernier` gem is installed and `sentry-ruby` ≥ 5.21.0 |
| StackProf missing constant error | Add `gem "stackprof"` to Gemfile and run `bundle install` |
| Profiles on some requests only | Expected — `profiles_sample_rate` is a fraction of sampled transactions, not all requests |
| Beta instability | Check [sentry-ruby releases](https://github.com/getsentry/sentry-ruby/releases) for fixes; report issues there |

---

## Reference: Tracing

# Tracing — Sentry Ruby SDK

> Minimum SDK: `sentry-ruby` v5.10.0+ for distributed tracing out of the box

## Contents

- [Configuration](#configuration)
- [Automatic Instrumentation](#automatic-instrumentation)
- [Custom Instrumentation](#custom-instrumentation)
- [Distributed Tracing](#distributed-tracing)
- [`before_send_transaction` hook](#before_send_transaction-hook)
- [OpenTelemetry — OTLP Integration](#opentelemetry--otlp-integration)
- [Framework Auto-Instrumentation Summary](#framework-auto-instrumentation-summary)
- [Request Queue Time](#request-queue-time)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Configuration

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `traces_sample_rate` | Float | `nil` | Uniform sample rate [0.0–1.0]; `nil` disables tracing |
| `traces_sampler` | Lambda | `nil` | Custom per-transaction sampling; overrides `traces_sample_rate` |
| `trace_propagation_targets` | Array | `[/.*/]` | URLs to inject `sentry-trace` + `baggage` headers into |
| `propagate_traces` | Boolean | `true` | Propagate trace headers on outbound Net::HTTP requests |
| `capture_queue_time` | Boolean | `true` | Record request queue time from `X-Request-Start` header (v6.4.0+) |

```ruby
Sentry.init do |config|
  config.traces_sample_rate = 1.0  # set to 0.05–0.2 in production

  # — or — per-transaction dynamic sampling:
  config.traces_sampler = lambda do |sampling_context|
    tc = sampling_context[:transaction_context]
    case tc[:op]
    when /http/
      case tc[:name]
      when /health/ then 0.0   # drop health checks
      else               0.1
      end
    when /sidekiq/ then 0.01
    else                0.0
    end
  end
end
```

## Automatic Instrumentation

### Rails (via `sentry-rails`)

No extra code needed. The following are auto-instrumented:

- `ActionController` — one transaction per request
- `ActiveRecord` — SQL queries as child spans
- `ActionMailer` — mail delivery as child spans
- `ActiveJob` — job execution as child spans
- `Net::HTTP` outbound calls — child spans with trace header propagation

### Rack / Sinatra (via `Sentry::Rack::CaptureExceptions`)

```ruby
use Sentry::Rack::CaptureExceptions
```

Wraps each Rack request in a transaction.

### Sidekiq (via `sentry-sidekiq`)

No extra code. Each worker execution becomes a transaction, inheriting distributed trace context from the enqueuing request.

## Custom Instrumentation

### Wrap a block in a child span (preferred)

```ruby
Sentry.with_child_span(op: "process_items", description: "processing order items") do |span|
  span&.set_data(:item_count, items.length)
  span&.set_data(:order_id, order.id)
  order.process_items
end
```

`with_child_span` yields `nil` when not sampling — always guard data calls with `span&.set_data`.

### Child span on an existing transaction

```ruby
transaction = Sentry.get_current_scope.get_transaction
transaction&.with_child_span(op: "cache.fetch", description: "fetch user cache") do |span|
  span&.set_data("cache.key", cache_key)
  Rails.cache.fetch(cache_key) { User.find(user_id) }
end
```

### Manual transaction (only when no automatic transaction wraps the code)

```ruby
transaction = Sentry.start_transaction(
  name: "ProcessBatch",
  op: "background_job",
  sampled: true
)
Sentry.get_current_scope.set_span(transaction)

begin
  process_batch(records)
  transaction.set_status("ok")
rescue => e
  transaction.set_status("internal_error")
  Sentry.capture_exception(e)
  raise
ensure
  transaction.finish
end
```

### Span data conventions

```ruby
Sentry.with_child_span(op: "http.client") do |span|
  span&.set_data("http.method", "POST")
  span&.set_data("http.url", endpoint)
  response = http_client.post(endpoint, body)
  span&.set_data("http.status_code", response.status)
  response
end
```

## Distributed Tracing

Distributed tracing works out of the box for same-process `Net::HTTP` calls — Sentry patches Net::HTTP to inject `sentry-trace` and `baggage` headers automatically.

### Manual header propagation (custom HTTP clients)

```ruby
headers = Sentry.get_trace_propagation_headers
# => { "sentry-trace" => "abc...xyz-1", "baggage" => "sentry-trace_id=abc..." }

faraday_conn.get("/api/orders") do |req|
  headers.each { |k, v| req.headers[k] = v }
end
```

### Frontend trace stitching (Ruby backend → JS frontend)

Inject Sentry trace metadata into your HTML `<head>` so the browser SDK can continue the same trace:

**Rails (`app/views/layouts/application.html.erb`):**

```erb
<head>
  <%= Sentry.get_trace_propagation_meta.html_safe %>
  ...
</head>
```

This renders two `<meta>` tags that `@sentry/browser` (and framework SDKs like `@sentry/react`, `sentry-svelte-sdk`) automatically read on page load. Requires `browserTracingIntegration` on the frontend SDK.

### Inbound trace propagation (accepting from upstream)

Rails and Rack middleware automatically read incoming `sentry-trace` and `baggage` headers and continue the trace — no configuration required.

## `before_send_transaction` hook

```ruby
config.before_send_transaction = lambda do |event, _hint|
  # Drop health check transactions
  if event.transaction&.match?(%r{/health(z|check)?$})
    next nil
  end

  # Scrub sensitive data from DB spans
  event.spans.each do |span|
    if span[:op]&.start_with?("db") && span[:description]&.include?("password")
      span[:description] = "<filtered>"
    end
  end

  event
end
```

## OpenTelemetry — OTLP Integration

> Minimum SDK: `sentry-ruby` v6.4.0+ with `sentry-opentelemetry` v6.4.0+

If the project already uses OpenTelemetry for tracing or logging, **use the OTLP integration instead of Sentry's native tracing**. Sentry ingests OTel spans directly via its OTLP endpoint — no span conversion, no dual instrumentation.

**When to use this path:** OTel tracing gems (`opentelemetry-sdk`, `opentelemetry-instrumentation-*`) detected in the Gemfile, or `OpenTelemetry::SDK.configure` found in source.

**When NOT to use this path:** No OpenTelemetry in the project — use Sentry's native `traces_sample_rate` instead.

**Logging:** OTLP replaces Sentry native *tracing* only. If the project does not use OTel for logging (`opentelemetry-logs-sdk` not in Gemfile), still set `config.enable_logs = true` for Sentry structured logging — this is the common case.

### Setup

```ruby
# Gemfile — add alongside existing opentelemetry gems:
gem "sentry-opentelemetry"
gem "opentelemetry-exporter-otlp"  # required for OTLP export
```

```ruby
# config/initializers/sentry.rb
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.send_default_pii = true
  config.otlp.enabled = true
  config.enable_logs = true  # keep Sentry native logging unless OTel logs SDK is also present

  # Do NOT set traces_sample_rate — tracing is handled by OTel
  # Errors, Logs, Crons, and Metrics are still captured natively by Sentry
  # and automatically linked to the active OTel trace
end
```

```ruby
# config/initializers/opentelemetry.rb — keep your existing OTel setup:
OpenTelemetry::SDK.configure do |c|
  c.use_all  # or specific instrumentations
  # Sentry auto-adds its OTLP exporter and propagator —
  # no manual SpanProcessor or Propagator wiring needed
end
```

### How it works

- Sentry derives an OTLP endpoint from your DSN and registers a `BatchSpanProcessor` with the existing `TracerProvider` — your other exporters (Jaeger, Zipkin, Collector) continue working
- A propagator injects `sentry-trace` + `baggage` headers for distributed tracing with other Sentry-instrumented services
- Errors captured via `Sentry.capture_exception` are automatically linked to the active OTel trace/span via shared `trace_id`

### OTLP configuration options

| Option | Default | Purpose |
|--------|---------|---------|
| `config.otlp.enabled` | `false` | Master switch |
| `config.otlp.setup_otlp_traces_exporter` | `true` | Auto-configure exporter; set `false` if you send to your own Collector |
| `config.otlp.setup_propagator` | `true` | Auto-configure propagator; set `false` if you manage propagation yourself |

### Important

**Do not combine OTLP with native Sentry tracing.** When `config.otlp.enabled = true`:
- Do **not** set `traces_sample_rate` or `traces_sampler`
- Do **not** set `config.instrumenter = :otel` (that is the legacy SpanProcessor approach)
- Do **not** call `Sentry.with_child_span` or `Sentry.start_transaction` — use OTel's `tracer.in_span` instead

## Framework Auto-Instrumentation Summary

| Framework / Library | Gem Required | What's Instrumented |
|--------------------|-------------|---------------------|
| Rails controllers | `sentry-rails` | Requests → transactions; actions → spans |
| ActiveRecord | `sentry-rails` | SQL queries → spans |
| ActionMailer | `sentry-rails` | Mail delivery → spans |
| ActiveJob | `sentry-rails` | Job execution → spans |
| Sidekiq workers | `sentry-sidekiq` | Worker execution → transactions |
| Resque workers | `sentry-resque` | Worker execution → transactions |
| DelayedJob | `sentry-delayed_job` | Job execution → transactions |
| Net::HTTP | `sentry-ruby` | Outbound HTTP → spans + header propagation |
| Redis | `sentry-ruby` | Redis commands → spans (needs `:redis_logger`) |
| GraphQL | `sentry-ruby` | Queries → transactions (enable with `enabled_patches`) |

## Request Queue Time

> Minimum SDK: `sentry-ruby` v6.4.0+. Enabled by default (`capture_queue_time = true`).

Sentry automatically reads the `X-Request-Start` header and records how long the request waited in the server queue before a worker thread picked it up. The value is stored as `http.server.request.time_in_queue` (milliseconds) on the transaction.

When running behind Puma, the SDK subtracts `puma.request_body_wait` (time Puma spent receiving the request body from a slow client) to isolate actual queue time from upload time.

### Proxy configuration required

Your reverse proxy must set the header. Without it, no queue time is recorded.

**Nginx:**
```nginx
proxy_set_header X-Request-Start "t=${msec}";
```

**Heroku:** Sets `X-Request-Start` automatically — no configuration needed.

**HAProxy:**
```
http-request set-header X-Request-Start t=%[date()]%[date_us()]
```

### Disable

```ruby
config.capture_queue_time = false
```

### Why this matters

High queue time means Puma workers are saturated — requests are waiting for a free thread. This is a key indicator for scaling decisions. Sentry surfaces it in the transaction waterfall so you can distinguish "the app is slow" from "the app was waiting for a worker."

## Best Practices

- Set `traces_sample_rate = 1.0` in development/staging; use `0.05`–`0.2` in production
- Use `traces_sampler` to exclude health checks and low-value endpoints
- Set `op` to a semantic value: `"http.server"`, `"db.query"`, `"queue.process"`, `"cache.get"`
- Prefer `with_child_span` over manual transaction management — it handles errors and finishing automatically
- Always guard span calls with `span&.set_data` — `with_child_span` yields `nil` when not sampling

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transactions in dashboard | Set `traces_sample_rate > 0`; ensure `sentry-rails` or Rack middleware is present |
| Sidekiq jobs not traced | Add `sentry-sidekiq` gem; no other config needed |
| Missing DB spans | Ensure `sentry-rails` is loaded (it patches ActiveRecord) |
| Distributed trace not stitching | Verify `sentry-trace` + `baggage` headers are forwarded by all services |
| Frontend trace not linking | Add `<%= Sentry.get_trace_propagation_meta.html_safe %>` to your HTML `<head>` |
| Health check transactions flooding | Use `traces_sampler` to return `0.0` for health check transaction names |
| `before_send_transaction` not filtering | Return `nil` (not `false`) to drop the event |
