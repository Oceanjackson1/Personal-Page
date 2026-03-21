---
title: "Sentry Python SDK"
description: "Full Sentry SDK setup for Python. Use when asked to 'add Sentry to Python', 'install sentry-sdk', 'setup Sentry in Python', or configure error monitoring, tracing, profiling, logging, metrics, crons, or AI monitoring for Python applications. Suppo..."
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "python", "sdk"]
date: 2026-03-20
---

# Sentry Python SDK

Opinionated wizard that scans your Python project and guides you through complete Sentry setup.

## Invoke This Skill When

- User asks to "add Sentry to Python" or "setup Sentry" in a Python app
- User wants error monitoring, tracing, profiling, logging, metrics, or crons in Python
- User mentions `sentry-sdk`, `sentry_sdk`, or Sentry + any Python framework
- User wants to monitor Django views, Flask routes, FastAPI endpoints, Celery tasks, or scheduled jobs

> **Note:** SDK versions and APIs below reflect Sentry docs at time of writing (sentry-sdk 2.x).
> Always verify against [docs.sentry.io/platforms/python/](https://docs.sentry.io/platforms/python/) before implementing.

---

## Phase 1: Detect

Run these commands to understand the project before making recommendations:

```bash
# Check existing Sentry
grep -i sentry requirements.txt pyproject.toml setup.cfg setup.py 2>/dev/null

# Detect web framework
grep -rE "django|flask|fastapi|starlette|aiohttp|tornado|quart|falcon|sanic|bottle" \
  requirements.txt pyproject.toml 2>/dev/null

# Detect task queues
grep -rE "celery|rq|huey|arq|dramatiq" requirements.txt pyproject.toml 2>/dev/null

# Detect logging libraries
grep -E "loguru" requirements.txt pyproject.toml 2>/dev/null

# Detect AI libraries
grep -rE "openai|anthropic|langchain|huggingface|google-genai|pydantic-ai|litellm" \
  requirements.txt pyproject.toml 2>/dev/null

# Detect schedulers / crons
grep -rE "celery|apscheduler|schedule|crontab" requirements.txt pyproject.toml 2>/dev/null

# Check for companion frontend
ls frontend/ web/ client/ ui/ static/ templates/ 2>/dev/null
```

**What to note:**
- Is `sentry-sdk` already in requirements? If yes, check if `sentry_sdk.init()` is present — may just need feature config.
- Which framework? (Determines where to place `sentry_sdk.init()`.)
- Which task queue? (Celery needs dual-process init; RQ needs a settings file.)
- AI libraries? (OpenAI, Anthropic, LangChain are auto-instrumented.)
- Companion frontend? (Triggers Phase 4 cross-link.)

---

## Phase 2: Recommend

Based on what you found, present a concrete proposal. Don't ask open-ended questions — lead with a recommendation:

**Always recommended (core coverage):**
- ✅ **Error Monitoring** — captures unhandled exceptions, supports `ExceptionGroup` (Python 3.11+)
- ✅ **Logging** — Python `logging` stdlib auto-captured; enhanced if Loguru detected

**Recommend when detected:**
- ✅ **Tracing** — HTTP framework detected (Django/Flask/FastAPI/etc.)
- ✅ **AI Monitoring** — OpenAI/Anthropic/LangChain/etc. detected (auto-instrumented, zero config)
- ⚡ **Profiling** — production apps where performance matters
- ⚡ **Crons** — Celery Beat, APScheduler, or cron patterns detected
- ⚡ **Metrics** — business KPIs, SLO tracking

**Recommendation matrix:**

| Feature | Recommend when... | Reference |
|---------|------------------|-----------|
| Error Monitoring | **Always** — non-negotiable baseline | `${SKILL_ROOT}/references/error-monitoring.md` |
| Tracing | Django/Flask/FastAPI/AIOHTTP/etc. detected | `${SKILL_ROOT}/references/tracing.md` |
| Profiling | Production + performance-sensitive workload | `${SKILL_ROOT}/references/profiling.md` |
| Logging | Always (stdlib); enhanced for Loguru | `${SKILL_ROOT}/references/logging.md` |
| Metrics | Business events or SLO tracking needed | `${SKILL_ROOT}/references/metrics.md` |
| Crons | Celery Beat, APScheduler, or cron patterns | `${SKILL_ROOT}/references/crons.md` |
| AI Monitoring | OpenAI/Anthropic/LangChain/etc. detected | `${SKILL_ROOT}/references/ai-monitoring.md` |

Propose: *"I recommend Error Monitoring + Tracing [+ Logging if applicable]. Want Profiling, Crons, or AI Monitoring too?"*

---

## Phase 3: Guide

### Install

```bash
# Core SDK (always required)
pip install sentry-sdk

# Optional extras (install only what matches detected framework):
pip install "sentry-sdk[django]"
pip install "sentry-sdk[flask]"
pip install "sentry-sdk[fastapi]"
pip install "sentry-sdk[celery]"
pip install "sentry-sdk[aiohttp]"
pip install "sentry-sdk[tornado]"

# Multiple extras:
pip install "sentry-sdk[django,celery]"
```

> Extras are optional — plain `sentry-sdk` works for all frameworks. Extras install complementary packages.

### Quick Start — Recommended Init

Full init enabling the most features with sensible defaults. Place **before** any app/framework code:

```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    environment=os.environ.get("SENTRY_ENVIRONMENT", "production"),
    release=os.environ.get("SENTRY_RELEASE"),   # e.g. "myapp@1.0.0"
    send_default_pii=True,

    # Tracing (lower to 0.1–0.2 in high-traffic production)
    traces_sample_rate=1.0,

    # Profiling — continuous, tied to active spans
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace",

    # Structured logs (SDK ≥ 2.35.0)
    enable_logs=True,
)
```

### Where to Initialize Per Framework

| Framework | Where to call `sentry_sdk.init()` | Notes |
|-----------|-----------------------------------|-------|
| **Django** | Top of `settings.py`, before any imports | No middleware needed — Sentry patches Django internally |
| **Flask** | Before `app = Flask(__name__)` | Must precede app creation |
| **FastAPI** | Before `app = FastAPI()` | `StarletteIntegration` + `FastApiIntegration` auto-enabled together |
| **Starlette** | Before `app = Starlette(...)` | Same auto-integration as FastAPI |
| **AIOHTTP** | Module level, before `web.Application()` | |
| **Tornado** | Module level, before app setup | No integration class needed |
| **Quart** | Before `app = Quart(__name__)` | |
| **Falcon** | Module level, before `app = falcon.App()` | |
| **Sanic** | Inside `@app.listener("before_server_start")` | Sanic's lifecycle requires async init |
| **Celery** | `@signals.celeryd_init.connect` in worker AND in calling process | Dual-process init required |
| **RQ** | `mysettings.py` loaded by worker via `rq worker -c mysettings` | |
| **ARQ** | Both worker module and enqueuing process | |

**Django example** (`settings.py`):
```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    send_default_pii=True,
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace",
    enable_logs=True,
)

# rest of Django settings...
INSTALLED_APPS = [...]
```

**FastAPI example** (`main.py`):
```python
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    send_default_pii=True,
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,
    profile_lifecycle="trace",
    enable_logs=True,
)

from fastapi import FastAPI
app = FastAPI()
```

### Auto-Enabled vs Explicit Integrations

Most integrations activate automatically when their package is installed — no `integrations=[...]` needed:

| Auto-enabled | Explicit required |
|-------------|-------------------|
| Django, Flask, FastAPI, Starlette, AIOHTTP, Tornado, Quart, Falcon, Sanic, Bottle | `DramatiqIntegration` |
| Celery, RQ, Huey, ARQ | `GRPCIntegration` |
| SQLAlchemy, Redis, asyncpg, pymongo | `StrawberryIntegration` |
| Requests, HTTPX, aiohttp-client | `AsyncioIntegration` |
| OpenAI, Anthropic, LangChain, Pydantic AI, MCP | `OpenTelemetryIntegration` |
| Python `logging`, Loguru | `WSGIIntegration` / `ASGIIntegration` |

### For Each Agreed Feature

Walk through features one at a time. Load the reference, follow its steps, verify before moving on:

| Feature | Reference file | Load when... |
|---------|---------------|-------------|
| Error Monitoring | `${SKILL_ROOT}/references/error-monitoring.md` | Always (baseline) |
| Tracing | `${SKILL_ROOT}/references/tracing.md` | HTTP handlers / distributed tracing |
| Profiling | `${SKILL_ROOT}/references/profiling.md` | Performance-sensitive production |
| Logging | `${SKILL_ROOT}/references/logging.md` | Always; enhanced for Loguru |
| Metrics | `${SKILL_ROOT}/references/metrics.md` | Business KPIs / SLO tracking |
| Crons | `${SKILL_ROOT}/references/crons.md` | Scheduler / cron patterns detected |
| AI Monitoring | `${SKILL_ROOT}/references/ai-monitoring.md` | AI library detected |

For each feature: `Read ${SKILL_ROOT}/references/<feature>.md`, follow steps exactly, verify it works.

---

## Configuration Reference

### Key `sentry_sdk.init()` Options

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `dsn` | `str` | `None` | SDK disabled if empty; env: `SENTRY_DSN` |
| `environment` | `str` | `"production"` | e.g., `"staging"`; env: `SENTRY_ENVIRONMENT` |
| `release` | `str` | `None` | e.g., `"myapp@1.0.0"`; env: `SENTRY_RELEASE` |
| `send_default_pii` | `bool` | `False` | Include IP, headers, cookies, auth user |
| `traces_sample_rate` | `float` | `None` | Transaction sample rate; `None` disables tracing |
| `traces_sampler` | `Callable` | `None` | Custom per-transaction sampling (overrides rate) |
| `profile_session_sample_rate` | `float` | `None` | Continuous profiling session rate |
| `profile_lifecycle` | `str` | `"manual"` | `"trace"` = auto-start profiler with spans |
| `profiles_sample_rate` | `float` | `None` | Transaction-based profiling rate |
| `enable_logs` | `bool` | `False` | Send logs to Sentry (SDK ≥ 2.35.0) |
| `sample_rate` | `float` | `1.0` | Error event sample rate |
| `attach_stacktrace` | `bool` | `False` | Stack traces on `capture_message()` |
| `max_breadcrumbs` | `int` | `100` | Max breadcrumbs per event |
| `debug` | `bool` | `False` | Verbose SDK debug output |
| `before_send` | `Callable` | `None` | Hook to mutate/drop error events |
| `before_send_transaction` | `Callable` | `None` | Hook to mutate/drop transaction events |
| `ignore_errors` | `list` | `[]` | Exception types or regex patterns to suppress |
| `auto_enabling_integrations` | `bool` | `True` | Set `False` to disable all auto-detection |

### Environment Variables

| Variable | Maps to | Notes |
|----------|---------|-------|
| `SENTRY_DSN` | `dsn` | |
| `SENTRY_RELEASE` | `release` | Also auto-detected from git SHA, Heroku, CircleCI, CodeBuild, GAE |
| `SENTRY_ENVIRONMENT` | `environment` | |
| `SENTRY_DEBUG` | `debug` | |

---

## Verification

Test that Sentry is receiving events:

```python
# Trigger a real error event — check dashboard within seconds
division_by_zero = 1 / 0
```

Or for a non-crashing check:
```python
sentry_sdk.capture_message("Sentry Python SDK test")
```

If nothing appears:
1. Set `debug=True` in `sentry_sdk.init()` — prints SDK internals to stdout
2. Verify the DSN is correct
3. Check `SENTRY_DSN` env var is set in the running process
4. For Celery/RQ: ensure init runs in the **worker** process, not just the calling process

---

## Phase 4: Cross-Link

After completing Python setup, check for a companion frontend missing Sentry:

```bash
ls frontend/ web/ client/ ui/ 2>/dev/null
cat frontend/package.json web/package.json client/package.json 2>/dev/null \
  | grep -E '"react"|"svelte"|"vue"|"next"|"nuxt"'
```

If a frontend exists without Sentry, suggest the matching skill:

| Frontend detected | Suggest skill |
|-------------------|--------------|
| React / Next.js | `sentry-react-sdk` |
| Svelte / SvelteKit | `sentry-svelte-sdk` |
| Vue / Nuxt | Use `@sentry/vue` — see [docs.sentry.io/platforms/javascript/guides/vue/](https://docs.sentry.io/platforms/javascript/guides/vue/) |
| Other JS/TS | `sentry-react-sdk` (covers generic browser JS patterns) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing | Set `debug=True`, verify DSN, check env vars in the running process |
| Malformed DSN error | Format: `https://<key>@o<org>.ingest.sentry.io/<project>` |
| Django exceptions not captured | Ensure `sentry_sdk.init()` is at the **top** of `settings.py` before other imports |
| Flask exceptions not captured | Init must happen **before** `app = Flask(__name__)` |
| FastAPI exceptions not captured | Init before `app = FastAPI()`; both `StarletteIntegration` and `FastApiIntegration` auto-enabled |
| Celery task errors not captured | Must call `sentry_sdk.init()` in the **worker process** via `celeryd_init` signal |
| Sanic init not working | Init must be inside `@app.listener("before_server_start")`, not module level |
| uWSGI not capturing | Add `--enable-threads --py-call-uwsgi-fork-hooks` to uWSGI command |
| No traces appearing | Verify `traces_sample_rate` is set (not `None`); check that the integration is auto-enabled |
| Profiling not starting | Requires `traces_sample_rate > 0` + either `profile_session_sample_rate` or `profiles_sample_rate` |
| `enable_logs` not working | Requires SDK ≥ 2.35.0; for direct structured logs use `sentry_sdk.logger`; for stdlib bridging use `LoggingIntegration(sentry_logs_level=...)` |
| Too many transactions | Lower `traces_sample_rate` or use `traces_sampler` to drop health checks |
| Cross-request data leaking | Don't use `get_global_scope()` for per-request data — use `get_isolation_scope()` |
| RQ worker not reporting | Pass `--sentry-dsn=""` to disable RQ's own Sentry shortcut; init via settings file instead |

---

## Reference: Ai Monitoring

# AI Monitoring — Sentry Python SDK

> Minimum SDK: `sentry-sdk` 2.1.0+ (core AI spans); 2.45.0+ for auto-enabling all integrations

## Prerequisites

Tracing must be enabled — AI spans require an active transaction:

```python
sentry_sdk.init(dsn="...", traces_sample_rate=1.0)
```

## Integration Matrix

| Integration | Package | Min Library | Auto-Enabled | Status |
|-------------|---------|-------------|-------------|--------|
| OpenAI | `sentry-sdk` | openai 1.0+ | ✅ Yes | Stable |
| Anthropic | `sentry-sdk` | anthropic 0.16.0+ | ✅ Yes | Stable |
| LangChain | `sentry-sdk` | langchain 0.1.0+ | ✅ Yes | Stable |
| LangGraph | `sentry-sdk` | langgraph 0.6.6+ | ✅ Yes | Stable |
| OpenAI Agents SDK | `sentry-sdk` | agents 0.0.19+ | ✅ Yes | ⚠️ Beta |
| Google GenAI | `sentry-sdk` | google-genai 1.29.0+ | ✅ Yes | Stable |
| HuggingFace Hub | `sentry-sdk` | huggingface_hub 0.24.7+ | ✅ Yes | Stable |
| LiteLLM | `sentry-sdk` | litellm 1.77.5+ | ❌ **No** | Stable |
| MCP | `sentry-sdk` | mcp 1.15.0+ | ✅ Yes | Stable |
| Pydantic AI | `sentry-sdk` | pydantic-ai 1.0.0+ | ✅ Yes | ⚠️ Beta |

**LiteLLM MUST be explicitly added to `integrations=[]`.**

## PII Control

Every integration follows the same two-layer control:

| `send_default_pii` | `include_prompts` | Prompts/outputs sent? |
|--------------------|-------------------|----------------------|
| `False` (default) | `True` (default) | ❌ No |
| `True` | `True` (default) | ✅ Yes |
| `True` | `False` | ❌ No |

Set `send_default_pii=True` to capture prompts. Use `include_prompts=False` per-integration to override.

## Configuration Examples

### Auto-enabled integrations (OpenAI, Anthropic, LangChain, etc.)

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    traces_sample_rate=1.0,
    send_default_pii=True,    # required to capture prompts/outputs
)

# OpenAI, Anthropic, LangChain, LangGraph, HuggingFace Hub activate automatically
```

### Explicit configuration with `include_prompts` override

```python
import sentry_sdk
from sentry_sdk.integrations.openai import OpenAIIntegration
from sentry_sdk.integrations.anthropic import AnthropicIntegration

sentry_sdk.init(
    dsn="...",
    traces_sample_rate=1.0,
    send_default_pii=True,
    integrations=[
        OpenAIIntegration(
            include_prompts=True,
            tiktoken_encoding_name="o200k_base",   # for gpt-4o streaming token counts
        ),
        AnthropicIntegration(include_prompts=True),
    ],
)
```

### Integrations that require explicit registration

```python
import sentry_sdk
from sentry_sdk.integrations.litellm import LiteLLMIntegration

sentry_sdk.init(
    dsn="...",
    traces_sample_rate=1.0,
    send_default_pii=True,
    integrations=[
        LiteLLMIntegration(include_prompts=True),   # 100+ providers via proxy
    ],
)
```

### Usage examples

```python
from openai import OpenAI
import sentry_sdk

client = OpenAI()

with sentry_sdk.start_transaction(name="AI inference", op="ai-inference"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Say hello"}],
    )
```

```python
import anthropic, sentry_sdk

client = anthropic.Anthropic()

with sentry_sdk.start_transaction(name="claude-request"):
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Explain async/await"}],
    )
