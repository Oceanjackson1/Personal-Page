---
title: "Rust Engineer"
description: "Writes, reviews, and debugs idiomatic Rust code with memory safety and zero-cost abstractions. Implements ownership patterns, manages lifetimes, designs trait hierarchies, builds async applications with tokio, and structures error handling with Re..."
category: "development"
source: "community"
author: "Community"
tags: ["rust", "engineer"]
date: 2026-03-20
---

# Rust Engineer

Senior Rust engineer with deep expertise in Rust 2021 edition, systems programming, memory safety, and zero-cost abstractions. Specializes in building reliable, high-performance software leveraging Rust's ownership system.

## Core Workflow

1. **Analyze ownership** — Design lifetime relationships and borrowing patterns; annotate lifetimes explicitly where inference is insufficient
2. **Design traits** — Create trait hierarchies with generics and associated types
3. **Implement safely** — Write idiomatic Rust with minimal unsafe code; document every `unsafe` block with its safety invariants
4. **Handle errors** — Use `Result`/`Option` with `?` operator and custom error types via `thiserror`
5. **Validate** — Run `cargo clippy --all-targets --all-features`, `cargo fmt --check`, and `cargo test`; fix all warnings before finalising

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Ownership | `references/ownership.md` | Lifetimes, borrowing, smart pointers, Pin |
| Traits | `references/traits.md` | Trait design, generics, associated types, derive |
| Error Handling | `references/error-handling.md` | Result, Option, ?, custom errors, thiserror |
| Async | `references/async.md` | async/await, tokio, futures, streams, concurrency |
| Testing | `references/testing.md` | Unit/integration tests, proptest, benchmarks |

## Key Patterns with Examples

### Ownership & Lifetimes

```rust
// Explicit lifetime annotation — borrow lives as long as the input slice
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Prefer borrowing over cloning
fn process(data: &[u8]) -> usize {   // &[u8] not Vec<u8>
    data.iter().filter(|&&b| b != 0).count()
}
```

### Trait-Based Design

```rust
use std::fmt;

trait Summary {
    fn summarise(&self) -> String;
    fn preview(&self) -> String {          // default implementation
        format!("{}...", &self.summarise()[..50])
    }
}

#[derive(Debug)]
struct Article { title: String, body: String }

impl Summary for Article {
    fn summarise(&self) -> String {
        format!("{}: {}", self.title, self.body)
    }
}
```

### Error Handling with `thiserror`

```rust
use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("I/O error: {0}")]
    Io(#[from] std::io::Error),
    #[error("parse error for value `{value}`: {reason}")]
    Parse { value: String, reason: String },
}

// ? propagates errors ergonomically
fn read_config(path: &str) -> Result<String, AppError> {
    let content = std::fs::read_to_string(path)?;  // Io variant via #[from]
    Ok(content)
}
```

### Async / Await with Tokio

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let result = fetch_data("https://example.com").await?;
    println!("{result}");
    Ok(())
}

async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let body = reqwest::get(url).await?.text().await?;
    Ok(body)
}

// Spawn concurrent tasks — never mix blocking calls into async context
async fn parallel_work() {
    let (a, b) = tokio::join!(
        sleep(Duration::from_millis(100)),
        sleep(Duration::from_millis(100)),
    );
}
```

### Validation Commands

```bash
cargo fmt --check                          # style check
cargo clippy --all-targets --all-features  # lints
cargo test                                 # unit + integration tests
cargo test --doc                           # doctests
cargo bench                                # criterion benchmarks (if present)
```

## Constraints

### MUST DO
- Use ownership and borrowing for memory safety
- Minimize unsafe code (document all unsafe blocks with safety invariants)
- Use type system for compile-time guarantees
- Handle all errors explicitly (`Result`/`Option`)
- Add comprehensive documentation with examples
- Run `cargo clippy` and fix all warnings
- Use `cargo fmt` for consistent formatting
- Write tests including doctests

### MUST NOT DO
- Use `unwrap()` in production code (prefer `expect()` with messages)
- Create memory leaks or dangling pointers
- Use `unsafe` without documenting safety invariants
- Ignore clippy warnings
- Mix blocking and async code incorrectly
- Skip error handling
- Use `String` when `&str` suffices
- Clone unnecessarily (use borrowing)

## Output Templates

When implementing Rust features, provide:
1. Type definitions (structs, enums, traits)
2. Implementation with proper ownership
3. Error handling with custom error types
4. Tests (unit, integration, doctests)
5. Brief explanation of design decisions

## Knowledge Reference

Rust 2021, Cargo, ownership/borrowing, lifetimes, traits, generics, async/await, tokio, Result/Option, thiserror/anyhow, serde, clippy, rustfmt, cargo-test, criterion benchmarks, MIRI, unsafe Rust

---

## Reference: Async

# Async Programming in Rust

## Basic Async/Await

```rust
use tokio;

// Async function returns a Future
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}

// Tokio runtime
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let data = fetch_data("https://api.example.com").await?;
    println!("Data: {}", data);
    Ok(())
}

// Manual runtime creation
fn main() {
    let runtime = tokio::runtime::Runtime::new().unwrap();
    runtime.block_on(async {
        println!("Hello from async context");
    });
}
```

## Concurrent Execution

```rust
use tokio;

// Sequential execution
async fn sequential() {
    let result1 = async_operation1().await;
    let result2 = async_operation2().await;  // Waits for operation1
}

// Concurrent execution with join!
async fn concurrent() {
    let (result1, result2) = tokio::join!(
        async_operation1(),
        async_operation2()
    );
}

// Concurrent with try_join! (stops on first error)
async fn concurrent_with_errors() -> Result<(), Box<dyn std::error::Error>> {
    let (result1, result2) = tokio::try_join!(
        fallible_operation1(),
        fallible_operation2()
    )?;
    Ok(())
}

