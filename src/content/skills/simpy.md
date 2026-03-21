---
title: "Simpy"
description: "Process-based discrete-event simulation framework in Python. Use this skill when building simulations of systems with processes, queues, resources, and time-based events such as manufacturing systems, service operations, network traffic, logistics..."
category: "development"
source: "community"
author: "Community"
tags: ["simpy"]
date: 2026-03-20
---

# SimPy - Discrete-Event Simulation

## Overview

SimPy is a process-based discrete-event simulation framework based on standard Python. Use SimPy to model systems where entities (customers, vehicles, packets, etc.) interact with each other and compete for shared resources (servers, machines, bandwidth, etc.) over time.

**Core capabilities:**
- Process modeling using Python generator functions
- Shared resource management (servers, containers, stores)
- Event-driven scheduling and synchronization
- Real-time simulations synchronized with wall-clock time
- Comprehensive monitoring and data collection

## When to Use This Skill

Use the SimPy skill when:

1. **Modeling discrete-event systems** - Systems where events occur at irregular intervals
2. **Resource contention** - Entities compete for limited resources (servers, machines, staff)
3. **Queue analysis** - Studying waiting lines, service times, and throughput
4. **Process optimization** - Analyzing manufacturing, logistics, or service processes
5. **Network simulation** - Packet routing, bandwidth allocation, latency analysis
6. **Capacity planning** - Determining optimal resource levels for desired performance
7. **System validation** - Testing system behavior before implementation

**Not suitable for:**
- Continuous simulations with fixed time steps (consider SciPy ODE solvers)
- Independent processes without resource sharing
- Pure mathematical optimization (consider SciPy optimize)

## Quick Start

### Basic Simulation Structure

```python
import simpy

def process(env, name):
    """A simple process that waits and prints."""
    print(f'{name} starting at {env.now}')
    yield env.timeout(5)
    print(f'{name} finishing at {env.now}')

# Create environment
env = simpy.Environment()

# Start processes
env.process(process(env, 'Process 1'))
env.process(process(env, 'Process 2'))

# Run simulation
env.run(until=10)
```

### Resource Usage Pattern

```python
import simpy

def customer(env, name, resource):
    """Customer requests resource, uses it, then releases."""
    with resource.request() as req:
        yield req  # Wait for resource
        print(f'{name} got resource at {env.now}')
        yield env.timeout(3)  # Use resource
        print(f'{name} released resource at {env.now}')

env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(customer(env, 'Customer 1', server))
env.process(customer(env, 'Customer 2', server))
env.run()
```

## Core Concepts

### 1. Environment

The simulation environment manages time and schedules events.

```python
import simpy

# Standard environment (runs as fast as possible)
env = simpy.Environment(initial_time=0)

# Real-time environment (synchronized with wall-clock)
import simpy.rt
env_rt = simpy.rt.RealtimeEnvironment(factor=1.0)

# Run simulation
env.run(until=100)  # Run until time 100
env.run()  # Run until no events remain
```

### 2. Processes

Processes are defined using Python generator functions (functions with `yield` statements).

```python
def my_process(env, param1, param2):
    """Process that yields events to pause execution."""
    print(f'Starting at {env.now}')

    # Wait for time to pass
    yield env.timeout(5)

    print(f'Resumed at {env.now}')

    # Wait for another event
    yield env.timeout(3)

    print(f'Done at {env.now}')
    return 'result'

# Start the process
env.process(my_process(env, 'value1', 'value2'))
```

### 3. Events

Events are the fundamental mechanism for process synchronization. Processes yield events and resume when those events are triggered.

**Common event types:**
- `env.timeout(delay)` - Wait for time to pass
- `resource.request()` - Request a resource
- `env.event()` - Create a custom event
- `env.process(func())` - Process as an event
- `event1 & event2` - Wait for all events (AllOf)
- `event1 | event2` - Wait for any event (AnyOf)

## Resources

SimPy provides several resource types for different scenarios. For comprehensive details, see `references/resources.md`.

### Resource Types Summary

| Resource Type | Use Case |
|---------------|----------|
| Resource | Limited capacity (servers, machines) |
| PriorityResource | Priority-based queuing |
| PreemptiveResource | High-priority can interrupt low-priority |
| Container | Bulk materials (fuel, water) |
| Store | Python object storage (FIFO) |
| FilterStore | Selective item retrieval |
| PriorityStore | Priority-ordered items |

### Quick Reference

```python
import simpy

env = simpy.Environment()

# Basic resource (e.g., servers)
resource = simpy.Resource(env, capacity=2)

# Priority resource
priority_resource = simpy.PriorityResource(env, capacity=1)

# Container (e.g., fuel tank)
fuel_tank = simpy.Container(env, capacity=100, init=50)

# Store (e.g., warehouse)
warehouse = simpy.Store(env, capacity=10)
```

## Common Simulation Patterns

### Pattern 1: Customer-Server Queue

```python
import simpy
import random

def customer(env, name, server):
    arrival = env.now
    with server.request() as req:
        yield req
        wait = env.now - arrival
        print(f'{name} waited {wait:.2f}, served at {env.now}')
        yield env.timeout(random.uniform(2, 4))

def customer_generator(env, server):
    i = 0
    while True:
        yield env.timeout(random.uniform(1, 3))
        i += 1
        env.process(customer(env, f'Customer {i}', server))

env = simpy.Environment()
server = simpy.Resource(env, capacity=2)
env.process(customer_generator(env, server))
env.run(until=20)
```

### Pattern 2: Producer-Consumer

```python
import simpy

def producer(env, store):
    item_id = 0
    while True:
        yield env.timeout(2)
        item = f'Item {item_id}'
        yield store.put(item)
        print(f'Produced {item} at {env.now}')
        item_id += 1

def consumer(env, store):
    while True:
        item = yield store.get()
        print(f'Consumed {item} at {env.now}')
        yield env.timeout(3)

env = simpy.Environment()
store = simpy.Store(env, capacity=10)
env.process(producer(env, store))
env.process(consumer(env, store))
env.run(until=20)
```

### Pattern 3: Parallel Task Execution

```python
import simpy

def task(env, name, duration):
    print(f'{name} starting at {env.now}')
    yield env.timeout(duration)
    print(f'{name} done at {env.now}')
    return f'{name} result'

def coordinator(env):
    # Start tasks in parallel
    task1 = env.process(task(env, 'Task 1', 5))
    task2 = env.process(task(env, 'Task 2', 3))
    task3 = env.process(task(env, 'Task 3', 4))

    # Wait for all to complete
    results = yield task1 & task2 & task3
    print(f'All done at {env.now}')

env = simpy.Environment()
env.process(coordinator(env))
env.run()
```

## Workflow Guide

### Step 1: Define the System

Identify:
- **Entities**: What moves through the system? (customers, parts, packets)
- **Resources**: What are the constraints? (servers, machines, bandwidth)
- **Processes**: What are the activities? (arrival, service, departure)
- **Metrics**: What to measure? (wait times, utilization, throughput)

### Step 2: Implement Process Functions

Create generator functions for each process type:

```python
def entity_process(env, name, resources, parameters):
    # Arrival logic
    arrival_time = env.now

    # Request resources
    with resource.request() as req:
        yield req

        # Service logic
        service_time = calculate_service_time(parameters)
        yield env.timeout(service_time)

    # Departure logic
    collect_statistics(env.now - arrival_time)
```

### Step 3: Set Up Monitoring