```

## Manual Instrumentation — `gen_ai.*` Spans

Use when the library isn't supported, or for wrapping custom AI logic.

### `gen_ai.request` — Raw LLM call

```python
import sentry_sdk, json

messages = [{"role": "user", "content": "Tell me a joke"}]

with sentry_sdk.start_span(op="gen_ai.request", name="chat gpt-4o") as span:
    span.set_data("gen_ai.request.model", "gpt-4o")
    span.set_data("gen_ai.request.messages", json.dumps(messages))   # must JSON-stringify
    span.set_data("gen_ai.request.temperature", 0.7)
    span.set_data("gen_ai.request.max_tokens", 500)

    result = my_llm_client.chat(model="gpt-4o", messages=messages)

    span.set_data("gen_ai.response.text", json.dumps([result.choices[0].message.content]))
    span.set_data("gen_ai.usage.input_tokens", result.usage.prompt_tokens)
    span.set_data("gen_ai.usage.output_tokens", result.usage.completion_tokens)
    span.set_data("gen_ai.usage.total_tokens", result.usage.total_tokens)
```

### `gen_ai.invoke_agent` — Full agent lifecycle

```python
import sentry_sdk

with sentry_sdk.start_span(op="gen_ai.invoke_agent",
                           name="invoke_agent Weather Agent") as span:
    span.set_data("gen_ai.request.model", "gpt-4o")
    span.set_data("gen_ai.agent.name", "Weather Agent")

    final_output = my_agent.run(task="What's the weather in Paris?")

    span.set_data("gen_ai.response.text", str(final_output))
    span.set_data("gen_ai.usage.input_tokens", my_agent.usage.input_tokens)
    span.set_data("gen_ai.usage.output_tokens", my_agent.usage.output_tokens)
