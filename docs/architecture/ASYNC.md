# 2.14 — Async and cancellation architecture

> Decision: **ARCH-ASYNC-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CONC-004](../requirements/CONCURRENCY.md#conc-004--structured-concurrency), [CONC-006](../requirements/CONCURRENCY.md#conc-006--cancellation), [CONC-007](../requirements/CONCURRENCY.md#conc-007--deadlines-and-timeouts), [CONC-015](../requirements/CONCURRENCY.md#conc-015--blocking-and-cpu-intensive-work), [CONC-019](../requirements/CONCURRENCY.md#conc-019--unified-concurrency-model), [NET-002](../requirements/domains/networking.md#net-002--scalable-asynchronous-io), [NET-013](../requirements/domains/networking.md#net-013--backpressure)

## Proposed decision and rationale

**Explicit async effects with compiler-lowered state machines and cooperative cancellation; operation completion controls buffer lifetime.**

Async is visible in function types and call graphs, even though its spelling is undecided. Calling an async operation constructs or starts work only as the eventual API contract specifies; the design must distinguish a cold computation from a spawned task. The initial async library will use cold operation values executed by awaiting or spawning into an owned task group. Captured owners remain in the state machine until completion.

Suspension is allowed only at explicit effect boundaries. State machines cannot store references into movable frames; owning/pinned task storage and loan analysis must prove validity. Pending OS I/O owns or borrows its buffers until a terminal completion, even after the caller requests cancellation. Cancellation is a request, not evidence that the kernel stopped using memory.

An operation has states created, submitted, cancel-requested, and terminal. A single terminal result wins a completion/cancellation race. The runtime drains late completions before freeing registrations. Task-group exit waits for this drain. A timeout uses a monotonic deadline, reports partial progress where relevant and does not silently retry non-idempotent work.

Sync/async coloring is a deliberate cost. Shared pure computation, parsing, error types and data representations remain common. Provide synchronous filesystem/CLI APIs for simple scripts and async variants for services. A sync facade may drive a root runtime only at a documented application boundary; nested blocking waits on executor threads are diagnosed/rejected. DNS and filesystem operations may use a bounded blocking pool when the platform lacks an appropriate nonblocking primitive.

## Options, advantages, disadvantages and rejected alternatives

Implicit green-thread blocking would reduce coloring but complicate foreign calls and memory/stack rules. Callback-only APIs obscure ownership and propagation. Unstructured promises lack mandatory supervision. Explicit async with structured tasks is proposed; the exact await notation is deferred to Phase 3.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: keep submitted buffers alive until terminal completion. Performance: state-machine size and poll/wakeup overhead are visible costs; batching is optional. DX: task cancellation is consistent across networking, automation and AI wrappers. Implementation: cancellation state machine, resource registration and scheduler-aware blocking diagnostics.

## Future verification

Later test completion-vs-cancel races, timeout with partial writes, DNS worker cancellation, nested runtime misuse, borrowed buffers and destructor ordering.

## Risks and open questions

Cancellation cannot forcibly terminate arbitrary native calls. APIs must report that limitation and retain their resources until those calls return.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