// Spawning tasks
async fn spawn_tasks() {
    let handle1 = tokio::spawn(async {
        // This runs on a separate task
        expensive_computation().await
    });

    let handle2 = tokio::spawn(async {
        another_computation().await
    });

    // Wait for both to complete
    let result1 = handle1.await.unwrap();
    let result2 = handle2.await.unwrap();
}
```

## Select and Race Conditions

```rust
use tokio::time::{sleep, Duration};

// select! - wait for first to complete
async fn first_to_complete() {
    tokio::select! {
        result = async_operation1() => {
            println!("Operation 1 completed first: {:?}", result);
        }
        result = async_operation2() => {
            println!("Operation 2 completed first: {:?}", result);
        }
    }
}

// Timeout pattern
async fn with_timeout() -> Result<String, &'static str> {
    tokio::select! {
        result = fetch_data("https://api.example.com") => {
            result.map_err(|_| "Fetch failed")
        }
        _ = sleep(Duration::from_secs(5)) => {
            Err("Timeout")
        }
    }
}

// Cancellation with select!
async fn cancellable_operation(mut cancel_rx: tokio::sync::watch::Receiver<bool>) {
    tokio::select! {
        result = long_running_task() => {
            println!("Task completed: {:?}", result);
        }
        _ = cancel_rx.changed() => {
            println!("Task cancelled");
        }
    }
}
```

## Streams

```rust
use tokio_stream::{self as stream, StreamExt};

// Creating streams
async fn stream_example() {
    let mut stream = stream::iter(vec![1, 2, 3, 4, 5]);

    while let Some(value) = stream.next().await {
        println!("Value: {}", value);
    }
}

// Stream combinators
async fn stream_combinators() {
    let stream = stream::iter(vec![1, 2, 3, 4, 5])
        .filter(|x| *x % 2 == 0)
        .map(|x| x * 2);

    let results: Vec<_> = stream.collect().await;
    println!("Results: {:?}", results);
}

// Async stream processing
use futures::stream::{self, StreamExt};

async fn process_stream() {
    let stream = stream::iter(vec![1, 2, 3, 4, 5])
        .then(|x| async move {
            tokio::time::sleep(Duration::from_millis(100)).await;
            x * 2
        });

    stream.for_each(|x| async move {
        println!("Processed: {}", x);
    }).await;
}
```

## Channels for Communication

```rust
use tokio::sync::{mpsc, oneshot, broadcast, watch};

// mpsc: multiple producer, single consumer
async fn mpsc_example() {
    let (tx, mut rx) = mpsc::channel(32);

    tokio::spawn(async move {
        tx.send("Hello").await.unwrap();
        tx.send("World").await.unwrap();
    });

    while let Some(msg) = rx.recv().await {
        println!("Received: {}", msg);
    }
}

// oneshot: single value, one-time use
async fn oneshot_example() {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        tx.send("Result").unwrap();
    });

    let result = rx.await.unwrap();
    println!("Got: {}", result);
}

// broadcast: multiple producers, multiple consumers
async fn broadcast_example() {
    let (tx, mut rx1) = broadcast::channel(16);
    let mut rx2 = tx.subscribe();

    tokio::spawn(async move {
        tx.send("Message").unwrap();
    });

    println!("rx1: {}", rx1.recv().await.unwrap());
    println!("rx2: {}", rx2.recv().await.unwrap());
}

// watch: single producer, multiple consumers (last value)
async fn watch_example() {
    let (tx, mut rx) = watch::channel("initial");

    tokio::spawn(async move {
        loop {
            rx.changed().await.unwrap();
            println!("Value changed to: {}", *rx.borrow());
        }
    });

    tx.send("updated").unwrap();
}
```

## Shared State

```rust
use std::sync::Arc;
use tokio::sync::{Mutex, RwLock};