```

### `gen_ai.execute_tool` — Tool/function call

```python
import sentry_sdk, json

with sentry_sdk.start_span(op="gen_ai.execute_tool",
                           name="execute_tool get_weather") as span:
    span.set_data("gen_ai.tool.name", "get_weather")
    span.set_data("gen_ai.tool.type", "function")   # "function"|"extension"|"datastore"
    span.set_data("gen_ai.tool.input", json.dumps({"location": "Paris"}))

    result = get_weather(location="Paris")

    span.set_data("gen_ai.tool.output", json.dumps(result))
```

### `gen_ai.handoff` — Agent-to-agent transition

```python
import sentry_sdk

with sentry_sdk.start_span(op="gen_ai.handoff",
                           name="handoff Billing → Refund Agent") as span:
    span.set_data("gen_ai.agent.name", "Refund Agent")
    result = refund_agent.run(context=billing_context)
```

## Span Attribute Reference

### Common attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `gen_ai.request.model` | string | ✅ | Model identifier (e.g., `gpt-4o`, `claude-opus-4-5`) |
| `gen_ai.operation.name` | string | No | Human-readable operation label |
| `gen_ai.agent.name` | string | No | Agent name (for agent spans) |

### Model config attributes

| Attribute | Type |
|-----------|------|
| `gen_ai.request.temperature` | float |
| `gen_ai.request.max_tokens` | int |
| `gen_ai.request.top_p` | float |
| `gen_ai.request.frequency_penalty` | float |
| `gen_ai.request.presence_penalty` | float |

### Content attributes (PII-gated — only when `send_default_pii=True` + `include_prompts=True`)

| Attribute | Type | Description |
|-----------|------|-------------|
| `gen_ai.request.messages` | string | **JSON-stringified** message array |
| `gen_ai.request.available_tools` | string | **JSON-stringified** tool definitions |
| `gen_ai.response.text` | string | **JSON-stringified** response array |
| `gen_ai.response.tool_calls` | string | **JSON-stringified** tool call array |

> ⚠️ Span attributes only accept primitives — arrays/objects must be JSON-stringified before calling `span.set_data()`.

### Token usage attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `gen_ai.usage.input_tokens` | int | Total input tokens (including cached) |
| `gen_ai.usage.input_tokens.cached` | int | Subset served from cache |
| `gen_ai.usage.input_tokens.cache_write` | int | Tokens written to cache (Anthropic) |
| `gen_ai.usage.output_tokens` | int | Total output tokens (including reasoning) |
| `gen_ai.usage.output_tokens.reasoning` | int | Subset for chain-of-thought reasoning |
| `gen_ai.usage.total_tokens` | int | Sum of input + output |

> ⚠️ Cached and reasoning tokens are **subsets** of totals, not additive. Incorrect reporting produces wrong cost calculations in the dashboard.

## Agent Workflow Hierarchy

```
Transaction
└── gen_ai.invoke_agent  "Weather Agent"
    ├── gen_ai.request   "chat gpt-4o"
    ├── gen_ai.execute_tool "get_weather"
    ├── gen_ai.request   "chat gpt-4o"        ← follow-up
    └── gen_ai.handoff   "→ Report Writer"
        └── gen_ai.invoke_agent "Report Writer"
            ├── gen_ai.request  "chat gpt-4o"
            └── gen_ai.execute_tool "format_report"
```

This populates the **AI Agents Dashboard** in Sentry with per-agent latency, tool call rates, token consumption, and model cost attribution.

### Conversation tracking (Alpha)

> Requires SDK ≥ 2.51.0

```python
import sentry_sdk

