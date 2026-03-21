---
title: "Cpp Pro"
description: "Writes, optimizes, and debugs C++ applications using modern C++20/23 features, template metaprogramming, and high-performance systems techniques. Use when building or refactoring C++ code requiring concepts, ranges, coroutines, SIMD optimization, ..."
category: "development"
source: "community"
author: "Community"
tags: ["cpp"]
date: 2026-03-20
---

# C++ Pro

Senior C++ developer with deep expertise in modern C++20/23, systems programming, high-performance computing, and zero-overhead abstractions.

## Core Workflow

1. **Analyze architecture** — Review build system, compiler flags, performance requirements
2. **Design with concepts** — Create type-safe interfaces using C++20 concepts
3. **Implement zero-cost** — Apply RAII, constexpr, and zero-overhead abstractions
4. **Verify quality** — Run sanitizers and static analysis; if AddressSanitizer or UndefinedBehaviorSanitizer report issues, fix all memory and UB errors before proceeding
5. **Benchmark** — Profile with real workloads; if performance targets are not met, apply targeted optimizations (SIMD, cache layout, move semantics) and re-measure

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Modern C++ Features | `references/modern-cpp.md` | C++20/23 features, concepts, ranges, coroutines |
| Template Metaprogramming | `references/templates.md` | Variadic templates, SFINAE, type traits, CRTP |
| Memory & Performance | `references/memory-performance.md` | Allocators, SIMD, cache optimization, move semantics |
| Concurrency | `references/concurrency.md` | Atomics, lock-free structures, thread pools, coroutines |
| Build & Tooling | `references/build-tooling.md` | CMake, sanitizers, static analysis, testing |

## Constraints

### MUST DO
- Follow C++ Core Guidelines
- Use concepts for template constraints
- Apply RAII universally
- Use `auto` with type deduction
- Prefer `std::unique_ptr` and `std::shared_ptr`
- Enable all compiler warnings (-Wall -Wextra -Wpedantic)
- Run AddressSanitizer and UndefinedBehaviorSanitizer
- Write const-correct code

### MUST NOT DO
- Use raw `new`/`delete` (prefer smart pointers)
- Ignore compiler warnings
- Use C-style casts (use static_cast, etc.)
- Mix exception and error code patterns inconsistently
- Write non-const-correct code
- Use `using namespace std` in headers
- Ignore undefined behavior
- Skip move semantics for expensive types

## Key Patterns

### Concept Definition (C++20)
```cpp
// Define a reusable, self-documenting constraint
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<Numeric T>
T clamp(T value, T lo, T hi) {
    return std::clamp(value, lo, hi);
}
```

### RAII Resource Wrapper
```cpp
// Wraps a raw handle; no manual cleanup needed at call sites
class FileHandle {
public:
    explicit FileHandle(const char* path)
        : handle_(std::fopen(path, "r")) {
        if (!handle_) throw std::runtime_error("Cannot open file");
    }
    ~FileHandle() { if (handle_) std::fclose(handle_); }

    // Non-copyable, movable
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;
    FileHandle(FileHandle&& other) noexcept
        : handle_(std::exchange(other.handle_, nullptr)) {}

    std::FILE* get() const noexcept { return handle_; }
private:
    std::FILE* handle_;
};
```

### Smart Pointer Ownership
```cpp
// Prefer make_unique / make_shared; avoid raw new/delete
auto buffer = std::make_unique<std::array<std::byte, 4096>>();

// Shared ownership only when genuinely needed
auto config = std::make_shared<Config>(parseArgs(argc, argv));
```

## Output Templates

When implementing C++ features, provide:
1. Header file with interfaces and templates
2. Implementation file (when needed)
3. CMakeLists.txt updates (if applicable)
4. Test file demonstrating usage
5. Brief explanation of design decisions and performance characteristics

---

## Reference: Build Tooling

# Build Systems and Tooling

## Modern CMake

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyProject VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Export compile commands for tools
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Compiler warnings
if(MSVC)
    add_compile_options(/W4 /WX)
else()
    add_compile_options(-Wall -Wextra -Wpedantic -Werror)
endif()

# Create library target
add_library(mylib
    src/mylib.cpp
    include/mylib.h
)

target_include_directories(mylib
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_compile_features(mylib PUBLIC cxx_std_20)

# Create executable
add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib)

# Dependencies with FetchContent
include(FetchContent)

FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG 10.1.1
)
FetchContent_MakeAvailable(fmt)

target_link_libraries(mylib PUBLIC fmt::fmt)

# Testing
enable_testing()
add_subdirectory(tests)