Use monitoring utilities to collect data. See `references/monitoring.md` for comprehensive techniques.

```python
from scripts.resource_monitor import ResourceMonitor

# Create and monitor resource
resource = simpy.Resource(env, capacity=2)
monitor = ResourceMonitor(env, resource, "Server")

# After simulation
monitor.report()
```

### Step 4: Run and Analyze

```python
# Run simulation
env.run(until=simulation_time)

# Generate reports
monitor.report()
stats.report()

# Export data for further analysis
monitor.export_csv('results.csv')
```

## Advanced Features

### Process Interaction

Processes can interact through events, process yields, and interrupts. See `references/process-interaction.md` for detailed patterns.

**Key mechanisms:**
- **Event signaling**: Shared events for coordination
- **Process yields**: Wait for other processes to complete
- **Interrupts**: Forcefully resume processes for preemption

### Real-Time Simulations

Synchronize simulation with wall-clock time for hardware-in-the-loop or interactive applications. See `references/real-time.md`.

```python
import simpy.rt

env = simpy.rt.RealtimeEnvironment(factor=1.0)  # 1:1 time mapping
# factor=0.5 means 1 sim unit = 0.5 seconds (2x faster)
```

### Comprehensive Monitoring

Monitor processes, resources, and events. See `references/monitoring.md` for techniques including:
- State variable tracking
- Resource monkey-patching
- Event tracing
- Statistical collection

## Scripts and Templates

### basic_simulation_template.py

Complete template for building queue simulations with:
- Configurable parameters
- Statistics collection
- Customer generation
- Resource usage
- Report generation

**Usage:**
```python
from scripts.basic_simulation_template import SimulationConfig, run_simulation

config = SimulationConfig()
config.num_resources = 2
config.sim_time = 100
stats = run_simulation(config)
stats.report()
```

### resource_monitor.py

Reusable monitoring utilities:
- `ResourceMonitor` - Track single resource
- `MultiResourceMonitor` - Monitor multiple resources
- `ContainerMonitor` - Track container levels
- Automatic statistics calculation
- CSV export functionality

**Usage:**
```python
from scripts.resource_monitor import ResourceMonitor

monitor = ResourceMonitor(env, resource, "My Resource")
# ... run simulation ...
monitor.report()
monitor.export_csv('data.csv')
```

## Reference Documentation

Detailed guides for specific topics:

- **`references/resources.md`** - All resource types with examples
- **`references/events.md`** - Event system and patterns
- **`references/process-interaction.md`** - Process synchronization
- **`references/monitoring.md`** - Data collection techniques
- **`references/real-time.md`** - Real-time simulation setup

## Best Practices

1. **Generator functions**: Always use `yield` in process functions
2. **Resource context managers**: Use `with resource.request() as req:` for automatic cleanup
3. **Reproducibility**: Set `random.seed()` for consistent results
4. **Monitoring**: Collect data throughout simulation, not just at the end
5. **Validation**: Compare simple cases with analytical solutions
6. **Documentation**: Comment process logic and parameter choices
7. **Modular design**: Separate process logic, statistics, and configuration

## Common Pitfalls

1. **Forgetting yield**: Processes must yield events to pause
2. **Event reuse**: Events can only be triggered once
3. **Resource leaks**: Use context managers or ensure release
4. **Blocking operations**: Avoid Python blocking calls in processes
5. **Time units**: Stay consistent with time unit interpretation
6. **Deadlocks**: Ensure at least one process can make progress

## Example Use Cases

- **Manufacturing**: Machine scheduling, production lines, inventory management
- **Healthcare**: Emergency room simulation, patient flow, staff allocation
- **Telecommunications**: Network traffic, packet routing, bandwidth allocation
- **Transportation**: Traffic flow, logistics, vehicle routing
- **Service operations**: Call centers, retail checkout, appointment scheduling
- **Computer systems**: CPU scheduling, memory management, I/O operations

---

## Reference: Events

# SimPy Events System

This guide covers the event system in SimPy, which forms the foundation of discrete-event simulation.

## Event Basics

Events are the core mechanism for controlling simulation flow. Processes yield events and resume when those events are triggered.

### Event Lifecycle

Events progress through three states:

1. **Not triggered** - Initial state as memory objects
2. **Triggered** - Scheduled in event queue; `triggered` property is `True`
3. **Processed** - Removed from queue with callbacks executed; `processed` property is `True`

```python
import simpy

env = simpy.Environment()

# Create an event
event = env.event()
print(f'Triggered: {event.triggered}, Processed: {event.processed}')  # Both False

# Trigger the event
event.succeed(value='Event result')
print(f'Triggered: {event.triggered}, Processed: {event.processed}')  # True, False

# Run to process the event
env.run()
print(f'Triggered: {event.triggered}, Processed: {event.processed}')  # True, True
print(f'Value: {event.value}')  # 'Event result'
```

## Core Event Types

### Timeout

Controls time progression in simulations. Most common event type.

```python
import simpy

def process(env):
    print(f'Starting at {env.now}')
    yield env.timeout(5)
    print(f'Resumed at {env.now}')

    # Timeout with value
    result = yield env.timeout(3, value='Done')
    print(f'Result: {result} at {env.now}')

env = simpy.Environment()
env.process(process(env))
env.run()
```

**Usage:**
- `env.timeout(delay)` - Wait for specified time
- `env.timeout(delay, value=val)` - Wait and return value

### Process Events

Processes themselves are events, allowing processes to wait for other processes to complete.

```python
import simpy

def worker(env, name, duration):
    print(f'{name} starting at {env.now}')
    yield env.timeout(duration)
    print(f'{name} finished at {env.now}')
    return f'{name} result'

def coordinator(env):
    # Start worker processes
    worker1 = env.process(worker(env, 'Worker 1', 5))
    worker2 = env.process(worker(env, 'Worker 2', 3))

    # Wait for worker1 to complete
    result = yield worker1
    print(f'Coordinator received: {result}')

    # Wait for worker2
    result = yield worker2
    print(f'Coordinator received: {result}')

env = simpy.Environment()
env.process(coordinator(env))
env.run()
```

### Event

Generic event that can be manually triggered.

```python
import simpy

def waiter(env, event):
    print(f'Waiting for event at {env.now}')
    value = yield event
    print(f'Event received with value: {value} at {env.now}')

def triggerer(env, event):
    yield env.timeout(5)
    print(f'Triggering event at {env.now}')
    event.succeed(value='Hello!')

env = simpy.Environment()
event = env.event()
env.process(waiter(env, event))
env.process(triggerer(env, event))
env.run()
```

## Composite Events

### AllOf - Wait for Multiple Events

Triggers when all specified events have occurred.

```python
import simpy

def process(env):
    # Start multiple tasks
    task1 = env.timeout(3, value='Task 1 done')
    task2 = env.timeout(5, value='Task 2 done')
    task3 = env.timeout(4, value='Task 3 done')

    # Wait for all to complete
    results = yield simpy.AllOf(env, [task1, task2, task3])
    print(f'All tasks completed at {env.now}')
    print(f'Results: {results}')

    # Alternative syntax using & operator
    task4 = env.timeout(2)
    task5 = env.timeout(3)
    yield task4 & task5
    print(f'Tasks 4 and 5 completed at {env.now}')

env = simpy.Environment()
env.process(process(env))
env.run()
```

**Returns:** Dictionary mapping events to their values

**Use cases:**
- Parallel task completion
- Barrier synchronization
- Waiting for multiple resources

