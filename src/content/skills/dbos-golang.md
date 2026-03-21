---
title: "Dbos Golang"
description: "DBOS Go SDK for building reliable, fault-tolerant applications with durable workflows. Use this skill when writing Go code with DBOS, creating workflows and steps, using queues, using the DBOS Clie..."
category: "writing"
source: "community"
author: "Community"
tags: ["dbos", "golang"]
date: 2026-03-20
---

# DBOS Go Best Practices

Guide for building reliable, fault-tolerant Go applications with DBOS durable workflows.

## When to Use

Reference these guidelines when:
- Adding DBOS to existing Go code
- Creating workflows and steps
- Using queues for concurrency control
- Implementing workflow communication (events, messages, streams)
- Configuring and launching DBOS applications
- Using the DBOS Client from external applications
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

Install the DBOS Go module:

```bash
go get github.com/dbos-inc/dbos-transact-golang/dbos@latest
```

### DBOS Configuration and Launch

A DBOS application MUST create a context, register workflows, and launch before running any workflows:

```go
package main

import (
	"context"
	"log"
	"os"
	"time"

	"github.com/dbos-inc/dbos-transact-golang/dbos"
)

func main() {
	ctx, err := dbos.NewDBOSContext(context.Background(), dbos.Config{
		AppName:     "my-app",
		DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	})
	if err != nil {
		log.Fatal(err)
	}
	defer dbos.Shutdown(ctx, 30*time.Second)

	dbos.RegisterWorkflow(ctx, myWorkflow)

	if err := dbos.Launch(ctx); err != nil {
		log.Fatal(err)
	}
}
```

### Workflow and Step Structure

Workflows are comprised of steps. Any function performing complex operations or accessing external services must be run as a step using `dbos.RunAsStep`:

```go
func fetchData(ctx context.Context) (string, error) {
	resp, err := http.Get("https://api.example.com/data")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	result, err := dbos.RunAsStep(ctx, fetchData, dbos.WithStepName("fetchData"))
	if err != nil {
		return "", err
	}
	return result, nil
}
```

### Key Constraints

- Do NOT start or enqueue workflows from within steps
- Do NOT use uncontrolled goroutines to start workflows - use `dbos.RunWorkflow` with queues or `dbos.Go`/`dbos.Select` for concurrent steps
- Workflows MUST be deterministic - non-deterministic operations go in steps
- Do NOT modify global variables from workflows or steps
- All workflows and queues MUST be registered before calling `Launch()`

## How to Use

Read individual rule files for detailed explanations and examples:

```
references/lifecycle-config.md
references/workflow-determinism.md
references/queue-concurrency.md
```

## References

- https://docs.dbos.dev/
- https://github.com/dbos-inc/dbos-transact-golang

---

## Reference: _Sections

# Section Definitions

This file defines the rule categories for DBOS Go best practices. Rules are automatically assigned to sections based on their filename prefix.

---

## 1. Lifecycle (lifecycle)
**Impact:** CRITICAL
**Description:** DBOS configuration, initialization, and launch patterns. Foundation for all DBOS applications.

## 2. Workflow (workflow)
**Impact:** CRITICAL
**Description:** Workflow creation, determinism requirements, background execution, and workflow IDs.

## 3. Step (step)
**Impact:** HIGH
**Description:** Step creation, retries, concurrent steps with Go/Select, and when to use steps vs workflows.

## 4. Queue (queue)
**Impact:** HIGH
**Description:** Queue creation, concurrency limits, rate limiting, partitioning, and priority.

## 5. Communication (comm)
**Impact:** MEDIUM
**Description:** Workflow events, messages, and streaming for inter-workflow communication.

## 6. Pattern (pattern)
**Impact:** MEDIUM
**Description:** Common patterns including idempotency, scheduled workflows, debouncing, and durable sleep.

## 7. Testing (test)
**Impact:** LOW-MEDIUM
**Description:** Testing DBOS applications with Go's testing package, mocks, and integration test setup.

## 8. Client (client)
**Impact:** MEDIUM
**Description:** DBOS Client for interacting with DBOS from external applications.

## 9. Advanced (advanced)
**Impact:** LOW
**Description:** Workflow versioning, patching, and safe code upgrades.

---

## Reference: Advanced Patching

## Use Patching for Safe Workflow Upgrades

Use `dbos.Patch` to safely deploy breaking changes to workflow code. Breaking changes alter which steps run or their order, which can cause recovery failures.

**Incorrect (breaking change without patching):**

```go
// BEFORE: original workflow
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	result, _ := dbos.RunAsStep(ctx, foo, dbos.WithStepName("foo"))
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}

// AFTER: breaking change - recovery will fail for in-progress workflows!
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	result, _ := dbos.RunAsStep(ctx, baz, dbos.WithStepName("baz")) // Changed step
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}
```

**Correct (using patch):**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	useBaz, err := dbos.Patch(ctx, "use-baz")
	if err != nil {
		return "", err
	}
	var result string
	if useBaz {
		result, _ = dbos.RunAsStep(ctx, baz, dbos.WithStepName("baz")) // New workflows
	} else {
		result, _ = dbos.RunAsStep(ctx, foo, dbos.WithStepName("foo")) // Old workflows
	}
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}
```

`dbos.Patch` returns `true` for new workflows and `false` for workflows that started before the patch.

**Deprecating patches (after all old workflows complete):**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	dbos.DeprecatePatch(ctx, "use-baz") // Always takes the new path
	result, _ := dbos.RunAsStep(ctx, baz, dbos.WithStepName("baz"))
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}
```

