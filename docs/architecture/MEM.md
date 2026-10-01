# 2.5 — Memory-management model

> Decision: **ARCH-MEM-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[CONC-013](../requirements/CONCURRENCY.md#conc-013--diagnosing-unsafe-sharing), [INTOP-005](../requirements/INTEROPERABILITY.md#intop-005--memory-ownership-across-the-boundary), [PERF-010](../requirements/PERFORMANCE.md#perf-010--memory-footprint-and-control), [PERF-011](../requirements/PERFORMANCE.md#perf-011--allocation-free-values), [SAFE-001](../requirements/SAFETY.md#safe-001--no-undefined-behavior-in-safe-code), [SAFE-002](../requirements/SAFETY.md#safe-002--spatial-memory-safety), [SAFE-003](../requirements/SAFETY.md#safe-003--temporal-memory-safety), [SAFE-004](../requirements/SAFETY.md#safe-004--no-double-release), [SAFE-005](../requirements/SAFETY.md#safe-005--valid-references), [SAFE-007](../requirements/SAFETY.md#safe-007--no-use-of-uninitialized-values), [SAFE-012](../requirements/SAFETY.md#safe-012--data-race-freedom), [SAFE-013](../requirements/SAFETY.md#safe-013--deterministic-resource-release), [SAFE-023](../requirements/SAFETY.md#safe-023--memory-management-evaluation-criteria), [SEC-005](../requirements/domains/cybersecurity.md#sec-005--secret-zeroization)

## Proposed decision and rationale

**Move-based ownership with statically checked scoped borrowing; optional explicit shared ownership later, without a mandatory tracing collector.**

Each resource-owning value has one responsible owner. Assignment or passing an owning value transfers ownership unless the type is an explicitly copyable scalar or aggregate of copyable fields. An implicit copy must not allocate, duplicate a resource handle or recursively clone a heap graph. Deep duplication is an explicit operation with documented cost and failure behavior.

A borrow grants either multiple read-only views or one exclusive mutable view for its checked lifetime. The owner cannot be moved, resized, destroyed or mutably accessed incompatibly while borrowed. Borrow lifetimes are inferred from control-flow uses, bounded by the owner and reborrow ancestry. v0.1 excludes user-stored borrowed fields and self-referential values; an escaping borrow must have an explicit, checkable relation to a parameter. Phase 3 chooses notation. A compiler that cannot prove the relation rejects the program with an ownership diagnostic.

Heap allocation is explicit through owning standard-library containers and compiler-known owning indirection. Small values remain unboxed. A view into a growable sequence prevents reallocation while live. Moving a handle need not move its allocation; pinning/address-stability constraints must be represented at a future FFI boundary. Destruction is deterministic but has no constant-time bound: nested collections may take time proportional to retained objects. This is a latency risk, not a hard-real-time guarantee.

Post-v0.1 shared ownership uses explicit immutable shared handles or synchronization-protected state with atomic reference management across threads. Weak handles make cycles manageable; cycles may leak and must be diagnosable. They may never justify unsafe access. Resource guards cannot rely on a shared graph being reclaimed. Arenas are optional checked library abstractions whose values cannot escape their region. Raw manual reclamation is confined to audited unsafe implementation boundaries.

Secret buffers are uniquely owned, non-copyable and excluded from ordinary formatting; see SECURITY-DOMAIN.md. This reduces reachable copies but does not prove elimination of register, OS or foreign-library copies.

## Options, advantages, disadvantages and rejected alternatives

| Candidate | Safety and concurrency | Latency and resources | FFI/secret buffers | Learning and compiler cost |
| --- | --- | --- | --- | --- |
| Tracing GC | Can ensure temporal safety; needs separate race controls | Collector work/headroom; guards still needed for prompt close | Moving collectors need pinning; stale secret copies problematic | Familiar sharing; substantial collector/runtime engineering |
| Ownership/borrowing | Static lifetime/alias checks; supports transfer isolation | No collector pauses; destruction/allocator delays remain | Stable owned buffers and scoped access; copy control | Proposed core; substantial checker and teaching cost |
| ARC | Automatic lifetime; synchronized sharing still needed | Refcount traffic, cascaded destruction, cycles | Stable buffers; secret lifetime affected by sharing | Easier shared graphs; cycle/weak-reference complexity |
| Regions/arenas | Safe if escape rules enforced | Bulk release, potentially high retained memory | Region lifetime must cover foreign access | Useful library option; restrictive as sole model |
| Manual allocation | Unsafe without verification | Control but allocator/deallocation costs remain | Direct access; high misuse risk | Rejected as safe default |
| Hybrid | Depends on precisely separated modes | Multiple cost models and interactions | Can reserve unique secrets/buffers | Limited explicit shared handles proposed later; mandatory GC+ownership hybrid rejected initially |

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: soundness depends on the borrow checker, layout lowering and trusted libraries; memory safety is a design obligation, not a proven implementation claim. Performance: no mandatory collector, but destructor cascades and allocation fragmentation remain. DX: this choice imposes a learning cost on automation users; standard-library helpers, inferred local borrows and actionable diagnostics are release gates. Implementation: move/loan dataflow, drop flags, checked views and tests of every aliasing boundary are required.

## Future verification

Before implementation release, test move-after-use, resize-with-live-view, partial initialization, nested drops, cycle behavior when shared handles arrive, and FFI lifetime violations. Review automation task walkthroughs with novice users. SAFE-023 remains unmet until this RFC is accepted.

## Risks and open questions

Ownership diagnostic usability and pathological destruction latency require later executable evidence; neither is asserted solved. A follow-up RFC is required if measured usability defeats the target-user goals.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