### AnyOf - Wait for Any Event

Triggers when at least one specified event has occurred.

```python
import simpy

def process(env):
    # Start multiple tasks with different durations
    fast_task = env.timeout(2, value='Fast')
    slow_task = env.timeout(10, value='Slow')

    # Wait for first to complete
    results = yield simpy.AnyOf(env, [fast_task, slow_task])
    print(f'First task completed at {env.now}')
    print(f'Results: {results}')

    # Alternative syntax using | operator
    task1 = env.timeout(5)
    task2 = env.timeout(3)
    yield task1 | task2
    print(f'One of the tasks completed at {env.now}')

env = simpy.Environment()
env.process(process(env))
env.run()
```

**Returns:** Dictionary with completed events and their values

**Use cases:**
- Racing conditions
- Timeout mechanisms
- First-to-respond scenarios

## Event Triggering Methods

Events can be triggered in three ways:

### succeed(value=None)

Marks event as successful.

```python
event = env.event()
event.succeed(value='Success!')
```

### fail(exception)

Marks event as failed with an exception.

```python
def process(env):
    event = env.event()
    event.fail(ValueError('Something went wrong'))

    try:
        yield event
    except ValueError as e:
        print(f'Caught exception: {e}')

env = simpy.Environment()
env.process(process(env))
env.run()
```

### trigger(event)

Copies another event's outcome.

```python
event1 = env.event()
event1.succeed(value='Original')

event2 = env.event()
event2.trigger(event1)  # event2 now has same outcome as event1
```

## Callbacks

Attach functions to execute when events are triggered.

```python
import simpy

def callback(event):
    print(f'Callback executed! Event value: {event.value}')

def process(env):
    event = env.timeout(5, value='Done')
    event.callbacks.append(callback)
    yield event

env = simpy.Environment()
env.process(process(env))
env.run()
```

**Note:** Yielding an event from a process automatically adds the process's resume method as a callback.

## Event Sharing

Multiple processes can wait for the same event.

```python
import simpy

def waiter(env, name, event):
    print(f'{name} waiting at {env.now}')
    value = yield event
    print(f'{name} resumed with {value} at {env.now}')

def trigger_event(env, event):
    yield env.timeout(5)
    event.succeed(value='Go!')

env = simpy.Environment()
shared_event = env.event()

env.process(waiter(env, 'Process 1', shared_event))
env.process(waiter(env, 'Process 2', shared_event))
env.process(waiter(env, 'Process 3', shared_event))
env.process(trigger_event(env, shared_event))

env.run()
```

**Use cases:**
- Broadcasting signals
- Barrier synchronization
- Coordinated process resumption

## Advanced Event Patterns

### Timeout with Cancellation

```python
import simpy

def process_with_timeout(env):
    work = env.timeout(10, value='Work complete')
    timeout = env.timeout(5, value='Timeout!')

    # Race between work and timeout
    result = yield work | timeout

    if work in result:
        print(f'Work completed: {result[work]}')
    else:
        print(f'Timed out: {result[timeout]}')

env = simpy.Environment()
env.process(process_with_timeout(env))
env.run()
```

### Event Chaining

```python
import simpy

def event_chain(env):
    # Create chain of dependent events
    event1 = env.event()
    event2 = env.event()
    event3 = env.event()

    def trigger_sequence(env):
        yield env.timeout(2)
        event1.succeed(value='Step 1')
        yield env.timeout(2)
        event2.succeed(value='Step 2')
        yield env.timeout(2)
        event3.succeed(value='Step 3')

    env.process(trigger_sequence(env))

    # Wait for sequence
    val1 = yield event1
    print(f'{val1} at {env.now}')
    val2 = yield event2
    print(f'{val2} at {env.now}')
    val3 = yield event3
    print(f'{val3} at {env.now}')

env = simpy.Environment()
env.process(event_chain(env))
env.run()
```

### Conditional Events

```python
import simpy

def conditional_process(env):
    temperature = 20

    if temperature > 25:
        yield env.timeout(5)  # Cooling required
        print('System cooled')
    else:
        yield env.timeout(1)  # No cooling needed
        print('Temperature acceptable')

env = simpy.Environment()
env.process(conditional_process(env))
env.run()
```

## Best Practices

1. **Always yield events**: Processes must yield events to pause execution
2. **Don't trigger events multiple times**: Events can only be triggered once
3. **Handle failures**: Use try-except when yielding events that might fail
4. **Composite events for parallelism**: Use AllOf/AnyOf for concurrent operations
5. **Shared events for broadcasting**: Multiple processes can yield the same event
6. **Event values for data passing**: Use event values to pass results between processes

---

## Reference: Monitoring

# SimPy Monitoring and Data Collection

This guide covers techniques for collecting data and monitoring simulation behavior in SimPy.

## Monitoring Strategy

Before implementing monitoring, define three things:

1. **What to monitor**: Processes, resources, events, or system state
2. **When to monitor**: On change, at intervals, or at specific events
3. **How to store data**: Lists, files, databases, or real-time output

## 1. Process Monitoring

### State Variable Tracking

Track process state by recording variables when they change.

```python
import simpy

def customer(env, name, service_time, log):
    arrival_time = env.now
    log.append(('arrival', name, arrival_time))

    yield env.timeout(service_time)

    departure_time = env.now
    log.append(('departure', name, departure_time))

    wait_time = departure_time - arrival_time
    log.append(('wait_time', name, wait_time))

env = simpy.Environment()
log = []

env.process(customer(env, 'Customer 1', 5, log))
env.process(customer(env, 'Customer 2', 3, log))
env.run()

print('Simulation log:')
for entry in log:
    print(entry)
```

### Time-Series Data Collection

```python
import simpy

def system_monitor(env, system_state, data_log, interval):
    while True:
        data_log.append((env.now, system_state['queue_length'], system_state['utilization']))
        yield env.timeout(interval)

def process(env, system_state):
    while True:
        system_state['queue_length'] += 1
        yield env.timeout(2)
        system_state['queue_length'] -= 1
        system_state['utilization'] = system_state['queue_length'] / 10
        yield env.timeout(3)

env = simpy.Environment()
system_state = {'queue_length': 0, 'utilization': 0.0}
data_log = []

env.process(system_monitor(env, system_state, data_log, interval=1))
env.process(process(env, system_state))
env.run(until=20)

print('Time series data:')
for time, queue, util in data_log:
    print(f'Time {time}: Queue={queue}, Utilization={util:.2f}')
```

### Multiple Variable Tracking

```python
import simpy

class SimulationData:
    def __init__(self):
        self.timestamps = []
        self.queue_lengths = []
        self.processing_times = []
        self.utilizations = []

    def record(self, timestamp, queue_length, processing_time, utilization):
        self.timestamps.append(timestamp)
        self.queue_lengths.append(queue_length)
        self.processing_times.append(processing_time)
        self.utilizations.append(utilization)

def monitored_process(env, data):
    queue_length = 0
    processing_time = 0
    utilization = 0.0

    for i in range(5):
        queue_length = i % 3
        processing_time = 2 + i
        utilization = queue_length / 10

        data.record(env.now, queue_length, processing_time, utilization)
        yield env.timeout(2)

env = simpy.Environment()
data = SimulationData()
env.process(monitored_process(env, data))
env.run()

print(f'Collected {len(data.timestamps)} data points')
```

## 2. Resource Monitoring

### Monkey-Patching Resources