**Removing patches (after all workflows using DeprecatePatch complete):**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	result, _ := dbos.RunAsStep(ctx, baz, dbos.WithStepName("baz"))
	_, _ = dbos.RunAsStep(ctx, bar, dbos.WithStepName("bar"))
	return result, nil
}
```

Lifecycle: `Patch()` → deploy → wait for old workflows → `DeprecatePatch()` → deploy → wait → remove patch entirely.

**Required configuration** — patching must be explicitly enabled:

```go
ctx, _ := dbos.NewDBOSContext(context.Background(), dbos.Config{
	AppName:        "my-app",
	DatabaseURL:    os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	EnablePatching: true, // Required for dbos.Patch and dbos.DeprecatePatch
})
```

Without `EnablePatching: true`, calls to `dbos.Patch` and `dbos.DeprecatePatch` will fail.

Reference: [Patching](https://docs.dbos.dev/golang/tutorials/upgrading-workflows#patching)

---

## Reference: Advanced Versioning

## Use Versioning for Blue-Green Deployments

Set `ApplicationVersion` in configuration to tag workflows with a version. DBOS only recovers workflows matching the current application version, preventing code mismatches during recovery.

**Incorrect (deploying new code that breaks in-progress workflows):**

```go
ctx, _ := dbos.NewDBOSContext(context.Background(), dbos.Config{
	AppName:     "my-app",
	DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	// No version set - version auto-computed from binary hash
	// Old workflows will be recovered with new code, which may break
})
```

**Correct (versioned deployment):**

```go
ctx, _ := dbos.NewDBOSContext(context.Background(), dbos.Config{
	AppName:            "my-app",
	DatabaseURL:        os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	ApplicationVersion: "2.0.0",
})
```

By default, the application version is automatically computed from a SHA-256 hash of the executable binary. Set it explicitly for more control.

**Blue-green deployment strategy:**

1. Deploy new version (v2) alongside old version (v1)
2. Direct new traffic to v2 processes
3. Let v1 processes "drain" (complete in-progress workflows)
4. Check for remaining v1 workflows:

```go
oldWorkflows, _ := dbos.ListWorkflows(ctx,
	dbos.WithAppVersion("1.0.0"),
	dbos.WithStatus([]dbos.WorkflowStatusType{dbos.WorkflowStatusPending}),
)
```

5. Once all v1 workflows are complete, retire v1 processes

**Fork to new version (for stuck workflows):**

```go
// Fork a workflow from a failed step to run on the new version
handle, _ := dbos.ForkWorkflowstring
```

Reference: [Versioning](https://docs.dbos.dev/golang/tutorials/upgrading-workflows#versioning)

---

## Reference: Client Enqueue

## Enqueue Workflows from External Applications

Use `client.Enqueue()` to submit workflows from outside your DBOS application. Since the Client runs externally, workflow and queue metadata must be specified explicitly by name.

**Incorrect (trying to use RunWorkflow from external code):**

```go
// RunWorkflow requires a full DBOS context with registered workflows
dbos.RunWorkflow(ctx, processTask, "data", dbos.WithQueue("myQueue"))
```

**Correct (using Client.Enqueue):**

```go
client, err := dbos.NewClient(context.Background(), dbos.ClientConfig{
	DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
})
if err != nil {
	log.Fatal(err)
}
defer client.Shutdown(10 * time.Second)

// Basic enqueue - specify workflow and queue by name
handle, err := client.Enqueue("task_queue", "processTask", "task-data")
if err != nil {
	log.Fatal(err)
}

// Wait for the result
result, err := handle.GetResult()
```

**Enqueue with options:**

```go
handle, err := client.Enqueue("task_queue", "processTask", "task-data",
	dbos.WithEnqueueWorkflowID("custom-id"),
	dbos.WithEnqueueDeduplicationID("unique-id"),
	dbos.WithEnqueuePriority(10),
	dbos.WithEnqueueTimeout(5*time.Minute),
	dbos.WithEnqueueQueuePartitionKey("user-123"),
	dbos.WithEnqueueApplicationVersion("2.0.0"),
)
```

Enqueue options:
- `WithEnqueueWorkflowID`: Custom workflow ID
- `WithEnqueueDeduplicationID`: Prevent duplicate enqueues
- `WithEnqueuePriority`: Queue priority (lower = higher priority)
- `WithEnqueueTimeout`: Workflow timeout
- `WithEnqueueQueuePartitionKey`: Partition key for partitioned queues
- `WithEnqueueApplicationVersion`: Override application version

The workflow name must match the registered name or custom name set with `WithWorkflowName` during registration.

Always call `client.Shutdown()` when done.

Reference: [DBOS Client Enqueue](https://docs.dbos.dev/golang/reference/client#enqueue)

---

## Reference: Client Setup

## Initialize Client for External Access

Use `dbos.NewClient` to interact with DBOS from external applications like API servers, CLI tools, or separate services. The Client connects directly to the DBOS system database.

**Incorrect (using full DBOS context from an external app):**

```go
// Full DBOS context requires Launch() - too heavy for external clients
ctx, _ := dbos.NewDBOSContext(context.Background(), config)
dbos.Launch(ctx)
```

**Correct (using Client):**

```go
client, err := dbos.NewClient(context.Background(), dbos.ClientConfig{
	DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
})
if err != nil {
	log.Fatal(err)
}
defer client.Shutdown(10 * time.Second)

// Send a message to a workflow
err = client.Send(workflowID, "notification", "topic")

// Get an event from a workflow
event, err := client.GetEvent(workflowID, "status", 60*time.Second)

// Retrieve a workflow handle
handle, err := client.RetrieveWorkflow(workflowID)
result, err := handle.GetResult()

// List workflows
workflows, err := client.ListWorkflows(
	dbos.WithStatus([]dbos.WorkflowStatusType{dbos.WorkflowStatusError}),
)

// Workflow management
err = client.CancelWorkflow(workflowID)
handle, err = client.ResumeWorkflow(workflowID)

// Read a stream
values, closed, err := client.ClientReadStream(workflowID, "results")

// Read a stream asynchronously
ch, err := client.ClientReadStreamAsync(workflowID, "results")
```

ClientConfig options:
- `DatabaseURL` (required unless `SystemDBPool` is set): PostgreSQL connection string
- `SystemDBPool`: Custom `*pgxpool.Pool`
- `DatabaseSchema`: Schema name (default: `"dbos"`)
- `Logger`: Custom `*slog.Logger`

Always call `client.Shutdown()` when done.

Reference: [DBOS Client](https://docs.dbos.dev/golang/reference/client)

---

## Reference: Comm Events

## Use Events for Workflow Status Publishing

Workflows can publish events (key-value pairs) with `dbos.SetEvent`. Other code can read events with `dbos.GetEvent`. Events are persisted and useful for real-time progress monitoring.

**Incorrect (using external state for progress):**

```go
var progress int // Global variable - not durable!

func processData(ctx dbos.DBOSContext, input string) (string, error) {
	progress = 50 // Not persisted, lost on restart
	return input, nil
}
```

**Correct (using events):**

```go
func processData(ctx dbos.DBOSContext, input string) (string, error) {
	dbos.SetEvent(ctx, "status", "processing")
	_, err := dbos.RunAsStep(ctx, stepOne, dbos.WithStepName("stepOne"))
	if err != nil {
		return "", err
	}
	dbos.SetEvent(ctx, "progress", 50)
	_, err = dbos.RunAsStep(ctx, stepTwo, dbos.WithStepName("stepTwo"))
	if err != nil {
		return "", err
	}
	dbos.SetEvent(ctx, "progress", 100)
	dbos.SetEvent(ctx, "status", "complete")
	return "done", nil
}