// Mutex for exclusive access
async fn mutex_example() {
    let data = Arc::new(Mutex::new(0));

    let mut handles = vec![];

    for _ in 0..10 {
        let data = Arc::clone(&data);
        let handle = tokio::spawn(async move {
            let mut lock = data.lock().await;
            *lock += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.await.unwrap();
    }

    println!("Final value: {}", *data.lock().await);
}

// RwLock for read-write patterns
async fn rwlock_example() {
    let data = Arc::new(RwLock::new(vec![1, 2, 3]));

    // Multiple readers
    let data1 = Arc::clone(&data);
    tokio::spawn(async move {
        let read = data1.read().await;
        println!("Read: {:?}", *read);
    });

    let data2 = Arc::clone(&data);
    tokio::spawn(async move {
        let read = data2.read().await;
        println!("Read: {:?}", *read);
    });

    // Single writer
    tokio::time::sleep(Duration::from_millis(100)).await;
    let mut write = data.write().await;
    write.push(4);
}
```

## Async Traits (with async-trait)

```rust
use async_trait::async_trait;

#[async_trait]
trait AsyncRepository {
    async fn find_by_id(&self, id: u64) -> Result<User, Error>;
    async fn save(&self, user: User) -> Result<(), Error>;
}

struct DatabaseRepository {
    pool: sqlx::PgPool,
}

#[async_trait]
impl AsyncRepository for DatabaseRepository {
    async fn find_by_id(&self, id: u64) -> Result<User, Error> {
        sqlx::query_as("SELECT * FROM users WHERE id = $1")
            .bind(id)
            .fetch_one(&self.pool)
            .await
            .map_err(Into::into)
    }

    async fn save(&self, user: User) -> Result<(), Error> {
        sqlx::query("INSERT INTO users (name, email) VALUES ($1, $2)")
            .bind(&user.name)
            .bind(&user.email)
            .execute(&self.pool)
            .await?;
        Ok(())
    }
}
```

## Pin and Futures

```rust
use std::pin::Pin;
use std::future::Future;
use std::task::{Context, Poll};

// Manual Future implementation
struct DelayedValue {
    value: i32,
    delay: tokio::time::Sleep,
}

impl Future for DelayedValue {
    type Output = i32;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        match Pin::new(&mut self.delay).poll(cx) {
            Poll::Ready(_) => Poll::Ready(self.value),
            Poll::Pending => Poll::Pending,
        }
    }
}

// Using pinned futures
async fn use_pinned() {
    let future = DelayedValue {
        value: 42,
        delay: tokio::time::sleep(Duration::from_secs(1)),
    };

    let result = future.await;
    println!("Result: {}", result);
}
```

## Background Tasks and Graceful Shutdown

```rust
use tokio::signal;

async fn background_task(mut shutdown: tokio::sync::watch::Receiver<bool>) {
    loop {
        tokio::select! {
            _ = tokio::time::sleep(Duration::from_secs(1)) => {
                println!("Background task running...");
            }
            _ = shutdown.changed() => {
                println!("Shutting down background task");
                break;
            }
        }
    }
}

#[tokio::main]
async fn main() {
    let (shutdown_tx, shutdown_rx) = tokio::sync::watch::channel(false);

    let task = tokio::spawn(background_task(shutdown_rx));

    // Wait for ctrl-c
    signal::ctrl_c().await.unwrap();
    println!("Received shutdown signal");

    // Signal shutdown
    shutdown_tx.send(true).unwrap();

    // Wait for task to complete
    task.await.unwrap();
}
```

## Error Handling in Async

```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum AsyncError {
    #[error("Network error: {0}")]
    Network(#[from] reqwest::Error),

    #[error("Timeout")]
    Timeout,

    #[error("Task failed")]
    TaskFailed(#[from] tokio::task::JoinError),
}

async fn robust_operation() -> Result<String, AsyncError> {
    let timeout = Duration::from_secs(5);

    let result = tokio::time::timeout(timeout, async {
        reqwest::get("https://api.example.com")
            .await?
            .text()
            .await
    })
    .await
    .map_err(|_| AsyncError::Timeout)??;

    Ok(result)
}
```

## Runtime Configuration

```rust
// Custom runtime configuration
fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .thread_name("my-worker")
        .thread_stack_size(3 * 1024 * 1024)
        .enable_all()
        .build()
        .unwrap();

    runtime.block_on(async {
        println!("Running on custom runtime");
    });
}

// Current-thread runtime (single-threaded)
fn single_threaded() {
    let runtime = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap();

    runtime.block_on(async {
        println!("Single-threaded async");
    });
}
```

## Best Practices

- Use tokio::spawn for CPU-bound tasks on multi-threaded runtime
- Use spawn_blocking for blocking operations (file I/O, sync code)
- Prefer tokio::sync primitives over std::sync in async code
- Use channels for task communication instead of shared state when possible
- Always handle JoinHandle results (tasks can panic)
- Use select! for cancellation patterns
- Avoid holding locks across .await points
- Use timeout for all external I/O operations
- Implement graceful shutdown with channels
- Use async-trait for trait-based async code
- Prefer try_join! over manual error handling
- Use Arc<Mutex<T>> sparingly (channels often better)
- Test async code with tokio::test macro
- Monitor task spawning to prevent unbounded growth

---

## Reference: Error Handling

# Error Handling in Rust

## Result and Option Basics

```rust
// Result: operation that can fail
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

// Option: value that might be absent
fn find_user(id: u64) -> Option<User> {
    if id == 1 {
        Some(User { id, name: "Alice".to_string() })
    } else {
        None
    }
}

// Using ? operator for propagation
fn calculate(a: f64, b: f64, c: f64) -> Result<f64, String> {
    let x = divide(a, b)?;  // Returns Err early if division fails
    let y = divide(x, c)?;
    Ok(y)
}
```

## Custom Error Types

```rust
use std::fmt;

// Manual error type
#[derive(Debug)]
enum AppError {
    NotFound(String),
    InvalidInput(String),
    DatabaseError(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            AppError::NotFound(msg) => write!(f, "Not found: {}", msg),
            AppError::InvalidInput(msg) => write!(f, "Invalid input: {}", msg),
            AppError::DatabaseError(msg) => write!(f, "Database error: {}", msg),
        }
    }
}

impl std::error::Error for AppError {}

// Usage
fn get_user(id: u64) -> Result<User, AppError> {
    if id == 0 {
        return Err(AppError::InvalidInput("ID cannot be zero".to_string()));
    }
    // ... fetch user
    Err(AppError::NotFound(format!("User {} not found", id)))
}
```

## Using thiserror

```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum DataError {
    #[error("Data not found: {0}")]
    NotFound(String),

    #[error("Invalid ID: {id}, reason: {reason}")]
    InvalidId { id: u64, reason: String },

    #[error("IO error")]
    Io(#[from] std::io::Error),

    #[error("Parse error")]
    Parse(#[from] std::num::ParseIntError),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
}

// Usage with automatic conversions
fn read_config(path: &str) -> Result<Config, DataError> {
    let content = std::fs::read_to_string(path)?;  // Auto-converts io::Error
    let port: u16 = content.parse()?;  // Auto-converts ParseIntError
    Ok(Config { port })
}
```

## Using anyhow for Applications

```rust
use anyhow::{Result, Context, bail, ensure};

// Simple error handling for applications
fn process_file(path: &str) -> Result<()> {
    let content = std::fs::read_to_string(path)
        .context(format!("Failed to read file: {}", path))?;

    ensure!(!content.is_empty(), "File is empty");

    if content.len() > 1000 {
        bail!("File too large");
    }

    // Process content...
    Ok(())
}

// Adding context to errors
fn main() -> Result<()> {
    process_file("config.txt")
        .context("Failed to process configuration")?;
    Ok(())
}
```

## Option Combinators

```rust
// map: transform Option<T> to Option<U>
let num: Option<i32> = Some(5);
let doubled = num.map(|n| n * 2);  // Some(10)

// and_then: chain operations
let result = Some(5)
    .and_then(|n| if n > 0 { Some(n * 2) } else { None })
    .and_then(|n| Some(n + 1));  // Some(11)

// or: provide alternative
let value = None.or(Some(42));  // Some(42)

// unwrap_or: provide default
let value = None.unwrap_or(42);  // 42

// unwrap_or_else: compute default lazily
let value = None.unwrap_or_else(|| expensive_computation());

// filter: conditional None
let num = Some(5).filter(|&n| n > 10);  // None

// Pattern matching
match find_user(1) {
    Some(user) => println!("Found: {}", user.name),
    None => println!("User not found"),
}

// if let for simple cases
if let Some(user) = find_user(1) {
    println!("Found: {}", user.name);
}
```

## Result Combinators

```rust
// map: transform Ok value
let result: Result<i32, String> = Ok(5);
let doubled = result.map(|n| n * 2);  // Ok(10)

// map_err: transform error
let result: Result<i32, &str> = Err("error");
let mapped = result.map_err(|e| e.to_uppercase());  // Err("ERROR")

// and_then: chain fallible operations
fn parse_then_double(s: &str) -> Result<i32, std::num::ParseIntError> {
    s.parse::<i32>()
        .and_then(|n| Ok(n * 2))
}

// or_else: provide alternative computation
let result = Err("error").or_else(|_| Ok(42));  // Ok(42)

// unwrap_or: provide default
let value = Err("error").unwrap_or(42);  // 42

// expect: unwrap with custom panic message
let value = result.expect("Failed to parse number");

// Pattern matching
match divide(10.0, 2.0) {
    Ok(result) => println!("Result: {}", result),
    Err(e) => eprintln!("Error: {}", e),
}
```

## Error Conversion and From Trait

```rust
use std::io;
use std::num::ParseIntError;

#[derive(Debug)]
enum MyError {
    Io(io::Error),
    Parse(ParseIntError),
}

impl From<io::Error> for MyError {
    fn from(err: io::Error) -> Self {
        MyError::Io(err)
    }
}

impl From<ParseIntError> for MyError {
    fn from(err: ParseIntError) -> Self {
        MyError::Parse(err)
    }
}

// Now ? operator works with automatic conversion
fn read_and_parse(path: &str) -> Result<i32, MyError> {
    let content = std::fs::read_to_string(path)?;  // io::Error -> MyError
    let number = content.trim().parse()?;  // ParseIntError -> MyError
    Ok(number)
}
```

## Advanced Error Patterns

```rust
// Multiple error sources with Box<dyn Error>
use std::error::Error;

fn complex_operation() -> Result<String, Box<dyn Error>> {
    let file = std::fs::read_to_string("data.txt")?;
    let number: i32 = file.trim().parse()?;
    Ok(format!("Number: {}", number))
}

// Error with backtrace (nightly)
#[derive(Debug)]
struct DetailedError {
    message: String,
    backtrace: std::backtrace::Backtrace,
}

impl DetailedError {
    fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
            backtrace: std::backtrace::Backtrace::capture(),
        }
    }
}

// Recoverable vs unrecoverable errors
fn might_fail(value: i32) -> Result<i32, String> {
    if value < 0 {
        Err("Negative value".to_string())  // Recoverable
    } else if value > 1000 {
        panic!("Value too large!");  // Unrecoverable
    } else {
        Ok(value * 2)
    }
}
```

## Try Blocks (Nightly)

```rust
#![feature(try_blocks)]

// Try block for localized error handling
let result: Result<i32, Box<dyn Error>> = try {
    let file = std::fs::read_to_string("config.txt")?;
    let num: i32 = file.trim().parse()?;
    num * 2
};
```

## Error Context Pattern

```rust
use thiserror::Error;

#[derive(Error, Debug)]
#[error("{message}")]
struct ContextError {
    message: String,
    #[source]
    source: Option<Box<dyn Error + Send + Sync>>,
}

impl ContextError {
    fn new(message: impl Into<String>) -> Self {
        Self {
            message: message.into(),
            source: None,
        }
    }

    fn with_source(mut self, source: impl Error + Send + Sync + 'static) -> Self {
        self.source = Some(Box::new(source));
        self
    }
}

// Extension trait for adding context
trait Context<T> {
    fn context(self, message: impl Into<String>) -> Result<T, ContextError>;
}

impl<T, E: Error + Send + Sync + 'static> Context<T> for Result<T, E> {
    fn context(self, message: impl Into<String>) -> Result<T, ContextError> {
        self.map_err(|e| ContextError::new(message).with_source(e))
    }
}
```

## Best Practices

- Use Result for recoverable errors, panic! for unrecoverable bugs
- Prefer ? operator over unwrap() in production code
- Use expect() with descriptive messages instead of unwrap()
- Use thiserror for libraries (structured errors)
- Use anyhow for applications (simple error handling)
- Implement std::error::Error trait for custom error types
- Add context to errors as they propagate up the stack
- Use #[from] in thiserror for automatic conversions
- Document error conditions in function documentation
- Use Option::ok_or() to convert Option to Result
- Use Result::ok() to convert Result to Option (discarding error)
- Avoid String as error type (use custom types instead)
- Use ensure! and bail! from anyhow for cleaner checks
- Log errors at boundaries, return them in library code

---

## Reference: Ownership

# Ownership, Borrowing, and Lifetimes

## Ownership Patterns

```rust
// Move semantics (ownership transfer)
fn take_ownership(s: String) {
    println!("{}", s);
} // s dropped here