Patch resource methods to intercept and log operations.

```python
import simpy

def patch_resource(resource, data_log):
    """Patch a resource to log all requests and releases."""

    # Save original methods
    original_request = resource.request
    original_release = resource.release

    # Create wrapper for request
    def logged_request(*args, **kwargs):
        req = original_request(*args, **kwargs)
        data_log.append(('request', resource._env.now, len(resource.queue)))
        return req

    # Create wrapper for release
    def logged_release(*args, **kwargs):
        result = original_release(*args, **kwargs)
        data_log.append(('release', resource._env.now, len(resource.queue)))
        return result

    # Replace methods
    resource.request = logged_request
    resource.release = logged_release

def user(env, name, resource):
    with resource.request() as req:
        yield req
        print(f'{name} using resource at {env.now}')
        yield env.timeout(3)
        print(f'{name} releasing resource at {env.now}')

env = simpy.Environment()
resource = simpy.Resource(env, capacity=1)
log = []

patch_resource(resource, log)

env.process(user(env, 'User 1', resource))
env.process(user(env, 'User 2', resource))
env.run()

print('\nResource log:')
for entry in log:
    print(entry)
```

### Resource Subclassing

Create custom resource classes with built-in monitoring.

```python
import simpy

class MonitoredResource(simpy.Resource):
    def __init__(self, env, capacity):
        super().__init__(env, capacity)
        self.data = []
        self.utilization_data = []

    def request(self, *args, **kwargs):
        req = super().request(*args, **kwargs)
        queue_length = len(self.queue)
        utilization = self.count / self.capacity
        self.data.append(('request', self._env.now, queue_length, utilization))
        self.utilization_data.append((self._env.now, utilization))
        return req

    def release(self, *args, **kwargs):
        result = super().release(*args, **kwargs)
        queue_length = len(self.queue)
        utilization = self.count / self.capacity
        self.data.append(('release', self._env.now, queue_length, utilization))
        self.utilization_data.append((self._env.now, utilization))
        return result

    def average_utilization(self):
        if not self.utilization_data:
            return 0.0
        return sum(u for _, u in self.utilization_data) / len(self.utilization_data)

def user(env, name, resource):
    with resource.request() as req:
        yield req
        print(f'{name} using resource at {env.now}')
        yield env.timeout(2)

env = simpy.Environment()
resource = MonitoredResource(env, capacity=2)

for i in range(5):
    env.process(user(env, f'User {i+1}', resource))

env.run()

print(f'\nAverage utilization: {resource.average_utilization():.2%}')
print(f'Total operations: {len(resource.data)}')
```

### Container Level Monitoring

```python
import simpy

class MonitoredContainer(simpy.Container):
    def __init__(self, env, capacity, init=0):
        super().__init__(env, capacity, init)
        self.level_data = [(0, init)]

    def put(self, amount):
        result = super().put(amount)
        self.level_data.append((self._env.now, self.level))
        return result

    def get(self, amount):
        result = super().get(amount)
        self.level_data.append((self._env.now, self.level))
        return result

def producer(env, container, amount, interval):
    while True:
        yield env.timeout(interval)
        yield container.put(amount)
        print(f'Produced {amount}. Level: {container.level} at {env.now}')

def consumer(env, container, amount, interval):
    while True:
        yield env.timeout(interval)
        yield container.get(amount)
        print(f'Consumed {amount}. Level: {container.level} at {env.now}')

env = simpy.Environment()
container = MonitoredContainer(env, capacity=100, init=50)

env.process(producer(env, container, 20, 3))
env.process(consumer(env, container, 15, 4))
env.run(until=20)

print('\nLevel history:')
for time, level in container.level_data:
    print(f'Time {time}: Level={level}')
```

## 3. Event Tracing

### Environment Step Monitoring

Monitor all events by patching the environment's step function.

```python
import simpy

def trace(env, callback):
    """Trace all events processed by the environment."""

    def _trace_step():
        # Get next event before it's processed
        if env._queue:
            time, priority, event_id, event = env._queue[0]
            callback(time, priority, event_id, event)

        # Call original step
        return original_step()

    original_step = env.step
    env.step = _trace_step

def event_callback(time, priority, event_id, event):
    print(f'Event: time={time}, priority={priority}, id={event_id}, type={type(event).__name__}')

def process(env, name):
    print(f'{name}: Starting at {env.now}')
    yield env.timeout(5)
    print(f'{name}: Done at {env.now}')

env = simpy.Environment()
trace(env, event_callback)

env.process(process(env, 'Process 1'))
env.process(process(env, 'Process 2'))
env.run()
```

### Event Scheduling Monitor

Track when events are scheduled.

```python
import simpy

class MonitoredEnvironment(simpy.Environment):
    def __init__(self):
        super().__init__()
        self.scheduled_events = []

    def schedule(self, event, priority=simpy.core.NORMAL, delay=0):
        super().schedule(event, priority, delay)
        scheduled_time = self.now + delay
        self.scheduled_events.append((scheduled_time, priority, type(event).__name__))

def process(env, name, delay):
    print(f'{name}: Scheduling timeout for {delay} at {env.now}')
    yield env.timeout(delay)
    print(f'{name}: Resumed at {env.now}')

env = MonitoredEnvironment()
env.process(process(env, 'Process 1', 5))
env.process(process(env, 'Process 2', 3))
env.run()

print('\nScheduled events:')
for time, priority, event_type in env.scheduled_events:
    print(f'Time {time}, Priority {priority}, Type {event_type}')
```

## 4. Statistical Monitoring

### Queue Statistics

```python
import simpy

class QueueStatistics:
    def __init__(self):
        self.arrival_times = []
        self.departure_times = []
        self.queue_lengths = []
        self.wait_times = []

    def record_arrival(self, time, queue_length):
        self.arrival_times.append(time)
        self.queue_lengths.append(queue_length)

    def record_departure(self, arrival_time, departure_time):
        self.departure_times.append(departure_time)
        self.wait_times.append(departure_time - arrival_time)

    def average_wait_time(self):
        return sum(self.wait_times) / len(self.wait_times) if self.wait_times else 0

    def average_queue_length(self):
        return sum(self.queue_lengths) / len(self.queue_lengths) if self.queue_lengths else 0

def customer(env, resource, stats):
    arrival_time = env.now
    stats.record_arrival(arrival_time, len(resource.queue))

    with resource.request() as req:
        yield req
        departure_time = env.now
        stats.record_departure(arrival_time, departure_time)
        yield env.timeout(2)

env = simpy.Environment()
resource = simpy.Resource(env, capacity=1)
stats = QueueStatistics()

for i in range(5):
    env.process(customer(env, resource, stats))

env.run()

print(f'Average wait time: {stats.average_wait_time():.2f}')
print(f'Average queue length: {stats.average_queue_length():.2f}')
```

## 5. Data Export

### CSV Export

```python
import simpy
import csv

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'Metric', 'Value'])
        writer.writerows(data)

def monitored_simulation(env, data_log):
    for i in range(10):
        data_log.append((env.now, 'queue_length', i % 3))
        data_log.append((env.now, 'utilization', (i % 3) / 10))
        yield env.timeout(1)

env = simpy.Environment()
data = []
env.process(monitored_simulation(env, data))
env.run()

export_to_csv(data, 'simulation_data.csv')
print('Data exported to simulation_data.csv')
```

### Real-time Plotting (requires matplotlib)