// Read events from outside the workflow
status, err := dbos.GetEventstring
progress, err := dbos.GetEventint
```

Events are useful for interactive workflows. For example, a checkout workflow can publish a payment URL for the caller to redirect to:

```go
func checkoutWorkflow(ctx dbos.DBOSContext, order Order) (string, error) {
	paymentURL, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return createPayment(order)
	}, dbos.WithStepName("createPayment"))
	if err != nil {
		return "", err
	}
	dbos.SetEvent(ctx, "paymentURL", paymentURL)
	// Continue processing...
	return "success", nil
}

// HTTP handler starts workflow and reads the payment URL
handle, _ := dbos.RunWorkflow(ctx, checkoutWorkflow, order)
url, _ := dbos.GetEventstring, "paymentURL", 300*time.Second)
```

`GetEvent` blocks until the event is set or the timeout expires. It returns the zero value of the type if the timeout is reached.

Reference: [Workflow Events](https://docs.dbos.dev/golang/tutorials/workflow-communication#workflow-events)

---

## Reference: Comm Messages

## Use Messages for Workflow Notifications

Use `dbos.Send` to send messages to a workflow and `dbos.Recv` to receive them. Messages are queued per topic and persisted for reliable delivery.

**Incorrect (using external messaging for workflow communication):**

```go
// External message queue is not integrated with workflow recovery
ch := make(chan string) // Not durable!
```

**Correct (using DBOS messages):**

```go
func checkoutWorkflow(ctx dbos.DBOSContext, orderID string) (string, error) {
	// Wait for payment notification (timeout 120 seconds)
	notification, err := dbos.Recvstring
	if err != nil {
		return "", err
	}

	if notification == "paid" {
		_, err = dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
			return fulfillOrder(orderID)
		}, dbos.WithStepName("fulfillOrder"))
		return "fulfilled", err
	}
	_, err = dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return cancelOrder(orderID)
	}, dbos.WithStepName("cancelOrder"))
	return "cancelled", err
}

// Send a message from a webhook handler
func paymentWebhook(ctx dbos.DBOSContext, workflowID, status string) error {
	return dbos.Send(ctx, workflowID, status, "payment_status")
}
```

Key behaviors:
- `Recv` waits for and consumes the next message for the specified topic
- Returns the zero value if the wait times out, with a `DBOSError` with code `TimeoutError`
- Messages without a topic can only be received by `Recv` without a topic
- Messages are queued per-topic (FIFO)

**Reliability guarantees:**
- All messages are persisted to the database
- Messages sent from workflows are delivered exactly-once

Reference: [Workflow Messaging and Notifications](https://docs.dbos.dev/golang/tutorials/workflow-communication#workflow-messaging-and-notifications)

---

## Reference: Comm Streaming

## Use Streams for Real-Time Data

Workflows can stream data to clients in real-time using `dbos.WriteStream`, `dbos.CloseStream`, and `dbos.ReadStream`/`dbos.ReadStreamAsync`. Useful for LLM output streaming or progress reporting.

**Incorrect (accumulating results then returning at end):**

```go
func processWorkflow(ctx dbos.DBOSContext, items []string) ([]string, error) {
	var results []string
	for _, item := range items {
		result, _ := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
			return processItem(item)
		}, dbos.WithStepName("process"))
		results = append(results, result)
	}
	return results, nil // Client must wait for entire workflow to complete
}
```

**Correct (streaming results as they become available):**

```go
func processWorkflow(ctx dbos.DBOSContext, items []string) (string, error) {
	for _, item := range items {
		result, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
			return processItem(item)
		}, dbos.WithStepName("process"))
		if err != nil {
			return "", err
		}
		dbos.WriteStream(ctx, "results", result)
	}
	dbos.CloseStream(ctx, "results") // Signal completion
	return "done", nil
}

// Read the stream synchronously (blocks until closed)
handle, _ := dbos.RunWorkflow(ctx, processWorkflow, items)
values, closed, err := dbos.ReadStreamstring, "results")
```

**Async stream reading with channels:**

```go
ch, err := dbos.ReadStreamAsyncstring, "results")
if err != nil {
	log.Fatal(err)
}
for sv := range ch {
	if sv.Err != nil {
		log.Fatal(sv.Err)
	}
	if sv.Closed {
		break
	}
	fmt.Println("Received:", sv.Value)
}
```

Key behaviors:
- A workflow may have any number of streams, each identified by a unique key
- Streams are immutable and append-only
- Writes from workflows happen exactly-once
- Streams are automatically closed when the workflow terminates
- `ReadStream` blocks until the workflow is inactive or the stream is closed
- `ReadStreamAsync` returns a channel of `StreamValue[R]` for non-blocking reads

Reference: [Workflow Streaming](https://docs.dbos.dev/golang/tutorials/workflow-communication#workflow-streaming)

---

## Reference: Lifecycle Config

## Configure and Launch DBOS Properly

Every DBOS application must create a context, register workflows and queues, then launch before running any workflows.

**Incorrect (missing configuration or launch):**

```go
// No context or launch!
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	return input, nil
}

func main() {
	// This will fail - DBOS is not initialized or launched
	dbos.RegisterWorkflow(nil, myWorkflow) // panic: ctx cannot be nil
}
```

**Correct (create context, register, launch):**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	return input, nil
}

func main() {
	ctx, err := dbos.NewDBOSContext(context.Background(), dbos.Config{
		AppName:     "my-app",
		DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	})
	if err != nil {
		log.Fatal(err)
	}
	defer dbos.Shutdown(ctx, 30*time.Second)

	dbos.RegisterWorkflow(ctx, myWorkflow)

	if err := dbos.Launch(ctx); err != nil {
		log.Fatal(err)
	}

	handle, err := dbos.RunWorkflow(ctx, myWorkflow, "hello")
	if err != nil {
		log.Fatal(err)
	}
	result, err := handle.GetResult()
	fmt.Println(result) // "hello"
}
```

Config fields:
- `AppName` (required): Application identifier
- `DatabaseURL` (required unless `SystemDBPool` is set): PostgreSQL connection string
- `SystemDBPool`: Custom `*pgxpool.Pool` (takes precedence over `DatabaseURL`)
- `DatabaseSchema`: Schema name (default: `"dbos"`)
- `Logger`: Custom `*slog.Logger` (defaults to stdout)
- `AdminServer`: Enable HTTP admin server (default: `false`)
- `AdminServerPort`: Admin server port (default: `3001`)
- `ApplicationVersion`: App version (auto-computed from binary hash if not set)
- `ExecutorID`: Executor identifier (default: `"local"`)
- `EnablePatching`: Enable code patching system (default: `false`)