# Link spans across turns in a multi-turn conversation
sentry_sdk.ai.set_conversation_id("user-session-abc123")
# All subsequent AI spans carry gen_ai.conversation.id = "user-session-abc123"
```

## Streaming

| Integration | Streaming | Token counts in streams |
|-------------|-----------|------------------------|
| OpenAI | ✅ | Requires `tiktoken>=0.3.0`; set `tiktoken_encoding_name` |
| Anthropic | ✅ | Automatic |
| LangChain | ✅ | Tracked |
| LiteLLM | ✅ | Tracked |
| Manual `gen_ai.*` | ✅ | Set token counts after stream completes |

## Unsupported Providers

| Provider | Workaround |
|----------|-----------|
| Cohere | Use `LiteLLMIntegration` or manual `gen_ai.*` spans |
| AWS Bedrock | Manual instrumentation |
| Mistral | `LiteLLMIntegration` |
| Groq | `LiteLLMIntegration` |
| Vertex AI | `GoogleGenAIIntegration` or `LiteLLMIntegration` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No AI spans appearing | Verify `traces_sample_rate > 0`; wrap calls in a transaction |
| Prompts not captured | Set `send_default_pii=True` and verify `include_prompts=True` (default) |
| LiteLLM not tracked | LiteLLM is NOT auto-enabled — add `LiteLLMIntegration` to `integrations=[]` explicitly |
| Token counts missing for OpenAI streaming | Install `tiktoken>=0.3.0` and set `tiktoken_encoding_name` |
| AI Agents Dashboard empty | Wrap agent runs in `gen_ai.invoke_agent` spans |
| Wrong cost calculations | Ensure cached/reasoning token counts are subsets of totals, not additions |

---

## Reference: Crons

# Crons — Sentry Python SDK

> Minimum SDK: `sentry-sdk` 1.x+ (stable); 1.44.1+ for async `@monitor`; 1.45.0+ for `MonitorConfig` upsert

## Overview

Sentry Crons monitors scheduled jobs by receiving check-ins at job start, success, and failure. Three approaches:

| Approach | Use when |
|----------|---------|
| `@monitor` decorator | Simple wrapping of any function |
| `capture_checkin()` manually | Need control over timing, status, or heartbeats |
| `CeleryIntegration(monitor_beat_tasks=True)` | Celery Beat tasks — zero boilerplate |

## Code Examples

### `@monitor` decorator (simplest)

```python
import sentry_sdk
from sentry_sdk.crons import monitor

@monitor(monitor_slug="nightly-report")
def generate_report():
    # Sends IN_PROGRESS on start, OK on success, ERROR on exception
    run_report()

# Async support (SDK 1.44.1+)
@monitor(monitor_slug="async-job")
async def async_task():
    await do_async_work()

# Context manager syntax
def generate_report():
    with monitor(monitor_slug="nightly-report"):
        run_report()
```

### `@monitor` with `MonitorConfig` — upsert monitor definition (SDK 1.45.0+)

```python
from sentry_sdk.crons import monitor

# Crontab schedule
@monitor(
    monitor_slug="nightly-report",
    monitor_config={
        "schedule": {"type": "crontab", "value": "0 2 * * *"},
        "timezone": "Europe/Vienna",
        "checkin_margin": 10,       # minutes late before MISSED alert
        "max_runtime": 30,          # minutes before TIMEOUT alert
        "failure_issue_threshold": 3,
        "recovery_threshold": 3,
    },
)
def nightly_report():
    generate_report()

# Interval schedule
@monitor(
    monitor_slug="sync-job",
    monitor_config={
        "schedule": {
            "type": "interval",
            "value": 2,
            "unit": "hour",   # minute | hour | day | week | month | year
        },
        "checkin_margin": 5,
        "max_runtime": 20,
    },
)
def sync_data():
    sync()
```

### Manual check-ins with `capture_checkin()`

```python
from sentry_sdk.crons import capture_checkin
from sentry_sdk.crons.consts import MonitorStatus

# 1. Signal job started
check_in_id = capture_checkin(
    monitor_slug="my-cron-job",
    status=MonitorStatus.IN_PROGRESS,
)

try:
    run_job()

    # 2a. Signal success
    capture_checkin(
        monitor_slug="my-cron-job",
        check_in_id=check_in_id,    # links back to IN_PROGRESS
        status=MonitorStatus.OK,
    )
except Exception:
    # 2b. Signal failure
    capture_checkin(
        monitor_slug="my-cron-job",
        check_in_id=check_in_id,
        status=MonitorStatus.ERROR,
    )
    raise
```

### Heartbeat pattern for long-running jobs

```python
from sentry_sdk.crons import capture_checkin
from sentry_sdk.crons.consts import MonitorStatus
import time

def long_running_job():
    check_in_id = capture_checkin(
        monitor_slug="data-pipeline",
        status=MonitorStatus.IN_PROGRESS,
    )

    for batch in get_batches():
        process_batch(batch)
        # Send periodic heartbeat to prevent TIMEOUT
        capture_checkin(
            monitor_slug="data-pipeline",
            check_in_id=check_in_id,
            status=MonitorStatus.IN_PROGRESS,
        )

    capture_checkin(
        monitor_slug="data-pipeline",
        check_in_id=check_in_id,
        status=MonitorStatus.OK,
    )
```

### Celery Beat auto-discovery

```python
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn="...",
    integrations=[
        CeleryIntegration(
            monitor_beat_tasks=True,        # enables auto-discovery
            exclude_beat_tasks=[
                "some-noisy-task",          # exact match
                "health-check-.*",          # regex pattern
            ],
        ),
    ],
)

# In celery config — monitor slug = beat schedule entry name
from celery.schedules import crontab

app.conf.beat_schedule = {
    "nightly-cleanup": {                    # → monitor slug: "nightly-cleanup"
        "task": "tasks.cleanup_old_records",
        "schedule": crontab(hour="1", minute="0"),
    },
}
```

Celery Beat constraints:

| Rule | Detail |
|------|--------|
| Auto-parses | `crontab` schedules only |
| First-run creation | Monitor created lazily on first task execution |
| No double-decoration | Don't use `@monitor` on tasks with `monitor_beat_tasks=True` |
| Default | `monitor_beat_tasks=False` — must be explicitly enabled |

## `MonitorStatus` Reference

```python
from sentry_sdk.crons.consts import MonitorStatus

MonitorStatus.IN_PROGRESS   # job has started
MonitorStatus.OK            # job completed successfully
MonitorStatus.ERROR         # job failed
# MISSED and TIMEOUT are generated server-side — not sent by SDK
```

## `MonitorConfig` Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schedule` | `dict` | ✅ | `{"type": "crontab", "value": "* * * * *"}` or `{"type": "interval", "value": N, "unit": "..."}` |
| `timezone` | `str` | No | IANA timezone name, default `"UTC"` |
| `checkin_margin` | `int` | No | Minutes late before MISSED alert |
| `max_runtime` | `int` | No | Minutes after IN_PROGRESS before TIMEOUT |
| `failure_issue_threshold` | `int` | No | Consecutive failures before opening an issue |
| `recovery_threshold` | `int` | No | Consecutive successes to resolve an issue |

## Best Practices

- Use `@monitor` with `monitor_config` so monitors are created automatically on first run — no Sentry UI setup needed
- For Celery Beat, prefer `monitor_beat_tasks=True` over decorating individual tasks
- Send `IN_PROGRESS` before starting work so TIMEOUT detection starts immediately
- For jobs longer than `max_runtime`, send periodic `IN_PROGRESS` check-ins as heartbeats
- Sentry enforces a rate limit of **6 check-ins/minute per monitor-environment** — excess are dropped silently

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Monitor not created in Sentry | Provide `monitor_config` — monitors are not auto-created without it (unless Celery Beat) |
| MISSED alerts firing too early | Increase `checkin_margin` to allow for job startup time |
| TIMEOUT alerts on slow jobs | Increase `max_runtime` or send periodic `IN_PROGRESS` heartbeats |
| Duplicate check-ins for Celery tasks | Remove `@monitor` decorator from tasks that use `monitor_beat_tasks=True` |
| Async `@monitor` not working | Upgrade SDK to ≥ 1.44.1 |

---

## Reference: Error Monitoring

# Error Monitoring — Sentry Python SDK

> Minimum SDK: `sentry-sdk` 1.x+ (2.x for `new_scope()`, `get_isolation_scope()`)

## Configuration

