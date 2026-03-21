---
title: "Dbos Typescript"
description: "DBOS TypeScript SDK for building reliable, fault-tolerant applications with durable workflows. Use this skill when writing TypeScript code with DBOS, creating workflows and steps, using queues, usi..."
category: "writing"
source: "community"
author: "Community"
tags: ["dbos", "typescript"]
date: 2026-03-20
---

# DBOS TypeScript Best Practices

Guide for building reliable, fault-tolerant TypeScript applications with DBOS durable workflows.

## When to Use

Reference these guidelines when:
- Adding DBOS to existing TypeScript code
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

### Installation

Always install the latest version of DBOS:

```bash
npm install @dbos-inc/dbos-sdk@latest
```

### DBOS Configuration and Launch

A DBOS application MUST configure and launch DBOS before running any workflows:

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function main() {
  DBOS.setConfig({
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  });
  await DBOS.launch();
  await myWorkflow();
}

main().catch(console.log);
```

### Workflow and Step Structure

Workflows are comprised of steps. Any function performing complex operations or accessing external services must be run as a step using `DBOS.runStep`:

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function fetchData() {
  return await fetch("https://api.example.com").then(r => r.json());
}

async function myWorkflowFn() {
  const result = await DBOS.runStep(fetchData, { name: "fetchData" });
  return result;
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

### Key Constraints

- Do NOT call, start, or enqueue workflows from within steps
- Do NOT use threads or uncontrolled concurrency to start workflows - use `DBOS.startWorkflow` or queues
- Workflows MUST be deterministic - non-deterministic operations go in steps
- Do NOT modify global variables from workflows or steps

## How to Use

Read individual rule files for detailed explanations and examples:

```
references/lifecycle-config.md
references/workflow-determinism.md
references/queue-concurrency.md
```

## References

- https://docs.dbos.dev/
- https://github.com/dbos-inc/dbos-transact-ts

---

## Reference: _Sections

# Section Definitions

This file defines the rule categories for DBOS TypeScript best practices. Rules are automatically assigned to sections based on their filename prefix.

---

## 1. Lifecycle (lifecycle)
**Impact:** CRITICAL
**Description:** DBOS configuration, initialization, and launch patterns. Foundation for all DBOS applications.

## 2. Workflow (workflow)
**Impact:** CRITICAL
**Description:** Workflow creation, determinism requirements, background execution, and workflow IDs.

## 3. Step (step)
**Impact:** HIGH
**Description:** Step creation, retries, transactions via datasources, and when to use steps vs workflows.

## 4. Queue (queue)
**Impact:** HIGH
**Description:** WorkflowQueue creation, concurrency limits, rate limiting, partitioning, and priority.

## 5. Communication (comm)
**Impact:** MEDIUM
**Description:** Workflow events, messages, and streaming for inter-workflow communication.

## 6. Pattern (pattern)
**Impact:** MEDIUM
**Description:** Common patterns including idempotency, scheduled workflows, debouncing, and class instances.

## 7. Testing (test)
**Impact:** LOW-MEDIUM
**Description:** Testing DBOS applications with Jest, mocking, and integration test setup.

## 8. Client (client)
**Impact:** MEDIUM
**Description:** DBOSClient for interacting with DBOS from external applications.

## 9. Advanced (advanced)
**Impact:** LOW
**Description:** Workflow versioning, patching, and safe code upgrades.

---

## Reference: Advanced Patching

## Use Patching for Safe Workflow Upgrades

Use `DBOS.patch()` to safely deploy breaking changes to workflow code. Breaking changes alter which steps run or their order, which can cause recovery failures.

**Incorrect (breaking change without patching):**

```typescript
// BEFORE: original workflow
async function workflowFn() {
  await foo();
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);

// AFTER: breaking change - recovery will fail for in-progress workflows!
async function workflowFn() {
  await baz(); // Changed step
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);
```

**Correct (using patch):**

```typescript
async function workflowFn() {
  if (await DBOS.patch("use-baz")) {
    await baz(); // New workflows run this
  } else {
    await foo(); // Old workflows continue with original code
  }
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);
```

`DBOS.patch()` returns `true` for new workflows and `false` for workflows that started before the patch.

**Deprecating patches (after all old workflows complete):**

```typescript
async function workflowFn() {
  if (await DBOS.deprecatePatch("use-baz")) { // Always returns true
    await baz();
  }
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);
```

**Removing patches (after all workflows using deprecatePatch complete):**

```typescript
async function workflowFn() {
  await baz();
  await bar();
}
const workflow = DBOS.registerWorkflow(workflowFn);
```

Lifecycle: `patch()` → deploy → wait for old workflows → `deprecatePatch()` → deploy → wait → remove patch entirely.

Use `DBOS.listWorkflows` to check for active old workflows before deprecating or removing patches.

Reference: [Patching](https://docs.dbos.dev/typescript/tutorials/upgrading-workflows#patching)

---

## Reference: Advanced Versioning

## Use Versioning for Blue-Green Deployments

Set `applicationVersion` in configuration to tag workflows with a version. DBOS only recovers workflows matching the current application version, preventing code mismatches during recovery.

**Incorrect (deploying new code that breaks in-progress workflows):**

```typescript
DBOS.setConfig({
  name: "my-app",
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  // No version set - all workflows recovered regardless of code version
});
```

**Correct (versioned deployment):**

```typescript
DBOS.setConfig({
  name: "my-app",
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  applicationVersion: "2.0.0",
});
```

By default, the application version is automatically computed from a hash of workflow source code. Set it explicitly for more control.

**Blue-green deployment strategy:**

1. Deploy new version (v2) alongside old version (v1)
2. Direct new traffic to v2 processes
3. Let v1 processes "drain" (complete in-progress workflows)
4. Check for remaining v1 workflows:

```typescript
const oldWorkflows = await DBOS.listWorkflows({
  applicationVersion: "1.0.0",
  status: "PENDING",
});
```

5. Once all v1 workflows are complete, retire v1 processes

**Fork to new version (for stuck workflows):**

```typescript
// Fork a workflow from a failed step to run on the new version
const handle = await DBOS.forkWorkflow<string>(
  workflowID,
  failedStepID,
  { applicationVersion: "2.0.0" }
);
```

Reference: [Versioning](https://docs.dbos.dev/typescript/tutorials/upgrading-workflows#versioning)

---

## Reference: Client Enqueue

## Enqueue Workflows from External Applications

Use `client.enqueue()` to submit workflows from outside your DBOS application. Since `DBOSClient` runs externally, workflow and queue metadata must be specified explicitly.

**Incorrect (trying to use DBOS.startWorkflow from external code):**

```typescript
// DBOS.startWorkflow requires a full DBOS setup
await DBOS.startWorkflow(processTask, { queueName: "myQueue" })("data");
```

**Correct (using DBOSClient.enqueue):**

```typescript
import { DBOSClient } from "@dbos-inc/dbos-sdk";