Reference: [Integrating DBOS](https://docs.dbos.dev/golang/integrating-dbos)

---

## Reference: Pattern Debouncing

## Debounce Workflows to Prevent Wasted Work

Use `dbos.NewDebouncer` to delay workflow execution until some time has passed since the last trigger. This prevents wasted work when a workflow is triggered multiple times in quick succession.

**Incorrect (executing on every trigger):**

```go
// Every keystroke triggers a new workflow - wasteful!
func onInputChange(ctx dbos.DBOSContext, userInput string) {
	dbos.RunWorkflow(ctx, processInput, userInput)
}
```

**Correct (using Debouncer):**

```go
// Create debouncer before Launch()
debouncer := dbos.NewDebouncer(ctx, processInput,
	dbos.WithDebouncerTimeout(120*time.Second), // Max wait: 2 minutes
)

func onInputChange(ctx dbos.DBOSContext, userID, userInput string) error {
	// Delays execution by 60 seconds from the last call
	// Uses the LAST set of inputs when finally executing
	_, err := debouncer.Debounce(ctx, userID, 60*time.Second, userInput)
	return err
}
```

Key behaviors:
- First argument to `Debounce` is the debounce key, grouping executions together (e.g., per user)
- Second argument is the delay duration from the last call
- `WithDebouncerTimeout` sets a max wait time since the first trigger
- When the workflow finally executes, it uses the **last** set of inputs
- After execution begins, the next `Debounce` call starts a new cycle
- Debouncers must be created **before** `Launch()`

Type signature: `Debouncer[P any, R any]` — the type parameters match the target workflow.

Reference: [Debouncing Workflows](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#debouncing)

---

## Reference: Pattern Idempotency

## Use Workflow IDs for Idempotency

Assign a workflow ID to ensure a workflow executes only once, even if called multiple times. This prevents duplicate side effects like double payments.

**Incorrect (no idempotency):**

```go
func processPayment(ctx dbos.DBOSContext, orderID string) (string, error) {
	_, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return chargeCard(orderID)
	}, dbos.WithStepName("chargeCard"))
	return "charged", err
}

// Multiple calls could charge the card multiple times!
dbos.RunWorkflow(ctx, processPayment, "order-123")
dbos.RunWorkflow(ctx, processPayment, "order-123") // Double charge!
```

**Correct (with workflow ID):**

```go
func processPayment(ctx dbos.DBOSContext, orderID string) (string, error) {
	_, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return chargeCard(orderID)
	}, dbos.WithStepName("chargeCard"))
	return "charged", err
}

// Same workflow ID = only one execution
workflowID := fmt.Sprintf("payment-%s", orderID)
dbos.RunWorkflow(ctx, processPayment, "order-123",
	dbos.WithWorkflowID(workflowID),
)
dbos.RunWorkflow(ctx, processPayment, "order-123",
	dbos.WithWorkflowID(workflowID),
)
// Second call returns the result of the first execution
```

Access the current workflow ID inside a workflow:

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	currentID, err := dbos.GetWorkflowID(ctx)
	if err != nil {
		return "", err
	}
	fmt.Printf("Running workflow: %s\n", currentID)
	return input, nil
}
```

Workflow IDs must be **globally unique** for your application. If not set, a random UUID is generated.

Reference: [Workflow IDs and Idempotency](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#workflow-ids-and-idempotency)

---

## Reference: Pattern Scheduled

## Create Scheduled Workflows

Use `dbos.WithSchedule` when registering a workflow to run it on a cron schedule. Each scheduled invocation runs exactly once per interval.

**Incorrect (manual scheduling with goroutine):**

```go
// Manual scheduling is not durable and misses intervals during downtime
go func() {
	for {
		generateReport()
		time.Sleep(60 * time.Second)
	}
}()
```

**Correct (using WithSchedule):**

```go
// Scheduled workflow must accept time.Time as input
func everyThirtySeconds(ctx dbos.DBOSContext, scheduledTime time.Time) (string, error) {
	fmt.Println("Running scheduled task at:", scheduledTime)
	return "done", nil
}

func dailyReport(ctx dbos.DBOSContext, scheduledTime time.Time) (string, error) {
	_, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		return generateReport()
	}, dbos.WithStepName("generateReport"))
	return "report generated", err
}

func main() {
	ctx, _ := dbos.NewDBOSContext(context.Background(), config)
	defer dbos.Shutdown(ctx, 30*time.Second)

	dbos.RegisterWorkflow(ctx, everyThirtySeconds,
		dbos.WithSchedule("*/30 * * * * *"),
	)
	dbos.RegisterWorkflow(ctx, dailyReport,
		dbos.WithSchedule("0 0 9 * * *"), // 9 AM daily
	)

	dbos.Launch(ctx)
	select {} // Block forever
}
```

Scheduled workflows must accept exactly one parameter of type `time.Time` representing the scheduled execution time.

DBOS crontab uses 6 fields with second precision:
```text
┌────────────── second
│ ┌──────────── minute
│ │ ┌────────── hour
│ │ │ ┌──────── day of month
│ │ │ │ ┌────── month
│ │ │ │ │ ┌──── day of week
* * * * * *
```

Reference: [Scheduled Workflows](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#scheduled-workflows)

---

## Reference: Pattern Sleep

## Use Durable Sleep for Delayed Execution

Use `dbos.Sleep` for durable delays within workflows. The wakeup time is stored in the database, so the sleep survives restarts.

**Incorrect (non-durable sleep):**

```go
func delayedTask(ctx dbos.DBOSContext, input string) (string, error) {
	// time.Sleep is not durable - lost on restart!
	time.Sleep(60 * time.Second)
	result, err := dbos.RunAsStep(ctx, doWork, dbos.WithStepName("doWork"))
	return result, err
}
```

**Correct (durable sleep):**

```go
func delayedTask(ctx dbos.DBOSContext, input string) (string, error) {
	// Durable sleep - survives restarts
	_, err := dbos.Sleep(ctx, 60*time.Second)
	if err != nil {
		return "", err
	}
	result, err := dbos.RunAsStep(ctx, doWork, dbos.WithStepName("doWork"))
	return result, err
}
```

`dbos.Sleep` takes a `time.Duration`. It returns the remaining sleep duration (zero if completed normally).

Use cases:
- Scheduling tasks to run in the future
- Implementing retry delays
- Delays spanning hours, days, or weeks

```go
func scheduledTask(ctx dbos.DBOSContext, task string) (string, error) {
	// Sleep for one week
	dbos.Sleep(ctx, 7*24*time.Hour)
	return processTask(task)
}
```

Reference: [Durable Sleep](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#durable-sleep)

---

## Reference: Queue Basics

## Use Queues for Concurrent Workflows

Queues run many workflows concurrently with managed flow control. Use them when you need to control how many workflows run at once.

**Incorrect (uncontrolled concurrency):**

```go
// Starting many workflows without control - could overwhelm resources
for _, task := range tasks {
	dbos.RunWorkflow(ctx, processTask, task)
}
```

**Correct (using a queue):**

```go
// Create queue before Launch()
queue := dbos.NewWorkflowQueue(ctx, "task_queue")