```python
import simpy
import matplotlib.pyplot as plt

class RealTimePlotter:
    def __init__(self):
        self.times = []
        self.values = []

    def update(self, time, value):
        self.times.append(time)
        self.values.append(value)

    def plot(self, title='Simulation Results'):
        plt.figure(figsize=(10, 6))
        plt.plot(self.times, self.values)
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title(title)
        plt.grid(True)
        plt.show()

def monitored_process(env, plotter):
    value = 0
    for i in range(20):
        value = value * 0.9 + (i % 5)
        plotter.update(env.now, value)
        yield env.timeout(1)

env = simpy.Environment()
plotter = RealTimePlotter()
env.process(monitored_process(env, plotter))
env.run()

plotter.plot('Process Value Over Time')
```

## Best Practices

1. **Minimize overhead**: Only monitor what's necessary; excessive logging can slow simulations

2. **Structured data**: Use classes or named tuples for complex data points

3. **Time-stamping**: Always include timestamps with monitored data

4. **Aggregation**: For long simulations, aggregate data rather than storing every event

5. **Lazy evaluation**: Consider collecting raw data and computing statistics after simulation

6. **Memory management**: For very long simulations, periodically flush data to disk

7. **Validation**: Verify monitoring code doesn't affect simulation behavior

8. **Separation of concerns**: Keep monitoring code separate from simulation logic

9. **Reusable components**: Create generic monitoring classes that can be reused across simulations

---

## Reference: Process Interaction

# SimPy Process Interaction

This guide covers the mechanisms for processes to interact and synchronize in SimPy simulations.

## Interaction Mechanisms Overview

SimPy provides three primary ways for processes to interact:

1. **Event-based passivation/reactivation** - Shared events for signaling
2. **Waiting for process termination** - Yielding process objects
3. **Interruption** - Forcefully resuming paused processes

## 1. Event-Based Passivation and Reactivation

Processes can share events to coordinate their execution.

### Basic Signal Pattern

```python
import simpy

def controller(env, signal_event):
    print(f'Controller: Preparing at {env.now}')
    yield env.timeout(5)
    print(f'Controller: Sending signal at {env.now}')
    signal_event.succeed()

def worker(env, signal_event):
    print(f'Worker: Waiting for signal at {env.now}')
    yield signal_event
    print(f'Worker: Received signal, starting work at {env.now}')
    yield env.timeout(3)
    print(f'Worker: Work complete at {env.now}')

env = simpy.Environment()
signal = env.event()
env.process(controller(env, signal))
env.process(worker(env, signal))
env.run()
```

**Use cases:**
- Start signals for coordinated operations
- Completion notifications
- Broadcasting state changes

### Multiple Waiters

Multiple processes can wait for the same signal event.

```python
import simpy

def broadcaster(env, signal):
    yield env.timeout(5)
    print(f'Broadcasting signal at {env.now}')
    signal.succeed(value='Go!')

def listener(env, name, signal):
    print(f'{name}: Waiting at {env.now}')
    msg = yield signal
    print(f'{name}: Received "{msg}" at {env.now}')
    yield env.timeout(2)
    print(f'{name}: Done at {env.now}')

env = simpy.Environment()
broadcast_signal = env.event()

env.process(broadcaster(env, broadcast_signal))
for i in range(3):
    env.process(listener(env, f'Listener {i+1}', broadcast_signal))

env.run()
```

### Barrier Synchronization

```python
import simpy

class Barrier:
    def __init__(self, env, n):
        self.env = env
        self.n = n
        self.count = 0
        self.event = env.event()

    def wait(self):
        self.count += 1
        if self.count >= self.n:
            self.event.succeed()
        return self.event

def worker(env, barrier, name, work_time):
    print(f'{name}: Working at {env.now}')
    yield env.timeout(work_time)
    print(f'{name}: Reached barrier at {env.now}')
    yield barrier.wait()
    print(f'{name}: Passed barrier at {env.now}')

env = simpy.Environment()
barrier = Barrier(env, 3)

env.process(worker(env, barrier, 'Worker A', 3))
env.process(worker(env, barrier, 'Worker B', 5))
env.process(worker(env, barrier, 'Worker C', 7))

env.run()
```

## 2. Waiting for Process Termination

Processes are events themselves, so you can yield them to wait for completion.

### Sequential Process Execution

```python
import simpy

def task(env, name, duration):
    print(f'{name}: Starting at {env.now}')
    yield env.timeout(duration)
    print(f'{name}: Completed at {env.now}')
    return f'{name} result'

def sequential_coordinator(env):
    # Execute tasks sequentially
    result1 = yield env.process(task(env, 'Task 1', 5))
    print(f'Coordinator: {result1}')

    result2 = yield env.process(task(env, 'Task 2', 3))
    print(f'Coordinator: {result2}')

    result3 = yield env.process(task(env, 'Task 3', 4))
    print(f'Coordinator: {result3}')

env = simpy.Environment()
env.process(sequential_coordinator(env))
env.run()
```

### Parallel Process Execution

```python
import simpy

def task(env, name, duration):
    print(f'{name}: Starting at {env.now}')
    yield env.timeout(duration)
    print(f'{name}: Completed at {env.now}')
    return f'{name} result'

def parallel_coordinator(env):
    # Start all tasks
    task1 = env.process(task(env, 'Task 1', 5))
    task2 = env.process(task(env, 'Task 2', 3))
    task3 = env.process(task(env, 'Task 3', 4))

    # Wait for all to complete
    results = yield task1 & task2 & task3
    print(f'All tasks completed at {env.now}')
    print(f'Task 1 result: {task1.value}')
    print(f'Task 2 result: {task2.value}')
    print(f'Task 3 result: {task3.value}')

env = simpy.Environment()
env.process(parallel_coordinator(env))
env.run()
```

### First-to-Complete Pattern

```python
import simpy

def server(env, name, processing_time):
    print(f'{name}: Starting request at {env.now}')
    yield env.timeout(processing_time)
    print(f'{name}: Completed at {env.now}')
    return name

def load_balancer(env):
    # Send request to multiple servers
    server1 = env.process(server(env, 'Server 1', 5))
    server2 = env.process(server(env, 'Server 2', 3))
    server3 = env.process(server(env, 'Server 3', 7))

    # Wait for first to respond
    result = yield server1 | server2 | server3

    # Get the winner
    winner = list(result.values())[0]
    print(f'Load balancer: {winner} responded first at {env.now}')

env = simpy.Environment()
env.process(load_balancer(env))
env.run()
```

## 3. Process Interruption

Processes can be interrupted using `process.interrupt()`, which throws an `Interrupt` exception.

### Basic Interruption

```python
import simpy

def worker(env):
    try:
        print(f'Worker: Starting long task at {env.now}')
        yield env.timeout(10)
        print(f'Worker: Task completed at {env.now}')
    except simpy.Interrupt as interrupt:
        print(f'Worker: Interrupted at {env.now}')
        print(f'Interrupt cause: {interrupt.cause}')

def interrupter(env, target_process):
    yield env.timeout(5)
    print(f'Interrupter: Interrupting worker at {env.now}')
    target_process.interrupt(cause='Higher priority task')

env = simpy.Environment()
worker_process = env.process(worker(env))
env.process(interrupter(env, worker_process))
env.run()
```

### Resumable Interruption

Process can re-yield the same event after interruption to continue waiting.