// Borrowing (immutable reference)
fn borrow(s: &String) {
    println!("{}", s);
} // s NOT dropped, caller still owns

// Mutable borrowing
fn borrow_mut(s: &mut String) {
    s.push_str(" world");
}

// Usage
let s = String::from("hello");
borrow(&s);           // OK, immutable borrow
let mut s2 = s;       // Move, s no longer valid
borrow_mut(&mut s2);  // OK, mutable borrow
```

## Lifetime Annotations

```rust
// Explicit lifetime: returned reference lives as long as input
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Multiple lifetimes
fn first_word<'a, 'b>(s: &'a str, _other: &'b str) -> &'a str {
    s.split_whitespace().next().unwrap_or("")
}

// Lifetime in structs
struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    fn announce_and_return(&self, announcement: &str) -> &'a str {
        println!("Attention: {}", announcement);
        self.part
    }
}

// Static lifetime (lives for entire program)
const GREETING: &'static str = "Hello, world!";
```

## Smart Pointers

```rust
use std::rc::Rc;
use std::cell::RefCell;
use std::sync::{Arc, Mutex};

// Box: heap allocation, single owner
let b = Box::new(5);

// Rc: reference counting (single-threaded)
let rc1 = Rc::new(vec![1, 2, 3]);
let rc2 = Rc::clone(&rc1);  // Increment count
println!("Count: {}", Rc::strong_count(&rc1));  // 2