func processAllTasks(ctx dbos.DBOSContext, tasks []string) ([]string, error) {
	var handles []dbos.WorkflowHandle[string]
	for _, task := range tasks {
		handle, err := dbos.RunWorkflow(ctx, processTask, task,
			dbos.WithQueue(queue.Name),
		)
		if err != nil {
			return nil, err
		}
		handles = append(handles, handle)
	}
	// Wait for all tasks
	var results []string
	for _, h := range handles {
		result, err := h.GetResult()
		if err != nil {
			return nil, err
		}
		results = append(results, result)
	}
	return results, nil
}
```

Queues process workflows in FIFO order. All queues must be created with `dbos.NewWorkflowQueue` before `Launch()`.

Reference: [DBOS Queues](https://docs.dbos.dev/golang/tutorials/queue-tutorial)

---

## Reference: Queue Concurrency

## Control Queue Concurrency

Queues support worker-level and global concurrency limits to prevent resource exhaustion.

**Incorrect (no concurrency control):**

```go
queue := dbos.NewWorkflowQueue(ctx, "heavy_tasks") // No limits - could exhaust memory
```

**Correct (worker concurrency):**

```go
// Each process runs at most 5 tasks from this queue
queue := dbos.NewWorkflowQueue(ctx, "heavy_tasks",
	dbos.WithWorkerConcurrency(5),
)
```

**Correct (global concurrency):**

```go
// At most 10 tasks run across ALL processes
queue := dbos.NewWorkflowQueue(ctx, "limited_tasks",
	dbos.WithGlobalConcurrency(10),
)
```

**In-order processing (sequential):**

```go
// Only one task at a time - guarantees order
serialQueue := dbos.NewWorkflowQueue(ctx, "sequential_queue",
	dbos.WithGlobalConcurrency(1),
)
```

Worker concurrency is recommended for most use cases. Take care with global concurrency as any `PENDING` workflow on the queue counts toward the limit, including workflows from previous application versions.

When using worker concurrency, each process must have a unique `ExecutorID` set in configuration (this is automatic with DBOS Conductor or Cloud).

Reference: [Managing Concurrency](https://docs.dbos.dev/golang/tutorials/queue-tutorial#managing-concurrency)

---

## Reference: Queue Deduplication

## Deduplicate Queued Workflows

Set a deduplication ID when enqueuing to prevent duplicate workflow executions. If a workflow with the same deduplication ID is already enqueued or executing, a `DBOSError` with code `QueueDeduplicated` is returned.

**Incorrect (no deduplication):**

```go
// Multiple calls could enqueue duplicates
func handleClick(ctx dbos.DBOSContext, userID, task string) error {
	_, err := dbos.RunWorkflow(ctx, processTask, task,
		dbos.WithQueue(queue.Name),
	)
	return err
}
```

**Correct (with deduplication):**

```go
func handleClick(ctx dbos.DBOSContext, userID, task string) error {
	_, err := dbos.RunWorkflow(ctx, processTask, task,
		dbos.WithQueue(queue.Name),
		dbos.WithDeduplicationID(userID),
	)
	if err != nil {
		// Check if it was deduplicated
		var dbosErr *dbos.DBOSError
		if errors.As(err, &dbosErr) && dbosErr.Code == dbos.QueueDeduplicated {
			fmt.Println("Task already in progress for user:", userID)
			return nil
		}
		return err
	}
	return nil
}
```

Deduplication is per-queue. The deduplication ID is active while the workflow has status `ENQUEUED` or `PENDING`. Once the workflow completes, a new workflow with the same deduplication ID can be enqueued.

This is useful for:
- Ensuring one active task per user
- Preventing duplicate form submissions
- Idempotent event processing

Reference: [Deduplication](https://docs.dbos.dev/golang/tutorials/queue-tutorial#deduplication)

---

## Reference: Queue Listening

## Control Which Queues a Worker Listens To

Use `ListenQueues` to make a process only dequeue from specific queues. This enables heterogeneous worker pools.

**Incorrect (all workers process all queues):**

```go
cpuQueue := dbos.NewWorkflowQueue(ctx, "cpu_queue")
gpuQueue := dbos.NewWorkflowQueue(ctx, "gpu_queue")

// Every worker processes both CPU and GPU tasks
// GPU tasks on CPU workers will fail or be slow!
dbos.Launch(ctx)
```

**Correct (selective queue listening):**

```go
cpuQueue := dbos.NewWorkflowQueue(ctx, "cpu_queue")
gpuQueue := dbos.NewWorkflowQueue(ctx, "gpu_queue")

workerType := os.Getenv("WORKER_TYPE") // "cpu" or "gpu"

if workerType == "gpu" {
	ctx.ListenQueues(ctx, gpuQueue)
} else if workerType == "cpu" {
	ctx.ListenQueues(ctx, cpuQueue)
}

dbos.Launch(ctx)
```

`ListenQueues` only controls dequeuing. A CPU worker can still enqueue tasks onto the GPU queue:

```go
// From a CPU worker, enqueue onto the GPU queue
dbos.RunWorkflow(ctx, gpuTask, "data",
	dbos.WithQueue(gpuQueue.Name),
)
```

Reference: [Listening to Specific Queues](https://docs.dbos.dev/golang/tutorials/queue-tutorial#listening-to-specific-queues)

---

## Reference: Queue Partitioning

## Partition Queues for Per-Entity Limits

Partitioned queues apply flow control limits per partition key instead of the entire queue. Each partition acts as a dynamic "subqueue".

**Incorrect (global concurrency for per-user limits):**

```go
// Global concurrency=1 blocks ALL users, not per-user
queue := dbos.NewWorkflowQueue(ctx, "tasks",
	dbos.WithGlobalConcurrency(1),
)
```

**Correct (partitioned queue):**

```go
queue := dbos.NewWorkflowQueue(ctx, "tasks",
	dbos.WithPartitionQueue(),
	dbos.WithGlobalConcurrency(1),
)