```python
import simpy

def resumable_worker(env):
    work_left = 10

    while work_left > 0:
        try:
            print(f'Worker: Working ({work_left} units left) at {env.now}')
            start = env.now
            yield env.timeout(work_left)
            work_left = 0
            print(f'Worker: Completed at {env.now}')
        except simpy.Interrupt:
            work_left -= (env.now - start)
            print(f'Worker: Interrupted! {work_left} units left at {env.now}')

def interrupter(env, worker_proc):
    yield env.timeout(3)
    worker_proc.interrupt()
    yield env.timeout(2)
    worker_proc.interrupt()

env = simpy.Environment()
worker_proc = env.process(resumable_worker(env))
env.process(interrupter(env, worker_proc))
env.run()
```

### Interrupt with Custom Cause

```python
import simpy

def machine(env, name):
    while True:
        try:
            print(f'{name}: Operating at {env.now}')
            yield env.timeout(5)
        except simpy.Interrupt as interrupt:
            if interrupt.cause == 'maintenance':
                print(f'{name}: Maintenance required at {env.now}')
                yield env.timeout(2)
                print(f'{name}: Maintenance complete at {env.now}')
            elif interrupt.cause == 'emergency':
                print(f'{name}: Emergency stop at {env.now}')
                break

def maintenance_scheduler(env, machine_proc):
    yield env.timeout(7)
    machine_proc.interrupt(cause='maintenance')
    yield env.timeout(10)
    machine_proc.interrupt(cause='emergency')

env = simpy.Environment()
machine_proc = env.process(machine(env, 'Machine 1'))
env.process(maintenance_scheduler(env, machine_proc))
env.run()
```

### Preemptive Resource with Interruption

```python
import simpy

def user(env, name, resource, priority, duration):
    with resource.request(priority=priority) as req:
        try:
            yield req
            print(f'{name} (priority {priority}): Got resource at {env.now}')
            yield env.timeout(duration)
            print(f'{name}: Done at {env.now}')
        except simpy.Interrupt:
            print(f'{name}: Preempted at {env.now}')

env = simpy.Environment()
resource = simpy.PreemptiveResource(env, capacity=1)

env.process(user(env, 'Low priority user', resource, priority=10, duration=10))
env.process(user(env, 'High priority user', resource, priority=1, duration=5))
env.run()
```

## Advanced Patterns

### Producer-Consumer with Signaling

```python
import simpy

class Buffer:
    def __init__(self, env, capacity):
        self.env = env
        self.capacity = capacity
        self.items = []
        self.item_available = env.event()

    def put(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            if not self.item_available.triggered:
                self.item_available.succeed()
            return True
        return False

    def get(self):
        if self.items:
            return self.items.pop(0)
        return None

def producer(env, buffer):
    item_id = 0
    while True:
        yield env.timeout(2)
        item = f'Item {item_id}'
        if buffer.put(item):
            print(f'Producer: Added {item} at {env.now}')
            item_id += 1

def consumer(env, buffer):
    while True:
        if buffer.items:
            item = buffer.get()
            print(f'Consumer: Retrieved {item} at {env.now}')
            yield env.timeout(3)
        else:
            print(f'Consumer: Waiting for items at {env.now}')
            yield buffer.item_available
            buffer.item_available = env.event()

env = simpy.Environment()
buffer = Buffer(env, capacity=5)
env.process(producer(env, buffer))
env.process(consumer(env, buffer))
env.run(until=20)
```

### Handshake Protocol

```python
import simpy

def sender(env, request_event, acknowledge_event):
    for i in range(3):
        print(f'Sender: Sending request {i} at {env.now}')
        request_event.succeed(value=f'Request {i}')
        yield acknowledge_event
        print(f'Sender: Received acknowledgment at {env.now}')

        # Reset events for next iteration
        request_event = env.event()
        acknowledge_event = env.event()
        yield env.timeout(1)

def receiver(env, request_event, acknowledge_event):
    for i in range(3):
        request = yield request_event
        print(f'Receiver: Got {request} at {env.now}')
        yield env.timeout(2)  # Process request
        acknowledge_event.succeed()
        print(f'Receiver: Sent acknowledgment at {env.now}')

        # Reset for next iteration
        request_event = env.event()
        acknowledge_event = env.event()

env = simpy.Environment()
request = env.event()
ack = env.event()
env.process(sender(env, request, ack))
env.process(receiver(env, request, ack))
env.run()
```

## Best Practices

1. **Choose the right mechanism**:
   - Use events for signals and broadcasts
   - Use process yields for sequential/parallel workflows
   - Use interrupts for preemption and emergency handling

2. **Exception handling**: Always wrap interrupt-prone code in try-except blocks

3. **Event lifecycle**: Remember that events can only be triggered once; create new events for repeated signaling

4. **Process references**: Store process objects if you need to interrupt them later

5. **Cause information**: Use interrupt causes to communicate why interruption occurred

6. **Resumable patterns**: Track progress to enable resumption after interruption

7. **Avoid deadlocks**: Ensure at least one process can make progress at any time

---

## Reference: Real Time

# SimPy Real-Time Simulations

This guide covers real-time simulation capabilities in SimPy, where simulation time is synchronized with wall-clock time.

## Overview

Real-time simulations synchronize simulation time with actual wall-clock time. This is useful for:

- **Hardware-in-the-loop (HIL)** testing
- **Human interaction** with simulations
- **Algorithm behavior analysis** under real-time constraints
- **System integration** testing
- **Demonstration** purposes

## RealtimeEnvironment

Replace the standard `Environment` with `simpy.rt.RealtimeEnvironment` to enable real-time synchronization.

### Basic Usage

```python
import simpy.rt

def process(env):
    while True:
        print(f'Tick at {env.now}')
        yield env.timeout(1)

# Real-time environment with 1:1 time mapping
env = simpy.rt.RealtimeEnvironment(factor=1.0)
env.process(process(env))
env.run(until=5)
```

### Constructor Parameters

```python
simpy.rt.RealtimeEnvironment(
    initial_time=0,      # Starting simulation time
    factor=1.0,          # Real time per simulation time unit
    strict=True          # Raise errors on timing violations
)
```

## Time Scaling with Factor

The `factor` parameter controls how simulation time maps to real time.

### Factor Examples

```python
import simpy.rt
import time

def timed_process(env, label):
    start = time.time()
    print(f'{label}: Starting at {env.now}')
    yield env.timeout(2)
    elapsed = time.time() - start
    print(f'{label}: Completed at {env.now} (real time: {elapsed:.2f}s)')

# Factor = 1.0: 1 simulation time unit = 1 second
print('Factor = 1.0 (2 sim units = 2 seconds)')
env = simpy.rt.RealtimeEnvironment(factor=1.0)
env.process(timed_process(env, 'Normal speed'))
env.run()

# Factor = 0.5: 1 simulation time unit = 0.5 seconds
print('\nFactor = 0.5 (2 sim units = 1 second)')
env = simpy.rt.RealtimeEnvironment(factor=0.5)
env.process(timed_process(env, 'Double speed'))
env.run()

# Factor = 2.0: 1 simulation time unit = 2 seconds
print('\nFactor = 2.0 (2 sim units = 4 seconds)')
env = simpy.rt.RealtimeEnvironment(factor=2.0)
env.process(timed_process(env, 'Half speed'))
env.run()
```

**Factor interpretation:**
- `factor=1.0` → 1 simulation time unit takes 1 real second
- `factor=0.1` → 1 simulation time unit takes 0.1 real seconds (10x faster)
- `factor=60` → 1 simulation time unit takes 60 real seconds (1 minute)