// Arc: atomic reference counting (thread-safe)
let arc1 = Arc::new(vec![1, 2, 3]);
let arc2 = Arc::clone(&arc1);
std::thread::spawn(move || {
    println!("{:?}", arc2);
});

// RefCell: interior mutability (runtime borrow checking)
let data = RefCell::new(5);
*data.borrow_mut() += 1;  // Mutable borrow at runtime

// Combining Rc + RefCell for shared mutable state
let shared = Rc::new(RefCell::new(vec![1, 2, 3]));
shared.borrow_mut().push(4);

// Combining Arc + Mutex for thread-safe shared state
let counter = Arc::new(Mutex::new(0));
let counter_clone = Arc::clone(&counter);
std::thread::spawn(move || {
    let mut num = counter_clone.lock().unwrap();
    *num += 1;
});
```

## Interior Mutability

```rust
use std::cell::{Cell, RefCell};

// Cell: Copy types only
let c = Cell::new(5);
c.set(10);
let val = c.get();

// RefCell: runtime borrow checking
let data = RefCell::new(vec![1, 2, 3]);
data.borrow_mut().push(4);

// Pattern: mock objects with interior mutability
struct MockLogger {
    messages: RefCell<Vec<String>>,
}

impl MockLogger {
    fn new() -> Self {
        Self { messages: RefCell::new(Vec::new()) }
    }

    fn log(&self, msg: &str) {
        self.messages.borrow_mut().push(msg.to_string());
    }

    fn get_messages(&self) -> Vec<String> {
        self.messages.borrow().clone()
    }
}
```

## Pin and Self-Referential Types

```rust
use std::pin::Pin;
use std::marker::PhantomPinned;

// Self-referential struct (requires Pin)
struct SelfReferential {
    data: String,
    pointer: *const String,
    _pin: PhantomPinned,
}

impl SelfReferential {
    fn new(data: String) -> Pin<Box<Self>> {
        let mut boxed = Box::pin(Self {
            data,
            pointer: std::ptr::null(),
            _pin: PhantomPinned,
        });

        // Safe: we're not moving the data after this
        let ptr = &boxed.data as *const String;
        unsafe {
            let mut_ref = Pin::as_mut(&mut boxed);
            Pin::get_unchecked_mut(mut_ref).pointer = ptr;
        }

        boxed
    }
}

// Pin in async contexts
async fn pinned_future() {
    // Futures are often self-referential, hence Pin
    let fut = async { 42 };
    let pinned = Box::pin(fut);
    pinned.await;
}
```

## Cow (Clone on Write)

```rust
use std::borrow::Cow;

fn process_text(input: &str) -> Cow<str> {
    if input.contains("bad") {
        // Need to modify: allocate new String
        Cow::Owned(input.replace("bad", "good"))
    } else {
        // No modification needed: just borrow
        Cow::Borrowed(input)
    }
}

// Usage
let text1 = "hello world";
let result1 = process_text(text1);  // Borrowed (no allocation)

let text2 = "bad word";
let result2 = process_text(text2);  // Owned (allocated)
```

## Drop Trait and RAII

```rust
struct FileGuard {
    name: String,
}

impl FileGuard {
    fn new(name: String) -> Self {
        println!("Opening {}", name);
        Self { name }
    }
}

impl Drop for FileGuard {
    fn drop(&mut self) {
        println!("Closing {}", self.name);
    }
}

// Usage: automatic cleanup
{
    let _file = FileGuard::new("data.txt".to_string());
    // Use file...
} // Drop called automatically here
```

## Common Patterns

```rust
// Builder pattern with ownership
struct Config {
    host: String,
    port: u16,
}

impl Config {
    fn builder() -> ConfigBuilder {
        ConfigBuilder::default()
    }
}

struct ConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
}

impl ConfigBuilder {
    fn host(mut self, host: impl Into<String>) -> Self {
        self.host = Some(host.into());
        self
    }

    fn port(mut self, port: u16) -> Self {
        self.port = Some(port);
        self
    }

    fn build(self) -> Result<Config, &'static str> {
        Ok(Config {
            host: self.host.ok_or("host required")?,
            port: self.port.unwrap_or(8080),
        })
    }
}

// Usage
let config = Config::builder()
    .host("localhost")
    .port(3000)
    .build()?;
