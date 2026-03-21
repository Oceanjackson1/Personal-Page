---
title: "Dbos Python"
description: "DBOS Python SDK for building reliable, fault-tolerant applications with durable workflows. Use this skill when writing Python code with DBOS, creating workflows and steps, using queues, using DBOSC..."
category: "writing"
source: "community"
author: "Community"
tags: ["dbos", "python"]
date: 2026-03-20
---

# DBOS Python Best Practices

Guide for building reliable, fault-tolerant Python applications with DBOS durable workflows.

## When to Use

Reference these guidelines when:
- Adding DBOS to existing Python code
- Creating workflows and steps
- Using queues for concurrency control
- Implementing workflow communication (events, messages, streams)
- Configuring and launching DBOS applications
- Using DBOSClient from external applications
- Testing DBOS applications

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Lifecycle | CRITICAL | `lifecycle-` |
| 2 | Workflow | CRITICAL | `workflow-` |
| 3 | Step | HIGH | `step-` |
| 4 | Queue | HIGH | `queue-` |
| 5 | Communication | MEDIUM | `comm-` |
| 6 | Pattern | MEDIUM | `pattern-` |
| 7 | Testing | LOW-MEDIUM | `test-` |
| 8 | Client | MEDIUM | `client-` |
| 9 | Advanced | LOW | `advanced-` |

## Critical Rules

### DBOS Configuration and Launch

A DBOS application MUST configure and launch DBOS inside its main function:

```python
import os
from dbos import DBOS, DBOSConfig

@DBOS.workflow()
def my_workflow():
    pass

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
```

### Workflow and Step Structure

Workflows are comprised of steps. Any function performing complex operations or accessing external services must be a step:

```python
@DBOS.step()
def call_external_api():
    return requests.get("https://api.example.com").json()

@DBOS.workflow()
def my_workflow():
    result = call_external_api()
    return result
```

### Key Constraints

- Do NOT call `DBOS.start_workflow` or `DBOS.recv` from a step
- Do NOT use threads to start workflows - use `DBOS.start_workflow` or queues
- Workflows MUST be deterministic - non-deterministic operations go in steps
- Do NOT create/update global variables from workflows or steps

## How to Use

Read individual rule files for detailed explanations and examples:

```
references/lifecycle-config.md
references/workflow-determinism.md
references/queue-concurrency.md
```

## References

- https://docs.dbos.dev/
- https://github.com/dbos-inc/dbos-transact-py

---

## Reference: _Sections

# Section Definitions

This file defines the rule categories for DBOS Python best practices. Rules are automatically assigned to sections based on their filename prefix.

---

## 1. Lifecycle (lifecycle)
**Impact:** CRITICAL
**Description:** DBOS configuration, initialization, and launch patterns. Foundation for all DBOS applications.

## 2. Workflow (workflow)
**Impact:** CRITICAL
**Description:** Workflow creation, determinism requirements, background execution, and workflow IDs.

## 3. Step (step)
**Impact:** HIGH
**Description:** Step creation, retries, transactions, and when to use steps vs workflows.

## 4. Queue (queue)
**Impact:** HIGH
**Description:** Queue creation, concurrency limits, rate limiting, partitioning, and priority.

## 5. Communication (comm)
**Impact:** MEDIUM
**Description:** Workflow events, messages, and streaming for inter-workflow communication.

## 6. Pattern (pattern)
**Impact:** MEDIUM
**Description:** Common patterns including idempotency, scheduled workflows, debouncing, and classes.

## 7. Testing (test)
**Impact:** LOW-MEDIUM
**Description:** Testing DBOS applications with pytest, fixtures, and best practices.

## 8. Client (client)
**Impact:** MEDIUM
**Description:** DBOSClient for interacting with DBOS from external applications.

## 9. Advanced (advanced)
**Impact:** LOW
**Description:** Async workflows, workflow versioning, patching, and code upgrades.

---

## Reference: Advanced Async

## Use Async Workflows Correctly

Coroutine (async) functions can be DBOS workflows. Use async-specific methods and patterns.

**Incorrect (mixing sync and async):**

```python
@DBOS.workflow()
async def async_workflow():
    # Don't use sync sleep in async workflow!
    DBOS.sleep(10)

    # Don't use sync start_workflow for async workflows
    handle = DBOS.start_workflow(other_async_workflow)
```

**Correct (async patterns):**

```python
import asyncio
import aiohttp

@DBOS.step()
async def fetch_async():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://example.com") as response:
            return await response.text()

@DBOS.workflow()
async def async_workflow():
    # Use async sleep
    await DBOS.sleep_async(10)

    # Await async steps
    result = await fetch_async()

    # Use async start_workflow
    handle = await DBOS.start_workflow_async(other_async_workflow)

    return result
```

### Running Async Steps In Parallel

You can run async steps in parallel if they are started in **deterministic order**:

**Correct (deterministic start order):**

```python
@DBOS.workflow()
async def parallel_workflow():
    # Start steps in deterministic order, then await together
    tasks = [
        asyncio.create_task(step1("arg1")),
        asyncio.create_task(step2("arg2")),
        asyncio.create_task(step3("arg3")),
    ]
    # Use return_exceptions=True for proper error handling
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

**Incorrect (non-deterministic order):**

```python
@DBOS.workflow()
async def bad_parallel_workflow():
    async def seq_a():
        await step1("arg1")
        await step2("arg2")  # Order depends on step1 timing

    async def seq_b():
        await step3("arg3")
        await step4("arg4")  # Order depends on step3 timing

    # step2 and step4 may run in either order - non-deterministic!
    await asyncio.gather(seq_a(), seq_b())
```

If you need concurrent sequences, use child workflows instead of interleaving steps.

For transactions in async workflows, use `asyncio.to_thread`:

```python
@DBOS.transaction()
def sync_transaction(data):
    DBOS.sql_session.execute(...)

@DBOS.workflow()
async def async_workflow():
    result = await asyncio.to_thread(sync_transaction, data)