Key `sentry_sdk.init()` options for error monitoring:

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `dsn` | `str` | env `SENTRY_DSN` | Data Source Name; SDK disabled if empty |
| `environment` | `str` | `"production"` | Deployment environment tag |
| `release` | `str` | env `SENTRY_RELEASE` | App version string |
| `sample_rate` | `float` | `1.0` | Fraction of error events to send (0.0–1.0) |
| `send_default_pii` | `bool` | `False` | Include IPs, cookies, sessions |
| `attach_stacktrace` | `bool` | `False` | Add stack traces to `capture_message()` |
| `max_breadcrumbs` | `int` | `100` | Max breadcrumbs per event |
| `ignore_errors` | `list` | `[]` | Exception types to never report |
| `before_send` | `callable` | `None` | Mutate or drop error events before sending |
| `before_breadcrumb` | `callable` | `None` | Mutate or drop breadcrumbs |
| `event_scrubber` | `EventScrubber` | `None` | Denylist-based PII scrubber |
| `include_local_variables` | `bool` | `True` | Capture stack-frame local variable values |
| `max_request_body_size` | `str` | `"medium"` | `"never"` / `"small"` / `"medium"` / `"always"` |

## Code Examples

### Basic setup

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    environment="production",
    release="my-app@1.0.0",
    sample_rate=1.0,
    send_default_pii=False,
    max_breadcrumbs=100,
)
```

### Capturing exceptions and messages

```python
import sentry_sdk

# Capture current exception (inside except block — reads sys.exc_info())
try:
    risky_operation()
except Exception:
    sentry_sdk.capture_exception()

# Capture explicit exception object
try:
    risky_operation()
except Exception as e:
    sentry_sdk.capture_exception(e)
    raise  # re-raise after capturing

# Capture a plain message
sentry_sdk.capture_message("Payment webhook received unexpected payload")
sentry_sdk.capture_message("Rate limit approaching", level="warning")

# Capture a fully manual event
sentry_sdk.capture_event({
    "message": "Billing failure",
    "level": "error",
    "tags": {"payment.method": "stripe"},
    "fingerprint": ["billing-charge-failure"],
})
```

### Automatic capture by framework

Framework integrations are **auto-enabled** when installed — no `integrations=[...]` needed for most:

```python
# Django — unhandled view exceptions auto-captured
import sentry_sdk
sentry_sdk.init(dsn="...")   # DjangoIntegration auto-enabled

# Flask — unhandled route exceptions auto-captured
from flask import Flask
import sentry_sdk
sentry_sdk.init(dsn="...")   # FlaskIntegration auto-enabled
app = Flask(__name__)

# FastAPI — unhandled endpoint exceptions auto-captured
import sentry_sdk
sentry_sdk.init(dsn="...")   # StarletteIntegration + FastApiIntegration auto-enabled

# Celery — task exceptions auto-captured
import sentry_sdk
sentry_sdk.init(dsn="...")   # CeleryIntegration auto-enabled
```

### Scope management (SDK 2.x)

Three scope layers merge when sending events:

| Scope | Lifetime | Use for |
|-------|----------|---------|
| **Global** | Process lifetime | App-wide tags, server metadata |
| **Isolation** | One request / task | Per-request user, tags |
| **Current** | One span | Per-span metadata |

```python
import sentry_sdk

# Per-request user (isolation scope — fresh per HTTP request with web integrations)
scope = sentry_sdk.get_isolation_scope()
scope.set_user({"id": "user_42", "email": "alice@example.com"})
scope.set_tag("request.id", "req_abc123")

# Temporary forked scope — changes don't leak out
with sentry_sdk.new_scope() as scope:
    scope.set_tag("payment.retry_attempt", "3")
    scope.set_context("charge", {"amount": 9900, "currency": "USD"})
    scope.fingerprint = ["payment-processing-error"]
    sentry_sdk.capture_exception(some_error)
# ← scope reverts here
```

### Context enrichment

```python
import sentry_sdk

# Tags — indexed and searchable; max key 32 chars, value 200 chars
sentry_sdk.set_tag("page.locale", "de-at")
sentry_sdk.set_tags({"feature.flag": "new_checkout_v2", "plan": "enterprise"})

# User identity
sentry_sdk.set_user({
    "id": "user_42",
    "username": "alice_wonder",
    "email": "alice@example.com",
    "ip_address": "{{auto}}",    # Sentry infers from connection
})
sentry_sdk.set_user(None)        # clear user (e.g., on logout)

# Structured context objects (not searchable, visible in event detail)
sentry_sdk.set_context("payment", {
    "provider": "stripe",
    "amount": 9900,
    "currency": "USD",
})

# Breadcrumbs
sentry_sdk.add_breadcrumb(
    type="http",
    category="auth",
    message="User authenticated via OAuth2",
    level="info",
    data={"provider": "google"},
)
```

### `before_send` hook — filtering and scrubbing

```python
import sentry_sdk

def before_send(event, hint):
    exc_info = hint.get("exc_info")

    # Drop non-actionable exceptions
    if exc_info and issubclass(exc_info[0], (KeyboardInterrupt, SystemExit)):
        return None

    # Scrub sensitive HTTP headers
    headers = event.get("request", {}).get("headers", {})
    for h in ("Authorization", "Cookie", "X-Api-Key"):
        if h in headers:
            headers[h] = "[Filtered]"

    # Scrub local variables
    for exc in event.get("exception", {}).get("values", []):
        for frame in exc.get("stacktrace", {}).get("frames", []):
            for key in ("password", "token", "secret"):
                frame.get("vars", {}).pop(key, None)

    # Custom fingerprinting
    if exc_info and isinstance(exc_info[1], TimeoutError):
        event["fingerprint"] = ["network-timeout"]

    return event

sentry_sdk.init(dsn="...", before_send=before_send)
```

### Fingerprinting (custom grouping)

```python
import sentry_sdk

# Static fingerprint via scope
with sentry_sdk.new_scope() as scope:
    scope.fingerprint = ["database-connection-failure"]
    sentry_sdk.capture_exception(db_error)

# Extend default grouping
with sentry_sdk.new_scope() as scope:
    scope.fingerprint = ["{{ default }}", "stripe-payment-failure"]
    sentry_sdk.capture_exception(payment_error)

# Dynamic fingerprint in before_send
def before_send(event, hint):
    exc_info = hint.get("exc_info")
    if exc_info and hasattr(exc_info[1], "status_code"):
        code = exc_info[1].status_code
        if code >= 500:
            event["fingerprint"] = ["http-server-error", str(code)]
    return event
```

### PII scrubbing with EventScrubber

```python
import sentry_sdk
from sentry_sdk.scrubber import EventScrubber, DEFAULT_DENYLIST

sentry_sdk.init(
    dsn="...",
    send_default_pii=False,
    event_scrubber=EventScrubber(
        denylist=DEFAULT_DENYLIST + ["stripe_key", "internal_secret", "ssn"],
        recursive=True,   # deep-scan nested dicts (has performance cost)
    ),
)
```

### Exception Groups (Python 3.11+)

```python
import sentry_sdk

# ExceptionGroup sub-exceptions appear as linked entries in Sentry UI
try:
    raise ExceptionGroup(
        "Batch job failures",
        [ValueError("Bad record #1"), KeyError("Missing field in record #5")],
    )
except* ValueError as eg:
    sentry_sdk.capture_exception(eg)
except* KeyError as eg:
    sentry_sdk.capture_exception(eg)
```

### Advanced: Framework middleware pattern

```python
import sentry_sdk
from flask import Flask

app = Flask(__name__)
sentry_sdk.init(dsn="...")

@app.before_request
def set_sentry_user():
    scope = sentry_sdk.get_isolation_scope()
    user = get_current_user()
    if user:
        scope.set_user({"id": str(user.id), "username": user.username})
        scope.set_tag("user.plan", user.plan)