```

## Best Practices

- Prefer borrowing (&T) over ownership transfer when possible
- Use &str over String for function parameters
- Use &[T] over Vec<T> for function parameters
- Clone only when necessary (profile first)
- Use Cow<'a, T> for conditional cloning
- Document lifetime relationships in complex cases
- Use Arc<Mutex<T>> for shared mutable state across threads
- Use Rc<RefCell<T>> for shared mutable state in single thread
- Implement Drop for RAII patterns
- Use PhantomData to constrain variance when needed

---

## Reference: Testing

# Testing in Rust

## Unit Tests

```rust
// Tests in same file
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_addition() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    fn test_subtraction() {
        assert!(10 - 5 == 5);
    }

    #[test]
    #[should_panic(expected = "division by zero")]
    fn test_panic() {
        divide(10, 0);
    }

    #[test]
    fn test_result() -> Result<(), String> {
        let result = divide(10, 2)?;
        assert_eq!(result, 5);
        Ok(())
    }

    #[test]
    #[ignore]
    fn expensive_test() {
        // Run with: cargo test -- --ignored
    }
}

// Assertions
fn assert_examples() {
    assert!(true);
    assert_eq!(2 + 2, 4);
    assert_ne!(2 + 2, 5);

    // Custom messages
    assert!(value > 0, "Value must be positive, got {}", value);
    assert_eq!(result, expected, "Calculation failed");
}
```

## Doctests

```rust
/// Adds two numbers together.
///
/// # Examples
///
/// ```
/// use mylib::add;
///
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
///
/// ```should_panic
/// use mylib::divide;
///
/// divide(10, 0);  // This will panic
/// ```
///
/// ```ignore
/// // This code won't compile but won't fail the test
/// let x = undefined_function();
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## Integration Tests

```rust
// tests/integration_test.rs
use mylib;

#[test]
fn test_full_workflow() {
    let config = mylib::Config::new("test.conf");
    let result = mylib::process(&config);
    assert!(result.is_ok());
}

// tests/common/mod.rs - shared test utilities
pub fn setup() -> TestContext {
    TestContext {
        db: create_test_db(),
    }
}

// tests/another_test.rs
mod common;

#[test]
fn test_with_common() {
    let ctx = common::setup();
    // Use ctx...
}
```

## Test Organization

```rust
// Nested test modules
#[cfg(test)]
mod tests {
    use super::*;

    mod addition {
        use super::*;

        #[test]
        fn positive_numbers() {
            assert_eq!(add(2, 3), 5);
        }

        #[test]
        fn negative_numbers() {
            assert_eq!(add(-2, -3), -5);
        }
    }

    mod subtraction {
        use super::*;

        #[test]
        fn test_subtract() {
            assert_eq!(subtract(10, 5), 5);
        }
    }
}
```

## Test Fixtures and Setup

```rust
struct TestContext {
    temp_dir: std::path::PathBuf,
    db: Database,
}

impl TestContext {
    fn setup() -> Self {
        let temp_dir = std::env::temp_dir().join("test");
        std::fs::create_dir_all(&temp_dir).unwrap();

        Self {
            temp_dir,
            db: Database::connect_test(),
        }
    }
}

impl Drop for TestContext {
    fn drop(&mut self) {
        // Cleanup
        std::fs::remove_dir_all(&self.temp_dir).ok();
        self.db.disconnect();
    }
}

#[test]
fn test_with_fixture() {
    let ctx = TestContext::setup();
    // Test uses ctx...
    // Automatic cleanup via Drop
}
```

## Async Tests

```rust
use tokio;

#[tokio::test]
async fn test_async_function() {
    let result = async_operation().await;
    assert_eq!(result, 42);
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_with_custom_runtime() {
    let result = concurrent_operation().await;
    assert!(result.is_ok());
}

// Testing async with timeout
#[tokio::test]
async fn test_with_timeout() {
    let timeout = std::time::Duration::from_secs(5);
    let result = tokio::time::timeout(timeout, slow_operation()).await;
    assert!(result.is_ok());
}
```

## Property-Based Testing (proptest)

```rust
use proptest::prelude::*;

// Simple property test
proptest! {
    #[test]
    fn test_reversing_twice_is_identity(ref s in ".*") {
        let reversed: String = s.chars().rev().collect();
        let double_reversed: String = reversed.chars().rev().collect();
        assert_eq!(s, &double_reversed);
    }
}

// Custom strategies
proptest! {
    #[test]
    fn test_addition_commutative(a in 0..1000i32, b in 0..1000i32) {
        assert_eq!(a + b, b + a);
    }

    #[test]
    fn test_vector_push_pop(
        ref v in prop::collection::vec(0..100i32, 0..100),
        item in 0..100i32
    ) {
        let mut v = v.clone();
        v.push(item);
        assert_eq!(v.pop(), Some(item));
    }
}

// Complex custom strategies
fn user_strategy() -> impl Strategy<Value = User> {
    (1..1000u64, "[a-z]{3,10}", "[a-z0-9.]+@[a-z]+\\.[a-z]+")
        .prop_map(|(id, name, email)| User { id, name, email })
}

proptest! {
    #[test]
    fn test_user_serialization(user in user_strategy()) {
        let json = serde_json::to_string(&user).unwrap();
        let deserialized: User = serde_json::from_str(&json).unwrap();
        assert_eq!(user, deserialized);
    }
}
```

## Mocking

```rust
// Using mockall
use mockall::*;
use mockall::predicate::*;

#[automock]
trait Database {
    fn get_user(&self, id: u64) -> Option<User>;
    fn save_user(&mut self, user: User) -> Result<(), Error>;
}

#[test]
fn test_with_mock() {
    let mut mock = MockDatabase::new();

    mock.expect_get_user()
        .with(eq(1))
        .times(1)
        .returning(|_| Some(User { id: 1, name: "Alice".to_string() }));

    mock.expect_save_user()
        .times(1)
        .returning(|_| Ok(()));

    // Use mock in test
    let user = mock.get_user(1);
    assert!(user.is_some());
}
```

## Benchmarks (Criterion)

```rust
// benches/my_benchmark.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 1,
        1 => 1,
        n => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn criterion_benchmark(c: &mut Criterion) {
    c.bench_function("fib 20", |b| b.iter(|| fibonacci(black_box(20))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);

// Cargo.toml:
// [dev-dependencies]
// criterion = "0.5"
//
// [[bench]]
// name = "my_benchmark"
// harness = false
```