const client = await DBOSClient.create({
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
});

// Basic enqueue
const handle = await client.enqueue(
  {
    workflowName: "processTask",
    queueName: "task_queue",
  },
  "task-data"
);

// Wait for the result
const result = await handle.getResult();
```

**Type-safe enqueue:**

```typescript
// Import or declare the workflow type
declare class Tasks {
  static processTask(data: string): Promise<string>;
}

const handle = await client.enqueue<typeof Tasks.processTask>(
  {
    workflowName: "processTask",
    workflowClassName: "Tasks",
    queueName: "task_queue",
  },
  "task-data"
);

// TypeScript infers the result type
const result = await handle.getResult(); // type: string
```

**Enqueue options:**
- `workflowName` (required): Name of the workflow function
- `queueName` (required): Name of the queue
- `workflowClassName`: Class name if the workflow is a class method
- `workflowConfigName`: Instance name if using `ConfiguredInstance`
- `workflowID`: Custom workflow ID
- `workflowTimeoutMS`: Timeout in milliseconds
- `deduplicationID`: Prevent duplicate enqueues
- `priority`: Queue priority (lower = higher priority)
- `queuePartitionKey`: Partition key for partitioned queues

Always call `client.destroy()` when done.

Reference: [DBOS Client Enqueue](https://docs.dbos.dev/typescript/reference/client#enqueue)

---

## Reference: Client Setup

## Initialize DBOSClient for External Access

Use `DBOSClient` to interact with DBOS from external applications like API servers, CLI tools, or separate services. `DBOSClient` connects directly to the DBOS system database.

**Incorrect (using DBOS directly from an external app):**

```typescript
// DBOS requires full setup with launch() - too heavy for external clients
DBOS.setConfig({ ... });
await DBOS.launch();
```

**Correct (using DBOSClient):**

```typescript
import { DBOSClient } from "@dbos-inc/dbos-sdk";

const client = await DBOSClient.create({
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
});

// Send a message to a workflow
await client.send(workflowID, "notification", "topic");

// Get an event from a workflow
const event = await client.getEvent<string>(workflowID, "status");

// Read a stream from a workflow
for await (const value of client.readStream(workflowID, "results")) {
  console.log(value);
}

// Retrieve a workflow handle
const handle = client.retrieveWorkflow<string>(workflowID);
const result = await handle.getResult();

// List workflows
const workflows = await client.listWorkflows({ status: "ERROR" });

// Workflow management
await client.cancelWorkflow(workflowID);
await client.resumeWorkflow(workflowID);

// Always destroy when done
await client.destroy();
```

Constructor options:
- `systemDatabaseUrl`: Connection string to the Postgres system database (required)
- `systemDatabasePool`: Optional custom `node-postgres` connection pool
- `serializer`: Optional custom serializer (must match the DBOS application's serializer)

Reference: [DBOS Client](https://docs.dbos.dev/typescript/reference/client)

---

## Reference: Comm Events

## Use Events for Workflow Status Publishing

Workflows can publish events (key-value pairs) with `DBOS.setEvent`. Other code can read events with `DBOS.getEvent`. Events are persisted and useful for real-time progress monitoring.

**Incorrect (using external state for progress):**

```typescript
let progress = 0; // Global variable - not durable!

async function processDataFn() {
  progress = 50; // Not persisted, lost on restart
}
const processData = DBOS.registerWorkflow(processDataFn);
```

**Correct (using events):**

```typescript
async function processDataFn() {
  await DBOS.setEvent("status", "processing");
  await DBOS.runStep(stepOne, { name: "stepOne" });
  await DBOS.setEvent("progress", 50);
  await DBOS.runStep(stepTwo, { name: "stepTwo" });
  await DBOS.setEvent("progress", 100);
  await DBOS.setEvent("status", "complete");
}
const processData = DBOS.registerWorkflow(processDataFn);

// Read events from outside the workflow
const status = await DBOS.getEvent<string>(workflowID, "status", 0);
const progress = await DBOS.getEvent<number>(workflowID, "progress", 0);
// Returns null if the event doesn't exist within the timeout (default 60s)
```

Events are useful for interactive workflows. For example, a checkout workflow can publish a payment URL for the caller to redirect to:

```typescript
async function checkoutWorkflowFn() {
  const paymentURL = await DBOS.runStep(createPayment, { name: "createPayment" });
  await DBOS.setEvent("paymentURL", paymentURL);
  // Continue processing...
}
const checkoutWorkflow = DBOS.registerWorkflow(checkoutWorkflowFn);

// HTTP handler starts workflow and reads the payment URL
const handle = await DBOS.startWorkflow(checkoutWorkflow)();
const url = await DBOS.getEvent<string>(handle.workflowID, "paymentURL", 300);
```

Reference: [Workflow Events](https://docs.dbos.dev/typescript/tutorials/workflow-communication#workflow-events)

---

## Reference: Comm Messages

## Use Messages for Workflow Notifications

Use `DBOS.send` to send messages to a workflow and `DBOS.recv` to receive them. Messages are queued per topic and persisted for reliable delivery.

**Incorrect (using external messaging for workflow communication):**

```typescript
// External message queue is not integrated with workflow recovery
import { Queue } from "some-external-queue";
```

**Correct (using DBOS messages):**

```typescript
async function checkoutWorkflowFn() {
  // Wait for payment notification (timeout 120 seconds)
  const notification = await DBOS.recv<string>("payment_status", 120);

  if (notification && notification === "paid") {
    await DBOS.runStep(fulfillOrder, { name: "fulfillOrder" });
  } else {
    await DBOS.runStep(cancelOrder, { name: "cancelOrder" });
  }
}
const checkoutWorkflow = DBOS.registerWorkflow(checkoutWorkflowFn);