func onUserTask(ctx dbos.DBOSContext, userID, task string) error {
	// Each user gets their own partition - at most 1 task per user
	// but tasks from different users can run concurrently
	_, err := dbos.RunWorkflow(ctx, processTask, task,
		dbos.WithQueue(queue.Name),
		dbos.WithQueuePartitionKey(userID),
	)
	return err
}
```

When a queue has `WithPartitionQueue()` enabled, you **must** provide a `WithQueuePartitionKey()` when enqueuing. Partition keys and deduplication IDs cannot be used together.

Reference: [Partitioning Queues](https://docs.dbos.dev/golang/tutorials/queue-tutorial#partitioning-queues)

---

## Reference: Queue Priority

## Set Queue Priority for Workflows

Enable priority on a queue to process higher-priority workflows first. Lower numbers indicate higher priority.

**Incorrect (no priority - FIFO only):**

```go
queue := dbos.NewWorkflowQueue(ctx, "tasks")
// All tasks processed in FIFO order regardless of importance
```

**Correct (priority-enabled queue):**

```go
queue := dbos.NewWorkflowQueue(ctx, "tasks",
	dbos.WithPriorityEnabled(),
)

// High priority task (lower number = higher priority)
dbos.RunWorkflow(ctx, processTask, "urgent-task",
	dbos.WithQueue(queue.Name),
	dbos.WithPriority(1),
)

// Low priority task
dbos.RunWorkflow(ctx, processTask, "background-task",
	dbos.WithQueue(queue.Name),
	dbos.WithPriority(100),
)
```

Priority rules:
- Range: `1` to `2,147,483,647`
- Lower number = higher priority
- Workflows **without** assigned priorities have the highest priority (run first)
- Workflows with the same priority are dequeued in FIFO order

Reference: [Priority](https://docs.dbos.dev/golang/tutorials/queue-tutorial#priority)

---

## Reference: Queue Rate Limiting

## Rate Limit Queue Execution

Set rate limits on a queue to control how many workflows start in a given period. Rate limits are global across all DBOS processes.

**Incorrect (no rate limiting):**

```go
queue := dbos.NewWorkflowQueue(ctx, "llm_tasks")
// Could send hundreds of requests per second to a rate-limited API
```

**Correct (rate-limited queue):**

```go
queue := dbos.NewWorkflowQueue(ctx, "llm_tasks",
	dbos.WithRateLimiter(&dbos.RateLimiter{
		Limit:  50,
		Period: 30 * time.Second,
	}),
)
```

This queue starts at most 50 workflows per 30 seconds.

**Combining rate limiting with concurrency:**

```go
// At most 5 concurrent and 50 per 30 seconds
queue := dbos.NewWorkflowQueue(ctx, "api_tasks",
	dbos.WithWorkerConcurrency(5),
	dbos.WithRateLimiter(&dbos.RateLimiter{
		Limit:  50,
		Period: 30 * time.Second,
	}),
)
```

Common use cases:
- LLM API rate limiting (OpenAI, Anthropic, etc.)
- Third-party API throttling
- Preventing database overload

Reference: [Rate Limiting](https://docs.dbos.dev/golang/tutorials/queue-tutorial#rate-limiting)

---

## Reference: Step Basics

## Use Steps for External Operations

Any function that performs complex operations, accesses external APIs, or has side effects should be a step. Step results are checkpointed, enabling workflow recovery.

**Incorrect (external call in workflow):**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// External API call directly in workflow - not checkpointed!
	resp, err := http.Get("https://api.example.com/data")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}
```

**Correct (external call in step using `dbos.RunAsStep`):**

```go
func fetchData(ctx context.Context) (string, error) {
	resp, err := http.Get("https://api.example.com/data")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	data, err := dbos.RunAsStep(ctx, fetchData, dbos.WithStepName("fetchData"))
	if err != nil {
		return "", err
	}
	return data, nil
}
```

`dbos.RunAsStep` can also accept an inline closure:

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	data, err := dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		resp, err := http.Get("https://api.example.com/data")
		if err != nil {
			return "", err
		}
		defer resp.Body.Close()
		body, _ := io.ReadAll(resp.Body)
		return string(body), nil
	}, dbos.WithStepName("fetchData"))
	return data, err
}
```

Step type signature: `type Step[R any] func(ctx context.Context) (R, error)`

Step requirements:
- The function must accept a `context.Context` parameter — use the one provided, not the workflow's context
- Inputs and outputs must be serializable to JSON
- Cannot start or enqueue workflows from within steps
- Calling a step from within another step makes the inner call part of the outer step's execution

When to use steps:
- API calls to external services
- File system operations
- Random number generation
- Getting current time
- Any non-deterministic operation

Reference: [DBOS Steps](https://docs.dbos.dev/golang/tutorials/step-tutorial)

---

## Reference: Step Concurrency

## Run Concurrent Steps with Go and Select

Use `dbos.Go` to run steps concurrently in goroutines and `dbos.Select` to durably select the first completed result. Both operations are checkpointed for recovery.

**Incorrect (raw goroutines without checkpointing):**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// Raw goroutines are not checkpointed - recovery breaks!
	ch := make(chan string, 2)
	go func() { ch <- callAPI1() }()
	go func() { ch <- callAPI2() }()
	return <-ch, nil
}
```