## Strict Mode

### strict=True (Default)

Raises `RuntimeError` if computation exceeds allocated real-time budget.

```python
import simpy.rt
import time

def heavy_computation(env):
    print(f'Starting computation at {env.now}')
    yield env.timeout(1)

    # Simulate heavy computation (exceeds 1 second budget)
    time.sleep(1.5)

    print(f'Computation done at {env.now}')

env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=True)
env.process(heavy_computation(env))

try:
    env.run()
except RuntimeError as e:
    print(f'Error: {e}')
```

### strict=False

Allows simulation to run slower than intended without crashing.

```python
import simpy.rt
import time

def heavy_computation(env):
    print(f'Starting at {env.now}')
    yield env.timeout(1)

    # Heavy computation
    time.sleep(1.5)

    print(f'Done at {env.now}')

env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=False)
env.process(heavy_computation(env))
env.run()

print('Simulation completed (slower than real-time)')
```

**Use strict=False when:**
- Development and debugging
- Computation time is unpredictable
- Acceptable to run slower than target rate
- Analyzing worst-case behavior

## Hardware-in-the-Loop Example

```python
import simpy.rt

class HardwareInterface:
    """Simulated hardware interface."""

    def __init__(self):
        self.sensor_value = 0

    def read_sensor(self):
        """Simulate reading from hardware sensor."""
        import random
        self.sensor_value = random.uniform(20.0, 30.0)
        return self.sensor_value

    def write_actuator(self, value):
        """Simulate writing to hardware actuator."""
        print(f'Actuator set to {value:.2f}')

def control_loop(env, hardware, setpoint):
    """Simple control loop running in real-time."""
    while True:
        # Read sensor
        sensor_value = hardware.read_sensor()
        print(f'[{env.now}] Sensor: {sensor_value:.2f}°C')

        # Simple proportional control
        error = setpoint - sensor_value
        control_output = error * 0.1

        # Write actuator
        hardware.write_actuator(control_output)

        # Control loop runs every 0.5 seconds
        yield env.timeout(0.5)

# Real-time environment: 1 sim unit = 1 second
env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=False)
hardware = HardwareInterface()
setpoint = 25.0

env.process(control_loop(env, hardware, setpoint))
env.run(until=5)
```

## Human Interaction Example

```python
import simpy.rt

def interactive_process(env):
    """Process that waits for simulated user input."""
    print('Simulation started. Events will occur in real-time.')

    yield env.timeout(2)
    print(f'[{env.now}] Event 1: System startup')

    yield env.timeout(3)
    print(f'[{env.now}] Event 2: Initialization complete')

    yield env.timeout(2)
    print(f'[{env.now}] Event 3: Ready for operation')

# Real-time environment for human-paced demonstration
env = simpy.rt.RealtimeEnvironment(factor=1.0)
env.process(interactive_process(env))
env.run()
```

## Monitoring Real-Time Performance

```python
import simpy.rt
import time

class RealTimeMonitor:
    def __init__(self):
        self.step_times = []
        self.drift_values = []

    def record_step(self, sim_time, real_time, expected_real_time):
        self.step_times.append(sim_time)
        drift = real_time - expected_real_time
        self.drift_values.append(drift)

    def report(self):
        if self.drift_values:
            avg_drift = sum(self.drift_values) / len(self.drift_values)
            max_drift = max(abs(d) for d in self.drift_values)
            print(f'\nReal-time performance:')
            print(f'Average drift: {avg_drift*1000:.2f} ms')
            print(f'Maximum drift: {max_drift*1000:.2f} ms')

def monitored_process(env, monitor, start_time, factor):
    for i in range(5):
        step_start = time.time()
        yield env.timeout(1)

        real_elapsed = time.time() - start_time
        expected_elapsed = env.now * factor
        monitor.record_step(env.now, real_elapsed, expected_elapsed)

        print(f'Sim time: {env.now}, Real time: {real_elapsed:.2f}s, ' +
              f'Expected: {expected_elapsed:.2f}s')

start = time.time()
factor = 1.0
env = simpy.rt.RealtimeEnvironment(factor=factor, strict=False)
monitor = RealTimeMonitor()

env.process(monitored_process(env, monitor, start, factor))
env.run()
monitor.report()
```

## Mixed Real-Time and Fast Simulation

```python
import simpy.rt

def background_simulation(env):
    """Fast background simulation."""
    for i in range(100):
        yield env.timeout(0.01)
    print(f'Background simulation completed at {env.now}')

def real_time_display(env):
    """Real-time display updates."""
    for i in range(5):
        print(f'Display update at {env.now}')
        yield env.timeout(1)

# Note: This is conceptual - SimPy doesn't directly support mixed modes
# Consider running separate simulations or using strict=False
env = simpy.rt.RealtimeEnvironment(factor=1.0, strict=False)
env.process(background_simulation(env))
env.process(real_time_display(env))
env.run()
```

## Converting Standard to Real-Time

Converting a standard simulation to real-time is straightforward:

```python
import simpy
import simpy.rt

def process(env):
    print(f'Event at {env.now}')
    yield env.timeout(1)
    print(f'Event at {env.now}')
    yield env.timeout(1)
    print(f'Event at {env.now}')

# Standard simulation (runs instantly)
print('Standard simulation:')
env = simpy.Environment()
env.process(process(env))
env.run()

# Real-time simulation (2 real seconds)
print('\nReal-time simulation:')
env_rt = simpy.rt.RealtimeEnvironment(factor=1.0)
env_rt.process(process(env_rt))
env_rt.run()
```

## Best Practices

1. **Factor selection**: Choose factor based on hardware/human constraints
   - Human interaction: `factor=1.0` (1:1 time mapping)
   - Fast hardware: `factor=0.01` (100x faster)
   - Slow processes: `factor=60` (1 sim unit = 1 minute)

2. **Strict mode usage**:
   - Use `strict=True` for timing validation
   - Use `strict=False` for development and variable workloads

3. **Computation budget**: Ensure process logic executes faster than timeout duration

4. **Error handling**: Wrap real-time runs in try-except for timing violations

5. **Testing strategy**:
   - Develop with standard Environment (fast iteration)
   - Test with RealtimeEnvironment (validation)
   - Deploy with appropriate factor and strict settings

6. **Performance monitoring**: Track drift between simulation and real time

7. **Graceful degradation**: Use `strict=False` when timing guarantees aren't critical

## Common Patterns

### Periodic Real-Time Tasks

```python
import simpy.rt

def periodic_task(env, name, period, duration):
    """Task that runs periodically in real-time."""
    while True:
        start = env.now
        print(f'{name}: Starting at {start}')

        # Simulate work
        yield env.timeout(duration)

        print(f'{name}: Completed at {env.now}')

        # Wait for next period
        elapsed = env.now - start
        wait_time = period - elapsed
        if wait_time > 0:
            yield env.timeout(wait_time)

env = simpy.rt.RealtimeEnvironment(factor=1.0)
env.process(periodic_task(env, 'Task', period=2.0, duration=0.5))
env.run(until=6)
```

### Synchronized Multi-Device Control

```python
import simpy.rt

def device_controller(env, device_id, update_rate):
    """Control loop for individual device."""
    while True:
        print(f'Device {device_id}: Update at {env.now}')
        yield env.timeout(update_rate)

# All devices synchronized to real-time
env = simpy.rt.RealtimeEnvironment(factor=1.0)

# Different update rates for different devices
env.process(device_controller(env, 'A', 1.0))
env.process(device_controller(env, 'B', 0.5))
env.process(device_controller(env, 'C', 2.0))

env.run(until=5)
```