// Send a message from a webhook handler
async function paymentWebhook(workflowID: string, status: string) {
  await DBOS.send(workflowID, status, "payment_status");
}
```

Key behaviors:
- `recv` waits for and consumes the next message for the specified topic
- Returns `null` if the wait times out (default timeout: 60 seconds)
- Messages without a topic can only be received by `recv` without a topic
- Messages are queued per-topic (FIFO)

**Reliability guarantees:**
- All messages are persisted to the database
- Messages sent from workflows are delivered exactly-once
- Messages sent from non-workflow code can use an idempotency key:

```typescript
await DBOS.send(workflowID, message, "topic", "idempotency-key-123");
```

Reference: [Workflow Messaging](https://docs.dbos.dev/typescript/tutorials/workflow-communication#workflow-messaging-and-notifications)

---

## Reference: Comm Streaming

## Use Streams for Real-Time Data

Workflows can stream data to clients in real-time using `DBOS.writeStream`, `DBOS.closeStream`, and `DBOS.readStream`. Useful for LLM output streaming or progress reporting.

**Incorrect (accumulating results then returning at end):**

```typescript
async function processWorkflowFn() {
  const results: string[] = [];
  for (const chunk of data) {
    results.push(await processChunk(chunk));
  }
  return results; // Client must wait for entire workflow to complete
}
```

**Correct (streaming results as they become available):**

```typescript
async function processWorkflowFn() {
  for (const chunk of data) {
    const result = await DBOS.runStep(() => processChunk(chunk), { name: "process" });
    await DBOS.writeStream("results", result);
  }
  await DBOS.closeStream("results"); // Signal completion
}
const processWorkflow = DBOS.registerWorkflow(processWorkflowFn);

// Read the stream from outside
const handle = await DBOS.startWorkflow(processWorkflow)();
for await (const value of DBOS.readStream<string>(handle.workflowID, "results")) {
  console.log(`Received: ${value}`);
}
```

Key behaviors:
- A workflow may have any number of streams, each identified by a unique key
- Streams are immutable and append-only
- Writes from workflows happen exactly-once
- Writes from steps happen at-least-once (retried steps may write duplicates)
- Streams are automatically closed when the workflow terminates
- `readStream` returns an async generator that yields values until the stream is closed

You can also read streams from outside the DBOS application using `DBOSClient.readStream`.

Reference: [Workflow Streaming](https://docs.dbos.dev/typescript/tutorials/workflow-communication#workflow-streaming)

---

## Reference: Lifecycle Config

## Configure and Launch DBOS Properly

Every DBOS application must configure and launch DBOS before running any workflows. All workflows and steps must be registered before calling `DBOS.launch()`.

**Incorrect (missing configuration or launch):**

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

// No configuration or launch!
async function myWorkflowFn() {
  // This will fail - DBOS is not launched
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
await myWorkflow();
```

**Correct (configure and launch in main):**

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function myWorkflowFn() {
  // workflow logic
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);

async function main() {
  DBOS.setConfig({
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  });
  await DBOS.launch();
  await myWorkflow();
}

main().catch(console.log);
```

Reference: [DBOS Lifecycle](https://docs.dbos.dev/typescript/reference/dbos-class)

---

## Reference: Lifecycle Express

## Integrate DBOS with Express

Configure and launch DBOS before starting your Express server. Register all workflows and steps before calling `DBOS.launch()`.

**Incorrect (DBOS not launched before server starts):**

```typescript
import express from "express";
import { DBOS } from "@dbos-inc/dbos-sdk";

const app = express();

async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// Server starts without launching DBOS!
app.listen(3000);
```

**Correct (launch DBOS first, then start Express):**

```typescript
import express from "express";
import { DBOS } from "@dbos-inc/dbos-sdk";

const app = express();

async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

app.post("/process", async (req, res) => {
  const handle = await DBOS.startWorkflow(processTask)(req.body.data);
  res.json({ workflowID: handle.workflowID });
});

async function main() {
  DBOS.setConfig({
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  });
  await DBOS.launch();
  app.listen(3000, () => {
    console.log("Server running on port 3000");
  });
}

main().catch(console.log);
```

Reference: [Integrating DBOS](https://docs.dbos.dev/typescript/integrating-dbos)

---

## Reference: Pattern Classes

## Use DBOS with Class Instances

Class instance methods can be workflows and steps. Classes with workflow methods must extend `ConfiguredInstance` to enable recovery.

**Incorrect (instance workflows without ConfiguredInstance):**

```typescript
class MyWorker {
  constructor(private config: any) {}

  @DBOS.workflow()
  async processTask(task: string) {
    // Recovery won't work - DBOS can't find the instance after restart
  }
}
```

**Correct (extending ConfiguredInstance):**

```typescript
import { DBOS, ConfiguredInstance } from "@dbos-inc/dbos-sdk";

class MyWorker extends ConfiguredInstance {
  cfg: WorkerConfig;

  constructor(name: string, config: WorkerConfig) {
    super(name); // Unique name required for recovery
    this.cfg = config;
  }

  override async initialize(): Promise<void> {
    // Optional: validate config at DBOS.launch() time
  }

  @DBOS.workflow()
  async processTask(task: string): Promise<void> {
    // Can use this.cfg safely - instance is recoverable
    const result = await DBOS.runStep(
      () => fetch(this.cfg.apiUrl).then(r => r.text()),
      { name: "callApi" }
    );
  }
}

// Create instances BEFORE DBOS.launch()
const worker1 = new MyWorker("worker-us", { apiUrl: "https://us.api.com" });
const worker2 = new MyWorker("worker-eu", { apiUrl: "https://eu.api.com" });

// Then launch
await DBOS.launch();
```

Key requirements:
- `ConfiguredInstance` constructor requires a unique `name` per class
- All instances must be created **before** `DBOS.launch()`
- The `initialize()` method is called during launch for validation
- Use `DBOS.runStep` inside instance workflows for step operations
- Event registration decorators like `@DBOS.scheduled` cannot be applied to instance methods

Reference: [Using TypeScript Objects](https://docs.dbos.dev/typescript/tutorials/instantiated-objects)

---

## Reference: Pattern Debouncing

## Debounce Workflows to Prevent Wasted Work

Use `Debouncer` to delay workflow execution until some time has passed since the last trigger. This prevents wasted work when a workflow is triggered multiple times in quick succession.

**Incorrect (executing on every trigger):**

```typescript
async function processInputFn(userInput: string) {
  // Expensive processing
}
const processInput = DBOS.registerWorkflow(processInputFn);

// Every keystroke triggers a new workflow - wasteful!
async function onInputChange(userInput: string) {
  await processInput(userInput);
}
```

**Correct (using Debouncer):**

```typescript
import { DBOS, Debouncer } from "@dbos-inc/dbos-sdk";

async function processInputFn(userInput: string) {
  // Expensive processing
}
const processInput = DBOS.registerWorkflow(processInputFn);

const debouncer = new Debouncer({
  workflow: processInput,
  debounceTimeoutMs: 120000, // Max wait: 2 minutes
});

