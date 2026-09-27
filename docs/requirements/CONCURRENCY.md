# Concurrency requirements

> **Status:** Phase 1 requirements baseline · **Defines language semantics:** No · **Last reviewed:** 2026-09-27

Concurrency is a foundational capability for Cretes ([Principle 5](../principles/DESIGN-PRINCIPLES.md#5-concurrency-as-a-foundational-capability)). Automation runs many jobs at once. Network services handle many connections. AI/ML preprocessing uses all cores. Security tools scan and parse in parallel. This document defines the required capabilities.

> **No concurrency implementation is selected.** OS threads, green threads, coroutines, event loops, work-stealing schedulers, compiler-generated async state machines and hybrid designs remain candidates. Phase 2 decides ([P2Q-011](../PHASE-2-OPEN-QUESTIONS.md#p2q-011--concurrency-runtime-architecture), [P2Q-012](../PHASE-2-OPEN-QUESTIONS.md#p2q-012--asynchronous-execution-model-and-api-coloring)).

The word **task** below means "an independently progressing unit of concurrent work". It does not imply any implementation.

Concurrency is **not** required in v0.1 ([V0.1-REQUIREMENTS.md](V0.1-REQUIREMENTS.md)). However, the v0.1 architecture must not make these requirements impractical.

Terminology, layers and targets are defined in the [requirements framework](README.md).

## Contents

- [Tasks and execution](#tasks-and-execution)
- [Lifecycle, cancellation and time](#lifecycle-cancellation-and-time)
- [Communication and synchronization](#communication-and-synchronization)
- [Safety](#safety)
- [Integration and tooling](#integration-and-tooling)

## Tasks and execution

### CONC-001 — Concurrent tasks

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Programs must be able to start tasks that progress concurrently and to obtain each task's result or failure.
- **Rationale:** The basic concurrency capability required by every domain.
- **Verification:** Conformance tests.

### CONC-002 — Non-blocking waiting

- **Priority:** MUST · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** A task waiting for I/O, a timer or another task must not prevent unrelated tasks from making progress.
- **Rationale:** Network services and automation orchestrators spend most of their time waiting.
- **Verification:** Integration tests; Benchmark (`concurrency/`).

### CONC-003 — Parallel execution

- **Priority:** MUST · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** Programs must be able to execute computation in parallel on multiple CPU cores.
- **Rationale:** Numerical work, parsing and compression scale with cores ([AI-011](domains/ai-ml.md#ai-011--parallel-numerical-computation)).
- **Verification:** Benchmark (`concurrency/`, `numerical/`).

### CONC-015 — Blocking and CPU-intensive work

- **Priority:** MUST · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** The runtime model must provide a documented way to run blocking operations without starving other tasks. Blocking operations include foreign calls and synchronous OS APIs. The same applies to long CPU-bound computation.
- **Rationale:** Many existing libraries and system calls block. Ignoring this is a common cause of latency collapse.
- **Verification:** Integration tests.

## Lifecycle, cancellation and time

### CONC-004 — Structured concurrency

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Tasks must by default be started within a scope. A scope must not complete until every task started in it has completed, failed or been cancelled. By default, a task must not outlive the scope that started it.
- **Rationale:** Structured lifetimes prevent leaked tasks, make resource cleanup deterministic ([SAFE-013](SAFETY.md#safe-013--deterministic-resource-release)) and make errors impossible to lose.
- **Verification:** Conformance tests.

### CONC-005 — Explicit detached tasks

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** If tasks that outlive their starting scope are supported, they should require an explicit, visible operation. Their failures must still be reported somewhere defined.
- **Rationale:** Some services need background work. It must be an opt-in exception, not the default.
- **Verification:** Conformance tests.

### CONC-006 — Cancellation

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Tasks must be cancellable. Cancellation must propagate to child tasks and must interrupt waiting operations. It must allow cleanup code to run and must release resources held by the task ([SAFE-013](SAFETY.md#safe-013--deterministic-resource-release)). Whether cancellation is cooperative, asynchronous or both is a Phase 2 decision.
- **Rationale:** Timeouts, user interrupts, shutdown and "first result wins" patterns all depend on reliable cancellation.
- **Verification:** Conformance tests; Integration tests.

### CONC-007 — Deadlines and timeouts

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Any waiting operation must be able to be bounded by a timeout or deadline. A deadline set on a scope must apply to the operations and child tasks within it. Deadlines must be measured with a monotonic clock.
- **Rationale:** Operations that can hang forever are an availability and security risk in network and automation code ([NET-010](domains/networking.md#net-010--timeouts-on-every-network-operation)).
- **Verification:** Integration tests.

### CONC-008 — Error propagation

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** A failure in a task must be observable by the scope or task that awaits it. The standard library must provide a documented policy for handling sibling tasks when one fails, such as cancel-on-first-failure or collect-all-results. Errors must never be silently discarded.
- **Rationale:** Extends [CORE-022](CORE.md#core-022--explicit-recoverable-errors) to concurrent code.
- **Verification:** Conformance tests.

### CONC-014 — Task lifecycle observation

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Programs must be able to wait for a task and to determine whether it completed, failed or was cancelled.
- **Rationale:** Supervision logic in automation and servers depends on outcome.
- **Verification:** Unit tests.

### CONC-016 — Waiting on multiple operations

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Programs should be able to wait for the first of several operations to complete, such as a message, a timeout or a cancellation signal, and to cancel the others.
- **Rationale:** Required for protocol state machines, timeouts and graceful shutdown.
- **Verification:** Unit tests.

## Communication and synchronization

### CONC-009 — Synchronization primitives

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide:
  - mutual exclusion;
  - reader–writer locking;
  - one-time initialization;
  - notification of waiting tasks;
  - atomic operations on primitive values.
- **Rationale:** Shared-state concurrency is sometimes the simplest correct design.
- **Verification:** Unit tests; Integration tests.

### CONC-010 — Memory model

- **Priority:** MUST · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** The specification must define a memory model for concurrent access. The model must state which writes a read may observe, and the ordering guarantees of atomic operations and synchronization primitives. It should also be compatible with the C/C++ memory model, for FFI.
- **Rationale:** Atomics and unsafe code cannot be written correctly without a defined model. FFI shares memory with C.
- **Verification:** Specification review.

### CONC-011 — Message passing

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library must provide channels for transferring values between tasks, with defined semantics for closing and for multiple producers and consumers.
- **Rationale:** Message passing reduces shared mutable state and fits pipeline-style automation and data processing.
- **Verification:** Unit tests.

### CONC-012 — Backpressure

- **Priority:** MUST · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** Channels and other standard queues must support bounded capacity. A bounded queue must make a producer wait or fail when the queue is full. Unbounded buffering must require an explicit choice.
- **Rationale:** Unbounded queues turn load spikes into memory exhaustion ([NET-013](domains/networking.md#net-013--backpressure)).
- **Verification:** Unit tests.

## Safety

### CONC-013 — Diagnosing unsafe sharing

- **Priority:** SHOULD · **Layer:** Language · **Target:** Post-v0.1
- **Requirement:** Whether a value may be shared between, or transferred across, concurrent tasks should be determinable by tools. Violations in safe code should be diagnosed before execution. Data-race freedom itself is a MUST ([SAFE-012](SAFETY.md#safe-012--data-race-freedom)). This requirement concerns detecting violations early rather than at run time.
- **Rationale:** Concurrency bugs found at compile time are far cheaper than those found in production.
- **Verification:** Conformance tests; Diagnostic tests.

### CONC-020 — Concurrency and foreign code

- **Priority:** MUST · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** The behavior of the following must be defined:
  - foreign calls made from tasks;
  - foreign code calling into Cretes from threads that Cretes did not create;
  - foreign code holding references to Cretes memory while Cretes tasks run.
- **Rationale:** AI runtimes, GUI toolkits and OS callbacks invoke code on their own threads ([INTOP-008](INTEROPERABILITY.md#intop-008--callbacks-from-foreign-code)).
- **Verification:** Integration tests; Design review.

## Integration and tooling

### CONC-017 — Concurrency observability

- **Priority:** SHOULD · **Layer:** Runtime · **Target:** Post-v0.1
- **Requirement:** Tasks should be nameable. The runtime should support inspecting live tasks and their scope hierarchy, and should support integration with tracing tools.
- **Rationale:** Diagnosing stuck or leaked work in production services requires visibility.
- **Verification:** Integration tests.

### CONC-018 — Deterministic concurrency testing

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library or test tooling should support controlled time and reproducible scheduling in tests, so that timeouts and interleavings can be tested deterministically.
- **Rationale:** Timing-dependent tests are slow and flaky.
- **Verification:** Unit tests.

### CONC-019 — Unified concurrency model

- **Priority:** SHOULD · **Layer:** Standard library · **Target:** Post-v0.1
- **Requirement:** The standard library should avoid requiring separate, incompatible versions of the same interface for concurrent and non-concurrent use. For example, it should not need both a blocking and an asynchronous file API that cannot be mixed. If Phase 2 concludes that a split is unavoidable, the reasons and the interoperation rules must be documented.
- **Rationale:** A divided ecosystem doubles library maintenance and confuses newcomers. The trade-off is analyzed under [P2Q-012](../PHASE-2-OPEN-QUESTIONS.md#p2q-012--asynchronous-execution-model-and-api-coloring).
- **Verification:** Design review.

## Related documents

- [Safety requirements](SAFETY.md)
- [Networking requirements](domains/networking.md)
- [Performance requirements](PERFORMANCE.md)
- [Phase 2 open questions](../PHASE-2-OPEN-QUESTIONS.md)