## Limitations

1. **Performance**: Real-time simulation adds overhead; not suitable for high-frequency events
2. **Synchronization**: Single-threaded; all processes share same time base
3. **Precision**: Limited by Python's time resolution and system scheduling
4. **Strict mode**: May raise errors frequently with computationally intensive processes
5. **Platform-dependent**: Timing accuracy varies across operating systems

---

## Reference: Resources

# SimPy Shared Resources

This guide covers all resource types in SimPy for modeling congestion points and resource allocation.

## Resource Types Overview

SimPy provides three main categories of shared resources:

1. **Resources** - Limited capacity resources (e.g., gas pumps, servers)
2. **Containers** - Homogeneous bulk materials (e.g., fuel tanks, silos)
3. **Stores** - Python object storage (e.g., item queues, warehouses)

## 1. Resources

Model resources that can be used by a limited number of processes at a time.

### Resource (Basic)

The basic resource is a semaphore with specified capacity.

```python
import simpy

env = simpy.Environment()
resource = simpy.Resource(env, capacity=2)

def process(env, resource, name):
    with resource.request() as req:
        yield req
        print(f'{name} has the resource at {env.now}')
        yield env.timeout(5)
        print(f'{name} releases the resource at {env.now}')

env.process(process(env, resource, 'Process 1'))
env.process(process(env, resource, 'Process 2'))
env.process(process(env, resource, 'Process 3'))
env.run()
```

**Key properties:**
- `capacity` - Maximum number of concurrent users (default: 1)
- `count` - Current number of users
- `queue` - List of queued requests

### PriorityResource

Extends basic resource with priority levels (lower numbers = higher priority).

```python
import simpy

env = simpy.Environment()
resource = simpy.PriorityResource(env, capacity=1)

def process(env, resource, name, priority):
    with resource.request(priority=priority) as req:
        yield req
        print(f'{name} (priority {priority}) has the resource at {env.now}')
        yield env.timeout(5)

env.process(process(env, resource, 'Low priority', priority=10))
env.process(process(env, resource, 'High priority', priority=1))
env.run()
```

**Use cases:**
- Emergency services (ambulances before regular vehicles)
- VIP customer queues
- Job scheduling with priorities

### PreemptiveResource

Allows high-priority requests to interrupt lower-priority users.

```python
import simpy

env = simpy.Environment()
resource = simpy.PreemptiveResource(env, capacity=1)

def process(env, resource, name, priority):
    with resource.request(priority=priority) as req:
        try:
            yield req
            print(f'{name} acquired resource at {env.now}')
            yield env.timeout(10)
            print(f'{name} finished at {env.now}')
        except simpy.Interrupt:
            print(f'{name} was preempted at {env.now}')

env.process(process(env, resource, 'Low priority', priority=10))
env.process(process(env, resource, 'High priority', priority=1))
env.run()
```

**Use cases:**
- Operating system CPU scheduling
- Emergency room triage
- Network packet prioritization

## 2. Containers

Model production and consumption of homogeneous bulk materials (continuous or discrete).

```python
import simpy

env = simpy.Environment()
container = simpy.Container(env, capacity=100, init=50)

def producer(env, container):
    while True:
        yield env.timeout(5)
        yield container.put(20)
        print(f'Produced 20. Level: {container.level}')

def consumer(env, container):
    while True:
        yield env.timeout(7)
        yield container.get(15)
        print(f'Consumed 15. Level: {container.level}')

env.process(producer(env, container))
env.process(consumer(env, container))
env.run(until=50)
```

**Key properties:**
- `capacity` - Maximum amount (default: float('inf'))
- `level` - Current amount
- `init` - Initial amount (default: 0)

**Operations:**
- `put(amount)` - Add to container (blocks if full)
- `get(amount)` - Remove from container (blocks if insufficient)

**Use cases:**
- Gas station fuel tanks
- Buffer storage in manufacturing
- Water reservoirs
- Battery charge levels

## 3. Stores

Model production and consumption of Python objects.

### Store (Basic)

Generic FIFO object storage.

```python
import simpy

env = simpy.Environment()
store = simpy.Store(env, capacity=2)

def producer(env, store):
    for i in range(5):
        yield env.timeout(2)
        item = f'Item {i}'
        yield store.put(item)
        print(f'Produced {item} at {env.now}')

def consumer(env, store):
    while True:
        yield env.timeout(3)
        item = yield store.get()
        print(f'Consumed {item} at {env.now}')

env.process(producer(env, store))
env.process(consumer(env, store))
env.run()
```

**Key properties:**
- `capacity` - Maximum number of items (default: float('inf'))
- `items` - List of stored items

**Operations:**
- `put(item)` - Add item to store (blocks if full)
- `get()` - Remove and return item (blocks if empty)

### FilterStore

Allows retrieval of specific objects based on filter functions.

```python
import simpy

env = simpy.Environment()
store = simpy.FilterStore(env, capacity=10)

def producer(env, store):
    for color in ['red', 'blue', 'green', 'red', 'blue']:
        yield env.timeout(1)
        yield store.put({'color': color, 'time': env.now})
        print(f'Produced {color} item at {env.now}')

def consumer(env, store, color):
    while True:
        yield env.timeout(2)
        item = yield store.get(lambda x: x['color'] == color)
        print(f'{color} consumer got item from {item["time"]} at {env.now}')

env.process(producer(env, store))
env.process(consumer(env, store, 'red'))
env.process(consumer(env, store, 'blue'))
env.run(until=15)
```

**Use cases:**
- Warehouse item picking (specific SKUs)
- Job queues with skill matching
- Packet routing by destination

### PriorityStore

Items retrieved in priority order (lowest first).

```python
import simpy

class PriorityItem:
    def __init__(self, priority, data):
        self.priority = priority
        self.data = data

    def __lt__(self, other):
        return self.priority < other.priority

env = simpy.Environment()
store = simpy.PriorityStore(env, capacity=10)

def producer(env, store):
    items = [(10, 'Low'), (1, 'High'), (5, 'Medium')]
    for priority, name in items:
        yield env.timeout(1)
        yield store.put(PriorityItem(priority, name))
        print(f'Produced {name} priority item')

def consumer(env, store):
    while True:
        yield env.timeout(5)
        item = yield store.get()
        print(f'Retrieved {item.data} priority item')

env.process(producer(env, store))
env.process(consumer(env, store))
env.run()
```

**Use cases:**
- Task scheduling
- Print job queues
- Message prioritization

## Choosing the Right Resource Type

| Scenario | Resource Type |
|----------|---------------|
| Limited servers/machines | Resource |
| Priority-based queuing | PriorityResource |
| Preemptive scheduling | PreemptiveResource |
| Fuel, water, bulk materials | Container |
| Generic item queue (FIFO) | Store |
| Selective item retrieval | FilterStore |
| Priority-ordered items | PriorityStore |

## Best Practices

1. **Capacity planning**: Set realistic capacities based on system constraints
2. **Request patterns**: Use context managers (`with resource.request()`) for automatic cleanup
3. **Error handling**: Wrap preemptive resources in try-except for Interrupt handling
4. **Monitoring**: Track queue lengths and utilization (see monitoring.md)
5. **Performance**: FilterStore and PriorityStore have O(n) retrieval time; use wisely for large stores
