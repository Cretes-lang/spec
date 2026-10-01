# 2.7 — Safety architecture

> Decision: **ARCH-SAFETY-001** · Status: **PROPOSED** · Implementation: **Not started** · Date: 2026-09-27

[Architecture index](README.md) · [Traceability](TRACEABILITY.md) · [Risks and gates](RISKS.md)

## Context and requirements

This decision responds to the Phase 1 outcomes below. Priorities and milestone targets remain authoritative in Phase 1; a design proposal does not satisfy an implementation requirement.

[SAFE-001](../requirements/SAFETY.md#safe-001--no-undefined-behavior-in-safe-code), [SAFE-002](../requirements/SAFETY.md#safe-002--spatial-memory-safety), [SAFE-003](../requirements/SAFETY.md#safe-003--temporal-memory-safety), [SAFE-004](../requirements/SAFETY.md#safe-004--no-double-release), [SAFE-005](../requirements/SAFETY.md#safe-005--valid-references), [SAFE-006](../requirements/SAFETY.md#safe-006--null-safety), [SAFE-007](../requirements/SAFETY.md#safe-007--no-use-of-uninitialized-values), [SAFE-012](../requirements/SAFETY.md#safe-012--data-race-freedom), [SAFE-015](../requirements/SAFETY.md#safe-015--type-safety), [SAFE-016](../requirements/SAFETY.md#safe-016--explicit-and-auditable-unsafe-code), [SAFE-017](../requirements/SAFETY.md#safe-017--safe-abstractions-over-unsafe-code), [SAFE-018](../requirements/SAFETY.md#safe-018--ffi-is-an-unsafe-boundary), [SAFE-019](../requirements/SAFETY.md#safe-019--package-level-unsafe-policy), [SAFE-020](../requirements/SAFETY.md#safe-020--defined-fault-behavior), [SAFE-021](../requirements/SAFETY.md#safe-021--defined-behavior-on-resource-exhaustion), [SAFE-022](../requirements/SAFETY.md#safe-022--checked-builds-for-unsafe-code), [SEC-029](../requirements/domains/cybersecurity.md#sec-029--unsafe-and-ffi-audit-reporting)

## Proposed decision and rationale

**Compile-time ownership/type checks plus mandatory dynamic bounds and arithmetic checks, with a narrow trusted boundary.**

| Hazard | Prevention or defined response |
| --- | --- |
| Out-of-bounds | Checked index/range arithmetic; fault or explicitly fallible lookup |
| Dangling/resized view | Owner/borrow dataflow prevents invalidation |
| Double release | Unique ownership and initialization/drop-state tracking |
| Null/invalid typed reference | Explicit optional values; validate foreign pointers before safe wrapping |
| Uninitialized data | Definite assignment for every control-flow join; no observable padding |
| Type confusion | Checked conversions; no safe raw reinterpretation |
| Data races | Future transfer/share capabilities plus exclusive mutation and synchronization |
| Integer edge cases | Profile-independent checks and explicit checked/wrapping/saturating alternatives |
| Exhaustion | Fallible APIs where provided; otherwise bounded fault path and termination |

v0.1 exposes no user unsafe operations. The compiler/runtime/standard-library implementation still contains trusted code and must be audited. Later unsafe regions explicitly contain raw pointer dereference, foreign calls, unchecked layout assertions and manual memory operations. The marker does not disable ordinary type checks or excuse violation of invariants. Safe wrappers must make every legal safe call sound, including adversarial call ordering.

The trusted computing base includes compiler passes, backend, runtime, allocator, OS, native libraries and relevant hardware. Safe-language guarantees cover conforming implementations and valid trust-boundary contracts. Arbitrary foreign behavior, hardware faults, logic errors, deadlocks, denial of service and side channels are not eliminated by ownership.

Stack exhaustion requires guard pages and target-specific stack probing or an equivalent verified limit; a signal handler alone is insufficient if the stack can jump over a guard. The fault reporter must work without heap allocation and with a reserved/alternate reporting path where required. Recursive destructor chains also require a release strategy that cannot corrupt the stack.

## Options, advantages, disadvantages and rejected alternatives

Purely dynamic checking adds overhead and later failures; purely static checking cannot bound arbitrary indices or external input. Disabling checks in optimized builds contradicts the safe-code contract. A checked hybrid is proposed; unsafe escape hatches are deferred beyond v0.1.

Doing nothing leaves the linked architecture questions unresolved and prevents a coherent implementation plan. This proposal is a review candidate, not an accepted language rule.

## Security, performance, developer experience and implementation impact

Security: explicitly document what the trusted boundary assumes. Performance: proof-driven check elimination only. DX: show the unsafe operation or conflicting loans, not opaque backend failures. Implementation: maintain a hazard-to-check test matrix and sanitizer coverage for trusted native code.

## Future verification

Later test each hazard positively and negatively, fuzz parsers/lowering, inspect stack probing per target, and test faults under heap and stack exhaustion.

## Risks and open questions

Target-specific exhaustion handling must pass conformance before a target is supported. The architecture does not certify memory safety today.

Cross-cutting risk owners and closure evidence are in [RISKS.md](RISKS.md). Acceptance requires the [RFC process](https://github.com/Cretes-lang/rfcs); publication or merge of this explicitly proposed document is not acceptance.