```

## Best Practices

- Set `send_default_pii=False` (default) — add explicit PII scrubbing via `before_send` or `EventScrubber`
- Use `get_isolation_scope()` for per-request data; use `new_scope()` for temporary isolated context
- Avoid `set_extra()` (deprecated) — use `set_context()` for structured data
- Prefer `set_tag()` for data you want to filter on; `set_context()` for detail-only data
- Use `ignore_errors=[...]` for exceptions you never want reported (e.g., `KeyboardInterrupt`)
- Set `in_app_include=["my_package"]` to correctly mark your frames as in-app in tracebacks

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Events not appearing in Sentry | Verify DSN, check `debug=True` output, ensure `sentry_sdk.init()` is called before app startup |
| User/tag data missing from events | Set scope data before the exception occurs; check isolation vs current scope |
| PII appearing in events | Set `send_default_pii=False` and add `EventScrubber` with your denylist |
| `capture_exception()` is a no-op | Must be called inside an `except` block or pass the exception explicitly |
| Breadcrumbs missing | Check `max_breadcrumbs` setting and `before_breadcrumb` hook |
| `push_scope()` / `configure_scope()` errors | Migrate to `new_scope()` / `get_isolation_scope()` (SDK 2.x) |

---

## Reference: Logging

# Logging — Sentry Python SDK

> Minimum SDK: `sentry-sdk` 2.35.0+ for structured Sentry Logs (`enable_logs=True`)

## Two Logging Systems

| System | Produces | Requires |
|--------|----------|---------|
| **Sentry Structured Logs** | Searchable log records in Sentry Logs UI | `enable_logs=True` + `sentry_sdk.logger.*` |
| **LoggingIntegration (classic)** | Breadcrumbs and/or error events from stdlib `logging` | Auto-enabled by default |

These run simultaneously. They are **not** mutually exclusive.

## Configuration

```python
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    enable_logs=True,                    # required for structured Sentry Logs
    integrations=[
        LoggingIntegration(
            sentry_logs_level=logging.INFO,   # stdlib records → Sentry Logs (requires enable_logs=True)
            level=logging.INFO,               # stdlib records → breadcrumbs
            event_level=logging.ERROR,        # stdlib records → Sentry error events
        ),
    ],
)
```

### `LoggingIntegration` parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| `sentry_logs_level` | `INFO` | Records ≥ level → **structured Sentry Logs** (needs `enable_logs=True`) |
| `level` | `INFO` | Records ≥ level → **breadcrumbs** (attached to next error event) |
| `event_level` | `ERROR` | Records ≥ level → standalone **Sentry error events** |

## Code Examples

### Sentry Structured Logs — direct API

```python
import sentry_sdk
from sentry_sdk import logger as sentry_logger

sentry_sdk.init(dsn="...", enable_logs=True)

sentry_logger.trace("Starting database connection {database}", database="users")
sentry_logger.debug("Cache miss for user {user_id}", user_id=123)
sentry_logger.info("Updated global cache")
sentry_logger.warning("Rate limit reached for endpoint {endpoint}", endpoint="/api/results/")
sentry_logger.error(
    "Failed to process payment. Order: {order_id}. Amount: {amount}",
    order_id="or_2342",
    amount=99.99,
)
sentry_logger.fatal("Database {database} connection pool exhausted", database="users")
```

Template `{attribute_name}` placeholders become **individually searchable attributes** in the Sentry Logs UI.

### Extra structured attributes

```python
from sentry_sdk import logger as sentry_logger

sentry_logger.error(
    "Payment processing failed",
    attributes={
        "payment.provider": "stripe",
        "payment.method": "credit_card",
        "payment.currency": "USD",
        "user.subscription_tier": "premium",
    },
)
```

### stdlib `logging` → Sentry Logs

```python
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_sdk.init(
    dsn="...",
    enable_logs=True,
    integrations=[LoggingIntegration(sentry_logs_level=logging.INFO)],
)

logger = logging.getLogger(__name__)
logger.info("User signed in", extra={"user_id": 42, "region": "eu-west-1"})
# extra fields become searchable attributes on the log entry
```

### Loguru integration

```python
import sentry_sdk
from loguru import logger

# LoguruIntegration auto-activates when loguru is installed
sentry_sdk.init(dsn="...", enable_logs=True)

logger.info("Application started")
logger.error("Critical failure in payment module")
```

Manual configuration for full control:

```python
import sentry_sdk
from sentry_sdk.integrations.loguru import LoguruIntegration, LoggingLevels

sentry_sdk.init(
    dsn="...",
    enable_logs=True,
    integrations=[
        LoguruIntegration(
            sentry_logs_level=LoggingLevels.INFO.value,    # → structured logs
            level=LoggingLevels.INFO.value,                # → breadcrumbs
            event_level=LoggingLevels.ERROR.value,         # → error events
        )
    ],
)
```

### `before_send_log` hook — filter and modify

```python
import sentry_sdk
from typing import Optional

def before_log(log, hint) -> Optional[dict]:
    # Drop all INFO logs
    if log["severity_text"] == "info":
        return None
    # Add custom attribute
    log["attributes"]["processed_by"] = "before_log"
    return log

sentry_sdk.init(dsn="...", enable_logs=True, before_send_log=before_log)
```

### `Log` object schema

| Key | Type | Description |
|-----|------|-------------|
| `severity_text` | `str` | `"trace"` / `"debug"` / `"info"` / `"warning"` / `"error"` / `"fatal"` |
| `severity_number` | `int` | 1–24 (OpenTelemetry spec) |
| `body` | `str` | Rendered message string |
| `attributes` | `dict` | Custom key-value pairs |
| `time_unix_nano` | `int` | Unix epoch in nanoseconds |
| `trace_id` | `str \| None` | Associated trace ID |

### Suppress noisy loggers

```python
from sentry_sdk.integrations.logging import ignore_logger

ignore_logger("a.spammy.logger")
ignore_logger("boto3.*")   # glob patterns supported
```

## Decision Table

| Goal | Tool |
|------|------|
| Searchable structured records in Sentry Logs UI | `sentry_sdk.logger.*` + `enable_logs=True` |
| Bridge existing stdlib `logging` to Sentry Logs | `LoggingIntegration(sentry_logs_level=...)` + `enable_logs=True` |
| Bridge loguru to Sentry Logs | `LoguruIntegration(sentry_logs_level=...)` + `enable_logs=True` |
| Breadcrumbs for error context | `LoggingIntegration(level=logging.INFO)` (default) |
| Auto-create error events from log calls | `LoggingIntegration(event_level=logging.ERROR)` (default) |
| Drop/modify a log before sending | `before_send_log` callback |

## Automatically Added Attributes

Every log record receives these automatically:

| Attribute | Source |
|-----------|--------|
| `sentry.environment` | `init(environment=...)` |
| `sentry.release` | `init(release=...)` |
| `sentry.sdk.name` / `sentry.sdk.version` | SDK metadata |
| `server.address` | hostname |
| `sentry.message.template` | Original template string |
| `sentry.message.parameter.*` | Template placeholder values |
| `user.id`, `user.name`, `user.email` | Active scope user (if set) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `sentry_sdk.logger.*` calls have no effect | Ensure `enable_logs=True` is set in `sentry_sdk.init()` |
| stdlib logs not appearing as Sentry Logs | Set `sentry_logs_level` in `LoggingIntegration` and `enable_logs=True` |
| Logger's own level filters out records | SDK respects the logger's configured level — set it to `logging.INFO` or lower |
| Too many log records hitting quota | Use `before_send_log` to filter by severity or attribute |
| Loguru not auto-activating | Verify `loguru` is installed; or add `LoguruIntegration()` explicitly |

---

## Reference: Metrics

# Metrics — Sentry Python SDK

> Minimum SDK: `sentry-sdk` 2.44.0+ · Status: ⚠️ Open beta

## Overview

`sentry_sdk.metrics` provides custom counters, gauges, and distributions. Metrics are enabled by default — no extra `init()` flag needed.

## Metric Types

| Type | API | Use for |
|------|-----|---------|
| Counter | `metrics.count()` | Event occurrences, request counts |
| Distribution | `metrics.distribution()` | Latencies, sizes — supports p50/p90/p95/p99 |
| Gauge | `metrics.gauge()` | Current values (min, max, avg, sum, count — no percentiles) |

## Configuration

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    # No extra flag — metrics are on by default
)
```

