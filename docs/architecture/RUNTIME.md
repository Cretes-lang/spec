# 2.12 — Runtime responsibilities

> Decision: **ARCH-RUNTIME-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CONC-001](../requirements/CONCURRENCY.md#conc-001--concurrent-tasks), [PERF-004](../requirements/PERFORMANCE.md#perf-004--program-startup-latency), [PERF-010](../requirements/PERFORMANCE.md#perf-010--memory-footprint-and-control), [PLAT-012](../requirements/PLATFORMS.md#plat-012--minimal-external-runtime-dependencies), [SAFE-020](../requirements/SAFETY.md#safe-020--defined-fault-behavior), [SAFE-021](../requirements/SAFETY.md#safe-021--defined-behavior-on-resource-exhaustion)

## Proposed decision and rationale

**A small linked core runtime; concurrency and protocol layers are optional later components.**

| Layer | Responsibility | Excluded responsibility |
| --- | --- | --- |
| Compiler | Types, ownership, layouts, explicit checks and lowering | HTTP, registry, cryptography implementation |
| Core runtime | Allocation adapters, minimal fault reporting, stack support, startup/exit | Mandatory scheduler or collector in every program |
| Standard library | Text, collections, files/streams, paths, arguments, environment, clocks | Web frameworks and ML training engines |
| Platform layer | Handles, filesystem, OS errors, process/thread/I/O facilities | Changing language numeric/error semantics by OS |
| Optional async runtime | Task supervision, timers, I/O drivers, blocking-work pool | User business logic or hidden detached work |
| First-party packages | HTTP/TLS, serialization, crypto and numerical integrations | Compiler semantics |

v0.1 links only its required synchronous core. It does not start scheduler threads, load network drivers or initialize cryptographic providers just because a program prints text. Initialization order is explicit and does not run arbitrary module top-level code. Fault paths avoid heap allocation and reentrant locking.

A runtime ABI is private to the compiler build. Artifacts identify the runtime revision; incompatible runtime objects are rejected at link time. Stable external interop uses the declared C ABI wrapper, not private runtime symbols. Runtime state is instance-scoped where possible so future embedding does not assume one process-global singleton.

Future runtime startup is explicit at the application boundary. A synchronous library may not secretly start a nested event loop. Resource ownership and shutdown order must be observable through documented APIs.

## Options, advantages, disadvantages and rejected alternatives

A large mandatory VM/runtime was rejected for startup and deployment cost. A zero-runtime slogan was rejected because allocation, OS integration and defined fault handling require support. Small core plus optional facilities is proposed.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: smaller linked surface reduces unnecessary facilities but is not a vulnerability guarantee. Performance: baseline footprint and startup are measured, not assumed. DX: ordinary synchronous programs need no executor setup. Implementation: version runtime symbols internally and separate feature linkage.

## Future verification

Later inspect minimal-program dependencies, startup threads, shutdown behavior, runtime-version mismatch and fault reporting under exhaustion.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