```

Reference: [Async Workflows](https://docs.dbos.dev/python/tutorials/workflow-tutorial#coroutine-async-workflows)

---

## Reference: Advanced Patching

## Use Patching for Safe Workflow Upgrades

Use `DBOS.patch()` to safely deploy breaking workflow changes. Breaking changes alter what steps run or their order.

**Incorrect (breaking change without patch):**

```python
# Original
@DBOS.workflow()
def workflow():
    foo()
    bar()

# Updated - breaks in-progress workflows!
@DBOS.workflow()
def workflow():
    baz()  # Replaced foo() - checkpoints don't match
    bar()
```

**Correct (using patch):**

```python
# Enable patching in config
config: DBOSConfig = {
    "name": "my-app",
    "enable_patching": True,
}
DBOS(config=config)

@DBOS.workflow()
def workflow():
    if DBOS.patch("use-baz"):
        baz()  # New workflows use baz
    else:
        foo()  # Old workflows continue with foo
    bar()
```

Deprecating patches after all old workflows complete:

```python
# Step 1: Deprecate (runs all workflows, stops inserting marker)
@DBOS.workflow()
def workflow():
    DBOS.deprecate_patch("use-baz")
    baz()
    bar()

# Step 2: Remove entirely (after all deprecated workflows complete)
@DBOS.workflow()
def workflow():
    baz()
    bar()
```

`DBOS.patch(name)` returns:
- `True` for new workflows (started after patch deployed)
- `False` for old workflows (started before patch deployed)

Reference: [Patching](https://docs.dbos.dev/python/tutorials/upgrading-workflows#patching)

---

## Reference: Advanced Versioning

## Use Versioning for Blue-Green Deployments

DBOS versions workflows to prevent unsafe recovery. Use blue-green deployments to safely upgrade.

**Incorrect (deploying breaking changes without versioning):**

```python
# Deploying new code directly kills in-progress workflows
# because their checkpoints don't match the new code

# Old code
@DBOS.workflow()
def workflow():
    step_a()
    step_b()

# New code replaces old immediately - breaks recovery!
@DBOS.workflow()
def workflow():
    step_a()
    step_c()  # Changed step - old workflows can't recover
```

**Correct (using versioning with blue-green deployment):**

```python
# Set explicit version in config
config: DBOSConfig = {
    "name": "my-app",
    "application_version": "2.0.0",  # New version
}
DBOS(config=config)

# Deploy new version alongside old version
# New traffic goes to v2.0.0, old workflows drain on v1.0.0

# Check for remaining old workflows before retiring v1.0.0
old_workflows = DBOS.list_workflows(
    app_version="1.0.0",
    status=["PENDING", "ENQUEUED"]
)

if len(old_workflows) == 0:
    # Safe to retire old version
    pass
```

Fork a workflow to run on a new version:

```python
# Fork workflow from step 5 on version 2.0.0
new_handle = DBOS.fork_workflow(
    workflow_id="old-workflow-id",
    start_step=5,
    application_version="2.0.0"
)
```

Reference: [Versioning](https://docs.dbos.dev/python/tutorials/upgrading-workflows#versioning)

---

## Reference: Client Enqueue

## Enqueue Workflows from External Applications

Use `client.enqueue()` to submit workflows from outside the DBOS application. Must specify workflow and queue names explicitly.

**Incorrect (missing required options):**

```python
from dbos import DBOSClient

client = DBOSClient(system_database_url=db_url)

# Missing workflow_name and queue_name!
handle = client.enqueue({}, task_data)
```

**Correct (with required options):**

```python
from dbos import DBOSClient, EnqueueOptions

client = DBOSClient(system_database_url=db_url)

options: EnqueueOptions = {
    "workflow_name": "process_task",  # Required
    "queue_name": "task_queue",       # Required
}
handle = client.enqueue(options, task_data)
result = handle.get_result()
client.destroy()
```

With optional parameters:

```python
options: EnqueueOptions = {
    "workflow_name": "process_task",
    "queue_name": "task_queue",
    "workflow_id": "custom-id-123",
    "workflow_timeout": 300,
    "deduplication_id": "user-123",
    "priority": 1,
}
```

Limitation: Cannot enqueue workflows that are methods on Python classes.

Reference: [DBOSClient.enqueue](https://docs.dbos.dev/python/reference/client#enqueue)

---

## Reference: Client Setup

## Initialize DBOSClient for External Access

Use `DBOSClient` to interact with DBOS from external applications (API servers, CLI tools, etc.).

**Incorrect (no cleanup):**

```python
from dbos import DBOSClient

client = DBOSClient(system_database_url=db_url)
handle = client.enqueue(options, data)
# Connection leaked - no destroy()!
```

**Correct (with cleanup):**

```python
import os
from dbos import DBOSClient

client = DBOSClient(
    system_database_url=os.environ["DBOS_SYSTEM_DATABASE_URL"]
)

try:
    handle = client.enqueue(options, data)
    result = handle.get_result()
finally:
    client.destroy()
```

Constructor parameters:
- `system_database_url`: Connection string to DBOS system database
- `serializer`: Must match the DBOS application's serializer (default: pickle)

## API Reference

Beyond `enqueue`, DBOSClient mirrors the DBOS API. Use the same patterns from other reference files:

| DBOSClient method | Same as DBOS method |
|-------------------|---------------------|
| `client.send()` | `DBOS.send()` - add `idempotency_key` for exactly-once |
| `client.get_event()` | `DBOS.get_event()` |
| `client.read_stream()` | `DBOS.read_stream()` |
| `client.list_workflows()` | `DBOS.list_workflows()` |
| `client.cancel_workflow()` | `DBOS.cancel_workflow()` |
| `client.resume_workflow()` | `DBOS.resume_workflow()` |
| `client.retrieve_workflow()` | `DBOS.retrieve_workflow()` |

Reference: [DBOSClient](https://docs.dbos.dev/python/reference/client)

---

## Reference: Comm Events

## Use Events for Workflow Status Publishing

Workflows can publish key-value events that clients can read. Events are persisted and useful for status updates.

**Incorrect (no way to monitor progress):**

```python
@DBOS.workflow()
def long_workflow():
    step_one()
    step_two()  # Client can't see progress
    step_three()
    return "done"