Optional `before_send_metric` hook:

```python
from typing import Optional

def before_metric(metric, hint) -> Optional[dict]:
    if metric["name"] == "noisy-metric":
        return None                          # drop this metric
    metric["attributes"]["env"] = "prod"    # add attribute
    return metric

sentry_sdk.init(dsn="...", before_send_metric=before_metric)
```

## Code Examples

### Counter — event occurrences

```python
import sentry_sdk

sentry_sdk.metrics.count(
    "button_click",
    1,
    attributes={
        "browser": "Firefox",
        "page": "/checkout",
    },
)

# Increment by more than 1
sentry_sdk.metrics.count("api.request", 5, attributes={"endpoint": "/v2/users"})
```

### Distribution — percentile analysis

Best for latencies, response sizes, durations where p50/p90/p99 matter:

```python
import time
import sentry_sdk

start = time.time()
process_order(order)
duration_ms = (time.time() - start) * 1000

sentry_sdk.metrics.distribution(
    "order.processing_time",
    duration_ms,
    unit="millisecond",
    attributes={"order.type": "subscription", "region": "eu"},
)
```

### Gauge — space-efficient aggregates

Use when high cardinality is a concern; no percentile support:

```python
import sentry_sdk

sentry_sdk.metrics.gauge(
    "queue.depth",
    len(pending_jobs),
    unit="none",
    attributes={"queue": "billing"},
)
```

### All four attribute value types

```python
sentry_sdk.metrics.count(
    "api.request",
    1,
    attributes={
        "endpoint": "/v2/users",     # str
        "method": "POST",
        "success": True,             # bool
        "status_code": 201,          # int
        "latency": 0.042,            # float
    },
)
```

### Unit strings

| Category | Values |
|----------|--------|
| Time | `"nanosecond"`, `"microsecond"`, `"millisecond"`, `"second"`, `"minute"`, `"hour"`, `"day"`, `"week"` |
| Data | `"bit"`, `"byte"`, `"kilobyte"`, `"megabyte"`, `"gigabyte"`, `"terabyte"` |
| Fractions | `"ratio"`, `"percent"` |
| Dimensionless | `"none"` (default when omitted) |

### `before_send_metric` — `Metric` schema

| Key | Type | Description |
|-----|------|-------------|
| `name` | `str` | Metric identifier |
| `type` | `str` | `"counter"` / `"gauge"` / `"distribution"` |
| `value` | `float` | Numeric measurement |
| `unit` | `str \| None` | Unit string |
| `attributes` | `dict` | Custom key-value pairs |
| `timestamp` | `float` | Epoch seconds |
| `trace_id` | `str \| None` | Associated trace ID |
| `span_id` | `str \| None` | Active span ID |

## Best Practices

- Keep attribute cardinality low — avoid user IDs, UUIDs, or timestamps as attribute values
- Use `distribution` over `gauge` when you need percentile analysis
- Prefix metric names with your service name: `"payments.charge_time"` not `"charge_time"`
- Use standard unit strings — Sentry renders them in the UI with proper labels
- Metrics are buffered and flushed periodically — avoid using them for critical alerting requiring sub-second latency

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Metrics not appearing | Verify SDK version ≥ 2.44.0; check `debug=True` output |
| Metric dropped silently | Check `before_send_metric` hook; verify metric name contains no special characters |
| High cardinality warning | Reduce attribute values — avoid per-user or per-request identifiers |
| No percentiles in Sentry UI | Switch from `gauge` to `distribution` — gauges do not support percentiles |

---

## Reference: Profiling

# Profiling — Sentry Python SDK

> Minimum SDK: `sentry-sdk` 1.18.0+ (transaction-based); 2.24.1+ (continuous / session-based)

## Configuration

| Option | API | Min SDK | Purpose |
|--------|-----|---------|---------|
| `profiles_sample_rate` | Transaction-based (legacy) | 1.18.0 | Fraction of transactions to profile; relative to `traces_sample_rate` |
| `profile_session_sample_rate` | Continuous (new) | 2.24.1 | Fraction of sessions to profile; evaluated once per process start |
| `profile_lifecycle` | Continuous (new) | 2.24.1 | `"trace"` = SDK auto-manages; `"manual"` = explicit start/stop |

Profiling requires `traces_sample_rate > 0` (or `traces_sampler`) to be set.

## API Comparison

| | `profiles_sample_rate` (transaction-based) | `profile_session_sample_rate` (continuous) |
|--|---------------------------------------------|---------------------------------------------|
| **Min SDK** | 1.18.0 | 2.24.1 |
| **Evaluated** | Per transaction | Once per process/deployment start |
| **Max duration** | 30 seconds per transaction | Unlimited |
| **Requires** | `traces_sample_rate` | `profile_lifecycle` + `traces_sample_rate` |
| **Use when** | Simple setup, short-lived transactions | Long-running apps, background services |

## Code Examples

### Transaction-based profiling (simple / legacy)

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,   # relative to traces_sample_rate
    # e.g. profiles_sample_rate=0.5 → profiles 50% of sampled transactions
)
```

Profiles start when the transaction starts and stop when it ends or after **30 seconds**, whichever is first.

### Continuous profiling — auto-managed (`profile_lifecycle="trace"`)

SDK automatically starts and stops the profiler around active spans.

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,   # evaluated once at process start
    profile_lifecycle="trace",          # SDK manages start/stop automatically
)
```

### Continuous profiling — manual control (`profile_lifecycle="manual"`)

Full programmatic control over profiler lifetime.

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    traces_sample_rate=1.0,
    profile_session_sample_rate=1.0,
    profile_lifecycle="manual",
)

# Application startup
sentry_sdk.profiler.start_profiler()

# ... application runs ...

# Application shutdown
sentry_sdk.profiler.stop_profiler()
```

### Production-recommended setup (continuous)

```python
import sentry_sdk
import signal

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    environment="production",
    release="my-app@2.0.0",
    traces_sample_rate=0.1,             # sample 10% of transactions
    profile_session_sample_rate=1.0,    # profile all sampled sessions
    profile_lifecycle="trace",
)
```

## Best Practices

- Use continuous profiling (`profile_session_sample_rate` + `profile_lifecycle`) for long-running services and production workloads
- Use transaction-based (`profiles_sample_rate`) for simple setups or short-lived scripts
- `profile_session_sample_rate` is evaluated **once at process start** — changing it requires a restart
- `"trace"` and `"manual"` profile lifecycles are mutually exclusive; do not mix them
- Reduce `traces_sample_rate` in production (e.g., `0.1`) — profiling overhead is low but not zero
- Python's GIL means the profiler captures the thread holding the GIL; async I/O wait time appears as near-zero CPU — this is expected

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No profiles appearing | Verify `traces_sample_rate > 0` and profiling options are set correctly |
| Profiles cut off at 30s | Switch to continuous profiling (`profile_session_sample_rate`) |
| `profile_session_sample_rate` has no effect | Check SDK version is ≥ 2.24.1; ensure `profile_lifecycle` is also set |
| Profiler not stopping | In `"manual"` mode, call `sentry_sdk.profiler.stop_profiler()` on shutdown |
| Async functions show no CPU time | Expected — Python profiler only captures GIL-holding time, not async I/O wait |

---

## Reference: Tracing

# Tracing — Sentry Python SDK

> Minimum SDK: `sentry-sdk` 0.11.2+ for basic tracing; 2.x for `update_current_span()` and enhanced `@trace`

## Configuration

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `traces_sample_rate` | `float` | `None` | Fraction of transactions to trace (0.0–1.0); `None` disables tracing |
| `traces_sampler` | `callable` | `None` | Per-transaction sampling function; overrides `traces_sample_rate` |
| `trace_propagation_targets` | `list` | all origins | URLs to inject `sentry-trace` / `baggage` headers into |
| `functions_to_trace` | `list` | `[]` | Fully-qualified function names to auto-wrap with spans |
| `instrumenter` | `str` | `"sentry"` | Set to `"otel"` to use OpenTelemetry bridge |

## Code Examples

### Enable tracing

```python
import sentry_sdk