async function onInputChange(userId: string, userInput: string) {
  // Delays execution by 60 seconds from the last call
  // Uses the LAST set of inputs when finally executing
  await debouncer.debounce(userId, 60000, userInput);
}
```

Key behaviors:
- `debounceKey` groups executions that are debounced together (e.g., per user)
- `debouncePeriodMs` delays execution by this amount from the last call
- `debounceTimeoutMs` sets a max wait time since the first trigger
- When the workflow finally executes, it uses the **last** set of inputs
- After execution begins, the next `debounce` call starts a new cycle
- Workflows from `ConfiguredInstance` classes cannot be debounced

Reference: [Debouncing Workflows](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#debouncing-workflows)

---

## Reference: Pattern Idempotency

## Use Workflow IDs for Idempotency

Assign a workflow ID to ensure a workflow executes only once, even if called multiple times. This prevents duplicate side effects like double payments.

**Incorrect (no idempotency):**

```typescript
async function processPaymentFn(orderId: string, amount: number) {
  await DBOS.runStep(() => chargeCard(amount), { name: "chargeCard" });
  await DBOS.runStep(() => updateOrder(orderId), { name: "updateOrder" });
}
const processPayment = DBOS.registerWorkflow(processPaymentFn);

// Multiple calls could charge the card multiple times!
await processPayment("order-123", 50);
await processPayment("order-123", 50); // Double charge!
```

**Correct (with workflow ID):**

```typescript
async function processPaymentFn(orderId: string, amount: number) {
  await DBOS.runStep(() => chargeCard(amount), { name: "chargeCard" });
  await DBOS.runStep(() => updateOrder(orderId), { name: "updateOrder" });
}
const processPayment = DBOS.registerWorkflow(processPaymentFn);

// Same workflow ID = only one execution
const workflowID = `payment-${orderId}`;
await DBOS.startWorkflow(processPayment, { workflowID })("order-123", 50);
await DBOS.startWorkflow(processPayment, { workflowID })("order-123", 50);
// Second call returns the result of the first execution
```

Access the current workflow ID inside a workflow:

```typescript
async function myWorkflowFn() {
  const currentID = DBOS.workflowID;
  console.log(`Running workflow: ${currentID}`);
}
```

Workflow IDs must be **globally unique** for your application. If not set, a random UUID is generated.

Reference: [Workflow IDs and Idempotency](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#workflow-ids-and-idempotency)

---

## Reference: Pattern Scheduled

## Create Scheduled Workflows

Use `DBOS.registerScheduled` to run workflows on a cron schedule. Each scheduled invocation runs exactly once per interval.

**Incorrect (manual scheduling with setInterval):**

```typescript
// Manual scheduling is not durable and misses intervals during downtime
setInterval(async () => {
  await generateReport();
}, 60000);
```

**Correct (using DBOS.registerScheduled):**

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function everyThirtySecondsFn(scheduledTime: Date, actualTime: Date) {
  DBOS.logger.info("Running scheduled task");
}
const everyThirtySeconds = DBOS.registerWorkflow(everyThirtySecondsFn);
DBOS.registerScheduled(everyThirtySeconds, { crontab: "*/30 * * * * *" });

async function dailyReportFn(scheduledTime: Date, actualTime: Date) {
  await DBOS.runStep(generateReport, { name: "generateReport" });
}
const dailyReport = DBOS.registerWorkflow(dailyReportFn);
DBOS.registerScheduled(dailyReport, { crontab: "0 9 * * *" });
```

Scheduled workflows must accept exactly two parameters: `scheduledTime` (Date) and `actualTime` (Date).

DBOS crontab supports 5 or 6 fields (optional seconds):
```text
┌────────────── second (optional)
│ ┌──────────── minute
│ │ ┌────────── hour
│ │ │ ┌──────── day of month
│ │ │ │ ┌────── month
│ │ │ │ │ ┌──── day of week
* * * * * *
```

Retroactive execution (for missed intervals):

```typescript
import { DBOS, SchedulerMode } from "@dbos-inc/dbos-sdk";

async function fridayNightJobFn(scheduledTime: Date, actualTime: Date) {
  // Runs even if the app was offline during the scheduled time
}
const fridayNightJob = DBOS.registerWorkflow(fridayNightJobFn);
DBOS.registerScheduled(fridayNightJob, {
  crontab: "0 21 * * 5",
  mode: SchedulerMode.ExactlyOncePerInterval,
});
```

Scheduled workflows cannot be applied to instance methods.