**Correct (using dbos.Go for concurrent steps):**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// Start steps concurrently
	ch1, err := dbos.Go(ctx, func(ctx context.Context) (string, error) {
		return callAPI1(ctx)
	}, dbos.WithStepName("api1"))
	if err != nil {
		return "", err
	}

	ch2, err := dbos.Go(ctx, func(ctx context.Context) (string, error) {
		return callAPI2(ctx)
	}, dbos.WithStepName("api2"))
	if err != nil {
		return "", err
	}

	// Wait for the first result (durable select)
	result, err := dbos.Select(ctx, []<-chan dbos.StepOutcome[string]{ch1, ch2})
	if err != nil {
		return "", err
	}
	return result, nil
}
```

**Waiting for all concurrent steps:**

```go
func myWorkflow(ctx dbos.DBOSContext, input string) ([]string, error) {
	ch1, _ := dbos.Go(ctx, step1, dbos.WithStepName("step1"))
	ch2, _ := dbos.Go(ctx, step2, dbos.WithStepName("step2"))
	ch3, _ := dbos.Go(ctx, step3, dbos.WithStepName("step3"))

	// Collect all results
	results := make([]string, 3)
	for i, ch := range []<-chan dbos.StepOutcome[string]{ch1, ch2, ch3} {
		outcome := <-ch
		if outcome.Err != nil {
			return nil, outcome.Err
		}
		results[i] = outcome.Result
	}
	return results, nil
}
```

Key behaviors:
- `dbos.Go` starts a step in a goroutine and returns a channel of `StepOutcome[R]`
- `dbos.Select` durably selects the first completed result and checkpoints which channel was selected
- On recovery, `Select` replays the same selection, maintaining determinism
- Steps started with `Go` follow the same retry and checkpointing rules as `RunAsStep`

Reference: [Concurrent Steps](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#concurrent-steps)

---

## Reference: Step Retries

## Configure Step Retries for Transient Failures

Steps can automatically retry on failure with exponential backoff. This handles transient failures like network issues.

**Incorrect (manual retry logic):**

```go
func fetchData(ctx context.Context) (string, error) {
	var lastErr error
	for attempt := 0; attempt < 3; attempt++ {
		resp, err := http.Get("https://api.example.com")
		if err == nil {
			defer resp.Body.Close()
			body, _ := io.ReadAll(resp.Body)
			return string(body), nil
		}
		lastErr = err
		time.Sleep(time.Duration(math.Pow(2, float64(attempt))) * time.Second)
	}
	return "", lastErr
}
```

**Correct (built-in retries with `dbos.RunAsStep`):**

```go
func fetchData(ctx context.Context) (string, error) {
	resp, err := http.Get("https://api.example.com")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	data, err := dbos.RunAsStep(ctx, fetchData,
		dbos.WithStepName("fetchData"),
		dbos.WithStepMaxRetries(10),
		dbos.WithBaseInterval(500*time.Millisecond),
		dbos.WithBackoffFactor(2.0),
		dbos.WithMaxInterval(5*time.Second),
	)
	return data, err
}
```

Retry parameters:
- `WithStepMaxRetries(n)`: Maximum retry attempts (default: `0` — no retries)
- `WithBaseInterval(d)`: Initial delay between retries (default: `100ms`)
- `WithBackoffFactor(f)`: Multiplier for exponential backoff (default: `2.0`)
- `WithMaxInterval(d)`: Maximum delay between retries (default: `5s`)

With defaults, retry delays are: 100ms, 200ms, 400ms, 800ms, 1.6s, 3.2s, 5s, 5s...

If all retries are exhausted, a `DBOSError` with code `MaxStepRetriesExceeded` is returned to the calling workflow.

Reference: [Configurable Retries](https://docs.dbos.dev/golang/tutorials/step-tutorial#configurable-retries)

---

## Reference: Test Setup

## Use Proper Test Setup for DBOS

DBOS applications can be tested with unit tests (mocking DBOSContext) or integration tests (real Postgres database).

**Incorrect (no lifecycle management between tests):**

```go
// Tests share state - results are inconsistent!
func TestOne(t *testing.T) {
	myWorkflow(ctx, "input")
}
func TestTwo(t *testing.T) {
	// Previous test's state leaks into this test
	myWorkflow(ctx, "input")
}
```

**Correct (unit testing with mocks):**

The `DBOSContext` interface is fully mockable. Use a mocking library like `testify/mock` or `mockery`:

```go
func TestWorkflow(t *testing.T) {
	mockCtx := mocks.NewMockDBOSContext(t)

	// Mock RunAsStep to return a canned value
	mockCtx.On("RunAsStep", mockCtx, mock.Anything, mock.Anything).
		Return("mock-result", nil)

	result, err := myWorkflow(mockCtx, "input")
	assert.NoError(t, err)
	assert.Equal(t, "expected", result)

	mockCtx.AssertExpectations(t)
}
```

**Correct (integration testing with Postgres):**

```go
func setupDBOS(t *testing.T) dbos.DBOSContext {
	t.Helper()
	databaseURL := os.Getenv("DBOS_TEST_DATABASE_URL")
	if databaseURL == "" {
		t.Skip("DBOS_TEST_DATABASE_URL not set")
	}

	ctx, err := dbos.NewDBOSContext(context.Background(), dbos.Config{
		AppName:     "test-" + t.Name(),
		DatabaseURL: databaseURL,
	})
	require.NoError(t, err)

	dbos.RegisterWorkflow(ctx, myWorkflow)

	err = dbos.Launch(ctx)
	require.NoError(t, err)

	t.Cleanup(func() {
		dbos.Shutdown(ctx, 10*time.Second)
	})
	return ctx
}

func TestWorkflowIntegration(t *testing.T) {
	ctx := setupDBOS(t)

	handle, err := dbos.RunWorkflow(ctx, myWorkflow, "test-input")
	require.NoError(t, err)

	result, err := handle.GetResult()
	require.NoError(t, err)
	assert.Equal(t, "expected-output", result)
}
```

Key points:
- Use `t.Cleanup` to ensure `Shutdown` is called after each test
- Use unique `AppName` per test to avoid collisions
- Mock `DBOSContext` for fast unit tests without Postgres
- Use real Postgres for integration tests that verify durable behavior

Reference: [Testing DBOS](https://docs.dbos.dev/golang/tutorials/testing)

---

## Reference: Workflow Background

## Start Workflows in Background

Use `dbos.RunWorkflow` to start a workflow and get a handle to track it. The workflow is guaranteed to run to completion even if the app is interrupted.

**Incorrect (no way to track background work):**

```go
func processData(ctx dbos.DBOSContext, data string) (string, error) {
	// ...
	return "processed: " + data, nil
}

// Fire and forget in a goroutine - no durability, no tracking
go func() {
	processData(ctx, data)
}()
```

**Correct (using RunWorkflow):**

```go
func processData(ctx dbos.DBOSContext, data string) (string, error) {
	return "processed: " + data, nil
}

func main() {
	// ... setup and launch ...

	// Start workflow, get handle
	handle, err := dbos.RunWorkflow(ctx, processData, "input")
	if err != nil {
		log.Fatal(err)
	}

	// Get the workflow ID
	fmt.Println(handle.GetWorkflowID())

	// Wait for result
	result, err := handle.GetResult()

	// Check status
	status, err := handle.GetStatus()
}
```

Retrieve a handle later by workflow ID:

```go
handle, err := dbos.RetrieveWorkflowstring
result, err := handle.GetResult()
```

`GetResult` supports options:
- `dbos.WithHandleTimeout(timeout)`: Return a timeout error if the workflow doesn't complete within the duration
- `dbos.WithHandlePollingInterval(interval)`: Control how often the database is polled for completion

Reference: [Workflows](https://docs.dbos.dev/golang/tutorials/workflow-tutorial)

---

## Reference: Workflow Constraints

## Follow Workflow Constraints

Workflows have specific constraints to maintain durability guarantees. Violating them can break recovery.

**Incorrect (starting workflows from steps):**

```go
func myStep(ctx context.Context) (string, error) {
	// Don't start workflows from steps!
	// The step's context.Context does not support workflow operations
	return "", nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// Starting a child workflow inside a step breaks determinism
	dbos.RunAsStep(ctx, func(ctx context.Context) (string, error) {
		handle, _ := dbos.RunWorkflow(ctx.(dbos.DBOSContext), otherWorkflow, "data") // WRONG
		return handle.GetWorkflowID(), nil
	})
	return "", nil
}
```

**Correct (workflow operations only from workflows):**

```go
func fetchData(ctx context.Context) (string, error) {
	// Steps only do external operations
	resp, err := http.Get("https://api.example.com")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	data, err := dbos.RunAsStep(ctx, fetchData, dbos.WithStepName("fetchData"))
	if err != nil {
		return "", err
	}
	// Start child workflows from the parent workflow
	handle, err := dbos.RunWorkflow(ctx, otherWorkflow, data)
	if err != nil {
		return "", err
	}
	// Receive messages from the workflow
	msg, err := dbos.Recvstring
	// Set events from the workflow
	dbos.SetEvent(ctx, "status", "done")
	return data, nil
}
```

Additional constraints:
- Don't modify global variables from workflows or steps
- All workflows and queues must be registered **before** `Launch()`
- Concurrent steps must start in deterministic order using `dbos.Go`/`dbos.Select`

Reference: [Workflow Guarantees](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#workflow-guarantees)

---

## Reference: Workflow Control

## Cancel, Resume, and Fork Workflows

DBOS provides functions to cancel, resume, and fork workflows for operational control.

**Incorrect (no way to handle stuck or failed workflows):**

```go
// Workflow is stuck or failed - no recovery mechanism
handle, _ := dbos.RunWorkflow(ctx, processTask, "data")
// If the workflow fails, there's no way to retry or recover
```

**Correct (using cancel, resume, and fork):**

```go
// Cancel a workflow - stops at its next step
err := dbos.CancelWorkflow(ctx, workflowID)