```

**Correct (publishing events):**

```python
@DBOS.workflow()
def long_workflow():
    DBOS.set_event("status", "starting")

    step_one()
    DBOS.set_event("status", "step_one_complete")

    step_two()
    DBOS.set_event("status", "step_two_complete")

    step_three()
    DBOS.set_event("status", "finished")
    return "done"

# Client code to read events
@app.post("/start")
def start_workflow():
    handle = DBOS.start_workflow(long_workflow)
    return {"workflow_id": handle.get_workflow_id()}

@app.get("/status/{workflow_id}")
def get_status(workflow_id: str):
    status = DBOS.get_event(workflow_id, "status", timeout_seconds=0) or "not started"
    return {"status": status}
```

Get all events from a workflow:

```python
all_events = DBOS.get_all_events(workflow_id)
# Returns: {"status": "finished", "other_key": "value"}
```

Events can be called from `set_event` from workflows or steps.

Reference: [Workflow Events](https://docs.dbos.dev/python/tutorials/workflow-communication#workflow-events)

---

## Reference: Comm Messages

## Use Messages for Workflow Notifications

Send messages to workflows to signal or notify them while running. Messages are persisted and queued per topic.

**Incorrect (polling external state):**

```python
@DBOS.workflow()
def payment_workflow():
    # Polling is inefficient and not durable
    while True:
        status = check_payment_status()
        if status == "paid":
            break
        time.sleep(1)
```

**Correct (using messages):**

```python
PAYMENT_STATUS = "payment_status"

@DBOS.workflow()
def payment_workflow():
    # Process order...
    DBOS.set_event("payment_id", payment_id)

    # Wait for payment notification (60 second timeout)
    payment_status = DBOS.recv(PAYMENT_STATUS, timeout_seconds=60)

    if payment_status == "paid":
        fulfill_order()
    else:
        cancel_order()

# Webhook endpoint to receive payment notification
@app.post("/payment_webhook/{workflow_id}/{status}")
def payment_webhook(workflow_id: str, status: str):
    DBOS.send(workflow_id, status, PAYMENT_STATUS)
    return {"ok": True}
```

Key points:
- `DBOS.recv()` can only be called from workflows
- Messages are queued per topic
- `recv()` returns `None` on timeout
- Messages are persisted for exactly-once delivery

Reference: [Workflow Messaging](https://docs.dbos.dev/python/tutorials/workflow-communication#workflow-messaging-and-notifications)

---

## Reference: Comm Streaming

## Use Streams for Real-Time Data

Workflows can stream data in real-time to clients. Useful for LLM responses, progress reporting, or long-running results.

**Incorrect (returning all data at end):**

```python
@DBOS.workflow()
def llm_workflow(prompt):
    # Client waits for entire response
    response = call_llm(prompt)
    return response
```

**Correct (streaming results):**

```python
@DBOS.workflow()
def llm_workflow(prompt):
    for chunk in call_llm_streaming(prompt):
        DBOS.write_stream("response", chunk)
    DBOS.close_stream("response")
    return "complete"

# Client reads stream
@app.get("/stream/{workflow_id}")
def stream_response(workflow_id: str):
    def generate():
        for value in DBOS.read_stream(workflow_id, "response"):
            yield value
    return StreamingResponse(generate())
```

Stream characteristics:
- Streams are immutable and append-only
- Writes from workflows happen exactly-once
- Writes from steps happen at-least-once (may duplicate on retry)
- Streams auto-close when workflow terminates

Close streams explicitly when done:

```python
@DBOS.workflow()
def producer():
    DBOS.write_stream("data", {"step": 1})
    DBOS.write_stream("data", {"step": 2})
    DBOS.close_stream("data")  # Signal completion
```

Reference: [Workflow Streaming](https://docs.dbos.dev/python/tutorials/workflow-communication#workflow-streaming)

---

## Reference: Lifecycle Config

## Configure and Launch DBOS Properly

Every DBOS application must configure and launch DBOS inside the main function.

**Incorrect (configuration at module level):**

```python
from dbos import DBOS, DBOSConfig

# Don't configure at module level!
config: DBOSConfig = {
    "name": "my-app",
}
DBOS(config=config)

@DBOS.workflow()
def my_workflow():
    pass

if __name__ == "__main__":
    DBOS.launch()
    my_workflow()
```

**Correct (configuration in main):**

```python
import os
from dbos import DBOS, DBOSConfig

@DBOS.workflow()
def my_workflow():
    pass

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
    my_workflow()
```

For scheduled-only applications (no HTTP server), block the main thread:

```python
import os
import threading
from dbos import DBOS, DBOSConfig

@DBOS.scheduled("* * * * *")
@DBOS.workflow()
def scheduled_task(scheduled_time, actual_time):
    pass

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
    threading.Event().wait()  # Block forever
```

Reference: [DBOS Configuration](https://docs.dbos.dev/python/reference/configuration)

---

## Reference: Lifecycle Fastapi

## Integrate DBOS with FastAPI

When using DBOS with FastAPI, configure and launch DBOS inside the main function before starting uvicorn.

**Incorrect (configuration at module level):**

```python
from fastapi import FastAPI
from dbos import DBOS, DBOSConfig

app = FastAPI()

# Don't configure at module level!
config: DBOSConfig = {"name": "my-app"}
DBOS(config=config)

@app.get("/")
@DBOS.workflow()
def endpoint():
    return {"status": "ok"}

if __name__ == "__main__":
    DBOS.launch()
    uvicorn.run(app)
```

**Correct (configuration in main):**

```python
import os
from fastapi import FastAPI
from dbos import DBOS, DBOSConfig
import uvicorn

app = FastAPI()

@DBOS.step()
def process_data():
    return "processed"

@app.get("/")
@DBOS.workflow()
def endpoint():
    result = process_data()
    return {"result": result}