Reference: [Scheduled Workflows](https://docs.dbos.dev/typescript/tutorials/scheduled-workflows)

---

## Reference: Pattern Sleep

## Use Durable Sleep for Delayed Execution

Use `DBOS.sleep()` for durable delays within workflows. The wakeup time is stored in the database, so the sleep survives restarts.

**Incorrect (non-durable sleep):**

```typescript
async function delayedTaskFn() {
  // setTimeout is not durable - lost on restart!
  await new Promise(r => setTimeout(r, 60000));
  await DBOS.runStep(doWork, { name: "doWork" });
}
const delayedTask = DBOS.registerWorkflow(delayedTaskFn);
```

**Correct (durable sleep):**

```typescript
async function delayedTaskFn() {
  // Durable sleep - survives restarts
  await DBOS.sleep(60000); // 60 seconds in milliseconds
  await DBOS.runStep(doWork, { name: "doWork" });
}
const delayedTask = DBOS.registerWorkflow(delayedTaskFn);
```

`DBOS.sleep()` takes milliseconds (unlike Python which takes seconds).

Use cases:
- Scheduling tasks to run in the future
- Implementing retry delays
- Delays spanning hours, days, or weeks

```typescript
async function scheduledTaskFn(task: string) {
  // Sleep for one week
  await DBOS.sleep(7 * 24 * 60 * 60 * 1000);
  await processTask(task);
}
```

For getting the current time durably, use `DBOS.now()`:

```typescript
async function myWorkflowFn() {
  const now = await DBOS.now(); // Checkpointed as a step
  // For random UUIDs:
  const id = await DBOS.randomUUID(); // Checkpointed as a step
}
```

Reference: [Durable Sleep](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#durable-sleep)

---

## Reference: Queue Basics

## Use Queues for Concurrent Workflows

Queues run many workflows concurrently with managed flow control. Use them when you need to control how many workflows run at once.

**Incorrect (uncontrolled concurrency):**

```typescript
async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// Starting many workflows without control - could overwhelm resources
for (const task of tasks) {
  await DBOS.startWorkflow(processTask)(task);
}
```

**Correct (using a queue):**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const queue = new WorkflowQueue("task_queue");

async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

async function processAllTasksFn(tasks: string[]) {
  const handles = [];
  for (const task of tasks) {
    // Enqueue by passing queueName to startWorkflow
    const handle = await DBOS.startWorkflow(processTask, {
      queueName: queue.name,
    })(task);
    handles.push(handle);
  }
  // Wait for all tasks
  const results = [];
  for (const h of handles) {
    results.push(await h.getResult());
  }
  return results;
}
const processAllTasks = DBOS.registerWorkflow(processAllTasksFn);
```

Queues process workflows in FIFO order. All queues should be created before `DBOS.launch()`.

Reference: [DBOS Queues](https://docs.dbos.dev/typescript/tutorials/queue-tutorial)

---

## Reference: Queue Concurrency

## Control Queue Concurrency

Queues support worker-level and global concurrency limits to prevent resource exhaustion.

**Incorrect (no concurrency control):**

```typescript
const queue = new WorkflowQueue("heavy_tasks"); // No limits - could exhaust memory
```

**Correct (worker concurrency):**

```typescript
// Each process runs at most 5 tasks from this queue
const queue = new WorkflowQueue("heavy_tasks", { workerConcurrency: 5 });
```

**Correct (global concurrency):**

```typescript
// At most 10 tasks run across ALL processes
const queue = new WorkflowQueue("limited_tasks", { concurrency: 10 });
```

**In-order processing (sequential):**

```typescript
// Only one task at a time - guarantees order
const serialQueue = new WorkflowQueue("sequential_queue", { concurrency: 1 });

async function processEventFn(event: string) {
  // ...
}
const processEvent = DBOS.registerWorkflow(processEventFn);

app.post("/events", async (req, res) => {
  await DBOS.startWorkflow(processEvent, { queueName: serialQueue.name })(req.body.event);
  res.send("Queued!");
});
```

Worker concurrency is recommended for most use cases. Take care with global concurrency as any `PENDING` workflow on the queue counts toward the limit, including workflows from previous application versions.

When using worker concurrency, each process must have a unique `executorID` set in configuration (this is automatic with DBOS Conductor or Cloud).

Reference: [Managing Concurrency](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#managing-concurrency)

---

## Reference: Queue Deduplication

## Deduplicate Queued Workflows

Set a deduplication ID when enqueuing to prevent duplicate workflow executions. If a workflow with the same deduplication ID is already enqueued or executing, a `DBOSQueueDuplicatedError` is thrown.

**Incorrect (no deduplication):**

```typescript
// Multiple clicks could enqueue duplicates
async function handleClick(userId: string) {
  await DBOS.startWorkflow(processTask, { queueName: queue.name })("task");
}
```

**Correct (with deduplication):**

```typescript
const queue = new WorkflowQueue("task_queue");

async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

async function handleClick(userId: string) {
  try {
    await DBOS.startWorkflow(processTask, {
      queueName: queue.name,
      enqueueOptions: { deduplicationID: userId },
    })("task");
  } catch (e) {
    // DBOSQueueDuplicatedError - workflow already active for this user
    console.log("Task already in progress for user:", userId);
  }
}
```

Deduplication is per-queue. The deduplication ID is active while the workflow has status `ENQUEUED` or `PENDING`. Once the workflow completes, a new workflow with the same deduplication ID can be enqueued.

This is useful for:
- Ensuring one active task per user
- Preventing duplicate form submissions
- Idempotent event processing

Reference: [Deduplication](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#deduplication)

---

## Reference: Queue Listening

## Control Which Queues a Worker Listens To

Configure `listenQueues` in DBOS configuration to make a process only dequeue from specific queues. This enables heterogeneous worker pools.

**Incorrect (all workers process all queues):**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const cpuQueue = new WorkflowQueue("cpu_queue");
const gpuQueue = new WorkflowQueue("gpu_queue");

// Every worker processes both CPU and GPU tasks
// GPU tasks on CPU workers will fail or be slow!
DBOS.setConfig({
  name: "my-app",
  systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
});
await DBOS.launch();
```

**Correct (selective queue listening):**

```typescript
import { DBOS, WorkflowQueue } from "@dbos-inc/dbos-sdk";

const cpuQueue = new WorkflowQueue("cpu_queue");
const gpuQueue = new WorkflowQueue("gpu_queue");

async function main() {
  const workerType = process.env.WORKER_TYPE; // "cpu" or "gpu"

  const config: any = {
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  };

  if (workerType === "gpu") {
    config.listenQueues = [gpuQueue];
  } else if (workerType === "cpu") {
    config.listenQueues = [cpuQueue];
  }

  DBOS.setConfig(config);
  await DBOS.launch();
}
```

`listenQueues` only controls dequeuing. A CPU worker can still enqueue tasks onto the GPU queue:

```typescript
// From a CPU worker, enqueue onto the GPU queue
await DBOS.startWorkflow(gpuTask, { queueName: gpuQueue.name })("data");
```

Reference: [Explicit Queue Listening](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#explicit-queue-listening)

---

## Reference: Queue Partitioning

## Partition Queues for Per-Entity Limits

Partitioned queues apply flow control limits per partition key instead of the entire queue. Each partition acts as a dynamic "subqueue".

**Incorrect (global concurrency for per-user limits):**

```typescript
// Global concurrency=1 blocks ALL users, not per-user
const queue = new WorkflowQueue("tasks", { concurrency: 1 });
```

**Correct (partitioned queue):**

```typescript
const queue = new WorkflowQueue("tasks", {
  partitionQueue: true,
  concurrency: 1,
});

async function onUserTask(userID: string, task: string) {
  // Each user gets their own partition - at most 1 task per user
  // but tasks from different users can run concurrently
  await DBOS.startWorkflow(processTask, {
    queueName: queue.name,
    enqueueOptions: { queuePartitionKey: userID },
  })(task);
}
```

**Two-level queueing (per-user + global limits):**

```typescript
const concurrencyQueue = new WorkflowQueue("concurrency-queue", { concurrency: 5 });
const partitionedQueue = new WorkflowQueue("partitioned-queue", {
  partitionQueue: true,
  concurrency: 1,
});

// At most 1 task per user AND at most 5 tasks globally
async function onUserTask(userID: string, task: string) {
  await DBOS.startWorkflow(concurrencyManager, {
    queueName: partitionedQueue.name,
    enqueueOptions: { queuePartitionKey: userID },
  })(task);
}

async function concurrencyManagerFn(task: string) {
  const handle = await DBOS.startWorkflow(processTask, {
    queueName: concurrencyQueue.name,
  })(task);
  return await handle.getResult();
}
const concurrencyManager = DBOS.registerWorkflow(concurrencyManagerFn);
```

Reference: [Partitioning Queues](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#partitioning-queues)

---

## Reference: Queue Priority

## Set Queue Priority for Workflows

Enable priority on a queue to process higher-priority workflows first. Lower numbers indicate higher priority.

**Incorrect (no priority - FIFO only):**

```typescript
const queue = new WorkflowQueue("tasks");
// All tasks processed in FIFO order regardless of importance
```

**Correct (priority-enabled queue):**

```typescript
const queue = new WorkflowQueue("tasks", { priorityEnabled: true });

async function processTaskFn(task: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// High priority task (lower number = higher priority)
await DBOS.startWorkflow(processTask, {
  queueName: queue.name,
  enqueueOptions: { priority: 1 },
})("urgent-task");

// Low priority task
await DBOS.startWorkflow(processTask, {
  queueName: queue.name,
  enqueueOptions: { priority: 100 },
})("background-task");
```

Priority rules:
- Range: `1` to `2,147,483,647`
- Lower number = higher priority
- Workflows **without** assigned priorities have the highest priority (run first)
- Workflows with the same priority are dequeued in FIFO order

Reference: [Priority](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#priority)

---

## Reference: Queue Rate Limiting

## Rate Limit Queue Execution

Set rate limits on a queue to control how many workflows start in a given period. Rate limits are global across all DBOS processes.

**Incorrect (no rate limiting):**

```typescript
const queue = new WorkflowQueue("llm_tasks");
// Could send hundreds of requests per second to a rate-limited API
```

**Correct (rate-limited queue):**

```typescript
const queue = new WorkflowQueue("llm_tasks", {
  rateLimit: { limitPerPeriod: 50, periodSec: 30 },
});
```

This queue starts at most 50 workflows per 30 seconds.

**Combining rate limiting with concurrency:**

```typescript
// At most 5 concurrent and 50 per 30 seconds
const queue = new WorkflowQueue("api_tasks", {
  workerConcurrency: 5,
  rateLimit: { limitPerPeriod: 50, periodSec: 30 },
});
```

Common use cases:
- LLM API rate limiting (OpenAI, Anthropic, etc.)
- Third-party API throttling
- Preventing database overload

Reference: [Rate Limiting](https://docs.dbos.dev/typescript/tutorials/queue-tutorial#rate-limiting)

---

## Reference: Step Basics

## Use Steps for External Operations

Any function that performs complex operations, accesses external APIs, or has side effects should be a step. Step results are checkpointed, enabling workflow recovery.

**Incorrect (external call in workflow):**

```typescript
async function myWorkflowFn() {
  // External API call directly in workflow - not checkpointed!
  const response = await fetch("https://api.example.com/data");
  return await response.json();
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

**Correct (external call in step using `DBOS.runStep`):**

```typescript
async function fetchData() {
  return await fetch("https://api.example.com/data").then(r => r.json());
}

async function myWorkflowFn() {
  const data = await DBOS.runStep(fetchData, { name: "fetchData" });
  return data;
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

`DBOS.runStep` can also accept an inline arrow function:

```typescript
async function myWorkflowFn() {
  const data = await DBOS.runStep(
    () => fetch("https://api.example.com/data").then(r => r.json()),
    { name: "fetchData" }
  );
  return data;
}
```

Alternatively, you can use `DBOS.registerStep` to pre-register a step or `@DBOS.step()` as a class decorator, but `DBOS.runStep` is preferred for most use cases.

Step requirements:
- Inputs and outputs must be serializable to JSON
- Cannot call, start, or enqueue workflows from within steps
- Calling a step from another step makes the called step part of the calling step's execution

When to use steps:
- API calls to external services
- File system operations
- Random number generation
- Getting current time
- Any non-deterministic operation

Reference: [DBOS Steps](https://docs.dbos.dev/typescript/tutorials/step-tutorial)

---

## Reference: Step Retries

## Configure Step Retries for Transient Failures

Steps can automatically retry on failure with exponential backoff. This handles transient failures like network issues.

**Incorrect (manual retry logic):**

```typescript
async function fetchData() {
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      return await fetch("https://api.example.com").then(r => r.json());
    } catch (e) {
      if (attempt === 2) throw e;
      await new Promise(r => setTimeout(r, 2 ** attempt * 1000));
    }
  }
}
```

**Correct (built-in retries with `DBOS.runStep`):**

```typescript
async function fetchData() {
  return await fetch("https://api.example.com").then(r => r.json());
}

async function myWorkflowFn() {
  const data = await DBOS.runStep(fetchData, {
    name: "fetchData",
    retriesAllowed: true,
    maxAttempts: 10,
    intervalSeconds: 1,
    backoffRate: 2,
  });
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

With an inline arrow function:

```typescript
async function myWorkflowFn() {
  const data = await DBOS.runStep(
    () => fetch("https://api.example.com").then(r => r.json()),
    { name: "fetchData", retriesAllowed: true, maxAttempts: 10 }
  );
}
```

Retry parameters:
- `retriesAllowed`: Enable automatic retries (default: `false`)
- `maxAttempts`: Maximum retry attempts (default: `3`)
- `intervalSeconds`: Initial delay between retries in seconds (default: `1`)
- `backoffRate`: Multiplier for exponential backoff (default: `2`)

With defaults, retry delays are: 1s, 2s, 4s, 8s, 16s...

If all retries are exhausted, a `DBOSMaxStepRetriesError` is thrown to the calling workflow.

Reference: [Configurable Retries](https://docs.dbos.dev/typescript/tutorials/step-tutorial#configurable-retries)

---

## Reference: Step Transactions

## Use Transactions for Database Operations

Use datasource transactions for database operations within workflows. Transactions commit exactly once and are checkpointed for recovery.

**Incorrect (raw database query in workflow):**

```typescript
import { Pool } from "pg";
const pool = new Pool();

async function myWorkflowFn() {
  // Direct database access in workflow - not checkpointed!
  const result = await pool.query("INSERT INTO orders ...");
}
```

**Correct (using a datasource transaction):**

Install a datasource package (e.g., Knex):
```
npm i @dbos-inc/knex-datasource
```

Configure the datasource:
```typescript
import { KnexDataSource } from "@dbos-inc/knex-datasource";

const config = { client: "pg", connection: process.env.DBOS_DATABASE_URL };
const dataSource = new KnexDataSource("app-db", config);
```

Run transactions inline with `runTransaction`:
```typescript
async function insertOrderFn(userId: string, amount: number) {
  const rows = await dataSource
    .client("orders")
    .insert({ user_id: userId, amount })
    .returning("id");
  return rows[0].id;
}

async function myWorkflowFn(userId: string, amount: number) {
  const orderId = await dataSource.runTransaction(
    () => insertOrderFn(userId, amount),
    { name: "insertOrder" }
  );
  return orderId;
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

You can also pre-register a transaction function with `dataSource.registerTransaction`:
```typescript
const insertOrder = dataSource.registerTransaction(insertOrderFn);
```

Available datasource packages: `@dbos-inc/knex-datasource`, `@dbos-inc/kysely-datasource`, `@dbos-inc/drizzle-datasource`, `@dbos-inc/typeorm-datasource`, `@dbos-inc/prisma-datasource`, `@dbos-inc/nodepg-datasource`, `@dbos-inc/postgres-datasource`.

Datasources require installing the DBOS schema (`transaction_completion` table) via `initializeDBOSSchema`.

Reference: [Transactions & Datasources](https://docs.dbos.dev/typescript/tutorials/transaction-tutorial)

---

## Reference: Test Setup

## Use Proper Test Setup for DBOS

DBOS applications can be tested with unit tests (mocking DBOS) or integration tests (real Postgres database).

**Incorrect (no lifecycle management between tests):**

```typescript
// Tests share state - results are inconsistent!
describe("tests", () => {
  it("test one", async () => {
    await myWorkflow("input");
  });
  it("test two", async () => {
    // Previous test's state leaks into this test
    await myWorkflow("input");
  });
});
```

**Correct (unit testing with mocks):**

```typescript
// Mock DBOS - no Postgres required
jest.mock("@dbos-inc/dbos-sdk", () => ({
  DBOS: {
    registerWorkflow: jest.fn((fn) => fn),
    runStep: jest.fn((fn) => fn()),
    setEvent: jest.fn(),
    recv: jest.fn(),
    startWorkflow: jest.fn(),
    workflowID: "test-workflow-id",
  },
}));

describe("workflow unit tests", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should process data", async () => {
    jest.mocked(DBOS.recv).mockResolvedValue("success");
    await myWorkflow("input");
    expect(DBOS.setEvent).toHaveBeenCalledWith("status", "done");
  });
});
```

Mock `registerWorkflow` to return the function directly (not wrapped with durable workflow code).

**Correct (integration testing with Postgres):**

```typescript
import { DBOS, DBOSConfig } from "@dbos-inc/dbos-sdk";
import { Client } from "pg";

async function resetDatabase(databaseUrl: string) {
  const dbName = new URL(databaseUrl).pathname.slice(1);
  const postgresDatabaseUrl = new URL(databaseUrl);
  postgresDatabaseUrl.pathname = "/postgres";
  const client = new Client({ connectionString: postgresDatabaseUrl.toString() });
  await client.connect();
  try {
    await client.query(`DROP DATABASE IF EXISTS ${dbName} WITH (FORCE)`);
    await client.query(`CREATE DATABASE ${dbName}`);
  } finally {
    await client.end();
  }
}

describe("integration tests", () => {
  beforeEach(async () => {
    const databaseUrl = process.env.DBOS_TEST_DATABASE_URL;
    if (!databaseUrl) throw Error("DBOS_TEST_DATABASE_URL must be set");
    await DBOS.shutdown();
    await resetDatabase(databaseUrl);
    DBOS.setConfig({ name: "my-integration-test", systemDatabaseUrl: databaseUrl });
    await DBOS.launch();
  }, 10000);

  afterEach(async () => {
    await DBOS.shutdown();
  });

  it("should complete workflow", async () => {
    const result = await myWorkflow("test-input");
    expect(result).toBe("expected-output");
  });
});
```

Key points:
- Call `DBOS.shutdown()` before resetting and reconfiguring
- Reset the database between tests for isolation
- Set a generous `beforeEach` timeout (10s) for database setup
- Use `DBOS.shutdown({ deregister: true })` if re-registering functions

Reference: [Testing & Mocking](https://docs.dbos.dev/typescript/tutorials/testing)

---

## Reference: Workflow Background

## Start Workflows in Background

Use `DBOS.startWorkflow` to start a workflow in the background and get a handle to track it. The workflow is guaranteed to run to completion even if the app is interrupted.

**Incorrect (no way to track background work):**

```typescript
async function processDataFn(data: string) {
  // ...
}
const processData = DBOS.registerWorkflow(processDataFn);

// Fire and forget - no way to track or get result
processData(data);
```

**Correct (using startWorkflow):**

```typescript
async function processDataFn(data: string) {
  return "processed: " + data;
}
const processData = DBOS.registerWorkflow(processDataFn);

async function main() {
  // Start workflow in background, get handle
  const handle = await DBOS.startWorkflow(processData)("input");

  // Get the workflow ID
  console.log(handle.workflowID);

  // Wait for result
  const result = await handle.getResult();

  // Check status
  const status = await handle.getStatus();
}
```

Retrieve a handle later by workflow ID:

```typescript
const handle = DBOS.retrieveWorkflow<string>(workflowID);
const result = await handle.getResult();
```

Reference: [Starting Workflows in Background](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#starting-workflows-in-the-background)

---

## Reference: Workflow Constraints

## Follow Workflow Constraints

Workflows have specific constraints to maintain durability guarantees. Violating them can break recovery.

**Incorrect (starting workflows from steps):**

```typescript
async function myStep() {
  // Don't start workflows from steps!
  await DBOS.startWorkflow(otherWorkflow)();
}

async function myOtherStep() {
  // Don't call recv from steps!
  const msg = await DBOS.recv("topic");
}

async function myWorkflowFn() {
  await DBOS.runStep(myStep, { name: "myStep" });
}
```

**Correct (workflow operations only from workflows):**

```typescript
async function fetchData() {
  // Steps only do external operations
  return await fetch("https://api.example.com").then(r => r.json());
}

async function myWorkflowFn() {
  await DBOS.runStep(fetchData, { name: "fetchData" });
  // Start child workflows from the parent workflow
  await DBOS.startWorkflow(otherWorkflow)();
  // Receive messages from the workflow
  const msg = await DBOS.recv("topic");
  // Set events from the workflow
  await DBOS.setEvent("status", "done");
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

Additional constraints:
- Don't modify global variables from workflows or steps
- Steps in parallel must start in deterministic order:

```typescript
// CORRECT - deterministic start order
const results = await Promise.allSettled([
  DBOS.runStep(() => step1("arg1"), { name: "step1" }),
  DBOS.runStep(() => step2("arg2"), { name: "step2" }),
  DBOS.runStep(() => step3("arg3"), { name: "step3" }),
]);
```

Use `Promise.allSettled` instead of `Promise.all` to safely handle errors without crashing the Node.js process.

Reference: [Workflow Guarantees](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#workflow-guarantees)

---

## Reference: Workflow Control

## Cancel, Resume, and Fork Workflows

DBOS provides methods to cancel, resume, and fork workflows for operational control.

**Incorrect (no way to handle stuck or failed workflows):**

```typescript
// Workflow is stuck or failed - no recovery mechanism
const handle = await DBOS.startWorkflow(processTask)("data");
// If the workflow fails, there's no way to retry or recover
```

**Correct (using cancel, resume, and fork):**

```typescript
// Cancel a workflow - stops at its next step
await DBOS.cancelWorkflow(workflowID);

// Resume from the last completed step
const handle = await DBOS.resumeWorkflow<string>(workflowID);
const result = await handle.getResult();
```

Cancellation sets the workflow status to `CANCELLED` and preempts execution at the beginning of the next step. Cancelling also cancels all child workflows.

Resume restarts a workflow from its last completed step. Use this for workflows that are cancelled or have exceeded their maximum recovery attempts. You can also use this to start an enqueued workflow immediately, bypassing its queue.

Fork a workflow from a specific step:

```typescript
// List steps to find the right step ID
const steps = await DBOS.listWorkflowSteps(workflowID);
// steps[i].functionID is the step's ID

// Fork from a specific step
const forkHandle = await DBOS.forkWorkflow<string>(
  workflowID,
  startStep,
  {
    newWorkflowID: "new-wf-id",
    applicationVersion: "2.0.0",
    timeoutMS: 60000,
  }
);
const forkResult = await forkHandle.getResult();
```

Forking creates a new workflow with a new ID, copying the original workflow's inputs and step outputs up to the selected step. Useful for recovering from downstream service outages or patching workflows that failed due to a bug.

Reference: [Workflow Management](https://docs.dbos.dev/typescript/tutorials/workflow-management)

---

## Reference: Workflow Determinism

## Keep Workflows Deterministic

Workflow functions must be deterministic: given the same inputs and step return values, they must invoke the same steps in the same order. Non-deterministic operations must be moved to steps.

**Incorrect (non-deterministic workflow):**

```typescript
async function exampleWorkflowFn() {
  // Random value in workflow breaks recovery!
  // On replay, Math.random() returns a different value,
  // so the workflow may take a different branch.
  const choice = Math.random() > 0.5 ? 1 : 0;
  if (choice === 0) {
    await stepOne();
  } else {
    await stepTwo();
  }
}
const exampleWorkflow = DBOS.registerWorkflow(exampleWorkflowFn);
```

**Correct (non-determinism in step):**

```typescript
async function exampleWorkflowFn() {
  // Step result is checkpointed - replay uses the saved value
  const choice = await DBOS.runStep(
    () => Promise.resolve(Math.random() > 0.5 ? 1 : 0),
    { name: "generateChoice" }
  );
  if (choice === 0) {
    await stepOne();
  } else {
    await stepTwo();
  }
}
const exampleWorkflow = DBOS.registerWorkflow(exampleWorkflowFn);
```

Non-deterministic operations that must be in steps:
- Random number generation (use `DBOS.randomUUID()` for UUIDs)
- Getting current time (use `DBOS.now()` for timestamps)
- Accessing external APIs
- Reading files
- Database queries (use transactions or steps)

Reference: [Workflow Determinism](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#determinism)

---

## Reference: Workflow Introspection

## List and Inspect Workflows

Use `DBOS.listWorkflows` to query workflow executions by status, name, time range, and other criteria.

**Incorrect (no monitoring of workflow state):**

```typescript
// Start workflow with no way to check on it later
await DBOS.startWorkflow(processTask)("data");
// If something goes wrong, no way to find or debug it
```

**Correct (listing and inspecting workflows):**

```typescript
// List workflows by status
const erroredWorkflows = await DBOS.listWorkflows({
  status: "ERROR",
});

for (const wf of erroredWorkflows) {
  console.log(`Workflow ${wf.workflowID}: ${wf.workflowName} - ${wf.error}`);
}
```

List workflows with multiple filters:

```typescript
const workflows = await DBOS.listWorkflows({
  workflowName: "processOrder",
  status: "SUCCESS",
  limit: 100,
  sortDesc: true,
  loadOutput: true,
});
```

List enqueued workflows:

```typescript
const queued = await DBOS.listQueuedWorkflows({
  queueName: "task_queue",
});
```

List workflow steps:

```typescript
const steps = await DBOS.listWorkflowSteps(workflowID);
if (steps) {
  for (const step of steps) {
    console.log(`Step ${step.functionID}: ${step.name}`);
    if (step.error) console.log(`  Error: ${step.error}`);
    if (step.childWorkflowID) console.log(`  Child: ${step.childWorkflowID}`);
  }
}
```

Workflow status values: `ENQUEUED`, `PENDING`, `SUCCESS`, `ERROR`, `CANCELLED`, `RETRIES_EXCEEDED`

To optimize performance, set `loadInput: false` and `loadOutput: false` when you don't need workflow inputs or outputs.

Reference: [Workflow Management](https://docs.dbos.dev/typescript/tutorials/workflow-management)

---

## Reference: Workflow Timeout

## Set Workflow Timeouts

Set a timeout for a workflow by passing `timeoutMS` to `DBOS.startWorkflow`. When the timeout expires, the workflow and all its children are cancelled.

**Incorrect (no timeout for potentially long workflow):**

```typescript
// No timeout - could run indefinitely
const handle = await DBOS.startWorkflow(processTask)("data");
```

**Correct (with timeout):**

```typescript
async function processTaskFn(data: string) {
  // ...
}
const processTask = DBOS.registerWorkflow(processTaskFn);

// Timeout after 5 minutes (in milliseconds)
const handle = await DBOS.startWorkflow(processTask, {
  timeoutMS: 5 * 60 * 1000,
})("data");
```

Key timeout behaviors:
- Timeouts are **start-to-completion**: the timeout begins when the workflow starts execution, not when it's enqueued
- Timeouts are **durable**: they persist across restarts, so workflows can have very long timeouts (hours, days, weeks)
- Cancellation happens at the **beginning of the next step** - the current step completes first
- Cancelling a workflow also cancels all **child workflows**

Reference: [Workflow Timeouts](https://docs.dbos.dev/typescript/tutorials/workflow-tutorial#workflow-timeouts)