sentry_sdk.init(
    dsn="https://<key>@<org>.ingest.sentry.io/<project>",
    traces_sample_rate=1.0,   # 1.0 = 100% of transactions; reduce in production
)
```

### Custom spans with context manager

```python
import sentry_sdk

# Top-level transaction
with sentry_sdk.start_transaction(op="task", name="Process Order"):
    with sentry_sdk.start_span(name="Validate Items") as span:
        span.set_data("item_count", len(items))
        validate(items)

    with sentry_sdk.start_span(name="Charge Card"):
        charge_card(order)
```

### `@sentry_sdk.trace` decorator

```python
import sentry_sdk

# Simple decorator — uses function name as span name
@sentry_sdk.trace
def process_payment(order_id: str):
    ...

# With custom op, name, and attributes (SDK 2.35.0+)
@sentry_sdk.trace(op="payment", name="Charge Customer", attributes={"version": 2})
def charge_customer(amount: int):
    ...

# Static / class methods — decorator order matters!
class PaymentService:
    @staticmethod
    @sentry_sdk.trace          # MUST come AFTER @staticmethod
    def process():
        ...

    @classmethod
    @sentry_sdk.trace          # MUST come AFTER @classmethod
    def batch_process(cls):
        ...
```

### Adding data to spans

```python
import sentry_sdk

with sentry_sdk.start_span(name="db-query") as span:
    span.set_data("db.system", "postgresql")
    span.set_data("db.table", "orders")
    span.set_data("row_count", 42)
    span.set_data("cache_hit", False)
    # Only primitive types: str, int, float, bool, or homogeneous lists
```

### Accessing the active span/transaction

```python
import sentry_sdk

# Get active span
span = sentry_sdk.get_current_span()
if span:
    span.set_data("key", "value")

# Get active transaction
txn = sentry_sdk.get_current_scope().transaction
if txn:
    txn.set_tag("order.type", "subscription")

# Update active span in-place (SDK 2.x)
sentry_sdk.update_current_span(
    op="http.client",
    name="POST /api/charge",
    attributes={"http.status_code": 200},
)
```

### Auto-trace multiple functions without decorators

```python
import sentry_sdk

sentry_sdk.init(
    dsn="...",
    traces_sample_rate=1.0,
    functions_to_trace=[
        {"qualified_name": "myapp.billing.processor.charge_card"},
        {"qualified_name": "myapp.billing.processor.BillingService.validate"},
    ],
)
# No changes to the functions themselves required
```

### Dynamic sampling with `traces_sampler`

```python
import sentry_sdk

def traces_sampler(sampling_context):
    # Honour parent's sampling decision in distributed traces
    parent = sampling_context.get("parent_sampled")
    if parent is not None:
        return float(parent)

    op = sampling_context["transaction_context"].get("op", "")

    if op == "http.server":
        name = sampling_context["transaction_context"].get("name", "")
        if name in ("/health", "/ping", "/readyz"):
            return 0          # drop health checks
        return 0.5            # sample 50% of HTTP requests
    elif op == "task":
        return 0.1            # sample 10% of background tasks
    else:
        return 0.01           # default 1%

sentry_sdk.init(dsn="...", traces_sampler=traces_sampler)
```

### Auto-instrumented frameworks

| Framework | Auto-enabled | What is traced |
|-----------|-------------|----------------|
| Django | ✅ | Requests, DB queries (ORM), cache, signals |
| Flask | ✅ | Requests, Jinja2 rendering |
| FastAPI / Starlette | ✅ | Requests, background tasks |
| Celery | ✅ | Task execution, queue operations |
| SQLAlchemy | ✅ | All queries as spans + breadcrumbs |
| Redis | ✅ | All commands as spans + breadcrumbs |
| PyMongo | ✅ | All queries (covers mongoengine, Motor) |
| requests / httpx | ✅ | Outbound HTTP calls with trace propagation |

### Database auto-instrumentation

```python
import sentry_sdk
from sentry_sdk.integrations.redis import RedisIntegration

# SQLAlchemy — auto-enabled, no config needed
sentry_sdk.init(dsn="...", traces_sample_rate=1.0)
# All queries appear as spans automatically

# Redis — with optional cache monitoring
sentry_sdk.init(
    dsn="...",
    traces_sample_rate=1.0,
    send_default_pii=True,       # enables full command data in spans
    integrations=[
        RedisIntegration(
            max_data_size=1024,                         # truncate large values
            cache_prefixes=["mycache:", "template."],   # appears in cache dashboard
        ),
    ],
)
```

### Distributed tracing

Frameworks propagate `sentry-trace` and `baggage` headers automatically. For manual HTTP calls:

```python
import sentry_sdk

# Outgoing: inject headers into arbitrary request
headers = {}
headers["sentry-trace"] = sentry_sdk.get_traceparent()
headers["baggage"] = sentry_sdk.get_baggage()
make_request(url="https://internal-api.example.com", headers=headers)

# Incoming: continue a trace from arbitrary headers
incoming_headers = get_headers_from_request()
transaction = sentry_sdk.continue_trace(incoming_headers)  # does NOT start it
with sentry_sdk.start_transaction(transaction):
    handle_request()

# Browser: inject into HTML meta tags for JS frontend pickup
meta = f'<meta name="sentry-trace" content="{sentry_sdk.get_traceparent()}">'
meta += f'<meta name="baggage" content="{sentry_sdk.get_baggage()}">'
```

### Limit propagation targets

```python
import sentry_sdk, re

sentry_sdk.init(
    dsn="...",
    traces_sample_rate=1.0,
    trace_propagation_targets=[
        "localhost",
        "https://api.myservice.com",
        re.compile(r"^https://internal\."),
    ],
    # Set to [] to disable outgoing propagation entirely
)
```

### OpenTelemetry bridge

```python
# pip install "sentry-sdk[opentelemetry]"
import sentry_sdk
from opentelemetry import trace
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.trace import TracerProvider
from sentry_sdk.integrations.opentelemetry import SentrySpanProcessor, SentryPropagator

sentry_sdk.init(
    dsn="...",
    traces_sample_rate=1.0,
    instrumenter="otel",      # disables built-in Sentry auto-instrumentation
)

provider = TracerProvider()
provider.add_span_processor(SentrySpanProcessor())
trace.set_tracer_provider(provider)
set_global_textmap(SentryPropagator())

# Use OTel API as normal — spans appear in Sentry
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("my-operation"):
    do_work()
```

## Best Practices

- Use `traces_sampler` instead of `traces_sample_rate` for production — it lets you drop health checks, adjust by route, and honour distributed trace decisions
- Always finish spans — unfinished spans are silently dropped
- Use `span.set_data()` not `span.set_tag()` for span-level data (tags are for scope-level filtering)
- Set `trace_propagation_targets` to avoid leaking `sentry-trace` headers to third-party services
- Add `sentry-trace` and `baggage` to your CORS allowlist when tracing browser-to-backend flows

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transactions appearing | Verify `traces_sample_rate > 0` or `traces_sampler` returns non-zero |
| Spans not linked to transaction | Ensure spans are created inside an active `start_transaction()` context |
| Distributed traces broken | Check that `sentry-trace` and `baggage` headers pass through proxies/gateways |
| `description=` deprecation warning | Replace `description=` with `name=` in `start_span()` calls |
| OTel spans not appearing | Ensure `SentrySpanProcessor` is added to `TracerProvider` before creating spans |
| `@sentry_sdk.trace` on static method fails | Put `@sentry_sdk.trace` AFTER `@staticmethod` / `@classmethod` |
