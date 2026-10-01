# 2.18 — Optimization architecture

> Decision: **ARCH-OPT-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[AI-001](../requirements/domains/ai-ml.md#ai-001--exact-numeric-semantics), [PERF-002](../requirements/PERFORMANCE.md#perf-002--documented-cost-model), [PERF-003](../requirements/PERFORMANCE.md#perf-003--visible-expensive-operations), [PERF-008](../requirements/PERFORMANCE.md#perf-008--development-and-optimized-profiles), [PERF-009](../requirements/PERFORMANCE.md#perf-009--optimizable-compute-throughput), [PERF-011](../requirements/PERFORMANCE.md#perf-011--allocation-free-values), [PERF-012](../requirements/PERFORMANCE.md#perf-012--artifact-size), [PERF-015](../requirements/PERFORMANCE.md#perf-015--numerical-throughput), [SAFE-001](../requirements/SAFETY.md#safe-001--no-undefined-behavior-in-safe-code), [SAFE-008](../requirements/SAFETY.md#safe-008--defined-integer-overflow)

## Proposed decision and rationale

**Semantics-preserving optimization on verified MIR and backend IR; identical safe behavior in development and optimized profiles.**

Constant evaluation uses Cretes numeric rules, never host-language overflow behavior. MIR may remove unreachable blocks, propagate constants, inline small calls, specialize known operations and eliminate checks proven redundant. Ownership and cleanup effects constrain every transformation. A check cannot be removed because the backend would treat the invalid input as undefined behavior.

No default floating fast-math, reassociation or fused contraction changes the specified results. Explicit later numerical APIs may request alternative semantics with documented reproducibility tradeoffs. Backend alias metadata is emitted only from a proven Cretes invariant, including interactions with interior mutability and FFI. No invalid reference is manufactured merely to help optimization.

Escape/allocation elimination is an opportunity after the compiler can prove lifetime and observable behavior. Allocation failure and resource effects limit transformations: either preserve the specified failure model or specify exactly which optimization-induced allocation changes are permitted through RFC. v0.1 starts with conservative transformations. Vectorization, devirtualization, link-time optimization and interprocedural specialization are later measured additions, not mandatory first-release features.

Every pass declares preconditions, preserved invariants, invalidated analyses and a verifier. The driver can dump stages for debugging without exposing private source paths by default. Development prioritizes low compile cost and debuggability; optimized prioritizes throughput/size within the same safety contract.

## Options, advantages, disadvantages and rejected alternatives

Optimizing directly on unvalidated ASTs was rejected. Disabling safety checks for release was rejected. Aggressive unsafe floating transformations by default were rejected. A conservative verified pipeline is proposed, with advanced passes added only alongside regression evidence.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: optimizer-introduced undefined behavior can invalidate all language guarantees. Performance: inlining/code-size and compilation/runtime tradeoffs require distributions, not slogans. DX: an optimized debug session may have unavailable variables, clearly labeled. Implementation: pass-level and end-to-end differential tests.

## Future verification

Later run the same conformance corpus under all profiles, boundary arithmetic tests, cleanup side-effect tests and differential randomized programs; record compile time, runtime and size.

## Risks and open questions

No additional semantic choice is delegated to implementation. Exact surface notation belongs to Phase 3 after RFC acceptance.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