// Resume from the last completed step
handle, err := dbos.ResumeWorkflowstring
result, err := handle.GetResult()
```

Cancellation sets the workflow status to `CANCELLED` and preempts execution at the beginning of the next step. Cancelling also cancels all child workflows.

Resume restarts a workflow from its last completed step. Use this for workflows that are cancelled or have exceeded their maximum recovery attempts. You can also use this to start an enqueued workflow immediately, bypassing its queue.

Fork a workflow from a specific step:

```go
// List steps to find the right step ID
steps, err := dbos.GetWorkflowSteps(ctx, workflowID)

// Fork from a specific step
forkHandle, err := dbos.ForkWorkflowstring
result, err := forkHandle.GetResult()
```

Forking creates a new workflow with a new ID, copying the original workflow's inputs and step outputs up to the selected step.

Reference: [Workflow Management](https://docs.dbos.dev/golang/tutorials/workflow-management)

---

## Reference: Workflow Determinism

## Keep Workflows Deterministic

Workflow functions must be deterministic: given the same inputs and step return values, they must invoke the same steps in the same order. Non-deterministic operations must be moved to steps.

**Incorrect (non-deterministic workflow):**

```go
func exampleWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// Random value in workflow breaks recovery!
	// On replay, rand.Intn returns a different value,
	// so the workflow may take a different branch.
	if rand.Intn(2) == 0 {
		return stepOne(ctx)
	}
	return stepTwo(ctx)
}
```

**Correct (non-determinism in step):**

```go
func exampleWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	// Step result is checkpointed - replay uses the saved value
	choice, err := dbos.RunAsStep(ctx, func(ctx context.Context) (int, error) {
		return rand.Intn(2), nil
	}, dbos.WithStepName("generateChoice"))
	if err != nil {
		return "", err
	}
	if choice == 0 {
		return stepOne(ctx)
	}
	return stepTwo(ctx)
}
```

Non-deterministic operations that must be in steps:
- Random number generation
- Getting current time (`time.Now()`)
- Accessing external APIs (`http.Get`, etc.)
- Reading files
- Database queries

Reference: [Workflow Determinism](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#determinism)

---

## Reference: Workflow Introspection

## List and Inspect Workflows

Use `dbos.ListWorkflows` to query workflow executions by status, name, time range, and other criteria.

**Incorrect (no monitoring of workflow state):**

```go
// Start workflow with no way to check on it later
dbos.RunWorkflow(ctx, processTask, "data")
// If something goes wrong, no way to find or debug it
```

**Correct (listing and inspecting workflows):**

```go
// List workflows by status
erroredWorkflows, err := dbos.ListWorkflows(ctx,
	dbos.WithStatus([]dbos.WorkflowStatusType{dbos.WorkflowStatusError}),
)

for _, wf := range erroredWorkflows {
	fmt.Printf("Workflow %s: %s - %v\n", wf.ID, wf.Name, wf.Error)
}
```

List workflows with multiple filters:

```go
workflows, err := dbos.ListWorkflows(ctx,
	dbos.WithName("processOrder"),
	dbos.WithStatus([]dbos.WorkflowStatusType{dbos.WorkflowStatusSuccess}),
	dbos.WithLimit(100),
	dbos.WithSortDesc(),
	dbos.WithLoadOutput(true),
)
```

List workflow steps:

```go
steps, err := dbos.GetWorkflowSteps(ctx, workflowID)
for _, step := range steps {
	fmt.Printf("Step %d: %s\n", step.StepID, step.StepName)
	if step.Error != nil {
		fmt.Printf("  Error: %v\n", step.Error)
	}
	if step.ChildWorkflowID != "" {
		fmt.Printf("  Child: %s\n", step.ChildWorkflowID)
	}
}
```

Workflow status values: `WorkflowStatusPending`, `WorkflowStatusEnqueued`, `WorkflowStatusSuccess`, `WorkflowStatusError`, `WorkflowStatusCancelled`, `WorkflowStatusMaxRecoveryAttemptsExceeded`

To optimize performance, avoid loading inputs/outputs when you don't need them (they are not loaded by default).

Reference: [Workflow Management](https://docs.dbos.dev/golang/tutorials/workflow-management#listing-workflows)

---

## Reference: Workflow Timeout

## Set Workflow Timeouts

Set a timeout for a workflow by using Go's `context.WithTimeout` or `dbos.WithTimeout` on the DBOS context. When the timeout expires, the workflow and all its children are cancelled.

**Incorrect (no timeout for potentially long workflow):**

```go
// No timeout - could run indefinitely
handle, err := dbos.RunWorkflow(ctx, processTask, "data")
```

**Correct (with timeout):**

```go
// Create a context with a 5-minute timeout
timedCtx, cancel := dbos.WithTimeout(ctx, 5*time.Minute)
defer cancel()

handle, err := dbos.RunWorkflow(timedCtx, processTask, "data")
if err != nil {
	log.Fatal(err)
}
```

Key timeout behaviors:
- Timeouts are **start-to-completion**: the timeout begins when the workflow starts execution, not when it's enqueued
- Timeouts are **durable**: they persist across restarts, so workflows can have very long timeouts (hours, days, weeks)
- Cancellation happens at the **beginning of the next step** - the current step completes first
- Cancelling a workflow also cancels all **child workflows**

Reference: [Workflow Timeouts](https://docs.dbos.dev/golang/tutorials/workflow-tutorial#workflow-timeouts)