# Install rules
include(GNUInstallDirs)
install(TARGETS mylib myapp
    EXPORT MyProjectTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

install(DIRECTORY include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
```

## Sanitizers

```cmake
# AddressSanitizer (ASan) - memory errors
set(CMAKE_CXX_FLAGS_ASAN
    "-g -O1 -fsanitize=address -fno-omit-frame-pointer"
    CACHE STRING "Flags for ASan build"
)

# UndefinedBehaviorSanitizer (UBSan)
set(CMAKE_CXX_FLAGS_UBSAN
    "-g -O1 -fsanitize=undefined -fno-omit-frame-pointer"
    CACHE STRING "Flags for UBSan build"
)

# ThreadSanitizer (TSan) - data races
set(CMAKE_CXX_FLAGS_TSAN
    "-g -O1 -fsanitize=thread -fno-omit-frame-pointer"
    CACHE STRING "Flags for TSan build"
)

# MemorySanitizer (MSan) - uninitialized reads
set(CMAKE_CXX_FLAGS_MSAN
    "-g -O1 -fsanitize=memory -fno-omit-frame-pointer"
    CACHE STRING "Flags for MSan build"
)

# Usage: cmake -DCMAKE_BUILD_TYPE=ASAN ..
```

## Static Analysis

```yaml
# .clang-tidy configuration
---
Checks: >
  *,
  -fuchsia-*,
  -google-*,
  -llvm-*,
  -modernize-use-trailing-return-type,
  -readability-identifier-length

WarningsAsErrors: '*'

CheckOptions:
  - key: readability-identifier-naming.ClassCase
    value: CamelCase
  - key: readability-identifier-naming.FunctionCase
    value: lower_case
  - key: readability-identifier-naming.VariableCase
    value: lower_case
  - key: readability-identifier-naming.ConstantCase
    value: UPPER_CASE
  - key: readability-identifier-naming.MemberCase
    value: lower_case
  - key: readability-identifier-naming.MemberSuffix
    value: '_'
  - key: modernize-use-nullptr.NullMacros
    value: 'NULL'
```

```bash
# Run clang-tidy
clang-tidy src/*.cpp -p build/

# Run cppcheck
cppcheck --enable=all --std=c++20 --suppress=missingInclude src/

# Run include-what-you-use
include-what-you-use -std=c++20 src/main.cpp
```

## Testing with Catch2

```cpp
#include <catch2/catch_test_macros.hpp>
#include <catch2/benchmark/catch_benchmark.hpp>
#include "mylib.h"

TEST_CASE("Vector operations", "[vector]") {
    std::vector<int> vec{1, 2, 3};

    SECTION("push_back") {
        vec.push_back(4);
        REQUIRE(vec.size() == 4);
        REQUIRE(vec.back() == 4);
    }

    SECTION("pop_back") {
        vec.pop_back();
        REQUIRE(vec.size() == 2);
        REQUIRE(vec.back() == 2);
    }
}

TEST_CASE("Exception handling", "[exceptions]") {
    REQUIRE_THROWS_AS(risky_function(), std::runtime_error);
    REQUIRE_THROWS_WITH(risky_function(), "error message");
}

TEST_CASE("Floating point", "[math]") {
    REQUIRE_THAT(compute_value(),
                 Catch::Matchers::WithinAbs(3.14, 0.01));
}

BENCHMARK("Vector creation") {
    return std::vector<int>(1000);
};

BENCHMARK("Vector fill") {
    std::vector<int> vec(1000);
    for (int i = 0; i < 1000; ++i) {
        vec[i] = i;
    }
    return vec;
};
```

## Testing with GoogleTest

```cpp
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "calculator.h"

class CalculatorTest : public ::testing::Test {
protected:
    void SetUp() override {
        calc = std::make_unique<Calculator>();
    }

    void TearDown() override {
        calc.reset();
    }

    std::unique_ptr<Calculator> calc;
};

TEST_F(CalculatorTest, Addition) {
    EXPECT_EQ(calc->add(2, 3), 5);
    EXPECT_EQ(calc->add(-1, 1), 0);
}

TEST_F(CalculatorTest, Division) {
    EXPECT_DOUBLE_EQ(calc->divide(10, 2), 5.0);
    EXPECT_THROW(calc->divide(10, 0), std::invalid_argument);
}

// Parameterized tests
class AdditionTest : public ::testing::TestWithParam<std::tuple<int, int, int>> {};

TEST_P(AdditionTest, ValidAddition) {
    auto [a, b, expected] = GetParam();
    Calculator calc;
    EXPECT_EQ(calc.add(a, b), expected);
}

INSTANTIATE_TEST_SUITE_P(
    AdditionSuite,
    AdditionTest,
    ::testing::Values(
        std::make_tuple(1, 2, 3),
        std::make_tuple(-1, -2, -3),
        std::make_tuple(0, 0, 0)
    )
);

// Mock objects
class MockDatabase : public Database {
public:
    MOCK_METHOD(void, connect, (const std::string&), (override));
    MOCK_METHOD(std::string, query, (const std::string&), (override));
    MOCK_METHOD(void, disconnect, (), (override));
};

TEST(ServiceTest, UsesDatabase) {
    MockDatabase mock_db;
    EXPECT_CALL(mock_db, connect("localhost"))
        .Times(1);
    EXPECT_CALL(mock_db, query("SELECT *"))
        .WillOnce(::testing::Return("result"));

    Service service(mock_db);
    service.process();
}
```

## Performance Profiling

```cpp
// Benchmark with Google Benchmark
#include <benchmark/benchmark.h>

static void BM_VectorPush(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> vec;
        for (int i = 0; i < state.range(0); ++i) {
            vec.push_back(i);
        }
        benchmark::DoNotOptimize(vec);
    }
}
BENCHMARK(BM_VectorPush)->Range(8, 8<<10);

static void BM_VectorReserve(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> vec;
        vec.reserve(state.range(0));
        for (int i = 0; i < state.range(0); ++i) {
            vec.push_back(i);
        }
        benchmark::DoNotOptimize(vec);
    }
}
BENCHMARK(BM_VectorReserve)->Range(8, 8<<10);

BENCHMARK_MAIN();
```

```bash
# Profiling with perf (Linux)
perf record -g ./myapp
perf report

# Profiling with Instruments (macOS)
instruments -t "Time Profiler" ./myapp

# Valgrind callgrind
valgrind --tool=callgrind ./myapp
kcachegrind callgrind.out.*

# Memory profiling
valgrind --tool=massif ./myapp
ms_print massif.out.*
```

## Conan Package Manager

```python
# conanfile.txt
[requires]
fmt/10.1.1
spdlog/1.12.0
catch2/3.4.0

[generators]
CMakeDeps
CMakeToolchain

[options]
fmt:header_only=True
```

```cmake
# CMakeLists.txt with Conan
cmake_minimum_required(VERSION 3.20)
project(MyProject)

find_package(fmt REQUIRED)
find_package(spdlog REQUIRED)
find_package(Catch2 REQUIRED)

add_executable(myapp src/main.cpp)
target_link_libraries(myapp
    PRIVATE
        fmt::fmt
        spdlog::spdlog
)

add_executable(tests test/main.cpp)
target_link_libraries(tests
    PRIVATE
        Catch2::Catch2WithMain
)
```

```bash
# Install dependencies
conan install . --output-folder=build --build=missing
cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
cmake --build .
```

## CI/CD with GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        compiler: [gcc, clang, msvc]
        build_type: [Debug, Release]

    steps:
    - uses: actions/checkout@v3

    - name: Install dependencies
      run: |
        pip install conan
        conan install . --output-folder=build --build=missing

    - name: Configure
      run: |
        cmake -B build -DCMAKE_BUILD_TYPE=${{ matrix.build_type }}

    - name: Build
      run: cmake --build build --config ${{ matrix.build_type }}

    - name: Test
      run: ctest --test-dir build -C ${{ matrix.build_type }}

  sanitizers:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        sanitizer: [asan, ubsan, tsan]

    steps:
    - uses: actions/checkout@v3

    - name: Build with sanitizer
      run: |
        cmake -B build -DCMAKE_BUILD_TYPE=${{ matrix.sanitizer }}
        cmake --build build

    - name: Run tests
      run: ctest --test-dir build

  static-analysis:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Run clang-tidy
      run: |
        cmake -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
        clang-tidy src/*.cpp -p build/

    - name: Run cppcheck
      run: cppcheck --enable=all --error-exitcode=1 src/
```

## Quick Reference

| Tool | Purpose | Command |
|------|---------|---------|
| CMake | Build system | `cmake -B build && cmake --build build` |
| Conan | Package manager | `conan install . --build=missing` |
| ASan | Memory errors | `-fsanitize=address` |
| UBSan | Undefined behavior | `-fsanitize=undefined` |
| TSan | Data races | `-fsanitize=thread` |
| clang-tidy | Static analysis | `clang-tidy src/*.cpp` |
| cppcheck | Static analysis | `cppcheck --enable=all src/` |
| Catch2 | Unit testing | `TEST_CASE("name") { REQUIRE(...); }` |
| GoogleTest | Unit testing | `TEST(Suite, Name) { EXPECT_EQ(...); }` |
| Google Benchmark | Performance | `BENCHMARK(func)->Range(...)` |
| Valgrind | Memory profiler | `valgrind --tool=memcheck ./app` |

---

## Reference: Concurrency

# Concurrency and Parallel Programming

## Atomics and Memory Ordering

```cpp
#include <atomic>
#include <thread>

// Basic atomics
std::atomic<int> counter{0};
std::atomic<bool> flag{false};

// Memory ordering
void producer(std::atomic<int>& data, std::atomic<bool>& ready) {
    data.store(42, std::memory_order_relaxed);
    ready.store(true, std::memory_order_release);  // Release barrier
}

void consumer(std::atomic<int>& data, std::atomic<bool>& ready) {
    while (!ready.load(std::memory_order_acquire)) {  // Acquire barrier
        std::this_thread::yield();
    }
    int value = data.load(std::memory_order_relaxed);
}

// Compare-and-swap
bool try_acquire_lock(std::atomic<bool>& lock) {
    bool expected = false;
    return lock.compare_exchange_strong(expected, true,
                                       std::memory_order_acquire,
                                       std::memory_order_relaxed);
}

// Fetch-and-add
int increment_counter(std::atomic<int>& counter) {
    return counter.fetch_add(1, std::memory_order_relaxed);
}
```

## Lock-Free Data Structures

```cpp
#include <atomic>
#include <memory>

// Lock-free stack
template<typename T>
class LockFreeStack {
    struct Node {
        T data;
        Node* next;
        Node(const T& value) : data(value), next(nullptr) {}
    };

    std::atomic<Node*> head_{nullptr};

public:
    void push(const T& value) {
        Node* new_node = new Node(value);
        new_node->next = head_.load(std::memory_order_relaxed);

        while (!head_.compare_exchange_weak(new_node->next, new_node,
                                           std::memory_order_release,
                                           std::memory_order_relaxed)) {
            // Retry with updated head
        }
    }

    bool pop(T& result) {
        Node* old_head = head_.load(std::memory_order_relaxed);

        while (old_head &&
               !head_.compare_exchange_weak(old_head, old_head->next,
                                           std::memory_order_acquire,
                                           std::memory_order_relaxed)) {
            // Retry
        }

        if (old_head) {
            result = old_head->data;
            delete old_head;  // Note: ABA problem exists
            return true;
        }
        return false;
    }
};

// Lock-free queue (single producer, single consumer)
template<typename T, size_t Size>
class SPSCQueue {
    std::array<T, Size> buffer_;
    alignas(64) std::atomic<size_t> head_{0};
    alignas(64) std::atomic<size_t> tail_{0};

public:
    bool push(const T& item) {
        size_t head = head_.load(std::memory_order_relaxed);
        size_t next_head = (head + 1) % Size;

        if (next_head == tail_.load(std::memory_order_acquire)) {
            return false;  // Queue full
        }

        buffer_[head] = item;
        head_.store(next_head, std::memory_order_release);
        return true;
    }

    bool pop(T& item) {
        size_t tail = tail_.load(std::memory_order_relaxed);

        if (tail == head_.load(std::memory_order_acquire)) {
            return false;  // Queue empty
        }

        item = buffer_[tail];
        tail_.store((tail + 1) % Size, std::memory_order_release);
        return true;
    }
};
```

## Thread Pool

```cpp
#include <thread>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <future>

class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex queue_mutex_;
    std::condition_variable condition_;
    bool stop_ = false;

public:
    ThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers_.emplace_back([this] {
                while (true) {
                    std::function<void()> task;

                    {
                        std::unique_lock<std::mutex> lock(queue_mutex_);
                        condition_.wait(lock, [this] {
                            return stop_ || !tasks_.empty();
                        });

                        if (stop_ && tasks_.empty()) {
                            return;
                        }

                        task = std::move(tasks_.front());
                        tasks_.pop();
                    }

                    task();
                }
            });
        }
    }

    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            stop_ = true;
        }
        condition_.notify_all();
        for (auto& worker : workers_) {
            worker.join();
        }
    }

    template<typename F, typename... Args>
    auto enqueue(F&& f, Args&&... args)
        -> std::future<typename std::invoke_result_t<F, Args...>> {

        using return_type = typename std::invoke_result_t<F, Args...>;

        auto task = std::make_shared<std::packaged_task<return_type()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...)
        );

        std::future<return_type> result = task->get_future();

        {
            std::unique_lock<std::mutex> lock(queue_mutex_);
            if (stop_) {
                throw std::runtime_error("enqueue on stopped ThreadPool");
            }
            tasks_.emplace([task]() { (*task)(); });
        }

        condition_.notify_one();
        return result;
    }
};
```

## Parallel STL Algorithms

```cpp
#include <algorithm>
#include <execution>
#include <vector>
#include <numeric>

void parallel_algorithms_demo() {
    std::vector<int> vec(1'000'000);
    std::iota(vec.begin(), vec.end(), 0);

    // Parallel sort
    std::sort(std::execution::par, vec.begin(), vec.end());

    // Parallel for_each
    std::for_each(std::execution::par_unseq, vec.begin(), vec.end(),
                  [](int& x) { x *= 2; });

    // Parallel transform
    std::vector<int> result(vec.size());
    std::transform(std::execution::par, vec.begin(), vec.end(),
                   result.begin(), [](int x) { return x * x; });

    // Parallel reduce
    int sum = std::reduce(std::execution::par, vec.begin(), vec.end());

    // Parallel transform_reduce (map-reduce)
    int sum_of_squares = std::transform_reduce(
        std::execution::par,
        vec.begin(), vec.end(),
        0,
        std::plus<>(),
        [](int x) { return x * x; }
    );
}
```

## Synchronization Primitives

```cpp
#include <mutex>
#include <shared_mutex>
#include <condition_variable>

// Mutex types
std::mutex mtx;
std::recursive_mutex rec_mtx;
std::timed_mutex timed_mtx;
std::shared_mutex shared_mtx;

// RAII locks
void exclusive_access() {
    std::lock_guard<std::mutex> lock(mtx);
    // Critical section
}

void unique_lock_example() {
    std::unique_lock<std::mutex> lock(mtx);
    // Can unlock and relock
    lock.unlock();
    // Do some work
    lock.lock();
}

// Reader-writer lock
class SharedData {
    mutable std::shared_mutex mutex_;
    std::string data_;

public:
    std::string read() const {
        std::shared_lock<std::shared_mutex> lock(mutex_);
        return data_;
    }

    void write(std::string new_data) {
        std::unique_lock<std::shared_mutex> lock(mutex_);
        data_ = std::move(new_data);
    }
};

// Condition variable
class Queue {
    std::queue<int> queue_;
    std::mutex mutex_;
    std::condition_variable cv_;

public:
    void push(int value) {
        {
            std::lock_guard<std::mutex> lock(mutex_);
            queue_.push(value);
        }
        cv_.notify_one();
    }

    int pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        cv_.wait(lock, [this] { return !queue_.empty(); });
        int value = queue_.front();
        queue_.pop();
        return value;
    }
};

// std::scoped_lock - multiple mutexes
std::mutex mtx1, mtx2;

void transfer(Account& from, Account& to, int amount) {
    std::scoped_lock lock(from.mutex, to.mutex);  // Deadlock-free
    from.balance -= amount;
    to.balance += amount;
}
```

## Async and Futures

```cpp
#include <future>

// std::async
auto future = std::async(std::launch::async, []() {
    return expensive_computation();
});

// Get result (blocks until ready)
auto result = future.get();

// Promise and future
void producer(std::promise<int> promise) {
    int value = compute_value();
    promise.set_value(value);
}

void consumer(std::future<int> future) {
    int value = future.get();
}

std::promise<int> promise;
std::future<int> future = promise.get_future();

std::thread producer_thread(producer, std::move(promise));
std::thread consumer_thread(consumer, std::move(future));

// Packaged task
std::packaged_task<int(int, int)> task([](int a, int b) {
    return a + b;
});

std::future<int> task_future = task.get_future();
std::thread task_thread(std::move(task), 5, 3);

int sum = task_future.get();  // 8
task_thread.join();
```

## Coroutine-Based Concurrency

```cpp
#include <coroutine>
#include <optional>

// Async task coroutine
template<typename T>
struct AsyncTask {
    struct promise_type {
        std::optional<T> value;
        std::exception_ptr exception;

        AsyncTask get_return_object() {
            return AsyncTask{
                std::coroutine_handle<promise_type>::from_promise(*this)
            };
        }

        std::suspend_never initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }

        void return_value(T v) {
            value = std::move(v);
        }

        void unhandled_exception() {
            exception = std::current_exception();
        }
    };

    std::coroutine_handle<promise_type> handle;

    AsyncTask(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~AsyncTask() { if (handle) handle.destroy(); }

    T get() {
        if (!handle.done()) {
            handle.resume();
        }

        if (handle.promise().exception) {
            std::rethrow_exception(handle.promise().exception);
        }

        return *handle.promise().value;
    }
};

// Usage
AsyncTask<int> async_compute() {
    co_return 42;
}
```

## Quick Reference

| Primitive | Use Case | Performance |
|-----------|----------|-------------|
| std::atomic | Simple shared state | Lock-free |
| std::mutex | Exclusive access | Kernel call |
| std::shared_mutex | Read-heavy workload | Better than mutex |
| Lock-free structures | High contention | Best throughput |
| Thread pool | Task parallelism | Avoid thread overhead |
| Parallel STL | Data parallelism | Automatic scaling |
| std::async | Simple async tasks | Thread pool |
| Coroutines | Async I/O | Minimal overhead |

## Memory Ordering Guide

| Ordering | Guarantees | Use Case |
|----------|-----------|----------|
| relaxed | No synchronization | Counters |
| acquire | Load barrier | Consumer |
| release | Store barrier | Producer |
| acq_rel | Both | RMW operations |
| seq_cst | Total order | Default |

---

## Reference: Memory Performance

# Memory Management & Performance

## Smart Pointers

```cpp
#include <memory>

// unique_ptr - exclusive ownership
auto create_resource() {
    return std::make_unique<Resource>("data");
}

// shared_ptr - reference counting
std::shared_ptr<Data> shared = std::make_shared<Data>(42);
std::weak_ptr<Data> weak = shared;  // Non-owning reference

// Custom deleters
auto file_deleter = [](FILE* fp) { if (fp) fclose(fp); };
std::unique_ptr<FILE, decltype(file_deleter)> file(
    fopen("data.txt", "r"),
    file_deleter
);

// enable_shared_from_this
class Node : public std::enable_shared_from_this<Node> {
public:
    std::shared_ptr<Node> get_shared() {
        return shared_from_this();
    }
};
```

## Custom Allocators

```cpp
#include <memory>
#include <vector>

// Pool allocator for fixed-size objects
template<typename T, size_t PoolSize = 1024>
class PoolAllocator {
    struct Block {
        alignas(T) std::byte data[sizeof(T)];
        Block* next;
    };

    Block pool_[PoolSize];
    Block* free_list_ = nullptr;

public:
    using value_type = T;

    PoolAllocator() {
        // Initialize free list
        for (size_t i = 0; i < PoolSize - 1; ++i) {
            pool_[i].next = &pool_[i + 1];
        }
        pool_[PoolSize - 1].next = nullptr;
        free_list_ = &pool_[0];
    }

    T* allocate(size_t n) {
        if (n != 1 || !free_list_) {
            throw std::bad_alloc();
        }
        Block* block = free_list_;
        free_list_ = free_list_->next;
        return reinterpret_cast<T*>(block->data);
    }

    void deallocate(T* p, size_t n) {
        if (n != 1) return;
        Block* block = reinterpret_cast<Block*>(p);
        block->next = free_list_;
        free_list_ = block;
    }
};

// Usage
std::vector<int, PoolAllocator<int>> vec;

// Arena allocator - bump allocator
class Arena {
    std::byte* buffer_;
    size_t size_;
    size_t offset_ = 0;

public:
    Arena(size_t size) : size_(size) {
        buffer_ = new std::byte[size];
    }

    ~Arena() {
        delete[] buffer_;
    }

    template<typename T>
    T* allocate(size_t n = 1) {
        size_t alignment = alignof(T);
        size_t space = size_ - offset_;
        void* ptr = buffer_ + offset_;

        if (std::align(alignment, sizeof(T) * n, ptr, space)) {
            offset_ = size_ - space + sizeof(T) * n;
            return static_cast<T*>(ptr);
        }

        throw std::bad_alloc();
    }

    void reset() {
        offset_ = 0;
    }
};
```

## Move Semantics

```cpp
#include <utility>
#include <algorithm>

class Buffer {
    size_t size_;
    char* data_;

public:
    // Constructor
    Buffer(size_t size) : size_(size), data_(new char[size]) {}

    // Destructor
    ~Buffer() { delete[] data_; }

    // Copy constructor
    Buffer(const Buffer& other) : size_(other.size_), data_(new char[size_]) {
        std::copy(other.data_, other.data_ + size_, data_);
    }

    // Copy assignment
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = new char[size_];
            std::copy(other.data_, other.data_ + size_, data_);
        }
        return *this;
    }

    // Move constructor
    Buffer(Buffer&& other) noexcept
        : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }

    // Move assignment
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = other.data_;
            other.size_ = 0;
            other.data_ = nullptr;
        }
        return *this;
    }
};

// Perfect forwarding
template<typename T>
void wrapper(T&& arg) {
    process(std::forward<T>(arg));  // Preserves lvalue/rvalue
}
```

## SIMD Optimization

```cpp
#include <immintrin.h>  // AVX/AVX2
#include <cstring>

// Vectorized sum using AVX2
float simd_sum(const float* data, size_t size) {
    __m256 sum_vec = _mm256_setzero_ps();

    size_t i = 0;
    // Process 8 floats at a time
    for (; i + 8 <= size; i += 8) {
        __m256 vec = _mm256_loadu_ps(&data[i]);
        sum_vec = _mm256_add_ps(sum_vec, vec);
    }

    // Horizontal sum
    alignas(32) float temp[8];
    _mm256_store_ps(temp, sum_vec);
    float result = 0.0f;
    for (int j = 0; j < 8; ++j) {
        result += temp[j];
    }

    // Handle remaining elements
    for (; i < size; ++i) {
        result += data[i];
    }

    return result;
}

// Vectorized multiply-add
void fma_operation(float* result, const float* a, const float* b,
                   const float* c, size_t size) {
    for (size_t i = 0; i + 8 <= size; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        __m256 vc = _mm256_loadu_ps(&c[i]);

        // result[i] = a[i] * b[i] + c[i]
        __m256 vr = _mm256_fmadd_ps(va, vb, vc);
        _mm256_storeu_ps(&result[i], vr);
    }
}
```

## Cache-Friendly Design

```cpp
// Structure of Arrays (SoA) - better cache locality
struct ParticlesAoS {
    struct Particle {
        float x, y, z;
        float vx, vy, vz;
    };
    std::vector<Particle> particles;
};

struct ParticlesSoA {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;

    void update_positions(float dt) {
        // All x coordinates are contiguous - better cache usage
        for (size_t i = 0; i < x.size(); ++i) {
            x[i] += vx[i] * dt;
            y[i] += vy[i] * dt;
            z[i] += vz[i] * dt;
        }
    }
};

// Cache line padding to avoid false sharing
struct alignas(64) CacheLinePadded {
    std::atomic<int> counter;
    char padding[64 - sizeof(std::atomic<int>)];
};

// Prefetching
void process_with_prefetch(const int* data, size_t size) {
    for (size_t i = 0; i < size; ++i) {
        // Prefetch data for next iteration
        if (i + 8 < size) {
            __builtin_prefetch(&data[i + 8], 0, 1);
        }
        // Process current data
        process(data[i]);
    }
}
```

## Memory Pool

```cpp
#include <vector>
#include <memory>

template<typename T, size_t ChunkSize = 256>
class MemoryPool {
    struct Chunk {
        alignas(T) std::byte data[sizeof(T) * ChunkSize];
    };

    std::vector<std::unique_ptr<Chunk>> chunks_;
    std::vector<T*> free_list_;
    size_t current_chunk_offset_ = ChunkSize;

public:
    T* allocate() {
        if (!free_list_.empty()) {
            T* ptr = free_list_.back();
            free_list_.pop_back();
            return ptr;
        }

        if (current_chunk_offset_ >= ChunkSize) {
            chunks_.push_back(std::make_unique<Chunk>());
            current_chunk_offset_ = 0;
        }

        Chunk* chunk = chunks_.back().get();
        T* ptr = reinterpret_cast<T*>(
            &chunk->data[sizeof(T) * current_chunk_offset_++]
        );
        return ptr;
    }

    void deallocate(T* ptr) {
        free_list_.push_back(ptr);
    }

    template<typename... Args>
    T* construct(Args&&... args) {
        T* ptr = allocate();
        new (ptr) T(std::forward<Args>(args)...);
        return ptr;
    }

    void destroy(T* ptr) {
        ptr->~T();
        deallocate(ptr);
    }
};
```

## Copy Elision and RVO

```cpp
// Return Value Optimization (RVO)
std::vector<int> create_vector() {
    std::vector<int> vec{1, 2, 3, 4, 5};
    return vec;  // RVO applies, no copy/move
}

// Named Return Value Optimization (NRVO)
std::string build_string(bool condition) {
    std::string result;
    if (condition) {
        result = "condition true";
    } else {
        result = "condition false";
    }
    return result;  // NRVO may apply
}

// Guaranteed copy elision (C++17)
struct NonMovable {
    NonMovable() = default;
    NonMovable(const NonMovable&) = delete;
    NonMovable(NonMovable&&) = delete;
};

NonMovable create() {
    return NonMovable{};  // Guaranteed no copy/move in C++17
}

auto obj = create();  // OK in C++17
```

## Alignment and Memory Layout

```cpp
#include <cstddef>

// Control alignment
struct alignas(64) CacheAligned {
    int data[16];
};

// Check alignment
static_assert(alignof(CacheAligned) == 64);

// Aligned allocation
void* aligned_alloc_wrapper(size_t alignment, size_t size) {
    void* ptr = nullptr;
    if (posix_memalign(&ptr, alignment, size) != 0) {
        throw std::bad_alloc();
    }
    return ptr;
}

// Placement new with alignment
alignas(32) std::byte buffer[sizeof(Data)];
Data* obj = new (buffer) Data();
obj->~Data();  // Manual destruction needed
```

## Quick Reference

| Technique | Use Case | Benefit |
|-----------|----------|---------|
| Smart Pointers | Ownership management | Memory safety |
| Move Semantics | Avoid copies | Performance |
| Custom Allocators | Specialized allocation | Speed + control |
| SIMD | Parallel computation | 4-8x speedup |
| SoA Layout | Sequential access | Cache efficiency |
| Memory Pools | Frequent alloc/dealloc | Reduced fragmentation |
| Alignment | SIMD/cache optimization | Performance |
| RVO/NRVO | Return objects | Zero-copy |

---

## Reference: Modern Cpp

# Modern C++20/23 Features

## Concepts and Constraints

```cpp
#include <concepts>

// Define custom concepts
template<typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template<typename T>
concept Hashable = requires(T a) {
    { std::hash<T>{}(a) } -> std::convertible_to<std::size_t>;
};

template<typename T>
concept Container = requires(T c) {
    typename T::value_type;
    typename T::iterator;
    { c.begin() } -> std::same_as<typename T::iterator>;
    { c.end() } -> std::same_as<typename T::iterator>;
    { c.size() } -> std::convertible_to<std::size_t>;
};

// Use concepts for function constraints
template<Numeric T>
T add(T a, T b) {
    return a + b;
}

// Concept-based overloading
template<std::integral T>
void process(T value) {
    std::cout << "Processing integer: " << value << '\n';
}

template<std::floating_point T>
void process(T value) {
    std::cout << "Processing float: " << value << '\n';
}
```

## Ranges and Views

```cpp
#include <ranges>
#include <vector>
#include <algorithm>

// Ranges-based algorithms
std::vector<int> numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

// Filter, transform, take - all lazy evaluation
auto result = numbers
    | std::views::filter([](int n) { return n % 2 == 0; })
    | std::views::transform([](int n) { return n * n; })
    | std::views::take(3);

// Copy to vector only when needed
std::vector<int> materialized(result.begin(), result.end());

// Custom range adaptor
auto is_even = [](int n) { return n % 2 == 0; };
auto square = [](int n) { return n * n; };

auto pipeline = std::views::filter(is_even)
              | std::views::transform(square);

auto processed = numbers | pipeline;
```

## Coroutines

```cpp
#include <coroutine>
#include <iostream>
#include <memory>

// Generator coroutine
template<typename T>
struct Generator {
    struct promise_type {
        T current_value;

        auto get_return_object() {
            return Generator{std::coroutine_handle<promise_type>::from_promise(*this)};
        }

        std::suspend_always initial_suspend() { return {}; }
        std::suspend_always final_suspend() noexcept { return {}; }

        std::suspend_always yield_value(T value) {
            current_value = value;
            return {};
        }

        void return_void() {}
        void unhandled_exception() { std::terminate(); }
    };

    std::coroutine_handle<promise_type> handle;

    Generator(std::coroutine_handle<promise_type> h) : handle(h) {}
    ~Generator() { if (handle) handle.destroy(); }

    bool move_next() {
        handle.resume();
        return !handle.done();
    }

    T current_value() {
        return handle.promise().current_value;
    }
};

// Usage
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

// Async coroutine
#include <future>

struct Task {
    struct promise_type {
        Task get_return_object() {
            return Task{std::coroutine_handle<promise_type>::from_promise(*this)};
        }
        std::suspend_never initial_suspend() { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() {}
    };

    std::coroutine_handle<promise_type> handle;
};

Task async_operation() {
    std::cout << "Starting async work\n";
    co_await std::suspend_always{};
    std::cout << "Resuming async work\n";
}
```

## Three-Way Comparison (Spaceship)

```cpp
#include <compare>

struct Point {
    int x, y;

    // Auto-generate all comparison operators
    auto operator<=>(const Point&) const = default;
};

// Custom spaceship operator
struct Version {
    int major, minor, patch;

    std::strong_ordering operator<=>(const Version& other) const {
        if (auto cmp = major <=> other.major; cmp != 0) return cmp;
        if (auto cmp = minor <=> other.minor; cmp != 0) return cmp;
        return patch <=> other.patch;
    }

    bool operator==(const Version& other) const = default;
};
```

## Designated Initializers

```cpp
struct Config {
    std::string host = "localhost";
    int port = 8080;
    bool ssl_enabled = false;
    int timeout_ms = 5000;
};

// C++20 designated initializers
Config cfg {
    .host = "example.com",
    .port = 443,
    .ssl_enabled = true
    // timeout_ms uses default
};
```

## Modules (C++20)

```cpp
// math.cppm - module interface
export module math;

export namespace math {
    template<typename T>
    T add(T a, T b) {
        return a + b;
    }

    class Calculator {
    public:
        int multiply(int a, int b);
    };
}

// Implementation
module math;

int math::Calculator::multiply(int a, int b) {
    return a * b;
}

// Usage in other files
import math;

int main() {
    auto result = math::add(5, 3);
    math::Calculator calc;
    auto product = calc.multiply(4, 7);
}
```

## constexpr Enhancements

```cpp
#include <string>
#include <vector>
#include <algorithm>

// C++20: constexpr std::string and std::vector
constexpr auto compute_at_compile_time() {
    std::vector<int> vec{1, 2, 3, 4, 5};
    std::ranges::reverse(vec);
    return vec[0]; // Returns 5
}

constexpr int value = compute_at_compile_time();

// constexpr virtual functions (C++20)
struct Base {
    constexpr virtual int get_value() const { return 42; }
    constexpr virtual ~Base() = default;
};

struct Derived : Base {
    constexpr int get_value() const override { return 100; }
};
```

## std::format (C++20)

```cpp
#include <format>
#include <iostream>

int main() {
    std::string msg = std::format("Hello, {}!", "World");

    // Positional arguments
    auto text = std::format("{1} {0}", "World", "Hello");

    // Formatting options
    double pi = 3.14159265;
    auto formatted = std::format("Pi: {:.2f}", pi); // "Pi: 3.14"

    // Custom types
    struct Point { int x, y; };
}

// Custom formatter
template<>
struct std::formatter<Point> {
    constexpr auto parse(format_parse_context& ctx) {
        return ctx.begin();
    }

    auto format(const Point& p, format_context& ctx) const {
        return std::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};
```

## Quick Reference

| Feature | C++17 | C++20 | C++23 |
|---------|-------|-------|-------|
| Concepts | - | ✓ | ✓ |
| Ranges | - | ✓ | ✓ |
| Coroutines | - | ✓ | ✓ |
| Modules | - | ✓ | ✓ |
| Spaceship | - | ✓ | ✓ |
| std::format | - | ✓ | ✓ |
| std::expected | - | - | ✓ |
| std::print | - | - | ✓ |
| Deducing this | - | - | ✓ |

---

## Reference: Templates

# Template Metaprogramming

## Variadic Templates

```cpp
#include <iostream>
#include <utility>

// Fold expressions (C++17)
template<typename... Args>
auto sum(Args... args) {
    return (args + ...);  // Unary right fold
}

template<typename... Args>
void print(Args&&... args) {
    ((std::cout << args << ' '), ...);  // Binary left fold
    std::cout << '\n';
}

// Recursive variadic template
template<typename T>
void log(T&& value) {
    std::cout << value << '\n';
}

template<typename T, typename... Args>
void log(T&& first, Args&&... rest) {
    std::cout << first << ", ";
    log(std::forward<Args>(rest)...);
}

// Parameter pack expansion
template<typename... Types>
struct TypeList {
    static constexpr size_t size = sizeof...(Types);
};

template<typename... Args>
auto make_tuple_advanced(Args&&... args) {
    return std::tuple<std::decay_t<Args>...>(std::forward<Args>(args)...);
}
```

## SFINAE and if constexpr

```cpp
#include <type_traits>

// SFINAE with std::enable_if (older style)
template<typename T>
std::enable_if_t<std::is_integral_v<T>, T>
double_value(T value) {
    return value * 2;
}

template<typename T>
std::enable_if_t<std::is_floating_point_v<T>, T>
double_value(T value) {
    return value * 2.0;
}

// Modern: if constexpr (C++17)
template<typename T>
auto process(T value) {
    if constexpr (std::is_integral_v<T>) {
        return value * 2;
    } else if constexpr (std::is_floating_point_v<T>) {
        return value * 2.0;
    } else {
        return value;
    }
}

// Detection idiom
template<typename T, typename = void>
struct has_serialize : std::false_type {};

template<typename T>
struct has_serialize<T, std::void_t<decltype(std::declval<T>().serialize())>>
    : std::true_type {};

template<typename T>
constexpr bool has_serialize_v = has_serialize<T>::value;

// Use with if constexpr
template<typename T>
void save(const T& obj) {
    if constexpr (has_serialize_v<T>) {
        obj.serialize();
    } else {
        // Default serialization
    }
}
```

## Type Traits

```cpp
#include <type_traits>

// Custom type traits
template<typename T>
struct remove_all_pointers {
    using type = T;
};

template<typename T>
struct remove_all_pointers<T*> {
    using type = typename remove_all_pointers<T>::type;
};

template<typename T>
using remove_all_pointers_t = typename remove_all_pointers<T>::type;

// Conditional types
template<bool Condition, typename T, typename F>
struct conditional_type {
    using type = T;
};

template<typename T, typename F>
struct conditional_type<false, T, F> {
    using type = F;
};

// Compile-time type selection
template<size_t N>
struct best_integral_type {
    using type = std::conditional_t<N <= 8, uint8_t,
                 std::conditional_t<N <= 16, uint16_t,
                 std::conditional_t<N <= 32, uint32_t, uint64_t>>>;
};

// Check for member functions
template<typename T, typename = void>
struct has_reserve : std::false_type {};

template<typename T>
struct has_reserve<T, std::void_t<decltype(std::declval<T>().reserve(size_t{}))>>
    : std::true_type {};
```

## CRTP (Curiously Recurring Template Pattern)

```cpp
// Static polymorphism with CRTP
template<typename Derived>
class Shape {
public:
    double area() const {
        return static_cast<const Derived*>(this)->area_impl();
    }

    void draw() const {
        static_cast<const Derived*>(this)->draw_impl();
    }
};

class Circle : public Shape<Circle> {
    double radius_;
public:
    Circle(double r) : radius_(r) {}

    double area_impl() const {
        return 3.14159 * radius_ * radius_;
    }

    void draw_impl() const {
        std::cout << "Drawing circle\n";
    }
};

class Rectangle : public Shape<Rectangle> {
    double width_, height_;
public:
    Rectangle(double w, double h) : width_(w), height_(h) {}

    double area_impl() const {
        return width_ * height_;
    }

    void draw_impl() const {
        std::cout << "Drawing rectangle\n";
    }
};

// CRTP for mixin capabilities
template<typename Derived>
class Printable {
public:
    void print() const {
        std::cout << static_cast<const Derived*>(this)->to_string() << '\n';
    }
};

class User : public Printable<User> {
    std::string name_;
public:
    User(std::string name) : name_(std::move(name)) {}

    std::string to_string() const {
        return "User: " + name_;
    }
};
```

## Template Template Parameters

```cpp
#include <vector>
#include <list>
#include <deque>

// Template template parameter
template<typename T, template<typename, typename> class Container>
class Stack {
    Container<T, std::allocator<T>> data_;

public:
    void push(const T& value) {
        data_.push_back(value);
    }

    T pop() {
        T value = data_.back();
        data_.pop_back();
        return value;
    }

    size_t size() const {
        return data_.size();
    }
};

// Usage with different containers
Stack<int, std::vector> vector_stack;
Stack<int, std::deque> deque_stack;
Stack<int, std::list> list_stack;
```

## Compile-Time Computation

```cpp
#include <array>

// Compile-time factorial
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

constexpr int fact_5 = factorial(5);  // Computed at compile time

// Compile-time prime checking
constexpr bool is_prime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) return false;
    }
    return true;
}

// Generate compile-time array of primes
template<size_t N>
constexpr auto generate_primes() {
    std::array<int, N> primes{};
    int count = 0;
    int candidate = 2;

    while (count < N) {
        if (is_prime(candidate)) {
            primes[count++] = candidate;
        }
        ++candidate;
    }

    return primes;
}

constexpr auto first_10_primes = generate_primes<10>();
```

## Expression Templates

```cpp
// Lazy evaluation with expression templates
template<typename E>
class VecExpression {
public:
    double operator[](size_t i) const {
        return static_cast<const E&>(*this)[i];
    }

    size_t size() const {
        return static_cast<const E&>(*this).size();
    }
};

class Vec : public VecExpression<Vec> {
    std::vector<double> data_;

public:
    Vec(size_t n) : data_(n) {}

    double operator[](size_t i) const { return data_[i]; }
    double& operator[](size_t i) { return data_[i]; }
    size_t size() const { return data_.size(); }

    // Evaluate expression template
    template<typename E>
    Vec& operator=(const VecExpression<E>& expr) {
        for (size_t i = 0; i < size(); ++i) {
            data_[i] = expr[i];
        }
        return *this;
    }
};

// Binary operation expression
template<typename E1, typename E2>
class VecSum : public VecExpression<VecSum<E1, E2>> {
    const E1& lhs_;
    const E2& rhs_;

public:
    VecSum(const E1& lhs, const E2& rhs) : lhs_(lhs), rhs_(rhs) {}

    double operator[](size_t i) const {
        return lhs_[i] + rhs_[i];
    }

    size_t size() const { return lhs_.size(); }
};

// Operator overload
template<typename E1, typename E2>
VecSum<E1, E2> operator+(const VecExpression<E1>& lhs,
                         const VecExpression<E2>& rhs) {
    return VecSum<E1, E2>(static_cast<const E1&>(lhs),
                          static_cast<const E2&>(rhs));
}

// Usage: a = b + c + d  (no temporaries created!)
```

## Quick Reference

| Technique | Use Case | Performance |
|-----------|----------|-------------|
| Variadic Templates | Variable arguments | Zero overhead |
| SFINAE | Conditional compilation | Compile-time |
| if constexpr | Type-based branching | Zero overhead |
| CRTP | Static polymorphism | No vtable cost |
| Expression Templates | Lazy evaluation | Eliminates temps |
| Type Traits | Type introspection | Compile-time |
| Fold Expressions | Parameter pack ops | Optimal |
| Template Specialization | Type-specific impl | Zero overhead |