## Advanced Benchmarking

```rust
use criterion::{BenchmarkId, Criterion, criterion_group, criterion_main};

fn bench_multiple_sizes(c: &mut Criterion) {
    let mut group = c.benchmark_group("sorting");

    for size in [10, 100, 1000, 10000].iter() {
        group.bench_with_input(BenchmarkId::from_parameter(size), size, |b, &size| {
            b.iter_batched(
                || generate_random_vec(size),
                |mut v| v.sort(),
                criterion::BatchSize::SmallInput,
            );
        });
    }

    group.finish();
}

// Comparing implementations
fn bench_comparison(c: &mut Criterion) {
    let mut group = c.benchmark_group("string_search");

    group.bench_function("naive", |b| {
        b.iter(|| naive_search(black_box("haystack"), black_box("needle")))
    });

    group.bench_function("optimized", |b| {
        b.iter(|| optimized_search(black_box("haystack"), black_box("needle")))
    });

    group.finish();
}

criterion_group!(benches, bench_multiple_sizes, bench_comparison);
criterion_main!(benches);
```

## Testing with External Resources

```rust
// Testing file I/O
#[test]
fn test_file_operations() {
    use std::io::Write;

    let temp_dir = std::env::temp_dir();
    let file_path = temp_dir.join("test_file.txt");

    // Write
    let mut file = std::fs::File::create(&file_path).unwrap();
    file.write_all(b"test content").unwrap();

    // Read
    let content = std::fs::read_to_string(&file_path).unwrap();
    assert_eq!(content, "test content");

    // Cleanup
    std::fs::remove_file(&file_path).unwrap();
}

// Testing with databases (using sqlx)
#[sqlx::test]
async fn test_database_operations(pool: sqlx::PgPool) -> sqlx::Result<()> {
    sqlx::query("INSERT INTO users (name) VALUES ($1)")
        .bind("Alice")
        .execute(&pool)
        .await?;

    let count: (i64,) = sqlx::query_as("SELECT COUNT(*) FROM users")
        .fetch_one(&pool)
        .await?;

    assert_eq!(count.0, 1);
    Ok(())
}
```

## Snapshot Testing

```rust
// Using insta crate
use insta::assert_snapshot;

#[test]
fn test_output_format() {
    let data = generate_complex_output();
    assert_snapshot!(data);
}

#[test]
fn test_json_output() {
    let json = serde_json::to_string_pretty(&get_data()).unwrap();
    assert_snapshot!(json);
}

// Run with: cargo insta test
// Review snapshots: cargo insta review
```

## Code Coverage

```rust
// Using tarpaulin
// cargo install cargo-tarpaulin
// cargo tarpaulin --out Html --output-dir coverage

// Using llvm-cov
// cargo install cargo-llvm-cov
// cargo llvm-cov --html
```

## Fuzzing

```rust
// Using cargo-fuzz
// cargo install cargo-fuzz
// cargo fuzz init

// fuzz/fuzz_targets/fuzz_target_1.rs
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(s) = std::str::from_utf8(data) {
        let _ = mylib::parse_input(s);
    }
});

// Run with: cargo fuzz run fuzz_target_1
```

## Best Practices

- Write tests alongside production code in #[cfg(test)] modules
- Use integration tests in tests/ directory for end-to-end testing
- Include doctests in documentation for examples that must work
- Use descriptive test names that explain what is being tested
- Test edge cases (empty inputs, max values, etc.)
- Use property-based testing for algorithmic code
- Benchmark performance-critical code with criterion
- Run tests in CI with cargo test --all-features
- Use cargo test -- --nocapture to see println! output
- Test error conditions with #[should_panic] or Result
- Mock external dependencies for unit tests
- Use test fixtures for complex setup/teardown
- Run clippy on test code too
- Measure code coverage and aim for high coverage
- Use fuzzing for security-critical parsers
- Test async code with tokio::test
- Use snapshot testing for complex output validation

---

## Reference: Traits

# Traits, Generics, and Type System

## Basic Trait Definition

```rust
// Simple trait
trait Drawable {
    fn draw(&self);
}

// Trait with default implementation
trait Describable {
    fn describe(&self) -> String {
        String::from("No description available")
    }
}

// Implementing traits
struct Circle {
    radius: f64,
}

impl Drawable for Circle {
    fn draw(&self) {
        println!("Drawing circle with radius {}", self.radius);
    }
}

impl Describable for Circle {
    fn describe(&self) -> String {
        format!("A circle with radius {}", self.radius)
    }
}
```

## Associated Types

```rust
// Associated types vs generic parameters
trait Container {
    type Item;

    fn add(&mut self, item: Self::Item);
    fn get(&self, index: usize) -> Option<&Self::Item>;
}

impl Container for Vec<i32> {
    type Item = i32;

    fn add(&mut self, item: i32) {
        self.push(item);
    }

    fn get(&self, index: usize) -> Option<&i32> {
        self.get(index)
    }
}

// Iterator trait (standard library example)
trait MyIterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;
}
```

## Generic Traits and Bounds

```rust
// Generic trait with multiple bounds
fn print_info<T>(item: &T)
where
    T: std::fmt::Display + std::fmt::Debug,
{
    println!("Display: {}", item);
    println!("Debug: {:?}", item);
}

// Generic struct with trait bounds
struct Pair<T: PartialOrd> {
    first: T,
    second: T,
}

impl<T: PartialOrd> Pair<T> {
    fn new(first: T, second: T) -> Self {
        Self { first, second }
    }

    fn larger(&self) -> &T {
        if self.first > self.second {
            &self.first
        } else {
            &self.second
        }
    }
}

// Blanket implementation
trait MyTrait {
    fn do_something(&self);
}

impl<T: std::fmt::Display> MyTrait for T {
    fn do_something(&self) {
        println!("Value: {}", self);
    }
}
```