if __name__ == "__main__":
    config: DBOSConfig = {
        "name": "my-app",
        "system_database_url": os.environ.get("DBOS_SYSTEM_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.launch()
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

The workflow decorator can be combined with FastAPI route decorators. The FastAPI decorator should come first (outermost).

Reference: [DBOS with FastAPI](https://docs.dbos.dev/python/tutorials/workflow-tutorial)

---

## Reference: Pattern Classes

## Use DBOS Decorators with Classes

DBOS decorators work with class methods. Workflow classes must inherit from `DBOSConfiguredInstance`.

**Incorrect (missing class setup):**

```python
class MyService:
    def __init__(self, url):
        self.url = url

    @DBOS.workflow()  # Won't work without proper setup
    def fetch_data(self):
        return self.fetch()
```

**Correct (proper class setup):**

```python
from dbos import DBOS, DBOSConfiguredInstance

@DBOS.dbos_class()
class URLFetcher(DBOSConfiguredInstance):
    def __init__(self, url: str):
        self.url = url
        # instance_name must be unique and passed to super()
        super().__init__(instance_name=url)

    @DBOS.workflow()
    def fetch_workflow(self):
        return self.fetch_url()

    @DBOS.step()
    def fetch_url(self):
        return requests.get(self.url).text

# Instantiate BEFORE DBOS.launch()
example_fetcher = URLFetcher("https://example.com")
api_fetcher = URLFetcher("https://api.example.com")

if __name__ == "__main__":
    DBOS.launch()
    print(example_fetcher.fetch_workflow())
```

Requirements:
- Class must be decorated with `@DBOS.dbos_class()`
- Class must inherit from `DBOSConfiguredInstance`
- `instance_name` must be unique and passed to `super().__init__()`
- All instances must be created before `DBOS.launch()`

Steps can be added to any class without these requirements.

Reference: [Python Classes](https://docs.dbos.dev/python/tutorials/classes)

---

## Reference: Pattern Debouncing

## Debounce Workflows to Prevent Wasted Work

Debouncing delays workflow execution until some time has passed since the last trigger. Useful for user input processing.

**Incorrect (processing every input):**

```python
@DBOS.workflow()
def process_input(user_input):
    # Expensive processing
    analyze(user_input)

@app.post("/input")
def on_input(user_id: str, input: str):
    # Every keystroke triggers processing!
    DBOS.start_workflow(process_input, input)
```

**Correct (debounced processing):**

```python
from dbos import Debouncer

@DBOS.workflow()
def process_input(user_input):
    analyze(user_input)

# Create a debouncer for the workflow
debouncer = Debouncer.create(process_input)

@app.post("/input")
def on_input(user_id: str, input: str):
    # Wait 5 seconds after last input before processing
    debounce_key = user_id  # Debounce per user
    debounce_period = 5.0   # Seconds
    handle = debouncer.debounce(debounce_key, debounce_period, input)
    return {"workflow_id": handle.get_workflow_id()}
```

Debouncer with timeout (max wait time):

```python
# Process after 5s idle OR 60s max wait
debouncer = Debouncer.create(process_input, debounce_timeout_sec=60)

def on_input(user_id: str, input: str):
    debouncer.debounce(user_id, 5.0, input)
```

When workflow executes, it uses the **last** inputs passed to `debounce`.

Reference: [Debouncing Workflows](https://docs.dbos.dev/python/tutorials/workflow-tutorial#debouncing-workflows)

---

## Reference: Pattern Idempotency

## Use Workflow IDs for Idempotency

Set workflow IDs to make operations idempotent. A workflow with the same ID executes only once.

**Incorrect (duplicate payments possible):**

```python
@app.post("/pay/{order_id}")
def process_payment(order_id: str):
    # Multiple clicks = multiple payments!
    handle = DBOS.start_workflow(payment_workflow, order_id)
    return handle.get_result()
```

**Correct (idempotent with workflow ID):**

```python
from dbos import SetWorkflowID

@app.post("/pay/{order_id}")
def process_payment(order_id: str):
    # Same order_id = same workflow ID = only one execution
    with SetWorkflowID(f"payment-{order_id}"):
        handle = DBOS.start_workflow(payment_workflow, order_id)
    return handle.get_result()

@DBOS.workflow()
def payment_workflow(order_id: str):
    charge_customer(order_id)
    send_confirmation(order_id)
    return "success"
```

Access the workflow ID inside workflows:

```python
@DBOS.workflow()
def my_workflow():
    current_id = DBOS.workflow_id
    DBOS.logger.info(f"Running workflow {current_id}")
```

Workflow IDs must be globally unique. Duplicate IDs return the existing workflow's result without re-executing.

Reference: [Workflow IDs and Idempotency](https://docs.dbos.dev/python/tutorials/workflow-tutorial#workflow-ids-and-idempotency)

---

## Reference: Pattern Scheduled

## Create Scheduled Workflows

Use `@DBOS.scheduled` to run workflows on a schedule. Workflows run exactly once per interval.

**Incorrect (manual scheduling):**

```python
# Don't use external cron or manual timers
import schedule
schedule.every(1).minute.do(my_task)
```

**Correct (DBOS scheduled workflow):**

```python
@DBOS.scheduled("* * * * *")  # Every minute
@DBOS.workflow()
def run_every_minute(scheduled_time, actual_time):
    print(f"Running at {scheduled_time}")
    do_maintenance_task()

@DBOS.scheduled("0 */6 * * *")  # Every 6 hours
@DBOS.workflow()
def periodic_cleanup(scheduled_time, actual_time):
    cleanup_old_records()
```

Scheduled workflow requirements:
- Must have `@DBOS.scheduled` decorator with crontab syntax
- Must accept two arguments: `scheduled_time` and `actual_time` (both `datetime`)
- Main thread must stay alive for scheduled workflows

For apps with only scheduled workflows (no HTTP server):

```python
import threading

if __name__ == "__main__":
    DBOS.launch()
    threading.Event().wait()  # Block forever
```

Crontab format: `minute hour day month weekday`
- `* * * * *` = every minute
- `0 * * * *` = every hour
- `0 0 * * *` = daily at midnight
- `0 0 * * 0` = weekly on Sunday

Reference: [Scheduled Workflows](https://docs.dbos.dev/python/tutorials/scheduled-workflows)

---

## Reference: Pattern Sleep

## Use Durable Sleep for Delayed Execution

Use `DBOS.sleep()` for durable delays that survive restarts. The wakeup time is persisted in the database.

**Incorrect (regular sleep):**

```python
import time

@DBOS.workflow()
def delayed_task(delay_seconds, task):
    # Regular sleep is lost on restart!
    time.sleep(delay_seconds)
    run_task(task)
```

**Correct (durable sleep):**

```python
@DBOS.workflow()
def delayed_task(delay_seconds, task):
    # Durable sleep - survives restarts
    DBOS.sleep(delay_seconds)
    run_task(task)
```

Use cases for durable sleep:
- Schedule a task for the future
- Wait between retries
- Implement delays spanning hours, days, or weeks

Example: Schedule a reminder:

```python
@DBOS.workflow()
def send_reminder(user_id: str, message: str, delay_days: int):
    # Sleep for days - survives any restart
    DBOS.sleep(delay_days * 24 * 60 * 60)
    send_notification(user_id, message)
```

For async workflows, use `DBOS.sleep_async()`:

```python
@DBOS.workflow()
async def async_delayed_task():
    await DBOS.sleep_async(60)
    await run_async_task()
```

Reference: [Durable Sleep](https://docs.dbos.dev/python/tutorials/workflow-tutorial#durable-sleep)

---

## Reference: Queue Basics

## Use Queues for Concurrent Workflows

Queues run many workflows concurrently with managed flow control. Use them when you need to control how many workflows run at once.

**Incorrect (uncontrolled concurrency):**

```python
@DBOS.workflow()
def process_task(task):
    pass

# Starting many workflows without control
for task in tasks:
    DBOS.start_workflow(process_task, task)  # Could overwhelm resources
```

**Correct (using queue):**

```python
from dbos import Queue

queue = Queue("task_queue")

@DBOS.workflow()
def process_task(task):
    pass

@DBOS.workflow()
def process_all_tasks(tasks):
    handles = []
    for task in tasks:
        # Queue manages concurrency
        handle = queue.enqueue(process_task, task)
        handles.append(handle)
    # Wait for all tasks
    return [h.get_result() for h in handles]
```

Queues process workflows in FIFO order. You can enqueue both workflows and steps.

```python
queue = Queue("example_queue")

@DBOS.step()
def my_step(data):
    return process(data)

# Enqueue a step
handle = queue.enqueue(my_step, data)
result = handle.get_result()
```

Reference: [DBOS Queues](https://docs.dbos.dev/python/tutorials/queue-tutorial)

---

## Reference: Queue Concurrency

## Control Queue Concurrency

Queues support worker-level and global concurrency limits to prevent resource exhaustion.

**Incorrect (no concurrency control):**

```python
queue = Queue("heavy_tasks")  # No limits - could exhaust memory

@DBOS.workflow()
def memory_intensive_task(data):
    # Uses lots of memory
    pass
```

**Correct (worker concurrency):**

```python
# Each process runs at most 5 tasks from this queue
queue = Queue("heavy_tasks", worker_concurrency=5)

@DBOS.workflow()
def memory_intensive_task(data):
    pass
```

**Correct (global concurrency):**

```python
# At most 10 tasks run across ALL processes
queue = Queue("limited_tasks", concurrency=10)
```

**In-order processing (sequential):**

```python
# Only one task at a time - guarantees order
queue = Queue("sequential_queue", concurrency=1)

@DBOS.step()
def process_event(event):
    pass

def handle_event(event):
    queue.enqueue(process_event, event)
```

Worker concurrency is recommended for most use cases. Global concurrency should be used carefully as pending workflows count toward the limit.

Reference: [Managing Concurrency](https://docs.dbos.dev/python/tutorials/queue-tutorial#managing-concurrency)

---

## Reference: Queue Deduplication

## Deduplicate Queued Workflows

Use deduplication IDs to ensure only one workflow with a given ID is active in a queue at a time.

**Incorrect (duplicate workflows possible):**

```python
queue = Queue("user_tasks")

@app.post("/process/{user_id}")
def process_for_user(user_id: str):
    # Multiple requests = multiple workflows for same user!
    queue.enqueue(process_workflow, user_id)
```

**Correct (deduplicated by user):**

```python
from dbos import Queue, SetEnqueueOptions
from dbos import error as dboserror

queue = Queue("user_tasks")

@app.post("/process/{user_id}")
def process_for_user(user_id: str):
    with SetEnqueueOptions(deduplication_id=user_id):
        try:
            handle = queue.enqueue(process_workflow, user_id)
            return {"workflow_id": handle.get_workflow_id()}
        except dboserror.DBOSQueueDeduplicatedError:
            return {"status": "already processing"}
```

Deduplication behavior:
- If a workflow with the same deduplication ID is `ENQUEUED` or `PENDING`, new enqueue raises `DBOSQueueDeduplicatedError`
- Once the workflow completes, a new workflow with the same ID can be enqueued
- Deduplication is per-queue (same ID can exist in different queues)

Use cases:
- One active task per user
- Preventing duplicate job submissions
- Rate limiting by entity

Reference: [Queue Deduplication](https://docs.dbos.dev/python/tutorials/queue-tutorial#deduplication)

---

## Reference: Queue Listening

## Control Which Queues a Worker Listens To

Use `DBOS.listen_queues()` to make a process only handle specific queues. Useful for CPU vs GPU workers.

**Incorrect (all workers handle all queues):**

```python
cpu_queue = Queue("cpu_tasks")
gpu_queue = Queue("gpu_tasks")

# Every worker processes both queues
# GPU tasks may run on CPU-only machines!
if __name__ == "__main__":
    DBOS(config=config)
    DBOS.launch()
```

**Correct (workers listen to specific queues):**

```python
from dbos import DBOS, DBOSConfig, Queue

cpu_queue = Queue("cpu_queue")
gpu_queue = Queue("gpu_queue")

@DBOS.workflow()
def cpu_task(data):
    pass

@DBOS.workflow()
def gpu_task(data):
    pass

if __name__ == "__main__":
    worker_type = os.environ.get("WORKER_TYPE")  # "cpu" or "gpu"
    config: DBOSConfig = {"name": "worker"}
    DBOS(config=config)

    if worker_type == "gpu":
        DBOS.listen_queues([gpu_queue])
    elif worker_type == "cpu":
        DBOS.listen_queues([cpu_queue])

    DBOS.launch()
```

Key points:
- Call `DBOS.listen_queues()` **before** `DBOS.launch()`
- Workers can still **enqueue** to any queue, just won't **dequeue** from others
- By default, workers listen to all declared queues

Use cases:
- CPU vs GPU workers
- Memory-intensive vs lightweight tasks
- Geographic task routing

Reference: [Explicit Queue Listening](https://docs.dbos.dev/python/tutorials/queue-tutorial#explicit-queue-listening)

---

## Reference: Queue Partitioning

## Partition Queues for Per-Entity Limits

Partitioned queues apply flow control limits per partition, not globally. Useful for per-user or per-entity concurrency limits.

**Incorrect (global limit affects all users):**

```python
queue = Queue("user_tasks", concurrency=1)  # Only 1 task total

def handle_user_task(user_id, task):
    # One user blocks all other users!
    queue.enqueue(process_task, task)
```

**Correct (per-user limits with partitioning):**

```python
from dbos import Queue, SetEnqueueOptions

# Partition queue with concurrency=1 per partition
queue = Queue("user_tasks", partition_queue=True, concurrency=1)

@DBOS.workflow()
def process_task(task):
    pass

def handle_user_task(user_id: str, task):
    # Each user gets their own "subqueue" with concurrency=1
    with SetEnqueueOptions(queue_partition_key=user_id):
        queue.enqueue(process_task, task)
```

For both per-partition AND global limits, use two-level queueing:

```python
# Global limit of 5 concurrent tasks
global_queue = Queue("global_queue", concurrency=5)
# Per-user limit of 1 concurrent task
user_queue = Queue("user_queue", partition_queue=True, concurrency=1)

def handle_task(user_id: str, task):
    with SetEnqueueOptions(queue_partition_key=user_id):
        user_queue.enqueue(concurrency_manager, task)

@DBOS.workflow()
def concurrency_manager(task):
    # Enforces global limit
    return global_queue.enqueue(process_task, task).get_result()

@DBOS.workflow()
def process_task(task):
    pass
```

Reference: [Partitioning Queues](https://docs.dbos.dev/python/tutorials/queue-tutorial#partitioning-queues)

---

## Reference: Queue Priority

## Set Queue Priority for Workflows

Use priority to control which workflows run first. Lower numbers = higher priority.

**Incorrect (no priority control):**

```python
queue = Queue("tasks")

# All tasks treated equally - urgent tasks may wait
for task in tasks:
    queue.enqueue(process_task, task)
```

**Correct (with priority):**

```python
from dbos import Queue, SetEnqueueOptions

# Must enable priority on the queue
queue = Queue("tasks", priority_enabled=True)

@DBOS.workflow()
def process_task(task):
    pass

def enqueue_task(task, is_urgent: bool):
    # Priority 1 = highest, runs before priority 10
    priority = 1 if is_urgent else 10
    with SetEnqueueOptions(priority=priority):
        queue.enqueue(process_task, task)
```

Priority behavior:
- Range: 1 to 2,147,483,647 (lower = higher priority)
- Workflows without priority have highest priority (run first)
- Same priority = FIFO order
- Must set `priority_enabled=True` on queue

Example with multiple priority levels:

```python
queue = Queue("jobs", priority_enabled=True)

PRIORITY_CRITICAL = 1
PRIORITY_HIGH = 10
PRIORITY_NORMAL = 100
PRIORITY_LOW = 1000

def enqueue_job(job, level):
    with SetEnqueueOptions(priority=level):
        queue.enqueue(process_job, job)
```

Reference: [Queue Priority](https://docs.dbos.dev/python/tutorials/queue-tutorial#priority)

---

## Reference: Queue Rate Limiting

## Rate Limit Queue Execution

Use rate limits when working with rate-limited APIs (like LLM APIs). Limits are global across all processes.

**Incorrect (no rate limiting):**

```python
queue = Queue("llm_tasks")

@DBOS.step()
def call_llm(prompt):
    # May hit rate limits if too many calls
    return openai.chat.completions.create(...)
```

**Correct (with rate limit):**

```python
# Max 50 tasks started per 30 seconds
queue = Queue("llm_tasks", limiter={"limit": 50, "period": 30})

@DBOS.step()
def call_llm(prompt):
    return openai.chat.completions.create(...)

@DBOS.workflow()
def process_prompts(prompts):
    handles = []
    for prompt in prompts:
        # Queue enforces rate limit
        handle = queue.enqueue(call_llm, prompt)
        handles.append(handle)
    return [h.get_result() for h in handles]
```

Rate limit parameters:
- `limit`: Maximum number of functions to start in the period
- `period`: Time period in seconds

Rate limits can be combined with concurrency limits:

```python
queue = Queue("api_tasks",
    worker_concurrency=5,
    limiter={"limit": 100, "period": 60})
```

Reference: [Rate Limiting](https://docs.dbos.dev/python/tutorials/queue-tutorial#rate-limiting)

---

## Reference: Step Basics

## Use Steps for External Operations

Any function that performs complex operations, accesses external APIs, or has side effects should be a step. Step results are checkpointed, enabling workflow recovery.

**Incorrect (external call in workflow):**

```python
import requests

@DBOS.workflow()
def my_workflow():
    # External API call directly in workflow - not checkpointed!
    response = requests.get("https://api.example.com/data")
    return response.json()
```

**Correct (external call in step):**

```python
import requests

@DBOS.step()
def fetch_data():
    response = requests.get("https://api.example.com/data")
    return response.json()

@DBOS.workflow()
def my_workflow():
    # Step result is checkpointed for recovery
    data = fetch_data()
    return data
```

Step requirements:
- Inputs and outputs must be serializable
- Should not modify global state
- Can be retried on failure (configurable)

When to use steps:
- API calls to external services
- File system operations
- Random number generation
- Getting current time
- Any non-deterministic operation

Reference: [DBOS Steps](https://docs.dbos.dev/python/tutorials/step-tutorial)

---

## Reference: Step Retries

## Configure Step Retries for Transient Failures

Steps can automatically retry on failure with exponential backoff. This handles transient failures like network issues.

**Incorrect (manual retry logic):**

```python
@DBOS.step()
def fetch_data():
    # Manual retry logic is error-prone
    for attempt in range(3):
        try:
            return requests.get("https://api.example.com").json()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
```

**Correct (built-in retries):**

```python
@DBOS.step(retries_allowed=True, max_attempts=10, interval_seconds=1.0, backoff_rate=2.0)
def fetch_data():
    # Retries handled automatically
    return requests.get("https://api.example.com").json()
```

Retry parameters:
- `retries_allowed`: Enable automatic retries (default: False)
- `max_attempts`: Maximum retry attempts (default: 3)
- `interval_seconds`: Initial delay between retries (default: 1.0)
- `backoff_rate`: Multiplier for exponential backoff (default: 2.0)

With defaults, retry delays are: 1s, 2s, 4s, 8s, 16s...

Reference: [Configurable Retries](https://docs.dbos.dev/python/tutorials/step-tutorial#configurable-retries)

---

## Reference: Step Transactions

## Use Transactions for Database Operations

Transactions are a special type of step optimized for database access. They execute as a single database transaction. Only use with Postgres.

**Incorrect (database access in regular step):**

```python
@DBOS.step()
def save_to_db(data):
    # For Postgres, use transactions instead of steps
    # This doesn't get transaction guarantees
    engine.execute("INSERT INTO table VALUES (?)", data)
```

**Correct (using transaction):**

```python
from sqlalchemy import text

@DBOS.transaction()
def save_to_db(name: str, value: str) -> None:
    sql = text("INSERT INTO my_table (name, value) VALUES (:name, :value)")
    DBOS.sql_session.execute(sql, {"name": name, "value": value})

@DBOS.transaction()
def get_from_db(name: str) -> str | None:
    sql = text("SELECT value FROM my_table WHERE name = :name LIMIT 1")
    row = DBOS.sql_session.execute(sql, {"name": name}).first()
    return row[0] if row else None
```

With SQLAlchemy ORM:

```python
from sqlalchemy import Table, Column, String, MetaData, select

greetings = Table("greetings", MetaData(),
    Column("name", String),
    Column("note", String))

@DBOS.transaction()
def insert_greeting(name: str, note: str) -> None:
    DBOS.sql_session.execute(greetings.insert().values(name=name, note=note))
```

Important:
- Only use transactions with Postgres databases
- For other databases, use regular steps
- Never use `async def` with transactions

Reference: [DBOS Transactions](https://docs.dbos.dev/python/reference/decorators#transactions)

---

## Reference: Test Fixtures

## Use Proper Test Fixtures for DBOS

Use pytest fixtures to properly reset DBOS state between tests.

**Incorrect (no reset between tests):**

```python
def test_workflow_one():
    DBOS.launch()
    result = my_workflow()
    assert result == "expected"

def test_workflow_two():
    # DBOS state from previous test!
    result = another_workflow()
```

**Correct (reset fixture):**

```python
import pytest
import os
from dbos import DBOS, DBOSConfig

@pytest.fixture()
def reset_dbos():
    DBOS.destroy()
    config: DBOSConfig = {
        "name": "test-app",
        "database_url": os.environ.get("TESTING_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.reset_system_database()
    DBOS.launch()
    yield
    DBOS.destroy()

def test_workflow_one(reset_dbos):
    result = my_workflow()
    assert result == "expected"

def test_workflow_two(reset_dbos):
    # Clean DBOS state
    result = another_workflow()
    assert result == "other_expected"
```

The fixture:
1. Destroys any existing DBOS instance
2. Creates fresh configuration
3. Resets the system database
4. Launches DBOS
5. Yields for test execution
6. Cleans up after test

Reference: [Testing DBOS](https://docs.dbos.dev/python/tutorials/testing)

---

## Reference: Workflow Background

## Start Workflows in Background

Use `DBOS.start_workflow` to run workflows in the background. This returns a handle to monitor or retrieve results.

**Incorrect (using threads):**

```python
import threading

@DBOS.workflow()
def long_task(data):
    # Long running work
    pass

# Don't use threads for DBOS workflows!
thread = threading.Thread(target=long_task, args=(data,))
thread.start()
```

**Correct (using start_workflow):**

```python
from dbos import DBOS, WorkflowHandle

@DBOS.workflow()
def long_task(data):
    # Long running work
    return "done"

# Start workflow in background
handle: WorkflowHandle = DBOS.start_workflow(long_task, data)

# Later, get the result
result = handle.get_result()

# Or check status
status = handle.get_status()
```

You can retrieve a workflow handle later using its ID:

```python
# Get workflow ID
workflow_id = handle.get_workflow_id()

# Later, retrieve the handle
handle = DBOS.retrieve_workflow(workflow_id)
result = handle.get_result()
```

Reference: [Starting Workflows](https://docs.dbos.dev/python/tutorials/workflow-tutorial#starting-workflows-in-the-background)

---

## Reference: Workflow Constraints

## Follow Workflow Constraints

DBOS workflows and steps have specific constraints that must be followed for correct operation.

**Incorrect (calling start_workflow from step):**

```python
@DBOS.step()
def my_step():
    # Never start workflows from inside a step!
    DBOS.start_workflow(another_workflow)
```

**Incorrect (modifying global state):**

```python
results = []  # Global variable

@DBOS.workflow()
def my_workflow():
    # Don't modify globals from workflows!
    results.append("done")
```

**Incorrect (using recv outside workflow):**

```python
@DBOS.step()
def my_step():
    # recv can only be called from workflows!
    msg = DBOS.recv("topic")
```

**Correct (following constraints):**

```python
@DBOS.workflow()
def parent_workflow():
    result = my_step()
    # Start child workflow from workflow, not step
    handle = DBOS.start_workflow(child_workflow, result)
    # Use recv from workflow
    msg = DBOS.recv("topic")
    return handle.get_result()

@DBOS.step()
def my_step():
    # Steps just do their work and return
    return process_data()

@DBOS.workflow()
def child_workflow(data):
    return transform(data)
```

Key constraints:
- Do NOT call `DBOS.start_workflow` from a step
- Do NOT call `DBOS.recv` from a step
- Do NOT call `DBOS.set_event` from outside a workflow
- Do NOT modify global variables from workflows or steps
- Do NOT use threads to start workflows

Reference: [DBOS Workflows](https://docs.dbos.dev/python/tutorials/workflow-tutorial)

---

## Reference: Workflow Control

## Cancel, Resume, and Fork Workflows

Use these methods to control workflow execution: stop runaway workflows, retry failed ones, or restart from a specific step.

**Incorrect (expecting immediate cancellation):**

```python
DBOS.cancel_workflow(workflow_id)
# Wrong: assuming the workflow stopped immediately
cleanup_resources()  # May race with workflow still running its current step
```

**Correct (wait for cancellation to complete):**

```python
DBOS.cancel_workflow(workflow_id)
# Cancellation happens at the START of the next step
# Wait for workflow to actually stop
handle = DBOS.retrieve_workflow(workflow_id)
status = handle.get_status()
while status.status == "PENDING":
    time.sleep(0.5)
    status = handle.get_status()
# Now safe to clean up
cleanup_resources()
```

### Cancel

Stop a workflow and remove it from its queue:

```python
DBOS.cancel_workflow(workflow_id)  # Cancels workflow and all children
```

### Resume

Restart a stopped workflow from its last completed step:

```python
# Resume a cancelled or failed workflow
handle = DBOS.resume_workflow(workflow_id)
result = handle.get_result()

# Can also bypass queue for an enqueued workflow
handle = DBOS.resume_workflow(enqueued_workflow_id)
```

### Fork

Start a new workflow from a specific step of an existing one:

```python
# Get steps to find the right starting point
steps = DBOS.list_workflow_steps(workflow_id)
for step in steps:
    print(f"Step {step['function_id']}: {step['function_name']}")

# Fork from step 3 (skips steps 1-2, uses their saved results)
new_handle = DBOS.fork_workflow(workflow_id, start_step=3)

# Fork to run on a new application version (useful for patching bugs)
new_handle = DBOS.fork_workflow(
    workflow_id,
    start_step=3,
    application_version="2.0.0"
)
```

Reference: [Workflow Management](https://docs.dbos.dev/python/tutorials/workflow-management)

---

## Reference: Workflow Determinism

## Keep Workflows Deterministic

Workflow functions must be deterministic: given the same inputs and step return values, they must invoke the same steps in the same order. Non-deterministic operations must be moved to steps.

**Incorrect (non-deterministic workflow):**

```python
import random

@DBOS.workflow()
def example_workflow():
    # Random number in workflow breaks recovery!
    choice = random.randint(0, 1)
    if choice == 0:
        step_one()
    else:
        step_two()
```

**Correct (non-determinism in step):**

```python
import random

@DBOS.step()
def generate_choice():
    return random.randint(0, 1)

@DBOS.workflow()
def example_workflow():
    # Random number generated in step - result is saved
    choice = generate_choice()
    if choice == 0:
        step_one()
    else:
        step_two()
```

Non-deterministic operations that must be in steps:
- Random number generation
- Getting current time
- Accessing external APIs
- Reading files
- Database queries (use transactions or steps)

Reference: [Workflow Determinism](https://docs.dbos.dev/python/tutorials/workflow-tutorial#determinism)

---

## Reference: Workflow Introspection

## List and Inspect Workflows

Use `DBOS.list_workflows()` to query workflows by status, name, queue, or other criteria.

**Incorrect (loading unnecessary data):**

```python
# Loading inputs/outputs when not needed is slow
workflows = DBOS.list_workflows(status="PENDING")
for w in workflows:
    print(w.workflow_id)  # Only using ID
```

**Correct (optimize with load flags):**

```python
# Disable loading inputs/outputs for better performance
workflows = DBOS.list_workflows(
    status="PENDING",
    load_input=False,
    load_output=False
)
for w in workflows:
    print(f"{w.workflow_id}: {w.status}")
```

Common queries:

```python
# Find failed workflows
failed = DBOS.list_workflows(status="ERROR", limit=100)

# Find workflows by name
processing = DBOS.list_workflows(
    name="process_task",
    status=["PENDING", "ENQUEUED"]
)

# Find workflows on a specific queue
queued = DBOS.list_workflows(queue_name="high_priority")

# Only queued workflows (shortcut)
queued = DBOS.list_queued_workflows(queue_name="task_queue")

# Find old version workflows for blue-green deploys
old = DBOS.list_workflows(
    app_version="1.0.0",
    status=["PENDING", "ENQUEUED"]
)

# Get workflow steps
steps = DBOS.list_workflow_steps(workflow_id)
for step in steps:
    print(f"Step {step['function_id']}: {step['function_name']}")
```

WorkflowStatus fields: `workflow_id`, `status`, `name`, `queue_name`, `created_at`, `input`, `output`, `error`

Status values: `ENQUEUED`, `PENDING`, `SUCCESS`, `ERROR`, `CANCELLED`, `MAX_RECOVERY_ATTEMPTS_EXCEEDED`

Reference: [Workflow Management](https://docs.dbos.dev/python/tutorials/workflow-management)

---

## Reference: Workflow Timeout

## Set Workflow Timeouts

Use `SetWorkflowTimeout` to limit workflow execution time. Timed-out workflows are cancelled.

**Incorrect (no timeout):**

```python
@DBOS.workflow()
def potentially_long_workflow():
    # Could run forever!
    while not done:
        process_next()
```

**Correct (with timeout):**

```python
from dbos import SetWorkflowTimeout

@DBOS.workflow()
def bounded_workflow():
    while not done:
        process_next()

# Workflow must complete within 60 seconds
with SetWorkflowTimeout(60):
    bounded_workflow()

# Or with start_workflow
with SetWorkflowTimeout(60):
    handle = DBOS.start_workflow(bounded_workflow)
```

Timeout behavior:
- Timeout is **start-to-completion** (doesn't count queue wait time)
- Timeouts are **durable** (persist across restarts)
- Cancellation happens at the **beginning of the next step**
- **All child workflows** are also cancelled

With queues:

```python
queue = Queue("example_queue")

# Timeout starts when dequeued, not when enqueued
with SetWorkflowTimeout(30):
    queue.enqueue(my_workflow)
```

Timeouts work with long durations (hours, days, weeks) since they're stored in the database.

Reference: [Workflow Timeouts](https://docs.dbos.dev/python/tutorials/workflow-tutorial#workflow-timeouts)
