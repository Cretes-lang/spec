# 2.13 — Concurrency architecture

> Decision: **ARCH-CONC-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CONC-001](../requirements/CONCURRENCY.md#conc-001--concurrent-tasks), [CONC-002](../requirements/CONCURRENCY.md#conc-002--non-blocking-waiting), [CONC-003](../requirements/CONCURRENCY.md#conc-003--parallel-execution), [CONC-004](../requirements/CONCURRENCY.md#conc-004--structured-concurrency), [CONC-005](../requirements/CONCURRENCY.md#conc-005--explicit-detached-tasks), [CONC-006](../requirements/CONCURRENCY.md#conc-006--cancellation), [CONC-007](../requirements/CONCURRENCY.md#conc-007--deadlines-and-timeouts), [CONC-008](../requirements/CONCURRENCY.md#conc-008--error-propagation), [CONC-009](../requirements/CONCURRENCY.md#conc-009--synchronization-primitives), [CONC-010](../requirements/CONCURRENCY.md#conc-010--memory-model), [CONC-011](../requirements/CONCURRENCY.md#conc-011--message-passing), [CONC-012](../requirements/CONCURRENCY.md#conc-012--backpressure), [CONC-013](../requirements/CONCURRENCY.md#conc-013--diagnosing-unsafe-sharing), [CONC-014](../requirements/CONCURRENCY.md#conc-014--task-lifecycle-observation), [CONC-015](../requirements/CONCURRENCY.md#conc-015--blocking-and-cpu-intensive-work), [CONC-016](../requirements/CONCURRENCY.md#conc-016--waiting-on-multiple-operations), [CONC-017](../requirements/CONCURRENCY.md#conc-017--concurrency-observability), [CONC-018](../requirements/CONCURRENCY.md#conc-018--deterministic-concurrency-testing), [CONC-019](../requirements/CONCURRENCY.md#conc-019--unified-concurrency-model), [CONC-020](../requirements/CONCURRENCY.md#conc-020--concurrency-and-foreign-code), [NET-003](../requirements/domains/networking.md#net-003--connection-scale-design-target), [PERF-014](../requirements/PERFORMANCE.md#perf-014--concurrency-overhead), [SAFE-012](../requirements/SAFETY.md#safe-012--data-race-freedom)

## Proposed decision and rationale

**Structured task groups with stackless tasks, explicit transfer/share capabilities and bounded scheduling resources, after v0.1.**

A task belongs to a lexical or explicitly owned group. Leaving a group joins its children; an error requests sibling cancellation and then joins before releasing captured resources. A task result distinguishes success, recoverable error and cancellation. Completion order is nondeterministic unless the API explicitly preserves input order. Detached tasks are not the default; a long-lived service supervisor is an owned object with shutdown obligations.

Cross-thread transfer requires a type to be safely movable between threads; shared access additionally requires an immutable representation or synchronization that prevents concurrent unsynchronized mutation. These are compiler-checked capabilities, not a convention based on names. Raw pointers, guards tied to an OS thread, and non-atomic local shared handles do not automatically qualify. Scoped borrowing into tasks requires the group to outlive/join every borrower.

OS threads are available through controlled standard-library facilities. Async tasks run on an executor with a bounded worker set; CPU work and blocking foreign calls use separately bounded queues. Work stealing is an optional scheduling optimization, not a semantic promise. A local executor can host non-transferable tasks while rejecting their migration. Channels are bounded by default; send/receive expose close, cancellation and capacity outcomes. Mutex guards cannot cross suspension by default; nonblocking async-aware synchronization is a distinct facility.

The concurrency memory contract is data-race freedom for safe code, with synchronization establishing happens-before relations. Atomic access and weak-memory ordering require a later detailed specification before exposure; ordinary users get safe mutex/channel abstractions first. Deadlocks, starvation and logical races remain possible and require diagnostics and workload tests. Structured concurrency alone does not make a blocking foreign function cancellable.

## Options, advantages, disadvantages and rejected alternatives

One OS thread per network connection consumes avoidable stack/scheduling resources. Green threads hide blocking but complicate stack/FFI integration. Actor isolation is useful as a library pattern but too restrictive as the only model. Unstructured futures permit leaked work. Structured stackless tasks plus controlled threads are proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: queues and child-task counts need limits against resource exhaustion. Performance: task state allocation, wakeups, contention and fairness need measurement. DX: one supervision/cancellation model across domains; synchronous helpers remain available. Implementation: transfer/share checking, group lifetime analysis, completion accounting and scheduler observability.

## Future verification

Later model/test cancellation races, join-before-drop, channel closure, non-transferable values, queue saturation, starvation and foreign blocking; record task/connection scale and memory.

## Risks and open questions

The first concurrency RFC follow-up must freeze the formal happens-before/atomic rules and executor fairness contract. No concurrency ships in v0.1.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