## Trait Objects (Dynamic Dispatch)

```rust
// Static dispatch (monomorphization)
fn static_dispatch<T: Drawable>(item: &T) {
    item.draw();
}

// Dynamic dispatch (trait objects)
fn dynamic_dispatch(item: &dyn Drawable) {
    item.draw();
}

// Storing trait objects
struct Canvas {
    shapes: Vec<Box<dyn Drawable>>,
}

impl Canvas {
    fn new() -> Self {
        Self { shapes: Vec::new() }
    }

    fn add_shape(&mut self, shape: Box<dyn Drawable>) {
        self.shapes.push(shape);
    }

    fn draw_all(&self) {
        for shape in &self.shapes {
            shape.draw();
        }
    }
}

// Object safety: traits must meet criteria
trait ObjectSafe {
    fn method(&self);  // OK: takes &self
}

trait NotObjectSafe {
    fn generic<T>(&self);  // NOT OK: generic method
    fn by_value(self);     // NOT OK: takes self by value
}
```

## Derive Macros

```rust
// Standard derive macros
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct User {
    id: u64,
    name: String,
}

// Deriving more traits
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
struct Point {
    x: i32,
    y: i32,
}

// Custom derive with serde
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    host: String,
    port: u16,
}
```

## Advanced Trait Patterns

```rust
// Extension trait pattern
trait StringExt {
    fn truncate_to(&self, max_len: usize) -> String;
}

impl StringExt for str {
    fn truncate_to(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len])
        }
    }
}

// Sealed trait pattern (prevent external implementation)
mod sealed {
    pub trait Sealed {}
}

pub trait MySealed: sealed::Sealed {
    fn method(&self);
}

struct MyType;
impl sealed::Sealed for MyType {}
impl MySealed for MyType {
    fn method(&self) {
        println!("Implemented");
    }
}

// Supertraits
trait Printable {
    fn print(&self);
}

trait Loggable: Printable {  // Supertrait: must also impl Printable
    fn log(&self) {
        self.print();  // Can call supertrait methods
    }
}
```

## Associated Constants

```rust
trait Config {
    const MAX_SIZE: usize;
    const DEFAULT_TIMEOUT: u64;
}

struct ServerConfig;

impl Config for ServerConfig {
    const MAX_SIZE: usize = 1024;
    const DEFAULT_TIMEOUT: u64 = 30;
}

fn use_config<T: Config>() {
    println!("Max size: {}", T::MAX_SIZE);
}
```

## Generic Associated Types (GATs)

```rust
// GATs allow generics in associated types
trait LendingIterator {
    type Item<'a> where Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>>;
}

struct WindowsMut<'data, T> {
    data: &'data mut [T],
    index: usize,
}

impl<'data, T> LendingIterator for WindowsMut<'data, T> {
    type Item<'a> = &'a mut [T] where Self: 'a;

    fn next<'a>(&'a mut self) -> Option<Self::Item<'a>> {
        if self.index >= self.data.len() {
            return None;
        }

        let start = self.index;
        self.index += 2;

        Some(&mut self.data[start..start.min(self.data.len())])
    }
}
```

## Marker Traits

```rust
use std::marker::{PhantomData, Send, Sync};

// Send: type can be transferred across thread boundaries
// Sync: type can be shared between threads (&T is Send)

// Custom marker trait
trait Trusted {}

struct TrustedData<T> {
    data: T,
    _marker: PhantomData<T>,
}

impl<T: Trusted> TrustedData<T> {
    fn new(data: T) -> Self {
        Self {
            data,
            _marker: PhantomData,
        }
    }
}
```

## Operator Overloading

```rust
use std::ops::{Add, Mul};

#[derive(Debug, Clone, Copy)]
struct Vector2D {
    x: f64,
    y: f64,
}

impl Add for Vector2D {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl Mul<f64> for Vector2D {
    type Output = Self;

    fn mul(self, scalar: f64) -> Self {
        Self {
            x: self.x * scalar,
            y: self.y * scalar,
        }
    }
}

// Usage
let v1 = Vector2D { x: 1.0, y: 2.0 };
let v2 = Vector2D { x: 3.0, y: 4.0 };
let v3 = v1 + v2;
let v4 = v1 * 2.5;
```

## From/Into Conversion Traits

```rust
struct UserId(u64);

impl From<u64> for UserId {
    fn from(id: u64) -> Self {
        UserId(id)
    }
}

// Into is automatically implemented
fn accept_user_id(id: impl Into<UserId>) {
    let user_id = id.into();
    println!("User ID: {}", user_id.0);
}

// TryFrom for fallible conversions
use std::convert::TryFrom;

impl TryFrom<i64> for UserId {
    type Error = &'static str;

    fn try_from(value: i64) -> Result<Self, Self::Error> {
        if value < 0 {
            Err("User ID cannot be negative")
        } else {
            Ok(UserId(value as u64))
        }
    }
}
```

## Const Traits (Nightly)

```rust
// Const trait implementations (requires nightly)
#![feature(const_trait_impl)]

#[const_trait]
trait ConstAdd {
    fn add(self, other: Self) -> Self;
}

impl const ConstAdd for i32 {
    fn add(self, other: Self) -> Self {
        self + other
    }
}

const fn compute() -> i32 {
    5.add(10)  // Can use in const context
}
```

## Best Practices

- Prefer associated types when there's one clear type per implementation
- Use generic parameters when multiple types might be used simultaneously
- Keep traits small and focused (single responsibility)
- Use extension traits to add functionality to existing types
- Document trait requirements and invariants
- Use marker traits for compile-time guarantees
- Prefer static dispatch for performance, dynamic dispatch for flexibility
- Use #[derive] when possible instead of manual implementations
- Implement standard traits (Debug, Clone, etc.) for better ecosystem integration
- Use sealed traits to prevent external implementations when needed
